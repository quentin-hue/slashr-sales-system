# PASS 1 : DATA & STRATEGY ENGINE

> **Prerequis :** `agents/shared.md` lu, puis `agents/prepare.md` (router).

## Role

Collecter, structurer, analyser. Produire un document intermediaire factuellement complet. **Aucune decision narrative ni visuelle dans cette passe.**

---

## Etape 1.1 : Collecte (11 modules)

> **Specs detaillees de chaque module :** `context/references/collection-modules.md`
> **Templates SDB et INTERNAL-DIAG :** `context/references/sdb-template.md`

### Module 1 : Pipedrive

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

### Module 2 : Drive

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

### Etape 1.1b : Cartographie des domaines (OBLIGATOIRE avant Module 3)

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

**Output :** Ajouter les champs `DOMAINE_PRINCIPAL` et `DOMAINES_SECONDAIRES` au debut du SDB.

### Modules 3-11 : Collecte SEO, GSC, Ads, Benchmark, Crawl

> **Specs detaillees :** `context/references/collection-modules.md`

| Module | Nom | Activation | Ce qu'il produit |
|--------|-----|------------|-----------------|
| **3** | SEO (DataForSEO) | TOUJOURS | `domain_rank_overview` + `ranked_keywords` (top 30) + `keywords_for_site` (top 20) |
| **3b** | GSC | TOUJOURS TENTER | Clics, impressions, CTR, positions reelles, quick wins. Prioritaire sur DFS. |
| **3c** | Google Ads | TOUJOURS TENTER | Campagnes, depenses, conversions, CPA reels |
| **4** | Benchmark | TOUJOURS | `competitors_domain` + `domain_rank_overview` x3 concurrents + `domain_intersection` |
| **4b** | Intent segmentation | TOUJOURS | 3 buckets : Commercial / Info captable / Info non-captable |
| **4c** | Niche detection | SI aucun concurrent business en M4 | SERP analysis → concurrents business → TASM |
| **4d** | SERP Features | TOUJOURS (0 appel API) | Features map + SHOPPING_SIGNAL |
| **4e** | Competitive Ads | SI Google Ads + SEA EXPLICIT/DETECTED | Auction insights, paysage paid concurrentiel |
| **4f** | Benchmark Synthesis | TOUJOURS (apres tous 4*) | Synthese structuree = colonne vertebrale narrative |
| **5** | GEO / IA | Brief mentionne IA/GEO OU perimetre GEO OU B2C notoire | AI Overviews, schema.org |
| **6** | SEA / Paid | Paid actif OU brief mentionne Ads OU perimetre SEA | Keywords payes, CPCs |
| **7** | Social Search | Perimetre Social OU brief TikTok/YouTube OU B2C jeune | YouTube Search, Trends |
| **8** | Technique / UX | Refonte OU brief perf/UX OU conversion faible | Lighthouse, instant pages |
| **9** | Tendances | Secteur saisonnier OU timing budget | Trends, historical rank |
| **10** | Contenu | Gap contenu important OU strategie contenu = pilier | keyword_ideas, related, difficulty |
| **11** | Website Crawl | TOUJOURS (avant diagnostic) | Sitemap, crawl echantillon, CTA, schema |

**Execution DataForSEO :** TOUS les appels via `python3 tools/batch_dataforseo.py` en 5 lots sequentiels. Voir `context/references/collection-modules.md` section "Strategie d'execution DataForSEO".

### Budget checkpoint (obligatoire apres Module 4 + 4c)

| Seuil | Appels consommes | Action |
|-------|-----------------|--------|
| **Normal** | < 15 | Continuer normalement |
| **Attention** | 15-25 | Modules 5-10 : activer uniquement ceux avec signal FORT |
| **Critique** | > 25 | Modules 5-10 : max 2, privilegier ceux qui alimentent la contrainte principale |

---

## Etape 1.2 : Structuration

> **Categories SDB et sections conditionnelles :** `context/references/collection-modules.md` section "Structuration SDB"

