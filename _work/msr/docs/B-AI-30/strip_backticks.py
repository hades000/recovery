"""Strip Markdown backticks from the scratch text (Word shows them literally)."""
from pathlib import Path

p = Path(r"_work/msr/docs/B-AI-30/Recovery Workbench Model Integration Design v3.md")
t = p.read_text(encoding="utf-8")
p.write_text(t.replace(chr(96), ""), encoding="utf-8", newline="\n")
print("backticks left:", p.read_text(encoding="utf-8").count(chr(96)))
