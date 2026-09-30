const csvFile = document.getElementById('csvFile');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');
const summaryArea = document.getElementById('summaryArea');
const logoutBtn = document.getElementById('logoutBtn');

logoutBtn.addEventListener('click', () => {
  clearToken();
  window.location.href = 'index.html';
});

uploadBtn.addEventListener('click', async () => {
  const file = csvFile.files[0];
  if (!file) {
    showUploadStatus('Please choose a CSV file first.', 'error');
    return;
  }

  uploadBtn.disabled = true;
  showUploadStatus('Uploading…', '');

  try {
    const result = await apiUploadCSV(file);
    showUploadStatus(
      `Done — ${result.inserted} transactions added${result.skipped ? `, ${result.skipped} skipped` : ''}.`,
      'success'
    );
    await loadSummary();
  } catch (err) {
    showUploadStatus(err.message, 'error');
  } finally {
    uploadBtn.disabled = false;
  }
});

function showUploadStatus(text, kind) {
  uploadStatus.textContent = text;
  uploadStatus.className = 'upload-status' + (kind ? ' ' + kind : '');
}

async function loadSummary() {
  try {
    const summary = await apiGetSummary();
    renderSummary(summary);
  } catch (err) {
    summaryArea.innerHTML = `<div class="empty-state">${err.message}</div>`;
  }
}

function renderSummary(summary) {
  if (!summary.by_category || summary.by_category.length === 0) {
    summaryArea.innerHTML = `<div class="empty-state">No transactions yet — upload a CSV above to see your summary.</div>`;
    return;
  }

  const maxCategory = Math.max(...summary.by_category.map(c => c.total));

  const barsHtml = summary.by_category
    .sort((a, b) => b.total - a.total)
    .map(c => `
      <div class="bar-row">
        <div class="bar-label">
          <span>${escapeHtml(capitalize(c.category))}</span>
          <span>₹${c.total.toFixed(2)}</span>
        </div>
        <div class="bar-track">
          <div class="bar-fill" style="width: ${(c.total / maxCategory) * 100}%"></div>
        </div>
      </div>
    `)
    .join('');

  summaryArea.innerHTML = `
    <div class="stats">
      <div class="stat">
        <div class="k">Total income</div>
        <div class="v">₹${summary.total_income.toFixed(2)}</div>
      </div>
      <div class="stat">
        <div class="k">Total expenses</div>
        <div class="v">₹${summary.total_expenses.toFixed(2)}</div>
      </div>
      <div class="stat">
        <div class="k">Savings rate</div>
        <div class="v pos">${summary.savings_rate.toFixed(1)}%</div>
      </div>
    </div>
    <div class="breakdown">
      <h2>Spending by category</h2>
      ${barsHtml}
    </div>
  `;
}

function capitalize(text) {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

// Load whatever summary already exists as soon as the page opens
loadSummary();

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}