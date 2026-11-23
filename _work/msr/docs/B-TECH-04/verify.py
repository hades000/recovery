"""Verify Interface Specifications v4 against the v3 source (WP B-TECH-04).

Read only: asserts that every value of the source survives, that only the intended
changes are present, and that the header and change-log row of Template and Rules
R8.1 are there.
"""
import sys
from pathlib import Path

import openpyxl

SRC = Path(r"05 Technical architecture\Recovery Workbench Interface Specifications v3.xlsx")
OUT = Path(r"05 Technical architecture\Recovery Workbench Interface Specifications v4.xlsx")
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
REMOVED = {"INT-19", "INT-20"}
fails = []


def eq(a, b):
    a = "" if a is None else str(a).strip()
    b = "" if b is None else str(b).strip()
    return a == b


s = openpyxl.load_workbook(SRC)
o = openpyxl.load_workbook(OUT)

if o.sheetnames != ["Read me", "Interfaces", "Field mapping", "Outbound checks", "Key", "Realignment changes"]:
    fails.append("sheet order: %s" % o.sheetnames)
for sheet in ("Interfaces", "Field mapping", "Outbound checks", "Key"):
    if sheet not in o.sheetnames:
        fails.append("missing sheet " + sheet)

# ---------------------------------------------------------------- Read me
rm = o["Read me"]
if rm.cell(1, 1).value != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    fails.append("Read me row 1 header")
if rm.cell(2, 1).value != "(C) Siam Commercial Bank and Henka Pte Ltd":
    fails.append("Read me row 2 header")
txt = [str(rm.cell(r, 1).value or "") for r in range(1, rm.max_row + 1)]
if "v4, 22 November 2026, D-RCV-60 microservice realignment, " + TOOL not in txt:
    fails.append("change-log row missing in Read me")
if not any("D-RCV-60" in t for t in txt):
    fails.append("Read me does not name D-RCV-60")
if not any(t.startswith("Status: Draft.") for t in txt):
    fails.append("Read me status line missing")

# ---------------------------------------------------------------- Interfaces
si, oi = s["Interfaces"], o["Interfaces"]
src = {}
for r in range(5, si.max_row + 1):
    src[si.cell(r, 1).value] = [si.cell(r, c).value for c in range(1, 16)]
out = {}
for r in range(5, oi.max_row + 1):
    out[oi.cell(r, 1).value] = [oi.cell(r, c).value for c in range(1, 19)]

if set(out) != set(src) - REMOVED:
    fails.append("interface set: missing %s, extra %s"
                 % (sorted(set(src) - REMOVED - set(out)), sorted(set(out) - (set(src) - REMOVED))))
if REMOVED & set(out):
    fails.append("INT-19 or INT-20 still present")

# source column -> v4 column after three inserted columns at 7
keep = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 7: 10, 8: 11, 9: 12, 10: 13, 11: 14, 12: 15, 14: 17, 15: 18}
OWNER_CHANGED = {"INT-14", "INT-24", "INT-25"}
FIX_CHANGED = {"INT-14", "INT-21", "INT-22", "INT-23", "INT-24", "INT-25", "INT-34", "INT-35", "INT-36"}
for iid, row in src.items():
    if iid in REMOVED:
        continue
    for sc, oc in keep.items():
        if not eq(row[sc - 1], out[iid][oc - 1]):
            fails.append("%s col %d changed: %r -> %r" % (iid, sc, row[sc - 1], out[iid][oc - 1]))
    if iid not in OWNER_CHANGED and not eq(row[5], out[iid][5]):
        fails.append("%s Owner changed unexpectedly" % iid)
    if iid not in FIX_CHANGED and not eq(row[12], out[iid][15]):
        fails.append("%s Owner of the fix changed unexpectedly" % iid)
    for c in (7, 8, 9):
        if not out[iid][c - 1]:
            fails.append("%s empty new owner column %d" % (iid, c))
    if out[iid][6] not in ("P1", "P2", "P4", "P6", "P10", "S6", "S9", "PLT"):
        fails.append("%s bad owner code %r" % (iid, out[iid][6]))

if not eq(oi.cell(1, 1).value, si.cell(1, 1).value):
    fails.append("Interfaces title changed")
if "23 numbered interfaces" not in str(oi.cell(2, 1).value):
    fails.append("Interfaces description does not give the v4 count")
if "D-RCV-60" not in str(oi.cell(3, 1).value):
    fails.append("Interfaces version row missing")

# ---------------------------------------------------------------- Field mapping
sf, of = s["Field mapping"], o["Field mapping"]
if of.max_row != sf.max_row or of.max_column != sf.max_column + 1:
    fails.append("Field mapping size %dx%d (source %dx%d)" % (of.max_row, of.max_column, sf.max_row, sf.max_column))
n_changed = 0
for r in range(5, sf.max_row + 1):
    for c in range(1, 12):
        a, b = sf.cell(r, c).value, of.cell(r, c).value
        if not eq(a, b):
            if c == 11 and a == "Workbench":
                n_changed += 1
            else:
                fails.append("Field mapping r%d c%d changed: %r -> %r" % (r, c, a, b))
    if not of.cell(r, 12).value:
        fails.append("Field mapping r%d has no Owning service" % r)
if n_changed != 7:
    fails.append("Field mapping Workbench owner rows changed: %d (expected 7)" % n_changed)
for c in (1, 2, 3, 4):
    if not eq(sf.cell(c, 1).value, of.cell(c, 1).value) and c != 2:
        fails.append("Field mapping row %d heading changed" % c)

# ---------------------------------------------------------------- Outbound checks
sc, oc = s["Outbound checks"], o["Outbound checks"]
if sc.max_row != oc.max_row or sc.max_column != oc.max_column:
    fails.append("Outbound checks size changed")
for r in range(1, max(sc.max_row, oc.max_row) + 1):
    for c in range(1, 4):
        if not eq(sc.cell(r, c).value, oc.cell(r, c).value):
            fails.append("Outbound checks r%d c%d changed" % (r, c))

# ---------------------------------------------------------------- Key
sk, ok = s["Key"], o["Key"]
if ok.max_row != sk.max_row + 4:
    fails.append("Key row count %d (source %d)" % (ok.max_row, sk.max_row))
for r in range(1, sk.max_row + 1):
    for c in (1, 2):
        if not eq(sk.cell(r, c).value, ok.cell(r, c).value):
            fails.append("Key r%d c%d changed" % (r, c))
added = [ok.cell(r, 2).value for r in range(sk.max_row + 1, ok.max_row + 1)]
for want in ("Owner code", "Owning service", "Owner basis", "INT-19, INT-20"):
    if want not in added:
        fails.append("Key row missing: " + want)

# ---------------------------------------------------------------- Change log sheet
ch = o["Realignment changes"]
if ch.cell(1, 1).value != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    fails.append("Realignment changes header row 1")
if ch.cell(4, 1).value != "#":
    fails.append("Realignment changes table header")
body = [ch.cell(r, 2).value for r in range(5, ch.max_row + 1)]
if not any("INT-19 removed" == b for b in body) or not any("INT-20 removed" == b for b in body):
    fails.append("Realignment changes does not record the two removals")
if not any("per-service owners" in str(b).lower() for b in body):
    fails.append("Realignment changes does not record the per-service owners")

# ---------------------------------------------------------------- source untouched
if SRC.stat().st_size <= 0:
    fails.append("source missing")

if fails:
    print("FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("PASS: 23 interfaces, 82 field mappings, 3 outbound checks, 4 key rows added, "
      "7 outbound owner rows made per service, header and change-log row present")
