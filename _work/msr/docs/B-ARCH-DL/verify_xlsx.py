import re
from pathlib import Path

import openpyxl

SRC = Path(r"01 Decisions and governance\Recovery Workbench Decision Log v10.xlsx")
OUT = Path(r"01 Decisions and governance\Recovery Workbench Decision Log v11.xlsx")
wb = openpyxl.load_workbook(OUT)

# 1. no person names anywhere (content and properties)
NAME = re.compile(r"\bK\.\s*[A-Z][a-z]+\b")
bad = []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and NAME.search(c.value):
                bad.append(f"{ws.title}!{c.coordinate}: {c.value[:70]}")
print("person-name hits:", bad)
pr = wb.properties
print("props:", pr.creator, "|", pr.lastModifiedBy, "|", pr.title, "|", pr.description)
for attr in ("creator", "lastModifiedBy", "title", "description", "subject", "keywords", "category"):
    v = getattr(pr, attr) or ""
    if NAME.search(v):
        print("NAME IN PROPERTY", attr, v)

# 2. every v10 ID, count and date still present
src = openpyxl.load_workbook(SRC)
for name in ("Open decisions", "Decisions taken", "By owner"):
    s, o = src[name], wb[name]
    s_ids = [str(s.cell(r, 1).value).strip() for r in range(6, s.max_row + 1)]
    o_ids = [str(o.cell(r, 1).value).strip() for r in range(6, o.max_row + 1)]
    print(name, "v10 ids", len(s_ids), "v11 ids", len(o_ids),
          "missing:", [i for i in s_ids if i not in o_ids])
    s_dates = [s.cell(r, 3).value for r in range(6, s.max_row + 1)] if name != "By owner" else []
    o_dates = [o.cell(r, 3).value for r in range(6, o.max_row + 1)] if name != "By owner" else []
    print("   dates preserved:", s_dates == o_dates[:len(s_dates)])

od, dt, bo = wb["Open decisions"], wb["Decisions taken"], wb["By owner"]
print("A2 open:", od["A2"].value[:60])
print("A2 taken:", dt["A2"].value[:60])
print("A2 owner:", bo["A2"].value[:80])
print("freeze:", od.freeze_panes, dt.freeze_panes, bo.freeze_panes,
      "| filters:", od.auto_filter.ref, dt.auto_filter.ref, bo.auto_filter.ref)
print("readme:", [wb["Read me"][f"A{i}"].value for i in (1, 2, 7, 8)])

# 3. new rows
for r in range(27, dt.max_row + 1):
    print(r, [str(dt.cell(r, c).value)[:60] for c in range(1, 6)], dt.cell(r, 3).number_format)

# 4. owner cells
for r in range(6, od.max_row + 1):
    v = od.cell(r, 6).value
    if isinstance(v, str) and len(v) > 60:
        print("OD", od.cell(r, 1).value, "->", v)

# 5. release-date marks
for r in range(6, od.max_row + 1):
    for c in range(1, 11):
        v = od.cell(r, c).value
        if isinstance(v, str) and "(tentative)" in v:
            print("TENT", od.cell(r, 1).value, od.cell(r, c).coordinate, v[:110])
