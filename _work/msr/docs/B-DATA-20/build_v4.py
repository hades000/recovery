"""Build Recovery Workbench Data Ownership and Stewardship v4 from the copied v3.

Every v3 cell is left as it is except the three cells listed in CHANGED. New
sheets, columns and rows carry the D-RCV-60 owner service per data set, taken
from the Ownership Map.
"""
import json
from copy import copy as _copy

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

V4 = "06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

# ---------------------------------------------------------------- ownership map
owb = openpyxl.load_workbook(OWN)
otab = owb["Tables"]
table_owner, table_schema = {}, {}
for row in otab.iter_rows(min_row=2, values_only=True):
    if not row or not row[0]:
        continue
    table_owner[str(row[0])] = str(row[1])
    table_schema[str(row[0])] = str(row[2])
osvc = owb["Services"]
service_name = {}
for row in osvc.iter_rows(min_row=2, values_only=True):
    if row and row[0]:
        service_name[str(row[0])] = str(row[1])
service_name.setdefault("PLT", "platform library")
EXT = {"party_ext", "contact_point_ext", "account_ext", "valuation_ext"}
LEGACY_NO_TARGET = {"lake_copy_watermark"}
assert len(table_owner) == 93, len(table_owner)
tier4 = {t: o for t, o in table_owner.items() if t not in EXT and t not in LEGACY_NO_TARGET}
assert len(tier4) == 88, len(tier4)
per_owner = {}
for t, o in tier4.items():
    per_owner.setdefault(o, []).append(t)
for o in per_owner:
    per_owner[o].sort()
order = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10",
         "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "PLT"]
assert set(per_owner) <= set(order)
print("tier4 tables", sum(len(v) for v in per_owner.values()), "owners", len(per_owner))
print({o: len(v) for o, v in per_owner.items() if o in order})

# ---------------------------------------------------------------- data products
# Owning service per data product. One owner each, from the Ownership Map sheet
# Tables plus Architecture v5 slide 41; a split is written into the basis cell
# and raised as a candidate gap.
DP_OWNER = {
    "DP01": ("P1", "rwb_source_data",
             "ACE account and payment data, read through the 30 recovery.v_ace_* views (Architecture v5 Text Extract v1 line 2884, slide 41 P1 'ACE view contract'; line 2079, slide 29; line 509, slide 7). The Ownership Map has no Workbench table for it."),
    "DP02": ("P1", "rwb_source_data",
             "party_ext and contact_point_ext are P1 rows of the Ownership Map sheet Tables; ACE customer and contact data are read through the same views (Architecture v5 Text Extract v1 line 509, slide 7)."),
    "DP03": ("P3", "rwb_case",
             "recovery_case, case_account, case_party, case_entry_exclusion, assignment, queue, queue_member, queue_measure, task and timer are P3 rows of the table map; slide 41 line 2880 P3 owns the case, the state, queues, tasks, allocation and timers."),
    "DP04": ("S2", "rwb_treatment",
             "treatment is S2 (slide 41 line 2893). The live guarantee claim is S3 (guarantee_claim) and the dated DP04 copies dp_treatment and dp_guarantee_claim are P1 (CG-B-DATA-20-2; ASM-B-DATA-20-2)."),
    "DP05": ("P1", "rwb_source_data",
             "interaction and efs_ledger_outcome are P1 rows (R-PREC default ruling, DP-18). Notices and templates are P6 and the case timeline is a P3 projection (CG-B-DATA-20-7; ASM-B-DATA-20-7)."),
    "DP06": ("S5", "rwb_asset",
             "asset_sale and listing are S5 rows and slide 41 line 2896 S5 owns assets taken on, holding, floor price, listings and auction rounds. ACE collateral and valuation stay ACE data read through P1; valuation_ext is P1 (CG-B-DATA-20-3)."),
    "DP07": ("S4", "rwb_litigation",
             "legal_action and hearing are S4 rows and slide 41 line 2895 S4 owns legal actions, hearings, judgments and enforcement. ACE LIT records are read through P1; the notice and proof of delivery are P6 (CG-B-DATA-20-4)."),
    "DP08": ("S9", "rwb_partner",
             "partner, partner_instruction and partner_user are S9 rows; slide 41 line 2891 S9 owns panel, partner users, instructions, results, fees and scorecards."),
    "DP09": ("S6", "rwb_debtsale",
             "debt_sale_lot and debt_sale_account are S6 rows; slide 41 line 2897 S6 owns lots, data room, buyer terms, bids, award and transfer."),
    "DP10": ("P5", "rwb_document",
             "the 12 P5 tables of the map cover it: document, document_text, document_field, document_custody, document_intake, document_type, document_checklist_item, case_document_check, document_hub_parameter, retention_rule, retention_action and signature_request (slide 41 line 2888)."),
    "DP11": ("S1", "rwb_valuation",
             "route economics is the S1 route decision output (slide 41 line 2892 S1 owns valuations, the D6 route decision and the route agent output); ACE collins_score is read through P1. The table map lists no rwb_valuation table (CG-B-DATA-20-5)."),
    "DP12": ("P7", "rwb_decision",
             "decision_log_entry, approval, rule_package, rule_package_version, rule_row and rule_test_case are P7 rows (slide 41 line 2881); each owning service writes its local decision record in its own schema (ADR-022; Temporal and Drools design lines 524, 888)."),
    "DP13": ("P8", "rwb_payment",
             "proceeds is a P8 row and slide 41 line 2890 P8 owns payment and proceeds matching, fees, bookings and posting files. write_off is S7 and ACE payment and gl_write_off are read through P1 (CG-B-DATA-20-6)."),
    "DP14": ("P3", "rwb_case",
             "lov_value, reference_row, reference_version, parameter_catalog and parameter_value are P3 rows (R-PREC default ruling). Roles, permissions and the DoA table are P4; templates and merge fields are P6 (CG-B-DATA-20-8)."),
}

