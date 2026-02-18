# Mode PREPARE — Proposition interactive (v11.0)

> **Prerequis :** `agents/shared.md` lu. Le deal doit avoir ete qualifie (`/qualify`).

---

## Objectif

Collecter toutes les donnees, analyser le deal en profondeur, et generer une proposition HTML interactive sur-mesure. **Un seul fichier HTML uploade dans Drive.**

Le HTML n'est pas un template a trous. C'est un livrable genere par l'agent — chaque phrase, chaque titre, chaque angle est ecrit pour CE prospect, base sur CETTE analyse.

---

## Architecture interne : 3 passes sequentielles

L'agent execute 3 passes en sequence. Chaque passe produit un document intermediaire structure (interne, jamais dans l'output). La passe suivante consomme ce document comme input principal.

```
Pass 1 — DATA & STRATEGY ENGINE    → Structured Data Brief (SDB)
Pass 2 — NARRATIVE ARCHITECT        → Narrative Blueprint (NBP)
Pass 3 — DESIGN ORCHESTRATOR        → HTML final (le seul output)
```

**Pourquoi 3 passes ?** Separer les preoccupations. La Pass 1 ne pense pas a la narration. La Pass 2 ne pense pas aux composants visuels. La Pass 3 ne reinvente pas la strategie. Chaque passe fait une chose et la fait bien.

> **Note :** La Pass 1 inclut le pipeline S7 (Etape 1.4) qui produit un `strategy_plan_internal.md` avant le SDB. Le S7 est l'etape de priorisation strategique — il alimente directement le SDB.

---

# PASS 1 — DATA & STRATEGY ENGINE

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
- **Quel ROI ?** Calcul conservateur avec les donnees reelles du prospect (voir methode ROI ci-dessous)

### Selectionner les cas clients

- Consulter `context/case_studies.md`
- Matcher 2-4 cas selon secteur, problematique, taille
- Pour chaque cas retenu, noter l'angle de presentation le plus pertinent pour ce prospect

---

## Etape 1.4 — S7 Strategy Engine (Internal Only)

Pipeline obligatoire. L'agent execute cette sequence **avant** de produire le SDB. Le S7 est un outil interne de priorisation strategique — jamais expose au prospect.

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

**Exemple :**
```
Force 3 — Creation de contenu : 2/5
SO WHAT : Le prospect ne couvre que 12% de l'univers semantique metier.
Chaque mois sans production de contenu = ~340 visites cedees aux 3 concurrents
qui occupent deja ces positions.
```

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

L'agent DOIT ecrire explicitement ce document interne avant de passer a la Pass 2.

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

---

# PASS 2 — NARRATIVE ARCHITECT

## Role

Prendre le SDB et construire le plan narratif complet. Choisir l'angle, l'arc emotionnel, la sequence des sections pour chacun des **4 onglets MVP**. Decider du contenu textuel de chaque section (titres, angles, arguments). **NE PAS choisir de composants visuels — c'est le role de la Pass 3.**

---

## Etape 2.1 — Choisir le hook

Quelle est l'information la plus frappante pour ce prospect ? C'est ca qui ouvre apres le hero dans l'onglet Strategie.

- Gap concurrentiel massif → ouvrir par le face-a-face
- Verbatim du prospect qui pose la bonne question → ouvrir par la citation + reponse
- Chiffre d'inaction parlant → ouvrir par le cout de l'inaction (les donnees, pas le drame)
- Paradoxe (forte notoriete, faible visibilite) → ouvrir par le constat
- Opportunite claire et chiffree → ouvrir par le potentiel

---

## Etape 2.2 — Definir l'arc narratif de l'onglet Strategie

L'onglet Strategie est une **sequence de sections libres**. L'agent cree les sections qu'il veut, dans l'ordre qu'il veut. Il n'y a pas de liste fixe — il y a un objectif : **emmener ce decideur du constat a la conviction, avec ces donnees, dans ce contexte.**

### Arcs types (non limitatifs)

