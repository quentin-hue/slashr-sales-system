# Specs Workflows n8n — SLASHR Sales System v3.0

> Ce document est la référence pour construire les 3 workflows dans n8n.
> Chaque workflow est décrit node par node avec la config exacte.

---

## Convention Google Drive

Le closer crée manuellement un dossier Drive par deal et colle le lien dans Pipedrive (`dossier_r1_link`, field id 58).

Structure attendue du dossier Drive :
```
📁 {Nom Prospect}/
├── transcript_r1.txt          ← déposé par le closer
├── notes_closer.txt           ← optionnel
├── cdc_prospect.pdf           ← optionnel
├── email_prospect.txt         ← optionnel
├── DEAL-{date}.md             ← généré par Workflow 1
├── RELANCES-{date}.md         ← généré par Workflow 3
└── Deck R2 - {Prospect}       ← Google Slides généré par Workflow 2
```

Convention de nommage des fichiers source (préfixe → type) :
- `transcript*` → transcript
- `notes*` → notes_closer
- `cdc*` / `cahier*` / `brief*` / `rfp*` / `spec*` → document_prospect
- `email*` / `mail*` → email_prospect
- autre → document

---

## Credentials nécessaires dans n8n

| Credential | Type | Où le trouver |
|-----------|------|---------------|
| Pipedrive API | API Token | `~/.pipedrive_token` ou Pipedrive > Settings > API |
| Claude API | API Key | `ANTHROPIC_API_KEY` |
| DataForSEO | Login + Password | `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` |
| Google OAuth | OAuth2 | n8n > Credentials > Google OAuth2 (scopes: Drive, Slides, Gmail) |

---

## WORKFLOW 1 — "R1 Done → Dossier Deal"

**Trigger** : Pipedrive webhook — deal.updated (stage change vers R1 Done, stage_id=2)

### Node 1 — Trigger Pipedrive
- **Type** : Pipedrive Trigger
- **Event** : deal.updated
- **Filtre** : `current.stage_id == 2` (R1 Done) ET `previous.stage_id != 2` (évite les re-triggers)

### Node 2 — Vérifier dossier_r1_link
- **Type** : IF
- **Condition** : le champ `dossier_r1_link` (field key `1fd2ec1073fa60e11fb59bddfec7a2f6656c4b0c`) n'est pas vide
- **Si vide → Branch ERREUR** (Node 2b)
- **Si rempli → continuer** (Node 3)

### Node 2b — Notifier lien manquant
- **Type** : Gmail (ou Email)
- **À** : closer (toi)
- **Objet** : `⚠️ SLASHR — Deal "{deal.title}" sans lien Drive`
- **Corps** : `Le deal "{deal.title}" est passé en R1 Done mais le champ dossier_r1_link est vide. Renseigne le lien du dossier Drive puis remets le deal en R1 Done pour relancer l'analyse.`
- **FIN du workflow pour ce branch**

### Node 3 — Extraire l'ID du dossier Drive
- **Type** : Code (JavaScript)
- **Code** :
```javascript
const driveLink = $input.first().json.current['1fd2ec1073fa60e11fb59bddfec7a2f6656c4b0c'];
// Extraire l'ID du dossier depuis l'URL Google Drive
// Formats possibles :
// https://drive.google.com/drive/folders/ABC123
// https://drive.google.com/drive/u/0/folders/ABC123
const match = driveLink.match(/folders\/([a-zA-Z0-9_-]+)/);
const folderId = match ? match[1] : null;

// Extraire le domaine prospect depuis l'org du deal (si disponible)
const orgName = $input.first().json.current.org_name || '';
const dealTitle = $input.first().json.current.title || '';

return [{ json: { folderId, driveLink, orgName, dealTitle, dealId: $input.first().json.current.id } }];
```

### Node 4 — Lister les fichiers du dossier Drive
- **Type** : Google Drive — Search Files
- **Folder ID** : `{{ $json.folderId }}`
- **Filtre** : exclure les fichiers déjà générés (DEAL-*, RELANCES-*, Deck R2*)

