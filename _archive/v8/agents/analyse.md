# Mode ANALYSE — Qualification R1 (v8.0)

> **Prerequis :** `agents/shared.md` lu.

---

## Processus — Passe unique

**Inventaire sources -> Extraction data -> Scoring -> Verdict -> Resume Search**

- Si verdict NURTURE -> brief allege (Sections 1, 4, 6, 7 + metadata). Inclure : raison de disqualification, condition de reactivation, potentiel Search si les donnees le montrent. STOP.
- Si verdict R2_GO ou R2_CONDITIONAL -> brief complet (toutes sections) + resume Search. Rappeler : `/deck {deal_id}`.

---

## Etape 0 — Inventaire des sources

1. Identifier chaque source (type, qualite : complete/partielle/sommaire)
2. Verifier la couverture des **5 questions non negociables** :
   - Q1 : Quel probleme business en termes de CA ?
   - Q2 : Que se passe-t-il si rien dans 6 mois ?
   - Q3 : Qui decide et quel process pour dire oui ?
   - Q4 : Enveloppe budget, meme approximative ?
   - Q5 : En mesure de demarrer ce mois-ci si la reco est pertinente ?
3. Determiner la fiabilite (HAUTE / MOYENNE / BASSE)
4. Si aucune source exploitable -> STOP : "Dossier R1 vide ou inexploitable"

## Etape 1 — Extraction structuree

- Parser **toutes les sources** (Pipedrive + fichiers Drive) pour extraire les champs du brief
- Priorite si info dans plusieurs sources : transcript > notes > document > email > Pipedrive (notes/activites)
- L'identite prospect (entreprise, contact, org) vient en priorite de Pipedrive — les fichiers completent
- Les verbatims critiques (douleur, urgence, budget) viennent des fichiers. Si pas de transcript -> "PAS DE TRANSCRIPT — VERBATIMS NON DISPONIBLES"
- Detecter le role reel de l'interlocuteur (decideur vs influenceur)
- **Marqueurs de donnees manquantes :**
  - `NON MENTIONNE` = le sujet n'a pas ete aborde (transcript complet disponible). C'est un signal.
  - `NON DOCUMENTE` = on ne sait pas, les sources ne couvrent pas ce point. Pas un signal.
  - Regle : si transcript complet disponible et info manque -> NON MENTIONNE. Si pas de transcript ou notes partielles -> NON DOCUMENTE.

## Etape 2 — Enrichissement data (DataForSEO)

**Detection des domaines a analyser :**

1. Domaine(s) renseigne(s) dans le deal Pipedrive (champ custom ou website org)
2. Domaine(s) detecte(s) dans les fichiers sources (transcript, notes, CdC)
3. Si aucun domaine trouve -> demander au closer

**Un prospect peut avoir plusieurs domaines** (ex : site principal + marketplace + blog). Chaque domaine est enrichi separement.

**Pour chaque domaine :**
- Trafic organique actuel (domain_rank_overview)
- Top keywords + positions vs concurrents (ranked_keywords)
- Estimation valeur trafic organique (ETV en euros/mois)
- Concurrents Search principaux (competitors_domain)

Si aucun domaine detecte -> noter "ENRICHISSEMENT DATAFORSEO : AUCUN DOMAINE DETECTE" et continuer.

## Etape 3 — Scoring (grille 5 niveaux) + Fiabilite

**Grille de scoring :**

