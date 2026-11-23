"""B-REQ-BRD-E2: build Recovery Workbench Business Requirements Epic 2 v3 (md) + registers.

Reads the converted source text, the split plan (legacy + slices + stats), the ownership
plan and the Ownership Map. Writes the md to the scratch folder and the two jsonl
registers. Never edits a source file.
"""
import json, re
from pathlib import Path

import openpyxl

ROOT = Path(".")
WP = "B-REQ-BRD-E2"
SCRATCH = ROOT / "_work/msr/docs" / WP
SRC = ROOT / "_work/msr/extract/Recovery Workbench Business Requirements Epic 2 v2.md"
PLAN = json.loads((ROOT / "_work/msr/plan/split_plan.json").read_text(encoding="utf-8"))
LEGACY, SLICES = PLAN["legacy"], PLAN["slices"]
OUT_MD = SCRATCH / "Recovery Workbench Business Requirements Epic 2 v3.md"

# ---------------------------------------------------------------- services (Ownership Map)
wb = openpyxl.load_workbook(ROOT / "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx",
                            data_only=True)
SVC = {}
for row in wb["Services"].iter_rows(min_row=2, values_only=True):
    if row[0]:
        SVC[row[0]] = {"service": row[1], "name": row[2], "wave": str(row[3])}

# ---------------------------------------------------------------- registers
GAPS = [
    {
        "id": f"CG-{WP}-1",
        "title": "RWB-E2-023 Automated EFS file load has no legacy story and no slice in the plan",
        "source": "Business Requirements Epic 2 v2.docx section 3.2 RWB-E2-023; _work/msr/plan/split_plan.json (legacy and slices); _work/msr/plan/legacy_index.json",
        "section": "Section 3.2 and section 9",
        "description": "The requirement is stated at development detail under the P2 Integration heading, but the plan holds no RWB-E2-023 legacy row and no slice carries that legacy key, so the requirement has no service epic, no story and no build lane in wave 2.",
        "evidence": "The plan's legacy block holds 41 RWB-E2 keys and none of them is RWB-E2-023; no row of split_plan slices carries legacy RWB-E2-023; the legacy index has no RWB-E2-023 row.",
        "type": "Missing",
        "area": "Requirements and story split",
        "severity": "P2",
        "needed_by_wave": "2 (tentative)",
        "legacy_ref": "RWB-E2-023",
        "owner_role": "Product owner with the data product owner",
        "asm": f"ASM-{WP}-6",
        "proposed": "Add a slice set for RWB-E2-023 with rwb-integration as primary service and register it in the plan before the wave 2 build starts.",
        "wp": WP,
    },
    {
        "id": f"CG-{WP}-2",
        "title": "Two open decisions name individuals as owners and the source states no role for either",
        "source": "Business Requirements Epic 2 v2.docx section 7, rows DL03 and DL09; AGENTS.md rule 4",
        "section": "Section 7.1 and section 10.5",
        "description": "DL03 names one individual with the architecture team and DL09 names two individuals. Run rule 4 forbids the name of a person anywhere, so the owner cells carry roles instead, and the source does not say which role holds either decision.",
        "evidence": "The owner cell of DL03 reads as a person and the architecture team; the owner cell of DL09 reads as two people.",
        "type": "Missing",
        "area": "Governance",
        "severity": "P3",
        "needed_by_wave": "2 (tentative)",
        "legacy_ref": "DL03, DL09",
        "owner_role": "Product owner",
        "asm": f"ASM-{WP}-8",
        "proposed": "Name the role that holds DL03 and DL09 when each decision is answered, and keep the role in place of the individual in every future version.",
        "wp": WP,
    },
    {
        "id": f"CG-{WP}-3",
        "title": "The document control block says Version 1 and 28 October 2026 while the source file is v2 and this version is 3",
        "source": "Business Requirements Epic 2 v2.docx metadata table; Template and Rules v1 R8.2",
        "section": "Metadata table and section 10.3",
        "description": "The metadata table carries Version 1 and the date 28 October 2026; the file it sits in is v2 and the next version in the family is v3. Both source values are kept word for word and the realignment values are added beside them, so no reader has to guess which is which.",
        "evidence": "The metadata table rows Version and Date; the file name ends v2; the family's highest version in the folder is v2.",
        "type": "Ambiguous",
        "area": "Document control",
        "severity": "P3",
        "needed_by_wave": "2 (tentative)",
        "legacy_ref": "Not applicable",
        "owner_role": "Product owner",
        "asm": "",
        "proposed": "Correct the metadata table at the next human edit so the version and the date match the file name.",
        "wp": WP,
    },
    {
        "id": f"CG-{WP}-4",
        "title": "Ten Epic 2 legacy keys in the plan have no requirement row in this BRD",
        "source": "Business Requirements Epic 2 v2.docx section 3 (32 requirements); _work/msr/plan/split_plan.json legacy block (41 RWB-E2 keys)",
        "section": "Section 9",
        "description": "The plan builds Epic 2 stories from 41 legacy keys and this BRD states 32 requirements. The ten keys with no row here are built from another source, so a reader cannot trace them to a requirement in this document.",
        "evidence": "Set difference between the plan's RWB-E2 keys and the requirement rows of section 3.",
        "type": "Missing",
        "area": "Traceability",
        "severity": "P3",
        "needed_by_wave": "2 (tentative)",
        "legacy_ref": "RWB-E2 keys listed in section 9",
        "owner_role": "Product owner with the business lead",
        "asm": "",
        "proposed": "Name the source document of each key in the traceability file, or add the requirement to the next version of this BRD.",
        "wp": WP,
    },
    {
        "id": f"CG-{WP}-5",
        "title": "RWB-E2-032 is conditional on a model existing and no decision row names who confirms it",
        "source": "Business Requirements Epic 2 v2.docx section 3.10 RWB-E2-032; _work/msr/plan/split_plan.json slices for RWB-E2-032",
        "section": "Section 3.10 and section 9",
        "description": "The requirement exposes the TDR offer-suggestion model if the model exists and carries the priority Could, but section 7 holds no decision row and the plan builds five slices for it, so the condition is neither owned nor dated.",
        "evidence": "The words 'if the model exists' in the requirement; the priority Could; no DL row about the model; the slice count in the plan.",
        "type": "Ambiguous",
        "area": "Requirements",
        "severity": "P3",
        "needed_by_wave": "2 (tentative)",
        "legacy_ref": "RWB-E2-032",
        "owner_role": "Restructure operations officer with the TDR team",
        "asm": "",
        "proposed": "Add a decision row that names who confirms the model exists and the date the answer is needed.",
        "wp": WP,
    },
]

