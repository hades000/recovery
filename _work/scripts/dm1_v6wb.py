import openpyxl
wb = openpyxl.load_workbook(r'06 Data/Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx', read_only=True, data_only=True)
COPY = ['asset','collateral','account_collateral','valuation','party','contact_point','loan_account','account_payment','score','collections_history','party_product']
STD = {'id','is_active','state','version','created_at','created_by','updated_at','updated_by'}
for r in wb['Fields'].iter_rows(min_row=5, values_only=True):
    if r[1] in COPY and r[2] not in STD and not (r[11] and r[11] not in ('Workbench','None')):
        print(r[0], r[1], r[2], r[3], r[4], r[6], r[8], r[10], r[11], r[12], '|', r[14])
