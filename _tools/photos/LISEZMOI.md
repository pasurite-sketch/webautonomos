# Une photo par page — automatisation

Mise en place le 29/09/2026. L'étude SERPmantics du 29/09 a montré que 283 des
291 pages du site n'avaient aucune image, alors que les quatre moteurs (Google,
AI Overview, ChatGPT, Gemini) en attendent sur toutes les pages analysées.

## Qui fait quoi

| Étape | Où |
|---|---|
| 1. Repérer les pages sans photo, les regrouper par sujet | VPS, `photos.py inventaire` (chaque nuit) |
| 2. Lire la page | VPS : titre, introduction, scène préparée dans `sujets.json` |
| 3. Rédiger le prompt (avec l'URL) | VPS, `photos.py` (`construire_prompt`) |
| 4. Générer la photo | ChatGPT, GPT « Photos WebAutonomos », abonnement d'Angelino : il tape « suivante » |
| 5. Télécharger et réduire la photo | VPS, `serveur.py` : 1600×900 en JPEG, WebP et WebP 800 px |
| 6. Poser la photo et publier | VPS : pages, données des articles, commit et push (GitHub Actions déploie) |

Le GPT ne fait qu'une chose que le serveur ne peut pas faire : générer l'image
avec l'abonnement ChatGPT. Il récupère le prompt par l'action `obtenirSuivante`
et renvoie l'image par `envoyerPhoto` (le mécanisme officiel `openaiFileIdRefs`
des GPT). Aucun robot ne pilote chatgpt.com : les conditions d'OpenAI
l'interdisent et la protection anti-robot le bloquerait.

## Fichiers

- `sujets.json` : la file. Un sujet = une photo partagée par les versions
  linguistiques d'une même page. `statut` : `pret`, `fait`, `saute`.
  `scene` : ce que la photo montre (écrite pour les 87 sujets du 29/09 ; pour une
  nouvelle page sans scène, ChatGPT choisit). `fichier` : nom dans `assets/`.
- `images.json` : la photo de chaque page (clé = fichier HTML), avec le texte
  alternatif et la légende dans la langue de la page. Écrit par `photos.py`.
- `photos_lib.py` : position et balisage. `injecter(rel, html)` est appelée par
  les générateurs juste avant d'écrire leurs pages (`poser_photo`), si bien
  qu'une page régénérée garde sa photo : `build_metier_pages`, `build_uk_pages`,
  `build_lang_homes`, `build_expat_pages`, `build_comparatifs`,
  `build_i18n_pages`, `generate_blog_index`. **Ne pas retirer ces crochets.**
- `serveur.py` : l'API appelée par le GPT (VPS, derrière le tunnel Cloudflare).
- `gpt/` : instructions et schéma des actions du GPT.
- `vps/` : services systemd et script d'installation.

## Où la photo est posée

- Article : juste après l'introduction, balisage identique à celui de
  `generate_spa_articles.py`. Le bloc `image` est aussi ajouté aux données de
  `index.html` (et à la file d'attente pour un article pas encore paru). Les
  articles existants ne sont **jamais régénérés** : leurs fichiers ont divergé des
  données (retouches du 14/09, nettoyages des 27 et 28/09).
- Page à bandeau (`section.hero`, `header.hero`) : juste après le bandeau et son
  fil d'Ariane.
- Page simple (H1 dans `<main>`) : après le paragraphe `p.lede` et ce qui le
  complète (note fiscale, encadré, boutons).

Exclus : l'accueil SPA `/` (hors automatisation, à traiter à la main), les pages
légales, et jusqu'à la fin de leur gel les pages gelées par
`_tools/seo_pipeline/pages.json` (`/precios` et « cuánto cuesta », gelées
jusqu'au 22/10 : la photo y est posée automatiquement le 23/10).

## Règles des photos

Photo réaliste, sans texte, logo ni marque lisibles, écrans flous ou éteints,
personne ne regarde l'objectif. Jamais présentée comme un client, un patient ou
un cas réel (légende comprise). Pages santé : aucun patient reconnaissable, pas
d'avant/après, pas de soin en gros plan.

## Commandes utiles (Mac ou VPS)

```bash
python3 _tools/photos/photos.py statut        # avancement
python3 _tools/photos/photos.py prompt art-13 # prompt que recevra ChatGPT
python3 _tools/photos/photos.py verifier      # chaque photo prévue est en place
python3 _tools/photos/photos.py essai         # teste la position partout, sans écrire
```

Poser une photo à la main (sans le GPT) :
`python3 _tools/photos/photos.py appliquer SUJET image.png textes.json`, où
`textes.json` vaut `[{"langue":"es","alt":"…","legende":"…"}, …]`.

## VPS

Utilisateur `ubuntu`, clone dédié `~/photos/webautonomos` (clé de déploiement
GitHub `photos-bot`), configuration `~/.config/photos/env`, journal
`~/.local/state/photos/serveur.log`. Services utilisateur : `photos-api`,
`photos-tunnel` (https://photos.webautonomos.es), `photos-nuit.timer` (4 h 40 :
inventaire des nouvelles pages, réapplication des photos effacées, contrôle).
Installation : `bash _tools/photos/vps/installer.sh` (étapes numérotées).
