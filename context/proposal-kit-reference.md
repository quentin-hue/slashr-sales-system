# Proposal Kit — Reference classes CSS

> Condense des classes CSS et structures HTML minimales du kit `templates/proposal-kit.html`.
> Utiliser ce fichier comme aide-memoire rapide. Pour le CSS complet, voir le kit source.

---

## LAYOUT

### Nav (barre fixe avec onglets)

Classes : `.nav`, `.nav-inner`, `.nav-logo`, `.nav-tab`, `.nav-tab.active`

```html
<nav class="nav">
  <div class="nav-inner">
    <div class="nav-logo"><span>SLASHR</span></div>
    <button class="nav-tab active" data-tab="diagnostic">Diagnostic</button>
    <button class="nav-tab" data-tab="strategie">Strategie</button>
    <button class="nav-tab" data-tab="investissement">Investissement</button>
    <button class="nav-tab" data-tab="cas-clients">Cas clients</button>
  </div>
</nav>
```

Barre fixe 56px, blur, onglets dynamiques via JS.

### Main + Tab content (conteneur scroll-snap)

Classes : `.main`, `.tab-content`, `.tab-content.active`

```html
<div class="main">
  <div class="tab-content active" id="tab-diagnostic">...</div>
  <div class="tab-content" id="tab-strategie">...</div>
  <div class="tab-content" id="tab-investissement">...</div>
  <div class="tab-content" id="tab-cas-clients">...</div>
</div>
```

Chaque `.tab-content` est un conteneur scroll-snap vertical independant.

### Slide (section plein ecran, snap target)

Classes : `.slide`, `.slide-full`, `.slide-constat`

```html
<div class="slide">...</div>
<div class="slide slide-constat">...</div>
```

`.slide` : max-width 1280px, centrage vertical, snap-align start. `.slide-full` : idem mais full-width. `.slide-constat` : centrage texte + vertical pour les statements chiffres.

### Hero (intro full-width avec blobs gradient)

Classes : `.hero`, `.hero-short`, `.hero-blobs`, `.hero-blob-3`, `.hero-tag`, `.hero-subtitle`, `.hero-date`, `.hero-scroll`

```html
<section class="hero">
  <div class="hero-blobs"><div class="hero-blob-3"></div></div>
  <span class="hero-tag">SLASHR x Prospect</span>
  <h1>Titre</h1>
  <p class="hero-subtitle">Sous-titre</p>
  <p class="hero-date">Date</p>
  <div class="hero-scroll"></div>
</section>
```

Full-height, blobs orange/magenta/violet en fond, scroll indicator anime. Utilise uniquement dans l'onglet Diagnostic.

### Header compact (onglets Strategie et Investissement)

Classes : `.tab-header`

```html
<div class="tab-header">
  <p class="section-label">Label onglet</p>
  <h1>Titre de l'onglet</h1>
  <p class="section-intro">Introduction courte.</p>
</div>
```

```css
/* Header compact — tabs 2 et 3 (pas de hero full-screen) */
.tab-header {
  padding: 80px 30px 40px;
  max-width: 1280px;
  margin: 0 auto;
}
.tab-header .section-label {
  color: var(--text-50);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 12px;
}
.tab-header h1 {
  font-family: var(--font-display);
  font-size: clamp(28px, 5vw, 44px);
  font-weight: 700;
  line-height: 1.15;
  margin-bottom: 16px;
}
.tab-header .section-intro {
  color: var(--text-70);
  font-size: 1.1rem;
  max-width: 720px;
}
```

Remplace le hero full-screen pour les onglets Strategie et Investissement. Pas de blobs, pas de plein ecran. Le contenu demarre directement apres le header.

### Section (label + titre + intro)

Classes : `.section`, `.section-label`, `.section-intro`

```html
<section class="section">
  <div class="section-label">Label</div>
  <h2>Titre</h2>
  <p class="section-intro">Introduction.</p>
</section>
```

Structure de base pour introduire un bloc de contenu. Le `h2` utilise Funnel Display.

### Grids (2, 3, 4 colonnes)

Classes : `.grid-2`, `.grid-3`, `.grid-4`

```html
<div class="grid-3">
  <div>...</div>
  <div>...</div>
  <div>...</div>
</div>
```

Grilles CSS responsive. Passent en 1 colonne sous 900px.

### Progress Dots — navigation intra-onglet

Classes : `.progress-dots`, `.progress-dot`, `.progress-dot.active`

```html
<div class="progress-dots">
  <span class="progress-dot active" data-slide="0"></span>
  <span class="progress-dot" data-slide="1"></span>
  <span class="progress-dot" data-slide="2"></span>
</div>
```

```css
.progress-dots {
  position: fixed; bottom: 24px; left: 50%;
  transform: translateX(-50%); z-index: 90;
  display: flex; gap: 8px;
  background: rgba(26,26,26,0.8);
  backdrop-filter: blur(10px);
  padding: 8px 16px; border-radius: var(--radius-full);
  border: 1px solid var(--border);
}
.progress-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--text-30); cursor: pointer;
  transition: all 0.3s;
}
.progress-dot.active {
  background: var(--orange); transform: scale(1.3);
}
```

**JS :** IntersectionObserver sur chaque `.slide` dans l'onglet actif. Le dot correspondant passe en `.active`. Clic sur un dot = `scrollIntoView({ behavior: 'smooth' })`.

### Footer

Classes : `.footer`

```html
<footer class="footer">SLASHR — Document confidentiel</footer>
```

Texte centre, bordure top subtile.

---

## COMPARER

### VS Block — face-a-face 2 entites

