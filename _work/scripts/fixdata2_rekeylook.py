import openpyxl
pairs=[('recovery_case','primary_customer_id','primary_person_key'),('case_account','account_id','account_key'),('case_party','party_id','person_key'),('notice','party_id','person_key'),('listing','asset_id','asset_key'),('asset_sale','asset_id','asset_key'),('debt_sale_account','account_id','account_key'),('interaction','party_id','person_key'),('interaction','contact_point_id','contact_key'),('document','party_id','person_key'),('proceeds','account_payment_id','payment_code'),('case_list_row','account_id','account_key'),('case_entry_exclusion','account_id','account_key'),('signature_request','party_id','person_key')]
dc=openpyxl.load_workbook('06 Data/Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx')['Fields']
ldm=openpyxl.load_workbook('06 Data/Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx')['Fields']
print([c.value for c in ldm[4]])
L={}
for r in ldm.iter_rows(min_row=5,values_only=True):
    L[(r[1],r[2])]=r
for t,o,n in pairs:
    for r in dc.iter_rows(min_row=5):
        if r[1].value==t and r[2].value in (o,n):
            print('DC', r[0].row, [c.value for c in r])
    for k in [(t,o),(t,n)]:
        if k in L: print('LDM', L[k])
    # match by entity column maybe different
