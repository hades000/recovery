"""Scratch merge for WP B-S2-06 registers (not a deliverable)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
W = ROOT / "_work" / "msr"
PARTS = W / "logs" / "B-S2-06-parts"
ORDER = ["RWB-S2-E2025-APP", "RWB-S2-E2026-APP", "RWB-S2-E2027-APP", "RWB-S2-E2032-APP"]
GAP_KEYS = ["id", "title", "source", "section", "description", "evidence", "type", "area", "severity",
            "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"]
ASM_KEYS = ["id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"]

out = {"gaps": [], "assumptions": []}
seen = set()
for sid in ORDER:
    for kind, keys, suffix in (("gaps", GAP_KEYS, "gaps"), ("assumptions", ASM_KEYS, "assumptions")):
        p = PARTS / f"{sid}-{suffix}.jsonl"
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            required = ["id", "title", "description", "type", "severity"] if kind == "gaps" else ["id", "text", "why"]
            miss = [k for k in required if not row.get(k)]
            if miss:
                raise SystemExit(f"{sid}: row {row.get('id')} missing {miss}")
            missing_all = [k for k in keys if k not in row]
            if missing_all:
                raise SystemExit(f"{sid}: row {row.get('id')} lacks keys {missing_all}")
            if row["id"] in seen:
                raise SystemExit(f"duplicate id {row['id']}")
            seen.add(row["id"])
            out[kind].append(row)

for kind in ("gaps", "assumptions"):
    target = W / kind / "B-S2-06.jsonl"
    target.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out[kind]), encoding="utf-8")
    print(kind, len(out[kind]), "->", target.relative_to(ROOT))
print("gap types:", sorted({r["type"] for r in out["gaps"]}))
print("severities:", sorted({r["severity"] for r in out["gaps"]}))
print("waves:", sorted({str(r["needed_by_wave"]) for r in out["gaps"]}))
print("legacy refs:", sorted({r["legacy_ref"] for r in out["gaps"]}))
print("confidence:", sorted({r["confidence"] for r in out["assumptions"]}))
