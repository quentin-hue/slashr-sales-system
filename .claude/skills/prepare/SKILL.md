---
name: prepare
description: Genere la proposition HTML interactive sur-mesure — 3 passes internes (Data & Strategy, Narrative, Design), 4 onglets MVP, uploadee dans Drive.
disable-model-invocation: true
---

# PREPARE — Proposition HTML interactive

**Deal ID :** $ARGUMENTS

## Prerequis

Le deal doit avoir ete qualifie (`/qualify`). Score >= 60 (GO) ou CONDITIONNEL valide par le manager.

## Etapes

1. Lis `agents/shared.md` (preambule partage : role, sources, regles)
2. Lis `agents/prepare.md` (processus complet en 3 passes sequentielles)
3. Lis `templates/proposal-kit.html` (kit CSS + catalogue de 27 composants organises par role narratif)
4. Suis le processus en 3 passes decrit dans prepare.md :

### Pass 1 — DATA & STRATEGY ENGINE

Collecte + structuration + analyse + **diagnostic S7**. Outputs internes : **`strategy_plan_internal.md`** puis **Structured Data Brief (SDB)**.

**Collecte (10 modules) :**

**Toujours actifs :**
- Module 1 — Pipedrive (deal, contact, org, notes, activites, emails)
- Module 2 — Drive (fichiers du dossier R1, types par prefixe)
- Module 3 — SEO (domain_rank_overview + ranked_keywords top 30 + keywords_for_site top 20)
- Module 4 — Benchmark (competitors_domain top 10 + domain_rank_overview x3 concurrents + domain_intersection)

**Conditionnels (activer selon les criteres decrits dans prepare.md) :**
- Module 5 — GEO / IA
- Module 6 — SEA / Paid
- Module 7 — Social Search
- Module 8 — Technique / UX
- Module 9 — Tendances / Saisonnalite
- Module 10 — Contenu / Semantique

**Structuration :** organiser les donnees en categories (PROSPECT_PROFILE, PAIN_POINTS, SEARCH_STATE, COMPETITIVE_GAP, OPPORTUNITIES, etc.)

**Analyse :** comprendre le prospect, diagnostiquer, construire la strategie, selectionner les cas clients, calculer le ROI.

**S7 Strategy Engine (Etape 1.4) :** pipeline obligatoire avant le SDB.
1. Lecture marche/demande
2. Diagnostic 7 forces (score 0-5 + SO WHAT par force — cf. `context/s7_search_operating_model.md`)
3. Classification : exactement 1 PRIMARY + 1-2 SECONDARY + reste DEFERRED (chaque DEFERRED justifie)
4. Synthese obligatoire : contrainte + leviers + insight central (non substituable)
5. Trajectoire 90 jours (M1/M2/M3) + 6 mois (M4-M6)
6. ROI conservateur (hypotheses explicites)
7. Resume decisionnel (6 bullets max)

Output : **`strategy_plan_internal.md`** sauvegarde dans le dossier Drive du deal (prefixe `INTERNAL-` → exclu des outputs prospect). Ce fichier alimente le SDB.

### Pass 2 — NARRATIVE ARCHITECT

Plan narratif complet. Output interne : **Narrative Blueprint (NBP)**.

- Choisir le hook (quelle info ouvre apres le hero)
- Definir l'arc emotionnel (classique, urgence, opportunite, technique, custom)
- Planifier les **4 onglets MVP** :
  - **Strategie** : arc libre, sections libres + **section S7 "Lecture strategique" obligatoire** (radar 7 forces, contrainte principale, leviers, insight). Les anciens onglets conditionnels (SEO, GEO, SEA, Social, Tech) deviennent des sections DANS Strategie
  - **Cas Clients** : 2-4 cas matche au prospect depuis `context/case_studies.md`
  - **ROI Interactif** : hypotheses pre-remplies + simulateur + 3 scenarios
  - **Livrables & Methode** : **resume decisionnel** (6 bullets) + **board-ready A4** (bouton print) + **sous-section Methode S7** + **trajectoire 90j** (M1/M2/M3) + **trajectoire 6 mois** (M4-M6) + pricing par intensite (Essentiel/Performance/Croissance) + FAQ
- Integrer les avantages competitifs (tisses apres chaque data block, jamais standalone)
- Tests : anti-generique + tonalite (zero pression, zero dramatisation)
- **Regle S7** : ne jamais recommander de travailler les 7 forces — max 3 leviers actifs

### Pass 3 — DESIGN ORCHESTRATOR

Generation HTML. Le seul output visible.

- Mapping composants par role narratif (COMPARER, DIAGNOSTIQUER, QUANTIFIER, CITER, STRUCTURER, ALERTER, VENDRE, CONTEXTUALISER)
- Regles de composition : rythme visuel, "so what" apres chaque data, expertise traduite en impact business
- Structure : 4 onglets toujours presents, nav fixe
- Ce n'est PAS un template a trous. Chaque phrase, titre, section est ecrit pour CE prospect

## Collecte Pipedrive

```bash
TOKEN=$(cat ~/.pipedrive_token)

# Deal
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN"

# Contact
curl -s "https://api.pipedrive.com/v1/persons/{person_id}?api_token=$TOKEN"

# Organisation
curl -s "https://api.pipedrive.com/v1/organizations/{org_id}?api_token=$TOKEN"

# Notes
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}/notes?api_token=$TOKEN"

# Activites
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}/activities?api_token=$TOKEN"

# Emails — filtrer par deal_id cote client
curl -s "https://api.pipedrive.com/v1/mailbox/mailThreads?folder=inbox&api_token=$TOKEN"
curl -s "https://api.pipedrive.com/v1/mailbox/mailThreads?folder=sent&api_token=$TOKEN"
curl -s "https://api.pipedrive.com/v1/mailbox/mailThreads/{thread_id}/mailMessages?api_token=$TOKEN"
```

## Collecte Drive

Le champ `dossier_r1_link` du deal contient l'URL du dossier. Extraire le folder ID, lister et telecharger les fichiers via l'API Google Drive (credentials : `~/.google_service_account.json`).

## Reference

- Field keys Pipedrive : `context/pipedrive_reference.md`
- Kit composants (27 composants, catalogue par role narratif) : `templates/proposal-kit.html`
- Design system : `context/design_system.md`
- Positionnement + structure offre : `context/positioning.md`
- Modele S7 (diagnostic vs activation) : `context/s7_search_operating_model.md`
- Cas clients : `context/case_studies.md`

## Output

2 fichiers uploades dans le dossier Drive du deal :

| Fichier | Audience | Contenu |
|---------|----------|---------|
| `PROPOSAL-{YYYYMMDD}-{entreprise-slug}.html` | **Prospect** (via closer) | Proposition HTML interactive — 4 onglets avec section S7 |
| `INTERNAL-S7-{YYYYMMDD}-{entreprise-slug}.md` | **Interne seulement** | Diagnostic S7 complet (scores, classification PRIMARY/SECONDARY/DEFERRED, synthese, trajectoires, ROI, resume decisionnel, evidence log) |

> Le prefixe `INTERNAL-` garantit que le fichier est exclu des outputs prospect (cf. Module 2 : exclure `DEAL-*`, `DECK-*`, `PROPOSAL-*`, `INTERNAL-*`).

Message de fin :
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
