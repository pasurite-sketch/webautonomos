#!/usr/bin/env bash
# Traite UNE page : rédacteur → contrôles → relecteur (→ correction) → PR GitHub.
# Usage : bash _tools/seo_pipeline/run_page.sh <slug> [--reprise]
#   --reprise : reprend un passage interrompu sur sa branche seo/<slug>-… (contrôles, relecture, suite)
# Variables (fichier ~/.seo_pipeline.env) :
#   ANTHROPIC_API_KEY, SERPMANTICS_API_KEY   (obligatoires)
#   WRITER_MODEL   (défaut claude-sonnet-5)   REVIEWER_MODEL (défaut claude-opus-5-5)
#   REVIEWER_EXTRA_ARGS  (ex. réglage d'effort, voir INSTALL_VPS.md)
#   MAX_FIX=2      nombre maximal de corrections après relecture
#   AUTO_MERGE=0   1 = fusion automatique des pages mode "auto" approuvées
set -euo pipefail
SLUG="${1:?usage: run_page.sh <slug>}"
REPO="$(git rev-parse --show-toplevel)"
cd "$REPO"
P="_tools/seo_pipeline"
[ -f "$HOME/.seo_pipeline.env" ] && set -a && . "$HOME/.seo_pipeline.env" && set +a
: "${ANTHROPIC_API_KEY:?ANTHROPIC_API_KEY manquante}"
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
[ "${2:-}" = "--reprise" ] && REPRISE=1
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
  git checkout -q main
  git pull -q --ff-only
  BASE="$(git rev-parse HEAD)"
  BR="seo/${SLUG}-$(date +%Y%m%d-%H%M)"
  git checkout -q -b "$BR"
  state en_cours "$BR"
fi

WRITER_TOOLS='Read,Edit,Write,Glob,Grep,Bash(python3 _tools/*),Bash(git diff*),Bash(git status*)'
abandon(){
  log "ABANDON : $1"
  git reset -q --hard "$BASE"
  git checkout -q main
  git branch -q -D "$BR" || true
  state bloque "$1"
  exit 1
}

redacteur(){ # $1 = writer|fix, $2 = numéro de passe
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

if [ "$REPRISE" = 1 ]; then
  passe="$(ls "$RUN"/writer_*.json 2>/dev/null | sed 's/.*writer_\([0-9]*\)\.json/\1/' | sort -n | tail -1)"
  passe="${passe:-0}"
  log "reprise après la passe $passe du rédacteur"
  controles
  relecteur "$passe"
else
  log "guides SERPmantics (serp.py)"
  python3 "$P/serp.py" guides "$SLUG" >> "$RUN/run.log" 2>&1 || abandon "guides SERPmantics indisponibles"
  redacteur writer 0
  controles
  relecteur 0
  passe=0
fi
while :; do
  if [ "$VERDICT" = "approuver" ] && [ "$CHECKS_OK" = 1 ]; then break; fi
  [ "$VERDICT" = "rejeter" ] && abandon "rejetée par le relecteur (voir $RUN/review.json)"
  passe=$((passe + 1))
  [ "$passe" -gt "$MAX_FIX" ] && abandon "toujours pas approuvée après $MAX_FIX corrections"
  redacteur fix "$passe"
  controles
  relecteur "$passe"
done

# Publication : commit + PR
python3 "$P/pipeline.py" summary "$SLUG" > "$RUN/pr.md"
git add -A  # runs/ et .claude/ exclus par .gitignore
git commit -q -m "SEO $SLUG : « $(python3 "$P/pipeline.py" field "$SLUG" requete) » (circuit SERPmantics + relecture)" \
  -m "Rédacteur $WRITER_MODEL, relecteur $REVIEWER_MODEL. Détails dans la PR."
git push -q -u origin "$BR"
TITRE="SEO — $(python3 "$P/pipeline.py" field "$SLUG" url)"
if [ "$MODE" = "validation" ]; then TITRE="[À VALIDER] $TITRE"; fi
PR_URL="$(gh pr create --base main --head "$BR" --title "$TITRE" --body-file "$RUN/pr.md")"
log "PR ouverte : $PR_URL"

if [ "$MODE" = "auto" ] && [ "$AUTO_MERGE" = "1" ]; then
  gh pr merge "$PR_URL" --squash --delete-branch
  state publie "$PR_URL"
  log "fusionnée : déploiement automatique en cours"
else
  state pr_ouverte "$PR_URL"
  log "en attente de ta validation sur GitHub"
fi
git checkout -q main
git pull -q --ff-only || true
