# Templates Relance Post-R2 — v1.0

## Contexte

Ces templates s'activent quand R2 est terminée sans signature.
Chaque template contient des variables à remplir par le Closing Coach à partir du brief R1 et des data DataForSEO.

**Règle absolue : chaque relance apporte de la valeur nouvelle. Zéro "je me permets de revenir vers vous".**

---

## Touch 1 — J+5 : L'insight

**Objet** : `{prénom}, {data_point} sur votre marché`

**Corps** :

```
{prénom},

En préparant votre dossier, j'ai identifié un point que je n'avais pas mentionné en R2.

{insight_personnalisé}

Concrètement : {implication_business_chiffrée}.

C'est le type de quick win qu'on adresse dans les 90 premiers jours.

Voulez-vous qu'on cale le démarrage cette semaine ou la suivante ?

{signature}
```

**Variables** :
- `{insight_personnalisé}` : donnée DataForSEO non partagée en R2 (keyword gap, concurrent qui accélère, perte de positions récente)
- `{implication_business_chiffrée}` : traduction en euros / leads / parts de marché

**Règle** : l'insight doit être réel et vérifiable. Pas de bluff.

---

## Touch 2 — J+12 : L'urgence douce

**Objet** : `Fenêtre de timing sur {secteur_prospect}`

**Corps** :

```
{prénom},

Je reviens vers vous avec un élément de contexte.

{élément_temporel} — ce qui signifie que {conséquence_si_inaction}.

Les entreprises qui lancent maintenant captent {bénéfice_chiffré} avant {deadline_naturelle}.

On avait identifié ensemble que {rappel_douleur_R1}. Le timing joue en votre faveur si on démarre avant {date_limite}.

Dites-moi si c'est toujours dans vos priorités.

{signature}
```

**Variables** :
- `{élément_temporel}` : saisonnalité, algo update, mouvement concurrent, fin de quarter
- `{conséquence_si_inaction}` : ce que le prospect perd en attendant
- `{rappel_douleur_R1}` : verbatim ou douleur identifiée en R1

**Règle** : l'urgence doit être factuelle (data, date, événement). Jamais artificielle.

---

## Touch 3 — J+20 : Le closer

**Objet** : `{entreprise_prospect} — on fait le point ?`

**Corps** :

```
{prénom},

Je préfère être direct.

On a identifié {résumé_opportunité_1_ligne} et je pense qu'on peut délivrer {résultat_attendu}.

Si c'est toujours un sujet, je vous propose qu'on cale 15 min cette semaine pour valider les modalités de démarrage.

Si les priorités ont changé, dites-le moi — je préfère une réponse claire à un silence.

{signature}
```

**Variables** :
- `{résumé_opportunité_1_ligne}` : synthèse en 1 phrase de l'opportunité SLASHR
- `{résultat_attendu}` : le ROI ou output concret promis

**Règle** : cette touch est la dernière. Si pas de réponse → deal marqué "Lost — Ghosting" dans Pipedrive. Pas de Touch 4.

---

## Règles transversales

- **Canal unique : email** — pas de LinkedIn, pas de SMS, pas de call non sollicité
- **Personnalisation obligatoire** — si le Closing Coach ne peut pas remplir les variables, la relance ne part pas
- **Espacement strict** — J+5, J+12, J+20. Pas de raccourcissement
- **Tracking** — chaque email tracké (ouverture, clic) via Pipedrive
- **Sortie propre** — après Touch 3 sans réponse, archivage automatique + tag "revisit_Q+1"
