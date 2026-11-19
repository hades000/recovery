import copy, datetime, docx
from docx.text.paragraph import Paragraph
from docx.table import Table

def set_text(p, text):
    runs = p.runs
    if not runs:
        p.add_run(text); return
    runs[0].text = text
    for r in runs[1:]:
        r._r.getparent().remove(r._r)

def set_cell(cell, text):
    ps = cell.paragraphs
    set_text(ps[0], text)
    for p in ps[1:]:
        p._p.getparent().remove(p._p)

def find_cell_row(table, first):
    for i, r in enumerate(table.rows):
        if r.cells[0].text.strip() == first:
            return i
    raise KeyError(first)

def set_row(table, first, values):
    r = table.rows[find_cell_row(table, first)]
    for c, v in zip(r.cells, values):
        if v is not None:
            set_cell(c, v)

def insert_row_after(table, first, values):
    i = find_cell_row(table, first)
    tr = table.rows[i]._tr
    new = copy.deepcopy(tr)
    tr.addnext(new)
    r = table.rows[i + 1]
    for c, v in zip(r.cells, values):
        set_cell(c, v)

def insert_para_after(p, text):
    new = copy.deepcopy(p._p)
    p._p.addnext(new)
    np = Paragraph(new, p._parent)
    set_text(np, text)
    return np

def para_starting(doc, start):
    for p in doc.paragraphs:
        if p.text.startswith(start):
            return p
    raise KeyError(start)

def doc_control(doc, title, change):
    set_text(para_starting(doc, 'SCB Collections and Recovery. Henka Group'),
             'SCB Collections and Recovery. Henka Group, 15 November 2026')
    t = doc.tables[0]
    set_row(t, 'Version', [None, '3'])
    set_row(t, 'Date', [None, '15 November 2026'])
    insert_row_after(t, 'Date', ['Change', change])
    cp = doc.core_properties
    cp.title = title
    cp.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
    cp.revision = (cp.revision or 1) + 1
