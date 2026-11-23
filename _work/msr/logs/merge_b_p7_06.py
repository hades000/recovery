"""B-P7-06: merge the five per-key scratch gap and assumption rows into the WP files.

Reads   _work/msr/logs/B-P7-06-<KEY>.{gaps,assumptions}.jsonl
Writes  _work/msr/gaps/B-P7-06.jsonl
        _work/msr/assumptions/B-P7-06.jsonl
Run: python -I "_work/msr/logs/merge_b_p7_06.py"
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
KEYS = ["E1018", "E1020", "E1021", "E1028", "E1030"]
GAP_KEYS = ["id", "title", "source", "section", "description", "evidence", "type", "area",
            "severity", "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"]
ASM_KEYS = ["id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"]
GAP_TYPES = {"Missing", "Conflict", "Ambiguous", "Outdated", "ID collision"}
SEV = {"P1", "P2", "P3"}
CONF = {"High", "Medium", "Low"}


def load(path):
    rows = []
    if not path.exists():
        print(f"WARN missing {path.relative_to(ROOT)}")
        return rows
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            sys.exit(f"FAIL {path.name}:{n} is not JSON: {exc}")
    return rows


def check(rows, keys, kind):
    seen = set()
    for r in rows:
        miss = [k for k in keys if k not in r]
        if miss:
            sys.exit(f"FAIL {kind} {r.get('id')} missing {miss}")
        if r["id"] in seen:
            sys.exit(f"FAIL duplicate {kind} id {r['id']}")
        seen.add(r["id"])
        if not re.match(r"^(CG|ASM)-B-P7-06-(E1018|E1020|E1021|E1028|E1030)-\d+$", r["id"]):
            sys.exit(f"FAIL bad {kind} id {r['id']}")
    if kind == "gap":
        for r in rows:
            if r["type"] not in GAP_TYPES:
                sys.exit(f"FAIL {r['id']} type {r['type']}")
            if r["severity"] not in SEV:
                sys.exit(f"FAIL {r['id']} severity {r['severity']}")
    else:
        for r in rows:
            if r["confidence"] not in CONF:
                sys.exit(f"FAIL {r['id']} confidence {r['confidence']}")
    return rows


def order(rows):
    key_of = lambda r: [k for k in KEYS if f"-{k}-" in r["id"]][0]
    return sorted(rows, key=lambda r: (KEYS.index(key_of(r)), int(r["id"].rsplit("-", 1)[1])))


def main():
    gaps = []
    asms = []
    for k in KEYS:
        gaps += load(WORK / "logs" / f"B-P7-06-{k}.gaps.jsonl")
        asms += load(WORK / "logs" / f"B-P7-06-{k}.assumptions.jsonl")
    gaps = order(check(gaps, GAP_KEYS, "gap"))
    asms = order(check(asms, ASM_KEYS, "asm"))

    gap_ids = {g["id"] for g in gaps}
    for a in asms:
        if a["gap"] and a["gap"] not in gap_ids:
            print(f"WARN {a['id']} cites a gap with no row: {a['gap']}")
    for g in gaps:
        if g["asm"] and g["asm"] not in {a["id"] for a in asms}:
            print(f"WARN {g['id']} cites an assumption with no row: {g['asm']}")

    (WORK / "gaps" / "B-P7-06.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=True) + "\n" for r in gaps), encoding="utf-8")
    (WORK / "assumptions" / "B-P7-06.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=True) + "\n" for r in asms), encoding="utf-8")
    print(f"gaps {len(gaps)}  assumptions {len(asms)}")
    for k in KEYS:
        print(k, "gaps", sum(1 for r in gaps if f"-{k}-" in r["id"]),
              "asms", sum(1 for r in asms if f"-{k}-" in r["id"]))


if __name__ == "__main__":
    main()
