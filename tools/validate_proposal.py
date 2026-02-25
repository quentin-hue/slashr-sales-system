#!/usr/bin/env python3
"""
SLASHR Proposal Validator — v2.0

Valide un HTML de proposition contre les 44 regles de validation (3 onglets : Diagnostic, Strategie, Investissement).
- Layer 1 (Structural) : PASS/FAIL — echec = REJECT
- Layer 2 (Content) : WARN — correction recommandee
- Layer 3 (Semantic) : checklist affichee pour revue manuelle
- Layer 4 (Quality Metrics) : WARN — metriques de qualite redactionnelle

Usage:
    python3 tools/validate_proposal.py <path_to_html>
    python3 tools/validate_proposal.py .cache/deals/560/artifacts/PROPOSAL-*.html
    python3 tools/validate_proposal.py --nbp <path_to_nbp.md>

Python 3.9, stdlib uniquement (html.parser, re, os, sys).
"""

import sys
import os
import re
from html.parser import HTMLParser


# ---------------------------------------------------------------------------
# HTML Parser — extrait la structure du document
# ---------------------------------------------------------------------------

class ProposalParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_tab = None
        self.tabs = {}  # id -> content text
        self.tab_elements = {}  # id -> list of (tag, attrs, text)
        self.all_text = []
        self.all_classes = []
        self.all_ids = []
        self.data_states = []
        self.has_print_media = False
        self.has_print_button = False
        self.css_content = ""
        self.in_style = False
        self.in_script = False
        self.current_tag_stack = []
        self.h2_order = []  # h2 texts in order within tab-diagnostic
        self.in_h2 = False
        self.h2_buffer = ""

        # R18: track <li> inside highlight-gradient in tab-investissement
        self.in_highlight_gradient_investissement = False
        self.highlight_gradient_depth = 0
        self.highlight_gradient_li_count = 0

        # Layer 4 quality metrics
        self.diag_paragraphs = []  # list of paragraph texts in tab-diagnostic
        self.diag_h2s = []  # list of h2 texts in tab-diagnostic
        self.in_p_diag = False
        self.p_diag_buffer = ""

        # R42: "Ce que cela implique" tracking (highlight-boxes OR li)
        self.implique_detected = False  # text "ce que cela implique" seen
        self.implique_done = False  # stop collecting when next slide starts
        self.implique_items = []  # list of text items (from highlight-box or li)
        # li tracking
        self.in_implique_list = False
        self.in_implique_li = False
        self.implique_li_buffer = ""
        # highlight-box tracking
        self.in_implique_highlight = False
        self.implique_highlight_depth = 0
        self.implique_highlight_buffer = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get("class", "")
        elem_id = attr_dict.get("id", "")

        if classes:
            self.all_classes.extend(classes.split())
        if elem_id:
            self.all_ids.append(elem_id)

        # Track tab content containers
        if "tab-content" in classes:
            self.current_tab = elem_id
            if elem_id not in self.tabs:
                self.tabs[elem_id] = []
                self.tab_elements[elem_id] = []

        # Track data-state for S7
        ds = attr_dict.get("data-state", "")
        if ds:
            self.data_states.append(ds)

        # Track style/script
        if tag == "style":
            self.in_style = True
        if tag == "script":
            self.in_script = True

        # Track h2 inside tab-diagnostic
        if tag == "h2" and self.current_tab == "tab-diagnostic":
            self.in_h2 = True
            self.h2_buffer = ""

        # R18: Track highlight-gradient in tab-investissement for bullet counting
        # Void elements (br, hr, img, etc.) don't have closing tags, so skip depth tracking
        void_elements = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base',
                         'col', 'embed', 'param', 'source', 'track', 'wbr'}
        if "highlight-gradient" in classes.split() and self.current_tab == "tab-investissement":
            self.in_highlight_gradient_investissement = True
            self.highlight_gradient_depth = 1
        elif self.in_highlight_gradient_investissement and tag not in void_elements:
            self.highlight_gradient_depth += 1
            if tag == "li":
                self.highlight_gradient_li_count += 1

        # Track print button
        if "window.print" in str(attrs):
            self.has_print_button = True

        # Layer 4: Track <p> in tab-diagnostic for density metric
        if tag == "p" and self.current_tab == "tab-diagnostic" and "section-label" not in classes:
            self.in_p_diag = True
            self.p_diag_buffer = ""

        # R42: Track items in "Ce que cela implique" section (highlight-boxes OR li)
        if self.implique_detected and not self.implique_done:
            # Stop when a new slide starts
            if "slide" in classes.split() and tag in ("div", "section"):
                self.implique_done = True
            # Track highlight-boxes as items
            elif "highlight-box" in classes.split() and not self.in_implique_highlight:
                self.in_implique_highlight = True
                self.implique_highlight_depth = 1
                self.implique_highlight_buffer = ""
            elif self.in_implique_highlight and tag not in void_elements:
                self.implique_highlight_depth += 1
            # Track li inside ul/ol as items
            if not self.implique_done and not self.in_implique_highlight:
                if tag in ("ul", "ol") and not self.in_implique_list:
                    self.in_implique_list = True
                if self.in_implique_list and tag == "li":
                    self.in_implique_li = True
                    self.implique_li_buffer = ""

        # Store element info for tab
        if self.current_tab and self.current_tab in self.tab_elements:
            self.tab_elements[self.current_tab].append((tag, classes, ""))

        self.current_tag_stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
        if tag == "script":
            self.in_script = False
        if tag == "h2" and self.in_h2:
            self.in_h2 = False
            self.h2_order.append(self.h2_buffer.strip())
        # R18: track highlight-gradient container depth
        if self.in_highlight_gradient_investissement:
            self.highlight_gradient_depth -= 1
            if self.highlight_gradient_depth <= 0:
                self.in_highlight_gradient_investissement = False

        # Layer 4: close <p> tracking
        if tag == "p" and self.in_p_diag:
            self.in_p_diag = False
            if self.p_diag_buffer.strip():
                self.diag_paragraphs.append(self.p_diag_buffer.strip())

        # R42: close highlight-box, <li> and <ul>/<ol> in implique section
        if self.in_implique_highlight:
            self.implique_highlight_depth -= 1
            if self.implique_highlight_depth <= 0:
                self.in_implique_highlight = False
                if self.implique_highlight_buffer.strip():
                    self.implique_items.append(self.implique_highlight_buffer.strip())
                self.implique_highlight_buffer = ""
        if tag == "li" and self.in_implique_li:
            self.in_implique_li = False
            if self.implique_li_buffer.strip():
                self.implique_items.append(self.implique_li_buffer.strip())
        if tag in ("ul", "ol") and self.in_implique_list:
            self.in_implique_list = False

        if self.current_tag_stack and self.current_tag_stack[-1] == tag:
            self.current_tag_stack.pop()

    def handle_data(self, data):
        if self.in_style:
            self.css_content += data
            if "@media print" in data:
                self.has_print_media = True
            return
        if self.in_script:
            if "window.print" in data:
                self.has_print_button = True
            return

        text = data.strip()
        if not text:
            return

        self.all_text.append(text)
        if self.current_tab and self.current_tab in self.tabs:
            self.tabs[self.current_tab].append(text)

        if self.in_h2:
            self.h2_buffer += data

        # Layer 4: accumulate paragraph text
        if self.in_p_diag:
            self.p_diag_buffer += data

        # R42: detect "Ce que cela implique" section and accumulate item text
        if self.current_tab == "tab-diagnostic" and "ce que cela implique" in data.lower():
            self.implique_detected = True
        if self.in_implique_li:
            self.implique_li_buffer += data
        if self.in_implique_highlight:
            self.implique_highlight_buffer += data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def tab_text(parser, tab_id):
    """Full text content of a tab."""
    return " ".join(parser.tabs.get(tab_id, []))


