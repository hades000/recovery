"""Dump every cell and style of the v3 workbook to v3_dump.json for the build and verify steps."""
import json
from pathlib import Path

import openpyxl

V3 = "06 Data/Recovery Workbench Reporting and Analytics Data Model v3.xlsx"
OUT = Path("_work/msr/docs/B-DATA-23/v3_dump.json")


def cell(c):
    return {
        "v": c.value,
        "b": c.font.b,
        "sz": c.font.sz,
        "color": (c.font.color.rgb if c.font.color and c.font.color.type == "rgb" else None),
        "fill": (c.fill.fgColor.rgb if c.fill and c.fill.fgColor and c.fill.patternType else None),
        "wrap": c.alignment.wrap_text,
        "vert": c.alignment.vertical,
    }


wb = openpyxl.load_workbook(V3)
out = {"order": wb.sheetnames, "sheets": {}}
for name in wb.sheetnames:
    ws = wb[name]
    out["sheets"][name] = {
        "max_row": ws.max_row,
        "max_col": ws.max_column,
        "freeze": ws.freeze_panes,
        "grid": ws.sheet_view.showGridLines,
        "widths": {k: v.width for k, v in ws.column_dimensions.items()},
        "cells": {c.coordinate: cell(c) for row in ws.iter_rows() for c in row if c.value is not None},
    }
OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print("WROTE", OUT, {k: (v["max_row"], v["max_col"]) for k, v in out["sheets"].items()})
