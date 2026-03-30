# SLASHR — Design System v2.0

> Document de reference pour l'identite visuelle Slashr.
> Utilisable pour tous les supports : site web, reseaux sociaux, presentations, print.

---

## 1. Principes visuels

| Principe | Description |
|----------|-------------|
| **Dark-first** | Fond sombre `#1a1a1a` comme base. Le contenu respire sur du noir. |
| **Gradients fluides** | Trois couleurs accent (orange, magenta, violet) utilisees en blobs floutes, jamais en aplat. |
| **Typographie display** | Titres en Funnel Display, grands, serres (`letter-spacing` negatif). Impact immediat. |
| **Sobriete** | Peu d'elements decoratifs. Le texte blanc sur fond sombre suffit. Les gradients sont en arriere-plan, jamais agressifs. |
| **Premium** | Micro-interactions soignees, bordures subtiles (white/10), effets holographiques au survol. |

---

## 2. Couleurs

### 2.1 Palette principale (accent)

| Nom | Hex | RGB | Usage |
|-----|-----|-----|-------|
| **Orange** | `#E74601` | 231, 70, 1 | Accent primaire, gradients, hover, CTA |
| **Magenta** | `#CE08A9` | 206, 8, 169 | Accent secondaire, gradients |
| **Violet** | `#8962FD` | 137, 98, 253 | Accent tertiaire, gradients |

### 2.2 Variantes accent

| Nom | Hex | Usage |
|-----|-----|-------|
| Orange clair | `#FF9011` | Stop de gradient |
| Orange alt | `#FF7828` | Variante hover |
| Magenta alt | `#CE16B5` | Stop de gradient |
| Violet clair | `#AD21FE` | Stop de gradient |

### 2.3 Neutres

| Nom | Hex | Usage |
|-----|-----|-------|
| **Fond page** | `#1a1a1a` | Background global |
| **Surface / Carte** | `#2C2E34` | Cards, tags, inputs |
| Surface alt | `#25272E` | Variante carte (case studies) |
| Surface hover | `#3a3d47` | Avatars, hover states |
| Surface icon | `#353535` | Icones sociales hover |

### 2.4 Texte (sur fond sombre)

| Opacite | Valeur CSS | Usage |
|---------|------------|-------|
| 100% | `#ffffff` | Titres, texte principal |
| 90% | `rgba(255,255,255,0.9)` | Descriptions, sous-titres |
| 70% | `rgba(255,255,255,0.7)` | Texte secondaire, muted |
| 50% | `rgba(255,255,255,0.5)` | Texte tertiaire |

### 2.5 Bordures

| Opacite | Valeur CSS | Usage |
|---------|------------|-------|
| 10% | `border-white/10` | Cartes, separations subtiles |
| 15% | `border-white/15` | Articles |
| 20% | `border-white/20` | Hover cartes |
| 30% | `border-white/30` | Navigation, elements interactifs |

---

## 3. Gradients

### 3.1 Gradient Brand (signature)

```
Direction : gauche -> droite (90deg)
#E74601 -> #CE08A9 -> #8962FD
```

### 3.2 Hero Gradient (3 blobs floutes — V2)

Fond de section hero : trois ellipses avec **gradients bicolores**, positionnees en bas, tres floutees, sur fond `#1a1a1a`. Technique GPU-optimized.

| Couche | Position | Taille | Gradient | Blur |
|--------|----------|--------|----------|------|
| Orange (::before) | `left:-15%, bottom:-10%` | 50% x 50% | `linear-gradient(239.24deg, #E74601 43.16%, #FF9011 70.85%)` | 100px |
| Magenta (::after) | `left:20%, bottom:0%` | 70% x 45% | `linear-gradient(239.24deg, #CE08A9 43.16%, #CE16B5 70.85%)` | 100px |
| Violet (div) | `right:-10%, bottom:-5%` | 50% x 55% | `linear-gradient(180deg, #8962FD 0%, #AD21FE 100%)` | 175px |

**Optimisation GPU :** Chaque blob utilise `transform: translateZ(0)` et `backface-visibility: hidden`.

**Z-index :** Blobs en `z-index: 1`, contenu texte en `z-index: 10`. Exclure les blobs du selecteur generique via `.hero > *:not(.hero-blobs):not(.hero-blob-3)`.

