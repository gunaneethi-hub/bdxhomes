"""
BDX Smart Homes — Bulk Project Page Generator
Generates projects/<slug>.html for each entry in PROJECTS and appends
matching cards to all-projects.html. Run from the repo root:
  python3 generate_projects.py
"""

import os
import re

REPO = os.path.dirname(os.path.abspath(__file__))
PLACEHOLDER_IMG = "../images/placeholder-project.svg"
PLACEHOLDER_IMG_ROOT = "images/placeholder-project.svg"

PROJECTS = [
    {"slug": "sk-res", "name": "SK Residence", "config": "5 BHK", "area": "2490.8", "floors": "G+2",
     "location": "Kayarambedu", "year": "March 2025", "duration": "10 Months", "structure": "RCC Frame",
     "review": "I want to sincerely thank the BDX team for the incredible work on my home. They executed the construction precisely as per the drawings, using high-quality materials and excellent workmanship. Every element was brought to reality with care and precision. I'm extremely happy with how beautifully everything came together and the integration of advanced technology has made the home even more functional, modern, and future-ready.",
     "overview": "SK Residence is a contemporary 5 BHK G+2 residence in Kayarambedu, designed to balance bold architectural character with comfortable modern living. Its distinctive façade combines exposed red brick, textured grey frames, clean white geometric volumes, and terracotta jaali screens, creating a warm and timeless identity. Spacious balconies, open terraces, greenery, and deep projections improve shade, privacy, natural light, and ventilation."},

    {"slug": "bdx-nila", "name": "BDX Nila", "config": "3 BHK", "area": "1759", "floors": "G+1",
     "location": "Guduvanchery", "year": "February 2025", "duration": "11 Months", "structure": "RCC Frame",
     "review": "We are genuinely excited and deeply thankful to BDX Smart Homes for bringing our dream home. This contemporary eclectic-style villa has been planned with meticulous attention to detail, ensuring excellent natural lighting and cross-ventilation throughout. The exterior façade has also been thoughtfully crafted, featuring a textured feature wall paired with a carefully designed lighting scheme that enhances the villa's presence in the evenings. Every element of the architectural planning reflects a perfect balance of function, beauty, and personal comfort.",
     "overview": "BDX Nila is a thoughtfully designed 3 BHK G+1 residence that blends contemporary eclectic style with practical family living. The home is planned with close attention to natural lighting and cross-ventilation, creating bright, airy, and comfortable interiors throughout the day. Its distinctive façade features a textured statement wall complemented by a carefully planned lighting scheme that enhances the villa's character after sunset."},

    {"slug": "av-res", "name": "AV Residence", "config": "5 BHK", "area": "4061.5", "floors": "G+2",
     "location": "Guduvanchery", "year": "March 2026", "duration": "11 Months", "structure": "RCC Frame",
     "review": "We're really happy with the construction by BDX Smart Homes. The team clearly understood our requirements and executed everything with care and clarity. The project tracking system and VR walkthrough gave us great confidence from the start. The Open Terrace Pergola with glass came out well and the sit-out area with the Buddha statue looks positive good feel effect. The house has good light, ventilation & the overall finishing matches exactly what was discussed at the beginning. Truly satisfied with their work and professionalism. Thankful to the entire BDX team for delivering exactly what was discussed.",
     "overview": "AV Residence is a distinctive G+2 residence in Guduvanchery, thoughtfully designed on a triangle-shaped plot to maximise space, comfort, and functionality. The home features bright, airy interiors with excellent natural light and cross-ventilation. A stylish open terrace with glass detailing enhances its contemporary character, while the sit-out area with a Buddha statue creates a peaceful and welcoming ambience."},

    {"slug": "nila-2-0", "name": "Nila 2.0", "config": "4 BHK", "area": "2481", "floors": "G+2",
     "location": "Thangappapuram", "year": "April 2026", "duration": "12 Months", "structure": "RCC Frame",
     "review": None,
     "overview": "Nila 2.0 is a thoughtfully designed 4 BHK G+2 residence in Thangappapuram, created to combine distinctive architecture with personalised family living. The home features a unique façade highlighted by a striking circular design element, giving it a memorable identity. Inside, the circular bedroom window, moon-themed bedroom, customised kids' room, built-in wardrobes, study corner, and smart storage solutions reflect the family's preferences."},

    {"slug": "ak-res", "name": "AK Residence", "config": "4 BHK", "area": "3392", "floors": "G+1",
     "location": "Kannivakkam", "year": "April 2026", "duration": "11 Months", "structure": "RCC Frame",
     "review": None, "overview": None},

    {"slug": "ds-res", "name": "DS Residence", "config": "3 BHK", "area": "1764.8", "floors": "G+1",
     "location": "Kannivakkam", "year": "May 2026", "duration": "12 Months", "structure": "RCC Frame",
     "review": None, "overview": None},

    {"slug": "vn-res", "name": "VN Residence", "config": "6 BHK", "area": "3293", "floors": "G+2",
     "location": "Guduvanchery", "year": "July 2025", "duration": "18 Months", "structure": "RCC Frame",
     "review": "Our experience with BDX Smart Homes has been absolutely amazing! We looked around and explored a lot of options, but BDX really stood out—and now we're so glad we chose them. From day one, they understood exactly what we had in mind and transformed it into a home that's even better than we imagined. The thoughtful layout—with a rental-ready ground floor and private upper floors fits our needs perfectly. The craftsmanship and quality materials stand out in every room, and the stylish exterior with brick cladding and grooved detailing gives the house a bold, elegant look.",
     "overview": "VN Residence is a spacious 6 BHK G+2 residence in Guduvanchery, thoughtfully planned for comfortable family living and long-term flexibility. The ground floor includes a rental-ready layout, while the upper floors offer greater privacy for the family. Bright interiors, efficient room planning, quality finishes, and good natural ventilation create a comfortable living environment. The façade combines warm brick cladding, refined grooved details, and clean geometric forms."},

    {"slug": "ra-res", "name": "RA Residence", "config": "3 BHK", "area": "2022", "floors": "G+1",
     "location": "Urapakkam", "year": "July 2025", "duration": "11 Months", "structure": None,
     "review": "Our experience with BDX Smart Homes has been absolutely amazing! We looked around and explored a lot of options, but BDX really stood out—and now we're so glad we chose them. From day one, they understood exactly what we had in mind and transformed it into a home that's even better than we imagined. The thoughtful layout—with a rental-ready ground floor and private upper floors fits our needs perfectly. The craftsmanship and quality materials stand out in every room, and the stylish exterior with brick cladding and grooved detailing gives the house a bold, elegant look.",
     "overview": "RA Residence is a serene 3 BHK G+1 residence in Urapakkam, thoughtfully designed around a calming sea-inspired theme. The home features an open mezzanine study, a sunken living area, and a bright internal courtyard that brings natural light and ventilation deep into the interiors. Its signature blue-and-white jaali façade creates a distinctive coastal identity, especially when illuminated at night."},

    {"slug": "nt-res", "name": "NT Residence", "config": "3 BHK", "area": "2415", "floors": "G+1",
     "location": "Villupuram", "year": "December 2025", "duration": "18 Months", "structure": None,
     "review": None, "overview": None},

    {"slug": "sa-res", "name": "Sanjay Residence", "config": "3 BHK", "area": "8000", "floors": "G+1",
     "location": "Guduvanchery", "year": "2023", "duration": None, "structure": None,
     "review": None,
     "overview": "Sanjay Residence is a contemporary 3 BHK G+1 residence in Guduvanchery, thoughtfully designed for refined family living. The home features a bold grey-and-white façade, glass balcony detailing, warm wooden gates, and clean geometric forms. Inside, customised wardrobes, a spacious modular kitchen, elegant bedrooms, and smart storage solutions create a practical and sophisticated environment. A private swimming pool, landscaped sit-out, floating staircase, and open double-height spaces add a sense of luxury."},

    {"slug": "karthick-res", "name": "Karthick Residence", "config": "3 BHK", "area": "3200", "floors": "G+2",
     "location": "Guduvanchery", "year": "2022", "duration": None, "structure": None,
     "review": None,
     "overview": "Karthick Residence is a contemporary 3 BHK G+2 residence in Guduvanchery, thoughtfully designed with clean lines, functional spaces, and refined modern detailing. The façade features a bold geometric jaali panel, textured finishes, and warm exterior lighting that gives the home a distinctive identity at night. Inside, the modular kitchen, sleek glass partitions, elegant ceiling lighting, and customised TV unit create a bright and sophisticated atmosphere."},

    {"slug": "lm-res", "name": "LM Residence", "config": "3 BHK", "area": "2200", "floors": "G+1",
     "location": "Guduvanchery", "year": "2023", "duration": None, "structure": None,
     "review": None, "overview": None},

    {"slug": "gk-res", "name": "GK Residence", "config": "3 BHK", "area": "2500", "floors": "G+1",
     "location": "Guduvanchery", "year": "2023", "duration": None, "structure": None,
     "review": None,
     "overview": "GK Residence is a contemporary 3 BHK G+1 residence in Guduvanchery, thoughtfully designed for bright, comfortable, and functional family living. The home features spacious interiors with abundant natural light, glossy marble-finish flooring, and clean modern detailing. A sleek modular kitchen with dark cabinetry, white countertops, integrated appliances, and warm task lighting creates a refined cooking space."},

    {"slug": "am-res", "name": "AM Residence", "config": "3 BHK", "area": "2600", "floors": "G+1",
     "location": "Thirupathoor", "year": "2023", "duration": None, "structure": None,
     "review": None, "overview": None},

    {"slug": "pr-res", "name": "PR Residence", "config": "5 BHK", "area": "4850", "floors": "G+2",
     "location": "Maraimalainagar", "year": "2024", "duration": None, "structure": None,
     "review": None, "overview": None},

    {"slug": "rr-res", "name": "RR Residence", "config": "5 BHK", "area": "4850", "floors": "G+2",
     "location": "Maraimalainagar", "year": "2024", "duration": None, "structure": None,
     "review": None, "overview": None},

    {"slug": "gj-res", "name": "GJ Residence", "config": "5 BHK", "area": "5120", "floors": "G+2",
     "location": "Maraimalainagar", "year": "2024", "duration": None, "structure": None,
     "review": None, "overview": None},
]

