# PASS 2 : NARRATIVE ARCHITECT

## Role

---

## TONE_PROFILE (modulable au Checkpoint 1)

Le SDB contient un champ `TONE_PROFILE` que le closer peut ajuster au Checkpoint 1.

| Profil | Description | Quand l'utiliser |
|--------|-------------|-----------------|
| **DIRECT** (defaut) | Factuel, pas de detour. Les donnees parlent. | Decideur C-level, deals simples |
| **PEDAGOGIQUE** | Explique le "pourquoi" derriere chaque constat. | Prospect decouvrant le SEO, operationnel qui doit convaincre son N+1 |
| **PROVOCATEUR** | Pose des questions, challenge les certitudes. | Prospect qui pense que "ca va bien" malgre les donnees |
| **TECHNIQUE** | Detail les mecanismes, vocabulaire expert (traduit). | CTO, Head of Digital, equipe tech |

Le TONE_PROFILE influence :
- Le vocabulaire (plus ou moins technique)
- La longueur des explications (court vs pedagogique)
- L'angle du SO WHAT (impact business vs mecanisme technique)
- Les questions de la FAQ

Le TONE_PROFILE N'influence PAS :
- Les regles absolues (zero pression, evidence chain, accents, lexique interdit)
- Le contenu strategique (memes conclusions, meme diagnostic)
- Le pricing (memes formules)

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

### Regles narratives (issues des reviews closer)

**Brand budget :** ne jamais recommander de couper une campagne qui a le meilleur CPA du compte. Si le brand performe bien (CPA bas, ratio budget/total < 5%), le dire : "rien a changer". Ca montre du pragmatisme.

**PMax :** toujours mentionner le risque de cannibalisation marque/Search. Ne pas presenter PMax comme "meilleur performer" sans nuancer. Recommander l'audit de cannibalisation avant reallocation.

**ROI :** ne pas diviser budget par CPA cible pour calculer les gains. Verifier que le CPA cible est realiste a l'echelle (PMax ne scale pas lineairement). Projections conservatrices, jamais optimistes.

**International :** ne jamais exclure un perimetre important pour le client. Prioriser ≠ exclure. Si le client opere a l'international, montrer qu'on le comprend (slide vue internationale) et expliquer pourquoi on priorise un marche, pas pourquoi on ignore les autres.

**Prestataires existants :** verifier le contexte concurrentiel avant de nommer un prestataire comme "partenaire" dans l'ecosysteme. Si on challenge l'agence en place, ne pas la nommer comme partenaire. Le diagnostic fait le travail.

**Landing pages / conversion :** toujours inclure les recommandations landing pages et parcours de conversion dans le scope SEO et SEA. C'est un levier systematiquement oublie.

**Reglementation sectorielle :** si le secteur est sensible (sante, addiction, finance, etc.), verifier la politique Google Ads. Ajouter un slide reglementation si risque de non-conformite.

**Cas clients :** l'onglet est optionnel. Le closer decide au Checkpoint 2.

Prendre le SDB et construire le plan narratif complet. Choisir l'angle, l'arc emotionnel, la sequence des sections pour chacun des **5-6 onglets** (Diagnostic, Strategie, Projet, Investissement, Cas clients + Contexte conditionnel). Decider du contenu textuel de chaque section (titres, angles, arguments). **NE PAS choisir de composants visuels, c'est le role de la Pass 3.**

### Champs SDB enrichis (consommes par Pass 2)

- `DECIDEUR_LEVEL` : adapter le ton (DECIDEUR → decision directe, INFLUENCEUR → board-ready A4 crucial, OPERATIONNEL → passage par le N+1)
- `PERIMETRE_SLASHR` : cadrer la recommandation (ne pas recommander hors perimetre)
- `REFONTE` : si refonte, les 3 actes (Securiser/Transformer/Accelerer) sont dans l'onglet Diagnostic
- `MODULES_ACTIFS` : savoir quels blocs de donnees sont disponibles dans le SDB
- `SEA_SIGNAL` : routage paid (EXPLICIT / DETECTED / ABSENT) — determine les sections conditionnelles SEA
- `SEA_POSTURE` : posture SLASHR vis-a-vis du paid (PILOTE / CONSEIL / HORS_PERIMETRE)
- `SEA_BRIEF_REQUESTS` : liste des demandes paid du prospect (verbatim brief)
- `NARRATIVE_HINTS` : point de depart pour l'etape de deduplication (non-contraignant)
- (champ `TRANSITION_OPPORTUNITIES` supprime du SDB, cf. Etape 2.4)
- `ROI Confidence globale` : determine si le label "Recommandation conditionnelle" est necessaire
- `CAS CLIENTS RETENUS` enrichis : `match_criteria`, `key_metric`, `sdb_juxtaposition`, `angle` par cas
- `BENCHMARK_SYNTHESIS` : gap principal, concurrents cles, opportunites, insight benchmark — **colonne vertebrale du storytelling**
- `COMPETITIVE_ADS` : paysage concurrentiel paid (si Google Ads disponible)
- `CLOSER_INPUT` (nouveau) : input du closer au Checkpoint 1
  - `CLOSER_ANGLE` : ce que le prospect attend → **oriente le choix du hook et de l'arc narratif**. Si le closer dit "il veut du ROI chiffre", l'arc doit ouvrir par les chiffres, pas par la marque. Si "il veut etre rassure sur la methode", l'onglet Projet prend plus de poids.
  - `CLOSER_INSIGHTS` : contexte hors-data → **enrichit les verbatims et le TONE_CONTEXT**. "Nouveau DG qui pousse le digital" change le framing (opportunite, pas menace).
  - `CLOSER_RED_FLAGS` : risques non detectes → **integres dans les objections FAQ et dans le pricing**. "Il compare avec 2 agences" → FAQ "Pourquoi SLASHR plutot qu'une autre agence" ou angles differenciateurs tisses plus fort.
