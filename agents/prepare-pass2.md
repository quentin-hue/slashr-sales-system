# PASS 2 : NARRATIVE ARCHITECT

## Role

---

## Cadre qualite Pass 2 (narration decision-ready)

### Regle : Pass 2 consomme le SDB thin (pas de data brute)
- Ne jamais coller de dumps (emails entiers, CSV longs, exports bruts).
- Utiliser les syntheses + references vers evidence.

### Faits / Hypotheses / Manquants (obligatoire)
Dans la recommendation (NBP), garder 3 sections courtes :
- **FAITS** : 6 bullets max, sourcés
- **HYPOTHESES** : 4 bullets max, confiance + validation
- **MANQUANTS** : 6 bullets max, impact + plan B + acces minimal

### Evidence Gate (leger)
- Chaque axe de reco doit etre relie a 1 fait OU explicite comme hypothese.


Prendre le SDB et construire le plan narratif complet. Choisir l'angle, l'arc emotionnel, la sequence des sections pour chacun des **3 onglets MVP** (Diagnostic, Strategie, Investissement). Decider du contenu textuel de chaque section (titres, angles, arguments). **NE PAS choisir de composants visuels, c'est le role de la Pass 3.**

### Champs SDB enrichis (consommes par Pass 2)

- `DECIDEUR_LEVEL` : adapter le ton (DECIDEUR → decision directe, INFLUENCEUR → board-ready A4 crucial, OPERATIONNEL → passage par le N+1)
- `PERIMETRE_SLASHR` : cadrer la recommandation (ne pas recommander hors perimetre)
- `REFONTE` : si refonte, les 3 actes (Securiser/Transformer/Accelerer) sont dans l'onglet Diagnostic
- `MODULES_ACTIFS` : savoir quels blocs de donnees sont disponibles dans le SDB
- `NARRATIVE_HINTS` : point de depart pour l'etape de deduplication (non-contraignant)
- `TRANSITION_OPPORTUNITIES` : obsolete (les transitions SLASHR sont supprimees, cf. Etape 2.4)
- `ROI Confidence globale` : determine si le label "Recommandation conditionnelle" est necessaire
- `CAS CLIENTS RETENUS` enrichis : `match_criteria`, `key_metric`, `sdb_juxtaposition`, `angle` par cas

---

## Etape 2.1 : Choisir le hook

Quelle est l'information la plus frappante pour ce prospect ? C'est ca qui ouvre apres le hero dans l'onglet Diagnostic.

- Gap concurrentiel massif → ouvrir par le face-a-face
- Verbatim du prospect qui pose la bonne question → ouvrir par la citation + reponse
- Chiffre d'inaction parlant → ouvrir par le cout de l'inaction (les donnees, pas le drame)
- Paradoxe (forte notoriete, faible visibilite) → ouvrir par le constat
- Opportunite claire et chiffree → ouvrir par le potentiel
- Ancrage identitaire → le hero tisse l'histoire de la marque/du prospect dans le constat. Pas de nostalgie ni de flatterie : un fait de marque qui rend le gap Search d'autant plus frappant. Ex : "Depuis 1888, La Mere Poulard fait les meilleurs palets. En 2026, personne ne les trouve en ligne." Usage : quand le prospect a une marque forte + un gap Search mesurable.

### Cascade narrative ouverture (OBLIGATOIRE)

L'ouverture de la proposition suit une cascade en 3 couches. Chaque couche avance le recit — aucune ne repete la precedente.

| Couche | Role | Contenu | Contrainte |
|--------|------|---------|------------|
| Hero subtitle | **QUOI** — la tension | Paradoxe ou contraste, sans data | Max 80 chars, teaser pur |
| H2 section 1 | **POURQUOI** — le mecanisme | Le fait qui explique la tension | Max 12 mots, 1 fait cle |
| KPIs section 1 | **PREUVE** — les donnees | Chiffres sources qui prouvent le mecanisme | 3-4 data points, tous sources |

**Test de non-repetition** : lire les 3 couches a la suite. Si deux couches disent la meme chose avec des mots differents, l'une est redondante — la reecrire pour qu'elle apporte un nouvel element.

