# -*- coding: utf-8 -*-
"""Build Recovery Workbench Dependency Map v3 from v2."""
import copy, shutil, datetime
import openpyxl

SRC = r"11 Delivery and operations\Recovery Workbench Dependency Map v2.xlsx"
DST = r"11 Delivery and operations\Recovery Workbench Dependency Map v3.xlsx"

shutil.copyfile(SRC, DST)
wb = openpyxl.load_workbook(DST)
ws = wb["Dependencies"]

# ---- DEP-14 re-worded (D-RCV-35 U1: no Workbench load, read the ACE batch through the views)
for r in range(5, ws.max_row + 1):
    if ws.cell(r, 1).value == "DEP-14":
        ws.cell(r, 3).value = ("ACE ingestion of account, payment, customer and score data "
                               "complete for the business date, read through v_ace_account, "
                               "v_ace_payment, v_ace_customer and v_ace_score; no Workbench "
                               "load and no staging table")
        ws.cell(r, 8).value = ("No case can be opened from the ACE account view for the "
                               "business date")

# ---- two new rows
last = ws.max_row
style = {c: copy.copy(ws.cell(last, c)._style) for c in range(1, 10)}
new = [
    ["DEP-34", "ACE team",
     "RWB-ACE-001: 14 tables, 12 columns, one batch record per source and business date and "
     "the SELECT grant that the 30 recovery.v_ace_* views read",
     "E1", datetime.datetime(2026, 11, 21), "ACE team lead", "DL43",
     "RWB-E1-069 has only the 16 Section A views; the case list, the case record and the 12 "
     "ACE columns are missing, so the 30 November release moves", "Open"],
    ["DEP-35", "ACE team",
     "DL43: the ACE team's estimate and acceptance of RWB-ACE-001, with the 14 ingestion jobs "
     "and the migration window in the 30 November release named",
     "E1", datetime.datetime(2026, 11, 21), "Sponsor with the ACE team lead", "DL43",
     "The ACE additions have no committed date; the plan holds the 21 November assumption and "
     "moves if it slips", "Open"],
]
for i, vals in enumerate(new):
    r = last + 1 + i
    for c, v in enumerate(vals, 1):
        cell = ws.cell(r, c, v)
        cell._style = copy.copy(style[c])

ws["A2"] = ("35 dependencies on the ACE team, the collection squad, the architecture team, "
            "data engineering, SCB IT security, the AI teams, the business and the partners. "
            "DEP-34 and DEP-35 carry the ACE delivery and DL43, added on 15 November 2026.")

# ---- By team and epic, recomputed from the rows above
bt = wb["By team and epic"]
teams = [bt.cell(r, 1).value for r in range(5, 14)]
epics = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]
grid = {t: {e: 0 for e in epics} for t in teams}
for r in range(5, ws.max_row + 1):
    t = ws.cell(r, 2).value
    e = ws.cell(r, 4).value
    assert t in grid, t
    grid[t][e] += 1
for r in range(5, 14):
    t = bt.cell(r, 1).value
    for j, e in enumerate(epics):
        n = grid[t][e]
        bt.cell(r, 2 + j).value = n if n else None
    bt.cell(r, 10).value = sum(grid[t].values())
for j, e in enumerate(epics):
    bt.cell(14, 2 + j).value = sum(grid[t][e] for t in teams)
bt.cell(14, 10).value = sum(grid[t][e] for t in teams for e in epics)

wb.properties.title = "Recovery Workbench Dependency Map v3"
wb.properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
wb.save(DST)
print("saved", DST, "rows", ws.max_row - 4)
print({t: sum(grid[t].values()) for t in teams}, bt.cell(14, 10).value)
