"""Build Recovery Workbench Business Requirements Epic 1 v4.docx from v3.

Scope (ACE DB Alignment tracker row 8): sections 3.1, 3.2, 4 and 7 re-based on
D-RCV-35 / ADR-010; title block and document control bumped to v4. Every other
section is copied unchanged. v3 is not modified.
"""
import copy
import sys

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = ROOT + r"\03 Requirements and specifications\Recovery Workbench Business Requirements Epic 1 v3.docx"
DST = ROOT + r"\03 Requirements and specifications\Recovery Workbench Business Requirements Epic 1 v4.docx"

DATE = "15 November 2026"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

d = docx.Document(SRC)
body = d.element.body
log = []


def set_text(cell_or_par, text):
    """Replace the text of a single-paragraph cell or a paragraph, keeping the first run's format."""
    par = cell_or_par.paragraphs[0] if hasattr(cell_or_par, "paragraphs") else cell_or_par
    runs = par.runs
    if not runs:
        raise SystemExit("no run to keep formatting from")
    runs[0].text = text
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def row_by_key(table, key):
    for r in table.rows:
        if r.cells[0].text.strip() == key:
            return r
    raise SystemExit(f"row {key} not found")


def set_row(table, key, values):
    """values: list of new texts per column, None keeps the cell."""
    r = row_by_key(table, key)
    for c, v in zip(r.cells, values):
        if v is not None and c.text != v:
            set_text(c, v)
    log.append(key)


def add_row_after(table, after_key, values, template_key=None):
    """Clone a row (template_key or after_key) and insert it after after_key."""
    after = row_by_key(table, after_key)._tr
    tmpl = row_by_key(table, template_key or after_key)._tr
    new = copy.deepcopy(tmpl)
    after.addnext(new)
    for r in table.rows:
        if r._tr is new:
            for c, v in zip(r.cells, values):
                set_text(c, v)
            break
    log.append("+" + values[0])


def find_par(text):
    for el in body.iterchildren():
        if el.tag == W + "p":
            p = Paragraph(el, d)
            if p.text.strip() == text:
                return p
    raise SystemExit(f"paragraph not found: {text}")


def insert_par_after(anchor_par, template_par, text):
    new = copy.deepcopy(template_par._p)
    anchor_par._p.addnext(new)
    set_text(Paragraph(new, d), text)


T = d.tables

# ---------------------------------------------------------------- title block
p = find_par("SCB Collections and Recovery. Henka Group, 28 October 2026")
set_text(p, f"SCB Collections and Recovery. Henka Group, {DATE}")
set_row(T[0], "Version", [None, "4"])
set_row(T[0], "Date", [None, DATE])
add_row_after(T[0], "Structure", [
    "Change",
    "Version 4 applies D-RCV-35 and ADR-010. Sections 3.1, 3.2, 4 and 7 now read source data from ACE "
    "through read-only views instead of loading and checking it. Load, data quality on load and tracker "
    "requirements are removed and keep their keys. RWB-E1-069 and RWB-ACE-001 are added. The counts in "
    "sections 1 and 2 and the tracker line in section 5 follow. Other sections are unchanged.",
])

# ---------------------------------------------------------------- 1 and 2 counts
# Derived from section 3: 67 Epic 1 stories - 8 removed (register Appendix A) + RWB-E1-069 = 60 live;
# all 8 removed were Must and E1-069 is Must, so 57 - 8 + 1 = 50; REQ-RDF-005 and 006 removed, 77 - 2 = 75.
# RWB-ACE-001 is an ACE team story and is not counted. brd_e1_v4 reproduces the v3 figures by the same rule.
set_row(T[1], "Requirements at development detail", [None, "60"])
set_row(T[1], "Must", [None, "50"])
set_row(T[1], "Program requirements this epic meets", [None, "75"])
WHO = [
    ("A product owner", 8), ("A case owner", 8), ("A litigation officer", 8), ("A team manager", 7),
    ("A developer", 6), ("A document hub owner", 6), ("An AI product owner", 5), ("A data product owner", 4),
    ("A center of excellence analyst", 2), ("The Tribe lead", 1), ("The case workflow module", 1),
    ("A head of recovery", 1), ("A security reviewer", 1), ("An operations engineer", 1),
    ("A business analyst", 1),
]
rows2 = T[2].rows[1:]
for r, (who, n) in zip(rows2, WHO):
    set_text(r.cells[0], who)
    set_text(r.cells[1], str(n))
