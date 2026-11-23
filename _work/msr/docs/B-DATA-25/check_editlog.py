import re
from pathlib import Path

t = Path("_work/msr/editlog/B-DATA-25.md").read_text(encoding="utf-8")
wp = Path("_work/msr/wp/B-DATA-25.md").read_text(encoding="utf-8")
blk = wp.split("Write only:", 1)[1].split("\nDo", 1)[0]
allowed = [l[2:].split(" (")[0].strip() for l in blk.splitlines() if l.startswith("- ")]
print("allowed:", allowed)
found = re.findall(r"(?m)^\s*[-*]\s+`?([^`\n]+?\.(?:md|json|jsonl|xlsx|docx|pptx|yaml|sql|svg|excalidraw))`?\s*$", t)
print("bullets found:", len(found))
for m in found:
    ok = any(m.replace("\\", "/").startswith(a.rstrip("/")) for a in allowed)
    print("OK" if ok else "OUT", m)
