# Local Helper Bridge (Frontend + HTA Worker Prototype)

This folder is intentionally standalone and separate from other project parts.

## What this contains right now

- `index.html`: frontend shell with a request builder and a send flow.
- `styles.css`: UX/UI styling for a modern card-based interface with dark gradient theme.
- `app.js`: frontend behavior that builds request JSON, validates input, attempts HTA launch, and logs activity.
- `local-worker.hta`: passive Windows helper window that indicates helper status and receives startup request payloads.
- `api-contract.txt`: source-of-truth contract for request envelope, launch transport, and HTA runtime behavior.

## Present architecture (current state only)

1. User creates a request in the frontend.
2. Frontend serializes request as JSON envelope.
3. Frontend attempts to launch HTA with URL-encoded request query string.
4. HTA starts as a small blue status window and parses request on startup.
5. HTA updates status text with latest task information.
6. If browser blocks ActiveX launch path, frontend logs warning and uses simulated fallback response.

## Frontend details

### `index.html`
- Hero section explains the HTA helper is passive.
- Task form includes:
  - task type select
  - payload text field
  - priority slider
- Dispatch actions include:
  - Send to HTA worker
  - Clear
- Request preview area shows request payload and launch/simulation output.
- Activity log records actions, validation errors, and fallback warnings.

### `styles.css`
- Dark-themed gradient background with glass-like cards.
- Strong contrast and visible focus states for accessibility.
- Responsive card layout for desktop and mobile sizes.
- Semantic button variants:
  - primary (preview)
  - success (send)
  - ghost (clear)
- Activity log color-codes success/error/warning states.

### `app.js`
- `buildRequest(overrides)`: normalizes UI values into API envelope.
- `getHtaAbsolutePath()`: resolves local `.hta` path when frontend is loaded from file URL.
- `launchHtaWithRequest(request)`: uses `ActiveXObject('WScript.Shell')` to run `mshta.exe` with encoded request.
- `sendRequest()`: validates request, attempts HTA launch, otherwise falls back to simulated response.
- `logActivity()`: timestamped event stream for operator clarity.

## HTA backend details

### `local-worker.hta`
- Purposefully minimal and non-interactive.
- Opens as a small blue window and displays `.hta helper is running`.
- On startup, reads `?request=...` query parameter if present.
- Parses request with compatibility path:
  - `window.JSON.parse` when available
  - legacy parser fallback when JSON global is not present
- Updates status text with `last task: <type>` when valid request is received.
- No buttons and no manual controls; this helper is intended to be managed from HTML frontend only.

## API contract

Use `api-contract.txt` as canonical contract documentation for current integration.
If frontend and HTA implementation diverge, update both code and contract together.

## How to run (current prototype)

### Frontend (integration attempt)
- Best for Windows local usage: open `index.html` from filesystem and run in an environment where `ActiveXObject` is allowed.
- Click **Send to HTA worker**.
- If launch is blocked, UI logs warning and shows simulation fallback.

### HTA
- `local-worker.hta` can be opened directly on Windows.
- It should display a blue status window and remain passive.

## Suggested next implementation steps

1. Replace browser-dependent launch path with a more robust local bridge executable.
2. Add allowlist + argument sanitization before enabling command execution.
3. Add structured status lifecycle (`queued`, `running`, `complete`, `failed`) with retry support.
4. Add persisted logs if this will be used operationally.
