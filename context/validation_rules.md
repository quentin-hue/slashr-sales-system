# Validation Rules — Proposition HTML

> Reference unique des 54 regles de validation. Utilisee par Pass 2 (tests pre-generation), Pass 3 (validation post-generation) et `tools/validate_proposal.py` (validation automatisee).

---

## Layer 1 : Structural (19 regles, PASS/FAIL)

Regles verifiables par DOM/CSS/regex. Echec = REJECT automatique.

| # | Regle | Test |
|---|-------|------|
| 3 | Fond sombre `#1a1a1a` present | CSS `background` ou `--bg` contient `#1a1a1a` |
| 5 | 4-6 onglets non-vides : `tab-diagnostic`, `tab-strategie`, `tab-investissement`, `tab-cas-clients` + optionnels `tab-contexte`, `tab-projet` | 4 a 6 `div.tab-content` avec contenu non-placeholder. Si `tab-contexte` present, positionne AVANT `tab-diagnostic`. Si `tab-projet` present, positionne entre `tab-strategie` et `tab-investissement` |
| 14 | Section S7 dans l'onglet Diagnostic | `s7-grid`, `s7-card`, `s7-radar-wrap` ou `s7-radar-svg` present dans `#tab-diagnostic` |
| 16 | Exactement 1 PRIMARY dans le S7 | 1 seul `data-state="primary"` ou `data-priority="primary"` dans `#tab-diagnostic` |
| 18 | Resume decisionnel <= 6 bullets | `.highlight-gradient` dans `#tab-investissement` avec max 6 `<li>` |
| 19 | Board-ready A4 / `window.print()` | `@media print` present dans le CSS ET bouton print dans le HTML ET section `.board-ready-a4` presente avec : resume decisionnel, pricing recommande, "decision attendue" |
| 26 | CTA avec verbe strategique | CTA ne contient PAS "Planifier un echange", "Discuter", "Echanger", "En savoir plus" |
| 29 | Zero jours/TJM/AMOA dans le texte visible | Regex `\b(jour[s]?[\s-]homme|TJM|AMOA|etude lexicale|plan de? redirections|recettage|recette fonctionnelle|phase de recette)\b` absent du body visible. NB : "monitoring" seul est autorise (cf. output_contract.md). "recette" culinaire est autorise (agroalimentaire). |
| 31 | Accordion FAQ present dans onglet Investissement | `.accordion` present dans `#tab-investissement` |
| 35 | "Prochaine etape" dans onglet Investissement | Texte "prochaine etape" (case-insensitive) dans `#tab-investissement` |
| 36 | Pas de pattern "Notre {X} :" | Regex `Notre (lecture|conviction|position|approche|methode|vision)\s*:` absent |
| 37 | Pas de structure anaphorique "Chaque mois/jour sans" | Regex `Chaque (mois|jour|semaine) sans` absent |
| 38 | Pricing cards exclusives a l'onglet Investissement | `.pricing` ou `.pricing-grid` absent de `#tab-strategie` |
| 39 | ETV vs trafic correctement etiquetes | "ETV" n'apparait pas la ou c'est du trafic (visites) et inversement |
| 27a | Si refonte : 3 actes narratifs + "0 perte de trafic strategique" | Conditionnel : si le deal implique une refonte |
| 28a | Investissement : 1 trajectoire recommandee + sous-bloc "cout de l'inaction" AVANT pricing | `.recommended` present + section cout inaction dans `#tab-investissement` + cout inaction (`.s7-insight`) positionne AVANT `.pricing`/`.pricing-grid` dans le DOM |
| 30 | Coherence levier : setup Phase 1 ↔ run Phase 2 | Chaque levier avec Phase 1 a un Phase 2 et inversement |
| 18b | Zero tiret cadratin et semi-cadratin separateur | Regex `\u2014` (em dash) et `\u2013` (en dash hors plages numeriques) absents du texte visible. Inclut `&mdash;` et `&ndash;` dans le HTML source |
| 50 | CTA H2 coherent avec la destination | Chaque lien `data-tab` dans un CTA a un H2 dont le texte mentionne l'onglet cible (ex: "Voir le projet" → `data-tab="projet"`, pas `data-tab="investissement"`) |
| 51 | Budget media mentionne dans le recap | Si `.pricing` ou `.pricing-grid` present, le texte "budget media" ou "budget média" (case-insensitive) apparait dans `#tab-investissement` |

