#!/bin/bash
# =============================================================================
# SLASHR Sales System — Deal Analyst Agent Runner (v2.1)
# Agent fusionné : Sales Analyst + Closing Coach → un seul appel, un seul output
#
# Usage:
#   ./scripts/run_deal_analyst.sh analyse <dossier_r1> [prospect_domain]
#   ./scripts/run_deal_analyst.sh relances <deal_file>
#
# Arguments:
#   mode             : analyse | relances
#   dossier_r1       : Fichier OU dossier contenant les sources R1
#                      - Si fichier (.txt, .md) : utilisé tel quel
#                      - Si dossier : tous les fichiers sont concaténés avec marqueurs
#   prospect_domain  : (optionnel) Domaine prospect pour enrichissement DataForSEO
#   deal_file        : Fichier DEAL-*.md (output du mode analyse)
#
# Structure dossier attendue (mode analyse avec dossier) :
#   inputs/prospect-name/
#   ├── transcript_r1.txt          → type auto-détecté : transcript
#   ├── notes_closer.txt           → type auto-détecté : notes_closer
#   ├── cdc_prospect.pdf           → type auto-détecté : document_prospect
#   ├── email_prospect.txt         → type auto-détecté : email_prospect
#   └── brief_prospect.md          → type auto-détecté : document_prospect
#
# Convention de nommage (préfixes reconnus) :
#   transcript*  → transcript
#   notes*       → notes_closer
#   cdc* | cahier* | brief* | rfp* | spec* → document_prospect
#   email* | mail* → email_prospect
#   Autre        → document (type générique)
#
# Output:
#   - Mode analyse  : outputs/DEAL-{YYYYMMDD}-{entreprise-slug}.md
#   - Mode relances : outputs/RELANCES-{YYYYMMDD}-{entreprise-slug}.md
#
# Requires:
#   - ANTHROPIC_API_KEY (env var)
#   - DATAFORSEO_LOGIN + DATAFORSEO_PASSWORD (env vars, optionnel pour enrichissement)
#   - python3, curl
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SYSTEM_PROMPT_FILE="$PROJECT_DIR/prompts/deal_analyst_system.md"
OUTPUTS_DIR="$PROJECT_DIR/outputs"

# --- Couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- Fonction : détecter le type de source par nom de fichier ---
detect_source_type() {
    local filename
    filename=$(basename "$1" | tr '[:upper:]' '[:lower:]')

    case "$filename" in
        transcript*) echo "transcript" ;;
        notes*)      echo "notes_closer" ;;
        cdc*|cahier*|brief*|rfp*|spec*) echo "document_prospect" ;;
        email*|mail*) echo "email_prospect" ;;
        *)           echo "document" ;;
    esac
}

