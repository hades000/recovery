# -*- coding: utf-8 -*-
import io, os, re, math, copy
import openpyxl
from openpyxl.utils import get_column_letter

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
U = os.path.join(BASE, "04 User stories")


def parse(md_path):
    doc = io.open(md_path, encoding="ascii").read()
    blocks = [b for b in re.split(r"(?m)^(?=## RWB-)", doc) if b.startswith("## RWB-")]
    out = []
    for b in blocks:
        key, title = re.match(r"## (RWB-\w+-\d+) (.*)", b).groups()
        removed = bool(re.search(r"(?m)^\*\*Removed by D-RCV-35", b))

        def meta(label):
            m = re.search(r"(?m)^\| " + re.escape(label) + r" \| (.*?) \|$", b)
            return m.group(1).strip() if m else ""

        epic = meta("Epic").split(",")[0].strip()
        module = meta("Module")
        mod_code, _, mod_name = module.partition(" ")

        story = re.search(r"(?ms)^\*\*Story\.\*\* (.*?)$", b)
        story = " ".join(story.group(1).split()) if story else ""

        ents = []
        dsec = re.search(r"(?ms)^\*\*Data\*\*\n(.*?)(?=^\*\*Endpoints|\Z)", b)
        if dsec:
            for ln in dsec.group(1).split("\n"):
                m = re.match(r"^\| ([a-z_0-9]+) \| ", ln)
                if m:
                    ents.append(m.group(1))

        screens = "None"
        ssec = re.search(r"(?ms)^\*\*Screen and states\*\*\n(.*?)(?=^\*\*Permission)", b)
        if ssec:
            names = []
            for ln in ssec.group(1).split("\n"):
                m = re.match(r"^\| (?:SCR-\d+|PRT-\d+) (.*?) \|", ln)
                if m:
                    names.append(m.group(1).strip())
            if names:
                screens = "; ".join(names)

        perms = []
        psec = re.search(r"(?ms)^\*\*Permission checks\*\*\n(.*?)(?=^\*\*Validation)", b)
        if psec:
            for ln in psec.group(1).split("\n"):
                m = re.match(r"^\| ([A-Za-z ]+) \| ([A-Z]) \|", ln)
                if m:
                    perms.append("%s %s" % (m.group(1).strip(), m.group(2)))
        perm = "; ".join(perms)

        msgs = []
        msec = re.search(r"(?ms)^\*\*Validation and messages\*\*\n(.*?)(?=^\*\*Test cases)", b)
        if msec:
            for ln in msec.group(1).split("\n"):
                m = re.match(r"^\| (MSG-[\w-]+) \|", ln)
                if m:
                    msgs.append(m.group(1))

        g = re.search(r"(?ms)```gherkin\n(.*?)```", b)
        gherkin = g.group(1).rstrip("\n") if g else ""
        acs = re.findall(r"(?m)^  Scenario: (AC\d+) (.*)$", b)

        tcs = []
        tsec = re.search(r"(?ms)^\*\*Test cases\*\*\n(.*?)(?=^\*\*Guardrails)", b)
        if tsec:
            for ln in tsec.group(1).split("\n"):
                m = re.match(r"^\| (TC-[\w-]+-\d+) \| ([^|]+?) \| (.*?) \|$", ln)
                if m:
                    tcs.append((m.group(1), m.group(2).strip(), m.group(3).strip()))

        out.append(dict(key=key, title=title.strip(), removed=removed, epic=epic,
                        mod_code=mod_code, mod_name=mod_name, story=story,
                        priority=meta("Priority"), deps=meta("Depends on"),
                        decision=meta("Decision"), ents=ents, screens=screens,
                        perm=perm, msgs=msgs, gherkin=gherkin,
                        acs=[c for c, n in acs], tcs=tcs))
    return out


