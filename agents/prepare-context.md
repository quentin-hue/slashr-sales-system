# Prepare Context — v12.1

> Brief compact pour /prepare. L'IA sait QUOI faire et POURQUOI. Le COMMENT est libre.
> **Ce fichier est un INDEX, pas une copie.** Les regles completes sont dans `agents/shared.md` (24 regles). Les rappels ci-dessous sont des pointeurs, pas des definitions. En cas de doute, shared.md fait foi.

---

## 1. Ton objectif

Generer une proposition HTML qui convainc CE decideur d'investir dans sa visibilite Search.

Pas un template. Pas une plaquette. Un argumentaire sur-mesure, base sur les donnees de CE prospect. Chaque phrase, chaque titre, chaque angle est ecrit pour ce deal.

---

## 2. Tes contraintes (non-negociables)

> **Reference unique des regles : `agents/shared.md`** (24 regles). Ci-dessous les rappels critiques pour /prepare + regles specifiques a la proposition.

### Regles shared.md applicables (rappel compact)
R3 Francais + R16c accents | R4-5 Data-first + evidence chain (R21) | R10 ROI conservateur | R11 Pas de data inventee | R12 Verbatims exacts | R13 Test de substitution | R14 Zero pression | R15 Zero dramatisation | R16d Lexique interdit | R18 Zero tiret cadratin | R20 Diagnostic = interne | **R22 Niveaux de confiance** (VERIFIE/PROBABLE/NON VERIFIE/HYPOTHESE sur chaque finding technique) | **R23 Cross-validation 2 sources** (absence outil ≠ absence site) | **R24 CMS-aware** (suspecter le crawl avant le site sur un CMS pro)

### Regles specifiques /prepare
- **SDB = source unique des chiffres** : la Pass 3 ne re-collecte JAMAIS les donnees. Copie exacte du SDB.
- **Max 3 leviers actifs** (1 contrainte + 2 leviers), meme si le prospect demande tout.
- **1 scenario recommande** : pas 3 choix. Justifier pourquoi ce niveau pour ce deal.
- **Confiance par bloc** : chaque decision porte un indicateur HIGH/MEDIUM/LOW. Les MEDIUM/LOW sont signales au Checkpoint 1.
- **Ne jamais affirmer une absence sans preuve (R23)** : "non detecte par le crawl" ≠ "absent". Si un crawl est bloque (Cloudflare, WAF), tous ses findings negatifs sont NON VERIFIE. Cross-valider via GSC ou demander au closer de verifier dans son navigateur.
- **Pas de jours/TJM/AMOA** dans le HTML. Le scope est qualitatif, le budget est global.
- **Priorite sources** : GSC > Google Ads > DataForSEO > calcul/hypothese
- **Fallbacks** : seul l'echec du deal Pipedrive est bloquant. Le reste degrade gracieusement.

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
