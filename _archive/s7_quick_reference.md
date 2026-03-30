# S7 Quick Reference

> Digest compact du modele S7. Pour le detail complet : `context/s7_search_operating_model.md`

---

## Les 7 forces (1 ligne chacune)

| # | Force | Mesure |
|---|-------|--------|
| S1 | Intentions de recherche | Alignement offre/demande search, couverture par bucket intent |
| S2 | Architecture & technique | Sante technique, performance, crawlabilite, donnees structurees |
| S3 | Creation de contenu | Ratio keywords couverts vs univers semantique |
| S4 | UX & Conversion | Experience utilisateur, taux de conversion, parcours monetisation |
| S5 | Autorite, signaux de confiance | DA, backlinks, notoriete marque, part marque/hors-marque |
| S6 | Diffusion multicanale | Presence YouTube, IA/GEO, Social Search |
| S7 | Amplification | Complementarite Paid/SEA, budget pub, temps forts |

## Echelle 0-5

| Score | Signification |
|-------|---------------|
| 0 | Inexistant |
| 1 | Critique (problemes majeurs bloquants) |
| 2 | Faible (fondations insuffisantes) |
| 3 | Correct (fonctionnel, pas optimise) |
| 4 | Bon (niveau marche) |
| 5 | Excellent (avantage competitif) |

## Classification

- **PRIMARY** (exactement 1) : contrainte qui bloque le plus de valeur. Justification 2-3 phrases data-first
- **SECONDARY** (1-2) : leviers a fort potentiel. 1 phrase chacun
- **DEFERRED-SEQUENTIAL** : forces qui seront activees quand PRIMARY/SECONDARY traite. "Sera active quand {condition}"
- **DEFERRED-SCOPE** : forces hors perimetre ou non pertinentes. "Hors perimetre car {raison}"
- **Max 3 leviers actifs** (1 PRIMARY + 2 SECONDARY), meme si le prospect demande les 7
- **Tiebreak** : si 2 forces a ≤ 1 point d'ecart → Confidence departage (High > Medium > Low)

## Anchors quantitatifs (reperes)

| Force | 0-1 | 2 | 3 | 4-5 |
|-------|-----|---|---|-----|
| S1 | < 5% TASM | 5-15% TASM | 15-35% TASM | > 35% TASM |
| S2 | Lighthouse < 50 | 50-79 | 80-89 | 90+ |
| S3 | < 5% kw couverts | 5-15% | 15-30% | > 30% |
| S4 | CVR < 0.3% | 0.3-0.7% | 0.7-1.5% | > 1.5% |
| S5 | DR < 20 | 20-35 | 35-50 | 50+ |
| S6 | 0 canal | 1 canal inactif | 2+ canaux irreguliers | Multi-canal actif |
| S7 | 0 paid | < 500 EUR/mois | Paid actif, pas de synergie | Strategie integree |

> Reperes indicatifs. Ajuster ±1 selon contexte sectoriel. Ecart ≥ 2 = justifier dans l'evidence log.

## 5 formulations interdites dans le diagnostic

1. "les concurrents avancent vite" → remplacer par le delta chiffre
2. "il est urgent d'agir" → remplacer par la fenetre temporelle factuelle
3. "le marche est concurrentiel" → remplacer par les metriques (KD, nb acteurs, volumes)
4. "fort potentiel de croissance" → remplacer par le chiffre cible source
5. Toute phrase qui passe le test de substitution

## Synthese obligatoire (post-grille)

```
CONTRAINTE PRINCIPALE : {force} (score {X}/5)
→ {pourquoi c'est le verrou, data-first}

LEVIERS PRIORITAIRES : {force A} + {force B}
→ {impact attendu si actives, chiffre}

PROJECTION PRIMARY : {direction} {delta chiffre} {source} → {horizon}
PROJECTION SECONDARY : {direction} {delta} → {horizon}

INSIGHT CENTRAL : {1 phrase non substituable}
```

> Projection obligatoire pour PRIMARY + SECONDARY. Format strict, source identifiee.
