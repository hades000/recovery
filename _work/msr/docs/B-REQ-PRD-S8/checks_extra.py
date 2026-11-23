import sys
from pathlib import Path
sys.path.insert(0, "22 Microservice Realignment/checks")
sys.path.insert(0, "22 Microservice Realignment/compat")
import run_all as R
from common import ROOT

files = [ROOT / w for w in R._wp_writes("B-REQ-PRD-S8")]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print("files checked:", [str(f.relative_to(ROOT)) for f in files])
for n in ["C14", "C17", "C19", "C20", "C01"]:
    try:
        res = R.ALL[n](files)
    except Exception as e:
        res = ("ERROR", [f"{type(e).__name__}: {e}"])
    print(n, res[0], len(res[1]))
    for x in res[1][:20]:
        print("   -", x)
