# RWB-PLT-E1056-OPS Run books and monitoring for every Epic 1 Workbench job

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Backfilled 10 mapped v9 test case IDs.
- P1 job view and rerun limited to rwb-source-data runs, published by RWB-P1-AD018-CON: one item per run, rerun by run ID with 202, MSG-P1-011 and MSG-P1-001 (RD-P1-012; findings #1, #2, #4, #8; AC3, AC5, AC13, AC14).
- AceDataReady and AceDataLate key, fields and timing; daily work starts only on ALS COMPLETED; JOB-04 is a child of AceIngestCheck (RD-P1-003, RD-P1-040; #5, #6; AC6, AC12).
- `case_list_row` removed (RD-P1-024; #7). No ACE view read outside rwb-source-data (#3).
- Left pending: other services' job reads (GAP-3271), the per-source batch date feed (GAP-3318, #3, #9), catalogue rows for the AceIngestCheck work (GAP-3319, #10).
- The header no longer names an app story as an integration dependency; the wave 4 job view and rerun are an external dependency on the published contract (W9-governance-0175).

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1056-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-OBS |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-056 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-PLT-E1056-OPS-16) |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | L-PLT-OBS-B |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-AD018-CON (job view and rerun), RWB-P1-E1015-CON (freshness read, AceDataReady, AceDataLate) |
| Contract version | rwb-source-data.yaml 5.1.0 and rwb-source-data.asyncapi.yaml 5.1.0 (API Specification v7); provider fake 5.1.0 under `fakes/rwb-source-data/5.1.0/` |
| Integration dependencies | None |
| External dependencies | The released rwb-source-data job view and rerun of RWB-P1-AD018-CON (wave 4) for AC5, AC8 and AC13 and for the P1 part of AC3 |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-024, RD-P1-040, RD-P1-041, RD-P1-066 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-056 for the platform observability epic; the 16 job rows, the eight run book sections, the message IDs and the guards are kept. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-PLT-E1056-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 30 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the platform to hold one run book for every Epic 1 Workbench job, a pipeline gate that proves the run books and the catalogue rows exist, one monitoring workbook that shows each job's last run, status and duration beside the last complete ACE business date per source, and alert and rerun guards that route to the owning role**, so that **the operations team can restart any Epic 1 job without the developer and can tell a late ACE batch from a failed Workbench job**.

### 2. Business rationale

The Workbench loads no source data (D-RCV-35 U1; ADR-010). Its scheduled work is the case list chain, the daily rebalancing, payment matching and booking confirmation, the WIN notice file, the outbox relay, document intake, the decision-record ingest and its hash-chain check, the reporting extract, retention, the agent runtime and the view conformance test. A failed job that only its developer can restart holds the case list and the morning allocation; a late ACE batch looks exactly like a failed Workbench job unless the monitor shows the ACE business date beside it.

In the target the 16 Epic 1 jobs no longer run in one scheduler: each runs as a Temporal Schedule or as an event-started workflow in the service that owns it (DP-10, Arch v5 slide 44), and JOB-05 and JOB-11 have no Schedule of their own, because timers live inside each workflow and the outbox relay runs in every service, while JOB-13 is continuous Kafka ingest. The catalogue row, the run book gate and the workbook therefore become the one platform place that spans the 16 jobs: they name the owning service and the mechanism, hold the owner role and the threshold, and prove in the pipeline that neither the row nor the run book is missing. No inbound load job is catalogued: ACE ingests every source, ACE monitors its own ingestion, and the Workbench watches only the business date it receives. This meets REQ-DRI-007 (a named owner for every failure), NFR-067 and NFR-068.

### 3. Preconditions

- The owning service workflows exist: DailyCaseRun and its steps in rwb-case, the reconciliation workflow in rwb-source-data, the matching and booking workflows in rwb-payment, the notice, document, decision and reporting work (RWB-PLT-WF and RWB-PLT-E1071-CON, DP-10).
- The Kafka platform and the outbox relay are in force, so JOB-11 and the event-started jobs have a transport (RWB-PLT-EVT, RWB-PLT-TE006-CON, DP-09).
- The per-service Flyway sequence is in force, so no migration of this story writes into an owning service's schema (RWB-PLT-E1044-CON, DP-15).
- The parameters and reference-data contracts are in force, so the owner role of a job is a reference-data value and not a literal (DP-06, DP-07).
- RWB-P1-E1015 is done: `v_ace_batch_status`, the stale marker on `data_product_load` and EV-27 `rwb.source-data.AceDataLate.v1` exist in rwb-source-data.
- The P1 job view and rerun are published by RWB-P1-AD018-CON and serve rwb-source-data runs only (`AceIngestCheck`, `ReconciliationWorkflow` as JOB-04, `Stage2ProductWorkflow`, `RetentionRunWorkflow`; RD-P1-012). Until RWB-P1-AD018 is released (wave 4) there is no P1 rerun: a failed or late P1 run is restarted by a repeated readiness call or the fallback poll (ASM-5710).
- Pending: the job read and rerun operations of the services that own the other jobs, owner solution architect, tracked as GAP-3271.
- Only rwb-source-data reads `recovery.v_ace_*` (D-RCV-60); this story and the jobs of other services use the rwb-source-data contract. Pending: the feed of the last complete ACE business date per source to the platform workbook, owner solution architect with the platform observability owner, tracked as GAP-3318.
- Pending: whether `AceIngestCheck`, its 05:30 Schedule `rwb-source-data-ace-late-check` and `Stage2ProductWorkflow` get a `job_catalog` row and run book, owner solution architect with the rwb-integration service owner, tracked as GAP-3319.
- `job_catalog` is owned by P2 rwb-integration and its admin operation exists, so the 16 Epic 1 rows are loaded as data (ownership map; DP-01).
- The Log Analytics workspace and the OpenTelemetry baseline receive the application logs, the spans and the job-run records (RWB-PLT-N005-OPS).
- The person holds RW-PLATADM through RWB-<env>-RW-PLATADM.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The platform administrator confirms one `job_catalog` row per job with job ID, name, owner role, schedule, run book path, expected duration and alert threshold. The 16 Epic 1 rows are JOB-02, JOB-03, JOB-04, JOB-05, JOB-06, JOB-07, JOB-08, JOB-10, JOB-11, JOB-12, JOB-13, JOB-14, JOB-15, JOB-17, AGT-01 and CHK-01; they are loaded as data through the P2 rwb-integration admin operation, not by code.
2. A squad member (RW-TRIBE) writes the run book at `docs/operations/runbooks/<job ID>.md` with the eight sections: purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation.
3. The squad member names in Dependencies the ACE data the job reads, through the rwb-source-data contract (a `recovery.v_ace_*` view name only in the run book of a rwb-source-data job), and the upstream Workbench job; names the STALE freshness stamp and EV-27 `rwb.source-data.AceDataLate.v1` in Failure signs when the job reads ACE data; and the CHK-01 run book names the view conformance test with the dictionary load through RWB-E1-043 in Checks and Restart steps.
4. The pipeline runs `RunbookCompletenessTest`: it checks every Temporal Schedule and every event-started job of the owning services and every catalogue row, checks the eight headings, and fails on the forbidden names (an inbound load job, a file arrival, a load rerun, a data quality exception console, a table in schema `public`).
5. Each job writes a structured job-run record at start and end with job ID, business date, status and duration: OpenTelemetry span attributes on the workflow or activity span, plus, for a job that runs inside rwb-source-data, its `job_run` row (`job_run_check` for the JOB-04 checks).
6. The platform administrator opens the workbook "Recovery jobs" and sees last run, status and duration per job from the job-run records, and the last complete ACE business date per source (feed Pending, GAP-3318). For rwb-source-data runs the P1 job view `GET /api/recovery/source-data/v1/admin/jobs` answers one item per run.
7. An alert rule emails the owner role and RW-PLATADM with MSG-P2-004 when a job is FAILED or runs past its threshold.
8. When an ACE batch is late or failed, `AceIngestCheck` in rwb-source-data publishes EV-27 (at 05:30 Asia/Bangkok for a source with no COMPLETED row, at once for a FAILED row) and the product's freshness stamp turns STALE (at once on a FAILED source, otherwise at its `expected_by`); the dependent job waits and the run book says to wait for the batch and not to rerun the job.
9. The platform administrator follows the restart steps in the run book. For a FAILED rwb-source-data run the step is `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` with the run ID, no body and an `Idempotency-Key` (UUID), answered 202; before RWB-P1-AD018 is released the step is a repeated readiness call for the business date (ASM-5710). For a job of another service the step is the owner's operation (GAP-3271).
10. The rerun starts a new run of the workflow (`runNo` + 1) for the business date and type of the failed run; daily work of other services starts again only on AceDataReady with `sourceSystem` ALS and `status` COMPLETED.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A job has a Temporal Schedule registration or an event trigger but no catalogue row, or a catalogue row with no run book, or a run book lacks a section | The pipeline fails and names the job and the missing section | MSG-P2-005 | AC1 |
| X2 | A run book names an inbound load job, a file arrival, a load rerun, a data quality exception console or a table in schema `public` | The pipeline fails and names the run book and the forbidden line | Build log: JOB-02.md names public.account; a run book may name only the Workbench jobs and the data its service may read | AC1, AC7 |
| X3 | A rwb-source-data rerun is requested while a run of the same type and business date is PENDING or RUNNING | Refused with 409; the running run continues | MSG-P1-011 | AC5 |
| X4 | A job runs past its alert threshold | The owner role and RW-PLATADM are alerted; the job is not stopped | MSG-P2-004 | AC4 |
| X5 | A rwb-source-data rerun is requested for a run that is not FAILED, for example a completed one | Refused with 409; no run is started and no business row changes | MSG-P1-011 | AC5 |
| X6 | An ACE batch is late or failed | The product stamp turns STALE, EV-27 is published, the dependent job waits and is not rerun | MSG-P1-001 | AC6 |
| X7 | The view conformance test CHK-01 fails | The merge is blocked; the CHK-01 run book gives the dictionary load through RWB-E1-043 as the fix | v_ace_account.legacy_bucket has no data dictionary entry | AC1, AC7 |
| X8 | A role without the right reruns a job | Refused; nothing changes | MSG-P4-002 | AC8 |
| X9 | A rwb-source-data rerun is requested while the ACE batch of the business date is not COMPLETED | Refused with 409; no run is started | MSG-P1-001 | AC13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the owning services' Schedules and event triggers (RWB-PLT-WF, RWB-PLT-E1071-CON), the batch view and stale marker of RWB-P1-E1015 and the telemetry baseline of RWB-PLT-N005-OPS; each job's own story supplies the job body |
| Negotiable | Owners, thresholds and paths are catalogue rows; the story fixes the eight run book sections and the gate |
| Valuable | Any Epic 1 job can be restarted by operations on the day it fails, and a late ACE batch is not mistaken for a Workbench failure |
| Estimable | 16 run books, one pipeline gate, one workbook, three alert rules, one business-date panel, the guard definitions and one catalogue baseline |
| Small | Within one week with its tests |
| Testable | Each criterion is one automated test, one pipeline check or one workbook query |

### 7. Acceptance criteria

```gherkin
Feature: Run books and monitoring for every Epic 1 Workbench job

  Background:
    Given job_catalog holds 16 rows with first release "E1": JOB-02, JOB-03, JOB-04, JOB-05, JOB-06, JOB-07, JOB-08, JOB-10, JOB-11, JOB-12, JOB-13, JOB-14, JOB-15, JOB-17, AGT-01 and CHK-01
    Given the daily chain is JOB-02, then JOB-03, JOB-04, JOB-07 and JOB-08, with JOB-05 carried by durable timers inside each workflow and JOB-13 continuous on Kafka

  Scenario: AC1 The run book set and the pipeline gate exist for every Epic 1 job (new, D-RCV-60)
    Given the 16 rows in job_catalog
    When RunbookCompletenessTest runs in the pipeline
    Then each of the 16 jobs has a file at docs/operations/runbooks/<job ID>.md named by its catalogue row's run book path
    Then each file has the sections purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation
    Then the gate checks every Temporal Schedule and every event-started job of the owning services as well as every catalogue row
    Then a Schedule or an event trigger with no catalogue row, and a catalogue row with no run book or a run book without a section, fail the gate with MSG-P2-005 naming the job and the missing section
    Then the run book for CHK-01 names the view conformance check and the dictionary load through RWB-E1-043 in Checks and Restart steps
    Then no file names an inbound load job, a file arrival, a load rerun, a data quality exception console or a table in schema public, and only the run book of a rwb-source-data job names a recovery.v_ace_ view

  Scenario: AC2 The 16-row Epic 1 catalogue baseline is loaded as data through the P2 admin operation and never as code (new, D-RCV-60)
    Given the Epic 1 catalogue baseline of 16 rows
    When the baseline is applied through the admin operation of rwb-integration
    Then each row carries the job ID, the job name, the owner role, the schedule, the run book path, the expected duration and the alert threshold
    Then applying the same baseline a second time changes nothing, because the load is idempotent by job ID
    Then no migration of this story inserts a catalogue row into a schema, and no job ID, owner role, schedule, path or threshold is hard-coded in a class, a test or a dashboard
    Then GET /api/recovery/integration/v1/admin/scheduled-jobs returns 16 entries

  Scenario: AC3 The workbook shows every job and agrees with the P1 job view on the rwb-source-data runs (new, D-RCV-60)
    Given every job in job_catalog ran at least once in SIT
    When the platform administrator opens the workbook "Recovery jobs"
    Then each of the 16 jobs shows its last run time, status and duration from its job-run records
    Then the workbook shows the last complete ACE business date per source beside the jobs, and reads no recovery.v_ace_ view
    Given JOB-04 ran twice for business date 2026-12-01, the first run FAILED and the second COMPLETE
    When GET /api/recovery/source-data/v1/admin/jobs?type=JOB-04 is read
    Then it returns one item per run ordered startedAt descending, with id, type JOB-04, runNo 2 then 1, businessDate, status, startedAt and endedAt
    Then the workbook's last run of JOB-04 has the same status, startedAt and endedAt as the first item

  Scenario: AC4 The alert rules fire for a failed job, a run past threshold and a held run, with MSG-P2-004 and MSG-P1-001 and the 15-minute target (new, D-RCV-60)
    Given JOB-02 has an alert threshold of 45 minutes (assumed; DL11)
    When JOB-02 fails at 05:40 on business date 2026-11-30
    Then the data steward group and the platform administrator group receive message MSG-P2-004 with the job, the time, the date and the run book path
    When JOB-02 has run for 46 minutes on business date 2026-12-01
    Then the data steward group and the platform administrator group receive message MSG-P2-004 and the system does not stop JOB-02
    When a job is held for a late ACE batch
    Then the held run raises MSG-P1-001 and the alert reaches the named owner role within the 15-minute target of NFR-068

  Scenario: AC5 A rerun is refused unless the run is FAILED and no run is open (new, D-RCV-60)
    Given the JOB-04 run of business date 2026-12-01 started at 06:40 and is RUNNING
    When a platform administrator calls POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun with that run ID and an Idempotency-Key at 06:45
    Then the response is 409 with messageCode MSG-P1-011
    Then the running run continues and no job_run row is added
    Given the JOB-04 run of business date 2026-12-01 is COMPLETE
    When a platform administrator reruns that run ID
    Then the response is 409 with messageCode MSG-P1-011
    Then reconciliation_result still holds one row per product group for 2026-12-01 and job_run holds no new row

  Scenario: AC6 A failed ALS batch turns the stamp STALE, publishes EV-27 and holds the daily work (new, D-RCV-60)
    Given the ALS batch of business date 2026-12-01 reads FAILED at 05:20
    When the AceIngestCheck run of 2026-12-01 reads the batch status
    Then the DP01 stamp in use is STALE at once with stale_flagged_at set
    Then rwb.source-data.AceDataLate.v1 is published once with record key "ALS:2026-12-01" and data sourceSystem ALS, businessDate 2026-12-01, status FAILED and completedAt
    Then no rwb.source-data.AceDataReady.v1 for ALS exists, so JOB-02, JOB-07 and JOB-08 do not start, and no JOB-04 run is started
    Then the held-run alert reaches the owner role with MSG-P1-001 and the run book says to wait for the ALS batch and not to rerun
    When the ALS batch reads COMPLETED at 08:40
    Then AceDataReady with sourceSystem ALS and status COMPLETED is published once, JOB-02, JOB-07 and JOB-08 start for 2026-12-01 and ReconciliationWorkflow recon-2026-12-01 starts as a child of AceIngestCheck

  Scenario: AC7 Every run book of a job that reads ACE data names that data, the STALE freshness stamp and EV-27, and no run book names a forbidden source (new, D-RCV-60)
    Given the run books of the jobs that the catalogue records as reading ACE
    When each of those run books is reviewed against the gate
    Then each names the rwb-source-data data it reads in Dependencies (v_ace_batch_status only in a rwb-source-data job's run book), and the STALE freshness stamp and EV-27 AceDataLate in Failure signs
    Then each of the 16 run books names a role and a service identity and never a person
    Then no run book names an inbound load, a file arrival, a load rerun, a data quality exception console or a table in schema public

  Scenario: AC8 Only a role with the rerun right may rerun; a role without it is refused with MSG-P4-002 and nothing changes (new, D-RCV-60)
    Given RW-CASEOWN holds no rerun right
    When RW-CASEOWN calls the P1 rerun operation with the run ID of a FAILED JOB-04 run and an Idempotency-Key
    Then the response is 403 with message MSG-P4-002
    Then nothing changes: job_run holds no new row and the catalogue holds the same values as before the call
    Then only RW-PLATADM, which holds Platform administration U, can rerun a job
  Scenario: AC9 The view conformance test has a run book (legacy RWB-E1-056 AC9)
    Given a branch adds column "legacy_bucket" to the rwb-source-data contract view of recovery.v_ace_account with no sys_fields row (DP-01, DP-05)
    When the pipeline runs CHK-01
    Then CHK-01 fails with "v_ace_account.legacy_bucket has no data dictionary entry"
    Then the merge is blocked
    Then the run book for CHK-01 gives the fix: load the dictionary row through RWB-E1-043 and rerun CHK-01

  Scenario: AC10 Owners, thresholds and paths are written only as job_catalog data through the P2 admin operation (new, D-RCV-60)
    Given the job_catalog rows and the source of the Epic 1 jobs
    When the rules of BR8 are checked
    Then no owner role, threshold or path is hard-coded in a class, a test or a dashboard
    Then job_catalog is written only through the admin operation of rwb-integration

  Scenario: AC11 A consumed call that fails or does not answer stops the run and is not recorded as complete (new, D-RCV-60)
    Given JOB-02 reads the rwb-source-data contract for business date 2026-12-01 (DP-01, DP-05)
    When the call fails or does not answer
    Then the run of JOB-02 is recorded as failed with the job and the call named
    Then the data steward group and the platform administrator group receive message MSG-P2-004 with the job, the time, the date and the run book path
    Then JOB-02 is not recorded as complete and no partial result is written for 2026-12-01

  Scenario: AC12 Daily work starts on the ALS completion only (new, RD-P1-003, RD-P1-040)
    Given rwb.source-data.AceDataReady.v1 for business date 2026-12-01 is published with sourceSystem EFS and status COMPLETED, with record key "EFS:2026-12-01"
    Then no run of JOB-02, JOB-07 or JOB-08 starts for 2026-12-01
    When the event with sourceSystem ALS and status COMPLETED is published
    Then each of them starts once, and a redelivery of the event starts nothing more

  Scenario: AC13 A FAILED rwb-source-data run is rerun by its run ID (new, RD-P1-012)
    Given the JOB-04 run 1 of business date 2026-12-01 is FAILED and the ACE batch is COMPLETED
    When a platform administrator calls the rerun with that run ID, no body and Idempotency-Key "3f0c9a52-7d1e-4c0b-9a1e-2b6f5d8c1a10"
    Then the response is 202 with a Job of status PENDING and runNo 2, and run 1 is unchanged
    Then a replay with the same key returns the stored 202 and starts nothing
    Then a call with no Idempotency-Key answers 400 MSG-PLT-N009-03, an unknown run ID answers 404 MSG-P4-003 and a run whose ACE batch is not COMPLETED answers 409 MSG-P1-001

  Scenario: AC14 Before the job view release a P1 run is restarted by the readiness call (new, RD-P1-012)
    Given RWB-P1-AD018 is not released and the AceIngestCheck run of 2026-12-01 has failed
    When the readiness call POST /api/recovery/source-data/v1/business-days/2026-12-01/ready is repeated
    Then it answers 202 and a new AceIngestCheck run ace-ingest-check-2026-12-01 starts
    Then the run books of the rwb-source-data jobs give this restart step
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every Epic 1 Workbench job, the agent runtime and the view conformance test have a run book, an alert and an owner, held as one `job_catalog` row and one file under `docs/operations/runbooks/`. No inbound load job is catalogued; ACE ingestion is ACE's and is not monitored here | FEAT-DRI-18; D-RCV-35 U1 |
| BR2 | A run book has eight sections: purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation | Story intent |
| BR3 | The owner of each job is the role in `job_catalog`: JOB-02 and JOB-04 data steward; JOB-03 and JOB-06 team managers; JOB-07 and JOB-08 credit administration; JOB-10, JOB-11, JOB-12 and CHK-01 platform administrator; JOB-13 data steward; JOB-14 and JOB-17 compliance; JOB-15 reporting and BI analyst; AGT-01 center of excellence | batch.txt; roles.txt |
| BR4 | JOB-02, JOB-07 and JOB-08 start only on AceDataReady with `sourceSystem` ALS and `status` COMPLETED; JOB-04 is `ReconciliationWorkflow`, a child of `AceIngestCheck` after the ALS stamp (RD-P1-040). Daily jobs restart in the order of the daily timeline: JOB-02, then JOB-03, JOB-04, JOB-07 and JOB-08; JOB-05 is carried by durable timers inside each workflow and has no Schedule of its own; JOB-06 runs at 06:30 as a Temporal Schedule; JOB-13 is continuous Kafka ingest and has no Schedule | batch.txt Daily timeline; Arch v5 slide 44; ownership map jobs |
| BR5 | A rerun of a completed job and business date is refused (rwb-source-data: only a FAILED run is rerun, 409 MSG-P1-011 otherwise); the job body is idempotent for its business date | R-UNI-40; events.txt Rules sheet, Delivery |
| BR6 | Only rwb-source-data reads ACE through `recovery.v_ace_*`; every other service's job reads ACE data through the rwb-source-data contract, and no job loads source data. A run book that names a public table, an inbound load job or a file arrival fails the build | D-RCV-60; D-RCV-35 U1, U4; ADR-010; RWB-TE-001 |
| BR7 | When an ACE batch is late or failed, the product stamp is STALE, EV-27 is published (05:30 cut-off, at once on a FAILED row) and the dependent job waits; the monitor shows the ACE business date beside the job run | RWB-E1-015; BR-P1-014 |
| BR8 | Owners, thresholds and paths are data rows in `job_catalog`, never code, and are written only through the P2 rwb-integration admin operation | Principle 1; DP-01; ownership map |

### 9. State transitions

None. This story does not change a case status. It reads job run status: for rwb-source-data runs PENDING, RUNNING, COMPLETE, FAILED and WAITING (`job_run`, RD-P1-012, RD-P1-020); the status values of the other services' job reads are Pending (GAP-3271). A rerun of a completed job for its business date is refused.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Maintains the catalogue rows through the P2 admin operation; reruns a job (Platform administration, U); owns JOB-10, JOB-11, JOB-12 and CHK-01 |
| RW-DATASTEW, data steward | Reads job runs; owns JOB-02, JOB-04 and JOB-13; receives their alerts (Platform administration, R) |
| RW-TEAMMGR, team manager | Owns JOB-03 and JOB-06; receives their alerts by email; no endpoint right |
| RW-CREDITAD, credit administration | Owns JOB-07 and JOB-08; receives their alerts by email |
| RW-BIANAL, reporting and BI analyst | Owns JOB-15; receives its alerts by email |
| RW-COE, center of excellence analyst | Owns AGT-01; receives its alerts by email |
| RW-COMPLY, compliance | Owns JOB-14 and JOB-17; receives their alerts by email |
| RW-TRIBE, squad member | Writes and maintains the run books and RunbookCompletenessTest; reads job runs (Platform administration, R) |
| RW-AUDIT and RW-SECADM | Read job runs (Platform administration, R) |

The service identity that runs the platform jobs and writes the job-run record is Not specified in the source documents (GAP-1419; ASM-2483).

### 11. Data

| BR Field ID | Entity | Field | Read or write | Owner |
|---|---|---|---|---|
| DF-OPS-224 to DF-OPS-232 | job_catalog | all 9 fields | Read and write through the P2 admin operation | P2 rwb-integration |
| DF-OPS-226 | job_catalog | job_name | Read and write through the P2 admin operation | P2 rwb-integration |
| DF-OPS-227 | job_catalog | owner_role | Read and write through the P2 admin operation | P2 rwb-integration |
| DF-OPS-228 | job_catalog | schedule_text | Read and write through the P2 admin operation | P2 rwb-integration |
| DF-OPS-229 | job_catalog | runbook_path | Read and write through the P2 admin operation | P2 rwb-integration |
| DF-OPS-230 | job_catalog | expected_minutes | Read and write through the P2 admin operation | P2 rwb-integration |
| DF-OPS-231 | job_catalog | alert_after_minutes | Read and write through the P2 admin operation | P2 rwb-integration |
| DF-OPS-232 | job_catalog | first_release | Read and write through the P2 admin operation | P2 rwb-integration |
| DF-ACE-178 | v_ace_batch_status | source_system | Read through the P1 contract only | P1 rwb-source-data |
| DF-ACE-179 | v_ace_batch_status | business_date | Read through the P1 contract only | P1 rwb-source-data |
| DF-ACE-181 | v_ace_batch_status | completed_at | Read through the P1 contract only | P1 rwb-source-data |
| DF-ACE-182 | v_ace_batch_status | status | Read through the P1 contract only | P1 rwb-source-data |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read through the P1 contract only | P1 rwb-source-data |
| DF-OPS-002 | data_product_load | product_code | Read through the P1 contract only | P1 rwb-source-data |
| DF-OPS-004 | data_product_load | business_date | Read through the P1 contract only | P1 rwb-source-data |
| DF-OPS-007 | data_product_load | status | Read through the P1 contract only | P1 rwb-source-data |
| DF-OPS-008 | data_product_load | stale_flagged_at | Read through the P1 contract only | P1 rwb-source-data |
| DF-OPS-233 to DF-OPS-251 | job_run, job_run_check | the run and its checks | Read through the P1 job view only | P1 rwb-source-data |
| DF-OPS-120 | reconciliation_result | business_date | Read through the P1 contract only | P1 rwb-source-data |
| DF-OPS-129 | reconciliation_result | result | Read through the P1 contract only | P1 rwb-source-data |
| DF-REF-035 | role | role_code | Read through the reference-data contract | P4 rwb-access (role as data) |

Field IDs are those in the Logical Data Model and Data Dictionary and in Physical Schema v7. One job-run record is added for each run: its fields are Not specified in the source documents (GAP-1419; ASM-2483); the story fixes that it carries the job ID, the business date, the status, the started and ended time and the duration, and no other business content. The run book path is the catalogue row's `runbook_path`, `docs/operations/runbooks/<job ID>.md`. This story owns no table: `job_catalog` stays with P2 rwb-integration and is written only through its admin operation, and no ACE view is read by this story: the ACE values reach it through the P1 contract only (the per-source batch values are Pending, GAP-3318). No business data and no personal data are held by this story; the job-run record and the run books carry job IDs, dates, statuses, durations and role names only.

### 12. Contract

#### 12.1 REST operations provided

None. This story provides no REST operation. The job view and the rerun of rwb-source-data runs are published by RWB-P1-AD018-CON and stay with P1 rwb-source-data (`GET /api/recovery/source-data/v1/admin/jobs` and `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun`) and the catalogue stays with P2 rwb-integration (`GET /api/recovery/integration/v1/admin/scheduled-jobs`, per the ownership map).

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/admin/jobs` | P1 rwb-source-data (RWB-P1-AD018-CON) | rwb-source-data runs only, `JobPage` with one item per run ordered `startedAt` descending (`id`, `type`, `runNo`, `businessDate`, `status`, `startedAt`, `endedAt`); one hop, 2 s client budget (DP-11) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data (RWB-P1-AD018-CON) | `{jobId}` is the run ID of a FAILED run; no body; `Idempotency-Key` UUID; 202 with the new `Job`; 400 MSG-PLT-N009-03, 404 MSG-P4-003, 409 MSG-P1-011, MSG-P1-001 or MSG-PLT-N009-05, 503 MSG-GEN-006 |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data (RWB-P1-E1015-CON) | The STALE marker beside a waiting job (`productCode`, `businessDate`, `status` LOADED or STALE) |
| GET | `/api/recovery/integration/v1/admin/scheduled-jobs` | P2 rwb-integration | The catalogue baseline load, the gate and the workbook read the 16 rows; the owner role, the schedule, the run book path and the alert threshold come from here |

#### 12.3 Events published

None. The job-run signal is a structured telemetry record (OpenTelemetry span attributes) plus the P1 job run log, not a business event; the v5 event catalogue carries no job-run event, so this story adds no topic and no event name.

#### 12.4 Events consumed

| Event | Topic | Use | Owner |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | Key `{sourceSystem}:{businessDate}`; `sourceSystem`, `businessDate`, `status`, `completedAt`; once per source and date when COMPLETED. The business-date panel (use Pending, GAP-3318: the Kafka catalog does not list a platform consumer of EV-26) | P1 rwb-source-data |
| `rwb.source-data.AceDataLate.v1` (EV-27) | `rwb.source-data.events.v1` | Same key and fields, `completedAt` null when no batch completed; once per source and date at 05:30 or at once on a FAILED row. The held-run alert (consumer `alerts` in the Kafka catalog) | P1 rwb-source-data |

Both topics and both events are owned by P1 rwb-source-data; this story consumes them and republishes nothing.

#### 12.5 Workflows and activities

None owned. The workbook and the gate observe the Schedules and the workflows of the owning services: DailyCaseRun in rwb-case, `AceIngestCheck` and its child `ReconciliationWorkflow` of rwb-source-data, and rwb-payment matching (JOB-07) and rwb-integration booking confirmation (JOB-08) are observed through their owners’ run records and job views; this story starts none of them and claims none of them.

#### 12.6 Schedules

None registered. The Schedules and event triggers observed, with the legacy job references: the JOB-06 rebalancing Schedule in rwb-case, the JOB-14 hash-chain check Schedule in rwb-decision, the JOB-17 retention Schedule in rwb-document, the event-started JOB-02 (case creation), JOB-07 (payment matching) and JOB-08 (booking confirmation, rwb-integration), each on AceDataReady with `sourceSystem` ALS and `status` COMPLETED, and JOB-04 (`ReconciliationWorkflow`, `recon-{businessDate}`), a child of `AceIngestCheck` that waits for rwb-case allocation until `caselist.allocation.wait.until` (07:15). The Schedule `rwb-source-data-ace-late-check` (05:30) of `AceIngestCheck` has no job ID (Pending, GAP-3319). JOB-05 has no Schedule (durable timers inside each workflow), JOB-11 has no Schedule (outbox relay in every service) and JOB-13 has no Schedule (continuous Kafka ingest); each still has a catalogue row and a run book.

#### 12.7 Tables owned

None. `job_catalog` is owned by P2 rwb-integration (ownership map) and this story writes it only through the P2 admin operation; the ACE values are read through the P1 contract only; this story creates no table and runs no migration.

#### 12.8 Contract fakes

| Fake | Use |
|---|---|
| rwb-source-data provider fake 5.1.0 (WireMock, `fakes/rwb-source-data/5.1.0/`) | Runs in the pipeline so the gate and the workbook tests can read a job view without the service, including the 202 rerun, the 409 answers of MSG-P1-011 and MSG-P1-001 and the freshness answer |
| rwb-integration WireMock | Runs in the pipeline so the catalogue baseline load and the gate can read 16 rows without the service |

The fakes are test-only workloads; they are not deployed into SIT, UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The job view, the rerun, the freshness read and the catalogue; one hop, 2 s (DP-11) |
| Kafka | 2 consumed, 0 published | EV-26 AceDataReady and EV-27 AceDataLate; the job-run signal is telemetry, not an event |
| Temporal | 0 owned; the observed Schedules and workflows are named in 12.5 and 12.6 | The story reads run records, it does not start or claim a workflow |
| File | None | The run books are repository content and the catalogue baseline is applied through the admin operation |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The nine rows are the patterns the legacy RWB-E1-056 carries after the split. DP-10 is the substantive one: the 16 jobs are Temporal Schedules or event-started workflows in their owning services, so a catalogue row and a run book name a mechanism the platform does not own and cannot schedule. DP-01, DP-05 and DP-07 keep the story off another service's tables and off schema `public`: the catalogue is written through the P2 admin operation, the ACE batch state is read through the P1 contract, and an owner role is resolved from reference data. DP-03 and DP-09 stay on the story because the job set it monitors includes the outbox relay (JOB-11) and the decision-record jobs (JOB-13 and JOB-14), whose run signals the story reads from the owning services and from the telemetry baseline, never from a topic of its own. DP-11 fixes the three consumed operations to one hop with a 2 s client budget, and DP-15 keeps the migration with the owning service, so this story seeds no Flyway migration. DP-19 is the gateway-bff route the workbook does not need and the P1 job view uses.

**Artefacts**

| Artefact | Content |
|---|---|
| Run book set | 16 files under `docs/operations/runbooks/<job ID>.md`, each with the eight sections purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation |
| `RunbookCompletenessTest` | Pipeline gate: every Temporal Schedule, every event-started job and every catalogue row has a run book with the eight headings; the forbidden names fail the build with MSG-P2-005 |
| Workbook "Recovery jobs" | Panels for last run, status and duration per job, the alert list, and the last complete ACE business date per source (feed Pending, GAP-3318) |
| Alert rules | One rule for a FAILED job, one for a run past its threshold, one for a held run; each emails the owner role and RW-PLATADM with MSG-P2-004 or MSG-P1-001 |
| ACE business-date panel | The last complete business date per source beside the job panels, fed through the rwb-source-data contract (feed Pending, GAP-3318) |
| Catalogue baseline | The 16 Epic 1 rows as a data set applied through the P2 admin operation, idempotent by job ID; no migration and no code |
| Guard definitions | For rwb-source-data runs the refusals of the rerun (409 MSG-P1-011, 409 MSG-P1-001) and the right check (MSG-P4-002), published by RWB-P1-AD018-CON and implemented by P1 rwb-source-data; the guards of the other services' reruns are Pending (GAP-3271) |

**Platform contract policy.** The DP table's platform H dependencies (RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) are wave 0 platform contracts, published before this story starts under the Day-1 rule (§R5.7). They are therefore not repeated in the metadata `Depends on (build)` row, which stays None, and the story builds against their published contracts and fakes (DP-11).

**Done when.** The gate passes on 16 run books and 16 catalogue rows and fails on a missing section and on a public table name; the catalogue baseline loads twice with one result; the workbook shows last run, status and duration for all 16 jobs and the last complete ACE business date per source, and agrees with the P1 job view on the rwb-source-data runs; the three alert rules fire with MSG-P2-004 and MSG-P1-001 inside the 15-minute target; and a platform administrator restarts JOB-02 in SIT from the run book alone after a late ACE batch. The join key between the P1 job run log, the P2 catalogue row and the telemetry record, and the default expected duration and alert threshold of each job, are Not specified in the source documents (GAP-1419; ASM-2483).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-004 | A job failed or runs past its threshold | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P2-005 | Pipeline finds a job without a complete run book | Job {job} has no run book with the six sections. Missing: {section}. |
| MSG-P1-011 | Rerun of a rwb-source-data run that is not FAILED, or while a run of the type and date is open | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-PLT-N009-03 | Rerun with no `Idempotency-Key` or a non-UUID value | The Idempotency-Key header is required and must be valid for {operation}. |
| MSG-P1-001 | A late or failed ACE batch holds a job, or a rerun is asked while the batch is not COMPLETED | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the right reruns a job | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

### 15. Screens and states

No Workbench screen in this story. The operator surfaces are the workbook "Recovery jobs" (job panels, the alert list and the ACE business-date panel), the P1 job view and the alert list. SCR-44 Interface and job monitor (states running, failed, complete; empty, loading, error and no access: Not specified in the source documents (CG-ALL-1483)) belongs to Epic 2, with the full monitor in Epic 8, and shows the same data from there. The workbook layout and its panel set are fixed at the wave 0 entry check (GAP-1419); the story fixes only the four things each panel must show: the last run, the status, the duration and the last complete ACE business date per source.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-056-08 | AC8 (legacy Access) | Component | RW-CASEOWN calls the P1 rerun operation; refused with MSG-P4-002. |
| TC-E1-056-01 | AC1, AC7 (legacy AC1, BR1, BR2) | Component | 16 catalogue rows and run book files; one file naming public.account |
| TC-E1-056-02 | AC1, AC3 (legacy AC2, BR4) | End to end | JOB-02 forced to fail on an account at 90 days past due |
| TC-E1-056-03 | AC2, AC3 (legacy AC3) | End to end | One run of each job in SIT and one ACE batch row per source. |
| TC-E1-056-04 | AC1 (legacy AC4, BR2) | Component | Run book without the Escalation section |
| TC-E1-056-05 | AC5 (legacy AC5) | Component | JOB-04 running. |
| TC-E1-056-06 | AC4 (legacy AC6, BR3) | Component | JOB-02 slowed past 45 minutes |
| TC-E1-056-07 | AC5 (legacy AC7, BR5) | Component | JOB-04 rerun for a completed date. |
| TC-E1-056-09 | AC6 (legacy AC8, BR7) | End to end | ALS batch FAILED at 05:20 for 2026-12-01; daily work held. |
| TC-E1-056-10 | AC1, AC7 (legacy AC9, BR6) | Component | Branch adding v_ace_account.legacy_bucket with no dictionary row |
| TC-E1-056-11 | AC10 (BR8) | Not specified in the source documents (NEWAC-RWB-PLT-E1056-OPS-AC10) | job_catalog rows and source scan for owner, threshold and path literals |
| TC-E1-056-12 | AC11 | Not specified in the source documents (NEWAC-RWB-PLT-E1056-OPS-AC11) | Consumed view call for JOB-02 fails or gets no answer |
| TC-PLT-E1056-OPS-01 | AC12 | Component | AC12 Daily work starts on the ALS completion only (new, RD-P1-003, RD-P1-040) |
| TC-PLT-E1056-OPS-02 | AC13 | Component | AC13 A FAILED rwb-source-data run is rerun by its run ID (new, RD-P1-012) |
| TC-PLT-E1056-OPS-03 | AC14 | End to end | AC14 Before the job view release a P1 run is restarted by the readiness call (new, RD-P1-012) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: owners, thresholds and paths are catalogue rows.
- No personal data in logs, tests or prompts; the job-run record and the run books hold job IDs, dates, statuses, counts, durations and role names only.
- No read of another service's tables, of a table in schema `public` or of a `recovery.v_ace_*` view: ACE data comes through the P1 contract only (D-RCV-60) and the catalogue through the P2 admin operation.
- ACE data is read only through the rwb-source-data contract (DP-05); no run book describes a direct read of an ACE table.
- A run book names roles and service identities, never a person.
- No run book describes an inbound load, a file arrival or a load rerun; the Workbench has none.
- No secret, credential or connection string appears in a run book, a workbook panel or an alert payload; each is a secret reference.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner | Program 5.2; Epic 1 3.2 | FEAT-DRI-18 | All recovery processes | R-UNI-40; D-RCV-35 U1 | TC-E1-056-01 to TC-E1-056-10 |
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel | Program 6.12 | FEAT-DRI-18 | All recovery processes | D-RCV-35 U1 | TC-E1-056-01, TC-E1-056-04 |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target | Program 6.12 (alert within 15 minutes, DL11) | FEAT-DRI-18 | All recovery processes | DL11 | TC-E1-056-06, TC-E1-056-09 |
| ADR-023 | Observability per service | Program 6.12 | FEAT-DRI-18 | All recovery processes | D-RCV-60 | TC-E1-056-03, TC-E1-056-06 |

Open decisions (still open; each carries an assumption): DL10 with ASM-2250, ASM-2357, ASM-2377 and ASM-2863; DL11 with ASM-0553, ASM-0703, ASM-1051 and ASM-1104.

### 19. Out of scope

- The job bodies and the 19 services' workflows: their own stories.
- The implementations of the P1 job view and rerun and of the P2 catalogue admin operation.
- The SCR-44 screen (Epic 2, full monitor in Epic 8).
- Incident handling after a job failure (FEAT-ADM-12, Epic 8).
- ACE's own ingestion monitoring and alerting; the Workbench watches the business date, not the ACE job.
- The freshness stamp, the stale marker and EV-27 (new stories of RWB-E1-015).
- The 30 views and the view conformance test CHK-01 (new stories of RWB-E1-069); this story only requires that its run book names them.
- The platform jobs JOB-21 and JOB-22 (platform workflow epic); they appear only on the baseline dashboards of RWB-PLT-N005-OPS.

### Remaining delivery steps

- Close GAP-3271, GAP-3318 and GAP-3319 before the workbook and the gate are accepted (solution architect).
- Plan AC5, AC8 and AC13 for the RWB-P1-AD018 release and use the readiness-call restart step until then (DevOps team).
- Size the story at refinement (squad).
- Add the changed and new TC-E1-056 rows to Test Cases v9 and the RTM (QA lead).
- Write the 16 run books and run the gate in the pipeline (DevOps team).