---

## Layer 2 : Content (14 regles, WARN)

Regles verifiables par heuristiques. Echec = WARNING, correction recommandee.

| # | Regle | Test |
|---|-------|------|
| 20 | Trajectoire 90j decoupee M1/M2/M3 | Texte "M1", "M2", "M3" presents dans la section trajectoire |
| 22 | Section "Ce que cela implique" presente | Texte "ce que cela implique" (case-insensitive) dans `#tab-diagnostic` |
| 23 | "Nous recommandons" dans la decision | Texte "nous recommandons" present dans la section decision |
| 24 | Section "Decision strategique" presente | Texte "decision strategique" present dans `#tab-strategie` (ouvre l'onglet Strategie) |
| 25 | Sequence Diagnostic → S7 → Implications (tab-diagnostic) puis Decision → 90j (tab-strategie) | Les sections apparaissent dans cet ordre dans le DOM |
| 28b | Sous-bloc "Ce que coute l'inaction" avec impacts lies au diagnostic | Section cout inaction presente avec donnees chiffrees |
| 32 | Pricing cards avec "Ce que ca debloque" | Texte "ce que ca debloque" dans chaque `.pricing` card |
| 33 | Si Confidence Low : label "Recommandation conditionnelle" | Conditionnel : label present sur `.recommended` si applicable |
| 34 | Board-ready A4 contient "Decision attendue" | Texte "decision attendue" dans la section print |
| 8 | Pas 2 blocs data consecutifs sans interpretation | Alternance data/highlight-box verifiee |
| 9 | Pas de section "Pourquoi SLASHR" standalone | Regex `pourquoi slashr` absent des titres h2/h3 |
| 10 | Differenciateurs lies a un data block | Transitions SLASHR precedees par un bloc de donnees |
| 28c | Brief paid non adresse | Si des keywords paid (google ads, sea, paid, campagne, roas) apparaissent dans le Diagnostic mais pas dans Strategie/Investissement → WARN "Brief paid mentionne dans Diagnostic mais non adresse dans Strategie/Investissement" |
| 46 | Section contexte presente | Texte "ce que nous avons compris" OU "votre situation" (case-insensitive) dans `#tab-diagnostic`, positionne avant le premier bar chart / constat | WARN si absente |
| 47 | Deduplication onglet Strategie | Nombre de `.slide` dans `#tab-strategie` <= 5 (hors hero et CTA). Au-dela → WARN "Onglet Strategie sur-dense, verifier la deduplication" | <= 5 slides |
| 48 | Densite slide (ecran unique) | Aucun `.slide` ne contient plus de 2 composants visuels (`.bar-chart` + `.donut-chart` + `table` + `.grid-2`/`.grid-3` avec > 4 enfants). Au-dela → WARN "Slide sur-dense, decouper" | Max 2 composants visuels par slide |
| 49 | Plan 90j contextuel | Si REFONTE mentionnee dans `#tab-diagnostic`, la timeline M1/M2/M3 dans `#tab-strategie` doit contenir "refonte" OU "migration" OU "accompagnement". WARN si plan generique malgre refonte | Coherence contexte/plan |
| 52 | Budget recap en slide dedie | Le recap budget global (total 2 ans ou annuel) doit etre dans son propre `.slide`, pas inline dans un slide pricing. WARN si le recap est dans le meme slide qu'un `.pricing-grid` | Slide dedie |
| 53 | Objectif phase associe au budget | Chaque phase dans le recap budget doit mentionner un objectif qualitatif (ex: "fondations", "accelerer", "CA"). WARN si budget sans objectif | Objectif visible |

---

## Layer 3 : Semantic (10 regles, checklist LLM)

Regles non-automatisables, revue par l'agent. Affichees comme checklist.

| # | Regle | Question de validation |
|---|-------|----------------------|
| 1 | Test de substitution | Chaque section echoue-t-elle au test de substitution ? (specifique a CE prospect) |
| 2 | Chiffres sources | Chaque chiffre a-t-il une source identifiable ? |
| 4 | Ton partenaire strategique | Le ton est-il partenaire (ni arrogant, ni suppliant, ni jargonneux) ? |
| 6 | ROI avec hypotheses sourcees | Le ROI utilise-t-il uniquement des hypotheses sourcees ? |
| 7 | Arc narratif justifie | L'ordre des sections est-il justifie par le contexte du deal ? |
| 11 | Zero pression commerciale | Aucune phrase type "ne manquez pas", "il est urgent de" ? |
| 12 | Zero dramatisation | Aucune phrase type "catastrophe", "crise", "vous perdez tout" ? |
| 13 | S7 : max 3 leviers | Le S7 recommande-t-il max 3 leviers (pas les 7) ? |
| 15 | Insight S7 non-substituable | L'insight central echoue-t-il au test de substitution ? |
| 17 | DEFERRED justifies | Chaque force DEFERRED a-t-elle un "pourquoi pas maintenant" ? |
| 17b | Brief paid adresse | Si SEA_SIGNAL=EXPLICIT dans le SDB, le brief paid est-il adresse dans la proposition (section Diagnostic paid + sous-section Strategie paid + FAQ SEA) ? |
| 17c | Opportunite paid exposee | Si SEA_SIGNAL=OPPORTUNITY dans le SDB, l'opportunite paid est-elle visible dans le diagnostic (CPCs, couverture concurrents) et integree dans la trajectoire Phase 2 ? |

---

## Layer 4 : Quality Metrics (6 regles, WARN)

Metriques de qualite redactionnelle mesurables automatiquement. Echec = WARNING avec score.

| # | Regle | Test | Seuil |
|---|-------|------|-------|
| 40 | Densite de donnees dans l'onglet Diagnostic | Ratio paragraphes contenant ≥ 1 chiffre / total paragraphes dans `#tab-diagnostic` | ≥ 50% des paragraphes |
| 41 | Specificite des titres h2 | % de `h2` dans `#tab-diagnostic` contenant un nom propre OU un chiffre | ≥ 60% des h2 |
| 42 | Triplet "Ce que cela implique" | Section "Ce que cela implique" contient exactement 3 items (`.highlight-box` OU `<li>`), le 3e contient un chiffre (projection). Scope au slide : le comptage s'arrete quand un nouveau `.slide` commence. | 3 items, chiffre dans le 3e |
| 43 | SO WHAT : chaque section Diagnostic a un highlight-box | Chaque `.slide` dans `#tab-diagnostic` contient au moins 1 `.highlight-box` | Toutes les sections |
| 44 | Au moins 1 micro-benchmark dans la proposition | `.micro-benchmark` present dans `#tab-diagnostic` OU `#tab-cas-clients` | ≥ 1 |
| 45 | Repetition density : aucun nombre n'apparait > 6 fois dans le texte visible | Counter sur les nombres multi-digits, seuil > 6 | Aucun nombre > 6x |

---

## Utilisation par passe

| Passe | Utilisation |
|-------|-----------|
| **Pass 2** (Narrative Architect) | Appliquer Layer 3 en entier + Layer 2 regles 22-25 comme checklist pre-generation |
| **Pass 3** (Design Orchestrator) | Appliquer les 4 layers comme gate de validation. Layer 1 FAIL = REJECT |
| **`validate_proposal.py`** | Automatise Layer 1 (PASS/FAIL) + Layer 2 (WARN) + Layer 4 (Quality Metrics). Layer 3 affichee comme checklist manuelle. Mode `--nbp` : pre-validation de la structure du NBP (7 checks) |
