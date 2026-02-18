# PASS 2 — NARRATIVE ARCHITECT

## Role

Prendre le SDB et construire le plan narratif complet. Choisir l'angle, l'arc emotionnel, la sequence des sections pour chacun des **4 onglets MVP**. Decider du contenu textuel de chaque section (titres, angles, arguments). **NE PAS choisir de composants visuels — c'est le role de la Pass 3.**

---

## Etape 2.1 — Choisir le hook

Quelle est l'information la plus frappante pour ce prospect ? C'est ca qui ouvre apres le hero dans l'onglet Strategie.

- Gap concurrentiel massif → ouvrir par le face-a-face
- Verbatim du prospect qui pose la bonne question → ouvrir par la citation + reponse
- Chiffre d'inaction parlant → ouvrir par le cout de l'inaction (les donnees, pas le drame)
- Paradoxe (forte notoriete, faible visibilite) → ouvrir par le constat
- Opportunite claire et chiffree → ouvrir par le potentiel

---

## Etape 2.2 — Definir l'arc narratif de l'onglet Strategie

L'onglet Strategie est une **sequence de sections libres**. L'agent cree les sections qu'il veut, dans l'ordre qu'il veut. Il n'y a pas de liste fixe — il y a un objectif : **emmener ce decideur du constat a la conviction, avec ces donnees, dans ce contexte.**

### Arcs types (non limitatifs)

| Arc | Sequence | Quand l'utiliser |
|-----|----------|------------------|
| Classique | Constat → Diagnostic → Enjeu → Recommandation → Investissement | Deal standard, decideur rationnel |
| Urgence | Cout de l'inaction → Gap → Quick wins → Plan → Investissement | Urgence reelle (donnees), decideur presse |
| Opportunite | Verbatim → Ce qu'on a trouve → Territoires a prendre → Comment → Investissement | Prospect curieux, pas encore en douleur |
| Technique | Etat actuel → Ce qui marche → Ce qui manque → Architecture cible → Plan → Investissement | Decideur technique, refonte |
| Custom | Tout autre enchainement justifie par le contexte | Quand aucun arc type ne colle |

### Nombre de sections

Autant que necessaire, pas plus.
- Un deal simple : 5-6 sections
- Un deal complexe : 8-10 sections
- Chaque section doit justifier son existence — si elle n'apporte rien de nouveau, elle n'existe pas

---

## Etape 2.3 — Planifier les 4 onglets MVP

La proposition HTML a toujours **4 onglets**. Aucun n'est optionnel.

### Onglet 1 : Strategie (decision-driving)

C'est l'onglet principal. Il contient :
- Le **hero** (nom prospect, accroche, sous-titre)
- Les **sections libres** suivant l'arc narratif
- La **section S7 "Lecture strategique"** (obligatoire — voir ci-dessous)
- Le **CTA** en fin d'onglet

**Les anciens onglets conditionnels (SEO, GEO/IA, SEA, Social, Tech/UX) deviennent des SECTIONS dans l'onglet Strategie** quand les donnees le justifient. Un deal avec des donnees GEO aura une section "Visibilite IA" dans l'onglet Strategie — pas un onglet separe.

**Pas de section "Pourquoi SLASHR" standalone.** Les differenciateurs sont tisses apres chaque bloc de donnees, en enchainage naturel (cf. Etape 2.4).

#### Section S7 "Lecture strategique" (obligatoire dans l'onglet Strategie)

Bloc compact qui traduit le diagnostic S7 interne en lecture C-level. Place apres le diagnostic et avant la recommandation dans l'arc narratif.

**Contenu :**
1. **Radar 7 forces** — visualisation SVG/canvas des 7 scores (0-5). Pas de legende longue : le nom de chaque force + son score suffit.
2. **Contrainte principale** — 1 highlight box qui nomme la force limitante et son implication business en 1-2 phrases.
3. **Leviers prioritaires** — 1-2 forces secondaires activees, avec l'impact attendu chiffre.
4. **Insight central** — 1 phrase de synthese strategique, non generique (doit echouer au test de substitution).

**Regles :**
- **Ne jamais recommander de travailler les 7 forces.** Le S7 sert a prioriser, pas a tout faire. Si les 7 forces sont affichees dans le radar, seules 2-3 sont mises en avant comme leviers d'action.
- Les forces non priorisees ne sont pas cachees — elles sont visibles dans le radar mais **pas commentees** (le prospect voit le score, pas une recommandation dessus).
- Le texte est C-level : phrases courtes, chiffres, zero jargon SEO non traduit.
- Le bloc reste **compact** — pas plus de 1 radar + 1 highlight box + 2-3 lignes de leviers + 1 phrase d'insight.

