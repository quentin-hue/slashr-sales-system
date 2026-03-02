---
name: qualify
description: Score un deal apres le R1 — collecte Pipedrive + Drive + SEO light, scoring terminal, update Pipedrive. Rejouable.
disable-model-invocation: true
---

# QUALIFY — Scoring rapide du deal

**Deal ID :** $ARGUMENTS

## Etapes

1. Lis `agents/shared.md` (preambule partage : role, sources, regles)
2. Lis `agents/qualify.md` (processus complet de scoring)
3. Suis le processus decrit dans qualify.md :
   - **Collecte** : Pipedrive (deal, contact, org, notes, activites, emails) + Drive (fichiers du dossier R1) + SEO light (`domain_rank_overview` par domaine)
   - **Scoring** : 5 criteres (Douleur x6, Urgence x5, Budget x4, Decideur x3, Fit x2), max 100
   - **Affichage** : format terminal structure (voir qualify.md)
   - **Update Pipedrive** : r1_score + decideur_level + qualification_status + leviers_pressentis + domaine_principal

## Collecte Pipedrive

```bash
TOKEN=$(cat ~/.pipedrive_token)

# Deal
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN"

# Contact (person_id du deal)
curl -s "https://api.pipedrive.com/v1/persons/{person_id}?api_token=$TOKEN"

# Organisation (org_id du deal)
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
- Design system : non utilise (pas de fichier genere)
- Positionnement : `context/positioning.md`

## Output

Scoring dans le terminal. Pas de fichier genere. Rejouable (ecrase le score precedent).
