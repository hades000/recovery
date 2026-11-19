import sys, openpyxl
for p in sys.argv[1:]:
    wb = openpyxl.load_workbook(p)
    pr = wb.properties
    print(p)
    print("  title:", pr.title, "| subject:", pr.subject, "| creator:", pr.creator, "| modified:", pr.modified, "| created:", pr.created, "| description:", pr.description)
    print("  sheets:", [ws.title for ws in wb.worksheets])
