"""Interface Specifications v3.xlsx and System Disposition v3.xlsx fixes (formatting preserved)."""
import json, os
from copy import copy
import openpyxl
import fixint_common as c

rows = json.load(open(os.path.join(os.path.dirname(__file__), "fixint_rows.json"), encoding="utf-8"))


def cp_style(src, dst):
    dst.font = copy(src.font); dst.fill = copy(src.fill); dst.border = copy(src.border)
    dst.alignment = copy(src.alignment); dst.number_format = src.number_format; dst.protection = copy(src.protection)


def find_row(ws, col, val):
    hits = [r for r in range(1, ws.max_row + 1) if ws.cell(r, col).value == val]
    assert len(hits) == 1, (ws.title, val, hits)
    return hits[0]


def setv(ws, addr, expect_sub, new):
    cur = ws[addr].value
    assert expect_sub is None or (cur and expect_sub in str(cur)), (ws.title, addr, cur)
    ws[addr].value = new


# ---------------- Interface Specifications v3.xlsx ----------------
wb = openpyxl.load_workbook(c.IFX)
ws = wb["Interfaces"]
setv(ws, "A2", "23 numbered interfaces",
     "25 numbered interfaces the Workbench builds or reads, including INT-35 (NLEADS credit decision) and INT-36 (EasyApp e-signature), "
     "the two new ACE inbound interfaces raised in RWB-ACE-001. Inbound source interfaces are owned by the ACE team; this sheet and the "
     "Field mapping sheet are the ACE ingestion contract. No component calls a system of record directly. Supersedes v2.")
r = find_row(ws, 1, "INT-12"); setv(ws, f"E{r}", "v_ace_npa_asset", "ACE ingestion, read through v_ace_asset, v_ace_npa_asset and v_ace_npa_sale")
r = find_row(ws, 1, "INT-21")
setv(ws, f"E{r}", "ACE sign-in", "ACE sign-in; group-to-role mapping read through v_ace_iam_group")
setv(ws, f"H{r}", "group membership", "User identity and Entra ID group membership; group-to-role mapping held in iam_group (new ACE table) and read through v_ace_iam_group.entra_group")
ph = [r for r in range(5, ws.max_row + 1) if ws.cell(r, 1).value == c.PLACEHOLDER]
assert len(ph) == 2
for r in ph:
    if ws.cell(r, 2).value == "NLEADS":
        ws.cell(r, 1).value = "INT-35"
        ws.cell(r, 3).value = "Credit approval result for a restructure plan, new to ACE and raised in RWB-ACE-001. The officer's submission in NLEADS stays INT-26"
    else:
        assert ws.cell(r, 2).value == "EasyApp"
        ws.cell(r, 1).value = "INT-36"
        ws.cell(r, 3).value = "E-signature reference and status for a restructure agreement, new to ACE and raised in RWB-ACE-001"

# Field mapping: 9 -> 11 columns
ws = wb["Field mapping"]
assert ws.max_row == 86 and [x.value for x in ws[4]][:9] == ["Interface", "Source field", "Entity", "Field", "Data type", "Physical type", "Mandatory", "Transformation", "Owner"]
srcmap = [1, 2, 3, 4, 4, 4, 5, 6, 7, 8, 9]   # new col -> old col for style
styles = {}
for rr in range(4, 87):
    styles[rr] = [ws.cell(rr, k)._style for k in range(1, 10)]
oldw = {k: ws.column_dimensions[k].width for k in "ABCDEFGHI"}
for rr in range(4, 87):
    for j, sc in enumerate(srcmap, 1):
        ws.cell(rr, j)._style = copy(styles[rr][sc - 1])
for j, h in enumerate(c.HEADER, 1):
    ws.cell(4, j).value = h
assert len(rows) == 82
for i, rv in enumerate(rows):
    for j, v in enumerate(rv, 1):
        ws.cell(5 + i, j).value = v
for k, w in zip("ABCDEFGHIJK", [22, 30, 34, 8, 40, 12, oldw["E"], oldw["F"], oldw["G"], 44, oldw["I"]]):
    ws.column_dimensions[k].width = w
ws.auto_filter.ref = "A4:K86"
setv(ws, "A2", "82 mappings",
     "82 mappings from the source system and bank file fields to the ACE table.column that holds each value (Tier 1 exists in ACE today, "
     "Tier 2 is added by the ACE team in RWB-ACE-001) and the recovery.v_ace_* view column the Workbench reads, per the LDM v7 ACE mapping sheet. "
     "Outbound rows (INT-14, INT-25) name the Workbench (Tier 4) column the file is built from. The inbound rows are the ACE ingestion specification and are owned by the ACE team.")

# Key additions
ws = wb["Key"]
last = ws.max_row
add = [("Column", "Table.column", "For an inbound interface, the ACE table and column that hold the value; for an outbound interface, the Workbench column the file is built from"),
       ("Column", "Read path", "The recovery.v_ace_* view column the Workbench reads; the ACE column name appears only in the view definition"),
       ("Column", "LDM field", "The field ID in the Logical Data Model and Data Dictionary v7"),
       ("Tier", "Tier 1", "An ACE table or column that exists today, read through a view and never altered by the Workbench"),
       ("Tier", "Tier 2", "A new ACE table or column owned by the ACE team and raised in RWB-ACE-001"),
       ("Tier", "Tier 4", "A Workbench-owned table; used only by the outbound interfaces")]
