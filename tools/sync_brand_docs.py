#!/usr/bin/env python3
"""
sync_brand_docs.py — Synchronise les docs de marque SLASHR depuis Google Drive.

Telecharge les Google Docs de reference (plateforme de marque, tone of voice)
et les ecrit dans context/ pour que le systeme les utilise.

Usage:
    python3 tools/sync_brand_docs.py
    python3 tools/sync_brand_docs.py --force  # ignore le cache

Les docs sont caches 7 jours. Apres 7 jours, re-telechargement automatique.
Avec --force, re-telechargement immediat.

Exit codes: 0=OK, 1=erreur auth, 2=erreur reseau, 3=erreur ecriture
"""

import json
import os
import sys
import time
from pathlib import Path

# --- Configuration ---
# Google Doc IDs extraits des URLs de partage
BRAND_DOCS = {
    "brand_platform": {
        "doc_id": "1AyQA6jybaFntG3ZBoGvYBSlcPZm4D395",
        "output": "context/brand_platform.md",
        "description": "Plateforme de marque SLASHR",
    },
    "tone_of_voice": {
        "doc_id": "1LbSyv4axvZdnEPBNoGEPcmp9LDyzHdjA",
        "output": "context/tone_of_voice.md",
        "description": "Tone of Voice SLASHR",
    },
}

CACHE_MAX_AGE_SECONDS = 7 * 24 * 3600  # 7 jours
CREDENTIALS_PATH = os.path.expanduser("~/.google_service_account.json")
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_drive_service():
    """Authentification Google Drive via service account."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH,
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )
        return build("drive", "v3", credentials=creds)
    except FileNotFoundError:
        print(f"[ERROR] Credentials not found: {CREDENTIALS_PATH}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Auth failed: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_doc_as_text(service, doc_id, description):
    """Telecharge un doc depuis Drive (Google Doc natif ou .docx uploade)."""
    # 1. Verifier le type de fichier
    try:
        meta = (
            service.files()
            .get(fileId=doc_id, fields="mimeType,name", supportsAllDrives=True)
            .execute()
        )
        mime = meta.get("mimeType", "")
        name = meta.get("name", "")
        print(f"[INFO] {name} ({mime})")
    except Exception as e:
        print(f"[ERROR] Cannot access {description}: {e}", file=sys.stderr)
        return None

    # 2a. Google Doc natif → export text/plain
    if mime == "application/vnd.google-apps.document":
        try:
            content = (
                service.files()
                .export(fileId=doc_id, mimeType="text/plain")
                .execute()
            )
            text = content.decode("utf-8") if isinstance(content, bytes) else content
            print(f"[OK] {description} ({len(text)} chars)")
            return text
        except Exception as e:
            print(f"[ERROR] Export failed: {e}", file=sys.stderr)
            return None

    # 2b. .docx uploade → telecharger le binaire et parser
    if "word" in mime or name.endswith(".docx"):
        try:
            import io
            import zipfile
            import xml.etree.ElementTree as ET

            content = (
                service.files()
                .get_media(fileId=doc_id, supportsAllDrives=True)
                .execute()
            )

            # Parser le .docx (c'est un zip contenant du XML)
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                xml_content = z.read("word/document.xml")

            root = ET.fromstring(xml_content)
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

            paragraphs = []
            for para in root.iter(f"{{{ns['w']}}}p"):
                texts = []
                for run in para.iter(f"{{{ns['w']}}}t"):
                    if run.text:
                        texts.append(run.text)
                if texts:
                    paragraphs.append("".join(texts))

            text = "\n\n".join(paragraphs)
            print(f"[OK] {description} (.docx parsed, {len(text)} chars)")
            return text
        except Exception as e:
            print(f"[ERROR] .docx parsing failed: {e}", file=sys.stderr)
            return None

    # 2c. Autre format → telecharger brut
    try:
        content = (
            service.files()
            .get_media(fileId=doc_id, supportsAllDrives=True)
            .execute()
        )
        text = content.decode("utf-8") if isinstance(content, bytes) else str(content)
        print(f"[OK] {description} (raw, {len(text)} chars)")
        return text
    except Exception as e:
        print(f"[ERROR] Download failed for {description}: {e}", file=sys.stderr)
        return None


def should_refresh(output_path, force=False):
    """Verifie si le fichier cache doit etre rafraichi."""
    if force:
        return True
    if not output_path.exists():
        return True
    age = time.time() - output_path.stat().st_mtime
    if age > CACHE_MAX_AGE_SECONDS:
        days = int(age / 86400)
        print(f"[INFO] Cache stale ({days}j) : {output_path.name}")
        return True
    days = int(age / 86400)
    print(f"[SKIP] Cache fresh ({days}j) : {output_path.name}")
    return False


def write_doc(output_path, content, description):
    """Ecrit le contenu avec un header de metadata."""
    header = (
        f"# {description}\n\n"
        f"> Source : Google Doc (synchro automatique via `tools/sync_brand_docs.py`)\n"
        f"> Derniere synchro : {time.strftime('%Y-%m-%d %H:%M')}\n"
        f"> Pour mettre a jour : modifier le Google Doc, puis `python3 tools/sync_brand_docs.py --force`\n\n"
        f"---\n\n"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(header + content, encoding="utf-8")
    print(f"[WRITE] {output_path}")


def main():
    force = "--force" in sys.argv

    print("=== Sync Brand Docs ===")

    # Check which docs need refresh
    docs_to_fetch = {}
    for key, config in BRAND_DOCS.items():
        output_path = PROJECT_ROOT / config["output"]
        if should_refresh(output_path, force):
            docs_to_fetch[key] = config

    if not docs_to_fetch:
        print("\nTous les docs sont a jour. Utilisez --force pour forcer le rafraichissement.")
        return

    # Fetch only if needed
    service = get_drive_service()
    errors = 0

    for key, config in docs_to_fetch.items():
        content = fetch_doc_as_text(service, config["doc_id"], config["description"])
        if content:
            output_path = PROJECT_ROOT / config["output"]
            write_doc(output_path, content, config["description"])
        else:
            errors += 1

    print(f"\n{'='*30}")
    print(f"Synchro terminee : {len(docs_to_fetch) - errors} OK, {errors} erreurs")

    if errors:
        sys.exit(2)


if __name__ == "__main__":
    main()
