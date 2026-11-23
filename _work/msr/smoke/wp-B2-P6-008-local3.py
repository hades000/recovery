import re
from pathlib import Path
t=Path("_work/msr/wp/B2-P6-008.md").read_text(encoding="utf-8",errors="replace")
blk=t.split("Write only:",1)[1].split("\nDo",1)[0]
allowed=[l[2:].split(" (")[0].strip() for l in blk.splitlines() if l.startswith("- ")]
log=Path("_work/msr/editlog/B2-P6-008.md").read_text(encoding="utf-8")
bullets=re.findall(r"(?m)^\s*[-*]\s+`?([^`\n]+?\.(?:md|json|jsonl|xlsx|docx|pptx|yaml|sql|svg|excalidraw))`?\s*$", log)
print("bullets:",len(bullets))
for b in bullets:
    ok=any(b.replace("\\","/").startswith(a.rstrip("/")) for a in allowed)
    print(("OK " if ok else "OUT"), b[:70])
print("tool line:", "T3 Code / OpenCode / DeepSeek v4.1 Flash" in log)
print("exists:", all(Path(x).exists() for x in allowed))
