# Local Helper Bridge (Frontend + HTA Worker Prototype)

This folder is intentionally standalone and separate from other project parts.

## What this contains right now

- `index.html`: frontend shell with a two-step request flow plus a direct "hello popup" action.
- `styles.css`: UX/UI styling for a modern card-based interface with dark gradient theme.
- `app.js`: frontend behavior that builds request JSON, validates, attempts auto-launch of HTA, and logs activity.
- `local-worker.hta`: Windows HTA backend placeholder that can execute startup requests instantly.
- `api-contract.txt`: current source-of-truth contract for request/response and launch transport.

## Present architecture (current state only)

1. User creates a request in the frontend.
2. Frontend serializes request as JSON envelope.
3. Frontend attempts to launch HTA with URL-encoded request query string.
4. HTA auto-parses startup request and executes immediately.
5. For now, `show-toast` with payload `hello` opens a small popup that says hello.
6. If browser blocks ActiveX launch path, frontend logs warning and uses simulated fallback response.

## Frontend details

### `index.html`
- Hero section explains auto-launch behavior and fallback behavior.
- Task form includes:
  - task type select
  - payload text field
  - priority slider
- Dispatch actions include:
  - Send to HTA worker
  - Open Hello window via HTA
  - Clear
- Request preview area shows request payload and launch/simulation output.
- Activity log records all actions, errors, and fallback warnings.

### `styles.css`
- Dark-themed gradient background with glass-like cards.
- Strong contrast and visible focus states for accessibility.
- Responsive card layout for desktop and mobile sizes.
- Semantic button variants:
  - primary (preview)
  - success (send)
  - accent (hello popup)
  - ghost (clear)
- Activity log color-codes success/error/warning states.

### `app.js`
- `buildRequest(overrides)`: normalizes UI values into API envelope, supports forced overrides.
- `getHtaAbsolutePath()`: resolves local `.hta` path when frontend is loaded from file URL.
- `launchHtaWithRequest(request)`: uses `ActiveXObject('WScript.Shell')` to run `mshta.exe` with encoded request.
- `sendRequest()`: validates request, attempts HTA launch, otherwise falls back to simulated response.
- `sendHelloWindowRequest()`: sends a prepared `show-toast` + `hello` request.
- `logActivity()`: timestamped event stream for operator clarity.

## HTA backend details

### `local-worker.hta`
- Starts with `processStartupRequest()` on body load.
- Reads `?request=...` from query string and executes immediately if present.
- `executeRequest(rawJson)` currently:
  - parses incoming JSON
  - logs task type and payload
  - if task is `show-toast` with payload `hello`, opens a small popup saying hello
  - returns queue acknowledgment JSON
- Includes comments for future Windows automation expansion points.

## API contract

Use `api-contract.txt` as canonical contract documentation for current integration.
If frontend and HTA implementation diverge, update both code and contract together.

## How to run (current prototype)

### Frontend (integration attempt)
- Best for Windows local usage: open `index.html` from filesystem and run in an environment where `ActiveXObject` is allowed.
- Click **Send to HTA worker** or **Open Hello window via HTA**.
- If launch is blocked, the UI will clearly log warning + simulation fallback.

### HTA
- On Windows, run `local-worker.hta` directly for manual testing.
- Use **Run demo request** to test hello popup + response path without frontend.

## Suggested next implementation steps

1. Replace browser-dependent launch path with a more robust local bridge executable.
2. Add allowlist + argument sanitization before enabling command execution.
3. Add structured status lifecycle (`queued`, `running`, `complete`, `failed`) with retry support.
4. Add persisted logs if this will be used operationally.
