# Mode PREPARE : Proposition interactive (v11.0)

> **Prerequis :** `agents/shared.md` lu. Le deal doit avoir ete qualifie (`/qualify`).

---

## Objectif

Collecter toutes les donnees, analyser le deal en profondeur, et generer une proposition HTML interactive sur-mesure. **Un seul fichier HTML uploade dans Drive.**

Le HTML n'est pas un template a trous. C'est un livrable genere par l'agent, chaque phrase, chaque titre, chaque angle est ecrit pour CE prospect, base sur CETTE analyse.

---

## Architecture interne : 3 passes sequentielles

L'agent execute 3 passes en sequence. Chaque passe produit un document intermediaire structure (interne, jamais dans l'output). La passe suivante consomme ce document comme input principal.

```
Pass 1 : DATA & STRATEGY ENGINE    → Structured Data Brief (SDB)
Pass 2 : NARRATIVE ARCHITECT        → Narrative Blueprint (NBP)
Pass 3 : DESIGN ORCHESTRATOR        → HTML final (le seul output)
```

**Pourquoi 3 passes ?** Separer les preoccupations. La Pass 1 ne pense pas a la narration. La Pass 2 ne pense pas aux composants visuels. La Pass 3 ne reinvente pas la strategie. Chaque passe fait une chose et la fait bien.

> **Note :** La Pass 1 inclut le pipeline S7 (Etape 1.4) qui produit un `strategy_plan_internal.md` avant le SDB. Le S7 est l'etape de priorisation strategique, il alimente directement le SDB.

---



---

## Cadre qualite global (/prepare)

Objectif : maximiser la qualite d'analyse tout en restant adaptatif au contexte du deal.

Regles transverses :
- **Faits / Hypotheses / Manquants** structure le raisonnement (Pass1 + Pass2) puis un resume en Pass3.
- **Evidence Gate (leger)** : reco structurante = rattachee a un fait OU assumee comme hypothese (confiance + validation).
- **Contradiction check + Quality Rubric** executes en fin de Pass3 (cf `context/output_contract.md`).

Ce cadre n'impose pas quoi conclure ; il impose seulement la lisibilite, la preuve, et l'honnetete du raisonnement.

## Execution deterministe (performance / fiabilite)

**Performance Budget :** `context/performance_budget.md`

### Cache & replay (obligatoire)
- Toutes les reponses API doivent etre stockees sous `.cache/deals/{deal_id}/...`
- Si cache < 24h : reutiliser (ne pas re-fetch)
- Ecrire les artefacts internes inter-pass :
  - `.cache/deals/{deal_id}/artifacts/SDB.md`
  - `.cache/deals/{deal_id}/artifacts/NBP.md`

**But :**
- Rejouer Pass 2 / Pass 3 sans re-collecter
- Debugger rapidement un deal (evidence log)


## Execution

Lire et executer chaque passe dans l'ordre :

### Pass 1 : DATA & STRATEGY ENGINE
**Fichier :** `agents/prepare-pass1.md`

Collecte (10 modules) + structuration + analyse strategique + diagnostic S7.
Outputs internes : `strategy_plan_internal.md` puis **Structured Data Brief (SDB)**.

### Pass 2 : NARRATIVE ARCHITECT
**Fichier :** `agents/prepare-pass2.md`

Plan narratif complet a partir du SDB. Choix du hook, de l'arc emotionnel, planification des 4 onglets (Diagnostic, Strategie, Investissement, Cas clients).
Output interne : **Narrative Blueprint (NBP)**.

**Pre-validation NBP (OBLIGATOIRE, gate bloquante) :** Apres la Pass 2, executer :
```bash
python3 tools/validate_proposal.py --nbp .cache/deals/{deal_id}/artifacts/NBP.md
```
- **Exit 0** : structure OK, passer a la Pass 3.
- **Exit 1-3** : problemes structurels. Corriger le NBP et re-valider avant de lancer la Pass 3. Ne PAS sauter cette etape.

### Pass 3 : DESIGN ORCHESTRATOR
**Fichier :** `agents/prepare-pass3.md`

Generation HTML a partir du NBP. Mapping composants par role narratif, regles de composition, validation.
Output : **HTML final** (le seul livrable visible) + **INTERNAL-S7** (diagnostic interne).

---

## References

- Kit composants (30 composants, catalogue par role narratif) : `templates/proposal-kit.html`
- Design system : `context/design_system.md`
- Positionnement + structure offre : `context/positioning.md`
- Modele S7 : `context/s7_search_operating_model.md`
- Cas clients : `context/case_studies.md`
- Pricing : `context/pricing_rules.md`
- Frontiere client/interne : `context/output_contract.md`
- Field keys Pipedrive : `context/pipedrive_reference.md`
