"""Probe: aggregates that v7 needs, printed before anything is written."""
import json
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[4]
o = json.loads((Path(__file__).resolve().parent / "owners.json").read_text(encoding="utf-8"))
ents, services = o["entities"], o["services"]
ORDER = ["P%d" % i for i in range(1, 11)] + ["PLT"] + ["S%d" % i for i in range(1, 10)]
wb = openpyxl.load_workbook(ROOT / "06 Data" / "Recovery Workbench Conceptual Data Model v6.xlsx")

ws = wb["Subject areas"]
for r in range(5, 22):
    area = ws.cell(row=r, column=1).value
    members = [ws2 for ws2 in ents if False]
    cols = str(ws.cell(row=r, column=4).value).split(", ")
    owners = [ents[c]["owner"] for c in cols if c in ents]
    missing = [c for c in cols if c not in ents]
    print("SA", area, "|", sorted(set(owners), key=ORDER.index), "| missing", missing, "| n", len(cols))

ws = wb["Data products"]
for r in range(5, 19):
    dp = ws.cell(row=r, column=1).value
    names = [e for e in ents if str(ws.cell(row=r, column=1).value + " " + str(ws.cell(row=r, column=2).value)).startswith(str(dp))]
    members = [e for e, v in ents.items() if False]
    dpn = [e for e in ents if any(e == x for x in [])]
    # entity rows whose data product cell starts with the DP id
    we = wb["Entities"]
    dpfull = f"{ws.cell(row=r, column=1).value} {ws.cell(row=r, column=2).value}"
    m = [we.cell(row=i, column=1).value for i in range(5, 127) if str(we.cell(row=i, column=3).value) == dpfull]
    print("DP", dp, "n", len(m), "owners", sorted({ents[e]["owner"] for e in m}, key=ORDER.index))

we = wb["Entities"]
useries = sorted({str(we.cell(row=i, column=3).value).split(" ")[0] for i in range(5, 127)})
print("data product codes in Entities:", useries)

wr = wb["Relationships"]
cross, same, bad = [], [], []
for r in range(5, 109):
    a, b = wr.cell(row=r, column=1).value, wr.cell(row=r, column=2).value
    if a not in ents or b not in ents:
        bad.append((r, a, b)); continue
    (same if ents[a]["owner"] == ents[b]["owner"] else cross).append((a, b, ents[a]["owner"], ents[b]["owner"]))
print("relationships", 108 - 5 + 1, "cross", len(cross), "same", len(same), "unresolved", bad)
from collections import Counter
print("cross pairs", Counter((x[2], x[3]) for x in cross).most_common())
