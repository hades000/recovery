"""RF-tests: targeted fixes to staged Test Cases v9 and RTM v9. Usage: python -I rf_apply.py [--write]"""
import sys, os, re, csv, collections
import openpyxl

sys.dont_write_bytecode = True
W = r'C:/Users/SahilMore/Downloads/Recovery Workbench SharePoint Set v14/_work/p1-ready'
__file__ = W + '/w2-sync/comp.py'
exec(open(__file__, encoding='utf-8').read())          # stories, tcs, trace, back, compose, title, texts helpers
WRITE = '--write' in sys.argv
MODEL, AGENT = 'claude-sonnet-5-5', 'RF-tests'
TCF = 'Recovery Workbench Test Cases v9.xlsx'
RTF = 'Recovery Workbench Requirements Traceability Matrix v9.xlsx'
BACK = W + '/tc-backfill.csv'
LOG = W + '/editlog/RF-tests.csv'
COL = dict(cov=4, title=5, level=6, given=7, when=8, then=9, data=10, reg=11, status=12, why=13, keys=15)


def P(x):
    """short story key -> full key"""
    return 'RWB-' + x


def from_ac(k, acs, cov=None, data=None, suffix=''):
    g, w, t = [], [], []
    for a in acs:
        cg, cw, ct = compose(k, a)
        assert cw or ct, (k, a)
        g.append('%s: %s' % (a, cg))
        w.append('%s: %s' % (a, cw))
        t.append('%s: %s' % (a, ct))
    ttl = title(k, acs[0]).replace('`', '"') + suffix
    d = dict(title=ttl, given='; '.join(g), when='; '.join(w), then='; '.join(t))
    if cov:
        d['cov'] = cov
    if data:
        d['data'] = data
    return d


def case(given, when, then, data=None, **kw):
    d = dict(given=given, when=when, then=then, data=data or given)
    d.update(kw)
    return d


EDIT = collections.OrderedDict()   # tid -> (finding_refs, note, values)
RET = collections.OrderedDict()    # tid -> (finding_refs, reason)


def edit(tid, ref, note, **vals):
    assert tid not in EDIT and tid not in RET, tid
    EDIT[tid] = (ref, note, vals)


def retire(tid, ref, reason):
    assert tid not in EDIT and tid not in RET, tid
    RET[tid] = (ref, reason)


# ---------------------------------------------------------------- ACE001, E1018
r = P('P1-ACE001-DB') + '#7'
edit('TC-ACE-001-07', r, 'data matched to section 16 of RWB-P1-ACE001-DB',
     data='A corrected 2026-11-30 redelivery with one changed value; row counts per business key and one row in "ace_batch_run"')
edit('TC-ACE-001-08', r, 'data matched to AC8 (81 field rows, not 80)',
     data='The 81 field rows against "information_schema.columns"; a missing column, a wrong type and an extra mapped column')
k = P('P1-E1018-APP')
edit('TC-ACE-001-09', r + '; RWB-P1-E1018#10', 'moved to the batch gate story and restated to its AC14 (activity failure, no HTTP 409)',
     keys=k, level='Component',
     **from_ac(k, ['AC14'], cov='AC14', data='"v_ace_batch_status" absent: the activity fails with AceBatchNotComplete and MSG-P1-001, no page'))
edit('TC-P1-E1018-APP-17', 'RWB-P1-E1018#6', 'contract restated to the two PUT operations, the activity and the provider fake of this story',
     cov='Contract of section 12.1', title='Contract of the two extension writes and of the listEligibleAccounts activity with its provider fake',
     **case('rwb-source-data.yaml 5.1.0, the contract jar and the "listEligibleAccounts" provider fake of section 12.8',
            'The contract test runs "PUT /extension-facts/parties/{personKey}", "PUT /extension-facts/accounts/{accountKey}" and the activity against them',
            'Each PUT takes its body of section 12.1 (four flags for a party, "disputeOpen" for an account), requires "If-Match" and answers 200 with the stored row and "ETag" or the status and messageCode of the section 12.1 error table; the fake serves two pages, breaks of each kind, "AceBatchNotComplete" with and without a last complete date and "BusinessDateNotCurrent"; no "GET /entry-candidates" is published',
            'Sections 12.1, 12.5 and 12.8: two PUT operations, one activity, the provider fake'))
edit('TC-P1-E1018-APP-18', 'RWB-P1-E1018#11', 'restated as the conformance test on the two tables; the story adds no migration',
     title='Conformance of "party_ext" and "account_ext"',
     **case('Schema "rwb_source_data" as delivered by RWB-P1-E1069-DB', 'The conformance test of the story runs',
            '"party_ext" is keyed by "person_key" and "account_ext" by "account_key", the mandatory columns are present and neither table has a foreign key into "public"; the story adds no migration',
            'The delivered "party_ext" and "account_ext" tables'))

# ---------------------------------------------------------------- AD018, AD019
r = P('P1-AD018-APP') + '#7'
for t in ('TC-AD-018-01', 'TC-AD-018-02', 'TC-AD-018-04'):
    retire(t, r, 'Retired: no criterion of the version 3 AD018 stories asserts this behaviour; the legacy wording is kept on the -ITG copy of RWB-ITG-AD018-ITG')
k = P('P1-AD018-APP')
edit('TC-AD-018-03', r, 'restated to AC7; the logged refusal is pending (GAP-3498) and is no longer asserted', keys=k,
     **from_ac(k, ['AC7'], cov='AC7', data='A caller with no session; a caller without Platform administration R for the list or U for the rerun'))
