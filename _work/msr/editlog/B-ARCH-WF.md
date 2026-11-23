# Edit log — WP B-ARCH-WF (Batch and Scheduling Design v-next and Temporal Workflow and Activity Catalog v1)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

## Files written

- 05 Technical architecture/Recovery Workbench Batch and Scheduling Design v5.xlsx

- 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx

- _work/msr/gaps/B-ARCH-WF.jsonl

- _work/msr/assumptions/B-ARCH-WF.jsonl

- _work/msr/editlog/B-ARCH-WF.md

Scratch files under `_work/msr/docs/B-ARCH-WF/` (build and verification only, not outputs of the run):

- _work/msr/docs/B-ARCH-WF/registers.py

- _work/msr/docs/B-ARCH-WF/build_batch.py

- _work/msr/docs/B-ARCH-WF/build_catalog.py

- _work/msr/docs/B-ARCH-WF/jobs.json

- _work/msr/docs/B-ARCH-WF/workflows.json

## 1. Batch and Scheduling Design v5

The source `05 Technical architecture/Recovery Workbench Batch and Scheduling Design v4.xlsx` was never opened for
writing. It was copied to v5 with `compat/office_write.py copy`, and only the copy was changed: a Read me sheet was
added first, the realignment was added as new columns and new sheets, and no source cell was deleted or reordered.

