"""Build WP B-ARCH-CON: Recovery Workbench Service Contract Catalog v1 (.md and .xlsx).

Sources (read only): Architecture v5 Text Extract v1 (slides 13-20, 41-44),
Temporal and Drools Design Text Extract v1 (slides 11-14), Ownership Map v1 (.xlsx),
_work/msr/plan/ownership.json, _work/msr/plan/ids.json, Template and Rules v1 (R1, R3, R5, R8, R9).
Never edits a source file.
"""
import json
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT_MD = ROOT / "05 Technical architecture" / "Recovery Workbench Service Contract Catalog v1.md"
XLSX_MD = HERE / "catalog_xlsx.md"
GAPS = ROOT / "_work" / "msr" / "gaps" / "B-ARCH-CON.jsonl"
ASMS = ROOT / "_work" / "msr" / "assumptions" / "B-ARCH-CON.jsonl"
EDITLOG = ROOT / "_work" / "msr" / "editlog" / "B-ARCH-CON.md"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
DATE = "22 November 2026"

# ---------------------------------------------------------------- services
PKG = {
    "rwb-source-data": "sourcedata", "rwb-integration": "integration", "rwb-case": "case",
    "rwb-access": "access", "rwb-document": "document", "rwb-comms": "comms",
    "rwb-decision": "decision", "rwb-payment": "payment", "rwb-reporting": "reporting",
    "rwb-agent": "agent", "rwb-valuation": "valuation", "rwb-treatment": "treatment",
    "rwb-guarantee": "guarantee", "rwb-litigation": "litigation", "rwb-asset": "asset",
    "rwb-debtsale": "debtsale", "rwb-writeoff": "writeoff", "rwb-deviation": "deviation",
    "rwb-partner": "partner",
}

wb = openpyxl.load_workbook(
    ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx",
    data_only=True)
SERVICES = []
for r in wb["Services"].iter_rows(min_row=2, values_only=True):
    if not r[0]:
        continue
    SERVICES.append(dict(code=r[0], svc=r[1], name=r[2], wave=int(r[3]), schema=r[4],
                         base=r[5], topic=r[6], queue=r[7],
                         pkg="th.co.scb.ace.workbench.recovery." + PKG[r[1]]))
SVC = {s["code"]: s for s in SERVICES}
LABEL = {c: f"{c} {SVC[c]['svc']}" for c in SVC}
LABEL["BFF"] = "gateway-bff"
LABEL["PLT"] = "PLT platform library"
LABEL["ACE-CMN"] = "ACE Common"
LABEL["ACE-DB"] = "ACE database"
LABEL["EXT"] = "Outside the cluster"
LABEL["ALL"] = "All 19 services"
LABEL["PARTNER"] = "Partner portal"
LABEL["REQUESTER"] = "The requesting service"
LABEL["NOTSPEC"] = "Not specified in the source documents (CG-B-ARCH-CON-4; ASM-B-ARCH-CON-4)"

OWN_ROWS = {
    "P1": "ACE view contract, extension tables, freshness, reconciliation",
    "P2": "interface config, file runs, outbound items, ACE integration paths",
    "P3": "case, CMMN state, queues, tasks, allocation, timers",
    "P4": "Recovery roles as data, scope, masking policy, DoA table, access log",
    "P5": "metadata, custody, OCR text and fields, signatures, retention",
    "P6": "notices, templates, merge fields, proof of delivery",
    "P7": "approvals, central decision ledger, DMN model registry",
    "P8": "payment and proceeds matching, fees, bookings, posting files",
    "P9": "measures, snapshots, steering dashboard, regulatory reports",
    "P10": "agent policies, prompts, runs, guardrails, evaluations",
    "S1": "valuations, D6 route decision, route agent output",
    "S2": "treatments, contracts, settlement and deed-in-lieu agreements, plan timers",
    "S3": "TCG and insurance claims, guarantor notices and pursuit",
    "S4": "legal actions, hearings, judgments, enforcement, LED auction ladder",
    "S5": "assets taken on, holding, floor price, listings, auction rounds",
    "S6": "lots, data room, buyer terms, bids, award, transfer",
    "S7": "eligibility, committee, posting, recovery after charge-off",
    "S8": "X1-X7 screening, pause, handling, return",
    "S9": "panel, partner users, instructions, results, fees, scorecards",
}

OWN = json.loads((ROOT / "_work" / "msr" / "plan" / "ownership.json").read_text(encoding="utf-8"))
API = OWN["api"]
WF = OWN["workflows"]
JOBS = OWN["jobs"]
TABLES = OWN["tables"]

# ---------------------------------------------------------------- events
# (id, name, producer, consumers, numbered)  Architecture v5 slides 42, 43 and the service contracts 14-20
EVENTS = [
    ("EV-01", "CaseCreated", "P3", ["P10", "S8", "P9"]),
    ("EV-02", "CaseAllocated", "P3", ["P9"]),
    ("EV-03", "CaseAllocationFailed", "P3", ["P3"]),
    ("EV-04", "CaseTransferred", "P3", ["P9"]),
    ("EV-05", "CaseStateChanged", "P3", ["P6", "P9"]),
    ("EV-06", "DeviationRaised", "S8", ["P3", "P6", "S2"]),
    ("EV-07", "DeviationCleared", "S8", ["P3", "P6"]),
    ("EV-08", "DecisionRecorded", "ALL", ["P7", "P9"]),
    ("EV-09", "ApprovalRequested", "P7", ["BFF"]),
    ("EV-10", "TreatmentApproved", "S2", ["P6", "P8"]),
    ("EV-11", "TreatmentBooked", "P8", ["P3", "S2"]),
    ("EV-12", "PaymentMissed", "P8", ["P3", "S2", "P6"]),
    ("EV-13", "NoticeGenerated", "P6", ["P7"]),
    ("EV-14", "NoticeDispatched", "P6", ["P9"]),
    ("EV-15", "NoticeDelivered", "P6", ["S4", "S3", "P3"]),
    ("EV-16", "DocumentStored", "P5", ["P10", "P3"]),
    ("EV-17", "DocumentFieldsExtracted", "P5", ["P3"]),
    ("EV-18", "TimerDue", "PLT", ["NONE"]),
    ("EV-19", "TimerBreached", "P3", ["BFF"]),
    ("EV-20", "InstructionIssued", "S9", ["PARTNER"]),
    ("EV-21", "PartnerResultSubmitted", "S9", ["S4", "S5", "P3"]),
    ("EV-22", "AssetTakenOn", "S5", ["P3", "P8"]),
    ("EV-23", "LotAwarded", "S6", ["P3", "P8"]),
    ("EV-24", "WriteOffApproved", "S7", ["P3", "P8", "P9"]),
    ("EV-25", "ProceedsMatched", "P8", ["P3", "S5", "S6", "S7", "S3"]),
    ("EV-26", "AceDataReady", "P1", ["P3", "P8", "S8", "S7"]),
    ("EV-27", "AceDataLate", "P1", ["BFF"]),
    ("EV-28", "AgentRunCompleted", "P10", ["P7", "P5", "S8"]),
    ("EV-29", "CaseEvent", "P3", ["NONE"]),
    ("EV-30", "RulePackageInForce", "P7", ["P3", "S1", "S2", "P8"]),
]
EV_NAME = {e[1]: e for e in EVENTS}
TOPIC = {s["code"]: s["topic"] for s in SERVICES}
TOPIC["ALL"] = "rwb.decision-record.v1"
TOPIC["PLT"] = "\u2014"

EXTRA_EVENTS = [
    ("RouteDecided", "S1", ["P3"]),
    ("AssetSold", "S5", ["P8", "P3"]),
    ("JudgmentRecorded", "S4", ["S5", "P3"]),
    ("AuctionResult", "S4", ["S5", "P3"]),
    ("TreatmentClosed", "S2", ["P3", "P9"]),
    ("GuaranteeClaimFiled", "S3", ["P3", "P9"]),
    ("GuaranteeClaimSettled", "S3", ["P3", "P9"]),
    ("AccountsTransferred", "S6", ["P3", "P9"]),
    ("AccessPolicyChanged", "P4", ["ALL"]),
    ("DoaLimitChanged", "P4", ["ALL"]),
    ("FileDelivered", "P2", ["REQUESTER"]),
    ("FileFailed", "P2", ["REQUESTER"]),
    ("ApprovalDecided", "P7", ["NOTSPEC"]),
    ("ReportPublished", "P9", ["NOTSPEC"]),
]

