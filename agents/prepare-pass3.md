# PASS 3 : DESIGN ORCHESTRATOR

## Role

---

## Rappel regles critiques (avant toute generation)

> **Regles completes : `agents/shared.md`.** Rappel des plus critiques pour Pass 3 :
> - **Chiffres = copie du SDB, jamais recalcules.** Copie exacte, meme nombre, meme unite. Arrondir uniquement pour la lisibilite.
> - R3 Francais | R7 Pas de sur-engineering | R12 Verbatims exacts | R14 Zero pression (inclut "chaque mois/jour sans") | R15 Zero dramatisation | R18 Zero tiret cadratin

---

## Gates qualite avant export (obligatoire)

### 0) Coherence donnees SDB → HTML (AVANT TOUT)
Verifier que chaque chiffre du HTML existe dans le SDB avec la meme valeur et la meme periode.
- Budget Ads : le HTML dit X, le SDB dit Y → doivent matcher
- CPA : meme valeur, meme periode (90j ou 30j)
- Trafic organique : meme perimetre pays
- **Pricing : le HTML dit X EUR/mois, le NBP dit Y EUR/mois → doivent matcher exactement.** Si le NBP dit Production 1 400 EUR/mois, le HTML ne peut pas dire 2 100 EUR/mois. La Pass 3 copie le NBP, elle ne recalcule pas.

Si un ecart est detecte → corriger le HTML pour matcher le SDB/NBP. Ne jamais modifier le SDB depuis la Pass 3.

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


Prendre le NBP et generer le **contenu HTML des 5-6 onglets** (Contexte conditionnel + Diagnostic + Strategie + Projet conditionnel + Investissement + Cas clients). Choisir les composants visuels du kit pour chaque section. Assurer le rythme visuel. **Ne PAS modifier le contenu strategique du NBP**, seulement le mettre en forme.

**Liberte de mise en forme :** l'IA peut adapter la presentation visuelle (choix de composants, decoupage en slides, rythme) tant que le fond strategique du NBP est respecte. Si un composant prevu dans le NBP ne fonctionne pas visuellement, l'IA peut en choisir un autre du kit.

### Architecture skeleton + tabs

Le boilerplate (CSS, JS, nav, structure page) est dans `templates/proposal-skeleton.html`. L'agent ne le reproduit PAS. Il genere uniquement le **contenu de chaque onglet** (le HTML entre les balises `<div class="tab-content">` et `</div>`).

**Workflow (PARALLELE OBLIGATOIRE) :**

Les onglets sont **independants** (chacun consomme le NBP, pas les autres onglets). Les generer en **parallele** via des subagents `writer-tab` :

1. Spawner en parallele 5-6 subagents `writer-tab` (un par onglet) :
   - (conditionnel) writer-tab → `/tmp/tab_contexte.html` — si CONTEXTE_TAB = YES dans le NBP
   - writer-tab → `/tmp/tab_diagnostic.html`
   - writer-tab → `/tmp/tab_strategie.html`
   - writer-tab → `/tmp/tab_projet.html`
   - writer-tab → `/tmp/tab_investissement.html`
   - writer-tab → `/tmp/tab_cas_clients.html`
2. Attendre que tous les writer-tab terminent. Verifier que les fichiers existent.
3. Si le simulateur ROI a du JS custom, ecrire `/tmp/extra_roi_sim.js`
4. Assembler avec `tools/build_proposal.py` :
   ```bash
   python3 tools/build_proposal.py \
     --deal-id {deal_id} \
     --title "Analyse strategique · {entreprise}" \
     --contexte /tmp/tab_contexte.html \
     --diagnostic /tmp/tab_diagnostic.html \
     --strategie /tmp/tab_strategie.html \
     --projet /tmp/tab_projet.html \
     --investissement /tmp/tab_investissement.html \
     --cas-clients /tmp/tab_cas_clients.html \
     --extra-js /tmp/extra_roi_sim.js \
     --output .cache/deals/{deal_id}/artifacts/PROPOSAL-{date}-{slug}.html
   ```
   Note : `--contexte` et `--projet` sont optionnels. Sans eux, la proposition a 4 onglets (comportement par defaut).

**Ce que l'agent genere (le vrai travail creatif) :**
- Le hero de chaque onglet (4 ou 5 heroes fullscreen, un par tab)
- Toutes les sections/slides de chaque onglet
- Les composants visuels (bar charts, KPIs, tables, highlight boxes, etc.)
- Le contenu textuel sur-mesure
- Le simulateur ROI custom (JS dans extra_roi_sim.js)

