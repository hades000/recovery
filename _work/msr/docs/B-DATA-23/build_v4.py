"""Build Recovery Workbench Reporting and Analytics Data Model v4 from the copied v3.

Every v3 cell is kept as it is except the ten cells listed in CHANGED: the Facts note
and the nine Facts refresh cells, which still describe a data lake and a direct
recovery.v_ace_* read. New sheets, columns and rows carry the D-RCV-60 read model in
rwb_reporting (P9) fed from events, with every owner taken from the Ownership Map.
"""
import json
from copy import copy as _copy
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

V3 = "06 Data/Recovery Workbench Reporting and Analytics Data Model v3.xlsx"
V4 = "06 Data/Recovery Workbench Reporting and Analytics Data Model v4.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

TITLE_FONT = Font(bold=True, size=16, color="4E297F")
SUB_FONT = Font(size=10, color="404040")
HDR_FONT = Font(bold=True, size=10, color="4E297F")
HDR_FILL = PatternFill("solid", fgColor="DCD3EB")
BODY_FONT = Font(size=10, color="1F1F1F")
BODY_BOLD = Font(bold=True, size=10, color="1F1F1F")
WRAP = Alignment(wrap_text=True, vertical="top")

# ---------------------------------------------------------------- ownership map
owb = openpyxl.load_workbook(OWN)
osvc = owb["Services"]
service_name = {str(r[0]): str(r[1]) for r in osvc.iter_rows(min_row=2, values_only=True) if r and r[0]}
service_name.setdefault("PLT", "platform library")
for code in ("P1", "P3", "P7", "P8", "P9", "S2", "S4", "S5", "S6", "S7", "S9"):
    assert code in service_name, code
otab = owb["Tables"]
table_owner = {str(r[0]): str(r[1]) for r in otab.iter_rows(min_row=2, values_only=True) if r and r[0]}
for t in ("measure_definition", "measure_snapshot", "measure_publish", "queue_measure",
          "recovery_case", "decision_log_entry", "treatment", "legal_action", "asset_sale",
          "debt_sale_lot", "proceeds", "write_off", "partner_instruction"):
    assert table_owner.get(t) is not None, t
print("ownership map read:", len(service_name), "services,", len(table_owner), "tables")
assert table_owner["measure_definition"] == "P9" and table_owner["measure_snapshot"] == "P9"
assert table_owner["measure_publish"] == "P9"

# ---------------------------------------------------------------- changed cells
# Ten v3 cells change, all of them because the lake and the direct ACE read are gone.
CHANGED = {
    ("Facts", "A2"):
        "Star schema in rwb_reporting (P9) for the steering dashboard and the reports, built from the "
        "business events on Kafka; no data lake (INT-19 and INT-20 removed; ADR-018; DP-17). ACE source "
        "rows come through the ACE view contract of rwb-source-data (P1) on the snapshot(page) activity "
        "and are never read from recovery.v_ace_* by the reporting layer. Workbench rows come from the "
        "events of their owning service. No source system is loaded directly.",
    ("Facts", "F5"): "Event-fed projections; publish 01:30 (JOB-15). ACE rows through the rwb-source-data contract, never a direct view read",
    ("Facts", "F6"): "Event-fed from DecisionRecorded on rwb.decision-record.v1; publish 01:30 (JOB-15)",
    ("Facts", "F7"): "Event-fed projections; publish 01:30 (JOB-15). ACE rows through the rwb-source-data contract",
    ("Facts", "F8"): "Event-fed projections; publish 01:30 (JOB-15). ACE rows through the rwb-source-data contract",
    ("Facts", "F9"): "Event-fed projections; publish 01:30 (JOB-15). ACE rows through the rwb-source-data contract",
    ("Facts", "F10"): "Event-fed from LotAwarded and AccountsTransferred; publish 01:30 (JOB-15)",
    ("Facts", "F11"): "Event-fed projections; publish 01:30 (JOB-15). ACE rows through the rwb-source-data contract",
    ("Facts", "F12"): "Event-fed from InstructionIssued and PartnerResultSubmitted; publish 01:30 (JOB-15)",
    ("Facts", "F13"): "Monthly from the rwb-source-data contract (P1 reads v_ace_bucket_log); publish 01:30 (JOB-15)",
}

