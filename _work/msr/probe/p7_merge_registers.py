"""Merge the key-scoped B-P7-01 register parts into the two WP registers, then drop the parts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
WP = "B-P7-01"
ORDER = ["E1008", "E1027", "E2005", "E2013", "E2014"]
REQ_G = {"id", "title", "source", "section", "description", "evidence", "type", "area", "severity",
         "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"}
REQ_A = {"id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"}

for kind, req in (("gaps", REQ_G), ("assumptions", REQ_A)):
    rows, seen, parts = [], set(), []
    for key in ORDER:
        p = WORK / kind / f"{WP}._p-{key}.jsonl"
        n = 0
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            miss = req - {k for k, v in r.items() if v not in (None, "")}
            if miss:
                raise SystemExit(f"{p.name}: {r.get('id')} missing {sorted(miss)}")
            if r["id"] in seen:
                raise SystemExit(f"duplicate id {r['id']}")
            seen.add(r["id"]); rows.append(r); n += 1
        parts.append((p, n))
    out = WORK / kind / f"{WP}.jsonl"
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(f"{kind}: {len(rows)} rows -> {out.relative_to(ROOT)}  from", ", ".join(f"{p.name.split('._p-')[1]}:{n}" for p, n in parts))
    for p, _ in parts:
        p.unlink()
    print("  parts removed:", len(parts))
