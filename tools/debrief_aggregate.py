#!/usr/bin/env python3
"""
SLASHR Debrief Aggregator — Analyse les debriefs structures et produit des patterns.

Usage: python3 tools/debrief_aggregate.py

Input: .cache/deals/*/debrief.json
Output: .cache/patterns_report.md + .cache/debrief_warnings.md
"""

import json
import glob
import os
from collections import Counter, defaultdict
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, ".cache")
DEALS_DIR = os.path.join(CACHE_DIR, "deals")


def load_debriefs():
    """Load all debrief.json files."""
    debriefs = []
    pattern = os.path.join(DEALS_DIR, "*", "debrief.json")
    for path in sorted(glob.glob(pattern)):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            debriefs.append(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"WARN: impossible de lire {path}: {e}")
    return debriefs


def safe_rate(wins, total):
    """Return win rate as percentage, or None if total is 0."""
    if total == 0:
        return None
    return round(100 * wins / total, 1)


def group_win_rate(debriefs, key):
    """Compute win rate grouped by a given key."""
    groups = defaultdict(lambda: {"won": 0, "lost": 0, "total": 0})
    for d in debriefs:
        val = d.get(key)
        if val is None:
            continue
        result = d.get("result", "").lower()
        groups[val]["total"] += 1
        if result == "won":
            groups[val]["won"] += 1
        elif result == "lost":
            groups[val]["lost"] += 1
    return dict(groups)


def combo_win_rate(debriefs):
    """Compute win rate for (arc_used, tone_profile, scenario_proposed) combos."""
    combos = defaultdict(lambda: {"won": 0, "lost": 0, "total": 0})
    for d in debriefs:
        arc = d.get("arc_used", "?")
        tone = d.get("tone_profile", "?")
        scenario = d.get("scenario_proposed", "?")
        key = f"{arc} + {tone} + {scenario}"
        result = d.get("result", "").lower()
        combos[key]["total"] += 1
        if result == "won":
            combos[key]["won"] += 1
        elif result == "lost":
            combos[key]["lost"] += 1
    return dict(combos)


def collect_objections(debriefs):
    """Collect all objections from closer feedback."""
    objections = []
    for d in debriefs:
        feedback = d.get("closer_feedback", {})
        objs = feedback.get("unanticipated_objections", [])
        if isinstance(objs, list):
            objections.extend(objs)
    return Counter(objections)


def avg_budget(debriefs, result_filter):
    """Average budget_proposed for a given result."""
    values = [
        d["budget_proposed"]
        for d in debriefs
        if d.get("result", "").lower() == result_filter
        and d.get("budget_proposed") is not None
    ]
    if not values:
        return None
    return round(sum(values) / len(values))


def format_group_stats(groups, min_for_pct=3, total_debriefs=0):
    """Format grouped stats as markdown lines."""
    lines = []
    sorted_groups = sorted(groups.items(), key=lambda x: x[1]["total"], reverse=True)
    for name, stats in sorted_groups:
        won = stats["won"]
        total = stats["total"]
        if total_debriefs >= min_for_pct and total > 0:
            rate = safe_rate(won, total)
            lines.append(f"- **{name}** : {rate}% win rate ({won}/{total} deals)")
        else:
            lines.append(f"- **{name}** : {won} won, {stats['lost']} lost sur {total} deals")
    return lines


