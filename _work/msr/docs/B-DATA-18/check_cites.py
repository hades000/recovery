"""Manual C17-style citation check over the B-DATA-18 write set."""
import json
import re
from pathlib import Path

ids = set()
for kind in ("gaps", "assumptions"):
    for line in Path(f"_work/msr/{kind}/B-DATA-18.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(json.loads(line)["id"])

cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
files = [Path("_work/msr/docs/B-DATA-18/build_notes.md"), Path("_work/msr/editlog/B-DATA-18.md")]
for p in Path("_work/msr/docs/B-DATA-18").glob("*.json"):
    files.append(p)

bad = []
for p in files:
    text = p.read_text(encoding="utf-8", errors="replace")
    for c in sorted(set(cite.findall(text))):
        if c not in ids and not c.startswith(("D-", "DP-")):
            bad.append((p.name, c))
print("ids:", sorted(ids))
print("bad citations:", bad)
print("rows:", len(ids))
