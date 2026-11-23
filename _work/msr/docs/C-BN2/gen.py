# C-BN2 builder: Build Notes Epic 2 v4 from v3 + D-RCV-60 realignment.
# Reads the source read-only, applies audited literal edits, inserts per-story
# realignment blocks from the plan and the Service Story Catalog, writes v4.
import json
import re
import sys
from pathlib import Path

ROOT = Path(r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14')
SRC = ROOT / '04 User stories' / 'Recovery Workbench Build Notes Epic 2 v3.md'
OUT = ROOT / '04 User stories' / 'Recovery Workbench Build Notes Epic 2 v4.md'
WORK = ROOT / '_work' / 'msr'
COVER = '22 November 2026'
TOOL = 'T3 Code / OpenCode / DeepSeek v4.1 Flash'

t = SRC.read_text(encoding='utf-8')
original = t

# ---------------------------------------------------------------- services
import openpyxl
wb = openpyxl.load_workbook(str(ROOT / '22 Microservice Realignment' / 'Recovery Workbench Microservice Ownership Map v1.xlsx'),
                            read_only=True, data_only=True)
SVC = {}
for row in list(wb['Services'].iter_rows(values_only=True))[1:]:
    code, svc, name, wave, schema, base, topic, queue = row[:8]
    SVC[code] = dict(code=code, svc=svc, name=name, wave=wave, schema=schema,
                     base=base, topic=topic, queue=queue,
                     pkg='th.co.scb.ace.workbench.recovery.' + svc.replace('rwb-', '').replace('-', ''))

# ---------------------------------------------------------------- plan
plan = json.load(open(WORK / 'plan' / 'split_plan.json', encoding='utf-8'))['legacy']

# ---------------------------------------------------------------- catalogue
cw = openpyxl.load_workbook(str(ROOT / '04 User stories' / 'Recovery Workbench Service Story Catalog v1.xlsx'),
                            read_only=True, data_only=True)
crows = list(cw['Stories'].iter_rows(values_only=True))
ch = crows[0]
ci = {h: i for i, h in enumerate(ch)}
CAT = {}
for r in crows[1:]:
    leg = str(r[ci['Legacy']] or '')
    if not re.match(r'RWB-E2-0\d\d$', leg):
        continue
    CAT.setdefault(leg, []).append(dict(story=r[ci['Story']], wt=r[ci['Work type']], svc=r[ci['Service']],
                                        epic=r[ci['Epic']], wave=r[ci['Wave']], be=r[ci['Business epic']],
                                        rel=r[ci['Release']], lane=r[ci['Lane']], ready=r[ci['Ready']]))

# ---------------------------------------------------------------- edits
# (old, new, expected count) — every literal is asserted before it is applied.
EDITS = [
    # ---- EV-26 is AceDataReady in the Arch v5 catalogue (CG-1, ASM-2)
    ('JOB-01 publishes LoadCompleted (EV-26)', 'rwb-source-data publishes AceDataReady (EV-26)', 3),
    ('Quartz starts this job; no person starts it. The trigger is daily and chained on an event: '
     'JOB-01 publishes LoadCompleted, event EV-26, when the ALS load for a business date has passed its checks, '
     'and JOB-08 runs after that.',
     'The rwb-payment event-started workflow confirmBookings (JOB-08 in the job catalogue) starts this job; '
     'no person starts it. The trigger is daily and chained on an event: rwb-source-data publishes AceDataReady, '
     'event EV-26, when the ALS load for a business date has passed its checks, and JOB-08 runs after that.', 1),
    ('Build PaymentMatchingJob as a Spring Batch job started by the LoadCompleted event, EV-26, that JOB-01 publishes '
     'for the ALS source once every check has passed.',
     'Build matchPayments, the event-started workflow in rwb-payment (JOB-07 in the job catalogue), started by the '
     'AceDataReady event, EV-26, that rwb-source-data publishes for the ALS source once every check has passed.', 1),
    ('EV-26 LoadCompleted for the COLLINS load', 'EV-26 AceDataReady for the COLLINS load', 1),
    ('ProceedsMatched, and LoadCompleted for the COLLINS load',
     'ProceedsMatched, and AceDataReady for the COLLINS load', 1),
    ('EfsContactOutcomeImporter (for LoadCompleted)', 'EfsContactOutcomeImporter (for AceDataReady)', 1),
    # ---- E2-001 hand-over split: rwb-integration does the work, rwb-case runs the job
    ('Build HandoverJob as the JOB-02 step in the Java package recovery.integration.handover, and chain JOB-03 '
     'allocation after it.',
     'Build HandoverJob as the hand-over step of rwb-integration, run from the rwb-case DailyCaseRun (JOB-02 in the '
     'job catalogue) through the rwb-integration contract, and chain JOB-03 allocation after it. The code sits in the '
     'Java package recovery.integration.handover.', 1),
    # ---- E2-004 durable timers replace JOB-05 and TimerDue
    ('**In the story.** JOB-05 Timer check: at the timer\'s expiry publishes TimerDue (EV-18) with the timer type and '
     'the treatment ID, and sets the timer status to EXPIRED.',
     '**In the story.** Durable timer: at the timer\'s expiry the treatment workflow wakes with the timer type and the '
     'treatment ID, and the timer status is set to EXPIRED.', 1),
    ('JOB-05 is the timer job from RWB-E1-028. It runs every five minutes and needs no change of its own. When it finds '
     'a timer past its expiry it publishes TimerDue and moves the timer status from RUNNING to EXPIRED. Your part is to '
     'make the INSTALLMENT_DUE timers it reads carry what the event needs, including the treatment_id column this story '
     'adds to timer with the index ix_timer_treatment_id.',
     'The timer is now a durable Temporal timer inside TreatmentWorkflow: JOB-05 from RWB-E1-028 and its five-minute '
     'timer check are retired (DP-10), and TimerDue (EV-18) is no longer an event type. When the INSTALLMENT_DUE timer '
     'expires the workflow continues on its own and the timer row that the screen projects is set to EXPIRED. Your part '
     'is to make the INSTALLMENT_DUE timers carry what the expiry needs, including the treatment_id column this story '
     'adds to timer with the index ix_timer_treatment_id.', 1),
    # ---- E2-004 rules come from the rwb-decision registry, evaluated locally
    ('The rule rows R-RES-25 and R-RES-27 sit in the Restructure route set and are loaded by the center of excellence '
     'through RWB-E1-073, so a condition can change without a code change.',
     'The rule rows R-RES-25 and R-RES-27 sit in the RESTRUCTURE rule package in rwb-decision (P7) and are loaded by '
     'the center of excellence through RWB-E1-073, so a condition can change without a code change; rwb-treatment '
     'evaluates them with the embedded Drools kit (DP-04).', 1),
    ('Add TreatmentExtractStep as a Spring Batch step in JOB-15.',
     'Add TreatmentExtractStep as a Spring Batch step of the rwb-reporting extract, JOB-15 in the job catalogue.', 1),
    # ---- E2-005, E2-013, E2-015, E2-041 per-service Flyway
    ('in migration V_E2_005__declog_approver_index.sql.',
     'in migration V_E2_005__declog_approver_index.sql of the rwb_decision Flyway sequence (DP-15).', 1),
    ('Create the row in the new approval table from the migration V_E2_013__approval.sql',
     'Create the row in the new approval table from the migration V_E2_013__approval.sql of the rwb_decision Flyway '
     'sequence', 1),
    ('JOB-05 of RWB-E1-028 publishes EV-19 TimerBreached',
     'The durable approval timer in ApprovalWorkflow raises EV-19 TimerBreached on rwb.case.events.v1', 1),
    ('migration V<next>__rwb_e2_015_timer_escalation.sql adds timer.escalated_to_role and timer.escalated_at, and '
     'EscalationRecorder changes the escalation step of JOB-05 from RWB-E1-028 to write them.',
     'migration V<next>__rwb_e2_015_timer_escalation.sql in the rwb_case Flyway sequence adds '
     'timer.escalated_to_role and timer.escalated_at, and EscalationRecorder writes them from the durable timer '
     'escalation step of CaseWorkflow (JOB-05 is retired).', 1),
    ('Store the checklist in `rule_package_version.change_checklist` (DF-REF-295) with the author, load time and '
     'checksum.',
     'Store the checklist in `rule_package_version.change_checklist` (DF-REF-295) in the rwb_decision sequence with '
     'the author, load time and checksum.', 1),
    # ---- E2-009 no data lake (DP-17)
    ('writes the snapshot rows and the INT-19 extract with the freshness stamp',
     'writes the snapshot rows and the reporting events with the freshness stamp', 1),
    ('On a match, write the measure_snapshot rows for the business date with published_at set, and write the INT-19 '
     'extract for the data lake with its freshness stamp.',
     'On a match, write the measure_snapshot rows for the business date with published_at set, and publish the measure '
     'events on rwb.reporting.events.v1 with the freshness stamp. The INT-19 extract and the data lake are removed '
     '(DP-17), so rwb-reporting is the interface the data set reads.', 1),
    ('Your part is that the INT-19 extract for the business date is in place with its freshness stamp before 07:30, '
     'which AC1 states.',
     'Your part is that the published measure rows for the business date are in place with their freshness stamp '
     'before 07:30, which AC1 states.', 1),
    ('On a held day there is no new extract, so the report keeps showing the previous published day with that day\'s '
     'date.',
     'On a held day there is no new published set, so the report keeps showing the previous published day with that '
     'day\'s date.', 1),
    # ---- E2-010 JOB-01 retired, ingest is the rwb-source-data workflow
    ('The stage 2 step is a new part of JOB-01, wired in after the COLLINS load for business date D has passed its '
     'own checks, so it runs daily before 07:00.',
     'The stage 2 step is a new step of the rwb-source-data ingest workflow AceIngestCheck (JOB-04 in the job '
     'catalogue), wired in after the AceDataReady event for business date D has passed its own checks, so it runs '
     'daily before 07:00.', 1),
    # ---- E2-018, E2-019 table ownership
    ('Create the table in the migration V2_018__signature_request.sql with a unique index on external_ref',
     'Create the table in the rwb_document migration V2_018__signature_request.sql of the P5 Flyway sequence, because '
     'the signature request is a document hub record (ownership ruling), with a unique index on external_ref', 1),
    ('Create the table partner_user with the migration V_E2_019__partner_user.sql,',
     'Create the table partner_user in the rwb_partner migration V_E2_019__partner_user.sql of the S9 Flyway '
     'sequence, because the partner user binding is a partner module record (ownership ruling),', 1),
    # ---- E2-021 JOB-10 as a Temporal Schedule, JOB-09 retired
    ('Build ConductCheckService and call it from WinNoticeFileJob, which comes from RWB-E1-055, before each file '
     'record is written.',
     'Build ConductCheckService and call it from WinNoticeFileJob, which comes from RWB-E1-055 and runs as the JOB-10 '
     'Temporal Schedule in rwb-comms with the file delivered by rwb-integration, before each file record is written.', 1),
    ('**In the story.** JOB-09: loads the INT-15 file; a Delivered record sets Delivered and publishes '
     'NoticeDelivered; P3 starts the notice period from the delivery date (R-LIT-07).',
     '**In the story.** rwb-source-data: loads the INT-15 file through its ACE view contract; a Delivered record sets '
     'Delivered and publishes NoticeDelivered; P3 starts the notice period from the delivery date (R-LIT-07).', 1),
    ('JOB-09 loads the file on its own. Add the INT-15 result column to the file reader',
     'rwb-source-data loads the file through the ACE view contract and publishes the delivery result on '
     'rwb.source-data.events.v1, which rwb-comms consumes; JOB-09 is retired, so no separate result loader is built. '
     'Add the INT-15 result column to the file reader', 1),
    # ---- E2-022 outbox relay is library work in every service
    ('JOB-11 runs every minute and picks up queued sends, with no person involved.',
     'The outbox relay, JOB-11 in the job catalogue and a library object in every service schema, runs every minute in '
     'rwb-comms and picks up queued sends, with no person involved.', 1),
    # ---- E2-023 reconciliation mechanism
    ('JOB-04 Daily reconciliation is already scheduled on Control-M from RWB-E1-051 and runs after JOB-02 for '
     'business date D',
     'JOB-04 reconciliation runs as the event-started workflow in rwb-source-data from RWB-E1-051 and runs after '
     'JOB-02 for business date D', 1),
    # ---- E2-034 inbox per service, ingest workflow
    ('Your work is to add a consumer named ledger-channels to rwb.integration.outbox.consumers and have it take seven '
     'events:',
     'Your work is to add the consumer group ledger-channels to the inbox of rwb-source-data, which holds the ledger '
     '(DP-18; the outbox and inbox are library objects in every service schema, DP-09), and have it take seven '
     'events:', 1),
    ('Write EfsContactOutcomeImporter as a step of JOB-01 COLLINS load check and intake, running under SY-DATALOAD '
     'after the load passes its checks.',
     'Write EfsContactOutcomeImporter as a step of the rwb-source-data ingest workflow AceIngestCheck (JOB-04 in the '
     'job catalogue), running under the rwb-source-data identity after the load passes its checks.', 1),
    # ---- E2-035 the five-minute check is a Temporal Schedule in rwb-case
    ('**In the story.** JOB-05 timer check: every 5 minutes finds active cases with no next action, resolves them from '
     'the latest state change in the decision log, or raises the same task once.',
     '**In the story.** Case schedule: every 5 minutes finds active cases with no next action, resolves them from the '
     'latest state change in the decision log, or raises the same task once.', 1),
    ('Build NextActionCheckStep inside JOB-05 Timer check, which runs every five minutes,',
     'Build NextActionCheckStep as a step of CaseWorkflow at each state change and as the five-minute Temporal '
     'Schedule in rwb-case that replaces the retired JOB-05 timer check,', 1),
    # ---- E2-037, E2-039 Quartz retired
    ('StuckWorkflowScanner runs every 15 minutes on Quartz and raises TemporalWorkflowStuck with MSG-P3-037.',
     'StuckWorkflowScanner runs every 15 minutes as the JOB-21 Temporal Schedule on rwb-platform and raises '
     'TemporalWorkflowStuck with MSG-P3-037.', 1),
    ('Build the scanner as a Quartz job under T2, running as SY-CASEWF with the client certificate of RWB-E1-070. It '
     'reads the visibility store, not the recovery schema,',
     'Build the scanner as the JOB-21 Temporal Schedule on the rwb-platform task queue, running as SY-CASEWF with the '
     'client certificate of RWB-E1-070. It reads the visibility store, not any service\'s own schema,', 1),
    ('Run the archive job on Quartz at 02:00 under T2, not on a Temporal Schedule.',
     'Run the archive job as a Temporal Schedule on rwb-platform at 02:00, since the monolith scheduler is '
     'retired (DP-10).', 1),
    # ---- E2-027 payment match rules are the PAYMENT_MATCH rule package (CG-5, CG-6)
    ('**In the story.** Reference data administrator: loads a parameter version through POST /admin/reference-loads '
     'with table "payment_match_rule" and a valid from date.',
     '**In the story.** Reference data administrator: loads a version of the PAYMENT_MATCH rule package through '
     'POST /admin/rule-packages/{packageCode}/versions with a valid from date.', 1),
    ('A person does this: the reference data administrator, holding Reference data right C. They post the file to '
     '/api/recovery/v1/admin/reference-loads as multipart form data with the file, the table name payment_match_rule '
     'and a valid from date. P4 owns the endpoint. Your work is PaymentMatchRuleLoadHandler, a ReferenceLoadHandler '
     'for that table, with its validate and apply methods. A version is a set of rows sharing a rule_version such as '
     'PM-2026.12, each row holding a rule code, a priority, a match type, an amount tolerance, window days before and '
     'after, and a partial floor. The endpoint takes the SHA-256 hash of the file per table, so a file already loaded '
     'is refused with 409 and MSG-P1-002.',
     'A person does this: the reference data administrator, holding Reference data right C, loads the workbook as the '
     'PAYMENT_MATCH rule package version through rwb-decision, which owns the registry and the endpoint (RWB-E2-042); '
     'the reference load role is held through the rwb-access role contract (DP-08). Your work is the PAYMENT_MATCH '
     'workbook and its scenario set: a version is a set of rows sharing a rule_version such as PM-2026.12, each row '
     'holding a rule code, a priority, a match type, an amount tolerance, window days before and after, and a partial '
     'floor. The load runs the compile, schema, overlap, unreachable row, default row, scenario and dry run checks of '
     'RWB-E1-073, and a workbook already loaded is refused with 409 and MSG-P1-002.', 1),
    ('Migration V2_027__match_rule_partial.sql adds partial_floor_pct as numeric(5,2), the check constraint on the '
     'tolerance, and a unique key on rule_version and priority.',
     'The PAYMENT_MATCH rows carry partial_floor_pct, the check on the tolerance and the unique priority within the '
     'version, and no match rule table is created in any service schema (DP-04).', 1),
    ('**In the story.** JOB-07: for the business date, reads the parameter version in force on that date.',
     '**In the story.** JOB-07: for the business date, reads the rule package version in force on that date.', 1),
    ('JOB-07 does this at the start of its run, with no person involved. The job already exists from RWB-E2-008. For '
     'the business date it is matching, read the rule rows whose valid_from is on or before that date and whose '
     'valid_to is empty or later, and use that one version for the whole run.',
     'matchPayments does this at the start of its run, with no person involved, in rwb-payment. The workflow already '
     'exists from RWB-E2-008. For the business date it is matching, read the PAYMENT_MATCH rows through '
     'RuleCatalog.row whose valid_from is on or before that date and whose valid_to is empty or later, and use that '
     'one version for the whole run; the rows come from rwb-decision over the registry contract and are evaluated '
     'locally by the embedded Drools kit (DP-04).', 1),
    ('tries the rows in priority order (EXACT, then WINDOW, then PARTIAL) against each running plan on the case',
     'tries the rows in priority order (EXACT, then PARTIAL, then WINDOW) against each running plan on the case', 1),
    ('Build MatchRuleEvaluator to take the rows of the version in force, sort them by priority and try each one '
     'against every running plan on the case, stopping at the first row that matches.',
     'Build MatchRuleEvaluator to take the rows of the version in force, sort them by priority and try each one '
     'against every running plan on the case, stopping at the first row that matches; the order is EXACT, then '
     'PARTIAL, then WINDOW, which RWB-E2-042 fixes for the package.', 1),
    ('When two rows would both match, the lower priority number decides, so a payment of the exact installment amount '
     'is matched by EXACT even though WINDOW also fits.',
     'When two rows would both match, the lower priority number decides, so a payment of the exact installment amount '
     'is matched by EXACT even though PARTIAL also fits.', 1),
    ('holding rule R-RES-26, the rule version equal to the parameter version in force,',
     'holding rule R-RES-26, the rule version equal to the rule package version in force,', 1),
    ('**In the story.** System: writes the D5 decision log entry with rule R-RES-26, rule version equal to the '
     'parameter version, the row code and the inputs; then writes the proceeds row and calls TreatmentApi.',
     '**In the story.** System: writes the D5 decision log entry with rule R-RES-26, rule version equal to the rule '
     'package version, the row code and the inputs; then writes the proceeds row and calls TreatmentApi.', 1),
    ('Until SCR-40 Reference data is built, the administrator reads the result of a parameter load on the reference '
     'load record.',
     'Until SCR-40 Reference data is built, the administrator reads the result of a package load on the rule package '
     'version record in rwb-decision.', 1),
]

for old, new, n in EDITS:
    got = t.count(old)
    if got != n:
        sys.exit('EDIT COUNT MISMATCH (%d != %d): %s' % (got, n, old[:120]))
    t = t.replace(old, new)

# ---------------------------------------------------------------- API bases (DP-13)
API = [
    ('/api/recovery/v1/admin/agent-', '/api/recovery/agent/v1/admin/agent-'),
    ('/api/recovery/v1/agent-runs/', '/api/recovery/agent/v1/agent-runs/'),
    ('/api/recovery/v1/cases/{caseId}/agent-outputs', '/api/recovery/agent/v1/cases/{caseId}/agent-outputs'),
    ('/api/recovery/v1/cases/{caseId}/generated-documents', '/api/recovery/document/v1/cases/{caseId}/generated-documents'),
    ('/api/recovery/v1/cases/{caseId}/notices', '/api/recovery/comms/v1/cases/{caseId}/notices'),
    ('/api/recovery/v1/cases/{caseId}/interactions', '/api/recovery/case/v1/cases/{caseId}/interactions'),
    ('/api/recovery/v1/cases/{caseId}/next-action', '/api/recovery/case/v1/cases/{caseId}/next-action'),
    ('/api/recovery/v1/cases/export', '/api/recovery/case/v1/cases/export'),
    ('/api/recovery/v1/cases', '/api/recovery/case/v1/cases'),
    ('/api/recovery/v1/queues', '/api/recovery/case/v1/queues'),
    ('/api/recovery/v1/approvals', '/api/recovery/decision/v1/approvals'),
    ('/api/recovery/v1/decision-log', '/api/recovery/decision/v1/decision-log'),
    ('/api/recovery/v1/notices', '/api/recovery/comms/v1/notices'),
    ('/api/recovery/v1/documents', '/api/recovery/document/v1/documents'),
    ('/api/recovery/v1/proceeds', '/api/recovery/payment/v1/proceeds'),
    ('/api/recovery/v1/data-products', '/api/recovery/source-data/v1/data-products'),
    ('/api/recovery/v1/admin/data-quality', '/api/recovery/source-data/v1/admin/data-quality'),
    ('/api/recovery/v1/admin/jobs', '/api/recovery/integration/v1/admin/jobs'),
]
for old, new in API:
    if old not in t:
        sys.exit('API literal missing: ' + old)
    t = t.replace(old, new)

# ---------------------------------------------------------------- packages
PKG = [
    ('recovery.data.api', 'recovery.sourcedata.api', 3),
    ('recovery.casewf.plan', 'recovery.case.plan', 1),
    ('recovery/casewf/placement', 'recovery/case/placement', 1),
    ('recovery.dochub.extract', 'recovery.document.extract', 1),
    ('recovery.dataengine.ledger', 'recovery.sourcedata.ledger', 1),
]
for old, new, n in PKG:
    got = t.count(old)
    if got != n:
        sys.exit('PKG COUNT MISMATCH (%d != %d): %s' % (got, n, old))
    t = t.replace(old, new)

if '/api/recovery/v1' in t:
    sys.exit('old API base left: ' + str(re.findall(r'/api/recovery/v1\S*', t)))
for bad in ('Quartz', 'Control-M', 'publishes LoadCompleted', '"payment_match_rule"'):
    if bad in t:
        sys.exit('marker left: ' + bad)
if t.count('INT-19') != 1:
    sys.exit('INT-19 left: %d' % t.count('INT-19'))

# ---------------------------------------------------------------- story notes
NOTES = {
'RWB-E2-001': 'The hand-over is rwb-integration work. It is started by the P1 event AceDataReady (EV-26) on '
    'rwb.source-data.events.v1, because JOB-01 is retired and ACE ingestion is read through the rwb-source-data view '
    'contract (DP-05). Case creation, the decision record and the account reads are calls on the rwb-case, rwb-decision '
    'and rwb-source-data contracts, never reads of their tables (DP-01, DP-03, DP-11), and the run summary is a '
    'rwb_integration interface_run row.',
'RWB-E2-002': 'The daily plan-status step stays in rwb-integration, started by the P2 schedule and switched by '
    'rwb.integration.ace-plan-status. It reads cases and writes plan_ref, plan_status and plan_status_as_of through the '
    'rwb-case contract (DP-11); those three columns are added in the rwb_case Flyway sequence (DP-15). ACE is reached '
    'only through its published interface, never by reading ACE tables (DP-05).',
'RWB-E2-003': 'The panel and its endpoint are rwb-integration: parties come from the rwb-case contract, products from '
    'the rwb-source-data contract and masking from the rwb-access masking rules (DP-05, DP-08, DP-11). The endpoint is '
    '/api/recovery/integration/v1/cases/{caseId}/customer-products.',
'RWB-E2-004': 'The treatment entity, its columns and its migration are S2 rwb-treatment records in rwb_treatment '
    '(DP-01, DP-15). The plan timers are durable Temporal timers inside TreatmentWorkflow and CaseWorkflow, because '
    'JOB-05 and TimerDue (EV-18) are retired (DP-10). R-RES-25 and R-RES-27 are rows of the RESTRUCTURE package in '
    'rwb-decision, evaluated by the embedded Drools kit in rwb-treatment (DP-04). The DP04 copy is written by '
    'rwb-source-data from the S2 contract (DP-01).',
'RWB-E2-005': 'The query screen and its endpoints are rwb-decision; the index migration sits in the rwb_decision '
    'sequence (DP-15) and the chain check runs as the JOB-14 Temporal Schedule in rwb-decision (DP-10). Access entries '
    'go to the local decision-record library and out on rwb.decision-record.v1 (DP-03); no lake copy is written (DP-17).',
'RWB-E2-006': 'The pack is assembled in rwb-integration from the rwb-treatment, rwb-source-data, rwb-document and '
    'rwb-decision contracts (DP-11). The checklist rows and the delegation levels stay data; the Workbench still never '
    'calls NLEADS.',
'RWB-E2-007': 'The booking match is rwb-integration work, run as the JOB-08 event-started workflow confirmBookings on '
    'AceDataReady (EV-26). TreatmentBooked (EV-11) is published by rwb-payment on rwb.payment.events.v1 and the '
    'treatment state moves through the rwb-treatment contract (DP-09, DP-11). Account values come from the '
    'rwb-source-data contract, never from loan_account (DP-01); the comparison rows are rows of the BOOKING_MATCH '
    'package in rwb-decision (DP-04).',
'RWB-E2-008': 'Matching is rwb-payment work, run as the JOB-07 event-started workflow matchPayments on AceDataReady '
    '(EV-26). Payments, plans, treatments and proceeds are read and written through the rwb-source-data, rwb-treatment '
    'and rwb-case contracts (DP-11), and PaymentMissed (EV-12) goes out on rwb.payment.events.v1 (DP-09). The match '
    'rules are rows of the PAYMENT_MATCH package (see RWB-E2-027).',
'RWB-E2-009': 'The steering extract is rwb-reporting work in the JOB-15 run that Airflow triggers. The INT-19 extract '
    'and the data lake are removed, so the published measure rows are the interface the data set reads (DP-17). Every '
    'figure comes through the rwb-case, rwb-decision, rwb-comms and rwb-agent contracts (DP-11), and the agent '
    'measures read rwb_agent records through the P10 contract, not a shared schema (DP-01).',
'RWB-E2-010': 'The stage 2 products are rwb-source-data records: dp_treatment and dp_guarantee_claim are copies in '
    'rwb_source_data built from the rwb-treatment and rwb-guarantee contracts (DP-01, DP-11), and the step runs inside '
    'the rwb-source-data ingest workflow AceIngestCheck (JOB-04), because JOB-01 is retired. Contract and case links '
    'come through the rwb-case contract.',
'RWB-E2-011': 'The queue views are rwb-case screens served from rwb_case on /api/recovery/case/v1. Labels come from '
    'the rwb-case reference data contract (DP-07), rights and scope from the rwb-access contract (DP-08), and the '
    'screens are composed through gateway-bff (DP-19).',
'RWB-E2-012': 'Transfer is rwb-case work: assignment, queue and case rows are rwb_case records, the decision entry is '
    'written through rwb-decision (DP-03), and the transfer rules are rows of the route package in rwb-decision '
    'evaluated by the embedded kit in rwb-case (DP-04). Deviation and hold checks come through their contracts.',
'RWB-E2-013': 'Approval routing is rwb-decision work: the approval table and its migration sit in rwb_decision '
    '(DP-15), delegation limits come through the rwb-access DoA contract (DP-08), task and timer calls go to rwb-case '
    '(DP-11), and the approval timer is a durable timer inside ApprovalWorkflow, because the JOB-05 timer check is '
    'retired (DP-10).',
'RWB-E2-014': 'The listener and the panels sit across rwb-comms and rwb-decision: NoticeGenerated (EV-13) arrives on '
    'rwb.comms.events.v1, the approval calls go to the rwb-decision endpoints, and regeneration goes through the '
    'rwb-comms contract (DP-09, DP-11). The notice state stays a rwb_comms record.',
'RWB-E2-015': 'The panels are rwb-case views over rwb_case timer rows that project durable Temporal timers (DP-10); '
    'deviations come through the S8 contract with a 2 s timeout and escalation roles from the rwb-case parameter '
    'contract (DP-06). The escalation columns are added in the rwb_case sequence (DP-15).',
'RWB-E2-016': 'The full timeline is a rwb-case screen: it reads rwb_case assignment and timer rows and calls '
    'rwb-decision, rwb-document and rwb-comms for the other sources (DP-11); interactions are read from the '
    'rwb-source-data ledger contract (DP-18).',
'RWB-E2-017': 'The generation screens are rwb-document work on /api/recovery/document/v1. Treatment state comes '
    'through the rwb-treatment contract, templates through the rwb-comms contract, and the decision entry is written '
    'through rwb-decision (DP-03, DP-11).',
'RWB-E2-018': 'The e-signature flow is rwb-comms work with the signature request table owned by rwb-document (P5) and '
    'its migration in the rwb_document sequence. The conduct check calls the S8 and rwb-case contracts, the signed '
    'file is a rwb-document version, and the treatment records through the rwb-treatment contract (DP-11).',
'RWB-E2-019': 'Partner identities split across two services: rwb-access owns the identity, role, session and scope '
    'model and the partner portal entry screen, while the partner user binding is a rwb-partner (S9) record with its '
    'migration in the rwb_partner sequence. The firm panel status and contract end come through the S9 contract '
    '(DP-11).',
'RWB-E2-021': 'Letter dispatch is rwb-comms work, run as the JOB-10 Temporal Schedule with the file delivered by '
    'rwb-integration. The INT-15 result file is read by rwb-source-data through its ACE view contract, because JOB-09 '
    'is retired, and the result arrives from the P1 event (DP-05, DP-09). The ledger entry is a rwb-source-data record '
    '(DP-18) and the decision entry is written through rwb-decision (DP-03).',
'RWB-E2-022': 'SMS and LINE dispatch is rwb-comms work: templates, notices and the send are rwb_comms records, the '
    'conduct check reads the S8, rwb-case and rwb-source-data contracts, and the send leaves through the outbox relay '
    '(JOB-11) with the message on rwb.comms.events.v1 (DP-09). Consent and contact point values come through the '
    'rwb-source-data contract (DP-05).',
'RWB-E2-023': 'The reconciliation step is rwb-integration work inside the JOB-04 reconciliation that rwb-source-data '
    'runs, reading handed-over accounts through the rwb-source-data contract and writing its run summary to '
    'rwb_integration (DP-01, DP-10, DP-11). The primary service comes from the source module line. The plan holds no '
    'row for this story, so its new stories and its lanes are Not specified in the source documents '
    '(CG-C-BN2-11; ASM-C-BN2-12), and its wave of 2 follows the W-MAP rule for EP02.',
'RWB-E2-024': 'Field captures are rwb-document records: the new columns, the partial index and the migration sit in '
    'rwb_document (DP-15), the files go to the write-once container through the document store, and the case scope is '
    'read through the rwb-case contract (DP-11). Position masking follows the rwb-access masking rules (DP-08).',
'RWB-E2-025': 'Extraction stays in rwb-document: the document type table and the field definitions are rwb_document '
    'reference rows, the classifier runs through the rwb-agent runtime contract (DP-20), and confirmed fields are read '
    'by S2 and S4 through the DocumentFieldReader contract (DP-11).',
'RWB-E2-026': 'The generation engine is rwb-document work: templates come through the rwb-comms contract, treatment '
    'state through the rwb-treatment contract, merge values through the rwb-case and rwb-source-data contracts, and '
    'the decision entry through rwb-decision (DP-03, DP-11). Draft files stay in the rwb-document container.',
'RWB-E2-027': 'The match rules are the PAYMENT_MATCH rule package in rwb-decision, not a local reference table: the '
    'version is loaded through the rule package endpoints of RWB-E2-042 with the row checks of RWB-E1-073, and '
    'rwb-payment evaluates the rows through RuleCatalog.row with the embedded kit (DP-04). No payment_match_rule table '
    'exists in any service schema, and the priority order is EXACT, then PARTIAL, then WINDOW.',
'RWB-E2-028': 'Agent output is a rwb_agent record and the panel reads it through /api/recovery/agent/v1; the feedback '
    'decision entry is written through rwb-decision (DP-03) and the case scope is read through the rwb-case contract '
    '(DP-11). The case is a rwb_case record.',
'RWB-E2-029': 'The evaluation run is a rwb_agent record, the proposals come from /api/recovery/agent/v1, and a '
    'confirmed proposal raises a deviation through the S8 contract (DP-11) with the decision entries written through '
    'rwb-decision (DP-03).',
'RWB-E2-030': 'The batch runs in rwb-agent: inputs come through the S4 litigation and P5 document contracts '
    '(DP-11), the pack and the scores stay rwb_agent records, and no user facing endpoint returns the pack. Shadow '
    'runs never change a rwb_case or rwb_document record.',
'RWB-E2-031': 'The monitor is a rwb-agent screen on /api/recovery/agent/v1. The agent daily rows and the drift step '
    'run inside the JOB-15 run in rwb-reporting, reading rwb_agent records through the P10 contract and decision '
    'entries through rwb-decision (DP-03, DP-11).',
'RWB-E2-032': 'The suggestion is rwb-agent work: the treatment panel reads it through the rwb-agent contract (DP-20), '
    'the model call goes through the model gateway (INT-23), and the decision entry is written through rwb-decision '
    '(DP-03). The treatment stays a rwb_treatment record owned by S2.',
'RWB-E2-033': 'The case list is a rwb-case screen served from rwb_case on /api/recovery/case/v1. Ageing comes from '
    'rwb_case timer and case rows, lists from the rwb-case reference data contract (DP-07) and scope from the '
    'rwb-access contract (DP-08). The plan keeps rwb-integration as the primary service while the code sits in '
    'rwb-case, as RWB-E2-036 states for its own story (CG-C-BN2-13).',
'RWB-E2-034': 'The ledger is a rwb-source-data record (DP-18): the consumer group ledger-channels reads from the inbox '
    'of rwb-source-data, the interaction API stays with rwb-case and reads the ledger through the P1 contract, and '
    'retention classes are rwb-source-data reference rows.',
'RWB-E2-035': 'Next action is rwb-case work: the columns are added in rwb_case, the rule rows are the RESTRUCTURE '
    'package in rwb-decision and the evaluation runs in the embedded kit in rwb-case (DP-04). The five-minute check '
    'runs as a Temporal Schedule in rwb-case, because the JOB-05 timer check is retired (DP-10).',
'RWB-E2-036': 'The placement endpoint is a rwb-case endpoint on /api/recovery/case/v1, POST /queues/{queueId}/placements, '
    'even though the story sits in the P2 backlog; the code sits in rwb-case and the decision entry is written through '
    'rwb-decision (DP-03).',
'RWB-E2-037': 'The platform work sits on rwb-platform: the scanner runs as the JOB-21 Temporal Schedule, alerts and '
    'dashboards follow the per-service observability decision (ADR-023), and each alert carries its run book. No '
    'service schema is read; the scanner reads the Temporal visibility store.',
'RWB-E2-038': 'The codec server and the admin audit sit with rwb-access and rwb-platform: the decode endpoint is an '
    'rwb-access endpoint, the authorizer plugin loads from the platform values file, and every decode, terminate, '
    'reset and signal writes a decision entry for the central ledger (DP-03).',
'RWB-E2-039': 'Backup, failover, upgrade and archive are platform operations on rwb-platform. The archive runs as a '
    'Temporal Schedule at 02:00 because Quartz is retired (DP-10), and it writes to the write-once container.',
'RWB-E2-040': 'The replay export and the gate are platform material: histories stay in the SIT '
    'rwb-temporal-replay container, the gate runs per service build, and no production history leaves production.',
'RWB-E2-041': 'The rule registry and its version rows are rwb-decision records: the checklist column is added in the '
    'rwb_decision sequence, the approval and the change report are rwb-decision endpoints, and the governance '
    'workflow around them is the P3 story (ownership ruling).',
'RWB-E2-042': 'The three packages load, approve and promote in rwb-decision, and each service runs the embedded '
    'Drools kit against RuleCatalog.row (DP-04). No payment_match_rule table is created in any service schema.',
'RWB-E2-043': 'The pattern is platform material: ReferenceCaseWorkflow runs on rwb-platform with the workflow kit, '
    'rule evaluation runs in an activity against the rwb-decision rows, and the decision entry is written through the '
    'decision-record library (DP-03, DP-04).',
}

# ---------------------------------------------------------------- assemble
blocks = re.split(r'(?m)^(## RWB-E2-\d+ )', t)
preamble = blocks[0]
stories = [(blocks[i].strip().replace('## ', ''), blocks[i + 1]) for i in range(1, len(blocks), 2)]

assert len(stories) == 42, len(stories)
for k in NOTES:
    assert k in [s[0] for s in stories], k


def service_name(code):
    if code == 'PLT':
        return 'PLT Platform'
    if code == 'ITG':
        return 'ITG Integration (the RWB-ITG-W2 harness)'
    s = SVC[code]
    return '%s %s' % (code, s['name'])


def story_block(key, body):
    row = plan.get(key)
    cat = CAT.get(key, [])
    lanes = sorted({c['lane'] for c in cat if c['lane']})
    lanes = [l for l in lanes if l.startswith('CG-')] + [l for l in lanes if not l.startswith('CG-')]
    if row:
        primary = row['primary']
        codes = [primary] + [s.split('-')[1] for s in row['slices'] if s.split('-')[1] != primary]
        seen, order = set(), []
        for c in codes:
            if c not in seen:
                seen.add(c)
                order.append(c)
        module = 'Module: %s (primary), with %s.' % (
            service_name(primary), ', '.join(service_name(c) for c in order[1:])) if len(order) > 1 \
            else 'Module: %s (primary).' % service_name(primary)
        epic = 'RWB-PLT-WF' if primary == 'PLT' else 'RWB-SVC-%s' % primary
        wave = cat[0]['wave'] if cat else row['wave']
        be = cat[0]['be'] if cat else 'EP02'
        rel = cat[0]['rel'] if cat else '31 December 2026 (tentative)'
        slices = ', '.join(row['slices'])
        patterns = ', '.join('DP-' + p[2:] if p.startswith('DP') else p for p in row['patterns'])
        if primary == 'PLT':
            svcline = ('Primary service PLT Platform · service epic %s · wave %s · business epic %s · release %s · '
                       'task queue rwb-platform · namespace rwb-recovery. ' % (epic, wave, be, rel))
        else:
            s = SVC[primary]
            svcline = ('Primary service %s %s · service epic %s · wave %s · business epic %s · release %s · '
                       'schema %s · login %s · REST base %s · topic %s · task queue %s · Java package %s. '
                       % (primary, s['svc'], epic, wave, be, rel, s['schema'], s['schema'], s['base'], s['topic'],
                          s['queue'], s['pkg']))
        laneline = 'Lanes: %s.' % ', '.join(lanes) if lanes else 'Lanes: Not specified in the source documents (CG-C-BN2-11; ASM-C-BN2-12).'
        block = ('**Realignment (D-RCV-60).** ' + svcline + 'New stories: ' + slices + '. ' + laneline +
                 ' Patterns: ' + patterns + '.\n')
    else:
        module = None
        block = ('**Realignment (D-RCV-60).** Primary service P2 rwb-integration, taken from the source module line; '
                 'the plan holds no row for this story, so its new stories, lanes, epic and wave are Not specified in '
                 'the source documents (CG-C-BN2-11; ASM-C-BN2-12). Schema rwb_integration · login rwb_integration · '
                 'REST base /api/recovery/integration/v1 · topic rwb.integration.events.v1 · task queue rwb-integration '
                 '· Java package th.co.scb.ace.workbench.recovery.integration.\n')
    note = NOTES[key]
    body = body.replace('\n\n### Step 1', '\n\n' + block + '\n' + note + '\n\n### Step 1', 1)
    if module:
        body, n = re.subn(r'(?m)^Module: .*$', module, body, count=1)
        assert n == 1, key
    return ('## ' + key + ' ' + body).rstrip()


new_stories = '\n\n'.join(story_block(k, b) for k, b in stories)

# ---------------------------------------------------------------- front matter
HEAD = """SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench build notes, Epic 2

| Item | Value |
|---|---|
| Document | Recovery Workbench build notes, Epic 2 |
| Version | 4 |
| Date | 22 November 2026 |
| Decision applied | D-RCV-60 microservice realignment |
| Realigned from | Recovery Workbench Build Notes Epic 2 v3, 16 November 2026 |
| Stories covered | 42 |
| Services covered | 19 |
| Status | Draft |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 3 | 16 November 2026 | D-RCV-36 version; the source of this version, carried over word for word except where this log records a change | (source version) |
| 4 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

Change-log row: 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash
"""

# the source preamble, from the D-RCV-36 note to the paragraph before the first story
pre = preamble
i = pre.index('> **D-RCV-36.**')
pre = pre[i:].rstrip('\n')

SVCROWS = '\n'.join(
    '| %s | %s | %s | %s | %s | %s | %s | %s |' % (c, SVC[c]['svc'], SVC[c]['name'], SVC[c]['wave'],
                                                   SVC[c]['schema'], SVC[c]['base'], SVC[c]['topic'], SVC[c]['queue'])
    for c in SVC)

MID = """
## How to read this version (D-RCV-60)

This is the v3 build notes realigned to the 19-service target. Every story keeps its key, its title, its steps, its IDs, its numbers and its dates; release dates read "(tentative)". Each story now opens with the services that own its work, and a realignment note names the primary service, its epic, its schema, login, REST base, topic, task queue and Java package, its new stories and its lanes. Where a mechanism of the monolith no longer exists in the target, the step text says what replaces it, and a gap row and an assumption row record the difference (Template and Rules §R9). Where no source carries a value, the text carries the placeholder of §R9.

The steps remain the specification of behaviour. Service names, endpoints, package names, job mechanisms, event names and table ownership are the realignment, and they are listed in this section once so a reader does not have to infer them story by story.

### The 19 services

| Code | Service | Name | Wave | Schema and login | REST base | Topic | Task queue |
|---|---|---|---|---|---|---|---|
""" + SVCROWS + """

Platform epics are RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE and RWB-PLT-OBS in wave 0; integration epics are RWB-ITG-W1 to RWB-ITG-W4 and RWB-ITG-NFR. The shared decision topic is rwb.decision-record.v1 and the Temporal namespace is rwb-recovery. A path written without a base in a story, such as `GET /cases/{caseId}`, belongs to the base of the service that owns it in that story.

### Legacy service identities

| Identity | What it named in the monolith | What runs the step now |
|---|---|---|
| SY-DATALOAD | the batch data load | the workload identity of the service that runs the step: rwb-source-data for a load, ingest or reconciliation step, rwb-integration for the hand-over, plan-status and booking steps, rwb-payment for matching |
| SY-CASEWF | case and workflow | rwb-case, and rwb-decision where the step writes a decision record or evaluates a rule |
| SY-RULES | the rules component | the embedded Drools kit of the acting service, reading the rule rows of rwb-decision (DP-04) |
| SY-AGENT | the agent runtime | rwb-agent |

The mapping is fixed once here rather than repeated in 42 stories, and it is recorded as ASM-C-BN2-1.

### Mechanisms replaced

| Monolith mechanism | Target mechanism | Rule and record |
|---|---|---|
| Quartz and Control-M triggers | a Temporal Schedule or an event-started workflow through the workflow kit; the JOB-nn IDs stay as catalogue keys | DP-10; CG-C-BN2-10, ASM-C-BN2-3 |
| the JOB-05 five-minute timer check and TimerDue (EV-18) | durable timers inside CaseWorkflow, TreatmentWorkflow and ApprovalWorkflow; JOB-05 and EV-18 retired | DP-10; CG-C-BN2-3, ASM-C-BN2-9 |
| the JOB-01 ingest and the JOB-09 result load | retired; ACE ingestion is read through the rwb-source-data view contract and AceDataReady (EV-26) is published by rwb-source-data | DP-05; CG-C-BN2-2, CG-C-BN2-9, ASM-C-BN2-9 |
| LoadCompleted (EV-26) | AceDataReady (EV-26) on rwb.source-data.events.v1 | CG-C-BN2-1, ASM-C-BN2-2 |
| the data lake, INT-19 and INT-20 | removed; rwb-reporting publishes events and the read model the data set reads | DP-17; CG-C-BN2-4, ASM-C-BN2-4 |
| DecisionLogWriter and the shared decision log table | the decision-record library in every service, the shared topic rwb.decision-record.v1 and the central ledger in rwb-decision | DP-03 |
| RuleEvaluator and the local payment_match_rule table | the embedded Drools kit and the PAYMENT_MATCH rule package in rwb-decision; no match-rule table in any schema | DP-04; CG-C-BN2-5, CG-C-BN2-6, ASM-C-BN2-5, ASM-C-BN2-6 |
| an in-process call on a published interface | one REST hop on the owner's contract, 2 s timeout, built against the published contract and its fake | DP-11 |
| `/api/recovery/v1` | `/api/recovery/<short>/v1` | DP-13 |
| a screen served by the monolith | a gateway-bff composite route | DP-19 |
| `recovery.<table>` and the single recovery schema | the owner's `rwb_<name>` schema, never a read of another service's tables | DP-01, DP-02, DP-15 |

Feature flag keys, parameters, message IDs, story IDs, step numbers and the JOB-nn identifiers are kept exactly as the source writes them, because they are keys other documents and the tracker use; ASM-C-BN2-11 records that ruling.

### Lanes and Day 1

Every contract story is Day 1: the Epic 2 contract group is CG-W2, and the four platform stories RWB-E2-037 to RWB-E2-040 sit in CG-W0. Each service's build lanes are named per story from the Service Story Catalog v1, and a build lane starts after its own service's contract story. The wave is 2 for every story of this epic except where the Service Story Catalog v1 carries a later release for the agent stories RWB-E2-028 to RWB-E2-030.

"""

TAIL_ROWS = []
for k, b in stories:
    title = re.match(r'## ' + k + r' (.+)', '## ' + k + ' ' + b).group(1).split('\n')[0]
    row = plan.get(k)
    cat = CAT.get(k, [])
    lanes = sorted({c['lane'] for c in cat if c['lane']})
    lanes = [l for l in lanes if l.startswith('CG-')] + [l for l in lanes if not l.startswith('CG-')]
    prim = service_name(row['primary']) if row else 'P2 Integration (source module line)'
    slices = ', '.join(row['slices']) if row else 'Not specified in the source documents (CG-C-BN2-11; ASM-C-BN2-12)'
    wave = cat[0]['wave'] if cat else 2
    be = cat[0]['be'] if cat else 'EP02'
    rel = cat[0]['rel'] if cat else '31 December 2026 (tentative)'
    TAIL_ROWS.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
        k, title, prim, slices, ', '.join(lanes) if lanes else 'Not specified (CG-C-BN2-11)',
        wave, be, rel))

