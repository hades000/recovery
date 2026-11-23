"""C-BN1 scratch: list the tables named in each source section and their owners."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr"
data = json.loads((WORK / "docs" / "C-BN1" / "data.json").read_text(encoding="utf-8"))
tables = data["tables"]
src = (ROOT / "04 User stories" / "Recovery Workbench Build Notes Epic 1 v6.md").read_text(encoding="utf-8")
parts = re.split(r"(?m)^## ", src)[1:]
out = []
for p in parts:
    title = p.splitlines()[0].strip()
    key = title.split(" ")[0]
    toks = set(re.findall(r"`([a-z][a-z0-9_]+)`", p))
    named = sorted(t for t in toks if t in tables)
    owners = sorted({tables[t]["owner"] for t in named})
    out.append((key, title, named, owners))
for k, t, n, o in out:
    print(f"{k} | owners={o} | tables={[(x, tables[x]['owner']) for x in n]}")
