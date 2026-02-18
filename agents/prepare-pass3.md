# PASS 3 — DESIGN ORCHESTRATOR

## Role

Prendre le NBP et generer le HTML final. Choisir les composants visuels du kit pour chaque section. Assurer le rythme visuel. **Ne PAS modifier le contenu strategique du NBP** — seulement le mettre en forme.

---

## Etape 3.1 — Mapping composants

Pour chaque section du NBP, choisir les composants par role narratif dans le catalogue.

### Catalogue de composants — par role narratif

L'agent ne choisit pas un composant par son nom technique. Il part de **ce qu'il veut montrer**, et le catalogue lui propose les options adaptees.

#### COMPARER — montrer des ecarts, des contrastes

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| VS block | Face-a-face 2 entites | 1 prospect vs 1 concurrent, metriques en miroir |
| Bar chart (anime) | Benchmark horizontal | 3-6 acteurs a comparer sur 1 metrique |
| Comparison matrix | Tableau multi-criteres | Comparer 3+ options sur plusieurs dimensions |
| Before/After | Transformation en 2 panneaux | Montrer l'etat actuel vs l'objectif post-intervention |

#### DIAGNOSTIQUER — analyser, prioriser, arbitrer

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Radar S7 | Heptagramme SVG, 7 axes (0-5), fond sombre, accents orange/violet | Section S7 "Lecture strategique" dans l'onglet Strategie — toujours |
| S7 constraint highlight | Highlight box (orange) + force limitante + implication 1-2 phrases | Apres le radar — contrainte principale |
| S7 levers row | 2-3 KPI mini alignes horizontalement, 1 force = 1 chiffre d'impact | Sous le radar — leviers prioritaires |

#### QUANTIFIER — chiffres, metriques, scores

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| KPI card (standard) | Chiffre + label + sous-texte | Grille de 2-4 metriques cles |
| KPI large | 1 chiffre dramatise, full-width | UN seul chiffre hero — le plus frappant du SDB |
| KPI mini | Icone + chiffre + label, compact | 4-8 metriques secondaires sans prendre de place |
| Stat row | Rangee horizontale avec separateurs | Apercu rapide, metriques legeres en 1 ligne |
| Cost card | Chiffre d'impact + description | Cout de l'inaction (visites perdues, euros, mois) |
| Progress bar | Barre de progression coloree | Scores, maturite, % de completion |
| Donut chart | Repartition en % (SVG) | Part marque/hors-marque, repartition trafic |
| Number ticker | Compteur anime de 0 a N au scroll | Dramatiser un chiffre unique a l'apparition |

#### CITER — voix du prospect, social proof

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Verbatim box | Citation prospect (bordure magenta) | Reprendre une phrase exacte du R1 ou des emails |
| Pull quote | Grande citation centree | Phrase strategique forte — rupture de rythme |
| Testimonial card | Avatar + citation + nom/role | Social proof, resultat client (onglet Cas Clients) |

#### STRUCTURER — organiser, sequencer, hierarchiser

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Timeline | Roadmap phases | Plan en 2-3 phases temporelles (onglet Livrables) |
| Routine grid | Etapes numerotees horizontales | Process repetitif, 4 piliers (onglet Livrables) |
| Funnel | Etapes connectees par des fleches | Parcours conversion, pipeline, flux |
| Accordion | Details cachees sous un resume | FAQ, scope detaille, methodologie (onglet Livrables) |

#### ALERTER — attirer l'attention, recommander

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Highlight box (orange) | Interpretation strategique | Apres un bloc de data — "ce que ca signifie" |
| Highlight box (magenta) | Alerte, risque, contrainte | Point d'attention, red flag |
| Highlight box (violet) | Conviction, position assumee | "Notre conviction" — prise de position SLASHR |
| Highlight box (gradient) | Conclusion forte | Synthese d'une section majeure |
| Callout banner | Bandeau full-width, fond gradient | Rupture visuelle, transition majeure |

#### VENDRE — conversion, investissement, ROI

| Composant | Usage | Quand le choisir |
|-----------|-------|------------------|
| Pricing card | Scenarios investissement | 2-3 niveaux, `.recommended` pour le conseille (onglet Livrables) |
| ROI Simulator | Sliders interactifs + calcul JS | Onglet ROI Interactif |
| CTA full-width | Appel a l'action avec blobs | Toujours en fin d'onglet Strategie ET Livrables |

#### CONTEXTUALISER — situation, donnees, details

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

## Etape 3.2 — Regles de composition

### Rythme visuel

