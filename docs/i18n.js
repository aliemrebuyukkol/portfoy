"use strict";
(function () {
  const loadLang = () => {
    try {
      const q = new URLSearchParams(location.search).get('lang');
      if (q === 'en' || q === 'tr') { localStorage.setItem('buyukkol.lang', q); return q; }
      const s = localStorage.getItem('buyukkol.lang');
      if (s === 'en' || s === 'tr') return s;
    } catch (e) {}
    return (navigator.language || '').toLowerCase().indexOf('tr') === 0 ? 'tr' : 'en';
  };
  const saveLang = (l) => { try { localStorage.setItem('buyukkol.lang', l); } catch (e) {} };
  let lang = loadLang(), copied = false, copyTimer = 0;

  const setText = (el, enVal) => {
    if (!el || enVal === undefined) return;
    if (el._trText === undefined) el._trText = el.textContent;
    el.textContent = lang === 'en' ? enVal : el._trText;
  };
  const setHtml = (el, enVal) => {
    if (!el || enVal === undefined) return;
    if (el._trHtml === undefined) el._trHtml = el.innerHTML;
    el.innerHTML = lang === 'en' ? enVal : el._trHtml;
  };
  const setOwnText = (el, enVal) => {
    if (!el || enVal === undefined) return;
    const tn = Array.from(el.childNodes).find((n) => n.nodeType === 3 && n.textContent.trim().length > 0);
    if (!tn) return;
    if (el._trOwnText === undefined) el._trOwnText = tn.textContent;
    tn.textContent = lang === 'en' ? enVal : el._trOwnText;
  };
  const setAttr = (el, attr, enVal) => {
    if (!el || enVal === undefined) return;
    if (!el._trAttrs) el._trAttrs = {};
    if (el._trAttrs[attr] === undefined) el._trAttrs[attr] = el.getAttribute(attr);
    const val = lang === 'en' ? enVal : el._trAttrs[attr];
    if (val === null) el.removeAttribute(attr);
    else el.setAttribute(attr, val);
  };
  const setList = (sel, arr, mode) => {
    if (!arr) return;
    const els = document.querySelectorAll(sel);
    arr.forEach((val, i) => {
      if (!els[i] || val === undefined) return;
      if (mode === 'html') setHtml(els[i], val);
      else if (mode === 'own') setOwnText(els[i], val);
      else setText(els[i], val);
    });
  };
  const setAttrs = (sel, attr, arr) => {
    if (!arr) return;
    const els = document.querySelectorAll(sel);
    arr.forEach((val, i) => { if (els[i] && val !== undefined) setAttr(els[i], attr, val); });
  };

  const PAGES = {
    hakkimda: {
      title: 'About — Ali Emre Büyükkol',
      desc: 'Ali Emre Büyükkol: an amateur vibecoder building apps, games, and tiny digital worlds so they feel warm and a bit different.',
      text: {
        '.hero .eyebrow': 'ABOUT',
        '#baslik': "Hi, I'm Ali Emre Büyükkol.",
        '#isler': 'Projects',
        '#araclar': 'What I use',
        '#iletisim': 'Got an idea?'
      },
      html: {
        '.hero .lead': "I build apps, games, and tiny digital worlds. I'm not a professional software engineer—I call myself a <b>vibecoder</b>. I bring the idea and the feel, and we write the code together with AI."
      },
      lists: {
        '.hero .muted': [
          "I'm an amateur, and I don't take myself too seriously. I just like making things that look cozy and slightly different: a campfire, lazy cats, miniature islands, quiet things hiding small surprises in their corners.",
          'And we love everyone. Whoever you are, welcome to the woods.'
        ],
        'main > .section .eyebrow': ['01 · IN THE WOODS', '02 · TOOLS', '03 · CONTACT'],
        '.work-meta': [
          'A journal and focus app: write a few lines, spark your fire, and grow your camp.',
          'A landscape iPhone game where your cat runs across rooftops drawn in ink and cream paper: 10 maps, 21 cats. SwiftUI, SpriteKit.',
          'Spot litter, spray & horn culprits! 236 levels across toy-like 3D worlds, 12 twists, and 50 animal pals. RealityKit, SwiftUI.',
          "A living web world placing Turkey's cult viral videos onto isometric miniature islands. React, PixiJS.",
          'A sports-broadcast-style cat swimming race that turns finger rhythm into paw strokes. SwiftUI, RealityKit.'
        ],
        '#araclar + .chips .chip': ['Swift & SwiftUI', 'SpriteKit', 'SceneKit', 'RealityKit', 'React', 'PixiJS', 'React Native & Expo', 'Firebase', 'Supabase', 'Blender', 'Claude Code'],
        '#iletisim + .stack .muted': ['Feel free to write about a project, a collaboration, or just to say hello.'],
        '#iletisim .row a.btn': ['Write an email', 'Walk the woods']
      },
      attrs: {
        'section.section[aria-labelledby="isler"] .list': ['aria-label', 'Projects']
      }
    },
    cozycamp: {
      title: 'Cozy Camp: Journal & Focus — Ali Emre Büyükkol',
      desc: 'Cozy Camp: a journal, a focus timer, and a tiny floating camp. Write a few lines and spark your fire. On the App Store for iPhone.',
      soundOff: 'Hear the fire',
      text: {
        '.stage .hint': 'TAP THE FIRE',
        '.intro .eyebrow': 'APP · ON THE APP STORE',
        '.intro .sub': 'Write, focus, grow your camp.',
        '.intro .lead': 'Write a few lines and spark your fire. Cozy Camp brings together a journal, a focus timer, and a tiny camp floating in the sky. Every day you write, your flame glows brighter, a memory joins your island, and animal friends visit your camp.',
        '#store-meta': 'iPhone · iOS 17+ · Free',
        '#dl-title': 'Light your campfire tonight',
        '#dl-desc': 'Download free—no sign-up needed. Everything you write stays privately on your iPhone.',
        '#neler': 'A corner of your own',
        '#kampplus': 'Free forever, optional extras',
        '#ekranlar': 'From the app',
        '#hikaye': 'How was it built?',
        '#destek': 'Help & privacy',
        '.film figcaption': '23-second preview. Use the video controls for audio.'
      },
      lists: {
        '.store small': ['Download free on the', 'Download free on the'],
        '.facts .chip': ['iPhone · iOS 17+', '33 languages incl. Turkish & English', 'Free · in-app purchases', '9+'],
        'main > .section .eyebrow': ['01 · AROUND THE CAMP', '02 · CAMP+', '03 · SCREENS', '04 · BUILD NOTES', '05 · SUPPORT'],
        '.feat .card h3': ['JOURNAL', 'AURA', 'FRIENDS', 'ISLANDS', 'BREAK', 'WOOD & FIRES', 'WIDGETS'],
        '.feat .card p': [
          "Even a single sentence counts. Guided prompts help when you get stuck; everything you write stays strictly on your phone.",
          'Pick up to three feelings and watch your campfire take on their colors. A weekly color map builds effortlessly over time.',
          'Fox, rabbit, owl… Greet the animal friends visiting your camp, play together, and leave food out for them.',
          'Each island has its own shape, plants, wildlife, and ambient sound. Seven writing days complete an island and reveal the next.',
          'A focus timer powered by nature sounds and breathing cues. Every 5 minutes of focus earns you firewood.',
          'Gather wood by writing, focusing, and finishing tasks; unlock new campfires and decorate your camp.',
          'Pin your camp and fire to your Home Screen to check in at a glance without opening the app.'
        ],
        'section[aria-labelledby="kampplus"] .muted': ['The free version includes one journal entry per day; optional short rewarded ads raise that to up to three per day. Camp+ is an optional subscription:'],
        '.checks li': ['Unlimited entries', '50% more firewood', 'Choose from 20 islands', 'Special fires and decorations', 'Deeper aura experience', 'Ad-free experience'],
        '.plans .plan span': ['Weekly', 'Monthly', 'Yearly'],
        'section[aria-labelledby="kampplus"] .note': ['Prices are taken from the Turkey App Store listing and may vary. Subscriptions renew automatically unless canceled at least 24 hours before period end via Apple Account settings.'],
        '.shot figcaption': ['Your camp', 'Companions', 'Break by the lighthouse', 'Archipelago', 'Island postcard', 'Widgets'],
        'section[aria-labelledby="ekranlar"] .note': ['Screenshots and video are from version 1.2 "Camp Life".'],
        'section[aria-labelledby="hikaye"] .muted': ["Built entirely with Apple's native frameworks. The camp world renders in SceneKit; trees, animals, tents, and fires are procedurally generated low-poly shapes rather than imported meshes. Journal sentiment is read on-device using NaturalLanguage, so your writing never leaves your phone. Ambient sounds are synthesized live with AVAudioEngine rather than recorded audio."],
        '.build .stat span': ['3D camp world', 'UI, plus WidgetKit widgets', 'sentiment analysis'],
        '.build .stat b': ['SceneKit', 'SwiftUI', 'On-device'],
        'section[aria-labelledby="hikaye"] .note': ['Developer: Ali Emre Büyükkol.'],
        'section[aria-labelledby="destek"] .muted': ['What you write in your journal stays only on your device. Details about other collected data and ads are in the privacy policy.'],
        'section[aria-labelledby="destek"] .btn': ['Privacy policy', 'Support', 'Terms of use']
      },
      attrs: {
        '#scene': ['aria-label', 'Pixel-art campfire scene: a monk sitting cross-legged by the fire, a tent, a steaming kettle, and fireflies.'],
        '.facts': ['aria-label', 'App details'],
        '.plans': ['aria-label', 'Camp+ pricing'],
        '.shots': ['aria-label', 'Screenshots, horizontally scrollable'],
        '.film video': ['aria-label', 'Cozy Camp promo video, 23 seconds: camp, journaling, companions, islands, and break screens.']
      },
      imgAlts: [
        'Camp screen: low-poly Pine Cove island floating in the sky with lighthouse, tent, and trees; island tasks, 20-day streak, wood count, and Write Today button.',
        'Camp Life screen: Squirrel companion card, rabbit, duck, and squirrel on the island; Greet, Pet, Play buttons and wish of the day.',
        'Break screen: 25:00 timer over a tiny island with a lighthouse, Start Break button, and 10, 25, 45 minute presets.',
        'Archipelago screen: distant miniature islands in the sea with a boat cruising between them; Pine Cove card and upcoming Winter Lights festival.',
        'Postcard screen: illustrated Pine Cove postcard with stamp and date; 7 writing days, 0 focus minutes, 2 companions, and Share button.',
        'Widgets screen: small home-screen widget showing camp and day count, wide camp widget, and companion interaction widget previews.'
      ]
    },
    sucustu: {
      title: 'SUÇÜSTÜ! (CAUGHT!) — Ali Emre Büyükkol',
      desc: 'CAUGHT!: spot litter, spray & horn culprits! 236 levels in toy-like 3D worlds, a different rule in every level, pals with abilities.',
      soundOff: 'Start the beat',
      text: {
        '.stage .hint': 'TAP THE FLOOR',
        '.intro .eyebrow': 'GAME · iPHONE · 3D',
        '.intro .sub': 'Spot litter, spray & horn culprits!',
        '.intro .lead': 'Somewhere in the crowd someone sprays paint, blasts a horn, or drops litter. Paint mist drifts on the wind, the dog fetches a tossed bottle, bystanders cover their ears; the evidence moves but its owner never changes. Spot the culprit in toy-like 3D worlds and tap them, red-handed.',
        '#nasil': 'One tap, sharp eyes',
        '#twist-baslik': 'Every level has its own twist',
        '.twist-lead': 'After the tutorial, every level comes with one of these rules; you read it on the level card before you start.',
        '#dostlar': '50 animal pals, 5 abilities',
        '.pal-lead': 'Your pal walks the patrol with you and lends you its ability. 1–3 charges per patrol by rarity; the higher your bond level, the stronger the ability and the more charges.',
        '#bolgeler': 'From the Neighborhood to the League of Legends',
        '#ekranlar': 'Trailer and screens',
        '#yapim': 'How was it built?',
        '#destek': 'Help & privacy',
        '.film figcaption': 'A 25-second trailer with the game’s own music.'
      },
      html: {
        '.status p': '<b>Version 1.2 is in TestFlight.</b> Not on the App Store yet—the download link will appear here once released.'
      },
      lists: {
        '.facts .chip': ['236 levels · 10 worlds', '12 different level twists', '50 animal pals', 'Plays offline'],
        'main > .section .eyebrow': ['01 · HOW TO PLAY', '02 · LEVEL TWISTS', '03 · PALS', '04 · WORLDS', '05 · SCREENS', '06 · BUILD NOTES', '07 · SUPPORT'],
        '.feat .card h3': ['TAP THE CULPRIT', 'EVERY LEVEL HAS A TWIST', 'PALS WITH ABILITIES', 'IT GETS HARDER', 'ONE MORE CHANCE', 'REAL SOUNDS'],
        '.feat .card p': [
          'Whoever left the paint mist, blasted the horn, or dropped the bottle. Tapping an innocent costs points; your decision time is on every level card.',
          'Noise drowns out horns and spray, a guard scans the area, twins act quietly. 12 different rules; neighbouring levels never play the same.',
          'Every animal pal has an ability: it tracks clues, slows time, shields you. The more you catch together, the stronger your bond.',
          'Fields grow, crowds swell, decision time shrinks. Rookie, Normal, Hard and Legend each keep their own stars.',
          'A second chance when five culprits escape, and if that fails, resume from the phase you reached. Daily patrol and endless waves every day.',
          'Six synthesized variations each for spray and horn effects, plus a cheerful brass band. All made in code, nothing recorded.'
        ],
        '.v12-twists .twist-card h3': ['Noise Curtain', 'Paint Trail', 'Fake Wind-up', 'Innocent Dog', 'Blind Spot', 'Closed Box', 'Crossing Crowds', 'Swap Places', 'Evidence First', 'Twins', 'Bumpy Ride', 'Wind Tracking'],
        '.v12-twists .twist-card p': [
          'Noise drowns out horns and spray. Watch the sound rings and paint mist.',
          'The culprit sprays paint and keeps walking. Catch whoever started the paint trail.',
          'Some fake a throw and back out. Don’t tap until something leaves their hand.',
          'The dog always barks at the wrong person. Look at the source of the clue, not the dog.',
          'The guard scans the area. Culprits always strike where they aren’t looking.',
          'Paint mist builds up inside. When the doors open, everyone swaps places.',
          'Two crowds pass through each other. Don’t lose the culprit in the crowd.',
          'The culprit slips away and an innocent steps in. Don’t trust who’s beside the clue.',
          'The culprit gives no warning. Spot the evidence first, then find the owner.',
          'Identical outfits and quiet clues. Keep your eyes peeled.',
          'With every bump everyone stumbles, and someone covers their ears for nothing.',
          'Strong wind carries the paint mist. Look against the wind to find the source.'
        ],
        '.pal-grid .twist-card h3': ['Track Clue', 'Slow Motion', 'Shield', 'Spotter', 'Token Magnet'],
        '.pal-grid .twist-card p': [
          'Dogs track the clue trail and point at the culprit briefly.',
          'Cats slow the world down for a few seconds.',
          'Big pals forgive one escaped culprit.',
          'Birds put an exclamation mark over offenders for a while.',
          'Rodents add extra tokens to your next catches.'
        ],
        'section[aria-labelledby="bolgeler"] .note': ['70 regions, 206 main levels and 30 special levels. Rain, snow, fog and night patrols; a black-hatted wanted ringleader in region finales.'],
        '.shot figcaption': ['Catch the culprit red-handed', 'Every level has a twist', 'Level card', '236 levels, 10 worlds', 'Night patrol', '50 animal pals'],
        'section[aria-labelledby="yapim"] .muted': ['It started as a top-down 2D sea game in SpriteKit, then moved to 3D with RealityKit: people, litter, and balls move with real physics, while drifting paint mist and sonic wave fields are simulated in world space. Dogs follow trails, cats flee dogs, pigeons take flight on sound. Audio effects are synthesized rather than recorded—each effect has six variants and never repeats back-to-back.'],
        '.build .stat b': ['RealityKit', 'SwiftUI', 'On-device'],
        '.build .stat span': ['3D scene & physics', 'menus & UI', 'progression & profiling'],
        'section[aria-labelledby="yapim"] .note': ['Developer: Ali Emre Büyükkol.'],
        'section[aria-labelledby="destek"] .muted': ['No login required; progression and settings stay on your device. Uses Unity Ads and Yandex Ads after the first three levels, with in-app privacy choices before ads start; no App Tracking Transparency requested. A one-time "Remove Ads" purchase disables ads permanently.'],
        'section[aria-labelledby="destek"] .btn': ['Privacy policy', 'Support', 'Terms of use']
      },
      ownLists: {
        '.bays li': ['Neighborhood', 'City Tour', 'Festival Season', 'Faraway Lands', 'Storm and Night', 'Animal Chaos', 'Four Seasons', 'The Big Crowd', 'Space and Beyond', 'League of Legends']
      },
      attrs: {
        '#scene': ['aria-label', 'Pixel-art dance floor: dancers drop litter, one catches someone red-handed, then they sweep up while dancing.'],
        '.facts': ['aria-label', 'Game details'],
        '.shots': ['aria-label', 'Screenshots, horizontally scrollable'],
        '.film video': ['aria-label', 'CAUGHT! trailer: spotting litter, paint spray and horn culprits, the guard’s blind spot, the night market and a level card.']
      },
      imgAlts: [
        'Basketball court level: the Noise Curtain is on, a crowd, and the pal button in the corner.',
        'Crowded beach: the guard’s orange gaze cone sweeping the field.',
        'Level card: Picnic, “This level’s twist: Wind Tracking” and examples of who to catch.',
        'Map: regions, levels and stars.',
        'Night market: a crowd on a wooden pier and a CAUGHT! stamp.',
        'Collection: portraits of premium animal pals.'
      ]
    },
    hosgeldiniz: {
      title: 'Hoşgeldiniz Efendim — Ali Emre Büyükkol',
      desc: "Hoşgeldiniz Efendim: a living web archipelago placing Turkey's cult viral videos onto isometric miniature islands, growing with each video.",
      soundOff: 'Hear the tea house',
      text: {
        '.stage .hint': 'TAP THE TV',
        '.intro .eyebrow': 'WEB · LIVING WORLD',
        '.intro .sub': 'An isometric archipelago of cult videos',
        '.intro .lead': "Turkey's iconic viral videos don't live in a playlist—they live on miniature islands. Each island is a video's world: frogs croak in the creek, market awnings sway, a samovar steams by the mountain hut. Tap an island to open its video.",
        '#takimada': 'A map instead of a video list',
        '#dioramalar': 'Each island is its own little world',
        '#yapim': 'How was it built?',
        '.hero-img figcaption': 'An early look at the archipelago. Today there are 24 islands on the map.'
      },
      html: {
        '.status p': '<b>Live now.</b> Explorable in desktop and mobile browsers—no install needed.'
      },
      ownText: {
        '.cta-row .btn': 'Visit the world'
      },
      lists: {
        '.facts .chip': ['24 islands', 'Desktop & mobile', 'Reduced motion support', 'Runs in browser'],
        'main > .section .eyebrow': ['01 · ARCHIPELAGO', '02 · DIORAMAS', '03 · BUILD NOTES'],
        '.steps li span': [
          '<b>Drag and zoom.</b> Pan with mouse or use two fingers on touch screens.',
          '<b>Tap an island.</b> Its video opens in a single player; closing it stops audio right away.',
          '<b>Open the island file.</b> Iconic quote, "why is it here?" note, and tags live in one place.',
          '<b>Take a guided tour.</b> Browse curated collections like First Steps, Night Classics, Music, and Square.'
        ],
        'section[aria-labelledby="dioramalar"] .muted': ["Islands aren't flat cards; they are miniature blocks with soil layers, overhanging grass, and cast shadows. Low-framerate micro-motions loop on top: tea steam, rippling water, blinking frog, swaying reeds."],
        '.dio figcaption': ['Creek & cabin', 'Mountain & samovar', 'Castle & market'],
        'section[aria-labelledby="yapim"] .muted': [
          'Written with React 19 and PixiJS 8. The scene runs on four layers: terrain, diorama art, micro-motion, and interaction. Whenever a new video is added, the map expands organically by scanning open neighbor slots and picking the spot touching the most existing islands—never moving older ones. Content management lives on Supabase with database-side write policies.',
          'When Reduced Motion is enabled, the engine, transitions, and ticker slow down together. Background chimes are synthesized directly in code inside the browser.'
        ],
        '.build .stat span': ['islands, one per video', 'layered scene', 'isometric projection'],
        'section[aria-labelledby="yapim"] .note': ['Videos open via embedded YouTube player and belong to their creators. Island illustrations are custom artwork made for this project rather than video screenshots. Developer: Ali Emre Büyükkol.']
      },
      attrs: {
        '#scene': ['aria-label', 'Pixel-art Turkish tea house: steaming samovar, tea server carrying a tray, two elders drinking tea, and an old TV changing channels.'],
        '.facts': ['aria-label', 'Project details'],
        '.hero-img img': ['alt', 'Six isometric islands floating in a rose-tinted sky: creek cabin, striped-awning market, autumn tea corner, night car island, and rug picnic island.'],
        'section[aria-labelledby="takimada"] ol.steps': ['aria-label', 'How to explore']
      },
      imgAlts: [
        'Six isometric islands floating in a rose-tinted sky: creek cabin, striped-awning market, autumn tea corner, night car island, and rug picnic island.',
        'Wooden red-roofed cabin beside a creek with tall trees and water flowing through rocks.',
        'Pine forest at the foot of a snowy mountain, cave mouth, and a capped elder sitting beside a steaming samovar.',
        'Tents, fruit crates, and a striped-awning market stall in front of a red-towered stone castle.'
      ]
    },
    patikulac: {
      title: 'Pati Kulaç — Ali Emre Büyükkol',
      desc: 'Pati Kulaç: a 3D cat swimming race powered by a 120 Hz physics engine that turns finger rhythm into paw strokes. In development for iPhone with SwiftUI & RealityKit.',
      soundOff: 'Hear the pond',
      text: {
        '.stage .hint': 'TAP THE POND',
        '.intro .eyebrow': 'GAME · iPHONE · 3D',
        '.intro .sub': 'A cat swimming race turning finger rhythm into paw strokes',
        '.intro .lead': 'Catch the water alternately with two fingers, keep the beat, and glide between strokes to recover stamina. Physics-driven cats racing across four lanes in a brisk 25-meter 3D pool sprint.',
        '#nasil': 'Catch the water, hold the beat, glide',
        '#havuz': 'Four lanes, real split times',
        '#ekranlar': 'Early prototype & concept frames',
        '#yapim': 'How was it built?',
        '.hero-img figcaption': "Character turnaround sheet and four-lane pool concept art for Çakıl, the first swimmer cat."
      },
      html: {
        '.status p': "<b>Early prototype, currently on internal TestFlight.</b> The physics core, four-lane race, and first cat rig are running; cat models, facial expressions, and new courses are still under construction. The frames below come directly from the early prototype build and Çakıl's character design sheet."
      },
      lists: {
        '.facts .chip': ['iPhone · iOS 18+', '25 m · 4 lanes', '120 Hz physics', 'Playable offline'],
        'main > .section .eyebrow': ['01 · HOW TO PLAY', '02 · IN THE POOL', '03 · SCREENS & CONCEPT', '04 · BUILD NOTES'],
        '.rule div b': ['PULL & RHYTHM', 'GLIDE & ENERGY', 'FOUR-STEP PRACTICE'],
        '.rule div p': [
          'Pull down alternately across the bottom zones, or tap as the rhythm ring fills. Tapping too early or forcing the same paw adds no extra speed.',
          'Each stroke produces thrust spread over time. Leaving a brief gap between strokes lets your cat glide smoothly and recover energy.',
          'An optional pool tutorial teaching your first stroke, alternating paws, rhythm cadence, and gliding to recover energy.'
        ],
        '.feat .card h3': ['REAR DIAGONAL CAMERA', 'PHYSICS-DRIVEN RIVALS', 'STANDS & AUDIO', 'ATOMIC SAVES'],
        '.feat .card p': [
          'A broadcast-style race camera keeping your swimmer and side lanes framed together from countdown to wall finish.',
          'The three cats beside you do not play canned animations—they run on the exact same water physics across five swim profiles.',
          'Dog and rabbit spectators reacting to race events from the stands, paired with water and stroke audio tied directly to engine events.',
          'Your last 20 swims, personal bests split by control mode, and early career goals are preserved safely on-device.'
        ],
        '.shot figcaption': ['Prototype home screen', '25 m race camera', 'Rhythm & stroke practice'],
        'section[aria-labelledby="yapim"] .muted': ['Written with SwiftUI and RealityKit. Swimming physics run inside a display-independent CatSwimCore package at a fixed 120 Hz step: buoyancy, water drag, time-distributed paw impulse, and fatigue come from a single physics source. First swimmer Çakıl swims with a 30-bone USDZ rig built in Blender, paired with Metal-based water and splash effects where paws hit the surface.'],
        '.build .stat span': ['fixed physics step, CatSwimCore', 'USDZ rig and Metal water', 'internal TestFlight prototype'],
        'section[aria-labelledby="yapim"] .note': ['Developer: Ali Emre Büyükkol.']
      },
      attrs: {
        '#scene': ['aria-label', 'Pixel-art pond scene: three cats swimming laps, a lifeguard cat blowing a whistle on a high chair, a cat waiting on the dock, and swaying reeds.'],
        '.facts': ['aria-label', 'Game details'],
        '.shots': ['aria-label', 'Prototype screenshots, horizontally scrollable']
      },
      imgAlts: [
        'Front, side, and back character turnaround sheet for tabby cat Çakıl, plus concept art swimming inside a yellow-and-white laned pool.',
        'Pati Kulaç early prototype home screen: 3D cat draft in pool, Çakıl card, 25 m distance, control mode picker, and Swim button.',
        'Pati Kulaç race screen: four 3D cat rigs swimming in four lanes, dog and rabbit spectators in the stands, and rhythm tap zone below.',
        'Pati Kulaç first swim practice: step card teaching stroke rhythm as the ring fills alongside an energy gauge.'
      ]
    },
    muchineko: {
      title: 'Muchineko — Ali Emre Büyükkol',
      desc: 'Muchineko: a landscape iPhone runner across rooftops of cream paper and ink. How full your cat is decides how it jumps.',
      soundOff: 'Enable sound',
      text: {
        '.stage .hint': 'TAP THE CATS',
        '.intro .eyebrow': 'GAME · iPHONE · LANDSCAPE',
        '.intro .sub': 'むちねこ · A little rooftop adventure',
        '.intro .lead': 'Across rooftops sketched in cream paper and ink, your cat runs on its own—you just time the jump. The catch is how full you are: the kibble you eat shifts your arc, so you read the route accordingly.',
        '#nasil': 'Tap, jump, balance your appetite',
        '#haritalar': 'Every series has its own rule',
        '#kediler': 'Twenty-one cats, each jumps its own way',
        '#ekranlar': 'From the game',
        '#yapim': 'How was it built?',
        'section[aria-labelledby="haritalar"] > .muted': 'Sixteen neighbourhood routes plus ten series: wind, steam, wet roofs, slipping past the lights, landing on the market drum\'s beat. A new Route of the Day opens every day.'
      },
      html: {
        '.status p': '<b>Coming soon to the App Store.</b> Version 1.0 is getting ready for release. Free to download; the link will appear here once it is live.'
      },
      lists: {
        '.facts .chip': ['iPhone · iOS 18+', 'Landscape mode', '10 maps · 81 routes', '21 cats', '11 languages', 'Playable offline'],
        'main > .section .eyebrow': ['01 · HOW TO PLAY', '02 · TEN MAPS', '03 · CATS & WIDGET', '04 · SCREENS', '05 · BUILD NOTES'],
        'section[aria-labelledby="nasil"] .muted': [
          'Tap short for a short hop; hold to go higher. Kibble increases fullness while catnip lowers it. The fullness gauge tells you which routes are open:',
          'A fall never costs the whole route: you carry on from the last roof you reached. At the end of a route you greet your cat, deepen your bond, and add a lasting detail to your rooftop.'
        ],
        '.rule div b': ['UNDER 40 · LIGHT', '40–70 · FIT', 'OVER 70 · CHUBBY'],
        '.rule div p': [
          'Land safely on clotheslines—only a light cat will be carried across.',
          'Strongest jump. The tallest roofs are reachable in this sweet spot.',
          'Drop onto shop awnings to bounce straight up to high sky paths.'
        ],
        '.feat h3': ['BOND & MEMORIES', 'HOME SCREEN WIDGET', 'FOR EVERYONE'],
        '.feat .muted': [
          'You start with Mochi and tabby Sumi. The more routes you run together, the more your bond grows and new cats and memories open.',
          'Pick your cat and serve its favourite food from the home screen at breakfast, lunch and dinner to grow your feeding streak.',
          'No internet or account needed. Relaxed jumps, large text and Reduce Motion support.'
        ],
        '.shot figcaption': ['Home screen', 'Running in Quiet Rooftops', "The Moon's Back Alley", 'Special map: Night Market', 'Twenty-one cats', 'Daily feeding widget'],
        'section[aria-labelledby="yapim"] .muted': ['A landscape iPhone game written in SwiftUI and SpriteKit, drawn entirely in a cream-paper-and-ink style. It plays offline, with progress written first to a local save on the device. The free version shows ads; the one-time Ad-Free, Whole City and Premium Cats packs and the yearly Cat Club subscription are optional.'],
        '.build .stat span': ['maps, 81 routes', 'cats, each jumps its own way', 'languages', 'first App Store release'],
        'section[aria-labelledby="yapim"] .note': ['Developer: Ali Emre Büyükkol.']
      },
      ownLists: {
        '.bays li': ['Awning Postal Cats', "The Moon's Back Alley", 'Steamy Courtyard', 'Wind Mapmakers', 'Storeroom of Lost Sounds', 'Greenhouse Knot', 'After the Rain', 'Lantern Parade', 'Misty Shore', 'Night Market · special map']
      },
      attrs: {
        '#scene': ['aria-label', 'Pixel-art forest: cats napping and chasing butterflies beneath a blooming tree.'],
        '.facts': ['aria-label', 'Game details'],
        '.shots': ['aria-label', 'Screenshots, horizontally scrollable']
      },
      imgAlts: [
        'Muchineko home screen: "One more bite." heading, Hit the Roofs button, Missions, Routes, Cats, Collection and Today cards, and black-and-white cat Mochi lying on a roof.',
        'Gameplay: a cat leaping across ink-drawn rooftops with the fullness gauge and kibble floating ahead.',
        "A route from The Moon's Back Alley series: night rooftops and lights.",
        'Special map Night Market: a cat running between stall lights.',
        'Cats screen: cat cards in different colours and patterns.',
        'Home screen widget: Mochi, breakfast, lunch and dinner meals, Dry, Wet and Fish food buttons, and a Pet button.'
      ]
    },
    '404': {
      title: 'Path not found — Büyükkol',
      text: {
        '.code': '404 · PATH NOT FOUND',
        '.lost h1': "This trail isn't in the woods.",
        '.lost .muted': "Maybe the trees shifted, or the address had a typo. Grab your lantern and let's head back to the cabin."
      },
      lists: {
        '.go a': ['Back to cabin', 'About']
      },
      attrs: {
        '#scene': ['aria-label', 'Nighttime pixel-art forest: a traveler carrying a lantern in front of a cabin.']
      }
    }
  };

  const getPageKey = () => {
    if (document.querySelector('.lost')) return '404';
    const seg = (location.pathname.split('/').pop() || '').replace(/\.html$/, '');
    if (PAGES[seg]) return seg;
    const h = document.getElementById('baslik');
    if (!h) return 'hakkimda';
    const t = h.textContent;
    if (t.indexOf('Cozy') >= 0) return 'cozycamp';
    if (t.indexOf('SUÇÜSTÜ') >= 0) return 'sucustu';
    if (t.indexOf('Hoşgeldiniz') >= 0) return 'hosgeldiniz';
    if (t.indexOf('Pati') >= 0) return 'patikulac';
    if (t.indexOf('Muchineko') >= 0) return 'muchineko';
    return 'hakkimda';
  };

  const COMMON_PN_K = {
    'Önceki proje': 'Previous project',
    'Sonraki proje': 'Next project',
    'Başa dön': 'Back to start',
    'Son durak': 'Final stop'
  };
  const COMMON_PN_N = {
    'Hakkımda': 'About',
    'Posta kutusu': 'Mailbox'
  };

  const ensureButtons = () => {
    let btn = document.getElementById('lang-btn');
    if (!btn) {
      btn = document.createElement('button');
      btn.type = 'button';
      btn.id = 'lang-btn';
      const barWrap = document.querySelector('.bar .wrap');
      if (barWrap) {
        const brand = barWrap.querySelector('.brand');
        let right = barWrap.querySelector('.bar-right');
        if (!right) {
          right = document.createElement('div');
          right.className = 'bar-right';
          barWrap.appendChild(right);
          if (brand) right.appendChild(brand);
        }
        btn.className = 'lang-btn';
        right.appendChild(btn);
      } else {
        const goBox = document.querySelector('.go');
        if (goBox) {
          btn.className = 'btn ghost';
          goBox.appendChild(btn);
        }
      }
      btn.addEventListener('click', () => {
        lang = lang === 'en' ? 'tr' : 'en';
        saveLang(lang);
        apply();
      });
    }
    return btn;
  };

  const syncSoundLabel = (cfg) => {
    const sndBtn = document.getElementById('snd');
    const sndLbl = document.getElementById('snd-lbl');
    if (!sndBtn || !sndLbl) return;
    if (sndLbl._trOff === undefined) sndLbl._trOff = sndLbl.textContent;
    const txt = sndLbl.textContent;
    const isErr = txt === 'Ses bu tarayıcıda çalışmıyor' || txt === 'Audio unavailable in this browser';
    if (isErr) {
      sndLbl.textContent = lang === 'en' ? 'Audio unavailable in this browser' : 'Ses bu tarayıcıda çalışmıyor';
      return;
    }
    const on = sndBtn.getAttribute('aria-pressed') === 'true';
    if (lang === 'en') sndLbl.textContent = on ? 'Mute sound' : (cfg.soundOff || 'Enable sound');
    else sndLbl.textContent = on ? 'Sesi kapat' : sndLbl._trOff;
  };

  const syncCopyBtn = () => {
    const btn = document.getElementById('copy-mail');
    if (!btn) return;
    if (btn._trLabel === undefined) btn._trLabel = btn.textContent;
    if (copied) btn.textContent = lang === 'en' ? 'Copied ✓' : 'Kopyalandı ✓';
    else btn.textContent = lang === 'en' ? 'Copy email' : btn._trLabel;
  };

  const apply = () => {
    const key = getPageKey();
    const cfg = PAGES[key] || PAGES.hakkimda;
    document.documentElement.lang = lang;
    if (document._trTitle === undefined) document._trTitle = document.title;
    document.title = lang === 'en' && cfg.title ? cfg.title : document._trTitle;
    const descMeta = document.querySelector('meta[name="description"]');
    if (descMeta && cfg.desc) setAttr(descMeta, 'content', cfg.desc);

    const langBtn = ensureButtons();
    if (langBtn) {
      langBtn.textContent = lang === 'en' ? 'TR' : 'EN';
      langBtn.setAttribute('aria-label', lang === 'en' ? 'Türkçeye geç' : 'Switch to English');
    }

    // Ortak navigasyon ve alt bilgi
    setOwnText(document.querySelector('.back'), 'Back to forest');
    document.querySelectorAll('.foot a').forEach((a) => {
      const hr = a.getAttribute('href') || '';
      if (hr.indexOf('index.html') >= 0) setText(a, 'Back to forest');
      else if (hr === 'hakkimda.html') setText(a, 'About');
    });
    const pnav = document.querySelector('.pnav');
    if (pnav) {
      setAttr(pnav, 'aria-label', 'Other projects');
      pnav.querySelectorAll('.pn-k').forEach((kEl) => {
        if (kEl._trOwnText === undefined) {
          const tn = Array.from(kEl.childNodes).find((n) => n.nodeType === 3 && n.textContent.trim().length > 0);
          if (tn) kEl._trOwnText = tn.textContent;
        }
        const raw = (kEl._trOwnText || '').trim();
        if (COMMON_PN_K[raw]) setOwnText(kEl, COMMON_PN_K[raw]);
      });
      pnav.querySelectorAll('.pn-n').forEach((nEl) => {
        if (nEl._trText === undefined) nEl._trText = nEl.textContent;
        if (COMMON_PN_N[nEl._trText]) setText(nEl, COMMON_PN_N[nEl._trText]);
      });
    }

    if (cfg.text) Object.entries(cfg.text).forEach(([s, v]) => setText(document.querySelector(s), v));
    if (cfg.html) Object.entries(cfg.html).forEach(([s, v]) => setHtml(document.querySelector(s), v));
    if (cfg.ownText) Object.entries(cfg.ownText).forEach(([s, v]) => setOwnText(document.querySelector(s), v));
    if (cfg.lists) Object.entries(cfg.lists).forEach(([s, v]) => setList(s, v, 'text'));
    if (cfg.ownLists) Object.entries(cfg.ownLists).forEach(([s, v]) => setList(s, v, 'own'));
    if (cfg.attrs) Object.entries(cfg.attrs).forEach(([s, pair]) => setAttr(document.querySelector(s), pair[0], pair[1]));
    if (cfg.imgAlts) setAttrs('.shot img, .dio img, .hero-img img', 'alt', cfg.imgAlts);

    syncSoundLabel(cfg);
    syncCopyBtn();
    window.dispatchEvent(new CustomEvent('buyukkol:lang', { detail: { lang } }));
  };

  const sndBtn = document.getElementById('snd');
  if (sndBtn) {
    sndBtn.addEventListener('click', () => {
      Promise.resolve().then(() => syncSoundLabel(PAGES[getPageKey()] || {}));
    });
  }

  const copyBtn = document.getElementById('copy-mail');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const email = copyBtn.dataset.copy || 'aliemrebuyukkol@gmail.com';
      const done = () => {
        copied = true;
        syncCopyBtn();
        clearTimeout(copyTimer);
        copyTimer = setTimeout(() => { copied = false; syncCopyBtn(); }, 2000);
      };
      const fallback = () => {
        try {
          const ta = document.createElement('textarea');
          ta.value = email;
          ta.setAttribute('readonly', '');
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
        } catch (e) {}
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(email).then(done).catch(() => { fallback(); done(); });
      } else {
        fallback();
        done();
      }
    });
  }

  apply();
})();