wb = openpyxl.load_workbook(V4)

TITLE_FONT = Font(bold=True, size=16, color="4E297F")
SUB_FONT = Font(size=10, color="404040")
HDR_FONT = Font(bold=True, size=10, color="4E297F")
HDR_FILL = openpyxl.styles.PatternFill("solid", fgColor="DCD3EB")
BODY_FONT = Font(size=10, color="1F1F1F")
WRAP = Alignment(wrap_text=True, vertical="top")


def put(ws, r, c, value, like):
    """Write a value and copy the style of a reference cell in the same sheet."""
    cell = ws.cell(row=r, column=c, value=value)
    cell._style = _copy(like._style)
    cell.alignment = WRAP
    return cell


# ---------------------------------------------------------------- Ownership sheet
ws = wb["Ownership"]
assert ws.max_row == 18 and ws.max_column == 11
hdr, body = ws["A4"], ws["A5"]
for c, name, width in ((12, "Owning service (D-RCV-60)", 22),
                       (13, "Owning schema (D-RCV-60)", 20),
                       (14, "Basis (D-RCV-60)", 78)):
    put(ws, 4, c, name, hdr)
    ws.column_dimensions[get_column_letter(c)].width = width
for r in range(5, 19):
    dp = str(ws.cell(row=r, column=1).value).strip()
    code, schema, basis = DP_OWNER[dp]
    put(ws, r, 12, f"{code} {service_name[code]}", body)
    put(ws, r, 13, schema, body)
    put(ws, r, 14, basis, body)
ws.auto_filter.ref = "A4:N18"
print("Ownership rows", ws.max_row - 4)

# ---------------------------------------------------------------- Ownership split
wsp = wb["Ownership split"]
assert wsp.max_row == 10 and wsp.max_column == 6
hdr, body = wsp["A4"], wsp["A5"]
for c, name, width in ((7, "Owning service (D-RCV-60)", 26),
                       (8, "Owning schema (D-RCV-60)", 34),
                       (9, "Basis (D-RCV-60)", 70)):
    put(wsp, 4, c, name, hdr)
    wsp.column_dimensions[get_column_letter(c)].width = width