Classes : `.vs-grid`, `.vs-card`, `.vs-separator`, `.vs-metric`, `.vs-metric-value`, `.vs-metric-value.good`, `.vs-metric-value.bad`, `.vs-metric-label`

```html
<div class="vs-grid">
  <div class="vs-card">
    <h3>Prospect</h3>
    <div class="vs-metric">
      <div class="vs-metric-value good">30M</div>
      <div class="vs-metric-label">Label</div>
    </div>
  </div>
  <div class="vs-separator">VS</div>
  <div class="vs-card">
    <h3>Concurrent</h3>
    <div class="vs-metric">
      <div class="vs-metric-value bad">5K</div>
      <div class="vs-metric-label">Label</div>
    </div>
  </div>
</div>
```

Grille 3 colonnes (card | VS | card). Modifier `.good` / `.bad` pour colorer les valeurs.

### Bar Chart — benchmark horizontal anime

Classes : `.chart-container`, `.chart-title`, `.bar-row`, `.bar-label`, `.bar-label.is-prospect`, `.bar-track`, `.bar-fill`, `.bar-fill.orange`, `.bar-fill.violet`, `.bar-fill.muted`, `.bar-value`, `.bar-value.is-prospect`

```html
<div class="chart-container">
  <div class="chart-title">Titre du benchmark</div>
  <div class="bar-row">
    <div class="bar-label is-prospect">Prospect</div>
    <div class="bar-track"><div class="bar-fill orange" data-width="15"></div></div>
    <div class="bar-value is-prospect">1 250</div>
  </div>
  <div class="bar-row">
    <div class="bar-label">Concurrent</div>
    <div class="bar-track"><div class="bar-fill muted" data-width="65"></div></div>
    <div class="bar-value">5 400</div>
  </div>
</div>
```

Barres animees au scroll via `data-width` (%). `.orange` = solid `var(--orange)` (prospect), `.violet` = solid `var(--violet)` (territoires informationnels), `.muted` = gris concurrents. Ne pas utiliser `var(--gradient)` sur les barres fines : le gradient ne rend pas sur des elements etroits.

### Comparison Matrix — tableau multi-criteres

Classes : `.matrix-wrap`, `th.recommended`, `td.recommended-col`, `.matrix-check`, `.matrix-cross`, `.matrix-partial`

```html
<div class="matrix-wrap">
  <table>
    <thead>
      <tr>
        <th>Critere</th>
        <th class="recommended">Option A</th>
        <th>Option B</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Critere 1</td>
        <td class="recommended-col"><span class="matrix-check">&#10003;</span></td>
        <td><span class="matrix-cross">&#10007;</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

Tableau comparatif. `.matrix-check` = vert, `.matrix-cross` = gris, `.matrix-partial` = orange. Colonne recommandee avec fond subtil.

### Before/After — transformation en 2 panneaux

Classes : `.before-after`, `.ba-panel`, `.ba-panel.before`, `.ba-panel.after`, `.ba-tag`, `.ba-arrow`

```html
<div class="before-after">
  <div class="ba-panel before">
    <span class="ba-tag">Aujourd'hui</span>
    <h3>Etat actuel</h3>
    <ul><li>Point 1</li></ul>
  </div>
  <div class="ba-arrow">&rarr;</div>
  <div class="ba-panel after">
    <span class="ba-tag">Objectif M12</span>
    <h3>Etat cible</h3>
    <ul><li>Point 1</li></ul>
  </div>
</div>
```

Grille 3 colonnes (avant | fleche | apres). Le panel `.after` a une bordure orange subtile. Les bullets ont des puces colorees par panel.

---

## DIAGNOSTIQUER

### S7 Overview Grid — 7 force cards avec score et etat

Classes : `.s7-grid`, `.s7-card`, `.s7-card[data-state="primary|secondary|deferred"]`, `.s7-card-header`, `.s7-card-id`, `.s7-badge`, `.s7-badge-primary`, `.s7-badge-secondary`, `.s7-badge-deferred`, `.s7-card-title`, `.s7-score`, `.s7-score-bar`, `.s7-score-fill`, `.s7-score-value`, `.s7-card-diagnostic`

```html
<div class="s7-grid">
  <div class="s7-card" data-state="primary">
    <div class="s7-card-header">
      <span class="s7-card-id">S2</span>
      <span class="s7-badge s7-badge-primary">Prioritaire</span>
    </div>
    <div class="s7-card-title">Architecture & technique</div>
    <div class="s7-score">
      <div class="s7-score-bar"><div class="s7-score-fill" style="width:20%"></div></div>
      <span class="s7-score-value">1/5</span>
    </div>
    <div class="s7-card-diagnostic">Diagnostic specifique.</div>
  </div>
</div>
```

Grille 4 colonnes. `data-state` controle la bordure et l'opacite (deferred = 0.6). Score fill colore selon l'etat.

### S7 Radar Interactif — visualisation 7 forces avec tooltips

Classes : `.s7-radar-wrap`, `.s7-radar-svg`, `.s7-radar-point`, `.s7-radar-point[data-state]`, `.s7-radar-tooltip`, `.s7-radar-label`

```html
<div class="s7-radar-wrap">
  <svg class="s7-radar-svg" viewBox="0 0 400 400">
    <!-- Grille radar (pentagones concentriques) -->
    <polygon class="s7-radar-grid" points="..." fill="none" stroke="rgba(255,255,255,0.1)" />
    <!-- ... 5 niveaux -->
    <!-- Forme du prospect -->
    <polygon class="s7-radar-shape" points="..." fill="rgba(231,70,1,0.15)" stroke="#E74601" />
    <!-- Points interactifs -->
    <circle class="s7-radar-point" data-state="primary" data-force="S3" cx="200" cy="50" r="8" />
    <circle class="s7-radar-point" data-state="secondary" data-force="S2" cx="350" cy="150" r="8" />
    <circle class="s7-radar-point" data-state="deferred" data-force="S5" cx="350" cy="300" r="8" />
  </svg>
  <!-- Labels autour du radar -->
  <div class="s7-radar-label" style="top:5%;left:50%">S1 · Intentions <span>2/5</span></div>
  <!-- ... 6 autres labels -->
  <!-- Tooltip (affiche au hover/click) -->
  <div class="s7-radar-tooltip" id="tooltip-S3" style="display:none">
    <div class="s7-radar-tooltip-title">S3 · Contenu — 1/5</div>
    <div class="s7-radar-tooltip-badge primary">Prioritaire</div>
    <div class="s7-radar-tooltip-text">SO WHAT simplifie pour le prospect.</div>
  </div>
