import openpyxl,re
wb=openpyxl.load_workbook('stage/05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v3.xlsx',read_only=True,data_only=True)
print(wb.sheetnames)
for ws in wb:
    n=0
    for row in ws.iter_rows(values_only=True):
        t=' | '.join(str(v) for v in row if v is not None)
        if re.search(r'source-data\.events|retry|PartnerResult',t) and n<14:
            print(ws.title,'::',t[:330]); n+=1
