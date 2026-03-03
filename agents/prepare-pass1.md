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
- Deal (titre, stage, montant, custom fields dont r1_score et decideur_level)
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

#### Module 3b : GSC (Google Search Console) — conditionnel

**Activer si :** le prospect a accorde l'acces Google Search Console au service account SLASHR.

**Detection automatique (apres Etape 1.1b) :** appeler le MCP tool `search_analytics` avec :
- `siteUrl` : `sc-domain:{DOMAINE_PRINCIPAL}` (si echec, essayer `https://www.{DOMAINE_PRINCIPAL}/`)
- `startDate` / `endDate` : 7 derniers jours
- `rowLimit` : 1

Si donnees retournees → acces confirme, continuer la collecte.
Si erreur (403, 404, vide) → pas d'acces API GSC. Tenter le **fallback fichier Drive** ci-dessous avant d'abandonner.

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
| **Critique** | > 25 appels | Modules conditionnels (5-10) : activer max 2, privilegier ceux qui alimentent le PRIMARY S7. Les autres → marquer dans le SDB : "Module {N} non active (budget API consomme, data insuffisante)" |

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
- Le score S1 (Intentions de recherche) — un prospect qui ne couvre ni le commercial ni l'informationnel captable a un score plus bas qu'un prospect qui couvre le commercial mais pas l'informationnel
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

#### Etape post-Module 6 : SEA Signal Classification (OBLIGATOIRE)

Apres l'execution du Module 6 (ou apres la decision de ne pas l'activer), l'agent classe le **signal SEA** du deal. Ce signal est independant du score S7 Amplification : le S7 mesure l'etat actuel (0/5 si pas de paid), le signal mesure la **demande du prospect**.

| Signal | Definition | Sources de detection | Posture SLASHR |
|--------|-----------|---------------------|----------------|
| **EXPLICIT** | Le brief demande du paid | Brief/transcript/emails mentionne : Google Ads, Meta Ads, campagnes paid, budget pub, ROAS, Shopping, Performance Max, retargeting, display | **CONSEIL** (defaut) ou **PILOTE** (si perimetre Croissance) |
| **DETECTED** | Le prospect a du paid actif mais n'en parle pas | Module 6 `ranked_keywords(paid)` retourne des resultats MAIS aucune mention paid dans brief/transcript/emails | Mentionner la synergie SEO/SEA dans la strategie |
| **OPPORTUNITY** | Pas de demande prospect, pas de paid actif, MAIS les donnees montrent une opportunite paid | CPCs bas (< 1.50 EUR) sur keywords commerciaux ET/OU 0 concurrent en paid sur 3+ keywords commerciaux ET/OU SHOPPING_SIGNAL = YES | Mentionner l'opportunite dans le diagnostic + integrer en Phase 2 |
| **ABSENT** | Ni demande, ni activite paid, ni opportunite detectee | Module 6 non active ET aucune mention paid ET aucun signal d'opportunite | DEFERRED-SCOPE standard |

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

**IMPORTANT :** le signal SEA est un routage de la demande prospect, pas un diagnostic. Le diagnostic (S7 Amplification) reste inchange.

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

#### Module 11 : Website Crawl (toujours actif)

Crawle le site reel du prospect pour alimenter les scores S2/S3/S4 avec des donnees concretes (contenu, structure, donnees structurees).

**Execution :** `python3 tools/crawl_site.py {domain} {deal_id}`

**Budget :** 0 appel DataForSEO, max 10 requetes HTTP, 60s total.

**Non-bloquant :** si le crawl echoue (homepage inaccessible, timeout global), le deal continue sans. L'agent note "Module 11 non disponible (site injoignable)" dans l'evidence log et continue avec les donnees DataForSEO seules.

**Output :** 4 fichiers JSON dans `.cache/deals/{deal_id}/website/` :
- `homepage.json` : titre, meta desc, OG, headings, Schema.org, liens, images, CTAs, formulaires
- `sitemap.json` : nombre total URLs, distribution (product/blog/pages/category), ratio editorial vs catalogue
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

