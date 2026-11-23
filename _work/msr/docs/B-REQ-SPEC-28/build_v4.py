"""Build Recovery Workbench Non Functional Specification v4 (D-RCV-60) from the v3 text extract.

Every source section, requirement ID, number and date is kept. The only changes are additive:
an owning service cell per table row (Microservice Ownership Map v1), the one-hop REST and 2 s
call timeout of Architecture v5 in section 3.2 with NFR-079 and NFR-080, short realignment notes,
two rows in section 4, and a new section 6 that records the change, the targets, the per-service
requirement index, the gaps and the assumptions.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "_work/msr/extract/Recovery Workbench Non Functional Specification v3.md"
OUT = ROOT / "_work/msr/docs/B-REQ-SPEC-28/Recovery Workbench Non Functional Specification v4.md"

OWN_COL = "Owning service (Ownership Map v1)"

REQ_OWNER = {
    "NFR-001": "P3 rwb-case (recovery_case, case_account)",
    "NFR-002": "PLT (gateway-bff session store); P4 rwb-access",
    "NFR-003": "S9 rwb-partner (partner, partner_user)",
    "NFR-004": "P5 rwb-document (document_intake)",
    "NFR-005": "S2 rwb-treatment (treatment)",
    "NFR-006": "S2 rwb-treatment (treatment)",
    "NFR-007": "P7 rwb-decision (decision_log_entry)",
    "NFR-069": "P5 rwb-document (document, document_custody)",
    "NFR-070": "P1 rwb-source-data (interaction)",
    "NFR-008": "PLT (gateway-bff composition); the owner of each call",
    "NFR-009": "P3 rwb-case; P5 rwb-document",
    "NFR-010": "P10 rwb-agent (agent_run, AgentRunWorkflow)",
    "NFR-011": "P7 rwb-decision (rule_package); each service's embedded Drools kit (DP-04)",
    "NFR-012": "P3 rwb-case; P5 rwb-document",
    "NFR-013": "P1 rwb-source-data (data_product, data_product_load)",
    "NFR-014": "P1 rwb-source-data (data_product_load)",
    "NFR-015": "P1 rwb-source-data",
    "NFR-016": "P5 rwb-document (document_intake, DocumentIntakeWorkflow)",
    "NFR-017": "P5 rwb-document; P10 rwb-agent (classification)",
    "NFR-018": "P1 rwb-source-data (reconciliation_result, JOB-04); P3 rwb-case (case list API)",
    "NFR-019": "P3 rwb-case (JOB-06 Schedule rebalancing)",
    "NFR-020": "PLT (platform); all 19 services",
    "NFR-021": "P2 rwb-integration (file windows); P6 rwb-comms",
    "NFR-022": "All 19 services (value not set; CG-B-REQ-SPEC-28-1; ASM-B-REQ-SPEC-28-2)",
    "NFR-023": "All 19 services (value not set; CG-B-REQ-SPEC-28-2; ASM-B-REQ-SPEC-28-3)",
    "NFR-024": "P10 rwb-agent",
    "NFR-025": "P2 rwb-integration (outbound_item)",
    "NFR-026": "P2 rwb-integration (outbound_item); PLT (outbox, inbox and .dlt)",
    "NFR-027": "PLT (service template and deployment)",
    "NFR-071": "P5 rwb-document (document, document_custody); PLT (Blob storage)",
    "NFR-028": "P5 rwb-document (document_type, retention_rule)",
    "NFR-029": "P5 rwb-document (Blob WORM)",
    "NFR-030": "P7 rwb-decision (decision_log_entry)",
    "NFR-031": "P3 rwb-case (recovery_case)",
    "NFR-032": "Not specified in the source documents (CG-B-REQ-SPEC-28-6; ASM-B-REQ-SPEC-28-7)",
    "NFR-072": "P3 rwb-case (POST /cases/{caseId}/legal-hold); P5 rwb-document",
    "NFR-073": "P5 rwb-document; P3 rwb-case",
    "NFR-074": "P5 rwb-document (retention_action)",
    "NFR-075": "P1 rwb-source-data (interaction)",
    "NFR-033": "P7 rwb-decision (decision_log_entry)",
    "NFR-034": "P7 rwb-decision (approval, rule_package_version)",
    "NFR-035": "P7 rwb-decision",
    "NFR-036": "P7 rwb-decision; P5 rwb-document",
    "NFR-037": "P3 rwb-case; S7 rwb-writeoff",
    "NFR-038": "P6 rwb-comms (notice)",
    "NFR-076": "P5 rwb-document (document, document_custody)",
    "NFR-077": "P1 rwb-source-data (interaction)",
    "NFR-078": "P10 rwb-agent (agent_run); P7 rwb-decision",
    "NFR-039": "P4 rwb-access (masking_rule); P1 rwb-source-data (party_ext)",
    "NFR-040": "P4 rwb-access; P10 rwb-agent",
    "NFR-041": "S6 rwb-debtsale (debt_sale_account, data room)",
    "NFR-042": "P1 rwb-source-data (data_product_access); P5 rwb-document; P7 rwb-decision",
    "NFR-043": "P1 rwb-source-data (party_ext); P5 rwb-document",
    "NFR-044": "P6 rwb-comms (notice)",
    "NFR-045": "PLT (platform environments)",
    "NFR-046": "PLT (platform, SCB Azure tenancy)",
    "NFR-047": "P1 rwb-source-data (data_product); P5 rwb-document (document_type)",
    "NFR-048": "P10 rwb-agent (private endpoint)",
    "NFR-049": "P4 rwb-access; PLT (ACE Common sign-in)",
    "NFR-050": "S9 rwb-partner; P4 rwb-access",
    "NFR-051": "P4 rwb-access",
    "NFR-052": "PLT (key store)",
    "NFR-053": "PLT (platform)",
    "NFR-054": "PLT (build pipeline)",
    "NFR-055": "P10 rwb-agent (agent_policy, guardrails)",
    "NFR-056": "PLT (platform); SCB IT security",
    "NFR-057": "P5 rwb-document (document_text)",
    "NFR-058": "P6 rwb-comms (template, merge_field)",
    "NFR-059": "PLT (gateway-bff screens)",
    "NFR-060": "PLT (gateway-bff screens)",
    "NFR-061": "PLT (gateway-bff screens)",
    "NFR-062": "PLT (gateway-bff screens)",
    "NFR-063": "S9 rwb-partner; PLT (partner gateway)",
    "NFR-064": "PLT (observability); all 19 services",
    "NFR-065": "P7 rwb-decision; P9 rwb-reporting (measure_definition)",
    "NFR-066": "P10 rwb-agent (agent_evaluation, agent_run); P9 rwb-reporting",
    "NFR-067": "PLT (observability); the owner of each job",
    "NFR-068": "PLT (observability)",
    "NFR-079": "PLT (service template and gateway-bff)",
    "NFR-080": "PLT (gateway-bff)",
}

AREA_OWNER = {
    "Volume": "P3 rwb-case (case store); P1 rwb-source-data (ACE accounts)",
    "Users": "P4 rwb-access; PLT (gateway-bff session store)",
    "Screens": "PLT (gateway-bff composition); the owner of each call",
    "Agents": "P10 rwb-agent",
    "Freshness": "P1 rwb-source-data (data_product_load)",
    "Availability": "PLT (platform); all 19 services",
    "Storage": "P5 rwb-document; P7 rwb-decision; P1 rwb-source-data",
    "Audit": "P7 rwb-decision (decision_log_entry)",
    "Security": "P4 rwb-access; PLT (platform)",
    "Partners": "S9 rwb-partner; PLT (partner gateway)",
}

MEASURE_OWNER = {
    "Accounts at 90 days past due, active inventory": "P1 rwb-source-data (30 recovery.v_ace_* views)",
    "New accounts at 90 days past due a month": "P1 rwb-source-data",
    "Open cases at go-live": "P3 rwb-case",
    "Open cases at the end of 2027": "P3 rwb-case",
    "Named users": "P4 rwb-access",
    "Online in the busiest hour": "PLT (gateway-bff session store)",
    "Requests a second in the busiest hour": "PLT (gateway-bff)",
    "Documents held at the end of 2031": "P5 rwb-document",
    "Hire purchase accounts outside the active inventory": "P1 rwb-source-data (v_ace_account view)",
}

HEADER = [
    "SCB Collections and Recovery. Henka Group, 22 November 2026.",
    "(C) Siam Commercial Bank and Henka Pte Ltd",
]

CONTROL = f"""| Item | Detail |
|---|---|
| Document | Recovery Workbench non-functional specification |
| Version | 4 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC 25010 quality characteristics |
| Requirements | 80 (78 in version 3, plus NFR-079 and NFR-080) |
| Decision | D-RCV-60 microservice realignment, on the Architecture v5 target; ADR-019, ADR-020 |
| Owner of record | Microservice Ownership Map v1; the owning service in every table below is taken from it |
| Status | Draft (no approval recorded; ASM-B-REQ-SPEC-28-1) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### Change log

