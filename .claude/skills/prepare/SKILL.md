---
name: prepare
description: Genere la proposition HTML interactive sur-mesure — 3 passes internes (Data & Strategy, Narrative, Design), 4 onglets MVP, uploadee dans Drive.
disable-model-invocation: true
---

# PREPARE — Proposition HTML interactive

**Deal ID :** $ARGUMENTS

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

L'agent DOIT lire ces fichiers dans l'ordre ci-dessous avant de lancer la Pass 1. Ne pas lire un fichier = ne pas connaitre la regle = generer un output non conforme.

| # | Fichier | Contenu | Quand |
|---|---------|---------|-------|
| 1 | `agents/shared.md` | Preambule partage : role, sources, 18 regles | Avant tout |
| 2 | `agents/prepare.md` | Routeur — architecture 3 passes | Avant tout |
| 3 | `context/positioning.md` | Positionnement, tonalite, structure offre | Avant tout |
| 4 | `context/s7_search_operating_model.md` | Modele S7 : scoring, classification, anti-patterns | Avant tout |
| 5 | `context/pricing_rules.md` | Calcul budgets Phase 1 & Phase 2 (interne) | Avant tout |
| 6 | `context/output_contract.md` | Frontiere client/interne (visible vs masque) | Avant tout |
| 6b | `context/validation_rules.md` | 39 regles de validation (3 layers) | Avant tout |
| 6c | `context/s7_quick_reference.md` | Digest compact S7 (7 forces, echelle, classification) | Avant tout |
| 7 | `context/design_system.md` | Couleurs, typo, gradients, espacements | Avant Pass 3 |
| 8 | `context/case_studies.md` | Bibliotheque cas clients | Avant Pass 2 |
| 9 | `templates/proposal-kit.html` | Kit CSS + 27 composants par role narratif | Avant Pass 3 |
| 10 | `context/proposal-kit-reference.md` | Aide-memoire classes CSS condensees | Avant Pass 3 |

## Etapes

1. Lis les fichiers 1-6c de la checklist ci-dessus
2. Execute les 3 passes dans l'ordre :
   - **Pass 1** : lis `agents/prepare-pass1.md` et execute (collecte + S7 + SDB)
   - **Pass 2** : lis fichiers 7-8, puis `agents/prepare-pass2.md` et execute (arc narratif + NBP). Lire aussi `agents/prepare-pass2-onglet4.md` pour l'onglet 4.
   - **Pass 3** : lis fichiers 9-10, puis `agents/prepare-pass3.md` et execute (HTML + validation + `tools/validate_proposal.py`)

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
- Kit composants (27 composants, catalogue par role narratif) : `templates/proposal-kit.html`
- Design system : `context/design_system.md`
- Positionnement + structure offre : `context/positioning.md`
- Modele S7 (diagnostic vs activation) : `context/s7_search_operating_model.md`
- Cas clients : `context/case_studies.md`

## Output

2 fichiers uploades dans le dossier Drive du deal :

| Fichier | Audience | Contenu |
|---------|----------|---------|
| `PROPOSAL-{YYYYMMDD}-{entreprise-slug}.html` | **Prospect** (via closer) | Proposition HTML interactive — 4 onglets avec section S7 |
| `INTERNAL-S7-{YYYYMMDD}-{entreprise-slug}.md` | **Interne seulement** | Diagnostic S7 complet (scores, classification PRIMARY/SECONDARY/DEFERRED, synthese, trajectoires, ROI, resume decisionnel, evidence log) |

> Le prefixe `INTERNAL-` garantit que le fichier est exclu des outputs prospect (cf. Module 2 : exclure `DEAL-*`, `DECK-*`, `PROPOSAL-*`, `INTERNAL-*`).

Message de fin :
```
Proposition generee : PROPOSAL-{date}-{slug}.html
Diagnostic interne : INTERNAL-S7-{date}-{slug}.md
Uploades dans le dossier Drive du deal.

Arc narratif : [description en 1 ligne de l'arc choisi et pourquoi]
S7 : contrainte = {force} | leviers = {2-3 forces} | insight = {1 phrase}
4 onglets : Strategie ({N} sections + S7) | Cas Clients ({N} cas) | ROI Interactif | Livrables & Methode

DRAFT — a valider avant partage avec le prospect.
Ouvre le fichier HTML dans un navigateur pour preview.
```
