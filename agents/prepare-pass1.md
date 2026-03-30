# PASS 1 : DATA & STRATEGY ENGINE

> **Prerequis :** `agents/shared.md` lu, puis `agents/prepare.md` (router).

## Role

Collecter, structurer, analyser. Produire un document intermediaire factuellement complet. **Aucune decision narrative ni visuelle dans cette passe.**

---

## Etape 1.1 : Collecte (10 modules)

### Modules toujours actifs

#### Module 1 : Pipedrive

> **Execution :** via `python3 tools/batch_pipedrive.py --deal-id {deal_id}`. Ne pas appeler endpoint par endpoint.

L'outil batch collecte en parallele (5 workers) :
- Deal (titre, stage, montant, custom fields dont decideur_level)
- Contact (prenom, nom, email, telephone)
- Organisation (nom, adresse, website)
- Notes chronologiques
- Activites (calls, meetings, taches)
- **Emails** : 12 pages en parallele (6 inbox + 6 sent) → filtre par deal_id → messages des threads matches

**Procedure :**
1. Executer `python3 tools/batch_pipedrive.py --deal-id {deal_id}`
2. Lire le JSON stdout (summary avec cache_paths)
3. Lire les fichiers cache dans `.cache/deals/{deal_id}/pipedrive/` pour exploiter les donnees

#### Module 2 : Drive

> **Execution :** via `python3 tools/batch_drive.py --deal-id {deal_id} --folder-url {dossier_r1_link}`. Ne pas telecharger fichier par fichier.

L'outil batch liste recursivement (3 niveaux) et telecharge en parallele (3 workers) :
- Exclure les outputs systeme (`DEAL-*`, `DECK-*`, `PROPOSAL-*`, `INTERNAL-*`)
- Limite : 25 fichiers max (plus recents si depassement)
- Telecharger et typer chaque fichier (transcript, notes_closer, document_prospect, document)
- Concatener avec marqueurs `=== SOURCE: {nom} (type: {type}) ===`

**Procedure :**
1. Extraire le folder ID depuis `dossier_r1_link`
2. Executer `python3 tools/batch_drive.py --deal-id {deal_id} --folder-id {folder_id}`
3. Lire le JSON stdout, puis les fichiers `.cache/deals/{deal_id}/drive/files/*.txt`

#### Etape 1.1b : Cartographie des domaines (OBLIGATOIRE avant Module 3)

Apres collecte Pipedrive (Module 1) et Drive (Module 2), l'agent identifie et classe TOUS les domaines mentionnes dans les sources. Cette etape est un prerequis au Module 3 : aucun appel DataForSEO ne peut etre lance sans domaine principal confirme.

**Etape 1 : Extraire tous les domaines**
Scanner toutes les sources collectees :
- Champ `website` de l'organisation Pipedrive
- URLs mentionnees dans les notes R1, complement-info-client, brief, transcript
- Domaines mentionnes dans les emails Pipedrive
- Domaines dans le titre du deal ou les custom fields

**Etape 2 : Classifier chaque domaine**

| Role | Definition | Exemple |
|------|-----------|---------|
| **PRINCIPAL** | Le site actif ou le prospect opere et vend aujourd'hui. C'est le domaine a analyser. | biscuiterie-mere-poulard.com |
| **SECONDAIRE** | Ancien domaine, domaine cible de migration, ou domaine d'une entite liee | biscuiterie-de-kerlann.com |
| **TIERS** | Domaine d'une autre entite du groupe, sans rapport direct avec le perimetre | lamerepoulard.com (hotel) |

