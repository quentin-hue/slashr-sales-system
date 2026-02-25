# PASS 3 : DESIGN ORCHESTRATOR

## Role

---

## Rappel regles critiques (avant toute generation)

> **Zero pression commerciale** : pas de "ne manquez pas", "il est urgent de", "derniere chance". Inclut "Chaque mois/jour sans X". (cf. `agents/shared.md`, regle 14)
> **Zero dramatisation** : pas de "catastrophe", "crise", "vous perdez tout". Les donnees suffisent. (cf. regle 15)
> **Francais** : tous les outputs en francais. (cf. regle 3)
> **Verbatims = citations exactes** entre guillemets. (cf. regle 12)
> **Pas de tiret cadratin** (`—`, `&mdash;`) dans aucun output. Remplacer par `:`, `,`, `.`, `·`. (cf. regle 18)
> **Pas de sur-engineering** : le closer copie-colle, on ne complique pas. (cf. regle 7)

---

## Gates qualite avant export (obligatoire)

### 1) Contradiction check
Appliquer les regles de `context/output_contract.md` (Contradiction check).
Si une contradiction reste, l'expliciter comme trade-off assume.

### 2) Quality Rubric
Appliquer le **Quality Rubric** de `context/output_contract.md`.
Sortie : `Score X/8` + corrections (max 3) avant generation finale.

### 3) Faits / Hypotheses / Manquants (resume)
Inclure un encart final (court) :
- 3 faits clefs (sourcés)
- 2 hypotheses (avec confiance)
- 3 manquants + acces minimal


Prendre le NBP et generer le HTML final. Choisir les composants visuels du kit pour chaque section. Assurer le rythme visuel. **Ne PAS modifier le contenu strategique du NBP**, seulement le mettre en forme.

---

## Etape 3.1 : Mapping composants

Pour chaque section du NBP, choisir les composants par role narratif dans le catalogue.

### Catalogue de composants : par role narratif

L'agent ne choisit pas un composant par son nom technique. Il part de **ce qu'il veut montrer**, et le catalogue lui propose les options adaptees.

#### COMPARER : montrer des ecarts, des contrastes

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| VS block | Face-a-face 2 entites | 1 prospect vs 1 concurrent, metriques en miroir. Eviter si les memes donnees sont deja dans un bar chart |
| Bar chart (anime) | Benchmark horizontal | 3-6 acteurs a comparer sur 1 metrique |
| Stacked bar chart | Benchmark avec decomposition | Comparer 3+ acteurs avec split interne (ex: marque/hors-marque). Privilegier quand le split est l'argument principal. Legende obligatoire |
| Comparison matrix | Tableau multi-criteres | Comparer 3+ options sur plusieurs dimensions |
| Before/After | Transformation en 2 panneaux | Montrer l'etat actuel vs l'objectif post-intervention |

#### DIAGNOSTIQUER : analyser, prioriser, arbitrer

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Radar S7 | Heptagramme SVG, 7 axes (0-5), fond sombre, accents orange/violet | Section S7 "Lecture strategique" dans l'onglet Diagnostic, toujours |
| S7 constraint highlight | Highlight box (orange) + force limitante + implication 1-2 phrases | Apres le radar : contrainte principale |
| S7 levers row | 2-3 KPI mini alignes horizontalement, 1 force = 1 chiffre d'impact | Sous le radar : leviers prioritaires |

#### QUANTIFIER : chiffres, metriques, scores

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| KPI card (standard) | Chiffre + label + sous-texte | Grille de 2-4 metriques cles |
| KPI large | 1 chiffre floating hero-style, glow + gradient | UN seul chiffre statement. Pas de box. Glow magenta/violet derriere, gradient orange→magenta sur le texte. Utiliser avec .slide-constat (titre + chiffre + data row + source). **Le titre h2 du slide-constat est un FAIT chiffre, jamais un jugement.** "14 800 recherches/mois sur votre marque. 0 client acquis via le Search generique." (bon) vs "Votre marque est connue. Mais votre site est invisible." (mauvais). Le KPI large amplifie le fait, il ne le remplace pas par une interpretation. |
| KPI mini | Icone + chiffre + label, compact | 4-8 metriques secondaires sans prendre de place |
| Stat row | Rangee horizontale avec separateurs | Apercu rapide, metriques legeres en 1 ligne |
| Cost card | Chiffre d'impact + description | Cout de l'inaction (visites perdues, euros, mois) |
| Progress bar | Barre de progression coloree | Scores, maturite, % de completion |
| Donut chart | Repartition en % (SVG) | Part marque/hors-marque, repartition trafic |
| Number ticker | Compteur anime de 0 a N au scroll | Dramatiser un chiffre unique a l'apparition |

