# -*- coding: utf-8 -*-
"""Build Recovery Workbench Release Plan v4.xlsx from v3."""
import copy, shutil, datetime
import openpyxl

SRC = r"11 Delivery and operations\Recovery Workbench Release Plan v3.xlsx"
DST = r"11 Delivery and operations\Recovery Workbench Release Plan v4.xlsx"

shutil.copyfile(SRC, DST)
wb = openpyxl.load_workbook(DST)
ws = wb["Releases"]

for r in range(5, ws.max_row + 1):
    ep = ws.cell(r, 1).value
    if ep == "E1":
        ws.cell(r, 10).value = (
            "P1 recovery data engine over the 30 read-only recovery.v_ace_* views: 92 tables, "
            "122 objects and 1,366 fields, with RWB-E1-069 building the 16 Section A and 14 "
            "Section B views; P3 case record, state model and rules component with allocation "
            "rules; P4 sign-in and roles; P5 document store and OCR; P6 notice generation; P7 "
            "decision log store; P9 baseline; P10 agent runtime in shadow")
        ws.cell(r, 11).value = (
            "One case list for every account at 90 days past due or more, reconciled to the ACE "
            "account view. Documents found by case. Decision log store. Read-only case record view")
        ws.cell(r, 13).value = 60
        ws.cell(r, 15).value = (
            "RWB-ACE-001 (ACE team, DL43) is due 21 November and gates RWB-E1-069; the 16 "
            "Section A views follow E1-001, the 14 Section B views and the 12 new ACE columns "
            "wait on the ACE delivery. A late ACE delivery moves the case list and the release")
    elif ep == "E2":
        ws.cell(r, 13).value = 31

ws["A2"] = ("One production release at each month end, shared with the collection squad. "
            "Epics 1 and 2 are confirmed; Epics 3 to 8 are proposed and confirmed one month "
            "ahead. The 30 November release reads ACE through the 30 read-only views and takes "
            "its data date from the ACE batch.")

# release rules: add the ACE gate
rr = wb["Release rules"]
last = rr.max_row
style = {c: copy.copy(rr.cell(last, c)._style) for c in range(1, 3)}
r = last + 1
for c, v in enumerate(["7", "A release that reads a new ACE table or column waits for "
                            "RWB-ACE-001; the ACE batch for the business date is the data date "
                            "of the release"], 1):
    cell = rr.cell(r, c, v)
    cell._style = copy.copy(style[c])

wb.properties.title = "Recovery Workbench Release Plan v4"
wb.properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
wb.save(DST)
print("saved", DST)
