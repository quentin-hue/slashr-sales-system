# SLASHR Sales Closing System — v11.0

Systeme de closing structure pilote par Claude Code. Un deal ID Pipedrive = tout le contexte automatiquement.

---

## Commandes

| Commande | Quand | Output | Stockage |
|----------|-------|--------|----------|
| `/qualify <deal_id>` | Apres R1 | Scoring terminal + update Pipedrive | Terminal |
| `/prepare <deal_id>` | R2 a preparer | PROPOSAL-*.html + INTERNAL-S7-*.md | Google Drive |
| `/validate <path_or_deal_id>` | Verification HTML | Rapport validation (4 layers, 45 regles) | Terminal |
| `/debrief <deal_id>` | Apres won/lost | Retroaction closer + patterns | `.cache/` |
| `/pipedrive <deal_id> <action>` | Sync CRM | Mise a jour Pipedrive | Pipedrive |

---

## Architecture

```
slashr-sales-system/
├── CLAUDE.md                          <- Router (commandes + regles)
├── README.md                          <- Ce fichier
├── .claude/skills/
│   ├── qualify/SKILL.md               <- Skill /qualify
│   ├── prepare/SKILL.md              <- Skill /prepare
│   ├── validate/SKILL.md            <- Skill /validate (HTML standalone)
│   └── debrief/SKILL.md             <- Skill /debrief (retroaction won/lost)
├── agents/
│   ├── shared.md                      <- Preambule partage (role, sources, regles)
│   ├── qualify.md                     <- Processus scoring
│   ├── prepare.md                     <- Routeur proposition (3 passes sequentielles)
│   ├── prepare-pass1.md               <- Pass 1 : Data & Strategy Engine (collecte + S7 + SDB)
│   ├── prepare-pass2.md               <- Pass 2 : Narrative Architect (arc + NBP)
│   ├── prepare-pass2-onglet4.md       <- Pass 2 : Spec detaillee onglet Investissement
│   └── prepare-pass3.md               <- Pass 3 : Design Orchestrator (HTML + validation)
├── tools/
│   ├── validate_proposal.py          <- Validation HTML automatisee (45 regles, 4 layers)
│   └── preflight_check.py            <- Verification dependances API pre-run
├── templates/
│   └── proposal-kit.html             <- Kit CSS + 30 composants par role narratif (reference, pas template)
├── context/
│   ├── pipedrive_reference.md         <- IDs Pipedrive
│   ├── sales_process.md               <- Closer handbook
│   ├── positioning.md                 <- Positionnement SLASHR + structure offre (Audit + Accompagnement)
│   ├── design_system.md               <- Identite visuelle
│   ├── case_studies.md                <- Bibliotheque cas clients (reference pour onglet Cas Clients)
│   ├── s7_search_operating_model.md   <- Modele S7 (diagnostic vs activation)
│   ├── s7_quick_reference.md          <- Digest compact S7 (7 forces, echelle, classification)
│   ├── validation_rules.md            <- 45 regles de validation consolidees (4 layers)
│   ├── pricing_rules.md               <- Logique de calcul budgets Phase 1 & Phase 2 (interne)
│   ├── output_contract.md             <- Frontiere client/interne (ce qui est visible vs masque)
│   ├── performance_budget.md          <- Budgets d'appels, cache, timeouts
│   └── proposal-kit-reference.md      <- Aide-memoire classes CSS + snippets standalone
├── setup/
│   └── google_drive_setup.md          <- Guide setup Google Drive API
└── _archive/                          <- Versions precedentes
```

---

## Stack

| Outil | Role |
|-------|------|
| Claude Code | Agent IA — 5 commandes |
| Pipedrive | CRM + source de verite (API REST) |
| Google Drive | Stockage sources + outputs (API Service Account) |
| DataForSEO | Enrichissement data prospect (MCP tools) |

---

## Credentials

| Fichier | Usage |
|---------|-------|
| `~/.pipedrive_token` | Token API Pipedrive |
| `~/.google_service_account.json` | Service Account Google Drive |
