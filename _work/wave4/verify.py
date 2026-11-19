# -*- coding: utf-8 -*-
import openpyxl, docx, pptx, sys, os, zipfile, re

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
    print("=" * 70)
    print(f, os.path.getsize(f), "bytes")
    texts = []
    if f.endswith(".xlsx"):
        wb = openpyxl.load_workbook(f, data_only=True)
        print("  sheets:", [ws.title for ws in wb.worksheets])
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str):
                        texts.append(c.value)
    elif f.endswith(".docx"):
        d = docx.Document(f)
        print("  paragraphs:", len(d.paragraphs), "tables:", len(d.tables),
              "words:", sum(len(p.text.split()) for p in d.paragraphs))
        texts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                for cell in row.cells:
                    texts.append(cell.text)
    else:
        prs = pptx.Presentation(f)
        print("  slides:", len(prs.slides))
        for s in prs.slides:
            for sh in s.shapes:
                if sh.has_text_frame:
                    texts.append(sh.text_frame.text)
                if sh.has_table:
                    for row in sh.table.rows:
                        for cell in row.cells:
                            texts.append(cell.text)
    bad = sorted({ch for t in texts for ch in t if ord(ch) > 127})
    print("  non-ascii:", [(c, hex(ord(c))) for c in bad] or "none")
    words = " ".join(texts)
    for token in ["TODO", "TBD", "XXX", "lorem", "placeholder", "[", "  "]:
        if token in words:
            print("  token hit:", repr(token), words[max(0, words.find(token) - 40):words.find(token) + 40])