| Version | Date | Change |
|---|---|---|
| 4 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

Version 4 keeps every section, requirement ID, number and date of version 3. What is new is listed in section 6.1;
the short note under each affected section gives the reason in place."""

NOTE_1 = """Realignment (D-RCV-60). The owning service cell is new: it names the service that owns the object a target measures,
taken from the Microservice Ownership Map v1 (Tables, Endpoints, Events, Workflows and activities, and Jobs sheets), with PLT
for the platform items the map leaves to the platform (gateway-bff, the key store, observability, the build pipeline). Every
source target, status and decision cell is unchanged, and a target whose owner the map does not name carries the section R9
placeholder."""

NOTE_2 = """Realignment (D-RCV-60). The concurrency figures do not agree across the sources: this table has about 410 users online in
the busiest hour, NFR-002 and NFR-003 give about 370 staff and about 50 partners, and Architecture v5 slide 48 gives 414
concurrent staff and 48 concurrent partners. Every number is kept as written; the difference is recorded as
CG-B-REQ-SPEC-28-5 with ASM-B-REQ-SPEC-28-6, which reads 414 staff and 48 partners as the load-test figures."""

NOTE_32 = """Realignment (D-RCV-60). REST is one hop from gateway-bff to the owning service, and a composite screen is composed from
parallel one-hop calls, never a call chain: gateway and session 0.15 s, the slowest parallel call 0.6 s and the merge 0.3 s
come to about 1.05 s, planned at about 1.2 s, against the 2 s target at the 95th percentile (Architecture v5 slides 10 and 11;
DP-11; ADR-020). Every REST call carries a 2 s timeout, a single GET retry with jitter, and a circuit breaker and bulkhead per
downstream (Architecture v5 slide 11). NFR-008 and NFR-009 are read against that composition, and NFR-079 and NFR-080 state
the rule as requirements."""

NOTE_33 = """Realignment (D-RCV-60). Only P1 rwb-source-data reads the 30 recovery.v_ace_* views, with its own read-only login and a
statement timeout; every other service reads ACE data through P1's published contract or its own v_ace_* view (Architecture v5
slides 9 and 11; DP-05). The view names and the batch-status row of NFR-013 and NFR-014 therefore belong to P1, and the
freshness rule, the business date and the alerts stay exactly as written."""

NOTE_34 = """Realignment (D-RCV-60). Architecture v5 splits the Workbench into 19 services and records that the recovery point and recovery
time objectives are not set (slide 48). NFR-022 and NFR-023 keep their source targets and stay Open under DL11; because the
value and the per-service tier are both missing, their owning service cell carries the section R9 placeholder and
CG-B-REQ-SPEC-28-1 and CG-B-REQ-SPEC-28-2 are raised. NFR-024 to NFR-027, NFR-071 and the two availability targets stay as
written and apply service by service."""

NOTE_35 = """Realignment (D-RCV-60). Retention periods are not set (DL26). The 28 days in the source set is the Temporal Continue-As-New
interval, at each stage end and at least every 28 days (Recovery Workbench Temporal and Drools Design Text Extract v1, slide 13),
not a retention period; any "weeks" wording used for the same period is a conflict, recorded as CG-B-REQ-SPEC-28-3 with
ASM-B-REQ-SPEC-28-4. Retention stays with P5 rwb-document (retention_rule, retention_action), the decision log with P7
rwb-decision and the interaction ledger with P1 rwb-source-data."""

NOTE_37 = """Realignment (D-RCV-60). NFR-042 names a data lake copy. Architecture v5 has no data lake: reporting is built from events into
P9 rwb-reporting (DP-17; ADR-018). The requirement text is kept as written and the contradiction is recorded as
CG-B-REQ-SPEC-28-4 with ASM-B-REQ-SPEC-28-5; the logged reads are the P1, P5 and P7 reads named in the row."""

ROUTE_ROWS = [
    "| Route in the target architecture | Staff through gateway-bff; partners through the partner gateway in the DMZ (FAPI 2.0), fronting S9 rwb-partner (Architecture v5 slides 8 and 10; ADR-019) |",
    "| Owning service (Ownership Map v1) | S9 rwb-partner for partner, partner_user, partner_instruction and results; PLT for the partner gateway (Architecture v5 slides 8 and 17) |",
]

NEW_ROWS = [
    "| NFR-079 | A REST call between services completes inside its timeout, and no call chain is deeper than one hop from gateway-bff. | 2 seconds per REST call; one hop only; GET retried once with jitter; circuit breaker and bulkhead per downstream | Solution architect | Proposed, D-RCV-60 | PLT (service template and gateway-bff) |",
    "| NFR-080 | A composite screen is composed by gateway-bff from parallel one-hop calls to the owning services, and never by one service calling another for a screen. | One hop per call; about 1.05 seconds budgeted at the 95th percentile, about 1.2 seconds planned, against the 2 second target | Solution architect | Proposed, D-RCV-60 | PLT (gateway-bff) |",
]

GAPS = [
    ("CG-B-REQ-SPEC-28-1", "Recovery point objective not stated for the 19 services", "Missing", "P1",
     "IT lead with Operational Risk"),
    ("CG-B-REQ-SPEC-28-2", "Recovery time objective not stated for the 19 services", "Missing", "P1",
     "IT lead with Operational Risk"),
    ("CG-B-REQ-SPEC-28-3", "'Weeks' versus '28 days' wording for the same period", "Conflict", "P2", "Business analyst"),
    ("CG-B-REQ-SPEC-28-4", "NFR-042 logs reads of a data lake copy that Architecture v5 removes", "Conflict", "P3",
     "Solution architect"),
    ("CG-B-REQ-SPEC-28-5", "Concurrency and named-user figures disagree between section 2, NFR-002/NFR-003 and Architecture v5",
     "Conflict", "P2", "Business lead"),
    ("CG-B-REQ-SPEC-28-6", "Owning service not derivable from the Ownership Map for NFR-032", "Missing", "P3",
     "Solution architect"),
]

ASMS = [
    ("ASM-B-REQ-SPEC-28-1", "The specification is issued as Draft version 4. No review or approval of any version is recorded, "
     "and this run takes no human approval step.", "High"),
    ("ASM-B-REQ-SPEC-28-2", "Until the recovery point objective is confirmed, no RPO value is tested; NFR-022 stays Open under DL11 "
     "and recovery testing uses the ACE platform tier.", "Low"),
    ("ASM-B-REQ-SPEC-28-3", "Until the recovery time objective is confirmed, no RTO value is tested; NFR-023 stays Open under DL11 "
     "and recovery testing uses the ACE platform tier.", "Low"),
    ("ASM-B-REQ-SPEC-28-4", "The 28 days is read only as the Temporal Continue-As-New interval; no retention period is 28 days and "
     "every retention period stays Not set under DL26.", "Medium"),
    ("ASM-B-REQ-SPEC-28-5", "The data lake copy named by NFR-042 is read as removed (DP-17, ADR-018); the logged reads are the P1, P5 "
     "and P7 reads, and no lake copy is built.", "Medium"),
    ("ASM-B-REQ-SPEC-28-6", "Where the concurrency figures differ, Architecture v5 slide 48 (414 staff, 48 partners) is used for the "
     "load test; the requirement text stays as written.", "Medium"),
    ("ASM-B-REQ-SPEC-28-7", "The archive location of NFR-032 is recorded per file in the Cutover and Go Live Plan; no single service "
     "owns it until that plan names one.", "Medium"),
    ("ASM-B-REQ-SPEC-28-8", "Every date of the source is copied unchanged and every release date named anywhere is tentative; this "
     "document names no release date of its own.", "High"),
    ("ASM-B-REQ-SPEC-28-9", "The version 4 change is additive: an owning service cell per row, the section notes, NFR-079 and "
     "NFR-080, two section 4 rows and section 6. PLT is used for the items the Ownership Map leaves to the platform, and no "
     "source cell is rewritten.", "High"),
]


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def row(cs):
    return "| " + " | ".join(cs) + " |"


def with_owner(block, first_cell_map, extra_rows=()):
    head = cells(block[0])
    out_rows = [row(head + [OWN_COL])]
    for line in block[1:]:
        cs = cells(line)
        if all(set(c) <= set("-: ") for c in cs):
            out_rows.append("|" + "---|" * (len(cs) + 1))
            continue
        key = cs[0]
        if key not in first_cell_map:
            raise SystemExit(f"no owner for {key!r} in table {head}")
        out_rows.append(row(cs + [first_cell_map[key]]))
    out_rows.extend(extra_rows)
    return out_rows


def req_first_cell(cs):
    return cs[0]


def transform(block):
    head = tuple(cells(block[0]))
    if head == ("Item", "Detail"):
        return CONTROL.splitlines()
    if head == ("Area", "Main target", "Status"):
        extra = ["| Calls | REST is one hop from gateway-bff to the owning service, with a 2 s call timeout, a single GET retry with jitter and a circuit breaker and bulkhead per downstream | Proposed, D-RCV-60 | PLT (gateway-bff); all 19 services |"]
        return with_owner(block, AREA_OWNER, extra)
    if head == ("Measure", "Value", "Basis"):
        return with_owner(block, MEASURE_OWNER)
    if head == ("ID", "Requirement", "Target", "Owner", "Status"):
        ids = {cells(l)[0] for l in block if l.startswith("| NFR-")}
        extra = ()
        if "NFR-011" in ids:
            extra = tuple(NEW_ROWS)
        return with_owner(block, REQ_OWNER, extra)
    if head == ("ID", "Requirement", "Owner", "Decision"):
        return with_owner(block, REQ_OWNER)
    if head == ("Item", "Requirement"):
        return block + ROUTE_ROWS
    return block


SERVICE_NAMES = [
    ("P1", "rwb-source-data"), ("P2", "rwb-integration"), ("P3", "rwb-case"), ("P4", "rwb-access"),
    ("P5", "rwb-document"), ("P6", "rwb-comms"), ("P7", "rwb-decision"), ("P8", "rwb-payment"),
    ("P9", "rwb-reporting"), ("P10", "rwb-agent"), ("S1", "rwb-valuation"), ("S2", "rwb-treatment"),
    ("S3", "rwb-guarantee"), ("S4", "rwb-litigation"), ("S5", "rwb-asset"), ("S6", "rwb-debtsale"),
    ("S7", "rwb-writeoff"), ("S8", "rwb-deviation"), ("S9", "rwb-partner"), ("PLT", "platform"),
]


def main():
    src = SRC.read_text(encoding="utf-8").splitlines()
    out, i, seen_titles = [], 0, 0
    while i < len(src):
        line = src[i]
        if not line.strip():
            out.append("")
            i += 1
            continue
        if line.startswith("|"):
            block = []
            while i < len(src) and src[i].startswith("|"):
                block.append(src[i])
                i += 1
            out.extend(transform(block))
            if tuple(cells(block[0])) == ("Measure", "Value", "Basis"):
                out.extend(["", NOTE_2])
            continue
        txt = line
        if txt == "Recovery Workbench" and seen_titles == 0:
            txt, seen_titles = "# Recovery Workbench", 1
        elif txt == "Non-functional specification":
            txt = "## Non-functional specification"
        out.append(txt)
        if txt.startswith("Each requirement has a measure"):
            out.extend(["", NOTE_1])
        for anchor, note in (
            ("ISO/IEC 25010: Performance efficiency: time behavior.", NOTE_32),
            ("ISO/IEC 25010: Performance efficiency and reliability.", NOTE_33),
            ("ISO/IEC 25010: Reliability: availability and recoverability.", NOTE_34),
            ("ISO/IEC 25010: Security: accountability; compliance.", NOTE_35),
            ("ISO/IEC 25010: Security: confidentiality. Tested by: Role-based tests", NOTE_37),
        ):
            if txt.startswith(anchor):
                out.extend(["", note])
        i += 1

    # requirement order and per-service index
    req_order = [r for r in REQ_OWNER]
    by_service = []
    for code, name in SERVICE_NAMES:
        pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(code) + r"(?![0-9])")
        ids = [rid for rid in req_order if pat.search(REQ_OWNER[rid])]
        by_service.append((code, name, ids))

    s6 = ["", "# 6. Realignment record (D-RCV-60)", "",
          "## 6.1 What version 4 changes", "",
          "Version 4 keeps every section, requirement ID, number and date of version 3. The changes are these, and nothing else.", "",
          "- An owning service cell is added to every target and requirement table, from the Microservice Ownership Map v1; no source cell is rewritten (ASM-B-REQ-SPEC-28-9).",
          "- Section 3.2 states the one-hop REST rule and the 2 s call timeout of Architecture v5, and NFR-079 and NFR-080 are added (78 requirements in version 3, 80 here).",
          "- Section 3.3 states that only P1 rwb-source-data reads the 30 recovery.v_ace_* views.",
          "- Section 3.4 records that the recovery point and recovery time objectives are not stated for the 19 services (CG-B-REQ-SPEC-28-1 and CG-B-REQ-SPEC-28-2).",
          "- Section 3.5 records the 'weeks' versus '28 days' wording (CG-B-REQ-SPEC-28-3).",
          "- Section 3.7 records the data lake copy named by NFR-042 against Architecture v5 (CG-B-REQ-SPEC-28-4).",
          "- Section 2 keeps the concurrency figures and records their difference from Architecture v5 slide 48 (CG-B-REQ-SPEC-28-5).",
          "- Section 4 records the partner gateway of ADR-019 and the owning service.",
          "- No release date is named by this document; the version 3 date of 15 November 2026 is kept, and every release date named elsewhere in the programme stays tentative (U7; DL48; ASM-B-REQ-SPEC-28-8).",
          "",
          "## 6.2 The realigned targets", "",
          "| Item | Value | Source |",
          "|---|---|---|",
          "| REST hop | One hop from gateway-bff to the owning service, and no call chain deeper than one in any service | Recovery Workbench Architecture v5 Text Extract v1, slide 11 |",
          "| REST call timeout | 2 s per call; GET retried once with jitter; circuit breaker and bulkhead per downstream; RFC 9457 problem details | Architecture v5, slide 11; ADR-020 |",
          "| Composite screen budget | Gateway and session 0.15 s, slowest parallel call 0.6 s, merge 0.3 s: about 1.05 s, planned at about 1.2 s, against the 2 s target at the 95th percentile | Architecture v5, slide 10; NFR-008, NFR-009 |",
          "| ACE data reads | Only P1 rwb-source-data reads the 30 recovery.v_ace_* views, with a read-only login and a statement timeout; every other service reads P1's contract | Architecture v5, slides 9 and 11; DP-05 |",
          "| Agent fallback | 60 s, then the rule result and the case still routes | Architecture v5, slide 16; NFR-010, NFR-024 |",
          "| Partner route | Partner gateway (FAPI 2.0) in the DMZ, fronting S9 rwb-partner; staff through gateway-bff | Architecture v5, slide 8; ADR-019 |",
          "| Decisions | D-RCV-60; ADR-013 to ADR-023; DL44 to DL49 | ids.json; Template and Rules R8.4 |",
          "| Story coverage | RWB-PLT-NF01-OPS, RWB-PLT-NF02-APP, RWB-PLT-NF03-OPS, RWB-PLT-NF04-OPS, RWB-PLT-NF05-OPS, RWB-PLT-NF06-DB, RWB-PLT-NF07-INF and RWB-PLT-NF08-INF carry the non-functional work in wave 0 | split plan, legacy rows NF-01 to NF-08 |",
          "",
          "## 6.3 Requirements by owning service", "",
          "Built from the owning service cell of every requirement table, in the order of this document.", "",
          "| Service | Requirements |", "|---|---|"]
    for code, name, ids in by_service:
        s6.append(f"| {code} {name} | {', '.join(ids) if ids else 'None'} |")
    s6 += ["", "## 6.4 Gap rows raised by this version", "",
           "| ID | Title | Type | Severity | Owner role |", "|---|---|---|---|---|"]
    s6 += [f"| {g[0]} | {g[1]} | {g[2]} | {g[3]} | {g[4]} |" for g in GAPS]
    s6 += ["", "Numbering is left to step D1 (Template and Rules R9); the ids here are the work-package ids.", "",
           "## 6.5 Assumption rows raised by this version", "",
           "| ID | Assumption | Confidence |", "|---|---|---|"]
    s6 += [f"| {a[0]} | {a[1]} | {a[2]} |" for a in ASMS]
    s6 += ["", "## 6.6 Sources read for version 4", "",
           "| Source | Used for |", "|---|---|",
           "| 03 Requirements and specifications/Recovery Workbench Non Functional Specification v3.docx (and its text extract) | Every section, requirement and number kept |",
           "| 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (slides 8 to 11, 16, 48) | One-hop REST, the 2 s timeout, the screen budget, the ACE read rule, RPO and RTO, the partner gateway |",
           "| 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md (slide 13) | The 28 days Continue-As-New interval |",
           "| 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx and _work/msr/plan/ownership.json | The owning service of every requirement |",
           "| 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (R1, R3, R5, R8, R9) | Header, change log, DP table, gaps and assumptions |",
           "| _work/msr/plan/ids.json and _work/msr/plan/split_plan.json (stats and legacy) | Decision ids and the NF-01 to NF-08 story coverage |", ""]

    text = "\n".join(HEADER + [""] + out + s6).rstrip() + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        raise SystemExit(f"REFUSED: {OUT} exists")
    OUT.write_text(text, encoding="utf-8")
    print("WROTE", OUT.relative_to(ROOT))
    print("requirements:", len(REQ_OWNER))


if __name__ == "__main__":
    sys.exit(main())
