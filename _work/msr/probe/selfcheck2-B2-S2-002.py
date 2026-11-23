import re
from pathlib import Path
wp=Path("_work/msr/wp/B2-S2-002.md").read_text(encoding="utf-8")
blk=wp.split("Write only:",1)[1].split("\nDo",1)[0]
allowed=[l[2:].split(" (")[0].strip() for l in blk.splitlines() if l.startswith("- ")]
print("allowed:"); [print("  ",a) for a in allowed]
log=Path("_work/msr/editlog/B2-S2-002.md").read_text(encoding="utf-8")
bad=[]
for m in re.findall(r"(?m)^\s*[-*]\s+`?([^`\n]+?\.(?:md|json|jsonl|xlsx|docx|pptx|yaml|sql|svg|excalidraw))`?\s*$",log):
    if not any(m.replace("\\","/").startswith(a.rstrip("/")) for a in allowed): bad.append(m)
print("C18 out-of-scope bullets:",bad)
print("C20 tool line:", "T3 Code / OpenCode / DeepSeek v4.1 Flash" in log)
print("wrong attribution:", bool(re.search(r"Co-Authored-By: Claude|Generated with \[Claude Code\]",log)))