#### CITER : voix du prospect, social proof

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Verbatim box | Citation prospect (bordure magenta) | Reprendre une phrase exacte du R1 ou des emails |
| Pull quote | Grande citation centree | Phrase strategique forte, rupture de rythme |
| Testimonial card | Avatar + citation + nom/role | Social proof, resultat client (onglet Diagnostic (cas clients inline)) |

#### STRUCTURER : organiser, sequencer, hierarchiser

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Timeline | Roadmap phases | Plan en 2-3 phases temporelles (onglet Investissement) |
| Routine grid | Etapes numerotees horizontales | Process repetitif, 4 piliers (onglet Investissement) |
| Funnel | Etapes connectees par des fleches | Parcours conversion, pipeline, flux |
| Accordion | Details cachees sous un resume | FAQ, scope detaille, methodologie (onglet Investissement) |

#### ALERTER : attirer l'attention, recommander

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Highlight box (orange) | Interpretation strategique | Apres un bloc de data : "ce que ca signifie" |
| Highlight box (magenta) | Alerte, risque, contrainte | Point d'attention, red flag |
| Highlight box (violet) | Conviction, position assumee | "Notre conviction", prise de position SLASHR |
| Highlight box (gradient) | Conclusion forte | Synthese d'une section majeure |
| Callout banner | Bandeau full-width, fond gradient | Rupture visuelle, transition majeure |

#### VENDRE : conversion, investissement, ROI

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Pricing card | Scenarios investissement | 2-3 niveaux, `.recommended` pour le conseille (onglet Investissement) |
| ROI Simulator | Sliders interactifs + calcul JS | Onglet Strategie (section ROI) |
| CTA full-width | Appel a l'action avec blobs | En fin d'onglet Investissement uniquement (CTA principal) |

#### CONTEXTUALISER : situation, donnees, details

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Context card | Icone + titre + description | Rappel de la situation prospect |
| Card (standard) | Titre + paragraphe | Bloc generique, opportunite, territoire |
| Card (accent) | Idem + bordure top gradient | Attirer l'oeil sur une card specifique |
| Card (icon) | Idem + icone ronde coloree | Ajouter une dimension visuelle |
| Quick win card | Icone + titre + desc + impact | Actions immediates a fort impact |
| Table | Donnees structurees | Keywords, positions, hypotheses sourcees |
| Tags | brand/generic labels | Dans les tables, pour typer les keywords |

---

## Etape 3.2 : Regles de composition

### Rythme visuel

- **Alterner** les types de composants. Pas 3 highlight boxes d'affilee. Pas 4 grilles de cards consecutives.
- **Creer des respirations** avec les Pull quotes, Callout banners, et KPI large, ils rompent le flux dense.
- **Apres chaque bloc de data** (table, bar chart, grid de KPIs), placer une interpretation (highlight box) qui repond a "et alors ?".
- **Les verbatims du prospect** sont des ancres narratives, les placer la ou ils creent un pont avec la recommandation.
- **Densite max par section** : chaque `.slide` (section plein ecran) contient au maximum **3 composants visuels** (hors titre et source). Au-dela, decouper en 2 slides ou fusionner des composants. Un slide surcharge perd le decideur.

### Interpretation strategique

- **Chaque data affichee a un "so what"**. Un bar chart sans interpretation est un dashboard, pas une proposition.
- **Le highlight box apres un bloc de data** ne repete pas les chiffres, il dit ce qu'ils signifient pour CE prospect.
- **Les recommandations sont justifiees** : "on recommande X parce que Y", jamais "on recommande X" seul.
- **L'expertise est traduite en impact business** : pas "votre DA est faible" mais "votre autorite de domaine limite votre capacite a capter du trafic sur les requetes a fort potentiel commercial".

### Contexte sectoriel

- **Ne pas parler dans le vide** : chaque analyse est ancree dans le secteur du prospect (concurrents nommes, dynamiques de marche, temporalite sectorielle).
- Rappel : test de substitution, zero pression, zero dramatisation (cf. `agents/shared.md`, regles 13-15).

---

## Etape 3.3 : Structure des 3 onglets

### Nav fixe avec 3 tabs

```
Diagnostic | Strategie | Investissement
```

Les 3 onglets sont **toujours presents**. Aucun n'est optionnel.

### Composants specifiques par onglet