### Node 5 — Télécharger et concaténer les fichiers
- **Type** : Code (JavaScript)
- **Logique** :
  - Pour chaque fichier, déterminer le type via le préfixe du nom
  - Concaténer avec marqueurs `=== SOURCE: {filename} (type: {type}) ===`
  - Les Google Docs sont convertis en texte brut via l'API
  - Les PDF sont lus via l'API Drive export
```javascript
// Input : array de fichiers téléchargés avec leur contenu
const files = $input.all();
let concatenated = '';

for (const file of files) {
  const filename = file.json.name.toLowerCase();
  let sourceType = 'document';

  if (filename.startsWith('transcript')) sourceType = 'transcript';
  else if (filename.startsWith('notes')) sourceType = 'notes_closer';
  else if (['cdc', 'cahier', 'brief', 'rfp', 'spec'].some(p => filename.startsWith(p))) sourceType = 'document_prospect';
  else if (filename.startsWith('email') || filename.startsWith('mail')) sourceType = 'email_prospect';

  concatenated += `\n=== SOURCE: ${file.json.name} (type: ${sourceType}) ===\n\n`;
  concatenated += file.json.content || file.json.text || '[Contenu non lisible]';
  concatenated += `\n\n=== FIN SOURCE: ${file.json.name} ===\n`;
}

return [{ json: { dossierContent: concatenated, fileCount: files.length } }];
```

### Node 6 — Enrichissement DataForSEO
- **Type** : HTTP Request (×3 en parallèle, ou séquentiel)
- **Condition** : le deal a un champ domaine OU on l'extrait de l'org Pipedrive
- **Si pas de domaine** : skip, mettre `dataforseoContext = "ENRICHISSEMENT DATAFORSEO : NON DISPONIBLE"`

**6a — Domain Rank Overview**
- POST `https://api.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live`
- Auth : Basic (DATAFORSEO_LOGIN:DATAFORSEO_PASSWORD)
- Body : `[{"target": "{domain}", "language_code": "fr", "location_name": "France"}]`

**6b — Ranked Keywords (top 20)**
- POST `https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live`
- Body : `[{"target": "{domain}", "language_code": "fr", "location_name": "France", "limit": 20, "order_by": ["ranked_serp_element.serp_item.rank_group,asc"]}]`

**6c — Competitors (top 5)**
- POST `https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live`
- Body : `[{"target": "{domain}", "language_code": "fr", "location_name": "France", "limit": 5}]`

### Node 7 — Appel Claude API (Deal Analyst)
- **Type** : HTTP Request
- **Method** : POST
- **URL** : `https://api.anthropic.com/v1/messages`
- **Headers** :
  - `x-api-key` : `{{ $credentials.claudeApi.apiKey }}`
  - `anthropic-version` : `2023-06-01`
  - `Content-Type` : `application/json`
- **Body** :
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 12000,
  "system": "CONTENU DE prompts/deal_analyst_system.md",
  "messages": [{
    "role": "user",
    "content": "## DOSSIER R1\n\n{{ $json.dossierContent }}\n\n{{ $json.dataforseoContext }}\n\n---\n\n**Mode : ANALYSE**\n\nAnalyse ce dossier R1 et produis le dossier deal complet.\n\nDate du jour : {{ $now.format('yyyy-MM-dd') }}"
  }]
}
```

> **Note** : Le system prompt (`deal_analyst_system.md`) doit être stocké dans n8n
> en tant que variable statique ou lu depuis un Google Doc partagé.
> Recommandation : le stocker en tant que **n8n Static Data** ou **Credential note**.

### Node 8 — Parser la réponse Claude
- **Type** : Code (JavaScript)
```javascript
const response = $input.first().json;
const content = response.content[0].text;

// Extraire score, verdict, fiabilité du JSON dans la réponse
const scoreMatch = content.match(/"score_total":\s*(\d+)/);
const verdictMatch = content.match(/"verdict":\s*"([^"]+)"/);
const fiabiliteMatch = content.match(/"fiabilite":\s*"([^"]+)"/);

const score = scoreMatch ? parseInt(scoreMatch[1]) : null;
const verdict = verdictMatch ? verdictMatch[1] : null;
const fiabilite = fiabiliteMatch ? fiabiliteMatch[1] : null;

