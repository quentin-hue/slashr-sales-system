# Mode PROPOSAL — Proposition commerciale client-facing (v8.0)

> **Prerequis :** `agents/shared.md` lu. Input : DECK-*.md + DEAL-*.md lus depuis Drive.

---

## Objectif

Generer une proposition commerciale HTML presentable au prospect en R2. C'est la **version client-facing du DECK** — filtree (pas d'objections, pas de script, pas de checklist) et enrichie (couverture, intro, CTA).

---

## Input

- Le fichier DECK-*.md (obligatoire — la proposal se genere APRES le deck)
- Le fichier DEAL-*.md (donnees prospect, scoring, angle R2)
- Le template `templates/proposal_base.html`
- Les references : `context/design_system.md` + `context/positioning.md`

---

## Mapping DECK -> Proposal

| Source DECK | -> Proposal ? | Section Proposal |
|-------------|--------------|------------------|
| Part 1 — Audit Search (data) | OUI (sans validation brief) | Diagnostic |
| Part 2 — Slides 1-9 | OUI (transformees en sections narratives) | Contexte -> Investissement |
| Part 2 — Slide 10 (Decision) | NON (script interne) | — |
| Part 3 — Objections | NON (interne) | — |
| Part 3 — Script fin R2 | NON (interne) | — |
| Part 3 — ROI projete | OUI (chaine + hypotheses + resume) | Business Case |
| Part 4 — Checklist | NON (interne) | — |

**Regle stricte :** les objections probables, le script de fin R2, et la checklist ne doivent JAMAIS apparaitre dans la proposal. Ce sont des outils internes du closer.

---

## Mapping variables HTML -> sources DECK

Chaque variable `{{...}}` du template a une source primaire et un fallback si la donnee manque.

| Variable template | Source primaire | Fallback si absent |
|---|---|---|
| `{{entreprise}}` | DEAL Section 1 (nom entreprise) | Pipedrive org name |
| `{{date}}` | Date de generation | — |
| `{{resume_executif}}` | DEAL Section 6 (angle R2) + DECK header | Reformuler DEAL Section 2 (douleur + risque) |
| `{{kpi_cards}}` | DECK Part 1 Audit Search (trafic, mots-cles, ETV, gap) | Omettre la card manquante — minimum 2 cards |
| `{{diagnostic_content}}` | DECK Part 1 (top 10 mots-cles hors-marque) | Top 5 si donnees insuffisantes |
| `{{benchmark_table}}` | DECK Part 1 (benchmark concurrentiel) | Prospect + top 3 concurrents minimum |
| `{{opportunity_content}}` | DEAL Section 2 (risque inaction) + DECK Slides 3-4 | Reformuler le gap concurrentiel en impact business |
| `{{approach_intro}}` | DECK Slide 5 (intro reco) | 1 phrase : "Notre recommandation s'articule en 3 phases" |
| `{{phase_cards}}` | DECK Slides 5-6 (3 phases) | **OBLIGATOIRE** — toujours 3 phases |
| `{{quick_wins}}` | DECK Slide 6 (quick wins 90j) | **OBLIGATOIRE** — 3 actions minimum |
| `{{team_content}}` | DECK Slide 7 + `positioning.md` | Description generique SLASHR |
| `{{pricing_intro}}` | DECK Slide 8 (intro pricing) | "Trois scenarios adaptes a votre ambition" |
| `{{pricing_cards}}` | DECK Slide 8 (scenarios) | **OBLIGATOIRE** — alerte closer si absent |
| `{{roi_chain}}` | DECK Part 3 ROI (chaine de calcul) | Omettre section si ROI non calcule — alerte closer |
| `{{roi_hypotheses_table}}` | DECK Part 3 ROI (tableau hypotheses) | Omettre si ROI absent |
| `{{roi_concrete}}` | DECK Part 3 ROI ("concretement") | Omettre si ROI absent |
| `{{next_steps}}` | 2-3 steps standards | Toujours present |
| `{{closer_email}}` | Pipedrive (email du closer / owner du deal) | Demander au closer |

**Si une section OBLIGATOIRE manque dans le DECK** -> inserer un commentaire HTML `<!-- ALERTE CLOSER : {variable} manquante dans le DECK. A completer avant envoi. -->` et generer un placeholder visible.

---

## Structure de la proposal — 9 sections

### Section 1 — Couverture
- Nom de l'entreprise prospect
- "Proposition strategique Search & IA"
- Date
- Tag SLASHR
- Design : gradient hero (3 blobs orange/magenta/violet sur fond `#1a1a1a`)

### Section 2 — Resume executif
- 3-4 bullets maximum
- Opportunite identifiee + approche proposee
- C'est le hook — pas de data encore, juste la promesse
- Source : DEAL Section 6 (angle R2) + DECK header (angle R2)

### Section 3 — Diagnostic
- **KPI cards** (3-4) : trafic organique, mots-cles positionnes, ETV, gap concurrentiel
- Top 10 mots-cles hors-marque (filtre depuis DECK Part 1 — top 20 reduit, marque exclue)
- Tableau benchmark concurrentiel (prospect vs top 3-5 concurrents)
- ETV avec explication : "ce que couterait ce trafic en achat Google Ads"
- Source : DECK Part 1 Audit Search

