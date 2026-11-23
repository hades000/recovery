"""Verify the v3 docx against the v2 source text (scratch check, reads only).

Checks
1. Header lines of Template and Rules §R8.1 are the first two paragraphs.
2. The D-RCV-60 change-log row with the tool line is present.
3. Every non-empty line of the v2 source text is present in the round-trip extract of v3,
   except the lines listed as intended changes.
4. No source bullet was rendered twice (the md-docx bullet fallback duplicates a bullet).
5. Sections 1 to 6 are present in order, with the subsections.
6. Every CG-/ASM- citation in the document resolves to a row of the two jsonl files.
7. Table count and core properties.
"""
import json
import re
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr"
NAME = "Recovery Workbench Availability Performance and Recovery Design"
SRC = WORK / "extract" / "B-TECH-11" / f"{NAME} v2.md"
RT = WORK / "docs" / "B-TECH-11" / "roundtrip" / f"{NAME} v3.md"
OUT = ROOT / "05 Technical architecture" / f"{NAME} v3.docx"

# Lines of the source that version 3 changes on purpose, with the reason.
CHANGED = {
    "SCB Collections and Recovery. Henka Group, 28 October 2026": "issue date of version 3",
    "| Version | 1 |": "version 3",
    "| Date | 28 October 2026 |": "issue date of version 3",
    "- The ACE service scales out on the shared AKS clusters by CPU and request rate; the recovery module adds no separate service.":
        "19 services, each with an API and a worker deployment (ADR-013, ADR-016)",
    "- PostgreSQL flexible server, zone redundant; read queries for reports go to the data lake copy, not the live database.":
        "no data lake; reports read the rwb-reporting read model (ADR-018, DP-17)",
}

fails = []


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


src_lines = [norm(l) for l in SRC.read_text(encoding="utf-8").splitlines() if norm(l)]
rt_text = RT.read_text(encoding="utf-8")
rt_lines = [norm(l) for l in rt_text.splitlines() if norm(l)]
rt_set = set(rt_lines)
rt_blob = norm(rt_text)

# 1. header
head = [l for l in RT.read_text(encoding="utf-8").splitlines() if l.strip()][:2]
if head[0] != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    fails.append(f"header line 1 is {head[0]!r}")
if head[1] != "(C) Siam Commercial Bank and Henka Pte Ltd":
    fails.append(f"header line 2 is {head[1]!r}")

# 2. change log row
row = "3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
if row not in rt_blob:
    fails.append("change-log row with D-RCV-60 and the tool line is missing")

# 3. fidelity
missing = []
for line in src_lines:
    if line in CHANGED:
        continue
    if line not in rt_set:
        missing.append(line)
if missing:
    fails.extend(f"source line not found: {m[:110]}" for m in missing)

# 4. no duplicated bullets
for line in src_lines:
    if line.startswith("- ") and rt_lines.count(line) > 1:
        fails.append(f"bullet rendered {rt_lines.count(line)} times: {line[:80]}")
if "\ufffd" in rt_text or "• " in rt_text:
    fails.append("bullet fallback artefact present in the round trip")

# 5. sections and subsections
d = docx.Document(str(OUT))
heads = [p.text.strip() for p in d.paragraphs if p.style.name.lower().startswith("heading")]
want = ["1. Service levels", "2. Load the design carries", "3. Scaling", "4. Backup and restore",
        "5. Degraded modes", "6. Tests"]
got = [h for h in heads if re.match(r"^\d+\. ", h)]
if got != want:
    fails.append(f"top sections are {got}")
subs = [h for h in heads if re.match(r"^\d+\.\d+ ", h)]
if len(subs) != 12:
    fails.append(f"expected 12 subsections, found {len(subs)}: {subs}")

# 6. citations resolve
ids = set()
for kind in ("gaps", "assumptions"):
    for p in sorted((WORK / kind).glob("*.jsonl")):
        for ln in p.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                ids.add(json.loads(ln)["id"])
cite = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", rt_text))
bad = sorted(c for c in cite if c not in ids)
if bad:
    fails.append(f"citations with no jsonl row: {bad}")
unused_gaps = sorted(i for i in ids if i.startswith("CG-B-TECH-11") and i not in cite)

# 7. tables and properties
if len(d.tables) < 15:
    fails.append(f"only {len(d.tables)} tables")
cp = d.core_properties
if cp.author != "Henka Group" or "DeepSeek" not in (cp.last_modified_by or ""):
    fails.append(f"core properties are {cp.author!r} / {cp.last_modified_by!r}")
src_hash = None

print("RESULT", "PASS" if not fails else "FAIL")
print("source lines", len(src_lines), "changed on purpose", len(CHANGED), "missing", len(missing))
print("sections", got)
print("subsections", subs)
print("tables", len(d.tables), "paragraphs", len(d.paragraphs))
print("citations", len(cite), "gap rows cited", len([c for c in cite if c.startswith("CG-")]))
print("gap rows not cited in the document", unused_gaps)
print("core", cp.author, "|", cp.last_modified_by, "|", cp.title, "|", cp.modified, "|", cp.revision)
for f in fails:
    print(" -", f)
raise SystemExit(1 if fails else 0)
