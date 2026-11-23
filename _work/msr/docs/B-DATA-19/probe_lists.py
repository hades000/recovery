"""Probe: parse the v4 Lists sheet, resolve owners and consumers from the Ownership Map."""
import json, re
from pathlib import Path

import openpyxl

SRC = "06 Data/Recovery Workbench Reference Data and Lists of Values v4.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"

wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["Lists"]
rows = []
for r in ws.iter_rows(min_row=5, values_only=True):
    if not r or not r[0]:
        continue
    rows.append([str(c).strip() if c is not None else "" for c in r[:6]])

owb = openpyxl.load_workbook(OWN, data_only=True)
table_owner, table_schema = {}, {}
for row in owb["Tables"].iter_rows(min_row=2, values_only=True):
    if row and row[0]:
        table_owner[str(row[0])] = str(row[1])
        table_schema[str(row[0])] = str(row[2])
svc = {}
for row in owb["Services"].iter_rows(min_row=2, values_only=True):
    if row and row[0]:
        svc[str(row[0])] = str(row[1])
svc["PLT"] = "platform library"

print("list rows", len(rows))
kinds = {}
for r in rows:
    kinds[r[1]] = kinds.get(r[1], 0) + 1
print(kinds)

unresolved = {}
owner_sets = {}
for r in rows:
    code, kind, vals, owner, used, source = r
    refs = [x.strip() for x in used.split(",") if x.strip()]
    tables, views, nofield = set(), set(), 0
    for ref in refs:
        if ref.startswith("No live field") or ref.startswith("ACE batch") or ref.startswith("ACE ingestion") or ref.startswith("Cutover plan") or ref.startswith("Outbound interfaces"):
            nofield += 1
            continue
        m = re.match(r"^([a-zA-Z0-9_]+)\.[a-zA-Z0-9_]+$", ref)
        if m:
            t = m.group(1)
            if t.startswith("v_ace"):
                views.add(t)
            elif t in table_owner:
                tables.add(t)
            else:
                unresolved.setdefault(code, []).append(ref)
        else:
            unresolved.setdefault(code, []).append(ref)
    owners = sorted({table_owner[t] for t in tables} | ({"P1"} if views else set()))
    owner_sets[code] = (owners, sorted(tables), sorted(views), nofield, kind)

print("unresolved:", json.dumps(unresolved, ensure_ascii=False, indent=1)[:3000])
multi = {k: v[0] for k, v in owner_sets.items() if len(v[0]) > 1}
print("multi-owner lists:", len(multi))
for k, v in sorted(multi.items()):
    print("  ", k, v)
nolen = {k: v for k, v in owner_sets.items() if not v[0]}
print("no-owner lists:", len(nolen))
for k, v in sorted(nolen.items()):
    print("  ", k, v[4], v[3])
json.dump({k: {"owners": v[0], "tables": v[1], "views": v[2], "nofield": v[3], "kind": v[4]} for k, v in owner_sets.items()},
          open("_work/msr/docs/B-DATA-19/owner_sets.json", "w", encoding="utf-8"), indent=1)
