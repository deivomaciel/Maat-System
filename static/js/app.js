/* Maat — app.js */

// ── Toast ────────────────────────────────────────────────────────────────────
function showToast(msg, type = '') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => {
    el.style.animation = 'toastOut .3s ease forwards';
    setTimeout(() => el.remove(), 300);
  }, 3000);
}

// ── Copy to clipboard ─────────────────────────────────────────────────────────
async function copyLink(text, btn) {
  try {
    await navigator.clipboard.writeText(text);
    const orig = btn.innerHTML;
    btn.innerHTML = '✓ Copiado!';
    showToast('Link copiado com sucesso!', 'success');
    setTimeout(() => { btn.innerHTML = orig; }, 2000);
  } catch {
    showToast('Não foi possível copiar.', 'error');
  }
}

// ── Modal ─────────────────────────────────────────────────────────────────────
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('open');
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('open');
}

// ── DOMContentLoaded ──────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

  // Close modal on backdrop click
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', e => {
      if (e.target === overlay) overlay.classList.remove('open');
    });
  });

  // Close modal on Escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open'));
    }
  });

  // Navbar shadow on scroll
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    const update = () => {
      navbar.style.boxShadow = window.scrollY > 10 ? '0 2px 24px rgba(0,0,0,.12)' : 'none';
    };
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  // Animate rating bars
  document.querySelectorAll('[data-width]').forEach(bar => {
    const target = bar.getAttribute('data-width');
    bar.style.width = '0%';
    requestAnimationFrame(() => {
      setTimeout(() => { bar.style.width = target + '%'; }, 80);
    });
  });

  // Flash messages from query params
  const params = new URLSearchParams(window.location.search);
  if (params.get('success')) showToast(decodeURIComponent(params.get('success')), 'success');
  if (params.get('error'))   showToast(decodeURIComponent(params.get('error')), 'error');

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });
});
