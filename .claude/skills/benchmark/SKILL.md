---
name: benchmark
description: Analyse concurrentielle standalone. Compare le prospect a ses concurrents Search.
disable-model-invocation: true
---

# BENCHMARK — Analyse concurrentielle

**Arguments :** $ARGUMENTS

## Parsing des arguments

Extraire du `$ARGUMENTS` :
- `deal_id` : le premier token numerique
- `--competitors domain1,domain2` : flag optionnel (concurrents fournis manuellement)
- `--fresh` : flag optionnel (force re-collecte)

Exemples : `/benchmark 560`, `/benchmark 560 --competitors rival1.com,rival2.com`

## Objectif

Produire une analyse concurrentielle standalone du prospect. Utile quand le closer veut preparer ses arguments avant R2 sans generer la proposition complete.

## Prerequis

1. Lis `agents/shared.md` (preambule partage, regles)
2. Lis `agents/benchmark.md` (processus benchmark)

## Etape 0 — Recuperer le deal et le domaine

```bash
TOKEN=$(cat ~/.pipedrive_token)
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN"
```

## Etapes

1. **Identifier le domaine principal**
2. **Collecter les donnees concurrentielles** via DataForSEO :
   - `competitors_domain` (top 10) → filtrer bruit vs business vs semantique
   - `domain_rank_overview` x top 5 concurrents
   - `domain_intersection` (prospect vs top 3 concurrents)
   - Si aucun concurrent business → Module 4c (detection niche via SERPs)
3. **Analyser les gaps** :
   - Gap de trafic (ratio prospect vs leader)
   - Keywords exclusifs a chaque concurrent
   - Opportunites non adressees par le prospect
   - Positionnement semantique compare
4. **Generer le rapport** dans `.cache/deals/{deal_id}/benchmark.md`
5. **Afficher le resume** dans le terminal

## Output

### Terminal
```
═══════════════════════════════════════════════
  BENCHMARK · {Entreprise} (Deal #{deal_id})
═══════════════════════════════════════════════

  Domaine prospect  {domaine} · {trafic} visites/mois · {N} keywords

───────────────────────────────────────────────
  CONCURRENTS IDENTIFIES
───────────────────────────────────────────────

  #  Domaine              Trafic     Keywords   ETV        Gap
  1. {concurrent1}        {trafic}   {kw}       {etv}      {ratio}x
  2. {concurrent2}        {trafic}   {kw}       {etv}      {ratio}x
  3. {concurrent3}        {trafic}   {kw}       {etv}      {ratio}x

───────────────────────────────────────────────
  GAPS STRATEGIQUES
───────────────────────────────────────────────

  Keywords que {concurrent1} a et pas {prospect} :
  - {keyword1} : {volume} rech/mois, difficulte {N}
  - {keyword2} : {volume} rech/mois, difficulte {N}
  - {keyword3} : {volume} rech/mois, difficulte {N}

───────────────────────────────────────────────
  OPPORTUNITES
───────────────────────────────────────────────

  {3-5 lignes : ce que le prospect peut aller chercher et comment}

  → Pour generer la proposition complete : /prepare {deal_id}
═══════════════════════════════════════════════
```

### Fichier cache
Ecrire dans `.cache/deals/{deal_id}/benchmark.md`

## Reference

- Processus benchmark : `agents/benchmark.md`
- Performance budget : `context/performance_budget.md`
- Filtrage concurrents : `agents/prepare-pass1.md` (Module 4)