- `SIGNALS` (si analyst-signals active) : sentiment, objections detectees, concurrence SLASHR → **calibre le ton et les objections FAQ**

### Le benchmark comme colonne vertebrale narrative

Le `BENCHMARK_SYNTHESIS` du SDB n'est pas une section parmi d'autres. C'est le fil rouge du diagnostic. Chaque slide du diagnostic devrait repondre a la question : "ou en est le prospect par rapport a ses concurrents sur CE point ?"

- Le hook d'ouverture vient souvent de l'INSIGHT BENCHMARK ("Laserostop domine les local packs de toutes vos villes")
- Chaque constat est contextualize par la concurrence ("votre CPA France est 25,5 EUR, la Belgique est a 14,8 EUR")
- Le "et alors ?" de chaque slide relie le constat a la position concurrentielle
- La strategie est une reponse a la position concurrentielle, pas une liste de best practices

**Si le benchmark est pauvre** (pas assez de donnees DataForSEO, niche sans concurrent identifiable) :
- Fallback 1 : utiliser les donnees GSC (top queries, positions) comme proxy de positionnement
- Fallback 2 : utiliser les SERPs manuelles (3-5 requetes commerciales) pour identifier qui domine
- Fallback 3 : contextualiser par le secteur ("dans votre secteur, les acteurs qui performent font X, vous faites Y")
- Ne jamais skipper le benchmark. Degrader gracieusement, mais toujours positionner le prospect par rapport a quelque chose.

---

## Etape 2.1 : Choisir le hook

**Objectif :** trouver l'information la plus frappante pour CE prospect. C'est ce qui ouvre apres le hero dans l'onglet Diagnostic.

**L'IA invente le hook.** Pas de liste limitative. Le hook doit etre impossible a deviner sans avoir lu les donnees du deal. Si on peut le remplacer par n'importe quel autre prospect, c'est un mauvais hook.

### Cascade narrative ouverture (OBLIGATOIRE)

L'ouverture suit une cascade en 3 couches. Chaque couche avance le recit, aucune ne repete la precedente.

| Couche | Role | Contrainte |
|--------|------|------------|
| Hero subtitle | **QUOI** — la tension | Max 80 chars, teaser pur, sans data |
| H2 section 1 | **POURQUOI** — le mecanisme | Max 12 mots, 1 fait cle |
| KPIs section 1 | **PREUVE** — les donnees | 3-4 data points, tous sources |

**Test de non-repetition** : lire les 3 couches a la suite. Si deux couches disent la meme chose avec des mots differents, reecrire.

**Exemple :**
- Subtitle : "Tout le monde vous cherche. Presque personne n'achete." (tension)
- H2 : "80% de votre trafic cherche votre nom. Pas vos produits." (mecanisme : dependance brandee)
- KPIs : 14 800 recherches brandees · 319 kw indexes · 55 745 EUR CA web (preuves)

---

## Etape 2.1b : Section contexte (OBLIGATOIRE, avant toute section data)

Apres le hero et avant la premiere section data du diagnostic, la proposition DOIT inclure une section de reformulation du besoin client. Cette section prouve au decideur qu'on a compris sa situation AVANT de diagnostiquer.

**Section : "Votre situation en un coup d'oeil"**
- Section-label : "Ce que nous avons compris"
- Layout : grid-2 (4 blocs compacts)

| Bloc | Contenu | Source SDB |
|------|---------|-----------|
| **L'objectif** | Chiffre cible ou ambition du prospect (verbatim si possible) | PAIN_POINTS, verbatims |
| **Le contexte** | Evenement declencheur (AO, refonte, recrutement, saison, budget) | PROSPECT_PROFILE, trigger |
| **La question** | Verbatim prospect : la vraie question posee en R1 | TONE_CONTEXT, verbatims |
| **L'approche** | 1 phrase methode adaptee au deal (test & learn, data-first, cadrage refonte, etc.) | diagnostic contrainte principale |

**Regles :**
- Chaque bloc = 2-3 lignes max. C'est un rappel, pas une analyse.
- Le verbatim "La question" doit etre une citation EXACTE (entre guillemets) ou une reformulation proche si aucun verbatim exact n'est disponible.
- Cette section n'a PAS de SO WHAT (c'est un cadrage, pas un argument).
- Si le SDB ne contient pas assez de verbatims pour les 4 blocs, adapter : 3 blocs minimum, 2 blocs si vraiment pauvre en contexte qualitatif.

**NBP :** ajouter cette section comme Section 0 dans la structure de l'onglet Diagnostic, avant les sections data.

---

## Etape 2.2 : Construire l'arc narratif du Diagnostic

**Objectif :** emmener ce decideur du constat a la conviction, avec ces donnees, dans ce contexte.

L'onglet Diagnostic est une **sequence de sections libres**. L'IA cree les sections qu'elle veut, dans l'ordre qu'elle veut. Il n'y a pas de liste fixe de sections ni d'arcs predetermines.

**Contraintes :**
- Max 5 slides (hors hero et CTA)
- Alternance data / interpretation (pas 2 blocs data consecutifs sans SO WHAT)
- Chaque section a un SO WHAT (highlight-box) qui traduit la donnee en impact business
- Le diagnostic se termine par les priorites strategiques (contrainte + leviers) en langage business

**Inspiration :** des exemples d'arcs narratifs sont dans `context/references/arcs-narratifs.md`. Ce sont des inspirations, pas des templates a suivre.

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

### Regle de fusion Benchmark / Opportunite commerciale (OBLIGATOIRE)

Si le benchmark (positions concurrentes par requete) et l'opportunite commerciale (volumes de recherche par requete) portent sur les MEMES requetes, les fusionner en 1 seule section. Un tableau unique combine volumes + positions + leader. Structure :
- Tableau : requete | vol/mois | position Delcourt | leader | position leader
- Stat row : total recherches/mois, requetes top 10, recherches hors top 10
- 1 seul SO WHAT qui chiffre le gap

