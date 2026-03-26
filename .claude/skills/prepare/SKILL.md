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

Le deal doit avoir ete qualifie (`/qualify`). Score >= 60 (GO) ou CONDITIONNEL valide par le manager.

## Etape 0 — Verification prerequis (OBLIGATOIRE avant toute collecte)

Avant de lancer la collecte, verifier que le deal est pret :

```bash
TOKEN=$(cat ~/.pipedrive_token)
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN"
```

Checker dans la reponse :
1. **`r1_score` (field `e529595ef908cdf5851df4355bbce866f322fcae`)** : doit exister et etre > 0. Si absent ou null → STOP : "Ce deal n'a pas ete qualifie. Lance `/qualify {deal_id}` d'abord."
2. **Score >= 40** : si < 40 (NURTURE) → STOP : "Score {score}/100 = NURTURE. Ce deal n'est pas eligible a /prepare."
3. **Score 40-59** (CONDITIONNEL) → AVERTISSEMENT : "Score {score}/100 = CONDITIONNEL. Confirmer avec le closer avant de continuer." Attendre confirmation.
4. **`dossier_r1_link` (field `1fd2ec1073fa60e11fb59bddfec7a2f6656c4b0c`)** : si absent → AVERTISSEMENT : "Pas de dossier Drive renseigne. La collecte Drive sera ignoree." Continuer sans le module Drive.

Si les checks passent → continuer avec les etapes suivantes.

## Checklist de lecture (OBLIGATOIRE — tout lire AVANT de commencer)

L'agent DOIT lire ces fichiers avant de commencer. Ne pas lire un fichier = ne pas connaitre la regle = generer un output non conforme.

| # | Fichier | Contenu | Quand |
|---|---------|---------|-------|
| 1 | `agents/prepare-context.md` | **Bundle compact** : role, regles, positionnement, S7, pricing, output contract, validation, performance budget | Avant tout |
| 2 | `agents/prepare.md` | Routeur — architecture 3 passes | Avant tout |
| 3 | `context/design_system.md` | Couleurs, typo, gradients, espacements | Avant Pass 3 |
| 4 | `context/case_studies.md` | Bibliotheque cas clients | Avant Pass 2 |
| 5 | `context/proposal-kit-reference.md` | Aide-memoire classes CSS condensees | Avant Pass 3 |

> Les fichiers originaux (shared.md, positioning.md, s7_search_operating_model.md, pricing_rules.md, output_contract.md, validation_rules.md, s7_quick_reference.md, performance_budget.md) restent la reference complete si un detail manque dans le bundle.

## Etapes

1. Lis les fichiers 1-2 de la checklist ci-dessus
2. Execute les 3 passes avec les 2 checkpoints interactifs :
   - **Pass 1** : lis `agents/prepare-pass1.md` et execute (collecte + analyse strategique + S7 interne + SDB). En mode `--fast`, skip cette passe si SDB frais (< 2h).
   - **CHECKPOINT 1** : presente le resume strategique au closer dans le terminal (cf. `agents/prepare.md`). **ATTENDRE la validation** avant de continuer. Si corrections → mettre a jour le SDB.
   - **Pass 2** : lis fichiers 3-4, puis `agents/prepare-pass2.md` et execute (arc narratif + NBP). Lire aussi `agents/prepare-pass2-onglet4.md` pour l'onglet Investissement.
   - **CHECKPOINT 2** : presente le plan narratif au closer dans le terminal (cf. `agents/prepare.md`). **ATTENDRE la validation** avant de continuer. Si modifications → mettre a jour le NBP.
   - **Pass 3** : lis fichier 5, puis `agents/prepare-pass3.md` et execute (HTML + validation + `tools/validate_proposal.py`). Le S7 ne doit JAMAIS apparaitre dans le HTML client (regle 20).

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
- Modele S7 (diagnostic vs activation) : `context/s7_search_operating_model.md`
- Cas clients : `context/case_studies.md`

## Output

2 fichiers uploades dans le dossier Drive du deal :

| Fichier | Audience | Contenu |
|---------|----------|---------|
| `PROPOSAL-{YYYYMMDD}-{entreprise-slug}.html` | **Prospect** (via closer) | Proposition HTML interactive — 4 onglets (Diagnostic + S7, Strategie, Investissement, Cas clients) |
| `INTERNAL-S7-{YYYYMMDD}-{entreprise-slug}.md` | **Interne seulement** | Diagnostic S7 complet (scores, classification PRIMARY/SECONDARY/DEFERRED, synthese, trajectoires, ROI, resume decisionnel, evidence log) |

> Le prefixe `INTERNAL-` garantit que le fichier est exclu des outputs prospect (cf. Module 2 : exclure `DEAL-*`, `DECK-*`, `PROPOSAL-*`, `INTERNAL-*`).

Apres upload, mettre a jour `r2_pack_link` dans Pipedrive avec l'URL Drive du fichier PROPOSAL (cf. `context/pipedrive_reference.md`).

Message de fin :
```
Proposition generee : PROPOSAL-{date}-{slug}.html
Diagnostic interne : INTERNAL-S7-{date}-{slug}.md
Uploades dans le dossier Drive du deal.

Arc narratif : [description en 1 ligne de l'arc choisi et pourquoi]
S7 : contrainte = {force} | leviers = {2-3 forces} | insight = {1 phrase}
4 onglets : Diagnostic ({N} sections + S7) | Strategie (decision + 90j + ROI) | Investissement | Cas clients ({N} cas)

DRAFT — a valider avant partage avec le prospect.
Ouvre le fichier HTML dans un navigateur pour preview.
```