edit('TC-AD-018-06', P('P1-AD018-APP') + '#13', 'concrete operations and results',
     title='Operations, events, workflows and schedules of section 12',
     **case('rwb-source-data.yaml 5.1.0 and the rwb-integration scheduled-jobs fake of section 12.8', 'The contract test runs the operations of section 12',
            '"GET /admin/jobs" answers a "JobPage" and "POST /admin/jobs/{jobId}/rerun" answers 202 with a new PENDING Job, with the errors of section 12.1; the one consumed operation is "GET /api/recovery/integration/v1/admin/scheduled-jobs" with a 2 s timeout; the story publishes and consumes no event and registers no workflow type or Schedule',
            'Version 5.1.0 paths under /api/recovery/source-data/v1'))
edit('TC-AD-018-07', P('P1-AD018-APP') + '#13', 'concrete tables and results',
     title='Tables of section 12.7 and the grants',
     **case('Schema "rwb_source_data" and the rwb-source-data login', 'The boundary test lists the tables read or written and the grants of the login',
            'The story uses "job_run", "job_run_check", "data_product_source" and "data_product_load" only, and writes no "data_product_load" row; the login reaches only its owned tables and the "recovery.v_ace_*" views; a select on a table of another service is refused',
            '"job_run", "job_run_check", "data_product_source", "data_product_load"'))
edit('TC-P1-AD018-OPS-07', P('P1-AD018-OPS') + '#8', 'concrete tables and results',
     title='Tables of section 12.7 on deployment',
     **case('The rendered release and the APP migration for "job_run" and "job_run_check"', 'The migration is applied and the schema and grants are listed',
            '"job_run" and "job_run_check" exist in "rwb_source_data"; no "job_catalog" table and no case-list table is created; the deployment changes no "data_product_load" row; the login has rights on "rwb_source_data" and SELECT on the approved "recovery.v_ace_*" views only',
            '"job_run", "job_run_check"; absent: "job_catalog" and case-list tables'))

r = P('P1-AD019-APP') + '#3'
retire('TC-AD-019-03', r, 'Retired: the access refusal is proved by TC-P1-AD019-APP-09 and TC-AD-019-04; no criterion asserts a logged refusal; the legacy wording is kept on the -ITG copy')
k = P('P3-AD019-APP')
edit('TC-AD-019-04', r, 'restated to AC4 of RWB-P3-AD019-APP; the decision log failure and MSG-P7-003 are asserted by no criterion', keys=k,
     level='Component', **from_ac(k, ['AC4'], cov='AC4, Access, BR8', data='A role without Platform administration R calls the console operations and is refused with MSG-P4-002'))
r = P('P1-AD019-APP') + '#7'
retire('TC-AD-019-12', r, 'Retired: listed as retired in section 16 of RWB-P1-AD019-APP; BR14 no longer exists and the result rows are asserted by AC1, AC8 and AC9')
retire('TC-P1-AD019-APP-17', r, 'Retired: listed as retired in section 16 of RWB-P1-AD019-APP; the single workflow is proved by AC7 (TC-P1-AD019-APP-10)')
edit('TC-AD-019-19', r, 'concrete contract expectation',
     **case('rwb-source-data.yaml 5.1.0 and the provider fakes of RWB-P1-E1011-CON and RWB-P1-E1015-CON', 'The contract test runs the two result reads of section 12.1',
            '"GET /admin/reconciliation/results" takes "recCode" (REC-01, REC-02), "product", "result" (PASS, BREAK), "from" and "to" and answers 400, 401, 403, 422 and 503; "GET /admin/reconciliation/results/{resultId}" answers one result or 400, 401, 403, 404 and 503; this delta publishes no separate operation, event, workflow, activity or Schedule',
            'Fakes at fakes/rwb-source-data/5.1.0/: page, single result, empty page and the declared errors'))
edit('TC-AD-019-20', r, 'concrete table expectation',
     **case('Schema "rwb_source_data" with E1011 result rows and the P1 run records', 'The result reads run and the schema is compared before and after',
            'The reads use "reconciliation_result" and the P1 run records and change no row; AD019 adds no table or migration, and creates no case-list table or "publish_status" column',
            '"reconciliation_result" and the run records; row counts before and after'))

# ---------------------------------------------------------------- DM
r = P('P1-DM002-APP') + '#1'
edit('TC-DM-002-06', r, 'the claim that the schema holds only two tables is removed (AC1: the story adds no object)',
     data='AC1 and AC4 fixtures; tables, views, columns, indexes, Flyway history rows and row counts of "rwb_source_data" recorded before and after the run (the story adds no object); "P0000123" with and "P0000456" without a "party_ext" row')
edit('TC-P1-DM002-APP-02', r, 'the claim that the schema holds only two tables is removed',
     data='One person with a "party_ext" row ("P0000123") and one without ("P0000456")')
r = P('P1-DM002-APP') + '#2'
V = 'The verification of this story runs'
edit('TC-DM-002-07', r, 'concrete data and result for BR1', **case('The delivery of this story: its migrations, repositories, jobs and scripts', 'The delivery is inspected',
     'It holds no extract, identifier map, load, reconciliation or cutover for customer and party data and no write statement', 'The build of the story'))
edit('TC-DM-002-08', r, 'concrete data and result for BR2', **case('The rwb-source-data login and schema "rwb_source_data"', 'The grants and constraints are listed',
     'The login holds SELECT only on the "recovery.v_ace_*" views and no privilege in "public"; no constraint references "public"; a link to an ACE record is a varchar(255) business key with no foreign key', 'Privilege and constraint queries'))
edit('TC-DM-002-09', r, 'concrete data and result for BR3', **case('Person "P0000123" in "v_ace_customer" with "id_no_masked" and "id_no_last4"', '"GET /customers/P0000123" is called',
     'The answer holds "idNoMasked" and "idNoLast4" and no other form of the identity number; no log line or fixture holds a clear identity number', 'Synthetic person "P0000123"'))
