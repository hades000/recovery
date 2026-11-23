"""Repair the fragment acs blocks of WP B-P4-01 so each one mirrors its story file.

Run: python -I "_work/msr/smoke/fix_frag_acs.py"
"""
import json, re
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
ROOT = WORK.parents[1]
IDS = ["RWB-P4-E1022-APP", "RWB-P4-E1022-CON", "RWB-P4-E1022-DB",
       "RWB-P4-E1037-APP", "RWB-P4-E1037-CON",
       "RWB-P4-E1039-APP", "RWB-P4-E1039-CON", "RWB-P4-E1039-DB", "RWB-P4-E1039-OPS",
       "RWB-P4-E2019-APP", "RWB-P4-E2019-CON", "RWB-P4-E2019-INF",
       "RWB-P4-AD001-APP", "RWB-P4-AD001-CON"]


def scenarios(text):
    out = []
    for m in re.finditer(r"Scenario: (AC\d+) ([^\n]*)\n(.*?)(?=\n\s*Scenario:|\n```|\Z)", text, re.S):
        head, body = m.group(2), m.group(3)
        tag = re.search(r"\((legacy RWB-[A-Z0-9-]+ (AC\d+)|new, D-RCV-60)\)\s*$", head)
        lines = [l.strip() for l in body.strip("\n").splitlines() if l.strip()]
        out.append((m.group(1), tag.group(1) if tag else "new, D-RCV-60", len(head) and lines[0] if lines else ""))
    return out


for sid in IDS:
    fp = WORK / "fragments" / f"{sid}.json"
    frag = json.loads(fp.read_text(encoding="utf-8"))
    text = (ROOT / frag["file"]).read_text(encoding="utf-8")
    acs = [{"id": a, "origin": o, "text_first_line": f} for a, o, f in scenarios(text)]
    if frag.get("acs") == acs:
        continue
    frag["acs"] = acs
    fp.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{sid}: acs = {len(acs)}")
print("done")
