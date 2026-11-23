import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr"
v6 = (ROOT / "04 User stories" / "Recovery Workbench Build Notes Epic 1 v6.md").read_text(encoding="utf-8")
v7 = (ROOT / "04 User stories" / "Recovery Workbench Build Notes Epic 1 v7.md").read_text(encoding="utf-8")

s6 = re.split(r"(?m)^(?=## RWB-)", v6)[1:]
s7 = re.split(r"(?m)^(?=## RWB-)", v7)[1:]
print("sections", len(s6), len(s7))

bad = 0
for a, b in zip(s6, s7):
    ka = re.match(r"## (\S+)", a).group(1)
    kb = re.match(r"## (\S+)", b).group(1)
    # strip the trailing block (starts at **Service and lane.)
    body = b[:b.index("**Service and lane.")].rstrip("\n")
    if a.rstrip("\n") != body:
        bad += 1
        print("DIFF", ka, kb)
print("sections differing from v6:", bad)

print("mojibake:", v7.count("\ufffd"))
print("sections sign:", v7.count("§"))
cites = set(re.findall(r"\b(?:CG|ASM)-BN1-\d+\b", v7))
ids = set()
for kind in ("gaps", "assumptions"):
    for p in (WORK / kind).glob("*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                ids.add(json.loads(line)["id"])
print("cites missing:", sorted(c for c in cites if c not in ids))
print("cites:", sorted(cites))
print("rows:", len([i for i in ids if i.startswith("CG-BN1")]), len([i for i in ids if i.startswith("ASM-BN1")]))
# table pipe sanity for the front matter
for i, line in enumerate(v7.splitlines()[:230], 1):
    if line.startswith("|") and line.count("|") < 3:
        print("bad row", i, line)
print("placeholders:", v7.count("Not specified in the source documents"))
