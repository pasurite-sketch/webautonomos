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
├── index.html          # React SPA (tout le site)
├── robots.txt          # Directives crawlers
├── sitemap.xml         # Plan du site pour Google
├── wrangler.jsonc      # Config Cloudflare Workers
├── CLAUDE.md           # Ce fichier (règles projet)
├── calendrier.json     # Calendrier éditorial blog
└── blog/               # Articles de blog (fichiers HTML individuels)
    └── es/             # Articles en espagnol
    └── val/            # Articles en valencien
    └── en/             # Articles en anglais
```

## Blog — Objectif & Stratégie

### But du Blog
Attirer du trafic organique vers webautonomos.es via du contenu SEO ciblant les autónomos espagnols qui cherchent à améliorer leur présence digitale. Chaque article doit démontrer l'expertise de WebAutonomos et inciter le lecteur à demander un devis.

### 4 Silos Thématiques (Catégories)

| Silo | Slug catégorie | Description | Mot-clé racine |
|------|---------------|-------------|----------------|
| **Presencia Digital** | `paginas-web` | Pourquoi et comment avoir un site web | páginas web para autónomos |
| **SEO Local** | `seo-local` | Référencement local, Google Maps | SEO local para autónomos |
| **Google My Business** | `google-my-business` | Optimisation fiche GBP | optimizar Google My Business |
| **Marketing Digital** | `marketing-digital` | Stratégies marketing pour artisans | marketing digital autónomos |

### Calendrier de Publication
- **Rythme** : 2 articles/semaine (lundi + jeudi)
- **Durée** : 14 semaines (S1 à S14)
- **Total** : 28 articles en espagnol (versions VAL + EN en différé)
- **Source** : `calendrier.json`

## Règles de Génération d'Articles

### Format de Sortie
Chaque article est un fichier HTML autonome :
- **Chemin** : `blog/{lang}/{slug}.html`
- **Exemple** : `blog/es/por-que-tu-negocio-necesita-una-web.html`

### Structure HTML d'un Article

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titre} | WebAutonomos Blog</title>
    <meta name="description" content="{meta_description max 155 caractères}">
    <meta property="og:title" content="{titre}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://webautonomos.es/blog/{lang}/{slug}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://webautonomos.es/blog/{lang}/{slug}">
    <!-- Hreflang pour les versions multilingues -->
    <link rel="alternate" hreflang="es" href="https://webautonomos.es/blog/es/{slug-es}">
    <link rel="alternate" hreflang="ca" href="https://webautonomos.es/blog/val/{slug-val}">
    <link rel="alternate" hreflang="en" href="https://webautonomos.es/blog/en/{slug-en}">
    <!-- Style Tailwind CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Schema.org Article -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "{titre}",
        "description": "{meta_description}",
        "author": {
            "@type": "Organization",
            "name": "WebAutonomos",
            "url": "https://webautonomos.es"
        },
        "publisher": {
            "@type": "Organization",
            "name": "WebAutonomos"
        },
        "datePublished": "{YYYY-MM-DD}",
        "dateModified": "{YYYY-MM-DD}",
        "mainEntityOfPage": "https://webautonomos.es/blog/{lang}/{slug}",
        "inLanguage": "{es|ca|en}"
    }
    </script>
</head>
<body class="bg-gray-50">
    <!-- Navigation minimale avec lien retour -->
    <nav>...</nav>

    <article class="max-w-3xl mx-auto px-4 py-8">
        <!-- Breadcrumb -->
        <!-- Badge catégorie + Date -->
        <!-- H1 : titre de l'article -->
        <!-- Temps de lecture estimé -->
        <!-- Contenu structuré H2/H3 -->
        <!-- CTA vers webautonomos.es/contacto -->
        <!-- Articles connexes (même silo) -->
        <!-- Auteur WebAutonomos -->
    </article>

    <footer>...</footer>
</body>
</html>
```

