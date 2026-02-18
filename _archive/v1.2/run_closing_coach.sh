#!/bin/bash
# =============================================================================
# SLASHR Sales System — Closing Coach Agent Runner
# Usage:
#   ./scripts/run_closing_coach.sh pack <brief_r1_file>
#   ./scripts/run_closing_coach.sh relances <brief_r1_file>
#   ./scripts/run_closing_coach.sh challenge <brief_r1_file> "<motif>"
#
# Arguments:
#   mode           : pack | relances | challenge
#   brief_r1_file  : Fichier brief R1 (output du Sales Analyst)
#   motif          : (pour challenge) Motif du challenge
#
# Requires:
#   - ANTHROPIC_API_KEY (env var)
#   - jq, curl
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SYSTEM_PROMPT_FILE="$PROJECT_DIR/prompts/closing_coach_system.md"
OUTPUTS_DIR="$PROJECT_DIR/outputs"

# --- Couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- Validation ---
if [ $# -lt 2 ]; then
    echo -e "${RED}Usage:${NC}"
    echo "  $0 pack <brief_r1_file>"
    echo "  $0 relances <brief_r1_file>"
    echo "  $0 challenge <brief_r1_file> \"<motif>\""
    echo ""
    echo "Exemples:"
    echo "  $0 pack outputs/R1-20260130-decathlon-fitness-club.md"
    echo "  $0 relances outputs/R1-20260130-decathlon-fitness-club.md"
    echo "  $0 challenge outputs/R1-20260130-decathlon-fitness-club.md \"Budget scoré 20/20 mais partagé avec dev\""
    exit 1
fi

MODE="$1"
BRIEF_FILE="$2"
CHALLENGE_MOTIF="${3:-}"

if [[ "$MODE" != "pack" && "$MODE" != "relances" && "$MODE" != "challenge" ]]; then
    echo -e "${RED}Erreur: Mode invalide '$MODE'. Utilise: pack | relances | challenge${NC}"
    exit 1
fi

if [ ! -f "$BRIEF_FILE" ]; then
    echo -e "${RED}Erreur: Brief introuvable: $BRIEF_FILE${NC}"
    exit 1
fi

if [[ "$MODE" == "challenge" && -z "$CHALLENGE_MOTIF" ]]; then
    echo -e "${RED}Erreur: Le mode challenge nécessite un motif${NC}"
    echo "  $0 challenge <brief_file> \"motif du challenge\""
    exit 1
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo -e "${RED}Erreur: ANTHROPIC_API_KEY non définie${NC}"
    exit 1
fi

if [ ! -f "$SYSTEM_PROMPT_FILE" ]; then
    echo -e "${RED}Erreur: System prompt introuvable: $SYSTEM_PROMPT_FILE${NC}"
    exit 1
fi

# --- Lecture des fichiers ---
echo -e "${BLUE}[Closing Coach] Mode: $MODE${NC}"
echo -e "${BLUE}[Closing Coach] Lecture du brief R1...${NC}"

BRIEF_CONTENT=$(cat "$BRIEF_FILE")
SYSTEM_PROMPT=$(cat "$SYSTEM_PROMPT_FILE")

# --- Construction du message selon le mode ---
case "$MODE" in
    pack)
        USER_MESSAGE="## BRIEF R1 À TRAITER

$BRIEF_CONTENT

---

**Mode : PACK R2**

Génère le pack complet de préparation R2 :
1. D'abord, valide le brief (checklist complète). Si incohérence → CHALLENGE.
2. Si brief OK → génère : objections probables, script de fin R2, données ammunition, ROI projeté, pre-R2 checklist.

Date du jour : $(date +%Y-%m-%d)"
        OUTPUT_PREFIX="R2-PACK"
        ;;
    relances)
        USER_MESSAGE="## BRIEF R1 — CONTEXTE PROSPECT

$BRIEF_CONTENT

---

**Mode : RELANCES POST-R2**

La R2 est terminée. Pas de signature après 48h. Génère les 3 emails de relance personnalisés :
- Touch 1 (J+5) : L'insight — data nouvelle
- Touch 2 (J+12) : L'urgence douce — élément temporel
- Touch 3 (J+20) : Le closer — direct et final

Chaque email doit être prêt à être collé dans Gmail comme brouillon. Variables toutes remplies.

Date du jour : $(date +%Y-%m-%d)"
        OUTPUT_PREFIX="RELANCES"
        ;;
    challenge)
        USER_MESSAGE="## BRIEF R1 CONTESTÉ

$BRIEF_CONTENT

---

**Mode : CHALLENGE**

Motif du challenge : $CHALLENGE_MOTIF

Analyse le brief, identifie les incohérences mentionnées, et produis :
1. Le JSON de challenge structuré
2. Les corrections recommandées
3. L'impact sur le score et le verdict

Date du jour : $(date +%Y-%m-%d)"
        OUTPUT_PREFIX="CHALLENGE"
        ;;
esac

# --- Appel API Claude ---
echo -e "${BLUE}[Closing Coach] Appel Claude API (claude-sonnet-4-20250514)...${NC}"

SYSTEM_ESCAPED=$(echo "$SYSTEM_PROMPT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
USER_ESCAPED=$(echo "$USER_MESSAGE" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

RESPONSE=$(curl -s -X POST "https://api.anthropic.com/v1/messages" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d "{
        \"model\": \"claude-sonnet-4-20250514\",
        \"max_tokens\": 8192,
        \"system\": $SYSTEM_ESCAPED,
        \"messages\": [{\"role\": \"user\", \"content\": $USER_ESCAPED}]
    }")

# --- Extraction du résultat ---
OUTPUT_CONTENT=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'content' in data and len(data['content']) > 0:
        print(data['content'][0]['text'])
    elif 'error' in data:
        print(f\"ERREUR API: {data['error']['message']}\")
        sys.exit(1)
    else:
        print('ERREUR: Réponse inattendue')
        sys.exit(1)
except Exception as e:
    print(f'ERREUR: {e}')
    sys.exit(1)
")

if [ $? -ne 0 ]; then
    echo -e "${RED}$OUTPUT_CONTENT${NC}"
    exit 1
fi

# --- Extraction du nom d'entreprise ---
ENTREPRISE_SLUG=$(echo "$BRIEF_CONTENT" | python3 -c "
import sys, re
content = sys.stdin.read()
match = re.search(r'Entreprise\s*\|\s*(.+)', content)
if match:
    name = match.group(1).strip()
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    print(slug)
else:
    print('unknown')
" 2>/dev/null || echo "unknown")

DATE_STAMP=$(date +%Y%m%d)
OUTPUT_FILE="$OUTPUTS_DIR/${OUTPUT_PREFIX}-${DATE_STAMP}-${ENTREPRISE_SLUG}.md"

# --- Sauvegarde ---
echo "$OUTPUT_CONTENT" > "$OUTPUT_FILE"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} $OUTPUT_PREFIX généré avec succès${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "  Fichier : ${BLUE}$OUTPUT_FILE${NC}"
echo -e "  Mode    : ${BLUE}$MODE${NC}"
echo ""

case "$MODE" in
    pack)
        echo -e "${YELLOW}[RAPPEL] Ce pack est un DRAFT — usage interne uniquement.${NC}"
        ;;
    relances)
        echo -e "${YELLOW}[RAPPEL] Ces emails sont des BROUILLONS — le closer relit et envoie manuellement.${NC}"
        ;;
    challenge)
        echo -e "${YELLOW}[RAPPEL] Le brief challengé doit être renvoyé au Sales Analyst pour correction.${NC}"
        ;;
esac
echo ""
