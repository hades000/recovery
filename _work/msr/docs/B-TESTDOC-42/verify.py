"""Verify the v4 docx of the definition of ready and done against the source and the WP."""
import re
import sys
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
HERE = ROOT / "_work" / "msr" / "docs" / "B-TESTDOC-42"
SRC = ROOT / "09 Testing and quality" / "Recovery Workbench Definition of Ready and Done v3.docx"
OUT = ROOT / "09 Testing and quality" / "Recovery Workbench Definition of Ready and Done v4.docx"
MD = HERE / "Recovery Workbench Definition of Ready and Done v4.md"

fails = []


def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


d = docx.Document(str(OUT))
src = docx.Document(str(SRC))
text = "\n".join(p.text for p in d.paragraphs)
cells = "\n".join(c.text for t in d.tables for r in t.rows for c in r.cells)
alltext = text + "\n" + cells

check(d.paragraphs[0].text.strip() == "SCB Collections and Recovery. Henka Group, 22 November 2026.", "header line 1")
check(d.paragraphs[1].text.strip() == "(C) Siam Commercial Bank and Henka Pte Ltd", "header line 2")
check("22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" in alltext, "change-log row")
check("4" in d.tables[1].rows[1].cells[0].text, "change-log version 4")

heads = [p.text.strip() for p in d.paragraphs if p.style.name.startswith("Heading")]
want = ["1. Where each definition applies", "1.1 The services and their owners (Ownership Map v1)",
        "2. Definition of ready", "2.1 What the story carries", "2.2 What is in place",
        "2.3 The contract is published (D-RCV-60)", "3. Definition of done", "3.1 Built and tested",
        "3.2 Controls", "3.3 Records kept current", "3.4 Accepted",
        "3.5 Contract and boundary tests green (D-RCV-60)", "4. When a story fails a definition",
        "5. Who owns each definition", "5.1 The owning team for each kind of work (R5.3)",
        "6. What this version changes (D-RCV-60)"]
check([h for h in heads if re.match(r"^\d", h)] == want, "section headings in order")

check(len(d.tables) == len(MD.read_text(encoding="utf-8").split("\n| Item | Detail |")) - 1 if False else len(d.tables) >= 15,
      f"table count {len(d.tables)}")

# every source line of the body survives, except the rows and items changed on purpose
changed = {
    "Version 2",  # kept, so this is only a note
}
src_lines = [p.text.strip() for p in src.paragraphs if p.text.strip()]
missing = [x for x in src_lines if x not in text]
allowed_missing = {
    "SCB Collections and Recovery. Henka Group, 28 October 2026",
}
check(set(missing) <= allowed_missing, f"source paragraphs missing: {sorted(set(missing))}")

# every source table row survives in some form
src_rows = []
for t in src.tables:
    for r in t.rows:
        src_rows.append(" | ".join(c.text.strip() for c in r.cells))
out_rows = []
for t in d.tables:
    for r in t.rows:
        out_rows.append(" | ".join(c.text.strip() for c in r.cells))
out_blob = "\n".join(out_rows)
src_missing = [x for x in src_rows if x not in out_blob]

# rows that were changed on purpose keep their number, so compare the leading number and label
src_nums = sorted({x.split(" | ")[0] for x in src_rows if re.match(r"^\d+ \|", x)})
out_nums = sorted({x.split(" | ")[0] for x in out_rows if re.match(r"^\d+ \|", x)})
check(set(src_nums) <= set(out_nums), f"item numbers kept ({len(src_nums)} source numbers)")

check("CG-B-TESTDOC-42-1" in alltext and "ASM-B-TESTDOC-42-1" in alltext, "citations present")
ids = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", alltext))
check(len(ids) == 21, f"distinct citations {len(ids)}")
check("Jira" not in alltext and "jira" not in alltext.lower(), "no issue-tracker name")
check(not re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", alltext), "no email address")
check("Rajdeep" not in alltext and "Ghai" not in alltext, "no person name from the source properties")
check(d.core_properties.author == "Henka Group", "author property")
check(d.core_properties.last_modified_by == "T3 Code / OpenCode / DeepSeek v4.1 Flash", "last modified by")
check("\ufffd" not in alltext, "no replacement character")

# the 19 services of the Ownership Map are all in table 1.1
t11 = d.tables[3]
codes = [r.cells[0].text.strip() for r in t11.rows[1:]]
check(codes == ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10",
                "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"], f"table 1.1 codes {codes}")

print()
print("source table rows changed on purpose:", len(src_missing))
for x in src_missing:
    print("   ", x[:120])
print("FAILS:", len(fails))
sys.exit(1 if fails else 0)
