import json
from collections import Counter
from pathlib import Path

g = [json.loads(l) for l in Path("_work/msr/gaps/B-REQ-PRD-S6.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
a = [json.loads(l) for l in Path("_work/msr/assumptions/B-REQ-PRD-S6.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
print(Counter(x["type"] for x in g))
print(Counter(x["severity"] for x in g))
print(len(g), len(a), sum(1 for x in a if not x["gap"]))