| Arc | Sequence | Quand l'utiliser |
|-----|----------|------------------|
| Classique | Constat → Diagnostic → Enjeu → Recommandation → Investissement | Deal standard, decideur rationnel |
| Urgence | Cout de l'inaction → Gap → Quick wins → Plan → Investissement | Urgence reelle (donnees), decideur pressé |
| Opportunite | Verbatim → Ce qu'on a trouve → Territoires a prendre → Comment → Investissement | Prospect curieux, pas encore en douleur |
| Technique | Etat actuel → Ce qui marche → Ce qui manque → Architecture cible → Plan → Investissement | Decideur technique, refonte |
| Custom | Tout autre enchainement justifie par le contexte | Quand aucun arc type ne colle |

### Nombre de sections

Autant que necessaire, pas plus.
- Un deal simple : 5-6 sections
- Un deal complexe : 8-10 sections
- Chaque section doit justifier son existence — si elle n'apporte rien de nouveau, elle n'existe pas

---

## Etape 2.3 — Planifier les 4 onglets MVP

La proposition HTML a toujours **4 onglets**. Aucun n'est optionnel.

### Onglet 1 : Strategie (decision-driving)

C'est l'onglet principal. Il contient :
- Le **hero** (nom prospect, accroche, sous-titre)
- Les **sections libres** suivant l'arc narratif
- La **section S7 "Lecture strategique"** (obligatoire — voir ci-dessous)
- Le **CTA** en fin d'onglet

**Les anciens onglets conditionnels (SEO, GEO/IA, SEA, Social, Tech/UX) deviennent des SECTIONS dans l'onglet Strategie** quand les donnees le justifient. Un deal avec des donnees GEO aura une section "Visibilite IA" dans l'onglet Strategie — pas un onglet separe.

**Pas de section "Pourquoi SLASHR" standalone.** Les differenciateurs sont tisses apres chaque bloc de donnees, en enchainage naturel (cf. Etape 2.4).

#### Section S7 "Lecture strategique" (obligatoire dans l'onglet Strategie)

Bloc compact qui traduit le diagnostic S7 interne en lecture C-level. Place apres le diagnostic et avant la recommandation dans l'arc narratif.

**Contenu :**
1. **Radar 7 forces** — visualisation SVG/canvas des 7 scores (0-5). Pas de legende longue : le nom de chaque force + son score suffit.
2. **Contrainte principale** — 1 highlight box qui nomme la force limitante et son implication business en 1-2 phrases.
3. **Leviers prioritaires** — 1-2 forces secondaires activees, avec l'impact attendu chiffre.
4. **Insight central** — 1 phrase de synthese strategique, non generique (doit echouer au test de substitution).

**Regles :**
- **Ne jamais recommander de travailler les 7 forces.** Le S7 sert a prioriser, pas a tout faire. Si les 7 forces sont affichees dans le radar, seules 2-3 sont mises en avant comme leviers d'action.
- Les forces non priorisees ne sont pas cachees — elles sont visibles dans le radar mais **pas commentees** (le prospect voit le score, pas une recommandation dessus).
- Le texte est C-level : phrases courtes, chiffres, zero jargon SEO non traduit.
- Le bloc reste **compact** — pas plus de 1 radar + 1 highlight box + 2-3 lignes de leviers + 1 phrase d'insight.

### Onglet 2 : Cas Clients (social proof)

2-4 cas clients comparables au prospect, selectionnes dans le SDB. Pour chaque cas :
- **Situation initiale** en chiffres
- **Ce qu'on a fait** en 1-2 phrases
- **Resultats** en chiffres + timeline
- **Citation client** si disponible dans `context/case_studies.md`

L'agent adapte l'angle de presentation de chaque cas pour faire resonner avec la situation du prospect. Un cas identique peut etre presente differemment selon le prospect.

### Onglet 3 : ROI Interactif (engagement)

