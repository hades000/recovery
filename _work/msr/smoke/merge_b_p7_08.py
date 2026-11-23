"""Merge the per-key register rows of WP B-P7-08 into the two WP registers.

Reads _work/msr/{gaps,assumptions}/B-P7-08-<key>.part.jsonl in key order and
writes _work/msr/{gaps,assumptions}/B-P7-08.jsonl. Validates every line, id
uniqueness, the prefix, the required R9 keys and the asm/gap cross-reference.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
KEYS = ["E1073", "E2001", "E2002", "E2004", "E2006"]
GAP_KEYS = ["id", "title", "source", "section", "description", "evidence", "type",
            "area", "severity", "needed_by_wave", "legacy_ref", "owner_role", "asm",
            "proposed", "wp"]
ASM_KEYS = ["id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm",
            "impact", "wp"]
TYPES = {"Missing", "Conflict", "Ambiguous", "Outdated", "ID collision"}
SEV = {"P1", "P2", "P3"}
CONF = {"High", "Medium", "Low"}


def load(kind):
    rows = []
    for key in KEYS:
        p = WORK / kind / f"B-P7-08-{key}.part.jsonl"
        for n, line in enumerate(p.read_text(encoding="utf-8-sig").splitlines(), 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError as e:
                sys.exit(f"{p.name}:{n}: bad JSON: {e}")
            rows.append(r)
    return rows


def main():
    gaps = load("gaps")
    asms = load("assumptions")
    problems = []

    for r in gaps:
        miss = [k for k in GAP_KEYS if k not in r]
        if miss:
            problems.append(f"{r.get('id')}: gap missing keys {miss}")
        if r.get("type") not in TYPES:
            problems.append(f"{r.get('id')}: gap type {r.get('type')!r}")
        if r.get("severity") not in SEV:
            problems.append(f"{r.get('id')}: gap severity {r.get('severity')!r}")
        if r.get("wp") != "B-P7-08":
            problems.append(f"{r.get('id')}: gap wp {r.get('wp')!r}")
        for k, v in r.items():
            if v in (None, ""):
                problems.append(f"{r.get('id')}: gap empty value in {k}")
    for r in asms:
        miss = [k for k in ASM_KEYS if k not in r]
        if miss:
            problems.append(f"{r.get('id')}: asm missing keys {miss}")
        if r.get("confidence") not in CONF:
            problems.append(f"{r.get('id')}: asm confidence {r.get('confidence')!r}")
        if r.get("wp") != "B-P7-08":
            problems.append(f"{r.get('id')}: asm wp {r.get('wp')!r}")
        for k, v in r.items():
            if v in (None, ""):
                problems.append(f"{r.get('id')}: asm empty value in {k}")

    gid = [r["id"] for r in gaps]
    aid = [r["id"] for r in asms]
    for i in gid + aid:
        if not i.startswith(("CG-B-P7-08-", "ASM-B-P7-08-")):
            problems.append(f"id prefix: {i}")
    for name, seq in (("gap", gid), ("asm", aid)):
        dup = {i for i in seq if seq.count(i) > 1}
        if dup:
            problems.append(f"duplicate {name} ids: {sorted(dup)}")
    gs, aset = set(gid), set(aid)
    for r in gaps:
        if r["asm"] not in aset:
            problems.append(f"{r['id']}: asm {r['asm']} not found")
    for r in asms:
        if r["gap"] not in gs:
            problems.append(f"{r['id']}: gap {r['gap']} not found")

    if problems:
        for p in problems:
            print("FAIL", p)
        sys.exit(1)

    for kind, rows in (("gaps", gaps), ("assumptions", asms)):
        out = WORK / kind / "B-P7-08.jsonl"
        text = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n"
        out.write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {out.relative_to(ROOT)} rows={len(rows)}")

    import re
    rx = re.compile(r"^(?:CG|ASM)-B-P7-08-([A-Z0-9]+)-\d+$")
    per = {}
    for r in gaps:
        per.setdefault(rx.match(r["id"]).group(1), [0, 0])[0] += 1
    for r in asms:
        per.setdefault(rx.match(r["id"]).group(1), [0, 0])[1] += 1
    for k in sorted(per):
        print(f"  {k}: CG={per[k][0]} ASM={per[k][1]}")
    print(f"total CG={len(gaps)} ASM={len(asms)}")


if __name__ == "__main__":
    main()
