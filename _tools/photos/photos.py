#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Automatisation « une photo par page » : commandes.

Le GPT « Photos WebAutonomos » (ChatGPT, abonnement) génère les photos ; le VPS
fait le reste par serveur.py. Ces commandes servent au VPS et au Mac :

    python3 _tools/photos/photos.py inventaire   # met la file à jour (sujets.json)
    python3 _tools/photos/photos.py statut       # avancement et prochains sujets
    python3 _tools/photos/photos.py prompt ID [maquette]   # prompt que recevra ChatGPT
    python3 _tools/photos/photos.py essai        # teste la position sur toutes les pages, sans rien écrire
    python3 _tools/photos/photos.py appliquer ID IMAGE TEXTES.json [maquette]   # pose une image à la main
    python3 _tools/photos/photos.py reappliquer  # remet les photos effacées par une régénération
    python3 _tools/photos/photos.py annuler ID [maquette]  # retire l'image d'un sujet partout, la remet en file
    python3 _tools/photos/photos.py verifier     # chaque photo prévue est en place, une seule fois
    python3 _tools/photos/photos.py nuit         # VPS : inventaire + réapplication + contrôle + push

Un sujet = une photo, partagée par les versions linguistiques d'une même page.
Sont exclus : l'accueil SPA (index.html, hors automatisation), les pages
légales, et jusqu'à leur date les pages gelées par pages.json (mesure SEO).
"""

import datetime
import glob
import html as _html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import photos_lib as L  # noqa: E402

BASE = 'https://webautonomos.es'
PAGES_JSON = os.path.join(L.ROOT, '_tools', 'seo_pipeline', 'pages.json')
EXCLUES = {'index.html', 'aviso-legal/index.html', 'privacidad/index.html', 'cookies/index.html'}
LANGUES = ('es', 'val', 'en', 'fr')
NOMS_LANGUES = {'es': 'espagnol', 'val': 'valencien (catalan de Valence)',
                'en': 'anglais britannique', 'fr': 'français'}

# Pages hors blog regroupées par photo (29/09/2026). Un groupe = une photo.
# (id, priorité, marché visuel, santé, pages — la première donne l'URL et le titre)
GROUPES = [
    ('page-tarifs', 10, 'europe', False, ['fr/tarifs.html', 'en/pricing.html', 'precios.html']),
    ('page-comparatifs', 11, 'europe', False, ['mejores-creadores-paginas-web-autonomos.html',
                                               'fr/meilleurs-createurs-de-sites-pour-independants.html',
                                               'en/best-website-builders-for-freelancers-in-spain.html']),
    ('page-services', 12, 'europe', False, ['servicios.html', 'fr/prestations.html', 'en/services.html']),
    ('metier-therapeute', 20, 'europe', True, ['fr/site-internet-psychologue-therapeute.html',
                                               'en/website-for-therapists-in-spain.html']),
    ('metier-kine', 21, 'europe', True, ['fr/site-internet-kinesitherapeute.html',
                                         'en/website-for-physiotherapists-in-spain.html']),
    ('metier-kine-uk', 22, 'uk', True, ['en/physiotherapy-website-design.html']),
    ('metier-dentiste', 23, 'europe', True, ['fr/site-internet-dentiste.html',
                                             'en/website-for-dentists-in-spain.html']),
    ('metier-dentiste-uk', 24, 'uk', True, ['en/dental-website-design.html']),
    ('metier-menuisier', 25, 'europe', False, ['fr/site-internet-menuisier.html',
                                               'en/website-for-carpenters-in-spain.html']),
    ('metier-plombier', 26, 'europe', False, ['fr/site-internet-plombier.html',
                                              'en/website-for-plumbers-in-spain.html', 'demo-fontanero.html']),
    ('metier-plombier-uk', 27, 'uk', False, ['en/web-design-for-plumbers.html']),
    ('metier-electricien', 28, 'europe', False, ['fr/site-internet-electricien.html',
                                                 'en/website-for-electricians-in-spain.html', 'demo-electricista.html']),
    ('metier-electricien-uk', 29, 'uk', False, ['en/web-design-for-electricians.html']),
    ('metier-artisan', 30, 'europe', False, ['fr/site-internet-artisan.html', 'en/website-for-builders-in-spain.html']),
    ('metier-artisan-uk', 31, 'uk', False, ['en/web-design-for-tradesmen.html']),
    ('page-accueils', 32, 'europe', False, ['fr/index.html', 'en/index.html']),
    ('page-demande-demo', 33, 'europe', False, ['demandez-votre-demo.html', 'get-your-demo.html']),
    ('page-expatries', 34, 'es', False, ['fr/site-internet-francophones-espagne.html',
                                         'en/web-design-for-expats-in-spain.html']),
    ('page-fonctionnement', 35, 'europe', False, ['como-funciona.html', 'fr/comment-ca-marche.html', 'en/how.html']),
    ('page-questions', 36, 'europe', False, ['preguntas.html', 'fr/questions.html', 'en/faq.html']),
    ('page-contact', 37, 'europe', False, ['contacto.html', 'fr/contact.html', 'en/contact.html']),
    ('page-diagnostic', 38, 'europe', False, ['diagnostico-automatizacion/index.html',
                                              'fr/diagnostic-automatisation/index.html',
                                              'en/automation-diagnostic/index.html']),
    ('page-visibilite-ia', 39, 'europe', False, ['visibilidad-ia/index.html', 'fr/visibilite-ia/index.html',
                                                 'en/ai-visibility/index.html']),
    ('page-marketing', 40, 'es', False, ['marketing.html']),
    ('page-blog', 41, 'europe', False, ['blog/index.html']),
]

# Articles français sans hreflang : rattachés à la main à leur article (id SPA).
ORPHELINS_SANS_HREFLANG = {'blog/fr/reservation-en-ligne-pour-independants.html': 60}

MARCHES = {
    'europe': "un décor d'Europe du Sud crédible aussi bien en France qu'en Espagne, sans détail propre à un pays",
    'es': "un décor espagnol de la Comunidad Valenciana (Valence, Alicante)",
    'fr': "un décor français",
    'uk': "un décor britannique (Royaume-Uni : intérieurs, fenêtres et prises électriques britanniques si elles sont visibles)",
}

CONSIGNES_TEXTES = (
    "Pour chaque langue de « langues », rédige dans cette langue : "
    "un texte alternatif « alt » de 80 à 125 caractères qui décrit factuellement ce que montre la photo "
    "(sans commencer par « photo de » ni « image de ») ; "
    "une légende « legende » de 60 à 110 caractères, utile au lecteur de la page. "
    "Ne présente jamais les personnes comme des clients, des patients ou un cas réel ; "
    "pas de chiffre, pas de promesse, pas de nom de marque. "
    "Langues : es = espagnol, val = valencien, en = anglais britannique, fr = français (vouvoiement si besoin)."
)


# --------------------------------------------------------------------------
# Lecture des pages
# --------------------------------------------------------------------------

def lire(rel):
    with open(os.path.join(L.ROOT, rel), encoding='utf-8', errors='ignore') as fh:
        return fh.read()


def texte(fragment):
    t = re.sub(r'<[^>]+>', ' ', fragment)
    t = re.sub(r'\s+', ' ', _html.unescape(t)).strip()
    return re.sub(r'\s+([,.])', r'\1', t)


def a_une_image(h):
    corps = re.sub(r'<script\b.*?</script>', '', h, flags=re.S | re.I)
    return re.search(r'<img\b', corps, re.I) is not None


def titre_page(h):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    if m and texte(m.group(1)):
        return texte(m.group(1))
    m = re.search(r'<title>(.*?)</title>', h, re.S)
    return texte(m.group(1)).split('|')[0].strip() if m else ''


def resume_page(h, n=380):
    """Introduction de la page, pour situer ChatGPT."""
    for motif in (L.INTRO_ARTICLE + r'(.*?)</p>', r'<p class="lede"[^>]*>(.*?)</p>',
                  r'</h1>.*?<p[^>]*>(.*?)</p>'):
        m = re.search(motif, h, re.S)
        if m and len(texte(m.group(1))) > 40:
            t = texte(m.group(1))
            return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'
    return ''


def url_de(rel):
    p = rel[:-len('index.html')] if rel.endswith('index.html') else rel[:-len('.html')]
    return BASE + '/' + p


def langue_de(rel):
    for lg in ('fr', 'en', 'val'):
        if rel.startswith(lg + '/') or rel.startswith('blog/%s/' % lg):
            return lg
    return 'es'


def gels():
    """Pages gelées par le circuit SEO : pas de photo avant le lendemain de la fin du gel."""
    out = {}
    try:
        pages = json.load(open(PAGES_JSON, encoding='utf-8'))['pages']
    except (OSError, KeyError, ValueError):
        return out
    for x in pages:
        m = re.match(r'gele_jusqu_au_(\d{4}-\d{2}-\d{2})', x.get('statut') or '')
        if m and x.get('fichier'):
            fin = datetime.date.fromisoformat(m.group(1)) + datetime.timedelta(days=1)
            out[x['fichier']] = fin.isoformat()
    return out


# --------------------------------------------------------------------------
# Inventaire
# --------------------------------------------------------------------------

def _page(rel, gel, spa=None):
    p = {'html': rel, 'lang': langue_de(rel), 'url': url_de(rel)}
    if spa:
        p['spa'] = spa
    if rel in gel:
        p['pas_avant'] = gel[rel]
    return p


def _a_traiter(pages, sid, poses):
    """Pages qui reviennent au sujet `sid` : sans image et sans photo prévue,
    ou déjà illustrées par ce même sujet (pour pouvoir refaire la photo)."""
    out = []
    for p in pages:
        cfg = poses.get(p['html'])
        if cfg is not None:
            if cfg.get('sujet') == sid:
                out.append(p)
        elif not a_une_image(lire(p['html'])):
            out.append(p)
    return out


def _sujets_articles(gel, poses):
    sys.path.insert(0, os.path.join(L.ROOT, '_tools'))
    import generate_spa_articles as G
    t = G.load_translations()
    par_id = {}
    for lg in LANGUES:
        for a in t[lg]['blog']['articles']:
            par_id.setdefault(a['id'], {})[lg] = a
    # Articles français présents sur le disque sans figurer dans les données :
    # on les rattache par leur hreflang espagnol.
    url_es = {BASE + '/blog/' + d['es']['slug']: i for i, d in par_id.items() if 'es' in d}
    connus_fr = {d['fr']['slug'] for d in par_id.values() if 'fr' in d}
    orphelins = {i: rel for rel, i in ORPHELINS_SANS_HREFLANG.items()
                 if os.path.isfile(os.path.join(L.ROOT, rel))}
    for f in sorted(glob.glob(os.path.join(L.ROOT, 'blog', 'fr', '*.html'))):
        rel = L.cle_page(f)
        if 'fr/' + os.path.basename(f)[:-5] in connus_fr:
            continue
        m = re.search(r'hreflang="es" href="([^"]+)"', lire(rel))
        if m and m.group(1) in url_es:
            orphelins[url_es[m.group(1)]] = rel
    out = []
    for rang, (i, d) in enumerate(sorted(par_id.items(), key=lambda kv: kv[0])):
        pages = []
        for lg in LANGUES:
            if lg in d:
                rel = 'blog/%s.html' % d[lg]['slug']
                if os.path.isfile(os.path.join(L.ROOT, rel)):
                    pages.append(_page(rel, gel, spa=d[lg]['slug']))
            elif lg == 'fr' and i in orphelins:
                pages.append(_page(orphelins[i], gel))
        sid = 'art-%02d' % i
        a_traiter = _a_traiter(pages, sid, poses)
        if not a_traiter:
            continue
        principal = d.get('es') or next(iter(d.values()))
        h = lire(pages[0]['html'])
        out.append({'id': sid, 'type': 'article', 'priorite': 100 + rang,
                    'titre': principal['title'], 'url': pages[0]['url'], 'resume': resume_page(h),
                    'marche': 'europe', 'sante': False, 'pages': a_traiter})
    return out


def _sujets_file():
    """Articles encore en file d'attente : la photo part avec eux à la publication.
    Une fois publiés, ils redeviennent des articles ordinaires (art-NN)."""
    out = []
    files = [json.load(open(f, encoding='utf-8')) | {'_f': f}
             for f in glob.glob(os.path.join(L.ROOT, '_tools', 'queue', '*.json'))]
    for rang, d in enumerate(sorted(files, key=lambda x: (x['publish_date'], x['slug']))):
        f = d.pop('_f')
        pages = []
        for lg in LANGUES:
            if lg not in d:
                continue
            slug = d[lg].get('slug') or d.get('slug')
            pages.append({'html': 'blog/%s/%s.html' % (lg, slug), 'lang': lg,
                          'url': '%s/blog/%s/%s' % (BASE, lg, slug), 'spa': '%s/%s' % (lg, slug)})
        intro = next((b.get('text') for b in d['es']['content'] if b.get('type') == 'intro'), '')
        out.append({'id': 'file-' + d['slug'], 'type': 'file', 'publication': d['publish_date'],
                    'file': L.cle_page(f), 'priorite': 1 + rang,
                    'titre': d['es']['title'], 'url': pages[0]['url'],
                    'resume': texte(intro)[:380], 'marche': 'europe', 'sante': False, 'pages': pages})
    return out


def _sujets_pages(gel, poses):
    out, vus = [], set()
    for gid, prio, marche, sante, rels in GROUPES:
        vus.update(rels)
        existantes = [_page(rel, gel) for rel in rels if os.path.isfile(os.path.join(L.ROOT, rel))]
        pages = _a_traiter(existantes, gid, poses)
        if not pages:
            continue
        h = lire(pages[0]['html'])
        out.append({'id': gid, 'type': 'page', 'priorite': prio, 'titre': titre_page(h),
                    'url': pages[0]['url'], 'resume': resume_page(h), 'marche': marche,
                    'sante': sante, 'pages': pages})
    # Pages du sitemap sans image et sans groupe (nouvelles pages) : un sujet chacune.
    sm = lire('sitemap.xml')
    for loc in sorted(set(re.findall(r'<loc>([^<]+)</loc>', sm))):
        chemin = loc[len(BASE):].strip('/')
        if not chemin or chemin == 'blog' or chemin.startswith('blog/'):
            continue
        for rel in (chemin + '.html', chemin + '/index.html'):
            if os.path.isfile(os.path.join(L.ROOT, rel)):
                break
        else:
            continue
        if rel in vus or rel in EXCLUES:
            continue
        sid = 'page-' + re.sub(r'[^a-z0-9]+', '-', chemin.lower()).strip('-')
        pages = _a_traiter([_page(rel, gel)], sid, poses)
        if not pages:
            continue
        h = lire(rel)
        out.append({'id': sid, 'type': 'page', 'priorite': 60, 'titre': titre_page(h), 'url': url_de(rel),
                    'resume': resume_page(h), 'marche': 'europe', 'sante': False, 'pages': pages})
    return out


GARDER = ('statut', 'scene', 'fichier', 'v', 'fait_le', 'textes', 'priorite_manuelle', 'note',
          'marche_force', 'sante_force', 'pages_en_plus', 'site', 'maquette')


def inventaire(ecrire=True):
    """Recalcule la file et fusionne avec sujets.json (statut, scène, fichier conservés)."""
    ancien = L.lire_json(L.SUJETS_JSON, {'sujets': []})
    par_id = {s['id']: s for s in ancien.get('sujets', [])}
    poses = L.images()
    gel = gels()
    frais = _sujets_file() + _sujets_pages(gel, poses) + _sujets_articles(gel, poses)
    ids_frais = {s['id'] for s in frais}
    # Un article de la file publié change d'identifiant (file-… -> art-NN) :
    # sa scène et son nom de fichier le suivent, retrouvés par ses pages.
    orphelins = {p['html']: a for a in par_id.values() if a['id'] not in ids_frais
                 and a.get('statut') == 'pret' for p in a.get('pages', [])}
    sujets, ajoutes = [], []
    for s in frais:
        a = par_id.pop(s['id'], None)
        if a is None:
            a = next((orphelins[p['html']] for p in s['pages'] if p['html'] in orphelins), None)
            if a is not None:
                par_id.pop(a['id'], None)
                a = {k: v for k, v in a.items() if k in ('scene', 'fichier', 'note', 'statut', 'site', 'maquette')}
        if a:
            for k in GARDER:
                if k in a:
                    s[k] = a[k]
            if 'priorite_manuelle' in s:
                s['priorite'] = s['priorite_manuelle']
            if 'marche_force' in s:
                s['marche'] = s['marche_force']
            if 'sante_force' in s:
                s['sante'] = s['sante_force']
            # pages ajoutées à la main (ex. version déjà illustrée avant l'automatisation)
            connues = {p['html'] for p in s['pages']}
            s['pages'] += [p for p in s.get('pages_en_plus', []) if p['html'] not in connues]
        else:
            s['statut'] = 'pret'
            ajoutes.append(s['id'])
        s.setdefault('fichier', 'photo-' + s['id'])
        suivi(s, 'maquette')
        sujets.append(s)
    # Sujets sortis de l'inventaire (article de la file publié, page supprimée) :
    # conservés s'ils ont une photo, pour pouvoir la refaire.
    for s in par_id.values():
        if s.get('statut') == 'fait':
            s['publie'] = True
            sujets.append(s)
    sujets.sort(key=lambda s: (s['priorite'], s['id']))
    data = {'_lisez_moi': [
        "File de l'automatisation « une photo par page » (voir _tools/photos/LISEZMOI.md).",
        "statut : pret = à générer ; fait = photo en ligne ; saute = laissé de côté par Angelino.",
        "scene : ce que la photo doit montrer (sinon ChatGPT choisit). fichier : nom des fichiers dans assets/.",
        "pages[].pas_avant : page gelée pour une mesure SEO, la photo n'y est posée qu'à partir de cette date."],
        'sujets': sujets}
    if ecrire:
        L.ecrire_json(L.SUJETS_JSON, data)
    return data, ajoutes


def charger():
    return L.lire_json(L.SUJETS_JSON, {'sujets': []})


def trouver(data, sid):
    for s in data['sujets']:
        if s['id'] == sid:
            return s
    raise L.PhotoErreur('sujet inconnu : %s' % sid)


def langues(s):
    vues = []
    for p in s['pages']:
        if p['lang'] not in vues:
            vues.append(p['lang'])
    return vues


def a_des_pages_actives(s, jour=None):
    if s.get('type') == 'file' and not s.get('publie'):
        return True
    return any(L.active(p, jour) for p in s['pages'])


def construire_prompt(s):
    """Prompt purement visuel. Essais du 29/09 : avec l'URL, le résumé de la page
    et une longue liste d'interdits dans le prompt, ChatGPT a ressorti deux fois
    une ancienne image du compte au lieu d'en générer une ; une phrase courte et
    visuelle donne une photo neuve. L'URL et le résumé voyagent à côté
    (charge_utile), pas dans le texte donné à la génération d'image."""
    if s.get('scene'):
        scene = s['scene'].rstrip('.')
    else:
        scene = ("une scène concrète et vivante du travail d'un professionnel indépendant, sur le thème « %s », "
                 "sans ordinateur portable ni poignée de main" % s['titre'])
    marche = MARCHES.get(s.get('marche'), MARCHES['europe'])
    interdits = ("Aucun texte, aucune lettre, aucun chiffre, aucun logo ; aucun papier, carte, écran, enseigne ni "
                 "étiquette lisibles ; personne ne regarde l'objectif")
    if s.get('sante'):
        interdits += " ; aucun patient reconnaissable, pas d'avant/après, pas de soin en gros plan"
    return ("Photographie réaliste, format paysage : %s.\nDécor : %s.\nLumière naturelle, rendu de photographie "
            "documentaire, couleurs naturelles.\n%s." % (scene, marche, interdits))


