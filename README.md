# SLASHR Sales Closing System — v11.0

Systeme de closing structure pilote par Claude Code. Un deal ID Pipedrive = tout le contexte automatiquement.

---

## Commandes

| Commande | Quand | Output | Stockage |
|----------|-------|--------|----------|
| `/qualify <deal_id>` | Apres R1 | Scoring terminal + update Pipedrive | Terminal |
| `/prepare <deal_id>` | R2 a preparer | PROPOSAL-*.html + INTERNAL-S7-*.md | Google Drive |
| `/pipedrive <deal_id> <action>` | Sync CRM | Mise a jour Pipedrive | Pipedrive |

---

## Architecture

```
slashr-sales-system/
├── CLAUDE.md                          <- Router (commandes + regles)
├── README.md                          <- Ce fichier
├── .claude/skills/
│   ├── qualify/SKILL.md               <- Skill /qualify
│   └── prepare/SKILL.md              <- Skill /prepare
├── agents/
│   ├── shared.md                      <- Preambule partage (role, sources, regles)
│   ├── qualify.md                     <- Processus scoring
│   └── prepare.md                     <- Processus proposition (3 passes + 3 onglets MVP)
├── templates/
│   └── proposal-kit.html             <- Kit CSS + 27 composants par role narratif
├── context/
│   ├── pipedrive_reference.md         <- IDs Pipedrive
│   ├── sales_process.md               <- Closer handbook
│   ├── positioning.md                 <- Positionnement SLASHR + structure offre
│   ├── design_system.md               <- Identite visuelle
│   ├── case_studies.md                <- Bibliotheque cas clients
│   ├── s7_search_operating_model.md   <- Modele S7 (diagnostic vs activation)
│   ├── pricing_rules.md               <- Logique de calcul budgets (interne)
│   └── output_contract.md             <- Frontiere client/interne
├── setup/
│   └── google_drive_setup.md          <- Guide setup Google Drive API
└── _archive/                          <- Versions precedentes
```

---

## Stack

| Outil | Role |
|-------|------|
| Claude Code | Agent IA — 3 commandes |
| Pipedrive | CRM + source de verite (API REST) |
| Google Drive | Stockage sources + outputs (API Service Account) |
| DataForSEO | Enrichissement data prospect (MCP tools) |

---

## Credentials

| Fichier | Usage |
|---------|-------|
| `~/.pipedrive_token` | Token API Pipedrive |
| `~/.google_service_account.json` | Service Account Google Drive |
