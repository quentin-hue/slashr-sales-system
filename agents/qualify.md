# Mode QUALIFY : Scoring terminal (v11.0)

> **Prerequis :** `agents/shared.md` lu.

---

## Objectif

Scorer un deal rapidement et peupler Pipedrive. Pas de fichier genere, tout se passe dans le terminal. Rejouable a volonte (nouveau mail, nouveau doc, nouvelle info → re-qualify).

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

## Scoring : grille simplifiee (v11.1)

> Objectif : mesurer la **qualite decisionnelle** du deal, pas seulement l'intérêt SEO.
> Score = somme(note x poids). Max = 100.

| Critere | Poids | 5/5 | 4/5 | 3/5 | 2/5 | 1/5 |
|---------|-------|-----|-----|-----|-----|-----|
| **Douleur** | x6 (30) | Perte CA **chiffrée** + verbatim | Pain très clair + ordre de grandeur | Douleur claire non chiffrée | Signal faible / implicite | Aucune douleur |
| **Urgence** | x5 (25) | Deadline < 6 sem + contrainte externe (board / refonte / saison) | Deadline < 3 mois | Objectif annuel, volonté d'agir | "On verra" / pas prioritaire | Pas de timeline |
| **Budget** | x4 (20) | Enveloppe précise validable | Fourchette crédible | Indices forts (paid connu / historique) | Hypothèse faible | Aucun signal |
| **Décideur** | x3 (15) | C-level en R1, signe seul | C-level accessible + sponsor fort | Head of / Directeur, process clair | Opérationnel + accès flou | Opérationnel seul |
| **Fit** | x2 (10) | Multi-marches / complexité + gros gap Search | Besoin clair + potentiel observable | Besoin réel mais scope limité | Petit site / faible potentiel | Vitrine / aucun trafic |

### KO rules (anti-faux positifs)

Appliquer ces règles **avant** le total :

- Si **Budget = 1/5** ET **Décideur <= 2/5** → statut = NURTURE (même si le total dépasse 40).
- Si **Urgence = 1/5** ET **Douleur <= 2/5** → statut = NURTURE.
- Si **Décideur = 1/5** ET aucune preuve d'accès au décideur → statut max = CONDITIONNEL.
- Si données insuffisantes : scorer au **médian 3/5** (pas au max). Le 1/5 est réservé à un signal négatif confirmé.

### Seuils (inchangés)

- >= 60 → GO (préparer la proposition)
- 40-59 → CONDITIONNEL (valider avec le manager)
- < 40 → NURTURE (pas de proposition)

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
  QUALIFY · {Entreprise} (Deal #{deal_id})
═══════════════════════════════════════════════

  Contact     {Prenom Nom} · {Role}
  Domaine(s)  {domaine1}, {domaine2}
  Stage       {stage Pipedrive}

───────────────────────────────────────────────
  SCORE : {score}/100 · {GO | CONDITIONNEL | NURTURE}
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
