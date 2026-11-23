"""Verify the v4 workbook against v3 cell by cell, and check the new blocks and the owners."""
import json
import re
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[4]
V3 = ROOT / "06 Data" / "Recovery Workbench Volume and Scale Forecast v3.xlsx"
V4 = ROOT / "06 Data" / "Recovery Workbench Volume and Scale Forecast v4.xlsx"
OM = ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx"
OUT = Path(__file__).resolve().parent / "verify_v4.json"

DECLARED = {"Read path!A2", "Read path!C15", "Read path!C16", "Inputs!G7", "Key!C10"}
problems, notes = [], []


def norm(v):
    return "" if v is None else str(v).strip()


w3 = openpyxl.load_workbook(V3)
w4 = openpyxl.load_workbook(V4)
o3 = {s: openpyxl.load_workbook(V3)[s] for s in w3.sheetnames}

# 1. every v3 sheet present, in the same relative order, and no v3 sheet lost
for s in w3.sheetnames:
    if s not in w4.sheetnames:
        problems.append(f"sheet lost: {s}")
order = [s for s in w4.sheetnames if s in w3.sheetnames]
if order != w3.sheetnames:
    problems.append(f"v3 sheet order changed: {order}")
notes.append(f"v3 sheets {len(w3.sheetnames)}, v4 sheets {len(w4.sheetnames)}, order kept: {order == w3.sheetnames}")

# 2. cell by cell on the eight v3 sheets: value, number format and style
changed, restyled, cells = [], [], 0
for name, ws3 in o3.items():
    ws4 = w4[name]
    if (ws3.max_row, ws3.max_column) != (ws4.max_row, ws4.max_column):
        problems.append(f"{name}: size changed {ws3.dimensions} -> {ws4.dimensions}")
    for r in range(1, ws3.max_row + 1):
        for c in range(1, ws3.max_column + 1):
            a, b = ws3.cell(r, c), ws4.cell(r, c)
            cells += 1
            ref = f"{name}!{a.coordinate}"
            if norm(a.value) != norm(b.value):
                changed.append(ref)
                if ref not in DECLARED:
                    problems.append(f"{ref}: changed but not declared")
            else:
                if a.number_format != b.number_format:
                    restyled.append(f"{ref} number format {a.number_format} -> {b.number_format}")
                if (a.font.b, a.font.sz) != (b.font.b, b.font.sz):
                    restyled.append(f"{ref} font {(a.font.b, a.font.sz)} -> {(b.font.b, b.font.sz)}")
                if a.fill.fgColor.rgb != b.fill.fgColor.rgb:
                    restyled.append(f"{ref} fill {a.fill.fgColor.rgb} -> {b.fill.fgColor.rgb}")
for ref in DECLARED:
    if ref not in changed:
        problems.append(f"{ref}: declared as changed but equals v3")
notes.append(f"compared {cells} cells on {len(o3)} v3 sheets: {len(changed)} changed, {len(restyled)} restyled")
if restyled:
    problems += restyled[:20]

# 3. new sheets and their order
expected = ["Read me", "Inputs", "Monthly", "Five years", "Users and load", "Read path",
            "Service volumes", "Topics and queues", "ACE growth", "Route activity", "Key"]
if w4.sheetnames != expected:
    problems.append(f"sheet order {w4.sheetnames}")

# 4. Read me
rm = w4["Read me"]
if rm["A1"].value != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    problems.append("Read me A1 header line")
if rm["A2"].value != "(C) Siam Commercial Bank and Henka Pte Ltd":
    problems.append("Read me A2 header line")
LOG = "v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
if rm["A9"].value != LOG:
    problems.append(f"change-log row: {rm['A9'].value!r}")

# 5. owners, topics and queues against the Ownership Map
om = {r[0]: r for r in openpyxl.load_workbook(OM, data_only=True)["Services"].iter_rows(min_row=2, values_only=True)}
sv = w4["Service volumes"]
rows = {sv.cell(r, 1).value: r for r in range(5, 24)}
if sorted(rows) != sorted(om):
    problems.append(f"Service volumes codes {sorted(rows)}")
