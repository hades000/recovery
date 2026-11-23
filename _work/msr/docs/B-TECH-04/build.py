"""Build Recovery Workbench Interface Specifications v4.xlsx (WP B-TECH-04, D-RCV-60).

The output file is created first with compat/office_write.py copy; this script only
touches the copy. It never writes the v3 source.

Changes made to the copy (nothing else in the workbook is touched):
  * Read me sheet added as the first sheet: Template and Rules R8.1 header lines,
    document control, the change-log row, counts and sources.
  * Interfaces sheet: INT-19 and INT-20 removed; three owner columns added
    (Owner code, Owning service, Owner basis) from the Microservice Ownership Map v1;
    Owner and Owner of the fix made per service where v3 named the single Workbench
    or a generic administrator; version row added in row 3.
  * Field mapping sheet: Owning service column added; Owner "Workbench" replaced by the
    owning service for the two outbound interfaces.
  * Key sheet: rows for the three new columns and for the two removed interfaces, and
    the Workbench row read as per-service.
  * Realignment changes sheet added last: every change with its decision, pattern and basis.
"""
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = Path(r"05 Technical architecture\Recovery Workbench Interface Specifications v4.xlsx")

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
H1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
H2 = "(C) Siam Commercial Bank and Henka Pte Ltd"

PURPLE = "FF4E297F"
TITLE_FONT = Font(name="Aptos", size=14, bold=True, color=PURPLE)
SUB_FONT = Font(name="Aptos", size=10, bold=True, color=PURPLE)
HDR_FONT = Font(name="Aptos", size=9, bold=True, color="FFFFFFFF")
HDR_FILL = PatternFill("solid", fgColor=PURPLE)
BODY_FONT = Font(name="Aptos", size=9, color="FF262626")
ALT_FILL = PatternFill("solid", fgColor="FFF3EFF9")
THIN = Side(style="thin", color="FFD9D2E6")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
TOP = Alignment(vertical="top")

# ------------------------------------------------------------------ owners
# Ownership Map v1, sheet Services (code, service, name, wave)
SERVICES = [
    ("P1", "rwb-source-data", "Source data", 1),
    ("P2", "rwb-integration", "Integration", 1),
    ("P3", "rwb-case", "Case and workflow", 1),
    ("P4", "rwb-access", "Access and authority", 1),
    ("P5", "rwb-document", "Document", 1),
    ("P6", "rwb-comms", "Communications", 1),
    ("P7", "rwb-decision", "Decision and rules", 1),
    ("P8", "rwb-payment", "Payment", 2),
    ("P9", "rwb-reporting", "Reporting", 1),
    ("P10", "rwb-agent", "Agent", 1),
    ("S1", "rwb-valuation", "Valuation and route", 3),
    ("S2", "rwb-treatment", "Treatment and offer", 2),
    ("S3", "rwb-guarantee", "Guarantee", 3),
    ("S4", "rwb-litigation", "Litigation", 3),
    ("S5", "rwb-asset", "Asset", 2),
    ("S6", "rwb-debtsale", "Debt sale", 3),
    ("S7", "rwb-writeoff", "Write-off", 4),
    ("S8", "rwb-deviation", "Deviation", 2),
    ("S9", "rwb-partner", "Partner", 4),
]
NAME = {s[1]: s[2] for s in SERVICES}
NAME_LOOKUP = {s[0]: "%s %s" % (s[0], s[1]) for s in SERVICES}

B_P1 = ("ADR-010 and Architecture v5 slide 9: only rwb-source-data reads the 30 "
        "recovery.v_ace_* views; Ownership Map v1, sheet Services.")
B_P6_FILE = ("Ownership Map v1 ruling JOB-10 (rwb-comms owns the notice and the 16:00 window); "
             "Architecture v5 slide 30 (5); rwb-integration performs deliverFile.")
B_P6_SMS = ("Architecture v5 slide 30 (5): rwb-comms sends SMS and LINE messages through the "
            "ACE notification path (NSS, LINE OA).")
B_P4 = ("Architecture v5 slide 30 (1): gateway-bff and rwb-access use ACE's Entra-based sign-in; "
        "Recovery roles, scope, masking and DoA stay as data in rwb-access.")
