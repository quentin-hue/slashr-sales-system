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

### 0. Detection de blocage bot (OBLIGATOIRE, avant tout)

Avant de lancer le crawl, tester si le site bloque les bots non-navigateur :

1. `GET https://{domain}/` avec un User-Agent standard
2. Verifier la reponse :
   - **Body < 2 KB** ET contient `challenge`, `captcha`, `cf-`, `__cf_bm`, `AES`, `decrypt`, `cookie` → **BOT_BLOCKED**
   - **Redirect vers une URL avec parametre crypto** (ex: `?c4dbf5544f66252c3efc189c4eabe16e=1`) → **BOT_BLOCKED**
   - **Status 403/503** avec body Cloudflare/Akamai/Incapsula → **BOT_BLOCKED**
   - Sinon → **BOT_OK**

**Si BOT_BLOCKED :**
- Flagger `bot_protection: "detected"` dans l'output JSON
- Continuer le crawl normalement MAIS ajouter un warning sur CHAQUE finding :
  `⚠️ BOT_BLOCKED: ce resultat peut etre un artefact du blocage anti-bot. Cross-validation GSC requise.`
- Les findings d'un crawl BOT_BLOCKED sont automatiquement NON VERIFIE (cf. regle 22 de shared.md)
- Inclure dans l'output : `"bot_protection_warning": "Cloudflare/WAF detecte. Tous les findings techniques de ce crawl doivent etre cross-valides via GSC URL inspection avant utilisation dans le diagnostic client."`

### 1. Fondamentaux (toujours)
1. **robots.txt** : `GET https://{domain}/robots.txt`. Si la reponse contient du HTML/JS au lieu de directives robots.txt → noter `robots_txt: "blocked_by_waf"` (pas "not_found")
2. **Sitemap** : parser robots.txt pour trouver le sitemap, sinon essayer `/sitemap.xml`, `/sitemap_index.xml`. **Aussi verifier via GSC** (`mcp__gsc__list_sitemaps_enhanced`) si la propriete est accessible. Le sitemap peut exister a un chemin non standard (ex: `/media/sitemaps/`) et etre soumis dans GSC sans etre dans robots.txt.
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
  "bot_protection": "none|detected",
  "bot_protection_warning": "...",
  "robots_txt": "found|not_found|blocked_by_waf",
  "sitemap": "found|not_found|found_via_gsc_only",
  "sitemap_source": "robots_txt|direct_url|gsc|not_found",
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
