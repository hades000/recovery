import sys; sys.path.insert(0, r'_work/scripts')
import openpyxl, datetime
from fixsmall_lib import load, rep1, set_modified, save
P = r'05 Technical architecture/Recovery Workbench Batch and Scheduling Design v3.docx'
z, x, core = load(P)
# D1 shared Quartz / Spring Batch tables
x = rep1(x, 'Quartz in the ACE service holds the schedules; one run per job across service instances.',
         "Quartz in the ACE service holds the schedules in ACE's existing qrtz_* tables, shared with ACE; one run per job across service instances. The Workbench creates no new qrtz_ table.")
x = rep1(x, 'It runs no inbound load.',
         "It runs no inbound load. Its step records go to ACE's existing Spring Batch batch_* tables, shared with ACE; no new batch_ table is created (ACE Data Tier Map rows 23 and 24).")
# D2
x = rep1(x, 'no job starts on a fixed clock time', 'no data job starts on a fixed clock time')
# D4 wording
x = rep1(x, '19 jobs run on Quartz and Spring Batch. JOB-01 and JOB-09 are retired under D-RCV-35 and keep their rows; the other 17 run.',
         '19 jobs are listed. JOB-01 and JOB-09 are retired under D-RCV-35 and keep their rows; the other 17 run on Quartz and Spring Batch.')
# D3 table When for JOB-07 / JOB-08 matches the section 3 chain
for j in ('JOB-07<', 'JOB-08<'):
    x = rep1(x, 'On the ACE batch-complete record for ALS<', 'On the ACE batch-complete record for ALS, after JOB-02<', start=j)
save(P, z, x, set_modified(core))
print('Batch docx done')

X = r'05 Technical architecture/Recovery Workbench Batch and Scheduling Design v3.xlsx'
wb = openpyxl.load_workbook(X)
ws = wb['Jobs']
old = '19 jobs on Quartz and Spring Batch in the ACE service; JOB-01 and JOB-09 are retired under D-RCV-35. '
assert ws['A2'].value.startswith(old)
ws['A2'].value = ws['A2'].value.replace(old,
    "19 jobs are listed; JOB-01 and JOB-09 are retired under D-RCV-35 and the other 17 run on Quartz and Spring Batch in the ACE service, "
    "using ACE's existing qrtz_* and batch_* tables shared with ACE (no new qrtz_ or batch_ table). ")
for r, jid in ((11, 'JOB-07'), (12, 'JOB-08')):
    assert ws[f'A{r}'].value == jid
    assert ws[f'D{r}'].value == 'On the ACE batch-complete record for ALS'
    assert ws[f'E{r}'].value == 'ACE batch (v_ace_batch_status)'
    ws[f'D{r}'].value = 'On the ACE batch-complete record for ALS, after JOB-02'
    ws[f'E{r}'].value = 'JOB-02; ACE batch (v_ace_batch_status)'
tl = wb['Daily timeline']
assert tl['B5'].value == 'JOB-02 case creation; JOB-04 reconciliation; JOB-07 payment matching; JOB-08 booking confirmation'
tl['B5'].value = 'JOB-02 case creation, then JOB-04 reconciliation, JOB-07 payment matching and JOB-08 booking confirmation'
wb.properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
wb.save(X)
print('Batch xlsx done')
