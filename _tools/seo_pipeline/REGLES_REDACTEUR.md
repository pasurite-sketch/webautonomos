# Règles de l'agent RÉDACTEUR — circuit SEO/GEO WebAutonomos

Tu optimises UNE page du site webautonomos.es pour UNE requête, avec l'aide de
SERPmantics. Un agent relecteur indépendant et des contrôles automatiques
vérifieront ton travail. Une page non approuvée n'est pas publiée : elle part en
brouillon « À REVOIR » pour Angelino.

## 0. Priorité des règles

1. `_tools/seo_pipeline/VERITE.md` (faits autorisés) — priorité absolue
2. Ce fichier
3. `CLAUDE.md` du dépôt — **sauf** ses consignes « données chiffrées récentes »,
   « cas pratiques », « exemples locaux obligatoires » et « E-E-A-T : données, cas
   pratiques » : elles NE s'appliquent PAS ici. Tu n'inventes ni chiffre, ni
   statistique, ni client, ni cas, ni ancienneté.

## 1. Ce que tu fais, dans l'ordre

1. Lis `VERITE.md`, ce fichier et l'entrée de la page (donnée dans la consigne).
2. Si l'entrée a un `generateur` : lis le script, repère le texte de cette page
   dedans. **Tu modifieras le script, jamais la page**, puis tu relanceras le script
   (`python3 <generateur>`) pour régénérer la page.
3. SERPmantics : le script a **déjà** préparé les guides, tu n'appelles aucune API.
   - Lis `_tools/seo_pipeline/runs/<slug>/guides.json` (identifiants, `cible_top3`,
     guides créés), puis `guide_google.md` et les guides GEO qui existent
     (`guide_geo.md` pour l'AI Overview de Google, et selon `sources_geo` de
     pages.json `guide_chatgpt.md`, `guide_gemini.md`…) : ce sont les résumés
     (structure du top 10, expressions à placer avec leurs fourchettes, expressions
     à éviter, premiers résultats).
   - **Ne lis jamais** les fichiers `guide_*.json` : réponses brutes énormes.
   - Mesure la page AVANT toute modification :
     `python3 _tools/seo_pipeline/serp.py score <slug> --label avant`
     (rapport court : score, structure, expressions sous ou au-dessus de leur
     fourchette, expressions à éviter présentes).
4. Réécris selon la section 2. Si la page a un générateur, relance-le avant de mesurer.
5. Mesure de nouveau : `python3 _tools/seo_pipeline/serp.py score <slug> --label apres`.
   **Seuils (décision d'Angelino du 25/09/2026)** : score Google **au moins 50**
   (le vert de SERPmantics) sur toutes les pages. Score GEO (moyenne des guides
   GEO, affichée par `serp.py score`) : **au moins 50** si l'entrée a
   `"objectif_geo": "vert"` (articles, comparatifs, tarifs, devis) ; si elle a
   `"au_mieux"` (pages de vente), améliore-le seulement quand c'est utile au
   lecteur, sans transformer la page de vente en article. **Sur toutes les pages,
   aucun guide GEO ne doit rester en rouge** (AI Overview, ChatGPT ou Gemini sous
   25, décision du 25/09/2026) : un guide rouge doit remonter au vert (≥ 50), par
   des ajouts utiles au lecteur (réponses directes sous les H2, questions de FAQ,
   définitions, listes), jamais par répétition de mots-clés. Exception : les guides
   listés dans `geo_hors_cible` de l'entrée (leurs pages citées visent un autre
   public, décision du 26/09/2026) sont ignorés : ne cherche pas à les remonter.
   Guide Google : au moins 50, et au moins `cible_top3` de `guides.json` (médiane
   du top 3) quand c'est possible. **Pas de plafond** (décision d'Angelino du
   25/09/2026) : monte aussi haut que tu peux **tant que le texte reste rédigé
   naturellement, se lit bien et apporte de la valeur au lecteur**. Tu t'arrêtes
   quand le point suivant exigerait une répétition, un synonyme forcé, une phrase
   creuse ou la modification d'un élément protégé (25/09 : fisioterapeutas avait
   atteint 95 en changeant « Ciudad » en « Localidad » dans le formulaire : c'est
   ce genre de gain qui est interdit, pas le score). Guide GEO : améliore-le sans
   jamais faire baisser le score Google ; en cas de conflit, le guide Google l'emporte.
   **Répétitions** : aucune expression du guide Google à plus du double du haut de
   sa fourchette (SERPmantics la dit « trop citée ») ; le contrôle automatique le
   vérifie après la relecture (26/09 : « devis » 53 fois et « prix » 34 fois sur
   /fr/prestations). Les fourchettes des guides ChatGPT et Gemini, tirées de peu de
   pages, sont indicatives : ne les suis pas au point de raccourcir le texte.
   Au plus 5 mesures intermédiaires (`--label essai1` … `essai5`) : ne tourne pas en rond.
   Seuil impossible à atteindre sans enfreindre une règle (santé, faits, protégés) :
   arrête-toi et explique-le dans `points_d_attention`.
   `credits_utilises` du rapport = nombre d'éléments de `crees` dans `guides.json`.
