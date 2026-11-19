import re, os, openpyxl
ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
md = open(os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.md"), encoding="ascii").read()
blocks = {re.match(r"## (RWB-\S+)", b).group(1): b for b in re.split(r"(?m)^(?=## RWB-)", md) if b.startswith("## RWB-")}
wb = openpyxl.load_workbook(os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.xlsx"), read_only=True)
ws = wb["Stories"]
bad = []
for r in ws.iter_rows(min_row=5, values_only=True):
    if not r[0]: continue
    b = blocks[r[0]]
    title = re.match(r"## RWB-\S+ (.*)", b).group(1)
    if r[3] != title: bad.append((r[0], "title", r[3], title))
    req = re.search(r"(?m)^\| Requirement IDs \| (.*?) \|$", b).group(1)
    if r[5] != req: bad.append((r[0], "req", r[5], req))
print("BAD", len(bad), bad[:5])
print("rows", ws.max_row - 4)
