# Structure du cache — Reference unique

> Tous les subagents (collecteurs, analystes, writers) DOIVENT respecter cette arborescence. Si un fichier n'est pas a l'emplacement prevu, le consommateur ne le trouvera pas.

```
.cache/deals/{deal_id}/
│
├── pipedrive/                          ← Collector Pipedrive
│   ├── deal.json
│   ├── person.json
│   ├── org.json
│   ├── notes.json
│   ├── activities.json
│   └── emails_*.json
│
├── drive/                              ← Collector Drive
│   ├── manifest.json                   (liste des fichiers + types)
│   └── files/
│       ├── {file_id}.txt               (Google Docs exportes)
│       ├── {file_id}.csv               (Google Sheets exportes)
│       ├── {file_id}.pdf               (PDFs telecharges)
│       └── crawl_sf.csv                (CSV Screaming Frog si detecte, type: crawl_sf)
│
├── dataforseo/                         ← Collector SEO
│   ├── domain_rank_overview.json
│   ├── ranked_keywords.json
│   ├── keywords_for_site.json
│   ├── competitors_domain.json
│   ├── domain_intersection_*.json
│   ├── serp_*.json
│   └── geo/                            (si module GEO active)
│       └── *.json
│
├── gsc/                                ← Collector GSC
│   ├── queries.json
│   ├── pages.json
│   ├── devices.json
│   ├── sitemaps.json
│   └── url_inspection_*.json
│
├── google-ads/                         ← Collector Google Ads
│   └── *.json
│
├── website/                            ← Collector Website
│   ├── crawl_summary.json              (resume : bot_protection, crawl_source, sitemap, etc.)
│   ├── robots.txt
│   ├── homepage.json
│   ├── sampled_pages.json              (pages crawlees par archetype)
│   ├── sitemap.json                    (inventaire sitemap par type)
│   └── crawl_sf.csv                    (copie du CSV SF si present dans Drive)
│
├── analysis/                           ← Analystes (Phase A')
│   ├── TECHNICAL_ANALYSIS.md           (analyst-technical)
│   ├── CONTENT_ANALYSIS.md             (analyst-content)
│   ├── COMPETITIVE_ANALYSIS.md         (analyst-competitive)
│   ├── GEO_ANALYSIS.md                 (analyst-geo, conditionnel)
│   ├── SIGNALS_ANALYSIS.md             (analyst-signals, optionnel)
│   ├── CONFRONTATION.md                (confrontation croisee, Etape 1.2a-bis)
│   └── DEVIL_ADVOCATE.md               (devil's advocate, Etape 1.2d)
│
├── artifacts/                          ← Outputs des Passes
│   ├── BRIEF_EXTRACT.md                (Etape 1.1b)
│   ├── SDB.md                          (output Pass 1)
│   ├── INTERNAL-DIAG.md                (output Pass 1, interne closer)
│   ├── NBP.md                          (output Pass 2)
│   ├── PROPOSAL-{date}-{prospect}.html (output Pass 3)
│   ├── REVISION-LOG.md                 (historique des modifications)
│   └── evidence_log.md                 (tracabilite des sources)
│
└── debrief/                            ← Outputs /debrief
    └── DEBRIEF-{date}.md
```

## Regles

1. **Pas d'invention de chemin.** Si un subagent doit ecrire un fichier qui n'est pas dans cette arborescence, il le signale au lieu de creer un chemin ad-hoc.
2. **Noms exacts.** Les noms en MAJUSCULES (TECHNICAL_ANALYSIS.md, SDB.md, etc.) sont des conventions obligatoires. Pas de variantes (technical_analysis.md, Technical-Analysis.md).
3. **Pas de fichier a la racine du deal.** Tout va dans un sous-dossier.