### Règles de Contenu SEO

1. **Titre H1** : Inclure le mot-clé principal, max 60 caractères
2. **Meta description** : Inclure le mot-clé, max 155 caractères, avec appel à l'action
3. **Structure** : H1 → H2 (sections principales) → H3 (sous-sections). Jamais sauter de niveau.
4. **Longueur** : 1200-2000 mots par article
5. **Mot-clé principal** : Dans H1, premier paragraphe, au moins 2 H2, meta description, URL slug
6. **Mots-clés secondaires** : 3-5 variations naturelles dans le corps du texte
7. **Liens internes** : Minimum 2 liens vers d'autres articles du même silo + 1 lien vers un article d'un autre silo
8. **CTA** : Chaque article doit se terminer par un appel à l'action vers webautonomos.es (demande de devis, contact, etc.)
9. **Ton** : Expert mais accessible. Tutoiement ("tú"). Concret avec des exemples locaux (Valencia, Alicante, Elda, Elche).
10. **Localisation** : Mentionner des villes/quartiers de la Comunidad Valenciana quand pertinent
11. **E-E-A-T** : Démontrer Expérience, Expertise, Autorité, Confiance. Citer des données, des cas pratiques.
12. **Pas de spam IA** : Contenu utile, spécifique, pas de remplissage générique

### Règles de Nommage

- **Slugs** : en minuscules, mots séparés par des tirets, sans accents
  - ✅ `seo-local-para-autonomos`
  - ❌ `SEO_Local_Para_Autónomos`
- **Fichiers** : `blog/{lang}/{slug}.html`
- **Images** : `blog/img/{slug}-{n}.webp` (si nécessaire)

### Maillage Interne (Liens entre articles)

Suivre la structure "toile d'araignée" :
- Chaque article du silo lie vers au moins 2 autres articles du même silo
- Chaque article lie vers au moins 1 article d'un silo différent
- Utiliser des ancres de texte descriptives (pas "cliquez ici")
- Le premier article de chaque silo est le "pilier" (article le plus long et complet)

### Traductions (VAL + EN)

- Les traductions ne sont PAS des traductions littérales — elles sont adaptées culturellement
- VAL : Valencien/Catalan, respecter la normative linguistique AVL
- EN : Anglais international, adapter les exemples au contexte espagnol
- Les slugs peuvent varier légèrement entre langues si nécessaire

## Workflow de Publication

### Commande Claude Code pour générer un article :

```bash
# Lire le calendrier pour identifier le prochain article à publier
cat calendrier.json | jq '.articles[] | select(.status == "pending")' | head -1

# Générer l'article
# Claude Code va :
# 1. Lire les specs dans calendrier.json
# 2. Créer le fichier HTML dans blog/es/
# 3. Mettre à jour calendrier.json (status: "published")
# 4. Mettre à jour sitemap.xml
# 5. Commit + push
```

### Checklist Avant Publication

- [ ] Titre H1 contient le mot-clé principal
- [ ] Meta description < 155 caractères
- [ ] Au moins 1200 mots
- [ ] Minimum 2 liens internes (même silo)
- [ ] Minimum 1 lien interne (autre silo)
- [ ] CTA présent en fin d'article
- [ ] Schema.org BlogPosting valide
- [ ] Hreflang tags présents
- [ ] URL canonical correcte
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

# Valider le HTML
npx html-validate blog/es/{slug}.html
```

## Rappels Importants

- **Ne JAMAIS modifier index.html** manuellement — c'est le bundle React compilé de Lovable
- **Toujours pousser sur `main`** — c'est la branche de production
- **Tester localement** avant de pousser : ouvrir le fichier HTML dans un navigateur
- **Les articles blog sont des pages HTML séparées** — ils ne font pas partie du SPA React
- **Cloudflare sert les fichiers statiques** — les chemins /blog/es/slug.html sont servis directement
