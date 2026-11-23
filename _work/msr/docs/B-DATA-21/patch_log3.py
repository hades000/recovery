from pathlib import Path
p = Path("_work/msr/editlog/B-DATA-21.md")
s = p.read_text(encoding="utf-8")
s = s.replace("- `_work/msr/docs/B-DATA-21/final_check.py`\n",
 "- `_work/msr/docs/B-DATA-21/final_check.py`\n- `_work/msr/docs/B-DATA-21/patch_log2.py`\n")
p.write_text(s, encoding="utf-8")
print("ok")
