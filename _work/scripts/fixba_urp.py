import sys, openpyxl
sys.path.insert(0, r'_work/scripts')
from fixba_common import *
src = D + r'/Recovery Workbench Users Roles and Permissions v3.xlsx'
dst = D + r'/Recovery Workbench Users Roles and Permissions v4.xlsx'
wb = openpyxl.load_workbook(src)
NAME = 'Recovery service identity'
r = wb['Roles']
assert r['A55'].value == 'SY-DATALOAD'
for col, v in zip('ABCDEFGHIJ', ['SY-RECOVERY', NAME, 'Non-human actor', 'Non-human actor', 'Recovery module',
        'Reads ACE source data for the recovery module through the SELECT-only recovery.v_ace_* views (read-only ACE view access). No direct read of a public ACE table and no write on any ACE table or view (D-RCV-35, U4)',
        'all', 'None', 'All', 'E1']):
    r[f'{col}55'].value = v
repl(r, 'A2', 'One row is one role, held as data in the roles table.',
     'One row is one role, held as data in the roles table. Version 4, 15 November 2026: the COLLINS data load actor is removed under D-RCV-35 (U1); SY-RECOVERY added.')
pm = wb['Permissions']
assert pm['A55'].value == 'SY-DATALOAD'
# capability areas D..Q: Case record, Queue, Treatment, Litigation, Asset, Debt sale, Write-off, Documents, Rules, Reference data, Decision log, Partner portal, Reporting, Platform admin
vals = ['R', '-', '-', 'R', 'R', '-', 'R', '-', '-', 'R', '-', '-', '-', '-']
pm['A55'].value = 'SY-RECOVERY'; pm['B55'].value = NAME
for i, v in enumerate(vals):
    pm.cell(55, 4 + i).value = v
s = wb['Single sign-on']
assert s['A50'].value == 'SY-DATALOAD'
s['A50'].value = 'SY-RECOVERY'; s['B50'].value = NAME
for col, env in zip('DEFG', ['DEV', 'SIT', 'UAT', 'PROD']):
    s[f'{col}50'].value = f'RWB-{env}-SY-RECOVERY'
# sanity: no DATALOAD anywhere
for ws in (wb['Roles'], wb['Permissions'], wb['Single sign-on']):
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and 'DATALOAD' in c.value:
                raise SystemExit(f'left {ws.title}!{c.coordinate}')
k = wb['Key']
last = k.max_row
add_row_like(k, last, ['Note', 'SY-RECOVERY', 'Recovery service identity: read-only ACE view access through recovery.v_ace_* (SELECT only), no write on ACE; matches Role to System Access Matrix v3 and Admin and Access Model v5 (8.3). The ACE view owner that owns the views is a database identity, not a role'])
add_row_like(k, last, ['Note', 'Retired actor', 'SY-DATALOAD (data load from COLLINS) is removed under D-RCV-35 (U1): ACE ingests every source and the Workbench loads none'])
add_row_like(k, last, ['Version', 'v4', '15 November 2026. Supersedes v3'])
k.auto_filter.ref = 'A4:C%d' % k.max_row
stamp(wb, 'Recovery Workbench Users Roles and Permissions v4')
wb.save(dst); print('ok urp v4')