# ---------------------------------------------------------------- appended columns
FACT_COLS = [
    ("Owner (D-RCV-60)", 22),
    ("Values from (D-RCV-60)", 62),
    ("Pattern (D-RCV-60)", 44),
]
E9 = "P9 rwb-reporting"
NOLK = "DP-17 no data lake"
FACT_VALUES = {
    5: (E9,
        "P3 rwb-case (recovery_case, queue, assignment, timer) · P1 rwb-source-data (ACE account rows, snapshot(page))",
        f"DP-09 events; DP-05 ACE rows through P1; {NOLK}"),
    6: (E9,
        "P7 rwb-decision (decision_log_entry central ledger) and each service's local decision record",
        f"DP-09 events on rwb.decision-record.v1; {NOLK}"),
    7: (E9,
        "S2 rwb-treatment (treatment) · P1 rwb-source-data (ACE plan rows, snapshot(page))",
        f"DP-09 events; DP-05 ACE rows through P1; {NOLK}"),
    8: (E9,
        "S4 rwb-litigation (legal_action, hearing) · P1 rwb-source-data (ACE lawsuit and hearing rows, snapshot(page))",
        f"DP-09 events; DP-05 ACE rows through P1; {NOLK}"),
    9: (E9,
        "S5 rwb-asset (asset_sale, listing) · P1 rwb-source-data (ACE asset rows, snapshot(page))",
        f"DP-09 events; DP-05 ACE rows through P1; {NOLK}"),
    10: (E9,
         "S6 rwb-debtsale (debt_sale_lot, debt_sale_account)",
         f"DP-09 events; {NOLK}"),
    11: (E9,
         "P8 rwb-payment (proceeds) · S7 rwb-writeoff (write_off) · P1 rwb-source-data (ACE payment and write-off rows, snapshot(page))",
         f"DP-09 events; DP-05 ACE rows through P1; {NOLK}"),
    12: (E9,
         "S9 rwb-partner (partner_instruction)",
         f"DP-09 events; {NOLK}"),
    13: (E9,
         "P1 rwb-source-data (ACE bucket log rows, snapshot(page))",
         f"DP-05 through P1; {NOLK}"),
}
DIM_COLS = [("Owner (D-RCV-60)", 22), ("Values from (D-RCV-60)", 64)]
DIM_VALUES = {
    5: (E9, "P1 rwb-source-data (ACE holiday rows through the ACE view contract)"),
    6: (E9, "P1 rwb-source-data (ACE product codes through the ACE view contract)"),
    7: (E9, "P3 rwb-case (LOV-ROUTE reference data)"),
    8: (E9, "P3 rwb-case (LOV-STAGE reference data)"),
    9: (E9, "P3 rwb-case (queue, queue_member, assignment)"),
    10: (E9, "S9 rwb-partner (partner, partner_user)"),
    11: (E9, "P7 rwb-decision (rule_package, rule_package_version)"),
    12: (E9, "P7 rwb-decision (decision_log_entry and the D1 to D9 decision model)"),
}
MEA_COLS = [("Owner (D-RCV-60)", 22), ("Served through (D-RCV-60)", 46)]
MEA_VALUE = "GET /dashboards/{id} · GET /reports/{id} behind gateway-bff"

