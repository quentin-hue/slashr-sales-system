# Mode BENCHMARK : Analyse concurrentielle standalone (v12.0)

> **Prerequis :** `agents/shared.md` lu.

---

## Objectif

Analyse concurrentielle standalone. Comparer le prospect a ses concurrents Search pour preparer les arguments du closer avant R2.

---

## Collecte

### DataForSEO (prospect)
- `domain_rank_overview` → trafic, keywords, ETV
- `ranked_keywords` (top 30) → keywords, positions

### DataForSEO (concurrents)
- `competitors_domain` (top 10) → identification concurrents
- Filtrage : bruit (facebook, pagesjaunes, wikipedia) vs semantique (ouest-france, amazon) vs business (meme secteur)
- `domain_rank_overview` x top 5 concurrents business
- `domain_intersection` prospect vs top 3 → keywords communs et exclusifs

### Module 4c (conditionnel)
Si `competitors_domain` ne remonte aucun concurrent business :
- Selectionner 5-8 keywords commerciaux cles
- `serp_organic_live_regular` pour chaque → extraire les domaines recurrents
- `domain_rank_overview` des concurrents niche identifies

---

## Analyse

### Gap de trafic
- Ratio trafic prospect / trafic leader
- Evolution potentielle si le prospect atteint le niveau du #3

### Keywords exclusifs
- Keywords que chaque concurrent a et pas le prospect
- Grouper par intent (informationnelle, commerciale, transactionnelle)
- Volume total adressable

### Positionnement semantique
- Univers semantiques couverts par le prospect vs concurrents
- Trous dans la couverture

### Opportunites
- Top 10 keywords a fort volume que le prospect ne couvre pas
- Pages types a creer (categories, guides, comparatifs)
- Quick wins (keywords en position 5-20)

---

## Regles

1. **Filtrage strict des concurrents.** Pas de bruit (annuaires, reseaux sociaux). Classifier chaque domaine.
2. **Donnees sourcees.** Chaque chiffre avec [src: dataforseo, endpoint, date].
3. **Pas de proposition.** C'est une analyse, pas un delivrable client.
4. **Cache reutilise.** Si un /prepare a deja collecte les donnees concurrentielles, les reutiliser.
5. **Concurrents manuels.** Si le closer fournit des concurrents via --competitors, les prioriser.
