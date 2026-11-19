import sys, openpyxl
sys.path.insert(0, r'_work/scripts')
from fixba_common import *
p = D + r'/Recovery Workbench Feature List v4.xlsx'
wb = openpyxl.load_workbook(p)
f = wb['Features']
def row(fid):
    for r in range(5, f.max_row + 1):
        if f.cell(r, 1).value == fid: return r
    raise SystemExit(fid)
def put(fid, col, new, old=None):
    setv(f, '%s%d' % (col, row(fid)), new, old)
# A2 counts
setv(f, 'A2', '368 live features in 19 modules across eight epics. Ten retired features remain listed. Two new features (FEAT-RDF-25, 26) cover the ACE read path and the ACE additions. Class is User, Admin, System or Retired - ACE ingestion; filter on Epic or Module.')
# D29 FEAT-DRI-10 systems
assert row('FEAT-DRI-10') == 29
put('FEAT-DRI-10', 'J', 'SFTP', 'SFTP, COLLINS')
# CHO-01
assert row('FEAT-CHO-01') == 61
put('FEAT-CHO-01', 'F', 'Takes the account and its contact and promise history at case entry by reading v_ace_account and v_ace_efs_action, which ACE fills from EFS in its daily batch.')
put('FEAT-CHO-01', 'J', 'ACE database, Workbench', 'EFS, Workbench')
put('FEAT-CHO-01', 'N', 'FEAT-RDF-25', 'FEAT-RDF-21')
# CHO-03
put('FEAT-CHO-03', 'E', 'Read customer facts from the ACE batch', 'Read customer facts from the COLLINS batch')
put('FEAT-CHO-03', 'F', 'Reads the customer profile ACE ingests from UDP, SCBPDM and the core bank (DL20) through v_ace_customer once the ACE batch completes (v_ace_batch_status).')
put('FEAT-CHO-03', 'J', 'ACE database, Workbench', 'Integration adapters')
put('FEAT-CHO-03', 'N', 'FEAT-RDF-25, FEAT-RDF-26', 'FEAT-DRI-09')
# CHO-04
put('FEAT-CHO-04', 'F', 'Replaces the weekly transfer with daily case creation from v_ace_account once the ACE batch completes (v_ace_batch_status).',
    'Replaces the weekly transfer with daily case creation from the COLLINS load.')
put('FEAT-CHO-04', 'J', 'ACE database, Workbench', 'Workbench, EFS')
put('FEAT-CHO-04', 'N', 'FEAT-CHO-01, FEAT-CWC-04, FEAT-RDF-25, FEAT-RDF-26', 'FEAT-CHO-01, FEAT-CWC-04')
# CHO-05
put('FEAT-CHO-05', 'E', 'Hold case creation when the ACE batch is late', 'Hold case creation when the COLLINS load is late')
put('FEAT-CHO-05', 'F', 'When v_ace_batch_status shows the ACE batch has not completed for the business date, keeps the previous position in use, creates the cases after the next completed batch, and logs the gap.',
    'Keeps the previous load in use, creates the cases on the next good load, and logs the gap.')
put('FEAT-CHO-05', 'J', 'ACE database, Workbench', 'EFS, COLLINS')
put('FEAT-CHO-05', 'N', 'FEAT-CHO-01, FEAT-RDF-25, FEAT-RDF-26', 'FEAT-CHO-01')
# CHO-08
put('FEAT-CHO-08', 'E', 'Confirm booked terms from the ACE account view', 'Confirm booked terms from the ALS load')
put('FEAT-CHO-08', 'F', "Matches the approved terms or settlement to the booked position in v_ace_account after the next ACE batch, which ACE ingests from ALS, and raises a task when it is missing.")
put('FEAT-CHO-08', 'J', 'ACE database, Workbench', 'ALS and GL, Integration adapters')
# CHO-09
put('FEAT-CHO-09', 'F', 'Adds the contract, plan and treatment read models to the recovery schema.',
    'Adds the contract, plan and treatment read models to the data store.')
# CHO-10 retire
put('FEAT-CHO-10', 'D', 'Retired - ACE ingestion', 'System')
put('FEAT-CHO-10', 'F', 'Retired under D-RCV-35 (U1); story E2-023 removed. Replaced the manual EFS file handling with an automated, checked load. ACE ingests EFS; the Workbench reads v_ace_efs_action. No Workbench load remains.',
    'Replaces the manual EFS file handling with an automated, checked load.')
stamp(wb, 'Recovery Workbench Feature List v4')
wb.save(p); print('ok feat')
