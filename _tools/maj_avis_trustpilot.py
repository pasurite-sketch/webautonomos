# -*- coding: utf-8 -*-
"""Avis Trustpilot du site : note, nombre d'avis et avis affichés (09/10/2026).

Constat sur Trustpilot le 09/10/2026 : 10 avis, tous à 5 étoiles, tous marqués
« Unprompted » (spontanés, pas « Verified ») ; TrustScore 4,4. Le site affichait
« 4,3 », « 8 avis vérifiés » / « verified reviews » / « opiniones verificadas » et
« note moyenne » (le TrustScore n'est pas une moyenne : elle serait de 5). Il lui
manquait les avis de Veronika Griessner (02/10) et d'Albert Vallverdú (29/09), et
les 7 pages métier espagnoles n'avaient pas non plus ceux d'Inés et de Sabine O.
Écrire « avis vérifiés » sans procédure de vérification est une pratique
commerciale trompeuse (C. conso L111-7-2 et L121-2 ; en Espagne, Ley 3/1991 art. 5
et TRLGDCU ; directive Omnibus). Remplace patch_trustpilot.py du 24/09, jamais lancé.

Ce script est RÉUTILISABLE : à chaque nouvel avis ou changement de note, modifier
TP_SCORE, TP_NB et NOUVEAUX ci-dessous, puis le relancer. Il converge vers l'état
voulu (compteurs remplacés quelle que soit leur valeur, avis ajoutés seulement
s'ils manquent) et ne réécrit rien s'il ne trouve pas une ancre attendue.

Ce qu'il fait :
  1. Générateurs : constantes TP_SCORE / TP_NB dans build_lang_homes.py, utilisées
     par build_expat_pages.py, build_metier_pages.py et build_uk_pages.py (fini les
     « 4,3 » codés en dur) ; avis ajoutés à AVIS (fr, en) et à l'ordre de chaque
     page métier ; guillemets anglais “…” sur les pages anglaises ; contrôle qui
     bloque le retour de « avis vérifiés », « verified reviews »… et d'une note
     différente de TP_SCORE.
  2. index.html (accueil, 4 langues) : testimonial9 et 10 ajoutés à translations et
     au carrousel, note et libellés « TrustScore », « publié sur Trustpilot » ;
     bloc avis du repli statique <div id="fallback"> reconstruit depuis
     translations.es (même format que patch_prix_iva_accueil_20261007.py).
  3. Pages démo (pide-tu-demo, demandez-votre-demo, get-your-demo ; leur
     générateur build_demo_pages.py est périmé) : note, libellé, 2 diapositives.
  4. 7 pages métier espagnoles : note, libellés, avis manquants.
  5. _tools/seo_pipeline/VERITE.md : ligne « Note Trustpilot affichée » ; CLAUDE.md : ligne du tableau
     des modifications d'index.html.
  Puis relance build_expat_pages.py, build_metier_pages.py (qui relance
  build_lang_homes.py et generate_sitemap.py) et build_uk_pages.py.

Sauvegarde : ~/webautonomos-work/backups/avis_trustpilot_<date>/
À lancer depuis ~/webautonomos, après git pull :
    python3 _tools/maj_avis_trustpilot.py
"""
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ═══════════════ À METTRE À JOUR QUAND TRUSTPILOT CHANGE ═══════════════
TP_SCORE = '4,4'      # TrustScore affiché par Trustpilot (virgule ; point en anglais)
TP_NB = 10            # nombre d'avis sur Trustpilot

