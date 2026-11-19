# -*- coding: utf-8 -*-
"""Build Recovery Workbench Cutover and Go Live Plan v3 from v2."""
import copy, shutil, datetime
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

SRC = r"11 Delivery and operations\Recovery Workbench Cutover and Go Live Plan v2.docx"
DST = r"11 Delivery and operations\Recovery Workbench Cutover and Go Live Plan v3.docx"

shutil.copyfile(SRC, DST)
d = docx.Document(DST)

def set_runs(p, text):
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

def set_cell(cell, text):
    p = cell.paragraphs[0]
    for extra in cell.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    set_runs(p, text)

def clone_para_before(target, template, text):
    el = copy.deepcopy(template._p)
    target._p.addprevious(el)
    p = Paragraph(el, target._parent)
    set_runs(p, text)
    return p

def clone_table_before(target, template):
    el = copy.deepcopy(template._tbl)
    target._p.addprevious(el)
    return Table(el, target._parent)

def fill_table(t, rows):
    body = t.rows[1:]
    cur = len(body)
    if cur < len(rows):
        tmpl = body[-1]._tr
        for _ in range(len(rows) - cur):
            t._tbl.append(copy.deepcopy(tmpl))
    elif cur > len(rows):
        for row in body[len(rows):]:
            t._tbl.remove(row._tr)
    for row, vals in zip(t.rows[1:], rows):
        for cell, v in zip(row.cells, vals):
            set_cell(cell, v)

paras = d.paragraphs
tables = d.tables

# ---- document control and title date
for row in tables[0].rows:
    if row.cells[0].text.strip() == "Version":
        set_cell(row.cells[1], "2")
    if row.cells[0].text.strip() == "Date":
        set_cell(row.cells[1], "15 November 2026")
set_runs(paras[3], "SCB Collections and Recovery. Henka Group, 15 November 2026")

# ---- section 1: no Workbench load
set_runs(paras[7],
         "Each monthly release goes live in the change window agreed with SCB IT (DL34). The "
         "first release, 30 November 2026, also starts the case list. The Workbench runs no "
         "load: ACE ingests every source and the release reads the 30 SELECT-only "
         "recovery.v_ace_* views (D-RCV-35, ADR-010). The release is ready when the ACE batch "
         "is ready, so the checks in section 6 are release gates.")

# ---- section 2 row: first morning
t2 = tables[1]
for row in t2.rows:
    if row.cells[0].text.strip() == "Next morning":
        set_cell(row.cells[1],
                 "ACE batch for the business date checked in v_ace_batch_status, then the case "
                 "list reconciled to the ACE account view")
        set_cell(row.cells[2], "Data steward")

# ---- rollback: add the ACE bullet
last_bullet = [p for p in paras if p.style.name == "List Paragraph"][-1]
clone_para_before(paras[17], last_bullet,
                  "No ACE data is rolled back with the Workbench: the views read the ACE batch "
                  "for the business date, and a wrong batch is corrected in ACE.")

# ---- new section 6: ACE batch readiness
h6_old = [p for p in d.paragraphs if p.text.startswith("6. First release specifics")][0]
h1_tmpl = h6_old
body_tmpl = [p for p in d.paragraphs if p.text.startswith("The release owner in the ACE team")][0]
spacer_tmpl = [p for p in d.paragraphs if p.style.name == "Normal" and p.text.strip() == ""][0]

h = clone_para_before(h6_old, h1_tmpl, "6. ACE batch readiness check")
clone_para_before(h6_old, body_tmpl,
                  "The check runs on the release day before the smoke test, and again on the "
                  "first morning after the release. A failed check holds the part of the "
                  "release that reads ACE; the Workbench features that read no ACE data go "
                  "ahead behind their flags.")
clone_para_before(h6_old, spacer_tmpl, "")
t6 = clone_table_before(h6_old, tables[1])
for cell, v in zip(t6.rows[0].cells, ["Check", "Passes when", "Who confirms"]):
    set_cell(cell, v)