# ---------------------------------------------------------------- read model sheet
RM_HEAD = ["Fact table", "Builds from topic", "Events", "Producer", "Late or replay rule", "Rebuild"]
RM_ROWS = [
    ["fact_case_daily", "rwb.case.events.v1 · rwb.source-data.events.v1",
     "CaseCreated, CaseAllocated, CaseTransferred, CaseStateChanged, AceDataReady",
     "P3 rwb-case · P1 rwb-source-data",
     "Inbox dedupe by event id; applied by business date; the day is reopened only while its measure_publish row is not Published",
     "Refold the retained topic history into rwb_reporting; no lake copy"],
    ["fact_decision", "rwb.decision-record.v1 · rwb.decision.events.v1", "DecisionRecorded",
     "P7 rwb-decision (central ledger) and every service's local record",
     "Inbox dedupe by event id; a decision is never overwritten, a later correction is a new entry",
     "Refold the retained topic history into rwb_reporting; no lake copy"],
    ["fact_treatment", "rwb.treatment.events.v1 · rwb.payment.events.v1",
     "TreatmentApproved, TreatmentClosed, TreatmentBooked", "S2 rwb-treatment · P8 rwb-payment",
     "Inbox dedupe by event id; the row is rebuilt from the treatment state carried on the event",
     "Refold the retained topic history into rwb_reporting; no lake copy"],
    ["fact_legal", "rwb.litigation.events.v1 · rwb.partner.events.v1",
     "JudgmentRecorded, AuctionResult, PartnerResultSubmitted", "S4 rwb-litigation · S9 rwb-partner",
     "Inbox dedupe by event id; a hearing or judgment arriving late reopens the action while the day is not frozen",
     "Refold the retained topic history into rwb_reporting; no lake copy"],
    ["fact_asset", "rwb.asset.events.v1 · rwb.litigation.events.v1",
     "AssetTakenOn, AssetSold, AuctionResult", "S5 rwb-asset · S4 rwb-litigation",
     "Inbox dedupe by event id; a month row is replaced whole on each event of that month until frozen",
     "Refold the retained topic history into rwb_reporting; no lake copy"],
    ["fact_lot", "rwb.debtsale.events.v1", "LotAwarded, AccountsTransferred", "S6 rwb-debtsale",
     "Inbox dedupe by event id; a lot row is replaced whole on each event until frozen",
     "Refold the retained topic history into rwb_reporting; no lake copy"],
    ["fact_recovery", "rwb.payment.events.v1 · rwb.writeoff.events.v1",
     "ProceedsMatched, PaymentMissed, WriteOffApproved", "P8 rwb-payment · S7 rwb-writeoff",
     "Inbox dedupe by event id; a receipt is applied once, keyed by its payment reference",
     "Refold the retained topic history into rwb_reporting; no lake copy"],
    ["fact_partner", "rwb.partner.events.v1", "InstructionIssued, PartnerResultSubmitted", "S9 rwb-partner",
     "Inbox dedupe by event id; the instruction row is replaced whole on the result event",
     "Refold the retained topic history into rwb_reporting; no lake copy"],
    ["fact_flow", "rwb.source-data.events.v1 (AceDataReady)", "AceDataReady", "P1 rwb-source-data",
     "Business date from AceDataReady; the month row is replaced whole from the P1 snapshot(page) result",
     "Rerun the P1 snapshot(page) activity for the month; no lake copy"],
]
CTRL_HEAD = ["Table", "Holds", "Owner", "Gate"]
CTRL_ROWS = [
    ["measure_definition", "The agreed definition, formula, unit and version of each measure", E9,
     "A definition change is a new definition_version, never an edit"],
    ["measure_snapshot", "The frozen value of one measure for a business date, product and dimension value", E9,
     "frozen = true once published; is_baseline marks the baseline date"],
    ["measure_publish", "Whether the day is published or held after reconciling to the case list", E9,
     "case_list_count must equal dashboard_count before status reads Published"],
]
RET_HEAD = ["Item", "v3", "v4", "Basis"]
RET_ROWS = [
    ["Landing place of the star schema", "Data lake", "rwb_reporting, the P9 own schema",
     "Architecture v5 slide 41; ADR-014; ADR-018; DP-17"],
    ["INT-19 Power BI feed and INT-20 data lake feed", "Data lake to Power BI",
     "Removed; dashboards and reports served by rwb-reporting through REST",
     "Architecture v5 slides 37 and 44; ADR-018; DP-17"],
    ["ACE read path", "recovery.v_ace_* views read by the reporting layer",
     "Read only by rwb-source-data (P1) through its ACE view contract and snapshot(page)",
     "Architecture v5 slide 41; ADR-010; DP-05"],
    ["Load of the Workbench rows", "Nightly from the recovery schema",
     "Event-fed projections, publish at 01:30 (JOB-15) behind the measure_publish gate",
     "Architecture v5 slides 31 and 44; ADR-018"],
    ["Decision log copy to the lake", "JOB-13 at 01:00 into the lake",
     "Continuous Kafka ingest into rwb-decision; no lake copy; RWB-E1-014 stays retired",
     "Architecture v5 slide 44; Template and Rules R6 (retired)"],
]

