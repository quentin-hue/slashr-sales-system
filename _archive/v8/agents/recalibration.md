# Mode RECALIBRATION — Analyse retrospective (v8.0)

> **Prerequis :** `agents/shared.md` lu.

---

## Objectif

Agreger les deals clotures sur une periode pour recalibrer le scoring et les process. Identifier les patterns de succes et d'echec. Produire des actions correctives concretes.

Reference format closure : `contracts/deal_closure.schema.md`

---

## Input

### Parametre : periode
- Defaut : dernier trimestre (90 jours)
- Formats acceptes : "Q1 2026", "last 90 days", "janvier a mars 2026"

### Donnees collectees

1. **Lister les deals Pipedrive** avec stage Won (Pending Signature, id=8) ou Lost sur la periode
   - API : `GET /v1/deals?pipeline_id=1&status=won` + `GET /v1/deals?pipeline_id=1&status=lost`
   - Filtrer par date de cloture dans la periode
2. **Pour chaque deal** : extraire r1_score, r1_verdict, r1_fiabilite, decideur_level, relance_status
3. **Si DEAL-*.md existe dans Drive** -> le lire pour enrichir l'analyse

### Garde-fou

**Si < 5 deals sur la periode -> "Echantillon insuffisant ({N} deals). Recalibration reportee. Minimum requis : 5 deals clotures."**

---

## Processus — 5 etapes

### Etape 1 — Inventaire deals

Tableau recapitulatif :

| # | Deal | Entreprise | Score R1 | Verdict | Resultat | Duree cycle (jours) |
|---|------|-----------|----------|---------|----------|-------------------|
| 1 | #{id} | {nom} | {score} | {verdict} | Won / Lost | {jours R1 -> cloture} |

### Etape 2 — Analyse scoring

- **Delta moyen** : ecart entre score initial et realite (deals Won avec score bas ? deals Lost avec score haut ?)
- **Critere le plus mal evalue** : quel critere de la grille surprend le plus souvent ? (ex : budget surestime, decideur mal identifie)
- **Calibrage seuil 60** : % deals Won avec score < 60 (faux negatifs) + % deals Lost avec score > 60 (faux positifs)
- **Verdict calibrage** : "Seuil 60 confirme" si faux positifs + faux negatifs < 20%. Sinon : "Seuil a ajuster a {X} — justification : {raison}"
- **Ventilation par decideur_level** : taux Won/Lost par DECIDEUR / INFLUENCEUR / OPERATIONNEL. Si un profil a un taux de perte > 70% -> signal d'alerte
- **Fiabilite vs resultat** : les deals BASSE fiabilite finissent-ils plus souvent Lost ?

### Etape 3 — Analyse conversion

- **Taux R1 -> R2** : % deals passant de R1 Done a R2 Scheduled
- **Taux R2 -> Won** : % deals signes apres R2
- **Taux par touch de relance** : si relances existent, quel touch convertit le plus ?
- **Duree moyenne de cycle** : R1 -> cloture (Won) vs R1 -> cloture (Lost)

### Etape 4 — Patterns de perte

- **Top 3 motifs de perte** (par frequence) : budget, timing, concurrent, pas de besoin, ghosting
- **Objections non anticipees** : objections recurrentes qui n'etaient pas dans les DECKs
- **Stage de decrochage** : a quel stage les deals tombent-ils le plus ?

### Etape 5 — Recommandations

Max 5 actions correctives concretes, **ordonnees par impact decroissant**.

Pour chacune :
- **Constat** : ce que les donnees montrent
- **Action** : ce qu'on change dans le process
- **Impact attendu** : HAUT / MOYEN / BAS

**Focus action #1 :** la premiere action de la liste est celle a implementer immediatement. La presenter en gras dans le format de sortie. C'est la seule chose que le closer doit changer cette semaine.

---

## Format de sortie — RECALIBRATION-*.md

```markdown
# Recalibration — {periode}

## Inventaire ({N} deals : {W} Won, {L} Lost)
{tableau Etape 1}

## Scoring : calibrage actuel
{analyse Etape 2}

## Conversion : taux pipeline
{analyse Etape 3}

## Patterns de perte
{analyse Etape 4}

## Actions correctives
{recommandations Etape 5}

---

### METADATA
{
  "recalibration_id": "RECALIBRATION-{YYYYMMDD}",
  "periode": "{debut} — {fin}",
  "nb_deals": 0,
  "nb_won": 0,
  "nb_lost": 0,
  "date_recalibration": "YYYY-MM-DD",
  "auteur": "Deal Analyst Agent",
  "version": "8.0",
  "status": "DRAFT"
}
```

---

## Limites connues

- La recalibration depend de la qualite des donnees Pipedrive (scores renseignes, stages a jour)
- Les deal_closure detailles (`contracts/deal_closure.schema.md`) sont aujourd'hui manuels — si absents, l'analyse se base uniquement sur Pipedrive
- Les motifs de perte non documentes sont marques "Motif non renseigne"
