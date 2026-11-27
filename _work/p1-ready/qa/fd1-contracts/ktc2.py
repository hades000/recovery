import openpyxl,re
wb=openpyxl.load_workbook('stage/05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v3.xlsx',read_only=True,data_only=True)
for row in wb['Events'].iter_rows(values_only=True):
    if row and row[0] in ('EV-26','EV-27'): print(row[0], row[9])
g=set()
for ws in wb:
    for row in ws.iter_rows(values_only=True):
        for v in row:
            for m in re.findall(r'rwb-[a-z-]+\.rwb\.source-data\.events\.v1',str(v)): g.add(m)
print(g)
for row in wb['ACLs'].iter_rows(values_only=True):
    if row and row[0] in ('rwb-payment','rwb-writeoff','rwb-deviation','rwb-case','gateway-bff') and 'source-data.events.v1.retry' in str(row[3]):
        print([str(x)[:300] for x in row])
