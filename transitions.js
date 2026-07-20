document.addEventListener('click', function (e) {
  const link = e.target.closest('a[href]');
  if (!link) return;
  const href = link.getAttribute('href');
  if (!href || href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:') || link.target === '_blank') return;
  const url = new URL(href, location.href);
  if (url.origin !== location.origin) return;
  e.preventDefault();
  document.body.classList.add('page-leaving');
  setTimeout(function () { location.href = href; }, 260);
});
