# -*- coding: utf-8 -*-
"""Rebuild the Epic 1 grooming order against the current 72-story set (v9)."""
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties

SRC = r"04 User stories\Recovery Workbench User Stories Epic 1 v9.xlsx"
OUT = r"Recovery_Workbench_Epic1_Grooming_Order_All_TE_v3.xlsx"

# ---------------------------------------------------------------- source data
wb_src = openpyxl.load_workbook(SRC, data_only=True)
ws_src = wb_src["Stories"]
meta = {}
for r in range(5, ws_src.max_row + 1):
    key = ws_src.cell(r, 1).value
    if not key:
        continue
    meta[key] = {
        "module": ws_src.cell(r, 3).value or "",
        "title": ws_src.cell(r, 4).value or "",
        "priority": ws_src.cell(r, 7).value or "",
        "deps_raw": ws_src.cell(r, 8).value or "",
    }
    meta[key]["deps"] = [
        d
        for d in re.findall(r"RWB-[A-Z0-9]+-\d+", str(meta[key]["deps_raw"]))
        if d.startswith("RWB-E1") or d.startswith("RWB-TE")
    ]

# ---------------------------------------------------------------- sessions
# (number, name, track, day, focus, participants, stories in grooming order)
SESSIONS = [
    (1, "Engineering Architecture & Delivery Guardrails", 1, 1,
     "Module boundaries, code ownership, API contract tests and PDPA lint",
     "Tech Leads, Solution Architect, Dev, QA, Security/Privacy",
     ["RWB-TE-001", "RWB-TE-002", "RWB-TE-003", "RWB-TE-011"]),
    (2, "Platform Foundation: Migrations, Configuration & Reference Data", 1, 1,
     "Migration versioning, parameter catalog, versioned reference data and multi-product parameters",
     "BA/PO, Solution Architect, Dev, DBA, QA",
     ["RWB-E1-044", "RWB-E1-042", "RWB-E1-043", "RWB-E1-045"]),
    (3, "Data Foundation, ACE Boundary & Environment", 1, 2,
     "Recovery schema, read-only ACE views and grants, data dictionary, sandbox and masked data",
     "Data Architect, DBA, BA, Dev, QA, Security",
     ["RWB-E1-001", "RWB-E1-069", "RWB-E1-064", "RWB-E1-065", "RWB-TE-004", "RWB-E1-047"]),
    (4, "Freshness, Outbound Integration & Run Books", 1, 2,
     "Freshness stamps, outbound adapters, run books and monitoring",
     "Integration Architect, Data Engineer, BA, DevOps, Ops",
     ["RWB-E1-015", "RWB-E1-007", "RWB-E1-056"]),
    (5, "Decision Log, Rules & Audit", 1, 3,
     "Append-only decision log, writer contract, Drools runtime and rule authoring",
     "BA/PO, Solution Architect, P7/P4 Dev, Audit/Risk, QA",
     ["RWB-E1-008", "RWB-E1-027", "RWB-E1-072", "RWB-E1-073"]),
    (6, "Identity, Roles & Access Administration", 1, 3,
     "Sign-on, role matrix, PDPA masking, delegation limits, access control and break-glass",
     "Security Architect, IAM, BA, P4 Dev, QA",
     ["RWB-E1-038", "RWB-E1-019", "RWB-E1-022", "RWB-E1-037", "RWB-E1-016", "RWB-E1-039"]),
    (7, "Case Creation, Assignment, SLA & Measures", 1, 4,
     "Case ID, allocation, transfer, SLA and timers, rebalancing and baseline measures",
     "Business SME, BA, Workflow Dev, Scheduler Owner, QA",
     ["RWB-E1-018", "RWB-E1-020", "RWB-E1-028", "RWB-E1-021", "RWB-E1-030", "RWB-E1-013"]),
    (8, "Workflow, Scheduling & Reliability Platform", 1, 5,
     "Outbox and retry, Quartz jobs, hash-chain check, Temporal platform and worker",
     "Solution Architect, DevOps, Integration, Ops, Performance QA",
     ["RWB-TE-006", "RWB-TE-007", "RWB-TE-008", "RWB-E1-070", "RWB-E1-071"]),
    (9, "Document Foundation & Storage", 2, 1,
     "Document types, store and index, storage containers",
     "Document SME, BA, P5 Dev, Security, QA",
     ["RWB-TE-012", "RWB-E1-025", "RWB-E1-024"]),
    (10, "Interaction Ledger", 2, 1,
     "Interaction capture, Workbench events and case-history reads",
     "Business SME, BA, Interaction Dev, QA",
     ["RWB-E1-066", "RWB-E1-067", "RWB-E1-068"]),
    (11, "Case List, Queue Views & Case Record", 2, 4,
     "Case list, queue and owner filters, read-only record, record v1.1",
     "Business SME, UX, BA, Frontend/Backend Dev, QA",
     ["RWB-E1-002", "RWB-E1-031", "RWB-E1-023", "RWB-E1-035"]),
    (12, "Reconciliation, Retention & Decision-Log Copy", 2, 3,
     "Reconciliation report, retention and archive, decision-log copy",
     "Data Owner, Data Engineer, BA, QA, Reporting",
     ["RWB-E1-011", "RWB-E1-017", "RWB-E1-014"]),
    (13, "Document Intake, OCR & Classification", 2, 2,
     "OCR pipeline, classification, field extraction, auto-attach and search",
     "Document SME, OCR/AI, Integration, P5 Dev, QA",
     ["RWB-E1-049", "RWB-E1-050", "RWB-E1-053", "RWB-E1-032", "RWB-E1-033"]),
    (14, "Document Review, Protection & Attachment", 2, 4,
     "Retention and virus scan, intake channels, attach screen, review queue and checklists",
     "Document SME, BA, P5 Dev, Security, QA",
     ["RWB-E1-041", "RWB-E1-057", "RWB-E1-026", "RWB-E1-054", "RWB-E1-040"]),
    (15, "Correspondence, Templates & Notices", 2, 5,
     "Merge fields, letter templates, notice generation and proof of delivery",
     "Business SME, WIN Integration, BA, P6 Dev, QA",
     ["RWB-E1-046", "RWB-E1-034", "RWB-E1-052", "RWB-E1-055"]),
    (16, "AI / Agent Foundation", 2, 5,
     "Agent platform, runtime client, shadow agents, evaluation and monitoring",
     "AI Architect, Data Scientist, BA, Dev, Model Risk, QA",
     ["RWB-E1-058", "RWB-TE-013", "RWB-E1-059", "RWB-E1-060", "RWB-E1-062", "RWB-E1-061", "RWB-E1-063"]),
]

