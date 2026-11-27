import os

import openpyxl

from ed import STAGE, log

NAME = '05 Technical architecture/Recovery Workbench Service Contract Catalog v3.xlsx'
path = os.path.join(STAGE, NAME)
wb = openpyxl.load_workbook(path)
ws = wb['Jobs']
r = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == 'JOB-08')
new = ['JOB-08', 'P2 rwb-integration', 'event-started workflow (BookingMatchWorkflow in rwb-integration)',
       'Arch v5 slide 44 (owner row superseded, GAP-0657); RD-P1-066']
old = ' | '.join(str(ws.cell(r, c).value) for c in range(1, 5))
for c, v in enumerate(new, 1):
    ws.cell(r, c).value = v
wb.save(path)
log('EDIT', NAME, 'Jobs JOB-08 owner (the .md twin holds no job table)', old, ' | '.join(new), 'RD-P1-066;RD-P1-040;RD-P1-003', '', 'GAP-0657', 'v2', 'v3')
print(old)
