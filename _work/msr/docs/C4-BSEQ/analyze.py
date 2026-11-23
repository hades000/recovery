"""Analyse the Build Sequence v6 source against the split plan and the story catalog."""
import json, sys
from pathlib import Path
import openpyxl

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
WORK = ROOT / "_work" / "msr"

plan = json.loads((WORK / "plan" / "split_plan.json").read_text(encoding="utf-8"))
legacy = plan["legacy"]

wb = openpyxl.load_workbook(ROOT / "04 User stories" / "Recovery Workbench Service Story Catalog v1.xlsx",
                            read_only=True, data_only=True)
ws = wb["Stories"]
rows = list(ws.iter_rows(values_only=True))
hdr = rows[0]
cat = {}
for r in rows[1:]:
    d = dict(zip(hdr, r))
    cat[d["Story"]] = d
wb.close()

src = openpyxl.load_workbook(ROOT / "11 Delivery and operations" /
                             "Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx",
                             read_only=True, data_only=True)
ws = src["Sequence"]
srows = [list(r) for r in ws.iter_rows(values_only=True)]
src.close()

items = []
for r in srows[4:]:
    if r[0] is None:
        continue
    items.append({"order": r[0], "key": r[1], "title": r[2], "module": r[3], "type": r[4],
                  "priority": r[5], "dep": r[6], "window": r[7], "dates": r[8], "release": r[9],
                  "cp": r[10]})
print("items", len(items))

missing_legacy = [i["key"] for i in items if i["key"] not in legacy]
print("missing from split_plan legacy:", missing_legacy)

missing_cat = set()
for k, v in legacy.items():
    for s in v["slices"]:
        if s not in cat:
            missing_cat.add(s)
print("slices not in catalog:", len(missing_cat), list(missing_cat)[:10])

# slices with no CON story for a legacy key used in the sheet
for i in items:
    v = legacy.get(i["key"])
    if not v:
        continue
    cons = [s for s in v["slices"] if s.endswith("-CON")]
    if not cons:
        print("NO CON:", i["key"], i["module"], v["slices"])

# lanes / waves for the items
print()
for i in items[:5]:
    v = legacy[i["key"]]
    print(i["key"], v["primary"], v["wave"], [cat[s]["Lane"] for s in v["slices"] if s in cat])
