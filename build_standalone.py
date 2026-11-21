"""Design tuvalindeki Main.dc.html'den bağımsız, alan adına konabilir index.html üretir.
Motor (buildAudio/buildGame) ve CSS tek kaynaktan alınır; arayüz sade JS ile yönetilir."""
import re, pathlib

root = pathlib.Path(__file__).parent
src = (root / 'tasarim' / 'Main.dc.html').read_text()

css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
script = re.search(r'data-dc-script[^>]*>(.*?)</script>', src, re.S).group(1)
start = script.index('  /* ================= Ambiyans sesi')
end = script.rstrip().rindex('}')  # class Component kapanışı
engine = script[start:end]
zones = re.search(r'  zones = \[(.*?)\n  \];', script, re.S).group(1)
PROJECTS = zones.count("type: 'project'")

ICON_ON = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M2.5 7v4h3l4 3.5v-11l-4 3.5h-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 6.5a3.5 3.5 0 0 1 0 5M14.5 4a7 7 0 0 1 0 10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
ICON_OFF = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M2.5 7v4h3l4 3.5v-11l-4 3.5h-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M12.5 6.5l4 5M16.5 6.5l-4 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
ARROW_UP = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>'
ARROW_R = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>'
APPLE_ICO = '<svg width="15" height="18" viewBox="0 0 18 22" fill="currentColor" aria-hidden="true"><path d="M14.94 11.58c-.02-2.29 1.87-3.4 1.96-3.45-1.07-1.56-2.73-1.77-3.32-1.8-1.4-.14-2.75.83-3.46.83-.72 0-1.82-.81-3-.79-1.53.02-2.95.9-3.74 2.27-1.61 2.79-.41 6.91 1.14 9.17.76 1.11 1.67 2.35 2.86 2.3 1.15-.05 1.59-.74 2.98-.74 1.39 0 1.79.74 3 .71 1.24-.02 2.02-1.12 2.77-2.23.88-1.28 1.24-2.53 1.26-2.59-.03-.01-2.43-.93-2.45-3.68ZM12.66 4.84c.63-.77 1.06-1.83.94-2.89-.91.04-2.02.61-2.67 1.37-.58.67-1.1 1.76-.96 2.79 1.02.08 2.06-.51 2.69-1.27Z"/></svg>'
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' shape-rendering='crispEdges'%3E%3Crect width='16' height='16' fill='%23141A30'/%3E%3Crect x='5' y='2' width='6' height='2' fill='%2369964B'/%3E%3Crect x='3' y='4' width='10' height='5' fill='%23426D3E'/%3E%3Crect x='4' y='5' width='3' height='2' fill='%2369964B'/%3E%3Crect x='7' y='9' width='2' height='4' fill='%235A3F2A'/%3E%3Crect x='11' y='11' width='2' height='2' fill='%23F6B26B'/%3E%3C/svg%3E"

chips = ''.join(
    f'<button type="button" class="chip" data-zone="{i}" aria-pressed="false"><span aria-hidden="true" class="chip-dot"></span><span class="chip-name"></span><span class="seen" aria-label="keşfedildi" hidden>✓</span></button>'
    for i in range(1, PROJECTS + 1))