Ne jamais avoir une section "Benchmark" + une section "Opportunite commerciale" qui listent les memes requetes sous deux angles differents. Pour le decideur, c'est le meme argument : "on est mal positionne sur les requetes qui comptent".

### Regle de densite : 1 visuel par slide (OBLIGATOIRE)

Chaque `.slide` contient au maximum **1 composant visuel** (bar chart, donut grid, cards grid, table) + **1 highlight-box** (SO WHAT). Au-dela, decouper en slides supplementaires. Un slide surcharge perd le decideur.

### Regle du constat : CONSTAT_MODE (signal NBP)

Le constat peut prendre 2 formes selon les donnees :

- **`statement`** (defaut) : KPI large + data row + source. Pour les cas ou un seul chiffre suffit a poser le probleme.
- **`tension`** : deux KPIs opposes avec un connecteur ("pourtant", "mais", "et pourtant"). Pour les cas ou le paradoxe EST l'argument (marque forte + invisibilite Search). Structure : KPI positif → connecteur → KPI negatif + preuves (requetes en pills).

Le NBP doit specifier `CONSTAT_MODE` pour que la Pass 3 choisisse le bon composant.

### Section conditionnelle "Recherches de marque" (si BRAND_SLIDE = YES)

**Placement :** apres la section contexte (Section 0), avant le constat. La marque est un actif qui cadre la lecture du diagnostic.

**Angle :** la marque est un **actif** et un **tremplin**, pas un probleme. Le volume de recherche de marque signale une autorite aupres de Google qui facilite le positionnement sur les requetes hors-marque adjacentes.

**Structure :**
- Gauche : volume marque + tableau top 5 requetes marque
- Droite : "Ce que ca signifie pour Google" (explication du tremplin : autorite thematique, confiance, facilite de positionnement hors-marque)

**INTERDIT :**
- Ne pas parler de conversion ou de technique (pages, Schema, alt, formulaires) : c'est traite plus loin dans la proposition
- Ne pas repeter le TASM (la section TASM suit plus bas avec ses propres chiffres)
- Ne pas faire un diagnostic du trafic de marque : c'est une mise en contexte positive

**SO WHAT :** pas de SO WHAT classique. La section se conclut par 1 phrase qui fait le pont vers le constat ("Ce tremplin existe. Reste a construire les pages qui captent le trafic hors-marque.")

### Section conditionnelle "Opportunite Google Shopping" (si SHOPPING_SIGNAL = YES)

**Placement :** apres l'opportunite commerciale.

**Angle :** "vos produits sont deja sur Google Shopping, pas vous" (revendeurs vs marque directe).

**Structure :**
- Constat : les produits apparaissent via des revendeurs (nommer les revendeurs)
- Data : {N} requetes declenchant Google Shopping, % intent commercial, volume
- Levier : Merchant Center + feed produit = presence directe
- Prerequis technique : rattacher a la refonte si applicable. Utiliser "nouveau CMS" ou "refonte e-commerce" tant que le CMS n'est pas confirme (AO = CMS non decide). Ne citer un CMS specifique que s'il est explicitement confirme dans les notes Pipedrive ou par le closer.

**SO WHAT :** highlight-box qui lie Shopping au vehicule technique (refonte) et au CA direct.

### Section conditionnelle "Marches B2B" (si B2B_SLIDE = YES)

**Placement :** apres Google Shopping (si present), sinon apres opportunite commerciale.

**Angle :** structurer ce qui existe deja (pas creer de toutes pieces). Le Search peut capter une demande B2B qui arrive aujourd'hui par des canaux informels (email, telephone).

**Structure :** 1 slide si 1 marche, 1 slide avec 2 colonnes si 2 marches.
- Pour chaque marche : nom + workflow actuel + requetes Search identifiees + lien refonte
- Distinguer les marches transactionnels (CE/CSE) des marches vitrine (B2B Pro)
- Mini-stats si disponibles (ex: "90% des commandes par email", "X recherches/mois")

**SO WHAT :** convergence vers le vehicule technique commun (refonte, architecture de site).

### Regle de l'opportunite : 3+ slides (OBLIGATOIRE si Intent Market Map disponible)

La section Opportunite se decoupe en 3 slides minimum, plus les sections conditionnelles ci-dessus si activees :

1. **Cartographie du marche** (section-label: "Opportunite — cartographie du marche") : donuts (commercial / informationnel / navigationnel) + SO WHAT global. Le decideur voit la taille du marche.
2. **Opportunite commerciale** (section-label: "Opportunite commerciale") : bar chart horizontal, 1 barre par territoire, trie par volume decroissant. Sous chaque barre : 1 ligne de contexte (concurrent leader + position LMP). Highlight-box saisonnalite si pertinent.
3. **Opportunite informationnelle** (section-label: "Opportunite informationnelle") : bar chart horizontal, 1 barre par territoire, trie par volume decroissant. SO WHAT qui lie l'informationnel au commercial.
4. **(conditionnel) Opportunite Google Shopping** : si SHOPPING_SIGNAL = YES (voir ci-dessus)
5. **(conditionnel) Marches B2B** : si B2B_SLIDE = YES (voir ci-dessus)

**Regle data :** chaque territoire doit afficher son volume mensuel (source: DataForSEO). Les volumes sont collectes en Pass 1 via l'endpoint `keywords_data/google_ads/search_volume`. Ne jamais presenter un territoire sans volume.

### Nombre de sections

Max 5 slides (hors hero et CTA). La deduplication (1 argument = 1 section) et cette limite sont les deux garde-fous.
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
6. **Maximum 8 mots** — au-dela, c'est une phrase, pas un titre. Le titre est un argument, pas une description.
7. **Section-intro obligatoire sous les charts** — quand un slide contient un graphique (bar chart, donut, stacked bars), ajouter un `<p class="section-intro">` sous le H2 qui explique ce qui est mesure. Le decideur ne doit jamais se demander "c'est du trafic ? des keywords ?"

