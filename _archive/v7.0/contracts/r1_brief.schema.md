# R1 Brief Schema — v1.2

## Contrat

Ce document est un **contrat de format**. Tout brief R1 qui ne respecte pas ce schema est rejeté. Pas d'exception, pas de "je complèterai plus tard". Un brief incomplet = un brief qui n'existe pas.

## Input — Dossier R1

L'input n'est pas un transcript unique — c'est un **dossier R1** composé d'un ou plusieurs éléments :

| Type de source | Description | Exemple |
|----------------|-------------|---------|
| **Transcript complet** | Call enregistré + transcription automatique | Fireflies, Otter, Google Meet transcript |
| **Notes closer** | Notes prises à la volée pendant ou après le call | Google Doc, note Pipedrive, message Slack |
| **Documents prospect** | Cahier des charges, brief, cadrage, RFP envoyé par le prospect | PDF, Google Doc, email avec pièce jointe |
| **Email prospect** | Le prospect décrit son besoin par écrit, sans call | Email brut ou thread |

**Règles :**
- Le dossier peut contenir **un seul ou plusieurs** de ces éléments
- L'agent doit travailler avec **ce qu'il a** — pas exiger un format idéal
- Chaque source est identifiée dans les metadata (Section 7)
- La qualité des sources détermine l'**indice de fiabilité** du brief (Section 4)

## Output

Brief stratégique structuré. 8 sections fixes, ordre imposé, limites strictes.

---

## Section 1 — Identité prospect

**Format : tableau. Tous les champs obligatoires.**

| Champ | Type | Règle |
|-------|------|-------|
| Entreprise | string | Nom légal ou commercial |
| Interlocuteur | string | Prénom + Nom |
| Titre / Rôle | string | Intitulé exact donné par le prospect |
| Secteur | string | Un mot : SaaS, E-commerce, B2B Services, etc. |
| Taille | string | Fourchette employés + CA si mentionné. Sinon : "NON MENTIONNÉ" |
| URL | url | Domaine principal. Obligatoire — sans URL, pas d'enrichissement DataForSEO |
| Source du lead | string | Canal d'origine : inbound (site, LinkedIn, referral) ou outbound (cold email, event, intro). Obligatoire — alimente le recalibrage trimestriel |

---

## Marqueurs de données manquantes

Deux marqueurs distincts. Ne pas les confondre.

| Marqueur | Signification | Impact scoring |
|----------|---------------|----------------|
| **"NON MENTIONNÉ"** | Le sujet a été abordé mais le prospect n'a pas répondu, ou l'info n'a pas été évoquée lors d'un échange documenté | Signal faible — l'absence d'info est un signal en soi |
| **"NON DOCUMENTÉ"** | L'info a **peut-être** été abordée mais n'apparaît pas dans les sources du dossier R1. Trou documentaire, pas trou de qualification | Pas de signal — le scoring doit être prudent (voir indice de fiabilité) |

**Règle :** "NON DOCUMENTÉ" n'est utilisable que si le dossier R1 est incomplet (notes partielles, pas de transcript). Si un transcript complet est disponible et qu'une info manque → c'est "NON MENTIONNÉ", pas "NON DOCUMENTÉ".

---

## Section 2 — Problème réel

**Format : 4 champs obligatoires. Pas de paraphrase — verbatim ou rien.**

| Champ | Règle |
|-------|-------|
| **Douleur business** | Le problème #1, formulé avec les mots exacts du prospect. Entre guillemets. Si le prospect n'a pas exprimé de douleur claire → écrire "AUCUNE DOULEUR EXPRIMÉE" (= red flag majeur). Si les sources ne couvrent pas ce sujet → "NON DOCUMENTÉ" |
| **Impact chiffré** | En euros, en %, ou en volume. Ce que la douleur coûte concrètement. Si non mentionné → "NON CHIFFRÉ" (= signal faible scoring). Si les sources ne couvrent pas ce sujet → "NON DOCUMENTÉ" |
| **Situation actuelle** | Ce qui est en place aujourd'hui : agence existante, équipe interne, rien, tentative passée échouée. Si non documenté → "NON DOCUMENTÉ" |
| **Risque d'inaction** | Ce qui se passe si le prospect ne fait rien dans les 6 mois. Extrait du dossier R1 ou déduit. Formulé en 1 phrase business. Ex : "Perte estimée de 15% de part de marché organique au profit de {concurrent}" |

