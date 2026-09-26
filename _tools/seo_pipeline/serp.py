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

    python3 _tools/seo_pipeline/serp.py verifier <slug>
        Mesure de contrôle (gratuite) et verdict « au vert » : score Google ≥ seuil
        (pages.json « seuil_vert », 50) et, si l'entrée a « objectif_geo »: "vert",
        moyenne des guides GEO ≥ seuil. Code de sortie 0 = au vert, 3 = à affiner.

    python3 _tools/seo_pipeline/serp.py sources
        Demande au serveur MCP de SERPmantics la liste de ses outils et les valeurs
        possibles de « source » (Google, AI Overview, ChatGPT, Gemini…). Gratuit.

    python3 _tools/seo_pipeline/serp.py score <slug> [--label avant|apres|fixN]
        Mesure le contenu ACTUEL de la page (balise <main>) avec chaque guide.
        Affiche un rapport court (score, structure, expressions sous/au-dessus
        des fourchettes, expressions à éviter présentes) et l'enregistre dans
        runs/<slug>/score_<label>.json. Gratuit (ne consomme ni crédit ni jeton).

Clé : variable SERPMANTICS_API_KEY (fichier ~/.seo_pipeline.env).
Sources des guides : Google + les sources GEO listées dans pages.json
(« sources_geo » : AI Overview de Google, et ChatGPT / Gemini une fois leurs noms
confirmés par `serp.py sources`). Réutilise un guide existant de moins de 175 jours.
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
SOURCES_GEO_DEFAUT = [{'cle': 'geo', 'source': 'google_ai_overview_citations', 'nom': 'AI Overview de Google'}]


def sources():
    """[(clé, source SERPmantics, nom)] : Google d'abord, puis les sources GEO de pages.json.
    Une source « auto:<motif> » (ex. auto:chatgpt|openai|gpt) est résolue d'après la liste
    officielle des sources SERPmantics ; introuvable, elle est ignorée."""
    geo = cfg().get('sources_geo') or SOURCES_GEO_DEFAUT
    out = [('google', 'google', 'Google')]
    for g in geo:
        src = g['source']
        if src.startswith('auto:'):
            src = resoudre_source(src[5:])
            if not src:
                continue
        out.append((g['cle'], src, g.get('nom', g['cle'])))
    return out


def valeurs_sources():
    """Valeurs possibles du paramètre « source » des guides, lues une fois par mois sur le
    serveur MCP de SERPmantics (gratuit) et gardées dans runs/_sources_serpmantics.json."""
    cache = os.path.join(RUNS, '_sources_serpmantics.json')
    try:
        c = json.load(open(cache, encoding='utf-8'))
        if time.time() - c.get('t', 0) < 30 * 86400 and c.get('valeurs'):
            return c['valeurs']
    except Exception:
        pass
    if not os.environ.get('SERPMANTICS_API_KEY'):
        return []
    try:
        outils = lister_outils_mcp()
    except Exception as e:
        log(f'liste des sources SERPmantics indisponible : {e}')
        return []
    valeurs, textes = [], []

    def collecter(schema):
        if not isinstance(schema, dict):
            return
        valeurs.extend(v for v in schema.get('enum') or [] if isinstance(v, str))
        textes.append(schema.get('description') or '')
        for k in ('items', 'anyOf', 'oneOf'):
            sous = schema.get(k)
            for x in (sous if isinstance(sous, list) else [sous]):
                collecter(x)
    for t in outils:
        collecter(((t.get('inputSchema') or {}).get('properties') or {}).get('source'))
    if not valeurs:  # pas d'enum : on prend les identifiants cités dans les descriptions
        for tx in textes:
            valeurs += re.findall(r'\b[a-z][a-z0-9]*(?:_[a-z0-9]+)*\b', tx)
    valeurs = list(dict.fromkeys(valeurs))
    os.makedirs(RUNS, exist_ok=True)
    json.dump({'t': time.time(), 'valeurs': valeurs}, open(cache, 'w', encoding='utf-8'), ensure_ascii=False)
    return valeurs


