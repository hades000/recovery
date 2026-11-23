"""Verify v4 against the v3 source: cells, rows, columns, header, change log."""
import json
import openpyxl

SRC = "06 Data/Recovery Workbench Data Ownership and Stewardship v3.xlsx"
OUT = "06 Data/Recovery Workbench Data Ownership and Stewardship v4.xlsx"
EXPECTED = {
    ("Ownership split", 7, 6): ("Read and write by the recovery module",
                                "Read and write by P1 rwb-source-data only, in rwb_source_data"),
    ("Ownership split", 8, 6): ("Read and write by the recovery module",
                                "Read and write by the owning service only, in its own rwb_<name> schema"),
    ("Quality measures", 10, 2): ("Every v_ace_* view compiles and no recovery table reads public.*",
                                  "Every v_ace_* view compiles and no rwb_<name> table reads public.*"),
}
a = openpyxl.load_workbook(SRC)
b = openpyxl.load_workbook(OUT)
problems, changed = [], []
print("v3 sheets", a.sheetnames)
print("v4 sheets", b.sheetnames)
if b.sheetnames[0] != "Read me":
    problems.append("Read me is not the first sheet")
for name in a.sheetnames:
    if name not in b.sheetnames:
        problems.append(f"sheet lost: {name}")
        continue
    wa, wb_ = a[name], b[name]
    if wb_.max_row < wa.max_row or wb_.max_column < wa.max_column:
        problems.append(f"{name}: grid shrank {wa.dimensions} -> {wb_.dimensions}")
    for r in range(1, wa.max_row + 1):
        for c in range(1, wa.max_column + 1):
            x, y = wa.cell(row=r, column=c).value, wb_.cell(row=r, column=c).value
            exp = EXPECTED.get((name, r, c))
            if exp:
                if x != exp[0] or y != exp[1]:
                    problems.append(f"{name}!{wa.cell(row=r, column=c).coordinate}: not the planned edit ({x!r} -> {y!r})")
                else:
                    changed.append(f"{name}!{wa.cell(row=r, column=c).coordinate}")
                continue
            if x != y:
                problems.append(f"{name}!{wa.cell(row=r, column=c).coordinate}: changed {x!r} -> {y!r}")
    print(name, "v3", wa.dimensions, "v4", wb_.dimensions, "merged", len(wb_.merged_cells.ranges))
if len(changed) != 3:
    problems.append(f"expected 3 changed cells, found {len(changed)}: {changed}")

# Ownership rows carry owner service and schema
ws = b["Ownership"]
dps = 0
for r in range(5, 19):
    dp = ws.cell(row=r, column=1).value
    own, sch = ws.cell(row=r, column=12).value, ws.cell(row=r, column=13).value
    if not dp or not own or not sch:
        problems.append(f"Ownership row {r}: missing owner service or schema ({dp}, {own}, {sch})")
    dps += 1
print("data products with an owner", dps)
ws = b["Ownership split"]
for r in range(5, 9):
    if not ws.cell(row=r, column=7).value or not ws.cell(row=r, column=8).value:
        problems.append(f"Ownership split tier row {r}: no owning service")

# Read me header and change log
rm = b["Read me"]
lines = [rm.cell(row=i, column=1).value or "" for i in range(1, rm.max_row + 1)]
print("read me line 1:", lines[0])
print("read me line 2:", lines[1])
if lines[0] != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    problems.append("Read me line 1 is not the Template and Rules R8.1 header")
if lines[1] != "(C) Siam Commercial Bank and Henka Pte Ltd":
    problems.append("Read me line 2 is not the Template and Rules R8.1 header")
body = "\n".join(str(x) for x in lines)
for need in ("v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash",
             "D-RCV-60"):
    if need not in body:
        problems.append(f"Read me lacks: {need}")

json.dump({"changed": changed, "problems": problems},
          open("_work/msr/docs/B-DATA-20/verify_v4.json", "w", encoding="utf-8"), indent=1)
print("changed cells", changed)
print("problems", len(problems))
for p in problems:
    print(" -", p)
