"""Build Recovery Workbench Reference Data and Lists of Values v5 from the copied v4.

Only the additions of the D-RCV-60 realignment are written: the Read me sheet, four
appended columns on Lists, four on Reference tables, the Reference data starter sheet,
one Change process step, four Key rows and the document properties. Every v4 cell of
the five source sheets is left as it is.
"""
import json
from copy import copy as _copy

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

V5 = "06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx"
D = "_work/msr/docs/B-DATA-19/derive.json"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

data = json.load(open(D, encoding="utf-8"))
items = {i["code"]: i for i in data["items"]}
refs = data["refs"]
starter = data["starter"]

TITLE_FONT = Font(bold=True, size=16, color="4E297F")
SUB_FONT = Font(size=10, color="404040")
HDR_FONT = Font(bold=True, size=10, color="4E297F")
BODY_FONT = Font(size=10, color="1F1F1F")
HDR_FILL = openpyxl.styles.PatternFill("solid", fgColor="DCD3EB")
WRAP = Alignment(wrap_text=True, vertical="top")

wb = openpyxl.load_workbook(V5)
name_of = data["service_name"]

# ---------------------------------------------------------------- Lists columns G to J
ws = wb["Lists"]
NEW = [
    ("Owning service (D-RCV-60)", 20),
    ("Owning schema (D-RCV-60)", 20),
    ("Shared-list route (D-RCV-60)", 46),
    ("Basis (D-RCV-60)", 78),
]
first = ws.max_column + 1          # 7 = G
for k, (title, width) in enumerate(NEW):
    col = first + k
    h = ws.cell(row=4, column=col, value=title)
    h.font = _copy(ws.cell(row=4, column=6).font)
    h.fill = _copy(ws.cell(row=4, column=6).fill)
    h.alignment = _copy(ws.cell(row=4, column=6).alignment)
    ws.column_dimensions[get_column_letter(col)].width = width
    for r in range(5, ws.max_row + 1):
        code = ws.cell(row=r, column=1).value
        if not code:
            continue
        it = items[str(code).strip()]
        vals = [f"{it['owner']} {name_of[it['owner']]}", it["schema"], it["route"], it["basis"]]
        c = ws.cell(row=r, column=col, value=vals[k])
        c.font = _copy(ws.cell(row=r, column=6).font)
        c.alignment = _copy(ws.cell(row=r, column=6).alignment)
assert ws.max_row == 142 and ws.max_column == 10, (ws.max_row, ws.max_column)
ws.auto_filter.ref = "A4:J142"

# ---------------------------------------------------------------- Reference tables F to I
ws = wb["Reference tables"]
NEW = [
    ("Owning service (D-RCV-60)", 20),
    ("Owning schema (D-RCV-60)", 20),
    ("Shared route (D-RCV-60)", 46),
    ("Basis (D-RCV-60)", 70),
]
first = ws.max_column + 1          # 6 = F
ref_by_name = {r["item"]: r for r in refs}
for k, (title, width) in enumerate(NEW):
    col = first + k
    h = ws.cell(row=4, column=col, value=title)
    h.font = _copy(ws.cell(row=4, column=5).font)
    h.fill = _copy(ws.cell(row=4, column=5).fill)
    h.alignment = _copy(ws.cell(row=4, column=5).alignment)
    ws.column_dimensions[get_column_letter(col)].width = width
    for r in range(5, ws.max_row + 1):
        name = ws.cell(row=r, column=1).value
        if not name:
            continue
        rf = ref_by_name[str(name).strip()]
        vals = [f"{rf['owner']} {name_of[rf['owner']]}", rf["schema"], rf["route"], rf["basis"]]
        c = ws.cell(row=r, column=col, value=vals[k])
        c.font = _copy(ws.cell(row=r, column=5).font)
        c.alignment = _copy(ws.cell(row=r, column=5).alignment)
assert ws.max_row == 18 and ws.max_column == 9, (ws.max_row, ws.max_column)
ws.auto_filter.ref = "A4:I18"