</div>
```

**Interactivite (JS) :**
- Hover/click sur un point ou un label = affiche le tooltip correspondant
- Points PRIMARY = orange plein, SECONDARY = violet plein, DEFERRED = gris semi-transparent
- Le tooltip affiche : nom force + score + badge classification + SO WHAT 1 phrase (C-level)
- Mobile : click toggle, pas hover

**Regles :**
- Le radar remplace le listing statique des 7 forces — il est plus compact et plus engageant
- Les SO WHAT dans les tooltips sont des versions **simplifiees** (1 phrase max, C-level) des SO WHAT du strategy_plan_internal.md
- Ne pas surcharger : le radar est un outil d'exploration, pas un dump de donnees

### S7 Insight Callout — contrainte principale

Classes : `.s7-insight`, `.s7-insight-label`, `.s7-insight-constraint`, `.s7-insight-why`

```html
<div class="s7-insight">
  <div class="s7-insight-label">Contrainte principale — S2</div>
  <div class="s7-insight-constraint">Titre de la contrainte</div>
  <div class="s7-insight-why"><strong>Pourquoi c'est le verrou :</strong> explication data-first.</div>
</div>
```

Fond gradient subtil orange/magenta, bordure gauche orange epaisse. Utilise apres la grille S7.

### S7 Priority Table — Force / Diagnostic / Action / Horizon

Classes : `.s7-priority-table`, `tr[data-priority="primary|secondary|deferred"]`, `.s7-horizon`, `.s7-horizon-90j`, `.s7-horizon-6m`, `.s7-horizon-12m`

```html
<div class="table-wrap">
  <table class="s7-priority-table">
    <thead>
      <tr><th>Force</th><th>Diagnostic</th><th>Action</th><th>Horizon</th></tr>
    </thead>
    <tbody>
      <tr data-priority="primary">
        <td>S2 — Architecture</td>
        <td>Diagnostic</td>
        <td>Action</td>
        <td><span class="s7-horizon s7-horizon-90j">90 jours</span></td>
      </tr>
      <tr data-priority="deferred">
        <td>S5 — Autorite</td>
        <td>Diagnostic</td>
        <td>Action differee</td>
        <td><span class="s7-horizon s7-horizon-12m">12 mois</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

Bordure gauche coloree par priorite. Les lignes deferred sont a 50% d'opacite. Badges horizon colores (orange 90j, violet 6m, magenta 12m).

---

## QUANTIFIER

### KPI Card — standard

Classes : `.kpi`, `.kpi-value`, `.kpi-value.magenta`, `.kpi-value.violet`, `.kpi-value.green`, `.kpi-label`, `.kpi-sub`

```html
<div class="kpi">
  <div class="kpi-value">1 250</div>
  <div class="kpi-label">Visites / mois</div>
  <div class="kpi-sub">source: DataForSEO</div>
</div>
```

Card centree avec chiffre orange par defaut. Utiliser dans `.grid-2`, `.grid-3` ou `.grid-4`.

### KPI Large — chiffre hero-style avec glow

Classes : `.kpi-large` (conteneur), reutilise `.kpi-value`, `.kpi-label`, `.kpi-sub`

```html
<div class="kpi-large">
  <div class="kpi-value">&lt; 1%</div>
  <div class="kpi-label">de visibilite hors-marque</div>
  <div class="kpi-sub">Source : DataForSEO</div>
</div>
```

Pas de box. Glow magenta/violet derriere, gradient orange-magenta sur le chiffre. A utiliser dans `.slide-constat`.

### Slide Constat — statement chiffre (conteneur pour KPI Large)

Classes : `.slide-constat`, `.constat-title`, `.constat-data`, `.constat-data-item`, `.constat-data-sep`, `.constat-source`

```html
<div class="slide slide-constat">
  <p class="section-label" style="text-align:center;">Label</p>
  <h2 class="constat-title">Fait chiffre. Pas un jugement.</h2>
  <div class="kpi-large">
    <div class="kpi-value">X</div>
    <div class="kpi-label">Description</div>
  </div>
  <div class="constat-data">
    <span class="constat-data-item"><strong>14 800</strong> recherches</span>
    <span class="constat-data-sep"></span>
    <span class="constat-data-item"><strong>153</strong> mots-cles</span>
  </div>
  <p class="constat-source">Source : DataForSEO</p>
</div>
```

Slide dediee au statement chiffre. Le titre h2 est un FAIT, pas un jugement.

### KPI Mini — compact inline

Classes : `.kpi-mini-grid`, `.kpi-mini`, `.kpi-mini-icon`, `.kpi-mini-icon.magenta`, `.kpi-mini-icon.violet`, `.kpi-mini-data`, `.kpi-mini-value`, `.kpi-mini-label`

