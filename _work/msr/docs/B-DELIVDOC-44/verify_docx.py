"""Compare the rendered docx with the Markdown it was rendered from, and scan for names."""
import re
import subprocess
import sys
from pathlib import Path

import docx

OUT = Path("11 Delivery and operations/Recovery Workbench Engineering Practices v6.docx")
MD = Path("_work/msr/docs/B-DELIVDOC-44/Recovery Workbench Engineering Practices v6.md")
EX = Path("_work/msr/docs/B-DELIVDOC-44/verify")

subprocess.run([sys.executable, "-I", "22 Microservice Realignment/compat/convert_sources.py",
                str(OUT), str(EX)], check=True)

def norm(s):
    s = s.replace("**", "").replace("\u00a0", " ")
    s = re.sub(r"^\s*[-\u2022]\s+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

md_lines = [norm(l) for l in MD.read_text(encoding="utf-8").splitlines() if norm(l)]
got = [norm(l) for l in (EX / OUT.with_suffix(".md").name).read_text(encoding="utf-8").splitlines() if norm(l)]
missing = [l for l in md_lines if l not in got]
extra = [l for l in got if l not in md_lines]
print("md lines", len(md_lines), "docx lines", len(got), "missing", len(missing), "extra", len(extra))
for l in missing[:10]:
    print("MISS:", l[:140])
for l in extra[:10]:
    print("EXTRA:", l[:140])

d = docx.Document(OUT)
print("tables", len(d.tables), "paragraphs", len(d.paragraphs))
print("headings", [(p.style.name, p.text[:60]) for p in d.paragraphs if p.style.name.startswith("Heading")])

PAT = re.compile(r"K\.\s*(Book|Pipat|Tee)|Rajdeep|Ghai|@|jira|confluence|atlassian", re.I)
bad = [l for l in got if PAT.search(l)]
print("scan hits", len(bad))
for l in bad[:10]:
    print("HIT:", l[:160])
