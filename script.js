const API_BASE = 'https://adahost.pe/edutrackai/api';
const TOKEN_KEY = 'edutrackai_jwt';

const loginForm = document.getElementById('login-form');
const loginFeedback = document.getElementById('login-feedback');
const authStatus = document.getElementById('auth-status');
const logoutBtn = document.getElementById('logout-btn');
const attendanceBody = document.getElementById('attendance-body');
const attendanceFeedback = document.getElementById('attendance-feedback');
const refreshAttendanceBtn = document.getElementById('refresh-attendance');
const downloadExcelBtn = document.getElementById('download-excel');
const incidentForm = document.getElementById('incident-form');
const incidentFeedback = document.getElementById('incident-feedback');

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
  renderAuthState();
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
  renderAuthState();
}

function renderAuthState() {
  const token = getToken();
  const loggedIn = Boolean(token);
  authStatus.textContent = loggedIn ? 'Sesión iniciada' : 'Sin sesión';
  logoutBtn.disabled = !loggedIn;
  refreshAttendanceBtn.disabled = !loggedIn;
  downloadExcelBtn.disabled = !loggedIn;
  incidentForm.querySelector('button[type="submit"]').disabled = !loggedIn;
}

function setFeedback(el, message, type = '') {
  el.textContent = message;
  el.classList.remove('success', 'error');
  if (type) el.classList.add(type);
}

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || response.statusText);
  }
  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    return response.json();
  }
  return response;
}

async function handleLogin(event) {
  event.preventDefault();
  setFeedback(loginFeedback, 'Autenticando...');
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  try {
    const data = await apiFetch('/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    if (!data || !data.token) {
      throw new Error('Respuesta de autenticación inválida');
    }
    setToken(data.token);
    setFeedback(loginFeedback, 'Sesión iniciada con éxito', 'success');
    await loadAttendance();
  } catch (error) {
    setFeedback(loginFeedback, `No se pudo iniciar sesión: ${error.message}`, 'error');
  }
}

async function loadAttendance() {
  if (!getToken()) {
    setFeedback(attendanceFeedback, 'Inicia sesión para ver asistencia.');
    return;
  }
  setFeedback(attendanceFeedback, 'Cargando asistencia...');
  attendanceBody.innerHTML = '<tr><td colspan="4" class="muted">Cargando...</td></tr>';
  try {
    const records = await apiFetch('/attendance', { method: 'GET' });
    if (!Array.isArray(records) || records.length === 0) {
      attendanceBody.innerHTML = '<tr><td colspan="4" class="muted">Sin datos</td></tr>';
      setFeedback(attendanceFeedback, 'No hay registros disponibles.');
      return;
    }
    attendanceBody.innerHTML = records.map((item) => `
      <tr>
        <td>${item.date ?? '—'}</td>
        <td>${item.course ?? '—'}</td>
        <td>${item.student ?? '—'}</td>
        <td>${item.status ?? '—'}</td>
      </tr>
    `).join('');
    setFeedback(attendanceFeedback, `Última actualización: ${new Date().toLocaleTimeString()}`, 'success');
  } catch (error) {
    attendanceBody.innerHTML = '<tr><td colspan="4" class="muted">Error al cargar datos</td></tr>';
    setFeedback(attendanceFeedback, `Error: ${error.message}`, 'error');
  }
}

async function downloadExcel() {
  if (!getToken()) return;
  setFeedback(attendanceFeedback, 'Preparando descarga...');
  downloadExcelBtn.disabled = true;
  try {
    const response = await apiFetch('/attendance/export', { method: 'GET' });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'asistencia.xlsx';
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    setFeedback(attendanceFeedback, 'Descarga iniciada', 'success');
  } catch (error) {
    setFeedback(attendanceFeedback, `No se pudo descargar: ${error.message}`, 'error');
  } finally {
    downloadExcelBtn.disabled = false;
  }
}

async function submitIncident(event) {
  event.preventDefault();
  if (!getToken()) return;
  const payload = {
    student: document.getElementById('incident-student').value,
    course: document.getElementById('incident-course').value,
    description: document.getElementById('incident-description').value,
    severity: document.getElementById('incident-severity').value,
  };
  setFeedback(incidentFeedback, 'Enviando incidencia...');
  try {
    await apiFetch('/incidents', { method: 'POST', body: JSON.stringify(payload) });
    setFeedback(incidentFeedback, 'Incidencia registrada', 'success');
    incidentForm.reset();
  } catch (error) {
    setFeedback(incidentFeedback, `Error: ${error.message}`, 'error');
  }
}

function init() {
  renderAuthState();
  loginForm.addEventListener('submit', handleLogin);
  logoutBtn.addEventListener('click', () => {
    clearToken();
    setFeedback(loginFeedback, 'Sesión cerrada');
    attendanceBody.innerHTML = '<tr><td colspan="4" class="muted">Sin datos</td></tr>';
  });
  refreshAttendanceBtn.addEventListener('click', loadAttendance);
  downloadExcelBtn.addEventListener('click', downloadExcel);
  incidentForm.addEventListener('submit', submitIncident);

  if (getToken()) {
    loadAttendance();
  }
}

document.addEventListener('DOMContentLoaded', init);
