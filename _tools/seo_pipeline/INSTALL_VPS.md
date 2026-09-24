# Installer le circuit SEO sur le VPS OVH

Pour un VPS **Ubuntu ou Debian**. Une commande par étape : exécute-la, vérifie
le résultat indiqué, puis passe à la suivante.

## A. Préparer les accès (sur ton ordinateur, une seule fois)

1. **Clé API Anthropic** : console.anthropic.com → API Keys → Create key.
   Garde-la de côté. Mets une limite de dépense mensuelle (Billing → Limits),
   par exemple 50 $ pour commencer.
2. **Clé API SERPmantics** (offre Pionnier ou plus) : page « API / MCP » de
   SERPmantics → créer une clé.
3. **Jeton GitHub limité au dépôt** : github.com → Settings → Developer settings →
   Fine-grained tokens → Generate new token
   - Repository access : *Only select repositories* → `pasurite-sketch/webautonomos`
   - Permissions : **Contents : Read and write**, **Pull requests : Read and write**
   - Rien d'autre.

## B. Installer les outils (sur le VPS)

1. `node -v` → doit afficher v18 ou plus. Sinon :
   `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -` puis `sudo apt install -y nodejs`
2. `sudo apt update`
3. `sudo apt install -y git python3 python3-pil fonts-liberation gh`
   (si `gh` est introuvable : voir https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
4. `sudo npm install -g @anthropic-ai/claude-code`
5. `claude --version` → doit afficher un numéro de version.
6. `claude --help | grep -E "mcp-config|allowedTools|permission-mode|max-turns|output-format|effort"`
   → vérifie que ces options existent. Si une option a changé de nom, dis-le-moi
   avant d'aller plus loin.

## C. Récupérer le dépôt

1. `gh auth login` → GitHub.com → HTTPS → *Paste an authentication token* → colle le jeton de A.3
2. `gh auth setup-git`
3. `git clone https://github.com/pasurite-sketch/webautonomos.git ~/webautonomos`
4. `cd ~/webautonomos`
5. `git config user.name "Circuit SEO WebAutonomos"`
6. `git config user.email "info@webautonomos.es"`

## D. Les clés

1. `nano ~/.seo_pipeline.env` puis colle (avec tes vraies clés) :

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   SERPMANTICS_API_KEY=...
   WRITER_MODEL=claude-sonnet-5
   REVIEWER_MODEL=claude-opus-5-5
   AUTO_MERGE=0
   ```

   Enregistre avec Ctrl+O, Entrée, puis Ctrl+X.
2. `chmod 600 ~/.seo_pipeline.env`

`AUTO_MERGE=0` : toutes les pages attendent ton clic sur GitHub au début.
On passera à `1` quand les premières pages auront fait leurs preuves.

Réglage d'effort du relecteur : si l'étape B.6 montre une option d'effort
(par ex. `--effort high`), ajoute la ligne `REVIEWER_EXTRA_ARGS=--effort high`.

## E. Vérifications avant le premier vrai passage

1. `python3 _tools/seo_pipeline/pipeline.py status` → le tableau des 30 pages
2. `python3 _tools/seo_pipeline/pipeline.py next --n 5` → les pages prêtes
3. **Test de la connexion SERPmantics** (1 crédit) :
   `set -a; . ~/.seo_pipeline.env; set +a; claude -p "Avec l'outil serpmantics get_credits, donne-moi mon solde de crédits et de jetons." --mcp-config _tools/seo_pipeline/mcp.json --allowedTools mcp__serpmantics`
   → doit afficher ton solde. Si c'est une erreur d'authentification, le nom
   de l'en-tête dans `mcp.json` est peut-être différent : envoie-moi le message.

## F. Premier passage, sur une seule page

1. `bash _tools/seo_pipeline/run_page.sh es-fontaneros`
   → 10 à 30 minutes. À la fin : « PR ouverte : https://github.com/... »
2. Ouvre le lien, lis le résumé, regarde le coût estimé en bas.
3. Envoie-moi le lien de la PR : on vérifie ensemble ce premier résultat
   avant de lancer les suivantes.

## G. Ensuite, en automatique (après validation du premier passage)

1. `crontab -e` puis ajoute la ligne (3 pages chaque nuit à 3 h) :

   ```
   0 3 * * * cd ~/webautonomos && N=3 bash _tools/seo_pipeline/run_batch.sh >> ~/seo_pipeline.log 2>&1
   ```

2. Chaque matin : GitHub t'envoie un email par PR. Les pages santé portent
   « [À VALIDER] » dans le titre.

## En cas de problème

- Journal d'une page : `cat ~/webautonomos/_tools/seo_pipeline/runs/<slug>/run.log`
- Verdict du relecteur : `cat ~/webautonomos/_tools/seo_pipeline/runs/<slug>/review.json`
- État de toutes les pages : `python3 _tools/seo_pipeline/pipeline.py status`
- Remettre une page bloquée dans la file : `python3 _tools/seo_pipeline/pipeline.py state <slug> a_refaire`
