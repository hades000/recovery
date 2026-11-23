import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "compat"))
import run_all as R

files = [ROOT / w for w in R._wp_writes("B-ITG-W2-01")]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print("files:", len(files))
for n in ["C02", "C03", "C05", "C06", "C07", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C19", "C20"]:
    try:
        res = R.ALL[n](files) if n != "C18" else R.ALL[n](files, wp="B-ITG-W2-01")
    except Exception as e:
        res = ("FAIL", [f"crashed: {type(e).__name__}: {e}"])
    print(n, res[0], len(res[1]))
    for f in res[1][:12]:
        print("   ", f)
