#!/usr/bin/env python3
"""
Basic tests for validate_proposal.py

Run: python3 -m pytest tests/ -v
"""

import subprocess
import sys
import os
import tempfile

TOOLS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
VALIDATE_SCRIPT = os.path.join(TOOLS_DIR, "validate_proposal.py")


def run_validator(html_content):
    """Run validate_proposal.py on a temporary HTML file, return stdout."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        f.flush()
        try:
            result = subprocess.run(
                [sys.executable, VALIDATE_SCRIPT, f.name],
                capture_output=True, text=True, timeout=30
            )
            return result.stdout, result.returncode
        finally:
            os.unlink(f.name)


MINIMAL_VALID_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Test</title>
<style>
:root { --bg: #1a1a1a; }
body { background: #1a1a1a; }
</style>
</head><body style="background:#1a1a1a">
<div class="main">
<div class="tab-content active" id="tab-diagnostic">
  <div class="slide"><h2>Diagnostic test</h2>
    <div class="s7-card" data-state="primary">Primary</div>
    <div class="highlight-box">Synthese priorites urgence</div>
    <div class="highlight-box">SO WHAT</div>
  </div>
</div>
<div class="tab-content" id="tab-strategie">
  <div class="slide"><h2>Strategie</h2>
    <p>M1 M2 M3 trajectoire 90 jours</p>
    <p>Recommandation feuille de route decision</p>
    <p>Ce que cela implique implications</p>
  </div>
</div>
<div class="tab-content" id="tab-investissement">
  <div class="highlight-box highlight-gradient">
    <ol><li>Point 1</li><li>Point 2</li><li>Point 3</li></ol>
  </div>
  <div class="slide">
    <p>cout de l'inaction</p>
    <p>inaction</p>
  </div>
  <div class="slide">
    <div class="pricing recommended">
      <p>Ce que ca debloque</p>
    </div>
    <p>Phase 1</p><p>Phase 2</p>
  </div>
  <div class="slide">
    <div class="accordion"><div class="accordion-item">FAQ</div></div>
    <p>Prochaine etape</p>
  </div>
  <div class="board-ready-a4">
    <p>Decision attendue</p>
  </div>
</div>
<div class="tab-content" id="tab-projet">
  <div class="slide"><h2>Projet</h2></div>
</div>
</div>
</body></html>"""


class TestValidatorRuns:
    """Basic smoke tests — validator runs without crashing."""

    def test_validator_exists(self):
        assert os.path.exists(VALIDATE_SCRIPT)

    def test_runs_on_minimal_html(self):
        stdout, code = run_validator(MINIMAL_VALID_HTML)
        assert "Layer 1" in stdout
        assert "Layer 2" in stdout

    def test_empty_html_fails(self):
        stdout, code = run_validator("<html><body></body></html>")
        assert code != 0 or "FAIL" in stdout


class TestLayer1Rules:
    """Layer 1 structural rules."""

    def test_r3_dark_background(self):
        """R3: fond sombre #1a1a1a"""
        html = MINIMAL_VALID_HTML.replace("#1a1a1a", "#ffffff")
        stdout, _ = run_validator(html)
        assert "R3" in stdout

    def test_r5_four_tabs(self):
        """R5: 4 onglets non-vides"""
        stdout, _ = run_validator(MINIMAL_VALID_HTML)
        # Should have at least diagnostic + strategie + investissement
        assert "R5" in stdout

    def test_r18b_no_emdash(self):
        """R18b: zero tiret cadratin"""
        html = MINIMAL_VALID_HTML.replace("Diagnostic test", "Diagnostic — test")
        stdout, _ = run_validator(html)
        lines = [l for l in stdout.split("\n") if "R18b" in l]
        assert len(lines) > 0

    def test_r37_no_chaque_mois_sans(self):
        """R37: pas de 'Chaque mois/jour sans'"""
        html = MINIMAL_VALID_HTML.replace("Diagnostic test", "Chaque mois sans action")
        stdout, _ = run_validator(html)
        lines = [l for l in stdout.split("\n") if "R37" in l and "FAIL" in l]
        assert len(lines) > 0


class TestBuildProposal:
    """Basic smoke test for build_proposal.py."""

    def test_build_script_exists(self):
        build_script = os.path.join(TOOLS_DIR, "build_proposal.py")
        assert os.path.exists(build_script)

    def test_build_help(self):
        build_script = os.path.join(TOOLS_DIR, "build_proposal.py")
        result = subprocess.run(
            [sys.executable, build_script, "--help"],
            capture_output=True, text=True, timeout=10
        )
        assert result.returncode == 0
        assert "deal-id" in result.stdout