TAIL = """
## Sources of this version

| Source | What it supplied |
|---|---|
| 04 User stories/Recovery Workbench Build Notes Epic 2 v3.md | every story, step, ID, number and date of this document |
| 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx, Stories sheet | the lanes, wave, business epic, release and story IDs per legacy key |
| 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx, Services, Tables, Events, Workflows and activities, Jobs sheets | the service, schema, login, REST base, topic and task queue; the table, event and job owner |
| _work/msr/plan/split_plan.json, blocks legacy and stats | the primary service, the patterns and the new stories of each legacy key |
| _work/msr/plan/ids.json | the decision, ADR and decision log identifiers of this run |
| 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md, sections R1, R3, R5, R8 and R9 | the rules applied: DP table, wave map, lanes, dependency classes, header, placeholder |
| 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md | the service boundaries, the event catalogue and the job map |
| 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md | the durable timer, workflow and rule package behaviour |

## Realignment map by service and lane

| Legacy key | Title | Primary service | New stories | Lanes | Wave | Business epic | Release |
|---|---|---|---|---|---|---|---|
""" + '\n'.join(TAIL_ROWS) + """

## Gaps and assumptions of this version

The rows below sit in `_work/msr/gaps/C-BN2.jsonl` and `_work/msr/assumptions/C-BN2.jsonl` and are numbered in step D1. Each is cited where it applies.

| ID | Title or text |
|---|---|
| CG-C-BN2-1 | LoadCompleted (EV-26) in the source against AceDataReady (EV-26) in the Arch v5 catalogue |
| CG-C-BN2-2 | JOB-01 is retired, yet three Epic 2 stories are keyed on it |
| CG-C-BN2-3 | JOB-05 and TimerDue (EV-18) are retired, yet three Epic 2 stories are keyed on them |
| CG-C-BN2-4 | RWB-E2-009 writes the INT-19 extract for a data lake that the target removes |
| CG-C-BN2-5 | RWB-E2-027 loads a payment_match_rule table that RWB-E2-042 forbids |
| CG-C-BN2-6 | The payment match priority order differs between RWB-E2-027 and RWB-E2-042 |
| CG-C-BN2-7 | The partner_user table is created by P4 in the story and owned by S9 in the map |
| CG-C-BN2-8 | The signature_request table is created by P6 in the story and owned by P5 in the map |
| CG-C-BN2-9 | JOB-09 is retired, yet RWB-E2-021 loads the INT-15 file with it |
| CG-C-BN2-10 | Quartz triggers appear in RWB-E2-037 and RWB-E2-039 after Quartz is retired |
| CG-C-BN2-11 | RWB-E2-023 has no row in the plan, so it has no service, lane or new stories |
| CG-C-BN2-12 | RWB-E2-020 is absent from the story set and the numbering skips it |
| CG-C-BN2-13 | RWB-E2-033 to RWB-E2-036 sit in the P2 backlog while the code and tables are in rwb-case |
| CG-C-BN2-14 | The payment match rule load is a P4 reference load in the story and a P7 rule package in the target |
| ASM-C-BN2-1 | The four legacy service identities map to the workload identity of the acting service |
| ASM-C-BN2-2 | EV-26 is read as AceDataReady, the Arch v5 catalogue name |
| ASM-C-BN2-3 | JOB-nn identifiers are kept and their mechanism is read as Temporal Schedule or event-started workflow |
| ASM-C-BN2-4 | The INT-19 extract is replaced by published measure rows and events |
| ASM-C-BN2-5 | Payment match rules are rows of the PAYMENT_MATCH package |
| ASM-C-BN2-6 | The PAYMENT_MATCH priority order is EXACT, then PARTIAL, then WINDOW |
| ASM-C-BN2-7 | The partner user binding is a S9 record and rwb-access keeps identity, role and scope |
| ASM-C-BN2-8 | The signature request is a P5 record and rwb-comms orchestrates it |
| ASM-C-BN2-9 | JOB-05, JOB-01 and JOB-09 are retired and their work is read from durable timers and the view contract |
| ASM-C-BN2-10 | The next-action check runs as a Temporal Schedule in rwb-case |
| ASM-C-BN2-11 | Configuration keys, message IDs, story IDs and JOB-nn identifiers keep their as-built names |
| ASM-C-BN2-12 | The primary service of a story is the plan's primary, and RWB-E2-023 falls back to its module line |
| ASM-C-BN2-13 | EV-19 TimerBreached is raised by the approval durable timer and stays owned by rwb-case |
| ASM-C-BN2-14 | The story set of this document is the 42 stories of v3, which is one more than the plan's 41 keys |
"""

out = HEAD + '\n' + pre + '\n' + MID + new_stories + '\n\n' + TAIL
OUT.write_text(out, encoding='utf-8')

# ---------------------------------------------------------------- assertions
assert out.count('## RWB-E2-') == 42
src_steps = original.count('### Step ')
out_steps = out.count('### Step ')
assert src_steps == out_steps, (src_steps, out_steps)
for k in NOTES:
    assert ('## %s ' % k) in out, k
out_lines = set(out.splitlines())
dropped = [l for l in t.splitlines() if l.strip() and l not in out_lines]
unexpected = [l for l in dropped if not l.startswith('Module: ')
              and 'SCB Collections and Recovery. Henka Group, 16 November 2026.' not in l]
assert not unexpected, 'lines lost: %s' % unexpected[:10]
print('module lines rewritten:', len([l for l in dropped if l.startswith('Module: ')]))
print('written', OUT, len(out), 'bytes; steps', out_steps)
print('stories', len(stories))