**Border-radius :** Le hero a des coins arrondis en bas : `border-radius: 0 0 40px 40px` (mobile), `0 0 75px 75px` (desktop >= 900px).

**Centrage :** `height: 100vh`, `padding-top: 56px` (compense la nav fixe), `justify-content: center`.

> **Pour reproduire :** Placer 3 cercles flous avec gradients bicolores en bas du visuel sur fond `#1a1a1a`. Les cercles debordent du cadre. Utiliser le meme angle (239.24deg) pour orange et magenta, 180deg pour violet.

### 3.3 Gradient Texte

Appliquer le gradient brand sur du texte (titres display).

### 3.4 Gradient Border anime (Snake)

Bordure animee avec un segment de gradient qui tourne. Utilise sur les CTA principaux.

---

## 4. Typographie

### 4.1 Familles de polices

| Police | Role | Source |
|--------|------|--------|
| **Funnel Display** | Titres display (h1 hero, grandes accroches) | Google Fonts |
| **Inter** | Corps de texte, UI, boutons, descriptions, headings h2/h3 | Google Fonts |

> **Note :** Geist Sans (Vercel) etait utilise sur le site web SLASHR. Pour les propositions HTML generees, **Inter** est la police body de reference car disponible sur Google Fonts sans CDN externe.

### 4.2 Echelle typographique

| Nom | Taille | Poids | Line-height | Letter-spacing | Police | Usage |
|-----|--------|-------|-------------|----------------|--------|-------|
| **Display XL** | `clamp(40px, 8vw, 90px)` | 600 | 95% | -0.03em | Funnel Display | Hero h1 |
| **Display L** | `clamp(36px, 7vw, 72px)` | 600 | 95% | -0.03em | Funnel Display | Service hero h1 |
| **Heading** | `clamp(28px, 5vw, 45px)` | 700 | 110% | -0.04em | Funnel Display (proposals) / Inter (UI) | Titres de section h2 |
| **Title** | 20px | 700 | 130% | -0.01em | Inter | Titres de cartes h3 |
| **Subtitle** | `clamp(14px, 2.5vw, 18.75px)` | 600 | 130% | -0.01em | Inter | Sous-titres hero |
| **Body** | 15px | 400 | 145% | 0 | Inter | Texte courant |
| **Small / Tag** | 11.25px | 700 | 140% | -0.01em | Inter | Tags, badges, labels |

### 4.3 Polices alternatives (presentations)

Si Funnel Display n'est pas disponible :

| Originale | Alternative Google | Alternative systeme |
|-----------|--------------------|--------------------|
| Funnel Display | Sora, DM Sans | -- |
| Inter | -- | SF Pro (macOS), Segoe UI (Windows) |

---

## 5. Espacement

### 5.1 Echelle de base

L'unite de base est **7.5px**. Tous les espacements sont des multiples :

| Token | Valeur | Usage courant |
|-------|--------|---------------|
| `space-1` | 7.5px | Intra-composant |
| `space-2` | 15px | Entre elements proches |
| `space-4` | 30px | Entre elements moyens |
| `space-8` | 60px | Entre blocs majeurs |

### 5.2 Conteneurs (largeurs max)

| Token | Valeur | Usage |
|-------|--------|-------|
| `max-w-content` | 1280px | Conteneur principal (slides, nav-inner, grilles) |
| `max-w-text` | 680px | Blocs de texte (section-intro, paragraphes longs) |

> **Note :** Equivalent Tailwind `max-w-7xl`. Toutes les proposals HTML utilisent `max-width: 1280px` comme largeur de reference.

### 5.3 Sections (proposals HTML)

Les proposals utilisent un systeme **scroll-snap slide-by-slide** :

| Element | Padding | Notes |
|---------|---------|-------|
| Section standard (inside .slide) | `padding: 0` | Pas de padding propre, le `.slide` gere l'espacement |
| Slide | `padding: 60px 30px` | Centrage vertical via flexbox |
| Hero | `padding: 30px` | Full-width, blobs gradient |
| CTA section | `padding: 100px 30px` | Full-width, blobs gradient |

---

## 6. Rayons de bordure

| Token | Valeur | Usage |
|-------|--------|-------|
| `radius-sm` | 11px | Inputs |
| `radius-md` | 14-15px | Cartes, FAQ |
| `radius-lg` | 37.5px | Boutons secondaires |
| `radius-full` | 50% / 9999px | Boutons CTA, tags, pills |

