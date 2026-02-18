# PASS 1 — DATA & STRATEGY ENGINE

> **Prerequis :** `agents/shared.md` lu, puis `agents/prepare.md` (router).

## Role

Collecter, structurer, analyser. Produire un document intermediaire factuellement complet. **Aucune decision narrative ni visuelle dans cette passe.**

---

## Etape 1.1 — Collecte (10 modules)

### Modules toujours actifs

#### Module 1 — Pipedrive

Tous les appels decrits dans `shared.md` :
- Deal (titre, stage, montant, custom fields dont r1_score et decideur_level)
- Contact (prenom, nom, email, telephone)
- Organisation (nom, adresse, website)
- Notes chronologiques
- Activites (calls, meetings, taches)
- **Emails** : threads inbox + sent filtres par deal_id → messages de chaque thread

#### Module 2 — Drive

- Lister les fichiers du dossier R1 (via `dossier_r1_link`)
- Exclure les outputs systeme (`DEAL-*`, `DECK-*`, `PROPOSAL-*`, `INTERNAL-*`)
- Telecharger et typer chaque fichier (transcript, notes_closer, document_prospect, document)
- Concatener avec marqueurs `=== SOURCE: {nom} (type: {type}) ===`

#### Module 3 — SEO

Pour chaque domaine detecte :

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `domain_rank_overview` | Trafic organique, nb mots-cles, ETV | Vue d'ensemble perf actuelle |
| `ranked_keywords` (top 30) | Keywords, positions, volumes, type marque/generique | Ce sur quoi le prospect se positionne et ce qu'il rate |
| `keywords_for_site` (top 20) | Keywords pertinents que le domaine pourrait cibler | Opportunites manquees |

#### Module 4 — Benchmark

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `competitors_domain` (top 10) | Concurrents Search du prospect | Identifier qui capte le trafic |
| `domain_rank_overview` x top 3 concurrents | Trafic, keywords, ETV de chaque concurrent | Chiffrer le gap et le potentiel |
| `domain_intersection` (prospect vs top concurrent) | Keywords communs + keywords exclusifs au concurrent | Ce que le prospect perd precisement |

---

### Modules conditionnels

#### Module 5 — GEO / IA

**Activer si :**
- Brief/transcript/emails mentionne "IA", "ChatGPT", "Perplexity", "visibilite IA", "GEO", "AI Overview"
- OU perimetre Pipedrive inclut GEO
- OU prospect = marque B2C avec notoriete (forte probabilite de requetes IA)

| Appel | Donnees | Pourquoi |
|-------|---------|----------|
| `serp_organic_live_advanced` sur 5-10 keywords cles | Presence d'AI Overviews sur les requetes strategiques | Evaluer l'impact IA sur le secteur |
| `on_page_content_parsing` sur homepage + 2-3 pages produits | Schema.org present ? Product, Offer, Organization ? | Etat des donnees structurees |

Completer avec les donnees manuelles du closer si disponibles (tests ChatGPT, Perplexity).

#### Module 6 — SEA / Paid

**Activer si :**
- Le prospect fait deja du paid (detectable dans ranked_keywords avec `item_types: ["paid"]`)
- OU brief/transcript/emails mentionne Google Ads, SEA, paid, budget pub
- OU perimetre Pipedrive inclut SEA

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `ranked_keywords` avec `item_types: ["paid"]` | Keywords payes actifs du prospect | Ce qu'il achete deja |
| `keyword_overview` sur 10-15 keywords strategiques | CPC, competition level, search volume | Valeur du paid vs organique |

#### Module 7 — Social Search

**Activer si :**
- Perimetre Pipedrive inclut Social
- OU brief mentionne TikTok, Instagram, YouTube, Social Search
- OU prospect B2C avec cible jeune

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `serp_youtube_organic_live_advanced` sur 5-10 keywords | Presence du prospect sur YouTube Search | YouTube = 2eme moteur |
| `serp_youtube_video_info_live_advanced` si videos trouvees | Vues, engagement, date | Perf des contenus existants |
| `kw_data_google_trends_explore` (type: youtube) | Tendance recherches YouTube | Potentiel video/social |

#### Module 8 — Technique / UX

