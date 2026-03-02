#!/usr/bin/env python3
"""
SLASHR Preflight Check — Validation des dependances API avant execution.

Verifie :
1. Pipedrive field keys (champs custom obligatoires)
2. Pipedrive enum IDs (decideur_level mapping)
3. Google Drive access (credentials + listing)
4. Cache (.cache/) : ecriture + fraicheur

Usage : python3 tools/preflight_check.py
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration ---

PIPEDRIVE_TOKEN_PATH = os.path.expanduser("~/.pipedrive_token")
GOOGLE_CREDS_PATH = os.path.expanduser("~/.google_service_account.json")
CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
STALE_THRESHOLD_DAYS = 7

REQUIRED_FIELD_KEYS = {
    "e529595ef908cdf5851df4355bbce866f322fcae": "r1_score",
    "0b4c7e8cc10ced7badf65b34dac6254bd10a0179": "decideur_level",
    "4b84e7bfe1a6b330318fc7a0d208e2faedf2530a": "r2_pack_link",
    "1fd2ec1073fa60e11fb59bddfec7a2f6656c4b0c": "dossier_r1_link",
    "f8c51fb60ea43a34c56998b6ad9bf946234149a1": "leviers_pressentis",
    "d76190f6be0ca288aeac6107f2fb5d784d0f5e28": "domaine_principal",
    "52fe480f70327c9f1a06bb113cfeabe398ae8f9c": "qualification_status",
}

REQUIRED_ENUM_IDS = {
    95: "DECIDEUR",
    96: "INFLUENCEUR",
    97: "OPERATIONNEL",
}

# --- Counters ---

criticals = 0
warnings = 0
results = []


def log_pass(msg):
    results.append(f"[PASS] {msg}")


def log_warn(msg):
    global warnings
    warnings += 1
    results.append(f"[WARN] {msg}")


def log_crit(msg):
    global criticals
    criticals += 1
    results.append(f"[CRIT] {msg}")


def log_skip(msg):
    results.append(f"[SKIP] {msg}")


# --- 1. Pipedrive field keys ---

def check_pipedrive_fields():
    """Validate that all required custom field keys exist in Pipedrive."""
    try:
        if not os.path.isfile(PIPEDRIVE_TOKEN_PATH):
            log_crit("Pipedrive: fichier token introuvable ({})".format(PIPEDRIVE_TOKEN_PATH))
            return None

        with open(PIPEDRIVE_TOKEN_PATH, "r") as f:
            token = f.read().strip()

        if not token:
            log_crit("Pipedrive: token vide dans {}".format(PIPEDRIVE_TOKEN_PATH))
            return None

        url = "https://api.pipedrive.com/v1/dealFields?api_token={}".format(token)
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        if not data.get("success"):
            log_crit("Pipedrive: API a repondu success=false")
            return None

        fields = data.get("data", [])
        field_keys_in_api = {f.get("key") for f in fields}

        missing = []
        for key, name in REQUIRED_FIELD_KEYS.items():
            if key not in field_keys_in_api:
                missing.append(name)

        found = len(REQUIRED_FIELD_KEYS) - len(missing)

        if missing:
            log_crit("Pipedrive field keys: {}/{} present. Manquants: {}".format(
                found, len(REQUIRED_FIELD_KEYS), ", ".join(missing)
            ))
        else:
            log_pass("Pipedrive field keys: {}/{} present".format(found, len(REQUIRED_FIELD_KEYS)))

        return fields

    except urllib.error.URLError as e:
        log_crit("Pipedrive: erreur reseau ({})".format(e))
        return None
    except Exception as e:
        log_crit("Pipedrive: erreur inattendue ({})".format(e))
        return None


# --- 2. Pipedrive enum IDs ---

def check_pipedrive_enums(fields):
    """Verify decideur_level enum options contain expected IDs."""
    if fields is None:
        log_skip("Pipedrive enum IDs: skip (fields non disponibles)")
        return

    try:
        decideur_key = "0b4c7e8cc10ced7badf65b34dac6254bd10a0179"
        decideur_field = None

        for f in fields:
            if f.get("key") == decideur_key:
                decideur_field = f
                break

        if decideur_field is None:
            log_crit("Pipedrive enum IDs: champ decideur_level introuvable dans la reponse")
            return

        options = decideur_field.get("options", [])
        option_ids = {opt.get("id") for opt in options}

        missing_enums = []
        for enum_id, label in REQUIRED_ENUM_IDS.items():
            if enum_id not in option_ids:
                missing_enums.append("{} (ID {})".format(label, enum_id))

        if missing_enums:
            log_crit("Pipedrive enum IDs: decideur_level mapping change. Manquants: {}".format(
                ", ".join(missing_enums)
            ))
        else:
            log_pass("Pipedrive enum IDs: decideur_level mapping OK")

    except Exception as e:
        log_crit("Pipedrive enum IDs: erreur inattendue ({})".format(e))


# --- 3. Google Drive access ---

def check_google_drive():
    """Test Google Drive credentials and basic listing."""
    try:
        if not os.path.isfile(GOOGLE_CREDS_PATH):
            log_warn("Google Drive: fichier credentials introuvable ({})".format(GOOGLE_CREDS_PATH))
            return

        # Try importing google libs
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
        except ImportError:
            log_warn("Google Drive: libs google-auth / google-api-python-client non installees")
            return

        SCOPES = ["https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_file(
            GOOGLE_CREDS_PATH, scopes=SCOPES
        )
        service = build("drive", "v3", credentials=creds)

        resp = service.files().list(
            pageSize=10,
            fields="files(id, name)",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
        ).execute()

        files = resp.get("files", [])

        if len(files) == 0:
            log_warn("Google Drive: credentials present mais listing retourne 0 fichiers (verifier permissions)")
        else:
            log_pass("Google Drive: credentials OK, {} fichier(s) accessible(s)".format(len(files)))

    except Exception as e:
        log_warn("Google Drive: erreur d'acces ({})".format(e))


# --- 4. Cache check ---

def check_cache():
    """Verify .cache/ is writable, count deals, flag stale files."""
    try:
        # Check writable
        if not CACHE_DIR.exists():
            try:
                CACHE_DIR.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                log_warn("Cache: impossible de creer .cache/ ({})".format(e))
                return

        # Test write (always, even after mkdir)
        test_file = CACHE_DIR / ".preflight_test"
        try:
            test_file.write_text("ok")
            test_file.unlink()
        except OSError as e:
            log_warn("Cache: .cache/ existe mais non accessible en ecriture ({})".format(e))
            return

        # Count deal folders
        deals_dir = CACHE_DIR / "deals"
        deal_count = 0
        stale_count = 0
        now = datetime.now()
        stale_cutoff = now - timedelta(days=STALE_THRESHOLD_DAYS)

        if deals_dir.exists():
            deal_folders = [d for d in deals_dir.iterdir() if d.is_dir()]
            deal_count = len(deal_folders)

            # Check for stale files
            for deal_folder in deal_folders:
                for cached_file in deal_folder.rglob("*"):
                    if cached_file.is_file():
                        mtime = datetime.fromtimestamp(cached_file.stat().st_mtime)
                        if mtime < stale_cutoff:
                            stale_count += 1

        parts = ["accessible en ecriture"]
        parts.append("{} deal(s) en cache".format(deal_count))
        if stale_count > 0:
            parts.append("{} fichier(s) obsolete(s) (>{}j)".format(stale_count, STALE_THRESHOLD_DAYS))

        log_pass("Cache: {}".format(", ".join(parts)))

    except Exception as e:
        log_warn("Cache: erreur inattendue ({})".format(e))


# --- Main ---

def main():
    print("\n=== SLASHR Preflight Check ===\n")

    # 1. Pipedrive field keys
    fields = check_pipedrive_fields()

    # 2. Pipedrive enum IDs
    check_pipedrive_enums(fields)

    # 3. Google Drive
    check_google_drive()

    # 4. Cache
    check_cache()

    # Output
    for r in results:
        print(r)

    print()
    if criticals == 0 and warnings == 0:
        print("Result: READY (0 critical, 0 warning)")
    elif criticals == 0:
        print("Result: DEGRADED (0 critical, {} warning{})".format(
            warnings, "s" if warnings != 1 else ""
        ))
    else:
        print("Result: NOT READY ({} critical{}, {} warning{})".format(
            criticals, "s" if criticals != 1 else "",
            warnings, "s" if warnings != 1 else ""
        ))

    # Exit: 0 = ready, 1 = criticals, 2 = warnings only
    if criticals > 0:
        sys.exit(1)
    elif warnings > 0:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