**Ce que le skeleton fournit (boilerplate identique a chaque proposition) :**
- Le `<head>` (charset, viewport, fonts)
- Tout le CSS (~2000 lignes, variables, composants, responsive, print)
- La nav fixe (4 onglets par defaut, jusqu'a 6 si Contexte et/ou Projet injectes par build_proposal.py)
- La structure `<div class="main">` + `<div class="tab-content">`
- Le footer
- Le JS core (tab switching, bar chart animation, accordion, ticker, donut animation)

> **Fallback :** si le skeleton n'est pas disponible, l'agent genere le HTML complet comme avant (lire `templates/proposal-kit.html`).

---

### Architecture des onglets (obligatoire)

**Hero sur chaque onglet :** chaque onglet COMMENCE par un `<section class="hero">` avec blobs gradient. Structure identique au hero Diagnostic : `hero-tag` (nom de l'onglet), `h1` (titre), `hero-subtitle` (1 phrase), `hero-scroll`. Pas de `.tab-header` compact.

**Footer entre onglets :** chaque onglet (sauf le dernier) SE TERMINE par une slide footer avec CTA vers l'onglet suivant. Structure : `<div class="slide">` (PAS `<section class="hero">` car ca casse les progress dots) avec blobs en fond (`<div class="hero-blobs"><div class="hero-blob-3"></div></div>`), contenu en `z-index:10`, et un `<a>` style inline (background gradient, padding, border-radius) avec un `onclick` qui change de tab + appelle `updateDots()`. Ne PAS utiliser `.nav-tab` ni `.cta-button` (styles ecrases par le skeleton).

**IDs sans accents :** les IDs des tabs ne doivent JAMAIS contenir de caracteres accentues. `tab-strategie` et non `tab-stratégie`. Les `data-tab` de la nav doivent matcher exactement.

### Choix des composants (libre)

L'IA choisit les composants du kit (`templates/proposal-kit.html`, reference condensee dans `context/proposal-kit-reference.md`) pour chaque section.

**Contraintes :**
- **Max 1 composant visuel par slide** (bar-chart, donut, table, cards grid). Si 2 composants sont necessaires, splitter en 2 slides.
- **Budget viewport : ~700px de contenu utile max par slide** (1440x900 - nav 56px - paddings). Si le contenu depasse, scinder en 2 slides. Le writer-tab doit verifier la densite AVANT de retourner le HTML.
- Pas 2 blocs data consecutifs sans interpretation (highlight-box ou texte)
- **Max 1 highlight-box (SO WHAT) par slide**, 3 lignes max.
- Le rythme visuel doit maintenir l'attention du decideur
- **Titres h2 : max 8 mots.** Le detail va dans le section-intro, pas dans le titre.
- **Section labels : max 4 mots.** Ex: "Google Ads France", pas "Google Ads France, Search, 30 derniers jours".
- **Ne jamais utiliser `.card-accent`** (bordure gradient moche). Utiliser `.card` + `border-top: 3px solid var(--orange/magenta/violet)`.
- **Simulateur ROI : max 2 sliders.** Le reste en constantes dans le JS. Trop d'inputs perd le decideur. Si ROI Confidence = LOW dans le SDB, remplacer le simulateur ROI par un simulateur de trafic (1 slider : gain clics) ou le supprimer.
- **board-ready-a4 : masque a l'ecran.** Le CSS doit inclure `.board-ready-a4 { display: none }` + `@media print { .board-ready-a4 { display: block } }`.

**L'IA decide :** quel composant pour quelle donnee. Un bar-chart n'est pas obligatoire pour un benchmark. Une table n'est pas obligatoire pour une comparaison. Le kit offre 30 composants, l'IA choisit ceux qui servent le mieux la narration.

---

## Etape 3.2 : Regles de composition

### Rythme visuel

- **Alterner** les types de composants. Pas 2 highlight boxes empilees (utiliser verbatim-box ou grid-2 pour casser la monotonie). Pas 4 grilles de cards consecutives.
- **Creer des respirations** avec les Pull quotes, Callout banners, et KPI large, ils rompent le flux dense.
- **Apres chaque bloc de data** (table, bar chart, grid de KPIs), placer une interpretation (highlight box) qui repond a "et alors ?".
- **Les verbatims du prospect** sont des ancres narratives, les placer la ou ils creent un pont avec la recommandation.
- **Coherence des elements repetes** : quand plusieurs elements du meme type sont generes (personas, cas clients, comparaisons), utiliser le MEME design pattern pour tous. Ne jamais mixer card-accent et surface-div pour des elements equivalents. Choisir un pattern et le repliquer.
- **Densite max par section** : chaque `.slide` (section plein ecran) contient au maximum **1 composant visuel** (bar chart, donut, table, cards grid) + **1 highlight-box** (SO WHAT). Au-dela, decouper en slides supplementaires. Un slide surcharge perd le decideur.

### Densite slide : regle de l'ecran unique (OBLIGATOIRE)

Chaque slide doit tenir sur un ecran standard (1440x900) sans scroll vertical interne. Si un slide necessite du scroll → le decouper ou reduire le contenu.

**Indicateurs de sur-densite (trigger le decoupage) :**
- Plus de 2 grids empiles verticalement
- Plus de 6 cards dans un grid
- Plus de 1 bar chart + 1 table dans le meme slide
- Plus de 3 highlight-boxes dans le meme slide
- Un grid-2 ou grid-3 ou les cards depassent 150px de hauteur chacune

**Action si sur-dense :** decouper en 2 slides. Le premier slide porte le composant visuel principal + le contexte. Le second porte le SO WHAT + les donnees secondaires.

**Nombre max de slides par onglet :**
- Diagnostic : pas de plafond (la deduplication est le garde-fou)
- Strategie : 5 slides max (hors hero et CTA)
- Projet : 5 slides (equipe, approche, production, collaboration, onboarding)
- Investissement : pas de plafond (structure fixe)
- Cas clients : 1 intro + 2-4 cas = 3-5 slides

### Progress dots (navigation intra-onglet)

Chaque onglet affiche des dots de progression en bas de l'ecran. Le dot actif correspond a la slide visible (IntersectionObserver). Les dots sont interactifs (clic = scroll to slide).
Classes CSS : `.progress-dots`, `.progress-dot`, `.progress-dot.active`

### Animation des donuts SVG

Les donuts SVG s'animent a l'entree dans le viewport (IntersectionObserver, threshold 0.3), meme pattern que les bar charts. Le stroke-dashoffset initial est egal a la circonference (251.33 pour r=40, 326.7 pour r=52 — pas de remplissage), et transite vers la valeur cible en 1.5s cubic-bezier(0.22, 1, 0.36, 1) quand le donut est visible. Stocker la valeur cible dans `data-offset` sur le `circle.donut-fill`.

### Inline styles → classes CSS

Eviter les inline styles. Utiliser les utility classes du design system :
- `.mb-0`, `.mb-sm` (8px), `.mb-md` (16px), `.mb-lg` (24px), `.mb-xl` (40px)
- `.text-sm` (13px), `.text-xs` (11px)
- `.text-center`
- `.max-w-700` (max-width: 700px)
- `.mt-md` (margin-top: 16px), `.mt-lg` (margin-top: 24px)
Si un style inline est necessaire pour un cas unique, il est tolere. Mais les patterns repetes (margin-bottom, font-size, color) doivent etre des classes.

### LAYOUT_MODE et HOOK_TYPE (signaux Pass 2 → Pass 3)

Si `HOOK_TYPE = "ancrage_identitaire"` dans le NBP : le hero-subtitle tisse l'histoire de la marque dans le constat. Le ton reste factuel (pas de flatterie), mais l'ouverture est emotionnelle.

Si `LAYOUT_MODE = "narrative-heavy"` : privilegier les highlight-boxes, pull-quotes et verbatims aux charts et tables.
Si `LAYOUT_MODE = "visual-heavy"` : privilegier les before/after, donuts, bar charts aux paragraphes de texte.
Si `LAYOUT_MODE = "data-heavy"` (defaut) : benchmark + tables + charts, equilibre standard.

### Interpretation strategique

- **Chaque data affichee a un "so what"**. Un bar chart sans interpretation est un dashboard, pas une proposition.
- **Le highlight box apres un bloc de data** ne repete pas les chiffres, il dit ce qu'ils signifient pour CE prospect.
- **Les recommandations sont justifiees** : "on recommande X parce que Y", jamais "on recommande X" seul.
- **L'expertise est traduite en impact business** : pas "votre DA est faible" mais "votre autorite de domaine limite votre capacite a capter du trafic sur les requetes a fort potentiel commercial".

### Contexte sectoriel

- **Ne pas parler dans le vide** : chaque analyse est ancree dans le secteur du prospect (concurrents nommes, dynamiques de marche, temporalite sectorielle).
- Rappel : test de substitution, zero pression, zero dramatisation (cf. `agents/shared.md`, regles 13-15).

## Principes de design éditorial (OBLIGATOIRE)

### Philosophie
La proposition est un document éditorial premium, pas un dashboard ni un template. Chaque slide raconte une étape de l'histoire. Le décideur scrolle et comprend l'arc narratif par les titres et les chiffres seuls.

### Composants préférés (dx-)
Les composants "dx-" (définis dans `context/proposal-kit-reference.md` section "DX — COMPOSANTS ÉDITORIAUX PREMIUM") sont le choix par défaut pour toutes les nouvelles propositions. Les anciens composants (highlight-box, card, kpi grid) restent disponibles comme fallback mais ne doivent PAS être le premier choix.

| Besoin | Composant dx- | Ancien composant (fallback) |
|--------|--------------|---------------------------|
| SO WHAT / interprétation | `.dx-insight` | `.highlight-box` |
| Chiffre clé hero | `.dx-metric` | `.kpi-large` |
| Liste de constats | `.dx-issues` (grille numérotée) | `.grid-2` + `.card` |
| Étapes / timeline | `.dx-steps` (numérotée) | `.timeline` |
| Contexte client | `.dx-context-grid` (bordures) | `.context-grid` + `.context-card` |
| Implications | `.dx-implication` (numérotée) | `.highlight-box` empilées |
| Contenu différé | `.dx-deferred` | `.highlight-box.highlight-gradient` |
| CTA | `.dx-cta-btn` (border gradient) | `.cta-btn` |

### Anti-patterns (INTERDIT sauf justification)

1. **Encadrer chaque bloc dans une card/box** — les séparations sont des lignes fines (`border-bottom: 1px solid var(--border)`), pas des rectangles avec `background: var(--surface)`
2. **highlight-boxes comme SO WHAT** — utiliser `.dx-insight` (border-left gradient 2px, texte libre, max-width 600px)
3. **Emojis dans des cercles colorés** — les labels de section sont textuels (`dx-tag` avec trait gradient)
4. **Plus de 2 composants visuels par slide** — 1 visuel + 1 dx-insight max
5. **Titres h2 pleine largeur** — contraindre à `max-width: 680px` via `.dx-title`
6. **Paragraphes de scope** — les scopes de prestation sont en bullets courtes, jamais en pavé de texte
7. **Grid-3 de highlight-boxes** — empiler verticalement les implications (`.dx-implication`)
8. **Métriques géantes empilées verticalement** — si 3+ métriques, les mettre en `grid-3` côte à côte (1 slide)

### Animations (OBLIGATOIRE)

Chaque `.slide` dans les onglets générés par writer-tab DOIT avoir la classe `.dx-reveal`. Les éléments internes utilisent `.dx-d1` à `.dx-d4` pour le stagger.

Chaque onglet DOIT inclure un script IntersectionObserver en haut :
```js
(function(){
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('dx-visible');
        e.target.querySelectorAll('.dx-bar-fill[data-w]').forEach(b => {
          b.style.width = b.dataset.w + '%';
        });
      }
    });
  }, { threshold: 0.15 });
  setTimeout(() => {
    document.querySelectorAll('#tab-{TAB_ID} .dx-reveal').forEach(el => obs.observe(el));
  }, 200);
})();
```

### Aération

- L'espace négatif (fond noir) est un élément de design, pas du vide à remplir
- margin-top entre sections : 48-56px minimum
- Les chiffres clés sont le premier élément lu (font-size > 48px, gradient)
- Max-width sur les blocs de texte : 560-680px (pas pleine largeur)

---

## Etape 3.3 : Structure des onglets

### Nav fixe avec 5-6 tabs

```
(Contexte) | Diagnostic | Strategie | Projet | Investissement | Cas clients
```

Les 5 onglets obligatoires sont **toujours presents** : Diagnostic, Strategie, Projet, Investissement, Cas clients. L'onglet Contexte est conditionnel :
- **Contexte** : si CONTEXTE_TAB = YES dans le NBP

### Composants specifiques par onglet

**Hero par onglet (obligatoire)** : chaque onglet a son propre hero fullscreen. Il n'y a plus de hero partage ni de `hero--compact`. Chaque hero contient : `.hero-blobs`, `.hero-tag` (nom de l'onglet), `h1` (nom du prospect), `.hero-subtitle` (baseline unique adaptee a l'onglet), `.hero-context` (contexte client), `.hero-date`, `.hero-scroll`.

Le `hero-tag` et le `hero-subtitle` varient selon l'onglet :
- **Contexte** (conditionnel) : tag = "Contexte", subtitle = baseline identitaire adaptee au Search
- **Diagnostic** : tag = "Diagnostic Search", subtitle = baseline du hook (constat principal)
- **Strategie** : tag = "Strategie Search", subtitle = direction strategique (ex: "De l'audit a l'amplification")
- **Projet** (conditionnel) : tag = "Projet", subtitle = angle humain (ex: "Un interlocuteur, une methode, un rythme")
- **Investissement** : tag = "Investissement", subtitle = angle decision (ex: "Ce que cela represente, ce que cela debloque")
- **Cas clients** : tag = "Cas clients", subtitle = angle preuves (ex: "Des resultats mesures sur des profils comparables")

Le `hero-context` et le `hero-date` sont identiques sur tous les onglets.

**Onglet Contexte (conditionnel)** : si CONTEXTE_TAB = YES dans le NBP
- Hero fullscreen (tag "Contexte", subtitle qui tisse identite + Search)
- **Slides ADN** (1 slide par pilier) : chaque pilier de marque est traduit en territoire de recherche. Composants : `section-label`, texte contextuel, `highlight-box` (variante au choix) avec l'opportunite Search, `query-pill` pour les requetes typiques
- **Slides Personas** (1 slide par persona, B2C puis B2B) : design STANDARDISE obligatoire. Format : `grid-2` avec deux divs surface (`background:var(--surface)`, `border-radius:var(--radius-md)`, `padding:28px`). Colonne gauche : titre "Profil & comportement" (couleur orange, uppercase 12px), liste `<ul>`. Colonne droite : titre "Parcours Search" (couleur magenta, uppercase 12px), paragraphe + `query-pill`. Sous le grid : `highlight-box` avec "Enjeu Search". **Meme design pour TOUS les personas (B2C et B2B), sans exception.**
- **Slide synthese** : titre centre, grid de piliers ADN (couleurs differenciees par pilier), `highlight-box highlight-gradient` qui nomme toutes les cibles et leur constat Search commun
- **CTA leger** : `cta-section` avec bouton vers onglet Diagnostic
- **Pas de data DataForSEO** dans cet onglet. Pas de bar charts, pas de tables comparatives. C'est du contexte qualitatif.

**Onglet Diagnostic** : composition libre, hero full screen (catalogue complet)
- Hero (blobs, contexte client tisse) → sections libres → **section priorites strategiques** → ce qu'on ne fait pas → implications
- Tout composant du catalogue est utilisable
- **Section "Priorites strategiques" obligatoire** : traduit les conclusions du diagnostic strategique interne en langage business. Highlight box (contrainte principale en impact business) + 2-3 axes d'action concrets + insight central. **ZERO jargon interne** : pas de radar, pas de noms de forces, pas de scores /5, pas de labels internes. Cf. regle 20 de `agents/shared.md`.
- **SO WHAT obligatoire** : chaque section se termine par un highlight box qui traduit les donnees en impact business chiffre, **3 lignes max**
- **Cas clients : onglet dedie** (onglet 4), pas inline dans le Diagnostic
- **Pas de transitions SLASHR** : la proposition ne mentionne jamais SLASHR ou ses services dans l'onglet Diagnostic. Le SO WHAT de chaque section suffit comme conclusion.
- **Fusion constat/benchmark** : si le constat et le benchmark utilisent les memes KPIs, les fusionner en 1 seule slide (KPI large → contexte → bar chart → table optionnelle → SO WHAT)

**Onglet Strategie** : hero propre + decision strategique
- Hero fullscreen (tag "Strategie Search"). Premiere section apres le hero : decision strategique.
- **Decision strategique** ("Nous recommandons...") : OUVRE l'onglet
- **Timeline 90 jours** : M1/M2/M3
- **ROI Simulator** : hypotheses sourcees + sliders + calcul JS + scenario recommande
- Highlight box violet pour la conviction ROI
- **CTA intermediaire leger** (lien texte, pas full-width)

**Onglet Projet** (obligatoire) : template fixe + variables deal-specific

> **Template HTML de reference : `templates/tab-projet-template.html`.**
> L'agent utilise ce template et remplace les variables `{{...}}` par les valeurs du deal. La structure, le design et le wording des sections fixes ne doivent PAS etre reinventes a chaque deal.

**Sections modulaires (adaptees par deal) :**
- **Ecosysteme :** le nombre de cards et les partenaires listes dependent du contexte du deal. Si on challenge un prestataire existant, ne PAS le lister comme partenaire. Si le prospect n'a que Buddy comme partenaire, 2 cards suffisent (SLASHR + Buddy). Adapter.
- **Production :** les 3 cards decrivent le PROCESS de production (identification data-driven, production IA+humain, mesure), PAS le scope strategique (qui est dans l'onglet Strategie). Inclure la redaction d'annonces si deal Ads.
- **Approche :** montrer les outils proprietaires (19 tools), l'IA integree aux pipelines (pas en surcouche), la capacite a construire des outils sur mesure. C'est le differenciateur.

**Variables a remplacer :**
- `{{PROSPECT_NAME}}` : nom du prospect (h1 hero)
- `{{PROSPECT_CONTEXT}}` : ligne contexte hero (secteur, CA, contexte)
- `{{HERO_DATE}}` : date
- `{{CP_DESCRIPTION}}` : description chef de projet (1-2 phrases adaptees au deal)
- `{{PRODUCTION_CARD_1/2/3_TITLE}}` : titres des 3 cards production (adaptes au deal)
- `{{PRODUCTION_CARD_1/2/3_DESC}}` : descriptions (adaptees au deal)
- `{{PRODUCTION_CARD_1/2/3_EX}}` : exemples concrets (specifiques au prospect)
- `{{PRODUCTION_CARD_1/2/3_KPI}}` : KPI/volume par type de production
- `{{REPORTING_AXES}}` : axes du reporting (adaptes au perimetre)
- `{{ONBOARDING_S1/S24/M2}}` : contenu onboarding (adapte au contexte du deal)
- `{{ONBOARDING_HIGHLIGHT}}` : phrase highlight onboarding

**Sections fixes (identiques a chaque deal, NE PAS modifier) :**
- Slide 1 Equipe : chef de projet + 3 associes (AL, QC, BD)
- Slide 2 Approche : 3 piliers + stack ("19 outils internes · 10 projets R&D")
- Slide 4 Collaboration : 4 cards (comite, reporting, acces direct, outils)
- CTA vers onglet Investissement

**Sections adaptees (variables uniquement) :**
- Hero : nom, contexte, date
- Slide 1 : description chef de projet
- Slide 3 Production : 3 cards specifiques au deal
- Slide 4 Collaboration : axes reporting
- Slide 5 Onboarding : timeline adaptee au contexte (refonte, AO, standard)

**Pas de pricing, pas de budget** dans cet onglet. C'est du "comment on travaille", pas du "combien ca coute".
**Slide Production : expliquer le PROCESS, pas le SCOPE.** La slide production explique comment on produit du contenu (identification data-driven → production IA+humain → mesure). Elle ne repete pas la strategie (pas de "optimisation pages centres" ni "conseil Ads" ici). Inclure la redaction d'annonces dans le process de production.
**Slide Approche (systeme IA) :** montrer ce qui differencie SLASHR. Outils proprietaires (19 tools), IA integree aux pipelines (pas en surcouche), capacite a construire des outils sur mesure pour le client.

**Onglet Investissement** : hero propre + resume decisionnel
- Hero fullscreen (tag "Investissement"). Premiere section apres le hero : resume decisionnel.
- **Resume decisionnel** : Highlight box (gradient) avec 6 bullets (max 120 chars chacun), en haut de l'onglet, c'est la premiere chose que le decideur voit
- **Board-ready A4** : bouton "Version imprimable" qui declenche `window.print()`, page `@media print` avec resume + priorites strategiques + ROI + pricing
- **Cout de l'inaction (AVANT le pricing)** : highlight-box avec 3 impacts business chiffres. Place AVANT les pricing cards pour l'ancrage psychologique : le decideur voit d'abord ce qu'il perd, puis ce que ca coute d'agir.
  > **Conditionnel :** n'inclure le cout de l'inaction que si les donnees permettent un chiffrage reel (gaspillage Ads quantifie, trafic concurrent chiffre, perte mesurable). Si les constats sont deja connus du prospect (repetes depuis le diagnostic), ne pas forcer cette section.
- **Investissement v12.0** : 2 blocs separes. (1) **Phase 1 "Mission structurante"** : card accent, scope qualitatif + livrables + budget global HT, SANS jours ni TJM. (2) **Phase 2 "Notre recommandation"** : 1 scenario recommande en `.recommended` avec border gradient et justification. Les alternatives mentionnees en 1-2 lignes compactes sous la recommandation. Scope qualitatif + budget mensuel HT, SANS jours/mois ni TJM. Sous chaque scenario, ajouter une ligne : "Ce que ca debloque en priorite : {levier en langage client, issu du NBP}". Utiliser le langage prospect (ex: "debloquer votre visibilite locale"), PAS les labels internes (ex: PAS "Contenu S3"). Ne jamais mentionner jours/TJM.
- **Recommandation conditionnelle** : si Confidence = Low sur 2+ ROI drivers, la carte `.recommended` conserve son statut mais affiche un label supplementaire : "Recommandation conditionnelle — validation des hypotheses en Phase 1".
- **Sous-section Methode d'analyse (optionnel)** : dans l'accordion FAQ si pertinent. 2-3 phrases generiques sur l'approche ("les dimensions cles de votre visibilite Search, priorisation des 2-3 axes a plus fort impact"). Pas de noms de forces internes, pas de scores, pas de radar.
- **Recap budget (slide dedie)** : vue consolidee sur 2 colonnes (annee 1 / annee 2 si applicable). Chaque phase porte : (1) un objectif qualitatif colore (orange Phase 1, magenta Phase 2), (2) budget accompagnement SLASHR, (3) budget media minimum en ligne separee, (4) total phase. Hero gradient avec total global HT. Footnote : "Budget media minimum pressenti : {montant}/mois. Ajustable selon la strategie et la saisonnalite. Sans engagement sur la Phase 2." Ce slide est SEPARE du pricing, jamais dans le meme slide.
- **Accordion "Questions frequentes"** : reprend les OBJECTIONS A PRE-EMPT du NBP. Chaque item : titre = objection formulee comme question, contenu = reponse data-first + source courte (DataForSEO / GSC / verbatim / benchmark). Si une objection n'a pas de source → ajouter "a confirmer en Phase 1".
- **Prochaine etape** : bloc 3 lignes (decision, date, action)
- **CTA full-width** (unique CTA principal de la proposition)

**Onglet Cas clients** (optionnel, decide au Checkpoint 2) : hero propre + slide intro
- **Slide intro** : H2 "Resultats observes sur des profils comparables" + section-intro qui cadre la pertinence par rapport au prospect
- **1 slide par cas client** (2-4 cas), chaque slide contient :
  - Micro-benchmark en tete (`.micro-benchmark`) : prospect → cas (avant) → cas (apres)
  - Highlight-box header : nom du cas + secteur + CA + profil
  - KPI row : 2-3 resultats chiffres
  - Grille 2 colonnes : situation initiale + ce qu'on a fait
  - Verbatim client (highlight-box magenta, italique)
  - SO WHAT timeline (quick wins → acceleration → resultats)
- **Regle** : les cas sont selectionnes par la Pass 2 (NBP section ONGLET CAS CLIENTS). La Pass 3 ne choisit pas les cas, elle les met en forme.

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

> **Regles de validation completes : `context/validation_rules.md`** (45 regles, 4 layers).

Appliquer les 4 layers dans l'ordre :

1. **Layer 1 Structural** (17 regles, PASS/FAIL) : DOM, CSS, regex. Un seul FAIL = REJECT du HTML.
2. **Layer 2 Content** (12 regles, WARN) : heuristiques de contenu. Correction recommandee.
3. **Layer 3 Semantic** (10 regles, checklist) : revue agent. Verifier chaque item manuellement.
4. **Layer 4 Quality Metrics** (6 regles, WARN) : metriques de qualite redactionnelle (densite donnees, specificite titres, triplet implications, SO WHAT, micro-benchmarks, repetitions).

---

## Etape 3.6 : Validation automatisee (post-generation)

Apres l'assemblage du HTML (via `build_proposal.py`) et avant l'upload Drive :

1. Verifier que le fichier `.cache/deals/{deal_id}/artifacts/PROPOSAL-{date}-{slug}.html` existe (produit par `build_proposal.py`)
2. Executer le script de validation :
   ```bash
   python3 tools/validate_proposal.py .cache/deals/{deal_id}/artifacts/PROPOSAL-*.html
   ```
3. **Si FAIL** (Layer 1) : corriger le HTML, re-valider. Ne pas uploader tant qu'il y a des FAIL.
4. **Si WARN** (Layer 2) : corriger si possible, sinon documenter dans le terminal pourquoi le WARN est acceptable.
5. **Layer 3** (checklist) : parcourir mentalement chaque item. Corriger si un item echoue.
6. Une fois valide : uploader dans Drive.
7. **Mettre a jour `r2_pack_link` dans Pipedrive** avec l'URL du fichier PROPOSAL uploade (cf. `context/pipedrive_reference.md` pour le field key).

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
4c. Objectif recommandé par défaut = X + 30% du gap (conservateur), sauf si diagnostic confidence High + signaux forts.
5. Multiplicateur conservateur justifie par le gap reel
6. Gain trafic → valorisation :
   A. Si taux de conversion connu : gain x CVR x panier moyen = CA additionnel
   B. Si CVR inconnu : utiliser ETV comme proxy
7. ROI = gain annuel / investissement SLASHR
```

### Methode SEA : economie et reallocation

Pour les deals avec un volet Ads, le ROI ne se calcule PAS par la chaine de trafic mais par l'economie et la reallocation :

```
1. Identifier le gaspillage : campagnes a CPA > 2x la moyenne, 0-2 conversions
2. Identifier les campagnes performantes : CPA < moyenne, volume significatif
3. Calculer l'economie directe : budget gaspille recupéré
4. Calculer le gain de reallocation : budget recupéré / CPA des campagnes performantes = leads supplementaires
5. NE PAS supposer que PMax absorbe le budget au meme CPA (PMax ne scale pas lineairement)
6. Projections conservatrices : gain réaliste = economie + reallocation vers le CPA moyen des top performers, pas vers le meilleur CPA
```

**Reality check obligatoire :**
- Le CPA cible est-il realiste ? (pas juste budget/CPA = leads)
- PMax scale-t-il lineairement ? (non, toujours nuancer)
- Les campagnes mCPC peuvent-elles basculer en tCPA sans transition ? (non, prevoir 2-4 semaines d'apprentissage)
- Le gain projete est-il coherent avec la mecanique reelle ?

**Simulateur SEA :** max 2 sliders (CPA cible + trafic organique local). Afficher la situation actuelle comme reference (leads actuels → gains → total apres). Les constantes (CPA actuel, budget, CVR) sont fixees dans le JS.

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

**Investissement dans le simulateur :** le simulateur ROI utilise le scenario recommande comme base de calcul. L'investissement total = Phase 1 + (mensuel recommande * 12). Le JS extrait le montant du `.recommended .pricing-price` dans `#tab-investissement` OU le hardcode a partir du NBP.

**Footnote simulateur (obligatoire)** : sous les resultats du simulateur, ajouter une note en `font-size:11px;color:var(--text-30)` qui cadre les projections : CPC moyen estime, investissement SLASHR (hors budget media), et "Projections a regime de croisiere, hors gain de conversion lie a la refonte" si une refonte est dans le scope.

---

## Boucle self-critique (OBLIGATOIRE, apres assemblage, avant upload)

Apres l'assemblage par `build_proposal.py`, le systeme ne montre PAS le HTML au closer. Il execute une boucle d'auto-amelioration (max 2 iterations).

### Iteration 1

```bash
python3 tools/validate_proposal.py .cache/deals/{deal_id}/artifacts/PROPOSAL-{date}-{slug}.html
```

**Lire le score et les resultats :**
- **Score >= 85 ET 0 HARD failures** → proposition prete, sortir de la boucle
- **HARD failures (Layer 1)** → corriger les onglets concernes :
  - Identifier quel onglet contient le probleme (jargon interne, tirets cadratins, TJM visible, CTA generique)
  - Re-generer le fragment HTML de cet onglet
  - Re-assembler avec `build_proposal.py`
  - Passer a l'iteration 2
- **Score < 85, 0 HARD** → analyser les WARN les plus impactants :
  - Densite slide excessive → decouper les slides sur-denses
  - Deduplication manquante → fusionner les sections redondantes
  - Accents manquants → corriger
  - Passer a l'iteration 2

### Iteration 2 (si declenchee)

```bash
python3 tools/validate_proposal.py .cache/deals/{deal_id}/artifacts/PROPOSAL-{date}-{slug}.html
```

- **Score >= 75 ET 0 HARD** → acceptable, sortir
- **Sinon** → sortir avec WARNING : "Score {X}/100, {N} problemes non resolus — verifier manuellement"

### Ce que le systeme corrige sans demander
- HARD failures Layer 1 (jargon interne R14, tirets R18b, TJM/jours R29, CTA R26)
- Accents manquants (R16c)
- Coherence chiffres SDB → HTML (gate 0)
- Slides sur-denses (Layer 2 R48)

### Ce que le systeme signale mais ne touche pas
- Choix narratifs (Layer 3 semantic) — c'est le territoire du closer
- Structure globale de l'arc — validee au Checkpoint 2
- Pricing — valide au Checkpoint 2

---

## Output

### Fichiers generes

| Fichier | Audience | Upload Drive |
|---------|----------|--------------|
| `PROPOSAL-{YYYYMMDD}-{entreprise-slug}.html` | Prospect (via closer) | Oui |
| `PROPOSAL-{YYYYMMDD}-{entreprise-slug}-score.json` | Interne (tracking) | Non |
| `INTERNAL-DIAG-{YYYYMMDD}-{entreprise-slug}.md` | Interne seulement | Oui (prefixe `INTERNAL-` = exclu de la collecte Module 2) |

Le `INTERNAL-DIAG-*.md` contient le diagnostic strategique complet (section diagnostic du SDB). Il est uploade dans le meme dossier Drive pour archivage et rejouabilite, mais n'est jamais partage au prospect.

### Message de fin

```
=== PROPOSITION GENEREE ===

Score qualite : {X}/100 (Grade {A/B/C/D/F})
  Structure  : {X}/35
  Contenu    : {X}/25
  Qualite    : {X}/25
  Semantique : {X}/15

{Si self-critique active : "Auto-corrigee : {N} problemes resolus (HARD: {n}, SOFT: {n})"}
{Si score < 75 : "Score bas — verifier les WARN ci-dessus"}

Arc narratif : {description en 1 ligne de l'arc choisi et pourquoi}
Diagnostic : contrainte = {en langage business} | leviers = {2-3 axes}
Onglets : {Contexte |} Diagnostic ({N} sections) | Strategie | {Projet |} Investissement | Cas clients ({N} cas)

Fichier : .cache/deals/{deal_id}/artifacts/PROPOSAL-{date}-{slug}.html
{Si uploade : Drive : {lien}}

DRAFT, a valider avant partage avec le prospect.
→ /review {deal_id} pour preview live + review slide par slide
```
