"""Build the BRD Epic 1 v5 markdown (D-RCV-60). Scratch generator for WP B-REQ-BRD-E1.

Body sections 1-7 are copied verbatim from the v4 extract; the document control block is
rewritten for version 5 and sections 8 (Delivery model) and 9 (trace) are added.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "_work" / "msr" / "extract" / "B-REQ-BRD-E1" / "Recovery Workbench Business Requirements Epic 1 v4.md"
PLAN = ROOT / "_work" / "msr" / "plan" / "split_plan.json"
MAP = ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx"
OUT_MD = ROOT / "03 Requirements and specifications" / "Recovery Workbench Business Requirements Epic 1 v5.md"
SCRATCH = ROOT / "_work" / "msr" / "docs" / "B-REQ-BRD-E1" / "Recovery Workbench Business Requirements Epic 1 v5.md"

HEADER = [
    "SCB Collections and Recovery. Henka Group, 22 November 2026.",
    "(C) Siam Commercial Bank and Henka Pte Ltd",
]

CONTROL = """| Item | Detail |
|---|---|
| Document | Recovery Workbench business requirements, Epic 1 |
| Version | 5 |
| Date | 22 November 2026 |
| Prepared by | Henka Group |
| Release | 30 November 2026 (tentative) |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |
| Change log | below, one row per version |
| Change | Version 5 is the D-RCV-60 microservice realignment. Sections 1 to 7 are copied from version 4 with every key, number, requirement, role and date unchanged; the release date is marked tentative. Section 8 adds the delivery model: 19 service epics inside ACE, four waves, platform and integration epics, and contract-first delivery. Section 9 adds the trace from each business requirement to its service epic and business epic. No business requirement is rewritten, added or removed by this version. Three delivery positions are recorded rather than edited into the text: RWB-E1-014 is retired by D-RCV-60, and RWB-E1-029 and RWB-E1-048 were cancelled before this run. Four decision-owner cells in section 7 named people; they carry the register placeholder of Template and Rules section R9 (CG-B-REQ-BRD-E1-6; ASM-B-REQ-BRD-E1-12) and their question and answer cells are unchanged. |

| Version | Date | Change | Owner |
|---|---|---|---|
| 4 | 15 November 2026 | Version 4 applies D-RCV-35 and ADR-010, which supersedes ADR-005. Section 3.1 states the four-tier read model, the 30 views, the dictionary, reconciliation and freshness position; section 3.2 is outbound only. Section 4 marks the removed requirements and re-words the data requirements, section 7 records DL43, and the requirement and role counts follow. RWB-E1-069 and RWB-ACE-001 are added; removed requirements keep their keys. Other sections are unchanged. | Henka Group |
| 5 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. Sections 1 to 7 unchanged, release marked tentative, section 8 delivery model and section 9 trace added. | Henka Group |
"""

DELIVERY = """# 8. Delivery model

Version 5 records how Epic 1 is delivered after D-RCV-60 adopts Architecture v5. The requirements in
section 3 are unchanged and keep their keys. What changes is the way they are built: the Workbench is
one module inside ACE, built as 19 services, ordered in waves 0 to 4, and every service starts with its
published contract.

## 8.1 One epic per service

The Workbench is a module in the ACE platform built as 19 services (ADR-013). Each service is one
development epic, `RWB-SVC-<code>`, with its own schema and login in ACE PostgreSQL (ADR-014), its own
REST base, its own event topic with a retry and a dead-letter topic (ADR-015) and its own Temporal task
queue (ADR-016). A requirement is delivered by the service that owns the data or the action. The
Ownership Map v1 is the single source for that ownership, and it is used for every owner named in this
section and in section 9.

| Code | Service epic | Service | Scope | Wave |
|---|---|---|---|---|
"""

WAVES = """
## 8.2 Waves

Wave 0 is the platform: the service template, the shared libraries, the workflow platform, the event
platform, the edge and gateway, observability, the ACE schemas and logins, and the integration harness.
Waves 1 to 4 follow the business epics. A story takes the earlier of its business-epic wave and its
service's wave, so an Epic 1 requirement is built in wave 1 even where its service is scheduled later
(CG-B-REQ-BRD-E1-4).

