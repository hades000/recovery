"""Round-trip check: every line of the built markdown must be in the built .docx."""
import re, sys
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[4]
MD = ROOT / "_work/msr/docs/B-TECH-07/Recovery Workbench Rules Engine Design v4.md"
DX = ROOT / "05 Technical architecture/Recovery Workbench Rules Engine Design v4.docx"

d = docx.Document(DX)
parts = [p.text for p in d.paragraphs]
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            parts.append(c.text)
doc_text = "\n".join(parts)
norm = lambda s: re.sub(r"\s+", " ", s).strip()
flat = norm(doc_text)

fails, n = [], 0
for line in MD.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line:
        continue
    if line.startswith("|"):
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip("|"))]
        for c in cells:
            if not c or set(c) <= set("-: "):
                continue
            n += 1
            if norm(c) not in flat:
                fails.append(f"table cell missing: {c[:70]}")
    else:
        line = re.sub(r"^#{1,6}\s+", "", line)
        line = re.sub(r"^[-*]\s+", "", line)
        n += 1
        if norm(line) not in flat:
            fails.append(f"line missing: {line[:70]}")

print("PASS" if not fails else "FAIL", f"({n} fragments checked)")
for f in fails[:40]:
    print(" -", f)
sys.exit(1 if fails else 0)