edit('TC-DM-002-10', r, 'concrete data and result for BR4', **case('"party_ext", "contact_point_ext" and the views "v_ace_customer" and "v_ace_contact"', 'The columns are compared',
     'No extension column copies an ACE column; each extension row is 1:1 with its ACE record and both tables carry the seven standard record columns', 'Column lists of the two tables and the two views'))
edit('TC-DM-002-11', r, 'concrete data and result for BR5', **case('"party_ext" and "contact_point_ext"', 'The primary keys and key values are checked',
     '"party_ext" is keyed by "person_key" and "contact_point_ext" by "contact_key" in the form "contact_type:key", with "contact_type" PHONE, EMAIL or ADDRESS', '"P0000123"; "PHONE:PH-0001", "EMAIL:EM-0001", "ADDRESS:AD-0001"'))
edit('TC-DM-002-12', r, 'concrete data and result for BR6', **case('The data product catalog row of DP02', 'The row is read',
     'Its system of record is "ACE (ingested from SCBPDM)" and its Workbench tables are "party_ext" and "contact_point_ext"', 'DP02 catalog row'))
edit('TC-DM-002-13', r, 'concrete data and result for BR7', **case('The delivery of this story for DP02', 'Its jobs, relays and outbound paths are inspected',
     'No relay, export, data lake or reporting table receives a copy of customer, contact or relation data', 'The build of the story'))
edit('TC-DM-002-14', r, 'concrete data and result for BR8 and BR9; switch and parameters removed', cov='BR8, BR9', title='BR8, BR9',
     **case('"P0000123" with a "party_ext" row and a "contact_point_ext" row with a recorded consent', '"GET /customers/P0000123" is called and the verification runs',
            'The flags and consent are those of the data rows and the answer fields are those of the published contract; the story writes no row and adds no migration or repository', 'AC4 fixtures; row counts before and after'))

r = P('P1-DM007-APP') + '#8'
edit('TC-P1-DM007-APP-07', r, 'data aligned with AC8: no provided operation',
     data='The cut-over step started with no token and without the Platform administration right; the DP07 record read asked for a case id with no row')
edit('TC-P1-DM007-APP-08', r, 'data aligned with AC9: no cut-over activity',
     data='The step interrupted after the legal action package and before the notice package for 2026-12-10, then run again; package and count rows checked')
edit('TC-P1-DM007-APP-09', r, 'data aligned with AC10: rwb-comms fails, not rwb-litigation',
     data='The rwb-litigation mock accepting its package and the rwb-comms mock failing or not answering for 2026-12-10; the date then run again with rwb-comms answering')

edit('TC-DM-008-04', P('P1-DM008-APP') + '#12', 'concrete message and no-read result',
     **case('A caller without the Platform administration right in the authorise fake', 'The caller starts the cutover step; then a caller with the right starts it',
            'The first is refused with MSG-P4-002 "You cannot run the partner cutover extract here. Your role does not include it."; the dump is not read, no package is written and no row changes; the second is not refused',
            'A caller without and a caller with the right in the authorise fake'))
edit('TC-DM-010-02', P('P1-DM010-APP') + '#9', 'aligned with section 16: the REC-05 read side and BR7', cov='AC3, BR7', title='REC-05 orphans on migrated records stop a clean day',
     **case('The reconciliation fixture with two REC-05 orphan rows on migrated records and a PASS row on the same business date', 'The clean-day counter reads the rows',
            'The date is not counted clean; the orphan list names the data steward and the ACE team; no migrated record is deleted or changed',
            'Two REC-05 orphans and one PASS row on one business date'))
edit('TC-DM-013-04', P('P1-DM013-APP') + '#13', 'concrete message and no-read result', cov='AC5; Access refusal; BR4', title='A caller without the Platform administration right is refused',
     **case('A caller without the Platform administration right in the authorise fake; row counts of "rwb_source_data" recorded', 'The caller starts the cutover run; then a caller with the right starts it',
            'The first is refused with MSG-P4-002 "You cannot run the money and closure cutover here. Your role does not include it."; the cutover record shows the refusal, no dump or ACE view is read, no file is written and the row counts are unchanged; the second is not refused',
            'A caller without and a caller with the right in the authorise fake'))

# ---------------------------------------------------------------- E1001, E1002
edit('TC-P1-E1001-APP-19', P('P1-E1001-APP') + '#13', 'expected observation stated',
     **case(tcs['TC-P1-E1001-APP-19'][7], 'The migration runs and the grants, constraints and views of each schema are listed',
            'Each table of section 12.7 exists in its owning schema; the rwb-source-data objects hold zero grants, joins, constraints and views on the 74 tables of the other services; no constraint references schema "public" and no table holds a copy of source data',
            tcs['TC-P1-E1001-APP-19'][10]))
k = P('P3-E1002-APP')
edit('TC-E1-002-11', P('P1-E1002-CON') + '#1', 'RWB-P1-E1002-CON is retired; the job read left for RWB-P1-AD018-CON; restated to the P3 story that cites this ID',
     keys=k + '; RWB-ITG-E1002-ITG', **from_ac(k, ['AC11'], cov='AC11, BR1, access', data='"u-owner-01" with scope Own and "RW-2026-000123" owned by "u-owner-02"; a role with no Case record right refused with 403 and MSG-P4-002'))