# ---------------------------------------------------------------- pairs (provider, consumer)
REST_PAIRS = [
    ("P3", "BFF", "GET /cases/{id}; GET /cases?queue=; POST /cases/{id}/actions; GET /tasks; POST /tasks/{id}/complete; GET /case-summary/{id}", "slide 14, slide 20"),
    ("P1", "BFF", "GET /customers/{id}; GET /accounts/{id}; GET /freshness (composite case screen, one hop each in parallel)", "slide 15, slide 20"),
    ("ACE-CMN", "BFF", "Sign-in through ACE Common; session to short-lived user JWT", "slide 20"),
    ("P4", "P3", "POST /authorise (role, scope, DoA), cached in rwb-case", "slide 13, slide 14"),
    ("P4", "P7", "GET /doa-limits (DoA limits)", "slide 13, slide 14"),
    ("ACE-CMN", "P4", "Sign-in, group-to-role (Entra ID)", "slide 13, slide 14"),
    ("P1", "S1", "Collateral and appraisals (GET /collateral/{id})", "slide 13, slide 18"),
    ("P1", "S8", "Party flags", "slide 13, slide 15"),
    ("P1", "S7", "GL outcome", "slide 13, slide 20"),
    ("P1", "P10", "Tool: read case facts (read-only tool-gateway call)", "slide 13, slide 16"),
    ("P5", "P10", "Tool: read extracted fields (read-only tool-gateway call)", "slide 13, slide 16"),
    ("P5", "S9", "Partner uploads (SAS link)", "slide 13, slide 17"),
    ("P5", "P2", "Fetch file by ID (SAS link)", "slide 13, slide 16"),
    ("EXT", "S9", "Partners (law firms, agencies, buyers) through the partner gateway, FAPI 2.0, MFA", "slide 13, slide 17"),
    ("EXT", "P10", "Enterprise AI private endpoint (INT-23), HTTPS", "slide 13, slide 16"),
    ("ACE-CMN", "P6", "Notification path (SMS, LINE OA)", "slide 13, slide 17"),
]
FILE_PAIRS = [
    ("P7", "EXT", "Immutable storage: daily ledger seal (WORM)", "slide 13, slide 14"),
    ("P5", "EXT", "Azure Blob (WORM): files, 2.8 TB by 2031", "slide 13, slide 16"),
    ("P2", "EXT", "WIN registered mail, daily outbound file (INT-14); debt buyers, per lot, encrypted (INT-25)", "slide 13, slide 16"),
]
SQL_PAIRS = [
    ("ACE-DB", "P1", "SELECT on the 30 recovery.v_ace_* views, read only (ADR-010)", "slide 13, slide 15"),
]
NEXUS_PAIRS = [
    ("ACE-CMN", "S2", "restructure.calculate (Nexus operation, namespace ace-collection)", "slide 13, slide 18"),
]
TMP_PAIRS = [
    ("P1", "P3", "Activity: listEligibleAccounts(businessDate)", "slide 14"),
    ("S1", "P3", "Child workflow: RouteDecisionWorkflow", "slide 14, slide 18"),
    ("S2", "P3", "Child workflow: the treatment stage workflows (TreatmentWorkflow)", "slide 14, slide 18"),
    ("S3", "P3", "Child workflow: GuaranteeClaimWorkflow", "slide 14, slide 18"),
    ("S4", "P3", "Child workflow: LitigationWorkflow", "slide 14, slide 19"),
    ("S5", "P3", "Child workflow: AssetDisposalWorkflow", "slide 14, slide 19"),
    ("S6", "P3", "Child workflow: DebtSaleWorkflow", "slide 14, slide 19"),
    ("S7", "P3", "Child workflow: WriteOffWorkflow", "slide 14, slide 20"),
    ("S8", "P3", "Child workflow: DeviationWorkflow", "slide 14, slide 15"),
    ("P7", "S1", "Child workflow: ApprovalWorkflow (kit template)", "slide 13, slide 18"),
    ("P10", "S1", "Child workflow: route agent run", "slide 13, slide 18"),
    ("P7", "S2", "Child workflow: ApprovalWorkflow (DoA)", "slide 13, slide 18"),
    ("P5", "S2", "Contract document generation and e-sign", "slide 13, slide 18"),
    ("P8", "S2", "Activity: postProceeds (saga step)", "slide 13, slide 18"),
    ("P6", "S3", "Child workflow: guarantor notice", "slide 13, slide 18"),
    ("P7", "S3", "Child workflow: ApprovalWorkflow", "slide 13, slide 18"),
    ("S9", "S4", "Activity: issueInstruction (law firm)", "slide 13, slide 19"),
    ("P6", "S4", "Child workflow: demand notice", "slide 13, slide 19"),
    ("P7", "S4", "Child workflow: ApprovalWorkflow", "slide 13, slide 19"),
    ("S9", "S5", "Activity: issueInstruction (auction vendor)", "slide 13, slide 19"),
    ("P7", "S5", "Child workflow: ApprovalWorkflow", "slide 13, slide 19"),
    ("P8", "S5", "Activity: postProceeds", "slide 13, slide 19"),
    ("P6", "S5", "Not specified in the source documents (CG-B-ARCH-CON-8; ASM-B-ARCH-CON-8)", "slide 13"),
    ("P5", "S6", "Document: data room pack", "slide 13, slide 19"),
    ("P7", "S6", "Child workflow: ApprovalWorkflow", "slide 13, slide 19"),
    ("P2", "S6", "Activity: deliverFile (buyer file)", "slide 13, slide 19"),
    ("P8", "S6", "Activity: postProceeds", "slide 13, slide 19"),
    ("P7", "S7", "Child workflow: committee approval", "slide 13, slide 20"),
    ("P8", "S7", "Activity: postProceeds", "slide 13, slide 20"),
    ("P10", "S8", "Child workflow: screening agent run", "slide 13, slide 15"),
    ("P10", "P5", "Child workflow: classify / extract run", "slide 13, slide 16"),
    ("P5", "P6", "Document: generate letter", "slide 13, slide 17"),
    ("P7", "P6", "Child workflow: approval", "slide 13, slide 17"),
    ("P2", "P6", "Activity: deliverFile (WIN letters)", "slide 13, slide 17"),
    ("P1", "P8", "Activity: payments for business date", "slide 13, slide 17"),
    ("P2", "P8", "Activity: deliverFile (posting file)", "slide 13, slide 17"),
    ("P1", "P9", "Activity: snapshot(page) for measures", "slide 13, slide 15"),
    ("P2", "P9", "Activity: deliverFile (regulatory extract)", "slide 13, slide 15"),
]

PAIRS = []
for p_, c, i, s in REST_PAIRS:
    PAIRS.append([p_, c, "REST", i, s])
for p_, c, i, s in TMP_PAIRS:
    PAIRS.append([p_, c, "Temporal", i, s])
for p_, c, i, s in NEXUS_PAIRS:
    PAIRS.append([p_, c, "Nexus", i, s])
for p_, c, i, s in FILE_PAIRS:
    PAIRS.append([p_, c, "File", i, s])
for p_, c, i, s in SQL_PAIRS:
    PAIRS.append([p_, c, "SQL view", i, s])
for eid, name, prod, cons in EVENTS:
    for c in cons:
        if c == "NONE":
            continue
        PAIRS.append([prod, c, "Kafka", name, f"slide 42, slide 43 ({eid})"])
for name, prod, cons in EXTRA_EVENTS:
    for c in cons:
        PAIRS.append([prod, c, "Kafka", name, "slide 43 (event catalogue, not numbered)"])
PAIRS.append(["ALL", "ACE-CMN", "Kafka", "Audit and PII logs", "slide 13 note"])

EDGE = ("BFF", "ACE-CMN", "ACE-DB", "EXT", "PARTNER", "REQUESTER")


def pair_class(p_, c):
    if p_ in EDGE or c in EDGE:
        return "X"
    if p_ == c:
        return "H"
    return "C"


def wave_of(code):
    return 0 if code in EDGE + ("ALL", "PLT", "NOTSPEC") else SVC[code]["wave"]


def itg(p_, c):
    w = max(wave_of(p_), wave_of(c), 1)
    return f"RWB-ITG-W{w} harness"


def artefact(p_, ctype, interface=""):
    if ctype == "REST":
        if p_ in SVC:
            return f"OpenAPI 3.1, {SVC[p_]['base']}"
        return {"ACE-CMN": "ACE Common API (sign-in, notification path)",
                "EXT": "The external API or interface of that party"}.get(p_, "OpenAPI 3.1")
    if ctype == "Kafka":
        if "Audit" in interface:
            return "AsyncAPI 3.0, ACE Common logging topics"
        t = TOPIC.get(p_, "-")
        return f"AsyncAPI 3.0, {t}" if t and t != "-" else "AsyncAPI 3.0"
    if ctype == "Temporal":
        return f"Activity contract jar on task queue {SVC[p_]['queue']}" if p_ in SVC else "Contract jar"
    if ctype == "Nexus":
        return "Nexus operation, ace-collection"
    if ctype == "File":
        return "File manifest (fileId, batchId, sha256, record count)"
    if ctype == "SQL view":
        return "View contract, SELECT only"
    return ""


def md_table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return out


# ---------------------------------------------------------------- sections
L = []
L.append("SCB Collections and Recovery. Henka Group, 22 November 2026.")
L.append("(C) Siam Commercial Bank and Henka Pte Ltd")
L.append("")
L.append("# Recovery Workbench Service Contract Catalog v1")
L.append("")
L += md_table(["Item", "Value"], [
    ["Document", "Recovery Workbench Service Contract Catalog"],
    ["Version", "1"],
    ["Date", DATE],
    ["Decision", f"{DEC} microservice realignment"],
    ["Tool", TOOL],
    ["Status", "Draft"],
    ["Owner role", "Solution architect"],
    ["Services in scope", "19: P1 to P10 and S1 to S9, plus the shared platform (PLT), gateway-bff and the partner gateway"],
    ["Source of record", "Recovery Workbench Architecture v5 Text Extract v1 (slides 13 to 20 and 41 to 44); Recovery Workbench Temporal and Drools Design Text Extract v1 (slides 11 to 14); Recovery Workbench Microservice Ownership Map v1"],
    ["Change log", "below"],
])
L.append("")
L += md_table(["Version", "Date", "Change", "Detail"], [
    ["1", DATE, f"{DEC} microservice realignment, {TOOL}",
     "First Service Contract Catalog. The contract model, the call-type matrix of Architecture v5 slide 13, every provider and consumer pair, the contract artefact per call type, the dependency classes and the contract tests are stated once, per service. No earlier version of this family exists (CG-B-ARCH-CON-1; ASM-B-ARCH-CON-1)."],
])
L.append("")

