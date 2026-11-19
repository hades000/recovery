import datetime, openpyxl
EX = 'EV-26 and EV-27 are exempt: they are raised from the ACE batch record, not from a Workbench change'
M = r'05 Technical architecture/Recovery Workbench Event and Messaging Design v3.md'
t = open(M, encoding='utf-8', newline='').read()
old_tx = '| Transactions | The event is written in the same transaction as the change; no event without the change and no change without the event |'
if EX not in t:
  assert t.count(old_tx) == 1 and t.count('  version: 1.0.0') == 1
  t = t.replace(old_tx, old_tx[:-2] + '. ' + EX + ' |')
  t = t.replace('  version: 1.0.0', '  version: 2.0.0')
  open(M, 'w', encoding='utf-8', newline='').write(t)
print('Event md done')

X = r'05 Technical architecture/Recovery Workbench Event and Messaging Design v3.xlsx'
wb = openpyxl.load_workbook(X)
ev = wb['Events']
assert ev['A2'].value.count('(DT12, DL06)') == 1
ev['A2'].value = ev['A2'].value.replace('(DT12, DL06)', '(D-RCV-35)')
ru = wb['Rules']
assert ru['A8'].value == 'Transactions' and ru['B8'].value == old_tx.split(' | ')[1].rstrip(' |')
ru['B8'].value = ru['B8'].value + '. ' + EX
assert ru['A2'].value == 'Applies to every event.'
ru['A2'].value = 'Applies to every event; EV-26 and EV-27 are exempt from the Transactions rule.'
wb.properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
wb.save(X)
print('Event xlsx done')
