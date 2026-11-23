"""Verify the v3 agent catalog against the v2 source (D-RCV-60). Read-only."""
import json
import re
from pathlib import Path

import openpyxl

SRC = Path(r"08 AI and agents\Recovery Workbench Agent Catalog and Specifications v2.xlsx")
OUT = Path(r"08 AI and agents\Recovery Workbench Agent Catalog and Specifications v3.xlsx")
WORK = Path("_work/msr")

H1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
H2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
CHANGE = "v3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"

fails = []
src = openpyxl.load_workbook(SRC)
out = openpyxl.load_workbook(OUT)

if out.sheetnames != ["Read me", "Agents", "Decision steps", "Agents v3", "Service summary",
                      "Realignment changes"]:
    fails.append("sheet order %s" % out.sheetnames)
if src.sheetnames != ["Agents", "Decision steps"]:
    fails.append("source sheet order changed: %s" % src.sheetnames)

# 1. source sheets identical cell for cell
for name in ("Agents", "Decision steps"):
    a, b = src[name], out[name]
    if (a.max_row, a.max_column) != (b.max_row, b.max_column):
        fails.append("%s: dimensions differ %s vs %s" % (name, (a.max_row, a.max_column), (b.max_row, b.max_column)))
        continue
    diff = 0
    for r in range(1, a.max_row + 1):
        for c in range(1, a.max_column + 1):
            if a.cell(r, c).value != b.cell(r, c).value:
                diff += 1
                if diff <= 5:
                    fails.append("%s!%s%d differs: %r vs %r" % (name, openpyxl.utils.get_column_letter(c), r,
                                                                a.cell(r, c).value, b.cell(r, c).value))
    print("%s: %d rows, %d columns, %d cell differences" % (name, a.max_row, a.max_column, diff))

# 2. Read me header, change row, status
rm = out["Read me"]
print("Read me A1:", rm["A1"].value)
print("Read me A2:", rm["A2"].value)
if rm["A1"].value != H1:
    fails.append("Read me A1 is not the R8.1 header line 1")
if rm["A2"].value != H2:
    fails.append("Read me A2 is not the R8.1 header line 2")
cells = [c.value for row in rm.iter_rows() for c in row if c.value]
if CHANGE not in cells:
    fails.append("change-log row missing or wrong")
if not any(str(v).startswith("Status: Draft") for v in cells):
    fails.append("status row missing")

# 3. Agents v3: 12 rows, every v2 behaviour word kept, owner resolvable
agents = {r[0].value: [c.value for c in r] for r in src["Agents"].iter_rows(min_row=5, max_row=16)}
v3 = out["Agents v3"]
rows = [[c.value for c in r] for r in v3.iter_rows(min_row=5, max_row=v3.max_row)]
print("Agents v3 rows:", len(rows))
if len(rows) != 12:
    fails.append("Agents v3 row count %d" % len(rows))
svc_codes = {}
for row in rows:
    name = row[0]
    if name not in agents:
        fails.append("unknown agent %r" % name)
        continue
    v2 = agents[name]
    # v2: Agent + 9 behaviour columns; v3 keeps them at 1 and 7..15
    if row[1] is None or row[2] is None:
        fails.append("%s: no owning service" % name)
    if row[6:15] != v2[1:10]:
        fails.append("%s: behaviour columns changed" % name)
    if not re.match(r"^RWB-SVC-(P\d{1,2}|S\d)$", row[4] or ""):
        fails.append("%s: bad service epic %r" % (name, row[4]))
    svc_codes.setdefault(row[1], 0)
    svc_codes[row[1]] += 1
print("service codes:", svc_codes)
if sum(svc_codes.values()) != 12:
    fails.append("owner counts do not sum to 12")

# 4. Service summary total
ss = out["Service summary"]
tot = [r for r in ss.iter_rows(min_row=5, values_only=True) if not r[0] and r[6] is not None and str(r[6]).isdigit() and str(r[6]) == "12"]
print("summary total row:", tot[-1] if tot else None)
if not tot or str(tot[-1][6]) != "12":
    fails.append("Service summary total is not 12")

# 5. citations resolve to jsonl rows
ids_g = {json.loads(l)["id"] for l in (WORK / "gaps" / "B-AI-31.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
ids_a = {json.loads(l)["id"] for l in (WORK / "assumptions" / "B-AI-31.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
ids = ids_g | ids_a
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
found = set()
for ws in out.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str):
                found.update(cite.findall(c.value))
print("cited:", sorted(found))
print("rows:", sorted(ids))
for x in sorted(found - ids):
    fails.append("cites %s with no jsonl row" % x)
for x in sorted(ids - found):
    fails.append("jsonl row %s is never cited in the workbook" % x)

# 6. counts
print("gaps", len(ids_g), "assumptions", len(ids_a))
print()
if fails:
    print("FAIL", len(fails))
    for f in fails:
        print(" -", f)
    raise SystemExit(1)
print("PASS: v3 matches v2 on both source sheets; header, change log, owners and citations check out.")
