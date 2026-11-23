import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"22 Microservice Realignment/checks").resolve()))
sys.path.insert(0, str(Path(r"22 Microservice Realignment/compat").resolve()))
import run_all as R
from common import ROOT

files = [ROOT / w for w in R._wp_writes("B-CTRL-35")]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print("files in scope:", len(files))
for n in ("C01", "C14", "C17", "C19", "C20", "C08", "C15", "C16"):
    fn = R.ALL[n]
    res = fn(files, wp="B-CTRL-35") if n == "C18" else fn(files)
    print(n, res[0], len(res[1]))
    for f in res[1][:12]:
        print("   ", f)
