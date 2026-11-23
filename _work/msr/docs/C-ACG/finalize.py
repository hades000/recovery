"""Finalise the v2 AC Glossary: sheet order, core properties, widths, and verification."""
import hashlib
import openpyxl
from pathlib import Path

ROOT = Path.cwd()
SRC = ROOT / "04 User stories/Recovery Workbench Acceptance Criteria Glossary v1.xlsx"
DST = ROOT / "04 User stories/Recovery Workbench Acceptance Criteria Glossary v2.xlsx"

wb = openpyxl.load_workbook(DST)

# 1. Sheet order: Read me first, the explanation sheet last.
order = ["Read me", "Keywords", "Sentence frames", "Words", "Code prefixes", "Realignment additions"]
missing = [s for s in order if s not in wb.sheetnames]
extra = [s for s in wb.sheetnames if s not in order]
assert not missing and not extra, (missing, extra)
wb._sheets = [wb[s] for s in order]

# 2. Core properties: no name of a person anywhere.
p = wb.properties
p.creator = "SCB Collections and Recovery / Henka Group"
p.lastModifiedBy = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
p.title = "Recovery Workbench Acceptance Criteria Glossary v2"
p.subject = "D-RCV-60 microservice realignment"
p.description = ("Next version of Recovery Workbench Acceptance Criteria Glossary v1. Adds the acceptance criteria "
                 "origin tag, the contract mock Given and the -ITG test case suffix.")
p.category = "Acceptance criteria glossary"
p.keywords = "D-RCV-60; acceptance criteria; origin tag; contract fake; -ITG"
p.revision = 2

# 3. Readability of the two new sheets only; the four source sheets keep their own layout.
widths = {
    "Read me": {"A": 42, "B": 46, "C": 96, "D": 46},
    "Realignment additions": {"A": 46, "B": 62, "C": 96, "D": 52, "E": 44, "F": 42},
}
for sheet, cols in widths.items():
    ws = wb[sheet]
    for col, w in cols.items():
        ws.column_dimensions[col].width = w

wb.save(DST)
print("SAVED", DST)

# 4. Verification: the four source sheets are unchanged cell by cell, and the header and change log are in place.
src = openpyxl.load_workbook(SRC)
out = openpyxl.load_workbook(DST)
print("SHEETS", out.sheetnames)
diffs = 0
cells = 0
for s in ("Keywords", "Words"):
    a, b = src[s], out[s]
    assert (a.max_row, a.max_column) == (b.max_row, b.max_column), s
    for r in range(1, a.max_row + 1):
        for c in range(1, a.max_column + 1):
            cells += 1
            if a.cell(r, c).value != b.cell(r, c).value:
                diffs += 1
                print("DIFF", s, r, c, repr(a.cell(r, c).value), repr(b.cell(r, c).value))
for s in ("Sentence frames", "Code prefixes"):
    a, b = src[s], out[s]
    for r in range(1, a.max_row + 1):
        for c in range(1, a.max_column + 1):
            cells += 1
            if a.cell(r, c).value != b.cell(r, c).value:
                diffs += 1
                print("DIFF", s, r, c, repr(a.cell(r, c).value), repr(b.cell(r, c).value))
print("SOURCE CELLS COMPARED", cells, "DIFFERENCES", diffs)

rm = out["Read me"]
print("A1", repr(rm["A1"].value))
print("A2", repr(rm["A2"].value))
line = "v2, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
hit = [c.coordinate for row in rm.iter_rows() for c in row if c.value == line]
print("CHANGE-LOG LINE CELLS", hit)
for s in out.sheetnames:
    print(s, out[s].max_row, out[s].max_column)
print("SHASRC", hashlib.sha256(SRC.read_bytes()).hexdigest()[:16])
