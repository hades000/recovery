import re
from pathlib import Path

p = Path(r"_work/msr/docs/B-TECH-10/Recovery Workbench Error Handling and Resilience Standard v4.md")
t = p.read_text(encoding="utf-8")
bt = chr(96)
print("backticks:", t.count(bt), "stars:", t.count("**"))
print(sorted(set(re.findall(bt + "[^" + bt + "]+" + bt, t))))
