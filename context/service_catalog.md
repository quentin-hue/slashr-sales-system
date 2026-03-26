# Service Catalog — v1.0

> Reference interne. Ce fichier definit les descriptions de prestations SLASHR, contextualisables par deal.
> Utilise par `/prepare` (onglet Investissement) et comme reference pour les budgets partenaires.

---

## Principe

Chaque prestation a 3 niveaux de description :

1. **Ligne budget** (1-2 lignes) — pour les tableaux Excel, budgets partenaires, devis
2. **Description proposition** (3-5 lignes) — pour l'onglet Investissement HTML
3. **Variables contextuelles** — ce qui change selon le deal (secteur, B2C/B2B, concurrents, contraintes)

L'agent contextualise chaque description en remplacant les variables par les donnees du deal (issues du SDB et du strategy_plan_internal).

---

## Prestations

### 1. Audit SEO

**Ligne budget :**
> Analyse semantique exhaustive du marche {secteur} ({dimensions}), integrant les concurrents valides ensemble. Clustering par intention de recherche et cible. Arborescence SEO avec mapping mots-cles par page. Roadmap priorisee par impact, exploitable par l'equipe technique.

**Description proposition :**
> La mission demarre par une cartographie complete de votre marche Search. On analyse l'ensemble des requetes pertinentes sur votre thematique — pas un echantillon, l'exhaustivite — en integrant {nb_concurrents} concurrents directs identifies ensemble. Chaque mot-cle est classe par intention (achat, information, navigation), par cible ({dimensions}) et par priorite. De cette analyse decoulent l'arborescence SEO (quelle page repond a quelle demande) et la strategie de contenu (quels contenus creer, dans quel ordre). Le livrable est concu pour etre directement exploitable : fichier structure filtrable, arborescence visuelle, et recommandations operationnelles.

**Livrables concrets :**
- Fichier de mots-cles structure (volume, difficulte, intention, cluster, cible, priorite)
- Arborescence SEO avec mapping mot-cle → page
- Benchmark concurrentiel ({concurrents_listes})
- Strategie de contenu priorisee par impact
- Recommandations techniques (si applicable)
- Roadmap court/moyen terme

**Variables contextuelles :**
- `{secteur}` : thematique du prospect (ex: "biscuitier", "e-commerce mode", "SaaS B2B")
- `{dimensions}` : axes de segmentation (ex: "B2C et B2B/CSE", "France et international", "marque et hors-marque")
- `{nb_concurrents}` : nombre de concurrents identifies (ex: "5-6", "3-4")
- `{concurrents_listes}` : noms si pertinent (ex: "La Trinitaine, Penven, Bonne Maman")
- `{contraintes_specifiques}` : contraintes sectorielles (ex: "distinction SEO/SEA sur les termes bretons", "multi-langues")

**Methodologie a communiquer (si le prospect demande des precisions) :**
> L'audit suit une sequence logique : analyse semantique exhaustive → clustering par intention et cible → arborescence → strategie de contenu → roadmap. Chaque etape nourrit la suivante. C'est pourquoi on ne s'engage pas sur un nombre fixe de mots-cles : l'objectif est la couverture complete du marche, pas un quota. Sur un marche comme {secteur}, avec {nb_concurrents} concurrents et les dimensions {dimensions}, l'analyse produit typiquement {fourchette_kw} mots-cles exploitables.

---

### 2. AMOA Technique SEO (refonte / migration)

**Ligne budget :**
> Cahier des charges SEO pour la refonte {type_refonte}, plan de redirections, recette SEO pre/post-bascule et assistance a la mise en production. Coordination avec l'equipe technique ({agence_tech}).

