const API_BASE = 'http://127.0.0.1:8000';

function saveToken(token) {
  localStorage.setItem('pennywise_token', token);
}

function getToken() {
  return localStorage.getItem('pennywise_token');
}

function clearToken() {
  localStorage.removeItem('pennywise_token');
}

async function apiLogin(email, password) {
  const body = new URLSearchParams();
  body.append('username', email);
  body.append('password', password);

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Login failed');
  }

  const data = await res.json();
  saveToken(data.access_token);
  return data;
}

async function apiRegister(email, password) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Registration failed');
  }

  return res.json();
}

async function authFetch(path, options = {}) {
  const token = getToken();

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    },
  });

  if (res.status === 401) {
    clearToken();
    window.location.href = 'index.html';
    throw new Error('Session expired, please log in again.');
  }

  return res;
}