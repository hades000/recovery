"""Normalise the DoA event spelling in the B-P7-01 files: DoLimitChanged and DoaLimitChanged -> DoaLimitChanged."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
STORY_DIR = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P7 rwb-decision (Decision and rules)"
FILES = [
    "RWB P7 E1008 APP Decision log store v1, append only and hash chained v1.md",
    "RWB P7 E1008 CON Decision log store v1, append only and hash chained - contract v1.md",
    "RWB P7 E1008 DB Decision log store v1, append only and hash chained - ACE DB v1.md",
    "RWB P7 E1008 OPS Decision log store v1, append only and hash chained - deployment v1.md",
    "RWB P7 E1027 APP Decision log writer v1 v1.md",
    "RWB P7 E1027 CON Decision log writer v1 - contract v1.md",
    "RWB P7 E2005 APP Decision log query API for audit v1.md",
    "RWB P7 E2005 CON Decision log query API for audit - contract v1.md",
    "RWB P7 E2013 APP Approval routing with the delegation of authority table v1.md",
    "RWB P7 E2013 CON Approval routing with the delegation of authority table - contract v1.md",
    "RWB P7 E2013 OPS Approval routing with the delegation of authority table - deployment v1.md",
    "RWB P7 E2014 APP Approval screen for D7.1 demand and recall notices v1.md",
    "RWB P7 E2014 CON Approval screen for D7.1 demand and recall notices - contract v1.md",
    "RWB P7 E2014 OPS Approval screen for D7.1 demand and recall notices - deployment v1.md",
]
FRAGS = ["RWB-P7-E1008-APP", "RWB-P7-E1008-CON", "RWB-P7-E1008-DB", "RWB-P7-E1008-OPS", "RWB-P7-E1027-APP",
         "RWB-P7-E1027-CON", "RWB-P7-E2005-APP", "RWB-P7-E2005-CON", "RWB-P7-E2013-APP", "RWB-P7-E2013-CON",
         "RWB-P7-E2013-OPS", "RWB-P7-E2014-APP", "RWB-P7-E2014-CON", "RWB-P7-E2014-OPS"]
TMP = sorted(WORK.glob("gaps/B-P7-01._p-*.jsonl")) + sorted(WORK.glob("assumptions/B-P7-01._p-*.jsonl"))

changed = []
for p in [STORY_DIR / f for f in FILES] + [WORK / "fragments" / f"{i}.json" for i in FRAGS] + TMP:
    if not p.exists():
        print("missing:", p.name); continue
    t = p.read_text(encoding="utf-8")
    n = t.replace("DoaLimitChanged", "DoaLimitChanged").replace("DoLimitChanged", "DoaLimitChanged")
    if n != t:
        p.write_text(n, encoding="utf-8")
        changed.append((p.name, t.count("DoaLimitChanged") + t.count("DoLimitChanged")))
print("files changed:", len(changed))
for n, c in changed:
    print(" ", n, "->", c, "occurrences normalised")
for p in [WORK / "fragments" / f"{i}.json" for i in FRAGS]:
    json.loads(p.read_text(encoding="utf-8"))
print("fragments still parse: ok")