html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#141A30">
<title>Ali Emre Büyükkol — Portföy ormanı</title>
<meta name="description" content="Ali Emre Büyükkol'un portföyü: piksel bir ormanda yürü; Cozy Camp, Suçüstü, Hoşgeldiniz Efendim, Pati Kulaç ve Muchineko projelerini keşfet.">
<meta property="og:title" content="BÜYÜKKOL — Portföy ormanı">
<meta property="og:description" content="Fenerini al, ormanda yürü. Her köşede başka bir proje, başka bir hava var.">
<meta property="og:type" content="website">
<link rel="canonical" href="https://buyukkol.com/">
<link rel="alternate" hreflang="tr" href="https://buyukkol.com/">
<link rel="alternate" hreflang="en" href="https://buyukkol.com/en/">
<link rel="alternate" hreflang="x-default" href="https://buyukkol.com/">
<meta property="og:url" content="https://buyukkol.com/">
<meta property="og:site_name" content="Büyükkol">
<meta property="og:locale" content="tr_TR">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:image" content="https://buyukkol.com/img/og-orman.png">
<meta property="og:image:secure_url" content="https://buyukkol.com/img/og-orman.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Piksel bir ormanda kulübe, kamp ateşi, fener taşıyan gezgin ve BÜYÜKKOL portföy ormanı başlığı.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="BÜYÜKKOL — Portföy ormanı">
<meta name="twitter:description" content="Fenerini al, ormanda yürü. Her köşede başka bir proje, başka bir hava var.">
<meta name="twitter:image" content="https://buyukkol.com/img/og-orman.png">
<meta name="twitter:image:alt" content="Piksel bir ormanda kulübe, kamp ateşi, fener taşıyan gezgin ve BÜYÜKKOL portföy ormanı başlığı.">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Space+Grotesk:wght@500;700&amp;family=Pixelify+Sans:wght@400;600&amp;display=swap" rel="stylesheet">
<style>{css}
[hidden]{{display:none !important}}
.chip-dot{{width:8px;height:8px;display:inline-block}}
</style>
</head>
<body>
<div class="root is-intro" id="root">
<div class="stage">
<canvas class="scene" id="scene" tabindex="0" role="img" aria-label="Piksel sanat bir orman: girişte bir kulübe, kamp ateşinin başında bir keşiş, çiçekli ağacın altında kediler, gölette yüzen kediler, dans pistinde hem çöp atıp hem süpüren dansçılar ve en sonda bir posta kutusu. Ok tuşlarıyla ya da kaydırarak yürüyebilirsin."></canvas>
</div>
<div class="bubble" id="bubble" aria-hidden="true"></div>

<section class="intro" id="intro" aria-label="Başlangıç">
<button type="button" class="hud-btn intro-lang" id="intro-lang" aria-label="Switch to English">EN</button>
<p id="intro-eyebrow" style="margin:0;font-family:'Pixelify Sans',monospace;font-size:15px;letter-spacing:.14em;color:#F6B26B">BİR PORTFÖY ORMANI</p>
<h1>BÜYÜKKOL</h1>
<p id="intro-desc" style="margin:0;max-width:34ch;font-size:clamp(16px,1.6vw,19px);line-height:1.5;color:#E4DDEC">Fenerini al, ormanda yürü. Her köşede başka bir proje, başka bir hava var.</p>
<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center">
<button type="button" class="intro-btn intro-p" id="enter-sound">Sesle gir</button>
<button type="button" class="intro-btn intro-g" id="enter-quiet">Sessiz gir</button>
</div>
<p style="margin:0;font-family:'Pixelify Sans',monospace;font-size:13px;letter-spacing:.08em;color:#B9B3CC"><span class="keys" id="intro-keys">← → İLE YÜRÜ · DOKUN, ORAYA GİT · 1–5 İLE PROJEYE ATLA</span><span class="touch" id="intro-touch">DOKUN, ORAYA GİT · KAYDIR, SONRAKİ PROJE</span></p>
<noscript><p style="color:#FFD28A">Orman JavaScript ile çalışıyor. Lütfen JavaScript'i aç.</p></noscript>
</section>

<div id="hud" hidden>
<header class="top">
<div style="display:flex;flex-direction:column">
<a href="#" class="logo" id="logo">BÜYÜKKOL</a>
<span class="tagline" id="tagline" style="font-size:14px;color:#D9D2E6;text-shadow:0 1px 0 rgba(14,16,30,.8)">Ormanda dolaş, her köşede başka bir proje var.</span>
</div>
<div style="display:flex;gap:8px">
<button type="button" class="hud-btn" id="snd" aria-pressed="false" aria-label="Ambiyansı aç"><span id="snd-on" hidden>{ICON_ON}</span><span id="snd-off" style="display:inline-flex">{ICON_OFF}</span><span class="lbl" id="snd-lbl">Ambiyansı aç</span></button>
<button type="button" class="hud-btn" id="go-about" aria-label="Hakkımda"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><circle cx="9" cy="6" r="3" stroke="currentColor" stroke-width="1.6"/><path d="M3 15.5c.8-3 3.2-4.5 6-4.5s5.2 1.5 6 4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><span class="lbl" id="about-lbl">Hakkımda</span></button>
<button type="button" class="hud-btn" id="go-contact" aria-label="İletişim"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><rect x="2" y="4" width="14" height="10" rx="1" stroke="currentColor" stroke-width="1.6"/><path d="m2.5 5 6.5 5 6.5-5" stroke="currentColor" stroke-width="1.6"/></svg><span class="lbl" id="contact-lbl">İletişim</span></button>
<button type="button" class="hud-btn lang-code" id="lang-btn" aria-label="Switch to English">EN</button>
</div>
</header>