# Avis à ajouter partout où ils manquent : texte, auteur, métier, mention de traduction.
# Textes relevés sur Trustpilot le 09/10/2026 ; traductions fidèles, signalées comme telles.
NOUVEAUX = [
    {'cle': 'Veronika Griessner',
     'es': ("Ha sido muy fácil y rápido. La web está preciosa: sencilla, clara y bonita, tal como la quería. "
            "Estoy muy contenta con la atención y el servicio recibidos por parte de Angelino. Sin duda "
            "recomendaré Web Autónomos a amigos y compañeros.", 'Psicóloga', ''),
     'val': ("Ha sigut molt fàcil i ràpid. La web és preciosa: senzilla, clara i bonica, tal com la volia. "
             "Estic molt contenta amb l'atenció i el servei rebuts per part d'Angelino. Sens dubte "
             "recomanaré Web Autónomos a amics i companys.", 'Psicòloga', 'traduït del castellà'),
     'en': ("It was very easy and quick. The website is lovely: simple, clear and beautiful, just as I wanted "
            "it. I'm very happy with the attention and service I received from Angelino. I'll definitely "
            "recommend Web Autónomos to friends and colleagues.", 'Psychologist', 'translated from Spanish'),
     'fr': ("Ça a été très facile et rapide. Le site est magnifique : simple, clair et beau, exactement comme "
            "je le voulais. Je suis très contente de l'attention et du service reçus de la part d'Angelino. "
            "Je recommanderai sans aucun doute Web Autónomos à mes amis et collègues.", 'Psychologue',
            "traduit de l'espagnol")},
    {'cle': 'Albert Vallverdú',
     'es': ("Estoy muy contento con la página web", 'Carpintero de aluminio y PVC', ''),
     'val': ("Estic molt content amb la pàgina web", "Fuster d'alumini i PVC", 'traduït del castellà'),
     'en': ("I'm very happy with the website", 'Aluminium and PVC joiner', 'translated from Spanish'),
     'fr': ("Je suis très content du site web", 'Menuisier aluminium et PVC', "traduit de l'espagnol")},
]
# Avis déjà affichés ailleurs, à ajouter aux pages métier espagnoles (texte de l'accueil espagnol)
ES_PAGES_EN_PLUS = [
    ('Inés', "Rápidos y eficaces, me gustó mucho cómo quedó la web, muchas gracias.", 'Crecimiento personal', ''),
    ('Sabine O.', "Muy buena experiencia con Webautonomos. Angelino hizo mi web teniendo en cuenta mis peticiones y "
                  "observaciones. Sus consejos, su paciencia y su disponibilidad me han sido de gran ayuda.",
     'Terapeuta de bienestar', 'traducido del francés'),
]
# Place d'un nouvel avis dans l'ordre des pages métier FR/EN/UK : en 2e position quand la page
# commence par un avis du même univers, sinon à la fin.
PROCHE = {'Veronika Griessner': ('Sabine O.', 'Ana Saiz'), 'Albert Vallverdú': ('Lee Robinson',)}
# ═════════════════════════════════════════════════════════════════════════

SCORE_EN = TP_SCORE.replace(',', '.')
LIB = {
    'fr': {'count': 'TrustScore calculé par Trustpilot sur %d avis' % TP_NB, 'verified': 'Avis publié sur Trustpilot'},
    'en': {'count': 'TrustScore calculated by Trustpilot from %d reviews' % TP_NB,
           'verified': 'Review published on Trustpilot'},
    'es': {'count': 'TrustScore calculado por Trustpilot sobre %d opiniones' % TP_NB,
           'verified': 'Opinión publicada en Trustpilot'},
    'val': {'count': 'TrustScore calculat per Trustpilot sobre %d opinions' % TP_NB,
            'verified': 'Opinió publicada en Trustpilot'},
}
INTERDITS = ('avis vérifiés', 'Avis vérifié', 'verified reviews', 'Verified review', 'verified Trustpilot',
             'opiniones verificadas', 'Opinión verificada', 'opinions verificades', 'Opinió verificada',
             'Note moyenne', 'Average rating', 'Valoración media', 'Valoració mitjana')
PAGES_ES = ['psicologos', 'dentistas', 'fisioterapeutas', 'electricistas', 'fontaneros', 'carpinteros', 'reformas']


class Erreur(Exception):
    pass


def remplacer(s, a, b, n=1, quoi=''):
    """Remplace a par b, n fois exactement ; déjà fait = rien à faire."""
    if s.count(a) == n:
        return s.replace(a, b)
    if a != b and s.count(b) >= n and s.count(a) == 0:
        return s
    raise Erreur('%s : ancre trouvée %dx au lieu de %d : %s' % (quoi, s.count(a), n, a.strip()[:80]))


