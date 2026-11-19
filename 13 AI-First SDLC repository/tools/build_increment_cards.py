#!/usr/bin/env python3
"""Build Epic 1 story-level increment cards and INDEX.md.

The story-to-run mapping comes from output/EPIC1-STORY-MANIFEST.json. The
story scope comes from the current per-story file, not from a stale spec.
The epic-level records live in docs/increments/epics/ and are shared.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "output" / "EPIC1-STORY-MANIFEST.json"
INCREMENTS = ROOT / "docs" / "increments"
EPICS = INCREMENTS / "epics"

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

APPROVAL_GATES = [
    ("Intake approval", "Product Owner"),
    ("Context readiness", "Forward Deployed Engineer"),
    ("Requirements approval (BRD / PRD)", "Product Owner, FDA"),
    ("Design and architecture approval", "Forward Deployed Architect"),
    ("Backlog and specification approval", "Product Owner"),
    ("Plan approval", "Forward Deployed Architect"),
    ("Task approval", "Forward Deployed Engineer"),
    ("Pull request approval (code review)", "Forward Deployed Engineer"),
    ("Quality and security gate", "FDA, Quality Engineer, Security"),
    ("Release readiness", "Forward Deployed Engineer"),
    ("Deployment approval", "Product Owner / PM"),
    ("Operate and learn review", "Ops / System Manager"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def section(text: str, number: int) -> str:
    m = re.search(rf"^##\s*{number}\.\s+.*$", text, re.M)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^##\s*\d+\.\s+", text[start:], re.M)
    end = start + nxt.start() if nxt else len(text)
    return text[start:end].strip()


def first_paragraph(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    parts = re.split(r"\n\s*\n", text, maxsplit=1)
    return " ".join(parts[0].split())


def bullets(text: str) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            out.append(m.group(1).strip())
    return out


def table_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        if cells[0] in ("Item", "Field", "ID", "Question", "Test", "Who"):
            continue
        rows.append(cells)
    return rows


def metadata(text: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for line in text.splitlines()[:40]:
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] not in ("Item", "Field", "---"):
            meta[cells[0]] = cells[1]
    return meta


def norm_ac(value: str) -> str:
    m = re.search(r"(\d+)", value)
    return f"AC{int(m.group(1))}" if m else value.strip()


def ac_key(value: str) -> int:
    m = re.search(r"(\d+)", value)
    return int(m.group(1)) if m else 0


def story_acs(text: str) -> tuple[list[tuple[str, str]], bool]:
    sec = section(text, 7)
    if "No business acceptance criteria" in sec:
        return [], True
    acs: list[tuple[str, str]] = []
    for line in sec.splitlines():
        m = re.match(r"^\s{0,4}Scenario:\s*(AC\s*\d+)\s*(.*)$", line, re.I)
        if m:
            acs.append((norm_ac(m.group(1)), m.group(2).strip()))
    return acs, not acs


def ac_gaps(acs: list[tuple[str, str]]) -> list[int]:
    nums = sorted({ac_key(a) for a, _ in acs if ac_key(a)})
    if not nums:
        return []
    return [n for n in range(1, max(nums) + 1) if n not in nums]


def spec_info(run_id: str, current_acs: set[str]) -> dict[str, str]:
    spec_path = ROOT / "output" / run_id / "specify" / "spec.md"
    comp_path = ROOT / "output" / run_id / "specify" / "compliance-validation.md"
    spec_text = read(spec_path) if spec_path.exists() else ""
    comp_text = read(comp_path) if comp_path.exists() else ""

    def field(name: str) -> str:
        m = re.search(rf"^\|\s*{re.escape(name)}\s*\|\s*([^|]+?)\s*\|", spec_text, re.M)
        return m.group(1).strip().strip("`") if m else ""

    def first_token(value: str) -> str:
        value = value.replace("`", "").strip()
        return value.split()[0] if value.split() else ""

    status = first_token(field("Status"))
    ui = first_token(field("UI In Scope")) or "?"
    api = first_token(field("API In Scope")) or "?"
    impact = first_token(field("API Impact Type")) or "?"
    change_type = first_token(field("Change Type")) or "?"

    comp_status = ""
    m = re.search(r"^\|\s*Overall status\s*\|\s*([^|]+?)\s*\|", comp_text, re.M)
    if m:
        comp_status = m.group(1).strip().replace("`", "")

    spec_acs = {norm_ac(x) for x in re.findall(r"\bAC\s*\d{1,2}\b", spec_text, re.I)}
    extra = sorted(spec_acs - current_acs, key=ac_key)

    if extra and "BLOCKED" in status.upper():
        spec_status = f"BLOCKED + STALE — spec maps {', '.join(extra)} not in the current story"
    elif extra:
        spec_status = f"STALE — spec maps {', '.join(extra)} not in the current story"
    elif "BLOCKED" in status.upper():
        spec_status = "BLOCKED — see spec Clarification Log"
    elif status:
        spec_status = f"{status} — spec matches the current story ACs"
    else:
        spec_status = "NOT FOUND — no spec"

    return {
        "status": status,
        "ui": ui,
        "api": api,
        "impact": impact,
        "change_type": change_type,
        "comp_status": comp_status,
        "extra_acs": extra,
        "spec_status": spec_status,
    }


def feature_flag(text: str) -> str:
    m = re.search(r"^\*\*Feature flag\.\*\*\s*(.+)$", text, re.M)
    if not m:
        m = re.search(r"^-\s*Feature flag:\s*(.+)$", text, re.M)
    if not m:
        return "None."
    value = " ".join(m.group(1).split())
    return value[:400]


def agents_for(ui: str, api: str, impact: str, story_type: str) -> list[tuple[str, str, str, str]]:
    api_needed = api.upper() == "YES" or impact.upper() not in ("NO_API_CHANGE", "")
    ui_needed = ui.upper() == "YES"
    is_spike = story_type.lower() == "spike"
    return [
        ("Requirements and discovery", "Context Builder", "Not used",
         "The context package exists; reuse `.github/contexts/` and `EPIC-001`."),
        ("Requirements and discovery", "BRD Builder", "Not used",
         "The BRD is approved; reuse it."),
        ("Requirements and discovery", "PRD Builder", "Not used",
         "The FSD/PRD is approved; reuse it."),
        ("Design, backlog and spec", "Jira Backlog Manager", "Optional",
         "The local story file is the backlog; Jira import is TBC."),
        ("Design, backlog and spec", "Technical Specifier", "Applicable",
         "Produces the implementation-ready spec."),
        ("Plan and build", "Implementation Planner", "Applicable",
         "Produces `plan.md` and `tasks.md`."),
        ("Plan and build", "Implementation Builder", "Optional" if is_spike else "Applicable",
         "Throwaway spike; not merged." if is_spike else "Builds the approved plan in the ACE repository."),
        ("Quality and release", "Compliance Reviewer", "Applicable",
         "Spec, plan and code gates."),
        ("Quality and release", "API Tester", "Applicable" if api_needed else "Not used",
         "Required by the spec's API scope." if api_needed else "API is not in scope."),
        ("Quality and release", "Functional Automation Test", "Applicable" if ui_needed else "Not used",
         "Required by the spec's UI scope." if ui_needed else "UI is not in scope."),
        ("Quality and release", "Azure Deploy pipeline", "Not used",
         "ACE uses its own pipeline."),
    ]


def render_card(story: dict[str, str], index: int) -> tuple[str, dict[str, object]]:
    key = story["key"]
    title = story["title"]
    run_id = f"INC-{index:03d}-epic-1-{key}"
    card_name = f"{run_id}.md"
    output_dir = ROOT / "output" / run_id / "specify"
    story_path = ROOT / story["story_file"]

    story_text = read(story_path)
    meta = metadata(story_text)
    acs, zero = story_acs(story_text)
    current_ac_set = {a for a, _ in acs}
    gaps = ac_gaps(acs)
    spec = spec_info(run_id, current_ac_set)

    story_statement = first_paragraph(section(story_text, 1))
    rationale = first_paragraph(section(story_text, 2))
    flow = section(story_text, 4)
    out_of_scope = bullets(section(story_text, 19)) or [first_paragraph(section(story_text, 19))]
    guardrails = bullets(section(story_text, 17)) or [first_paragraph(section(story_text, 17))]
    authority_rows = table_rows(section(story_text, 10))
    flag = feature_flag(section(story_text, 13))
    module_label = meta.get("Module") or story.get("module", "")

    flow_steps = [
        re.sub(r"^\d+\.\s*", "", line.strip())
        for line in flow.splitlines()
        if re.match(r"^\d+\.\s*", line.strip())
    ][:6]

    if zero:
        ac_status = "0 — engineering enabler; no business ACs (see §7 note)"
    else:
        ac_status = f"{len(acs)} ACs in the current story ({', '.join(a for a, _ in acs)})"

    log_rel = f"output/{run_id}/specify/agent-run-log.md"
    if not (ROOT / log_rel).exists() and (ROOT / f"output/{run_id}/agent-run-log.md").exists():
        log_rel = f"output/{run_id}/agent-run-log.md"

    if zero:
        gap_status = "Not applicable — no ACs"
    elif gaps:
        if key == "RWB-E1-021":
            gap_status = f"Gap: {', '.join(f'AC{g}' for g in gaps)} (pre-existing in the source story)"
        else:
            gap_status = f"Gaps: {', '.join(f'AC{g}' for g in gaps)} (removed by the 4 November 2026 cleanup)"
    else:
        gap_status = "None — AC numbering is contiguous"

    if spec["spec_status"].startswith(("STALE", "BLOCKED + STALE")):
        if key == "RWB-E1-021":
            comp_status = (f"{spec['comp_status']} (stale — pre-existing AC mismatch)"
                           if spec["comp_status"] else "STALE (pre-existing)")
        else:
            comp_status = (f"{spec['comp_status']} (stale — predates the AC cleanup)"
                           if spec["comp_status"] else "STALE")
    else:
        comp_status = spec["comp_status"] or "TBC"

    spec_display = spec["spec_status"]
    if key == "RWB-E1-021" and spec_display.startswith("STALE"):
        spec_display = spec_display.replace("STALE", "STALE (pre-existing)", 1)

    lines: list[str] = []
    lines.append(f"# Increment Card — {run_id}")
    lines.append("")
    lines.append(f"**{key} — {title}**")
    lines.append("")
    lines.append("## Identification")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| Increment ID | `INC-{index:03d}` |")
    lines.append(f"| Title | {cell(title)} |")
    lines.append("| Programme / product | Recovery Workbench (recovery module of ACE) |")
    lines.append(f"| Jira epic / key | `E1` / `{key}` |")
    lines.append(f"| RUN_ID | `{run_id}` |")
    lines.append("| Parent epic card | `epics/EPIC-001-foundation-1.md` |")
    lines.append(f"| Module | {cell(module_label)} |")
    lines.append(f"| Story type | {cell(story.get('type', ''))} |")
    lines.append(f"| Priority | {cell(story.get('priority', ''))} |")
    lines.append(f"| Window | {cell(story.get('window', ''))} |")
    lines.append(f"| Critical path | {cell(story.get('critical_path') or 'No')} |")
    lines.append(f"| Depends on | {cell(story.get('depends_on') or 'None')} |")
    lines.append("| Status | In delivery |")
    lines.append("")
    lines.append("## Project type")
    lines.append("")
    lines.append("**Path:** Greenfield development of the Workbench module with brownfield ACE "
                 "integration constraints. The full 13-question classification is in "
                 "`epics/EPIC-001-foundation-1.md` and applies to this story.")
    lines.append("")
    lines.append(f"**Story type:** {cell(story.get('type', ''))}. "
                 f"**Module:** {cell(module_label)}. "
                 f"**Build group:** {cell(story.get('group', ''))}.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(f"**Story:** {story_statement or 'See the story file.'}")
    lines.append("")
    if flow_steps:
        lines.append("**Main flow:**")
        for n, step in enumerate(flow_steps, 1):
            lines.append(f"{n}. {step}")
        lines.append("")
    lines.append("**Out of scope:**")
    for item in out_of_scope:
        if item:
            lines.append(f"- {item}")
    lines.append("")
    lines.append(f"**Business outcome and value hypothesis:** {rationale or 'See story §2.'}")
    lines.append("")
    lines.append("**Constraints and guardrails:**")
    for item in guardrails:
        if item:
            lines.append(f"- {item}")
    lines.append("")
    lines.append("## Reused approved artefacts")
    lines.append("")
    lines.append("| Artefact | Version / link |")
    lines.append("|---|---|")
    lines.append(f"| Story file | `{cell(story['story_file'])}` |")
    lines.append(f"| Requirement IDs | {cell(meta.get('Requirement IDs', 'See story metadata'))} |")
    lines.append(f"| BRD section | {cell(meta.get('BRD section', 'See story metadata'))} |")
    lines.append("| Epic card | `epics/EPIC-001-foundation-1.md` |")
    lines.append("| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |")
    lines.append("| Module FSD / PRD | `docs/prds/` |")
    lines.append("| Module TSD | `requirement/legacy/05-technical-architecture/` |")
    lines.append("| Logical data model and data dictionary | `requirement/legacy/06-data/` |")
    lines.append("| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |")
    lines.append("| Business rules and routing logic | `requirement/legacy/02-business-architecture-and-process/` |")
    lines.append("| Error and message standard | `requirement/legacy/07-screens-and-experience/` |")
    lines.append("| Engineering practices | `AGENTS.md` |")
    lines.append("")
    lines.append("## Lifecycle tailoring")
    lines.append("")
    lines.append("Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; "
                 "this card records the story-specific agents and evidence.")
    lines.append("")
    if authority_rows:
        lines.append("## Story authority")
        lines.append("")
        lines.append("| Role | Rights in this story |")
        lines.append("|---|---|")
        for row in authority_rows:
            if len(row) >= 2:
                lines.append(f"| {cell(row[0])} | {cell(row[1])} |")
        lines.append("")
    lines.append("## Owners and approvals")
    lines.append("")
    lines.append("| Gate | Accountable role | Name | Decision / date |")
    lines.append("|---|---|---|---|")
    for gate, role in APPROVAL_GATES:
        lines.append(f"| {gate} | {role} | TBC | |")
    lines.append("")
    lines.append("`TBC` is not an approval (`GAP-006`). The story is in delivery at the specification "
                 "stage; the human gates remain open until named.")
    lines.append("")
    lines.append("## Agents selected")
    lines.append("")
    lines.append("| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |")
    lines.append("|---|---|---|---|")
    for group, agent, status, reason in agents_for(spec["ui"], spec["api"], spec["impact"], story.get("type", "")):
        lines.append(f"| {group} | {agent} | {status} | {cell(reason)} |")
    lines.append("")
    lines.append("## Risk, rollback and stop signals")
    lines.append("")
    lines.append("- **Rollback route:** feature flag off or redeploy the previous tag; see "
                 "`epics/EPIC-001-foundation-1.md`.")
    lines.append(f"- **Feature flag:** {flag}")
    lines.append(f"- **Critical path:** {cell(story.get('critical_path') or 'No')}; "
                 f"**depends on:** {cell(story.get('depends_on') or 'None')}.")
    lines.append("- **Stop signals:** see the epic card; story guardrails are:")
    for item in guardrails:
        if item:
            lines.append(f"  - {item}")
    lines.append("")
    lines.append("## Evidence links")
    lines.append("")
    lines.append("| Evidence | Location |")
    lines.append("|---|---|")
    lines.append(f"| Story file | `{cell(story['story_file'])}` |")
    lines.append(f"| Specification | `output/{run_id}/specify/spec.md` |")
    lines.append(f"| Compliance validation | `output/{run_id}/specify/compliance-validation.md` |")
    lines.append(f"| Agent run log | `{log_rel}` |")
    lines.append(f"| Plan and tasks | `output/{run_id}/plan/` (TBC) |")
    lines.append(f"| Implementation evidence | `output/{run_id}/implement/` (TBC) |")
    lines.append(f"| API / functional test reports | `output/{run_id}/api-tests/`, `functional-tests/` (TBC) |")
    lines.append(f"| Review findings | `output/{run_id}/review/` (TBC) |")
    lines.append("| Traceability | `requirement/Traceability_Matrix.md` |")
    lines.append("")
    lines.append("## Card status")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append("| Status | In delivery |")
    lines.append(f"| Specification | {cell(spec_display)} |")
    lines.append(f"| Compliance review | {cell(comp_status)} |")
    lines.append(f"| Acceptance criteria | {cell(ac_status)} |")
    lines.append(f"| AC numbering | {cell(gap_status)} |")
    lines.append(f"| Story source | `{cell(story['story_file'])}` |")
    lines.append(f"| Output run | `output/{run_id}/specify/` |")
    lines.append("| Card history | Backfilled on 2026-11-04; split from the epic card now at "
                 "`epics/EPIC-001-foundation-1.md`. Future increments create the story card before "
                 "the Technical Specifier starts. |")
    lines.append("")

    info = {
        "index": index,
        "run_id": run_id,
        "card_name": card_name,
        "key": key,
        "title": title,
        "module": module_label,
        "type": story.get("type", ""),
        "priority": story.get("priority", ""),
        "spec_status": spec["spec_status"],
        "ac_status": ac_status,
        "ac_count": len(acs),
        "gap_status": gap_status,
        "zero": zero,
        "gaps": gaps,
    }
    return "\n".join(lines), info


def build_index(cards: list[dict[str, object]]) -> str:
    zero = [c for c in cards if c["zero"]]
    stale = [c for c in cards if str(c["spec_status"]).startswith(("STALE", "BLOCKED + STALE"))]
    blocked = [c for c in cards if "BLOCKED" in str(c["spec_status"])]
    gaps = [c for c in cards if c["gaps"]]
    lines: list[str] = []
    lines.append("# Increment index")
    lines.append("")
    lines.append("Two epic-level records live in `epics/`. The 78 story-level records in this folder "
                 "match the Epic 1 output run IDs one-to-one.")
    lines.append("")
    lines.append("## Epics")
    lines.append("")
    lines.append("| Epic | Card | Tailoring | Release | Status |")
    lines.append("|---|---|---|---|---|")
    lines.append("| `EPIC-001` Foundation 1 | `epics/EPIC-001-foundation-1.md` | "
                 "`epics/EPIC-001-tailoring.md` | 30 Nov 2026 | In delivery |")
    lines.append("| `EPIC-002` Foundation 2 | `epics/EPIC-002-foundation-2.md` | "
                 "`epics/EPIC-002-tailoring.md` | 31 Dec 2026 | Mobilised |")
    lines.append("")
    lines.append("## Story increments")
    lines.append("")
    lines.append("| INC | Story | Title | Module | Type | Priority | Spec | ACs | Gaps | Card | Run |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for c in cards:
        spec_short = "UNKNOWN"
        status_text = str(c["spec_status"])
        if status_text.startswith("BLOCKED + STALE"):
            spec_short = "BLOCKED + STALE"
        elif status_text.startswith("STALE"):
            spec_short = "STALE"
        elif status_text.startswith("BLOCKED"):
            spec_short = "BLOCKED"
        elif status_text.startswith("SUCCESS"):
            spec_short = "SUCCESS"
        gaps_short = "-"
        if c["gaps"]:
            gap_list = c["gaps"]
            if len(gap_list) == 1:
                gaps_short = f"AC{gap_list[0]}"
            elif gap_list == list(range(gap_list[0], gap_list[-1] + 1)):
                gaps_short = f"AC{gap_list[0]}-AC{gap_list[-1]}"
            else:
                gaps_short = ", ".join(f"AC{g}" for g in gap_list)
        lines.append(
            f"| {c['index']:03d} | `{c['key']}` | {cell(c['title'])} | {cell(c['module'])} | "
            f"{cell(c['type'])} | {cell(c['priority'])} | {spec_short} | {c['ac_count']} | "
            f"{gaps_short} | `{c['card_name']}` | `output/{c['run_id']}/specify/` |"
        )
    lines.append("")
    stale_keys = ", ".join(f"`{c['key']}`" for c in stale)
    blocked_keys = ", ".join(f"`{c['key']}`" for c in blocked)
    zero_keys = ", ".join(f"`{c['key']}`" for c in zero)
    gap_keys = ", ".join(f"`{c['key']}`" for c in gaps)
    lines.append("## Status notes")
    lines.append("")
    lines.append("- **78** story cards, one per Epic 1 build-sequence story.")
    lines.append(f"- **{len(stale)}** specs are stale against the current story ACs and must be "
                 f"regenerated: {stale_keys}.")
    lines.append(f"- **{len(blocked)}** specs are blocked: {blocked_keys}.")
    lines.append(f"- **{len(zero)}** stories have zero business ACs: {zero_keys}.")
    lines.append(f"- **{len(gaps)}** stories have AC-numbering gaps: {gap_keys}.")
    lines.append("- Named approvers remain `TBC` (`GAP-006`); the mandatory-control checklist in "
                 "`epics/EPIC-001-tailoring.md` is still unchecked.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate the cards without writing")
    args = ap.parse_args()

    manifest = json.loads(read(MANIFEST))
    stories = [s for g in manifest["groups"] for s in g["stories"]]
    cards: list[dict[str, object]] = []
    rendered: list[tuple[Path, str]] = []

    for story in stories:
        key = story["key"]
        m = re.search(r"INC-(\d{3})-epic-1-", story["output_dir"])
        if not m:
            raise SystemExit(f"Cannot parse INC number from output_dir for {key}: {story['output_dir']}")
        index = int(m.group(1))
        text, info = render_card(story, index)
        card_path = INCREMENTS / info["card_name"]
        rendered.append((card_path, text))
        cards.append(info)

    if len(cards) != 78:
        raise SystemExit(f"Expected 78 stories, found {len(cards)}")
    indices = [c["index"] for c in cards]
    if sorted(indices) != list(range(1, 79)):
        raise SystemExit(f"INC numbers are not 1..78: {sorted(indices)}")
    run_ids = [c["run_id"] for c in cards]
    if len(set(run_ids)) != len(run_ids):
        raise SystemExit("Duplicate RUN_IDs")
    cards.sort(key=lambda c: c["index"])
    rendered.sort(key=lambda x: x[0].name)

    index_text = build_index(cards)

    if args.check:
        failures: list[str] = []
        for path, _ in rendered:
            if not path.exists():
                failures.append(f"missing card: {path.relative_to(ROOT)}")
                continue
            text = read(path)
            run_id = path.stem
            if f"| RUN_ID | `{run_id}` |" not in text:
                failures.append(f"RUN_ID mismatch: {path.relative_to(ROOT)}")
            for section_name in CARD_SECTIONS:
                if section_name not in text:
                    failures.append(f"missing section {section_name}: {path.relative_to(ROOT)}")
        if not (INCREMENTS / "INDEX.md").exists():
            failures.append("missing docs/increments/INDEX.md")
        for old in ("INC-001-epic-1.md", "INC-001-tailoring.md",
                    "INC-002-epic-2.md", "INC-002-tailoring.md"):
            if (INCREMENTS / old).exists():
                failures.append(f"old card still exists: docs/increments/{old}")
        if failures:
            print(f"FAIL: {len(failures)} issue(s)")
            for f in failures:
                print(f"  - {f}")
            raise SystemExit(1)
        print(f"PASS: {len(cards)} cards, INDEX.md, RUN_IDs and sections")
        return

    for path, text in rendered:
        write_text(path, text)
    write_text(INCREMENTS / "INDEX.md", index_text)
    print(f"Wrote {len(cards)} story cards and INDEX.md")
    stale_count = sum(1 for c in cards if str(c["spec_status"]).startswith(("STALE", "BLOCKED + STALE")))
    print(f"Stale specs: {stale_count}")
    print(f"Zero-AC stories: {sum(1 for c in cards if c['zero'])}")
    print(f"AC gaps: {sum(1 for c in cards if c['gaps'])}")


if __name__ == "__main__":
    main()