### En scrollant les titres seuls, l'arc narratif est lisible

Test : extraire uniquement les h2 de l'onglet Diagnostic et les lire dans l'ordre. Ils doivent raconter une histoire coherente, meme sans le contenu des sections.

---

## Etape 2.3 : Planifier les onglets

La proposition HTML a **5 onglets obligatoires** (Diagnostic, Strategie, Projet, Investissement, Cas clients) + **1 onglet conditionnel** (Contexte, si BRAND_CONTEXT.CONTEXTE_TAB = YES).

```
(conditionnel) Onglet 0 : Contexte — "Votre marque, vos cibles, votre terrain Search"
Onglet 1 : Diagnostic — "Voici votre situation"
Onglet 2 : Strategie — "Voici ce qu'on recommande"
Onglet 3 : Projet — "Comment on travaille ensemble"
Onglet 4 : Investissement — "Voici ce que ca coute"
Onglet 5 : Cas clients — "Resultats observes sur des profils comparables"
```

### Onglet 0 (conditionnel) : Contexte ("Votre marque, vos cibles, votre terrain Search")

**Activer si :** `BRAND_CONTEXT.CONTEXTE_TAB = YES` dans le SDB.

Cet onglet cree un ancrage emotionnel et strategique AVANT le diagnostic chiffre. Il traduit l'ADN de marque et les cibles en opportunites Search. Il ne contient PAS de data DataForSEO : c'est du contexte qualitatif, pas du diagnostic.

