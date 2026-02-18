# Mode DECK — Preparation R2 (v8.0)

> **Prerequis :** `agents/shared.md` lu. Input : DEAL-*.md lu depuis Drive.

---

## Input

- Le fichier DEAL-*.md, lu depuis Google Drive
- Les donnees DataForSEO re-fetchees (domain_rank_overview + ranked_keywords top 20 + competitors_domain top 10)

## Processus de generation — 7 etapes

---

### Etape 1 — Validation du brief

Checklist de coherence interne sur le DEAL-*.md :
- Score coherent avec les indicateurs Section 3
- Budget correctement qualifie (budget global =/= budget dedie SLASHR)
- Micro-engagement traite
- Verbatims exploitables
- Risque d'inaction en impact business concret
- Fiabilite coherente avec les sources
- Question killer R2 presente dans Section 6 (si absente -> en generer une a partir du point de tension + red flags)

**Si incoherence detectee** -> inserer un bloc ALERTE en tete du DECK avec les corrections.

**Adaptation selon fiabilite :**

| Fiabilite | Impact sur le DECK |
|-----------|-------------------|
| HAUTE | DECK standard |
| MOYENNE | Ajouter : "completer qualification — questions a poser en debut de R2 : {liste}" |
| BASSE | Alerte closer : "Brief base sur sources incompletes. Completer qualification AVANT R2. Questions a poser : {liste}" |

---

### Etape 2 — Audit Search complet

Pour chaque domaine analyse, presenter les metriques dans cet **ordre obligatoire** :

**1. Trafic organique estime** (visites/mois)
La metrique principale. Nombre de visiteurs uniques estimes provenant de la recherche organique.

**2. Mots-cles positionnes** (total + ventilation)
- Total de mots-cles sur lesquels le domaine apparait dans les resultats
- Ventilation : top 3 / top 10 / top 20 / top 50

**3. Positions cles** (top 20 par trafic estime)
- Tableau des 20 mots-cles generant le plus de trafic
- Colonnes : mot-cle, position, volume de recherche mensuel, type (marque / generique)
- Separer clairement les requetes de marque des requetes generiques

**4. Part de voix vs concurrents**
- Tableau comparatif : domaine prospect vs top 3-5 concurrents Search
- Colonnes : domaine, trafic organique estime, nombre de mots-cles, ratio vs prospect
- Identifier qui capte le trafic que le prospect ne capte pas

**5. Valeur du trafic organique (ETV)**
- **Toujours en dernier.** Toujours avec l'explication suivante :
> "L'ETV (Estimated Traffic Value) represente ce que couterait ce trafic organique s'il devait etre achete via Google Ads. Pour {domaine}, cela represente {X}EUR/mois — autrement dit, {domaine} economise {X}EUR/mois en acquisition grace a son referencement naturel."
- Contexte comparatif : ETV prospect vs ETV concurrents

---

### Etape 3 — 10 Slides R2

Pour chaque slide (10 au total), produire :

| Champ | Format |
|-------|--------|
| **Titre** | Max 8 mots. Accrocheur, pas descriptif |
| **Sous-titre** | 1 ligne de contexte |
| **Bullets** | 3-4 points max, 15 mots chacun max |
| **Notes speaker** | 2-3 phrases : ce que le closer DOIT dire. Ton conversationnel |

**Structure des 10 slides :**

| # | Slide | Source | Objectif |
|---|-------|--------|----------|
| 1 | Contexte prospect | DEAL Section 1 + Section 2 | Montrer qu'on a ecoute |
| 2 | Diagnostic data | DECK Part 1 Audit Search | Objectiver avec de la data |
| 3 | Cout de l'inaction | DEAL Section 2 (risque d'inaction) | Creer l'urgence rationnelle |
| 4 | Vision cible | DEAL Section 6 (angle R2) + DECK Part 3 ROI | Ouvrir le champ des possibles |
| 5 | Recommandation strategique | DEAL Section 6 + positioning.md | 3 piliers du plan SLASHR |
| 6 | Quick wins 90 jours | DECK Part 1 (positions cles) + Part 3 ROI | 3 actions immediates + resultats attendus |
| 7 | Equipe et methode | `positioning.md` + contexte deal | Rassurer sur l'execution |

