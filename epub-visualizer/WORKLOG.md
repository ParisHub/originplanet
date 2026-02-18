# WORKLOG (for future me)

This document captures *what* was built and *why* specific implementation choices were made.

## Goal

Create a standalone `.epub` visualizer in a separate folder that exposes chapter structure clearly, with chapter-by-chapter viewing.

## Design decisions

### 1) Standalone static app
- Picked plain HTML/CSS/JS (no build step).
- Reason: zero project coupling, easy to copy into another repo.

### 2) EPUB parsing strategy
- Used `JSZip` to read EPUB internals client-side.
- Parsing flow:
  - `META-INF/container.xml` -> OPF package path
  - OPF `manifest` + `spine`
  - TOC via nav XHTML (preferred)
  - fallback TOC via NCX
- Reason: this follows normal EPUB packaging and covers EPUB2 + EPUB3 in common cases.

### 3) Separate chapter surfaces
- Two explicit panels:
  - TOC list (logical chapter map)
  - Spine list (physical reading order documents)
- Reason: user asked to "display all different chapters etc separately".

### 4) Preview rendering
- Uses `iframe.srcdoc` to isolate chapter content.
- Tries to inline:
  - linked stylesheets
  - image sources
- Reason: improves fidelity without needing filesystem URLs.

### 5) Resilience
- Status text updates for load errors and partial parsing outcomes.
- Missing nav/toc still shows spine content.

## Caveats I intentionally accepted

- JSZip CDN dependency to keep repo small and avoid vendoring third-party artifacts.
- Only common image MIME types guessed.
- No global CSS rewriting for relative URLs inside imported stylesheets yet.

## Future improvements

1. Vendor JSZip locally for offline usage.
2. Parse and inline font files and media assets.
3. Rewrite relative URLs in inlined CSS (`url(...)`).
4. Add chapter search/filter.
5. Add previous/next controls for spine navigation.
6. Add EPUB metadata panel (title, creator, language, identifier).

## Manual verification checklist used

- [x] App loads in browser.
- [x] File chooser accepts `.epub`.
- [x] Spine list renders.
- [x] TOC list renders when nav/NCX is present.
- [x] Clicking TOC/spine item updates iframe preview.
- [x] Status message updates on success/failure.