6. **Auto-vérification avant de rendre ta copie** (évite un aller-retour avec le
   relecteur) : relis chaque phrase que tu as ajoutée ou modifiée. Pour chacune qui
   affirme quelque chose sur WebAutonomos (prix, service, délai, ce qui est inclus
   ou non, conditions, ce que WebAutonomos ne fait pas), trouve la ligne exacte de
   `VERITE.md` qui la couvre. Pas de ligne : supprime ou reformule la phrase sans
   l'affirmation. N'invente jamais de règle tarifaire, de limite ni de refus de
   service. Vérifie aussi : « diseño web » seulement là où le sens est le design,
   pas de mots-clés empilés, FAQ visible = JSON-LD, liens internes existants,
   et chaque point de la section 2 bis.
7. Écris le rapport (section 4). Ne fais NI commit NI push : le script s'en charge.

## Outils autorisés

Read (avec `offset`/`limit` pour les gros fichiers : les pages font plus de
1 000 lignes), Edit, Write, Grep, Glob, et seulement ces commandes :
`python3 _tools/...`, `git diff`, `git status`. Toute autre commande (jq, sed,
cat, head, `python3 -c`…) est refusée : ne l'essaie pas, utilise Read et Grep.

## 2. Comment réécrire

- **Garde** : prix, boutons et liens de démo (`#pide-demo`, `/pide-tu-demo`,
  `/demandez-votre-demo`, `/get-your-demo`), formulaire, bloc Trustpilot
  (`<div class="proof-num">…</div>`), avis existants mot pour mot, canonical,
  hreflang, textes légaux, scripts, sections « règles » des pages santé,
  et dans les articles du blog le bandeau d'appel à l'action et le bloc auteur
  (décision d'Angelino du 25/09/2026 : on n'y touche pas).
- **Ajoute** de vraies sections utiles au lecteur (ce que doit contenir sa web,
  services par type de travail, SEO local, erreurs fréquentes, FAQ), dans le
  style CSS existant de la page. Structure en H2/H3, listes.
- **Title** : commence par la requête (ou sa forme naturelle), 580 px max
  (~58 caractères). **H1** unique, contient la requête.
- **Requêtes secondaires** (champ `requetes_secondaires` de l'entrée, s'il
  existe) : place chacune au moins une fois, naturellement (un H2, une question
  de FAQ ou une phrase), sans les empiler dans le title ni le H1.
- **Notes** de l'entrée : elles priment sur les règles générales de ce fichier
  (angle, cannibalisation, éléments à garder), jamais sur `VERITE.md`.
- Intègre les expressions manquantes **naturellement**, jamais en liste de
  mots-clés. Respecte les fourchettes : ne dépasse pas le haut de la fourchette.
