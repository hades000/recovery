import sys, openpyxl
sys.path.insert(0, r'_work/scripts')
from fixba_common import *
p = D + r'/Recovery Workbench Business Glossary v3.xlsx'
wb = openpyxl.load_workbook(p)
g = wb['Glossary']
assert g['A72'].value == 'Proof of delivery'
setv(g, 'D72', 'notice.callback_date, notice.delivery_status; v_ace_pod (WIN proof of delivery ingested by ACE)')
k = wb['Key']
setv(k, 'C6', 'The entity, field, list of values or role that holds the concept in the logical data model, or the ACE view (recovery.v_ace_*) that reads it')
stamp(wb, 'Recovery Workbench Business Glossary v3')
wb.save(p); print('ok gloss')
