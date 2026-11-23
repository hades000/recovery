"""Probe: every B-P2-01 gap/assumption citation in fragments and stories resolves."""
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
IDS = [
    "RWB-P2-E1007-APP", "RWB-P2-E1007-CON", "RWB-P2-E1007-INF", "RWB-P2-E1007-OPS",
    "RWB-P2-E2001-APP", "RWB-P2-E2001-CON", "RWB-P2-E2001-OPS",
    "RWB-P2-E2002-APP", "RWB-P2-E2002-CON", "RWB-P2-E2002-OPS",
    "RWB-P2-E2007-APP", "RWB-P2-E2007-CON", "RWB-P2-E2007-OPS",
    "RWB-P2-E2033-APP", "RWB-P2-E2033-CON",
]


def load(path):
    return [json.loads(line) for line in io.open(path, encoding="utf-8") if line.strip()]


gaps = {r["id"] for r in load(WORK / "gaps" / "B-P2-01.jsonl")}
asms = {r["id"] for r in load(WORK / "assumptions" / "B-P2-01.jsonl")}
fails = []
cited_g = set()
cited_a = set()

for sid in IDS:
    frag = json.loads((WORK / "fragments" / f"{sid}.json").read_text(encoding="utf-8"))
    for gid in list(frag.get("gaps", [])) + [r.get("id") for r in frag.get("gap_rows", []) if isinstance(r, dict)]:
        cited_g.add(gid)
        if gid not in gaps:
            fails.append(f"{sid}: gap {gid} not in register")
    for aid in list(frag.get("assumptions", [])) + [r.get("id") for r in frag.get("asm_rows", []) if isinstance(r, dict)]:
        cited_a.add(aid)
        if aid not in asms:
            fails.append(f"{sid}: assumption {aid} not in register")
    for r in frag.get("asm_rows", []):
        if isinstance(r, dict) and r.get("gap") and r["gap"] not in gaps:
            fails.append(f"{sid}: {r.get('id')} cites gap {r['gap']} not in register")
    story = (ROOT / frag["file"]).read_text(encoding="utf-8-sig")
    for gid in set(re.findall(r"CG-B-P2-01-[A-Za-z0-9-]+", story)):
        if gid not in gaps:
            fails.append(f"{sid} story: gap {gid} not in register")
    for aid in set(re.findall(r"ASM-B-P2-01-[A-Za-z0-9-]+", story)):
        if aid not in asms:
            fails.append(f"{sid} story: assumption {aid} not in register")

print(f"register ids: {len(gaps)} gaps, {len(asms)} assumptions")
print(f"cited by B-P2-01 fragments: {len(cited_g & gaps)} gaps, {len(cited_a & asms)} assumptions")
unused_g = gaps - cited_g
unused_a = asms - cited_a
if unused_g:
    print("gaps not cited by any B-P2-01 fragment:", sorted(unused_g))
if unused_a:
    print("assumptions not cited by any B-P2-01 fragment:", sorted(unused_a))
if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("PASS every citation resolves")
