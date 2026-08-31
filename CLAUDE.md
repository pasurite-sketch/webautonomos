# CLAUDE.md — Règles Projet WebAutonomos.es

## Identité du Projet

- **Site** : https://webautonomos.es
- **Activité** : Agence web spécialisée sites vitrines pour autónomos (artisans + professions libérales)
- **Zone** : Comunidad Valenciana, Espagne
- **Offre principale** : Site vitrine à 15€/mois (modèle location)
- **Services complémentaires** : Google My Business (99€ setup + 29€/mois), SEO Local (+15€/mois)
- **Repo** : github.com/pasurite-sketch/webautonomos
- **Hébergement** : Cloudflare Workers (assets statiques), déployé via GitHub Actions sur push `main`

## Stack Technique

- **Architecture** : React SPA (Single Page Application) — un seul `index.html` (~536KB)
- **Hébergement** : Cloudflare Pages via `wrangler.jsonc` (assets statiques)
- **DNS + Email** : Cloudflare (email routing vers info@webautonomos.es)
- **Domaine** : webautonomos.es (registrar DonDominio)
- **Déploiement** : `git push origin main` → GitHub Action `deploy.yml` → `wrangler deploy`
  - ⚠️ Il n'y a **pas** d'intégration Cloudflare↔GitHub native : c'est le workflow qui déploie.
  - Les pushes du bot blog (GITHUB_TOKEN) ne déclenchent pas `deploy.yml` — `publish-blog.yml` déploie déjà lui-même.
  - Redéploiement manuel : `npx wrangler deploy` en local, ou l'onglet Actions → « Déployer sur Cloudflare Workers » → Run workflow.