r = P('P1-E1002-OPS') + '#1'
retire('TC-P1-E1002-OPS-06', r, 'Retired: version 2 access rule on the jobs operation is withdrawn; callers of the read are refused under AC13 (TC-P1-E1002-OPS-22)')
for t, br in (('TC-P1-E1002-OPS-09', 'BR1'), ('TC-P1-E1002-OPS-10', 'BR2'), ('TC-P1-E1002-OPS-11', 'BR3'),
              ('TC-P1-E1002-OPS-13', 'BR5'), ('TC-P1-E1002-OPS-14', 'BR6'), ('TC-E1-002-20', 'BR8')):
    retire(t, r, 'Retired: %s of RWB-P1-E1002-OPS is withdrawn with the case-list run (section 8); grants and secrets are proved by AC19 (TC-P1-E1002-OPS-28)' % br)

# ---------------------------------------------------------------- E1011
r = P('P1-E1011-APP') + '#12'
edit('TC-P1-E1011-APP-14', r, 'concrete expected values for BR6',
     **case('"recon.tolerance.pct" 0.10; business date 2026-11-30', 'Count checks compare 1000000 with 999000 and 1000000 with 998999, and zero with zero',
            'The first row stores variance_pct 0.1000 and PASS, the second 0.1001 and BREAK; "variance_count" holds the absolute difference; zero against zero stores 0.0000 and PASS',
            '1000000 against 999000 and 998999; zero against zero'))
edit('TC-P1-E1011-APP-19', r, 'concrete expected values for BR5 and BR13',
     **case('"party_ext" person_key "P0099881" has no row in "v_ace_customer"', 'REC-05 completes',
            'The run summary and the decision record count one orphan; the orphan is listed for the data steward and the ACE team; the "party_ext" and ACE rows are unchanged and the result store holds no REC-05 row',
            '"party_ext" person_key "P0099881" absent from "v_ace_customer"'))
r = P('P1-E1011-OPS') + '#4'
edit('TC-P1-E1011-OPS-10', r, 'consumer group and .dlt check removed (AC11); concrete contract check', cov='§12 operations, events and activities', title='Contract of section 12: no event consumed',
     **case('The E1015 base release with the E1011 delta and the E1011-CON fake pinned to 5.1.0', 'The routes, worker registrations and subscriptions are listed',
            'The two result reads answer on /api/recovery/source-data/v1; the shared worker registers "ReconciliationWorkflow" and activity "reconciliation" on task queue "rwb-source-data" in namespace "rwb-recovery"; the delta adds no consumer, subscription, retry topic, ".dlt" topic or Schedule',
            'Rendered release and worker registrations'))
edit('TC-P1-E1011-OPS-11', r, 'tables the delta does not add are removed; concrete boundary check', cov='§12.7 tables (ASM-3438)', title='Tables of section 12.7: one index only',
     **case('Schema "rwb_source_data" with existing "reconciliation_result" rows', 'The release migration is applied and the schema is compared',
            'Only index "ix_reconciliation_date" on "reconciliation_result" (business_date, rec_code, product_group) is added; no table or column is added and existing rows are unchanged; a cross-schema write attempt is denied',
            'Schema listing before and after the migration'))

# ---------------------------------------------------------------- E1013
r = P('P1-E1013-APP') + '#9'
edit('TC-P1-E1013-APP-22', r, 'restated to the access rules of this story', title='Access to the readiness pair and the payment read',
     **case('The readiness workload identity with and without Platform administration U and R, a user identity, and a payment client with and without Case record R and scope', 'Ready, status and "GET /payments?accountKey=" are called, once also with no token',
            'No token answers 401 MSG-P4-001; a caller without the right or scope, and a user identity on the readiness pair, answers 403 MSG-P4-002; nothing is written or returned',
            'Section 10 identities; "ACC0000017"; date 2026-11-27'))
edit('TC-P1-E1013-APP-23', r, 'three operations, not four', cov='Contract of the three operations of 12.1', title='Contract of the three operations of 12.1',
     **case('Provider contract rwb-source-data.yaml 5.1.0 and its fake', 'The contract test calls "POST /business-days/{date}/ready", "GET /business-days/{date}/status" and "GET /payments"',
            'Ready answers 202 and status 200 with "BusinessDayStatus"; payments answers 200 "PaymentsAnswer" for exactly one of "businessDate" or "accountKey" and 400 MSG-GEN-001 for both or neither; errors are "application/problem+json" with "messageCode"',
            'The three operations of section 12.1'))
retire('TC-P1-E1013-APP-25', r, 'Retired: BR6 is not a rule of this story; age bands and measure definitions belong to RWB-P9-E1013-APP')
edit('TC-P1-E1013-APP-26', r, 'concrete result for BR8', **case('Readiness for 2026-11-27 is RUNNING and the ALS stamp is not written', 'The status is read, then E1015 commits the ALS stamp and it is read again',
     'The first answer is RUNNING and the second DONE; this story writes no freshness stamp', 'Business date 2026-11-27'))
edit('TC-P1-E1013-APP-27', r, 'concrete result for BR9', **case('A test fixture that names the retired INT-19 lake endpoint', 'LakeFreeRule runs and a readiness call is made',
     'The build with the fixture fails and reports the component; the delivered build calls no lake endpoint and writes no extract file', 'INT-19 fixture'))
edit('TC-P1-E1013-APP-28', r, 'concrete result for BR10', **case('The payment view query cannot finish within the 2 s caller budget', 'The authorised payment read is called',
     'It answers 503 MSG-GEN-006, caches no successful result and calls no other service to obtain the data', 'Delayed payment view fixture'))
edit('TC-P1-E1013-APP-29', r, 'concrete result for BR11', **case('A first ready call for 2026-11-27', 'The outbound messages of this story are listed',
     'It consumes no source event and publishes no ACE event; the only message is the decision record of the platform library, with no account, case or customer identifier', 'Outbox rows after one ready call'))