SPLIT = {
    5: ("P1 rwb-source-data",
        "rwb_source_data (views only; the 22 ACE tables stay in the ACE schemas)",
        "The 22 ACE tables are read through the 16 recovery.v_ace_* views of the ACE view contract in rwb_source_data (Architecture v5 Text Extract v1 lines 509 slide 7, 2079 slide 29 and 2884 slide 41). No service holds an ACE table."),
    6: ("P1 rwb-source-data",
        "rwb_source_data",
        "The 14 new ACE tables and 12 new columns stay an ACE change under RWB-ACE-001 (Template and Rules R5.5 DP-05); the views land with the ACE change and are read through P1."),
    7: ("P1 rwb-source-data",
        "rwb_source_data",
        "party_ext, contact_point_ext, account_ext and valuation_ext are the four P1 rows of the Ownership Map sheet Tables."),
    8: ("Split across 18 services and the platform library: " +
        ", ".join(f"{o} {len(per_owner[o])}" for o in order if o in per_owner),
        "rwb_<name>, one schema per owner",
        "88 of the 93 rows of the Ownership Map sheet Tables; 4 rows are the Tier 3 extension tables and lake_copy_watermark has no target under DP-17 (CG-B-DATA-20-9). S1 rwb-valuation owns no table row (CG-B-DATA-20-5)."),
}
for r, vals in SPLIT.items():
    for i, v in enumerate(vals):
        put(wsp, r, 7 + i, v, body)
CHANGED = [
    (wsp, "F7", "Read and write by the recovery module",
     "Read and write by P1 rwb-source-data only, in rwb_source_data"),
    (wsp, "F8", "Read and write by the recovery module",
     "Read and write by the owning service only, in its own rwb_<name> schema"),
]
for sheet, ref, old, new in CHANGED:
    assert sheet[ref].value == old, (ref, sheet[ref].value)
    sheet[ref].value = new
wsp.auto_filter.ref = "A4:I8"

# ---------------------------------------------------------------- Roles
wr = wb["Roles"]
assert wr.max_row == 12
body = wr["A5"]
put(wr, 13, 1, "Service data steward (D-RCV-60)", body)
put(wr, 13, 2, "Keeps the definitions, read mappings, quality checks and exception list of one rwb_<name> schema. The Workbench data steward of row 6 and the Workbench application owner of row 7 are held per service after the realignment: one owner per schema, 19 owners in all (CG-B-DATA-20-10; ASM-B-DATA-20-10).", body)
wr.auto_filter.ref = "A4:B13"

# ---------------------------------------------------------------- Change process
wc = wb["Change process"]
assert wc.max_row == 11
body = wc["A5"]
put(wc, 12, 1, 8, body)
put(wc, 12, 2, "Owner service (D-RCV-60)", body)
put(wc, 12, 3, "Every Tier 3 and Tier 4 change names the owning service from the Ownership sheet and is made in that service's own rwb_<name> schema by its own Flyway sequence (DP-01, DP-15). A cross-service read is a contract call and never a table or view read (Architecture v5 Text Extract v1 line 2149, slide 29).", body)
wc.auto_filter.ref = "A4:C12"

# ---------------------------------------------------------------- Quality measures
wq = wb["Quality measures"]
assert wq.max_row == 11
body = wq["A5"]
assert wq["B10"].value == "Every v_ace_* view compiles and no recovery table reads public.*"
wq["B10"].value = "Every v_ace_* view compiles and no rwb_<name> table reads public.*"
put(wq, 12, 1, "Schema isolation (D-RCV-60)", body)
put(wq, 12, 2, "No service reads another service's tables or views; each rwb_<name> schema is reachable only by its owner login (Architecture v5 Text Extract v1 line 2149, slide 29)", body)
put(wq, 12, 3, "Boundary test in every service build; per-service DB story", body)
wq.auto_filter.ref = "A4:C12"