| Critere | Poids | 5 pts (max) | 4 pts | 3 pts | 2 pts | 1 pt (min) |
|---------|-------|-------------|-------|-------|-------|------------|
| Douleur (x6) | 30 max | Perte CA chiffree en euros + verbatim | Symptome chiffre (%, volume) | Douleur claire non chiffree | Douleur vague ("ameliorer") | Aucune douleur |
| Urgence (x5) | 25 max | Deadline < 6 sem, pression board | Deadline < 3 mois, trigger identifie | Objectif annuel, volonte d'agir | Timeline floue | Pas de timeline, exploration |
| Budget (x4) | 20 max | Enveloppe precise dediee SLASHR | Fourchette donnee, budget global | Indices forts (budget paid connu) | Indices faibles, evasif | Aucun signal, refus |
| Decideur (x3) | 15 max | C-level en call, signe seul | Budget owner, validation simple | Influenceur fort, decideur accessible | Influenceur, decideur "informe" | Operationnel seul |
| Fit (x2) | 10 max | Multi-marches, Search+IA, CA > 10M, gap concurrentiel > x3 | Search fort, 1 marche, CA > 5M, gap concurrentiel x2-3 | Besoin reel, scope limite, trafic organique existant | Besoin ponctuel, trafic < 500/mois | Site vitrine, aucun trafic organique |

**Enrichissement Fit par DataForSEO :** le trafic organique actuel et le gap concurrentiel (ratio concurrent/prospect) alimentent le scoring Fit. Un prospect avec un fort potentiel Search (gap > x3) mais peu de trafic actuel = opportunite forte. Un prospect sans trafic ET sans gap = faible potentiel.

**Score = somme(points x poids). Max = 100.**

**Seuils :**
- >= 60 -> `R2_GO`
- 40-59 -> `R2_CONDITIONAL` (validation manager obligatoire)
- < 40 -> `NURTURE` (pas de R2)

**Regle prudence :** critere `NON DOCUMENTE` -> scorer au median (3/5). Le minimum (1/5) est reserve aux signaux negatifs confirmes.

**Indice de fiabilite :**

| Fiabilite | Critere |
|-----------|---------|
| HAUTE | Transcript complet OU notes detaillees couvrant 4-5/5 questions. Peu de NON DOCUMENTE |
| MOYENNE | Notes partielles ou docs prospect. 2-3/5 questions couvertes. Quelques NON DOCUMENTE |
| BASSE | Email seul ou notes tres sommaires. < 2/5 questions couvertes. Plusieurs NON DOCUMENTE critiques |

**Override 1 — Fiabilite x score :**

| Fiabilite | Score >= 60 | Score 40-59 | Score < 40 |
|-----------|-------------|-------------|------------|
| HAUTE | Inchange | Inchange | Inchange |
| MOYENNE | Inchange | Inchange | Inchange |
| BASSE | R2_GO -> R2_CONDITIONAL + action "completer qualification" | Action ajoutee : "completer qualification avant validation" | Inchange |

**Override 2 — Micro-engagement x score :**

Le micro-engagement (OUI / PARTIEL / NON) est un deuxieme filtre applique APRES l'override fiabilite.

| Micro-engagement | Score >= 60 | Score 40-59 | Score < 40 |
|------------------|-------------|-------------|------------|
| OUI (3/3) | R2 GO | R2 CONDITIONAL — validation manager | NURTURE |
| PARTIEL (1-2/3) | R2 GO mais action pre-R2 obligatoire sous 48h. Si non obtenu -> R2 suspendue | R2 bloquee. Deadline 72h. Au-dela -> NURTURE | NURTURE |
| NON (0/3) | R2 non programmee. NURTURE | NURTURE | NURTURE |

**Un micro-engagement PARTIEL n'est jamais un feu vert definitif — c'est un feu orange avec action corrective.**

Ordre d'application : Score brut -> Override fiabilite -> Override micro-engagement -> Verdict final.

## Etape 4 — Analyse strategique

**Red flags** (max 4) et **green flags** (max 4) :
- Si fiabilite < HAUTE -> red flag obligatoire : "Qualification incomplete — {N} questions non couvertes"
- Chaque flag = 1 bullet, max 15 mots, factuel (pas "prospect hesitant" -> "pas de timeline mentionnee, exploration declaree")

