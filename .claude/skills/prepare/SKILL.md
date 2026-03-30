---
name: prepare
description: Genere la proposition HTML interactive sur-mesure — 3 passes internes (Data & Strategy, Narrative, Design), 4 onglets (Diagnostic, Strategie, Investissement, Cas clients), uploadee dans Drive.
disable-model-invocation: true
---

# PREPARE — Proposition HTML interactive

**Arguments :** $ARGUMENTS

## Parsing des arguments

Extraire du `$ARGUMENTS` :
- `deal_id` : le premier token numerique
- `--fast` : flag optionnel (re-run rapide, skip Pass 1 si SDB frais)
- `--fresh` : flag optionnel (force re-collecte, ignore le cache)

Exemples : `/prepare 560`, `/prepare 560 --fast`, `/prepare 560 --fresh`

## Mode --fast (re-run rapide)

Si `--fast` est present :
1. Verifier l'existence de `.cache/deals/{deal_id}/artifacts/SDB.md`
2. Lire la premiere ligne du SDB — chercher `GENERATED_AT: {ISO timestamp}`
3. Si SDB existe ET age < 2h → **SKIP Pass 1 entiere**, passer directement a Pass 2
4. Si SDB absent OU age >= 2h → ignorer `--fast`, executer normalement (afficher : "SDB absent ou trop ancien ({age}), execution normale.")

Le mode `--fast` est concu pour les re-runs : "refais la presentation avec un angle different", "change le scenario recommande", etc. Les donnees sont encore fraiches, seul l'angle narratif change.

## Prerequis

Aucun prerequis de scoring. Le closer decide quand lancer /prepare.

## Etape 0 — Verification prerequis (OBLIGATOIRE avant toute collecte)

### 0a. Synchro docs de marque
```bash
python3 tools/sync_brand_docs.py
```
Met a jour `context/brand_platform.md` et `context/tone_of_voice.md` si le cache a expire (> 7 jours). Silencieux si les docs sont frais.

### 0b. Verifier le deal
```bash
TOKEN=$(cat ~/.pipedrive_token)
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN"
```

Checker dans la reponse :
1. **Deal existe** : si 404 → STOP : "Ce deal n'existe pas dans Pipedrive."
2. **`dossier_r1_link` (field `1fd2ec1073fa60e11fb59bddfec7a2f6656c4b0c`)** : si absent → AVERTISSEMENT : "Pas de dossier Drive renseigne. La collecte Drive sera ignoree." Continuer sans le module Drive.
3. **Audit disponible** : si `.cache/deals/{deal_id}/audit.md` existe, le lire pour enrichir l'analyse (donnees deja collectees reutilisables).

Si les checks passent → continuer avec les etapes suivantes.

## Checklist de lecture (OBLIGATOIRE — tout lire AVANT de commencer)

L'agent DOIT lire ces fichiers avant de commencer. Ne pas lire un fichier = ne pas connaitre la regle = generer un output non conforme.

| # | Fichier | Contenu | Quand |
|---|---------|---------|-------|
| 1 | `agents/prepare-context.md` | **Bundle compact** : role, regles, positionnement, pricing, output contract, validation, performance budget | Avant tout |
| 2 | `agents/prepare.md` | Routeur — architecture 3 passes | Avant tout |
| 3 | `context/design_system.md` | Couleurs, typo, gradients, espacements | Avant Pass 3 |
| 4 | `context/case_studies.md` | Bibliotheque cas clients | Avant Pass 2 |
| 5 | `context/proposal-kit-reference.md` | Aide-memoire classes CSS condensees | Avant Pass 3 |

> Les fichiers originaux (shared.md, positioning.md, pricing_rules.md, output_contract.md, validation_rules.md, performance_budget.md) restent la reference complete si un detail manque dans le bundle.

## Etapes

