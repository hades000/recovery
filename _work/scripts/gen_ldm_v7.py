# -*- coding: utf-8 -*-
"""Build Logical Data Model and Data Dictionary v7 from v6 and the v5 dictionary."""
import csv
import io
import openpyxl

SRC = r'06 Data\Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx'
OUT = r'06 Data\Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx'

REMOVED = {'loan_account', 'account_payment', 'party', 'contact_point', 'collateral', 'account_collateral',
           'collections_history', 'party_product', 'valuation', 'score', 'asset',
           'load_run', 'dq_exception', 'dq_rule', 'source_field_map', 'source_code_map',
           'interface_run', 'interface_signoff', 'tracker_inventory', 'tracker_row'}
DROP_COLS = {('treatment', 'nleads_ref'), ('treatment', 'credit_result'),
             ('treatment', 'credit_result_reason'), ('treatment', 'credit_result_at'),
             ('signature_request', 'external_ref'), ('role', 'entra_group')}

def opencsv(path):
    raw = io.open(path, 'rb').read()
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
        text = raw.decode('utf-16')
    else:
        text = raw.decode('utf-8-sig')
    return list(csv.DictReader(io.StringIO(text)))


objs = opencsv(r'_work\data\v5_objects.csv')
fields = opencsv(r'_work\data\v5_fields.csv')
by_obj = {}
for f in fields:
    by_obj.setdefault(f['object_name'], []).append(f)

wb = openpyxl.load_workbook(SRC)
ent = wb['Entities']
fld = wb['Fields']

# ---------- Entities ----------
rows = [list(r) for r in ent.iter_rows(min_row=5, values_only=True)
        if r[0] and str(r[0]).strip() != 'Total' and str(r[0]) not in REMOVED]
existing = {r[0] for r in rows}

NEW_ENT = {
    'party_ext': ('Party extension', 'Party', 'DP02', 'Workbench flags about an ACE customer: vulnerability, death override, bankruptcy and fraud.', 'Workbench', 'Workbench; keyed by ACE person_key'),
    'contact_point_ext': ('Contact point extension', 'Party', 'DP02', 'Consent and contact quality for an ACE phone, email or address.', 'Workbench', 'Workbench; keyed by ACE phone_key, email_key or address_key'),
    'account_ext': ('Account extension', 'Account and arrears', 'DP01', 'Workbench state about an ACE account, such as an open dispute.', 'Workbench', 'Workbench; keyed by ACE account_key'),
    'valuation_ext': ('Valuation extension', 'Collateral and asset', 'DP06', 'The Workbench decision about an ACE appraisal: accepted, valuer, stale and age.', 'Workbench', 'Workbench; keyed by ACE valuation_key'),
}

ent_rows = []
for r in rows:
    ent_rows.append(r[:7] + [len(by_obj.get(r[0], [])), ''])
for name, (biz, subj, dp, what, sor, ace) in NEW_ENT.items():
    ent_rows.append([name, biz, subj, dp, what, sor, ace, len(by_obj.get(name, [])), ''])
for o in objs:
    if o['object_name'].startswith('v_ace_'):
        ent_rows.append([o['object_name'], o['business_name'], 'ACE read', 'ACE', o['description'], 'ACE', 'Read-only view',
                         len(by_obj.get(o['object_name'], [])), ''])

ent.delete_rows(4, ent.max_row)
for c, h in enumerate(['Entity', 'Business name', 'Subject area', 'Data product', 'What it is', 'System of record', 'ACE', 'Fields', 'Personal data fields'], 1):
    ent.cell(row=4, column=c, value=h)
ent['A1'] = 'Entities'
ent['A2'] = ('%d entities: 88 Workbench tables, 4 extension tables and %d ACE source views. '
             'Field counts are calculated from the Fields tab.' % (len(ent_rows), len([o for o in objs if o['object_name'].startswith('v_ace_')])))
for i, row in enumerate(ent_rows, 5):
    for c, v in enumerate(row, 1):
        ent.cell(row=i, column=c, value=v)

# ---------- Fields ----------
frows = []
for r in fld.iter_rows(min_row=5, values_only=True):
    if not r[0]:
        continue
    if r[1] in REMOVED or (r[1], r[2]) in DROP_COLS:
        continue
    frows.append(list(r))

existing_ids = {r[0] for r in frows}
for f in fields:
    if f['field_id'] in existing_ids:
        continue
    pt = f['physical_type']
    length = ''
    if pt.startswith('varchar(') or pt.startswith('numeric('):
        length = pt[pt.find('(') + 1:pt.find(')')]
    frows.append([f['field_id'], f['object_name'], f['field_name'], f['data_type'], pt, length,
                  'Yes' if f['is_mandatory'] == 'true' else 'No', 'None', f['lov_code'] or 'None',
                  'None', f['references_object'] or 'None', f['source_system'],
                  f['source_field'] or 'None', 'Yes' if f['is_personal'] == 'true' else 'No', f['description']])

