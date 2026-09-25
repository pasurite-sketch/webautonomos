#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôles automatiques (sans IA) du circuit SEO/GEO WebAutonomos.

Compare l'arbre de travail à un commit de base et bloque la publication si :
  - un fichier hors périmètre a été modifié ;
  - une page générée a été modifiée sans passer par son script ;
  - le HTML est déséquilibré, un JSON-LD est invalide, la FAQ visible et le
    JSON-LD FAQPage divergent ;
  - le title dépasse 580 px, il n'y a pas exactement un H1 ;
  - canonical, hreflang, bloc Trustpilot, formulaire, liens de démo ou prix
    ont été retirés ;
  - un nombre non autorisé, un pourcentage ou une expression interdite
    (VERITE.md §7 et §8) a été ajouté ;
  - des mots espagnols courants sont écrits sans accent.

Usage :
    python3 _tools/seo_pipeline/checks.py <slug> --base <commit> [--no-generators]
Sortie : JSON sur stdout ; code 0 si aucun blocage, 1 sinon.

Attention : le contrôle des générateurs fait `git add -A` puis relance les
scripts ; si un script modifie une page, la page est restaurée depuis l'index.
"""
import argparse, html as H, json, os, re, subprocess, sys, unicodedata

ROOT = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().strip()
P = os.path.join(ROOT, '_tools', 'seo_pipeline')
GENERATEURS_IDEMPOTENTS = ['_tools/build_lang_homes.py', '_tools/build_metier_pages.py',
                           '_tools/build_expat_pages.py']
DEMO_RE = re.compile(r'href="[^"]*(#pide-demo|/pide-tu-demo|/demandez-votre-demo|/get-your-demo)[^"]*"')
PRIX_RE = re.compile(r'(?<![\d,.])(15|349)\s?(€|euros?)|€\s?(15|349)(?![\d,])')
ACCENTS_ES = re.compile(r'\b(pagina|paginas|diseno|disenos|informacion|tambien|ademas|facil|faciles|rapido|rapida|'
                        r'telefono|movil|moviles|busqueda|busquedas|atencion|espana|codigo|articulo|articulos|'
                        r'pequena|pequenas|tecnico|tecnica|ubicacion|construccion|albanileria|carpinteria|banos|'
                        r'mas alla|despues|dificil|numero|unico|unica)\b')


def git(*a):
    return subprocess.check_output(['git', *a], cwd=ROOT).decode('utf-8', 'replace')


def lire_base(base, path):
    try:
        return git('show', f'{base}:{path}')
    except subprocess.CalledProcessError:
        return None


def texte_visible(s):
    s = re.sub(r'(?is)<(script|style|noscript|template)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?is)<!--.*?-->', ' ', s)
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', H.unescape(s)).strip()


def sans_accents(t):
    return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')


def largeur_title(t):
    try:
        from PIL import ImageFont
        for f in ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                  '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                  '/Library/Fonts/Arial.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf'):
            if os.path.exists(f):
                return round(ImageFont.truetype(f, 20).getlength(t)), 'px'
    except Exception:
        pass
    return len(t), 'caracteres'


# Milliers écrits à la française (« 2 000 »), à l'anglaise (« 2,000 ») ou à l'espagnole
# (« 2.000 ») : ramenés à « 2000 » des deux côtés de la comparaison (25/09 : faux
# positifs « 000 », « 500 », « 2,000 » sur /fr/prestations et /en/services).
MILLIERS = re.compile(r'(?<![\d.,])\d{1,3}(?:[ \u00a0\u202f.,]\d{3})+(?![\d])')


def sans_milliers(t):
    return MILLIERS.sub(lambda m: re.sub(r'[ \u00a0\u202f.,]', '', m.group(0)), t)


def verite():
    v = open(os.path.join(P, 'VERITE.md'), encoding='utf-8').read()
    blocs = re.findall(r'```\n(.*?)```', v, re.S)
    # §7 = premier bloc (chiffres), §8 = second bloc (interdits)
    nombres = set()
    for item in re.split(r',\s+|\n', blocs[0] if blocs else ''):
        item = item.strip()
        if not item:
            continue
        nombres.add(re.sub(r'\s', '', item))
        nombres.update(re.findall(r'\d[\d.,]*\d|\d', item))
        item_n = sans_milliers(item)
        nombres.add(re.sub(r'\s', '', item_n))
        nombres.update(re.findall(r'\d[\d.,]*\d|\d', item_n))
    interdits = [l.strip() for l in (blocs[1] if len(blocs) > 1 else '').splitlines() if l.strip()]
    return nombres, interdits


def compter(motif, texte, flags=re.I):
    return len(re.findall(motif, texte, flags))


def nombres_du_texte(t):
    toks = re.findall(r'\d[\d.,]*\d|\d', sans_milliers(t))
    out = {}
    for x in toks:
        x = x.rstrip('.,')
        out[x] = out.get(x, 0) + 1
    return out


def faq_visible(s):
    return [texte_visible(q) for q in re.findall(r'(?is)<summary[^>]*>(.*?)</summary>', s)]


def faq_jsonld(s):
    qs = []
    for m in re.findall(r'(?is)<script type="application/ld\+json">(.*?)</script>', s):
        try:
            d = json.loads(m)
        except Exception:
            continue
        items = d.get('@graph', [d]) if isinstance(d, dict) else d
        for it in items if isinstance(items, list) else [items]:
            if isinstance(it, dict) and it.get('@type') == 'FAQPage':
                qs += [q.get('name', '') for q in it.get('mainEntity', [])]
    return qs


def controler_html(path, base_s, new_s, lang, bloquants, avert, infos):
    nom = path
    # équilibre des balises : l'écart ouvrantes/fermantes ne doit pas changer
    for tag in ('div', 'section', 'details', 'ul', 'ol', 'table', 'form', 'main', 'article'):
        delta = lambda s: compter(rf'<{tag}\b', s) - compter(rf'</{tag}>', s)
        if base_s is not None and delta(new_s) != delta(base_s):
            bloquants.append(f'{nom} : balises <{tag}> déséquilibrées ({delta(base_s)} → {delta(new_s)})')
    # JSON-LD
    for i, m in enumerate(re.findall(r'(?is)<script type="application/ld\+json">(.*?)</script>', new_s)):
        try:
            json.loads(m)
        except Exception as e:
            bloquants.append(f'{nom} : JSON-LD n°{i + 1} invalide ({e})')
    # FAQ visible <-> FAQPage
    norm = lambda t: re.sub(r'[\s¿?¡!.,:;«»"]+', ' ', sans_accents(t).lower()).strip()
    visible = norm(texte_visible(new_s))
    for q in faq_jsonld(new_s):
        if norm(q) and norm(q) not in visible:
            bloquants.append(f'{nom} : question du JSON-LD FAQPage absente du texte visible : « {q[:80]} »')
    # title et H1
    t = re.search(r'(?is)<title>(.*?)</title>', new_s)
    if not t:
        bloquants.append(f'{nom} : pas de <title>')
    else:
        titre = H.unescape(t.group(1)).strip()
        w, unite = largeur_title(titre)
        infos.setdefault('titles', {})[nom] = f'{titre} ({w} {unite})'
        tb_ = re.search(r'(?is)<title>(.*?)</title>', base_s or '')
        inchange = tb_ is not None and H.unescape(tb_.group(1)).strip() == titre
        if (unite == 'px' and w > 580) or (unite == 'caracteres' and w > 60):
            (avert if inchange else bloquants).append(
                f'{nom} : title trop long ({w} {unite}){" — déjà le cas avant" if inchange else ""} : « {titre} »')
    n_h1 = compter(r'<h1\b', new_s)
    if n_h1 != 1:
        deja = base_s is not None and compter(r'<h1\b', base_s) == n_h1
        (avert if deja else bloquants).append(f'{nom} : {n_h1} balises <h1> (attendu : 1)'
                                              f'{" — déjà le cas avant" if deja else ""}')
    if base_s is None:
        return
    # éléments protégés
    for motif, libelle in ((r'<link rel="canonical"[^>]*>', 'canonical'),
                           (r'<link rel="alternate" hreflang[^>]*>', 'hreflang'),
                           (r'<div class="proof-num">[^<]*</div>', 'bloc Trustpilot')):
        a, b = re.findall(motif, base_s), re.findall(motif, new_s)
        if sorted(a) != sorted(b):
            bloquants.append(f'{nom} : {libelle} modifié ou supprimé')
    if compter(r'<form\b', new_s) < compter(r'<form\b', base_s):
        bloquants.append(f'{nom} : formulaire supprimé')
    if len(DEMO_RE.findall(new_s)) < len(DEMO_RE.findall(base_s)):
        bloquants.append(f'{nom} : liens vers la démo en baisse '
                         f'({len(DEMO_RE.findall(base_s))} → {len(DEMO_RE.findall(new_s))})')
    tb, tn = texte_visible(base_s), texte_visible(new_s)
    if len(PRIX_RE.findall(tn)) < len(PRIX_RE.findall(tb)):
        avert.append(f'{nom} : moins de mentions du prix (15 € / 349 €) qu\'avant')
    if not PRIX_RE.search(tn) and PRIX_RE.search(tb):
        bloquants.append(f'{nom} : plus aucune mention du prix')
    infos.setdefault('mots', {})[nom] = [len(tb.split()), len(tn.split())]
    # nombres ajoutés : seuls les nombres NOUVEAUX pour la page comptent. Répéter un
    # nombre déjà présent (tableau repris dans la FAQ, par ex.) n'est pas bloquant :
    # le relecteur juge le contexte. (25/09 : 9 faux positifs sur es-comparatif.)
    autorises, interdits = verite()
    nb, nn = nombres_du_texte(tb), nombres_du_texte(tn)
    for k in nn:
        if k not in nb and re.sub(r'\s', '', k) not in autorises:
            bloquants.append(f'{nom} : nombre ajouté non autorisé par VERITE.md : « {k} »')
    pct = lambda t: set(re.findall(r'(\d[\d.,]*)\s?%', t)) | set(re.findall(r'%\s?(\d[\d.,]*)', t))
    nouveaux_pct = pct(tn) - pct(tb)
    if nouveaux_pct:
        bloquants.append(f'{nom} : pourcentage ajouté (interdit sans source dans VERITE.md) : '
                         + ', '.join(sorted(nouveaux_pct)))
    # expressions interdites
    for motif in interdits:
        try:
            if compter(motif, tn) > compter(motif, tb):
                bloquants.append(f'{nom} : expression interdite ajoutée (VERITE.md §8) : /{motif}/')
        except re.error:
            avert.append(f'VERITE.md : motif invalide /{motif}/')
    # accents (espagnol)
    if lang == 'es':
        lb, ln = tb.lower(), tn.lower()
        for m in set(ACCENTS_ES.findall(ln)):
            if compter(rf'\b{re.escape(m)}\b', ln) > compter(rf'\b{re.escape(m)}\b', lb):
                bloquants.append(f'{nom} : mot sans accent ajouté : « {m} »')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slug')
    ap.add_argument('--base', required=True)
    ap.add_argument('--no-generators', action='store_true')
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(P, 'pages.json'), encoding='utf-8'))
    entree = next((p for p in cfg['pages'] if p['slug'] == a.slug), None)
    if not entree:
        print(json.dumps({'ok': False, 'bloquants': [f'slug inconnu : {a.slug}']}, ensure_ascii=False))
        sys.exit(1)
    bloquants, avert, infos = [], [], {}

    changes = [l for l in git('diff', '--name-only', a.base).splitlines() if l]
    changes += [l for l in git('ls-files', '--others', '--exclude-standard').splitlines() if l]
    changes = sorted(set(c for c in changes
                         if not c.startswith(('_tools/seo_pipeline/runs/', '.claude/'))))
    infos['fichiers_modifies'] = changes

    # périmètre
    permis = {entree['fichier']}
    if entree.get('generateur'):
        permis.add(entree['generateur'])
    autres = [c for c in changes if c not in permis]
    liens_blog = [c for c in autres if re.match(r'blog/(es|fr|en|val)/[^/]+\.html$', c)]
    for c in autres:
        if c in liens_blog[:1]:
            avert.append(f'{c} : article du blog modifié (lien interne attendu uniquement)')
            continue
        bloquants.append(f'fichier hors périmètre modifié : {c}')
    if len(liens_blog) > 1:
        bloquants.append('plus d\'un article du blog modifié')
    if entree['fichier'] not in changes:
        bloquants.append(f'la page cible {entree["fichier"]} n\'a pas changé')

    # pages générées : le script doit reproduire exactement la page
    if not a.no_generators and changes:
        git('add', '-A')  # runs/ et .claude/ sont exclus par .gitignore (une exclusion explicite d'un chemin ignoré fait échouer git add)
        for g in GENERATEURS_IDEMPOTENTS:
            r = subprocess.run([sys.executable, g], cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0:
                bloquants.append(f'{g} échoue : {(r.stdout + r.stderr).strip()[-300:]}')
        derive = [l for l in git('diff', '--name-only').splitlines() if l]
        if derive:
            bloquants.append('un script a régénéré des fichiers différents de la version modifiée '
                             '(page générée modifiée à la main ?) : ' + ', '.join(derive))
            git('checkout', '--', *derive)

    # contrôles HTML
    for c in changes:
        if not c.endswith('.html') or not os.path.exists(os.path.join(ROOT, c)):
            continue
        base_s = lire_base(a.base, c)
        new_s = open(os.path.join(ROOT, c), encoding='utf-8').read()
        lang = entree['lang'] if c == entree['fichier'] else (c.split('/')[1] if c.startswith('blog/') else entree['lang'])
        controler_html(c, base_s, new_s, lang, bloquants, avert, infos)

    res = {'ok': not bloquants, 'slug': a.slug, 'bloquants': bloquants, 'avertissements': avert, 'infos': infos}
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0 if res['ok'] else 1)


if __name__ == '__main__':
    main()
