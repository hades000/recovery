import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx
from secenv_lib import *

SRC = '05 Technical architecture/Recovery Workbench Environment and Deployment Design v2.docx'
DST = '05 Technical architecture/Recovery Workbench Environment and Deployment Design v3.docx'
d = docx.Document(SRC)
doc_control(d, 'Recovery Workbench Environment and Deployment Design v3',
    'D-RCV-35 (ADR-010): no inbound load. Spring Batch runs automated chains on the ACE Quartz and Spring Batch tables; '
    'two-migration rule for the ACE views and the view conformance test; stale data from ace_batch_run lateness; '
    'no load containers or inbound file folders (sections 1, 3, 4, 5, 7, 8)')
T = d.tables

# 1. One page
insert_row_after(T[1], 'Where it runs', ['Source data',
    'Read from the ACE database through read-only recovery.v_ace_* views. The Workbench runs no inbound load and receives no source file',
    'Agreed; D-RCV-35'])

# 2. Environments
p = para_starting(d, 'No production data reaches DEV.')
set_text(p, p.text + ' Every environment holds the ACE schema the views read; in DEV and in the pipeline test database it is the ACE schema '
    'with synthetic rows, so the views compile and return data.')

# 3. What runs
set_row(T[3], 'Database', [None,
    'PostgreSQL flexible server, zone redundant: the ACE database, with the recovery schema owned by the service. The recovery module reads ACE '
    'tables only through the recovery.v_ace_* views', 'Same server and database; own schema'])
set_row(T[3], 'Document storage', [None,
    'Blob storage with a write-once container for legal document types. No load container and no inbound file folder: the Workbench receives no source files',
    'New containers'])
set_row(T[3], 'Scheduler', [None,
    'Quartz for timers and scheduled jobs; Spring Batch for automated chains (case creation, reconciliation, payment matching, allocation, write-off scan) '
    'and outbound files, with restart from the last chunk. No Spring Batch job loads source data. Both share ACE\'s existing Quartz (qrtz_*) and '
    'Spring Batch (batch_job_*, batch_step_*) tables; the Workbench adds no qrtz_ or batch tables',
    'Yes; same Quartz and Spring Batch tables'])
insert_row_after(T[3], 'Scheduler', ['Source loads',
    'None. No load container, no inbound file folder, no staging table and no load job. ACE ingests every source and records each batch in ace_batch_run',
    'ACE ingestion'])
insert_row_after(T[3], 'Identity', ['Database roles',
    'recovery_svc, the recovery service role: SELECT on recovery.v_ace_* only, no direct public read, no write. ace_view_owner: a NOLOGIN ACE role '
    'that owns the views and holds SELECT on the ACE tables they read. PUBLIC is revoked. These are the names the ACE Source Views v1 grants use',
    'ace_view_owner is an ACE role'])

# 4.1 Gates
set_row(T[4], '6 Module boundary', [None,
    'No call or table read across a module boundary; the recovery module reads ACE only through recovery.v_ace_* views (TE-001)'])
set_row(T[4], '7 Integration and contract tests', [None,
    'Modules work with the database and the generated types; the view conformance test passes against the ACE schema (section 5)'])

# 5. Database changes
p19 = para_starting(d, 'Every schema change is a versioned migration script')
a = insert_para_after(p19, 'V0001 is the baseline of the recovery schema (D-RCV-28). No recovery migration creates or alters a table in the ACE '
    'public schema; the ACE tables and columns change only through the ACE team\'s own migrations (RWB-ACE-001).')
b = insert_para_after(a, 'Two-migration rule. A view cannot be created over a table that does not exist, so the ACE views ship in two migrations. '
    'Section A, 16 views over the ACE tables that exist today, with the grants and the revoke from PUBLIC, ships with RWB-E1-069 as the next free '
    'sequence after V0001.')
c = insert_para_after(b, 'Section B, 14 views over the tables and columns the ACE team adds, ships as a later sequence in the week RWB-ACE-001 lands '
    'in each environment. Until then the features that read the Section B views stay behind their feature flags, switched off.')
e = insert_para_after(c, 'The pipeline runs the view conformance test after the migrations in every environment: every v_ace_* view compiles; no '
    'constraint in schema recovery references a public table; recovery_svc cannot select a public table directly and cannot insert, update or '
    'delete on any public or recovery table. A failure stops the deployment, so an ACE column change that breaks a view is found before release.')
insert_para_after(e, 'In DEV and the pipeline test database the ACE schema runs first, then V0001, then Section A, then Section B once the ACE '
    'additions are present.')

# 7. Resilience
set_row(T[7], 'Load failure', ['Late ACE data',
    'There is no Workbench load to fail. Data is stale when ace_batch_run, read through v_ace_batch_status, has no COMPLETED record for the business '
    'date at the Workbench cut-off. AceDataLate goes to the data steward, the data products show their last complete business date and are marked '
    'stale, and the data jobs start when the record arrives', 'Designed; D-RCV-35'])

# 8. Open decisions
insert_row_after(T[8], 'DL37', ['DL43',
    'Whether the ACE team accepts the RWB-ACE-001 scope and dates, needed by 21 November 2026',
    'Section A views only; the features that need the Section B views stay behind their flags'])

d.save(DST)
print('saved', DST)
