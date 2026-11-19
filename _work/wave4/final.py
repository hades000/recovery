# -*- coding: utf-8 -*-
import openpyxl, docx, pptx, os

files = [
    r"11 Delivery and operations\Recovery Workbench Build Sequence Epic 1 and Epic 2 v5.xlsx",
    r"11 Delivery and operations\Recovery Workbench Story Build Order v2.docx",
    r"11 Delivery and operations\Recovery Workbench Dependency Map v3.xlsx",
    r"11 Delivery and operations\Recovery Workbench Risks Assumptions Issues and Dependencies v3.xlsx",
    r"11 Delivery and operations\Recovery Workbench Cutover and Go Live Plan v3.docx",
    r"11 Delivery and operations\Recovery Workbench Release Plan v4.pptx",
    r"11 Delivery and operations\Recovery Workbench Release Plan v4.xlsx",
    r"10 Policy, controls and compliance\Recovery Workbench Controls Catalog v3.xlsx",
    r"04 User stories\Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v3.xlsx",
]
for f in files:
    if f.endswith(".xlsx"):
        wb = openpyxl.load_workbook(f)
        n = sum(ws.max_row for ws in wb.worksheets)
        print("OK xlsx", n, "cells-rows", os.path.getsize(f), f)
    elif f.endswith(".docx"):
        d = docx.Document(f)
        print("OK docx", len(d.paragraphs), "paras", len(d.tables), "tables", os.path.getsize(f), f)
    else:
        p = pptx.Presentation(f)
        print("OK pptx", len(p.slides), "slides", os.path.getsize(f), f)
