# Checklist d'analyse pre-diagnostic

> Lu par l'IA ENTRE la collecte et le diagnostic. Chaque question doit etre repondue avec des donnees.
> Si la donnee manque, noter dans les MANQUANTS du Checkpoint 1.
>
> **Pour ajouter une regle** : ajouter une ligne dans la section appropriee.
> Format : `- [ ] **Question ?** Contexte. [src: outil] {PRIORITE}`

---

## 0. Relire le brief (AVANT TOUT)

Avant de diagnostiquer, revenir aux sources (transcript, brief, notes closer) et repondre a :

- [ ] **Qu'est-ce que le prospect a demande explicitement ?** Pas ce qu'on pense qu'il a besoin, ce qu'il a dit. Citer les verbatims. {CRITICAL}
- [ ] **Quelle est sa priorite declaree ?** Ads ? SEO ? Refonte ? Les deux ? Si le prospect dit "la priorite c'est les Ads", le diagnostic et la proposition doivent ouvrir par les Ads. {CRITICAL}
- [ ] **Quelle est sa douleur ?** Pas un probleme SEO generique, SA douleur a lui. "Mon prestataire est deborde", "la courbe s'inverse", "on est moins bon". {CRITICAL}
- [ ] **Qui d'autre intervient ?** Agence SEO existante ? Freelance Ads ? Agence Meta ? Verifier si on CHALLENGE l'agence en place ou si c'est un vrai partenaire. Ne pas nommer un concurrent comme partenaire. {HIGH}
- [ ] **Le secteur est-il reglemente sur Google Ads ?** Sante, addiction, finance, alcool, cannabis, pharma. Verifier la politique Google Ads. Si oui, ajouter un slide reglementation et inclure la verification certification dans l'audit Phase 1. {HIGH}
- [ ] **Le prospect opere-t-il a l'international ?** Verifier les pays dans les campagnes Ads et le trafic GSC par pays. Ne jamais exclure un marche important pour le client. Prioriser ≠ exclure. {HIGH}

**REGLE : le diagnostic et la proposition suivent la hierarchie du prospect, pas la hierarchie du systeme.** Si le prospect veut du SEA, on ouvre par le SEA meme si SLASHR est un cabinet SEO. L'expertise SEO est le differenciateur, pas le sujet d'ouverture.

**Output :** ecrire dans le SDB :
```
BRIEF PROSPECT :
- Demande explicite : "{verbatim}"
- Priorite declaree : {Ads / SEO / les deux / refonte / autre}
- Douleur : "{verbatim}"
- Partenaires existants : {liste}
- Ce qui n'a PAS ete demande mais qu'on recommande : {SEO local / GEO / etc.}
```

---

## 1. Conformite reglementaire Google Ads

Si le prospect fait de la publicite Google Ads, verifier AVANT le diagnostic :

- [ ] **Le secteur est-il reglemente par Google Ads ?** Sante, addiction, finance, pharma, gambling, alcool, cannabis, armes, services juridiques. Consulter les politiques Google Ads (Healthcare and medicines, Financial services, Gambling). {CRITICAL}
- [ ] **Une certification Google est-elle requise ?** Certains secteurs (addiction treatment, pharmacie en ligne, services financiers) necessitent une certification Google pour diffuser. Verifier le statut du compte. {CRITICAL}
- [ ] **Y a-t-il des mots-cles / annonces / landing pages a risque ?** Cartographier les termes qui pourraient declencher les filtres (alcool, cannabis, traitement addiction). Risque : refus d'annonces ou suspension du compte. {HIGH}
- [ ] **Le tracking de conversion est-il fiable ?** GA4 installe ? Conversions Google Ads correctement configurees ? Si le tracking est biaise, les CPA affiches sont faux. {HIGH}

**Output :** documenter dans le SDB :
- `COMPLIANCE_STATUS` : SAFE / AT_RISK / UNKNOWN
- `CERTIFICATION_REQUIRED` : YES / NO / TO_VERIFY
- `TRACKING_STATUS` : VERIFIED / UNVERIFIED / BIASED

