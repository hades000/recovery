import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = "03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md"
t = open(p, encoding="utf-8").read()
print("bytes", len(t.encode("utf-8")), "lines", t.count("\n"))
for fam in ["CAP-P9-", "FR-P9-", "NFR-P9-", "AC-P9-", "ROL-P9-", "JRN-P9-", "OQ-P9-"]:
    ids = sorted(set(re.findall(fam + r"\d{3}|\d{2}", t)))
    print(fam, len(ids), ids[:2], ids[-2:])
cg = sorted({int(x) for x in re.findall(r"CG-B-REQ-PRD-P9-(\d+)", t)})
am = sorted({int(x) for x in re.findall(r"ASM-B-REQ-PRD-P9-(\d+)", t)})
print("CG cited", cg)
print("ASM cited", am)
print("tentative", t.count("(tentative)"))
print("first line:", t.split("\n")[0])
print("second line:", t.split("\n")[1])
print("D-RCV-60 rows:", t.count("D-RCV-60"))
