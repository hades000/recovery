import json, io
d = json.load(io.open("_work/msr/plan/split_plan.json", encoding="utf-8"))
for s in d["slices"]:
    if "agency" in s["title"].lower() or "debt sale" in s["title"].lower() or "lot" in s["title"].lower():
        print(s["id"], "|", s["title"], "|", s["service"], "|", s["legacy"])