fill_table(t6, [
    ["ACE additions", "RWB-ACE-001 is applied in PROD and the 14 tables and 12 columns are "
     "present", "ACE team lead"],
    ["Batch complete", "ace_batch_run holds a COMPLETED row for each recovery source and the "
     "business date, and v_ace_batch_status returns it", "ACE ingestion owner"],
    ["Grant in place", "The view-owner role selects the 21 listed ACE tables and no other; the "
     "recovery role reads recovery.v_ace_* only and writes no ACE table",
     "ACE DBA with SCB IT security"],
    ["Views resolve", "16 Section A and 14 Section B views compile, and the conformance test "
     "resolves the 80 appendix fields", "Data steward"],
    ["Case list runs", "JOB-02 starts on AceDataReady for the ALS business date and creates no "
     "case from an incomplete batch", "QA lead with the data steward"],
    ["Fallback agreed", "If a check fails, the case list holds, the data screens stay behind "
     "their flags, and the ACE team names the recovery date",
     "Release owner with the product owner"],
])

# ---- first release specifics
set_runs(h6_old, "7. First release specifics")
t3 = tables[2]
fill_table(t3, [
    ["Case list", "Built from the ACE account view on the first COMPLETED ALS batch for the "
                  "business date; reconciled to v_ace_account before it is shown"],
    ["ACE views", "16 Section A views live on the day; the 14 Section B views and the 12 new "
                  "ACE columns need RWB-ACE-001 (DL43, due 21 November)"],
    ["Spreadsheets", "Retired team by team under the procedure in section 8; each team keeps a "
                     "read-only archive"],
    ["Access", "Administration roles only; business roles from Epic 2 (DL39)"],
    ["Documents", "Store and OCR live; bulk intake of open-case documents starts"],
])

# ---- new section 8: tracker retirement
h9 = [p for p in d.paragraphs if p.text.startswith("7. Open decisions")][0]
h = clone_para_before(h9, h1_tmpl, "8. Tracker retirement")
clone_para_before(h9, body_tmpl,
                  "The 20 Excel and SharePoint trackers, 14 marked LOAD and 6 marked RETIRE in "
                  "the inventory, are retired in this release, team by team. Six teams own them: "
                  "TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF. None is loaded into the "
                  "Workbench. RWB-E1-005, RWB-E1-010 and RWB-E1-012 are removed under D-RCV-35, "
                  "so the Workbench provides no inventory, no load and no retirement screen: the "
                  "procedure below is run by the teams and recorded in one report.")
clone_para_before(h9, spacer_tmpl, "")
t8 = clone_table_before(h9, tables[1])
for cell, v in zip(t8.rows[0].cells, ["Step", "What happens", "Who"]):
    set_cell(cell, v)
fill_table(t8, [
    ["1", "The team manager works from the case list for two working days after the last "
          "tracker file of the team is signed off", "Team manager"],
    ["2", "The team manager makes each tracker read-only or moves it to the read-only archive, "
          "and records the archive location", "Team manager"],
    ["3", "The team manager confirms the retirement of each tracker, with the archive location "
          "and the date", "Team manager"],
    ["4", "The data steward records the fields of each tracker that no data product carries, "
          "for the later epic that picks them up", "Data steward"],
    ["5", "The Tribe lead reads the six-team report: trackers, retired, outstanding and the "
          "confirming manager for each team", "Tribe lead"],
    ["6", "The report is filed with the release checklist on 26 November 2026; a team with an "
          "outstanding tracker is named with its tracker codes", "Tribe lead with the business lead"],
])

# ---- open decisions
set_runs(h9, "9. Open decisions")
t4 = tables[3]
body = t4.rows[1:]
tmpl = body[-1]._tr
t4._tbl.append(copy.deepcopy(tmpl))
set_cell(t4.rows[-1].cells[0], "DL43")
set_cell(t4.rows[-1].cells[1], "Whether the ACE team accepts RWB-ACE-001 and its 21 November "
                                "date")

d.core_properties.title = "Recovery Workbench Cutover and Go Live Plan v3"
d.core_properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
d.save(DST)
print("saved", DST, "tables", len(d.tables), "paras", len(d.paragraphs))