**Exemple :**
- Subtitle : "Tout le monde vous cherche. Presque personne n'achete." (tension)
- H2 : "80% de votre trafic cherche votre nom. Pas vos produits." (mecanisme : dependance brandee)
- KPIs : 14 800 recherches brandees · 319 kw indexes · 55 745 EUR CA web (preuves)

---

## Etape 2.2 : Definir l'arc narratif de l'onglet Diagnostic

L'onglet Diagnostic est une **sequence de sections libres**. L'agent cree les sections qu'il veut, dans l'ordre qu'il veut. Il n'y a pas de liste fixe, il y a un objectif : **emmener ce decideur du constat a la conviction, avec ces donnees, dans ce contexte.**

### Arcs types (non limitatifs)

| Arc | Sequence | Quand l'utiliser |
|-----|----------|------------------|
| Classique | Constat → Diagnostic → Enjeu → Recommandation → Investissement | Deal standard, decideur rationnel |
| Urgence | Cout de l'inaction → Gap → Quick wins → Plan → Investissement | Urgence reelle (donnees), decideur presse |
| Opportunite | Verbatim → Ce qu'on a trouve → Territoires a prendre → Comment → Investissement | Prospect curieux, pas encore en douleur |
| Technique | Etat actuel → Ce qui marche → Ce qui manque → Architecture cible → Plan → Investissement | Decideur technique, refonte |
| Custom | Tout autre enchainement justifie par le contexte | Quand aucun arc type ne colle |

### Etape de deduplication (OBLIGATOIRE avant de creer les sections)

Avant de creer les sections, regrouper les blocs du SDB qui alimentent le **meme argument**. Un argument = une section. Plusieurs blocs de data qui disent la meme chose (ex: "le prospect est invisible hors-marque") = 1 section avec plusieurs composants visuels, pas plusieurs sections.

**Processus :**
1. Lire les `NARRATIVE_HINTS` du SDB (si presents). Ils suggerent des regroupements de blocs par argument decideur.
2. Partir des hints comme point de depart, puis lister les blocs du SDB qui seront utilises dans l'onglet Diagnostic.
3. Pour chaque paire de blocs non encore groupee, se demander : "est-ce que ces deux blocs racontent le meme argument au decideur ?" Si oui, les fusionner dans une seule section.
4. Le resultat est une liste d'**arguments distincts**, chacun alimente par 1+ blocs de data.
5. Chaque argument devient 1 section. Pas plus.

Note : les NARRATIVE_HINTS sont des suggestions, pas des contraintes. Pass 2 peut les ignorer ou les recomposer si l'arc narratif le justifie.

**Exemple :** Si le SDB contient SEARCH STATE (200 kw, 75% marque), COMPETITIVE GAP (ratio 1:44, positions Alma vs Oney) et INTENT MARKET MAP (5 500 recherches commerciales non captees), ces 3 blocs racontent le meme argument ("Oney est invisible sur les requetes que les marchands tapent"). Ils deviennent 1 section avec un bar chart + table + KPI cards, pas 3 sections separees.

### Regle de fusion Constat / Benchmark (OBLIGATOIRE)

Si le constat et le benchmark utilisent les memes KPIs (volume de marque, mots-cles, visites, % marque), les fusionner en 1 seule section "Le constat". Le KPI large ouvre, le benchmark prouve. Structure d'une section constat fusionnee :
- KPI large (le chiffre choc)
- Contexte rapide (3 data items inline)
- Bar chart benchmark
- Table comparative (optionnelle si le bar chart suffit)
- 1 seul SO WHAT
- 1 micro-benchmark (si pertinent)

Ne jamais avoir une section "Le constat" + une section "Benchmark concurrentiel" qui repete les memes metriques. Si les metriques different, les deux sections restent distinctes.

### Nombre de sections

Pas de plafond de sections. La deduplication (1 argument = 1 section) est le seul garde-fou.
- Si le diagnostic justifie 12 sections, il y a 12 sections. Si 4 suffisent, 4.
- Chaque section doit apporter un **nouvel argument**. Si elle reformule un argument deja presente, elle n'existe pas — les donnees sont integrees dans la section existante.

