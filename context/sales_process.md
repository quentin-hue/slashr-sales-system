# Sales Process SLASHR — v9.0 (Closer Handbook)

> Guide de reference du closer humain. Pour les instructions systeme : voir `agents/`.

---

## Pipeline — 5 commandes

| # | Stage | Commande | Action closer |
|---|-------|----------|---------------|
| 1 | Lead In | — | — |
| 2 | R1 Scheduled | — | Preparer les 5 questions R1 |
| 3 | R1 Done | `/qualify {deal_id}` | Relire le scoring, valider |
| 4 | R2 Scheduled | `/prepare {deal_id}` | Preview la proposition HTML, valider |
| 5 | R2 Done | — | Relancer manuellement si besoin |
| 6 | Pending Signature | — | Finaliser le deal |

Reference IDs Pipedrive : `context/pipedrive_reference.md`

---

## Flux complet

```
1. R1 DONE
   -> Deposer les fichiers dans le dossier Drive du deal
   -> Verifier que dossier_r1_link est rempli dans Pipedrive
   -> /qualify {deal_id}
   -> Relire le scoring dans le terminal

2. PREPARER R2
   -> /prepare {deal_id}
   -> Ouvrir la PROPOSAL HTML dans le navigateur pour preview
   -> Personnaliser si besoin, valider avant envoi

3. APRES R2 — PAS DE SIGNATURE
   -> Relancer manuellement (email, call)
   -> /qualify {deal_id} pour re-scorer si nouvel element

4. DEAL SIGNE
   -> /pipedrive {deal_id} won
   -> /debrief {deal_id}
   -> Repondre aux 5 questions de feedback

5. DEAL PERDU
   -> /pipedrive {deal_id} lost "motif"
   -> /debrief {deal_id}
   -> Repondre aux 5 questions de feedback
```

---

## Regles non negociables

1. Tous les outputs sont des DRAFTS — aucun envoi automatique au prospect
2. Le systeme ne contacte jamais un prospect directement
3. Chaque affirmation s'appuie sur une source ou un chiffre (data-first)
4. Le scoring est transparent — chaque note justifiee en 1 ligne
5. ROI conservateur — CTR reels > CTR estimes
6. Tonalite partenaire strategique — jamais arrogant, jamais suppliant
7. Perimetre adapte au deal — ne pas forcer Search global si le besoin est SEO seul
8. Pipedrive = source de verite — tout passe par le deal ID

---

## R1 — Qualification

### Posture

R1 n'est pas un call de decouverte. C'est un interrogatoire strategique bienveillant. Le closer qualifie **le prospect**, pas l'inverse. Si le prospect n'a pas de douleur urgente, on ne force pas — on disqualifie.

### 5 questions non negociables

| # | Question | Ce qu'on cherche |
|---|----------|------------------|
| 1 | "Quel est le probleme business que vous essayez de resoudre — en termes de chiffre d'affaires ?" | Douleur chiffree |
| 2 | "Qu'est-ce qui se passe si vous ne faites rien dans les 6 prochains mois ?" | Urgence reelle |
| 3 | "Qui d'autre est implique dans cette decision, et quel est le process pour dire oui ?" | Mapping decisionnel |
| 4 | "Vous avez une enveloppe budget en tete, meme approximative ?" | Capacite d'investissement |
| 5 | "Si on vous montre un plan qui repond a ca, vous etes en mesure de demarrer ce mois-ci ?" | Test d'engagement |

### Scoring

Apres le R1, `/qualify {deal_id}` produit un score 0-100 dans le terminal.

| Seuil | Verdict | Action |
|-------|---------|--------|
| >= 60 | GO | Preparer la proposition : `/prepare {deal_id}` |
| 40-59 | CONDITIONNEL | Valider avec le manager avant /prepare |
| < 40 | NURTURE | Pas de proposition. Condition de reactivation a definir |

---

## R2 — Recommandation decisionnelle

### Posture

R2 n'est pas un pitch. C'est la presentation d'une recommandation strategique. Le closer ne vend pas — il recommande.

### Support

La proposition HTML interactive generee par `/prepare`. Elle contient tout : contexte, diagnostic, strategie, pricing, ROI.

Le closer parcourt la proposition HTML en partage d'ecran (ou l'envoie en amont).

### Pitch S7 — quand on arrive sur la section "Lecture strategique"

Le closer arrive sur le radar S7 dans l'onglet Diagnostic. **30 secondes max.** Pas de cours sur le framework — juste assez pour que le decideur comprenne la logique.

**Mini-script (a adapter au ton de la conversation) :**

> "On utilise un modele proprietaire en 7 forces pour analyser votre situation Search. L'idee est simple : on ne travaille pas les 7 en meme temps. On identifie les 2-3 leviers qui debloquent le plus de valeur pour vous, et on concentre les ressources dessus."

