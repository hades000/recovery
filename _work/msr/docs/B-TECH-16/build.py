"""Build Recovery Workbench System Disposition and Integration Inventory v4.xlsx (WP B-TECH-16, D-RCV-60).

The output file is created first with compat/office_write.py copy; this script only
touches the copy and never writes the v3 source.

Changes made to the copy (nothing else in the workbook is touched):
  * Read me sheet added as the first sheet: Template and Rules R8.1 header lines,
    document control, the change-log row, what the version holds, counts, sources
    and open points.
  * Disposition sheet: one Service column added after Owner, filled on 25 of 25 rows
    from the Microservice Ownership Map v1.
  * Interfaces sheet: one Service column added after Owner, filled on 36 of 36 rows.
  * By route sheet: the In, Out, Both and Total counts calculated from the 36
    interfaces (v3 left every count cell empty).
  * Key sheet: six rows appended (Service, the three readings of the Owner column,
    INT-19 and INT-20, and the pointer to the Service rules); the 27 source rows
    are unchanged.
  * By service, Service rules and Realignment changes sheets added at the end.
  * Workbook properties set to the organisation and the tool (root rule 4).
"""
from copy import copy
from datetime import datetime
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

OUT = Path(r"05 Technical architecture\Recovery Workbench System Disposition and Integration Inventory v4.xlsx")

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
H1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
H2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
PURPLE = "004E297F"
GREY = "00404040"

# ------------------------------------------------------------------ services
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
LABEL = {c: f"{c} {s}" for c, s, _, _ in SERVICES}
WAVE = {c: w for c, _, _, w in SERVICES}
NAME = {c: n for c, _, n, _ in SERVICES}
PLT = "PLT RWB-PLT-OBS"

# --------------------------------------------------- Disposition sheet, rows 5..29
DISP = {
    "Core bank (ALS)": "P1 rwb-source-data (INT-01, INT-02); P8 rwb-payment (INT-03)",
    "SCBPDM": "P1 rwb-source-data",
    "UDP": "P1 rwb-source-data",
    "AAL": "P1 rwb-source-data",
    "EFS": "P1 rwb-source-data",
    "COLLINS": "P1 rwb-source-data (INT-08); P9 rwb-reporting (INT-20)",
    "ACE": "P2 rwb-integration (INT-34); P4 rwb-access (INT-21); PLT RWB-PLT-OBS (INT-22)",
    "LIT": "P1 rwb-source-data (INT-09); S4 rwb-litigation (INT-33)",
    "CCMS": "P1 rwb-source-data",
    "SVAF": "P1 rwb-source-data",
    "AMIS": "P1 rwb-source-data",
    "RPS": "P1 rwb-source-data",
    "WIN": "P6 rwb-comms (INT-14); P1 rwb-source-data (INT-15)",
    "GL": "P1 rwb-source-data",
    "NSS and LINE OA": "P6 rwb-comms (INT-17, INT-18)",
    "Data lake and Power BI": "P9 rwb-reporting (INT-19)",
    "Enterprise AI model endpoint": "P10 rwb-agent (INT-23)",
    "Partner portal": "S9 rwb-partner (INT-24); S6 rwb-debtsale (INT-25)",
    "NLEADS": "P1 rwb-source-data (INT-35); no path for INT-26 (the officer submits in NLEADS)",
    "HOME.SCB": "S5 rwb-asset (INT-27)",
    "SCIS, TCG, NCB, Aric, Salesforce": (
        "S5 rwb-asset (INT-28, INT-32); S3 rwb-guarantee (INT-29); "
        "P1 rwb-source-data (INT-30); S8 rwb-deviation (INT-31)"
    ),
    "Recovery team spreadsheets and SharePoint lists": "P1 rwb-source-data",
    "Email approvals in Outlook": "P7 rwb-decision",
    "Shared folders of scanned documents": "P5 rwb-document",
    "EasyApp": "P1 rwb-source-data (INT-36); P5 rwb-document for the signed file",
}