def regex(s, motif, rempl, quoi, mini=1, flags=0):
    s2, n = re.subn(motif, rempl, s, flags=flags)
    if n < mini:
        raise Erreur('%s : motif introuvable : %s' % (quoi, motif[:80]))
    return s2


def js(x):
    return json.dumps(x, ensure_ascii=False)


# ─────────────────────────── 1. générateurs ───────────────────────────
QUOTE_OLD = ("                   '<blockquote>« %s »</blockquote><div class=\"tp-who\">— %s%s</div></div></div>') % (\n"
             "            E(txt), E(who),")
QUOTE_LANG = ("                   '<blockquote>%s</blockquote><div class=\"tp-who\">— %s%s</div></div></div>') % (\n"
              "            ('«\\u00a0%s\\u00a0»' if lang == 'fr' else '“%s”') % E(txt), E(who),")
QUOTE_EN = ("                   '<blockquote>“%s”</blockquote><div class=\"tp-who\">— %s%s</div></div></div>') % (\n"
            "            E(txt), E(who),")


def avis_tuple(lang, r):
    txt, job, tr = r[lang]
    return (txt, '%s — %s' % (r['cle'], job), tr)


def gen_homes(s):
    q = '_tools/build_lang_homes.py'
    if 'TP_SCORE = ' not in s:
        s = remplacer(s, "TRUSTPILOT = 'https://www.trustpilot.com/review/webautonomos.es'\n",
                      "TRUSTPILOT = 'https://www.trustpilot.com/review/webautonomos.es'\n"
                      "# Note et nombre d'avis Trustpilot des pages générées : tenus à jour par\n"
                      "# _tools/maj_avis_trustpilot.py (avis spontanés, pas « vérifiés » ; TrustScore, pas une moyenne).\n"
                      "TP_SCORE = '4,4'\nTP_NB = 10\n", quoi=q)
        s = remplacer(s, "  rating='<b>4,3/5</b> · 8 avis vérifiés sur Trustpilot',",
                      "  rating='<b>TrustScore %s/5</b> · %d avis sur Trustpilot' % (TP_SCORE, TP_NB),", quoi=q)
        s = remplacer(s, "rev_count='Note moyenne sur 8 avis vérifiés Trustpilot',",
                      "rev_count='TrustScore calculé par Trustpilot sur %d avis' % TP_NB,", quoi=q)
        s = remplacer(s, "  rating='<b>4.3/5</b> · 8 verified reviews on Trustpilot',",
                      "  rating='<b>TrustScore %s/5</b> · %d reviews on Trustpilot' % (TP_SCORE.replace(',', '.'), TP_NB),",
                      quoi=q)
        s = remplacer(s, "rev_count='Average rating from 8 verified Trustpilot reviews',",
                      "rev_count='TrustScore calculated by Trustpilot from %d reviews' % TP_NB,", quoi=q)
        s = remplacer(s, "<span class=\"tp-score\">{'4,3' if lang == 'fr' else '4.3'}</span>",
                      "<span class=\"tp-score\">{TP_SCORE if lang == 'fr' else TP_SCORE.replace(',', '.')}</span>", quoi=q)
        s = remplacer(s, QUOTE_OLD, QUOTE_LANG, quoi=q)
        s = remplacer(s, '"Inés — Croissance personnelle"', '"Inés — Développement personnel"', quoi=q)
        s = remplacer(
            s,
            "    for interdit in ('Plus de 40', 'More than 40', 'tp-score\">4,2', 'tp-score\">4.2', ' 6 avis', ' 6 verified'):\n"
            "        if interdit in s:\n"
            "            err.append('mention périmée : %s' % interdit)\n",
            "    for interdit in ('Plus de 40', 'More than 40', 'tp-score\">4,2', 'tp-score\">4.2', ' 6 avis', ' 6 verified',\n"
            "                     # avis Trustpilot spontanés, pas vérifiés ; TrustScore, pas une moyenne (09/10/2026)\n"
            "                     'avis vérifiés', 'verified reviews', 'verified Trustpilot', 'Note moyenne sur',\n"
            "                     'Average rating from'):\n"
            "        if interdit in s:\n"
            "            err.append('mention périmée : %s' % interdit)\n"
            "    for note in re.findall(r'class=\"tp-score\">([^<]*)<', s):\n"
            "        if note not in (TP_SCORE, TP_SCORE.replace(',', '.')):\n"
            "            err.append('note Trustpilot %s au lieu de %s (TP_SCORE)' % (note, TP_SCORE))\n"
            "    if '<html lang=\"en\"' in s and '<blockquote>«' in s:\n"
            "        err.append('guillemets français dans les témoignages d\\'une page anglaise')\n", quoi=q)
    s = regex(s, r"(?m)^TP_SCORE = '[^']*'$", "TP_SCORE = '%s'" % TP_SCORE, q)
    s = regex(s, r'(?m)^TP_NB = \d+$', 'TP_NB = %d' % TP_NB, q)
    # nouveaux avis en fin de liste, fr et en
    for lang in ('fr', 'en'):
        debut = s.index(" '%s': [\n" % lang, s.index('AVIS = {'))
        fin = s.index('\n ],\n', debut)
        bloc = s[debut:fin]
        ajout = ''
        for r in NOUVEAUX:
            if '"%s — ' % r['cle'] not in bloc:
                txt, who, tr = avis_tuple(lang, r)
                ajout += '\n  (%s, %s, %s),' % (js(txt), js(who), js(tr))
        s = s[:fin] + ajout + s[fin:]
    return s