| Wave | Business epic | Theme | Release (tentative) | Service epics that start in the wave |
|---|---|---|---|---|
| 0 | Platform and non-functional | Service template, libraries, workflow, events, edge, observability, ACE schemas, integration harness | Before wave 1 | RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS, RWB-ITG-W1, RWB-ITG-W2, RWB-ITG-W3, RWB-ITG-W4, RWB-ITG-NFR |
| 1 | EP01 Foundation 1 | One case list, documents by case, decision log store, read-only case record view | 30 November 2026 (tentative) | RWB-SVC-P1, RWB-SVC-P2, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P5, RWB-SVC-P6, RWB-SVC-P7, RWB-SVC-P9, RWB-SVC-P10 |
| 2 | EP02 Foundation 2; EP03 Settle, deed in lieu, assets | One owner and a timer on every case, approval routing, litigation notices; settlements and deeds in lieu end to end, asset record and listing | 31 December 2026 (tentative); 31 January 2027 (tentative) | RWB-SVC-P8, RWB-SVC-S2, RWB-SVC-S5, RWB-SVC-S8 |
| 3 | EP04 Route decision; EP05 Litigation | Route recommended and approved within the delegation of authority, guarantees and TCG claims; litigation instructed and tracked | 28 February 2027 (tentative); 31 March 2027 (tentative) | RWB-SVC-S1, RWB-SVC-S3, RWB-SVC-S4, RWB-SVC-S6 |
| 4 | EP06 Debt sale and write-off; EP07 Deviations and partners; EP08 Administration and hardening | Debt sale and write-off; deviations X1 to X7 and partner management; full administration and hardening | 30 April 2027 (tentative); 31 May 2027 (tentative); 30 June 2027 (tentative) | RWB-SVC-S7, RWB-SVC-S9 |

## 8.3 Contract first

Every service epic opens with a contract story. The contract is published as an OpenAPI file, an
AsyncAPI file and an activity jar before application work starts, and application stories build against
the published contract and its fake. A service therefore never waits for another service's code. Each
service calls one hop over REST with a 2 second timeout (ADR-020), publishes CloudEvents on
`rwb.<short>.events.v1` with retries and a dead-letter topic (ADR-015), and runs its workflows on its
own Temporal task queue (ADR-016). Scheduled work is a Temporal Schedule and not a Quartz job. There is
no data lake: reporting is built from events into the reporting read model (ADR-018).

Contract stories are Day 1 work. An application story that depends on another service's contract builds
against the published contract and its fake, so the dependency never blocks a lane.

## 8.4 Work types and soft ownership

Each story is one of six work types, and each work type carries a suggested owner by team type. The
suggestion is not binding: any team may pick up a story, and no person is named in any output.

| Work type | Work | Suggested owner |
|---|---|---|
| CON | Contract | TechX (suggested; any team may pick up this story) |
| APP | App development | TechX (suggested; any team may pick up this story) |
| DB | ACE DB | ACE team (suggested; any team may pick up this story) |
| INF | Infrastructure | SCB IT infrastructure (suggested; any team may pick up this story) |
| OPS | DevOps | DevOps team (suggested; any team may pick up this story) |
| ITG | Integration, harness and non-functional | TechX for integration and QA team for harness and non-functional (suggested; any team may pick up this story) |

## 8.5 Requirements kept, changed, retired and cancelled

The business content of section 3 is unchanged. The delivery model changes only how a requirement is
built. Five positions apply.

| Position | Requirements | What the delivery model does |
|---|---|---|
| Built or in build, kept | RWB-E1-042, RWB-E1-043, RWB-E1-044 | The as-built content is kept word for word. The microservice change is separate delta stories: one schema and one contract per service, parameters and reference data behind the rwb-case contract, and Flyway per service. No built code changes until a delta story is picked up. |
| Must change | RWB-E1-001 | The built single-schema migration (92 tables, 14 data products, dictionary) is kept. The split into one schema per service is new work under RWB-PLT-DB and the per-service DB stories, and it is recorded in the Change Register. |
| Retired by D-RCV-60 | RWB-E1-014 | Architecture v5 has no data lake. The decision log is read from events into the reporting read model. The requirement keeps its key and its text, and no story is built (CG-B-REQ-BRD-E1-1). |
| Already cancelled before this run | RWB-E1-029, RWB-E1-048 | No story is built. The keys and the text stay in section 3.3 (CG-B-REQ-BRD-E1-2 and CG-B-REQ-BRD-E1-3). |
| Removed by D-RCV-35 | RWB-E1-003, RWB-E1-004, RWB-E1-005, RWB-E1-006, RWB-E1-009, RWB-E1-010, RWB-E1-012, RWB-E1-051 | Already marked Removed in section 3, each naming its later home: ACE ingestion, or the Cutover plan. Nothing further changes. |

## 8.6 Dates

Every release date in this document is unchanged from version 4, and every one is tentative
(DL48). Epic 1 releases on 30 November 2026 (tentative), and the programme finishes within eight
months.

# 9. Business requirement to service epic trace

Every requirement in section 3 keeps its key. The key is the business requirement ID of this epic and
it does not change between versions. The primary service epic is the chapter that owns the largest part
of the requirement in the Ownership Map v1; where a key has several stories, the other service epics
carry the linked stories of the same key. Every requirement that is built belongs to business epic EP01
Foundation 1, which is wave 1 and releases on 30 November 2026 (tentative). The story count is the
number of story slices the plan holds for the key.