DAYS = {
    1: "Mon, 16 Nov 2026",
    2: "Tue, 17 Nov 2026",
    3: "Wed, 18 Nov 2026",
    4: "Thu, 19 Nov 2026",
    5: "Fri, 20 Nov 2026",
}
DAY_LABEL = {
    1: "Day 1 — Monday, 16 Nov 2026",
    2: "Day 2 — Tuesday, 17 Nov 2026",
    3: "Day 3 — Wednesday, 18 Nov 2026",
    4: "Day 4 — Thursday, 19 Nov 2026",
    5: "Day 5 — Friday, 20 Nov 2026 (Target Completion)",
}

TRACK_NAME = {1: "Group 1 — Platform & Case Engine", 2: "Group 2 — Experience, Content & Intelligence"}
LAYER = {1: "1 – Foundation", 2: "1 – Foundation", 3: "1 – Foundation",
         4: "2 – Platform Services", 5: "2 – Platform Services", 6: "2 – Platform Services",
         7: "3 – Case Engine", 8: "3 – Case Engine",
         9: "4 – Experience & Content", 10: "4 – Experience & Content",
         11: "4 – Experience & Content", 12: "4 – Experience & Content",
         13: "4 – Experience & Content", 14: "4 – Experience & Content",
         15: "4 – Experience & Content",
         16: "5 – AI & Agents"}

# ---------------------------------------------------------------- status, remarks, notes
STATUS = {
    "RWB-E1-001": "Groomed", "RWB-E1-064": "Groomed", "RWB-E1-065": "Groomed",
    "RWB-TE-004": "Groomed",
    "RWB-E1-007": "Partially Groomed",
    "RWB-E1-042": "Partially Groomed", "RWB-E1-043": "Partially Groomed",
    "RWB-E1-044": "Partially Groomed",
}
REMARKS = {
    "RWB-E1-001": "Groomed before v9; re-check E1-069 linkage",
    "RWB-E1-064": "Groomed before v9",
    "RWB-E1-065": "Groomed before v9",
    "RWB-TE-004": "Groomed before v9",
    "RWB-E1-007": "Outbound-only scope under D-RCV-35",
    "RWB-E1-042": "In Sprint 1",
    "RWB-E1-043": "In Sprint 1",
    "RWB-E1-044": "In Sprint 1",
    "RWB-E1-069": "New in v9 (D-RCV-35)",
    "RWB-E1-070": "New in v9 (D-RCV-36)",
    "RWB-E1-071": "New in v9 (D-RCV-36)",
    "RWB-E1-072": "New in v9 (D-RCV-36)",
    "RWB-E1-073": "New in v9; replaces E1-029 and TE-005 (D-RCV-36)",
    "RWB-E1-037": "Retitled in v9: role matrix + PDPA masking",
    "RWB-E1-038": "Retitled in v9: delegation of authority table",
}
NOTES = {
    "RWB-TE-001": "Confirm package boundary rule and the build gate owner.",
    "RWB-TE-002": "Name the code owners for each recovery package.",
    "RWB-TE-003": "Confirm the API spec version used for generated types.",
    "RWB-TE-011": "Confirm PDPA rules for test data, prompts and logs.",
    "RWB-E1-044": "No prerequisites. Confirm schema-name parameter convention and migration ownership.",
    "RWB-E1-042": "Carry over Sprint 1 clarifications: catalog scope and approval route.",
    "RWB-E1-043": "Carry over Sprint 1 clarifications: versioned table pattern and cache refresh.",
    "RWB-E1-045": "Confirm the three product parameter sets and effective dating.",
    "RWB-E1-001": "Previously groomed. Re-check only the E1-069 ACE boundary linkage.",
    "RWB-E1-069": "ACE dependency RWB-ACE-001; 14 Section B views (DL43); SELECT-only grants and build-time boundary rule.",
    "RWB-E1-064": "Re-check the dictionary against the 14 ACE views.",
    "RWB-E1-065": "Confirm synthetic data volume and refresh.",
    "RWB-TE-004": "Confirm masking rules for SIT and UAT.",
    "RWB-E1-047": "Confirm the flag removal date and release owner.",
    "RWB-E1-015": "Daily freshness gate moves here from retired E1-006. Confirm the threshold per data product.",
    "RWB-E1-007": "Scope is outbound-only under D-RCV-35; inbound load content is retired.",
    "RWB-E1-056": "Run books cover every Epic 1 job; confirm monitoring ownership with Ops.",
    "RWB-E1-008": "Append-only, hash-chained store; confirm retention and tamper evidence.",
    "RWB-E1-027": "Writer contract, idempotency and rule/package version capture.",
    "RWB-E1-072": "Embedded Drools; package store; one RuleEvaluator for every engine.",
    "RWB-E1-073": "XLS decision-table template, scenarios, SoD approval, effective date and one-call rollback.",
    "RWB-E1-038": "Confirm delegation limits by product and the approval route.",
    "RWB-E1-019": "Confirm the seed set of roles, teams and queues and their ownership.",
    "RWB-E1-022": "Confirm Entra groups, MFA route and the break-glass path.",
    "RWB-E1-037": "Confirm the role-to-permission matrix and the PDPA masking matrix with Privacy.",
    "RWB-E1-016": "Access control per data product and catalog entry; depends on the role matrix.",
    "RWB-E1-039": "Confirm who can break glass and how the access log is audited.",
    "RWB-E1-018": "Now also depends on the Drools runtime and authoring stories (072, 073).",
    "RWB-E1-020": "Confirm allocation rules, queue capacity and rebalancing inputs.",
    "RWB-E1-028": "Timer lifecycle, warnings, escalation and prescription dates.",
    "RWB-E1-021": "Confirm transfer rules and authority limits.",
    "RWB-E1-030": "Confirm daily rebalancing rules and queue measure definitions.",
    "RWB-E1-013": "Confirm reporting cut, data source and baseline period.",
    "RWB-TE-006": "Outbox, retry, idempotency and replay.",
    "RWB-TE-007": "Quartz scheduling, concurrency and recovery; now also depends on E1-028.",
    "RWB-TE-008": "Confirm hash-chain check frequency and alerting.",
    "RWB-E1-070": "Temporal cluster per environment on ACE AKS; persistence DBs, namespace, mTLS and Entra SSO.",
    "RWB-E1-071": "Spring Boot worker, task-queue and workflow-ID conventions, PDPA codec and smoke workflow.",
    "RWB-TE-012": "Storage containers, access boundaries and environment configuration.",
    "RWB-E1-025": "Confirm the six document types and their fields.",
    "RWB-E1-024": "Store and index; confirm the case-record and decision-log hooks.",
    "RWB-E1-066": "Confirm the interaction event schema.",
    "RWB-E1-067": "Confirm the full list of Workbench actions to capture.",
    "RWB-E1-068": "Confirm the read interface and history view.",
    "RWB-E1-002": "Confirm columns, default sort and queue/owner display.",
    "RWB-E1-031": "Confirm the queue model and filter set.",
    "RWB-E1-023": "Confirm fields shown and role-based masking.",
    "RWB-E1-035": "Confirm documents and history timeline on the record.",
    "RWB-E1-011": "Confirm reconciliation thresholds, recipients and failure route.",
    "RWB-E1-017": "Confirm retention classes with Records Management.",
    "RWB-E1-014": "Confirm the data-lake watermark and failure handling.",
    "RWB-E1-049": "Confirm OCR engine, volume and throughput.",
    "RWB-E1-050": "Confirm document classes and confidence bands.",
    "RWB-E1-053": "Confirm the fields extracted for each of the six types.",
    "RWB-E1-032": "Confirm auto-attach rules and the fallback path.",
    "RWB-E1-033": "Search across cases; depends on the document index and extraction.",
    "RWB-E1-041": "Confirm retention classes and the virus-scan service.",
    "RWB-E1-057": "Confirm intake channels, SLAs and ownership.",
    "RWB-E1-026": "Confirm the attach and search screen with UX.",
    "RWB-E1-054": "Confirm the low-confidence threshold and review ownership.",
    "RWB-E1-040": "Confirm the checklist per case type.",
    "RWB-E1-046": "Confirm merge fields and the template catalog owner.",
    "RWB-E1-034": "Confirm template lifecycle and approval.",
    "RWB-E1-052": "Confirm notice templates, triggers and delivery evidence.",
    "RWB-E1-055": "Confirm the WIN interface and proof-of-delivery capture.",
    "RWB-E1-058": "Confirm model providers, PDPA controls and the shadow-mode exit criteria.",
    "RWB-TE-013": "Timeouts, fallback, idempotency and decision-log linkage.",
    "RWB-E1-059": "Confirm the shadow population and evaluation measures.",
    "RWB-E1-060": "Confirm the extraction evaluation set.",
    "RWB-E1-061": "Confirm the L1 proposal format and reviewer.",
    "RWB-E1-062": "Confirm deviation rules and the shadow population.",
    "RWB-E1-063": "Confirm dashboard measures, thresholds and alerting.",
}

