"""Targeted coverage check for the four legacy keys of B-PLT-LIB-02."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("run_all", ROOT / "22 Microservice Realignment" / "checks" / "run_all.py")
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)

KEYS = {"RWB-E1-047", "RWB-E1-072", "RWB-TE-006", "NF-02"}
plan = ra._plan()
owned = {}
for f in ra._frags().values():
    for a in f.get("acs", []):
        owned.setdefault(f.get("legacy"), set()).add(a.get("id") if isinstance(a, dict) else a)
idx = {r["key"]: r for r in ra.read_json(ra.WORK / "plan" / "legacy_index.json", [])}
for k in KEYS:
    v = plan["legacy"].get(k, {})
    miss = [a for a in idx.get(k, {}).get("acs", []) if a not in owned.get(k, set())]
    print(k, "disposition", v.get("disposition"), "missing ACs", miss)

seen = set()
for x in plan["slices"]:
    p = ROOT / x["file"]
    if p.exists():
        seen.update(ra.re.findall(r"\bTC-[A-Z0-9]+-\d{3}-\d{2}\b", ra._t(p)))
for k in KEYS:
    miss = [t for t in idx.get(k, {}).get("tcs", []) if t not in seen]
    print(k, "missing TCs", miss)
