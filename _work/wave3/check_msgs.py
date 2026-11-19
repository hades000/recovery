# -*- coding: utf-8 -*-
import io, os, re, collections

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
F = [os.path.join(BASE, r"04 User stories\Recovery Workbench Administration Stories v3.md"),
     os.path.join(BASE, r"04 User stories\Recovery Workbench Data Migration Stories v3.md")]

texts = collections.defaultdict(set)
removed = ["RWB-E1-003", "RWB-E1-004", "RWB-E1-005", "RWB-E1-006", "RWB-E1-009", "RWB-E1-010",
           "RWB-E1-012", "RWB-E1-051", "RWB-E2-023"]

for p in F:
    doc = io.open(p, encoding="ascii").read()
    for ln in doc.split("\n"):
        m = re.match(r"^\| (MSG-[\w-]+) \| [A-Za-z]+ \| (.*?) \|$", ln)
        if m:
            texts[m.group(1)].add(m.group(2))
    hits = [k for k in removed if k in doc]
    print(os.path.basename(p), "removed-story refs:", hits)
    feats = re.findall(r"(?m)^Feature: (.*)$", doc)
    titles = re.findall(r"(?m)^## RWB-\w+-\d+ (.*)$", doc)
    norm = lambda x: x.strip().lower()
    tn = {norm(t) for t in titles}
    odd = [f for f in feats if norm(f) not in tn]
    print("  features:", len(feats), "features not matching a title:", odd)

print("\nmessage texts with more than one wording:")
for k, v in sorted(texts.items()):
    if len(v) > 1:
        print(" ", k, v)
print("messages defined:", len(texts))