for code, r in rows.items():
    o = om[code]
    if sv.cell(r, 2).value != o[1]:
        problems.append(f"{code}: service {sv.cell(r, 2).value!r} vs {o[1]!r}")
    if int(sv.cell(r, 3).value) != int(o[3]):
        problems.append(f"{code}: wave {sv.cell(r, 3).value} vs {o[3]}")
    if sv.cell(r, 8).value != o[6]:
        problems.append(f"{code}: topic {sv.cell(r, 8).value!r} vs {o[6]!r}")
    if sv.cell(r, 9).value != o[7]:
        problems.append(f"{code}: queue {sv.cell(r, 9).value!r} vs {o[7]!r}")
    if not sv.cell(r, 5).value:
        problems.append(f"{code}: no volume")
    if not sv.cell(r, 7).value:
        problems.append(f"{code}: no basis")
notes.append(f"Service volumes: {len(rows)} service rows, topic and queue equal to the Ownership Map on all rows")

tq = w4["Topics and queues"]
topics = {tq.cell(r, 1).value: tq.cell(r, 2).value for r in range(6, 26)}
if len(topics) != 20:
    problems.append(f"topic rows {len(topics)}")
for code, o in om.items():
    if o[6] not in topics:
        problems.append(f"topic missing for {code}: {o[6]}")
if "rwb.decision-record.v1 (shared)" not in topics:
    problems.append("shared decision-record topic missing")
for r in range(6, 26):
    if (tq.cell(r, 4).value, tq.cell(r, 5).value, tq.cell(r, 6).value, tq.cell(r, 7).value) != (12, 3, "7 days", "caseId"):
        problems.append(f"topic settings row {r}")
    if not str(tq.cell(r, 10).value).endswith(".dlt"):
        problems.append(f"dead letter row {r}: {tq.cell(r, 10).value}")

wh = None
for r in range(27, tq.max_row + 1):
    if tq.cell(r, 1).value == "Task queue":
        wh = r
        break
queues = {tq.cell(r, 1).value: tq.cell(r, 2).value for r in range(wh + 1, wh + 20) if tq.cell(r, 1).value}
if len(queues) != 19:
    problems.append(f"queue rows {len(queues)}")
for code, o in om.items():
    if queues.get(o[7]) != f"{o[0]} {o[1]}":
        problems.append(f"queue {o[7]} maps to {queues.get(o[7])!r} not '{o[0]} {o[1]}'")
notes.append(f"Topics and queues: {len(topics)} topic rows, {len(queues)} queue rows, all matching the Ownership Map")

# 6. counts and placeholders
pl = [sv.cell(r, 1).value for r in rows.values() if str(sv.cell(r, 5).value).startswith("Not specified")]
notes.append(f"placeholder volumes: {pl}")
cite = re.compile(r"(?:CG|ASM)-B-DATA-26-\d")
allcite = sorted({m.group(0) for ws in w4.worksheets for row in ws.iter_rows() for c in row
                  if isinstance(c.value, str) for m in cite.finditer(c.value)})
notes.append(f"register ids cited in the workbook: {allcite}")

# 7. no person name in the workbook
p = w4.properties
if p.creator != "Recovery Workbench programme":
    problems.append(f"creator not scrubbed: {p.creator!r}")
if p.lastModifiedBy != "T3 Code / OpenCode / DeepSeek v4.1 Flash":
    problems.append(f"lastModifiedBy: {p.lastModifiedBy!r}")
if "Rajdeep" in (p.creator or "") or "Ghai" in (p.creator or ""):
    problems.append("person name in the properties")
susp = [f"{ws.title}!{c.coordinate}" for ws in w4.worksheets for row in ws.iter_rows() for c in row
        if isinstance(c.value, str) and re.search(r"Rajdeep|Ghai", c.value)]
if susp:
    problems.append(f"person name in cells: {susp}")

res = {"changed_cells": sorted(changed), "restyled": restyled[:20], "problems": problems, "notes": notes,
       "result": "PASS" if not problems else "FAIL"}
OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
for n in notes:
    print("..", n)
print("changed:", sorted(changed))
print("PROBLEMS:", len(problems))
for x in problems:
    print(" -", x)
print("RESULT", res["result"])
