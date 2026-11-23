import sys, json
from pathlib import Path
sys.path.insert(0, "22 Microservice Realignment/compat")
sys.path.insert(0, "22 Microservice Realignment/checks")
from common import ROOT
import run_all as R

files = [ROOT / w for w in R._wp_writes("B-REQ-PRD-S4")]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
for name in ("C17", "C14", "C19"):
    fn = R.ALL[name]
    if name == "C17":
        res = fn(files)
    else:
        res = fn(files)
    print(name, res[0], len(res[1]))
    for x in res[1][:10]:
        print("   ", x)
print("files checked:", len(files))
