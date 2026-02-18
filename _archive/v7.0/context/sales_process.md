# Sales Process SLASHR — v7.0

## Pipeline

| Étape | Objectif | Output | Owner |
|-------|----------|--------|-------|
| R1 — Qualification haute tension | Extraire la douleur, l'urgence et le pouvoir de décision | Dossier de qualification (brief scoré + résumé Search) | Deal Analyst Agent (`/analyse`) |
| R2 — Préparation | Préparer l'arsenal complet du closer | DECK complet (audit Search + slides + ammunition + checklist) | Deal Analyst Agent (`/deck`) |
| R2 — Recommandation décisionnelle | Poser la reco, traiter les blocages, verrouiller | Signature ou objection finale traitée | Closer humain |
| Post-R2 | Convertir ou clôturer | Séquence 3 touches puis archivage | Deal Analyst Agent (`/relances`) |

---

## Règles non négociables

1. **Aucun deck avant R2** — le prospect ne voit rien tant qu'il n'est pas qualifié
2. **R2 ≠ présentation** — c'est une recommandation. On ne montre pas ce qu'on fait, on dit ce qu'on ferait pour eux
3. **R2 se termine par un OUI ou un blocage nommé** — jamais par "on revient vers vous"
4. **Pas de discount, jamais** — on repositionne la valeur ou on laisse partir
5. **Pas d'urgence en R1 = pas de R2** — un prospect sans pression n'achète pas
6. **Max 48h R1→R2** — au-delà, le deal perd 60% de chances de closing
7. **3 relances max post-R2** — après, c'est mort. On archive proprement
8. **Le closer drive la conversation** — on pose les questions, on fixe le cadre, on contrôle le tempo
9. **Aucun envoi prospect sans validation humaine** — les agents produisent des DRAFTS. Le closer relit, valide, et envoie lui-même. Pas d'email automatique, pas de doc partagé sans approbation explicite

---

## Dossier R1 — Types d'input acceptés

Le système ne reçoit pas toujours un transcript parfait. Le closer peut fournir un **dossier R1** composé d'un ou plusieurs éléments :

| Type | Description | Fiabilité attendue |
|------|-------------|--------------------|
| **Transcript complet** | Call enregistré + transcription auto | HAUTE |
| **Notes closer** | Notes à la volée, format libre | MOYENNE à HAUTE |
| **Documents prospect** | CdC, brief, cadrage, RFP | MOYENNE |
| **Email prospect** | Besoin décrit par écrit, sans call | BASSE à MOYENNE |

### Indice de fiabilité

Chaque brief R1 porte un **indice de fiabilité** (HAUTE / MOYENNE / BASSE) qui mesure la confiance qu'on peut accorder au score en fonction de la qualité des sources.

**Critères de calcul :**
- Nombre de questions non négociables couvertes par les sources (0 à 5)
- Type de source principal (transcript > notes > documents > email)
- Nombre de champs marqués "NON DOCUMENTÉ" dans le brief

### Règle fiabilité × score

| Fiabilité | Score >= 60 | Score 40-59 | Score < 40 |
|-----------|-------------|-------------|------------|
| **HAUTE** | Verdict inchangé | Verdict inchangé | Verdict inchangé |
| **MOYENNE** | Verdict inchangé | Verdict inchangé | Verdict inchangé |
| **BASSE** | Override : R2_GO → R2_CONDITIONAL + action "compléter qualification" | Action ajoutée : "compléter qualification avant validation" | Verdict inchangé |

**Principe : un deal prometteur avec des sources incomplètes n'est pas bloqué — il est conditionné à une complétion de la qualification.**

### "NON MENTIONNÉ" vs "NON DOCUMENTÉ"

| Marqueur | Signification | Scoring |
|----------|---------------|---------|
| **NON MENTIONNÉ** | Le sujet n'a pas été abordé (transcript complet disponible) | Signal faible → score bas sur ce critère |
| **NON DOCUMENTÉ** | On ne sait pas — les sources ne couvrent pas ce point | Pas de signal → score médian (3/5) par prudence |

---

## R1 — Qualification haute tension

### Posture

R1 n'est pas un call de découverte. C'est un interrogatoire stratégique bienveillant. Le closer qualifie **le prospect**, pas l'inverse. Si le prospect n'a pas de douleur urgente, on ne force pas — on disqualifie.

### 5 questions non négociables

