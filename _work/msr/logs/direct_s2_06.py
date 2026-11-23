"""Scratch direct check for WP B-S2-06 (not a deliverable). The --wp path parser truncates
folder names containing ' (', so the story files are checked here with an explicit list."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
import run_all as R

W = ROOT / "_work" / "msr"
stories = [ROOT / f["file"] for f in (
    __import__("json").loads((W / "fragments" / f"RWB-S2-E20{n}-APP.json").read_text(encoding="utf-8"))
    for n in (25, 26, 27, 32))]
files = stories + [ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Story Template and Rules v1.md"]
files += [W / "gaps" / "B-S2-06.jsonl", W / "assumptions" / "B-S2-06.jsonl"]
files += sorted((W / "fragments").glob("RWB-S2-E20*.json"))

for name in ("c02", "c03", "c05", "c12", "c13", "c16", "c17", "c20"):
    res, findings = getattr(R, name)(files)
    print(name.upper(), res, len(findings))
    for f in findings:
        print("   ", f)
for name in ("c06", "c07", "c15"):
    res, findings = getattr(R, name)(None)
    print(name.upper(), res, len(findings))
    for f in findings:
        print("   ", f)