# ---------------------------------------------------------------- derived helpers
key_session = {}
key_index = {}
for num, name, track, day, focus, participants, stories in SESSIONS:
    for i, k in enumerate(stories):
        key_session[k] = num
        key_index[k] = i

SESSION = {num: dict(num=num, name=name, track=track, day=day, focus=focus,
                     participants=participants, stories=stories)
           for num, name, track, day, focus, participants, stories in SESSIONS}

missing_keys = [k for k in meta if k not in key_session]
extra_keys = [k for k in key_session if k not in meta]
dupes = [k for k, n in __import__("collections").Counter(key_session.keys()).items() if n > 1]
assert not missing_keys, missing_keys
assert not extra_keys, extra_keys
assert not dupes, dupes
assert len(key_session) == 72, len(key_session)

# dependency edges that stay inside Epic 1
edges = [(k, d) for k in meta for d in meta[k]["deps"] if d in meta]

# Track independence: Group 1 must not depend on Group 2
group2_to_group1 = []
group1_to_group2 = []
for consumer, prereq in edges:
    ct, pt = SESSION[key_session[consumer]]["track"], SESSION[key_session[prereq]]["track"]
    if ct == 2 and pt == 1:
        group2_to_group1.append((consumer, prereq))
    if ct == 1 and pt == 2:
        group1_to_group2.append((consumer, prereq))
assert not group1_to_group2, group1_to_group2

blocks = {k: [] for k in meta}
for k, d in edges:
    blocks[d].append(k)
for k in blocks:
    blocks[k].sort(key=lambda x: (key_session[x], key_index[x]))

def dep_sort(k):
    return SESSION[key_session[k]]["day"], SESSION[key_session[k]]["track"], key_session[k], key_index[k]

# overall order: capability session, then position in session
ordered = sorted(meta, key=lambda k: (key_session[k], key_index[k]))
overall = {k: i + 1 for i, k in enumerate(ordered)}

def dep_text(k):
    ds = meta[k]["deps"]
    if not ds:
        return "No prerequisites"
    txt = ", ".join(ds)
    if k == "RWB-E1-069":
        txt += "  |  External: RWB-ACE-001 (14 Section B views, DL43)"
    return txt

def blocks_text(k):
    bs = blocks[k]
    if not bs:
        return "—"
    return ", ".join(bs)

def item_type(k):
    return "Technical Enabler" if k.startswith("RWB-TE") else "Business Story"

def dependency_note(k):
    """What the facilitator must confirm, using grooming day as the clock."""
    later = []
    same = []
    for d in meta[k]["deps"]:
        if d not in meta:
            continue
        sd, dd = SESSION[key_session[k]], SESSION[key_session[d]]
        if dd["day"] > sd["day"]:
            later.append(f"{d} (D{dd['day']})")
        elif dd["day"] == sd["day"] and dd["num"] != sd["num"]:
            same.append(f"{d} (S{dd['num']})")
    if later:
        head = ", ".join(later[:2])
        if len(later) > 2:
            head += f" +{len(later) - 2}"
        return "Confirm later: " + head
    if same:
        head = ", ".join(same[:2])
        if len(same) > 2:
            head += f" +{len(same) - 2}"
        return "Same-day link: " + head
    return "Prereqs cleared"

