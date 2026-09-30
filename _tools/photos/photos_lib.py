# -*- coding: utf-8 -*-
"""Automatisation « une photo par page » : fonctions communes.

Deux fichiers de ce dossier pilotent tout :
- sujets.json : la file des photos à produire. Un sujet = une photo, partagée
  par les versions linguistiques d'une même page, avec la scène à photographier ;
- images.json : pour chaque page HTML, la photo qu'elle affiche (fichiers dans
  assets/, texte alternatif et légende dans la langue de la page).

injecter(rel, html) pose ou remplace la photo d'une page d'après images.json.
Les générateurs (build_*.py, generate_blog_index.py) l'appellent juste avant
d'écrire leur fichier : une page régénérée garde sa photo. photos.py
l'applique directement aux pages sans générateur.

Positions retenues (29/09/2026) :
- article du blog : juste après le paragraphe d'introduction, avec le balisage
  exact de generate_spa_articles.py ;
- page à bandeau (H1 dans <section class="hero"> ou <header class="hero">) :
  juste après le bandeau et son fil d'Ariane ;
- page simple (H1 dans <main>) : après le paragraphe d'introduction (p.lede)
  et les notes ou boutons qui le suivent immédiatement.
"""

import datetime
import html as _html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ASSETS = os.path.join(ROOT, 'assets')
IMAGES_JSON = os.path.join(HERE, 'images.json')
SUJETS_JSON = os.path.join(HERE, 'sujets.json')
INDEX = os.path.join(ROOT, 'index.html')

LARGEUR, HAUTEUR = 1600, 900
MARQUE_DEBUT = '<!-- photo:auto -->'
MARQUE_FIN = '<!-- /photo:auto -->'
# Deuxième image (30/09/2026) : maquette MacBook + smartphone, au milieu de la page.
MAQ_DEBUT = '<!-- maquette:auto -->'
MAQ_FIN = '<!-- /maquette:auto -->'
# Sections (id, classe) et intertitres qui ne comptent pas pour trouver le milieu
# d'une page : FAQ, témoignages, formulaires, contact.
_HORS_MILIEU = re.compile(r'faq|pregunt|question|formul|contact|t[ée]moign|testimon|opini', re.I)
_TITRES_HORS_MILIEU = re.compile(
    r'preguntas frecuentes|questions fr[ée]quentes|frequently asked|\bfaq\b|suelen preguntar|'
    r'ce que disent|lo que dicen|what our clients|t[ée]moignages|testimonios|testimonials|opiniones|'
    r'contact', re.I)
INTRO_ARTICLE = '<p class="text-lg text-gray-700 leading-relaxed mb-6">'

# Paragraphes qui complètent l'introduction d'une page simple : la photo passe
# après eux pour ne pas séparer un prix de sa note fiscale ni l'intro de ses
# boutons.
SUITES_LEDE = ('tax-note', 'no-plantilla')


class PhotoErreur(Exception):
    pass


def E(s):
    return _html.escape(s or '', quote=True)


# --------------------------------------------------------------------------
# Fichiers de pilotage
# --------------------------------------------------------------------------

def lire_json(path, defaut):
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except FileNotFoundError:
        return defaut


def ecrire_json(path, data):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    os.replace(tmp, path)


def cle_page(rel):
    """Chemin d'une page relatif à la racine du dépôt, avec des « / »."""
    return os.path.relpath(os.path.abspath(rel), ROOT).replace(os.sep, '/')


def images():
    return lire_json(IMAGES_JSON, {}).get('pages', {})


def maquettes():
    return lire_json(IMAGES_JSON, {}).get('maquettes', {})


def aujourdhui():
    return datetime.date.today().isoformat()


def active(cfg, jour=None):
    """Une photo peut attendre une date (page gelée pour une mesure SEO)."""
    pa = cfg.get('pas_avant')
    return not pa or (jour or aujourdhui()) >= pa


# --------------------------------------------------------------------------
# Balisage
# --------------------------------------------------------------------------

