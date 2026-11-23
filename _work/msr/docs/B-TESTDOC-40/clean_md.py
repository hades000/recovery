"""Clean the scratch markdown for Word: literal bullets instead of "- " lines and no backticks.

compat/office_write.py md-docx looks the "List Bullet" style up by name; the source template has
no such style, so a "- " line produces the paragraph twice. A literal bullet character keeps one
paragraph. Backticks are markdown syntax and are removed for the Word page.
"""
from pathlib import Path

P = Path(r"_work/msr/docs/B-TESTDOC-40/Recovery Workbench Non Functional Test Plan v3.md")
t = P.read_text(encoding="utf-8")
lines = []
for line in t.splitlines():
    if line.startswith("- "):
        line = "\u2022 " + line[2:]
    lines.append(line.replace("`", ""))
out = "\n".join(lines) + "\n"
P.write_text(out, encoding="utf-8")
print("CLEANED", P, "bullet lines", sum(1 for l in lines if l.startswith("\u2022 ")),
      "backticks left", out.count("`"))
