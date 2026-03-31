# SDB & INTERNAL-DIAG Templates

> Templates de reference pour les outputs Pass 1.
> Utilises par analyst-strategy pour produire le SDB et le diagnostic interne.

---

## SDB thin (obligatoire)

La Pass 1 produit un **SDB compact** (pas de dumps) :

- 8-12 bullets max (constats + opportunites + risques)
- Tables compactes : top N (N=10 ou 20 max)
- AUCUN body email complet sauf si absolument necessaire (sinon snippet)
- AUCUN CSV long : uniquement agregats + top lignes

---

## Evidence log (obligatoire)

Pour chaque chiffre cle, conserver :
- source (Pipedrive/Drive/DataForSEO)
- endpoint (ex: ranked_keywords)
- parametres (domain, date)
- timestamp
- fichier cache (.cache/...)

Ce log sert au debug et a la rejouabilite.

---

## Erreurs et fallbacks (obligatoire dans l'evidence log)

Pour chaque erreur API rencontree pendant la collecte :
- **Endpoint** : URL ou nom de l'endpoint
- **Status** : code HTTP ou message d'erreur
- **Impact** : quel bloc du SDB est affecte (ex: "COMPETITIVE_GAP incomplet")
- **Fallback** : action prise (ex: "utilise domain_rank_overview seul", "module ignore")

Format dans l'evidence log :
```
ERRORS & FALLBACKS:
- dataforseo/ranked_keywords (timeout 20s) → impact: SEARCH_STATE partiel → fallback: domain_rank_overview seul
- drive/files/abc123 (403 Forbidden) → impact: document_prospect manquant → fallback: collecte sans ce fichier
```

---

## Format de source dans le SDB (obligatoire)

Chaque affirmation quantitative dans le SDB DOIT porter une etiquette source inline au format :

`[src: {origine}, {endpoint}, {periode}, {date_collecte}]`

Origines valides : `pipedrive`, `drive`, `dataforseo`, `gsc`, `google-ads`, `calcul`, `benchmark`, `crawl`

Exemples :
- Trafic organique: 13 499 clics/mois `[src: gsc, performance_overview, 28j, 2026-03-27]`
- Budget Ads: 15 676 EUR/mois `[src: google-ads, campaigns, 2026-02-27 au 2026-03-27, collecte 2026-03-27]`
- ETV: 2 757 EUR `[src: dataforseo, domain_rank_overview, snapshot, 2026-03-27]`
- CVR implicite: 4.4% `[src: calcul, 792 conv / 18 063 clics, google-ads 30j]`

**REGLE PERIODE (CRITIQUE)** : ne pas fixer UNE periode unique. Utiliser la bonne periode pour le bon usage.

| Usage | Periode | Source | Pourquoi |
|-------|---------|--------|----------|
| **Diagnostic performance** | 90 jours | GSC 90j, Google Ads 90j | Lisse les anomalies, couvre un trimestre, representatif |
| **Tendance** | 12 mois ou daily trend 28j | GSC daily, Google Ads monthly | Detecte saisonnalite et trajectoire |
| **Budget mensuel actuel** | Dernier mois complet | Google Ads | Pour citer un budget reel, pas une moyenne |
| **Quick wins / positions** | 28 jours | GSC 28j | Positions recentes |
| **Benchmark concurrent** | Snapshot | DataForSEO | Pas de notion de periode, snapshot au jour J |

```
SNAPSHOT DONNEES:
- Date de collecte : {YYYY-MM-DD}
- GSC performance : 90 jours ({start} au {end})
- GSC tendance : 28 jours daily trend
- Google Ads diagnostic : 90 jours ({start} au {end})
- Google Ads budget mensuel : dernier mois complet ({mois})
- DataForSEO : snapshot au {date}
```

**REGLE : chaque chiffre du SDB porte sa periode.** "Budget mensuel : 15 676 EUR (mars 2026)" et "CPA moyen : 19.8 EUR (90 jours, jan-mars 2026)" sont deux chiffres avec des periodes differentes. Les deux sont corrects. L'important est que le HTML reprenne la meme periode que le SDB.

**Pourquoi** : si le SDB dit "15 676 EUR" (mars complet) et que la Pass 3 re-collecte et trouve "14 000 EUR" (27 jours de mars), les chiffres du HTML ne matchent plus le diagnostic.