B_PLT = ("Architecture v5 slide 30 (2): every service sends audit and personal-data access logs "
         "through ACE's PII Kafka path; the platform observability set RWB-PLT-OBS owns the sender library.")
B_P10 = "Architecture v5 slides 6 and 8: the Enterprise AI private endpoint (INT-23) is called by rwb-agent."
B_S9 = ("Architecture v5 slide 8: the partner gateway (FAPI 2.0) fronts rwb-partner; "
        "Ownership Map v1 ruling EV-21.")
B_S6 = ("Service Catalog v1, S6 file contract (buyer file per lot through rwb-integration); "
        "Architecture v5 slide 17 (debt-buyer files from rwb-integration).")
B_P2 = ("Architecture v5 slide 17: rwb-integration owns interface config, file runs, outbound items "
        "and ACE integration paths; consumers per Architecture v5 slide 30.")
B_P1_C = ("ADR-010: read through a recovery.v_ace_* view by rwb-source-data only; "
          "the business consumer follows Architecture v5 slide 30.")

# owner code, owning service name, basis
OWNERS = {
    "INT-01": ("P1", B_P1), "INT-02": ("P1", B_P1), "INT-04": ("P1", B_P1),
    "INT-07": ("P1", B_P1), "INT-08": ("P1", B_P1), "INT-09": ("P1", B_P1),
    "INT-10": ("P1", B_P1), "INT-11": ("P1", B_P1), "INT-12": ("P1", B_P1),
    "INT-13": ("P1", B_P1), "INT-15": ("P1", B_P1), "INT-16": ("P1", B_P1),
    "INT-14": ("P6", B_P6_FILE),
    "INT-17": ("P6", B_P6_SMS),
    "INT-18": ("P6", B_P6_SMS),
    "INT-21": ("P4", B_P4),
    "INT-22": ("PLT", B_PLT),
    "INT-23": ("P10", B_P10),
    "INT-24": ("S9", B_S9),
    "INT-25": ("S6", B_S6),
    "INT-34": ("P2", B_P2),
    "INT-35": ("P1", B_P1_C),
    "INT-36": ("P1", B_P1_C),
}
SERVICE_LABEL = {"PLT": "platform observability (RWB-PLT-OBS)"}

# Owner cell, where v3 named the single Workbench
OWNER_F = {"INT-14": "P6 rwb-comms", "INT-24": "S9 rwb-partner", "INT-25": "S6 rwb-debtsale"}
# Owner of the fix cell, where v3 named a generic administrator or a single party
FIX_M = {
    "INT-14": "P6 rwb-comms; P2 rwb-integration for the file transfer",
    "INT-24": "S9 rwb-partner; partner and agency manager",
    "INT-25": "S6 rwb-debtsale; P2 rwb-integration for the file transfer",
    "INT-21": "P4 rwb-access; ACE team for the sign-in",
    "INT-22": "PLT (RWB-PLT-OBS); ACE team for the PII Kafka path",
    "INT-23": "P10 rwb-agent; Enterprise AI for the endpoint",
    "INT-34": "P2 rwb-integration; ACE team for the shared service",
    "INT-35": "P1 rwb-source-data; ACE team for the feed",
    "INT-36": "P1 rwb-source-data; ACE team for the feed",
}

REMOVED = ("INT-19", "INT-20")

DESCRIPTION = (
    "23 numbered interfaces the Workbench builds or reads (25 in v3, 22 November 2026, D-RCV-60: "
    "INT-19 and INT-20 are removed under DP-17 and ADR-018, no data lake), including INT-35 "
    "(NLEADS credit decision) and INT-36 (EasyApp e-signature), the two new ACE inbound interfaces "
    "raised in RWB-ACE-001. Inbound source interfaces are owned by the ACE team; this sheet and the "
    "Field mapping sheet are the ACE ingestion contract. No component calls a system of record "
    "directly. Owner code, Owning service and Owner basis give the per-service owner from the "
    "Microservice Ownership Map v1. Supersedes v3."
)

