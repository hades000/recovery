# -*- coding: utf-8 -*-
import io, os, re
import openpyxl

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
U = os.path.join(BASE, "04 User stories")


def md_gherkins(path):
    doc = io.open(path, encoding="ascii").read()
    out = {}
    for b in [x for x in re.split(r"(?m)^(?=## RWB-)", doc) if x.startswith("## RWB-")]:
        key = re.match(r"## (RWB-\w+-\d+)", b).group(1)
        g = re.search(r"(?ms)```gherkin\n(.*?)```", b)
        out[key] = g.group(1).rstrip("\n") if g else ""
    return out


def md_entities(path):
    doc = io.open(path, encoding="ascii").read()
    out = {}
    for b in [x for x in re.split(r"(?m)^(?=## RWB-)", doc) if x.startswith("## RWB-")]:
        key = re.match(r"## (RWB-\w+-\d+)", b).group(1)
        ents = []
        d = re.search(r"(?ms)^\*\*Data\*\*\n(.*?)(?=^\*\*Endpoints|\Z)", b)
        if d:
            for ln in d.group(1).split("\n"):
                m = re.match(r"^\| ([a-z_0-9]+) \| ", ln)
                if m:
                    ents.append(m.group(1))
        out[key] = ents
    return out


for stem in ["Administration", "Data Migration"]:
    md = os.path.join(U, "Recovery Workbench %s Stories v3.md" % stem)
    xl = os.path.join(U, "Recovery Workbench %s Stories v3.xlsx" % stem)
    g = md_gherkins(md)
    e = md_entities(md)
    wb = openpyxl.load_workbook(xl)
    ws = wb["Acceptance criteria"] if "Acceptance criteria" in wb.sheetnames else None
    print("==", stem)
    print("   sheets:", wb.sheetnames)
    if ws:
        mismatch = 0
        for r in ws.iter_rows(min_row=5, values_only=True):
            if not r[0]:
                continue
            if (r[2] or "") != g.get(r[0], "<none>"):
                mismatch += 1
                print("   GHERKIN MISMATCH", r[0])
        print("   acceptance rows:", ws.max_row - 4, "mismatches:", mismatch)
    st = wb["Stories"]
    ent_bad = 0
    for r in st.iter_rows(min_row=5, values_only=True):
        if not r[0]:
            continue
        cell = (r[8] or "").strip()
        want = ", ".join(e[r[0]])
        if cell != want:
            ent_bad += 1
            print("   ENTITIES MISMATCH", r[0], "|", cell, "|", want)
    print("   stories rows:", st.max_row - 4, "entity mismatches:", ent_bad)
    # counts
    acs = sum(len(re.findall(r"(?m)^  Scenario: ", v)) for v in g.values())
    print("   scenarios in md:", acs)
    nonascii = 0
    for s in wb.worksheets:
        for row in s.iter_rows(values_only=True):
            for c in row:
                if isinstance(c, str) and any(ord(ch) > 127 for ch in c):
                    nonascii += 1
    print("   non-ascii cells:", nonascii)
    for s in wb.worksheets:
        print("   merged:", s.title, len(s.merged_cells.ranges))
