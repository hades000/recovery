import sys
sys.path.insert(0, r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\22 Microservice Realignment\checks")
import run_all as R
from pathlib import Path

wp = "B-REQ-PRD-S2"
files = [R.ROOT / w for w in R._wp_writes(wp)]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print("files", len(files))
for n in ("c14", "c15", "c16", "c17", "c19", "c20"):
    fn = getattr(R, n)
    try:
        res = fn(files)
    except Exception as e:
        res = ("FAIL", [f"crashed {type(e).__name__}: {e}"])
    print(n.upper(), res[0], len(res[1]))
    for x in res[1][:12]:
        print("   -", x)