def generate_patterns_report(debriefs):
    """Generate .cache/patterns_report.md."""
    n = len(debriefs)
    won = sum(1 for d in debriefs if d.get("result", "").lower() == "won")
    lost = sum(1 for d in debriefs if d.get("result", "").lower() == "lost")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Rapport Patterns — SLASHR Debriefs",
        "",
        f"*Genere le {now} — {n} debriefs analyses*",
        "",
        "---",
        "",
        "## Vue d'ensemble",
        "",
    ]

    if n >= 3:
        lines.append(f"- **Total deals** : {n}")
        lines.append(f"- **Win rate global** : {safe_rate(won, won + lost)}% ({won} won / {lost} lost)")
    else:
        lines.append(f"- **Total deals** : {n}")
        lines.append(f"- Won : {won}, Lost : {lost}")
        lines.append("")
        lines.append("*Moins de 3 debriefs — donnees brutes, pas de pourcentages.*")

    # Budget moyen
    avg_won = avg_budget(debriefs, "won")
    avg_lost = avg_budget(debriefs, "lost")
    lines.append("")
    lines.append("## Budget propose moyen")
    lines.append("")
    if avg_won is not None:
        lines.append(f"- Deals won : **{avg_won:,} EUR**/mois".replace(",", " "))
    else:
        lines.append("- Deals won : pas de donnees")
    if avg_lost is not None:
        lines.append(f"- Deals lost : **{avg_lost:,} EUR**/mois".replace(",", " "))
    else:
        lines.append("- Deals lost : pas de donnees")

    # Win rate par arc
    lines.append("")
    lines.append("## Win rate par arc narratif")
    lines.append("")
    arc_groups = group_win_rate(debriefs, "arc_used")
    lines.extend(format_group_stats(arc_groups, total_debriefs=n))

    # Win rate par tone
    lines.append("")
    lines.append("## Win rate par tone profile")
    lines.append("")
    tone_groups = group_win_rate(debriefs, "tone_profile")
    lines.extend(format_group_stats(tone_groups, total_debriefs=n))

    # Win rate par scenario
    lines.append("")
    lines.append("## Win rate par scenario propose")
    lines.append("")
    scenario_groups = group_win_rate(debriefs, "scenario_proposed")
    lines.extend(format_group_stats(scenario_groups, total_debriefs=n))

    # Combinaisons
    lines.append("")
    lines.append("## Correlations (arc + tone + scenario)")
    lines.append("")
    combos = combo_win_rate(debriefs)
    if n >= 3:
        sorted_combos = sorted(
            combos.items(),
            key=lambda x: (safe_rate(x[1]["won"], x[1]["total"]) or 0, x[1]["total"]),
            reverse=True,
        )
        for name, stats in sorted_combos:
            rate = safe_rate(stats["won"], stats["total"])
            lines.append(f"- **{name}** : {rate}% ({stats['won']}/{stats['total']})")
    else:
        for name, stats in combos.items():
            lines.append(f"- **{name}** : {stats['won']} won, {stats['lost']} lost sur {stats['total']}")

    # Objections
    lines.append("")
    lines.append("## Objections non anticipees (par frequence)")
    lines.append("")
    objections = collect_objections(debriefs)
    if objections:
        for obj, count in objections.most_common():
            lines.append(f"- \"{obj}\" ({count}x)")
    else:
        lines.append("- Aucune objection enregistree")

    # Auto-analyse summary
    lines.append("")
    lines.append("## Auto-analyse — distribution")
    lines.append("")
    for field in ["diagnostic_accuracy", "arc_fit", "roi_accuracy", "pricing_fit"]:
        counter = Counter()
        for d in debriefs:
            aa = d.get("auto_analysis", {})
            val = aa.get(field)
            if val:
                counter[val] += 1
        if counter:
            parts = ", ".join(f"{k}: {v}" for k, v in counter.most_common())
            label = field.replace("_", " ").title()
            lines.append(f"- **{label}** : {parts}")

    # Deals detail
    lines.append("")
    lines.append("## Detail par deal")
    lines.append("")
    lines.append("| Deal | Entreprise | Resultat | Arc | Tone | Scenario | Budget |")
    lines.append("|------|-----------|----------|-----|------|----------|--------|")
    for d in debriefs:
        deal_id = d.get("deal_id", "?")
        company = d.get("company", "?")
        result = d.get("result", "?")
        arc = d.get("arc_used", "?")
        tone = d.get("tone_profile", "?")
        scenario = d.get("scenario_proposed", "?")
        budget = d.get("budget_proposed")
        budget_str = f"{budget:,} EUR".replace(",", " ") if budget else "?"
        lines.append(f"| {deal_id} | {company} | {result} | {arc} | {tone} | {scenario} | {budget_str} |")

    lines.append("")
    return "\n".join(lines)