# Pool used for "You May Also Like" — includes RD Residence (has a real photo already).
RELATED_POOL = [{"slug": "rd-residence", "name": "RD Residence", "location": "Madhavaram",
                  "img": "../images/portfolio-rd.webp"}] + \
               [{"slug": p["slug"], "name": p["name"], "location": p["location"],
                 "img": PLACEHOLDER_IMG} for p in PROJECTS]


def initials(name):
    words = re.findall(r"[A-Za-z0-9]+", name)
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return name[:2].upper()


def features_list(p):
    feats = [f"{p['config']} Residential Home", f"{p['floors']} Floors"]
    if p["structure"]:
        feats.append(f"{p['structure']} Structure")
    if p["duration"]:
        feats.append(f"Completed in {p['duration']}")
    return feats


def spec_rows(p):
    rows = [
        ("Build Type", p["name"]),
        ("Configuration", p["config"]),
        ("Built-Up Area", f"{p['area']} sq.ft"),
        ("Floors", p["floors"]),
        ("Location", f"{p['location']}, Chennai"),
        ("Year Completed", p["year"]),
    ]
    if p["duration"]:
        rows.append(("Duration", p["duration"]))
    if p["structure"]:
        rows.append(("Structure", p["structure"]))
    return rows


def overview_paragraphs(p):
    if p["overview"]:
        return [p["overview"]]
    return [f"{p['name']} is a {p['config']} {p['floors']} residence in {p['location']}, "
            f"Chennai, built by BDX Smart Homes across {p['area']} sq.ft."]


