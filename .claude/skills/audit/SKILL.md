---
name: audit
description: Diagnostic SEO rapide du prospect. Score 0-100 oriente closing. Genere un rapport markdown dans le cache.
disable-model-invocation: true
---

# AUDIT — Diagnostic SEO rapide

**Arguments :** $ARGUMENTS

## Parsing des arguments

Extraire du `$ARGUMENTS` :
- `deal_id` : le premier token numerique
- `--fresh` : flag optionnel (force re-collecte, ignore le cache)

Exemples : `/audit 560`, `/audit 560 --fresh`

## Objectif

Produire un diagnostic SEO rapide du prospect, calibre pour le closing (pas un audit technique generique). Repond a la question : "Ce prospect a-t-il un potentiel Search suffisant pour justifier une proposition ?"

Utilisable entre le R1 et le /prepare pour enrichir la discussion avec le closer.

## Prerequis

1. Lis `agents/shared.md` (preambule partage, regles)
2. Lis `agents/audit.md` (processus audit)

## Etape 0 — Recuperer le deal Pipedrive

```bash
TOKEN=$(cat ~/.pipedrive_token)
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN"
```

Extraire : titre, org, website, dossier_r1_link.

## Etapes

1. **Identifier le domaine principal** (meme logique que /prepare : org website > notes > emails)
2. **Lancer les collectes en parallele** :
   - Collector SEO (DataForSEO : domain_rank_overview + ranked_keywords top 30 + competitors_domain)
   - Collector Website (crawl technique : robots.txt, sitemap, homepage, 3 pages)
   - Collector GSC (si disponible)
3. **Analyser et scorer** (cf. `agents/audit.md` pour la grille)
4. **Generer le rapport** dans `.cache/deals/{deal_id}/audit.md`
5. **Afficher le resume** dans le terminal

## Ponderation du score SEO (orientee closing)

| Categorie | Poids | Justification |
|-----------|-------|---------------|
| Potentiel de marche (volumes, gaps) | 30% | Prouver l'opportunite business |
| Technical SEO | 20% | Fondamentaux |
| Content & E-E-A-T | 20% | Qualite du contenu existant |
| Benchmark concurrentiel | 15% | Gap concurrentiel = argument de vente |
| GEO / AI Search | 10% | Differenciateur SLASHR |
| Local (conditionnel) | 5% | Poids faible sauf business local |

## Output

### Terminal
```
═══════════════════════════════════════════════
  AUDIT SEO · {Entreprise} (Deal #{deal_id})
═══════════════════════════════════════════════

  Domaine        {domaine}
  Score SEO      {score}/100

───────────────────────────────────────────────
  POTENTIEL DE MARCHE (30%)         {note}/100
───────────────────────────────────────────────
  Trafic organique : {N} visites/mois
  Keywords indexes : {N}
  Volume marche adressable : {N} rech/mois
  Gap vs leader : {N}%

───────────────────────────────────────────────
  TECHNICAL (20%)                   {note}/100
───────────────────────────────────────────────
  HTTPS : {oui/non}
  Mobile : {oui/non}
  Sitemap : {oui/non}
  robots.txt : {ok/probleme}

───────────────────────────────────────────────
  CONTENT (20%)                     {note}/100
───────────────────────────────────────────────
  Pages indexees : {N}
  Contenu thin : {N} pages
  Schema : {types trouves}

───────────────────────────────────────────────
  BENCHMARK (15%)                   {note}/100
───────────────────────────────────────────────
  Top 3 concurrents : {noms}
  Gap trafic vs #1 : {N}x
  Keywords exclusifs concurrent : {N}

───────────────────────────────────────────────
  GEO / AI SEARCH (10%)            {note}/100
───────────────────────────────────────────────
  llms.txt : {present/absent}
  Donnees structurees : {ok/partiel/absent}
  Citabilite IA : {haute/moyenne/faible}

───────────────────────────────────────────────
  RECOMMANDATION
───────────────────────────────────────────────
  {3-5 lignes : potentiel, risques, next step}

  → Pour generer la proposition : /prepare {deal_id}
  → Pour l'analyse concurrentielle : /benchmark {deal_id}
═══════════════════════════════════════════════
```

### Fichier cache
Ecrire dans `.cache/deals/{deal_id}/audit.md` le rapport complet.

## Reference

- Processus audit : `agents/audit.md`
- References techniques : `context/references/` (on-demand)
- Performance budget : `context/performance_budget.md`
