#!/usr/bin/env python3
"""
Tests for specific validation rules in validate_proposal.py.

Run: python3 -m pytest tests/test_validate_rules.py -v
"""

import os
import subprocess
import sys
import tempfile
import unittest

TOOLS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
VALIDATE_SCRIPT = os.path.join(TOOLS_DIR, "validate_proposal.py")


def run_validator(html_content):
    """Run validate_proposal.py on a temporary HTML file, return (stdout, returncode)."""
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


def rule_lines(stdout, rule_id):
    """Extract output lines mentioning a specific rule ID."""
    return [l for l in stdout.split("\n") if rule_id in l]


# A minimal HTML that passes most Layer 1 rules, used as a base for modifications.
BASELINE_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Test</title>
<style>
:root { --bg: #1a1a1a; }
body { background: #1a1a1a; }
@media print { .no-print { display: none; } }
</style>
</head><body style="background:#1a1a1a">
<div class="main">
<div class="tab-content active" id="tab-diagnostic">
  <div class="slide"><h2>Diagnostic</h2>
    <div class="s7-card" data-state="primary">Priorite</div>
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
    <button onclick="window.print()">Imprimer</button>
  </div>
  <div class="board-ready-a4">
    <p>Decision attendue</p>
  </div>
</div>
<div class="tab-content" id="tab-cas-clients">
  <div class="slide"><h2>Cas clients</h2><p>Resultats obtenus</p><p>Performance SEO</p><p>Croissance organique</p></div>
</div>
</div>
</body></html>"""


class TestR14InternalJargon(unittest.TestCase):
    """R14: Section synthese must exist in Diagnostic tab."""

    def test_passes_with_s7_card(self):
        """Baseline has s7-card -> R14 should PASS."""
        stdout, _ = run_validator(BASELINE_HTML)
        lines = rule_lines(stdout, "R14")
        self.assertTrue(len(lines) > 0, "R14 should appear in output")
        # Should pass (PASS or checkmark)
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertEqual(len(fail_lines), 0, "R14 should not FAIL with s7-card present")

    def test_fails_without_synthese(self):
        """Remove all synthese indicators -> R14 should FAIL."""
        html = BASELINE_HTML.replace('class="s7-card"', 'class="card"')
        html = html.replace("Synthese priorites urgence", "Information")
        html = html.replace("synthese", "xyz")
        html = html.replace("Synthese", "Xyz")
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R14")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R14 should FAIL without synthese section")


class TestR26CTAVerb(unittest.TestCase):
    """R26: CTA should not use passive/generic verbs."""

    def test_passes_without_bad_cta(self):
        """Baseline has no bad CTA -> R26 PASS."""
        stdout, _ = run_validator(BASELINE_HTML)
        lines = rule_lines(stdout, "R26")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertEqual(len(fail_lines), 0, "R26 should PASS without bad CTA verbs")

    def test_fails_with_planifier_un_echange(self):
        """'Planifier un echange' is a bad CTA -> R26 FAIL."""
        html = BASELINE_HTML.replace(
            "Prochaine etape",
            "Prochaine etape : planifier un echange"
        )
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R26")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R26 should FAIL with 'planifier un echange'")

    def test_fails_with_en_savoir_plus(self):
        """'En savoir plus' is a bad CTA -> R26 FAIL."""
        html = BASELINE_HTML.replace(
            "Prochaine etape",
            "Prochaine etape en savoir plus"
        )
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R26")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R26 should FAIL with 'en savoir plus'")


class TestR29NoTJMJours(unittest.TestCase):
    """R29: No TJM/jours-homme/AMOA in visible text."""

    def test_passes_clean_text(self):
        """Baseline has no internal terms -> R29 PASS."""
        stdout, _ = run_validator(BASELINE_HTML)
        lines = rule_lines(stdout, "R29")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertEqual(len(fail_lines), 0, "R29 should PASS on clean text")

    def test_fails_with_tjm(self):
        """TJM in visible text -> R29 FAIL."""
        html = BASELINE_HTML.replace("Phase 1", "Phase 1 (TJM 650 EUR)")
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R29")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R29 should FAIL with TJM")

    def test_fails_with_jours_homme(self):
        """jours-homme in visible text -> R29 FAIL."""
        html = BASELINE_HTML.replace("Phase 1", "Phase 1 : 12 jours-homme")
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R29")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R29 should FAIL with jours-homme")

    def test_fails_with_amoa(self):
        """AMOA in visible text -> R29 FAIL."""
        html = BASELINE_HTML.replace("Phase 2", "Phase 2 AMOA incluse")
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R29")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R29 should FAIL with AMOA")


class TestR18bEmDash(unittest.TestCase):
    """R18b: No em dash (tiret cadratin) in visible text."""

    def test_passes_without_emdash(self):
        """Baseline has no em dash -> R18b PASS."""
        stdout, _ = run_validator(BASELINE_HTML)
        lines = rule_lines(stdout, "R18b")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertEqual(len(fail_lines), 0, "R18b should PASS without em dash")

    def test_fails_with_unicode_emdash(self):
        """Unicode em dash (U+2014) -> R18b FAIL."""
        html = BASELINE_HTML.replace("Diagnostic", "Diagnostic \u2014 Vue globale")
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R18b")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R18b should FAIL with unicode em dash")

    def test_fails_with_html_entity_emdash(self):
        """HTML entity &mdash; -> R18b FAIL."""
        html = BASELINE_HTML.replace("Diagnostic", "Diagnostic &mdash; Vue globale")
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R18b")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R18b should FAIL with &mdash; entity")


class TestR36NotrePattern(unittest.TestCase):
    """R36: No 'Notre {X} :' pattern (lecture, conviction, etc.)."""

    def test_passes_without_notre(self):
        """Baseline has no 'Notre X :' -> R36 PASS."""
        stdout, _ = run_validator(BASELINE_HTML)
        lines = rule_lines(stdout, "R36")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertEqual(len(fail_lines), 0, "R36 should PASS without 'Notre X :' pattern")

    def test_fails_with_notre_lecture(self):
        """'Notre lecture :' -> R36 FAIL."""
        html = BASELINE_HTML.replace("Diagnostic", "Notre lecture : Diagnostic")
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R36")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R36 should FAIL with 'Notre lecture :'")

    def test_fails_with_notre_conviction(self):
        """'Notre conviction :' -> R36 FAIL."""
        html = BASELINE_HTML.replace("Strategie", "Notre conviction : Strategie")
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R36")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R36 should FAIL with 'Notre conviction :'")

    def test_fails_with_notre_approche(self):
        """'Notre approche :' -> R36 FAIL."""
        html = BASELINE_HTML.replace("Strategie", "Notre approche : la croissance")
        stdout, _ = run_validator(html)
        lines = rule_lines(stdout, "R36")
        fail_lines = [l for l in lines if "FAIL" in l]
        self.assertTrue(len(fail_lines) > 0, "R36 should FAIL with 'Notre approche :'")


class TestLayer1MinimalValid(unittest.TestCase):
    """A well-formed HTML should pass Layer 1 structural checks."""

    def test_baseline_passes_layer1(self):
        """Baseline HTML should have no Layer 1 FAILs."""
        stdout, _ = run_validator(BASELINE_HTML)
        # Extract Layer 1 section
        lines = stdout.split("\n")
        in_layer1 = False
        layer1_fails = []
        for line in lines:
            if "Layer 1" in line:
                in_layer1 = True
                continue
            if "Layer 2" in line:
                in_layer1 = False
                continue
            if in_layer1 and "FAIL" in line:
                layer1_fails.append(line.strip())
        self.assertEqual(
            layer1_fails, [],
            f"Baseline HTML should pass all Layer 1 rules. Failures: {layer1_fails}"
        )


if __name__ == "__main__":
    unittest.main()
