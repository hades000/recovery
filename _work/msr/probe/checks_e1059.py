"""Run the relevant check functions from checks/run_all.py against the six files of this key only."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "compat"))
import run_all as r

files = [
    ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1059 APP Case intake agent in shadow [E1b] v1.md",
    ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)/RWB P10 E1059 CON Case intake agent in shadow [E1b] - contract v1.md",
    ROOT / "_work/msr/fragments/RWB-P10-E1059-APP.json",
    ROOT / "_work/msr/fragments/RWB-P10-E1059-CON.json",
    ROOT / "_work/msr/gaps/B-P10-01-E1059.jsonl",
    ROOT / "_work/msr/assumptions/B-P10-01-E1059.jsonl",
]
checks = [r.c02, r.c03, r.c05, r.c12, r.c13, r.c16, r.c17, r.c20]
bad = 0
for c in checks:
    res, findings = c(files)
    print(c.__name__, res, len(findings))
    for f in findings:
        print("  -", f)
    bad += res == "FAIL"
print("OK" if not bad else "FAILURES")
sys.exit(1 if bad else 0)