**Slide 7 — elements concrets attendus :**
- Taille equipe dediee au prospect (meme approximative)
- Frequence des livrables / points de contact (hebdo, mensuel)
- Outils et process (reporting, dashboards, communication)
- Methodologie par phase (M1-3 / M3-6 / M6-12) — reference `context/positioning.md`
- Si pertinent : reference client ou cas similaire (sans NDA)
| 8 | Investissement | DEAL Section 3 (budget) + positioning.md (scenarios) | 2-3 scenarios adaptes au prospect |
| 9 | ROI projete | DECK Part 3 ROI | Justifier le prix par le retour |
| 10 | Decision | Script de fin R2 | Slide vide — script de closing en notes speaker |

**Adaptation par profil decideur :**

| Profil | Slides a appuyer | Slides a survoler |
|--------|-----------------|-------------------|
| C-level | S3 (cout inaction), S9 (ROI), S10 (decision) | S2 (diagnostic technique), S7 (methode) |
| Influenceur | S6 (quick wins), S7 (methode), S2 (diagnostic) | S8 (pricing — pas son budget), S10 (decision — pas son call) |
| Operationnel | S6 (quick wins), S7 (methode), S2 (diagnostic) | S3 (cout inaction — pas son levier), S9 (ROI global) |

Le closer adapte le temps passe par slide, pas l'ordre. La structure reste 1-10.

**Regles du deck :**
1. Chaque slide a UN message — pas de slide fourre-tout
2. Les bullets sont des affirmations, pas des descriptions — "Vos concurrents captent x4 plus de trafic sur les memes requetes" vs "Analyse du trafic organique"
3. La data precede toujours l'opinion — chiffre d'abord, recommandation ensuite
4. Slide 10 = le script de fin R2 complet dans les notes speaker (6 temps : recap, question killer, temperature, gap, CTA, silence)
5. Le pricing propose 2-3 scenarios adaptes au prospect (ex : Essentiel / Performance / Croissance), avec perimetre et frequence clairs. Le closer ajuste les montants
6. Ton des notes speaker : conversationnel, partenaire strategique — c'est ce que le closer dit a voix haute, pas ce qu'il lit. Jamais arrogant, jamais suppliant
7. 1-2 slides "vision marche" max (Search IA, zero-click) — le prospect veut du concret, pas 5 slides educatives
8. Les recommandations sont structurees par phase temporelle (M1-3 fondations, M3-6 acceleration, M6-12 autorite) avec indicateurs impact/effort quand pertinent
9. **Design system obligatoire** — les slides suivent `context/design_system.md` : fond `#1a1a1a`, titres blancs, accent orange `#E74601` pour les KPIs, accent magenta `#CE08A9` pour les highlights, tableaux fond `#2C2E34` bordures `white/10`, 3-4 bullets max par slide, gradient brand sur slide de couverture et de cloture. Le closer applique ces directives dans Google Slides

---

### Etape 4 — Objections probables (max 6)

**Regle de sourcing :** chaque red flag du DEAL Section 5 doit generer au moins une objection. Les objections sans lien avec un signal du brief (red flag, verbatim, indicateur Section 3) sont suspectes — les supprimer ou les justifier.

Pour chaque objection, format **liste** (pas de tableau multi-colonnes) :

```
### Objection 1 — "{formulation probable du prospect}"
- **Probabilite :** Haute / Moyenne / Basse
- **Source :** {indice repere dans le brief}
- **Reponse :** {script en 3 phrases max. Direct, factuel, pas defensif}
- **Pivot :** {question de relance post-reponse vers le closing}
```

---

