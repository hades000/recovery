import openpyxl, json
p = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\12 Project communication\Recovery Workbench Document Control Sheet v12.xlsx"
wb = openpyxl.load_workbook(p)
ws = wb["Control sheet"]
rows=[]
for r in range(5, ws.max_row+1):
    vals=[ws.cell(r,c).value for c in range(1,12)]
    if vals[0] is None and vals[3] is None: continue
    rows.append(vals)
print(len(rows))
print("last rows:")
for v in rows[-3:]: print(v[:5])
c=ws.cell(5,1)
print("style", c.font.name, c.font.sz, c.font.b, "fill", c.fill.fgColor.rgb, "align", c.alignment.wrap_text, c.alignment.vertical)
print("widths", {k:v.width for k,v in ws.column_dimensions.items()})
print("freeze", ws.freeze_panes, "autofilter", ws.auto_filter.ref, "merged", ws.merged_cells.ranges)
json.dump([[str(x) if x is not None else None for x in v] for v in rows], open(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\msr\docs\D2-CTL\src_rows.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