---

## Etape 2.2b : Regles de titrage

Les titres de section sont la colonne vertebrale narrative. Le prospect scrolle et lit les titres avant de lire le contenu. Si les titres ne racontent pas l'histoire, la proposition echoue.

### Integration du contexte deal

Si le deal a un contexte specifique (AO, co-traitance, canal partenaire), l'arc narratif doit le refleter :
- **AO / co-traitance** : la proposition se positionne comme un perimetre precis dans une reponse globale. Pas un consultant isole. Mentionner la coordination dans la reco ou les 90 jours.
- **Canal partenaire** : adapter le ton au fait que le prospect arrive via un intermediaire (pas de cold pitch).
- **Grand groupe** : privilegier la rigueur methodologique, les hypotheses sourcees, le processus structure. Eviter l'emotionnel.

### Le hero porte l'arc narratif

Le `hero-subtitle` est la premiere phrase que le prospect lit apres le nom de son entreprise. Il DOIT poser l'arc narratif choisi a l'Etape 2.2, pas le resumer en jargon marketing.

**Regle du subtitle : teaser, pas data.**
- Le subtitle cree une **tension** (paradoxe, contraste, question implicite). Il ne la resout pas.
- **Pas de chiffres dans le subtitle.** Les donnees arrivent dans la premiere section du body ou elles sont contextualisees et sourcees.
- **Max 80 caracteres** (1 phrase courte ou 2 tres courtes). Au-dela, c'est un paragraphe, pas un teaser.
- Le subtitle doit etre **factuellement defendable** par l'evidence log — pas de superlatifs inverifiables ("le plus X de France" sans preuve comparative).

| A eviter | Pourquoi | A faire |
|----------|----------|---------|
| "Transformer votre visibilite Search" | Jargon generique | "Tout le monde vous cherche. Presque personne n'achete." |
| "14 800 recherches/mois, position 3 sur 40 500 requetes..." | Trop long, data dans le hero | "La demande existe. Le site ne la capte pas." |
| "La marque la plus recherchee du biscuit francais" | Superlatif inverifiable | "Vos concurrents captent le trafic que votre site ne voit pas." |
| "Strategie d'acquisition organique sur-mesure" | Pourrait etre n'importe qui | "4 200 recherches/jour sur votre metier. 0 mene a votre site." |

Le hero-subtitle echoue si :
- Il pourrait s'appliquer a n'importe quel prospect (test de substitution)
- Il contient des chiffres detailles (qui appartiennent au body)
- Il depasse 80 caracteres
- Il contient un superlatif non sourcable

### Chaque titre de section passe le test "1 lecture"

Un titre doit etre compris en 1 lecture. Regles :

1. **Fait, pas jugement** — le titre est une donnee ou un fait, jamais une interpretation. "14 800 recherches/mois sur votre marque. 0 client acquis via le Search generique." (fait) vs "Votre marque est connue. Mais votre site est invisible." (jugement). Le fait est incontestable, le jugement est discutable.
2. **Pas de double negation** — "qui capte le trafic que vous ne captez pas" → "La Trinitaine capte 75 000 recherches/mois. Pas vous."
3. **Pas de structure passive** — "Les territoires que la refonte peut ouvrir" → "4 territoires a capter des la refonte"
4. **Privilegier le chiffre ou le nom propre** — un titre avec "75 000" ou "La Trinitaine" est plus concret qu'un titre generique
5. **Privilegier la consequence** — "Sans action, la refonte ne changera rien" plutot que "Ce que cela implique"
6. **Maximum 12 mots** — au-dela, c'est une phrase, pas un titre

### En scrollant les titres seuls, l'arc narratif est lisible

Test : extraire uniquement les h2 de l'onglet Diagnostic et les lire dans l'ordre. Ils doivent raconter une histoire coherente, meme sans le contenu des sections.

---

## Etape 2.3 : Planifier les 3 onglets MVP

La proposition HTML a toujours **3 onglets**. Aucun n'est optionnel.

