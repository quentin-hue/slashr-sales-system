# Mode AUDIT : Diagnostic SEO rapide (v12.0)

> **Prerequis :** `agents/shared.md` lu.

---

## Objectif

Diagnostic SEO rapide du prospect, calibre pour le closing. Pas de proposition HTML, pas de narration. Un rapport factuel qui repond a : "Ce prospect a-t-il un potentiel Search exploitable ?"

---

## Collecte (parallele)

Lancer en parallele :

### Agent 1 : Collector SEO
- `domain_rank_overview` → trafic, keywords, ETV
- `ranked_keywords` (top 30) → split marque/hors-marque, positions
- `competitors_domain` (top 10) → benchmark

### Agent 2 : Collector Website
- robots.txt, sitemap, homepage, 3 pages samples
- Schema JSON-LD, mobile, HTTPS
- **Detection de blocage bot obligatoire** (cf. collector-website.md, Etape 0)

### Agent 3 : Collector GSC (conditionnel)
- Probe d'acces → si OK : performance, queries, pages
- **Si GSC dispo : URL inspection sur la homepage + 1 fiche produit** (source de verite pour schema, indexation, fetch status)
- **Si GSC dispo : list_sitemaps_enhanced** (source de verite pour le sitemap)

---

## Cross-validation post-collecte (OBLIGATOIRE)

Avant de scorer, croiser les resultats du crawl avec les donnees GSC :

### Si `bot_protection == "detected"` dans le crawl :
1. **Tous les findings negatifs du crawl** (pas de sitemap, pas de schema, contenu vide, images sans alt) sont NON VERIFIE
2. **Utiliser GSC comme source de verite** si disponible :
   - GSC sitemaps → sitemap present ou absent ?
   - GSC URL inspection → rich results detectes ? fetch successful ?
3. **Si GSC non disponible** : scorer les dimensions Technical SEO et Content avec la mention `(non verifiable, crawl bloque)` et avertir le closer dans le rapport
4. **Ne jamais conclure "absent"** sur la base d'un seul crawl bloque. Formuler "non detecte par le crawl (protection anti-bot active)"

### Si `bot_protection == "none"` :
Scorer normalement. Les findings du crawl sont fiables.

---

## Grille de scoring (100 points)

### Potentiel de marche (30 pts)
| Signal | Score |
|--------|-------|
| Volume marche adressable > 50K rech/mois | 30 |
| Volume 10-50K | 20 |
| Volume 1-10K | 10 |
| Volume < 1K | 5 |

Bonus +5 si gap vs leader > 5x (grosse marge de progression).

### Technical SEO (20 pts)
| Signal | Points |
|--------|--------|
| HTTPS | 5 |
| Mobile-friendly (viewport) | 5 |
| Sitemap XML present | 4 |
| robots.txt correct (pas de Disallow: /) | 3 |
| Schema JSON-LD present | 3 |

### Content & E-E-A-T (20 pts)
| Signal | Points |
|--------|--------|
| > 100 pages indexees | 8 |
| 10-100 pages | 5 |
| < 10 pages | 2 |
| Contenu unique (pas de thin) | 6 |
| H1 coherents et uniques | 3 |
| Meta descriptions presentes | 3 |

### Benchmark concurrentiel (15 pts)
| Signal | Points |
|--------|--------|
| 3+ concurrents business identifies | 5 |
| Gap trafic > 3x vs leader | 5 |
| Keywords exclusifs concurrent > 50% | 5 |

### GEO / AI Search (10 pts)
| Signal | Points |
|--------|--------|
| llms.txt present | 3 |
| Donnees structurees riches | 4 |
| Contenu citable (FAQ, definitions, listes) | 3 |

### Local (5 pts, conditionnel)
Active si business local detecte (adresse physique, GMB, NAP).
| Signal | Points |
|--------|--------|
| Google Business Profile | 2 |
| NAP coherent | 2 |
| Avis > 4 etoiles | 1 |

---

## Seuils d'interpretation

| Score | Interpretation | Recommandation |
|-------|---------------|----------------|
| >= 70 | Fort potentiel Search | /prepare recommande |
| 40-69 | Potentiel modere, a qualifier | /prepare possible si budget adapte |
| < 40 | Potentiel faible | /prepare deconseille sans elements supplementaires |

---

## Regles

1. **Rapide.** Max 15 appels API au total (DataForSEO + crawl + GSC). Les appels GSC URL inspection comptent dans ce budget mais sont prioritaires sur les appels DataForSEO supplementaires.
2. **Factuel.** Chaque score est justifie par un signal mesurable.
3. **Pas de proposition.** C'est un diagnostic, pas un delivrable client.
4. **Cache reutilise.** Si un /prepare a deja collecte les donnees, les reutiliser.
5. **Enrichit le /prepare.** Le rapport audit est lu par Pass 1 pour accelerer l'analyse.
6. **Niveaux de confiance.** Chaque finding du scoring porte un niveau (VERIFIE / PROBABLE / NON VERIFIE) selon la regle 22 de shared.md. Si un finding est NON VERIFIE (crawl bloque, pas de GSC pour cross-valider), le signaler dans le rapport avec `⚠️` et ne pas le compter comme penalite dans le score. Un score gonfle artificiellement par des faux negatifs de crawl est plus dangereux qu'un score optimiste.
7. **Jamais "absent" sans 2 sources.** Cf. regle 23 de shared.md. "Le crawl ne detecte pas de sitemap" ≠ "il n'y a pas de sitemap".