Ces questions doivent être posées en R1. Pas d'exception. Elles servent aussi de **référentiel pour le calcul de fiabilité** : le nombre de questions dont la réponse apparaît dans le dossier R1 détermine la fiabilité du brief.

**Note :** si le R1 n'est pas un call (email, document seul), les réponses à ces questions peuvent être extraites des sources disponibles. L'important n'est pas qu'elles soient "posées" verbalement, mais que l'information soit présente dans le dossier.

| # | Question | Ce qu'on cherche |
|---|----------|------------------|
| 1 | "Quel est le problème business que vous essayez de résoudre — en termes de chiffre d'affaires ?" | Douleur chiffrée, pas un vague "on veut plus de visibilité" |
| 2 | "Qu'est-ce qui se passe si vous ne faites rien dans les 6 prochains mois ?" | Urgence réelle. Si "rien de grave" → red flag |
| 3 | "Qui d'autre est impliqué dans cette décision, et quel est le process pour dire oui ?" | Mapping décisionnel. Décideur absent = R2 à risque |
| 4 | "Vous avez une enveloppe budget en tête, même approximative ?" | Capacité d'investissement. Pas de budget = pas de deal |
| 5 | "Si on vous montre un plan qui répond à ça, vous êtes en mesure de démarrer ce mois-ci ?" | Test d'engagement. Réponse floue = prospect pas prêt |

### Règle de micro-engagement

Avant de raccrocher R1, le closer obtient **un engagement concret** du prospect :

- Confirmation de la date R2 (dans les 48h)
- Confirmation de la présence du décideur en R2
- Accord verbal : "Si la recommandation est pertinente, vous êtes prêt à avancer"

**Règles de traitement selon le niveau de micro-engagement :**

| Micro-engagement | Score >= 60 | Score 40-59 | Score < 40 |
|------------------|-------------|-------------|------------|
| **OUI** (3/3 obtenus) | R2 GO — process normal | R2 CONDITIONAL — validation manager | NURTURE |
| **PARTIEL** (1-2/3 obtenus) | R2 GO mais action pré-R2 obligatoire : fixer un call SLASHR dédié sous 48h pour sécuriser les engagements manquants. Si non obtenus → R2 suspendue | R2 bloquée tant que le PARTIEL n'est pas converti en OUI. Deadline : 72h. Au-delà → NURTURE | NURTURE |
| **NON** (0/3) | R2 non programmée. NURTURE | NURTURE | NURTURE |

**Un micro-engagement PARTIEL n'est jamais un feu vert définitif — c'est un feu orange avec une action corrective obligatoire.**

### Scoring R1 — Grille 5 niveaux + Fiabilité

Référence complète : `contracts/r1_brief.schema.md` Section 4 (scoring + indice de fiabilité + règle fiabilité × score).

| Critère | Poids | 5 pts (max) | 1 pt (min) |
|---------|-------|-------------|------------|
| Douleur business | ×6 | Perte de CA chiffrée en € + verbatim | Aucune douleur exprimée |
| Urgence | ×5 | Deadline < 6 semaines, pression board | Pas de timeline, exploration |
| Budget | ×4 | Enveloppe précise dédiée SLASHR | Aucun signal, refus de répondre |
| Décideur | ×3 | C-level en call, peut signer seul | Opérationnel, décideur inconnu |
| Fit stratégique | ×2 | Multi-marchés, Search+IA, CA > 10M€ | Site vitrine, aucun enjeu strat |

**Score = somme(points × poids). Max = 100.**

**>= 60 → R2 GO**
**40-59 → R2 conditionnelle (validation manager + micro-engagement renforcé)**
**< 40 → NURTURE. Pas de R2.**

---

## R2 — Recommandation décisionnelle

### Posture

R2 n'est pas un pitch. C'est la présentation d'une recommandation stratégique construite pour ce prospect. Le closer ne vend pas — il recommande. La différence : un vendeur espère un oui, un conseiller stratégique assume sa reco et demande une décision.

### Structure R2 — 10 slides max, 30 minutes

