# PASS 2 : ONGLET 3 — Investissement

> Ce fichier est reference par `agents/prepare-pass2.md`. Il definit la structure de l'onglet 3 (Investissement) selon le contexte du deal.

---

## Resume decisionnel (obligatoire, debut de l'onglet)

---

## Preuves & mesure (qualite)

### Evidence log (obligatoire)
Quand tu affiches un chiffre / une projection / un classement :
- indiquer la source (GSC/GA4/DataForSEO/Pipedrive/Drive/MCP)
- la methode (modele / hypothese)
- et referencer l'evidence (endpoint + timestamp + chemin cache)

### Hypotheses explicites
Si une estimation repose sur des hypotheses (CTR, conversion, panier moyen) :
- les lister
- donner un intervalle (min/max) plutot qu'une valeur unique
- proposer comment valider rapidement


Bloc compact de 6 bullets maximum, issu du `strategy_plan_internal.md`. C'est ce que le decideur retient, ce qu'il presente a son board. Chaque bullet est une phrase complete, chiffree, specifique.

1. Le probleme business (douleur chiffree)
2. Le cout de l'inaction (visites/euros/mois perdus)
3. Le levier principal (contrainte S7 → action)
4. Les quick wins 90 jours (resultats rapides)
5. Le ROI attendu (conservateur, source)
6. L'investissement (fourchette selon scenario)

- Chaque bullet doit contenir AU MOINS un element concret parmi : chiffre, horizon (90j/6m/12m), ou condition ("si… alors…").

**Board-ready A4 (obligatoire, dans le HTML, accessible par bouton) :**

Page print-friendly (CSS `@media print`) qui reprend :
- En-tete : logo SLASHR + nom prospect + date
- Les 6 bullets du resume decisionnel
- Le radar S7 (version print : niveaux de gris ou simplifie)
- Le ROI en 1 ligne
- Le pricing recommande
- 1 CTA : "Prochaine etape : [action datee]"
- Un encadre "Decision attendue" : {choix scenario} + {date cible} + {prochaine etape}

Le decideur peut imprimer cette page A4 pour son comite de direction. Accessible via un bouton "Version imprimable" dans l'onglet Investissement.

---

## Prochaine etape (obligatoire)

Bloc de 3 lignes max, au format :
- **Decision** : {scenario recommande} (ou {2 scenarios si incertitude})
- **Date** : {date proposee sous 7-10 jours}
- **Action** : "Atelier 60 min — valider hypotheses ROI + lancer Phase 1"

Regles :
- Date = relative ("semaine du …") si contexte AO / comite.
- Ton : simple, direct, pas de pression.

---

## Sous-section Methode S7

Bloc leger integre dans l'onglet (pas un onglet separe). Place avant le pricing ou dans l'accordion FAQ/methodo.

**Contenu :**
1. **Definition S7** : 2-3 phrases max. Quoi : un cadre d'analyse en 7 forces. Pourquoi : prioriser les actions a plus fort impact, pas tout faire en meme temps.
2. **7 forces** : liste compacte, 1 ligne par force (nom + ce qu'elle mesure, pas de score, les scores sont dans l'onglet Diagnostic).
3. **Regle d'arbitrage** : 1 phrase : "On ne travaille jamais les 7 forces en parallele. Le S7 identifie les 2-3 leviers qui debloquent le plus de valeur pour votre situation."

**Regles :**
- Pas de jargon "framework", "methodology", dire "grille d'analyse" ou "cadre de priorisation"
- Ton : transparent, simple. Le prospect comprend pourquoi on ne fait pas tout.
- **Ne PAS repeter les scores** : ils sont dans l'onglet Diagnostic. Ici c'est la methode, pas le diagnostic.

---

## Phase 1 : Mission structurante (ponctuelle)

Phase 1 = mission calibree. Ce n'est PAS un pack. Voir `context/pricing_rules.md` pour le detail des blocs et le calcul.

Blocs :
- **Audit SEO** (5j, toujours actif)
- **Refonte SEO** (3-6j, si refonte prevue)
- **Activation contenu** (1j minimum, toujours actif)
- **SEA setup** (2j, si SEA dans perimetre)
- **GEO setup** (2j, si GEO/IA dans perimetre)
- **Social setup** (2j, si Social dans perimetre)

Budget = total jours x TJM (cf. `context/pricing_rules.md`).

**Regle d'affichage client (STRICTE) :** le HTML affiche le scope qualitatif + le budget global. Jamais de jours, jamais de TJM, jamais de sous-composants internes. Voir `context/output_contract.md`.

Le detail en jours est ecrit dans le fichier `INTERNAL-S7` (section "Budget interne").

---

## Phase 2 : Orchestration mensuelle (recurrente)

Chaque levier active en Phase 1 implique un run mensuel incompressible (1j/mois minimum par levier). Voir `context/pricing_rules.md`.

3 niveaux d'intensite :
- **Essentiel** (1-2j/mois) : pilotage + monitoring. Execution internalisee.
- **Performance** (2-3j/mois) : + production deleguee. Pour les prospects qui delegent.
- **Croissance** (3-4+j/mois) : + multi-leviers + amplification. Ambitions fortes.

