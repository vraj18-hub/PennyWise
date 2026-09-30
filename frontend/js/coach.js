const chatLog = document.getElementById('chatLog');
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const logoutBtn = document.getElementById('logoutBtn');
const suggestions = document.getElementById('suggestions');
const dataBanner = document.getElementById('dataBanner');

logoutBtn.addEventListener('click', () => {
  clearToken();
  window.location.href = 'index.html';
});

suggestions.addEventListener('click', (e) => {
  if (e.target.dataset.q) {
    questionInput.value = e.target.dataset.q;
    askQuestion();
  }
});

askBtn.addEventListener('click', askQuestion);
questionInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') askQuestion();
});

// On load: tell the user whether the coach has any spending data to work with
async function checkData() {
  try {
    const summary = await apiGetSummary();
    if (!summary.by_category || summary.by_category.length === 0) {
      dataBanner.innerHTML =
        'No spending data yet. Upload a CSV at <a href="ledger.html">The Ledger Desk</a> so the coach can personalize its advice.';
    } else {
      dataBanner.classList.add('ok');
      dataBanner.textContent =
        `Using your latest summary: savings rate ${summary.savings_rate.toFixed(1)}%.`;
    }
  } catch (err) {
    dataBanner.textContent = 'Could not check your spending data.';
  }
}

async function askQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

  addBubble(question, 'user');
  questionInput.value = '';
  askBtn.disabled = true;

  const loadingBubble = addBubble('Looking at your numbers…', 'assistant loading');

  try {
    const result = await apiAskInsight(question);
    loadingBubble.remove();
    addBubble(result.answer, 'assistant');
  } catch (err) {
    loadingBubble.remove();
    addBubble(err.message, 'assistant error');
  } finally {
    askBtn.disabled = false;
  }
}

function addBubble(text, className) {
  const div = document.createElement('div');
  div.className = 'bubble ' + className;
  div.textContent = text;
  chatLog.appendChild(div);
  div.scrollIntoView({ behavior: 'smooth', block: 'end' });
  return div;
}

checkData();