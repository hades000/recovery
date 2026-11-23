import openpyxl

for p in ("06 Data/Recovery Workbench Source to Target Mapping v4.xlsx",
          "06 Data/Recovery Workbench Source to Target Mapping v5.xlsx"):
    wb = openpyxl.load_workbook(p)
    pr = wb.properties
    print(p)
    print("  creator:", pr.creator, "| lastModifiedBy:", pr.lastModifiedBy, "| title:", pr.title,
          "| company:", getattr(pr, "company", None))