1. Lis les fichiers 1-2 de la checklist ci-dessus
2. Execute les 3 passes avec les 2 checkpoints interactifs :
   - **Pass 1** : lis `agents/prepare-pass1.md` et execute (collecte + diagnostic strategique + SDB). En mode `--fast`, skip cette passe si SDB frais (< 2h).
   - **CHECKPOINT 1** : presente le resume strategique au closer dans le terminal (cf. `agents/prepare.md`). **ATTENDRE la validation** avant de continuer. Si corrections → mettre a jour le SDB.
   - **Pass 2** : lis fichiers 3-4, puis `agents/prepare-pass2.md` et execute (arc narratif + NBP). Lire aussi `agents/prepare-pass2-onglet4.md` pour l'onglet Investissement.
   - **CHECKPOINT 2** : presente le plan narratif au closer dans le terminal (cf. `agents/prepare.md`). **ATTENDRE la validation** avant de continuer. Si modifications → mettre a jour le NBP.
   - **Pass 3** : lis fichier 5, puis `agents/prepare-pass3.md` et execute (HTML + validation + `tools/validate_proposal.py`). Le diagnostic interne ne doit JAMAIS apparaitre dans le HTML client (regle 20).

## Collecte Pipedrive

```bash
TOKEN=$(cat ~/.pipedrive_token)

# Deal
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN"

# Contact
curl -s "https://api.pipedrive.com/v1/persons/{person_id}?api_token=$TOKEN"

# Organisation
curl -s "https://api.pipedrive.com/v1/organizations/{org_id}?api_token=$TOKEN"

# Notes
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}/notes?api_token=$TOKEN"

# Activites
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}/activities?api_token=$TOKEN"

# Emails — filtrer par deal_id cote client
curl -s "https://api.pipedrive.com/v1/mailbox/mailThreads?folder=inbox&api_token=$TOKEN"
curl -s "https://api.pipedrive.com/v1/mailbox/mailThreads?folder=sent&api_token=$TOKEN"
curl -s "https://api.pipedrive.com/v1/mailbox/mailThreads/{thread_id}/mailMessages?api_token=$TOKEN"
```

## Collecte Drive

Le champ `dossier_r1_link` du deal contient l'URL du dossier. Extraire le folder ID, lister et telecharger les fichiers via l'API Google Drive (credentials : `~/.google_service_account.json`).

## Reference

- Field keys Pipedrive : `context/pipedrive_reference.md`
- Kit composants (30 composants, catalogue par role narratif) : `templates/proposal-kit.html`
- Squelette HTML (CSS + JS + nav, boilerplate) : `templates/proposal-skeleton.html`
- Assembleur HTML : `tools/build_proposal.py`
- Design system : `context/design_system.md`
- Positionnement + structure offre : `context/positioning.md`
- Cas clients : `context/case_studies.md`

## Output

2 fichiers uploades dans le dossier Drive du deal :

| Fichier | Audience | Contenu |
|---------|----------|---------|
| `PROPOSAL-{YYYYMMDD}-{entreprise-slug}.html` | **Prospect** (via closer) | Proposition HTML interactive — 4 onglets (Diagnostic, Strategie, Investissement, Cas clients) |
| `INTERNAL-DIAG-{YYYYMMDD}-{entreprise-slug}.md` | **Interne seulement** | Diagnostic complet (contrainte, leviers, confiance, ROI, resume decisionnel, evidence log) |

> Le prefixe `INTERNAL-` garantit que le fichier est exclu des outputs prospect (cf. Module 2 : exclure `DEAL-*`, `DECK-*`, `PROPOSAL-*`, `INTERNAL-*`).

Apres upload, mettre a jour `r2_pack_link` dans Pipedrive avec l'URL Drive du fichier PROPOSAL (cf. `context/pipedrive_reference.md`).

Message de fin :
```
Proposition generee : PROPOSAL-{date}-{slug}.html
Diagnostic interne : INTERNAL-DIAG-{date}-{slug}.md
Uploades dans le dossier Drive du deal.

Arc narratif : [description en 1 ligne de l'arc choisi et pourquoi]
Diagnostic : contrainte = {description} | leviers = {2-3 leviers} | insight = {1 phrase}
4-6 onglets : Diagnostic ({N} sections) | Strategie (decision + 90j + ROI) | Investissement | Cas clients ({N} cas)

DRAFT — a valider avant partage avec le prospect.
Ouvre le fichier HTML dans un navigateur pour preview.
```