---

## Section 3 — Qualification

**Format : 5 indicateurs. Valeurs imposées. Pas de texte libre.**

### Urgence

| Valeur | Critère |
|--------|---------|
| **CRITIQUE** | Deadline < 3 mois, événement déclencheur imminent, pression board/investisseur |
| **MOYENNE** | Objectif annuel, volonté d'agir mais pas de contrainte temporelle dure |
| **FAIBLE** | Pas de timeline, exploration, "on regarde ce qui se fait" |

### Budget implicite estimé

| Valeur | Critère |
|--------|---------|
| **CONFIRMÉ** | Enveloppe annoncée ou fourchette donnée. Montant : {X}€ |
| **IMPLICITE** | Pas de montant, mais indices (taille entreprise, budget paid actuel, mentions "on investit"). Estimation : {X}€ |
| **INCONNU** | Aucun signal budget. Réponse évasive ou "ça dépend de la presta" |

### Niveau décisionnaire

| Valeur | Critère |
|--------|---------|
| **DÉCIDEUR** | C-level, founder, VP, budget owner — peut signer seul |
| **INFLUENCEUR** | Head of, Manager — recommande mais ne signe pas. Qui signe : {nom/rôle} |
| **OPÉRATIONNEL** | Exécutant envoyé en éclaireur. Décideur non identifié |

### Micro-engagement obtenu

| Valeur | Critère |
|--------|---------|
| **OUI** | Date R2 fixée + décideur confirmé + accord verbal d'avancer si reco pertinente |
| **PARTIEL** | Date R2 fixée mais décideur incertain OU accord verbal flou |
| **NON** | Aucun engagement concret obtenu en fin de R1 |

**Règle PARTIEL :** un micro-engagement PARTIEL avec score >= 60 déclenche une action pré-R2 obligatoire (call dédié SLASHR sous 48h pour convertir PARTIEL → OUI). Si non converti → R2 suspendue. Voir `sales_process.md` pour la matrice complète.

### Fit stratégique SLASHR

| Valeur | Critère |
|--------|---------|
| **FORT** | Multi-marchés, enjeu Search+IA structurant, CA > 5M€, ambition acquisition organique |
| **MOYEN** | Marché unique, besoin Search réel mais scope limité |
| **FAIBLE** | Site vitrine, besoin ponctuel, pas d'enjeu stratégique identifiable |

---

## Section 4 — Score closing + Fiabilité

**Format : JSON strict. Pas de texte autour.**

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

### Indice de fiabilité du brief

L'indice mesure la confiance qu'on peut accorder au score, **en fonction de la qualité des sources du dossier R1**.

| Fiabilité | Critère |
|-----------|---------|
| **HAUTE** | Transcript complet OU notes détaillées couvrant au moins 4/5 questions non négociables. Peu ou pas de "NON DOCUMENTÉ" dans le brief |
| **MOYENNE** | Notes partielles ou documents prospect sans call. 2-3 questions non négociables couvertes. Quelques "NON DOCUMENTÉ" |
| **BASSE** | Email seul ou notes très sommaires. < 2 questions non négociables couvertes. Plusieurs "NON DOCUMENTÉ" sur des champs critiques (douleur, budget, décideur) |

### Règle fiabilité × score (override de verdict)

