import sys, json, io, re, glob
sys.path.insert(0, r"22 Microservice Realignment/compat")
from common import ROOT, WORK
import importlib.util
spec = importlib.util.spec_from_file_location("ra", r"22 Microservice Realignment/checks/run_all.py")
ra = importlib.util.module_from_spec(spec); spec.loader.exec_module(ra)
files = []
for line in (WORK/"wp"/"B-ITG-W2-03.md").read_text(encoding="utf-8").split("Write only:")[1].split("\nDo",1)[0].splitlines():
    if line.startswith("- "):
        p = ROOT/line[2:].split(" (")[0].strip()
        files += [x for x in p.rglob("*") if x.is_file()] if p.is_dir() else ([p] if p.exists() else [])
for fn in ("c17","c06","c07","c15"):
    try:
        r = getattr(ra, fn)(files)
        print(fn, r[0], len(r[1]), r[1][:5])
    except Exception as e:
        print(fn, "ERR", e)