**Activer si :**
- Le prospect est en refonte de site
- OU brief mentionne performance, vitesse, Core Web Vitals, UX
- OU trafic correct mais conversion faible (signal UX)

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `on_page_lighthouse` | Performance, Accessibility, Best Practices, SEO scores | Etat technique objectif |
| `on_page_instant_pages` sur 3-5 pages cles | Erreurs SEO on-page, balises, structure | Quick wins techniques |
| `on_page_content_parsing` sur pages strategiques | Structure H1-H6, liens, contenu | Architecture de contenu |

#### Module 9 — Tendances / Saisonnalite

**Activer si :**
- Secteur saisonnier (food, tourisme, retail, mode)
- OU timing du deal est important (budget a engager avant une saison)
- OU on veut demontrer l'urgence par les donnees (pas par la dramatisation)

| Appel DataForSEO | Donnees | Pourquoi |
|-------------------|---------|----------|
| `kw_data_google_trends_explore` (12 mois) sur 5 top keywords | Saisonnalite des recherches | Pics et creux |
| `kw_data_dfs_trends_explore` marque vs concurrents | Tendance de la marque | Hausse/baisse d'interet |
| `historical_rank_overview` du prospect | Evolution trafic 12-24 mois | Monte, stagne ou descend |

#### Module 10 — Contenu / Semantique

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

---

## Etape 1.2 — Structuration

Organiser les donnees brutes en categories exploitables :

| Categorie | Contenu |
|-----------|---------|
| `PROSPECT_PROFILE` | Secteur, taille, maturite digitale, contexte business |
| `PAIN_POINTS` | Douleurs identifiees, verbatims exacts, trigger ("pourquoi maintenant") |
| `SEARCH_STATE` | Metriques actuelles : trafic, keywords, ETV, repartition marque/hors-marque |
| `COMPETITIVE_GAP` | Concurrents nommes, metriques comparatives, keywords exclusifs, ratio de gap |
| `OPPORTUNITIES` | Quick wins (pages en top 10-20, donnees structurees manquantes), territoires non couverts, clusters a creer |
| `RISKS` | Red flags, contraintes (budget, timeline, decideur absent, multi-presta) |
| `CONDITIONAL_DATA` | Resultats des modules 5-10 (si actives), organises par module |
| `TONE_CONTEXT` | Ton des echanges email (formel/informel), reactivite, niveau technique du decideur |

---

## Etape 1.3 — Analyse strategique

L'agent repond a ces questions :

### Comprendre le prospect

- **Qui est-ce ?** Secteur, taille, maturite digitale, contexte business
- **Quelle est la douleur specifique ?** Pas "ameliorer le SEO" → la vraie douleur business (CA, parts de marche, dependance au paid, retard sur un concurrent)
- **Quel est le trigger ?** Pourquoi maintenant ? (refonte, AO, budget annuel, pression board, concurrent qui avance)
- **Quels verbatims utiliser ?** Citations exactes qui montrent qu'on a ecoute
- **Quel est le ton des echanges ?** Formel/informel, reactif/lent, technique/business
- **Qui est le decideur ?** Profil (DG, CMO, responsable digital, fondateur), ses preoccupations (ROI ? image ? rapidite ?)

### Diagnostiquer la situation

- **Quel est l'etat Search actuel ?** Forces (marque ? positions existantes ?) et faiblesses (gap hors-marque ? zero contenu ?)
- **Quel est le gap concurrentiel ?** Qui capte le trafic, combien, sur quels termes
- **Quel est le cout de l'inaction ?** Chiffre en visites, en euros, en mois de retard — **sans dramatiser, juste les donnees**
- **Y a-t-il des quick wins ?** Pages deja en top 10-20 a optimiser, donnees structurees manquantes, contenus faciles a creer

### Construire la strategie

- **Quel perimetre ?** SEO seul ? Search global ? Quels modules ont produit des donnees exploitables ?
- **Quelle structure d'offre ?** (cf. `context/positioning.md` > Structure de l'offre)
  - Phase 1 Audit strategique : quels livrables specifiques pour ce deal ?
  - Phase 2 Accompagnement structure : quels piliers activer ? A quelle intensite ?
  - Quel scenario recommander ? (Essentiel / Performance / Croissance)