# --------------------------------------------------- Interfaces sheet, rows 5..40
INT = {
    "INT-01": "P1", "INT-02": "P1", "INT-03": "P8", "INT-04": "P1", "INT-05": "P1",
    "INT-06": "P1", "INT-07": "P1", "INT-08": "P1", "INT-09": "P1", "INT-10": "P1",
    "INT-11": "P1", "INT-12": "P1", "INT-13": "P1", "INT-14": "P6", "INT-15": "P1",
    "INT-16": "P1", "INT-17": "P6", "INT-18": "P6", "INT-19": "P9", "INT-20": "P9",
    "INT-21": "P4", "INT-22": "PLT", "INT-23": "P10", "INT-24": "S9", "INT-25": "S6",
    "INT-26": "P2", "INT-27": "S5", "INT-28": "S5", "INT-29": "S3", "INT-30": "P1",
    "INT-31": "S8", "INT-32": "S5", "INT-33": "S4", "INT-34": "P2", "INT-35": "P1",
    "INT-36": "P1",
}
ORDER = [c for c, _, _, _ in SERVICES] + ["PLT"]
SHOW = dict(LABEL, PLT=PLT)


def svc(code):
    return SHOW[code]


# ------------------------------------------------------------------ styles
def style_from(cell, src):
    cell.font = copy(src.font)
    cell.fill = copy(src.fill)
    cell.alignment = copy(src.alignment)
    cell.border = copy(src.border)
    if src.number_format:
        cell.number_format = src.number_format


def title_rows(ws, a1, a2):
    ws["A1"] = a1
    ws["A2"] = a2


def header_row(ws, row, values, ref):
    for col, v in enumerate(values, 1):
        c = ws.cell(row=row, column=col, value=v)
        style_from(c, ref)


def body_rows(ws, rows, ref_map):
    for r, vals in enumerate(rows):
        row = r + 1
        for col, v in enumerate(vals, 1):
            c = ws.cell(row=row, column=col, value=v)
            style_from(c, ref_map(col))


