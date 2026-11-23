"""B-BIZ-38 - verify the v5 workbook against the v4 source.

Checks:
  1. every cell value of every v4 sheet appears unchanged in v5 (same sheet, same cell)
  2. every v4 sheet keeps its order and position ahead of the new sheets
  3. the R8.1 header lines, the change-log row and the tool line are present
  4. no person name from the v4 document properties appears anywhere in v5
  5. the 54 role rows, 14 areas, 8 pairs, 18 flow rows, 54 single sign-on rows hold
"""
import re
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "02 Business architecture and process" / "Recovery Workbench Users Roles and Permissions v4.xlsx"
DST = ROOT / "02 Business architecture and process" / "Recovery Workbench Users Roles and Permissions v5.xlsx"

src = openpyxl.load_workbook(SRC)
dst = openpyxl.load_workbook(DST)

fails = []
diffs = 0
cells = 0
for ws in src:
    if ws.title not in dst.sheetnames:
        fails.append(f"sheet {ws.title} missing from v5")
        continue
    d = dst[ws.title]
    for row in ws.iter_rows():
        for c in row:
            if c.value is None:
                continue
            cells += 1
            got = d.cell(c.row, c.column).value
            if got != c.value:
                diffs += 1
                fails.append(f"{ws.title}!{c.coordinate}: v4={c.value!r} v5={got!r}")

if dst.sheetnames[1:9] != src.sheetnames:
    fails.append(f"v4 sheet order changed: {dst.sheetnames[1:9]} vs {src.sheetnames}")

readme = dst["Read me"]
head = [readme.cell(1, 1).value, readme.cell(2, 1).value]
if head != ["SCB Collections and Recovery. Henka Group, 22 November 2026.",
            "(C) Siam Commercial Bank and Henka Pte Ltd"]:
    fails.append(f"header lines wrong: {head}")
flat = "\n".join(str(c.value) for row in readme.iter_rows() for c in row if c.value)
need = ["5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash",
        "T3 Code / OpenCode / DeepSeek v4.1 Flash"]
for n in need:
    if n not in flat:
        fails.append(f"Read me missing: {n}")

bad = re.compile(r"Rajdeep|Ghai", re.I)
for ws in dst:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and bad.search(c.value):
                fails.append(f"{ws.title}!{c.coordinate}: person name")
for attr in ("creator", "lastModifiedBy"):
    if bad.search(str(getattr(dst.properties, attr))):
        fails.append(f"document property {attr} carries a person name")

roles = dst["Roles"]
if roles.max_row != 58:
    fails.append(f"Roles rows {roles.max_row}")
if roles.max_column != 11:
    fails.append(f"Roles columns {roles.max_column}")
if roles.cell(4, 11).value != "Enforcing services (D-RCV-60)":
    fails.append("Roles column K header")
blank_k = [r for r in range(5, 59) if not roles.cell(r, 11).value]
if blank_k:
    fails.append(f"blank column K rows {blank_k}")

perm = dst["Permissions"]
if perm.max_row != 58 or perm.max_column != 17:
    fails.append(f"Permissions grid changed: {perm.max_row}x{perm.max_column}")
if len([c for c in perm[4] if c.value]) != 17:
    fails.append("Permissions header row changed")

if dst["Separation of duty"].max_row != 13:
    fails.append(f"Separation of duty rows {dst['Separation of duty'].max_row}")
if dst["Access flow"].max_row != 21:
    fails.append(f"Access flow rows {dst['Access flow'].max_row}")
if dst["Single sign-on"].max_row != 54:
    fails.append(f"Single sign-on rows {dst['Single sign-on'].max_row}")
if dst["Systems by role"].max_row != 42:
    fails.append(f"Systems by role rows {dst['Systems by role'].max_row}")
if dst["Key"].max_row != 26:
    fails.append(f"Key rows {dst['Key'].max_row}")

areas = dst["Area owners"]
n_areas = len([r for r in range(5, 20) if areas.cell(r, 1).value and areas.cell(r, 2).value])
if n_areas != 15:
    fails.append(f"Area owners rows {n_areas}")

ac = dst["Authorise contract"]
ops = [ac.cell(r, 1).value for r in range(1, ac.max_row + 1)]
for op in ("POST /authorise", "GET /me/permissions", "GET /doa-limits", "GET /masking-policies",
           "AccessPolicyChanged", "DoaLimitChanged", "JOB-18"):
    if not any(op in str(o) for o in ops):
        fails.append(f"Authorise contract missing {op}")

print(f"cells_compared={cells} differences={diffs} sheets={dst.sheetnames}")
print("PASS" if not fails else "FAIL")
for f in fails[:40]:
    print(" -", f)
raise SystemExit(1 if fails else 0)
