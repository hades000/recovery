"""B-BIZ-36 — build Recovery Workbench Feature List v5.xlsx from the v4 copy.

Run after:  python -I "22 Microservice Realignment/compat/office_write.py" copy
              "02 Business architecture and process/Recovery Workbench Feature List v4.xlsx"
              "02 Business architecture and process/Recovery Workbench Feature List v5.xlsx"

Adds (never edits the source):
  - a first "Read me" sheet carrying the R8.1 header, the change log and the notes
  - Features columns O and P: Service (D-RCV-60), Service epic (D-RCV-60)
  - "(tentative)" on every release date on Features and By epic
  - By module columns H and I: the same two columns
  - Key: two new Column rows
"""
import json
import sys
from copy import copy
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr" / "docs" / "B-BIZ-36"
TARGET = ROOT / "02 Business architecture and process" / "Recovery Workbench Feature List v5.xlsx"
SRC = ROOT / "02 Business architecture and process" / "Recovery Workbench Feature List v4.xlsx"

SERVICES = {  # code: (short name, wave)  -- Microservice Ownership Map v1, Services sheet
    "P1": ("rwb-source-data", 1), "P2": ("rwb-integration", 1), "P3": ("rwb-case", 1),
    "P4": ("rwb-access", 1), "P5": ("rwb-document", 1), "P6": ("rwb-comms", 1),
    "P7": ("rwb-decision", 1), "P8": ("rwb-payment", 2), "P9": ("rwb-reporting", 1),
    "P10": ("rwb-agent", 1), "S1": ("rwb-valuation", 3), "S2": ("rwb-treatment", 2),
    "S3": ("rwb-guarantee", 3), "S4": ("rwb-litigation", 3), "S5": ("rwb-asset", 2),
    "S6": ("rwb-debtsale", 3), "S7": ("rwb-writeoff", 4), "S8": ("rwb-deviation", 2),
    "S9": ("rwb-partner", 4),
}

HDR_SERVICE = "Service (D-RCV-60)"
HDR_EPIC = "Service epic (D-RCV-60)"


def service_of(code):
    short, wave = SERVICES[code]
    return f"{code} {short}", f"RWB-SVC-{code}", wave


def clone_style(src, dst):
    dst.font = copy(src.font)
    dst.fill = copy(src.fill)
    dst.border = copy(src.border)
    dst.alignment = copy(src.alignment)
    dst.number_format = src.number_format
    dst.protection = copy(src.protection)


def build_readme(wb):
    ws = wb.create_sheet("Read me", 0)
    ws.column_dimensions["A"].width = 155
    bold = ("Read me", "Recovery Workbench Feature List v5", "Change log",
            "What changed in v5", "What did not change", "Counts", "Open points")
    rows = [l for l in (WORK / "readme.md").read_text(encoding="utf-8").splitlines()]
    r = 1
    after_heading = False
    for line in rows:
        text = line[3:].strip() if line.startswith("## ") else line.strip()
        if not text:
            if not after_heading:
                r += 1
            continue
        after_heading = line.startswith("## ")
        if True:
            ws.cell(r, 1, text)
            if text in bold:
                ws.cell(r, 1).font = openpyxl.styles.Font(bold=True, size=12 if text not in ("Change log",) else 11)
            else:
                ws.cell(r, 1).alignment = openpyxl.styles.Alignment(wrap_text=False)
        r += 1
    for w in ("A",):
        pass
    ws.sheet_view.showGridLines = True
    return ws


def main():
    if not TARGET.exists():
        sys.exit(f"missing copy: {TARGET} (run office_write.py copy first)")
    wb = openpyxl.load_workbook(TARGET)

    # ---------- Features ----------
    ws = wb["Features"]
    assert ws.max_row == 382 and ws.max_column == 14, (ws.max_row, ws.max_column)
    for col, head in ((15, HDR_SERVICE), (16, HDR_EPIC)):
        c = ws.cell(4, col, head)
        clone_style(ws.cell(4, 14), c)
        c.font = copy(ws.cell(4, 14).font)
        c.font = openpyxl.styles.Font(bold=True)
    ws.column_dimensions["O"].width = 24
    ws.column_dimensions["P"].width = 18
    ws.auto_filter.ref = "A4:P382"
    n_feat = 0
    for r in range(5, 383):
        code = ws.cell(r, 2).value
        if not code:
            continue
        svc, epic, _wave = service_of(str(code).strip())
        for col, val in ((15, svc), (16, epic)):
            c = ws.cell(r, col, val)
            clone_style(ws.cell(r, 14), c)
        rel = ws.cell(r, 12)
        if rel.value and "(tentative)" not in str(rel.value):
            rel.value = f"{rel.value} (tentative)"
        n_feat += 1

    # ---------- By module ----------
    wsm = wb["By module"]
    for col, head in ((8, HDR_SERVICE), (9, HDR_EPIC)):
        c = wsm.cell(4, col, head)
        clone_style(wsm.cell(4, 7), c)
        c.font = openpyxl.styles.Font(bold=True)
    wsm.column_dimensions["H"].width = 24
    wsm.column_dimensions["I"].width = 18
    wsm.auto_filter.ref = "A4:I23"
    n_mod = 0
    for r in range(5, 24):
        code = wsm.cell(r, 1).value
        if str(code) not in SERVICES:
            continue
        svc, epic, _wave = service_of(str(code))
        for col, val in ((8, svc), (9, epic)):
            c = wsm.cell(r, col, val)
            clone_style(wsm.cell(r, 7), c)
        n_mod += 1

    # ---------- By epic ----------
    wse = wb["By epic"]
    n_ep = 0
    for r in range(5, 13):
        c = wse.cell(r, 2)
        if c.value and "(tentative)" not in str(c.value):
            c.value = f"{c.value} (tentative)"
            n_ep += 1

    # ---------- Key ----------
    wsk = wb["Key"]
    wsk.insert_rows(12, 2)
    new = [
        ("Column", HDR_SERVICE,
         "The service that owns the feature, from the Microservice Ownership Map v1: the code and short name "
         "of the service of the row's module (P1 rwb-source-data, S9 rwb-partner). One service per module, "
         "as Architecture v5 splits Recovery into one service per business module."),
        ("Column", HDR_EPIC,
         "The service epic of Template and Rules R4 and R5.1 that the feature is delivered under: RWB-SVC-P1 "
         "to RWB-SVC-S9. The wave of the service is not a column; it is held against the service in the "
         "Ownership Map and the Read me sheet."),
    ]
    for i, (a, b, c) in enumerate(new):
        r = 12 + i
        wsk.cell(r, 1, a).font = copy(wsk.cell(11, 1).font)
        wsk.cell(r, 2, b).font = copy(wsk.cell(11, 2).font)
        cell = wsk.cell(r, 3, c)
        cell.alignment = copy(wsk.cell(11, 3).alignment)
        cell.font = copy(wsk.cell(11, 3).font)

    # ---------- Read me ----------
    build_readme(wb)
    wb.active = 0
    wb.save(TARGET)
    print(json.dumps({"features": n_feat, "modules": n_mod, "epic_releases": n_ep}))


if __name__ == "__main__":
    main()
