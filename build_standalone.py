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
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' shape-rendering='crispEdges'%3E%3Crect width='16' height='16' fill='%23141A30'/%3E%3Crect x='5' y='2' width='6' height='2' fill='%2369964B'/%3E%3Crect x='3' y='4' width='10' height='5' fill='%23426D3E'/%3E%3Crect x='4' y='5' width='3' height='2' fill='%2369964B'/%3E%3Crect x='7' y='9' width='2' height='4' fill='%235A3F2A'/%3E%3Crect x='11' y='11' width='2' height='2' fill='%23F6B26B'/%3E%3C/svg%3E"

chips = ''.join(
    f'<button type="button" class="chip" data-zone="{i}" aria-pressed="false"><span aria-hidden="true" class="chip-dot"></span><span class="chip-name"></span><span class="seen" aria-label="keşfedildi" hidden>✓</span></button>'
    for i in range(1, PROJECTS + 1))

html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#141A30">
<title>Ali Emre Büyükkol — Portföy ormanı</title>
<meta name="description" content="Ali Emre Büyükkol'un portföyü: piksel bir ormanda yürü; Cozy Camp, Muchineko, Pati Kulaç ve Suçüstü projelerini keşfet.">
<meta property="og:title" content="Büyükkol — Portföy ormanı">
<meta property="og:description" content="Fenerini al, ormanda yürü. Her köşede başka bir proje, başka bir hava var.">
<meta property="og:type" content="website">
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
<p style="margin:0;font-family:'Pixelify Sans',monospace;font-size:15px;letter-spacing:.14em;color:#F6B26B">BİR PORTFÖY ORMANI</p>
<h1>BÜYÜKKOL</h1>
<p style="margin:0;max-width:34ch;font-size:clamp(16px,1.6vw,19px);line-height:1.5;color:#E4DDEC">Fenerini al, ormanda yürü. Her köşede başka bir proje, başka bir hava var.</p>
<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center">
<button type="button" class="intro-btn intro-p" id="enter-sound">Sesle gir</button>
<button type="button" class="intro-btn intro-g" id="enter-quiet">Sessiz gir</button>
</div>
<p style="margin:0;font-family:'Pixelify Sans',monospace;font-size:13px;letter-spacing:.08em;color:#B9B3CC"><span class="keys">← → İLE YÜRÜ · DOKUN, ORAYA GİT · 1–4 İLE PROJEYE ATLA</span><span class="touch">DOKUN, ORAYA GİT · KAYDIR, SONRAKİ PROJE</span></p>
<noscript><p style="color:#FFD28A">Orman JavaScript ile çalışıyor. Lütfen JavaScript'i aç.</p></noscript>
</section>

<div id="hud" hidden>
<header class="top">
<div style="display:flex;flex-direction:column">
<a href="#" class="logo" id="logo">BÜYÜKKOL</a>
<span class="tagline" style="font-size:14px;color:#D9D2E6;text-shadow:0 1px 0 rgba(14,16,30,.8)">Ormanda dolaş, her köşede başka bir proje var.</span>
</div>
<div style="display:flex;gap:8px">
<button type="button" class="hud-btn" id="snd" aria-pressed="false" aria-label="Ambiyansı aç"><span id="snd-on" hidden>{ICON_ON}</span><span id="snd-off" style="display:inline-flex">{ICON_OFF}</span><span class="lbl" id="snd-lbl">Ambiyansı aç</span></button>
<button type="button" class="hud-btn" id="go-about" aria-label="Hakkımda"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><circle cx="9" cy="6" r="3" stroke="currentColor" stroke-width="1.6"/><path d="M3 15.5c.8-3 3.2-4.5 6-4.5s5.2 1.5 6 4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><span class="lbl">Hakkımda</span></button>
<button type="button" class="hud-btn" id="go-contact" aria-label="İletişim"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true"><rect x="2" y="4" width="14" height="10" rx="1" stroke="currentColor" stroke-width="1.6"/><path d="m2.5 5 6.5 5 6.5-5" stroke="currentColor" stroke-width="1.6"/></svg><span class="lbl">İletişim</span></button>
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
<div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap"><a href="#" class="cta" id="c-cta">Projeye git{ARROW_UP}</a><span class="cta cta-soon" id="c-soon" hidden>Yakında</span><button type="button" class="cta cta-ghost" id="c-next"><span id="c-next-lbl"></span>{ARROW_R}</button></div>
</div>
<div id="c-about" hidden style="flex-direction:column;gap:inherit">
<p class="card-desc">Uygulamalar, oyunlar ve küçük dijital dünyalar tasarlayıp geliştiriyorum. Ormanda yürü, her durakta biri seni bekliyor.</p>
<div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap"><a href="hakkimda.html" class="cta">Beni tanı</a><button type="button" class="cta" id="go-first" style="background:transparent;color:#F3ECDD;box-shadow:inset 0 0 0 1px rgba(243,236,221,.4)">İlk projeye yürü{ARROW_R}</button></div>
</div>
<div id="c-contact" hidden style="flex-direction:column;gap:inherit">
<div class="links"><a href="mailto:aliemrebuyukkol@gmail.com">aliemrebuyukkol@gmail.com</a><a href="https://github.com/aliemrebuyukkol" target="_blank" rel="noopener">GitHub</a></div>
<div style="display:flex;gap:8px;flex-wrap:wrap"><a href="mailto:aliemrebuyukkol@gmail.com" class="cta">Mektup yaz</a><button type="button" class="cta cta-ghost" id="go-home">Başa dön</button></div>
</div>
</section>

