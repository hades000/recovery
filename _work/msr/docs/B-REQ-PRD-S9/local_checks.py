"""Run the non-quick checks against this WP's outputs only."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "22 Microservice Realignment" / "checks"))
import run_all as R

WP = "B-REQ-PRD-S9"
files = [R.ROOT / w for w in R._wp_writes(WP)]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print(len(files), "output files")
for n in ["C01", "C04", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C20"]:
    fn = R.ALL[n]
    res = fn(files, wp=WP) if n == "C18" else fn(files)
    print(n, res[0], len(res[1]))
    for f in res[1][:12]:
        print("   ", f)
