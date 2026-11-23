"""Merge the B-PLT-TPL-01 probe row files into the WP gap and assumption registers."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
PROBE = WORK / "probe"
WP = "B-PLT-TPL-01"

GAP_KEYS = ["id", "title", "source", "section", "description", "evidence", "type", "area",
            "severity", "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"]
ASM_KEYS = ["id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"]


def load(pattern):
    rows = []
    for p in sorted(PROBE.glob(pattern)):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def merge(kind, pattern, keys, out_name):
    rows = load(pattern)
    by_id = {}
    problems = []
    for r in rows:
        aid = r.get("id", "")
        if not aid.startswith(f"{'CG' if kind == 'gaps' else 'ASM'}-{WP}-"):
            problems.append(f"{kind}: bad id {aid!r}")
        missing = [k for k in keys if k not in r]
        if missing:
            problems.append(f"{kind}: {aid} missing keys {missing}")
        if aid in by_id and by_id[aid] != r:
            problems.append(f"{kind}: duplicate id with different content {aid}")
        by_id[aid] = r
    ordered = [by_id[k] for k in sorted(by_id)]
    out = WORK / kind / out_name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in ordered) + ("\n" if ordered else ""),
                   encoding="utf-8")
    return ordered, problems


def main():
    gaps, gp = merge("gaps", "rows-B-PLT-TPL-01-*-gaps.jsonl", GAP_KEYS, f"{WP}.jsonl")
    asms, ap = merge("assumptions", "rows-B-PLT-TPL-01-*-asm.jsonl", ASM_KEYS, f"{WP}.jsonl")

    ids = {r["id"] for r in gaps} | {r["id"] for r in asms}
    for r in gaps:
        if r.get("asm") and r["asm"] not in ids:
            gp.append(f"gap {r['id']} points at missing assumption {r['asm']}")
    for r in asms:
        if r.get("gap") and r["gap"] not in ids:
            ap.append(f"assumption {r['id']} points at missing gap {r['gap']}")

    print(f"gaps={len(gaps)} assumptions={len(asms)}")
    for p in gp:
        print("GAP-PROBLEM", p)
    for p in ap:
        print("ASM-PROBLEM", p)
    if gp or ap:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