for r in rows2[len(WHO):]:          # a program manager now serves no live requirement
    r._tr.getparent().remove(r._tr)
log.append("s1/s2 counts")

# ---------------------------------------------------------------- 5 tracker request dropped
r5 = row_by_key(T[13], "List every recovery Excel file, SharePoint list and local tracker, with its owner and fields")
r5._tr.getparent().remove(r5._tr)
tbl_el = T[13]._tbl
new_p = copy.deepcopy(find_par("The epic releases on time only if the business gives the support below during the build.")._p)
tbl_el.addnext(new_p)
set_text(Paragraph(new_p, d), "Excel and SharePoint trackers are retired through the Cutover plan (U5).")
log.append("s5 tracker line")

# ---------------------------------------------------------------- 3.1 P1
intro_tmpl = find_par("Each requirement is one backlog story. The requirement states what the Workbench does, "
                      "the benefit states what changes for the user, and the scenarios are the acceptance "
                      "criteria in the story.")
h31 = find_par("3.1 P1 Recovery data engine")
insert_par_after(h31, intro_tmpl,
                 "The Workbench reads source data from the ACE database through read-only recovery.v_ace_* views. "
                 "It does not load, copy or check source data; ACE ingestion does (D-RCV-35, ADR-010). "
                 "A requirement for a load, a data quality check on load or a tracker is removed. "
                 "It keeps its key and names its later home.")

t = T[3]
REM = "Removed"
set_row(t, "RWB-E1-001", [None, None,
    "The recovery schema in the ACE database for the 14 data products: 92 tables, including the 4 extension "
    "tables keyed by ACE business keys, with a data dictionary and one system of record, read path and owner "
    "per product. Source data is read through the ACE views and is never copied",
    None, "Every product has one source and one read path", None, None])
set_row(t, "RWB-E1-002", [None, None,
    "One case list with case ID, account, product, stage, status, owner, queue, route, balance and days past "
    "due for every 90 days past due or more account, read from the ACE account view (v_ace_account) each day "
    "after the ACE batch completes, and available in Power BI",
    None, None, None, None])
set_row(t, "RWB-E1-003", [None, None,
    "Removed by D-RCV-35 (U1). ACE ingests ALS, and the Workbench reads v_ace_account and v_ace_payment. "
    "Later home: ACE ingestion",
    None, "-", REM, "-"])
set_row(t, "RWB-E1-004", [None, None,
    "Removed by D-RCV-35 (U1). ACE ingests EFS, and the Workbench reads v_ace_efs_action and "
    "v_ace_efs_assignment. Later home: ACE ingestion",
    None, "-", REM, "-"])
set_row(t, "RWB-E1-005", [None, None,
    "Removed by D-RCV-35 (U5). Excel and SharePoint trackers leave system scope. Later home: the Cutover plan",
    None, "-", REM, "-"])
set_row(t, "RWB-E1-006", [None, None,
    "Removed by D-RCV-35 (U1). Data quality checks on source data run in ACE ingestion. The daily gate moves "
    "into RWB-E1-015. Later home: ACE ingestion checks",
    None, "-", REM, "-"])
set_row(t, "RWB-E1-009", [None, None,
    "Removed by D-RCV-35 (U1). ACE ingests CCMS and SVAF through RWB-ACE-001, and the Workbench reads "
    "v_ace_collateral, v_ace_collateral_detail and v_ace_valuation. Later home: ACE ingestion",
    None, "-", REM, "-"])
set_row(t, "RWB-E1-010", [None, None,
    "Removed by D-RCV-35 (U5). No tracker is loaded. Later home: the Cutover plan",
    None, "-", REM, "-"])
set_row(t, "RWB-E1-011", [None, None,
    "A daily reconciliation of the case list to the ACE account view (v_ace_account), with the variance and "
    "the results of reconciliation rules REC-01 to REC-05 in one Power BI report",
    None, None, None, None])
set_row(t, "RWB-E1-012", [None, None,
    "Removed by D-RCV-35 (U5). Each team retires its tracker through the Cutover plan. Later home: the Cutover plan",
    None, "-", REM, "-"])
