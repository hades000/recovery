"""Append the D-RCV-60 realignment columns and sheets to the v4 workbook. Edits the copy only."""
import json
from pathlib import Path
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "06 Data" / "Recovery Workbench Party and Customer Master Data Design v4.xlsx"
DOCS = ROOT / "_work" / "msr" / "docs" / "B-DATA-22"

HEAD_FILL = PatternFill("solid", fgColor="DCD3EB")
HEAD_FONT = Font(bold=True, size=10)
BODY_FONT = Font(size=10)
WRAP = Alignment(wrap_text=True, vertical="top")

OWNER = {
    "case_party": ("P3", "rwb_case",
                   "Owned by rwb-case; no other service reads the table (DP-01). Served by GET /api/recovery/case/v1/cases/{id}."),
    "v_ace_customer": ("P1", "recovery (read-only)",
                       "Read-only view; SELECT by the rwb_source_data login only (DP-05). Served by GET /api/recovery/source-data/v1/customers/{id}."),
    "v_ace_contact": ("P1", "recovery (read-only)",
                      "Read-only view; SELECT by the rwb_source_data login only (DP-05). Served with the customer; payload coverage is open (CG-B-DATA-22-1)."),
    "v_ace_ca_relation": ("P1", "recovery (read-only)",
                          "Read-only view; SELECT by the rwb_source_data login only (DP-05). Served with the account; the consumer is open (CG-B-DATA-22-3)."),
    "party_ext": ("P1", "rwb_source_data",
                  "Owned by rwb-source-data (DP-01). Flags are served with the customer; the write operation is open (CG-B-DATA-22-2)."),
    "contact_point_ext": ("P1", "rwb_source_data",
                          "Owned by rwb-source-data (DP-01). Consent and history are served with the customer; the write operation is open (CG-B-DATA-22-2)."),
    "partner": ("S9", "rwb_partner",
                "Owned by rwb-partner; no other service reads the table (DP-01). Served by GET /api/recovery/partner/v1/partners."),
}
MATCH = {
    "M1": ("ACE ingestion; rwb-source-data view contract (v_ace_customer)", "P1"),
    "M2": ("ACE ingestion; rwb-source-data view contract (v_ace_customer)", "P1"),
    "M3": ("ACE ingestion; rwb-source-data view contract (v_ace_customer)", "P1"),
    "M4": ("ACE ingestion; rwb-source-data view contract (v_ace_customer)", "P1"),
    "M5": ("rwb-partner partner master (rwb_partner)", "S9"),
}


def head(ws, row, cols):
    for col in cols:
        c = ws.cell(row, col)
        c.font = HEAD_FONT
        c.fill = HEAD_FILL
        c.alignment = WRAP


def realign_party(ws):
    head(ws, 4, (8, 9, 10))
    ws.cell(4, 8, "Owning service")
    ws.cell(4, 9, "Target schema")
    ws.cell(4, 10, "Access rule")
    for r in range(5, ws.max_row + 1):
        ent = ws.cell(r, 1).value
        if ent not in OWNER:
            continue
        code, schema, rule = OWNER[ent]
        for col, val in ((8, code), (9, schema), (10, rule)):
            c = ws.cell(r, col, val)
            c.font = BODY_FONT
            c.alignment = WRAP
    for col, w in ((8, 10), (9, 24), (10, 78)):
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.auto_filter.ref = f"A4:J{ws.max_row}"


def realign_match(ws):
    head(ws, 4, (5, 6))
    ws.cell(4, 5, "Target component")
    ws.cell(4, 6, "Owning service")
    for r in range(5, ws.max_row + 1):
        rule = ws.cell(r, 1).value
        if rule not in MATCH:
            continue
        comp, code = MATCH[rule]
        for col, val in ((5, comp), (6, code)):
            c = ws.cell(r, col, val)
            c.font = BODY_FONT
            c.alignment = WRAP
    ws.column_dimensions["E"].width = 46
    ws.column_dimensions["F"].width = 12
    ws.auto_filter.ref = "A4:F9"


def rebuild_table(ws, title, blurb, widths):
    rows = [[ws.cell(r, c).value for c in range(1, ws.max_column + 1)] for r in range(1, ws.max_row + 1)]
    header, body = rows[0], rows[1:]
    ncol = len(header)
    ws.delete_rows(1, ws.max_row)
    ws.cell(1, 1, title).font = Font(bold=True, size=16)
    ws.cell(2, 1, blurb).font = BODY_FONT
    for c, val in enumerate(header, 1):
        cell = ws.cell(4, c, val)
    head(ws, 4, range(1, ncol + 1))
    for i, row in enumerate(body, 5):
        for c, val in enumerate(row, 1):
            cell = ws.cell(i, c, val)
            cell.font = BODY_FONT
            cell.alignment = WRAP
    for c, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:{get_column_letter(ncol)}{4 + len(body)}"


def style_readme(ws):
    ws.column_dimensions["A"].width = 132
    bold_rows = {4, 8, 11, 18, 22, 27, 31}
    for r in range(1, ws.max_row + 1):
        c = ws.cell(r, 1)
        c.alignment = Alignment(wrap_text=False, vertical="top")
        if r == 4:
            c.font = Font(bold=True, size=14)
        elif r in (1, 2):
            c.font = Font(size=10)
        elif r in bold_rows:
            c.font = Font(bold=True, size=10)
        else:
            c.font = Font(size=10)


def main():
    wb = openpyxl.load_workbook(OUT)
    realign_party(wb["Party fields"])
    realign_match(wb["Match rules"])
    rebuild_table(wb["Service ownership"], "Service ownership",
                  "One row per service that owns a table or a view in this design. Owners come from the Ownership Map v1 "
                  "(sheet Tables) and Architecture v5 slides 35, 37 and 41.", [8, 20, 26, 7, 20, 14, 52, 16, 96])
    rebuild_table(wb["Read paths"], "Read paths",
                  "How each consumer gets party data in the 19-service design. ACE party data is read only through "
                  "rwb-source-data; case_party belongs to rwb-case and the panel entry to rwb-partner.", [26, 44, 62, 10, 8, 78])
    style_readme(wb["Read me"])
    wb.move_sheet("Read me", offset=-wb.sheetnames.index("Read me"))
    p = wb.properties
    p.creator = "Recovery Workbench programme"
    p.lastModifiedBy = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
    p.title = "Recovery Workbench Party and Customer Master Data Design v4"
    p.subject = "D-RCV-60 microservice realignment"
    wb.active = 0
    wb.save(OUT)
    print("BUILT", OUT)
    print("sheets", wb.sheetnames)
    for name in wb.sheetnames:
        ws = wb[name]
        print(name, ws.dimensions, "freeze", ws.freeze_panes, "filter", ws.auto_filter.ref)


if __name__ == "__main__":
    main()
