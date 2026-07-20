"""
BDX Smart Homes — Project Page Sync
Run this whenever you add a new project page:
  python3 sync-projects.py
"""

import glob

PROJECTS_DIR = '/Users/guna/Downloads/bdx-smarthomes/projects'

FOOTER_AND_MODAL = '''
  <!-- CONTACT MODAL -->
  <div class="cf-modal-backdrop" id="cfModalBackdrop" aria-hidden="true">
    <div class="cf-modal-card" role="dialog" aria-modal="true" aria-label="Contact form">
      <button class="cf-modal-close" id="cfModalClose" aria-label="Close">
        <i data-lucide="x"></i>
      </button>
      <h3 class="contact-form-title">Start Your Journey with Us!</h3>
      <form class="contact-form" id="projContactForm" novalidate>
        <div class="form-field">
          <label for="pcf-name">Full Name</label>
          <input id="pcf-name" type="text" placeholder="Enter your full name" />
        </div>
        <div class="form-field">
          <label for="pcf-phone">Phone Number <span class="form-required">*</span></label>
          <div class="phone-input-wrap">
            <span class="phone-prefix">+91</span>
            <div class="phone-divider"></div>
            <input id="pcf-phone" type="tel" placeholder="98765 43210" required />
          </div>
        </div>
        <div class="form-field">
          <label for="pcf-email">Email address <span class="form-required">*</span></label>
          <input id="pcf-email" type="email" placeholder="Enter your email address" required />
        </div>
        <div class="form-field">
          <label for="pcf-service">Services</label>
          <div class="select-wrap">
            <select id="pcf-service">
              <option value="">Consultation</option>
              <option>Architecture Design</option>
              <option>Residential Construction</option>
              <option>Home Interiors</option>
              <option>Project Management</option>
            </select>
            <i data-lucide="chevron-down" class="select-chevron"></i>
          </div>
        </div>
        <button type="submit" class="btn-primary form-submit">Free consultation <span class="arrow">→</span></button>
        <p class="form-privacy">We respect your privacy. Your information is 100% secure and never shared.</p>
      </form>
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <a href="../index.html" class="footer-logo-link">
          <img src="../images/footer-logo.webp" alt="BDX Smart Homes" class="footer-logo" />
        </a>
        <p class="footer-tagline">Building dream homes in Chennai since 2014. We combine architectural excellence with transparent construction to deliver homes that stand the test of time.</p>
        <div class="footer-socials">
          <a href="#" class="footer-social" aria-label="Instagram"><img src="../images/social-instagram.svg" alt="Instagram" /></a>
          <a href="#" class="footer-social" aria-label="Facebook"><img src="../images/social-facebook.svg" alt="Facebook" /></a>
          <a href="#" class="footer-social" aria-label="YouTube"><img src="../images/social-youtube.svg" alt="YouTube" /></a>
          <a href="#" class="footer-social" aria-label="Twitter / X"><img src="../images/social-twitter.svg" alt="Twitter" /></a>
        </div>
      </div>
      <div class="footer-col">
        <h4 class="footer-col-heading">Services</h4>
        <ul class="footer-links">
          <li><a href="../index.html#services">Architecture Design</a></li>
          <li><a href="../index.html#services">Residential Construction</a></li>
          <li><a href="../index.html#services">Home Interiors</a></li>
          <li><a href="../index.html#services">Project Management</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 class="footer-col-heading">Company</h4>
        <ul class="footer-links">
          <li><a href="../index.html#home">About Us</a></li>
          <li><a href="../index.html#portfolio">Our Projects</a></li>
          <li><a href="../index.html#process">Our Process</a></li>
          <li><a href="../index.html#testimonials">Testimonials</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 class="footer-col-heading">Legal</h4>
        <ul class="footer-links">
          <li><a href="#">Privacy Policy</a></li>
          <li><a href="#">Terms of Service</a></li>
          <li><a href="#">Disclaimer</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 BDX Smart Homes. All rights reserved.</p>
      <p>Designed &amp; Developed by <a href="#" class="footer-credit">✦ DigiBoomi</a></p>
    </div>
  </footer>

  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    lucide.createIcons();
    const nav = document.getElementById('nav');
    window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 10));
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('nav-mobile');
    hamburger.addEventListener('click', () => mobileMenu.classList.toggle('open'));
    mobileMenu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => mobileMenu.classList.remove('open')));
    (function () {
      const backdrop = document.getElementById('cfModalBackdrop');
      const closeBtn = document.getElementById('cfModalClose');
      const ctaBtn   = document.getElementById('projCtaBtn');
      if (!backdrop || !ctaBtn) return;
      function openModal() { backdrop.classList.add('open'); backdrop.removeAttribute('aria-hidden'); document.body.style.overflow = 'hidden'; closeBtn.focus(); }
      function closeModal() { backdrop.classList.remove('open'); backdrop.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; ctaBtn.focus(); }
      ctaBtn.addEventListener('click', openModal);
      closeBtn.addEventListener('click', closeModal);
      backdrop.addEventListener('click', e => { if (e.target === backdrop) closeModal(); });
      document.addEventListener('keydown', e => { if (e.key === 'Escape' && backdrop.classList.contains('open')) closeModal(); });
    })();
    (function () {
      const form = document.getElementById('projContactForm');
      if (!form) return;
      function showError(field, msg) {
        field.classList.add('input-error');
        const err = document.createElement('span');
        err.className = 'form-error';
        err.textContent = msg;
        field.closest('.form-field').appendChild(err);
      }
      form.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', () => {
          input.classList.remove('input-error');
          const err = input.closest('.form-field')?.querySelector('.form-error');
          if (err) err.remove();
        });
      });
      form.addEventListener('submit', e => {
        e.preventDefault();
        form.querySelectorAll('.form-error').forEach(el => el.remove());
        form.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));
        let valid = true;
        const phone = form.querySelector('[type="tel"]');
        const email = form.querySelector('[type="email"]');
        const digits = phone.value.replace(/\D/g, '');
        if (!digits) { showError(phone, 'Phone number is required.'); valid = false; }
        else if (digits.length !== 10) { showError(phone, 'Enter a valid 10-digit phone number.'); valid = false; }
        const emailVal = email.value.trim();
        if (!emailVal) { showError(email, 'Email address is required.'); valid = false; }
        else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailVal)) { showError(email, 'Enter a valid email address.'); valid = false; }
        if (!valid) return;
        form.innerHTML = `<div class="form-success"><i data-lucide="circle-check-big" class="form-success-icon"></i><h4>Thank you!</h4><p>We've received your details and will reach out within 24 hours.</p></div>`;
        lucide.createIcons();
      });
    })();
  </script>
</body>
</html>'''

