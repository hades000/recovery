"""Stage-B style checks over the B-P7-01 file set only (C02, C03, C05, C06, C07, C12, C13, C15, C16, C17, C18, C20)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
import run_all as R  # noqa: E402

WORK = ROOT / "_work" / "msr"
STORY_DIR = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P7 rwb-decision (Decision and rules)"
IDS = ["RWB-P7-E1008-APP", "RWB-P7-E1008-CON", "RWB-P7-E1008-DB", "RWB-P7-E1008-OPS", "RWB-P7-E1027-APP",
       "RWB-P7-E1027-CON", "RWB-P7-E2005-APP", "RWB-P7-E2005-CON", "RWB-P7-E2013-APP", "RWB-P7-E2013-CON",
       "RWB-P7-E2013-OPS", "RWB-P7-E2014-APP", "RWB-P7-E2014-CON", "RWB-P7-E2014-OPS"]
files = [p for p in STORY_DIR.glob("RWB P7 E1*.md") if "E1008" in p.name or "E1027" in p.name]
files += [p for p in STORY_DIR.glob("RWB P7 E2*.md") if "E2005" in p.name or "E2013" in p.name or "E2014" in p.name]
files += [WORK / "fragments" / f"{i}.json" for i in IDS]
files += [WORK / "gaps" / "B-P7-01.jsonl", WORK / "assumptions" / "B-P7-01.jsonl"]
files = [f for f in files if f.exists()]
print("files:", len(files))

for name in ("C02", "C03", "C05", "C12", "C13", "C15", "C16", "C17", "C20"):
    res, findings = R.ALL[name](files)
    print(name, res, len(findings))
    for f in findings:
        print("   ", f)
for name in ("C06", "C07", "C08"):
    res, findings = R.ALL[name](files)
    mine = [f for f in findings if any(i.split("-P7-")[1].split("-")[0] and f.startswith(i) for i in IDS)]
    print(name, res, f"{len(findings)} findings, {len(mine)} mine")
    for f in mine[:20]:
        print("   ", f)
