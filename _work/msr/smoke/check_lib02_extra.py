"""Run the non-quick WP checks that are safe to run for this WP and print only findings that touch B-PLT-LIB-02."""
import importlib.util, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("run_all", ROOT / "22 Microservice Realignment" / "checks" / "run_all.py")
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)

files = []
for w in ra._wp_writes("B-PLT-LIB-02"):
    p = ROOT / w
    if p.exists():
        files.append(p)
for p in (ra.WORK / "fragments").glob("RWB-PLT-*.json"):
    files.append(p)
for p in (ra.WORK / "gaps").glob("B-PLT-LIB-02.jsonl"):
    files.append(p)
for p in (ra.WORK / "assumptions").glob("B-PLT-LIB-02.jsonl"):
    files.append(p)

for name in ["C06", "C07", "C09", "C10", "C11", "C15", "C16", "C17", "C20"]:
    try:
        res = ra.ALL[name](files)
    except Exception as e:
        res = ("FAIL", [f"crashed: {type(e).__name__}: {e}"])
    hits = [f for f in res[1] if "B-PLT-LIB-02" in f or any(p.name in f for p in files)]
    print(name, res[0], "total", len(res[1]), "ours", len(hits))
    for h in hits[:20]:
        print("  ", h)
