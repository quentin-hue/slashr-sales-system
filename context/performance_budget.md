# Performance Budget — v1.0 (Rapidite / Fiabilite / Scalabilite)

Objectif : rendre /qualify et /prepare predictibles, rapides, et rejouables.
Ce doc est la source de verite des limites d'execution.

---

## 1) Principes

1. **Idempotent** : relancer /prepare sur le meme deal ne doit pas redemander inutilement les memes APIs.
2. **Graceful degradation** : seul l'echec du deal Pipedrive est bloquant. Le reste degrade et continue. (cf. agents/shared.md)
3. **Evidence-first** : chaque chiffre important doit pointer vers une evidence (source + endpoint + timestamp).
4. **Context thin** : on ne met jamais des dumps bruts (emails complets, gros CSV) dans le "raisonnement" si un resume suffit.

---

## 2) Budgets d'appels (par execution /prepare)

### Pipedrive

> **Execution recommandee :** via `tools/batch_pipedrive.py` en parallele. Voir section **3c) Batch Pipedrive Tool**.

- Pagination threads : **max 6 pages** (6 * 50 = 300 threads inbox + 300 sent)
- Messages : **max 10 derniers** par thread retenu
- Body complet : seulement si snippet insuffisant (**max 3 bodies**)

### Google Drive

> **Execution recommandee :** via `tools/batch_drive.py` en parallele. Voir section **3d) Batch Drive Tool**.

- Recursion dossiers : **max 3 niveaux** (deja en place)
- Taille par fichier export : **max 100 000 caracteres** (deja en place)
- Nombre max de fichiers telecharges : **25** (au-dela : prendre les 25 plus recents + log warning)

### DataForSEO (par domaine prospect)

> **Execution recommandee :** via `tools/batch_dataforseo.py` par lots paralleles. Voir section **3b) Batch DataForSEO Tool** pour les parametres et le decoupage en lots.

- domain_rank_overview : 1
- ranked_keywords : 1 (top 30)
- keywords_for_site : 1 (top 20)
- competitors_domain : 1 (top 10)
- domain_rank_overview concurrents : 3 max
- domain_intersection : 1 (vs top concurrent)
- search_intent : 1 (max **1000 keywords**)

### DataForSEO — Module 4c (conditionnel, niches sans concurrent business)
Declenche uniquement si `competitors_domain` ne remonte aucun concurrent business.
- serp_organic_live_regular : 5-8 (requetes commerciales cles)
- domain_rank_overview (concurrents niche) : 5 max
- ranked_keywords (concurrents niche) : 5 max
- domain_intersection : 1

**Comptage typique Module 4c : 16-19 appels.**

**Hard stop** : si DataForSEO renvoie timeouts / erreurs 500 sur 2 tentatives, continuer avec domain_rank_overview uniquement.

### Module 11 — Website Crawl (toujours actif)
- Requetes HTTP : **max 10** (robots.txt + homepage + sitemap + 3-5 pages samples)
- Timeout global : **60s**
- Timeout par requete : **20s**
- Retry : **1** sur timeout uniquement (homepage), 0 pour les pages samples
- Hard stop : si homepage KO apres 1 retry → SKIP Module 11, le deal continue sans
- DataForSEO : **0 appels**
- Body cap : **500 KB** par page

### Google Search Console (Module 3b, conditionnel)
- Appel probe (detection acces) : 1 appel MCP (rowLimit 1, 7 jours)
- Si acces confirme : 3 appels MCP (performance, queries, pages)
- Total : 1-4 appels MCP, 0 appels DataForSEO
- Timeout : 15s par appel
- Cache : meme politique que DataForSEO (< 24h reuse, 24h-7j warn+reuse, > 7j refetch)

