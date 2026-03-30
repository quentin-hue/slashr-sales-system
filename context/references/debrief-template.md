# Debrief Template — Feedback structure

> Ce template structure le feedback post-deal pour permettre l'amelioration automatique du systeme.

## Champs obligatoires

| Champ | Type | Description |
|-------|------|-------------|
| `DEAL_ID` | int | ID Pipedrive |
| `OUTCOME` | enum | WON / LOST / PENDING |
| `CLOSER_CORRECTIONS` | int | Nombre de corrections demandees par le closer sur la proposition |
| `REVIEW_TIME_MIN` | int | Temps de review closer en minutes (estime) |
| `QUALITY_SCORE` | 1-5 | Auto-evaluation de la qualite de la proposition generee |

## Issues identifiees (liste)

Pour chaque correction closer, documenter :

| Champ | Type | Description |
|-------|------|-------------|
| `ISSUE_TYPE` | enum | DATA_INCOHERENCE / DESIGN_DENSITY / NARRATIVE_ANGLE / PRICING_ERROR / MISSING_SECTION / TONE / OTHER |
| `AFFECTED_TAB` | enum | diagnostic / strategie / projet / investissement / cas_clients |
| `AFFECTED_RULE` | string | ID de la regle (ex: "R14", "h2_length", "brand_pragmatism") |
| `SEVERITY` | enum | CRITICAL (bloque le closing) / HIGH (reduit la credibilite) / MEDIUM (amelioration) / LOW (cosmetique) |
| `DESCRIPTION` | string | Description du probleme |
| `FIX_APPLIED` | string | Correction appliquee |
| `SYSTEM_FIX` | string | Modification systeme a faire pour eviter la recurrence (ou "NONE") |

## Patterns a tracker

| Pattern | Metrique | Seuil d'alerte |
|---------|----------|---------------|
| Incohérence chiffres SDB/HTML | nb corrections DATA_INCOHERENCE par deal | > 2 |
| Slides trop denses | nb corrections DESIGN_DENSITY par deal | > 3 |
| ROI sur-estime | correction a la baisse du ROI projete | > 20% |
| Pricing incorrect | ecart pricing NBP vs HTML | > 0 |
| Corrections closer totales | nb total par deal | > 10 = systeme defaillant |

## Score qualite par deal

```
score = 5 - (critical * 2) - (high * 1) - (medium * 0.3)
score = max(1, min(5, score))
```

Un score < 3 sur 3 deals consecutifs declenche une review systeme.
