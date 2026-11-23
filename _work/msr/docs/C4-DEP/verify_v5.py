"""C4-DEP: verify that v5 keeps every source cell of v4 and that the new sheets are coherent."""
import collections
import sys
from pathlib import Path

import openpyxl

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
V4 = ROOT / "11 Delivery and operations" / "Recovery Workbench Dependency Map v4.xlsx"
V5 = ROOT / "11 Delivery and operations" / "Recovery Workbench Dependency Map v5.xlsx"
CAT = ROOT / "04 User stories" / "Recovery Workbench Service Story Catalog v1.xlsx"

fails = []
a = openpyxl.load_workbook(V4, data_only=True)
b = openpyxl.load_workbook(V5, data_only=True)

pairs = [("Dependencies", "Dependencies"), ("Story dependencies", "Story dependencies v4"),
         ("By team and epic", "By team and epic"), ("How they are tracked", "How they are tracked")]
checked = 0
for s, t in pairs:
    wsa, wsb = a[s], b[t]
    for row in wsa.iter_rows():
        for c in row:
            if c.value is None:
                continue
            v = wsb.cell(row=c.row, column=c.column).value
            checked += 1
            if v != c.value:
                fails.append(f"{t}!{c.coordinate}: {c.value!r} -> {v!r}")

# counts
st = b["Story dependencies v5"]
hdr = [c.value for c in st[4]]
rows = [r for r in st.iter_rows(min_row=5, values_only=True) if r[0] and r[13] in ("H", "C", "I", "X")]
cls = collections.Counter(r[13] for r in rows)
if len(rows) != 2534:
    fails.append(f"Story dependencies v5 has {len(rows)} data rows, expected 2534")
if dict(cls) != {"H": 1600, "C": 440, "I": 412, "X": 82}:
    fails.append(f"class counts {dict(cls)}")

cat = openpyxl.load_workbook(CAT, read_only=True, data_only=True)
want = {(r[0], r[1]) for r in cat["Dependencies"].iter_rows(min_row=2, values_only=True) if r[0]}
got = {(r[0], r[7]) for r in rows}
if want != got:
    fails.append(f"row set differs from the catalog: missing {len(want - got)}, extra {len(got - want)}")
cat.close()

# every service code resolves against the Ownership Map
own = openpyxl.load_workbook(ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx",
                             read_only=True, data_only=True)
codes = {r[0] for r in own["Services"].iter_rows(min_row=2, values_only=True) if r[0]} | {"PLT", "ITG"}
own.close()
bad = {r[5] for r in rows} | {r[11] for r in rows}
if not bad <= codes:
    fails.append(f"unknown service code {sorted(bad - codes)}")

# header on sheet 1 and the change-log row
rm = b["Read me"]
if rm["A1"].value != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    fails.append("Read me A1 is not the R8.1 header line")
if rm["A2"].value != "(C) Siam Commercial Bank and Henka Pte Ltd":
    fails.append("Read me A2 is not the R8.1 header line")
tool = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
if tool not in str(rm["A6"].value) or "D-RCV-60 microservice realignment" not in str(rm["A13"].value or ""):
    fails.append("Read me change-log row or tool line missing")
if "v5, 22 November 2026, D-RCV-60 microservice realignment" not in str(rm["A13"].value):
    fails.append("change-log row text")

# legacy trace
tr = b["Legacy dependency trace"]
trows = [r for r in tr.iter_rows(min_row=5, values_only=True) if r[0] and r[7] in ("Carried", "Carried by redirect", "Dropped", "Not carried")]
if len(trows) != 325:
    fails.append(f"Legacy dependency trace has {len(trows)} rows, expected 325")
ts = collections.Counter(r[7] for r in trows)
if sum(ts.values()) != 325:
    fails.append("trace status counts do not add up")

# external Dependencies sheet: 36 rows each with class X
dp = b["Dependencies"]
dep_rows = [r for r in dp.iter_rows(min_row=5, max_row=40, values_only=True) if r[0]]
if len(dep_rows) != 36 or {r[9] for r in dep_rows} != {"X"}:
    fails.append("Dependencies sheet rows or class column")

# totals on By service and class must reconcile
bs = b["By service and class"]
svc_rows = [r for r in bs.iter_rows(min_row=5, max_row=25, values_only=True) if r[0]]
if sum(r[7] for r in svc_rows) != 2534 or sum(r[12] for r in svc_rows) != 2534:
    fails.append(f"service totals do not add to 2534: out {sum(r[7] for r in svc_rows)}, in {sum(r[12] for r in svc_rows)}")
wave_rows = [r for r in bs.iter_rows(min_row=30, max_row=34, values_only=True) if r[0] is not None and r[6] is not None]
if sum(r[6] for r in wave_rows) != 2534:
    fails.append(f"wave totals do not add to 2534: {sum(r[6] for r in wave_rows)}")

# no person name, no issue tracker, no monolith API base anywhere in the workbook text
bad_words = ["rajdeep", "ghai", "jira", "atlassian", "confluence", "@", "/api/recovery/v1/"]
for name in b.sheetnames:
    for row in b[name].iter_rows(values_only=True):
        for v in row:
            if isinstance(v, str):
                low = v.lower()
                for w in bad_words:
                    if w in low:
                        fails.append(f"{name}: text contains {w!r}: {v[:80]!r}")
                        break
props = b.properties
for p in (props.creator, props.lastModifiedBy, props.title, props.subject):
    if p and "ghai" in str(p).lower():
        fails.append(f"workbook property carries a person name: {p}")

print(f"cells compared: {checked}")
print("trace:", dict(ts))
print("FAIL" if fails else "PASS")
for f in fails[:40]:
    print(" -", f)
sys.exit(1 if fails else 0)
