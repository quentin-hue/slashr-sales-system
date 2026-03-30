# Prepare Context — v12.0

> Brief compact pour /prepare. L'IA sait QUOI faire et POURQUOI. Le COMMENT est libre.

---

## 1. Ton objectif

Generer une proposition HTML qui convainc CE decideur d'investir dans sa visibilite Search.

Pas un template. Pas une plaquette. Un argumentaire sur-mesure, base sur les donnees de CE prospect. Chaque phrase, chaque titre, chaque angle est ecrit pour ce deal.

---

## 2. Tes contraintes (non-negociables)

### Contenu
- **Evidence chain** : chaque chiffre source (API + date + periode dans le SDB). Pas de source → pas dans le HTML.
- **SDB = source unique des chiffres** : la Pass 3 ne re-collecte JAMAIS les donnees. Elle copie les chiffres du SDB. Si le SDB dit 15 676 EUR, le HTML dit 15 676 EUR. Pas d'arrondi sauvage, pas de re-calcul.
- **Diagnostic = interne** : les labels d'arbitrage (contrainte, leviers, confiance) ne sortent JAMAIS dans le HTML. Traduire en langage business.
- **Max 3 leviers actifs** (1 contrainte + 2 leviers), meme si le prospect demande tout.
- **1 scenario recommande** : pas 3 choix. Justifier pourquoi ce niveau pour ce deal.
- **Zero pression commerciale** : pas de "ne manquez pas", "il est urgent de", "derniere chance", "chaque mois sans".
- **Zero dramatisation** : pas de "catastrophe", "crise", "vous perdez tout". Les donnees suffisent.
- **Test de substitution** : si une phrase fonctionne pour n'importe quel prospect, la reecrire.
- **Verbatims = citations exactes** entre guillemets.
- **ROI conservateur** : CTR reels > estimes. Fourchette, pas valeur unique. Methode dans `context/references/roi-methodology.md`.
- **Confiance par bloc** : chaque decision (contrainte, leviers, ROI, scenario) porte un indicateur HIGH/MEDIUM/LOW. Les blocs MEDIUM/LOW sont signales au Checkpoint 1 pour review.
- **Ne jamais affirmer une absence sans preuve** : "pas de CTA", "pas de pages locales", "pas de schema" demandent un crawl. "Les pages locales sous-performent" demande des donnees GSC. Le diagnostic ne contient que des constats verifiables, pas des hypotheses deguisees en faits.

### Forme
- **Francais** avec accents obligatoires (stratégie, données, référence, résultat, etc.)
- **Lexique interdit** : thin content, maillage, netlinking, KPIs, Schema, LLM, cluster, R1/R2. Remplacements dans `agents/shared.md` regle 16d.
- **Zero tiret cadratin/semi-cadratin** separateur. Remplacer par `:`, `,`, `.`, parentheses.
- **Pas de jours/TJM/AMOA** dans le HTML. Le scope est qualitatif, le budget est global.

### Priorite des sources
```
GSC (donnees reelles) > Google Ads (donnees reelles) > DataForSEO (estimations) > calcul/hypothese
```

### Fallbacks
Seul l'echec du deal Pipedrive est bloquant. Le reste degrade gracieusement.

---

## 3. Tes outils

| Outil | Fichier | Usage |
|-------|---------|-------|
| Kit composants (30) | `templates/proposal-kit.html` | Catalogue par role narratif |
| CSS reference | `context/proposal-kit-reference.md` | Aide-memoire classes |
| Squelette HTML | `templates/proposal-skeleton.html` | Boilerplate (CSS, JS, nav) |
| Assembleur | `tools/build_proposal.py` | Skeleton + tabs → HTML final |
| Validateur | `tools/validate_proposal.py` | 54 regles, 4 layers (HARD/SOFT) |
| Design system | `context/design_system.md` | Couleurs, typo, gradients |
| Plateforme de marque | `context/brand_platform.md` | ADN, positionnement, valeurs SLASHR |
| Tone of Voice | `context/tone_of_voice.md` | Registre, voix, principes redactionnels |
| Cas clients | `context/case_studies.md` | Bibliotheque de cas |
| Pricing | `context/pricing_rules.md` | TJM, jours, formules |
| Output contract | `context/output_contract.md` | Frontiere client/interne |
| References on-demand | `context/references/` | CWV, E-E-A-T, GEO, arcs, ROI |
| **Checklist d'analyse** | `context/references/analysis-checklist.md` | **Questions a repondre AVANT de diagnostiquer** |
| Debrief warnings | `.cache/debrief_warnings.md` | Patterns des deals precedents |

---

## 4. Le flux (3 passes, 2 checkpoints)

```
Pass 1 : Collecter → Checklist d'analyse → Diagnostiquer → SDB
  CHECKPOINT 1 : closer valide strategie
Pass 2 : Construire le plan narratif → NBP
  CHECKPOINT 2 : closer valide narration
Pass 3 : Generer le HTML → PROPOSAL
```

Chaque passe a son fichier de spec : `agents/prepare-pass1.md`, `prepare-pass2.md`, `prepare-pass3.md`.

---

## 5. Ce que tu decides librement

- Le hook d'ouverture (invente, pas un menu)
- L'arc narratif du Diagnostic (nombre de sections, ordre, contenu)
- Les composants visuels (choisis dans le kit, pas mappes par une table)
- Le ton (module par TONE_PROFILE : DIRECT, PEDAGOGIQUE, PROVOCATEUR, TECHNIQUE)
- Les cas clients (par angle strategique, pas juste par secteur)
- La structure du simulateur ROI (inputs adaptes aux donnees reelles du deal)
- Les onglets custom (propose au Checkpoint 2, le closer valide)
- La confiance par bloc (HIGH/MEDIUM/LOW sur chaque decision, visible aux checkpoints)
