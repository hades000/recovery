import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("run_all", "22 Microservice Realignment/checks/run_all.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

files = [m.ROOT / w for w in m._wp_writes("B-REQ-PRD-S6")]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print("files", len(files))
for name in ("C14", "C15", "C16", "C17", "C20"):
    fn = m.ALL[name]
    res = fn(files, wp="B-REQ-PRD-S6") if name == "C18" else fn(files)
    print(name, res[0], len(res[1]), res[1][:3])