`[src: {origine}, {endpoint_ou_fichier}]`

Origines valides : `pipedrive`, `drive`, `dataforseo`, `calcul`, `benchmark`

Exemples :
- Trafic organique: 20,489 visites/mois `[src: dataforseo, domain_rank_overview]`
- CA web 2025: 55,745 EUR `[src: drive, recap_ventes-web.xlsx]`
- CVR implicite: 0.45% `[src: calcul, 1099 commandes / (20489 x 12)]`
- Migration sans perte: 0% `[src: benchmark, cas client 4]`

Les qualificatifs (ex: "maturite digitale faible") ne necessitent pas de source mais doivent pouvoir etre justifies par au moins un data point de l'evidence log.

**Regle :** si un chiffre apparait dans le SDB sans etiquette `[src:]`, il est rejete a la relecture. L'agent corrige avant de passer a Pass 2.

### Ecriture artefacts (obligatoire)
Ecrire :
- `.cache/deals/{deal_id}/artifacts/SDB.md`
- `.cache/deals/{deal_id}/evidence/evidence_log.md`


## Etape 1.3 : Analyse strategique + S7 Engine (bloc unifie)

> **Bloc unifie.** L'analyse strategique et le diagnostic S7 sont executes en une seule passe de raisonnement sur les memes donnees. L'agent produit une analyse plus coherente (pas de risque de contradiction entre diagnostic et S7) et plus rapide (une seule passe).

L'agent repond a ces questions, puis enchaine directement sur le scoring S7 et la strategie, sans relire les donnees.

### A. Comprendre le prospect

- **Qui est-ce ?** Secteur, taille, maturite digitale, contexte business
- **Quelle est la douleur specifique ?** Pas "ameliorer le SEO" → la vraie douleur business (CA, parts de marche, dependance au paid, retard sur un concurrent)
- **Quel est le trigger ?** Pourquoi maintenant ? (refonte, AO, budget annuel, pression board, concurrent qui avance)
- **Quels verbatims utiliser ?** Citations exactes qui montrent qu'on a ecoute
- **Quel est le ton des echanges ?** Formel/informel, reactif/lent, technique/business
- **Qui est le decideur ?** Profil (DG, CMO, responsable digital, fondateur), ses preoccupations (ROI ? image ? rapidite ?)

### B. Diagnostiquer la situation + S7 (en un seul raisonnement)

Pendant le diagnostic, l'agent evalue simultanement les 7 forces S7. Le S7 est un outil interne de priorisation strategique, jamais expose au prospect.

> Echelle 0-5, classification, anchors quantitatifs : voir `agents/prepare-context.md` section 3.
> Modele complet (diagnostic vs activation, piliers, anti-patterns) : voir `context/s7_search_operating_model.md`.

**Questions diagnostic :**
- **Quel est l'etat Search actuel ?** Forces et faiblesses → alimente S1-S5
- **Quel est le gap concurrentiel ?** Qui capte le trafic, combien, sur quels termes → alimente S1, S3, S5
- **Quel est le cout de l'inaction ?** Chiffre en visites, en euros, en mois de retard. **Sans dramatiser, juste les donnees**
- **Y a-t-il des quick wins ?** Pages en top 10-20, donnees structurees manquantes, contenus faciles → alimente S2, S3

**Scoring S7 (7 forces, chacune 0-5 avec SO WHAT) :**

Pour chaque force, l'agent produit :
1. Score (0-5 avec anchor quantitatif)
2. Evidence (1 data point minimum)
3. Confidence (High/Med/Low)
4. SO WHAT (1-2 phrases, implication business, pas description)
5. Projection 6-12M (si donnees disponibles)
6. Interdependance (quelle force conditionne/est conditionnee)

**Sources Module 11 pour le scoring S7 :**
Si le Module 11 a produit des donnees (`crawl_summary.json` disponible), les integrer :

