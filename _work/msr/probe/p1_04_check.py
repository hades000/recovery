import sys, json
from pathlib import Path
sys.path.insert(0, "22 Microservice Realignment/checks")
import run_all as R
from common import ROOT
files = [ROOT/w for w in R._wp_writes("B-P1-04")]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print("n files", len(files))
for n in ["C06","C07","C09","C10","C11","C15","C16","C17","C20"]:
    try:
        fn = R.ALL[n]
        res = fn(files, wp="B-P1-04") if n=="C18" else fn(files)
        print(n, res[0], len(res[1]))
        for f in res[1][:8]:
            print("   ", f)
    except Exception as e:
        print(n, "CRASH", type(e).__name__, e)
