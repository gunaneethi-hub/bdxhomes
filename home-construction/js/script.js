(function(){
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.getElementById('year').textContent = new Date().getFullYear();

  /* Hero headline entrance */
  requestAnimationFrame(() => document.body.classList.add('loaded'));

  /* Header shadow + scroll progress + active nav link */
  const header = document.querySelector('.header');
  const bar = document.querySelector('.progress');
  const links = [...document.querySelectorAll('.nav a[href^="#"]:not(.nav-mobile-cta)')];
  const sections = links.map(a => document.querySelector(a.getAttribute('href')));
  let ticking = false;
  function onScroll(){
    const y = window.scrollY;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    header.classList.toggle('scrolled', y > 10);
    let current = -1;
    sections.forEach((s, i) => { if (s && s.getBoundingClientRect().top < window.innerHeight * 0.4) current = i; });
    links.forEach((a, i) => a.classList.toggle('active', i === current));
    ticking = false;
  }
  window.addEventListener('scroll', () => { if (!ticking){ requestAnimationFrame(onScroll); ticking = true; } }, {passive:true});
  onScroll();

  /* Mobile menu */
  const menuBtn = document.querySelector('.menu-btn');
  function setMenu(open){
    document.body.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', open);
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  menuBtn.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
  document.querySelectorAll('.nav a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

  /* Scroll reveal */
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, {threshold:0.15, rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.rv, .service, .why-item').forEach(el => io.observe(el));

  /* Stat counters */
  const counters = document.querySelectorAll('[data-count]');
  const cio = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      const el = en.target, end = +el.dataset.count;
      cio.unobserve(el);
      if (reduce){ el.textContent = end; return; }
      const dur = 1600, t0 = performance.now();
      (function step(t){
        const p = Math.min((t - t0) / dur, 1);
        el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(step);
      })(t0);
    });
  }, {threshold:0.6});
  counters.forEach(c => cio.observe(c));

  /* Plan ↔ Built comparison slider */
  const cmp = document.getElementById('compare');
  const knob = document.getElementById('knob');
  let pos = 100, dragging = false;
  function setPos(v){
    pos = Math.max(0, Math.min(100, v));
    cmp.style.setProperty('--pos', pos + '%');
    knob.setAttribute('aria-valuenow', Math.round(pos));
  }
  function fromEvent(e){
    const r = cmp.getBoundingClientRect();
    const x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
    setPos(x / r.width * 100);
  }
  cmp.addEventListener('pointerdown', e => { dragging = true; cmp.setPointerCapture(e.pointerId); fromEvent(e); });
  cmp.addEventListener('pointermove', e => { if (dragging) fromEvent(e); });
  cmp.addEventListener('pointerup', () => dragging = false);
  cmp.addEventListener('pointercancel', () => dragging = false);
  knob.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft'){ setPos(pos - 5); e.preventDefault(); }
    if (e.key === 'ArrowRight'){ setPos(pos + 5); e.preventDefault(); }
  });
  /* Opening sweep: plan reveals into the finished home, settles at the middle */
  if (reduce){ setPos(50); }
  else {
    setTimeout(() => {
      const t0 = performance.now(), dur = 2200;
      (function sweep(t){
        if (dragging) return;
        const p = Math.min((t - t0) / dur, 1);
        const ease = x => x < .5 ? 4*x*x*x : 1 - Math.pow(-2*x + 2, 3) / 2;
        // 100% plan → 12% (almost all built) → settle at 50%
        setPos(p < .6 ? 100 - 88 * ease(p / .6) : 12 + 38 * ease((p - .6) / .4));
        if (p < 1) requestAnimationFrame(sweep);
      })(t0);
    }, 700);
  }

  /* FAQ accordion (one open at a time) */
  document.querySelectorAll('.faq-q').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.parentElement;
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(i => {
        i.classList.remove('open'); i.querySelector('.faq-q').setAttribute('aria-expanded','false');
      });
      if (!isOpen){ item.classList.add('open'); btn.setAttribute('aria-expanded','true'); }
    });
  });

  /* Lead form validation */
  const form = document.getElementById('leadForm');
  const phone = form.phone;
  phone.addEventListener('input', () => { phone.value = phone.value.replace(/\D/g,'').slice(0,10); });
  form.addEventListener('submit', e => {
    e.preventDefault();
    const okPhone = /^[6-9]\d{9}$/.test(phone.value);
    const okEmail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.email.value.trim());
    phone.closest('.field').classList.toggle('error', !okPhone);
    form.email.closest('.field').classList.toggle('error', !okEmail);
    if (!okPhone){ phone.focus(); return; }
    if (!okEmail){ form.email.focus(); return; }

    const data = {
      name: form.name.value.trim(),
      phone: '+91' + phone.value,
      email: form.email.value.trim(),
      service: form.service.value
    };
    if (window.bdxSubmitFormLead) {
      window.bdxSubmitFormLead(form);
    } else {
      console.error('Lead form intake is unavailable; the lead was not submitted.');
      return;
    }
    form.classList.add('sent');
  });
})();