# 1
L.append("# 1. Purpose and scope")
L.append("")
L.append("This catalogue is the contract register of the 19 Recovery services. For every service it states what the service provides, to whom, in which call type, under which artefact and version, and what it consumes from which provider. It is the document a team reads before writing code, the document the contract tests are generated from, and the register in which each service publishes its contract document (the CON stories of every service epic name this catalogue as the place of publication).")
L.append("")
L.append("It answers five questions:")
L.append("")
L.append("- What is the interface between these two services, and which call type is it?")
L.append("- Which artefact carries the contract, and which version of it?")
L.append("- May this call be synchronous, and if not, what replaces it?")
L.append("- What does the consumer build against while the provider is not yet built?")
L.append("- Which test proves that the contract holds, and which story runs it?")
L.append("")
L.append("What this catalogue does not contain: the operation schemas and examples (API Specification v5, one file per service plus gateway-bff and an index), the event payloads (Kafka Topic and Event Catalog v1), the workflow steps and activity signatures (Temporal Workflow and Activity Catalog v1), the table columns (Logical Data Model and Physical Schema) and the story-level build order (Build Sequence). Where those documents define a payload, this catalogue names the contract and points at them.")
L.append("")
L.append("Release dates are not held here. They are held in the Release Plan, they are unchanged, and every one of them is tentative (Decision U7 and DL48).")
L.append("")

# 2
L.append("# 2. How this catalogue is built")
L.append("")
L.append("## 2.1 Precedence")
L.append("")
L.append("Where two sources disagree, the higher one in the list below wins and the loser is recorded as a gap row and an assumption row (Template and Rules \u00a7R3). The order used here is:")
L.append("")
L.append("1. the Arch v5 catalogue slides 13 to 20 and 41 to 44, for services, resources, call types and jobs;")
L.append("2. the Recovery Temporal and Drools Design v1, for the workflow split, the activity contracts and the rules placement;")
L.append("3. the Arch v5 narrative slides, for the standards that every contract follows;")
L.append("4. the Recovery Workbench Microservice Ownership Map v1, for the owner of every table, endpoint, event, workflow and job;")
L.append("5. the current architecture documents (Decision Log, ADRs, TSDs, FSDs, LDM), which the realignment rewrites.")
L.append("")
L.append("The Ownership Map is used for every owner in this catalogue. Its Services sheet is the source of the code, the service name, the wave, the schema, the REST base, the topic and the task queue. Its Endpoints, Events, Workflows and activities, Jobs and Tables sheets are the source of the owner of every contract element named below. Where the map carries a ruling, the ruling is applied and the assumption behind it is named in the map.")
L.append("")
L.append("## 2.2 What changed in this version")
L.append("")
L.append("- The one recovery service with one REST surface and one schema becomes 19 services, each with its own OpenAPI contract, its own AsyncAPI contract, its own activity contract jar and its own schema (Arch v5 slide 41; ADR-013 and ADR-014).")
L.append("- Contract-first becomes the rule: the contract artefact is published before the code, the consumer builds against it and its fake, and a contract test in both builds proves the pair (ADR-020; Architecture v5 slide 46).")
L.append("- The call-type matrix of Architecture v5 slide 13 is reproduced in section 4 and is the authority for every pair in section 5. A pair that is not in the matrix is not a contract.")
L.append("- Every cross-service pair is classified in the dependency classes of Template and Rules \u00a7R5.4: C for the consuming story, which builds against the provider's published contract and its fake, and I for the integration story of the wave, which tests the real behaviour.")
L.append("- No service, contract or call type is added, removed or renamed against Architecture v5. The points the sources leave open are recorded in section 11 and in the two registers.")
L.append("")

# 3
L.append("# 3. The contract model")
L.append("")
L.append("## 3.1 One call type per interface")
L.append("")
L.append("A service never mixes call types for the same purpose. A REST call answers a person who is waiting. An event announces a fact that has already happened. A Temporal call commands a step in another service or runs a long process. A file moves bulk data or reaches a party outside the bank. A SQL view reads ACE data, and only rwb-source-data does that.")
L.append("")
L += md_table(["Call type", "What it is for", "Contract artefact", "Version form", "Source"], [
    ["REST", "A person waits for the answer: gateway-bff to the owner service, one hop, in parallel for composite screens, and a cached reference read", "OpenAPI 3.1 document per service, server /api/recovery/&lt;short&gt;/v1", "/v1 in the path", "Arch v5 slides 10, 11, 13"],
    ["Kafka event", "A fact others may react to; never a command", "AsyncAPI 3.0 per service, CloudEvents 1.0 binary mode, JSON Schema in the registry, BACKWARD compatibility", "rwb.&lt;short&gt;.events.v1; event name rwb.&lt;short&gt;.&lt;Event&gt;.v1", "Arch v5 slides 11, 22, 42, 43"],
    ["Temporal", "A step in another service, a child workflow per stage, or a Schedule", "Typed activity and workflow interface in a contract jar, published on task queue rwb-&lt;short&gt;", "Contract jar major version; workflow type name", "Arch v5 slide 11; Temporal and Drools Design slides 11 to 14"],
    ["Nexus", "A call into another namespace, used once in this design for the restructure calculator in ACE", "Nexus operation restructure.calculate in namespace ace-collection", "Operation name and version", "Arch v5 slides 9 and 18; Temporal and Drools Design slide 12"],
    ["File", "Bulk data or a party outside the bank: WIN registered mail, debt-buyer files, WORM storage", "Manifest with fileId, batchId, sha256 and record count; SAS link open for 15 minutes", "Manifest version and file naming", "Arch v5 slides 11, 16"],
    ["SQL view", "Reading ACE data, rwb-source-data only", "The 30 recovery.v_ace_* views, SELECT only (ADR-010)", "View name and column contract", "Arch v5 slides 11, 15, 29"],
])
L.append("")
L.append("The database is not a contract between services. A service writes only its own schema rwb_&lt;name&gt;, holds no grant on any other schema, and never joins across schemas (DP-01; Arch v5 slide 29). The only database contract in this catalogue is the ACE view contract between rwb-source-data and the ACE database.")
L.append("")
L.append("## 3.2 The contract key")
L.append("")
L.append("A contract is named in this catalogue by four values, all of them taken from the sources and none of them a new identifier:")
L.append("")
L.append("- the provider service code (P1 to P10, S1 to S9, PLT, gateway-bff, ACE Common, ACE database, outside the cluster);")
L.append("- the consumer service code, or All 19 services where the source says every service;")
L.append("- the call type of section 3.1;")
L.append("- the interface as the source names it: the operation path, the event name, the activity, child workflow or Schedule, the file, or the view.")
L.append("")
L.append("Where the source gives no consumer for an event, the row states Not specified in the source documents (CG-B-ARCH-CON-4; ASM-B-ARCH-CON-4) rather than a guess.")
L.append("")
L.append("## 3.3 What every contract states")
L.append("")
L += md_table(["Element", "REST", "Kafka", "Temporal", "File"], [
    ["Provider", "The owning service of the resource", "The service that writes the fact", "The service whose queue runs the activity or workflow", "The service that writes the file"],
    ["Consumer", "gateway-bff or a service, one hop", "Every service that reacts; never a command target", "The caller, on the provider's queue", "The receiving party"],
    ["Identity and authorisation", "User JWT from ACE Common sign-in; the service authorises through rwb-access", "Workload identity per service; topic ACL by service", "Workload identity; namespace rwb-recovery", "Partner gateway FAPI 2.0 or the bank MFT channel"],
    ["Timeout and retry", "2 s timeout, one GET retry with jitter, breaker and bulkhead per downstream", "Retry 1 min, 10 min, 1 h, then .dlt with an alert and a replay tool", "1 s initial interval, back-off 2, 10 attempts; non-retryable list per activity", "FileFailed event, operator retry, checksum on receipt"],
    ["Idempotency", "Idempotency-Key on every POST and PATCH", "idempotency_key and processed_event in the same transaction as the change", "Workflow ID and activity idempotency key", "batchId and sha256 checked before the file is accepted"],
    ["Error form", "RFC 9457 problem details", "CloudEvents data with an error code and no personal data", "Typed failures; the workflow decides", "Manifest with the reason and the record count reached"],
    ["Source", "Arch v5 slides 10, 11, 13", "Arch v5 slides 11, 22, 42", "Arch v5 slide 11; Temporal and Drools Design slide 14", "Arch v5 slide 11"],
])
L.append("")
L.append("## 3.4 Versioning and compatibility")
L.append("")
L.append("- REST carries the version in the path, /v1, and a breaking change is a new path version served side by side until the consumers move. Additive change inside v1 is allowed when every consumer tolerates unknown fields.")
L.append("- Events are versioned in the registry with BACKWARD compatibility, and the topic carries the version: rwb.&lt;short&gt;.events.v1, with the retry and dead-letter topics .retry.1m, .retry.10m, .retry.1h and .dlt beside it.")
L.append("- Temporal contract jars are versioned with the workflow kit and the activity interfaces; a change to an activity signature is a new major version of the jar and a new worker deployment, so a running workflow keeps replaying against the version it started with.")
L.append("- The file manifest is versioned with the interface; INT-14 and INT-25 keep their identifiers unchanged.")
L.append("- A contract document is registered in section 7 of this catalogue with its version and its publisher, and the CON story of the service epic is what publishes it.")
L.append("")

