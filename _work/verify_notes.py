import re, os
ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
p = os.path.join(ROOT, "04 User stories", "Recovery Workbench Build Notes Epic 1 v5.md")
t = open(p, encoding="ascii").read()
blocks = [b for b in re.split(r"(?m)^(?=## )", t) if b.startswith("## RWB-")]
print("STORY SECTIONS", len(blocks))
bad = []
for b in blocks:
    key = re.match(r"## (RWB-\S+)", b).group(1)
    for note in ("**View.**", "**Grant.**", "**Freshness.**", "**Boundary.**"):
        if b.count(note) != 1:
            bad.append((key, note, b.count(note)))
    if "Module:" not in b:
        bad.append((key, "module", 0))
print("BAD", bad)
for pat in ["expects As", "expected As", "  ", "None.", "including ;"]:
    n = t.count(pat)
    if n: print("PATTERN", repr(pat), n)
print("ASCII", all(ord(c) < 128 for c in t), "lines", t.count("\n"))
print("WORDS", len(t.split()))
# check every story key in v8 present
md = open(os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.md"), encoding="ascii").read()
keys = re.findall(r"(?m)^## (RWB-\S+)", md)
bkeys = [re.match(r"## (RWB-\S+)", b).group(1) for b in blocks]
print("MISSING", [k for k in keys if k not in bkeys])
print("EXTRA", [k for k in bkeys if k not in keys])
print("ORDER OK", keys == bkeys)
