"""Build Recovery Workbench Source to Target Mapping v5 from the copied v4.

Reads the copied v5 workbook, adds the D-RCV-60 realignment columns, the new
mapping-rule rows and the Read me sheet. Every v4 cell is left as it is, except
the one 'By source' cell recorded in CG-B-DATA-18-3.
"""
import json
from copy import copy as _copy

import openpyxl
from openpyxl.styles import Font, Alignment

V5 = "06 Data/Recovery Workbench Source to Target Mapping v5.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"

# ---------------------------------------------------------------- ownership
owb = openpyxl.load_workbook(OWN)
otab = owb["Tables"]
owner_of, schema_of = {}, {}
for row in otab.iter_rows(min_row=2, values_only=True):
    if not row or not row[0]:
        continue
    owner_of[str(row[0])] = str(row[1])
    schema_of[str(row[0])] = str(row[2])

# ACE-side entities: not Workbench tables; read through rwb-source-data (ADR-010, DP-05).
ACE_ENTITIES = {
    "party", "contact_point", "loan_account", "account_payment", "collateral",
    "account_collateral", "valuation", "asset", "score", "collections_history",
    "party_product",
}
RWBSRC = ("rwb_source_data", "P1")

wb = openpyxl.load_workbook(V5)

# ---------------------------------------------------------------- Mapping sheet
ws = wb["Mapping"]
assert ws.max_column == 14, ws.max_column
hdr_font = _copy(ws["A1"].font)
hdr_align = _copy(ws["A1"].alignment)
hdr_fill = _copy(ws["A1"].fill)
ws.cell(row=1, column=15, value="Target schema")
ws.cell(row=1, column=16, value="Owning service")
for c in (15, 16):
    cell = ws.cell(row=1, column=c)
    cell.font = hdr_font
    cell.alignment = hdr_align
    cell.fill = hdr_fill
ws.column_dimensions["O"].width = 20
ws.column_dimensions["P"].width = 15

seen = {}
for r in range(2, ws.max_row + 1):
    ent = ws.cell(row=r, column=3).value
    ent = str(ent).strip() if ent else ""
    if not ent:
        raise SystemExit(f"row {r} has no Workbench entity")
    seen[ent] = seen.get(ent, 0) + 1
    if ent in ACE_ENTITIES:
        schema, owner = RWBSRC
    else:
        schema, owner = schema_of.get(ent), owner_of.get(ent)
        if not schema:
            raise SystemExit(f"entity {ent} (row {r}) is not in the Ownership Map Tables sheet")
    ws.cell(row=r, column=15, value=schema)
    ws.cell(row=r, column=16, value=owner)

print("mapping rows", ws.max_row - 1, "entities", len(seen))
print("owned entities", {k: v for k, v in seen.items() if k not in ACE_ENTITIES})

# ---------------------------------------------------------------- ACE gaps sheet
wg = wb["ACE gaps"]
assert wg.max_column == 8, wg.max_column
wg.cell(row=1, column=9, value="Target schema")
wg.cell(row=1, column=10, value="Owning service")
for c in (9, 10):
    cell = wg.cell(row=1, column=c)
    cell.font = hdr_font
    cell.alignment = hdr_align
    cell.fill = hdr_fill
wg.column_dimensions["I"].width = 20
wg.column_dimensions["J"].width = 15
for r in range(2, wg.max_row + 1):
    if wg.cell(row=r, column=1).value in (None, ""):
        continue
    wg.cell(row=r, column=9, value=RWBSRC[0])
    wg.cell(row=r, column=10, value=RWBSRC[1])
print("ace gap rows", wg.max_row - 1)

# ---------------------------------------------------------------- By source (one cell)
wbys = wb["By source"]
fixed = 0
for r in range(2, wbys.max_row + 1):
    if wbys.cell(row=r, column=1).value == "Aric via COLLINS":
        assert wbys.cell(row=r, column=8).value == "recovery"
        wbys.cell(row=r, column=8, value="rwb_source_data.party_ext")
        fixed += 1
assert fixed == 1, fixed