# 4 matrix
MATRIX_COLS = ["P3", "P7", "P4", "S8", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "P5", "P6", "P8", "S9", "P2", "P1", "P9", "P10", "ACE Cmn", "ACE DB", "Outside"]
M = {
    "P3": {"P7": "E", "P4": "R", "S8": "T E", "S1": "T E", "S2": "T E", "S3": "T E", "S4": "T E", "S5": "T E", "S6": "T E", "S7": "T E", "P5": "E", "P6": "E", "P8": "E", "S9": "E", "P1": "T E"},
    "P7": {"P4": "R", "P6": "E", "P10": "E", "Outside": "F"},
    "P4": {"ACE Cmn": "R"},
    "S8": {"P3": "E", "P1": "R E", "P10": "T E"},
    "S1": {"P7": "T E", "P1": "R", "P10": "T"},
    "S2": {"P7": "T E", "S8": "E", "P5": "T", "P8": "T E", "ACE Cmn": "N"},
    "S3": {"P7": "T", "P6": "T E", "P8": "E"},
    "S4": {"P7": "T", "P6": "T E", "S9": "T E"},
    "S5": {"P7": "T", "S4": "E", "P6": "T", "P8": "T E", "S9": "T E"},
    "S6": {"P7": "T", "P5": "T", "P8": "T E", "P2": "T"},
    "S7": {"P7": "T", "P8": "T E", "P1": "R E"},
    "P5": {"P10": "T E", "Outside": "F"},
    "P6": {"P3": "E", "P7": "T", "S8": "E", "S2": "E", "P5": "T", "P8": "E", "P2": "T", "ACE Cmn": "R"},
    "P8": {"P7": "E", "S2": "E", "S5": "E", "S6": "E", "S7": "E", "P2": "T", "P1": "T E"},
    "S9": {"P5": "R", "Outside": "R"},
    "P2": {"P5": "R", "Outside": "F"},
    "P1": {"ACE DB": "S"},
    "P9": {"P3": "E", "S2": "E", "S3": "E", "S6": "E", "S7": "E", "P6": "E", "P2": "T", "P1": "T"},
    "P10": {"P3": "E", "P5": "R E", "P1": "R", "Outside": "R"},
}

L.append("# 4. The call-type matrix (Architecture v5 slide 13)")
L.append("")
L.append("Row = the service that starts the interaction; column = the service it calls or listens to. The table is reproduced exactly as Architecture v5 slide 13 prints it, including the combined cells. It is the authority for section 5.")
L.append("")
L += md_table(["starts / target"] + MATRIX_COLS,
             [[LABEL[r]] + [M[r].get(c, "") for c in MATRIX_COLS] for r in M])
L.append("")
L += md_table(["Cell", "Meaning"], [
    ["T", "Temporal: an activity on the owner's queue, or a child workflow there"],
    ["N", "Nexus operation into ACE"],
    ["R", "REST call"],
    ["E", "Listens to the column's Kafka events"],
    ["S", "SQL views"],
    ["F", "File"],
])
L.append("")
L.append("Four rules come with the matrix and hold in every section below (Arch v5 slide 13):")
L.append("")
L.append("1. Route services reach the shared capabilities through Temporal, never REST.")
L.append("2. Only rwb-source-data touches ACE's tables; every other service asks it through its contract.")
L.append("3. rwb-decision and rwb-reporting listen widely and call almost nobody.")
L.append("4. The case router in rwb-case turns events into signals; no service calls another service directly for a business step.")
L.append("")
L.append("Not shown in the matrix because every service does it: audit and PII logs to ACE Common on Kafka, DecisionRecorded to rwb-decision on rwb.decision-record.v1, permission data cached from rwb-access, and traces to OpenTelemetry. The first two and the permission cache are carried in section 5 as All 19 services so that they are not lost; traces are a platform contract and are named in section 7.3.")
L.append("")

# 5 inventory
L.append("# 5. The contract inventory")
L.append("")
L.append("Every pair in the matrix, resolved to the interface the sources name. The order is provider code, then consumer code, then call type. The dependency class is the class of Template and Rules \u00a7R5.4 that the consuming story takes: C means the consuming story builds against the provider's published contract and its fake, X means the pair crosses an edge outside the 19 services and is tracked rather than built against, and H appears once, where rwb-case consumes its own CaseAllocationFailed.")
L.append("")
counts = {}
for p, c, t, i, s in PAIRS:
    counts[t] = counts.get(t, 0) + 1
L += md_table(["Call type", "Pairs"], [[k, counts[k]] for k in sorted(counts)] + [["Total", len(PAIRS)]])
L.append("")
ALIAS = {"ACE Cmn": "ACE-CMN", "ACE DB": "ACE-DB", "Outside": "EXT"}
rows = []
for p, c, t, i, s in sorted(PAIRS, key=lambda x: (x[0], x[1], x[2], x[3])):
    rows.append([LABEL.get(p, p), LABEL.get(c, c), t, i, artefact(p, t, i), pair_class(p, c), s])
L += md_table(["Provider", "Consumer", "Call type", "Interface", "Contract artefact", "Class", "Source"], rows)
L.append("")
L.append("The same inventory is the Contract pairs sheet of the workbook next to this document.")
L.append("")

# 6 service detail
L.append("# 6. Service contracts")
L.append("")
L.append("One section per service, in Ownership Map order: platform services P1 to P10, then the route services S1 to S9. Each section has the identity and the contract artefacts, the contracts the service provides, the contracts it consumes, and the REST operations the Ownership Map assigns to it. A row under Temporal that names another service is a call the service makes on that service's queue; a row that names no other service is its own work and is not a contract.")
L.append("")
L.append("The REST operations are the operation set of the Ownership Map v1 Endpoints sheet. The per-service base path applies to every operation of that service (Template and Rules \u00a7R4); the final per-service paths and payloads are written in API Specification v5 (CG-B-ARCH-CON-2; ASM-B-ARCH-CON-2).")
L.append("")
n = 0
for s in SERVICES:
    n += 1
    code = s["code"]
    L.append(f"## 6.{n} {code} {s['svc']} — {s['name']}")
    L.append("")
    L += md_table(["Item", "Value"], [
        ["Service code", code],
        ["Service", s["svc"]],
        ["Service name", s["name"]],
        ["Wave (Arch v5)", s["wave"]],
        ["Service epic", f"RWB-SVC-{code}"],
        ["Schema and login", s["schema"]],
        ["REST base", s["base"]],
        ["Kafka topic", s["topic"]],
        ["Retry and dead-letter topics", f"{s['topic']}.retry.1m, {s['topic']}.retry.10m, {s['topic']}.retry.1h, {s['topic']}.dlt"],
        ["Temporal task queue", s["queue"]],
        ["Java package", s["pkg"]],
        ["Contract artefacts", f"OpenAPI 3.1 for {s['base']}; AsyncAPI 3.0 for {s['topic']}; activity contract jar on {s['queue']}"],
        ["Owns (Arch v5 slide 41)", OWN_ROWS[code]],
        ["Status", "Draft"],
    ])
    L.append("")
    L.append("**Contracts provided**")
    L.append("")
    prov = [x for x in PAIRS if x[0] == code]
    prov.sort(key=lambda x: (x[2], x[1], x[3]))
    if prov:
        L += md_table(["Call type", "Consumer", "Interface", "Contract artefact", "Class", "Source"],
                      [[t, LABEL.get(c, c), i, artefact(p, t, i), pair_class(p, c), src] for p, c, t, i, src in prov])
    else:
        L.append("None. The service provides no interface to another service; its work is internal to its own queue and its own schema.")
    L.append("")
    L.append("**Contracts consumed**")
    L.append("")
    cons = [x for x in PAIRS if x[1] == code]
    cons.sort(key=lambda x: (x[2], x[0], x[3]))
    if cons:
        L += md_table(["Call type", "Provider", "Interface", "Contract artefact", "Class", "Build against", "Source"],
                      [[t, LABEL.get(p, p), i, artefact(p, t, i), pair_class(p, c),
                        {"C": "The provider's published contract and its fake",
                         "H": "Its own contract and its own contract test",
                         "X": "The edge stub named in section 8.4"}[pair_class(p, c)],
                        src] for p, c, t, i, src in cons])
    else:
        L.append("None. The service calls no other service; it reacts to events and works on its own queue.")
    L.append("")
    L.append(f"**REST operations owned (Ownership Map v1, Endpoints sheet)**")
    L.append("")
    ops = sorted([k for k, v in API.items() if v["owner"] == code])
    if ops:
        L += md_table(["Operation", "Contract path", "Owner"],
                      [[o, f"{s['base']}{o.split(' ', 1)[1]}", code] for o in ops])
    else:
        L.append("None.")
    L.append("")
    L.append("**Schema boundary**")
    L.append("")
    L.append(f"- Writes {s['schema']} only. No grant on any other schema, no cross-schema join, view or foreign key (DP-01; Arch v5 slide 29).")
    if code == "P1":
        L.append("- Reads the 30 recovery.v_ace_* views, SELECT only; the only service with that grant (ADR-010).")
    if code == "P3":
        L.append("- Owns the case list API, the parameters and the reference data by the R-PREC default ruling (E1-042, E1-043).")
    if code == "P7":
        L.append("- Owns the rule package registry by the R-PREC default ruling; every service evaluates its own rules with the package version it was told is in force.")
    if code == "S9":
        L.append("- The partner portal is the only partner surface, behind the partner gateway (FAPI 2.0).")
    if code == "PLT":
        L.append("- Owns the shared tables the template instantiates in every schema.")
    L.append("")

