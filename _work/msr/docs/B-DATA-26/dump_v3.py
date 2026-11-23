import json, sys
import openpyxl
from openpyxl.utils import get_column_letter

SRC = "06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx"

wb = openpyxl.load_workbook(SRC, data_only=False)
out = {"source": SRC, "sheets": []}
for ws in wb.worksheets:
    sh = {"title": ws.title, "max_row": ws.max_row, "max_col": ws.max_column,
          "dims": ws.dimensions, "merged": [str(r) for r in ws.merged_cells.ranges],
          "col_widths": {k: v.width for k, v in ws.column_dimensions.items()},
          "rows": []}
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=ws.max_column):
        cells = []
        for c in row:
            v = c.value
            if v is not None or (c.fill is not None and c.fill.fgColor and c.fill.fgColor.rgb not in (None, "00000000")):
                cells.append({"ref": c.coordinate, "v": v})
        if cells:
            sh["rows"].append(cells)
    out["sheets"].append(sh)

with open("_work/msr/docs/B-DATA-26/v3_dump.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1, default=str)

print("sheets:", [s["title"] for s in out["sheets"]])
for s in out["sheets"]:
    print("---", s["title"], s["dims"], "merged:", s["merged"], "widths:", s["col_widths"])
    for r in s["rows"]:
        print(" | ".join(f"{c['ref']}={c['v']!r}" for c in r))
