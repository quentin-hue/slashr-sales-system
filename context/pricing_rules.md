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

> **Note (v13.6) :** Pour les deals avec refonte, l'AMOA SEO est integree dans les mois de production (Phase 1 M2-M4), pas vendue comme pack separe. Le bilan de Phase 1 intervient quand le site est en production, pas a M4 calendaire. L'accompagnement run peut demarrer avant la MEP avec accord du client.

---

## Phase 1 — 4 mois (engagement)

Phase 1 = audits + 3 mois d'execution. Vendu comme un bloc unique de 4 mois.

**Pourquoi 4 mois :** 1 mois d'audit + 3 mois d'execution = assez de temps pour obtenir des resultats ou a minima des signaux positifs. Le client ne decide de la Phase 2 qu'apres avoir vu des resultats concrets.

**Bilan de fin de Phase 1 :** obligatoire. Revue des resultats, ajustement du perimetre Phase 2 si besoin (intensite SEO, ajout de leviers, couverture internationale, acceleration GEO).

### Structure Phase 1

```
Phase 1 = Mois 1 (audits) + Mois 2-4 (execution au tarif Phase 2)
budget_phase1 = budget_audits + (budget_mensuel_phase2 x 3)
```

### Audits (livrables separes dans le devis, mais vendus dans le bloc Phase 1)

| Audit | Prix | Contenu |
|-------|------|---------|
| **Audit SEO** | 3 500 EUR HT | Architecture, contenu, blog, liens internes, SXO, donnees structurees, benchmark |
| **Audit SEA** | 1 400 EUR HT | Structure campagnes, encheres, cannibalisation PMax, conformite reglementaire, cartographie par pays |
| **Audit GEO** (option) | 1 400 EUR HT | Visibilite IA (ChatGPT, Gemini, Perplexity), positionnement vs concurrents |

> **L'audit SEO est TOUJOURS complet** : architecture, contenu, technique, blog, liens internes, SXO. Jamais "audit SEO local" ou "audit technique" seul. Le local est un axe de l'audit, pas l'audit entier.

### Exemples Phase 1

| Profil | Audits | Mensuel (M2-M4) | Phase 1 (bloc 4 mois) |
|--------|--------|-----------------|----------------------|
| SEO seul, production (2j/mois) | 3 500 | 1 400 | 7 700 EUR |
| SEO + SEA, production (2j SEO + 2j Ads) | 4 900 | 2 800 | 13 300 EUR |
| SEO + SEA + GEO, production | 6 300 | 2 800 | 14 700 EUR |
| SEO + SEA, acceleration (3j SEO + 2j Ads) | 4 900 | 3 500 | 15 400 EUR |

---

## Phase 2 — Run mensuel (sans engagement)

Apres le bilan Phase 1, l'accompagnement continue **sans engagement**. Le client reste parce qu'il voit les resultats, pas parce qu'il est engage.

Le perimetre Phase 2 est ajuste lors du bilan Phase 1 : intensite SEO, ajout de leviers (GEO, international), couverture geographique.

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

### Accompagnement Google Ads (forfait separe)

| Prestation | Budget | Contenu |
|-----------|--------|---------|
| **Accompagnement Google Ads** | 1 400 EUR/mois HT | Optimisation campagnes, encheres, annonces, landing pages, reporting hebdo, veille |

Le pilotage Ads est un forfait mensuel, pas un "+1 jour". Il inclut le reporting hebdomadaire (vs mensuel pour le SEO) et la gestion active des encheres.

**Hors perimetre :** budget media Google Ads (facture directement par Google au client). Toujours mentionner "hors budget media" dans la proposition.

### Calcul budget mensuel (mise a jour)

```
budget_mensuel = (socle_seo_jours x TJM) + forfait_ads (si applicable)
```

Exemple : Production SEO (2j = 1 400) + Ads (1 400 forfait) = 2 800 EUR/mois

### Calcul budget mensuel (legacy, SEO seul)

```
budget_mensuel = (socle_jours + nb_leviers) x TJM
```

---

## Regles d'affichage dans la proposition client

### Ce que le client VOIT (HTML)

Phase 1 (4 mois) :
- Presenter comme un bloc unique de 4 mois (pas "audit + 3 mois de run")
- Mois 1 : audits (SEO, SEA, GEO option) avec prix individuels visibles
- Mois 2-4 : execution au tarif Phase 2 (meme niveau de service)
- Budget global HT du bloc
- Bilan de fin de Phase 1 mentionne (ajustement perimetre Phase 2)
- **Non inclus** (obligatoire) : lister ce qui n'est pas dans la Phase 1. "Ces leviers peuvent etre actives apres le bilan."

Accompagnement mensuel :
- 1 seule recommandation affichee en hero (pas 3 tiers egaux, pas de grid 3 colonnes)
- Les alternatives mentionnees en 1 ligne sous la recommandation ("Ajustable : Pilotage {budget}/mois ou Acceleration {budget}/mois")
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

Dans le fichier `INTERNAL-DIAG-{date}-{prospect}.md` — section "Budget interne".
Le closer a acces au detail complet. Le prospect ne voit que le budget et le scope.
