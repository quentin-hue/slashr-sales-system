# Mode PREPARE : Proposition interactive (v12.0)

> **Prerequis :** `agents/shared.md` lu.

---

## Objectif

Collecter toutes les donnees, analyser le deal en profondeur, et generer une proposition HTML interactive sur-mesure. **Un seul fichier HTML uploade dans Drive.**

Le HTML n'est pas un template a trous. C'est un livrable genere par l'agent, chaque phrase, chaque titre, chaque angle est ecrit pour CE prospect, base sur CETTE analyse.

---

## Architecture interne : 3 passes + 2 checkpoints

L'agent execute 3 passes en sequence avec **2 checkpoints interactifs** ou le closer valide avant de continuer.

```
Pass 1 : DATA & STRATEGY ENGINE    → Structured Data Brief (SDB)
  ↓
CHECKPOINT 1 : Resume strategique dans le terminal → closer valide / corrige / reoriente
  ↓
Pass 2 : NARRATIVE ARCHITECT        → Narrative Blueprint (NBP)
  ↓
CHECKPOINT 2 : Plan narratif dans le terminal → closer reordonne / renomme / ajoute / supprime
  ↓
Pass 3 : DESIGN ORCHESTRATOR        → HTML final (le seul output)
```

**Pourquoi les checkpoints ?** Sans validation intermediaire, une erreur en Pass 1 (mauvaise priorisation, donnee manquante) cascade dans les Pass 2 et 3. Le closer decouvre le probleme dans le HTML final et doit tout reprendre. Les checkpoints coupent cette cascade : le closer valide la strategie AVANT la narration, et le plan narratif AVANT la generation HTML.

> **Note :** La Pass 1 inclut le diagnostic strategique (Etape 1.3) qui alimente directement le SDB. Le diagnostic est interne, il ne sort JAMAIS dans le HTML client (cf. regle 20).

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

### Debrief warnings (retroaction active)
Si `.cache/debrief_warnings.md` existe, le lire AVANT la Pass 2. Ce fichier contient des patterns identifies par les debriefs precedents (arcs qui sous-performent, objections recurrentes, ajustements pricing). L'integrer dans le choix narratif.

### Donnees /audit et /benchmark
Si `.cache/deals/{deal_id}/audit.md` ou `benchmark.md` existent, les reutiliser pour accelerer la Pass 1 (donnees deja collectees).

### References on-demand
Les subagents chargent les references techniques (`context/references/`) uniquement quand le contexte du deal l'exige. Pas de chargement systematique.

## Execution

Lire et executer chaque passe dans l'ordre, avec les 2 checkpoints interactifs.

### Pass 1 : DATA & STRATEGY ENGINE
**Fichier :** `agents/prepare-pass1.md`

Collecte (10 modules) + structuration + analyse strategique + diagnostic interne (Etape 1.3).
Output interne : **Structured Data Brief (SDB)** (inclut le diagnostic strategique).

> **Mode `--fast`** : si le flag `--fast` est present et qu'un SDB frais (< 2h) existe, cette passe est entierement skippee. L'agent passe directement au Checkpoint 1 avec le SDB existant.

### Si un NBP existe deja (re-run)

Si `.cache/deals/{deal_id}/artifacts/NBP.md` existe deja :
1. La Pass 1 genere le nouveau SDB normalement (re-collecte)
2. **Comparer le nouveau SDB avec les donnees cles du NBP existant :**
   - Le budget Ads a-t-il change de plus de 10% ?
   - Le nombre de conversions a-t-il change de plus de 20% ?
   - De nouvelles campagnes ou de nouveaux centres sont apparus ?
   - Le diagnostic (contrainte + leviers) est-il toujours valide ?
3. **Si les donnees sont stables** (ecarts < 10-20%) : presenter au Checkpoint 1, mentionner "NBP existant toujours valide", proposer de passer directement en Pass 3.
4. **Si les donnees ont significativement change** : signaler au Checkpoint 1 "Les donnees ont change depuis le dernier NBP", lister les ecarts, et recommander de refaire la Pass 2.

Le closer decide : garder le NBP existant ou le refaire.

### CHECKPOINT 1 : Validation strategique (OBLIGATOIRE)

Apres la Pass 1, presenter au closer un **resume strategique compact** dans le terminal. Format :