edit('TC-P1-E1013-APP-30', r, 'concrete result for BR12', **case('A ready call with an invalid date and one with a non-UUID key', 'The calls are made',
     'They answer 400 MSG-GEN-001 and 400 MSG-PLT-N009-03 as published; this story raises no freshness message and writes no row', 'Invalid date; non-UUID "Idempotency-Key"'))
edit('TC-P1-E1013-APP-31', r, 'concrete result for BR14', **case('A first ready call for 2026-11-27 and a date row that is DONE or LATE', 'The same key is replayed, then a new UUID key is sent for the DONE or LATE date',
     'The replay answers the stored response and starts nothing; the new key answers 202 with the stored state and starts no workflow; one readiness row exists for the date', 'Business date 2026-11-27; two keys'))
edit('TC-E1-013-18', r, 'concrete result for BR13', **case('An E1013 readiness call, payment read and snapshot component', 'Their table access is inspected',
     'None reads or writes "measure_definition" or "measure_snapshot"; measure computation stays with P9', 'Table access of the story build'))

# ---------------------------------------------------------------- E1015
r = P('P1-E1015-APP') + '#16'
edit('TC-E1-015-13', r, 'concrete contract expectation', cov='Operations, events and activities of section 12', title='Operations, events and activities of section 12',
     **case('rwb-source-data.yaml 5.1.0, the provider fake of RWB-P1-E1015-CON and the contract jar', 'The contract test runs the freshness read, the two events and the worker registration',
            '"GET /data-products/freshness" answers 200 "DataProductFreshness[]", 400 MSG-GEN-007, 401 MSG-P4-001, 403 MSG-P4-002 or 503 MSG-GEN-006; "AceDataReady" and "AceDataLate" carry key "{sourceSystem}:{businessDate}" and data sourceSystem, businessDate, status and completedAt on "rwb.source-data.events.v1"; "AceIngestCheck" has ID "ace-ingest-check-{businessDate}" with activities "readBatchStatus", "stampProducts", "markStale" and "checkDailyCompleteness"; Schedule "rwb-source-data-ace-late-check" is 05:30 Asia/Bangkok',
            'Sections 12.1, 12.3, 12.5 and 12.6'))
edit('TC-E1-015-14', r, 'concrete table expectation', cov='Tables of section 12.7', title='Tables of section 12.7',
     **case('A COMPLETED batch for a business date and the rwb-source-data login', 'The ingest run stamps the date and its table access is recorded',
            'Of the section 12.7 objects only "data_product_load" and the library "outbox_event" are written; "data_product" and "data_product_source" are read; "decision_log_entry" is neither read nor written; "v_ace_batch_status" and "v_ace_holiday" are read only',
            'Statement log of one run'))

# ---------------------------------------------------------------- E1016
r = P('P1-E1016-APP') + '#12'
k = P('P1-E1016-APP')
UU = 'case UUID 00000000-0000-4000-8000-000000000102; DPA-2026.11'
for t, a, old, d in (('TC-P1-E1016-APP-27', 'AC1', 'AC1', 'RW-AUDIT on DP02; ' + UU),
                     ('TC-P1-E1016-APP-28', 'AC3', 'AC3', 'RW-PHONECOL on DP06; ' + UU),
                     ('TC-P1-E1016-APP-29', 'AC4', 'AC4', 'Access load DPA-2026.12 with role RW-UNKNOWN'),
                     ('TC-P1-E1016-APP-31', 'AC6', 'AC6', 'RW-COMPLY; no masking rule in force; ' + UU),
                     ('TC-P1-E1016-APP-32', 'AC7', 'AC7', 'PII log stub rejecting writes; ' + UU),
                     ('TC-P1-E1016-APP-33', 'AC8', 'AC8', 'DPA-2026.12 DP06 row from 2026-12-15; business date 2026-12-14 then 2026-12-15; ' + UU)):
    edit(t, r, 'restated to %s with the case UUID' % a, **from_ac(k, [a], data=d, suffix=' (legacy RWB-E1-016 %s)' % old))
r = P('P1-E1016-APP') + '#18'
edit('TC-P1-E1016-APP-34', r, 'concrete result', cov='AC16; Access', **{x: y for x, y in from_ac(k, ['AC16'], data='RW-TRIBE calls "GET /admin/data-products"').items() if x != 'cov'})
edit('TC-P1-E1016-APP-38', r, 'concrete contract expectation',
     **case('rwb-source-data.yaml 5.1.0 and the contract fakes of section 12.8', 'The contract test runs the provided and consumed operations of section 12',
            '"GET /data-products/{productCode}/records" answers "DataProductRecordPage" and "GET /admin/data-products" answers "DataProductCatalogEntry[]" with the errors of section 12.1; each consumed call is one hop with a 2 s budget; the story publishes and consumes no event and registers no workflow, activity or Schedule',
            'Sections 12.1 to 12.6'))
edit('TC-P1-E1016-APP-39', r, 'concrete table expectation',
     **case('Schema "rwb_source_data" with the delivered read model', 'A records read, a catalog read and an access load run and the statements are recorded',
            'Only "data_product_access" is written; "data_product", "sys_objects", "sys_fields", "sys_field_version" and "data_contract" are read only; no table of another service is read, including "retention_rule" and "masking_rule"; the story creates no "v_data_product_catalog" or extension table',
            'Statement log; DPA-2026.11'))
retire('TC-P1-E1016-CON-27', P('P1-E1016-CON') + '#10', 'Retired: section 13 of RWB-P1-E1016-CON publishes no Java read interface (no AceSourceRead)')

