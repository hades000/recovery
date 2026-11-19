# -*- coding: utf-8 -*-
"""Build Recovery Workbench Release Plan v4.pptx from v3."""
import copy, shutil, datetime
from pptx import Presentation
import lxml.etree as etree

SRC = r"11 Delivery and operations\Recovery Workbench Release Plan v3.pptx"
DST = r"11 Delivery and operations\Recovery Workbench Release Plan v4.pptx"

shutil.copyfile(SRC, DST)
prs = Presentation(DST)

def set_para(p, text):
    runs = p.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p.text = text

def set_cell(cell, text):
    tf = cell.text_frame
    for extra in tf.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    set_para(tf.paragraphs[0], text)

def find_table(slide, name_hint=None):
    for sh in slide.shapes:
        if sh.has_table:
            return sh.table
    return None

def table_text(tbl):
    return [[c.text for c in row.cells] for row in tbl.rows]

slides = list(prs.slides)

# ---------- slide 1: date
s1 = slides[0]
for sh in s1.shapes:
    if sh.has_text_frame and "28 October 2026" in sh.text_frame.text:
        for p in sh.text_frame.paragraphs:
            if "28 October 2026" in p.text:
                set_para(p, "Henka Group, 15 November 2026")

# ---------- slide 2: E1 business outcome
t2 = find_table(slides[1])
for row in t2.rows:
    if row.cells[0].text.strip() == "E1":
        set_cell(row.cells[2],
                 "One case list for every account at 90 days past due or more, reconciled to "
                 "the ACE account view. Documents found by case. Decision log store. Read-only "
                 "case record view")

# ---------- slide 3: release dates and E1 content
RELEASE = {"E1": "30 Nov", "E2": "31 Dec", "E3": "31 Jan", "E4": "28 Feb",
           "E5": "31 Mar", "E6": "30 Apr", "E7": "31 May", "E8": "30 Jun"}
t3 = find_table(slides[2])
for row in t3.rows:
    ep = row.cells[0].text.strip()
    if ep in RELEASE:
        set_cell(row.cells[1], RELEASE[ep])
    if ep == "E1":
        set_cell(row.cells[2],
                 "P1 recovery data engine over the 30 read-only recovery.v_ace_* views "
                 "(RWB-E1-069); P3 case record, state model and rules component with allocation "
                 "rules; P4 sign-in and roles; P5 document store and OCR; P6 notice generation; "
                 "P7 decision log store; P9 baseline; P10 agent runtime in shadow")

# ---------- slide 7: release dates
t7 = find_table(slides[6])
for row in t7.rows:
    ep = row.cells[0].text.strip()
    if ep in RELEASE:
        set_cell(row.cells[1], RELEASE[ep])

# ---------- slide 8: dependencies, ACE first, DEP-14 re-worded
t8 = find_table(slides[7])
for row in t8.rows:
    if row.cells[0].text.startswith("COLLINS load"):
        set_cell(row.cells[0],
                 "ACE ingestion of account, payment, customer and score data, complete for the "
                 "business date")

# add a row at the end and move it to the first data position
tbl = t8._tbl
new_tr = copy.deepcopy(tbl.tr_lst[len(tbl.tr_lst) - 1])
tbl.append(new_tr)
row = t8.rows[len(t8.rows) - 1]
vals = ["ACE DB additions for the Workbench: 14 tables, 12 columns and the read grant "
        "(RWB-ACE-001)", "E1", "21 Nov", "ACE team (DL43)",
        "RWB-E1-069 has only the Section A views; the case list and the release move"]
for cell, v in zip(row.cells, vals):
    set_cell(cell, v)
tbl.remove(new_tr)
tbl.tr_lst[0].addnext(new_tr)

# ---------- slide 9: calendar risks, add E1 and use the release dates of slide 4
t9 = find_table(slides[8])
FIX9 = {"E3": "31 Jan", "E5": "31 Mar", "E6": "30 Apr"}
for row in t9.rows:
    ep = row.cells[0].text.strip()
    if ep in FIX9:
        set_cell(row.cells[1], FIX9[ep])
tbl9 = t9._tbl
new_tr9 = copy.deepcopy(tbl9.tr_lst[len(tbl9.tr_lst) - 1])
tbl9.append(new_tr9)
row9 = t9.rows[len(t9.rows) - 1]
for cell, v in zip(row9.cells, ["E1", "30 Nov",
        "RWB-ACE-001 (ACE team, DL43) is due 21 November and gates RWB-E1-069; a late ACE "
        "delivery moves the case list and the release"]):
    set_cell(cell, v)
tbl9.remove(new_tr9)
tbl9.tr_lst[0].addnext(new_tr9)

# ---------- properties
cp = prs.core_properties
cp.title = "Recovery Workbench Release Plan v4"
cp.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
prs.save(DST)
print("saved", DST)



