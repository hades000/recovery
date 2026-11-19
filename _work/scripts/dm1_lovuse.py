import openpyxl
wb = openpyxl.load_workbook(r'06 Data/Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx', read_only=True, data_only=True)
L = ['LOV-APPRAISAL', 'LOV-ASSET-TYPE', 'LOV-COLL-TYPE', 'LOV-CONSENT', 'LOV-CONTACT-SRC', 'LOV-CREDIT-RESULT', 'LOV-DQ-RULE-TYPE', 'LOV-DQ-STATUS', 'LOV-ENCUMBRANCE', 'LOV-HOLDING', 'LOV-ID-TYPE', 'LOV-INTERFACE-RUN', 'LOV-LOAD-STATUS', 'LOV-OCCUPANCY', 'LOV-PARTY-TYPE', 'LOV-PRODUCT-STATUS', 'LOV-TRACKER-DECISION', 'LOV-TRACKER-LOCATION', 'LOV-TRACKER-STATUS', 'LOV-TRANSFER-IN', 'LOV-UPDATE-CYCLE','LOV-TRANSPORT','LOV-ROUTE','LOV-BUCKET','LOV-BU']
for r in wb['Fields'].iter_rows(min_row=5, values_only=True):
    if r[8] in L: print(r[8], r[0], r[1], r[2])
ws = wb['Lists of values']
for r in ws.iter_rows(min_row=1, max_row=3, values_only=True): print(r)
ws = wb['Loaded lists']
for r in ws.iter_rows(values_only=True): print(r)