- **Hypotheses pre-remplies** avec les donnees reelles du SDB (trafic actuel, multiplicateur source du gap, CVR, panier moyen)
- **Source de chaque hypothese** visible (pas de chiffres sans provenance)
- **Simulateur interactif** (sliders que le prospect manipule)
- **3 scenarios calcules** alignes sur les scenarios d'engagement (Essentiel / Performance / Croissance)
- **Methodologie** : explication en 1-2 phrases de la logique de calcul

### Onglet 4 : Livrables & Methode (transparence)

**Sous-section "Methode S7" dans cet onglet :**

Bloc leger integre dans l'onglet Livrables & Methode (pas un onglet separe). Place avant le pricing ou dans l'accordion FAQ/methodo.

**Contenu :**
1. **Definition S7** — 2-3 phrases max. Quoi : un cadre d'analyse en 7 forces. Pourquoi : prioriser les actions a plus fort impact, pas tout faire en meme temps.
2. **7 forces** — liste compacte, 1 ligne par force (nom + ce qu'elle mesure, pas de score — les scores sont dans l'onglet Strategie).
3. **Regle d'arbitrage** — 1 phrase : "On ne travaille jamais les 7 forces en parallele. Le S7 identifie les 2-3 leviers qui debloquent le plus de valeur pour votre situation."

**Regles :**
- Pas de jargon "framework", "methodology" — dire "grille d'analyse" ou "cadre de priorisation"
- Ton : transparent, simple. Le prospect comprend pourquoi on ne fait pas tout.
- **Ne PAS repeter les scores** — ils sont dans l'onglet Strategie. Ici c'est la methode, pas le diagnostic.