```
Onglet 1 : Diagnostic — "Voici votre situation"
Onglet 2 : Strategie — "Voici ce qu'on recommande"
Onglet 3 : Investissement — "Voici ce que ca coute"
```

### Onglet 1 : Diagnostic ("Voici votre situation")

C'est l'onglet principal. Il contient :
- Le **hero** (full screen, contexte client tisse : pas juste le nom, mais le contexte business : AO, refonte, objectif CA, etc.)
- Les **sections libres** du diagnostic : constat, benchmark, territoires, S7, deferred, implications
- Les **cas clients inline** (micro-benchmarks integres dans les sections pertinentes)
- Un **SO WHAT obligatoire** sur chaque section (highlight box avec impact business chiffre)

**Contexte client tisse :** le hero et la premiere section prouvent que le diagnostic est personnalise. Le hero-subtitle tisse le contexte business (AO, refonte, objectif, etc.). La premiere section ouvre sur une donnee que le prospect ne connaissait pas SUR LUI.

**Les anciens onglets conditionnels (SEO, GEO/IA, SEA, Social, Tech/UX) deviennent des SECTIONS dans l'onglet Diagnostic** quand les donnees le justifient. Un deal avec des donnees GEO aura une section "Visibilite IA" dans l'onglet Diagnostic, pas un onglet separe.

**Pas de section "Pourquoi SLASHR" standalone.** Les differenciateurs sont tisses apres chaque bloc de donnees, en enchainage naturel (cf. Etape 2.4).

**Regle de placement des metriques Search :**
- **Onglet Diagnostic (benchmark)** : utiliser le trafic organique (visites/mois) + split marque/hors-marque. C'est le diagnostic. Le decideur comprend un gap en volume.
- **Section ROI (onglet Strategie)** : utiliser l'ETV (Estimated Traffic Value) comme "equivalent budget Google Ads". Ca valorise le SEO vs le paid et pose l'argument SEA. Formuler : "La Trinitaine genere l'equivalent de X EUR/mois en achat publicitaire grace a son SEO."
- **Ne jamais afficher l'ETV dans le benchmark** — c'est une metrique d'analyste, pas de decideur. Le prospect comprend "8 000 visites/mois", pas "27 658 EUR d'ETV".

**SO WHAT obligatoire :** chaque section de l'onglet Diagnostic se termine par un highlight box qui traduit les donnees en impact business chiffre, specifique au prospect. Un bar chart sans interpretation est un dashboard, pas une proposition.

**Micro-benchmark inline :** apres chaque section diagnostic ou un cas client est pertinent, inserer un composant micro-benchmark :
- Format : {Prospect} : {metrique} → {Cas} (avant) : {metrique} → {Cas} (apres) : {metrique}
- Source : SDB > CAS CLIENTS RETENUS > sdb_juxtaposition
- Maximum 2-3 micro-benchmarks dans l'onglet, places la ou ils renforcent le plus l'argument

#### Section S7 "Lecture strategique" (obligatoire dans l'onglet Diagnostic)

Bloc compact qui traduit le diagnostic S7 interne en lecture C-level. Place apres le diagnostic et avant les implications dans l'arc narratif.

**Contenu :**
1. **Radar 7 forces** : visualisation SVG/canvas des 7 scores (0-5). Pas de legende longue : le nom de chaque force + son score suffit.
2. **Contrainte principale** : 1 highlight box qui nomme la force limitante et son implication business en 1-2 phrases.
3. **Leviers prioritaires** : 1-2 forces secondaires activees, avec l'impact attendu chiffre.
4. **Insight central** : 1 phrase de synthese strategique, non generique (doit echouer au test de substitution).

**Regles :**
- **Ne jamais recommander de travailler les 7 forces.** Le S7 sert a prioriser, pas a tout faire. Si les 7 forces sont affichees dans le radar, seules 2-3 sont mises en avant comme leviers d'action.
- Les forces non priorisees ne sont pas cachees, elles sont visibles dans le radar mais **pas commentees** (le prospect voit le score, pas une recommandation dessus).
- Le texte est C-level : phrases courtes, chiffres, zero jargon SEO non traduit.
- Le bloc reste **compact** : pas plus de 1 radar + 1 highlight box + 2-3 lignes de leviers + 1 phrase d'insight.

