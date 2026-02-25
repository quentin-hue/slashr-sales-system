# S7 Search Operating Model — v2.0

> Reference interne. Ce document clarifie l'articulation entre le **diagnostic S7** et les **7 piliers d'activation** SLASHR.

---

## 1. Deux couches, un modele

| Couche | Role | Question cle | Quand |
|--------|------|--------------|-------|
| **S7 — Diagnostic & Arbitrage** | Evaluer, prioriser, decider | "Ou concentrer les ressources pour debloquer le plus de valeur ?" | R1 Done → avant la proposition |
| **7 Piliers — Activation & Execution** | Executer, mesurer, iterer | "Comment activer concretement les leviers priorises ?" | Phase 1 (Audit) + Phase 2 (Run) |

**Le S7 dit QUOI prioriser. Les piliers disent COMMENT executer.**

**Phrase C-level (pour R2) :**
> "On analyse votre situation Search sur 7 forces. Ca nous donne une lecture objective de vos atouts et de vos contraintes. Ensuite on arbitre : on ne travaille pas les 7 — on concentre les ressources sur les 2-3 leviers qui debloquent le plus de valeur pour vous."

---

## 2. S7 — Grille de diagnostic

Le S7 est un outil d'arbitrage strategique. Il repond a la question : **que prioriser ?**

### Les 7 forces

| # | Force | Ce qu'elle mesure | Sources typiques |
|---|-------|-------------------|------------------|
| S1 | Intentions de recherche | Alignement offre/demande search par type d'intent : couverture des requetes commerciales (achat, comparaison) ET des requetes informationnelles captables (recettes, guides, comparatifs ou la marque a une legitimite). Volume, tendance, couverture par bucket intent | keyword_overview, keywords_for_site, search_intent, google_trends_explore, Intent Market Map (Module 4b) |
| S2 | Architecture & technique | Sante technique du site, performance, structure de donnees, crawlabilite | domain_rank_overview, on_page_lighthouse, on_page_instant_pages |
| S3 | Creation de contenu | Ratio keywords couverts vs univers semantique, qualite et profondeur du contenu | ranked_keywords, keywords_for_site, keyword_ideas |
| S4 | UX & Conversion | Experience utilisateur, taux de conversion estime, parcours de monetisation | on_page_lighthouse (performance), transcript, brief |
| S5 | Autorite, signaux de confiance | DA, profil backlinks, notoriete marque, part marque/hors-marque | domain_rank_overview, ranked_keywords (filtre marque) |
| S6 | Diffusion multicanale | Presence YouTube, IA/GEO, Social Search, coherence cross-canal | serp_youtube_organic, serp_organic_live_advanced |
| S7 | Amplification | Complementarite Paid/SEA, budget pub, exploitation des temps forts | ranked_keywords (paid), keyword_overview (CPC) |

### Echelle de scoring

| Score | Signification |
|-------|---------------|
| 0 | Inexistant — rien n'est en place |
| 1 | Critique — des problemes majeurs bloquent la performance |
| 2 | Faible — les fondations existent mais sont insuffisantes |
| 3 | Correct — fonctionnel, mais pas optimise ni competitif |
| 4 | Bon — au niveau du marche, quelques optimisations possibles |
| 5 | Excellent — avantage competitif sur cette dimension |

### Anchors quantitatifs (reperes indicatifs par force)

Les seuils ci-dessous sont des **reperes** pour reduire la variance entre runs. Ils ne remplacent pas le jugement contextuel (un 3 en SaaS B2B ≠ un 3 en e-commerce alimentaire), mais fournissent un point de depart objectif.

