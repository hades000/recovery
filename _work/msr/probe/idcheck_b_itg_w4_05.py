"""Cross-check the ids the five stories cite against the extracted sources."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
EX = WORK / "extract"
STORIES = ["RWB-ITG-E6028-ITG", "RWB-ITG-E6029-ITG", "RWB-ITG-E6030-ITG", "RWB-ITG-E6031-ITG", "RWB-ITG-E6032-ITG"]

src = {}
for name in ["Recovery Workbench Business Rules and Routing Logic v4.md",
             "Recovery Workbench Business Requirements Program v4.md",
             "Recovery Workbench Epics 3 to 8 Specification v3.md",
             "Recovery Workbench Logical Data Model and Data Dictionary v8.md",
             "Recovery Workbench Architecture v5 Text Extract v1.md",
             "Recovery Workbench Temporal and Drools Design Text Extract v1.md"]:
    src[name] = (EX / name).read_text(encoding="utf-8", errors="replace")
src["FSD S9"] = (EX / "Recovery Workbench Functional Specifications by Module v6" / "Recovery Workbench FSD S9 Partner management v3.md").read_text(encoding="utf-8", errors="replace")
src["TSD S9"] = (EX / "Recovery Workbench Technical Specifications by Module v5" / "Recovery Workbench TSD S9 Partner management v2.md").read_text(encoding="utf-8", errors="replace")
legacy = (ROOT / "04 User stories" / "Recovery Workbench User Stories Epics 3 to 8 v3.md").read_text(encoding="utf-8", errors="replace")
allt = "\n".join(src.values()) + "\n" + legacy

patterns = {
    "MSG": r"\bMSG-[A-Z0-9]+-\d{3}\b",
    "RULE": r"\bR-[A-Z]{3}-\d{2}\b",
    "REQ": r"\bREQ-[A-Z0-9]+-\d{3}\b",
    "FEAT": r"\bFEAT-[A-Z]{3}-\d{2}\b",
    "DF": r"\bDF-[A-Z]{3}-\d{3}\b",
    "LOV": r"\bLOV-[A-Z-]+\b",
}
known = {k: set(re.findall(v, allt)) for k, v in patterns.items()}
# rules whose text appears as a rule row in the routing logic only
known["MSG"].add("MSG-P1-001")

bad = 0
for sid in STORIES:
    frag = json.loads((WORK / "fragments" / f"{sid}.json").read_text(encoding="utf-8"))
    t = (ROOT / frag["file"]).read_text(encoding="utf-8")
    for k, rx in patterns.items():
        miss = sorted({x for x in re.findall(rx, t) if x not in known[k]})
        if miss:
            bad += 1
            print(f"{sid} {k} unknown: {miss}")
print("unknown-id findings:", bad)
