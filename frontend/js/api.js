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

async function apiUploadCSV(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await authFetch('/transactions/upload', {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Upload failed');
  }

  return res.json();
}

async function apiGetSummary() {
  const res = await authFetch('/transactions/summary');

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not load summary');
  }

  return res.json();
}

async function apiAskRag(question) {
  const res = await authFetch('/rag/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Something went wrong');
  }

  return res.json();
}

async function apiAskInsight(question) {
  const res = await authFetch('/insights/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Something went wrong');
  }

  return res.json();
}

async function apiDeleteAccount() {
  const res = await authFetch('/auth/me', {
    method: 'DELETE',
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not delete account');
  }

  return res.json();
}

async function apiGetTransactions() {
  const res = await authFetch('/transactions/');

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not load transactions');
  }

  return res.json();
}

async function apiClearTransactions() {
  const res = await authFetch('/transactions/', {
    method: 'DELETE',
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not clear transactions');
  }

  return res.json();
}

async function apiChangePassword(currentPassword, newPassword) {
  const res = await authFetch('/auth/password', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      current_password: currentPassword,
      new_password: newPassword,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Could not change password');
  }

  return res.json();
}