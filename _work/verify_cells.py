import re, os, openpyxl
ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
md = open(os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.md"), encoding="ascii").read()
blocks = {re.match(r"## (RWB-\S+)", b).group(1): b for b in re.split(r"(?m)^(?=## RWB-)", md) if b.startswith("## RWB-")}
wb = openpyxl.load_workbook(os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.xlsx"), read_only=True)
ac = wb["Acceptance criteria"]
bad = 0
for r in ac.iter_rows(min_row=5, values_only=True):
    if not r[0]: continue
    g = re.search(r"(?ms)```gherkin\n(.*?)```", blocks[r[0]]).group(1).rstrip("\n")
    if g != r[2]:
        bad += 1
        print("DIFF", r[0], len(g), len(r[2]))
print("GHERKIN DIFFS", bad)
tc = wb["Test cases"]
md_tc = re.findall(r"(?m)^\| (TC-\S+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", md)
xl_tc = [(r[0], r[2], r[4], r[5]) for r in tc.iter_rows(min_row=5, values_only=True) if r[0]]
print("TC MD", len(md_tc), "XL", len(xl_tc))
diff = [(a, b) for a, b in zip(md_tc, xl_tc) if a[0] != b[0] or a[1].strip() != b[1].strip() or a[2].strip() != b[2].strip() or a[3].strip() != b[3].strip()]
print("TC DIFF", len(diff), diff[:3])