# ---------------------------------------------------------------- E1055
r = P('P1-E1055-APP') + '#8'
for t, a, d in (('TC-P1-E1055-APP-16', 'AC1', None),
                ('TC-P1-E1055-APP-21', 'AC8', 'A proof-of-delivery request; statement log of the database access'),
                ('TC-P1-E1055-APP-22', 'AC9', 'A request with no valid token; a workload identity other than rwb-comms'),
                ('TC-P1-E1055-APP-23', 'AC3', '"v_ace_pod" row of 2026-11-30: DELIVERED, barcode "RR123456789TH", notice "N-0001", call-back 2026-11-28')):
    v = dict(cov=a, title=title(P('P1-E1055-APP'), a).replace('`', '"'))
    if d:
        v['data'] = d
    edit(t, r, 'retitled to the criterion it tests (%s)' % a, **v)

# ---------------------------------------------------------------- E1064
r = P('P1-E1064-APP') + '#11'
for i in range(1, 9):
    retire('TC-E1-064-%02d' % i, r, 'Retired: superseded by TC-P1-E1064-APP-%d (at least 123 objects and 1,379 fields); the legacy wording is kept on the -ITG copy' % (10 + i))
k = P('P4-E1064-APP')
edit('TC-E1-064-09', P('P1-E1064-OPS') + '#10', 'removed from the P1 stories and restated to section 16 of RWB-P4-E1064-APP', keys=k + '; RWB-ITG-E1064-ITG',
     cov='AC9, BR10', **{x: y for x, y in from_ac(k, ['AC9'], data='RW-TRIBE with Reference data R only calls approve; a token with no role').items() if x != 'cov'})
r = P('P1-E1064-APP') + '#12'
edit('TC-P1-E1064-APP-20', r, 'events and activities removed (the story has none); concrete result',
     **case('rwb-source-data.yaml 5.1.0 and the RWB-P1-E1064-CON provider fake', 'The five operations of section 12.1 are called',
            'Each answers its schema and only the statuses and message codes of the section 12.1 table; every PATCH requires "If-Match" and returns the new "ETag"; publish requires "Idempotency-Key"; the story publishes no event of its own, consumes none and registers no workflow, activity or Schedule',
            'Five operations: two reads, two PATCH, one publish'))
edit('TC-P1-E1064-APP-21', r, 'concrete table expectation',
     **case('The baseline of at least 123 objects and 1,379 fields in "rwb_source_data"', 'A field change, a confirmation and a publish run and the statements are recorded',
            'Of the section 12.7 tables only "sys_fields", "sys_field_version" and "data_contract" are written (the platform library keeps its own idempotency and decision-record rows); "sys_objects" and "data_product" are read only; no table, column, index or constraint is added and no table of another service is read',
            'Statement log and schema listing before and after'))

# ---------------------------------------------------------------- E1065, E1066, E1067, E1069
r = P('P1-E1065-APP') + '#8'
retire('TC-P1-E1065-APP-19', r, 'Retired: the case read access check is not a criterion of RWB-P1-E1065-APP (section 16); the scope moved to the P4 and P3 slices')
retire('TC-P1-E1065-APP-20', r, 'Retired: the 13-table object check is not a criterion of RWB-P1-E1065-APP (section 16); the story is proved by AC1 to AC18')
edit('TC-E1-066-10', P('P1-E1066-APP') + '#7', 'withdrawn flat entry path replaced by the case-scoped path',
     cov='Contract §12 — POST and GET entry on /cases/{caseId}/interactions', title='Contract §12: append and entry read',
     **case('rwb-source-data.yaml 5.1.0 and the case and decision-log fakes', 'The contract test calls "POST /cases/{caseId}/interactions" and "GET /cases/{caseId}/interactions/{entryId}"',
            'A new business key answers 201 with the stored entry and a stored one 200 with the existing entry; the entry read answers that entry, or 404 MSG-P4-003 when it is not on the case; errors are those of section 12.1',
            'Case "RW-2026-000201"; one append and one entry read'))
r = P('P1-E1067-APP') + '#8'
for t, rep in (('TC-E1-067-04', 'TC-P1-E1067-APP-10'), ('TC-E1-067-08', 'TC-P1-E1067-APP-13')):
    edit(t, r, 'no longer a case of the P1 stories (%s proves it there); kept for the P3 and P5 slices that cite it' % rep,
         keys='; '.join(x.strip() for x in tcs[t][15].split(';') if not x.strip().startswith('RWB-P1-')))
retire('TC-P1-E1067-APP-14', r, 'Retired: the intake has no caller; the access check of the append is RWB-P1-E1066-APP AC10 (TC-P1-E1066-APP-18)')
r = P('P1-E1069-APP') + '#8; RWB-P1-E1069-DB#11'
for i in range(1, 9):
    t = 'TC-E1-069-%02d' % i
    edit(t, r, 'removed from RWB-P1-E1069-APP and -DB (their own rows prove the criteria); kept for the P4 slice that cites the ID',
         keys='; '.join(x.strip() for x in tcs[t][15].split(';') if x.strip() not in (P('P1-E1069-APP'), P('P1-E1069-DB'))))

# ---------------------------------------------------------------- E2001, E2010, E2021, E2022
r = P('P1-E2001-APP') + '#6'
edit('TC-P1-E2001-APP-15', r, 'one read and the provider fake', title='Section 12: the one read at contract level',
     **case('The provider fake of rwb-source-data.yaml 5.1.0 for "GET /efs-history"', 'The contract test runs one mapping per documented status',
            '200 answers "EfsHistoryAnswer" (A-0001, 16 rows); 400 MSG-GEN-001, 401 MSG-P4-001, 403 MSG-P4-002, 409 MSG-P1-001 and 503 MSG-GEN-006 are "application/problem+json"; the story publishes and consumes no event and registers no activity',
            'fakes/rwb-source-data/5.1.0/'))
