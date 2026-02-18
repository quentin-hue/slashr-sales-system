# SLASHR Sales Closing System — v5.0

## Objectif

Système de closing structuré pour transformer les R1 en deals signés. Piloté par un deal ID Pipedrive — Claude Code récupère tout le contexte automatiquement.

## Comment ça marche

```
/analyse 42       →  Dossier deal complet (brief scoré + pack R2)
/deck 42          →  Contenu des 10 slides R2
/relances 42      →  3 emails de relance post-R2
/onboarding 42    →  Kit de lancement post-signature
/pipedrive 42 ... →  Mise à jour CRM
```

**Un seul identifiant, le deal ID.** Claude va chercher :
- Pipedrive : deal, contact, org, notes, activités
- Google Drive : fichiers source dans le dossier du deal
- DataForSEO : enrichissement du/des domaine(s) prospect

## Flux

```
R1 terminé
  │  Le closer dépose les fichiers source dans le dossier Drive
  │  Le closer vérifie que dossier_r1_link est rempli dans Pipedrive
  ▼
/analyse 42
  → Pipedrive (deal + contact + org + notes)
  → Google Drive (transcript, notes, CdC, emails)
  → DataForSEO (domaine(s) détecté(s))
  → DEAL-*.md uploadé dans Drive
  → Pipedrive mis à jour (score, verdict, fiabilité)
  │
  ▼
/deck 42
  → Lit le DEAL-*.md depuis Drive
  → DECK-*.md (10 slides) uploadé dans Drive
  → Le closer copie dans son template Google Slides
  │
  ▼
R2 terminée, pas de signature après 48h
  │
  ▼
/relances 42
  → Lit le DEAL-*.md + email du contact (Pipedrive)
  → RELANCES-*.md (3 emails) uploadé dans Drive
  → Le closer copie dans Gmail, envoie manuellement
  │
  ▼
Deal signé
  │
  ▼
/onboarding 42
  → ONBOARDING-*.md uploadé dans Drive
  → Le closer partage avec l'équipe delivery
```

## Architecture

```
slashr-sales-system/
├── CLAUDE.md                              # Project prompt — 5 commandes
├── README.md                              # Ce fichier
├── context/
│   ├── sales_process.md        v5.0       # Pipeline, scoring, fiabilité, Pipedrive mapping
│   └── positioning.md          v1.0       # Positionnement, différenciateurs, tonalité
├── prompts/
│   └── deal_analyst_system.md  v4.0       # System prompt (4 modes)
├── templates/
│   └── followups.md            v1.0       # Templates relance J+5, J+12, J+20
├── contracts/
│   ├── r1_brief.schema.md     v1.2       # Contrat format brief R1
│   └── deal_closure.schema.md v1.1       # Contrat format debrief
├── setup/
│   └── google_drive_setup.md              # Guide setup Service Account Google Drive
└── _archive/                              # Versions précédentes
```

## Stack

| Outil | Rôle |
|-------|------|
| **Claude Code** | Cerveau unique — 5 commandes |
| **Pipedrive** | CRM + source de vérité — deal ID = point d'entrée |
| **Google Drive** | Stockage — fichiers source + outputs (1 dossier par deal) |
| **DataForSEO** | Enrichissement data prospect (via MCP tools) |
| **Google Slides** | Template deck R2 (copier-coller du contenu généré) |
| **Gmail** | Copier-coller des brouillons de relance |

## Credentials nécessaires

| Fichier | Quoi | Setup |
|---------|------|-------|
| `~/.pipedrive_token` | Token API Pipedrive | Pipedrive > Settings > API |
| `~/.google_service_account.json` | Service Account Google | `setup/google_drive_setup.md` |

DataForSEO : via MCP tools intégrés dans Claude Code (pas de credentials locaux).

## Prochaines étapes

- [x] Configurer Pipedrive (pipeline, stages, deal fields, activity types)
- [x] Implémenter le Deal Analyst Agent (system prompt 4 modes)
- [x] Architecture v5.0 — deal ID = point d'entrée unique
- [ ] Setup Google Drive Service Account (`setup/google_drive_setup.md`)
- [ ] Tester `/analyse` sur un deal réel
- [ ] Tester `/deck`, `/relances`, `/onboarding`
- [ ] Premier recalibrage trimestriel après 10 deals clôturés