**Onglet Diagnostic** : composition libre, hero full screen (catalogue complet)
- Hero complet (blobs, contexte client tisse) → sections libres → **section S7** → deferred → implications
- Tout composant du catalogue est utilisable
- **Section S7 obligatoire** : Radar S7 + S7 constraint highlight + S7 levers row + Pull quote (insight central)
- **Cas clients inline** : composant micro-benchmark (.micro-benchmark) insere apres les sections pertinentes (max 2-3 dans l'onglet)
- **SO WHAT obligatoire** : chaque section se termine par un highlight box qui traduit les donnees en impact business chiffre

**Onglet Strategie** : header compact, pas de hero full-screen
- Remplacer le hero full-screen par un **header compact** : `.tab-header` avec section-label + h2 + section-intro. Pas de blobs.
- **Decision strategique** ("Nous recommandons...") : OUVRE l'onglet
- **Timeline 90 jours** : M1/M2/M3
- **ROI Simulator** : hypotheses sourcees + sliders + calcul JS + 3 scenarios
- Highlight box violet pour la conviction ROI
- **CTA intermediaire leger** (lien texte, pas full-width)

**Onglet Investissement** : header compact, pas de hero full-screen
- Meme format **header compact** (`.tab-header`)
- **Resume decisionnel** : Highlight box (gradient) avec 6 bullets, en haut de l'onglet, c'est la premiere chose que le decideur voit
- **Board-ready A4** : bouton "Version imprimable" qui declenche `window.print()`, page `@media print` avec resume + radar S7 + ROI + pricing
- **Investissement v12.0** : 2 blocs separes. (1) **Phase 1 "Mission structurante"** : card accent, scope qualitatif + livrables + budget global HT, SANS jours ni TJM. (2) **Phase 2 "Orchestration mensuelle"** : 3 niveaux d'intensite (Essentiel/Performance/Croissance), le recommande en `.recommended` avec border gradient, les autres compacts. Scope qualitatif + budget mensuel HT, SANS jours/mois ni TJM. Sous chaque scenario, ajouter une ligne : "Ce que ca debloque en priorite : {PRIMARY S7} (+ {SECONDARY si utile})". PRIMARY/SECONDARY issus du strategy_plan_internal.md. Ne jamais mentionner jours/TJM. + sous-bloc "Ce que coute l'inaction" (composant s7-insight avec 3 impacts business chiffres).
- **Recommandation conditionnelle** : si Confidence = Low sur 2+ ROI drivers, la carte `.recommended` conserve son statut mais affiche un label supplementaire : "Recommandation conditionnelle — validation des hypotheses en Phase 1".
- **Sous-section Methode S7** : Card (accent) avec definition 2-3 phrases + liste compacte 7 forces (1 ligne chacune) + 1 phrase d'arbitrage. Peut etre dans un Accordion "Notre methode d'analyse".
- **Accordion "Questions frequentes"** : reprend les OBJECTIONS A PRE-EMPT du NBP. Chaque item : titre = objection formulee comme question, contenu = reponse data-first + source courte (DataForSEO / GSC / verbatim / benchmark). Si une objection n'a pas de source → ajouter "a confirmer en Phase 1".
- **Prochaine etape** : bloc 3 lignes (decision, date, action)
- **CTA full-width** (unique CTA principal de la proposition)

---

## Etape 3.4 : Design system

Voir `context/design_system.md` pour les couleurs, typographies, gradients, espacements. Les regles non-negociables :
- Fond sombre `#1a1a1a` (jamais de fond blanc)
- Accents : orange `#E74601`, magenta `#CE08A9`, violet `#8962FD`
- Titres : Funnel Display (Google Fonts)
- Corps : Inter (Google Fonts)
- Responsive (mobile-first)
- Print-friendly (@media print)

---

## Etape 3.5 : Validation

> **Regles de validation completes : `context/validation_rules.md`** (44 regles, 4 layers).

Appliquer les 3 layers dans l'ordre :

1. **Layer 1 Structural** (17 regles, PASS/FAIL) : DOM, CSS, regex. Un seul FAIL = REJECT du HTML.
2. **Layer 2 Content** (12 regles, WARN) : heuristiques de contenu. Correction recommandee.
3. **Layer 3 Semantic** (10 regles, checklist) : revue agent. Verifier chaque item manuellement.

---

## Etape 3.6 : Validation automatisee (post-generation)

Apres la generation du HTML et avant l'upload Drive :

1. Ecrire le HTML dans `.cache/deals/{deal_id}/artifacts/PROPOSAL-{date}-{slug}.html`
2. Executer le script de validation :
   ```bash
   python3 tools/validate_proposal.py .cache/deals/{deal_id}/artifacts/PROPOSAL-*.html
   ```
3. **Si FAIL** (Layer 1) : corriger le HTML, re-valider. Ne pas uploader tant qu'il y a des FAIL.
4. **Si WARN** (Layer 2) : corriger si possible, sinon documenter dans le terminal pourquoi le WARN est acceptable.
5. **Layer 3** (checklist) : parcourir mentalement chaque item. Corriger si un item echoue.
6. Une fois valide : uploader dans Drive.

> Le script `tools/validate_proposal.py` automatise les Layers 1 et 2. Il ne remplace pas la revue semantique (Layer 3).

---

## ROI : Methode de calcul

### Methode primaire : chaine de trafic

```
1. Trafic organique actuel = X visites/mois (source: DataForSEO)
2. Separation marque / hors-marque
3. Benchmark concurrent = C visites/mois
4. Gap = C - X = potentiel recuperable
4b. Plafond crédible = benchmark concurrent (C) : les objectifs M12 ne doivent jamais dépasser C sans justification.
4c. Objectif recommandé par défaut = X + 30% du gap (conservateur), sauf si S7 confidence High + signaux forts.
5. Multiplicateur conservateur justifie par le gap reel
6. Gain trafic → valorisation :
   A. Si taux de conversion connu : gain x CVR x panier moyen = CA additionnel
   B. Si CVR inconnu : utiliser ETV comme proxy
7. ROI = gain annuel / investissement SLASHR
```

### Regles ROI

- Jamais de multiplicateur sorti du chapeau, justifie par un gap concurrentiel reel
- Le trafic de marque n'est PAS multiplie
- Si l'investissement n'est pas connu, fournir la formule avec placeholder
- Toujours le scenario conservateur (arrondir en defaveur)
- Chaque hypothese sourcee dans un tableau
- Toujours afficher un tableau "Hypothèses & sources" (DataForSEO, benchmark secteur, verbatim prospect, etc.)
- Si Confidence = Low sur 2+ drivers → afficher un avertissement soft : "Hypothèses à confirmer en Phase 1"

### Simulateur interactif (section ROI dans l'onglet Strategie)

Le simulateur ROI utilise des sliders que le prospect peut manipuler :
- **Trafic actuel** (pre-rempli avec la donnee reelle, lecture seule ou ajustable)
- **Visites cibles M12** (pre-rempli avec le benchmark concurrent. Le prospect manipule un objectif en visites/mois — PAS un "multiplicateur x2, x3". Afficher le label "Objectif visites/mois a 12 mois")
- **Taux de conversion** (pre-rempli avec estimation secteur ou donnee reelle)
- **Panier moyen** (pre-rempli si connu)
- **Investissement mensuel** (pre-rempli selon scenario recommande)

Les 3 KPIs se recalculent en temps reel (JS vanilla) : visites a M12, CA organique annuel, ROI.

**Regle UX :** le slider "Visites cibles M12" est l'element central. Son min = trafic actuel, son max = benchmark concurrent (le plafond credible). Le prospect comprend immediatement ce qu'il ajuste. Un "multiplicateur x2.5" est abstrait — "passer de 3 200 a 8 000 visites/mois" est concret.

---

## Output

### Fichiers generes

| Fichier | Audience | Upload Drive |
|---------|----------|--------------|
| `PROPOSAL-{YYYYMMDD}-{entreprise-slug}.html` | Prospect (via closer) | Oui |
| `INTERNAL-S7-{YYYYMMDD}-{entreprise-slug}.md` | Interne seulement | Oui (prefixe `INTERNAL-` = exclu de la collecte Module 2) |

Le `INTERNAL-S7-*.md` contient le diagnostic S7 complet tel que produit a l'Etape 1.4 (`strategy_plan_internal.md`). Il est uploade dans le meme dossier Drive pour archivage et rejouabilite, mais n'est jamais partage au prospect.

### Message de fin

```
Proposition generee : PROPOSAL-{date}-{slug}.html
Diagnostic interne : INTERNAL-S7-{date}-{slug}.md
Uploades dans le dossier Drive du deal.

Arc narratif : [description en 1 ligne de l'arc choisi et pourquoi]
S7 : contrainte = {force} | leviers = {2-3 forces} | insight = {1 phrase}
3 onglets : Diagnostic ({N} sections + S7) | Strategie (decision + 90j + ROI) | Investissement

DRAFT, a valider avant partage avec le prospect.
Ouvre le fichier HTML dans un navigateur pour preview.
```
