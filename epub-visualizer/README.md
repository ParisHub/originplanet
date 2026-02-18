# EPUB Chapter Visualizer

A standalone browser-based `.epub` visualizer that separates and previews:

- Table of contents entries (chapters/sections)
- Spine documents in reading order

## Why this exists

This folder is intentionally separate from the existing project files, so it can be moved or deleted independently.

## Quick start

Because browsers block some local-file features, run a lightweight HTTP server in this folder:

```bash
cd epub-visualizer
python3 -m http.server 4173
```

Then open:

- `http://localhost:4173`

## Features

- **Separated chapter surfaces**
  - TOC entries (logical chapter structure)
  - Spine entries (document reading order)
- **View mode toggle for each chapter**
  - **Rendered**: iframe preview with inlined assets where possible
  - **Source**: raw chapter XHTML/HTML markup in a code-style text block

## How it works

1. Reads the selected `.epub` file as a ZIP archive via `JSZip`.
2. Parses `META-INF/container.xml` to locate the OPF package document.
3. Parses OPF `manifest` and `spine`.
4. Attempts to locate a nav document first (`.xhtml` nav).
5. Falls back to NCX (`.ncx`) if nav is missing.
6. Renders:
   - TOC entries in the Chapters panel
   - Spine items in the Spine panel
7. Clicking an item loads the chapter and stores both:
   - Raw source markup
   - Processed rendered markup
8. The view toggle switches between source and rendered modes without reloading the chapter from disk.

## Known limitations

- JSZip is loaded from a CDN (`jsdelivr`), so network access is required unless you vendor JSZip locally.
- Some EPUBs use advanced scripting/fonts/media that are not currently inlined.
- TOC detection is best-effort; unusual EPUB packaging may need parser tweaks.

## Files

- `index.html` — UI shell and toggle controls
- `styles.css` — layout and component styling (including toggle/source panel styles)
- `app.js` — EPUB parsing + chapter rendering/source toggle logic
- `WORKLOG.md` — implementation notes intended for future maintenance