# ---------------------------------------------------------------- Read me
rm = wb.create_sheet("Read me", 0)
rm.column_dimensions["A"].width = 132
rm.sheet_view.showGridLines = False
lines = [
    "SCB Collections and Recovery. Henka Group, 22 November 2026.",
    "(C) Siam Commercial Bank and Henka Pte Ltd",
    "",
    "Recovery Workbench Data Ownership and Stewardship v4",
    "Next version of Recovery Workbench Data Ownership and Stewardship v3.xlsx. Decision D-RCV-60 microservice realignment.",
    f"Tool: {TOOL}.",
    "",
    "Change log",
    f"v4, 22 November 2026, {DEC} microservice realignment, {TOOL}",
    "",
    "What changed in v4",
    "1. Ownership sheet: three columns are added at the end. 'Owning service (D-RCV-60)' gives one service code and name per data product, 'Owning schema (D-RCV-60)' gives its rwb_<name> schema and 'Basis (D-RCV-60)' gives the Ownership Map table rows and the Architecture v5 line that carry the ruling. Columns A to K are unchanged, cell for cell.",
    "2. Ownership split sheet: the same three columns are added. Tier 1, Tier 2 and Tier 3 fall to P1 rwb-source-data; Tier 4 is split across 18 services and the platform library, one schema per owner, with the table count per owner in the cell.",
    "3. Ownership split sheet: two cells change in the 'Workbench access' column. Tier 3 and Tier 4 no longer read 'Read and write by the recovery module': the module is replaced by the owning service, and a service reads only its own schema (DP-01, DP-02).",
    "4. Roles sheet: one row is added for the service data steward, who holds one rwb_<name> schema. The v3 rows are unchanged.",
    "5. Change process sheet: one step is added (step 8, owner service) for a Tier 3 or Tier 4 change made by the owning service in its own schema.",
    "6. Quality measures sheet: one measure is added (schema isolation) and one cell changes, so the view conformance check reads 'no rwb_<name> table reads public.*' instead of 'no recovery table reads public.*'.",
    "7. Read me: this sheet is new and carries the header of Template and Rules section R8.1 and the change-log row.",
    "",
    "What did not change",
    "All 14 data products, the DP01 to DP14 identifiers, every 'What it holds', 'Business owner', 'Data steward', 'System of record', 'Who may change it', 'How a change is requested', 'Freshness' and 'Tier' cell, the four tiers and their table counts (22 ACE tables through 16 views, 14 new tables and 12 new columns through 14 views, 4 extension tables, 88 Workbench tables), the 12 data roles and the 7 change steps are copied from v3 unchanged.",
    "Where v3 says 'the recovery module' or 'Application owner (DL02)', v4 still says so and the owner is read from the appended 'Owning service (D-RCV-60)' column (CG-B-DATA-20-11; ASM-B-DATA-20-11).",
    "The source carries no date in any of its five sheets, so no release date exists to mark (tentative) and no date is changed.",
    "",
    "Counts",
    "Ownership: 14 data products, one owning service each. P1 rwb-source-data on 3 (DP01, DP02, DP05), P3 rwb-case on 2 (DP03, DP14), and one each on P5 rwb-document (DP10), P7 rwb-decision (DP12), P8 rwb-payment (DP13), S1 rwb-valuation (DP11), S2 rwb-treatment (DP04), S4 rwb-litigation (DP07), S5 rwb-asset (DP06), S6 rwb-debtsale (DP09) and S9 rwb-partner (DP08).",
    "Ownership split: 93 Ownership Map tables. 4 are Tier 3 extension tables in rwb_source_data, 1 legacy table (lake_copy_watermark) has no target, and the remaining 88 are Tier 4, split P1 13, P2 3, P3 15, P4 5, P5 12, P6 3, P7 6, P8 1, P9 3, P10 8, S2 1, S3 1, S4 2, S5 2, S6 2, S7 1, S8 1, S9 3 and the platform library 6.",
    "Roles: 12 v3 rows plus 1 new row. Change process: 7 v3 steps plus 1 new step. Quality measures: 7 v3 measures plus 1 new measure.",
    "",
    "Open points",
    "CG-B-DATA-20-1 to CG-B-DATA-20-11 and ASM-B-DATA-20-1 to ASM-B-DATA-20-11 in the Gap and Assumption registers hold what this version leaves open. Each is cited in the cell it affects.",
]
for i, line in enumerate(lines, start=1):
    c = rm.cell(row=i, column=1, value=line)
    c.alignment = Alignment(vertical="top", wrap_text=True)
    if i in (1, 2):
        c.font = Font(bold=True, size=10)
    elif i == 4:
        c.font = TITLE_FONT
    elif i == 5:
        c.font = SUB_FONT
    elif i in (8, 11, 20, 25, 30):
        c.font = HDR_FONT

wb.active = 0
wb.save(V4)
print("saved", V4, wb.sheetnames)
