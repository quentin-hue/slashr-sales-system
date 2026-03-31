---
name: debrief
description: Collecte le resultat d'un deal (won/lost), auto-analyse SDB vs resultat, pattern matching, injection dans futurs /prepare.
disable-model-invocation: true
---

# DEBRIEF — Boucle de retroaction enrichie (v12.0)

**Deal ID :** $ARGUMENTS

## Prerequis

1. Lis `agents/shared.md` (preambule partage, regles)

## Usage

```
/debrief <deal_id>
/debrief 560
```

## Etapes

### 1. Collecter les informations du deal

```bash
TOKEN=$(cat ~/.pipedrive_token)
curl -s "https://api.pipedrive.com/v1/deals/{deal_id}?api_token=$TOKEN"
```

Extraire :
- **Status** : `won`, `lost`, ou `open`
- **Montant** : `value`
- **Lost reason** : `lost_reason` (si lost)
- **r2_pack_link** (field `4b84e7bfe1a6b330318fc7a0d208e2faedf2530a`) : lien vers la proposition
- **domaine_principal** : domaine analyse (si renseigne)

### 2. Collecter les artefacts existants

Verifier la presence de :
- `.cache/deals/{deal_id}/artifacts/PROPOSAL-*.html`
- `.cache/deals/{deal_id}/artifacts/INTERNAL-DIAG-*.md`
- `.cache/deals/{deal_id}/artifacts/NBP.md`
- `.cache/deals/{deal_id}/artifacts/SDB.md`
- `.cache/deals/{deal_id}/audit.md` (si /audit a ete execute)
- `.cache/deals/{deal_id}/benchmark.md` (si /benchmark a ete execute)

### 3. Demander le feedback closer

Poser ces questions au closer (via le terminal) :

1. **Resultat** : Won / Lost / En cours (confirmer avec Pipedrive)
2. **Facteur decisif** : "Quel a ete le facteur decisif pour le prospect ?" (1-2 phrases)
3. **Qualite proposition** : "La proposition etait-elle adaptee ? Qu'aurait-il fallu changer ?" (1-2 phrases)
4. **Arc narratif** : "L'angle strategique etait-il le bon ?" (1 phrase)
5. **Objections non anticipees** : "Y a-t-il eu des objections que la proposition n'avait pas pre-emptees ?" (liste)

### 4. Auto-analyse (NOUVEAU v12)

Comparer automatiquement les predictions du SDB avec le resultat reel :

| Prediction SDB | vs Resultat | Analyse |
|----------------|-------------|---------|
| Diagnostic contrainte | Feedback closer | Le diagnostic etait-il correct ? |
| Arc narratif NBP | Feedback closer | L'angle choisi etait-il adapte ? |
| ROI estime | Montant signe (won) ou feedback (lost) | Le ROI etait-il credible ? |
| Scenario recommande | Budget reel du prospect | Le pricing etait-il dans la bonne fourchette ? |
| Objections anticipees (FAQ) | Objections reelles | Quelles objections n'ont pas ete pre-emptees ? |

Produire un verdict auto :
```
AUTO-ANALYSE :
- Diagnostic contrainte : {CORRECT | PARTIEL | INCORRECT} — {explication}
- Arc narratif : {ADAPTE | A AJUSTER} — {explication}
- ROI : {CREDIBLE | SUR-ESTIME | SOUS-ESTIME} — {explication}
- Pricing : {DANS LA FOURCHETTE | TROP HAUT | TROP BAS} — {explication}
- Objections : {N} anticipees sur {M} reelles — {lacunes}
```

### 5. Pattern matching (NOUVEAU v12, des le 1er debrief)

Meme avec 1 seul debrief, identifier les patterns en comparant avec les connaissances systeme :

- **Patterns connus** : quels arcs fonctionnent pour quels profils decideur ?
- **Correlations** : ROI > x2 correle avec won ? Score audit > 70 correle avec won ?
- **Anti-patterns** : quelles objections reviennent ? Quels arcs sous-performent ?

Si >= 3 debriefs existent, produire des correlations statistiques.

### 5b. Ecrire le debrief structure (JSON)

En plus du fichier markdown, ecrire `.cache/deals/{deal_id}/debrief.json` :

