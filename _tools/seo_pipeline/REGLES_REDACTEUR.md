# Règles de l'agent RÉDACTEUR — circuit SEO/GEO WebAutonomos

Tu optimises UNE page du site webautonomos.es pour UNE requête, avec l'aide de
SERPmantics. Un agent relecteur indépendant et des contrôles automatiques
vérifieront ton travail. Une page rejetée n'est pas publiée.

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
3. SERPmantics (outils `mcp__serpmantics__*` ; lis leurs noms exacts dans ta liste d'outils) :
   a. **Solde** : lis le solde de crédits (outil « credits », gratuit). Un guide
      coûte 1 crédit. S'il en reste moins de 2, arrête-toi sans rien modifier et
      écris-le dans le rapport (`points_d_attention`).
   b. **Réutilise avant de créer** : liste les guides existants filtrés sur la
      requête. Ce filtre est une expression régulière insensible à la casse :
      compare toi-même `query`, `lang` et `source`. Un guide qui a exactement la
      même requête, la même langue et la même source, créé il y a moins de
      180 jours, est réutilisé : n'en crée pas un second.
   c. Sinon, crée **au plus deux guides**, avec `lang` = la langue du guide
      indiquée dans la consigne :
      - `source: "google"` : SEO, 1 crédit, guide principal ;
      - `source: "google_ai_overview_citations"` : GEO, contenu des pages citées
        par les réponses IA de Google, 1 crédit.
      Aucune autre source (les moteurs IA coûtent 4 crédits par guide).
      Lis la réponse : une requête dans `guidesFailed` n'a pas créé de guide et
      son crédit est rendu, tu peux la renvoyer une fois ; une requête dans
      `guidesUnknown` ne doit **jamais** être renvoyée (tu paierais deux fois) :
      attends quelques minutes et cherche-la dans la liste des guides. Si le guide
      GEO échoue (pas de réponse IA de Google pour cette requête), continue avec
      le seul guide Google et note-le dans le rapport.
   d. Lis chaque guide : expressions attendues et leurs fourchettes, expressions à
      éviter, statistiques du top 10 (mots, titres, listes).
   e. Outil « score » sur le contenu ACTUEL de la page, pour chaque guide →
      scores de départ.
   f. N'utilise **aucun** outil qui consomme des jetons IA (meta, outline,
      intent, internal-links, eeat, eeat-competitors).
4. Réécris selon la section 2.
5. Outil « score » sur le nouveau contenu, pour chaque guide. Guide Google : vise
   **le niveau médian du top 3**, plafonné à 80 ; au-delà, tu bourres : arrête-toi.
   Guide GEO : améliore-le sans jamais faire baisser le score Google ; en cas de
   conflit entre les deux guides, le guide Google l'emporte.
6. Écris le rapport (section 4). Ne fais NI commit NI push : le script s'en charge.

## 2. Comment réécrire

- **Garde** : prix, boutons et liens de démo (`#pide-demo`, `/pide-tu-demo`,
  `/demandez-votre-demo`, `/get-your-demo`), formulaire, bloc Trustpilot
  (`<div class="proof-num">…</div>`), avis existants mot pour mot, canonical,
  hreflang, textes légaux, scripts, sections « règles » des pages santé.
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
- Expressions « à éviter » : retire-les si c'est sans perte ; **garde** prix et
  formules de paiement même si l'outil les juge « à éviter » (c'est l'argument
  commercial de WebAutonomos).
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

## 3. Interdits (rejet automatique)

- Tout fait absent de `VERITE.md` : ancienneté, nombre de clients, résultats
  obtenus, délais autres que ceux listés, services non listés.
- Tout pourcentage ou statistique de marché.
- Tout client, prénom, entreprise ou « cas réel », même présenté comme exemple.
- Les expressions de la section 8 de `VERITE.md`.
- Toute modification d'une page générée sans passer par son script.
- Santé : témoignages de patients, promesses de résultat, prix promotionnels.

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

## 5. En cas de retour du relecteur

Tu reçois `review.json` et `checks.json`. Corrige **uniquement** les points
signalés, relance l'outil « score » sur les guides existants (ne crée **aucun**
nouveau guide), mets à jour le rapport. Ne réécris pas tout.
