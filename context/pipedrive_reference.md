# Pipedrive Reference — SLASHR v11.0

> **Source unique** pour tous les IDs Pipedrive. Les autres fichiers y font reference.

---

## Pipeline

Pipeline SLASHR (id: `1`)

| # | Stage | ID | Proba | Commande |
|---|-------|----|-------|----------|
| 1 | Lead In | `1` | 0% | — |
| 2 | R1 Scheduled | `6` | 10% | — |
| 3 | R1 Done | `2` | 30% | `/audit` |
| 4 | R2 Scheduled | `7` | 50% | `/prepare` |
| 5 | R2 Done | `4` | 50% | — |
| 6 | Pending Signature | `8` | 80% | — |

---

## Deal Fields

| Champ | ID | Key hash | Type | Valeurs |
|-------|----|----------|------|---------|
| Leviers pressentis | `42` | `f8c51fb60ea43a34c56998b6ad9bf946234149a1` | set | SEO, GEO, SEA/SMA, DATA, UX, DEV, Autres |
| Canal d'origine | `36` | — (champ standard) | enum | Partenaire, Site web, Action marketing, Prospection, Reseau, Bouche a oreille, Relation client |
| decideur_level | `56` | `0b4c7e8cc10ced7badf65b34dac6254bd10a0179` | enum | DECIDEUR (95), INFLUENCEUR (96), OPERATIONNEL (97) |
| r2_pack_link | `55` | `4b84e7bfe1a6b330318fc7a0d208e2faedf2530a` | varchar | URL Google Drive (proposition) |
| dossier_r1_link | `58` | `1fd2ec1073fa60e11fb59bddfec7a2f6656c4b0c` | varchar | URL Google Drive (dossier R1) |
| domaine_principal | `59` | `d76190f6be0ca288aeac6107f2fb5d784d0f5e28` | varchar | Domaine principal du prospect (ex: resetlaser.com) |
| gads_customer_id | — | `2389e066f59aa6dae4edb9903557fdec7924426a` | varchar | Customer ID Google Ads du prospect (format: 475-819-4195) |

> **Champs supprimes en v12 :** `r1_score` (52), `qualification_status` (60), `r1_verdict` (53), `r1_fiabilite` (54), `relance_status` (57).

---

## Org Fields

| Champ | Key hash |
|-------|----------|
| URL du site internet | `9d5262c3746211eb06e2b06ab13d5162c22e5734` |

---

## API Endpoints

### Deal, Contact, Organisation, Notes, Activites

```bash
TOKEN=$(cat ~/.pipedrive_token)

# Deal (titre, stage, custom fields)
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN"

# Contact (prenom, nom, email, telephone)
curl -s "https://api.pipedrive.com/v1/persons/{person_id}?api_token=$TOKEN"

# Organisation (nom, domaine)
curl -s "https://api.pipedrive.com/v1/organizations/{org_id}?api_token=$TOKEN"

# Notes du deal
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}/notes?api_token=$TOKEN"

# Activites du deal
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}/activities?api_token=$TOKEN"

# Update deal field
curl -s -X PUT "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"field_key": "value"}'
```

### Emails (synchro Pipedrive)

Les emails sont synchronises dans Pipedrive, pas dans Drive. Recuperer les threads lies au deal :

```bash
# Threads inbox lies au deal (filtrer cote client par deal_id)
curl -s "https://api.pipedrive.com/v1/mailbox/mailThreads?folder=inbox&api_token=$TOKEN"

# Threads envoyes lies au deal
curl -s "https://api.pipedrive.com/v1/mailbox/mailThreads?folder=sent&api_token=$TOKEN"

# Messages d'un thread (from, to, subject, snippet, body_url)
curl -s "https://api.pipedrive.com/v1/mailbox/mailThreads/{thread_id}/mailMessages?api_token=$TOKEN"
```

**Note :** Le filtre `deal_id` ne fonctionne pas cote serveur sur les endpoints mailbox. Recuperer tous les threads et filtrer cote client par `deal_id == {id}`.
