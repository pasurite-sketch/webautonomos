#!/usr/bin/env bash
# Traite UNE page : rédacteur → contrôles → relecteur (→ correction) → PR GitHub.
# Usage : bash _tools/seo_pipeline/run_page.sh <slug> [--reprise | --reparer | --affiner]
#   --reprise : reprend un passage interrompu sur sa branche seo/<slug>-… (contrôles, relecture, suite)
#   --reparer : repart de la dernière version écrite (runs/<slug>/diff.patch) et des
#               remarques du relecteur (runs/<slug>/review.json) : passes de correction,
#               relecture, PR. Sert aux pages non approuvées lors d'un passage précédent.
#   --affiner : page déjà publiée. Mesure gratuite des scores SERPmantics ; si la page
#               n'atteint pas ses seuils (Google ≥ 50, GEO ≥ 50 pour les articles), passe
#               de retouche minimale, relecture, PR. Sinon, rien (code de sortie 3).
# Une page non approuvée n'est jamais jetée : elle part en PR brouillon « [À REVOIR] »
# avec les remarques du relecteur (non fusionnable en l'état, jamais publiée seule).
# Codes de sortie : 0 PR ouverte ou fusionnée · 1 échec ou À REVOIR · 2 condition non
# remplie (rien touché) · 3 affinage inutile, la page est déjà au vert.
# Variables (fichier ~/.seo_pipeline.env) :
#   CLAUDE_CODE_OAUTH_TOKEN (abonnement) ou ANTHROPIC_API_KEY ; SERPMANTICS_API_KEY
#   WRITER_MODEL   (défaut claude-sonnet-5)   REVIEWER_MODEL (défaut claude-opus-5-5)
#   REVIEWER_EXTRA_ARGS  (ex. réglage d'effort, voir INSTALL_VPS.md)
#   MAX_FIX=2      nombre maximal de corrections après relecture
#   AUTO_MERGE=0   1 = fusion automatique des pages mode "auto" approuvées
#
# Tout le script est dans main() : bash le lit en entier avant de l'exécuter, donc un
# `git pull` qui modifie ce fichier pendant qu'il tourne ne peut pas le corrompre.
main() {
set -euo pipefail
SLUG="${1:?usage: run_page.sh <slug> [--reprise | --reparer | --affiner]}"
REPO="$(git rev-parse --show-toplevel)"
cd "$REPO"
P="_tools/seo_pipeline"
[ -f "$HOME/.seo_pipeline.env" ] && set -a && . "$HOME/.seo_pipeline.env" && set +a
# Authentification Claude : abonnement (CLAUDE_CODE_OAUTH_TOKEN, via `claude setup-token`)
# ou clé API (ANTHROPIC_API_KEY). Si les deux sont présentes, claude -p utilise la clé API :
# on la retire donc quand un jeton d'abonnement est fourni.
if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
  unset ANTHROPIC_API_KEY
elif [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "ni CLAUDE_CODE_OAUTH_TOKEN ni ANTHROPIC_API_KEY : arrêt" >&2; exit 2
fi
: "${SERPMANTICS_API_KEY:?SERPMANTICS_API_KEY manquante}"
WRITER_MODEL="${WRITER_MODEL:-claude-sonnet-5}"
REVIEWER_MODEL="${REVIEWER_MODEL:-claude-opus-5-5}"
MAX_FIX="${MAX_FIX:-2}"
AUTO_MERGE="${AUTO_MERGE:-0}"
RUN="$P/runs/$SLUG"
mkdir -p "$RUN"
log(){ echo "[$(date '+%F %T')] $SLUG — $*" | tee -a "$RUN/run.log"; }
state(){ python3 "$P/pipeline.py" state "$SLUG" "$@"; }

MODE="$(python3 "$P/pipeline.py" field "$SLUG" mode)"
[ "$MODE" = "manuel" ] && { log "mode manuel : ignorée"; exit 0; }

REPRISE=0
REPARER=0
AFFINER=0
case "${2:-}" in
  "") ;;
  --reprise) REPRISE=1 ;;
  --reparer) REPARER=1 ;;
  --affiner) AFFINER=1 ;;
  *) echo "option inconnue : $2 (attendu : --reprise, --reparer ou --affiner)" >&2; exit 2 ;;
esac

WRITER_TOOLS='Read,Edit,Write,Glob,Grep,Bash(python3 _tools/*),Bash(git diff*),Bash(git status*)'

abandon(){ # échec technique : rien à garder
  log "ABANDON : $1"
  git reset -q --hard "$BASE"
  git checkout -q main
  git branch -q -D "$BR" || true
  state bloque "$1"
  exit 1
}

a_revoir(){ # page non approuvée : le travail est gardé en PR brouillon, avec les remarques
  log "À REVOIR : $1"
  if git diff --quiet "$BASE" -- .; then abandon "$1 (aucune modification à garder)"; fi
  python3 "$P/pipeline.py" summary "$SLUG" > "$RUN/pr.md"
  git add -A  # runs/ et .claude/ exclus par .gitignore
  git commit -q -m "SEO $SLUG — À REVOIR : $1" \
    -m "Non approuvée par le circuit. Remarques du relecteur dans la PR brouillon."
  git push -q -u origin "$BR"
  PR_URL="$(gh pr create --draft --base main --head "$BR" \
    --title "[À REVOIR] SEO — $(python3 "$P/pipeline.py" field "$SLUG" url)" --body-file "$RUN/pr.md")"
  state a_revoir "$PR_URL"
  log "PR brouillon (non fusionnable en l'état) : $PR_URL"
  git checkout -q main
  exit 1
}