ASMS = [
    {
        "id": f"ASM-{WP}-1",
        "text": "Epic 2 carries the business epic tag EP02 and wave 2 of the wave map.",
        "why": "The source names the epic as Epic 2 and Foundation 2; it does not use the run's EP01-EP08 tags or waves.",
        "read": "The plan's every RWB-E2 slice carries business_epic EP02 and wave 2, and Template and Rules R5.6 maps EP02 to wave 2.",
        "gap": "",
        "applied_in": "Sections 8.3, 9 and 10.1",
        "confidence": "High",
        "confirm": "Programme office",
        "impact": "None on the requirement text; it fixes the tag and the wave used in the trace table.",
        "wp": WP,
    },
    {
        "id": f"ASM-{WP}-2",
        "text": "The Delivery model and the requirement-to-service-epic trace table are added from the run's plan, not from the source document.",
        "why": "The source BRD has seven sections and no statement of services, waves, contract-first delivery or service ownership.",
        "read": "Template and Rules R4, R5.1, R5.2, R5.6, R5.7 and R8.4, the Ownership Map Services sheet and the plan's legacy and slices blocks supply every value.",
        "gap": "",
        "applied_in": "Sections 8, 9 and 10.1",
        "confidence": "High",
        "confirm": "Product owner and solution architect",
        "impact": "Adds two sections; changes no requirement, priority, number or date.",
        "wp": WP,
    },
    {
        "id": f"ASM-{WP}-3",
        "text": "The module codes P1 to P10 of section 3 are read as the service epics RWB-SVC-P1 to RWB-SVC-P10, and the business names the source uses (recovery data store, document hub, case store) are kept as business names only.",
        "why": "The source groups requirements by business module; the run gives one epic per service and the same ten codes.",
        "read": "Template and Rules R4 fixes the codes and the service names; the Ownership Map Services sheet confirms them; the plan's slices name the epic of each story.",
        "gap": "",
        "applied_in": "Sections 8.1, 9 and 10.3",
        "confidence": "High",
        "confirm": "Solution architect",
        "impact": "None on the requirement text.",
        "wp": WP,
    },
    {
        "id": f"ASM-{WP}-4",
        "text": "No requirement text, identifier, priority, count or date of the source is changed. The edits are the two header lines, the added metadata rows, the tentative marking of the release date, two owner cells written as roles, and sections 7.1 and 8 to 10.",
        "why": "The work package keeps business content unchanged and changes only what the realignment needs.",
        "read": "A line-by-line comparison of the source text with this version, recorded in section 10.3 and in the edit log.",
        "gap": "",
        "applied_in": "Whole document; section 10.3",
        "confidence": "High",
        "confirm": "Product owner",
        "impact": "A reviewer can diff the two versions and see every change.",
        "wp": WP,
    },
    {
        "id": f"ASM-{WP}-5",
        "text": "Where a service epic's Architecture v5 wave is later than wave 2 — S3 rwb-guarantee, S4 rwb-litigation and S9 rwb-partner in this epic — the plan's wave 2 governs for the Epic 2 stories, and the conflict gap is raised once per service and business epic in the service work packages, not here.",
        "why": "The wave map keeps the earlier wave for a story and asks for one conflict gap per service and business epic; raising it here as well would duplicate it.",
        "read": "Template and Rules R5.6 and R5.7; the Ownership Map wave column against the wave 2 of EP02; the plan's wave 2 on every Epic 2 slice.",
        "gap": "",
        "applied_in": "Sections 8.3 and 9",
        "confidence": "Medium",
        "confirm": "Solution architect and the S3, S4 and S9 service owners",
        "impact": "The trace table shows both waves so the reader sees the difference without a second gap row.",
        "wp": WP,
    },
    {
        "id": f"ASM-{WP}-6",
        "text": "RWB-E2-023 is read as module P2 Integration from its section heading, which is the only source that places it.",
        "why": "The requirement has no legacy story row and no slice, so the plan cannot place it.",
        "read": "Section 3.2 heading P2 Integration holds the requirement; gap CG-" + WP + "-1 records the missing story and slice.",
        "gap": f"CG-{WP}-1",
        "applied_in": "Sections 3.2, 8.1 and 9",
        "confidence": "Medium",
        "confirm": "Product owner and the rwb-integration service owner",
        "impact": "The trace table names RWB-SVC-P2 for the requirement and says no story exists.",
        "wp": WP,
    },
    {
        "id": f"ASM-{WP}-7",
        "text": "The document is issued as Draft without human approval in this run; the approval table of section 10.2 is left empty for the approvers.",
        "why": "The realignment run records missing approval as an assumption and continues in Draft.",
        "read": "D-RCV-60 run rule 8 and Template and Rules R1 U8.",
        "gap": "",
        "applied_in": "Metadata table, section 10.2",
        "confidence": "High",
        "confirm": "Product owner, business owner, architecture, security and compliance approvers",
        "impact": "The document cannot be treated as approved until section 10.2 is signed.",
        "wp": WP,
    },
    {
        "id": f"ASM-{WP}-8",
        "text": "The individual names in the owner cells of DL03 and DL09 are replaced by the role that appears to hold the decision, and the replacement is recorded here rather than in the decision text.",
        "why": "Run rule 4 forbids the name of a person anywhere, and the source does not state the role.",
        "read": "DL03 reads as the architecture lead with the architecture team; DL09 reads as the business lead with the test lead. Gap CG-" + WP + "-2 records that the source states no role.",
        "gap": f"CG-{WP}-2",
        "applied_in": "Section 7 and section 7.1",
        "confidence": "Medium",
        "confirm": "Product owner and the owners of DL03 and DL09",
        "impact": "Two owner cells name a role instead of a person; no question, answer or date changes.",
        "wp": WP,
    },
    {
        "id": f"ASM-{WP}-9",
        "text": "The source carries no business-rule or key-performance identifiers, so none is added; the program requirement identifiers REQ-* of section 4 are the testable statements this BRD gives.",
        "why": "Adding rule or measure identifiers would invent content the source does not have.",
        "read": "The seven sections of the source: section 3 requirements, section 4 program requirements, section 5 support, section 6 acceptance, section 7 decisions.",
        "gap": "",
        "applied_in": "Sections 4, 9 and 10.4",
        "confidence": "High",
        "confirm": "Product owner and business lead",
        "impact": "A reader looking for rule or measure identifiers is pointed to REQ-* and to the Business Rules and Routing Logic document.",
        "wp": WP,
    },
]

