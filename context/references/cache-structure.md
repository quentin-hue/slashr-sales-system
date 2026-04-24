# Structure du cache par deal

> Reference pour les analystes. Décrit où trouver les fichiers collectés.

## Arborescence

```
.cache/deals/{deal_id}/
├── pipedrive/
│   ├── deal.json
│   ├── person.json
│   ├── org.json
│   ├── notes.json
│   ├── activities.json
│   └── emails_messages_thread_*.json
├── drive/
│   ├── manifest.json
│   └── files/*.txt
├── dataforseo/
│   └── domain_{domaine}/
│       ├── domain_rank_overview.json
│       ├── ranked_keywords.json.gz
│       ├── keywords_for_site.json
│       ├── competitors_domain.json
│       ├── search_intent.json
│       ├── competitor_*/domain_rank_overview.json
│       └── serps/*.json
├── gsc/
│   ├── gsc_summary.json
│   ├── performance.json
│   ├── queries.json
│   └── pages.json
├── google-ads/
│   └── collection-result.json
├── website/
│   ├── homepage.json
│   ├── sitemap.json
│   ├── sampled_pages.json
│   └── crawl_summary.json
├── analysis/
│   ├── TECHNICAL_ANALYSIS.md
│   ├── CONTENT_ANALYSIS.md
│   ├── COMPETITIVE_ANALYSIS.md
│   └── GEO_ANALYSIS.md (conditionnel)
├── artifacts/
│   ├── SDB.md
│   ├── NBP.md
│   ├── INTERNAL-DIAG.md
│   ├── PROPOSAL-*.html
│   ├── REVIEW-STATE.json
│   └── REVISION-LOG.md
└── evidence/
    └── evidence_log.md
```
