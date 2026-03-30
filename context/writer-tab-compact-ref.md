# Writer Tab — Reference compacte CSS

> Ce fichier est le seul fichier CSS que les writer-tab agents doivent lire.
> Il remplace la lecture de proposal-kit-reference.md (trop long) pour les subagents.

## Composants essentiels

### Layout
- `.slide` : section plein ecran, scroll-snap. Max 1 composant visuel + 1 highlight-box.
- `.hero` : intro full-width avec `.hero-blobs > .hero-blob-3`, `.hero-tag`, `h1`, `.hero-subtitle`, `.hero-context`, `.hero-date`, `.hero-scroll` (onclick obligatoire)
- `.section` + `.section-label` (max 4 mots) + `h2` (max 8 mots) + `.section-intro`
- `.grid-2`, `.grid-3` : grilles responsive (1 col < 900px)

### Cards
- `.card` avec `border-top: 3px solid var(--orange/magenta/violet)` et `padding: 24px`
- INTERDIT : `.card-accent`, `.card-icon`
- Labels : `<p>` en uppercase 0.75rem avec couleur accent

### Data
- `.chart-container` > `.bar-row` > `.bar-label` + `.bar-track` > `.bar-fill.orange/.muted` + `.bar-value`
- `.kpi-row` > `.kpi-card` > `.kpi-value` + `.kpi-label`
- `.highlight-box` (SO WHAT, 3 lignes max). Variantes : `.highlight-gradient`, `.highlight-magenta`, `.highlight-violet`

### Pricing
- `.pricing` + `.pricing.recommended` : cards prix. `.pricing-name`, `.pricing-price`, `.pricing-period`, `.pricing-scope`
- `.accordion` > `.accordion-item` > `.accordion-trigger` + `.accordion-content` > `.accordion-body`

### Navigation
- `.timeline` > `.phase` > `.phase-tag` + `h3` + contenu
- `.before-after` > `.ba-panel.before` + `.ba-arrow` + `.ba-panel.after`
- `.cta-section` avec `.hero-blobs` + `h2` + `.cta-wrap` > `.cta-btn`
- `.progress-dots` > `.progress-dot` (gere par le skeleton JS)

### Utilitaires
- `.mb-sm` (8px), `.mb-md` (16px), `.mb-lg` (24px), `.mt-lg` (24px)
- `.text-sm` (13px), `.text-xs` (11px), `.text-center`
- `.max-w-700`

## Couleurs (variables CSS)
- `var(--orange)` #E74601, `var(--magenta)` #CE08A9, `var(--violet)` #8962FD
- `var(--bg)` #1a1a1a, `var(--surface)` #2C2E34
- `var(--text-70)` rgba(255,255,255,0.7), `var(--text-50)` 0.5, `var(--text-30)` 0.3
- `var(--border)` rgba(255,255,255,0.1)

## Typo
- Titres display : `var(--font-display)` = Funnel Display
- Corps : Inter
- h2 : `clamp(28px, 5vw, 45px)`, font-weight 700
