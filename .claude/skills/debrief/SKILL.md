---
name: debrief
description: Collecte le resultat d'un deal (won/lost), le feedback closer, et alimente la boucle de retroaction.
disable-model-invocation: true
---

# DEBRIEF — Boucle de retroaction deal-to-deal

**Deal ID :** $ARGUMENTS

## Prerequis

1. Lis `agents/shared.md` (preambule partage, 18 regles)

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
- **r1_score** (field `e529595ef908cdf5851df4355bbce866f322fcae`)
- **Montant** : `value`
- **Lost reason** : `lost_reason` (si lost)

### 2. Collecter les artefacts existants

Verifier la presence de :
- `.cache/deals/{deal_id}/artifacts/PROPOSAL-*.html`
- `.cache/deals/{deal_id}/artifacts/INTERNAL-S7-*.md`
- `.cache/deals/{deal_id}/artifacts/strategy_plan_internal.md`
- `.cache/deals/{deal_id}/artifacts/NBP.md`
- `.cache/deals/{deal_id}/artifacts/SDB.md`

### 3. Demander le feedback closer

Poser ces questions au closer (via le terminal) :

1. **Resultat** : Won / Lost / En cours (confirmer avec Pipedrive)
2. **Facteur decisif** : "Quel a ete le facteur decisif pour le prospect ?" (1-2 phrases)
3. **Qualite proposition** : "La proposition etait-elle adaptee ? Qu'aurait-il fallu changer ?" (1-2 phrases)
4. **Arc narratif** : "L'angle strategique etait-il le bon ?" (1 phrase)
5. **Objections non anticipees** : "Y a-t-il eu des objections que la proposition n'avait pas pre-emptees ?" (liste)

### 4. Analyser et stocker

Produire le fichier debrief :

```
=== DEBRIEF ===

Deal: {deal_id} · {nom entreprise}
Date debrief: {date}
Resultat: {Won | Lost | En cours}

CONTEXTE:
- Score qualify: {r1_score}/100
- Montant: {montant} EUR
- Arc narratif utilise: {arc du NBP}
- S7 PRIMARY: {force} ({score}/5)
- Scenario recommande: {Essentiel | Performance | Croissance}
- Nombre de sections Diagnostic: {N}

FEEDBACK CLOSER:
- Facteur decisif: {reponse}
- Qualite proposition: {reponse}
- Arc narratif: {reponse}
- Objections non anticipees: {liste}

ANALYSE SYSTEME:
- [ ] Le S7 PRIMARY etait-il le bon ? (comparer avec le feedback)
- [ ] L'arc narratif etait-il adapte au profil decideur ?
- [ ] Le ROI etait-il credible ? (comparer avec le montant signe ou le feedback)
- [ ] Les objections auraient-elles pu etre pre-emptees par le SDB ?
- [ ] Le pricing etait-il dans la bonne fourchette ?

PATTERNS IDENTIFIES:
- {pattern 1 : ex "ROI x1.5+ correle avec won"}
- {pattern 2 : ex "Arc Technique fonctionne mieux pour les refontes"}
- {pattern 3 : ex "Objection budget non anticipee"}

RECOMMANDATIONS SYSTEME:
- {reco 1 pour ameliorer le processus /prepare}
- {reco 2 pour ameliorer le processus /qualify}

=== FIN DEBRIEF ===
```

Ecrire dans : `.cache/deals/{deal_id}/debrief.md`

### 5. Mettre a jour le rapport patterns (si >= 5 debriefs existent)

Verifier combien de fichiers debrief existent :
```bash
find .cache/deals/*/debrief.md 2>/dev/null | wc -l
```

Si >= 5 debriefs : produire un rapport transversal :

```
=== RAPPORT PATTERNS (N deals) ===

CORRELATIONS:
- Arc {X} : {N} deals, {win_rate}% won
- S7 PRIMARY S3 (Contenu) : {N} deals, {win_rate}% won
- ROI > x2 : {N} deals, {win_rate}% won
- Score qualify > 70 : {N} deals, {win_rate}% won

OBJECTIONS RECURRENTES:
1. {objection} ({N} fois) → {deja pre-emptee ? | a ajouter au systeme}
2. {objection} ({N} fois) → {idem}

RECOMMANDATIONS:
- {reco prioritaire basee sur les patterns}

=== FIN RAPPORT ===
```

Ecrire dans : `.cache/patterns_report.md`

### 6. Message de fin

```
Debrief enregistre : .cache/deals/{deal_id}/debrief.md
Resultat : {Won | Lost | En cours}
Facteur decisif : {1 phrase}
{N} debriefs au total. {Rapport patterns mis a jour. | Rapport patterns disponible apres {5-N} debriefs supplementaires.}
```

## Reference

- Field keys Pipedrive : `context/pipedrive_reference.md`
- Artefacts /prepare : `.cache/deals/{deal_id}/artifacts/`
