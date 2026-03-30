---
name: collector-google-ads
description: Subagent de collecte Google Ads (conditionnel). Spawne en parallele dans Pass 1 de /prepare.
tools: [Read, Bash, Write]
---

# Collector Google Ads

## Role
Collecter les donnees Google Ads reelles du prospect si l'acces est disponible. Ce subagent est spawne par l'orchestrateur Pass 1.

## Input attendu
- `deal_id` : ID du deal
- `prospect_name` : nom de l'entreprise (pour matcher dans les comptes)
- `gads_customer_id` : customer ID Google Ads (si renseigne dans Pipedrive, field key `2389e066f59aa6dae4edb9903557fdec7924426a`, format "475-819-4195")

## Execution

### Phase 0 : Detecter le compte Google Ads (OBLIGATOIRE)

**Priorite 1 : champ Pipedrive `gads_customer_id`**
Si le champ est renseigne dans le deal Pipedrive → utiliser directement (retirer les tirets : "475-819-4195" → "4758194195"). C'est la source la plus fiable.

**Priorite 2 : exploration du MCC (fallback)**
Si le champ n'est pas renseigne :
1. Pour le customer_id MCC SLASHR (`1468186390`) : appeler `search` sur la ressource `customer_client` pour lister les sous-comptes :
   ```
   resource: customer_client
   fields: [customer_client.id, customer_client.descriptive_name, customer_client.status]
   customer_id: 1468186390
   ```
2. Chercher dans les sous-comptes un nom qui matche le prospect (match partiel, case-insensitive)
3. Si aucun match → Google Ads non disponible pour ce deal

### Phase 1 : Collecte (si compte trouve)

L'IA choisit les requetes pertinentes. Axes disponibles :

**Axe 1 : Vue globale (30 derniers jours)**
```
resource: campaign
fields: [campaign.name, campaign.advertising_channel_type, campaign.status, campaign.bidding_strategy_type, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.ctr, metrics.average_cpc, metrics.conversions, metrics.search_impression_share]
conditions: [campaign.status = ENABLED, segments.date >= '{30j_ago}', segments.date <= '{yesterday}']
orderings: [metrics.cost_micros DESC]
limit: 20
```

**Axe 2 : Quality Score (top keywords)**
```
resource: ad_group_criterion
fields: [ad_group_criterion.keyword.text, ad_group_criterion.quality_info.quality_score, metrics.clicks, metrics.impressions, metrics.average_cpc, metrics.conversions]
conditions: [ad_group_criterion.type = KEYWORD, ad_group_criterion.status = ENABLED, segments.date >= '{30j_ago}', segments.date <= '{yesterday}']
orderings: [metrics.clicks DESC]
limit: 30
```

**Axe 3 : Search terms convertisseurs**
```
resource: search_term_view
fields: [search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.conversions, metrics.cost_micros]
conditions: [metrics.conversions > 0, segments.date >= '{30j_ago}', segments.date <= '{yesterday}']
orderings: [metrics.conversions DESC]
limit: 20
```

### Phase 2 : Calculs derives
- Depense mensuelle totale (cost_micros / 1 000 000)
- CPC moyen global
- CVR global (conversions / clics)
- CPA moyen (depense / conversions)
- Impression share moyenne sur les campagnes Search
- Nombre de campagnes par type (Search, PMax, Display, etc.)

## Output
```json
{
  "status": "ok|not_available",
  "customer_id": "...",
  "customer_name": "...",
  "global": {
    "total_spend_monthly": 0,
    "total_clicks": 0,
    "total_conversions": 0,
    "avg_cpc": 0,
    "cvr_pct": 0,
    "cpa": 0,
    "campaign_count": 0,
    "campaign_types": {}
  },
  "impression_share": {
    "avg_search_impression_share": 0,
    "budget_limited_campaigns": 0
  },
  "cache_path": ".cache/deals/{deal_id}/google-ads/"
}
```

## Regles
- **TOUJOURS explorer le MCC d'abord** (customer_id `1468186390`). Ne jamais deviner le customer_id.
- Google Ads > DataForSEO pour CPC, budget, conversions, ROAS, quality score
- Les montants sont en micros (÷ 1 000 000 pour EUR)
- Cache sous `.cache/deals/{deal_id}/google-ads/`
- Timeout 20s par requete
- Ne JAMAIS afficher le customer_id dans les outputs clients
