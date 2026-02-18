const input = document.getElementById("epubInput");
const statusNode = document.getElementById("status");
const tocList = document.getElementById("tocList");
const spineList = document.getElementById("spineList");
const chapterTitle = document.getElementById("chapterTitle");
const chapterFrame = document.getElementById("chapterFrame");
const chapterSource = document.getElementById("chapterSource");
const renderedViewBtn = document.getElementById("renderedViewBtn");
const sourceViewBtn = document.getElementById("sourceViewBtn");

let zipRef = null;
let opfBasePath = "";
let spineDocuments = [];
let currentViewMode = "rendered";
let currentRenderedMarkup = "";
let currentSourceMarkup = "";

renderedViewBtn.addEventListener("click", () => setViewMode("rendered"));
sourceViewBtn.addEventListener("click", () => setViewMode("source"));

input.addEventListener("change", async (event) => {
  const [file] = event.target.files;
  if (!file) {
    return;
  }

  if (typeof JSZip === "undefined") {
    updateStatus("JSZip did not load. Check network/CDN access.");
    return;
  }

  resetView();
  updateStatus(`Loading ${file.name}...`);

  try {
    const buffer = await file.arrayBuffer();
    zipRef = await JSZip.loadAsync(buffer);

    const containerPath = "META-INF/container.xml";
    const containerXml = await readZipText(containerPath);
    const rootfilePath = getRootfilePath(containerXml);

    const opfXml = await readZipText(rootfilePath);
    opfBasePath = rootfilePath.includes("/")
      ? rootfilePath.slice(0, rootfilePath.lastIndexOf("/") + 1)
      : "";

    const { manifestById, spineItemRefs } = parseOpf(opfXml);
    spineDocuments = spineItemRefs
      .map((idref) => {
        const item = manifestById.get(idref);
        if (!item) return null;
        return {
          id: idref,
          href: item.href,
          mediaType: item.mediaType,
          path: toAbsoluteOpfPath(item.href),
        };
      })
      .filter(Boolean);

    renderSpine(spineDocuments);

    const navDoc = findNavDocument(manifestById);
    if (navDoc) {
      const navPath = toAbsoluteOpfPath(navDoc.href);
      const navHtml = await readZipText(navPath);
      const tocEntries = parseNavDocument(navHtml, navPath);
      renderToc(tocEntries);
    } else {
      const ncxDoc = findNcxDocument(manifestById);
      if (ncxDoc) {
        const ncxXml = await readZipText(toAbsoluteOpfPath(ncxDoc.href));
        renderToc(parseNcx(ncxXml));
      } else {
        updateStatus("Loaded EPUB, but no nav/toc document found. Showing spine only.");
      }
    }

    if (spineDocuments.length > 0) {
      await openDocument(spineDocuments[0].path, "First spine document");
    }

    updateStatus(`Loaded ${file.name}: ${spineDocuments.length} spine item(s).`);
  } catch (error) {
    console.error(error);
    updateStatus(`Failed to parse EPUB: ${error.message}`);
  }
});

function resetView() {
  tocList.innerHTML = "";
  spineList.innerHTML = "";
  chapterTitle.textContent = "Chapter Preview";
  currentRenderedMarkup = "";
  currentSourceMarkup = "";
  chapterFrame.srcdoc = "";
  chapterSource.textContent = "";
  setViewMode("rendered");
}

function setViewMode(mode) {
  currentViewMode = mode;
  const showRendered = mode === "rendered";

  renderedViewBtn.classList.toggle("active", showRendered);
  sourceViewBtn.classList.toggle("active", !showRendered);

  chapterFrame.hidden = !showRendered;
  chapterSource.hidden = showRendered;

  if (showRendered) {
    chapterFrame.srcdoc = currentRenderedMarkup;
    return;
  }

  chapterSource.textContent = currentSourceMarkup || "No chapter source loaded yet.";
}

function updateStatus(message) {
  statusNode.textContent = message;
}

async function readZipText(path) {
  const entry = zipRef.file(path);
  if (!entry) {
    throw new Error(`Missing file in archive: ${path}`);
  }
  return entry.async("text");
}

function getRootfilePath(containerXml) {
  const doc = new DOMParser().parseFromString(containerXml, "application/xml");
  const rootfile = doc.querySelector("rootfile");
  if (!rootfile) {
    throw new Error("container.xml has no rootfile element");
  }
  const fullPath = rootfile.getAttribute("full-path");
  if (!fullPath) {
    throw new Error("rootfile missing full-path");
  }
  return fullPath;
}

function parseOpf(opfXml) {
  const doc = new DOMParser().parseFromString(opfXml, "application/xml");
  const manifestById = new Map();

  doc.querySelectorAll("manifest > item").forEach((item) => {
    const id = item.getAttribute("id");
    const href = item.getAttribute("href");
    const mediaType = item.getAttribute("media-type") || "unknown";
    if (id && href) {
      manifestById.set(id, { href, mediaType });
    }
  });

  const spineItemRefs = Array.from(doc.querySelectorAll("spine > itemref"))
    .map((itemRef) => itemRef.getAttribute("idref"))
    .filter(Boolean);

  return { manifestById, spineItemRefs };
}

function findNavDocument(manifestById) {
  for (const [, item] of manifestById.entries()) {
    if (item.mediaType === "application/xhtml+xml" && item.href.toLowerCase().includes("nav")) {
      return item;
    }
  }
  return null;
}

function findNcxDocument(manifestById) {
  for (const [, item] of manifestById.entries()) {
    if (item.mediaType === "application/x-dtbncx+xml") {
      return item;
    }
  }
  return null;
}