def testimonial_section(p):
    if not p["review"]:
        return ""
    return f"""
  <!-- ── TESTIMONIAL ── -->
  <section class="proj-testimonial">
    <div class="proj-testimonial-inner">
      <div>
        <span class="section-eyebrow">Client Story</span>
        <h2 class="section-heading proj-section-heading">What the Client Said</h2>
      </div>
      <div class="proj-testi-card">
        <div class="testi-photo"><img src="{PLACEHOLDER_IMG}" alt="{p['name']}" /></div>
        <div class="testi-content">
          <div class="testi-top">
            <div class="testi-stars">
              <i data-lucide="star" class="star-icon"></i><i data-lucide="star" class="star-icon"></i>
              <i data-lucide="star" class="star-icon"></i><i data-lucide="star" class="star-icon"></i>
              <i data-lucide="star" class="star-icon"></i>
            </div>
            <blockquote class="testi-quote">"{p['review']}"</blockquote>
          </div>
          <div class="testi-author">
            <div class="testi-avatar-placeholder">{initials(p['name'])}</div>
            <div class="testi-author-info">
              <strong>Verified Client</strong>
              <span>Google Review · {p['location']}, Chennai</span>
              <span class="testi-project">{p['config']} Home · {p['area']} sq.ft</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""


def related_section(p):
    others = [r for r in RELATED_POOL if r["slug"] != p["slug"]][:3]
    cards = []
    for r in others:
        href = "rd-residence.html" if r["slug"] == "rd-residence" else f"{r['slug']}.html"
        cards.append(f"""        <div class="proj-card">
          <img src="{r['img']}" alt="{r['name']}" class="proj-img" />
          <div class="proj-overlay"><div class="proj-info"><h3 class="proj-name">{r['name']}</h3><p class="proj-location"><i data-lucide="map-pin" aria-hidden="true"></i> {r['location']}</p></div></div>
          <a href="{href}" class="proj-hover-btn">View This Project <i data-lucide="arrow-right" class="btn-arrow"></i></a>
          <span class="proj-chip proj-chip--done">Completed</span>
        </div>""")
    return "\n".join(cards)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <link rel="icon" type="image/x-icon" href="../favicon.ico" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name} — Completed {config} Home in {location} | BDX Smart Homes</title>
  <meta name="description" content="{name} — a {area} sq.ft {config} home in {location}, Chennai by BDX Smart Homes." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../style.css" />
</head>
<body class="proj-page">

  <!-- NAV -->
  <header class="nav" id="nav">
    <div class="nav-inner">
      <a href="../index.html" class="nav-logo">
        <img src="../images/footer-logo.webp" alt="BDX Smart Homes" />
      </a>
      <nav>
        <ul class="nav-links">
          <li><a href="../index.html#home">Home</a></li>
          <li><a href="../index.html#services">Services</a></li>
          <li><a href="../index.html#portfolio" class="active">Projects</a></li>
          <li><a href="../index.html#promise">7G Services</a></li>
          <li><a href="../index.html#faq">FAQ</a></li>
          <li><a href="../index.html#contact">Contact</a></li>
        </ul>
      </nav>
      <div class="nav-right">
        <a href="tel:+919150007269" class="nav-phone">
          <i data-lucide="phone" aria-hidden="true"></i>
          +91 91500 07269
        </a>
        <a href="../index.html#contact" class="btn-primary">Free Consultation</a>
        <button class="nav-hamburger" id="hamburger" aria-label="Open menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
    <div class="nav-mobile" id="nav-mobile">
      <a href="../index.html#home">Home</a>
      <a href="../index.html#services">Services</a>
      <a href="../index.html#portfolio">Projects</a>
      <a href="../index.html#promise">7G Services</a>
      <a href="../index.html#faq">FAQ</a>
      <a href="../index.html#contact">Contact</a>
      <a href="tel:+919150007269">\U0001F4DE +91 91500 07269</a>
      <a href="../index.html#contact" class="btn-primary">Free Consultation</a>
    </div>
  </header>

  <!-- BREADCRUMB -->
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <a href="../index.html" class="breadcrumb-link">Home</a>
    <span class="breadcrumb-sep">›</span>
    <a href="../all-projects.html" class="breadcrumb-link">All Projects</a>
    <span class="breadcrumb-sep">›</span>
    <span class="breadcrumb-current">{name}</span>
  </nav>

  <!-- PROJECT HERO -->
  <section class="proj-hero">
    <img
      src="{placeholder}"
      alt="{name} — completed {config} home in {location}, Chennai by BDX Smart Homes"
      class="proj-hero-image"
    />

    <div class="proj-hero-info">

      <span class="proj-status-chip done">Completed</span>

      <h1 class="proj-hero-name">{name}</h1>

      <p class="proj-hero-location">
        <i data-lucide="map-pin" aria-hidden="true"></i>
        {location}, Chennai
      </p>

      <div class="proj-stats-strip">
        <div class="proj-stat-box">
          <span>{area}</span>
          <label>Sq.ft Area</label>
        </div>
        <div class="proj-stat-box">
          <span>{config}</span>
          <label>Configuration</label>
        </div>
        <div class="proj-stat-box">
          <span>{floors}</span>
          <label>Floors</label>
        </div>
      </div>

      <div>
        <p class="proj-features-heading">Key Features</p>
        <ul class="proj-features-list">
{features_html}
        </ul>
      </div>

      <button class="btn-primary proj-cta-btn" id="projCtaBtn">
        Let's Build Yours <i data-lucide="arrow-right" class="btn-arrow"></i>
      </button>
    </div>
  </section>
  <!-- ── OVERVIEW ── -->
  <section class="proj-overview">
    <div class="proj-overview-inner">
      <div class="proj-overview-desc">
        <span class="section-eyebrow">About This Project</span>
        <h2 class="section-heading proj-section-heading">Project Overview</h2>
{overview_html}
      </div>
      <div>
        <div class="proj-specs-table">
{specs_html}
        </div>
      </div>
    </div>
  </section>

  <!-- ── GALLERY ── -->
  <section class="proj-gallery">
    <div class="proj-gallery-inner">
      <span class="section-eyebrow">Photo Gallery</span>
      <h2 class="section-heading proj-section-heading">The Home</h2>
      <div class="proj-gallery-grid proj-gallery-grid--single">
        <a class="proj-gallery-item" data-index="0"><img src="{placeholder}" alt="{name} — photos coming soon" /></a>
      </div>
    </div>
  </section>
  <div class="proj-lightbox" id="projLightbox">
    <button class="proj-lb-close" id="lbClose" aria-label="Close"><svg viewBox="0 0 24 24" fill="none"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
    <button class="proj-lb-prev"  id="lbPrev"  aria-label="Previous"><svg viewBox="0 0 24 24" fill="none"><polyline points="15 18 9 12 15 6"/></svg></button>
    <img class="proj-lightbox-img" id="lbImg" src="" alt="" />
    <button class="proj-lb-next"  id="lbNext"  aria-label="Next"><svg viewBox="0 0 24 24" fill="none"><polyline points="9 18 15 12 9 6"/></svg></button>
  </div>
{testimonial_html}
  <!-- ── RELATED PROJECTS ── -->
  <section class="proj-related">
    <div class="proj-related-inner">
      <span class="section-eyebrow">More Projects</span>
      <h2 class="section-heading proj-section-heading">You May Also Like</h2>
      <div class="proj-related-grid">
{related_html}
      </div>
    </div>
  </section>

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
        <button type="submit" class="btn-primary form-submit">Submit</button>
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
          <li><a href="../careers.html">Careers</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 class="footer-col-heading">Legal</h4>
        <ul class="footer-links">
          <li><a href="../privacy-policy.html">Privacy Policy</a></li>
          <li><a href="#">Terms of Service</a></li>
          <li><a href="#">Disclaimer</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 BDX Smart Homes. All rights reserved.</p>
      <p>Designed &amp; Developed by <a href="https://www.digiboomi.com" class="footer-credit" target="_blank" rel="noopener">✦ DigiBoomi</a></p>
    </div>
  </footer>

  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    lucide.createIcons();
    (function () {{
      const lightbox = document.getElementById('projLightbox');
      const lbImg    = document.getElementById('lbImg');
      const items    = Array.from(document.querySelectorAll('.proj-gallery-item'));
      const srcs     = items.map(el => el.querySelector('img').src);
      const alts     = items.map(el => el.querySelector('img').alt);
      let current    = 0;
      function open(i) {{ current = i; lbImg.src = srcs[i]; lbImg.alt = alts[i]; lightbox.classList.add('open'); document.body.style.overflow = 'hidden'; }}
      function close() {{ lightbox.classList.remove('open'); document.body.style.overflow = ''; }}
      function prev()  {{ open((current - 1 + srcs.length) % srcs.length); }}
      function next()  {{ open((current + 1) % srcs.length); }}
      items.forEach((el, i) => el.addEventListener('click', e => {{ e.preventDefault(); open(i); }}));
      document.getElementById('lbClose').addEventListener('click', close);
      document.getElementById('lbPrev').addEventListener('click', prev);
      document.getElementById('lbNext').addEventListener('click', next);
      lightbox.addEventListener('click', e => {{ if (e.target === lightbox) close(); }});
      document.addEventListener('keydown', e => {{
        if (!lightbox.classList.contains('open')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowLeft') prev();
        if (e.key === 'ArrowRight') next();
      }});
    }})();
    const nav = document.getElementById('nav');
    window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 10));
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('nav-mobile');
    hamburger.addEventListener('click', () => mobileMenu.classList.toggle('open'));
    mobileMenu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => mobileMenu.classList.remove('open')));
    (function () {{
      const backdrop = document.getElementById('cfModalBackdrop');
      const closeBtn = document.getElementById('cfModalClose');
      const ctaBtn   = document.getElementById('projCtaBtn');
      if (!backdrop || !ctaBtn) return;
      function openModal() {{ document.body.style.overflow = 'hidden'; backdrop.classList.add('open'); backdrop.removeAttribute('aria-hidden'); closeBtn.focus({{ preventScroll: true }}); }}
      function closeModal() {{ backdrop.classList.remove('open'); backdrop.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; ctaBtn.focus({{ preventScroll: true }}); }}
      ctaBtn.addEventListener('click', openModal);
      closeBtn.addEventListener('click', closeModal);
      backdrop.addEventListener('click', e => {{ if (e.target === backdrop) closeModal(); }});
      document.addEventListener('keydown', e => {{ if (e.key === 'Escape' && backdrop.classList.contains('open')) closeModal(); }});
    }})();
    (function () {{
      const form = document.getElementById('projContactForm');
      if (!form) return;
      function showError(field, msg) {{
        field.classList.add('input-error');
        const err = document.createElement('span');
        err.className = 'form-error';
        err.textContent = msg;
        field.closest('.form-field').appendChild(err);
      }}
      form.querySelectorAll('input').forEach(input => {{
        input.addEventListener('input', () => {{
          input.classList.remove('input-error');
          const err = input.closest('.form-field')?.querySelector('.form-error');
          if (err) err.remove();
        }});
      }});
      form.addEventListener('submit', e => {{
        e.preventDefault();
        form.querySelectorAll('.form-error').forEach(el => el.remove());
        form.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));
        let valid = true;
        const phone = form.querySelector('[type="tel"]');
        const email = form.querySelector('[type="email"]');
        const digits = phone.value.replace(/\\D/g, '');
        if (!digits) {{ showError(phone, 'Phone number is required.'); valid = false; }}
        else if (digits.length !== 10) {{ showError(phone, 'Enter a valid 10-digit phone number.'); valid = false; }}
        const emailVal = email.value.trim();
        if (!emailVal) {{ showError(email, 'Email address is required.'); valid = false; }}
        else if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(emailVal)) {{ showError(email, 'Enter a valid email address.'); valid = false; }}
        if (!valid) return;
        form.innerHTML = `<div class="form-success"><i data-lucide="circle-check-big" class="form-success-icon"></i><h4>Thank you!</h4><p>We've received your details and will reach out within 24 hours.</p></div>`;
        lucide.createIcons();
      }});
    }})();
  </script>
  <script src="../transitions.js"></script>

  <!-- WHATSAPP FLOAT -->
  <a href="https://wa.me/919150007269" class="whatsapp-float" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  </a>
</body>
</html>
"""


