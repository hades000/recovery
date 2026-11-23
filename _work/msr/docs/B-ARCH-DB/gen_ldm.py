"""Append the D-RCV-60 sheets to LDM v9 and put the R8.1 header sheet first."""
import json
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[4]
XLSX = ROOT / "06 Data" / "Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx"
OM = json.load(open(ROOT / "_work" / "msr" / "plan" / "ownership.json", encoding="utf-8"))
REP = json.load(open(Path(__file__).resolve().parent / "schema_report.json", encoding="utf-8"))

DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
SERVICES = [
    ("P1", "rwb-source-data", "Source data", 1, "rwb_source_data"),
    ("P2", "rwb-integration", "Integration", 1, "rwb_integration"),
    ("P3", "rwb-case", "Case and workflow", 1, "rwb_case"),
    ("P4", "rwb-access", "Access and authority", 1, "rwb_access"),
    ("P5", "rwb-document", "Document", 1, "rwb_document"),
    ("P6", "rwb-comms", "Communications", 1, "rwb_comms"),
    ("P7", "rwb-decision", "Decision and rules", 1, "rwb_decision"),
    ("P8", "rwb-payment", "Payment", 2, "rwb_payment"),
    ("P9", "rwb-reporting", "Reporting", 1, "rwb_reporting"),
    ("P10", "rwb-agent", "Agent", 1, "rwb_agent"),
    ("S1", "rwb-valuation", "Valuation and route", 3, "rwb_valuation"),
    ("S2", "rwb-treatment", "Treatment and offer", 2, "rwb_treatment"),
    ("S3", "rwb-guarantee", "Guarantee", 3, "rwb_guarantee"),
    ("S4", "rwb-litigation", "Litigation", 3, "rwb_litigation"),
    ("S5", "rwb-asset", "Asset", 2, "rwb_asset"),
    ("S6", "rwb-debtsale", "Debt sale", 3, "rwb_debtsale"),
    ("S7", "rwb-writeoff", "Write-off", 4, "rwb_writeoff"),
    ("S8", "rwb-deviation", "Deviation", 2, "rwb_deviation"),
    ("S9", "rwb-partner", "Partner", 4, "rwb_partner"),
]
CODE = {c: (svc, name, wave, schema) for c, svc, name, wave, schema in SERVICES}
SCHEMA = {c: s for c, _, _, _, s in SERVICES}
LIBRARY = {"outbox_event", "outbox_delivery", "processed_event", "idempotency_key"}
HOSTED = {"feature_flag", "feature_flag_change"}
EXT = {"party_ext", "contact_point_ext", "account_ext", "valuation_ext"}


def style_header(ws, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="DDEBF7")
        cell.alignment = Alignment(wrap_text=True, vertical="top")


def widths(ws, w):
    for i, x in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(i)].width = x


def read_me(wb):
    ws = wb.create_sheet("Read me", 0)
    rows = [
        ("SCB Collections and Recovery. Henka Group, 22 November 2026.", None),
        ("(C) Siam Commercial Bank and Henka Pte Ltd", None),
        (None, None),
        ("Recovery Workbench Logical Data Model and Data Dictionary v9", None),
        (None, None),
        ("Item", "Value"),
        ("Version", "9"),
        ("Date", "22 November 2026"),
        ("Change log", f"9, 22 November 2026, {DEC} microservice realignment, {TOOL}"),
        ("Source", "06 Data/Recovery Workbench Logical Data Model and Data Dictionary v8.xlsx (read only, version 8)"),
        ("Decision", "D-RCV-60: adopt Architecture v5 and realign the documents and stories"),
        ("Tool", TOOL),
        ("What changed", "The 123 entities gain an owner service and a target schema from the Microservice Ownership Map v1; the 48 foreign keys that cross an owner boundary become plain uuid references; the six platform library objects are placed; no entity, field, list of values, relationship or ACE mapping row is removed or reworded."),
        ("Unchanged sheets", "Entities, Fields, Standard columns, Lists of values, Loaded lists, ACE mapping, Relationships, Sources, Key"),
        ("New sheets", "Service ownership, Schema map, Cross-service references, Realignment change log"),
        ("Counts", "123 entities: 89 Workbench tables, 4 extension tables and 30 ACE views; 1392 fields; 124 closed lists with 598 values; 119 references"),
        ("Owner source", "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx, sheet Tables"),
    ]
    for r in rows:
        ws.append(list(r))
    ws["A1"].font = Font(bold=True)
    ws["A4"].font = Font(bold=True, size=14)
    ws["A6"].font = Font(bold=True)
    ws["B6"].font = Font(bold=True)
    widths(ws, [22, 120])
    for row in ws.iter_rows(min_row=7, max_row=ws.max_row):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")


