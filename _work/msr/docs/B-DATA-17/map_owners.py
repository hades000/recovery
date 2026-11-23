"""Build the entity -> owning service map for the Conceptual Data Model v7.

Sources (read only): Ownership Map v1 xlsx (Services, Tables sheets), plan/ownership.json,
LDM v8 extract (to resolve the three entity names that are not a mechanical table name),
Decision Log v10 (D-RCV-36 T10 for payment_match_rule), Architecture v5 extract (views).
"""
import json, re
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

# --- services from the Ownership Map -----------------------------------------
wb = openpyxl.load_workbook(ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx")
ws = wb["Services"]
services = {}
for r in ws.iter_rows(min_row=2, values_only=True):
    if not r or not r[0]:
        continue
    services[r[0]] = {"service": r[1], "name": r[2], "wave": str(r[3]), "schema": r[4]}

# --- tables from the Ownership Map -------------------------------------------
ws = wb["Tables"]
tables = {}
for r in ws.iter_rows(min_row=2, values_only=True):
    if not r or not r[0]:
        continue
    tables[r[0]] = {"owner": r[1], "schema": r[2], "basis": r[3], "ruling": r[4], "asm": r[5]}

# --- entity name -> table name, where the name is not the table name ----------
EXPLICIT = {
    "Rule": "rule_row",                        # LDM v8: rule_row "Rule", 18 fields
    "List value": "lov_value",
    "Party extension": "party_ext",
    "Contact point extension": "contact_point_ext",
    "Account extension": "account_ext",
    "Valuation extension": "valuation_ext",
}

# --- entity -> owning service -------------------------------------------------
VIEW_BASIS = ("Architecture v5 Text Extract v1 slides 15 and 41: the 30 recovery.v_ace_* views are read only by "
              "rwb-source-data (ADR-010, DP-05); rwb-source-data owns the ACE view contract, so the view is not "
              "owned by the domain service that consumes its data")
NO_MAP_BASIS = ("Decision Log v10 D-RCV-36 T10 drops payment_match_rule and makes payment matching the PAYMENT_MATCH "
                "rule package in rwb-decision; the Ownership Map has no row for the table because it has no target table")


def snake(n):
    return re.sub(r"[^a-z0-9]+", "_", str(n).lower()).strip("_")


def build(entities):
    """entities: list of entity names from the Entities sheet, in sheet order."""
    out = {}
    for e in entities:
        if str(e).startswith("v_ace_"):
            out[e] = {"table": str(e), "owner": "P1", "schema": "recovery (ACE, read-only view)",
                      "basis": VIEW_BASIS, "kind": "ACE read-only view", "map_row": False}
            continue
        t = EXPLICIT.get(e, snake(e))
        if t == "payment_match_rule":
            out[e] = {"table": t, "owner": "P7", "schema": services["P7"]["schema"],
                      "basis": NO_MAP_BASIS, "kind": "Workbench table (retired by D-RCV-36 T10)",
                      "map_row": False}
            continue
        if t not in tables:
            out[e] = {"table": t, "owner": "", "schema": "", "basis": "", "kind": "?", "map_row": False}
            continue
        m = tables[t]
        basis = f"Ownership Map v1, table row {t}: {m['basis']}"
        if m["ruling"]:
            basis += f"; ruling: {m['ruling']}"
        out[e] = {"table": t, "owner": m["owner"], "schema": m["schema"], "basis": basis,
                  "kind": "Workbench table" if not t.endswith("_ext") else "Workbench extension table",
                  "map_row": True}
    return out


if __name__ == "__main__":
    wb = openpyxl.load_workbook(ROOT / "06 Data" / "Recovery Workbench Conceptual Data Model v6.xlsx")
    ws = wb["Entities"]
    ents = [ws.cell(row=r, column=1).value for r in range(5, 127)]
    m = build(ents)
    bad = {k: v for k, v in m.items() if not v["owner"]}
    print("entities", len(m), "unowned", bad)
    from collections import Counter
    c = Counter(v["owner"] for v in m.values())
    print("owner counts", dict(sorted(c.items())))
    print("no map row:", [k for k, v in m.items() if not v["map_row"]])
    print("map rows unused:", sorted(set(tables) - {v["table"] for v in m.values() if v["map_row"]}))
    (OUT / "owners.json").write_text(json.dumps({"services": services, "entities": m}, indent=1), encoding="utf-8")
