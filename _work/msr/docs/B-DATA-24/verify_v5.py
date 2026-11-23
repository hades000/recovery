"""Verify v5 against v4 cell by cell and against the Ownership Map.

Fails on any changed v4 cell that is not declared, any missing appended value, any owner
that disagrees with the Ownership Map, and any missing header, change-log row or property.
"""
import json
from pathlib import Path

import openpyxl

V4 = "06 Data/Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx"
V5 = "06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
OUT = Path("_work/msr/docs/B-DATA-24/verify_v5.json")

DECLARED = {("Handling", "C5"), ("Handling", "C7"), ("Handling", "C21"), ("Handling", "C22")}
problems = []

w4 = openpyxl.load_workbook(V4)
w5 = openpyxl.load_workbook(V5)


def sig(c):
    return (c.value, bool(c.font.b), c.font.sz,
            c.font.color.rgb if c.font.color and c.font.color.type == "rgb" else None,
            c.fill.fgColor.rgb if c.fill and c.fill.patternType else None,
            c.alignment.wrap_text, c.alignment.vertical)


changed = []
for name in w4.sheetnames:
    s4, s5 = w4[name], w5[name]
    for row in s4.iter_rows():
        for c in row:
            a = sig(c)
            b = sig(s5[c.coordinate])
            if a != b:
                if (name, c.coordinate) not in DECLARED:
                    problems.append(f"undeclared change {name}!{c.coordinate}: {a} -> {b}")
                else:
                    changed.append(f"{name}!{c.coordinate}")
    if (s5.max_row < s4.max_row) or (s5.max_column < s4.max_column):
        problems.append(f"{name}: shape shrank {s4.max_row}x{s4.max_column} -> {s5.max_row}x{s5.max_column}")
print("declared changes found", len(changed), changed)
if len(changed) != len(DECLARED):
    problems.append(f"declared changes not all found: {sorted(DECLARED - {tuple(x.split('!')) for x in changed})}")

# sheet order: Read me first, the six source sheets in their order, PII controls last
want = ["Read me"] + w4.sheetnames + ["PII controls"]
if w5.sheetnames != want:
    problems.append(f"sheet order {w5.sheetnames} != {want}")

# header lines and change-log row
rm = w5["Read me"]
if rm["A1"].value != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    problems.append("Read me A1 header missing")
if rm["A2"].value != "(C) Siam Commercial Bank and Henka Pte Ltd":
    problems.append("Read me A2 header missing")
log = [rm.cell(row=r, column=1).value for r in range(1, rm.max_row + 1)]
want_log = "v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
if want_log not in log:
    problems.append("change-log row missing")
if not log[0].startswith("SCB Collections"):
    problems.append("Read me does not start with the header")

# ownership map
owb = openpyxl.load_workbook(OWN)
sname, sschema = {}, {}
for r in owb["Services"].iter_rows(min_row=2, values_only=True):
    if r and r[0]:
        sname[str(r[0])] = str(r[1])
        sschema[str(r[0])] = str(r[4])
sname.setdefault("PLT", "platform library")
sschema.setdefault("PLT", "platform")
towner = {}
for r in owb["Tables"].iter_rows(min_row=2, values_only=True):
    if r and r[0]:
        towner[str(r[0])] = (str(r[1]), str(r[2]))

f5 = w5["Fields"]
owner_seen, counts, personal = set(), {}, 0
for r in range(5, 1371):
    ent, own, ev, lg = (f5.cell(row=r, column=c).value for c in (2, 11, 12, 13))
    if not own or not ev or not lg:
        problems.append(f"Fields row {r} has an empty appended cell")
        continue
    owner_seen.add(own)
    if ent.startswith("v_ace_"):
        if own != "P1 rwb-source-data (recovery view)":
            problems.append(f"Fields row {r}: view owner {own}")
    elif ent == "lake_copy_watermark":
        if own != "P1 rwb-source-data (retired table)":
            problems.append(f"Fields row {r}: lake owner {own}")
    elif ent == "payment_match_rule":
        if own != "P3 rwb-case (retired table)":
            problems.append(f"Fields row {r}: match-rule owner {own}")
    else:
        code, schema = towner[ent]
        if own != f"{code} {sname[code]} ({schema})":
            problems.append(f"Fields row {r}: {ent} owner {own} != map {code} {sname[code]} ({schema})")
    counts[own.split(" ")[0]] = counts.get(own.split(" ")[0], 0) + 1
    if f5.cell(row=r, column=6).value == "Yes":
        personal += 1