### Section 4 — L'opportunite
- Cout de l'inaction (chiffre en euros ou %)
- Gap vs concurrents (ratio x, visiteurs perdus)
- Vision cible : ce que ca donne si on corrige
- Source : DEAL Section 2 (risque inaction) + DECK Part 2 Slides 3-4

### Section 5 — Notre approche
- 3 phases temporelles en cards :
  - **M1-3 : Fondations** (orange) — audit, quick wins, socle technique
  - **M3-6 : Acceleration** (magenta) — contenu, autorite, positions
  - **M6-12 : Autorite** (violet) — visibilite durable, GEO/IA, scale
- Pour chaque phase : 2-3 actions concretes + resultats attendus
- Quick wins 90 jours (3 actions specifiques)
- Source : DECK Part 2 Slides 5-6

### Section 6 — Equipe et execution
- Taille equipe dediee
- Frequence livrables / points de contact
- Outils et dashboards
- Methodologie
- Source : DECK Part 2 Slide 7 + `positioning.md`

### Section 7 — Investissement
- 2-3 scenarios en pricing cards :
  - Nom du scenario (Essentiel / Performance / Croissance)
  - Perimetre
  - Montant
  - Le scenario recommande est marque visuellement
- Le closer ajuste les montants avant envoi
- Source : DECK Part 2 Slide 8

### Section 8 — Business case
- Chaine de calcul ROI (trafic actuel -> gap -> gain projete -> valorisation)
- Tableau des hypotheses (source, valeur, justification pour chaque hypothese)
- "Concretement" : 2-3 phrases en francais courant, sans jargon, impact business
- Source : DECK Part 3 ROI projete

### Section 9 — Prochaines etapes
- 2-3 next steps concrets (ex : signer LOI, planifier kick-off, transmettre acces)
- CTA button avec email du closer
- Pas de pression — ton partenaire strategique

---

## Adaptation par profil decideur

Le `decideur_level` du DEAL module la profondeur des sections.

| Profil | Sections a developper | Sections a alleger |
|--------|----------------------|-------------------|
| **DECIDEUR** (C-level) | Opportunite (S4), Business case (S8), Investissement (S7) — impact business, ROI, vision | Diagnostic (S3) abregé, Equipe (S6) abregee |
| **INFLUENCEUR** (Head of) | Approche (S5), Equipe (S6), Quick wins — comment on fait, avec quoi | Business case (S8) simplifie ("concretement" suffit) |
| **OPERATIONNEL** (Manager) | Diagnostic (S3), Approche (S5), Quick wins — data detaillee, actions concretes | Opportunite (S4) allegee, Business case (S8) simplifie |

**Regle :** adapter la longueur, pas le contenu. Toutes les sections sont presentes. Le closer peut aussi overrider ce comportement.

---

## Regles de transformation slides -> prose

Le DECK est ecrit en format "slides" (bullets + notes speaker). La proposal transforme ce contenu en **prose narrative client-facing**.

**Regles de transformation par type de contenu :**

| Type de contenu DECK | Transformation proposal |
|---------------------|------------------------|
| **Data brute** (ex: "Trafic : 12K/mois") | Phrase avec contexte : "Votre site genere aujourd'hui 12 000 visites organiques par mois" |
| **Bullet d'action** (ex: "Audit technique + quick wins") | Paragraphe avec resultat attendu : "Dans les 90 premiers jours, nous realisons un audit technique complet et identifions les quick wins — des corrections rapides qui liberent du trafic immediatement" |
| **Benchmark** (ex: "Prospect : 12K vs Concurrent A : 45K") | Comparaison narrative : "La ou votre site capte 12 000 visiteurs, votre concurrent principal en attire 45 000 — un ecart de 3,7x qui represente autant de clients potentiels" |
| **Notes speaker** (ex: "[pause] Laisser reagir") | **SUPPRIMER** — contenu interne |
| **Chiffre seul** (ex: "ETV : 8 500 EUR") | Chiffre contextualise : "La valeur equivalente en publicite de votre trafic organique est de 8 500 EUR — ce que vous devriez depenser en Google Ads pour obtenir le meme volume de visites" |
| **Recommandation** (ex: "3 piliers : fondations, acceleration, autorite") | Phrase narrative : "Notre approche s'articule autour de trois phases progressives" |

**Registre :** le prospect lit cette proposal seul. Le ton est ecrit (pas oral), fluide, sans bullet points isoles. Chaque paragraphe fait 2-4 phrases. Le vocabulaire est accessible — si un terme technique est utilise, il est immediatement explique entre parentheses.

---

## Exemples HTML des composants dynamiques

L'agent genere du HTML pour les zones `{{...}}` dynamiques. Voici le markup attendu pour chaque composant.

### KPI Card
```html
<div class="kpi-card">
  <div class="kpi-value">12 400</div>
  <div class="kpi-label">Visiteurs organiques / mois</div>
  <div class="kpi-detail">Source : DataForSEO, fevrier 2026</div>
</div>
```

