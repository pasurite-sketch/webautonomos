# CLAUDE.md — Règles Projet WebAutonomos.es

## Identité du Projet

- **Site** : https://webautonomos.es
- **Activité** : Agence web spécialisée sites vitrines pour autónomos (artisans + professions libérales)
- **Zone** : Comunidad Valenciana, Espagne
- **Offre principale** : Site vitrine à 15€/mois (modèle location)
- **Services complémentaires** : Google My Business (99€ setup + 29€/mois), SEO Local (+15€/mois)
- **Repo** : github.com/pasurite-sketch/webautonomos
- **Hébergement** : Cloudflare Pages (Worker-based, auto-deploy depuis GitHub branche `main`)

## Stack Technique

- **Architecture** : React SPA (Single Page Application) — un seul `index.html` (~536KB)
- **Hébergement** : Cloudflare Pages via `wrangler.jsonc` (assets statiques)
- **DNS + Email** : Cloudflare (email routing vers info@webautonomos.es)
- **Domaine** : webautonomos.es (registrar DonDominio)
- **Déploiement** : `git push origin main` → auto-deploy Cloudflare
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
├── calendrier.json         # Calendrier éditorial blog
├── blog-spa-data.json      # Données SPA pré-générées (3 langues) pour publish-articles.js
├── template-article.html   # Template HTML de référence pour les articles
├── scripts/
│   └── publish-articles.js # Script auto-publication SPA + sitemap
├── .github/
│   └── workflows/
│       └── publish-articles.yml  # GitHub Action (lun/jeu 8h Madrid)
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
**Ajout au SPA** : automatisé via GitHub Action (`scripts/publish-articles.js`) selon les dates de `calendrier.json`

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

### Traductions (VAL + EN)

- Les traductions ne sont PAS littérales — elles sont adaptées culturellement
- VAL : Valencien/Catalan, respecter la normative linguistique AVL
- EN : Anglais international, adapter les exemples au contexte espagnol
- Hreflang : `es`, `ca-ES` (pour valencien/catalan), `en`
- Les slugs peuvent varier légèrement entre langues si nécessaire

## Workflow de Publication

### Publication automatique (GitHub Action)

Le script `scripts/publish-articles.js` est exécuté automatiquement par `.github/workflows/publish-articles.yml` chaque lundi et jeudi à 8h (heure Madrid). Il :

1. Lit `calendrier.json` et `blog-spa-data.json`
2. Trouve les articles avec `publish_date ≤ aujourd'hui` et `status: "published"`
3. Insère les entrées SPA dans `index.html` (3 langues : ES, VAL, EN)
4. Ajoute les URLs manquantes dans `sitemap.xml`
5. Met à jour `calendrier.json` (`status: "published_spa"`)
6. Commit, push, et déploie via Cloudflare Workers

### Commande Claude Code pour générer un nouvel article :

```bash
# Lire le calendrier pour identifier le prochain article à publier
cat calendrier.json | jq '.articles[] | select(.status == "pending")' | head -1

# Générer l'article — Claude Code va :
# 1. Lire les specs dans calendrier.json
# 2. Lire le template-article.html comme base
# 3. Créer le fichier HTML dans blog/es/
# 4. Générer les données SPA (ES/VAL/EN) dans blog-spa-data.json
# 5. Ajouter l'URL dans sitemap.xml
# 6. Mettre à jour calendrier.json (status: "published")
# 7. Commit + push → le GitHub Action ajoutera l'article au SPA à la date prévue
```

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

Après chaque article publié, ajouter dans `sitemap.xml` :
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
# Déployer les changements
git add -A && git commit -m "blog: add article {slug}" && git push origin main

# Vérifier le statut du calendrier
cat calendrier.json | jq '[.articles[] | .status] | group_by(.) | map({status: .[0], count: length})'

# Lister les articles publiés
ls blog/es/*.html | wc -l

# Voir le prochain article à publier
cat calendrier.json | jq '.articles[] | select(.status == "pending") | {id, title_es, silo, publish_date}' | head -20
```

## Rappels Importants

- **Ne JAMAIS modifier index.html** — c'est le bundle React compilé de Lovable
- **Ne JAMAIS régénérer les 6 articles existants** — ils vivent dans le SPA React
- **Toujours pousser sur `main`** — c'est la branche de production
- **Toujours se baser sur template-article.html** — pour la structure HTML
- **Tester localement** avant de pousser : ouvrir le fichier HTML dans un navigateur
- **Les articles blog sont des pages HTML séparées** — ils ne font pas partie du SPA React
- **Cloudflare sert les fichiers statiques** — les chemins /blog/es/slug.html sont servis directement