def figure_article(cfg):
    """Exactement ce que generate_spa_articles.py rend pour un bloc image."""
    base = '/assets/' + cfg['fichier']
    v = cfg.get('v', 1)
    w, h = cfg.get('largeur', LARGEUR), cfg.get('hauteur', HAUTEUR)
    lignes = [
        '            <figure class="my-10">',
        '                <picture>',
        '                    <source type="image/webp" srcset="%s-800.webp?v=%s 800w, %s.webp?v=%s %sw" sizes="(max-width: 820px) calc(100vw - 40px), 780px">' % (base, v, base, v, w),
        '                    <img src="%s.jpg?v=%s" alt="%s" width="%s" height="%s" loading="lazy" decoding="async" class="w-full rounded-2xl">' % (base, v, E(cfg.get('alt')), w, h),
        '                </picture>']
    if cfg.get('legende'):
        lignes.append('                <figcaption class="text-sm text-gray-500 mt-3">%s</figcaption>' % E(cfg['legende']))
    lignes.append('            </figure>')
    return '\n'.join(lignes)


def figure_page(cfg, entre_sections, marques=(MARQUE_DEBUT, MARQUE_FIN)):
    """Balisage autonome (styles en ligne) : il ne dépend d'aucune feuille de
    style, donc il s'affiche pareil sur tous les gabarits du site."""
    base = '/assets/' + cfg['fichier']
    v = cfg.get('v', 1)
    w, h = cfg.get('largeur', LARGEUR), cfg.get('hauteur', HAUTEUR)
    marge, retrait = ('40px auto', '0 20px') if entre_sections else ('28px auto', '0')
    lignes = [
        marques[0],
        '<figure class="photo-auto" style="max-width:880px;margin:%s;padding:%s;box-sizing:border-box">' % (marge, retrait),
        '<picture>',
        '<source type="image/webp" srcset="%s-800.webp?v=%s 800w, %s.webp?v=%s %sw" sizes="(max-width: 920px) calc(100vw - 40px), 880px">' % (base, v, base, v, w),
        '<img src="%s.jpg?v=%s" alt="%s" width="%s" height="%s" loading="lazy" decoding="async" style="display:block;width:100%%;height:auto;border-radius:16px">' % (base, v, E(cfg.get('alt')), w, h),
        '</picture>']
    if cfg.get('legende'):
        lignes.append('<figcaption style="margin:10px 0 0;font-size:14px;line-height:1.5;color:#6b7280;text-align:center">%s</figcaption>' % E(cfg['legende']))
    lignes += ['</figure>', marques[1]]
    return '\n'.join(lignes)


# --------------------------------------------------------------------------
# Position d'insertion
# --------------------------------------------------------------------------

def _fin_element(h, debut, tag):
    """Index juste après la balise fermante qui équilibre celle ouverte en `debut`."""
    motif = re.compile(r'<(/?)%s\b[^>]*>' % tag, re.I)
    profondeur = 0
    for m in motif.finditer(h, debut):
        profondeur += -1 if m.group(1) else 1
        if profondeur == 0:
            return m.end()
    raise PhotoErreur('balise <%s> jamais fermée' % tag)


def _blancs(h, i):
    while i < len(h) and h[i] in ' \t\r\n':
        i += 1
    return i


def point_insertion(h):
    """(index, gabarit, entre_sections) : où poser la photo dans la page `h`."""
    i_h1 = h.find('<h1')
    if i_h1 < 0:
        raise PhotoErreur('pas de <h1> dans la page')

    # 1. Article du blog : après l'introduction.
    j = h.find(INTRO_ARTICLE)
    if j >= 0:
        return h.find('</p>', j) + len('</p>'), 'article', False

    # 2. Page à bandeau : après le <section|header class="hero…"> qui contient le H1.
    hero = None
    for m in re.finditer(r'<(section|header)\b[^>]*\bclass="[^"]*\bhero\b[^"]*"[^>]*>', h[:i_h1]):
        hero = m
    if hero is not None:
        fin = _fin_element(h, hero.start(), hero.group(1))
        if fin > i_h1:
            k = _blancs(h, fin)
            if h.startswith('<p class="crumbs"', k):
                fin = h.find('</p>', k) + len('</p>')
            return fin, 'page', True

    # 3. Page simple : après p.lede et ce qui la complète immédiatement.
    fin_h1 = h.find('</h1>', i_h1) + len('</h1>')
    k = _blancs(h, fin_h1)
    if h.startswith('<p class="lede"', k):
        pos = h.find('</p>', k) + len('</p>')
        while True:
            k = _blancs(h, pos)
            m = re.match(r'<p class="([^"]+)"', h[k:k + 80])
            if m and m.group(1) in SUITES_LEDE:
                pos = h.find('</p>', k) + len('</p>')
                continue
            if h.startswith('<div class="actions"', k):
                pos = _fin_element(h, k, 'div')
                continue
            return pos, 'page', False
    j = h.find('</p>', fin_h1)
    if j < 0:
        raise PhotoErreur('aucun paragraphe après le <h1>')
    return j + len('</p>'), 'page', False


