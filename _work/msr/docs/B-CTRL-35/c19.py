import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"22 Microservice Realignment/checks").resolve()))
sys.path.insert(0, str(Path(r"22 Microservice Realignment/compat").resolve()))
import run_all as R
from common import ROOT
files = []
r = R.ALL["C19"](files)
hits = [f for f in r[1] if "B-CTRL-35" in f]
print("C19 total findings:", len(r[1]), "| B-CTRL-35 findings:", hits)
