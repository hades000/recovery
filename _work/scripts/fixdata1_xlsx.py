"""Fix agent data1: CDM v6 xlsx (D1, minors), DQ v3 xlsx (D4), Party MDM v3 xlsx (D5/D8, D6, D7, D9)."""
import copy
import os
import openpyxl

ROOT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\06 Data'


def p(name):
    return os.path.join(ROOT, name)


def set_title(wb, fname):
    wb.properties.title = os.path.splitext(fname)[0]


# ---------- CDM v6 xlsx ----------
f = 'Recovery Workbench Conceptual Data Model v6.xlsx'
wb = openpyxl.load_workbook(p(f))
g = wb['Gaps']
assert g['B40'].value == 'efs_action' and g['E40'].value == 2
g['E40'] = 3  # D1: contact_result serves 2 fields -> 3 read; column sums to 80
assert sum(g.cell(r, 5).value for r in range(24, 41)) == g['E41'].value == 80
assert g['D16'].value == 'All loaded data products'
g['D16'] = 'All data products read from ACE views'  # minor: Workbench loads nothing
dp = wb['Data products']
last = wb['Entities'].max_row  # 126
for r in range(5, 19):
    dp.cell(r, 10).value = '=COUNTIF(Entities!$C$5:$C$%d,A%d&" "&B%d)' % (last, r, r)
dp['J19'] = '=SUM(J5:J18)'
set_title(wb, f)
wb.save(p(f))

# ---------- DQ and Reconciliation Rules v3 ----------
f = 'Recovery Workbench Data Quality and Reconciliation Rules v3.xlsx'
wb = openpyxl.load_workbook(p(f))
ws = wb['Reconciliations']
assert ws['A9'].value == 'REC-05' and ws['A13'].value == 'REC-09'
assert ws['B13'].value == 'Notices sent to WIN'
# swap the bodies of rows 9 and 13 so REC-05 = WIN barcodes (as v2 and other live docs), REC-09 = business keys
for c in range(2, 8):
    a, b = ws.cell(9, c), ws.cell(13, c)
    a.value, b.value = b.value, a.value
qm = wb['Quality measures']
assert qm['B10'].value.endswith('(REC-05)')
qm['B10'] = qm['B10'].value.replace('(REC-05)', '(REC-09)')
set_title(wb, f)
wb.save(p(f))

# ---------- Party and Customer MDM v3 xlsx ----------
f = 'Recovery Workbench Party and Customer Master Data Design v3.xlsx'
wb = openpyxl.load_workbook(p(f))
ws = wb['Party fields']
# D9: annotate the three Section B columns
for coord in ('G13', 'G16', 'G20'):
    v = ws[coord].value
    assert v.endswith('Tier 2, added by RWB-ACE-001'), v
    ws[coord] = v.replace('Tier 2, added by RWB-ACE-001', 'Tier 2 column in v_ace_customer (Section B, after RWB-ACE-001)')
# D7: add v_ace_ca_relation rows after the v_ace_contact block (row 37)
assert ws['A37'].value == 'v_ace_contact' and ws['A38'].value == 'contact_point_ext'
new = [
    ('person_key', 'TEXT', 'varchar(255)', 'ca_relation.person_key', 'ACE customer on the account; business key, no foreign key'),
    ('account_key', 'TEXT', 'varchar(255)', 'ca_relation.account_key', 'ACE account the customer is related to; business key, no foreign key'),
    ('relation_type', 'TEXT', 'varchar(255)', 'ca_relation.relation_type', 'Borrower, co-borrower or guarantor on the account'),
    ('amount_of_guarantee', 'NUMBER', 'numeric(38,2)', 'ca_relation.amount_of_guarantee', 'Amount the guarantor guarantees; blank for a borrower'),
    ('date_of_guarantee', 'DATE', 'date', 'ca_relation.date_of_guarantee', 'Date the guarantee was given; blank for a borrower'),
]
n = len(new)
old_max = ws.max_row  # 51
heights = {r: ws.row_dimensions[r].height for r in range(38, old_max + 1)}
ws.insert_rows(38, n)
for r, h in heights.items():
    ws.row_dimensions[r + n].height = h
for i, (fld, dt, pt, sf, meaning) in enumerate(new):
    r = 38 + i
    vals = ['v_ace_ca_relation', fld, dt, pt, 'ACE', sf, meaning]
    for c, v in enumerate(vals, start=1):
        src = ws.cell(37, c)
        dst = ws.cell(r, c)
        dst.value = v
        dst._style = copy.copy(src._style)
    ws.row_dimensions[r].height = 16.8
ws.auto_filter.ref = 'A4:G%d' % (old_max + n)
# D5/D8 + D6: M5 stays with the Workbench partner master; restore the case-merge rule
mr = wb['Match rules']
assert mr['A9'].value == 'M5'
mr['A2'] = ('M1 to M4 run in ACE ingestion, before a customer row reaches the Workbench. '
            'M5 runs in the Workbench partner master.')
mr['D9'] = ('In the Workbench partner master, not in ACE: a partner firm is a Workbench record. '
            'The partner and agency manager confirms the panel entry')
mr['A11'] = ('M1 to M4 run in ACE ingestion. The Workbench never re-matches, merges or re-masters a person: '
             'it reads the person_key that ACE publishes in v_ace_customer. A suspected duplicate is raised with '
             'the ACE data steward. M5 runs in the Workbench partner master, because a partner firm is a Workbench '
             'record, not an ACE customer. A case is never merged by the party match; duplicate cases follow R-UNI-17.')
mr.row_dimensions[11].height = 55.2
set_title(wb, f)
wb.save(p(f))
print('xlsx done')
