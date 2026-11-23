"""Final targeted checks for B-PLT-LIB-02, including the queue expectation and the edit log."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("run_all", ROOT / "22 Microservice Realignment" / "checks" / "run_all.py")
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)

files = []
for w in ra._wp_writes("B-PLT-LIB-02"):
    p = ROOT / w
    if p.exists():
        files += [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else [p]
files += [p for p in (ra.WORK / "fragments").glob("RWB-PLT-*.json")]
files += [p for p in (ra.WORK / "gaps").glob("B-PLT-LIB-02.jsonl")]
files += [p for p in (ra.WORK / "assumptions").glob("B-PLT-LIB-02.jsonl")]

for name in ["C06", "C07", "C09", "C15", "C16", "C17", "C19", "C20"]:
    res = ra.ALL[name](files, wp="B-PLT-LIB-02") if name == "C18" else ra.ALL[name](files)
    hits = [f for f in res[1] if "B-PLT-LIB-02" in f]
    print(name, res[0], "total", len(res[1]), "ours", len(hits))
    for h in hits[:20]:
        print("  ", h)