edit('TC-P1-E2001-APP-16', r, 'limited to the views', title='Section 12.7: the three views are read only',
     **case('"v_ace_efs_action", "v_ace_efs_assignment" and "v_ace_batch_status" in schema "recovery"', 'The read runs and a write is attempted on each view',
            'The read selects from the three views; each write attempt is refused; no table or column is created and this story writes no row',
            'The three views of section 12.7'))
k = P('P1-E2001-APP')
for t, a, d in (('TC-P1-E2001-APP-22', 'AC2', 'A second identical view row "EFS-SYN-0007"; two reads of "A-0001" for 2026-12-14'),
                ('TC-P1-E2001-APP-24', 'AC4', 'COMPLETED ALS row for 2026-12-14 and none for 2026-12-15'),
                ('TC-E2-001-21', 'AC6', 'The "action_code" of "EFS-SYN-0001" changed between two reads')):
    edit(t, r, 'realigned to %s' % a, cov=a, data=d)
retire('TC-P1-E2001-APP-17', r, 'Retired: the decision log write is rwb-decision behaviour, no criterion of this story; the 5 s view failure is AC7 (TC-P1-E2001-APP-04)')
retire('TC-P1-E2001-APP-18', r, 'Retired: the refused second start belongs to the run, no criterion of this story; the caller refusal is AC8 (TC-P1-E2001-APP-05)')

for t in ('TC-E2-010-06', 'TC-E2-010-07'):
    edit(t, P('P1-E2010-APP') + '#11', 'removed from RWB-P1-E2010-APP; TC-P1-E2010-APP-09 and -10 prove AC6 and AC7 there',
         keys='; '.join(x.strip() for x in tcs[t][15].split(';') if x.strip() != P('P1-E2010-APP')))

r = P('P1-E2021-APP') + '#3'
edit('TC-P1-E2021-APP-14', r, 'out-of-scope answer of the record read as RWB-P1-E1016-APP AC5 (404), matching the section 16 data', title='A case outside the caller scope on the DP02 record read',
     **case('Notice "N-0200" and its case outside the scope of the caller', 'The dispatch loop calls "GET /data-products/DP02/records" with that case uuid',
            'The answer is 404 with MSG-P4-003 and no row is answered (the record read of RWB-P1-E1016-APP, AC5)', tcs['TC-P1-E2021-APP-14'][10]))
k = P('P1-E2021-APP')
edit('TC-P1-E2021-APP-16', r, 'access case restated to AC9 (no right: 403)', cov='AC9', level='Component',
     **{x: y for x, y in from_ac(k, ['AC9'], data="The caller's role carries no right on the read of the case; refused with MSG-P4-002").items() if x != 'cov'})

r = P('P1-E2022-APP') + '#5'
edit('TC-P1-E2022-APP-05', r, 'data matched to AC1 (consent WITHDRAWN)', data='P-0077 verified MOBILE contact point, consent WITHDRAWN, failed count 0; NSS stub reference NSS-7781')
retire('TC-P1-E2022-APP-17', r, 'Retired: the message send right belongs to RWB-P4-E2022-APP; access on this story is AC10, AC12 and AC13')

# ---------------------------------------------------------------- rows sync.py reports as behind the story text
SYNCED = {'TC-P1-E1016-CON-01': ('P1-E1016-CON', None), 'TC-P1-E1016-CON-10': ('P1-E1016-CON', None), 'TC-P1-E1016-CON-02': ('P1-E1016-CON', None),
          'TC-P1-E1016-CON-21': ('P1-E1016-CON', None), 'TC-P1-E1018-APP-23': ('P1-E1018-APP', None)}
for t, (s, _) in SYNCED.items():
    k = P(s)
    covered = [a for a in re.findall(r'AC\d+[a-z]?', str(tcs[t][4]).split('—')[0]) if a in stories[k]['acs']]
    d = from_ac(k, covered)
    edit(t, '', 'synced to the current criterion text of %s %s' % (k, ', '.join(covered)), given=d['given'], when=d['when'], then=d['then'])

# ================================================================ apply
wbw = openpyxl.load_workbook(TC)
ws = wbw['Story test cases']
rowno = {ws.cell(i, 1).value: i for i in range(5, ws.max_row + 1) if ws.cell(i, 1).value}
logrows, changed, retired = [], [], []


def clip(s):
    s = str(s or '').replace('\n', ' ')
    return s if len(s) <= 400 else s[:399] + '…'


def log(action, f, section, before, after, refs=''):
    logrows.append(['%s-%04d' % (AGENT, len(logrows) + 1), action, f, 'v9', 'v9', section, clip(before), clip(after), refs, '', '', MODEL, AGENT])


oldkeys = {}
for tid, (ref, note, vals) in EDIT.items():
    i = rowno[tid]
    before, after = [], []
    oldkeys[tid] = str(ws.cell(i, 16).value or '')
    for name, v in vals.items():
        c = ws.cell(i, COL[name] + 1)
        if c.value != v:
            before.append('%s=%s' % (name, str(c.value)[:120]))
            after.append('%s=%s' % (name, str(v)[:120]))
            c.value = v
    if after:
        changed.append(tid)
        log('EDIT', TCF, 'Story test cases %s (%s)' % (tid, note), '; '.join(before), '; '.join(after), ref)
    else:
        print('no change', tid)
for tid, (ref, reason) in RET.items():
    i = rowno[tid]
    if ws.cell(i, 13).value == 'Retired':
        print('already retired', tid)
        continue
    assert ws.cell(i, 13).value == 'Live'
    ws.cell(i, 13).value = 'Retired'
    ws.cell(i, 14).value = reason
    ws.cell(i, 12).value = 'No'
    retired.append(tid)
    log('REMOVE', TCF, 'Story test cases %s (row kept, marked Retired)' % tid, 'Live', 'Retired. ' + reason, ref)