#### Composant "Territoires de contenu" (donnees Intent Market Map)

Bloc de presentation des donnees issues du Module 4b (Intent Market Map). Ce n'est pas une section autonome — c'est un **composant visuel** que l'etape de deduplication peut integrer dans n'importe quelle section de l'onglet Diagnostic (constat, benchmark, recommandation).

**Contenu du composant :**
1. **Segmentation du marche** : 1 visualisation (donut chart ou KPI cards) montrant la repartition Commercial / Informationnel captable / (Informationnel non-captable omis). Montrer les volumes.
2. **Territoire commercial** : les requetes d'achat que le prospect ne capte pas (pages categorie, produit). Composant : cards ou table avec keywords + volumes.
3. **Territoire informationnel** : pourquoi ces requetes comptent, meme si l'intent n'est pas d'achat. 1 highlight box qui explique le pont specifique a ce prospect. Composant : cards avec le mecanisme (contenu → CTA → conversion).
4. **SO WHAT** : highlight box qui lie les territoires a la recommandation.

**Regles :**
- Ne pas presenter le volume brut total sans segmentation. Dire "75 000 recherches/mois" sans preciser que 63 000 sont des recettes est trompeur.
- Toujours expliquer POURQUOI le territoire informationnel est captable pour CE prospect (legitimite de marque, fabricant, expert).
- **Ne PAS utiliser ce composant** si la marque n'a pas de legitimite sur le contenu informationnel (ex: revendeur generique, marketplace).
- Ce composant est **soumis a la deduplication** (Etape 2.3) : s'il repete un argument deja couvert par une autre section, il est fusionne dans cette section, pas affiche en doublon.

### Onglet 2 : Strategie ("Voici ce qu'on recommande")

Header compact (pas de hero full-screen). L'onglet ouvre directement sur la decision strategique.

**Regle de deduplication tab-header vs highlight-gradient :**
Le tab-header de l'onglet Strategie donne le TITRE de la recommandation (phrase courte, max 8 mots, ex: "Integrer le SEO dans la refonte").
Le highlight-gradient "Nous recommandons" DEVELOPPE cette recommandation avec les donnees cles (chiffres du gap, contrainte S7, objectif).
Les deux NE DOIVENT PAS etre la meme phrase.

- **Decision strategique** ("Nous recommandons...") : OUVRE l'onglet au lieu d'etre enterree en fin de scroll
- **90 jours** (M1/M2/M3) : plan d'action immediat
- **ROI Simulateur** : hypotheses sourcees + sliders + scenarios (absorbe l'ex-onglet ROI Interactif)
  - **Hypotheses pre-remplies** avec les donnees reelles du SDB (trafic actuel, multiplicateur source du gap, CVR, panier moyen)
  - **Source de chaque hypothese** visible (pas de chiffres sans provenance)
  - **Chaine de calcul visible** : H1 x H2 x H3 = resultat. Chaque hypothese affiche son niveau de confiance.
  - **Intervalle ROI** : borne basse (conservatrice) par defaut, borne haute via simulateur. Le chiffre unique est interdit.
  - **Simulateur interactif** (sliders) : recalcul en temps reel
  - **3 scenarios calcules** alignes sur Essentiel / Performance / Croissance
  - **Methodologie** : explication en 1-2 phrases de la logique de calcul
- **CTA intermediaire leger** (lien texte, pas full-width)

**Regle Confidence ROI :** si le SDB indique `Confidence globale: Low` ou si 2+ hypotheses ROI sont tagees `Low`, la section ROI DOIT afficher "Hypotheses a confirmer en Phase 1" sous le simulateur, et la carte `.recommended` de l'onglet Investissement recoit le label "Recommandation conditionnelle".

### Onglet 3 : Investissement ("Voici ce que ca coute")

**Spec complete : `agents/prepare-pass2-onglet4.md`.**

Header compact (pas de hero full-screen). Contient : resume decisionnel (6 bullets), board-ready A4, pricing cards Phase 1/Phase 2 avec pont S7, sous-bloc unique "cout de l'inaction", methode S7, FAQ accordion, prochaine etape, CTA final.

---

## Etape 2.4 : Pas de transitions SLASHR

Pas de transitions SLASHR. Le SO WHAT de chaque section suffit comme conclusion.
Si une section mene naturellement a la suivante, le lien est dans le titre H2
de la section suivante (ex: "La refonte est un moment de bascule" enchaine
logiquement apres le benchmark concurrentiel).
La proposition ne doit jamais mentionner SLASHR ou ses services dans
l'onglet Diagnostic, sauf dans la section S7 (methode d'analyse).

