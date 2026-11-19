#!/usr/bin/env python3
"""Verify the Recovery Workbench repository package."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "13 AI-First SDLC repository"
OUT = REPO / "output" / "VERIFICATION-20261104" / "verification-report.md"
CTX_FILES = [
    REPO / ".github" / "contexts" / "project-context.md",
    REPO / ".github" / "contexts" / "domain-context.md",
    REPO / ".github" / "contexts" / "frontend-context.md",
    REPO / ".github" / "contexts" / "backend-context.md",
    REPO / ".github" / "contexts" / "testing-standards.md",
    REPO / "requirement" / "Context_RecoveryWorkbench.md",
]
REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    ".github/contexts/project-context.md",
    ".github/contexts/domain-context.md",
    ".github/contexts/frontend-context.md",
    ".github/contexts/backend-context.md",
    ".github/contexts/testing-standards.md",
    "requirement/Context_RecoveryWorkbench.md",
    "requirement/BRD_RecoveryWorkbench.md",
    "requirement/RecoveryWorkbench_Requirements.md",
    "requirement/Intake_Gap_Report_RecoveryWorkbench.md",
    "requirement/Traceability_Matrix.md",
    "docs/increments/INDEX.md",
    "docs/increments/epics/EPIC-001-foundation-1.md",
    "docs/increments/epics/EPIC-001-tailoring.md",
    "docs/increments/epics/EPIC-002-foundation-2.md",
    "docs/increments/epics/EPIC-002-tailoring.md",
    "output/CONTEXT-20261104/agent-run-log.md",
    "output/INC-043-epic-1-RWB-E1-020/specify/spec.md",
    "output/INC-043-epic-1-RWB-E1-020/specify/compliance-validation.md",
    "output/INC-043-epic-1-RWB-E1-020/agent-run-log.md",
    "requirement/legacy/DOCUMENT_MAP.md",
    "requirement/legacy/_conversion-report.md",
    "requirement/legacy/_manifest.json",
]
SPEC_SECTIONS = [
    "## Change Scope Declaration",
    "## Requirement-to-SPEC Logic Coverage",
    "## Unit Test Applicability",
    "## Clarification Log",
    "## Status reporting",
]
CARD_SECTIONS = [
    "## Identification",
    "## Project type",
    "## Scope",
    "## Reused approved artefacts",
    "## Lifecycle tailoring",
    "## Owners and approvals",
    "## Agents selected",
    "## Risk, rollback and stop signals",
    "## Evidence links",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> None:
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append((name, ok, detail))

    for rel in REQUIRED_FILES:
        p = REPO / rel
        check(f"file exists: {rel}", p.exists(), "" if p.exists() else "missing")

    # CTX IDs
    ctx_all: dict[str, list[str]] = {}
    for p in CTX_FILES:
        if not p.exists():
            continue
        ids = re.findall(r"CTX-[A-Z]+-\d{3}", read(p))
        ctx_all[p.name] = ids
    project_ids = set(ctx_all.get("project-context.md", []))
    project_text = read(REPO / ".github" / "contexts" / "project-context.md")
    table_ids = re.findall(r"^\| (CTX-[A-Z]+-\d{3}) \|", project_text, flags=re.M)
    ctx_dupes = len(table_ids) - len(set(table_ids))
    check("project context has CTX IDs", len(project_ids) > 0, f"{len(project_ids)} unique")
    check("no duplicate CTX IDs in the project-context tables", ctx_dupes == 0,
          f"{ctx_dupes} duplicate table rows")

    # Matrix
    matrix = REPO / "requirement" / "Traceability_Matrix.md"
    matrix_text = read(matrix) if matrix.exists() else ""
    matrix_ctx = set(re.findall(r"^\| (CTX-[A-Z]+-\d{3}) \|", matrix_text, flags=re.M))
    excluded = {i for i in project_ids if i.startswith("CTX-TECH-") or i.startswith("CTX-GAP-")}
    missing_ctx = sorted(project_ids - matrix_ctx - excluded)
    check("all requirement CTX IDs are in the matrix", not missing_ctx,
          f"missing: {', '.join(missing_ctx[:10])}" if missing_ctx else f"{len(matrix_ctx)} matrix rows")
    check("CTX-TECH and CTX-GAP are intentionally outside the requirement matrix",
          len(excluded) > 0, f"{len(excluded)} excluded (technical context and gaps)")

    # Header columns
    header = next((l for l in matrix_text.splitlines() if l.startswith("| CTX ID |")), "")
    check("matrix has the 16 required columns", header.count("|") == 17, f"{header.count('|')} pipes")

    # Build sequence story keys
    build = REPO / "requirement" / "legacy" / "11-delivery-and-operations" / \
        "recovery-workbench-build-sequence-epic-1-and-epic-2-v4-xlsx.md"
    build_keys = set(re.findall(r"RWB-(?:E1|E2|TE)-\d{3}", read(build)))
    matrix_us = set(re.findall(r"US-(RWB-(?:E1|E2|TE)-\d{3})", matrix_text))
    missing_keys = sorted(build_keys - matrix_us)
    check("all build-sequence story keys are in the matrix", not missing_keys,
          f"missing: {', '.join(missing_keys[:10])}" if missing_keys else f"{len(build_keys)} keys")

    # Spec
    spec = REPO / "output" / "INC-043-epic-1-RWB-E1-020" / "specify" / "spec.md"
    spec_text = read(spec) if spec.exists() else ""
    for section in SPEC_SECTIONS:
        check(f"spec section: {section}", section in spec_text, "")
    spec_ids = re.findall(r"SPEC-RWB-E1-020-\d{3}", spec_text)
    check("spec has SPEC IDs", len(spec_ids) > 0, f"{len(set(spec_ids))} unique")
    check("spec declares UI/Logic/API scope",
          all(x in spec_text for x in ("UI In Scope", "Logic In Scope", "API In Scope")), "")
    check("spec declares design evidence status", "DESIGN_EVIDENCE_STATUS" in spec_text, "")
    check("spec declares clarification status", "CLARIFICATION_STATUS" in spec_text, "")
    check("spec has frontend and backend unit-test rows",
          "| Frontend |" in spec_text and "| Backend |" in spec_text, "")
    check("all clarifications are resolved",
          "OPEN" not in re.findall(r"\| CLAR-\d+ .*?\| (RESOLVED|OPEN) \|", spec_text),
          "no OPEN CLAR rows")

    # Compliance
    comp = REPO / "output" / "INC-043-epic-1-RWB-E1-020" / "specify" / "compliance-validation.md"
    comp_text = read(comp) if comp.exists() else ""
    check("compliance review has a status", "Overall status" in comp_text, "")
    check("compliance review has findings", "REVIEW-RWB-E1-020-001" in comp_text, "")

    # Epic increment cards
    for name in ("EPIC-001-foundation-1.md", "EPIC-002-foundation-2.md"):
        p = REPO / "docs" / "increments" / "epics" / name
        text = read(p) if p.exists() else ""
        for section in CARD_SECTIONS:
            check(f"{name} section: {section}", section in text, "")
    for name in ("EPIC-001-tailoring.md", "EPIC-002-tailoring.md"):
        p = REPO / "docs" / "increments" / "epics" / name
        text = read(p) if p.exists() else ""
        check(f"{name} has phase decisions", "## Phase decisions" in text, "")
        check(f"{name} has reuse records", "## Skip and reuse records" in text, "")

    # Story increment cards
    story_cards = sorted((REPO / "docs" / "increments").glob("INC-*-epic-1-RWB-*.md"))
    check("78 Epic 1 story increment cards", len(story_cards) == 78, f"{len(story_cards)} cards")
    card_names = [p.stem for p in story_cards]
    check("story increment card names are unique", len(set(card_names)) == len(card_names),
          f"{len(card_names) - len(set(card_names))} duplicates")
    index_text = read(REPO / "docs" / "increments" / "INDEX.md")
    index_rows = re.findall(r"^\| \d{3} \| `RWB-(?:E1|TE)-\d{3}` \|", index_text, flags=re.M)
    check("INDEX.md lists 78 story increments", len(index_rows) == 78, f"{len(index_rows)} rows")
    missing_runs = []
    bad_run_ids = []
    missing_sections = []
    for p in story_cards:
        text = read(p)
        if f"| RUN_ID | `{p.stem}` |" not in text:
            bad_run_ids.append(p.name)
        if not (REPO / "output" / p.stem / "specify").exists():
            missing_runs.append(p.stem)
        if any(section not in text for section in CARD_SECTIONS):
            missing_sections.append(p.name)
    check("every story card RUN_ID matches its card name", not bad_run_ids,
          ", ".join(bad_run_ids[:5]) if bad_run_ids else f"{len(story_cards)} cards")
    check("every story card has an output run folder", not missing_runs,
          ", ".join(missing_runs[:5]) if missing_runs else f"{len(story_cards)} runs")
    check("every story card has the template sections", not missing_sections,
          ", ".join(missing_sections[:5]) if missing_sections else f"{len(story_cards)} cards")
    old_cards = [name for name in ("INC-001-epic-1.md", "INC-001-tailoring.md",
                                   "INC-002-epic-2.md", "INC-002-tailoring.md")
                 if (REPO / "docs" / "increments" / name).exists()]
    check("old epic card names are retired", not old_cards, ", ".join(old_cards))

    # Conversion
    manifest = json.loads(read(REPO / "requirement" / "legacy" / "_manifest.json"))
    failures = [m for m in manifest if m.get("conversion") == "failed"]
    check("conversion has no failures", not failures, f"{len(failures)} failures")
    check("manifest has 411 entries", len(manifest) == 411, f"{len(manifest)} entries")
    check("manifest has 256 source files and 155 zip entries",
          len([m for m in manifest if m.get("kind") == "file"]) == 256 and
          len([m for m in manifest if m.get("kind") == "zip-entry"]) == 155,
          f"{len([m for m in manifest if m.get('kind') == 'file'])} files / "
          f"{len([m for m in manifest if m.get('kind') == 'zip-entry'])} zip entries")
    map_text = read(REPO / "requirement" / "legacy" / "DOCUMENT_MAP.md")
    map_rows = re.findall(r"^\| \d{2}-\d{3} \|", map_text, flags=re.M)
    check("document map has 411 rows", len(map_rows) == 411, f"{len(map_rows)} rows")
    check("document map reports no failures", "## Failures\n\nNone." in map_text, "")

    # Empty outputs
    tiny = []
    for p in REPO.rglob("*.md"):
        if "_csv" in p.parts or "legacy" in p.parts:
            continue
        if p.stat().st_size < 200:
            tiny.append(p.relative_to(REPO).as_posix())
    check("no tiny generated markdown outside the legacy corpus", not tiny,
          ", ".join(tiny[:5]) if tiny else "")

    # PII scan
    scan_files = list((REPO / ".github" / "contexts").glob("*.md")) + \
        list((REPO / "requirement").glob("*.md")) + \
        list((REPO / "docs").rglob("*.md")) + \
        list((REPO / "output").rglob("*.md")) + [REPO / "AGENTS.md", REPO / "README.md"]
    pii_hits: list[tuple[str, str]] = []
    for p in scan_files:
        if not p.exists():
            continue
        text = read(p)
        for pattern, label in ((r"\b\d{13}\b", "13-digit number"),
                               (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "email"),
                               (r"\b0\d{9}\b", "Thai phone")):
            if re.search(pattern, text):
                pii_hits.append((p.relative_to(REPO).as_posix(), label))
    check("no obvious PII patterns in generated docs", not pii_hits,
          "; ".join(f"{f}: {l}" for f, l in pii_hits[:5]))

    # Counts
    ctx_count = len(project_ids)
    summary = [
        ("Required files", len(REQUIRED_FILES)),
        ("Story increment cards", len(story_cards)),
        ("CTX IDs in project-context", ctx_count),
        ("CTX rows in matrix", len(matrix_ctx)),
        ("Build-sequence story keys", len(build_keys)),
        ("US rows in matrix", len(matrix_us)),
        ("Manifest entries", len(manifest)),
        ("Document map rows", len(map_rows)),
        ("Spec SPEC IDs", len(set(spec_ids))),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    failed = len(checks) - passed
    lines = [
        "# Verification report",
        "",
        f"Run: 2026-11-04",
        f"Checks: **{len(checks)}** · Passed: **{passed}** · Failed: **{failed}**",
        "",
        "## Summary",
        "",
        "| Measure | Value |",
        "|---|---:|",
    ]
    for name, value in summary:
        lines.append(f"| {name} | {value} |")
    lines += ["", "## Checks", "", "| Check | Result | Detail |", "|---|---|---|"]
    for name, ok, detail in checks:
        safe_detail = detail.replace("|", "\\|")
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {safe_detail} |")
    lines += ["", "## Result", ""]
    if failed == 0:
        lines.append("**PASS** — the package is internally consistent. The open items are the recorded")
        lines.append("gaps (GAP-001..020) and the `TBC` approvers, not verification failures.")
    else:
        lines.append(f"**FAIL** — {failed} check(s) need attention. See the table above.")
    lines += ["", "## What this verifies", "",
              "- Every required artifact exists.",
              "- The context package has unique CTX IDs and the requirement CTX IDs are in the matrix.",
              "- The matrix has the required 16 columns and every build-sequence story key.",
              "- The pilot spec (`INC-043`) has the required sections, unique SPEC IDs, both unit-test rows and no open clarification.",
              "- The pilot compliance review has a status and findings.",
              "- The increment structure has 2 epic cards, 2 tailoring records, 78 story cards and an INDEX;",
              "- Story card names and RUN_IDs match the output run folders.",
              "- The conversion has 411 entries, 0 failures and a 411-row map.",
              "- No obvious PII patterns in the generated docs.",
              "",
              "## What this does not verify", "",
              "- Spec-to-story AC alignment; the 15 stale or mismatched specs are listed in `docs/increments/INDEX.md`.",
              "- The accuracy of every converted table against the original binary file (spot checks only).",
              "- The truth of the source documents; it verifies that the package reflects them.",
              "- Implementation behaviour, API execution or test results; those need the ACE repository.",
              "- Named approvers; they are `TBC` by design (GAP-006)."]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Checks: {len(checks)}; passed: {passed}; failed: {failed}")
    if failed:
        for name, ok, detail in checks:
            if not ok:
                print(f"FAIL: {name} — {detail}")


if __name__ == "__main__":
    main()