now = {ws.cell(i, 1).value: [ws.cell(i, c).value for c in range(1, 19)] for i in rowno.values()}
total, live = len(now), sum(1 for r in now.values() if r[12] == 'Live')
old = ws['A2'].value
ws['A2'].value = re.sub(r'^\d+ rows, \d+ live', '%d rows, %d live' % (total, live), old)
log('EDIT', TCF, 'Story test cases A2 totals', old, ws['A2'].value)
cell = wbw['Read me']['C22']
old = cell.value
cell.value = re.sub(r'Story test cases: \d+ rows \(\d+ Live\)', 'Story test cases: %d rows (%d Live)' % (total, live), old)
log('EDIT', TCF, 'Read me C22 totals', old, cell.value)

# ---------------------------------------------------------------- RTM
rtw = openpyxl.load_workbook(RTM)
trs, rts = rtw['Criterion trace'], rtw['RTM']
tr_row = {(trs.cell(i, 1).value, trs.cell(i, 2).value): i for i in range(5, trs.max_row + 1) if trs.cell(i, 1).value}
split = lambda v: [x.strip() for x in str(v or '').split(',') if x.strip()]
req_rows = {rts.cell(i, 1).value: i for i in range(11, rts.max_row + 1) if rts.cell(i, 1).value}


def keys_of(t):
    return [x.strip() for x in str(now[t][15] or '').split(';') if x.strip()]


def acs_of(t):
    c = str(now[t][4] or '').split('—')[0]
    return [] if c.startswith(('Legacy', 'Owner')) else list(dict.fromkeys(re.findall(r'AC\d+[a-z]?', c)))


gain = collections.defaultdict(list)   # (k, ac) -> tids
for t in changed:
    if now[t][12] != 'Live':
        continue
    for k in keys_of(t):
        if k in stories and len(keys_of(t)) <= 2 and not k.startswith('RWB-ITG'):
            for a in acs_of(t):
                if (k, a) in tr_row:
                    gain[(k, a)].append(t)
req_add, req_drop = collections.defaultdict(list), collections.defaultdict(list)
for (k, a), i in tr_row.items():
    cur = split(trs.cell(i, 4).value)
    new = [x for x in cur if x not in retired and not (x in changed and k not in keys_of(x))
           and not (x in changed and 'cov' in EDIT.get(x, ('', '', {}))[2] and k in keys_of(x) and acs_of(x) and a not in acs_of(x))]
    new += [x for x in gain.get((k, a), []) if x not in new]
    if new != cur:
        assert new, ('empty trace', k, a, cur)
        trs.cell(i, 4).value = ', '.join(new)
        log('EDIT', RTF, 'Criterion trace %s %s' % (k, a), ', '.join(cur), ', '.join(new))
    for q in split(trs.cell(i, 5).value):
        req_add[q] += [x for x in gain.get((k, a), [])]
for q, i in req_rows.items():
    cur = split(rts.cell(i, 11).value)
    new = [x for x in cur if x not in retired]
    new += [x for x in dict.fromkeys(req_add.get(q, [])) if x not in new]
    if new != cur:
        rts.cell(i, 11).value = ', '.join(new)
        cov = str(rts.cell(i, 18).value or '')
        rts.cell(i, 18).value = re.sub(r'Tests: \d+ test cases', 'Tests: %d test cases' % len(new), cov)
        log('EDIT', RTF, 'RTM %s Tests' % q, 'removed: ' + ', '.join(x for x in cur if x not in new), 'added: ' + ', '.join(x for x in new if x not in cur))
dead = [(ws_.title, i, x) for ws_, col in ((rts, 11), (trs, 4)) for i in range(5, ws_.max_row + 1)
        for x in split(ws_.cell(i, col).value) if x.startswith('TC-') and (x not in now or now[x][12] != 'Live')]
assert not dead, dead[:5]

# ---------------------------------------------------------------- tc-backfill
rows = list(csv.reader(open(BACK, encoding='utf-8-sig')))
keep, dropped, seen = [rows[0]], [], set()
for k, a, t in rows[1:]:
    gone = t in retired or (t in changed and k not in keys_of(t)) or (
        t in changed and 'cov' in EDIT[t][2] and k in keys_of(t) and acs_of(t) and a not in acs_of(t))
    (dropped if gone else keep).append([k, a, t])
    if not gone:
        seen.add((k, a, t))
added = [[k, a, t] for (k, a), ts in gain.items() for t in ts if (k, a, t) not in seen]
log('EDIT', 'tc-backfill.csv', 'story, criterion, test case pairs',
    '; '.join(' '.join(x) for x in dropped), '; '.join(' '.join(x) for x in added))

print('rows edited', len(changed), 'retired', len(retired), 'total', total, 'live', live)
print('backfill dropped', len(dropped), 'added', len(added))
for x in dropped:
    print('  -', ' '.join(x))
for x in added:
    print('  +', ' '.join(x))
print('log rows', len(logrows), collections.Counter((r[2][:20], r[1]) for r in logrows))

if WRITE:
    wbw.save(TC)
    rtw.save(RTM)
    with open(BACK, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(keep + added)
    new_file = not os.path.exists(LOG)
    assert new_file
    with open(LOG, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow('edit_id,action,file,old_version,new_version,section,before,after,finding_refs,decision_refs,gap_asm_refs,model,agent'.split(','))
        w.writerows(logrows)
    # record of the new or changed IDs
    with open(W + '/qa/rf-tests/changed-ids.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(['tc_id', 'change', 'story_keys', 'covers'])
        for t in changed:
            w.writerow([t, 'changed', now[t][15], now[t][4]])
        for t in retired:
            w.writerow([t, 'retired', now[t][15], now[t][4]])
    print('written')