def gen_expat(s):
    q = '_tools/build_expat_pages.py'
    if 'H.TP_SCORE' in s:
        return s
    s = remplacer(s, "rating='<b>4,3/5</b> · 8 avis vérifiés sur Trustpilot',",
                  "rating='<b>TrustScore %s/5</b> · %d avis sur Trustpilot' % (H.TP_SCORE, H.TP_NB),", quoi=q)
    s = remplacer(s, "rev_count='Note moyenne sur 8 avis vérifiés Trustpilot',",
                  "rev_count='TrustScore calculé par Trustpilot sur %d avis' % H.TP_NB,", quoi=q)
    s = remplacer(s, "rating='<b>4.3/5</b> · 8 verified reviews on Trustpilot',",
                  "rating='<b>TrustScore %s/5</b> · %d reviews on Trustpilot' % (H.TP_SCORE.replace(',', '.'), H.TP_NB),",
                  quoi=q)
    s = remplacer(s, "rev_count='Average rating from 8 verified Trustpilot reviews',",
                  "rev_count='TrustScore calculated by Trustpilot from %d reviews' % H.TP_NB,", quoi=q)
    s = remplacer(s, "<span class=\"tp-score\">{'4,3' if lang == 'fr' else '4.3'}</span>",
                  "<span class=\"tp-score\">{H.TP_SCORE if lang == 'fr' else H.TP_SCORE.replace(',', '.')}</span>", quoi=q)
    return remplacer(s, QUOTE_OLD, QUOTE_LANG, quoi=q)


def gen_metier(s):
    q = '_tools/build_metier_pages.py'
    if 'H.TP_SCORE' not in s:
        s = remplacer(s, "<span class=\"tp-score\">{'4,3' if lang == 'fr' else '4.3'}</span>",
                      "<span class=\"tp-score\">{H.TP_SCORE if lang == 'fr' else H.TP_SCORE.replace(',', '.')}</span>",
                      quoi=q)
        s = remplacer(s, QUOTE_OLD, QUOTE_LANG, quoi=q)
        s = remplacer(
            s,
            "NOTE_ES = [('<div class=\"proof-num\">4,2★</div>', '<div class=\"proof-num\">4,3★</div>'),\n"
            "           ('<div class=\"proof-label\">Valoración media sobre<br>6 opiniones en Trustpilot</div>',\n"
            "            '<div class=\"proof-label\">Valoración media sobre<br>8 opiniones en Trustpilot</div>')]\n",
            "# Note des pages métier espagnoles : tenue à jour par _tools/maj_avis_trustpilot.py ; ici, simple contrôle.\n"
            "NOTE_ES = [('<div class=\"proof-num\">4,3★</div>', '<div class=\"proof-num\">%s★</div>' % H.TP_SCORE),\n"
            "           ('<div class=\"proof-label\">Valoración media sobre<br>8 opiniones en Trustpilot</div>',\n"
            "            '<div class=\"proof-label\">TrustScore de Trustpilot<br>sobre %d opiniones</div>' % H.TP_NB)]\n",
            quoi=q)
    # ordre des avis de chaque page métier
    def ordre(m):
        liste = json.loads(m.group(1).replace("'", '"'))
        for r in NOUVEAUX:
            if r['cle'] in liste:
                continue
            if liste and liste[0] in PROCHE.get(r['cle'], ()):
                liste.insert(1, r['cle'])
            else:
                liste.append(r['cle'])
        return 'avis_ordre=%s,' % js(liste).replace('"', "'")
    return regex(s, r"avis_ordre=(\[[^\]]*\]),", ordre, q, mini=7)


