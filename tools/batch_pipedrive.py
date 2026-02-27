#!/usr/bin/env python3
"""
SLASHR Batch Pipedrive — Parallel API collector with cache

Collecte toutes les donnees Pipedrive d'un deal en parallele :
- Deal, Person, Organization, Notes, Activities
- Email threads (inbox + sent, 6 pages each) filtrees par deal_id
- Messages des threads matches

Usage:
    python3 tools/batch_pipedrive.py --deal-id 560

Output (stdout = JSON summary, stderr = logs):
    {
        "deal_id": "560",
        "total": 18, "cached": 12, "fetched": 5, "failed": 1,
        "email_threads_matched": 3,
        "email_messages_fetched": 15,
        "results": { ... }
    }

Exit codes:
    0 = all OK
    1 = usage error / credentials missing
    2 = partial (deal OK but some secondary sources failed)
    3 = fatal (deal fetch failed)

Dependencies: stdlib only (Python 3.9+)
"""

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_WORKERS = 5
TIMEOUT_PER_REQUEST = 20  # seconds
MAX_EMAIL_PAGES = 6
EMAIL_PAGE_SIZE = 50
MAX_MESSAGES_PER_THREAD = 10
MAX_BODY_DOWNLOADS = 3
PIPEDRIVE_BASE = "https://api.pipedrive.com/v1"

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
CACHE_FRESHNESS_HOURS = 24

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
# APIError
# ---------------------------------------------------------------------------


class APIError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


class Credentials:
    def __init__(self, token):
        self.token = token

    @classmethod
    def load(cls):
        token_path = os.path.expanduser("~/.pipedrive_token")
        try:
            with open(token_path, "r") as f:
                token = f.read().strip()
        except FileNotFoundError:
            raise APIError("Token manquant: ~/.pipedrive_token")
        if not token:
            raise APIError("Token vide: ~/.pipedrive_token")
        return cls(token)


# ---------------------------------------------------------------------------
# CacheManager
# ---------------------------------------------------------------------------


class CacheManager:
    def __init__(self, deal_id):
        self.base_dir = CACHE_DIR / "deals" / str(deal_id) / "pipedrive"

    def check(self, cache_path):
        """Returns: ("fresh"|"stale"|"expired"|"miss", full_path)"""
        full_path = self.base_dir / cache_path
        if not full_path.exists():
            return "miss", full_path

        try:
            content = full_path.read_text(encoding="utf-8")
            if not content.strip():
                return "miss", full_path
            json.loads(content)
        except (json.JSONDecodeError, ValueError):
            log_warn("Cache non-parseable: {}".format(cache_path))
            return "miss", full_path

        age_hours = (time.time() - full_path.stat().st_mtime) / 3600
        if age_hours < CACHE_FRESHNESS_HOURS:
            return "fresh", full_path
        elif age_hours < 24 * 7:
            log_warn("Cache stale ({:.0f}h) pour {}".format(age_hours, cache_path))
            return "stale", full_path
        else:
            return "expired", full_path

    def read(self, cache_path):
        """Read and parse a cached file."""
        full_path = self.base_dir / cache_path
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def write(self, cache_path, data):
        full_path = self.base_dir / cache_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(full_path)


# ---------------------------------------------------------------------------
# PipedriveClient
# ---------------------------------------------------------------------------


class PipedriveClient:
    def __init__(self, credentials):
        self.token = credentials.token

    def get(self, endpoint, params=None):
        """Execute a GET request. Returns parsed JSON data."""
        params = params or {}
        params["api_token"] = self.token
        url = "{}/{}?{}".format(PIPEDRIVE_BASE, endpoint, urlencode(params))

        try:
            req = urllib_request.Request(url, headers={
                "Accept": "application/json",
                "User-Agent": "SLASHR-Bot/1.0",
            })
            resp = urllib_request.urlopen(req, timeout=TIMEOUT_PER_REQUEST)
            raw = resp.read()
            data = json.loads(raw.decode("utf-8"))

            if not data.get("success"):
                error_msg = data.get("error", "Unknown error")
                raise APIError("Pipedrive: {}".format(error_msg))

            return data

        except HTTPError as e:
            raise APIError("HTTP {} {}".format(e.code, e.reason), status_code=e.code)
        except (URLError, OSError, TimeoutError) as e:
            raise APIError("Network: {}".format(e))


