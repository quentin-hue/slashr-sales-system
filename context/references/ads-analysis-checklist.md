# Checklist d'analyse Google Ads pre-diagnostic

> Lu par l'IA apres la collecte Google Ads et avant le diagnostic.
> Chaque question doit etre repondue avec des donnees. Si la donnee manque, noter dans les MANQUANTS.
>
> **Pre-requis** : donnees Google Ads collectees (campaigns, search_terms, quality_scores si dispo).
> Si Google Ads non disponible, cette checklist est skippee.

---

## 1. Structure du compte

- [ ] **Combien de campagnes actives, par type ?** Compter Search, PMax, Display, Video, Shopping. Un compte avec 50+ campagnes Search pilotees par un freelance seul est un signal de sur-fragmentation. [src: google-ads campaigns] {CRITICAL}
- [ ] **Quelle strategie d'encheres par campagne ?** Lister : tCPA, tROAS, mCPC, Maximize Clicks, Maximize Conversions, Maximize Impression Share. Un mix incoherent (tCPA + mCPC + MaxImpression sur le meme compte) est un signal de manque de strategie. [src: google-ads bidding_strategy_type] {HIGH}
- [ ] **Comment le compte est-il structure ?** Par pays, par ville, par service, par type de campagne ? Y a-t-il une logique ou c'est un empilement historique ? [src: google-ads campaign names] {HIGH}
- [ ] **Y a-t-il une campagne brand separee ?** Si oui, quel budget, quelles conversions ? Si le brand est dans les campagnes generiques ou PMax sans exclusion, l'attribution est faussee. [src: google-ads search_term_view filtre marque] {HIGH}

---

## 2. Performance par segment

- [ ] **CPA par type de campagne ?** Comparer PMax vs Search vs Display. Un ecart > 3x entre le meilleur et le pire type indique un probleme de mix. [src: google-ads campaigns, 90j] {CRITICAL}
- [ ] **CPA par zone geographique ?** Comparer pays, regions, villes. Des ecarts > 2x entre zones signalent un besoin de reventilation budgetaire. [src: google-ads campaigns par geo] {CRITICAL}
- [ ] **Top 5 et bottom 5 campagnes par CPA ?** Les top performers sont les modeles a scaler. Les bottom performers sont les candidats a la pause ou restructuration. Calculer : si le budget des bottom 5 etait reaffecte aux top 5, combien de conversions additionnelles ? [src: google-ads campaigns] {CRITICAL}
- [ ] **Impression share par campagne Search ?** < 30% = le prospect rate 70%+ de la demande. Diagnostiquer pourquoi : budget insuffisant (budget_lost) ou rank insuffisant (rank_lost). [src: google-ads search_impression_share] {HIGH}
- [ ] **Y a-t-il des campagnes avec < 5 conversions sur 90 jours ?** Ce sont des campagnes sans assez de signal pour que l'algo optimise. Candidats a la consolidation. [src: google-ads campaigns, 90j] {HIGH}

---

## 3. Search terms et conversion

- [ ] **Quels search terms convertissent ?** Top 20 par conversions. Distinguer marque vs generique vs local. Le top convertisseur est-il la marque du prospect ? Si oui, combien depense-t-il pour acheter sa propre marque ? [src: google-ads search_term_view] {CRITICAL}
- [ ] **Les search terms qui convertissent sont-ils couverts en organique ?** Croiser avec GSC : overlap = economie potentielle. Paid-only converters = priorites SEO. [src: google-ads x gsc] {HIGH}
- [ ] **Y a-t-il du gaspillage sur les termes de recherche ?** Chercher les search terms a fort cout et 0 conversion. Sont-ils negatifs ? [src: google-ads search_term_view, filtre conversions=0, orderings cost DESC] {MEDIUM}

---

## 4. Synergie paid / organic

- [ ] **Le prospect achete-t-il ses propres clics de marque ?** Conversions paid sur le nom de marque vs position organique. Si position 1 organique avec sitelinks, le budget marque est defensif, pas offensif. [src: google-ads search_term_view marque + gsc query marque] {HIGH}
- [ ] **Le concurrent achete-t-il la marque du prospect ?** Verifier la SERP marque (annonces concurrentes ? PAA du concurrent ?). Si oui, un budget brand defensif est justifie. Si non, reduire. [src: serp_organic sur requete marque] {HIGH}
- [ ] **Les landing pages Ads sont-elles les memes que les pages organiques ?** Si oui, le SEO nourrit le quality score. Si non (ex: domaine separe comme reset-laser.com), il y a une dilution. [src: google-ads campaign urls + sitemap] {MEDIUM}

---

## 5. Recommandations actionables

Pour chaque probleme identifie, la recommandation doit etre CONCRETE et CHIFFREE :

**Format obligatoire :**
```
PROBLEME : {description factuelle + chiffres}
ACTION : {ce qu'on fait concretement}
IMPACT ESTIME : {combien de conversions / EUR gagnes/economises}
HORIZON : {M1 / M2 / M3}
CONFIANCE : {HIGH / MEDIUM / LOW}
```

**Exemples de recommandations granulaires (pas des generalites) :**

BON :
- "Pauser Nancy (CPA 275 EUR, 1 conv/mois). Reaffecter les 275 EUR vers PMax France (CPA 10.9 EUR) = ~25 conversions additionnelles. M1. HIGH."
- "Migrer Troyes, Valenciennes, Lens de mCPC vers tCPA 25 EUR. Impact attendu : -30% CPA sur ces campagnes (benchmark des campagnes deja en tCPA sur le compte). M1. MEDIUM."
- "Reduire le budget brand Search de 850 a 250 EUR/mois. Reaffecter 600 EUR vers Concurrence (impression share 18% → ~35%). M1. HIGH."

MAUVAIS :
- "Optimiser les campagnes" (vague, pas actionable)
- "Restructurer le compte" (comment ?)
- "Reduire le CPA" (de combien ? sur quelles campagnes ?)

---

## Output attendu

Apres la checklist, l'IA ecrit dans le SDB :

```
GOOGLE ADS ANALYSIS:

STRUCTURE :
- {N} campagnes actives ({N} Search, {N} PMax, {N} autres)
- Strategies encheres : {mix}
- Logique structure : {pays/ville/service/mix}

PERFORMANCE (90 jours) :
- Budget total : {N} EUR ({N}/mois)
- Conversions : {N} | CPA moyen : {N} EUR | CVR : {N}%
- Top 3 : {campagne} CPA {N}, {campagne} CPA {N}, {campagne} CPA {N}
- Bottom 3 : {campagne} CPA {N}, {campagne} CPA {N}, {campagne} CPA {N}
- Ecart top/bottom : {N}x

SEARCH TERMS :
- Top convertisseur : "{term}" ({N} conv, {marque/generique/local})
- Achat marque : {N} conv, {N} EUR/mois sur la marque
- Overlap paid/organic : {N} requetes communes

RECOMMANDATIONS :
1. {PROBLEME → ACTION → IMPACT → HORIZON → CONFIANCE}
2. {idem}
3. {idem}

ESTIMATION IMPACT GLOBAL :
- Budget constant : {N} EUR/mois
- CPA cible : {N} EUR (actuel : {N} EUR)
- Conversions cible : {N}/mois (actuel : {N}/mois)
- Economie reallocation : {N} EUR/mois
```