### Phase Card
```html
<div class="phase-card phase-1">
  <span class="phase-tag">M1-3 : Fondations</span>
  <h3>Poser les bases</h3>
  <p>Audit technique, corrections prioritaires et premiers quick wins pour liberer du trafic existant.</p>
  <ul>
    <li>Audit SEO technique complet</li>
    <li>Correction des erreurs critiques</li>
    <li>Optimisation des 10 pages a plus fort potentiel</li>
  </ul>
</div>
```
Classes : `.phase-1` (orange), `.phase-2` (magenta), `.phase-3` (violet).

### Pricing Card
```html
<div class="pricing-card recommended">
  <div class="pricing-name">Performance</div>
  <div class="price">3 500 &euro;</div>
  <div class="price-period">par mois, engagement 6 mois</div>
  <div class="pricing-scope">SEO technique + contenu + autorite. Reporting mensuel. Point bi-mensuel.</div>
</div>
```
Ajouter `.recommended` sur le scenario recommande. Le badge "Recommande" s'affiche automatiquement via CSS.

### Benchmark Table
```html
<table>
  <thead>
    <tr>
      <th>Domaine</th>
      <th>Trafic organique</th>
      <th>Mots-cles</th>
      <th>Valeur equiv. pub.</th>
    </tr>
  </thead>
  <tbody>
    <tr class="prospect-row">
      <td>prospect.fr</td>
      <td class="highlight">12 400</td>
      <td>890</td>
      <td>8 500 &euro;</td>
    </tr>
    <tr>
      <td>concurrent-a.fr</td>
      <td>45 200</td>
      <td>3 400</td>
      <td>32 000 &euro;</td>
    </tr>
  </tbody>
</table>
```
La ligne du prospect utilise la classe `.prospect-row` (mise en gras). Les chiffres cles du prospect utilisent `.highlight` (orange).

### Highlight Box (Business case "concretement")
```html
<div class="highlight-box">
  <strong>Concretement :</strong> En comblant 30% du gap avec votre concurrent principal, vous pourriez capter 10 000 visiteurs supplementaires par mois — soit l'equivalent de 25 000 EUR en achat publicitaire annuel.
</div>
```

---

## Regles de redaction

1. **Ton :** partenaire strategique. On recommande, on ne vend pas. "Voici ce que les donnees montrent, voici ce qu'on recommande"
2. **Data avant opinion :** chaque affirmation est appuyee par un chiffre ou une source
3. **Pas de jargon non explique :** CTR -> "taux de clic", ETV -> "valeur equivalente en publicite", SERP -> "resultats de recherche"
4. **Chaque section = 1 message cle.** Pas de section fourre-tout
5. **Max 3-4 bullets par section.** Le blanc est du design
6. **KPIs en orange** (`#E74601`). Highlights en magenta (`#CE08A9`)
7. **Chiffres du prospect d'abord**, benchmark ensuite, recommandation en dernier
8. **Max 15 ecrans** en rendu HTML. Si c'est plus long, condenser
9. **Confidentiel :** la proposal est un document confidentiel, personnalise en footer avec le nom du prospect
10. **Accents obligatoires** dans tout le contenu genere. Le HTML utilise les entites HTML (`&eacute;`, `&egrave;`, etc.) pour les titres du template, mais le contenu genere peut utiliser les caracteres UTF-8 directement

---

## Processus de generation

1. Lis le DECK-*.md et le DEAL-*.md
2. Lis le template `templates/proposal_base.html`
3. Identifie le `decideur_level` dans le DEAL -> adapte la profondeur des sections
4. Pour chaque variable `{{...}}`, extrais les data du DECK selon le mapping ci-dessus
5. Transforme les slides (format bullet/notes speaker) en **prose narrative** selon les regles de transformation
6. Genere le HTML des composants dynamiques selon les exemples (kpi-card, phase-card, pricing-card, table)
7. Remplace les `{{variables}}` du template par le contenu HTML genere
8. Si une donnee OBLIGATOIRE manque -> inserer commentaire `<!-- ALERTE CLOSER -->` + placeholder visible
9. Verifie : aucune objection, aucun script, aucune checklist, aucune note speaker
10. Genere le fichier PROPOSAL-*.html complet

---

## Format de sortie — PROPOSAL-*.html

Le fichier HTML complet, pret a etre ouvert dans un navigateur.

Nom : `PROPOSAL-{YYYYMMDD}-{entreprise-slug}.html`

**Pas de metadata JSON dans la proposal** — c'est un document client-facing. Les metadata restent dans le DECK.

---

## Validation

La proposal est **REJECTED** si :
1. Elle contient des objections, un script de fin, ou une checklist (contenu interne)
2. Elle contient des "notes speaker" (format interne du DECK)
3. Un chiffre est present sans source identifiable dans le DECK ou le DEAL
4. Le HTML ne respecte pas le design system (fond blanc, pas de dark mode, accents manquants)
5. Le ton est arrogant, suppliant, ou contient du jargon non explique
6. Elle depasse 15 ecrans de contenu
7. Une variable OBLIGATOIRE est vide sans alerte closer
