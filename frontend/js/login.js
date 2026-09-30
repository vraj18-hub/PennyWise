let mode = 'login'; // or 'register'

const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const submitBtn = document.getElementById('submitBtn');
const status = document.getElementById('status');
const toggleMode = document.getElementById('toggleMode');
const formTitle = document.getElementById('formTitle');
const formSubtitle = document.getElementById('formSubtitle');

// If already logged in from a previous visit, skip straight to the lobby
if (getToken()) {
  showLobbyInstantly();
}

toggleMode.addEventListener('click', () => {
  mode = mode === 'login' ? 'register' : 'login';
  updateFormMode();
});

function updateFormMode() {
  status.textContent = '';
  status.className = 'status';
  if (mode === 'login') {
    formTitle.textContent = 'PennyWise';
    formSubtitle.textContent = 'Your finance coach is waiting inside.';
    submitBtn.textContent = 'Log in';
    toggleMode.textContent = 'New here? Create an account';
  } else {
    formTitle.textContent = 'Create your account';
    formSubtitle.textContent = 'Takes less than a minute.';
    submitBtn.textContent = 'Register';
    toggleMode.textContent = 'Already have an account? Log in';
  }
}

submitBtn.addEventListener('click', async () => {
  const email = emailInput.value.trim();
  const password = passwordInput.value;

  if (!email || !password) {
    showStatus('Please fill in both fields.', 'error');
    return;
  }

  submitBtn.disabled = true;
  showStatus(mode === 'login' ? 'Checking your details…' : 'Creating your account…', '');

  try {
    if (mode === 'register') {
      await apiRegister(email, password);
      showStatus('Account created. Logging you in…', 'success');
    }

    await apiLogin(email, password);
    showStatus('Welcome!', 'success');
    enterBank();
  } catch (err) {
    showStatus(err.message, 'error');
    submitBtn.disabled = false;
  }
});

function showStatus(text, kind) {
  status.textContent = text;
  status.className = 'status' + (kind ? ' ' + kind : '');
}

function enterBank() {
  const facade = document.getElementById('facade');
  const loginCard = document.getElementById('loginCard');
  const gate = document.getElementById('gate');
  const lobby = document.getElementById('lobby');
  const flash = document.getElementById('flash');

  facade.style.transform = 'translateX(-50%) scale(6)';
  facade.style.opacity = '0';
  loginCard.style.opacity = '0';

  setTimeout(() => {
    flash.style.transition = 'opacity 0.35s ease';
    flash.style.opacity = '1';
  }, 900);

  setTimeout(() => {
    gate.style.display = 'none';
    lobby.style.opacity = '1';
    lobby.style.pointerEvents = 'auto';
    flash.style.transition = 'opacity 0.6s ease';
    flash.style.opacity = '0';
  }, 1250);
}

function showLobbyInstantly() {
  document.getElementById('gate').style.display = 'none';
  const lobby = document.getElementById('lobby');
  lobby.style.opacity = '1';
  lobby.style.pointerEvents = 'auto';
}

document.querySelectorAll('.desk').forEach(desk => {
  desk.addEventListener('click', () => {
    window.location.href = desk.dataset.page;
  });
});