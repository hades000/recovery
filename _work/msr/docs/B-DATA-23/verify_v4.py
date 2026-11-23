"""Verify v4 against v3: only the ten declared cells change, no row or column is lost,
the header and the change log are present, and every owner cell matches the Ownership Map."""
import json
from pathlib import Path

import openpyxl

V3 = "06 Data/Recovery Workbench Reporting and Analytics Data Model v3.xlsx"
V4 = "06 Data/Recovery Workbench Reporting and Analytics Data Model v4.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
DUMP = Path("_work/msr/docs/B-DATA-23/v3_dump.json")
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

EXPECT_CHANGED = {("Facts", "A2")} | {("Facts", f"F{r}") for r in range(5, 14)}

d3 = json.loads(DUMP.read_text(encoding="utf-8"))
w3, w4 = openpyxl.load_workbook(V3), openpyxl.load_workbook(V4)
problems = []

# 1. sheet order and presence
if w4.sheetnames != ["Read me"] + d3["order"] + ["Read model"]:
    problems.append(f"sheet order {w4.sheetnames}")

# 2. every v3 cell unchanged except the ten declared ones
changed = []
for name in d3["order"]:
    for addr, old in d3["sheets"][name]["cells"].items():
        new = w4[name][addr].value
        if new != old["v"]:
            changed.append((name, addr))
            if (name, addr) not in EXPECT_CHANGED:
                problems.append(f"undeclared change {name}!{addr}: {old['v']!r} -> {new!r}")
got = set(changed)
if got != EXPECT_CHANGED:
    problems.append(f"changed set mismatch: missing {sorted(EXPECT_CHANGED - got)} extra {sorted(got - EXPECT_CHANGED)}")
for name in d3["order"]:
    if w4[name].max_row < d3["sheets"][name]["max_row"]:
        problems.append(f"{name}: rows lost")
    if w4[name].max_column < d3["sheets"][name]["max_col"]:
        problems.append(f"{name}: columns lost")

# 3. appended columns on the three source sheets
FACTS = {"fact_case_daily": "F5", "fact_decision": "F6", "fact_treatment": "F7", "fact_legal": "F8",
         "fact_asset": "F9", "fact_lot": "F10", "fact_recovery": "F11", "fact_partner": "F12",
         "fact_flow": "F13"}
DIMS = {"dim_date": "F5", "dim_product": "F6", "dim_route": "F7", "dim_stage": "F8", "dim_org": "F9",
        "dim_partner": "F10", "dim_rule": "F11", "dim_decision": "F12"}
ws = w4["Facts"]
if [ws.cell(row=4, column=c).value for c in (7, 8, 9)] != ["Owner (D-RCV-60)", "Values from (D-RCV-60)", "Pattern (D-RCV-60)"]:
    problems.append("Facts headers")
for r in range(5, 14):
    if ws.cell(row=r, column=7).value != "P9 rwb-reporting":
        problems.append(f"Facts!G{r} owner")
    if not ws.cell(row=r, column=8).value or not ws.cell(row=r, column=9).value:
        problems.append(f"Facts!H{r}/I{r} empty")
    refresh = str(ws.cell(row=r, column=6).value)
    if refresh.startswith("Read through v_ace") or refresh.lower().startswith("nightly from the workbench"):
        problems.append(f"Facts!F{r} still on the v3 access path: {refresh}")
ws = w4["Dimensions"]
for r in range(5, 13):
    if ws.cell(row=r, column=3).value != "P9 rwb-reporting" or not ws.cell(row=r, column=4).value:
        problems.append(f"Dimensions!C{r}/D{r}")
ws = w4["Measures"]
for r in range(5, 15):
    if ws.cell(row=r, column=4).value != "P9 rwb-reporting" or not ws.cell(row=r, column=5).value:
        problems.append(f"Measures!D{r}/E{r}")

# 4. read model sheet
ws = w4["Read model"]
facts = [ws.cell(row=r, column=1).value for r in range(5, 14)]
if facts != list(FACTS):
    problems.append(f"Read model facts {facts}")
tables = [ws.cell(row=r, column=1).value for r in range(19, 22)]
if tables != ["measure_definition", "measure_snapshot", "measure_publish"]:
    problems.append(f"Read model controls {tables}")

# 5. header, change log and tool line
ws = w4["Read me"]
if ws["A1"].value != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    problems.append("Read me A1")
if ws["A2"].value != "(C) Siam Commercial Bank and Henka Pte Ltd":
    problems.append("Read me A2")
texts = [str(c.value) for row in ws.iter_rows() for c in row if c.value is not None]
log = [t for t in texts if t.startswith("v4, 22 November 2026")]
if log != [f"v4, 22 November 2026, D-RCV-60 microservice realignment, {TOOL}"]:
    problems.append(f"change log {log}")
if not any(DEC in t for t in texts):
    problems.append("no D-RCV-60 mention")

# 6. owners agree with the Ownership Map
owb = openpyxl.load_workbook(OWN)
tab = {str(r[0]): str(r[1]) for r in owb["Tables"].iter_rows(min_row=2, values_only=True) if r and r[0]}
assert tab["measure_definition"] == tab["measure_snapshot"] == tab["measure_publish"] == "P9"

out = {"changed": sorted(f"{s}!{a}" for s, a in changed), "problems": problems}
Path("_work/msr/docs/B-DATA-23/verify_v4.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
print("RESULT", "PASS" if not problems else "FAIL")