Organiser les donnees brutes en categories exploitables : `PROSPECT_PROFILE`, `PAIN_POINTS`, `SEARCH_STATE`, `COMPETITIVE_GAP`, `INTENT_MARKET_MAP`, `OPPORTUNITIES`, `RISKS`, `CONDITIONAL_DATA`, `TONE_CONTEXT`, `BRAND_SEARCH_ANALYSIS`, `SERP_FEATURES_MAP`, `SECONDARY_MARKETS`.

Sections conditionnelles : `BRAND_CONTEXT`, `BRAND_SEARCH_ANALYSIS`, `SECONDARY_MARKETS`. Voir `context/references/collection-modules.md` pour les conditions d'activation et le contenu SDB de chacune.

---

## Etape 1.2a : Analyse dimensionnelle (PARALLELE, OBLIGATOIRE)

> **Phase A' — entre la collecte et le diagnostic.** Les 4 analystes lisent le cache des collecteurs et produisent des analyses structurees avec scores, insights, et angles narratifs. Ils ne font **aucun appel API**.

### Lancement parallele

Spawner en parallele (subagent_type indique entre parentheses) :

| Agent | Subagent type | Activation | Input | Output |
|---|---|---|---|---|
| **analyst-technical** | `analyst-technical` | TOUJOURS | website cache + DFS on_page | `analysis/TECHNICAL_ANALYSIS.md` |
| **analyst-content** | `analyst-content` | TOUJOURS | website cache + DFS keywords | `analysis/CONTENT_ANALYSIS.md` |
| **analyst-competitive** | `analyst-competitive` | TOUJOURS | DFS benchmark + SERP data | `analysis/COMPETITIVE_ANALYSIS.md` |
| **analyst-geo** | `analyst-geo` | CONDITIONNEL | SERP data + crawl + schema | `analysis/GEO_ANALYSIS.md` |

**Condition d'activation analyst-geo :** au moins une condition remplie :
- Module 5 (GEO/IA) a ete active dans la collecte
- Brief/transcript/emails mentionne IA, ChatGPT, Perplexity, AI Overview, GEO
- Prospect = marque B2C avec notoriete
- SERP data disponible avec AI Overviews detectees

### Prompt de lancement (pour chaque analyste)

```
Tu es l'analyste {dimension} du systeme SLASHR.
Deal ID : {deal_id}
Domaine : {domain}
{si analyst-competitive : competitors_business : [{liste}]}

Lis ton agent spec dans .claude/agents/analyst-{type}.md puis execute l'analyse.
Ecris ton output dans .cache/deals/{deal_id}/analysis/{OUTPUT_FILE}.
```

### Attente et verification

1. Attendre que les 3-4 analystes terminent (parallele)
2. Verifier que les fichiers output existent :
   - `.cache/deals/{deal_id}/analysis/TECHNICAL_ANALYSIS.md` — OBLIGATOIRE
   - `.cache/deals/{deal_id}/analysis/CONTENT_ANALYSIS.md` — OBLIGATOIRE
   - `.cache/deals/{deal_id}/analysis/COMPETITIVE_ANALYSIS.md` — OBLIGATOIRE
   - `.cache/deals/{deal_id}/analysis/GEO_ANALYSIS.md` — conditionnel
3. Si un analyste echoue → le noter dans l'evidence log, continuer sans (degradation gracieuse). analyst-strategy travaillera avec les donnees brutes pour cette dimension.