```html
<div class="kpi-mini-grid">
  <div class="kpi-mini">
    <div class="kpi-mini-icon">emoji</div>
    <div class="kpi-mini-data">
      <div class="kpi-mini-value">153</div>
      <div class="kpi-mini-label">Label</div>
    </div>
  </div>
</div>
```

Grille auto-fit (min 200px). Icone ronde coloree + chiffre + label compact.

### Stat Row — rangee horizontale de stats

Classes : `.stat-row`, `.stat-row-item`, `.stat-row-value`, `.stat-row-value.orange|.magenta|.violet|.green`, `.stat-row-label`

```html
<div class="stat-row">
  <div class="stat-row-item">
    <div class="stat-row-value orange">153</div>
    <div class="stat-row-label">Mots-cles</div>
  </div>
  <div class="stat-row-item">
    <div class="stat-row-value magenta">~100%</div>
    <div class="stat-row-label">Marque</div>
  </div>
</div>
```

Barre horizontale avec separateurs verticaux automatiques entre les items.

### Cost Card — chiffre d'impact (cout de l'inaction)

Classes : `.cost-card`, `.cost-value`, `.cost-label`, `.cost-desc`

```html
<div class="cost-card">
  <div class="cost-value">6 900</div>
  <div class="cost-label">Visites perdues / mois</div>
  <div class="cost-desc">Description de l'impact.</div>
</div>
```

Card centree avec chiffre orange. A utiliser dans `.grid-3`.

### Progress Bar — barre de progression

Classes : `.progress-group`, `.progress-item`, `.progress-header`, `.progress-label`, `.progress-value`, `.progress-track`, `.progress-fill`, `.progress-fill.orange|.magenta|.violet|.green`, `.progress-sub`

```html
<div class="progress-group">
  <div class="progress-item">
    <div class="progress-header">
      <span class="progress-label">Label</span>
      <span class="progress-value">85/100</span>
    </div>
    <div class="progress-track">
      <div class="progress-fill green" data-width="85"></div>
    </div>
    <div class="progress-sub">Sous-texte optionnel</div>
  </div>
</div>
```

Barre animee au scroll via `data-width`. Gradient par defaut, couleur unique avec modificateur.

### Donut Chart — repartition en % (SVG)

Classes : `.donut-grid`, `.donut-item`, `.donut-svg`, `.donut-track`, `.donut-fill`, `.donut-fill.orange|.magenta|.violet|.green`, `.donut-center`, `.donut-label`

```html
<div class="donut-grid">
  <div class="donut-item">
    <svg class="donut-svg" viewBox="0 0 120 120">
      <circle class="donut-track" cx="60" cy="60" r="52" />
      <circle class="donut-fill magenta" cx="60" cy="60" r="52"
        stroke-dasharray="326.7"
        stroke-dashoffset="16.3" />
    </svg>
    <div class="donut-center">95%</div>
    <div class="donut-label">Label</div>
  </div>
</div>
```

Circumference = 326.7 (r=52). Dashoffset = 326.7 * (1 - pourcentage). Grille auto-fit (min 200px).

**Animation :** les donuts demarrent avec `stroke-dashoffset` = circumference (cercle invisible). Quand le donut entre dans le viewport (IntersectionObserver, threshold 0.3), transiter vers la valeur cible en 1.5s `cubic-bezier(0.22, 1, 0.36, 1)`. Stocker la valeur cible dans `data-offset` sur le `circle.donut-fill`. Le CSS initial met `stroke-dashoffset: 326.7`. Le JS anime vers `data-offset`.

### Number Ticker — compteur anime au scroll

Classes : `.ticker-row`, `.ticker-value`, `.ticker-suffix`

```html
<div class="ticker-row">
  <span class="ticker-value" data-target="21000">0</span>
  <span class="ticker-suffix">visites/mois</span>
</div>
```

Anime de 0 a `data-target` au scroll (ease-out cubic, 1.5s). Gradient sur le chiffre.

---

## CITER

### Verbatim Box — citation prospect

Classes : `.verbatim-box`, `.verbatim-box .source`

```html
<div class="verbatim-box">
  &laquo; Citation exacte du prospect. &raquo;
  <span class="source">Prenom, R1</span>
</div>
```

Fond surface, bordure gauche magenta, texte italique.

### Pull Quote — grande citation centree

Classes : `.pull-quote`, `.pull-source`

```html
<div class="pull-quote">
  <p>Phrase strategique forte.</p>
  <div class="pull-source">Source</div>
</div>
```

Guillemet geant decoratif (pseudo-element), texte Display center, rupture de rythme visuel.

### Testimonial Card — photo + citation + nom/role

Classes : `.testimonial-grid`, `.testimonial`, `.testimonial-text`, `.testimonial-author`, `.testimonial-avatar`, `.testimonial-name`, `.testimonial-role`

```html
<div class="testimonial-grid">
  <div class="testimonial">
    <div class="testimonial-text">&laquo; Citation client. &raquo;</div>
    <div class="testimonial-author">
      <div class="testimonial-avatar">emoji</div>
      <div>
        <div class="testimonial-name">Prenom Nom</div>
        <div class="testimonial-role">Poste · Entreprise</div>
      </div>
    </div>
  </div>
</div>
```

Grille auto-fit (min 300px). Card avec hover scale. Avatar rond 40px.

---

## STRUCTURER

### Timeline — roadmap phases

Classes : `.timeline`, `.phase`, `.phase-1`, `.phase-2`, `.phase-3`, `.phase-tag`

