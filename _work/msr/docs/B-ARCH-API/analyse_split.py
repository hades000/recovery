"""Analyse refs, orphans and per-service assignment for the API v5 split (read only)."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "05 Technical architecture" / "Recovery Workbench API Specification v4.yaml"
doc = yaml.safe_load(SRC.read_text(encoding="utf-8"))
own = json.loads((ROOT / "_work/msr/plan/ownership_part_api.json").read_text(encoding="utf-8"))
owners = {e["id"]: e["owner"] for e in own["api"]}

def refs(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                out.add(v)
            else:
                refs(v, out)
    elif isinstance(node, list):
        for v in node:
            refs(v, out)

ops = []
for p, item in doc["paths"].items():
    for m, op in item.items():
        if m in ("get", "post", "put", "patch", "delete"):
            ops.append((m.upper(), p, op))

# path level keys other than methods
print("path-level non-method keys:", {p: [k for k in i if k not in ('get','post','put','patch','delete')] for p, i in doc["paths"].items() if [k for k in i if k not in ('get','post','put','patch','delete')]})

# op keys used
keys = set()
for m, p, op in ops:
    keys |= set(op.keys())
print("operation keys:", sorted(keys))

# refs from ops
oprefs = set()
for m, p, op in ops:
    refs(op, oprefs)
print("refs from operations:", len(oprefs))

def resolve(r):
    prefix = "#/components/"
    assert r.startswith(prefix), r
    parts = r[len(prefix):].split("/")
    return parts[0], parts[1]

comp = doc["components"]
closure = set(oprefs)
frontier = set(oprefs)
while frontier:
    nxt = set()
    for r in frontier:
        sec, name = resolve(r)
        nxt_r = set()
        refs(comp[sec][name], nxt_r)
        for x in nxt_r:
            if x not in closure:
                closure.add(x)
                nxt.add(x)
    frontier = nxt
print("closure:", len(closure))
bysec = {}
for r in closure:
    s, n = resolve(r)
    bysec.setdefault(s, set()).add(n)
print({k: len(v) for k, v in bysec.items()})
orphans = {s: sorted(set(comp[s]) - bysec.get(s, set())) for s in comp}
print("orphans per section:", {k: len(v) for k, v in orphans.items()})
for k, v in orphans.items():
    if v:
        print(" ", k, v[:20])
# Does Problem come from responses?
print("\nentries in components.responses:")
for k, v in comp["responses"].items():
    print(" ", k, v.get("description", "")[:80], list(v.get("content", {}).keys()))

# assignment
svc = {}
wbrows = {}
import openpyxl
wb = openpyxl.load_workbook(ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx", data_only=True)
ws = wb["Services"]
services = []
for r in ws.iter_rows(min_row=2, values_only=True):
    if r[0]:
        services.append({"code": r[0], "service": r[1], "name": r[2], "wave": r[3], "schema": r[4], "base": r[5], "topic": r[6], "queue": r[7]})
print("\nservices:", len(services))
for s in services:
    print(" ", s)

for m, p, op in ops:
    ow = owners[f"{m} {p}"]
    svc.setdefault(ow, []).append(f"{m} {p}")
print("\nper owner:")
for k in sorted(svc, key=lambda x: (len(x), x)):
    print(f"  {k}: {len(svc[k])}")
# paths split across owners
bypath = {}
for m, p, op in ops:
    bypath.setdefault(p, []).append(owners[f"{m} {p}"])
print("\npaths with ops in more than one owner:", {p: v for p, v in bypath.items() if len(set(v)) > 1})
print("\nops with same path+method duplicates: n/a")
# tags used per owner
tags = {}
for m, p, op in ops:
    ow = owners[f"{m} {p}"]
    for t in op.get("tags", []):
        tags.setdefault(ow, set()).add(t)
print("\ntags per owner:", {k: sorted(v) for k, v in tags.items()})
