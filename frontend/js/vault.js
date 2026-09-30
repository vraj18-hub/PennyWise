(function () {
  // ---- Guard: redirect to login if no token ----
  if (!getToken()) {
    window.location.href = 'index.html';
    return;
  }

  // ---- Grab DOM elements ----
  const emailEl      = document.getElementById('userEmail');
  const createdEl    = document.getElementById('userCreated');
  const txnCountEl   = document.getElementById('txnCount');
  const txnTableEl   = document.getElementById('txnTableArea');
  const clearBtn     = document.getElementById('clearBtn');
  const clearStatus  = document.getElementById('clearStatus');
  const currentPwEl  = document.getElementById('currentPw');
  const newPwEl      = document.getElementById('newPw');
  const confirmPwEl  = document.getElementById('confirmPw');
  const changePwBtn  = document.getElementById('changePwBtn');
  const pwStatusEl   = document.getElementById('pwStatus');
  const deleteBtn    = document.getElementById('deleteBtn');
  const statusEl     = document.getElementById('deleteStatus');
  const logoutBtn    = document.getElementById('logoutBtn');

  // ---- Load profile on page open ----
  async function loadProfile() {
    try {
      const res = await authFetch('/auth/me');
      if (!res.ok) throw new Error('Could not load profile');
      const user = await res.json();

      emailEl.textContent = user.email;

      // If the backend returns created_at, format it nicely
      if (user.created_at) {
        createdEl.textContent = new Date(user.created_at).toLocaleDateString();
      }
    } catch (err) {
      emailEl.textContent = 'Error loading profile';
    }
  }

  // ---- Load transaction history ----
  async function loadTransactions() {
    try {
      const transactions = await apiGetTransactions();

      if (transactions.length === 0) {
        txnTableEl.innerHTML = '<div class="empty-history">No transactions uploaded yet.</div>';
        txnCountEl.textContent = '';
        return;
      }

      txnCountEl.textContent = `Showing ${transactions.length} transaction${transactions.length === 1 ? '' : 's'}`;

      let html = `
        <table class="txn-table">
          <thead>
            <tr><th>Date</th><th>Description</th><th>Category</th><th>Amount</th></tr>
          </thead>
          <tbody>
      `;

      for (const t of transactions) {
        const date = new Date(t.date).toLocaleDateString();
        const amt = Number(t.amount).toFixed(2);
        const cls = t.amount >= 0 ? 'amt-pos' : 'amt-neg';
        const sign = t.amount >= 0 ? '+' : '';

        html += `<tr>
          <td>${date}</td>
          <td>${t.description}</td>
          <td>${t.category}</td>
          <td class="${cls}">${sign}${amt}</td>
        </tr>`;
      }

      html += '</tbody></table>';
      txnTableEl.innerHTML = html;

    } catch (err) {
      txnTableEl.innerHTML = '<div class="empty-history">Could not load transactions.</div>';
    }
  }

  loadProfile();
  loadTransactions();

  // ---- Clear all transactions ----
  clearBtn.addEventListener('click', async () => {
    const confirmed = window.confirm(
      'This will delete all your uploaded transactions. Your account will remain. Continue?'
    );
    if (!confirmed) return;

    clearBtn.disabled = true;
    clearStatus.textContent = 'Clearing…';
    clearStatus.style.color = '#8A7F6C';

    try {
      const result = await apiClearTransactions();
      clearStatus.textContent = `Deleted ${result.deleted} transactions.`;
      clearStatus.style.color = 'var(--sage)';

      // Refresh the table to show the empty state
      loadTransactions();
    } catch (err) {
      clearStatus.textContent = err.message;
      clearStatus.style.color = 'var(--error)';
    } finally {
      clearBtn.disabled = false;
    }
  });

  // ---- Change password ----
  changePwBtn.addEventListener('click', async () => {
    const current = currentPwEl.value;
    const next    = newPwEl.value;
    const confirm = confirmPwEl.value;

    // Client-side validation
    if (!current || !next || !confirm) {
      pwStatusEl.textContent = 'Please fill in all fields.';
      pwStatusEl.style.color = 'var(--error)';
      return;
    }

    if (next !== confirm) {
      pwStatusEl.textContent = 'New passwords do not match.';
      pwStatusEl.style.color = 'var(--error)';
      return;
    }

    if (next.length < 8) {
      pwStatusEl.textContent = 'New password must be at least 8 characters.';
      pwStatusEl.style.color = 'var(--error)';
      return;
    }

    changePwBtn.disabled = true;
    pwStatusEl.textContent = 'Updating…';
    pwStatusEl.style.color = '#8A7F6C';

    try {
      await apiChangePassword(current, next);
      pwStatusEl.textContent = 'Password updated!';
      pwStatusEl.style.color = 'var(--sage)';

      // Clear the input fields
      currentPwEl.value = '';
      newPwEl.value = '';
      confirmPwEl.value = '';
    } catch (err) {
      pwStatusEl.textContent = err.message;
      pwStatusEl.style.color = 'var(--error)';
    } finally {
      changePwBtn.disabled = false;
    }
  });

  // ---- Delete account ----
  deleteBtn.addEventListener('click', async () => {
    // First confirm — never delete without asking
    const confirmed = window.confirm(
      'Are you sure? This will permanently delete your account and ALL your data. This cannot be undone.'
    );
    if (!confirmed) return;

    deleteBtn.disabled = true;
    statusEl.textContent = 'Deleting…';
    statusEl.className = 'status';

    try {
      await apiDeleteAccount();

      // Success — clear token and go back to login
      clearToken();
      window.location.href = 'index.html';
    } catch (err) {
      statusEl.textContent = err.message;
      statusEl.className = 'status error';
      deleteBtn.disabled = false;
    }
  });

  // ---- Logout ----
  logoutBtn.addEventListener('click', () => {
    clearToken();
    window.location.href = 'index.html';
  });
})();