**Description proposition :**
> La refonte est une fenetre strategique : bien preparee, elle accelere les performances Search ; mal geree, elle detruit le capital existant. On intervient en amont pour definir le cahier des charges SEO (structure d'URLs, balisage, donnees structurees, performances), produire le plan de redirections complet, puis recetter l'implementation avant mise en ligne. L'objectif : zero regression SEO a la bascule, et des fondations techniques solides pour la croissance.

**Livrables concrets :**
- Cahier des charges SEO (specs techniques pour {agence_tech})
- Plan de redirections (mapping ancien → nouveau, regles de redirection)
- Recette SEO pre-production (checklist technique)
- Monitoring post-bascule (alertes indexation, crawl, positions)
- Coordination technique avec {agence_tech}

**Variables contextuelles :**
- `{type_refonte}` : nature de la refonte (ex: "migration WooCommerce → Shopify", "refonte complete", "migration de domaine")
- `{agence_tech}` : nom du partenaire technique (ex: "Fractory", "l'equipe dev interne")
- `{volumetrie}` : taille du site (ex: "~200 URLs", "1 500+ pages")

---

### 3. Contenus SEO strategiques

**Ligne budget :**
> Creation des contenus des pages strategiques ({types_pages}) sur la base de l'arborescence SEO et du zoning valide. Contenus optimises par intention de recherche, prets a integrer.

**Description proposition :**
> Les contenus sont produits a partir de l'analyse semantique : chaque page cible un cluster de mots-cles precis, avec une structure optimisee pour le positionnement et la conversion. On ne redige pas "du contenu SEO" generique — on cree des pages qui repondent a une intention de recherche identifiee, dans le ton de la marque, avec les informations que l'utilisateur attend a ce stade de son parcours.

**Livrables concrets :**
- {nb_contenus} contenus rediges, structures et optimises
- Brief par contenu (mot-cle cible, intention, structure, CTA)
- Contenus livres au format {format} (integrable directement)

**Variables contextuelles :**
- `{types_pages}` : types concernes (ex: "categories, page CSE, page B2B Pro", "fiches produits", "pages recettes")
- `{nb_contenus}` : volume (ex: "~10 pages strategiques", "~120 fiches produits")
- `{format}` : format de livraison (ex: "Google Docs sur la base du zoning", "directement dans le CMS")

---

### 4. Audit SEA / SMA

**Ligne budget :**
> Definition de la strategie d'acquisition Paid ({leviers_paid}), architecture des campagnes, structure de compte et ventilation budgetaire. Livrable exploitable par l'equipe d'execution ou l'agence media.

**Description proposition :**
> L'audit Paid part des memes fondations que l'audit SEO : la cartographie des intentions de recherche. On identifie les territoires ou le paid a le plus d'impact (intentions commerciales a fort volume, segments non captables en organique a court terme), on definit l'architecture de compte et la strategie d'encheres, et on produit un cahier des charges directement exploitable pour l'execution.

**Livrables concrets :**
- Architecture de compte ({leviers_paid})
- Strategie d'encheres et de ciblage
- Ventilation budgetaire par campagne/levier
- Cahier des charges pour l'execution (equipe interne ou agence media)

**Variables contextuelles :**
- `{leviers_paid}` : leviers concernes (ex: "Google Ads Search + Shopping", "Google Ads + Meta Ads", "SEA uniquement")
- `{posture_slashr}` : PILOTE (SLASHR pilote) ou CONSEIL (SLASHR recommande, un tiers execute)

---

### 5. Accompagnement SEO (run mensuel)

**Ligne budget :**
> Monitoring des performances Search post-{evenement}, suivi de la roadmap SEO, production de contenus ({type_production}) et optimisations continues. Reporting mensuel.

**Description proposition :**
> L'accompagnement mensuel assure la continuite apres l'audit : suivi des positions et du trafic, ajustements strategiques en fonction des resultats, production de contenus selon la roadmap definie, et optimisations techniques continues. Chaque mois, un reporting clair mesure la progression vers les objectifs fixes.

**Livrables concrets (par mois) :**
- Suivi des positions et du trafic organique
- Production de contenus selon roadmap ({cadence_contenu})
- Optimisations techniques et on-page
- Reporting mensuel (positions, trafic, conversions, actions)
- Recommandations d'ajustement

**Variables contextuelles :**
- `{evenement}` : contexte (ex: "refonte", "lancement", "audit initial")
- `{type_production}` : nature des contenus (ex: "fiches produits, categories, recettes", "articles blog, landing pages")
- `{cadence_contenu}` : rythme (ex: "2-4 contenus/mois", "optimisations existantes + 1-2 nouveaux contenus")

---

### 6. Accompagnement SEA / SMA (run mensuel)

**Ligne budget :**
> Pilotage strategique des campagnes {leviers_paid}, optimisations continues, ajustements saisonniers et reporting performance. Coordination avec {executant_ads}.

**Description proposition :**
> Le pilotage mensuel couvre la strategie et l'optimisation des campagnes Paid : ajustement des encheres et du ciblage, adaptation aux saisonnalites, tests A/B, et reporting ROI. SLASHR definit la strategie et les optimisations ; l'execution quotidienne (bid management, creation d'annonces) est assuree par {executant_ads}.

**Livrables concrets (par mois) :**
- Revue strategique des campagnes
- Recommandations d'optimisation (encheres, ciblage, budgets)
- Ajustements saisonniers
- Reporting performance (ROAS, CPA, volumes, evolution)

**Variables contextuelles :**
- `{leviers_paid}` : leviers actifs (ex: "Google Ads Search + Shopping + Meta Ads")
- `{executant_ads}` : qui execute au quotidien (ex: "l'equipe interne", "l'agence media partenaire", "Cocoa")

---

## Regles de contextualisation

### Pour le `/prepare` (onglet Investissement)

1. La Pass 1 identifie les variables contextuelles dans le SDB (secteur, dimensions, concurrents, refonte, leviers)
2. La Pass 2 utilise les **descriptions proposition** contextualisees pour l'onglet Investissement — integrees dans les blocs Phase 1 et Phase 2
3. Les descriptions ne remplacent pas la structure existante (Pont S7, pricing cards, etc.) — elles enrichissent le **scope qualitatif** de chaque phase

### Pour les budgets partenaires (Excel, devis)

1. Utiliser les **lignes budget** contextualisees
2. Adapter le niveau de detail au format (1-2 lignes pour un tableau Excel, 3-4 lignes pour un devis detaille)
3. Toujours inclure : la methodologie sequentielle, les livrables concrets, les variables specifiques au deal

### Regles generales

- **Ne jamais s'engager sur un nombre fixe** de mots-cles, contenus ou concurrents sans avoir fait l'analyse prealable. Donner une fourchette si necessaire.
- **Toujours montrer la sequence logique** : analyse → clustering → arborescence → contenu → roadmap. Chaque etape decoule de la precedente.
- **Toujours distinguer les dimensions** du deal (B2C/B2B, FR/international, marque/hors-marque) dans les descriptions.
- **Les jours et le TJM restent INTERNES** — cf. `output_contract.md`. Les descriptions client parlent de scope et de livrables, jamais de jours.