**REGLE PASS 3** : la Pass 3 ne re-collecte JAMAIS les donnees. Elle utilise UNIQUEMENT les chiffres du SDB. Si un chiffre manque dans le SDB, elle remonte au SDB (pas aux APIs). Si le SDB est trop vieux (> 7 jours), relancer la Pass 1.

Les qualificatifs (ex: "maturite digitale faible") ne necessitent pas de source mais doivent pouvoir etre justifies par au moins un data point de l'evidence log.

**Regle :** si un chiffre apparait dans le SDB sans etiquette `[src:]`, il est rejete a la relecture. L'agent corrige avant de passer a Pass 2.

---

## INTERNAL-DIAG Template

**Ecriture obligatoire :** `.cache/deals/{deal_id}/artifacts/INTERNAL-DIAG.md` (utilise par Pass 2 et par `/debrief`).

```
=== DIAGNOSTIC STRATEGIQUE ===

CONTRAINTE PRINCIPALE : {en langage business, 2-3 phrases data-first}
→ Pourquoi c'est le verrou. Donnees sources.
→ Projection : {direction} {delta chiffre} {source} → {horizon}

LEVIERS PRIORITAIRES :
1. {levier} — {impact attendu, chiffre source}
   → Projection : {direction} {delta} → {horizon}
2. {levier} — {impact attendu, chiffre source}
   → Projection : {direction} {delta} → {horizon}

CE QU'ON NE FAIT PAS MAINTENANT :
- {axe} — {pourquoi pas maintenant, condition de reactivation}
- {axe} — {idem}

EXCEPTION SEA_SIGNAL (obligatoire si SEA_SIGNAL = EXPLICIT) :
Si `SEA_SIGNAL = EXPLICIT`, l'axe Amplification/Paid ne peut PAS etre differe hors perimetre. Reclassifier :
- Si opportunite paid significative + perimetre Croissance → levier prioritaire
- Si brief EXPLICIT mais fondations Search absentes → differe sequentiel ("cadrage SEA strategique M1, activation M3-M4 une fois les fondations Search posees")
- Justification obligatoire : "Le prospect demande un accompagnement paid. L'absence de structure paid renforce le besoin de cadrage strategique."

CONFIANCE : {High / Medium / Low}
→ {justification : quelles donnees manquent, quelles hypotheses}

TONE_PROFILE : {DIRECT / PEDAGOGIQUE / PROVOCATEUR / TECHNIQUE}
→ {justification basee sur le profil decideur et le contexte du deal}

ARC_CHOICE_RATIONALE :
- Arc retenu : {Classique | Urgence | Opportunite | Technique | Custom}
- Raison liee au decideur : {1 phrase — profil decideur + contexte}
- Raison liee aux donnees : {1 phrase — quel pattern dans le SDB oriente cet arc}
- Arc ecarte : {quel arc a ete considere et pourquoi rejete}

ROI DRIVERS (pont vers l'onglet ROI) :
- Driver 1 (Traffic) : {source} → {variable ROI impactee : visites cibles M12}
- Driver 2 (Conversion) : {source} → {variable ROI impactee : CVR / panier}
- Driver 3 (Mix marque/hors-marque) : {source} → {variable ROI impactee : part scalable}

PLAN 90 JOURS (contextuel, aligne sur la contrainte principale, 3 etapes max) :
CONTEXTE STRUCTURANT : {Refonte | AO | Saisonnalite | Standard}
1) M1 · {objectif adapte au contexte} → {livrable} → {signal attendu}
2) M2 · {objectif adapte au contexte} → {livrable} → {signal attendu}
3) M3 · {objectif adapte au contexte} → {livrable} → {signal attendu}

INSIGHT CENTRAL : {1 phrase non substituable}

TRAJECTOIRE 6 MOIS · Phase 2 "Run":
- M4-M6: {piliers actives, montee en puissance, intensite}
- Si SEA_SIGNAL = OPPORTUNITY : integrer activation paid en M4+
- Objectifs M6: {KPIs cibles sources}

ROI CONSERVATEUR (intervalle obligatoire) :
- Hypothese 1: {description} = {valeur_basse} - {valeur_haute} | Confidence: {High/Med/Low} | Validation: {comment valider} (source: {DataForSEO/GSC/transcript/benchmark})
- Hypothese 2: {description} = {valeur_basse} - {valeur_haute} | Confidence: {High/Med/Low} | Validation: {comment valider} (source: {source})
- Hypothese N: ...
- Chaine de calcul : H1 ({valeur}) x H2 ({valeur}) x ... = {resultat}
- ROI intervalle : x{N_bas} - x{N_haut} sur {periode}
- ROI affiche (conservateur) : x{N_bas} (borne basse de l'intervalle)
- Confidence globale ROI: {High/Medium/Low} (= min des confidences individuelles)
- Si Low sur 2+ hypotheses → ajouter dans le SDB: "Recommandation conditionnelle, validation en Phase 1"

> **Regle intervalle** : chaque hypothese a une borne basse (conservatrice) et une borne haute (optimiste realiste). Le ROI affiche au prospect = borne basse. L'intervalle complet est dans le simulateur ROI (onglet 3) pour que le prospect explore lui-meme.

Definitions de confiance ROI :
| Niveau | Critere | Exemple |
|--------|---------|---------|
| **High** | Donnee mesuree directement (prospect OU benchmark concret) | CA WooCommerce, panier moyen reel, positions DataForSEO |
| **Medium** | Donnee estimee via proxy fiable (DataForSEO ETV, benchmark secteur) | Trafic estime via ETV, CVR moyen secteur |
| **Low** | Hypothese sans mesure directe ni proxy fort | CVR post-refonte, impact contenu a 12 mois |

RESUME DECISIONNEL (6 bullets max):
1. {Douleur business chiffree : le probleme}
2. {Cout de l'inaction : ce que ca coute de ne rien faire}
3. {Levier principal : ce qu'on recommande}
4. {Quick wins 90 jours : resultats rapides attendus}
5. {ROI attendu : retour sur investissement}
6. {Investissement : fourchette prix}

EVIDENCE LOG:
- {affirmation 1} → source: {DataForSEO endpoint / GSC / transcript p.X / benchmark secteur}
- {affirmation 2} → source: {source}
- ...

=== FIN DIAGNOSTIC STRATEGIQUE ===
```