| Slide | Contenu | Durée | Objectif |
|-------|---------|-------|----------|
| 1 | **Contexte prospect** — ce qu'on a compris de leur situation | 2 min | Montrer qu'on a écouté. Valider avec le prospect |
| 2 | **Diagnostic data** — chiffres DataForSEO (trafic, positions, gap concurrentiel) | 3 min | Objectiver la douleur avec de la data |
| 3 | **Coût de l'inaction** — ce que le prospect perd chaque mois en restant immobile | 2 min | Créer l'urgence rationnelle |
| 4 | **Vision cible** — où le prospect peut être dans 6-12 mois | 2 min | Ouvrir le champ des possibles |
| 5 | **Recommandation stratégique** — les 3 piliers du plan SLASHR pour ce prospect | 5 min | Le coeur de la reco. Spécifique, pas générique |
| 6 | **Quick wins 90 jours** — les 3 actions immédiates et leurs résultats attendus | 3 min | Prouver qu'on démarre vite et qu'on délivre tôt |
| 7 | **Équipe et méthode** — qui intervient, comment on pilote | 2 min | Rassurer sur l'exécution |
| 8 | **Investissement** — 2-3 scénarios adaptés au prospect | 3 min | Essentiel / Performance / Croissance. Périmètre et fréquence clairs. Le closer ajuste les montants |
| 9 | **ROI projeté** — retour estimé vs investissement sur 12 mois | 3 min | Justifier le prix par le retour |
| 10 | **Décision** — slide vide, c'est le moment du closing | 6 min | Verrouiller |

**Total : 30 min max. Pas de Q&A flottant — les questions se traitent slide par slide.**

### Script de fin R2 — mot à mot

Ce script se déroule sur la slide 10. Le closer le suit à la lettre.

---

**Étape 1 — Récap (30 sec)**

> "Pour résumer : vous avez un problème de {douleur_principale} qui vous coûte {impact_chiffré}. On vous a montré un plan qui adresse ça en {timeline} avec des premiers résultats visibles à 90 jours. L'investissement est de {prix}."

**Étape 2 — Question de température**

> "Sur une échelle de 1 à 10, 10 étant 'on démarre lundi' — vous en êtes où ?"

**Étape 3 — Traitement du gap**

- Si **8-10** : passer directement à l'étape 4
- Si **5-7** : "OK. Qu'est-ce qui vous manque pour être à 10 ?" → traiter l'objection → reposer la question
- Si **< 5** : "Je comprends. Qu'est-ce qui bloque principalement ?" → si le blocage est traitable, traiter. Si non → "Je préfère qu'on soit honnêtes. Si ce n'est pas le bon moment, on se reparle quand ce sera le cas."

**Étape 4 — Verrouillage**

> "Parfait. Voilà ce que je vous propose comme next step : je vous envoie la lettre d'engagement aujourd'hui, vous la relisez, et on se cale un call de 15 min jeudi pour finaliser. Ça vous va ?"

**Étape 5 — Silence**

Après la question de verrouillage : **se taire**. Le premier qui parle perd. Attendre la réponse, même si le silence dure 10 secondes.

---

**Sorties possibles de R2 :**

| Résultat | Action |
|----------|--------|
| OUI → signature | Envoyer LOI dans l'heure. Call de finalisation dans 48h |
| OUI MAIS → objection traitable | Traiter sur place. Reposer la question de verrouillage |
| PAS MAINTENANT → timing | Fixer une date de re-contact précise. Pas de "revenez vers moi" |
| NON | Accepter. Demander le feedback. Archiver proprement |
| SILENCE / FLOU | Activer le protocole anti-ghosting |

---

## Protocole anti-ghosting post-R2

### Déclenchement

Pas de réponse claire 48h après R2 → activation automatique.

### Sources de vérité

- **Templates, variables et structure des emails :** `templates/followups.md`
- **Instanciation personnalisée :** `prompts/deal_analyst_system.md`

Ce document définit les principes. Pas de duplication du contenu des templates.

### Principes

| # | Principe | Conséquence |
|---|----------|-------------|
| 1 | Chaque touch apporte de la valeur nouvelle | Jamais de "je me permets de revenir vers vous" |
| 2 | Personnalisation obligatoire | Si les variables ne sont pas remplissables → la relance ne part pas |
| 3 | Espacement strict : J+5, J+12, J+20 | Pas de raccourcissement, même si le deal semble chaud |
| 4 | Canal unique : email | Pas de LinkedIn, SMS, ou call non sollicité |
| 5 | 3 touches maximum | Après Touch 3 sans réponse → "Lost — Ghosting", tag "revisit_Q+1" |
| 6 | Zéro Touch 4 | La dignité du positionnement passe avant le deal |
| 7 | **Validation humaine obligatoire** | Les emails sont générés en DRAFT. Le closer relit, ajuste si besoin, et envoie lui-même. Aucun envoi automatique |

