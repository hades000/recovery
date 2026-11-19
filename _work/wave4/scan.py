# -*- coding: utf-8 -*-
import openpyxl, docx, pptx

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

def texts(f):
    out = []
    if f.endswith(".xlsx"):
        wb = openpyxl.load_workbook(f, data_only=True)
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str):
                        out.append((ws.title, c.coordinate, c.value))
    elif f.endswith(".docx"):
        d = docx.Document(f)
        for i, p in enumerate(d.paragraphs):
            out.append(("para", i, p.text))
        for ti, t in enumerate(d.tables):
            for ri, row in enumerate(t.rows):
                for ci, cell in enumerate(row.cells):
                    out.append(("tbl%d" % ti, "%d,%d" % (ri, ci), cell.text))
    else:
        prs = pptx.Presentation(f)
        for si, s in enumerate(prs.slides, 1):
            for sh in s.shapes:
                if sh.has_text_frame:
                    out.append(("slide%d" % si, sh.name, sh.text_frame.text))
                if sh.has_table:
                    for ri, row in enumerate(sh.table.rows):
                        for ci, cell in enumerate(row.cells):
                            out.append(("slide%d" % si, "%d,%d" % (ri, ci), cell.text))
    return out

TOKENS = ["115", " 33 ", "42 controls", "12 risks", "v4.xlsx", "v2.docx", "v3.pptx",
          "29 Nov", "27 Dec", "24 Jan", "18 Apr", "16 May", "13 Jun", "RWB-E2-023",
          "E2-023", "116 contradictions", "eight data load"]
for f in files:
    hits = []
    for where, loc, txt in texts(f):
        for t in TOKENS:
            if t in txt:
                hits.append((where, loc, t, txt[:120]))
    print("=" * 60)
    print(f)
    print("  hits:", len(hits))
    for h in hits[:12]:
        print("   ", h)