- **Alterner** les types de composants. Pas 3 highlight boxes d'affilee. Pas 4 grilles de cards consecutives.
- **Creer des respirations** avec les Pull quotes, Callout banners, et KPI large — ils rompent le flux dense.
- **Apres chaque bloc de data** (table, bar chart, grid de KPIs), placer une interpretation (highlight box) qui repond a "et alors ?".
- **Les verbatims du prospect** sont des ancres narratives — les placer la ou ils creent un pont avec la recommandation.

### Interpretation strategique

- **Chaque data affichee a un "so what"**. Un bar chart sans interpretation est un dashboard, pas une proposition.
- **Le highlight box apres un bloc de data** ne repete pas les chiffres — il dit ce qu'ils signifient pour CE prospect.
- **Les recommandations sont justifiees** : "on recommande X parce que Y" — jamais "on recommande X" seul.
- **L'expertise est traduite en impact business** : pas "votre DA est faible" mais "votre autorite de domaine limite votre capacite a capter du trafic sur les requetes a fort potentiel commercial".

### Contexte sectoriel

- **Ne pas parler dans le vide** — chaque analyse est ancree dans le secteur du prospect (concurrents nommes, dynamiques de marche, temporalite sectorielle).
- **Test de substitution** — si la phrase marche pour n'importe quel prospect, c'est trop generique. Reecrire.

---

## Etape 3.3 — Structure des 4 onglets

### Nav fixe avec 4 tabs

```
Strategie | Cas Clients | ROI Interactif | Livrables & Methode
```

Les 4 onglets sont **toujours presents**. Aucun n'est optionnel.

### Composants specifiques par onglet

**Onglet Strategie** — composition libre (catalogue complet)
- Hero → sections libres → **section S7** → recommandation → CTA
- Tout composant du catalogue est utilisable
- **Section S7 obligatoire** : Radar S7 + S7 constraint highlight + S7 levers row + Pull quote (insight central)

**Onglet Cas Clients** — composants social proof
- Testimonial cards pour les citations clients
- Before/After pour les transformations
- KPI cards / Stat row pour les chiffres avant/apres
- Highlight box pour le "so what" (lien avec la situation du prospect)

**Onglet ROI Interactif** — composants engagement
- KPI cards pour les hypotheses sourcees
- Table pour le detail des hypotheses
- ROI Simulator (sliders + calcul JS)
- Pricing cards pour les 3 scenarios (avec lien vers onglet Livrables)
- Highlight box violet pour la conviction ROI

**Onglet Livrables & Methode** — composants structure
- **Resume decisionnel** : Highlight box (gradient) avec 6 bullets — en haut de l'onglet, c'est la premiere chose que le decideur voit
- **Board-ready A4** : bouton "Version imprimable" qui declenche `window.print()` — page `@media print` avec resume + radar S7 + ROI + pricing
- **Sous-section Methode S7** : Card (accent) avec definition 2-3 phrases + liste compacte 7 forces (1 ligne chacune) + 1 phrase d'arbitrage. Peut etre dans un Accordion "Notre methode d'analyse".
- **Trajectoire 90 jours** : Timeline 3 etapes (M1 → M2 → M3) avec livrables specifiques par mois
- **Trajectoire 6 mois** : Card ou Timeline M4-M6 avec montee en puissance et KPIs
- Routine grid (intensite du scenario recommande : priorites/mois)
- Accordion (FAQ + scope detaille)
- **Investissement v12.0** : 2 blocs separes — (1) **Phase 1 "Mission structurante"** : card accent, scope qualitatif + livrables + budget global HT, SANS jours ni TJM. (2) **Phase 2 "Orchestration mensuelle"** : 3 niveaux d'intensite (Essentiel/Performance/Croissance), le recommande en `.recommended` avec border gradient, les autres compacts. Scope qualitatif + budget mensuel HT, SANS jours/mois ni TJM. + sous-bloc "Ce que coute l'inaction" (composant s7-insight avec 3 impacts business chiffres).
- CTA full-width

---

## Etape 3.4 — Design system

Voir `context/design_system.md` pour les couleurs, typographies, gradients, espacements. Les regles non-negociables :
- Fond sombre `#1a1a1a` (jamais de fond blanc)
- Accents : orange `#E74601`, magenta `#CE08A9`, violet `#8962FD`
- Titres : Funnel Display (Google Fonts)
- Corps : Inter (Google Fonts)
- Responsive (mobile-first)
- Print-friendly (@media print)

---

## Etape 3.5 — Validation