READ_ME = [
    (H1, TITLE_FONT),
    (H2, BODY_FONT),
    (None, None),
    ("Recovery Workbench Interface Specifications v4. Decision D-RCV-60. Next version of Recovery "
     "Workbench Interface Specifications v3 (15 November 2026, D-RCV-35).", TITLE_FONT),
    ("The numbered interfaces the Workbench builds or reads, the field mapping that forms the ACE "
     "ingestion specification, the checks every outbound file passes and the key. Every section, ID, "
     "number and date of v3 is kept; INT-19 and INT-20 are removed (no data lake) and every interface "
     "carries the per-service owner of the Microservice Ownership Map v1.", BODY_FONT),
    ("Tool: " + TOOL + ".", BODY_FONT),
    ("Status: Draft. This document is issued with no approval recorded (ASM-B-TECH-04-1).", BODY_FONT),
    ("Release: the interface set is delivered across waves 1 to 4 of the Ownership Map v1; any release "
     "date written into this workbook is tentative (Template and Rules \u00a7R1 U7).", BODY_FONT),
    (None, None),
    ("Change log", SUB_FONT),
    ("v4, 22 November 2026, D-RCV-60 microservice realignment, " + TOOL, BODY_FONT),
    ("v3, 15 November 2026, D-RCV-35 (the source of this version; it is not changed by this run).", BODY_FONT),
    (None, None),
    ("What this version holds", SUB_FONT),
    ("Interfaces: 23 numbered interfaces, 14 read into ACE through a recovery.v_ace_* view, 1 further "
     "inbound interface (INT-21), 5 outbound interfaces and 3 that run both ways.", BODY_FONT),
    ("Field mapping: 82 mappings kept character for character, 75 inbound (Tier 1 and Tier 2) and 7 "
     "outbound (Tier 4); one Owning service column added.", BODY_FONT),
    ("Outbound checks: the 3 checks of v3 (layout, control totals, acknowledgement), unchanged.", BODY_FONT),
    ("Key: the terms of v3 plus a row for Owner code, Owning service, Owner basis and the removed "
     "interfaces.", BODY_FONT),
    ("Realignment changes: every change of v4 in one table with its decision, pattern and basis.", BODY_FONT),
    (None, None),
    ("Counts", SUB_FONT),
    ("23 interfaces: P1 rwb-source-data owns 14, P6 rwb-comms owns 3, and P2 rwb-integration, "
     "P4 rwb-access, P10 rwb-agent, PLT (RWB-PLT-OBS), S6 rwb-debtsale and S9 rwb-partner own 1 each.", BODY_FONT),
    ("82 field mappings: 75 inbound and 7 outbound; no INT-19 or INT-20 mapping exists in v3, so none "
     "is removed.", BODY_FONT),
    ("2 interfaces removed: INT-19 (data lake and Power BI) and INT-20 (COLLINS model learning).", BODY_FONT),
    (None, None),
    ("Sources", SUB_FONT),
    ("Recovery Workbench Interface Specifications v3.xlsx (15 November 2026, D-RCV-35), sheets "
     "Interfaces, Field mapping, Outbound checks and Key.", BODY_FONT),
    ("Recovery Workbench Architecture v5 Text Extract v1, slides 6, 8, 9, 17, 30, 37 and 41.", BODY_FONT),
    ("Recovery Workbench Microservice Ownership Map v1, sheets Services, Tables, Events, Jobs and "
     "Rulings, and _work/msr/plan/ownership.json.", BODY_FONT),
    ("Recovery Workbench Temporal and Drools Design Text Extract v1 (Temporal layers L1 to L5, Nexus, "
     "file windows).", BODY_FONT),
    ("Template and Rules v1 \u00a7R1 (U2, U5, U7), \u00a7R3 (R-PREC and the default rulings), \u00a7R5.5 DP-17, "
     "\u00a7R8.1, \u00a7R8.2 and \u00a7R9.", BODY_FONT),
    ("_work/msr/plan/ids.json: ADR-013 to ADR-023 and DL44 to DL49 are the decisions of this run.", BODY_FONT),
    (None, None),
    ("Open points", SUB_FONT),
    ("No reporting interface replaces INT-19 and INT-20 in this workbook: rwb-reporting builds its read "
     "model from events (DP-17), and the interface that delivers the reporting output is not specified "
     "in the source documents (CG-B-TECH-04-1; ASM-B-TECH-04-2).", BODY_FONT),
    ("INT-34 (ACE Common) has five consumers and no single owning service in the source; "
     "P2 rwb-integration is recorded (CG-B-TECH-04-3; ASM-B-TECH-04-4).", BODY_FONT),
    ("Candidate gap rows CG-B-TECH-04-1 to CG-B-TECH-04-9 and candidate assumption rows "
     "ASM-B-TECH-04-1 to ASM-B-TECH-04-12 are written by this work package; step D1 renumbers them.",
     BODY_FONT),
]

