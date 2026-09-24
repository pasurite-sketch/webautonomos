#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Accès SERPmantics du circuit SEO (API REST, sans passer par l'agent).

Pourquoi : lus par l'agent via MCP, les guides SERPmantics sont d'énormes JSON
qui saturent son contexte (1er essai du 24/09 : 16 min, 3,66 $, abandon).
Ce script fait le travail mécanique et ne donne à l'agent que des résumés.

    python3 _tools/seo_pipeline/serp.py guides <slug>
        Trouve ou crée les 2 guides de la page (Google + pages citées par les
        réponses IA de Google), attend qu'ils soient prêts, écrit :
          runs/<slug>/guides.json            identifiants + cible de score
          runs/<slug>/guide_google.md        résumé lisible (à lire par l'agent)
          runs/<slug>/guide_geo.md           idem pour le guide GEO (si disponible)
          runs/<slug>/guide_*.json           réponses brutes (NE PAS faire lire à l'agent)

    python3 _tools/seo_pipeline/serp.py score <slug> [--label avant|apres|fixN]
        Mesure le contenu ACTUEL de la page (balise <main>) avec chaque guide.
        Affiche un rapport court (score, structure, expressions sous/au-dessus
        des fourchettes, expressions à éviter présentes) et l'enregistre dans
        runs/<slug>/score_<label>.json. Gratuit (ne consomme ni crédit ni jeton).

Clé : variable SERPMANTICS_API_KEY (fichier ~/.seo_pipeline.env).
Ne crée jamais de guide pour un autre moteur que Google (les moteurs IA
coûtent 4 crédits) ; réutilise un guide existant de moins de 175 jours.
"""
import datetime
import html as htmlmod
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

P = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(P, '..', '..'))
RUNS = os.path.join(P, 'runs')
API = 'https://app.serpmantics.com/api/v1'
SOURCES = [('google', 'google'), ('geo', 'google_ai_overview_citations')]


# ---------------------------------------------------------------- utilitaires
def cfg():
    return json.load(open(os.path.join(P, 'pages.json'), encoding='utf-8'))


def entree(slug):
    for p in cfg()['pages']:
        if p['slug'] == slug:
            return p
    sys.exit(f'slug inconnu : {slug}')


def lang_code(e):
    brut = cfg().get('langues_serpmantics', {}).get(e['lang'], e['lang'])
    m = re.match(r'\s*([a-z]{2}-[a-z]{2})', brut, re.I)
    return m.group(1).lower() if m else brut.strip().lower()


def norm(t):
    t = unicodedata.normalize('NFD', (t or '').lower())
    return ''.join(c for c in t if unicodedata.category(c) != 'Mn').strip()


def dossier(slug):
    d = os.path.join(RUNS, slug)
    os.makedirs(d, exist_ok=True)
    return d


def api(methode, chemin, params=None, corps=None, essais=3):
    cle = os.environ.get('SERPMANTICS_API_KEY')
    if not cle:
        sys.exit('SERPMANTICS_API_KEY manquante (charge ~/.seo_pipeline.env)')
    url = API + chemin + ('?' + urllib.parse.urlencode(params) if params else '')
    data = json.dumps(corps).encode() if corps is not None else None
    for i in range(essais):
        req = urllib.request.Request(url, data=data, method=methode, headers={
            'Authorization': f'Bearer {cle}', 'Content-Type': 'application/json',
            'Accept': 'application/json', 'User-Agent': 'webautonomos-circuit-seo/1.0'})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                txt = r.read().decode('utf-8', 'replace')
                return r.status, (json.loads(txt) if txt.strip() else {})
        except urllib.error.HTTPError as e:
            txt = e.read().decode('utf-8', 'replace')
            try:
                j = json.loads(txt)
            except Exception:
                j = {'brut': txt[:500]}
            if e.code >= 500 and i < essais - 1 and methode == 'GET':
                time.sleep(10)
                continue
            return e.code, j
        except (urllib.error.URLError, TimeoutError) as e:
            if i < essais - 1 and methode == 'GET':
                time.sleep(10)
                continue
            return 0, {'erreur': str(e)}
    return 0, {}


def log(msg):
    print(f'[serp {datetime.datetime.now():%H:%M:%S}] {msg}', file=sys.stderr, flush=True)


# ---------------------------------------------------------------- guides
def chercher_guide(requete, lang, source):
    """Guide existant identique (requête, langue, source), non expiré, < 175 jours."""
    cible_q, cible_s = norm(requete), source.upper()
    limite = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=175)

    def convient(g):
        if norm(g.get('query')) != cible_q or (g.get('lang') or '').lower() != lang:
            return False
        if (g.get('source') or 'GOOGLE').upper() != cible_s or g.get('expired'):
            return False
        try:
            cree = datetime.datetime.fromisoformat(g['createdAt'].replace('Z', '+00:00'))
            return cree > limite
        except Exception:
            return True

    motif = re.sub(r'([.^$*+?()\[\]{}|\\])', r'\\\1', requete)  # regex côté serveur
    code, j = api('GET', '/guides', {'query': motif, 'pageSize': 100})
    trouves = [g for g in (j.get('guides') or []) if convient(g)] if code == 200 else []
    if not trouves:  # le filtre est une regex côté serveur : on vérifie aussi sans filtre
        for page in range(1, 6):
            code, j = api('GET', '/guides', {'page': page, 'pageSize': 100})
            lot = (j.get('guides') or []) if code == 200 else []
            trouves += [g for g in lot if convient(g)]
            if len(lot) < 100:
                break
    trouves.sort(key=lambda g: g.get('createdAt', ''), reverse=True)
    return trouves[0] if trouves else None


def attendre_guide(gid, max_min=25):
    fin = time.time() + max_min * 60
    while time.time() < fin:
        code, j = api('GET', '/guide', {'id': gid})
        if code == 200 and j.get('success') and j.get('guide'):
            g = j['guide']
            if g.get('isReady', True) and g.get('guide'):
                return 'pret', j
        if code == 200 and (j.get('status') == 'failed' or j.get('creationFailed')):
            return 'echec', j
        if code == 410:
            return 'expire', j
        time.sleep(20)
    return 'delai', {}


def creer_guide(requete, lang, source):
    code, j = api('POST', '/guides', corps={'queries': [requete], 'lang': lang, 'source': source})
    log(f'création {source} : HTTP {code}')
    if j.get('guides'):
        return j['guides'][0]['id']
    if j.get('guidesFailed'):
        log(f'refus sans guide créé (crédit rendu) : {json.dumps(j)[:300]}')
        return None
    # guidesUnknown ou réponse sans identifiant : NE PAS renvoyer, chercher le guide
    for _ in range(20):
        time.sleep(30)
        g = chercher_guide(requete, lang, source)
        if g:
            return g['id']
    log('guide introuvable après 10 min (ne pas le recréer : voir le support SERPmantics)')
    return None


def resume_guide(j, cle_src, requete, lang):
    g = j['guide']
    gg = g.get('guide') or {}
    L = [f"# Guide SERPmantics {g.get('source', cle_src.upper())} — « {requete} » ({lang}) — id {g.get('id')}", '']
    st = gg.get('structure') or {}
    if st:
        L.append('## Structure du top 10 (fourchette à viser)')
        noms = {'length': 'mots', 'headings': 'titres', 'paragraphs': 'paragraphes', 'images': 'images',
                'videos': 'vidéos', 'linksInternal': 'liens internes', 'linksExternal': 'liens externes',
                'tables': 'tableaux', 'lists': 'listes'}
        for k, v in st.items():
            if isinstance(v, dict):
                L.append(f"- {noms.get(k, k)} : {v.get('from')} à {v.get('to')}")
        L.append('')
    add = gg.get('add') or []
    if add:
        L.append(f'## Expressions à placer, par ordre d’importance ({len(add)}) — « expression : min–max »')
        L.append(', '.join(f"{a.get('expression')} : {a.get('from')}–{a.get('to')}" for a in add))
        L.append('')
    avoid = gg.get('avoid') or []
    if avoid:
        L.append('## Expressions à éviter (absentes de la 1re page de Google)')
        L.append(', '.join(a.get('expression', '') for a in avoid))
        L.append('')
    top = g.get('topSERPResultsDetails') or []
    if top:
        L.append('## Premiers résultats')
        for i, r in enumerate(top[:10], 1):
            if not isinstance(r, dict):
                continue
            url = r.get('url') or r.get('link') or ''
            sc = r.get('score')
            mots = (r.get('structure') or {}).get('length') if isinstance(r.get('structure'), dict) else None
            L.append(f"{i}. {url}" + (f" — score {sc}" if sc is not None else '') + (f" — {mots} mots" if mots else ''))
        L.append('')
    return '\n'.join(L)


def cible_top3(j):
    top = j['guide'].get('topSERPResultsDetails') or []
    scores = [r.get('score') for r in top if isinstance(r, dict) and isinstance(r.get('score'), (int, float))][:3]
    if not scores:
        return 70
    scores.sort()
    return min(80, round(scores[len(scores) // 2]))


def cmd_guides(slug):
    e = entree(slug)
    requete, lang, d = e['requete'], lang_code(e), dossier(slug)
    res = {'requete': requete, 'lang': lang, 'crees': []}
    for cle_src, source in SOURCES:
        g = chercher_guide(requete, lang, source)
        gid = g['id'] if g else None
        log(f'{cle_src} : ' + (f'guide existant réutilisé ({gid})' if gid else 'aucun guide existant, création'))
        if not gid:
            gid = creer_guide(requete, lang, source)
            if gid:
                res['crees'].append(cle_src)
        if not gid:
            res[cle_src] = None
            continue
        etat, j = attendre_guide(gid)
        log(f'{cle_src} : {etat}')
        if etat != 'pret':
            res[cle_src] = None
            res[cle_src + '_erreur'] = (j.get('error') or etat) if isinstance(j, dict) else etat
            continue
        json.dump(j, open(os.path.join(d, f'guide_{cle_src}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        open(os.path.join(d, f'guide_{cle_src}.md'), 'w', encoding='utf-8').write(resume_guide(j, cle_src, requete, lang))
        res[cle_src] = gid
        if cle_src == 'google':
            res['cible_top3'] = cible_top3(j)
    json.dump(res, open(os.path.join(d, 'guides.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False))
    if not res.get('google'):
        sys.exit('guide Google indisponible')


# ---------------------------------------------------------------- score
def contenu_page(e):
    s = open(os.path.join(REPO, e['fichier']), encoding='utf-8').read()
    m = re.search(r'(?is)<main[^>]*>(.*)</main>', s) or re.search(r'(?is)<body[^>]*>(.*)</body>', s)
    c = m.group(1) if m else s
    c = re.sub(r'(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>', ' ', c)
    c = re.sub(r'(?s)<!--.*?-->', ' ', c)
    return re.sub(r'\s+', ' ', c).strip()


def texte(html):
    return htmlmod.unescape(re.sub(r'<[^>]+>', ' ', html))


def compter(expr, txt_norm):
    return len(re.findall(r'(?<!\w)' + re.escape(norm(expr)) + r'(?!\w)', txt_norm))


def analyser(j_guide, j_score, contenu):
    gg = j_guide['guide'].get('guide') or {}
    ca = j_score.get('contentAnalysis') or {}
    expr = {norm(k): v for k, v in (ca.get('expressions') or {}).items()}
    txt_n = norm(texte(contenu))
    sous, dessus = [], []
    for a in gg.get('add') or []:
        e_ = a.get('expression', '')
        n = expr.get(norm(e_))
        if n is None:
            n = compter(e_, txt_n)
        if a.get('from') is not None and n < a['from']:
            sous.append(f"{e_} {n}/{a['from']}–{a['to']}")
        elif a.get('to') is not None and n > a['to']:
            dessus.append(f"{e_} {n}/{a['from']}–{a['to']}")
    eviter = []
    for a in gg.get('avoid') or []:
        n = compter(a.get('expression', ''), txt_n)
        if n:
            eviter.append(f"{a.get('expression')} ×{n}")
    st_g, st_p = gg.get('structure') or {}, ca.get('structure') or {}
    struct = []
    corresp = {'length': 'mots', 'headings': 'titres', 'paragraphs': 'paragraphes', 'images': 'images',
               'tables': 'tableaux', 'lists': 'listes', 'videos': 'vidéos'}
    for k, nom in corresp.items():
        if k in st_g and k in st_p:
            f, t = st_g[k].get('from'), st_g[k].get('to')
            v = st_p[k]
            etat = 'OK' if (f is None or v >= f) and (t is None or v <= t) else ('trop bas' if f is not None and v < f else 'trop haut')
            struct.append(f'{nom} {v} ({f}–{t}) {etat}')
    if 'linksInternal' in st_g and 'links' in st_p:
        f = (st_g['linksInternal'].get('from') or 0) + (st_g.get('linksExternal', {}).get('from') or 0)
        t = (st_g['linksInternal'].get('to') or 0) + (st_g.get('linksExternal', {}).get('to') or 0)
        struct.append(f"liens {st_p['links']} ({f}–{t})")
    return {'score': ca.get('score'), 'structure': struct, 'sous_fourchette': sous,
            'au_dessus_fourchette': dessus, 'a_eviter_presentes': eviter}


def cmd_score(slug, label):
    e, d = entree(slug), dossier(slug)
    try:
        ids = json.load(open(os.path.join(d, 'guides.json'), encoding='utf-8'))
    except Exception:
        sys.exit('lance d’abord : python3 _tools/seo_pipeline/serp.py guides ' + slug)
    contenu = contenu_page(e)
    rapport = {'label': label, 'fichier': e['fichier'], 'cible_top3': ids.get('cible_top3')}
    for cle_src, _ in SOURCES:
        gid = ids.get(cle_src)
        if not gid:
            continue
        try:
            jg = json.load(open(os.path.join(d, f'guide_{cle_src}.json'), encoding='utf-8'))
        except Exception:
            continue
        code, js = api('POST', '/score', corps={'guideId': gid, 'content': contenu,
                                                'saveToGuide': label != 'avant',
                                                'scoreProgressive': False, 'includeEmbedding': False})
        if code != 200 or not js.get('success', True):
            rapport[cle_src] = {'erreur': f'HTTP {code}', 'detail': str(js)[:300]}
            continue
        rapport[cle_src] = analyser(jg, js, contenu)
    json.dump(rapport, open(os.path.join(d, f'score_{label}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    L = [f"SCORE SERPmantics ({label}) — {e['fichier']} — cible Google : {rapport.get('cible_top3')} (médiane du top 3, plafond 80)"]
    for cle_src, _ in SOURCES:
        r = rapport.get(cle_src)
        if not r:
            continue
        if 'erreur' in r:
            L.append(f"[{cle_src}] ERREUR {r['erreur']} {r.get('detail', '')}")
            continue
        L.append(f"[{cle_src}] score {r['score']}")
        L.append('  structure : ' + ' · '.join(r['structure']))
        L.append(f"  sous la fourchette ({len(r['sous_fourchette'])}) : " + ', '.join(r['sous_fourchette'][:40]))
        L.append(f"  au-dessus ({len(r['au_dessus_fourchette'])}) : " + ', '.join(r['au_dessus_fourchette']))
        if r['a_eviter_presentes']:
            L.append('  à éviter présentes : ' + ', '.join(r['a_eviter_presentes']))
    print('\n'.join(L))


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == 'guides':
        cmd_guides(a[1])
    elif len(a) >= 2 and a[0] == 'score':
        lab = a[a.index('--label') + 1] if '--label' in a else 'mesure'
        if not re.fullmatch(r'[a-z0-9_-]{1,20}', lab):
            sys.exit('label invalide')
        cmd_score(a[1], lab)
    else:
        sys.exit(__doc__)
