import sys
sys.path.insert(0, "22 Microservice Realignment/compat")
sys.path.insert(0, "22 Microservice Realignment/checks")
from common import ROOT
import run_all as R

res = R.ALL["C19"]()
mine = [x for x in res[1] if "B-REQ-PRD-S4" in x or "PRD S4" in x]
print("total", len(res[1]), "mine", len(mine))
for m in mine:
    print("  ", m)
