# -*- coding: utf-8 -*-
"""Build Recovery Workbench Story Build Order v2 from v1 and the v5 sequence."""
import copy, shutil, datetime
import docx
from docx.oxml.ns import qn
import openpyxl

SRC = r"11 Delivery and operations\Recovery Workbench Story Build Order v1.docx"
DST = r"11 Delivery and operations\Recovery Workbench Story Build Order v2.docx"
SEQ = r"11 Delivery and operations\Recovery Workbench Build Sequence Epic 1 and Epic 2 v5.xlsx"

shutil.copyfile(SRC, DST)
d = docx.Document(DST)

# ---------- data
ws = openpyxl.load_workbook(SEQ, data_only=True)["Sequence"]
items = []
for r in range(5, ws.max_row + 1):
    items.append({
        "n": ws.cell(r, 1).value,
        "key": ws.cell(r, 2).value,
        "title": ws.cell(r, 3).value,
        "module": ws.cell(r, 4).value,
        "type": ws.cell(r, 5).value,
        "dep": ws.cell(r, 7).value or "",
        "window": ws.cell(r, 8).value,
        "dates": ws.cell(r, 9).value,
        "release": ws.cell(r, 10).value,
    })
WINDOWS = ["Window 1", "Window 2", "Window 3", "Window 4", "Epic 3"]
WINDOW_TEXT = {"Window 1": "2 to 13 November 2026",
               "Window 2": "16 to 27 November 2026",
               "Window 3": "30 November to 11 December 2026",
               "Window 4": "14 to 25 December 2026",
               "Epic 3": "28 December 2026 to 22 January 2027"}
groups = {w: [i for i in items if i["window"] == w] for w in WINDOWS}

# ---------- helpers
def set_cell(cell, text):
    ps = cell.paragraphs
    p = ps[0]
    for extra in ps[1:]:
        extra._p.getparent().remove(extra._p)
    runs = p.runs
    keep = None
    for r in runs:
        if r._element.find(qn("w:rPr")) is not None:
            keep = r
    if keep is None and runs:
        keep = runs[-1]
    for r in runs:
        if r is not keep:
            r._element.getparent().remove(r._element)
    if keep is None:
        keep = p.add_run()
    keep.text = text

def resize(table, n):
    body = table.rows[1:]
    cur = len(body)
    if cur < n:
        tmpl = body[-1]._tr
        for _ in range(n - cur):
            table._tbl.append(copy.deepcopy(tmpl))
    elif cur > n:
        for row in body[n:]:
            table._tbl.remove(row._tr)

def short(dep):
    if not dep:
        return "None"
    out = []
    for x in [y.strip() for y in dep.split(",") if y.strip()]:
        out.append(x.replace("RWB-", ""))
    return ", ".join(out)

def para_text(p, text):
    runs = p.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        p.add_run(text)

# ---------- paragraphs
paras = d.paragraphs
para_text(paras[1], "E2E Recovery Workbench. SCB Collections and Recovery. "
                    "Henka Group, 15 November 2026.")
para_text(paras[2],
          "The order the 107 items are built in, from Recovery Workbench Build Sequence "
          "Epic 1 and Epic 2 v5.xlsx. The story numbers are a catalog, not an order: "
          "RWB-E1-001 depends on RWB-E1-043 and RWB-E1-044, which are built before it. "
          "Pull the next item whose dependencies are done. E is an enabler, S is a user "
          "story. Waits on names the items that must finish first, by their number within "
          "the same family. RWB-ACE-001 is the ACE team's delivery and is not pulled by "
          "either squad; it gates RWB-E1-069.")

heads = [p for p in paras if p.text.startswith("Window ") or p.text.startswith("Epic 3, ")]
counts = [p for p in paras if "items, releasing in Epic" in p.text]
assert len(heads) == 5 and len(counts) == 5, (len(heads), len(counts))

for h, w in zip(heads, WINDOWS):
    para_text(h, "%s, %s" % (w, WINDOW_TEXT[w]))
for c, w in zip(counts, WINDOWS):
    para_text(c, "%d items, releasing in Epic %s." % (len(groups[w]), groups[w][0]["release"][1:]))

# ---------- tables
for t, w in zip(d.tables, WINDOWS):
    rows = groups[w]
    resize(t, len(rows))
    for row, item in zip(t.rows[1:], rows):
        vals = [str(item["n"]), item["key"], item["title"], item["module"],
                "E" if item["type"] == "Enabler" else "S", short(item["dep"])]
        for cell, v in zip(row.cells, vals):
            set_cell(cell, v)

# ---------- how to use it
how = [p for p in d.paragraphs if p.text.startswith("Take the next item in order")][0]
para_text(how,
          "Take the next item in order whose dependencies are done. Work in progress per squad "
          "stays within the board limit. An item on the critical path is taken before any other "
          "item. An item that will miss its release stays behind its flag and moves to the next "
          "release. The two squads agree the split at the daily board; the product owner settles "
          "a disagreement the same day.")

# ---------- closing paragraphs
last = [p for p in d.paragraphs if p.text.startswith("The critical path runs")][0]
para_text(last,
          "The critical path starts outside the squads. RWB-ACE-001, the ACE team's 14 tables, "
          "12 columns and read grant, is due on 21 November under DL43 and gates RWB-E1-069, "
          "the 30 read-only views. RWB-E1-069 gates RWB-E1-018 and RWB-E1-002, the case record "
          "and the case list. From RWB-E1-020 the chain runs RWB-E1-028, RWB-E1-030, RWB-E1-059, "
          "RWB-E1-061 and RWB-E1-063, then RWB-E2-031, RWB-E2-028 and RWB-E2-029: 13 items end "
          "to end. A day lost on RWB-ACE-001 or on RWB-E1-069 moves the 30 November release.")

d.core_properties.title = "Recovery Workbench Story Build Order v2"
d.core_properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
d.save(DST)
print("saved", DST, {w: len(groups[w]) for w in WINDOWS})


