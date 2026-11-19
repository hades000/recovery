import openpyxl
p = r'06 Data/Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx'
wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
fld = [r for r in list(wb['Fields'].iter_rows(values_only=True))[4:] if r[1]]
want = {'v_ace_valuation', 'v_ace_score', 'valuation_ext', 'party_ext', 'contact_point_ext', 'account_ext'}
for r in fld:
    if r[1] in want:
        print(r[0], '|', r[1], '|', r[2], '|', r[3], '|', r[4], '|', r[7], '|', r[9], '|', r[10], '|', r[14])
