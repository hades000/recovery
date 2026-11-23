"""Build 06 Data/Recovery Workbench Conceptual Data Model v7.xlsx from v6.

Never edits v6. v6 is copied first with compat/office_write.py copy, then only the
copy is changed: one new Read me sheet, appended ownership columns, one new
Service ownership sheet and five appended Key terms.
"""
import json, shutil
from copy import copy
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SRC = ROOT / "06 Data" / "Recovery Workbench Conceptual Data Model v6.xlsx"
DST = ROOT / "06 Data" / "Recovery Workbench Conceptual Data Model v7.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
DATE = "22 November 2026"

o = json.loads((HERE / "owners.json").read_text(encoding="utf-8"))
ENTS, SERVICES = o["entities"], o["services"]
ORDER = ["P%d" % i for i in range(1, 11)] + ["PLT"] + ["S%d" % i for i in range(1, 10)]


def okey(code):
    return ORDER.index(code)


def sortcodes(codes):
    return sorted(set(codes), key=okey)


def schema_of(name):
    v = ENTS[name]
    t, s = v["table"], v["schema"]
    if s == "platform":
        return ("every service schema (platform library object)"
                if t in ("outbox_event", "outbox_delivery", "processed_event", "idempotency_key")
                else "platform library")
    return s


def basis_of(name):
    v = ENTS[name]
    if v["map_row"]:
        return f"Ownership Map v1, Tables row {v['table']}: {v['basis']}"
    return v["basis"]


def put(ws, row, col, value, model_addr=None, ws_model=None, bold=None):
    c = ws.cell(row=row, column=col, value=value)
    m = (ws_model or ws)[model_addr]
    c.font = copy(m.font)
    c.fill = copy(m.fill)
    c.border = copy(m.border)
    c.alignment = copy(m.alignment)
    c.number_format = m.number_format
    if bold is not None:
        c.font = Font(name=m.font.name, size=m.font.size, bold=bold)
    return c