# ---------------------------------------------------------------- source text (sections 1-7)
src_lines = SRC.read_text(encoding="utf-8").splitlines()
start = next(i for i, l in enumerate(src_lines) if l.startswith("# 1. What this epic delivers"))
body = "\n".join(src_lines[start:]).rstrip() + "\n"

REPL = [
    ("Epic 2, Foundation 2, releases on 31 December 2026.",
     "Epic 2, Foundation 2, releases on 31 December 2026 (tentative)."),
    ("| K. Book with the architecture team |", "| Architecture lead with the architecture team |"),
    ("| K. Tee with K. Jao |", "| Business lead with the test lead |"),
]
for a, b in REPL:
    assert a in body, f"source text not found: {a[:40]}"
    body = body.replace(a, b)

# ---------------------------------------------------------------- section 3 rows (source order)
sec3 = body.split("# 3. Requirements at development detail")[1].split("# 4. Program requirements")[0]
BR_ROWS, module = [], None
for line in sec3.splitlines():
    m = re.match(r"^## 3\.\d+ (P\d+) (.+?)\s*$", line)
    if m:
        module = (m.group(1), m.group(2))
        continue
    m = re.match(r"^\| (RWB-E2-\d{3}) \| (.*?) \|", line)
    if m and module:
        BR_ROWS.append({"key": m.group(1), "title": m.group(2), "module": module[0], "module_name": module[1]})

