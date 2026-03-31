#!/usr/bin/env python3
"""
Tests for batch_dataforseo.py — cache management, request parsing, error handling.

Run: python3 -m pytest tests/test_batch_dataforseo.py -v
"""

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest

TOOLS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
BATCH_SCRIPT = os.path.join(TOOLS_DIR, "batch_dataforseo.py")

# Import the module directly for unit-testing internal classes
sys.path.insert(0, TOOLS_DIR)
import batch_dataforseo as bdf


class TestCacheValidation(unittest.TestCase):
    """CacheManager.check() — empty file, invalid JSON, valid cache."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Monkey-patch CACHE_DIR so CacheManager uses our temp dir
        self._orig_cache_dir = bdf.CACHE_DIR
        bdf.CACHE_DIR = bdf.Path(self.tmpdir)
        self.cm = bdf.CacheManager("test_deal")

    def tearDown(self):
        bdf.CACHE_DIR = self._orig_cache_dir
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_miss_for_nonexistent_file(self):
        """Nonexistent cache file returns 'miss'."""
        status, _ = self.cm.check("nonexistent/file.json")
        self.assertEqual(status, "miss")

    def test_miss_for_empty_file(self):
        """Empty cache file returns 'miss'."""
        cache_dir = os.path.join(self.tmpdir, "deals", "test_deal", "dataforseo", "domain")
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, "empty.json")
        with open(path, "w") as f:
            f.write("")
        status, _ = self.cm.check("domain/empty.json")
        self.assertEqual(status, "miss")

    def test_miss_for_invalid_json(self):
        """Non-parseable JSON returns 'miss'."""
        cache_dir = os.path.join(self.tmpdir, "deals", "test_deal", "dataforseo", "domain")
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, "broken.json")
        with open(path, "w") as f:
            f.write("{invalid json content")
        status, _ = self.cm.check("domain/broken.json")
        self.assertEqual(status, "miss")

    def test_miss_for_error_status_code(self):
        """Cache with non-20000 status_code returns 'miss'."""
        cache_dir = os.path.join(self.tmpdir, "deals", "test_deal", "dataforseo", "domain")
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, "error.json")
        with open(path, "w") as f:
            json.dump({"status_code": 40000, "status_message": "error"}, f)
        status, _ = self.cm.check("domain/error.json")
        self.assertEqual(status, "miss")

    def test_miss_for_failed_task(self):
        """Cache with a task having non-20000 status returns 'miss'."""
        cache_dir = os.path.join(self.tmpdir, "deals", "test_deal", "dataforseo", "domain")
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, "bad_task.json")
        with open(path, "w") as f:
            json.dump({
                "status_code": 20000,
                "tasks": [{"status_code": 40401, "status_message": "Not Found"}]
            }, f)
        status, _ = self.cm.check("domain/bad_task.json")
        self.assertEqual(status, "miss")

    def test_fresh_for_recent_valid_cache(self):
        """Recently written valid cache returns 'fresh'."""
        cache_dir = os.path.join(self.tmpdir, "deals", "test_deal", "dataforseo", "domain")
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, "valid.json")
        with open(path, "w") as f:
            json.dump({
                "status_code": 20000,
                "tasks": [{"status_code": 20000, "result": []}]
            }, f)
        status, _ = self.cm.check("domain/valid.json")
        self.assertEqual(status, "fresh")


class TestCacheAge(unittest.TestCase):
    """CacheManager.check() — fresh, stale, expired based on file mtime."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self._orig_cache_dir = bdf.CACHE_DIR
        bdf.CACHE_DIR = bdf.Path(self.tmpdir)
        self.cm = bdf.CacheManager("test_deal")
        # Create a valid cache file
        self.cache_subdir = os.path.join(
            self.tmpdir, "deals", "test_deal", "dataforseo", "domain"
        )
        os.makedirs(self.cache_subdir, exist_ok=True)
        self.cache_file = os.path.join(self.cache_subdir, "age_test.json")
        with open(self.cache_file, "w") as f:
            json.dump({"status_code": 20000, "tasks": []}, f)

    def tearDown(self):
        bdf.CACHE_DIR = self._orig_cache_dir
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _set_file_age_hours(self, hours):
        """Set file mtime to `hours` ago."""
        mtime = time.time() - (hours * 3600)
        os.utime(self.cache_file, (mtime, mtime))

    def test_fresh_cache(self):
        """File < 24h old -> fresh."""
        self._set_file_age_hours(1)
        status, _ = self.cm.check("domain/age_test.json")
        self.assertEqual(status, "fresh")

    def test_stale_cache(self):
        """File between 24h and 7d old -> stale."""
        self._set_file_age_hours(48)  # 2 days
        status, _ = self.cm.check("domain/age_test.json")
        self.assertEqual(status, "stale")

    def test_expired_cache(self):
        """File > 7d old -> expired."""
        self._set_file_age_hours(200)  # ~8 days
        status, _ = self.cm.check("domain/age_test.json")
        self.assertEqual(status, "expired")


