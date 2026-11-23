"""Verify the two new workbooks against their sources: source cells unchanged, new columns filled, new rows sane."""
import sys, collections
from pathlib import Path
sys.path.insert(0, str(Path("22 Microservice Realignment/compat").resolve()))
import openpyxl
from common import ROOT

PAIRS = [("09 Testing and quality/Recovery Workbench Test Cases v7.xlsx", "Story test cases",
          "09 Testing and quality/Recovery Workbench Test Cases v8.xlsx", 14),
         ("09 Testing and quality/Recovery Workbench Test Cases v7.xlsx", "Rule test cases",
          "09 Testing and quality/Recovery Workbench Test Cases v8.xlsx", 10),
         ("09 Testing and quality/Recovery Workbench Regression Suite v6.xlsx", "Suite",
          "09 Testing and quality/Recovery Workbench Regression Suite v7.xlsx", 10)]

for src, sheet, out, ncol in PAIRS:
    a = openpyxl.load_workbook(ROOT / src, read_only=True, data_only=True)[sheet]
    b = openpyxl.load_workbook(ROOT / out, read_only=True, data_only=True)[sheet]
    ra = [r for r in a.iter_rows(values_only=True)]
    rb = [r for r in b.iter_rows(values_only=True)]
    diff = 0
    for i in range(len(ra)):
        x = ra[i][:ncol] + (None,) * max(0, ncol - len(ra[i]))
        y = rb[i][:ncol] + (None,) * max(0, ncol - len(rb[i]))
        if [str(v) if v is not None else "" for v in x] != [str(v) if v is not None else "" for v in y]:
            diff += 1
            if diff <= 3:
                print("  DIFF row", i + 1, [str(v)[:20] for v in x], [str(v)[:20] for v in y])
    print(f"{sheet}: source rows {len(ra)}, new rows {len(rb)}, source-cell diffs {diff}")
    wide = len(rb[3])
    print("  header width", wide, "new headers", [rb[3][i] for i in range(ncol, wide)])

# new-column fill and new-row sanity on the story sheet
wb = openpyxl.load_workbook(ROOT / "09 Testing and quality/Recovery Workbench Test Cases v8.xlsx", read_only=True, data_only=True)
rows = [r for r in wb["Story test cases"].iter_rows(min_row=5, values_only=True) if r[0]]
print("story rows", len(rows), "blank O/P/Q/R", sum(1 for r in rows if not all(r[14:18])))
new = [r for r in rows if str(r[17]).startswith("new, ")]
print("added", len(new), "by level", collections.Counter(r[16] for r in new).most_common())
print("added with blank Service/Story/Level", sum(1 for r in new if not r[14] or not r[15] or not r[16]))
print("added with blank Test/Expected/Data", sum(1 for r in new if not r[5] or not r[9] or not r[10]))
print("added ids unique", len({r[0] for r in new}) == len(new))

rs = openpyxl.load_workbook(ROOT / "09 Testing and quality/Recovery Workbench Regression Suite v7.xlsx", read_only=True, data_only=True)
srows = [r for r in rs["Suite"].iter_rows(min_row=5, values_only=True) if r[0]]
print("suite rows", len(srows), "blank K..N", sum(1 for r in srows if not all(r[10:14])),
      "added", sum(1 for r in srows if str(r[13]).startswith("new, ")))
print("sheets", wb.sheetnames, rs.sheetnames)
for name in ("Read me",):
    for w in (wb, rs):
        ws = w[name]
        print(name, w is wb and "TC" or "RS", "A1:", ws["A1"].value, "| A2:", ws["A2"].value)