# ---------------------------------------------------------------- trace data
plan_keys = sorted(k for k in LEGACY if k.startswith("RWB-E2-"))
brd_keys = {r["key"] for r in BR_ROWS}
missing = [k for k in plan_keys if k not in brd_keys]

rows, primary_count, touched = [], {}, {}
for r in BR_ROWS:
    key, mod = r["key"], r["module"]
    sl = [s for s in SLICES if s["legacy"] == key]
    code = LEGACY.get(key, {}).get("primary", mod)
    epic = f"RWB-SVC-{code}"
    others, seen = [], set()
    for s in sl:
        e = s["epic"]
        if e != epic and e not in seen:
            seen.add(e)
            others.append(e)
    primary_count[epic] = primary_count.get(epic, 0) + 1
    for e in others:
        if e.startswith("RWB-SVC-"):
            touched.setdefault(e, []).append(key)
    wave = LEGACY.get(key, {}).get("wave", 2)
    disposition = LEGACY.get(key, {}).get("disposition", "")
    if sl:
        trace = f"{disposition}, {len(sl)} stories"
    else:
        trace = f"No story in the plan (CG-{WP}-1; ASM-{WP}-6)"
    rows.append({
        "key": key, "title": r["title"], "epic": epic, "svc": SVC[code]["service"],
        "others": ", ".join(others) if others else "None",
        "be": "EP02", "wave": wave, "svc_wave": SVC[code]["wave"], "trace": trace,
    })

