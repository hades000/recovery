import re, math, os
import openpyxl
from copy import copy

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
MD = BASE + r"\04 User stories\Recovery Workbench User Stories Epic 2 v6.md"
SRC = BASE + r"\04 User stories\Recovery Workbench User Stories Epic 2 v5.xlsx"
DST = BASE + r"\04 User stories\Recovery Workbench User Stories Epic 2 v6.xlsx"
REWRITTEN = {"RWB-E2-001", "RWB-E2-003", "RWB-E2-007", "RWB-E2-008", "RWB-E2-010", "RWB-E2-034"}

doc = open(MD, encoding="ascii").read()
blocks = re.split(r"(?m)^(?=## RWB-E2-\d+ )", doc)
blocks = [b for b in blocks if b.startswith("## RWB-E2-")]

def meta(block, label):
    m = re.search(r"(?m)^\| " + re.escape(label) + r" \| (.*?) \|$", block)
    return m.group(1).strip() if m else ""

stories = []
for b in blocks:
    key, title = re.match(r"## (RWB-E2-\d+) (.*)", b).groups()
    story_sec = re.search(r"(?ms)### 1\. Story(.*?)(?=### 2\.)", b).group(1)
    story_txt = " ".join(x.strip() for x in story_sec.strip().split("\n") if x.strip())
    story_txt = story_txt.replace("**", "")
    data_sec = re.search(r"(?ms)### 11\. Data(.*?)(?=### 12\.)", b).group(1)
    ents = []
    for ln in data_sec.split("\n"):
        mm = re.match(r"\| (DF-[\w\-]+(?: to DF-[\w\-]+)?|Standard column) \| ([a-z_0-9]+) \|", ln)
        if mm and mm.group(2) not in ents:
            ents.append(mm.group(2))
    g = re.search(r"(?ms)```gherkin\n(.*?)```", b)
    gherkin = g.group(1).rstrip("\n") if g else ""
    acs = re.findall(r"(?m)^  Scenario: (AC\d+) (.*)$", b)
    tcsec = re.search(r"(?ms)### 16\. Test cases(.*?)(?=### 17\.)", b)
    tcs = []
    if tcsec:
        for ln in tcsec.group(1).split("\n"):
            mm = re.match(r"\| (TC-E2-\d{3}-\d{2}) \| (.*?) \| (.*?) \| (.*?) \|$", ln)
            if mm:
                tcs.append(mm.groups())
    trsec = re.search(r"(?ms)### 18\. Traceability(.*?)(?=### 19\.)", b)
    reqs = []
    if trsec:
        for ln in trsec.group(1).split("\n"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 2 and re.match(r"REQ-", cells[0]):
                reqs.append(cells[0])
    stories.append(dict(key=key, title=title.strip(), module=meta(b, "Module"),
                        reqs=meta(b, "Requirement IDs"), priority=meta(b, "Priority"),
                        deps=meta(b, "Depends on"), decision=meta(b, "Decision"),
                        story=story_txt, ents=ents, gherkin=gherkin, acs=acs, tcs=tcs, treqs=reqs))

assert len(stories) == 34

# ---------- old workbook ----------
old = openpyxl.load_workbook(SRC)
osheet = {
    "Stories": {r[0]: r for r in old["Stories"].iter_rows(min_row=5, values_only=True)},
    "Acceptance criteria": {r[0]: r for r in old["Acceptance criteria"].iter_rows(min_row=5, values_only=True)},
    "Test cases": {r[0]: r for r in old["Test cases"].iter_rows(min_row=5, values_only=True)},
}
oheight = {}
for name in old.sheetnames:
    ws = old[name]
    for r in range(5, ws.max_row + 1):
        k = ws.cell(row=r, column=1).value
        if k:
            oheight[(name, k)] = ws.row_dimensions[r].height

wb = openpyxl.load_workbook(SRC)

def est_height(vals, minh=15.0):
    longest = max((len(str(v)) if v is not None else 0) for v in vals)
    return max(minh, math.ceil(longest / 49.0) * 12.75 + 8)

def rewrite(ws, rows, keyfn, changed):
    # style template from existing row 5
    tmpl = [ws.cell(row=5, column=c)._style for c in range(1, ws.max_column + 1)]
    # clear old data rows
    for r in range(5, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            ws.cell(row=r, column=c).value = None
    for i, vals in enumerate(rows):
        r = 5 + i
        for c in range(1, ws.max_column + 1):
            cell = ws.cell(row=r, column=c)
            cell._style = copy(tmpl[c - 1])
            cell.value = vals[c - 1] if c - 1 < len(vals) else None
        k = keyfn(vals)
        h = None if changed(k) else oheight.get((ws.title, k))
        ws.row_dimensions[r].height = h if h else est_height(vals)
    last = 4 + len(rows)
    ws.auto_filter.ref = "A4:%s%d" % (openpyxl.utils.get_column_letter(ws.max_column), last)
    return last

# ---------- Stories ----------
rows = []
for s in stories:
    o = osheet["Stories"].get(s["key"], (None,) * 14)
    rows.append([s["key"], o[1], s["module"], s["title"], s["story"], s["reqs"],
                 s["priority"], s["deps"], ", ".join(s["ents"]), o[9], o[10],
                 len(s["acs"]), len(s["tcs"]), s["decision"]])
ws = wb["Stories"]
last = rewrite(ws, rows, lambda v: v[0], lambda k: k in REWRITTEN)
ws["A2"] = "%d stories. Full detail of each story is in the Markdown file and the story file" % len(rows)

# ---------- Acceptance criteria ----------
rows = [[s["key"], s["title"], s["gherkin"]] for s in stories]
ws = wb["Acceptance criteria"]
rewrite(ws, rows, lambda v: v[0], lambda k: k in REWRITTEN)

# ---------- Test cases ----------
old_tc_titles = {}
for k, r in osheet["Test cases"].items():
    old_tc_titles[k] = r[3]
acname = {}
for s in stories:
    for code, name in s["acs"]:
        acname[(s["key"], code)] = name
rows = []
for s in stories:
    for tcid, covers, level, data in s["tcs"]:
        title = None
        m = re.match(r"(AC\d+)", covers)
        if m and (s["key"], m.group(1)) in acname:
            title = acname[(s["key"], m.group(1))]
        if not title:
            title = old_tc_titles.get(tcid) or covers
        rows.append([tcid, s["key"], covers, title, level, data])
ws = wb["Test cases"]
last = rewrite(ws, rows, lambda v: v[0], lambda k: k.split("-")[1] and ("RWB-E2-" + k.split("-")[1]) in REWRITTEN)
ws["A2"] = "%d test cases. Given, When and the expected result of each are in the Test Case" % len(rows)

# ---------- Traceability ----------
rows = []
for s in stories:
    for rq in s["treqs"]:
        rows.append([s["key"], s["title"], rq])
ws = wb["Traceability"]
rewrite(ws, rows, lambda v: v[0], lambda k: k in REWRITTEN)

# ---------- Dependencies ----------
rows = []
for s in stories:
    if s["deps"] and s["deps"].strip():
        for d in [x.strip() for x in s["deps"].split(",") if x.strip()]:
            rows.append([s["key"], s["title"], d])
ws = wb["Dependencies"]
rewrite(ws, rows, lambda v: v[0], lambda k: k in REWRITTEN)

wb.save(DST)
print("rows: stories", len(stories), "tc", len(ws.parent["Test cases"]["A5":"A2000"]))
print("saved", DST)
