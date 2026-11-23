"""Verify Recovery Workbench System Disposition and Integration Inventory v4.xlsx (WP B-TECH-16).

Checks, all read-only:
  1. header lines 1 and 2 of the Read me sheet are the Template and Rules R8.1 header;
  2. the change-log row names D-RCV-60 and the tool line;
  3. every cell of the 25 disposition rows and the 36 interface rows equals the v3 cell,
     except the one new Service cell of each row (no source cell changed, none dropped);
  4. the By route counts equal a recount of the Interfaces sheet;
  5. the By service counts equal the same recount;
  6. the Key, Disposition and Interfaces sheet keep their header and their row counts;
  7. no person name and no email address anywhere in the workbook;
  8. the source v3 file is byte-for-byte the file it was before the build.
"""
import hashlib
import re
from pathlib import Path

import openpyxl

SRC = Path(r"05 Technical architecture\Recovery Workbench System Disposition and Integration Inventory v3.xlsx")
OUT = Path(r"05 Technical architecture\Recovery Workbench System Disposition and Integration Inventory v4.xlsx")
SRC_SHA16 = "d78cb10f14f63d6c"
H1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
H2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
fails = []


def bad(msg):
    fails.append(msg)


src = openpyxl.load_workbook(SRC)
out = openpyxl.load_workbook(OUT)

# 8. source untouched
h = hashlib.sha256(SRC.read_bytes()).hexdigest()[:16]
if h != SRC_SHA16:
    bad(f"v3 source changed: sha {h}")

# 1, 2. Read me
rd = out["Read me"]
if rd["A1"].value != H1:
    bad(f"Read me A1 is not the R8.1 first header line: {rd['A1'].value!r}")
if rd["A2"].value != H2:
    bad(f"Read me A2 is not the R8.1 second header line: {rd['A2'].value!r}")
log = [rd.cell(row=r, column=1).value for r in range(1, rd.max_row + 1)]
if "v4, 22 November 2026, D-RCV-60 microservice realignment, " + TOOL not in log:
    bad("change-log row missing from the Read me sheet")
if not any("D-RCV-60" in str(v) for v in log):
    bad("no D-RCV-60 reference in the Read me sheet")

# sheets
if out.sheetnames[:5] != ["Read me", "Disposition", "Interfaces", "By route", "Key"]:
    bad(f"sheet order: {out.sheetnames}")
added = out.sheetnames[5:]
if added != ["By service", "Service rules", "Realignment changes"]:
    bad(f"added sheets: {added}")

# 3. cell-by-cell diff of the two data sheets
sd, od = src["Disposition"], out["Disposition"]
if [sd.cell(row=4, column=c).value for c in range(1, 10)] != [od.cell(row=4, column=c).value
                                                              for c in (1, 2, 3, 4, 5, 7, 8, 9, 10)]:
    bad("Disposition header row changed")
if od.cell(row=4, column=6).value != "Service":
    bad("Disposition Service header missing")
if od.max_row != 29:
    bad(f"Disposition row count {od.max_row}")
diff = 0
for r in range(5, 30):
    if not od.cell(row=r, column=6).value:
        bad(f"Disposition row {r}: Service cell empty")
    for sc, oc in zip(range(1, 10), (1, 2, 3, 4, 5, 7, 8, 9, 10)):
        if sd.cell(row=r, column=sc).value != od.cell(row=r, column=oc).value:
            diff += 1
            bad(f"Disposition r{r} c{sc}: {sd.cell(row=r, column=sc).value!r} -> "
                f"{od.cell(row=r, column=oc).value!r}")
if diff:
    bad(f"{diff} Disposition cells changed")
if sd.cell(row=2, column=1).value != od.cell(row=2, column=1).value:
    bad("Disposition description row changed")
if sd.cell(row=1, column=1).value != od.cell(row=1, column=1).value:
    bad("Disposition title row changed")

si, oi = src["Interfaces"], out["Interfaces"]
if [si.cell(row=4, column=c).value for c in range(1, 14)] != [oi.cell(row=4, column=c).value
                                                               for c in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14)]:
    bad("Interfaces header row changed")
if oi.cell(row=4, column=11).value != "Service":
    bad("Interfaces Service header missing")
if oi.max_row != 40:
    bad(f"Interfaces row count {oi.max_row}")