---

## 2. Multi-site / Multi-pays

Si le prospect a plusieurs etablissements ou opere dans plusieurs pays :

- [ ] **Combien de centres/etablissements ?** Lister par pays. {HIGH}
- [ ] **Quelle repartition du budget Ads par pays ?** Verifier dans Google Ads. Identifier le marche le plus sous-optimise (ratio budget/performance). {HIGH}
- [ ] **Quelle repartition du trafic organique par pays ?** Verifier dans GSC par country. {HIGH}
- [ ] **Les pages locales existent-elles ?** Combien sont indexees ? Quelles donnees structurees ? {HIGH}
- [ ] **La reglementation differe-t-elle par pays ?** Certification Google, restrictions sectorielles, langues. {MEDIUM}
- [ ] **Quels partenaires par marche ?** Agence locale, freelance, equipe interne ? On les CHALLENGE ou on s'ARTICULE ? {HIGH}
- [ ] **Le prospect pense-t-il en centres ou en global ?** Un dirigeant de franchise pense en centres. Adapter la vue (performance par centre dans le diagnostic). {MEDIUM}

**Output :** documenter dans le SDB :
- `MULTI_SITE` : YES ({nb} centres, {nb} pays) / NO
- `MARKET_PRIORITY` : {pays} (justification)
- `PARTNERS_BY_MARKET` : {marche} → {partenaire} (CHALLENGE/ARTICULE)

---

## 0b. Detection du type de business

Identifier le type de business du prospect. Ca determine quelles sections de la checklist sont pertinentes.

| Type | Signaux | Sections prioritaires |
|------|---------|----------------------|
| **Multi-sites / franchise** | Plusieurs adresses, store locator, pages par ville | Structure du site (local), Local packs, GBP, **section 6 (multi-sites)** |
| **E-commerce** | Catalogue produit, panier, fiches produit | Structure du site (produit), Schema Product, Shopping |
| **Service B2B** | Pages service, formulaire de contact, cas clients | Contenu, E-E-A-T, parcours de conversion |
| **Contenu / media** | Blog, articles, actualites | Contenu, E-E-A-T, GEO/IA |
| **Local unique** | 1 adresse, zone de chalandise | Local pack, GBP, avis Google |

---

## 1. Structure du site

- [ ] **Combien de pages par type ?** Parser le sitemap complet (index + sous-sitemaps). Classifier par URL pattern (blog, produit, categorie, local/centre, landing). Ne jamais supposer l'absence d'un type de page sans avoir verifie. [src: sitemap crawl] {CRITICAL}
- [ ] **Les pages strategiques sont-elles indexees ?** `batch_url_inspection` sur 5-10 URLs cles (homepage, top pages, pages locales). Indexe ≠ performant, mais non-indexe = invisible. [src: GSC URL inspection] {HIGH}
- [ ] **Quel est le parcours de conversion ?** Crawler au moins 1 page de chaque type. Verifier : CTA, formulaire, store locator, telephone, prise de RDV. Ne jamais affirmer "pas de CTA" sans preuve. [src: crawl echantillon] {CRITICAL}
- [ ] **Schema present ?** Verifier JSON-LD sur homepage + pages cles. Types attendus selon le business : Organization, LocalBusiness (multi-sites), Product (e-commerce), Article (blog). [src: crawl echantillon] {MEDIUM}

### Gates structure
- **Si 0 page dans le sitemap** → verifier manuellement (le sitemap peut etre absent ou mal configure)
- **Si type de page attendu absent du sitemap** (ex: multi-sites sans pages locales) → verifier par crawl direct avant de conclure

---

## 2. Trafic et performance

