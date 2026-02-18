# Setup Google Drive API — Service Account

## Pourquoi un Service Account

Un Service Account permet à Claude Code de lire/écrire dans Google Drive sans OAuth interactif.
Ça fonctionne partout : Mac local, serveur cloud, CI/CD.

## Setup (une seule fois)

### 1. Créer le projet Google Cloud

1. Va sur https://console.cloud.google.com
2. Crée un projet : "SLASHR Sales System"
3. Active l'API Google Drive : APIs & Services → Enable → "Google Drive API"

### 2. Créer le Service Account

1. APIs & Services → Credentials → Create Credentials → Service Account
2. Nom : "slashr-sales-agent"
3. Rôle : aucun (on partage le Drive directement)
4. Clique sur le Service Account créé → Keys → Add Key → JSON
5. Télécharge le fichier JSON → renomme en `google_service_account.json`

### 3. Stocker les credentials

```bash
mv ~/Downloads/google_service_account.json ~/.google_service_account.json
chmod 600 ~/.google_service_account.json
```

### 4. Partager le Drive avec le Service Account

Le Service Account a une adresse email du type :
`slashr-sales-agent@slashr-sales-system.iam.gserviceaccount.com`

1. Va dans Google Drive
2. Ouvre le dossier racine partagé de SLASHR (celui qui contient les dossiers deals)
3. Clic droit → Partager → colle l'email du Service Account
4. Permission : **Éditeur** (pour pouvoir écrire les outputs)

### 5. Vérifier

```bash
# Le script ci-dessous teste l'accès
python3 setup/test_drive_access.py
```

## Comment ça marche

1. Claude Code lit `~/.google_service_account.json`
2. Génère un JWT token signé
3. L'échange contre un access token Google (valide 1h)
4. Utilise l'access token pour les appels API Drive (lister, lire, écrire)

Tout se fait via `curl` — pas de SDK, pas de dépendance.

## Shared Drive (Drive partagé d'équipe)

⚠️ **SLASHR utilise un Shared Drive** (pas "Mon Drive"). Toutes les requêtes API doivent inclure :

- `supportsAllDrives=true` — sur chaque appel (get, list, create, update)
- `includeItemsFromAllDrives=true` — sur les appels list

Sans ces paramètres, l'API retourne 404 même si le partage est correct.

**Shared Drive ID :** `0ABVHWXVZf0ogUk9PVA`

## Référence API

Tous les exemples incluent les paramètres Shared Drive :

- Lister les fichiers d'un dossier : `GET https://www.googleapis.com/drive/v3/files?q='{folderId}'+in+parents&supportsAllDrives=true&includeItemsFromAllDrives=true`
- Lire le contenu d'un fichier : `GET https://www.googleapis.com/drive/v3/files/{fileId}?alt=media&supportsAllDrives=true`
- Exporter un Google Doc en texte : `GET https://www.googleapis.com/drive/v3/files/{fileId}/export?mimeType=text/plain`
- Créer un fichier : `POST https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true`
- Metadata d'un fichier : `GET https://www.googleapis.com/drive/v3/files/{fileId}?fields=id,name,mimeType&supportsAllDrives=true`
