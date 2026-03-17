# Pricing Rules — v2.0

> Reference interne. Ce fichier definit la logique de calcul des budgets.
> Les jours et TJM sont INTERNES — jamais affiches dans les outputs clients.

---

## Constantes

| Parametre | Valeur | Modification |
|-----------|--------|-------------|
| **TJM** | 700 EUR HT | Modifier ici si le TJM evolue. Toutes les formules ci-dessous utilisent cette valeur. |

> **Point unique de verite :** le TJM est defini UNIQUEMENT dans ce tableau. Les formules de calcul referent a `TJM` comme variable, pas a une valeur en dur. Si le TJM change, modifier cette seule ligne suffit.

---

## Audit SEO (ponctuel)

L'audit est le socle de tout engagement. Prix fixe + options.

### Socle

| Composant | Prix | Condition |
|-----------|------|-----------|
| **Audit SEO** (strategie + technique) | 3 500 EUR HT | Toujours inclus |

Contenu interne (jamais au client) : etude lexicale, diagnostic technique, benchmark concurrentiel, plan d'action priorise.

### Options audit

| Option | Prix | Condition d'activation |
|--------|------|------------------------|
| **+1 levier** (GEO, SEA, Multicanal) | +1 400 EUR / levier | Si le levier est dans le perimetre |
| **Environnement technique complexe** | +1 400 EUR | Headless, multi-domaines, stack custom, etc. |

### Calcul budget audit

```
budget_audit = 3 500
             + 1 400 x nb_leviers_additionnels
             + 1 400 (si env complexe)
```

### Pack Refonte (separe)

Le pack Refonte est un projet a part, vendu separement quand il y a une creation ou refonte de site.

| Volumetrie | Jours | Budget |
|------------|-------|--------|
| Site simple (< 200 URLs) | 3 | 2 100 EUR |
| Site moyen (200-1000 URLs) | 4 | 2 800 EUR |
| Site volumetrique (1000+ URLs) | 5-6 | 3 500-4 200 EUR |

Contenu interne : AMOA SEO + plan redirections + recette & monitoring post-bascule.

---

## Phase 1 — 90 jours (bloc)

Phase 1 = audit + 3 mois d'accompagnement. Vendu comme un bloc unique.

### Calcul budget Phase 1

```
budget_phase1 = budget_audit + (budget_mensuel x 3)
```

### Exemples

| Profil | Audit | Mensuel | Phase 1 (bloc) |
|--------|-------|---------|----------------|
| SEO seul, pilotage (1j/mois) | 3 500 | 700 | 5 600 EUR |
| SEO seul, production (2j/mois) | 3 500 | 1 400 | 7 700 EUR |
| SEO seul, acceleration (3j/mois) | 3 500 | 2 100 | 9 800 EUR |
| SEO + GEO, production | 4 900 | 2 100 | 11 200 EUR |
| SEO + SEA, production | 4 900 | 2 100 | 11 200 EUR |

---

## Accompagnement mensuel (recurrent, post-Phase 1)

Apres le bilan a 90 jours, l'accompagnement continue **sans engagement**, ajustable chaque mois.

### Intensite du socle Search

| Niveau | Label client | Ce que SLASHR fait | Ce que le client fait | Jours/mois | Budget |
|--------|-------------|-------------------|----------------------|-----------|--------|
| **Pilotage** | "On pilote, vous executez" | Strategie, specs, monitoring | Produit et implemente | 1 | 700 EUR/mois |
| **Production** | "On produit, vous validez" | Strategie + production contenu + optimisations | Valide | 2 | 1 400 EUR/mois |
| **Acceleration** | "On accelere" | Tout + liens externes + couverture elargie | Valide | 3 | 2 100 EUR/mois |

### Leviers additionnels

| Levier | Jours/mois | Budget |
|--------|-----------|--------|
| +1 levier (GEO, SEA, Multicanal) | +1 | +700 EUR/mois |

### Calcul budget mensuel

```
budget_mensuel = (socle_jours + nb_leviers) x TJM
```

---

## Regles d'affichage dans la proposition client

### Ce que le client VOIT (HTML)

Phase 1 (90 jours) :
- "Audit SEO" (pas juste "Audit")
- Description qualitative de ce que la mission inclut (pas de jours)
- Budget global HT (bloc unique = audit + 3 mois)
- Ce que ca produit (livrables nommes)
- "Mise en place du reporting" (pas "Reporting mensuel")
- Benchmark concurrentiel (sans s'engager sur le nombre d'acteurs)
- **Non inclus** (obligatoire) : lister explicitement ce qui n'est pas dans la Phase 1 (ex: audit GEO, audit Social Search). "Ces leviers peuvent etre actives apres le bilan, en accelerateur."

Accompagnement mensuel :
- 1 recommandation mise en avant (pas 3 tiers egaux)
- Echelle de lecture en 4 colonnes alignees : Pilotage / Production / Acceleration / +Levier accelerateur
- Labels client : "On pilote, vous executez" / "On produit, vous validez" / "On accelere"
- Leviers additionnels : +700 EUR/mois par levier ("Acceleration SEO, visibilite IA, Ads, reseaux sociaux")
- Budget mensuel HT
- Budget annee 1 (Phase 1 + 9 mois accompagnement)
- **Budget achat de liens** : mentionner explicitement "non inclus, facture a part selon la strategie definie"
- **Sans engagement** : l'accompagnement post-Phase 1 est sans engagement, ajustable apres le bilan

### Recap budget (slide dedie dans l'onglet Investissement)

- **Slide separe** du pricing : vue consolidee sur 2 colonnes (annee 1 / annee 2)
- **Objectif par phase** : chaque phase porte un objectif qualitatif (ex: "Poser les fondations" / "Accelerer vers 200K de CA")
- **Budget media** : ligne separee sous l'accompagnement SLASHR, avec mention "minimum pressenti, ajustable selon la strategie et la saisonnalite"
- **Total global** : hero gradient avec le montant total HT
- **Footnote** : "Sans engagement sur la Phase 2"

### Ce que le client NE VOIT PAS

- Nombre de jours
- TJM
- Decomposition interne (etude lexicale, benchmark, AMOA, etc.)
- Calculs intermediaires

### Ou sont les jours ?

Dans le fichier `INTERNAL-S7-{date}-{prospect}.md` — section "Budget interne".
Le closer a acces au detail complet. Le prospect ne voit que le budget et le scope.
