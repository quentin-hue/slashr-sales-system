# Validation Rules — Proposition HTML

> Reference unique des 39 regles de validation. Utilisee par Pass 2 (tests pre-generation), Pass 3 (validation post-generation) et `tools/validate_proposal.py` (validation automatisee).

---

## Layer 1 : Structural (17 regles, PASS/FAIL)

Regles verifiables par DOM/CSS/regex. Echec = REJECT automatique.

| # | Regle | Test |
|---|-------|------|
| 3 | Fond sombre `#1a1a1a` present | CSS `background` ou `--bg` contient `#1a1a1a` |
| 5 | 4 onglets non-vides : `tab-strategie`, `tab-cas-clients`, `tab-roi`, `tab-livrables` | 4 `div.tab-content` avec contenu non-placeholder |
| 14 | Section S7 dans l'onglet Strategie | `s7-grid` ou `s7-card` present dans `#tab-strategie` |
| 16 | Exactement 1 PRIMARY dans le S7 | 1 seul `data-state="primary"` dans la section S7 |
| 18 | Resume decisionnel <= 6 bullets | `.highlight-gradient` dans `#tab-livrables` avec max 6 `<li>` |
| 19 | Board-ready A4 / `window.print()` | `@media print` present dans le CSS ET bouton print dans le HTML |
| 26 | CTA avec verbe strategique | CTA ne contient PAS "Planifier un echange", "Discuter", "Echanger", "En savoir plus" |
| 29 | Zero jours/TJM/AMOA dans le texte visible | Regex `\b(jour[s]?[\s-]homme|TJM|AMOA|etude lexicale|plan de? redirections|recette)\b` absent du body visible. NB : "monitoring" seul est autorise (cf. output_contract.md) |
| 31 | Accordion FAQ present dans onglet Livrables | `.accordion` present dans `#tab-livrables` |
| 35 | "Prochaine etape" dans onglet Livrables | Texte "prochaine etape" (case-insensitive) dans `#tab-livrables` |
| 36 | Pas de pattern "Notre {X} :" | Regex `Notre (lecture|conviction|position|approche|methode|vision)\s*:` absent |
| 37 | Pas de structure anaphorique "Chaque mois/jour sans" | Regex `Chaque (mois|jour|semaine) sans` absent |
| 38 | Pricing cards exclusives a l'onglet Livrables | `.pricing` ou `.pricing-grid` absent de `#tab-roi` |
| 39 | ETV vs trafic correctement etiquetes | "ETV" n'apparait pas la ou c'est du trafic (visites) et inversement |
| 27a | Si refonte : 3 actes narratifs + "0 perte de trafic strategique" | Conditionnel : si le deal implique une refonte |
| 28a | Investissement : 1 trajectoire recommandee + sous-bloc "cout de l'inaction" | `.recommended` present + section cout inaction dans `#tab-livrables` |
| 30 | Coherence levier : setup Phase 1 ↔ run Phase 2 | Chaque levier avec Phase 1 a un Phase 2 et inversement |

---

## Layer 2 : Content (12 regles, WARN)

Regles verifiables par heuristiques. Echec = WARNING, correction recommandee.

| # | Regle | Test |
|---|-------|------|
| 20 | Trajectoire 90j decoupee M1/M2/M3 | Texte "M1", "M2", "M3" presents dans la section trajectoire |
| 22 | Section "Ce que cela implique" presente | Texte "ce que cela implique" (case-insensitive) dans `#tab-strategie` |
| 23 | "Nous recommandons" dans la decision | Texte "nous recommandons" present dans la section decision |
| 24 | Section "Decision strategique" presente | Texte "decision strategique" present dans `#tab-strategie` |
| 25 | Sequence Diagnostic → S7 → Implications → Decision → 90j | Les sections apparaissent dans cet ordre dans le DOM |
| 28b | Sous-bloc "Ce que coute l'inaction" avec impacts lies au diagnostic | Section cout inaction presente avec donnees chiffrees |
| 32 | Pricing cards avec "Ce que ca debloque" | Texte "ce que ca debloque" dans chaque `.pricing` card |
| 33 | Si Confidence Low : label "Recommandation conditionnelle" | Conditionnel : label present sur `.recommended` si applicable |
| 34 | Board-ready A4 contient "Decision attendue" | Texte "decision attendue" dans la section print |
| 8 | Pas 2 blocs data consecutifs sans interpretation | Alternance data/highlight-box verifiee |
| 9 | Pas de section "Pourquoi SLASHR" standalone | Regex `pourquoi slashr` absent des titres h2/h3 |
| 10 | Differenciateurs lies a un data block | Transitions SLASHR precedees par un bloc de donnees |

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

---

## Utilisation par passe

| Passe | Utilisation |
|-------|-----------|
| **Pass 2** (Narrative Architect) | Appliquer Layer 3 en entier + Layer 2 regles 22-25 comme checklist pre-generation |
| **Pass 3** (Design Orchestrator) | Appliquer les 3 layers comme gate de validation. Layer 1 FAIL = REJECT |
| **`validate_proposal.py`** | Automatise Layer 1 (PASS/FAIL) + Layer 2 (WARN). Layer 3 affichee comme checklist manuelle |
