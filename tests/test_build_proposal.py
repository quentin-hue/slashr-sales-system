#!/usr/bin/env python3
"""
Tests for build_proposal.py — HTML assembly from skeleton + tab fragments.

Run: python3 -m pytest tests/test_build_proposal.py -v
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

TOOLS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
BUILD_SCRIPT = os.path.join(TOOLS_DIR, "build_proposal.py")
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
SKELETON_PATH = os.path.join(TEMPLATES_DIR, "proposal-skeleton.html")


def run_build(args, timeout=15):
    """Run build_proposal.py with given args, return (stdout, stderr, returncode)."""
    result = subprocess.run(
        [sys.executable, BUILD_SCRIPT] + args,
        capture_output=True, text=True, timeout=timeout
    )
    return result.stdout, result.stderr, result.returncode


class TestBuildMissingArgs(unittest.TestCase):
    """Missing required arguments should fail with exit code 2 (argparse error)."""

    def test_no_args(self):
        _, _, code = run_build([])
        self.assertEqual(code, 2, "No args should cause argparse error (exit 2)")

    def test_missing_deal_id(self):
        _, _, code = run_build([
            "--title", "Test",
            "--diagnostic", "/tmp/x.html",
            "--strategie", "/tmp/x.html",
            "--investissement", "/tmp/x.html",
        ])
        self.assertEqual(code, 2)

    def test_missing_title(self):
        _, _, code = run_build([
            "--deal-id", "999",
            "--diagnostic", "/tmp/x.html",
            "--strategie", "/tmp/x.html",
            "--investissement", "/tmp/x.html",
        ])
        self.assertEqual(code, 2)

    def test_missing_diagnostic(self):
        _, _, code = run_build([
            "--deal-id", "999",
            "--title", "Test",
            "--strategie", "/tmp/x.html",
            "--investissement", "/tmp/x.html",
        ])
        self.assertEqual(code, 2)


class TestBuildMissingFiles(unittest.TestCase):
    """Missing input files should fail with exit code 2."""

    def test_missing_diagnostic_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write("<p>Strategie</p>")
            strat = f.name
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write("<p>Investissement</p>")
            invest = f.name
        try:
            _, stderr, code = run_build([
                "--deal-id", "999",
                "--title", "Test",
                "--diagnostic", "/tmp/nonexistent_diag_12345.html",
                "--strategie", strat,
                "--investissement", invest,
            ])
            self.assertEqual(code, 2, f"Expected exit 2 for missing file, got {code}. stderr: {stderr}")
        finally:
            os.unlink(strat)
            os.unlink(invest)


class TestBuildSuccessful(unittest.TestCase):
    """Successful assembly with minimal tab content."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Create minimal tab fragments (including projet/cas-clients to avoid
        # placeholder removal mismatch between skeleton comments and script)
        self.tabs = {}
        for name in ("diagnostic", "strategie", "investissement", "projet", "cas_clients"):
            path = os.path.join(self.tmpdir, f"tab_{name}.html")
            with open(path, "w") as f:
                f.write(f'<div class="slide"><h2>{name.capitalize()}</h2><p>Content for {name}</p></div>')
            self.tabs[name] = path
        self.output_path = os.path.join(self.tmpdir, "output.html")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _requires_skeleton(self):
        if not os.path.exists(SKELETON_PATH):
            self.skipTest("Skeleton template not found")

    def _all_tabs_args(self):
        """Return args for all tabs (required + optional) to avoid placeholder issues."""
        return [
            "--diagnostic", self.tabs["diagnostic"],
            "--strategie", self.tabs["strategie"],
            "--investissement", self.tabs["investissement"],
            "--projet", self.tabs["projet"],
            "--cas-clients", self.tabs["cas_clients"],
        ]

    def test_minimal_assembly(self):
        """Assemble with all tabs produces valid output."""
        self._requires_skeleton()
        stdout, stderr, code = run_build([
            "--deal-id", "999",
            "--title", "Test Proposal",
            *self._all_tabs_args(),
            "--output", self.output_path,
        ])
        self.assertEqual(code, 0, f"Expected exit 0, got {code}. stderr: {stderr}")
        self.assertTrue(os.path.exists(self.output_path), "Output file should be created")

        # Stdout should be valid JSON summary
        summary = json.loads(stdout)
        self.assertEqual(summary["status"], "ok")
        self.assertIn("diagnostic", summary["tabs"])
        self.assertIn("size_bytes", summary)

    def test_output_contains_tab_content(self):
        """Tab content should appear in the assembled HTML."""
        self._requires_skeleton()
        stdout, _, code = run_build([
            "--deal-id", "999",
            "--title", "Test Proposal",
            *self._all_tabs_args(),
            "--output", self.output_path,
        ])
        self.assertEqual(code, 0)
        with open(self.output_path, "r") as f:
            html = f.read()
        self.assertIn("Content for diagnostic", html)
        self.assertIn("Content for strategie", html)
        self.assertIn("Content for investissement", html)

    def test_title_placeholder_replaced(self):
        """{{TITLE}} placeholder should be replaced with the provided title."""
        self._requires_skeleton()
        stdout, _, code = run_build([
            "--deal-id", "999",
            "--title", "Mon Titre Custom",
            *self._all_tabs_args(),
            "--output", self.output_path,
        ])
        self.assertEqual(code, 0)
        with open(self.output_path, "r") as f:
            html = f.read()
        self.assertIn("Mon Titre Custom", html)
        self.assertNotIn("{{TITLE}}", html)

    def test_no_unreplaced_placeholders(self):
        """No {{PLACEHOLDER}} patterns should remain in output."""
        self._requires_skeleton()
        import re
        stdout, _, code = run_build([
            "--deal-id", "999",
            "--title", "Test",
            *self._all_tabs_args(),
            "--output", self.output_path,
        ])
        self.assertEqual(code, 0)
        with open(self.output_path, "r") as f:
            html = f.read()
        remaining = re.findall(r'\{\{[A-Z_]+\}\}', html)
        self.assertEqual(remaining, [], f"Unreplaced placeholders found: {remaining}")