- [ ] **D'ou vient le trafic par pays ?** `get_search_analytics` dimensions: country. Un site multilingue peut avoir 60% de trafic hors-cible. Le diagnostic doit porter sur le marche cible. [src: GSC country] {CRITICAL}
- [ ] **Quel type de page genere le trafic ?** Croiser le sitemap (categories) avec GSC (clics par page). Agreger par categorie. "Blog = 90%, pages centres = 4%" change le diagnostic. [src: GSC page + sitemap] {CRITICAL}
- [ ] **Quel est le split marque / hors-marque ?** Filtrer GSC par queries contenant le nom de marque. Trafic 80% brande = dependance notoriete. [src: GSC query] {HIGH}
- [ ] **Quelle est la tendance ?** Daily trend GSC 28 jours. Monte, stagne, descend ? Pattern saisonnier ? [src: GSC performance overview] {MEDIUM}
- [ ] **Quel est le CTR par type de page ?** Les pages blog ont un CTR different des pages locales ou produit. Comparer. Un CTR faible sur des pages bien positionnees = meta titles/descriptions a optimiser. [src: GSC page] {HIGH}

### Gates trafic
- **Si GSC non teste** → STOP, toujours tenter `list_properties` avant de diagnostiquer le trafic
- **Si trafic total utilise sans segmentation pays** → WARN, le diagnostic peut etre fausse

---

## 3. Paid (si Google Ads disponible)

**Si Google Ads est disponible, parcourir la checklist detaillee : `context/references/ads-analysis-checklist.md`**

La checklist Ads couvre 5 axes (16 questions) :
1. **Structure du compte** : nombre de campagnes, types, strategies d'encheres, logique de structure, campagne brand
2. **Performance par segment** : CPA par type, par geo, top/bottom 5, impression share, campagnes < 5 conv
3. **Search terms et conversion** : top convertisseurs, marque vs generique, overlap paid/organic, gaspillage
4. **Synergie paid/organic** : achat marque, concurrent sur la marque, landing pages
5. **Recommandations actionables** : format PROBLEME → ACTION → IMPACT → HORIZON → CONFIANCE

Chaque recommandation doit etre concrete et chiffree. "Optimiser les campagnes" n'est pas une recommandation. "Pauser Nancy (CPA 275 EUR), reaffecter vers PMax (CPA 10.9 EUR) = +25 conversions" en est une.

### Gates paid
- **Si Google Ads non teste** → toujours tenter (champ Pipedrive `gads_customer_id` puis MCC)
- **Si le prospect depense 10K+/mois en paid** → l'analyse Ads est aussi importante que l'analyse SEO, parcourir la checklist Ads en entier
- **Si les recommandations Ads sont vagues** ("restructurer", "optimiser") → STOP, reprendre avec le format PROBLEME → ACTION → IMPACT

---

## 4. Concurrence

- [ ] **Qui sont les vrais concurrents business ?** DataForSEO remonte souvent des medias (santemagazine, doctissimo). Filtrer. Vrais concurrents = meme offre, meme cible. [src: DataForSEO competitors + SERP] {HIGH}
- [ ] **Qui domine les local packs ?** (si multi-sites) Verifier 2-3 SERPs locales. Les local packs sont souvent plus impactants que les resultats organiques. [src: SERP live] {HIGH pour multi-sites}
- [ ] **Gap quantifie ?** Pas "le concurrent est devant" mais "le concurrent a X clics, X keywords, position moyenne Y". Chiffrer le delta. [src: DataForSEO domain_rank_overview] {MEDIUM}

---

## 5. Garde-fous diagnostic

- [ ] **Chaque affirmation est-elle un CONSTAT ou une HYPOTHESE ?** "Pages centres < 500 clics/mois" (constat GSC) vs "les pages centres n'ont pas de CTA" (hypothese non verifiee). Distinguer explicitement. {CRITICAL}
- [ ] **Le diagnostic porte-t-il sur le bon perimetre ?** Si le brief parle de la France, diagnostiquer le trafic francais (19 134 clics), pas le trafic mondial (46 000). [src: GSC country] {CRITICAL}
- [ ] **GSC et Google Ads ont-ils ete croises ?** Si les deux sont dispo, ne jamais diagnostiquer sans les avoir croises. [src: GSC + Google Ads] {HIGH}
- [ ] **Le sitemap a-t-il ete crawle AVANT le diagnostic ?** Si non, risque de diagnostiquer l'absence de pages qui existent. [src: sitemap crawl] {CRITICAL}