set_row(t, "RWB-E1-015", [None, None,
    "Every data product row to carry the business date and load time of its ACE batch, taken from the ACE "
    "batch record (ace_batch_run, read through v_ace_batch_status), exposed to every consumer and shown on the "
    "case record view. The case list waits for a completed ACE batch and shows the last completed business date",
    None, None, None, None])
set_row(t, "RWB-E1-016", [None, None,
    "Read access to each data product granted by role through the read-only views, PDPA fields tagged, every "
    "read logged, and a catalog entry per product with owner, system of record (ACE, ingested from the named "
    "source), freshness and fields",
    None, None, None, None])
set_row(t, "RWB-E1-064", [None, None,
    "Every field in the 14 data products typed, sourced and owned. The dictionary covers the Workbench tables, "
    "the 4 extension tables and the 30 ACE views: 122 objects and 1,366 fields",
    None, "A data contract can be agreed with the ACE team for every field the Workbench reads", None, None])
set_row(t, "RWB-E1-065", [None, None,
    "A sandbox database holding the ACE schema, the ACE views and synthetic recovery data",
    None, "I can build and test before the ACE additions and the real data are available", None, None])
add_row_after(t, "RWB-E1-068", [
    "RWB-E1-069",
    "Read-only ACE source views, grants and boundary rule",
    "The 30 SELECT-only recovery.v_ace_* views: 16 over ACE tables that exist today (Section A) and 14 over the "
    "ACE additions (Section B, when RWB-ACE-001 lands). The 4 extension tables. SELECT on the views for the "
    "recovery service identity and nothing else. A test that fails the build on a direct read of a public "
    "table, a write to ACE or a foreign key into ACE",
    "A developer",
    "Source data has one copy and one read path, and a wrong read fails the build",
    "Must",
    "-",
])
add_row_after(t, "RWB-E1-069", [
    "RWB-ACE-001",
    "ACE DB additions for the Recovery Workbench",
    "Not built by the Workbench. The ACE team adds 14 tables and 12 columns to the ACE database for the 80 "
    "source fields ACE does not hold, with the ACE batch record ace_batch_run, all filled by ACE ingestion. "
    "The Section B views and the features that need them stay behind their flags until it lands (DL43)",
    "The ACE team lead",
    "The recovery module reads one copy of source data and no recovery load is built",
    "Must",
    "8",
])

# ---------------------------------------------------------------- 3.2 P2
h32 = find_par("3.2 P2 Integration")
insert_par_after(h32, intro_tmpl,
                 "Inbound data comes only through ACE ingestion and the ACE views. "
                 "P2 covers outbound files and events, feature flags and the running of Workbench jobs.")
t = T[4]
set_row(t, "RWB-E1-007", [None,
    "Integration adapters for outbound files and events",
    "One adapter pattern for outbound files and events, with checks, logging, retry and an exception queue. "
    "No inbound file load runs in the Workbench",
    None, "Every later outbound interface follows one pattern", None, None])
set_row(t, "RWB-E1-051", [None, None,
    "Removed by D-RCV-35 (U1). No ADF or Control-M job carries recovery source data; ACE ingestion does. "
    "Later home: ACE ingestion",
    None, "-", REM, "-"])
set_row(t, "RWB-E1-056", [None, None,
    "A run book for every Workbench scheduled job and service (purpose, schedule, owner, failure signs, restart "
    "steps, escalation) and monitoring for each. Source loads are ACE jobs and sit in the ACE run books",
    None, None, None, None])

# ---------------------------------------------------------------- 4 Program requirements
t = T[12]
set_row(t, "REQ-RDF-001", [None,
    "Recovery data is organized in 14 data products, each with exactly one named system of record, one read "
    "path and one named owner. Source data is read from ACE through read-only views and is not copied.",
    None, None])
set_row(t, "REQ-RDF-002", [None,
    "Account balance, arrears, payments and classification for every account at 90 or more days past due are "
    "read from ACE and are current to the previous working day of the ACE batch.",
    None, None])
set_row(t, "REQ-RDF-003", [None,
    "Collections contact history, promises and case status from EFS are read from ACE, which ingests them, so "
    "that the case carries what happened before day 90.",
    None, None])