for i, vals in enumerate(add, 1):
    for j, v in enumerate(vals, 1):
        cell = ws.cell(last + i, j); cell.value = v; cp_style(ws.cell(last, j), cell)
    if ws.row_dimensions[last].height:
        ws.row_dimensions[last + i].height = ws.row_dimensions[last].height
ws.auto_filter.ref = f"A4:C{last + len(add)}"
wb.save(c.IFX)
print("Interface Specifications v3.xlsx saved")

# ---------------- System Disposition v3.xlsx ----------------
wb = openpyxl.load_workbook(c.DISP)
ws = wb["Disposition"]
setv(ws, "A2", "25 systems", "25 systems and tools that recovery uses today, what happens to each, who owns the data path and when. Supersedes v2.")
dval = {"Core bank (ALS)": "Partly", "SCBPDM": "Partly", "COLLINS": "Partly", "LIT": "No", "CCMS": "Partly",
        "SVAF": "No", "AMIS": "Partly", "Data lake and Power BI": "Not applicable"}
for sysname, v in dval.items():
    ws.cell(find_row(ws, 1, sysname), 4).value = v
r = find_row(ws, 1, "NLEADS")
setv(ws, f"F{r}", "new ACE interface", "ACE ingests the credit decision result through INT-35 and the Workbench reads it through v_ace_credit_decision; the officer still submits the request in NLEADS (INT-26)")
setv(ws, f"H{r}", c.PLACEHOLDER, "INT-26, INT-35")
r = find_row(ws, 1, "EasyApp")
setv(ws, f"F{r}", "new ACE interface", "ACE ingests the signature request reference and status through INT-36 and the Workbench reads it through v_ace_esign; the signed file stays in the document hub")
setv(ws, f"H{r}", c.PLACEHOLDER, "INT-36")

ws = wb["Interfaces"]
setv(ws, "A2", "outbound paths stay with the Workbench",
     "36 numbered interfaces with 32 systems. ACE ingests every inbound source and the Workbench reads it through the read-only v_ace_* views. "
     "The Workbench owns its outbound files, the reporting feeds and the partner portal; SMS, LINE and the audit and security logs "
     "(INT-17, INT-18, INT-22) leave through paths the ACE team owns. No component calls a system of record directly. "
     "INT-35 (NLEADS credit decision) and INT-36 (EasyApp e-signature) are the two new ACE inbound interfaces raised in RWB-ACE-001.")
ival = {"INT-01": "Partly", "INT-03": "Not applicable", "INT-04": "Partly", "INT-08": "No", "INT-09": "No", "INT-10": "Partly",
        "INT-11": "No", "INT-12": "Partly", "INT-19": "Not applicable", "INT-20": "Not applicable", "INT-21": "Partly",
        "INT-26": "Not applicable", "INT-33": "Not applicable"}
for iid, v in ival.items():
    ws.cell(find_row(ws, 1, iid), 9).value = v
r = find_row(ws, 1, "INT-26")
setv(ws, f"F{r}", "new ACE interface", "Submitted by the officer in NLEADS; the decision returns through INT-35")
assert ws.max_row == 38
new = [["INT-35", "NLEADS", "Credit decision result for restructure plans", "In", "File", "ACE ingests the file", "As decisions are made",
        "DP04", "No", "ACE team", "E3", "File specification", "D-RCV-35"],
       ["INT-36", "EasyApp", "E-signature reference and status for restructure agreements", "In", "File", "ACE ingests the file",
        "As signatures are requested", "DP10", "No", "ACE team", "E2", "File specification", "D-RCV-35"]]
for i, vals in enumerate(new, 39):
    for j, v in enumerate(vals, 1):
        cell = ws.cell(i, j); cell.value = v; cp_style(ws.cell(38, j), cell)
    if ws.row_dimensions[38].height:
        ws.row_dimensions[i].height = ws.row_dimensions[38].height
ws.auto_filter.ref = "A4:M40"

ws = wb["By route"]
for row in ws.iter_rows(min_row=5, max_row=9, min_col=2, max_col=4):
    for cell in row:
        assert "$38" in cell.value
        cell.value = cell.value.replace("$38", "$40")

ws = wb["Key"]
assert [ws.cell(r, 2).value for r in (21, 22, 23)] == ["Yes", "Partly", "No"] and ws.max_row == 26
for r in (26, 25, 24):   # shift Owner rows down one
    for j in range(1, 4):
        ws.cell(r + 1, j).value = ws.cell(r, j).value
        ws.cell(r + 1, j)._style = copy(ws.cell(r, j)._style)
ws.cell(21, 3).value = "Every field the Workbench reads is in an ACE table that exists today (Tier 1), read through a v_ace_* view"
ws.cell(22, 3).value = "Part of the data is in ACE tables today (Tier 1); RWB-ACE-001 adds the rest as new ACE tables or columns (Tier 2)"
ws.cell(23, 3).value = "ACE does not hold it today; where the Workbench reads it, RWB-ACE-001 adds it as new ACE tables or columns only (Tier 2)"
for j, v in enumerate(["In ACE today", "Not applicable", "Outbound or entered by partners; ACE holds no source data for it, so the tier rule does not apply"], 1):
    ws.cell(24, j).value = v; ws.cell(24, j)._style = copy(ws.cell(23, j)._style)
ws.auto_filter.ref = "A4:C27"
wb.save(c.DISP)
print("System Disposition v3.xlsx saved")
