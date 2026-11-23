"""Probe: run the C-checks directly over the B-P2-01 files (story paths are truncated by _wp_writes)."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R22 = ROOT / "22 Microservice Realignment"
spec = importlib.util.spec_from_file_location("run_all", R22 / "checks" / "run_all.py")
ra = importlib.util.module_from_spec(spec)
sys.modules["run_all"] = ra
spec.loader.exec_module(ra)

STORY_DIR = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P2 rwb-integration (Integration)"
IDS = [
    "RWB-P2-E1007-APP", "RWB-P2-E1007-CON", "RWB-P2-E1007-INF", "RWB-P2-E1007-OPS",
    "RWB-P2-E2001-APP", "RWB-P2-E2001-CON", "RWB-P2-E2001-OPS",
    "RWB-P2-E2002-APP", "RWB-P2-E2002-CON", "RWB-P2-E2002-OPS",
    "RWB-P2-E2007-APP", "RWB-P2-E2007-CON", "RWB-P2-E2007-OPS",
    "RWB-P2-E2033-APP", "RWB-P2-E2033-CON",
]
files = []
for sid in IDS:
    frag = json.loads((ROOT / "_work" / "msr" / "fragments" / f"{sid}.json").read_text(encoding="utf-8"))
    files.append(ROOT / "_work" / "msr" / "fragments" / f"{sid}.json")
    files.append(ROOT / frag["file"])
files += [
    ROOT / "_work" / "msr" / "gaps" / "B-P2-01.jsonl",
    ROOT / "_work" / "msr" / "assumptions" / "B-P2-01.jsonl",
    ROOT / "_work" / "msr" / "editlog" / "B-P2-01.md",
]
files = [f for f in files if f.exists()]

mine = {f.name for f in files} | {"B-P2-01.jsonl", "B-P2-01.md"}
names = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09",
         "C12", "C13", "C14", "C15", "C16", "C18", "C20"]
bad = 0
for n in names:
    fn = ra.ALL[n]
    try:
        res = fn(files, wp="B-P2-01") if n == "C18" else fn(files)
    except Exception as e:  # noqa: BLE001
        print(n, "CRASH", type(e).__name__, e)
        bad += 1
        continue
    considered = [x for x in res[1] if any(m in x for m in mine)]
    print(n, res[0], len(res[1]), "| involving B-P2-01 files:", len(considered))
    for x in considered[:8]:
        print("   -", x)
    if considered:
        bad += 1
print("files checked:", len(files))
print("RESULT", "PASS" if not bad else f"{bad} check(s) with B-P2-01 findings")
sys.exit(1 if bad else 0)