# Deuxième image (30/09/2026) : maquette MacBook + smartphone qui montre le site
# de l'activité de la page (celle de sa photo). Écrans sans texte lisible
# (barres grises) ; jamais présentée comme le site d'un vrai client.
SUPPORTS = ("un bureau en bois clair près d'une fenêtre", "une table blanche lumineuse",
            "un comptoir en bois de boutique", "une table de terrasse de café, en plein jour")

CONSIGNES_TEXTES_MAQUETTE = (
    "Pour chaque langue de « langues », rédige dans cette langue : un texte alternatif « alt » de 80 à 125 "
    "caractères qui décrit l'ordinateur portable et le smartphone et ce qu'affichent leurs écrans (le site de "
    "l'activité, en version ordinateur et mobile), sans commencer par « photo de » ni « image de » ; une légende "
    "« legende » de 50 à 100 caractères qui commence par « Exemple de site » (es : « Ejemplo de web », "
    "val : « Exemple de web », en : « Example website »). Jamais le site d'un client réel ; pas de nom de marque."
)


def _site(s):
    return s.get('site') or ("d'une activité liée au thème « %s »" % s['titre'])


def construire_prompt_maquette(s):
    """Même forme que le prompt des photos : il commence par « Photographie
    réaliste », que le GPT reconnaît, et reste purement visuel."""
    support = SUPPORTS[sum(map(ord, s['id'])) % len(SUPPORTS)]
    return ("Photographie réaliste, format paysage : un ordinateur portable de style MacBook ouvert et un "
            "smartphone posés côte à côte sur %s ; les deux écrans affichent le site web %s, avec une grande "
            "photo, des blocs de couleur et des boutons, en version ordinateur et en version mobile.\n"
            "Lumière naturelle, rendu de photographie produit, couleurs naturelles.\n"
            "Aucun logo ni marque sur les appareils ; aucun texte lisible sur les écrans : les titres et les "
            "paragraphes sont de simples barres grises." % (support, _site(s)))


