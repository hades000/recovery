"""Merge the five per-key register shards of WP B-P4-01 into the two WP registers.

Run: python -I "_work/msr/smoke/merge_b_p4_01.py"
"""
import json
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
ROOT = WORK.parents[1]
KEYS = ["E1022", "E1037", "E1039", "E2019", "AD001"]


def num(rid):
    return int(rid.rsplit("-", 1)[1])


for kind, prefix in (("gap", "CG"), ("asm", "ASM")):
    rows, seen = [], set()
    for k in KEYS:
        p = WORK / "smoke" / f"{kind}-B-P4-01-{k}.jsonl"
        if not p.exists():
            raise SystemExit(f"missing shard {p}")
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            rid = r["id"]
            if not rid.startswith(f"{prefix}-B-P4-01-"):
                raise SystemExit(f"bad id {rid} in {p.name}")
            if rid in seen:
                raise SystemExit(f"duplicate id {rid}")
            seen.add(rid)
            rows.append(r)
    rows.sort(key=lambda r: (KEYS.index(r["id"].split("-")[4]), num(r["id"])))
    out = WORK / ("gaps" if kind == "gap" else "assumptions") / "B-P4-01.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(rows)} rows")