def main():
    wb = openpyxl.load_workbook(OUT)
    src_disp, src_key = wb["Disposition"], wb["Key"]
    title_font = copy(src_disp["A1"].font)
    sub_font = copy(src_disp["A2"].font)
    hdr_font = copy(src_disp["A4"].font)
    hdr_fill = copy(src_disp["A4"].fill)
    hdr_align = copy(src_disp["A4"].alignment)
    hdr_border = copy(src_disp["A4"].border)
    body_ref = {k: src_disp[k] for k in ("A5",)}
    body_font = copy(body_ref["A5"].font)
    body_fill = copy(body_ref["A5"].fill)
    body_align = copy(body_ref["A5"].alignment)
    body_border = copy(body_ref["A5"].border)

    def new_sheet(title, a1, a2, headers, widths):
        ws = wb.create_sheet(title)
        ws["A1"] = a1
        ws["A2"] = a2
        for col, v in enumerate(headers, 1):
            c = ws.cell(row=4, column=col, value=v)
            c.font, c.fill, c.alignment, c.border = (copy(hdr_font), copy(hdr_fill),
                                                     copy(hdr_align), copy(hdr_border))
        for col, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(col)].width = w
        ws["A1"].font = copy(title_font)
        ws["A2"].font = copy(sub_font)
        ws.freeze_panes = "A5"
        return ws

    def fill(ws, first_row, rows, ncols):
        for r, vals in enumerate(rows):
            for col in range(1, ncols + 1):
                c = ws.cell(row=first_row + r, column=col, value=vals[col - 1] if col <= len(vals) else None)
                c.font, c.fill, c.alignment, c.border = (copy(body_font), copy(body_fill),
                                                         copy(body_align), copy(body_border))

    # ------------------------------------------------------------ Disposition
    disp = wb["Disposition"]
    keys = [disp.cell(row=r, column=1).value for r in range(5, 30)]
    assert keys == list(DISP), keys
    disp.insert_cols(6)
    for r in range(5, 30):
        c = disp.cell(row=r, column=6, value=DISP[disp.cell(row=r, column=1).value])
        style_from(c, disp.cell(row=r, column=5))  # Owner style of the same row
        c.font = copy(body_font)
        c.alignment = copy(body_align)
    style_from(disp.cell(row=4, column=6, value="Service"), disp.cell(row=4, column=5))
    for col, w in zip("ABCDEFGHIJ", (30, 44, 16, 14, 13, 22, 64, 7, 26, 12)):
        disp.column_dimensions[col].width = w
    disp.auto_filter.ref = "A4:J29"

    # ------------------------------------------------------------ Interfaces
    itf = wb["Interfaces"]
    ids = [itf.cell(row=r, column=1).value for r in range(5, 41)]
    assert ids == list(INT), ids
    itf.insert_cols(11)
    for r in range(5, 41):
        c = itf.cell(row=r, column=11, value=svc(INT[itf.cell(row=r, column=1).value]))
        style_from(c, itf.cell(row=r, column=10))
        c.font = copy(body_font)
        c.alignment = copy(body_align)
    style_from(itf.cell(row=4, column=11, value="Service"), itf.cell(row=4, column=10))
    for col, w in zip("ABCDEFGHIJKLMN", (8, 26, 44, 9, 16, 38, 18, 12, 12, 13, 20, 10, 18, 11)):
        itf.column_dimensions[col].width = w
    itf.auto_filter.ref = "A4:N40"

    # ------------------------------------------------------------ By route
    by_route = wb["By route"]
    routes = [by_route.cell(row=r, column=1).value for r in range(5, 10)]
    assert routes == ["COLLINS", "File", "Direct through ACE", "Through partners", "Not at all today"], routes
    counts = {}
    for r in range(5, 41):
        route, direction = itf.cell(row=r, column=5).value, itf.cell(row=r, column=4).value
        counts.setdefault(route, {"In": 0, "Out": 0, "Both": 0})[direction] += 1
    expect = {"COLLINS": (8, 0, 0), "File": (8, 4, 0), "Direct through ACE": (1, 3, 3),
              "Through partners": (1, 0, 0), "Not at all today": (2, 5, 1)}
    total = {"In": 0, "Out": 0, "Both": 0}
    for r in range(5, 10):
        route = by_route.cell(row=r, column=1).value
        got = counts.get(route, {"In": 0, "Out": 0, "Both": 0})
        assert (got["In"], got["Out"], got["Both"]) == expect[route], (route, got)
        for col, k in zip((2, 3, 4), ("In", "Out", "Both")):
            total[k] += got[k]
            c = by_route.cell(row=r, column=col, value=got[k])
            style_from(c, body_ref["A5"])
            c.alignment = Alignment(horizontal="center", vertical="top")
        c = by_route.cell(row=r, column=5, value=sum(got.values()))
        style_from(c, body_ref["A5"])
        c.alignment = Alignment(horizontal="center", vertical="top")
    assert total == {"In": 20, "Out": 12, "Both": 4}, total
    c = by_route.cell(row=10, column=1)  # "Total" label is the source value, keep it
    for col, v in zip((2, 3, 4, 5), (20, 12, 4, 36)):
        cell = by_route.cell(row=10, column=col, value=v)
        style_from(cell, c)
        cell.font = copy(c.font)
        cell.alignment = Alignment(horizontal="center", vertical="top")

    # ------------------------------------------------------------ Key
    key = wb["Key"]
    assert key.max_row == 27
    key_rows = [
        ("Service", "P1 to P10, S1 to S9 and PLT",
         "The owning service of the path, from the Microservice Ownership Map v1 and the Architecture v5 service "
         "catalogue (D-RCV-60; ADR-013, ADR-014). Every row of the Disposition and Interfaces sheets carries one; "
         "where a source row spans several interfaces the cell names one service per interface."),
        ("Owner", "Workbench (read as per service)",
         "v3 names the single Workbench. In this version each Workbench path is owned by the service in the Service "
         "column (D-RCV-60; ASM-B-TECH-16-3)."),
        ("Owner", "ACE team (read as the ingest path)",
         "The ACE team keeps the ingestion, the checks and the 30 read-only v_ace_* views; rwb-source-data is the only "
         "reader of the views, so the Workbench side of every inbound ACE path is P1 (ADR-010)."),
        ("Owner", "Bank platform (read as the endpoint)",
         "The endpoint stays with the bank platform; the Workbench side of INT-23 is P10 rwb-agent (Architecture v5 "
         "slides 16 and 30)."),
        ("Interfaces", "INT-19, INT-20",
         "Kept in this version with the IDs of v3 because the inventory keeps every ID. Architecture v5 removes both "
         "under DP-17 and ADR-018 (no data lake), so no story is raised for them; open point CG-B-TECH-16-2 "
         "(ASM-B-TECH-16-4)."),
        ("Ruling", "Service column",
         "One rule per path group sits on the Service rules sheet, rows SR-01 to SR-19, with the slide, ADR or "
         "Ownership Map ruling behind each one."),
    ]
    for r, vals in enumerate(key_rows, start=28):
        for col, v in enumerate(vals, 1):
            c = key.cell(row=r, column=col, value=v)
            style_from(c, key.cell(row=27, column=col))
    key.auto_filter.ref = "A4:C33"

    # ------------------------------------------------------------ By service
    per = {code: {"In": 0, "Out": 0, "Both": 0, "ids": []} for code in ORDER}
    for r in range(5, 41):
        code = INT[itf.cell(row=r, column=1).value]
        per[code][itf.cell(row=r, column=4).value] += 1
        per[code]["ids"].append(itf.cell(row=r, column=1).value)
    by_svc = new_sheet("By service", "Interfaces by owning service",
                       "Calculated from the Service column of the Interfaces tab.",
                       ["Service code", "Service", "Name", "Wave", "In", "Out", "Both", "Total", "Interfaces"],
                       [13, 20, 22, 7, 7, 7, 7, 8, 70])
    rows, t_col = [], {"In": 0, "Out": 0, "Both": 0}
    for code in ORDER:
        d = per[code]
        if not sum((d["In"], d["Out"], d["Both"])):
            continue
        for k in t_col:
            t_col[k] += d[k]
        rows.append((code if code != "PLT" else "PLT", SHOW[code].split(" ", 1)[1], NAME.get(code, "Platform observability"),
                     WAVE.get(code, 0), d["In"], d["Out"], d["Both"], sum((d["In"], d["Out"], d["Both"])),
                     ", ".join(d["ids"])))
    assert t_col == {"In": 20, "Out": 12, "Both": 4}, t_col
    fill(by_svc, 5, rows, 9)
    tot_row = 5 + len(rows)
    fill(by_svc, tot_row, [("Total", "", "", "", 20, 12, 4, 36, "36 numbered interfaces")], 9)
    for col in range(5, 9):
        by_svc.cell(row=tot_row, column=col).font = copy(hdr_font)
    by_svc.auto_filter.ref = f"A4:I{5 + len(rows) - 1}"
    by_svc.column_dimensions["D"].alignment = Alignment(horizontal="center")

    # ------------------------------------------------------------ Service rules
    rules = [
        ("SR-01", "Inbound ACE source read through a recovery.v_ace_* view", "P1 rwb-source-data",
         "INT-01, INT-02, INT-04 to INT-13, INT-15, INT-16, INT-30, INT-35, INT-36",
         "ADR-010; Architecture v5 slides 7, 9, 15 and 29: only rwb-source-data reads the 30 recovery.v_ace_* views, "
         "every other service asks it through REST or a Temporal activity (ASM-B-TECH-16-6)."),
        ("SR-02", "Booking the officer makes in the core bank", "P8 rwb-payment", "INT-03",
         "Architecture v5 slide 17: rwb-payment owns payment and proceeds matching, fees, bookings and posting files; "
         "the disposition row keeps the officer booking in the core bank (ASM-B-TECH-16-8)."),
        ("SR-03", "Registered mail letters (WIN)", "P6 rwb-comms, with P2 rwb-integration for the file", "INT-14",
         "Architecture v5 slide 17 (rwb-comms: generate letter; Integration: deliverFile) and slide 30 (5); "
         "Ownership Map v1 ruling JOB-10 (16:00 window); ASM-B-TECH-16-7."),
        ("SR-04", "SMS and LINE messages to customers", "P6 rwb-comms", "INT-17, INT-18",
         "Architecture v5 slide 17 (ACE Common notification path: SMS, LINE) and slide 30 (5)."),
        ("SR-05", "Sign-in and the roles a user holds", "P4 rwb-access", "INT-21",
         "Architecture v5 slide 14 (rwb-access: sign-in, group-to-role) and slide 30 (1); the ACE team keeps the "
         "Entra path."),
        ("SR-06", "Audit and personal-data access logs", "PLT RWB-PLT-OBS", "INT-22",
         "Architecture v5 slide 30 (2) and slide 23: every service sends audit and personal-data access logs through "
         "the ACE PII Kafka path; the platform capability owns the sender."),
        ("SR-07", "Enterprise AI model endpoint", "P10 rwb-agent", "INT-23",
         "Architecture v5 slide 16 (rwb-agent: Enterprise AI endpoint, HTTPS private endpoint) and slides 6 and 8."),
        ("SR-08", "Partner portal and the results partners report", "S9 rwb-partner", "INT-24",
         "Architecture v5 slide 8 (partner gateway, FAPI 2.0, in front of rwb-partner) and slide 17; "
         "ASM-B-TECH-16-11."),
        ("SR-09", "Debt-buyer data tape for an awarded lot", "S6 rwb-debtsale, with P2 rwb-integration for the file",
         "INT-25", "Service Catalog v1, S6 file contract; Architecture v5 slide 17 (Integration: deliverFile, buyer "
         "file); ASM-B-TECH-16-7."),
        ("SR-10", "Reporting and model-learning output", "P9 rwb-reporting", "INT-19, INT-20",
         "ADR-018 and Architecture v5 slide 15 (rwb-reporting: measures, snapshots, regulatory reports; "
         "deliverFile for the extract); DP-17 removes the data lake. CG-B-TECH-16-2."),
        ("SR-11", "Credit approval request for a restructure plan", "P2 rwb-integration", "INT-26",
         "Architecture v5 slide 16 (interface config, file runs, outbound items, ACE integration paths); API "
         "Specification v4 GET /treatments/{treatmentId}/credit-pack, x-module P2."),
        ("SR-12", "Listing, vehicle transfer and NPA work order", "S5 rwb-asset", "INT-27, INT-28, INT-32",
         "Architecture v5 slide 19 (rwb-asset: assets taken on, holding, floor price, listings, auction rounds)."),
        ("SR-13", "Guarantee quota and claim", "S3 rwb-guarantee", "INT-29",
         "Architecture v5 slide 18 (rwb-guarantee: TCG and insurance claims, guarantor notices and pursuit)."),
        ("SR-14", "Litigation, enforcement and court records", "S4 rwb-litigation, with S9 rwb-partner for the entry",
         "INT-33", "Architecture v5 slide 19 (rwb-litigation: legal actions, hearings, judgments, enforcement) and "
         "slide 17 (partners enter through the partner gateway)."),
        ("SR-15", "Deviation screening and handling", "S8 rwb-deviation", "INT-31",
         "Architecture v5 slide 15 (rwb-deviation: X1-X7 screening, pause, handling, return)."),
        ("SR-16", "Approval of a recovery decision", "P7 rwb-decision", "Disposition: Email approvals in Outlook",
         "Architecture v5 slide 14 (rwb-decision: approvals, central decision ledger); DP-03."),
        ("SR-17", "Recovery documents and originals custody", "P5 rwb-document",
         "Disposition: Shared folders of scanned documents; EasyApp signed file",
         "Architecture v5 slide 16 (rwb-document: metadata, custody, OCR, signatures, retention)."),
        ("SR-18", "Open recovery work trackers", "P1 rwb-source-data",
         "Disposition: Recovery team spreadsheets and SharePoint lists",
         "API Specification v4 /admin/trackers, x-module P1; trackers leave system scope (D-RCV-35 U5)."),
        ("SR-19", "ACE Common shared services", "P2 rwb-integration", "INT-34",
         "Architecture v5 slide 7 (ACE Common, INT-34) and slide 30 (1) to (6): sign-in, logging, shared case view, "
         "restructure calculator, notification path and shared entities; rwb-integration owns the interface "
         "configuration and the ACE integration paths (ASM-B-TECH-16-12)."),
    ]
    srs = new_sheet("Service rules", "Service rules for the Service column",
                    "One rule per path group: the service it gives and the source behind it (D-RCV-60).",
                    ["Rule", "Path group", "Service", "Rows covered", "Basis"], [9, 42, 34, 44, 70])
    fill(srs, 5, rules, 5)
    srs.auto_filter.ref = f"A4:E{4 + len(rules)}"

    # ------------------------------------------------------------ Realignment changes
    changes = [
        ("R-01", "All sheets", "Four sheets and no header or change log",
         "Read me sheet first: header lines 1 and 2, document control, change-log row, what the version holds, "
         "counts, sources and open points", "D-RCV-60", "none", "Template and Rules v1 R8.1 and R8.2"),
        ("R-02", "Disposition", "No Service column; Owner was the ACE team, the Workbench or the bank platform",
         "Service column added after Owner and filled on 25 of 25 rows from the Microservice Ownership Map v1",
         "ADR-013, ADR-014, DL44", "DP-01, DP-05",
         "Ownership Map v1 sheet Services; Architecture v5 slides 13 to 20 and 41"),
        ("R-03", "Interfaces", "No Service column; Owner was the ACE team, the Workbench or the bank platform",
         "Service column added after Owner and filled on 36 of 36 rows from the Microservice Ownership Map v1",
         "ADR-013, ADR-014, DL44", "DP-05, DP-11, DP-16",
         "Ownership Map v1 sheet Services; Architecture v5 slides 15 to 20, 29 and 30; ADR-010"),
        ("R-04", "Interfaces", "The Workbench was one owner for every inbound and outbound path",
         "17 inbound rows owned by P1 rwb-source-data, the only reader of the recovery.v_ace_* views",
         "ADR-010", "DP-01, DP-05", "Architecture v5 slides 7, 9, 15 and 29"),
        ("R-05", "Interfaces", "INT-14, INT-17 and INT-18 owned by the Workbench",
         "P6 rwb-comms owns INT-14, INT-17 and INT-18; P2 rwb-integration builds and transfers the WIN file",
         "ADR-013", "DP-11, DP-16",
         "Architecture v5 slides 17, 30 (5) and 44 JOB-10; Ownership Map v1 ruling JOB-10"),
        ("R-06", "Interfaces", "INT-19 and INT-20 nightly to the data lake and Power BI, owned by the Workbench",
         "Both IDs kept as written and owned by P9 rwb-reporting; no story is raised for them "
         "(CG-B-TECH-16-2)", "ADR-018, DL44", "DP-17",
         "Architecture v5 slides 2, 7, 9 and 37; Template and Rules v1 R5.5 DP-17"),
        ("R-07", "Interfaces",
         "INT-21, INT-22, INT-23, INT-24, INT-25, INT-34, INT-35 and INT-36 owned by the ACE team, the Workbench or "
         "the bank platform",
         "The same owners, with the Workbench side named: P4, PLT (RWB-PLT-OBS), P10, S9, S6, P2, P1 and P1",
         "ADR-013, ADR-019, ADR-023", "DP-05, DP-08, DP-16, DP-20",
         "Architecture v5 slides 7, 8, 14, 16, 17 and 30"),
        ("R-08", "Disposition", "Every system row had one Owner and no service",
         "Every row carries the owning service of its data path; nine rows name one service per interface because the "
         "source row spans several", "ADR-013, DL46", "DP-01, DP-05, DP-11",
         "Ownership Map v1 sheet Services; Architecture v5 slides 13 to 20"),
        ("R-09", "By route",
         "Six route rows with every count cell empty although the sheet says it is calculated from the Interfaces tab",
         "In, Out, Both and Total calculated from the 36 interfaces: 20 In, 12 Out, 4 Both, 36 Total",
         "D-RCV-60", "none", "v3 sheet Interfaces, columns Direction and Route; CG-B-TECH-16-1"),
        ("R-10", "By service", "Sheet not present",
         "New sheet: the 36 interfaces counted per owning service, with the interfaces of each service named",
         "D-RCV-60", "none", "The Service column of this version"),
        ("R-11", "Key", "23 key rows (rows 5 to 27)",
         "The same 23 rows plus six: Service, the three readings of the Owner column, the two interface IDs "
         "Architecture v5 removes, and the pointer to the Service rules", "D-RCV-60", "none",
         "ASM-B-TECH-16-14"),
        ("R-12", "Service rules", "Sheet not present",
         "New sheet: 19 rules, one per path group, with the service and the slide, ADR or ruling behind it",
         "D-RCV-60", "none", "Architecture v5 slides 7 to 20, 29, 30 and 41; ADR-010"),
        ("R-13", "Workbook properties", "The author and last-modified-by properties carried a person name",
         "Henka Group and T3 Code / OpenCode / DeepSeek v4.1 Flash; title v4; dated 22 November 2026",
         "D-RCV-60", "none", "Root AGENTS.md rule 4; ASM-B-TECH-16-15"),
        ("R-14", "All sheets", "No other value changed",
         "Every other cell of the 25 disposition rows and the 36 interface rows is unchanged, checked cell by cell",
         "D-RCV-60", "none", "ASM-B-TECH-16-14"),
    ]
    rc = new_sheet("Realignment changes", "Realignment changes in v4 (D-RCV-60)",
                    "One row per change: the v3 value, the v4 value, the decision, the pattern and the basis.",
                    ["Ref", "Sheet", "v3 value", "v4 value", "Decision", "Pattern", "Basis"],
                    [8, 20, 46, 58, 22, 20, 60])
    fill(rc, 5, changes, 7)
    rc.auto_filter.ref = f"A4:G{4 + len(changes)}"

    # ------------------------------------------------------------ Read me
    readme = wb.create_sheet("Read me", 0)
    readme.column_dimensions["A"].width = 165
    lead = 15
    counts = {c: per[c]["In"] + per[c]["Out"] + per[c]["Both"] for c in ORDER}
    disp_codes = set()
    multi = 0
    for v in DISP.values():
        codes = [p.split(" ")[0] for p in v.split(";")]
        disp_codes.update(codes)
        multi += len(codes) > 1
    lead_p1 = sum(1 for v in DISP.values() if v.startswith("P1 "))
    all_codes = [c for c in ORDER if counts[c] or c in disp_codes]
    missing = [LABEL[c] for c in ORDER if c not in all_codes]
    assert lead_p1 == 15 and multi == 9, (lead_p1, multi)
    assert counts["P1"] == 17 and counts["P6"] == 3 and counts["S5"] == 3, counts
    assert missing == ["P3 rwb-case", "S1 rwb-valuation", "S2 rwb-treatment", "S7 rwb-writeoff"], missing
    int_line = ("36 interfaces: P1 rwb-source-data owns 17, P6 rwb-comms 3, S5 rwb-asset 3, P2 rwb-integration 2, "
                "P9 rwb-reporting 2, and P4 rwb-access, P8 rwb-payment, P10 rwb-agent, PLT (RWB-PLT-OBS), S3 "
                "rwb-guarantee, S4 rwb-litigation, S6 rwb-debtsale, S8 rwb-deviation and S9 rwb-partner 1 each.")
    rows = [
        (H1, "title"), (H2, "body"), ("", None),
        ("Recovery Workbench System Disposition and Integration Inventory v4. Decision D-RCV-60. Next version of "
         "Recovery Workbench System Disposition and Integration Inventory v3 (15 November 2026).", "title"),
        ("The 25 systems and tools that recovery uses today and the 36 numbered interfaces with the 32 systems behind "
         "them: what happens to each path, who owns the data path and when, the route, the data product and the "
         "standard. Every section, ID, number and date of v3 is kept. The realignment adds one Service column to the "
         "Disposition and Interfaces sheets and fills it for every row from the Microservice Ownership Map v1; the By "
         "route counts are calculated, and a By service sheet, the Service rules and the Realignment changes are "
         "added.", "body"),
        ("Tool: " + TOOL + ".", "body"),
        ("Status: Draft. This document is issued with no approval recorded (ASM-B-TECH-16-1).", "body"),
        ("Release: the paths are delivered across waves 1 to 4 of the Microservice Ownership Map v1. No release date "
         "appears in v3 and none is added; any release date written into this workbook later is tentative (Template "
         "and Rules v1 R1 U7; DL48).", "body"),
        ("", None),
        ("Change log", "sub"),
        ("v4, 22 November 2026, D-RCV-60 microservice realignment, " + TOOL, "body"),
        ("v3, 15 November 2026 (the source of this version; it is not changed by this run).", "body"),
        ("", None),
        ("What this version holds", "sub"),
        ("Disposition: the 25 systems and tools of v3, one row each, with Role in recovery today, Disposition, In ACE "
         "today, Owner, What the Workbench does with it, From, Interfaces and Decision unchanged; one Service column "
         "added after Owner and filled on 25 of 25 rows.", "body"),
        ("Interfaces: the 36 numbered interfaces of v3, one row each, with System, What the Workbench uses it for, "
         "Direction, Route, Path, Frequency, Data product, In ACE today, Owner, First needed, Standard and Decision "
         "unchanged; one Service column added after Owner and filled on 36 of 36 rows.", "body"),
        ("By route: the six rows of v3 (COLLINS, File, Direct through ACE, Through partners, Not at all today and "
         "Total) with the In, Out, Both and Total counts calculated from the 36 interfaces. v3 left every count cell "
         "empty although the sheet says it is calculated (CG-B-TECH-16-1; ASM-B-TECH-16-2).", "body"),
        ("By service: new sheet. The 36 interfaces counted per owning service, calculated from the Service column, "
         "with the interfaces of each service named.", "body"),
        ("Key: the 23 key rows of v3 unchanged, plus six rows for the Service column, the per-service reading of the "
         "Owner column, the two interface IDs that Architecture v5 removes, and the pointer to the Service rules.",
         "body"),
        ("Service rules: new sheet. One rule per path group with the service it gives and the slide, ADR or Ownership "
         "Map ruling behind it.", "body"),
        ("Realignment changes: new sheet. Every change of this version with the v3 value, the v4 value, the decision, "
         "the pattern and the basis.", "body"),
        ("", None),
        ("Counts", "sub"),
        (f"25 systems and tools: 25 Service cells filled; {lead_p1} rows lead with P1 rwb-source-data and {multi} name "
         "more than one service because the source row spans more than one interface.", "body"),
        (int_line, "body"),
        ("2 interface IDs kept although Architecture v5 removes them: INT-19 (data lake and Power BI) and INT-20 "
         "(COLLINS model learning).", "body"),
        (f"{len(all_codes)} of the 20 owner entries own at least one row: the 19 services and the platform "
         f"observability set, less {', '.join(missing)} (CG-B-TECH-16-3; ASM-B-TECH-16-13).", "body"),
        ("", None),
        ("Sources", "sub"),
        ("Recovery Workbench System Disposition and Integration Inventory v3.xlsx (15 November 2026), sheets "
         "Disposition, Interfaces, By route and Key.", "body"),
        ("Recovery Workbench System Disposition and Integration Inventory v2.xlsx (3 November 2026), sheet By route, "
         "read only to confirm that the counts were blank there too.", "body"),
        ("Recovery Workbench Microservice Ownership Map v1, sheets Services, Tables, Endpoints and Jobs, and "
         "_work/msr/plan/ownership.json.", "body"),
        ("Recovery Workbench Architecture v5 Text Extract v1, slides 2, 6, 7, 8, 9, 13 to 20, 23, 29, 30, 37, 41, 44 "
         "and 45.", "body"),
        ("Recovery Workbench Temporal and Drools Design Text Extract v1 (one transaction, decision record, points of "
         "no return).", "body"),
        ("Recovery Workbench Microservice Story Template and Rules v1 R1 (U2, U5, U7), R3 (R-PREC and the default "
         "rulings), R5.5 (DP-01, DP-05, DP-11, DP-16, DP-17, DP-18), R8.1, R8.2 and R9.", "body"),
        ("_work/msr/plan/ids.json: ADR-013 to ADR-023 and DL44 to DL49 are the decisions of this run.", "body"),
        ("", None),
        ("Open points", "sub"),
        ("INT-19 and INT-20 stay in this workbook with the IDs of v3 while Architecture v5 removes them; no story is "
         "raised for either (CG-B-TECH-16-2; ASM-B-TECH-16-4).", "body"),
        ("The source names no owning service for any system or interface; the Service column is derived from the "
         "Ownership Map and the Architecture v5 catalogue and the rule behind each group sits on the Service rules "
         "sheet (CG-B-TECH-16-4; ASM-B-TECH-16-3).", "body"),
        ("The data product of INT-06 reads To confirm in v3 and is kept as written (CG-B-TECH-16-5; "
         "ASM-B-TECH-16-5).", "body"),
        ("INT-33 has no standard in v3 and two candidate services, S4 and S9 (CG-B-TECH-16-6; ASM-B-TECH-16-9).",
         "body"),
        ("Three statements of v3 are kept word for word although they read as outdated: the Interfaces description "
         "says the Workbench owns the reporting feeds, the Disposition description says the workbook supersedes v2, "
         "and the partner portal row says the external gateway (CG-B-TECH-16-7; CG-B-TECH-16-8; ASM-B-TECH-16-10; "
         "ASM-B-TECH-16-11).", "body"),
        ("No date is raised by this workbook: no release date appears in the source (ASM-B-TECH-16-16).", "body"),
    ]
    for r, (text, kind) in enumerate(rows, start=1):
        c = readme.cell(row=r, column=1, value=text)
        if kind == "title":
            c.font = copy(title_font)
        elif kind == "sub":
            c.font = Font(name="Aptos", size=10, bold=True, color=PURPLE)
        elif kind == "body":
            c.font = Font(name="Aptos", size=10, color=GREY)
            c.alignment = Alignment(wrap_text=True, vertical="top")
    _ = lead

    # ------------------------------------------------------------ properties
    p = wb.properties
    p.creator = "Henka Group"
    p.lastModifiedBy = TOOL
    p.title = "Recovery Workbench System Disposition and Integration Inventory v4"
    p.subject = "D-RCV-60 microservice realignment"
    p.description = "Next version of the System Disposition and Integration Inventory v3; Service column added."
    p.revision = 4
    p.created = p.created
    p.modified = datetime(2026, 11, 22)

    wb.active = 0
    wb.save(OUT)
    print("WROTE", OUT)
    print("sheets", wb.sheetnames)


if __name__ == "__main__":
    main()