| Fiabilité | Score >= 60 | Score 40-59 | Score < 40 |
|-----------|-------------|-------------|------------|
| **HAUTE** | Verdict inchangé | Verdict inchangé | Verdict inchangé |
| **MOYENNE** | Verdict inchangé | Verdict inchangé | Verdict inchangé |
| **BASSE** | ⚠️ Override : `R2_GO` → `R2_CONDITIONAL`. Action pré-R2 obligatoire : "Compléter la qualification — call de 15 min pour couvrir les questions manquantes" | ⚠️ Override : `R2_CONDITIONAL` → action pré-R2 ajoutée : "Compléter la qualification avant validation manager" | Verdict inchangé |

**Principe : on ne bloque pas un deal prometteur à cause de notes incomplètes, mais on ne fonce pas en R2 à l'aveugle non plus.**

**Grille de calcul — 5 niveaux :**

| Critère | 5 pts (× poids) | 4 pts | 3 pts | 2 pts | 1 pt (× poids) |
|---------|-----------------|-------|-------|-------|-----------------|
| Douleur (×6) | Perte de CA chiffrée en € + verbatim clair | Symptôme chiffré (%, volume) sans traduction en € | Douleur exprimée clairement mais non chiffrée | Douleur vague ("on veut améliorer") | Aucune douleur exprimée |
| Urgence (×5) | Deadline < 6 semaines, pression board active | Deadline < 3 mois, événement déclencheur identifié | Objectif annuel avec volonté d'agir | Timeline floue, "dans les mois à venir" | Pas de timeline, exploration pure |
| Budget (×4) | Enveloppe précise annoncée, dédiée au scope SLASHR | Fourchette donnée, mais budget global (scope partagé) | Pas de montant, indices forts (budget paid connu, taille entreprise) | Indices faibles, réponse évasive | Aucun signal budget, refus de répondre |
| Décideur (×3) | C-level / founder en call, peut signer seul | Budget owner en call, process de validation simple | Influenceur fort (Head of), décideur identifié et accessible | Influenceur, décideur "informé" mais non mappé | Opérationnel seul, décideur non identifié |
| Fit (×2) | Multi-marchés, enjeu Search+IA structurant, CA > 10M€ | Enjeu Search fort, 1 marché, CA > 5M€ | Besoin Search réel, scope limité mais potentiel d'extension | Besoin ponctuel, peu de potentiel long terme | Site vitrine, pas d'enjeu stratégique |

**Calcul : score = somme(points × poids). Max = (5×6)+(5×5)+(5×4)+(5×3)+(5×2) = 100.**

**Seuils :**
- **>= 60** → `R2_GO`
- **40-59** → `R2_CONDITIONAL` (validation manager obligatoire)
- **< 40** → `NURTURE` (brief archivé, pas de R2)

---

## Section 5 — Signaux

**Format : bullets. Max 4 par catégorie. Pas de phrase > 15 mots.**

### Red flags (max 4)
- _bullet_

### Green flags (max 4)
- _bullet_

### Verbatims à réutiliser en R2 (max 3)
- "{citation exacte du prospect}"

**Règles verbatims :**
- Les verbatims sont des citations exactes entre guillemets. Pas de paraphrase.
- Si aucun verbatim exploitable → écrire "AUCUN VERBATIM EXPLOITABLE" (= le R1 a manqué de profondeur)
- Si le dossier R1 ne contient pas de transcript (notes seules, email) → écrire "PAS DE TRANSCRIPT — VERBATIMS NON DISPONIBLES". Ce n'est pas un red flag si la fiabilité est documentée en Section 4.

---

## Section 6 — Recommandation

**Format : 1 valeur + 4 champs. Pas de paragraphe.**

### Verdict

`CONTINUER` ou `DISQUALIFIER`

- **CONTINUER** = score >= 40, au moins un micro-engagement, douleur identifiée
- **DISQUALIFIER** = score < 40 OU aucune douleur OU aucun micro-engagement OU fit FAIBLE

### Si CONTINUER

