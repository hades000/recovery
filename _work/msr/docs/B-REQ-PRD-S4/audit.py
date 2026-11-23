import json, re, io, glob, os

ids = set()
for kind in ("gaps", "assumptions"):
    for p in glob.glob("_work/msr/%s/*.jsonl" % kind):
        for line in io.open(p, encoding="utf-8"):
            line = line.strip()
            if line:
                ids.add(json.loads(line)["id"])

prd = "03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md"
t = io.open(prd, encoding="utf-8").read()
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
missing = sorted({c for c in cite.findall(t) if c not in ids})
print("missing citations:", missing)

# counts
print("CG rows:", len([i for i in ids if i.startswith("CG-B-REQ-PRD-S4-")]))
print("ASM rows:", len([i for i in ids if i.startswith("ASM-B-REQ-PRD-S4-")]))

for fam in ("CAP-S4-", "FR-S4-", "NFR-S4-", "AC-S4-", "JRN-S4-", "ROL-S4-", "OQ-S4-"):
    found = sorted(set(re.findall(r"\b" + fam + r"\d{3}\b|\b" + fam + r"\d{2}\b", t)))
    print(fam, len(found), found[0] if found else "", found[-1] if found else "")
