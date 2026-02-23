# Output Contract — v1.0

> Ce fichier definit ce qui est visible dans chaque output et ce qui reste interne.

---

## Principe general

Deux niveaux d'information :
1. **CLIENT** — ce que le prospect voit (HTML proposition)
2. **INTERNE** — ce que le closer voit (INTERNAL-S7, terminal)

La frontiere est stricte. Aucune information INTERNE ne doit fuiter dans un output CLIENT.

---

## Output CLIENT : Proposition HTML

### Section Investissement — Phase 1

| Visible | Invisible |
|---------|-----------|
| Nom de la mission ("Mission structurante") | Nombre de jours |
| Ce que ca inclut (scope qualitatif) | TJM |
| Budget global EUR HT | Decomposition jours par bloc |
| Livrables produits | Sous-composants (etude lexicale, AMOA, etc.) |

**Formulation type Phase 1 :**
```
"La Phase 1 est une mission structurante de {duree qualitative} qui pose les fondations de votre strategie Search."

Inclut :
→ Audit SEO complet (diagnostic, benchmark, opportunites)
→ Accompagnement refonte SEO (si applicable)
→ {Levier additionnel} (si applicable)

Budget : {montant} EUR HT
```

Les termes "5 jours", "4 jours", "TJM", "jour-homme" sont INTERDITS dans le HTML.

### Section Investissement — Phase 2

| Visible | Invisible |
|---------|-----------|
| Nom du niveau ("Essentiel", "Performance", "Croissance") | Nombre de jours/mois |
| Ce que ca inclut (scope qualitatif) | TJM |
| Budget mensuel EUR HT | Calcul jours x TJM |
| Engagement (duree) | Incompressibles par levier |

**Formulation type Phase 2 :**
```
"L'accompagnement mensuel assure le pilotage, la production et le monitoring de votre visibilite Search."

Essentiel : {budget}/mois — pilotage + monitoring
Performance : {budget}/mois — + production deleguee
Croissance : {budget}/mois — + multi-leviers
```

### Section ROI (onglet ROI Interactif)

| Visible | Invisible |
|---------|-----------|
| Hypotheses sourcees (tableau) | Formule de calcul TJM |
| Simulateur interactif | Marges SLASHR |
| Scenarios pricing (lien vers investissement) | Detail interne des jours |

---

## Output INTERNE : INTERNAL-S7

### Section "Budget interne" (NOUVELLE — ajoutee en fin de fichier S7)

```markdown
## Budget interne (CONFIDENTIEL — closer uniquement)

### Phase 1 — Detail jours

| Bloc | Jours | Justification |
|------|-------|---------------|
| Audit SEO | 5 | Standard |
| Refonte SEO | {X} | {volumetrie : X URLs} |
| Activation contenu | 1 | Standard |
| {Levier optionnel} | {X} | {justification} |
| **TOTAL** | **{somme}** | **{somme} x TJM = {budget} EUR HT** |

### Phase 2 — Detail mensuel

| Levier | Jours/mois | Justification |
|--------|-----------|---------------|
| SEO run | {X} | {intensite + scope} |
| {Levier optionnel} run | {X} | {scope} |
| **TOTAL** | **{somme}** | **{somme} x TJM = {budget} EUR/mois HT** |

### Scenarios

| Scenario | Phase 1 | Phase 2/mois | Total annuel |
|----------|---------|-------------|-------------|
| Essentiel | {budget} | {budget} | {calcul} |
| Performance | {budget} | {budget} | {calcul} |
| Croissance | {budget} | {budget} | {calcul} |
```

---

## Regles de coherence

1. `budget_phase1_html == jours_phase1_interne x TJM` (cf. `context/pricing_rules.md`) — toujours
2. `budget_mensuel_html == jours_mensuels_interne x TJM` (cf. `context/pricing_rules.md`) — toujours
3. Le total annuel affiche dans la synthese = Phase 1 + (Phase 2 x 12)
4. Si un levier est active en Phase 1 setup, il DOIT avoir un run en Phase 2
5. Si un levier n'a PAS de setup Phase 1, il ne peut PAS avoir de run Phase 2

---

## Quality Rubric (auto-controle obligatoire)

Avant de sortir le livrable final, appliquer ce rubric (0/1 par item) et corriger si besoin.

1) Objectifs business clairs et priorises (pas seulement SEO)
2) Recommandations reliees explicitement aux objectifs
3) Faits vs hypotheses clairement distingues
4) Points manquants explicites + plan B (proxy / assumptions / next access)
5) Concurrence / marche : au moins 3 insights actionnables
6) Plan 30/60/90 realiste (priorites + dependances)
7) KPIs & mesure : comment on prouve le progres (et avec quelles sources)
8) Budget/charge/coherence : la recommandation colle au budget annonce

**Sortie attendue :**
- Score: X/8
- 3 corrections max appliquees avant publication
- Si score < 6/8 : re-travailler la structure, pas juste ajouter du contenu

---

## Contradiction check (anti-incoherences)

Verifier et corriger toute contradiction de type :
- Budget faible vs plan trop large
- Objectif "conversion" mais actions uniquement "contenu"
- Delais ambitieux sans prerequis (tracking, accès, dev)
- Recos qui contredisent les contraintes (CMS, ressources, gouvernance)
- "GEO/IA" annonce mais aucune action concrete associee

Regle : si une contradiction reste, elle doit etre explicitement justifiee (trade-off assume).

