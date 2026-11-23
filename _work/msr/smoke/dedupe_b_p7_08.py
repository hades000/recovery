"""Confirm the merged registers of WP B-P7-08 hold every part row once, then
remove the per-key part files so the two registers carry each row exactly once.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
KEYS = ["E1073", "E2001", "E2002", "E2004", "E2006"]

bad = []
for kind in ("gaps", "assumptions"):
    merged = WORK / kind / "B-P7-08.jsonl"
    rows = [json.loads(l) for l in merged.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    by_id = {}
    for r in rows:
        if r["id"] in by_id:
            bad.append(f"duplicate in merged {kind}: {r['id']}")
        by_id[r["id"]] = json.dumps(r, sort_keys=True, ensure_ascii=False)
    part_total = 0
    for key in KEYS:
        p = WORK / kind / f"B-P7-08-{key}.part.jsonl"
        for line in p.read_text(encoding="utf-8-sig").splitlines():
            if not line.strip():
                continue
            part_total += 1
            r = json.loads(line)
            if r["id"] not in by_id:
                bad.append(f"{p.name}: {r['id']} missing from merged {kind}")
            elif by_id[r["id"]] != json.dumps(r, sort_keys=True, ensure_ascii=False):
                bad.append(f"{p.name}: {r['id']} differs from merged {kind}")
    if part_total != len(rows):
        bad.append(f"{kind}: part rows {part_total} != merged rows {len(rows)}")
    print(f"{kind}: merged={len(rows)} part={part_total}")

if bad:
    for b in bad[:50]:
        print("FAIL", b)
    sys.exit(1)

for kind in ("gaps", "assumptions"):
    for key in KEYS:
        p = WORK / kind / f"B-P7-08-{key}.part.jsonl"
        if p.exists():
            p.unlink()
            print("removed", p.relative_to(ROOT))