def _retirer(h, cfg, marques=(MARQUE_DEBUT, MARQUE_FIN)):
    """Retire l'image déjà posée (marqueurs, ou figure d'article portant le
    même fichier) pour pouvoir la remplacer."""
    a = h.find(marques[0])
    if a >= 0:
        b = h.find(marques[1], a)
        if b < 0:
            raise PhotoErreur('marqueur de fin absent (%s)' % marques[0])
        b += len(marques[1])
        if h[a - 1:a] == '\n':
            a -= 1
        return h[:a] + h[b:]
    cible = 'src="/assets/%s.jpg?v=' % cfg['fichier']
    for m in re.finditer(r'\n            <figure class="my-10">.*?</figure>', h, re.S):
        if cible in m.group(0):
            return h[:m.start()] + h[m.end():]
    return h


def _sections(h, depart):
    """Sections de premier niveau qui commencent après `depart` :
    (début, balise ouvrante, contenu)."""
    out, fin_prec = [], -1
    for m in re.finditer(r'<section\b[^>]*>', h):
        if m.start() < fin_prec:
            continue          # section imbriquée
        fin = _fin_element(h, m.start(), 'section')
        fin_prec = fin
        if m.start() > depart:
            out.append((m.start(), m.group(0), h[m.end():fin]))
    return out


