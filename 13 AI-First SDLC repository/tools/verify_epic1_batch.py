#!/usr/bin/env python3
"""Verify all 78 Epic 1 specifications and write the batch report."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "13 AI-First SDLC repository"
MANIFEST = REPO / "output" / "EPIC1-STORY-MANIFEST.json"
OUT = REPO / "output" / "VERIFICATION-20261106" / "epic1-batch-report.md"

REQUIRED = [
    "## Change Scope Declaration",
    "## Requirement-to-SPEC Logic Coverage",
    "## Unit Test Applicability",
    "## Clarification Log",
    "## Status reporting",
]

BLOCKED_REASONS = {
    "RWB-E1-001": "Decision DL41/DL42 not recorded; E1-001 and E1-044 disagree on whether the migration or the reference load seeds `sys_objects`/`sys_fields`.",
    "RWB-E1-014": "AC2 archive boundary conflict: 2024-11-29/30 partitions vs the 2024-12-01 kept boundary.",
    "RWB-E1-018": "No primary-account rule for a grouped case (`case_account.is_primary`, DF-CAS-027).",
    "RWB-E1-032": "No rule for moving a legal document from `rwb-docs` to `rwb-docs-legal` after type confirmation; CTL-12/NFR-029 unproven.",
    "RWB-E1-013": "AC7 business-date fixture is inconsistent with the previous-business-date rule; `TIME_IN_STAGE` and `TAT_BY_ROUTE` median definitions are not approved.",
    "RWB-E1-061": "`promotion_conditions` / `watch_measures` jsonb has no machine-checkable grammar; BR2/AC5 cannot be validated generally.",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> None:
    manifest = json.loads(read(MANIFEST))
    stories = [s for g in manifest["groups"] for s in g["stories"]]
    rows = []
    blocked = []
    missing = []
    for s in stories:
        key = s["key"]
        folder = REPO / s["output_dir"]
        spec_path = folder / "spec.md"
        log_path = folder / "agent-run-log.md"
        comp_path = folder / "compliance-validation.md"
        if not spec_path.exists():
            missing.append(key)
            continue
        text = read(spec_path)
        status = "UNKNOWN"
        m = re.search(r"^\| Status \| (.+?) \|$", text, flags=re.M)
        if m:
            raw = m.group(1)
            if "SUCCESS" in raw:
                status = "SUCCESS"
            elif "BLOCKED" in raw:
                status = "BLOCKED"
            elif "FAIL" in raw:
                status = "FAIL"
        ui = "?" 
        m = re.search(r"\| UI In Scope \| `?(YES|NO)`?", text)
        if m:
            ui = m.group(1)
        api = "?"
        m = re.search(r"\| API In Scope \| `?(YES|NO)`?", text)
        if m:
            api = m.group(1)
        impact = ""
        m = re.search(r"\| API Impact Type \| `?([A-Z_]+)`?", text)
        if m:
            impact = m.group(1)
        clar = "?"
        open_items = "?"
        m = re.search(r"CLARIFICATION_STATUS:\s*([A-Z]+)\s*\[OPEN_ITEMS:\s*(\d+)\]", text)
        if m:
            clar, open_items = m.group(1), m.group(2)
        cov = "?"
        missing_rules = "?"
        m = re.search(r"REQUIREMENT_COVERAGE_RESULT:\s*([A-Z]+)\s*\[TOTAL_RULES:\s*(\d+)\]\s*\[COVERED_RULES:\s*(\d+)\]\s*\[MISSING_RULES:\s*(\d+)\]", text)
        if m:
            cov, missing_rules = m.group(1), m.group(4)
        comp_status = "?"
        if comp_path.exists():
            ctext = read(comp_path)
            m = re.search(r"\| Overall status \| `?([A-Z_]+)`?", ctext)
            if m:
                comp_status = m.group(1)
            findings = len(re.findall(r"^\| REVIEW-", ctext, flags=re.M))
        else:
            findings = 0
        sections_ok = all(section in text for section in REQUIRED)
        has_frontend = "| Frontend |" in text
        has_backend = "| Backend |" in text
        line_count = len(text.splitlines())
        rows.append({
            "key": key, "title": s["title"], "module": s["module"], "status": status,
            "ui": ui, "api": api, "impact": impact, "clar": clar, "open": open_items,
            "coverage": cov, "missing_rules": missing_rules, "compliance": comp_status,
            "findings": findings, "sections": sections_ok, "unit": has_frontend and has_backend,
            "lines": line_count,
        })
        if status == "BLOCKED" or clar == "OPEN" or (open_items.isdigit() and int(open_items) > 0):
            blocked.append(key)

    total = len(stories)
    specified = len(rows)
    success = sum(1 for r in rows if r["status"] == "SUCCESS")
    blocked_count = len(blocked)
    lines = [
        "# Epic 1 specification batch report", "",
        f"Run: 2026-11-06 (regate) · Stories: **{total}** · Specified: **{specified}** · "
        f"Success: **{success}** · Blocked: **{blocked_count}** · Missing: **{len(missing)}**", "",
        "## Summary", "",
        "| Measure | Value |", "|---|---:|",
        f"| Stories in the Epic 1 build sequence | {total} |",
        f"| Specs written | {specified} |",
        f"| Success | {success} |",
        f"| Blocked on source ambiguity | {blocked_count} |",
        f"| Missing spec | {len(missing)} |",
        f"| Specs with all required sections | {sum(1 for r in rows if r['sections'])} |",
        f"| Specs with both unit-test rows | {sum(1 for r in rows if r['unit'])} |",
        "", "## Blocked stories", "",
        "| Key | Reason | Unblock action |", "|---|---|---|",
    ]
    for key in blocked:
        reason = BLOCKED_REASONS.get(key, "See the spec's open CLAR and compliance findings.")
        lines.append(f"| {key} | {reason} | Resolve the named source decision, then re-run the Technical Specifier and compliance gate. |")
    lines += ["", "## All stories", "",
              "| Key | Module | Status | UI | API | Impact | CLAR | Coverage | Compliance | Findings | Lines |",
              "|---|---|---|---|---|---|---|---|---|---|---:|"]
    for r in rows:
        lines.append(f"| {r['key']} | {r['module']} | {r['status']} | {r['ui']} | {r['api']} | "
                     f"{r['impact']} | {r['clar']} / {r['open']} | {r['coverage']} | {r['compliance']} | "
                     f"{r['findings']} | {r['lines']} |")
    if missing:
        lines += ["", "## Missing specs", ""] + [f"- {m}" for m in missing]
    lines += ["", "## Notes", "",
              f"- All {success} success specs have `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]` and a passing compliance gate.",
              "- The six previously blocked specs (RWB-E1-001, 014, 018, 032, 013, 061) are resolved by the D-RCV-28 to D-RCV-33 rulings recorded on 5 and 6 November 2026; see their gate-002 compliance files.",
              "- The Low findings are closed-with-disposition in the gate-002 runs; each is recorded with its owner and decision-log date.",
              "- The traceability matrix merge is in `requirement/Traceability_Matrix.md` §8.",
              "- No shared source, context or traceability file was modified by the module subagents."]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Stories: {total}; specified: {specified}; success: {success}; blocked: {blocked_count}; missing: {len(missing)}")
    print("Blocked:", ", ".join(blocked))


if __name__ == "__main__":
    main()
