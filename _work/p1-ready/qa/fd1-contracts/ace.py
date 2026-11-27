import openpyxl
wb=openpyxl.load_workbook('ACE schema/ACE-data-schema_20261104.xlsx',read_only=True,data_only=True)
print(wb.sheetnames[:40])
want={'days_since_last_contact','days_since_last_collection_activity','number_reschedules','tdr_aging','delay_days','expiry_date','collateral_value','register_date','in_active','birth_date','deceased_date','amount_of_guarantee','date_of_guarantee','account_status_date','contract_date','last_tdr_date','total_balance','insured_value'}
for ws in wb:
    for row in ws.iter_rows(values_only=True):
        vals=[str(v) for v in row if v is not None]
        if any(v.lower() in want for v in vals):
            print(ws.title, vals[:8])
