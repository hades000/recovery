import re
import sys
from pathlib import Path

sys.path.insert(0, "22 Microservice Realignment/checks")
sys.path.insert(0, "22 Microservice Realignment/compat")
import run_all as r

allowed = r._wp_writes("B-TECH-13")
t = Path("_work/msr/editlog/B-TECH-13.md").read_text(encoding="utf-8")
pat = r"(?m)^\s*[-*]\s+`?([^`\n]+?\.(?:md|json|jsonl|xlsx|docx|pptx|yaml|sql|svg|excalidraw))`?\s*$"
ms = re.findall(pat, t)
print("ALLOWED", allowed)
print("MATCHED", ms)
for m in ms:
    print(m, any(m.replace("\\", "/").startswith(a.rstrip("/")) for a in allowed))
print("C18", r.c18([Path("05 Technical architecture/Recovery Workbench Document Management Design v3.docx")], wp="B-TECH-13"))
