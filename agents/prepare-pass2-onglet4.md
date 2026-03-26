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


Bloc compact de 6 bullets maximum, issu du `strategy_plan_internal.md`. C'est ce que le decideur retient, ce qu'il presente a son board.

**Contrainte de longueur (STRICTE) :** chaque bullet = 1 phrase, max 120 caracteres.
Le decideur a 30 secondes. Si un bullet depasse 1 ligne a l'ecran, il est trop long.
Privilegier les chiffres aux mots : "319 kw vs 10 307 leader" plutot que
"La Mere Poulard capte 319 mots-cles alors que le leader en a 10 307".

1. Le probleme business (douleur chiffree)
2. Le cout de l'inaction (visites/euros/mois perdus)
3. Le levier principal (contrainte identifiee → action)
4. Les quick wins 90 jours (resultats rapides)
5. Le ROI attendu (conservateur, source)
6. L'investissement (fourchette selon scenario)

- Chaque bullet doit contenir AU MOINS un element concret parmi : chiffre, horizon (90j/6m/12m), ou condition ("si… alors…").

**Board-ready A4 (obligatoire, dans le HTML, accessible par bouton) :**

Page print-friendly (CSS `@media print`) qui reprend :
- En-tete : logo SLASHR + nom prospect + date
- Les 6 bullets du resume decisionnel
- Les priorites strategiques (contrainte + leviers)
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

## Sous-section Methode d'analyse (optionnel)

Bloc leger optionnel dans l'accordion FAQ/methodo. Le S7 en tant que framework n'est JAMAIS expose au client. Si la methode est mentionnee, c'est en termes generiques.

**Contenu (si inclus dans la FAQ) :**
- 2-3 phrases : "Notre analyse couvre 7 dimensions de votre visibilite Search (technique, contenu, concurrence, etc.). On identifie les 2-3 axes qui debloquent le plus de valeur pour votre situation, pas tout en parallele."
- Pas de noms de forces, pas de scores, pas de radar, pas de "S7".

**Regles :**
- Pas de jargon "framework", "methodology", "S7", "7 forces". Dire "notre analyse" ou "notre grille de priorisation"
- Ton : transparent, simple. Le prospect comprend pourquoi on ne fait pas tout.
- **Ne PAS repeter les scores** : ils sont dans l'onglet Diagnostic. Ici c'est la methode, pas le diagnostic.

---

## Phase 1 : Mission structurante (ponctuelle)

Phase 1 = mission calibree. Ce n'est PAS un pack. Voir `context/pricing_rules.md` pour le detail des blocs et le calcul.

Blocs :
- **Audit SEO** (5j, toujours actif)
- **Refonte SEO** (3-6j, si refonte prevue)
- **Activation contenu** (1j minimum, toujours actif)
- **SEA setup** (2j, si SEA_POSTURE = PILOTE ou CONSEIL)
  - PILOTE : audit campagnes existantes + structure compte + strategie encheres + plan activation 90j
  - CONSEIL : audit strategique + recommandations structure + cahier des charges pour equipe execution / agence media
- **GEO setup** (2j, si GEO/IA dans perimetre)
- **Social setup** (2j, si Social dans perimetre)

Budget = total jours x TJM (cf. `context/pricing_rules.md`).

**Regle d'affichage client (STRICTE) :** le HTML affiche le scope qualitatif + le budget global. Jamais de jours, jamais de TJM, jamais de sous-composants internes. Voir `context/output_contract.md`.

Le detail en jours est ecrit dans le fichier `INTERNAL-S7` (section "Budget interne").

**Regles de formulation Phase 1 :**
- Dire "Audit SEO complet" (pas juste "Audit complet")
- Benchmark concurrentiel : rester vague ("Benchmark concurrentiel"), ne pas s'engager sur un nombre d'acteurs
- Reporting : "Mise en place du reporting" (pas "Reporting mensuel", qui est un livrable Phase 2)
- **Non inclus (obligatoire)** : lister explicitement sous la highlight-box ce qui n'est PAS dans la Phase 1 (ex: "Non inclus dans la Phase 1 : audit GEO (visibilite IA), audit Social Search. Ces leviers peuvent etre actives apres le bilan, en accelerateur.")

---

## Phase 2 : Accompagnement mensuel (recurrent, sans engagement)