def tab_has_class(parser, tab_id, cls):
    """Check if a CSS class appears in a tab's elements."""
    for _, classes, _ in parser.tab_elements.get(tab_id, []):
        if cls in classes.split():
            return True
    return False


def count_in_tab(parser, tab_id, cls):
    """Count elements with a CSS class in a tab."""
    count = 0
    for _, classes, _ in parser.tab_elements.get(tab_id, []):
        if cls in classes.split():
            count += 1
    return count


def full_text(parser):
    """All visible text concatenated."""
    return " ".join(parser.all_text)


# ---------------------------------------------------------------------------
# Layer 1 — Structural (PASS/FAIL)
# ---------------------------------------------------------------------------

def check_layer1(parser, html_raw):
    results = []

    # R3: Fond sombre #1a1a1a
    has_bg = "#1a1a1a" in parser.css_content or "#1a1a1a" in html_raw
    results.append(("R3", "Fond sombre #1a1a1a", has_bg))

    # R5: 3 onglets non-vides
    required_tabs = ["tab-diagnostic", "tab-strategie", "tab-investissement"]
    tabs_ok = all(
        tab_id in parser.tabs and len(parser.tabs[tab_id]) > 2
        for tab_id in required_tabs
    )
    missing = [t for t in required_tabs if t not in parser.tabs or len(parser.tabs.get(t, [])) <= 2]
    detail = f" (manquants/vides: {', '.join(missing)})" if missing else ""
    results.append(("R5", f"3 onglets non-vides{detail}", tabs_ok))

    # R14: Section S7 dans onglet Diagnostic
    diag_text = tab_text(parser, "tab-diagnostic").lower()
    has_s7 = tab_has_class(parser, "tab-diagnostic", "s7-grid") or \
             tab_has_class(parser, "tab-diagnostic", "s7-card") or \
             "s7-grid" in diag_text or "s7-card" in diag_text
    results.append(("R14", "Section S7 dans onglet Diagnostic", has_s7))

    # R16: Exactement 1 PRIMARY
    primary_count = parser.data_states.count("primary")
    results.append(("R16", f"Exactement 1 PRIMARY (trouve: {primary_count})", primary_count == 1))

    # R18: Resume decisionnel <= 6 bullets
    has_gradient = tab_has_class(parser, "tab-investissement", "highlight-gradient")
    li_count = parser.highlight_gradient_li_count
    if has_gradient and li_count > 6:
        results.append(("R18", f"Resume decisionnel <= 6 bullets (trouve: {li_count})", False))
    elif has_gradient:
        results.append(("R18", f"Resume decisionnel <= 6 bullets ({li_count} bullets)", True))
    else:
        results.append(("R18", "Resume decisionnel absent (highlight-gradient manquant)", False))

    # R19: Board-ready A4 / print
    has_print = parser.has_print_media and parser.has_print_button
    results.append(("R19", "Board-ready A4 (@media print + bouton print)", has_print))

    # R26: CTA avec verbe strategique
    ft = full_text(parser).lower()
    bad_ctas = ["planifier un echange", "discuter", "echanger", "en savoir plus"]
    has_bad_cta = any(bc in ft for bc in bad_ctas)
    results.append(("R26", "CTA sans verbe passif/generique", not has_bad_cta))

    # R29: Zero jours/TJM/AMOA/termes internes
    internal_pattern = re.compile(
        r'\b(jour[s]?[\s\-]homme|TJM|AMOA|etude lexicale|plan de? redirections|recettage|recette fonctionnelle|phase de recette)\b',
        re.IGNORECASE
    )
    # Check only visible text (not CSS/JS)
    visible = full_text(parser)
    has_internal = bool(internal_pattern.search(visible))
    if has_internal:
        matches = internal_pattern.findall(visible)
        results.append(("R29", f"Zero jours/TJM/AMOA (trouve: {', '.join(matches[:3])})", False))
    else:
        results.append(("R29", "Zero jours/TJM/AMOA dans le texte visible", True))

    # R31: Accordion FAQ dans Investissement
    has_accordion = tab_has_class(parser, "tab-investissement", "accordion")
    results.append(("R31", "Accordion FAQ dans onglet Investissement", has_accordion))

    # R35: "Prochaine etape" dans Investissement
    has_next = "prochaine" in tab_text(parser, "tab-investissement").lower() and \
               "tape" in tab_text(parser, "tab-investissement").lower()
    results.append(("R35", "\"Prochaine etape\" dans Investissement", has_next))

    # R36: Pas de "Notre {X} :"
    notre_pattern = re.compile(
        r'Notre\s+(lecture|conviction|position|approche|methode|vision)\s*:',
        re.IGNORECASE
    )
    has_notre = bool(notre_pattern.search(visible))
    results.append(("R36", "Pas de pattern \"Notre {X} :\"", not has_notre))

    # R37: Pas de "Chaque mois/jour sans"
    anaphore_pattern = re.compile(r'Chaque\s+(mois|jour|semaine)\s+sans', re.IGNORECASE)
    has_anaphore = bool(anaphore_pattern.search(visible))
    results.append(("R37", "Pas de structure anaphorique \"Chaque mois/jour sans\"", not has_anaphore))

    # R38: Pricing cards exclusives a Investissement (pas dans Strategie)
    has_pricing_in_strat = tab_has_class(parser, "tab-strategie", "pricing") or \
                           tab_has_class(parser, "tab-strategie", "pricing-grid")
    results.append(("R38", "Pricing cards absentes de l'onglet Strategie", not has_pricing_in_strat))

    # R39: ETV vs trafic — only flag if ETV is directly mislabeled as visits
    etv_mislabeled = False
    strat_lower = tab_text(parser, "tab-diagnostic").lower()
    if "etv" in strat_lower:
        # Flag only direct mislabeling patterns: "ETV de X visites", "ETV : X visites"
        mislabel_patterns = [
            r'\betv\b\s*(?:de\s+)?\d[\d\s,.]*\s*visites?',
            r'visites?\s*(?:=|:)\s*\d[\d\s,.]*\s*\betv\b',
            r'\betv\b\s*(?:=|:)\s*\d[\d\s,.]*\s*visites?',
        ]
        for pat in mislabel_patterns:
            if re.search(pat, strat_lower):
                etv_mislabeled = True
                break
    results.append(("R39", "ETV/trafic correctement etiquetes", not etv_mislabeled))

    # R28a: Investissement avec .recommended + cout inaction (AVANT pricing)
    has_recommended = "recommended" in " ".join(parser.all_classes)
    livr_lower = tab_text(parser, "tab-investissement").lower()
    cout_inaction = "inaction" in livr_lower and ("cout" in livr_lower or "coute" in livr_lower)
    # Check order: cout inaction should appear BEFORE first pricing element
    inaction_before_pricing = True
    if cout_inaction:
        inv_elements = parser.tab_elements.get("tab-investissement", [])
        inaction_pos = -1
        pricing_pos = -1
        for i, (tag, classes, _) in enumerate(inv_elements):
            cls_list = classes.split()
            if inaction_pos < 0 and "s7-insight" in cls_list:
                inaction_pos = i
            if pricing_pos < 0 and ("pricing" in cls_list or "pricing-grid" in cls_list):
                pricing_pos = i
        if inaction_pos >= 0 and pricing_pos >= 0:
            inaction_before_pricing = inaction_pos < pricing_pos
    r28a_ok = has_recommended and cout_inaction
    detail_parts = []
    if not has_recommended:
        detail_parts.append(".recommended absent")
    if not cout_inaction:
        detail_parts.append("cout inaction absent")
    if cout_inaction and not inaction_before_pricing:
        detail_parts.append("cout inaction APRES pricing (doit etre AVANT)")
        r28a_ok = False
    detail = f" ({', '.join(detail_parts)})" if detail_parts else ""
    results.append(("R28a", f"Investissement : .recommended + cout inaction avant pricing{detail}", r28a_ok))

    # R30: Coherence Phase 1 ↔ Phase 2
    has_phase1 = "phase 1" in livr_lower or "mission structurante" in livr_lower
    has_phase2 = "phase 2" in livr_lower or "accompagnement mensuel" in livr_lower
    has_pricing = tab_has_class(parser, "tab-investissement", "pricing") or \
                  tab_has_class(parser, "tab-investissement", "pricing-grid") or \
                  tab_has_class(parser, "tab-investissement", "pricing-card")
    if has_pricing or has_phase1 or has_phase2:
        r30_ok = has_phase1 and has_phase2
        if not r30_ok:
            missing = "Phase 1" if not has_phase1 else "Phase 2"
            results.append(("R30", f"Coherence Phase 1 ↔ Phase 2 ({missing} absente)", False))
        else:
            # Check lever coherence: same levers in both phases
            levers = {"seo": "SEO", "sea": "SEA", "geo": "GEO", "social": "Social"}
            # Split on Phase 2 section heading (not first mention in resume)
            # Look for "accompagnement mensuel" first (heading-only), then
            # fall back to "mission structurante" boundary (end of Phase 1 card)
            p2_idx = livr_lower.find("accompagnement mensuel")
            if p2_idx < 0:
                # Find the Phase 2 section: look for "phase 2" after "mission structurante"
                p1_section = livr_lower.find("mission structurante")
                if p1_section > 0:
                    p2_idx = livr_lower.find("phase 2", p1_section)
                else:
                    p2_idx = livr_lower.rfind("phase 2")
            if p2_idx > 0:
                p1_text = livr_lower[:p2_idx]
                p2_text = livr_lower[p2_idx:]
                mismatched = []
                for key, label in levers.items():
                    in_p1 = key in p1_text
                    in_p2 = key in p2_text
                    if in_p1 and not in_p2:
                        mismatched.append(f"{label} Phase 1 only")
                    elif in_p2 and not in_p1:
                        mismatched.append(f"{label} Phase 2 only")
                if mismatched:
                    results.append(("R30", f"Coherence leviers ({', '.join(mismatched)})", False))
                else:
                    results.append(("R30", "Coherence Phase 1 ↔ Phase 2", True))
            else:
                results.append(("R30", "Coherence Phase 1 ↔ Phase 2", True))
    else:
        results.append(("R30", "Coherence Phase 1 ↔ Phase 2 (pas de pricing detecte)", True))

    return results