| Force | Source Module 11 | Impact sur le score |
|-------|-------------------|---------------------|
| **S2 · Architecture & technique** | Schema.org coverage, qualite sitemap, structure heading, detection SPA | Sans Schema.org/sitemap/headings → S2 vers le bas |
| **S3 · Contenu** | Ratio editorial vs catalogue, page count, word count moyen, meta manquantes | Peu de contenu editorial, thin content, meta manquantes → S3 vers le bas |
| **S4 · UX / Conversion** | CTAs, formulaires, profondeur navigation, images sans alt | Sans CTA/formulaire, navigation pauvre → S4 vers le bas |

> Rappel : 5 formulations interdites, test de substitution (cf. `agents/prepare-context.md` section 3).

**Synthese S7 (post-grille, obligatoire) :**
Produire : CONTRAINTE PRINCIPALE + LEVIERS PRIORITAIRES + INSIGHT CENTRAL + PROJECTIONS.

### C. Construire la strategie + ROI + trajectoires

Enchaine directement depuis le S7, sans relire les donnees.

- **Quel perimetre ?** SEO seul ? Search global ? Quels modules ont produit des donnees exploitables ?
- **Quelle structure d'offre ?** (cf. `agents/prepare-context.md` section 2, Structure de l'offre)
  - Phase 1 Audit strategique : quels livrables specifiques pour ce deal ?
  - Phase 2 Accompagnement structure : quels piliers activer ? A quelle intensite ?
  - Quel scenario recommander ? (Essentiel / Performance / Croissance)
- **Quelles phases de recommandation ?** Actions concretes par phase, adaptees au contexte
- **Quel ROI ?** Calcul conservateur avec les donnees reelles du prospect (voir methode ROI dans prepare-pass3.md)

**Classification S7 (max 3 leviers actifs) :**
- PRIMARY : S{X} → justification 2-3 phrases data-first
- SECONDARY : S{Y} + S{Z} → 1 phrase chacun
- DEFERRED-SEQUENTIAL : forces a activer quand condition remplie
- DEFERRED-SCOPE : forces hors perimetre

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
- Le plan 90 jours reste aligne sur le PRIMARY S7 : chaque mois doit adresser la contrainte principale

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
- S7 PRIMARY + `RISKS` → "Le verrou et ses consequences"
- `ROI` + `STRATEGIE_RECOMMANDEE` → "Le plan et son rendement"

Les differenciateurs SLASHR emergent des donnees elles-memes dans la proposition (cf. `agents/prepare-pass2.md`, Etape 2.4). Pass 1 ne produit pas de "transition opportunities" explicites.

### Output interne : `strategy_plan_internal.md`

L'agent DOIT produire ce document interne (jamais expose au prospect) avant de rediger le SDB. Il alimente directement les sections "Strategie recommandee" et "ROI" du SDB.

**Ecriture obligatoire :** `.cache/deals/{deal_id}/artifacts/strategy_plan_internal.md` (utilise par Pass 2 et par `/debrief`).

