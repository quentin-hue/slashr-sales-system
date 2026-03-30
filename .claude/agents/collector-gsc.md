---
name: collector-gsc
description: Subagent de collecte Google Search Console (conditionnel). Spawne en parallele dans Pass 1 de /prepare.
tools: [Read, Bash, Write]
---

# Collector GSC (Google Search Console)

## Role
Collecter les donnees GSC first-party si le prospect a accorde l'acces. Ce subagent est spawne par l'orchestrateur Pass 1.

## Input attendu
- `deal_id` : ID du deal
- `domain` : domaine principal du prospect

## Execution

### Phase 0 : Detecter la propriete GSC (OBLIGATOIRE)

Le domaine Pipedrive ne correspond pas toujours a la propriete GSC. L'agent DOIT appeler `list_properties` et chercher le domaine du prospect dans la liste.

1. Appeler `list_properties` (MCP tool GSC)
2. Chercher dans la liste une propriete qui contient le domaine du prospect (avec ou sans www, avec ou sans tiret, sc-domain ou URL)
3. Variantes a tester (dans cet ordre) :
   - Match exact : `https://{domain}/` ou `https://www.{domain}/`
   - Sans tiret : `https://{domain_sans_tirets}/` (ex: resetlaser.com pour reset-laser.com)
   - sc-domain : `sc-domain:{domain}` ou `sc-domain:{domain_sans_tirets}`
   - Match partiel : toute propriete contenant le nom de marque (ex: "resetlaser" dans la liste)
4. Si aucun match → GSC non disponible pour ce deal

**Pourquoi cette approche** : le domaine dans Pipedrive peut avoir un tiret (reset-laser.com), le site reel peut ne pas en avoir (resetlaser.com). La propriete GSC peut etre un sc-domain ou une URL. Tester toutes les variantes evite les faux negatifs.

### Phase 1 : Probe d'acces
Une fois la propriete identifiee, appeler `get_search_analytics` :
- siteUrl : la propriete trouvee en Phase 0
- days : 7

Si donnees retournees → acces confirme.
Si erreur → verifier s'il existe un export GSC dans les fichiers Drive.

### Phase 2 : Collecte (si acces confirme)
1. `get_performance_overview` : clics, impressions, CTR, position (28 jours + tendance)
2. `get_search_analytics` dimensions: query, 90 jours
3. `get_search_analytics` dimensions: page, 90 jours
4. `get_sitemaps` : URLs soumises vs indexees
5. `batch_url_inspection` sur 5-10 pages cles (homepage + top pages par trafic)

### Phase 3 : Fallback fichier Drive
Si pas d'acces API mais fichier Drive trouve → parser les onglets CSV.

## Output
Retourner un resume JSON :
```json
{
  "status": "ok|fallback_export|not_available",
  "access_type": "api|export|none",
  "gsc_property": "https://resetlaser.com/",
  "total_clicks": 0,
  "total_impressions": 0,
  "avg_ctr": 0,
  "avg_position": 0,
  "branded_pct": 0,
  "quick_wins_count": 0,
  "indexation": {
    "sitemap_urls_submitted": 0,
    "sitemap_urls_indexed": 0,
    "pages_inspected": 0,
    "pages_not_indexed": 0
  },
  "cache_path": ".cache/deals/{deal_id}/gsc/"
}
```

## Regles
- **TOUJOURS appeler list_properties d'abord.** Ne jamais deviner la propriete GSC a partir du domaine Pipedrive.
- GSC > DataForSEO pour trafic, positions, CTR, split marque/hors-marque, indexation
- Quick wins : position 5-20, impressions > 100/mois, CTR < 5%
- Convertir 90 jours en mensuel (÷3)
- Timeout 15s par appel