# ---------------------------------------------------------------------------
# Layer 2 — Content (WARN)
# ---------------------------------------------------------------------------

def check_layer2(parser, html_raw):
    results = []
    diag = tab_text(parser, "tab-diagnostic").lower()
    strat = tab_text(parser, "tab-strategie").lower()
    livr = tab_text(parser, "tab-investissement").lower()

    # R20: Trajectoire 90j M1/M2/M3
    has_m1m2m3 = all(f"m{i}" in livr or f"m{i}" in strat for i in [1, 2, 3])
    results.append(("R20", "Trajectoire 90j avec M1/M2/M3", has_m1m2m3))

    # R22: "Ce que cela implique" (dans onglet Diagnostic)
    has_implies = "ce que cela implique" in diag
    results.append(("R22", "Section \"Ce que cela implique\" presente", has_implies))

    # R23: "Nous recommandons"
    has_reco = "nous recommandons" in strat
    results.append(("R23", "\"Nous recommandons\" dans la decision", has_reco))

    # R24: "Decision strategique"
    has_decision = "decision strategique" in strat or "décision stratégique" in strat
    results.append(("R24", "Section \"Decision strategique\" presente", has_decision))

    # R25: Sequence Diagnostic → S7 → Implications (tab-diagnostic) puis Decision → 90j (tab-strategie)
    sequence_markers = [
        ("diagnostic", "diagnostic" in diag or "lecture strategique" in diag),
        ("s7", "s7" in diag or tab_has_class(parser, "tab-diagnostic", "s7-grid")),
        ("implications", "ce que cela implique" in diag),
        ("decision", "decision strategique" in strat or "nous recommandons" in strat),
        ("90j", "90 jours" in strat or "90j" in strat),
    ]
    all_present = all(present for _, present in sequence_markers)
    missing_seq = [name for name, present in sequence_markers if not present]
    detail = f" (manquants: {', '.join(missing_seq)})" if missing_seq else ""
    results.append(("R25", f"Sequence narrative complete{detail}", all_present))

    # R32: Pricing cards avec "Ce que ca debloque"
    has_debloque = "ce que ca debloque" in livr or "ce que ça débloque" in livr
    results.append(("R32", "Pricing cards avec \"Ce que ca debloque\"", has_debloque))

    # R8: Pas 2 blocs data consecutifs sans interpretation
    # Heuristic: check that highlight-box appears between data components
    results.append(("R8", "Alternance data/interpretation (verification manuelle)", None))

    # R9: Pas de "Pourquoi SLASHR" standalone
    pourquoi_pattern = re.compile(r'pourquoi\s+slashr', re.IGNORECASE)
    visible = full_text(parser)
    has_pourquoi = bool(pourquoi_pattern.search(visible))
    results.append(("R9", "Pas de section \"Pourquoi SLASHR\" standalone", not has_pourquoi))

    # R34: Board-ready avec "Decision attendue"
    has_decision_attendue = "decision attendue" in full_text(parser).lower() or \
                            "décision attendue" in full_text(parser).lower()
    results.append(("R34", "Board-ready avec \"Decision attendue\"", has_decision_attendue))

    # R10: Differenciateurs lies a un data block
    results.append(("R10", "Differenciateurs lies a un data block (verification manuelle)", None))

    # R28b: Cout inaction avec impacts chiffres (dans onglet Investissement)
    has_cout = "inaction" in livr
    # Verify that "inaction" section contains actual numbers (not just the word)
    if has_cout:
        # Extract text around "inaction" and check for digits
        inaction_positions = [m.start() for m in re.finditer(r'inaction', livr)]
        has_numbers_near_inaction = False
        for pos in inaction_positions:
            context_window = livr[pos:min(pos + 500, len(livr))]
            if re.search(r'\d[\d\s,.]*\d', context_window):
                has_numbers_near_inaction = True
                break
        if not has_numbers_near_inaction:
            results.append(("R28b", "Sous-bloc \"cout de l'inaction\" present MAIS sans impacts chiffres", False))
        else:
            results.append(("R28b", "Sous-bloc \"cout de l'inaction\" avec impacts chiffres", True))
    else:
        results.append(("R28b", "Sous-bloc \"cout de l'inaction\" absent", False))

    return results