```html
<div class="timeline">
  <div class="phase phase-1">
    <span class="phase-tag">M1 · M3</span>
    <h3>Titre</h3>
    <p>Description.</p>
    <ul><li>Action</li></ul>
  </div>
  <div class="phase phase-2">
    <span class="phase-tag">M3 · M6</span>
    <h3>Titre</h3>
    <p>Description.</p>
    <ul><li>Action</li></ul>
  </div>
  <div class="phase phase-3">
    <span class="phase-tag">M6 · M12</span>
    <h3>Titre</h3>
    <p>Description.</p>
    <ul><li>Action</li></ul>
  </div>
</div>
```

Grille 3 colonnes. Couleurs par phase : orange, magenta, violet (tag + bullets).

### Routine Grid — process en etapes numerotees

Classes : `.routine-grid`, `.routine-step`, `.routine-num`, `.routine-title`, `.routine-desc`

```html
<div class="routine-grid">
  <div class="routine-step">
    <div class="routine-num">01</div>
    <div class="routine-title">Titre</div>
    <div class="routine-desc">Description.</div>
  </div>
</div>
```

Grille 4 colonnes, separees par 2px gap. Numeros en gradient. Coins arrondis premier/dernier.

### Funnel — etapes connectees par des fleches

Classes : `.funnel`, `.funnel-step`, `.funnel-arrow`, `.funnel-icon`, `.funnel-value`, `.funnel-label`, `.funnel-sub`

```html
<div class="funnel">
  <div class="funnel-step">
    <div class="funnel-icon">emoji</div>
    <div class="funnel-value">12 700</div>
    <div class="funnel-label">Visites</div>
    <div class="funnel-sub">Sous-texte</div>
  </div>
  <div class="funnel-arrow">&rarr;</div>
  <div class="funnel-step">...</div>
</div>
```

Flex horizontal. Fleches orange entre les etapes. Passe en vertical sous 900px.

### Accordion — details cachees sous un resume cliquable

Classes : `.accordion`, `.accordion-item`, `.accordion-item.open`, `.accordion-trigger`, `.accordion-icon`, `.accordion-content`, `.accordion-body`

```html
<div class="accordion">
  <div class="accordion-item">
    <button class="accordion-trigger">
      Question ou titre
      <span class="accordion-icon">+</span>
    </button>
    <div class="accordion-content">
      <div class="accordion-body">Contenu cache.</div>
    </div>
  </div>
</div>
```

Le JS toggle `.open` sur l'item. L'icone "+" tourne a 45deg quand ouvert. Max-height anime a 500px.

---

## ALERTER

### Highlight Box — encadre avec bordure coloree

Classes : `.highlight-box` (orange par defaut), `.highlight-box.highlight-magenta`, `.highlight-box.highlight-violet`, `.highlight-box.highlight-gradient`

```html
<!-- Orange (strategique) -->
<div class="highlight-box">
  <strong>Notre lecture :</strong> interpretation.
</div>

<!-- Magenta (alerte) -->
<div class="highlight-box highlight-magenta">
  <strong>Point d'attention :</strong> risque.
</div>

<!-- Violet (conviction) -->
<div class="highlight-box highlight-violet">
  <strong>Notre conviction :</strong> position.
</div>

<!-- Gradient (conclusion forte) -->
<div class="highlight-box highlight-gradient">
  <strong>En synthese :</strong> conclusion.
</div>
```

Bordure gauche 3px coloree. Fond surface. Le gradient utilise `border-image`.

### Callout Banner — bandeau full-width avec fond gradient

Classes : `.callout-banner`

```html
<div class="callout-banner">
  <h3>Titre fort</h3>
  <p>Description.</p>
</div>
```

Deborde du conteneur (margin negatif 50vw). Fond gradient a 8% d'opacite. Rupture visuelle.

---

## COMPARER (suite)

### Constat-tension — deux KPIs opposes avec connecteur

Classes : `.constat-tension`, `.constat-tension-kpi`, `.constat-tension-connector`, `.constat-tension-proofs`, `.proof-pill`

```html
<div class="constat-tension">
  <div class="constat-tension-kpi positive">
    <div class="kpi-value">14 800</div>
    <div class="kpi-label">recherches/mois sur votre marque</div>
  </div>
  <div class="constat-tension-connector">pourtant</div>
  <div class="constat-tension-kpi negative">
    <div class="kpi-value">&lt; 1%</div>
    <div class="kpi-label">de visibilite hors-marque</div>
  </div>
  <div class="constat-tension-proofs">
    <span class="proof-pill">coffret biscuit : pos. 0</span>
    <span class="proof-pill">biscuit artisanal : pos. 0</span>
    <span class="proof-pill">cadeau gourmand : pos. 0</span>
  </div>
</div>
```

```css
.constat-tension {
  text-align: center;
  padding: 40px 0;
}
.constat-tension-kpi .kpi-value {
  font-size: 3rem; font-weight: 700;
  background: linear-gradient(90deg, var(--orange), var(--magenta));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.constat-tension-kpi .kpi-label {
  color: var(--text-70); font-size: 1rem; margin-top: 4px;
}
.constat-tension-connector {
  font-family: var(--font-display); font-size: 1.3rem;
  color: var(--text-50); margin: 16px 0; font-style: italic;
}
.constat-tension-proofs {
  display: flex; gap: 8px; justify-content: center;
  flex-wrap: wrap; margin-top: 20px;
}
.proof-pill {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-full); padding: 6px 14px;
  font-size: 0.85rem; color: var(--text-70);
}
```

Usage : quand `CONSTAT_MODE = tension` dans le NBP. Le paradoxe est l'argument principal (marque forte + invisible en Search). Ne pas utiliser si un seul KPI suffit (utiliser `.slide-constat` a la place).