# --- Fonction : concaténer un dossier multi-fichiers ---
concat_directory() {
    local dir="$1"
    local result=""
    local file_count=0

    # Trier par type : transcript d'abord, puis notes, puis docs, puis emails
    for priority in "transcript" "notes" "cdc cahier brief rfp spec" "email mail"; do
        for file in "$dir"/*; do
            [ -f "$file" ] || continue
            local basename_lower
            basename_lower=$(basename "$file" | tr '[:upper:]' '[:lower:]')

            local match=false
            for prefix in $priority; do
                if [[ "$basename_lower" == ${prefix}* ]]; then
                    match=true
                    break
                fi
            done

            if [ "$match" = true ]; then
                local source_type
                source_type=$(detect_source_type "$file")
                local basename_file
                basename_file=$(basename "$file")

                result+="
=== SOURCE: ${basename_file} (type: ${source_type}) ===

$(cat "$file")

=== FIN SOURCE: ${basename_file} ===

"
                file_count=$((file_count + 1))
                echo -e "  ${GREEN}✓${NC} ${basename_file} → ${BLUE}${source_type}${NC}" >&2
            fi
        done
    done

    # Fichiers restants (pas matchés par les patterns de priorité)
    for file in "$dir"/*; do
        [ -f "$file" ] || continue
        local basename_lower
        basename_lower=$(basename "$file" | tr '[:upper:]' '[:lower:]')

        local already_matched=false
        for prefix in transcript notes cdc cahier brief rfp spec email mail; do
            if [[ "$basename_lower" == ${prefix}* ]]; then
                already_matched=true
                break
            fi
        done

        if [ "$already_matched" = false ]; then
            local source_type
            source_type=$(detect_source_type "$file")
            local basename_file
            basename_file=$(basename "$file")

            result+="
=== SOURCE: ${basename_file} (type: ${source_type}) ===

$(cat "$file")

=== FIN SOURCE: ${basename_file} ===

"
            file_count=$((file_count + 1))
            echo -e "  ${GREEN}✓${NC} ${basename_file} → ${BLUE}${source_type}${NC}" >&2
        fi
    done

    if [ "$file_count" -eq 0 ]; then
        echo -e "${RED}Erreur: Aucun fichier trouvé dans $dir${NC}" >&2
        exit 1
    fi

    echo -e "${GREEN}[Sources] ${file_count} fichier(s) chargé(s)${NC}" >&2
    echo "$result"
}

# --- Validation ---
if [ $# -lt 2 ]; then
    echo -e "${RED}Usage:${NC}"
    echo "  $0 analyse <dossier_ou_fichier_r1> [prospect_domain]"
    echo "  $0 relances <deal_file>"
    echo ""
    echo "Exemples:"
    echo "  $0 analyse inputs/decathlon-fitness-club/ decathlonfitnessclub.fr"
    echo "  $0 analyse inputs/transcript_prospect.txt domaine.fr"
    echo "  $0 relances outputs/DEAL-20260216-decathlon-fitness-club.md"
    exit 1
fi

MODE="$1"
INPUT_PATH="$2"
PROSPECT_DOMAIN="${3:-}"

if [[ "$MODE" != "analyse" && "$MODE" != "relances" ]]; then
    echo -e "${RED}Erreur: Mode invalide '$MODE'. Utilise: analyse | relances${NC}"
    exit 1
fi

if [ ! -e "$INPUT_PATH" ]; then
    echo -e "${RED}Erreur: Chemin introuvable: $INPUT_PATH${NC}"
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

# --- Lecture de l'input (fichier unique OU dossier multi-fichiers) ---
echo -e "${BLUE}[Deal Analyst] Mode: $MODE${NC}"

if [ -d "$INPUT_PATH" ]; then
    echo -e "${BLUE}[Sources] Dossier détecté: $INPUT_PATH${NC}"
    echo -e "${BLUE}[Sources] Concaténation des fichiers avec détection de type...${NC}"
    INPUT_CONTENT=$(concat_directory "$INPUT_PATH")
elif [ -f "$INPUT_PATH" ]; then
    local_type=$(detect_source_type "$INPUT_PATH")
    local_basename=$(basename "$INPUT_PATH")
    echo -e "${BLUE}[Sources] Fichier unique: $local_basename → ${local_type}${NC}"
    INPUT_CONTENT="=== SOURCE: ${local_basename} (type: ${local_type}) ===

$(cat "$INPUT_PATH")

=== FIN SOURCE: ${local_basename} ==="
fi

# --- Enrichissement DataForSEO (mode analyse uniquement, si domaine fourni) ---
DATAFORSEO_CONTEXT=""

if [[ "$MODE" == "analyse" ]] && [ -n "$PROSPECT_DOMAIN" ] && [ -n "${DATAFORSEO_LOGIN:-}" ] && [ -n "${DATAFORSEO_PASSWORD:-}" ]; then
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
        echo -e "${YELLOW}[DataForSEO] Pas de données récupérées — le dossier sera sans enrichissement${NC}"
    fi
elif [[ "$MODE" == "analyse" ]] && [ -n "$PROSPECT_DOMAIN" ]; then
    echo -e "${YELLOW}[DataForSEO] Credentials manquants (DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD)${NC}"
    echo -e "${YELLOW}[DataForSEO] Le dossier sera généré sans enrichissement data${NC}"
fi

# --- Lecture du system prompt ---
SYSTEM_PROMPT=$(cat "$SYSTEM_PROMPT_FILE")

# --- Construction du message selon le mode ---
case "$MODE" in
    analyse)
        USER_MESSAGE="## DOSSIER R1

$INPUT_CONTENT
$DATAFORSEO_CONTEXT

---

**Mode : ANALYSE**

Analyse ce dossier R1 et produis le dossier deal complet :
- Passe 1 : Brief stratégique scoré (Partie A — Sections 1 à 6)
- Passe 2 : Pack R2 si verdict R2_GO ou R2_CONDITIONAL (Partie B — Sections 7 à 12)

Date du jour : $(date +%Y-%m-%d)"
        OUTPUT_PREFIX="DEAL"
        MAX_TOKENS=12000
        ;;
    relances)
        USER_MESSAGE="## DOSSIER DEAL — CONTEXTE PROSPECT

$INPUT_CONTENT

---

**Mode : RELANCES POST-R2**

La R2 est terminée. Pas de signature après 48h. Génère les 3 emails de relance personnalisés :
- Touch 1 (J+5) : L'insight — data nouvelle
- Touch 2 (J+12) : L'urgence douce — élément temporel
- Touch 3 (J+20) : Le closer — direct et final

Chaque email doit être prêt à être collé dans Gmail comme brouillon. Variables toutes remplies.

Date du jour : $(date +%Y-%m-%d)"
        OUTPUT_PREFIX="RELANCES"
        MAX_TOKENS=4096
        ;;
esac

# --- Appel API Claude ---
echo -e "${BLUE}[Deal Analyst] Appel Claude API (claude-sonnet-4-20250514)...${NC}"

SYSTEM_ESCAPED=$(echo "$SYSTEM_PROMPT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
USER_ESCAPED=$(echo "$USER_MESSAGE" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

RESPONSE=$(curl -s -X POST "https://api.anthropic.com/v1/messages" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d "{
        \"model\": \"claude-sonnet-4-20250514\",
        \"max_tokens\": $MAX_TOKENS,
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
ENTREPRISE_SLUG=$(echo "$OUTPUT_CONTENT" | python3 -c "
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
echo -e "${GREEN} ${OUTPUT_PREFIX} généré avec succès${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "  Fichier : ${BLUE}$OUTPUT_FILE${NC}"
echo -e "  Mode    : ${BLUE}$MODE${NC}"
echo ""

case "$MODE" in
    analyse)
        echo -e "${YELLOW}[RAPPEL] Ce dossier est un DRAFT — le closer doit valider avant tout usage.${NC}"
        if echo "$OUTPUT_CONTENT" | grep -q "PARTIE B"; then
            echo -e "${GREEN}[INFO] Le dossier contient le brief + le pack R2 (verdict R2_GO ou R2_CONDITIONAL).${NC}"
        else
            echo -e "${YELLOW}[INFO] Le dossier contient uniquement le brief (verdict NURTURE — pas de pack R2).${NC}"
        fi
        ;;
    relances)
        echo -e "${YELLOW}[RAPPEL] Ces emails sont des BROUILLONS — le closer relit et envoie manuellement.${NC}"
        ;;
esac
echo ""