CHANGES = [
    ("1", "Header lines and change log added",
     "Read me sheet (new, first sheet)",
     "No header lines and no change log in the workbook",
     "Header lines 1 and 2 of Template and Rules \u00a7R8.1; change-log row naming D-RCV-60 and the tool line",
     "D-RCV-60", "Template and Rules \u00a7R8.1, \u00a7R8.2"),
    ("2", "Version row added to the Interfaces sheet",
     "Interfaces, row 3",
     "Row 3 blank",
     "Version 4, 22 November 2026, D-RCV-60, 23 interfaces",
     "D-RCV-60", "Template and Rules \u00a7R8.2"),
    ("3", "INT-19 removed",
     "Interfaces, sheet row of INT-19",
     "Data lake and Power BI, case, queue, decision and outcome data for reporting, daily batch",
     "Row removed. Reporting reads events into rwb-reporting; no data lake connection",
     "D-RCV-60, ADR-018, DP-17",
     "Architecture v5 slide 37 (INT-19/20 removed); slide 44 (JOB-13 continuous Kafka ingest); Template and Rules \u00a7R5.5 DP-17"),
    ("4", "INT-20 removed",
     "Interfaces, sheet row of INT-20",
     "COLLINS decisions and outcomes for model learning, daily batch to the data lake",
     "Row removed. No data lake; model learning reads the decision records in rwb-decision",
     "D-RCV-60, ADR-018, DP-17",
     "Architecture v5 slide 37; slide 44 JOB-13; Template and Rules \u00a7R5.5 DP-17"),
    ("5", "Count in the sheet description corrected",
     "Interfaces, row 2",
     "25 numbered interfaces",
     "23 numbered interfaces (25 in v3; INT-19 and INT-20 removed) and a pointer to the owner columns",
     "D-RCV-60", "This sheet; Template and Rules \u00a7R8.2"),
    ("6", "Per-service owners added",
     "Interfaces, columns Owner code, Owning service and Owner basis; Field mapping, column Owning service",
     "One Owner column with ACE team, Workbench or Bank platform",
     "The interface owner party kept; the Recovery-side owner given as the service code and name from the Ownership Map v1, with the basis",
     "D-RCV-60, DL44, DL46", "Microservice Ownership Map v1, sheet Services; Architecture v5 slides 9, 17 and 30"),
    ("7", "Owner column made per service where it read Workbench",
     "Interfaces, column Owner, rows INT-14, INT-24 and INT-25",
     "Workbench",
     "P6 rwb-comms (INT-14), S9 rwb-partner (INT-24), S6 rwb-debtsale (INT-25)",
     "D-RCV-60, DL45", "Architecture v5 slides 8, 17 and 30; Ownership Map v1 ruling JOB-10; Service Catalog v1, S6"),
    ("8", "Owner of the fix made per service",
     "Interfaces, column Owner of the fix, rows INT-14, INT-21, INT-22, INT-23, INT-24, INT-25, INT-34, INT-35 and INT-36",
     "Owning team, platform administrator; Security administrator; Enterprise AI; Partner and agency manager; ACE team",
     "The owning service first, then the role or party that acts",
     "D-RCV-60, DL46", "Microservice Ownership Map v1; Architecture v5 slide 30"),
    ("9", "Inbound read path recorded",
     "Interfaces, rows INT-01 to INT-16, INT-35 and INT-36",
     "Owner ACE team, read path in the Approach column",
     "Owner code P1, Owning service rwb-source-data: only rwb-source-data reads the recovery.v_ace_* views",
     "D-RCV-60, ADR-010", "Architecture v5 slide 9; Architecture Decision Records v3 ADR-010"),
    ("10", "Field mapping kept and extended",
     "Field mapping, all 82 rows",
     "82 mappings; Owner ACE team or Workbench",
     "82 mappings kept character for character; Owner Workbench replaced by the owning service on the 7 outbound rows; Owning service column added on every row",
     "D-RCV-60, DP-01", "This workbook; Template and Rules \u00a7R5.5 DP-01"),
    ("11", "Key extended",
     "Key, last rows",
     "No row for an owner code, an owning service or a removed interface",
     "Rows for Owner code, Owning service, Owner basis and INT-19/INT-20; the Workbench row read as per service",
     "D-RCV-60", "This workbook"),
    ("12", "No release date added",
     "Whole workbook",
     "The source carries no release date",
     "No release date is added; any release date written later is tentative",
     "D-RCV-60", "Template and Rules \u00a7R1 U7"),
]