# 7 artefacts
L.append("# 7. Contract artefacts and registration")
L.append("")
L.append("## 7.1 What each service publishes")
L.append("")
L.append("A service publishes three artefacts before any code story starts, and registers them here with the version it publishes. The artefacts are the deliveries of the service's CON story in its service epic.")
L.append("")
L += md_table(["Code", "Service", "OpenAPI 3.1", "AsyncAPI 3.0", "Activity contract jar", "Published by"], [
    [s["code"], s["svc"], s["base"], s["topic"], s["queue"], f"RWB-SVC-{s['code']} CON story"]
    for s in SERVICES
])
L.append("")
L.append("The coordinates of the contract jars (groupId, artifactId, version) are Not specified in the source documents (CG-B-ARCH-CON-3; ASM-B-ARCH-CON-3). The Java package column of section 6 is the package root the jar follows; the exact coordinates are allocated with the repositories in the service template work.")
L.append("")
L.append("## 7.2 The artefact rules")
L.append("")
L += md_table(["Rule", "Detail", "Source"], [
    ["Contract first", "The OpenAPI document, the AsyncAPI document and the activity contract jar are published and versioned before the implementation story of the contract starts", "ADR-020; Arch v5 slide 46"],
    ["One artefact per service", "One OpenAPI document per service, one AsyncAPI document per service, one contract jar per service; gateway-bff has its own OpenAPI document and no topic", "Arch v5 slides 20 and 41; Template and Rules \u00a7R8.4"],
    ["Registry", "Event schemas are registered with BACKWARD compatibility; the registry product is Not specified in the source documents (CG-B-ARCH-CON-5; ASM-B-ARCH-CON-5)", "Arch v5 slide 42"],
    ["Validation", "The documents validate against OpenAPI 3.1, AsyncAPI 3.0 and the Temporal SDK interface rules; the build fails on a validation error", "Arch v5 slide 46"],
    ["Fake", "Each provider publishes a fake from its own contract; the consumer runs its contract tests against the fake, so the consumer never waits for the provider", "Template and Rules \u00a7R5.4 (class C)"],
    ["Publication", "The contract document is registered in section 6 of this catalogue with its version; the CON story is Done when it is registered", "Story set, CON stories of every service epic"],
])
L.append("")
L.append("## 7.3 The shared platform contracts")
L.append("")
L += md_table(["Contract", "Provider", "Consumers", "Artefact", "Source"], [
    ["Workflow kit: Approval, Notify, Document intake, Agent run, Human task with SLA, Saga runner, Scheduled job, Partner instruction", "PLT", "All 19 services", "Versioned workflow kit library", "Temporal and Drools Design slides 12 and 14"],
    ["EvaluateRules and RecordAndApply activities", "Every service, on its own queue", "Its own workflows", "Activity contract jar plus the rule package contract", "Temporal and Drools Design slide 12; ADR-017"],
    ["Rule package in force", "P7 rwb-decision", "All services that evaluate rules", "RulePackageInForce event on rwb.decision.events.v1 plus the package checksum", "Arch v5 slides 14 and 43; ADR-017"],
    ["Decision record", "Every service, locally", "P7 rwb-decision central ledger", "DecisionRecorded on rwb.decision-record.v1, hash-chained", "Arch v5 slides 20 and 43; ADR-022"],
    ["Authorise", "P4 rwb-access", "All staff-facing services", "POST /authorise on /api/recovery/access/v1, cached at the caller", "Arch v5 slide 14"],
    ["Feature flags", "PLT platform library", "All 19 services", "Feature flag tables in every schema and the flag API", "Ownership Map v1 ruling; Template and Rules \u00a7R3"],
    ["Observability", "PLT", "All 19 services", "OpenTelemetry traces, metrics and logs; /health and /metrics per service", "ADR-023; Arch v5 slide 20"],
])
L.append("")

# 8 dependency
L.append("# 8. Dependency classes and decoupling rules")
L.append("")
L.append("## 8.1 The four classes")
L.append("")
L += md_table(["Class", "Meaning for a contract", "Blocks the build?", "Source"], [
    ["H", "The same service, or a platform CON story. Inside one service the contract is its own module boundary.", "Only H on a non-CON story, in the same lane", "Template and Rules \u00a7R5.4"],
    ["C", "Another service's CON story. The consumer builds against the published contract and its fake; the provider is never a build blocker.", "No", "Template and Rules \u00a7R5.4"],
    ["I", "The real cross-service behaviour. Allowed only on ITG stories, which run the contract harness against the real providers.", "ITG only", "Template and Rules \u00a7R5.4"],
    ["X", "External or team-type work: gateway-bff, ACE Common, the ACE database, Blob, Enterprise AI, partners, the bank file channels, and the DB, INF or OPS story of the same legacy key.", "No; tracked", "Template and Rules \u00a7R5.4"],
])
L.append("")
L.append("Every row of section 5 carries its C or X class. The same pair becomes an I dependency on the integration story of the later wave, which is how the real behaviour is proved without making any service wait for another.")
L.append("")
L.append("## 8.2 The decoupling patterns as contract rules")
L.append("")
L += md_table(["DP", "Legacy marker", "Contract rule in this catalogue", "Dependency"], [
    ["DP-01", "recovery.&lt;table&gt; or the recovery schema", "The owner's schema rwb_&lt;name&gt;; a reader uses the owner's contract, never its tables", "none"],
    ["DP-02", "recovery_svc login", "One login per service; no shared login is a contract", "none"],
    ["DP-03", "DecisionLogWriter, decision log", "Local decision-record library plus DecisionRecorded on rwb.decision-record.v1", "H RWB-PLT-E1027-CON"],
    ["DP-04", "RuleEvaluator, Drools", "Embedded Drools kit in the owning service; rule packages arrive from rwb-decision on RulePackageInForce", "H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON"],
    ["DP-05", "AceSourceQuery, v_ace_*, account_ext", "Read through rwb-source-data's contract, or through the service's own ACE views where the ruling gives it one", "none"],
])
L.append("")
L.append("The full DP table is Template and Rules \u00a7R5.5; the rows above are the ones that create or remove a contract in this catalogue.")
L.append("")
L.append("## 8.3 The one-hop rule")
L.append("")
L.append("- REST is one hop: gateway-bff to the owner service, or a cached reference read from rwb-access or rwb-source-data. A service never calls another service to answer a screen.")
L.append("- A composite screen is composed in gateway-bff with parallel calls, each with a 2 s timeout and its own breaker, and the budget for the case screen is about 1.2 s (Arch v5 slide 46).")
L.append("- Anything longer than one hop is a workflow. The route services reach decision, document, payment, partner and communications through Temporal, never through REST (section 4, rule 1).")
L.append("- Trace analysis flags a call depth above one, and the build fails on it (ADR-020).")
L.append("")
L.append("## 8.4 The edge contracts")
L.append("")
L += md_table(["Edge", "Contract", "Stub used by the 19 services", "Source"], [
    ["gateway-bff", "OpenAPI 3.1 for the browser surface; session cookie with a 15 minute idle timeout; one hop to the owner", "A gateway stub with the route table of section 5", "Arch v5 slide 20"],
    ["ACE Common", "Sign-in and group-to-role (Entra ID), notification path (SMS, LINE OA), audit and PII logging on Kafka", "The ACE Common test double in the integration harness", "Arch v5 slides 14, 17, 20"],
    ["ACE database", "The 30 recovery.v_ace_* views, SELECT only", "View fixtures in the P1 contract test", "ADR-010; Arch v5 slide 29"],
    ["Enterprise AI", "HTTPS private endpoint (INT-23) from rwb-agent", "A recorded-response double", "Arch v5 slide 16"],
    ["WIN and debt buyers", "INT-14 daily outbound file; INT-25 encrypted buyer files through the bank MFT channel", "A file fixture with a manifest", "Arch v5 slide 16"],
    ["Partner gateway", "FAPI 2.0 in the DMZ fronting rwb-partner; MFA for partner users", "The partner gateway stub", "Arch v5 slides 8 and 17; ADR-019"],
])
L.append("")

