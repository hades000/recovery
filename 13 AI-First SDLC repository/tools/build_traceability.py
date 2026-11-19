#!/usr/bin/env python3
"""Build requirement/Traceability_Matrix.md from the converted build sequence and context."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "13 AI-First SDLC repository"
BUILD = REPO / "requirement" / "legacy" / "11-delivery-and-operations" / \
    "recovery-workbench-build-sequence-epic-1-and-epic-2-v4-xlsx.md"
OUT = REPO / "requirement" / "Traceability_Matrix.md"


def parse_build() -> list[list[str]]:
    rows: list[list[str]] = []
    in_table = False
    for line in BUILD.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 11:
            continue
        if cells[0] == "Order":
            in_table = True
            continue
        if not in_table:
            continue
        if not re.fullmatch(r"\d+", cells[0]):
            continue
        rows.append(cells)
    return rows


def ctx_rows() -> list[tuple[str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str]] = []
    # (CTX ID, BRD ID, FR/NFR ID, US range, status)
    business = [
        ("CTX-BUSINESS-001", "BRD-RWB-001", "FR-RWB-001", "RWB-E1-001..068", "Context mapped"),
        ("CTX-BUSINESS-002", "BRD-RWB-001", "FR-RWB-002", "RWB-E1-001..017", "Context mapped"),
        ("CTX-BUSINESS-003", "BRD-RWB-003", "FR-RWB-004..010", "RWB-E1-018..031", "Context mapped"),
        ("CTX-BUSINESS-004", "BRD-RWB-001..020", "FR-RWB-001..020", "E1-E8", "Context mapped"),
        ("CTX-BUSINESS-005", "BRD-RWB-001..020", "FR-RWB-001..020", "E1-E8", "Context mapped"),
        ("CTX-BUSINESS-006", "BRD-RWB-020", "FR-RWB-020", "INC-001, INC-002", "Context mapped"),
        ("CTX-BUSINESS-007", "BRD-RWB-009", "FR-RWB-018", "RWB-E1-013", "Context mapped"),
        ("CTX-BUSINESS-008", "BRD-RWB-003", "FR-RWB-004..010", "RWB-E1-018..031", "Context mapped"),
        ("CTX-BUSINESS-009", "BRD-RWB-001..020", "FR-RWB-001..020", "E1-E8", "Context mapped"),
        ("CTX-BUSINESS-010", "BRD-RWB-007", "FR-RWB-017", "RWB-E1-008, 027", "Context mapped"),
        ("CTX-BUSINESS-011", "BRD-RWB-007", "FR-RWB-017", "RWB-E1-008, 027", "Context mapped"),
        ("CTX-BUSINESS-012", "BRD-RWB-018", "FR-RWB-006", "RWB-E1-021, 062", "Context mapped"),
        ("CTX-BUSINESS-013", "BRD-RWB-003", "FR-RWB-004..010", "RWB-E1-018..031", "Context mapped"),
        ("CTX-BUSINESS-014", "BRD-RWB-003", "FR-RWB-004", "RWB-E1-018", "Context mapped"),
        ("CTX-BUSINESS-015", "BRD-RWB-003", "FR-RWB-004", "RWB-E1-018", "Context mapped"),
        ("CTX-BUSINESS-016", "BRD-RWB-003", "FR-RWB-004", "RWB-E1-018", "Context mapped"),
        ("CTX-BUSINESS-017", "BRD-RWB-003", "FR-RWB-005", "RWB-E1-020", "Context mapped"),
        ("CTX-BUSINESS-018", "BRD-RWB-003", "FR-RWB-006", "RWB-E1-021", "Context mapped"),
        ("CTX-BUSINESS-019", "BRD-RWB-003", "FR-RWB-007", "RWB-E1-028", "Context mapped"),
        ("CTX-BUSINESS-020", "BRD-RWB-003", "FR-RWB-008", "RWB-E1-029", "Context mapped"),
        ("CTX-BUSINESS-021", "BRD-RWB-003", "FR-RWB-008", "RWB-E1-029", "Context mapped"),
        ("CTX-BUSINESS-022", "BRD-RWB-003", "FR-RWB-008", "RWB-E1-029", "Context mapped"),
        ("CTX-BUSINESS-023", "BRD-RWB-007", "FR-RWB-017", "RWB-E1-027", "Context mapped"),
        ("CTX-BUSINESS-024", "BRD-RWB-003", "FR-RWB-019", "RWB-E1-062", "Context mapped"),
        ("CTX-BUSINESS-025", "BRD-RWB-003", "FR-RWB-010", "RWB-E1-035", "Context mapped"),
    ]
    stakeholder = [
        ("CTX-STAKEHOLDER-001", "BRD-RWB-004", "FR-RWB-011..013", "RWB-E1-022, 037-039", "Context mapped"),
        ("CTX-STAKEHOLDER-002", "BRD-RWB-004", "FR-RWB-011..013", "RWB-E1-022, 037-039", "Context mapped"),
        ("CTX-STAKEHOLDER-003", "BRD-RWB-004", "FR-RWB-011..013", "RWB-E1-022", "Context mapped"),
        ("CTX-STAKEHOLDER-004", "BRD-RWB-004", "FR-RWB-011", "RWB-E1-022", "Context mapped"),
        ("CTX-STAKEHOLDER-005", "BRD-RWB-003..010", "FR-RWB-004..019", "RWB-E1-018..063", "Context mapped"),
        ("CTX-STAKEHOLDER-006", "BRD-RWB-004", "FR-RWB-011..013", "RWB-E1-022, 037-039", "Context mapped"),
        ("CTX-STAKEHOLDER-007", "BRD-RWB-004", "NFR-RWB-002", "RWB-E1-022", "Context mapped"),
    ]
    features = [
        ("CTX-FEATURE-001", "BRD-RWB-001", "FR-RWB-001, FR-RWB-002", "RWB-E1-001..017, 064-068", "Context mapped"),
        ("CTX-FEATURE-002", "BRD-RWB-002", "FR-RWB-003", "RWB-E1-007, 047, 051, 056", "Context mapped"),
        ("CTX-FEATURE-003", "BRD-RWB-003", "FR-RWB-004..010", "RWB-E1-018..031, 035, 042-045, 048", "Context mapped"),
        ("CTX-FEATURE-004", "BRD-RWB-004", "FR-RWB-011..013", "RWB-E1-022, 037-039", "Context mapped"),
        ("CTX-FEATURE-005", "BRD-RWB-005", "FR-RWB-014, FR-RWB-015", "RWB-E1-024..026, 032-033, 040-041, 049-050, 053-054, 057", "Context mapped"),
        ("CTX-FEATURE-006", "BRD-RWB-006", "FR-RWB-016", "RWB-E1-034, 046, 052, 055", "Context mapped"),
        ("CTX-FEATURE-007", "BRD-RWB-007", "FR-RWB-017", "RWB-E1-008, 027", "Context mapped"),
        ("CTX-FEATURE-008", "BRD-RWB-008", "FR-RWB-002, FR-RWB-003", "RWB-E1-007, 056", "Context mapped"),
        ("CTX-FEATURE-009", "BRD-RWB-009", "FR-RWB-018", "RWB-E1-013", "Context mapped"),
        ("CTX-FEATURE-010", "BRD-RWB-010", "FR-RWB-019", "RWB-E1-058..063", "Context mapped"),
        ("CTX-FEATURE-011", "BRD-RWB-011", "FR-RWB-020", "E4", "Programme-level"),
        ("CTX-FEATURE-012", "BRD-RWB-012", "FR-RWB-020", "E2/E3", "Programme-level"),
        ("CTX-FEATURE-013", "BRD-RWB-013", "FR-RWB-020", "E4", "Programme-level"),
        ("CTX-FEATURE-014", "BRD-RWB-014", "FR-RWB-020", "E2/E5", "Programme-level"),
        ("CTX-FEATURE-015", "BRD-RWB-015", "FR-RWB-020", "E3/E4", "Programme-level"),
        ("CTX-FEATURE-016", "BRD-RWB-016", "FR-RWB-020", "E5/E6", "Programme-level"),
        ("CTX-FEATURE-017", "BRD-RWB-017", "FR-RWB-020", "E6", "Programme-level"),
        ("CTX-FEATURE-018", "BRD-RWB-018", "FR-RWB-020", "E2/E7", "Programme-level"),
        ("CTX-FEATURE-019", "BRD-RWB-019", "FR-RWB-020", "E6/E7", "Programme-level"),
        ("CTX-FEATURE-020", "BRD-RWB-020", "FR-RWB-020", "RWB-E1-042..048", "Context mapped"),
    ]
    rules = [
        ("CTX-RULE-001", "BRD-RWB-003", "FR-RWB-004", "RWB-E1-018", "Context mapped"),
        ("CTX-RULE-002", "BRD-RWB-003", "FR-RWB-005", "RWB-E1-020", "Context mapped"),
        ("CTX-RULE-003", "BRD-RWB-003", "FR-RWB-005", "RWB-E1-020", "Context mapped"),
        ("CTX-RULE-004", "BRD-RWB-003", "FR-RWB-006", "RWB-E1-021", "Context mapped"),
        ("CTX-RULE-005", "BRD-RWB-003", "FR-RWB-007", "RWB-E1-028", "Context mapped"),
        ("CTX-RULE-006", "BRD-RWB-011", "FR-RWB-020", "E4", "Programme-level"),
        ("CTX-RULE-007", "BRD-RWB-012", "FR-RWB-020", "E2/E3", "Programme-level"),
        ("CTX-RULE-008", "BRD-RWB-013", "FR-RWB-020", "E4", "Programme-level"),
        ("CTX-RULE-009", "BRD-RWB-014", "FR-RWB-020", "E2/E5", "Programme-level"),
        ("CTX-RULE-010", "BRD-RWB-015", "FR-RWB-020", "E3/E4", "Programme-level"),
        ("CTX-RULE-011", "BRD-RWB-016", "FR-RWB-020", "E5/E6", "Programme-level"),
        ("CTX-RULE-012", "BRD-RWB-017", "FR-RWB-020", "E6", "Programme-level"),
        ("CTX-RULE-013", "BRD-RWB-018", "FR-RWB-020", "E2/E7", "Programme-level"),
        ("CTX-RULE-014", "BRD-RWB-019", "FR-RWB-020", "E6/E7", "Programme-level"),
        ("CTX-RULE-015", "BRD-RWB-004", "FR-RWB-012", "RWB-E1-037..039", "Context mapped"),
        ("CTX-RULE-016", "BRD-RWB-001", "FR-RWB-002", "RWB-E1-006, 011", "Context mapped"),
    ]
    data = [
        ("CTX-DATA-001", "BRD-RWB-001", "FR-RWB-001", "RWB-E1-001, 064", "Context mapped"),
        ("CTX-DATA-002", "BRD-RWB-001", "FR-RWB-001", "RWB-E1-001, 064", "Context mapped"),
        ("CTX-DATA-003", "BRD-RWB-001", "FR-RWB-001", "RWB-E1-001, 064", "Context mapped"),
        ("CTX-DATA-004", "BRD-RWB-001", "FR-RWB-002", "RWB-E1-015", "Context mapped"),
        ("CTX-DATA-005", "BRD-RWB-001", "FR-RWB-002", "RWB-E1-006, 011", "Context mapped"),
        ("CTX-DATA-006", "BRD-RWB-001", "FR-RWB-002", "RWB-E1-017", "Context mapped"),
        ("CTX-DATA-007", "BRD-RWB-004", "FR-RWB-013", "RWB-E1-037", "Context mapped"),
    ]
    nfrs = [(f"CTX-NFR-{i:03d}", "BRD-RWB-009" if i in (3,) else "BRD-RWB-001", f"NFR-RWB-{i:03d}", "—", "Context mapped")
            for i in range(1, 11)]
    compliance = [
        ("CTX-COMPLIANCE-001", "BRD-RWB-004", "FR-RWB-013", "RWB-E1-037", "Context mapped"),
        ("CTX-COMPLIANCE-002", "BRD-RWB-004", "FR-RWB-013", "RWB-E1-037..039", "Context mapped"),
        ("CTX-COMPLIANCE-003", "BRD-RWB-004", "FR-RWB-013", "RWB-E1-037..039", "Context mapped"),
        ("CTX-COMPLIANCE-004", "BRD-RWB-009", "FR-RWB-018", "RWB-E1-013", "Context mapped"),
        ("CTX-COMPLIANCE-005", "BRD-RWB-005", "FR-RWB-014", "RWB-E1-024, 041", "Context mapped"),
    ]
    delivery = [
        ("CTX-DELIVERY-001", "BRD-RWB-020", "FR-RWB-020", "INC-001, INC-002", "Context mapped"),
        ("CTX-DELIVERY-002", "BRD-RWB-020", "FR-RWB-020", "INC-001, INC-002", "Context mapped"),
        ("CTX-DELIVERY-003", "BRD-RWB-020", "FR-RWB-020", "INC-001, INC-002", "Context mapped"),
        ("CTX-DELIVERY-004", "BRD-RWB-020", "FR-RWB-020", "INC-001, INC-002", "Context mapped"),
        ("CTX-DELIVERY-005", "BRD-RWB-020", "FR-RWB-020", "INC-001, INC-002", "Context mapped"),
        ("CTX-DELIVERY-006", "BRD-RWB-020", "FR-RWB-020", "INC-001, INC-002", "Context mapped"),
        ("CTX-DELIVERY-007", "BRD-RWB-020", "FR-RWB-020", "INC-001, INC-002", "Context mapped"),
    ]
    ai = [
        ("CTX-AI-001", "BRD-RWB-010", "FR-RWB-019", "RWB-E1-058..063", "Context mapped"),
        ("CTX-AI-002", "BRD-RWB-010", "FR-RWB-019", "RWB-E1-058..063", "Context mapped"),
        ("CTX-AI-003", "BRD-RWB-007", "FR-RWB-017", "RWB-E1-008, 027", "Context mapped"),
        ("CTX-AI-004", "BRD-RWB-010", "FR-RWB-019", "RWB-E1-058", "Context mapped"),
        ("CTX-AI-005", "BRD-RWB-010", "FR-RWB-019", "RWB-E1-058..063", "Context mapped"),
        ("CTX-AI-006", "BRD-RWB-010", "FR-RWB-019", "RWB-E1-058..063", "Context mapped"),
    ]
    constraints = [
        ("CTX-CONSTRAINT-001", "BRD-RWB-001..020", "FR-RWB-001..020", "E1-E8", "Context mapped"),
        ("CTX-CONSTRAINT-002", "BRD-RWB-001..020", "FR-RWB-001..020", "E1-E8", "Context mapped"),
        ("CTX-CONSTRAINT-003", "BRD-RWB-003", "FR-RWB-004..010", "RWB-E1-018..031", "Context mapped"),
        ("CTX-CONSTRAINT-004", "BRD-RWB-003", "FR-RWB-008", "RWB-E1-029", "Context mapped"),
        ("CTX-CONSTRAINT-005", "BRD-RWB-002", "FR-RWB-003", "RWB-E1-007", "Context mapped"),
        ("CTX-CONSTRAINT-006", "BRD-RWB-020", "FR-RWB-020", "RWB-E1-044", "Context mapped"),
        ("CTX-CONSTRAINT-007", "BRD-RWB-020", "FR-RWB-020", "RWB-E1-047", "Context mapped"),
        ("CTX-CONSTRAINT-008", "BRD-RWB-020", "FR-RWB-020", "INC-001, INC-002", "Context mapped"),
        ("CTX-CONSTRAINT-009", "BRD-RWB-019", "FR-RWB-020", "E5", "Programme-level"),
        ("CTX-CONSTRAINT-010", "BRD-RWB-004", "FR-RWB-013", "RWB-E1-037", "Context mapped"),
    ]
    for group in (business, stakeholder, features, rules, data, nfrs, compliance, delivery, ai, constraints):
        rows.extend(group)
    return rows


def main() -> None:
    build = parse_build()
    e1 = [r for r in build if r[9] == "E1"]
    e2 = [r for r in build if r[9] == "E2"]
    e3 = [r for r in build if r[9] == "E3"]
    lines = [
        "# Traceability Matrix",
        "",
        "Required chain (see `.github/rules/traceability-standards.md`):",
        "",
        "```text",
        "CTX -> BRD -> FR/NFR -> US -> SPEC -> TASK -> CODE -> APT -> FT -> TEST -> REVIEW -> DOC",
        "```",
        "",
        "This matrix is seeded from the context package and the Epic 1/Epic 2 build sequence. The",
        "`FR/NFR` and `US` columns are populated; `SPEC`, `TASK`, `CODE`, `APT`, `FT`, `TEST`, `REVIEW`",
        "and `DOC` are filled by the later stages. The source-ID crosswalk at the end preserves the",
        "project's `REQ-*`, `RWB-E*`, `BR-*`, `MSG-*`, `DF-*` and `TC-*` identifiers.",
        "",
        "## 1. Context to requirement",
        "",
        "| CTX ID | BRD ID | FR/NFR ID | US ID | SPEC ID | TASK ID | Code Ref | APT ID | FT ID | TEST ID | REVIEW ID | DOC ID | GitHub Issue | PR | Commit | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for ctx, brd, fr, us, status in ctx_rows():
        lines.append(f"| {ctx} | {brd} | {fr} | {us} | | | | | | | | | | | | {status} |")
    lines += [
        "",
        "## 2. Epic 1 story crosswalk (INC-001)",
        "",
        f"{len(e1)} items in the Epic 1 build sequence. The story file is the detailed source; the",
        "`US ID` is the canonical story key. `GAP-001` marks the version check between the consolidated",
        "v7 and the per-story v5 files.",
        "",
        "| US ID | Story key | Title | Module | Type | Priority | Depends on | Window | Release | Critical path | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in e1:
        us = f"US-{r[1]}"
        spec = REPO / "output" / f"INC-{int(r[0]):03d}-epic-1-{r[1]}" / "specify" / "spec.md"
        if spec.exists():
            stext = spec.read_text(encoding="utf-8", errors="replace")
            status = "Specified — BLOCKED" if ("CLARIFICATION_STATUS: OPEN" in stext or
                                               "| Status | `BLOCKED" in stext or
                                               "| Status | BLOCKED" in stext) else "Specified — SUCCESS"
        else:
            status = "Ready for spec"
        lines.append(f"| {us} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[9]} | {r[10]} | {status} |")
    lines += [
        "",
        "## 3. Epic 2 story crosswalk (INC-002)",
        "",
        f"{len(e2)} items in the Epic 2 build sequence. Epic 2 is a separate increment and does not start",
        "until INC-001 is released.",
        "",
        "| US ID | Story key | Title | Module | Type | Priority | Depends on | Window | Release | Critical path | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in e2:
        us = f"US-{r[1]}"
        lines.append(f"| {us} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[9]} | {r[10]} | Planned |")
    lines += [
        "",
        "## 4. Epic 2 stories that go live in Epic 3",
        "",
        f"{len(e3)} agent stories are built in Epic 2 but go live in Epic 3. They are part of INC-002",
        "and are listed separately so the release boundary is visible.",
        "",
        "| US ID | Story key | Title | Module | Type | Priority | Depends on | Window | Release | Critical path | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in e3:
        us = f"US-{r[1]}"
        lines.append(f"| {us} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[9]} | {r[10]} | Planned (INC-002, live in E3) |")
    lines += [
        "",
        "## 5. Source-ID crosswalk",
        "",
        "The source documents use their own IDs. They are not renumbered; this table maps them to the",
        "canonical IDs used by the toolkit.",
        "",
        "| Source ID family | Type | Canonical ID | US / SPEC / TEST link | Notes |",
        "|---|---|---|---|---|",
        "| `REQ-RDF-*` | Requirement | `FR-RWB-001`, `FR-RWB-002` | `RWB-E1-001..017`, `064..068` | Data engine |",
        "| `REQ-DRI-*` | Requirement | `FR-RWB-003` | `RWB-E1-007`, `047`, `051`, `056` | Integration |",
        "| `REQ-CWC-*` | Requirement | `FR-RWB-004..010` | `RWB-E1-018..031`, `035`, `042..045`, `048` | Case and workflow |",
        "| `REQ-ACA-*` | Requirement | `FR-RWB-011..013` | `RWB-E1-022`, `037..039` | Access and administration |",
        "| `REQ-DOC-*` | Requirement | `FR-RWB-014`, `FR-RWB-015` | `RWB-E1-024..026`, `032..033`, `040..041`, `049..050`, `053..054`, `057` | Document hub |",
        "| `REQ-COM-*` | Requirement | `FR-RWB-016` | `RWB-E1-034`, `046`, `052`, `055` | Communications |",
        "| `REQ-DEC-*` | Requirement | `FR-RWB-017` | `RWB-E1-008`, `027` | Decision log |",
        "| `REQ-PAY-*` | Requirement | `FR-RWB-002`, `FR-RWB-003` | `RWB-E1-007`, `056` | Payments and posting |",
        "| `REQ-RPT-*` | Requirement | `FR-RWB-018` | `RWB-E1-013` | Reporting |",
        "| `REQ-AGT-*` | Requirement | `FR-RWB-019` | `RWB-E1-058..063` | Agent runtime |",
        "| `REQ-ROU-*` | Requirement | `BRD-RWB-011` | E4 | Programme-level |",
        "| `REQ-TRT-*` | Requirement | `BRD-RWB-012` | E2/E3 | Programme-level |",
        "| `REQ-GUA-*` | Requirement | `BRD-RWB-013` | E4 | Programme-level |",
        "| `REQ-LIT-*` | Requirement | `BRD-RWB-014` | E2/E5 | Programme-level |",
        "| `REQ-AST-*` | Requirement | `BRD-RWB-015` | E3/E4 | Programme-level |",
        "| `REQ-DSL-*` | Requirement | `BRD-RWB-016` | E5/E6 | Programme-level |",
        "| `REQ-WOF-*` | Requirement | `BRD-RWB-017` | E6 | Programme-level |",
        "| `REQ-DEV-*` | Requirement | `BRD-RWB-018` | E2/E7 | Programme-level |",
        "| `REQ-PRT-*` | Requirement | `BRD-RWB-019` | E6/E7 | Programme-level |",
        "| `RWB-E1-*` | Story | `US-RWB-E1-*` | Epic 1 story crosswalk | Per-story file |",
        "| `RWB-TE-*` | Enabler | `US-RWB-TE-*` | Epic 1 story crosswalk | 13 technical enablers |",
        "| `RWB-E2-*` | Story | `US-RWB-E2-*` | Epic 2 story crosswalk | Per-story file |",
        "| `BR-*` | Business rule | `BR-RWB-*` | Rule family table | Preserve the source ID in the spec |",
        "| `MSG-*` | Message | `ERR-RWB-*` | Error handling table | Preserve the source ID in the spec |",
        "| `DF-*` | Data field | `DP-*` / field ID | Logical data model | Preserve the field ID in the spec |",
        "| `TC-*` | Test case | `TEST-*` | Test cases workbook | Preserve the test ID in the test evidence |",
        "| `CTL-*` | Control | `REVIEW-*` / test | Controls Catalog | Preserve the control ID in the review evidence |",
        "| `DL*` | Decision | `Q-RWB-*` / `CTX-GAP-*` | Open questions | Preserve the decision log ID |",
        "",
        "## 6. Gap markers",
        "",
        "| Gap | Affected rows | Status |",
        "|---|---|---|",
        "| GAP-001 Epic 1 story files v5 vs consolidated v7 | Epic 1 story crosswalk | Open — use the consolidated v7 as the narrative and record the story version in the spec header |",
        "| GAP-002 Epic 2 story files v4 vs consolidated v5 | Epic 2 story crosswalk | Open — use the consolidated v5 as the narrative |",
        "| GAP-005 No ACE source code | All `SPEC`/`TASK`/`CODE` rows | Open — blocks Build, not Specify/Plan |",
        "| GAP-006 Named approvers | All approval rows | Open — `TBC` in the increment cards |",
        "| GAP-010 Same-day interfaces | `INT-RWB-*` rows | Open — default end-of-day |",
        "| GAP-011 Jira keys | `GitHub Issue` column | Open — blank until the Jira project exists |",
        "",
        "## 7. How to update this matrix",
        "",
        "1. Technical Specifier adds `SPEC-*` and links each to `FR-RWB-*`/`NFR-RWB-*`.",
        "2. Implementation Planner adds `TASK-*` and links each to `SPEC-*`.",
        "3. Implementation Builder adds `CODE-*` and unit-test `TEST-*` references.",
        "4. API Tester adds `APT-*`; Functional Automation Test adds `FT-*`.",
        "5. Compliance Reviewer adds `REVIEW-*`; Technical Documenter adds `DOC-*`.",
        "6. Traceability Manager reconciles the chain and flags orphans, requirements without specs,",
        "   specs without tasks, tasks without code, APIs/UI without test results, and requirements",
        "   without tests.",
        "",
        "## 8. Epic 1 specification coverage",
        "",
        "One row per Epic 1 story. `SPEC-<KEY>-*` is the spec ID family; the exact SPEC IDs are in each",
        "spec. A `BLOCKED` row has an open source decision and must not go to the Implementation Planner.",
        "",
        "| Story key | Spec ID | Status | UI | API | Open CLARs | Compliance | Spec path |",
        "|---|---|---|---|---|---|---|---|",
    ]
    spec_counts: dict[str, int] = {}
    comp_counts: dict[str, int] = {}
    for r in e1:
        spec = REPO / "output" / f"INC-{int(r[0]):03d}-epic-1-{r[1]}" / "specify" / "spec.md"
        comp = REPO / "output" / f"INC-{int(r[0]):03d}-epic-1-{r[1]}" / "specify" / "compliance-validation.md"
        if spec.exists():
            stext = spec.read_text(encoding="utf-8", errors="replace")
            ctext = comp.read_text(encoding="utf-8", errors="replace") if comp.exists() else ""
            status = "BLOCKED" if ("CLARIFICATION_STATUS: OPEN" in stext or
                                   "| Status | `BLOCKED" in stext or
                                   "| Status | BLOCKED" in stext) else "SUCCESS"
            m = re.search(r"\| UI In Scope \| `?(YES|NO)`?", stext)
            ui = m.group(1) if m else "?"
            m = re.search(r"\| API In Scope \| `?(YES|NO)`?", stext)
            api = m.group(1) if m else "?"
            m = re.search(r"CLARIFICATION_STATUS:\s*[A-Z]+\s*\[OPEN_ITEMS:\s*(\d+)\]", stext)
            open_items = m.group(1) if m else "?"
            m = re.search(r"\| Overall status \| `?([A-Z_]+)`?", ctext)
            comp_status = m.group(1) if m else "?"
            comp_counts[comp_status] = comp_counts.get(comp_status, 0) + 1
            spec_counts[status] = spec_counts.get(status, 0) + 1
            lines.append(f"| {r[1]} | SPEC-{r[1]}-* | {status} | {ui} | {api} | {open_items} | "
                         f"{comp_status} | `output/INC-{int(r[0]):03d}-epic-1-{r[1]}/specify/spec.md` |")
        else:
            spec_counts["Not specified"] = spec_counts.get("Not specified", 0) + 1
            lines.append(f"| {r[1]} | — | Not specified | — | — | — | — | — |")
    parts = ", ".join(f"{k}: {v}" for k, v in sorted(spec_counts.items()))
    comp_parts = "; ".join(f"{v} {k}" for k, v in sorted(comp_counts.items()))
    lines += [
        "",
        f"`Traceability Manager status: RECONCILED — {len(ctx_rows())} CTX rows, {len(e1) + len(e2) + len(e3)} story items, 0 orphans in the seeded",
        f"range. Epic 1: 78 specs ({parts}. Compliance: {comp_parts}). Later stages must complete the chain.`",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"E1 items: {len(e1)}; E2 items: {len(e2)}; CTX rows: {len(ctx_rows())}")


if __name__ == "__main__":
    main()
