const chatLog = document.getElementById('chatLog');
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const logoutBtn = document.getElementById('logoutBtn');
const suggestions = document.getElementById('suggestions');

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

async function askQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

  addBubble(question, 'user');
  questionInput.value = '';
  askBtn.disabled = true;

  const loadingBubble = addBubble('Thinking…', 'assistant loading');

  try {
    const result = await apiAskRag(question);
    loadingBubble.remove();

    const sourcesText = result.chunks && result.chunks.length
      ? 'Sources: ' + [...new Set(result.chunks.map(c => c.source))].join(', ')
      : '';

    addBubble(result.answer, 'assistant', sourcesText);
  } catch (err) {
    loadingBubble.remove();
    addBubble(err.message, 'assistant error');
  } finally {
    askBtn.disabled = false;
  }
}

function addBubble(text, className, sourcesText) {
  const div = document.createElement('div');
  div.className = 'bubble ' + className;
  div.textContent = text;

  if (sourcesText) {
    const src = document.createElement('div');
    src.className = 'sources';
    src.textContent = sourcesText;
    div.appendChild(src);
  }

  chatLog.appendChild(div);
  div.scrollIntoView({ behavior: 'smooth', block: 'end' });
  return div;
}