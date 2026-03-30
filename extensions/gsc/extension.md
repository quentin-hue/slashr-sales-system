# Extension Google Search Console — v2.0

## Manifest
- **Nom** : Google Search Console
- **Version** : 2.0
- **MCP Server requis** : `gsc`
- **Auto-detection** : verifier la presence du MCP server `gsc` au runtime
- **Credentials** : `~/.google_service_account.json` (meme service account que Drive)

## Capabilities

### Donnees de performance (existant)
- `get_search_analytics` : clics, impressions, CTR, positions reels
- Dimensions : query, page, device, country, date
- Quick wins detection : position 5-20, impressions > 100/mois, CTR < 5%

### Inspection d'URLs (NOUVEAU v2.0)
- `inspect_url_enhanced` : statut d'indexation, rich results, crawl mobile d'une URL
- `batch_url_inspection` : inspection batch de N URLs (10-20 pages strategiques)
- `check_indexing_issues` : detection de problemes d'indexation sur un lot d'URLs

### Sitemaps (NOUVEAU v2.0)
- `get_sitemaps` : liste des sitemaps, URLs soumises vs indexees, dernier crawl
- `get_sitemap_details` : detail d'un sitemap specifique

### Proprietes
- `list_properties` : lister les sites auxquels le service account a acces
- `get_site_details` : detail d'une propriete (type, permissions)

## Priorite
**GSC > DataForSEO** pour : trafic, positions, CTR, split marque/hors-marque, indexation.
DataForSEO reste exclusif pour : volumes de marche, concurrents, keyword difficulty.

## Usage par commande

| Commande | Endpoints utilises |
|----------|-------------------|
| /audit | probe + performance + queries + sitemaps + batch_url_inspection (5-10 pages cles) |
| /prepare Pass 1 | probe + performance + queries + pages + sitemaps + inspect_url (homepage + top pages) + check_indexing_issues |
| /benchmark | non utilise |

## Donnees cles exploitables

### Performance (search_analytics)
- Trafic organique reel (clics/mois)
- Split marque / hors-marque (par query)
- Positions moyennes reelles
- CTR par position (benchmark interne)
- Quick wins (position 5-20, fort potentiel)
- Evolution mois par mois (si dimensions: date)

### Indexation (URL inspection)
- Pages indexees vs non indexees parmi les pages strategiques
- Raisons de non-indexation (crawled not indexed, noindex, redirect, etc.)
- Compatibilite mobile (erreurs mobile-first)
- Rich results detectes (FAQ, Product, Article, etc.)
- Dernier crawl par Googlebot (date + type : mobile/desktop)

### Sitemaps
- Ratio URLs soumises / URLs indexees (gap = probleme d'indexation ou de qualite)
- Derniere date de soumission
- Erreurs de sitemap

## Comportement si absent
- Fallback performance : chercher un export GSC dans les fichiers Drive
- Fallback indexation : utiliser les donnees DataForSEO (on_page_instant_pages) comme proxy
- Fallback sitemaps : crawler le sitemap directement (Module 11)
- Si aucun fallback : continuer avec DataForSEO seul, Confidence: Medium