def gen_uk(s):
    q = '_tools/build_uk_pages.py'
    if 'H.TP_SCORE' in s:
        return s
    s = remplacer(s, '<span class="tp-score">4.3</span>',
                  "<span class=\"tp-score\">{H.TP_SCORE.replace(',', '.')}</span>", quoi=q)
    return remplacer(s, QUOTE_OLD, QUOTE_EN, quoi=q)


# ─────────────────────────── 2. index.html (accueil SPA) ───────────────────────────
TITRES = {'es': 'Lo que dicen nuestros clientes', 'val': 'El que diuen els nostres clients',
          'en': 'What our clients say', 'fr': 'Ce que disent nos clients'}
COULEURS = ['bg-blue-500', 'bg-green-500', 'bg-purple-500', 'bg-orange-500', 'bg-teal-500', 'bg-pink-500',
            'bg-indigo-500', 'bg-amber-500']


def fin_bloc(s, i):
    """Index de l'accolade fermante du bloc qui s'ouvre en s[i] ('{'), chaînes comprises."""
    prof, k, chaine = 0, i, None
    while k < len(s):
        c = s[k]
        if chaine:
            if c == '\\':
                k += 2
                continue
            if c == chaine:
                chaine = None
        elif c in '"\'`':
            chaine = c
        elif c == '{':
            prof += 1
        elif c == '}':
            prof -= 1
            if prof == 0:
                return k
        k += 1
    raise Erreur('index.html : accolade non fermée')


def lire_translations(s):
    i = s.index('const translations=') + len('const translations=')
    obj = s[i:fin_bloc(s, i) + 1]
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write('process.stdout.write(JSON.stringify(' + obj + '));')
    r = subprocess.run(['node', f.name], capture_output=True, text=True)
    os.unlink(f.name)
    if r.returncode:
        raise Erreur('index.html : translations illisibles : ' + r.stderr[:300])
    return json.loads(r.stdout)


def e(x):
    return html.escape(x, quote=False)


def bloc_avis_repli(ts):
    """Même format que repli() de patch_prix_iva_accueil_20261007.py."""
    L = ['    <h2>%s</h2>' % e(ts['title']), '    <p>%s/5 — %s</p>' % (e(ts['ratingScore']), e(ts['ratingLabel']))]
    n = 1
    while 'testimonial%d' % n in ts:
        job, tr = ts.get('testimonial%dJob' % n, ''), ts.get('testimonial%dTranslated' % n, '')
        L.append('    <blockquote><p>%s</p><footer>%s%s%s</footer></blockquote>' % (
            e(ts['testimonial%d' % n]), e(ts['testimonial%dAuthor' % n]), (' · ' + e(job)) if job else '',
            (' (' + e(tr) + ')') if tr else ''))
        n += 1
    return '\n'.join(L) + '\n'


