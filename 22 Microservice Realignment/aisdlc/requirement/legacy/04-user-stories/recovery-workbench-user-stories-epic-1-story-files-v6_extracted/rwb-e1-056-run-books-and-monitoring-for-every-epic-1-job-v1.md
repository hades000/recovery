<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 056 Run books and monitoring for every Epic 1 job v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 056 Run books and monitoring for every Epic 1 job v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-056 Run books and monitoring for every Epic 1 Workbench job

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-056 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | FEAT-DRI-18 Run run books and monitoring for every job |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.2 |
| L3 process | All recovery processes |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 |
| Priority | Must |
| Depends on | RWB-E1-007, RWB-E1-015, RWB-E1-069 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **a run book for every Workbench job, the agent runtime and the view conformance check (purpose, schedule, owner, dependencies, failure signs, checks, restart steps, escalation) and monitoring of each job's last run, status and duration beside the last complete ACE business date per source**, so that **the operations team can restart any Epic 1 job without the developer and can tell a late ACE batch from a failed Workbench job**.

## 2. Business rationale

The Workbench loads no source data (D-RCV-35 U1; ADR-010). Its scheduled work is the case list chain, the timer check, daily rebalancing, payment matching, booking confirmation, the WIN notice file, the outbox sender, document intake, the decision log copy and its hash chain check, the reporting extract, retention, the agent runtime and the view conformance test. A failed job that only its developer can restart holds the case list and the morning allocation; a late ACE batch looks exactly like a failed Workbench job unless the monitor shows the ACE business date beside it.

This story gives each job a catalog row with an owner and a run book, checks in the pipeline that both exist and that the run books name the ACE batch dependency, the stale marker and AceDataLate, and the view conformance test, and shows each job's last run, status and duration beside the last complete ACE business date per source from `v_ace_batch_status`. No inbound load job is catalogued: ACE ingests every source, ACE monitors its own ingestion, and the Workbench watches only the business date it receives. It meets REQ-DRI-007 (a named owner for every failure).

## 3. Preconditions

- RWB-E1-007 is done: JOB-10 and JOB-11 send the outbound files and write the outbox.
- RWB-E1-015 is done: `v_ace_batch_status`, `data_product_load`, the stale marker and EV-27 AceDataLate are in place.
- RWB-E1-069 is done: the 30 `recovery.v_ace_*` views, the grants and the view conformance test CHK-01.
- The Workbench jobs are built or stubbed: JOB-02, JOB-03, JOB-04, JOB-05, JOB-06, JOB-07, JOB-08, JOB-10, JOB-11, JOB-12, JOB-13, JOB-14, JOB-15 and JOB-17, plus the agent runtime service AGT-01 and the view conformance test CHK-01. The catalog row sets `first_release` to "E1".
- The jobs run on the clustered ACE Quartz scheduler and record each run through the P1 job run log (RWB-TE-007). No inbound load job exists.
- The person holds RW-PLATADM through RWB-<env>-RW-PLATADM.
- The Log Analytics workspace of the ACE service receives the application logs.

## 4. Flow

