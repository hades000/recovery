# -*- coding: utf-8 -*-
import csv
import io
import openpyxl

# 1. fields.csv: the contact view column is contact_value, not value
rows = list(csv.DictReader(io.open(r'_work\data\fields.csv', encoding='utf-8')))
for r in rows:
    if r['Field ID'] == 'DF-PTY-016':
        r['Read path'] = 'v_ace_contact.contact_value'
with io.open(r'_work\data\fields.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# 2. LDM v7: rename the 14 re-keyed fields and repoint them
LDM = r'06 Data\Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx'
REKEY = [
    ('recovery_case', 'primary_customer_id', 'primary_person_key', 'v_ace_customer'),
    ('case_account', 'account_id', 'account_key', 'v_ace_account'),
    ('case_party', 'party_id', 'person_key', 'v_ace_customer'),
    ('notice', 'party_id', 'person_key', 'v_ace_customer'),
    ('listing', 'asset_id', 'asset_key', 'v_ace_asset'),
    ('asset_sale', 'asset_id', 'asset_key', 'v_ace_asset'),
    ('debt_sale_account', 'account_id', 'account_key', 'v_ace_account'),
    ('interaction', 'party_id', 'person_key', 'v_ace_customer'),
    ('interaction', 'contact_point_id', 'contact_key', 'v_ace_contact'),
    ('document', 'party_id', 'person_key', 'v_ace_customer'),
    ('proceeds', 'account_payment_id', 'payment_code', 'v_ace_payment'),
    ('case_list_row', 'account_id', 'account_key', 'v_ace_account'),
    ('case_entry_exclusion', 'account_id', 'account_key', 'v_ace_account'),
    ('signature_request', 'party_id', 'person_key', 'v_ace_customer'),
]
wb = openpyxl.load_workbook(LDM)
ws = wb['Fields']
n = 0
for r in range(5, ws.max_row + 1):
    ent = ws.cell(row=r, column=2).value
    fld = ws.cell(row=r, column=3).value
    for table, old, new, target in REKEY:
        if ent == table and fld == old:
            ws.cell(row=r, column=3, value=new)
            ws.cell(row=r, column=4, value='TEXT')
            ws.cell(row=r, column=5, value='varchar(255)')
            ws.cell(row=r, column=6, value='255')
            ws.cell(row=r, column=11, value=target + ' (business key; no foreign key)')
            ws.cell(row=r, column=12, value='ACE')
            ws.cell(row=r, column=13, value='public.' + target.replace('v_ace_', '') + '.' + new)
            n += 1
            break
print('renamed', n)

# ACE mapping tab read path
ws2 = wb['ACE mapping']
for r in range(2, ws2.max_row + 1):
    if ws2.cell(row=r, column=1).value == 'DF-PTY-016':
        ws2.cell(row=r, column=6, value='v_ace_contact.contact_value')
wb.save(LDM)
print('saved LDM')