def accueil(s):
    q = 'index.html'
    i0 = s.index('const translations=')
    t = lire_translations(s)
    # blocs testimonials des 4 langues, repérés par leur titre
    for lang, titre in TITRES.items():
        a = s.index('testimonials:{title:%s' % js(titre), i0)
        b = fin_bloc(s, s.index('{', a))
        bloc = s[a:b]
        ts = t[lang]['testimonials']
        bloc = regex(bloc, r'ratingScore:"[^"]*"', 'ratingScore:%s' % js(TP_SCORE if lang != 'en' else SCORE_EN), q)
        bloc = regex(bloc, r'ratingLabel:"[^"]*"', 'ratingLabel:%s' % js(LIB[lang]['count']), q)
        bloc = regex(bloc, r'verifiedLabel:"[^"]*"', 'verifiedLabel:%s' % js(LIB[lang]['verified']), q)
        if lang == 'fr':
            bloc = bloc.replace('Job:"Croissance personnelle"', 'Job:"Développement personnel"')
        auteurs = [ts[k] for k in ts if re.fullmatch(r'testimonial\d+Author', k)]
        n = max(int(k[11:]) for k in ts if re.fullmatch(r'testimonial\d+', k))
        for r in NOUVEAUX:
            if r['cle'] in auteurs:
                continue
            n += 1
            txt, job, tr = r[lang]
            bloc += ',testimonial%d:%s,testimonial%dAuthor:%s,testimonial%dJob:%s,testimonial%dTranslated:%s' % (
                n, js(txt), n, js(r['cle']), n, js(job), n, js(tr))
        s = s[:a] + bloc + s[b:]
    # carrousel : un objet par testimonialN présent dans translations.es
    t = lire_translations(s)
    nb = max(int(k[11:]) for k in t['es']['testimonials'] if re.fullmatch(r'testimonial\d+', k))
    for lang in TITRES:
        nl = max(int(k[11:]) for k in t[lang]['testimonials'] if re.fullmatch(r'testimonial\d+', k))
        if nl != nb:
            raise Erreur('index.html : %d avis en %s, %d en es' % (nl, lang, nb))
    debut = s.index('const testimonials=[')
    fin = s.index('];', debut)
    car = s[debut:fin]
    deja = len(re.findall(r'\{text:t\.testimonials\.testimonial\d+,', car))
    ajout = ''
    for k in range(deja + 1, nb + 1):
        ajout += (',{text:t.testimonials.testimonial%d,author:t.testimonials.testimonial%dAuthor,'
                  'job:t.testimonials.testimonial%dJob,translated:t.testimonials.testimonial%dTranslated,color:"%s"}'
                  % (k, k, k, k, COULEURS[(k - 1) % len(COULEURS)]))
    s = s[:fin] + ajout + s[fin:]
    # repli statique : bloc des avis reconstruit depuis translations.es
    ts = lire_translations(s)['es']['testimonials']
    a = s.index('<div id="fallback">')
    h2 = s.index('    <h2>%s</h2>\n' % e(ts['title']), a)
    fin_avis = s.index('\n\n', h2) + 1
    s = s[:h2] + bloc_avis_repli(ts) + s[fin_avis:]
    return s


# ─────────────────────────── 3. pages démo ───────────────────────────
DEMOS = {'pide-tu-demo.html': 'es', 'demandez-votre-demo.html': 'fr', 'get-your-demo.html': 'en'}


def demo(s, lang, q):
    s = regex(s, r'(<span class="tp-score">)[^<]*(</span>)', r'\g<1>%s\g<2>' % (SCORE_EN if lang == 'en' else TP_SCORE), q)
    s = regex(s, r'(<span class="tp-count">)[^<]*(</span>)', r'\g<1>%s\g<2>' % LIB[lang]['count'], q)
    if lang == 'en':
        s = s.replace('<blockquote>«\u00a0', '<blockquote>“').replace('\u00a0»</blockquote>', '”</blockquote>')
    if lang == 'fr':
        s = s.replace('— Inés — Croissance personnelle', '— Inés — Développement personnel')
    fin_track = s.index('</div></div>\n', s.index('<div class="tp-track" id="tpTrack">'))
    track = s[s.index('<div class="tp-track" id="tpTrack">'):fin_track]
    dots_a = s.index('<div class="tp-dots" id="tpDots">')
    dots_b = s.index('</div>', dots_a)
    dots = s[dots_a:dots_b]
    m = re.findall(r'<button class="tp-dot[^"]*" onclick="tpGo\((\d+)\)" aria-label="([^"]*) (\d+)"></button>', dots)
    if not m:
        raise Erreur('%s : points du carrousel introuvables' % q)
    n, prefixe = len(m), m[0][1]
    slides, boutons = '', ''
    for r in NOUVEAUX:
        if '— %s — ' % r['cle'] in track:
            continue
        txt, job, tr = r[lang]
        guil = ('“%s”' if lang == 'en' else '«\u00a0%s\u00a0»') % e(txt)
        slides += ('<div class="tp-slide"><div class="tp-card"><div class="tp-stars">★★★★★</div><blockquote>%s</blockquote>'
                   '<div class="tp-who">— %s — %s%s</div></div></div>') % (
            guil, e(r['cle']), e(job), '<span class="tp-tr">%s</span>' % e(tr) if tr else '')
        boutons += '<button class="tp-dot" onclick="tpGo(%d)" aria-label="%s %d"></button>' % (n, prefixe, n + 1)
        n += 1
    s = s[:dots_b] + boutons + s[dots_b:]
    return s[:fin_track] + slides + s[fin_track:]


