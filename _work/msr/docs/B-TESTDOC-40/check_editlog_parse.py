"""Reproduce the C18 edit-log parse so a silent regex mismatch cannot pass for compliance."""
import re
from pathlib import Path

log = Path(r"_work/msr/editlog/B-TESTDOC-40.md").read_text(encoding="utf-8")
rx = re.compile(r"(?m)^\s*[-*]\s+`?([^`\n]+?\.(?:md|json|jsonl|xlsx|docx|pptx|yaml|sql|svg|excalidraw))`?\s*$")
found = rx.findall(log)
print("lines found:", len(found))
for f in found:
    print("  ", f)