# ---------------------------------------------------------------- Reference data starter
if "Reference data starter" in wb.sheetnames:
    raise SystemExit("sheet already present")
st = wb.create_sheet("Reference data starter", wb.sheetnames.index("Reference tables") + 1)
st.sheet_view.showGridLines = False
lines = [
    ("Reference data starter", TITLE_FONT, 52),
    (f"{len(starter)} rows: one per service and starter item. The starter is the set of lists and reference "
     "tables a service reads or holds at its first deployment, in the wave of that service (Ownership Map "
     "sheet Services).", SUB_FONT, 60),
    ("A row exists when the service owns a table whose column uses a list (Lists sheet 'Used by'; Ownership Map "
     "sheet Tables), owns the ACE view a list column is read from (P1 rwb-source-data, DP-05), or owns a "
     "reference table of the Reference tables sheet. A list is held once, in the service the Lists sheet names in "
     "'Owning service (D-RCV-60)', and every other service reads it through that owner's contract (DP-07); an "
     "ACE-sourced list is read through the P1 contract and never loaded (DP-05).", SUB_FONT, 60),
    ("Not in the starter: 11 closed lists that have no live field after D-RCV-35, and two services with no "
     "derived row, S1 rwb-valuation and S7 rwb-writeoff (CG-B-DATA-19-3; CG-B-DATA-19-4; "
     "ASM-B-DATA-19-3; ASM-B-DATA-19-4).", SUB_FONT, 60),
]
for i, (text, font, width) in enumerate(lines, start=1):
    c = st.cell(row=i, column=1, value=text)
    c.font = font
    c.alignment = WRAP
st.row_dimensions[1].height = 24
for r in (2, 3, 4):
    st.row_dimensions[r].height = 44

HEAD = ["Service", "Service name", "Service wave", "Starter item", "Item kind", "Starter mode",
        "Route (D-RCV-60)", "Basis (D-RCV-60)"]