# ---------------------------------------------------------------------------
# BatchOrchestrator
# ---------------------------------------------------------------------------


class BatchOrchestrator:
    def __init__(self, deal_id, credentials):
        self.deal_id = deal_id
        self.cache = CacheManager(deal_id)
        self.client = PipedriveClient(credentials)
        self.results = {}
        self.stats = {"cached": 0, "fetched": 0, "failed": 0}

    def run(self):
        """Main pipeline: deal (blocking) → parallel fetch → email filter → messages."""

        # Phase 1: Fetch deal (blocking, needed for person_id, org_id)
        deal_data = self._fetch_one("deal.json", "deals/{}".format(self.deal_id))
        if not deal_data:
            log_error("Deal {} inaccessible, arret".format(self.deal_id))
            return self._build_summary(fatal=True)

        deal = deal_data.get("data", {})
        person_id = self._extract_id(deal, "person_id")
        org_id = self._extract_id(deal, "org_id")

        # Phase 2: Parallel fetch of everything else
        tasks = []

        if person_id:
            tasks.append(("person.json", "persons/{}".format(person_id), {}))
        else:
            log_warn("person_id null, skip person fetch")

        if org_id:
            tasks.append(("org.json", "organizations/{}".format(org_id), {}))
        else:
            log_warn("org_id null, skip org fetch")

        tasks.append(("notes.json", "deals/{}/notes".format(self.deal_id), {}))
        tasks.append(("activities.json", "deals/{}/activities".format(self.deal_id), {}))

        # Email threads: 6 pages inbox + 6 pages sent (12 parallel requests)
        for page in range(MAX_EMAIL_PAGES):
            start = page * EMAIL_PAGE_SIZE
            tasks.append((
                "emails_threads_inbox_page{}.json".format(page),
                "mailbox/mailThreads",
                {"folder": "inbox", "limit": EMAIL_PAGE_SIZE, "start": start},
            ))
            tasks.append((
                "emails_threads_sent_page{}.json".format(page),
                "mailbox/mailThreads",
                {"folder": "sent", "limit": EMAIL_PAGE_SIZE, "start": start},
            ))

        log_info("Phase 2: {} requetes en parallele (person, org, notes, activities, 12 pages emails)".format(
            len(tasks)))
        self._fetch_parallel(tasks)

        # Phase 3: Filter email threads by deal_id
        matched_thread_ids = self._filter_email_threads()
        log_info("Email threads matches deal {}: {}".format(
            self.deal_id, len(matched_thread_ids)))

        # Phase 4: Fetch messages for matched threads (parallel)
        messages_fetched = 0
        if matched_thread_ids:
            msg_tasks = []
            for thread_id in matched_thread_ids:
                msg_tasks.append((
                    "emails_messages_thread_{}.json".format(thread_id),
                    "mailbox/mailThreads/{}/mailMessages".format(thread_id),
                    {"limit": MAX_MESSAGES_PER_THREAD},
                ))

            log_info("Phase 4: {} threads → fetch messages".format(len(msg_tasks)))
            self._fetch_parallel(msg_tasks)
            messages_fetched = sum(
                1 for k in self.results
                if k.startswith("emails_messages_") and self.results[k]["status"] in ("ok", "cached")
            )

        return self._build_summary(
            email_threads_matched=len(matched_thread_ids),
            email_messages_fetched=messages_fetched,
        )

    def _extract_id(self, deal, field):
        """Extract an ID from Pipedrive deal data (handles both int and dict formats)."""
        val = deal.get(field)
        if isinstance(val, dict):
            return val.get("value")
        if isinstance(val, int) and val > 0:
            return val
        return None

    def _fetch_one(self, cache_path, endpoint, params=None):
        """Fetch a single endpoint with cache check. Returns parsed data or None."""
        status, full_path = self.cache.check(cache_path)

        if status in ("fresh", "stale"):
            self.stats["cached"] += 1
            log_info("Cache {}: {}".format(status, cache_path))
            self.results[cache_path] = {
                "status": "cached",
                "cache_path": str(full_path),
                "cache_age": status,
            }
            return self.cache.read(cache_path)

        try:
            data = self.client.get(endpoint, params)
            written = self.cache.write(cache_path, data)
            self.stats["fetched"] += 1
            self.results[cache_path] = {
                "status": "ok",
                "cache_path": written,
            }
            log_info("Fetched: {}".format(cache_path))
            return data

        except APIError as e:
            self.stats["failed"] += 1
            self.results[cache_path] = {
                "status": "error",
                "error": str(e),
            }
            log_error("{}: {}".format(cache_path, e))
            return None

    def _fetch_parallel(self, tasks):
        """Fetch multiple endpoints in parallel."""
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_task = {
                executor.submit(self._fetch_one, cp, ep, pa): cp
                for cp, ep, pa in tasks
            }
            for future in as_completed(future_to_task):
                cp = future_to_task[future]
                try:
                    future.result()
                except Exception as e:
                    log_error("Unexpected {}: {}".format(cp, e))

    def _filter_email_threads(self):
        """Scan cached email pages, return thread IDs matching this deal_id."""
        matched = set()
        deal_id_int = int(self.deal_id)

        for cache_path, result in self.results.items():
            if not cache_path.startswith("emails_threads_"):
                continue
            if result["status"] not in ("ok", "cached"):
                continue

            data = self.cache.read(cache_path)
            if not data:
                continue

            threads = data.get("data") or []
            for thread in threads:
                if isinstance(thread, dict) and thread.get("deal_id") == deal_id_int:
                    tid = thread.get("id")
                    if tid:
                        matched.add(tid)

        return sorted(matched)

    def _build_summary(self, fatal=False, email_threads_matched=0, email_messages_fetched=0):
        total = self.stats["cached"] + self.stats["fetched"] + self.stats["failed"]
        return {
            "deal_id": self.deal_id,
            "total": total,
            "cached": self.stats["cached"],
            "fetched": self.stats["fetched"],
            "failed": self.stats["failed"],
            "email_threads_matched": email_threads_matched,
            "email_messages_fetched": email_messages_fetched,
            "fatal": fatal,
            "results": self.results,
        }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    deal_id = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--deal-id" and i + 1 < len(sys.argv):
            deal_id = sys.argv[i + 1]
            i += 2
        else:
            print("Argument inconnu: {}".format(sys.argv[i]), file=sys.stderr)
            i += 1

    if not deal_id:
        print("Usage: python3 tools/batch_pipedrive.py --deal-id <ID>", file=sys.stderr)
        sys.exit(1)

    try:
        credentials = Credentials.load()
    except APIError as e:
        log_error(str(e))
        sys.exit(1)

    log_info("Batch Pipedrive — deal {}".format(deal_id))

    try:
        orchestrator = BatchOrchestrator(deal_id, credentials)
        summary = orchestrator.run()
    except Exception as e:
        log_error("Fatal: {}".format(e))
        sys.exit(3)

    # Output JSON to stdout
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # Log summary
    log_info("Done: {cached} cached, {fetched} fetched, {failed} failed, "
             "{email_threads_matched} threads, {email_messages_fetched} messages".format(**summary))

    # Exit code
    if summary.get("fatal"):
        sys.exit(3)
    elif summary["failed"] > 0:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
