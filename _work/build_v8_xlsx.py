import re, os, json, math
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
MD = os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.md")
DST = os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.xlsx")
SCHEMA = os.path.join(ROOT, "06 Data", "Recovery Workbench Physical Schema v5.sql")

doc = open(MD, encoding="ascii").read()
blocks = [b for b in re.split(r"(?m)^(?=## RWB-)", doc) if b.startswith("## RWB-")]
assert len(blocks) == 71, len(blocks)

# schema order
sql = open(SCHEMA, encoding="utf-8-sig", errors="replace").read()
tables = re.findall(r"(?m)^CREATE TABLE\s+\"?([a-z0-9_]+)\"?", sql, re.I)
assert len(tables) == 92 and len(set(tables)) == 92, (len(tables), len(set(tables)))

SECTION_A = ["v_ace_account","v_ace_payment","v_ace_customer","v_ace_contact","v_ace_ca_relation",
 "v_ace_aa_relation","v_ace_collateral","v_ace_asset","v_ace_efs_action","v_ace_efs_action_code",
 "v_ace_efs_assignment","v_ace_bucket_log","v_ace_product","v_ace_branch","v_ace_holiday","v_ace_plan"]
SECTION_B = ["v_ace_batch_status","v_ace_valuation","v_ace_collateral_detail","v_ace_npa_asset",
 "v_ace_npa_sale","v_ace_lawsuit","v_ace_hearing","v_ace_pod","v_ace_write_off","v_ace_score",
 "v_ace_party_product","v_ace_credit_decision","v_ace_esign","v_ace_iam_group"]

BASE7 = {"data_product","sys_objects","sys_fields","party_ext","contact_point_ext","account_ext","valuation_ext"}
assert BASE7.issubset(set(tables))

def meta(block, label):
    m = re.search(r"(?m)^\| " + re.escape(label) + r" \| (.*?) \|$", block)
    return m.group(1).strip() if m else ""

def section(block, n):
    m = re.search(r"(?ms)### %d\. .*?$(.*?)(?=### \d+\. |\Z)" % n, block)
    return m.group(1) if m else ""

def rows_of(sec):
    out = []
    for l in sec.split("\n"):
        s = l.strip()
        if s.startswith("|") and s.endswith("|"):
            out.append([c.strip() for c in s.strip("|").split("|")])
    return out

stories = []
for b in blocks:
    key, title = re.match(r"## (RWB-\S+) (.*)", b).groups()
    story_sec = section(b, 1)
    story_txt = " ".join(x.strip() for x in story_sec.strip().split("\n") if x.strip())
    story_txt = story_txt.replace("**", "")
    ents = []
    for r in rows_of(section(b, 11)):
        if len(r) >= 4 and r[0].startswith("DF-"):
            for p in r[1].split(","):
                p = p.strip()
                if not p:
                    continue
                if p == "the 85 other Workbench tables":
                    for t in tables:
                        if t not in BASE7 and t not in ents:
                            ents.append(t)
                elif p == "the 16 Section A views":
                    for v in SECTION_A:
                        if v not in ents: ents.append(v)
                elif p == "the 14 Section B views":
                    for v in SECTION_B:
                        if v not in ents: ents.append(v)
                elif p not in ents:
                    ents.append(p)
    g = re.search(r"(?ms)```gherkin\n(.*?)```", b)
    gherkin = g.group(1).rstrip("\n") if g else ""
    acs = re.findall(r"(?m)^  Scenario: (AC\d+) (.*)$", b)
    tcs = []
    for r in rows_of(section(b, 16)):
        if len(r) >= 4 and re.match(r"TC-", r[0]):
            tcs.append((r[0], r[1], r[2], r[3]))
    treqs = []
    for r in rows_of(section(b, 18)):
        if len(r) >= 7 and r[0].startswith("REQ-"):
            treqs.append(r[0])
    scr = sorted(set(re.findall(r"SCR-\d+", b)))
    msg = sorted(set(re.findall(r"MSG-[A-Z0-9]+(?:-\d+)?", b)))
    stories.append(dict(key=key, title=title.strip(), module=meta(b, "Module"),
                        reqs=meta(b, "Requirement IDs"), priority=meta(b, "Priority"),
                        deps=meta(b, "Depends on"), decision=meta(b, "Decision"),
                        story=story_txt, ents=ents, gherkin=gherkin, acs=acs, tcs=tcs, treqs=treqs,
                        scr=scr, msg=msg))

wb = openpyxl.Workbook()
TITLE_FONT = Font(name="Aptos", size=16, bold=True, color="4E297F")
SUB_FONT = Font(name="Aptos", size=10, color="404040")
HEAD_FONT = Font(name="Aptos", size=10, bold=True, color="4E297F")
HEAD_FILL = PatternFill("solid", fgColor="DCD3EB")
DATA_FONT = Font(name="Aptos", size=10, color="1F1F1F")
KEY_FONT = Font(name="Aptos", size=10, bold=True, color="1F1F1F")
WRAP = Alignment(wrap_text=True, vertical="top")

