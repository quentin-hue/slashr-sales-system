#!/usr/bin/env python3
"""
SLASHR Proposal Validator — v1.1

Valide un HTML de proposition contre les 42 regles de validation.
- Layer 1 (Structural) : PASS/FAIL — echec = REJECT
- Layer 2 (Content) : WARN — correction recommandee
- Layer 3 (Semantic) : checklist affichee pour revue manuelle
- Layer 4 (Quality Metrics) : WARN — metriques de qualite redactionnelle

Usage:
    python3 tools/validate_proposal.py <path_to_html>
    python3 tools/validate_proposal.py .cache/deals/560/artifacts/PROPOSAL-*.html

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
        self.h2_order = []  # h2 texts in order within tab-strategie
        self.in_h2 = False
        self.h2_buffer = ""

        # R18: track <li> inside highlight-gradient in tab-livrables
        self.in_highlight_gradient_livrables = False
        self.highlight_gradient_depth = 0
        self.highlight_gradient_li_count = 0

        # Layer 4 quality metrics
        self.strat_paragraphs = []  # list of paragraph texts in tab-strategie
        self.strat_h2s = []  # list of h2 texts in tab-strategie
        self.in_p_strat = False
        self.p_strat_buffer = ""

        # R42: "Ce que cela implique" li tracking
        self.implique_detected = False  # text "ce que cela implique" seen
        self.in_implique_list = False  # inside the first ul/ol after detection
        self.implique_list_done = False  # first list already collected
        self.implique_lis = []
        self.in_implique_li = False
        self.implique_li_buffer = ""

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

        # Track h2 inside tab-strategie
        if tag == "h2" and self.current_tab == "tab-strategie":
            self.in_h2 = True
            self.h2_buffer = ""

        # R18: Track highlight-gradient in tab-livrables for bullet counting
        # Void elements (br, hr, img, etc.) don't have closing tags, so skip depth tracking
        void_elements = {'br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base',
                         'col', 'embed', 'param', 'source', 'track', 'wbr'}
        if "highlight-gradient" in classes.split() and self.current_tab == "tab-livrables":
            self.in_highlight_gradient_livrables = True
            self.highlight_gradient_depth = 1
        elif self.in_highlight_gradient_livrables and tag not in void_elements:
            self.highlight_gradient_depth += 1
            if tag == "li":
                self.highlight_gradient_li_count += 1

        # Track print button
        if "window.print" in str(attrs):
            self.has_print_button = True

        # Layer 4: Track <p> in tab-strategie for density metric
        if tag == "p" and self.current_tab == "tab-strategie" and "section-label" not in classes:
            self.in_p_strat = True
            self.p_strat_buffer = ""

        # R42: Track <li> in "Ce que cela implique" section
        if self.implique_detected and not self.implique_list_done:
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
        if self.in_highlight_gradient_livrables:
            self.highlight_gradient_depth -= 1
            if self.highlight_gradient_depth <= 0:
                self.in_highlight_gradient_livrables = False

        # Layer 4: close <p> tracking
        if tag == "p" and self.in_p_strat:
            self.in_p_strat = False
            if self.p_strat_buffer.strip():
                self.strat_paragraphs.append(self.p_strat_buffer.strip())

        # R42: close <li> and <ul>/<ol> in implique section
        if tag == "li" and self.in_implique_li:
            self.in_implique_li = False
            if self.implique_li_buffer.strip():
                self.implique_lis.append(self.implique_li_buffer.strip())
        if tag in ("ul", "ol") and self.in_implique_list:
            self.in_implique_list = False
            self.implique_list_done = True

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
        if self.in_p_strat:
            self.p_strat_buffer += data

        # R42: detect "Ce que cela implique" section and accumulate li text
        if self.current_tab == "tab-strategie" and "ce que cela implique" in data.lower():
            self.implique_detected = True
        if self.in_implique_li:
            self.implique_li_buffer += data


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

    # R5: 4 onglets non-vides
    required_tabs = ["tab-strategie", "tab-cas-clients", "tab-roi", "tab-livrables"]
    tabs_ok = all(
        tab_id in parser.tabs and len(parser.tabs[tab_id]) > 2
        for tab_id in required_tabs
    )
    missing = [t for t in required_tabs if t not in parser.tabs or len(parser.tabs.get(t, [])) <= 2]
    detail = f" (manquants/vides: {', '.join(missing)})" if missing else ""
    results.append(("R5", f"4 onglets non-vides{detail}", tabs_ok))

    # R14: Section S7 dans onglet Strategie
    strat_text = tab_text(parser, "tab-strategie").lower()
    has_s7 = tab_has_class(parser, "tab-strategie", "s7-grid") or \
             tab_has_class(parser, "tab-strategie", "s7-card") or \
             "s7-grid" in strat_text or "s7-card" in strat_text
    results.append(("R14", "Section S7 dans onglet Strategie", has_s7))

    # R16: Exactement 1 PRIMARY
    primary_count = parser.data_states.count("primary")
    results.append(("R16", f"Exactement 1 PRIMARY (trouve: {primary_count})", primary_count == 1))

    # R18: Resume decisionnel <= 6 bullets
    has_gradient = tab_has_class(parser, "tab-livrables", "highlight-gradient")
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
        r'\b(jour[s]?[\s\-]homme|TJM|AMOA|etude lexicale|plan de? redirections|recette)\b',
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

    # R31: Accordion FAQ dans Livrables
    has_accordion = tab_has_class(parser, "tab-livrables", "accordion")
    results.append(("R31", "Accordion FAQ dans onglet Livrables", has_accordion))

    # R35: "Prochaine etape" dans Livrables
    has_next = "prochaine" in tab_text(parser, "tab-livrables").lower() and \
               "tape" in tab_text(parser, "tab-livrables").lower()
    results.append(("R35", "\"Prochaine etape\" dans Livrables", has_next))

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

    # R38: Pricing cards exclusives a Livrables (pas dans ROI)
    has_pricing_in_roi = tab_has_class(parser, "tab-roi", "pricing") or \
                         tab_has_class(parser, "tab-roi", "pricing-grid")
    results.append(("R38", "Pricing cards absentes de l'onglet ROI", not has_pricing_in_roi))

    # R39: ETV vs trafic — only flag if ETV is directly mislabeled as visits
    etv_mislabeled = False
    strat_lower = tab_text(parser, "tab-strategie").lower()
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

    # R28a: Investissement avec .recommended + cout inaction
    has_recommended = "recommended" in " ".join(parser.all_classes)
    livr_lower = tab_text(parser, "tab-livrables").lower()
    cout_inaction = "inaction" in livr_lower and ("cout" in livr_lower or "coute" in livr_lower)
    r28a_ok = has_recommended and cout_inaction
    detail_parts = []
    if not has_recommended:
        detail_parts.append(".recommended absent")
    if not cout_inaction:
        detail_parts.append("cout inaction absent")
    detail = f" ({', '.join(detail_parts)})" if detail_parts else ""
    results.append(("R28a", f"Investissement : .recommended + cout inaction{detail}", r28a_ok))

    # R30: Coherence Phase 1 ↔ Phase 2
    has_phase1 = "phase 1" in livr_lower or "mission structurante" in livr_lower
    has_phase2 = "phase 2" in livr_lower or "accompagnement mensuel" in livr_lower
    has_pricing = tab_has_class(parser, "tab-livrables", "pricing") or \
                  tab_has_class(parser, "tab-livrables", "pricing-grid") or \
                  tab_has_class(parser, "tab-livrables", "pricing-card")
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
    strat = tab_text(parser, "tab-strategie").lower()
    livr = tab_text(parser, "tab-livrables").lower()

    # R20: Trajectoire 90j M1/M2/M3
    has_m1m2m3 = all(f"m{i}" in livr or f"m{i}" in strat for i in [1, 2, 3])
    results.append(("R20", "Trajectoire 90j avec M1/M2/M3", has_m1m2m3))

    # R22: "Ce que cela implique"
    has_implies = "ce que cela implique" in strat
    results.append(("R22", "Section \"Ce que cela implique\" presente", has_implies))

    # R23: "Nous recommandons"
    has_reco = "nous recommandons" in strat
    results.append(("R23", "\"Nous recommandons\" dans la decision", has_reco))

    # R24: "Decision strategique"
    has_decision = "decision strategique" in strat or "décision stratégique" in strat
    results.append(("R24", "Section \"Decision strategique\" presente", has_decision))

    # R25: Sequence Diagnostic → S7 → Implications → Decision → 90j
    sequence_markers = [
        ("diagnostic", "diagnostic" in strat or "lecture strategique" in strat),
        ("s7", "s7" in strat or tab_has_class(parser, "tab-strategie", "s7-grid")),
        ("implications", "ce que cela implique" in strat),
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

    # R28b: Cout inaction avec impacts chiffres
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

    # R40: Densite de donnees dans l'onglet Strategie
    # >= 50% des paragraphes contiennent au moins 1 chiffre
    paragraphs = parser.strat_paragraphs
    if paragraphs:
        has_number = sum(1 for p in paragraphs if re.search(r'\d', p))
        ratio = has_number / len(paragraphs)
        pct = int(ratio * 100)
        ok = ratio >= 0.5
        results.append(("R40", f"Densite donnees onglet Strategie : {pct}% paragraphes avec chiffre (seuil: 50%)", ok))
    else:
        results.append(("R40", "Densite donnees : aucun paragraphe detecte dans l'onglet Strategie", False))

    # R41: Specificite des titres h2 dans tab-strategie
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
        results.append(("R41", "Specificite titres : aucun h2 dans l'onglet Strategie", False))

    # R42: Triplet "Ce que cela implique" — 3 <li>, le 3e contient un chiffre (projection)
    lis = parser.implique_lis
    if lis:
        count_ok = len(lis) == 3
        third_has_number = len(lis) >= 3 and bool(re.search(r'\d', lis[2]))
        ok = count_ok and third_has_number
        detail = f"{len(lis)} li"
        if len(lis) >= 3:
            detail += f", 3e li {'contient' if third_has_number else 'NE contient PAS'} un chiffre"
        results.append(("R42", f"Triplet 'Ce que cela implique' : {detail}", ok))
    else:
        results.append(("R42", "Section 'Ce que cela implique' non detectee", None))

    return results


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_results(layer1, layer2, layer3, layer4):
    fails = 0
    warns = 0
    passes = 0

    print("\n=== SLASHR Proposal Validator v1.1 ===\n")

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
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/validate_proposal.py <path_to_html>")
        print("       python3 tools/validate_proposal.py .cache/deals/560/artifacts/PROPOSAL-*.html")
        sys.exit(1)

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