**Structure :**
1. **Hero** (tag "Contexte", subtitle qui tisse l'identite de marque dans le constat Search)
2. **Slides ADN de marque** (1 slide par pilier identifie dans BRAND_CONTEXT.Piliers) : chaque pilier est traduit en un territoire de recherche. Format : titre pilier + contexte marque + "en Search, cela signifie..." + requetes typiques (query-pills) + highlight-box opportunite
3. **Slides Personas** (1 slide par persona, B2C puis B2B) : chaque persona est traduit en comportement Search. Format standardise : grid-2 ("Profil & comportement" | "Parcours Search") + highlight-box "Enjeu Search" + query-pills. **Tous les personas utilisent le meme design pattern.**
4. **Slide synthese** : "Avant d'acheter, il faut vous trouver". Resume les cibles (B2C + B2B) et leur constat commun Search. Grid de piliers ADN avec couleurs differenciees + highlight-box gradient qui nomme chaque cible et son comportement Search.
5. **CTA Diagnostic** : bouton qui bascule vers l'onglet Diagnostic ("Voir les donnees")

**Regles :**
- Les piliers de marque proviennent des sources Drive (PPT, charte, brief). L'agent les reformule pour la vision Search, il ne les invente pas.
- Les personas proviennent des sources Drive ou des notes Pipedrive. Si aucun persona n'est documente, l'agent peut proposer des personas types bases sur le secteur + les donnees Search, mais il le signale comme hypothese.
- L'onglet Contexte est positionne A GAUCHE de Diagnostic dans la nav (premier onglet, actif par defaut).
- Le ton est factuel et strategique (pas de flatterie, pas de nostalgie). L'heritage de marque est un fait, pas une emotion.
- **CMS-agnostique :** si REFONTE = OUI et CMS non confirme, utiliser "nouveau site e-commerce" ou "refonte e-commerce".

### Onglet 1 : Diagnostic ("Voici votre situation")

C'est l'onglet principal. Il contient :
- Le **hero** (full screen, contexte client tisse : pas juste le nom, mais le contexte business : AO, refonte, objectif CA, etc.)
- Les **sections libres** du diagnostic : constat, benchmark, territoires, priorites strategiques, ce qu'on ne fait pas, implications
- Un **SO WHAT obligatoire** sur chaque section (highlight box avec impact business chiffre, 3 lignes max)

**Contexte client tisse :** le hero et la premiere section prouvent que le diagnostic est personnalise. Le hero-subtitle tisse le contexte business (AO, refonte, objectif, etc.). La premiere section ouvre sur une donnee que le prospect ne connaissait pas SUR LUI.

**Les anciens onglets conditionnels (SEO, GEO/IA, SEA, Social, Tech/UX) deviennent des SECTIONS dans l'onglet Diagnostic** quand les donnees le justifient. Un deal avec des donnees GEO aura une section "Visibilite IA" dans l'onglet Diagnostic, pas un onglet separe.

#### Section conditionnelle "Visibilite paid" (si SEA_SIGNAL = EXPLICIT)

**Si SEA_SIGNAL = EXPLICIT :** section obligatoire dans l'onglet Diagnostic : "Visibilite paid : etat des lieux"

- **Si le prospect a du paid actif (DETECTED + EXPLICIT) :** audit CPC, keywords payes, deperdition budget vs organique
- **Si zero paid (EXPLICIT sans DETECTED) :** CPC de reference secteur (source DataForSEO), cout acquisition paid vs organique, gap entre intent commercial et absence de couverture paid
- **SO WHAT :** positionnement cabinet conseil vs agence media. Framing obligatoire : "Nous structurons la strategie paid. L'execution quotidienne releve d'une agence media ou de votre equipe, sous notre pilotage strategique."

**Si SEA_SIGNAL = DETECTED :** pas de section dediee. Mention de la synergie SEO/SEA dans la section benchmark ou opportunites (1-2 phrases).

**Si SEA_SIGNAL = OPPORTUNITY :** section legere dans l'onglet Diagnostic montrant l'opportunite paid (terrain vierge, CPCs bas, 0 concurrent en Ads). Pas de section strategie paid dediee, mais :
- Integrer le paid comme axe dans la recommandation (ex: "Activer le paid sur un terrain vierge une fois les fondations posees")
- Integrer le paid dans la trajectoire globale en Phase 2 (pas Phase 1)
- Mentionner les donnees cles (CPCs, couverture concurrents) dans la section diagnostic ou opportunites
- Le ton est "opportunite future" (pas urgence, pas demande client) : "Le terrain paid est vierge. C'est un levier a activer une fois les fondations Search posees."

**Si SEA_SIGNAL = ABSENT :** rien.

**Pas de section "Pourquoi SLASHR" standalone.** Les differenciateurs sont tisses apres chaque bloc de donnees, en enchainage naturel (cf. Etape 2.4).

**Regle de placement des metriques Search :**
- **Onglet Diagnostic (benchmark)** : utiliser le trafic organique (visites/mois) + split marque/hors-marque. C'est le diagnostic. Le decideur comprend un gap en volume.
- **Section ROI (onglet Strategie)** : utiliser l'ETV (Estimated Traffic Value) comme "equivalent budget Google Ads". Ca valorise le SEO vs le paid et pose l'argument SEA. Formuler : "La Trinitaine genere l'equivalent de X EUR/mois en achat publicitaire grace a son SEO."
- **Ne jamais afficher l'ETV dans le benchmark** — c'est une metrique d'analyste, pas de decideur. Le prospect comprend "8 000 visites/mois", pas "27 658 EUR d'ETV".

**SO WHAT obligatoire :** chaque section de l'onglet Diagnostic se termine par un highlight box qui traduit les donnees en impact business chiffre, specifique au prospect. Un bar chart sans interpretation est un dashboard, pas une proposition. **Contrainte : 3 lignes maximum.** Si le SO WHAT depasse 3 lignes, il est trop long — couper le superflu.

**Cas clients : onglet dedie (pas inline).** Les cas clients ne sont plus integres dans le diagnostic. Ils ont leur propre onglet (onglet 4 "Cas clients"). Voir section Onglet 4 ci-dessous.

#### Section "Priorites strategiques" (obligatoire dans l'onglet Diagnostic)

Bloc compact qui traduit les conclusions du diagnostic strategique en lecture business. Place apres le diagnostic et avant les implications dans l'arc narratif. **Le diagnostic en tant que vocabulaire interne (contrainte, leviers, confiance, labels) ne doit JAMAIS apparaitre dans le HTML client.**

**Contenu :**
1. **Contrainte principale** : 1 highlight box qui nomme le blocage en langage business et son implication chiffree en 1-2 phrases. Ex: "Le site ne produit aucun contenu qui attire de nouveaux visiteurs. Sur 2,7M de recherches mensuelles, 96% arrivent chez les concurrents."
2. **Leviers prioritaires** : 2-3 axes d'action concrets, avec l'impact attendu chiffre. Ex: "Creer les pages categories et recettes (objectif : +500 visiteurs/mois en 6 mois)"
3. **Ce qu'on ne fait pas maintenant** : transparence sur ce qui est hors perimetre et pourquoi. Ex: "La presence sur les reseaux sociaux sera activee une fois que le site aura du contenu a diffuser."
4. **Insight central** : 1 phrase de synthese strategique, non generique (doit echouer au test de substitution).

**Regles :**
- **Zero jargon interne** : pas de "contrainte principale", pas de "leviers prioritaires", pas de labels internes, pas de scores.
- **Max 3 axes d'action.** Le prospect ne peut pas tout faire. L'analyse priorise, pas enumere.
- Le texte est C-level : phrases courtes, chiffres, zero jargon SEO non traduit.
- Le bloc reste **compact** : highlight box + 2-3 axes + 1 insight.

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

Hero fullscreen propre a cet onglet (tag "Strategie Search", subtitle = direction strategique). L'onglet ouvre sur le hero, puis la decision strategique.

**Regle de deduplication tab-header vs highlight-gradient :**
Le tab-header de l'onglet Strategie donne le TITRE de la recommandation (phrase courte, max 8 mots, ex: "Integrer le SEO dans la refonte").
Le highlight-gradient "Nous recommandons" DEVELOPPE cette recommandation avec les donnees cles (chiffres du gap, contrainte identifiee dans le diagnostic, objectif).
Les deux NE DOIVENT PAS etre la meme phrase.

#### Slides de l'onglet Strategie (4-5 max)

Chaque slide a un **role unique**. Deux slides ne peuvent pas couvrir le meme sujet sous un angle different.

| # | Slide | Role unique | Contenu |
|---|-------|-------------|---------|
| 1 | **Le plan** | Timeline / projection immediate | Decision strategique ("Nous recommandons...") + timeline contextuelle (Phase 1 M1-M3 + Phase 2 M4+). Le plan est cale sur l'evenement structurant du deal. |
| 2 | **ROI Simulateur** | Quantification de l'impact | Hypotheses sourcees + sliders + calcul JS + scenario recommande. Chaine de calcul visible. |
| 3 | **Trajectoire globale** | Vision chiffree | Synthese des leviers (SEO, SEA si applicable, UX) avec contribution chiffree de chacun. Les donnees paid sont integrees ICI (pas dans une slide separee). |
| 4 | **Comment nous travaillons** | Methode / processus | Phase 1 (livrables) + Phase 2 (cadence). Pas de reprise du contenu timeline. |
| 5 | **(conditionnel) Strategie Paid** | Positionnement paid | Uniquement si SEA_POSTURE = PILOTE ou CONSEIL. Sinon les donnees paid sont integrees dans les slides 1 et 3. |

**ROI Simulateur (details) :**
- **Hypotheses pre-remplies** avec les donnees reelles du SDB (trafic actuel, multiplicateur source du gap, CVR, panier moyen)
- **Source de chaque hypothese** visible (pas de chiffres sans provenance)
- **Chaine de calcul visible** : H1 x H2 x H3 = resultat. Chaque hypothese affiche son niveau de confiance.
- **Intervalle ROI** : borne basse (conservatrice) par defaut, borne haute via simulateur. Le chiffre unique est interdit.
- **Simulateur interactif** (sliders) : recalcul en temps reel
- **1 scenario recommande** avec justification (Pilotage / Production / Acceleration selon le deal)
- **Methodologie** : explication en 1-2 phrases de la logique de calcul

**CTA intermediaire leger** (lien texte en fin d'onglet, pas full-width).

#### Deduplication onglet Strategie (OBLIGATOIRE)

Avant de creer les slides, verifier :
1. Chaque slide a un ROLE UNIQUE (timeline / quantification / vision / methode)
2. Deux slides ne peuvent pas couvrir le meme sujet sous un angle different (ex: "Recommandation 3 axes" + "Plan d'action 3 mois" = doublon si les axes = les mois)
3. Les donnees paid (si SEA_SIGNAL != EXPLICIT) sont integrees DANS les slides existantes (dans la trajectoire, pas dans une slide separee)
4. Maximum 5 slides par onglet (hors hero et CTA)
5. Test : pour chaque paire de slides, se demander "est-ce qu'un decideur dirait que ces 2 slides disent la meme chose ?" Si oui → fusionner.

**Regle Confidence ROI :** si le SDB indique `Confidence globale: Low` ou si 2+ hypotheses ROI sont tagees `Low`, la section ROI DOIT afficher "Hypotheses a confirmer en Phase 1" sous le simulateur, et la carte `.recommended` de l'onglet Investissement recoit le label "Recommandation conditionnelle".

### Onglet 3 : Projet ("Comment on travaille ensemble")

Hero fullscreen propre a cet onglet (tag "Projet", subtitle "Comment on travaille ensemble.").

**Structure : 5 slides obligatoires**

#### Slide 1 : Votre equipe
- **Titre court** : ex "Une seule personne a appeler"
- **Bloc chef de projet** (highlight-box avec logo SLASHR `<img>`, pas un cercle texte) :
  - Label : "Votre chef de projet" (JAMAIS "Account Manager")
  - Sous-titre percutant : ex "Un profil senior, pas un junior qui apprend sur votre budget"
  - Description : pilote le projet, produit les livrables, assure le reporting. Un seul interlocuteur.
  - Ne PAS mentionner SEA/GEO si hors perimetre du deal
- **3 fondateurs en appui** (grid-3, cards centrees avec initiales colorees) :
  - Anthony L. / Strategie : definit les priorites, valide les choix strategiques
  - Quentin C. / Business : garant des interets business du client
  - Benoit D. / Technique : garant de l'expertise et de la qualite des livrables
  - NE PAS inventer d'anciennete ou de chiffres non verifies

#### Slide 2 : Notre approche
- **Titre** : "On ne vend pas du temps. On vend un systeme."
- **3 piliers** (grid-3, cards avec border-top coloree) :
  1. "Vos donnees, pas des moyennes" (diagnostic sur mesure)
  2. "Production automatisee" (PAS "Agents & workflows internes")
  3. "Validation humaine" (PAS "Verification humaine")
- **Highlight-box** : "Votre budget finance un systeme qui tourne, pas des heures de consultant."
- **Ligne stack** compacte : "{N} outils internes · {N} projets R&D en cours" + lien vers agence-slashr.fr/r-and-d/
  - NE PAS lister les noms d'outils internes (Brief Generator, Janus, AI Ranker = bruit pour le prospect)
  - NE PAS lister DataForSEO dans les outils client-facing

#### Slide 3 : Production
- **Titre** : "Le bon contenu, au bon format, au bon moment"
- **3 formats** (grid-3) : Guides/articles, Pages categories/fiches, Optimisations de l'existant
  - Exemples personnalises au deal (pas generiques)
  - Volumes adaptes a la Phase 1
- **Highlight-box** : "Pourquoi on ne compte pas en articles ?"

#### Slide 4 : Collaboration
- **Titre** : "Comment ca se passe concretement"
- **4 cards** (grid-2 x2) avec labels temporels colores (pas de lettres cryptiques) :
  - "Chaque mois" → Comite de pilotage (45 min)
  - "En continu" → Reporting partage (positions, trafic + resultats business)
  - "A la demande" → Acces direct (reponse sous **48h** ouvrees, pas 24h)
  - "Inclus" → Outils et licences (lister seulement les outils du site agence)
- NE PAS dire "KPIs" → dire "indicateurs", "resultats", "conversions, chiffre d'affaires"

#### Slide 5 : Demarrage (onboarding)
- **Titre** : "Et apres la signature ?"
- **Timeline 3 etapes** :
  - S1 : acces, crawl, prise en main des donnees
  - S2-3 : audit livre, premieres optimisations, plan d'action partage
  - M1 : premier comite de pilotage, resultats quick wins, priorites M2
- **Highlight-box** : "Pas de tunnel de 3 mois avant de voir quelque chose. Les premieres actions sont visibles des les premieres semaines."

**CTA final** : bouton vers l'onglet Investissement.

**Regles design :**
- Snake hover sur toutes les highlight-boxes (bloc `@property --snake-angle` dans le `<style>` du tab)
- Fonds opaques obligatoires sur highlight-boxes et snake-inner : `background:linear-gradient(135deg,#1f1810,#1d1623)`
- Logo SLASHR : `<img src="https://agence-slashr.fr/blog/images/2024/03/LOGO-SLASHR-BLANC-1.png">` (pas un cercle texte)

---

### Onglet 4 : Investissement ("Voici ce que ca coute")

**Spec complete : `agents/prepare-pass2-onglet4.md`.**

Contient : Phase 1 (audit + 90j), accompagnement mensuel (echelle 4 colonnes), simulateur ROI, FAQ accordion, CTA final.

### Onglet 5 : Cas clients ("Resultats observes sur des profils comparables")

Hero fullscreen propre a cet onglet (tag "Cas clients", subtitle = angle preuves). Apres le hero, ouvre sur une slide intro + les cas selectionnes.

**Structure :**
1. **Slide intro** : H2 "Resultats observes sur des profils comparables" + section-intro qui cadre la pertinence par rapport au prospect.
2. **1 slide par cas client** (2-4 cas), chaque slide contient :
   - Highlight-box header : nom du cas + secteur + CA + profil
   - KPI row : 2-3 resultats chiffres (les metriques les plus parlantes pour ce prospect)
   - Grille 2 colonnes : situation initiale + ce qu'on a fait
   - Verbatim client (highlight-box magenta, italique)
   - SO WHAT timeline (quick wins → acceleration → resultats)

### Selection des cas clients

**Critere primaire :** pertinence de l'angle strategique. Un cas d'un secteur different peut etre plus pertinent qu'un cas du meme secteur si le levier est le meme.

**Critere secondaire :** proximite sectorielle (le prospect se reconnait plus facilement).

**Source prioritaire : KB SLASHR.** AVANT d'utiliser les cas generiques de `context/case_studies.md`, interroger la KB SLASHR (MCP slashr-kb) avec `kb_search(query="bilan résultats trafic clics hors-marque", scope="drive")` pour trouver des bilans clients reels avec des resultats chiffres. Prioriser les cas reels (donnees sourcees, bilans existants) sur les cas generiques. Les cas generiques de `case_studies.md` sont un fallback si la KB ne retourne rien de pertinent.

L'IA choisit 1-3 cas en justifiant le critere de selection pour chacun. Jamais inventer un cas ni un chiffre.

**Regle de cadrage :** chaque cas est presente sous l'angle qui resonne avec le prospect. Le meme cas peut etre presente differemment selon le deal.

---

## Etape 2.4 : Pas de transitions SLASHR

Pas de transitions SLASHR. Le SO WHAT de chaque section suffit comme conclusion.
Si une section mene naturellement a la suivante, le lien est dans le titre H2
de la section suivante (ex: "La refonte est un moment de bascule" enchaine
logiquement apres le benchmark concurrentiel).
La proposition ne doit jamais mentionner SLASHR ou ses services dans
l'onglet Diagnostic, sauf dans la section methode d'analyse.

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
- [ ] Sequence Priorites → Implications (onglet Diagnostic) → Decision → 90 jours (onglet Strategie) complete et dans cet ordre dans le DOM
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
- [ ] Zero transition SLASHR dans l'onglet Diagnostic (sauf section methode)
- [ ] Chaque expertise traduite en impact business (pas de jargon brut)

---

## Output Pass 2 : Narrative Blueprint (NBP)

L'agent DOIT ecrire explicitement ce document interne avant de passer a la Pass 3.

```
=== NARRATIVE BLUEPRINT ===

ARC GLOBAL: {arc narratif en 1 ligne}, {justification liee au decideur et au contexte}
TONE_PROFILE: {DIRECT | PEDAGOGIQUE | PROVOCATEUR | TECHNIQUE}
HOOK: {description du hook et pourquoi il est frappant pour ce prospect}
CONSTAT_MODE: {tension | statement}
  - tension : deux KPIs opposes (marque forte + invisible en Search). Utiliser quand le paradoxe EST l'argument.
  - statement (defaut) : KPI large unique. Utiliser quand un seul chiffre suffit.
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

--- ONGLET CONTEXTE (conditionnel, si BRAND_CONTEXT.CONTEXTE_TAB = YES) ---

CONTEXTE_TAB: YES | NO
Hero subtitle: {baseline qui tisse identite + Search, ex: "Une marque qui se transmet depuis 1888. Demain, une marque qui se trouve."}

Piliers ADN (1 slide par pilier):
- Pilier 1 "{nom}": angle Search = {territoire de recherche}, requetes typiques: {exemples}
- Pilier 2 "{nom}": angle Search = {territoire}, requetes: {exemples}
- ...

Personas (1 slide par persona, design standardise):
- B2C: {liste personas avec profil et comportement Search}
- B2B: {liste personas avec profil et comportement Search} (si applicable)

Synthese: {baseline, ex: "X cibles, un constat commun"} + {resume constat Search par cible}

--- ONGLET DIAGNOSTIC ---

1. {Titre section} · role: {accroche / diagnostic / enjeu / opportunite / ...}
   Angle: {description en 1-2 phrases de ce que cette section dit}
   Donnees utilisees: {quelles donnees du SDB alimentent cette section}
   SO WHAT: {highlight box : impact business chiffre pour ce prospect}
   Pourquoi ici: {justification de sa position dans l'arc}

2. {Titre section} · role: {...]
   ...

X. Section "Priorites strategiques" · role: priorisation / conviction
   Contenu: traduction business de la contrainte + leviers identifies
   - Contrainte principale traduite en impact business
   - Leviers prioritaires avec projection chiffree
   - Ce qu'on ne fait pas maintenant (et pourquoi)
   Source: SDB > DIAGNOSTIC STRATEGIQUE

X+0.3. (conditionnel) Section technique/operationnelle (refonte, migration, etc.) · role: vehicule concret
   Si le deal implique une refonte (REFONTE=true), placer la slide technique ICI (apres les priorites, pas avant). Le diagnostic identifie l'architecture comme levier → la refonte devient le vehicule concret. Placer cette slide avant les priorites interrompt le crescendo d'opportunite.
   **Regle CMS :** si le deal est un AO ou que le CMS n'est pas confirme dans les notes, utiliser "refonte e-commerce" ou "nouveau CMS". Ne jamais ecrire "refonte WooCommerce" (ou Shopify, PrestaShop) sauf si le CMS est explicitement confirme par le closer.
   Pourquoi ici: {le diagnostic vient d'identifier l'architecture comme levier, la refonte y repond — causalite directe}

X+0.5. Section "Ce que nous ne priorisons pas (maintenant)" · role: transparence strategique (OBLIGATOIRE)
   3 bullets maximum, issus des axes differes du diagnostic (SDB).
   Chaque bullet :
   - Nom du levier differe
   - Pourquoi il est differe (justification logique uniquement, liee au diagnostic)
   - A quel moment il deviendra pertinent (condition ou horizon)
   Regles :
   - Ton strategique, pas defensif. C'est un choix d'expert, pas une excuse.
   - Pas de justification budget ("c'est trop cher" interdit). Justification logique uniquement ("tant que S3 n'est pas traite, S6 n'a pas de contenu a diffuser").
   - Le prospect doit comprendre que ne PAS faire quelque chose est une decision autant que faire quelque chose.
   - **Override SEA (si SEA_SIGNAL = EXPLICIT) :** le SEA ne doit PAS apparaitre dans cette section "Ce que nous ne priorisons pas". A la place, referencer le pont : "Le cadrage SEA strategique est integre dans la Phase 1. L'activation campagnes intervient en M3-M4, une fois les fondations Search posees." Ce bullet remplace le DEFERRED-SCOPE SEA standard.
   Pourquoi ici: {juste apres les priorites, avant les implications — le decideur voit qu'on a arbitre, pas ignore}

X+1. Section "Ce que cela implique" · role: verrou narratif decisionnel (OBLIGATOIRE)
   **Triplet structure obligatoire** — exactement 3 bullets, chacun avec un role distinct :

   | # | Role | Contenu | Source SDB |
   |---|------|---------|-----------|
   | 1 | **Verrou systemique** | La contrainte PRIMARY et ce qu'elle bloque concretement. Factuel, C-level. | SDB > DIAGNOSTIC STRATEGIQUE > Primary constraint + Systemic limitation |
   | 2 | **Actif inexploite** | Ce qui est DEJA en place chez le prospect et qui n'est pas utilise. Ton positif : le prospect a des atouts. | SDB > SEARCH_STATE forces, GREEN FLAGS, ou donnee specifique |
   | 3 | **Fenetre temporelle** | Projection chiffree issue du diagnostic. Le delta mesurable si rien ne change. | SDB > DIAGNOSTIC STRATEGIQUE > Projection PRIMARY (obligatoire) |

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
   Liee explicitement a la contrainte principale
   Format: "Nous recommandons de [action] car [raison liee au diagnostic]."
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
   3 etapes max alignees strictement sur la contrainte principale
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
   Scenario recommande: {niveau} ({prix}/mois) — {justification 1 phrase}
   Alternatives: {mention 1 ligne}

4. CTA intermediaire leger (lien texte, pas full-width)
   Interdit : "Planifier un echange", "Discuter", "Echanger", "En savoir plus"
   Obligatoire : CTA oriente decision, lie a la trajectoire 90 jours
   Exemples : "Demarrer la Phase 1", "Valider le lancement Phase 1"

5. Sous-section "Strategie Paid" (CONDITIONNEL : si SEA_POSTURE = PILOTE ou CONSEIL)
   Place apres le ROI Simulateur, avant le CTA.
   Contenu :
   a. Rappel de la demande prospect (verbatim brief, issu de SEA_BRIEF_REQUESTS)
   b. Positionnement : "Cabinet conseil Search, pas agence media. Nous structurons la strategie, l'execution quotidienne releve de votre equipe ou d'une agence specialisee sous notre pilotage."
   c. Si PILOTE : trajectoire paid integree au plan 90j (M1 audit campagnes, M2 structure compte + strategie encheres, M3 activation)
   d. Si CONSEIL : bloc "Pont organique → paid" montrant la cascade :
      - Intent mapping (SEO) → Targeting (SEA)
      - Contenu optimise → Quality Score
      - Architecture site → Structure de compte Ads
   e. **INTERDIT : projection ROAS sans donnees historiques.** Reponse type : "L'estimation ROAS fiable necessite 3 mois de donnees campagne. La Phase 1 pose le cadre de mesure."
   f. **INTERDIT : "on gere vos campagnes"** (faux — cabinet conseil, pas agence execution)

--- ONGLET INVESTISSEMENT ---

Structure complete : voir `agents/prepare-pass2-onglet4.md`
Scenario recommande: {lequel et pourquoi}

--- ONGLET CAS CLIENTS ---

Cas selectionnes: {N} cas, critere de selection justifie par cas (angle strategique > secteur)

1. {Nom du cas} · angle: {angle specifique au prospect}
   Metriques cles: {2-3 resultats}
   Verbatim: {citation}
   Pertinence: {pourquoi ce cas resonne avec ce prospect}

2. {Nom du cas} · angle: {...]
   ...

--- SI SEA_SIGNAL = EXPLICIT ---

SEA_POSTURE: {PILOTE | CONSEIL}
SEA_FRAMING: {1 phrase positionnement cabinet conseil, ex: "Nous structurons la strategie paid. L'execution quotidienne releve d'une agence media ou de votre equipe."}
SEA_DIAGNOSTIC: {angle section paid dans Diagnostic, ex: "CPC secteur a X EUR, aucune couverture paid — cadrage strategique necessaire"}
SEA_STRATEGIE: {description sous-bloc paid dans Strategie, ex: "Pont organique→paid : intent mapping, quality score, structure compte"}
SEA_INVESTISSEMENT: {blocs actives — SEA setup / SEA run / les deux}
PONT_ORGANIQUE_PAID: {1-2 phrases : comment le SEO prepare le SEA, ex: "La cartographie d'intentions et l'architecture du site posent les fondations d'un compte Ads structure et performant."}

--- FIN SI SEA ---

=== FIN NBP ===
```
