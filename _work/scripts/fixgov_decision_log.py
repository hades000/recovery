import openpyxl, datetime
P = '01 Decisions and governance/Recovery Workbench Decision Log v9.xlsx'
wb = openpyxl.load_workbook(P)
wb.properties.title = 'Recovery Workbench Decision Log v9'
ws = wb['By owner']
assert ws['A30'].value == 'K. Book with the data architect' and ws['D30'].value == 'DL41'
assert ws['A36'].value == 'Risk with the product heads'
# shift rows 31..35 up to 30..34 (values only; styles are identical per column)
for r in range(30, 35):
    for c in range(1, 5):
        ws.cell(r, c).value = ws.cell(r + 1, c).value
ws['A35'] = 'ACE team lead'; ws['B35'] = 1
ws['C35'] = datetime.datetime(2026, 11, 21); ws['D35'] = 'DL43'
# DL06 recommendation: B covers named same-day triggers on top of the ACE batch
od = wb['Open decisions']
assert od['A11'].value == 'DL06'
old = od['E11'].value
new = ('B for the named same-day triggers, on top of the ACE batch ingestion; option A is superseded by D-RCV-35 '
       '(ACE ingests all source data in its batch, so the Workbench runs no batch load of its own). '
       'ACE has no real time feed today. Name the same-day triggers now: case transferred from EFS, payment received, legal event.')
assert old.startswith('B for the named same-day triggers; option A is superseded by D-RCV-35.')
od['E11'] = new
wb.save(P)
print('ok')