# 9 conformance
L.append("# 9. Contract conformance and tests")
L.append("")
L.append("A contract is conformant when every row below is true. The list is the contract part of the Definition of Done in the Service Template Specification v1, and each row names the test that proves it.")
L.append("")
L += md_table(["#", "Contract rule", "Tested by"], [
    ["1", "The provider publishes its OpenAPI 3.1, AsyncAPI 3.0 and activity contract jar before the implementation story starts", "Contract publication gate in the pipeline"],
    ["2", "Every operation in section 6 exists in the published contract, under the service's own base path", "OpenAPI diff against the Ownership Map Endpoints sheet"],
    ["3", "Every event the service publishes is in its AsyncAPI document, on its own topic, with CloudEvents 1.0 binary mode and key caseId", "AsyncAPI validation plus a schema registry check"],
    ["4", "Every event the service consumes is deduplicated in processed_event, in the same transaction as the change", "Inbox test"],
    ["5", "Every activity and child workflow the service calls is declared in the provider's contract jar; no service imports another service's code", "Activity contract test"],
    ["6", "No REST chain longer than one hop; route services reach shared capabilities through Temporal", "Contract test plus trace-depth check"],
    ["7", "No cross-schema read, join, view or foreign key; the boundary test fails the build on any violation", "Architecture test"],
    ["8", "Every POST and PATCH is idempotent through Idempotency-Key, and every consumer of the same key returns the first result", "Idempotency test"],
    ["9", "Error responses follow RFC 9457 for REST and the error code form for events", "Contract example test"],
    ["10", "The provider's fake serves every operation and every event of its contract", "Fake conformance test in the consumer build"],
    ["11", "The pair is proved end to end in the integration story of the later wave", "RWB-ITG-W&lt;n&gt; harness"],
    ["12", "The contract document is registered in section 6 with its version", "Registration check on the CON story"],
])
L.append("")
L.append("The integration stories that run the harness are RWB-ITG-W1 to RWB-ITG-W4, one per wave, plus RWB-ITG-NFR for the non-functional contracts. A pair is assigned to the harness of the later of its two waves.")
L.append("")

# 10 change control
L.append("# 10. Contract change control")
L.append("")
L += md_table(["Step", "What happens", "Recorded in"], [
    ["Propose", "The provider team raises the change against its own contract and names the consumers from section 5", "The service's CON story"],
    ["Assess", "Every consumer in section 5 is checked; an additive change stays in v1, a breaking change takes a new path version or a new topic version", "This catalogue, section 5 and 6"],
    ["Publish", "The new artefact version is published with its fake before the code changes", "Section 7.1"],
    ["Prove", "The consumer contract test and the wave harness pass against both the old and the new version for one release", "Section 9"],
    ["Retire", "The old version is withdrawn only when no consumer in section 5 names it", "This catalogue, section 6"],
])
L.append("")
L.append("A change to a shared edge contract (ACE Common, ACE database views, Enterprise AI, WIN, debt buyers, the partner gateway) follows the same steps and is tracked as class X against the owning external party.")
L.append("")

# 11 open points
L.append("# 11. Open points")
L.append("")
L += md_table(["ID", "Point", "Effect in this catalogue", "Owner role"], [
    ["CG-B-ARCH-CON-1", "No earlier Service Contract Catalog exists, so v1 carries no inherited sections, IDs, numbers or dates", "Version 1, status Draft; the change-log row is the first", "Delivery lead"],
    ["CG-B-ARCH-CON-2", "The Ownership Map Endpoints sheet holds the monolith operations of API Specification v4, while Architecture v5 slide 41 states a per-service base path; the per-service paths and payloads are written in API Specification v5", "Section 6 lists the operation per owning service under its base path and leaves the final path to API Specification v5", "Solution architect"],
    ["CG-B-ARCH-CON-3", "The coordinates of the activity contract jars (groupId, artifactId, version) are not specified", "Section 7.1 states the artefact and the package root, and leaves the coordinates open", "Tech lead"],
    ["CG-B-ARCH-CON-4", "The event catalogue does not name the consumers of ApprovalDecided or ReportPublished", "The two rows state Not specified in the source documents (CG-B-ARCH-CON-4; ASM-B-ARCH-CON-4)", "Solution architect"],
    ["CG-B-ARCH-CON-5", "The schema registry product and its deployment are not specified; only the BACKWARD compatibility rule is stated", "Section 7.2 states the compatibility rule and not the product", "Platform architect"],
    ["CG-B-ARCH-CON-6", "The slide 13 rule that route services reach shared capabilities through Temporal sits beside REST cells from S1, S7 and S8 to rwb-source-data", "Section 8.3 reads the rule as covering the five shared capabilities named in the slide note; the rwb-source-data reads stay REST", "Solution architect"],
    ["CG-B-ARCH-CON-7", "The request and response content of the Enterprise AI private endpoint (INT-23) is not specified", "Section 8.4 names the edge and the stub, not a payload", "Solution architect"],
    ["CG-B-ARCH-CON-8", "The call-type matrix marks S5 to P6 as Temporal, but the asset contract on Architecture v5 slide 19 names no communications interface and no other slide supplies one", "Section 6.15 carries the placeholder in its Temporal row and no interface is invented", "Solution architect"],
])
L.append("")
L.append("The full text of every gap and assumption is in the Gap Register and the Assumptions Register (folder 23). Candidate rows are in `_work/msr/gaps/B-ARCH-CON.jsonl` and `_work/msr/assumptions/B-ARCH-CON.jsonl`.")
L.append("")

# 12 changelog
L.append("# 12. Change log")
L.append("")
L += md_table(["Version", "Date", "Change", "Detail"], [
    ["1", DATE, f"{DEC} microservice realignment, {TOOL}",
     "First Service Contract Catalog: the contract model and the five call types, the call-type matrix of Architecture v5 slide 13, the contract inventory of every provider and consumer pair, the contract by service with its artefacts, the shared platform contracts, the dependency classes and decoupling rules, the contract tests and the change control."],
])
L.append("")

TEXT = "\n".join(L).replace("&lt;", "<").replace("&gt;", ">")
OUT_MD.write_text(TEXT + "\n", encoding="utf-8")
print("WROTE", OUT_MD, len(L), "lines")


# ================================================================ workbook source
X = []
X.append("## Read me")
X.append("")
xr = [
    ["SCB Collections and Recovery. Henka Group, 22 November 2026.", "(C) Siam Commercial Bank and Henka Pte Ltd"],
    ["Item", "Value"],
    ["Document", "Recovery Workbench Service Contract Catalog v1"],
    ["Version", "1"],
    ["Date", DATE],
    ["Decision", f"{DEC} microservice realignment"],
    ["Tool", TOOL],
    ["Status", "Draft"],
    ["Owner role", "Solution architect"],
    ["Purpose", "The contract register of the 19 Recovery services: what each service provides and consumes, in which call type, under which artefact, with which dependency class and which test"],
    ["Source of record", "Architecture v5 Text Extract v1 slides 13 to 20 and 41 to 44; Temporal and Drools Design Text Extract v1 slides 11 to 14; Microservice Ownership Map v1"],
    ["Sheets", "Services; Call type matrix; Contract pairs; REST operations; Events; Temporal contracts; Jobs; Resources owned; Conformance; Open points; Change log"],
    ["How to read", "Contract pairs is the flat list behind section 5 of the document; one row per provider and consumer pair, class C for a service pair, X for an edge, H for the one self-subscription"],
    ["Ownership", "Every owner in this workbook comes from the Microservice Ownership Map v1"],
]
for r in xr:
    X.append("| " + " | ".join(r) + " |")
X.append("")

X.append("## Services")
X.append("")
rows = [["Code", "Service", "Name", "Wave", "Schema and login", "REST base", "Kafka topic", "Task queue", "Java package", "Service epic", "Owns (Arch v5 slide 41)"]]
for s in SERVICES:
    rows.append([s["code"], s["svc"], s["name"], s["wave"], s["schema"], s["base"], s["topic"], s["queue"], s["pkg"], f"RWB-SVC-{s['code']}", OWN_ROWS[s["code"]]])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Call type matrix")
X.append("")
rows = [["starts / target"] + MATRIX_COLS]
for r in M:
    rows.append([LABEL[r]] + [M[r].get(c, "") for c in MATRIX_COLS])
for r in rows:
    X.append("| " + " | ".join(r) + " |")
X.append("")

X.append("## Contract pairs")
X.append("")
rows = [["#", "Provider", "Consumer", "Call type", "Interface", "Contract artefact", "Class", "ITG harness", "Source"]]
for n, (p_, c, ty, i, src) in enumerate(sorted(PAIRS, key=lambda x: (x[0], x[1], x[2], x[3])), 1):
    rows.append([n, LABEL.get(p_, p_), LABEL.get(c, c), ty, i, artefact(p_, ty, i), pair_class(p_, c), itg(p_, c), src])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## REST operations")
X.append("")
rows = [["Operation", "Owner", "Contract path", "Base path"]]
for op in sorted(API):
    o = API[op]["owner"]
    rows.append([op, o, f"{SVC[o]['base']}{op.split(' ', 1)[1]}" if o in SVC else op, SVC[o]["base"] if o in SVC else "PLT"])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Events")
