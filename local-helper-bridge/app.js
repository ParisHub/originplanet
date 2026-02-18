const openCBtn = document.getElementById('openCBtn');
const statusEl = document.getElementById('status');

function setStatus(text) {
  statusEl.textContent = text;
}

function getHtaAbsolutePath() {
  const baseUrl = window.location.href.slice(0, window.location.href.lastIndexOf('/'));
  const htaUrl = `${baseUrl}/local-worker.hta`;

  if (!htaUrl.startsWith('file:///')) {
    return null;
  }

  return decodeURIComponent(htaUrl.replace('file:///', '').replace(/\//g, '\\'));
}

function launchHtaToOpenC() {
  const htaPath = getHtaAbsolutePath();

  if (!htaPath) {
    setStatus('Open this HTML via file:/// on Windows so HTA can be launched.');
    return;
  }

  try {
    const shell = new ActiveXObject('WScript.Shell');
    shell.Run(`mshta.exe "${htaPath}"`, 1, false);
    setStatus('Launching HTA helper...');
  } catch (error) {
    setStatus(`Failed to launch HTA: ${error.message}`);
  }
}

openCBtn.addEventListener('click', launchHtaToOpenC);
setStatus('Ready.');