def build_page(p):
    features_html = "\n".join(
        f'          <li><i data-lucide="check-circle" aria-hidden="true"></i> {f}</li>'
        for f in features_list(p)
    )
    specs_html = "\n".join(
        f'          <div class="proj-spec-row"><span class="proj-spec-label">{label}</span><span class="proj-spec-value">{value}</span></div>'
        for label, value in spec_rows(p)
    )
    overview_html = "\n".join(f"        <p>{para}</p>" for para in overview_paragraphs(p))
    return PAGE_TEMPLATE.format(
        name=p["name"], config=p["config"], area=p["area"], floors=p["floors"],
        location=p["location"], placeholder=PLACEHOLDER_IMG,
        features_html=features_html, specs_html=specs_html, overview_html=overview_html,
        testimonial_html=testimonial_section(p), related_html=related_section(p),
    )


def card_html(p):
    sqft = int(float(p["area"]))
    return f"""      <div class="proj-card" data-status="done" data-sqft="{sqft}">
        <img src="{PLACEHOLDER_IMG_ROOT}" alt="{p['name']} — completed {p['config']} home in {p['location']}, Chennai" class="proj-img" />
        <div class="proj-overlay">
          <div class="proj-info">
            <h3 class="proj-name">{p['name']}</h3>
            <p class="proj-location"><i data-lucide="map-pin" aria-hidden="true"></i> {p['location']}</p>
          </div>
        </div>
        <a href="projects/{p['slug']}.html" class="proj-hover-btn">View This Project <i data-lucide="arrow-right" class="btn-arrow"></i></a>
        <span class="proj-chip proj-chip--done">Completed</span>
      </div>
"""


def main():
    projects_dir = os.path.join(REPO, "projects")
    for p in PROJECTS:
        out_path = os.path.join(projects_dir, f"{p['slug']}.html")
        with open(out_path, "w") as f:
            f.write(build_page(p))
        print(f"wrote projects/{p['slug']}.html")

    cards = "\n".join(card_html(p) for p in PROJECTS)
    all_projects_path = os.path.join(REPO, "all-projects.html")
    with open(all_projects_path) as f:
        content = f.read()
    marker = '    </div>\n\n    <!-- INFINITE SCROLL SENTINEL -->'
    if marker not in content:
        raise SystemExit("Could not find insertion marker in all-projects.html")
    content = content.replace(marker, cards + marker, 1)
    with open(all_projects_path, "w") as f:
        f.write(content)
    print(f"appended {len(PROJECTS)} cards to all-projects.html")


if __name__ == "__main__":
    main()
