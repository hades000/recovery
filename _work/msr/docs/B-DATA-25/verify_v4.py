"""Verify Recovery Workbench Data Quality and Reconciliation Rules v4 against v3 and the Ownership Map."""
import json
import re
from pathlib import Path

import openpyxl

V3 = "06 Data/Recovery Workbench Data Quality and Reconciliation Rules v3.xlsx"
V4 = "06 Data/Recovery Workbench Data Quality and Reconciliation Rules v4.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
DECLARED = {("Reconciliations", "B12"), ("Reconciliations", "C12"), ("Quality measures", "B7")}

problems, changed = [], []

w3, w4 = openpyxl.load_workbook(V3), openpyxl.load_workbook(V4)

# ---------------------------------------------------------------- sheets and header
if w4.sheetnames != ["Read me", "Load checks", "Reconciliations", "Per-service reconciliation", "Quality measures"]:
    problems.append(f"sheet order: {w4.sheetnames}")
rm = w4["Read me"]
if rm["A1"].value != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    problems.append(f"header line 1: {rm['A1'].value!r}")
if rm["A2"].value != "(C) Siam Commercial Bank and Henka Pte Ltd":
    problems.append(f"header line 2: {rm['A2'].value!r}")
cl = [rm.cell(row=r, column=1).value for r in range(1, 12)]
if not any(v == f"v4, 22 November 2026, {DEC} microservice realignment, {TOOL}" for v in cl):
    problems.append("change-log row missing or wrong")
if not any(v and TOOL in v for v in cl):
    problems.append("tool line missing")

# ---------------------------------------------------------------- cell-by-cell
for name in ("Load checks", "Reconciliations", "Quality measures"):
    s3, s4 = w3[name], w4[name]
    for r in range(1, s3.max_row + 1):
        for c in range(1, s3.max_column + 1):
            a, b = s3.cell(row=r, column=c).value, s4.cell(row=r, column=c).value
            if a != b:
                changed.append((name, s3.cell(row=r, column=c).coordinate, a, b))
    for r in range(1, s3.max_row + 1):
        for c in range(1, s3.max_column + 1):
            if s3.cell(row=r, column=c).value is not None and s4.cell(row=r, column=c).value is None:
                problems.append(f"{name}!{s3.cell(row=r, column=c).coordinate} value lost")
for ch in changed:
    if (ch[0], ch[1]) not in DECLARED:
        problems.append(f"undeclared change {ch[0]}!{ch[1]}: {ch[2]!r} -> {ch[3]!r}")
missing = DECLARED - {(c[0], c[1]) for c in changed}
if missing:
    problems.append(f"declared change not made: {sorted(missing)}")

# ---------------------------------------------------------------- Ownership Map
owb = openpyxl.load_workbook(OWN)
svc = {str(r[0]): (str(r[1]), str(r[4])) for r in owb["Services"].iter_rows(min_row=2, values_only=True) if r and r[0]}
tab = {str(r[0]): str(r[1]) for r in owb["Tables"].iter_rows(min_row=2, values_only=True) if r and r[0]}
assert len(svc) == 19

# Reconciliations owner column
rec = w4["Reconciliations"]
if rec["H4"].value != "Owner (D-RCV-60)" or rec["I4"].value != "Per-service reconciliation (D-RCV-60)":
    problems.append(f"Reconciliations headers: {rec['H4'].value!r} {rec['I4'].value!r}")
for r in range(5, 14):
    if not rec.cell(row=r, column=8).value:
        problems.append(f"Reconciliations!H{r} empty")
    if not rec.cell(row=r, column=9).value:
        problems.append(f"Reconciliations!I{r} empty")

# Quality measures owner column
qm = w4["Quality measures"]
if qm["D4"].value != "Owner service (D-RCV-60)":
    problems.append(f"Quality measures header: {qm['D4'].value!r}")
for r in range(5, 11):
    if not qm.cell(row=r, column=4).value:
        problems.append(f"Quality measures!D{r} empty")

# Per-service sheet
ps = w4["Per-service reconciliation"]
head = [ps.cell(row=4, column=c).value for c in range(1, 12)]
if head != ["Service", "Service name", "Schema", "Owns in its schema (Ownership Map, sheet Tables)",
            "Reconciles its own rows, and against what", "Key", "Tolerance", "When",
            "Break and result route", "Pattern", "Basis"]:
    problems.append(f"per-service header: {head}")
codes = []
for r in range(5, 24):
    code = ps.cell(row=r, column=1).value
    codes.append(code)
    if code not in svc:
        problems.append(f"per-service row {r}: unknown service {code!r}")
        continue
    name, schema = svc[code]
    if ps.cell(row=r, column=2).value != name:
        problems.append(f"per-service row {r}: name {ps.cell(row=r, column=2).value!r} != {name!r}")
    if ps.cell(row=r, column=3).value != schema:
        problems.append(f"per-service row {r}: schema {ps.cell(row=r, column=3).value!r} != {schema!r}")
    owns = ps.cell(row=r, column=4).value or ""
    if code == "S1":
        if "CG-B-DATA-25-7" not in owns:
            problems.append("S1 owns cell: placeholder missing")
    else:
        listed = [t.strip() for t in owns.split(",") if t.strip()]
        for t in listed:
            if t not in tab:
                problems.append(f"per-service row {r}: table {t!r} not in the Ownership Map")
            elif tab[t] != code:
                problems.append(f"per-service row {r}: table {t} is owned by {tab[t]}, not {code}")
        expected = sorted(t for t, o in tab.items() if o == code)
        if sorted(listed) != expected:
            problems.append(f"per-service row {r} ({code}): tables differ from the map: {sorted(set(expected) - set(listed))} missing")
if sorted(codes) != sorted(svc):
    problems.append(f"per-service codes: {codes}")

# placeholders must cite a register id
ph = re.compile(r"Not specified in the source documents \(CG-B-DATA-25-\d+; ASM-B-DATA-25-\d+\)")
for row in ps.iter_rows():
    for cell in row:
        if isinstance(cell.value, str) and cell.value.startswith("Not specified"):
            if not ph.search(cell.value):
                problems.append(f"placeholder without citation: {cell.coordinate}")
for sheet in ("Read me", "Per-service reconciliation", "Reconciliations", "Quality measures", "Load checks"):
    for row in w4[sheet].iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and "Not specified in the source documents" in cell.value:
                if not ph.search(cell.value):
                    problems.append(f"{sheet}!{cell.coordinate}: placeholder without citation")

# every cited candidate row must exist in the register files
ids = set()
for kind in ("gaps", "assumptions"):
    for p in Path("_work/msr", kind).glob("B-DATA-25.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                ids.add(json.loads(line)["id"])
cited = set()
for sheet in w4.sheetnames:
    for row in w4[sheet].iter_rows():
        for cell in row:
            if isinstance(cell.value, str):
                cited.update(re.findall(r"\b(?:CG|ASM)-B-DATA-25-\d+\b", cell.value))
for c in sorted(cited):
    if c not in ids:
        problems.append(f"cites {c} but no register row has it")

res = {"changed_cells": len(changed), "changed": [f"{s}!{a}" for s, a, _, _ in changed],
       "services": len(codes), "cited_ids": len(cited), "problems": problems,
       "result": "PASS" if not problems else "FAIL"}
Path("_work/msr/docs/B-DATA-25/verify_v4.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
for c in changed:
    print("CHANGED", c[0], c[1], "->", str(c[3])[:90])
print(json.dumps({k: v for k, v in res.items() if k != "changed"}, indent=1))
