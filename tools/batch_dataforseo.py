#!/usr/bin/env python3
"""
SLASHR Batch DataForSEO — Parallel API caller with cache

Execute multiple DataForSEO requests in parallel (ThreadPoolExecutor, 5 workers)
with cache management and retry logic.

Usage:
    python3 tools/batch_dataforseo.py --deal-id 560 --requests-file /tmp/batch.json
    python3 tools/batch_dataforseo.py --deal-id 560 --requests '[...]'

Request format (JSON array):
    [
        {
            "id": "overview_prospect",
            "endpoint": "dataforseo_labs/google/domain_rank_overview/live",
            "body": [{"target": "example.com", "language_code": "fr", "location_code": 2250}],
            "cache_path": "domain_example.com/domain_rank_overview.json"
        },
        ...
    ]

Output (stdout = JSON only, stderr = logs):
    {
        "total": 4, "cached": 1, "fetched": 2, "failed": 1,
        "total_cost": 0.03,
        "results": {
            "overview_prospect": {"status": "cached", "cache_path": "..."},
            "ranked_kw": {"status": "ok", "cache_path": "...", "cost": 0.015},
            "intent": {"status": "error", "error": "timeout"}
        }
    }

Exit codes:
    0 = all OK (all cached or fetched)
    1 = usage error (bad args, missing credentials)
    2 = partial success (some requests failed)
    3 = fatal error (all requests failed or unexpected error)

Dependencies: stdlib only (Python 3.9+)
"""

import base64
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_WORKERS = 5
TIMEOUT_PER_REQUEST = 20  # seconds
MAX_RETRIES = 2
BACKOFF_SECONDS = [1, 3]  # backoff per retry
DATAFORSEO_BASE = "https://api.dataforseo.com/v3/"

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"

# Cache freshness thresholds (hours)
CACHE_FRESH = 24
CACHE_STALE = 24 * 7  # 7 days

# ---------------------------------------------------------------------------
# Logging (stderr only — stdout reserved for JSON output)
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
    def __init__(self, message, status_code=None, retryable=True):
        super().__init__(message)
        self.status_code = status_code
        self.retryable = retryable


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


class Credentials:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        token = base64.b64encode(
            "{}:{}".format(login, password).encode()
        ).decode()
        self.auth_header = "Basic {}".format(token)

    @classmethod
    def load(cls):
        login_path = os.path.expanduser("~/.dataforseo_login")
        password_path = os.path.expanduser("~/.dataforseo_password")

        try:
            with open(login_path, "r") as f:
                login = f.read().strip()
            with open(password_path, "r") as f:
                password = f.read().strip()
        except FileNotFoundError as e:
            raise APIError(
                "Credentials manquants: {}".format(e),
                retryable=False,
            )

        if not login or not password:
            raise APIError(
                "Credentials vides (~/.dataforseo_login ou ~/.dataforseo_password)",
                retryable=False,
            )

        return cls(login, password)


# ---------------------------------------------------------------------------
# CacheManager
# ---------------------------------------------------------------------------


class CacheManager:
    def __init__(self, deal_id):
        self.base_dir = CACHE_DIR / "deals" / str(deal_id) / "dataforseo"

    def check(self, cache_path):
        """Check cache status for a given path.

        Returns: ("fresh"|"stale"|"expired"|"miss", full_path)
        """
        full_path = self.base_dir / cache_path
        if not full_path.exists():
            return "miss", full_path

        # Validate: non-empty, parseable JSON, status_code 20000
        try:
            content = full_path.read_text(encoding="utf-8")
            if not content.strip():
                log_warn("Cache vide: {}".format(cache_path))
                return "miss", full_path

            data = json.loads(content)

            # Check for DataForSEO success indicator
            status_code = None
            if isinstance(data, dict):
                status_code = data.get("status_code")
                # Also check nested tasks
                tasks = data.get("tasks", [])
                if tasks and isinstance(tasks, list):
                    for task in tasks:
                        if isinstance(task, dict):
                            tc = task.get("status_code")
                            if tc and tc != 20000:
                                log_warn("Cache invalide (task status {}): {}".format(
                                    tc, cache_path))
                                return "miss", full_path

            if status_code is not None and status_code != 20000:
                log_warn("Cache invalide (status {}): {}".format(
                    status_code, cache_path))
                return "miss", full_path

        except (json.JSONDecodeError, ValueError):
            log_warn("Cache non-parseable: {}".format(cache_path))
            return "miss", full_path

        # Check age
        age_hours = (time.time() - full_path.stat().st_mtime) / 3600

        if age_hours < CACHE_FRESH:
            return "fresh", full_path
        elif age_hours < CACHE_STALE:
            log_warn("Cache stale ({:.0f}h) pour {}".format(
                age_hours, cache_path))
            return "stale", full_path
        else:
            log_info("Cache expire ({:.0f}h) pour {} — refetch".format(
                age_hours, cache_path))
            return "expired", full_path

    def write(self, cache_path, data):
        """Write API response to cache."""
        full_path = self.base_dir / cache_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return str(full_path)


