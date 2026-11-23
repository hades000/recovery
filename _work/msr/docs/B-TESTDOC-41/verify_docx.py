"""Compare the rendered docx with the Markdown it came from."""
import re
import sys
from pathlib import Path

import docx

md = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
d = docx.Document(sys.argv[2])

heads = [(p.style.name, p.text) for p in d.paragraphs if p.style.name.startswith("Heading")]
bul = [p for p in d.paragraphs if p.style.name == "List Bullet"]
print("tables:", len(d.tables))
print("headings:", len(heads))
for s, t in heads:
    print("  ", s, "|", t)
print("bullets:", len(bul))

md_heads = [(len(m.group(1)), m.group(2).strip()) for m in
            (re.match(r"^(#{1,6})\s+(.*)$", l) for l in md) if m]
md_heads = [("#" * n, t) for n, t in md_heads]
print("md headings:", len(md_heads))
for n, t in md_heads:
    if n not in ("#", "##"):
        print("  ODD LEVEL", n, t)

body = "\n".join(p.text for p in d.paragraphs)
cells = "\n".join(c.text for t in d.tables for r in t.rows for c in r.cells)
alltext = body + "\n" + cells

# every non-table, non-heading md line must appear as a paragraph
missing = []
for l in md:
    s = l.strip()
    if not s or s.startswith("|") or s.startswith("#"):
        continue
    s2 = re.sub(r"^[-*]\s+", "", s).replace("**", "")
    if s2 not in body:
        missing.append(s2[:110])
print("paragraph lines missing from docx:", len(missing))
for m in missing[:10]:
    print("  -", m)

# table rows preserved
md_rows = [l for l in md if l.strip().startswith("|") and not re.match(r"^\|[-: |]+\|$", l.strip())]
print("md table rows:", len(md_rows), "| docx table rows:", sum(len(t.rows) for t in d.tables))
print("header ok:", body.startswith("SCB Collections and Recovery. Henka Group, 22 November 2026.")
      or d.paragraphs[0].text.startswith("SCB Collections and Recovery. Henka Group, 22 November 2026."))
print("first 3 paragraphs:", [p.text[:60] for p in d.paragraphs[:3]])