def suivi(s, genre):
    """Objet qui porte statut, version, fichier et textes d'une image : le sujet
    lui-même pour la photo, son sous-objet « maquette » pour la maquette."""
    if genre == 'maquette':
        return s.setdefault('maquette', {'statut': 'pret', 'fichier': s['fichier'] + '-maquette'})
    return s


def charge_utile(s, restants, genre='photo'):
    maq = genre == 'maquette'
    return {'sujet_id': s['id'], 'genre': genre, 'titre': ('Maquette — ' if maq else '') + s['titre'],
            'url': s['url'], 'resume': s.get('resume') or '',
            'prompt': construire_prompt_maquette(s) if maq else construire_prompt(s),
            'langues': langues(s), 'consignes_textes': CONSIGNES_TEXTES_MAQUETTE if maq else CONSIGNES_TEXTES,
            'restants': restants}


# --------------------------------------------------------------------------
# Pose
# --------------------------------------------------------------------------

def _propre(t, n):
    t = re.sub(r'\s+', ' ', (t or '')).strip().strip('"«»“”').strip()
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0]


def normaliser_textes(textes):
    """[{langue, alt, legende}] ou {langue: {alt, legende}} -> {langue: {alt, legende}}."""
    out = {}
    if isinstance(textes, dict):
        textes = [dict(v, langue=k) for k, v in textes.items()]
    for t in textes or []:
        lg = (t.get('langue') or t.get('lang') or '').strip().lower()
        lg = {'ca': 'val', 'va': 'val', 'valencien': 'val', 'es-es': 'es', 'en-gb': 'en', 'fr-fr': 'fr'}.get(lg, lg)
        if lg in LANGUES:
            out[lg] = {'alt': _propre(t.get('alt'), 160), 'legende': _propre(t.get('legende'), 180)}
    return out


