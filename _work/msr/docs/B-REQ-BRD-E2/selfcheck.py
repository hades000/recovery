import json, re
from pathlib import Path

W = Path("_work/msr")
md = Path("03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.md").read_text(encoding="utf-8")
ids = set()
for kind, req in (("gaps", {"id", "title", "description", "type", "severity"}),
                  ("assumptions", {"id", "text", "why"})):
    p = W / kind / "B-REQ-BRD-E2.jsonl"
    for line in p.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        miss = req - {k for k, v in r.items() if v not in (None, "")}
        ids.add(r["id"])
        print(kind, r["id"], "OK" if not miss else f"MISSING {miss}")
cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", md))
print("cited", sorted(cited))
print("uncited rows:", sorted(ids - cited))
print("dangling:", sorted(cited - ids))
print("jira:", bool(re.search(r"(?i)\bjira\b|atlassian\.net", md)))
print("emails:", re.findall(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", md))
print("BRD requirement rows:", len(re.findall(r"(?m)^\| RWB-E2-\d{3} \|", md)))
print("program rows:", len(re.findall(r"(?m)^\| REQ-[A-Z]+-\d{3} \|", md)))
print("tentative:", md.count("(tentative)"))