NAV_DESKTOP = '''        <ul class="nav-links">
          <li><a href="../index.html#home">Home</a></li>
          <li><a href="../index.html#services">Services</a></li>
          <li><a href="../index.html#portfolio" class="active">Projects</a></li>
          <li><a href="../index.html#promise">7G Services</a></li>
          <li><a href="../index.html#faq">FAQ</a></li>
          <li><a href="../index.html#contact">Contact</a></li>
        </ul>'''

NAV_MOBILE = '''    <div class="nav-mobile" id="nav-mobile">
      <a href="../index.html#home">Home</a>
      <a href="../index.html#services">Services</a>
      <a href="../index.html#portfolio">Projects</a>
      <a href="../index.html#promise">7G Services</a>
      <a href="../index.html#faq">FAQ</a>
      <a href="../index.html#contact">Contact</a>
      <a href="tel:+919150007269">📞 +91 91500 07269</a>
      <a href="../index.html#contact" class="btn-primary">Free consultation →</a>
    </div>'''

CTA_BUTTON = '''      <button class="btn-primary proj-cta-btn" id="projCtaBtn">
        Let\'s Build Yours <span class="arrow">→</span>
      </button>'''


def sync(fpath):
    import re
    with open(fpath) as f:
        content = f.read()

    original = content

    # 1. Sync desktop nav links (include leading whitespace in match to avoid drift)
    content = re.sub(
        r'[ \t]*<ul class="nav-links">.*?</ul>',
        NAV_DESKTOP,
        content,
        flags=re.DOTALL
    )

    # 2. Sync mobile nav (include leading whitespace in match to avoid drift)
    content = re.sub(
        r'[ \t]*<div class="nav-mobile" id="nav-mobile">.*?</div>(?=\s*\n\s*</header>)',
        NAV_MOBILE,
        content,
        flags=re.DOTALL
    )

    # 3. Ensure CTA is a button (not anchor)
    content = re.sub(
        r'<a href="[^"]*" class="btn-primary proj-cta-btn">.*?</a>',
        CTA_BUTTON,
        content,
        flags=re.DOTALL
    )

    # 4. Replace everything after </section> (the last one) with modal+footer+script
    idx = content.rfind('</section>')
    if idx != -1:
        content = content[:idx + len('</section>')] + '\n' + FOOTER_AND_MODAL.lstrip('\n')

    if content != original:
        with open(fpath, 'w') as f:
            f.write(content)
        print(f'  updated : {fpath}')
    else:
        print(f'  no change: {fpath}')


files = sorted(glob.glob(f'{PROJECTS_DIR}/*.html'))
print(f'Syncing {len(files)} project pages...')
for fpath in files:
    sync(fpath)
print('Done.')
