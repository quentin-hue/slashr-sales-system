# Extension DataForSEO

## Manifest
- **Nom** : DataForSEO
- **Version** : 1.0
- **MCP Server requis** : `dataforseo`
- **Auto-detection** : verifier la presence du MCP server `dataforseo` au runtime

## Capabilities
- domain_rank_overview : vue d'ensemble trafic/keywords
- ranked_keywords : keywords positionnes
- keywords_for_site : opportunites keywords
- competitors_domain : concurrents semantiques
- domain_intersection : keywords communs/exclusifs
- serp_organic_live_regular : SERPs live
- search_intent : classification intent
- bulk_keyword_difficulty : difficulte keywords

## Usage par commande

| Commande | Endpoints utilises |
|----------|-------------------|
| /audit | domain_rank_overview, ranked_keywords (top 30), competitors_domain |
| /prepare Pass 1 | Tous (lots 1-5 selon modules actifs) |
| /benchmark | domain_rank_overview, competitors_domain, domain_intersection, ranked_keywords |

## Configuration
- Batch tool : `tools/batch_dataforseo.py`
- Cache : `.cache/deals/{deal_id}/dataforseo/`
- Performance budget : cf. `context/performance_budget.md`

## Comportement si absent
Si le MCP server `dataforseo` n'est pas disponible :
- /audit : score Potentiel de marche = 0 (donnees insuffisantes), WARN dans le terminal
- /prepare : continuer sans les modules SEO, mentionner dans le SDB
- /benchmark : STOP (impossible sans donnees concurrentielles)
