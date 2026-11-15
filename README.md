# Büyükkol — Portföy ormanı

Ali Emre Büyükkol'un portföy sitesi. Ziyaretçi, piksel sanat bir ormanda fenerli bir gezginle yürüyor; her köşede başka bir proje, başka bir ambiyans var.

| Durak | Ne var |
| --- | --- |
| Kulübe | Hakkımda |
| Cozy Camp | Kamp ateşi, keşiş, tilki, tavşan, baykuş, gökte süzülen ada |
| Suçüstü | Dans pisti: dansçılar çöp atıyor, sonra dans ederek süpürüyor |
| Hoşgeldiniz Efendim | Çay ocağı: semaver, tepsiyle dolaşan çaycı, eski televizyon (canlı siteye gider) |
| Pati Kulaç | Gölette kulaç atan kediler, cankurtaran kedi |
| Muchineko | Çiçekli ağacın altında kediler |
| Posta kutusu | İletişim |

## Klasörler

```
docs/                  Yayınlanan site (GitHub Pages bu klasörden yayınlayabilir)
  index.html           Orman (ana sayfa)
  hakkimda.html        Hakkımda
  cozycamp.html        Cozy Camp proje sayfası
  sucustu.html         SUÇÜSTÜ! proje sayfası (3D sürüm)
  hosgeldiniz.html     Hoşgeldiniz Efendim proje sayfası
  muchineko.html       Muchineko proje sayfası
  media/               Cozy Camp tanıtım videosu
  404.html             Kayıp patika sayfası (GitHub Pages kendiliğinden kullanır)
  sitemap.xml, robots.txt  Arama motorları için
  img/                 Proje ekran görüntüleri (webp)
  engine.js            Orman motoru (üretilir, elle düzenleme)
  site.css             Alt sayfaların ortak stili
tasarim/               Claude Design tuvalindeki kaynak dosyalar
  Main.dc.html         Ormanın tek kaynağı: motor, sahne, arayüz
  Taslak-v1.dc.html    İlk klasik portföy taslağı
  canvas.json          Tuval düzeni
build_standalone.py    tasarim/Main.dc.html -> docs/index.html + docs/engine.js
```

## Ormanı değiştirmek

Motor ve sahne `tasarim/Main.dc.html` içinde. Değişiklikten sonra siteyi yeniden üret:

```sh
python3 build_standalone.py
```

`docs/hakkimda.html`, `docs/cozycamp.html`, `docs/sucustu.html`, `docs/hosgeldiniz.html`, `docs/muchineko.html` ve `docs/site.css` elle yazılmış sayfalar; doğrudan düzenlenir.

## Yerelde açmak

Herhangi bir statik sunucu yeterli:

```sh
cd docs && python3 -m http.server 8000
# http://localhost:8000
```

## buyukkol.com'da yayınlamak (GitHub Pages)

1. Depo ayarları > Pages > Source: `main` dalı, `/docs` klasörü.
2. Alan adı alındığında: Pages > Custom domain alanına `buyukkol.com` yaz (GitHub `docs/CNAME` dosyasını kendisi ekler).
3. Alan adı sağlayıcısında GitHub Pages'in DNS kayıtlarını tanımla ve "Enforce HTTPS"i aç.

## Alan adına geçerken

Paylaşım kartları (`og:image`), `canonical` bağlantıları, `sitemap.xml` ve `robots.txt` şimdilik `https://aliemrebuyukkol.github.io/portfoy/` adresini gösteriyor. buyukkol.com bağlandığında bu adresi tek seferde değiştir:

```
grep -rl "aliemrebuyukkol.github.io/portfoy" docs build_standalone.py | xargs sed -i '' 's#https://aliemrebuyukkol.github.io/portfoy/#https://buyukkol.com/#g'
python3 build_standalone.py
```

`robots.txt` yalnız alan adının kökünde çalışır; github.io alt yolunda etkisizdir, buyukkol.com'da devreye girer. Paylaşım kartı görselleri `docs/img/og-*.jpg`; ormanın kendi sahnelerinden üretildi.

## Henüz eksik olanlar

Sitede yer tutucu kalmadı. Açık işler:

- Pati Kulaç proje sayfası (oyun erken prototip aşamasında, sanatı henüz taslak; kartta "Yakında" yazıyor)
- Suçüstü App Store'da yayımlanınca sayfadaki TestFlight notunun yerine mağaza bağlantısı
- Suçüstü 3D için kısa oynanış videosu (projede henüz kayıt yok)
- Muchineko App Store'a çıkınca gizlilik ve destek bağlantıları
- İstenirse proje sayfalarına kişisel "neden yaptım" notları

## Notlar

- Sesler kayıt değil; tarayıcıda Web Audio ile üretilir ve kullanıcı açmadan çalmaz.
- Keşif ilerlemesi yalnızca ziyaretçinin tarayıcısında (`localStorage`) tutulur.
- `prefers-reduced-motion` açıksa rüzgâr ve yaprak efektleri kapanır.
- Ağaçlardaki rüzgâr tekniği SpriteCook'un piksel ağaçlarda rüzgâr eğitiminden uyarlanmıştır.
