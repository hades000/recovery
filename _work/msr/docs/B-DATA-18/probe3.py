import json, re
from pathlib import Path

dump = json.load(open("_work/msr/docs/B-DATA-18/v4_dump.json", encoding="utf-8"))
# dates anywhere
pat = re.compile(r"\b(20\d\d|January|February|March|April|May|June|July|August|September|October|November|December)\b")
for sheet, rows in dump.items():
    for i, r in enumerate(rows):
        for c in r:
            if pat.search(str(c)):
                print("DATE?", sheet, i, c)
print("---- legacy keys with ACE")
plan = json.load(open("_work/msr/plan/split_plan.json", encoding="utf-8"))
for k, v in plan["legacy"].items():
    if "ACE" in k:
        print(k, v["disposition"], v["primary"] if "primary" in v else "", v["slices"][:6])
print("---- Interface Specifications docs")
for p in Path(".").rglob("*Interface Specification*"):
    print(p)
print("---- ACE001 stories")
for s in plan["slices"]:
    if "ACE" in s["legacy"]:
        print(s["id"], s["legacy"], s["wt"], s["title"])