- **Quelles phases de recommandation ?** Actions concretes par phase, adaptees au contexte
- **Quel ROI ?** Calcul conservateur avec les donnees reelles du prospect (voir methode ROI dans prepare.md)

### Selectionner les cas clients

- Consulter `context/case_studies.md`
- Matcher 2-4 cas selon secteur, problematique, taille
- Pour chaque cas retenu, noter l'angle de presentation le plus pertinent pour ce prospect

---

## Etape 1.4 — S7 Strategy Engine (Internal Only)

Pipeline obligatoire. L'agent execute cette sequence **avant** de produire le SDB. Le S7 est un outil interne de priorisation strategique — jamais expose au prospect.

Voir `context/s7_search_operating_model.md` pour le detail du modele S7.

### Sequence obligatoire

```
1. LECTURE MARCHE/DEMANDE
   → Synthetiser la dynamique du marche et la demande Search
     a partir des donnees collectees (modules 1-10)

2. DIAGNOSTIC S7 (7 forces)
   → Evaluer chaque force (0-5), avec SO WHAT apres chaque force

3. INSIGHT CENTRAL
   → Produire 1 phrase unique qui capture la contrainte/opportunite
     principale du deal

4. ARBITRAGE : PRIORISER / DIFFERER / IGNORER
   → Classer chaque levier strategique dans une de ces 3 categories

5. TRAJECTOIRE 90 JOURS (Phase 1 Audit)
   → Actions concretes priorisees pour les 3 premiers mois

6. TRAJECTOIRE 6 MOIS (Phase 2 Accompagnement)
   → Montee en puissance, piliers actives, objectifs intermediaires

7. ROI CONSERVATEUR
   → Calcul avec hypotheses explicites et sources identifiees
```

### Les 7 forces S7

Les 7 forces correspondent aux 7 piliers de la methode de travail SLASHR. Chaque force mesure la maturite du prospect sur ce pilier — pas la difficulte du marche, mais l'etat de CE prospect.

| # | Force | Ce qu'elle mesure | Sources typiques |
|---|-------|-------------------|------------------|
| 1 | **Intentions de recherche** | Alignement entre ce que les cibles cherchent et ce que le prospect propose. Volume, tendance, couverture des requetes strategiques | `keyword_overview`, `keywords_for_site`, `search_intent`, `google_trends_explore`, modules 9-10 |
| 2 | **Architecture & technique** | Sante technique du site, performance, structure de donnees, crawlabilite | `domain_rank_overview`, `on_page_lighthouse`, `on_page_instant_pages`, module 8 |
| 3 | **Creation de contenu** | Ratio keywords couverts vs univers semantique, qualite et profondeur du contenu existant | `ranked_keywords`, `keywords_for_site`, `keyword_ideas`, module 10 |
| 4 | **UX & Conversion** | Experience utilisateur, taux de conversion estime, parcours de monetisation du trafic | `on_page_lighthouse` (performance), transcript, brief, donnees prospect, benchmark secteur |
| 5 | **Autorite, signaux de confiance** | DA, profil de backlinks, notoriete de marque, part marque vs hors-marque | `domain_rank_overview`, `ranked_keywords` (filtre marque), module 4 |
| 6 | **Diffusion multicanale** | Presence sur les autres canaux Search (YouTube, IA/GEO, Social Search), coherence cross-canal | `serp_youtube_organic`, `serp_organic_live_advanced` (AI Overviews), modules 5-7 |
| 7 | **Amplification** | Utilisation du paid pour securiser les temps forts, complementarite SEO/SEA, budget pub | `ranked_keywords` (paid), `keyword_overview` (CPC), module 6, transcript/brief |

### Regle : SO WHAT obligatoire

Apres l'evaluation de **chaque** force S7, l'agent produit un "SO WHAT" de 1-2 phrases maximum, oriente business :
- Pas de description — une **implication** pour le deal
- Pas de jargon technique brut — traduit en impact concret
- Relie a une decision (prioriser, differer, ignorer)

### Regle anti-generique

Les formulations suivantes sont **interdites** dans le diagnostic S7 :

