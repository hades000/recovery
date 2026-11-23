"""Verification of the two B-ARCH-EVT workbooks (read only)."""
import json
import re
import sys
from pathlib import Path

import openpyxl

SRC = Path(r"05 Technical architecture\Recovery Workbench Event and Messaging Design v4.xlsx")
DST = Path(r"05 Technical architecture\Recovery Workbench Event and Messaging Design v5.xlsx")
CAT = Path(r"05 Technical architecture\Recovery Workbench Kafka Topic and Event Catalog v1.xlsx")
GAPS = Path(r"_work\msr\gaps\B-ARCH-EVT.jsonl")
ASMS = Path(r"_work\msr\assumptions\B-ARCH-EVT.jsonl")

fails = []

# ---------------------------------------------------------------- source sheets untouched
a, b = openpyxl.load_workbook(SRC), openpyxl.load_workbook(DST)
for name in ("Events", "Rules"):
    wa, wb_ = a[name], b[name]
    if (wa.max_row, wa.max_column) != (wb_.max_row, wb_.max_column):
        fails.append("%s: dimension changed %s -> %s" % (name, (wa.max_row, wa.max_column),
                                                         (wb_.max_row, wb_.max_column)))
    for r in range(1, wa.max_row + 1):
        for c in range(1, wa.max_column + 1):
            if wa.cell(r, c).value != wb_.cell(r, c).value:
                fails.append("%s!%s changed: %r -> %r" % (name, wa.cell(r, c).coordinate,
                                                          wa.cell(r, c).value, wb_.cell(r, c).value))
print("source sheets: Events %d rows, Rules %d rows, differences: %d"
      % (a["Events"].max_row, a["Rules"].max_row, len(fails)))

# ---------------------------------------------------------------- ids cited exist
ids = set()
for p in (GAPS, ASMS):
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(json.loads(line)["id"])
print("register rows:", len(ids))
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
seen = set()
for path in (DST, CAT):
    wbx = openpyxl.load_workbook(path)
    for ws in wbx.worksheets:
        for row in ws.iter_rows(values_only=True):
            for val in row:
                if isinstance(val, str):
                    seen.update(cite.findall(val))
missing = sorted(seen - ids)
print("cited ids:", len(seen), "missing from the registers:", missing)
if missing:
    fails.append("cites ids with no register row: %s" % missing)
unused = sorted(ids - seen)
print("register rows not cited in the workbooks:", unused)

# ---------------------------------------------------------------- event and topic counts
cat = openpyxl.load_workbook(CAT)


def rows_of(ws, hdr_row=4):
    hdr = [c.value for c in ws[hdr_row]]
    out = []
    for r in ws.iter_rows(min_row=hdr_row + 1, values_only=True):
        if any(r):
            out.append(dict(zip(hdr, r)))
    return out


ev = rows_of(cat["Events"])
print("catalog events:", len(ev))
names = [e["Event"] for e in ev]
if len(set(names)) != len(names):
    fails.append("duplicate event names in the catalog")
if len(ev) != 45:
    fails.append("catalog Events holds %d rows, expected 45 (30 v4 entries + 15 new)" % len(ev))
num = [e for e in ev if str(e["EV row"]).startswith("EV-")]
print("rows with an EV number:", len(num), "new:", len(ev) - len(num))

topics = rows_of(cat["Topics"])
print("catalog event topics:", len(topics))
per = {t["Topic"]: str(t["Event types carried"]).count(",") + 1 for t in topics}
print("event types per topic total:", sum(per.values()))
if sum(per.values()) != 43:
    fails.append("event types per topic total %d, expected 43" % sum(per.values()))
for t, n in per.items():
    print("   ", t, n)

dlt = rows_of(cat["Dead-letter topics"])
print("dead-letter topics:", len(dlt))
if len(topics) != 20 or len(dlt) != 20:
    fails.append("topic counts are %d event and %d dead-letter" % (len(topics), len(dlt)))

# every event's topic exists in the Topics sheet
tset = {t["Topic"] for t in topics}
for e in ev:
    t = e["Topic"]
    if str(t).startswith("rwb.") and t not in tset:
        fails.append("%s carries unknown topic %s" % (e["Event"], t))
    if not str(t).startswith("rwb.") and e["Family"] not in ("Retired (durable timer)", "Temporal signal"):
        fails.append("%s has no topic but family %s" % (e["Event"], e["Family"]))

# ---------------------------------------------------------------- design register
d = openpyxl.load_workbook(DST)
dv = rows_of(d["Events v5"])
print("design Events v5 rows:", len(dv))
if len(dv) != 45:
    fails.append("design Events v5 holds %d rows" % len(dv))
if [x["Event"] for x in dv] != names:
    fails.append("the two event registers are not in the same order")
if [list(x.values()) for x in dv] != [list(x.values()) for x in ev]:
    fails.append("the two event registers do not hold the same values")
print("design sheets:", d.sheetnames)

# ---------------------------------------------------------------- names and emails
bad = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
for path in (DST, CAT):
    wbx = openpyxl.load_workbook(path)
    for ws in wbx.worksheets:
        for row in ws.iter_rows(values_only=True):
            for val in row:
                if isinstance(val, str) and bad.search(val):
                    fails.append("%s!%s: email address" % (ws.title, val[:40]))

print()
if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("ALL CHECKS PASS")
