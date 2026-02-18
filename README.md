# SLASHR Sales Closing System — v8.0

Systeme de closing structure pilote par Claude Code. Un deal ID Pipedrive = tout le contexte automatiquement.

---

## Commandes

| Commande | Quand | Output | Stockage |
|----------|-------|--------|----------|
| `/analyse <deal_id>` | Apres R1 | DEAL-*.md (qualification) | Google Drive |
| `/deck <deal_id>` | R2 a preparer | DECK-*.md (audit + slides + ammunition) | Google Drive |
| `/proposal <deal_id>` | Apres /deck, avant/apres R2 | PROPOSAL-*.html (proposition commerciale) | Google Drive |
| `/relances <deal_id>` | 48h apres R2 sans signature | RELANCES-*.md (3 emails) | Google Drive |
| `/onboarding <deal_id>` | Deal signe | ONBOARDING-*.md (kit lancement) | Google Drive |
| `/status <deal_id>` | A tout moment | Affichage inline | Pas de fichier |
| `/recalibration [periode]` | Trimestriel | RECALIBRATION-*.md | Google Drive |
| `/pipedrive <deal_id> <action>` | Sync CRM | Mise a jour Pipedrive | Pipedrive |

---

## Architecture

```
slashr-sales-system/
├── CLAUDE.md                          <- Router (commandes + API sequences)
├── README.md                          <- Ce fichier
├── context/
│   ├── sales_process.md               <- Closer handbook
│   ├── positioning.md                 <- Positionnement SLASHR
│   ├── design_system.md               <- Identite visuelle
│   └── pipedrive_reference.md         <- Source unique IDs Pipedrive
├── agents/
│   ├── shared.md                      <- Preambule partage
│   ├── analyse.md                     <- Mode ANALYSE
│   ├── deck.md                        <- Mode DECK
│   ├── proposal.md                    <- Mode PROPOSAL
│   ├── relances.md                    <- Mode RELANCES
│   ├── onboarding.md                  <- Mode ONBOARDING
│   ├── status.md                      <- Mode STATUS
│   └── recalibration.md              <- Mode RECALIBRATION
├── templates/
│   ├── followups.md                   <- Templates relances
│   └── proposal_base.html             <- Template HTML proposition
├── contracts/
│   └── deal_closure.schema.md         <- Format debrief deal
├── setup/
│   └── google_drive_setup.md          <- Setup Google Drive API
└── _archive/                          <- Versions precedentes
```

---

## Stack

| Outil | Role |
|-------|------|
| Claude Code | Agent IA — 8 commandes |
| Pipedrive | CRM + source de verite (API REST) |
| Google Drive | Stockage sources + outputs (API Service Account) |
| DataForSEO | Enrichissement data prospect (MCP tools) |
| Google Slides | Template deck R2 (copier-coller manuel) |
| Gmail | Envoi relances (copier-coller manuel) |

---

## Credentials

| Fichier | Usage |
|---------|-------|
| `~/.pipedrive_token` | Token API Pipedrive |
| `~/.google_service_account.json` | Service Account Google Drive |