**Regles :**
- Pas de phrase de transition entre un bloc de donnees et l'expertise SLASHR
- Pas de "Pourquoi nous", "Nos avantages", "Notre methode", "C'est exactement ce que..."
- Pas de pattern "Notre {X} :" (lecture, conviction, position, approche). C'est un marqueur d'auto-promotion.
- Les donnees parlent d'elles-memes. Le decideur detecte l'auto-promotion.

---

## Etape 2.5 : Tests de validation pre-generation

> **Regles completes : `context/validation_rules.md`**. Appliquer Layer 3 (semantic) + Layer 2 regles 22-25 comme checklist avant de passer a Pass 3.
> Rappel : test de substitution, zero pression, zero dramatisation (cf. `agents/shared.md`, regles 13-15).

### Checklist pre-Pass 3 (obligatoire)

**Anti-generique :**
- [ ] Chaque titre contient le nom du prospect OU un element specifique
- [ ] Donnees = chiffres reels, pas de formule passe-partout
- [ ] Aucune phrase ne marcherait pour un autre prospect (test de substitution)
- [ ] Le hook est un FAIT (chiffre/verbatim/gap), pas une opinion
- [ ] Hero-subtitle : teaser sans chiffres, max 80 chars, factuellement defendable
- [ ] Cascade narrative : subtitle (QUOI) → h2 section 1 (POURQUOI) → KPIs (PREUVE), 3 couches = 3 choses differentes

**Structure narrative :**
- [ ] Sequence S7 → Implications → Decision → 90 jours complete et dans cet ordre
- [ ] "Ce que cela implique" : 3 bullets max, consequences strategiques, pas de chiffrage cout inaction
- [ ] "Decision strategique recommandee" : phrase affirmative avec "Nous recommandons"
- [ ] "90 jours" : 3 etapes max alignees sur PRIMARY
- [ ] Deduplication verifiee : aucune section ne reformule un argument precedent
- [ ] Test des h2 : les titres de l'onglet Diagnostic dans l'ordre = une histoire coherente
- [ ] SO WHAT : chaque section Diagnostic a un highlight box avec impact business chiffre

**Tonalite :**
- [ ] Zero pression commerciale (inclut structures anaphoriques "chaque mois/jour sans")
- [ ] Zero dramatisation
- [ ] Zero auto-promotion deguisee (pas de "Notre {X} :", pas de "C'est exactement ce que")
- [ ] Zero transition SLASHR dans l'onglet Diagnostic (sauf section S7)
- [ ] Chaque expertise traduite en impact business (pas de jargon brut)

---

## Output Pass 2 : Narrative Blueprint (NBP)

L'agent DOIT ecrire explicitement ce document interne avant de passer a la Pass 3.