Apres le bilan a 90 jours, l'accompagnement continue **sans engagement**, ajustable chaque mois.

3 niveaux d'intensite avec labels client :
- **Pilotage** (1j/mois) : "On pilote, vous executez". Strategie, specs, monitoring.
- **Production** (2j/mois) : "On produit, vous validez". + production contenu + optimisations. **Recommande par defaut.**
- **Acceleration** (3j/mois) : "On accelere". + liens externes + couverture elargie.

Levier accelerateur : +700 EUR/mois ("Acceleration SEO, visibilite IA, Ads, reseaux sociaux").

Budget mensuel = jours/mois x TJM (cf. `context/pricing_rules.md`).

**Regle d'affichage client (STRICTE) :**
- Echelle de lecture en **4 colonnes alignees** (grid) : Pilotage / Production / Acceleration / +Levier accelerateur
- Production mis en avant visuellement (couleur accent)
- 1 recommandation snake-wrap au-dessus avec le budget recommande + details + budget annee 1
- Budget achat de liens : **mentionner explicitement "non inclus, facture a part selon la strategie definie"**
- Jamais de jours/mois, jamais de TJM. Voir `context/output_contract.md`.

**Regle de coherence levier :** si un levier a un setup Phase 1, il DOIT avoir un run Phase 2. Si un levier n'a PAS de setup, il ne peut PAS avoir de run.

---

## Trajectoire 6 mois (obligatoire)

Bloc "M4-M6" qui montre la montee en puissance post-Phase 1 :
- Quels axes strategiques passent de differe a actif
- Quels KPIs sont attendus a M6
- Comment l'intensite evolue

---

## Simulateur ROI (obligatoire)

