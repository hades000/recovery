"""B-P4-01 probe 3: run the checks tool functions directly on the 14 story files."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
import run_all as R

FOLDER = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P4 rwb-access (Access and authority)"
files = sorted(p for p in FOLDER.glob("RWB P4 *.md")
               if any(k in p.name for k in ("E1022", "E1037", "E1039", "E2019", "AD001")))
print("files:", len(files))
for n in ("C02", "C03", "C05", "C12", "C13", "C15", "C16", "C17", "C20"):
    res, findings = R.ALL[n](files)
    print(n, res, len(findings), findings[:3])