- **Langues** : ES (Español), VAL (Valenciano/Català), EN (English)
- **URLs** : SEO-friendly avec slugs (pas d'IDs numériques)

## Structure du Repo

```
webautonomos/
├── index.html              # React SPA (tout le site)
├── robots.txt              # Directives crawlers
├── sitemap.xml             # Plan du site pour Google
├── wrangler.jsonc          # Config Cloudflare Workers
├── .assetsignore           # Fichiers exclus du déploiement Cloudflare
├── CLAUDE.md               # Ce fichier (règles projet)
├── calendrier.json         # Calendrier éditorial blog (référence rédactionnelle)
├── blog-spa-data.json      # Données SPA pré-générées (3 langues) — legacy
├── template-article.html   # Template HTML de référence pour les articles
├── _tools/                 # Outillage blog (non déployé, cf. .assetsignore)
│   ├── publish_next.py     # Publie le prochain article dû (appelé par le GitHub Action)
│   ├── add_article.py      # Insertion SPA + sitemap (utilisé par publish_next.py)
│   └── queue/              # File d'attente : 1 JSON par article à paraître
│       └── published/      # Articles déjà publiés (déplacés ici après publication)
├── scripts/
│   └── publish-articles.js # ⚠️ Legacy, plus appelé par aucun workflow
├── .github/
│   └── workflows/
│       ├── publish-blog.yml # Publication blog (cron lun/jeu 06:00 UTC) + deploy
│       └── deploy.yml       # Déploiement Cloudflare sur push `main`
└── blog/                   # Articles de blog (fichiers HTML individuels)
    └── es/                 # Articles en espagnol (22 articles)
    └── val/                # Articles en valencien
    └── en/                 # Articles en anglais
```

## Articles Existants (SPA React)

⚠️ **6 articles existent déjà dans le SPA React (index.html).** NE PAS les régénérer en HTML autonome.

| ID Cal | URL existante (SPA) | Titre | Silo | Status |
|--------|---------------------|-------|------|--------|
| 1 | /blog/5-razones-pagina-web-negocio-2026 | 5 razones por las que tu negocio necesita una página web en 2026 | paginas-web | ✅ existant |
| 2 | /blog/como-aparecer-google-maps-autonomos | Cómo aparecer en Google Maps: guía completa para autónomos | google-my-business | ✅ existant |
| 3 | /blog/seo-local-que-es-autonomos | SEO local: qué es y por qué es clave para electricistas y fontaneros | seo-local | ✅ existant |
| 5 | /blog/cuanto-cuesta-pagina-web-autonomos-espana | ¿Cuánto cuesta una página web para autónomos en España? | paginas-web | ✅ existant |
| 6 | /blog/como-conseguir-resenas-google-negocio | Cómo conseguir más reseñas en Google (sin parecer desesperado) | google-my-business | ✅ existant |
| 8 | /blog/configurar-whatsapp-business-gratis-autonomos | WhatsApp Business: la herramienta gratuita que todo autónomo debería usar | marketing-digital | ✅ existant |

**Articles HTML générés** : 22 (IDs 4, 7, 9-28) — tous dans `blog/es/` et dans `sitemap.xml`
**Ajout au SPA** : automatisé via GitHub Action (`_tools/publish_next.py`) selon le `publish_date` des JSON de `_tools/queue/`

## Blog — Objectif & Stratégie

### But du Blog
Attirer du trafic organique vers webautonomos.es via du contenu SEO ciblant les autónomos espagnols qui cherchent à améliorer leur présence digitale. Chaque article doit démontrer l'expertise de WebAutonomos et inciter le lecteur à demander un devis. L'objectif est d'atteindre la 1ère position Google pour chaque mot-clé ciblé.

### Stratégie "1ère place"
Pour chaque article, le contenu doit être **objectivement meilleur** que le résultat #1 actuel :
- **3x plus long** que la concurrence (2000-2500 mots vs ~800 mots moyens)
- **Sommaire visible** (les concurrents n'en ont pas)
- **FAQ structurée** avec Schema FAQPage (Rich Snippets)
- **4 Schemas JSON-LD** (BlogPosting, FAQPage, BreadcrumbList, Organization)
- **Exemples locaux** Valencia/Alicante/Elda/Elche (les concurrents sont généralistes)
- **Données récentes** 2025-2026 (les concurrents ont du contenu daté)

### 4 Silos Thématiques (Catégories)

| Silo | Slug catégorie | Color | Mot-clé racine |
|------|---------------|-------|----------------|
| **Presencia Digital** | `paginas-web` | #3B82F6 | páginas web para autónomos |
| **SEO Local** | `seo-local` | #10B981 | SEO local para autónomos |
| **Google My Business** | `google-my-business` | #F59E0B | optimizar Google My Business |
| **Marketing Digital** | `marketing-digital` | #8B5CF6 | marketing digital autónomos |

### Calendrier de Publication
- **Rythme** : 2 articles/semaine (lundi + jeudi)
- **Durée** : 14 semaines (S1 à S14)
- **Total** : 28 articles en espagnol (versions VAL + EN en différé)
- **Source** : `calendrier.json`

## Règles de Génération d'Articles

### Format de Sortie
Chaque article est un fichier HTML autonome :
- **Chemin** : `blog/{lang}/{slug}.html`
- **Exemple** : `blog/es/como-conseguir-clientes-por-internet.html`
- **Template de référence** : `template-article.html` (à la racine du repo)

### Structure HTML Obligatoire

⚠️ **Toujours se baser sur `template-article.html` pour la structure exacte.**

Chaque article DOIT contenir dans cet ordre :

#### 1. HEAD — SEO complet
- `<title>` : mot-clé + année + "| WebAutonomos" (max 60 car.)
- `<meta description>` : 150-155 car. avec CTA
- `<link canonical>` vers URL définitive
- `<meta robots>` : "index, follow, max-snippet:-1, max-image-preview:large"
- Hreflang : `es`, `ca-ES` (valencien), `en`, `x-default`
- Open Graph complet (og:type, og:url, og:title, og:description, og:locale, article:*)
- Twitter Card (summary_large_image)
- **4 Schemas JSON-LD** :
  - `BlogPosting` (headline, author, publisher, datePublished, wordCount)
  - `BreadcrumbList` (Inicio > Blog > Catégorie > Titre)
  - `FAQPage` (5 questions/réponses)
  - `Organization` (WebAutonomos, areaServed: Comunidad Valenciana)
- Preconnect Tailwind CDN
- CSS custom (smooth scroll, gradient-wa, tip-box, warning-box, toc-link, FAQ accordion)

#### 2. NAVIGATION
- Barre sticky blanche avec logo "W" gradient + lien retour blog

#### 3. BREADCRUMB
- Inicio > Blog > {Catégorie} — texte gris, liens cliquables

#### 4. EN-TÊTE ARTICLE
- Badge catégorie (couleur du silo, texte blanc, rounded-full)
- Date formatée + temps de lecture estimé
- **H1** : mot-clé principal (text-3xl md:text-4xl font-bold)
- Paragraphe d'introduction (text-lg, mot-clé dans les 100 premiers mots)

#### 5. SOMMAIRE — ⚠️ TOUJOURS VISIBLE (pas de `<details>`)
- Encadré `bg-white rounded-2xl shadow-sm` avec bordure gauche couleur du silo
- Titre : "📑 Contenido del artículo"
- Liste numérotée `<ol>` de tous les H2 (liens ancres #seccion-N)
- **La FAQ est le dernier item** : "Preguntas frecuentes"
- Hover : fond violet léger (#F5F3FF)

#### 6. CORPS — 2000-2500 mots
- **H2** pour sections principales (mot-clé dans ≥2 H2, id="seccion-N")
- **H3** pour sous-sections
- Paragraphes courts (3-4 lignes, line-height: 1.8)
- Encadrés "💡 Consejo" (.tip-box, bordure #7C3AED, fond #F5F3FF)
- Encadrés "⚠️ Importante" (.warning-box, bordure #F59E0B, fond #FFFBEB)
- **Exemples locaux** obligatoires : mentionner Valencia, Alicante, Elda, Elche
- **Données chiffrées** récentes (2025-2026)
- **Liens internes** : 2 même silo + 1 autre silo minimum (texte d'ancre descriptif)

#### 7. FAQ — 5 questions (format accordéon `<details>/<summary>`)
- Questions tirées des "People Also Ask" de Google
- Réponses concises (2-3 phrases)
- **Schema FAQPage** intégré dans le HEAD (même contenu)

#### 8. CTA
- Encadré gradient (.gradient-wa, rounded-2xl)
- Titre accrocheur **lié au sujet de l'article**
- Bouton blanc "Pedir presupuesto gratis →" vers /contacto
- Mention : "Páginas web profesionales desde 15€/mes · Sin permanencia"

#### 9. ARTICLES CONNEXES
- 3 articles avec titre + description courte
- Liens vers articles existants (SPA: /blog/{slug}) OU nouveaux (blog/es/{slug})
- Priorité au même silo (2) + 1 d'un autre silo

#### 10. AUTEUR
- Avatar gradient "W" (w-16 h-16, gradient-wa)
- "WebAutonomos" + description

#### 11. FOOTER
- Lien "← Volver al blog" + lien webautonomos.es

### Liens Internes — Mapping des URLs

⚠️ Important : les 6 articles existants utilisent des URLs SPA, les nouveaux utilisent des URLs HTML autonomes.

**Articles existants (SPA)** — utiliser ces URLs pour les liens internes :
- `/blog/5-razones-pagina-web-negocio-2026`
- `/blog/como-aparecer-google-maps-autonomos`
- `/blog/seo-local-que-es-autonomos`
- `/blog/cuanto-cuesta-pagina-web-autonomos-espana`
- `/blog/como-conseguir-resenas-google-negocio`
- `/blog/configurar-whatsapp-business-gratis-autonomos`

**Nouveaux articles (HTML autonome)** — utiliser ces URLs :
- `/blog/es/{slug}` (sans .html dans le lien, Cloudflare sert le fichier)

### Règles de Contenu SEO

1. **Titre H1** : Inclure le mot-clé principal, max 60 caractères
2. **Meta description** : Inclure le mot-clé, max 155 caractères, avec appel à l'action
3. **Structure** : H1 → H2 (sections) → H3 (sous-sections). Jamais sauter de niveau
4. **Longueur** : 2000-2500 mots par article (objectif : 3x le concurrent #1)
5. **Mot-clé principal** : Dans H1, premier paragraphe, au moins 2 H2, meta description, URL slug
6. **Mots-clés secondaires** : 3-5 variations naturelles dans le corps
7. **Liens internes** : Minimum 2 liens même silo + 1 lien autre silo
8. **CTA** : Chaque article finit par un appel à l'action vers webautonomos.es
9. **Ton** : Expert mais accessible. Tutoiement ("tú"). Concret avec exemples locaux
10. **Localisation** : Mentionner villes de la Comunidad Valenciana quand pertinent
11. **E-E-A-T** : Expérience, Expertise, Autorité, Confiance. Données, cas pratiques
12. **Pas de spam IA** : Contenu utile, spécifique, pas de remplissage générique
13. **Sommaire** : TOUJOURS visible, jamais dans un `<details>` accordéon
14. **FAQ** : 5 questions basées sur "People Also Ask", format `<details>/<summary>`
15. **Schema** : 4 blocs JSON-LD obligatoires (BlogPosting, FAQPage, BreadcrumbList, Organization)

### Règles de Nommage

- **Slugs** : en minuscules, mots séparés par des tirets, sans accents
  - ✅ `seo-local-para-autonomos`
  - ❌ `SEO_Local_Para_Autónomos`
- **Fichiers** : `blog/{lang}/{slug}.html`
- **Images** : `blog/img/{slug}-{n}.webp` (si nécessaire)

### Maillage Interne (Toile d'araignée)

- Chaque article du silo lie vers au moins 2 autres articles du même silo
- Chaque article lie vers au moins 1 article d'un silo différent
- Utiliser des ancres de texte descriptives (pas "cliquez ici")
- Le premier article de chaque silo est le "pilier" (article le plus long et complet)
- Les articles SPA existants comptent comme cibles de liens valides

### Traductions (VAL + EN + FR)

- Les traductions ne sont PAS littérales — elles sont adaptées culturellement
- VAL : Valencien/Catalan, respecter la normative linguistique AVL
- EN : anglais britannique, lecteur installé en Espagne (voir plus bas)
- FR : français de France/Belgique/Suisse, exemples transposés en villes francophones
- Hreflang : `es`, `ca-ES` (pour valencien/catalan), `en`, `fr`
- Les slugs peuvent varier légèrement entre langues si nécessaire

#### Cible EN : qui lit ces articles

**Le marché espagnol, lu en anglais.** Ce sont les expatriés britanniques et
irlandais installés en Espagne — Costa Blanca, Comunidad Valenciana — et les
anglophones qui y travaillent. Ils cherchent un plombier à Alicante, pas à
Manchester.

C'est l'exact opposé du français. Le lecteur FR vit en pays francophone et les
exemples se transposent chez lui ; le lecteur EN vit en Espagne et les exemples
restent là où ils sont.

| Élément | FR | EN |
|---------|----|----|
| Villes des exemples — Valencia, Alicante, Elda, Elche | **Transposées** (Lyon, Nantes, Bruxelles) | **Conservées telles quelles** |
| Prénoms et entreprises fictives | Transposés | Conservés (Antonio, María, Fontanería López) |
| Quartiers, journaux locaux (Las Provincias, Levante-EMV) | Transposés | Conservés |
| Références réglementaires espagnoles (RETA, Kit Digital, IVA) | Équivalent local, sinon reformuler | **Conservées et expliquées** |
| Institutions (ATA, INE, Banco de España) | Reformuler | **Nom espagnol conservé** |

#### Adaptation culturelle (EN)

- **Villes : ne rien transposer.** Un article anglais sur les plombiers parle de
  Valencia et d'Elche, parce que c'est là que vit le lecteur.
- **Requêtes de recherche : traduites.** `"fontanero urgente Valencia"` devient
  `"emergency plumber Valencia"` — le nom de la ville reste, le reste passe en
  anglais. Le lecteur cherche en anglais mais dans une ville espagnole.
- **Prix : inchangés.** « 15 €/mois » s'écrit `€15/month`, symbole avant le
  nombre selon l'usage anglais, montant strictement identique. Idem pour les
  349 €, 99 € et 29 €.
- **Anglais britannique** : *optimised*, *specialising*, *colours*,
  *neighbourhood*, *organisation*. `og:locale` vaut `en_GB`, la date s'écrit
  jour-mois-année (`20 July 2026`).
- **Registre** : *you* neutre. L'anglais ne distingue pas tutoiement et
  vouvoiement — le profil EN n'a donc **aucune garde de registre**, à la
  différence du français.

Le contrôle de résidu castillan du profil EN exclut délibérément les homographes
(`local`, `digital`, `total`, `personal`, `son`, `no`, `la`, `de`) et masque les
toponymes espagnols, les institutions et le logo. Voir `_tools/translate_article.py`,
`EN_ES_WORDS` et `EN_LEGIT`.

#### Registre : divergence assumée entre les langues

| Langue | Registre |
|--------|----------|
| ES | **tutoiement** (`tú`) |
| VAL | **tutoiement** (`tu`) |
| EN | *you* (neutre) |
| FR | **vouvoiement** (`vous`) |

⚠️ **Le français vouvoie, l'espagnol et le valencien tutoient. C'est une divergence
volontaire, pas une incohérence** : le `tú` commercial est la norme en Espagne, le
tutoiement d'un prospect inconnu ne l'est pas en français. Ne pas « harmoniser ».

En FR : `vous / votre / vos / le vôtre`, participes et adjectifs au pluriel de
politesse. Aucune 2ᵉ personne du singulier — ni `tu`, ni `ton/ta/tes`, ni `toi`,
ni impératif singulier (`utilise` → `utilisez`).

Le contrôle est automatisé et **bloquant** : `_tools/translate_article.py` refuse
d'écrire un fichier FR contenant du tutoiement.

#### Cible FR : qui lit ces articles

**Francophones de France, de Belgique et de Suisse.** Ce sont des lecteurs qui
vivent en pays francophone, **pas des expatriés en Espagne** — ces derniers sont
servis par les articles ES.

Décision figée le 2026-08-29. Elle remplace la formulation antérieure
(« francophones des deux côtés »), qui laissait le périmètre ambigu.

Conséquences :

| Élément | Traitement |
|---------|-----------|
| Exemples illustratifs — villes, prénoms, quartiers, adresses, téléphones, noms d'entreprises fictives | **Transposés** en France, Belgique ou Suisse |
| Faits sur WebAutonomos — `areaServed`, NAP, description `Organization` | **Conservés tels quels** |
| Statistiques ATA, INE, Banco de España décrivant le marché de WebAutonomos | **Conservées telles quelles** |
| Prix en euros, « 15 €/mois » | **Inchangés**, strictement tels quels |

La ligne de partage : un **exemple pédagogique** se transpose, un **fait** sur
l'entreprise ou sur le marché d'où elle facture ne se transpose pas.

#### Adaptation culturelle (FR)

- **Villes** : transposer les exemples espagnols en villes francophones — Lyon,
  Nantes, Bruxelles, Lausanne — quartiers compris.
  **Exception** : garder la ville quand elle désigne WebAutonomos lui-même
  (siège d'Ontinyent, `areaServed` « Comunidad Valenciana », adresse du NAP).
  C'est un fait sur l'entreprise, pas un exemple pédagogique.
- **Références réglementaires** espagnoles sans équivalent francophone (RETA,
  Kit Digital, IVA, autónomo societario) : donner l'équivalent local s'il existe,
  sinon **reformuler sans la mention**. Ne jamais traduire littéralement un
  dispositif qui n'existe pas chez le lecteur.
- **Prix** : montants en euros inchangés, et « 15 €/mois » strictement tel quel —
  c'est l'offre commerciale, pas un exemple.

## Workflow de Publication

### Publication automatique (GitHub Action)

Le script `_tools/publish_next.py` est exécuté par `.github/workflows/publish-blog.yml` chaque lundi et jeudi à 06:00 UTC (~08:00 Madrid en été). Il :

1. Lit tous les `_tools/queue/*.json`
2. Garde ceux dont `publish_date ≤ aujourd'hui` et publie **le plus ancien** (un seul par exécution)
3. Appelle `_tools/add_article.py` : insertion SPA dans `index.html` + ajout de l'URL au `sitemap.xml`
4. Déplace le JSON publié dans `_tools/queue/published/`
5. Commit, push, puis `wrangler deploy`

Déclenchement manuel possible : Actions → « Publier un article de blog » → Run workflow (option `force` pour publier
le prochain article de la file sans attendre sa date).

### Déploiement (GitHub Action)

`.github/workflows/deploy.yml` lance `wrangler deploy` à chaque push sur `main` (hors fichiers non déployés :
`CLAUDE.md`, `.github/`, `_tools/`, `scripts/`, etc.). Il n'existe pas d'intégration Cloudflare↔GitHub native :
**sans ce workflow, un push ne publie rien**. En cas de besoin, déploiement manuel via `npx wrangler deploy`.

### Commande Claude Code pour générer un nouvel article :

```bash
# Voir ce qui reste en file d'attente et à quelle date
for f in _tools/queue/*.json; do jq -r '"\(.publish_date)  \(.slug)"' "$f"; done | sort

# Générer l'article — Claude Code va :
# 1. Lire les specs (calendrier.json sert de référence rédactionnelle : sujets, silos, mots-clés)
# 2. Lire le template-article.html comme base
# 3. Créer un JSON dans _tools/queue/ (publish_date, slug, category, readTime + blocs es/val/en)
#    → chaque bloc langue : date, title, seoTitle, metaDescription, keywords, excerpt, content, faq
# 4. Commit + push → le GitHub Action publiera l'article (SPA + sitemap) à la date prévue,
#    puis déploiera automatiquement
```

⚠️ L'insertion dans `index.html` et `sitemap.xml` est faite **par le script** au moment de la publication —
ne pas les éditer à la main pour un nouvel article.

### Checklist SEO Avant Publication (12/12)

- [ ] H1 contient le mot-clé principal (max 60 car.)
- [ ] Meta description < 155 caractères avec CTA
- [ ] 2000-2500 mots
- [ ] Sommaire visible (pas de `<details>`) avec tous les H2
- [ ] FAQ 5 questions avec `<details>/<summary>`
- [ ] 4 Schemas JSON-LD (BlogPosting, FAQPage, BreadcrumbList, Organization)
- [ ] Minimum 2 liens internes même silo + 1 autre silo
- [ ] CTA présent en fin d'article avec lien /contacto
- [ ] Hreflang tags (es, ca-ES, en, x-default)
- [ ] URL canonical correcte
- [ ] Exemples locaux (Valencia, Alicante, Elda, Elche)
- [ ] Fichier ajouté au sitemap.xml

### Mise à jour du Sitemap

Pour les articles passant par `_tools/queue/`, l'ajout au sitemap est **automatique** (`add_article.py`).
Pour toute autre page ajoutée à la main, insérer dans `sitemap.xml` :
```xml
<url>
    <loc>https://webautonomos.es/blog/es/{slug}</loc>
    <lastmod>{YYYY-MM-DD}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
</url>
```

## Commandes Utiles

```bash
# Déployer les changements (push → GitHub Action deploy.yml → wrangler deploy)
git add -A && git commit -m "blog: add article {slug}" && git push origin main

# Déploiement manuel immédiat (nécessite `npx wrangler login`)
npx wrangler deploy

# Vérifier ce qui est réellement en ligne (et non juste committé)
npx wrangler deployments list | tail -10

# File d'attente : articles pas encore publiés, par date
for f in _tools/queue/*.json; do jq -r '"\(.publish_date)  \(.slug)"' "$f"; done | sort

# Articles déjà publiés via la file
ls _tools/queue/published/*.json | wc -l

# Lister les articles HTML autonomes
ls blog/es/*.html | wc -l
```

## Rappels Importants

- **Ne JAMAIS modifier index.html** — c'est le bundle React compilé de Lovable
- **Ne JAMAIS régénérer les 6 articles existants** — ils vivent dans le SPA React
- **Toujours pousser sur `main`** — c'est la branche de production
- **Toujours se baser sur template-article.html** — pour la structure HTML
- **Tester localement** avant de pousser : ouvrir le fichier HTML dans un navigateur
- **Les articles blog sont des pages HTML séparées** — ils ne font pas partie du SPA React
- **Cloudflare sert les fichiers statiques** — les chemins /blog/es/slug.html sont servis directement
- **Committé ≠ en ligne** — vérifier le run `deploy.yml` (ou `npx wrangler deployments list`) après un push
- **Le cache Cloudflare répond `HIT` même après un déploiement raté** — se fier au déploiement, pas au fait que la page charge
