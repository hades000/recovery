import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
for rel in sys.argv[1:]:
    p = ROOT / rel
    t = p.read_text(encoding="utf-8")
    print("#" * 100)
    print(p.name)
    # metadata table
    meta = t.split("## 1.", 1)[0]
    print(meta.strip()[:1800])
    for sec in ("7. Acceptance criteria", "16. Test cases"):
        m = re.search(rf"^## {re.escape(sec)}\s*$(.*?)(?=^## \d+\.|\Z)", t, re.M | re.S)
        print("\n-----", sec, "-----")
        print(m.group(1).strip() if m else "NOT FOUND")
