/* =============================================
   BDX SMART HOMES — main.js
   ============================================= */

// Initialise Lucide icons
lucide.createIcons();

// Sticky nav shadow on scroll
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 10);
});

// Hamburger menu toggle
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('nav-mobile');

hamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');
});

// Close mobile menu when any link clicked
mobileMenu.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => mobileMenu.classList.remove('open'));
});

// Nav scroll-spy
(function () {
  const navLinks = document.querySelectorAll('.nav-links a');
  const sections = Array.from(navLinks)
    .map(a => document.querySelector(a.getAttribute('href')))
    .filter(Boolean);

  function setActive(id) {
    navLinks.forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === '#' + id);
    });
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) setActive(entry.target.id);
    });
  }, {
    rootMargin: `-${nav.offsetHeight}px 0px -60% 0px`,
    threshold: 0
  });

  sections.forEach(sec => observer.observe(sec));
  setActive(sections[0].id);
})();

// Stat count-up animation
function countUp(el, target, suffix, duration) {
  const start = performance.now();
  function tick(now) {
    const t = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(eased * target) + suffix;
    if (t < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

if ('IntersectionObserver' in window) {
  const statsCard = document.querySelector('.stats-card');
  const observer = new IntersectionObserver((entries, obs) => {
    if (entries[0].isIntersecting) {
      document.querySelectorAll('.stat-number').forEach(el => {
        countUp(el, +el.dataset.count, el.dataset.suffix, 2000);
      });
      obs.unobserve(statsCard);
    }
  }, { threshold: 0.3 });
  observer.observe(statsCard);
}

// 7G cards — staggered appear on scroll
if ('IntersectionObserver' in window) {
  const gCards = document.querySelectorAll('.g-card');
  const gObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const card = entry.target;
        const i = +card.dataset.gIndex;
        setTimeout(() => card.classList.add('g-visible'), i * 100);
        obs.unobserve(card);
      }
    });
  }, { threshold: 0.15 });

  gCards.forEach((card, i) => {
    card.dataset.gIndex = i;
    gObserver.observe(card);
  });
}

// Testimonial slider
(function () {
  const track   = document.getElementById('testiTrack');
  const dots    = document.querySelectorAll('.testi-dot');
  const prevBtn = document.getElementById('testiPrev');
  const nextBtn = document.getElementById('testiNext');
  if (!track) return;

  const cards = Array.from(track.children);
  const total = cards.length;
  let current = 0;

  function setWidths() {
    const w = track.parentElement.offsetWidth;
    track.style.width = (w * total) + 'px';
    cards.forEach(c => c.style.width = w + 'px');
  }

  function goTo(index) {
    current = (index + total) % total;
    const w = track.parentElement.offsetWidth;
    track.style.transform = `translateX(-${current * w}px)`;
    dots.forEach((d, i) => d.classList.toggle('active', i === current));
  }

  setWidths();
  window.addEventListener('resize', () => { setWidths(); goTo(current); });

  prevBtn.addEventListener('click', () => goTo(current - 1));
  nextBtn.addEventListener('click', () => goTo(current + 1));
  dots.forEach(d => d.addEventListener('click', () => goTo(+d.dataset.index)));

  // Auto-advance every 6s

  let timer = setInterval(() => goTo(current + 1), 6000);
  [prevBtn, nextBtn, ...dots].forEach(el =>
    el.addEventListener('click', () => { clearInterval(timer); timer = setInterval(() => goTo(current + 1), 6000); })
  );
})();

// Contact modal
(function () {
  const backdrop = document.getElementById('cfModalBackdrop');
  const closeBtn = document.getElementById('cfModalClose');
  const heroBtn = document.getElementById('heroCtaBtn');
  if (!backdrop) return;

  function openModal() {
    document.body.style.overflow = 'hidden';
    backdrop.classList.add('open');
    backdrop.removeAttribute('aria-hidden');
    closeBtn.focus({ preventScroll: true });
  }

  function closeModal() {
    backdrop.classList.remove('open');
    backdrop.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (heroBtn) heroBtn.focus({ preventScroll: true });
  }

  if (heroBtn) heroBtn.addEventListener('click', openModal);
  closeBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', e => { if (e.target === backdrop) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && backdrop.classList.contains('open')) closeModal(); });
})();

// Form validation
function validateForm(form) {
  let valid = true;

  // Clear previous errors
  form.querySelectorAll('.form-error').forEach(el => el.remove());
  form.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));

  function showError(field, msg) {
    field.classList.add('input-error');
    const err = document.createElement('span');
    err.className = 'form-error';
    err.textContent = msg;
    field.closest('.form-field').appendChild(err);
    valid = false;
  }

  const phone = form.querySelector('[type="tel"]');
  const email = form.querySelector('[type="email"]');

  if (phone) {
    const digits = phone.value.replace(/\D/g, '');
    if (!digits) showError(phone, 'Phone number is required.');
    else if (digits.length !== 10) showError(phone, 'Enter a valid 10-digit phone number.');
  }

  if (email) {
    const emailVal = email.value.trim();
    if (!emailVal) showError(email, 'Email address is required.');
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailVal)) showError(email, 'Enter a valid email address.');
  }

  return valid;
}

function handleFormSubmit(form, onSuccess) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!validateForm(form)) return;
    onSuccess();
  });

  // Clear error on input
  form.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', () => {
      input.classList.remove('input-error');
      const err = input.closest('.form-field')?.querySelector('.form-error');
      if (err) err.remove();
    });
  });
}

function showSuccess(form) {
  form.innerHTML = `
    <div class="form-success">
      <i data-lucide="circle-check-big" class="form-success-icon"></i>
      <h4>Thank you!</h4>
      <p>We've received your details and will reach out within 24 hours.</p>
    </div>`;
  lucide.createIcons();
}

handleFormSubmit(document.getElementById('heroContactForm'), () => {
  window.bdxSubmitFormLead(document.getElementById('heroContactForm'));
  showSuccess(document.getElementById('heroContactForm'));
});
handleFormSubmit(document.getElementById('contactForm'), () => {
  window.bdxSubmitFormLead(document.getElementById('contactForm'));
  showSuccess(document.getElementById('contactForm'));
});

// FAQ accordion
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(el => {
      el.classList.remove('open');
      el.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
    });
    if (!isOpen) {
      item.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
    }
  });
});
