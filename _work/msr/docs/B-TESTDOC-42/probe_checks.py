"""Run the checks outside the quick set against this WP's own outputs."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
import run_all  # noqa: E402

WP = "B-TESTDOC-42"
files = [ROOT / w for w in run_all._wp_writes(WP)]
files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
print(len(files), "files")
for name in ("C01", "C14", "C17", "C19", "C20"):
    fn = run_all.ALL[name]
    res = fn(files, wp=WP) if name == "C18" else fn(files)
    print(name, res[0], len(res[1]))
    for x in res[1][:12]:
        print("   ", x)