### Etape 5 — Script de fin R2 (5 temps)

1. **Recap valeur** (30 sec) — resumer les 2-3 points de douleur + la solution SLASHR
2. **Question killer** — poser la question killer R2 du DEAL Section 6. C'est la question de deblocage AVANT la temperature. Elle force le prospect a verbaliser son frein principal
3. **Question de temperature** — "Sur une echelle de 1 a 10..."
4. **Traitement du gap** — selon la note : 8-10 / 5-7 / < 5
5. **Call to action** — lettre d'engagement + call de finalisation
6. **Silence** — se taire. Le premier qui parle perd.

Adapter le script au profil decideur :
- C-level : ROI, vision strategique, impact pipeline
- Influenceur : credibilite interne, quick wins pour prouver le choix
- Operationnel : facilite d'execution, support, onboarding

---

### Etape 6 — ROI projete

**Methode primaire : chaine de trafic**

```
1. Trafic organique actuel = X visites/mois (source : DataForSEO domain_rank_overview)
2. Separation marque / hors-marque :
   - Trafic de marque = Y visites/mois (requetes contenant le nom de l'entreprise)
   - Trafic hors-marque = Z visites/mois (X - Y)
3. Potentiel demontre :
   - Concurrent {nom} capte C visites/mois sur les memes requetes generiques
   - Gap = C - Z = potentiel recuperable
   - Multiplicateur justifie = C / Z (arrondi, base sur le gap concurrentiel reel)
4. Gain trafic projete = nouveau hors-marque estime - hors-marque actuel
5. Valorisation du gain :
   A. Si taux de conversion connu : gain x taux conversion x panier moyen = CA additionnel
   B. Si taux de conversion inconnu : utiliser l'ETV du gain comme proxy conservateur
      -> "Chaque visite organique supplementaire vaut en moyenne {ETV/visite}EUR en equivalent
         publicitaire. {gain} visites x {ETV/visite}EUR = {total}EUR/mois d'economie d'acquisition."
6. ROI = gain annuel / investissement SLASHR
   -> L'investissement est le montant du devis SLASHR. Si inconnu -> noter "ROI calculable
      une fois le budget defini" et fournir la formule avec un placeholder {investissement}.
```

**Methode secondaire : validation par ETV**

Comparer l'ETV actuelle vs l'ETV du concurrent pour confirmer l'ordre de grandeur du gain projete. Cette methode ne remplace pas la chaine de trafic — elle la valide.

**Methode alternative : CTR marche (quand acces Search Console)**

Si le closer a acces a la Search Console du prospect :
1. Selectionner les mots-cles prioritaires (positions 8-20, plus gros volumes)
2. Appliquer un gain de positions realiste (+5 positions par mot-cle)
3. Utiliser les CTR **reels** observes dans la Search Console du client
4. Calculer le trafic additionnel et la conversion avec le taux de conversion reel du site

**Sans acces Search Console** (cas standard en R2) :
- Utiliser les CTR moyens du marche (courbes Sistrix/AWR/FirstPageSage) en precisant explicitement qu'il s'agit de CTR estimes
- Appliquer aux mots-cles prioritaires avec un gain de positions conservateur
- Mentionner : "Projection basee sur des CTR moyens du marche. Les CTR reels seront valides avec les donnees Search Console en phase audit."

**Section obligatoire : "Ce que ca veut dire concretement"**

Rediger 2-3 phrases en francais courant, sans jargon, resumant ce que le gain represente pour le prospect en termes business.

**Tableau des hypotheses**

| Hypothese | Valeur | Source |
|-----------|--------|--------|
| Trafic organique actuel | X visites/mois | DataForSEO domain_rank_overview, {date} |
| Dont trafic de marque | Y visites/mois | Estimation basee sur ranked_keywords |
| Trafic hors-marque actuel | Z visites/mois | X - Y |
| Benchmark concurrent | C visites/mois | DataForSEO competitors_domain, {concurrent} |
| Multiplicateur applique | xM | Ratio concurrent/prospect sur requetes generiques |
| Taux de conversion | T% | {source : prospect / estimation secteur / inconnu} |
| Panier moyen | P EUR | {source : prospect / estimation secteur / inconnu} |
| Investissement SLASHR | I EUR/an | {source : devis / placeholder} |