diff = 0
for r in range(5, 41):
    if not oi.cell(row=r, column=11).value:
        bad(f"Interfaces row {r}: Service cell empty")
    for sc, oc in zip(range(1, 14), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14)):
        if si.cell(row=r, column=sc).value != oi.cell(row=r, column=oc).value:
            diff += 1
            bad(f"Interfaces r{r} c{sc}: {si.cell(row=r, column=sc).value!r} -> "
                f"{oi.cell(row=r, column=oc).value!r}")
if diff:
    bad(f"{diff} Interfaces cells changed")
if si.cell(row=2, column=1).value != oi.cell(row=2, column=1).value:
    bad("Interfaces description row changed")

# 4, 5. counts
counts = {}
for r in range(5, 41):
    route, direction = oi.cell(row=r, column=5).value, oi.cell(row=r, column=4).value
    counts.setdefault(route, {"In": 0, "Out": 0, "Both": 0})[direction] += 1
br = out["By route"]
tot = {"In": 0, "Out": 0, "Both": 0}
for r in range(5, 10):
    route = br.cell(row=r, column=1).value
    got = counts.get(route, {"In": 0, "Out": 0, "Both": 0})
    for col, k in zip((2, 3, 4), ("In", "Out", "Both")):
        tot[k] += got[k]
        if br.cell(row=r, column=col).value != got[k]:
            bad(f"By route {route} {k}: {br.cell(row=r, column=col).value} != {got[k]}")
    if br.cell(row=r, column=5).value != sum(got.values()):
        bad(f"By route {route} total")
for col, k in zip((2, 3, 4, 5), ("In", "Out", "Both", None)):
    want = tot[k] if k else sum(tot.values())
    if br.cell(row=10, column=col).value != want:
        bad(f"By route Total {k or 'all'}: {br.cell(row=10, column=col).value} != {want}")

per = {}
for r in range(5, 41):
    code = str(oi.cell(row=r, column=11).value).split(" ")[0]
    per[code] = per.get(code, 0) + 1
bs = out["By service"]
seen = {}
for r in range(5, bs.max_row):
    code = bs.cell(row=r, column=1).value
    if code == "Total":
        continue
    seen[code] = bs.cell(row=r, column=8).value
    if bs.cell(row=r, column=8).value != per.get(code):
        bad(f"By service {code}: {bs.cell(row=r, column=8).value} != {per.get(code)}")
if set(seen) != set(per):
    bad(f"By service codes {sorted(seen)} != {sorted(per)}")
if bs.cell(row=bs.max_row, column=8).value != 36:
    bad("By service total is not 36")

# 6. header rows of Key
ko, ks = out["Key"], src["Key"]
if [ks.cell(row=4, column=c).value for c in (1, 2, 3)] != [ko.cell(row=4, column=c).value for c in (1, 2, 3)]:
    bad("Key header row changed")
if ks.max_row != 27 or ko.max_row != 33:
    bad(f"Key rows: source {ks.max_row}, output {ko.max_row}")
for r in range(1, 28):
    for c in range(1, 4):
        if ks.cell(row=r, column=c).value != ko.cell(row=r, column=c).value:
            bad(f"Key r{r} c{c} changed")

# 7. no person name / email
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
names = set()
for ws in out.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            v = cell.value
            if isinstance(v, str):
                if EMAIL.search(v):
                    bad(f"{ws.title}!{cell.coordinate}: email address")
                for token in re.findall(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", v):
                    if token not in ("Henka Group", "Siam Commercial", "Core bank", "Recovery Workbench",
                                     "Service Catalog", "Data lake", "Power BI", "Enterprise AI", "Shared App",
                                     "Debt Sale", "Credit Decision", "Case Management", "Technical Architecture"):
                        names.add(token)
props = out.properties
if props.creator != "Henka Group":
    bad(f"creator {props.creator!r}")
if props.lastModifiedBy != TOOL:
    bad(f"lastModifiedBy {props.lastModifiedBy!r}")
if not props.title or "v4" not in props.title:
    bad(f"title {props.title!r}")

print("PASS" if not fails else "FAIL")
for f in fails[:60]:
    print(" -", f)
print(f"sheets: {out.sheetnames}")
print(f"Disposition rows: {od.max_row - 4}, Interfaces rows: {oi.max_row - 4}, Key rows: {ko.max_row - 4}")
print(f"By route total {sum(tot.values())} (In {tot['In']}, Out {tot['Out']}, Both {tot['Both']})")
print(f"services with a path: {len(per)}; person-like tokens seen: {sorted(names)}")
print(f"props: {props.creator} / {props.lastModifiedBy} / {props.title} / revision {props.revision}")
