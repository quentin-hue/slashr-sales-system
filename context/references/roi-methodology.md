# ROI Methodology — 3 methodes standard

> Reference on-demand. L'IA choisit la methode la plus adaptee au deal et l'applique de facon reproductible. Si aucune methode n'est applicable, l'IA le dit et ne produit pas de ROI.

## Methode A : Gap CTR (quand GSC est disponible)

**Quand :** donnees GSC disponibles, le prospect a du trafic existant a optimiser.

```
ROI = (trafic actuel x (CTR cible - CTR actuel)) x taux conversion x panier moyen x 12 mois
```

- **CTR actuel** : GSC, 90 derniers jours (÷3 pour mensuel)
- **CTR cible** : benchmark position cible (position 1 = ~28%, position 3 = ~11%, position 5 = ~6%)
- **Taux conversion** : donnees prospect si disponibles, sinon benchmark sectoriel (source a citer)
- **Panier moyen** : donnees prospect si disponibles, sinon estimation conservatrice

**Confiance :** High (si GSC + CVR reel), Medium (si GSC + CVR estime)

## Methode B : Gap concurrent (quand le benchmark est clair)

**Quand :** le gap concurrentiel est mesurable, le prospect peut raisonnablement atteindre le niveau du #3.

```
ROI = (trafic concurrent #3 x part capturable) x taux conversion x panier moyen x 12 mois
```

- **Trafic concurrent #3** : DataForSEO domain_rank_overview
- **Part capturable** : 30-50% du trafic hors-marque du concurrent (conservateur)
- **Taux conversion / Panier moyen** : memes sources que Methode A

**Confiance :** Medium (estimations DataForSEO + hypothese de captation)

## Methode C : Volume adressable (quand le marche est quantifie)

**Quand :** TASM calcule (Module 4c), le prospect part de loin.

```
ROI = (volume captable x CTR position cible) x taux conversion x panier moyen x 12 mois
```

- **Volume captable** : TASM commercial + info captable (hors non-captable)
- **CTR position cible** : CTR moyen top 10 (~3-5% pour position 5-10)
- Appliquer un facteur de realisme : 20-40% du volume captable en annee 1

**Confiance :** Low-Medium (projections a long terme, beaucoup d'hypotheses)

## Regles transverses

1. **Toujours presenter une fourchette** (scenario conservateur + optimiste), pas une valeur unique
2. **Lister toutes les hypotheses** dans le simulateur ROI (source + methode de validation)
3. **Ne jamais promettre** : "potentiel estime" pas "vous allez gagner"
4. **Si les donnees sont insuffisantes** : ne pas calculer de ROI. Dire "ROI non calculable sans donnees de conversion. A valider en Phase 1."
5. **Le ROI le plus credible gagne** : si Methode A est applicable, elle prime sur B et C
