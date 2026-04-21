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

Collecte en 2 phases (contexte puis SEO) + analyse dimensionnelle parallele (4 analystes) + confrontation croisee + structuration + synthese strategique + devil's advocate + diagnostic interne.
Output interne : **Structured Data Brief (SDB)** (inclut les scores dimensionnels, la validation croisee inter-sources, et le diagnostic strategique challenge).

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

SCORES DIMENSIONNELS :
- Technical  : {X}/100 — {top probleme en 1 ligne}
- Contenu    : {X}/100 ({Fort/Moyen/Faible}) — {gap principal}
- Competitive: {insight benchmark en 1 ligne}
- GEO/IA     : {X}/100 ({Pret/Partiel/Absent}) ou N/A

DONNEES CLES :
1. {donnee 1 — chiffre + source}
2. {donnee 2 — chiffre + source}
3. {donnee 3 — chiffre + source}
4. {donnee 4 — chiffre + source}
5. {donnee 5 — chiffre + source}

DIAGNOSTIC :                                    CONFIANCE
- Contrainte : {en langage business}             {HIGH/MEDIUM/LOW}
  Dimensions : {technique + contenu / etc.}
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

SIGNAUX CLOSER (si analyst-signals active) :
- Sentiment prospect : {Chaud/Tiede/Froid}
- Objections detectees : {liste ou "aucune"}
- Concurrence : {Confirmee/Suspectee/Absente}

─────────────────────────────────────
QUESTIONS POUR TOI (reponds en 1-2 phrases chacune) :

1. CONFIANCE : Sur le diagnostic ci-dessus, ton niveau de confiance ? (1-5)
   → 1 = "je ne suis pas d'accord", 5 = "c'est exactement ca"

2. ANGLE : Quel angle le prospect attend-il ?
   → Ex: "il veut du ROI chiffre", "il veut etre rassure sur la methode", "il veut voir que ses concurrents avancent"

3. HORS-DATA : Quelque chose que les donnees ne montrent pas ?
   → Ex: "il a un nouveau DG qui pousse le digital", "il a ete decu par son agence actuelle", "decision a prendre avant juin"

4. TONE : Le ton propose ({TONE_PROFILE}) te semble adapte ?
   → Sinon, quel profil ? (DIRECT / PEDAGOGIQUE / PROVOCATEUR / TECHNIQUE)

5. RED FLAGS : Un risque que le systeme n'a pas detecte ?
   → Ex: "budget serre", "il compare avec 2 autres agences", "le decideur n'etait pas en R1"
─────────────────────────────────────
```

**Attendre la reponse du closer avant de continuer.**

**Traitement des reponses :**
- Si confiance <= 2 → demander ce qui ne va pas, corriger le diagnostic, re-presenter
- Si confiance 3 → traiter les points specifiques mentionnes, ajuster
- Si confiance 4-5 → continuer
- Les reponses aux questions 2-5 sont integrees dans le SDB :
  - Q2 (angle) → champ `CLOSER_ANGLE` dans le SDB (utilise par Pass 2 pour choisir le hook et l'arc)
  - Q3 (hors-data) → champ `CLOSER_INSIGHTS` dans le SDB (contexte non mesurable)
  - Q4 (tone) → met a jour `TONE_PROFILE` si le closer change
  - Q5 (red flags) → ajoute aux `RED FLAGS` du SDB

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

─────────────────────────────────────
QUESTIONS POUR TOI :

1. SCROLLING TEST : En lisant les titres H2 du Diagnostic dans l'ordre, est-ce que l'histoire tient ?
   → Sinon, quel titre changer ou deplacer ?

2. HOOK : Le hero subtitle "{hook}" va accrocher TON prospect ?
   → Sinon, quel angle preferes-tu ?

3. OBJECTIONS : Les 3 FAQ pre-emptent les vraies objections que tu anticipes ?
   → Manque-t-il une question que le prospect posera forcement ?

4. CAS CLIENTS : Les cas selectionnes sont pertinents pour ce prospect ?
   → Preferes-tu d'autres cas ? Ou pas de cas clients du tout ?

5. PRICING : Le scenario {scenario} a {budget}/mois, ca passe pour ce prospect ?
   → Trop haut ? Trop bas ? Faut-il ajuster avant de generer ?
─────────────────────────────────────
```

