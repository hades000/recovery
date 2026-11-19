# -*- coding: utf-8 -*-
"""Build Recovery Workbench Controls Catalog v3 from v2."""
import copy, shutil, datetime
import openpyxl

SRC = r"10 Policy, controls and compliance\Recovery Workbench Controls Catalog v2.xlsx"
DST = r"10 Policy, controls and compliance\Recovery Workbench Controls Catalog v3.xlsx"

shutil.copyfile(SRC, DST)
wb = openpyxl.load_workbook(DST)
ws = wb["Controls"]

for r in range(5, ws.max_row + 1):
    cid = ws.cell(r, 1).value
    if cid == "CTL-01":
        ws.cell(r, 4).value = ("Every account at 90 days past due or more in v_ace_account has "
                               "exactly one open case, and the five ACE reconciliations REC-01 "
                               "to REC-05 close with zero unexplained on each business date")
        ws.cell(r, 7).value = "Rules component; data steward reviews the REC-01 to REC-05 breaks"
        ws.cell(r, 8).value = ("Daily reconciliation report for REC-01 to REC-05; decision log "
                               "entry per case created")
        ws.cell(r, 9).value = ("Run REC-01 to REC-05 against v_ace_account for the business date; "
                               "every break is explained or raised")
        ws.cell(r, 11).value = "R-UNI-16, R-UNI-17; REC-01 to REC-05"
    elif cid == "CTL-02":
        ws.cell(r, 4).value = ("Each ACE ingestion job for a recovery source completes for the "
                               "business date and passes the business date, structure, control "
                               "total, key, reference and list checks before the views serve it")
        ws.cell(r, 7).value = "ACE ingestion; ACE data steward"
        ws.cell(r, 8).value = ("ace_batch_run row per source and business date; ingestion check "
                               "log")
        ws.cell(r, 9).value = ("Load a file with a wrong control total in ACE SIT; no row is "
                               "written for that source and business date and the previous "
                               "COMPLETED row stays")
        ws.cell(r, 10).value = "Each ACE batch run"
        ws.cell(r, 11).value = "ACE ingestion checks; RWB-ACE-001 AC3 and AC7"

last = ws.max_row
style = {c: copy.copy(ws.cell(last, c)._style) for c in range(1, 15)}
new = [
    ["CTL-43", "16.5", "Control access and data protection",
     "Every read of ACE source data goes through recovery.v_ace_*; the view-owner role holds "
     "SELECT on the listed ACE tables and nothing else; the recovery role has no privilege on an "
     "ACE table and cannot write a view",
     "Preventive", "Automated", "ACE DBA; security review",
     "Grant script and the result of the grant check",
     "As the recovery role, select a public ACE table in SIT (refused) and insert into a view "
     "(refused); compare the grant list with the 21 listed tables",
     "Each deployment", "D-RCV-35 U4; ADR-010", "REG-22, REG-32",
     "Unsuitable user access to EFS and the voice bot", "E1"],
    ["CTL-44", "16.4", "Answer audit and regulatory requests",
     "Every recovery.v_ace_* view exists with the columns and types the dictionary and the data "
     "contract publish: 30 views, 122 objects and 1,366 fields",
     "Detective", "Automated", "Data steward; build pipeline",
     "Conformance test result for each deployment",
     "Remove a column in ACE SIT; the conformance test fails and names the field",
     "Each deployment and each ACE release", "D-RCV-35 U3; ADR-010", "REG-11, REG-27",
     "None", "E1"],
]
for i, vals in enumerate(new):
    r = last + 1 + i
    for c, v in enumerate(vals, 1):
        cell = ws.cell(r, c, v)
        cell._style = copy.copy(style[c])

ws["A2"] = ("44 controls: what each checks, who performs it, the evidence it produces and how it "
            "is tested. Each answers an audit finding or a regulatory obligation.")
ws.auto_filter.ref = "A4:N%d" % (last + len(new))

# ---- By type
bt = wb["By type"]
for r in range(5, bt.max_row + 1):
    t, h = bt.cell(r, 1).value, bt.cell(r, 2).value
    if (t, h) == ("Preventive", "Automated"):
        bt.cell(r, 3).value = 28
    elif (t, h) == ("Detective", "Automated"):
        bt.cell(r, 3).value = 10

# ---- By release
br = wb["By release"]
for r in range(5, br.max_row + 1):
    if br.cell(r, 1).value == "E1":
        br.cell(r, 2).value = 10

wb.properties.title = "Recovery Workbench Controls Catalog v3"
wb.properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
wb.save(DST)
print("saved", DST, "controls", last + len(new) - 4)