def resoudre_source(motif):
    for v in valeurs_sources():
        if re.search(motif, v, re.I):
            return v
    log(f'aucune source SERPmantics ne correspond à « {motif} » : ignorée')
    return None


def seuil_vert():
    return int(cfg().get('seuil_vert', 50))


def seuil_rouge():
    return int(cfg().get('seuil_rouge', 25))


# ---------------------------------------------------------------- utilitaires
def cfg():
    return json.load(open(os.path.join(P, 'pages.json'), encoding='utf-8'))


def entree(slug):
    for p in cfg()['pages']:
        if p['slug'] == slug:
            return p
    sys.exit(f'slug inconnu : {slug}')


def lang_codes(e):
    """Codes de langue SERPmantics à essayer, dans l'ordre (pages.json :
    « en-es (si SERPmantics le refuse : en-gb) » → ['en-es', 'en-gb']). Le champ
    « langue_serpmantics » de la page, s'il existe, prime (pages britanniques : en-gb)."""
    brut = e.get('langue_serpmantics') or cfg().get('langues_serpmantics', {}).get(e['lang'], e['lang'])
    codes = [c.lower() for c in re.findall(r'\b([a-z]{2}-[a-z]{2})\b', brut, re.I)]
    return list(dict.fromkeys(codes)) or [brut.strip().lower()]


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
    """Renvoie (identifiant ou None, refus) ; refus = demande rejetée, rien n'a été créé."""
    code, j = api('POST', '/guides', corps={'queries': [requete], 'lang': lang, 'source': source})
    log(f'création {source} ({lang}) : HTTP {code}')
    if j.get('guides'):
        return j['guides'][0]['id'], False
    if j.get('guidesFailed'):
        log(f'refus sans guide créé (crédit rendu) : {json.dumps(j, ensure_ascii=False)[:300]}')
        return None, True
    if 400 <= code < 500 and code not in (408, 429):
        # demande refusée (langue non prise en charge, paramètre invalide…) : rien n'a
        # été créé, inutile d'attendre (25/09 : 20 min perdues sur en-carpenters)
        log(f'demande refusée : {json.dumps(j, ensure_ascii=False)[:300]}')
        return None, True
    # guidesUnknown ou réponse sans identifiant : NE PAS renvoyer, chercher le guide
    for _ in range(20):
        time.sleep(30)
        g = chercher_guide(requete, lang, source)
        if g:
            return g['id'], False
    log('guide introuvable après 10 min (ne pas le recréer : voir le support SERPmantics)')
    return None, False


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
    return round(scores[len(scores) // 2])  # pas de plafond (décision du 25/09/2026)


def obtenir_guide(requete, lang, cle_src, source, res):
    """Identifiant d'un guide existant ou nouvellement créé ; (None, refus) sinon."""
    g = chercher_guide(requete, lang, source)
    gid = g['id'] if g else None
    log(f'{cle_src} ({lang}) : ' + (f'guide existant réutilisé ({gid})' if gid else 'aucun guide existant, création'))
    if gid:
        return gid, False
    gid, refus = creer_guide(requete, lang, source)
    if gid:
        res['crees'].append(cle_src)
    return gid, refus


def cmd_guides(slug):
    e = entree(slug)
    requete, d = e['requete'], dossier(slug)
    langs = lang_codes(e)
    res = {'requete': requete, 'lang': langs[0], 'crees': []}
    # guide Google d'abord, en essayant les langues de repli si SERPmantics refuse
    gid_google = None
    for i, lang in enumerate(langs):
        res['lang'] = lang
        gid_google, refus = obtenir_guide(requete, lang, 'google', 'google', res)
        if gid_google or not refus:
            break
        if i + 1 < len(langs):
            log(f'langue {lang} refusée : essai avec {langs[i + 1]}')
    lang = res['lang']
    for cle_src, source, _nom in sources():
        if cle_src == 'google':
            gid = gid_google
        else:
            gid, _ = obtenir_guide(requete, lang, cle_src, source, res)
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
    for cle_src, _src, _nom in sources():
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
    hors = set(e.get('geo_hors_cible') or [])
    geo = [rapport[c]['score'] for c, _s, _n in sources()[1:]
           if c not in hors and isinstance(rapport.get(c), dict) and isinstance(rapport[c].get('score'), (int, float))]
    rapport['geo_hors_cible'] = sorted(hors)
    rapport['score_geo_moyen'] = round(sum(geo) / len(geo)) if geo else None
    json.dump(rapport, open(os.path.join(d, f'score_{label}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    L = [f"SCORE SERPmantics ({label}) — {e['fichier']} — cible Google : au moins 50 et {rapport.get('cible_top3')} (médiane du top 3), sans plafond si le texte reste naturel"]
    for cle_src, _src, nom in sources():
        r = rapport.get(cle_src)
        if not r:
            continue
        if 'erreur' in r:
            L.append(f"[{cle_src}] ERREUR {r['erreur']} {r.get('detail', '')}")
            continue
        L.append(f"[{cle_src} — {nom}] score {r['score']}")
        L.append('  structure : ' + ' · '.join(r['structure']))
        L.append(f"  sous la fourchette ({len(r['sous_fourchette'])}) : " + ', '.join(r['sous_fourchette'][:40]))
        L.append(f"  au-dessus ({len(r['au_dessus_fourchette'])}) : " + ', '.join(r['au_dessus_fourchette']))
        if r['a_eviter_presentes']:
            L.append('  à éviter présentes : ' + ', '.join(r['a_eviter_presentes']))
    if rapport.get('score_geo_moyen') is not None:
        L.append(f"GEO moyen (toutes sources GEO) : {rapport['score_geo_moyen']}")
    print('\n'.join(L))
    return rapport


REPETITION = re.compile(r'^(.*) (\d+)/(\d+)\u2013(\d+)$')


def repetitions(r):
    """Expressions du guide Google nettement trop répétées (SERPmantics les dit « trop
    citées ») : au moins 10 occurrences et plus du double du haut de la fourchette."""
    out = []
    for x in ((r.get('google') or {}).get('au_dessus_fourchette') or []):
        m = REPETITION.match(x)
        if m:
            expr, n, haut = m.group(1), int(m.group(2)), int(m.group(4))
            if n >= 10 and n > 2 * haut:
                out.append(f'{expr} {n}× (fourchette {m.group(3)}–{haut})')
    return out


def cmd_verifier(slug, label='controle'):
    e = entree(slug)
    r = cmd_score(slug, label)
    s = seuil_vert()
    g = (r.get('google') or {}).get('score')
    geo = r.get('score_geo_moyen')
    objectif = e.get('objectif_geo', 'au_mieux')
    manque = []
    if not isinstance(g, (int, float)):
        sys.exit('score Google indisponible')  # code 1 : erreur, pas une décision
    if g < s:
        manque.append(f'Google {g} < {s}')
    if objectif == 'vert' and geo is not None and geo < s:
        manque.append(f'GEO moyen {geo} < {s} (objectif_geo : vert)')
    # toutes les pages : aucun guide GEO en rouge (décision d'Angelino du 25/09/2026, 23h29)
    for cle, _src, nom in sources()[1:]:
        if cle in (e.get('geo_hors_cible') or []):
            continue  # pages citées hors du public visé (décision du 26/09/2026)
        sc = (r.get(cle) or {}).get('score') if isinstance(r.get(cle), dict) else None
        if isinstance(sc, (int, float)) and sc < seuil_rouge():
            manque.append(f'GEO {nom} {sc} en rouge (< {seuil_rouge()}) : à remonter au vert')
    trop = repetitions(r)
    if trop:
        manque.append('répétitions à réduire (texte peu naturel) : ' + ', '.join(trop))
    if manque:
        print('À AFFINER : ' + ' ; '.join(manque))
        sys.exit(3)
    print(f'SEUILS ATTEINTS : Google {g}' + (f', GEO moyen {geo}' if geo is not None else '')
          + f' (objectif_geo : {objectif}, aucun guide GEO en rouge)')


def mcp_appel(methode, params=None, session=None, ident=1):
    cle = os.environ.get('SERPMANTICS_API_KEY')
    if not cle:
        sys.exit('SERPMANTICS_API_KEY manquante (charge ~/.seo_pipeline.env)')
    corps = {'jsonrpc': '2.0', 'method': methode}
    if ident is not None:
        corps['id'] = ident
    if params is not None:
        corps['params'] = params
    h = {'Authorization': f'Bearer {cle}', 'Content-Type': 'application/json',
         'Accept': 'application/json, text/event-stream', 'User-Agent': 'webautonomos-circuit-seo/1.0'}
    if session:
        h['Mcp-Session-Id'] = session
    req = urllib.request.Request(API + '/mcp', data=json.dumps(corps).encode(), method='POST', headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        txt = r.read().decode('utf-8', 'replace')
        sid = r.headers.get('Mcp-Session-Id') or session
    donnees = [l[5:].strip() for l in txt.splitlines() if l.startswith('data:')]
    brut = donnees[-1] if donnees else txt
    try:
        return json.loads(brut) if brut.strip() else {}, sid
    except Exception:
        return {'brut': brut[:500]}, sid


def lister_outils_mcp():
    _init, sid = mcp_appel('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {},
                                          'clientInfo': {'name': 'webautonomos-circuit-seo', 'version': '1.0'}})
    try:
        mcp_appel('notifications/initialized', None, sid, ident=None)
    except Exception:
        pass
    rep_, _ = mcp_appel('tools/list', {}, sid, ident=2)
    outils = ((rep_.get('result') or {}).get('tools')) or []
    if not outils:
        raise RuntimeError('réponse inattendue : ' + json.dumps(rep_, ensure_ascii=False)[:500])
    return outils


def cmd_sources():
    try:
        outils = lister_outils_mcp()
    except Exception as e:
        print(e)
        return
    for t in outils:
        props = ((t.get('inputSchema') or {}).get('properties')) or {}
        src = props.get('source')
        ligne = f"- {t.get('name')}"
        if src:
            ligne += f" | source : {json.dumps(src, ensure_ascii=False)[:600]}"
        print(ligne)
        d = t.get('description') or ''
        if re.search(r'chatgpt|gemini|perplexity|llm|source|cr[ée]dit', d, re.I):
            print('    ' + re.sub(r'\s+', ' ', d)[:700])
    try:
        os.remove(os.path.join(RUNS, '_sources_serpmantics.json'))  # relire la liste à jour
    except OSError:
        pass
    print('\nSources utilisées par le circuit :')
    for cle, src, nom in sources():
        print(f'  {cle:8} {nom:24} → {src}')


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == 'guides':
        cmd_guides(a[1])
    elif len(a) >= 2 and a[0] == 'verifier':
        lab = a[a.index('--label') + 1] if '--label' in a else 'controle'
        if not re.fullmatch(r'[a-z0-9_-]{1,20}', lab):
            sys.exit('label invalide')
        cmd_verifier(a[1], lab)
    elif a and a[0] == 'sources':
        cmd_sources()
    elif len(a) >= 2 and a[0] == 'score':
        lab = a[a.index('--label') + 1] if '--label' in a else 'mesure'
        if not re.fullmatch(r'[a-z0-9_-]{1,20}', lab):
            sys.exit('label invalide')
        cmd_score(a[1], lab)
    else:
        sys.exit(__doc__)
