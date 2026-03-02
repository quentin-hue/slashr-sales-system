#!/usr/bin/env python3
"""
SLASHR Batch Google Drive — Parallel file collector with cache

Liste recursivement un dossier Drive et telecharge les fichiers en parallele.

Usage:
    python3 tools/batch_drive.py --deal-id 560 --folder-id 1ABcdEfGhIjKlMnOpQrStUvWxYz
    python3 tools/batch_drive.py --deal-id 560 --folder-url "https://drive.google.com/drive/folders/1ABC..."

Output (stdout = JSON summary, stderr = logs):
    {
        "deal_id": "560",
        "total_files": 12, "cached": 8, "downloaded": 3, "skipped": 1, "failed": 0,
        "manifest_path": "...",
        "results": { ... }
    }

Exit codes:
    0 = all OK
    1 = usage error / credentials missing
    2 = partial (some files failed)
    3 = fatal (folder inaccessible)

Dependencies: google-auth (installed), stdlib
"""

import json
import os
import re
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse, parse_qs

# Suppress Python 3.9 EOL warnings from google-auth
warnings.filterwarnings("ignore", category=FutureWarning)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_WORKERS = 3
TIMEOUT_PER_REQUEST = 20  # seconds
MAX_FILES = 25
MAX_RECURSION = 3
MAX_FILE_SIZE = 100_000  # characters
DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"
DOCS_API_BASE = "https://docs.googleapis.com/v1"

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
CACHE_FRESHNESS_HOURS = 24

# System output prefixes to exclude
SYSTEM_PREFIXES = ("DEAL-", "DECK-", "PROPOSAL-", "INTERNAL-")

# Export MIME types
EXPORT_MIMES = {
    "application/vnd.google-apps.document": ("text/plain", ".txt"),
    "application/vnd.google-apps.spreadsheet": ("text/csv", ".csv"),
    "application/vnd.google-apps.presentation": ("text/plain", ".txt"),
}

