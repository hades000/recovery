"""Run C14, C17 and C20 against the same file set the WP writes, as the quick run does."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path("22 Microservice Realignment/checks").resolve()))
sys.path.insert(0, str(Path("22 Microservice Realignment/compat").resolve()))
import run_all as R
from common import ROOT

WP = "B-DELIVDOC-44"
files = []
for w in R._wp_writes(WP):
    p = ROOT / w
    files += [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else ([p] if p.exists() else [])
print("files", len(files))
for f in files:
    print("  ", f.relative_to(ROOT))
for name in ("C14", "C17", "C20"):
    print(name, R.ALL[name](files, wp=WP) if name == "C18" else R.ALL[name](files))
