# Deal Closure Schema — v1.1

## Contrat

Ce document est obligatoire à la clôture de chaque deal (Won ou Lost). Pas de deal archivé sans closure. Le debrief alimente le recalibrage trimestriel du scoring et des process.

## Déclencheur

- Deal passé en "Won" dans Pipedrive
- Deal passé en "Lost — Declined", "Lost — Ghosting", ou "Lost — Disqualified"
- À remplir dans les 48h suivant la clôture

## Output

Debrief structuré. 5 sections fixes.

---

## Section 1 — Identité deal

| Champ | Type | Règle |
|-------|------|-------|
| brief_id | string | Référence du brief R1 associé (ex: R1-20260130-decathlon-fitness-club) |
| entreprise | string | Nom du prospect |
| closer | string | Nom du closer humain |
| date_r1 | date | Date du call R1 |
| date_r2 | date | Date du call R2. "N/A" si R2 non réalisée |
| date_closure | date | Date de clôture du deal |
| durée_cycle | number | Nombre de jours entre R1 et clôture |

---

## Section 2 — Résultat

| Champ | Règle |
|-------|-------|
| **Statut** | `WON` / `LOST_DECLINED` / `LOST_GHOSTING` / `LOST_DISQUALIFIED` / `LOST_TIMING` |
| **Motif** | 1 phrase. Raison principale du résultat. Ex : "Budget validé, fit stratégique confirmé en R2" ou "Prospect a choisi une agence low-cost après R2" |
| **Valeur deal** | Montant signé (si Won) ou montant estimé perdu (si Lost). En euros |

---

## Section 3 — Analyse prédictive

**Objectif : mesurer si le système a correctement anticipé le résultat.**

| Champ | Règle |
|-------|-------|
| **Score R1 initial** | Score /100 tel que calculé dans le brief |
| **Verdict initial** | R2_GO / R2_CONDITIONAL / NURTURE |
| **Score R1 recalculé** | Avec le recul post-R2, quel score aurait dû être attribué ? /100 |
| **Delta scoring** | Écart entre score initial et recalculé. Si > 15 points → le scoring a dysfonctionné |
| **Critère le plus mal évalué** | Lequel des 5 critères était le plus éloigné de la réalité ? 1 mot : douleur / urgence / budget / decideur / fit |

---

## Section 4 — Analyse tactique

### Objections

| Champ | Règle |
|-------|-------|
| **Objections anticipées (pack R2)** | Lister les objections prévues par le Closing Coach |
| **Objections réelles (R2)** | Lister les objections effectivement apparues |
| **Objections surprises** | Celles qui n'étaient pas dans le pack. Max 3 |
| **Taux de prédiction** | % d'objections réelles qui étaient anticipées |

### Relances (si applicable)

| Champ | Règle |
|-------|-------|
| **Touches envoyées** | 0, 1, 2, ou 3 |
| **Ouvertures** | Nombre d'emails ouverts |
| **Réponses** | Nombre de réponses reçues |
| **Touch qui a converti** | Numéro de la touch qui a déclenché une réponse. "AUCUNE" si ghosting total |

---

## Section 5 — Apprentissages

| Champ | Règle |
|-------|-------|
| **Ce qui a fonctionné** | Max 3 bullets. Ce qui a contribué au résultat (positif ou négatif) |
| **Ce qu'on ferait différemment** | Max 3 bullets. Changement de tactique, de timing, de scoring |
| **Recommandation process** | Si cette closure révèle un pattern, recommandation pour améliorer le système. 1 phrase. "AUCUNE" si RAS |

---

## Metadata

```json
{
  "closure_id": "CL-{YYYY}{MM}{DD}-{entreprise}",
  "date_closure": "YYYY-MM-DD",
  "auteur": "Closer humain + Closing Coach Agent",
  "version": "1.1",
  "status": "DRAFT | VALIDATED"
}
```

---

## Routine de recalibrage trimestrielle

Tous les trimestres, agréger les closures pour :

1. **Recalibrer le scoring** — si le delta moyen > 10 pts, la grille doit être ajustée
2. **Ajuster les seuils** — le seuil 60 est-il le bon ? Comparer taux de conversion par tranche
3. **Enrichir les objections** — ajouter les objections surprises récurrentes au pack par défaut
4. **Mesurer le taux de conversion** — R1→R2, R2→Won, et par touch de relance
5. **Identifier les patterns de perte** — motifs récurrents → action corrective

**Livrable trimestriel : 1 page de recalibrage avec décisions prises. Stocké dans `outputs/recalibrage/`.**