# ---------------------------------------------------------------- build the document
L = []
A = L.append

A("SCB Collections and Recovery. Henka Group, 22 November 2026.")
A("(C) Siam Commercial Bank and Henka Pte Ltd")
A("")
A("Recovery Workbench")
A("")
A("Business requirements, Epic 2")
A("")
A("SCB Collections and Recovery. Henka Group, 28 October 2026")
A("")
A("| Item | Detail |")
A("|---|---|")
A("| Document | Recovery Workbench business requirements, Epic 2 |")
A("| Version | 1 |")
A("| Date | 28 October 2026 |")
A("| Prepared by | Henka Group |")
A("| Release | 31 December 2026 (tentative) |")
A("| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |")
A("| Realigned version | 3 |")
A("| Realignment date | 22 November 2026 |")
A("| Realignment decision | D-RCV-60 microservice realignment |")
A("| Status | Draft |")
A("| Author of this version | BRD Builder (AI draft) |")
A("| Reviewers | The five approvers of section 10.2 |")
A("| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |")
A("")
A(body.rstrip())
A("")

# 7.1
A("## 7.1 Effect of the realignment on these decisions")
A("")
A("The ten decisions keep their identifiers, questions, answers and dates. Four of them meet a fact that Architecture v5 fixes; the table says which fact, without answering the decision for its owner.")
A("")
A("| Decision | Fact the realignment fixes | Where it is recorded |")
A("|---|---|---|")
A("| DL03 | Partner access is delivered on the partner gateway in the DMZ, and the partner service epic RWB-SVC-S9 rwb-partner sits in wave 4. Who makes the architecture change stays open. | ADR-019; section 8.1 |")
A("| DL18 | The delegation of authority table is held by rwb-access (P4) as versioned reference data; the levels and limits load as parameters until the holders are signed. | Ownership Map rulings (delegation_limit); REQ-APD-001 and REQ-APD-010 |")
A("| DL30 | The realignment fixes 19 services and one epic per service, so each capability in the question sits with the service that owns it; A or B is no longer the frame. | D-RCV-60, DL44 and DL45; sections 8.1 and 9 |")
A("| DL31 | Screen design sits on the gateway-bff composite routes of the edge, with the TechX designer under the product owner unchanged. | ADR-019; pattern DP-19; section 8.4 |")
A("")
A("The other six decisions — DL09, DL10, DL22, DL23, DL28 and DL39 — are unaffected by the realignment.")
A("")

# 8. Delivery model
A("# 8. Delivery model")
A("")
A("Epic 2 is delivered as wave 2 of a programme of 19 service epics, 7 platform epics and 5 integration epics. Every story carries this business epic, EP02, as a tag beside its service epic, and every service epic in this section is named, numbered and waved exactly as the Ownership Map and the run's story template and rules write it. Nothing in this section changes a requirement: it says who delivers each part of the epic and in what order the contracts are published.")
A("")
A("## 8.1 The 19 service epics")
A("")
A("| Code | Service epic | Service | Module name | Wave (Architecture v5) |")
A("|---|---|---|---|---|")
for code in sorted(SVC, key=lambda c: (c[0] != "P", int(c[1:]))):
    A(f"| {code} | RWB-SVC-{code} | {SVC[code]['service']} | {SVC[code]['name']} | {SVC[code]['wave']} |")
