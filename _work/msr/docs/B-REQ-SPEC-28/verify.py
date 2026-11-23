"""Check that version 4 keeps every source section, requirement, number and date of version 3.

For every source line the script proves one of:
- the line reappears verbatim (paragraphs, headings, bullets), or
- for a table row, a version 4 row exists whose leading cells are the source cells, character for
  character (the owning service cell may be appended), or
- the line is one of the declared changed lines (the document control table, and the title lines that
  become headings).
It also checks the requirement IDs (78 kept, 2 added), the header lines, the change-log row and that every
cited CG/ASM id exists in the two jsonl files.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "_work/msr/extract/Recovery Workbench Non Functional Specification v3.md"
OUT = ROOT / "_work/msr/docs/B-REQ-SPEC-28/Recovery Workbench Non Functional Specification v4.md"
GAPS = ROOT / "_work/msr/gaps/B-REQ-SPEC-28.jsonl"
ASMS = ROOT / "_work/msr/assumptions/B-REQ-SPEC-28.jsonl"

CHANGED = {
    "Version | 3",
    "Requirements | 78",
    "Recovery Workbench",
    "Non-functional specification",
}


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    src = SRC.read_text(encoding="utf-8").splitlines()
    out = OUT.read_text(encoding="utf-8").splitlines()
    out_set = set(out)
    out_rows = [cells(l) for l in out if l.startswith("|")]

    fails, changed = [], []
    in_control = False
    for line in src:
        if line.strip() == "| Item | Detail |":
            in_control = True
            continue
        if in_control:
            if not line.strip():
                in_control = False
            continue
        if not line.strip():
            continue
        if line.startswith("|"):
            cs = cells(line)
            if all(set(c) <= set("-: ") for c in cs):
                continue
            if not any(r[: len(cs)] == cs for r in out_rows):
                fails.append(f"table row not preserved: {line[:90]}")
            continue
        if line in out_set:
            continue
        key = next((k for k in CHANGED if line.strip().endswith(k.split(" | ")[-1]) and k in line), None)
        if key:
            changed.append(line)
            continue
        fails.append(f"line not preserved: {line[:90]}")

    # header and change log
    if out[0] != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
        fails.append("header line 1 wrong")
    if out[1] != "(C) Siam Commercial Bank and Henka Pte Ltd":
        fails.append("header line 2 wrong")
    if not any("D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" in l and l.startswith("| 4 |")
               for l in out):
        fails.append("change-log row missing")

    # requirement ids
    src_ids = [m for l in src for m in re.findall(r"\| (NFR-\d{3}) \|", l)]
    out_ids = [m for l in out for m in re.findall(r"\| (NFR-\d{3}) \|", l)]
    missing = [i for i in set(src_ids) if i not in out_ids]
    if missing:
        fails.append(f"requirements lost: {sorted(missing)}")
    if len(set(src_ids)) != 78:
        fails.append(f"source requirement count is {len(set(src_ids))}, expected 78")
    if len(set(out_ids)) != 80:
        fails.append(f"output requirement count is {len(set(out_ids))}, expected 80")
    for must in ("2 seconds per REST call", "one hop", "2 s call timeout"):
        if must not in OUT.read_text(encoding="utf-8"):
            fails.append(f"2 s / one hop wording missing: {must}")

    # citations resolve
    ids = set()
    for p in (GAPS, ASMS):
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    ids.add(json.loads(line)["id"])
    cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", OUT.read_text(encoding="utf-8")))
    for c in sorted(cited - ids):
        fails.append(f"cited id with no jsonl row: {c}")

    print("source requirements:", len(set(src_ids)), "output requirements:", len(set(out_ids)))
    print("changed source lines:", changed)
    print("rows in output:", len(out_rows), "citations:", len(cited))
    if fails:
        print("FAIL", len(fails))
        for f in fails:
            print(" -", f)
        return 1
    print("OK: every source section, requirement, number and date is preserved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
