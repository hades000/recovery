import json
import re
from pathlib import Path

g = Path(r"_work/msr/gaps/B-ARCH-DL.jsonl")
a = Path(r"_work/msr/assumptions/B-ARCH-DL.jsonl")
GK = {"id", "title", "source", "section", "description", "evidence", "type", "severity", "needed_by_wave",
      "legacy_ref", "owner_role", "asm", "proposed", "wp", "area"}
AK = {"id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"}
for p, keys in ((g, GK), (a, AK)):
    rows = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    print(p.name, len(rows), "rows")
    for r in rows:
        miss = keys - set(r)
        extra = set(r) - keys
        print("  ", r["id"], "missing", sorted(miss), "extra", sorted(extra))
        for k, v in r.items():
            if isinstance(v, str) and re.search(r"\bK\.\s*[A-Z]", v):
                print("     NAME in", k)

NAME = re.compile(r"\bK\.\s*[A-Z]")
LOG = Path(r"_work/msr/editlog/B-ARCH-DL.md")
t = LOG.read_text(encoding="utf-8")
print("editlog name hits:", NAME.findall(t), "| jira:", re.findall(r"(?i)jira|atlassian", t))
print("tool line present:", "T3 Code / OpenCode / DeepSeek v4.1 Flash" in t)
print("citations:", sorted(set(re.findall(r"\b(?:CG|ASM)-B-ARCH-DL-\d\b", t))))