```
=== STRATEGY PLAN INTERNAL (S7) ===

S7 SCORES (avec evidence + confiance):
| Force | Score | Evidence (1 data point minimum) | Confidence | SO WHAT (business) | Projection 6-12M | Interdependance |
|-------|-------|----------------------------------|------------|---------------------|-------------------|-----------------|
| S1 · Intentions | {0-5} | {ex: Intent map: 12 400 req/mois commercial, couverture 6%} | {High/Med/Low} | {1-2 phrases} | {voir regle ci-dessous} | {voir regle ci-dessous} |
| S2 · Arch & tech | {0-5} | {ex: Lighthouse 38, 40% pages non indexees} | {High/Med/Low} | {1-2 phrases} | {idem} | {idem} |
| S3 · Contenu | {0-5} | {ex: 23 pages indexees vs 850 req pertinentes} | {High/Med/Low} | {1-2 phrases} | {idem} | {idem} |
| S4 · UX/CVR | {0-5} | {ex: parcours friction, conversion 100% app} | {High/Med/Low} | {1-2 phrases} | {idem} | {idem} |
| S5 · Autorite | {0-5} | {ex: Domain Rank / part marque vs hors-marque} | {High/Med/Low} | {1-2 phrases} | {idem} | {idem} |
| S6 · Diffusion | {0-5} | {ex: absence YouTube/IA/social sur intents cles} | {High/Med/Low} | {1-2 phrases} | {idem} | {idem} |
| S7 · Amplification | {0-5} | {ex: CPC eleve + dependance paid + saisonnalite} | {High/Med/Low} | {1-2 phrases} | {idem} | {idem} |

INTERDEPENDANCE / SYSTEMIC LIMITATION :
→ PRIMARY (obligatoire) : 1 phrase qui explique pourquoi cette force limite l'ensemble du systeme. Doit faire reference a au moins une autre force.
  Ex: "S3 (Contenu) limite le systeme : sans pages cibles, S1 (Intentions) reste non captee et S5 (Autorite) ne peut pas se construire."
→ SECONDARY (recommande si pertinent) : 1 phrase d'interdependance, comment cette force conditionne ou est conditionnee par d'autres.
  Ex: "Si S2 echoue (migration mal geree) → S3 (contenu) et S1 (intentions) perdent leur base"
→ DEFERRED : optionnel, uniquement si la dependance explique le report ("S6 non priorise car S3 n'a pas encore de contenu a diffuser")
→ Le tiret (—) reste acceptable pour les forces sans interdependance notable.

PROJECTION 6-12 MOIS (obligatoire pour PRIMARY et SECONDARY) :
→ Source : keyword_dynamics (solde new vs lost), historical_rank_overview (si Module 9 actif), tendances concurrents (Module 4c dynamics)
→ Format : "{direction} {delta chiffre} en {horizon}"
  Ex PRIMARY : "Erosion: -31 kw nets/mois pour LMP, +709 nets pour le leader. A ce rythme, gap x2 en 12 mois."
  Ex SECONDARY : "Stagnation: trafic stable +/-5% sur 6 mois mais concurrents en progression de +15%"
→ Si aucune donnee de tendance disponible : "Projection non disponible (pas de donnees historiques)" + ajouter dans MANQUANTS
→ Pour les forces DEFERRED : optionnel mais recommande si la donnee existe
→ Anti-dramatisation : la projection est factuelle. Pas de "catastrophe en vue".

CLASSIFICATION (max 3 leviers actifs) :
- PRIMARY : S{X} (score {X}/5) → {justif 2-3 phrases data-first}
- SECONDARY : S{Y} + S{Z} → {1 phrase chacun : pourquoi amplifie}
- DEFERRED-SEQUENTIAL : {forces} → {1 phrase chacun : "sera active quand {condition}"}
- DEFERRED-SCOPE : {forces} → {1 phrase chacun : "hors perimetre car {raison}"}

EXCEPTION SEA_SIGNAL (obligatoire si SEA_SIGNAL = EXPLICIT) :
Si `SEA_SIGNAL = EXPLICIT`, S7 Amplification ne peut PAS etre DEFERRED-SCOPE. Reclassifier :
- S7 Amplification >= 2 + perimetre Croissance → SECONDARY
- S7 Amplification < 2 + brief EXPLICIT → DEFERRED-SEQUENTIAL ("cadrage SEA strategique M1, activation M3-M4 une fois les fondations Search posees")
- Justification obligatoire : "Le prospect demande un accompagnement paid. Le score {X}/5 confirme l'absence de structure — renforce le besoin de cadrage strategique."

ARC_CHOICE_RATIONALE :
- Arc retenu : {Classique | Urgence | Opportunite | Technique | Custom}
- Raison liee au decideur : {1 phrase — profil decideur + contexte}
- Raison liee aux donnees : {1 phrase — quel pattern dans le SDB oriente cet arc}
- Arc ecarte : {quel arc a ete considere et pourquoi rejete}

ROI DRIVERS (pont vers l'onglet ROI) :
- Driver 1 (Traffic) : {source} → {variable ROI impactée : visites cibles M12}
- Driver 2 (Conversion) : {source} → {variable ROI impactée : CVR / panier}
- Driver 3 (Mix marque/hors-marque) : {source} → {variable ROI impactée : part scalable}

PLAN 90 JOURS (contextuel, aligne PRIMARY, 3 etapes max) :
CONTEXTE STRUCTURANT : {Refonte | AO | Saisonnalite | Standard}
1) M1 · {objectif adapte au contexte} → {livrable} → {signal attendu}
2) M2 · {objectif adapte au contexte} → {livrable} → {signal attendu}
3) M3 · {objectif adapte au contexte} → {livrable} → {signal attendu}

INSIGHT CENTRAL : {1 phrase non substituable}

SYNTHESE:
CONTRAINTE PRINCIPALE : S{X} · {nom} (score {X}/5)
→ {pourquoi c'est le verrou, 2-3 phrases data-first}

LEVIERS PRIORITAIRES : S{Y} · {nom} + S{Z} · {nom}
→ {impact attendu si actives, chiffre}

TRAJECTOIRE 90 JOURS · Phase 1 (contextuelle) :
Contexte : {decrire l'evenement structurant et comment il conditionne le plan}
- M1 · {titre adapte}: {actions concretes liees au contexte}
- M2 · {titre adapte}: {actions concretes liees au contexte}
- M3 · {titre adapte}: {actions concretes liees au contexte}

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

=== FIN STRATEGY PLAN INTERNAL ===
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

S7 SYNTHESIS (from strategy_plan_internal.md):
- Primary constraint: {force} ({score}/5) : {1 phrase data-first sur le verrou}
- Systemic limitation: {1 phrase : pourquoi cette force bloque les autres, reference inter-forces}
- Levers:
  - {SECONDARY force A} ({score}/5) : {impact chiffre attendu si active}
  - {SECONDARY force B} ({score}/5) : {impact chiffre attendu si active}
- Deferred-Sequential (avec condition d'activation) :
  - {force} : sera active quand {condition}, horizon {X mois}
  - {force} : {idem}
- Deferred-Scope (hors perimetre) :
  - {force} : hors perimetre car {raison}
  - {force} : {idem}
- Projection PRIMARY (obligatoire) : {direction} {delta chiffre} {source} → {projection X mois}
- Projection SECONDARY (obligatoire pour chaque) : {direction} {delta} → {horizon}
- Insight central: {1 phrase non substituable}
- Confidence globale S7: {High/Medium/Low}

STRATEGIE RECOMMANDEE:
- Perimetre: {SEO seul / Search global / ...}
- Scenario recommande: {Essentiel / Performance / Croissance}
- Phase 1 "Diagnostic & activation prioritaire" (90 jours):
  - M1 · Cadrage & audit: {livrables}
  - M2 · Quick wins & fondations: {actions}
  - M3 · Activation & premiers resultats: {KPIs}
- Phase 2 "Run" ({scenario}):
  - Intensite: {Essentiel = 1 priorite/mois | Performance = 2 priorites/mois | Croissance = 3+ priorites/mois}
  - Piliers actives: {lesquels, en lien avec S7 SECONDARY}
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

RED FLAGS: {liste}
GREEN FLAGS: {liste}

NARRATIVE_HINTS (suggestions pour Pass 2, non-contraignant):
- Hint 1: {bloc SDB A} + {bloc SDB B} → argument "{nom de l'argument}"
- Hint 2: {bloc SDB C} + {bloc SDB D} → argument "{nom}"
- Hint 3: {bloc SDB E} → argument "{nom}" (standalone)
- ... (3-5 hints max)

=== FIN SDB ===
```
