# -*- coding: utf-8 -*-
"""Pages françaises « Comment ça marche » et « Contact » (plan SEO FR-EN, 29/09/2026).

Crée :
    /fr/comment-ca-marche   équivalent de /como-funciona et /en/how
    /fr/contact             équivalent de /contacto et /en/contact
sur le gabarit de fr/questions.html (styles, fenêtres « Mentions légales » et
« Confidentialité », pied de page). Faits limités à _tools/seo_pipeline/VERITE.md.

Et relie ces pages au reste du site :
  - hreflang « fr » sur /como-funciona, /contacto, /en/how et /en/contact ;
  - lien « Contact » du pied de page des pages FR faites à la main -> /fr/contact ;
  - llms.txt (section Français).
Les pages générées (accueil /fr/, pages métier FR, page francophones) prennent
les liens par build_lang_homes.py (URLS['fr'] : how, contact ; menu FR).

Idempotent. Usage, depuis la racine du dépôt :
    python3 _tools/patch_fr_pages_20260929.py            écrit
    python3 _tools/patch_fr_pages_20260929.py --check    vérifie sans écrire
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHECK = '--check' in sys.argv
BASE = 'https://webautonomos.es'
E = lambda t: html.escape(t, quote=False)
A = lambda t: html.escape(t, quote=True)


def abandon(msg):
    sys.exit('ABANDON : %s. Rien écrit.' % msg)


def lire(rel):
    return open(rel, encoding='utf-8').read()


TAXE = ("Prix hors taxes. L'IVA espagnole de 21 % s'ajoute. Si votre entreprise est établie dans un autre pays "
        "de l'UE, en France par exemple, avec un numéro de TVA intracommunautaire, la facture est émise sans TVA "
        "et vous déclarez la TVA vous-même (autoliquidation).")

CSS_EXTRA = """<style>
.tax-note{font-size:.85rem;color:#6b7280;margin:-8px 0 22px;line-height:1.5;max-width:70ch}
.no-plantilla{background:#eff6ff;border-left:4px solid #2563eb;padding:12px 16px;border-radius:8px;margin:14px 0 22px;line-height:1.55}
.aside{background:#f4fbf7;border:1px solid #d1e8d9;border-radius:10px;padding:14px 16px;margin:0 0 24px;font-size:.97rem;line-height:1.65}
ul.plain li a{color:var(--blue)}
.updated{font-size:.85rem;color:var(--gray);margin:34px 0 0;padding-top:16px;border-top:1px solid var(--border)}
</style>"""

# ─── contenu ────────────────────────────────────────────────────────────────
HOW = dict(
    slug='comment-ca-marche',
    es='/como-funciona', en='/en/how',
    title="Comment ça marche : votre site prêt en 24 h | WebAutonomos",
    description=("Nous créons une démonstration de votre site en moins de 24 heures, avec vos informations "
                 "réelles, et vous ne payez que si elle vous plaît. En français, sans engagement."),
    crumb='Comment ça marche',
    faq=[
        ("Dois-je préparer des textes ou des photos ?",
         "Non. Nous rédigeons les textes à partir de ce que vous nous dites et de votre fiche d'établissement "
         "Google, et nous utilisons vos photos : celles de votre fiche ou celles que vous nous envoyez."),
        ("Et si la démonstration ne me plaît pas ?",
         "Vous ne payez rien et vous n'êtes engagé à rien. Avant la mise en ligne, les retouches sont illimitées : "
         "textes, photos, couleurs, sections."),
        ("Comment se passent les modifications après la mise en ligne ?",
         "Une modification par mois est comprise, dans les deux formules et sans limite de durée : un texte, une "
         "photo, des horaires, une prestation, un tarif. Envoyez-la par WhatsApp ou par email. Un changement plus "
         "important, comme une refonte ou une nouvelle grande section, se fait sur devis fermé."),
        ("Faut-il des connaissances techniques ?",
         "Aucune. Hébergement, nom de domaine, certificat SSL, textes légaux, mises à jour et sauvegardes : nous "
         "nous en occupons."),
        ("Travaillez-vous avec des entreprises installées en France ?",
         "Oui. Nous travaillons à distance, par email, WhatsApp et visioconférence, et en français. Le site d'une "
         "entreprise installée en France utilise un nom de domaine en .fr, compris la première année."),
    ],
)

HOW_MAIN = """  <p class="crumb"><a href="/fr/">Accueil</a> &rsaquo; Comment ça marche</p>
  <h1>Comment ça marche : votre site internet prêt en 24 heures</h1>
  <p class="lede">Nous construisons d'abord une démonstration de votre site, avec vos propres informations, et vous ne payez que si elle vous convient. Aucun modèle à remplir, rien à configurer, et tout se passe en français.</p>
  <p class="no-plantilla"><strong>C'est notre méthode « Déjà-Fait ».</strong> Beaucoup d'offres vous demandent de vous engager avant d'avoir vu quoi que ce soit. Nous faisons l'inverse : vous voyez votre site terminé, puis vous décidez.</p>

  <h2>1. Vous nous présentez votre activité</h2>
  <p>Quelques minutes suffisent : votre métier, vos principales prestations, la ville où vous travaillez et la façon de vous joindre (WhatsApp ou email). Remplissez le <a href="/demandez-votre-demo#pide-demo">formulaire de démonstration</a> ou envoyez-nous simplement un message WhatsApp.</p>

  <h2>2. Nous préparons votre démonstration en moins de 24 heures</h2>
  <p>Nous rédigeons les textes à partir de ce que vous nous avez dit et de votre fiche d'établissement Google : vos prestations, vos horaires, vos photos. Nous ajoutons le bouton WhatsApp, le formulaire de contact, qui envoie les demandes sur votre email, les liens vers vos réseaux sociaux et les pages de mentions légales, de confidentialité et de cookies.</p>

  <h2>3. Nous la revoyons ensemble</h2>
  <p>Nous vous envoyons un lien privé : vous la regardez quand vous voulez, et nous pouvons la parcourir ensemble par WhatsApp ou en visioconférence. Vous nous dites ce qu'il faut changer — textes, photos, couleurs, sections — et nous vous renvoyons la version corrigée. Avant la mise en ligne, les retouches sont illimitées.</p>

  <h2>4. Vous validez, et le site est mis en ligne</h2>
  <p>Quand le résultat vous convient, nous connectons votre nom de domaine, déposé à votre nom, et le site est mis en ligne. Pour une entreprise installée en France, c'est un .fr, compris la première année puis environ 12 € par an. Vous payez alors 15 € par mois, sans engagement, ou 349 € une seule fois. <a href="/fr/tarifs">Comparer les deux formules</a>.</p>
  <p class="tax-note">{taxe}</p>

  <h2>Après la mise en ligne</h2>
  <ul class="plain">
    <li>Une modification par mois, sans limite de durée</li>
    <li>Hébergement et certificat SSL (https)</li>
    <li>Sauvegardes quotidiennes et surveillance 24/7</li>
    <li>Maintenance technique</li>
    <li>Assistance par email et WhatsApp, réponse dans la journée</li>
    <li>En location, vous arrêtez quand vous voulez, sans pénalité, et votre nom de domaine reste à vous</li>
  </ul>

  <h2>Un site en plusieurs langues</h2>
  <p>Votre site peut exister en plusieurs langues sans supplément, jusqu'à 4 : français, anglais, espagnol ou une langue co-officielle d'Espagne (catalan, valencien, galicien, basque). Nous rédigeons nous-mêmes chaque version, et la modification mensuelle comprise vaut pour toutes les langues.</p>

  <h2>Ce que vous n'avez pas à faire</h2>
  <p class="aside">Choisir un modèle, apprendre un éditeur, comparer des hébergeurs, installer des extensions, rédiger vos mentions légales ou votre politique de cookies, penser à renouveler un certificat SSL. C'est notre travail ; vous relisez et validez chaque contenu.</p>

  <h2>Questions fréquentes</h2>
  <dl class="qa">
{faq}
  </dl>
  <div class="actions">
    <a class="btn btn-primary" href="/demandez-votre-demo#pide-demo">Demander ma démonstration gratuite</a>
    <a class="btn btn-ghost" href="/fr/prestations">Voir ce qui est inclus</a>
  </div>
  <p class="updated">Mis à jour : septembre 2026</p>"""

CONTACT = dict(
    slug='contact',
    es='/contacto', en='/en/contact',
    title="Contact | Votre site internet professionnel | WebAutonomos",
    description=("Écrivez-nous par WhatsApp ou par email, ou appelez-nous : nous répondons dans la journée, en "
                 "français, et préparons une démonstration gratuite de votre site."),
    crumb='Contact',
    faq=[],
)

CONTACT_MAIN = """  <p class="crumb"><a href="/fr/">Accueil</a> &rsaquo; Contact</p>
  <h1>Contacter WebAutonomos</h1>
  <p class="lede">Vous voulez un site internet professionnel ? Écrivez-nous par WhatsApp ou par email, ou appelez-nous. Nous répondons dans la journée, en français, et sans engagement.</p>

  <h2>Nous joindre</h2>
  <ul class="plain">
    <li>Téléphone : <a href="tel:+34961877356">+34 961 877 356</a></li>
    <li>WhatsApp : <a href="https://wa.me/34654239520" rel="noopener">+34 654 23 95 20</a></li>
    <li>Email : <a href="mailto:info@webautonomos.es">info@webautonomos.es</a></li>
    <li>Calle Pintor Josep Segrelles, 26 — 46870 Ontinyent (Valencia), Espagne</li>
  </ul>
  <p>Nous travaillons à distance avec des indépendants et des petites entreprises installés en France et en Espagne, par email, WhatsApp ou visioconférence. Dites-nous ce que vous faites : nous préparons une démonstration gratuite de votre site en moins de 24 heures, et vous ne payez que si elle vous plaît.</p>

  <h2>Ce qu'il est utile de nous dire</h2>
  <ul class="plain">
    <li>Votre métier et vos principales prestations</li>
    <li>La ville ou la zone où vous travaillez</li>
    <li>Le lien de votre fiche d'établissement Google, si vous en avez une</li>
    <li>La ou les langues souhaitées pour le site</li>
  </ul>
  <p>Vous préférez voir d'abord comment se déroule la création ? <a href="/fr/comment-ca-marche">Comment ça marche, étape par étape</a>. Les prix sont sur la page <a href="/fr/tarifs">Tarifs</a>.</p>

  <h2>Qui sommes-nous</h2>
  <p>WebAutonomos est une marque de PASURITE SLU (NIF ESB42890012), dont l'équipe est basée dans la province de Valencia, en Espagne.</p>

  <div class="actions">
    <a class="btn btn-primary" href="/demandez-votre-demo#pide-demo">Demander ma démonstration gratuite</a>
    <a class="btn btn-ghost" href="/fr/">Retour à l'accueil</a>
  </div>
  <p class="updated">Mis à jour : septembre 2026</p>"""


def jsonld(P):
    url = '%s/fr/%s' % (BASE, P['slug'])
    blocs = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/fr/"},
        {"@type": "ListItem", "position": 2, "name": P['crumb'], "item": url}]}]
    if P['faq']:
        blocs.insert(0, {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "fr",
                         "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in P['faq']]})
    if P['slug'] == 'contact':
        blocs.insert(0, {"@context": "https://schema.org", "@type": "ContactPage", "inLanguage": "fr",
                         "url": url, "name": P['title'],
                         "mainEntity": {"@type": "Organization", "name": "WebAutonomos",
                                        "legalName": "PASURITE SLU", "url": BASE + "/fr/",
                                        "email": "info@webautonomos.es", "telephone": "+34961877356",
                                        "address": {"@type": "PostalAddress",
                                                    "streetAddress": "Calle Pintor Josep Segrelles 26",
                                                    "postalCode": "46870", "addressLocality": "Ontinyent",
                                                    "addressRegion": "Valencia", "addressCountry": "ES"}}})
    return ''.join('<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(b, ensure_ascii=False, indent=2)
                   for b in blocs)


def page(P, main):
    tpl = lire('fr/questions.html')
    head_end = tpl.index('</style>') + len('</style>')
    head = tpl[:head_end]
    url = '%s/fr/%s' % (BASE, P['slug'])
    rempl = [
        (r'<title>[^<]*</title>', '<title>%s</title>' % E(P['title'])),
        (r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % A(P['description'])),
        (r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url),
        (r'<link rel="alternate" hreflang="es-ES" href="[^"]*">\n<link rel="alternate" hreflang="en" href="[^"]*">\n'
         r'<link rel="alternate" hreflang="fr" href="[^"]*">\n<link rel="alternate" hreflang="x-default" href="[^"]*">',
         '<link rel="alternate" hreflang="es-ES" href="%s%s">\n<link rel="alternate" hreflang="en" href="%s%s">\n'
         '<link rel="alternate" hreflang="fr" href="%s">\n<link rel="alternate" hreflang="x-default" href="%s%s">'
         % (BASE, P['es'], BASE, P['en'], url, BASE, P['es'])),
        (r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url),
        (r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % A(P['title'])),
        (r'<meta property="og:description" content="[^"]*">',
         '<meta property="og:description" content="%s">\n<meta property="og:image" content="%s/og-image.png">'
         % (A(P['description']), BASE)),
    ]
    for motif, nouveau in rempl:
        head, n = re.subn(motif, lambda m: nouveau, head, count=1)
        if n != 1:
            abandon('gabarit fr/questions.html : %s introuvable' % motif[:50])
    body_tpl = tpl[tpl.index('<footer>'):]
    footer_modals = body_tpl.replace('<a href="/demandez-votre-demo#pide-demo">Contact</a>',
                                     '<a href="/fr/contact">Contact</a>')
    faq = '\n'.join('    <dt>%s</dt>\n    <dd>%s</dd>' % (E(q), E(r)) for q, r in P['faq'])
    main = main.replace('{faq}', faq).replace('{taxe}', E(TAXE))
    return (head + '\n' + jsonld(P) + CSS_EXTRA + '\n</head>\n<body>\n\n<main>\n' + main + '\n</main>\n\n'
            + footer_modals)


def ajoute_hreflang(rel, fr_url):
    s = lire(rel)
    ligne = '<link rel="alternate" hreflang="fr" href="%s%s">' % (BASE, fr_url)
    if ligne in s:
        return s
    ancre = re.search(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', s)
    if not ancre or s.count('hreflang="x-default"') != 1:
        abandon('%s : hreflang x-default introuvable ou multiple' % rel)
    return s[:ancre.start()] + ligne + '\n' + s[ancre.start():]


def main():
    ecrits = {}
    ecrits['fr/comment-ca-marche.html'] = page(HOW, HOW_MAIN)
    ecrits['fr/contact.html'] = page(CONTACT, CONTACT_MAIN)

    for rel, fr in (('como-funciona.html', '/fr/comment-ca-marche'), ('en/how.html', '/fr/comment-ca-marche'),
                    ('contacto.html', '/fr/contact'), ('en/contact.html', '/fr/contact')):
        ecrits[rel] = ajoute_hreflang(rel, fr)

    # pied de page des pages FR faites à la main
    for rel in ('fr/tarifs.html', 'fr/prestations.html', 'fr/questions.html',
                'fr/meilleurs-createurs-de-sites-pour-independants.html'):
        s = lire(rel)
        a, b = '<a href="/demandez-votre-demo#pide-demo">Contact</a>', '<a href="/fr/contact">Contact</a>'
        if s.count(a) + s.count(b) != 1:
            abandon('%s : lien Contact du pied de page trouvé %dx' % (rel, s.count(a) + s.count(b)))
        ecrits[rel] = s.replace(a, b)

    # llms.txt
    llms = lire('llms.txt')
    ancre = '- [Questions fréquentes](https://webautonomos.es/fr/questions)\n'
    ajout = ('- [Comment ça marche](https://webautonomos.es/fr/comment-ca-marche)\n'
             '- [Contact](https://webautonomos.es/fr/contact)\n')
    if ajout not in llms:
        if llms.count(ancre) != 1:
            abandon('llms.txt : ancre FR introuvable')
        llms = llms.replace(ancre, ancre + ajout)
    ecrits['llms.txt'] = llms

    # contrôles : vouvoiement, JSON-LD, balises
    for rel in ('fr/comment-ca-marche.html', 'fr/contact.html'):
        s = ecrits[rel]
        texte = re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)\b.*?</\1>', ' ', s, flags=re.S))
        tu = re.findall(r"\b(tu|ton|ta|tes|toi|te)\b", texte.split('Mentions légales')[0], flags=re.I)
        if tu:
            abandon('%s : tutoiement : %s' % (rel, tu[:5]))
        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            json.loads(m)
        for tag in ('main', 'dl', 'ul', 'p', 'a', 'div', 'footer'):
            o, f = len(re.findall(r'<%s\b' % tag, s)), s.count('</%s>' % tag)
            if o != f:
                abandon('%s : <%s> %d ouvertures, %d fermetures' % (rel, tag, o, f))

    for rel, s in ecrits.items():
        ancien = lire(rel) if os.path.exists(rel) else None
        if ancien == s:
            print('  = %s déjà à jour' % rel)
            continue
        if CHECK:
            print('  ✓ %s à écrire — non écrit' % rel)
            continue
        open(rel, 'w', encoding='utf-8').write(s)
        print('  ✓ %s écrit' % rel)


if __name__ == '__main__':
    main()
