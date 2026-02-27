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
- Pagination threads : **max 6 pages** (6 * 50 = 300 threads inbox + 300 sent)
- Messages : **max 10 derniers** par thread retenu
- Body complet : seulement si snippet insuffisant (**max 3 bodies**)

### Google Drive
- Recursion dossiers : **max 3 niveaux** (deja en place)
- Taille par fichier export : **max 100 000 caracteres** (deja en place)
- Nombre max de fichiers telecharges : **25** (au-dela : prendre les 25 plus recents + log warning)

### DataForSEO (par domaine prospect)
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

Regle : si un fichier cache existe et a moins de 24h, le reutiliser.

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

### Invalidation

- Un re-run `/prepare` sur un deal deja cache reutilise le cache sauf si force (`/prepare {id} --fresh`)
- Un `/qualify` ne partage PAS le cache avec `/prepare` (les besoins sont differents)
