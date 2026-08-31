#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Traduit un article blog/es/{slug}.html vers blog/fr/{slug-fr}.html
SANS JAMAIS pouvoir produire un fichier tronque.

------------------------------------------------------------------------------
POURQUOI CET OUTIL EXISTE
------------------------------------------------------------------------------
Le 2026-03-18, les 88 fichiers blog/val et blog/en ont ete produits par une
generation unique du document entier. La sortie a bute sur un plafond de
longueur (~30 Ko) : 21 fichiers EN sur 22 sont coupes, 14 en plein corps de
texte, 7 au milieu d'un attribut HTML, et 4 fichiers VAL contiennent deux fois
le meme article mal recolle. Le texte perdu n'existe nulle part.

Deux principes en decoulent, et ils structurent tout ce script :

  1. LE MARKUP N'EST JAMAIS GENERE. Le document de sortie est un clone du
     document source ; seuls les fragments de texte sont substitues, en place.
     Une troncature de generation ne peut donc pas casser la structure : il n'y
     a aucune structure a generer.

  2. RIEN N'EST TRAITE D'UN SEUL BLOC. Le texte est decoupe en segments courts
     (un titre, un paragraphe, une reponse de FAQ...), traduits independamment.
     Aucun appel ne porte sur le document entier.

Et un garde-fou final : le CONTROLE D'INTEGRITE est BLOQUANT. Tant qu'un seul
critere echoue, rien n'est ecrit sur disque. Un fichier tronque ne peut pas
atteindre le repertoire blog/.

------------------------------------------------------------------------------
UTILISATION
------------------------------------------------------------------------------
  # 1. extraire les segments a traduire
  python3 _tools/translate_article.py extract seo-local-que-es-autonomos \\
      --fr-slug seo-local-quest-ce-que-cest-independants

  # -> ecrit _tools/translations/{fr-slug}.json : chaque segment a un champ "fr"
  #    vide, a remplir. Le champ "source" ne doit jamais etre modifie.

  # 2. reassembler et verifier (n'ecrit que si TOUS les controles passent)
  python3 _tools/translate_article.py build seo-local-que-es-autonomos \\
      --fr-slug seo-local-quest-ce-que-cest-independants

  # verifier un fichier deja produit
  python3 _tools/translate_article.py check blog/fr/mon-article.html \\
      --source blog/es/mon-article.html
"""

import argparse
import html as H
import json
import os
import difflib
import glob
import re
import unicodedata
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'
TRANSLATIONS_DIR = os.path.join(ROOT, '_tools', 'translations')

# Elements sans balise fermante.
VOID = {'meta', 'link', 'br', 'hr', 'img', 'input', 'source', 'col', 'area',
        'base', 'wbr', 'embed', 'track', 'param'}

# Elements "blocs" : un segment traduisible est un bloc qui ne contient
# aucun autre bloc (une feuille). Les balises en ligne (strong, em, a...)
# restent DANS le segment, pour que la phrase garde son sens.
# 'div' en fait partie : sans lui les reponses de FAQ, qui vivent dans un
# <div>, echappaient a l'extraction. La couverture mesuree a l'extraction
# (mots captures / mots du document) est la garantie qu'aucun texte ne fuit.
# 'pre' y figure depuis qu'un exemple de code JSON-LD a traverse le pipeline sans
# etre vu : ses valeurs espagnoles (« Fontaneria Lopez Elda », « +34 », pays ES)
# survivaient a une traduction declaree complete. C'etait la 3e lacune de la
# meme famille, apres le texte orphelin des blocs parents.
BLOCK = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'summary', 'dt', 'dd',
         'td', 'th', 'caption', 'figcaption', 'blockquote', 'address', 'div',
         'pre'}

# Seuil de perte de texte tolere. Le francais est structurellement plus long
# que l'espagnol (~10-15%), donc descendre sous 85% signale une amputation,
# pas une difference de langue.
MIN_WORD_RATIO = 0.85


# ==========================================================================
# 1. Analyse du document source
# ==========================================================================

TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)((?:"[^"]*"|\'[^\']*\'|[^>"\'])*?)(/?)>')


def mask_raw_text(s):
    """Remplace le contenu de <script> et <style> par des blancs.

    Conserve la longueur exacte, pour que tous les offsets calcules sur la
    chaine masquee restent valables sur la chaine d'origine.
    """
    out = list(s)
    for m in re.finditer(r'(?is)<(script|style)\b[^>]*>(.*?)</\1>', s):
        for i in range(m.start(2), m.end(2)):
            if out[i] != '\n':
                out[i] = ' '
    return ''.join(out)


def iter_tags(masked):
    for m in TAG_RE.finditer(masked):
        yield m, m.group(1) == '/', m.group(2).lower(), m.group(4) == '/'


def leaf_blocks(s):
    """[(debut_contenu, fin_contenu, nom_balise)] des zones de texte a traduire.

    Deux familles :
      - les blocs FEUILLES : un <p>, un <li>, un <h2> sans bloc enfant ;
      - le texte ORPHELIN d'un bloc parent : du texte qui vit directement dans un
        bloc ayant par ailleurs des blocs enfants, et qui n'appartient donc a
        aucune feuille.

    La seconde famille a ete ajoutee apres un trou reel : dans

        <div class="faq-item"><strong>Question ?</strong><p>Reponse.</p></div>

    seule la reponse etait une feuille. La question, posee dans un <strong> du
    <div> parent, n'etait extraite par personne et restait donc en espagnol dans
    un fichier par ailleurs declare traduit. Meme famille de bug que le <pre>
    de l'article Schema : ce que l'extraction ne voit pas, la traduction ne le
    corrige pas.
    """
    masked = mask_raw_text(s)
    # nom, debut contenu, a_un_bloc_enfant, [spans des blocs enfants directs]
    stack, spans = [], []
    for m, is_close, name, self_closing in iter_tags(masked):
        if name in VOID or self_closing:
            continue
        if not is_close:
            if name in BLOCK:
                for fr in reversed(stack):
                    if fr[0] in BLOCK:
                        fr[2] = True
                        fr[3].append([m.start(), None])   # span du bloc enfant direct
                        break
            stack.append([name, m.end(), False, []])
        else:
            while stack and stack[-1][0] != name:
                stack.pop()
            if not stack:
                continue
            open_name, content_start, has_block_child, kids = stack.pop()
            if open_name not in BLOCK:
                continue
            # Tout bloc qui se ferme referme son span chez son parent — feuille
            # comprise. Ne le faire que pour les parents laissait les feuilles
            # hors des spans enfants, et leur texte etait alors compte deux fois :
            # une fois comme feuille, une fois comme orphelin du parent.
            for fr in reversed(stack):
                if fr[0] in BLOCK:
                    if fr[3] and fr[3][-1][1] is None:
                        fr[3][-1][1] = m.end()
                    break
            if not has_block_child:
                spans.append((content_start, m.start(), open_name))
                continue
            # texte orphelin = contenu du parent moins les spans de ses enfants
            cursor = content_start
            for a, b in kids:
                if b is None:
                    continue
                if a > cursor and visible_words(masked[cursor:a]):
                    spans.append((cursor, a, open_name))
                cursor = max(cursor, b)
            if m.start() > cursor and visible_words(masked[cursor:m.start()]):
                spans.append((cursor, m.start(), open_name))
    return sorted(spans)


def visible_words(s):
    t = re.sub(r'(?is)<(script|style)\b[^>]*>.*?</\1>', ' ', s)
    t = re.sub(r'<[^>]+>', ' ', t)
    return H.unescape(t).split()


def inline_tag_signature(fragment):
    """Multiset des balises en ligne, pour verifier qu'une traduction les conserve."""
    sig = {}
    for m, is_close, name, self_closing in iter_tags(mask_raw_text(fragment)):
        key = ('/' if is_close else '') + name
        sig[key] = sig.get(key, 0) + 1
    return sig


# ==========================================================================
# 2. Extraction
# ==========================================================================

# (nom, motif, est_un_attribut). Dans un attribut il faut echapper les quotes ;
# dans le contenu de <title> ce serait du bruit (&#x27; a la place de ').
META_FIELDS = [
    ('title', r'(<title[^>]*>)(.*?)(</title>)'),
    ('description', r'(<meta name="description" content=")([^"]*)(")'),
    ('og:title', r'(<meta property="og:title" content=")([^"]*)(")'),
    ('og:description', r'(<meta property="og:description" content=")([^"]*)(")'),
    ('twitter:title', r'(<meta name="twitter:title" content=")([^"]*)(")'),
    ('twitter:description', r'(<meta name="twitter:description" content=")([^"]*)(")'),
    ('article:section', r'(<meta property="article:section" content=")([^"]*)(")'),
]

# Champs de chaine traduisibles dans les blocs JSON-LD.
JSONLD_KEYS = {'headline', 'description', 'name', 'text', 'articleSection', 'keywords'}


def jsonld_blocks(s):
    return list(re.finditer(r'(?is)(<script type="application/ld\+json">)(.*?)(</script>)', s))


