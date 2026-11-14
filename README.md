# Büyükkol — Portföy ormanı

Ali Emre Büyükkol'un portföy sitesi. Ziyaretçi, piksel sanat bir ormanda fenerli bir gezginle yürüyor; her köşede başka bir proje, başka bir ambiyans var.

| Durak | Ne var |
| --- | --- |
| Kulübe | Hakkımda |
| Cozy Camp | Kamp ateşi, keşiş, tilki, tavşan, baykuş, gökte süzülen ada |
| Suçüstü | Dans pisti: dansçılar çöp atıyor, sonra dans ederek süpürüyor |
| Pati Kulaç | Gölette kulaç atan kediler, cankurtaran kedi |
| Muchineko | Çiçekli ağacın altında kediler |
| Posta kutusu | İletişim |

## Klasörler

```
docs/                  Yayınlanan site (GitHub Pages bu klasörden yayınlayabilir)
  index.html           Orman (ana sayfa)
  hakkimda.html        Hakkımda
  cozycamp.html        Cozy Camp proje sayfası
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

`docs/hakkimda.html`, `docs/cozycamp.html` ve `docs/site.css` elle yazılmış sayfalar; doğrudan düzenlenir.

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

## Henüz eksik olanlar

Sitede amber renkli, kesik çizgili alanlar doldurulmayı bekleyen yer tutuculardır:

- Muchineko, Suçüstü ve Pati Kulaç için açıklama ve proje sayfaları
- Cozy Camp ekran görüntüleri ve "Neden yaptım?" metni
- Gerçek e-posta adresi ve sosyal medya bağlantıları (şu an `merhaba@buyukkol.com` ve `#`)

## Notlar

- Sesler kayıt değil; tarayıcıda Web Audio ile üretilir ve kullanıcı açmadan çalmaz.
- Keşif ilerlemesi yalnızca ziyaretçinin tarayıcısında (`localStorage`) tutulur.
- `prefers-reduced-motion` açıksa rüzgâr ve yaprak efektleri kapanır.
- Ağaçlardaki rüzgâr tekniği SpriteCook'un piksel ağaçlarda rüzgâr eğitiminden uyarlanmıştır.