# ---------------------------------------------------------------- styling
PURPLE = "4B1F6F"
LAVENDER = "EDE2F5"
ROW_ALT = "F7F4FA"
CREAM = "FFF1D6"
WHITE = "FFFFFF"
INK = "251A2D"
GRID = "D9D2E9"
GROUP1_FILL = "E8F0FE"
GROUP2_FILL = "E6F4EA"
G1_HEAD = "1F4E79"
G2_HEAD = "1E6B52"

TITLE_FONT = Font(name="Carlito", size=18, bold=True, color=WHITE)
SUB_FONT = Font(name="Carlito", size=11, color=INK)
HEAD_FONT = Font(name="Aptos", size=10, bold=True, color=WHITE)
BODY_FONT = Font(name="Aptos", size=9, color=INK)
BODY_BOLD = Font(name="Aptos", size=9, bold=True, color=INK)
SMALL_FONT = Font(name="Aptos", size=8, color="5A5163")

thin = Side(style="thin", color=GRID)
BORDER = Border(bottom=thin)

def fill(color):
    return PatternFill("solid", fgColor=color)

def put(ws, row, col, value, font=BODY_FONT, bg=None, align=None, border=True):
    c = ws.cell(row=row, column=col, value=value)
    c.font = font
    if bg:
        c.fill = fill(bg)
    c.alignment = align or Alignment(vertical="top", wrap_text=True)
    if border:
        c.border = BORDER
    return c