### Budget /debrief
- Pipedrive : 1 appel GET deal (status, montant, lost_reason)
- Fichiers locaux : lecture `.cache/deals/{deal_id}/artifacts/` (pas d'API)
- DataForSEO : 0 appels

---

## 3) Timeouts / Retries

- Timeout par requete : 20s
- Retries : 2 max
- Backoff : 1s puis 3s
- Jitter : oui (si possible)

---

## 3b) Batch DataForSEO Tool

**Outil :** `tools/batch_dataforseo.py` — execute N appels DataForSEO en parallele avec cache integre.

### Parametres

| Parametre | Valeur |
|-----------|--------|
| Workers paralleles | 5 (ThreadPoolExecutor) |
| Timeout par requete | 20s |
| Retries | 2 max |
| Backoff | 1s puis 3s |
| Cache < 24h | Reutiliser (fresh) |
| Cache 24h-7j | Reutiliser + WARNING (stale) |
| Cache > 7j | Re-fetch obligatoire (expired) |
| Validation cache | Non-vide + JSON parseable + status_code 20000 |

### Invocation

```bash
# Via fichier (recommande pour les gros lots)
python3 tools/batch_dataforseo.py --deal-id 560 --requests-file /tmp/batch_lot1.json

# Via argument inline (petits lots)
python3 tools/batch_dataforseo.py --deal-id 560 --requests '[...]'
```

### Output

- **stdout** : JSON summary uniquement (parseable par l'agent)
- **stderr** : logs `[INFO]`/`[WARN]`/`[ERROR]`
- **Exit codes** : 0=OK, 1=usage, 2=partiel, 3=fatal

### Decoupage en 5 lots (alignes sur prepare-pass1.md)

| Lot | Contenu | Requetes typiques | Dependance |
|-----|---------|-------------------|------------|
| 1 | Modules 3 + 4 debut | 4 | Domaine connu |
| 2 | Module 4 benchmark | 4 | Lot 1 (concurrents) |
| 3 | Module 4c SERPs (conditionnel) | 5-8 | Lot 1 (pas de concurrent business) |
| 4 | Module 4c deep-dive (conditionnel) | 11 | Lot 3 (niche identifies) |
| 5 | Module 4b + conditionnels 5-10 | 1-10 | Lots precedents |

**Comptage typique :** 8-37 requetes selon activation Module 4c et modules conditionnels.

---

## 3c) Batch Pipedrive Tool

**Outil :** `tools/batch_pipedrive.py` — collecte toutes les donnees Pipedrive d'un deal en parallele.

### Parametres

| Parametre | Valeur |
|-----------|--------|
| Workers paralleles | 5 (ThreadPoolExecutor) |
| Timeout par requete | 20s |
| Pagination emails | 6 pages inbox + 6 pages sent (12 requetes paralleles) |
| Messages par thread | 10 max |
| Cache | < 24h reuse, 24h-7j warn+reuse, > 7j refetch |

### Pipeline

```
Phase 1: GET deal (bloquant, besoin de person_id + org_id)
Phase 2: parallele (person + org + notes + activities + 12 pages emails)
Phase 3: filtre threads par deal_id
Phase 4: parallele (messages des threads matches)
```

### Invocation

```bash
python3 tools/batch_pipedrive.py --deal-id 560
```

**Gain :** 12 pages emails en parallele au lieu de sequentiel → **120s → 30-40s**.

---

## 3d) Batch Drive Tool

**Outil :** `tools/batch_drive.py` — listing recursif + telechargements paralleles des fichiers Drive.

### Parametres

| Parametre | Valeur |
|-----------|--------|
| Workers paralleles | 3 (ThreadPoolExecutor) |
| Recursion dossiers | 3 niveaux max |
| Fichiers max | 25 (plus recents) |
| Taille max par fichier | 100 000 caracteres |
| Cache | < 24h reuse, 24h-7j warn+reuse, > 7j refetch |

### Invocation

```bash
python3 tools/batch_drive.py --deal-id 560 --folder-id XXXXX
python3 tools/batch_drive.py --deal-id 560 --folder-url "https://drive.google.com/..."
```

**Gain :** 12 fichiers en parallele (3 workers) → **100s → 30s** sur collections fraiches.

---

## 4) Cache (obligatoire)

Stocker toutes les reponses API sous `.cache/` pour replay et debug.

Arborescence :

.cache/
  deals/{deal_id}/
    pipedrive/
      deal.json
      org.json
      person.json
      notes.json
      activities.json
      emails_threads_inbox_page*.json
      emails_threads_sent_page*.json
      emails_messages_thread_{id}.json
    drive/
      manifest.json
      files/{file_id}.txt
    dataforseo/
      domain_{domain}/domain_rank_overview.json
      domain_{domain}/ranked_keywords.json
      domain_{domain}/keywords_for_site.json
      domain_{domain}/competitors_domain.json
      domain_{domain}/competitor_{domain}/domain_rank_overview.json
      domain_{domain}/domain_intersection_{competitor}.json
      domain_{domain}/search_intent.json
    website/
      homepage.json
      sitemap.json
      sampled_pages.json
      crawl_summary.json

Regle : si un fichier cache existe et a moins de 24h, le reutiliser.

### Compression gzip (DataForSEO)

Les reponses DataForSEO > 100 KB sont automatiquement compressees en `.json.gz` par `batch_dataforseo.py`. La decompression est transparente a la lecture (le tool gere les deux formats). Gain typique : `ranked_keywords` 241 KB → ~35 KB (7x).

---

## 5) Contrats inter-pass (reduction tokens)

**SDB (Pass1 output interne)** = "thin + evidence log"
- Synthese (bullets)
- Tables compactes (top N)
- Evidence log (liste des sources + endpoints + timestamps)

**NBP (Pass2)** : jamais de data brute. Que narration + references vers les blocs SDB.

---

## 6) Validation et fraicheur du cache

### Validation JSON avant reutilisation

Avant de reutiliser un fichier cache :
1. Verifier que le fichier n'est pas vide (taille > 0)
2. Verifier qu'il est parseable en JSON valide
3. Verifier que la reponse contient un indicateur de succes (`success`, `status_code`, etc.)
4. Si la validation echoue : supprimer le fichier cache et re-fetch

### Fraicheur

| Age du cache | Action |
|-------------|--------|
| < 24h | Reutiliser directement |
| 24h - 7j | Reutiliser + afficher WARNING dans le terminal : "Cache stale ({age}h) pour {endpoint}" |
| > 7j | Re-fetch obligatoire. Supprimer le cache obsolete avant |

### Perimetre du cache

Cacher **toutes** les reponses API, pas seulement DataForSEO :

| Source | Fichiers caches |
|--------|----------------|
| Pipedrive | `deal.json`, `org.json`, `person.json`, `notes.json`, `activities.json`, `emails_*.json` |
| Google Drive | `manifest.json`, `files/{id}.txt` |
| DataForSEO | Tous les endpoints par domaine |
| Website Crawl (Module 11) | `website/homepage.json`, `website/sitemap.json`, `website/sampled_pages.json`, `website/crawl_summary.json` |
| Google Search Console (Module 3b) | `gsc/performance.json`, `gsc/queries.json`, `gsc/pages.json` |

### Invalidation

- Un re-run `/prepare` sur un deal deja cache reutilise le cache sauf si force (`/prepare {id} --fresh`)
- Un `/qualify` ne partage PAS le cache avec `/prepare` (les besoins sont differents)
