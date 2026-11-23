import sys, json, re
from pathlib import Path
sys.path.insert(0, "22 Microservice Realignment/checks")
sys.path.insert(0, "22 Microservice Realignment/compat")
import run_all as R

wp = "B-P4-03"
allowed = R._wp_writes(wp)
files = []
for a in allowed:
    p = R.ROOT / a
    if p.is_dir():
        files += [x for x in p.rglob("*") if x.is_file()]
    elif p.exists():
        files.append(p)
print("files", len(files))
for name in ("C02", "C03", "C05", "C06", "C07", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20"):
    fn = R.ALL[name]
    try:
        res = fn(files, wp=wp) if name == "C18" else fn(files)
    except Exception as e:
        res = ("FAIL", [f"crashed: {type(e).__name__}: {e}"])
    print(name, res[0], len(res[1]))
    for x in res[1][:12]:
        print("   -", x)