A("")
A("One epic per service, so that each capability has its own code, release, owner, contract, schema, topic and task queue. A service owns its schema, its login, its REST base (/api/recovery/<short>/v1), its topic (rwb.<short>.events.v1) with retry and dead-letter topics, its Temporal task queue (rwb-<short>) and its Java package. The shared platform — the edge, Kafka, the Temporal layer, the database schemas and observability — is not one of the 19. The values are the service's name, base and queue as the Ownership Map writes them, and a reader who needs them reads that map.")
A("")
A("## 8.2 Platform and integration epics")
A("")
A("| Epic | What it delivers | Wave |")
A("|---|---|---|")
A("| RWB-PLT-TPL | Service template and repositories | 0 |")
A("| RWB-PLT-LIB | Shared libraries | 0 |")
A("| RWB-PLT-WF | Temporal workflow platform | 0 |")
A("| RWB-PLT-DB | ACE database schemas and logins | 0 |")
A("| RWB-PLT-EVT | Kafka event platform | 0 |")
A("| RWB-PLT-EDGE | Edge and gateway | 0 |")
A("| RWB-PLT-OBS | Observability | 0 |")
A("| RWB-ITG-W1 | Integration harness for wave 1 | 1 |")
A("| RWB-ITG-W2 | Integration harness for wave 2 | 2 |")
A("| RWB-ITG-W3 | Integration harness for wave 3 | 3 |")
A("| RWB-ITG-W4 | Integration harness for wave 4 | 4 |")
A("| RWB-ITG-NFR | Non-functional integration work | 0 |")
A("")
A("## 8.3 Waves and the business epic tags")
A("")
A("| Business epic | Wave |")
A("|---|---|")
A("| EP01 | 1 |")
A("| EP02 | 2 |")
A("| EP03 | 2 |")
A("| EP04 | 3 |")
A("| EP05 | 3 |")
A("| EP06, EP07, EP08 | 4 |")
A("| Platform and non-functional | 0 |")
A("")
A("Epic 2 is EP02 and therefore wave 2, releasing on 31 December 2026 (tentative). A story whose wave in this map is earlier than its service's wave in Architecture v5 keeps the earlier wave, and the difference is raised once per service and business epic in the service's own work package. In this epic the difference falls on S3 rwb-guarantee (wave 3), S4 rwb-litigation (wave 3) and S9 rwb-partner (wave 4); the trace table of section 9 shows both numbers.")
A("")
A("## 8.4 Contract-first delivery")
A("")
A("The build order inside every service epic follows the contract, not the screen.")
A("")
A("- **A contract story first, on Day 1.** Every service epic starts with a contract story that publishes the operations, the events and the shapes it will answer to. A contract story has no build dependency and sits in the contract group of its wave.")
A("- **Application stories build against the published contract and its fake.** A dependency on another service's contract never blocks a build, because the fake answers it; only a dependency inside the same service, or on a platform contract story, waits.")
A("- **Real cross-service behaviour is integration work.** It sits only on integration stories of the wave harness, never on an application story.")
A("- **One REST hop with a 2 s timeout.** A screen calls the edge, the edge calls one service, and the service answers from its own data or from one published contract.")
A("- **Facts travel as events.** A published fact goes out through the outbox on the owner's topic and is consumed through the inbox, with retry and dead-letter topics.")
A("- **Long running work is a workflow.** Steps that outlive a request run on the Temporal layer, with a child workflow per stage of a case and a schedule in place of a scheduler job.")
A("- **Rules are embedded per service and registered centrally.** Each service evaluates the rule packages it uses, and the package registry and its versions live in rwb-decision.")
A("- **The owner of a story is a suggestion.** Every story names a team type — TechX for contracts and application code, the ACE team for database work, SCB IT infrastructure for infrastructure, the DevOps team for operations, and the QA team for the harness and the non-functional work — and any team may pick the story up. Every team type therefore has Day-1 work in wave 2.")
A("")
A("A story identifier reads RWB-<scope>-<legacy compact>-<work type>, with a -2 suffix on the delta copy of a preserved story. The work types are CON, APP, DB, INF, OPS and ITG.")
A("")

# 9. Traceability
A("# 9. Requirement to service epic traceability")
A("")
A("Every requirement of section 3 is delivered by the service epic named below as primary, with the other service epics and the wave 2 integration harness taking part where the plan gives them a story. The primary service epic is the one the plan names for the requirement, and the business epic is EP02 for all 32 requirements.")
A("")
A("| Service epic | Service | Requirements where it is primary | Requirements it also takes part in |")
A("|---|---|---|---|")
for epic in sorted(primary_count, key=lambda e: int(e.split("-")[-1][1:]) + (0 if e.split("-")[-1][0] == "P" else 100)):
    code = epic.split("-")[-1]
    also = touched.get(epic, [])
    A(f"| {epic} | {SVC[code]['service']} | {primary_count[epic]} | "
      f"{len(also) if also else 0} |")