```
=== NARRATIVE BLUEPRINT ===

ARC GLOBAL: {type d'arc choisi}, {justification en 1 ligne liee au decideur et au contexte}
HOOK: {description du hook et pourquoi il est frappant pour ce prospect}
HOOK_TYPE: {gap_concurrentiel | verbatim | inaction | paradoxe | opportunite | ancrage_identitaire}
LAYOUT_MODE: {data-heavy | narrative-heavy | visual-heavy}
  - data-heavy (defaut) : benchmark + tables + charts. Pour les deals avec beaucoup de donnees comparatives.
  - narrative-heavy : plus de texte, moins de composants data. Pour les deals qualitatifs (marque forte, peu de concurrents mesurables).
  - visual-heavy : plus de charts, donuts, before/after. Pour les deals ou la transformation visuelle est l'argument principal.
PROFIL DECIDEUR: {type}, sensible a: {preoccupation principale}
DECISION MODE: {Rapide | Comite | AO}, risque principal: {budget | timing | politique interne | multi-interlocuteurs}
ADAPTATION AU PROFIL DECIDEUR :
- DG : parler allocation capital, dependance paid, part de marche
- CMO : parler mix canal, brand vs generic, efficience media
- Head of E-commerce : parler conversion, panier, ROAS implicite
- Responsable SEO : parler architecture, intent, couverture cluster

DEDUPLICATION (obligatoire — documenter AVANT de creer les sections) :
Blocs SDB utilises: {liste des blocs du SDB mobilises}
Regroupement par argument:
- Argument 1 "{nom}": blocs {A, B, C} → 1 section
- Argument 2 "{nom}": blocs {D} → 1 section
- Argument 3 "{nom}": blocs {E, F} → 1 section
- ...
Total sections Diagnostic: {N} (pas de plafond, deduplication seul garde-fou)

--- ONGLET DIAGNOSTIC ---

1. {Titre section} · role: {accroche / diagnostic / enjeu / opportunite / ...}
   Angle: {description en 1-2 phrases de ce que cette section dit}
   Donnees utilisees: {quelles donnees du SDB alimentent cette section}
   SO WHAT: {highlight box : impact business chiffre pour ce prospect}
   Cas client inline: {si pertinent : Prospect: metrique → Cas (avant): metrique → Cas (apres): metrique}
   Pourquoi ici: {justification de sa position dans l'arc}

2. {Titre section} · role: {...]
   ...

X. Section S7 "Lecture strategique" · role: priorisation / conviction
   Radar: {7 forces avec scores}
   Contrainte principale: {force + implication business}
   Leviers: {2-3 forces priorisees + impact chiffre}
   Insight: {1 phrase non generique}
   Pourquoi ici: {apres le diagnostic, avant les implications, c'est le pont}

X+0.5. Section "Ce que nous ne priorisons pas (maintenant)" · role: transparence strategique (OBLIGATOIRE)
   3 bullets maximum, issus des DEFERRED du strategy_plan_internal.md.
   Chaque bullet :
   - Nom du levier differe
   - Pourquoi il est differe (justification logique uniquement, liee au diagnostic)
   - A quel moment il deviendra pertinent (condition ou horizon)
   Regles :
   - Ton strategique, pas defensif. C'est un choix d'expert, pas une excuse.
   - Pas de justification budget ("c'est trop cher" interdit). Justification logique uniquement ("tant que S3 n'est pas traite, S6 n'a pas de contenu a diffuser").
   - Le prospect doit comprendre que ne PAS faire quelque chose est une decision autant que faire quelque chose.
   Pourquoi ici: {juste apres le S7, avant les implications — le decideur voit qu'on a arbitre, pas ignore}

X+1. Section "Ce que cela implique" · role: verrou narratif decisionnel (OBLIGATOIRE)
   **Triplet structure obligatoire** — exactement 3 bullets, chacun avec un role distinct :

   | # | Role | Contenu | Source SDB |
   |---|------|---------|-----------|
   | 1 | **Verrou systemique** | La contrainte PRIMARY et ce qu'elle bloque concretement. Factuel, C-level. | S7 SYNTHESIS > Primary constraint + Systemic limitation |
   | 2 | **Actif inexploite** | Ce qui est DEJA en place chez le prospect et qui n'est pas utilise. Ton positif : le prospect a des atouts. | SDB > SEARCH_STATE forces, GREEN FLAGS, ou donnee specifique |
   | 3 | **Fenetre temporelle** | Projection chiffree issue du S7. Le delta mesurable si rien ne change. | SDB > S7 SYNTHESIS > Projection PRIMARY (obligatoire) |

   Ton: factuel et affirmatif, zero jargon technique
   INTERDIT dans cette section :
   - Structure anaphorique ("Chaque mois..." x3) = effet marteau = pression commerciale
   - Repetition du meme leitmotiv dans les 3 bullets (ex: "sans contenu" x3)
   - Ton alarmiste ou dramatique. Les donnees suffisent.
   - Chiffrer le "cout de l'inaction" en euros : c'est dans le sous-bloc Investissement (onglet 3), pas ici
   - Inventer une projection que Pass 1 n'a pas calculee. Le bullet 3 utilise UNIQUEMENT la Projection PRIMARY du SDB.
   Pourquoi ici: {le prospect a compris le diagnostic, maintenant il doit voir les implications}

OBJECTIONS A PRE-EMPT (max 4, reponses data-first, 2 phrases chacune) :
1) {objection probable} → {reponse courte + preuve (source/data/verbatim)}
2) {objection probable} → {reponse courte + preuve}
3) {objection probable} → {reponse courte + preuve}
4) {objection probable} → {reponse courte + preuve}
Regles :
- Objections typiques : budget, timing, "contenu = SEO 2020", dependance dev, "on a deja une agence", ROI incertain.
- Reponses : jamais defensives, jamais aggressives. Toujours "les donnees montrent..." + "Phase 1 confirme".

--- ONGLET STRATEGIE ---

1. Section "Decision strategique recommandee" · role: declencheur de decision (OUVRE l'onglet)
   Titre: "Decision strategique recommandee" (avec emoji cible)
   1 phrase tranchee, affirmative, non conditionnelle, non vague
   Liee explicitement a la contrainte S7 PRIMARY
   Format: "Nous recommandons de [action] car [raison liee au S7]."
   REGLE DE PRECISION STRATEGIQUE :
   Les termes suivants sont autorises : visibilite, SEO, trafic, notoriete.
   MAIS ils ne doivent jamais apparaitre seuls ou comme objectif final.
   Chaque occurrence doit etre :
   - Qualifiee par un impact business (CA, part de marche, dependance paid, efficience media, etc.)
   - OU associee a une metrique concrete (hors-marque, intent commercial, segment cible, saisonnalite, etc.)
   Exemples acceptables :
   - "Augmenter la part de trafic hors-marque sur les requetes commerciales"
   - "Reduire la dependance au paid via un actif SEO durable"
   - "Transformer la notoriete en captation Search mesurable"
   Exemples interdits :
   - "Ameliorer la visibilite"
   - "Optimiser le SEO"
   - "Augmenter le trafic"
   - "Gagner en notoriete"
   Regle : tout objectif formule doit repondre implicitement a la question "pourquoi business ?"

2. Sous-bloc "Ce que cela signifie concretement (90 jours)" · role: projection immediate
   3 etapes max alignees strictement sur la contrainte S7 PRIMARY
   Pas de liste generique, seulement ce qui decoule du diagnostic
   Chaque etape = action concrete + livrable ou KPI attendu

3. ROI Simulateur · role: quantification de l'impact
   Chaine de calcul (visible dans le simulateur) :
     H1: Trafic actuel = {X} visites/mois [Confidence: {H/M/L}] (source: DataForSEO)
     H2: Visites cibles M12 = {Y_bas} - {Y_haut} visites/mois [Confidence: {H/M/L}] (source: gap analysis)
     H3: CVR = {W_bas}% - {W_haut}% [Confidence: {H/M/L}] (source: {benchmark / prospect})
     H4: Panier moyen = {V} EUR [Confidence: {H/M/L}] (source: {prospect})
     → Resultat : H2 x H3 x H4 = {CA_bas} - {CA_haut} EUR/an additionnel
     → ROI intervalle : x{N_bas} - x{N_haut}
     → ROI affiche (defaut) : x{N_bas} (borne basse conservatrice)
   3 scenarios: Essentiel ({prix}) / Performance ({prix}) / Croissance ({prix})

4. CTA intermediaire leger (lien texte, pas full-width)
   Interdit : "Planifier un echange", "Discuter", "Echanger", "En savoir plus"
   Obligatoire : CTA oriente decision, lie a la trajectoire 90 jours
   Exemples : "Demarrer la Phase 1", "Valider le lancement Phase 1"

--- ONGLET INVESTISSEMENT ---

Structure complete : voir `agents/prepare-pass2-onglet4.md`
Scenario recommande: {lequel et pourquoi}

=== FIN NBP ===
```