### Budget temps
- Cible : 30-45 secondes (pas d'appels API, que de la lecture + analyse)
- Si un analyste depasse 90 secondes → timeout, continuer sans

---

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

**REGLE D'ORDONNANCEMENT : le diagnostic et la proposition suivent la hierarchie du prospect.** Si `BRIEF PROSPECT > Priorite declaree = Ads`, le diagnostic ouvre par l'analyse Ads, la strategie ouvre par les recommandations Ads, et le SEO vient en opportunite complementaire.

### A. Comprendre le prospect

- **Qui est-ce ?** Secteur, taille, maturite digitale, contexte business
- **Quelle est la douleur specifique ?** Pas "ameliorer le SEO" → la vraie douleur business
- **Quel est le trigger ?** Pourquoi maintenant ?
- **Quels verbatims utiliser ?** Citations exactes qui montrent qu'on a ecoute
- **Quel est le ton des echanges ?** Formel/informel, reactif/lent, technique/business
- **Qui est le decideur ?** Profil, preoccupations

### B. Diagnostiquer la situation

L'agent raisonne sur les donnees collectees pour produire un diagnostic strategique. Le diagnostic est un outil interne de priorisation, jamais expose au prospect.

> Rappel : 5 formulations interdites, test de substitution (cf. `agents/prepare-context.md` section 3).

**Output obligatoire :**

```
DIAGNOSTIC STRATEGIQUE
GENERATED_AT: {ISO timestamp}

CONTRAINTE PRINCIPALE : {en langage business, 2-3 phrases data-first}
→ Confiance : {HIGH / MEDIUM / LOW} — {justification}

LEVIERS PRIORITAIRES (max 2) :
1. {levier} — {impact attendu, chiffre source}
   Confiance : {HIGH / MEDIUM / LOW}
2. {levier} — {impact attendu, chiffre source}
   Confiance : {HIGH / MEDIUM / LOW}

CE QU'ON NE FAIT PAS MAINTENANT :
- {axe} — {pourquoi, condition de reactivation}

ROI :
  Methode : {A (Gap CTR) / B (Gap concurrent) / C (Volume adressable)}
  Fourchette : {min} — {max} EUR/an
  Confiance : {HIGH / MEDIUM / LOW}

SCENARIO RECOMMANDE :
  Niveau : {Pilotage / Production / Acceleration}
  Budget : {montant}/mois

TONE_PROFILE : {DIRECT / PEDAGOGIQUE / PROVOCATEUR / TECHNIQUE}
CONFIANCE GLOBALE : {HIGH / MEDIUM / LOW}
```

**Regles :**
- Max 3 leviers actifs (1 contrainte + 2 leviers)
- Chaque conclusion appuyee par des donnees (evidence chain)
- Si les donnees sont insuffisantes, le dire (Confiance Low)
- Le diagnostic est INTERNE. Les conclusions sont traduites en langage business dans le HTML.
- **ROI sans donnees business :** si aucune donnee de conversion n'est disponible (pas d'acces GA4, pas de donnees e-commerce, pas de panier moyen reel), ne PAS estimer de ROI monetaire. Utiliser des metriques trafic : gain de clics/mois, gain de positions, gain de CTR. Le ROI monetaire sera calcule en Phase 1 quand les donnees Analytics seront accessibles. Marquer `ROI Confidence: LOW` dans le SDB.

### C. Construire la strategie + ROI + trajectoires

Enchaine directement depuis le diagnostic, sans relire les donnees.

- **Quel perimetre ?** SEO seul ? Search global ?
- **Quelle structure d'offre ?** (cf. `agents/prepare-context.md` section 2)
  - Phase 1 Audit strategique : quels livrables specifiques ?
  - Phase 2 Accompagnement structure : quels piliers, quelle intensite ?
  - Quel scenario recommander ? (Pilotage / Production / Acceleration)
- **Quelles descriptions de prestations ?** Contextualiser les templates de `context/service_catalog.md` avec les donnees du deal. Produire `SERVICE_DESCRIPTIONS` du SDB.
- **Quelles phases de recommandation ?** Actions concretes par phase
- **Quel ROI ?** Calcul conservateur avec donnees reelles (voir `context/references/roi-methodology.md`)

**Classification diagnostic (max 3 leviers actifs) :**
- Contrainte principale : {axe} → justification 2-3 phrases data-first
- Leviers prioritaires : {axe A} + {axe B} → 1 phrase chacun
- Differe (sequentiel) : axes a activer quand condition remplie
- Differe (hors perimetre) : axes hors perimetre