A("| RWB-ITG-W2 | Integration harness for wave 2 | 0 | "
  f"{sum(1 for r in rows if 'RWB-ITG-W2' in r['others'])} |")
A("")
A("| Requirement | Requirement title | Primary service epic | Other service epics and the harness | Business epic | Wave | Service wave (Architecture v5) | Stories in the plan |")
A("|---|---|---|---|---|---|---|---|")
for r in rows:
    A(f"| {r['key']} | {r['title']} | {r['epic']} | {r['others']} | {r['be']} | {r['wave']} | "
      f"{r['svc_wave']} | {r['trace']} |")
A("")
A(f"The plan holds {len(plan_keys)} Epic 2 legacy keys against the {len(BR_ROWS)} requirements above. The {len(missing)} keys with no requirement row here are "
  + ", ".join(k.replace("RWB-", "") for k in missing)
  + f" (CG-{WP}-4); they are built from another source. RWB-E2-023 is the one requirement with no story and no slice (CG-{WP}-1; ASM-{WP}-6), and RWB-E2-011 is the one requirement the plan moves without impact on its content.")
A("")

# 10. control, decisions, approval, change log, sources, registers
A("# 10. Document control and change log")
A("")
A("## 10.1 Decisions this version adopts")
A("")
A("Each identifier below is allocated in the run's identifier plan and recorded in the Decision Log and the architecture decision records of this run. This document adopts them; it does not approve them, and a reader who needs the decision itself reads that record.")
A("")
A("| ID | Decision | Where it applies in this document |")
A("|---|---|---|")
A("| D-RCV-60 | Adopt Architecture v5 and realign the documents and the stories | Header, sections 8 to 10 |")
A("| DL44 | Adopt Architecture v5 | Sections 8 and 9 |")
A("| DL45 | Service epics plus business-epic tags | Sections 8.1, 8.3 and 9 |")
A("| DL46 | Soft ownership by team type | Section 8.4 |")
A("| DL47 | Epic 1 preservation rule | Whole document: no Epic 1 requirement is rewritten here |")
A("| DL48 | Dates unchanged and tentative | Metadata table, section 1 |")
A("| DL49 | Gap and assumption registers | Section 10.5 |")
A("| ADR-013 | 19 services inside ACE; supersedes the single-service decision | Section 8.1 |")
A("| ADR-014 | Schema and login per service in ACE PostgreSQL | Section 8.1 |")
A("| ADR-015 | Kafka with outbox, inbox and CloudEvents | Section 8.4 |")
A("| ADR-016 | Reusable Temporal layer; schedules replace the scheduler | Section 8.4 |")
A("| ADR-017 | Embedded rules per service; rule registry in rwb-decision | Sections 8.4 and 9 |")
A("| ADR-018 | No data lake; reporting read model from events | Sections 3.9 and 8.4 |")
A("| ADR-019 | Edge: gateway-bff and partner gateway | Sections 7.1 and 8.4 |")
A("| ADR-020 | Contract-first REST, one hop, 2 s timeout | Sections 8.4 and 9 |")
A("| ADR-021 | Per-service migration ownership | Section 8.1 |")
A("| ADR-022 | Local decision record plus central ledger | Sections 3.7 and 8.4 |")
A("| ADR-023 | Observability per service | Section 8.4 |")
A("")
A("## 10.2 Approval")
A("")
A("The table is left empty for the people who approve this version. Until it is signed the document is Draft.")
A("")
A("| Role | Name | Decision | Date |")
A("|---|---|---|---|")
A("| Product Owner |  |  |  |")
A("| Business owner |  |  |  |")
A("| Architecture |  |  |  |")
A("| Security |  |  |  |")
A("| Compliance |  |  |  |")
A("")
A("## 10.3 Change log")
A("")
A("| Version | Date | Change | Tool |")
A("|---|---|---|---|")
A("| 3 | 22 November 2026 | D-RCV-60 microservice realignment: two header lines; metadata rows for the realigned version, date, decision, status and tool; the release date marked tentative; two owner cells written as roles; section 7.1 on the effect of the realignment; section 8 Delivery model; section 9 requirement to service epic traceability; section 10 document control. No requirement, identifier, priority, count or date changes. | T3 Code / OpenCode / DeepSeek v4.1 Flash |")
A("")
A("Version 1 is the version the metadata table names and version 2 is the file this version was read from; both values are kept as the source writes them (CG-" + WP + "-3).")
A("")
A("## 10.4 Traceability to sources")
A("")
A("| Content | Source |")
A("|---|---|")
A("| Sections 1 to 7 | Recovery Workbench Business Requirements Epic 2 v2.docx, converted text |")
A("| Header lines and the change-log row | Microservice Story Template and Rules v1, R8.1 and R8.2 |")
A("| The 19 service epics, their names and waves | Ownership Map v1, Services sheet; Template and Rules R4 |")
A("| Platform and integration epics | Template and Rules R5.1 |")
A("| Wave map and the conflict rule | Template and Rules R5.6 and R5.7 |")
A("| Contract-first order, work types and suggested owners | Template and Rules R5.2, R5.3 and R5.7 |")
A("| Primary service epic, other service epics, story counts and dispositions | split_plan.json, legacy and slices blocks, for each RWB-E2 key |")
A("| Delegation of authority ownership | Ownership Map rulings, delegation_limit |")
A("| Decision, ADR and DL identifiers | ids.json; Template and Rules R8.4 |")
A("| Personal-data classes | This version's classification of the requirements of section 3; no source states a classification |")
A("")
A("## 10.5 Gaps and assumptions in this version")
A("")
A("Each row is a candidate in the run's registers and is numbered with the other work packages.")
A("")
A("| ID | Kind | Statement |")
A("|---|---|---|")
for g in GAPS:
    A(f"| {g['id']} | Gap ({g['type']}, {g['severity']}) | {g['title']} |")
