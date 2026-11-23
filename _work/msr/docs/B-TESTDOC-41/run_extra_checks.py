"""Run every check C01-C20 over this WP's file set (the quick list is C02,C03,C05,C12,C13,C18)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path("22 Microservice Realignment/checks").resolve()))
sys.path.insert(0, str(Path("22 Microservice Realignment/compat").resolve()))
import run_all as R
from common import ROOT

wp = "B-TESTDOC-41"
files = [ROOT / w for w in R._wp_writes(wp)]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print("files:", len(files))
for n in ("C14", "C15", "C16", "C17", "C19", "C20", "C01", "C04"):
    fn = R.ALL[n]
    res = fn(files, wp=wp) if n == "C18" else fn(files)
    print(n, res[0], len(res[1]))
    for f in res[1][:10]:
        print("   -", f)