Slide dedie avec sliders interactifs. Regles UX :
- **Sliders en colonne unique** (pas de grille 2 colonnes, ca casse l'alignement)
- **Gap reduit** entre les sliders (6px)
- **Justification sous chaque curseur** (sim-sub) : source de la donnee ou methode de calcul
  - Trafic actuel : "Source : Google Search Console, 90 derniers jours"
  - Gain trafic projete : "{min} a {max} clics/mois (detail dans l'onglet Strategie)"
  - Taux de conversion : "Benchmark e-commerce niche : X%, a confirmer via Analytics des M1"
  - Panier moyen : "Valeur moyenne par commande, a affiner avec vos donnees"
  - Budget mensuel : "Accompagnement Search, ajustable apres le bilan a 90 jours"
- **Resultats compacts** : 3 KPI (Trafic cible M12, CA additionnel annuel, ROI annee 1) sans justification redondante
- Pas de highlight-box (trop dense), une simple note de footnote pour le CVR

---

## Investissement : structure v12.0

Regle : 2 blocs separes (Phase 1 mission + Phase 2 accompagnement) + echelle de lecture 4 colonnes. Pas 3 packs egaux.
Le scenario recommande est la decision logique. Les autres ajustent l'intensite, pas la strategie.

**Bloc Phase 1 : "Mission structurante" :**
- **Pont strategique** (sous-titre) : {1 phrase qui relie la mission au diagnostic}
  Ex : "Poser les fondations Search avant la refonte — securiser ce qui existe, preparer ce qui manque"
- **Description qualitative contextualisee** : utiliser les `SERVICE_DESCRIPTIONS (description proposition)` du SDB pour decrire le scope. Ces descriptions montrent la methodologie (sequence analyse → clustering → arborescence → contenu → roadmap), les specificites du deal (dimensions B2C/B2B, concurrents, contraintes) et les livrables concrets. Ne JAMAIS utiliser de descriptions generiques ("liste de mots-cles, arborescence, recommandations"). Cf. `context/service_catalog.md`.
- Liste des livrables produits
- Budget global EUR HT
- Timeline ("demarrage sous X jours ouvres")

**Bloc Phase 2 : "Orchestration mensuelle" :**
- Explication pedagogique : "Chaque levier active necessite un accompagnement mensuel."
- 3 niveaux d'intensite presentes comme des curseurs, pas comme des packs :

1. **Essentiel** (recommande pour les PME / execution interne) :
   - **Pont strategique** (sous-titre) : {1 phrase qui relie au diagnostic, en langage client}
     Ex : "Pilotage de votre visibilite produit et suivi des positions cles"
   - Scope : pilotage + monitoring + reporting
   - Budget : {montant}/mois HT
   - Engagement : 12 mois

2. **Performance** (recommande, mis en avant visuellement) :
   - **Pont strategique** (sous-titre) : {1 phrase qui relie au diagnostic, en langage client}
     Ex : "Ce qui construit votre visibilite produit et securise votre migration"
   - Scope : + production deleguee + accompagnement continu
   - Budget : {montant}/mois HT
   - Engagement : 12 mois
   - Objectifs chiffres : {CA additionnel, timeline}

3. **Croissance** (pour les ambitions fortes / multi-leviers) :
   - **Pont strategique** (sous-titre) : {1 phrase qui relie au diagnostic, en langage client}
     Ex : "Visibilite produit + contenus + diffusion multi-canal : le search comme levier de croissance"
   - Scope : + leviers additionnels (SEA, GEO, Social) + amplification
   - Budget : {montant}/mois HT
   - Engagement : 12 mois

> **Regle Pont strategique :** chaque pricing card a un sous-titre de 1 phrase qui relie l'investissement au diagnostic. Traduit en impact client ("Ce qui construit votre visibilite produit"). Le sous-titre repond a la question implicite du prospect : "Qu'est-ce que je paie exactement et pourquoi ?"

**Sous-bloc "Ce que coute l'inaction" (OBLIGATOIRE, AVANT le pricing — ancrage psychologique) :**
- C'est le **seul endroit** de toute la proposition ou le cout de l'inaction est detaille
- **PLACEMENT :** le cout de l'inaction est positionne AVANT les pricing cards (Phase 1 + Phase 2). Le decideur voit d'abord ce qu'il perd, puis ce que ca coute d'agir.
- 3 impacts business max, lies aux donnees du diagnostic
- Chaque impact = chiffre + source (DataForSEO, GSC, Google Ads)
- Composant : highlight-box (style alerte)
- Pas de dramatisation, les chiffres suffisent
- INTERDIT : structure anaphorique ("Chaque mois sans X..." repete N fois). Varier les formulations.

**Pont "Du diagnostic aux campagnes" (CONDITIONNEL : si SEA_SIGNAL = EXPLICIT et SEA_POSTURE = CONSEIL) :**
- Place APRES le cout de l'inaction, AVANT les pricing cards
- Composant : highlight-box
- 3 bullets montrant la cascade organique → paid :
  1. **Phase 1** : cartographie d'intentions + audit technique = fondations partagees SEO & SEA
  2. **M3-M4** : activation campagnes sur les intentions commerciales identifiees en Phase 1
  3. **M6-M12** : synergie mesuree — baisse progressive du CPA paid grace au renfort organique (quality score, landing pages optimisees)
- Ton : factuel, pas de promesse. Le pont montre la logique, pas un resultat garanti.

---

## FAQ

3-5 questions pertinentes pour ce deal. Reponses specifiques, pas generiques.

**FAQ conditionnelles SEA (ajouter si SEA_SIGNAL = EXPLICIT) :**
- **"SLASHR gere-t-il les campagnes Google Ads au quotidien ?"** → "Non. SLASHR est un cabinet conseil Search. Nous definissons la strategie, l'architecture de compte et les KPIs. L'execution quotidienne (bid management, creation d'annonces, ajustements encheres) releve de votre equipe ou d'une agence media specialisee, sous notre pilotage strategique."
- **"Pourquoi commencer par le SEO si le besoin est en paid ?"** → "SEO et SEA partagent les memes fondations : mapping d'intentions de recherche, landing pages optimisees, architecture de site. Un compte Ads sans ces fondations gaspille du budget — quality score bas, pages non pertinentes, ciblage approximatif. La Phase 1 pose le socle commun."

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
- Cout de l'inaction (AVANT les prix)
- Pricing (Phase 1 + Phase 2) avec pont strategique
- Methode d'analyse (optionnel, dans FAQ)
- FAQ
- Prochaine etape
- CTA final

### SI PAS de refonte

Structure identique :
- Resume decisionnel (6 bullets)
- Board-ready A4
- Cout de l'inaction (AVANT les prix)
- Pricing (Phase 1 + Phase 2) avec pont strategique
- Methode d'analyse (optionnel, dans FAQ)
- FAQ
- Prochaine etape
- CTA final
