"""Verify the generated API v5 set against API Specification v4 (read only)."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "05 Technical architecture" / "Recovery Workbench API Specification v4.yaml"
OUT = ROOT / "05 Technical architecture" / "Recovery Workbench API Specification v5"
doc = yaml.safe_load(SRC.read_text(encoding="utf-8"))

ops_src = {}
for p, item in doc["paths"].items():
    for m, op in item.items():
        if m in ("get", "post", "put", "patch", "delete"):
            ops_src[f"{m.upper()} {p}"] = op

files = sorted(OUT.glob("*.yaml"))
print("files:", [f.name for f in files])
seen = {}
problems = []
schemas = {}
responses = {}
for f in files:
    if f.name == "index.yaml":
        continue
    t = f.read_text(encoding="utf-8")
    lines = t.split("\n")
    if lines[0] != "# SCB Collections and Recovery. Henka Group, 22 November 2026." or \
       lines[1] != "# (C) Siam Commercial Bank and Henka Pte Ltd":
        problems.append(f"{f.name}: header lines")
    if "5.0.0, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" not in t:
        problems.append(f"{f.name}: change-log row")
    d = yaml.safe_load(t)
    if d.get("openapi") != "3.1.0":
        problems.append(f"{f.name}: openapi version")
    for p, item in (d.get("paths") or {}).items():
        for m, op in item.items():
            k = f"{m.upper()} {p}"
            if k in seen:
                problems.append(f"duplicate operation {k} in {f.name} and {seen[k]}")
            seen[k] = f.name
            src = ops_src.get(k)
            if src is None:
                problems.append(f"{f.name}: {k} not in source")
                continue
            cmp = dict(op)
            owner = cmp.pop("x-owner", None)
            note = cmp.pop("x-owner-note", None)
            if owner is None:
                problems.append(f"{f.name}: {k} has no x-owner")
            if cmp != src:
                diff = [kk for kk in set(cmp) | set(src) if cmp.get(kk) != src.get(kk)]
                problems.append(f"{f.name}: {k} content differs: {diff}")
    for name, sch in (d.get("components", {}).get("schemas") or {}).items():
        if name in schemas and schemas[name] != sch:
            problems.append(f"schema {name} differs between files ({f.name} and earlier)")
        schemas[name] = sch
    for name, r in (d.get("components", {}).get("responses") or {}).items():
        if name in responses and responses[name] != r:
            problems.append(f"response {name} differs")
        responses[name] = r

missing = set(ops_src) - set(seen)
extra = set(seen) - set(ops_src)
print("ops in source:", len(ops_src), "in v5:", len(seen), "missing:", sorted(missing), "extra:", sorted(extra))
print("schemas:", len(schemas), "of", len(doc["components"]["schemas"]))
print("responses:", len(responses), "of", len(doc["components"]["responses"]))
for name, sch in doc["components"]["schemas"].items():
    if name not in schemas:
        problems.append(f"source schema {name} absent")
    elif schemas[name] != sch:
        problems.append(f"schema {name} content differs from v4")
for name, r in doc["components"]["responses"].items():
    if responses.get(name) != r:
        problems.append(f"response {name} content differs from v4")
print("security:", {f.name: yaml.safe_load(f.read_text(encoding='utf-8')).get("security") for f in files if f.name != "index.yaml"} and "checked")

# asyncapi
asyncs = sorted((OUT / "asyncapi").glob("*.yaml"))
print("asyncapi docs:", len(asyncs))
for a in asyncs:
    t = a.read_text(encoding="utf-8")
    lines = t.split("\n")
    if lines[0] != "# SCB Collections and Recovery. Henka Group, 22 November 2026." or \
       lines[1] != "# (C) Siam Commercial Bank and Henka Pte Ltd":
        problems.append(f"{a.name}: header lines")
    if "5.0.0, 22 November 2026, D-RCV-60" not in t:
        problems.append(f"{a.name}: change-log row")
    d = yaml.safe_load(t)
    if d.get("asyncapi") != "3.0.0":
        problems.append(f"{a.name}: asyncapi version")
    # channel refs resolve
    chans = d.get("channels") or {}
    for opid, op in (d.get("operations") or {}).items():
        ref = op["channel"]["$ref"].split("/channels/")[1]
        if ref not in chans:
            problems.append(f"{a.name}: {opid} channel ref {ref} unresolved")
        for msg in op.get("messages", []):
            r = msg["$ref"]
            ch, _, name = r.split("/channels/")[1].partition("/messages/")
            if ch not in chans or name not in (chans[ch].get("messages") or {}):
                problems.append(f"{a.name}: {opid} message ref {r} unresolved")
            if name not in (d["components"]["messages"]):
                problems.append(f"{a.name}: message {name} has no component")
    for name, msg in (d.get("components", {}).get("messages") or {}).items():
        pref = msg["payload"]["$ref"].split("/schemas/")[1]
        if pref not in (d["components"]["schemas"] or {}):
            problems.append(f"{a.name}: payload schema {pref} missing")
        href = msg["headers"]["$ref"].split("/schemas/")[1]
        if href not in (d["components"]["schemas"] or {}):
            problems.append(f"{a.name}: header schema missing")

idx = yaml.safe_load((OUT / "index.yaml").read_text(encoding="utf-8"))
print("index keys:", list(idx))
print("index docs:", len(idx["x-document-set"]))
if idx["x-totals"]["operations"] != len(ops_src):
    problems.append("index totals operations mismatch")
if not (OUT / "index.yaml").read_text(encoding="utf-8").startswith(
        "# SCB Collections and Recovery. Henka Group, 22 November 2026.\n# (C) Siam Commercial Bank and Henka Pte Ltd"):
    problems.append("index header")

print("\nPROBLEMS:", len(problems))
for p in problems[:60]:
    print(" -", p)
