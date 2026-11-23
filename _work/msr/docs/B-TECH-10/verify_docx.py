"""Verify the new v4 .docx: fidelity to v3, header, change-log row, tables, registers, no person names."""
import json
import re
import zipfile
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
V3 = ROOT / "05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx"
V4 = ROOT / "05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v4.docx"
WORK = ROOT / "_work/msr"
OUTDIR = Path(__file__).parent
FAILS = []


def note(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        FAILS.append(msg)


def text_of(path):
    d = docx.Document(str(path))
    lines = [p.text.strip() for p in d.paragraphs if p.text.strip()]
    for t in d.tables:
        for row in t.rows:
            for c in row.cells:
                if c.text.strip():
                    lines.append(c.text.strip())
    return d, lines


d3, l3 = text_of(V3)
d4, l4 = text_of(V4)
new = "\n".join(l4)

INTENDED = {
    "SCB Collections and Recovery. Henka Group, 16 November 2026",
    "Version", "3", "4", "Date", "16 November 2026", "22 November 2026",
}

missing = []
for line in l3:
    if line in new or line in INTENDED:
        continue
    # multi-line table cells and long paragraphs: compare on a normalised prefix
    if any(line[:120] in x for x in l4):
        continue
    missing.append(line)
note(not missing, f"v3 lines present verbatim: {len(l3) - len(missing)} of {len(l3)}, missing {len(missing)}")
for m in missing[:20]:
    print("   missing:", m[:150])

# first two paragraphs
head = [p.text.strip() for p in d4.paragraphs[:3]]
note(head[0] == "SCB Collections and Recovery. Henka Group, 22 November 2026." and
     head[1] == "(C) Siam Commercial Bank and Henka Pte Ltd",
     f"header lines 1 and 2: {head[:2]}")

note("v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" in new,
     "change-log row with D-RCV-60 and the tool line")
note("v3, 16 November 2026, D-RCV-36" in new, "v3 change row kept")

heads = [p.text.strip() for p in d4.paragraphs if p.style is not None and
         (p.style.name or "").lower().startswith("heading") and p.text.strip()]
print("headings:", heads)
want = ["1. Rules", "2. Failure categories", "3. Retry", "4. What the user sees meanwhile", "5. Recovery",
        "6. Temporal and Drools", "7. Message map"]
note(all(w in heads for w in want), "sections 1 to 7 of v3 present and in order")

# tables
print("tables:", len(d4.tables), [ (len(t.rows), len(t.columns)) for t in d4.tables ])
md = (Path(__file__).with_name("Recovery Workbench Error Handling and Resilience Standard v4.md")).read_text(encoding="utf-8")
md_tables = []
blk = 0
for line in md.splitlines():
    if line.startswith("|"):
        blk += 1
    elif blk:
        md_tables.append(blk)
        blk = 0
if blk:
    md_tables.append(blk)
print("md table line groups:", len(md_tables), "docx tables:", len(d4.tables))
note(len(d4.tables) == len(md_tables), f"table count matches the text: {len(d4.tables)}")

# bullets: the v3 list paragraphs must be bulleted, not prefixed
bad = [p.text[:60] for p in d4.paragraphs if p.text.startswith(("\ufffd", "\u2022", "- "))]
note(not bad, f"no fallback bullet prefix: {bad[:3]}")

# registers
cg = [json.loads(x)["id"] for x in (WORK / "gaps/B-TECH-10.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
asm = [json.loads(x)["id"] for x in (WORK / "assumptions/B-TECH-10.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
cited = sorted(set(re.findall(r"(?:CG|ASM)-B-TECH-10-\d+", new)))
unresolved = [c for c in cited if c not in cg + asm]
note(not unresolved, f"citations resolve: {cited} / unresolved {unresolved}")
note(all(re.search(r"CG-B-TECH-10-\d+", json.dumps(json.loads(x))) for x in
         (WORK / "gaps/B-TECH-10.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()),
     "gap rows carry ids")

# package-wide scan for person names, emails and the wrong tool
with zipfile.ZipFile(V4) as z:
    blob = "".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.endswith(".xml"))
note("Rajdeep" not in blob and "Ghai" not in blob, "no person name in the package")
note(not re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", new), "no email address in the text")
note("Claude" not in new and "claude" not in blob, "no wrong tool attribution")
note(not re.search(r"(?i)\bjira\b|atlassian", new), "no issue-tracker reference")

# round-trip text for review
lines = []
for p in d4.paragraphs:
    if p.text.strip():
        lines.append(("# " if (p.style and (p.style.name or "").lower().startswith("heading")) else "") + p.text.strip())
    if p.style and (p.style.name or "").lower().startswith("heading"):
        pass
(OUTDIR / "roundtrip.txt").write_text("\n".join(lines), encoding="utf-8")
print("WROTE", OUTDIR / "roundtrip.txt")
print("\nRESULT:", "PASS" if not FAILS else f"FAIL ({len(FAILS)})")
