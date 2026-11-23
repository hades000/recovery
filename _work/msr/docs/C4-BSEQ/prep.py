"""Build the mapping data for the Build Sequence v7 (scratch only)."""
import json
from pathlib import Path
import openpyxl

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
WORK = ROOT / "_work" / "msr"
OUT = WORK / "docs" / "C4-BSEQ"

SERVICES = [
    ("P1", "source-data", "Source data", 1), ("P2", "integration", "Integration", 1),
    ("P3", "case", "Case and workflow", 1), ("P4", "access", "Access and authority", 1),
    ("P5", "document", "Document", 1), ("P6", "comms", "Communications", 1),
    ("P7", "decision", "Decision and rules", 1), ("P8", "payment", "Payment", 2),
    ("P9", "reporting", "Reporting", 1), ("P10", "agent", "Agent", 1),
    ("S1", "valuation", "Valuation and route", 3), ("S2", "treatment", "Treatment and offer", 2),
    ("S3", "guarantee", "Guarantee", 3), ("S4", "litigation", "Litigation", 3),
    ("S5", "asset", "Asset", 2), ("S6", "debtsale", "Debt sale", 3),
    ("S7", "writeoff", "Write-off", 4), ("S8", "deviation", "Deviation", 2),
    ("S9", "partner", "Partner", 4),
]
CODE = {s[1]: s for s in SERVICES}
CODE["platform"] = ("PLT", "platform", "Platform", 0)
CODE["integration"] = ("ITG", "integration", "Integration waves", 0)

WT_OWNER_SHORT = {"CON": "TechX", "APP": "TechX", "ITG": "TechX", "DB": "ACE team",
                  "INF": "SCB IT infrastructure", "OPS": "DevOps team"}

plan = json.loads((WORK / "plan" / "split_plan.json").read_text(encoding="utf-8"))
legacy = plan["legacy"]

wb = openpyxl.load_workbook(ROOT / "04 User stories" / "Recovery Workbench Service Story Catalog v1.xlsx",
                            read_only=True, data_only=True)
ws = wb["Stories"]
rows = list(ws.iter_rows(values_only=True))
hdr = list(rows[0])
cat = {}
for r in rows[1:]:
    d = dict(zip(hdr, r))
    cat[d["Story"]] = d
wb.close()

src = openpyxl.load_workbook(ROOT / "11 Delivery and operations" /
                             "Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx",
                             read_only=True, data_only=True)
srows = [list(r) for r in src["Sequence"].iter_rows(values_only=True)]
win = [list(r) for r in src["By window"].iter_rows(values_only=True)]
crit = [list(r) for r in src["Critical path"].iter_rows(values_only=True)]
mod = [list(r) for r in src["By module"].iter_rows(values_only=True)]
pull = [list(r) for r in src["Pull rules"].iter_rows(values_only=True)]
src.close()

items = []
for r in srows[4:]:
    if r[0] is None:
        continue
    items.append({"order": int(r[0]), "key": r[1], "title": r[2], "module": r[3], "type": r[4],
                  "priority": r[5], "dep": r[6], "window": r[7], "dates": r[8], "release": r[9],
                  "cp": r[10]})

for it in items:
    v = legacy[it["key"]]
    slices = []
    for s in v["slices"]:
        c = cat[s]
        slices.append({"id": s, "wt": c["Work type"], "svc": c["Service"], "lane": c["Lane"],
                       "ready": c["Ready"], "owner": c["Suggested owner"], "title": c["Title"],
                       "epic": c["Epic"], "wave": c["Wave"], "release": c["Release"]})
    it["primary_svc"] = v.get("primary") or (v["slices"][0].split("-")[1] if v["slices"] else "")
    it["wave"] = v.get("wave") or (slices[0]["wave"] if slices else "")
    it["disposition"] = v["disposition"]
    it["slices"] = slices
    it["con"] = [s for s in slices if s["wt"] == "Contract"]
    it["del"] = [s for s in slices if s["wt"] != "Contract"]

# platform day-1 block
plt = [dict(zip(hdr, r)) for r in rows[1:] if str(r[5]).startswith("RWB-PLT")]
cg = {}
for d in cat.values():
    if d["Work type"] == "Contract":
        cg.setdefault(d["Lane"], []).append(d)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "mapping.json").write_text(json.dumps({
    "items": items, "plt": plt, "cg": {k: len(v) for k, v in cg.items()},
    "win": win, "crit": crit, "mod": mod, "pull": pull,
}, ensure_ascii=False, indent=1), encoding="utf-8")

print("items", len(items), "plt stories", len(plt), "cg", {k: len(v) for k, v in cg.items()})
for it in items[:4]:
    print(it["key"], it["module"], "| CON:", [c["id"] for c in it["con"]],
          "| DEL:", [c["id"] for c in it["del"]][:4], "| ready:", it["del"][0]["ready"] if it["del"] else "")
print()
print("release values:", sorted({str(i["release"]) for i in items}))
print("windows:", sorted({str(i["window"]) for i in items}))
print("modules:", sorted({str(i["module"]) for i in items}))
print("plt releases:", sorted({str(p["Release"]) for p in plt}))
print("plt epics:", sorted({str(p["Epic"]) for p in plt}))
print("plt lanes sample:", sorted({str(p["Lane"]) for p in plt}))