for a in ASMS:
    A(f"| {a['id']} | Assumption ({a['confidence']}) | {a['text']} |")
A("")
A("## 10.6 Personal data in this epic")
A("")
A("The requirements touch personal data and financial data. The classes below are this version's classification, made from the requirement text; no source document states one, and no real customer, message, account or amount appears anywhere in this document.")
A("")
A("| Class | Where it appears | Handling the requirement already states |")
A("|---|---|---|")
A("| PII | Contact points and contact history, letters and their proof of delivery, messages on SMS and LINE, partner users of the partner portal (REQ-CHO-003, REQ-ILG-009, REQ-OCC-003, REQ-OCC-004, REQ-ACA-012) | Contact stops and consent withdrawal are applied on the channel and the case; partner users are scoped to their own cases through the external gateway |")
A("| SENSITIVE_FINANCIAL | Payments and matched amounts, plan and settlement terms, treatment records, booking confirmations, hearing and judgment dates and amounts (REQ-CHO-006, REQ-CHO-008, REQ-CHO-009, REQ-DCM-012) | Amounts are matched and recorded against the plan or the treatment; the requirement names the fact and the record, never a customer's figures |")
A("")

md = "\n".join(L)
SCRATCH.mkdir(parents=True, exist_ok=True)
if OUT_MD.exists():
    raise SystemExit(f"REFUSED: {OUT_MD} exists")
OUT_MD.write_text(md, encoding="utf-8")

for name, rows_ in (("gaps", GAPS), ("assumptions", ASMS)):
    p = ROOT / "_work/msr" / name / f"{WP}.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows_) + "\n", encoding="utf-8")

print("WROTE", OUT_MD, len(md.splitlines()), "lines")
print("BR rows", len(BR_ROWS), "plan keys", len(plan_keys), "unmapped", missing)
print("primary", primary_count)
print("gaps", len(GAPS), "assumptions", len(ASMS))