**Regles de classification :**
1. Le domaine PRINCIPAL est celui mentionne comme **le site du prospect** dans les notes R1 ou le brief, pas un ancien domaine ni un domaine cible de migration future
2. Si une URL complete (`https://www.example.com/`) est donnee dans les notes R1 ou le brief comme reference du site actuel, c'est le PRINCIPAL
3. En cas de migration, le domaine SOURCE actuel (celui qui a le trafic aujourd'hui) est PRINCIPAL, le domaine CIBLE est SECONDAIRE, sauf si les notes indiquent que le domaine CIBLE est deja le site actif
4. Le champ `website` de l'org Pipedrive prime sur les autres sources SAUF si les notes R1 contredisent explicitement

**Etape 3 : Confirmer**
- Si 1 seul domaine detecte → PRINCIPAL par defaut
- Si 2+ domaines detectes ET le PRINCIPAL est clair (regle 1-4) → continuer
- Si 2+ domaines detectes ET ambiguite → **STOP : demander au closer** "Quel est le site actif du prospect ? Domaines detectes : {liste avec contexte de chaque mention}"

**Output :** Ajouter les champs `DOMAINE_PRINCIPAL` et `DOMAINES_SECONDAIRES` au debut du SDB (voir template SDB ci-dessous).

#### Module 3 : SEO

> **Execution :** via batch (voir "Strategie d'execution DataForSEO : batch parallele" ci-dessous). Ne pas appeler endpoint par endpoint.

Pour chaque domaine detecte :

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `domain_rank_overview` | Trafic organique, nb mots-cles, ETV | Vue d'ensemble perf actuelle |
| `ranked_keywords` (top 30) | Keywords, positions, volumes, type marque/generique | Ce sur quoi le prospect se positionne et ce qu'il rate |
| `keywords_for_site` (top 20) | Keywords pertinents que le domaine pourrait cibler | Opportunites manquees |

**Regle SDB thin (ranked_keywords) :** le SDB ne contient que le **top 10 keywords** + statistiques agregees (total keywords, split marque/hors-marque, volume total). Le dump complet reste dans le cache (`.cache/deals/{deal_id}/dataforseo/`) et dans l'evidence log. Ne jamais injecter les 30+ keywords dans le SDB.

#### Module 3b : GSC (Google Search Console) — TOUJOURS TENTER

**TOUJOURS appeler `list_properties` (MCP GSC) pour chercher le prospect dans les proprietes accessibles.** Ne jamais deviner la propriete a partir du domaine Pipedrive : le domaine CRM peut avoir un tiret, le site reel non. La propriete GSC peut etre un sc-domain ou une URL.

**Detection (cf. `.claude/agents/collector-gsc.md` Phase 0) :**
1. `list_properties` → chercher le domaine du prospect (match exact, sans tiret, partiel par nom de marque)
2. Si propriete trouvee → probe `get_search_analytics` sur cette propriete
3. Si aucune propriete → fallback fichier Drive

**Pourquoi toujours tenter :** les donnees GSC changent completement le diagnostic. Sans GSC, on peut croire qu'un site a 0 trafic organique alors qu'il en a 13 500 clics/mois.

#### Module 3c : Google Ads — TOUJOURS TENTER

**Priorite 1 :** lire le champ `gads_customer_id` du deal Pipedrive (field key `2389e066f59aa6dae4edb9903557fdec7924426a`). Si renseigne → utiliser directement (retirer les tirets).

**Priorite 2 (fallback) :** explorer le MCC SLASHR (`1468186390`) via `search` resource `customer_client` → chercher un nom qui matche le prospect.

**Detection (cf. `.claude/agents/collector-google-ads.md` Phase 0) :**
1. Champ Pipedrive `gads_customer_id` → customer_id direct
2. Sinon : lister les sous-comptes du MCC, matcher par nom
3. Si compte trouve → collecter les donnees (campagnes, depenses, conversions, CPA)

**Pourquoi toujours tenter :** les donnees Google Ads reelles (CVR 4.4%, CPA 19.8 EUR) sont incomparablement plus precises que les estimations DataForSEO. Elles permettent de calculer un ROI reel et de credibiliser la proposition.

**Fallback fichier Drive (si pas d'acces API GSC) :**

Chercher dans les fichiers Drive deja collectes (Module 2) un export GSC :
- Nom de fichier contenant "GSC" ou "Search Console" (insensible a la casse)
- OU fichier Google Sheets avec onglets nommes "query" ou "page"

Si un fichier correspond → parser les onglets CSV (separes par marqueurs `=== ONGLET: ... ===`) :
- **Onglet "query"** (ou nom similaire : "Queries", "Requetes") : colonnes `query`, `clicks`, `impressions`, `ctr`, `position`
- **Onglet "page"** (ou nom similaire : "Pages", "URL") : colonnes `page`, `clicks`, `impressions`, `ctr`, `position`
- **Onglet "query/page"** (optionnel, ou "Query+Page") : combinaisons query+page

Calculer les memes metriques que l'API :
- Clics / impressions / CTR / position agreges (somme pour clics/impressions, moyenne ponderee par impressions pour CTR et position)
- Split marque / hors-marque (requetes contenant le nom de marque du prospect → marque, le reste → hors-marque)
- Quick wins : position 5-20, impressions > 100/mois (ajuster au prorata si export ≠ 12 mois), CTR < 5%
- Top 10 queries hors-marque (par clics decroissants)
- Top 10 pages (par clics decroissants)

**Si trouve :**
- Ecrire `GSC_ACCESS: YES (EXPORT)` dans le SDB
- Taguer les donnees `[src: gsc-export]` (au lieu de `[src: gsc]`)
- Les regles de priorite GSC > DataForSEO s'appliquent identiquement
- Impact ROI : `Confidence: Medium-High` (donnees reelles mais potentiellement moins fraiches que l'API)
- Source affichee dans le HTML : "Source: Google Search Console (export)"

**Si aucun fichier trouve :** Ecrire `GSC_ACCESS: NO` dans le SDB et continuer sans ce module.

**Collecte API (3 appels MCP, sequentiels) — si acces API confirme :**

| Requete | Parametres | Objectif |
|---------|-----------|----------|
| Performance globale | dimensions: aucune, 90 derniers jours | Clics, impressions, CTR, position moyenne reels |
| Top queries | dimensions: `query`, rowLimit: 500, detectQuickWins: true | Split marque/hors-marque exact, quick wins |
| Top pages | dimensions: `page`, rowLimit: 100 | Pages performantes, contenu a optimiser |

**Periode :** 90 derniers jours (endDate = hier, startDate = J-90).

**Quick wins GSC :** requetes en position 5-20, impressions > 100/mois, CTR < 5%. Ce sont des gains rapides : le site est deja visible, il suffit d'optimiser le titre/meta pour augmenter le CTR.

**Cache :** ecrire les reponses brutes dans `.cache/deals/{deal_id}/gsc/` :
- `performance.json` (requete 1)
- `queries.json` (requete 2)
- `pages.json` (requete 3)

**Regle SDB thin :** le SDB contient les metriques agregees + top 10 queries + top 10 pages. Le dump complet reste dans le cache.

**Regle de priorite (GSC > DataForSEO) :** quand les deux sources sont disponibles :

| Metrique | Source prioritaire | Raison |
|----------|-------------------|--------|
| Trafic organique (visites/mois) | **GSC** (clics reels) | Mesure directe vs estimation |
| Split marque / hors-marque | **GSC** (par requete) | Exact vs heuristique |
| Positions moyennes | **GSC** (ponderee) | Moyenne reelle vs snapshot |
| CTR | **GSC** (exclusif) | DataForSEO ne fournit pas de CTR |
| Volumes de recherche (marche) | **DataForSEO** (exclusif) | GSC ne montre que les impressions du site |
| Concurrents | **DataForSEO** (exclusif) | GSC ne couvre pas la concurrence |
| Keyword difficulty | **DataForSEO** (exclusif) | Absent de GSC |
| ETV | **DataForSEO** (exclusif) | Proxy budget Ads, absent de GSC |

**Impact sourcing :** donnees GSC → `[src: gsc]`. Source affichee dans le HTML : "Source: Google Search Console" (au lieu de "Source: DataForSEO").

**Impact ROI :** si GSC disponible, l'hypothese H1 (trafic actuel) passe de `Confidence: Medium` a `Confidence: High` (donnee mesuree directement).

#### Module 4 : Benchmark (concurrents semantiques)

> **Execution :** via batch (voir "Strategie d'execution DataForSEO : batch parallele" ci-dessous). Ne pas appeler endpoint par endpoint.

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `competitors_domain` (top 10) | Concurrents Search du prospect | Identifier qui capte le trafic |
| `domain_rank_overview` x top 3 concurrents | Trafic, keywords, ETV de chaque concurrent | Chiffrer le gap et le potentiel |
| `domain_intersection` (prospect vs top concurrent) | Keywords communs + keywords exclusifs au concurrent | Ce que le prospect perd precisement |

**Filtrage obligatoire des resultats `competitors_domain` :**
L'endpoint remonte les domaines par intersection de keywords, ce qui favorise les gros sites generiques. Avant d'utiliser ces resultats, classifier chaque domaine :

| Type | Definition | Exemples | Usage |
|------|-----------|----------|-------|
| **Concurrent business** | Meme secteur, meme offre, meme cible | tourniayre.com, maisondubiscuit.fr | Benchmark principal, gap analysis |
| **Concurrent semantique** | Capte les memes keywords mais ne vend pas le meme produit | ouest-france.fr, carrefour.fr, amazon.fr | Contexte ("qui prend le trafic"), pas benchmark |
| **Bruit** | Reseaux sociaux, annuaires, Wikipedia | facebook.com, pagesjaunes.fr, wikipedia.org | Ignorer |

Si `competitors_domain` ne remonte **aucun concurrent business** (cas frequent pour les niches artisanales), declencher le **Module 4c** ci-dessous.

#### Module 4c : Detection concurrents de niche (conditionnel)

**Activer si :** le Module 4 ne remonte aucun concurrent business (= que du semantique et du bruit).

**Objectif :** trouver les vrais concurrents en analysant les SERPs des keywords commerciaux du prospect, puis construire le Total Addressable Search Market (TASM).

**Etape 1 :** Selectionner 5-8 keywords commerciaux cles
- Prendre les top keywords hors-marque du prospect (issus du Module 3 `ranked_keywords`)
- Completer avec 3-5 keywords sectoriels evidents (ex: "{produit} artisanal", "{produit} en ligne", "coffret {produit}")
- Privilegier les keywords a intent commercial/transactionnel

**Etape 2 :** Analyser les SERPs
- Appeler `serp_organic_live_regular` sur chaque keyword (location: France, language: fr)
- Pour chaque SERP, extraire les domaines en top 20
- Compter les apparitions de chaque domaine sur l'ensemble des SERPs

**Etape 3 :** Identifier les concurrents business
- Un domaine qui apparait sur 2+ SERPs commerciaux et qui vend un produit comparable = concurrent business
- Exclure les marketplaces (amazon, cdiscount), les retailers generiques (carrefour, leclerc), les annuaires, les medias
- Garder les **sites de marque ou fabricant du meme secteur**
- **Pas de limite** sur le nombre de concurrents identifies — lister tous ceux qui passent le filtre

**Etape 4 :** Deep-dive sur les top 5 concurrents business (par nombre d'apparitions SERP)
- `domain_rank_overview` sur chacun des 5 → trafic, keywords, ETV
- `ranked_keywords` (top 50) sur chacun des 5 → univers keyword de chaque concurrent
- `domain_intersection` (prospect vs top 1 concurrent business) → gap detaille

**Etape 5 :** Construire le TASM (Total Addressable Search Market)

Le TASM est l'union dedupliquee des keywords de tous les concurrents business + le prospect.

1. Collecter les `ranked_keywords` du prospect (Module 3) + des top 5 concurrents (Etape 4)
2. Dedupliquer par keyword exact
3. Sommer les volumes de recherche uniques
4. Segmenter par intent (commercial / info captable / info non-captable) via Module 4b

```
TASM (Total Addressable Search Market) :
- Sources : {prospect} + {N} concurrents business (Module 4c)
- Keywords uniques (brut avant filtrage) : {N_brut} (stocke dans evidence log uniquement)
- Keywords retenus (filtre secteur) : {N_filtre} (methode: {ne retenir que les kw ou prospect OU concurrent business apparait en top 50})
- Volume filtre : {X_filtre} recherches/mois
  - Commercial : {Y} recherches/mois ({%})
  - Informationnel captable : {Z} recherches/mois ({%})
  - Non-captable : {W} recherches/mois (ecarte du total)
- Marche captable : {Y+Z} recherches/mois
- Part actuelle du prospect : {trafic hors-marque prospect} / {Y+Z} = {%}
- Gap : {Y+Z - trafic hors-marque prospect} recherches/mois non captees
```

**Regle :** le TASM est la reference unique pour chiffrer le potentiel dans la proposition. Interdiction d'utiliser un seul keyword comme proxy du marche (ex: "40 000+ recherches/mois" base sur "biscuits" seul). Le chiffre affiche dans la proposition = le TASM captable, pas un keyword isole.

**Regle TASM filtre obligatoire :** le TASM affiche dans le SDB DOIT etre filtre par pertinence sectorielle et segmente par intent. Le volume brut (avant filtrage) est stocke dans l'evidence log sous `tasm_raw_volume` avec la note "NON FILTRE, pour reference uniquement". Le SDB ne contient JAMAIS le volume brut non filtre. Si le filtrage automatique est impossible (pas assez de donnees), l'agent applique un filtre conservateur (ne retenir que les keywords ou le prospect OU un concurrent business apparait en top 50) et documente la methode dans l'evidence log.

**Etape 6 :** Integrer dans le SDB

**Output `COMPETITIVE_GAP` :**
```
CONCURRENTS BUSINESS (Module 4c — detection SERP) :
- {domaine1} : {N} apparitions SERP, {trafic}, {keywords}, top 3 kw exclusifs
- {domaine2} : ...
- {domaine3} : ...
(tous les concurrents business identifies, deep-dive sur top 5)
Methode : analyse SERP sur {N} keywords commerciaux

TASM : {X} recherches captables/mois (commercial + info captable)
Part prospect : {%} | Gap : {Y} recherches/mois
```

**Regle :** si le Module 4c identifie des concurrents business, ceux-ci REMPLACENT les concurrents semantiques comme reference de benchmark dans le gap analysis et le bar chart. Les concurrents semantiques restent mentionnes en contexte ("qui capte le trafic aujourd'hui") mais ne servent pas de reference pour le gap chiffre.

#### Budget checkpoint (obligatoire apres Module 4 + 4c)

Apres l'execution des modules de benchmark (4 + 4c si active), l'agent evalue sa consommation DataForSEO :

| Seuil | Appels consommes | Action |
|-------|-----------------|--------|
| **Normal** | < 15 appels | Continuer normalement (modules 4b, 5-10 si pertinents) |
| **Attention** | 15-25 appels | Modules conditionnels (5-10) : activer uniquement ceux avec signal FORT (mention explicite dans le brief/transcript, pas juste une inference) |
| **Critique** | > 25 appels | Modules conditionnels (5-10) : activer max 2, privilegier ceux qui alimentent la contrainte principale. Les autres → marquer dans le SDB : "Module {N} non active (budget API consomme, data insuffisante)" |

Ce checkpoint est informatif, pas un hard stop. L'objectif est d'eviter les deals ou 40+ appels DataForSEO sont faits alors que 20 suffisaient.

**Comptage typique Module 4c :** `serp_organic_live_regular` x5-8 + `domain_rank_overview` x5 + `ranked_keywords` x5 + `domain_intersection` x1 = 16-19 appels.

#### Module 4b : Segmentation intent du marche

**Toujours actif.** Apres le benchmark (Module 4 + 4c si active), l'agent segmente les keywords du marche par intention de recherche.

**Etape 1 :** Constituer la liste des keywords du marche
- **Si Module 4c active (TASM disponible)** : utiliser directement l'union dedupliquee des keywords du TASM. Le gros du travail est deja fait — il reste a segmenter par intent.
- **Sinon** : Top 15-20 keywords hors-marque des concurrents (issus de `ranked_keywords` ou `domain_intersection`) + 10-15 keywords sectoriels identifies dans les clusters (`keyword_ideas`, `keyword_overview`)
- Dedupliquer

**Etape 2 :** Appeler `search_intent` sur cette liste (max 1000 keywords)

**Etape 3 :** Classer chaque keyword dans 3 buckets

| Bucket | Intent DataForSEO | Definition | Exemple (biscuiterie) |
|--------|-------------------|------------|-----------------------|
| **Commercial** | `transactional`, `commercial` | Le chercheur veut acheter ou comparer pour acheter | "coffret biscuit breton", "biscuit artisanal achat" |
| **Informationnel captable** | `informational` + legitimite marque | Le chercheur ne veut pas acheter MAIS la marque a une legitimite pour capter ce trafic et le rediriger (recette du fabricant, guide de l'expert) | "recette palet breton", "galette bretonne" |
| **Informationnel non-captable** | `informational` + pas de legitimite | Requete trop eloignee du business, pas monetisable | "histoire de la Bretagne", "culture normande" |

**Criteres de legitimite pour le bucket "Informationnel captable" :**
- Le prospect est fabricant/expert du produit recherche
- Un CTA produit naturel existe (recette → "goutez l'original")
- Un concurrent direct se positionne deja dessus (preuve de marche)
- Le volume justifie l'investissement (> 500 recherches/mois)

**Etape 4 :** Agreger par bucket

```
INTENT MARKET MAP:
- Commercial : {N} keywords, {volume total}/mois
  Top 5 : {kw1} ({vol}), {kw2} ({vol}), ...
- Informationnel captable : {N} keywords, {volume total}/mois
  Top 5 : {kw1} ({vol}), {kw2} ({vol}), ...
  Strategie : {1 phrase — ex: "contenu recette → CTA produit → funnel acquisition"}
- Informationnel non-captable : {N} keywords, {volume total}/mois (ecarte)
- TOTAL marche captable : {commercial + info captable}/mois
```

**Cette segmentation alimente :**
- Le diagnostic (axe Intentions de recherche) — un prospect qui ne couvre ni le commercial ni l'informationnel captable est plus contraint qu'un prospect qui couvre le commercial mais pas l'informationnel
- La section "Territoires de contenu" dans l'onglet Strategie (Pass 2)
- Le chiffrage du marche dans les titres et le benchmark (seul le "marche captable" est cite, jamais le brut non-captable)

#### Module 4d : SERP Features Analysis (toujours actif)

Apres les Modules 4/4b/4c, analyser les SERP features presentes sur les keywords commerciaux du prospect. Ces donnees sont deja collectees par les SERPs du Module 4c (`serp_organic_live_regular`) ou du Module 5 (`serp_organic_live_advanced`). Ce module ne fait pas de nouveaux appels API, il exploite les donnees existantes.

**Etape 1 :** Pour chaque resultat SERP deja en cache, extraire les features presentes :
- `popular_products` / `shopping` : Google Shopping
- `local_pack` : resultats locaux
- `featured_snippet` : position 0
- `ai_overview` : AI Overview
- `video` : resultats video
- `images` : bloc images
- `people_also_ask` : PAA

**Etape 2 :** Agreger par feature :
```
SERP_FEATURES_MAP:
- {feature}: {N}/{total} queries, volume total {X}/mois, {%} intent commercial
  Prospect present: OUI/NON
  Concurrents presents: {qui}
```

**Etape 3 :** Signaler les opportunites Shopping :
- Si `popular_products` OU `shopping` sur 3+ queries commerciales ET prospect absent → `SHOPPING_SIGNAL = YES`
- Sinon → `SHOPPING_SIGNAL = NO`

**Etape 4 :** Integrer dans le SDB (bloc `SERP_FEATURES_MAP` + `SHOPPING_SIGNAL`).

**Budget API :** 0 appel supplementaire (reutilise les SERPs des modules precedents).

---

### Modules conditionnels

#### Module 5 : GEO / IA

**Activer si :**
- Brief/transcript/emails mentionne "IA", "ChatGPT", "Perplexity", "visibilite IA", "GEO", "AI Overview"
- OU perimetre Pipedrive inclut GEO
- OU prospect = marque B2C avec notoriete (forte probabilite de requetes IA)

| Appel | Donnees | Pourquoi |
|-------|---------|----------|
| `serp_organic_live_advanced` sur 5-10 keywords cles | Presence d'AI Overviews sur les requetes strategiques | Evaluer l'impact IA sur le secteur |
| `on_page_content_parsing` sur homepage + 2-3 pages produits | Schema.org present ? Product, Offer, Organization ? | Etat des donnees structurees |

Completer avec les donnees manuelles du closer si disponibles (tests ChatGPT, Perplexity).

#### Module 6 : SEA / Paid

**Activer si :**
- Le prospect fait deja du paid (detectable dans ranked_keywords avec `item_types: ["paid"]`)
- OU brief/transcript/emails mentionne Google Ads, SEA, paid, budget pub
- OU perimetre Pipedrive inclut SEA

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `ranked_keywords` avec `item_types: ["paid"]` | Keywords payes actifs du prospect | Ce qu'il achete deja |
| `keyword_overview` sur 10-15 keywords strategiques | CPC, competition level, search volume | Valeur du paid vs organique |

#### Module 4e : Competitive Ads Analysis (conditionnel)

**Activer si :** Google Ads MCP disponible ET `SEA_SIGNAL = EXPLICIT` ou `DETECTED`.

**Objectif :** comprendre le paysage concurrentiel paid, pas juste organique. Qui achete les memes mots-cles ? A quel CPA ? Quelle part d'impressions ?

**Etape 1 :** Auction insights (si disponible via Google Ads API)
- Identifier les concurrents qui encherissent sur les memes keywords
- Part d'impressions du prospect vs concurrents
- Taux de chevauchement (overlap rate)

**Etape 2 :** Analyse SERP paid (via DataForSEO si pas d'auction insights)
- Sur les 5 keywords commerciaux cles, verifier qui apparait en annonces
- Comparer les positions payantes du prospect vs concurrents

**Etape 3 :** Integrer dans le SDB

```
COMPETITIVE_ADS:
- Concurrents Ads identifies : {liste}
- Part d'impressions prospect : {%} (si disponible)
- Concurrent dominant Ads : {domaine} (present sur {N}/{total} requetes)
- Opportunite : {description — ex: "0 concurrent Ads sur les requetes locales"}
Source : [src: google-ads auction_insights / dataforseo serp, {date}]
```

**Budget API :** 0-3 appels Google Ads (auction_insights) + 0 appels DataForSEO supplementaires (reutilise les SERPs existantes).

---

#### Module 4f : Benchmark Synthesis (TOUJOURS ACTIF — apres tous les modules 4*)

**Objectif :** agreger toutes les donnees concurrentielles en une synthese structuree pour le storytelling. C'est cette section que la Pass 2 utilise comme **colonne vertebrale narrative**.

**Etape 1 :** Construire la synthese

```
BENCHMARK SYNTHESIS:
---
GAP PRINCIPAL:
  Prospect : {trafic hors-marque ou clics GSC} / mois
  Leader : {domaine} — {trafic} / mois
  Ratio : 1:{X} (le leader capte {X}x plus de trafic)
  Source : {GSC clics reels | DataForSEO ETV — preciser}

CONCURRENTS CLES (top 3 business) :
  1. {domaine} : {trafic}, {keywords}, domine sur {requetes}. Present en {local packs / PAA / featured snippets}.
  2. {domaine} : {trafic}, {keywords}. {angle specifique — ex: "contenu blog agressif"}
  3. {domaine} : {trafic}, {keywords}. {angle}

OPPORTUNITES NON COUVERTES (top 5 keywords a fort volume que le prospect n'a pas) :
  1. "{keyword}" — {volume}/mois — {intent} — couvert par {concurrent}
  2. "{keyword}" — {volume}/mois — ...
  ...

QUI DOMINE OU :
  - Local packs : {domaine} (present sur {N}/{total} requetes locales)
  - PAA : {domaine} (present sur {N}/{total})
  - Featured snippets : {domaine} (si applicable)
  - Ads : {domaine} ({part d'impressions} si disponible)

INSIGHT BENCHMARK (1 phrase) :
  "{ex: Laserostop est le seul concurrent present dans les resultats locaux de toutes les villes. Le prospect est invisible malgre 46 centres indexes.}"
---
```

**Etape 2 :** Inserer dans le SDB (section dediee, apres COMPETITIVE_GAP et SERP_FEATURES_MAP).

**Regle :** l'INSIGHT BENCHMARK est la phrase qui devient le fil rouge du diagnostic en Pass 2. C'est le "et alors ?" du benchmark, pas un resume des chiffres. C'est ce que le closer dit au prospect quand il ouvre la proposition.

---

#### Etape post-Module 6 : SEA Signal Classification (OBLIGATOIRE)

Apres l'execution du Module 6 (ou apres la decision de ne pas l'activer), l'agent classe le **signal SEA** du deal. Ce signal est independant du diagnostic : le diagnostic mesure l'etat actuel, le signal mesure la **demande du prospect**.

| Signal | Definition | Sources de detection | Posture SLASHR |
|--------|-----------|---------------------|----------------|
| **EXPLICIT** | Le brief demande du paid | Brief/transcript/emails mentionne : Google Ads, Meta Ads, campagnes paid, budget pub, ROAS, Shopping, Performance Max, retargeting, display | **CONSEIL** (defaut) ou **PILOTE** (si perimetre Croissance) |
| **DETECTED** | Le prospect a du paid actif mais n'en parle pas | Module 6 `ranked_keywords(paid)` retourne des resultats MAIS aucune mention paid dans brief/transcript/emails | Mentionner la synergie SEO/SEA dans la strategie |
| **OPPORTUNITY** | Pas de demande prospect, pas de paid actif, MAIS les donnees montrent une opportunite paid | CPCs bas (< 1.50 EUR) sur keywords commerciaux ET/OU 0 concurrent en paid sur 3+ keywords commerciaux ET/OU SHOPPING_SIGNAL = YES | Mentionner l'opportunite dans le diagnostic + integrer en Phase 2 |
| **ABSENT** | Ni demande, ni activite paid, ni opportunite detectee | Module 6 non active ET aucune mention paid ET aucun signal d'opportunite | Differe hors perimetre |

**Regles de classification :**
1. Scanner brief, transcript, emails et notes Pipedrive pour les keywords paid (Google Ads, Meta Ads, Facebook Ads, campagnes, budget pub, ROAS, CPA, Shopping, Performance Max, retargeting, display, paid search, SEA)
2. Si au moins 1 mention → `SEA_SIGNAL = EXPLICIT`
3. Sinon, si Module 6 active ET `ranked_keywords(paid)` retourne des resultats → `SEA_SIGNAL = DETECTED`
4. Sinon, detecter l'opportunite paid :
   - Verifier les CPCs sur les keywords commerciaux (issus de `keyword_overview` si Module 6 active, ou de `ranked_keywords` du Module 3)
   - Si CPCs moyens < 1.50 EUR sur les keywords commerciaux OU 0 concurrent en paid sur 3+ keywords commerciaux OU SHOPPING_SIGNAL = YES → `SEA_SIGNAL = OPPORTUNITY`
   - Documenter dans le SDB : `SEA_OPPORTUNITY: "{raison}" (ex: "0 concurrent Search Ads, CPCs 0.30 EUR, terrain vierge")`
5. Sinon → `SEA_SIGNAL = ABSENT`

**Posture SLASHR (mapping) :**
- `EXPLICIT` + perimetre Croissance → `SEA_POSTURE = PILOTE` (SLASHR gere la strategie + pilotage campagnes)
- `EXPLICIT` + autre perimetre → `SEA_POSTURE = CONSEIL` (defaut — cabinet conseil, pas agence media)
- `DETECTED` → `SEA_POSTURE = CONSEIL` (pas de section dediee, mention synergie SEO/SEA dans la section benchmark ou opportunites, 1-2 phrases)
- `OPPORTUNITY` → `SEA_POSTURE = HORS_PERIMETRE` (pas de section dediee paid, mais les donnees sont exposees dans le diagnostic et le paid est integre dans la trajectoire Phase 2)
- `ABSENT` → `SEA_POSTURE = HORS_PERIMETRE`

**IMPORTANT :** le signal SEA est un routage de la demande prospect, pas un diagnostic. Le diagnostic strategique reste inchange.

#### Module 7 : Social Search

**Activer si :**
- Perimetre Pipedrive inclut Social
- OU brief mentionne TikTok, Instagram, YouTube, Social Search
- OU prospect B2C avec cible jeune

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `serp_youtube_organic_live_advanced` sur 5-10 keywords | Presence du prospect sur YouTube Search | YouTube = 2eme moteur |
| `serp_youtube_video_info_live_advanced` si videos trouvees | Vues, engagement, date | Perf des contenus existants |
| `kw_data_google_trends_explore` (type: youtube) | Tendance recherches YouTube | Potentiel video/social |

#### Module 8 : Technique / UX

**Activer si :**
- Le prospect est en refonte de site
- OU brief mentionne performance, vitesse, Core Web Vitals, UX
- OU trafic correct mais conversion faible (signal UX)

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `on_page_lighthouse` | Performance, Accessibility, Best Practices, SEO scores | Etat technique objectif |
| `on_page_instant_pages` sur 3-5 pages cles | Erreurs SEO on-page, balises, structure | Quick wins techniques |
| `on_page_content_parsing` sur pages strategiques | Structure H1-H6, liens, contenu | Architecture de contenu |

#### Module 9 : Tendances / Saisonnalite

**Activer si :**
- Secteur saisonnier (food, tourisme, retail, mode)
- OU timing du deal est important (budget a engager avant une saison)
- OU on veut demontrer l'urgence par les donnees (pas par la dramatisation)

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `kw_data_google_trends_explore` (12 mois) sur 5 top keywords | Saisonnalite des recherches | Pics et creux |
| `kw_data_dfs_trends_explore` marque vs concurrents | Tendance de la marque | Hausse/baisse d'interet |
| `historical_rank_overview` du prospect | Evolution trafic 12-24 mois | Monte, stagne ou descend |

#### Module 10 : Contenu / Semantique

**Activer si :**
- Diagnostic SEO revele un gap de contenu important (peu de keywords hors-marque)
- OU strategie de contenu = pilier de la recommandation
- OU prospect a beaucoup de pages mais mal optimisees

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `keyword_ideas` (5-10 seed keywords secteur) | Univers semantique a couvrir | Thematiques manquantes |
| `related_keywords` (3-5 top keywords) | Longue traine, requetes associees | Angles de contenu |
| `keyword_suggestions` (termes sectoriels) | Suggestions long-tail | Plan editorial |
| `search_intent` (20 keywords prioritaires) | Intent : info, nav, commercial, transactionnel | Prioriser par intent d'achat |
| `bulk_keyword_difficulty` (opportunites identifiees) | Difficulte de positionnement | Realisme des recos |

#### Module 11 : Website Crawl + Structure Audit (TOUJOURS ACTIF, AVANT DIAGNOSTIC)

Crawle le site reel du prospect. Ce module est un prerequis au diagnostic : **ne jamais diagnostiquer sans connaitre la structure du site.**

**Etape 1 : Sitemap (OBLIGATOIRE)**
1. Lire `robots.txt` → trouver le sitemap
2. Parser le sitemap index puis chaque sous-sitemap
3. **Inventorier la structure** : combien de pages par type (produit, categorie, blog, local/centre, landing page, etc.)
4. Ecrire le resume dans le cache

**Pourquoi obligatoire :** sans le sitemap, l'IA peut croire qu'un site n'a pas de pages locales alors qu'il en a 54. Le sitemap revele la structure reelle du site, pas juste les pages qui rankent.

**Etape 2 : Croisement sitemap x GSC (si GSC disponible)**
1. Pour chaque categorie de pages identifiee (ex: `/centre-*`), filtrer les donnees GSC par URL pattern
2. Calculer les metriques agregees par categorie : clics, impressions, CTR, position moyenne
3. Identifier les categories qui sous-performent (beaucoup de pages, peu de trafic)

**Exemple :** 54 pages `/centre-anti-tabac-*` dans le sitemap mais seulement 35 clics/mois sur la meilleure → les pages locales existent mais ne performent pas. C'est un diagnostic completement different de "les pages locales n'existent pas".

**Etape 3 : Crawl echantillon (OBLIGATOIRE)**
- Homepage + 3-5 pages strategiques (1 page locale, 1 page blog, 1 page service)
- Extraire : title, meta, H1, schema JSON-LD, liens internes
- **Verifier les CTA et parcours de conversion** : est-ce que les pages blog ont des CTA vers les pages service/centres ? Est-ce que les pages centres ont un formulaire de prise de rendez-vous ? Est-ce que le store locator fonctionne ?

**REGLE CRITIQUE : ne jamais affirmer l'absence de quelque chose (CTA, pages locales, schema, etc.) sans l'avoir verifie par un crawl.** "Les pages blog n'ont pas de CTA" est une affirmation factuelle qui demande une preuve (crawl de la page). "Les pages blog sous-performent" est un constat mesurable (GSC). Le diagnostic ne doit contenir que des constats verifiables, pas des hypotheses deguisees en faits.

**Budget :** 0 appel DataForSEO, max 10 requetes HTTP, 60s total.

**Non-bloquant :** si le crawl echoue (homepage inaccessible, timeout global), le deal continue sans. L'agent note "Module 11 non disponible (site injoignable)" dans l'evidence log et continue avec les donnees DataForSEO seules.

**Output :** 4 fichiers JSON dans `.cache/deals/{deal_id}/website/` :
- `homepage.json` : titre, meta desc, OG, headings, Schema.org, liens, images, CTAs, formulaires
- `sitemap.json` : nombre total URLs **declarees dans le sitemap**, distribution (product/blog/pages/category), ratio editorial vs catalogue. **ATTENTION : le sitemap ne reflete pas toujours le nombre de pages indexees par Google.** Pour le nombre reel de pages indexees, utiliser `site:{domain}` ou les donnees GSC. Le SDB doit distinguer clairement "URLs sitemap" et "pages indexees".
- `sampled_pages.json` : analyse de 3-5 pages echantillonnees (word count, headings, meta, schema)
- `crawl_summary.json` : synthese + `scoring_hints` (S2, S3, S4) — **fichier principal consomme par l'agent**

**Donnees extraites et destination :**

| Donnee | Source | Alimente |
|--------|--------|----------|
| Title, meta desc, OG tags | Homepage | SDB SEARCH_STATE |
| H1-H6 hierarchy | Homepage + samples | S2 score |
| Schema.org types (trouves/manquants) | Homepage + samples | S2 score, OPPORTUNITIES |
| Sitemap total URLs + distribution | /sitemap.xml | S3 score (page count reel) |
| Ratio editorial vs catalog | Sitemap patterns | S3 score |
| Word count moyen | Samples | S3 score (thin content) |
| CTA, formulaires, nav items | Homepage | S4 score |
| Images sans alt | Homepage | OPPORTUNITIES (quick wins) |
| Meta desc manquantes | Samples | OPPORTUNITIES (quick wins) |

---

### Strategie d'execution DataForSEO : batch parallele (OBLIGATOIRE)

**INTERDIT d'appeler les endpoints DataForSEO un par un.** Tous les appels DataForSEO (Modules 3, 4, 4b, 4c, 5-10) DOIVENT etre executes par lots via l'outil batch parallele. L'outil gere le cache, les retries et la parallelisation (5 workers).

**Outil :** `python3 tools/batch_dataforseo.py --deal-id {deal_id} --requests-file /tmp/batch_lot{N}.json`

**Procedure par lot :**
1. Ecrire le fichier `/tmp/batch_lot{N}.json` (tableau JSON de requetes)
2. Executer `batch_dataforseo.py`
3. Lire le JSON stdout (summary avec statuts et cache_paths)
4. Lire les fichiers cache pour exploiter les resultats

**Les 5 lots :**

| Lot | Contenu | Requetes typiques | Dependance |
|-----|---------|-------------------|------------|
| **1** | Modules 3 + 4 debut | 4 (`domain_rank_overview` + `ranked_keywords` + `keywords_for_site` + `competitors_domain`) | Domaine PRINCIPAL confirme (Etape 1.1b) |
| **2** | Module 4 benchmark | 4 (3x `domain_rank_overview` concurrents + 1x `domain_intersection`) | Lot 1 → concurrents identifies |
| **3** | Module 4c SERPs (conditionnel) | 5-8 (`serp_organic_live_regular` par keyword) | Lot 1 → aucun concurrent business |
| **4** | Module 4c deep-dive (conditionnel) | 11 (5x `domain_rank_overview` + 5x `ranked_keywords` + 1x `domain_intersection`) | Lot 3 → concurrents niche identifies |
| **5** | Module 4b + conditionnels 5-10 | 1-10 (`search_intent` + modules actives) | Lots precedents termines |

**Format de chaque requete dans le tableau :**
```json
{
  "id": "overview_prospect",
  "endpoint": "dataforseo_labs/google/domain_rank_overview/live",
  "body": [{"target": "example.com", "language_code": "fr", "location_code": 2250}],
  "cache_path": "domain_example.com/domain_rank_overview.json"
}
```

**Regles :**
- Le lot 2 depend des resultats du lot 1 (concurrents identifies) → sequentiel
- Les lots 3 et 4 sont conditionnels (Module 4c) → seulement si aucun concurrent business
- Le lot 5 attend les resultats precedents (intent market map, modules conditionnels)
- Si un lot echoue partiellement (exit code 2), lire les resultats OK et noter les echecs dans l'evidence log

### Input consultant SEA (optionnel)

Si le deal inclut un volet Ads et qu'un consultant SEA est disponible :

1. Apres la collecte Google Ads (module conditionnel), partager le SDB avec le consultant
2. Le consultant injecte ses notes dans le champ `SEA_CONSULTANT_NOTES` du SDB :
   - Conformite reglementaire
   - Cannibalisation PMax/Search
   - Recommandations budget et encheres
   - Nouveaux canaux (Demand Gen, YouTube)
   - Risques compte
3. Ces notes sont integrees dans le diagnostic strategique (Etape 1.3)
4. Si aucun consultant n'est disponible, l'agent fait son analyse avec les donnees collectees

Le consultant peut aussi deposer un document dans le dossier Drive du deal (prefixe `SEA-NOTES-*`).

---

## Etape 1.2 : Structuration

Organiser les donnees brutes en categories exploitables :

| Categorie | Contenu |
|-----------|---------|
| `PROSPECT_PROFILE` | Secteur, taille, maturite digitale, contexte business |
| `PAIN_POINTS` | Douleurs identifiees, verbatims exacts, trigger ("pourquoi maintenant") |
| `SEARCH_STATE` | Metriques actuelles : trafic organique estime (visites/mois), keywords, ETV (valeur EUR/mois), repartition marque/hors-marque. **IMPORTANT : ne pas confondre trafic (visites) et ETV (equivalent budget ads en EUR). Toujours etiqueter clairement : "trafic organique estime" (source: domain_rank_overview, champ organic_count = visites) vs "valeur trafic ETV" (source: domain_rank_overview, champ etv = EUR).** Enrichir avec les donnees Module 11 (si disponibles) : pages sitemap (total + distribution product/blog/pages), ratio editorial vs catalogue, Schema.org types trouves + manquants recommandes, profondeur heading, images sans alt. |
| `COMPETITIVE_GAP` | **Concurrents business** (meme secteur, meme offre) en priorite, concurrents semantiques en contexte. Metriques comparatives, keywords exclusifs, ratio de gap. Si Module 4c active : preciser la source (SERP analysis) et la methode. |
| `INTENT_MARKET_MAP` | Segmentation intent du marche : buckets Commercial / Info captable / Info non-captable, volumes par bucket, top keywords, strategie par bucket |
| `OPPORTUNITIES` | Quick wins (pages en top 10-20, donnees structurees manquantes), territoires non couverts par bucket intent, clusters a creer |
| `RISKS` | Red flags, contraintes (budget, timeline, decideur absent, multi-presta) |
| `CONDITIONAL_DATA` | Resultats des modules 5-10 (si actives), organises par module |
| `TONE_CONTEXT` | Ton des echanges email (formel/informel), reactivite, niveau technique du decideur |
| `BRAND_SEARCH_ANALYSIS` | (conditionnel) Analyse des recherches de marque si volume significatif. Voir section ci-dessous. |
| `SERP_FEATURES_MAP` | (conditionnel) SERP features detectees sur les keywords commerciaux. Voir Module 4d. |
| `SECONDARY_MARKETS` | (conditionnel) Marches B2B, CE/CSE, export detectes dans les sources. Voir section ci-dessous. |

### BRAND_CONTEXT (conditionnel — onglet Contexte)

**Activer si** au moins 2 des conditions suivantes sont remplies :
1. Le prospect a une marque patrimoniale ou identitaire forte (heritage, territoire, histoire)
2. Les sources Drive contiennent des documents de contexte marque (PPT partenaire, charte, brand book, personas, plateforme de marque, brief)
3. HOOK_TYPE = "ancrage_identitaire" (identifie en Etape 1.3)
4. BRAND_SEARCH_ANALYSIS.BRAND_SLIDE = YES (volume marque significatif)
5. SECONDARY_MARKETS.B2B_SLIDE = YES (cibles multiples justifiant un mapping personas)

**Detection :** scanner les fichiers Drive (Module 2) pour les termes : marque, ADN, heritage, territoire, persona, cible, charte, positionnement, brand, identite, plateforme de marque, brief creatif. Scanner aussi les notes Pipedrive pour des mentions de contexte identitaire.

**Contenu SDB :**
```
BRAND_CONTEXT:
  CONTEXTE_TAB: YES | NO
  Conditions remplies: {liste des conditions cochees parmi 1-5}
  Sources contexte: {fichiers Drive identifies, avec chemins cache}
  Piliers de marque: {liste si identifies dans les sources}
  Personas detectes:
    B2C: {liste si identifies}
    B2B: {liste si identifies}
  Si CONTEXTE_TAB = NO: justification en 1 ligne
```

**Regle :** si CONTEXTE_TAB = YES, Pass 2 doit planifier un onglet Contexte dans le NBP. Les donnees brutes des sources Drive sont transmises telles quelles (pas d'interpretation en Pass 1).

---

### BRAND_SEARCH_ANALYSIS (conditionnel)

**Activer si :** volume marque > 5 000 recherches/mois OU part marque > 60% du trafic organique.

L'objectif n'est pas de diagnostiquer un probleme (conversion, technique) mais de montrer que la marque est un **actif strategique** : un tremplin de confiance aupres de Google.

**Contenu SDB :**
```
BRAND_SEARCH_ANALYSIS:
  BRAND_SLIDE: YES | NO
  Volume marque: {X} recherches/mois [src: dataforseo, ranked_keywords]
  Part marque: {X}% du trafic organique
  Top 5 requetes marque:
    - {kw1} ({vol}/mois)
    - {kw2} ({vol}/mois)
    - ...
  Signal Google: La marque genere un volume de recherche eleve, ce qui
    signale a Google une autorite thematique. C'est un tremplin pour
    se positionner sur les requetes hors-marque adjacentes.
  INTERDIT: ne pas diagnostiquer la conversion marque ici (c'est plus loin)
```

### SECONDARY_MARKETS (conditionnel)

**Activer si :** les sources Drive/Pipedrive mentionnent des marches secondaires (B2B, CE/CSE, export, grossiste, professionnel, etc.).

**Detection :** scanner toutes les sources collectees (Module 1 + 2) pour les termes : B2B, CE, CSE, comite d'entreprise, professionnel, grossiste, revendeur, distributeur, GMS, CHR, wholesale, corporate, export, pro.

**Contenu SDB :**
```
SECONDARY_MARKETS:
  B2B_SLIDE: YES | NO
  Marches detectes:
    - {nom}: {source fichier/note}
      Workflow actuel: {comment les commandes arrivent (email, telephone, formulaire)}
      Lien Search: {requetes identifiees + volume OU "pas de signal Search"}
      Lien refonte: {OUI/NON + pourquoi}
    - {nom}: ...
  Si aucun marche detecte: SECONDARY_MARKETS = NONE
```

**Regles :**
- Distinguer les marches transactionnels (CE/CSE = commandes reelles, Search-relevant) des marches vitrine (B2B Pro = showcase only, peu de signal Search)
- Pour chaque marche, evaluer si le Search peut capter de la demande ou si c'est un canal hors-Search (email, reseau, appel)
- Le signal `B2B_SLIDE = YES` est emis si au moins 1 marche a un lien Search identifie

---


---

## Output Pass 1 (SDB thin + Evidence log) — regle de performance

La Pass 1 produit un **SDB compact** (pas de dumps) :

### SDB thin (obligatoire)
- 8-12 bullets max (constats + opportunites + risques)
- Tables compactes : top N (N=10 ou 20 max)
- AUCUN body email complet sauf si absolument necessaire (sinon snippet)
- AUCUN CSV long : uniquement agregats + top lignes

### Evidence log (obligatoire)
Pour chaque chiffre cle, conserver :
- source (Pipedrive/Drive/DataForSEO)
- endpoint (ex: ranked_keywords)
- parametres (domain, date)
- timestamp
- fichier cache (.cache/...)

Ce log sert au debug et a la rejouabilite.

### Erreurs et fallbacks (obligatoire dans l'evidence log)

Pour chaque erreur API rencontree pendant la collecte :
- **Endpoint** : URL ou nom de l'endpoint
- **Status** : code HTTP ou message d'erreur
- **Impact** : quel bloc du SDB est affecte (ex: "COMPETITIVE_GAP incomplet")
- **Fallback** : action prise (ex: "utilise domain_rank_overview seul", "module ignore")

Format dans l'evidence log :
```
ERRORS & FALLBACKS:
- dataforseo/ranked_keywords (timeout 20s) → impact: SEARCH_STATE partiel → fallback: domain_rank_overview seul
- drive/files/abc123 (403 Forbidden) → impact: document_prospect manquant → fallback: collecte sans ce fichier
```

### Format de source dans le SDB (obligatoire)

Chaque affirmation quantitative dans le SDB DOIT porter une etiquette source inline au format :

`[src: {origine}, {endpoint}, {periode}, {date_collecte}]`

Origines valides : `pipedrive`, `drive`, `dataforseo`, `gsc`, `google-ads`, `calcul`, `benchmark`, `crawl`

Exemples :
- Trafic organique: 13 499 clics/mois `[src: gsc, performance_overview, 28j, 2026-03-27]`
- Budget Ads: 15 676 EUR/mois `[src: google-ads, campaigns, 2026-02-27 au 2026-03-27, collecte 2026-03-27]`
- ETV: 2 757 EUR `[src: dataforseo, domain_rank_overview, snapshot, 2026-03-27]`
- CVR implicite: 4.4% `[src: calcul, 792 conv / 18 063 clics, google-ads 30j]`

**REGLE PERIODE (CRITIQUE)** : ne pas fixer UNE periode unique. Utiliser la bonne periode pour le bon usage.

| Usage | Periode | Source | Pourquoi |
|-------|---------|--------|----------|
| **Diagnostic performance** | 90 jours | GSC 90j, Google Ads 90j | Lisse les anomalies, couvre un trimestre, representatif |
| **Tendance** | 12 mois ou daily trend 28j | GSC daily, Google Ads monthly | Detecte saisonnalite et trajectoire |
| **Budget mensuel actuel** | Dernier mois complet | Google Ads | Pour citer un budget reel, pas une moyenne |
| **Quick wins / positions** | 28 jours | GSC 28j | Positions recentes |
| **Benchmark concurrent** | Snapshot | DataForSEO | Pas de notion de periode, snapshot au jour J |

```
SNAPSHOT DONNEES:
- Date de collecte : {YYYY-MM-DD}
- GSC performance : 90 jours ({start} au {end})
- GSC tendance : 28 jours daily trend
- Google Ads diagnostic : 90 jours ({start} au {end})
- Google Ads budget mensuel : dernier mois complet ({mois})
- DataForSEO : snapshot au {date}
```

**REGLE : chaque chiffre du SDB porte sa periode.** "Budget mensuel : 15 676 EUR (mars 2026)" et "CPA moyen : 19.8 EUR (90 jours, jan-mars 2026)" sont deux chiffres avec des periodes differentes. Les deux sont corrects. L'important est que le HTML reprenne la meme periode que le SDB.

**Pourquoi** : si le SDB dit "15 676 EUR" (mars complet) et que la Pass 3 re-collecte et trouve "14 000 EUR" (27 jours de mars), les chiffres du HTML ne matchent plus le diagnostic.

**REGLE PASS 3** : la Pass 3 ne re-collecte JAMAIS les donnees. Elle utilise UNIQUEMENT les chiffres du SDB. Si un chiffre manque dans le SDB, elle remonte au SDB (pas aux APIs). Si le SDB est trop vieux (> 7 jours), relancer la Pass 1.

Les qualificatifs (ex: "maturite digitale faible") ne necessitent pas de source mais doivent pouvoir etre justifies par au moins un data point de l'evidence log.

**Regle :** si un chiffre apparait dans le SDB sans etiquette `[src:]`, il est rejete a la relecture. L'agent corrige avant de passer a Pass 2.

### Ecriture artefacts (obligatoire)
Ecrire :
- `.cache/deals/{deal_id}/artifacts/SDB.md`
- `.cache/deals/{deal_id}/evidence/evidence_log.md`


## Etape 1.2b : Checklist d'analyse pre-diagnostic (OBLIGATOIRE)

**AVANT de diagnostiquer, parcourir `context/references/analysis-checklist.md`.**

Chaque question de la checklist doit etre repondue avec des donnees. Si la donnee manque, le noter. Cette etape empeche les diagnostics fondes sur des hypotheses non verifiees (ex: "pas de pages locales" alors qu'il y en a 54, "pas de CTA" alors qu'il y en a).

**Output :** pour chaque question, ecrire la reponse dans le SDB avec la source. Compteur : "Checklist : X/Y questions repondues."

---

## Etape 1.2c : Approfondissement contextuel (OBLIGATOIRE)

Apres la checklist, l'IA dispose de toutes les donnees de base. Avant de diagnostiquer, elle doit se poser 3 questions d'approfondissement specifiques a CE deal :

**Question 1 : "Qu'est-ce qui pourrait contredire mon diagnostic ?"**
Identifier le diagnostic qui emerge des donnees, puis chercher activement ce qui pourrait le fausser.
- Si le diagnostic est "les pages locales sous-performent" → verifier si c'est un probleme de contenu (crawler une page), d'indexation (URL inspection), ou de concurrence (SERP locale)
- Si le diagnostic est "le prospect depend du paid" → verifier si le paid achete du trafic que l'organique a deja (overlap)

**Question 2 : "Qu'est-ce que le concurrent fait que le prospect ne fait pas ?"**
Chercher 1-2 SERPs strategiques et comparer la presence du prospect vs le concurrent principal.
- Qui apparait dans les local packs ?
- Qui apparait dans les People Also Ask ?
- Le concurrent achete-t-il la marque du prospect en Ads ?
- Le concurrent a-t-il du schema que le prospect n'a pas ?

**Question 3 : "Si j'etais le closer en R2, quelle question le prospect me poserait et est-ce que j'ai la donnee pour repondre ?"**
Les questions typiques :
- "Qu'est-ce qui ne va pas concretement ?" → donnees specifiques, pas des generalites
- "Que font mes concurrents ?" → benchmark chiffre
- "Combien ca va rapporter ?" → ROI avec methode explicite
- "Par quoi on commence ?" → quick wins concrets et actionnables

**Question 4 : "Mon diagnostic est-il aligne avec le brief du prospect ?"**
Relire le champ `BRIEF PROSPECT` du SDB (rempli en section 0 de la checklist). Verifier :
- Le diagnostic ouvre-t-il par la priorite declaree du prospect ? Si le prospect veut des Ads et que le diagnostic ouvre par le SEO, c'est un probleme de cadrage.
- La proposition repond-elle d'abord a la douleur exprimee, puis ajoute la valeur non demandee ?
- L'ordre des sections suit-il la hierarchie du prospect, pas celle du systeme ?

**REGLE : on diagnostique ce qu'on trouve, mais on presente dans l'ordre de ce que le prospect veut entendre.** L'analyse SEO peut etre la plus riche, mais si le brief dit "Ads first", le Diagnostic ouvre par les Ads et le SEO vient en opportunite.

**Output :** 3-5 insights specifiques a ce deal + validation de l'alignement brief/diagnostic.

---

## Etape 1.3 : Diagnostic strategique

**Objectif :** a partir de toutes les donnees collectees, de la checklist d'analyse ET de l'approfondissement contextuel, identifier ce qui bloque le plus de valeur et ce qui peut la debloquer.

**L'IA raisonne librement.** Pas de grille a remplir, pas de scores a attribuer. Le diagnostic est un raisonnement structure :

**REGLE D'ORDONNANCEMENT : le diagnostic et la proposition suivent la hierarchie du prospect.** Si `BRIEF PROSPECT > Priorite declaree = Ads`, le diagnostic ouvre par l'analyse Ads, la strategie ouvre par les recommandations Ads, et le SEO vient en opportunite complementaire. L'expertise SEO est le differenciateur de SLASHR, mais ce n'est pas forcement le sujet d'ouverture.

### A. Comprendre le prospect

- **Qui est-ce ?** Secteur, taille, maturite digitale, contexte business
- **Quelle est la douleur specifique ?** Pas "ameliorer le SEO" → la vraie douleur business (CA, parts de marche, dependance au paid, retard sur un concurrent)
- **Quel est le trigger ?** Pourquoi maintenant ? (refonte, AO, budget annuel, pression board, concurrent qui avance)
- **Quels verbatims utiliser ?** Citations exactes qui montrent qu'on a ecoute
- **Quel est le ton des echanges ?** Formel/informel, reactif/lent, technique/business
- **Qui est le decideur ?** Profil (DG, CMO, responsable digital, fondateur), ses preoccupations (ROI ? image ? rapidite ?)

### B. Diagnostiquer la situation

L'agent raisonne sur les donnees collectees pour produire un diagnostic strategique. Le diagnostic est un outil interne de priorisation, jamais expose au prospect.

> Rappel : 5 formulations interdites, test de substitution (cf. `agents/prepare-context.md` section 3).

### Output obligatoire

```
DIAGNOSTIC STRATEGIQUE
GENERATED_AT: {ISO timestamp}

CONTRAINTE PRINCIPALE : {en langage business, 2-3 phrases data-first}
→ Pourquoi c'est le verrou. Donnees sources.
→ Confiance : {HIGH / MEDIUM / LOW} — {source de la confiance ou raison du doute}

LEVIERS PRIORITAIRES (max 2) :
1. {levier} — {impact attendu, chiffre source}
   Confiance : {HIGH / MEDIUM / LOW} — {justification}
2. {levier} — {impact attendu, chiffre source}
   Confiance : {HIGH / MEDIUM / LOW} — {justification}

CE QU'ON NE FAIT PAS MAINTENANT :
- {force/axe} — {pourquoi pas maintenant, condition de reactivation}

ROI :
  Methode : {A (Gap CTR) / B (Gap concurrent) / C (Volume adressable)}
  Fourchette : {min} — {max} EUR/an
  Confiance : {HIGH / MEDIUM / LOW} — {ex: "GSC + CVR reel = High" ou "DataForSEO estimates + CVR benchmark = Medium"}

SCENARIO RECOMMANDE :
  Niveau : {Pilotage / Production / Acceleration}
  Budget : {montant}/mois
  Confiance : {HIGH / MEDIUM / LOW} — {ex: "gap justifie la production, equipe interne absente" ou "budget prospect inconnu, hypothese"}

TONE_PROFILE : {DIRECT / PEDAGOGIQUE / PROVOCATEUR / TECHNIQUE}
→ {justification basee sur le profil decideur et le contexte du deal}

CONFIANCE GLOBALE : {HIGH / MEDIUM / LOW}
→ Resume : {N} decisions HIGH, {N} MEDIUM, {N} LOW. Points d'attention : {liste}
```

### Regles
- Max 3 leviers actifs (1 contrainte + 2 leviers)
- Chaque conclusion appuyee par des donnees (evidence chain)
- Si les donnees sont insuffisantes pour conclure, le dire (Confiance Low)
- Le diagnostic est INTERNE. Les conclusions sont traduites en langage business dans le HTML.

### C. Construire la strategie + ROI + trajectoires

Enchaine directement depuis le diagnostic, sans relire les donnees.

- **Quel perimetre ?** SEO seul ? Search global ? Quels modules ont produit des donnees exploitables ?
- **Quelle structure d'offre ?** (cf. `agents/prepare-context.md` section 2, Structure de l'offre)
  - Phase 1 Audit strategique : quels livrables specifiques pour ce deal ?
  - Phase 2 Accompagnement structure : quels piliers activer ? A quelle intensite ?
  - Quel scenario recommander ? (Pilotage / Production / Acceleration)
- **Quelles descriptions de prestations ?** Contextualiser les templates de `context/service_catalog.md` avec les donnees du deal (secteur, dimensions B2C/B2B/international, concurrents, contraintes specifiques, partenaires techniques). Produire la section SERVICE_DESCRIPTIONS du SDB.
- **Quelles phases de recommandation ?** Actions concretes par phase, adaptees au contexte
- **Quel ROI ?** Calcul conservateur avec les donnees reelles du prospect (voir `context/references/roi-methodology.md`)

**Classification diagnostic (max 3 leviers actifs) :**
- Contrainte principale : {axe} → justification 2-3 phrases data-first
- Leviers prioritaires : {axe A} + {axe B} → 1 phrase chacun
- Differe (sequentiel) : axes a activer quand condition remplie
- Differe (hors perimetre) : axes hors perimetre

**Trajectoire 90 jours (contextuelle, JAMAIS generique) :**

Le plan 90 jours est cale sur l'evenement structurant du deal, pas sur un template fixe. L'agent choisit le contexte applicable et adapte M1/M2/M3 :

| Contexte | M1 | M2 | M3 |
|----------|----|----|-----|
| **Refonte** (REFONTE = OUI) | Audit + cadrage refonte (specs SEO, architecture cible, plan de migration) | Accompagnement refonte (suivi dev, redirections, recette SEO) | Activation sur le nouveau site (contenu, Merchant Center, tracking) |
| **AO** (contexte AO) | Cadrage perimetre SEO + livrables pour reponse AO | Quick wins pre-AO (gains rapides demonstrables) | Plan strategique post-decision AO |
| **Saisonnalite** (pic saisonnier < 4 mois) | Audit + quick wins cibles sur le pic | Activation contenu saisonnier + optimisations | Mesure impact pic + plan long terme |
| **Standard** (aucun evenement structurant) | Cadrage + audit | Quick wins + structure | Activation + mesure |

**Regles :**
- Le plan 90 jours est CONSTRUIT AUTOUR de l'evenement structurant, pas a cote
- Si plusieurs contextes se combinent (refonte + saisonnalite), prioriser celui qui conditionne le reste (generalement la refonte)
- Chaque mois = 1 objectif + 1 livrable + 1 signal de succes (pas de liste generique)
- Le plan 90 jours reste aligne sur la contrainte principale du diagnostic : chaque mois doit adresser le verrou identifie

**Trajectoire 6 mois :** M4-M6 montee en puissance, piliers actives, objectifs intermediaires. Si SEA_SIGNAL = OPPORTUNITY, integrer l'activation paid en M4+ (pas avant).

**ROI conservateur :** chaque hypothese avec intervalle (borne basse conservatrice / borne haute optimiste realiste). ROI affiche = borne basse.

### D. Selectionner les cas clients

- Consulter `context/case_studies.md`
- Matcher 2-4 cas selon secteur (priorite 1), problematique (priorite 2), taille (priorite 3)
- Pour chaque cas retenu, structurer :
  - `match_criteria` : ce qui rend ce cas similaire au prospect (sectoriel, problematique, taille, profil decideur)
  - `key_metric` : le chiffre-resultat du cas le plus convaincant pour CE prospect
  - `sdb_juxtaposition` : quel bloc du SDB mettre en regard (pour que Pass 2 construise le parallele)
  - `angle` : l'angle de presentation adapte a CE prospect (1-2 phrases)

### E. Pre-grouper les blocs SDB par argument narratif

L'agent identifie 3-5 "arguments decideurs" et produit les `NARRATIVE_HINTS` dans le SDB.

**Exemples de regroupements typiques :**
- `SEARCH_STATE` + `COMPETITIVE_GAP` → "Le prospect est en retard mesurable"
- `INTENT_MARKET_MAP` + `OPPORTUNITIES` → "Le potentiel existe et est captable"
- Contrainte principale + `RISKS` → "Le verrou et ses consequences"
- `ROI` + `STRATEGIE_RECOMMANDEE` → "Le plan et son rendement"

Les differenciateurs SLASHR emergent des donnees elles-memes dans la proposition (cf. `agents/prepare-pass2.md`, Etape 2.4). Pass 1 ne produit pas de "transition opportunities" explicites.

### Output interne : section diagnostic du SDB

L'agent produit le diagnostic strategique directement dans le SDB (section `DIAGNOSTIC STRATEGIQUE`). Ce diagnostic est interne (jamais expose au prospect) et alimente directement les sections "Strategie recommandee" et "ROI" du SDB.

Le diagnostic est aussi archive dans un fichier separe pour rejouabilite :

**Ecriture obligatoire :** `.cache/deals/{deal_id}/artifacts/INTERNAL-DIAG.md` (utilise par Pass 2 et par `/debrief`).

```
=== DIAGNOSTIC STRATEGIQUE ===

CONTRAINTE PRINCIPALE : {en langage business, 2-3 phrases data-first}
→ Pourquoi c'est le verrou. Donnees sources.
→ Projection : {direction} {delta chiffre} {source} → {horizon}

LEVIERS PRIORITAIRES :
1. {levier} — {impact attendu, chiffre source}
   → Projection : {direction} {delta} → {horizon}
2. {levier} — {impact attendu, chiffre source}
   → Projection : {direction} {delta} → {horizon}

CE QU'ON NE FAIT PAS MAINTENANT :
- {axe} — {pourquoi pas maintenant, condition de reactivation}
- {axe} — {idem}

EXCEPTION SEA_SIGNAL (obligatoire si SEA_SIGNAL = EXPLICIT) :
Si `SEA_SIGNAL = EXPLICIT`, l'axe Amplification/Paid ne peut PAS etre differe hors perimetre. Reclassifier :
- Si opportunite paid significative + perimetre Croissance → levier prioritaire
- Si brief EXPLICIT mais fondations Search absentes → differe sequentiel ("cadrage SEA strategique M1, activation M3-M4 une fois les fondations Search posees")
- Justification obligatoire : "Le prospect demande un accompagnement paid. L'absence de structure paid renforce le besoin de cadrage strategique."

CONFIANCE : {High / Medium / Low}
→ {justification : quelles donnees manquent, quelles hypotheses}

TONE_PROFILE : {DIRECT / PEDAGOGIQUE / PROVOCATEUR / TECHNIQUE}
→ {justification basee sur le profil decideur et le contexte du deal}

ARC_CHOICE_RATIONALE :
- Arc retenu : {Classique | Urgence | Opportunite | Technique | Custom}
- Raison liee au decideur : {1 phrase — profil decideur + contexte}
- Raison liee aux donnees : {1 phrase — quel pattern dans le SDB oriente cet arc}
- Arc ecarte : {quel arc a ete considere et pourquoi rejete}

ROI DRIVERS (pont vers l'onglet ROI) :
- Driver 1 (Traffic) : {source} → {variable ROI impactee : visites cibles M12}
- Driver 2 (Conversion) : {source} → {variable ROI impactee : CVR / panier}
- Driver 3 (Mix marque/hors-marque) : {source} → {variable ROI impactee : part scalable}

PLAN 90 JOURS (contextuel, aligne sur la contrainte principale, 3 etapes max) :
CONTEXTE STRUCTURANT : {Refonte | AO | Saisonnalite | Standard}
1) M1 · {objectif adapte au contexte} → {livrable} → {signal attendu}
2) M2 · {objectif adapte au contexte} → {livrable} → {signal attendu}
3) M3 · {objectif adapte au contexte} → {livrable} → {signal attendu}

INSIGHT CENTRAL : {1 phrase non substituable}

TRAJECTOIRE 6 MOIS · Phase 2 "Run":
- M4-M6: {piliers actives, montee en puissance, intensite}
- Si SEA_SIGNAL = OPPORTUNITY : integrer activation paid en M4+
- Objectifs M6: {KPIs cibles sources}

ROI CONSERVATEUR (intervalle obligatoire) :
- Hypothese 1: {description} = {valeur_basse} - {valeur_haute} | Confidence: {High/Med/Low} | Validation: {comment valider} (source: {DataForSEO/GSC/transcript/benchmark})
- Hypothese 2: {description} = {valeur_basse} - {valeur_haute} | Confidence: {High/Med/Low} | Validation: {comment valider} (source: {source})
- Hypothese N: ...
- Chaine de calcul : H1 ({valeur}) x H2 ({valeur}) x ... = {resultat}
- ROI intervalle : x{N_bas} - x{N_haut} sur {periode}
- ROI affiche (conservateur) : x{N_bas} (borne basse de l'intervalle)
- Confidence globale ROI: {High/Medium/Low} (= min des confidences individuelles)
- Si Low sur 2+ hypotheses → ajouter dans le SDB: "Recommandation conditionnelle, validation en Phase 1"

> **Regle intervalle** : chaque hypothese a une borne basse (conservatrice) et une borne haute (optimiste realiste). Le ROI affiche au prospect = borne basse. L'intervalle complet est dans le simulateur ROI (onglet 3) pour que le prospect explore lui-meme.

Definitions de confiance ROI :
| Niveau | Critere | Exemple |
|--------|---------|---------|
| **High** | Donnee mesuree directement (prospect OU benchmark concret) | CA WooCommerce, panier moyen reel, positions DataForSEO |
| **Medium** | Donnee estimee via proxy fiable (DataForSEO ETV, benchmark secteur) | Trafic estime via ETV, CVR moyen secteur |
| **Low** | Hypothese sans mesure directe ni proxy fort | CVR post-refonte, impact contenu a 12 mois |

RESUME DECISIONNEL (6 bullets max):
1. {Douleur business chiffree : le probleme}
2. {Cout de l'inaction : ce que ca coute de ne rien faire}
3. {Levier principal : ce qu'on recommande}
4. {Quick wins 90 jours : resultats rapides attendus}
5. {ROI attendu : retour sur investissement}
6. {Investissement : fourchette prix}

EVIDENCE LOG:
- {affirmation 1} → source: {DataForSEO endpoint / GSC / transcript p.X / benchmark secteur}
- {affirmation 2} → source: {source}
- ...

=== FIN DIAGNOSTIC STRATEGIQUE ===
```

---

## Output Pass 1 : Structured Data Brief (SDB)

L'agent DOIT ecrire explicitement ce document interne avant de passer a la Pass 2 (`agents/prepare-pass2.md`).

```
GENERATED_AT: {ISO 8601 timestamp, ex: 2026-03-02T14:30:00}
=== STRUCTURED DATA BRIEF ===

PROSPECT: {nom} | {secteur} | {taille} | {maturite digitale}
DOMAINE_PRINCIPAL: {domaine} [src: {source de detection, ex: "drive, Prise de note R1 ligne 9"}]
DOMAINES_SECONDAIRES: {domaine1} ({role: migration cible / ancien / entite liee}), {domaine2} ({role}) | ou AUCUN
DECIDEUR: {prenom} {nom} | {role} | {preoccupation principale}
DECIDEUR_LEVEL: {DECIDEUR | INFLUENCEUR | OPERATIONNEL} [src: pipedrive, decideur_level]
DOULEUR: {1 phrase} | Verbatim: "{citation exacte}"
TRIGGER: {pourquoi maintenant}
TON: {formel/informel} | {reactif/lent} | {technique/business}
TONE_PROFILE: {DIRECT / PEDAGOGIQUE / PROVOCATEUR / TECHNIQUE} → {justification basee sur le profil decideur et le contexte du deal}
PERIMETRE_SLASHR: {SEO seul / SEO + GEO / Search global / etc.} [src: pipedrive, notes R1]
REFONTE: {OUI | NON} | {si OUI: timeline, ex: "go mars, MEL juin 2026"} | {CMS prevu si connu}
MODULES_ACTIFS: [{liste des modules actives, ex: 1-Pipedrive, 2-Drive, 3-SEO, 3b-GSC, 4-Benchmark, 4b-Intent, 4c-Niche, 5-GEO, 8-Technique, 9-Saisonnalite}]

SEA_SIGNAL: {EXPLICIT | DETECTED | ABSENT} [src: etape post-Module 6]
SEA_POSTURE: {PILOTE | CONSEIL | HORS_PERIMETRE}
SEA_BRIEF_REQUESTS: [{liste des demandes paid identifiees dans le brief, ex: "Google Ads Search", "Shopping", "3 scenarios budget", "estimation ROAS"}] (vide si ABSENT)

GSC_ACCESS: {YES | NO}

SEARCH STATE:
- Trafic organique: {X} visites/mois [src: dataforseo, domain_rank_overview]
- Keywords: {Y} total ({Z} marque / {W} hors-marque)
- ETV: {V} EUR
- Forces: {liste}
- Faiblesses: {liste}
- GSC (si Module 3b actif):
  - Clics: {X} /mois (90j) [src: gsc]
  - Impressions: {Y} /mois (90j) [src: gsc]
  - CTR moyen: {Z}% [src: gsc]
  - Position moyenne: {P} [src: gsc]
  - Split: {M}% marque / {HM}% hors-marque [src: gsc] (PRIORITAIRE sur DataForSEO)
  - Quick wins: {N} requetes (pos 5-20, impressions > 100, CTR < 5%) [src: gsc]
  - Top 10 queries hors-marque: [{requete, clics, impressions, CTR, position}] [src: gsc]

COMPETITIVE GAP:
- Concurrent #1: {nom} → {trafic} visites/mois (x{ratio} vs prospect)
- Concurrent #2: {nom} → {trafic} visites/mois
- Concurrent #3: {nom} → {trafic} visites/mois
- Keywords exclusifs concurrent #1: {top 5 avec volumes}
- Cout inaction: {visites perdues}/mois = {ETV} EUR/an

INTENT MARKET MAP:
- Commercial: {N} kw, {volume}/mois — Top: {kw1}, {kw2}, {kw3} [src: dataforseo, search_intent]
- Info captable: {N} kw, {volume}/mois — Top: {kw1}, {kw2}, {kw3} [src: dataforseo, search_intent]
  Strategie: {1 phrase — ex: contenu recette → CTA produit}
- Info non-captable: {volume}/mois (ecarte)
- TASM captable: {commercial + info captable}/mois [src: dataforseo, TASM Module 4c filtre par Module 4b]
- Part prospect actuelle: {trafic hors-marque} / {TASM captable} = {%} [src: calcul]
- Gap: {TASM captable - trafic hors-marque} recherches/mois non captees

OPPORTUNITIES:
- Quick wins: {liste avec impact estime}
- Territoires commerciaux: {clusters intent commercial non couverts}
- Territoires informationnels: {clusters info captable non couverts, avec strategie de monetisation}
- {GEO/IA si module 5 active}: {resultats}
- {SEA si module 6 active OU SEA_SIGNAL != ABSENT}:
  Si EXPLICIT: demandes brief (verbatim) + gap paid vs organic + CPC reference secteur + posture SLASHR (PILOTE/CONSEIL)
  Si DETECTED: activite paid actuelle (keywords payes, depense estimee) + synergie SEO/SEA potentielle
- {Social si module 7 active}: {resultats}
- {Technique si module 8 active}: {resultats}
- {Tendances si module 9 active}: {resultats}
- {Contenu si module 10 active}: {resultats}

DIAGNOSTIC STRATEGIQUE:
- Contrainte principale : {en langage business, 2-3 phrases data-first sur le verrou}
- Leviers prioritaires :
  - {levier A} : {impact chiffre attendu si active}
  - {levier B} : {impact chiffre attendu si active}
- Differe (sequentiel, avec condition d'activation) :
  - {axe} : sera active quand {condition}, horizon {X mois}
  - {axe} : {idem}
- Differe (hors perimetre) :
  - {axe} : hors perimetre car {raison}
  - {axe} : {idem}
- Projection contrainte principale (obligatoire) : {direction} {delta chiffre} {source} → {projection X mois}
- Projection leviers (obligatoire pour chaque) : {direction} {delta} → {horizon}
- Insight central: {1 phrase non substituable}
- Confiance globale diagnostic: {High/Medium/Low}
- TONE_PROFILE: {DIRECT / PEDAGOGIQUE / PROVOCATEUR / TECHNIQUE} → {justification}

STRATEGIE RECOMMANDEE:
- Perimetre: {SEO seul / Search global / ...}
- Scenario recommande: {Pilotage / Production / Acceleration} ({budget}/mois) — {justification}
- Phase 1 "Diagnostic & activation prioritaire" (90 jours):
  - M1 · Cadrage & audit: {livrables}
  - M2 · Quick wins & fondations: {actions}
  - M3 · Activation & premiers resultats: {KPIs}
- Phase 2 "Run" ({scenario}):
  - Intensite: {Pilotage = 1 priorite/mois | Production = 2 priorites/mois | Acceleration = 3+ priorites/mois}
  - Piliers actives: {lesquels, en lien avec les leviers prioritaires}
  - M4-M6: {trajectoire concrete}

ROI (intervalle) :
- Methode utilisee: {chaine de trafic / ETV proxy}
- Chaine de calcul : H1 x H2 x H3 = resultat (chaine visible dans le simulateur)
- Hypotheses (avec intervalle) :
  - H1: {description} = {basse} - {haute} | {High/Med/Low} [src: {source}]
  - H2: {description} = {basse} - {haute} | {High/Med/Low} [src: {source}]
  - ...
- ROI intervalle : x{N_bas} - x{N_haut} sur {periode}
- ROI affiche : x{N_bas} (borne basse conservatrice)
- Confidence globale: {High/Medium/Low}
- Si Low sur 2+ hypotheses: "Recommandation conditionnelle, validation en Phase 1"

CAS CLIENTS RETENUS:
- Cas {N}: {nom}
  match_criteria: {ce qui rend ce cas similaire: secteur, problematique, taille, profil decideur}
  key_metric: {le chiffre-cle qui convaincra, ex: "x3.8 trafic hors-marque en 12 mois"}
  sdb_juxtaposition: {quel bloc SDB mettre en regard, ex: "SEARCH_STATE 80% marque → cas 92% marque"}
  angle: {angle de presentation pour CE prospect, 1-2 phrases}
- Cas {N}: {nom}
  match_criteria: {idem}
  key_metric: {idem}
  sdb_juxtaposition: {idem}
  angle: {idem}

BRAND_CONTEXT:
  CONTEXTE_TAB: {YES | NO}
  Conditions remplies: {liste}
  Sources contexte: {fichiers Drive ou NONE}
  Piliers de marque: {liste ou NON IDENTIFIES}
  Personas: {B2C: liste, B2B: liste, ou NONE}

RED FLAGS: {liste}
GREEN FLAGS: {liste}

SERVICE_DESCRIPTIONS (contextualise depuis context/service_catalog.md):
- Audit SEO (ligne budget): "{description contextualisee 1-2 lignes}"
- Audit SEO (description proposition): "{description contextualisee 3-5 lignes}"
- {Si REFONTE = OUI} AMOA Technique SEO (ligne budget): "{description contextualisee}"
- {Si REFONTE = OUI} AMOA Technique SEO (description proposition): "{description contextualisee}"
- {Si contenus dans perimetre} Contenus SEO (ligne budget): "{description contextualisee}"
- {Si SEA_SIGNAL = EXPLICIT} Audit SEA (ligne budget): "{description contextualisee}"
- Accompagnement SEO run (ligne budget): "{description contextualisee}"
- {Si SEA_POSTURE != HORS_PERIMETRE} Accompagnement SEA run (ligne budget): "{description contextualisee}"
Variables utilisees: secteur={}, dimensions={}, nb_concurrents={}, contraintes={}, type_refonte={}, agence_tech={}

NARRATIVE_HINTS (suggestions pour Pass 2, non-contraignant):
- Hint 1: {bloc SDB A} + {bloc SDB B} → argument "{nom de l'argument}"
- Hint 2: {bloc SDB C} + {bloc SDB D} → argument "{nom}"
- Hint 3: {bloc SDB E} → argument "{nom}" (standalone)
- ... (3-5 hints max)

=== FIN SDB ===
```