<section class="card" id="card" aria-live="polite">
<div style="display:flex;align-items:center;gap:10px">
<span aria-hidden="true" id="c-dot" style="width:10px;height:10px"></span>
<span id="c-eyebrow" style="font-family:'Pixelify Sans',monospace;font-size:13px;letter-spacing:.12em;color:#C9C3D9"></span>
</div>
<h2 id="c-name"></h2>
<p class="card-vibe" id="c-vibe"></p>
<div id="c-project" style="display:flex;flex-direction:column;gap:inherit">
<p class="card-desc" id="c-desc"></p>
<div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap"><a href="#" class="cta cta-store" id="c-store" target="_blank" rel="noopener" hidden>{APPLE_ICO}<span id="c-store-lbl">App Store'dan indir</span>{ARROW_UP}</a><a href="#" class="cta" id="c-cta"><span id="c-cta-lbl">Projeye git</span>{ARROW_UP}</a><span class="cta cta-soon" id="c-soon" hidden>Yakında</span><button type="button" class="cta cta-ghost" id="c-next"><span id="c-next-lbl"></span>{ARROW_R}</button></div>
</div>
<div id="c-about" hidden style="flex-direction:column;gap:inherit">
<p class="card-desc" id="about-desc">Amatör bir vibecoder. Uygulamalar, oyunlar ve küçük dijital dünyalar yapıyorum; güzel ve biraz farklı görünsünler diye. Ormanda yürü, her durakta biri seni bekliyor.</p>
<div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap"><a href="hakkimda.html" class="cta" id="know-me">Beni tanı</a><button type="button" class="cta" id="go-first" style="background:transparent;color:#F3ECDD;box-shadow:inset 0 0 0 1px rgba(243,236,221,.4)"><span id="go-first-lbl">İlk projeye yürü</span>{ARROW_R}</button></div>
</div>
<div id="c-contact" hidden style="flex-direction:column;gap:inherit">
<div class="links"><a href="mailto:aliemrebuyukkol@gmail.com">aliemrebuyukkol@gmail.com</a><a href="https://github.com/aliemrebuyukkol" target="_blank" rel="noopener">GitHub</a></div>
<div style="display:flex;gap:8px;flex-wrap:wrap"><a href="mailto:aliemrebuyukkol@gmail.com" class="cta" id="c-mail-cta">Mektup yaz</a><button type="button" class="cta cta-ghost" id="copy-mail">E-postayı kopyala</button><button type="button" class="cta cta-ghost" id="go-home">Başa dön</button></div>
</div>
</section>

<nav class="dock" id="dock" aria-label="Projeler">
<div class="dock-row">
<button type="button" class="hud-btn navbtn" id="prev" aria-label="Önceki durak"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3 5 8l5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg></button>
<div class="chips" id="chips">{chips}</div>
<button type="button" class="hud-btn navbtn" id="next" aria-label="Sonraki durak"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m6 3 5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg></button>
</div>
<span class="hint" id="hint"></span>
</nav>
</div>
</div>

<script src="engine.js"></script>
<script>
"use strict";
const Engine = window.BuyukkolEngine;

