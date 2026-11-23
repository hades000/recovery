"""C-BN1 scratch: read the Service Story Catalog v1 and the split plan into one JSON."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr"
OUT = WORK / "docs" / "C-BN1" / "data.json"

import openpyxl

wb = openpyxl.load_workbook(ROOT / "04 User stories" / "Recovery Workbench Service Story Catalog v1.xlsx", read_only=True)


def sheet(name):
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    return [dict(zip(hdr, r)) for r in rows[1:] if r[0]]


stories = sheet("Stories")
deps = sheet("Dependencies")
plan = json.loads((WORK / "plan" / "split_plan.json").read_text(encoding="utf-8"))
own = json.loads((WORK / "plan" / "ownership.json").read_text(encoding="utf-8"))

e1 = {}
for s in stories:
    legacy = str(s["Legacy"])
    if legacy.startswith(("RWB-E1-", "RWB-TE-", "RWB-ACE")):
        e1.setdefault(legacy, []).append({
            "id": s["Story"], "title": s["Title"], "wt": s["Work type"], "owner": s["Suggested owner"],
            "service": s["Service"], "epic": s["Epic"], "wave": s["Wave"], "be": s["Business epic"],
            "release": s["Release"], "disposition": s["Disposition"], "lane": s["Lane"], "ready": s["Ready"],
            "file": s["File"],
        })

d = {}
for r in deps:
    if r["Story"] in {x["id"] for v in e1.values() for x in v}:
        d.setdefault(r["Story"], []).append({"on": r["Depends on"], "class": r["Class"]})

for k, v in e1.items():
    for x in v:
        x["deps"] = d.get(x["id"], [])

data = {
    "stories": e1,
    "legacy": {k: {kk: vv for kk, vv in v.items() if kk in ("disposition", "primary", "patterns", "slices", "wave")}
               for k, v in plan["legacy"].items() if k.startswith(("RWB-E1-", "RWB-TE-", "RWB-ACE"))},
    "tables": own["tables"],
}
OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
print("legacy keys", len(data["legacy"]), "epic1 stories", sum(len(v) for v in e1.values()))
