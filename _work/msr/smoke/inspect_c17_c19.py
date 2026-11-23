"""Inspect C17 findings and the B-PLT-LIB-02 C19 expectations directly."""
import importlib.util, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("run_all", ROOT / "22 Microservice Realignment" / "checks" / "run_all.py")
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)

res = ra.c17([])
print("C17", res[0], len(res[1]))
for f in res[1]:
    print("  ", f)

print("C19 for our WP:")
fails = []
for q in sorted((ra.WORK / "wp").glob("queue-*.json")):
    for item in json.loads(q.read_text(encoding="utf-8")):
        if item.get("wp") != "B-PLT-LIB-02":
            continue
        for e in item.get("expect", []):
            p = ROOT / e
            if not p.exists():
                fails.append(f"missing: {e}")
            elif p.suffix == ".md" and "editlog" not in e and "fragments" not in e and ra.decision() not in ra._t(p):
                fails.append(f"no decision row: {e}")
print("  fails", fails)