// Mapping verdict → Pipedrive enum IDs
const verdictMap = { 'R2_GO': 89, 'R2_CONDITIONAL': 90, 'NURTURE': 91 };
const fiabiliteMap = { 'HAUTE': 92, 'MOYENNE': 93, 'BASSE': 94 };

return [{
  json: {
    dealContent: content,
    score,
    verdict,
    fiabilite,
    verdictPipedriveId: verdictMap[verdict] || null,
    fiabilitePipedriveId: fiabiliteMap[fiabilite] || null
  }
}];
```

### Node 9 — Sauvegarder DEAL-*.md dans Google Drive
- **Type** : Google Drive — Create File
- **Folder ID** : `{{ $json.folderId }}` (du Node 3)
- **File Name** : `DEAL-{{ $now.format('yyyyMMdd') }}-{{ $json.dealTitle }}.md`
- **Content** : `{{ $json.dealContent }}`

### Node 10 — Mettre à jour Pipedrive
- **Type** : Pipedrive — Update Deal
- **Deal ID** : `{{ $json.dealId }}`
- **Fields** :
  - `e529595ef908cdf5851df4355bbce866f322fcae` (r1_score) : `{{ $json.score }}`
  - `10acdb5b3c31d46baa19936775b00758edf6d6bc` (r1_verdict) : `{{ $json.verdictPipedriveId }}`
  - `25258b25cbbe4e3ed41546251476ae752156f8aa` (r1_fiabilite) : `{{ $json.fiabilitePipedriveId }}`
- **Si verdict = R2_GO** : `stage_id` → `7` (R2 Scheduled)
- **Si verdict = R2_CONDITIONAL** : `stage_id` reste à `2` (R1 Done, le closer décide)
- **Si verdict = NURTURE** : ne pas changer le stage

### Node 11 — Notifier le closer
- **Type** : Gmail
- **À** : closer
- **Objet** : `✅ Dossier deal "{dealTitle}" — Score {{ score }}/100 — {{ verdict }}`
- **Corps** :
```
Dossier deal généré pour {{ dealTitle }}.

Score : {{ score }}/100
Verdict : {{ verdict }}
Fiabilité : {{ fiabilite }}

📁 Dossier Drive : {{ driveLink }}

{{ verdict == 'R2_GO' ? '→ Deal déplacé en R2 Scheduled. Vérifie le deck et la checklist.' : '' }}
{{ verdict == 'R2_CONDITIONAL' ? '→ Deal reste en R1 Done. Actions pré-R2 requises avant de continuer.' : '' }}
{{ verdict == 'NURTURE' ? '→ Deal non qualifié. Pas de R2. Voir la recommandation dans le dossier.' : '' }}

Ce dossier est un DRAFT — à valider avant usage.
```

---

## WORKFLOW 2 — "R2 Scheduled → Deck Slides"

**Trigger** : Pipedrive webhook — deal.updated (stage change vers R2 Scheduled, stage_id=7)

### Node 1 — Trigger Pipedrive
- **Event** : deal.updated
- **Filtre** : `current.stage_id == 7` ET `previous.stage_id != 7`

### Node 2 — Récupérer le DEAL-*.md depuis Drive
- **Type** : Google Drive — Search Files
- **Folder ID** : extrait de `dossier_r1_link`
- **Query** : `name contains 'DEAL-'` et `mimeType = 'text/markdown'` ou `mimeType = 'text/plain'`

### Node 3 — Lire le contenu du fichier
- **Type** : Google Drive — Download File

### Node 4 — Appel Claude API (génération contenu slides)
- **Type** : HTTP Request
- **System prompt** : Prompt dédié slides (ci-dessous)
- **User message** : Le contenu du DEAL-*.md
- **Prompt slides** :
```
Tu reçois un dossier deal SLASHR. Génère le contenu textuel pour 10 slides de R2.

Pour chaque slide, donne :
- Titre (max 8 mots)
- Sous-titre (1 ligne)
- Bullet points (max 4, max 15 mots chacun)
- Note speaker (ce que le closer doit dire, 2-3 phrases)

