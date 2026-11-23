"""Format the v6 Case and Workflow Model: sheet order, widths, freeze panes."""
from pathlib import Path
import openpyxl
from openpyxl.styles import Alignment, Font

p = Path("02 Business architecture and process/Recovery Workbench Case and Workflow Model v6.xlsx")
wb = openpyxl.load_workbook(p)

order = [
    "Read me",
    "Stages", "Elements", "Case status", "Status transitions", "Milestones",
    "Tasks", "Event listeners", "Sentries", "Case file",
    "Workflow model (v5)", "Stage ownership (v5)", "Case file ownership (v5)",
    "Change log", "Realignment changes",
]
present = [s for s in order if s in wb.sheetnames]
for i, name in enumerate(present):
    wb.move_sheet(name, offset=i - wb.sheetnames.index(name))

widths = {
    "Read me": [26, 110],
    "Workflow model (v5)": [20, 26, 42, 12, 22, 14, 16, 16, 60, 14, 70],
    "Stage ownership (v5)": [34, 18, 32, 12, 18, 14, 16, 34, 70],
    "Case file ownership (v5)": [22, 44, 30, 40, 22, 14, 55, 70],
    "Change log": [10, 18, 55, 12, 45],
    "Realignment changes": [24, 110, 60],
}
for name, ws_widths in widths.items():
    ws = wb[name]
    for i, w in enumerate(ws_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    for row in ws.iter_rows():
        for c in row:
            if c.value is not None and isinstance(c.value, str):
                c.alignment = Alignment(wrap_text=True, vertical="top")
    if name == "Workflow model (v5)":
        ws.freeze_panes = "A6"
        for c in ws[5]:
            c.font = Font(bold=True)
    if name == "Stage ownership (v5)":
        ws.freeze_panes = "A6"
        for c in ws[5]:
            c.font = Font(bold=True)
    if name == "Case file ownership (v5)":
        ws.freeze_panes = "A6"
        for c in ws[5]:
            c.font = Font(bold=True)
    if name == "Change log":
        for c in ws[3]:
            c.font = Font(bold=True)
    if name == "Realignment changes":
        for c in ws[5]:
            c.font = Font(bold=True)

wb.save(p)
print("FORMATTED", p)
print("SHEETS:", wb.sheetnames)
