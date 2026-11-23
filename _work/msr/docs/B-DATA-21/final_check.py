import docx, json, re
from pathlib import Path
d = docx.Document("06 Data/Recovery Workbench Data Migration Approach v4.docx")
ps = [p.text for p in d.paragraphs if p.text.strip()]
print("P1:", ps[0]); print("P2:", ps[1])
print("CHANGELOG:", any("D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" in x for x in ps))
txt = "\n".join(ps) + "\n" + "\n".join(c.text for t in d.tables for r in t.rows for c in r.cells)
print("TABLES:", len(d.tables))
print("SECTIONS:", [x for x in re.findall(r"(?m)^(\d+\. [A-Z][^\n]*)$", txt)][:12])
print("CG:", sorted(set(re.findall(r"CG-B-DATA-21-\d+", txt))))
print("ASM:", sorted(set(re.findall(r"ASM-B-DATA-21-\d+", txt))))
print("jira:", "jira" in txt.lower())
for f in ("_work/msr/gaps/B-DATA-21.jsonl","_work/msr/assumptions/B-DATA-21.jsonl"):
    rows=[json.loads(l) for l in Path(f).read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f, len(rows), rows[0]["id"], rows[-1]["id"])
