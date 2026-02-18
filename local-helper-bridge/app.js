const taskTypeEl = document.getElementById('taskType');
const taskPayloadEl = document.getElementById('taskPayload');
const taskPriorityEl = document.getElementById('taskPriority');
const previewBtn = document.getElementById('previewBtn');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const requestPreviewEl = document.getElementById('requestPreview');
const activityLogEl = document.getElementById('activityLog');

let currentRequest = null;

function buildRequest() {
  return {
    version: '1.0',
    source: 'local-helper-bridge-ui',
    timestamp: new Date().toISOString(),
    task: {
      type: taskTypeEl.value,
      payload: taskPayloadEl.value.trim(),
      priority: Number(taskPriorityEl.value)
    }
  };
}

function logActivity(message, state = 'success') {
  const li = document.createElement('li');
  li.className = state;
  li.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  activityLogEl.prepend(li);
}

function previewRequest() {
  currentRequest = buildRequest();
  requestPreviewEl.textContent = JSON.stringify(currentRequest, null, 2);
  logActivity('Built request payload.');
}

function validateRequest(request) {
  if (!request.task.payload) {
    return 'Payload is required before dispatch.';
  }

  if (request.task.payload.length > 260) {
    return 'Payload is too long for classic Windows path/command usage.';
  }

  return null;
}

function mockHtaBackend(request) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        accepted: true,
        worker: 'local-worker.hta',
        requestId: Math.random().toString(16).slice(2),
        echo: request.task
      });
    }, 380);
  });
}

async function sendRequest() {
  if (!currentRequest) {
    previewRequest();
  }

  const validationError = validateRequest(currentRequest);
  if (validationError) {
    logActivity(validationError, 'error');
    return;
  }

  sendBtn.disabled = true;
  sendBtn.textContent = 'Sending...';

  const response = await mockHtaBackend(currentRequest);
  requestPreviewEl.textContent = `${requestPreviewEl.textContent}\n\n// Simulated HTA response\n${JSON.stringify(response, null, 2)}`;
  logActivity(`Request dispatched. Worker response id: ${response.requestId}`);

  sendBtn.disabled = false;
  sendBtn.textContent = 'Send to HTA worker';
}

function clearState() {
  currentRequest = null;
  taskPayloadEl.value = '';
  requestPreviewEl.textContent = '';
  logActivity('Cleared current request state.', 'success');
}

previewBtn.addEventListener('click', previewRequest);
sendBtn.addEventListener('click', sendRequest);
clearBtn.addEventListener('click', clearState);

previewRequest();
logActivity('UI initialized and ready.');