**Trajectoire 90 jours (contextuelle, JAMAIS generique) :**

Le plan 90 jours est cale sur l'evenement structurant du deal, pas sur un template fixe :

| Contexte | M1 | M2 | M3 |
|----------|----|----|-----|
| **Refonte** (REFONTE = OUI) | Audit + cadrage refonte (specs SEO, architecture cible, plan de migration) | Accompagnement refonte (suivi dev, redirections, recette SEO) | Activation sur le nouveau site (contenu, Merchant Center, tracking) |
| **AO** (contexte AO) | Cadrage perimetre SEO + livrables pour reponse AO | Quick wins pre-AO (gains rapides demonstrables) | Plan strategique post-decision AO |
| **Saisonnalite** (pic saisonnier < 4 mois) | Audit + quick wins cibles sur le pic | Activation contenu saisonnier + optimisations | Mesure impact pic + plan long terme |
| **Standard** (aucun evenement structurant) | Cadrage + audit | Quick wins + structure | Activation + mesure |

**Regles :**
- Le plan est CONSTRUIT AUTOUR de l'evenement structurant, pas a cote
- Si plusieurs contextes se combinent, prioriser celui qui conditionne le reste
- Chaque mois = 1 objectif + 1 livrable + 1 signal de succes
- Le plan reste aligne sur la contrainte principale

**Trajectoire 6 mois :** M4-M6 montee en puissance, piliers actives, objectifs intermediaires. Si SEA_SIGNAL = OPPORTUNITY, integrer l'activation paid en M4+.

**ROI conservateur :** chaque hypothese avec intervalle (borne basse conservatrice / borne haute optimiste realiste). ROI affiche = borne basse.

### D. Selectionner les cas clients

- Consulter `context/case_studies.md`
- Matcher 2-4 cas selon secteur (priorite 1), problematique (priorite 2), taille (priorite 3)
- Pour chaque cas retenu, structurer : `match_criteria`, `key_metric`, `sdb_juxtaposition`, `angle`

### E. Pre-grouper les blocs SDB par argument narratif

L'agent identifie 3-5 "arguments decideurs" et produit les `NARRATIVE_HINTS` dans le SDB.

**Exemples de regroupements typiques :**
- `SEARCH_STATE` + `COMPETITIVE_GAP` → "Le prospect est en retard mesurable"
- `INTENT_MARKET_MAP` + `OPPORTUNITIES` → "Le potentiel existe et est captable"
- Contrainte principale + `RISKS` → "Le verrou et ses consequences"
- `ROI` + `STRATEGIE_RECOMMANDEE` → "Le plan et son rendement"

Les differenciateurs SLASHR emergent des donnees elles-memes dans la proposition (cf. `agents/prepare-pass2.md`, Etape 2.4). Pass 1 ne produit pas de "transition opportunities" explicites.

### Output interne : diagnostic dans le SDB + INTERNAL-DIAG

L'agent produit le diagnostic strategique directement dans le SDB (section `DIAGNOSTIC STRATEGIQUE`). Ce diagnostic est interne (jamais expose au prospect).

Le diagnostic est aussi archive dans un fichier separe pour rejouabilite :
**Ecriture obligatoire :** `.cache/deals/{deal_id}/artifacts/INTERNAL-DIAG.md`

> **Template INTERNAL-DIAG complet :** `context/references/sdb-template.md`

---

## Output Pass 1

> **Templates complets SDB et INTERNAL-DIAG :** `context/references/sdb-template.md`
> **Regles format source, periodes, evidence log :** `context/references/sdb-template.md`

**Ecrire :**
- `.cache/deals/{deal_id}/artifacts/SDB.md` — template SDB complet
- `.cache/deals/{deal_id}/artifacts/INTERNAL-DIAG.md` — template INTERNAL-DIAG
- `.cache/deals/{deal_id}/evidence/evidence_log.md`
