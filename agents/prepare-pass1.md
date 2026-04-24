# PASS 1 : DATA & STRATEGY ENGINE

> **Prerequis :** `agents/shared.md` lu, puis `agents/prepare.md` (router).

## Role

Collecter, structurer, analyser. Produire un document intermediaire factuellement complet. **Aucune decision narrative ni visuelle dans cette passe.**

---

## Etape 1.1 : Collecte en 2 phases (CONTEXTE puis SEO)

> **Specs detaillees de chaque module :** `context/references/collection-modules.md`
> **Templates SDB et INTERNAL-DIAG :** `context/references/sdb-template.md`

> **Pourquoi 2 phases ?** Les appels SEO (DataForSEO, GSC, Ads, Website Crawl) dependent du domaine principal et du brief prospect. Lancer ces appels AVANT d'avoir lu le brief risque d'analyser le mauvais domaine ou de gaspiller du budget API sur un axe non prioritaire. Phase A collecte le contexte, Phase B collecte les donnees SEO sur le bon domaine.

### Phase A : Collecte contexte (PARALLELE)

Lancer en parallele :

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

### Etape 1.1b : Lecture brief + Cartographie domaines (SEQUENTIEL, OBLIGATOIRE avant Phase B)

**Apres** que la Phase A est terminee (Pipedrive + Drive collectes), l'agent effectue 2 operations sequentielles AVANT tout appel SEO.

#### b1. Lecture du brief prospect

Lire les sources dans l'ordre de priorite :
1. Transcripts Drive (type `transcript`)
2. Notes closer Drive (type `notes_closer`)
3. Documents prospect Drive (type `document_prospect`)
4. Notes Pipedrive
5. Emails Pipedrive

Extraire et **ecrire dans un fichier dedie** :

**Ecriture obligatoire :** `.cache/deals/{deal_id}/artifacts/BRIEF_EXTRACT.md`

```markdown
# Brief Prospect — Deal {deal_id}
GENERATED_AT: {ISO timestamp}
SOURCES: {liste des fichiers lus, ex: "transcript-r1.txt, notes.json, brief-client.txt"}

## Demande explicite
"{verbatim exact du prospect}"

## Priorite declaree
{Ads / SEO / les deux / refonte / autre}
Source : "{verbatim qui justifie cette classification}"

## Douleur
"{verbatim exact}"

## Partenaires existants
- {nom} : {perimetre} — {CHALLENGE ou ARTICULE}

## Business type
{Multi-sites / E-commerce / Service B2B / Contenu-media / Local unique}

## Ce qui n'a PAS ete demande mais qu'on recommande
- {axe} — {pourquoi}

## Verbatims cles (a reutiliser dans la proposition)
- "{verbatim 1}" — contexte : {ou et quand}
- "{verbatim 2}" — contexte : {ou et quand}
- "{verbatim 3}" — contexte : {ou et quand}
```

**Pourquoi un fichier separe ?** Ce fichier est lu par le devil's advocate (Etape 1.2d) comme point d'ancrage independant des analyses. C'est la voix non filtree du prospect. Le contenu est aussi recopie dans le SDB a la fin de Pass 1.

**Le `business_type` detecte est transmis au collector-website (Phase B) pour un crawl cible par archetype de page.**

#### b2. Cartographie des domaines

L'agent identifie et classe TOUS les domaines mentionnes dans les sources. Aucun appel DataForSEO ne peut etre lance sans domaine principal confirme.

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

**Output :** Ajouter les champs `DOMAINE_PRINCIPAL`, `DOMAINES_SECONDAIRES` et `BUSINESS_TYPE` au debut du SDB.

### Validation des noms de concurrents R1 (OBLIGATOIRE)

Après la cartographie des domaines, l'agent DOIT vérifier les noms des concurrents cités par le prospect en R1 via une recherche SERP (`serp_organic_live_advanced` sur "{nom} + {secteur}").

**Pourquoi :** les noms cités oralement peuvent être mal orthographiés (ex: "Okobo" → en réalité "Ocobo", domaine ocobo.co). Un benchmark sur le mauvais domaine invalide toute l'analyse concurrentielle.

**Procédure :**
1. Pour chaque concurrent cité en R1, lancer `serp_organic_live_advanced` sur "{nom} {secteur}"
2. Identifier le domaine réel dans les résultats
3. Vérifier que le domaine correspond au bon secteur (pas un homonyme)
4. Utiliser le domaine vérifié pour le benchmark, pas le nom supposé