# ---------------------------------------------------------------- Mapping rules
wmr = wb["Mapping rules"]
assert wmr.max_row == 11, wmr.max_row
NEW_RULES = [
    ("Target schema (D-RCV-60)",
     "Every Workbench field lands in the schema of its owner, rwb_<name>, taken row by row from the Ownership Map sheet Tables. No field lands in the monolith schema recovery and no service reads another service's tables (DP-01, DP-02)."),
    ("Owning service (D-RCV-60)",
     "One owner per field, from the Ownership Map sheet Tables: P1 rwb-source-data, P3 rwb-case, P4 rwb-access, P5 rwb-document, P6 rwb-comms, P7 rwb-decision, P8 rwb-payment, S2 rwb-treatment, S4 rwb-litigation, S5 rwb-asset, S6 rwb-debtsale and S7 rwb-writeoff."),
    ("ACE reads (D-RCV-60)",
     "Only rwb-source-data reads the 30 recovery.v_ace_* views, over a read-only login (ADR-010, Architecture v5 slide 29). Every other service asks rwb-source-data through REST or a Temporal activity, so a field whose read path is v_ace_* is owned by P1 and read through its contract (DP-05)."),
    ("ACE-side entities (D-RCV-60)",
     "party, contact_point, loan_account, account_payment, collateral, account_collateral, valuation, asset, score, collections_history and party_product are ACE entities, not Workbench tables. Their target schema is rwb_source_data, where the ACE view contract lives; they are not copied into a service schema."),
    ("Extension fields (D-RCV-60)",
     "party_ext, contact_point_ext, account_ext and valuation_ext are Workbench tables in rwb_source_data. A source row links to its extension row by business key; the extension value is never read by another service directly."),
    ("Cross-service links (D-RCV-60)",
     "A link across two services is a business key (varchar 255) and a contract call, never a foreign key; a foreign key stays only inside one rwb_<name> schema (DP-01, DP-11)."),
    ("Migration and load (D-RCV-60)",
     "There is still no load-time transform: a rename or a type cast happens in the recovery.v_ace_* view. Each service owns its Flyway sequence in its own schema (DP-15); no row of this mapping is migrated by another service."),
    ("Status after realignment (D-RCV-60)",
     "'Ready' is unchanged. 'Waiting on RWB-ACE-001' keeps its v4 wording; the legacy key RWB-ACE-001 is carried by the ACE DB story RWB-P1-ACE001-DB, and the dependent feature stays behind its flag until that story is done."),
]
start = wmr.max_row + 1
for i, (rule, detail) in enumerate(NEW_RULES):
    wmr.cell(row=start + i, column=1, value=rule)
    wmr.cell(row=start + i, column=2, value=detail)
print("mapping rules", wmr.max_row - 1)

# ---------------------------------------------------------------- Read me sheet
rm = wb.create_sheet("Read me", 0)
rm.column_dimensions["A"].width = 132
lines = [
    "SCB Collections and Recovery. Henka Group, 22 November 2026.",
    "(C) Siam Commercial Bank and Henka Pte Ltd",
    "",
    "Recovery Workbench Source to Target Mapping v5",
    "Next version of Recovery Workbench Source to Target Mapping v4.xlsx. Decision D-RCV-60 microservice realignment.",
    "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.",
    "",
    "Change log",
    "v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash",
    "",
    "What changed in v5",
    "1. Mapping sheet: two columns are added at the end. 'Target schema' gives rwb_<name> and 'Owning service' gives the owner code, row by row from the Ownership Map sheet Tables. Columns A to N are unchanged, cell for cell.",
    "2. ACE gaps sheet: the same two columns are added at the end. Every one of the 80 fields ACE must add is read through rwb-source-data, so the target schema is rwb_source_data and the owner is P1.",
    "3. By source sheet: one cell changes. The extension field from Aric via COLLINS no longer lands in the monolith schema recovery; its ACE table cell reads rwb_source_data.party_ext. Every count and the Total row are unchanged.",
    "4. Mapping rules sheet: eight rules are added for the target schema, the owner per field, the ACE read path, the ACE-side entities, the extension tables, cross-service links, migration and the status text. The ten v4 rules are unchanged, word for word.",
    "5. Read me: this sheet is new and carries the header of Template and Rules section R8.1 and the change-log row.",
    "",
    "What did not change",
    "Every Field ID, data product, Workbench entity, Workbench field, data type, mandatory flag, source system, source field, ACE object column, read path, transformation, frequency, interface and status is copied from v4 unchanged. The 80 ACE gap rows are unchanged. The 18 'By source' rows keep their counts: 133 fields, 52 ACE reuse, 80 ACE new and 1 extension.",
    "The source carries no release date, so no date is marked (tentative) and no date is changed. The 81 field rows that carry no data product in v4 still carry none, because no source assigns one (CG-B-DATA-18-7; ASM-B-DATA-18-7).",
    "",
    "Counts",
    "Mapping: 133 field rows over 25 Workbench entities and 17 source systems.",
    "ACE gaps: 80 rows. By source: 17 source rows and 1 Total row. Mapping rules: 10 v4 rules plus 8 new rules.",
    "",
    "Open points",
    "CG-B-DATA-18-1 to CG-B-DATA-18-7 and ASM-B-DATA-18-1 to ASM-B-DATA-18-7 in the Gap and Assumption registers hold the questions this version leaves open. Each is cited on the sheet it affects in the build note under _work/msr/docs/B-DATA-18/.",
]
for i, line in enumerate(lines, start=1):
    c = rm.cell(row=i, column=1, value=line)
    if i in (1, 2):
        c.font = Font(bold=True)
    if i == 4:
        c.font = Font(bold=True, size=13)
    if i in (8, 11, 18, 22, 27):
        c.font = Font(bold=True)
    c.alignment = Alignment(vertical="top", wrap_text=True)
rm.sheet_view.showGridLines = False

wb.active = 0
wb.save(V5)
print("saved", V5, wb.sheetnames)