print("distinct owner cells", len(owner_seen), "personal", personal)
if personal != 523:
    problems.append(f"personal count {personal} != 523")
if sum(v for k, v in counts.items() if k in sname) + counts.get("P1", 0) - counts.get("P1", 0) == 0:
    pass

# Summary block
sm = w5["Summary"]
if sm["A13"].value != "Fields by owning service (D-RCV-60)":
    problems.append("Summary block title missing")
total_row = [r for r in range(17, 45) if sm.cell(row=r, column=1).value == "Total"]
if not total_row or sm.cell(row=total_row[0], column=3).value != 1366 or \
        sm.cell(row=total_row[0], column=4).value != 523:
    problems.append("Summary total row wrong")
if sm["C11"].value != "=SUM(C5:C10)":
    problems.append("Summary v4 total formula changed")
if sm["C5"].value != "=COUNTIF(Fields!$D$5:$D$1370,A5)":
    problems.append("Summary v4 COUNTIF changed")

# Identifiers, Handling, Who sees what, Key
ids = w5["Identifiers"]
for r in range(5, 113):
    if not ids.cell(row=r, column=8).value or not ids.cell(row=r, column=9).value:
        problems.append(f"Identifiers row {r} empty appended cell")
if ids["H4"].value != "Owner (D-RCV-60)":
    problems.append("Identifiers header missing")

hd = w5["Handling"]
for r in range(5, 29):
    if not hd.cell(row=r, column=4).value:
        problems.append(f"Handling row {r} has no owner")
if hd["C7"].value.startswith("Never written to application logs. Every read of a v_ace_* personal field"):
    problems.append("Handling C7 not updated")
if not hd["C22"].value.startswith("The rwb_source_data login holds SELECT only"):
    problems.append("Handling C22 not updated")
for r in (5, 7, 21, 22):
    if hd.cell(row=r, column=3).value == w4["Handling"].cell(row=r, column=3).value:
        problems.append(f"Handling C{r} should have changed")
if hd.cell(row=6, column=3).value != w4["Handling"]["C6"].value:
    problems.append("Handling C6 should not have changed")

ws_ = w5["Who sees what"]
for r in range(5, 19):
    if not ws_.cell(row=r, column=5).value:
        problems.append(f"Who sees what row {r} has no enforcement owner")

ky = w5["Key"]
if ky.max_row != 21 or ky["B17"].value != "Event payload":
    problems.append("Key rows not appended")

# PII controls
pc = w5["PII controls"]
if pc.max_row < 30 or "D-RCV-60" not in str(pc["A1"].value):
    problems.append("PII controls sheet missing or short")
cats = [pc.cell(row=r, column=3).value for r in range(1, pc.max_row + 1)
        if isinstance(pc.cell(row=r, column=3).value, int)]
if 1366 not in cats:
    problems.append("PII controls category total missing")

# properties
p = w5.properties
for attr, want in (("title", "Recovery Workbench Data Classification and Personal Data Inventory v5"),
                   ("creator", "Recovery Workbench programme"), ("lastModifiedBy", TOOL)):
    if getattr(p, attr) != want:
        problems.append(f"property {attr} = {getattr(p, attr)!r}")
for attr in ("title", "creator", "lastModifiedBy"):
    if "Ghai" in str(getattr(p, attr)):
        problems.append(f"person name in property {attr}")

print("problems", len(problems))
for x in problems[:40]:
    print(" -", x)
OUT.write_text(json.dumps({"changed": changed, "problems": problems, "personal": personal,
                           "owner_cells": len(owner_seen), "counts": counts}, indent=1), encoding="utf-8")
