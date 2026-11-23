"""Scratch: confirm C18 parses the B-S2-06 editlog bullets and they are all allowed."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
import run_all as R

txt = (ROOT / "_work/msr/editlog/B-S2-06.md").read_text(encoding="utf-8")
found = re.findall(r"(?m)^\s*[-*]\s+`?([^`\n]+?\.(?:md|json|jsonl|xlsx|docx|pptx|yaml|sql|svg|excalidraw))`?\s*$", txt)
allow = R._wp_writes("B-S2-06")
print("bullets parsed:", len(found))
for f in found:
    print(" ", f, "| allowed:", any(f.replace("\\", "/").startswith(a.rstrip("/")) for a in allow))
print("C18:", R.c18(None, wp="B-S2-06"))
