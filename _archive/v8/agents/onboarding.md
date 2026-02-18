# Mode ONBOARDING — Kit lancement post-signature (v8.0)

> **Prerequis :** `agents/shared.md` lu.

---

## Input

- Le fichier DEAL-*.md (qualification) depuis Google Drive
- Le fichier DECK-*.md (audit Search + slides + ammunition) depuis Google Drive

---

## Section 1 — Resume contexte client

| Champ | Source |
|-------|--------|
| Entreprise, interlocuteurs | DEAL Section 1 |
| Douleur business | DEAL Section 2 |
| Enjeux strategiques | DEAL Section 5 (signaux) |
| Historique R1/R2 | Ce qui s'est passe, ce qui a convaincu le client |
| Attentes explicites | Verbatims cles du prospect |
| Points de vigilance | Red flags identifies |
| Objections traitees en R2 | Ce qui a ete dit pour convaincre — delivery ne doit pas contredire le discours commercial |

**Format :** narrative, 150 mots max. L'equipe delivery doit comprendre le client en 2 minutes.

---

## Section 2 — Objectifs 90 jours

Extraits du DECK Part 2 (Slide 6 — Quick wins) + Part 3 (ROI projete).

| # | Objectif | KPI | Baseline actuelle | Cible a 90j | Methode de mesure |
|---|----------|-----|-------------------|-------------|-------------------|
| 1 | {objectif} | {KPI} | {valeur actuelle — source DECK Part 1} | {cible} | {comment on mesure} |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |

**Regle :** max 3 objectifs. Chacun SMART (specifique, mesurable, atteignable, realiste, temporel).

---

## Section 3 — Scope valide

| Inclus dans le scope | Hors scope |
|---------------------|------------|
| {livrable 1} | {ce qui n'est PAS inclus} |
| {livrable 2} | ... |
| ... | ... |

**Regle :** le hors-scope est aussi important que le scope. Prevenir les derives des le depart.

---

## Section 4 — Conditions contractuelles

| Champ | Valeur |
|-------|--------|
| Scenario signe | {Essentiel / Performance / Croissance} |
| Montant | {X EUR/mois ou EUR/an} |
| Frequence | {mensuel / trimestriel} |
| Duree engagement | {X mois} |
| Perimetre | {SEO seul / Search global / ...} |
| Conditions particulieres | {remise, clause de sortie, phase test, etc. Sinon "RAS"} |

**Source :** Pipedrive (deal value) + informations du closer.

---

## Section 5 — Checklist de demarrage

- [ ] Acces Google Analytics / Search Console obtenus
- [ ] Acces CMS / back-office obtenus
- [ ] Point de contact technique identifie cote client
- [ ] Kick-off call planifie (dans les 5 jours post-signature)
- [ ] Template de reporting mensuel prepare
- [ ] Baseline data exportee (source : DECK Part 1 Audit Search — positions, trafic, ETV avant intervention)
- [ ] {autres items specifiques au deal}

---

## Section 6 — Email de kickoff (brouillon)

**Objet :** `{Entreprise} x SLASHR — Lancement du projet`

**Corps :**
```
{prenom},

Ravi de demarrer ce projet ensemble.

Pour rappel, nos 3 objectifs a 90 jours :
1. {objectif 1 — avec KPI et cible}
2. {objectif 2 — avec KPI et cible}
3. {objectif 3 — avec KPI et cible}

Voici les prochaines etapes :

1. {etape 1 — ex: Kick-off call le {date}}
2. {etape 2 — ex: Transmission des acces}
3. {etape 3 — ex: Livraison de l'audit initial sous 2 semaines}

En attendant, voici ce dont nous avons besoin de votre cote :
- {acces 1}
- {acces 2}

N'hesitez pas a revenir vers moi si vous avez des questions.

{signature}
```

**Regles :** l'email est concret (dates, actions, noms). Pas de blabla corporate.

---

## METADATA

```json
{
  "onboarding_id": "ONBOARDING-{YYYYMMDD}-{entreprise-slug}",
  "pipedrive_deal_id": 0,
  "date_signature": "YYYY-MM-DD",
  "date_onboarding": "YYYY-MM-DD",
  "auteur": "Deal Analyst Agent",
  "version": "8.0",
  "status": "DRAFT",
  "deal_source": "DEAL-{date}-{entreprise}.md",
  "deck_source": "DECK-{date}-{entreprise}.md"
}
```