def generate_warnings(debriefs):
    """Generate .cache/debrief_warnings.md."""
    n = len(debriefs)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Warnings actifs (generes par /debrief)",
        "",
        f"*Mis a jour le {now} — base: {n} debriefs*",
        "",
        "> Ce fichier est lu par Pass 2 de /prepare pour injecter des warnings contextuels.",
        "",
        "---",
        "",
    ]

    # Arc warnings
    lines.append("## Arcs narratifs")
    lines.append("")
    arc_groups = group_win_rate(debriefs, "arc_used")
    for arc, stats in sorted(arc_groups.items(), key=lambda x: x[1]["total"], reverse=True):
        won = stats["won"]
        total = stats["total"]
        if total == 0:
            continue
        if n >= 3 and total >= 2:
            rate = safe_rate(won, total)
            if rate >= 60:
                lines.append(f"- **{arc}** : {rate}% win rate ({won}/{total} deals) — privilegier pour deals similaires")
            elif rate <= 30:
                lines.append(f"- **{arc}** : {rate}% win rate ({won}/{total} deals) — ATTENTION: sous-performance, envisager un arc alternatif")
            else:
                lines.append(f"- **{arc}** : {rate}% win rate ({won}/{total} deals)")
        else:
            lines.append(f"- **{arc}** : {won} won / {total} deals")

    # Tone warnings
    lines.append("")
    lines.append("## Tone profiles")
    lines.append("")
    tone_groups = group_win_rate(debriefs, "tone_profile")
    for tone, stats in sorted(tone_groups.items(), key=lambda x: x[1]["total"], reverse=True):
        won = stats["won"]
        total = stats["total"]
        if total == 0:
            continue
        if n >= 3 and total >= 2:
            rate = safe_rate(won, total)
            lines.append(f"- **{tone}** : {rate}% win rate ({won}/{total} deals)")
        else:
            lines.append(f"- **{tone}** : {won} won / {total} deals")

    # Objection warnings
    lines.append("")
    lines.append("## Objections recurrentes")
    lines.append("")
    objections = collect_objections(debriefs)
    if objections:
        for obj, count in objections.most_common():
            if count >= 2:
                lines.append(f"- \"{obj}\" ({count} fois) — pre-empter dans la FAQ investissement")
            else:
                lines.append(f"- \"{obj}\" ({count} fois) — surveiller")
    else:
        lines.append("- Aucune objection recurrente")

    # Pricing warnings
    lines.append("")
    lines.append("## Pricing")
    lines.append("")
    pricing_counter = Counter()
    for d in debriefs:
        aa = d.get("auto_analysis", {})
        pf = aa.get("pricing_fit")
        if pf:
            pricing_counter[pf] += 1
    if pricing_counter:
        for label, count in pricing_counter.most_common():
            if label == "TROP_HAUT" and count >= 2:
                lines.append(f"- Pricing juge TROP HAUT {count} fois — ajuster le scenario vers le bas ou renforcer la justification ROI")
            elif label == "TROP_BAS" and count >= 2:
                lines.append(f"- Pricing juge TROP BAS {count} fois — opportunite d'upsell detectee")
            else:
                lines.append(f"- {label.replace('_', ' ')} : {count} deals")
    else:
        lines.append("- Pas de donnees pricing")

    # Scenario warnings
    lines.append("")
    lines.append("## Scenarios")
    lines.append("")
    scenario_groups = group_win_rate(debriefs, "scenario_proposed")
    for scenario, stats in sorted(scenario_groups.items(), key=lambda x: x[1]["total"], reverse=True):
        won = stats["won"]
        total = stats["total"]
        if total == 0:
            continue
        if n >= 3 and total >= 2:
            rate = safe_rate(won, total)
            if rate >= 60:
                lines.append(f"- **{scenario}** : {rate}% win rate ({won}/{total}) — scenario performant")
            elif rate <= 30:
                lines.append(f"- **{scenario}** : {rate}% win rate ({won}/{total}) — revoir le positionnement")
            else:
                lines.append(f"- **{scenario}** : {rate}% win rate ({won}/{total})")
        else:
            lines.append(f"- **{scenario}** : {won} won / {total} deals")

    # Combo anti-patterns
    lines.append("")
    lines.append("## Anti-patterns (combinaisons a eviter)")
    lines.append("")
    combos = combo_win_rate(debriefs)
    found_antipattern = False
    if n >= 3:
        for name, stats in combos.items():
            total = stats["total"]
            won = stats["won"]
            if total >= 2 and won == 0:
                lines.append(f"- **{name}** : 0% win rate ({total} deals) — eviter cette combinaison")
                found_antipattern = True
    if not found_antipattern:
        lines.append("- Aucun anti-pattern detecte (donnees insuffisantes)")

    lines.append("")
    return "\n".join(lines)


def main():
    debriefs = load_debriefs()

    if not debriefs:
        print("Aucun debrief.json trouve dans .cache/deals/*/")
        return

    print(f"{len(debriefs)} debriefs trouves.")

    # Ensure .cache exists
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Generate reports
    report = generate_patterns_report(debriefs)
    report_path = os.path.join(CACHE_DIR, "patterns_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Rapport patterns: {report_path}")

    warnings = generate_warnings(debriefs)
    warnings_path = os.path.join(CACHE_DIR, "debrief_warnings.md")
    with open(warnings_path, "w", encoding="utf-8") as f:
        f.write(warnings)
    print(f"Warnings: {warnings_path}")


if __name__ == "__main__":
    main()