### Onglet 2 : Cas Clients (social proof)

2-4 cas clients comparables au prospect, selectionnes dans le SDB. Pour chaque cas :
- **Situation initiale** en chiffres
- **Ce qu'on a fait** en 1-2 phrases
- **Resultats** en chiffres + timeline
- **Citation client** si disponible dans `context/case_studies.md`

L'agent adapte l'angle de presentation de chaque cas pour faire resonner avec la situation du prospect. Un cas identique peut etre presente differemment selon le prospect.

### Onglet 3 : ROI Interactif (engagement)

- **Hypotheses pre-remplies** avec les donnees reelles du SDB (trafic actuel, multiplicateur source du gap, CVR, panier moyen)
- **Source de chaque hypothese** visible (pas de chiffres sans provenance)
- **Simulateur interactif** (sliders que le prospect manipule)
- **3 scenarios calcules** alignes sur les scenarios d'engagement (Essentiel / Performance / Croissance)
- **Methodologie** : explication en 1-2 phrases de la logique de calcul

### Onglet 4 : Livrables & Methode (transparence)

**Sous-section "Methode S7" dans cet onglet :**

Bloc leger integre dans l'onglet Livrables & Methode (pas un onglet separe). Place avant le pricing ou dans l'accordion FAQ/methodo.

**Contenu :**
1. **Definition S7** — 2-3 phrases max. Quoi : un cadre d'analyse en 7 forces. Pourquoi : prioriser les actions a plus fort impact, pas tout faire en meme temps.
2. **7 forces** — liste compacte, 1 ligne par force (nom + ce qu'elle mesure, pas de score — les scores sont dans l'onglet Strategie).
3. **Regle d'arbitrage** — 1 phrase : "On ne travaille jamais les 7 forces en parallele. Le S7 identifie les 2-3 leviers qui debloquent le plus de valeur pour votre situation."

**Regles :**
- Pas de jargon "framework", "methodology" — dire "grille d'analyse" ou "cadre de priorisation"
- Ton : transparent, simple. Le prospect comprend pourquoi on ne fait pas tout.
- **Ne PAS repeter les scores** — ils sont dans l'onglet Strategie. Ici c'est la methode, pas le diagnostic.

