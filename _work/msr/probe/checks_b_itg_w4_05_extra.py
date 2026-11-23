"""Run the remaining checks (C04, C11, C14-C17, C19, C20) against the B-ITG-W4-05 outputs."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
import run_all  # noqa: E402

files = [ROOT / w for w in run_all._wp_writes("B-ITG-W4-05")]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print("files:", len(files))
for name in ("C01", "C04", "C06", "C07", "C08", "C09", "C10", "C11", "C14", "C15", "C16", "C17", "C19", "C20"):
    fn = run_all.ALL[name]
    try:
        res = fn(files, wp="B-ITG-W4-05") if name == "C18" else fn(files)
    except Exception as e:  # noqa: BLE001
        res = ("FAIL", [f"crashed {type(e).__name__}: {e}"])
    print(name, res[0], len(res[1]))
    for f in res[1][:12]:
        print("   -", f)
