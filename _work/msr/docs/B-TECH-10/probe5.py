import docx

d = docx.Document(r"05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx")
for ti in (0, 1, 2):
    t = d.tables[ti]
    print("table", ti, "cols", len(t.columns), "rows", len(t.rows))
    for ci in range(len(t.columns)):
        r0 = t.cell(0, ci).paragraphs[0].runs
        r1 = t.cell(1, ci).paragraphs[0].runs
        print("  col", ci, "hdr bold", [r.bold for r in r0][:2], "body bold", [r.bold for r in r1][:2])
    print("  tblW", t._tbl.tblPr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tblW").attrib)
