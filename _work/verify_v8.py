import re, os, openpyxl, collections

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
X = os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.xlsx")
MD = os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.md")
SCHEMA = os.path.join(ROOT, "06 Data", "Recovery Workbench Physical Schema v5.sql")

sql = open(SCHEMA, encoding="utf-8-sig", errors="replace").read()
tables = set(re.findall(r"(?m)^CREATE TABLE\s+\"?([a-z0-9_]+)\"?", sql, re.I))
views = set(re.findall(r"(?m)^CREATE (?:OR REPLACE )?VIEW\s+(?:recovery\.)?\"?([a-z0-9_]+)\"?", sql, re.I))
known = tables | views

wb = openpyxl.load_workbook(X, read_only=True)
print("SHEETS", wb.sheetnames)
for ws in wb.worksheets:
    print(ws.title, "rows", ws.max_row, "cols", ws.max_column)

st = wb["Stories"]
rows = [r for r in st.iter_rows(min_row=5, values_only=True) if r[0]]
print("STORIES", len(rows))
bad = []
for r in rows:
    for e in [x.strip() for x in (r[8] or "").split(",") if x.strip()]:
        if e not in known:
            bad.append((r[0], e))
print("UNRESOLVED ENTITIES", len(bad), bad[:10])
print("criteria sum", sum(int(r[11]) for r in rows), "tests sum", sum(int(r[12]) for r in rows))

ac = wb["Acceptance criteria"]
acrows = [r for r in ac.iter_rows(min_row=5, values_only=True) if r[0]]
print("AC ROWS", len(acrows), "GHERKIN ACS", sum(len(re.findall(r"(?m)^  Scenario: AC\d+", r[2] or "")) for r in acrows))

tc = wb["Test cases"]
tcrows = [r for r in tc.iter_rows(min_row=5, values_only=True) if r[0]]
print("TC ROWS", len(tcrows), "UNIQUE", len(set(r[0] for r in tcrows)))
print("TC covers missing", [r[0] for r in tcrows if not r[2]])

tr = wb["Traceability"]
trrows = [r for r in tr.iter_rows(min_row=5, values_only=True) if r[0]]
print("TRACE", len(trrows), "REQ ids", len(set(r[2] for r in trrows)))

dp = wb["Dependencies"]
dprows = [r for r in dp.iter_rows(min_row=5, values_only=True) if r[0]]
print("DEPS", len(dprows))
keys = set(r[0] for r in rows)
print("DANGLING DEPS", [(r[0], r[2]) for r in dprows if r[2] not in keys and not r[2].startswith("RWB-ACE")])

# removed stories must not appear as sections
md = open(MD, encoding="ascii").read()
for k in ["RWB-E1-003","RWB-E1-004","RWB-E1-005","RWB-E1-006","RWB-E1-009","RWB-E1-010","RWB-E1-012","RWB-E1-051"]:
    n = len(re.findall(r"(?m)^## %s " % k, md))
    if n: print("REMOVED SECTION PRESENT", k, n)
print("MD sections", len(re.findall(r"(?m)^## RWB-", md)), "ascii ok", all(ord(c) < 128 for c in md))