def walk_jsonld(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str) and k in JSONLD_KEYS and v.strip():
                out.append(('.'.join(path + [k]), v))
            else:
                walk_jsonld(v, path + [k], out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_jsonld(v, path + [str(i)], out)


def cmd_extract(args):
    src_path = os.path.join(ROOT, 'blog', 'es', args.es_slug + '.html')
    if not os.path.isfile(src_path):
        sys.exit('source introuvable : ' + src_path)
    s = open(src_path, encoding='utf-8').read()

    segments = []

    # --- metadonnees du <head>
    for name, pattern in META_FIELDS:
        m = re.search(pattern, s, re.S)
        if m and m.group(2).strip():
            segments.append(dict(id='meta:' + name, kind='meta', source=m.group(2).strip(), fr=''))

    # --- blocs feuilles du corps
    for i, (a, b, tag) in enumerate(leaf_blocks(s)):
        frag = s[a:b]
        if not visible_words(frag):
            continue
        segments.append(dict(id='block:%04d' % i, kind=tag, offset=[a, b],
                             source=frag.strip(), fr=''))

    # --- chaines des blocs JSON-LD
    for bi, m in enumerate(jsonld_blocks(s)):
        try:
            data = json.loads(m.group(2))
        except json.JSONDecodeError:
            continue
        found = []
        walk_jsonld(data, [], found)
        for path, value in found:
            segments.append(dict(id='jsonld:%d:%s' % (bi, path), kind='jsonld',
                                 source=value, fr=''))

    faq_count = len(re.findall(r'<details\b', s))
    h2_count = len(re.findall(r'<h2\b', s))

    payload = dict(
        es_slug=args.es_slug, fr_slug=args.fr_slug, lang=args.lang,
        source_file=os.path.relpath(src_path, ROOT),
        source_metrics=dict(words=len(visible_words(s)), details=faq_count, h2=h2_count),
        instructions=(
            "Remplir le champ 'fr' de chaque segment. Ne jamais modifier 'source' ni 'id'. "
            "Conserver exactement les memes balises en ligne (<strong>, <a>, <em>...) "
            "et les memes URL. Traduction adaptee, pas litterale. "
            "REGISTRE — REGLE ABSOLUE : le francais VOUVOIE le lecteur, JAMAIS il ne le "
            "tutoie. Employer vous / votre / vos / le votre, et accorder les participes et "
            "adjectifs au pluriel de politesse (« vous etes prets », « si vous etes "
            "positionne »). Aucune forme de 2e personne du singulier ne doit subsister : "
            "ni « tu », ni « ton / ta / tes », ni « toi », ni imperatif singulier "
            "(« utilise » -> « utilisez », « ne depasse pas » -> « ne depassez pas »). "
            "Le controle de registre de la commande 'build' est bloquant. "
            "ADAPTATION CULTURELLE — la traduction n'est pas litterale, elle transpose. "
            "(a) VILLES : remplacer les villes espagnoles citees EN EXEMPLE par des villes "
            "francophones representatives — Lyon, Nantes, Bruxelles, Lausanne — et les "
            "quartiers par des quartiers de ces villes. EXCEPTION : garder la ville telle "
            "quelle quand elle designe WebAutonomos lui-meme (siege d'Ontinyent, zone "
            "desservie « Comunidad Valenciana » du bloc Organization, adresse du pied de "
            "page NAP) : c'est un fait sur l'entreprise, pas un exemple pedagogique. "
            "(b) REFERENCES REGLEMENTAIRES espagnoles sans equivalent francophone (RETA, "
            "Kit Digital, IVA, autonomo societario) : donner l'equivalent local s'il existe, "
            "sinon REFORMULER la phrase sans la mention. Ne jamais traduire litteralement un "
            "dispositif qui n'existe pas chez le lecteur. "
            "(c) PRIX : laisser les montants en euros inchanges, et « 15 €/mois » "
            "strictement tel quel — c'est l'offre commerciale, pas un exemple."),
        segments=segments,
    )
    os.makedirs(TRANSLATIONS_DIR, exist_ok=True)
    out = os.path.join(TRANSLATIONS_DIR, args.fr_slug + '.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)

    # Couverture : tout mot visible du document doit se retrouver dans un segment.
    captured = sum(len(visible_words(seg['source']))
                   for seg in segments if seg['id'].startswith('block:'))
    total = len(visible_words(s))
    coverage = captured / total if total else 0

    kinds = {}
    for seg in segments:
        kinds[seg['kind']] = kinds.get(seg['kind'], 0) + 1
    print('  source   : %s' % payload['source_file'])
    print('  segments : %d  (%s)' % (len(segments),
          ', '.join('%s=%d' % kv for kv in sorted(kinds.items()))))
    print('  metriques source : %d mots, %d <h2>, %d <details>'
          % (payload['source_metrics']['words'], h2_count, faq_count))
    print('  couverture du texte : %d/%d mots (%.1f%%)' % (captured, total, coverage * 100))
    print('  ecrit    : %s' % os.path.relpath(out, ROOT))
    if coverage < 0.95:
        print('  ATTENTION : couverture < 95%, du texte echapperait a la traduction.')
        return 1
    return 0


# ==========================================================================
# 3. Reassemblage
# ==========================================================================

# ==========================================================================
# Mesure d'audience
# ==========================================================================
#
# Le clonage structurel recopie le <head> de la source espagnole. Tant que
# celle-ci porte les traceurs, la sortie FR les herite — mais on ne peut pas en
# dependre : 28 articles ES viennent de template-article.html, et rien ne
# garantit qu'une source future les aura. L'insertion est donc faite ici aussi,
# et elle est idempotente : si les blocs sont deja la, elle ne fait rien.
#
# Repris a l'identique des landings : meme identifiant GA4, meme extrait
# Clarity, meme ordre, tout a la fin du <head>, apres le JSON-LD.

TRACKING = """<!-- Google Analytics GA4 -->
<script defer src="https://www.googletagmanager.com/gtag/js?id=G-MT6S7CH7N9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-MT6S7CH7N9');
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "wb9354sv4p");
</script>"""

GA4_ID = 'G-MT6S7CH7N9'
CLARITY_ID = 'wb9354sv4p'


def ensure_tracking(s):
    """Insere gtag + Clarity en fin de <head> si absents. Idempotent."""
    if GA4_ID in s and CLARITY_ID in s:
        return s, False
    if '</head>' not in s:
        return s, False
    return s.replace('</head>', TRACKING + '\n</head>', 1), True


def adapt_head(s, es_slug, out_slug, prof):
    """lang, canonical, hreflang, Open Graph : passage a la langue cible."""
    fr_url = prof.url(out_slug)

    s = re.sub(r'<html lang="[^"]*">', '<html lang="%s">' % prof.html_lang, s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">',
               '<link rel="canonical" href="%s">' % fr_url, s, count=1)

    # hreflang : les 4 langues, x-default sur l'espagnol (version de reference).
    # La langue cible remplace l'entree correspondante ; les autres pointent vers
    # le slug espagnol, faute de connaitre les slugs localises des autres langues.
    alts = [('es', '%s/blog/es/%s' % (BASE, es_slug)),
            ('ca-ES', '%s/blog/val/%s' % (BASE, es_slug)),
            ('en', '%s/blog/en/%s' % (BASE, es_slug)),
            ('fr', '%s/blog/fr/%s' % (BASE, es_slug)),
            ('x-default', '%s/blog/es/%s' % (BASE, es_slug))]
    alts = [(h, fr_url if h == prof.hreflang else u) for h, u in alts]
    block = '\n'.join('    <link rel="alternate" hreflang="%s" href="%s">' % a for a in alts)
    s, n = re.subn(r'(?:[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?)+',
                   block + '\n', s, count=1)
    if not n:
        s = s.replace('<link rel="canonical"', block + '\n    <link rel="canonical"', 1)

    s = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
               lambda m: m.group(1) + fr_url + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:locale" content=")[^"]*(")',
               lambda m: m.group(1) + prof.og_locale + m.group(2), s, count=1)

    s, _ = ensure_tracking(s)
    return s


def es_to_fr_slugs(prof=None):
    """{slug ES: slug FR} d'apres les payloads de traduction presents sur disque.

    La correspondance n'est PAS l'identite : « citas-locales-nap-que-son-por-que-
    importan » devient « citations-locales-nap-guide-complet ». Une version
    anterieure de retarget_links substituait /blog/es/X -> /blog/fr/X a slug
    constant ; comme aucun fichier FR ne porte un slug espagnol, la regle ne
    s'appliquait jamais et TOUS les liens internes des articles FR continuaient
    de pointer vers l'espagnol.
    """
    prof = prof or PROFILES['fr']
    out = {}
    for path in glob.glob(os.path.join(TRANSLATIONS_DIR, '*.json')):
        try:
            payload = json.load(open(path, encoding='utf-8'))
        except (ValueError, OSError):
            continue
        if payload.get('lang', 'fr') != prof.code:
            continue
        es = os.path.basename(payload.get('source_file', ''))[:-5]
        fr = os.path.basename(path)[:-5]
        if es and os.path.isfile(os.path.join(ROOT, 'blog', prof.directory,
                                              fr + '.html')):
            out[es] = fr
    return out


def retarget_links(s, fr_slug, prof, mapping=None):
    """Repointe les liens internes vers la version FR quand elle existe.

    Trois formes rencontrees dans les sources ES :
      /blog/es/{slug}         articles HTML autonomes
      /blog/es/{slug}.html    idem, avec extension
      /blog/{slug}            les 6 articles historiques du SPA React
    Un lien dont la traduction n'existe pas reste sur l'espagnol : mieux vaut
    une page espagnole qu'un 404.

    Le selecteur de langue et les auto-references sont exclus : ils pointent
    vers l'autre version DU MEME article, ce qui est le comportement voulu.
    """
    m = es_to_fr_slugs(prof) if mapping is None else mapping

    def repl(match):
        slug = match.group('slug')
        fr = m.get(slug)
        if not fr or fr == fr_slug:
            return match.group(0)
        return match.group('pre') + '/blog/%s/' % prof.directory + fr

    return re.sub(
        r'(?P<pre>href=")(?:https://webautonomos\.es)?/blog/(?:es/)?'
        r'(?P<slug>[a-z0-9-]+)(?:\.html)?(?=")',
        repl, s)


