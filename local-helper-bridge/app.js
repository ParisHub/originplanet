const openCBtn = document.getElementById('openCBtn');
const statusEl = document.getElementById('status');

const BRIDGE_COMMAND_KEY = 'localHelperBridge.command';
const BRIDGE_ACK_KEY = 'localHelperBridge.ack';
const ACK_TIMEOUT_MS = 4500;

function setStatus(text, tone = 'info') {
  statusEl.textContent = text;
  statusEl.dataset.tone = tone;
}

function getStorageSafe() {
  try {
    if (window.localStorage && typeof window.localStorage.getItem === 'function') {
      return window.localStorage;
    }
  } catch (_error) {
    return null;
  }

  return null;
}

function parseJsonSafe(raw) {
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw);
  } catch (_error) {
    return null;
  }
}

function sendOpenCCommand() {
  const storage = getStorageSafe();

  if (!storage) {
    setStatus('localStorage is unavailable in this browser context.', 'error');
    return;
  }

  const command = {
    id: `cmd-${Date.now()}`,
    action: 'open-c',
    createdAt: new Date().toISOString(),
    source: 'local-helper-bridge-ui'
  };

  storage.setItem(BRIDGE_COMMAND_KEY, JSON.stringify(command));
  setStatus('Command sent. Waiting for HTA acknowledgment...', 'pending');

  window.setTimeout(() => {
    const ack = parseJsonSafe(storage.getItem(BRIDGE_ACK_KEY));

    if (ack && ack.commandId === command.id && ack.status === 'ok') {
      return;
    }

    setStatus('No HTA acknowledgment yet. Ensure local-worker.hta is open and has localStorage access.', 'warning');
  }, ACK_TIMEOUT_MS);
}

window.addEventListener('storage', (event) => {
  if (event.key !== BRIDGE_ACK_KEY || !event.newValue) {
    return;
  }

  const ack = parseJsonSafe(event.newValue);

  if (!ack) {
    return;
  }

  if (ack.status === 'ok') {
    setStatus(`HTA acknowledged command (${ack.commandId}). Explorer should be open.`, 'success');
    return;
  }

  setStatus(`HTA reported an error: ${ack.message || 'unknown error'}`, 'error');
});

openCBtn.addEventListener('click', sendOpenCCommand);
setStatus('Ready. Open local-worker.hta, then click the button.', 'info');