Le HTML est **REJECTED** si :
1. Une section est generique (echoue au test de substitution)
2. Un chiffre est present sans source identifiable
3. Le design ne respecte pas le design system (fond blanc, accents manquants)
4. Le ton est arrogant, suppliant, ou contient du jargon non explique
5. Un des 4 onglets MVP est vide ou avec du contenu placeholder
6. Le ROI utilise des hypotheses non sourcees
7. L'arc narratif n'est pas justifie (ordre des sections arbitraire)
8. Deux blocs de data consecutifs sans interpretation entre eux
9. Une section "Pourquoi SLASHR" standalone existe
10. Un differenciateur SLASHR n'est pas lie a un data block precedent
11. Le ton contient de la pression commerciale ou de la dramatisation
12. Une phrase est dramatique au lieu de strategique ("catastrophe", "crise", "vous perdez tout")
13. La section S7 recommande de travailler les 7 forces (le S7 priorise — max 3 leviers actifs)
14. La section S7 est absente de l'onglet Strategie
15. L'insight central du S7 passe le test de substitution (= fonctionne pour n'importe quel prospect)
16. Le S7 a plus d'1 PRIMARY ou 0 PRIMARY (exactement 1 obligatoire)
17. Un DEFERRED n'a pas de justification "pourquoi pas maintenant"
18. Le resume decisionnel est absent ou depasse 6 bullets
19. La page board-ready A4 (print) est absente
20. La trajectoire 90 jours n'est pas decoupee en M1/M2/M3 avec actions concretes
21. Un SO WHAT utilise une formulation generique interdite (cf. regle anti-generique)
22. La section "Ce que cela implique" est absente apres le bloc S7 dans l'onglet Strategie
23. La section "Decision strategique recommandee" est absente ou ne contient pas "Nous recommandons" ou "Decision strategique"
24. La section "Ce que cela signifie concretement (90 jours)" est absente sous la decision recommandee
25. La sequence obligatoire Diagnostic → S7 → Ce que cela implique → Decision recommandee → 90 jours n'est pas respectee dans l'onglet Strategie
26. Le CTA final contient un verbe passif ou generique ("Planifier un echange", "Discuter", "Echanger", "En savoir plus") au lieu d'un verbe d'action strategique lie a la Phase 1 ("Demarrer", "Valider", "Activer", "Lancer")
27. Le deal comporte une refonte et l'onglet n'est pas structure en 3 actes narratifs (Acte 1 Securiser / Acte 2 Transformer / Acte 3 Accelerer) avec ponts narratifs entre chaque acte, OU la phrase "0 perte de trafic strategique" est absente, OU la synthese/pricing apparait avant les 3 actes, OU les actes sont des blocs juxtaposes sans transitions narratives
28. La section Investissement presente 3 packs egaux au lieu de 1 trajectoire recommandee + 2 variantes, OU le sous-bloc "Ce que coute l'inaction" est absent ou contient des impacts non lies aux donnees du diagnostic
29. La section Investissement affiche des jours, un TJM, ou des sous-composants internes (etude lexicale, diagnostic, benchmark, AMOA, plan redirections, recette, monitoring) — seuls le scope qualitatif et le budget global sont visibles dans le HTML client
30. Un levier a un setup Phase 1 mais pas de run Phase 2, OU un levier a un run Phase 2 sans setup Phase 1 — la coherence levier doit etre stricte

---

## ROI — Methode de calcul

### Methode primaire : chaine de trafic

```
1. Trafic organique actuel = X visites/mois (source: DataForSEO)
2. Separation marque / hors-marque
3. Benchmark concurrent = C visites/mois
4. Gap = C - X = potentiel recuperable
5. Multiplicateur conservateur justifie par le gap reel
6. Gain trafic → valorisation :
   A. Si taux de conversion connu : gain x CVR x panier moyen = CA additionnel
   B. Si CVR inconnu : utiliser ETV comme proxy
7. ROI = gain annuel / investissement SLASHR
```

### Regles ROI

- Jamais de multiplicateur sorti du chapeau — justifie par un gap concurrentiel reel
- Le trafic de marque n'est PAS multiplie
- Si l'investissement n'est pas connu, fournir la formule avec placeholder
- Toujours le scenario conservateur (arrondir en defaveur)
- Chaque hypothese sourcee dans un tableau

### Simulateur interactif (onglet ROI Interactif)

Le simulateur ROI utilise des sliders que le prospect peut manipuler :
- Trafic actuel (pre-rempli avec la donnee reelle)
- Multiplicateur cible (pre-rempli avec le gap concurrent)
- Taux de conversion (pre-rempli avec estimation secteur ou donnee reelle)
- Panier moyen (pre-rempli si connu)
- Investissement mensuel (pre-rempli selon scenario recommande)

Les 3 KPIs se recalculent en temps reel (JS vanilla) : visites a M12, CA organique annuel, ROI.

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
4 onglets : Strategie ({N} sections + S7) | Cas Clients ({N} cas) | ROI Interactif | Livrables & Methode

DRAFT — a valider avant partage avec le prospect.
Ouvre le fichier HTML dans un navigateur pour preview.
```