```
=== CHECKPOINT 1 : VALIDATION STRATEGIQUE ===

PROSPECT : {nom} | {secteur} | {contexte}

DONNEES CLES :
1. {donnee 1 — chiffre + source}
2. {donnee 2 — chiffre + source}
3. {donnee 3 — chiffre + source}
4. {donnee 4 — chiffre + source}
5. {donnee 5 — chiffre + source}

DIAGNOSTIC :                                    CONFIANCE
- Contrainte : {en langage business}             {HIGH/MEDIUM/LOW}
- Levier 1 : {en langage business}               {HIGH/MEDIUM/LOW}
- Levier 2 : {en langage business}               {HIGH/MEDIUM/LOW}
- Ce qu'on ne fait pas : {et pourquoi}

STRATEGIE :
- Perimetre : {SEO seul / SEO + Refonte / etc.}
- Scenario : {nom} ({budget}/mois)                {HIGH/MEDIUM/LOW}
- Phase 1 : {scope en 1 ligne}
- Phase 2 : {scope en 1 ligne}
- ROI : {fourchette} (methode {A/B/C})            {HIGH/MEDIUM/LOW}

MANQUANTS :
- {donnee manquante 1 — impact + plan B}
- {donnee manquante 2 — impact + plan B}

SOURCES :
- GSC : {disponible / non}
- Google Ads : {disponible / non}
- DataForSEO : {N appels}
- Drive : {N fichiers}

CONFIANCE GLOBALE : {HIGH/MEDIUM/LOW} — {N} decisions sures, {N} a valider
→ Les blocs MEDIUM/LOW meritent ton attention. Le reste est fonde sur des donnees reelles.

→ Valide ? Corrige ? Reoriente ?
```

**Attendre la reponse du closer avant de continuer.** Si le closer corrige (priorisation, perimetre, angle), mettre a jour le SDB en consequence avant de lancer la Pass 2.

### Pass 2 : NARRATIVE ARCHITECT
**Fichier :** `agents/prepare-pass2.md`

Plan narratif complet a partir du SDB valide. Choix du hook, de l'arc emotionnel, planification des 5-6 onglets (Contexte conditionnel, Diagnostic, Strategie, Projet, Investissement, Cas clients).
Output interne : **Narrative Blueprint (NBP)**.

**Pre-validation NBP (OBLIGATOIRE, gate bloquante) :** Apres la Pass 2, executer :
```bash
python3 tools/validate_proposal.py --nbp .cache/deals/{deal_id}/artifacts/NBP.md
```
- **Exit 0** : structure OK, passer au Checkpoint 2.
- **Exit 1-3** : problemes structurels. Corriger le NBP et re-valider.

### CHECKPOINT 2 : Validation narrative (OBLIGATOIRE)

Apres la Pass 2, presenter au closer le **plan narratif** dans le terminal. Format :

```
=== CHECKPOINT 2 : VALIDATION NARRATIVE ===

ARC CHOISI : {nom de l'arc} — {pourquoi cet arc pour ce deal, 1 phrase}
HOOK : {hero subtitle propose}
TONE_PROFILE : {DIRECT/PEDAGOGIQUE/PROVOCATEUR/TECHNIQUE}

ONGLET DIAGNOSTIC ({N} sections) :
 1. "{titre H2}" — {angle en 1 ligne}
 2. "{titre H2}" — {angle en 1 ligne}
 ...
 N. "{titre H2}" — {angle en 1 ligne}

ONGLET STRATEGIE ({N} slides) :
 1. "{titre}" — {contenu en 1 ligne}
 2. "{titre}" — {contenu en 1 ligne}
 ...

ONGLET INVESTISSEMENT :
 - Cout inaction : {3 impacts}
 - Phase 1 : {budget} — {scope}
 - Recommandation : {scenario} ({budget}/mois) — {pourquoi}
 - Alternatives : {mention 1 ligne}

OBJECTIONS PRE-EMPTEES (FAQ) :
 1. {question}
 2. {question}
 3. {question}

DECISIONS A FAIBLE CONFIANCE (blocs MEDIUM/LOW du Checkpoint 1) :
 - {decision} : {comment elle est traitee dans la narration}
 - {decision} : {comment elle est traitee}
→ Si un bloc LOW est toujours non resolu, le signaler ici.

→ Reordonne ? Renomme ? Ajoute ? Supprime ?
```

**Attendre la reponse du closer avant de continuer.** Si le closer modifie (ordre, titres, sections a ajouter/supprimer), mettre a jour le NBP en consequence avant de lancer la Pass 3.

### Pass 3 : DESIGN ORCHESTRATOR
**Fichier :** `agents/prepare-pass3.md`

Generation du contenu HTML des 5-6 onglets a partir du NBP valide. Mapping composants par role narratif, regles de composition. Assemblage final via `tools/build_proposal.py` (squelette + contenu). Validation.
Output : **HTML final** (le seul livrable visible) + **INTERNAL-DIAG** (diagnostic interne pour le closer).

---

## References

- Kit composants (30 composants, catalogue par role narratif) : `templates/proposal-kit.html`
- Design system : `context/design_system.md`
- Positionnement + structure offre : `context/positioning.md`
- Cas clients : `context/case_studies.md`
- Pricing : `context/pricing_rules.md`
- Frontiere client/interne : `context/output_contract.md`
- Field keys Pipedrive : `context/pipedrive_reference.md`