def _valider_index(nouveau):
    """L'objet translations de index.html doit rester lisible par node."""
    sys.path.insert(0, os.path.join(L.ROOT, '_tools'))
    import generate_spa_articles as G
    G.load_translations()  # sort du programme si l'objet est illisible
    return True


def _ecrire_index(index, index0):
    with open(L.INDEX, 'w', encoding='utf-8') as fh:
        fh.write(index)
    try:
        _valider_index(index)
    except SystemExit:
        with open(L.INDEX, 'w', encoding='utf-8') as fh:
            fh.write(index0)
        raise L.PhotoErreur('index.html serait devenu illisible : rien écrit')


def appliquer(sid, image, textes, jour=None, genre='photo'):
    """Traite l'image et la pose sur toutes les pages du sujet : la photo après
    l'introduction, la maquette (genre='maquette') au milieu de la page.
    Renvoie les fichiers modifiés (relatifs au dépôt)."""
    maq = genre == 'maquette'
    data = charger()
    s = trouver(data, sid)
    obj = suivi(s, genre)
    textes = normaliser_textes(textes)
    manque = [lg for lg in langues(s) if not textes.get(lg, {}).get('alt')]
    if manque:
        raise L.PhotoErreur('texte alternatif manquant pour : %s' % ', '.join(manque))
    v = int(obj.get('v') or 0) + 1
    fichier = obj['fichier']
    L.traiter_image(image, fichier)
    modifies = {'assets/%s%s' % (fichier, ext) for ext in ('.jpg', '.webp', '-800.webp')}
    imgs = L.lire_json(L.IMAGES_JSON, {})
    imgs['_lisez_moi'] = ("Images de chaque page (clé = fichier HTML) : « pages » pour la photo, « maquettes » "
                          "pour la maquette MacBook + smartphone. Écrit par _tools/photos/photos.py ; lu par les "
                          "générateurs via photos_lib.injecter.")
    pages_cfg = imgs.setdefault('maquettes' if maq else 'pages', {})
    index0 = index = open(L.INDEX, encoding='utf-8').read()
    file_cfg = {}
    for p in s['pages']:
        t = textes[p['lang']]
        cfg = {'sujet': sid, 'fichier': fichier, 'largeur': L.LARGEUR, 'hauteur': L.HAUTEUR,
               'v': v, 'alt': t['alt'], 'legende': t['legende']}
        if p.get('pas_avant'):
            cfg['pas_avant'] = p['pas_avant']
        pages_cfg[p['html']] = cfg
        if s.get('type') == 'file' and not s.get('publie') and os.path.isfile(os.path.join(L.ROOT, s['file'])):
            file_cfg[p['lang']] = cfg
            continue
        if not L.active(cfg, jour):
            continue
        if p.get('spa') and index.count('slug:"%s"' % p['spa']) == 1:
            index = L.poser_bloc_spa(index, p['spa'], cfg, milieu=maq)
        chemin = os.path.join(L.ROOT, p['html'])
        if os.path.isfile(chemin):
            h = lire(p['html'])
            h2 = (L.injecter(p['html'], h, None, jour, maquette=cfg) if maq
                  else L.injecter(p['html'], h, cfg, jour))
            if L.compte_photo(h2, cfg) != 1:
                raise L.PhotoErreur('%s mal posée dans %s' % (genre, p['html']))
            if h2 != h:
                with open(chemin, 'w', encoding='utf-8') as fh:
                    fh.write(h2)
                modifies.add(p['html'])
    if file_cfg:
        L.poser_bloc_file(os.path.join(L.ROOT, s['file']), file_cfg, milieu=maq)
        modifies.add(s['file'])
    if index != index0:
        _ecrire_index(index, index0)
        modifies.add('index.html')
    obj.update(statut='fait', v=v, fait_le=datetime.datetime.now().isoformat(timespec='seconds'), textes=textes)
    L.ecrire_json(L.IMAGES_JSON, imgs)
    L.ecrire_json(L.SUJETS_JSON, data)
    modifies |= {'_tools/photos/images.json', '_tools/photos/sujets.json'}
    return sorted(modifies)