**Attendre la reponse du closer avant de continuer.**

**Traitement des reponses :**
- Q1-2 : ajuster les titres/hook dans le NBP
- Q3 : ajouter/modifier les FAQ dans le NBP
- Q4 : changer les cas clients ou supprimer l'onglet
- Q5 : ajuster le scenario/budget dans le NBP et le SDB (coherence pricing_rules.md)
- Toute modification → re-valider le NBP avec `validate_proposal.py --nbp`

### Pass 3 : DESIGN ORCHESTRATOR
**Fichier :** `agents/prepare-pass3.md`

Generation du contenu HTML des 5-6 onglets a partir du NBP valide. Mapping composants par role narratif, regles de composition. Assemblage final via `tools/build_proposal.py` (squelette + contenu).
Output : **HTML final** (le seul livrable visible) + **INTERNAL-DIAG** (diagnostic interne pour le closer).

### Boucle self-critique (OBLIGATOIRE, apres assemblage, avant upload)

Apres assemblage du HTML par `build_proposal.py`, le systeme ne montre PAS immediatement le resultat. Il execute une boucle d'auto-amelioration :

```
BOUCLE SELF-CRITIQUE (max 2 iterations)

Iteration 1:
  1. Valider : python3 tools/validate_proposal.py {html_path}
  2. Lire le score (0-100) et les resultats
  3. Si score >= 85 ET 0 HARD failures → SORTIR (proposition prete)
  4. Si HARD failures → corriger les onglets concernes, re-assembler, re-valider
  5. Si score < 85 (mais 0 HARD) → analyser les WARN et SOFT, corriger les plus impactants

Iteration 2 (si declenchee):
  1. Re-valider apres corrections
  2. Si score >= 75 ET 0 HARD failures → SORTIR (acceptable)
  3. Sinon → SORTIR avec WARNING au closer : "Score {X}/100, {N} problemes non resolus"

Post-boucle:
  - Afficher le score final dans le terminal
  - Uploader le HTML dans Drive
  - Presenter le resultat au closer avec le score
```

**Ce que le systeme corrige automatiquement (sans demander) :**
- HARD failures Layer 1 (jargon interne, tirets cadratins, TJM/jours visibles, CTA generiques)
- Accents manquants (regle 16c)
- Coherence chiffres SDB → HTML (gate 0 de Pass 3)

**Ce que le systeme signale mais ne corrige pas :**
- Problemes narratifs (Layer 3 semantic)
- Densité de slides (Layer 2 content)
- Score qualite redactionnelle (Layer 4)

**Affichage au closer :**
```
=== PROPOSITION GENEREE ===

Score qualite : {X}/100 (Grade {A/B/C/D/F})
  Structure  : {X}/35
  Contenu    : {X}/25
  Qualite    : {X}/25
  Semantique : {X}/15

{Si iterations > 0 : "Auto-corrigee : {N} problemes resolus (HARD: {n}, SOFT: {n})"}
{Si score < 75 : "⚠ Score bas — verifier les WARN dans le terminal ci-dessus"}

Fichier : .cache/deals/{deal_id}/artifacts/PROPOSAL-{date}-{slug}.html
Drive : {lien si uploade}

→ /review {deal_id} pour preview live + review slide par slide
```

---

## References

- Kit composants (30 composants, catalogue par role narratif) : `templates/proposal-kit.html`
- Design system : `context/design_system.md`
- Positionnement + structure offre : `context/positioning.md`
- Cas clients : `context/case_studies.md`
- Pricing : `context/pricing_rules.md`
- Frontiere client/interne : `context/output_contract.md`
- Field keys Pipedrive : `context/pipedrive_reference.md`
