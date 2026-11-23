import openpyxl

SRC = r"01 Decisions and governance\Recovery Workbench Decision Log v10.xlsx"
wb = openpyxl.load_workbook(SRC)


def d(ref, ws):
    c = ws[ref]
    b = c.border
    color = None
    if c.font.color is not None and c.font.color.type == "rgb":
        color = c.font.color.rgb
    fill = c.fill.fgColor.rgb if c.fill and c.fill.fill_type else None
    sides = []
    for side in (b.bottom, b.top, b.left, b.right):
        sides.append(side.style if side is not None else None)
    print(ref, repr(c.value)[:45], "|font", c.font.name, c.font.sz, "b" if c.font.b else "",
          color, "|fill", fill, "|align", c.alignment.horizontal, c.alignment.vertical,
          c.alignment.wrap_text, "|fmt", c.number_format, "|bd", sides,
          "|rowh", ws.row_dimensions[c.row].height)


for name, refs in [
    ("Decisions taken", ["A2", "A5", "A6", "C6", "E6", "A26", "C26", "D26"]),
    ("By owner", ["A2", "A5", "C6", "A35"]),
    ("Open decisions", ["A6", "F6", "G6", "J6", "C45", "J45"]),
]:
    print("===", name)
    sheet = wb[name]
    for r in refs:
        d(r, sheet)

print("props", wb.properties.creator, "|", wb.properties.lastModifiedBy, "|", wb.properties.title)
print("sheets", wb.sheetnames)
