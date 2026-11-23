"""Probe: B-P2-01 fragment tcs vs story section 16 tables, and fragment id arrays."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
IDS = sorted(
    [
        "RWB-P2-E1007-APP", "RWB-P2-E1007-CON", "RWB-P2-E1007-INF", "RWB-P2-E1007-OPS",
        "RWB-P2-E2001-APP", "RWB-P2-E2001-CON", "RWB-P2-E2001-OPS",
        "RWB-P2-E2002-APP", "RWB-P2-E2002-CON", "RWB-P2-E2002-OPS",
        "RWB-P2-E2007-APP", "RWB-P2-E2007-CON", "RWB-P2-E2007-OPS",
        "RWB-P2-E2033-APP", "RWB-P2-E2033-CON",
    ]
)

fails = []
for sid in IDS:
    fp = WORK / "fragments" / f"{sid}.json"
    if not fp.exists():
        fails.append(f"{sid}: missing fragment")
        continue
    frag = json.loads(fp.read_text(encoding="utf-8"))
    sp = ROOT / frag["file"]
    if not sp.exists():
        fails.append(f"{sid}: missing story {frag['file']}")
        continue
    txt = sp.read_text(encoding="utf-8-sig")
    m = re.search(r"(?ms)^#{2,4} 16\b.*?(?=^#{2,4} 17\b)", txt)
    if not m:
        fails.append(f"{sid}: no section 16")
        continue
    story_tcs = re.findall(r"^\|\s*(TC-[A-Za-z0-9-]+)\s*\|", m.group(0), re.M)
    if frag["tcs"] != story_tcs:
        fails.append(f"{sid}: tcs differ from section 16\n  frag : {frag['tcs']}\n  story: {story_tcs}")
    # id arrays must match the row ids present
    for pair in (("gaps", "gap_rows"), ("assumptions", "asm_rows")):
        ids = frag.get(pair[0], [])
        rows = frag.get(pair[1], [])
        row_ids = [r if isinstance(r, str) else r.get("id") for r in rows]
        if ids != row_ids:
            fails.append(f"{sid}: {pair[0]} {ids} != {pair[1]} ids {row_ids}")

print(f"fragments checked: {len(IDS)}")
if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("PASS all fragment tcs match their story section 16 tables")