**Angle R2** — construis-le en 3 couches :
1. **Douleur** : le probleme business exprime par le prospect (Section 2)
2. **Data** : ce que les donnees Search revelent (Etape 2 — trafic, gap concurrentiel, positions)
3. **Synthese** : la phrase qui connecte les deux = l'angle d'attaque

Formule : "{prospect} perd {impact} parce que {cause data}. SLASHR corrige ca en {approche}."

**Point de tension** — le moment ou le prospect doit choisir :
- Identifier le declencheur : deadline, budget qui expire, concurrent qui avance, saisonnalite
- Formuler en 1 phrase : "Si {prospect} n'agit pas avant {deadline}, {consequence concrete}"

**Question killer R2** — la question que le closer DOIT poser en R2 pour debloquer :
- Derivee du point de tension + de l'objection la plus probable
- Format : question ouverte, orientee decision, pas oui/non

**Actions pre-R2** (max 3) :
- Ce que le closer doit faire/verifier avant d'entrer en R2

## Etape 5 — Resume data Search

Rediger un resume de 3 a 5 lignes en prose, en metriques business :
- Trafic organique estime (visites/mois)
- Nombre de mots-cles positionnes
- Positions cles (top requetes, separation marque/hors-marque si pertinent)
- Constat principal (force, faiblesse, opportunite)

**Regles du resume Search :**
- Pas de tableau. Pas d'ETV isolee. Prose concise.
- Si l'ETV est mentionnee, toujours avec l'explication : "ce qui equivaut a X EUR/mois en achat Google Ads"
- L'objectif = donner au closer une vision business en 30 secondes de lecture

## Etape 6 — Verdict de routage

- Si verdict = **NURTURE** -> produire le brief score + recommandation DISQUALIFIER. STOP.
- Si verdict = **R2_GO** ou **R2_CONDITIONAL** -> produire le brief complet. Rappeler : "Pour preparer la R2 : `/deck {deal_id}`".

---

## Format de sortie — DEAL-*.md (qualification)

Tu DOIS produire le dossier dans ce format exact. **Cible : < 150 lignes.**

**Budget indicatif par section :**

| Section | Lignes |
|---------|--------|
| S1 — Identite | ~10 |
| S2 — Probleme reel | ~15 |
| S3 — Qualification | ~12 |
| S4 — Score + fiabilite | ~18 |
| S5 — Signaux | ~12 |
| S6 — Recommandation | ~10 |
| S7 — Resume Search | ~5 |
| Metadata | ~15 |
| Separateurs + titres | ~10 |
| **Total** | **~107** |

Marge de ~40 lignes pour les deals complexes (multi-domaines, verbatims longs). Ne pas depasser 150.

### Section 1 — Identite prospect