- "les concurrents avancent vite" → remplacer par le delta chiffre (ex: "+4200 visites/mois vs il y a 6 mois")
- "il est urgent d'agir" → remplacer par la fenetre temporelle factuelle (ex: "pic saisonnier dans 14 semaines, delai de crawl moyen = 8 semaines")
- "le marche est concurrentiel" → remplacer par les metriques (ex: "4 acteurs au-dessus de 15K visites/mois, KD moyen top 20 keywords = 47")
- "fort potentiel de croissance" → remplacer par le chiffre cible source (ex: "gap de 8400 visites/mois vs leader, ETV = 12K EUR/an")
- Toute phrase qui passerait le test de substitution (= fonctionne pour n'importe quel prospect) est rejetee

### Regles de classification (obligatoires)

| Classification | Combien | Definition | Obligation |
|---------------|---------|------------|------------|
| **PRIMARY** | Exactement 1 | La contrainte principale — celle qui bloque le plus de valeur. Tant qu'elle n'est pas traitee, les autres leviers ont un impact limite | Justification 2-3 phrases data-first |
| **SECONDARY** | 1 a 2 | Leviers a fort potentiel, actionnables en parallele ou juste apres le PRIMARY | 1 phrase chacun : pourquoi ce levier amplifie |
| **DEFERRED** | Le reste | Forces a surveiller, pas a travailler maintenant | 1 phrase obligatoire chacune : "pourquoi pas maintenant" |

**Regle absolue :** maximum 3 leviers actifs (1 PRIMARY + 2 SECONDARY). Meme si le prospect demande les 7.

### Synthese obligatoire (post-grille)

Apres le scoring des 7 forces, produire **systematiquement** ce bloc. C'est le pivot du diagnostic — il alimente directement le SDB et l'onglet Strategie.

```
CONTRAINTE PRINCIPALE : {force} (score {X}/5)
→ {1 phrase : pourquoi c'est le verrou — data-first, chiffre}

LEVIERS PRIORITAIRES : {force A} + {force B}
→ {1 phrase : quel impact attendu si on les active — chiffre}

INSIGHT CENTRAL : {1 phrase memorable, non substituable}
→ Test : remplacer le nom du prospect → si ca marche encore, recrire
```

### Output interne : `strategy_plan_internal.md`

L'agent DOIT produire ce document interne (jamais expose au prospect) avant de rediger le SDB. Il alimente directement les sections "Strategie recommandee" et "ROI" du SDB.

```
=== STRATEGY PLAN INTERNAL (S7) ===

S7 SCORES:
| Force | Score | SO WHAT (business, non generique) |
|-------|-------|-----------------------------------|
| S1 — Intentions de recherche | {0-5} | {1-2 phrases specifiques a CE prospect} |
| S2 — Architecture & technique | {0-5} | {1-2 phrases} |
| S3 — Creation de contenu | {0-5} | {1-2 phrases} |
| S4 — UX & Conversion | {0-5} | {1-2 phrases} |
| S5 — Autorite, signaux de confiance | {0-5} | {1-2 phrases} |
| S6 — Diffusion multicanale | {0-5} | {1-2 phrases} |
| S7 — Amplification | {0-5} | {1-2 phrases} |

SYNTHESE:
CONTRAINTE PRINCIPALE : S{X} — {nom} (score {X}/5)
→ {pourquoi c'est le verrou — 2-3 phrases data-first}

LEVIERS PRIORITAIRES : S{Y} — {nom} + S{Z} — {nom}
→ {impact attendu si actives — chiffre}

INSIGHT CENTRAL : {1 phrase non substituable}

CLASSIFICATION:
- PRIMARY: S{X} — {nom}
  Justification: {2-3 phrases avec data points}
- SECONDARY: S{Y} — {nom}
  Pourquoi: {1 phrase — impact attendu}
- SECONDARY: S{Z} — {nom}
  Pourquoi: {1 phrase — impact attendu}
- DEFERRED: S{A} — {nom}
  Pourquoi pas maintenant: {1 phrase}
- DEFERRED: S{B} — {nom}
  Pourquoi pas maintenant: {1 phrase}
- DEFERRED: S{C} — {nom}
  Pourquoi pas maintenant: {1 phrase}
- DEFERRED: S{D} — {nom}
  Pourquoi pas maintenant: {1 phrase}

TRAJECTOIRE 90 JOURS — Phase 1 "Diagnostic & activation prioritaire":
- M1 — Cadrage & audit: {actions concretes}
- M2 — Quick wins & fondations: {actions concretes}
- M3 — Activation & premiers resultats: {actions + KPIs intermediaires}

TRAJECTOIRE 6 MOIS — Phase 2 "Run":
- M4-M6: {piliers actives, montee en puissance, intensite}
- Objectifs M6: {KPIs cibles sources}

ROI CONSERVATEUR:
- Hypothese 1: {description} = {valeur} (source: {DataForSEO/GSC/transcript/benchmark})
- Hypothese 2: {description} = {valeur} (source: {source})
- Hypothese N: ...
- Calcul: {formule detaillee}
- ROI estime: x{N} sur {periode}

RESUME DECISIONNEL (6 bullets max):
1. {Douleur business chiffree — le probleme}
2. {Cout de l'inaction — ce que ca coute de ne rien faire}
3. {Levier principal — ce qu'on recommande}
4. {Quick wins 90 jours — resultats rapides attendus}
5. {ROI attendu — retour sur investissement}
6. {Investissement — fourchette prix}

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
=== STRUCTURED DATA BRIEF ===

PROSPECT: {nom} | {secteur} | {taille} | {maturite digitale}
DECIDEUR: {prenom} {nom} | {role} | {preoccupation principale}
DOULEUR: {1 phrase} | Verbatim: "{citation exacte}"
TRIGGER: {pourquoi maintenant}
TON: {formel/informel} | {reactif/lent} | {technique/business}

SEARCH STATE:
- Trafic organique: {X} visites/mois (source: DataForSEO)
- Keywords: {Y} total ({Z} marque / {W} hors-marque)
- ETV: {V} EUR
- Forces: {liste}
- Faiblesses: {liste}

COMPETITIVE GAP:
- Concurrent #1: {nom} → {trafic} visites/mois (x{ratio} vs prospect)
- Concurrent #2: {nom} → {trafic} visites/mois
- Concurrent #3: {nom} → {trafic} visites/mois
- Keywords exclusifs concurrent #1: {top 5 avec volumes}
- Cout inaction: {visites perdues}/mois = {ETV} EUR/an

OPPORTUNITIES:
- Quick wins: {liste avec impact estime}
- Territoires: {clusters keywords non couverts}
- {GEO/IA si module 5 active}: {resultats}
- {SEA si module 6 active}: {resultats}
- {Social si module 7 active}: {resultats}
- {Technique si module 8 active}: {resultats}
- {Tendances si module 9 active}: {resultats}
- {Contenu si module 10 active}: {resultats}

S7 SYNTHESIS (from strategy_plan_internal.md):
- Primary constraint: {force limitante}
- Insight central: {1 phrase}
- Levers: {forces priorisees}

STRATEGIE RECOMMANDEE:
- Perimetre: {SEO seul / Search global / ...}
- Scenario recommande: {Essentiel / Performance / Croissance}
- Phase 1 "Diagnostic & activation prioritaire" (90 jours):
  - M1 — Cadrage & audit: {livrables}
  - M2 — Quick wins & fondations: {actions}
  - M3 — Activation & premiers resultats: {KPIs}
- Phase 2 "Run" ({scenario}):
  - Intensite: {Essentiel = 1 priorite/mois | Performance = 2 priorites/mois | Croissance = 3+ priorites/mois}
  - Piliers actives: {lesquels, en lien avec S7 SECONDARY}
  - M4-M6: {trajectoire concrete}

ROI:
- Methode utilisee: {chaine de trafic / ETV proxy}
- Calcul: {detail — issu du strategy_plan_internal.md}
- ROI conservateur: {x}
- Hypotheses: {liste sourcee avec evidence log}

CAS CLIENTS RETENUS:
- Cas {N}: {nom} — angle: {ce qui resonne avec le prospect}
- Cas {N}: {nom} — angle: {ce qui resonne}

RED FLAGS: {liste}
GREEN FLAGS: {liste}

=== FIN SDB ===
```