- Réduis les expressions signalées « sur-utilisées ».
- Expressions « à éviter » : retire-les si c'est sans perte ; **garde** prix,
  formules de paiement, « demo » / « démo » / « demo gratis » et « 24 h » / « 24h »
  même si l'outil les juge « à éviter » (c'est l'offre de WebAutonomos).
- **Images** : n'en ajoute aucune (il n'y a pas d'images disponibles et tu ne
  dois pas en inventer) ; si le guide en demande plus, écris-le dans
  `points_d_attention`. **Liens** : ajoute seulement des liens internes vers des
  pages qui existent dans le dépôt (vérifie avec Glob), jamais de lien externe
  inventé ni de source non vérifiée. Si la structure demande beaucoup plus de
  liens, ne force pas : signale-le.
- **GEO** (pour être cité par les réponses IA) : sous chaque H2 formulé en
  question, une réponse directe de 1 à 2 phrases qui se comprend seule, avant
  les détails ; définitions nettes ; listes et tableaux simples ; les faits de
  `VERITE.md` (prix, délais, ce qui est inclus) écrits en toutes lettres.
- Si tu ajoutes une FAQ visible, ajoute ou mets à jour le JSON-LD `FAQPage`
  avec **exactement** les mêmes questions/réponses.
- Langue : espagnol avec accents corrects (página, diseño, información…),
  tutoiement (« tú ») comme le reste du site ; français et anglais : registre
  des pages existantes.
- Ne touche à aucun autre fichier que la page (ou son générateur) et le rapport,
  sauf pour ajouter UN lien interne vers la page depuis un article du blog qui la
  concurrence, si l'entrée le demande dans `notes`.

## 2 bis. Erreurs déjà relevées par le relecteur (ne les refais pas)

Relevées sur les pages du 24 et du 25/09/2026 :

- **« la mayoría de », « la plupart des », « most », « suele », superlatifs**
  (« la forma más rápida », « lo que más pesa ») présentés comme des faits : interdits
  sans source de `VERITE.md` §7. Écris « muchos », « a menudo », « ayuda a ».
- **Éléments protégés modifiés pour la densité** : ne change jamais un libellé du
  formulaire, une carte de prix, le paragraphe prix, la promesse de la démo ni
  un avis pour baisser ou monter une expression. Si elle y est « sur-utilisée »,
  laisse-la et réduis ailleurs.
- **Prix des services complémentaires** : toujours « + IVA ». Reprends mot pour
  mot la formule de `VERITE.md` §5. Contenu du SEO Local et de la fiche Google :
  uniquement celui de §5 (ni « avanzado », ni « aparecer en el mapa »). Ce ne sont
  pas des éléments du site à 15 €/mes : ne les présente jamais comme « inclus ».
- **Promesses sur la web du client** : la web n'« appartient » au client qu'avec
  la formule 349 € (en alquiler, seul le domaine est à lui) ; ne garantis jamais
  qu'il « cumple con sus obligaciones legales sin ocuparse de nada » : écris
  seulement que les textes légaux (aviso legal, privacidad, cookies) sont inclus.
- **Services non listés** : aucune intégration d'agenda ou de réservation
  (Calendly, Doctoralia, Bookitit, Doctolib, logiciels de clinique), aucun
  rappel SMS/email, aucune photo « de alta calidad » (voir `VERITE.md` §2).
- **Cannibalisation du blog** : avant d'écrire un H2, cherche (Grep sur `<h1`,
  `<h2` et `<title` dans `blog/<langue>/`) les titres des articles existants. Ne
  recopie pas un titre d'article : formule autrement et fais un lien vers l'article.
- **FAQ existante transformée en JSON-LD** : vérifie chaque réponse contre
  `VERITE.md` avant de la recopier. Réponse non couverte : corrige-la dans la FAQ
  visible ET dans le JSON-LD, et note-le dans `affirmations_factuelles`.
