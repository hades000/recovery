"""Verify v7 against v6: nothing lost, nothing changed outside the allowed additions."""
import re
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[4]
V6 = ROOT / "06 Data" / "Recovery Workbench Conceptual Data Model v6.xlsx"
V7 = ROOT / "06 Data" / "Recovery Workbench Conceptual Data Model v7.xlsx"
ALLOWED = {("Entities", "col", 8), ("Entities", "col", 9), ("Entities", "col", 10),
           ("Subject areas", "col", 6), ("Data products", "col", 11),
           ("Relationships", "col", 6), ("Relationships", "col", 7), ("Relationships", "col", 8)}
KEY_EXTRA = range(22, 27)

a, b = openpyxl.load_workbook(V6), openpyxl.load_workbook(V7)
fails = []

# 1. sheets: same order, v6 plus the two new ones
v6s = a.sheetnames
v7s = [s for s in b.sheetnames if s not in ("Read me", "Service ownership")]
if v7s != v6s:
    fails.append(f"sheet order changed: {v7s} vs {v6s}")
if b.sheetnames[0] != "Read me":
    fails.append("Read me is not the first sheet")
if b.sheetnames[-1] != "Service ownership":
    fails.append("Service ownership is not the last sheet")

# 2. every v6 cell that is inside the v6 grid keeps its value
changed = []
for name in v6s:
    sa, sb = a[name], b[name]
    for r in range(1, sa.max_row + 1):
        for c in range(1, sa.max_column + 1):
            va = sa.cell(row=r, column=c).value
            if va is None:
                continue
            if name == "Key" and r in KEY_EXTRA:
                continue
            vb = sb.cell(row=r, column=c).value
            if va != vb:
                changed.append(f"{name}!{sa.cell(row=r, column=c).coordinate}: {str(va)[:40]!r} -> {str(vb)[:40]!r}")
if changed:
    fails += changed

# 3. nothing written outside the allowed new cells
extra = []
for name in v6s:
    sa, sb = a[name], b[name]
    for r in range(1, sb.max_row + 1):
        for c in range(1, sb.max_column + 1):
            if sa.max_row >= r and sa.max_column >= c and sa.cell(row=r, column=c).value is not None:
                continue
            if sb.cell(row=r, column=c).value is None:
                continue
            if (name, "col", c) in ALLOWED:
                continue
            if name == "Key" and r in KEY_EXTRA and c <= 3:
                continue
            extra.append(f"{name}!{sb.cell(row=r, column=c).coordinate} = {str(sb.cell(row=r, column=c).value)[:40]!r}")
if extra:
    fails += ["unexpected new cell: " + x for x in extra]

# 4. every entity row carries an owner and a schema
we = b["Entities"]
blank = [r for r in range(5, 127) if not we.cell(row=r, column=8).value or not we.cell(row=r, column=9).value]
if blank:
    fails.append(f"entities without owner or schema: {blank}")
kinds = [we.cell(row=r, column=9).value for r in range(5, 127)]
if sum(1 for k in kinds if k == "recovery (ACE, read-only view)") != 30:
    fails.append("the 30 ACE views are not all marked as read-only ACE views")
if any(re.match(r"^rwb_[a-z_]+$", k) is None for k in kinds if k != "recovery (ACE, read-only view)"
       and "platform" not in k and "every service" not in k):
    fails.append("a target schema is not rwb_<name>")

# 5. formulas of the Data products sheet survived
wdp = b["Data products"]
form = [wdp.cell(row=r, column=10).value for r in range(5, 19)]
if not all(isinstance(f, str) and f.startswith("=COUNTIF") for f in form):
    fails.append(f"Data products entity count formulas lost: {form[:3]}")

# 6. relationships: every row has three values
wr = b["Relationships"]
for r in range(5, 109):
    if not all(wr.cell(row=r, column=c).value for c in (6, 7, 8)):
        fails.append(f"Relationships row {r} incomplete")

# 7. header lines and change-log row of Template and Rules R8.1
rm = b["Read me"]
txt = [rm.cell(row=r, column=1).value or "" for r in range(1, 32)]
if txt[0] != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    fails.append(f"Read me row 1: {txt[0]!r}")
if txt[1] != "(C) Siam Commercial Bank and Henka Pte Ltd":
    fails.append(f"Read me row 2: {txt[1]!r}")
log = "v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
if log not in txt:
    fails.append("change-log row missing")

# 8. no person name, no e-mail, no issue tracker, no old API base
alltext = []
for name in b.sheetnames:
    for row in b[name].iter_rows(values_only=True):
        for v in row:
            if isinstance(v, str):
                alltext.append(v)
blob = "\n".join(alltext)
for rx, why in [(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "email"), (r"(?i)\bjira\b|atlassian\.net", "issue tracker"),
                (r"/api/recovery/v1/", "old API base"), (r"(?i)\bmonolith\b", "monolith wording")]:
    m = re.search(rx, blob)
    if m:
        fails.append(f"{why} found: {blob[max(0, m.start() - 40):m.end() + 40]!r}")

print("sheets:", b.sheetnames)
print("Entities:", we.max_row - 4, "rows,", we.max_column, "columns")
print("Read me rows:", rm.max_row)
print("Service ownership rows:", b["Service ownership"].max_row - 4)
if fails:
    print("PROBLEMS", len(fails))
    for f in fails[:40]:
        print(" -", f)
    raise SystemExit(1)
print("OK: 0 problems")
