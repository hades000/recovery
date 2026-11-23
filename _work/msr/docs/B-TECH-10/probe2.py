import docx

d = docx.Document(r"05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx")
for i, t in enumerate(d.tables):
    try:
        st = t.style.name
    except Exception as e:
        st = f"<{e}>"
    tblPr = t._tbl.tblPr
    print(i, "rows", len(t.rows), "cols", len(t.columns), "style", st)
    print("   tblPr:", tblPr.xml.replace("\n", " ")[:400])
    print("   first cell:", t.cell(0, 0).text[:40])
print("style names with tbl:", [s.name for s in d.styles if s.type == 3])