def service_ownership(wb):
    ws = wb.create_sheet("Service ownership")
    ws.append(["Entity", "Kind", "Owner code", "Service", "Schema", "Wave", "Note"])
    ent = wb["Entities"]
    ents = [r[0] for r in ent.iter_rows(min_row=5, values_only=True) if r[0]]
    tables = OM["tables"]
    for e in ents:
        if e in tables:
            owner = tables[e]["owner"]
            if e in LIBRARY:
                code, svc, _, schema = "PLT", "platform library", 0, "every rwb_<service> schema"
                note = "Created in every service schema (DP-09; ownership ruling ASM-A6-tables-8); no FK to a business table."
            elif e in HOSTED:
                code, svc, _, schema = "PLT", "platform library", 0, "rwb_integration"
                note = "Platform library owned by PLT; emitted once in rwb_integration for the feature-flag admin API (ruling ASM-A6-api-2; ASM-B-ARCH-DB-3)."
            else:
                svc, _, wave, schema = CODE[owner]
                code, note = owner, tables[e].get("ruling") or "Owner from Ownership Map v1, sheet Tables."
                if e == "lake_copy_watermark":
                    note = "No target: the data lake is removed (DP-17) and JOB-13 is continuous Kafka ingest; the DDL is kept and marked for retirement (ASM-A6-tables-13; CG-B-ARCH-DB-8)."
            kind = "Extension table" if e in EXT else "Workbench table"
        else:
            code, svc, schema, wave = "P1", "rwb-source-data", "recovery", 1
            kind = "ACE view"
            note = "Read-only ACE view; P1 owns the ACE view contract (Architecture v5 slide 29; DP-05)."
        ws.append([e, kind, code, svc, schema, wave, note])
    style_header(ws, 7)
    widths(ws, [34, 18, 12, 26, 34, 8, 90])


def schema_map(wb):
    ws = wb.create_sheet("Schema map")
    ws.append(["Code", "Service", "Name", "Wave", "Schema", "Login", "REST base", "Topic", "Queue", "Tables owned", "Hosted PLT tables", "Library objects"])
    tcount, hcount = {}, {}
    for e, v in OM["tables"].items():
        if e in LIBRARY:
            continue
        if e in HOSTED:
            hcount["P2"] = hcount.get("P2", 0) + 1
        else:
            tcount[v["owner"]] = tcount.get(v["owner"], 0) + 1
    for c, svc, name, wave, schema in SERVICES:
        short = svc[4:]
        ws.append([c, svc, name, wave, schema, schema, f"/api/recovery/{short}/v1", f"rwb.{short}.events.v1", svc, tcount.get(c, 0), hcount.get(c, 0), 4])
    style_header(ws, 12)
    widths(ws, [8, 20, 22, 8, 22, 22, 32, 34, 20, 12, 14, 14])


def cross_refs(wb):
    ws = wb.create_sheet("Cross-service references")
    ws.append(["#", "From table", "From owner", "From service", "Column", "To table", "To owner", "To service", "Becomes"])
    for i, c in enumerate(REP["cuts"], 1):
        fs = CODE.get(c["from_owner"], ("platform library",))[0]
        ts = CODE.get(c["to_owner"], ("platform library",))[0]
        ws.append([i, c["from"], c["from_owner"], fs, c["column"], c["to"], c["to_owner"], ts,
                   f"plain uuid; integrity through the {ts} contract"])
    style_header(ws, 9)
    widths(ws, [6, 22, 12, 22, 24, 24, 12, 22, 50])
    ws.freeze_panes = "A2"


def change_log(wb):
    ws = wb.create_sheet("Realignment change log")
    ws.append(["Version", "Date", "Change", "Decision", "Tool"])
    ws.append([9, "22 November 2026", "D-RCV-60 microservice realignment: owner service and target schema per entity, FK cuts, library placement, new sheets", DEC, TOOL])
    ws.append([8, "16 November 2026", "Source version (read only)", "-", "-"])
    style_header(ws, 5)
    widths(ws, [8, 18, 100, 14, 44])


def main():
    wb = openpyxl.load_workbook(XLSX)
    read_me(wb)
    service_ownership(wb)
    schema_map(wb)
    cross_refs(wb)
    change_log(wb)
    wb.save(XLSX)
    print("WROTE", XLSX.name, wb.sheetnames)


if __name__ == "__main__":
    main()
