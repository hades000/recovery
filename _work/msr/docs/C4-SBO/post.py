"""Post-processes the new docx: fixed table layout, column widths, header rows, document properties."""
import sys, datetime, zipfile
import docx
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PATH = sys.argv[1]
W = {
    ("#", "Key", "Title", "Module", "E or S", "Waits on"): [0.394, 1.102, 3.779, 0.669, 0.551, 3.936],
    ("#", "Key", "New story", "Work type", "Service", "Suggested owner", "Parallel lane", "Ready to start"):
        [0.42, 0.95, 2.05, 1.02, 1.38, 1.10, 1.28, 2.23],
    ("Wave", "Stories", "Lanes used", "Contract group", "Day 1", "Waits for a story in its lane"):
        [0.8, 0.9, 1.0, 1.5, 0.9, 5.33],
    ("Team type", "Day-1 stories of the 115 items", "Work types"): [2.6, 2.2, 5.63],
    ("Legacy key", "New story", "Work type", "Service", "Suggested owner", "Parallel lane", "Ready to start"):
        [0.95, 1.95, 1.1, 1.4, 1.5, 1.35, 2.18],
    ("Version", "Date", "Change", "Tool"): [0.7, 1.25, 6.85, 1.63],
}

def fixed(table):
    tblPr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)

def header_row(table):
    trPr = table.rows[0]._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    trPr.append(el)
    for cell in table.rows[0].cells:
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True

d = docx.Document(PATH)
applied = 0
for t in d.tables:
    head = tuple(c.text.strip() for c in t.rows[0].cells)
    widths = W.get(head)
    if not widths:
        print("NO WIDTHS FOR", head)
        continue
    t.autofit = False
    fixed(t)
    header_row(t)
    for row in t.rows:
        for i, cell in enumerate(row.cells):
            if i < len(widths):
                cell.width = Inches(widths[i])
    applied += 1

cp = d.core_properties
cp.author = "SCB Collections and Recovery. Henka Group"
cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
cp.title = "Recovery Workbench Story Build Order v4"
cp.subject = "The build order of the 115 items as microservice stories, with lane and Ready to start"
cp.category = "Delivery and operations"
cp.comments = "D-RCV-60 microservice realignment. Draft."
cp.keywords = "D-RCV-60; story build order; parallel lane; Day 1; Ready to start"
cp.revision = 4
cp.created = datetime.datetime(2026, 11, 22, 9, 0, 0)
cp.modified = datetime.datetime(2026, 11, 22, 9, 0, 0)
cp.last_printed = datetime.datetime(2026, 11, 22, 9, 0, 0)
d.save(PATH)
print("WROTE", PATH, "tables", len(d.tables), "widths applied", applied)

bad = []
with zipfile.ZipFile(PATH) as z:
    for n in z.namelist():
        b = z.read(n)
        for probe in (b"Rajdeep", b"Ghai", b"Claude"):
            if probe in b:
                bad.append((n, probe))
print("person-name probes:", bad)
