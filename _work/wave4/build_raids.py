# -*- coding: utf-8 -*-
"""Build Recovery Workbench Risks Assumptions Issues and Dependencies v3 from v2."""
import copy, shutil, datetime
import openpyxl

SRC = r"11 Delivery and operations\Recovery Workbench Risks Assumptions Issues and Dependencies v2.xlsx"
DST = r"11 Delivery and operations\Recovery Workbench Risks Assumptions Issues and Dependencies v3.xlsx"

shutil.copyfile(SRC, DST)
wb = openpyxl.load_workbook(DST)

# ---------------- Risks
rs = wb["Risks"]
for r in range(5, rs.max_row + 1):
    rid = rs.cell(r, 1).value
    if rid == "R-01":
        rs.cell(r, 5).value = ("Closed by D-RCV-35 on 15 November 2026: the Workbench runs no "
                               "load, so its position is the ACE business date and every screen "
                               "shows the freshness stamp; ACE batch lateness is carried by R-13")
        rs.cell(r, 8).value = "Closed"
    elif rid == "R-02":
        rs.cell(r, 5).value = ("Age limits on decision inputs; the ACE feed cadence and the age "
                               "of each data product are published in the catalog (DL12 option A "
                               "is superseded by D-RCV-35)")

last = rs.max_row
style = {c: copy.copy(rs.cell(last, c)._style) for c in range(1, 9)}
new = ["R-13",
       "RWB-ACE-001 lands late, or the ACE team does not accept the 14 tables, 12 columns, "
       "the batch record and the grant",
       "High", "Medium",
       "DL43 estimated and accepted by 21 November; the 16 Section A views go first so the case "
       "record can start; a Tier 1-only fallback for the case list is costed",
       "ACE team lead; program manager", datetime.datetime(2026, 11, 21), "Open"]
r = last + 1
for c, v in enumerate(new, 1):
    cell = rs.cell(r, c, v)
    cell._style = copy.copy(style[c])
rs["A2"] = ("13 risks: 12 open and 1 closed by D-RCV-35, with impact, likelihood, action, "
            "owner and review date.")
rs.auto_filter.ref = "A4:H%d" % r

# ---------------- Assumptions
asm = wb["Assumptions"]
for r in range(5, asm.max_row + 1):
    if asm.cell(r, 1).value == "A-04":
        asm.cell(r, 2).value = ("Customer facts from ACE, which ingests them from SCBPDM and "
                                "the core bank, read through v_ace_customer")

# ---------------- Issues
iss = wb["Issues"]
for r in range(5, iss.max_row + 1):
    if iss.cell(r, 1).value == "I-03":
        iss.cell(r, 2).value = ("CCMS and SVAF layouts not confirmed by the ACE team before "
                                "RWB-ACE-001")
        iss.cell(r, 3).value = "ACE team"
        iss.cell(r, 4).value = datetime.datetime(2026, 11, 21)
        iss.cell(r, 5).value = ("ACE team confirms both layouts inside RWB-ACE-001; the Workbench "
                               "builds no adapter and holds no copy")

# ---------------- Dependencies
dp = wb["Dependencies"]
last = dp.max_row
style = {c: copy.copy(dp.cell(last, c)._style) for c in range(1, 8)}
new = [
    ["DEP-34", "ACE team",
     "RWB-ACE-001: 14 tables, 12 columns, one batch record per source and business date and "
     "the SELECT grant that the 30 recovery.v_ace_* views read",
     "E1", datetime.datetime(2026, 11, 21), "ACE team lead", "DL43"],
    ["DEP-35", "ACE team",
     "DL43: the ACE team's estimate and acceptance of RWB-ACE-001, with the 14 ingestion jobs "
     "and the migration window in the 30 November release named",
     "E1", datetime.datetime(2026, 11, 21), "Sponsor with the ACE team lead", "DL43"],
]
for i, vals in enumerate(new):
    r = last + 1 + i
    for c, v in enumerate(vals, 1):
        cell = dp.cell(r, c, v)
        cell._style = copy.copy(style[c])
dp.auto_filter.ref = "A4:G%d" % r

wb.properties.title = "Recovery Workbench Risks Assumptions Issues and Dependencies v3"
wb.properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
wb.save(DST)
print("saved", DST, "risks to", rs.max_row - 4, "deps to", dp.max_row - 4)
