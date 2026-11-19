# -*- coding: utf-8 -*-
"""Build Recovery Workbench Build Sequence Epic 1 and Epic 2 v5 from v4."""
import copy, datetime, os, re, shutil
import openpyxl
from openpyxl.utils import get_column_letter

SRC = r"11 Delivery and operations\Recovery Workbench Build Sequence Epic 1 and Epic 2 v4.xlsx"
DST = r"11 Delivery and operations\Recovery Workbench Build Sequence Epic 1 and Epic 2 v5.xlsx"

shutil.copyfile(SRC, DST)
wb = openpyxl.load_workbook(DST)
ws = wb["Sequence"]

# ---- read v4 rows
rows = {}
order4 = []
for r in range(5, ws.max_row + 1):
    vals = [ws.cell(r, c).value for c in range(1, 12)]
    rows[vals[1]] = vals
    order4.append(vals[1])

DROP = {"RWB-E1-003", "RWB-E1-004", "RWB-E1-005", "RWB-E1-006",
        "RWB-E1-009", "RWB-E1-010", "RWB-E1-012", "RWB-E1-051", "RWB-E2-023"}

DEPENDS = {
    "RWB-E1-002": "RWB-E1-018, RWB-E1-069, RWB-E1-007, RWB-E1-020",
    "RWB-E1-007": "RWB-E1-001, RWB-E1-069",
    "RWB-E1-011": "RWB-E1-002, RWB-E1-015, RWB-E1-069",
    "RWB-E1-015": "RWB-E1-001, RWB-E1-069, RWB-E1-027",
    "RWB-E1-016": "RWB-E1-037, RWB-E1-001, RWB-E1-064, RWB-E1-069",
    "RWB-E1-018": "RWB-E1-016, RWB-E1-027, RWB-E1-042, RWB-E1-069",
    "RWB-E1-025": "RWB-E1-069",
    "RWB-E1-045": "RWB-E1-042, RWB-E1-043",
    "RWB-E1-046": "RWB-E1-001, RWB-E1-069",
    "RWB-E1-052": "RWB-E1-015, RWB-E1-027, RWB-E1-046, RWB-E1-069",
    "RWB-E1-058": "RWB-E1-001, RWB-E1-037",
    "RWB-E1-064": "RWB-E1-001, RWB-E1-043, RWB-E1-069",
    "RWB-E1-065": "RWB-E1-001, RWB-E1-069",
    "RWB-E2-001": "RWB-E1-069, RWB-E1-015, RWB-E1-007",
    "RWB-E2-003": "RWB-E1-069, RWB-E1-007",
    "RWB-E2-008": "RWB-E2-004, RWB-E1-069",
    "RWB-E2-034": ("RWB-E1-027, RWB-E2-016, RWB-E1-069, RWB-E1-007, RWB-E1-066, "
                   "RWB-E1-067, RWB-TE-006"),
}

TITLE = {"RWB-E1-007": "Integration adapters for outbound files",
         "RWB-E2-001": "EFS hand-over with full history"}

# E1-011 now needs E1-015, so the two swap places
SWAP = ("RWB-E1-011", "RWB-E1-015")

new_items = []
for k in order4:
    if k in DROP:
        continue
    v = list(rows[k])
    if k in TITLE:
        v[2] = TITLE[k]
    if k in DEPENDS:
        v[6] = DEPENDS[k]
    new_items.append(v)
    if k == "RWB-E1-001":
        new_items.append([None, "RWB-E1-069",
                          "Read-only ACE source views, grants and boundary rule",
                          "P1", "User story", "Must",
                          "RWB-E1-001, RWB-ACE-001",
                          "Window 1", "2 Nov to 13 Nov", "E1", "Yes"])

CRIT = {"RWB-E1-069", "RWB-E1-018", "RWB-E1-020", "RWB-E1-002", "RWB-E1-028",
        "RWB-E1-030", "RWB-E1-059", "RWB-E1-061", "RWB-E1-063",
        "RWB-E2-031", "RWB-E2-028", "RWB-E2-029"}
# swap E1-011 and E1-015 so E1-011 (which needs E1-015) comes second
i1 = next(i for i, v in enumerate(new_items) if v[1] == SWAP[0])
i2 = next(i for i, v in enumerate(new_items) if v[1] == SWAP[1])
new_items[i1], new_items[i2] = new_items[i2], new_items[i1]
for i, v in enumerate(new_items, 1):
    v[0] = i
    v[10] = "Yes" if v[1] in CRIT else None

# ---- rewrite Sequence rows, keeping the column styles of the old first body row
styles = {}
for c in range(1, 12):
    styles[c] = copy.copy(ws.cell(5, c)._style)
height5 = ws.row_dimensions[5].height

ws.delete_rows(5, ws.max_row - 4)
for i, v in enumerate(new_items):
    r = 5 + i
    for c in range(1, 12):
        cell = ws.cell(r, c, v[c - 1])
        cell._style = copy.copy(styles[c])
    ws.row_dimensions[r].height = height5

ws["A2"] = ("107 items. Delivery runs as Kanban (DT04): items are pulled in this order "
            "as capacity frees up. The two-week windows are the sponsor review points, not "
            "sprint boundaries. RWB-ACE-001, the ACE team's schema delivery, gates window 1 "
            "and is not pulled by either squad.")
ws.auto_filter.ref = "A4:K%d" % (4 + len(new_items))

# ---- By window
bw = wb["By window"]
counts = {}
for v in new_items:
    counts[v[7]] = counts.get(v[7], 0) + 1