redacteur(){ # $1 = writer|fix|affine, $2 = numéro de passe
  log "rédacteur ($1, passe $2, $WRITER_MODEL)"
  claude -p "$(python3 "$P/pipeline.py" prompt "$1" "$SLUG")" \
    --model "$WRITER_MODEL" \
    --allowedTools "$WRITER_TOOLS" \
    --permission-mode acceptEdits \
    --max-turns 100 \
    --output-format json > "$RUN/writer_$2.json" || abandon "le rédacteur a échoué (passe $2)"
  [ -f "$RUN/writer_report.json" ] || abandon "pas de writer_report.json"
}

controles(){
  log "contrôles automatiques"
  if python3 "$P/checks.py" "$SLUG" --base "$BASE" > "$RUN/checks.json"; then CHECKS_OK=1; else CHECKS_OK=0; fi
}

relecteur(){ # $1 = numéro de passe
  git diff "$BASE" -- . ':(exclude)_tools/seo_pipeline/runs' > "$RUN/diff.patch"
  log "relecteur (passe $1, $REVIEWER_MODEL)"
  # shellcheck disable=SC2086
  claude -p "$(python3 "$P/pipeline.py" prompt review "$SLUG")" \
    --model "$REVIEWER_MODEL" \
    --allowedTools "Read,Glob,Grep" \
    --max-turns 40 \
    --output-format json ${REVIEWER_EXTRA_ARGS:-} > "$RUN/review_raw_$1.json" || abandon "le relecteur a échoué"
  VERDICT="$(python3 "$P/pipeline.py" extract-review "$SLUG" "$RUN/review_raw_$1.json")"
  log "verdict : $VERDICT — contrôles : $([ "$CHECKS_OK" = 1 ] && echo OK || echo ÉCHEC)"
}

archiver(){ # nouveau passage : les fichiers du passage précédent vont dans runs/<slug>/archive/
  local d f
  d="$RUN/archive/$(date +%Y%m%d-%H%M)"
  for f in "$RUN"/writer_*.json "$RUN"/writer_report.json "$RUN"/review_raw_*.json "$RUN"/review.json \
           "$RUN"/checks.json "$RUN"/score_*.json "$RUN"/diff.patch "$RUN"/pr.md; do
    [ -e "$f" ] || continue
    mkdir -p "$d"
    mv "$f" "$d/"
  done
}

if [ "$REPRISE" = 1 ]; then
  # Reprise d'un passage interrompu : on garde la branche et le travail en cours
  BR="$(git rev-parse --abbrev-ref HEAD)"
  case "$BR" in
    "seo/${SLUG}-"*) ;;
    *) log "reprise impossible : la branche courante ($BR) n'est pas seo/${SLUG}-…"; exit 2 ;;
  esac
  BASE="$(git rev-parse HEAD)"
  state en_cours "$BR (reprise)"
else
  # Départ propre depuis main à jour
  if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    log "arbre de travail modifié : arrêt (rien n'est touché)"; exit 2
  fi
  if [ "$REPARER" = 1 ] && { [ ! -s "$RUN/diff.patch" ] || [ ! -f "$RUN/review.json" ]; }; then
    log "réparation impossible : $RUN/diff.patch ou review.json absent"; exit 2
  fi
  # main local = GitHub, toujours (le VPS ne garde jamais de commit à lui sur main)
  git checkout -q main
  git fetch -q origin main
  git reset -q --hard origin/main
  BASE="$(git rev-parse HEAD)"
  if [ "$AFFINER" = 1 ]; then
    python3 "$P/pipeline.py" sync >/dev/null 2>&1 || true
    case "$(python3 "$P/pipeline.py" etat "$SLUG")" in
      pr_ouverte|a_revoir|en_cours)
        log "affinage reporté : une PR de cette page attend encore ta décision sur GitHub"; exit 2 ;;
    esac
    # Mesure gratuite AVANT de créer quoi que ce soit : rien à faire si la page est au vert
    python3 "$P/serp.py" guides "$SLUG" >> "$RUN/run.log" 2>&1 || { log "affinage impossible : guides indisponibles"; exit 2; }
    set +e
    python3 "$P/serp.py" verifier "$SLUG" >> "$RUN/run.log" 2>&1
    rc=$?
    set -e
    case "$rc" in
      0) python3 "$P/pipeline.py" controle "$SLUG" vert
         log "affinage inutile : la page atteint déjà ses seuils"; exit 3 ;;
      3) python3 "$P/pipeline.py" controle "$SLUG" a_affiner
         log "affinage : la page n'atteint pas ses seuils (détail dans ce journal)" ;;
      *) log "affinage impossible : mesure SERPmantics en erreur"; exit 2 ;;
    esac
  fi
  [ "$REPARER" = 1 ] || archiver
  BR="seo/${SLUG}-$(date +%Y%m%d-%H%M)"
  [ "$REPARER" = 1 ] && BR="${BR}-reparation"
  [ "$AFFINER" = 1 ] && BR="${BR}-affinage"
  git checkout -q -b "$BR"
  # si la page (ou son générateur) a changé depuis, on tente une fusion à 3 voies
  if [ "$REPARER" = 1 ] && ! git apply "$RUN/diff.patch" && ! git apply --3way "$RUN/diff.patch"; then
    git reset -q --hard "$BASE"; git checkout -q main; git branch -q -D "$BR" || true
    log "réparation impossible : la page a changé depuis, diff.patch ne s'applique plus"; exit 2
  fi
  state en_cours "$BR"