def annuler(sid, genre='photo'):
    """Retire une image d'un sujet partout (pages, données des articles, file
    d'attente, fichiers de assets/) et la remet en « pret ». La version est
    gardée : la prochaine prendra v+1, ce qui contourne les caches."""
    maq = genre == 'maquette'
    data = charger()
    s = trouver(data, sid)
    obj = suivi(s, genre)
    imgs = L.lire_json(L.IMAGES_JSON, {})
    pages_cfg = imgs.setdefault('maquettes' if maq else 'pages', {})
    fichier = obj['fichier']
    marques = (L.MAQ_DEBUT, L.MAQ_FIN) if maq else (L.MARQUE_DEBUT, L.MARQUE_FIN)
    modifies = set()
    index0 = index = open(L.INDEX, encoding='utf-8').read()
    for p in s['pages']:
        cfg = pages_cfg.pop(p['html'], None) or {'fichier': fichier}
        if p.get('spa') and index.count('slug:"%s"' % p['spa']) == 1:
            index = L.retirer_bloc_spa(index, p['spa'], cfg)
        chemin = os.path.join(L.ROOT, p['html'])
        if os.path.isfile(chemin):
            h = lire(p['html'])
            h2 = L._retirer(h, cfg, marques)
            if h2 != h:
                with open(chemin, 'w', encoding='utf-8') as fh:
                    fh.write(h2)
                modifies.add(p['html'])
    if s.get('file') and os.path.isfile(os.path.join(L.ROOT, s['file'])):
        if L.retirer_bloc_file(os.path.join(L.ROOT, s['file']), fichier):
            modifies.add(s['file'])
    if index != index0:
        _ecrire_index(index, index0)
        modifies.add('index.html')
    for ext in ('.jpg', '.webp', '-800.webp'):
        f = os.path.join(L.ASSETS, fichier + ext)
        if os.path.isfile(f):
            os.remove(f)
            modifies.add('assets/%s%s' % (fichier, ext))
    obj['statut'] = 'pret'
    for k in ('fait_le', 'textes'):
        obj.pop(k, None)
    L.ecrire_json(L.IMAGES_JSON, imgs)
    L.ecrire_json(L.SUJETS_JSON, data)
    return sorted(modifies | {'_tools/photos/images.json', '_tools/photos/sujets.json'})


