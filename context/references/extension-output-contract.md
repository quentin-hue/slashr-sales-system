# Extension Output Contract — v1.0

> Chaque extension (source de donnees) produit des outputs standardises.
> L'analyst-strategy consomme ces outputs, pas les resultats bruts.
> Ajouter une source = implementer ce contrat, pas modifier l'analyseur.

---

## Contrat par extension

### DataForSEO

| Output | Cle | Type | Description |
|--------|-----|------|-------------|
| `organic_overview` | `etv`, `keywords_count`, `top1_count`, `top10_count` | dict | Vue d'ensemble organique |
| `top_keywords` | liste de `{keyword, position, volume, url, intent}` | list[dict] | Top 30 keywords par trafic |
| `competitors` | liste de `{domain, etv, keywords_count, common_keywords}` | list[dict] | Top 10 concurrents organiques |
| `serp_positions` | liste de `{query, position, url, features}` | list[dict] | Positions SERP sur requetes cles |

### GSC (Google Search Console)

| Output | Cle | Type | Description |
|--------|-----|------|-------------|
| `performance_overview` | `clicks`, `impressions`, `ctr`, `position` | dict | Totaux periode |
| `traffic_by_country` | liste de `{country, clicks, impressions, ctr, position}` | list[dict] | Repartition geographique |
| `traffic_by_page` | liste de `{page, clicks, impressions, ctr, position}` | list[dict] | Top pages |
| `top_queries` | liste de `{query, clicks, impressions, ctr, position}` | list[dict] | Top requetes |

### Google Ads

| Output | Cle | Type | Description |
|--------|-----|------|-------------|
| `account_overview` | `cost`, `conversions`, `cpa`, `clicks`, `impressions` | dict | Totaux compte |
| `campaigns` | liste de `{name, type, status, cost, conversions, cpa, bidding_strategy, impression_share}` | list[dict] | Toutes campagnes actives |
| `campaigns_by_country` | liste de `{country, cost, conversions, cpa, pct_budget}` | list[dict] | Repartition par pays |
| `brand_campaigns` | liste de `{name, cost, conversions, cpa}` | list[dict] | Campagnes marque |
| `waste_campaigns` | liste de `{name, cost, conversions, cpa, issue}` | list[dict] | Campagnes identifiees comme gaspillage (CPA > 2x moyenne ou 0-2 conv) |
| `search_terms_top` | liste de `{term, conversions, cost, cpa}` | list[dict] | Top search terms par conversions |

### Pipedrive

| Output | Cle | Type | Description |
|--------|-----|------|-------------|
| `deal` | `title`, `stage`, `value`, `custom_fields` | dict | Donnees deal |
| `contact` | `name`, `email`, `phone` | dict | Contact principal |
| `organization` | `name`, `address`, `website` | dict | Organisation |
| `brief` | `explicit_request`, `priority`, `pain`, `partners`, `verbatims` | dict | Brief extrait (transcript + notes + emails) |

### Drive

| Output | Cle | Type | Description |
|--------|-----|------|-------------|
| `files` | liste de `{name, type, content_summary}` | list[dict] | Fichiers collectes |
| `transcript` | `content` | string | Transcript R1 si disponible |

### Website Crawl

| Output | Cle | Type | Description |
|--------|-----|------|-------------|
| `pages_count` | int | Nombre de pages dans le sitemap |
| `local_pages` | liste de `{url, indexed, schema_type, has_cta}` | list[dict] | Pages locales/centres |
| `schema_types` | liste de types trouves | list[string] | Types de donnees structurees |
| `technical_issues` | liste de `{issue, severity, url}` | list[dict] | Problemes techniques |

---

## Usage dans analyst-strategy

L'analyseur consomme les outputs standardises :

```python
# Pseudo-code
data = load_collector_outputs(deal_id)

# Toujours disponible
deal = data['pipedrive']['deal']
brief = data['pipedrive']['brief']

# Conditionnel
if 'gsc' in data:
    traffic = data['gsc']['performance_overview']
    # GSC > DataForSEO pour le trafic
else:
    traffic = data['dataforseo']['organic_overview']

if 'google_ads' in data:
    ads = data['google_ads']['account_overview']
    waste = data['google_ads']['waste_campaigns']
```

## Ajouter une nouvelle source

1. Creer un dossier `extensions/{nom}/`
2. Ecrire `extension.md` (manifest + capabilities)
3. Ecrire `agent.md` (spec subagent)
4. Implementer les outputs standardises ci-dessus
5. L'analyst-strategy consomme les outputs sans modification
