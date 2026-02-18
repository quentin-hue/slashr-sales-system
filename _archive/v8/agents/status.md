# Mode STATUS — Vue rapide deal (v8.0)

> **Commande legere. Pas de fichier genere. Affichage inline uniquement.**

---

## Input

Pipedrive deal data uniquement :
- Deal (titre, stage, value, custom fields, add_time)
- Contact (prenom, email)
- Derniere activite (date, type)

**Pas de Google Drive. Pas de DataForSEO.**

---

## Donnees a extraire

1. Titre du deal + stage actuel + deal value
2. r1_score, r1_verdict, r1_fiabilite (si renseignes)
3. relance_status (si applicable)
4. Derniere activite (date + type)
5. Contact principal (prenom + email)
6. Anciennete du deal (jours depuis creation)
7. Jours depuis derniere activite

Reference field keys : `context/pipedrive_reference.md`

---

## Format de sortie — inline (pas de fichier)

```
=== STATUS: {deal_title} (#{deal_id}) ===

Stage       : {stage_name}
Valeur      : {deal_value} EUR
Anciennete  : {X} jours (cree le {add_time})
Score R1    : {score}/100 — {verdict} (fiabilite: {fiabilite})
Contact     : {prenom} ({email})
Relances    : {relance_status | "N/A"}
Derniere activite : {date} — {type_activite} ({Y} jours)
Prochaine etape   : {next_step}
{alerte si applicable}
===
```

Si score/verdict/fiabilite non renseignes -> afficher "Non renseigne".

**Alerte STALE :** si derniere activite > 7 jours ET pas de progression de stage recente -> ajouter :
`⚠ STALE — {X} jours sans activite. Relancer ou archiver.`

---

## Logique "prochaine etape"

| Stage actuel | Prochaine etape recommandee |
|-------------|---------------------------|
| Lead In | Planifier R1 |
| R1 Scheduled | Attendre R1, preparer les 5 questions |
| R1 Done | `/analyse {deal_id}` |
| R2 Scheduled | `/deck {deal_id}` si pas fait. Valider Pre-R2 Checklist |
| R2 Done | `/relances {deal_id}` si 48h+ sans signature |
| Pending Signature | `/onboarding {deal_id}` |

Si relance_status est renseigne, preciser :
- PAS_COMMENCEE -> "Envoyer Touch 1 (J+5)"
- J5_ENVOYEE -> "Attendre J+12 pour Touch 2"
- J12_ENVOYEE -> "Attendre J+20 pour Touch 3"
- J20_ENVOYEE -> "Attendre reponse. Si silence -> Lost — Ghosting"
- REPONSE -> "Traiter la reponse"
