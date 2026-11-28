"use strict";
// Up or Oops yasal sayfaları: Türkçe / English. Seçim sitenin geri kalanıyla aynı anahtarda saklanır.
// Sıra: ?lang= > #en / #tr bağlantısı > kayıtlı seçim > tarayıcı dili. Betik yoksa iki dil de görünür.
(function () {
  var KEY = "buyukkol.lang";
  var root = document.documentElement;
  var store = function (l) { try { localStorage.setItem(KEY, l); } catch (e) {} };
  var pick = function () {
    try {
      var q = new URLSearchParams(location.search).get("lang");
      if (q === "en" || q === "tr") { store(q); return q; }
    } catch (e) {}
    var h = location.hash.slice(1);
    if (/^en(-|$)/.test(h)) return "en";
    if (/^tr(-|$)/.test(h)) return "tr";
    try {
      var s = localStorage.getItem(KEY);
      if (s === "en" || s === "tr") return s;
    } catch (e) {}
    return (navigator.language || "").toLowerCase().indexOf("tr") === 0 ? "tr" : "en";
  };

  var trTitle = document.title;
  var desc = document.querySelector('meta[name="description"]');
  var trDesc = desc ? desc.getAttribute("content") : "";
  var swaps = Array.prototype.slice.call(document.querySelectorAll("[data-en]"));
  swaps.forEach(function (el) { el._tr = el.textContent; });

  var apply = function (lang, scroll) {
    root.lang = lang;
    document.title = lang === "en" ? root.getAttribute("data-title-en") : trTitle;
    if (desc) desc.setAttribute("content", lang === "en" ? root.getAttribute("data-desc-en") : trDesc);
    swaps.forEach(function (el) { el.textContent = lang === "en" ? el.getAttribute("data-en") : el._tr; });
    var trEl = document.getElementById("tr");
    var enEl = document.getElementById("en");
    if (trEl) trEl.hidden = lang !== "tr";
    if (enEl) enEl.hidden = lang !== "en";
    document.querySelectorAll(".seg button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === lang));
    });
    var t = document.getElementById("lang-toggle");
    if (t) {
      t.textContent = lang === "en" ? "TR" : "EN";
      t.setAttribute("aria-label", lang === "en" ? "Türkçeye geç" : "Switch to English");
    }
    if (scroll) {
      var target = location.hash && document.getElementById(location.hash.slice(1));
      if (target && !target.closest("[hidden]")) target.scrollIntoView();
    }
  };
  var set = function (lang) { store(lang); apply(lang, false); };

  var lt = document.getElementById("lang-toggle");
  if (lt) {
    lt.addEventListener("click", function () { set(root.lang === "en" ? "tr" : "en"); });
  }
  document.querySelectorAll(".seg button").forEach(function (b) {
    b.addEventListener("click", function () { set(b.getAttribute("data-lang")); });
  });
  window.addEventListener("hashchange", function () {
    var h = location.hash.slice(1);
    var lang = /^en(-|$)/.test(h) ? "en" : /^tr(-|$)/.test(h) ? "tr" : null;
    if (lang && lang !== root.lang) apply(lang, true);
  });

  document.querySelectorAll(".copy-mail").forEach(function (btn) {
    var label = btn.textContent, timer = 0;
    btn.addEventListener("click", function () {
      var done = function () {
        btn.textContent = btn.getAttribute("data-done");
        clearTimeout(timer);
        timer = setTimeout(function () { btn.textContent = label; }, 2000);
      };
      var mail = btn.getAttribute("data-copy");
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(mail).then(done, done);
      else done();
    });
  });

  apply(pick(), true);
})();