# Downloadable MIME types (direct download)
DOWNLOADABLE_MIMES = {
    "application/pdf",
    "text/plain",
    "text/csv",
    "text/markdown",
    "text/html",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

# ---------------------------------------------------------------------------
# Logging (stderr only)
# ---------------------------------------------------------------------------


def log_info(msg):
    print("[INFO] {}".format(msg), file=sys.stderr)


def log_warn(msg):
    print("[WARN] {}".format(msg), file=sys.stderr)


def log_error(msg):
    print("[ERROR] {}".format(msg), file=sys.stderr)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class DriveError(Exception):
    pass


# ---------------------------------------------------------------------------
# Credentials (Google Service Account)
# ---------------------------------------------------------------------------


class Credentials:
    def __init__(self):
        self._creds = None

    def load(self):
        creds_path = os.path.expanduser("~/.google_service_account.json")
        if not os.path.exists(creds_path):
            raise DriveError("Service account manquant: ~/.google_service_account.json")

        try:
            from google.oauth2 import service_account
            self._creds = service_account.Credentials.from_service_account_file(
                creds_path,
                scopes=["https://www.googleapis.com/auth/drive"],
            )
        except Exception as e:
            raise DriveError("Erreur chargement credentials: {}".format(e))

        return self

    def get_token(self):
        """Get a valid access token, refreshing if needed."""
        if not self._creds.valid:
            from google.auth.transport.requests import Request
            self._creds.refresh(Request())
        return self._creds.token


# ---------------------------------------------------------------------------
# CacheManager
# ---------------------------------------------------------------------------


class CacheManager:
    def __init__(self, deal_id):
        self.base_dir = CACHE_DIR / "deals" / str(deal_id) / "drive"
        self.files_dir = self.base_dir / "files"

    def check(self, filename):
        """Check cache for a file. Returns ("fresh"|"stale"|"miss", full_path)."""
        full_path = self.files_dir / filename
        if not full_path.exists():
            return "miss", full_path

        try:
            size = full_path.stat().st_size
            if size == 0:
                return "miss", full_path
        except OSError:
            return "miss", full_path

        age_hours = (time.time() - full_path.stat().st_mtime) / 3600
        if age_hours < CACHE_FRESHNESS_HOURS:
            return "fresh", full_path
        elif age_hours < 24 * 7:
            return "stale", full_path
        else:
            return "miss", full_path

    def write_file(self, filename, content):
        """Write file content to cache."""
        self.files_dir.mkdir(parents=True, exist_ok=True)
        full_path = self.files_dir / filename
        if isinstance(content, bytes):
            with open(full_path, "wb") as f:
                f.write(content)
        else:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        return str(full_path)

    def write_manifest(self, manifest):
        """Write the file manifest."""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        path = self.base_dir / "manifest.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        return str(path)


# ---------------------------------------------------------------------------
# DriveClient
# ---------------------------------------------------------------------------


class DriveClient:
    def __init__(self, credentials):
        self.credentials = credentials

    def _request(self, url, params=None):
        """Make an authenticated GET request."""
        if params:
            url = "{}?{}".format(url, urlencode(params))

        token = self.credentials.get_token()
        req = urllib_request.Request(url, headers={
            "Authorization": "Bearer {}".format(token),
            "Accept": "application/json",
            "User-Agent": "SLASHR-Bot/1.0",
        })

        try:
            resp = urllib_request.urlopen(req, timeout=TIMEOUT_PER_REQUEST)
            return resp.read()
        except HTTPError as e:
            raise DriveError("HTTP {} {}".format(e.code, e.reason))
        except (URLError, OSError, TimeoutError) as e:
            raise DriveError("Network: {}".format(e))

    def list_files(self, folder_id, page_token=None):
        """List files in a folder."""
        params = {
            "q": "'{}' in parents and trashed = false".format(folder_id),
            "fields": "nextPageToken,files(id,name,mimeType,size,modifiedTime)",
            "pageSize": 100,
            "includeItemsFromAllDrives": "true",
            "supportsAllDrives": "true",
        }
        if page_token:
            params["pageToken"] = page_token

        raw = self._request("{}/files".format(DRIVE_API_BASE), params)
        return json.loads(raw.decode("utf-8"))

    def export_file(self, file_id, export_mime):
        """Export a Google Workspace file."""
        params = {
            "mimeType": export_mime,
            "supportsAllDrives": "true",
        }
        raw = self._request(
            "{}/files/{}/export".format(DRIVE_API_BASE, file_id), params)
        return raw

    def download_file(self, file_id):
        """Download a binary file."""
        params = {
            "alt": "media",
            "supportsAllDrives": "true",
        }
        raw = self._request(
            "{}/files/{}".format(DRIVE_API_BASE, file_id), params)
        return raw

    def get_document(self, document_id):
        """Get a Google Doc with all tabs via Docs API."""
        params = {"includeTabsContent": "true"}
        raw = self._request(
            "{}/documents/{}".format(DOCS_API_BASE, document_id), params
        )
        return json.loads(raw.decode("utf-8"))


# ---------------------------------------------------------------------------
# Docs API text extraction
# ---------------------------------------------------------------------------


def extract_text_from_content(content_elements):
    """Extract plain text from Docs API content elements (recursive for tables)."""
    text = ""
    for element in content_elements:
        if "paragraph" in element:
            for pe in element["paragraph"].get("elements", []):
                text += pe.get("textRun", {}).get("content", "")
        elif "table" in element:
            for row in element["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    text += extract_text_from_content(cell.get("content", []))
    return text


def extract_text_from_doc(doc_data):
    """Extract text from all tabs of a Google Doc."""
    tabs = doc_data.get("tabs", [])
    if not tabs:
        return ""
    if len(tabs) == 1:
        body = tabs[0].get("documentTab", {}).get("body", {})
        return extract_text_from_content(body.get("content", []))
    parts = []
    for tab in tabs:
        title = tab.get("tabProperties", {}).get("title", "Sans titre")
        body = tab.get("documentTab", {}).get("body", {})
        text = extract_text_from_content(body.get("content", []))
        parts.append("=== ONGLET: {} ===\n{}".format(title, text))
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# BatchOrchestrator
# ---------------------------------------------------------------------------


class BatchOrchestrator:
    def __init__(self, deal_id, folder_id, credentials):
        self.deal_id = deal_id
        self.folder_id = folder_id
        self.cache = CacheManager(deal_id)
        self.client = DriveClient(credentials)
        self.results = {}
        self.stats = {"cached": 0, "downloaded": 0, "skipped": 0, "failed": 0}

    def run(self):
        """List files recursively, then download in parallel."""

        # Phase 1: Recursive listing
        log_info("Listing dossier {} (recursion max {})".format(
            self.folder_id, MAX_RECURSION))

        all_files = self._list_recursive(self.folder_id, depth=0)
        log_info("{} fichiers trouves".format(len(all_files)))

        # Filter system outputs
        filtered = []
        for f in all_files:
            name = f.get("name", "")
            if any(name.startswith(prefix) for prefix in SYSTEM_PREFIXES):
                log_info("Exclu (systeme): {}".format(name))
                continue
            filtered.append(f)

        # Limit to MAX_FILES (most recent first)
        if len(filtered) > MAX_FILES:
            log_warn("Trop de fichiers ({}), selection des {} plus recents".format(
                len(filtered), MAX_FILES))
            filtered.sort(
                key=lambda f: f.get("modifiedTime", ""),
                reverse=True,
            )
            filtered = filtered[:MAX_FILES]

        # Write manifest
        manifest = {
            "folder_id": self.folder_id,
            "deal_id": self.deal_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "total_found": len(all_files),
            "total_filtered": len(filtered),
            "files": [
                {
                    "id": f["id"],
                    "name": f["name"],
                    "mimeType": f.get("mimeType", ""),
                    "size": f.get("size"),
                }
                for f in filtered
            ],
        }
        manifest_path = self.cache.write_manifest(manifest)
        log_info("Manifest: {} fichiers".format(len(filtered)))

        # Phase 2: Parallel download
        if filtered:
            log_info("Phase 2: download {} fichiers (max {} workers)".format(
                len(filtered), MAX_WORKERS))
            self._download_parallel(filtered)

        return self._build_summary(
            total_files=len(filtered),
            manifest_path=manifest_path,
        )

    def _list_recursive(self, folder_id, depth):
        """List files in folder, recurse into subfolders."""
        all_files = []
        page_token = None

        while True:
            try:
                resp = self.client.list_files(folder_id, page_token)
            except DriveError as e:
                log_error("Listing {}: {}".format(folder_id, e))
                break

            files = resp.get("files", [])
            for f in files:
                mime = f.get("mimeType", "")
                if mime == "application/vnd.google-apps.folder":
                    if depth < MAX_RECURSION:
                        sub_files = self._list_recursive(f["id"], depth + 1)
                        all_files.extend(sub_files)
                    else:
                        log_warn("Recursion max atteinte, skip sous-dossier: {}".format(
                            f.get("name", "")))
                else:
                    all_files.append(f)

            page_token = resp.get("nextPageToken")
            if not page_token:
                break

        return all_files

    def _download_parallel(self, files):
        """Download files in parallel."""
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_file = {
                executor.submit(self._download_one, f): f
                for f in files
            }
            for future in as_completed(future_to_file):
                f = future_to_file[future]
                try:
                    future.result()
                except Exception as e:
                    fid = f.get("id", "?")
                    log_error("Unexpected {}: {}".format(fid, e))

    def _download_one(self, file_info):
        """Download/export a single file with cache check."""
        file_id = file_info["id"]
        name = file_info.get("name", "unknown")
        mime = file_info.get("mimeType", "")

        # Determine cache filename and download method
        if mime in EXPORT_MIMES:
            export_mime, ext = EXPORT_MIMES[mime]
            cache_name = "{}.txt".format(file_id)
            method = "export"
        elif mime in DOWNLOADABLE_MIMES:
            # Keep original extension
            ext = Path(name).suffix or ".bin"
            cache_name = "{}{}".format(file_id, ext)
            method = "download"
            # Also create a .txt version for text extraction
        else:
            log_warn("Format non supporte: {} ({})".format(name, mime))
            self.stats["skipped"] += 1
            self.results[file_id] = {
                "status": "skipped",
                "name": name,
                "reason": "format non supporte: {}".format(mime),
            }
            return

        # Cache check (on .txt version for exports)
        txt_cache = "{}.txt".format(file_id)
        status, full_path = self.cache.check(txt_cache)
        if status in ("fresh", "stale"):
            self.stats["cached"] += 1
            log_info("Cache {}: {} ({})".format(status, name, txt_cache))
            self.results[file_id] = {
                "status": "cached",
                "name": name,
                "cache_path": str(full_path),
                "cache_age": status,
            }
            return

        # Download/export
        try:
            if method == "export":
                if mime == "application/vnd.google-apps.document":
                    # Google Docs : Docs API pour multi-onglets, fallback Drive export
                    try:
                        doc_data = self.client.get_document(file_id)
                        content = extract_text_from_doc(doc_data)
                        tab_count = len(doc_data.get("tabs", []))
                        if tab_count > 1:
                            log_info("Multi-onglet ({} tabs): {}".format(tab_count, name))
                    except DriveError:
                        log_warn("Docs API fallback export: {}".format(name))
                        raw = self.client.export_file(file_id, export_mime)
                        content = raw.decode("utf-8", errors="replace")
                else:
                    raw = self.client.export_file(file_id, export_mime)
                    content = raw.decode("utf-8", errors="replace")

                # Size check
                if len(content) > MAX_FILE_SIZE:
                    log_warn("Fichier trop volumineux: {} ({} chars)".format(
                        name, len(content)))
                    content = content[:MAX_FILE_SIZE]

                written = self.cache.write_file(txt_cache, content)

            elif method == "download":
                raw = self.client.download_file(file_id)

                # Save original binary
                written_bin = self.cache.write_file(cache_name, raw)

                # Try to create .txt version
                content = raw.decode("utf-8", errors="replace")
                if len(content) > MAX_FILE_SIZE:
                    content = content[:MAX_FILE_SIZE]
                written = self.cache.write_file(txt_cache, content)

            self.stats["downloaded"] += 1
            self.results[file_id] = {
                "status": "ok",
                "name": name,
                "cache_path": written,
                "size": len(content) if isinstance(content, str) else len(raw),
            }
            log_info("Downloaded: {} ({})".format(name, file_id))

        except DriveError as e:
            self.stats["failed"] += 1
            self.results[file_id] = {
                "status": "error",
                "name": name,
                "error": str(e),
            }
            log_error("{} ({}): {}".format(name, file_id, e))

    def _build_summary(self, total_files=0, manifest_path=""):
        return {
            "deal_id": self.deal_id,
            "folder_id": self.folder_id,
            "total_files": total_files,
            "cached": self.stats["cached"],
            "downloaded": self.stats["downloaded"],
            "skipped": self.stats["skipped"],
            "failed": self.stats["failed"],
            "manifest_path": manifest_path,
            "results": self.results,
        }


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def extract_folder_id(url_or_id):
    """Extract folder ID from a Drive URL or return as-is."""
    if url_or_id.startswith("http"):
        parsed = urlparse(url_or_id)
        # https://drive.google.com/drive/folders/XXXXX
        parts = parsed.path.strip("/").split("/")
        if "folders" in parts:
            idx = parts.index("folders")
            if idx + 1 < len(parts):
                return parts[idx + 1]
        # Fallback: query param
        qs = parse_qs(parsed.query)
        if "id" in qs:
            return qs["id"][0]
        raise DriveError("Impossible d'extraire le folder ID de: {}".format(url_or_id))
    return url_or_id


def parse_args(argv):
    deal_id = None
    folder_id = None

    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--deal-id" and i + 1 < len(argv):
            deal_id = argv[i + 1]
            i += 2
        elif arg == "--folder-id" and i + 1 < len(argv):
            folder_id = argv[i + 1]
            i += 2
        elif arg == "--folder-url" and i + 1 < len(argv):
            folder_id = extract_folder_id(argv[i + 1])
            i += 2
        else:
            print("Argument inconnu: {}".format(arg), file=sys.stderr)
            i += 1

    if not deal_id or not folder_id:
        print("Usage: python3 tools/batch_drive.py --deal-id <ID> "
              "--folder-id <FOLDER_ID> | --folder-url <URL>", file=sys.stderr)
        sys.exit(1)

    return deal_id, folder_id


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    deal_id, folder_id = parse_args(sys.argv)

    try:
        credentials = Credentials().load()
    except DriveError as e:
        log_error(str(e))
        sys.exit(1)

    log_info("Batch Drive — deal {}, folder {}".format(deal_id, folder_id))

    try:
        orchestrator = BatchOrchestrator(deal_id, folder_id, credentials)
        summary = orchestrator.run()
    except Exception as e:
        log_error("Fatal: {}".format(e))
        sys.exit(3)

    # Output JSON to stdout
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # Log summary
    log_info("Done: {cached} cached, {downloaded} downloaded, "
             "{skipped} skipped, {failed} failed".format(**summary))

    # Exit code
    if summary["failed"] > 0 and summary["downloaded"] == 0 and summary["cached"] == 0:
        sys.exit(3)
    elif summary["failed"] > 0:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
