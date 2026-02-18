# Local Helper Bridge (Frontend + HTA Worker Prototype)

This folder is intentionally standalone and separate from other project parts.

## What this contains right now

- `index.html`: the lightweight frontend shell with a polished two-step flow (build request, dispatch request).
- `styles.css`: UX/UI styling for a modern card-based interface with dark gradient theme.
- `app.js`: frontend behavior that builds request JSON, validates it, simulates HTA dispatch, and logs activity.
- `local-worker.hta`: a Windows HTA backend placeholder that parses requests and logs responses.
- `api-contract.txt`: current source-of-truth contract describing request and response structures.

## Present architecture (no history, current state only)

1. User selects a task type and enters payload in the frontend.
2. Frontend creates a request envelope (`version`, `source`, `timestamp`, `task`).
3. Frontend validates payload before dispatch.
4. Dispatch currently uses a simulated backend response in-browser.
5. HTA file includes compatible parsing and response structure for future direct wiring.

## Frontend details

### `index.html`
- Hero section explains this is a future-ready local automation bridge.
- Task form includes:
  - task type select
  - payload text field
  - priority slider
- Request preview area shows JSON payload and response.
- Activity log records all actions and validation outcomes.

### `styles.css`
- Dark-themed gradient background with glass-like cards.
- Strong contrast and visible focus states for accessibility.
- Responsive layout: side-by-side cards on larger screens, stacked on smaller devices.
- Buttons use semantic color cues (primary, success, ghost).

### `app.js`
- `buildRequest()`: normalizes UI values into the API envelope.
- `validateRequest()`: blocks empty payload and oversized input.
- `mockHtaBackend()`: async placeholder for eventual HTA bridge transport.
- `logActivity()`: timestamped event stream for operator clarity.
- Automatically generates an initial preview on load.

## HTA backend details

### `local-worker.hta`
- Provides a minimal windowed interface with a demo button.
- `executeRequest(rawJson)` currently:
  - parses incoming JSON
  - logs task type and payload
  - returns a queue acknowledgment JSON response
- Includes comments for future local Windows automation integration points.

## API contract

Use `api-contract.txt` as the current canonical contract description.
If frontend and HTA implementations diverge, update both code and the contract file together.

## How to run (current prototype)

### Frontend
- Open `index.html` in a browser.
- Preview and send requests to observe serialization + simulated backend responses.

### HTA
- On Windows, run `local-worker.hta` directly.
- Use “Run demo request” to test parse + response behavior.

## Suggested next implementation steps

1. Replace `mockHtaBackend` with real transport.
2. Add task allowlist and argument sanitization.
3. Add response status polling and richer error display.
4. Add persisted logs if this will be used operationally.
