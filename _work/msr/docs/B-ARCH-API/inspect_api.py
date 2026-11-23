"""Inspect the API Specification v4 YAML structure (read only)."""
import json, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "05 Technical architecture" / "Recovery Workbench API Specification v4.yaml"

doc = yaml.safe_load(SRC.read_text(encoding="utf-8"))

print("TOP KEYS:", list(doc.keys()))
print("INFO:", json.dumps({k: v for k, v in doc["info"].items() if k != "description"}, indent=1))
print("SERVERS:", doc.get("servers"))
print("SECURITY:", doc.get("security"))
print("TAGS:", [t.get("name") for t in doc.get("tags", [])])
print("NUM PATHS:", len(doc["paths"]))
ops = []
for p, item in doc["paths"].items():
    for m, op in item.items():
        if m in ("get", "post", "put", "patch", "delete", "head", "options", "trace"):
            ops.append((m.upper(), p, op.get("operationId"), op.get("x-module"), op.get("tags"), list(op.keys())))
print("NUM OPS:", len(ops))
mods = {}
for m, p, oid, mod, tags, keys in ops:
    mods.setdefault(mod, []).append(f"{m} {p}")
for mod in sorted(mods):
    print(f"  module {mod}: {len(mods[mod])}")
print("PATH-LEVEL KEYS sample:", {p: list(i.keys()) for p, i in list(doc["paths"].items())[:2]})
comp = doc.get("components", {})
print("COMPONENT SECTIONS:", {k: len(v) if isinstance(v, dict) else v for k, v in comp.items()})
for k in comp:
    if isinstance(comp[k], dict) and k not in ("schemas",):
        print(f"  {k}: {sorted(comp[k].keys())}")
print("SCHEMAS:", len(comp.get("schemas", {})))
print("SCHEMA NAMES:", sorted(comp.get("schemas", {}).keys()))
extra = {k: v for k, v in doc.items() if k not in ("openapi", "info", "servers", "security", "tags", "paths", "components")}
print("OTHER TOP KEYS:", json.dumps(extra, indent=1)[:3000])
json.dump({"ops": ops}, (Path(__file__).parent / "ops.json").open("w", encoding="utf-8"), indent=1)
