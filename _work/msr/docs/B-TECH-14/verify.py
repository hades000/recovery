"""Verify the v3 notification and correspondence design against the source and the registers."""
import json
import re
import sys
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "05 Technical architecture" / "Recovery Workbench Notification and Correspondence Design v2.docx"
OUT = ROOT / "05 Technical architecture" / "Recovery Workbench Notification and Correspondence Design v3.docx"
MD = ROOT / "_work" / "msr" / "docs" / "B-TECH-14" / "Recovery Workbench Notification and Correspondence Design v3.md"
WP = "B-TECH-14"

INTENDED = {
    "SCB Collections and Recovery. Henka Group, 28 October 2026",
    "Version | 1",
    "Date | 28 October 2026",
}
CHANGED_CELLS = {"1", "28 October 2026"}

fails, notes = [], []


def body_lines(p):
    d = docx.Document(str(p))
    out = [x.text.strip() for x in d.paragraphs if x.text.strip()]
    for t in d.tables:
        for row in t.rows:
            cells = [c.text.strip() for c in row.cells]
            out.append(" | ".join(cells))
            out.extend(c for c in cells if c)
    return out


src, dst = body_lines(SRC), body_lines(OUT)
dst_set = set(dst)
src_set = set(src)
missing = [x for x in src_set - dst_set if x not in INTENDED]

md = MD.read_text(encoding="utf-8")
lines = md.splitlines()
if lines[0] != "SCB Collections and Recovery. Henka Group, 22 November 2026." or lines[1] != "(C) Siam Commercial Bank and Henka Pte Ltd":
    fails.append("header lines 1 and 2 are not the R8.1 header")
if "D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" not in md:
    fails.append("change-log row with D-RCV-60 and the tool line is missing")

ids = set()
for kind in ("gaps", "assumptions"):
    for line in (ROOT / "_work" / "msr" / kind / f"{WP}.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(json.loads(line)["id"])
cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", md))
unresolved = sorted(c for c in cited if c not in ids)

order = [h for h in re.findall(r"(?m)^# (.+)$", md)]
expected_sections = ["1. What is sent", "2. How a notice is produced", "3. Templates", "4. Contact rules",
                     "5. Volumes", "6. Open decisions", "7. Owners and contracts", "8. Decisions",
                     "9. Realignment changes in version 3 (D-RCV-60)"]
if order[1:] != expected_sections:
    fails.append(f"section order: {order}")

if "\ufffd" in md:
    fails.append("replacement character in the markdown")

print("SOURCE unique non-empty lines:", len(src_set))
print("INTENDED changes:", len(missing), "unexplained missing:", [x for x in missing if x not in INTENDED])
for m in missing:
    if m not in INTENDED:
        fails.append(f"source line not found and not intended: {m}")
print("CITED ids:", len(cited), "unresolved:", unresolved)
for u in unresolved:
    fails.append(f"unresolved citation {u}")
print("TABLES in v3 docx:", len(docx.Document(str(OUT)).tables))
print("SECTIONS:", order[1:])
print("PROPS:", docx.Document(str(OUT)).core_properties.author, "|",
      docx.Document(str(OUT)).core_properties.last_modified_by)
print("RESULT:", "PASS" if not fails else "FAIL")
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