(function () {{
  const zones = [{zones}
  ];
  const IDS = ['kulube', 'cozy-camp', 'sucustu', 'hosgeldiniz-efendim', 'pati-kulac', 'muchineko', 'posta'];
  const LAST = IDS.length - 1, NPROJ = {PROJECTS};
  const loadLang = () => {{
    try {{
      const q = new URLSearchParams(location.search).get('lang');
      if (q === 'en' || q === 'tr') {{ localStorage.setItem('buyukkol.lang', q); return q; }}
      const s = localStorage.getItem('buyukkol.lang');
      if (s === 'en' || s === 'tr') return s;
    }} catch (e) {{}}
    return (navigator.language || '').toLowerCase().indexOf('tr') === 0 ? 'tr' : 'en';
  }};
  const saveLang = (l) => {{ try {{ localStorage.setItem('buyukkol.lang', l); }} catch (e) {{}} }};
  const loadSeen = () => {{ try {{ const v = JSON.parse(localStorage.getItem('buyukkol.seen.v2') || '[]'); return Array.isArray(v) ? v.filter((n) => Number.isInteger(n) && n >= 1 && n <= NPROJ) : []; }} catch (e) {{ return []; }} }};
  const saveSeen = (v) => {{ try {{ localStorage.setItem('buyukkol.seen.v2', JSON.stringify(v)); }} catch (e) {{ /* depolama yoksa sessizce geç */ }} }};
  const st = {{ zone: 0, sound: false, intro: true, seen: loadSeen(), lang: loadLang(), copied: false }};
  const $ = (id) => document.getElementById(id);
  const chipEls = Array.from(document.querySelectorAll('.chip'));
  const T = {{
    tr: {{
      title: 'Ali Emre Büyükkol — Portföy ormanı',
      scene: 'Piksel sanat bir orman: girişte bir kulübe, kamp ateşinin başında bir keşiş, çiçekli ağacın altında kediler, gölette yüzen kediler, dans pistinde hem çöp atıp hem süpüren dansçılar ve en sonda bir posta kutusu. Ok tuşlarıyla ya da kaydırarak yürüyebilirsin.',
      introAria: 'Başlangıç',
      introEyebrow: 'BİR PORTFÖY ORMANI',
      introDesc: 'Fenerini al, ormanda yürü. Her köşede başka bir proje, başka bir hava var.',
      enterSound: 'Sesle gir',
      enterQuiet: 'Sessiz gir',
      keys: '← → İLE YÜRÜ · DOKUN, ORAYA GİT · 1–5 İLE PROJEYE ATLA',
      touch: 'DOKUN, ORAYA GİT · KAYDIR, SONRAKİ PROJE',
      tagline: 'Ormanda dolaş, her köşede başka bir proje var.',
      soundOn: 'Sesi kapat',
      soundOff: 'Ambiyansı aç',
      about: 'Hakkımda',
      contact: 'İletişim',
      projectPrefix: 'PROJE ',
      storeCta: "App Store'dan indir",
      goProj: 'Projeye git',
      soon: 'Yakında',
      nextPrefix: 'Sonraki: ',
      aboutDesc: 'Amatör bir vibecoder. Uygulamalar, oyunlar ve küçük dijital dünyalar yapıyorum; güzel ve biraz farklı görünsünler diye. Ormanda yürü, her durakta biri seni bekliyor.',
      knowMe: 'Beni tanı',
      firstProj: 'İlk projeye yürü',
      writeMail: 'Mektup yaz',
      copyMail: 'E-postayı kopyala',
      copied: 'Kopyalandı ✓',
      home: 'Başa dön',
      dockAria: 'Projeler',
      prevAria: 'Önceki durak',
      nextAria: 'Sonraki durak',
      seenAria: 'keşfedildi',
      foundAll: 'HEPSİNİ BULDUN! ',
      foundPart: 'KEŞİF ',
      walkHint: '← → İLE YÜRÜ',
      langBtn: 'EN',
      langAria: 'Switch to English'
    }},
    en: {{
      title: 'Ali Emre Büyükkol — Portfolio Woods',
      scene: 'A pixel-art forest: a cabin at the entrance, a monk by the campfire, cats beneath a blooming tree, cats swimming laps in a pond, dancers littering and sweeping on a dance floor, and a mailbox at the end. Walk with arrow keys or swipe.',
      introAria: 'Introduction',
      introEyebrow: 'A PORTFOLIO FOREST',
      introDesc: 'Grab your lantern, walk the woods. Every clearing holds a different project and mood.',
      enterSound: 'Enter with sound',
      enterQuiet: 'Enter quietly',
      keys: '← → TO WALK · TAP TO MOVE · 1–5 JUMP TO PROJECT',
      touch: 'TAP TO MOVE · SWIPE, NEXT PROJECT',
      tagline: 'Wander the woods, every corner holds a project.',
      soundOn: 'Mute sound',
      soundOff: 'Enable sound',
      about: 'About',
      contact: 'Contact',
      projectPrefix: 'PROJECT ',
      storeCta: 'Get on App Store',
      goProj: 'View project',
      soon: 'Soon',
      nextPrefix: 'Next: ',
      aboutDesc: 'An amateur vibecoder. I build apps, games, and tiny digital worlds so they feel warm and a bit unexpected. Walk the woods—each stop has someone waiting.',
      knowMe: 'About me',
      firstProj: 'Walk to first project',
      writeMail: 'Write an email',
      copyMail: 'Copy email',
      copied: 'Copied ✓',
      home: 'Back to start',
      dockAria: 'Projects',
      prevAria: 'Previous stop',
      nextAria: 'Next stop',
      seenAria: 'discovered',
      foundAll: 'FOUND THEM ALL! ',
      foundPart: 'FOUND ',
      walkHint: 'WALK WITH ← →',
      langBtn: 'TR',
      langAria: 'Türkçeye geç'
    }}
  }};

  const render = () => {{
    const en = st.lang === 'en', t = T[st.lang];
    const z = st.zone, p = zones[z];
    document.documentElement.lang = st.lang;
    document.title = t.title;
    $('scene').setAttribute('aria-label', t.scene);
    $('intro').setAttribute('aria-label', t.introAria);
    $('intro-eyebrow').textContent = t.introEyebrow;
    $('intro-desc').textContent = t.introDesc;
    $('enter-sound').textContent = t.enterSound;
    $('enter-quiet').textContent = t.enterQuiet;
    $('intro-keys').textContent = t.keys;
    $('intro-touch').textContent = t.touch;
    $('intro-lang').textContent = t.langBtn;
    $('intro-lang').setAttribute('aria-label', t.langAria);
    $('tagline').textContent = t.tagline;
    $('go-about').setAttribute('aria-label', t.about); $('about-lbl').textContent = t.about;
    $('go-contact').setAttribute('aria-label', t.contact); $('contact-lbl').textContent = t.contact;
    $('lang-btn').textContent = t.langBtn; $('lang-btn').setAttribute('aria-label', t.langAria);
    $('c-cta-lbl').textContent = t.goProj;
    $('c-store-lbl').textContent = t.storeCta;
    $('c-soon').textContent = t.soon;
    $('about-desc').textContent = t.aboutDesc;
    $('know-me').textContent = t.knowMe;
    $('go-first-lbl').textContent = t.firstProj;
    $('c-mail-cta').textContent = t.writeMail;
    $('copy-mail').textContent = st.copied ? t.copied : t.copyMail;
    $('go-home').textContent = t.home;
    $('dock').setAttribute('aria-label', t.dockAria);
    $('prev').setAttribute('aria-label', t.prevAria);
    $('next').setAttribute('aria-label', t.nextAria);

    $('root').className = st.intro ? 'root is-intro' : 'root';
    $('intro').hidden = !st.intro;
    $('hud').hidden = st.intro;
    $('snd').setAttribute('aria-pressed', st.sound ? 'true' : 'false');
    const sl = st.sound ? t.soundOn : t.soundOff;
    $('snd').setAttribute('aria-label', sl); $('snd-lbl').textContent = sl;
    $('snd-on').hidden = !st.sound; $('snd-on').style.display = st.sound ? 'inline-flex' : '';
    $('snd-off').hidden = st.sound; $('snd-off').style.display = st.sound ? '' : 'inline-flex';
    let pi = 0;
    zones.forEach((q, i) => {{ if (q.type === 'project' && i <= z) pi++; }});
    $('c-dot').style.background = p.color;
    const pKind = en && p.kindEn ? p.kindEn : p.kind;
    const pEyebrow = en && p.eyebrowEn ? p.eyebrowEn : p.eyebrow;
    const pName = en && p.nameEn ? p.nameEn : p.name;
    const pVibe = en && p.vibeEn ? p.vibeEn : p.vibe;
    const pDesc = en && p.descEn ? p.descEn : p.desc;
    const pSay = en && p.sayEn ? p.sayEn : p.say;
    $('c-eyebrow').textContent = p.type === 'project' ? t.projectPrefix + pi + ' / ' + NPROJ + (pKind ? ' · ' + pKind : '') : pEyebrow;
    $('c-name').textContent = pName; $('c-name').style.color = p.color;
    $('c-vibe').textContent = pVibe;
    $('c-store').href = p.storeHref || '#'; $('c-store').hidden = !p.storeHref;
    $('c-cta').href = p.href || '#'; $('c-cta').hidden = !p.href; $('c-soon').hidden = !!p.href;
    $('c-cta').className = p.storeHref ? 'cta cta-ghost' : 'cta';
    if (p.ext) {{ $('c-cta').target = '_blank'; $('c-cta').rel = 'noopener'; }} else {{ $('c-cta').removeAttribute('target'); $('c-cta').removeAttribute('rel'); }}
    const nz = zones[z + 1];
    const nzName = nz ? (nz.type === 'contact' ? t.contact : (en && nz.nameEn ? nz.nameEn : nz.name)) : '';
    $('c-next').hidden = !nz; $('c-next-lbl').textContent = nz ? t.nextPrefix + nzName : '';
    const d = $('c-desc'); d.textContent = '';
    if (pDesc) d.textContent = pDesc;
    else {{ const ph = document.createElement('span'); ph.className = 'ph'; ph.textContent = '[Tek cümlelik proje açıklaması]'; d.appendChild(ph); }}
    [['c-project', 'project'], ['c-about', 'about'], ['c-contact', 'contact']].forEach(([id, type]) => {{
      const on = p.type === type; $(id).hidden = !on; $(id).style.display = on ? 'flex' : '';
    }});
    chipEls.forEach((b) => {{
      const i = +b.dataset.zone, on = i === z, cq = zones[i];
      b.querySelector('.chip-name').textContent = (en && cq.nameEn) ? cq.nameEn : cq.name;
      b.querySelector('.chip-dot').style.background = cq.color;
      b.className = 'chip' + (on ? ' on' : '');
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      const seenEl = b.querySelector('.seen');
      seenEl.hidden = st.seen.indexOf(i) < 0;
      seenEl.setAttribute('aria-label', t.seenAria);
    }});
    const found = st.seen.length;
    $('hint').textContent = (found === NPROJ ? t.foundAll : t.foundPart + found + '/' + NPROJ + ' · ') + t.walkHint;
    $('bubble').textContent = pSay;
  }};

  const eng = new Engine();
  const game = eng.buildGame($('scene'), {{
    onZone: (i) => {{
      if (i === st.zone) return;
      const fresh = zones[i].type === 'project' && st.seen.indexOf(i) < 0;
      if (fresh && !st.intro && navigator.vibrate && (!navigator.userActivation || navigator.userActivation.hasBeenActive)) {{ try {{ navigator.vibrate(12); }} catch (e) {{ /* desteklenmiyor */ }} }}
      st.zone = i;
      if (fresh) {{ st.seen = st.seen.concat([i]); saveSeen(st.seen); if (st.seen.length === NPROJ) game.celebrate(); }}
      if (!st.intro && history.replaceState) {{ try {{ history.replaceState(null, '', i === 0 ? location.pathname + location.search : '#' + IDS[i]); }} catch (e) {{ /* sessizce geç */ }} }}
      render();
      const on = document.querySelector('.chip.on');
      const box = $('chips');
      if (on && box.scrollTo) box.scrollTo({{ left: Math.max(0, on.offsetLeft - (box.clientWidth - on.offsetWidth) / 2), behavior: 'smooth' }});
    }},
    bubble: () => $('bubble'),
    card: () => $('card')
  }}, eng.buildAudio());

  const go = (i) => game.go(Math.max(0, Math.min(LAST, i)));
  const enter = (sound) => {{ st.intro = false; st.sound = sound; render(); if (sound) game.setSound(true); game.begin(); $('scene').focus({{ preventScroll: true }}); }};
  $('enter-sound').addEventListener('click', () => enter(true));
  $('enter-quiet').addEventListener('click', () => enter(false));
  $('snd').addEventListener('click', () => {{ st.sound = !st.sound; render(); game.setSound(st.sound); }});
  $('go-about').addEventListener('click', () => go(0));
  $('logo').addEventListener('click', (e) => {{ e.preventDefault(); go(0); }});
  $('go-contact').addEventListener('click', () => go(LAST));
  $('go-home').addEventListener('click', () => go(0));
  $('c-next').addEventListener('click', () => go(st.zone + 1));
  $('go-first').addEventListener('click', () => go(1));
  $('prev').addEventListener('click', () => go(st.zone - 1));
  $('next').addEventListener('click', () => go(st.zone + 1));
  chipEls.forEach((b) => b.addEventListener('click', () => go(+b.dataset.zone)));
  const toggleLang = () => {{ st.lang = st.lang === 'en' ? 'tr' : 'en'; saveLang(st.lang); render(); }};
  $('lang-btn').addEventListener('click', toggleLang);
  $('intro-lang').addEventListener('click', toggleLang);
  let copyTimer = 0;
  $('copy-mail').addEventListener('click', () => {{
    const email = 'aliemrebuyukkol@gmail.com';
    const done = () => {{
      st.copied = true; render();
      clearTimeout(copyTimer);
      copyTimer = setTimeout(() => {{ st.copied = false; render(); }}, 2000);
    }};
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(email).then(done).catch(() => {{ fallbackCopy(email); done(); }});
    }} else {{
      fallbackCopy(email); done();
    }}
  }});
  function fallbackCopy(text) {{
    try {{
      const ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }} catch (e) {{}}
  }}

  const cv = $('scene');
  let ptr = null;
  cv.addEventListener('pointerdown', (e) => {{ ptr = {{ x: e.clientX, y: e.clientY, t: Date.now(), id: e.pointerId }}; if (e.pointerType === 'mouse') cv.focus({{ preventScroll: true }}); }});
  cv.addEventListener('pointerup', (e) => {{
    const p = ptr; ptr = null;
    if (!p || p.id !== e.pointerId || st.intro) return;
    const dx = e.clientX - p.x, dy = e.clientY - p.y, dt = Date.now() - p.t;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.3 && dt < 700) go(st.zone + (dx < 0 ? 1 : -1));
    else if (Math.abs(dx) < 12 && Math.abs(dy) < 12) game.tap(e.clientX, e.clientY, cv.getBoundingClientRect());
  }});
  cv.addEventListener('pointercancel', () => {{ ptr = null; }});
  const isL = (k) => k === 'ArrowLeft' || k === 'a' || k === 'A', isR = (k) => k === 'ArrowRight' || k === 'd' || k === 'D';
  window.addEventListener('keydown', (e) => {{
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const tag = e.target && e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
    if (st.intro) {{
      if ((e.key === 'Enter' || e.key === ' ') && !(e.target && e.target.closest && e.target.closest('button, a'))) {{
        e.preventDefault();
        enter(false);
      }}
      return;
    }}
    if (isL(e.key)) {{ game.hold(-1); e.preventDefault(); }}
    else if (isR(e.key)) {{ game.hold(1); e.preventDefault(); }}
    else if (e.key >= '1' && e.key <= String(NPROJ)) go(+e.key);
    else if (e.key === '0' || e.key === 'Home') {{ go(0); if (e.key === 'Home') e.preventDefault(); }}
    else if (e.key === String(LAST) || e.key === 'End') {{ go(LAST); if (e.key === 'End') e.preventDefault(); }}
  }});
  window.addEventListener('keyup', (e) => {{ if (isL(e.key) || isR(e.key)) game.hold(0); }});
  window.addEventListener('blur', () => game.hold(0));
  cv.addEventListener('blur', () => game.hold(0));
  render();
  // Bir proje sayfasından dönüş: index.html#cozy-camp gibi bir adresle gelindiyse girişi atla, o durakta başla.
  const startAt = IDS.indexOf((location.hash || '').slice(1));
  if (startAt >= 0) {{ st.intro = false; render(); game.jump(startAt); }}
  window.addEventListener('hashchange', () => {{
    const i = IDS.indexOf((location.hash || '').slice(1));
    if (i < 0) return;
    if (st.intro) {{ st.intro = false; render(); game.jump(i); }} else go(i);
  }});
}})();
</script>
</body>
</html>
'''
(root / 'docs').mkdir(exist_ok=True)
(root / 'docs' / 'engine.js').write_text('"use strict";\n/* Büyükkol orman motoru — Main.dc.html içinden üretilir, elle düzenleme. */\nwindow.BuyukkolEngine = class {\n' + engine + '\n};\n')
out = root / 'docs' / 'index.html'
out.parent.mkdir(exist_ok=True)
out.write_text(html)
print('wrote', out, len(html), 'bytes')