NAP_FOOTER = """
    <footer style="background:linear-gradient(135deg,#1a3a8f 0%,#1a7a5a 50%,#22c55e 100%); padding:24px 6%; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px; margin-top:48px;">
        <a href="{base}" style="font-weight:800; font-size:1rem; color:rgba(255,255,255,0.85); text-decoration:none;">&#127760; webautonomos.es</a>
        <div style="display:flex; gap:20px; flex-wrap:wrap;">
            <a href="{base}/aviso-legal" style="color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.9rem;">Mentions légales</a>
            <a href="{base}/privacidad" style="color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.9rem;">Confidentialité</a>
            <a href="{base}/contacto" style="color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.9rem;">Contact</a>
        </div>
        <address style="flex-basis:100%; order:3; margin-top:4px; padding-top:16px; border-top:1px solid rgba(255,255,255,0.12); font-style:normal; font-size:0.78rem; line-height:1.7; color:rgba(255,255,255,0.55); display:flex; flex-direction:column; gap:1px;">
            <strong>WebAutonomos</strong>
            <span>Calle Pintor Josep Segrelles, 26</span>
            <span>46870 Ontinyent, Valencia</span>
            <a href="tel:+34961877356" style="color:rgba(255,255,255,0.55); text-decoration:none;">+34 961 877 356</a>
            <a href="mailto:info@webautonomos.es" style="color:rgba(255,255,255,0.55); text-decoration:none;">info@webautonomos.es</a>
        </address>
    </footer>
""".replace('{base}', BASE)


def assemble(src, payload, prof=None):
    """Clone le document source en substituant les fragments traduits."""
    prof = prof or PROFILES['fr']
    by_id = {seg['id']: seg for seg in payload['segments']}
    s = src

    # --- blocs du corps : de la fin vers le debut, pour garder les offsets valides
    blocks = [seg for seg in payload['segments'] if seg['id'].startswith('block:')]
    for seg in sorted(blocks, key=lambda x: -x['offset'][0]):
        a, b = seg['offset']
        original = src[a:b]
        lead = original[:len(original) - len(original.lstrip())]
        trail = original[len(original.rstrip()):]
        s = s[:a] + lead + seg['fr'] + trail + s[b:]

    # --- metadonnees du <head>
    for name, pattern in META_FIELDS:
        seg = by_id.get('meta:' + name)
        if not seg:
            continue
        is_attr = name != 'title'
        value = H.escape(seg['fr'], quote=is_attr)
        s = re.sub(pattern, lambda m: m.group(1) + value + m.group(3),
                   s, count=1, flags=re.S)

    # --- blocs JSON-LD : reserialises depuis la structure, jamais bricoles en texte
    def set_path(node, path, value):
        cur = node
        for key in path[:-1]:
            cur = cur[int(key)] if isinstance(cur, list) else cur[key]
        last = path[-1]
        if isinstance(cur, list):
            cur[int(last)] = value
        else:
            cur[last] = value

    # Les substitutions sont calculees d'abord, puis appliquees de la FIN vers le
    # DEBUT : remplacer en avancant invaliderait les offsets des blocs suivants.
    edits = []
    for bi, m in enumerate(jsonld_blocks(s)):
        try:
            data = json.loads(m.group(2))
        except json.JSONDecodeError:
            continue
        changed = False
        prefix = 'jsonld:%d:' % bi
        for seg in payload['segments']:
            if not seg['id'].startswith(prefix) or not seg['fr']:
                continue
            set_path(data, seg['id'][len(prefix):].split('.'), seg['fr'])
            changed = True
        if changed:
            edits.append((m.start(), m.end(),
                          m.group(1) + '\n' + json.dumps(data, ensure_ascii=False, indent=8)
                          + '\n    ' + m.group(3)))
    for start, end, new_text in sorted(edits, reverse=True):
        s = s[:start] + new_text + s[end:]

    s = adapt_head(s, payload['es_slug'], payload['fr_slug'], prof)
    s = retarget_links(s, payload['fr_slug'], prof)

    # --- pied de page NAP, insere AVANT </article> : le document doit se terminer
    # exactement par </article></body></html>, sans rien entre les trois.
    if 'Pintor Josep Segrelles' not in s:
        if '</article>' in s:
            s = s.replace('</article>', NAP_FOOTER + '    </article>', 1)
        else:
            s = s.replace('</body>', NAP_FOOTER + '</body>', 1)
    return s


# ==========================================================================
# 4. Controle d'integrite — BLOQUANT
# ==========================================================================

def integrity(out, src, prof=None):
    """[(ok, libelle, detail)] — l'ecriture n'a lieu que si tous les ok sont True."""
    prof = prof or PROFILES['fr']
    checks = []

    # Le document doit se fermer proprement. Deux dispositions valides coexistent
    # dans le repo : le pied de page NAP a l'interieur de <article> (sortie de ce
    # script) ou juste apres (sortie de generate_spa_articles.py). Ce qui est
    # verifie, c'est l'invariant commun : <article> ferme, et le fichier se
    # termine par </body></html>. Une troncature echoue dans les deux cas.
    # <article> n'est exige que si la SOURCE en contient un : reservas-online-
    # autonomos-2026 est bati sans <article>, et l'exiger en absolu bloquait une
    # sortie pourtant complete. L'invariant reel est : la sortie se ferme comme
    # la source. Une troncature echoue toujours sur la fin de document.
    tail = out.rstrip()
    needs_article = '</article>' in src
    closes = (re.search(r'</body>\s*</html>$', tail) is not None
              and ('</article>' in out if needs_article else True))
    checks.append((closes,
                   'document ferme : %sfin sur </body></html>'
                   % ('</article> present, ' if needs_article else ''),
                   '...' + repr(tail[-34:])))

    masked = mask_raw_text(out)
    stack, orphans = [], []
    for m, is_close, name, self_closing in iter_tags(masked):
        if name in VOID or self_closing:
            continue
        if is_close:
            if stack and stack[-1] == name:
                stack.pop()
            else:
                orphans.append(name)
        else:
            stack.append(name)
    checks.append((not stack and not orphans, 'balises equilibrees, pile ouverte vide',
                   'pile=%s orphelines=%s' % (stack[:5], orphans[:5])))

    for label, pattern in (('<!DOCTYPE>', r'(?i)<!DOCTYPE'), ('<html>', r'<html\b'),
                           ('<body>', r'<body\b'), ('<title>', r'<title\b')):
        n = len(re.findall(pattern, out))
        checks.append((n == 1, 'exactement un %s' % label, 'trouve %d' % n))

    n_src = len(re.findall(r'<details\b', src))
    n_out = len(re.findall(r'<details\b', out))
    checks.append((n_out == n_src, '<details> == questions FAQ de la source',
                   'source=%d sortie=%d' % (n_src, n_out)))

    h_src = len(re.findall(r'<h2\b', src))
    h_out = len(re.findall(r'<h2\b', out))
    checks.append((h_out == h_src, '<h2> == source', 'source=%d sortie=%d' % (h_src, h_out)))

    # Le controle de registre ne vaut que pour le francais : en espagnol le
    # tutoiement est la norme editoriale du site, et « tu » y est partout.
    # Les deux controles linguistiques ne valent que pour la langue cible : sur un
    # document espagnol ils n'ont aucun sens, le castillan y est la norme.
    if re.search(r'<html[^>]*\blang="%s"' % prof.html_lang, out):
        hits = prof.register(out)
        checks.append((not hits, prof.register_label,
                       ('%d occurrence(s) : ' % len(hits)) + '; '.join(h[0] + ' -> ' + h[1]
                        for h in hits[:6]) if hits else 'zero occurrence'))
        # Couvre TOUT le fichier, <pre>/<code> et attributs compris : c'est
        # precisement ce que les segments extraits laissaient passer.
        res = prof.residue(out)
        checks.append((not res, 'aucun residu espagnol (fichier entier)',
                       ('%d occurrence(s) : ' % len(res)) + ' | '.join(
                           'l.%d %s « %s »' % (h[0], h[1], h[2]) for h in res[:8])
                       if res else 'zero occurrence'))
    else:
        checks.append((True, 'registre', 'document hors langue cible : controle sans objet'))
        checks.append((True, 'residu espagnol', 'document hors langue cible : controle sans objet'))

    w_src, w_out = len(visible_words(src)), len(visible_words(out))
    ratio = w_out / w_src if w_src else 0
    checks.append((ratio >= MIN_WORD_RATIO,
                   'mots >= %d%% de la source' % (MIN_WORD_RATIO * 100),
                   'source=%d sortie=%d ratio=%.1f%%' % (w_src, w_out, ratio * 100)))
    return checks


# Detection du tutoiement residuel. On travaille sur le TEXTE VISIBLE seulement :
# les attributs HTML (style, class, href) contiennent des fragments comme "gratuit"
# ou "status" qui declencheraient de faux positifs.
# Detection du tutoiement residuel, sur le TEXTE VISIBLE seulement (les attributs
# HTML contiennent des fragments qui declencheraient de faux positifs).
#
# Piege principal : pour les verbes du 1er groupe, l'imperatif singulier et la 3e
# personne du singulier sont homographes — « utilise » vaut aussi bien pour
# « utilise le format WebP » (tutoiement) que pour « Google utilise » (3e pers.).
# On ne peut donc PAS se contenter de chercher la forme nue. Trois familles :
#   1. marqueurs non ambigus  : tu, ton, ta, tes, toi, t', tien
#   2. present 2e pers. sing. : formes qui n'existent qu'au tutoiement (as, peux,
#      dois...) et verbes du 1er groupe en -es (utilises, cherches...)
#   3. imperatif singulier    : forme nue, mais UNIQUEMENT en debut de phrase,
#      la ou un sujet ne peut pas la preceder.

UNAMBIGUOUS = [
    (r"\btu\b", 'pronom « tu »'),
    # « ton » est aussi un nom commun (« un ton professionnel »). On l'exclut
    # quand il est precede d'un determinant qui impose la lecture nominale.
    (r"(?<!\bun )(?<!\ble )(?<!\bce )(?<!\bdu )(?<!\bau )(?<!\bmon )(?<!\bson )"
     r"(?<!\bvotre )(?<!\bnotre )(?<!\bleur )(?<!\bmeme )(?<!\bmême )(?<!\bbon )\bton\b",
     'possessif « ton »'),
    (r"\bta\b", 'possessif « ta »'),
    (r"\btes\b", 'possessif « tes »'),
    (r"\btoi\b", 'pronom « toi »'),
    (r"\bt'(?:a|as|es|y|en|in)\b", "elision « t' »"),
    (r"\btien(?:s|ne|nes)?\b", 'possessif « tien »'),
]