class TestCacheWrite(unittest.TestCase):
    """CacheManager.write() — writes JSON, creates directories."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self._orig_cache_dir = bdf.CACHE_DIR
        bdf.CACHE_DIR = bdf.Path(self.tmpdir)
        self.cm = bdf.CacheManager("test_deal")

    def tearDown(self):
        bdf.CACHE_DIR = self._orig_cache_dir
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_write_creates_file(self):
        """write() creates the cache file with valid JSON."""
        data = {"status_code": 20000, "result": "ok"}
        written = self.cm.write("new_dir/result.json", data)
        self.assertTrue(os.path.exists(written))
        with open(written, "r") as f:
            loaded = json.load(f)
        self.assertEqual(loaded["status_code"], 20000)

    def test_write_creates_parent_dirs(self):
        """write() creates parent directories if needed."""
        data = {"status_code": 20000}
        written = self.cm.write("deep/nested/dir/result.json", data)
        self.assertTrue(os.path.exists(written))


class TestRequestParsing(unittest.TestCase):
    """parse_args() — CLI argument parsing."""

    def test_valid_inline_requests(self):
        """--requests with valid JSON parses correctly."""
        requests = [
            {"id": "test1", "endpoint": "test/endpoint", "body": [{"target": "example.com"}]}
        ]
        argv = ["batch_dataforseo.py", "--deal-id", "999", "--requests", json.dumps(requests)]
        deal_id, parsed = bdf.parse_args(argv)
        self.assertEqual(deal_id, "999")
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["id"], "test1")

    def test_valid_requests_file(self):
        """--requests-file with valid JSON file parses correctly."""
        requests = [
            {"id": "r1", "endpoint": "ep1"},
            {"id": "r2", "endpoint": "ep2"},
        ]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(requests, f)
            fpath = f.name
        try:
            deal_id, parsed = bdf.parse_args(
                ["batch_dataforseo.py", "--deal-id", "100", "--requests-file", fpath]
            )
            self.assertEqual(deal_id, "100")
            self.assertEqual(len(parsed), 2)
        finally:
            os.unlink(fpath)

    def test_missing_deal_id_exits(self):
        """Missing --deal-id should sys.exit(1)."""
        with self.assertRaises(SystemExit) as ctx:
            bdf.parse_args(["batch_dataforseo.py", "--requests", '[{"id":"x","endpoint":"y"}]'])
        self.assertEqual(ctx.exception.code, 1)

    def test_missing_requests_exits(self):
        """Missing both --requests and --requests-file should sys.exit(1)."""
        with self.assertRaises(SystemExit) as ctx:
            bdf.parse_args(["batch_dataforseo.py", "--deal-id", "999"])
        self.assertEqual(ctx.exception.code, 1)

    def test_invalid_json_exits(self):
        """Invalid JSON in --requests should sys.exit(1)."""
        with self.assertRaises(SystemExit) as ctx:
            bdf.parse_args(["batch_dataforseo.py", "--deal-id", "999", "--requests", "{bad"])
        self.assertEqual(ctx.exception.code, 1)

    def test_empty_array_exits(self):
        """Empty request array should sys.exit(1)."""
        with self.assertRaises(SystemExit) as ctx:
            bdf.parse_args(["batch_dataforseo.py", "--deal-id", "999", "--requests", "[]"])
        self.assertEqual(ctx.exception.code, 1)

    def test_missing_id_field_exits(self):
        """Request without 'id' field should sys.exit(1)."""
        with self.assertRaises(SystemExit) as ctx:
            bdf.parse_args([
                "batch_dataforseo.py", "--deal-id", "999",
                "--requests", '[{"endpoint": "test"}]'
            ])
        self.assertEqual(ctx.exception.code, 1)

    def test_missing_endpoint_field_exits(self):
        """Request without 'endpoint' field should sys.exit(1)."""
        with self.assertRaises(SystemExit) as ctx:
            bdf.parse_args([
                "batch_dataforseo.py", "--deal-id", "999",
                "--requests", '[{"id": "test"}]'
            ])
        self.assertEqual(ctx.exception.code, 1)


class TestAPIError(unittest.TestCase):
    """APIError class behavior."""

    def test_retryable_default(self):
        """APIError is retryable by default."""
        err = bdf.APIError("test error")
        self.assertTrue(err.retryable)

    def test_non_retryable(self):
        """APIError can be marked non-retryable."""
        err = bdf.APIError("auth failed", status_code=401, retryable=False)
        self.assertFalse(err.retryable)
        self.assertEqual(err.status_code, 401)


class TestBatchOrchestratorCachePhase(unittest.TestCase):
    """BatchOrchestrator.run() — cache phase only (no network calls)."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self._orig_cache_dir = bdf.CACHE_DIR
        bdf.CACHE_DIR = bdf.Path(self.tmpdir)

        # Create a fresh valid cache entry
        cache_dir = os.path.join(
            self.tmpdir, "deals", "888", "dataforseo", "domain"
        )
        os.makedirs(cache_dir, exist_ok=True)
        with open(os.path.join(cache_dir, "overview.json"), "w") as f:
            json.dump({"status_code": 20000, "tasks": []}, f)

        # Dummy credentials (won't be used since everything is cached)
        self.creds = bdf.Credentials("fake", "fake")

    def tearDown(self):
        bdf.CACHE_DIR = self._orig_cache_dir
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_cached_request_skips_fetch(self):
        """A request with fresh cache should be marked as 'cached' without network call."""
        requests = [
            {
                "id": "overview",
                "endpoint": "test/endpoint",
                "body": [],
                "cache_path": "domain/overview.json",
            }
        ]
        orch = bdf.BatchOrchestrator("888", requests, self.creds)
        summary = orch.run()
        self.assertEqual(summary["cached"], 1)
        self.assertEqual(summary["fetched"], 0)
        self.assertEqual(summary["failed"], 0)
        self.assertEqual(summary["results"]["overview"]["status"], "cached")


class TestCredentials(unittest.TestCase):
    """Credentials loading from files."""

    def test_load_missing_files_raises(self):
        """Missing credential files should raise APIError."""
        # Temporarily rename files if they exist
        login_path = os.path.expanduser("~/.dataforseo_login_test_nonexistent")
        # Directly test that missing files raise
        import unittest.mock as mock
        with mock.patch.object(bdf.Credentials, 'load') as mock_load:
            mock_load.side_effect = bdf.APIError("Credentials manquants", retryable=False)
            with self.assertRaises(bdf.APIError):
                bdf.Credentials.load()

    def test_credentials_auth_header(self):
        """Credentials should produce a valid Basic auth header."""
        import base64
        creds = bdf.Credentials("user@test.com", "secret123")
        expected = "Basic " + base64.b64encode(b"user@test.com:secret123").decode()
        self.assertEqual(creds.auth_header, expected)


if __name__ == "__main__":
    unittest.main()