Budget mensuel = jours/mois x TJM (cf. `context/pricing_rules.md`).

**Regle d'affichage client (STRICTE) :** le HTML affiche le scope qualitatif par niveau + le budget mensuel. Jamais de jours/mois, jamais de TJM. Voir `context/output_contract.md`.

**Regle de coherence levier :** si un levier a un setup Phase 1, il DOIT avoir un run Phase 2. Si un levier n'a PAS de setup, il ne peut PAS avoir de run.

---

## Trajectoire 6 mois (obligatoire)

Bloc "M4-M6" qui montre la montee en puissance post-Phase 1 :
- Quels piliers S7 passent de DEFERRED a actif
- Quels KPIs sont attendus a M6
- Comment l'intensite evolue

---

## Investissement : structure v12.0

Regle : 2 blocs separes (Phase 1 mission + Phase 2 orchestration) + 3 niveaux d'intensite. Pas 3 packs egaux.
Le scenario recommande est la decision logique. Les deux autres ajustent l'intensite, pas la strategie.

**Bloc Phase 1 : "Mission structurante" :**
- **Pont S7** (sous-titre) : {1 phrase qui relie la mission au diagnostic}
  Ex : "Poser les fondations Search avant la refonte — securiser ce qui existe, preparer ce qui manque"
- Description qualitative de ce que la mission inclut (JAMAIS de jours, JAMAIS de TJM)
- Liste des livrables produits
- Budget global EUR HT
- Timeline ("demarrage sous X jours ouvres")

**Bloc Phase 2 : "Orchestration mensuelle" :**
- Explication pedagogique : "Chaque levier active necessite un accompagnement mensuel."
- 3 niveaux d'intensite presentes comme des curseurs, pas comme des packs :

1. **Essentiel** (recommande pour les PME / execution interne) :
   - **Pont S7** (sous-titre) : {1 phrase qui relie au diagnostic, en langage client}
     Ex : "Pilotage de votre visibilite produit et suivi des positions cles"
   - Scope : pilotage + monitoring + reporting
   - Budget : {montant}/mois HT
   - Engagement : 12 mois

2. **Performance** (recommande, mis en avant visuellement) :
   - **Pont S7** (sous-titre) : {1 phrase qui relie au diagnostic, en langage client}
     Ex : "Ce qui construit votre visibilite produit et securise votre migration"
   - Scope : + production deleguee + accompagnement continu
   - Budget : {montant}/mois HT
   - Engagement : 12 mois
   - Objectifs chiffres : {CA additionnel, timeline}

3. **Croissance** (pour les ambitions fortes / multi-leviers) :
   - **Pont S7** (sous-titre) : {1 phrase qui relie au diagnostic, en langage client}
     Ex : "Visibilite produit + contenus + diffusion multi-canal : le search comme levier de croissance"
   - Scope : + leviers additionnels (SEA, GEO, Social) + amplification
   - Budget : {montant}/mois HT
   - Engagement : 12 mois

> **Regle Pont S7 :** chaque pricing card a un sous-titre de 1 phrase qui relie l'investissement au diagnostic S7. Pas de jargon S7 ("PRIMARY S3") — traduit en impact client ("Ce qui construit votre visibilite produit"). Le sous-titre repond a la question implicite du prospect : "Qu'est-ce que je paie exactement et pourquoi ?"

**Sous-bloc "Ce que coute l'inaction" (OBLIGATOIRE, unique endroit) :**
- C'est le **seul endroit** de toute la proposition ou le cout de l'inaction est detaille
- 3 impacts business max, lies aux donnees du diagnostic
- Chaque impact = chiffre + source DataForSEO/S7
- Composant : s7-insight (meme style visuel que la contrainte S7)
- Pas de dramatisation, les chiffres suffisent
- INTERDIT : structure anaphorique ("Chaque mois sans X..." repete N fois). Varier les formulations.

---

## FAQ

3-5 questions pertinentes pour ce deal. Reponses specifiques, pas generiques.

---

## CTA decisionnel

Verbe d'action strategique lie a la Phase 1 ("Demarrer", "Valider", "Activer", "Lancer").
INTERDIT : "Planifier un echange", "Discuter", "Echanger", "En savoir plus".

---

## Structure conditionnelle selon contexte deal

### SI refonte prevue

Les 3 actes refonte (Securiser/Transformer/Accelerer) sont dans l'onglet **Diagnostic** (ils font partie du diagnostic contextualise). L'onglet Investissement garde la meme structure quel que soit le contexte :

Structure :
- Resume decisionnel (6 bullets)
- Board-ready A4
- Pricing (Phase 1 + Phase 2) avec pont S7
- Cout de l'inaction
- Methode S7
- FAQ
- Prochaine etape
- CTA final

### SI PAS de refonte

Structure identique :
- Resume decisionnel (6 bullets)
- Board-ready A4
- Pricing (Phase 1 + Phase 2) avec pont S7
- Cout de l'inaction
- Methode S7
- FAQ
- Prochaine etape
- CTA final
