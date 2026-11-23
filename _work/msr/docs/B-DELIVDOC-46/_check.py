import json, re
from pathlib import Path

for f in ("_work/msr/gaps/B-DELIVDOC-46.jsonl", "_work/msr/assumptions/B-DELIVDOC-46.jsonl"):
    rows = [json.loads(l) for l in Path(f).read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f, len(rows), [r["id"] for r in rows])

md = Path("_work/msr/docs/B-DELIVDOC-46/Recovery Workbench Cutover and Go Live Plan v4.md").read_text(encoding="utf-8")
ids = set()
for f in ("_work/msr/gaps/B-DELIVDOC-46.jsonl", "_work/msr/assumptions/B-DELIVDOC-46.jsonl"):
    for l in Path(f).read_text(encoding="utf-8").splitlines():
        if l.strip():
            ids.add(json.loads(l)["id"])
cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", md))
print("cited", len(cited))
print("missing rows:", sorted(cited - ids))
print("uncited rows:", sorted(ids - cited))
print("jira?", re.search(r"(?i)\bjira\b|atlassian\.net", md))
print("first lines:", md.splitlines()[:2])
