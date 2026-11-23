from pathlib import Path
p = Path("_work/msr/editlog/B-DATA-21.md")
s = p.read_text(encoding="utf-8")
s = s.replace("- `_work/msr/docs/B-DATA-21/patch_verify.py`\n",
 "- `_work/msr/docs/B-DATA-21/patch_verify.py`\n- `_work/msr/docs/B-DATA-21/patch_md.py`\n- `_work/msr/docs/B-DATA-21/patch_log.py`\n- `_work/msr/docs/B-DATA-21/final_check.py`\n")
s = s.replace("157 paragraph and table-row blocks", "158 paragraph and table-row blocks")
p.write_text(s, encoding="utf-8")
print("ok")
