# Extension Google Ads — v2.0

## Manifest
- **Nom** : Google Ads
- **Version** : 2.0
- **MCP Server requis** : `google-ads`
- **Auto-detection** : verifier la presence du MCP server `google-ads` au runtime

## Pre-requis
L'acces aux donnees Google Ads necessite le `customer_id` du compte prospect. Detection :
1. Le closer fournit le customer_id dans le brief ou les notes Pipedrive
2. Sinon, appeler `list_accessible_customers` pour lister les comptes accessibles
3. Si aucun compte accessible → extension inactive pour ce deal

## Capabilities

### Campagnes et budget
- **Campagnes actives** : nom, type (SEARCH, SHOPPING, PERFORMANCE_MAX, DISPLAY), statut, budget
- **Depense totale** : cost_micros par campagne et par periode
- **Strategie d'encheres** : target_cpa, target_roas, maximize_conversions, manual_cpc

### Performance reelle
- **Metriques campagne** : clicks, impressions, ctr, average_cpc, conversions, conversions_value, cost_micros
- **ROAS reel** : conversions_value / cost (par campagne)
- **Quality Score** : quality_info sur les keywords (creative_quality, landing_page_quality, search_predicted_ctr)
- **Impression Share** : search_impression_share, search_budget_lost_impression_share

### Keywords et search terms
- **Keywords achetes** : ad_group_criterion.keyword.text + match_type + quality_score + cpc_bid
- **Search terms reels** : search_term_view → les requetes qui declenchent les annonces
- **Top converters** : search terms avec le plus de conversions

### Shopping (si applicable)
- **Produits** : shopping_product (titre, prix, statut, categorie)
- **Performance produit** : clicks, impressions, conversions par produit

## Priorite
**Google Ads > DataForSEO** pour :
- CPC reels (vs estimations DataForSEO)
- Budget paid reel (vs "il fait du paid" binaire)
- Keywords qui convertissent (vs keywords positionnes)
- ROAS (impossible sans Google Ads)
- Quality Score (impossible sans Google Ads)

## Usage par commande

| Commande | Utilisation |
|----------|------------|
| /audit | Budget mensuel + ROAS global + nb campagnes actives (score signal paid) |
| /prepare Pass 1 | Collecte complete : campagnes, keywords, search terms, quality scores, shopping |
| /benchmark | non utilise (donnees du prospect uniquement) |

## Requetes types (exemples GAQL)

### Budget et performance globale (30 derniers jours)
```
resource: campaign
fields: [campaign.name, campaign.advertising_channel_type, campaign.status, campaign.bidding_strategy_type, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.ctr, metrics.average_cpc, metrics.conversions, metrics.conversions_value, metrics.search_impression_share]
conditions: [campaign.status = ENABLED, segments.date >= '2026-02-25', segments.date <= '2026-03-27']
```

### Keywords avec Quality Score
```
resource: ad_group_criterion
fields: [ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.creative_quality_score, ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.search_predicted_ctr, metrics.clicks, metrics.impressions, metrics.average_cpc, metrics.conversions]
conditions: [ad_group_criterion.type = KEYWORD, ad_group_criterion.status = ENABLED, segments.date >= '2026-02-25', segments.date <= '2026-03-27']
orderings: [metrics.clicks DESC]
limit: 50
```

### Search terms qui convertissent
```
resource: search_term_view
fields: [search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.conversions, metrics.conversions_value, metrics.cost_micros]
conditions: [metrics.conversions > 0, segments.date >= '2026-02-25', segments.date <= '2026-03-27']
orderings: [metrics.conversions DESC]
limit: 30
```

### Impression Share perdue (budget)
```
resource: campaign
fields: [campaign.name, metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share]
conditions: [campaign.status = ENABLED, campaign.advertising_channel_type = SEARCH, segments.date >= '2026-02-25', segments.date <= '2026-03-27']
```

## Comportement si absent
- /prepare : SEA_SIGNAL base sur le brief/notes + DataForSEO (estimations). Pas de donnees reelles.
- /audit : pas d'impact sur le scoring (le paid est un bonus, pas un prerequis)
- Mentionner dans le SDB : "Donnees Google Ads non disponibles. Analyse SEA basee sur les estimations DataForSEO."

## Donnees cles pour le diagnostic

Quand Google Ads est disponible, l'IA peut produire des insights impossibles autrement :

- **"Vous depensez 3 200 EUR/mois en Google Ads avec un ROAS de 1.8. Votre Quality Score moyen est de 4/10, ce qui signifie que vous surpayez chaque clic de 30-50%."**
- **"Vos 5 search terms les plus convertisseurs sont X, Y, Z. Aucun n'est couvert en organique."**
- **"Vous perdez 40% de vos impressions par manque de budget. L'organique pourrait couvrir ces requetes sans cout par clic."**
- **"Vos campagnes Shopping generent 60% de vos conversions mais 80% de votre budget. L'optimisation des fiches produits (SEO) reduirait la dependance paid."**