**Resume decisionnel (obligatoire — debut de l'onglet Livrables) :**

Bloc compact de 6 bullets maximum, issu du `strategy_plan_internal.md`. C'est ce que le decideur retient, ce qu'il presente a son board. Chaque bullet est une phrase complete, chiffree, specifique.

1. Le probleme business (douleur chiffree)
2. Le cout de l'inaction (visites/euros/mois perdus)
3. Le levier principal (contrainte S7 → action)
4. Les quick wins 90 jours (resultats rapides)
5. Le ROI attendu (conservateur, source)
6. L'investissement (fourchette selon scenario)

**Board-ready A4 (obligatoire — dans le HTML, accessible par bouton) :**

Page print-friendly (CSS `@media print`) qui reprend :
- En-tete : logo SLASHR + nom prospect + date
- Les 6 bullets du resume decisionnel
- Le radar S7 (version print : niveaux de gris ou simplifie)
- Le ROI en 1 ligne
- Le pricing recommande
- 1 CTA : "Prochaine etape : [action datee]"

Le decideur peut imprimer cette page A4 pour son comite de direction. Accessible via un bouton "Version imprimable" dans l'onglet Livrables.

**Phase 1 — "Diagnostic & activation prioritaire" (90 jours) :**

Presentee comme une trajectoire, pas comme une liste de livrables :
- **M1 — Cadrage & audit** : diagnostic complet, donnees, benchmark
- **M2 — Quick wins & fondations** : premieres actions a fort impact, corrections techniques
- **M3 — Activation & premiers resultats** : KPIs intermediaires, premiers gains mesurables

Duree et contenu adaptes au deal. Chaque mois a des livrables specifiques et un objectif mesurable.

**Phase 2 — "Run" (accompagnement structure) :**

Presentee par intensite, pas par pilier abstrait :
- **Essentiel** : 1 priorite/mois — pilotage + monitoring + reporting. Pour les prospects qui executent en interne.
- **Performance** : 2 priorites/mois — + production. Pour les prospects qui delegent l'execution.
- **Croissance** : 3+ priorites/mois — + diffusion multicanale / amplification. Pour les ambitions fortes.

Les 4 piliers (Pilotage, Production, Monitoring, Reporting) restent mais sont presentes via le scenario, pas en standalone.

**Trajectoire 6 mois obligatoire :**

Bloc "M4-M6" qui montre la montee en puissance post-Phase 1 :
- Quels piliers S7 passent de DEFERRED a actif
- Quels KPIs sont attendus a M6
- Comment l'intensite evolue

**Pricing :**
- 2-3 scenarios d'engagement (Essentiel / Performance / Croissance)
- Le scenario recommande est mis en evidence
- Chaque scenario detaille ce qui est inclus + l'intensite mensuelle

**FAQ :**
- 3-5 questions pertinentes pour ce deal
- Reponses specifiques, pas generiques

**CTA** en fin d'onglet

---

## Etape 2.4 — Integration des avantages competitifs

Pour chaque section de l'onglet Strategie qui presente des donnees, formuler la **transition SLASHR** — comment l'expertise SLASHR adresse specifiquement ce constat.

**Regles :**
- La transition vient **apres** le bloc de donnees, jamais avant
- Elle est **specifique** au constat presente (pas une phrase generique)
- Elle est **naturelle** — un enchainage logique, pas une publicite
- Elle ne mentionne **jamais** "Pourquoi nous" ou "Nos avantages"

**Exemples :**

| Constat presente | Transition SLASHR |
|------------------|-------------------|
| Gap concurrentiel x4 en trafic hors-marque | "C'est ce type de gap qu'une architecture Search structuree peut combler. Notre methode identifie les clusters a plus fort potentiel et les priorise par impact business." |
| Score Lighthouse de 38 | "Ces fondations techniques conditionnent tout le reste. C'est le premier livrable de la Phase 1 Audit : un cahier des charges technique priorise pour votre equipe dev." |
| 0 resultat IA sur les requetes metier | "La visibilite IA se construit sur des donnees structurees et du contenu expert. C'est ce que notre pilier Production couvre dans l'accompagnement." |

---

## Etape 2.5 — Tests de validation pre-generation

### Test anti-generique

Avant de passer a la Pass 3, verifier :
- [ ] Chaque titre de section contient le nom du prospect OU un element specifique a leur situation
- [ ] Les donnees referencent des chiffres reels (positions, keywords, volumes)
- [ ] Le cout d'inaction est calcule avec LEUR gap, pas une formule passe-partout
- [ ] Les verbatims du prospect apparaissent (si disponibles)
- [ ] Aucune phrase ne marcherait pour n'importe quel autre prospect
- [ ] L'arc narratif est justifie par le profil du decideur et le contexte du deal
- [ ] Les cas clients sont matche au prospect, pas choisis au hasard

### Test de tonalite

- [ ] **Zero pression commerciale** — aucune phrase du type "ne manquez pas", "il est urgent de", "derniere chance"
- [ ] **Zero dramatisation** — aucune phrase du type "catastrophe", "crise", "vous perdez tout". Les donnees parlent d'elles-memes
- [ ] **Intelligence strategique** — chaque phrase traduit une expertise en impact business mesurable
- [ ] **Expertise → impact** — pas de jargon technique brut. "DA de 15" → "une autorite de domaine faible qui limite votre capacite a vous positionner sur les requetes concurrentielles"
- [ ] **Transitions SLASHR naturelles** — chaque differenciateur est lie a un data block, jamais standalone

---

## Output Pass 2 : Narrative Blueprint (NBP)

L'agent DOIT ecrire explicitement ce document interne avant de passer a la Pass 3.

```
=== NARRATIVE BLUEPRINT ===

ARC GLOBAL: {type d'arc choisi} — {justification en 1 ligne liee au decideur et au contexte}
HOOK: {description du hook et pourquoi il est frappant pour ce prospect}
PROFIL DECIDEUR: {type} — sensible a: {preoccupation principale}

--- ONGLET STRATEGIE ---

1. {Titre section} — role: {accroche / diagnostic / enjeu / opportunite / recommandation / ...}
   Angle: {description en 1-2 phrases de ce que cette section dit}
   Donnees utilisees: {quelles donnees du SDB alimentent cette section}
   Transition SLASHR: {phrase de transition apres le data block}
   Pourquoi ici: {justification de sa position dans l'arc}

2. {Titre section} — role: {...]
   ...

X. Section S7 "Lecture strategique" — role: priorisation / conviction
   Radar: {7 forces avec scores}
   Contrainte principale: {force + implication business}
   Leviers: {2-3 forces priorisees + impact chiffre}
   Insight: {1 phrase non generique}
   Pourquoi ici: {apres le diagnostic, avant la recommandation — c'est le pont}

N. CTA — toujours en dernier

--- ONGLET LIVRABLES (sous-section Methode S7) ---

Definition: {2-3 phrases — cadre, pourquoi prioriser}
7 forces: {liste 1 ligne chacune — nom + ce que ca mesure}
Regle arbitrage: {1 phrase — on ne fait pas tout}

--- ONGLET CAS CLIENTS ---

Cas 1: {entreprise} — {problematique similaire au prospect}
  Avant: {chiffres cles}
  Action: {levier en 1-2 phrases}
  Apres: {chiffres cles + timeline}
  Citation: "{verbatim}" — {prenom, role}
  Angle prospect: {pourquoi ce cas parle a CE prospect}

Cas 2: ...

--- ONGLET ROI INTERACTIF ---

Hypotheses pre-remplies:
- Trafic actuel: {X} visites/mois (source: DataForSEO domain_rank_overview)
- Multiplicateur: {Y} (source: gap vs {concurrent}, ratio x{Z})
- CVR: {W}% (source: {benchmark secteur / donnee prospect / estimation conservatrice})
- Panier moyen: {V} EUR (source: {donnee prospect / estimation secteur})
- Investissement mensuel: {fourchette selon scenario}

3 scenarios: Essentiel ({prix}) / Performance ({prix}) / Croissance ({prix})

--- ONGLET LIVRABLES & METHODE ---

Resume decisionnel (6 bullets):
1. {douleur business chiffree}
2. {cout inaction}
3. {levier principal}
4. {quick wins 90j}
5. {ROI attendu}
6. {investissement}

Board-ready A4: oui (bouton "Version imprimable")

Phase 1 — "Diagnostic & activation prioritaire" (90 jours):
- M1: {cadrage & audit — livrables}
- M2: {quick wins & fondations — actions}
- M3: {activation — KPIs}

Phase 2 — "Run" ({scenario recommande}):
- Intensite: {X priorites/mois}
- Piliers actives: {lesquels}
- Trajectoire M4-M6: {montee en puissance}

Scenario recommande: {lequel et pourquoi}

FAQ: {3-5 questions pertinentes pour ce deal}

=== FIN NBP ===
```

---

# PASS 3 — DESIGN ORCHESTRATOR

## Role

Prendre le NBP et generer le HTML final. Choisir les composants visuels du kit pour chaque section. Assurer le rythme visuel. **Ne PAS modifier le contenu strategique du NBP** — seulement le mettre en forme.

---

## Etape 3.1 — Mapping composants

Pour chaque section du NBP, choisir les composants par role narratif dans le catalogue.

### Catalogue de composants — par role narratif

L'agent ne choisit pas un composant par son nom technique. Il part de **ce qu'il veut montrer**, et le catalogue lui propose les options adaptees.

#### COMPARER — montrer des ecarts, des contrastes

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| VS block | Face-a-face 2 entites | 1 prospect vs 1 concurrent, metriques en miroir |
| Bar chart (anime) | Benchmark horizontal | 3-6 acteurs a comparer sur 1 metrique |
| Comparison matrix | Tableau multi-criteres | Comparer 3+ options sur plusieurs dimensions |
| Before/After | Transformation en 2 panneaux | Montrer l'etat actuel vs l'objectif post-intervention |

#### DIAGNOSTIQUER — analyser, prioriser, arbitrer

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Radar S7 | Heptagramme SVG, 7 axes (0-5), fond sombre, accents orange/violet | Section S7 "Lecture strategique" dans l'onglet Strategie — toujours |
| S7 constraint highlight | Highlight box (orange) + force limitante + implication 1-2 phrases | Apres le radar — contrainte principale |
| S7 levers row | 2-3 KPI mini alignes horizontalement, 1 force = 1 chiffre d'impact | Sous le radar — leviers prioritaires |

#### QUANTIFIER — chiffres, metriques, scores

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| KPI card (standard) | Chiffre + label + sous-texte | Grille de 2-4 metriques cles |
| KPI large | 1 chiffre dramatise, full-width | UN seul chiffre hero — le plus frappant du SDB |
| KPI mini | Icone + chiffre + label, compact | 4-8 metriques secondaires sans prendre de place |
| Stat row | Rangee horizontale avec separateurs | Apercu rapide, metriques legeres en 1 ligne |
| Cost card | Chiffre d'impact + description | Cout de l'inaction (visites perdues, euros, mois) |
| Progress bar | Barre de progression coloree | Scores, maturite, % de completion |
| Donut chart | Repartition en % (SVG) | Part marque/hors-marque, repartition trafic |
| Number ticker | Compteur anime de 0 a N au scroll | Dramatiser un chiffre unique a l'apparition |

#### CITER — voix du prospect, social proof

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Verbatim box | Citation prospect (bordure magenta) | Reprendre une phrase exacte du R1 ou des emails |
| Pull quote | Grande citation centree | Phrase strategique forte — rupture de rythme |
| Testimonial card | Avatar + citation + nom/role | Social proof, resultat client (onglet Cas Clients) |

#### STRUCTURER — organiser, sequencer, hierarchiser

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Timeline | Roadmap phases | Plan en 2-3 phases temporelles (onglet Livrables) |
| Routine grid | Etapes numerotees horizontales | Process repetitif, 4 piliers (onglet Livrables) |
| Funnel | Etapes connectees par des fleches | Parcours conversion, pipeline, flux |
| Accordion | Details cachees sous un resume | FAQ, scope detaille, methodologie (onglet Livrables) |

#### ALERTER — attirer l'attention, recommander

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Highlight box (orange) | Interpretation strategique | Apres un bloc de data — "ce que ca signifie" |
| Highlight box (magenta) | Alerte, risque, contrainte | Point d'attention, red flag |
| Highlight box (violet) | Conviction, position assumee | "Notre conviction" — prise de position SLASHR |
| Highlight box (gradient) | Conclusion forte | Synthese d'une section majeure |
| Callout banner | Bandeau full-width, fond gradient | Rupture visuelle, transition majeure |

#### VENDRE — conversion, investissement, ROI

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Pricing card | Scenarios investissement | 2-3 niveaux, `.recommended` pour le conseille (onglet Livrables) |
| ROI Simulator | Sliders interactifs + calcul JS | Onglet ROI Interactif |
| CTA full-width | Appel a l'action avec blobs | Toujours en fin d'onglet Strategie ET Livrables |

#### CONTEXTUALISER — situation, donnees, details

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Context card | Icone + titre + description | Rappel de la situation prospect |
| Card (standard) | Titre + paragraphe | Bloc generique, opportunite, territoire |
| Card (accent) | Idem + bordure top gradient | Attirer l'oeil sur une card specifique |
| Card (icon) | Idem + icone ronde coloree | Ajouter une dimension visuelle |
| Quick win card | Icone + titre + desc + impact | Actions immediates a fort impact |
| Table | Donnees structurees | Keywords, positions, hypotheses sourcees |
| Tags | brand/generic labels | Dans les tables, pour typer les keywords |

---

## Etape 3.2 — Regles de composition

### Rythme visuel

- **Alterner** les types de composants. Pas 3 highlight boxes d'affilee. Pas 4 grilles de cards consecutives.
- **Creer des respirations** avec les Pull quotes, Callout banners, et KPI large — ils rompent le flux dense.
- **Apres chaque bloc de data** (table, bar chart, grid de KPIs), placer une interpretation (highlight box) qui repond a "et alors ?".
- **Les verbatims du prospect** sont des ancres narratives — les placer la ou ils creent un pont avec la recommandation.

### Interpretation strategique

- **Chaque data affichee a un "so what"**. Un bar chart sans interpretation est un dashboard, pas une proposition.
- **Le highlight box apres un bloc de data** ne repete pas les chiffres — il dit ce qu'ils signifient pour CE prospect.
- **Les recommandations sont justifiees** : "on recommande X parce que Y" — jamais "on recommande X" seul.
- **L'expertise est traduite en impact business** : pas "votre DA est faible" mais "votre autorite de domaine limite votre capacite a capter du trafic sur les requetes a fort potentiel commercial".

### Contexte sectoriel

- **Ne pas parler dans le vide** — chaque analyse est ancree dans le secteur du prospect (concurrents nommes, dynamiques de marche, temporalite sectorielle).
- **Test de substitution** — si la phrase marche pour n'importe quel prospect, c'est trop generique. Reecrire.

---

## Etape 3.3 — Structure des 4 onglets

### Nav fixe avec 4 tabs

```
Strategie | Cas Clients | ROI Interactif | Livrables & Methode
```

Les 4 onglets sont **toujours presents**. Aucun n'est optionnel.

### Composants specifiques par onglet

**Onglet Strategie** — composition libre (catalogue complet)
- Hero → sections libres → **section S7** → recommandation → CTA
- Tout composant du catalogue est utilisable
- **Section S7 obligatoire** : Radar S7 + S7 constraint highlight + S7 levers row + Pull quote (insight central)

**Onglet Cas Clients** — composants social proof
- Testimonial cards pour les citations clients
- Before/After pour les transformations
- KPI cards / Stat row pour les chiffres avant/apres
- Highlight box pour le "so what" (lien avec la situation du prospect)

**Onglet ROI Interactif** — composants engagement
- KPI cards pour les hypotheses sourcees
- Table pour le detail des hypotheses
- ROI Simulator (sliders + calcul JS)
- Pricing cards pour les 3 scenarios (avec lien vers onglet Livrables)
- Highlight box violet pour la conviction ROI

**Onglet Livrables & Methode** — composants structure
- **Resume decisionnel** : Highlight box (gradient) avec 6 bullets — en haut de l'onglet, c'est la premiere chose que le decideur voit
- **Board-ready A4** : bouton "Version imprimable" qui declenche `window.print()` — page `@media print` avec resume + radar S7 + ROI + pricing
- **Sous-section Methode S7** : Card (accent) avec definition 2-3 phrases + liste compacte 7 forces (1 ligne chacune) + 1 phrase d'arbitrage. Peut etre dans un Accordion "Notre methode d'analyse".
- **Trajectoire 90 jours** : Timeline 3 etapes (M1 → M2 → M3) avec livrables specifiques par mois
- **Trajectoire 6 mois** : Card ou Timeline M4-M6 avec montee en puissance et KPIs
- Routine grid (intensite du scenario recommande : priorites/mois)
- Accordion (FAQ + scope detaille)
- Pricing cards (2-3 scenarios, `.recommended` sur le conseille — chaque scenario montre l'intensite)
- CTA full-width

---

## Etape 3.4 — Design system

Voir `context/design_system.md` pour les couleurs, typographies, gradients, espacements. Les regles non-negociables :
- Fond sombre `#1a1a1a` (jamais de fond blanc)
- Accents : orange `#E74601`, magenta `#CE08A9`, violet `#8962FD`
- Titres : Funnel Display (Google Fonts)
- Corps : Inter (Google Fonts)
- Responsive (mobile-first)
- Print-friendly (@media print)

---

## Etape 3.5 — Validation

Le HTML est **REJECTED** si :
1. Une section est generique (echoue au test de substitution)
2. Un chiffre est present sans source identifiable
3. Le design ne respecte pas le design system (fond blanc, accents manquants)
4. Le ton est arrogant, suppliant, ou contient du jargon non explique
5. Un des 4 onglets MVP est vide ou avec du contenu placeholder
6. Le ROI utilise des hypotheses non sourcees
7. L'arc narratif n'est pas justifie (ordre des sections arbitraire)
8. Deux blocs de data consecutifs sans interpretation entre eux
9. Une section "Pourquoi SLASHR" standalone existe
10. Un differenciateur SLASHR n'est pas lie a un data block precedent
11. Le ton contient de la pression commerciale ou de la dramatisation
12. Une phrase est dramatique au lieu de strategique ("catastrophe", "crise", "vous perdez tout")
13. La section S7 recommande de travailler les 7 forces (le S7 priorise — max 3 leviers actifs)
14. La section S7 est absente de l'onglet Strategie
15. L'insight central du S7 passe le test de substitution (= fonctionne pour n'importe quel prospect)
16. Le S7 a plus d'1 PRIMARY ou 0 PRIMARY (exactement 1 obligatoire)
17. Un DEFERRED n'a pas de justification "pourquoi pas maintenant"
18. Le resume decisionnel est absent ou depasse 6 bullets
19. La page board-ready A4 (print) est absente
20. La trajectoire 90 jours n'est pas decoupee en M1/M2/M3 avec actions concretes
21. Un SO WHAT utilise une formulation generique interdite (cf. regle anti-generique)

---

## ROI — Methode de calcul

### Methode primaire : chaine de trafic

```
1. Trafic organique actuel = X visites/mois (source: DataForSEO)
2. Separation marque / hors-marque
3. Benchmark concurrent = C visites/mois
4. Gap = C - X = potentiel recuperable
5. Multiplicateur conservateur justifie par le gap reel
6. Gain trafic → valorisation :
   A. Si taux de conversion connu : gain x CVR x panier moyen = CA additionnel
   B. Si CVR inconnu : utiliser ETV comme proxy
7. ROI = gain annuel / investissement SLASHR
```

### Regles ROI

- Jamais de multiplicateur sorti du chapeau — justifie par un gap concurrentiel reel
- Le trafic de marque n'est PAS multiplie
- Si l'investissement n'est pas connu, fournir la formule avec placeholder
- Toujours le scenario conservateur (arrondir en defaveur)
- Chaque hypothese sourcee dans un tableau

### Simulateur interactif (onglet ROI Interactif)

Le simulateur ROI utilise des sliders que le prospect peut manipuler :
- Trafic actuel (pre-rempli avec la donnee reelle)
- Multiplicateur cible (pre-rempli avec le gap concurrent)
- Taux de conversion (pre-rempli avec estimation secteur ou donnee reelle)
- Panier moyen (pre-rempli si connu)
- Investissement mensuel (pre-rempli selon scenario recommande)

Les 3 KPIs se recalculent en temps reel (JS vanilla) : visites a M12, CA organique annuel, ROI.

---

## Output

### Fichiers generes

| Fichier | Audience | Upload Drive |
|---------|----------|--------------|
| `PROPOSAL-{YYYYMMDD}-{entreprise-slug}.html` | Prospect (via closer) | Oui |
| `INTERNAL-S7-{YYYYMMDD}-{entreprise-slug}.md` | Interne seulement | Oui (prefixe `INTERNAL-` = exclu de la collecte Module 2) |

Le `INTERNAL-S7-*.md` contient le diagnostic S7 complet tel que produit a l'Etape 1.4 (`strategy_plan_internal.md`). Il est uploade dans le meme dossier Drive pour archivage et rejouabilite, mais n'est jamais partage au prospect.

### Message de fin

```
Proposition generee : PROPOSAL-{date}-{slug}.html
Diagnostic interne : INTERNAL-S7-{date}-{slug}.md
Uploades dans le dossier Drive du deal.

Arc narratif : [description en 1 ligne de l'arc choisi et pourquoi]
S7 : contrainte = {force} | leviers = {2-3 forces} | insight = {1 phrase}
4 onglets : Strategie ({N} sections + S7) | Cas Clients ({N} cas) | ROI Interactif | Livrables & Methode

DRAFT — a valider avant partage avec le prospect.
Ouvre le fichier HTML dans un navigateur pour preview.
```