def reappliquer(jour=None):
    """Remet chaque image prévue (photo et maquette) là où elle manque : page
    régénérée, page gelée arrivée à sa date, article publié depuis."""
    photos, maqs = L.images(), L.maquettes()
    data = charger()
    spa = {p['html']: p['spa'] for s in data['sujets'] for p in s['pages'] if p.get('spa')}
    index0 = index = open(L.INDEX, encoding='utf-8').read()
    modifies = set()
    for rel in sorted(set(photos) | set(maqs)):
        for cfg, milieu in ((photos.get(rel), False), (maqs.get(rel), True)):
            if not cfg or not L.active(cfg, jour):
                continue
            if not os.path.isfile(os.path.join(L.ASSETS, cfg['fichier'] + '.jpg')):
                print('  ! fichiers absents pour %s (%s)' % (rel, cfg['fichier']))
            slug = spa.get(rel)
            if slug and index.count('slug:"%s"' % slug) == 1 and not L.a_bloc_image(index, slug, cfg):
                index = L.poser_bloc_spa(index, slug, cfg, milieu=milieu)
        chemin = os.path.join(L.ROOT, rel)
        if os.path.isfile(chemin):
            h = lire(rel)
            h2 = L.injecter(rel, h, jour=jour)
            if h2 != h:
                with open(chemin, 'w', encoding='utf-8') as fh:
                    fh.write(h2)
                modifies.add(rel)
    if index != index0:
        _ecrire_index(index, index0)
        modifies.add('index.html')
    return sorted(modifies)


