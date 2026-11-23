"""Run the wider checks (C14, C17, C19, C20) over the WP C3-TC file set only."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path("22 Microservice Realignment/checks").resolve()))
import run_all as R
from common import ROOT

wp = "C3-TC"
files = [ROOT / w for w in R._wp_writes(wp)]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print("files", len(files))
for name, fn in (("C14", R.c14), ("C17", R.c17), ("C18", lambda f: R.c18(f, wp=wp)), ("C20", R.c20)):
    res = fn(files)
    print(name, res[0], len(res[1]))
    for x in res[1][:10]:
        print("   ", x)
