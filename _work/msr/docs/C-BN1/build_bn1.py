"""C-BN1 scratch: build 04 User stories/Recovery Workbench Build Notes Epic 1 v7.md."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr"
SRC = ROOT / "04 User stories" / "Recovery Workbench Build Notes Epic 1 v6.md"
OUT = ROOT / "04 User stories" / "Recovery Workbench Build Notes Epic 1 v7.md"

d = json.loads((WORK / "docs" / "C-BN1" / "data.json").read_text(encoding="utf-8"))
STORIES = d["stories"]
LEGACY = d["legacy"]
TABLES = d["tables"]

SVC = {
    "P1": ("rwb-source-data", "rwb_source_data"), "P2": ("rwb-integration", "rwb_integration"),
    "P3": ("rwb-case", "rwb_case"), "P4": ("rwb-access", "rwb_access"),
    "P5": ("rwb-document", "rwb_document"), "P6": ("rwb-comms", "rwb_comms"),
    "P7": ("rwb-decision", "rwb_decision"), "P8": ("rwb-payment", "rwb_payment"),
    "P9": ("rwb-reporting", "rwb_reporting"), "P10": ("rwb-agent", "rwb_agent"),
    "S1": ("rwb-valuation", "rwb_valuation"), "S2": ("rwb-treatment", "rwb_treatment"),
    "S3": ("rwb-guarantee", "rwb_guarantee"), "S4": ("rwb-litigation", "rwb_litigation"),
    "S5": ("rwb-asset", "rwb_asset"), "S6": ("rwb-debtsale", "rwb_debtsale"),
    "S7": ("rwb-writeoff", "rwb_writeoff"), "S8": ("rwb-deviation", "rwb_deviation"),
    "S9": ("rwb-partner", "rwb_partner"),
}
WAVE = {"P1": 1, "P2": 1, "P3": 1, "P4": 1, "P5": 1, "P6": 1, "P7": 1, "P8": 2, "P9": 1, "P10": 1,
        "S1": 3, "S2": 2, "S3": 3, "S4": 3, "S5": 2, "S6": 3, "S7": 4, "S8": 2, "S9": 4}
WT_ORDER = {"Contract": 0, "App development": 1, "ACE DB": 2, "Infrastructure": 3, "DevOps": 4, "Integration": 5}

# What the realignment changes, per legacy key. One or more sentences, sourced from the
# Ownership Map, the split plan, Arch v5, the Temporal and Drools design and Template and Rules R5-R6.
NOTES = {
 "RWB-E1-001": "The one `recovery` schema becomes 19 schemas (ADR-014). This story keeps the dictionary, the data products and the four extension tables in `rwb_source_data`; every other table moves to the schema of the service that owns it, and the split is new work carried by RWB-PLT-NF06-DB and the per-service DB stories (Template and Rules \u00a7R6). The built migration is unchanged until the split stories are picked up.",
 "RWB-E1-002": "The case list row stays with P1 in `rwb_source_data` and the case itself comes from P3 `rwb_case` through the case API (R-PREC default ruling: case list API to rwb-case). The ACE read moves to P1 only, so this story no longer names `v_ace_account`, `v_ace_efs_action` or `v_ace_batch_status`; the P3 slice reads the freshness of DP01 from P1's contract.",
 "RWB-E1-007": "The outbound adapter stays with P2 `rwb_integration`, and the outbox, inbox and idempotency tables become the platform library objects created in P2's own schema (DP-09). `debt_sale_account` is owned by S6 `rwb_debtsale`, so the write named in the View note goes through S6's contract (CG-BN1-7). The P3, P4, P5 and P6 slices consume the file contract and name no ACE view.",
 "RWB-E1-008": "The decision log store becomes P7 `rwb_decision`, and the writer that other services call is the platform library RWB-PLT-E1027 (DP-03). The P4 slice records an access decision through that library and keeps no ledger table of its own.",
 "RWB-E1-011": "Reconciliation stays with P1 `rwb_source_data` and reads the ACE views there. The case rows it reconciles come from P3 `rwb_case` through the case API, and the P6 and S5 slices consume the reconciliation result as a report rather than reading a P1 table (CG-BN1-16).",
 "RWB-E1-013": "The measures and snapshots stay with P9 `rwb_reporting`. Money collected comes from P1's payment read and the case stock from P3 `rwb_case`, both by contract; P9 names no ACE view and holds only `measure_definition` and `measure_snapshot`.",
 "RWB-E1-014": "The decision log copy has no target: Arch v5 has no data lake, so there is no lake copy to make (DP-17). `lake_copy_watermark` has no target and P1's DB story drops it, and the change is recorded in the Change Register (CG-BN1-12).",
 "RWB-E1-015": "The freshness stamp stays with P1 `rwb_source_data`, which publishes it through `GET /freshness` and the `AceDataReady` and `AceDataLate` events. Every other service reads the business date from that contract instead of stamping a copy of `data_product_load` (CG-BN1-1).",
 "RWB-E1-016": "The data product access rows stay with P1 `rwb_source_data`; `masking_rule` is owned by P4 `rwb_access` (Ownership Map), so the masking rows this story relies on come from P4's contract. The access decisions are made per product and per view, not per table copy.",
 "RWB-E1-017": "`retention_rule` and `retention_action` are owned by P5 `rwb_document` (Ownership Map ruling, ASM-A6-tables-10), so P1's retention classes end and P5 applies them to Workbench documents (CG-BN1-5). P7 keeps the decision log retention by contract.",
 "RWB-E1-070": "The Temporal platform is platform work: RWB-PLT-E1070 owns the cluster, its namespace `rwb-recovery`, its upgrades and its run book, and lives in a platform lane (CG-BN1-10). P3 consumes the platform through the SDK and contributes no platform story.",
 "RWB-E1-071": "The worker kit and the smoke workflow are platform work (RWB-PLT-E1071), and the platform story also replaces the Quartz scheduler of RWB-TE-007 (DP-10). P3 registers its own workflow and activity classes and its own task queue `rwb-case`.",
 "RWB-E1-072": "The rule registry is P7 `rwb_decision` (Ownership Map ruling, ASM-A6-tables-3) and the runtime is the embedded Drools kit RWB-PLT-E1072 (DP-04). The table location in the source note is superseded: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 tables, and a service holds only its evaluated copy (CG-BN1-4). The five Epic 1 package codes are not reconciled with the eight phase 1 packages of the design (CG-BN1-14).",
 "RWB-E1-073": "Authoring, test, four-eyes approval, valid-from dating and rollback are central in P7 `rwb_decision`; evaluation is local in the owning service (Temporal and Drools design slide 15). The P3, P6 and P2 slices are the package owners of their own rules, and each fetches a version with `GET /rule-models/{n}/{v}` and verifies the checksum (CG-BN1-4).",
 "RWB-E1-018": "The case, the case accounts and parties and the entry exclusion stay with P3 `rwb_case`. `party_ext` and `account_ext` are P1 extension tables (Ownership Map), so the write named in the View note becomes a P1 story and P3 calls it by contract (CG-BN1-9). The entry gate reads the ACE batch state from P1's freshness contract.",
 "RWB-E1-019": "Teams and queues stay with P3 `rwb_case`; `role` is owned by P4 `rwb_access`, so the role load in this story becomes a P4 story and P3 reads roles by contract (CG-BN1-6). The reference rows and their versions stay with P3 (R-PREC default ruling, DP-07).",
 "RWB-E1-020": "Allocation stays with P3 `rwb_case`; the queue membership it reads is its own and the rule rows are P7's, reached by contract (DP-04). The P4 slice authorises the assignment, the P7 slice records it and the S8 slice reacts to the case state; none of them writes a case table.",
 "RWB-E1-021": "Transfers stay with P3 `rwb_case`; the rule rows are P7's and the decision entries are P7's, both by contract. The S8 slice clears a deviation on transfer, and P4 authorises it, so the transfer holds no cross-service constraint.",
 "RWB-E1-022": "Sign-on and the first roles are P4 `rwb_access`, which owns `role`, `permission` and `role_conflict`. Identity comes from ACE Common (Entra) through the sign-in contract, and no ACE identity table is copied.",
 "RWB-E1-023": "The case record is P3 `rwb_case`; the documents are P5's and the interactions are P1's, so both are read by contract. The five ACE views are read by P1 only, and the freshness line the note describes arrives from P1's contract (CG-BN1-1).",
 "RWB-E1-024": "The document store and index are P5 `rwb_document`, which owns `document`, `document_field`, `document_type` and `document_hub_parameter`. Files go to the P5 Blob container, and no ACE table is read.",
 "RWB-E1-025": "The document types and fields are P5 `rwb_document` reference data. The type list comes from the fields the P1 view contract can supply plus the types legal counsel signs off, so the story names no view itself.",
 "RWB-E1-026": "The attach and search screen is served by P5 `rwb_document`, composed at gateway-bff from P5 and P3 calls (DP-19). The case key comes from P3's contract and the type list from P5's own reference data.",
 "RWB-E1-027": "The writer stays with P7 `rwb_decision`; the library that other services embed is RWB-PLT-E1027 and the shared topic is `rwb.decision-record.v1` (DP-03). P7 also serves `GET /api/recovery/decision/v1/decision-log`.",
 "RWB-E1-028": "Service levels and timers are P3 `rwb_case`: the clock is a durable timer inside `CaseWorkflow` and `timer` remains the screen projection (Ownership Map ruling, ASM-A6-tables-12). Days past due and the prescription basis come from P1's account read, and the decision entries are P7's.",
 "RWB-E1-030": "Rebalancing stays with P3 `rwb_case` and runs as a Temporal Schedule in `rwb-case` (JOB-06, Arch v5 slide 44), not as a Quartz job. The case list it waits on comes from P1's contract, and the decision entries are P7's.",
 "RWB-E1-031": "The queue and owner filter is P3 `rwb_case`, served by `GET /api/recovery/case/v1/cases` and `/queues/{queueId}/cases`. The product category shown when the caller may see it comes from P1's account read.",
 "RWB-E1-032": "The OCR intake attach is P5 `rwb_document`. The account key it matches comes from P1's account read, the intake can also arrive from a partner SFTP (S9 slice), and the decision entry is P7's.",
 "RWB-E1-033": "Search stays with P5 `rwb_document` over `document_text`, `document_field` and `document`. An ACE field is reached through the P1 view contract and only when a document links to one.",
 "RWB-E1-034": "Letter template management is P6 `rwb_comms`, which owns `template`, `merge_field` and the notice catalogue. The LOV rows are P3's reference data, read by contract (DP-07).",
 "RWB-E1-035": "The timeline is P3 `rwb_case`; `interaction` is owned by P1 `rwb_source_data` (DP-18 ruling), so the timeline reads the ledger by contract. Documents come from P5 and decision entries from P7.",
 "RWB-E1-037": "The role to permission matrix and masking policy are P4 `rwb_access`, and the guard library other services embed is RWB-PLT-E1037 (DP-08). The two masked identity fields come from P1's customer read, which never exposes a clear identity number.",
 "RWB-E1-038": "The delegation of authority table is P4 `rwb_access` (Ownership Map ruling, ASM-A6-tables-4) and is read by `GET /api/recovery/access/v1/doa-limits`. The LOV rows are P3's reference data, read by contract.",
 "RWB-E1-039": "Access logging is P4 `rwb_access`: a break-glass action is a decision record written through the RWB-PLT-E1027 library and stored in P7's ledger (DP-03). The P5 and P7 slices consume the event.",
 "RWB-E1-040": "The document checklist is P5 `rwb_document` reference data over its own `document_type`, `document` and `case_document_check`. The case key comes from P3's contract.",
 "RWB-E1-041": "Retention classes and the virus scan are P5 `rwb_document`, which owns `retention_rule`, `retention_action` and the scan state. ACE source documents stay in ACE, and the scan runs on the P5 intake only.",
 "RWB-E1-042": "The parameter catalogue stays with P3 `rwb_case` (R-PREC default ruling, DP-06) and is served by `GET /api/recovery/case/v1/admin/parameters`. The client library other services embed is RWB-PLT-E1042; the story is preserved, and the microservice change ships as the platform CON and APP stories and the P3 CON and APP stories.",
 "RWB-E1-043": "Versioned reference data stays with P3 `rwb_case` (R-PREC default ruling, DP-07) and is served by the reference-load endpoints. The client library other services embed is RWB-PLT-E1043; the story is preserved, and the microservice change ships as the platform CON and APP stories and the P3 CON and APP stories.",
 "RWB-E1-044": "Database migrations become the platform template rule RWB-PLT-E1044 (DP-15): one Flyway sequence per service in that service's own schema. The preserved story keeps its base ID and the microservice change ships as `RWB-PLT-E1044-APP-2`.",
 "RWB-E1-045": "Multi-product parameters stay with P3 `rwb_case`; the product category they are keyed by comes from P1's account read. The three products stay reference data, and no ACE table is read.",
 "RWB-E1-046": "The template and merge field catalogue is P6 `rwb_comms` reference data. The fields are checked against P1's dictionary contract, so a merge field names a BR Field ID and never a source column.",
 "RWB-E1-047": "Feature flags move to the platform library (R-PREC default ruling, ASM-A6-tables-7), which owns `feature_flag` and `feature_flag_change`; P2's admin API serves them (CG-BN1-8). Section B features keep a flag until RWB-ACE-001 is deployed and V0003 applies.",
 "RWB-E1-049": "The OCR pipeline stays with P5 `rwb_document`, which owns `document_intake`, `document_text` and `document_hub_parameter`. The worker pool runs in the P5 namespace, and the P6 slice consumes `DocumentFieldsExtracted`.",
 "RWB-E1-050": "Classification stays with P5 `rwb_document`; the P3 slice links the classified document to the case by contract. The classifier reads the document text only.",
 "RWB-E1-052": "Notice generation is P6 `rwb_comms`: the merge values come from P1's account, customer and contact reads, the proof of delivery from P1's `v_ace_pod` read, the documents from P5 and the approval from P7. P6 names no ACE view.",
 "RWB-E1-053": "Field extraction stays with P5 `rwb_document`. An ACE field is compared through the P1 dictionary entry and never written back.",
 "RWB-E1-054": "The review queue is P5 `rwb_document`; masking follows P4's policy, the case key comes from P3's contract and the decision entry from P7. A reviewer confirms a Workbench field, and no ACE object is updated.",
 "RWB-E1-055": "Proof of delivery is P6 `rwb_comms`; the delivery evidence comes from P1's `v_ace_pod` read, the case from P3, the notice from P6 and the document from P5. P1's read stays behind its flag until RWB-ACE-001 lands.",
 "RWB-E1-056": "The run books and monitoring are platform work: RWB-PLT-E1056-OPS gives every Workbench job and the ACE batch record a run book, and each service's own run book rows move to its ops lane (CG-BN1-11). The `job_catalog` view stays with P2 (Ownership Map ruling).",
 "RWB-E1-057": "Intake is P5 `rwb_document`, with a partner SFTP source from S9 and the worker pool in the P5 namespace. ACE ingests no document from this path, and the file record stays in `document_intake`.",
 "RWB-E1-058": "The agent platform is P10 `rwb_agent`, which owns `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation`, `agent_evaluation_run`, `agent_feedback` and `agent_alert`. The case facts come from P3 and the rule rows from P7, both by contract.",
 "RWB-E1-059": "The shadow case intake agent is P10 `rwb_agent`; the values it compares come from P1's collateral and contact reads, and its results stay in the P10 tables. The ACE read stays behind P1's flag until RWB-ACE-001 lands.",
 "RWB-E1-060": "The extraction evaluation is P10 `rwb_agent` over P5's extracted fields, read by contract. The reviewed Workbench field is P5's record, and the agent never writes it.",
 "RWB-E1-061": "The intake agent evaluation and the L1 proposal are P10 `rwb_agent`; the proposal is a decision record in P7's ledger, not an automatic case change. The case state comes from P3 by contract.",
 "RWB-E1-062": "Screening stays with P10 `rwb_agent`, while `deviation` is owned by S8 `rwb_deviation`: the agent proposes and S8 records the deviation (Ownership Map). The P5, P7 and P4 slices supply fields, rule rows and masking.",
 "RWB-E1-063": "The agent monitoring dashboard is P10 `rwb_agent` over its own runs, policies, evaluations and alerts, with the freshness line of the products the agents read supplied by P1. The P4, P6 and OPS slices add masking, contacts and alerting.",
 "RWB-E1-064": "The dictionary stays with P1 `rwb_source_data`, which owns `sys_objects`, `sys_fields`, `sys_field_version`, `data_contract` and `data_product`. It is the one place where a P1 view column and its ACE source field are defined, and P4 consumes it for access decisions.",
 "RWB-E1-065": "The sandbox stays with P1 `rwb_source_data`, but it now applies 19 Flyway sequences into 19 schemas and fills the tables each service owns (CG-BN1-15). The P4, P3, S8 and P5 slices seed their own schemas, and the 30 views remain P1 artefacts.",
 "RWB-E1-066": "The interaction ledger is P1 `rwb_source_data` (R-PREC default ruling, DP-18), which owns `interaction`. The case key comes from P3's contract, and the case timeline in P3 reads the ledger by contract.",
 "RWB-E1-067": "Every Workbench action into the ledger is P1 `rwb_source_data`; the interception library is the platform inbox and outbox (DP-09), and an ACE change reaches the ledger as an event reference. The P3 and P5 slices publish their actions.",
 "RWB-E1-068": "The ledger read interface is P1 `rwb_source_data`, served under `/api/recovery/source-data/v1`; P3's case timeline reads the ledger through it (DP-18), and masking of `summary` follows P4's policy.",
 "RWB-E1-069": "The views, the grants and the view conformance test stay with P1 `rwb_source_data`, but the single `recovery_svc` login is replaced by one login per service (DP-02; CG-BN1-3), and the grants are split so that each service holds DML only in its own schema. V0002 ships the Section A views and V0003 the Section B views, and only P1 names them.",
 "RWB-TE-001": "The folder layout and the boundary test become the platform template rule RWB-PLT-TE001 (DP-13, DP-19), and the microservice change ships as the delta copy `RWB-PLT-TE001-APP-2`. Rule BND-6 is applied per service against the 30 view names in `recovery-modules.yaml`, which is a P1 artefact.",
 "RWB-TE-002": "Code owners become the platform template rule RWB-PLT-TE002 and cover the 19 service folders as well as the view migrations. The OPS slice publishes the ownership map that the Ownership Map v1 records by team type only.",
 "RWB-TE-003": "The generated types and contract tests become the platform template rule RWB-PLT-TE003, with the microservice change in `RWB-PLT-TE003-APP-2`. Every service's contract test is generated from its own OpenAPI and AsyncAPI documents under `/api/recovery/<short>/v1`.",
 "RWB-TE-004": "The masked copy becomes platform work (RWB-PLT-TE004), but the tables it fills belong to P3, P5 and P1, so the copy can only run in the owning service's own schema and no such service story exists yet (CG-BN1-17). ACE supplies its own SIT and UAT data.",
 "RWB-TE-006": "The outbox and retry library is the platform rule RWB-PLT-TE006 (DP-09), embedded in every service with its own `outbox_event`, `outbox_delivery` and `processed_event` tables. A failed ACE ingest is ACE's retry and shows as a stale product.",
 "RWB-TE-007": "The Quartz scheduler is replaced by Temporal Schedules in the owning service (RWB-PLT-E1071, DP-10; Arch v5 slide 44), and every dependency on TE-007 points to RWB-PLT-E1071-CON (CG-BN1-13).",
 "RWB-TE-008": "The decision log hash-chain check becomes the platform rule RWB-PLT-TE008 and runs over P7's ledger. The chain covers entries that name ACE business keys, and P7 exposes the check as a Schedule.",
 "RWB-TE-011": "The PDPA lint becomes the platform rule RWB-PLT-TE011 and reads the field list from P1's dictionary, so the view columns and the Workbench fields are covered by one rule set. The lint runs per service in its own pipeline.",
 "RWB-TE-012": "The document storage containers become the platform rule RWB-PLT-TE012 and hold P5 documents only; an ACE source document stays in ACE. The container carries the WORM policy of Arch v5 slide 16.",
 "RWB-TE-013": "The agent runtime client and its fallback become the P10 contract RWB-P10-TE013 (DP-20), which P7's decision centre also calls. The fallback keeps a person in the path when the agent runtime is unavailable.",
}

# ---------------------------------------------------------------- source split

src = SRC.read_text(encoding="utf-8")
head, rest = src.split("## RWB-E1-001 Recovery tables for the 14 data products", 1)
sections = ["## RWB-E1-001 Recovery tables for the 14 data products" + rest]
sections = re.split(r"(?m)^(?=## RWB-)", sections[0])
sections = [s for s in sections if s.strip()]
assert len(sections) == 72, len(sections)
keys = [re.match(r"## (\S+)", s).group(1) for s in sections]
assert set(keys) == set(NOTES) | {"RWB-E1-014", "RWB-TE-007"}, set(keys) ^ set(NOTES)

# ---------------------------------------------------------------- helpers


def esc(t):
    return t.replace("|", "\\|")


def story_line(s):
    return "`{}` ({}, `{}`, {})".format(s["id"], s["wt"], s["lane"], s["ready"].replace("After ", "after "))


def group_by_service(sts):
    out = {}
    for s in sorted(sts, key=lambda x: (x["service"], WT_ORDER.get(x["wt"], 9), x["id"])):
        out.setdefault(s["service"], []).append(s)
    return out


def tables_in(key):
    body = next(s for s in sections if s.startswith("## " + key + " "))
    toks = set(re.findall(r"`([a-z][a-z0-9_]+)`", body))
    return sorted(t for t in toks if t in TABLES)


def owner_text(code):
    if code == "PLT":
        return "platform library (no service schema)"
    return "{} `{}`".format(code, SVC[code][1])


NAME2CODE = {v[0]: k for k, v in SVC.items()}


def svc_label(c):
    if c == "integration":
        return "integration `RWB-ITG-W1`"
    if c == "platform":
        return "platform (wave 0, `CG-W0` and `L-PLT-*`)"
    code = NAME2CODE.get(c)
    return "{} `{}`".format(code, c)


def svc_short(c):
    if c == "integration":
        return "integration"
    if c == "platform":
        return "platform"
    return "{} `{}`".format(NAME2CODE.get(c), c)


def block(key):
    sts = STORIES.get(key, [])
    if not sts:
        return ("**Service and lane.** Retired (D-RCV-60): no new story, no lane and no Day-1 work. "
                "The source note above is kept word for word for traceability.\n\n"
                "**What moves.** " + NOTES[key] + "\n")
    pri = LEGACY[key]["primary"]
    svcs = group_by_service(sts)
    lines = []
    order = sorted(svcs, key=lambda c: (0 if NAME2CODE.get(c) == pri else 1, c))
    names = []
    for c in order:
        names.append(svc_label(c) + (" (primary)" if NAME2CODE.get(c) == pri else ""))
    lines.append("**Service and lane.** " + "; ".join(names) + ".")
    lines.append("")
    for c in order:
        lines.append("- {}: {}.".format(svc_short(c), "; ".join(story_line(s) for s in svcs[c])))
    lines.append("")
    day1 = [s["id"] for s in sts if s["ready"] == "Day 1"]
    later = [s for s in sts if s["ready"] != "Day 1"]
    ready = "Ready to start: Day 1 for {} of the {} stories".format(len(day1), len(sts))
    if later:
        ready += "; " + "; ".join("`{}` {}".format(s["id"], s["ready"].replace("After ", "after ")) for s in later)
    lines.append(ready + ".")
    lines.append("")
    tb = tables_in(key)
    if tb:
        parts = []
        for t in tb:
            parts.append("`{}` {}".format(t, owner_text(TABLES[t]["owner"])))
        lines.append("**Tables and owner.** " + "; ".join(parts) + " (Ownership Map v1).")
    else:
        lines.append("**Tables and owner.** No table in the service schemas; the objects are platform, template or deployment artefacts.")
    lines.append("")
    byclass = {"H": [], "C": [], "I": [], "X": []}
    for s in sts:
        for x in s["deps"]:
            if x["on"] not in byclass[x["class"]]:
                byclass[x["class"]].append(x["on"])
    pats = ", ".join(LEGACY[key]["patterns"]) or "none"
    dep = "**Dependencies.** Patterns: {}.".format(pats)
    for c, lbl in (("H", "Build (H)"), ("C", "Contract (C)"), ("I", "Integration (I)"), ("X", "External (X)")):
        ids = sorted(byclass[c])
        dep += " {}: {}.".format(lbl, ", ".join("`" + i + "`" for i in ids) if ids else "none")
    lines.append(dep)
    lines.append("")
    lines.append("**What moves.** " + NOTES[key])
    return "\n".join(lines) + "\n"

# ---------------------------------------------------------------- front matter

def lane_summary(lanes):
    groups = {}
    for l in lanes:
        if l.startswith("CG-"):
            key = l
        else:
            key = l[:l.rfind("-")] if l.count("-") > 1 else l
        groups.setdefault(key, []).append(l)
    parts = []
    for key in sorted(groups):
        n = len(groups[key])
        if n == 1 and key == groups[key][0]:
            parts.append("1 (`{}`)".format(key))
        else:
            parts.append("{}{} (`{}-*`)".format("" if n else "", n, key))
    return ", ".join(parts)


svc_rows = []
for code in [c for c in SVC]:
    sts = [s for k in STORIES for s in STORIES[k] if s["service"] == SVC[code][0]]
    if not sts:
        svc_rows.append("| {} | `{}` | `{}` | {} | 0 | none | none |".format(code, SVC[code][0], SVC[code][1], WAVE[code]))
        continue
    lanes = sorted({s["lane"] for s in sts})
    day1 = sum(1 for s in sts if s["ready"] == "Day 1")
    svc_rows.append("| {} | `{}` | `{}` | {} | {} | {} {}: {} | {} |".format(
        code, SVC[code][0], SVC[code][1], WAVE[code], len(sts), len(lanes), "lane" if len(lanes) == 1 else "lanes",
        lane_summary(lanes), day1))

map_rows = []
for key in keys:
    sts = STORIES.get(key, [])
    title = next(s for s in sections if s.startswith("## " + key + " ")).split("\n", 1)[0][len("## " + key + " "):]
    if not sts:
        map_rows.append("| `{}` | {} | {} | none | none | none | none |".format(
            key, esc(title), LEGACY.get(key, {}).get("disposition", "Retired (D-RCV-60)")))
        continue
    by = {}
    for s in sorted(sts, key=lambda x: x["id"]):
        by.setdefault(s["service"], []).append(s["id"])
    stories_cell = "; ".join("{} `{}`".format(k, "`, `".join(v)) for k, v in by.items())
    lanes = sorted({s["lane"] for s in sts})
    later = [s for s in sts if s["ready"] != "Day 1"]
    ready = "Day 1 for {} of {}".format(len(sts) - len(later), len(sts))
    if later:
        ready += "; " + "; ".join("`{}` {}".format(s["id"], s["ready"].replace("After ", "after "))
                                  for s in later)
    map_rows.append("| `{}` | {} | {} | {} | {} | {} | {} |".format(
        key, esc(title), LEGACY[key]["disposition"], LEGACY[key]["primary"], stories_cell, ", ".join(lanes), ready))

n_legacy = len(keys)
n_stories = sum(len(v) for v in STORIES.values())

front = []
front.append("SCB Collections and Recovery. Henka Group, 22 November 2026.")
front.append("(C) Siam Commercial Bank and Henka Pte Ltd")
front.append("")
front.append("# Recovery Workbench build notes, Epic 1")
front.append("")
front.append("### Change log")
front.append("")
front.append("| Version | Date | Change | Tool |")
front.append("|---|---|---|---|")
front.append("| v7 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |")
front.append("")
front.append("The change-log row is v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. "
             "Version 6 of these notes is dated 16 November 2026. Version 7 keeps its 72 story notes word for word and adds "
             "a service-and-lane note, a table-and-owner note and a dependency note to each one.")
front.append("")
front.append("> **D-RCV-60.** This version applies decision D-RCV-60. The Workbench runs as 19 services inside ACE, each with its own "
             "schema `rwb_<name>`, one login of its own, REST base `/api/recovery/<name>/v1`, Kafka topic `rwb.<name>.events.v1`, "
             "Temporal task queue `rwb-<name>` in namespace `rwb-recovery`, and the service epic `RWB-SVC-<code>`. Only "
             "rwb-source-data reads the 30 `recovery.v_ace_*` views; every other service asks it through its contract. The rule "
             "registry moves to rwb-decision and each owning service evaluates locally with the embedded Drools kit. Temporal "
             "Schedules replace Quartz in the owning service, and the data lake is removed. Epic 1 work already built or in build "
             "is not changed until its delta story is picked up (Template and Rules \u00a7R6).")
front.append("")
front.append("> **D-RCV-36.** This version applies decision D-RCV-36. Temporal runs the case lifecycle from Epic 3, with case data in the ACE database, and Drools evaluates rules from versioned rule packages. RWB-E1-029, RWB-TE-005 and RWB-E1-048 are retired; their work moved to RWB-E1-073 and RWB-E2-041. The new configuration notes RWB-E1-070 to RWB-E1-073 sit before RWB-E1-018 in the build order.")
front.append("")
front.append("These notes follow the 72 stories of Recovery Workbench User Stories Epic 1 v9. Version 4 walked every flow step, and most of those steps were load or job steps. The ACE re-base of 15 November 2026 (D-RCV-35, ADR-010) removed that estate: the Workbench takes no inbound source data, ACE ingests every source, and the recovery module reads ACE only through the 30 SELECT-only `recovery.v_ace_*` views. In this version each story carries four notes in place of the old steps, and a new configuration story adds its build order and main risk.")
front.append("")
front.append("| Note | What it answers |")
front.append("|---|---|")
front.append("| View | Which views or Workbench tables the story reads, and what it takes from each |")
front.append("| Grant | Which role holds which privilege, and what the story may not do |")
front.append("| Freshness | Which data product the read belongs to, how its business date and stamp are set, and what a stale product does |")
front.append("| Boundary | Where the module boundary falls and which rule fails the build when a class crosses it |")
front.append("| Service and lane | Which services own the story, which new story IDs carry it, which lane each one sits in, and when it is ready to start (D-RCV-60) |")
front.append("| Tables and owner | Which service owns each table the note names, and in which schema (Ownership Map v1) |")
front.append("| Dependencies | The decoupling patterns applied and the H, C, I and X dependencies of each new story (D-RCV-60) |")
front.append("")
front.append("The story remains the specification. Where these notes and the story differ, the story governs. Section 13 of each story is its solution plan and section 16 its tests; where version 4 described a Workbench step that the re-base did not change, that section still carries it, and where it described a load or a job, the four notes replace it. RWB-E1-069 owns the view list, the grants and the view conformance test. RWB-ACE-001 owns the 14 Tier 2 tables and the 12 columns that Section B needs, and nothing in the Workbench creates or alters them.")
front.append("")
front.append("## Epic 1 and the 19 services")
front.append("")
front.append("Thirteen of the 19 services take Epic 1 stories; S1 rwb-valuation, S2 rwb-treatment, S3 rwb-guarantee, "
             "S4 rwb-litigation, S6 rwb-debtsale and S7 rwb-writeoff have none. The 298 Epic 1 stories are 212 service "
             "stories, 52 integration stories and 34 platform stories. Nine of the thirteen are wave 1 services; P8 rwb-payment, "
             "S5 rwb-asset, S8 rwb-deviation and S9 rwb-partner take their Epic 1 stories in wave 1 by the W-MAP rule, ahead of "
             "their own Arch v5 wave (CG-BN1-18 to CG-BN1-21).")
front.append("")
front.append("| Code | Service | Schema | Arch v5 wave | Epic 1 stories | Epic 1 lanes | Day-1 stories |")
front.append("|---|---|---|---|---|---|---|")
front.extend(svc_rows)
front.append("")
front.append("The platform stories of Epic 1 sit in wave 0 lanes (`CG-W0` and `L-PLT-*`) with the business epic EP01 as their tag, "
             "which is how a wave 1 business story gets platform work on Day 1 (Template and Rules \u00a7R5.7).")
front.append("")
front.append("Every team type has Day-1 work in Epic 1, as \u00a7R5.7 rule 6 requires. The counts below are the Epic 1 stories whose "
             "ready-to-start value is Day 1, by suggested owner.")
front.append("")
team_counts = {}
for k in STORIES:
    for s in STORIES[k]:
        if s["ready"] != "Day 1":
            continue
        for team in ("TechX", "ACE team", "SCB IT infrastructure", "DevOps team", "QA team"):
            if team in (s["owner"] or ""):
                team_counts.setdefault(team, []).append(s["id"])
front.append("| Team type | Day-1 Epic 1 stories | Example stories |")
front.append("|---|---|---|")
for team in ("TechX", "ACE team", "SCB IT infrastructure", "DevOps team", "QA team"):
    ids = sorted(team_counts.get(team, []))
    front.append("| {} | {} | {} |".format(team, len(ids), ", ".join("`" + i + "`" for i in ids[:3]) if ids else "none"))
front.append("")
front.append("## The 30 views and their sources")
front.append("")
front.append("The 16 Section A views ship in V0002 and read the 21 ACE tables that exist today. The 14 Section B views ship in V0003 and read the tables that RWB-ACE-001 adds. Together they hold 304 columns, each with a dictionary row in the 122-object, 1,366-field dictionary of V0001.")
front.append("")
front.append("Under D-RCV-60 the views stay with P1 rwb-source-data and no other service names them (DP-05; Arch v5 slide 45: only rwb-source-data reads the 30 `recovery.v_ace_*` views). Every other service reaches ACE data through P1's REST contract (`GET /customers/{id}`, `/accounts/{id}`, `/collateral/{id}`, `/payments?accountId=`, `/freshness`) or a P1 Temporal activity (`listEligibleAccounts`, `snapshot(page)`), and listens to `AceDataReady` and `AceDataLate`.")
front.append("")
front.append("| View | ACE source | Fields | Section | Read by (D-RCV-60) |")
front.append("|---|---|---:|---|---|")
for line in head.splitlines():
    m = re.match(r"^\| `(v_ace_[a-z_]+)` \| (.+?) \| (\d+) \| ([AB]) \|$", line)
    if m:
        front.append("| `{}` | {} | {} | {} | P1 `rwb_source_data` only |".format(*m.groups()))
front.append("")
front.append("## The grants")
front.append("")
front.append("Two database roles carry the read path. Their names are fixed in the Environment and Deployment Design, and no story invents a third.")
front.append("")
front.append("| Role | Holds | On what | Set by |")
front.append("|---|---|---|---|")
front.append("| `ace_view_owner` | USAGE and SELECT | The 21 Section A tables and the 14 Section B tables in `public`; owner of the 30 views | V0002 and V0003 (RWB-E1-069), with the SELECT on the Tier 2 tables granted to it by RWB-ACE-001 |")
front.append("| `recovery_svc` | USAGE on `recovery` and SELECT on each view | The 30 views only; no privilege of any kind in `public` | V0002 for Section A, V0003 for Section B |")
front.append("| `recovery_svc` | DML on the Workbench tables | The 92 tables of schema `recovery` | V0001 (RWB-E1-001) |")
front.append("| `PUBLIC` | Nothing | Nothing | `REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC` in V0002 |")
front.append("")
front.append("No view takes an INSERT, UPDATE, DELETE or TRUNCATE. A story that changes a Workbench decision writes its own table; a story that appears to change an ACE record writes an extension table keyed by the ACE business key.")
front.append("")
front.append("**D-RCV-60.** `recovery_svc` is the login of the as-built monolith and it ends at cutover (ADR-014). DP-02 gives every "
             "service one login of its own with DML in its own schema only and no privilege of any kind in another schema; the login "
             "names are set by the ACE DB stories of RWB-PLT-DB and are not fixed in the source documents (CG-BN1-2; ASM-BN1-2). "
             "`ace_view_owner` and the 30 views stay with P1 (CG-BN1-3).")
front.append("")
front.append("| Code | Service | Its own schema | Holds there | Holds elsewhere |")
front.append("|---|---|---|---|---|")
for code, (name, schema) in SVC.items():
    holds = "DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09)"
    elsewhere = "SELECT on the 30 `recovery.v_ace_*` views" if code == "P1" else "Nothing"
    front.append("| {} | `{}` | `{}` | {} | {} |".format(code, name, schema, holds, elsewhere))
front.append("")
front.append("## Freshness")
front.append("")
front.append("A product is fresh when ACE reports its batch for the business date COMPLETE. RWB-E1-015 writes one `data_product_load` row per product per business date from `v_ace_batch_status`, and the `ace_batch_run` record that RWB-ACE-001 adds carries the business date, the status and the record count. A read that finds no COMPLETE batch keeps the last good business date, marks the product stale and raises MSG-P1-001. The Workbench products (DP03, DP04, DP08, DP09, DP10, DP12 and DP14) are stamped from their own last committed write, because no ACE batch produces them.")
front.append("")
front.append("| Product | Data | Cycle | Expected by | Owning service (D-RCV-60) |")
front.append("|---|---|---|---|---|")
for line in head.splitlines():
    if re.match(r"^\| DP\d\d \|", line):
        front.append(line + " Not specified in the source documents (CG-BN1-1; ASM-BN1-1) |")
front.append("")
front.append("**D-RCV-60.** The freshness stamp stays with P1 rwb-source-data, which publishes it through `GET /freshness` and the "
             "`AceDataReady` and `AceDataLate` events (Arch v5 slide 15). A service reads the business date from that contract and "
             "raises its own stale flag; no service writes `data_product_load`, and no service reads `v_ace_batch_status` itself. "
             "Which service owns each of the 14 products is not fixed in the source documents (CG-BN1-1; ASM-BN1-1).")
front.append("")
front.append("## The boundary")
front.append("")
front.append("The boundary has four parts, and each one fails loudly.")
front.append("")
front.append("- **No copy.** The recovery schema holds no ACE source table. The 88 Workbench tables hold Workbench records; the four extension tables hold a Workbench decision about an ACE record; the 30 views are the only read of ACE data.")
front.append("- **No constraint into `public`.** No foreign key, check or unique constraint in `recovery` names a table or type outside it, because ACE cascades deletes on `account`. A link is a varchar(255) business key with no foreign key.")
front.append("- **No direct read.** Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table. The allowed objects are the 30 view names in `recovery-modules.yaml`, not a literal list in the test.")
front.append("- **No write to a view.** `recovery_svc` holds SELECT only; the view conformance test of RWB-E1-069 fails if it finds a write privilege or a privilege in `public`.")
front.append("")
front.append("**D-RCV-60.** The boundary is applied per service. No service schema holds an ACE source table and no constraint names "
             "another schema or a `public` type; a cross-service link is an ID in a varchar(255) column, and a cross-service read is a "
             "contract call (ADR-014, ADR-020). BND-6 runs in each service's build against the same `recovery-modules.yaml`, and only "
             "P1 may name a `recovery.v_ace_*` view. The four extension tables and the 30 views stay with P1.")
front.append("")
front.append("## What this version removes from version 4")
front.append("")
front.append("| Removed | Why | Where it went |")
front.append("|---|---|---|")
for line in head.splitlines():
    if re.match(r"^\| RWB-E1-0", line):
        front.append(line)
front.append("")
front.append("D-RCV-36 also retires RWB-E1-029, RWB-TE-005 and RWB-E1-048. Their notes are removed and the work is carried by RWB-E1-073 and RWB-E2-041. The job steps that remain are Workbench jobs: allocation, rebalancing, the letter and notice runs, OCR and the agent runs. Every one of them reads its source through a view and writes only a Workbench table. The pipeline steps that remain are migrations, the dictionary conformance test, the view conformance test, the boundary test and the PDPA lint.")
front.append("")
front.append("## What D-RCV-60 retires, preserves and keeps in Epic 1")
front.append("")
front.append("| Group | Stories | Rule in this version |")
front.append("|---|---|---|")
front.append("| Built or in build, preserved | RWB-TE-001, TE-002, TE-003, E1-042, E1-043, E1-044 | The as-built story keeps its base ID with `preserved=true`; the microservice change is a separate delta story (`-2` copy, or a CON or OPS story). No change to built code until a delta story is picked up. |")
front.append("| Must change | RWB-E1-001 | The single recovery schema is kept as built; the split into `rwb_*` schemas is new work (RWB-PLT-NF06-DB and the per-service DB stories). |")
front.append("| Retired | RWB-E1-014 (no data lake, DP-17); RWB-TE-007 (Quartz replaced by Temporal Schedules, DP-10) | No new story. Dependencies on E1-014 are dropped; dependencies on TE-007 point to RWB-PLT-E1071-CON. |")
front.append("| Already cancelled | E1-003, 004, 005, 006, 009, 010, 012, 029, 048, 051; TE-005 | No new story. |")
front.append("| No impact | E1-024, 025, 026, 033, 034, 038, 040, 041, 045, 053, 060, 061, 068; TE-010, TE-012 | Moved to their epic with content unchanged. |")
front.append("")
front.append("## The 72 story notes, by legacy key")
front.append("")
front.append("One row per source note. The new stories, the lane and the ready-to-start position come from the Service Story Catalog "
             "v1 and the split plan. The release of every story of these 72 notes is 30 November 2026 (tentative); the two "
             "non-functional integration stories RWB-ITG-TE009-ITG and RWB-ITG-TE010-ITG are dated 31 December 2026 (tentative) "
             "and are not sections of these notes. The platform stories sit in wave 0.")
front.append("")
front.append("| Legacy key | Story note | Disposition | Primary | New stories | Lane(s) | Ready to start |")
front.append("|---|---|---|---|---|---|---|")
front.extend(map_rows)
front.append("")
front.append("## The 72 story notes, with their service-and-lane note")
front.append("")
front.append("Each section below reproduces the version 6 note word for word and then states what the realignment changes.")
front.append("")

body = []
for s in sections:
    key = re.match(r"## (\S+)", s).group(1)
    body.append(s.rstrip("\n"))
    body.append("")
    body.append(block(key).rstrip("\n"))
    body.append("")

text = "\n".join(front) + "\n" + "\n".join(body)
OUT.write_bytes(text.encode("utf-8"))
print("wrote", OUT)
print("bytes", len(text.encode("utf-8")), "lines", text.count("\n"))
print("sections", len(keys), "stories", n_stories)
