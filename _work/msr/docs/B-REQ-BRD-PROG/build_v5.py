"""Build Recovery Workbench Business Requirements Program v5 (D-RCV-60).

Reads the v4 extract read-only, applies the realignment changes, writes:
  _work/msr/docs/B-REQ-BRD-PROG/Recovery Workbench Business Requirements Program v5.md  (docx source)
  03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.md
Never edits the source. Refuses to overwrite an existing output.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "_work/msr/extract/Recovery Workbench Business Requirements Program v4.md"
OUT_SCRATCH = ROOT / "_work/msr/docs/B-REQ-BRD-PROG/Recovery Workbench Business Requirements Program v5.md"
OUT_DOC = ROOT / "03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.md"

CG = "CG-B-REQ-BRD-PROG"
ASM = "ASM-B-REQ-BRD-PROG"


def rep(text, old, new, why):
    if text.count(old) != 1:
        raise SystemExit(f"REPLACEMENT NOT UNIQUE ({text.count(old)}): {why}")
    return text.replace(old, new)


t = SRC.read_text(encoding="utf-8")

# ---------------------------------------------------------------- 1. title block
t = rep(t,
        "Business requirements, program\n\nSCB Collections and Recovery. Henka Group, 15 November 2026",
        "Business requirements, program\n\nSCB Collections and Recovery. Henka Group, 22 November 2026",
        "title block date")

# ---------------------------------------------------------------- 2. document control
t = rep(t, "| Version | 4 |", "| Version | 5 |", "version")
t = rep(t, "| Date | 15 November 2026 |", "| Date | 22 November 2026 |", "date")
t = rep(t, "| Prepared by | Henka Group |",
        "| Prepared by | Henka Group |\n| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |",
        "tool row")

V5_CHANGE = (
    "Version 5 is the D-RCV-60 microservice realignment. Requirement IDs, requirement text, targets, "
    "decision dates and the numbering of sections 1 to 9 are unchanged. Section 7 restates the three "
    "constraints that D-RCV-60 supersedes: the platform shape, the schema per service and the workflow "
    "engine. In section 9 the four owner cells that named persons are replaced by the placeholder in "
    "section 12 (root rule 4). New section 10 gives the delivery model: 19 service epics, seven platform "
    "and five integration epics, four waves and the contract-first build order. New section 11 traces "
    "every business requirement to its service epic and its business epic. New section 12 lists the gaps "
    "and assumptions this version raises. Release dates are marked tentative (U7, DL48)."
)

lines = t.splitlines()
i = next(n for n, l in enumerate(lines) if l.startswith("| Change | "))
lines.insert(i + 1, f"| Change (version 5) | {V5_CHANGE} |")
lines.insert(i + 2, "")
lines.insert(i + 3, "| Version | Date | Change | Author |")
lines.insert(i + 4, "|---|---|---|---|")
lines.insert(i + 5, "| 4 | 15 November 2026 | Version 4, as described in the Change row above | Henka Group |")
lines.insert(i + 6, "| 5 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |")
t = "\n".join(lines) + "\n"

# ---------------------------------------------------------------- 3. release dates tentative
for epic, date in (("E1", "30 Nov 2026"), ("E2", "31 Dec 2026"), ("E3", "31 Jan 2027"), ("E4", "28 Feb 2027"),
                   ("E5", "31 Mar 2027"), ("E6", "30 Apr 2027"), ("E7", "31 May 2027"), ("E8", "30 Jun 2027")):
    t = rep(t, f"| {epic} | {date} |", f"| {epic} | {date} (tentative) |", f"release {epic}")

# ---------------------------------------------------------------- 4. section 7 constraints
t = rep(t,
        "| Built on ACE | The Workbench is a module of ACE: one service, one repository, one front end |",
        "| Built on ACE | The Workbench is a module of ACE: 19 services in one ACE platform, one ACE database "
        "and one front end, with shape given by D-RCV-60 and ADR-013 (" + CG + "-5; " + ASM + "-3) |",
        "constraint Built on ACE")

t = rep(t,
        "| Modular monolith | Common, collection and recovery modules, with boundaries checked at build time |",
        "| Modular monolith | Superseded by D-RCV-60 and ADR-014: the recovery module is split into 19 services, "
        "each with its own schema, login, topic and task queue in the ACE database, and the boundaries are "
        "checked at build time (" + CG + "-5; " + ASM + "-4) |",
        "constraint Modular monolith")

t = rep(t,
        "| Programmatic workflow | Case, stage and task state held in the database and moved by code, in CMMN 1.1 "
        "terms. No Temporal |",
        "| Programmatic workflow | Superseded by D-RCV-60 and ADR-016: case, stage and task state is still held in "
        "the owner's database and is still described in CMMN 1.1 terms, but a case is moved by a durable workflow, "
        "with one parent case workflow and one child workflow per stage, and a schedule per job (" + CG + "-5; "
        + ASM + "-5) |",
        "constraint Programmatic workflow")

t = rep(t,
        "by 21 November 2026 for the 30 November release (DL43)",
        "by 21 November 2026 for the 30 November release (tentative) (DL43)",
        "ACE team dependency release date")

# ---------------------------------------------------------------- 5. section 9 owner cells
PH = f"Not specified in the source documents ({CG}-1; {ASM}-6)"
t = rep(t, "| K. Book with K. Pipat |", f"| {PH} |", "DL06 owner")
t = rep(t, "| K. Tony with K. Book |", f"| {PH} |", "DL12 owner")
t = rep(t, "| K. Tee with TechX and Henka |", f"| {PH} |", "DL13 owner")
t = rep(t, "| Solution architect with K. Book |", f"| Solution architect with {PH} |", "DL20 owner")

# ---------------------------------------------------------------- 6. new sections 10-12
TRACE = [
    ("REQ-RDF-001 to REQ-RDF-013", 13, "RWB-SVC-P1", "rwb-source-data", 1, "EP01"),
    ("REQ-RDF-014", 1, "RWB-SVC-P1", "rwb-source-data", 1, "EP02"),
    ("REQ-ILG-001 to REQ-ILG-008, REQ-ILG-014", 9, "RWB-SVC-P1", "rwb-source-data", 1, "EP01"),
    ("REQ-ILG-009 to REQ-ILG-013", 5, "RWB-SVC-P1", "rwb-source-data", 1, "EP02"),
    ("REQ-DRI-006 to REQ-DRI-008", 3, "RWB-SVC-P2", "rwb-integration", 1, "EP01"),
    ("REQ-DRI-013", 1, "RWB-SVC-P2", "rwb-integration", 1, "EP02"),
    ("REQ-CWC-001 to REQ-CWC-016", 16, "RWB-SVC-P3", "rwb-case", 1, "EP01"),
    ("REQ-CWC-017 to REQ-CWC-020", 4, "RWB-SVC-P3", "rwb-case", 1, "EP02"),
    ("REQ-CHO-001 to REQ-CHO-010", 10, "RWB-SVC-P3", "rwb-case", 1, "EP02"),
    ("REQ-WKM-001 to REQ-WKM-009, REQ-WKM-011 to REQ-WKM-016", 15, "RWB-SVC-P3", "rwb-case", 1, "EP02"),
    ("REQ-WKM-010", 1, "RWB-SVC-P3", "rwb-case", 1, "EP07"),
    ("REQ-DRI-010, REQ-DRI-011", 2, "RWB-SVC-P3", "rwb-case", 1, "EP01"),
    ("REQ-ACA-001 to REQ-ACA-010", 10, "RWB-SVC-P4", "rwb-access", 1, "EP01"),
    ("REQ-ACA-011, REQ-ACA-012", 2, "RWB-SVC-P4", "rwb-access", 1, "EP02"),
    ("REQ-ACA-013", 1, "RWB-SVC-P4", "rwb-access", 1, "EP08"),
    ("REQ-DCM-001 to REQ-DCM-011, REQ-DCM-014 to REQ-DCM-016, REQ-DCM-020", 15, "RWB-SVC-P5", "rwb-document", 1, "EP01"),
    ("REQ-DCM-012, REQ-DCM-013, REQ-DCM-017 to REQ-DCM-019", 5, "RWB-SVC-P5", "rwb-document", 1, "EP02"),
    ("REQ-OCC-001, REQ-OCC-002, REQ-OCC-007", 3, "RWB-SVC-P6", "rwb-comms", 1, "EP01"),
    ("REQ-OCC-003 to REQ-OCC-006, REQ-OCC-008 to REQ-OCC-010", 7, "RWB-SVC-P6", "rwb-comms", 1, "EP02"),
    ("REQ-OCC-011", 1, "RWB-SVC-P6", "rwb-comms", 1, "EP04"),
    ("REQ-DRI-001 to REQ-DRI-005, REQ-DRI-009", 6, "RWB-SVC-P7", "rwb-decision", 1, "EP01"),
    ("REQ-DRI-012", 1, "RWB-SVC-P7", "rwb-decision", 1, "EP02"),
    ("REQ-APD-001 to REQ-APD-011", 11, "RWB-SVC-P7", "rwb-decision", 1, "EP02"),
    ("REQ-S1-001 to REQ-S1-008", 8, "RWB-SVC-S1", "rwb-valuation", 3, "EP04"),
    ("REQ-S2-001 to REQ-S2-010", 10, "RWB-SVC-S2", "rwb-treatment", 2, "EP03"),
    ("REQ-S3-001 to REQ-S3-007", 7, "RWB-SVC-S3", "rwb-guarantee", 3, "EP04"),
    ("REQ-S4-001 to REQ-S4-010", 10, "RWB-SVC-S4", "rwb-litigation", 3, "EP05"),
    ("REQ-S5-001 to REQ-S5-005", 5, "RWB-SVC-S5", "rwb-asset", 2, "EP03"),
    ("REQ-S5-006 to REQ-S5-010", 5, "RWB-SVC-S5", "rwb-asset", 2, "EP04"),
    ("REQ-S6-001 to REQ-S6-003", 3, "RWB-SVC-S6", "rwb-debtsale", 3, "EP05"),
    ("REQ-S6-004 to REQ-S6-009", 6, "RWB-SVC-S6", "rwb-debtsale", 3, "EP06"),
    ("REQ-S7-001 to REQ-S7-008", 8, "RWB-SVC-S7", "rwb-writeoff", 4, "EP06"),
    ("REQ-DVH-001 to REQ-DVH-007, REQ-DVH-009, REQ-DVH-010", 9, "RWB-SVC-S8", "rwb-deviation", 2, "EP02"),
    ("REQ-DVH-008", 1, "RWB-SVC-S8", "rwb-deviation", 2, "EP03"),
    ("REQ-DVH-011", 1, "RWB-SVC-S8", "rwb-deviation", 2, "EP07"),
    ("REQ-S8-001 to REQ-S8-007", 7, "RWB-SVC-S8", "rwb-deviation", 2, "EP07"),
    ("REQ-S9-001 to REQ-S9-004, REQ-S9-008", 5, "RWB-SVC-S9", "rwb-partner", 4, "EP06"),
    ("REQ-S9-005 to REQ-S9-007, REQ-S9-009", 4, "RWB-SVC-S9", "rwb-partner", 4, "EP07"),
]

SERVICES = [
    ("RWB-SVC-P1", "P1", "rwb-source-data", "rwb_source_data", 1, "EP01 to EP02"),
    ("RWB-SVC-P2", "P2", "rwb-integration", "rwb_integration", 1, "EP01 to EP02"),
    ("RWB-SVC-P3", "P3", "rwb-case", "rwb_case", 1, "EP01, EP02, EP07"),
    ("RWB-SVC-P4", "P4", "rwb-access", "rwb_access", 1, "EP01, EP02, EP08"),
    ("RWB-SVC-P5", "P5", "rwb-document", "rwb_document", 1, "EP01 to EP02"),
    ("RWB-SVC-P6", "P6", "rwb-comms", "rwb_comms", 1, "EP01, EP02, EP04"),
    ("RWB-SVC-P7", "P7", "rwb-decision", "rwb_decision", 1, "EP01 to EP02"),
    ("RWB-SVC-P8", "P8", "rwb-payment", "rwb_payment", 2, "EP02 to EP08"),
    ("RWB-SVC-P9", "P9", "rwb-reporting", "rwb_reporting", 1, "EP01 to EP08"),
    ("RWB-SVC-P10", "P10", "rwb-agent", "rwb_agent", 1, "EP01 to EP08"),
    ("RWB-SVC-S1", "S1", "rwb-valuation", "rwb_valuation", 3, "EP04"),
    ("RWB-SVC-S2", "S2", "rwb-treatment", "rwb_treatment", 2, "EP03"),
    ("RWB-SVC-S3", "S3", "rwb-guarantee", "rwb_guarantee", 3, "EP04"),
    ("RWB-SVC-S4", "S4", "rwb-litigation", "rwb_litigation", 3, "EP05"),
    ("RWB-SVC-S5", "S5", "rwb-asset", "rwb_asset", 2, "EP03 to EP04"),
    ("RWB-SVC-S6", "S6", "rwb-debtsale", "rwb_debtsale", 3, "EP05 to EP06"),
    ("RWB-SVC-S7", "S7", "rwb-writeoff", "rwb_writeoff", 4, "EP06"),
    ("RWB-SVC-S8", "S8", "rwb-deviation", "rwb_deviation", 2, "EP02, EP03, EP07"),
    ("RWB-SVC-S9", "S9", "rwb-partner", "rwb_partner", 4, "EP06 to EP07"),
]

total = sum(r[1] for r in TRACE)
if total != 231:
    raise SystemExit(f"trace total is {total}, expected 231")


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


sec10 = []
sec10.append("")
sec10.append("# 10. Delivery model")
sec10.append("")
sec10.append(
    "Under D-RCV-60 the program is delivered as 19 service epics, seven platform epics and five integration "
    "epics, and every story also carries its business epic EP01 to EP08 as a tag (U1, DL45). The eight business "
    "epics keep the releases in section 8. The requirement IDs in section 5, their text, their priorities, their "
    "business owners and their epic column do not change; what this section adds is which epic delivers each "
    "requirement, in which wave, and in what order the work can start."
)
sec10.append("")
sec10.append("## 10.1 Epic structure")
sec10.append("")
sec10.append(table(
    ["Epic group", "Epics", "Count", "What the epic delivers"],
    [("Platform", "RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS", 7,
      "Service template and repositories, shared libraries, the workflow platform, the ACE database schemas and "
      "logins, the event platform, the edge and gateway, and observability"),
     ("Service", "RWB-SVC-P1 to RWB-SVC-S9", 19,
      "One epic per service, covering the contract, application, database, infrastructure, operations and "
      "integration work of that service"),
     ("Integration", "RWB-ITG-W1, RWB-ITG-W2, RWB-ITG-W3, RWB-ITG-W4, RWB-ITG-NFR", 5,
      "One integration harness per wave, and the non-functional work of section 6"),
     ("Business epic tag", "EP01 to EP08", 8,
      "The business release a requirement lands in; carried as a tag on every story, alongside the service epic")]))
sec10.append("")
sec10.append(
    "The platform epics deliver first, as wave 0, because every service epic builds on the template, the "
    "libraries, the workflow platform, the schemas and logins, the event platform, the edge and the "
    "observability baseline. RWB-PLT-EVT carries the event platform; the shared topic that every service "
    "writes its decision record to is rwb.decision-record.v1, and the Temporal namespace is rwb-recovery."
)
sec10.append("")
sec10.append("## 10.2 The 19 service epics and their waves")
sec10.append("")
sec10.append(
    "Each service epic is one service in the ACE platform, with its own schema and login in the ACE database, "
    "and each is reusable or replaceable on its own. The service, schema and wave are the Ownership Map "
    "entries (Ownership Map, Services sheet), which follow the Architecture v5 service catalogue (R-PREC rank 1)."
)
sec10.append("")
sec10.append(table(
    ["Service epic", "Module", "Service", "Schema", "Wave", "Business epics served"],
    SERVICES))
sec10.append("")
sec10.append(
    "Owner in delivery terms is a suggestion only: every service epic is picked up by TechX (suggested; any "
    "team may pick up this story), and the database, infrastructure and operations work inside it by the ACE "
    "team, SCB IT infrastructure and the DevOps team as their suggested owners. No owner is a named person "
    "(U3, DL46)."
)
sec10.append("")
sec10.append("## 10.3 Waves and releases")
sec10.append("")
sec10.append(
    "A wave groups the monthly releases that can be built together. The wave of a business epic is fixed: EP01 "
    "in wave 1, EP02 and EP03 in wave 2, EP04 and EP05 in wave 3, and EP06 to EP08 in wave 4, with platform and "
    "non-functional work in wave 0. A service is created in the wave shown in 10.2, so a service that a later "
    "wave needs first is created earlier rather than the requirement moving."
)
sec10.append("")
sec10.append(table(
    ["Wave", "Business epics in the wave", "Service epics created in the wave", "Release (tentative)"],
    [("0", "Platform and non-functional", "The seven platform epics and RWB-ITG-NFR", "Before EP01, November 2026"),
     ("1", "EP01", "RWB-SVC-P1, P2, P3, P4, P5, P6, P7, P9, P10", "30 Nov 2026"),
     ("2", "EP02, EP03", "RWB-SVC-P8, S2, S5, S8", "31 Dec 2026 and 31 Jan 2027"),
     ("3", "EP04, EP05", "RWB-SVC-S1, S3, S4, S6", "28 Feb 2027 and 31 Mar 2027"),
     ("4", "EP06, EP07, EP08", "RWB-SVC-S7, S9", "30 Apr 2027, 31 May 2027 and 30 Jun 2027"),
     ("per wave", "All", "RWB-ITG-W1 to RWB-ITG-W4, one harness per wave", "The same wave dates, tentative")]))
sec10.append("")
sec10.append(
    "The dates are the section 8 dates, unchanged and tentative (U7, DL48). The program finishes inside eight "
    "months of the first release."
)
sec10.append("")
sec10.append("## 10.4 Contract-first delivery")
sec10.append("")
sec10.append(
    "Every service publishes its contract before its build starts, and no service waits for another service "
    "to be built (ADR-020)."
)
sec10.append("")
sec10.append(
    "- The contract of a service is four things: its REST resources under /api/recovery/<short>/v1 behind "
    "gateway-bff, its topic rwb.<short>.events.v1 with its event names, its Temporal task queue rwb-<short> in "
    "the namespace rwb-recovery, and the call types it offers and accepts (REST, Kafka, Temporal, file)."
)
sec10.append(
    "- A contract story is Day 1 in every service epic and has no build dependency. Application stories build "
    "against the published contract and its fake, so a dependency on another service's contract never blocks "
    "a build."
)
sec10.append(
    "- One hop from the gateway, a two second timeout, and no service reads another service's tables or "
    "schema: each service owns its own schema and login, and only rwb-source-data holds SELECT on the ACE "
    "views (ADR-014, ADR-020)."
)
sec10.append(
    "- Events carry identifiers and facts, never personal data; each service writes to its own outbox in the "
    "same transaction as its state change and deduplicates through its inbox (ADR-015)."
)
sec10.append(
    "- Rules are governed in rwb-decision and evaluated in the owning service; a decision record is written "
    "locally and sealed in the central ledger (ADR-017, ADR-022)."
)
sec10.append(
    "- A case is moved by one parent case workflow with one child workflow per stage, and a job is a Temporal "
    "Schedule or an event-started workflow in the owning service; no shared scheduler table remains (ADR-016)."
)
sec10.append(
    "- There is no data lake: reporting is a read model built from events into rwb-reporting, and the data lake "
    "interfaces and the daily copy are removed (ADR-018)."
)
sec10.append(
    "- Users reach the Workbench through gateway-bff, and partners through the partner gateway in the DMZ "
    "(ADR-019)."
)
sec10.append("")
sec10.append("## 10.5 Ownership of the shared items")
sec10.append("")
sec10.append(
    "Where a requirement in section 5 needs a shared item, the owner is taken from the Ownership Map, not "
    "from the module the requirement happens to sit under."
)
sec10.append("")
sec10.append(table(
    ["Shared item", "Owner", "Basis"],
    [("Parameters and reference data", "P3 rwb-case",
      "Ownership Map, Parameters sheet; the default ruling of R-PREC"),
     ("Case list API and screen", "P3 rwb-case; the daily case list row is P1",
      "Ownership Map, Rulings sheet (the API, not the row table)"),
     ("Rule package registry", "P7 rwb-decision", "The default ruling of R-PREC"),
     ("Interaction ledger", "P1 rwb-source-data; the case timeline and the interaction API stay with P3",
      "Ownership Map, Rulings sheet; DP-18"),
     ("Delegation of authority table", "P4 rwb-access", "Ownership Map, Rulings sheet"),
     ("Feature flags", "The platform library", "The default ruling of R-PREC"),
     ("Outbox, inbox and idempotency tables", "The platform library, with one copy created in each service schema",
      "Ownership Map, Rulings sheet; DP-09")]))
sec10.append("")
sec10.append("## 10.6 What this changes in section 5")
sec10.append("")
sec10.append(
    "- No requirement ID, requirement text, priority, business owner or epic column in section 5 changes."
)
sec10.append(
    "- The requirements in 5.7 that concern the interaction ledger are delivered by RWB-SVC-P1, and those that "
    "concern parameters and reference data by RWB-SVC-P3, because the Ownership Map gives those items to P1 "
    "and P3. They stay written where they are, under P7, so that the IDs remain stable (" + CG + "-6; "
    + ASM + "-8; " + ASM + "-10)."
)
sec10.append(
    "- The requirements in 5.7 that concern approvals are delivered by RWB-SVC-P7, and the delegation of "
    "authority table they read is P4's (" + CG + "-7; " + ASM + "-9)."
)
sec10.append(
    "- Section 4 stays the business process view of 19 L1 processes; it is not a service list, and no service "
    "is mapped to a process here."
)
sec10.append("")
s10 = "\n".join(sec10)

sec11 = []
sec11.append("")
sec11.append("# 11. Business requirement trace: requirement to service epic to business epic")
sec11.append("")
sec11.append(
    "Every business requirement in section 5 appears exactly once in this table, with the service epic that "
    "delivers it, the service, the wave and the business epic whose release it lands in. The business epic is "
    "taken from the Epic column of the requirement's own table (E1 to E8), read as EP01 to EP08 ("
    + ASM + "-12). The service epic is taken from the module the requirement sits under, corrected where the "
    "Ownership Map gives the item to another service (" + CG + "-2; " + CG + "-6; " + CG + "-7; " + ASM + "-7; "
    + ASM + "-8; " + ASM + "-9; " + ASM + "-10)."
)
sec11.append("")
sec11.append(table(
    ["Business requirements", "Count", "Service epic", "Service", "Wave", "Business epic"],
    TRACE + [("Total", total, "", "", "", "")]))
sec11.append("")
sec11.append(
    "The 78 non-functional requirements of section 6 are not business requirements and are delivered as "
    "non-functional work: RWB-ITG-NFR for the harness and the measured targets, and the platform epics "
    "RWB-PLT-OBS, RWB-PLT-EDGE, RWB-PLT-EVT, RWB-PLT-DB and RWB-PLT-WF for the mechanism each one relies on, "
    "in wave 0 and then in every wave that a target first applies to (" + ASM + "-14)."
)
sec11.append("")
sec11.append(
    "Three modules have no requirement section of their own: P8 payment, P9 reporting and P10 agent. Their "
    "requirements are carried inside other sections: payment matching and posting in 5.3 and 5.12 to 5.14, "
    "the steering and management information duties in 5.3, 5.6 and 5.7, and the agent and model duties in "
    "5.3, 5.5, 5.7 and 6.9. Their service epics therefore appear in 10.2 with no row of their own in this "
    "table (" + CG + "-8; " + ASM + "-13)."
)
sec11.append("")
s11 = "\n".join(sec11)

GAPS = [
    ("CG-1", "Conflict", "Decision owners in section 9 are person names"),
    ("CG-2", "Ambiguous", "One requirement prefix, REQ-DRI, is used by two modules"),
    ("CG-3", "Missing", "No delivery model or service-epic mapping in version 4"),
    ("CG-4", "Missing", "Business epic codes EP01 to EP08 are not defined in this document"),
    ("CG-5", "Conflict", "Three constraints in section 7 contradict the target architecture"),
    ("CG-6", "Ambiguous", "Interaction ledger requirements sit under P7 but the ledger is P1's"),
    ("CG-7", "Ambiguous", "Approval requirements sit under P7 but the authority table is P4's"),
    ("CG-8", "Missing", "No requirement section for P8 payment, P9 reporting or P10 agent"),
]
ASMS = [
    ("ASM-1", "The document stays in Draft in this run", "Overlay D-RCV-60; no human approval in this run"),
    ("ASM-2", "EP01 to EP08 are Epic 1 to Epic 8 of section 8", "The wave map names the codes; section 8 names the epics"),
    ("ASM-3", "Built on ACE is read as 19 services inside ACE", "D-RCV-60, ADR-013"),
    ("ASM-4", "Modular monolith is read as one schema and login per service", "D-RCV-60, ADR-014"),
    ("ASM-5", "No Temporal is read as superseded by the workflow platform", "D-RCV-60, ADR-016"),
    ("ASM-6", "The four named owners are replaced by the section 12 placeholder", "Root rule 4"),
    ("ASM-7", "REQ-DRI-001 to 005 and 009 to 012 are P7; 006 to 008 and 013 are P2", "Section 5.2 and 5.7"),
    ("ASM-8", "The REQ-ILG requirements are delivered by P1", "Ownership Map, Rulings sheet; DP-18"),
    ("ASM-9", "REQ-APD is P7; the authority table it reads is P4", "Ownership Map, Rulings sheet"),
    ("ASM-10", "REQ-DRI-010 and 011 are delivered by P3", "Default ruling of R-PREC"),
    ("ASM-11", "Release dates carry (tentative)", "U7, DL48"),
    ("ASM-12", "The Epic column E1 to E8 is read as EP01 to EP08", "Section 5 tables"),
    ("ASM-13", "P8, P9 and P10 have no requirement section of their own", "Section 5 has 16 sections"),
    ("ASM-14", "The 78 non-functional requirements are delivered as non-functional work", "Section 6; RWB-ITG-NFR"),
]
sec12 = []
sec12.append("")
sec12.append("# 12. Gaps and assumptions raised by this version")
sec12.append("")
sec12.append(
    "The rows below are the gaps and assumptions this version raises. They are numbered by the register step, "
    "and the identifiers here are the candidate identifiers (" + CG + "-n and " + ASM + "-n)."
)
sec12.append("")
sec12.append("## 12.1 Gaps")
sec12.append("")
sec12.append(table(["ID", "Type", "What it affects"], GAPS))
sec12.append("")
sec12.append("## 12.2 Assumptions")
sec12.append("")
sec12.append(table(["ID", "Assumption", "Why"], ASMS))
sec12.append("")
sec12.append(
    "The document stays in Draft until the Product Owner and the business owner approve it. No approval is "
    "recorded in this version (" + ASM + "-1)."
)
sec12.append("")
s12 = "\n".join(sec12)

body = t.rstrip("\n") + "\n" + s10 + "\n" + s11 + "\n" + s12

HEADER = ("SCB Collections and Recovery. Henka Group, 22 November 2026.\n"
          "(C) Siam Commercial Bank and Henka Pte Ltd\n\n")
body = HEADER + body

for out in (OUT_SCRATCH, OUT_DOC):
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print("WROTE", out.relative_to(ROOT))
print("trace rows", len(TRACE), "requirement total", total)
