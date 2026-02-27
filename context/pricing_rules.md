# Pricing Rules — v1.0

> Reference interne. Ce fichier definit la logique de calcul des budgets Phase 1 et Phase 2.
> Les jours et TJM sont INTERNES — jamais affiches dans les outputs clients.

---

## Constantes

| Parametre | Valeur | Modification |
|-----------|--------|-------------|
| **TJM** | 700 EUR HT | Modifier ici si le TJM evolue. Toutes les formules ci-dessous utilisent cette valeur. |

> **Point unique de verite :** le TJM est defini UNIQUEMENT dans ce tableau. Les formules de calcul referent a `TJM` comme variable, pas a une valeur en dur. Si le TJM change, modifier cette seule ligne suffit.

---

## Phase 1 — Mission structurante (ponctuelle)

Phase 1 = mission calibree selon les blocs actives. Ce n'est PAS un pack.

### Blocs Phase 1

| Bloc | Jours | Condition d'activation | Contenu interne (jamais au client) |
|------|-------|------------------------|-------------------------------------|
| **Audit SEO** | 5 (fixe) | Toujours actif | Etude lexicale + diagnostic technique + benchmark concurrentiel |
| **Refonte SEO** | 3 a 6 (selon volumetrie) | Si refonte prevue | AMOA SEO + plan redirections + recette & monitoring post-bascule |
| **Activation contenu** | 1 (minimum) | Toujours actif | Specification pages piliers prioritaires |
| **SEA setup** | 2 (incompressible) | Si SEA_POSTURE = PILOTE ou CONSEIL | Cabinet conseil — strategie et architecture, pas execution quotidienne. PILOTE : audit campagnes + structure compte + strategie encheres + plan activation 90j. CONSEIL : audit strategique + recommandations structure + cahier des charges pour equipe execution. |
| **GEO setup** | 2 (incompressible) | Si GEO/IA dans le perimetre | Audit visibilite IA + donnees structurees + strategie GEO |
| **Social setup** | 2 (incompressible) | Si Social Search dans le perimetre | Audit presence sociale + strategie Social Search |

### Calcul budget Phase 1

```
jours_phase1 = audit_seo (5)
             + refonte_seo (3-6, si applicable)
             + activation_contenu (1)
             + sea_setup (2, si applicable)
             + geo_setup (2, si applicable)
             + social_setup (2, si applicable)

budget_phase1 = jours_phase1 x TJM
```

### Variable : Refonte SEO

Le nombre de jours Refonte s'adapte a la volumetrie :

| Volumetrie | Jours |
|------------|-------|
| Site simple (< 200 URLs) | 3 |
| Site moyen (200-1000 URLs) | 4 |
| Site volumetrique (1000+ URLs) | 5-6 |

---

## Phase 2 — Orchestration mensuelle (recurrente)

Chaque levier active en Phase 1 implique un run mensuel incompressible.

### Run mensuel par levier

| Levier | Jours/mois (minimum incompressible) |
|--------|--------------------------------------|
| **SEO run** | 1 |
| **SEA run** | 1 | Pilotage strategique : revue performance mensuelle, ajustements strategie, recommandations. Pas de bid management quotidien. |
| **GEO run** | 1 |
| **Social run** | 1 |

### Niveaux d'intensite

L'intensite determine le nombre total de jours/mois. Les incompressibles sont le plancher.

| Niveau | Jours/mois | Profil |
|--------|-----------|--------|
| **Essentiel** | 1-2 | PME, execution internalisee, pilotage + monitoring |
| **Performance** | 2-3 | ETI, execution deleguee, production incluse |
| **Croissance** | 3-4+ | Grands comptes, multi-leviers, ambition forte |

### Calcul budget Phase 2

```
jours_mensuels = somme des incompressibles par levier active
               + jours supplementaires selon intensite

budget_mensuel = jours_mensuels x TJM
```

### Exemples de calcul

**Exemple 1 — SEO seul, Performance :**
- SEO run : 1j incompressible + 2j production = 3j/mois
- Budget : 3 x 700 = 2 100 EUR/mois

**Exemple 2 — SEO + SEA, Performance :**
- SEO run : 1j + 1j production = 2j
- SEA run : 1j + 0,5j optimisation = 1,5j
- Total : 3,5j/mois → 2 450 EUR/mois

**Exemple 3 — SEO + GEO + Social, Croissance :**
- SEO run : 1j + 2j production = 3j
- GEO run : 1j
- Social run : 1j
- Total : 5j/mois → 3 500 EUR/mois

---

## Scenarios types (reperes, pas formules figees)

| Scenario | Phase 1 (exemple SEO + refonte) | Phase 2 |
|----------|--------------------------------|---------|
| **Essentiel** | Audit (5j) + Refonte (3j) + Contenu (1j) = 9j → 6 300 EUR | 1-2j/mois → 700-1 400 EUR/mois |
| **Performance** | Audit (5j) + Refonte (4j) + Contenu (1j) = 10j → 7 000 EUR | 2-3j/mois → 1 400-2 100 EUR/mois |
| **Croissance** | Audit (5j) + Refonte (4j) + Contenu (1j) + GEO (2j) = 12j → 8 400 EUR | 3-4j/mois → 2 100-2 800 EUR/mois |

> Ces chiffres sont des reperes. Claude adapte au deal.

---

## Regles d'affichage dans la proposition client

### Ce que le client VOIT (HTML)

Phase 1 :
- Description qualitative de ce que la mission inclut (pas de jours)
- Budget global HT
- Ce que ca produit (livrables nommes)

Phase 2 :
- Description qualitative par niveau d'intensite
- Budget mensuel HT
- Ce que ca inclut (scope nomme)

### Ce que le client NE VOIT PAS

- Nombre de jours
- TJM
- Decomposition interne des blocs (etude lexicale, diagnostic, benchmark, AMOA, redirections, recette...)
- Calculs intermediaires

### Ou sont les jours ?

Dans le fichier `INTERNAL-S7-{date}-{prospect}.md` — section "Budget interne".
Le closer a acces au detail complet. Le prospect ne voit que le budget et le scope.