---

## 7. Composants cles

### 7.1 Boutons

**Primary / CTA (blanc, border gradient au hover) :**
- Fond : `#ffffff`, Texte : `#1a1a1a`
- Padding : 14px vertical x 40px horizontal
- Border-radius : full (pill)
- Technique : wrapper `.cta-wrap` avec `padding: 2px` et `background: transparent`
- Hover : le wrapper passe a `background: var(--gradient)` — cree une bordure gradient de 2px
- Transition : 300ms

**Secondary (bordure blanche) :**
- Fond : transparent, Bordure : 1px solid white
- Texte : `#ffffff`
- Hover : fond white/10

**CTA gradient :**
- Fond : gradient `#E74601` -> `#CE08A9`
- Texte : blanc
- Border-radius : full

### 7.2 Cartes

- Fond : `#2C2E34`
- Border-radius : 14-15px
- Padding : 24-32px
- Bordure : 1px white/10
- Hover : `border-color: white/20` + `transform: scale(1.02)`
- Transition : `border-color 0.3s, transform 0.3s`
- **Pas de box-shadow** : la profondeur est geree par blur/opacity, pas par des ombres
- Variante gradient border : wrapper technique (meme principe que CTA wrap)

### 7.3 Tags / Badges

- Fond : `#2C2E34`
- Texte : blanc, 12px, uppercase, tracking-wider
- Padding : px-3 py-1.5
- Border-radius : full

---

## 8. Application aux presentations (Google Slides / PPT)

### Fond de slide

- Couleur : `#1a1a1a`
- Optionnel : ajouter les blobs gradient en bas (image de fond)

### Couleurs de slide

| Element | Couleur |
|---------|---------|
| Fond | `#1a1a1a` |
| Titre | `#ffffff` |
| Corps de texte | `rgba(255,255,255,0.7)` |
| Accent / highlight | `#E74601` |
| Accent secondaire | `#CE08A9` |
| Ligne de separation | `rgba(255,255,255,0.1)` |

### Regles de composition pour les slides R2

1. **Fond sombre obligatoire** : `#1a1a1a` sur toutes les slides
2. **Titres en blanc pur** : `#ffffff`, gras, equivalent Funnel Display ou Sora
3. **Corps en blanc attenue** : `rgba(255,255,255,0.7)` pour la lisibilite
4. **Accent orange** : `#E74601` pour les chiffres cles, KPI, donnees impactantes
5. **Accent magenta** : `#CE08A9` pour les elements secondaires, liens, highlights
6. **Tableaux** : fond `#2C2E34`, bordures `white/10`, texte blanc
7. **Pas de fond blanc** : jamais de slide blanche. Le dark-first est non-negociable
8. **Gradient en arriere-plan** : les 3 blobs (orange/magenta/violet) en bas de la slide de couverture et de la slide de cloture
9. **Sobriete** : 3-4 bullets max par slide. Le vide est un choix
10. **Tag SLASHR** : "Slashr -- Agence SEO & Search Marketing" en petit tag discret (11px, uppercase) sur la slide de couverture

---

## 9. Recap rapide

### Couleurs a retenir

```
Orange     #E74601
Magenta    #CE08A9
Violet     #8962FD
Fond       #1a1a1a
Surface    #2C2E34
Texte      #ffffff
```

### Gradient signature

```
#E74601 -> #CE08A9 -> #8962FD
```

### Polices a retenir

```
Titres display : Funnel Display (600-700)
Corps / UI     : Inter (400-700)
Fallback       : SF Pro / Segoe UI / Sora
```

### Espacements cles

```
Base  : 7.5px
x2    : 15px
x4    : 30px
x8    : 60px
```

---

## 10. Interactions & Animations (V2)

### 10.1 Transitions

| Element | Proprietes | Duree | Easing |
|---------|-----------|-------|--------|
| Cartes (card, kpi, testimonial, diagnostic-card) | `border-color, transform` | 300ms | ease (defaut) |
| Pricing cards | `border-color, transform` | 300ms | ease |
| Boutons CTA | `background` (wrapper) | 300ms | ease |
| Nav tabs | `all` | 200ms | ease |

### 10.2 Hover effects

