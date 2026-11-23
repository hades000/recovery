"""B-ARCH-DB: split Physical Schema v6 into the 19 rwb_<schema>.sql files, recovery_views.sql and README.

Reads (read only): 06 Data/Recovery Workbench Physical Schema v6.sql,
_work/msr/plan/ownership.json, 22 Microservice Realignment/...Ownership Map v1.xlsx
Writes: 06 Data/Recovery Workbench Physical Schema v7/*
Never edits the source.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "06 Data" / "Recovery Workbench Physical Schema v6.sql"
OUT = ROOT / "06 Data" / "Recovery Workbench Physical Schema v7"
OWN = ROOT / "_work" / "msr" / "plan" / "ownership.json"
WP = "B-ARCH-DB"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
HDR1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
HDR2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
CHG = f"7, 22 November 2026, {DEC} microservice realignment, {TOOL}"

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
CODE_TO_SCHEMA = {c: s for c, _, _, _, s in SERVICES}
CODE_TO_SVC = {c: (svc, name, wave) for c, svc, name, wave, _ in SERVICES}

# Platform library objects created in every service schema (DP-09, RWB-PLT-TE006-CON).
LIBRARY = ["outbox_event", "outbox_delivery", "processed_event", "idempotency_key"]
# Platform library objects hosted once, in rwb_integration, for the feature-flag admin API.
HOSTED = {"feature_flag": "P2", "feature_flag_change": "P2"}

# Notes emitted next to a table whose status needs a word beyond the source.
NOTES = {
    "lake_copy_watermark": [
        "-- Retirement note: lake_copy_watermark has no target. The data lake is removed (Architecture v5 slide 37; DP-17)",
        "-- and JOB-13 is continuous Kafka ingest in rwb-decision (Architecture v5 slide 44), so the P1 DB story drops this",
        "-- table (Ownership Map ruling ASM-A6-tables-13). The DDL is kept here so no source object is lost; see CG-B-ARCH-DB-8.",
    ],
    "feature_flag": [
        "-- Hosting note: feature_flag and feature_flag_change are platform library objects owned by PLT in the Ownership Map.",
        "-- They are emitted once, in rwb_integration, because rwb-integration serves the feature-flag admin API",
        "-- (Ownership Map ruling ASM-A6-api-2; CG-B-ARCH-DB-3, ASM-B-ARCH-DB-3).",
    ],
}


def load_owner():
    d = json.load(open(OWN, encoding="utf-8"))
    return {k: v for k, v in d["tables"].items()}, d


def split_statements(text):
    """Return a list of statement dicts: {lead:[lines], body:[lines], text:str}."""
    lines = text.splitlines()
    out, buf, dollar = [], [], False
    for line in lines:
        buf.append(line)
        if line.count("$$") % 2 == 1:
            dollar = not dollar
        if not dollar and line.rstrip().endswith(";"):
            st = strip_stmt(buf)
            if st:
                out.append(st)
            buf = []
    if buf:
        st = strip_stmt(buf)
        if st:
            out.append(st)
    return out


def strip_stmt(buf):
    lead = []
    i = 0
    while i < len(buf) and (not buf[i].strip() or buf[i].lstrip().startswith("--")):
        lead.append(buf[i])
        i += 1
    body = buf[i:]
    while body and not body[-1].strip():
        body.pop()
    if not body:
        return None
    return {"lead": lead, "body": body, "text": "\n".join(body)}


def classify(st):
    first = ""
    for l in st["body"]:
        if l.strip() and not l.lstrip().startswith("--"):
            first = l.strip()
            break
    m = re.match(r"CREATE TABLE (?:IF NOT EXISTS )?(\w+)", first)
    if m:
        return "table", m.group(1)
    m = re.match(r"CREATE (?:OR REPLACE )?VIEW ([\w\.\"]+)", first)
    if m:
        return "view", m.group(1).replace("recovery.", "")
    m = re.match(r"CREATE (?:OR REPLACE )?FUNCTION ([\w\.]+)", first)
    if m:
        return "function", m.group(1)
    m = re.match(r"CREATE TRIGGER (\w+) .* ON (\w+)", first)
    if m:
        return "trigger", m.group(2)
    m = re.match(r"COMMENT ON TABLE (\w+)", first)
    if m:
        return "comment_table", m.group(1)
    m = re.match(r"COMMENT ON COLUMN (\w+)\.(\w+)", first)
    if m:
        return "comment_column", m.group(1)
    m = re.match(r"COMMENT ON VIEW ([\w\.]+)", first)
    if m:
        return "comment_view", m.group(1).replace("recovery.", "")
    m = re.match(r"COMMENT ON FUNCTION ([\w\.]+)", first)
    if m:
        return "comment_function", m.group(1)
    m = re.match(r"CREATE (?:UNIQUE )?INDEX \w+ ON (\w+)", first)
    if m:
        return "index", m.group(1)
    m = re.match(r"ALTER TABLE (\w+) ADD CONSTRAINT \w+ FOREIGN KEY \((\w+)\) REFERENCES (\w+) \((\w+)\)", first)
    if m:
        return "fk", m.group(1)
    m = re.match(r"INSERT INTO (\w+)", first)
    if m:
        return "insert", m.group(1)
    if first.startswith("CREATE SCHEMA"):
        return "schema", None
    if first.startswith("SET "):
        return "set", None
    if first.startswith("CREATE EXTENSION"):
        return "extension", None
    return "other", None


def head_comment(st):
    """The description line(s) before CREATE TABLE, if any."""
    return [l for l in st["lead"] if l.strip().startswith("--")]


def target_label(owner):
    return CODE_TO_SCHEMA.get(owner, "platform-library")


def annotate(body, table, cut):
    """Append a cross-owner reference note to each cut column line."""
    cuts = [r for r in cut if r[0] == table]
    if not cuts:
        return body
    blines = body.splitlines()
    for i, bl in enumerate(blines):
        mm = re.match(r"^(\s*)([a-z][a-z0-9_]*)\s", bl)
        if not mm:
            continue
        col = mm.group(2)
        for r in cuts:
            if r[3] == col:
                blines[i] = bl + f"  -- cross-service reference: {target_label(r[5])}.{r[4]}({r[6]}); integrity through the owner's contract"
                break
    return "\n".join(blines)


def main():
    text = SRC.read_text(encoding="utf-8")
    tables, om = load_owner()
    stmts = split_statements(text)
    kinds = {}
    for st in stmts:
        st["kind"], st["obj"] = classify(st)
        kinds.setdefault(st["kind"], []).append(st["obj"])

    print("statements", len(stmts))
    print({k: len(v) for k, v in sorted(kinds.items())})

    owner_of = {t: v["owner"] for t, v in tables.items()}
    table_order = [s["obj"] for s in stmts if s["kind"] == "table"]
    assert len(table_order) == 93, len(table_order)

    # FK classification
    fks = [s for s in stmts if s["kind"] == "fk"]
    rx = re.compile(r"ALTER TABLE (\w+) ADD CONSTRAINT (\w+) FOREIGN KEY \((\w+)\) REFERENCES (\w+) \((\w+)\)(.*);")
    kept, cut = [], []
    for s in fks:
        m = rx.match(s["text"].strip())
        src, cn, col, tgt, tcol, rest = m.groups()
        a, b = owner_of[src], owner_of[tgt]
        rec = (src, a, cn, col, tgt, b, tcol, rest)
        (kept if a == b else cut).append(rec)
    print("fk kept", len(kept), "cut", len(cut))

    # Group by service
    by_service = {c: {"tables": [], "fks": [], "indexes": [], "ctable": [], "ccol": [], "inserts": []} for c, *_ in SERVICES}
    hosted_to = {}
    for t in table_order:
        o = owner_of[t]
        if t in LIBRARY:
            continue
        if t in HOSTED:
            hosted_to[t] = HOSTED[t]
            by_service[HOSTED[t]]["tables"].append(t)
        else:
            by_service[o]["tables"].append(t)
    for c in by_service:
        by_service[c]["tables"] = sorted(by_service[c]["tables"], key=table_order.index)
        # library tables appended in a stable order after the owned tables
        if c != "S1" or True:
            by_service[c]["library"] = list(LIBRARY)

    for s in stmts:
        if s["kind"] == "fk":
            continue
        if s["kind"] in ("index", "comment_table", "comment_column", "insert"):
            t = s["obj"]
            o = owner_of.get(t)
            if o is None:
                raise SystemExit(f"unknown table in {s['kind']}: {t}")
            target = HOSTED.get(t, o)
            if t in LIBRARY:
                for c in by_service:
                    by_service[c][{"index": "indexes", "comment_table": "ctable",
                                   "comment_column": "ccol", "insert": "inserts"}[s["kind"]]].append(s)
            elif target:
                by_service[target][{"index": "indexes", "comment_table": "ctable",
                                    "comment_column": "ccol", "insert": "inserts"}[s["kind"]]].append(s)

    # kept FKs by service (source table owner). A PLT-owned pair exists in every
    # service schema, so its key is emitted in every file.
    for rec in kept:
        src, a = rec[0], rec[1]
        if a == "PLT":
            for c in by_service:
                by_service[c]["fks"].append(rec)
        else:
            by_service[a]["fks"].append(rec)

    # Append-only trigger guard: refuse_change() plus one trigger per table.
    triggers = [s for s in stmts if s["kind"] == "trigger"]
    refuse = next(s for s in stmts if s["kind"] == "function" and s["obj"] == "refuse_change")
    by_service["P7"]["triggers"] = []
    by_service["P1"]["triggers"] = []
    for c in by_service:
        by_service[c].setdefault("triggers", [])
    for s in triggers:
        by_service[owner_of[s["obj"]]]["triggers"].append(s)

    # write the 19 files
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    cut_report = []
    for code, svc, name, wave, schema in SERVICES:
        data = by_service[code]
        path = OUT / f"{schema}.sql"
        L = []
        L.append(f"-- {HDR1}")
        L.append(f"-- {HDR2}")
        L.append(f"-- Recovery Workbench physical schema, PostgreSQL. Service {svc} ({code}, {name}), wave {wave}. Version 7.")
        L.append(f"-- Change log: {CHG}.")
        L.append(f"-- Schema {schema}; login {schema}; REST base /api/recovery/{svc[4:]}/v1; topic rwb.{svc[4:]}.events.v1; queue {svc}.")
        L.append("-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.")
        own_count = len(data["tables"])
        true_owned = sum(1 for t in data["tables"] if owner_of.get(t) == code)
        L.append(f"-- Tables in this file: {own_count}. Owned by this service in the Ownership Map v1: {true_owned}. Platform library objects created here as well: {len(LIBRARY)}.")
        L.append("-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).")
        L.append("-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).")
        L.append("")
        L.append(f"CREATE SCHEMA IF NOT EXISTS {schema};")
        L.append(f"SET search_path TO {schema};")
        L.append("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        L.append("")
        # library block
        if LIBRARY:
            L.append("-- ---------------------------------------------------------------------------")
            L.append("-- Platform library objects (owner PLT in the Ownership Map; DP-09, RWB-PLT-TE006-CON).")
            L.append("-- Created in every service schema. No foreign key to a business table.")
            L.append("-- ---------------------------------------------------------------------------")
            L.append("")
            for t in LIBRARY:
                st = next(s for s in stmts if s["kind"] == "table" and s["obj"] == t)
                for l in head_comment(st):
                    L.append(l)
                L.append(annotate(st["text"], t, cut))
                L.append("")
        # owned tables
        for t in data["tables"]:
            st = next(s for s in stmts if s["kind"] == "table" and s["obj"] == t)
            for l in head_comment(st):
                L.append(l)
            L.append(annotate(st["text"], t, cut))
            L.append("")
            if t in NOTES:
                L.extend(NOTES[t])
                L.append("")
        if code == "S1":
            L.append("-- This service owns no table in the Ownership Map v1. valuation_ext stays in rwb_source_data")
            L.append("-- (ruling ASM-A6-tables-15) and route economics come from ACE through the rwb-source-data contract (DP-05).")
            L.append("-- The local tables that a later TSD may add are Not specified in the source documents (CG-B-ARCH-DB-2; ASM-B-ARCH-DB-2).")
            L.append("")
        # kept FKs
        if data["fks"]:
            L.append("-- ---------------------------------------------------------------------------")
            L.append("-- Foreign keys kept inside this service (same owner).")
            L.append("-- ---------------------------------------------------------------------------")
            L.append("")
            for r in data["fks"]:
                L.append(f"ALTER TABLE {r[0]} ADD CONSTRAINT {r[2]} FOREIGN KEY ({r[3]}) REFERENCES {r[4]} ({r[6]}){r[7]};")
            L.append("")
        # append-only trigger guard
        if data.get("triggers"):
            L.append("-- ---------------------------------------------------------------------------")
            L.append("-- Append-only guard (trigger) from the source")
            L.append("-- ---------------------------------------------------------------------------")
            L.append("")
            L.append(refuse["text"])
            L.append("")
            for s in data["triggers"]:
                L.append(s["text"])
            L.append("")
        # indexes
        if data["indexes"] or True:
            idx = [s for s in data["indexes"]]
            if idx:
                L.append("-- ---------------------------------------------------------------------------")
                L.append("-- Indexes")
                L.append("-- ---------------------------------------------------------------------------")
                L.append("")
                for s in idx:
                    for l in head_comment(s):
                        L.append(l)
                    L.append(s["text"])
                L.append("")
        # comments
        if data["ctable"] or data["ccol"]:
            L.append("-- ---------------------------------------------------------------------------")
            L.append("-- Data dictionary comments")
            L.append("-- ---------------------------------------------------------------------------")
            L.append("")
            for s in data["ctable"]:
                L.append(s["text"])
            for s in data["ccol"]:
                L.append(s["text"])
            L.append("")
        # seeds
        if data["inserts"]:
            L.append("-- ---------------------------------------------------------------------------")
            L.append("-- Seed and dictionary rows")
            L.append("-- ---------------------------------------------------------------------------")
            L.append("")
            for s in data["inserts"]:
                for l in head_comment(s):
                    L.append(l)
                L.append(s["text"])
            L.append("")
        # cut note
        cuts_here = [r for r in cut if r[0] in set(data["tables"]) | set(LIBRARY)]
        if cuts_here:
            L.append("-- ---------------------------------------------------------------------------")
            L.append("-- Cross-service references cut from this file (no database foreign key)")
            L.append("-- ---------------------------------------------------------------------------")
            for r in cuts_here:
                L.append(f"-- {r[0]}.{r[3]} -> {target_label(r[5])}.{r[4]}.{r[6]} (owner {r[5]}); the column stays uuid and integrity is through the owner's contract.")
            L.append("")
        path.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
        written.append(path)
        print("WROTE", path.name, len(L), "lines")

    # report
    rep = {
        "tables": len(table_order), "fk_total": len(fks), "fk_kept": len(kept), "fk_cut": len(cut),
        "per_service": {c: len(by_service[c]["tables"]) + len(LIBRARY) for c, *_ in SERVICES},
        "cuts": [{"from": r[0], "from_owner": r[1], "constraint": r[2], "column": r[3],
                  "to": r[4], "to_owner": r[5], "to_column": r[6]} for r in cut],
        "views": [s["obj"] for s in stmts if s["kind"] == "view"],
        "no_table_comment": sorted(set(table_order) - {s["obj"] for s in stmts if s["kind"] == "comment_table"}),
    }
    (Path(__file__).parent / "schema_report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
    print(json.dumps({k: rep[k] for k in ("tables", "fk_total", "fk_kept", "fk_cut", "per_service", "no_table_comment")}, indent=1))


if __name__ == "__main__":
    main()