# ─────────────────────────── 4. pages métier espagnoles ───────────────────────────
def carte_es(nom, txt, job, tr):
    meta = 'Opinión en Trustpilot' + (' · ' + tr if tr else '')
    return ('      <div class="review-card">\n'
            '        <div class="proof-stars">★★★★★</div>\n'
            '        <blockquote>"%s"</blockquote>\n'
            '        <cite>— %s%s<br><span class="review-meta">%s</span></cite>\n'
            '      </div>\n') % (e(txt), e(nom), ', ' + e(job) if job else '', meta)


def page_es(s, p, q):
    s = regex(s, r'Opiniones reales de clientes, \w+ en Trustpilot\.',
              'Opiniones reales de clientes, publicadas en Trustpilot.', q)
    s = regex(s, r'<div class="proof-num">\d,\d★</div>', '<div class="proof-num">%s★</div>' % TP_SCORE, q)
    s = regex(s, r'<div class="proof-label">(?:Valoración media sobre|TrustScore de Trustpilot)<br>[^<]*</div>',
              '<div class="proof-label">TrustScore de Trustpilot<br>sobre %d opiniones</div>' % TP_NB, q)
    s = s.replace('<span class="review-meta">Opinión verificada', '<span class="review-meta">Opinión en Trustpilot')
    a = s.index('<div class="reviews-track">')
    b = s.index('    </div>\n  </div>\n  <p class="reviews-link">', a)
    track = s[a:b]
    cartes = re.findall(r'      <div class="review-card">\n.*?\n      </div>\n', track, re.S)
    if not cartes:
        raise Erreur('%s : cartes d\'avis introuvables' % q)
    entete = track[:track.index(cartes[0])]
    nouvelles = [(r['cle'],) + r['es'] for r in NOUVEAUX] + ES_PAGES_EN_PLUS
    for nom, txt, job, tr in nouvelles:
        if '<cite>— %s' % e(nom) in track:
            continue
        carte = carte_es(nom, txt, job, tr)
        if p == 'psicologos' and nom == 'Veronika Griessner':
            cartes.insert(2, carte)        # 3 avis de psychologues en tête (seuls 3 visibles sur grand écran)
        elif p == 'carpinteros' and nom == 'Albert Vallverdú':
            cartes.insert(1, carte)        # les deux menuisiers en tête
        else:
            cartes.append(carte)
        track = entete + ''.join(cartes)
    return s[:a] + entete + ''.join(cartes) + s[b:]


# ─────────────────────────── 5. VERITE.md ───────────────────────────
def verite(s):
    return regex(s, r'(?m)^- Note Trustpilot affichée : .*$',
                 '- Note Trustpilot affichée : **TrustScore %s/5 sur %d avis** (avis spontanés : ne jamais écrire '
                 '« vérifiés » ni « note moyenne » ; à mettre à jour ici et dans `_tools/maj_avis_trustpilot.py`, '
                 'qui met le site à jour, quand elle change)' % (TP_SCORE, TP_NB), '_tools/seo_pipeline/VERITE.md')


