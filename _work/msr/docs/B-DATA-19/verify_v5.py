"""Verify v5 against v4 cell by cell: only the intended additions may differ."""
import json

import openpyxl

V4 = "06 Data/Recovery Workbench Reference Data and Lists of Values v4.xlsx"
V5 = "06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
problems = []

a = openpyxl.load_workbook(V4)
b = openpyxl.load_workbook(V5)

print("v5 sheets", b.sheetnames)
if b.sheetnames != ["Read me", "Lists", "Values", "Reference tables", "Reference data starter",
                    "Change process", "Key"]:
    problems.append("sheet order")

# 1. every original cell unchanged, and its style unchanged
for name in ["Lists", "Values", "Reference tables", "Change process", "Key"]:
    wa, wb_ = a[name], b[name]
    for row in wa.iter_rows():
        for c in row:
            d = wb_[c.coordinate]
            if c.value != d.value:
                problems.append(f"{name}!{c.coordinate}: value {c.value!r} -> {d.value!r}")
            for attr in ("number_format",):
                if getattr(c, attr) != getattr(d, attr):
                    problems.append(f"{name}!{c.coordinate}: {attr} changed")
            if c.font.b != d.font.b or c.font.sz != d.font.sz or c.font.color.rgb != d.font.color.rgb:
                problems.append(f"{name}!{c.coordinate}: font changed")
            if c.fill.patternType != d.fill.patternType:
                problems.append(f"{name}!{c.coordinate}: fill changed")

# 2. Lists: appended columns complete
wa, wb_ = a["Lists"], b["Lists"]
print("Lists dims", wa.max_row, wa.max_column, "->", wb_.max_row, wb_.max_column)
if (wb_.max_row, wb_.max_column) != (142, 10):
    problems.append("Lists shape")
heads = [wb_.cell(row=4, column=c).value for c in range(7, 11)]
if heads != ["Owning service (D-RCV-60)", "Owning schema (D-RCV-60)",
             "Shared-list route (D-RCV-60)", "Basis (D-RCV-60)"]:
    problems.append(f"Lists headers {heads}")
for r in range(5, 143):
    for c in range(7, 11):
        if not wb_.cell(row=r, column=c).value:
            problems.append(f"Lists!{wb_.cell(row=r, column=c).coordinate} empty")
if wb_.auto_filter.ref != "A4:J142":
    problems.append(f"Lists autofilter {wb_.auto_filter.ref}")

# 3. Reference tables
wa, wb_ = a["Reference tables"], b["Reference tables"]
print("Reference tables dims", wa.max_row, wa.max_column, "->", wb_.max_row, wb_.max_column)
if (wb_.max_row, wb_.max_column) != (18, 9):
    problems.append("Reference tables shape")
for r in range(5, 19):
    for c in range(6, 10):
        if not wb_.cell(row=r, column=c).value:
            problems.append(f"Reference tables!{wb_.cell(row=r, column=c).coordinate} empty")
if wb_.auto_filter.ref != "A4:I18":
    problems.append(f"Reference tables autofilter {wb_.auto_filter.ref}")

# 4. starter
st = b["Reference data starter"]
head = [st.cell(row=6, column=c).value for c in range(1, 9)]
exp = ["Service", "Service name", "Service wave", "Starter item", "Item kind", "Starter mode",
       "Route (D-RCV-60)", "Basis (D-RCV-60)"]
if head != exp:
    problems.append(f"starter header {head}")
rows = 0
for r in range(7, st.max_row + 1):
    if st.cell(row=r, column=1).value in (None, ""):
        continue
    if str(st.cell(row=r, column=1).value).startswith("Counts:"):
        continue
    rows += 1
    for c in range(1, 9):
        if not st.cell(row=r, column=c).value:
            problems.append(f"starter r{r}c{c} empty")
print("starter data rows", rows, "expected 179")
if rows != 179:
    problems.append("starter row count")
d = json.load(open("_work/msr/docs/B-DATA-19/derive.json", encoding="utf-8"))
codes = {i["code"] for i in d["items"]}
for r in range(7, 7 + 179):
    item = st.cell(row=r, column=4).value
    if str(item).startswith("LOV-") and item not in codes:
        problems.append(f"starter unknown item {item}")
    mode = st.cell(row=r, column=6).value
    if mode not in ("Load", "Read"):
        problems.append(f"starter mode {mode}")

# 5. Read me
rm = b["Read me"]
print("read me rows", rm.max_row)
if rm["A1"].value != "SCB Collections and Recovery. Henka Group, 22 November 2026.":
    problems.append("read me line 1")
if rm["A2"].value != "(C) Siam Commercial Bank and Henka Pte Ltd":
    problems.append("read me line 2")
txt = "\n".join(str(c.value) for row in rm.iter_rows() for c in row if c.value)
if "v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" not in txt:
    problems.append("change log row")
if DEC not in txt or TOOL not in txt:
    problems.append("decision or tool missing")

# 6. change process and key rows
print("change process max_row", b["Change process"].max_row, "Key max_row", b["Key"].max_row)
if b["Change process"].max_row != 13:
    problems.append("change process rows")
if b["Key"].max_row != 16:
    problems.append("key rows")
if b["Change process"]["B13"].value != "Shared list":
    problems.append("step 9 stage")

# 7. properties
print("props", b.properties.creator, "|", b.properties.lastModifiedBy, "|", b.properties.title)
if "Rajdeep" in str(b.properties.creator):
    problems.append("creator still a person name")

# 8. no person name or tracker word anywhere
bad = []
for ws in b.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str):
                low = c.value.lower()
                if "jira" in low or "atlassian" in low or "@" in low and "." in low and " " not in low.split("@")[0]:
                    bad.append((ws.title, c.coordinate, c.value[:60]))
if bad:
    problems.append(f"suspicious cells {bad[:5]}")

print("\nPROBLEMS", len(problems))
for p in problems[:40]:
    print(" -", p)
json.dump(problems, open("_work/msr/docs/B-DATA-19/verify_v5.json", "w", encoding="utf-8"), indent=1)