Structure des 10 slides :
1. Contexte prospect
2. Diagnostic data
3. Coût de l'inaction
4. Vision cible
5. Recommandation stratégique (3 piliers)
6. Quick wins 90 jours
7. Équipe et méthode
8. Investissement
9. ROI projeté
10. Décision (slide vide — script de fin)

Format de sortie : JSON array de 10 objets.
```

### Node 5 — Créer le Google Slides
- **Type** : Google Slides API (HTTP Request)
- **Méthode** : Copier un template existant, puis remplacer les placeholders
- **Template ID** : à stocker dans n8n (tu crées un master template une fois)
- **Pour chaque slide** : `replaceAllText` avec les données du JSON Claude

### Node 6 — Sauvegarder le lien dans Pipedrive
- **Type** : Pipedrive — Update Deal
- **Field** : `r2_pack_link` → lien du Google Slides créé

### Node 7 — Créer activité "Pre-R2 Checklist"
- **Type** : Pipedrive — Create Activity
- **Type d'activité** : `pre_r2_checklist` (id: 10)
- **Deal ID** : `{{ $json.dealId }}`
- **Subject** : `Pre-R2 Checklist — {{ dealTitle }}`
- **Due date** : aujourd'hui

### Node 8 — Notifier le closer
- **Objet** : `📊 Deck R2 "{dealTitle}" prêt`
- **Corps** : Lien Slides + rappel "Checklist à valider avant R2"

---

## WORKFLOW 3 — "R2 Done + 48h → Relances"

**Trigger** : Pipedrive webhook — deal.updated (stage change vers R2 Done, stage_id=4)

### Node 1 — Trigger Pipedrive
- **Event** : deal.updated
- **Filtre** : `current.stage_id == 4` ET `previous.stage_id != 4`

### Node 2 — Wait 48h
- **Type** : Wait
- **Duration** : 48 heures

### Node 3 — Vérifier que le deal est toujours en R2 Done
- **Type** : Pipedrive — Get Deal
- **Deal ID** : `{{ $json.dealId }}`
- **Condition** : si `stage_id != 4` (deal a bougé) → STOP
- **Si `stage_id == 4`** → continuer

### Node 4 — Récupérer le DEAL-*.md depuis Drive
- (identique au Workflow 2, Node 2-3)

### Node 5 — Récupérer l'email du contact prospect
- **Type** : Pipedrive — Get Person (lié au deal)
- **Extraire** : `email`, `first_name`

### Node 6 — Appel Claude API (mode RELANCES)
- **Type** : HTTP Request
- **System prompt** : `deal_analyst_system.md` (le mode RELANCES est dedans)
- **User message** :
```
## DOSSIER DEAL — CONTEXTE PROSPECT

{{ dealContent }}

---

**Mode : RELANCES POST-R2**

Email prospect : {{ prospectEmail }}
Prénom : {{ prospectFirstName }}
Entreprise : {{ orgName }}

Génère les 3 emails de relance personnalisés (J+5, J+12, J+20).
Variables toutes remplies. Prêts à copier dans Gmail.

Date du jour : {{ $now.format('yyyy-MM-dd') }}
```

### Node 7 — Parser les 3 emails
- **Type** : Code (JavaScript)
- Extraire les 3 emails du markdown (split sur "Touch 1", "Touch 2", "Touch 3")
- Pour chaque email : extraire objet + corps

### Node 8 — Sauvegarder RELANCES-*.md dans Drive
- **Type** : Google Drive — Create File
- **Folder ID** : dossier du deal
- **File Name** : `RELANCES-{{ $now.format('yyyyMMdd') }}.md`

### Node 9 — Créer 3 brouillons Gmail
- **Type** : Gmail — Create Draft (×3)
- **Draft 1** (J+5) :
  - To : `{{ prospectEmail }}`
  - Subject : `{{ touch1_subject }}`
  - Body : `{{ touch1_body }}`
- **Draft 2** (J+12) : idem avec touch2
- **Draft 3** (J+20) : idem avec touch3

### Node 10 — Créer 3 activités Pipedrive
- **Type** : Pipedrive — Create Activity (×3)
- **Activité 1** :
  - Type : `relance_j5` (id: 11)
  - Subject : `Relance J+5 à envoyer — {{ dealTitle }}`
  - Due date : `{{ $now.plus(5, 'days').format('yyyy-MM-dd') }}`
- **Activité 2** :
  - Type : `relance_j12` (id: 12)
  - Due date : `{{ $now.plus(12, 'days').format('yyyy-MM-dd') }}`
- **Activité 3** :
  - Type : `relance_j20` (id: 13)
  - Due date : `{{ $now.plus(20, 'days').format('yyyy-MM-dd') }}`

### Node 11 — Mettre à jour relance_status
- **Type** : Pipedrive — Update Deal
- **Field** : `relance_status` → `PAS_COMMENCEE` (id: 98)

### Node 12 — Notifier le closer
- **Objet** : `📧 3 relances prêtes — "{dealTitle}"`
- **Corps** :
```
3 brouillons Gmail créés pour {{ dealTitle }}.

