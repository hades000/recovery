"""Check every operation in section 12.2 against the Ownership Map, path and owner.

Query strings are dropped and a {placeholders} segment matches the map's own placeholder,
after the data-product code and similar literal parameters are folded back to their template.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
own = json.loads((WORK / "plan" / "ownership.json").read_text(encoding="utf-8"))
api = {k: v["owner"] for k, v in own["api"].items()}
STORIES = ["RWB-ITG-E6028-ITG", "RWB-ITG-E6029-ITG", "RWB-ITG-E6030-ITG", "RWB-ITG-E6031-ITG", "RWB-ITG-E6032-ITG"]


def normalise(rel):
    rel = rel.split("?", 1)[0]
    rel = re.sub(r"/DP\d\d(?=/|$)", "/{productCode}", rel)
    rel = re.sub(r"\{[^}]+\}", "{}", rel)
    return rel


def map_keys():
    out = {}
    for k, owner in api.items():
        out[normalise(k)] = owner
    return out


MAP = map_keys()
fails = []
for sid in STORIES:
    frag = json.loads((WORK / "fragments" / f"{sid}.json").read_text(encoding="utf-8"))
    t = (ROOT / frag["file"]).read_text(encoding="utf-8")
    block = re.search(r"#### 12\.2 REST operations consumed(.*?)#### 12\.3", t, re.S).group(1)
    rows = re.findall(r"^\| (GET|POST|PATCH|PUT|DELETE) \| `([^`]+)` \| ([A-Z0-9]+) [^|]+ \|", block, re.M)
    print(sid, len(rows), "rows")
    for method, path, owner in rows:
        m = re.match(r"^/api/recovery/([a-z-]+)/v1(/.*)?$", path)
        if not m:
            fails.append(f"{sid}: path not on a service base: {path}")
            continue
        rel = m.group(2) or "/"
        if (method, normalise(rel)) not in {(k.split(' ', 1)[0], k.split(' ', 1)[1]) for k in MAP}:
            fails.append(f"{sid}: op not in the map: {method} {path}")
        elif MAP.get(f"{method} {normalise(rel)}") != owner:
            fails.append(f"{sid}: {method} {path} owner {owner} but map says {MAP[f'{method} {normalise(rel)}']}")
    for method, path in re.findall(r"(?<![\w/])(GET|POST|PATCH|PUT|DELETE) [\"`](/api/recovery/[^\"`\s]+)", t):
        m = re.match(r"^/api/recovery/([a-z-]+)/v1(/.*)?$", path)
        if not m:
            fails.append(f"{sid}: stray path {path}")
            continue
        rel = m.group(2) or "/"
        if f"{method} {normalise(rel)}" not in MAP:
            fails.append(f"{sid}: cited op not in the map: {method} {path}")
print()
print("FAIL" if fails else "PASS")
for f in fails:
    print(" -", f)