def verifier(jour=None):
    problemes = []
    for nom, dico in (('photo', L.images()), ('maquette', L.maquettes())):
        for rel, cfg in sorted(dico.items()):
            if not L.active(cfg, jour):
                continue
            for ext in ('.jpg', '.webp', '-800.webp'):
                if not os.path.isfile(os.path.join(L.ASSETS, cfg['fichier'] + ext)):
                    problemes.append('%s : assets/%s%s absent' % (rel, cfg['fichier'], ext))
            if os.path.isfile(os.path.join(L.ROOT, rel)):
                n = L.compte_photo(lire(rel), cfg)
                if n != 1:
                    problemes.append('%s : %s présente %d fois' % (rel, nom, n))
    return problemes


# --------------------------------------------------------------------------
# Git (dépôt du robot, sur le VPS uniquement)
# --------------------------------------------------------------------------

def _git(*args):
    return subprocess.run(['git', '-C', L.ROOT] + list(args), capture_output=True, text=True)


def robot():
    return os.environ.get('PHOTOS_ROBOT') == '1'


def synchro():
    """Repart de origin/main : le clone du robot ne garde jamais rien en local."""
    if not robot():
        return
    for args in (('fetch', '-q', 'origin'), ('reset', '-q', '--hard', 'origin/main')):
        r = _git(*args)
        if r.returncode:
            raise L.PhotoErreur('git %s : %s' % (args[0], r.stderr.strip()[:300]))


def publier(fichiers, message):
    """Commit + push. False si le push est refusé (quelqu'un a poussé entre-temps)."""
    if not robot():
        return True
    _git('add', '-A', '-f', '--', *fichiers)  # -A : enregistre aussi les fichiers supprimés
    if not _git('diff', '--cached', '--quiet').returncode:
        return True
    r = _git('-c', 'user.name=photos-bot', '-c', 'user.email=photos-bot@users.noreply.github.com',
             'commit', '-q', '-m', message)
    if r.returncode:
        raise L.PhotoErreur('git commit : %s' % (r.stderr or r.stdout).strip()[:300])
    r = _git('push', '-q', 'origin', 'HEAD:main')
    return r.returncode == 0