| Business requirement | Requirement | Primary service epic | Service | Wave | Business epic | Stories |
|---|---|---|---|---|---|---|
"""

DISP = {
    "Must change": "Must change, {}",
    "Split (rework)": "Split into {}",
    "Moved (no impact)": "Moved unchanged, {}",
    "Preserved + delta": "Kept as built, {} including the delta",
}
CANCELLED = {"RWB-E1-029", "RWB-E1-048"}
RETIRED = {"RWB-E1-014"}

PH = "Not specified in the source documents (CG-B-REQ-BRD-E1-6; ASM-B-REQ-BRD-E1-12)"
NAMES = {
    "K. Book with K. Pipat": PH,
    "K. Tee with K. Jao": PH,
    "K. Tony with K. Book": PH,
    "Solution architect with K. Book": PH,
}


def services():
    import openpyxl

    wb = openpyxl.load_workbook(MAP, read_only=True)
    ws = wb["Services"]
    out = []
    for row in list(ws.iter_rows(values_only=True))[1:]:
        if row and row[0]:
            out.append((row[0], row[1], row[2], int(row[3])))
    return out


def main():
    src = SRC.read_text(encoding="utf-8").splitlines()
    i = src.index("# 1. What this epic delivers")
    body = src[i:]
    body = [
        l.replace(
            "Epic 1, Foundation 1, releases on 30 November 2026.",
            "Epic 1, Foundation 1, releases on 30 November 2026 (tentative).",
        )
        for l in body
    ]
    for old, new in NAMES.items():
        body = [l.replace(f"| {old} |", f"| {new} |") for l in body]

    svc = services()
    parts = [*HEADER, "", "Recovery Workbench", "", "Business requirements, Epic 1", "", CONTROL]
    parts += body
    parts.append("")
    parts.append(DELIVERY.rstrip("\n"))
    for code, short, name, wave in svc:
        parts.append(f"| {code} | RWB-SVC-{code} | {short} | {name} | {wave} |")
    parts.append("| ITG | RWB-ITG-W1 to RWB-ITG-W4, RWB-ITG-NFR | Integration harness per wave, and non-functional | Integration | 0 |")
    parts.append("")
    parts.append(
        "The service names above are the Ownership Map v1 service names; the requirement headings in "
        "section 3 keep the module names of version 4 (ASM-B-REQ-BRD-E1-9). The seven platform epics are "
        "RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE and RWB-PLT-OBS."
    )
    parts.append(WAVES.rstrip("\n"))

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    leg = plan["legacy"]
    slices = {s["id"]: s for s in plan["slices"]}
    pos = {c: n for c, n, _s, _w in svc}

    body_text = "\n".join(body)
    keys = re.findall(r"(?m)^\| (RWB-E1-\d{3}|RWB-ACE-001) \| ([^|]+)\|", body_text)
    names = {c: n2 for c, n2, _s, _w in svc}
    rows = []
    for key, title in keys:
        title = title.strip()
        v = leg.get(key)
        if key in RETIRED:
            rows.append((key, title, "None", "-", "-", "-", "No story: retired by D-RCV-60"))
            continue
        if key in CANCELLED:
            rows.append((key, title, "None", "-", "-", "-", "No story: already cancelled before this run"))
            continue
        if v is None:
            rows.append((key, title, "None", "-", "-", "-", "Removed by D-RCV-35, no story"))
            continue
        primary = v.get("primary", "")
        wave = v.get("wave", "")
        n = len(v.get("slices", []))
        if primary == "PLT":
            epics = [slices[x]["epic"] for x in v["slices"] if x in slices and slices[x]["epic"].startswith("RWB-PLT")]
            epic = max(sorted(set(epics)), key=epics.count) if epics else "-"
            svc_cell = "Platform"
        else:
            epic = f"RWB-SVC-{primary}"
            svc_cell = f"{primary} {names.get(primary, '-')}"
        be = sorted({slices[x]["business_epic"] for x in v["slices"] if x in slices})
        text = DISP.get(v["disposition"], v["disposition"])
        if "{}" in text:
            text = text.format(f"{n} story" if n == 1 else f"{n} stories")
        rows.append((key, title, epic, svc_cell, wave, ", ".join(be) or "-", text))

    for r in rows:
        parts.append("| " + " | ".join(str(x) for x in r) + " |")

    parts.append("")
    parts.append(
        "A key with no service epic is not built: RWB-E1-014 is retired by D-RCV-60 and RWB-E1-029 and "
        "RWB-E1-048 were cancelled before this run (section 8.5). The eight removed keys keep their text "
        "and their later home. No requirement text, key, count or date in sections 1 to 7 is changed by "
        "this version; the five positions in section 8.5 and the positions in this table are the only "
        "delivery statements added."
    )

    doc = "\n".join(parts) + "\n"
    SCRATCH.write_text(doc, encoding="utf-8")
    OUT_MD.write_text(doc, encoding="utf-8")
    print("WROTE", SCRATCH)
    print("WROTE", OUT_MD)
    print("trace rows", len(rows), "service rows", len(svc) + 1)


if __name__ == "__main__":
    main()
