import copy, datetime
D = r'02 Business architecture and process'
def setv(ws, ref, new, old=None):
    c = ws[ref]
    if old is not None and c.value != old:
        raise SystemExit(f'{ws.title}!{ref} unexpected: {c.value!r}')
    c.value = new
def repl(ws, ref, a, b):
    c = ws[ref]
    if a not in (c.value or ''):
        raise SystemExit(f'{ws.title}!{ref} missing {a!r}: {c.value!r}')
    c.value = c.value.replace(a, b)
def add_row_like(ws, src_row, vals):
    r = ws.max_row + 1
    for i, v in enumerate(vals, 1):
        s = ws.cell(src_row, i); d = ws.cell(r, i, v)
        d._style = copy.copy(s._style)
    if ws.row_dimensions[src_row].height:
        ws.row_dimensions[r].height = ws.row_dimensions[src_row].height
    return r
def stamp(wb, title):
    wb.properties.title = title
    wb.properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
