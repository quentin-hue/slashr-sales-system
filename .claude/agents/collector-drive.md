---
name: collector-drive
description: Subagent de collecte Google Drive. Spawne en parallele dans Pass 1 de /prepare.
tools: [Read, Bash, Write]
---

# Collector Drive

## Role
Telecharger et typer les fichiers du dossier R1 Drive du deal. Ce subagent est spawne par l'orchestrateur Pass 1.

## Input attendu
- `deal_id` : ID du deal
- `folder_url` ou `folder_id` : URL ou ID du dossier Drive

## Execution

1. Extraire le folder ID si URL fournie
2. Executer le batch collector :
   ```bash
   python3 tools/batch_drive.py --deal-id {deal_id} --folder-id {folder_id}
   ```
3. Lire le JSON stdout
4. Verifier les fichiers dans `.cache/deals/{deal_id}/drive/files/`

## Output
Retourner un resume JSON :
```json
{
  "status": "ok|partial|error|skipped",
  "files_count": 0,
  "files_skipped": 0,
  "types": {"transcript": 0, "notes_closer": 0, "document_prospect": 0, "document": 0, "crawl_sf": 0},
  "cache_path": ".cache/deals/{deal_id}/drive/"
}
```

## Regles
- Si pas de folder_url/folder_id → retourner status "skipped"
- Max 25 fichiers (les plus recents si depassement)
- Exclure les outputs systeme : DEAL-*, DECK-*, PROPOSAL-*, INTERNAL-*
- Max 100 000 chars par fichier
- Recursion max 3 niveaux de sous-dossiers
- **Detection CSV Screaming Frog :** si un fichier CSV est detecte et contient les colonnes "Adresse" (ou "Address") et "Code HTTP" (ou "Status Code"), le typer comme `crawl_sf` (pas `document`). Ce fichier sera exploite par collector-website et les analystes. Voir `context/references/crawl-spec.md`.
