"""Write recovery_views.sql and README.md into the v7 schema folder."""
import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_schema as g

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "06 Data" / "Recovery Workbench Physical Schema v7"
SRC = ROOT / "06 Data" / "Recovery Workbench Physical Schema v6.sql"

HDR1, HDR2, CHG, TOOL = g.HDR1, g.HDR2, g.CHG, g.TOOL


def clean_lead(lead):
    """Keep descriptive comments, drop the repeated section banners."""
    out = []
    for l in lead:
        s = l.strip()
        if not s.startswith("--"):
            continue
        if re.match(r"^--\s*-+$", s):
            continue
        if any(k in s for k in ("ACE source views. Section", "Helper functions. Immutable", "Section A - Tier 1", "Section B - Tier 2")):
            continue
        out.append(l)
    return out


def main():
    stmts = g.split_statements(SRC.read_text(encoding="utf-8"))
    for s in stmts:
        s["kind"], s["obj"] = g.classify(s)
    views = [s for s in stmts if s["kind"] == "view"]
    vcomments = {s["obj"]: s for s in stmts if s["kind"] == "comment_view"}
    funcs = [s for s in stmts if s["kind"] == "function" and s["obj"].startswith("recovery.")]
    cfuncs = [s for s in stmts if s["kind"] == "comment_function"]
    others = [s for s in stmts if s["kind"] == "other"]

    vdd = next(s for s in views if s["obj"] == "v_data_dictionary")
    ace = [s for s in views if s["obj"].startswith("v_ace_")]

    L = []
    L.append(f"-- {HDR1}")
    L.append(f"-- {HDR2}")
    L.append("-- Recovery Workbench views, PostgreSQL. Version 7.")
    L.append(f"-- Change log: {CHG}.")
    L.append("-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only), the v_data_dictionary view, the 30 ACE source views, the helper functions, the grants block and the conformance test. The view text is copied unchanged; only the schema of the data dictionary view changes.")
    L.append("-- 31 views: rwb_source_data.v_data_dictionary (the data dictionary held as data) and 30 read-only recovery.v_ace_* views over the ACE database.")
    L.append("-- No table is created here. The 19 rwb_<schema>.sql files hold every table.")
    L.append("-- Run order: after rwb_source_data.sql, because v_data_dictionary reads rwb_source_data.sys_fields, sys_objects and data_product.")
    L.append("-- The recovery schema keeps the 30 ACE views only; it holds no table after the realignment (Architecture v5 slide 29: recovery.v_ace_* is SELECT-only for rwb-source-data).")
    L.append("")
    L.append("CREATE SCHEMA IF NOT EXISTS recovery;")
    L.append("CREATE SCHEMA IF NOT EXISTS rwb_source_data;")
    L.append("")
    L.append("-- ---------------------------------------------------------------------------")
    L.append("-- Helper functions. Immutable, no side effects, safe in a view definition.")
    L.append("-- ---------------------------------------------------------------------------")
    L.append("")
    for s in funcs:
        for l in clean_lead(s["lead"]):
            L.append(l)
        L.append(s["text"])
        L.append("")
    for s in cfuncs:
        L.append(s["text"])
    L.append("")
    L.append("-- ---------------------------------------------------------------------------")
    L.append("-- Data dictionary view (rwb-source-data)")
    L.append("-- ---------------------------------------------------------------------------")
    L.append("")
    body = vdd["text"]
    body = body.replace("CREATE VIEW v_data_dictionary AS", "CREATE VIEW rwb_source_data.v_data_dictionary AS", 1)
    body = body.replace("FROM sys_fields f", "FROM rwb_source_data.sys_fields f")
    body = body.replace("JOIN sys_objects o", "JOIN rwb_source_data.sys_objects o")
    body = body.replace("LEFT JOIN data_product p", "LEFT JOIN rwb_source_data.data_product p")
    L.append(body)
    L.append("")
    vc = vcomments["v_data_dictionary"]["text"].replace("COMMENT ON VIEW v_data_dictionary", "COMMENT ON VIEW rwb_source_data.v_data_dictionary", 1)
    L.append(vc)
    L.append("")
    L.append("SET search_path TO recovery;")
    L.append("")
    L.append("-- ---------------------------------------------------------------------------")
    L.append("-- ACE source views. Section A ships as V0002; Section B ships after RWB-ACE-001.")
    L.append("-- Section A - Tier 1 views over ACE tables that exist today (16 views).")
    L.append("-- Section B - Tier 2 views (14 views).")
    L.append("-- ---------------------------------------------------------------------------")
    L.append("")
    for s in ace:
        for l in clean_lead(s["lead"]):
            L.append(l)
        L.append(s["text"])
        L.append("")
        c = vcomments.get(s["obj"])
        if c:
            L.append(c["text"])
            L.append("")
    L.append("-- ---------------------------------------------------------------------------")
    L.append("-- Grants. The recovery service identity may read the views and nothing else.")
    L.append("-- Replace :recovery_role and :ace_view_owner with the names fixed in the Environment and Deployment Design.")
    L.append("-- Adapted to the 19 logins: each rwb_<schema> login gets SELECT on the 30 recovery.v_ace_* views")
    L.append("-- and no DML on any table; ownership stays with the ACE view owner.")
    L.append("-- ---------------------------------------------------------------------------")
    L.append("")
    raw = SRC.read_text(encoding="utf-8")
    start = raw.find("-- Grants. The recovery service identity may read the views and nothing else.")
    grant = raw[start:]
    # drop the four header lines we replaced just above
    grant_lines = grant.splitlines()
    grant_lines = grant_lines[4:]
    L.append("\n".join(grant_lines).rstrip())
    path = OUT / "recovery_views.sql"
    path.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print("WROTE", path.name, len("\n".join(L).splitlines()), "lines")


if __name__ == "__main__":
    main()