📌 J+5 ({{ dueDate1 }}) : "{{ touch1_subject }}"
📌 J+12 ({{ dueDate2 }}) : "{{ touch2_subject }}"
📌 J+20 ({{ dueDate3 }}) : "{{ touch3_subject }}"

Activités créées dans Pipedrive avec les dates d'envoi.

⚠️ Ces emails sont des BROUILLONS — relis et envoie manuellement.
```

---

## IDs Pipedrive — Référence rapide

### Stages
| Stage | ID |
|-------|----|
| Lead In | 1 |
| R1 Scheduled | 6 |
| R1 Done | 2 |
| R2 Scheduled | 7 |
| R2 Done | 4 |
| Pending Signature | 8 |

### Deal Fields (custom)
| Champ | Key hash | ID |
|-------|----------|----|
| r1_score | `e529595ef908cdf5851df4355bbce866f322fcae` | 52 |
| r1_verdict | `10acdb5b3c31d46baa19936775b00758edf6d6bc` | 53 |
| r1_fiabilite | `25258b25cbbe4e3ed41546251476ae752156f8aa` | 54 |
| r2_pack_link | `4b84e7bfe1a6b330318fc7a0d208e2faedf2530a` | 55 |
| decideur_level | `0b4c7e8cc10ced7badf65b34dac6254bd10a0179` | 56 |
| relance_status | `e2ed93c97e15989382085b83caca790da0e516d3` | 57 |
| dossier_r1_link | `1fd2ec1073fa60e11fb59bddfec7a2f6656c4b0c` | 58 |

### Enum Values
| Champ | Valeur | ID |
|-------|--------|----|
| r1_verdict | R2_GO | 89 |
| r1_verdict | R2_CONDITIONAL | 90 |
| r1_verdict | NURTURE | 91 |
| r1_fiabilite | HAUTE | 92 |
| r1_fiabilite | MOYENNE | 93 |
| r1_fiabilite | BASSE | 94 |
| relance_status | PAS_COMMENCEE | 98 |
| relance_status | J5_ENVOYEE | 99 |
| relance_status | J12_ENVOYEE | 100 |
| relance_status | J20_ENVOYEE | 101 |
| relance_status | REPONSE | 102 |

### Activity Types
| Activité | ID | Key |
|----------|----|-----|
| Valider R1 Done | 9 | valider_r1_done |
| Pre-R2 Checklist | 10 | pre_r2_checklist |
| Relance J+5 | 11 | relance_j5 |
| Relance J+12 | 12 | relance_j12 |
| Relance J+20 | 13 | relance_j20 |

---

## Checklist de déploiement

- [ ] Créer les credentials dans n8n (Pipedrive, Claude API, DataForSEO, Google OAuth)
- [ ] Stocker le system prompt `deal_analyst_system.md` en variable n8n ou Google Doc
- [ ] Créer le template Google Slides master pour les decks R2
- [ ] Configurer les webhooks Pipedrive (deal.updated) vers n8n
- [ ] Construire Workflow 1 (R1 Done → Dossier Deal)
- [ ] Tester Workflow 1 avec le deal Decathlon Fitness Club
- [ ] Construire Workflow 2 (R2 Scheduled → Deck Slides)
- [ ] Construire Workflow 3 (R2 Done → Relances)
- [ ] Test end-to-end sur un deal complet
