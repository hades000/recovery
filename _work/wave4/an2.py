import openpyxl
seq = openpyxl.load_workbook(r"11 Delivery and operations\Recovery Workbench Build Sequence Epic 1 and Epic 2 v4.xlsx", data_only=True)["Sequence"]
sids = [seq.cell(r,2).value for r in range(5, seq.max_row+1)]
e1 = openpyxl.load_workbook(r"04 User stories\Recovery Workbench User Stories Epic 1 v8.xlsx", data_only=True)["Stories"]
v8 = [e1.cell(r,1).value for r in range(4, e1.max_row+1) if e1.cell(r,1).value]
e2 = openpyxl.load_workbook(r"04 User stories\Recovery Workbench User Stories Epic 2 v6.xlsx", data_only=True)["Stories"]
v6 = [e2.cell(r,1).value for r in range(4, e2.max_row+1) if e2.cell(r,1).value]
print("seq E1 not in v8:", sorted(set(sids)-set(v8)))
print("v8 not in seq:", sorted(set(v8)-set(sids)))
print("seq E2 not in v6:", sorted(set(sids)-set(v6)))
print("v6 not in seq:", sorted(set(v6)-set(sids)))
print("len v8 e1 only:", len([x for x in v8 if x.startswith('RWB-E1')]), "te:", len([x for x in v8 if x.startswith('RWB-TE')]))
