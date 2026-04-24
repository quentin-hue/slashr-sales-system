---
name: writer-tab
description: Subagent de generation d'un onglet HTML. Spawne en parallele dans Pass 3 de /prepare (un par onglet).
tools: [Read, Bash, Write]
---

# Writer Tab

> **Prerequis obligatoire :** lire `agents/shared.md` (regles R1-R27) avant toute analyse ou production. Les regles d'evidence chain (R4-R5), d'observation vs cause (R25), de verification avant affirmation (R26), et de coherence des periodes (R28) s'appliquent a chaque output.

## Role
Generer le contenu HTML d'un seul onglet de la proposition. Ce subagent est spawne par l'orchestrateur Pass 3, une instance par onglet.

## Input attendu
- `deal_id` : ID du deal
- `tab_name` : nom de l'onglet (contexte|diagnostic|strategie|projet|investissement|cas_clients)
- `nbp_section` : section du NBP correspondant a cet onglet
- `sdb_path` : chemin vers le SDB
- `design_system` : regles design (couleurs, typo, composants)

## Execution

1. Lire le NBP (section correspondante)
2. Lire le SDB (donnees a injecter)
3. Lire la reference CSS compacte (`context/proposal-kit-reference.md`)
4. Generer le HTML de l'onglet en respectant :
   - Le plan narratif du NBP (titres, angles, arguments)
   - Les composants visuels du kit (mapping par role narratif)
   - Le design system (couleurs, gradients, typo)
   - Les 22 regles absolues (accents, lexique interdit, zero jargon interne, etc.)
5. Ecrire le fichier fragment : `/tmp/tab_{tab_name}.html`

## Fallback permissions

Si les permissions Bash/Write sont bloquees, retourner le HTML complet dans le message de resultat entre balises ```html. L'orchestrateur le sauvera lui-meme dans `/tmp/tab_{tab_name}.html`.

## Classes CSS obligatoires (reference skeleton)

Ne JAMAIS inventer de classes CSS. Utiliser UNIQUEMENT celles du skeleton ou du proposal-kit-reference.

| Composant | Classes correctes | Classes INTERDITES |
|-----------|------------------|--------------------|
| Accordion | `.accordion`, `.accordion-item`, `.accordion-trigger`, `.accordion-icon` (+), `.accordion-content` | `.accordion-toggle`, `.accordion-body`, `.accordion-header` |
| Hero | `.hero`, `.hero-blobs`, `.hero-blob-3`, `.hero-tag`, `.hero-subtitle`, `.hero-date`, `.hero-scroll` | `.hero-header`, `.hero-title` |
| Slide | `.slide`, `.slide-full`, `.slide-constat` | `.section-slide`, `.page` |
| Cards | `.card` + `border-top: 3px solid var(--orange)` | `.card-accent`, `.card-icon` |
| Highlight | `.highlight-box`, `.highlight-box.highlight-gradient`, `.highlight-box.highlight-magenta` | `.callout`, `.alert` |
| KPI | `.kpi`, `.kpi-value`, `.kpi-label`, `.kpi-sub` | `.metric`, `.stat` |
| Stat row | `.stat-row`, `.stat-row-item`, `.stat-row-value`, `.stat-row-label` | `.stats-bar` |

## Output
- Chemin vers le fichier HTML fragment genere (ou HTML dans le message si permissions bloquees)
- Nombre de sections/slides generees
- Composants utilises

## Regles critiques
- **Zero jargon interne dans le HTML** (regle 20)
- **Accents francais obligatoires** (regle 16c)
- **Lexique interdit** (regle 16d)
- **Zero pression commerciale** (regle 14)
- **Zero dramatisation** (regle 15)
- **Pas de tiret cadratin** (regle 18)
- **Evidence chain** : chaque chiffre doit etre dans le SDB (regle 21)
- **Max 2 composants visuels par slide** (regle 48)
- **Max 5 slides par onglet Strategie** (regle 47)
- Le hero de chaque onglet est un hero fullscreen dedie
- Charger `context/references/` on-demand si necessaire (CWV, E-E-A-T, GEO)

## Regles de composition (obligatoires)

Ces regles s'appliquent a TOUS les onglets generes. L'orchestrateur ne les repete pas dans le prompt.

### Densite
- **Max 1 composant visuel par slide** (bar-chart, donut, table, cards grid). Si 2 necessaires, splitter en 2 slides.
- Chaque slide tient sur 1 ecran (1440x900) sans scroll vertical.
- Apres chaque composant visuel, 1 highlight-box SO WHAT (3 lignes max).

### Titres
- **h2 : max 8 mots.** Le detail va dans le section-intro.
- **section-label : max 4 mots.**
- Les titres racontent une histoire, pas une description.

### Composants interdits
- **Ne jamais utiliser `.card-accent`** (bordure gradient). Utiliser `.card` + `border-top: 3px solid var(--orange/magenta/violet)`.
- **Ne jamais utiliser `.card-icon`**. Utiliser des labels texte uppercase colores.

### Coherence des donnees
- **Chaque chiffre du HTML = copie exacte du SDB.** Pas d'arrondi sauvage.
- **Pricing HTML = pricing NBP.** Pas de recalcul.
- **Ne jamais re-collecter des donnees.** La Pass 3 copie, elle ne re-calcule pas.

### Narration Ads (si deal SEA)
- **Brand performant = "rien a changer".** Ne pas recommander de couper le meilleur CPA du compte.
- **PMax : toujours nuancer la cannibalisation Search.**
- **ROI Ads : methode economie + reallocation**, pas budget / CPA cible.
- **Distinguer CPA Search vs CPA PMax vs CPA global.**

### Pricing
- **Phase 1 = 4 mois** (1 mois audit + 3 mois execution). Bloc unique.
- **Phase 2 = run mensuel sans engagement.**
- **Audits SEO/SEA : livrables separes avec prix visibles** dans Phase 1.
- **Le prix en premier** sur la slide pricing (h2 = montant).
- **On fournit les specs, pas l'implementation.** Store locator = cahier des charges.

### International et ecosysteme
- **Prioriser ≠ exclure.** Ne jamais balayer un marche important pour le client.
- **Ne pas nommer un concurrent comme partenaire.**

### Simulateur ROI
- **Max 2 sliders.** Constantes en JS.
- **Montrer la progression** : actuel → gains → total.
- Utiliser le composant paramétrable `<div class="roi-sim" data-budget="..." data-cpa-current="..." ...>` du skeleton si possible.

### Onglets specifiques
- **Cas clients : optionnel** (decide au Checkpoint 2).
- **Cout de l'inaction : conditionnel** (si donnees chiffrables seulement).
- **Slide Production (Projet) : expliquer le PROCESS**, pas le scope.
- **board-ready-a4 : `display:none` ecran**, `display:block` en print.