**Enchainer immediatement avec le radar :**
- Montrer les scores (le visuel parle tout seul)
- Nommer la contrainte principale et les leviers prioritaires (ils sont affiches)
- Ne PAS detailler les forces non priorisees — le prospect les voit, ca suffit

**2 questions obligatoires apres le pitch S7 :**

| # | Question | Objectif |
|---|----------|----------|
| 1 | "Est-ce que cette lecture de votre situation est juste ?" | **Validation du diagnostic.** Si le prospect corrige, on ajuste — ca renforce la credibilite. Si il valide, on a son buy-in sur l'analyse. |
| 2 | "Si on ne devait travailler qu'un seul levier, lequel est prioritaire selon vous ?" | **Arbitrage.** On implique le decideur dans la priorisation. Sa reponse revele ses vraies priorites (pas toujours celles du transcript R1). |

**Regles :**
- Ne pas dire "framework" ou "methodology" au prospect — dire "grille d'analyse" ou "notre modele"
- Si le prospect pose des questions sur une force non priorisee, repondre factuellement mais recentrer : "C'est un sujet, mais les donnees montrent que {levier prioritaire} aura plus d'impact a court terme."
- **Ne jamais proposer de travailler les 7 forces** — meme si le prospect le demande. Repondre : "On pourrait, mais ca diluerait l'impact. Mieux vaut debloquer {contrainte} d'abord, puis elargir."

### Script de fin R2

**Etape 1 — Recap avec resume decisionnel (30 sec)**

Utiliser les 6 bullets du resume decisionnel de la proposition (onglet Investissement). Le decideur les a sous les yeux — le closer les verbalise.

> "Pour resumer : vous avez un probleme de {douleur_principale} qui vous coute {impact_chiffre}. Notre diagnostic montre que {contrainte S7} est le verrou principal. On vous propose un plan en {timeline} avec des premiers resultats a 90 jours. L'investissement est de {prix}."

**Etape 2 — Micro-validation**

Avant la temperature, valider le diagnostic :
> "Est-ce que cette lecture de votre situation est juste ?"

Si oui → enchainer. Si correction → noter, ajuster, puis enchainer. Chaque correction renforce l'engagement (le prospect co-construit).

**Etape 3 — Question de temperature**
> "Sur une echelle de 1 a 10, 10 etant 'on demarre lundi' — vous en etes ou ?"

**Etape 4 — Objection cachee**

Quel que soit le score, poser cette question **avant** de traiter le gap :
> "En dehors de {le gap mentionne}, est-ce qu'il y a autre chose qui vous fait hesiter ?"

**Pourquoi :** la premiere objection est rarement la vraie. Le "je dois en parler a mon associe" cache souvent un doute sur le prix, le ROI, ou la confiance. Cette question ouvre la porte a l'objection reelle.

**Etape 5 — Traitement du gap**
- **8-10** : passer au verrouillage
- **5-7** : "Qu'est-ce qui vous manque pour etre a 10 ?" → traiter → reposer la temperature
- **< 5** : "Qu'est-ce qui bloque principalement ?" → si traitable, traiter. Sinon → "Je prefere qu'on soit honnetes."

**Etape 6 — Verrouillage**
> "Je vous envoie la lettre d'engagement aujourd'hui. On se cale un call de 15 min {jour precis} pour finaliser. Ca vous va ?"

**Etape 7 — Silence**
Apres la question de verrouillage : **se taire**. Attendre. Ne pas combler le silence.

### Regle absolue : ne jamais finir un R2 sans next step date

Peu importe le score de temperature (meme un 3/10) — le R2 se termine avec une action datee. Pas "on se rappelle la semaine prochaine" — un jour et une heure.

| Score | Next step |
|-------|-----------|
| 8-10 | Date d'envoi lettre d'engagement + call de finalisation |
| 5-7 | Call de 15 min pour traiter le gap identifie — date fixee avant de raccrocher |
| < 5 | Call de 10 min dans 1-2 semaines pour faire le point — "ca ne vous engage a rien, mais ca evite que ca traine" |

**Si le prospect refuse tout next step :** c'est un signal. Le noter dans Pipedrive, passer en protocole anti-ghosting.

---

## Protocole anti-ghosting post-R2

**Declenchement :** pas de reponse claire 48h apres R2.

| # | Principe |
|---|----------|
| 1 | Chaque touch apporte de la valeur nouvelle |
| 2 | Espacement : J+5, J+12, J+20 |
| 3 | Canal : email |
| 4 | 3 touches maximum |
| 5 | Zero Touch 4 — la dignite passe avant le deal |
| 6 | Validation humaine obligatoire |

### Post-sequence

| Scenario | Action |
|----------|--------|
| Reponse positive | Call de finalisation sous 48h |
| Reponse negative | Lost — noter motif |
| Aucune reponse | Lost — Ghosting |
