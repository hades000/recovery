"""Merge the per-key candidate rows of B-ITG-W4-05 into the WP register files."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
WP = "B-ITG-W4-05"
KEYS = ["E6028", "E6029", "E6030", "E6031", "E6032"]


def rows(kind, key):
    p = WORK / "logs" / f"{WP}-{key}-{kind}s.jsonl" if kind == "assumption" else WORK / "logs" / f"{WP}-{key}-gaps.jsonl"
    if kind == "assumption":
        p = WORK / "logs" / f"{WP}-{key}-assumptions.jsonl"
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(json.loads(line))
    return out


def order(r):
    m = re.search(r"-E(\d{4})-(\d+)$", r.get("id", ""))
    return (m.group(1) if m else "", int(m.group(2)) if m else 0)


for kind, dest in (("gap", WORK / "gaps" / f"{WP}.jsonl"), ("assumption", WORK / "assumptions" / f"{WP}.jsonl")):
    all_rows = []
    for key in KEYS:
        all_rows += rows(kind, key)
    all_rows.sort(key=order)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8", newline="\n") as f:
        for r in all_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(kind, len(all_rows), "->", dest.relative_to(ROOT))
    for r in all_rows:
        print("   ", r.get("id"))