def claude_md(s):
    """Ligne du tableau « index.html : ce que le dépôt contient en plus de Lovable »."""
    if 'maj_avis_trustpilot.py' in s:
        return s
    ancre = "| Textes de l'accueil espagnol conformes à VERITE"
    i = s.index(ancre)
    fin = s.index('\n', i) + 1
    ligne = ("| Avis Trustpilot 9 et 10 (Veronika Griessner, Albert Vallverdú) dans les 4 langues et le carrousel, note et "
             "libellés « TrustScore », « publié sur Trustpilot », bloc avis du repli `fallback` | "
             "`_tools/maj_avis_trustpilot.py`, le 2026-10-09 (à relancer, après mise à jour de ses constantes, à chaque "
             "nouvel avis ou changement de note) | Les deux derniers avis ; « 4,3 », « 8 opiniones verificadas » et "
             "« valoración media » reviendraient, alors que les avis sont spontanés et que 4,4 est un TrustScore |\n")
    return s[:fin] + ligne + s[fin:]


def main():
    os.chdir(ROOT)
    travaux = {
        '_tools/build_lang_homes.py': gen_homes,
        '_tools/build_expat_pages.py': gen_expat,
        '_tools/build_metier_pages.py': gen_metier,
        '_tools/build_uk_pages.py': gen_uk,
        'index.html': accueil,
        '_tools/seo_pipeline/VERITE.md': verite,
        'CLAUDE.md': claude_md,
    }
    for f, lang in DEMOS.items():
        travaux[f] = (lambda l, q: lambda s: demo(s, l, q))(lang, f)
    for p in PAGES_ES:
        rel = p + '/index.html'
        travaux[rel] = (lambda pp, q: lambda s: page_es(s, pp, q))(p, rel)

    nouveaux, err = {}, []
    for rel, f in travaux.items():
        try:
            avant = open(rel, encoding='utf-8').read()
            apres = f(avant)
            if rel.endswith('.py'):
                compile(apres, rel, 'exec')
            elif rel.endswith('.html'):
                visible = re.sub(r'<script.*?</script>', '', apres, flags=re.S)
                for x in INTERDITS:
                    if x in visible:
                        err.append('%s : il reste « %s »' % (rel, x))
            if apres != avant:
                nouveaux[rel] = apres
        except (Erreur, ValueError, SyntaxError) as exc:
            err.append(str(exc))
    # index.html : le bundle doit rester du JavaScript valide, sans mention interdite
    if 'index.html' in nouveaux and not err:
        h = nouveaux['index.html']
        for x in ('Opinión verificada', 'Opinió verificada', 'Verified review', 'Avis vérifié', 'opiniones verificadas',
                  'opinions verificades', 'verified reviews', 'avis vérifiés'):
            if x in h:
                err.append('index.html : il reste « %s »' % x)
        for m in re.finditer(r'<script>(.*?)</script>', h, re.S):
            if 'const translations=' in m.group(1):
                with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as fh:
                    fh.write(m.group(1))
                r = subprocess.run(['node', '--check', fh.name], capture_output=True, text=True)
                os.unlink(fh.name)
                if r.returncode:
                    err.append('index.html : JavaScript invalide : ' + r.stderr[:300])
    if err:
        sys.exit('ABANDON : vérifications :\n  - ' + '\n  - '.join(err) + '\nRien n\'a été modifié.')
    if not nouveaux:
        print('Rien à faire : le site est déjà à jour (TrustScore %s, %d avis).' % (TP_SCORE, TP_NB))
    else:
        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        bak = os.path.expanduser('~/webautonomos-work/backups/avis_trustpilot_%s' % stamp)
        for rel in nouveaux:
            d = os.path.join(bak, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(rel, d)
        for rel, s in nouveaux.items():
            open(rel, 'w', encoding='utf-8').write(s)
            print('  ✓ %s' % rel)
        print('Sauvegarde : %s\n' % bak.replace(os.path.expanduser('~'), '~'))
    for script in ('_tools/build_expat_pages.py', '_tools/build_metier_pages.py', '_tools/build_uk_pages.py'):
        print('→ %s' % script)
        r = subprocess.run([sys.executable, script], cwd=ROOT)
        if r.returncode:
            sys.exit('ÉCHEC de %s : relance-le à la main après correction.' % script)
    print('\nOK — étape suivante : git add, commit et push (le déploiement suit automatiquement).')


if __name__ == '__main__':
    main()
