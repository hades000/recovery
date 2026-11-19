<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 056 Run books and monitoring for every Epic 1 job v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 056 Run books and monitoring for every Epic 1 job v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-056 Run books and monitoring for every Epic 1 job

SCB Collections and Recovery. Henka Group, 28 October 2026.

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
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-007 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **a run book for every scheduled job (purpose, schedule, owner, failure signs, restart steps, escalation) and monitoring of each job's last run, status and duration**, so that **the operations team can restart any Epic 1 job without the developer**.

## 2. Business rationale

Epic 1 runs its loads, case creation, allocation, timers and copies as unattended jobs. A failed job that only its developer can restart holds the case list and the morning allocation. This story gives each job a catalog row with an owner and a run book, checks in the pipeline that both exist, and shows each job's last run, status and duration, so a failed job is noticed and restarted on the same day. It meets REQ-DRI-007 (a named owner for every failure).

## 3. Preconditions

- RWB-E1-007 (adapters and interface_run) is done.
- The Epic 1 jobs are built or stubbed: JOB-01, JOB-02, JOB-03, JOB-04, JOB-05, JOB-09, JOB-10, JOB-11, JOB-12, JOB-13, JOB-14, JOB-15 and JOB-17 (Epic 1 list assumed from the batch schedule; the catalog row sets first_release).
- Spring Batch and Quartz write their execution tables in the ACE database (ACE scheduler pattern, REUSE).
- The person holds RW-PLATADM through RWB-<env>-RW-PLATADM.
- The Log Analytics workspace of the ACE service receives the application logs.

## 4. Flow

1. Platform administrator: adds a job_catalog row per job with job ID, name, owner role, schedule, run book path, expected duration and alert threshold.
2. Squad member (RW-TRIBE): writes the run book at `docs/operations/runbooks/<job ID>.md` with the six sections.
3. Pipeline: RunbookCompletenessTest checks that every Quartz job and Spring Batch job in the service has a catalog row and a run book with the six headings; it fails the build if one is missing.
4. Each job: writes a structured event `rwb.job.run` at start and end with job ID, business date, status and duration.
5. Platform administrator: opens the Log Analytics workbook "Recovery jobs" or calls GET /admin/jobs and sees last run, status and duration per job.
6. Alert rule: a job with status FAILED, or running longer than its alert threshold, emails the owner role and RW-PLATADM with MSG-P2-004.
7. Platform administrator: follows the restart steps in the run book and calls POST /admin/jobs/{jobId}/rerun.
8. System: restarts the job from its failed step; the dependent jobs run in the order of the daily timeline.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X2 | A rerun is requested while the job runs | Refused; the running job continues | MSG-P2-006 | AC5 |
| X3 | A job runs past its alert threshold | The owner role and RW-PLATADM are alerted; the job is not stopped | MSG-P2-004 | AC6 |
| X4 | A rerun of a job that already completed for the business date | The job writes DUPLICATE runs for each key and changes nothing | None | AC7 |
| X5 | A role without the right reruns a job | Refused; nothing changes | MSG-P4-002 | TC-E1-056-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the adapters and run rows of RWB-E1-007; each job's own story supplies the job |
| Negotiable | Owners, thresholds and paths are catalog rows |
| Valuable | Any Epic 1 job can be restarted by operations on the day it fails |
| Estimable | One table, one pipeline test, one workbook, one alert rule, one endpoint |
| Small | Within one week with its tests |
| Testable | Each criterion below is one automated test or pipeline check |

## 7. Acceptance criteria

