import openpyxl, copy
P = '06 Data/Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx'
wb = openpyxl.load_workbook(P)
F = wb['Fields']
ren = {'DF-CAS-004': 'primary_person_key', 'DF-CAS-026': 'account_key', 'DF-CAS-032': 'person_key',
       'DF-LEG-030': 'person_key', 'DF-SAL-002': 'asset_key', 'DF-SAL-010': 'asset_key',
       'DF-SAL-033': 'account_key', 'DF-INT-003': 'person_key', 'DF-INT-022': 'contact_key',
       'DF-DOC-003': 'person_key', 'DF-FIN-004': 'payment_code', 'DF-RPT-005': 'account_key',
       'DF-CAS-057': 'account_key', 'DF-DOC-100': 'person_key'}
def cpstyle(src, dst):
    dst.font = copy.copy(src.font); dst.fill = copy.copy(src.fill); dst.border = copy.copy(src.border)
    dst.alignment = copy.copy(src.alignment); dst.number_format = src.number_format; dst.protection = copy.copy(src.protection)
tmpl = 6  # DF-CAS-002, an Indirect identifier row
assert F.cell(tmpl, 4).value == 'Indirect identifier'
done = 0
for r in range(5, F.max_row + 1):
    fid = F.cell(r, 1).value
    if fid in ren:
        F.cell(r, 3).value = ren[fid]
        for c, v in zip(range(4, 10), ['Indirect identifier', 'Confidential', 'Yes',
                                     "Shown within the role's scope; masked in UAT",
                                     'Contract (PDPA section 24)', 'Per data product (DL26)']):
            F.cell(r, c).value = v
            cpstyle(F.cell(tmpl, c), F.cell(r, c))
        if fid == 'DF-INT-022':
            F.cell(r, 10).value = ('The ACE contact reached, held as contact_type:key (phone_key, email_key or address_key); '
                                   'no foreign key. The number or address is read through v_ace_contact and masked for display at E1-037')
        done += 1
assert done == 14, done
last = F.max_row
# Summary: restore formulas
S = wb['Summary']
for r in range(5, 11):
    S.cell(r, 3).value = '=COUNTIF(Fields!$D$5:$D$%d,A%d)' % (last, r)
S['C11'] = '=SUM(C5:C10)'
# Identifiers: rebuild from Fields in Fields order
I = wb['Identifiers']
cats = ('Direct identifier', 'Sensitive', 'Indirect identifier')
rows = [[F.cell(r, c).value for c in (1, 2, 3, 4, 5, 7, 10)] for r in range(5, last + 1) if F.cell(r, 4).value in cats]
old = {I.cell(r, 1).value for r in range(5, I.max_row + 1)}
new = {x[0] for x in rows}
assert old <= new and len(new - old) == 14, (old - new, new - old)
oldmax = I.max_row
styles = {}
for r in range(5, oldmax + 1):
    styles.setdefault(I.cell(r, 4).value, r)
for i, vals in enumerate(rows):
    r = 5 + i
    srow = styles[vals[3]]
    for c, v in enumerate(vals, 1):
        I.cell(r, c).value = v
    if r > oldmax or True:
        for c in range(1, 8):
            cpstyle(I.cell(srow, c), I.cell(r, c))
    if I.row_dimensions[srow].height is not None:
        I.row_dimensions[r].height = I.row_dimensions[srow].height
n = len(rows)
I.auto_filter.ref = 'A4:G%d' % (4 + n)
I['A2'] = I['A2'].value.replace('94 fields', '%d fields' % n)
# Handling restricted / stored
H = wb['Handling']
assert H['A5'].value == 'Restricted' and H['B5'].value == 'Stored'
H['C5'] = 'ACE source fields stored in ACE only; Workbench Restricted fields encrypted at rest. Identification numbers never leave ACE in clear'
wb.properties.title = 'Recovery Workbench Data Classification and Personal Data Inventory v4'
wb.save(P)
from collections import Counter
print(n, Counter(F.cell(r, 4).value for r in range(5, last + 1)))
