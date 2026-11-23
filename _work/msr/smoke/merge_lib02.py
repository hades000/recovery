"""Merge the per-key B-PLT-LIB-02 candidate rows into the WP registers, then drop the per-key temps."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
KEYS = ["E1047", "E1072", "TE006", "NF02"]

def merge(kind):
    out = WORK / kind / "B-PLT-LIB-02.jsonl"
    rows, seen = [], set()
    for key in KEYS:
        p = WORK / kind / f"B-PLT-LIB-02-{key}.jsonl"
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row["id"] in seen:
                continue
            seen.add(row["id"])
            rows.append(row)
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(kind, len(rows), "rows")
    for key in KEYS:
        (WORK / kind / f"B-PLT-LIB-02-{key}.jsonl").unlink()

merge("gaps")
merge("assumptions")