| Champ | Valeur |
|-------|--------|
| Entreprise | {nom} |
| Interlocuteur | {prenom nom} |
| Titre / Role | {role exact} |
| Secteur | {1 mot} |
| Taille | {employes + CA si connu. Sinon "NON MENTIONNE" ou "NON DOCUMENTE"} |
| Domaine(s) | {domaine principal + domaines secondaires si plusieurs} |
| Source du lead | {canal d'origine} |
| Deal Pipedrive | #{deal_id} — {stage actuel} |

### Section 2 — Probleme reel

| Champ | Valeur |
|-------|--------|
| Douleur business | {verbatim exact entre guillemets. Si aucune -> "AUCUNE DOULEUR EXPRIMEE". Si non couvert -> "NON DOCUMENTE"} |
| Impact chiffre | {euros/%, sinon "NON CHIFFRE", sinon "NON DOCUMENTE"} |
| Situation actuelle | {description} |
| Risque d'inaction | {1 phrase business} |

### Section 3 — Qualification

Pour chaque indicateur : valeur + justification en 1 ligne.

- **Urgence** : CRITIQUE / MOYENNE / FAIBLE
- **Budget** : CONFIRME {montant} / IMPLICITE {estimation} / INCONNU
- **Decideur** : DECIDEUR / INFLUENCEUR / OPERATIONNEL
- **Micro-engagement** : OUI / PARTIEL / NON
- **Fit strategique** : FORT / MOYEN / FAIBLE

### Section 4 — Score closing + Fiabilite

```json
{
  "score_total": 0,
  "fiabilite": "HAUTE | MOYENNE | BASSE",
  "breakdown": {
    "douleur_business": { "points": 0, "max": 30 },
    "urgence": { "points": 0, "max": 25 },
    "budget": { "points": 0, "max": 20 },
    "decideur": { "points": 0, "max": 15 },
    "fit_strategique": { "points": 0, "max": 10 }
  },
  "verdict": "R2_GO | R2_CONDITIONAL | NURTURE"
}
```

Justification scoring : 1 ligne par critere.

### Section 5 — Signaux

- **Red flags** (max 4) : bullets, max 15 mots chacun
- **Green flags** (max 4) : bullets, max 15 mots chacun
- **Verbatims a reutiliser en R2** (max 3) : citations exactes entre guillemets. Si pas de transcript -> "PAS DE TRANSCRIPT — VERBATIMS NON DISPONIBLES"

### Section 6 — Recommandation

**Verdict** : `CONTINUER` ou `DISQUALIFIER`

Si CONTINUER :
- Angle R2 (1 phrase)
- Point de tension (1 phrase)
- Question killer R2 (1 question ouverte — la question que le closer DOIT poser pour debloquer)
- Risque R2 (1 phrase)
- Actions pre-R2 (max 3)

Si DISQUALIFIER :
- Raison (1 phrase)
- Condition de reactivation (1 phrase — qu'est-ce qui changerait le verdict ?)
- Potentiel Search (1 phrase — si les donnees DataForSEO montrent un vrai potentiel malgre le timing)
- Route de sortie : nurture / revisit Q+1 / dead

### Section 7 — Resume data Search

{3-5 lignes de prose — voir Etape 5}

---

### METADATA (toujours en fin de document)

```json
{
  "deal_id": "DEAL-{YYYYMMDD}-{entreprise-slug}",
  "pipedrive_deal_id": 0,
  "date_r1": "YYYY-MM-DD",
  "date_brief": "YYYY-MM-DD",
  "auteur": "Deal Analyst Agent",
  "version": "8.0",
  "status": "DRAFT",
  "sources_dossier_r1": [
    {
      "type": "transcript | notes_closer | document_prospect | email_prospect",
      "description": "Description courte",
      "qualite": "complete | partielle | sommaire",
      "origine": "google_drive | pipedrive_notes"
    }
  ],
  "domaines_analyses": ["example.com"],
  "questions_couvertes": [],
  "nb_non_documente": 0
}
```

---

## Validation

Un brief est **REJECTED** automatiquement si :
1. Un champ obligatoire est vide (exception : "NON MENTIONNE" et "NON DOCUMENTE" sont valides)
2. Le score n'est pas calcule ou incoherent avec les indicateurs Section 3
3. Le verdict Section 6 contredit le score Section 4 (apres application de la regle fiabilite x score)
4. Aucun verbatim extrait ET aucune mention "AUCUN VERBATIM EXPLOITABLE" ou "PAS DE TRANSCRIPT"
5. Le brief depasse 150 lignes
6. La recommandation est floue ("peut-etre", "a voir", "interessant")
7. L'indice de fiabilite n'est pas renseigne ou incoherent avec les sources
8. Les `sources_dossier_r1` ne sont pas renseignees en metadata

**Un brief REJECTED ne declenche aucune action downstream.**

### Workflow CHALLENGED

Le closer peut contester un brief s'il detecte une incoherence :
- Score incoherent avec les indicateurs
- Verbatim manquant ou mal extrait
- Risque sous-evalue ou red flag absent
- Angle R2 non exploitable

**Action :** corriger le brief et re-valider. Pas de DECK tant que le brief est conteste.
