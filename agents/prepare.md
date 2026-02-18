# Mode PREPARE — Proposition interactive (v11.0)

> **Prerequis :** `agents/shared.md` lu. Le deal doit avoir ete qualifie (`/qualify`).

---

## Objectif

Collecter toutes les donnees, analyser le deal en profondeur, et generer une proposition HTML interactive sur-mesure. **Un seul fichier HTML uploade dans Drive.**

Le HTML n'est pas un template a trous. C'est un livrable genere par l'agent — chaque phrase, chaque titre, chaque angle est ecrit pour CE prospect, base sur CETTE analyse.

---

## Architecture interne : 3 passes sequentielles

L'agent execute 3 passes en sequence. Chaque passe produit un document intermediaire structure (interne, jamais dans l'output). La passe suivante consomme ce document comme input principal.

```
Pass 1 — DATA & STRATEGY ENGINE    → Structured Data Brief (SDB)
Pass 2 — NARRATIVE ARCHITECT        → Narrative Blueprint (NBP)
Pass 3 — DESIGN ORCHESTRATOR        → HTML final (le seul output)
```

**Pourquoi 3 passes ?** Separer les preoccupations. La Pass 1 ne pense pas a la narration. La Pass 2 ne pense pas aux composants visuels. La Pass 3 ne reinvente pas la strategie. Chaque passe fait une chose et la fait bien.

> **Note :** La Pass 1 inclut le pipeline S7 (Etape 1.4) qui produit un `strategy_plan_internal.md` avant le SDB. Le S7 est l'etape de priorisation strategique — il alimente directement le SDB.

---

## Execution

Lire et executer chaque passe dans l'ordre :

### Pass 1 — DATA & STRATEGY ENGINE
**Fichier :** `agents/prepare-pass1.md`

Collecte (10 modules) + structuration + analyse strategique + diagnostic S7.
Outputs internes : `strategy_plan_internal.md` puis **Structured Data Brief (SDB)**.

### Pass 2 — NARRATIVE ARCHITECT
**Fichier :** `agents/prepare-pass2.md`

Plan narratif complet a partir du SDB. Choix du hook, de l'arc emotionnel, planification des 4 onglets MVP.
Output interne : **Narrative Blueprint (NBP)**.

### Pass 3 — DESIGN ORCHESTRATOR
**Fichier :** `agents/prepare-pass3.md`

Generation HTML a partir du NBP. Mapping composants par role narratif, regles de composition, validation.
Output : **HTML final** (le seul livrable visible) + **INTERNAL-S7** (diagnostic interne).

---

## References

- Kit composants (27 composants, catalogue par role narratif) : `templates/proposal-kit.html`
- Design system : `context/design_system.md`
- Positionnement + structure offre : `context/positioning.md`
- Modele S7 : `context/s7_search_operating_model.md`
- Cas clients : `context/case_studies.md`
- Pricing : `context/pricing_rules.md`
- Frontiere client/interne : `context/output_contract.md`
- Field keys Pipedrive : `context/pipedrive_reference.md`
