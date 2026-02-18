# SLASHR — Design System v1.0

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

### 3.2 Hero Gradient (3 blobs floutes)

Fond de section hero : trois ellipses colorees positionnees en bas, tres floutees, sur fond `#1a1a1a`.

- **Blob Orange** : bas gauche, 50% largeur, blur 100px
- **Blob Magenta** : centre bas, 70% largeur, blur 100px
- **Blob Violet** : bas droite, 50% largeur, blur 175px

> **Pour reproduire sur un autre support :** Placer 3 cercles flous en bas du visuel (orange a gauche, magenta au centre, violet a droite) sur fond `#1a1a1a`. Les cercles debordent du cadre.

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
| **Heading** | `clamp(28px, 5vw, 45px)` | 700 | 110% | -0.04em | Inter | Titres de section h2 |
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

**Primary (blanc sur fond sombre) :**
- Fond : `#ffffff`, Texte : `#2C2E34`
- Padding : 30px horizontal x 15px vertical
- Border-radius : full (pill)
- Hover : bordure gradient brand (2px)

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
- Hover : bordure gradient brand

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
