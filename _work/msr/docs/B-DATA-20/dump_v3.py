"""Dump Recovery Workbench Data Ownership and Stewardship v3.xlsx cell by cell."""
import json
import openpyxl

SRC = "06 Data/Recovery Workbench Data Ownership and Stewardship v3.xlsx"
wb = openpyxl.load_workbook(SRC)
out = {"sheets": [], "cells": {}}
for ws in wb.worksheets:
    out["sheets"].append({"title": ws.title, "dims": ws.dimensions,
                          "max_row": ws.max_row, "max_column": ws.max_column,
                          "merged": [str(m) for m in ws.merged_cells.ranges]})
    grid = []
    for r in range(1, ws.max_row + 1):
        row = []
        for c in range(1, ws.max_column + 1):
            v = ws.cell(row=r, column=c).value
            row.append("" if v is None else str(v))
        grid.append(row)
    out["cells"][ws.title] = grid

with open("_work/msr/docs/B-DATA-20/v3_dump.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

for s in out["sheets"]:
    print("=" * 90)
    print(s)
    for i, row in enumerate(out["cells"][s["title"]], start=1):
        print(i, " | ".join(row))