---

## VENDRE

### Pricing Card — scenarios investissement

Classes : `.pricing-grid`, `.pricing`, `.pricing.recommended`, `.pricing-name`, `.pricing-price`, `.pricing-period`, `.pricing-scope`

```html
<div class="pricing-grid">
  <div class="pricing">
    <div class="pricing-name">Essentiel</div>
    <div class="pricing-price">X K&euro;</div>
    <div class="pricing-period">/mois HT</div>
    <div class="pricing-scope">
      <ul><li>Scope item</li></ul>
    </div>
  </div>
  <div class="pricing recommended">
    <div class="pricing-name">Performance</div>
    <div class="pricing-price">Y K&euro;</div>
    <div class="pricing-period">/mois HT</div>
    <div class="pricing-scope">
      <ul><li>Scope item</li></ul>
    </div>
  </div>
</div>
```

Grille 3 colonnes. `.recommended` ajoute une bordure gradient + badge "Recommande" en pseudo-element.

### ROI Simulator — sliders interactifs + calcul JS

Classes : `.sim-row`, `.sim-label`, `.sim-sub`, `.sim-slider`, `.sim-value`, `.sim-results`, `.sim-result`, `.sim-result-value`, `.sim-result-value.orange|.magenta|.violet`, `.sim-result-label`

```html
<!-- Slider -->
<div class="sim-row">
  <div><div class="sim-label">Label</div><div class="sim-sub">Sous-texte</div></div>
  <input type="range" class="sim-slider" id="sim-X" min="0" max="100" value="50">
  <div class="sim-value" id="val-X">50</div>
</div>

<!-- Resultats -->
<div class="sim-results">
  <div class="sim-result">
    <div class="sim-result-value orange" id="res-X">3 750</div>
    <div class="sim-result-label">Label</div>
  </div>
</div>
```

Grille 3 colonnes pour les sliders (label | range | valeur). Resultats en grille 3 colonnes. JS vanilla pour le calcul en temps reel.

### CTA — appel a l'action full-width avec blobs

Classes : `.cta-section`, `.cta-wrap`, `.cta-btn`

```html
<section class="cta-section">
  <div class="hero-blobs"><div class="hero-blob-3"></div></div>
  <h2>Titre CTA</h2>
  <p>Sous-texte.</p>
  <div class="cta-wrap">
    <a href="mailto:contact@slashr.fr" class="cta-btn">Verbe d'action</a>
  </div>
</section>
```

Full-height snap target. Blobs a 50% opacite. Bouton blanc avec bordure gradient au hover.

---

## CONTEXTUALISER

### Context Card — icone + titre + description

Classes : `.context-grid`, `.context-card`, `.context-icon`, `.context-body`

```html
<div class="context-grid">
  <div class="context-card">
    <div class="context-icon">emoji</div>
    <div class="context-body">
      <h3>Titre</h3>
      <p>Description avec <strong>donnees</strong>.</p>
    </div>
  </div>
</div>
```

Grille 2 colonnes. Icone ronde 48px fond orange subtil. Disposition horizontale (flex).

### Card — generique + variantes

Classes : `.card`, `.card.card-accent`, `.card.card-icon`, `.card-icon-circle`, `.card-icon-circle.orange|.magenta|.violet`

```html
<!-- Standard -->
<div class="card">
  <h3>Titre</h3>
  <p>Contenu.</p>
</div>

<!-- Accent (bordure top gradient) -->
<div class="card card-accent">
  <h3>Titre</h3>
  <p>Contenu.</p>
</div>

<!-- Icon (icone ronde en haut) -->
<div class="card card-icon">
  <div class="card-icon-circle orange">emoji</div>
  <h3>Titre</h3>
  <p>Contenu.</p>
</div>
```

Card de base polyvalente. `.card-accent` ajoute un top border gradient. `.card-icon` ajoute un cercle colore en en-tete.

### Quick Win Card — icone + titre + description + impact

Classes : `.qw-grid`, `.qw`, `.qw-icon`, `.qw-icon.orange|.magenta|.violet`, `.qw-impact`

```html
<div class="qw-grid">
  <div class="qw">
    <div class="qw-icon orange">emoji</div>
    <h3>Titre</h3>
    <p>Description.</p>
    <div class="qw-impact">Impact estime : +X</div>
  </div>
</div>
```

Grille 3 colonnes. Icone ronde coloree + texte d'impact en orange.

### Table — donnees structurees

Classes : `.table-wrap`, `tr.prospect`, `td.highlight`, `td.pos-good`, `td.pos-mid`, `td.pos-bad`

```html
<div class="table-wrap">
  <table>
    <thead><tr><th>Col 1</th><th>Col 2</th></tr></thead>
    <tbody>
      <tr class="prospect"><td>Prospect</td><td class="highlight">Valeur</td></tr>
      <tr><td>Autre</td><td class="pos-good">3</td></tr>
    </tbody>
  </table>
</div>
```

Container arrondi avec fond surface. `.prospect` = ligne mise en avant (fond orange subtil). Positions : `.pos-good` (vert), `.pos-mid` (orange), `.pos-bad` (gris).

### Tags — labels marque/generique

Classes : `.tag-brand`, `.tag-generic`

```html
<span class="tag-brand">Marque</span>
<span class="tag-generic">Generique</span>
```

Badges inline. `.tag-brand` = magenta, `.tag-generic` = violet.

---

## PROUVER

### Micro-benchmark — juxtaposition prospect vs cas client

Classes : `.micro-benchmark`, `.mb-step`, `.mb-step.mb-prospect`, `.mb-step.mb-before`, `.mb-step.mb-after`, `.mb-arrow`, `.mb-value`, `.mb-label`