def style_header(ws, row, first, last):
    for c in range(first, last + 1):
        cell = ws.cell(row, c)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.border = BORDER
        cell.alignment = Alignment(wrap_text=True, vertical="center")


def style_body(ws, r1, r2, ncol):
    for r in range(r1, r2 + 1):
        for c in range(1, ncol + 1):
            cell = ws.cell(r, c)
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = WRAP
            if (r - r1) % 2 == 1:
                cell.fill = ALT_FILL


def build_read_me(wb):
    ws = wb.create_sheet("Read me", 0)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 150
    for i, (text, font) in enumerate(READ_ME, 1):
        cell = ws.cell(i, 1)
        if text is None:
            continue
        cell.value = text
        cell.font = font or BODY_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    return ws


def build_interfaces(ws):
    assert ws.cell(20, 1).value == "INT-19", ws.cell(20, 1).value
    assert ws.cell(21, 1).value == "INT-20", ws.cell(21, 1).value
    ws.delete_rows(20, 2)
    last = ws.max_row
    assert last == 27, last  # 23 data rows, header on row 4

    ws.insert_cols(7, 3)
    # header of the three new columns, styled from the Owner header
    for col, title in ((7, "Owner code"), (8, "Owning service"), (9, "Owner basis")):
        cell = ws.cell(4, col)
        cell.value = title
        cell._style = copy(ws.cell(4, 6)._style)

    for r in range(5, last + 1):
        iid = ws.cell(r, 1).value
        code, basis = OWNERS[iid]
        label = SERVICE_LABEL.get(code) or NAME_LOOKUP[code]
        for col, value in ((7, code), (8, label), (9, basis)):
            cell = ws.cell(r, col)
            cell.value = value
            cell._style = copy(ws.cell(r, 6)._style)
        if iid in OWNER_F:
            ws.cell(r, 6).value = OWNER_F[iid]
        if iid in FIX_M:
            ws.cell(r, 16).value = FIX_M[iid]

    ws.cell(2, 1).value = DESCRIPTION
    v = ws.cell(3, 1)
    v.value = ("Version 4, 22 November 2026. D-RCV-60. 23 interfaces: INT-19 and INT-20 are removed "
               "(no data lake, DP-17).")
    v.font = Font(name="Aptos", size=10, bold=True, color=PURPLE)

    ws.column_dimensions["G"].width = 10
    ws.column_dimensions["H"].width = 20
    ws.column_dimensions["I"].width = 46
    ws.auto_filter.ref = "A4:%s%d" % (get_column_letter(ws.max_column), last)
    return ws