| Force | Score 0-1 | Score 2 | Score 3 | Score 4-5 | Metrique cle |
|-------|-----------|---------|---------|-----------|-------------|
| S1 · Intentions | Couverture < 5% du TASM captable | 5-15% du TASM | 15-35% du TASM | > 35% du TASM | Part de marche search captee (hors-marque) |
| S2 · Architecture | Lighthouse SEO < 50 OU > 20% pages non indexees | Lighthouse 50-79 OU 10-20% non indexees | Lighthouse 80-89, < 10% erreurs, CWV mixtes | Lighthouse 90+, CWV verts, 0 erreur critique | Score Lighthouse SEO + taux crawl |
| S3 · Contenu | < 5% keywords couverts vs univers pertinent | 5-15% couverts, pas de contenu editorial | 15-30% couverts, quelques contenus editoriaux | > 30% couverts, strategie editoriale active | Ratio pages indexees / univers semantique |
| S4 · UX/CVR | CVR < 0.3% OU parcours casse | CVR 0.3-0.7%, friction identifiee | CVR 0.7-1.5%, parcours fonctionnel | CVR > 1.5%, automation active (abandon panier, CRM) | Taux de conversion e-commerce |
| S5 · Autorite | Domain Rank < 20, 0 backlinks strategy | DR 20-35, quelques backlinks, pas de strategie | DR 35-50, profil backlinks organique | DR 50+, strategie active, mentions RP | Domain Rank + tendance backlinks |
| S6 · Diffusion | 0 presence hors site web | 1 canal non-structure (ex: page FB inactive) | 2+ canaux avec contenu irregulier | Strategie multi-canal active (YouTube, GEO, Social) | Nombre de canaux actifs + regularite |
| S7 · Amplification | 0 investissement paid | Budget paid < 500 EUR/mois OU ROI negatif | Budget paid actif, pas de synergie SEO/SEA | Strategie paid integree, synergie SEO/SEA mesuree | Budget paid + synergie organique |

> **Usage :** l'agent commence par les anchors, puis ajuste ±1 point selon le contexte sectoriel et concurrentiel. Un ecart de +2 par rapport a l'anchor doit etre justifie explicitement dans l'evidence log.

### Regles de scoring

- Chaque force : **score 0 a 5**
- Chaque score justifie par **au moins 1 data point source**
- Toujours relatif au secteur du prospect (un 3 en SaaS B2B ≠ un 3 en e-commerce alimentaire)
- Apres chaque score : **SO WHAT** (1-2 phrases) — traduction business, pas technique
- Le score global n'existe pas. Pas de moyenne.
- **Regle de tiebreak :** quand 2 forces sont a ≤ 1 point d'ecart pour la classification PRIMARY/SECONDARY, la **Confidence** departage. A score egal, la force avec Confidence High l'emporte sur Medium, qui l'emporte sur Low. Raison : prioriser la ou le diagnostic est le plus sur.

### SO WHAT — regles

Chaque SO WHAT doit repondre a : "Et alors, concretement, pour CE prospect ?"

**Interdit :**
- "A ameliorer" / "Peut mieux faire" / "Necessite une attention particuliere"
- "Performance sous-optimale" / "Potentiel inexploite"
- Toute phrase qui fonctionne pour n'importe quel prospect (test de substitution)

**Obligatoire :**
- Chiffrer l'impact quand possible (volume, CA, part de marche)
- Nommer le prospect ou son secteur specifique
- Lier a une consequence business concrete

**Exemples :**
- ❌ "Le contenu est insuffisant et necessite une strategie editoriale"
- ✅ "Avec 23 pages indexees sur un univers de 850 requetes pertinentes, {Prospect} ne couvre que 3% du potentiel search de son secteur — ses 3 concurrents directs en couvrent 15 a 40%"