```html
<div class="micro-benchmark">
  <div class="mb-step mb-prospect">
    <div class="mb-value">319</div>
    <div class="mb-label">LMP (vous)</div>
  </div>
  <div class="mb-arrow">&rarr;</div>
  <div class="mb-step mb-before">
    <div class="mb-value">412</div>
    <div class="mb-label">Cas client (avant)</div>
  </div>
  <div class="mb-arrow">&rarr;</div>
  <div class="mb-step mb-after">
    <div class="mb-value">5 643</div>
    <div class="mb-label">Cas client (apres)</div>
  </div>
</div>
```

**Style :**
- Flex horizontal, fleches orange entre les steps
- `.mb-prospect` : bordure orange, fond surface
- `.mb-before` : bordure grise, fond surface
- `.mb-after` : bordure verte, fond surface, valeur en vert
- Valeurs en gros (1.5rem, 700), labels en petit (0.85rem, text-70)
- Mobile : passe en vertical

**Usage :** bandeau en tete de chaque cas client dans l'onglet Cas Clients. Alimente par `sdb_juxtaposition` du SDB.

---

## Utility classes

Classes utilitaires pour eviter les inline styles repetes. Les patterns courants (margin, font-size, text-align) doivent utiliser ces classes.

```css
.mb-0{margin-bottom:0}.mb-sm{margin-bottom:8px}
.mb-md{margin-bottom:16px}.mb-lg{margin-bottom:24px}
.mb-xl{margin-bottom:40px}
.mt-md{margin-top:16px}.mt-lg{margin-top:24px}
.text-sm{font-size:13px}.text-xs{font-size:11px}
.text-center{text-align:center}
.max-w-700{max-width:700px}
```

Si un style inline est necessaire pour un cas unique, il est tolere. Mais les patterns repetes doivent etre des classes.

---

## Variables CSS de reference

```css
--orange: #E74601;
--orange-light: #FF9011;
--magenta: #CE08A9;
--violet: #8962FD;
--green: #4ade80;
--bg: #1a1a1a;
--surface: #2C2E34;
--surface-alt: #25272E;
--text: #ffffff;
--text-70: rgba(255,255,255,0.7);
--text-50: rgba(255,255,255,0.5);
--text-30: rgba(255,255,255,0.3);
--border: rgba(255,255,255,0.1);
--gradient: linear-gradient(90deg, #E74601, #CE08A9, #8962FD);
--font-display: "Funnel Display";
--font-body: "Inter";
--radius: 14px;
--radius-full: 9999px;
```

---

## Snippets standalone par categorie

> Chaque snippet est un mini-HTML copiable dans un fichier isole pour tester un composant sans ouvrir le monolithe `proposal-kit.html`.