set_row(t, "REQ-RDF-004", [None,
    "Collateral records and appraisal values are available on the case without a person looking them up in "
    "CCMS or SVAF. ACE ingests them under RWB-ACE-001.",
    None, None])
set_row(t, "REQ-RDF-005", [None,
    "Removed by D-RCV-35 (U5). Excel and SharePoint trackers leave system scope. Later home: the Cutover plan "
    "lists and retires them.",
    REM, None])
set_row(t, "REQ-RDF-006", [None,
    "Removed by D-RCV-35 (U5). No tracker file is loaded. Later home: the Cutover plan retires each local copy "
    "with the owner's confirmation and a read-only archive.",
    REM, None])
set_row(t, "REQ-RDF-007", [None,
    "The case list reconciles daily to the ACE account view, which ACE ingests from ALS, with no variance (DL25).",
    None, None])
set_row(t, "REQ-RDF-008", [None,
    "No Workbench load runs, so data quality checks on source data run in ACE ingestion. Reconciliation rules "
    "REC-01 to REC-05 run on the case list every day, and every failed account carries a reason code visible "
    "to the data product owner.",
    None, None])
set_row(t, "REQ-RDF-009", [None,
    "Every data product carries a freshness stamp from the ACE batch record, and every decision records the "
    "freshness of the data it used.",
    None, None])
set_row(t, "REQ-RDF-010", [None,
    "Access to each data product is controlled per role through the read-only views, and personal data is "
    "masked by role in line with PDPA.",
    None, None])
set_row(t, "REQ-RDF-011", [None,
    "Every data product has a catalog entry stating its definition, owner, system of record (ACE, ingested "
    "from the named source), refresh cycle and retention.",
    None, None])
set_row(t, "REQ-CWC-001", [None,
    "Every account at 90 or more days past due that is not excluded carries one recovery case, created by rule "
    "from the daily ACE batch.",
    None, None])
set_row(t, "REQ-DRI-006", [None,
    "No component calls a system of record directly. Source data is read from the ACE database through the "
    "read-only recovery.v_ace_* views, and leaves through paths ACE already has (D-RCV-35, ADR-010).",
    None, None])
set_row(t, "REQ-DRI-007", [None,
    "The integration adapters log every outbound file and event, retry on a defined schedule, and place "
    "anything that fails after the retry limit in an exception queue with a task for a named owner.",
    None, None])
set_row(t, "REQ-DRI-008", [None,
    "Data from other systems reaches the Workbench only through ACE ingestion and the ACE views. Interfaces "
    "that need same-day data are named under DL06 before any is built.",
    None, None])

# ---------------------------------------------------------------- 7 Open decisions
t = T[14]
first_data = t.rows[1]._tr
new06 = copy.deepcopy(first_data)
first_data.addprevious(new06)
for r in t.rows:
    if r._tr is new06:
        for c, v in zip(r.cells, [
            "DL06",
            "Which interfaces need real-time data, and which take the daily batch?",
            "Option A, a daily batch through COLLINS, is superseded by D-RCV-35: ACE ingests all source data "
            "and the Workbench runs no batch load. Same-day triggers are named under option B: case transferred "
            "from EFS, payment received, legal event.",
            "K. Book with K. Pipat",
            "30 Oct"]):
            set_text(c, v)
log.append("+DL06")
add_row_after(t, "DL10", [
    "DL12",
    "Which legacy systems are kept, and does any need enhancing?",
    "No legacy enhancement. The read and write wording of option A is superseded by D-RCV-35: source data is "
    "read only, through the recovery.v_ace_* views.",
    "K. Tony with K. Book",
    "7 Nov",
])
set_row(t, "DL20", [None, None,
    "The customer facts ACE holds, ingested from SCBPDM and the core bank, read through v_ace_customer. "
    "Amended by D-RCV-35.",
    None, None])
set_row(t, "DL25", [None,
    "How large a difference between the case list and the ACE account view is accepted?",
    None, None, None])
add_row_after(t, "DL40", [
    "DL43",
    "Does the ACE team accept the RWB-ACE-001 scope and its dates?",
    "Yes: 14 tables, 12 columns and 80 source fields by 21 November. Until they land, the Section B views and "
    "the features that need them stay behind their flags.",
    "ACE team lead",
    "21 Nov",
])

d.save(DST)
print("saved", DST)
print("edited:", ", ".join(log))