**Exemple S1 enrichi (segmentation intent) :**
- ❌ "Le marche represente 75 000 recherches/mois" (volume brut, sans nuance d'intent)
- ✅ "Le marche biscuitier genere 12 000 recherches d'achat/mois et 63 000 recherches recette/mois. La Mere Poulard ne capte ni les unes ni les autres. Les requetes recette sont un territoire d'acquisition : 22 200 personnes/mois cherchent 'palet breton' — le fabricant historique devrait etre la reference, pas un blog cuisine."

---

## 3. Regles de classification

| Classification | Combien | Definition | Obligation |
|---------------|---------|------------|------------|
| **PRIMARY** | Exactement 1 | La contrainte principale — celle qui bloque le plus de valeur. Tant qu'elle n'est pas traitee, les autres leviers ont un impact limite | Justification en 2-3 phrases data-first |
| **SECONDARY** | 1 a 2 | Leviers a fort potentiel, actionnables en parallele ou juste apres le PRIMARY | 1 phrase : pourquoi ce levier amplifie |
| **DEFERRED-SEQUENTIAL** | Variable | Forces qui seront activees quand le PRIMARY/SECONDARY sera traite. Dependance logique identifiee | 1 phrase : "sera active quand {condition}" |
| **DEFERRED-SCOPE** | Variable | Forces hors perimetre ou non pertinentes actuellement. Pas de dependance, choix de focus | 1 phrase : "hors perimetre car {raison}" |

> **Distinction DEFERRED :** SEQUENTIAL = le levier a du potentiel mais depend d'un autre (ex: "S5 Autorite sera activee quand S3 Contenu fournira du contenu linkable"). SCOPE = le levier n'est pas prevu dans la mission (ex: "S7 Amplification hors perimetre SLASHR, gere par l'equipe media interne"). Le prospect comprend la difference entre "pas maintenant" et "pas nous".

**Regle absolue :** ne jamais recommander de travailler les 7 forces simultanement. Maximum 3 leviers actifs (1 PRIMARY + 2 SECONDARY). Meme si le prospect le demande.

### Logique d'interdependance

La contrainte principale est la force dont la faiblesse **empeche les autres de produire des resultats** :

| Si la contrainte est... | Alors investir dans... est inutile tant que... |
|------------------------|------------------------------------------------|
| S2 (Architecture) | S3 (Contenu) — le contenu n'a pas de structure pour ranker |
| S2 (Architecture) | S1 (Intentions) — meme si on comprend la demande, le site ne peut pas y repondre |
| S3 (Contenu) | S5 (Autorite) — il n'y a rien a linker |
| S5 (Autorite) | S3 (Contenu) sur les requetes competitives — pas assez de credibilite pour ranker |
| S4 (UX) | S1 (Intentions) — le trafic arrive mais ne convertit pas |

### Synthese obligatoire (post-grille)

Apres le scoring des 7 forces, produire **systematiquement** ce bloc :

```
CONTRAINTE PRINCIPALE : {force} (score {X}/5)
→ {1 phrase : pourquoi c'est le verrou — data-first}

LEVIERS PRIORITAIRES : {force A} + {force B}
→ {1 phrase : quel impact attendu si on les active}

PROJECTION PRIMARY (obligatoire) : {direction} {delta chiffre} {source} → {projection X mois}
PROJECTION SECONDARY (obligatoire pour chaque) : {direction} {delta} → {horizon}

INSIGHT CENTRAL : {1 phrase memorable, non substituable}
```

**Projection 6-12M (obligatoire pour PRIMARY + SECONDARY) :**
- Format strict : `{direction} {delta chiffre} en {horizon}` avec source identifiee
- Sources preferees : keyword_dynamics (solde new vs lost), historical_rank_overview, tendances concurrents
- Si aucune donnee de tendance : "Projection non disponible (pas de donnees historiques)" + ajouter dans MANQUANTS du SDB
- Anti-dramatisation : la projection est factuelle, pas speculative. "Erosion: -31 kw nets/mois" est acceptable. "Catastrophe imminente" ne l'est pas.

**Test de l'insight :** si on peut remplacer le nom du prospect par n'importe quel autre et que la phrase fonctionne encore → recrire. L'insight doit etre specifique a CE prospect, CE marche, CES donnees.

---

## 4. 7 Piliers — Grille d'activation

Les 7 piliers sont le **mode operatoire** SLASHR. Ils repondent a la question : **comment executer ?**

| # | Pilier | Actions typiques |
|---|--------|-----------------|
| P1 | Intentions de recherche | Cartographie semantique, clusters thematiques, analyse des SERPs, mapping intent |
| P2 | Architecture & technique | Audit crawl, Core Web Vitals, structure Hn, donnees structurees, maillage interne |
| P3 | Creation de contenu | Production editoriale, optimisation pages existantes, content gap analysis |
| P4 | UX & Conversion | Parcours utilisateur, CRO, landing pages, signaux d'engagement |
| P5 | Autorite, signaux de confiance | Link building strategique, RP digitales, mentions marque, E-E-A-T |
| P6 | Diffusion multicanale | YouTube SEO, GEO/IA (ChatGPT, Perplexity), Social Search (TikTok, Instagram) |
| P7 | Amplification | SEA complementaire, remarketing, temps forts saisonniers, synergie paid/organic |

### Lien S7 → Piliers

Le diagnostic S7 determine **quels piliers activer en priorite**. Chaque force S7 mappe directement sur le pilier du meme numero.

```
S7 Force (diagnostic)  →  Pilier (activation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S1 Intentions           →  P1 Intentions (cartographie)
S2 Architecture         →  P2 Architecture (audit + fix)
S3 Contenu              →  P3 Contenu (production)
S4 UX & Conversion      →  P4 UX (optimisation)
S5 Autorite             →  P5 Autorite (link building)
S6 Diffusion            →  P6 Diffusion (multicanal)
S7 Amplification        →  P7 Amplification (paid)
```

**Exemple concret :**
- S7 diagnostic → S2 Architecture = PRIMARY (score 1/5, Lighthouse 32, crawl errors 40%)
- Activation → Pilier P2 en priorite Phase 1 : audit technique, fix CWV, restructuration Hn, donnees structurees
- Resultat attendu : debloquer le potentiel des autres piliers (un bon contenu ne performe pas sur un site lent)

---

## 5. Articulation dans la proposition HTML

### Onglet Strategie (prospect-facing)

Section "Lecture strategique" :
- Visualisation radar 7 forces (scores)
- 1 contrainte principale mise en evidence (PRIMARY) — badge rouge
- 1-2 leviers secondaires (SECONDARY) — badge bleu
- Forces DEFERRED visibles sur le radar mais sans detail (grisees)
- Insight central (1 phrase)

### Onglet Livrables & Methode (prospect-facing)

Sous-section "Notre approche — S7" :
- Definition en 2-3 phrases (diagnostic + arbitrage)
- Liste des 7 forces (1 ligne chacune)
- Regle d'arbitrage ("on ne travaille pas les 7, on priorise")

### Document interne (INTERNAL-S7-*.md)

Le diagnostic complet avec :
- Scores detailles + SO WHAT par force
- Classification PRIMARY/SECONDARY/DEFERRED avec justifications
- Evidence log (sources utilisees)
- Trajectoires 90 jours + 6 mois
- ROI conservateur avec hypotheses explicites

---

## 6. Anti-patterns

| Anti-pattern | Pourquoi c'est un probleme | Correction |
|-------------|---------------------------|------------|
| Recommander les 7 forces | Dilue l'impact, impossible a executer, perd en credibilite | Max 3 leviers actifs |
| 2+ PRIMARY | Pas de priorisation = pas de decision | Exactement 1 PRIMARY |
| SO WHAT generique ("a ameliorer") | N'apporte aucune info au decideur | Traduire en impact CA/trafic/conversion specifique |
| Insight substituable | Montre qu'on n'a pas compris le prospect | Tester : remplacer le nom → si ca marche encore, recrire |
| Confondre diagnostic et activation | Le S7 dit QUOI prioriser, pas COMMENT faire | S7 = arbitrage, Piliers = execution |
| DEFERRED sans justification | Le prospect ne comprend pas pourquoi on ignore une force | Chaque DEFERRED-SEQUENTIAL a un "sera active quand...", chaque DEFERRED-SCOPE a un "hors perimetre car..." |
| DEFERRED sans distinction SEQ/SCOPE | Le prospect ne sait pas si c'est un report ou une exclusion | Toujours typer : SEQUENTIAL (viendra apres) vs SCOPE (pas prevu) |
| Score global / moyenne | Masque la contrainte principale | Pas de moyenne. La contrainte peut etre un 1 meme si le reste est a 4 |
| Dramatiser les scores bas | Zero dramatisation — les donnees suffisent | "Score 1/5" + SO WHAT factuel, pas "situation catastrophique" |
