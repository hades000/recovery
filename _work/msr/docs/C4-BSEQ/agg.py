"""Compute the v7 aggregates for the Build Sequence (scratch only)."""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
OUT = ROOT / "_work" / "msr" / "docs" / "C4-BSEQ"
data = json.loads((OUT / "mapping.json").read_text(encoding="utf-8"))
items = data["items"]

WINDOW_ORDER = ["Window 1", "Window 2", "Window 3", "Window 4", "Epic 3"]
CODE = {"source-data": "P1", "integration": "P2", "case": "P3", "access": "P4", "document": "P5",
        "comms": "P6", "decision": "P7", "payment": "P8", "reporting": "P9", "agent": "P10",
        "valuation": "S1", "treatment": "S2", "guarantee": "S3", "litigation": "S4", "asset": "S5",
        "debtsale": "S6", "writeoff": "S7", "deviation": "S8", "partner": "S9",
        "platform": "PLT", "integration": "ITG"}
for _s in list(CODE):
    if _s not in ("platform", "integration"):
        CODE["rwb-" + _s] = CODE[_s]
CODE["rwb-integration"] = "P2"

# per window: items, stories, contract stories
for w in WINDOW_ORDER:
    its = [i for i in items if i["window"] == w]
    sl = [s for i in its for s in i["slices"]]
    con = [s for s in sl if s["wt"] == "Contract"]
    print(w, "items", len(its), "stories", len(sl), "con", len(con),
          "with con", sum(1 for i in its if i["con"]))
print("TOTAL items", len(items), "stories", sum(len(i["slices"]) for i in items))

# per service per window
tab = defaultdict(Counter)
for i in items:
    for s in i["slices"]:
        c = CODE[s["svc"]]
        tab[c][i["window"]] += 1
        tab[c]["Total"] += 1
        tab[c]["CON" if s["wt"] == "Contract" else "DEL"] += 1
        tab[c]["lane:" + str(s["lane"])] += 1
for c in sorted(tab, key=lambda x: (x[0] != "P", x.startswith("S"), len(x), x)):
    d = tab[c]
    print(c, {w: d[w] for w in WINDOW_ORDER}, "tot", d["Total"], "con", d["CON"], "lanes", len([k for k in d if k.startswith("lane:")]))

# day-1 counts among slices
print("Day1 slices", sum(1 for i in items for s in i["slices"] if s["ready"] == "Day 1"),
      "of", sum(len(i["slices"]) for i in items))
print("windows order check", Counter(i["window"] for i in items))
