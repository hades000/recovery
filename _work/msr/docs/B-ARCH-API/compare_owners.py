import json, re
from pathlib import Path
import yaml, openpyxl

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "05 Technical architecture" / "Recovery Workbench API Specification v4.yaml"
doc = yaml.safe_load(SRC.read_text(encoding="utf-8"))

ops = []
for p, item in doc["paths"].items():
    for m, op in item.items():
        if m in ("get", "post", "put", "patch", "delete"):
            ops.append({"m": m.upper(), "p": p, "id": f"{m.upper()} {p}", "x": op.get("x-module"),
                        "oid": op.get("operationId"), "tags": op.get("tags")})

own_api = json.loads((ROOT / "_work/msr/plan/ownership_part_api.json").read_text(encoding="utf-8"))
owners = {e["id"]: e for e in own_api["api"]}
print("ownership api entries:", len(owners))

wb = openpyxl.load_workbook(ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx", data_only=True)
ws = wb["Endpoints"]
xl = {}
for r in ws.iter_rows(min_row=2, values_only=True):
    if r[0]:
        xl[r[0]] = r[1]
print("xlsx endpoints:", len(xl))

missing = [o["id"] for o in ops if o["id"] not in owners]
print("ops missing from ownership_part_api:", len(missing))
for m in missing:
    print("   ", m, "| xlsx owner:", xl.get(m))
extra = [k for k in owners if k not in {o["id"] for o in ops}]
print("ownership entries not in v4 yaml:", len(extra))
for e in extra:
    print("   ", e, "->", owners[e]["owner"])

# mismatches x-module vs owner
print("\nOWNER != x-module:")
for o in ops:
    ow = owners.get(o["id"], {}).get("owner") or xl.get(o["id"])
    if ow and ow != o["x"]:
        print(f"  {o['id']}: x-module {o['x']} owner {ow}")

# duplicate operation ids?
ids = [o["oid"] for o in ops]
print("\ndup operationIds:", [i for i in set(ids) if ids.count(i) > 1])