**Header and change log.** Read me rows 1 and 2 are the header of Template and Rules §R8.1. Row 8 is the change-log
row `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Row 9 keeps
the v4 line `v4, 16 November 2026, D-RCV-36` for the version chain.

**Fidelity to v4.** The v4 Jobs sheet has 208 cells and the v4 Daily timeline has 24. After the build, exactly four
source cells differ, and each one is deliberate:

| Cell | v4 | v5 |
|---|---|---|
| Jobs A2 | 20 jobs "run on Quartz and Spring Batch … ACE's existing qrtz_* and batch_* tables" | the same 22 jobs, JOB-01 and JOB-09 retired under D-RCV-35, the other 20 in the owning service as a Temporal Schedule or an event-started workflow, no Quartz and no qrtz_*/batch_* tables; columns A to H declared as the v4 text |
| Jobs A3 | Version 4, 16 November 2026. D-RCV-36. | Version 5, 22 November 2026. D-RCV-60. Previous: Version 4, 16 November 2026. D-RCV-36. |
| Jobs G4 | Owner | Owner (v4 role) |
| Jobs H4 | TimerScheduler | TimerScheduler (v4) |

Every other v4 cell — all 22 job rows A to H, every time, dependency, failure rule, owner role and TimerScheduler
value — is unchanged, verified cell by cell against the source. The v4 Daily timeline is unchanged; the v5 block is
appended below it.

**Realignment added to the Jobs sheet (columns I to N).** One owner service per job from the Ownership Map v1 and
`_work/msr/plan/ownership.json`, the v5 mechanism, the workflow or Schedule, the task queue, a note and the source:

- 10 Temporal Schedules: JOB-06, JOB-10, JOB-14, JOB-16, JOB-17, JOB-18, JOB-19, JOB-20, JOB-21, JOB-22.
- 6 event-started: JOB-02 (DailyCaseRun), JOB-03 (a DailyCaseRun step), JOB-04 (AceIngestCheck and reconciliation),
  JOB-07 and JOB-08 (the payment run with matchPayments and confirmBookings, workflow name not in any source),
  JOB-12 (DocumentIntakeWorkflow).
- 1 Airflow trigger: JOB-15.
- 3 with neither a Schedule nor a workflow: JOB-05 (durable timers), JOB-11 (outbox relay), JOB-13 (continuous ingest).
- 2 retired: JOB-01 and JOB-09.

**New sheets.** `Daily timeline` keeps the v4 table and gains a v5 block (time, jobs, mechanism) that states that
JOB-13 is continuous, JOB-15 runs at 01:30 from Airflow and JOB-14 at 02:00 from its Schedule. `Schedule and event map`
gives 22 rows: job, owner service, mechanism, Schedule or workflow, Schedule ID, task queue, trigger, overlap policy
and source.

**Dates.** No release date is stated anywhere in this document. The v4 version date 16 November 2026 is carried
unchanged and unmarked because it is a version date, not a release date; nothing is raised as a date gap.

**Document properties.** The v4 property block named an individual as creator and last-modified-by. The v5 copy
carries "SCB Collections and Recovery" for both, because root rule 4 forbids names of people in any output.

## 2. Temporal Workflow and Activity Catalog v1

New document, no source file to copy. Seven sheets, all built from the text extracts named in the WP:

1. **Read me** — header §R8.1, the change-log row, what the catalog is, counts, how to read a row, status, sources and
   precedence, the gaps and assumptions cited, related documents.
2. **Workflows** — 20 rows: 11 domain workflows, 2 rwb-source-data workflows, 4 kit templates, the platform smoke
   workflow and 2 placeholder rows for the event-started payment workflows of JOB-07 and JOB-08. Columns: kind, owner,
   service, task queue, started by, steps, hands back, activities, history and limits, source.
3. **Activities** — 19 rows: EvaluateRules and RecordAndApply as universal activities, 15 named service activities,
   the OCR/classify/extract steps, and the restructure calculator as a Nexus operation. Retry policy per row; timeout
   and heartbeat as the §R9 placeholder.
4. **Schedules** — the 10 Schedules with job, source name, owner, queue, trigger, what it starts, overlap and catch-up,
   note and source. Where the source does not name what a Schedule starts, the cell carries the §R9 placeholder.
5. **Task queues and namespaces** — 25 rows: the rwb-recovery namespace, the cluster, the 19 service queues,
   rwb-platform, the ace-collection namespace reached through Nexus, the codec server and the Temporal UI roles.
6. **Platform rules** — 20 rules that apply to every workflow and activity (determinism, retry, timeouts, Continue-As-New,
   parent close policy, search attributes, codec, retention, versioning, strict mode, agent fallback, Kafka, Schedule
   overlap, KEDA, Temporal 1.30+, no Quartz, no case of record, workflow ID).
7. **Open points** — the six open points of Temporal design slide 32, with the suggested owner role (a role, never a
   person) and where each one bites.

Both sheets of the v4 source that carry a mechanism (Jobs, Daily timeline) are reflected one for one in the catalog's
Schedules and Platform rules, so a story can take §12.5, §12.6 and §12.9 from one place.

## 3. Registers

- Gap rows written: **7** candidate rows, `GAP-0142` to `GAP-0148`, in `_work/msr/gaps/B-ARCH-WF.jsonl`
  (5 Missing, 1 Ambiguous, 1 Conflict; 5 of severity P2 and 2 of P3).
- Assumption rows written: **13** candidate rows, `ASM-0220` to `ASM-0232`, in
  `_work/msr/assumptions/B-ARCH-WF.jsonl` (10 High, 3 Medium).
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.
- The job-ownership conflicts that WP A6 already raised are cited, not duplicated: GAP-0042 to GAP-0046 with
  ASM-0060, 8, 10, 11 and 12. The seven new rows are the ones this WP adds: Schedule identifiers and calendars,
  activity timeouts, the unnamed payment workflow, the work started by six Schedules and three workflows, DailyCaseRun
  as Schedule and event, the rwb-platform queue and the case workflow ID.

No value is invented. Every missing value in either document carries the §R9 placeholder with its CG and ASM citation,
and every placeholder cites a row that exists in one of the two registers.

## 4. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ARCH-WF --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

Report: `22 Microservice Realignment/checks/reports/wp-B-ARCH-WF-20261122-210031.md` (written by the check script).
C12 finds no person name and no email in the files of this WP; C13 finds no issue-tracker reference; C18 finds no write
outside the "Write only" list and no change to a story master.

## 5. Status

Both documents are issued in **Draft**: no approval is recorded for this run (ASM-0220). No later lifecycle
stage was started.
