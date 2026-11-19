import sys, openpyxl
sys.path.insert(0, r'_work/scripts')
from fixba_common import *
p = D + r'/Recovery Workbench Role to System Access Matrix v3.xlsx'
wb = openpyxl.load_workbook(p)
m = wb['Matrix']
# steward R on ACE removed: Admin and Access Model v5 (8.3) grants ACE read only to the ACE view owner and the recovery service identity
setv(m, 'Y33', '-', 'R')
assert m['A33'].value == 'RW-DATASTEW'
repl(m, 'A2', 'only the recovery service identity and the data steward hold R on ACE; no role holds W.',
     'only the recovery service identity (SY-RECOVERY) holds R on ACE, through the recovery.v_ace_* views; no role holds W. CCMS shows no role: its data reaches the Workbench via ACE ingestion; no direct Workbench access.')
al = wb['Access list']
assert al['A82'].value == 'RW-DATASTEW' and al['D82'].value == 'ACE database (read-only)'
al.delete_rows(82)
al.auto_filter.ref = 'A4:E%d' % al.max_row
repl(al, 'A2', '109 role and system pairs', '108 role and system pairs')
sy = wb['Systems']
assert sy['A26'].value == 'ACE database (read-only)'
setv(sy, 'C26', 1, 2)
assert sy['A13'].value == 'CCMS'
setv(sy, 'B13', 'Collateral systems owner; via ACE ingestion; no direct Workbench access', 'Collateral systems owner')
k = wb['Key']
repl(k, 'C12', 'SELECT for the recovery service identity and the data steward, no write for any role',
     'SELECT for the recovery service identity (SY-RECOVERY) only, no write for any role (Admin and Access Model v5, 8.3)')
add_row_like(k, 13, ['Note', 'CCMS', 'No role holds CCMS access: CCMS data reaches the Workbench via ACE ingestion; no direct Workbench access (D-RCV-35, U1). The column is kept for traceability.'])
k.auto_filter.ref = 'A4:C%d' % k.max_row
stamp(wb, 'Recovery Workbench Role to System Access Matrix v3')
wb.save(p); print('ok role')