### Phase B : Collecte SEO (PARALLELE, sur domaine confirme)

> **Prerequis :** domaine principal confirme (Etape 1.1b), brief lu, business_type identifie.

Lancer en parallele les collecteurs SEO :

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
| **11** | Website Crawl | TOUJOURS (avant diagnostic) | Sitemap, crawl par archetype (`business_type`), CTA, schema |

**Execution DataForSEO :** TOUS les appels via `python3 tools/batch_dataforseo.py` en 5 lots sequentiels. Voir `context/references/collection-modules.md` section "Strategie d'execution DataForSEO".

**Collector-website :** passer `--business-type {business_type}` pour un crawl cible par archetype de page (cf. `.claude/agents/collector-website.md`).

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

3. **Gestion des echecs (fallback par analyste) :**

| Analyste | Si echec (timeout ou erreur) | Impact sur le flow |
|----------|------------------------------|-------------------|
| **analyst-technical** | Degradation : analyst-strategy utilise les donnees brutes du crawl (website cache). Noter "analyse technique non disponible, diagnostic base sur donnees brutes" dans evidence log. | Le diagnostic technique sera moins structure mais les donnees existent. |
| **analyst-content** | Degradation : analyst-strategy utilise les ranked_keywords et le crawl. | Le diagnostic contenu sera base sur les metriques, pas sur l'analyse qualitative. |
| **analyst-competitive** | Degradation : analyst-strategy utilise le benchmark brut (competitors_domain, rank_overview). | Le gap concurrentiel sera chiffre mais pas interprete. |
| **analyst-geo** | Ignorer (conditionnel). | Pas d'impact si GEO n'est pas dans le perimetre. Si GEO est dans le perimetre, noter "analyse GEO non disponible" au Checkpoint 1. |
| **analyst-devil-advocate** | **CRITIQUE** : relancer 1 fois. Si echec au 2e essai, l'agent principal execute le challenge manuellement (lire les analyses, appliquer la grille des 8 angles, documenter dans DEVIL_ADVOCATE.md). Ne JAMAIS diagnostiquer sans challenge. |

4. **Documenter les echecs dans l'evidence log :**
```
SUBAGENT_STATUS:
  analyst-technical: {OK / FAILED (reason) / TIMEOUT}
  analyst-content: {OK / FAILED / TIMEOUT}
  analyst-competitive: {OK / FAILED / TIMEOUT}
  analyst-geo: {OK / SKIPPED (not activated) / FAILED / TIMEOUT}
  analyst-devil-advocate: {OK / FAILED / MANUAL_FALLBACK}
```