**Regles ROI :**
- Jamais de multiplicateur sorti du chapeau. Chaque multiplicateur est justifie par un gap concurrentiel reel
- Le trafic de marque n'est PAS multiplie — SLASHR ne cree pas de notoriete, il capte du trafic generique
- Si l'investissement n'est pas connu, ne pas l'inventer. Fournir la formule
- Toujours le scenario conservateur (arrondir en defaveur)
- CTR : utiliser les CTR **reels** (Search Console) quand disponibles. Sinon, CTR moyens marche en precisant "estimes"
- Taux de conversion : utiliser le taux reel du prospect si connu. Sinon, estimer par secteur en le precisant

---

### Etape 7 — Pre-R2 Checklist

Le closer DOIT valider avant d'entrer en R2 :

- [ ] DEAL-*.md lu integralement
- [ ] DECK-*.md lu integralement
- [ ] Deck 10 slides pret dans Google Slides avec data personnalisee
- [ ] Data Search verifiee et a jour
- [ ] Top 3 objections repetees a voix haute avec reponses
- [ ] Script de fin visible pendant le call
- [ ] ROI projete verifie et justifiable (chaque hypothese sourcable)
- [ ] Micro-engagements cibles identifies
- [ ] Si R1 en call partage -> angle de repositionnement prepare
- [ ] Si fiabilite BASSE/MOYENNE -> qualification completee

**Si checklist non validee -> R2 reportee.**
**Si fiabilite BASSE et qualification non completee -> R2 bloquee.**

---

## Format de sortie — DECK-*.md

```markdown
# DECK R2 — {Entreprise}

> **Deal** #{deal_id} | **Score** {score}/100 — {verdict} | **Fiabilite** {fiabilite}
> **Angle R2** : {angle R2 du DEAL Section 6}
> **Question killer** : {question killer R2 du DEAL Section 6}
> **Date** : {YYYY-MM-DD}

---

## Part 1 — Audit Search

### Validation brief
{resultat de l'Etape 1 : VALIDATED ou ALERTE}

### Audit Search — {domaine 1}
{contenu de l'Etape 2 pour ce domaine}

### Audit Search — {domaine 2} (si applicable)
{contenu de l'Etape 2 pour ce domaine}

---

## Part 2 — 10 Slides R2

### Slide 1 — {Titre}
**Sous-titre :** {sous-titre}
- {bullet 1}
- {bullet 2}
- {bullet 3}

> **Notes speaker :** {ce que le closer dit}

---

### Slide 2 — {Titre}
[...]

---

## Part 3 — Ammunition

### Objections probables
{contenu de l'Etape 4}

### Script de fin R2
{contenu de l'Etape 5}

### ROI projete
#### Chaine de calcul
{methode primaire : chaine de trafic detaillee}
#### Tableau des hypotheses
{tableau source/valeur/justification pour chaque hypothese}
#### Ce que ca veut dire concretement
{2-3 phrases en francais courant, sans jargon, impact business}

---

## Part 4 — Pre-R2 Checklist
{contenu de l'Etape 7}

---

### METADATA

{
  "deck_id": "DECK-{YYYYMMDD}-{entreprise-slug}",
  "pipedrive_deal_id": 0,
  "deal_source": "DEAL-{date}-{entreprise-slug}.md",
  "date_deck": "YYYY-MM-DD",
  "auteur": "Deal Analyst Agent",
  "version": "8.0",
  "status": "DRAFT",
  "domaines_analyses": ["example.com"],
  "dataseo_fetch_date": "YYYY-MM-DD"
}
```
