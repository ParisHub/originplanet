# Local Helper Bridge (Manual Dual-Open)

## What exists now

- `index.html`: one centered button UI that sends one command (`open-c`).
- `styles.css`: minimal polished styling for centered one-button layout plus status tones.
- `app.js`: writes command to localStorage and listens for HTA acknowledgement.
- `local-worker.hta`: passive blue helper window polling for commands; opens `C:\` in Explorer when instructed.
- `api-contract.txt`: current command/ack contract and runtime requirements.

## Architecture (present state)

1. User manually opens `local-worker.hta`.
2. User manually opens `index.html`.
3. HTML button click writes command JSON to localStorage.
4. HTA polling loop reads command and executes `explorer.exe C:\`.
5. HTA writes acknowledgement JSON to localStorage.
6. HTML displays ack status.

## Frontend notes

### `index.html`
- One centered action button: **Open C:\ in Explorer**.
- Static hint reminds operator that HTA must be opened first.
- Live status text confirms sent/ack/warning/error outcomes.

### `styles.css`
- Fullscreen dark-blue gradient background.
- Centered CTA with focus/hover states.
- Status tone colors for success/warning/error.

### `app.js`
- Uses safe localStorage detection before read/write.
- Writes command object to `localHelperBridge.command`.
- Listens for `storage` updates on `localHelperBridge.ack`.
- Shows warning if no ack is observed within timeout window.
- Contains no auto-launch behavior and no simulated backend.

## HTA notes

### `local-worker.hta`
- Passive blue status window, no user controls.
- Polls localStorage every 500ms for command key updates.
- Executes only known action `open-c` by running `explorer.exe C:\`.
- Publishes ack payload to `localHelperBridge.ack`.
- If localStorage is unavailable in the HTA host, shows warning text and avoids script crashes.

## How to run

1. On Windows, open `local-helper-bridge/local-worker.hta` first.
2. Then open `local-helper-bridge/index.html`.
3. Click **Open C:\ in Explorer**.
4. Explorer should open `C:\`, and HTML should show an acknowledgement status.
