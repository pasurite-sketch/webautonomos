/* Origine des leads (10/10/2026). Inclus dans le <head> de toutes les pages, index.html et blog compris, par
   _tools/patch_origine_leads_20261010.py et par les générateurs (_tools/origine_lead.py) : relancer le patch après un
   ré-export d'index.html ou pour une page écrite à la main.
   1. À chaque visite : garde 90 jours les identifiants publicitaires (gclid, gbraid, wbraid, utm_*) sous la même
      clé que le script des pages de démo (wa_ads), et l'arrivée sur le site (site d'origine, page d'entrée) sous
      wa_origine. Une nouvelle arrivée par une annonce ou depuis un autre site remplace l'ancienne ; une visite
      directe la garde.
   2. Au moment où un formulaire est envoyé (écouteur en phase de capture, donc avant le code du formulaire, React
      compris) : ajoute ces données en champs cachés, plus form_page (la page du formulaire). Les formulaires qui
      lisent new FormData(form) les transmettent tels quels (Make : referrer, landing_page, form_page). */
(function () {
  var ADS = 'wa_ads', ORIGINE = 'wa_origine', DUREE = 90 * 24 * 3600 * 1000;
  var CLES = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term'];

  function lire(cle) {
    try {
      var o = JSON.parse(localStorage.getItem(cle) || 'null');
      return o && o.t && (Date.now() - o.t) < DUREE ? (o.d || {}) : null;
    } catch (e) { return null; }
  }
  function ecrire(cle, d) {
    try { localStorage.setItem(cle, JSON.stringify({ t: Date.now(), d: d })); } catch (e) {}
  }
  function sansAncre(u) { return String(u || '').split('#')[0]; }

  var p = new URLSearchParams(location.search), pub = {}, annonce = false;
  CLES.forEach(function (k) { var v = p.get(k); if (v) { pub[k] = v; annonce = true; } });
  if (annonce) ecrire(ADS, pub);

  var ref = document.referrer || '';
  var interne = ref && ref.indexOf(location.protocol + '//' + location.host) === 0;
  var deja = lire(ORIGINE);
  if (!interne && (annonce || ref)) {
    // arrivée par une annonce, un lien tagué ou un autre site (Google, Instagram, annuaire…)
    ecrire(ORIGINE, { referrer: ref ? sansAncre(ref) : '(direct)', landing_page: sansAncre(location.href) });
  } else if (!deja) {
    // première trace : visite directe, ou arrivée par une page du site sans ce script (l'ancienne page fait foi).
    // Une page du site (rechargement, lien interne) ne remplace jamais une origine déjà notée.
    ecrire(ORIGINE, interne && !annonce
      ? { referrer: '(page du site sans suivi)', landing_page: sansAncre(ref) }
      : { referrer: '(direct)', landing_page: sansAncre(location.href) });
  }

  // Pour les formulaires qui construisent leurs données à la main (pages Visibilidad IA) : window.origineLead()
  window.origineLead = function () {
    var a = lire(ADS) || {}, o = lire(ORIGINE) || {}, champs = {};
    CLES.forEach(function (k) { if (a[k]) champs[k] = a[k]; });
    if (o.referrer) champs.referrer = o.referrer;
    if (o.landing_page) champs.landing_page = o.landing_page;
    champs.form_page = sansAncre(location.href);
    return champs;
  };

  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM') return;
    var champs = window.origineLead();
    Object.keys(champs).forEach(function (k) {
      var el = f.querySelector('[name="' + k + '"]');
      if (!el) {
        el = document.createElement('input');
        el.type = 'hidden';
        el.name = k;
        f.appendChild(el);
      }
      if (!el.value) el.value = champs[k];
    });
  }, true);
})();