### Post-séquence

| Scénario | Action Pipedrive |
|----------|-----------------|
| Réponse positive | Call de finalisation sous 48h |
| Réponse négative explicite | "Lost — Declined". Noter motif. Tag "revisit_Q+1" |
| Ouverture sans réponse | Ne rien faire. L'ouverture n'est pas un signal d'achat |
| Aucune ouverture, aucune réponse | "Lost — Ghosting". Tag "revisit_Q+1". Archiver |

### Deal closure

**Tout deal clôturé (Won ou Lost) déclenche un debrief obligatoire : `contracts/deal_closure.schema.md`.**

---

## Validation humaine — Règle absolue

**Aucun output du système n'est envoyé à un prospect sans validation explicite du closer.**

### Ce que le système produit = des DRAFTS

| Output | Statut | Commande | Stockage | Validation |
|--------|--------|----------|----------|------------|
| Dossier de qualification (brief scoré + résumé Search) | DRAFT | `/analyse {deal_id}` | DEAL-*.md → Drive | Le closer relit, valide |
| DECK complet R2 (audit Search + slides + ammunition + checklist) | DRAFT | `/deck {deal_id}` | DECK-*.md → Drive | Le closer relit, copie slides dans Google Slides, personnalise |
| Kit onboarding | DRAFT | `/onboarding {deal_id}` | ONBOARDING-*.md → Drive | Le closer partage avec l'équipe delivery |
| Email relance J+5 | DRAFT | `/relances {deal_id}` | RELANCES-*.md → Drive | Le closer copie dans Gmail, ajuste, envoie |
| Email relance J+12 | DRAFT | `/relances {deal_id}` | → idem | Idem |
| Email relance J+20 | DRAFT | `/relances {deal_id}` | → idem | Idem |

### Ce que Claude Code ne fait JAMAIS

- ❌ Envoyer un email à un prospect
- ❌ Partager un Google Doc avec un prospect
- ❌ Créer un événement calendrier avec un prospect
- ❌ Envoyer un message LinkedIn, SMS ou autre canal

### Ce que Claude Code PEUT faire

- ✅ Lire les données Pipedrive via API (deal, contact, org, notes, activités)
- ✅ Mettre à jour Pipedrive via API (champs, stages, activités)
- ✅ Lire les fichiers sources depuis Google Drive (transcript, notes, CdC, emails)
- ✅ Écrire les outputs dans Google Drive (DEAL-*.md, DECK-*.md, RELANCES-*.md, ONBOARDING-*.md)
- ✅ Enrichir via DataForSEO (trafic, keywords, concurrents)
- ✅ Produire des fichiers markdown structurés (dossiers deal, decks, relances, onboarding)

### Workflow de validation relances

```
/relances {deal_id}
    → Claude Code lit le DEAL-*.md depuis Google Drive + email contact depuis Pipedrive
    → Génère 3 emails personnalisés → uploade RELANCES-*.md dans le dossier Drive du deal
    → Le closer copie chaque email en brouillon Gmail
    → Le closer relit, ajuste si besoin, envoie manuellement
    → /pipedrive {deal_id} relance J5_ENVOYEE (puis J12, J20)
```

---

## Intégrations

| Outil | Rôle | Accès |
|-------|------|-------|
| **Claude Code** | Cerveau unique — 5 commandes : `/analyse`, `/deck`, `/relances`, `/onboarding`, `/pipedrive` | — |
| **Pipedrive** | CRM + source de vérité — deal ID = point d'entrée unique | API REST — token dans `~/.pipedrive_token` |
| **Google Drive** | Stockage — fichiers sources (dossier R1) + tous les outputs générés | API REST — Service Account dans `~/.google_service_account.json` |
| **DataForSEO** | Enrichissement data prospect (trafic, keywords, concurrents) | MCP tools intégrés dans Claude Code |
| **Google Slides** | Template deck R2 — le closer copie le contenu généré par `/deck` | Manuel (copier-coller) |
| **Gmail** | Le closer copie les brouillons de relance générés par `/relances` | Manuel (copier-coller) |

---

## Pipedrive Mapping — Source de vérité IDs

> **Pipeline :** Pipeline SLASHR (id: `1`)

### Stages