1. Platform administrator: confirms one `job_catalog` row per job with job ID, name, owner role, schedule, run book path, expected duration and alert threshold. V0004 seeds the 16 Epic 1 rows; later changes are data rows, not code.
2. Squad member (RW-TRIBE): writes the run book at `docs/operations/runbooks/<job ID>.md` with eight sections: purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation.
3. Squad member: names the ACE sources the job reads through `recovery.v_ace_*` and the upstream Workbench job in Dependencies; names the stale marker on `data_product_load` and EV-27 AceDataLate in Failure signs when the job reads ACE; the view conformance run book names CHK-01 and the dictionary load through RWB-E1-043 in Checks and Restart steps.
4. Pipeline: `RunbookCompletenessTest` checks that every Quartz job and every catalog row has a run book with the eight headings, that no run book names an inbound load job, a file arrival, a load rerun or a data quality exception console, and that no run book names a table in schema `public`.
5. Each job: writes a structured event `rwb.job.run` at start and end with job ID, business date, status and duration.
6. Platform administrator: opens the Log Analytics workbook "Recovery jobs" or calls GET /admin/jobs and sees last run, status and duration per job, and the last complete ACE business date per source from `v_ace_batch_status`.
7. Alert rule: a job with status FAILED, or running longer than its alert threshold, emails the owner role and RW-PLATADM with MSG-P2-004.
8. System: when an ACE batch is late or failed, the freshness step marks the product STALE, publishes EV-27 AceDataLate and holds the dependent job; the run book says to wait for the batch and not to rerun the job.
9. Platform administrator: follows the restart steps in the run book and calls POST /admin/jobs/{jobId}/rerun.
10. System: restarts the job from its failed step; the dependent jobs run in the order of the daily timeline.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A job has no catalog row or no run book, or a run book lacks a section | The pipeline fails and names the job and the missing section | MSG-P2-005 | AC4 |
| X2 | A run book names an inbound load job, a file arrival, a load rerun, a data quality exception console or a table in schema public | The pipeline fails and names the run book and the forbidden line | Build log: JOB-02.md names public.account; a run book may name only the Workbench jobs and recovery.v_ace_* | AC1 |
| X3 | A rerun is requested while the job runs | Refused; the running job continues | MSG-P2-006 | AC5 |
| X4 | A job runs past its alert threshold | The owner role and RW-PLATADM are alerted; the job is not stopped | MSG-P2-004 | AC6 |
| X5 | A rerun of a job that already completed for the business date | Refused with 409; the job runs nothing and no business row changes | MSG-GEN-004 | AC7 |
| X6 | An ACE batch is late or failed | The product is marked STALE, EV-27 is published, the dependent job is recorded WAITING and is not rerun | MSG-P1-001 | AC8 |
| X7 | The view conformance test CHK-01 fails | The merge is blocked; the run book gives the dictionary load through RWB-E1-043 as the fix | v_ace_account.legacy_bucket has no data dictionary entry | AC9 |
| X8 | A role without the right reruns a job | Refused; nothing changes | MSG-P4-002 | TC-E1-056-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the outbound jobs of RWB-E1-007, the batch view and stale marker of RWB-E1-015 and the views and conformance test of RWB-E1-069; each job's own story supplies the job |
| Negotiable | Owners, thresholds and paths are catalog rows; the story fixes the eight run book sections and the two checks |
| Valuable | Any Workbench job can be restarted by operations on the day it fails, and a late ACE batch is not mistaken for a Workbench failure |
| Estimable | One seed migration, one pipeline test, one workbook, two alert rules, one endpoint |
| Small | Within one week with its tests |
| Testable | Each criterion below is one automated test or pipeline check |

## 7. Acceptance criteria