def build_field_mapping(ws):
    last = ws.max_row
    assert ws.cell(4, 11).value == "Owner", ws.cell(4, 11).value
    ws.insert_cols(12, 1)
    cell = ws.cell(4, 12)
    cell.value = "Owning service"
    cell._style = copy(ws.cell(4, 11)._style)
    n = 0
    for r in range(5, last + 1):
        iid = ws.cell(r, 1).value
        if iid in REMOVED:
            raise SystemExit("unexpected removed interface in Field mapping: %s" % iid)
        code = OWNERS[iid][0]
        label = SERVICE_LABEL.get(code) or NAME_LOOKUP[code]
        cell = ws.cell(r, 12)
        cell.value = label
        cell._style = copy(ws.cell(r, 11)._style)
        if ws.cell(r, 11).value == "Workbench":
            ws.cell(r, 11).value = label
        n += 1
    ws.column_dimensions["L"].width = 20
    ws.auto_filter.ref = "A4:%s%d" % (get_column_letter(ws.max_column), last)
    return n


def build_key(ws):
    last = ws.max_row
    rows = [
        ("Column", "Owner code",
         "The service code of the Ownership Map v1 (P1 to P10, S1 to S9) or PLT for a platform "
         "capability. New in v4 under D-RCV-60."),
        ("Column", "Owning service",
         "The service that owns the interface on the Recovery side. For an inbound source interface "
         "the ACE team stays the owner of the interface and rwb-source-data is the owning service, "
         "because only rwb-source-data reads the recovery.v_ace_* views. New in v4 under D-RCV-60."),
        ("Column", "Owner basis",
         "The slide, ruling or document that gives the owner of the row. New in v4 under D-RCV-60."),
        ("Interface", "INT-19, INT-20",
         "Removed in v4: there is no data lake. Reporting reads events into rwb-reporting (ADR-018, "
         "DP-17) and no interface delivers case data to Power BI."),
    ]
    for i, row in enumerate(rows, last + 1):
        for c, value in enumerate(row, 1):
            cell = ws.cell(i, c)
            cell.value = value
            cell._style = copy(ws.cell(last, c)._style)
    # the Workbench row of v3 is read as per service
    for r in range(5, last + 1):
        if ws.cell(r, 1).value == "Owner" and ws.cell(r, 2).value == "Workbench":
            ws.cell(r, 3).value = ("v3 named the single Workbench. In v4 the outbound interface is owned "
                                   "by the delivering service (Owner code and Owning service), and the "
                                   "case data it sends stays in that service's own schema.")
    ws.auto_filter.ref = "A4:C%d" % (last + len(rows))
    return len(rows)


def build_changes(wb):
    ws = wb.create_sheet("Realignment changes")
    ws.sheet_view.showGridLines = False
    hdr = ["#", "Change", "Where", "v3 (source)", "v4 (this version)", "Decision", "Basis"]
    for c, value in enumerate(hdr, 1):
        ws.cell(4, c).value = value
    style_header(ws, 4, 1, len(hdr))
    for i, row in enumerate(CHANGES, 5):
        for c, value in enumerate(row, 1):
            ws.cell(i, c).value = value
    style_body(ws, 5, 4 + len(CHANGES), len(hdr))
    for col, w in zip("ABCDEFG", (5, 40, 44, 52, 62, 26, 58)):
        ws.column_dimensions[col].width = w
    ws.cell(1, 1).value = H1
    ws.cell(1, 1).font = Font(name="Aptos", size=9, bold=True, color=PURPLE)
    ws.cell(2, 1).value = H2
    ws.cell(2, 1).font = BODY_FONT
    ws.cell(3, 1).value = ("Every change of Interface Specifications v4 against v3, with the decision, "
                           "the pattern and the source. Nothing else in the workbook is changed.")
    ws.cell(3, 1).font = BODY_FONT
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = "A4:G%d" % (4 + len(CHANGES))
    return ws


def main():
    wb = openpyxl.load_workbook(OUT)
    assert wb.sheetnames == ["Interfaces", "Field mapping", "Outbound checks", "Key"], wb.sheetnames
    build_read_me(wb)
    ws = wb["Interfaces"]
    build_interfaces(ws)
    n = build_field_mapping(wb["Field mapping"])
    k = build_key(wb["Key"])
    build_changes(wb)
    wb.active = 0
    wb.save(OUT)
    print("WROTE", OUT)
    print("interfaces rows", ws.max_row - 4, "field mapping rows", n, "key rows added", k)


if __name__ == "__main__":
    main()