class TestBuildOptionalArgs(unittest.TestCase):
    """Optional arguments (--contexte, --projet, --cas-clients, --extra-js)."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.tabs = {}
        for name in ("diagnostic", "strategie", "investissement", "projet", "cas_clients"):
            path = os.path.join(self.tmpdir, f"tab_{name}.html")
            with open(path, "w") as f:
                f.write(f'<div class="slide"><h2>{name.capitalize()}</h2><p>{name}</p></div>')
            self.tabs[name] = path
        self.output_path = os.path.join(self.tmpdir, "output.html")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _requires_skeleton(self):
        if not os.path.exists(SKELETON_PATH):
            self.skipTest("Skeleton template not found")

    def _all_tabs_args(self):
        """Return args for all tabs to avoid placeholder issues."""
        return [
            "--diagnostic", self.tabs["diagnostic"],
            "--strategie", self.tabs["strategie"],
            "--investissement", self.tabs["investissement"],
            "--projet", self.tabs["projet"],
            "--cas-clients", self.tabs["cas_clients"],
        ]

    def test_with_contexte_tab(self):
        """--contexte adds a Contexte tab."""
        self._requires_skeleton()
        ctx_path = os.path.join(self.tmpdir, "tab_contexte.html")
        with open(ctx_path, "w") as f:
            f.write('<div class="slide"><h2>Contexte</h2><p>Contexte content here</p></div>')

        stdout, _, code = run_build([
            "--deal-id", "999",
            "--title", "Test",
            "--contexte", ctx_path,
            *self._all_tabs_args(),
            "--output", self.output_path,
        ])
        self.assertEqual(code, 0)
        summary = json.loads(stdout)
        self.assertIn("contexte", summary["tabs"])

        with open(self.output_path, "r") as f:
            html = f.read()
        self.assertIn("Contexte content here", html)

    def test_with_projet_tab(self):
        """--projet adds a Projet tab with custom content."""
        self._requires_skeleton()
        # Override the default projet tab with custom content
        proj_path = os.path.join(self.tmpdir, "tab_projet_custom.html")
        with open(proj_path, "w") as f:
            f.write('<div class="slide"><h2>Projet</h2><p>Custom projet content</p></div>')

        stdout, _, code = run_build([
            "--deal-id", "999",
            "--title", "Test",
            "--diagnostic", self.tabs["diagnostic"],
            "--strategie", self.tabs["strategie"],
            "--investissement", self.tabs["investissement"],
            "--projet", proj_path,
            "--cas-clients", self.tabs["cas_clients"],
            "--output", self.output_path,
        ])
        self.assertEqual(code, 0)
        summary = json.loads(stdout)
        self.assertIn("projet", summary["tabs"])

    def test_with_extra_js(self):
        """--extra-js injects custom JavaScript."""
        self._requires_skeleton()
        js_path = os.path.join(self.tmpdir, "extra.js")
        with open(js_path, "w") as f:
            f.write('console.log("ROI simulator loaded");')

        stdout, _, code = run_build([
            "--deal-id", "999",
            "--title", "Test",
            *self._all_tabs_args(),
            "--extra-js", js_path,
            "--output", self.output_path,
        ])
        self.assertEqual(code, 0)
        summary = json.loads(stdout)
        self.assertTrue(summary["extra_js"])

        with open(self.output_path, "r") as f:
            html = f.read()
        self.assertIn("ROI simulator loaded", html)


if __name__ == "__main__":
    unittest.main()