# ---------------------------------------------------------------------------
# DataForSEOClient
# ---------------------------------------------------------------------------


class DataForSEOClient:
    def __init__(self, credentials):
        self.credentials = credentials

    def execute(self, endpoint, body):
        """Execute a single DataForSEO API call with retries.

        Returns: (response_dict, cost)
        Raises: APIError on failure after retries
        """
        url = DATAFORSEO_BASE + endpoint
        payload = json.dumps(body).encode("utf-8")

        last_error = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                req = urllib_request.Request(
                    url,
                    data=payload,
                    method="POST",
                    headers={
                        "Authorization": self.credentials.auth_header,
                        "Content-Type": "application/json",
                    },
                )

                resp = urllib_request.urlopen(req, timeout=TIMEOUT_PER_REQUEST)
                raw = resp.read()
                data = json.loads(raw.decode("utf-8"))

                # Check top-level status
                status_code = data.get("status_code", 0)
                if status_code != 20000:
                    msg = data.get("status_message", "Unknown error")
                    # 40x errors are not retryable
                    retryable = status_code >= 50000
                    raise APIError(
                        "{} (status {})".format(msg, status_code),
                        status_code=status_code,
                        retryable=retryable,
                    )

                # Extract cost
                cost = data.get("cost", 0) or 0

                return data, cost

            except APIError as e:
                last_error = e
                if not e.retryable or attempt >= MAX_RETRIES:
                    raise
                backoff = BACKOFF_SECONDS[min(attempt, len(BACKOFF_SECONDS) - 1)]
                log_warn("Retry {}/{} dans {}s pour {} — {}".format(
                    attempt + 1, MAX_RETRIES, backoff, endpoint, e))
                time.sleep(backoff)

            except HTTPError as e:
                last_error = APIError(
                    "HTTP {} {}".format(e.code, e.reason),
                    status_code=e.code,
                    retryable=e.code >= 500,
                )
                if e.code < 500 or attempt >= MAX_RETRIES:
                    raise last_error
                backoff = BACKOFF_SECONDS[min(attempt, len(BACKOFF_SECONDS) - 1)]
                log_warn("Retry {}/{} dans {}s pour {} — HTTP {}".format(
                    attempt + 1, MAX_RETRIES, backoff, endpoint, e.code))
                time.sleep(backoff)

            except (URLError, OSError, TimeoutError) as e:
                last_error = APIError(
                    "Network error: {}".format(e),
                    retryable=True,
                )
                if attempt >= MAX_RETRIES:
                    raise last_error
                backoff = BACKOFF_SECONDS[min(attempt, len(BACKOFF_SECONDS) - 1)]
                log_warn("Retry {}/{} dans {}s pour {} — {}".format(
                    attempt + 1, MAX_RETRIES, backoff, endpoint, e))
                time.sleep(backoff)

        raise last_error


# ---------------------------------------------------------------------------
# BatchOrchestrator
# ---------------------------------------------------------------------------


