"""Probe: add ASM-B-P2-01-E2033-11 to RWB-P2-E2033-CON (list and row)."""
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
frag_p = WORK / "fragments" / "RWB-P2-E2033-CON.json"
reg = [
    json.loads(line)
    for line in io.open(WORK / "assumptions" / "B-P2-01.jsonl", encoding="utf-8")
    if line.strip()
]
row = {r["id"]: r for r in reg}["ASM-B-P2-01-E2033-11"]
frag = json.loads(frag_p.read_text(encoding="utf-8"))

if "ASM-B-P2-01-E2033-11" in frag["assumptions"]:
    print("already in list")
else:
    a = frag["assumptions"]
    a.insert(a.index("ASM-B-P2-01-E2033-10") + 1 if "ASM-B-P2-01-E2033-10" in a else len(a), "ASM-B-P2-01-E2033-11")

rows = frag["asm_rows"]
if any(r.get("id") == "ASM-B-P2-01-E2033-11" for r in rows):
    print("already in rows")
else:
    idx = [r.get("id") for r in rows].index("ASM-B-P2-01-E2033-10") + 1
    rows.insert(idx, row)

frag_p.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
out = json.loads(frag_p.read_text(encoding="utf-8"))
print("assumptions", out["assumptions"])
print("asm_rows", [r.get("id") for r in out["asm_rows"]])