### COMPARER — VS Block (test standalone)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
  :root { --orange:#E74601; --magenta:#CE08A9; --bg:#1a1a1a; --surface:#2C2E34; --text:#fff; --text-70:rgba(255,255,255,.7); --radius:14px; }
  body { background:var(--bg); color:var(--text); font-family:Inter,sans-serif; padding:40px; }
  .vs-grid { display:grid; grid-template-columns:1fr auto 1fr; gap:24px; align-items:center; }
  .vs-card { background:var(--surface); border-radius:var(--radius); padding:32px; text-align:center; }
  .vs-separator { font-size:1.5rem; color:var(--text-70); font-weight:700; }
  .vs-metric-value { font-size:2rem; font-weight:700; color:var(--orange); }
  .vs-metric-value.bad { color:var(--text-70); }
  .vs-metric-label { color:var(--text-70); font-size:.85rem; margin-top:4px; }
</style>
</head>
<body>
  <div class="vs-grid">
    <div class="vs-card"><h3>Prospect</h3><div class="vs-metric"><div class="vs-metric-value">1 250</div><div class="vs-metric-label">visites/mois</div></div></div>
    <div class="vs-separator">VS</div>
    <div class="vs-card"><h3>Concurrent</h3><div class="vs-metric"><div class="vs-metric-value bad">12 400</div><div class="vs-metric-label">visites/mois</div></div></div>
  </div>
</body>
</html>
```

### DIAGNOSTIQUER — S7 Card (test standalone)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
  :root { --orange:#E74601; --magenta:#CE08A9; --violet:#8962FD; --bg:#1a1a1a; --surface:#2C2E34; --text:#fff; --text-70:rgba(255,255,255,.7); --radius:14px; }
  body { background:var(--bg); color:var(--text); font-family:Inter,sans-serif; padding:40px; }
  .s7-card { background:var(--surface); border-radius:var(--radius); padding:24px; border-left:3px solid var(--orange); }
  .s7-card[data-state="primary"] { border-color:var(--orange); }
  .s7-card-header { display:flex; gap:8px; align-items:center; margin-bottom:12px; }
  .s7-card-id { font-weight:700; color:var(--orange); }
  .s7-badge { font-size:.75rem; padding:2px 8px; border-radius:9999px; }
  .s7-badge-primary { background:rgba(231,70,1,.15); color:var(--orange); }
  .s7-card-title { font-weight:600; margin-bottom:12px; }
  .s7-score-bar { background:rgba(255,255,255,.1); border-radius:4px; height:6px; }
  .s7-score-fill { background:var(--orange); height:100%; border-radius:4px; }
  .s7-score { display:flex; align-items:center; gap:8px; }
  .s7-score-value { font-size:.85rem; color:var(--text-70); }
  .s7-card-diagnostic { margin-top:12px; font-size:.9rem; color:var(--text-70); }
</style>
</head>
<body>
  <div class="s7-card" data-state="primary">
    <div class="s7-card-header"><span class="s7-card-id">S3</span><span class="s7-badge s7-badge-primary">Prioritaire</span></div>
    <div class="s7-card-title">Creation de contenu</div>
    <div class="s7-score"><div class="s7-score-bar" style="flex:1"><div class="s7-score-fill" style="width:20%"></div></div><span class="s7-score-value">1/5</span></div>
    <div class="s7-card-diagnostic">23 pages indexees sur 850 requetes pertinentes : couverture de 3%.</div>
  </div>
</body>
</html>
```

### QUANTIFIER — KPI Large + Slide Constat (test standalone)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
  :root { --orange:#E74601; --magenta:#CE08A9; --bg:#1a1a1a; --text:#fff; --text-70:rgba(255,255,255,.7); }
  body { background:var(--bg); color:var(--text); font-family:Inter,sans-serif; padding:40px; text-align:center; }
  .kpi-large { position:relative; }
  .kpi-large .kpi-value { font-size:4rem; font-weight:700; background:linear-gradient(90deg,var(--orange),var(--magenta)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
  .kpi-large .kpi-label { font-size:1.1rem; color:var(--text-70); margin-top:8px; }
  .constat-title { font-size:1.5rem; font-weight:600; margin-bottom:24px; }
  .constat-data { display:flex; gap:24px; justify-content:center; margin-top:24px; }
  .constat-data-item { color:var(--text-70); }
  .constat-data-item strong { color:var(--text); }
  .constat-source { color:var(--text-70); font-size:.8rem; margin-top:16px; }
</style>
</head>
<body>
  <h2 class="constat-title">14 800 recherches/mois sur votre marque. 0 client acquis via le Search generique.</h2>
  <div class="kpi-large"><div class="kpi-value">&lt; 1%</div><div class="kpi-label">de visibilite hors-marque</div></div>
  <div class="constat-data"><span class="constat-data-item"><strong>14 800</strong> recherches brandees</span><span class="constat-data-item"><strong>153</strong> mots-cles indexes</span></div>
  <p class="constat-source">Source : DataForSEO</p>
</body>
</html>
```

### VENDRE — Pricing Cards (test standalone)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
  :root { --orange:#E74601; --magenta:#CE08A9; --violet:#8962FD; --bg:#1a1a1a; --surface:#2C2E34; --text:#fff; --text-70:rgba(255,255,255,.7); --gradient:linear-gradient(90deg,#E74601,#CE08A9,#8962FD); --radius:14px; }
  body { background:var(--bg); color:var(--text); font-family:Inter,sans-serif; padding:40px; }
  .pricing-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:24px; }
  .pricing { background:var(--surface); border-radius:var(--radius); padding:32px; text-align:center; }
  .pricing.recommended { border:2px solid transparent; border-image:var(--gradient) 1; position:relative; }
  .pricing.recommended::before { content:"Recommande"; position:absolute; top:-12px; left:50%; transform:translateX(-50%); background:var(--gradient); color:#fff; padding:2px 12px; border-radius:9999px; font-size:.75rem; }
  .pricing-name { font-weight:700; font-size:1.1rem; margin-bottom:8px; }
  .pricing-price { font-size:2rem; font-weight:700; color:var(--orange); }
  .pricing-period { color:var(--text-70); font-size:.85rem; }
  .pricing-scope { text-align:left; margin-top:16px; }
  .pricing-scope li { color:var(--text-70); margin:4px 0; }
</style>
</head>
<body>
  <div class="pricing-grid">
    <div class="pricing"><div class="pricing-name">Essentiel</div><div class="pricing-price">2 500&euro;</div><div class="pricing-period">/mois HT</div><div class="pricing-scope"><ul><li>Pilotage + monitoring</li></ul></div></div>
    <div class="pricing recommended"><div class="pricing-name">Performance</div><div class="pricing-price">4 500&euro;</div><div class="pricing-period">/mois HT</div><div class="pricing-scope"><ul><li>+ production deleguee</li></ul></div></div>
    <div class="pricing"><div class="pricing-name">Croissance</div><div class="pricing-price">7 000&euro;</div><div class="pricing-period">/mois HT</div><div class="pricing-scope"><ul><li>+ multi-leviers</li></ul></div></div>
  </div>
</body>
</html>
```

### ALERTER — Highlight Boxes (test standalone)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
  :root { --orange:#E74601; --magenta:#CE08A9; --violet:#8962FD; --bg:#1a1a1a; --surface:#2C2E34; --text:#fff; --text-70:rgba(255,255,255,.7); --gradient:linear-gradient(90deg,#E74601,#CE08A9,#8962FD); --radius:14px; }
  body { background:var(--bg); color:var(--text); font-family:Inter,sans-serif; padding:40px; display:flex; flex-direction:column; gap:16px; }
  .highlight-box { background:var(--surface); border-radius:var(--radius); padding:20px 24px; border-left:3px solid var(--orange); }
  .highlight-magenta { border-color:var(--magenta); }
  .highlight-violet { border-color:var(--violet); }
  .highlight-gradient { border-image:var(--gradient) 1; border-left-width:3px; border-left-style:solid; }
</style>
</head>
<body>
  <div class="highlight-box"><strong>Concretement :</strong> interpretation strategique.</div>
  <div class="highlight-box highlight-magenta"><strong>Point d'attention :</strong> risque identifie.</div>
  <div class="highlight-box highlight-violet"><strong>Ce que les donnees montrent :</strong> position data-first.</div>
  <div class="highlight-box highlight-gradient"><strong>En synthese :</strong> conclusion forte.</div>
</body>
</html>
```