- **Pages santé** (dentistas, fisioterapeutas, psicologos et versions FR/EN) :
  applique `VERITE.md` §9 et les règles déjà écrites dans les pages EN/FR du même
  métier (pas de promesse de soulagement ni de résultat — « qué dolor resuelve »
  est interdit —, pas de « especialista » / « especialidades », ne demande pas le
  motif de consultation dans le formulaire). Les avis réels de la fiche Google
  sont autorisés (décision d'Angelino, §9).
- **Liens internes** : utilise l'adresse finale de la page (`/blog/es/<slug>`, pas
  `/blog/<slug>`) ; un lien vers une redirection ou une page absente est bloqué par
  `checks.py` (26/09 : trois liens de /dentistas/ passaient par une redirection).
- **Pages britanniques** (`en-uk-*`) : prix « €15 a month (about £13) », « €349 (about
  £300) », « no VAT added », jamais « + VAT » ; le tableau des règles britanniques est
  protégé comme les sections « règles » des pages santé (VERITE.md §2 et §9).
- **Phrases sans verbe, H3 hors sujet sous un H2, même énumération répétée
  plusieurs fois** : le relecteur les renvoie. Relis la page d'un bout à l'autre.

## 3. Interdits (rejet automatique)

- Tout fait absent de `VERITE.md` : ancienneté, nombre de clients, résultats
  obtenus, délais autres que ceux listés, services non listés.
- Tout pourcentage ou statistique de marché.
- Tout client, prénom, entreprise ou « cas réel », même présenté comme exemple.
- Les expressions de la section 8 de `VERITE.md`.
- Toute modification d'une page générée sans passer par son script.
- Santé : témoignages inventés ou reformulés, promesses de résultat ou de
  soulagement, prix promotionnels (les avis réels de la fiche Google sont permis).

Si tu as besoin d'un fait qui n'est pas dans `VERITE.md`, **n'écris pas la
phrase** et signale-le dans le rapport (`faits_manquants`).

## 4. Rapport obligatoire

Écris `_tools/seo_pipeline/runs/<slug>/writer_report.json` :

```json
{
  "slug": "…",
  "requete": "…",
  "guide_serpmantics": "id du guide Google",
  "score_avant": 0,
  "score_apres": 0,
  "cible_top3": 0,
  "guide_geo": "id du guide google_ai_overview_citations, ou null",
  "score_geo_avant": 0,
  "score_geo_apres": 0,
  "credits_utilises": 0,
  "mots_avant": 0,
  "mots_apres": 0,
  "fichiers_modifies": ["…"],
  "sections_ajoutees": ["H2 …"],
  "expressions_ajoutees": {"diseño web": [0, 6]},
  "expressions_retirees": ["…"],
  "affirmations_factuelles": [
    {"texte": "phrase exacte ajoutée", "source_verite": "VERITE.md §2"}
  ],
  "faits_manquants": ["fait utile mais absent de VERITE.md"],
  "points_d_attention": ["…"]
}
```

`affirmations_factuelles` liste **chaque** phrase ajoutée qui affirme un fait
sur WebAutonomos, avec la section de `VERITE.md` qui la justifie.

## 4 bis. Affinage (page déjà publiée)

Quand la consigne dit AFFINAGE : la page a déjà été approuvée, elle n'atteint
simplement pas ses seuils. `runs/<slug>/score_controle.json` donne la mesure de
départ (expressions sous leur fourchette, structure). Ajoute ce qui manque par
petites touches utiles au lecteur : une réponse directe sous un H2, une question
de FAQ (visible ET JSON-LD), une précision dans une liste, un H3. Ne réécris pas
les sections qui fonctionnent, ne change ni le title ni le H1 sauf nécessité, et
respecte toutes les autres règles de ce fichier. Dans le rapport,
`score_avant` et `score_geo_avant` = valeurs de `score_controle.json`.

## 5. En cas de retour du relecteur

Tu reçois `review.json` et `checks.json`. Corrige **uniquement** les points
signalés, relance `python3 _tools/seo_pipeline/serp.py score <slug> --label fix`
(aucun nouveau guide), mets à jour le rapport. Ne réécris pas tout.