```gherkin
Feature: Run books and monitoring for every Epic 1 job

  Background:
    Given job_catalog holds 13 rows with first release "E1"

  Scenario: AC2 Restart by run book
    Given JOB-01 failed at 05:20 on business date 2026-11-26 while it loaded the EFS data for "INT-07"
    When a platform administrator follows the restart steps and calls POST /admin/jobs/{jobId}/rerun at 06:05
    Then JOB-01 restarts from its failed step and ends with status "COMPLETED" at 06:25
    Then JOB-02 runs after JOB-01 and the case list shows cases with data as of 2026-11-26
    Then the system records no developer action in the run

  Scenario: AC3 Monitoring in place
    Given every job in job_catalog ran at least once in SIT
    When the platform administrator opens the workbook "Recovery jobs"
    Then each of the 13 jobs shows its last run time, status and duration
    Then GET /admin/jobs returns the same last run, status, startedAt and endedAt for each job

  Scenario: AC5 Rerun while running refused
    Given JOB-03 started at 06:40 and is running
    When a platform administrator calls POST /admin/jobs/{jobId}/rerun for JOB-03 at 06:45
    Then the response is 409 with message MSG-P2-006
    Then JOB-03 continues its run

  Scenario: AC6 Job running past its threshold
    Given JOB-02 has an alert threshold of 45 minutes (assumed; DL11)
    When JOB-02 has run for 46 minutes on business date 2026-11-27
    Then the data steward group and the platform administrator group receive message MSG-P2-004
    Then the system does not stop JOB-02

  Scenario: AC7 Rerun of a completed job changes nothing
    Given JOB-01 completed for business date 2026-11-28
    When a platform administrator reruns it for the same date
    Then each interface run for that date is written as "DUPLICATE"
    Then the system loads no account record a second time
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every scheduled job has a run book, an alert and an owner | FEAT-DRI-18; batch.txt Owner column |
| BR2 | A run book has six sections: purpose, schedule, owner, failure signs, restart steps, escalation | Story intent |
| BR3 | The owner of each job is the role named in the batch schedule, for example JOB-01 and JOB-02 data steward, JOB-03 team managers, JOB-05 platform administrator | batch.txt |
| BR4 | Daily jobs restart in the order of the daily timeline: JOB-01, then JOB-02, JOB-04, JOB-07, JOB-08, then JOB-03 | batch.txt Daily timeline |
| BR5 | A rerun is idempotent for the job and business date | R-UNI-40; events.txt Rules sheet, Delivery |
| BR6 | Owners, thresholds and paths are data rows, never code | Principle 1 |

## 9. State transitions

None. This story does not change a case status. It reads job run status (STARTED, COMPLETED, FAILED) from the Spring Batch execution tables and the interface_run rows.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Maintains job_catalog rows; reruns a job (Platform administration, U) |
| RW-DATASTEW, data steward | Reads job runs; receives alerts for JOB-01, JOB-02, JOB-04, JOB-09, JOB-13 (Platform administration, R) |
| RW-TEAMMGR, team manager | Receives alerts for JOB-03 and JOB-06 by email; no endpoint right |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read job runs (Platform administration, R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-224 to DF-OPS-232 | job_catalog | all fields | Write |
| DF-OPS-226 | job_catalog | job_name | Write |
| DF-OPS-227 | job_catalog | owner_role | Write |
| DF-OPS-228 | job_catalog | schedule_text | Write |
| DF-OPS-229 | job_catalog | runbook_path | Write |
| DF-OPS-230 | job_catalog | expected_minutes | Write |
| DF-OPS-231 | job_catalog | alert_after_minutes | Write |
| DF-OPS-232 | job_catalog | first_release | Write |
| DF-OPS-156 | interface_run | status | Read |
| DF-OPS-153 | interface_run | business_date | Read |
| DF-OPS-159 | interface_run | started_at | Read |
| DF-OPS-160 | interface_run | ended_at | Read |
| DF-REF-035 | role | role_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /admin/jobs | Query: type (job ID), status, from, to | Array of Job: id, type, businessDate, status, startedAt, endedAt, checks | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 | Platform administration, R | Read only |
| POST /admin/jobs/{jobId}/rerun | Path: jobId (the failed execution) | Job | 401; 403 (MSG-P4-002); 404 unknown execution (MSG-P4-003); 409 job running (MSG-P2-006); 503 | Platform administration, U | Per job and business date |
| GET /admin/scheduled-jobs (new, recorded in additions) | None | Array of JobCatalogEntry: jobId, jobName, ownerRole, schedule, runbookPath, expectedMinutes, alertAfterMinutes, firstRelease | 401; 403 (MSG-P4-002) | Platform administration, R | Read only |

GET /admin/jobs and the rerun endpoint are P1 endpoints (x-module P1); their controller calls the published interface below for the catalog and the restart.

**Published interface (package recovery.integration.ops.api).**

```java
public interface JobOperations {
    List<JobCatalogEntry> catalog();
    JobRunView lastRun(String jobId);
    JobRunView rerun(long failedExecutionId); // throws JobAlreadyRunningException, mapped to 409 MSG-P2-006
}
```

## 13. Solution plan

- **Package.** folder `src/main/java/recovery/integration/ops`, Java package `recovery.integration.ops`; run books in `docs/operations/runbooks/`; workbook and alert rules in `ops/monitoring/`.

| Component | Type | Responsibility |
|---|---|---|
| JobCatalogController | Controller | GET /admin/scheduled-jobs |
| JobOperationsImpl | Published interface | Catalog, last run from the Spring Batch job repository, restart through JobOperator.restart |
| JobRunEventListener | Listener | Spring Batch JobExecutionListener writing `rwb.job.run` at start and end |
| JobCatalogRepository | Repository | job_catalog only |
| JobCatalogEntry | Entity | JPA entity with the standard columns |
| RunbookCompletenessTest | Test | Finds every Quartz JobDetail and Spring Batch Job bean; checks the catalog row and the six headings |
| RecoveryJobsWorkbook | Rule table | Log Analytics workbook and the alert rules for FAILED and over-threshold runs |

- **Database:** Flyway migration `V2026_11_56__p2_job_catalog.sql` creates job_catalog (primary key job_id, check job_id matches `^JOB-[0-9]{2}$`) and inserts the 13 Epic 1 rows from the batch schedule.
- **Configuration and reference data:** job_catalog rows maintained by RW-PLATADM; alert thresholds assumed at 1.5 times the expected duration (DL11).
- **Build steps:**
  1. Write the migration and the entity and repository with tests.
  2. Build JobRunEventListener and attach it to every Spring Batch job.
  3. Build JobOperationsImpl with restart, the running check and the idempotent rerun.
  4. Build RunbookCompletenessTest and add it to the pipeline.
  5. Write the 13 run books with the six sections.
  6. Build the workbook and the two alert rules; test each with a forced failure in SIT.
  7. Build GET /admin/scheduled-jobs with the access check.
- **Feature flag:** `rwb.integration.job-monitoring`.
- **Done when:** the tests in section 16 pass and a platform administrator restarts JOB-01 in SIT from the run book alone.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-004 | A job failed or runs past its threshold | {job} failed at {time} for business date {date}. Follow run book {runbook}. |
| MSG-P2-005 | Pipeline finds a job without a complete run book | Job {job} has no run book with the six sections. Missing: {section}. |
| MSG-P2-006 | Rerun of a running job | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right reruns a job | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. The platform administrator uses the Log Analytics workbook "Recovery jobs" and the admin endpoints. SCR-44 Interface and job monitor (states running, failed, complete) shows the same data from Epic 2.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-056-01 | BR1, BR2 | System | 13 catalog rows and run book files |
| TC-E1-056-02 | AC2, BR4 | System | JOB-01 forced to fail on the INT-07 step |
| TC-E1-056-03 | AC3 | System | One run of each job in SIT |
| TC-E1-056-04 | BR2 | System | Run book without the Escalation section |
| TC-E1-056-05 | AC5 | System | JOB-03 running |
| TC-E1-056-06 | AC6, BR3 | System | JOB-02 slowed past 45 minutes |
| TC-E1-056-07 | AC7, BR5 | System | JOB-01 rerun for a completed date |
| TC-E1-056-08 | Access | Access | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: owners, thresholds and paths are catalog rows.
- No personal data in logs, tests or prompts; job events hold job IDs, dates, counts and durations only.
- No read of another module's tables; the Spring Batch tables are read through the framework job repository.
- A run book names roles and service identities, never a person.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner | Program 5.2; Epic 1 3.2 | FEAT-DRI-18 | All recovery processes | R-UNI-40 | TC-E1-056-01 to TC-E1-056-07 |

## 19. Out of scope

- The SCR-44 screen: Epic 2; full monitor in Epic 8.
- Incident handling after a job failure: FEAT-ADM-12, Epic 8.
- The feeds on Control-M and ADF: RWB-E1-051.