```gherkin
Feature: Run books and monitoring for every Epic 1 Workbench job

  Background:
    Given job_catalog holds 16 rows with first release "E1": JOB-02, JOB-03, JOB-04, JOB-05, JOB-06, JOB-07, JOB-08, JOB-10, JOB-11, JOB-12, JOB-13, JOB-14, JOB-15, JOB-17, AGT-01 and CHK-01
    Given the daily case list chain is JOB-02, then JOB-03, JOB-04, JOB-07 and JOB-08, with JOB-05 every five minutes

  Scenario: AC1 Run book present
    Given the 16 rows in job_catalog
    When RunbookCompletenessTest runs in the pipeline
    Then each of the 16 jobs has a file in docs/operations/runbooks
    Then each file has the sections purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation
    Then every run book of a job that reads ACE names v_ace_batch_status in Dependencies and the stale marker and EV-27 AceDataLate in Failure signs
    Then the run book for CHK-01 names the view conformance check and the dictionary load through RWB-E1-043 in Checks and Restart steps
    Then no file names an inbound load job, a file arrival, a load rerun, a data quality exception console or a table in schema public

  Scenario: AC2 Restart by run book
    Given JOB-02 failed at 05:40 on business date 2026-11-30 at its case creation step, because v_ace_account returned no row for an account at 90 days past due
    When a platform administrator follows the restart steps, confirms in v_ace_batch_status that ALS is COMPLETED for 2026-11-30, and calls POST /admin/jobs/{jobId}/rerun at 06:05
    Then JOB-02 restarts from its failed step and ends with status "COMPLETED" at 06:20
    Then JOB-03 runs after JOB-02 and the case list shows the cases with data as of 2026-11-30
    Then the run records no developer action

  Scenario: AC3 Monitoring in place
    Given every job in job_catalog ran at least once in SIT
    When the platform administrator opens the workbook "Recovery jobs"
    Then each of the 16 jobs shows its last run time, status and duration
    Then the workbook shows the last complete ACE business date per source from v_ace_batch_status beside the jobs
    Then GET /admin/jobs returns the same last run, status, startedAt and endedAt for each job
    Then GET /admin/scheduled-jobs returns 16 entries with owner role, schedule, run book path and alert threshold

  Scenario: AC4 Missing run book blocks the build
    Given a developer adds a Quartz job "JOB-20" with a run book that has no "Escalation" section
    When the pipeline runs
    Then the build fails with message MSG-P2-005 naming job "JOB-20" and section "Escalation"

  Scenario: AC5 Rerun while running refused
    Given JOB-04 started at 06:40 and is running
    When a platform administrator calls POST /admin/jobs/{jobId}/rerun for JOB-04 at 06:45
    Then the response is 409 with message MSG-P2-006
    Then JOB-04 continues its run

  Scenario: AC6 Job running past its threshold
    Given JOB-02 has an alert threshold of 45 minutes (assumed; DL11)
    When JOB-02 has run for 46 minutes on business date 2026-12-01
    Then the data steward group and the platform administrator group receive message MSG-P2-004
    Then the system does not stop JOB-02

  Scenario: AC7 Rerun of a completed job changes nothing
    Given JOB-04 completed for business date 2026-12-01
    When a platform administrator reruns it for the same date
    Then the response is 409 with message MSG-GEN-004
    Then case_list_row still holds one row per case account for 2026-12-01
    Then reconciliation_result still holds one row per product group for 2026-12-01

  Scenario: AC8 A late ACE batch holds the job
    Given v_ace_batch_status shows EFS for business date 2026-12-01 with status "FAILED" at 05:20
    When the freshness step runs
    Then data_product_load marks DP05 Contact and promises "STALE" at 05:20 and EV-27 AceDataLate is published
    Then the case list step of JOB-04 does not start for 2026-12-01 and its run is recorded "WAITING"
    Then the run book for JOB-04 says to wait for the EFS batch and not to rerun JOB-04
    Then when the EFS batch completes at 08:40, the daily gate returns COMPLETE and JOB-04 starts for 2026-12-01

  Scenario: AC9 The view conformance test has a run book
    Given a branch adds column "legacy_bucket" to recovery.v_ace_account with no sys_fields row
    When the pipeline runs CHK-01
    Then CHK-01 fails with "v_ace_account.legacy_bucket has no data dictionary entry"
    Then the merge is blocked
    Then the run book for CHK-01 gives the fix: load the dictionary row through RWB-E1-043 and rerun CHK-01
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every Workbench job, the agent runtime and the view conformance test have a run book, an alert and an owner. No inbound load job is catalogued; ACE ingestion is ACE's and is not monitored here | FEAT-DRI-18; D-RCV-35 U1 |
| BR2 | A run book has eight sections: purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation | Story intent |
| BR3 | The owner of each job is the role in `job_catalog`: JOB-02 and JOB-04 data steward; JOB-03 and JOB-06 team managers; JOB-07 and JOB-08 credit administration; JOB-10, JOB-11, JOB-12 and CHK-01 platform administrator; JOB-13 data steward; JOB-14 and JOB-17 compliance; JOB-15 reporting and BI analyst; AGT-01 center of excellence | batch.txt; roles.txt |
| BR4 | Daily jobs restart in the order of the daily timeline: JOB-02, then JOB-03, JOB-04, JOB-07 and JOB-08; JOB-05 runs every five minutes; JOB-06 runs at 06:30 | batch.txt Daily timeline |
| BR5 | A rerun of a completed job and business date is refused; the job body is idempotent for its business date | R-UNI-40; events.txt Rules sheet, Delivery |
| BR6 | A job reads ACE only through `recovery.v_ace_*` and never loads source data. A run book that names a public table, an inbound load job or a file arrival fails the build | D-RCV-35 U1, U4; ADR-010; RWB-TE-001 |
| BR7 | When an ACE batch is late or failed, the product is STALE, EV-27 is published and the dependent job waits; the monitor shows the ACE business date beside the job run | RWB-E1-015; BR-P1-014 |
| BR8 | Owners, thresholds and paths are data rows, never code | Principle 1 |

## 9. State transitions

None. This story does not change a case status. It reads and records job run status: STARTED, COMPLETED, FAILED, WAITING and SKIPPED. A rerun of a completed job for its business date is refused.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Maintains job_catalog rows; reruns a job (Platform administration, U); owns JOB-10, JOB-11, JOB-12 and CHK-01 |
| RW-DATASTEW, data steward | Reads job runs; owns JOB-02, JOB-04 and JOB-13; receives their alerts (Platform administration, R) |
| RW-TEAMMGR, team manager | Owns JOB-03 and JOB-06; receives their alerts by email; no endpoint right |
| RW-CREDITAD, credit administration | Owns JOB-07 and JOB-08; receives their alerts by email |
| RW-BIANAL, reporting and BI analyst | Owns JOB-15; receives its alerts by email |
| RW-COE, center of excellence analyst | Owns AGT-01; receives its alerts by email |
| RW-COMPLY, compliance | Owns JOB-14 and JOB-17; receives their alerts by email |
| RW-TRIBE, squad member | Writes and maintains the run books and RunbookCompletenessTest; reads job runs (Platform administration, R) |
| RW-AUDIT and RW-SECADM | Read job runs (Platform administration, R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-224 to DF-OPS-232 | job_catalog | all 9 fields | Write |
| DF-OPS-226 | job_catalog | job_name | Write |
| DF-OPS-227 | job_catalog | owner_role | Write |
| DF-OPS-228 | job_catalog | schedule_text | Write |
| DF-OPS-229 | job_catalog | runbook_path | Write |
| DF-OPS-230 | job_catalog | expected_minutes | Write |
| DF-OPS-231 | job_catalog | alert_after_minutes | Write |
| DF-OPS-232 | job_catalog | first_release | Write |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-181 | v_ace_batch_status | completed_at | Read |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-OPS-002 | data_product_load | product_code | Read |
| DF-OPS-004 | data_product_load | business_date | Read |
| DF-OPS-007 | data_product_load | status | Read |
| DF-OPS-008 | data_product_load | stale_flagged_at | Read |
| DF-RPT-002 | case_list_row | business_date | Read |
| DF-OPS-120 | reconciliation_result | business_date | Read |
| DF-OPS-129 | reconciliation_result | result | Read |
| DF-REF-035 | role | role_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary and in Physical Schema v5. `job_catalog` is created by V0001; this story seeds its rows and adds no column.

## 12. Contract

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /admin/jobs | Query: type (job ID), status, from, to | Array of Job: id, type, businessDate, status, startedAt, endedAt, runbookPath, checks | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 | Platform administration, R | Read only |
| POST /admin/jobs/{jobId}/rerun | Path: jobId (the failed execution) | Job | 401; 403 (MSG-P4-002); 404 unknown execution (MSG-P4-003); 409 job running (MSG-P2-006) or run already completed (MSG-GEN-004); 503 | Platform administration, U | Per job and business date |
| GET /admin/scheduled-jobs | None | JobCatalogResponse: entries of JobCatalogEntry (jobId, jobName, ownerRole, schedule, runbookPath, expectedMinutes, alertAfterMinutes, firstRelease) and aceBatchStatus of AceBatchStatus (sourceSystem, businessDate, startedAt, completedAt, status, isComplete) | 401; 403 (MSG-P4-002); 503 | Platform administration, R | Read only |

GET /admin/jobs and the rerun endpoint are P1 endpoints (x-module P1); their controller calls the published interface below for the catalog, the last run, the restart and the ACE batch status.

**Published interface (package recovery.integration.ops.api).**

```java
public interface JobOperations {
    List<JobCatalogEntry> catalog();
    JobRunView lastRun(String jobId);
    JobRunView rerun(long failedExecutionId); // throws JobAlreadyRunningException, mapped to 409 MSG-P2-006
    List<AceBatchStatus> aceBatchStatus();     // reads recovery.v_ace_batch_status only
}
```

## 13. Solution plan

- **Package.** Folder `src/main/java/recovery/integration/ops`, Java package `recovery.integration.ops`; run books in `docs/operations/runbooks/`; workbook and alert rules in `ops/monitoring/`.

| Component | Type | Responsibility |
|---|---|---|
| JobCatalogController | Controller | GET /admin/scheduled-jobs |
| JobOperationsImpl | Published interface | Catalog, last run from the job run log, restart through the scheduler, ACE batch status from v_ace_batch_status |
| JobRunEventListener | Listener | Quartz and job-runner listener writing `rwb.job.run` at start and end |
| JobCatalogRepository | Repository | job_catalog only |
| JobCatalogEntry | Entity | JPA entity with the standard columns |
| AceBatchStatusReader | Repository | Reads v_ace_batch_status; no other ACE object |
| RunbookCompletenessTest | Test | Finds every Quartz JobDetail and every catalog row; checks the run book, the eight headings and the forbidden names |
| RecoveryJobsWorkbook | Rule table | Log Analytics workbook and the alert rules for FAILED and over-threshold runs, with the ACE business date panel |

- **Database:** `job_catalog` is created by V0001 (RWB-E1-001) with 9 business columns. Flyway migration `V0004__rwb_e1_056_job_catalog_seed.sql` inserts the 16 Epic 1 rows and changes nothing on a second run (`ON CONFLICT (job_id) DO NOTHING`).
- **Configuration and reference data:** job_catalog rows maintained by RW-PLATADM; alert thresholds assumed at 1.5 times the expected duration (DL11); the forbidden-name list in `recovery-modules.yaml`, read from the module map of RWB-TE-001.
- **Build steps:**
  1. Write the seed migration and the entity and repository with tests.
  2. Build JobRunEventListener and attach it to every Quartz job and the agent runtime.
  3. Build JobOperationsImpl with restart, the running check and the idempotent rerun.
  4. Build AceBatchStatusReader over `v_ace_batch_status` and add the panel to the workbook.
  5. Build RunbookCompletenessTest with the eight headings and the forbidden names; prove it fails on a missing section and on a public table name.
  6. Write the 16 run books with the eight sections.
  7. Build the workbook and the two alert rules; test each with a forced failure in SIT.
  8. Build GET /admin/scheduled-jobs with the access check.
- **Feature flag:** `rwb.integration.job-monitoring`.
- **Done when:** the tests in section 16 pass and a platform administrator restarts JOB-02 in SIT from the run book alone after a late ACE batch.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-004 | A job failed or runs past its threshold | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P2-005 | Pipeline finds a job without a complete run book | Job {job} has no run book with the eight sections. Missing: {section}. |
| MSG-P2-006 | Rerun of a running job | {job} is already running. Wait until it ends before you run it again. |
| MSG-GEN-004 | A rerun of a run that already completed, or a change from an old version | Someone else changed this record. Reload it to see their change. |
| MSG-P1-001 | A late or failed ACE batch holds a job | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | A role without the right reruns a job | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. The platform administrator uses the Log Analytics workbook "Recovery jobs" and the admin endpoints. SCR-44 Interface and job monitor (states running, failed, complete) shows the same data from Epic 2.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-056-01 | AC1, BR1, BR2 | System | 16 catalog rows and run book files; one file naming public.account |
| TC-E1-056-02 | AC2, BR4 | System | JOB-02 forced to fail on an account at 90 days past due |
| TC-E1-056-03 | AC3 | System | One run of each job in SIT and one ACE batch row per source |
| TC-E1-056-04 | AC4, BR2 | System | Run book without the Escalation section |
| TC-E1-056-05 | AC5 | System | JOB-04 running |
| TC-E1-056-06 | AC6, BR3 | System | JOB-02 slowed past 45 minutes |
| TC-E1-056-07 | AC7, BR5 | System | JOB-04 rerun for a completed date |
| TC-E1-056-08 | Access | Access | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |
| TC-E1-056-09 | AC8, BR7 | System | EFS batch FAILED at 05:20 for 2026-12-01; JOB-04 held |
| TC-E1-056-10 | AC9, BR6 | System | Branch adding v_ace_account.legacy_bucket with no dictionary row |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: owners, thresholds and paths are catalog rows.
- No personal data in logs, tests or prompts; job events hold job IDs, dates, counts and durations only.
- No read of another module's tables and no read of a table in schema `public`: ACE data comes through `recovery.v_ace_*` only. The Quartz tables are read through the scheduler API.
- A run book names roles and service identities, never a person.
- No run book describes an inbound load, file arrival or load rerun; the Workbench has none.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner | Program 5.2; Epic 1 3.2 | FEAT-DRI-18 | All recovery processes | R-UNI-40; D-RCV-35 U1 | TC-E1-056-01 to TC-E1-056-10 |

## 19. Out of scope

- The SCR-44 screen: Epic 2; full monitor in Epic 8.
- Incident handling after a job failure: FEAT-ADM-12, Epic 8.
- ACE's own ingestion monitoring and alerting: RWB-ACE-001. The Workbench watches the business date, not the ACE job.
- The freshness stamp, the stale marker and EV-27: RWB-E1-015.
- The 30 views and the view conformance test: RWB-E1-069.
- The job bodies and the agent runtime: their own stories.