# ---------------------------------------------------------------- read me sheet
README = [
    ("SCB Collections and Recovery. Henka Group, 22 November 2026.", TITLE_FONT),
    ("(C) Siam Commercial Bank and Henka Pte Ltd", BODY_FONT),
    ("", None),
    ("Recovery Workbench Reporting and Analytics Data Model v4", TITLE_FONT),
    ("Next version of Recovery Workbench Reporting and Analytics Data Model v3.xlsx. "
     f"Decision {DEC} microservice realignment.", SUB_FONT),
    (f"Tool: {TOOL}.", SUB_FONT),
    ("", None),
    ("Change log", HDR_FONT),
    ("v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash", BODY_FONT),
    ("", None),
    ("What changed in v4", HDR_FONT),
    ("1. Facts sheet, note A2: the star schema is no longer in a data lake. It is the read model in "
     "rwb_reporting (P9), built from the business events on Kafka; INT-19 and INT-20 are removed "
     "(ADR-018; DP-17). ACE rows come through the ACE view contract of rwb-source-data (P1) on the "
     "snapshot(page) activity and are never read from recovery.v_ace_* by the reporting layer.", BODY_FONT),
    ("2. Facts sheet, Refresh column F5 to F13: the nine refresh cells no longer say 'Read through "
     "v_ace_*' or 'Nightly from the Workbench'. Each reads event-fed projections or a named event, with "
     "the 01:30 publish (JOB-15) and, for the five ACE-fed facts, the rwb-source-data contract.", BODY_FONT),
    ("3. Facts sheet: three columns are added at the end. Owner gives P9 rwb-reporting on all nine facts, "
     "Values from names the owning service and table of each input, and Pattern cites DP-09, DP-05 and "
     "DP-17. Columns A to F are unchanged except A2 and F5 to F13.", BODY_FONT),
    ("4. Dimensions sheet: two columns are added at the end, Owner (P9 on all eight) and Values from "
     "(P1, P3, P7 or S9 per dimension, from the Ownership Map sheet Tables). Columns A and B are "
     "unchanged, cell for cell.", BODY_FONT),
    ("5. Measures sheet: two columns are added at the end, Owner (P9 on all ten) and Served through "
     "(GET /dashboards/{id} and GET /reports/{id} behind gateway-bff). Columns A to C are unchanged.", BODY_FONT),
    ("6. Read model sheet: new. Row by row, how each of the nine fact tables is built from its topic, "
     "which events feed it, who produces them, the late-arrival rule and how it is rebuilt without a "
     "lake. Below it, the three P9 control tables and the five items the realignment retired or moved.", BODY_FONT),
    ("7. Read me: this sheet is new and carries the header of Template and Rules section R8.1 and the "
     "change-log row.", BODY_FONT),
    ("", None),
    ("What did not change", HDR_FONT),
    ("The nine fact tables keep their names, grains, dimensions, measures and source entities. The eight "
     "dimensions keep their names and what they hold. The ten measure definitions keep their names, "
     "formulas and the fact table each reads. Every identifier in the source is copied character for "
     "character: fact_case_daily, fact_decision, fact_treatment, fact_legal, fact_asset, fact_lot, "
     "fact_recovery, fact_partner, fact_flow, dim_date, dim_product, dim_route, dim_stage, dim_org, "
     "dim_partner, dim_rule, dim_decision, and the LOV codes LOV-ROUTE and LOV-STAGE.", BODY_FONT),
    ("The source carries no version number, no release date and no named person in any of its three "
     "sheets, so no release date is marked (tentative) and no date is changed.", BODY_FONT),
    ("", None),
    ("Counts", HDR_FONT),
    ("Facts: 9 fact tables over 9 fact rows; 3 appended columns on 9 rows. Dimensions: 8 tables, 2 "
     "appended columns on 8 rows. Measures: 10 measures, 2 appended columns on 10 rows. Read model: 9 "
     "build rows, 3 control tables and 5 retired or moved items.", BODY_FONT),
    ("Changed v3 cells: 10 (Facts!A2 and Facts!F5 to F13). Appended cells: 3 headers and 27 values on "
     "Facts, 2 headers and 16 values on Dimensions, 2 headers and 20 values on Measures.", BODY_FONT),
    ("", None),
    ("Open points", HDR_FONT),
    ("CG-B-DATA-23-1 to CG-B-DATA-23-8 and ASM-B-DATA-23-1 to ASM-B-DATA-23-8 in the Gap and Assumption "
     "registers hold the questions this version leaves open. Each is cited on the sheet it affects in "
     "the build note under _work/msr/docs/B-DATA-23/.", BODY_FONT),
]


def put(ws, r, c, value, font=None, fill=None, like=None):
    cell = ws.cell(row=r, column=c, value=value)
    if like is not None:
        cell._style = _copy(like._style)
    if font is not None:
        cell.font = font
    if fill is not None:
        cell.fill = fill
    cell.alignment = WRAP
    return cell