# ---------------------------------------------------------------------------
# Layer 3 — Semantic (checklist)
# ---------------------------------------------------------------------------

LAYER3_CHECKLIST = [
    ("R1", "Test de substitution : chaque section est specifique a CE prospect ?"),
    ("R2", "Chaque chiffre a une source identifiable ?"),
    ("R4", "Ton partenaire strategique (ni arrogant, ni suppliant, ni jargonneux) ?"),
    ("R6", "ROI : hypotheses toutes sourcees ?"),
    ("R7", "Arc narratif justifie par le contexte du deal ?"),
    ("R11", "Zero pression commerciale (\"ne manquez pas\", \"il est urgent de\") ?"),
    ("R12", "Zero dramatisation (\"catastrophe\", \"crise\", \"vous perdez tout\") ?"),
    ("R13", "S7 : max 3 leviers actifs (pas les 7) ?"),
    ("R15", "Insight S7 non-substituable ?"),
    ("R17", "Chaque DEFERRED a un \"pourquoi pas maintenant\" ?"),
]


# ---------------------------------------------------------------------------
# Layer 4 — Quality Metrics (WARN)
# ---------------------------------------------------------------------------

def check_layer4(parser, html_raw):
    results = []

    # R40: Densite de donnees dans l'onglet Diagnostic
    # >= 50% des paragraphes contiennent au moins 1 chiffre
    paragraphs = parser.diag_paragraphs
    if paragraphs:
        has_number = sum(1 for p in paragraphs if re.search(r'\d', p))
        ratio = has_number / len(paragraphs)
        pct = int(ratio * 100)
        ok = ratio >= 0.5
        results.append(("R40", f"Densite donnees onglet Diagnostic : {pct}% paragraphes avec chiffre (seuil: 50%)", ok))
    else:
        results.append(("R40", "Densite donnees : aucun paragraphe detecte dans l'onglet Diagnostic", False))

    # R41: Specificite des titres h2 dans tab-diagnostic
    # >= 60% des h2 contiennent un nom propre (majuscule non initiale) ou un chiffre
    h2s = parser.h2_order
    if h2s:
        specific = 0
        for h2 in h2s:
            has_digit = bool(re.search(r'\d', h2))
            # Detect proper nouns: words starting with uppercase that are not
            # the first word and not common French words
            words = h2.split()
            has_proper = False
            for i, w in enumerate(words):
                if i > 0 and w[0:1].isupper() and len(w) > 2:
                    has_proper = True
                    break
            if has_digit or has_proper:
                specific += 1
        ratio = specific / len(h2s)
        pct = int(ratio * 100)
        ok = ratio >= 0.6
        results.append(("R41", f"Specificite titres h2 : {pct}% avec nom propre/chiffre ({specific}/{len(h2s)}, seuil: 60%)", ok))
    else:
        results.append(("R41", "Specificite titres : aucun h2 dans l'onglet Diagnostic", False))

    # R42: Triplet "Ce que cela implique" — 3 items (highlight-boxes OR li), le 3e contient un chiffre
    items = parser.implique_items
    if items:
        count_ok = len(items) == 3
        third_has_number = len(items) >= 3 and bool(re.search(r'\d', items[2]))
        ok = count_ok and third_has_number
        detail = f"{len(items)} items"
        if len(items) >= 3:
            detail += f", 3e item {'contient' if third_has_number else 'NE contient PAS'} un chiffre"
        results.append(("R42", f"Triplet 'Ce que cela implique' : {detail}", ok))
    else:
        results.append(("R42", "Section 'Ce que cela implique' non detectee", None))

    # R43: SO WHAT — chaque .slide dans #tab-diagnostic contient un .highlight-box
    diag_slides = []
    diag_slide_highlight = []
    in_diag_slide = False
    current_slide_has_highlight = False
    for tag, classes, _ in parser.tab_elements.get("tab-diagnostic", []):
        cls_list = classes.split()
        if "slide" in cls_list and tag in ("div", "section"):
            if in_diag_slide:
                diag_slides.append(current_slide_has_highlight)
            in_diag_slide = True
            current_slide_has_highlight = False
        if in_diag_slide and "highlight-box" in cls_list:
            current_slide_has_highlight = True
    if in_diag_slide:
        diag_slides.append(current_slide_has_highlight)
    if diag_slides:
        missing = sum(1 for h in diag_slides if not h)
        ok = missing == 0
        results.append(("R43", f"SO WHAT dans chaque section Diagnostic : {len(diag_slides) - missing}/{len(diag_slides)} sections OK", ok))
    else:
        results.append(("R43", "SO WHAT : aucune section detectee dans l'onglet Diagnostic", None))

    # R44: Au moins 1 .micro-benchmark dans #tab-diagnostic
    has_micro = tab_has_class(parser, "tab-diagnostic", "micro-benchmark")
    results.append(("R44", "Au moins 1 micro-benchmark dans onglet Diagnostic", has_micro))

    # R45: Repetition density — same number appears > 6 times in visible text
    visible = full_text(parser)
    numbers = re.findall(r'\b\d[\d\s]*\d\b|\b\d{2,}\b', visible)
    normalized = [n.replace(' ', '') for n in numbers]
    if normalized:
        from collections import Counter
        counts = Counter(normalized)
        repeated = {n: c for n, c in counts.items() if c > 6}
        if repeated:
            top = sorted(repeated.items(), key=lambda x: -x[1])[:3]
            detail = ", ".join(f"{n} ({c}x)" for n, c in top)
            results.append(("R45", f"Repetition excessive : {detail}", False))
        else:
            results.append(("R45", "Densite repetition OK", True))
    else:
        results.append(("R45", "Densite repetition OK (aucun nombre multi-digit)", True))

    return results


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_results(layer1, layer2, layer3, layer4):
    fails = 0
    warns = 0
    passes = 0

    print("\n=== SLASHR Proposal Validator v2.0 ===\n")

    # Layer 1
    l1_pass = 0
    l1_fail = 0
    print("--- Layer 1 : Structural (PASS/FAIL) ---\n")
    for rule_id, desc, passed in layer1:
        if passed:
            print(f"  [PASS] {rule_id} — {desc}")
            l1_pass += 1
        else:
            print(f"  [FAIL] {rule_id} — {desc}")
            l1_fail += 1
    fails = l1_fail

    # Layer 2
    l2_pass = 0
    l2_warn = 0
    l2_manual = 0
    print("\n--- Layer 2 : Content (WARN) ---\n")
    for rule_id, desc, passed in layer2:
        if passed is None:
            print(f"  [MANUAL] {rule_id} — {desc}")
            l2_manual += 1
        elif passed:
            print(f"  [PASS] {rule_id} — {desc}")
            l2_pass += 1
        else:
            print(f"  [WARN] {rule_id} — {desc}")
            l2_warn += 1
    warns = l2_warn

    # Layer 3
    print("\n--- Layer 3 : Semantic (checklist manuelle) ---\n")
    for rule_id, question in layer3:
        print(f"  [ ] {rule_id} — {question}")

    # Layer 4
    l4_pass = 0
    l4_warn = 0
    l4_manual = 0
    print("\n--- Layer 4 : Quality Metrics (WARN) ---\n")
    for rule_id, desc, passed in layer4:
        if passed is None:
            print(f"  [MANUAL] {rule_id} — {desc}")
            l4_manual += 1
        elif passed:
            print(f"  [PASS] {rule_id} — {desc}")
            l4_pass += 1
        else:
            print(f"  [WARN] {rule_id} — {desc}")
            l4_warn += 1
    warns += l4_warn

    # Summary
    print(f"\n{'=' * 50}")
    print(f"Layer 1 : {l1_pass} PASS, {l1_fail} FAIL")
    print(f"Layer 2 : {l2_pass} PASS, {l2_warn} WARN, {l2_manual} MANUAL")
    print(f"Layer 3 : {len(layer3)} items a verifier manuellement")
    print(f"Layer 4 : {l4_pass} PASS, {l4_warn} WARN, {l4_manual} MANUAL")
    print(f"{'=' * 50}")

    if fails > 0:
        print(f"\nResultat : REJECT ({fails} FAIL)")
        print("Corriger les regles FAIL avant upload Drive.")
        return 1
    elif warns > 0:
        print(f"\nResultat : CONDITIONNEL ({warns} WARN)")
        print("Corriger les WARN recommande avant upload Drive.")
        return 0
    else:
        print(f"\nResultat : PASS")
        return 0