fi

if [ "$REPARER" = 1 ]; then
  log "réparation : dernière version écrite + remarques du relecteur ($(python3 "$P/pipeline.py" verdict "$SLUG"))"
  controles
  VERDICT=reviser  # au moins une passe de correction, même après un « rejeter »
  passe=0
elif [ "$REPRISE" = 1 ]; then
  passe="$(ls "$RUN"/writer_*.json 2>/dev/null | sed 's/.*writer_\([0-9]*\)\.json/\1/' | sort -n | tail -1)"
  passe="${passe:-0}"
  log "reprise après la passe $passe du rédacteur"
  controles
  relecteur "$passe"
elif [ "$AFFINER" = 1 ]; then
  redacteur affine 0
  controles
  relecteur 0
  passe=0
else
  log "guides SERPmantics (serp.py)"
  python3 "$P/serp.py" guides "$SLUG" >> "$RUN/run.log" 2>&1 || abandon "guides SERPmantics indisponibles"
  redacteur writer 0
  controles
  relecteur 0
  passe=0
fi
seuils_ok(){ # contrôle automatique des seuils après approbation (0 = atteints ou mesure indisponible)
  local rc
  set +e
  python3 "$P/serp.py" verifier "$SLUG" --label seuils > "$RUN/seuils.txt" 2>&1
  rc=$?
  set -e
  cat "$RUN/seuils.txt" >> "$RUN/run.log"
  [ "$rc" != 3 ]
}
while :; do
  if [ "$VERDICT" = "approuver" ] && [ "$CHECKS_OK" = 1 ]; then
    if seuils_ok; then break; fi
    if [ "$passe" -ge "$MAX_FIX" ]; then
      log "seuils SERPmantics pas encore atteints après $MAX_FIX corrections : texte approuvé publié, l'affinage de nuit reprendra"
      break
    fi
    log "approuvée par le relecteur, mais seuils SERPmantics non atteints : passe de correction"
    VERDICT="$(python3 "$P/pipeline.py" review-seuils "$SLUG")"
  fi
  [ "$VERDICT" = "rejeter" ] && a_revoir "rejetée par le relecteur"
  passe=$((passe + 1))
  [ "$passe" -gt "$MAX_FIX" ] && a_revoir "toujours pas approuvée après $MAX_FIX corrections"
  redacteur fix "$passe"
  controles
  relecteur "$passe"
done

# Publication : commit + PR
[ "$(git rev-parse --abbrev-ref HEAD)" = "$BR" ] || abandon "la branche a changé pendant le passage (autre processus sur le dépôt)"
python3 "$P/pipeline.py" summary "$SLUG" > "$RUN/pr.md"
git add -A  # runs/ et .claude/ exclus par .gitignore
QUOI="circuit SERPmantics + relecture"
[ "$AFFINER" = 1 ] && QUOI="affinage des scores SERPmantics + relecture"
git commit -q -m "SEO $SLUG : « $(python3 "$P/pipeline.py" field "$SLUG" requete) » ($QUOI)" \
  -m "Rédacteur $WRITER_MODEL, relecteur $REVIEWER_MODEL. Détails dans la PR."
git push -q -u origin "$BR"
TITRE="SEO — $(python3 "$P/pipeline.py" field "$SLUG" url)"
[ "$AFFINER" = 1 ] && TITRE="SEO (affinage) — $(python3 "$P/pipeline.py" field "$SLUG" url)"
if [ "$MODE" = "validation" ]; then TITRE="[À VALIDER] $TITRE"; fi
PR_URL="$(gh pr create --base main --head "$BR" --title "$TITRE" --body-file "$RUN/pr.md")"
log "PR ouverte : $PR_URL"

if [ "$MODE" = "auto" ] && [ "$AUTO_MERGE" = "1" ]; then
  if gh pr merge "$PR_URL" --squash --delete-branch; then
    state publie "$PR_URL"
    log "fusionnée : déploiement automatique en cours"
  else
    state pr_ouverte "$PR_URL"
    log "fusion automatique refusée par GitHub : la PR attend ton clic"
  fi
else
  state pr_ouverte "$PR_URL"
  log "en attente de ta validation sur GitHub"
fi
git checkout -q main
git fetch -q origin main && git reset -q --hard origin/main || true
}
main "$@"