---

## 6. Multi-sites / franchise (si type detecte en 0b)

Section conditionnelle. Active uniquement pour les prospects avec plusieurs points de vente/centres.

- [ ] **Performance par centre/ville ?** Si Google Ads disponible : CPA par campagne locale. Si GSC disponible : clics par page centre. Produire un classement top 5 / bottom 5 centres. Le decideur franchise pense en centres, pas en moyennes globales. [src: google-ads campaigns par ville + gsc par page centre] {CRITICAL}
- [ ] **Couverture Ads vs couverture centres ?** Tous les centres ont-ils une campagne dediee ? Y a-t-il des centres sans aucune visibilite paid ? [src: google-ads campaign names vs sitemap centres] {HIGH}
- [ ] **Coherence GBP / site / Ads ?** Les fiches Google Business Profile pointent-elles vers les pages centres du site ? Les campagnes Ads pointent-elles vers les bonnes landing pages (centre local vs landing generique vs second domaine) ? [src: crawl + google-ads] {HIGH}
- [ ] **Le contenu est-il duplique entre les pages centres ?** Crawler 2-3 pages centres et comparer le contenu. Si c'est du copie-colle avec juste le nom de ville qui change, c'est un risque de thin content. [src: crawl echantillon] {MEDIUM}

---

## 7. Ecosysteme partenaires (si partenaires existants detectes en section 0)

Section conditionnelle. Active quand le prospect a deja des prestataires.

- [ ] **Qui fait quoi aujourd'hui ?** Lister les partenaires, leur perimetre, leur anciennete. [src: transcript, brief] {HIGH}
- [ ] **Ou se situe SLASHR dans l'ecosysteme ?** Le perimetre propose doit etre explicitement distinct de celui des partenaires existants. Pas de chevauchement ambigu. [src: proposition] {CRITICAL}
- [ ] **L'onglet Projet montre-t-il l'articulation ?** Un slide ou un schema montrant qui fait quoi : SLASHR (Google Search + SEO local), Buddy (Meta), Push (SEO Belgique), etc. Le decideur doit comprendre en 10 secondes comment ca s'organise. [src: NBP onglet Projet] {HIGH}

---

## Priorites d'action (pour les recommandations)

Chaque recommandation du diagnostic porte un niveau de priorite :

| Priorite | Definition | Horizon |
|----------|-----------|---------|
| **CRITICAL** | Bloque la performance ou fausse le diagnostic. Fix immediat. | Phase 1, M1 |
| **HIGH** | Impact significatif sur le trafic/leads. | Phase 1, M1-M2 |
| **MEDIUM** | Opportunite d'optimisation. | Phase 1-2, M2-M3 |
| **LOW** | Amelioration marginale. Backlog. | Phase 2+ |

---

## Output attendu

Apres la checklist, l'IA ecrit dans le SDB :

```
CHECKLIST D'ANALYSE : {X}/{Y} questions repondues
Type de business : {type detecte}

STRUCTURE :
- Sitemap : {N} pages ({N} blog, {N} centres, {N} service, {N} autres)
- Indexation : {N}/{N} pages cles indexees
- Parcours conversion : {CTA type} verifie sur {N} pages

TRAFIC (perimetre {pays}) :
- Total : {N} clics/mois [src: GSC, {pays}]
- Split par type de page : blog {N}% | centres {N}% | homepage {N}%
- Split marque/hors-marque : {N}% / {N}%
- Tendance : {hausse/stable/baisse} ({delta}%)

PAID :
- Budget : {N} EUR/mois | Conversions : {N} | CPA : {N} EUR | CVR : {N}%
- Top search terms convertisseurs : {liste}
- Overlap paid/organic : {N} requetes communes

CONCURRENCE :
- Concurrents business : {liste}
- Local packs : {qui domine}

MANQUANTS : {liste avec impact + plan B}
```