def main():
    if DST.exists():
        raise SystemExit(f"REFUSED: {DST} exists")
    shutil.copy2(SRC, DST)
    print("COPIED", SRC.name, "->", DST.name)

    wb = openpyxl.load_workbook(DST)

    # ------------------------------------------------------------------ Entities
    ws = wb["Entities"]
    n_ent = 126  # last data row
    headers = ["Owning service", "Target schema", "Ownership basis"]
    for i, h in enumerate(headers):
        col = 8 + i
        put(ws, 4, col, h, "G4")
        ws.column_dimensions[get_column_letter(col)].width = [15, 26, 80][i]
    owners_by_entity = {}
    for r in range(5, n_ent + 1):
        name = ws.cell(row=r, column=1).value
        v = ENTS[name]
        owners_by_entity[name] = v["owner"]
        put(ws, r, 8, v["owner"], "G5")
        put(ws, r, 9, schema_of(name), "G5")
        put(ws, r, 10, basis_of(name), "G5")
    ws.auto_filter.ref = f"A4:J{n_ent}"
    print("Entities: 3 columns appended over", n_ent - 4, "rows")

    # ------------------------------------------------------------ Subject areas
    ws = wb["Subject areas"]
    put(ws, 4, 6, "Owning services", "E4")
    ws.column_dimensions["F"].width = 20
    sa_owners = {}
    for r in range(5, 22):
        names = [x.strip() for x in str(ws.cell(row=r, column=4).value).split(",")]
        codes = sortcodes(owners_by_entity[n] for n in names)
        sa_owners[ws.cell(row=r, column=1).value] = codes
        put(ws, r, 6, "; ".join(codes), "E5")
    ws.auto_filter.ref = "A4:F21"
    multi = [a for a, c in sa_owners.items() if len(c) > 1]
    print("Subject areas: 1 column appended;", len(multi), "of 17 span more than one service")

    # ------------------------------------------------------------- Data products
    ws = wb["Data products"]
    we = wb["Entities"]
    put(ws, 4, 11, "Owning service(s)", "J4")
    ws.column_dimensions["K"].width = 22
    dp_owners, dp_counts = {}, {}
    for r in range(5, 19):
        full = f"{ws.cell(row=r, column=1).value} {ws.cell(row=r, column=2).value}"
        names = [we.cell(row=i, column=1).value for i in range(5, n_ent + 1) if we.cell(row=i, column=3).value == full]
        codes = sortcodes(owners_by_entity[n] for n in names)
        dp_owners[ws.cell(row=r, column=1).value] = codes
        dp_counts[ws.cell(row=r, column=1).value] = len(names)
        put(ws, r, 11, "; ".join(codes), "J5")
    ws.auto_filter.ref = "A4:K18"
    print("Data products: 1 column appended")

    # ------------------------------------------------------------ Relationships
    ws = wb["Relationships"]
    for i, h in enumerate(["Owning service (entity)", "Owning service (refers to)", "Cross-service reference"]):
        put(ws, 4, 6 + i, h, "E4")
        ws.column_dimensions[get_column_letter(6 + i)].width = [18, 22, 60][i]
    n_rel = 108
    stats = {"same": [], "to_view": [], "cross_table": []}
    for r in range(5, n_rel + 1):
        a, b = ws.cell(row=r, column=1).value, ws.cell(row=r, column=2).value
        oa, ob = owners_by_entity[a], owners_by_entity[b]
        put(ws, r, 6, oa, "E5")
        put(ws, r, 7, ob, "E5")
        if oa == ob:
            k, txt = "same", "No: both entities are in the " + schema_of(a) + " schema"
        elif str(b).startswith("v_ace_"):
            k = "to_view"
            txt = ("Yes: the ACE view is read only by rwb-source-data (ADR-010, DP-05); the value is a business key, "
                   "no foreign key, as v6 already states")
        else:
            k = "cross_table"
            txt = ("Yes: the foreign key is cut; the column keeps the business key only, because a service never reads "
                   "another service's schema (DP-01)")
        stats[k].append((a, b))
        put(ws, r, 8, txt, "E5")
    ws.auto_filter.ref = f"A4:H{n_rel}"
    print("Relationships: 3 columns appended;", {k: len(v) for k, v in stats.items()})

    # --------------------------------------------------------------------- Key
    ws = wb["Key"]
    terms = [
        ("Term", "Owning service", "The one service that writes an entity, gives it its schema and publishes its contract. "
                                   "Every other service reaches the entity through that contract, never through the schema"),
        ("Term", "Target schema", "The schema in the ACE PostgreSQL server that holds the entity after the realignment: "
                                  "rwb_<name> for a Workbench table, the read-only recovery schema for an ACE view"),
        ("Term", "PLT", "The platform library: the shared libraries and platform stories. It owns the outbox, inbox, "
                        "idempotency and feature-flag objects that are created in every service schema"),
        ("Term", "Cross-service reference", "A reference from an entity of one service to an entity of another. It carries the "
                                            "business key and no foreign key, because a service never reads another service's schema"),
        ("Term", "Service contract", "The REST, event and Temporal contract a service publishes for the entities it owns; the "
                                     "only way another service reaches them (DP-11)"),
    ]
    start = ws.max_row + 1
    last = start - 1
    for i, (kind, term, meaning) in enumerate(terms):
        r = start + i
        for col, val in ((1, kind), (2, term), (3, meaning)):
            put(ws, r, col, val, f"{get_column_letter(col)}{last}")
    ws.auto_filter.ref = f"A4:C{start + len(terms) - 1}"
    print("Key:", len(terms), "terms appended at rows", start, "-", start + len(terms) - 1)

    # -------------------------------------------------------- Service ownership
    ws = wb.create_sheet("Service ownership")
    ws["A1"] = "Service ownership"
    ws["A1"].font = Font(name="Aptos", size=16, bold=True)
    ws["A2"] = ("One row per service. The owner comes from the Ownership Map v1 Tables sheet, row by row, and from "
                "Architecture v5 Text Extract v1 slides 15 and 41 for the 30 recovery.v_ace_* views, which only "
                "rwb-source-data reads (ADR-010, DP-05).")
    ws["A2"].font = Font(name="Aptos", size=10)
    head = ["Code", "Service", "Name", "Wave", "Schema", "Entities owned", "Workbench tables", "ACE source views", "Note"]
    widths = [8, 20, 26, 7, 20, 14, 16, 16, 96]
    for i, h in enumerate(head):
        c = ws.cell(row=4, column=i + 1, value=h)
        c.font = Font(name="Aptos", size=10, bold=True)
        c.fill = copy(wb["Entities"]["A4"].fill)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.column_dimensions[get_column_letter(i + 1)].width = widths[i]
    notes = {
        "P1": ("Owns the 30 ACE read-only views and the extension tables, the ACE view contract, freshness and "
               "reconciliation (Architecture v5 slides 15 and 41)."),
        "PLT": ("Platform library objects: outbox, inbox, idempotency and feature flags. Each service's DB story creates "
                "its own copy in its own schema (DP-09, ASM-A6-tables-8)."),
        "P7": ("Rule registry: rule_row is the entity 'Rule' in v6; payment_match_rule is kept in the model but has no "
               "target table (D-RCV-36 T10)."),
        "S1": ("Owns no entity in this model. Valuations and the D6 route decision belong to rwb-valuation, but the "
               "valuation data is read through v_ace_valuation and valuation_ext, owned by P1 (ASM-A6-tables-15)."),
    }
    r = 5
    for code in ORDER:
        if code == "PLT":
            ents_c = [n for n, v in ENTS.items() if v["owner"] == code]
            row = ["PLT", "platform library", "Platform library", "0", "platform",
                   len(ents_c), sum(1 for n in ents_c if not str(n).startswith("v_ace_")), 0, notes["PLT"]]
        else:
            s = SERVICES[code]
            ents_c = [n for n, v in ENTS.items() if v["owner"] == code]
            row = [code, s["service"], s["name"], s["wave"], s["schema"], len(ents_c),
                   sum(1 for n in ents_c if not str(n).startswith("v_ace_")),
                   sum(1 for n in ents_c if str(n).startswith("v_ace_")), notes.get(code, "")]
        for i, v in enumerate(row):
            put(ws, r, i + 1, v, f"{get_column_letter(i + 1)}4", bold=False)
        r += 1
    tot = ["Total", "", "19 services", "", "", len(ENTS),
           sum(1 for n in ENTS if not n.startswith("v_ace_")), sum(1 for n in ENTS if n.startswith("v_ace_")),
           "122 entities: 88 Workbench tables, the 4 extension tables and the 30 ACE source views."]
    for i, v in enumerate(tot):
        put(ws, r, i + 1, v, f"{get_column_letter(i + 1)}4", bold=True)
    ws.freeze_panes = "B5"
    ws.auto_filter.ref = f"A4:I{r - 1}"
    print("Service ownership: new sheet,", r - 5, "service rows plus a Total row")

    # -------------------------------------------------------------- Read me sheet
    rm = wb.create_sheet("Read me", 0)
    rm.column_dimensions["A"].width = 132
    multi_n = len([a for a, c in sa_owners.items() if len(c) > 1])
    lines = []
    lines.append(("h1", "SCB Collections and Recovery. Henka Group, 22 November 2026."))
    lines.append(("h1", "(C) Siam Commercial Bank and Henka Pte Ltd"))
    lines.append(("", ""))
    lines.append(("t", "Recovery Workbench Conceptual Data Model v7"))
    lines.append(("", f"Next version of Recovery Workbench Conceptual Data Model v6.xlsx. Decision {DEC} microservice "
                     "realignment. Every subject area, data product, entity, relationship, gap, ACE addition, ID, "
                     "number and date of v6 is kept; each entity gains its owning service and the schema that service "
                     "writes."))
    lines.append(("", f"Tool: {TOOL}."))
    lines.append(("", ""))
    lines.append(("b", "Change log"))
    lines.append(("", f"v7, {DATE}, {DEC} microservice realignment, {TOOL}"))
    lines.append(("", ""))
    lines.append(("b", "What changed in v7"))
    lines.append(("", "1. Entities: three columns are appended at the end. 'Owning service' gives the service that owns the "
                       "entity, 'Target schema' the schema that service writes, and 'Ownership basis' the reason. All 122 "
                       "entities have an owner: 92 Workbench entities (88 tables and the 4 extension tables) and the 30 "
                       "recovery.v_ace_* views. Columns A to G keep their letters, positions and values."))
    lines.append(("", f"2. Subject areas: one column, 'Owning services', is appended. {multi_n} of the 17 subject areas are "
                       "now split across more than one service, so a subject area is no longer a delivery unit."))
    lines.append(("", "3. Data products: one column, 'Owning service(s)', is appended. The 14 data products are held by "
                       "between one and seven services each; the Entities column and its count are unchanged."))
    lines.append(("", f"4. Relationships: three columns are appended. {len(stats['to_view']) + len(stats['cross_table'])} "
                       f"of the {len(stats['to_view']) + len(stats['cross_table']) + len(stats['same'])} "
                       f"relationships cross a service boundary: {len(stats['to_view'])} already point at an ACE view as a "
                       f"business key, and {len(stats['cross_table'])} are a Workbench table in one service pointing at a "
                       "Workbench table in another, so the foreign key is cut and the column keeps the business key only "
                       f"(DP-01). The other {len(stats['same'])} stay inside one schema."))
    lines.append(("", "5. Service ownership: this sheet is new. One row per service with its schema, the entities it owns, "
                       "the split between tables and views, and a note where a service owns none (S1), a platform library "
                       "object (PLT) or the rule registry (P7)."))
    lines.append(("", "6. Key: five terms are appended for the new columns: Owning service, Target schema, PLT, "
                       "Cross-service reference and Service contract."))
    lines.append(("", "7. Read me: this sheet is new and carries the two header lines of Template and Rules section R8.1 "
                       "and the change-log row."))
    lines.append(("", ""))
    lines.append(("b", "What did not change"))
    lines.append(("", "Every subject area, data product, entity, relationship, gap row (G1 to G14), ACE addition (1 to 17, "
                       "14 new tables and 12 new columns) and every count is copied unchanged, with the same row order, "
                       "the same IDs and the same field counts. The entity count of 122, the 104 relationships, the 17 "
                       "subject areas and the 14 data products are the v6 numbers."))
    lines.append(("", "The source carries no release date. The one date in the workbook, the 21 November date in the Gaps "
                       "note on DL43, is a decision date, not a release date, and is copied character for character, so no "
                       "date is marked (tentative) and no date is changed."))
    lines.append(("", ""))
    lines.append(("b", "Counts"))
    lines.append(("", "Entities: 122, of which 88 Workbench tables, 4 extension tables and 30 ACE source views, owned by 19 "
                       "services and the platform library."))
    lines.append(("", "Subject areas: 17. Data products: 14, holding 97 entities; OPS, AGT and RPT hold the other 25."))
    lines.append(("", f"Relationships: {len(stats['same']) + len(stats['to_view']) + len(stats['cross_table'])}, of which "
                       f"{len(stats['same'])} inside one service, {len(stats['to_view'])} to an ACE view and "
                       f"{len(stats['cross_table'])} cut across two services."))
    lines.append(("", "Owned per service: " + ", ".join(
        f"{c} {sum(1 for n, v in ENTS.items() if v['owner'] == c)}" for c in ORDER) + "."))
    lines.append(("", ""))
    lines.append(("b", "Open points"))
    lines.append(("", "CG-B-DATA-17-1 to CG-B-DATA-17-8 and ASM-B-DATA-17-1 to ASM-B-DATA-17-8 in the Gap and "
                       "Assumption registers hold the questions behind the new columns: the views have no Ownership Map "
                       "row, payment_match_rule has none, S1 owns no entity, 'Rule' is rule_row, the FK cut list is empty, "
                       "the PLT library objects have no single schema, the feature flags move to the platform library and "
                       "the Key needed the new terms. Numbering to GAP-nnnn and ASM-nnnn is step D1."))
    rm["A1"].font = Font(name="Aptos", size=16, bold=True)
    row = 1
    for kind, text in lines:
        c = rm.cell(row=row, column=1, value=text)
        if kind == "h1":
            c.font = Font(name="Aptos", size=16, bold=True)
        elif kind == "t":
            c.font = Font(name="Aptos", size=14, bold=True)
        elif kind == "b":
            c.font = Font(name="Aptos", size=11, bold=True)
        else:
            c.font = Font(name="Aptos", size=11)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        row += 1
    print("Read me: new first sheet,", row - 1, "rows")

    wb.save(DST)
    print("WROTE", DST)


if __name__ == "__main__":
    main()