X.append("")
rows = [["ID", "Event", "Producer", "Topic", "Consumers", "Numbered in the event catalogue", "Source"]]
for eid, name, prod, cons in EVENTS:
    topic = "rwb.decision-record.v1" if eid == "EV-08" else (TOPIC.get(prod, "-") if prod != "PLT" else "-")
    rows.append([eid, name, LABEL.get(prod, prod), topic, "; ".join(LABEL.get(c, c) for c in cons), "Yes", "Arch v5 slide 42, slide 43"])
for name, prod, cons in EXTRA_EVENTS:
    rows.append(["-", name, LABEL.get(prod, prod), TOPIC.get(prod, "-"), "; ".join(LABEL.get(c, c) for c in cons), "No", "Arch v5 slide 43 (not numbered)"])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Temporal contracts")
X.append("")
rows = [["Type", "Name", "Owner", "Task queue", "Contract artefact", "Consumers", "Source"]]
for name in sorted(WF, key=lambda n: (WF[n]["owner"], n)):
    o = WF[name]["owner"]
    rows.append(["Workflow", name, LABEL.get(o, o), SVC[o]["queue"] if o in SVC else "-", "Activity contract jar", (lambda cs: "; ".join(sorted(cs)) if cs else "None named in the sources")({LABEL.get(c, c) for p_, c, ty, i, src in PAIRS if ty == "Temporal" and i.endswith(name)}), "Ownership Map v1, Workflows and activities"])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Jobs")
X.append("")
rows = [["Job", "Owner", "Contract form", "Source"]]
JOBDESC = {}
for jid in sorted(JOBS):
    o = JOBS[jid]["owner"]
    rows.append([jid, LABEL.get(o, o), JOBS[jid].get("replacement", ""), "Arch v5 slide 44; Ownership Map v1, Jobs"])
for r in rows:
    X.append("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |")
X.append("")

X.append("## Resources owned")
X.append("")
rows = [["Table", "Owner", "Schema", "Basis"]]
for tb in sorted(TABLES):
    o = TABLES[tb]["owner"]
    basis = TABLES[tb]["basis"]
    basis = ("Ownership Map ruling" if TABLES[tb].get("ruling") else "Ownership Map v1, Tables sheet") + (f"; {TABLES[tb]['asm']}" if TABLES[tb].get("asm") else "")
    rows.append([tb, o, TABLES[tb].get("schema", SVC[o]["schema"] if o in SVC else "every rwb_* schema"), basis])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Conformance")
X.append("")
rows = [["#", "Contract rule", "Tested by"]]
conf = [
    "The provider publishes its OpenAPI 3.1, AsyncAPI 3.0 and activity contract jar before the implementation story starts",
    "Every operation in section 6 exists in the published contract, under the service's own base path",
    "Every event the service publishes is in its AsyncAPI document, on its own topic, with CloudEvents 1.0 binary mode and key caseId",
    "Every event the service consumes is deduplicated in processed_event, in the same transaction as the change",
    "Every activity and child workflow the service calls is declared in the provider's contract jar; no service imports another service's code",
    "No REST chain longer than one hop; route services reach shared capabilities through Temporal",
    "No cross-schema read, join, view or foreign key; the boundary test fails the build on any violation",
    "Every POST and PATCH is idempotent through Idempotency-Key, and every consumer of the same key returns the first result",
    "Error responses follow RFC 9457 for REST and the error code form for events",
    "The provider's fake serves every operation and every event of its contract",
    "The pair is proved end to end in the integration story of the later wave",
    "The contract document is registered in section 6 with its version",
]
ctests = ["Contract publication gate in the pipeline", "OpenAPI diff against the Ownership Map Endpoints sheet",
          "AsyncAPI validation plus a schema registry check", "Inbox test", "Activity contract test",
          "Contract test plus trace-depth check", "Architecture test", "Idempotency test", "Contract example test",
          "Fake conformance test in the consumer build", "RWB-ITG-W<n> harness", "Registration check on the CON story"]
for n, (a, b) in enumerate(zip(conf, ctests), 1):
    rows.append([n, a, b])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Open points")
X.append("")
rows = [["ID", "Point", "Effect in this catalogue", "Owner role"]]
pts = [
    ("CG-B-ARCH-CON-1", "No earlier Service Contract Catalog exists, so v1 carries no inherited sections, IDs, numbers or dates", "Version 1, status Draft; the change-log row is the first", "Delivery lead"),
    ("CG-B-ARCH-CON-2", "The Ownership Map Endpoints sheet holds the monolith operations of API Specification v4, while Architecture v5 slide 41 states a per-service base path; the per-service paths and payloads are written in API Specification v5", "Section 6 lists the operation per owning service under its base path and leaves the final path to API Specification v5", "Solution architect"),
    ("CG-B-ARCH-CON-3", "The coordinates of the activity contract jars (groupId, artifactId, version) are not specified", "Section 7.1 states the artefact and the package root, and leaves the coordinates open", "Tech lead"),
    ("CG-B-ARCH-CON-4", "The event catalogue does not name the consumers of ApprovalDecided or ReportPublished", "The two rows state Not specified in the source documents", "Solution architect"),
    ("CG-B-ARCH-CON-5", "The schema registry product and its deployment are not specified; only the BACKWARD compatibility rule is stated", "Section 7.2 states the compatibility rule and not the product", "Platform architect"),
    ("CG-B-ARCH-CON-6", "The slide 13 rule that route services reach shared capabilities through Temporal sits beside REST cells from S1, S7 and S8 to rwb-source-data", "Section 8.3 reads the rule as covering the five shared capabilities named in the slide note; the rwb-source-data reads stay REST", "Solution architect"),
    ("CG-B-ARCH-CON-7", "The request and response content of the Enterprise AI private endpoint (INT-23) is not specified", "Section 8.4 names the edge and the stub, not a payload", "Solution architect"),
    ("CG-B-ARCH-CON-8", "The call-type matrix marks S5 to P6 as Temporal, but the asset contract on Architecture v5 slide 19 names no communications interface and no other slide supplies one", "Section 6.15 carries the placeholder in its Temporal row and no interface is invented", "Solution architect"),
]
for r in pts:
    rows.append(list(r))
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Change log")
X.append("")
rows = [["Version", "Date", "Change", "Detail"],
        ["1", DATE, f"{DEC} microservice realignment, {TOOL}",
         "First Service Contract Catalog: contract model, call-type matrix, contract inventory, contract by service, shared platform contracts, dependency classes, contract tests and change control"]]
for r in rows:
    X.append("| " + " | ".join(r) + " |")
X.append("")

for line in X:
    if line.startswith("|") and "|" in line[1:]:
        cells = line.strip().strip("|").split("|")
        for cell in cells:
            if "\n" in cell:
                raise SystemExit("NEWLINE IN CELL")
XLSX_MD.write_text("\n".join(X) + "\n", encoding="utf-8")
print("WROTE", XLSX_MD)