| Element | Effet |
|---------|-------|
| Cartes generiques | `border-color: white/20` + `transform: scale(1.02)` |
| KPI cards | `border-color: white/20` + `transform: scale(1.02)` |
| Testimonials | `border-color: white/20` + `transform: scale(1.02)` |
| Diagnostic cards | `border-color: white/20` + `transform: scale(1.02)` |
| Pricing cards | `transform: scale(1.02)` |
| CTA button | Wrapper passe de `transparent` a `var(--gradient)` (bordure gradient 2px) |

> **Regle : pas de `translateY` ni de `box-shadow`.** L'elevation se fait par `scale(1.02)` uniquement. La profondeur visuelle est geree par blur/opacity sur les gradients, pas par des ombres portees.

### 10.3 Scroll-snap (proposals HTML)

```
html        → height: 100%
body        → height: 100%; overflow: hidden
.main       → height: calc(100vh - 56px); margin-top: 56px; overflow: hidden
.tab-content → scroll-snap-type: y proximity; overflow-y: auto
.slide       → min-height: calc(100vh - 56px); scroll-snap-align: start
.hero        → scroll-snap-align: start
.cta-section → scroll-snap-align: start
```

> **`proximity` et non `mandatory`** : permet aux sliders interactifs (ROI) de fonctionner sans blocage.

### 10.4 Profondeur

La profondeur est obtenue **exclusivement** par :
- Blur sur les gradient blobs (`filter: blur(100-175px)`)
- Opacity sur les bordures (`white/10` → `white/20` au hover)
- Scale subtil au hover (`1.02`)
- Backdrop blur sur la nav (`blur(20px)`)

**Jamais de `box-shadow`** sur les composants.

---

## 11. Board-ready A4 — Spec print layout

Le board-ready A4 est une version imprimable de la proposition, destinee aux comites de direction. Accessible via un bouton "Version imprimable" dans l'onglet Investissement.

### 11.1 Contenu obligatoire (1 page A4)

| Ordre | Element | Source | Contrainte |
|-------|---------|--------|------------|
| 1 | En-tete | Design system | Logo SLASHR (petit, discret) + nom prospect + date |
| 2 | Insight central | Diagnostic du SDB | 1 phrase, en gras, centree |
| 3 | Resume decisionnel | diagnostic du SDB | 6 bullets max, numerotes |
| 4 | Diagnostic visuel | Onglet Strategie | Version niveaux de gris, labels + scores, pas de couleur |
| 5 | ROI en 1 ligne | Onglet ROI | "ROI conservateur : x{N_bas} sur {periode}" |
| 6 | Pricing recommande | Onglet Livrables | Scenario recommande uniquement : Phase 1 + Phase 2/mois |
| 7 | Decision attendue | NBP | Encadre : {scenario} + {date cible} + {prochaine etape} |
| 8 | CTA | NBP | 1 ligne : "Prochaine etape : {action datee}" |

### 11.2 Hierarchie typographique print

| Element | Taille | Poids | Couleur |
|---------|--------|-------|---------|
| Nom prospect | 18pt | 700 | `#1a1a1a` |
| Insight central | 14pt | 700 | `#1a1a1a` |
| Resume bullets | 10pt | 400 | `#333333` |
| Radar labels | 9pt | 600 | `#555555` |
| ROI / Pricing | 11pt | 600 | `#1a1a1a` |
| Decision attendue | 11pt | 700 | `#E74601` (accent) |
| Footer | 8pt | 400 | `#999999` |

### 11.3 Elements masques en print

```css
@media print {
  /* Masquer */
  .nav, .tab-nav, .cta-section, .slider-container,
  .accordion, .faq, .hero-blobs, .hero-blob-3,
  .btn-print, footer, .scroll-indicator { display: none !important; }

  /* Forcer fond blanc */
  body, .main, .tab-content, .slide { background: #ffffff !important; color: #1a1a1a !important; }

  /* Forcer 1 page */
  .board-ready-a4 { page-break-after: always; max-height: 100vh; overflow: hidden; }
}
```

### 11.4 Regles

- **1 page maximum** — si ca depasse, reduire les bullets (4 au lieu de 6) ou le radar
- **Lisible en noir et blanc** — tout doit fonctionner sans couleur (impression N&B)
- **Autonome** — un decideur qui ne lit QUE cette page comprend le probleme, la solution et l'investissement
- **Pas de gradient, pas de blob, pas d'animation** — c'est un document professionnel sobre
