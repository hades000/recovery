"""Run every check C01-C20 of run_all.py directly on the 13 files of WP B-P7-08.

The WP path reader in run_all.py splits an allowed path at the first " (" and so
shortens the story folder name of this WP; this runner passes the full paths.
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHECK = ROOT / "22 Microservice Realignment" / "checks" / "run_all.py"
FOLDER = "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P7 rwb-decision (Decision and rules)"
STORIES = [
    "RWB P7 E1073 APP Rule authoring, validation, test scenarios, approval and rollback in Drools v1.md",
    "RWB P7 E2001 APP EFS hand-over with full history v1.md",
    "RWB P7 E2002 APP ACE plan status on the case v1.md",
    "RWB P7 E2004 APP Treatment entity and plan timers data model v1.md",
    "RWB P7 E2006 APP Credit approval pack for NLEADS v1.md",
]
IDS = ["E1073", "E2001", "E2002", "E2004", "E2006"]

spec = importlib.util.spec_from_file_location("run_all", CHECK)
run_all = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_all)

files = [ROOT / FOLDER / s for s in STORIES]
files += [ROOT / "_work" / "msr" / "fragments" / f"RWB-P7-{i}-APP.json" for i in IDS]
files += [ROOT / "_work" / "msr" / k / "B-P7-08.jsonl" for k in ("gaps", "assumptions")]
files += [ROOT / "_work" / "msr" / "editlog" / "B-P7-08.md"]
files = [f for f in files if f.exists()]

missing = [str(f.relative_to(ROOT)) for f in [ROOT / FOLDER / s for s in STORIES]
           if not f.exists()]
if missing:
    print("MISSING", missing)

bad = 0
for n in [f"C{i:02d}" for i in range(1, 21)]:
    fn = getattr(run_all, n.lower())
    try:
        res = fn(files, wp="B-P7-08") if n == "C18" else fn(files)
        result, findings = res
    except Exception as e:  # noqa: BLE001
        result, findings = "CRASH", [f"{type(e).__name__}: {e}"]
    if result != "PASS":
        bad += 1
    print(n, result, len(findings))
    for f in findings[:12]:
        print("   -", f)

print("files checked:", len(files))
sys.exit(1 if bad else 0)