def fix_sheet(ws, rows, min_row=5):
    tmpl = [ws.cell(row=min_row, column=c)._style for c in range(1, ws.max_column + 1)]
    for r in range(min_row, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            ws.cell(row=r, column=c).value = None
    for i, vals in enumerate(rows):
        r = min_row + i
        for c in range(1, ws.max_column + 1):
            cell = ws.cell(row=r, column=c)
            cell._style = copy.copy(tmpl[c - 1])
            cell.value = vals[c - 1] if c - 1 < len(vals) else None
        longest = max((len(str(v)) if v is not None else 0) for v in vals)
        ws.row_dimensions[r].height = max(15.0, math.ceil(longest / 49.0) * 12.75 + 8)
    last = min_row - 1 + len(rows)
    ws.auto_filter.ref = "A%d:%s%d" % (min_row - 1, get_column_letter(ws.max_column), last)
    return last


# ------------------------------------------------------------------ administration
adm = parse(os.path.join(U, "Recovery Workbench Administration Stories v3.md"))
assert len(adm) == 22, len(adm)
src = os.path.join(U, "Recovery Workbench Administration Stories v2.xlsx")
dst = os.path.join(U, "Recovery Workbench Administration Stories v3.xlsx")
wb = openpyxl.load_workbook(src)

rows = [[s["key"], s["epic"], s["mod_code"], s["mod_name"], s["title"], s["story"], s["priority"],
         s["deps"], ", ".join(s["ents"]), s["screens"], s["perm"], ", ".join(s["msgs"]),
         len(s["acs"]), len(s["tcs"]), s["decision"]] for s in adm]
ws = wb["Stories"]
fix_sheet(ws, rows)
ws["A2"] = "22 stories. Re-based on D-RCV-35: RWB-AD-018 and RWB-AD-019 rewritten, RWB-AD-004 a minor edit."

fix_sheet(wb["Acceptance criteria"], [[s["key"], s["title"], s["gherkin"]] for s in adm])

acname = {}
for s in adm:
    for m in re.finditer(r"(?m)^  Scenario: (AC\d+) (.*)$", s["gherkin"]):
        acname[(s["key"], m.group(1))] = m.group(2)
rows = []
for s in adm:
    for tcid, covers, test in s["tcs"]:
        code = covers.split(",")[0].strip()
        rows.append([tcid, s["key"], covers, acname.get((s["key"], code), test)])
fix_sheet(wb["Test cases"], rows)
wb["Test cases"]["A2"] = "%d test cases." % len(rows)
for r in range(5, wb["Related backlog"].max_row + 1):
    if wb["Related backlog"].cell(row=r, column=1).value == "RWB-E1-056":
        wb["Related backlog"].cell(row=r, column=2).value = "Run books and monitoring for every Epic 1 Workbench job"
wb.save(dst)
print("AD", dst, "stories", len(adm), "tc", len(rows))

# ------------------------------------------------------------------ data migration
dm = parse(os.path.join(U, "Recovery Workbench Data Migration Stories v3.md"))
assert len(dm) == 14, len(dm)
src = os.path.join(U, "Recovery Workbench Data Migration Stories v2.xlsx")
dst = os.path.join(U, "Recovery Workbench Data Migration Stories v3.xlsx")
wb = openpyxl.load_workbook(src)

rows = []
for s in dm:
    if s["removed"]:
        why = re.search(r"(?ms)^## " + re.escape(s["key"]) + r".*?\| Why \| (.*?) \|$", s["gherkin"] or s["story"] or "")
        rows.append([s["key"], s["epic"], s["mod_code"], s["mod_name"], s["title"],
                     "Removed by D-RCV-35. The data is already in ACE and is read from the views.",
                     "Must", "None", "None", "None", "None", "None", 0, 0, "D-RCV-35"])
    else:
        rows.append([s["key"], s["epic"], s["mod_code"], s["mod_name"], s["title"], s["story"],
                     s["priority"], s["deps"], ", ".join(s["ents"]), s["screens"], s["perm"],
                     ", ".join(s["msgs"]), len(s["acs"]), len(s["tcs"]), s["decision"]])
ws = wb["Stories"]
fix_sheet(ws, rows)
ws["A2"] = "14 stories, one per data product. RWB-DM-001 and RWB-DM-002 are removed: the data is already in ACE."
wb.save(dst)
print("DM", dst, "stories", len(dm))