function parseNavDocument(navHtml, navPath) {
  const doc = new DOMParser().parseFromString(navHtml, "application/xhtml+xml");
  const nav = doc.querySelector('nav[epub\\:type="toc"], nav[*|type="toc"], nav');
  if (!nav) return [];

  const results = [];

  function walkList(list, depth = 0) {
    if (!list) return;
    list.querySelectorAll(":scope > li").forEach((li) => {
      const link = li.querySelector(":scope > a");
      const label = link ? link.textContent.trim() : li.textContent.trim();
      const href = link ? link.getAttribute("href") : null;

      if (href) {
        const path = resolveRelativePath(navPath, href.split("#")[0]);
        results.push({ label, path, depth });
      }

      walkList(li.querySelector(":scope > ol, :scope > ul"), depth + 1);
    });
  }

  walkList(nav.querySelector("ol, ul"), 0);
  return results;
}

function parseNcx(ncxXml) {
  const doc = new DOMParser().parseFromString(ncxXml, "application/xml");
  const navPoints = Array.from(doc.querySelectorAll("navMap > navPoint"));
  const results = [];

  function walk(points, depth = 0) {
    points.forEach((point) => {
      const labelNode = point.querySelector("navLabel > text");
      const contentNode = point.querySelector("content");
      const href = contentNode?.getAttribute("src")?.split("#")[0];
      if (href) {
        results.push({
          label: labelNode?.textContent?.trim() || "Untitled",
          path: toAbsoluteOpfPath(href),
          depth,
        });
      }
      const children = Array.from(point.querySelectorAll(":scope > navPoint"));
      walk(children, depth + 1);
    });
  }

  walk(navPoints, 0);
  return results;
}

function toAbsoluteOpfPath(href) {
  return resolveRelativePath(opfBasePath, href);
}

function resolveRelativePath(baseFile, relativePath) {
  const normalizedBase = baseFile.endsWith("/")
    ? baseFile
    : baseFile.slice(0, baseFile.lastIndexOf("/") + 1);

  const stack = normalizedBase.split("/").filter(Boolean);
  const parts = relativePath.split("/").filter(Boolean);

  parts.forEach((part) => {
    if (part === ".") return;
    if (part === "..") {
      stack.pop();
      return;
    }
    stack.push(part);
  });

  return stack.join("/");
}

function renderToc(entries) {
  tocList.innerHTML = "";
  if (entries.length === 0) {
    tocList.innerHTML = "<li>No TOC entries found.</li>";
    return;
  }

  entries.forEach((entry, index) => {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.className = "toc-item";
    button.type = "button";

    const depthPrefix = entry.depth > 0 ? "↳ ".repeat(entry.depth) : "";
    button.innerHTML = `${depthPrefix}${escapeHtml(entry.label)} <span class=\"toc-depth\">(${entry.path})</span>`;
    button.addEventListener("click", () => openDocument(entry.path, entry.label || `TOC entry ${index + 1}`));

    item.appendChild(button);
    tocList.appendChild(item);
  });
}

function renderSpine(items) {
  spineList.innerHTML = "";
  if (items.length === 0) {
    spineList.innerHTML = "<li>No spine items found.</li>";
    return;
  }

  items.forEach((item, index) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.className = "spine-item";
    button.type = "button";
    button.textContent = `${index + 1}. ${item.path} [${item.mediaType}]`;
    button.addEventListener("click", () => openDocument(item.path, `Spine ${index + 1}`));

    li.appendChild(button);
    spineList.appendChild(li);
  });
}

async function openDocument(path, label) {
  chapterTitle.textContent = label;

  try {
    const rawHtml = await readZipText(path);
    const embedded = await inlineReferencedAssets(rawHtml, path);
    currentSourceMarkup = rawHtml;
    currentRenderedMarkup = embedded;
  } catch (error) {
    currentSourceMarkup = `Unable to load ${path}\n\n${error.message}`;
    currentRenderedMarkup = `<pre>${escapeHtml(currentSourceMarkup)}</pre>`;
  }

  setViewMode(currentViewMode);
}

async function inlineReferencedAssets(html, sourcePath) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "application/xhtml+xml");

  const imageNodes = Array.from(doc.querySelectorAll("img[src]"));
  for (const image of imageNodes) {
    const src = image.getAttribute("src");
    if (!src || src.startsWith("data:")) continue;
    const extPath = resolveRelativePath(sourcePath, src.split("#")[0]);
    const entry = zipRef.file(extPath);
    if (!entry) continue;

    const bytes = await entry.async("base64");
    const mimeType = guessMimeType(extPath);
    image.setAttribute("src", `data:${mimeType};base64,${bytes}`);
  }

  const styleNodes = Array.from(doc.querySelectorAll("link[rel='stylesheet'][href]"));
  for (const link of styleNodes) {
    const href = link.getAttribute("href");
    const extPath = resolveRelativePath(sourcePath, href.split("#")[0]);
    const entry = zipRef.file(extPath);
    if (!entry) continue;
    const css = await entry.async("text");
    const styleTag = doc.createElement("style");
    styleTag.textContent = css;
    link.replaceWith(styleTag);
  }

  return new XMLSerializer().serializeToString(doc);
}

function guessMimeType(path) {
  const lowered = path.toLowerCase();
  if (lowered.endsWith(".png")) return "image/png";
  if (lowered.endsWith(".jpg") || lowered.endsWith(".jpeg")) return "image/jpeg";
  if (lowered.endsWith(".gif")) return "image/gif";
  if (lowered.endsWith(".svg")) return "image/svg+xml";
  if (lowered.endsWith(".webp")) return "image/webp";
  return "application/octet-stream";
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