| Champ | Règle |
|-------|-------|
| **Angle R2** | La proposition de valeur #1 à poser en R2. 1 phrase. |
| **Point de tension** | Le levier business/émotionnel à activer. 1 phrase. |
| **Risque R2** | Ce qui peut faire capoter. 1 phrase. |
| **Action pré-R2** | Ce qu'il faut préparer avant R2 (data DataForSEO, benchmark, POC). 1 phrase. |

### Si DISQUALIFIER

| Champ | Règle |
|-------|-------|
| **Raison** | Motif principal de disqualification. 1 phrase. |
| **Route de sortie** | Nurture, revisit Q+1, ou dead. |

---

## Section 7 — Metadata

```json
{
  "brief_id": "R1-{YYYY}{MM}{DD}-{entreprise}",
  "date_r1": "YYYY-MM-DD",
  "date_brief": "YYYY-MM-DD",
  "auteur": "Sales Analyst Agent",
  "version": "1.2",
  "word_count": 0,
  "status": "DRAFT | VALIDATED | CHALLENGED | REJECTED",
  "sources_dossier_r1": [
    {
      "type": "transcript | notes_closer | document_prospect | email_prospect",
      "description": "Description courte de la source",
      "qualite": "complète | partielle | sommaire"
    }
  ],
  "questions_couvertes": ["Q1_douleur", "Q2_inaction", "Q3_decideur", "Q4_budget", "Q5_engagement"],
  "nb_non_documente": 0
}
```

**Règles metadata sources :**
- Chaque source du dossier R1 est listée avec son type et sa qualité
- `questions_couvertes` : liste des 5 questions non négociables dont la réponse apparaît dans les sources. Sert au calcul de fiabilité
- `nb_non_documente` : nombre de champs marqués "NON DOCUMENTÉ" dans le brief. Sert de signal pour le Closing Coach

### Statut CHALLENGED

Le Closing Coach peut renvoyer un brief en statut `CHALLENGED` s'il détecte une incohérence lors de la génération du pack R2.

**Motifs de challenge valides :**
- Score incohérent avec les indicateurs (ex : budget CONFIRMÉ à 20/20 alors que le budget est partagé)
- Verbatim manquant ou mal extrait
- Risque sous-évalué ou red flag absent
- Angle R2 non exploitable en l'état

**Format du challenge :**

```json
{
  "challenger": "Closing Coach Agent",
  "date_challenge": "YYYY-MM-DD",
  "champs_contestés": ["budget", "scoring"],
  "motif": "1 phrase par champ contesté",
  "action_demandée": "recalculer | compléter | corriger"
}
```

**Workflow :** Brief CHALLENGED → retour au Sales Analyst → correction → revalidation → le brief passe en VALIDATED ou REJECTED. Le Closing Coach ne génère aucun pack R2 tant que le brief est en CHALLENGED.

---

## Règles de validation

Un brief est **REJECTED** automatiquement si :

1. Un champ obligatoire est vide (pas de "à compléter", pas de "N/A"). Exception : "NON MENTIONNÉ" et "NON DOCUMENTÉ" sont des valeurs valides selon les règles de marquage
2. Le score n'est pas calculé ou incohérent avec les indicateurs Section 3
3. Le verdict Section 6 contredit le score Section 4 (après application de la règle fiabilité × score)
4. Aucun verbatim extrait ET aucune mention "AUCUN VERBATIM EXPLOITABLE" ou "PAS DE TRANSCRIPT — VERBATIMS NON DISPONIBLES"
5. Le brief dépasse 500 mots (hors JSON et tableaux)
6. La recommandation est floue ("peut-être", "à voir", "intéressant")
7. L'indice de fiabilité n'est pas renseigné ou incohérent avec les sources listées en Section 7
8. Les `sources_dossier_r1` ne sont pas renseignées en metadata

**Un brief REJECTED ne déclenche aucune action downstream. Il est renvoyé à l'agent pour correction.**