<nav class="dock" aria-label="Projeler">
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
  const loadSeen = () => {{ try {{ const v = JSON.parse(localStorage.getItem('buyukkol.seen.v2') || '[]'); return Array.isArray(v) ? v.filter((n) => Number.isInteger(n) && n >= 1 && n <= NPROJ) : []; }} catch (e) {{ return []; }} }};
  const saveSeen = (v) => {{ try {{ localStorage.setItem('buyukkol.seen.v2', JSON.stringify(v)); }} catch (e) {{ /* depolama yoksa sessizce geç */ }} }};
  const st = {{ zone: 0, sound: false, intro: true, seen: loadSeen() }};
  const $ = (id) => document.getElementById(id);
  const chipEls = Array.from(document.querySelectorAll('.chip'));
  chipEls.forEach((b) => {{
    const z = zones[+b.dataset.zone];
    b.querySelector('.chip-name').textContent = z.name;
    b.querySelector('.chip-dot').style.background = z.color;
  }});

  const render = () => {{
    const z = st.zone, p = zones[z];
    $('root').className = st.intro ? 'root is-intro' : 'root';
    $('intro').hidden = !st.intro;
    $('hud').hidden = st.intro;
    $('snd').setAttribute('aria-pressed', st.sound ? 'true' : 'false');
    const sl = st.sound ? 'Sesi kapat' : 'Ambiyansı aç';
    $('snd').setAttribute('aria-label', sl); $('snd-lbl').textContent = sl;
    $('snd-on').hidden = !st.sound; $('snd-on').style.display = st.sound ? 'inline-flex' : '';
    $('snd-off').hidden = st.sound; $('snd-off').style.display = st.sound ? '' : 'inline-flex';
    let pi = 0;
    zones.forEach((q, i) => {{ if (q.type === 'project' && i <= z) pi++; }});
    $('c-dot').style.background = p.color;
    $('c-eyebrow').textContent = p.type === 'project' ? 'PROJE ' + pi + ' / ' + NPROJ + (p.kind ? ' · ' + p.kind : '') : p.eyebrow;
    $('c-name').textContent = p.name; $('c-name').style.color = p.color;
    $('c-vibe').textContent = p.vibe;
    $('c-cta').href = p.href || '#'; $('c-cta').hidden = !p.href; $('c-soon').hidden = !!p.href;
    if (p.ext) {{ $('c-cta').target = '_blank'; $('c-cta').rel = 'noopener'; }} else {{ $('c-cta').removeAttribute('target'); $('c-cta').removeAttribute('rel'); }}
    const nz = zones[z + 1];
    $('c-next').hidden = !nz; $('c-next-lbl').textContent = nz ? 'Sonraki: ' + (nz.type === 'contact' ? 'İletişim' : nz.name) : '';
    const d = $('c-desc'); d.textContent = '';
    if (p.desc) d.textContent = p.desc;
    else {{ const ph = document.createElement('span'); ph.className = 'ph'; ph.textContent = '[Tek cümlelik proje açıklaması]'; d.appendChild(ph); }}
    [['c-project', 'project'], ['c-about', 'about'], ['c-contact', 'contact']].forEach(([id, type]) => {{
      const on = p.type === type; $(id).hidden = !on; $(id).style.display = on ? 'flex' : '';
    }});
    chipEls.forEach((b) => {{
      const i = +b.dataset.zone, on = i === z;
      b.className = 'chip' + (on ? ' on' : '');
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.querySelector('.seen').hidden = st.seen.indexOf(i) < 0;
    }});
    const found = st.seen.length;
    $('hint').textContent = (found === NPROJ ? 'HEPSİNİ BULDUN! ' : 'KEŞİF ' + found + '/' + NPROJ + ' · ') + '← → İLE YÜRÜ';
    $('bubble').textContent = p.say;
  }};

  const eng = new Engine();
  const game = eng.buildGame($('scene'), {{
    onZone: (i) => {{
      if (i === st.zone) return;
      const fresh = zones[i].type === 'project' && st.seen.indexOf(i) < 0;
      if (fresh && !st.intro && navigator.vibrate && (!navigator.userActivation || navigator.userActivation.hasBeenActive)) {{ try {{ navigator.vibrate(12); }} catch (e) {{ /* desteklenmiyor */ }} }}
      st.zone = i;
      if (fresh) {{ st.seen = st.seen.concat([i]); saveSeen(st.seen); if (st.seen.length === NPROJ) game.celebrate(); }}
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
  cv.addEventListener('keydown', (e) => {{
    if (st.intro) return;
    if (isL(e.key)) {{ game.hold(-1); e.preventDefault(); }}
    else if (isR(e.key)) {{ game.hold(1); e.preventDefault(); }}
    else if (e.key >= '1' && e.key <= String(NPROJ)) go(+e.key);
  }});
  cv.addEventListener('keyup', (e) => {{ if (isL(e.key) || isR(e.key)) game.hold(0); }});
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
