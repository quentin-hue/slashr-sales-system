# Mode QUALIFY — Scoring terminal (v9.0)

> **Prerequis :** `agents/shared.md` lu.

---

## Objectif

Scorer un deal rapidement et peupler Pipedrive. Pas de fichier genere — tout se passe dans le terminal. Rejouable a volonte (nouveau mail, nouveau doc, nouvelle info → re-qualify).

---

## Collecte

### Module Pipedrive (complet)

Tous les appels decrits dans `shared.md`, y compris les emails.

### Module Drive

Lire les fichiers du dossier R1 si `dossier_r1_link` est renseigne.

### Module SEO (light)

Un seul appel DataForSEO par domaine detecte :
- `domain_rank_overview` → trafic organique, nb mots-cles, ETV

Pas de ranked_keywords, pas de competitors. C'est juste pour alimenter le score Fit.

---

## Detection des domaines

1. Website de l'organisation Pipedrive
2. Domaine(s) mentionnes dans les fichiers sources (transcript, notes, brief)
3. Domaine(s) mentionnes dans les emails Pipedrive
4. Si aucun domaine trouve → demander au closer

---

## Scoring — grille simplifiee

| Critere | Poids | 5/5 | 3/5 | 1/5 |
|---------|-------|-----|-----|-----|
| **Douleur** (x6) | 30 max | Perte CA chiffree + verbatim | Douleur claire non chiffree | Aucune douleur |
| **Urgence** (x5) | 25 max | Deadline < 6 sem, pression board | Objectif annuel, volonte d'agir | Pas de timeline |
| **Budget** (x4) | 20 max | Enveloppe precise | Indices forts (budget paid connu) | Aucun signal |
| **Decideur** (x3) | 15 max | C-level en call, signe seul | Influenceur fort, decideur accessible | Operationnel seul |
| **Fit** (x2) | 10 max | Multi-marches, CA > 10M, gap > x3 | Besoin reel, trafic existant | Site vitrine, aucun trafic |

**Score = somme(note x poids). Max = 100.**

**Seuils :**
- >= 60 → GO (preparer la proposition)
- 40-59 → CONDITIONNEL (valider avec le manager)
- < 40 → NURTURE (pas de proposition)

**Critere non documente → scorer au median (3/5).** Le minimum (1/5) est reserve aux signaux negatifs confirmes.

---

## Detection du decideur

| Signal | Niveau |
|--------|--------|
| C-level en R1, valide le budget seul | DECIDEUR |
| Head of / Directeur, budget owner ou acces direct au C-level | INFLUENCEUR |
| Manager / Chef de projet, pas de visibilite budget | OPERATIONNEL |

---

## Affichage terminal

```
═══════════════════════════════════════════════
  QUALIFY — {Entreprise} (Deal #{deal_id})
═══════════════════════════════════════════════

  Contact     {Prenom Nom} — {Role}
  Domaine(s)  {domaine1}, {domaine2}
  Stage       {stage Pipedrive}

───────────────────────────────────────────────
  SCORE : {score}/100 — {GO | CONDITIONNEL | NURTURE}
───────────────────────────────────────────────

  Douleur     {note}/5  {justification courte}
  Urgence     {note}/5  {justification courte}
  Budget      {note}/5  {justification courte}
  Decideur    {note}/5  {justification courte}  → {DECIDEUR|INFLUENCEUR|OPERATIONNEL}
  Fit         {note}/5  {justification courte}

───────────────────────────────────────────────
  RESUME
───────────────────────────────────────────────

  {3-5 lignes : douleur, situation, potentiel Search, risque principal}

───────────────────────────────────────────────
  SIGNAUX
───────────────────────────────────────────────

  Red flags    • {flag 1}
               • {flag 2}

  Green flags  • {flag 1}
               • {flag 2}

───────────────────────────────────────────────
  PROCHAINE ETAPE
───────────────────────────────────────────────

  {Si GO : "Pour generer la proposition : /prepare {deal_id}"}
  {Si CONDITIONNEL : "Valider avec le manager avant /prepare"}
  {Si NURTURE : "Deal disqualifie. Condition de reactivation : {condition}"}

═══════════════════════════════════════════════
```

---

## Update Pipedrive

Apres le scoring, mettre a jour automatiquement :
- `r1_score` → valeur 0-100
- `decideur_level` → DECIDEUR (95) | INFLUENCEUR (96) | OPERATIONNEL (97)

Reference field keys : `context/pipedrive_reference.md`

---

## Regles

1. **Pas de fichier genere.** Tout est dans le terminal + Pipedrive.
2. **Rejouable.** Chaque `/qualify` ecrase le score precedent. Le closer peut re-qualifier apres un nouvel echange.
3. **Rapide.** DataForSEO en mode light (rank_overview seul). Pas de ranked_keywords, pas de competitors.
4. **Honnete.** Si les sources sont insuffisantes, le dire. Scorer au median, pas au maximum.
5. **Pas de DECK, pas de slides, pas d'objections.** C'est un scoring, pas une preparation.