**Resume decisionnel (obligatoire — debut de l'onglet Livrables) :**

Bloc compact de 6 bullets maximum, issu du `strategy_plan_internal.md`. C'est ce que le decideur retient, ce qu'il presente a son board. Chaque bullet est une phrase complete, chiffree, specifique.

1. Le probleme business (douleur chiffree)
2. Le cout de l'inaction (visites/euros/mois perdus)
3. Le levier principal (contrainte S7 → action)
4. Les quick wins 90 jours (resultats rapides)
5. Le ROI attendu (conservateur, source)
6. L'investissement (fourchette selon scenario)

**Board-ready A4 (obligatoire — dans le HTML, accessible par bouton) :**

Page print-friendly (CSS `@media print`) qui reprend :
- En-tete : logo SLASHR + nom prospect + date
- Les 6 bullets du resume decisionnel
- Le radar S7 (version print : niveaux de gris ou simplifie)
- Le ROI en 1 ligne
- Le pricing recommande
- 1 CTA : "Prochaine etape : [action datee]"

Le decideur peut imprimer cette page A4 pour son comite de direction. Accessible via un bouton "Version imprimable" dans l'onglet Livrables.

**Phase 1 — Mission structurante (ponctuelle) :**

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

**Phase 2 — Orchestration mensuelle (recurrente) :**

Chaque levier active en Phase 1 implique un run mensuel incompressible (1j/mois minimum par levier). Voir `context/pricing_rules.md`.

3 niveaux d'intensite :
- **Essentiel** (1-2j/mois) : pilotage + monitoring. Execution internalisee.
- **Performance** (2-3j/mois) : + production deleguee. Pour les prospects qui delegent.
- **Croissance** (3-4+j/mois) : + multi-leviers + amplification. Ambitions fortes.

Budget mensuel = jours/mois x TJM (cf. `context/pricing_rules.md`).

**Regle d'affichage client (STRICTE) :** le HTML affiche le scope qualitatif par niveau + le budget mensuel. Jamais de jours/mois, jamais de TJM. Voir `context/output_contract.md`.

**Regle de coherence levier :** si un levier a un setup Phase 1, il DOIT avoir un run Phase 2. Si un levier n'a PAS de setup, il ne peut PAS avoir de run.

**Trajectoire 6 mois obligatoire :**

Bloc "M4-M6" qui montre la montee en puissance post-Phase 1 :
- Quels piliers S7 passent de DEFERRED a actif
- Quels KPIs sont attendus a M6
- Comment l'intensite evolue

**Pricing :**
- 3 scenarios d'intensite (Essentiel / Performance / Croissance)
- Le scenario recommande est mis en evidence
- Chaque scenario affiche : scope qualitatif + budget Phase 1 + budget Phase 2/mois + engagement

**FAQ :**
- 3-5 questions pertinentes pour ce deal
- Reponses specifiques, pas generiques

**CTA** en fin d'onglet

---

## Etape 2.4 — Integration des avantages competitifs

Pour chaque section de l'onglet Strategie qui presente des donnees, formuler la **transition SLASHR** — comment l'expertise SLASHR adresse specifiquement ce constat.

**Regles :**
- La transition vient **apres** le bloc de donnees, jamais avant
- Elle est **specifique** au constat presente (pas une phrase generique)
- Elle est **naturelle** — un enchainage logique, pas une publicite
- Elle ne mentionne **jamais** "Pourquoi nous" ou "Nos avantages"

**Exemples :**

| Constat presente | Transition SLASHR |
|------------------|-------------------|
| Gap concurrentiel x4 en trafic hors-marque | "C'est ce type de gap qu'une architecture Search structuree peut combler. Notre methode identifie les clusters a plus fort potentiel et les priorise par impact business." |
| Score Lighthouse de 38 | "Ces fondations techniques conditionnent tout le reste. C'est le premier livrable de la Phase 1 Audit : un cahier des charges technique priorise pour votre equipe dev." |
| 0 resultat IA sur les requetes metier | "La visibilite IA se construit sur des donnees structurees et du contenu expert. C'est ce que notre pilier Production couvre dans l'accompagnement." |

---

## Etape 2.5 — Tests de validation pre-generation

### Test anti-generique

Avant de passer a la Pass 3, verifier :
- [ ] Chaque titre de section contient le nom du prospect OU un element specifique a leur situation
- [ ] Les donnees referencent des chiffres reels (positions, keywords, volumes)
- [ ] Le cout d'inaction est calcule avec LEUR gap, pas une formule passe-partout
- [ ] Les verbatims du prospect apparaissent (si disponibles)
- [ ] Aucune phrase ne marcherait pour n'importe quel autre prospect
- [ ] L'arc narratif est justifie par le profil du decideur et le contexte du deal
- [ ] Les cas clients sont matche au prospect, pas choisis au hasard
- [ ] La section "Ce que cela implique" contient 3 bullets max en impact business (pas technique)
- [ ] La section "Decision strategique recommandee" contient une phrase affirmative avec "Nous recommandons"
- [ ] La sous-section "90 jours" contient 3 etapes max alignees sur la contrainte S7 PRIMARY uniquement
- [ ] La sequence S7 → Implications → Decision → 90 jours est complete et dans cet ordre

### Test de tonalite

- [ ] **Zero pression commerciale** — aucune phrase du type "ne manquez pas", "il est urgent de", "derniere chance"
- [ ] **Zero dramatisation** — aucune phrase du type "catastrophe", "crise", "vous perdez tout". Les donnees parlent d'elles-memes
- [ ] **Intelligence strategique** — chaque phrase traduit une expertise en impact business mesurable
- [ ] **Expertise → impact** — pas de jargon technique brut. "DA de 15" → "une autorite de domaine faible qui limite votre capacite a vous positionner sur les requetes concurrentielles"
- [ ] **Transitions SLASHR naturelles** — chaque differenciateur est lie a un data block, jamais standalone

---

## Output Pass 2 : Narrative Blueprint (NBP)

L'agent DOIT ecrire explicitement ce document interne avant de passer a la Pass 3.

```
=== NARRATIVE BLUEPRINT ===

ARC GLOBAL: {type d'arc choisi} — {justification en 1 ligne liee au decideur et au contexte}
HOOK: {description du hook et pourquoi il est frappant pour ce prospect}
PROFIL DECIDEUR: {type} — sensible a: {preoccupation principale}

--- ONGLET STRATEGIE ---

1. {Titre section} — role: {accroche / diagnostic / enjeu / opportunite / recommandation / ...}
   Angle: {description en 1-2 phrases de ce que cette section dit}
   Donnees utilisees: {quelles donnees du SDB alimentent cette section}
   Transition SLASHR: {phrase de transition apres le data block}
   Pourquoi ici: {justification de sa position dans l'arc}

2. {Titre section} — role: {...]
   ...

X. Section S7 "Lecture strategique" — role: priorisation / conviction
   Radar: {7 forces avec scores}
   Contrainte principale: {force + implication business}
   Leviers: {2-3 forces priorisees + impact chiffre}
   Insight: {1 phrase non generique}
   Pourquoi ici: {apres le diagnostic, avant la recommandation — c'est le pont}

X+1. Section "Ce que cela implique" — role: verrou narratif decisionnel (OBLIGATOIRE)
   3 bullets max — reformulation de la contrainte S7 en impact business C-level
   Ton: direct, affirmatif, zero jargon technique
   Chaque bullet relie la contrainte S7 a une consequence business concrete
   Pourquoi ici: {le prospect a compris le diagnostic — maintenant il doit voir la decision}

X+2. Section "Decision strategique recommandee" — role: declencheur de decision (OBLIGATOIRE)
   Titre: "Decision strategique recommandee" (avec emoji cible)
   1 phrase tranchee, affirmative, non conditionnelle, non vague
   Liee explicitement a la contrainte S7 PRIMARY
   Format: "Nous recommandons de [action] car [raison liee au S7]."
   Pourquoi ici: {la decision doit etre formulee noir sur blanc avant de parler methode}

X+3. Sous-bloc "Ce que cela signifie concretement (90 jours)" — role: projection immediate
   3 etapes max alignees strictement sur la contrainte S7 PRIMARY
   Pas de liste generique — seulement ce qui decoule du diagnostic
   Chaque etape = action concrete + livrable ou KPI attendu
   Pourquoi ici: {la decision est prise — le prospect voit immediatement ce que ca donne}

N. CTA — toujours en dernier (REGLE v10.4 : CTA DECISIONNEL)
   Interdit : "Planifier un echange", "Discuter", "Echanger", "En savoir plus", ou tout verbe passif/generique
   Obligatoire : CTA oriente decision, lie a la trajectoire 90 jours si elle existe
   Exemples : "Demarrer la Phase 1", "Valider le lancement Phase 1", "Activer la Phase 1 (90 jours)"
   Le libelle du bouton CTA doit correspondre a la decision recommandee de la section precedente
   Si aucun verbe d'action strategique n'est present dans le CTA, la generation echoue

--- ONGLET LIVRABLES (sous-section Methode S7) ---

Definition: {2-3 phrases — cadre, pourquoi prioriser}
7 forces: {liste 1 ligne chacune — nom + ce que ca mesure}
Regle arbitrage: {1 phrase — on ne fait pas tout}

--- ONGLET CAS CLIENTS ---

Cas 1: {entreprise} — {problematique similaire au prospect}
  Avant: {chiffres cles}
  Action: {levier en 1-2 phrases}
  Apres: {chiffres cles + timeline}
  Citation: "{verbatim}" — {prenom, role}
  Angle prospect: {pourquoi ce cas parle a CE prospect}

Cas 2: ...

--- ONGLET ROI INTERACTIF ---

Hypotheses pre-remplies:
- Trafic actuel: {X} visites/mois (source: DataForSEO domain_rank_overview)
- Multiplicateur: {Y} (source: gap vs {concurrent}, ratio x{Z})
- CVR: {W}% (source: {benchmark secteur / donnee prospect / estimation conservatrice})
- Panier moyen: {V} EUR (source: {donnee prospect / estimation secteur})
- Investissement mensuel: {fourchette selon scenario}

3 scenarios: Essentiel ({prix}) / Performance ({prix}) / Croissance ({prix})

--- ONGLET LIVRABLES & METHODE (ou "REFONTE & METHODE" si refonte) ---

### Regle narrative v11.2 : la page raconte une histoire en 3 actes, pas une juxtaposition de blocs.

### Structure onglet — conditionnelle selon contexte deal

**SI le deal comporte une refonte prevue** (detectee dans transcript/brief/notes/Pipedrive) :

Ouverture narrative : hero court (60vh) qui pose les 3 objectifs — "Securiser. Activer. Accelerer."
Label onglet dans la nav : "Refonte & Methode" (pas "Livrables & Methode")

ACTE 1 — "Securiser la refonte"
   Transition narrative : on commence par la peur — ce que la migration risque de couter si non pilotee
   - AMOA SEO : {role SLASHR, coordination agence web, comite bi-mensuel}
   - Plan de redirections : {scope — nombre d'URLs, methode 1:1}
   - Recette technique : {validation pre-bascule — crawl, indexation, donnees structurees}
   - Monitoring post-bascule : {alertes, suivi J+1 a J+30, correction immediate}
   - Rassurance obligatoire : "Objectif : 0 perte de trafic strategique lors de la migration."
   - Pont narratif vers Acte 2 : relier a un cas client si pertinent

ACTE 2 — "Transformer la refonte en levier de croissance"
   Transition narrative : on passe de la defense a l'attaque — la refonte devient un accelerateur
   - Activation du levier S7 PRIMARY : {actions concretes liees a la contrainte principale}
   - Pages piliers prioritaires : {clusters, volumes, calendrier pre-migration}
   - Architecture & donnees structurees : {integrees au cahier des charges refonte}
   - Livraison avant migration : {les pages rankent avant la bascule — la migration les transfere}
   - Pont narratif vers Acte 3 : projeter vers la montee en puissance post-bascule

ACTE 3 — "Accelerer apres la migration"
   Transition narrative : le site est securise, les pages rankent — on accelere vers les objectifs business
   - Production contenu : {rythme — X pages/mois, clusters cibles}
   - Netlinking : {strategie si pertinente, sinon justifier le report}
   - Amplification : {pics saisonniers, paid complementaire}
   - Monitoring & reporting : {routine, frequence, KPIs suivis}
   - Pont narratif : relier aux pics saisonniers du prospect pour ancrer dans le reel

Chaque acte doit etre coherent avec la contrainte S7 PRIMARY du deal.
Chaque acte doit contenir un pont narratif (highlight-box) qui fait la transition vers le suivant.

APRES les 3 actes :

Synthese (6 bullets) :
1. {douleur business chiffree}
2. {cout inaction}
3. {levier principal}
4. {securisation refonte}
5. {ROI attendu}
6. {investissement}

Board-ready A4: oui (bouton "Version imprimable")

### Investissement — structure v12.0 : Phase 1 + Phase 2 + 3 intensites

Regle : 2 blocs separes (Phase 1 mission + Phase 2 orchestration) + 3 niveaux d'intensite. Pas 3 packs egaux.
Le scenario recommande est la decision logique. Les deux autres ajustent l'intensite, pas la strategie.

**Bloc Phase 1 — "Mission structurante" :**
- Description qualitative de ce que la mission inclut (JAMAIS de jours, JAMAIS de TJM)
- Liste des livrables produits
- Budget global EUR HT
- Timeline ("demarrage sous X jours ouvres")

**Bloc Phase 2 — "Orchestration mensuelle" :**
- Explication pedagogique : "Chaque levier active necessite un accompagnement mensuel."
- 3 niveaux d'intensite presentes comme des curseurs, pas comme des packs :

1. **Essentiel** (recommande pour les PME / execution interne) :
   - Scope : pilotage + monitoring + reporting
   - Budget : {montant}/mois HT
   - Engagement : 12 mois

2. **Performance** (recommande — mis en avant visuellement) :
   - Scope : + production deleguee + accompagnement continu
   - Budget : {montant}/mois HT
   - Engagement : 12 mois
   - Objectifs chiffres : {CA additionnel, timeline}

3. **Croissance** (pour les ambitions fortes / multi-leviers) :
   - Scope : + leviers additionnels (SEA, GEO, Social) + amplification
   - Budget : {montant}/mois HT
   - Engagement : 12 mois

4. Sous-bloc "Ce que coute l'inaction" (OBLIGATOIRE) :
   - 3 impacts business max, lies aux donnees du diagnostic
   - Chaque impact = chiffre + source DataForSEO/S7
   - Composant : s7-insight (meme style visuel que la contrainte S7)
   - Pas de dramatisation — les chiffres suffisent

FAQ: {3-5 questions pertinentes pour ce deal}

CTA decisionnel unique (v10.4) : {verbe d'action strategique lie a la Phase 1}

**SI le deal NE comporte PAS de refonte** :

Structure standard :
- Phase 1 (90 jours) : M1/M2/M3
- Phase 2 (Run) : intensite + piliers + trajectoire M4-M6
- Synthese (6 bullets) + Board-ready A4
- Investissement (meme logique v11.3 : 1 reco + 2 variantes + cout inaction)
- FAQ
- CTA decisionnel

Scenario recommande: {lequel et pourquoi}

=== FIN NBP ===
```