# Verbes du 1er groupe susceptibles d'apparaitre a l'imperatif dans ce type de texte.
ER_VERBS = [
    'utilise', 'compresse', 'ajoute', 'regarde', 'cherche', 'corrige', 'identifie',
    'observe', 'consulte', 'evite', 'évite', 'commence', 'verifie', 'vérifie',
    'optimise', 'publie', 'demande', 'cree', 'crée', 'garde', 'copie', 'envisage',
    'migre', 'pense', 'essaie', 'indique', 'redige', 'rédige',
    'depasse', 'dépasse', 'oublie', 'imagine', 'considere', 'considère',
]

# Formes du present qui n'existent QU'A la 2e personne du singulier.
# Piege : en francais la 1re et la 2e personne du singulier sont homographes pour
# presque tous les verbes — « je peux / tu peux », « je fais / tu fais »,
# « je suis / tu suis ». Une premiere version listait ces formes et signalait
# « Je suis auto-entrepreneur » comme du tutoiement. Seuls 'as' et 'vas' sont
# vraiment discriminants (1re personne : « j'ai », « je vais »). Pour tout le
# reste, c'est le pronom « tu » qui fait foi — il est de toute facon quasiment
# toujours present en francais.
PRESENT_2S = ['as', 'vas']


def tutoiement_hits(html_text):
    """[(extrait, motif)] des formes de tutoiement dans le texte visible."""
    body = html_text[html_text.find('<body'):] or html_text
    text = re.sub(r'(?is)<(script|style)\b[^>]*>.*?</\1>', ' ', body)
    # Chaque bloc commence une phrase : sans ce marqueur, un imperatif place en
    # tete de paragraphe (« Utilisez le format WebP ») n'aurait aucune ponctuation
    # devant lui apres le retrait des balises, et echapperait a la regle.
    text = re.sub(r'(?i)</(p|h[1-6]|li|div|summary|dt|dd|td|th|blockquote)>', ' . ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = H.unescape(re.sub(r'\s+', ' ', text)).strip()
    # Les exemples cites (requetes, titres) sont hors perimetre.
    text = re.sub(r'«[^»]*»', ' ', text)
    text = re.sub(r'"[^"]*"', ' ', text)

    patterns = list(UNAMBIGUOUS)
    patterns.append((r"\b(?:%s)\b" % '|'.join(PRESENT_2S), 'present 2e personne du singulier'))
    # Pas de regle sur les formes en -es : en francais le pronom sujet est
    # obligatoire, donc « tu utilises » est deja attrape par le motif « tu ».
    # La regle etait donc redondante, et elle heurtait des noms communs
    # homographes — « les demandes d'itineraire », « les gardes », « les notes ».
    # imperatif singulier : forme nue en tete de phrase uniquement
    patterns.append((r"(?:^|(?<=[.!?:;])\s{1,3})(?:%s)\b" % '|'.join(ER_VERBS),
                     'imperatif singulier en tete de phrase ou de bloc'))

    hits = []
    for pattern, label in patterns:
        for m in re.finditer(pattern, text, re.I):
            around = text[max(0, m.start() - 32):m.end() + 32].strip()
            hits.append((around, label))
    return hits


# ==========================================================================
# Localisation de l'habillage partage
# ==========================================================================
#
# Le corps de l'article passe par l'extraction, mais pas l'habillage : barre de
# navigation, bouton CTA, serviceType du JSON-LD, badge de categorie. Ces blocs
# viennent de template-article.html, en espagnol, et le clonage structurel les
# recopie tels quels — un article FR sortait donc avec « Servicios / Precios /
# Ver mi web gratis ». Sans cette passe, le probleme revient a chaque build.
#
# Chaque substitution est ancree sur son balisage (« >Servicios</a> », pas
# « Servicios ») : elle ne peut donc pas toucher la prose de l'article.
#
# Ce qui N'EST PAS traduit, parce que ce sont des faits sur l'entreprise :
# le NAP, le telephone, « Comunidad Valenciana », addressCountry ES, et les
# liens vers /blog/es/ qui pointent vers la version espagnole.

CHROME_FR = [
    # barre de navigation
    ('>Inicio</a>',            '>Accueil</a>'),
    ('>Servicios</a>',         '>Services</a>'),
    ('>Precios</a>',           '>Tarifs</a>'),
    ('>Contacto</a>',          '>Contact</a>'),
    ('>Ver mi web gratis</a>', '>Voir mon site gratuit</a>'),
    # boutons CTA
    ('>Solicitar mi web gratis<', '>Demander mon site gratuitement<'),
    ('Pedir presupuesto gratis →', 'Demander un devis gratuit →'),
    # badges et fil d'Ariane de categorie
    ('>P\u00e1ginas Web<',      '>Sites web<'),
    ('>Marketing Digital<',    '>Marketing digital<'),
    ('>Facturaci\u00f3n y Legal<', '>Facturation et juridique<'),
    ('>Automatizaci\u00f3n<',    '>Automatisation<'),
    # pied de page
    ('>Aviso legal</a>',       '>Mentions l\u00e9gales</a>'),
    ('>Privacidad</a>',        '>Confidentialit\u00e9</a>'),
    ('>Contacto</a>',          '>Contact</a>'),
    ('← Volver al blog',       '← Retour au blog'),
]


# Valeurs du JSON-LD Organization. Elles sont indentees sur plusieurs lignes :
# la substitution doit passer par une regex, pas par un litteral.
CHROME_FR_RE = [
    # \u00e9 dans un remplacement re est une echappement invalide : on ecrit le
    # caractere, pas sa notation.
    ('("serviceType"\\s*:\\s*\\[\\s*")Dise\u00f1o web(")',
     '\\g<1>Cr\u00e9ation de sites web\\g<2>',
     'serviceType : Dise\u00f1o web'),
]


def localize_chrome(out, prof):
    """Traduit l'habillage partage. Retourne (texte, [(motif, occurrences)])."""
    applied = []
    for src_txt, fr_txt in prof.chrome:
        n = out.count(src_txt)
        if n:
            out = out.replace(src_txt, fr_txt)
            applied.append((src_txt, n))
    for pattern, repl, label in prof.chrome_re:
        out, n = re.subn(pattern, repl, out)
        if n:
            applied.append((label, n))
    return out, applied


# ==========================================================================
# Detection du residu espagnol
# ==========================================================================
#
# Motivation : l'extraction ne couvre que les blocs de texte reconnus. Un
# exemple de code dans <pre><code> (le JSON-LD modele de l'article Schema)
# n'y figure pas, donc ses valeurs espagnoles — « Fontaneria Lopez Elda »,
# « +34 966 123 456 », « addressCountry: ES » — survivaient intactes a une
# traduction jugee complete. Ce controle-ci ne lit PAS les segments : il lit
# le fichier produit, en entier, attributs et <pre>/<code> compris.
#
# Le prix a payer est une liste d'exceptions, car un article FR contient
# legitimement de l'espagnol :
#   - les URL du site (webautonomos.es/blog/es/..., /aviso-legal, /pide-tu-demo)
#   - le NAP reel de l'entreprise (Ontinyent, Valencia, +34 961 877 356)
#   - le selecteur de langue (title="Espanol", hreflang="es", og:locale)
# Ces zones sont neutralisees AVANT l'analyse, en conservant la longueur du
# texte pour que les numeros de ligne restent exacts.

# Faits WebAutonomos : ne se transposent jamais (cf. CLAUDE.md, cible FR).
WA_LITERALS = [
    'Calle Pintor Josep Segrelles, 26',
    '46870 Ontinyent, Valencia',
    '+34 961 877 356',
    '+34961877356',
    'Ontinyent',
    'Comunidad Valenciana',
    'WebAutonomos.es',
    'WebAutonomos',
    'webautonomos',
]

# Attributs qui ne portent pas de prose : les analyser ne produit que du bruit.
NOISE_ATTRS = ('class', 'style', 'id', 'd', 'viewBox', 'fill', 'width', 'height',
               'xmlns', 'rel', 'type', 'charset', 'property', 'itemprop', 'href',
               'src', 'lang', 'hreflang', 'sizes', 'crossorigin', 'as')

# 1. Caracteres qui n'existent pas en francais.
ES_CHARS = (r'[\u00f1\u00d1\u00bf\u00a1\u00e1\u00ed\u00f3\u00fa\u00c1\u00cd\u00d3\u00da]',
            'caractere espagnol')

# 2. Mots espagnols frequents SANS homographe francais. Tout mot qui existe aussi
#    en francais est exclu de la liste (la, le, les, des, un, une, en, sur, par,
#    pour, avec, sans, dans, entre, sobre, bien, se, si, no, or, plus, mais...) :
#    un faux positif bloquerait une traduction correcte, ce qui est pire que rien.
ES_WORDS = [
    'el', 'los', 'las', 'del', 'al', 'una', 'unos', 'unas', 'con', 'sin', 'por',
    'para', 'como', 'cuando', 'donde', 'pero', 'muy', 'este', 'esta', 'estos',
    'estas', 'ese', 'esa', 'eso', 'esto', 'tiene', 'tienen', 'tienes', 'puede',
    'pueden', 'puedes', 'hacer', 'hace', 'hacen', 'ser', 'fue', 'hay',
    'desde', 'hasta', 'cada', 'mismo', 'misma', 'todo', 'todos', 'toda', 'todas',
    'otro', 'otros', 'otra', 'otras', 'mejor', 'mejores', 'mucho', 'muchos',
    'poco', 'pocos', 'nada', 'algo', 'alguien', 'porque', 'aunque', 'mientras',
    'incluso', 'siempre', 'nunca', 'ahora', 'negocio', 'negocios', 'empresa',
    'empresas', 'autonomo', 'autonomos', 'ficha', 'fichas',
    'resena', 'resenas', 'busqueda', 'busquedas', 'usuario', 'usuarios',
    'servicios', 'producto', 'productos', 'trabajo', 'ciudad', 'precio',
    'precios', 'espana', 'espanol', 'espanola', 'espanoles', 'hacienda',
    'seguridad', 'volver', 'gratis', 'ejemplo', 'ejemplos', 'consejo', 'aqui',
]

# 3. Villes et provinces espagnoles employees comme exemples pedagogiques.
#    Ontinyent est absent : c'est le siege de WebAutonomos, deja neutralise.
ES_CITIES = [
    'Valencia', 'Alicante', 'Elda', 'Elche', 'Petrer', 'Novelda', 'Monovar',
    'Sax', 'Crevillente', 'Santa Pola', 'Benimaclet', 'Altabix', 'Madrid',
    'Barcelona', 'Sevilla', 'Zaragoza', 'Malaga', 'Murcia', 'Castellon',
    'Alcoy', 'Alcoi', 'Gandia', 'Torrevieja', 'Benidorm', 'Xativa', 'Denia',
    'Villena', 'Aspe',
]


def _blank(m):
    """Remplace par des espaces de meme longueur : les lignes ne bougent pas."""
    return re.sub(r'[^\n]', ' ', m.group(0))


def mask_legitimate_spanish(html_text):
    """Neutralise les zones ou l'espagnol est legitime, longueur preservee."""
    s = html_text
    # <style> et <script> non-JSON-LD : du code, pas de la prose. Le JSON-LD est
    # conserve — c'est la que vit addressCountry.
    s = re.sub(r'(?is)<style\b[^>]*>.*?</style>', _blank, s)
    s = re.sub(r'(?is)<script\b(?![^>]*ld\+json)[^>]*>.*?</script>', _blank, s)
    # URL : un lien vers /blog/es/<slug-espagnol> est la version ES, pas un residu.
    s = re.sub(r'https?://[^\s"\'<>]+', _blank, s)
    s = re.sub(r'(?i)\b(?:href|src|content)\s*=\s*"(?:/|#|mailto:|tel:)[^"]*"', _blank, s)
    # Attributs sans prose.
    s = re.sub(r'(?i)\b(?:%s)\s*=\s*"[^"]*"' % '|'.join(NOISE_ATTRS), _blank, s)
    # Selecteur de langue et og:locale.
    s = re.sub(r'(?i)title\s*=\s*"(?:Espa\u00f1ol|Valenci\u00e0|English|Fran\u00e7ais)"', _blank, s)
    s = re.sub(r'(?i)"[a-z]{2}_[A-Z]{2}"', _blank, s)
    # Bloc PostalAddress de WebAutonomos : « Ontinyent » l'identifie de facon
    # sure. addressRegion Valencia et addressCountry ES y sont des faits.
    s = re.sub(r'(?s)\{[^{}]*Ontinyent[^{}]*\}', _blank, s)
    # Le logo coupe en trois <span> : web | autonomos | .es
    s = re.sub(r'>autonomos</span>', _blank, s)
    # Faits WebAutonomos.
    for lit in WA_LITERALS:
        s = re.sub(re.escape(lit), _blank, s, flags=re.I)
    return s


def spanish_residue_hits(html_text):
    """[(ligne, motif, extrait)] du residu espagnol dans TOUT le fichier."""
    masked = mask_legitimate_spanish(html_text)
    # Comparaison insensible aux accents pour la liste de mots : « busqueda »
    # attrape « busqueda » comme « b\u00fasqueda ». Les accents eux-memes sont
    # traites par ES_CHARS, sur le texte non deplie.
    folded = ''.join(
        unicodedata.normalize('NFD', c)[0] if unicodedata.combining(
            unicodedata.normalize('NFD', c)[-1]) else c
        for c in masked)

    patterns = [
        (ES_CHARS[0], ES_CHARS[1], masked, 0),
        (r'\b(?:%s)\b' % '|'.join(ES_WORDS), 'mot espagnol', folded, re.I),
        (r'\b(?:%s)\b' % '|'.join(ES_CITIES), 'ville espagnole', folded, 0),
        (r'\+\s?34\b', 'indicatif telephonique +34', masked, 0),
        (r'(?i)"addressCountry"\s*:\s*"ES"', 'addressCountry ES', masked, 0),
        (r'(?i)"addressRegion"\s*:\s*"(?:Alicante|Valencia|Castell)', 'addressRegion espagnole',
         masked, 0),
    ]

    hits, seen = [], set()
    for pattern, label, subject, flags in patterns:
        for m in re.finditer(pattern, subject, flags):
            line = subject.count('\n', 0, m.start()) + 1
            key = (line, m.start())
            if key in seen:
                continue
            seen.add(key)
            raw = html_text[max(0, m.start() - 40):m.end() + 40]
            hits.append((line, label, m.group(0).strip(), ' '.join(raw.split())))
    hits.sort()
    return hits


# ==========================================================================
# Profils de langue
# ==========================================================================
#
# Le script a ete ecrit pour le francais, et le francais s'y etait infiltre a
# dix endroits : chemin de sortie, attribut lang, og:locale, ordre des
# hreflang, table d'habillage, blocs de pre-remplissage, liste du controle de
# residu, garde de registre, table de correspondance des slugs, et le repertoire
# balaye par retarget-all. Tout cela est desormais reuni dans un objet par
# langue ; les fonctions structurelles — leaf_blocks, assemble, les controles de
# fermeture, d'equilibre de balises, de comptage et de ratio de mots — n'ont
# jamais eu de langue et n'en prennent pas.
#
# Note de compatibilite : le champ des segments s'appelle toujours 'fr', et la
# clef du payload 'fr_slug'. Ces noms datent de l'epoque ou le francais etait la
# seule cible ; les renommer casserait les 44 payloads existants. Lire « langue
# cible » partout ou il est ecrit « fr ».


class LangProfile:
    def __init__(self, code, html_lang, directory, og_locale, hreflang,
                 chrome, chrome_re, prefill_blocks, prefill_jsonld, months,
                 passthrough, residue, register, register_label, read_label):
        self.code = code                    # cle CLI : 'fr', 'val'
        self.html_lang = html_lang          # attribut <html lang="...">
        self.directory = directory          # blog/<directory>/
        self.og_locale = og_locale
        self.hreflang = hreflang            # code hreflang de CETTE langue
        self.chrome = chrome                # [(source, cible)] litteral
        self.chrome_re = chrome_re          # [(motif, remplacement, libelle)]
        self.prefill_blocks = prefill_blocks
        self.prefill_jsonld = prefill_jsonld
        self.months = months
        self.passthrough = passthrough      # regex des blocs recopies tels quels
        self.residue = residue              # html -> [(ligne, motif, token, extrait)]
        self.register = register            # html -> [(extrait, motif)]
        self.register_label = register_label
        self.read_label = read_label     # « min de lectura » -> libelle cible

    def url(self, slug):
        return '%s/blog/%s/%s' % (BASE, self.directory, slug)


# --------------------------------------------------------------------------
# Valencien : habillage. Repris des libelles de generate_spa_articles.py, qui
# sert deja le valencien depuis les donnees SPA — meme vocabulaire, donc.
# --------------------------------------------------------------------------

CHROME_VAL = [
    ('>Inicio</a>',               '>Inici</a>'),
    ('>Servicios</a>',            '>Serveis</a>'),
    ('>Precios</a>',              '>Preus</a>'),
    ('>Contacto</a>',             '>Contacte</a>'),
    ('>Ver mi web gratis</a>',    '>Veure la meua web gratis</a>'),
    ('>Solicitar mi web gratis<', '>Sol\u00b7licitar la meua web gratis<'),
    ('Pedir presupuesto gratis \u2192', 'Demanar pressupost gratis \u2192'),
    ('>P\u00e1ginas Web<',         '>P\u00e0gines Web<'),
    ('>Marketing Digital<',       '>M\u00e0rqueting Digital<'),
    ('>Facturaci\u00f3n y Legal<',  '>Facturaci\u00f3 i Legal<'),
    ('>Automatizaci\u00f3n<',       '>Automatitzaci\u00f3<'),
    # Variantes espacees : le gabarit ecrit « > Paginas Web < » avec des blancs,
    # que la forme collee ne rattrape pas.
    (' P\u00e1ginas Web ',          ' P\u00e0gines Web '),
    (' Marketing Digital ',       ' M\u00e0rqueting Digital '),
    (' SEO Local ',               ' SEO Local '),
    (' Google My Business ',      ' Google My Business '),
    (' Presencia Digital ',       ' Presencia Digital '),
    ('Art\u00edculos relacionados',  'Articles relacionats'),
    ('min de lectura',            'min de lectura'),
    ('>Aviso legal</a>',          '>Av\u00eds legal</a>'),
    ('>Privacidad</a>',           '>Privacitat</a>'),
    ('\u2190 Volver al blog',       '\u2190 Tornar al blog'),
]

CHROME_VAL_RE = [
    ('("serviceType"\\s*:\\s*\\[\\s*")Dise\u00f1o web(")',
     '\\g<1>Disseny web\\g<2>', 'serviceType : Dise\u00f1o web'),
]

MONTHS_ES_VAL = {
    'enero': 'gener', 'febrero': 'febrer', 'marzo': 'mar\u00e7', 'abril': 'abril',
    'mayo': 'maig', 'junio': 'juny', 'julio': 'juliol', 'agosto': 'agost',
    'septiembre': 'setembre', 'octubre': 'octubre', 'noviembre': 'novembre',
    'diciembre': 'desembre',
}

PREFILL_BLOCKS_VAL = {
    'W': 'W',
    'WebAutonomos': 'WebAutonomos',
    'Preguntas frecuentes': 'Preguntes freq\u00fcents',
    '\U0001F4D1 Contenido del art\u00edculo': "\U0001F4D1 Contingut de l'article",
    '\u00bfQuieres una web as\u00ed para tu negocio?':
        'Vols una web aix\u00ed per al teu negoci?',
    'P\u00e1ginas web profesionales desde 15 \u20ac/mes \u00b7 Sin permanencia':
        'P\u00e0gines web professionals des de 15 \u20ac/mes \u00b7 Sense perman\u00e8ncia',
    'Agencia web especializada en aut\u00f3nomos de la Comunidad Valenciana. '
    'P\u00e1ginas web profesionales desde 15 \u20ac/mes, sin permanencia.':
        'Ag\u00e8ncia web especialitzada en aut\u00f2noms de la Comunitat Valenciana. '
        'P\u00e0gines web professionals des de 15 \u20ac/mes, sense perman\u00e8ncia.',
    '\u00bfCu\u00e1nto cuesta y cu\u00e1nto tarda?': 'Quant costa i quant tarda?',
    '15 euros al mes, sin alta y sin permanencia, o 349 euros en pago \u00fanico. '
    'Tu web est\u00e1 lista en 24 horas.':
        '15 \u20ac/mes, sense alta i sense perman\u00e8ncia, o 349 euros en pagament '
        '\u00fanic. La teua web est\u00e0 llesta en 24 hores.',
}

PREFILL_JSONLD_VAL = {
    'jsonld:0:author.name': 'WebAutonomos',
    'jsonld:0:publisher.name': 'WebAutonomos',
    'jsonld:1:itemListElement.0.name': 'Inici',
    'jsonld:1:itemListElement.1.name': 'Blog',
    'jsonld:3:name': 'WebAutonomos',
    'jsonld:3:description': "Ag\u00e8ncia de m\u00e0rqueting digital especialitzada en "
                            'p\u00e0gines web i SEO local per a aut\u00f2noms de la '
                            'Comunitat Valenciana',
    'jsonld:3:areaServed.name': 'Comunitat Valenciana',
    'jsonld:4:name': 'Blog WebAutonomos.es',
    'jsonld:4:description': 'Consells i guies de SEO local i m\u00e0rqueting digital '
                            'per a aut\u00f2noms',
    'jsonld:4:publisher.name': 'WebAutonomos.es',
}

# --------------------------------------------------------------------------
# Valencien : controle de residu castillan
# --------------------------------------------------------------------------
#
# Beaucoup plus delicat qu'en francais, parce que castillan et catalan
# partagent une large part de leur lexique et que la frontiere passe souvent
# par un seul accent. Deux regles tirees d'un premier essai rate, qui signalait
# 250 formes correctes :
#
#   1. NE JAMAIS replier les accents. En catalan l'accent EST le discriminant :
#      pero/pero`, son/son', pagina/pa`gina, esta/esta`. Replier revient a
#      declarer fautif du valencien impeccable.
#   2. Ecarter ce que le valencien possede en propre. « este / esta / estos /
#      estes » sont les demonstratifs valenciens normatifs, « ser » et « busca »
#      sont des verbes catalans, « gratis » est catalan, « Valencia » est la
#      graphie catalane de la ville.
#
# Ne subsistent que des formes sans aucun equivalent catalan.

VAL_ES_CHARS = (r'[\u00f1\u00d1]', 'caractere castillan')   # le catalan ecrit 'ny'

VAL_ES_WORDS = [
    # fonctionnels — catalan : amb, sense, pero`, molt, cap a, des de, fins
    'con', 'sin', 'pero', 'muy', 'hacia', 'hasta', 'desde', 'aunque', 'porque',
    'tambien', 'tambi\u00e9n', 'segun', 'seg\u00fan', 'despues', 'despu\u00e9s',
    'siempre', 'nunca', 'ahora', 'mientras', 'incluso', 'mismo', 'misma',
    'otro', 'otra', 'otros', 'otras', 'mucho', 'muchos', 'mucha', 'muchas',
    'poco', 'pocos', 'nada', 'algo', 'alguien', 'todo', 'todos', 'toda',
    'todas', 'los', 'las', 'mas', 'm\u00e1s', 's\u00f3lo', 'solo',
    # verbes — catalan : fer, te, pot
    'hacer', 'hace', 'hacen', 'hacemos', 'tiene', 'tienen', 'tienes', 'puede',
    'pueden', 'puedes', 'necesitas', 'quieres', 'debes', 'llamada',
    # noms — catalan : pa`gina, cerca, ressenya, fitxa, preu, treball, ciutat
    'pagina', 'p\u00e1gina', 'paginas', 'p\u00e1ginas', 'busqueda', 'b\u00fasqueda',
    'busquedas', 'b\u00fasquedas', 'resena', 'rese\u00f1a', 'resenas', 'rese\u00f1as',
    'ficha', 'fichas', 'precio', 'precios', 'trabajo', 'ciudad', 'usuario',
    # « clientes » est ecarte : c'est le pluriel FEMININ catalan de « client »
    # (« les teues clientes »), indiscernable du pluriel castillan. Meme piege
    # qu'en francais, ou il avait deja fallu le retirer.
    'usuarios', 'negocio', 'negocios', 'ejemplo', 'ejemplos',
    'consejo', 'consejos', 'tienda', 'a\u00f1o', 'a\u00f1os',
]

# Toponymes en graphie castillane ; la graphie catalane est legitime et reste.
VAL_ES_CITIES = {'Alicante': 'Alacant', 'Elche': 'Elx'}


def valencian_residue_hits(html_text):
    """[(ligne, motif, token, extrait)] du castillan residuel dans un texte VAL."""
    masked = mask_legitimate_spanish(html_text)
    patterns = [
        (VAL_ES_CHARS[0], VAL_ES_CHARS[1]),
        # Le trait d'union prefixe un pronom enclitique : « respon-los »,
        # « mostra'l », « respon-les » sont du valencien correct. Sans cette
        # garde, le controle signale l'article castillan « los » a l'interieur
        # d'un imperatif parfaitement normatif.
        (r'(?<!-)\b(?:%s)\b' % '|'.join(sorted(VAL_ES_WORDS, key=len, reverse=True)),
         'mot castillan'),
        (r'\b(?:%s)\b' % '|'.join(VAL_ES_CITIES), 'toponyme en graphie castillane'),
    ]
    hits, seen = [], set()
    for pattern, label in patterns:
        for m in re.finditer(pattern, masked):
            if m.start() in seen:
                continue
            seen.add(m.start())
            line = masked.count('\n', 0, m.start()) + 1
            raw = html_text[max(0, m.start() - 40):m.end() + 40]
            hits.append((line, label, m.group(0).strip(), ' '.join(raw.split())))
    hits.sort()
    return hits


# --------------------------------------------------------------------------
# Valencien : garde de registre
# --------------------------------------------------------------------------
#
# Le valencien tutoie, comme le castillan : il n'y a donc rien a verifier du
# cote du registre. La garde porte a la place sur deux points de la normative
# AVL qui se controlent mecaniquement et sans ambiguite. Elle ne pretend pas
# valider la normative dans son ensemble — seulement ce qu'une machine peut
# affirmer sans risque de faux positif.

# La l geminee s'ecrit avec un point volant : instal.lar, non installar.
AVL_GEMINATE = ['installar', 'installacio', 'installaci\u00f3', 'installat',
                'paralel', 'paralela', 'cellula', 'sillaba', 'illusio',
                'illusi\u00f3', 'collaborar', 'collocar', 'collocaci\u00f3',
                'excellent', 'intelligent', 'intellig\u00e8ncia']


def avl_hits(html_text):
    """[(extrait, motif)] des ecarts a la normative AVL detectables sans ambiguite."""
    body = html_text[html_text.find('<body'):] or html_text
    text = re.sub(r'(?is)<(script|style)\b[^>]*>.*?</\1>', ' ', body)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = H.unescape(re.sub(r'\s+', ' ', text))
    hits = []
    # Le catalan normatif n'emploie pas les signes ouvrants castillans.
    for m in re.finditer(r'[\u00bf\u00a1]', text):
        hits.append((text[max(0, m.start() - 30):m.end() + 40].strip(),
                     'signe ouvrant castillan (non normatif en catalan)'))
    for m in re.finditer(r'\b(?:%s)\b' % '|'.join(AVL_GEMINATE), text, re.I):
        hits.append((text[max(0, m.start() - 30):m.end() + 30].strip(),
                     'l geminee sans point volant : %s' % m.group(0)))
    return hits

def report(checks):
    width = max(len(c[1]) for c in checks)
    for ok, label, detail in checks:
        print('  %s  %-*s  %s' % ('OK  ' if ok else 'ECHEC', width, label, detail))
    return all(c[0] for c in checks)


# ==========================================================================
# 5. Commandes build / check
# ==========================================================================

def cmd_build(args):
    prof = profile_for(args.lang)
    payload_path = os.path.join(TRANSLATIONS_DIR, args.fr_slug + '.json')
    if not os.path.isfile(payload_path):
        sys.exit('fichier de traduction introuvable : ' + payload_path + "\nLance d'abord 'extract'.")
    payload = json.load(open(payload_path, encoding='utf-8'))
    src_path = os.path.join(ROOT, payload['source_file'])
    src = open(src_path, encoding='utf-8').read()

    # --- controles PREALABLES sur les segments
    missing = [s['id'] for s in payload['segments'] if not str(s.get('fr', '')).strip()]
    if missing:
        print('  %d segment(s) non traduit(s), rien ecrit :' % len(missing))
        for mid in missing[:20]:
            print('    -', mid)
        return 1

    drift = []
    for seg in payload['segments']:
        if seg['kind'] in ('meta', 'jsonld'):
            continue
        a, b = inline_tag_signature(seg['source']), inline_tag_signature(seg['fr'])
        if a != b:
            drift.append((seg['id'], a, b))
    if drift:
        print('  %d segment(s) dont les balises en ligne ne correspondent pas, rien ecrit :'
              % len(drift))
        for sid, a, b in drift[:10]:
            print('    - %s  source=%s  fr=%s' % (sid, a, b))
        return 1

    out = assemble(src, payload, prof)
    if re.search(r'<html[^>]*\blang="%s"' % prof.html_lang, out):
        out, chrome = localize_chrome(out, prof)
        if chrome:
            print('  habillage localise : %s'
                  % ', '.join('%s x%d' % (c[0][:28], c[1]) for c in chrome))

    print('  CONTROLE D\'INTEGRITE (bloquant)')
    checks = integrity(out, src, prof)
    if not report(checks):
        print('\n  -> au moins un controle a echoue : RIEN N\'A ETE ECRIT.')
        return 1

    dest = os.path.join(ROOT, 'blog', prof.directory, payload['fr_slug'] + '.html')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w', encoding='utf-8') as fh:
        fh.write(out)
    print('\n  tous les controles passent -> ecrit : %s (%d octets)'
          % (os.path.relpath(dest, ROOT), len(out.encode('utf-8'))))
    return 0


def cmd_check(args):
    out = open(os.path.join(ROOT, args.path), encoding='utf-8').read()
    src = open(os.path.join(ROOT, args.source), encoding='utf-8').read()
    prof = profile_for(args.lang)
    print('  CONTROLE D\'INTEGRITE de %s' % args.path)
    return 0 if report(integrity(out, src, prof)) else 1


# ==========================================================================
# Pre-remplissage deterministe du payload
# ==========================================================================
#
# Une bonne moitie des segments d'un article n'a pas a etre traduite a la main :
# l'habillage est identique mot pour mot d'un article a l'autre, les dates se
# convertissent mecaniquement, et plusieurs valeurs JSON-LD reprennent
# textuellement un bloc du corps (la reponse d'une FAQ, le <h1>, le titre).
# Les retaper article par article, c'etait 8 lots durant une source d'oublis :
# chaque « segment vide » ou « jsonld non resolu » refuse par build venait de la.
#
# Ce qui reste a la charge du traducteur, c'est le corps redactionnel — et c'est
# tres bien ainsi : c'est la seule partie ou un choix editorial se joue.

# Faits WebAutonomos : recopies tels quels (cf. CLAUDE.md, cible FR).
PREFILL_PASSTHROUGH = re.compile(r'(title="Espa\u00f1ol"|Calle Pintor Josep Segrelles)')

MONTHS_ES_FR = {
    'enero': 'janvier', 'febrero': 'f\u00e9vrier', 'marzo': 'mars', 'abril': 'avril',
    'mayo': 'mai', 'junio': 'juin', 'julio': 'juillet', 'agosto': 'ao\u00fbt',
    'septiembre': 'septembre', 'octubre': 'octobre', 'noviembre': 'novembre',
    'diciembre': 'd\u00e9cembre',
}

# Blocs d'habillage, identiques dans tous les articles du gabarit SPA.
PREFILL_BLOCKS = {
    'W': 'W',
    'WebAutonomos': 'WebAutonomos',
    'Preguntas frecuentes': 'Questions fr\u00e9quentes',
    '\U0001F4D1 Contenido del art\u00edculo': "\U0001F4D1 Sommaire de l'article",
    '\u00bfQuieres una web as\u00ed para tu negocio?':
        'Vous voulez un site comme celui-ci pour votre activit\u00e9 ?',
    'P\u00e1ginas web profesionales desde 15 \u20ac/mes \u00b7 Sin permanencia':
        'Sites web professionnels \u00e0 partir de 15 \u20ac/mois \u00b7 Sans engagement',
    'Agencia web especializada en aut\u00f3nomos de la Comunidad Valenciana. '
    'P\u00e1ginas web profesionales desde 15 \u20ac/mes, sin permanencia.':
        'Agence web sp\u00e9cialis\u00e9e dans les ind\u00e9pendants de la Communaut\u00e9 '
        'valencienne. Sites web professionnels \u00e0 partir de 15 \u20ac/mois, sans engagement.',
    '\u00bfCu\u00e1nto cuesta y cu\u00e1nto tarda?':
        'Combien \u00e7a co\u00fbte et combien de temps \u00e7a prend ?',
    '15 euros al mes, sin alta y sin permanencia, o 349 euros en pago \u00fanico. '
    'Tu web est\u00e1 lista en 24 horas.':
        "15 \u20ac/mois, sans frais d'ouverture et sans engagement, ou 349 euros en "
        'paiement unique. Votre site est pr\u00eat en 24 heures.',
}

# Valeurs JSON-LD qui decrivent WebAutonomos, pas l'article.
PREFILL_JSONLD = {
    'jsonld:0:author.name': 'WebAutonomos',
    'jsonld:0:publisher.name': 'WebAutonomos',
    'jsonld:1:itemListElement.0.name': 'Accueil',
    'jsonld:1:itemListElement.1.name': 'Blog',
    'jsonld:3:name': 'WebAutonomos',
    'jsonld:3:description': 'Agence de marketing digital sp\u00e9cialis\u00e9e dans les sites '
                            'web et le SEO local pour les ind\u00e9pendants de la '
                            'Communaut\u00e9 valencienne',
    'jsonld:3:areaServed.name': 'Communaut\u00e9 valencienne',
    'jsonld:4:name': 'Blog WebAutonomos.es',
    'jsonld:4:description': 'Conseils et guides de SEO local et de marketing digital '
                            'pour les ind\u00e9pendants',
    'jsonld:4:publisher.name': 'WebAutonomos.es',
}


def _flat(txt):
    return ' '.join(txt.split())


def prefill_block(src_txt, prof):
    """Traduction du bloc d'habillage, ou None si le bloc est redactionnel."""
    flat = _flat(src_txt)
    if flat in prof.prefill_blocks:
        return prof.prefill_blocks[flat]
    # date de publication : « 30 Julio 2026 · 11 min de lectura »
    if '<time' in flat:
        out = src_txt
        for es, fr in prof.months.items():
            out = re.sub(es, fr, out, flags=re.I)
        return out.replace('min de lectura', prof.read_label)
    # logo « web | autonomos | .es », eventuellement suivi du lien Blog
    if '>autonomos</span>' in flat and '>web</span>' in flat:
        return src_txt
    # bloc sans aucune lettre : emoji, puce, symbole. Rien a traduire.
    if flat and not re.search(r'[A-Za-z\u00c0-\u024f]', re.sub(r'<[^>]+>', '', flat)):
        return src_txt
    # Retour au blog, boutons CTA et pied de page legal figurent tous dans la
    # table d'habillage du profil : on l'applique, plutot que de tenir des
    # libelles francais en dur. C'etait la derniere poche de langue hors profil.
    if ('Volver al blog' in flat or 'Pedir presupuesto gratis' in flat
            or 'Solicitar mi web gratis' in flat
            or ('aviso-legal' in flat and 'privacidad' in flat)):
        out = src_txt
        for a, b in prof.chrome:
            out = out.replace(a, b)
        return out
    # Depuis que l'extraction couvre le texte orphelin des blocs parents, la
    # barre de navigation et le bouton CTA sont des segments a part entiere. Ils
    # etaient jusqu'ici traites par localize_chrome au moment de l'assemblage :
    # on reutilise la meme table plutot que d'en tenir une seconde.
    localized, applied = localize_chrome(src_txt, prof)
    if applied:
        return localized
    return None


def _visible(txt):
    return ' '.join(H.unescape(re.sub(r'<[^>]+>', ' ', txt)).split())


def _loose(txt):
    return re.sub(r'[^0-9a-z]+', '', _visible(txt).lower())


def cmd_prefill(args):
    """Remplit ce qui se deduit sans choix editorial. Idempotente, relancable.

    A lancer deux fois : juste apres 'extract' pour l'habillage, puis une fois le
    corps traduit, pour resoudre les valeurs JSON-LD qui reprennent un bloc.
    """
    prof = profile_for(args.lang)
    path = os.path.join(TRANSLATIONS_DIR, args.fr_slug + '.json')
    if not os.path.isfile(path):
        sys.exit('fichier de traduction introuvable : ' + path)
    payload = json.load(open(path, encoding='utf-8'))
    segs = payload['segments']

    def empty(seg):
        return not str(seg.get('fr', '')).strip()

    n_chrome = 0
    for seg in segs:
        if not seg['id'].startswith('block:') or not empty(seg):
            continue
        if prof.passthrough.search(seg['source']):
            seg['fr'] = seg['source']
            n_chrome += 1
            continue
        fr = prefill_block(seg['source'], prof)
        if fr is not None:
            seg['fr'] = fr
            n_chrome += 1

    # JSON-LD : d'abord les valeurs fixes, puis celles qui reprennent un bloc
    # deja traduit — une reponse de FAQ, le <h1>, le titre de la page.
    idx, idx_loose = {}, {}
    for seg in segs:
        if seg['id'].startswith('block:') and not empty(seg):
            idx[_visible(seg['source'])] = _visible(seg['fr'])
            idx_loose[_loose(seg['source'])] = _visible(seg['fr'])
    for seg in segs:
        if seg['id'].startswith('meta:') and not empty(seg):
            idx.setdefault(_visible(seg['source']), _visible(seg['fr']))
            idx_loose.setdefault(_loose(seg['source']), _visible(seg['fr']))

    n_ld = 0
    for seg in segs:
        if not seg['id'].startswith('jsonld') or not empty(seg):
            continue
        if seg['id'] in prof.prefill_jsonld:
            seg['fr'] = prof.prefill_jsonld[seg['id']]
            n_ld += 1
            continue
        key = _visible(seg['source'])
        if key in idx:
            seg['fr'] = idx[key]
            n_ld += 1
        elif _loose(seg['source']) in idx_loose:
            seg['fr'] = idx_loose[_loose(seg['source'])]
            n_ld += 1

    if not args.dry_run:
        json.dump(payload, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    rest = [s['id'] for s in segs if empty(s)]
    verbe = 'a remplir' if args.dry_run else 'remplis'
    print('  %d bloc(s) d\'habillage %s, %d segment(s) JSON-LD %s'
          % (n_chrome, verbe, n_ld, verbe))
    print('  %d segment(s) restant(s), a traduire a la main :' % len(rest))
    for sid in rest[:12]:
        print('    -', sid)
    if len(rest) > 12:
        print('    ... et %d autre(s)' % (len(rest) - 12))
    return 0


def normalise_candidate(fragment, prof):
    """Normalise un fragment repris avant de le soumettre aux controles.

    Retirer « ¿ » et « ¡ » d'un texte valencien par ailleurs correct n'est pas une
    traduction : c'est appliquer la normative, qui ne connait pas ces signes. On
    le fait donc AVANT le controle, plutot que de refuser le bloc et de le
    retraduire a l'identique. Toute autre non-conformite fait toujours refuser.
    """
    if prof.code == 'val':
        return fragment.replace('\u00bf', '').replace('\u00a1', '')
    return fragment


def segment_is_clean(fragment, prof):
    """Un fragment candidat passe-t-il les controles linguistiques du profil ?

    Applique les DEUX gardes, pas seulement le residu. La premiere version de la
    recuperation valencienne ne verifiait que le castillan : 188 blocs repris de
    l'ancien corpus sont passes, dont 175 portaient les signes ouvrants « ¿ » et
    « ¡ », non normatifs en catalan. Il a fallu les corriger apres coup. Un bloc
    recupere doit satisfaire exactement ce qu'on exige d'un bloc traduit.
    """
    if prof.residue(fragment):
        return False
    # les gardes de registre lisent a partir de <body> : on encadre le fragment
    if prof.register('<body>' + fragment + '</body>'):
        return False
    return True


def cmd_recover(args):
    """Reprend la traduction deja presente dans un fichier de la langue cible.

    Sert quand une version existe deja mais qu'elle est structurellement abimee
    ou partiellement castillane : on aligne les blocs feuilles sur la source et
    on reprend ceux qui passent les controles. Le reste sera traduit a la main.
    """
    prof = profile_for(args.lang)
    path = os.path.join(TRANSLATIONS_DIR, args.fr_slug + '.json')
    if not os.path.isfile(path):
        sys.exit('fichier de traduction introuvable : ' + path)
    payload = json.load(open(path, encoding='utf-8'))
    src = open(os.path.join(ROOT, payload['source_file']), encoding='utf-8').read()
    old_path = os.path.join(ROOT, 'blog', prof.directory, args.source + '.html')
    if not os.path.isfile(old_path):
        sys.exit('fichier source de recuperation introuvable : ' + old_path)
    old = open(old_path, encoding='utf-8', errors='replace').read()

    be, bo = leaf_blocks(src), leaf_blocks(old)
    to = [old[a:b].strip() for a, b, _ in bo]
    sm = difflib.SequenceMatcher(None, [t for _, _, t in be], [t for _, _, t in bo],
                                 autojunk=False)
    by_id = {s['id']: s for s in payload['segments']}
    took = refused = 0
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            seg = by_id.get('block:%04d' % (a + k))
            if not seg or str(seg.get('fr', '')).strip():
                continue
            cand = normalise_candidate(to[b + k], prof)
            if not cand:
                continue
            if not segment_is_clean(cand, prof):
                refused += 1
                continue
            if inline_tag_signature(seg['source']) != inline_tag_signature(cand):
                refused += 1
                continue
            seg['fr'] = cand
            took += 1
    if not args.dry_run:
        json.dump(payload, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    rest = [s['id'] for s in payload['segments'] if not str(s.get('fr', '')).strip()]
    print('  %d bloc(s) repris, %d refuse(s) par les controles, %d segment(s) restant(s)'
          % (took, refused, len(rest)))
    return 0


def cmd_retarget_all(args):
    """Passe globale : repointe les liens ES vers leur equivalent FR partout.

    Raison d'etre : retarget_links, appele pendant un build, ne convertit un
    lien que si le fichier FR cible existe DEJA. Dans un lot ou les articles se
    citent mutuellement, les premiers batis ne peuvent pas pointer vers les
    derniers — site-web-pour-plombiers-guide-complet a ete ecrit avant
    site-web-pour-electriciens et citait donc encore la version espagnole.
    Cette commande se lance apres le lot, quand tous les fichiers sont la.

    Les exceptions sont celles de retarget_links, qui reposent toutes sur la
    meme regle : un lien vers la version ES/VAL/EN DU MEME article est voulu,
    pas subi. Cela couvre les balises hreflang, le selecteur de langue et une
    carte « articles similaires » qui pointerait vers l'article lui-meme.

    Idempotente : une fois passee, un second appel ne trouve plus rien.
    """
    prof = profile_for(args.lang)
    mapping = es_to_fr_slugs(prof)
    paths = sorted(glob.glob(os.path.join(ROOT, 'blog', prof.directory, '*.html')))
    if not paths:
        print('  aucun fichier dans blog/%s/' % prof.directory)
        return 0

    link_re = re.compile(
        r'href="(?:https://webautonomos\.es)?/blog/(?:es/)?'
        r'([a-z0-9-]+)(?:\.html)?(?=")')

    total, touched = 0, 0
    for path in paths:
        fr_slug = os.path.basename(path)[:-5]
        before = open(path, encoding='utf-8').read()
        hits = [es for es in link_re.findall(before)
                if mapping.get(es) and mapping[es] != fr_slug]
        if not hits:
            continue
        after = retarget_links(before, fr_slug, prof, mapping)
        total += len(hits)
        touched += 1
        counts = {}
        for es in hits:
            counts[es] = counts.get(es, 0) + 1
        for es in sorted(counts):
            print('  %-46s %s -> %s%s' % (fr_slug, es, mapping[es],
                                          ' x%d' % counts[es] if counts[es] > 1 else ''))
        if not args.dry_run:
            open(path, 'w', encoding='utf-8').write(after)

    verbe = 'a repointer' if args.dry_run else 'repointes'
    print('  %d fichier(s) balaye(s), %d lien(s) %s dans %d fichier(s)'
          % (len(paths), total, verbe, touched))
    return 0


PROFILES = {
    'fr': LangProfile(
        code='fr', html_lang='fr', directory='fr', og_locale='fr_FR',
        hreflang='fr',
        chrome=CHROME_FR, chrome_re=CHROME_FR_RE,
        prefill_blocks=PREFILL_BLOCKS, prefill_jsonld=PREFILL_JSONLD,
        months=MONTHS_ES_FR, passthrough=PREFILL_PASSTHROUGH,
        residue=spanish_residue_hits,
        register=tutoiement_hits,
        register_label='aucune 2e personne du singulier (vouvoiement)',
        read_label='min de lecture'),
    'val': LangProfile(
        code='val', html_lang='ca', directory='val', og_locale='ca_ES',
        hreflang='ca-ES',
        chrome=CHROME_VAL, chrome_re=CHROME_VAL_RE,
        prefill_blocks=PREFILL_BLOCKS_VAL, prefill_jsonld=PREFILL_JSONLD_VAL,
        months=MONTHS_ES_VAL, passthrough=PREFILL_PASSTHROUGH,
        residue=valencian_residue_hits,
        register=avl_hits,
        register_label='normative AVL (signes ouvrants, l geminee)',
        read_label='min de lectura'),   # identique en catalan
}


def profile_for(code):
    if code not in PROFILES:
        sys.exit('langue inconnue : %s (connues : %s)' % (code, ', '.join(sorted(PROFILES))))
    return PROFILES[code]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    def add_lang(parser):
        parser.add_argument('--lang', default='fr', choices=sorted(PROFILES),
                            help="langue cible (defaut : fr)")
        return parser

    e = sub.add_parser('extract', help='extrait les segments a traduire')
    e.add_argument('es_slug')
    e.add_argument('--fr-slug', required=True)
    add_lang(e)
    e.set_defaults(func=cmd_extract)

    b = sub.add_parser('build', help='reassemble, verifie, puis ecrit si tout passe')
    b.add_argument('es_slug', nargs='?')
    b.add_argument('--fr-slug', required=True)
    add_lang(b)
    b.set_defaults(func=cmd_build)

    c = sub.add_parser('check', help='verifie un fichier deja produit')
    c.add_argument('path')
    c.add_argument('--source', required=True)
    add_lang(c)
    c.set_defaults(func=cmd_check)

    p = sub.add_parser('prefill',
                       help="remplit l'habillage, les dates et le JSON-LD deductible ; "
                            "a lancer apres extract, puis apres la traduction du corps")
    p.add_argument('--fr-slug', required=True)
    p.add_argument('--dry-run', action='store_true',
                   help='affiche ce qui serait rempli sans ecrire')
    add_lang(p)
    p.set_defaults(func=cmd_prefill)

    v = sub.add_parser('recover',
                       help="reprend la traduction d'un fichier existant de la langue "
                            "cible ; un bloc n'est repris que s'il passe les controles")
    v.add_argument('--fr-slug', required=True)
    v.add_argument('--source', required=True, help='slug du fichier existant a reprendre')
    v.add_argument('--dry-run', action='store_true')
    add_lang(v)
    v.set_defaults(func=cmd_recover)

    r = sub.add_parser('retarget-all',
                       help='repointe les liens ES vers le FR dans tout blog/fr/ '
                            '(a lancer apres chaque lot)')
    r.add_argument('--dry-run', action='store_true',
                   help="liste ce qui serait modifie sans rien ecrire")
    add_lang(r)
    r.set_defaults(func=cmd_retarget_all)

    args = ap.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