# ================================================================ gap and assumption rows
gap_rows = [
    {"id": "CG-B-ARCH-CON-1", "title": "No earlier Service Contract Catalog exists",
     "source": "05 Technical architecture (folder listing); Template and Rules \u00a7R8.4", "section": "Document control; section 12",
     "description": "This family has no earlier version, so v1 cannot inherit sections, IDs, numbers or dates from it.",
     "evidence": "No Service Contract Catalog file exists in folder 05 or anywhere else in the set; Template and Rules \u00a7R8.4 lists Service Contract Catalog v1 as a new architecture output.",
     "type": "Missing", "area": "Document version", "severity": "P3", "needed_by_wave": 0, "legacy_ref": "",
     "owner_role": "Delivery lead", "asm": "ASM-B-ARCH-CON-1",
     "proposed": "Publish v1 as the first version, status Draft, and start the change log with the D-RCV-60 row.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-2", "title": "Ownership Map endpoints are the monolith operations",
     "source": "Recovery Workbench Microservice Ownership Map v1, Endpoints sheet; Architecture v5 Text Extract v1 slide 41", "section": "Section 6",
     "description": "The Endpoints sheet holds 156 operations with the monolith paths of API Specification v4 and a per-module owner, while Architecture v5 slide 41 states a per-service base path. The per-service path and payload of each operation are not written in any source in this read set.",
     "evidence": "Ownership Map v1 Endpoints sheet rows such as GET /cases/{caseId} owned by P3; Architecture v5 slide 41 gives the base /api/recovery/case/v1; API Specification v5 is the document that rewrites them.",
     "type": "Ambiguous", "area": "REST contract", "severity": "P2", "needed_by_wave": 1, "legacy_ref": "RWB-E1-001",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-2",
     "proposed": "List each operation under its owning service and its Architecture v5 base path, and leave the final operation path and payload to API Specification v5.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-3", "title": "Activity contract jar coordinates are not specified",
     "source": "Architecture v5 Text Extract v1 slide 11; Temporal and Drools Design Text Extract v1 slide 12", "section": "Section 7.1",
     "description": "Each service publishes an activity contract jar on its own task queue, but no source states the groupId, artifactId or versioning scheme of those jars.",
     "evidence": "Temporal and Drools Design slide 12 names the L4 activity contracts per service; Architecture v5 says no service imports another's code, only its contract jar; neither gives coordinates.",
     "type": "Missing", "area": "Temporal contract", "severity": "P2", "needed_by_wave": 1, "legacy_ref": "",
     "owner_role": "Tech lead", "asm": "ASM-B-ARCH-CON-3",
     "proposed": "State the artefact and the Java package root now, and allocate the coordinates with the repositories in the service template work.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-4", "title": "Consumers of two events are not named",
     "source": "Architecture v5 Text Extract v1 slides 42 and 43", "section": "Section 5; section 6",
     "description": "The event catalogue names no consumer for ApprovalDecided (rwb.decision.events.v1) or ReportPublished (rwb.reporting.events.v1), although both events are listed in the service contracts of slide 14 as OUT.",
     "evidence": "Slide 14 P7 OUT names ApprovalDecided; slide 15 P9 OUT names ReportPublished; slides 42 and 43 give consumers for every other event and none for these two.",
     "type": "Missing", "area": "Event contract", "severity": "P3", "needed_by_wave": 1, "legacy_ref": "",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-4",
     "proposed": "Carry the two rows with the placeholder and settle the consumers with the API and event catalogue owners.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-5", "title": "Schema registry product is not specified",
     "source": "Architecture v5 Text Extract v1 slide 42 notes", "section": "Section 7.2",
     "description": "The sources fix the compatibility rule (BACKWARD) and the AsyncAPI per service, but not the registry product, its deployment or its retention.",
     "evidence": "Architecture v5 slide 42 notes: schemas are versioned in the registry with BACKWARD compatibility. No product is named anywhere in the read set.",
     "type": "Missing", "area": "Event contract", "severity": "P3", "needed_by_wave": 1, "legacy_ref": "",
     "owner_role": "Platform architect", "asm": "ASM-B-ARCH-CON-5",
     "proposed": "State the compatibility rule and the artefact in this catalogue; choose the product in the Kafka event platform work.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-6", "title": "Route-services-through-Temporal rule meets REST cells to rwb-source-data",
     "source": "Architecture v5 Text Extract v1 slide 13", "section": "Section 4; section 8.3",
     "description": "Slide 13 states that route services reach shared capabilities through Temporal, never REST, and the same matrix gives REST cells from S1, S7 and S8 to rwb-source-data.",
     "evidence": "Slide 13 note: route services reach shared capabilities through Temporal, never REST, only rwb-source-data touches ACE's tables. Matrix cells S1 to P1, S7 to P1 and S8 to P1 are R.",
     "type": "Conflict", "area": "Call type", "severity": "P2", "needed_by_wave": 1, "legacy_ref": "",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-6",
     "proposed": "Read the rule as covering the five shared capabilities named in the slide note (decision, document, payment, partner, comms); keep the rwb-source-data reference reads as REST, one hop and cached.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-7", "title": "Enterprise AI endpoint contract is not specified",
     "source": "Architecture v5 Text Extract v1 slide 16", "section": "Section 8.4",
     "description": "rwb-agent calls Enterprise AI on an HTTPS private endpoint (INT-23); no source in the read set gives the request, the response, the timeout or the model routing.",
     "evidence": "Slide 16 P10 OUT: Enterprise AI endpoint: HTTPS private endpoint. The System Disposition and Integration Inventory names INT-23 only.",
     "type": "Missing", "area": "External contract", "severity": "P3", "needed_by_wave": 2, "legacy_ref": "",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-7",
     "proposed": "Name the edge and the test double here, and settle the payload with the P10 agent work.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-8", "title": "Matrix cell S5 to P6 has no named interface",
     "source": "Architecture v5 Text Extract v1 slides 13, 17 and 19", "section": "Section 5; section 6.15",
     "description": "The call-type matrix marks the S5 Asset row against P6 Communications as Temporal, but the asset contract on slide 19 lists no communications call and no other slide names one.",
     "evidence": "Slide 13 S5 row, P6 column: T. Slide 19 S5 OUT: Partner issueInstruction, Decision approval, Payment postProceeds, and no comms entry.",
     "type": "Conflict", "area": "Temporal contract", "severity": "P3", "needed_by_wave": 2, "legacy_ref": "",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-8",
     "proposed": "Carry the row with the placeholder in section 6.15 and confirm the interface with the S5 and P6 owners; do not invent an operation.", "wp": "B-ARCH-CON"},
]
GAPS.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in gap_rows) + "\n", encoding="utf-8")

asm_rows = [
    {"id": "ASM-B-ARCH-CON-1", "text": "This is version 1 of the Service Contract Catalog and it inherits no section, ID, number or date.",
     "why": "No earlier version of the family exists.", "read": "Folder 05 listing; Template and Rules \u00a7R8.4", "gap": "CG-B-ARCH-CON-1",
     "applied_in": "Document control; section 12", "confidence": "High", "confirm": "Delivery lead", "impact": "None on content; the change log starts here.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-2", "text": "The Ownership Map Endpoints sheet is read as the operation set per owning service; the per-service base path comes from Architecture v5 slide 41 and Template and Rules \u00a7R4, and the final path and payload belong to API Specification v5.",
     "why": "Two sources describe the REST surface at different levels.", "read": "Ownership Map v1, Endpoints sheet; Architecture v5 slide 41; Template and Rules \u00a7R4", "gap": "CG-B-ARCH-CON-2",
     "applied_in": "Section 6, REST operations owned", "confidence": "Medium", "confirm": "Solution architect", "impact": "No operation is added or removed; only the base path is applied.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-3", "text": "The activity contract jars are named by their task queue and Java package root; the coordinates are left open for allocation.",
     "why": "The coordinates are not stated in any source.", "read": "Architecture v5 slide 11; Temporal and Drools Design slide 12", "gap": "CG-B-ARCH-CON-3",
     "applied_in": "Section 7.1", "confidence": "Medium", "confirm": "Tech lead", "impact": "The build story allocates coordinates; no contract changes.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-4", "text": "ApprovalDecided and ReportPublished are recorded with the placeholder for their consumers rather than an assumed consumer.",
     "why": "The event catalogue names no consumer.", "read": "Architecture v5 slides 14, 15, 42, 43", "gap": "CG-B-ARCH-CON-4",
     "applied_in": "Section 5; section 6", "confidence": "High", "confirm": "Solution architect", "impact": "Two registry rows stay open.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-5", "text": "This catalogue states the AsyncAPI artefact, CloudEvents 1.0 binary mode and BACKWARD compatibility, and does not name a registry product.",
     "why": "The product is not specified in the read set.", "read": "Architecture v5 slide 42 notes", "gap": "CG-B-ARCH-CON-5",
     "applied_in": "Section 7.2", "confidence": "High", "confirm": "Platform architect", "impact": "The platform work chooses the product; the contract rule holds either way.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-6", "text": "The rule that route services reach shared capabilities through Temporal is read as covering decision, document, payment, partner and communications, the five capabilities the slide note names; the rwb-source-data reference reads stay REST, one hop and cached.",
     "why": "The matrix gives both REST cells to rwb-source-data and the rule.", "read": "Architecture v5 slide 13 and its notes", "gap": "CG-B-ARCH-CON-6",
     "applied_in": "Section 4; section 8.3", "confidence": "Medium", "confirm": "Solution architect", "impact": "Three REST pairs stay synchronous; no route service gains a REST call to a shared capability.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-7", "text": "The Enterprise AI call is carried as an edge contract with a recorded-response double; no payload is stated.",
     "why": "The integration contract is not specified.", "read": "Architecture v5 slide 16", "gap": "CG-B-ARCH-CON-7",
     "applied_in": "Section 8.4", "confidence": "Medium", "confirm": "Solution architect", "impact": "P10 tests against the double until the endpoint contract is agreed.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-8", "text": "The S5 to P6 Temporal cell is kept with the placeholder and no interface is invented.",
     "why": "The matrix and the service contract disagree.", "read": "Architecture v5 slides 13 and 19", "gap": "CG-B-ARCH-CON-8",
     "applied_in": "Section 5; section 6.15", "confidence": "Medium", "confirm": "Solution architect", "impact": "One Temporal row stays open in the S5 contract.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-9", "text": "Every cross-service pair is class C for the consuming story and class I for the integration story of the later wave; every pair that touches gateway-bff, ACE Common, the ACE database, Enterprise AI, the bank file channels or partners is class X.",
     "why": "Template and Rules \u00a7R5.4 defines the classes but not the assignment per pair.", "read": "Template and Rules \u00a7R5.4", "gap": "",
     "applied_in": "Section 5; section 8.1", "confidence": "High", "confirm": "Solution architect", "impact": "No consumer story waits for a provider build.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-10", "text": "No release date is held in this catalogue; the dates in the Release Plan are unchanged and every one is tentative.",
     "why": "Decision U7 and DL48 fix this, and the source has no release date.", "read": "Template and Rules \u00a7R1 (U7); Architecture v5 slide 38", "gap": "",
     "applied_in": "Section 1", "confidence": "High", "confirm": "Delivery lead", "impact": "None; this catalogue carries no date but the document date.", "wp": "B-ARCH-CON"},
]
ASMS.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in asm_rows) + "\n", encoding="utf-8")
print("WROTE", GAPS, "and", ASMS, len(gap_rows), len(asm_rows))
