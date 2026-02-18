# Local Helper Bridge (Minimal)

## What exists now

- `index.html`: single centered button UI.
- `styles.css`: minimal polished styling for centered one-button layout.
- `app.js`: button click handler that launches `.hta` locally.
- `local-worker.hta`: immediately opens `C:\` in Explorer on startup.
- `api-contract.txt`: concise runtime contract for this exact behavior.

## Architecture (present state)

1. Click button in HTML.
2. HTML launches `mshta.exe` with `local-worker.hta` path.
3. HTA starts and runs `explorer.exe C:\`.
4. Explorer opens `C:\`.

## Frontend notes

### `index.html`
- One centered action button: **Open C:\ in Explorer**.
- Small status text at bottom for immediate feedback.

### `styles.css`
- Fullscreen dark-blue gradient background.
- Centered call-to-action button with clear focus/hover behavior.
- Minimal status text styling.

### `app.js`
- Resolves local `.hta` path from current `file:///` location.
- Uses `ActiveXObject('WScript.Shell')` to run `mshta.exe`.
- Sets simple status messages for ready, launch, and failure states.

## HTA notes

### `local-worker.hta`
- Passive blue window.
- No user controls.
- On load, calls `explorer.exe C:\`.
- Displays status text in-window.

## How to run

1. On Windows, open `local-helper-bridge/index.html` directly from disk.
2. Click **Open C:\ in Explorer**.
3. HTA helper launches and opens File Explorer at `C:\`.
