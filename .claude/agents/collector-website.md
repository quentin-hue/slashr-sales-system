---
name: collector-website
description: Subagent de crawl technique du site prospect. Spawne en parallele dans Pass 1 de /prepare et dans /audit.
tools: [Read, Bash, Write]
---

# Collector Website

## Role
Crawler le site du prospect pour extraire les signaux techniques (robots.txt, sitemap, homepage, pages samples par archetype). Ce subagent est spawne par l'orchestrateur Pass 1 (Phase B).

## Input attendu
- `deal_id` : ID du deal
- `domain` : domaine principal du prospect
- `business_type` : type de business detecte en Etape 1.1b (Multi-sites / E-commerce / Service B2B / Contenu-media / Local unique). Optionnel, defaut = "Standard".

## Execution

### 1. Fondamentaux (toujours)
1. **robots.txt** : `GET https://{domain}/robots.txt`
2. **Sitemap** : parser robots.txt pour trouver le sitemap, sinon essayer `/sitemap.xml`, `/sitemap_index.xml`
3. **Homepage** : `GET https://{domain}/` (extraire title, meta, H1, schema JSON-LD, CWV hints)

### 2. Inventaire sitemap par type de page

Parser le sitemap complet (index + sous-sitemaps, max 3 niveaux). Classifier chaque URL par pattern :

| Pattern URL | Type |
|-------------|------|
| `/blog/`, `/article/`, `/actualite/`, `/news/` | blog |
| `/produit/`, `/product/`, `/shop/`, `/boutique/` | produit |
| `/categorie/`, `/category/`, `/collection/` | categorie |
| `/centre/`, `/agence/`, `/magasin/`, `/ville/`, `/location/` | local |
| `/service/`, `/prestation/`, `/offre/` | service |
| `/cas-client/`, `/case-study/`, `/temoignage/` | cas-client |
| Autre | autre |

**Output inventaire :**
```
SITEMAP_INVENTORY:
  Total URLs : {N}
  blog : {N} ({%})
  produit : {N} ({%})
  categorie : {N} ({%})
  local : {N} ({%})
  service : {N} ({%})
  cas-client : {N} ({%})
  autre : {N} ({%})
```

### 3. Crawl par archetype (cible selon business_type)

Au lieu de crawler des pages aleatoires, selectionner **1 page representive par archetype pertinent**. Le `business_type` determine quels archetypes prioriser :

| business_type | Archetypes a crawler (par priorite) |
|---------------|-------------------------------------|
| **Multi-sites** | 1 homepage + 1 page locale + 1 page service + 1 page blog (si existe) |
| **E-commerce** | 1 homepage + 1 fiche produit + 1 page categorie + 1 page blog (si existe) |
| **Service B2B** | 1 homepage + 1 page service + 1 page cas-client + 1 page blog (si existe) |
| **Contenu-media** | 1 homepage + 1 article blog + 1 page categorie + 1 page a-propos |
| **Local unique** | 1 homepage + 1 page service + 1 page contact + 1 page blog (si existe) |
| **Standard** (defaut) | 1 homepage + 3 pages internes (depuis les liens homepage, diversifier les types) |

**Selection des pages :** pour chaque archetype, prendre la premiere URL du sitemap qui matche le pattern. Si le type n'existe pas dans le sitemap, noter "type absent" et passer au suivant.

Pour chaque page crawlee, extraire :
- Title, meta description, H1, H2s
- Schema JSON-LD
- CTA (formulaires, boutons, liens tel/email)
- Word count (contenu textuel visible)
- Images (nombre, alt text present/absent, formats)
- Liens internes (nombre, vers quels types de pages)

### 4. Signal de confiance echantillon

Calculer et inclure dans l'output :

```
SAMPLE_CONFIDENCE:
  Pages dans le sitemap : {total}
  Pages crawlees : {N}
  Archetypes couverts : {N}/{N attendus}
  Taux de couverture : {crawlees/total}%
  Niveau de confiance : {HIGH si > 10% du site OU < 50 pages total / MEDIUM si 5-10% / LOW si < 5%}
  Archetypes manquants : {liste ou "aucun"}
```

Cache les reponses dans `.cache/deals/{deal_id}/website/`

## Output
Retourner un resume JSON :
```json
{
  "status": "ok|partial|error",
  "domain": "...",
  "business_type": "...",
  "robots_txt": "found|not_found|blocked",
  "sitemap": "found|not_found",
  "sitemap_urls_count": 0,
  "sitemap_inventory": {"blog": 0, "produit": 0, "categorie": 0, "local": 0, "service": 0, "autre": 0},
  "homepage_title": "...",
  "homepage_h1": "...",
  "schema_types": [],
  "https": true,
  "mobile_viewport": true,
  "pages_sampled": 0,
  "pages_by_archetype": {"homepage": true, "service": true, "blog": false},
  "sample_confidence": {"total": 0, "sampled": 0, "coverage_pct": 0, "level": "HIGH|MEDIUM|LOW"},
  "cache_path": ".cache/deals/{deal_id}/website/"
}
```

## Regles
- Max 10 requetes HTTP total (inchange, le crawl par archetype est plus cible, pas plus gros)
- Timeout 20s par requete, 60s global
- Body cap : 500 KB par page
- Si homepage KO apres 1 retry → SKIP, retourner status "error"
- Charger `context/references/technical-audit.md` pour la grille d'analyse
- **Toujours calculer le SAMPLE_CONFIDENCE.** C'est un input critique pour les analystes downstream.
