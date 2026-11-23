"""Verify v4 against v3: nothing lost, nothing changed outside the appended cells."""
import sys
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "06 Data" / "Recovery Workbench Party and Customer Master Data Design v3.xlsx"
OUT = ROOT / "06 Data" / "Recovery Workbench Party and Customer Master Data Design v4.xlsx"
problems = []

src = openpyxl.load_workbook(SRC)
out = openpyxl.load_workbook(OUT)


def sig(c):
    fill = c.fill.fgColor.rgb if c.fill and c.fill.patternType else None
    return (c.value, c.font.bold, c.font.sz, fill, c.alignment.wrap_text, c.alignment.vertical)


# 1. every source cell, value and style, in the same coordinate
for name in ("Party fields", "Match rules"):
    a, b = src[name], out[name]
    for r in range(1, a.max_row + 1):
        for c in range(1, a.max_column + 1):
            if sig(a.cell(r, c)) != sig(b.cell(r, c)):
                problems.append(f"{name}!{a.cell(r, c).coordinate}: {sig(a.cell(r, c))} -> {sig(b.cell(r, c))}")
    for k, v in a.column_dimensions.items():
        if v.width is not None and b.column_dimensions[k].width != v.width:
            problems.append(f"{name} column {k} width {v.width} -> {b.column_dimensions[k].width}")

if src.sheetnames != [s for s in out.sheetnames if s in src.sheetnames]:
    problems.append(f"source sheets missing or renamed: {src.sheetnames} vs {out.sheetnames}")

# 2. header lines and change log
readme = out["Read me"]
if readme["A1"].value != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    problems.append("Read me A1 header line missing")
if readme["A2"].value != "(C) Siam Commercial Bank and Henka Pte Ltd":
    problems.append("Read me A2 header line missing")
log = "v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
if log not in [readme.cell(r, 1).value for r in range(1, readme.max_row + 1)]:
    problems.append("change-log row missing")

# 3. appended columns
pf = out["Party fields"]
if [pf.cell(4, c).value for c in (8, 9, 10)] != ["Owning service", "Target schema", "Access rule"]:
    problems.append(f"Party fields headers H4:J4 = {[pf.cell(4, c).value for c in (8, 9, 10)]}")
owners = {"case_party": (6, "P3"), "v_ace_customer": (13, "P1"), "party_ext": (5, "P1"), "v_ace_contact": (9, "P1"),
          "v_ace_ca_relation": (5, "P1"), "contact_point_ext": (7, "P1"), "partner": (7, "S9")}
seen = {}
for r in range(5, pf.max_row + 1):
    ent, code, schema, rule = (pf.cell(r, c).value for c in (1, 8, 9, 10))
    seen[ent] = seen.get(ent, 0) + 1
    if not all((code, schema, rule)):
        problems.append(f"Party fields row {r} ({ent}) has an empty new cell")
    if ent in owners and code != owners[ent][1]:
        problems.append(f"Party fields row {r} ({ent}) owner {code} != {owners[ent][1]}")
if seen != {k: v[0] for k, v in owners.items()}:
    problems.append(f"entity counts changed: {seen}")

mr = out["Match rules"]
if [mr.cell(4, c).value for c in (5, 6)] != ["Target component", "Owning service"]:
    problems.append(f"Match rules headers E4:F4 = {[mr.cell(4, c).value for c in (5, 6)]}")
if [mr.cell(r, 6).value for r in range(5, 10)] != ["P1", "P1", "P1", "P1", "S9"]:
    problems.append(f"Match rules owners = {[mr.cell(r, 6).value for r in range(5, 10)]}")

# 4. new sheets
so = out["Service ownership"]
if so["A1"].value != "Service ownership" or so["A4"].value != "Code":
    problems.append("Service ownership title or header row missing")
tot = [so.cell(r, 8).value for r in range(5, so.max_row + 1)]
if sum(v for v in tot if isinstance(v, int) and so.cell(so.max_row, 2).value == "Total" and True) is None:
    pass
data_rows = [r for r in range(5, so.max_row + 1) if so.cell(r, 2).value != "Total"]
if sum(so.cell(r, 8).value for r in data_rows) != 52:
    problems.append(f"Service ownership field sum = {sum(so.cell(r, 8).value for r in data_rows)}")

rp = out["Read paths"]
if rp["A1"].value != "Read paths" or rp["A4"].value != "Consumer":
    problems.append("Read paths title or header row missing")
if rp.max_row != 14:
    problems.append(f"Read paths rows = {rp.max_row}")

# 5. properties
if out.properties.creator and out.properties.creator != "Recovery Workbench programme":
    problems.append(f"creator not scrubbed: {out.properties.creator}")

print(f"problems: {len(problems)}")
for p in problems[:40]:
    print(" -", p)
sys.exit(1 if problems else 0)