# ---------------------------------------------------------------------------
# NBP Pre-Validator (markdown structure checks)
# ---------------------------------------------------------------------------

def validate_nbp(filepath):
    """Validate a Narrative Blueprint (NBP) markdown file for structural correctness."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    results = []
    content_lower = content.lower()

    # NBP-1: 3 onglets presents
    tabs = ["onglet diagnostic", "onglet strategie", "onglet investissement"]
    missing_tabs = [t for t in tabs if t not in content_lower]
    if missing_tabs:
        results.append(("NBP-1", f"Onglets manquants : {', '.join(missing_tabs)}", False))
    else:
        results.append(("NBP-1", "3 onglets presents", True))

    # NBP-2: Chaque section Diagnostic a un champ "SO WHAT"
    diag_start = content_lower.find("onglet diagnostic")
    diag_end = content_lower.find("onglet strategie")
    if diag_start >= 0 and diag_end >= 0:
        diag_section = content[diag_start:diag_end]
        # Count sections (numbered lines like "1. " or "2. ")
        section_lines = re.findall(r'^\d+\.\s+', diag_section, re.MULTILINE)
        so_what_count = len(re.findall(r'SO\s*WHAT', diag_section, re.IGNORECASE))
        if len(section_lines) > 0 and so_what_count < len(section_lines):
            results.append(("NBP-2", f"SO WHAT manquants : {so_what_count}/{len(section_lines)} sections", False))
        elif len(section_lines) > 0:
            results.append(("NBP-2", f"SO WHAT dans chaque section ({so_what_count}/{len(section_lines)})", True))
        else:
            results.append(("NBP-2", "Aucune section numerotee detectee dans Diagnostic", None))
    else:
        results.append(("NBP-2", "Section Diagnostic non trouvee", False))

    # NBP-3: Pas de champ "Transition SLASHR"
    has_transition = bool(re.search(r'transition\s+slashr', content_lower))
    results.append(("NBP-3", "Pas de champ 'Transition SLASHR'", not has_transition))

    # NBP-4: Resume decisionnel : 6 items, chacun < 120 chars
    # Look for numbered list items (1. through 6.) after "resume" or "decisionnel"
    resume_match = re.search(r'(?:resume|decisionnel).*?(?=(?:board|---|\n\n[A-Z]))', content, re.IGNORECASE | re.DOTALL)
    if resume_match:
        resume_text = resume_match.group(0)
        bullets = re.findall(r'^\d+\.\s+(.+)$', resume_text, re.MULTILINE)
        long_bullets = [b for b in bullets if len(b.strip()) > 120]
        if len(bullets) != 6:
            results.append(("NBP-4", f"Resume decisionnel : {len(bullets)} bullets (attendu: 6)", len(bullets) == 6))
        elif long_bullets:
            results.append(("NBP-4", f"Resume decisionnel : {len(long_bullets)} bullets > 120 chars", False))
        else:
            results.append(("NBP-4", "Resume decisionnel : 6 bullets, tous <= 120 chars", True))
    else:
        results.append(("NBP-4", "Resume decisionnel non detecte", None))

    # NBP-5: HOOK_TYPE present
    has_hook_type = bool(re.search(r'HOOK_TYPE', content))
    results.append(("NBP-5", "HOOK_TYPE present", has_hook_type))

    # NBP-6: LAYOUT_MODE present
    has_layout_mode = bool(re.search(r'LAYOUT_MODE', content))
    results.append(("NBP-6", "LAYOUT_MODE present", has_layout_mode))

    # NBP-7: Deduplication — pas 2 sections avec le meme "Angle"
    angles = re.findall(r'Angle\s*:\s*(.+)', content)
    if angles:
        angles_lower = [a.strip().lower() for a in angles]
        seen = set()
        dupes = []
        for a in angles_lower:
            if a in seen:
                dupes.append(a)
            seen.add(a)
        if dupes:
            results.append(("NBP-7", f"Deduplication : angles dupliques ({', '.join(dupes[:2])})", False))
        else:
            results.append(("NBP-7", f"Deduplication : {len(angles)} angles distincts", True))
    else:
        results.append(("NBP-7", "Aucun champ Angle detecte", None))

    # Print results
    print(f"\n=== SLASHR NBP Pre-Validator ===\n")
    print(f"Fichier : {filepath}\n")
    fails = 0
    for rule_id, desc, passed in results:
        if passed is None:
            print(f"  [SKIP] {rule_id} — {desc}")
        elif passed:
            print(f"  [PASS] {rule_id} — {desc}")
        else:
            print(f"  [FAIL] {rule_id} — {desc}")
            fails += 1

    print(f"\n{'=' * 40}")
    if fails > 0:
        print(f"Resultat : {fails} FAIL — corriger avant de lancer la Pass 3.")
        return 1
    else:
        print("Resultat : PASS — structure NBP OK.")
        return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/validate_proposal.py <path_to_html>")
        print("       python3 tools/validate_proposal.py --nbp <path_to_nbp.md>")
        print("       python3 tools/validate_proposal.py .cache/deals/560/artifacts/PROPOSAL-*.html")
        sys.exit(1)

    # NBP pre-validation mode
    if sys.argv[1] == "--nbp":
        if len(sys.argv) < 3:
            print("Usage: python3 tools/validate_proposal.py --nbp <path_to_nbp.md>")
            sys.exit(1)
        nbp_path = sys.argv[2]
        if not os.path.isfile(nbp_path):
            print(f"Fichier introuvable : {nbp_path}")
            sys.exit(1)
        exit_code = validate_nbp(nbp_path)
        sys.exit(exit_code)

    filepath = sys.argv[1]

    # Handle glob patterns
    if "*" in filepath:
        import glob
        matches = glob.glob(filepath)
        if not matches:
            print(f"Aucun fichier trouve pour : {filepath}")
            sys.exit(1)
        filepath = matches[0]
        print(f"Fichier selectionne : {filepath}")

    if not os.path.isfile(filepath):
        print(f"Fichier introuvable : {filepath}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        html_raw = f.read()

    if len(html_raw) < 100:
        print(f"Fichier trop petit ({len(html_raw)} chars) — probablement pas une proposition valide.")
        sys.exit(1)

    # Parse
    parser = ProposalParser()
    try:
        parser.feed(html_raw)
    except Exception as e:
        print(f"Erreur de parsing HTML : {e}")
        sys.exit(1)

    # Validate
    layer1 = check_layer1(parser, html_raw)
    layer2 = check_layer2(parser, html_raw)
    layer3 = LAYER3_CHECKLIST
    layer4 = check_layer4(parser, html_raw)

    exit_code = print_results(layer1, layer2, layer3, layer4)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