### Budget temps
- Cible : 30-45 secondes par analyste (pas d'appels API, que de la lecture + analyse)
- Timeout : 90 secondes par analyste. Au-dela, appliquer le fallback ci-dessus.
- Si 2+ analystes OBLIGATOIRES echouent → avertir le closer au Checkpoint 1 : "Analyse partielle, les dimensions {X} et {Y} sont basees sur les donnees brutes."

---

## Etape 1.2a-bis : Confrontation croisee (OBLIGATOIRE, apres analyses)

> **Pourquoi ?** Les analystes travaillent en silos. Chacun produit un score et des conclusions sans connaitre les conclusions des autres. Cela peut generer des contradictions non detectees (ex: analyst-content recommande de produire du contenu alors que analyst-technical a detecte que 76% des pages ne sont pas indexees). La confrontation croisee detecte ces incoherences AVANT le diagnostic strategique.

### Procedure

1. **Extraire les conclusions cles de chaque analyste** (lire les fichiers analysis/*.md)

Pour chaque analyste, extraire :
- Score global
- Top 3 conclusions (problemes OU forces)
- Recommandation principale

2. **Construire la matrice de confrontation**

```
=== CONFRONTATION CROISEE ===

ANALYST-TECHNICAL ({score}/100) :
  1. {conclusion 1}
  2. {conclusion 2}
  3. {conclusion 3}
  → Recommandation : {reco}

ANALYST-CONTENT ({score}/100) :
  1. {conclusion 1}
  2. {conclusion 2}
  3. {conclusion 3}
  → Recommandation : {reco}

ANALYST-COMPETITIVE :
  1. {conclusion 1}
  2. {conclusion 2}
  3. {conclusion 3}
  → Recommandation : {reco}

ANALYST-GEO ({score}/100 ou N/A) :
  1. {conclusion 1}
  ...
```

3. **Detecter les contradictions**

Verifier systematiquement ces patterns de contradiction :

| Pattern | Contradiction | Resolution |
|---------|--------------|------------|
| Content dit "produire du contenu" + Technical dit "indexation cassee" | Produire du contenu sur un site qui n'indexe pas = effort gaspille | Prioriser l'indexation AVANT la production de contenu |
| Technical dit "site performant" + Competitive dit "gap technique vs concurrent" | Contradiction sur l'etat technique relatif | Distinguer technique absolue (OK) vs technique relative (en retard) |
| Content dit "E-E-A-T fort" + Competitive dit "concurrent domine en contenu" | Contradiction sur la force editoriale | Verifier si la force est qualitative (E-E-A-T) mais pas quantitative (couverture) |
| GEO dit "absent de l'IA Search" + Technical dit "schema riche" | Contradiction sur la citabilite | Le schema existe mais le contenu n'est pas structure pour la citation IA |
| Content dit "quick wins position 10-30" + Technical dit "CWV rouge" | Quick wins SEO inaccessibles si perf bloque le ranking | Les quick wins ne livreront leur plein effet qu'apres correction CWV |

4. **Documenter les contradictions resolues**

**Output :** Ecrire dans `.cache/deals/{deal_id}/analysis/CONFRONTATION.md` :

```markdown
# Confrontation croisee — Deal {deal_id}
GENERATED_AT: {ISO timestamp}

## Contradictions detectees : {N}

### Contradiction 1 : {titre court}
- Analyste A dit : "{conclusion}"
- Analyste B dit : "{conclusion}"
- Resolution : {comment on tranche, avec source}
- Impact sur le diagnostic : {comment ca change la priorisation}

### Contradiction 2 : ...

## Coherences fortes (renforcement mutuel)
- {dimension A} + {dimension B} convergent vers : {insight}
- ...

## Metriques de confiance echantillon
- analyst-technical : analyse basee sur {N} pages / {total sitemap} — Confiance echantillon : {HIGH/MEDIUM/LOW}
- analyst-content : analyse basee sur {N} pages / {total sitemap} — Confiance echantillon : {HIGH/MEDIUM/LOW}
```

**Regles :**
- Si 0 contradiction detectee → documenter quand meme ("Pas de contradiction identifiee. Les analyses convergent.")
- Chaque contradiction doit etre **resolue** (pas juste signalee). L'agent tranche avec une source.
- Les contradictions resolues sont transmises a `analyst-strategy` via le fichier CONFRONTATION.md
- Budget temps : < 15 secondes (lecture + raisonnement, pas d'appel API)

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

## Etape 1.2d : Devil's Advocate (OBLIGATOIRE, avant diagnostic)

> **Pourquoi avant le diagnostic ?** L'approfondissement (1.2c) est execute par le meme agent qui va diagnostiquer. Le biais de confirmation est structurel. Le devil's advocate est un **subagent separe** qui challenge les donnees et pre-conclusions AVANT que le diagnostic soit formalise. Il ne challenge pas un diagnostic deja ecrit (trop tard pour reorienter), il force l'agent a confronter des contre-arguments avant de trancher.

**Spawner** un subagent `analyst-devil-advocate` :

```
Tu es le devil's advocate du systeme SLASHR.
Deal ID : {deal_id}
Domaine : {domain}

Tu recois les analyses et les donnees assemblees. Ton job : argumenter CONTRE l'intervention SLASHR et contre les pre-conclusions qui emergent des analyses.
Lis ton agent spec dans .claude/agents/analyst-devil-advocate.md puis execute le challenge.
Ecris ton output dans .cache/deals/{deal_id}/analysis/DEVIL_ADVOCATE.md.
```

**Attente et integration :**
1. Attendre l'output du devil's advocate
2. Lire `.cache/deals/{deal_id}/analysis/DEVIL_ADVOCATE.md`
3. **Integrer dans le diagnostic (Etape 1.3)** : chaque challenge valide doit etre adresse dans le diagnostic. Chaque challenge rejete doit etre documente avec la raison du rejet. Le diagnostic est plus solide quand il a survecu a un adversaire.

**Output dans le SDB :**

```
DEVIL_ADVOCATE_RESOLVED:
  Challenges recus : {N}
  Acceptes (pre-conclusions ajustees) : {N} — {liste courte}
  Rejetes (pre-conclusions confirmees) : {N} — {liste courte}
  Impact sur le diagnostic : {ce qui a change grace au challenge}
```

**Regles :**
- Le devil's advocate ne peut PAS bloquer le process. Il challenge, l'agent principal decide.
- Si le devil's advocate detecte un probleme CRITIQUE (mauvais domaine, donnee manifestement fausse, desalignement total brief/analyses), c'est un hard stop : corriger avant de diagnostiquer.
- Budget temps : < 30 secondes (lecture + raisonnement, pas d'appel API)

---

## Etape 1.2e : Checkpoint verification browser (CONDITIONNEL)

> **Declencheur :** cette etape est obligatoire si le crawl technique a detecte `bot_protection: "detected"` OU si le devil's advocate a identifie des findings NON VERIFIE necessitant une cross-validation navigateur.

**Objectif :** demander au closer de verifier dans son navigateur les findings qui ne peuvent pas etre cross-valides automatiquement (GSC indisponible ou insuffisant pour trancher).

**Procedure :**
1. Lister les findings NON VERIFIE restants apres la cross-validation GSC
2. Pour chaque finding, formuler une question claire et verifiable en 30 secondes :

```
Avant de finaliser le diagnostic, peux-tu verifier ces points dans ton navigateur ?
- [ ] {url}/robots.txt → le fichier s'affiche normalement ? Copie-colle le contenu.
- [ ] {url}/sitemap.xml → le fichier se telecharge ou s'affiche ?
- [ ] {url fiche produit} → clic droit > code source > chercher "ld+json" → tu vois du schema ?
- [ ] {url categorie} → la page a du contenu texte au-dessus des produits ?
```

3. Attendre les reponses du closer
4. Mettre a jour les niveaux de confiance : les findings confirmes passent a VERIFIE, les infirmes sont retires du diagnostic

**Si le closer repond :**
- Mettre a jour les analyses techniques avec les corrections
- Documenter dans l'evidence log : `[src: browser-check, {element}, {date}]`

**Si le closer ne peut pas verifier (pas d'acces, pas le temps) :**
- Les findings restent NON VERIFIE
- Les exclure des outputs clients
- Les mentionner dans le fichier INTERNAL comme "a verifier"

---

## Etape 1.3 : Diagnostic strategique

**Objectif :** a partir de toutes les donnees collectees, de la checklist d'analyse, de l'approfondissement contextuel ET des challenges du devil's advocate, identifier ce qui bloque le plus de valeur et ce qui peut la debloquer.

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
- **COMPLETENESS obligatoire.** Le SDB doit commencer par le bloc COMPLETENESS (cf. `context/references/sdb-template.md`). Si verdict = INSUFFISANT, STOP. Ne pas diagnostiquer.
- **Causalite sourcee (R25/R26).** Toute phrase du SDB qui attribue une cause a un constat de performance doit citer la source de verification directe. "Position 25 parce que contenu insuffisant" est interdit sans word count ou extraction source.

**Champs requis par Pass 2 (a remplir au Checkpoint 1 si non remplis par le diagnostic) :**

Le SDB et l'INTERNAL-DIAG doivent contenir ces champs pour que Pass 2 puisse fonctionner correctement. Si un champ ne peut pas etre rempli automatiquement par le diagnostic, le Checkpoint 1 demande au closer de le remplir.

| Champ | Source | Utilise par Pass 2 pour |
|-------|--------|------------------------|
| TONE_PROFILE | Diagnostic (profil decideur) ou Checkpoint 1 (closer) | Calibrer le ton de la narration |
| ARC_CHOICE_RATIONALE | Diagnostic (pattern donnees) | Choisir l'arc narratif |
| CLOSER_ANGLE | Checkpoint 1 Q2 (reponse closer) | Hook et subtitle du hero |
| CLOSER_INSIGHTS | Checkpoint 1 (points non-mesurables du closer) | Enrichir les transitions narratives |
| RED_FLAGS | Checkpoint 1 Q3 (objections anticipees par le closer) | Construire les FAQ pre-emptives |
| CAS_CLIENTS_SELECTION | Checkpoint 1 Q4 (validation closer) | Onglet Cas Clients |

Si le closer ne repond pas a une question du Checkpoint 1, le champ est marque `[NON RENSEIGNE]` et Pass 2 utilise un default conservateur (TONE_PROFILE = DIRECT, CAS_CLIENTS = selection automatique par secteur).

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