def band(ws, row, first, last, value, font, bg):
    ws.merge_cells(start_row=row, start_column=first, end_row=row, end_column=last)
    for c in range(first, last + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = fill(bg)
        cell.border = Border()
    cell = ws.cell(row=row, column=first, value=value)
    cell.font = font
    cell.alignment = Alignment(horizontal="left", vertical="center")

def est_height(values, widths, minimum=30):
    lines = 1
    for v, w in zip(values, widths):
        if not v:
            continue
        txt = str(v)
        chars = max(8, int(w * 1.15))
        n = sum(max(1, -(-len(part) // chars)) for part in txt.split("\n"))
        lines = max(lines, n)
    return max(minimum, 13.2 * lines + 6)

# ---------------------------------------------------------------- workbook
wb = openpyxl.Workbook()

# =================================================================== SHEET 1
ws = wb.active
ws.title = "Epic 1 Grooming Plan"
ws.sheet_properties.tabColor = PURPLE

cols = [
    ("Overall Order", 8),
    ("Session", 9),
    ("Grooming Group", 32),
    ("Order in Session", 10),
    ("Story Key", 15),
    ("Title", 44),
    ("Item Type", 15),
    ("Primary Grooming Focus", 40),
    ("Grooming Status", 14),
    ("Remarks", 24),
    ("Owner", 12),
    ("Target Date", 14),
    ("Notes / Open Clarifications", 44),
    ("Planned Grooming Date", 17),
    ("Track (Group 1 / 2)", 14),
    ("Dependency Layer", 21),
    ("Depends on (Prerequisites)", 52),
    ("Blocks (Downstream)", 52),
]
widths = [w for _, w in cols]
for i, (_, w) in enumerate(cols, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w

band(ws, 1, 1, 18, "Recovery Workbench Epic 1 — Grooming Order v3", TITLE_FONT, PURPLE)
ws.row_dimensions[1].height = 28
band(ws, 2, 1, 18,
     "72 current stories, 16 capability sessions, two parallel tracks. Group 1 has no dependency on Group 2. Window: 16–20 Nov 2026.",
     SUB_FONT, LAVENDER)
ws.row_dimensions[2].height = 22

HEAD_ROW = 4
for i, (name, _) in enumerate(cols, start=1):
    c = ws.cell(HEAD_ROW, i, name)
    c.font = HEAD_FONT
    c.fill = fill(PURPLE)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = Border()
ws.row_dimensions[HEAD_ROW].height = 46

row = HEAD_ROW + 1
for k in ordered:
    s = SESSION[key_session[k]]
    bg = WHITE if row % 2 == 0 else ROW_ALT
    values = [
        overall[k], s["num"], s["name"], key_index[k] + 1, k, meta[k]["title"],
        item_type(k), s["focus"], STATUS.get(k, "Not Started"), REMARKS.get(k, ""),
        None, None, NOTES.get(k, ""), DAYS[s["day"]],
        f"Group {s['track']}", LAYER[s["num"]], dep_text(k), blocks_text(k),
    ]
    for i, v in enumerate(values, start=1):
        align = Alignment(vertical="top", wrap_text=True)
        if i in (1, 2, 4, 9, 12, 15):
            align = Alignment(horizontal="center", vertical="top", wrap_text=True)
        cell = put(ws, row, i, v, BODY_FONT, bg, align)
        if i == 5:
            cell.fill = fill(CREAM)
            cell.font = BODY_BOLD
        if i == 9:
            cell.font = BODY_BOLD
        if i == 15:
            cell.fill = fill(GROUP1_FILL if s["track"] == 1 else GROUP2_FILL)

    ws.row_dimensions[row].height = est_height(
        [meta[k]["title"], s["focus"], NOTES.get(k, ""), dep_text(k), blocks_text(k)],
        [widths[5], widths[7], widths[12], widths[16], widths[17]],
    )
    row += 1

last_data_row = row - 1
ws.freeze_panes = "F5"
ws.auto_filter.ref = f"A4:R{last_data_row}"

# totals
band(ws, row + 1, 1, 18,
     f"72 stories  •  Group 1: 38  •  Group 2: 34  •  Sessions: 16  •  Groomed: 4  •  Partially groomed: 4  •  Not started: 64",
     Font(name="Aptos", size=9, bold=True, color=INK), LAVENDER)
ws.row_dimensions[row + 1].height = 20

dv_status = DataValidation(type="list", formula1='"Not Started,Partially Groomed,Ready for Grooming,Groomed,Blocked"', allow_blank=True)
ws.add_data_validation(dv_status)
dv_status.add(f"I5:I{last_data_row}")
dv_track = DataValidation(type="list", formula1='"Group 1,Group 2"', allow_blank=True)
ws.add_data_validation(dv_track)
dv_track.add(f"O5:O{last_data_row}")

# =================================================================== SHEET 2
ws2 = wb.create_sheet("Parallel Schedule (Group 1 & 2)")
ws2.sheet_properties.tabColor = G1_HEAD

w2 = [5, 15, 44, 38, 34, 3, 5, 15, 44, 38, 34]
for i, w in enumerate(w2, start=1):
    ws2.column_dimensions[get_column_letter(i)].width = w

band(ws2, 1, 1, 11, "Epic 1 Parallel Grooming Schedule — Group 1 & Group 2", TITLE_FONT, PURPLE)
ws2.row_dimensions[1].height = 28
band(ws2, 2, 1, 11,
     "Two parallel grooming rooms. Group 1 is upstream and never waits on Group 2. Group 2 references Group 1 decisions; those references are on the Cross-Track References sheet. A later prerequisite is a design reference, not a blocker.",
     SUB_FONT, LAVENDER)
ws2.row_dimensions[2].height = 40

r = 4
for day in range(1, 6):
    g1 = [k for k in ordered if SESSION[key_session[k]]["day"] == day and SESSION[key_session[k]]["track"] == 1]
    g2 = [k for k in ordered if SESSION[key_session[k]]["day"] == day and SESSION[key_session[k]]["track"] == 2]

    band(ws2, r, 1, 11, f"{DAY_LABEL[day]}      •      Group 1: {len(g1)} items      •      Group 2: {len(g2)} items      •      Total: {len(g1) + len(g2)}",
         Font(name="Carlito", size=12, bold=True, color=WHITE), PURPLE)
    ws2.row_dimensions[r].height = 24
    r += 1

    band(ws2, r, 1, 5, f"GROUP 1 (Track 1 — upstream) — {len(g1)} stories", Font(name="Aptos", size=9, bold=True, color=WHITE), G1_HEAD)
    band(ws2, r, 7, 11, f"GROUP 2 (Track 2 — downstream) — {len(g2)} stories", Font(name="Aptos", size=9, bold=True, color=WHITE), G2_HEAD)
    ws2.row_dimensions[r].height = 19
    r += 1

    heads = ["#", "Story Key", "Title", "Session", "Dependency note"]
    for i, h in enumerate(heads, start=1):
        c = ws2.cell(r, i, h)
        c.font = HEAD_FONT
        c.fill = fill(G1_HEAD)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for i, h in enumerate(heads, start=7):
        c = ws2.cell(r, i, h)
        c.font = HEAD_FONT
        c.fill = fill(G2_HEAD)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws2.row_dimensions[r].height = 24
    r += 1

    height = max(len(g1), len(g2))
    for i in range(height):
        values1 = None
        if i < len(g1):
            k = g1[i]
            values1 = [i + 1, k, meta[k]["title"], f"S{SESSION[key_session[k]]['num']}: {SESSION[key_session[k]]['name']}", dependency_note(k)]
        values2 = None
        if i < len(g2):
            k = g2[i]
            values2 = [i + 1, k, meta[k]["title"], f"S{SESSION[key_session[k]]['num']}: {SESSION[key_session[k]]['name']}", dependency_note(k)]

        bg = WHITE if i % 2 == 0 else ROW_ALT
        for j in range(5):
            v = values1[j] if values1 else None
            align = Alignment(horizontal="center", vertical="top", wrap_text=True) if j == 0 else Alignment(vertical="top", wrap_text=True)
            cell = put(ws2, r, j + 1, v, BODY_FONT, bg, align)
            if j == 1 and v:
                cell.fill = fill(CREAM)
                cell.font = BODY_BOLD
        for j in range(5):
            v = values2[j] if values2 else None
            align = Alignment(horizontal="center", vertical="top", wrap_text=True) if j == 0 else Alignment(vertical="top", wrap_text=True)
            cell = put(ws2, r, j + 7, v, BODY_FONT, bg, align)
            if j == 1 and v:
                cell.fill = fill(CREAM)
                cell.font = BODY_BOLD
        ws2.row_dimensions[r].height = est_height(
            [values1[2] if values1 else "", values2[2] if values2 else "",
             values1[4] if values1 else "", values2[4] if values2 else ""],
            [44, 44, 38, 38], minimum=26)
        r += 1
    r += 1
    if day in (2, 4):
        from openpyxl.worksheet.pagebreak import Break
        ws2.row_breaks.append(Break(id=r - 1))


ws2.freeze_panes = "A4"

# =================================================================== SHEET 3
ws3 = wb.create_sheet("Cross-Track References")
ws3.sheet_properties.tabColor = G2_HEAD
w3 = [6, 15, 40, 26, 8, 34, 30, 10, 30]
for i, w in enumerate(w3, start=1):
    ws3.column_dimensions[get_column_letter(i)].width = w

band(ws3, 1, 1, 9, "Group 2 → Group 1 Dependency References", TITLE_FONT, PURPLE)
ws3.row_dimensions[1].height = 28
band(ws3, 2, 1, 9,
     f"{len({c for c, p in group2_to_group1})} Group 2 stories reference {len(group2_to_group1)} Group 1 decisions. There are ZERO Group 1 → Group 2 references, so Group 1 never waits on Group 2.",
     SUB_FONT, LAVENDER)
ws3.row_dimensions[2].height = 32

h3 = ["#", "Group 2 Story", "Title", "Group 2 Session", "Day", "Group 1 Prerequisites", "Group 1 Session(s)", "Latest Day", "Handling"]
for i, h in enumerate(h3, start=1):
    c = ws3.cell(4, i, h)
    c.font = HEAD_FONT
    c.fill = fill(PURPLE)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws3.row_dimensions[4].height = 30

by_story = {}
for consumer, prereq in group2_to_group1:
    by_story.setdefault(consumer, []).append(prereq)

rows3 = sorted(by_story, key=lambda k: (SESSION[key_session[k]]["day"], key_session[k], key_index[k]))
r = 5
for n, k in enumerate(rows3, start=1):
    s = SESSION[key_session[k]]
    prereqs = sorted(by_story[k], key=lambda x: (SESSION[key_session[x]]["day"], key_session[x], key_index[x]))
    max_day = max(SESSION[key_session[p]]["day"] for p in prereqs)
    sessions_txt = ", ".join(sorted({f"S{SESSION[key_session[p]]['num']}" for p in prereqs},
                                    key=lambda x: int(x[1:])))
    if max_day < s["day"]:
        handling = f"Group 1 input on Day {max_day} — before this session"
    elif max_day == s["day"]:
        handling = "Same day — confirm at session start"
    else:
        handling = "Later Group 1 input — design reference only"
    bg = WHITE if r % 2 else ROW_ALT
    vals = [n, k, meta[k]["title"], f"S{s['num']}: {s['name']}", s["day"],
            ", ".join(prereqs), sessions_txt, f"Day {max_day}", handling]
    for i, v in enumerate(vals, start=1):
        align = Alignment(horizontal="center", vertical="top", wrap_text=True) if i in (1, 5, 8) else Alignment(vertical="top", wrap_text=True)
        cell = put(ws3, r, i, v, BODY_FONT, bg, align)
        if i == 2:
            cell.fill = fill(CREAM)
            cell.font = BODY_BOLD
    ws3.row_dimensions[r].height = est_height(
        [meta[k]["title"], ", ".join(prereqs), f"S{s['num']}: {s['name']}"],
        [40, 34, 26], minimum=30)
    r += 1

band(ws3, r + 1, 1, 9,
     "All links are one-way. No Group 1 story lists a Group 2 story as a prerequisite. That is the independence guarantee for Track 1.",
     Font(name="Aptos", size=9, bold=True, color=INK), LAVENDER)
ws3.row_dimensions[r + 1].height = 22
ws3.freeze_panes = "C5"

# =================================================================== SHEET 4
ws4 = wb.create_sheet("Session Summary")
ws4.sheet_properties.tabColor = "8A5A00"
w4 = [10, 38, 12, 8, 46, 42, 17, 28]
for i, w in enumerate(w4, start=1):
    ws4.column_dimensions[get_column_letter(i)].width = w

band(ws4, 1, 1, 8, "Epic 1 Grooming Session Summary", TITLE_FONT, PURPLE)
ws4.row_dimensions[1].height = 28
band(ws4, 2, 1, 8, "16 capability sessions across two tracks; 72 stories; 16–20 Nov 2026.",
     SUB_FONT, LAVENDER)
ws4.row_dimensions[2].height = 20

h4 = ["Session", "Grooming Group", "Track", "Items", "Primary Grooming Focus", "Recommended Participants", "Planned Date", "Dependency Position"]
for i, h in enumerate(h4, start=1):
    c = ws4.cell(4, i, h)
    c.font = HEAD_FONT
    c.fill = fill(PURPLE)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws4.row_dimensions[4].height = 34

r = 5
for s in SESSIONS:
    num, name, track, day, focus, participants, stories = s
    position = {
        1: "Starts the chain; no internal prerequisites",
        2: "Needs S1 (module boundary)",
        3: "Needs S2 (migrations and reference data)",
        4: "Needs S3 (data and ACE views)",
        5: "Needs S4 (run books)",
        6: "Needs S5 (decision log)",
        7: "Needs S6 (access) and S5 (rules)",
        8: "Needs S7 (SLA) and S6 (sign-on)",
        9: "Needs S1 (TE-001) for storage containers",
        10: "Needs S7 (case) and S5 (decision log)",
        11: "Needs S10 (ledger) and S7 (case record)",
        12: "Needs S11 (case list) and S9 (retention)",
        13: "Needs S9 (document store) and S2 (parameters)",
        14: "Needs S13 (OCR) and S11 (case record)",
        15: "Needs S14 (review) and S5 (decision log)",
        16: "Needs S12 (decision-log copy) and S13 (extraction)",
    }[num]
    bg = WHITE if r % 2 else ROW_ALT
    vals = [f"S{num}", name, f"Group {track}", len(stories), focus, participants, DAYS[day], position]
    for i, v in enumerate(vals, start=1):
        align = Alignment(horizontal="center", vertical="top", wrap_text=True) if i in (1, 3, 4, 7) else Alignment(vertical="top", wrap_text=True)
        cell = put(ws4, r, i, v, BODY_FONT, bg, align)
        if i == 3:
            cell.fill = fill(GROUP1_FILL if track == 1 else GROUP2_FILL)
    ws4.row_dimensions[r].height = est_height([name, focus, participants, position], [38, 46, 42, 28], minimum=38)
    r += 1

# =================================================================== SHEET 5 — DAILY WORKLOAD
ws5 = wb.create_sheet("Daily Workload")
ws5.sheet_properties.tabColor = "6B4A8A"
for i, w in enumerate([26, 14, 14, 14, 14, 14], start=1):
    ws5.column_dimensions[get_column_letter(i)].width = w

band(ws5, 1, 1, 6, "Epic 1 Daily Parallel Workload", TITLE_FONT, PURPLE)
ws5.row_dimensions[1].height = 28
band(ws5, 2, 1, 6, "Finish Fri 20 Nov 2026. Group 1 and Group 2 run in parallel each day; peak load is 16 stories on Day 5.",
     SUB_FONT, LAVENDER)
ws5.row_dimensions[2].height = 20

headers = ["Day", "Group 1", "Group 2", "Total", "Cumulative", "Cumulative %"]
for i, h in enumerate(headers, start=1):
    c = ws5.cell(4, i, h)
    c.font = HEAD_FONT
    c.fill = fill(PURPLE)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws5.row_dimensions[4].height = 28

r = 5
cum = 0
for day in range(1, 6):
    g1 = sum(1 for k in meta if SESSION[key_session[k]]["day"] == day and SESSION[key_session[k]]["track"] == 1)
    g2 = sum(1 for k in meta if SESSION[key_session[k]]["day"] == day and SESSION[key_session[k]]["track"] == 2)
    cum += g1 + g2
    vals = [DAYS[day], g1, g2, g1 + g2, cum, f"{cum / 72:.0%}"]
    for i, v in enumerate(vals, start=1):
        cell = put(ws5, r, i, v, BODY_FONT, WHITE if r % 2 else ROW_ALT,
                   Alignment(horizontal="left" if i == 1 else "center", vertical="center"))
    ws5.row_dimensions[r].height = 22
    r += 1
for i, v in enumerate(["Total", 38, 34, 72, "", "100%"], start=1):
    put(ws5, r, i, v, BODY_BOLD, LAVENDER,
        Alignment(horizontal="left" if i == 1 else "center", vertical="center"))
ws5.row_dimensions[r].height = 22

chart = BarChart()
chart.type = "col"
chart.grouping = "stacked"
chart.overlap = 100
chart.title = "Daily grooming load by track"
chart.y_axis.title = "Stories"
chart.x_axis.title = "Grooming day"
data = Reference(ws5, min_col=2, max_col=3, min_row=4, max_row=9)
cats = Reference(ws5, min_col=1, min_row=5, max_row=9)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
chart.height = 8.5
chart.width = 16
ws5.add_chart(chart, "A12")

# =================================================================== SHEET 6
ws6 = wb.create_sheet("Notes & Legend")
ws6.sheet_properties.tabColor = "6B6B6B"
w5 = [30, 26, 62, 62]
for i, w in enumerate(w5, start=1):
    ws6.column_dimensions[get_column_letter(i)].width = w

band(ws6, 1, 1, 4, "Notes & Legend", TITLE_FONT, PURPLE)
ws6.row_dimensions[1].height = 28

r = 3
def section(title):
    global r
    band(ws6, r, 1, 4, title, Font(name="Carlito", size=11, bold=True, color=WHITE), "6B4A8A")
    ws6.row_dimensions[r].height = 22
    r += 1

def table_header(headers):
    global r
    for i, h in enumerate(headers, start=1):
        c = ws6.cell(r, i, h)
        c.font = HEAD_FONT
        c.fill = fill(PURPLE)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws6.row_dimensions[r].height = 22
    r += 1

def row4(vals, bold_first=False, center_first=False):
    global r
    for i, v in enumerate(vals, start=1):
        align = Alignment(horizontal="center" if (center_first and i == 1) else "left",
                          vertical="top", wrap_text=True)
        cell = put(ws6, r, i, v, BODY_BOLD if (bold_first and i == 1) else BODY_FONT,
                   WHITE if r % 2 else ROW_ALT, align)
    ws6.row_dimensions[r].height = est_height(vals, w5, minimum=20)
    r += 1

section("1. Scope and sources")
table_header(["Item", "Value", "Detail", "Why it matters"])
row4(["Epic", "Epic 1 only", "72 stories from Recovery Workbench User Stories Epic 1 v9 (Stories sheet).", "The v9 story sheet is the single source of truth for keys, titles and prerequisites."], True)
row4(["Story set", "72 stories", "10 Technical Enablers: TE-001, 002, 003, 004, 006, 007, 008, 011, 012 and 013.", "TE-009 is Epic 2 (release 31 Dec 2026) and is out of scope. The v2 sheet listed it with no session."], True)
row4(["Retired keys", "11 removed", "E1-003, 004, 005, 006, 009, 010, 012, 029, 048, 051 and TE-005.", "D-RCV-35 (ACE ingests all source data) and D-RCV-36 (Temporal and Drools) retire these. Do not re-add them."], True)
row4(["New keys", "5 added", "E1-069 ACE views; E1-070/071 Temporal; E1-072/073 Drools.", "These form the new platform backbone and are groomed in S3, S8 and S5."], True)
row4(["Numbering gap", "E1-036", "No E1-036 row exists in v9.", "The sequence moves from E1-035 to E1-037. Nothing is missing."], True)

r += 1
section("2. Two-track design — what “no dependency” can and cannot mean")
table_header(["Measure", "Result", "What it means", "How the plan uses it"])
row4(["Stories", "72", "All Epic 1 stories in v9, each groomed once.", "72 rows on the Grooming Plan sheet."], True)
row4(["Dependency links", "194", "Story-to-story prerequisites declared in v9.", "Used to order sessions and to build the reference table."], True)
row4(["Connected components", "1", "Every story is reachable from every other story through prerequisites.", "A strict two-way zero-dependency split does not exist."], True)
row4(["Best balanced cut", "≈40 links", "Even the best 36/36 split still leaves about 40 cross-links.", "A claim of zero links in both directions would be false."], True)
row4(["Guarantee used", "0 reverse links", "Group 1 lists no Group 2 story as a prerequisite; Group 2 references Group 1 only.", "Group 1 can be groomed in complete isolation. Group 2 consumes settled Group 1 decisions."], True)
row4(["Cross-track meetings", "0", "No joint grooming session and no reciprocal handoff is scheduled.", "Replaces the 46-row sync checklist in v2 with one reference table."], True)

r += 1
section("3. Why the split is one-way, not two-way")
table_header(["Point", "Evidence", "Consequence", "If strict independence is mandatory"])
row4(["Group 1", "38 stories: guardrails, platform foundation, data/ACE, freshness and integration, decision log and rules, access, case engine, scheduling and Temporal.", "Nothing in Group 1 depends on a Group 2 story. Verified against all 194 links.", "This is the strongest available independence property."], True)
row4(["Group 2", "34 stories: document foundation and intake, interaction ledger, case list and record, reconciliation and retention, correspondence, AI agents.", "Group 2 references Group 1 decisions in 45 places. All are build-order references, not reciprocal handoffs.", "Only two honest options: duplicate foundation grooming, or run the tracks in sequence. Neither is recommended."], True)
row4(["Residual risk", "A Group 2 story groomed before its Group 1 prerequisite is visible in the Dependency note column.", "The facilitator records the open decision and confirms it when the Group 1 session closes.", "Treat the note as a design reference, not a blocker."], True)

r += 1
section("4. Dependency handling and the one cycle in v9")
table_header(["Topic", "Applies to", "Treatment", "Reason"])
row4(["Circular link", "E1-007 → E1-056 → E1-027 → E1-015 → E1-007", "Grooming order breaks the loop at E1-027 → E1-015: freshness is groomed in S4, the decision-log writer in S5.", "A cycle cannot be ordered. This is the weakest link in the loop and the logging hook is confirmed in S5."], True)
row4(["Backward references", "Group 2 stories listed on the Cross-Track References sheet", "Groom with the reference visible; confirm the prerequisite decision at the session start.", "Grooming a story before its build prerequisite is normal; the design decision still has to be recorded."], True)
row4(["Same-session links", "Within each session", "Stories are ordered so a prerequisite inside the session comes first.", "Removes avoidable within-session backtracking."], True)
row4(["External dependency", "E1-069", "RWB-ACE-001 and DL43 are outside Epic 1.", "Raise once with the ACE team; do not hold the session for it."], True)

r += 1
section("5. Status definitions")
table_header(["Status", "Meaning", "Used for", "Action"])
row4(["Groomed", "Agreed against the current story text.", "E1-001, E1-064, E1-065, TE-004", "Re-check only if a linked story changed the decision."], True)
row4(["Partially Groomed", "Discussed, but open points remain.", "E1-007, E1-042, E1-043, E1-044", "Close the listed clarifications only; do not repeat the whole story."], True)
row4(["Not Started", "No grooming record against v9.", "The other 64 stories", "Groom in the session and date shown."], True)
row4(["Ready for Grooming", "Pre-read complete, ready for the room.", "Optional", "Use when the BA has circulated the story and open points."], True)
row4(["Blocked", "Cannot proceed without an external decision.", "Optional", "Name the decision and owner in the Notes column."], True)

r += 1
section("6. What changed from v2")
table_header(["Area", "v2", "v3", "Effect"])
row4(["Story set", "79 rows, including 11 retired keys and TE-009 (Epic 2).", "72 current v9 stories, 10 Epic 1 TEs.", "The plan can be worked as written."], True)
row4(["Sessions", "16 sessions, mixed capability boundaries.", "16 capability sessions, re-cut around the new platform stories.", "Related stories are groomed together and interconnectivity is visible."], True)
row4(["Tracks", "46 cross-track sync rows; several same-day, two-way links.", "One-way split: Group 1 independent, Group 2 references Group 1.", "No joint sync meeting; one reference table instead."], True)
row4(["Dates", "Day 1 Fri 13 Nov 2026 (already past).", "Mon 16 Nov to Fri 20 Nov 2026.", "The window is actionable."], True)
row4(["Dependency view", "One combined Related Stories column.", "Split into Depends on and Blocks, plus a Dependency Layer.", "Filter and sort by upstream or downstream."], True)
row4(["TE scope", "TE-009 listed with no session.", "Removed; Epic 2 enabler.", "No orphan row."], True)

r += 1
section("7. Open points to close in the room")
table_header(["#", "Topic", "Story", "Decision needed"])
opens = [
    ("1", "ACE boundary", "E1-069", "Confirm the 14 Section B views (DL43), SELECT-only grants and the build-time rule with RWB-ACE-001."),
    ("2", "Drools package model", "E1-072 / E1-073", "Confirm the XLS decision-table template, package version fields, scenario minimum and rollback evidence."),
    ("3", "Temporal platform", "E1-070 / E1-071", "Confirm environments, persistence sizing, namespace, mTLS, task-queue and workflow-ID conventions."),
    ("4", "Decision-log cycle", "E1-015 / E1-027 / E1-056", "Confirm the freshness-to-writer link and the run-book monitoring hook in S4 and S5."),
    ("5", "Role masking matrix", "E1-037", "Confirm role-to-permission and PDPA field masking with Privacy."),
    ("6", "Retention classes", "E1-017 / E1-041", "Confirm classes, archive trigger and Records Management sign-off."),
    ("7", "OCR confidence", "E1-053 / E1-054", "Confirm extraction fields per type and the low-confidence threshold."),
    ("8", "Agent controls", "E1-058 / TE-013", "Confirm model providers, PDPA payload handling, fallback and shadow-mode exit criteria."),
    ("9", "Run-book ownership", "E1-056", "Confirm Ops ownership and the monitoring route for every Epic 1 job."),
    ("10", "Feature-flag removal", "E1-047", "Confirm the removal date and the release owner."),
]
for o in opens:
    row4(list(o), center_first=True)

r += 1
section("8. How to use the workbook")
table_header(["Sheet", "Use", "Filter / sort", "Owner"])
row4(["Epic 1 Grooming Plan", "One row per story. The working list for the week.", "Filter Grooming Track, Planned Date, Session or Grooming Status.", "BA / PO"], True)
row4(["Parallel Schedule", "The room-by-room, day-by-day running order.", "Read left to right for Group 1 and Group 2 on the same day.", "Facilitator"], True)
row4(["Cross-Track References", "The only places Group 2 needs a Group 1 decision.", "Filter by Group 2 session or latest day.", "Facilitator / architect"], True)
row4(["Session Summary", "Session scope, participants and dependency position.", "Check participants and the session-to-session flow.", "PM / BA lead"], True)
row4(["Daily Workload", "Stories per track per day, with the stacked bar chart.", "Use the chart to check the daily balance.", "PM / BA lead"], True)
row4(["Notes & Legend", "Scope, method, status definitions and open points.", "Read before the first session.", "All"], True)

# ---------------------------------------------------------------- page setup
def setup_page(ws, paper=8, fit_width=1, fit_height=0, title_rows=None):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = paper
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_setup.fitToWidth = fit_width
    ws.page_setup.fitToHeight = fit_height
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = 0.25
    ws.page_margins.right = 0.25
    ws.page_margins.top = 0.4
    ws.page_margins.bottom = 0.45
    ws.page_margins.header = 0.2
    ws.page_margins.footer = 0.2
    if title_rows:
        ws.print_title_rows = title_rows
    ws.oddFooter.center.text = "Page &P of &N"
    ws.oddFooter.center.size = 8
    ws.oddFooter.center.color = "808080"

setup_page(ws, paper=8, fit_width=2, title_rows="4:4")
setup_page(ws2, paper=8, fit_width=1, title_rows="1:2")
setup_page(ws3, paper=8, fit_width=1, fit_height=1, title_rows="1:4")
setup_page(ws4, paper=9, fit_width=1, fit_height=1)
setup_page(ws5, paper=9, fit_width=1, fit_height=1)
setup_page(ws6, paper=9, fit_width=1)

# ---------------------------------------------------------------- save
wb.save(OUT)

print("saved", OUT)
print("stories", len(ordered), "edges", len(edges))
print("Group1", sum(1 for k in meta if SESSION[key_session[k]]["track"] == 1),
      "Group2", sum(1 for k in meta if SESSION[key_session[k]]["track"] == 2))
print("group2->group1 refs", len(group2_to_group1), "stories", len({c for c, p in group2_to_group1}))
print("group1->group2 refs", len(group1_to_group2))
for day in range(1, 6):
    g1 = sum(1 for k in meta if SESSION[key_session[k]]["day"] == day and SESSION[key_session[k]]["track"] == 1)
    g2 = sum(1 for k in meta if SESSION[key_session[k]]["day"] == day and SESSION[key_session[k]]["track"] == 2)
    print("day", day, g1, g2, g1 + g2)
