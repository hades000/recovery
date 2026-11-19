#!/usr/bin/env python3
"""Build the v2 repository records from the converted 16 November 2026 corpus.

Reads the converted story files and Build Sequence v6, then writes:
  output/EPIC1-STORY-MANIFEST.json / .md
  docs/increments/INC-0NN-*.md and INDEX.md
  docs/retirements/story-retirement-register.md
  docs/increments/epic-2-stories.md

No network, no interactive questions. Every ambiguity is resolved by the
documented default in docs/decisions/decision-register.md.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "requirement" / "legacy"
STORY_DIRS = [
    LEGACY / "04-user-stories" / "recovery-workbench-user-stories-epic-1-story-files-v7_extracted",
    LEGACY / "04-user-stories" / "recovery-workbench-user-stories-epic-2-story-files-v5_extracted",
]
BUILD_SEQUENCE = ROOT / "docs" / "increments" / "build-sequence.md"
OUT = ROOT / "output"
INC = ROOT / "docs" / "increments"
RET = ROOT / "docs" / "retirements"

RETIRED = {
    "RWB-E1-003": ("Data-load story removed by D-RCV-35 U1", "ACE ingestion (RWB-ACE-001)"),
    "RWB-E1-004": ("Data-load story removed by D-RCV-35 U1", "ACE ingestion (RWB-ACE-001)"),
    "RWB-E1-005": ("Tracker story removed by D-RCV-35 U5", "Cutover plan, section 8"),
    "RWB-E1-006": ("Data-quality load story removed by D-RCV-35 U1", "ACE ingestion checks; daily gate in RWB-E1-015"),
    "RWB-E1-009": ("Data-load story removed by D-RCV-35 U1", "ACE ingestion (RWB-ACE-001)"),
    "RWB-E1-010": ("Tracker story removed by D-RCV-35 U5", "Cutover plan, section 8"),
    "RWB-E1-012": ("Tracker-retirement story removed by D-RCV-35 U5", "Cutover plan, section 8"),
    "RWB-E1-029": ("Rule-load story retired by D-RCV-36 T8", "RWB-E1-073"),
    "RWB-E1-048": ("Rule audit story retired by D-RCV-36 T8", "RWB-E2-041"),
    "RWB-E1-051": ("ADF/Control-M story removed by D-RCV-35 U1", "ACE ingestion (RWB-ACE-001)"),
    "RWB-TE-005": ("Rule-table harness retired by D-RCV-36 T8", "RWB-E1-073"),
}

PRESERVED = {
    "RWB-E1-044": "INC-001 (10 November 2026 run)",
    "RWB-TE-001": "INC-002 (10 November 2026 run)",
    "RWB-E1-042": "E1-042 Migration and Clarifications (10 November 2026)",
    "RWB-E1-043": "INC-009 (10 November 2026 run)",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
    part = re.split(r"\n\s*\n", text, maxsplit=1)[0]
    return " ".join(part.split())


def metadata(text: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for line in text.splitlines()[:50]:
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] not in ("Item", "Field", "---"):
            meta[cells[0]] = cells[1]
    return meta


def story_key(path: Path) -> str | None:
    m = re.search(r"rwb-(e1|te|e2)-(\d{3})", path.name, re.I)
    if not m:
        return None
    return f"RWB-{m.group(1).upper()}-{m.group(2)}"


def story_title(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if not m:
        return ""
    title = m.group(1).strip()
    return re.sub(r"^RWB-[A-Z0-9]+-\d{3}\s+", "", title)


def acs(text: str) -> list[tuple[str, str]]:
    sec = section(text, 7)
    if "No business acceptance criteria" in sec:
        return []
    out = []
    for line in sec.splitlines():
        m = re.match(r"^\s{0,4}Scenario:\s*(AC\s*\d+)\s*(.*)$", line, re.I)
        if m:
            out.append((m.group(1).replace(" ", ""), m.group(2).strip()))
    return out


def parse_build_sequence() -> list[dict[str, str]]:
    text = read(BUILD_SEQUENCE)
    m = re.search(r"^## Sequence\s*$", text, re.M)
    body = text[m.end():] if m else text
    nxt = re.search(r"^##\s+", body, re.M)
    if nxt:
        body = body[:nxt.start()]
    rows = []
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7 or not re.fullmatch(r"\d+", cells[0]):
            continue
        if not cells[1].startswith("RWB-"):
            continue
        rows.append({
            "order": cells[0], "key": cells[1], "title": cells[2], "module": cells[3],
            "type": cells[4], "priority": cells[5], "depends_on": cells[6],
            "release": cells[9] if len(cells) > 9 else "",
        })
    return rows


def find_stories() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for directory in STORY_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            key = story_key(path)
            if not key:
                continue
            # The v7 / Epic 2 v5 extracted folders hold the current revision.
            found[key] = path
    return found


def cover(text: str, limit: int = 180) -> str:
    value = " ".join(text.split())
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def render_card(story: dict, order: int) -> str:
    key = story["key"]
    text = read(story["path"])
    meta = story["meta"]
    ac_list = story["acs"]
    story_statement = first_paragraph(section(text, 1))
    rationale = first_paragraph(section(text, 2))
    preconditions = section(text, 3)
    flow = section(text, 4)
    guardrails = section(text, 17)
    out_of_scope = section(text, 19)
    authority = section(text, 10)
    contract = section(text, 12)
    tests = section(text, 16)

    flow_steps = [re.sub(r"^\d+\.\s*", "", l.strip()) for l in flow.splitlines() if re.match(r"^\d+\.\s*", l.strip())][:6]
    ac_status = (f"{len(ac_list)} acceptance criteria" if ac_list
                 else "0 — engineering enabler; acceptance is the business rules and test cases (D-RCV-16)")
    status = story["status"]
    run_id = story["run_id"]

    lines = [
        f"# Increment Card — {run_id}", "",
        f"**{key} — {story['title']}**", "",
        "## Identification", "",
        "| Field | Value |", "|---|---|",
        f"| Increment ID | `INC-{order:03d}` |",
        f"| Title | {story['title']} |",
        "| Programme / product | Recovery Workbench (recovery module of ACE) |",
        f"| Jira epic / key | `{story['epic']}` / `{key}` |",
        f"| RUN_ID | `{run_id}` |",
        "| Parent epic card | `epics/EPIC-001-foundation-1.md` |",
        f"| Module | {meta.get('Module', story['module'])} |",
        f"| Story type | {story['type']} |",
        f"| Priority | {meta.get('Priority', story['priority'])} |",
        f"| Build order | {order} of 72 (Build Sequence v6, 16 November 2026) |",
        f"| Depends on | {meta.get('Depends on', story['depends_on']) or 'None'} |",
        f"| Blocks | {meta.get('Blocks', 'See the build sequence')} |",
        f"| Status | {status} |", "",
        "## Project type", "",
        "**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question "
        "classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.", "",
        f"**Story type:** {story['type']}. **Module:** {meta.get('Module', story['module'])}.", "",
        "## Scope", "",
        f"**Story:** {story_statement or 'See the story file.'}", "",
        f"**Business outcome:** {rationale or 'See story §2.'}", "",
    ]
    if flow_steps:
        lines += ["**Main flow:**"] + [f"{i}. {s}" for i, s in enumerate(flow_steps, 1)] + [""]
    if ac_list:
        lines += ["**Acceptance criteria:**"] + [f"- {a}: {t}" for a, t in ac_list] + [""]
    lines += ["**Out of scope:**"]
    for line in out_of_scope.splitlines():
        if line.strip().startswith(("- ", "* ")):
            lines.append(f"- {line.strip()[2:]}")
    if not any(l.startswith("- ") for l in lines[-5:]):
        lines.append("- See story §19.")
    lines += ["", "## Reused approved artefacts", "",
              "| Artefact | Version / link |", "|---|---|",
              f"| Story file | `{story['rel']}` |",
              f"| Requirement IDs | {meta.get('Requirement IDs', 'See story metadata')} |",
              f"| BRD section | {meta.get('BRD section', 'See story metadata')} |",
              f"| Decision | {meta.get('Decision', 'See decision register')} |",
              "| Epic card | `epics/EPIC-001-foundation-1.md` |",
              "| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |",
              "| Module FSD / PRD | `docs/prds/` |",
              "| Module TSD | `requirement/legacy/05-technical-architecture/` |",
              "| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |",
              "| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |",
              "| Engineering practices | `AGENTS.md` |", "",
              "## Lifecycle tailoring", "",
              "Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; "
              "this card records the story-specific agents and evidence.", ""]
    if authority:
        lines += ["## Story authority", "", authority, ""]
    if contract:
        lines += ["## Contract extract", "", cover(contract, 900), ""]
    lines += ["## Owners and approvals", "",
              "| Gate | Accountable role | Name | Decision / date |", "|---|---|---|---|",
              "| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |",
              "| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |",
              "| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |",
              "| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |", "",
              "## Agents selected", "",
              "| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |", "|---|---|---|---|",
              "| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |",
              "| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |",
              "| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |",
              "| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |",
              "| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |",
              "| Quality and release | API Tester | Per API scope | Driven by the spec. |",
              "| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |", "",
              "## Risk, rollback and stop signals", "",
              "- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.",
              "- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; "
              "a direct read of an ACE table outside `recovery.v_ace_*`.", ""]
    if guardrails:
        lines += ["**Guardrails:**", "", cover(guardrails, 900), ""]
    lines += ["## Evidence links", "",
              "| Evidence | Location |", "|---|---|",
              f"| Story file | `{story['rel']}` |",
              f"| Specification | `output/{run_id}/specify/spec.md` |",
              f"| Compliance validation | `output/{run_id}/specify/compliance-validation.md` |",
              f"| Agent run log | `output/{run_id}/specify/agent-run-log.md` |",
              f"| Plan and tasks | `output/{run_id}/plan/` |",
              f"| Implementation evidence | `output/{run_id}/implement/` |",
              f"| API / functional test reports | `output/{run_id}/api-tests/`, `functional-tests/` |",
              f"| Review findings | `output/{run_id}/review/` |",
              "| Traceability | `requirement/Traceability_Matrix.md` |", "",
              "## Card status", "",
              "| Field | Value |", "|---|---|",
              f"| Status | {status} |",
              f"| Specification | {story['spec_status']} |",
              f"| Compliance review | {story['compliance']} |",
              f"| Acceptance criteria | {ac_status} |",
              f"| Test cases in story | {len(re.findall(r'TC-' + re.escape(key) + r'-', tests))} |",
              f"| Preserved implementation | {story['preserved']} |",
              f"| Story source | `{story['rel']}` |",
              f"| Output run | `output/{run_id}/` |", "",
              ]
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INC.mkdir(parents=True, exist_ok=True)
    RET.mkdir(parents=True, exist_ok=True)
    (INC / "epics").mkdir(parents=True, exist_ok=True)

    rows = parse_build_sequence()
    found = find_stories()
    order_map = {r["key"]: int(r["order"]) for r in rows
                 if r["key"].startswith(("RWB-E1-", "RWB-TE-")) and r.get("release") == "E1"}
    seq_map = {r["key"]: r for r in rows}

    active = []
    for key, order in sorted(order_map.items(), key=lambda kv: kv[1]):
        if key not in found:
            continue
        path = found[key]
        text = read(path)
        meta = metadata(text)
        ac_list = acs(text)
        run_id = f"INC-{order:03d}-epic-1-{key}"
        preserved = ""
        if key in PRESERVED:
            if key in ("RWB-E1-044", "RWB-E1-043"):
                preserved = f"Spec and plan carried from `{PRESERVED[key]}`; not built."
            else:
                preserved = f"Carried from `{PRESERVED[key]}`; implementation evidence preserved."
        if key == "RWB-E1-042":
            preserved = "IMPLEMENTED. Migration pack `E1-042 Migration and Clarifications`; evidence `output/INC-003-epic-1-RWB-E1-042/implement/`."
            status = "Implemented — migration applied and tested; spec and plan rebaselined 16 Nov 2026"
            spec_status = "SUCCESS — new v2 spec 16 Nov 2026"
            compliance = "PASS"
        elif key == "RWB-TE-001":
            preserved = "IMPLEMENTED. Module boundary and BND-1..BND-5 built and merged (ACE MR !285); evidence `output/INC-002-epic-1-RWB-TE-001/implement/`."
            status = "Implemented — module boundary built; spec and plan rebaselined 16 Nov 2026"
            spec_status = "SUCCESS — new v2 spec 16 Nov 2026"
            compliance = "PASS"
        elif key == "RWB-E1-044":
            status = "Planned — plan carried from the 10 Nov 2026 run; schema basis reverted to `recovery` by D-RCV-35; re-plan before build"
            spec_status = "SUCCESS — 10 Nov 2026, needs re-baseline for D-RCV-35"
            compliance = "PASS (2026-11-10)"
        elif key == "RWB-E1-043":
            status = "Planned — plan carried from the 10 Nov 2026 run; re-baseline for D-RCV-35"
            spec_status = "SUCCESS — 10 Nov 2026, needs re-baseline for D-RCV-35"
            compliance = "PASS (2026-11-10)"
        else:
            status = "Ready for specify" if order <= 15 else "Backlog — not started"
            spec_status = "NOT RUN — new v2 baseline"
            compliance = "Not run"
        active.append({
            "key": key,
            "title": meta.get("Story key", "") and story_title(text) or story_title(text),
            "epic": "EPIC-001",
            "module": meta.get("Module", seq_map[key]["module"]),
            "type": meta.get("Story key", "") and seq_map[key]["type"] or seq_map[key]["type"],
            "priority": meta.get("Priority", seq_map[key]["priority"]),
            "depends_on": meta.get("Depends on", seq_map[key]["depends_on"]),
            "path": path,
            "rel": path.relative_to(ROOT).as_posix(),
            "meta": meta,
            "acs": ac_list,
            "status": status,
            "spec_status": spec_status,
            "compliance": compliance,
            "preserved": preserved,
            "run_id": run_id,
        })

    rendered = []
    for story in active:
        order = order_map[story["key"]]
        rendered.append((INC / f"{story['run_id']}.md", render_card(story, order)))

    for path, text in rendered:
        path.write_text(text + "\n", encoding="utf-8")

    # INDEX
    lines = ["# Increment index", "",
             "The 72 Epic 1 story records match the Build Sequence v6 order one-to-one. "
             "Epic 2 records are listed separately until their increments are opened.", "",
             "## Epics", "",
             "| Epic | Card | Tailoring | Release | Status |", "|---|---|---|---|---|",
             "| `EPIC-001` Foundation 1 | `epics/EPIC-001-foundation-1.md` | `epics/EPIC-001-tailoring.md` | 30 Nov 2026 | In delivery |",
             "| `EPIC-002` Foundation 2 | `epics/EPIC-002-foundation-2.md` | `epics/EPIC-002-tailoring.md` | 31 Dec 2026 | Mobilised |", "",
             "## Story increments", "",
             "| INC | Story | Title | Module | Type | Priority | Status | Spec | ACs | Card | Run |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for story in active:
        order = order_map[story["key"]]
        if story["key"] in ("RWB-E1-044", "RWB-E1-043"):
            spec_short = "HISTORICAL"
        elif story["spec_status"].startswith("SUCCESS"):
            spec_short = "SUCCESS"
        else:
            spec_short = "NOT RUN"
        lines.append(
            f"| {order:03d} | `{story['key']}` | {story['title']} | {story['module']} | {story['type']} | "
            f"{story['priority']} | {story['status'].split(' — ')[0]} | {spec_short} | {len(story['acs'])} | "
            f"`{story['run_id']}.md` | `output/{story['run_id']}/` |"
        )
    lines += ["", "## Status notes", "",
              "- **72** active Epic 1 story records (62 user stories and enablers in the v7 story set, plus 10 technical enablers).",
              "- **10** stories are removed or retired by D-RCV-35 and D-RCV-36; see `../retirements/story-retirement-register.md`.",
              "- **New in this version:** `RWB-E1-069` read-only ACE views and `RWB-E1-070`..`RWB-E1-073` Temporal/Drools.",
              "- **Implemented:** `RWB-E1-042` (migration pack) and `RWB-TE-001` (module boundary). "
              "**Planned and preserved:** `RWB-E1-044`, `RWB-E1-043`.",
              "- `RWB-E1-036` has no story file in any version; it is not in the build sequence and is not created here.",
              "", "## Epic 2", "",
              "The Epic 2 story set is v5 (16 November 2026). `epic-2-stories.md` lists its 43 items, "
              "including the new `RWB-E2-037`..`RWB-E2-043` and `RWB-TE-009`/`RWB-TE-010`.", ""]
    (INC / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")

    # Retirement register
    ret = ["# Story retirement register", "",
           "Source decisions: D-RCV-35 (ACE DB alignment, U1–U5) and D-RCV-36 (Temporal and Drools, T8). "
           "No retired story is rebuilt in this repository.", "",
           "| Story | Reason | New home | Evidence |", "|---|---|---|---|"]
    for key, (reason, home) in RETIRED.items():
        ret.append(f"| `{key}` | {reason} | {home} | `docs/retirements/` and the source change register |")
    ret += ["", "`RWB-E1-007` survives as outbound-only adapters; only its inbound file-load part is removed. "
            "`RWB-E1-006` survives only as the daily gate in `RWB-E1-015`.", ""]
    (RET / "story-retirement-register.md").write_text("\n".join(ret), encoding="utf-8")

    # Manifest
    manifest = {
        "generated": "2026-11-16",
        "base": "17 AI-First SDLC Repository v2",
        "source": "Build Sequence Epic 1 and Epic 2 v6; User Stories Epic 1 v7; Technical Enabler Stories v7",
        "groups": [{"epic": "EPIC-001", "name": "Foundation 1", "release": "30 Nov 2026",
                    "stories": [{k: v for k, v in s.items() if k not in ("path", "meta", "acs")}
                                for s in active]}],
    }
    (OUT / "EPIC1-STORY-MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    md = ["# Epic 1 story manifest", "", "| INC | Story | Title | Module | Type | Priority | Status |",
          "|---|---|---|---|---|---|---|"]
    for s in active:
        md.append(f"| {order_map[s['key']]:03d} | `{s['key']}` | {s['title']} | {s['module']} | {s['type']} | {s['priority']} | {s['status']} |")
    (OUT / "EPIC1-STORY-MANIFEST.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # Epic 2 list
    e2 = sorted([k for k in found if k.startswith(("RWB-E2-", "RWB-TE-")) and k not in order_map])
    e2lines = ["# Epic 2 story set (v5, 16 November 2026)", "",
               "| Story | Title | Module | Status |", "|---|---|---|---|"]
    for key in e2:
        path = found[key]
        text = read(path)
        meta = metadata(text)
        e2lines.append(f"| `{key}` | {story_title(text)} | {meta.get('Module', '')} | Backlog |")
    (INC / "epic-2-stories.md").write_text("\n".join(e2lines) + "\n", encoding="utf-8")

    print(f"Wrote {len(active)} Epic 1 cards, INDEX.md, manifest, retirements and {len(e2)} Epic 2 rows")


if __name__ == "__main__":
    main()
