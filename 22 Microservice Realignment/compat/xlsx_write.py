from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HEAD_FILL = PatternFill("solid", fgColor="1F3864")

def write_book(path, sheets, read_me=None):
    """sheets: dict name -> (header list, rows list). Header row bold white on navy, freeze, filter."""
    wb = Workbook(); wb.remove(wb.active)
    if read_me:
        ws = wb.create_sheet("Read me")
        for line in read_me.splitlines():
            ws.append([line])
        ws.column_dimensions["A"].width = 120
    for name, (head, rows) in sheets.items():
        ws = wb.create_sheet(name[:31]); ws.append(head)
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF"); c.fill = HEAD_FILL; c.alignment = Alignment(wrap_text=True, vertical="top")
        for r in rows:
            ws.append([("; ".join(map(str, v)) if isinstance(v, (list, tuple, set)) else v) for v in r])
        ws.freeze_panes = "A2"
        if rows:
            ws.auto_filter.ref = ws.dimensions
        for i, h in enumerate(head, 1):
            ws.column_dimensions[get_column_letter(i)].width = min(60, max(12, len(str(h)) + 4))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path
