#!/bin/bash
# =============================================================================
# SLASHR Sales System — Sales Analyst Agent Runner
# Usage: ./scripts/run_sales_analyst.sh <dossier_r1_file> [prospect_domain]
#
# Arguments:
#   dossier_r1_file  : Fichier texte contenant le dossier R1 (transcript, notes, etc.)
#   prospect_domain  : (optionnel) Domaine du prospect pour enrichissement DataForSEO
#
# Output:
#   - Brief R1 en markdown dans outputs/
#   - Brief R1 en JSON dans outputs/
#
# Requires:
#   - ANTHROPIC_API_KEY (env var)
#   - DATAFORSEO_LOGIN + DATAFORSEO_PASSWORD (env vars, optionnel)
#   - jq, curl
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SYSTEM_PROMPT_FILE="$PROJECT_DIR/prompts/sales_analyst_system.md"
OUTPUTS_DIR="$PROJECT_DIR/outputs"

# --- Couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- Validation ---
if [ $# -lt 1 ]; then
    echo -e "${RED}Usage: $0 <dossier_r1_file> [prospect_domain]${NC}"
    echo ""
    echo "  dossier_r1_file : Fichier texte du dossier R1"
    echo "  prospect_domain : Domaine prospect pour DataForSEO (optionnel)"
    echo ""
    echo "Exemples:"
    echo "  $0 inputs/dossier_r1_decathlon.txt decathlonfitnessclub.fr"
    echo "  $0 inputs/notes_call_prospect.txt"
    exit 1
fi

DOSSIER_FILE="$1"
PROSPECT_DOMAIN="${2:-}"

if [ ! -f "$DOSSIER_FILE" ]; then
    echo -e "${RED}Erreur: Fichier introuvable: $DOSSIER_FILE${NC}"
    exit 1
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo -e "${RED}Erreur: ANTHROPIC_API_KEY non définie${NC}"
    echo "export ANTHROPIC_API_KEY=sk-ant-..."
    exit 1
fi

if [ ! -f "$SYSTEM_PROMPT_FILE" ]; then
    echo -e "${RED}Erreur: System prompt introuvable: $SYSTEM_PROMPT_FILE${NC}"
    exit 1
fi

# --- Enrichissement DataForSEO (si domaine fourni) ---
DATAFORSEO_CONTEXT=""

if [ -n "$PROSPECT_DOMAIN" ] && [ -n "${DATAFORSEO_LOGIN:-}" ] && [ -n "${DATAFORSEO_PASSWORD:-}" ]; then
    echo -e "${BLUE}[DataForSEO] Enrichissement domaine: $PROSPECT_DOMAIN${NC}"

    # Domain rank overview
    DOMAIN_DATA=$(curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live" \
        -u "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" \
        -H "Content-Type: application/json" \
        -d "[{\"target\": \"$PROSPECT_DOMAIN\", \"language_code\": \"fr\", \"location_name\": \"France\"}]" 2>/dev/null || echo "")

    # Ranked keywords (top 20)
    KEYWORDS_DATA=$(curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live" \
        -u "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" \
        -H "Content-Type: application/json" \
        -d "[{\"target\": \"$PROSPECT_DOMAIN\", \"language_code\": \"fr\", \"location_name\": \"France\", \"limit\": 20, \"order_by\": [\"ranked_serp_element.serp_item.rank_group,asc\"]}]" 2>/dev/null || echo "")

    # Competitors
    COMPETITORS_DATA=$(curl -s -X POST "https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live" \
        -u "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" \
        -H "Content-Type: application/json" \
        -d "[{\"target\": \"$PROSPECT_DOMAIN\", \"language_code\": \"fr\", \"location_name\": \"France\", \"limit\": 5}]" 2>/dev/null || echo "")

    if [ -n "$DOMAIN_DATA" ]; then
        DATAFORSEO_CONTEXT="

--- DONNÉES DATAFORSEO ---

Domaine analysé: $PROSPECT_DOMAIN

Domain Rank Overview:
$DOMAIN_DATA

Top 20 Keywords:
$KEYWORDS_DATA

Top 5 Competitors:
$COMPETITORS_DATA

--- FIN DONNÉES DATAFORSEO ---"
        echo -e "${GREEN}[DataForSEO] Enrichissement OK${NC}"
    else
        echo -e "${YELLOW}[DataForSEO] Pas de données récupérées — le brief sera sans enrichissement${NC}"
    fi
elif [ -n "$PROSPECT_DOMAIN" ]; then
    echo -e "${YELLOW}[DataForSEO] Credentials manquants (DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD)${NC}"
    echo -e "${YELLOW}[DataForSEO] Le brief sera généré sans enrichissement data${NC}"
fi

# --- Lecture des fichiers ---
echo -e "${BLUE}[Sales Analyst] Lecture du dossier R1...${NC}"
DOSSIER_CONTENT=$(cat "$DOSSIER_FILE")
SYSTEM_PROMPT=$(cat "$SYSTEM_PROMPT_FILE")

# --- Construction du message utilisateur ---
USER_MESSAGE="## DOSSIER R1

$DOSSIER_CONTENT
$DATAFORSEO_CONTEXT

---

Analyse ce dossier R1 et produis le brief stratégique complet selon le format imposé.
Date du jour : $(date +%Y-%m-%d)"

# --- Appel API Claude ---
echo -e "${BLUE}[Sales Analyst] Appel Claude API (claude-sonnet-4-20250514)...${NC}"

# Escape pour JSON
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
BRIEF_CONTENT=$(echo "$RESPONSE" | python3 -c "
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
    echo -e "${RED}$BRIEF_CONTENT${NC}"
    exit 1
fi

# --- Extraction du nom d'entreprise pour le filename ---
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
OUTPUT_FILE="$OUTPUTS_DIR/R1-${DATE_STAMP}-${ENTREPRISE_SLUG}.md"

# --- Sauvegarde ---
echo "$BRIEF_CONTENT" > "$OUTPUT_FILE"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} Brief R1 généré avec succès${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "  Fichier : ${BLUE}$OUTPUT_FILE${NC}"
echo -e "  Entreprise : ${BLUE}$ENTREPRISE_SLUG${NC}"
echo ""
echo -e "${YELLOW}[RAPPEL] Ce brief est un DRAFT — le closer doit valider avant tout usage.${NC}"
echo ""