| # | Stage | Pipedrive ID | Proba | Commande Claude Code | Action closer |
|---|-------|-------------|-------|---------------------|---------------|
| 1 | Lead In | `1` | 0% | — | — |
| 2 | R1 Scheduled | `6` | 10% | — | — |
| 3 | R1 Done | `2` | 30% | `/analyse` → DEAL-*.md (qualification) | Relire le DEAL, valider |
| 4 | R2 Scheduled | `7` | 50% | `/deck` → DECK-*.md (audit + slides + ammunition + checklist) | Copier slides dans Google Slides, valider Pre-R2 Checklist (DECK Part 4) |
| 5 | R2 Done | `4` | 50% | `/relances` → 3 emails | Copier en brouillons Gmail, envoyer |
| 6 | Pending Signature | `8` | 80% | `/onboarding` → kit lancement | Partager avec l'équipe delivery |

### Deal Fields customs

| Champ | Pipedrive ID | Key (hash) | Type | Valeurs |
|-------|-------------|------------|------|---------|
| Leviers pressentis | `42` | `f8c51fb60ea43a34c56998b6ad9bf946234149a1` | set | SEO, GEO, SEA/SMA, DATA, UX, DEV, Autres |
| Canal d'origine | `36` | — (champ standard) | enum | Partenaire, Site web, Action marketing, Prospection, Réseau, Bouche à oreille, Relation client |
| r1_score | `52` | `e529595ef908cdf5851df4355bbce866f322fcae` | double | 0-100 |
| r1_verdict | `53` | `10acdb5b3c31d46baa19936775b00758edf6d6bc` | enum | R2_GO (89), R2_CONDITIONAL (90), NURTURE (91) |
| r1_fiabilite | `54` | `25258b25cbbe4e3ed41546251476ae752156f8aa` | enum | HAUTE (92), MOYENNE (93), BASSE (94) |
| r2_pack_link | `55` | `4b84e7bfe1a6b330318fc7a0d208e2faedf2530a` | varchar | URL Google Doc |
| decideur_level | `56` | `0b4c7e8cc10ced7badf65b34dac6254bd10a0179` | enum | DÉCIDEUR (95), INFLUENCEUR (96), OPÉRATIONNEL (97) |
| relance_status | `57` | `e2ed93c97e15989382085b83caca790da0e516d3` | enum | PAS_COMMENCEE (98), J5_ENVOYEE (99), J12_ENVOYEE (100), J20_ENVOYEE (101), REPONSE (102) |
| dossier_r1_link | `58` | `1fd2ec1073fa60e11fb59bddfec7a2f6656c4b0c` | varchar | URL Google Doc / Drive |

### Activity Types

| Activité | Pipedrive ID | Key | Trigger | Couleur |
|----------|-------------|-----|---------|---------|
| Valider R1 Done | `9` | `valider_r1_done` | Deal → stage "R1 Done" (id=2) | 🟢 green |
| Pre-R2 Checklist | `10` | `pre_r2_checklist` | Deal → stage "R2 Scheduled" (id=7) | 🔵 blue |
| Relance J+5 | `11` | `relance_j5` | 48h après "R2 Done — Pending" si pas Won | 🟡 yellow |
| Relance J+12 | `12` | `relance_j12` | Idem | 🟡 yellow |
| Relance J+20 | `13` | `relance_j20` | Idem | 🔴 red |

### Workflow closer — 5 commandes Claude Code

> **Un seul identifiant : le deal ID Pipedrive.** Claude va chercher tout le contexte automatiquement (Pipedrive + Google Drive + DataForSEO).

```
1. R1 DONE
   → Déposer les fichiers sources dans le dossier Drive du deal
   → Vérifier que dossier_r1_link est rempli dans Pipedrive
   → /analyse {deal_id}
   → Relire le DEAL-*.md (uploadé automatiquement dans Drive)
   → Pipedrive mis à jour automatiquement (score, verdict, fiabilité)

2. PRÉPARER R2
   → /deck {deal_id}
   → Copier les slides (DECK Part 2) dans le template Google Slides
   → Personnaliser les slides
   → Valider la Pre-R2 Checklist (DECK Part 4)

3. APRÈS R2 — PAS DE SIGNATURE (48h+)
   → /relances {deal_id}
   → Copier chaque email en brouillon Gmail
   → Envoyer manuellement à J+5, J+12, J+20
   → /pipedrive {deal_id} relance J5_ENVOYEE (etc.)

4. DEAL SIGNÉ
   → /pipedrive {deal_id} stage "Pending Signature"
   → /onboarding {deal_id}
   → Partager le kit ONBOARDING-*.md avec l'équipe delivery
```