class BatchOrchestrator:
    def __init__(self, deal_id, requests, credentials):
        self.deal_id = deal_id
        self.requests = requests
        self.cache = CacheManager(deal_id)
        self.client = DataForSEOClient(credentials)

    def run(self):
        """Execute all requests: cache check → parallel fetch → write results."""
        results = {}
        to_fetch = []
        total_cost = 0.0

        # Phase 1: cache check
        for req in self.requests:
            req_id = req["id"]
            cache_path = req.get("cache_path")

            if not cache_path:
                to_fetch.append(req)
                continue

            status, full_path = self.cache.check(cache_path)

            if status in ("fresh", "stale"):
                results[req_id] = {
                    "status": "cached",
                    "cache_path": str(full_path),
                    "cache_age": status,
                }
                log_info("Cache {}: {} → {}".format(status, req_id, cache_path))
            else:
                # miss or expired → fetch
                to_fetch.append(req)

        cached_count = len(results)
        log_info("{} cached, {} to fetch".format(cached_count, len(to_fetch)))

        # Phase 2: parallel fetch
        if to_fetch:
            fetch_results = self._fetch_parallel(to_fetch)
            for req_id, result in fetch_results.items():
                results[req_id] = result
                if result.get("cost"):
                    total_cost += result["cost"]

        # Build summary
        fetched_count = sum(
            1 for r in results.values() if r["status"] == "ok"
        )
        failed_count = sum(
            1 for r in results.values() if r["status"] == "error"
        )

        summary = {
            "total": len(self.requests),
            "cached": cached_count,
            "fetched": fetched_count,
            "failed": failed_count,
            "total_cost": round(total_cost, 4),
            "results": results,
        }

        return summary

    def _fetch_parallel(self, requests):
        """Fetch requests in parallel with ThreadPoolExecutor."""
        results = {}

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_req = {
                executor.submit(self._fetch_one, req): req
                for req in requests
            }

            for future in as_completed(future_to_req):
                req = future_to_req[future]
                req_id = req["id"]

                try:
                    result = future.result()
                    results[req_id] = result
                except Exception as e:
                    log_error("{}: {}".format(req_id, e))
                    results[req_id] = {
                        "status": "error",
                        "error": str(e),
                    }

        return results

    def _fetch_one(self, req):
        """Fetch a single request, write to cache, return result."""
        req_id = req["id"]
        endpoint = req["endpoint"]
        body = req.get("body", [])
        cache_path = req.get("cache_path")

        log_info("Fetch: {} → {}".format(req_id, endpoint))

        try:
            data, cost = self.client.execute(endpoint, body)

            # Write to cache
            written_path = None
            if cache_path:
                written_path = self.cache.write(cache_path, data)

            log_info("OK: {} (cost: {})".format(req_id, cost))

            result = {
                "status": "ok",
                "cost": cost,
            }
            if written_path:
                result["cache_path"] = written_path

            return result

        except APIError as e:
            raise
        except Exception as e:
            raise APIError("Unexpected: {}".format(e), retryable=False)


# ---------------------------------------------------------------------------
# Argument parsing (stdlib only)
# ---------------------------------------------------------------------------


def parse_args(argv):
    """Parse CLI arguments. Returns (deal_id, requests_list)."""
    deal_id = None
    requests_raw = None
    requests_file = None

    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--deal-id" and i + 1 < len(argv):
            deal_id = argv[i + 1]
            i += 2
        elif arg == "--requests" and i + 1 < len(argv):
            requests_raw = argv[i + 1]
            i += 2
        elif arg == "--requests-file" and i + 1 < len(argv):
            requests_file = argv[i + 1]
            i += 2
        else:
            print("Argument inconnu: {}".format(arg), file=sys.stderr)
            i += 1

    if not deal_id:
        print("Usage: python3 tools/batch_dataforseo.py --deal-id <ID> "
              "--requests '<json>' | --requests-file <path>", file=sys.stderr)
        sys.exit(1)

    # Load requests
    if requests_file:
        try:
            with open(requests_file, "r", encoding="utf-8") as f:
                requests_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print("Erreur lecture --requests-file: {}".format(e), file=sys.stderr)
            sys.exit(1)
    elif requests_raw:
        try:
            requests_list = json.loads(requests_raw)
        except json.JSONDecodeError as e:
            print("Erreur parsing --requests: {}".format(e), file=sys.stderr)
            sys.exit(1)
    else:
        print("--requests ou --requests-file requis", file=sys.stderr)
        sys.exit(1)

    if not isinstance(requests_list, list) or not requests_list:
        print("Les requetes doivent etre un tableau JSON non-vide", file=sys.stderr)
        sys.exit(1)

    # Validate each request
    for i, req in enumerate(requests_list):
        if not isinstance(req, dict):
            print("Requete {} n'est pas un objet".format(i), file=sys.stderr)
            sys.exit(1)
        if "id" not in req or "endpoint" not in req:
            print("Requete {} manque 'id' ou 'endpoint'".format(i), file=sys.stderr)
            sys.exit(1)

    return deal_id, requests_list


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    deal_id, requests_list = parse_args(sys.argv)

    # Load credentials
    try:
        credentials = Credentials.load()
    except APIError as e:
        log_error(str(e))
        sys.exit(1)

    log_info("Batch DataForSEO — deal {} — {} requetes".format(
        deal_id, len(requests_list)))

    # Run batch
    try:
        orchestrator = BatchOrchestrator(deal_id, requests_list, credentials)
        summary = orchestrator.run()
    except Exception as e:
        log_error("Fatal: {}".format(e))
        sys.exit(3)

    # Output JSON to stdout
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # Log summary to stderr
    log_info("Done: {cached} cached, {fetched} fetched, {failed} failed, "
             "cost: {total_cost}".format(**summary))

    # Exit code
    if summary["failed"] == 0:
        sys.exit(0)
    elif summary["fetched"] > 0 or summary["cached"] > 0:
        sys.exit(2)
    else:
        sys.exit(3)


if __name__ == "__main__":
    main()