---

## SDB Template

**Ecriture obligatoire :** `.cache/deals/{deal_id}/artifacts/SDB.md`

```
GENERATED_AT: {ISO 8601 timestamp, ex: 2026-03-02T14:30:00}
=== STRUCTURED DATA BRIEF ===

PROSPECT: {nom} | {secteur} | {taille} | {maturite digitale}
DOMAINE_PRINCIPAL: {domaine} [src: {source de detection, ex: "drive, Prise de note R1 ligne 9"}]
DOMAINES_SECONDAIRES: {domaine1} ({role: migration cible / ancien / entite liee}), {domaine2} ({role}) | ou AUCUN
DECIDEUR: {prenom} {nom} | {role} | {preoccupation principale}
DECIDEUR_LEVEL: {DECIDEUR | INFLUENCEUR | OPERATIONNEL} [src: pipedrive, decideur_level]
DOULEUR: {1 phrase} | Verbatim: "{citation exacte}"
TRIGGER: {pourquoi maintenant}
TON: {formel/informel} | {reactif/lent} | {technique/business}
TONE_PROFILE: {DIRECT / PEDAGOGIQUE / PROVOCATEUR / TECHNIQUE} → {justification basee sur le profil decideur et le contexte du deal}
PERIMETRE_SLASHR: {SEO seul / SEO + GEO / Search global / etc.} [src: pipedrive, notes R1]
REFONTE: {OUI | NON} | {si OUI: timeline, ex: "go mars, MEL juin 2026"} | {CMS prevu si connu}
MODULES_ACTIFS: [{liste des modules actives, ex: 1-Pipedrive, 2-Drive, 3-SEO, 3b-GSC, 4-Benchmark, 4b-Intent, 4c-Niche, 5-GEO, 8-Technique, 9-Saisonnalite}]

SEA_SIGNAL: {EXPLICIT | DETECTED | ABSENT} [src: etape post-Module 6]
SEA_POSTURE: {PILOTE | CONSEIL | HORS_PERIMETRE}
SEA_BRIEF_REQUESTS: [{liste des demandes paid identifiees dans le brief, ex: "Google Ads Search", "Shopping", "3 scenarios budget", "estimation ROAS"}] (vide si ABSENT)

GSC_ACCESS: {YES | NO}

SEARCH STATE:
- Trafic organique: {X} visites/mois [src: dataforseo, domain_rank_overview]
- Keywords: {Y} total ({Z} marque / {W} hors-marque)
- ETV: {V} EUR
- Forces: {liste}
- Faiblesses: {liste}
- GSC (si Module 3b actif):
  - Clics: {X} /mois (90j) [src: gsc]
  - Impressions: {Y} /mois (90j) [src: gsc]
  - CTR moyen: {Z}% [src: gsc]
  - Position moyenne: {P} [src: gsc]
  - Split: {M}% marque / {HM}% hors-marque [src: gsc] (PRIORITAIRE sur DataForSEO)
  - Quick wins: {N} requetes (pos 5-20, impressions > 100, CTR < 5%) [src: gsc]
  - Top 10 queries hors-marque: [{requete, clics, impressions, CTR, position}] [src: gsc]

COMPETITIVE GAP:
- Concurrent #1: {nom} → {trafic} visites/mois (x{ratio} vs prospect)
- Concurrent #2: {nom} → {trafic} visites/mois
- Concurrent #3: {nom} → {trafic} visites/mois
- Keywords exclusifs concurrent #1: {top 5 avec volumes}
- Cout inaction: {visites perdues}/mois = {ETV} EUR/an

INTENT MARKET MAP:
- Commercial: {N} kw, {volume}/mois — Top: {kw1}, {kw2}, {kw3} [src: dataforseo, search_intent]
- Info captable: {N} kw, {volume}/mois — Top: {kw1}, {kw2}, {kw3} [src: dataforseo, search_intent]
  Strategie: {1 phrase — ex: contenu recette → CTA produit}
- Info non-captable: {volume}/mois (ecarte)
- TASM captable: {commercial + info captable}/mois [src: dataforseo, TASM Module 4c filtre par Module 4b]
- Part prospect actuelle: {trafic hors-marque} / {TASM captable} = {%} [src: calcul]
- Gap: {TASM captable - trafic hors-marque} recherches/mois non captees

OPPORTUNITIES:
- Quick wins: {liste avec impact estime}
- Territoires commerciaux: {clusters intent commercial non couverts}
- Territoires informationnels: {clusters info captable non couverts, avec strategie de monetisation}
- {GEO/IA si module 5 active}: {resultats}
- {SEA si module 6 active OU SEA_SIGNAL != ABSENT}:
  Si EXPLICIT: demandes brief (verbatim) + gap paid vs organic + CPC reference secteur + posture SLASHR (PILOTE/CONSEIL)
  Si DETECTED: activite paid actuelle (keywords payes, depense estimee) + synergie SEO/SEA potentielle
- {Social si module 7 active}: {resultats}
- {Technique si module 8 active}: {resultats}
- {Tendances si module 9 active}: {resultats}
- {Contenu si module 10 active}: {resultats}

DIAGNOSTIC STRATEGIQUE:
- Contrainte principale : {en langage business, 2-3 phrases data-first sur le verrou}
- Leviers prioritaires :
  - {levier A} : {impact chiffre attendu si active}
  - {levier B} : {impact chiffre attendu si active}
- Differe (sequentiel, avec condition d'activation) :
  - {axe} : sera active quand {condition}, horizon {X mois}
  - {axe} : {idem}
- Differe (hors perimetre) :
  - {axe} : hors perimetre car {raison}
  - {axe} : {idem}
- Projection contrainte principale (obligatoire) : {direction} {delta chiffre} {source} → {projection X mois}
- Projection leviers (obligatoire pour chaque) : {direction} {delta} → {horizon}
- Insight central: {1 phrase non substituable}
- Confiance globale diagnostic: {High/Medium/Low}
- TONE_PROFILE: {DIRECT / PEDAGOGIQUE / PROVOCATEUR / TECHNIQUE} → {justification}

STRATEGIE RECOMMANDEE:
- Perimetre: {SEO seul / Search global / ...}
- Scenario recommande: {Pilotage / Production / Acceleration} ({budget}/mois) — {justification}
- Phase 1 "Diagnostic & activation prioritaire" (90 jours):
  - M1 · Cadrage & audit: {livrables}
  - M2 · Quick wins & fondations: {actions}
  - M3 · Activation & premiers resultats: {KPIs}
- Phase 2 "Run" ({scenario}):
  - Intensite: {Pilotage = 1 priorite/mois | Production = 2 priorites/mois | Acceleration = 3+ priorites/mois}
  - Piliers actives: {lesquels, en lien avec les leviers prioritaires}
  - M4-M6: {trajectoire concrete}

ROI (intervalle) :
- Methode utilisee: {chaine de trafic / ETV proxy}
- Chaine de calcul : H1 x H2 x H3 = resultat (chaine visible dans le simulateur)
- Hypotheses (avec intervalle) :
  - H1: {description} = {basse} - {haute} | {High/Med/Low} [src: {source}]
  - H2: {description} = {basse} - {haute} | {High/Med/Low} [src: {source}]
  - ...
- ROI intervalle : x{N_bas} - x{N_haut} sur {periode}
- ROI affiche : x{N_bas} (borne basse conservatrice)
- Confidence globale: {High/Medium/Low}
- Si Low sur 2+ hypotheses: "Recommandation conditionnelle, validation en Phase 1"

CAS CLIENTS RETENUS:
- Cas {N}: {nom}
  match_criteria: {ce qui rend ce cas similaire: secteur, problematique, taille, profil decideur}
  key_metric: {le chiffre-cle qui convaincra, ex: "x3.8 trafic hors-marque en 12 mois"}
  sdb_juxtaposition: {quel bloc SDB mettre en regard, ex: "SEARCH_STATE 80% marque → cas 92% marque"}
  angle: {angle de presentation pour CE prospect, 1-2 phrases}
- Cas {N}: {nom}
  match_criteria: {idem}
  key_metric: {idem}
  sdb_juxtaposition: {idem}
  angle: {idem}

BRAND_CONTEXT:
  CONTEXTE_TAB: {YES | NO}
  Conditions remplies: {liste}
  Sources contexte: {fichiers Drive ou NONE}
  Piliers de marque: {liste ou NON IDENTIFIES}
  Personas: {B2C: liste, B2B: liste, ou NONE}

RED FLAGS: {liste}
GREEN FLAGS: {liste}

SERVICE_DESCRIPTIONS (contextualise depuis context/service_catalog.md):
- Audit SEO (ligne budget): "{description contextualisee 1-2 lignes}"
- Audit SEO (description proposition): "{description contextualisee 3-5 lignes}"
- {Si REFONTE = OUI} AMOA Technique SEO (ligne budget): "{description contextualisee}"
- {Si REFONTE = OUI} AMOA Technique SEO (description proposition): "{description contextualisee}"
- {Si contenus dans perimetre} Contenus SEO (ligne budget): "{description contextualisee}"
- {Si SEA_SIGNAL = EXPLICIT} Audit SEA (ligne budget): "{description contextualisee}"
- Accompagnement SEO run (ligne budget): "{description contextualisee}"
- {Si SEA_POSTURE != HORS_PERIMETRE} Accompagnement SEA run (ligne budget): "{description contextualisee}"
Variables utilisees: secteur={}, dimensions={}, nb_concurrents={}, contraintes={}, type_refonte={}, agence_tech={}

NARRATIVE_HINTS (suggestions pour Pass 2, non-contraignant):
- Hint 1: {bloc SDB A} + {bloc SDB B} → argument "{nom de l'argument}"
- Hint 2: {bloc SDB C} + {bloc SDB D} → argument "{nom}"
- Hint 3: {bloc SDB E} → argument "{nom}" (standalone)
- ... (3-5 hints max)

CLOSER_INPUT (rempli au Checkpoint 1 — vide avant validation closer):
  CLOSER_CONFIDENCE: {1-5} — confiance du closer sur le diagnostic
  CLOSER_ANGLE: "{ce que le prospect attend}" — oriente le hook et l'arc en Pass 2
  CLOSER_INSIGHTS: "{contexte hors-data}" — elements non mesurables (nouveau DG, deception agence, deadline cachee)
  CLOSER_RED_FLAGS: ["{flag1}", "{flag2}"] — risques non detectes par le systeme

=== FIN SDB ===
```

---

## Ecriture artefacts (obligatoire)

Ecrire :
- `.cache/deals/{deal_id}/artifacts/SDB.md`
- `.cache/deals/{deal_id}/evidence/evidence_log.md`