def est_height(vals, widths, minh=15.0):
    lines = 1
    for v, w in zip(vals, widths):
        if v is None:
            continue
        s = str(v)
        chars = max(1, int(w * 1.15))
        n = 0
        for part in s.split("\n"):
            n += max(1, math.ceil(len(part) / chars))
        lines = max(lines, n)
    return max(minh, min(lines, 20) * 12.75 + 6)

def sheet(name, headers, widths, rows, keybold=True):
    ws = wb.create_sheet(name)
    ws["A1"] = {"Stories": "Stories, Epic 1", "Traceability": "Story to requirement",
                "Dependencies": "Story dependencies"}.get(name, name)
    ws["A1"].font = TITLE_FONT
    ws["A2"].font = SUB_FONT
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        c = ws.cell(row=4, column=i, value=h)
        c.font = HEAD_FONT; c.fill = HEAD_FILL; c.alignment = WRAP
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[4].height = 30
    for ri, vals in enumerate(rows, 5):
        for ci, v in enumerate(vals, 1):
            c = ws.cell(row=ri, column=ci, value=v)
            c.font = KEY_FONT if (ci == 1 and keybold) else DATA_FONT
            c.alignment = WRAP
        ws.row_dimensions[ri].height = est_height(vals, widths)
    ws.freeze_panes = "B5"
    ws.auto_filter.ref = "A4:%s%d" % (get_column_letter(len(headers)), 4 + len(rows))
    return ws

# Stories
widths = [12, 6, 22, 34, 60, 26, 9, 22, 34, 18, 30, 9, 10, 12]
rows = []
for s in stories:
    rows.append([s["key"], "E1", s["module"], s["title"], s["story"], s["reqs"], s["priority"],
                 s["deps"], ", ".join(s["ents"]), ", ".join(s["scr"]) if s["scr"] else "None",
                 ", ".join(s["msg"]) if s["msg"] else "None", len(s["acs"]), len(s["tcs"]), s["decision"]])
ws = sheet("Stories", ["Key","Epic","Module","Title","Story","Requirement IDs","Priority","Depends on",
                       "Entities","Screens","Messages","Criteria","Test cases","Decision"], widths, rows)
ws["A2"] = "%d stories. Full detail of each story is in the Markdown file and the story files." % len(rows)
ws["A2"].font = SUB_FONT

# Acceptance criteria
ws = sheet("Acceptance criteria", ["Key", "Title", "Gherkin"], [12, 34, 110],
           [[s["key"], s["title"], s["gherkin"]] for s in stories])
ws["A2"] = "Gherkin per story, as written in the Markdown file."
ws["A2"].font = SUB_FONT

# Test cases
ws = None
acname = {(s["key"], code): name for s in stories for code, name in s["acs"]}
rows = []
for s in stories:
    for tcid, covers, level, data in s["tcs"]:
        m = re.match(r"(AC\d+)", covers)
        title = acname.get((s["key"], m.group(1))) if m else None
        if not title:
            title = "A role without the right is refused with MSG-P4-002" if level == "Access" else covers
        rows.append([tcid, s["key"], covers, title, level, data])
ws = sheet("Test cases", ["Test case", "Story", "Covers", "Test", "Level", "Data"], [16, 12, 14, 56, 11, 44], rows)
ws["A2"] = "%d test cases. Given, When and the expected result of each are in the Test Cases file." % len(rows)
ws["A2"].font = SUB_FONT

# Traceability
rows = [[s["key"], s["title"], rq] for s in stories for rq in s["treqs"]]
ws = sheet("Traceability", ["Story", "Title", "Requirement"], [12, 44, 16], rows)
ws["A2"] = "Each row is one requirement a story meets."
ws["A2"].font = SUB_FONT

# Dependencies
rows = []
seen = set()
for s in stories:
    for d in re.findall(r"RWB-[A-Z0-9]+-\d+", s["deps"]):
        if (s["key"], d) in seen: continue
        seen.add((s["key"], d))
        rows.append([s["key"], s["title"], d])
ws = sheet("Dependencies", ["Story", "Title", "Depends on"], [12, 44, 16], rows)
ws["A2"] = "Each row is one dependency; the story on the right is finished first."
ws["A2"].font = SUB_FONT

del wb["Sheet"]
wb.save(DST)
print("saved", DST)
print("stories", len(stories), "acs", sum(len(s["acs"]) for s in stories), "tests", sum(len(s["tcs"]) for s in stories),
      "trace rows", sum(len(s["treqs"]) for s in stories), "dep rows", len(rows))