```json
{
  "deal_id": {deal_id},
  "date": "{ISO date}",
  "result": "won|lost|open",
  "company": "{nom entreprise}",
  "sector": "{secteur}",
  "amount_proposed": {montant propose EUR},
  "amount_signed": {montant signe EUR, null si lost/open},
  "arc_used": "{arc du NBP}",
  "hook_type": "{type de hook}",
  "tone_profile": "{DIRECT|PEDAGOGIQUE|PROVOCATEUR|TECHNIQUE}",
  "scenario_proposed": "{Pilotage|Production|Acceleration}",
  "budget_proposed": {budget mensuel EUR},
  "budget_accepted": {budget mensuel accepte EUR, null si lost},
  "roi_estimated": {multiplicateur ROI estime},
  "audit_score": {score audit 0-100, null si pas d'audit},
  "confidence_global": "{High|Medium|Low}",
  "decideur_level": "{DECIDEUR|INFLUENCEUR|OPERATIONNEL}",
  "sea_signal": "{EXPLICIT|DETECTED|OPPORTUNITY|ABSENT}",
  "modules_used": ["liste des modules actives"],
  "gsc_available": true|false,
  "google_ads_available": true|false,
  "closer_feedback": {
    "decisive_factor": "{reponse}",
    "proposal_quality": "{reponse}",
    "narrative_arc": "{reponse}",
    "unanticipated_objections": ["{objection1}", "{objection2}"]
  },
  "auto_analysis": {
    "diagnostic_accuracy": "{CORRECT|PARTIEL|INCORRECT}",
    "arc_fit": "{ADAPTE|A_AJUSTER}",
    "roi_accuracy": "{CREDIBLE|SUR_ESTIME|SOUS_ESTIME}",
    "pricing_fit": "{DANS_FOURCHETTE|TROP_HAUT|TROP_BAS}",
    "objections_anticipated": {N},
    "objections_total": {M}
  },
  "patterns": ["{pattern1}", "{pattern2}"],
  "recommendations": ["{reco1}", "{reco2}"]
}
```

### 6. Produire le fichier debrief enrichi

```
=== DEBRIEF v12 ===

Deal: {deal_id} · {nom entreprise}
Date debrief: {date}
Resultat: {Won | Lost | En cours}

CONTEXTE:
- Montant: {montant} EUR
- Arc narratif utilise: {arc du NBP}
- Contrainte principale: {description}
- Scenario recommande: {Pilotage | Production | Acceleration}
- Score audit SEO: {score}/100 (si /audit execute)

FEEDBACK CLOSER:
- Facteur decisif: {reponse}
- Qualite proposition: {reponse}
- Arc narratif: {reponse}
- Objections non anticipees: {liste}

AUTO-ANALYSE:
- Diagnostic contrainte: {verdict}
- Arc narratif: {verdict}
- ROI: {verdict}
- Pricing: {verdict}
- Objections: {verdict}

PATTERNS IDENTIFIES:
- {pattern 1}
- {pattern 2}
- {pattern 3}

RECOMMANDATIONS SYSTEME:
- {reco 1 pour ameliorer /prepare}
- {reco 2 pour ameliorer /audit}

WARNINGS POUR FUTURS /prepare:
- {warning 1 : condition → action}
- {warning 2 : condition → action}

=== FIN DEBRIEF ===
```

Ecrire dans : `.cache/deals/{deal_id}/debrief.md`

### 7. Mettre a jour le rapport patterns

```bash
python3 tools/debrief_aggregate.py
```

Le script lit tous les `debrief.json` et produit/met a jour :
- `.cache/patterns_report.md` (correlations cumulees)
- `.cache/debrief_warnings.md` (warnings pour futurs /prepare)

### 8. Injection dans futurs /prepare (NOUVEAU v12)

Ecrire/mettre a jour `.cache/debrief_warnings.md` :
```
# Warnings actifs (generes par /debrief)

## Arcs narratifs
- {arc X} : {win_rate}% won ({N} deals) — {recommandation}

## Objections recurrentes
- {objection} ({N} fois) — {pre-emption suggeree}

## Pricing
- {pattern pricing} — {ajustement suggere}
```

Ce fichier est lu par Pass 2 de /prepare pour injecter des warnings contextuels dans le processus narratif.

### 9. Message de fin

```
Debrief enregistre : .cache/deals/{deal_id}/debrief.md + debrief.json
Resultat : {Won | Lost | En cours}
Facteur decisif : {1 phrase}

Auto-analyse : Diag={verdict}, Arc={verdict}, ROI={verdict}
{N} debriefs au total. Rapport patterns mis a jour.
Warnings injectes dans les futurs /prepare.
```

## Reference

- Field keys Pipedrive : `context/pipedrive_reference.md`
- Artefacts /prepare : `.cache/deals/{deal_id}/artifacts/`
- Rapport patterns : `.cache/patterns_report.md`
- Warnings actifs : `.cache/debrief_warnings.md`
