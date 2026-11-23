import re
from pathlib import Path
p = Path("_work/msr/docs/B-DATA-21/verify_src.py")
s = p.read_text(encoding="utf-8")
s = s.replace('    if not s or set(s) <= set("-|: "):', '    if s.startswith("- "):\n        s = s[2:].strip()\n    if not s or set(s) <= set("-|: "):')
p.write_text(s, encoding="utf-8")
