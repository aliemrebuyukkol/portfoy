"use strict";
(function () {
  const imgs = Array.from(document.querySelectorAll('.shot img, .dio img, .hero-img img'));
  if (!imgs.length) return;

  const dlg = document.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.setAttribute('aria-label', 'Görsel önizleme');
  dlg.innerHTML =
    '<div class="lb-shell">' +
      '<button type="button" class="lb-btn lb-close" aria-label="Kapat">' +
        '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M4 4l10 10M14 4 4 14" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>' +
      '</button>' +
      '<img class="lb-img" alt="">' +
      '<div class="lb-foot">' +
        '<button type="button" class="lb-btn lb-prev" aria-label="Önceki görsel">' +
          '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3 5 8l5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>' +
        '</button>' +
        '<div class="lb-meta"><p class="lb-cap"></p><span class="lb-count"></span></div>' +
        '<button type="button" class="lb-btn lb-next" aria-label="Sonraki görsel">' +
          '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>' +
        '</button>' +
      '</div>' +
    '</div>';
  document.body.appendChild(dlg);

  const shell = dlg.querySelector('.lb-shell');
  const pic = dlg.querySelector('.lb-img');
  const cap = dlg.querySelector('.lb-cap');
  const count = dlg.querySelector('.lb-count');
  const prevBtn = dlg.querySelector('.lb-prev');
  const nextBtn = dlg.querySelector('.lb-next');
  const closeBtn = dlg.querySelector('.lb-close');
  let idx = 0, opener = null, touch = null;

  if (imgs.length <= 1) {
    prevBtn.hidden = true;
    nextBtn.hidden = true;
    count.hidden = true;
  }

  const show = (i) => {
    idx = (i + imgs.length) % imgs.length;
    const srcImg = imgs[idx];
    const fig = srcImg.closest('figure');
    const fc = fig && fig.querySelector('figcaption');
    pic.src = srcImg.currentSrc || srcImg.src;
    pic.alt = srcImg.alt || '';
    cap.textContent = fc ? fc.textContent : '';
    cap.hidden = !cap.textContent;
    count.textContent = (idx + 1) + ' / ' + imgs.length;
  };

  const syncLabels = () => {
    const en = document.documentElement.lang === 'en';
    dlg.setAttribute('aria-label', en ? 'Image preview' : 'Görsel önizleme');
    closeBtn.setAttribute('aria-label', en ? 'Close' : 'Kapat');
    prevBtn.setAttribute('aria-label', en ? 'Previous image' : 'Önceki görsel');
    nextBtn.setAttribute('aria-label', en ? 'Next image' : 'Sonraki görsel');
    imgs.forEach((img) => {
      const fig = img.closest('figure');
      const fc = fig && fig.querySelector('figcaption');
      img.setAttribute('aria-label', (fc ? fc.textContent + ' — ' : '') + (en ? 'zoom image' : 'görseli büyüt'));
    });
    if (dlg.open) show(idx);
  };

  const openAt = (i, trigger) => {
    opener = trigger || imgs[i];
    show(i);
    if (dlg.showModal) dlg.showModal();
    else dlg.setAttribute('open', '');
  };

  const close = () => {
    if (dlg.close) dlg.close();
    else dlg.removeAttribute('open');
  };

  imgs.forEach((img, i) => {
    img.tabIndex = 0;
    img.setAttribute('role', 'button');
    img.addEventListener('click', () => openAt(i, img));
    img.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openAt(i, img); }
    });
  });
  syncLabels();
  window.addEventListener('buyukkol:lang', syncLabels);

  prevBtn.addEventListener('click', () => show(idx - 1));
  nextBtn.addEventListener('click', () => show(idx + 1));
  closeBtn.addEventListener('click', close);

  shell.addEventListener('click', (e) => {
    if (e.target === shell) close();
  });

  dlg.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
  });

  dlg.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) touch = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  }, { passive: true });
  dlg.addEventListener('touchend', (e) => {
    if (!touch || e.changedTouches.length !== 1) { touch = null; return; }
    const dx = e.changedTouches[0].clientX - touch.x;
    const dy = e.changedTouches[0].clientY - touch.y;
    touch = null;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.3) show(idx + (dx < 0 ? 1 : -1));
  });

  dlg.addEventListener('close', () => {
    if (opener && opener.focus) opener.focus({ preventScroll: true });
    opener = null;
  });
})();
