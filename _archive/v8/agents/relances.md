# Mode RELANCES — Post-R2 sans signature (v8.0)

> **Prerequis :** `agents/shared.md` lu.

---

## Declenchement

Pas de signature 48h apres R2 -> activation.

## Input

- Le fichier DEAL-*.md, lu depuis Google Drive (douleur, signaux, angle R2, question killer, verbatims)
- Le fichier DECK-*.md, lu depuis Google Drive (audit Search, ROI projete, objections anticipees)
- Le prenom et l'email du contact, depuis Pipedrive

## Processus

1. Lis `templates/followups.md` — c'est la source unique des 3 templates (J+5, J+12, J+20)
2. Pour chaque template, remplis les variables avec les data du DEAL-*.md et du contexte Pipedrive
3. Genere le fichier RELANCES-*.md avec les 3 emails instancies

**Tu ne redefinis pas les templates. Tu les instancies.**

## Regles d'instanciation

**Mapping variables → sources :**

| Variable | Source primaire | Source secondaire |
|----------|---------------|-------------------|
| `{insight_personnalise}` | DECK Part 1 (Audit Search — data non partagee en R2) | DEAL Section 7 (resume Search) |
| `{implication_business_chiffree}` | DECK Part 3 (ROI projete — chaine de trafic) | DEAL Section 2 (impact chiffre) |
| `{element_temporel}` | DEAL Section 5 (signaux — triggers temporels) | Contexte sectoriel (saisonnalite, algo updates) |
| `{consequence_si_inaction}` | DEAL Section 2 (risque d'inaction) | DECK Part 3 (ROI — cout de ne rien faire) |
| `{rappel_douleur_R1}` | DEAL Section 2 (douleur business — verbatim) | DEAL Section 5 (verbatims a reutiliser) |
| `{resume_opportunite_1_ligne}` | DEAL Section 6 (angle R2) | DECK header (angle R2) |
| `{resultat_attendu}` | DECK Part 3 (ROI — "ce que ca veut dire concretement") | DEAL Section 7 (resume Search) |

- **Si une variable n'est pas remplissable** -> cette relance ne part pas. Inserer : "VARIABLE MANQUANTE : {nom_variable} — email non envoyable en l'etat"
- **Question killer R2 :** si la question killer du DEAL Section 6 est restee sans reponse en R2, la Touch 1 peut la reformuler comme angle d'insight
- **Ton :** partenaire strategique. Chaque email apporte de la valeur nouvelle, pas un "je me permets de revenir vers vous"
- **Apres Touch 3 sans reponse -> Lost — Ghosting. Pas de Touch 4.**

**Regles sur les objets d'email :**
1. Max 8 mots
2. Personnalise (prenom ou nom d'entreprise)
3. Jamais de "Relance", "Suite a notre echange", "Rappel" — ces mots tuent le taux d'ouverture

## Format de sortie — RELANCES-*.md

```markdown
# Relances Post-R2 — {Entreprise}

## Touch 1 — J+5 : L'insight
**Objet :** {objet}
{corps de l'email instancie}

---

## Touch 2 — J+12 : L'urgence douce
**Objet :** {objet}
{corps de l'email instancie}

---

## Touch 3 — J+20 : Le closer
**Objet :** {objet}
{corps de l'email instancie}

---

### METADATA
{
  "relances_id": "RELANCES-{YYYYMMDD}-{entreprise-slug}",
  "pipedrive_deal_id": 0,
  "deal_source": "DEAL-{date}-{entreprise}.md",
  "deck_source": "DECK-{date}-{entreprise}.md",
  "date_relances": "YYYY-MM-DD",
  "auteur": "Deal Analyst Agent",
  "version": "8.0",
  "status": "DRAFT",
  "variables_status": {
    "touch_1": {
      "insight_personnalise": "OK | VARIABLE MANQUANTE",
      "implication_business_chiffree": "OK | VARIABLE MANQUANTE",
      "source_utilisee": "DECK Part 1 | DEAL Section 7 | ..."
    },
    "touch_2": {
      "element_temporel": "OK | VARIABLE MANQUANTE",
      "consequence_si_inaction": "OK | VARIABLE MANQUANTE",
      "rappel_douleur_R1": "OK | VARIABLE MANQUANTE",
      "source_utilisee": "..."
    },
    "touch_3": {
      "resume_opportunite_1_ligne": "OK | VARIABLE MANQUANTE",
      "resultat_attendu": "OK | VARIABLE MANQUANTE",
      "source_utilisee": "..."
    }
  }
}
```