fld.delete_rows(4, fld.max_row)
for c, h in enumerate(['BR Field ID', 'Entity', 'Field', 'Data type', 'Physical type', 'Length', 'Mandatory',
                       'Default', 'List of values', 'Key', 'Refers to', 'Source system', 'Source field',
                       'Personal data', 'Meaning'], 1):
    fld.cell(row=4, column=c, value=h)
fld['A1'] = 'Data dictionary'
fld['A2'] = ('%d fields in %d entities. Every source field is resolved in the ACE mapping tab: '
             '52 already in ACE, 80 added by RWB-ACE-001, 1 in an extension table.' % (len(frows), len(ent_rows)))
for i, row in enumerate(frows, 5):
    for c, v in enumerate(row, 1):
        fld.cell(row=i, column=c, value=v)

# ---------- Relationships ----------
rel = wb['Relationships']
rrows = [list(r) for r in rel.iter_rows(min_row=5, values_only=True) if r[0]]
REKEY = {
    ('recovery_case', 'primary_customer_id'): ('primary_person_key', 'v_ace_customer'),
    ('case_account', 'account_id'): ('account_key', 'v_ace_account'),
    ('case_party', 'party_id'): ('person_key', 'v_ace_customer'),
    ('notice', 'party_id'): ('person_key', 'v_ace_customer'),
    ('listing', 'asset_id'): ('asset_key', 'v_ace_asset'),
    ('asset_sale', 'asset_id'): ('asset_key', 'v_ace_asset'),
    ('debt_sale_account', 'account_id'): ('account_key', 'v_ace_account'),
    ('interaction', 'party_id'): ('person_key', 'v_ace_customer'),
    ('interaction', 'contact_point_id'): ('contact_key', 'v_ace_contact'),
    ('document', 'party_id'): ('person_key', 'v_ace_customer'),
    ('proceeds', 'account_payment_id'): ('payment_code', 'v_ace_payment'),
    ('case_list_row', 'account_id'): ('account_key', 'v_ace_account'),
    ('case_entry_exclusion', 'account_id'): ('account_key', 'v_ace_account'),
    ('signature_request', 'party_id'): ('person_key', 'v_ace_customer'),
}
newrel = []
for row in rrows:
    key = (row[0], row[1])
    if key in REKEY:
        nf, nt = REKEY[key]
        newrel.append([row[0], nf, nt, 'N:1', row[4], 'No foreign key; business key'])
    elif row[0] in REMOVED or row[2] in REMOVED:
        continue
    else:
        newrel.append(row)
rel.delete_rows(4, rel.max_row)
for c, h in enumerate(['Entity', 'Field', 'Refers to', 'Cardinality', 'Mandatory', 'Note'], 1):
    rel.cell(row=4, column=c, value=h)
for i, row in enumerate(newrel, 5):
    for c, v in enumerate(row[:6], 1):
        rel.cell(row=i, column=c, value=v)

# ---------- Sources ----------
src = wb['Sources']
src.delete_rows(4, src.max_row)
cnt_t1 = len([f for f in fields if f['source_system'] == 'ACE' and f['source_field'].startswith('public.')])
src_rows = [
    ('ACE, read through 30 views', 'Read-only, SELECT only; the only path to ACE', cnt_t1, 'v_ace_account, v_ace_customer, v_ace_collateral and the other views'),
    ('ACE additions (RWB-ACE-001)', 'Ingested by ACE; read through the views', len([f for f in fields if f['source_system'] == 'ACE' and not f['source_field'].startswith('public.')]), 'v_ace_valuation, v_ace_lawsuit, v_ace_batch_status and the other Tier 2 views'),
    ('Workbench', 'Written by the Workbench', len([f for f in fields if f['source_system'] == 'Workbench']), 'The case, extension tables, documents, decisions, reference data and agent runtime'),
]
for c, h in enumerate(['Source system', 'How it reaches the Workbench', 'Fields', 'Entities'], 1):
    src.cell(row=4, column=c, value=h)
for i, row in enumerate(src_rows, 5):
    for c, v in enumerate(row, 1):
        src.cell(row=i, column=c, value=v)

# ---------- ACE mapping ----------
if 'ACE mapping' in wb.sheetnames:
    del wb['ACE mapping']
ws = wb.create_sheet('ACE mapping', 5)
ws.append(['BR Field ID', 'Workbench entity', 'Workbench field', 'Disposition', 'ACE object column', 'Read path', 'Source system today', 'Note'])
for f in csv.DictReader(io.open(r'_work\data\fields.csv', encoding='utf-8')):
    ws.append([f['Field ID'], f['Entity'], f['Field'], f['Disposition'], f['ACE object column'],
               f['Read path'], f['Source system'], f['Note']])
for c in range(1, 9):
    ws.cell(row=1, column=c).font = openpyxl.styles.Font(bold=True, color='FFFFFF')
    ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width = [13, 22, 24, 18, 40, 40, 28, 70][c - 1]

wb.save(OUT)
print('saved', OUT, 'entities', len(ent_rows), 'fields', len(frows), 'relationships', len(newrel),
      'view entities', len([o for o in objs if o['object_name'].startswith('v_ace_')]))