for r in range(5, 10):
    w = bw.cell(r, 1).value
    bw.cell(r, 4).value = counts.get(w, 0)
bw.cell(10, 4).value = sum(counts.values())
bw["A2"] = ("Items expected to finish in each two-week window. Window 1 includes "
            "RWB-E1-069, which stays open until RWB-ACE-001 lands (21 November, DL43).")

# ---- Critical path
cp = wb["Critical path"]
cp.delete_rows(5, cp.max_row - 4)
cp["A1"] = "The chain that sets the release date"
cp["A2"] = ("13 items. RWB-ACE-001 gates RWB-E1-069, and RWB-E1-069 gates RWB-E1-018 and "
            "RWB-E1-002: a day lost on the ACE delivery or on the views moves the 30 November "
            "release. E1-069 also needs RWB-E1-001, the V0001 migration, built in window 1.")
cp["A4"] = "Step"
cp["B4"] = "Key"
cp["C4"] = "Title"
cp["D4"] = "Module"
cp["E4"] = "Window"
cp["F4"] = "Gated by"
hdr_style = copy.copy(cp.cell(4, 5)._style)
cell_style = copy.copy(cp.cell(5, 5)._style)
cp.cell(4, 6).value = "Gated by"
cp.cell(4, 6)._style = copy.copy(hdr_style)
cp.column_dimensions["F"].width = 28

chain = [
    ("1", "RWB-ACE-001", "ACE DB additions for the Recovery Workbench", "ACE", "Window 1",
     "None. ACE team; DL43, needed 21 November"),
    ("2", "RWB-E1-069", "Read-only ACE source views, grants and boundary rule", "P1", "Window 1",
     "RWB-ACE-001 (Section B); RWB-E1-001 (Section A)"),
    ("3", "RWB-E1-018", "Case ID issuance and case record v1", "P3", "Window 2",
     "RWB-E1-069, RWB-E1-016"),
    ("4", "RWB-E1-020", "Allocation and assignment engine v1", "P3", "Window 2",
     "RWB-E1-018"),
    ("5", "RWB-E1-002", "Case list v1 with case ID, owner and queue", "P1", "Window 2",
     "RWB-E1-018, RWB-E1-069, RWB-E1-020"),
    ("6", "RWB-E1-028", "Service levels, timers, escalation and prescription dates", "P3",
     "Window 2", "RWB-E1-020"),
    ("7", "RWB-E1-030", "Daily rebalancing and queue measures", "P3", "Window 2",
     "RWB-E1-028"),
    ("8", "RWB-E1-059", "Case intake agent in shadow [E1b]", "P10", "Window 2", "RWB-E1-030"),
    ("9", "RWB-E1-061", "Intake agent evaluation and L1 proposal [E2a]", "P10", "Window 2",
     "RWB-E1-059"),
    ("10", "RWB-E1-063", "Agent monitoring dashboard v1 [E2c]", "P10", "Window 2",
     "RWB-E1-061"),
    ("11", "RWB-E2-031", "Agent monitoring dashboard v2 [E3d]", "P10", "Window 4",
     "RWB-E1-063"),
    ("12", "RWB-E2-028", "Case intake agent live at L1 [E3a]", "P10", "Epic 3",
     "RWB-E2-031"),
    ("13", "RWB-E2-029", "Deviation screening agent evaluation and L1 on one segment [E3b]",
     "P10", "Epic 3", "RWB-E2-028, RWB-E1-062"),
]
for i, row in enumerate(chain):
    r = 5 + i
    for c, val in enumerate(row, 1):
        cell = cp.cell(r, c, val)
        cell._style = copy.copy(cell_style)

# ---- By module
bm = wb["By module"]
mods = [bm.cell(r, 1).value for r in range(4, 14)]
windows = ["Window 1", "Window 2", "Window 3", "Window 4", "Epic 3"]
grid = {m: {w: 0 for w in windows} for m in mods}
for v in new_items:
    for m in [x.strip() for x in str(v[3]).split(",")]:
        grid[m][v[7]] += 1
for r in range(4, 14):
    m = bm.cell(r, 1).value
    total = 0
    for j, w in enumerate(windows):
        n = grid[m][w]
        bm.cell(r, 2 + j).value = n if n else None
        total += n
    bm.cell(r, 7).value = total
for j, w in enumerate(windows):
    bm.cell(14, 2 + j).value = counts.get(w, 0)
bm.cell(14, 7).value = sum(counts.values())
bm["A2"] = ("How the work spreads across the windows, to balance the two squads. One item is "
            "one story or enabler. An item that spans two modules is counted under each, so "
            "the module rows add to more than the 107 items.")

# ---- Pull rules: add the ACE gate
pr = wb["Pull rules"]
last = pr.max_row  # 9
r = last + 1
for c, v in ((1, "6"),
             (2, ("RWB-ACE-001 is the ACE team's delivery: RWB-E1-069 builds the 16 Section A "
                  "views now and the 14 Section B views only after the ACE tables, columns and "
                  "grant land (DL43, 21 November)"))):
    cell = pr.cell(r, c, v)
    cell._style = copy.copy(pr.cell(last, c)._style)

wb.properties.title = "Recovery Workbench Build Sequence Epic 1 and Epic 2 v5"
wb.properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
wb.save(DST)
print("saved", DST, "items", len(new_items))
print("windows", counts)
print("modules", {m: sum(grid[m].values()) for m in mods})


