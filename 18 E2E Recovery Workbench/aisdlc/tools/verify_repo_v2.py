#!/usr/bin/env python3
"""Verify the v2 AISDLC repository package.

Checks structure, the generated Claude agents, the 72 active story cards, the
context package, the requirement set and the four current specify/plan runs.
No network, no questions.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAIL: list[str] = []
WARN: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        FAIL.append(message)


def warn(condition: bool, message: str) -> None:
    if not condition:
        WARN.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> None:
    required = [
        ".gitignore", ".mcp.json", "AGENTS.md", "CLAUDE.md",
        ".claude/agents/context-builder.md", ".claude/agents/context-updater.md",
        ".claude/agents/technical-specifier.md", ".claude/agents/implementation-planner.md",
        ".claude/agents/implementation-builder.md", ".claude/agents/compliance-reviewer.md",
        ".claude/commands/brd-builder.md", ".claude/commands/prd-builder.md",
        ".claude/commands/backlog-builder.md",
        ".github/agents/context-builder.agent.md", ".github/scripts/sync-claude-agents.mjs",
        ".github/contexts/project-context.md", ".github/contexts/domain-context.md",
        ".github/contexts/frontend-context.md", ".github/contexts/backend-context.md",
        ".github/contexts/testing-standards.md", ".github/contexts/backend-standards.md",
        ".github/contexts/frontend-standards.md", ".github/contexts/context-manifest.json",
        "requirement/Context_RecoveryWorkbench.md", "requirement/BRD_RecoveryWorkbench.md",
        "requirement/RecoveryWorkbench_Requirements.md",
        "requirement/Intake_Gap_Report_RecoveryWorkbench.md",
        "requirement/Traceability_Matrix.md",
        "docs/decisions/decision-register.md", "docs/open-items.md",
        "docs/increments/INDEX.md", "docs/increments/epics/EPIC-001-foundation-1.md",
        "docs/increments/epics/EPIC-002-foundation-2.md",
        "docs/retirements/story-retirement-register.md",
        "output/CONTEXT-20261116/agent-run-log.md",
        "output/EPIC1-STORY-MANIFEST.json",
        "output/INC-003-epic-1-RWB-E1-042/specify/spec.md",
        "output/INC-003-epic-1-RWB-E1-042/specify/compliance-validation.md",
        "output/INC-003-epic-1-RWB-E1-042/plan/plan.md",
        "output/INC-003-epic-1-RWB-E1-042/plan/tasks.md",
        "output/INC-004-epic-1-RWB-TE-002/specify/spec.md",
        "output/INC-004-epic-1-RWB-TE-002/specify/compliance-validation.md",
        "output/INC-004-epic-1-RWB-TE-002/plan/plan.md",
        "output/INC-004-epic-1-RWB-TE-002/plan/tasks.md",
        "output/INC-005-epic-1-RWB-TE-003/specify/spec.md",
        "output/INC-005-epic-1-RWB-TE-003/specify/compliance-validation.md",
        "output/INC-005-epic-1-RWB-TE-003/plan/plan.md",
        "output/INC-005-epic-1-RWB-TE-003/plan/tasks.md",
        "output/INC-003-epic-1-RWB-E1-042/implement/sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql",
        "output/INC-003-epic-1-RWB-E1-042/implement/evidence/migration-test-output.txt",
        "output/INC-002-epic-1-RWB-TE-001/specify/spec.md",
        "output/INC-002-epic-1-RWB-TE-001/plan/plan.md",
        "output/INC-002-epic-1-RWB-TE-001/implement/report.md",
        "output/INC-001-epic-1-RWB-E1-044/specify/spec.md",
        "output/INC-008-epic-1-RWB-E1-043/specify/spec.md",
        "output/_archive/epic1-specs-20261106/README.md",
    ]
    for rel in required:
        check((ROOT / rel).exists(), f"missing required file: {rel}")

    # Generated Claude agents are in sync.
    result = subprocess.run(
        ["node", ".github/scripts/sync-claude-agents.mjs", "--check"],
        cwd=ROOT, capture_output=True, text=True,
    )
    check(result.returncode == 0, "Claude agents are not in sync: " + (result.stderr or result.stdout).strip())

    # Story cards and manifest.
    manifest = json.loads(read(ROOT / "output/EPIC1-STORY-MANIFEST.json"))
    stories = manifest["groups"][0]["stories"]
    check(len(stories) == 72, f"expected 72 Epic 1 stories, found {len(stories)}")
    cards = sorted((ROOT / "docs/increments").glob("INC-*.md"))
    check(len(cards) == 72, f"expected 72 story cards, found {len(cards)}")
    keys = {s["key"] for s in stories}
    check("RWB-E1-042" in keys and "RWB-TE-001" in keys, "implemented stories missing from manifest")
    check("RWB-E1-069" in keys, "new ACE view story missing")
    check("RWB-E1-070" in keys and "RWB-E1-073" in keys, "new Temporal/Drools stories missing")
    for retired in ["RWB-E1-029", "RWB-TE-005", "RWB-E1-048", "RWB-E1-051"]:
        check(retired not in keys, f"retired story still active: {retired}")
    check(not list((ROOT / "docs/increments").glob("INC-*-RWB-E1-029.md")), "retired card E1-029 exists")
    check(not list((ROOT / "docs/increments").glob("INC-*-RWB-E1-048.md")), "retired card E1-048 exists")

    # Cards have the required sections and a unique RUN_ID.
    required_sections = ["## Identification", "## Scope", "## Reused approved artefacts",
                         "## Owners and approvals", "## Agents selected", "## Evidence links",
                         "## Card status"]
    run_ids = []
    for card in cards:
        text = read(card)
        for sec in required_sections:
            check(sec in text, f"{card.name}: missing section {sec}")
        m = re.search(r"\| RUN_ID \| `([^`]+)` \|", text)
        check(bool(m), f"{card.name}: missing RUN_ID")
        if m:
            run_ids.append(m.group(1))
            check(m.group(1) in card.name, f"{card.name}: RUN_ID mismatch")
    check(len(run_ids) == len(set(run_ids)), "duplicate RUN_IDs in cards")

    # Contexts.
    contexts = [".github/contexts/project-context.md", ".github/contexts/domain-context.md",
                ".github/contexts/frontend-context.md", ".github/contexts/backend-context.md",
                ".github/contexts/testing-standards.md", ".github/contexts/backend-standards.md",
                ".github/contexts/frontend-standards.md"]
    for rel in contexts:
        text = read(ROOT / rel)
        check(len(text) > 1500, f"{rel}: too short to be substantive")
        check("TBD" not in text, f"{rel}: contains TBD")
        check("N/A" in text or "Not applicable" in text or "not applicable" in text,
              f"{rel}: no N/A handling")
    project = read(ROOT / ".github/contexts/project-context.md")
    for term in ["D-RCV-35", "D-RCV-36", "recovery.v_ace_", "Temporal", "Drools", "72", "43", "93", "30"]:
        check(term in project, f"project context missing {term}")
    backend = read(ROOT / ".github/contexts/backend-context.md")
    for term in ["${recoverySchema}", "v_ace_", "Temporal", "Drools", "BND-6", "93 tables", "30 views"]:
        check(term in backend, f"backend context missing {term}")

    # Decision register and retirements.
    decisions = read(ROOT / "docs/decisions/decision-register.md")
    for term in ["D-RCV-35", "D-RCV-36", "D-RCV-51", "D-RCV-52", "superseded", "L-RCV-03"]:
        check(term in decisions, f"decision register missing {term}")
    retirements = read(ROOT / "docs/retirements/story-retirement-register.md")
    for term in ["RWB-E1-029", "RWB-TE-005", "RWB-E1-048", "RWB-E1-051", "RWB-E1-073"]:
        check(term in retirements, f"retirement register missing {term}")

    # Current specify and plan runs.
    for run in ["INC-003-epic-1-RWB-E1-042", "INC-002-epic-1-RWB-TE-001",
                "INC-004-epic-1-RWB-TE-002", "INC-005-epic-1-RWB-TE-003"]:
        base = ROOT / "output" / run
        spec = read(base / "specify/spec.md")
        plan = read(base / "plan/plan.md")
        check("## Change Scope Declaration" in spec, f"{run}: spec missing Change Scope Declaration")
        check("## Requirement-to-SPEC Logic Coverage" in spec, f"{run}: spec missing coverage table")
        check("## Unit Test Applicability" in spec, f"{run}: spec missing unit-test applicability")
        check("## Assumptions" in spec, f"{run}: spec missing assumptions")
        check("TBD" not in spec, f"{run}: spec contains TBD")
        check("## Plan approval preconditions" in plan, f"{run}: plan missing preconditions")
        check("## Status reporting" in plan, f"{run}: plan missing status reporting")
        check("PLAN_STATUS: SUCCESS" in plan, f"{run}: plan status is not SUCCESS")
        check("No question" in read(base / "specify/agent-run-log.md") or "No questions" in read(base / "specify/agent-run-log.md"),
              f"{run}: spec run log does not record the no-question rule")
        check("No question" in read(base / "plan/agent-run-log.md") or "No questions" in read(base / "plan/agent-run-log.md"),
              f"{run}: plan run log does not record the no-question rule")

    # Preserved implementation evidence.
    te = ROOT / "output/INC-002-epic-1-RWB-TE-001/implement"
    check((te / "report.md").exists(), "TE-001 implementation report missing")
    check((te / "backend/recoveryCoverageReport.xml").exists(), "TE-001 JaCoCo report missing")
    check((te / "frontend/coverage-summary.json").exists(), "TE-001 frontend coverage missing")
    e42 = ROOT / "output/INC-003-epic-1-RWB-E1-042/implement"
    check((e42 / "sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql").exists(), "E1-042 migration missing")
    check((e42 / "tests/test_migrations.sh").exists(), "E1-042 migration test missing")
    check((e42 / "evidence/migration-test-output.txt").exists(), "E1-042 evidence missing")
    sql = read(e42 / "sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql")
    check("${recoverySchema}" in sql, "E1-042 SQL does not use ${recoverySchema}")
    check("-- Story: RWB-E1-042" in sql, "E1-042 SQL missing story header")
    check("CREATE TABLE IF NOT EXISTS" in sql, "E1-042 SQL is not baseline-guarded")

    # Traceability.
    trace = read(ROOT / "requirement/Traceability_Matrix.md")
    rows = len(re.findall(r"^\| \d{3} \| `RWB-", trace, re.M))
    check(rows == 72, f"traceability matrix has {rows} story rows, expected 72")
    check("TRACEABILITY_STATUS: CURRENT" in trace, "traceability status is not CURRENT")

    # No stale D-RCV-47 claim in current files.
    for rel in ["AGENTS.md", "CLAUDE.md", ".github/contexts/backend-context.md",
                ".github/contexts/project-context.md", "docs/decisions/decision-register.md"]:
        text = read(ROOT / rel)
        if "D-RCV-47" in text:
            check("superseded" in text.lower() or "Superseded" in text,
                  f"{rel} mentions D-RCV-47 without marking it superseded")

    # Report.
    print(f"Checked {ROOT.name}")
    print(f"Story cards: {len(cards)}; traceability rows: {rows}; contexts: {len(contexts)}")
    if WARN:
        print(f"WARN: {len(WARN)}")
        for w in WARN:
            print("  -", w)
    if FAIL:
        print(f"FAIL: {len(FAIL)}")
        for f in FAIL:
            print("  -", f)
        sys.exit(1)
    print("PASS: structure, agents, contexts, stories, decisions, retirements, runs and evidence")


if __name__ == "__main__":
    main()
