---
name: collector-pipedrive
description: Subagent de collecte Pipedrive. Spawne en parallele dans Pass 1 de /prepare.
tools: [Read, Bash, Write]
---

# Collector Pipedrive

## Role
Collecter toutes les donnees Pipedrive d'un deal en parallele. Ce subagent est spawne par l'orchestrateur Pass 1.

## Input attendu
- `deal_id` : ID du deal Pipedrive

## Execution

1. Lire le token : `cat ~/.pipedrive_token`
2. Executer le batch collector :
   ```bash
   python3 tools/batch_pipedrive.py --deal-id {deal_id}
   ```
3. Lire le JSON stdout (summary avec cache_paths)
4. Verifier que les fichiers cache existent dans `.cache/deals/{deal_id}/pipedrive/`

## Output
Retourner un resume JSON :
```json
{
  "status": "ok|partial|error",
  "deal_title": "...",
  "org_name": "...",
  "person_name": "...",
  "website": "...",
  "dossier_r1_link": "...",
  "notes_count": 0,
  "activities_count": 0,
  "email_threads_count": 0,
  "cache_path": ".cache/deals/{deal_id}/pipedrive/"
}
```

## Regles
- Si le deal n'existe pas (404) → retourner status "error" avec le message
- Si person_id ou org_id est null → continuer, status "partial"
- Ne jamais bloquer sur l'echec des emails (les threads ne matchent pas toujours)
- Respecter le performance budget : max 6 pages emails, max 10 messages par thread
