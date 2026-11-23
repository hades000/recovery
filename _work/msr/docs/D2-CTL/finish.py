"""Finish the Document Control Sheet v13 workbook: header and change-log sheet,
a note on the Control sheet, summary ranges and the row style.

Writes only 12 Project communication/Recovery Workbench Document Control Sheet v13.xlsx.
"""
import json
from pathlib import Path
import openpyxl
from openpyxl.styles import Alignment, Font
from copy import copy

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
OUT = ROOT / "12 Project communication/Recovery Workbench Document Control Sheet v13.xlsx"
SCRATCH = ROOT / "_work/msr/docs/D2-CTL"
report = json.loads((SCRATCH / "rows_report.json").read_text(encoding="utf-8"))

wb = openpyxl.load_workbook(OUT)
ws = wb["Control sheet"]
first_new = 139              # first appended row (source rows are 5..138)
last_new = 138 + report["rows"]
assert ws.max_row == last_new, (ws.max_row, last_new)

# ---- 1. style the appended rows like the last source row
src_style_row = 138
for r in range(first_new, last_new + 1):
    for c in range(1, 12):
        s = ws.cell(src_style_row, c)
        d = ws.cell(r, c)
        d.font = copy(s.font)
        d.alignment = copy(s.alignment)
        d.border = copy(s.border)
        d.fill = copy(s.fill)
        d.number_format = s.number_format
    ws.row_dimensions[r].height = ws.row_dimensions[src_style_row].height

# ---- 2. the note under the title: keep the source sentence, add the v13 statement
note = ws.cell(2, 1)
old = note.value
add = (f" Document set v15 adds {report['rows']} rows, numbered {report['first']} to {report['last']}: "
       f"the realignment documents of D-RCV-60, each marked 'Document set v15' in the comments column, "
       f"so this sheet now controls {len(range(135, report['last'] + 1)) + 134} documents. "
       "The change log is on the sheet 'Change log'.")
if "Document set v15 adds" not in old:
    note.value = old.rstrip() + add

# ---- 3. filter and summary ranges reach the last row
ws.auto_filter.ref = f"A4:K{last_new}"
summ = wb["Summary"]
for row in summ.iter_rows():
    for cell in row:
        if isinstance(cell.value, str) and "$B$5:$B$136" in cell.value:
            cell.value = cell.value.replace("$B$5:$B$136", f"$B$5:$B${last_new}").replace(
                "$I$5:$I$136", f"$I$5:$I${last_new}")

# ---- 4. change-log sheet, first in the book
title = "Change log"
if title in wb.sheetnames:
    del wb[title]
cl = wb.create_sheet(title, 0)
rows = [
    ("SCB Collections and Recovery. Henka Group, 22 November 2026.",),
    ("(C) Siam Commercial Bank and Henka Pte Ltd",),
    (),
    ("Recovery Workbench Document Control Sheet v13 - change log",),
    (),
    ("v13, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash",),
    (),
    ("What v13 changes",),
    (f"161 rows are added to the Control sheet, numbered {report['first']} to {report['last']}, one row per "
     "document the D-RCV-60 microservice realignment issues or re-issues. Every one of the 134 source rows, "
     "its number, its document, its files, its reviewers and its comments are copied unchanged.",),
    ("Every added row is labelled 'Document set v15' in the comments column, and it carries the priority, "
     "layer and review roles of its own document family, so the priority bands and the Summary sheet stay comparable "
     "with v12.",),
    ("The Owner named in a comment is the owning service of the Recovery Workbench Microservice Ownership Map v1, "
     "for example P3 rwb-case. Roles are used everywhere; no person is named. The sheet keeps its 11 source columns "
     "and carries the owner in the comments column (CG-D2-CTL-2).",),
    ("The Summary sheet now counts rows 5 to 295. In v12 its formulas stopped at row 136 and left the last two "
     "source rows uncounted (CG-D2-CTL-5).",),
    ("Where a document is new there is no earlier row to copy: its priority, layer and review roles are taken from "
     "the nearest family, as recorded in the Assumptions Register (CG-D2-CTL-6).",),
    ("One row per document, with the files of that document in the Files column, follows the convention the 134 "
     "source rows already use; the 1065 story files are controlled as 31 rows, one per epic folder (CG-D2-CTL-3).",),
    ("The document index v14, the project hub v15, the team start pack v3 and the CTO presentation v4 are rows of "
     "this set; the index had not been written when this sheet was prepared (CG-D2-CTL-4).",),
    ("The project hub exists at v17 in folder 14 Story Updates under D-RCV-36, and the realignment file is v15 in "
     "folder 12 Project communication; both rows are kept (CG-D2-CTL-1).",),
    (),
    ("Source",),
    ("12 Project communication/Recovery Workbench Document Control Sheet v12.xlsx (read only, not edited)",),
]
for i, row in enumerate(rows, 1):
    if row:
        cl.cell(i, 1, row[0])
cl.column_dimensions["A"].width = 130
for r in (1, 2, 4, 6, 8):
    cl.cell(r, 1).font = Font(name="Aptos", size=10, bold=r in (4,)),
    cl.cell(r, 1).alignment = Alignment(wrap_text=True, vertical="top")
cl.cell(6, 1).font = Font(name="Aptos", size=10, bold=True)
cl.cell(1, 1).font = Font(name="Aptos", size=10)
cl.cell(2, 1).font = Font(name="Aptos", size=10)

# ---- 5. every sheet view starts at the top left
for s in wb.worksheets:
    s.sheet_view.selection[0].activeCell = "A1"
    s.sheet_view.selection[0].sqref = "A1"

wb.save(OUT)
print("SAVED", OUT, "rows", ws.max_row, "sheets", wb.sheetnames)