WIDTHS = [9, 20, 9, 26, 15, 11, 48, 78]
for k, (h, w) in enumerate(zip(HEAD, WIDTHS), start=1):
    c = st.cell(row=6, column=k, value=h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = WRAP
    st.column_dimensions[get_column_letter(k)].width = w
st.row_dimensions[6].height = 30
name_of = data["service_name"]
for r, row in enumerate(starter, start=7):
    vals = [row["service"], name_of[row["service"]], row["wave"], row["item"], row["kind"],
            row["mode"], row["route"], row["basis"]]
    for k, v in enumerate(vals, start=1):
        c = st.cell(row=r, column=k, value=v)
        c.font = BODY_FONT
        c.alignment = WRAP
last = 6 + len(starter)
st.freeze_panes = "A7"
st.auto_filter.ref = f"A6:H{last}"
summary = (f"Counts: Load {sum(1 for r in starter if r['mode'] == 'Load')} and "
           f"Read {sum(1 for r in starter if r['mode'] == 'Read')}; "
           f"wave 0 {sum(1 for r in starter if r['wave'] == '0')}, "
           f"wave 1 {sum(1 for r in starter if r['wave'] == '1')}, "
           f"wave 2 {sum(1 for r in starter if r['wave'] == '2')}, "
           f"wave 3 {sum(1 for r in starter if r['wave'] == '3')}, "
           f"wave 4 {sum(1 for r in starter if r['wave'] == '4')}.")
c = st.cell(row=last + 2, column=1, value=summary)
c.font = BODY_FONT
c.alignment = WRAP

# ---------------------------------------------------------------- Change process step 9
ws = wb["Change process"]
assert ws.max_row == 12, ws.max_row
c = ws.cell(row=13, column=1, value=9)
c.font = _copy(ws.cell(row=12, column=1).font)
c.alignment = _copy(ws.cell(row=12, column=1).alignment)
c = ws.cell(row=13, column=2, value="Shared list")
c.font = _copy(ws.cell(row=12, column=2).font)
c.alignment = _copy(ws.cell(row=12, column=2).alignment)
c = ws.cell(row=13, column=3, value=(
    "A list is held once, in the service of its 'Owning service (D-RCV-60)' column, and loaded there through steps 1 to 7. "
    "No other service loads a copy: it reads the list through that owner's contract, with the asOf business date, and the "
    "read records the version it used (DP-07; RWB-P3-E1043-CON). A service that needs a code the owner does not hold raises "
    "the change with the owner, not in its own schema."))
c.font = _copy(ws.cell(row=12, column=3).font)
c.alignment = _copy(ws.cell(row=12, column=3).alignment)

# ---------------------------------------------------------------- Key rows
ws = wb["Key"]
assert ws.max_row == 12, ws.max_row
key_rows = [
    ("Column", "Owning service (D-RCV-60)",
     "The service, from the Ownership Map, that holds the list or the reference table in its own rwb_<name> schema"),
    ("Column", "Shared-list route (D-RCV-60)",
     "The contract a consumer calls to read the list, with the business date; the list is never copied into the consumer's schema"),
    ("Column", "Starter mode",
     "Load: the values are held and versioned by the owning service. Read: the values are ACE data, read through the P1 contract and never loaded"),
    ("Term", "Reference data starter",
     "The set of lists and reference tables a service reads or holds at its first deployment, in its wave, on the Reference data starter sheet"),
]
for k, row in enumerate(key_rows, start=13):
    for col, v in enumerate(row, start=1):
        c = ws.cell(row=k, column=col, value=v)
        c.font = _copy(ws.cell(row=12, column=col).font)
        c.alignment = _copy(ws.cell(row=12, column=col).alignment)

# ---------------------------------------------------------------- Read me
rm = wb.create_sheet("Read me", 0)
rm.column_dimensions["A"].width = 132
rm.sheet_view.showGridLines = False
n_load = sum(1 for r in starter if r["mode"] == "Load")
n_read = sum(1 for r in starter if r["mode"] == "Read")
svc = len({r["service"] for r in starter})
lines = [
    ("SCB Collections and Recovery. Henka Group, 22 November 2026.", Font(bold=True, size=10)),
    ("(C) Siam Commercial Bank and Henka Pte Ltd", Font(bold=True, size=10)),
    ("", None),
    ("Recovery Workbench Reference Data and Lists of Values v5", TITLE_FONT),
    ("Next version of Recovery Workbench Reference Data and Lists of Values v4.xlsx. Decision D-RCV-60 microservice realignment.", SUB_FONT),
    (f"Tool: {TOOL}.", SUB_FONT),
    ("", None),
    ("Change log", HDR_FONT),
    (f"v5, 22 November 2026, {DEC} microservice realignment, {TOOL}", BODY_FONT),
    ("", None),
    ("What changed in v5", HDR_FONT),
    ("1. Lists sheet: four columns are added at the end. 'Owning service (D-RCV-60)' and 'Owning schema (D-RCV-60)' give the service code and name and the rwb_<name> schema that hold the list, 'Shared-list route (D-RCV-60)' gives the contract a consumer calls, and 'Basis (D-RCV-60)' names the Ownership Map row behind it. Columns A to F are unchanged, cell for cell.", BODY_FONT),
    ("2. Lists sheet: the holding service follows the Ownership Map, not the old single schema. 126 lists are held by P3 rwb-case in rwb_case (lov_value), 7 are ACE data read through P1 rwb-source-data, 2 are held by P5 rwb-document, 2 are held by P7 rwb-decision and 1 by P4 rwb-access. The business owner in column D is copied unchanged and stays the stewardship role.", BODY_FONT),
    ("3. Reference tables sheet: the same four columns are added at the end (F to I). delegation_limit, role, permission and masking_rule go to P4 rwb-access (ASM-A6-tables-4; Ownership Map sheet Tables), rule_row to P7 rwb-decision (ASM-A6-tables-3), document_type and retention_rule to P5 rwb-document (Ownership Map sheet Tables; ASM-A6-tables-10), template to P6 rwb-comms, partner to S9 rwb-partner, queue, timer and reference_row to P3 rwb-case, and feature flags to the platform library (R-PREC default ruling).", BODY_FONT),
    (f"4. New sheet 'Reference data starter', after Reference tables: {len(starter)} rows, one per service and starter item, with the item, the mode (Load or Read), the route, the wave and the basis. It is the refdata starter of the D-RCV-60 change: what each service needs at its first deployment, and where it comes from.", BODY_FONT),
    ("5. Change process sheet: one step is added (step 9, shared list). A list is held once, in its owning service, and every other service reads it through that owner's contract with the asOf business date; no service loads a second copy (DP-07).", BODY_FONT),
    ("6. Key sheet: four rows are added, one for each new term ('Owning service', 'Shared-list route', 'Starter mode' and 'Reference data starter').", BODY_FONT),
    ("7. Read me: this sheet is new and carries the header of Template and Rules section R8.1 and the change-log row.", BODY_FONT),
    ("", None),
    ("What did not change", HDR_FONT),
    ("All 138 lists, the 124 closed and 14 source split, every list code, kind, 'Values or source', 'Owner', 'Used by' and 'Source' cell, all 598 values with their Thai label, order and valid from date, the 14 reference table rows, the 8 change steps and the 12 key rows of v4, and every number and date of v4 are copied unchanged.", BODY_FONT),
    ("The only dates in the source are the 598 'Valid from' dates of 30 November 2026 in the Values sheet. They are copied unchanged because they are the in-force dates of the values; the programme release of 30 November 2026 is carried as tentative by the programme documents, and no date is changed here.", BODY_FONT),
    ("Where v4 says 'the Workbench' or names a stewardship role in column D, v5 still says so, and the service owner is read from the appended column (CG-B-DATA-19-7; ASM-B-DATA-19-7).", BODY_FONT),
    ("", None),
    ("Counts", HDR_FONT),
    ("Lists: 138 rows with 4 appended columns, 552 appended cells. Owning service: P3 126, P1 7, P5 2, P7 2, P4 1. Shared-list route: rwb-case list read 124, rwb-case parameters contract 1, rwb-case queue resource 1, ACE read through P1 7, rwb-decision rule packages 2, rwb-document contract 2, rwb-access contract 1.", BODY_FONT),
    (f"Reference data starter: {len(starter)} rows over {svc} service codes ({svc - 1} of the 19 services plus the platform library), {n_load} Load and {n_read} Read. Wave 0: 3, wave 1: 147, wave 2: 13, wave 3: 10, wave 4: 6.", BODY_FONT),
    ("Reference tables: 14 rows with 4 appended columns, 56 appended cells. Change process: 8 rows plus 1. Key: 12 rows plus 4. Values: 598 rows, no cell changed.", BODY_FONT),
    ("", None),
    ("Open points", HDR_FONT),
    ("CG-B-DATA-19-1 to CG-B-DATA-19-7 and ASM-B-DATA-19-1 to ASM-B-DATA-19-7 in the Gap and Assumption registers hold what this version leaves open: the 25 codes of LOV-REF-TABLE against the twelve of the contract, the dropped payment_match_rule, the two services with no derived starter row, the starter rule itself, the source lists held in another service's table, the meaning of the Owner column, and the reference rows that name no table.", BODY_FONT),
]
for i, (line, font) in enumerate(lines, start=1):
    c = rm.cell(row=i, column=1, value=line)
    if font is not None:
        c.font = font
    c.alignment = WRAP

wb.active = 0
wb.properties.title = "Recovery Workbench Reference Data and Lists of Values v5"
wb.properties.creator = "SCB Collections and Recovery, Henka Group"
wb.properties.lastModifiedBy = TOOL
wb.properties.subject = "D-RCV-60 microservice realignment"
wb.properties.description = "Reference data and lists of values, next version under the 19-service realignment."
wb.save(V5)
print("saved", V5, wb.sheetnames)