def point_milieu(h):
    """(index, gabarit, entre_sections) : où poser la maquette, au milieu de la
    page, en ignorant FAQ, témoignages, formulaires et contact."""
    a = h.find(MARQUE_FIN)
    if a >= 0:
        depart = a
    else:
        try:
            depart = point_insertion(h)[0]
        except PhotoErreur:
            depart = 0
    # 1. Articles : intertitres numérotés (seccion-N).
    h2 = [m.start() for m in re.finditer(r'<h2\b[^>]*\bid="seccion-\d+"', h) if m.start() > depart]
    if len(h2) >= 2:
        return h2[len(h2) // 2], ('article' if INTRO_ARTICLE in h else 'page'), False
    # 2. Pages à sections : entre deux sections.
    cands = []
    for debut, balise, contenu in _sections(h, depart):
        t = re.search(r'<h2\b[^>]*>(.*?)</h2>', contenu, re.S)
        if not t or '<form' in contenu:
            continue
        if _HORS_MILIEU.search(balise) or _TITRES_HORS_MILIEU.search(re.sub(r'<[^>]+>', '', t.group(1))):
            continue
        cands.append(debut)
    if len(cands) >= 2:
        return cands[len(cands) // 2], 'page', True
    # 3. Pages simples : intertitres.
    h2 = [m.start() for m in re.finditer(r'<h2\b[^>]*>(.*?)</h2>', h, re.S)
          if m.start() > depart and not _TITRES_HORS_MILIEU.search(re.sub(r'<[^>]+>', '', m.group(1)))]
    if len(h2) >= 2:
        return h2[len(h2) // 2], 'page', False
    # 4. Pages sans intertitre (FAQ, contact, démos) : fin du contenu, loin de la photo.
    j = h.rfind('</main>')
    if j > depart:
        return j, 'page', False
    raise PhotoErreur('aucune position trouvée pour la maquette')


def injecter(rel, h, cfg=None, jour=None, maquette=None):
    """Page `h` avec sa photo et sa maquette (d'après images.json quand `cfg`
    ou `maquette` sont absents). Sans image prévue, ou avant sa date, la page
    revient inchangée."""
    cle = cle_page(rel)
    if cfg is None:
        cfg = images().get(cle)
    if maquette is None:
        maquette = maquettes().get(cle)
    if cfg and active(cfg, jour):
        h = _retirer(h, cfg)
        pos, gabarit, entre = point_insertion(h)
        bloc = figure_article(cfg) if gabarit == 'article' else figure_page(cfg, entre)
        h = h[:pos] + '\n' + bloc + h[pos:]
    if maquette and active(maquette, jour):
        h = _retirer(h, maquette, (MAQ_DEBUT, MAQ_FIN))
        pos, gabarit, entre = point_milieu(h)
        if gabarit == 'article':
            bloc = figure_article(maquette)
        else:
            bloc = figure_page(maquette, entre, (MAQ_DEBUT, MAQ_FIN))
        # au début de la ligne de l'intertitre : même rendu que le générateur
        debut_ligne = h.rfind('\n', 0, pos) + 1
        if not h[debut_ligne:pos].strip():
            pos = debut_ligne
        h = h[:pos] + bloc + '\n' + h[pos:]
    return h


def compte_photo(h, cfg):
    """Nombre de fois où la photo de `cfg` figure dans la page."""
    return h.count('src="/assets/%s.jpg?v=' % cfg['fichier'])


# --------------------------------------------------------------------------
# Données des articles (objet translations de index.html)
# --------------------------------------------------------------------------

def js_valeur(v):
    """Littéral JavaScript, dans la convention de _tools/add_article.py."""
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'
    if isinstance(v, list):
        return '[' + ','.join(js_valeur(x) for x in v) + ']'
    if isinstance(v, dict):
        return '{' + ','.join(k + ':' + js_valeur(x) for k, x in v.items()) + '}'
    raise TypeError(type(v))


def bloc_image(cfg):
    """Bloc de contenu lu par generate_spa_articles.py."""
    b = {'type': 'image', 'src': '/assets/%s.jpg' % cfg['fichier'],
         'width': cfg.get('largeur', LARGEUR), 'height': cfg.get('hauteur', HAUTEUR),
         'v': str(cfg.get('v', 1)), 'alt': cfg.get('alt') or ''}
    if cfg.get('legende'):
        b['caption'] = cfg['legende']
    return b


def _fin_chaine_js(s, i):
    q = s[i]
    i += 1
    while True:
        c = s[i]
        if c == '\\':
            i += 2
        elif c == q:
            return i + 1
        else:
            i += 1


def _fin_valeur_js(s, i):
    """s[i] ouvre un objet ou un tableau ; index juste après sa fermeture."""
    profondeur = 0
    while True:
        c = s[i]
        if c in '"\'`':
            i = _fin_chaine_js(s, i)
            continue
        if c in '{[':
            profondeur += 1
        elif c in '}]':
            profondeur -= 1
            if profondeur == 0:
                return i + 1
        i += 1


def _blocs_article(s, slug):
    """(ouverture du tableau content, [(début, fin) de chaque bloc])."""
    cle = 'slug:"%s"' % slug
    n = s.count(cle)
    if n != 1:
        raise PhotoErreur('%s trouvé %d fois dans index.html' % (cle, n))
    i = s.find(cle)
    j = s.find('content:[', i)
    suivant = s.find('slug:"', i + len(cle))
    if j < 0 or (0 <= suivant < j):
        raise PhotoErreur('contenu introuvable pour %s' % slug)
    a = j + len('content:')
    fin = _fin_valeur_js(s, a)
    blocs, p = [], a + 1
    while True:
        while s[p] in ' \t\r\n,':
            p += 1
        if p >= fin - 1:
            break
        e = _fin_valeur_js(s, p)
        blocs.append((p, e))
        p = e
    return a, blocs


def a_bloc_image(s, slug, cfg):
    _, blocs = _blocs_article(s, slug)
    cible = 'src:"/assets/%s.jpg"' % cfg['fichier']
    return any(s[d:e].startswith('{type:"image"') and cible in s[d:e] for d, e in blocs)


def poser_bloc_spa(s, slug, cfg, milieu=False):
    """index.html avec le bloc image de l'article `slug` (ex. « es/mon-article ») :
    la photo juste après l'introduction ; la maquette (milieu=True) avant
    l'intertitre du milieu. Le bloc déjà posé pour ce fichier est remplacé."""
    s = retirer_bloc_spa(s, slug, cfg)
    a, blocs = _blocs_article(s, slug)
    nouveau = js_valeur(bloc_image(cfg))
    if milieu:
        titres = [d for d, e in blocs if s[d:e].startswith('{type:"heading"')]
        if len(titres) >= 2:
            d = titres[len(titres) // 2]
            return s[:d] + nouveau + ',' + s[d:]
        if blocs:
            e = blocs[-1][1]
            return s[:e] + ',' + nouveau + s[e:]
        return s[:a + 1] + nouveau + s[a + 1:]
    if blocs and s[blocs[0][0]:blocs[0][1]].startswith('{type:"intro"'):
        pos = blocs[0][1]
        return s[:pos] + ',' + nouveau + s[pos:]
    return s[:a + 1] + nouveau + (',' if blocs else '') + s[a + 1:]


def retirer_bloc_spa(s, slug, cfg):
    """index.html sans le bloc image (de ce fichier) de l'article `slug`."""
    _, blocs = _blocs_article(s, slug)
    cible = 'src:"/assets/%s.jpg"' % cfg['fichier']
    for i, (d, e) in enumerate(blocs):
        if s[d:e].startswith('{type:"image"') and cible in s[d:e]:
            if i > 0:
                return s[:s.rfind(',', blocs[i - 1][1], d)] + s[e:]
            if len(blocs) > 1:
                return s[:d] + s[s.find(',', e) + 1:]
            return s[:d] + s[e:]
    return s


def _ecrire_file(path, brut, d):
    """Réécrit un JSON de la file dans la convention de l'original."""
    m = re.match(r'\{\s*\n( +)"', brut)
    retrait = len(m.group(1)) if m else 2
    # accents bruts ou échappés, comme dans le fichier d'origine
    ascii_ = not re.search(r'[^\x00-\x7f]', brut)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=ascii_, indent=retrait)
        if brut.endswith('\n'):
            fh.write('\n')


def poser_bloc_file(path, cfg_par_langue, milieu=False):
    """Article en file d'attente (_tools/queue/*.json) : bloc image après
    l'introduction (photo) ou avant l'intertitre du milieu (maquette), dans
    chaque langue. publish_next.py le reprendra tel quel."""
    brut = open(path, encoding='utf-8').read()
    d = json.loads(brut)
    for lg, cfg in cfg_par_langue.items():
        if lg not in d:
            continue
        bloc = bloc_image(cfg)
        contenu = [b for b in d[lg]['content'] if not (b.get('type') == 'image' and b.get('src') == bloc['src'])]
        if milieu:
            titres = [i for i, b in enumerate(contenu) if b.get('type') == 'heading']
            pos = titres[len(titres) // 2] if len(titres) >= 2 else len(contenu)
        else:
            pos = 1 if contenu and contenu[0].get('type') == 'intro' else 0
        contenu.insert(pos, bloc)
        d[lg]['content'] = contenu
    _ecrire_file(path, brut, d)


def retirer_bloc_file(path, fichier):
    """Retire d'un article en file le bloc image de ce fichier. True si modifié."""
    brut = open(path, encoding='utf-8').read()
    d = json.loads(brut)
    cible = '/assets/%s.jpg' % fichier
    modifie = False
    for v in d.values():
        if isinstance(v, dict) and isinstance(v.get('content'), list):
            garde = [b for b in v['content'] if not (b.get('type') == 'image' and b.get('src') == cible)]
            if len(garde) != len(v['content']):
                v['content'] = garde
                modifie = True
    if modifie:
        _ecrire_file(path, brut, d)
    return modifie


# --------------------------------------------------------------------------
# Image
# --------------------------------------------------------------------------

_OCR = None


def textes_dans_image(chemin):
    """Textes lisibles détectés dans l'image (RapidOCR, local et gratuit).
    Les photos du site n'en contiennent aucun : une seule zone suffit à refuser.
    Renvoie None si le détecteur n'est pas installé (environnement ~/photos/venv
    du VPS), la liste des textes sinon."""
    global _OCR
    try:
        if _OCR is None:
            from rapidocr_onnxruntime import RapidOCR
            _OCR = RapidOCR()
    except ImportError:
        return None
    resultat, _ = _OCR(chemin)
    return [txt.strip() for _, txt, score in (resultat or []) if score >= 0.6 and len(txt.strip()) >= 3]


def traiter_image(source, fichier, dossier=ASSETS):
    """Recadre en 16:9 et écrit les trois fichiers du site : .jpg (secours),
    .webp (1600 px) et -800.webp (mobile). Renvoie les poids en octets."""
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(source)).convert('RGB')
    w, h = im.size
    if w / h < 1.2:
        raise PhotoErreur("l'image doit être au format paysage (reçu %d×%d)" % (w, h))
    cible = LARGEUR / HAUTEUR
    if w / h > cible:
        nw = round(h * cible)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w / cible)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    if im.size[0] < 1000:
        raise PhotoErreur('image trop petite (%d×%d)' % im.size)
    grand = im.resize((LARGEUR, HAUTEUR), Image.LANCZOS)
    petit = im.resize((800, 450), Image.LANCZOS)
    base = os.path.join(dossier, fichier)
    grand.save(base + '.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
    grand.save(base + '.webp', 'WEBP', quality=80, method=6)
    petit.save(base + '-800.webp', 'WEBP', quality=80, method=6)
    return {ext: os.path.getsize(base + ext) for ext in ('.jpg', '.webp', '-800.webp')}