wb = openpyxl.load_workbook(V4)

# ---------------------------------------------------------------- changed cells
for (sheet, addr), value in CHANGED.items():
    wb[sheet][addr] = value
print("changed cells", len(CHANGED))

# ---------------------------------------------------------------- Facts columns
ws = wb["Facts"]
assert ws.max_row == 13 and ws.max_column == 6
hdr, body, bold = ws["A4"], ws["A5"], ws["A5"]
for i, (name, width) in enumerate(FACT_COLS, start=7):
    put(ws, 4, i, name, like=hdr)
    ws.column_dimensions[get_column_letter(i)].width = width
for r in range(5, 14):
    owner, values, pattern = FACT_VALUES[r]
    put(ws, r, 7, owner, like=body)
    put(ws, r, 8, values, like=body)
    put(ws, r, 9, pattern, like=body)
ws.auto_filter.ref = "A4:I13"
print("Facts rows", ws.max_row - 4)

# ---------------------------------------------------------------- Dimensions columns
ws = wb["Dimensions"]
assert ws.max_row == 12 and ws.max_column == 2
hdr, body = ws["A4"], ws["A5"]
for i, (name, width) in enumerate(DIM_COLS, start=3):
    put(ws, 4, i, name, like=hdr)
    ws.column_dimensions[get_column_letter(i)].width = width
for r in range(5, 13):
    owner, values = DIM_VALUES[r]
    put(ws, r, 3, owner, like=body)
    put(ws, r, 4, values, like=body)
ws.auto_filter.ref = "A4:D12"
print("Dimensions rows", ws.max_row - 4)

# ---------------------------------------------------------------- Measures columns
ws = wb["Measures"]
assert ws.max_row == 14 and ws.max_column == 3
hdr, body = ws["A4"], ws["A5"]
for i, (name, width) in enumerate(MEA_COLS, start=4):
    put(ws, 4, i, name, like=hdr)
    ws.column_dimensions[get_column_letter(i)].width = width
for r in range(5, 15):
    put(ws, r, 4, E9, like=body)
    put(ws, r, 5, MEA_VALUE, like=body)
ws.auto_filter.ref = "A4:E14"
print("Measures rows", ws.max_row - 4)


# ---------------------------------------------------------------- read model sheet
def section(ws, r, title, note, head, rows, widths):
    ws.cell(row=r, column=1, value=title).font = TITLE_FONT
    ws.cell(row=r + 1, column=1, value=note).font = SUB_FONT
    hr = r + 3
    for i, h in enumerate(head, start=1):
        put(ws, hr, i, h, font=HDR_FONT, fill=HDR_FILL)
    for j, row in enumerate(rows, start=hr + 1):
        for i, v in enumerate(row, start=1):
            put(ws, j, i, v, font=BODY_FONT)
    return hr + len(rows)


ws = wb.create_sheet("Read model")
ws.sheet_view.showGridLines = False
for i, w in enumerate((22, 34, 46, 34, 58, 50), start=1):
    ws.column_dimensions[get_column_letter(i)].width = w
end = section(ws, 1, "Read model",
              "How each fact table is built in rwb_reporting (P9) from the service topics. The projections are "
              "the only input; there is no data lake (INT-19 and INT-20 removed; ADR-018; DP-17).",
              RM_HEAD, RM_ROWS, None)
end = section(ws, end + 2, "Read-model controls",
              "The P9 tables that hold the definitions, the frozen values and the publish gate.",
              CTRL_HEAD, CTRL_ROWS, None)
section(ws, end + 2, "Retired or moved in v4 (D-RCV-60)",
        "The five items the realignment changed, with the source that decides each one.",
        RET_HEAD, RET_ROWS, None)
print("Read model rows", len(RM_ROWS) + len(CTRL_ROWS) + len(RET_ROWS))

# ---------------------------------------------------------------- read me sheet
ws = wb.create_sheet("Read me", 0)
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 130
for i, (text, font) in enumerate(README, start=1):
    if text == "":
        continue
    c = ws.cell(row=i, column=1, value=text)
    if font is not None:
        c.font = font
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if font is TITLE_FONT or font is HDR_FONT:
        ws.row_dimensions[i].height = 18

wb.save(V4)
print("WROTE", V4)
print("sheets", wb.sheetnames)