def en_boucle(operation, message, essais=3):
    """synchro -> opération -> push, recommencé si quelqu'un a poussé entre-temps."""
    for _ in range(essais):
        synchro()
        fichiers = operation()
        if not fichiers:
            return []
        if publier(fichiers, message):
            return fichiers
    raise L.PhotoErreur('push refusé %d fois de suite' % essais)


# --------------------------------------------------------------------------
# Commandes
# --------------------------------------------------------------------------

def cmd_statut():
    data = charger()
    pages = sum(len(s['pages']) for s in data['sujets'])
    print('Sujets : %d — %d pages' % (len(data['sujets']), pages))
    for genre in ('photo', 'maquette'):
        compte = {}
        for s in data['sujets']:
            st = suivi(s, genre).get('statut')
            compte[st] = compte.get(st, 0) + 1
        print('  %-9s %s' % (genre + 's', ', '.join('%s %d' % kv for kv in sorted(compte.items()))))
    print('Prochains :')
    prochains = [(s, 'photo') for s in data['sujets'] if s.get('statut') == 'pret']
    prochains += [(s, 'maquette') for s in data['sujets'] if suivi(s, 'maquette').get('statut') == 'pret']
    for s, genre in prochains[:12]:
        print('  %-9s %-24s %2d page(s)  %s' % (genre, s['id'], len(s['pages']), s['titre'][:62]))


def cmd_essai(genre='photo'):
    """Pose une image fictive (photo ou maquette) sur chaque page de la file,
    sans rien écrire, et montre où elle tombe."""
    data = charger()
    faux = {'fichier': 'essai-' + genre, 'alt': 'essai', 'legende': 'essai', 'v': 1}
    erreurs = 0
    for s in data['sujets']:
        for p in s['pages']:
            chemin = os.path.join(L.ROOT, p['html'])
            if not os.path.isfile(chemin):
                continue
            h = lire(p['html'])
            try:
                if genre == 'maquette':
                    base = L.injecter(p['html'], h, None, None, maquette={})  # photo déjà prévue
                    pos, gabarit, entre = L.point_milieu(base)
                    h2 = L.injecter(p['html'], h, None, None, maquette=faux)
                    apres = re.sub(r'<[^>]+>', ' ', base[pos:pos + 400])
                    repere = re.sub(r'\s+', ' ', apres).strip()[:55]
                else:
                    pos, gabarit, entre = L.point_insertion(L._retirer(h, faux))
                    h2 = L.injecter(p['html'], h, faux)
                    repere = re.sub(r'\s+', ' ', h[max(0, pos - 70):pos])[-55:]
                ok = (L.compte_photo(h2, faux) == 1 and h2.count('<figure') == h2.count('</figure>')
                      and len(h2) > len(h))
                print('%s %-9s %-58s %s' % ('ok' if ok else 'KO', gabarit + ('+' if entre else ''),
                                           p['html'][:58], repere))
                erreurs += not ok
            except L.PhotoErreur as e:
                print('KO %-68s %s' % (p['html'], e))
                erreurs += 1
    print('%d erreur(s)' % erreurs)
    return erreurs


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == 'inventaire':
        data, ajoutes = inventaire()
        print('%d sujets, %d nouveaux' % (len(data['sujets']), len(ajoutes)))
        cmd_statut()
    elif cmd == 'statut':
        cmd_statut()
    elif cmd == 'prompt':
        s = trouver(charger(), argv[1])
        print(construire_prompt_maquette(s) if argv[2:] == ['maquette'] else construire_prompt(s))
    elif cmd == 'essai':
        return 1 if cmd_essai('maquette' if argv[1:] == ['maquette'] else 'photo') else 0
    elif cmd == 'appliquer':
        textes = json.load(open(argv[3], encoding='utf-8'))
        genre = 'maquette' if argv[4:] == ['maquette'] else 'photo'
        for f in appliquer(argv[1], argv[2], textes, genre=genre):
            print('  modifié :', f)
    elif cmd == 'reappliquer':
        for f in reappliquer():
            print('  réappliqué :', f)
    elif cmd == 'annuler':
        sid, genre = argv[1], ('maquette' if argv[2:] == ['maquette'] else 'photo')
        for f in en_boucle(lambda: annuler(sid, genre),
                           'Photos auto : %s retirée (%s), remise en file' % (genre, sid)):
            print('  modifié :', f)
    elif cmd == 'verifier':
        pb = verifier()
        print('\n'.join(pb) if pb else 'toutes les photos prévues sont en place')
        return 1 if pb else 0
    elif cmd == 'nuit':
        def operation():
            inventaire()
            fichiers = set(reappliquer()) | {'_tools/photos/sujets.json'}
            pb = verifier()
            if pb:
                print('\n'.join(pb))
            return sorted(fichiers)
        print('publié :', en_boucle(operation, 'Photos auto : inventaire et réapplication'))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
