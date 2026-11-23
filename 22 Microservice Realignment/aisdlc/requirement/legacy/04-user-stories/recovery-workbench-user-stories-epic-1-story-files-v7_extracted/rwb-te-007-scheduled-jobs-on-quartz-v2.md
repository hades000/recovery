<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB TE 007 Scheduled jobs on Quartz v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB TE 007 Scheduled jobs on Quartz v2.md`  
> **Converted from:** Markdown (extracted)

# RWB-TE-007 Scheduled jobs on Quartz

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-007 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | None (technical enabler) |
| Requirement IDs | REQ-CWC-007, REQ-CWC-011, REQ-RDF-007 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.1, 5.3 and 6.3 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1, T2); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-044, RWB-E1-056, RWB-E1-028 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the timer check, the morning allocation run and the daily reconciliation run as Quartz jobs with a run book each**, so that **scheduled work runs once, on time and visibly, and a missed run is caught up for its business date**.

## 2. Business rationale

The morning allocation must finish by 07:00 so no new case waits for a person (JOB-03), the timer check must find every due timer every 5 minutes (JOB-05), and the reconciliation must compare the case list with the core bank every day (JOB-04). The ACE service runs on more than one instance, so without a shared schedule a job runs twice or not at all, and an outage loses a day's run. This story runs the three jobs on the clustered ACE Quartz scheduler with one run per business date, catch-up after an outage and a run book for each. It meets REQ-CWC-007, REQ-CWC-011 and REQ-RDF-007. The measure is one successful run per job per business date, and JOB-03 complete by 07:00 (NFR-013).

Quartz is kept for every Epic 1 and Epic 2 job (D-RCV-36 T2). JOB-05 is also the Quartz implementation of the published TimerScheduler port of RWB-E1-028, so Epic 3 replaces the implementation with Temporal durable timers without changing a caller (ADR-011). No new Quartz job may hold a case wait: a wait on a case belongs to the case workflow and moves to Temporal in Epic 3.

## 3. Preconditions

- RWB-E1-044 is done: migrations run with the parameterized schema.
- RWB-E1-056 is done: the job monitor records runs and alerts the operations channel.
- RWB-E1-028 is done: the published TimerScheduler port exists in package `recovery.casewf.timers` and JOB-05 implements it.
- The ACE Quartz scheduler runs with a clustered JDBC job store; its `QRTZ_` tables belong to the ACE common module.
- JOB-01 COLLINS load check and intake publishes LoadCompleted (EV-26) with the business date; JOB-02 Case creation records its run per business date.
- The job bodies exist: allocation (RWB-E1-020), reconciliation (RWB-E1-011) and timer check (RWB-E1-028).
- `jobs.catch-up.max-dates` = 5 (assumed; DL11) and the 07:00 deadline for JOB-03 (NFR-013) are in the configuration service.
- No Temporal schedule and no Temporal durable timer is registered in Epic 1 or Epic 2 (D-RCV-36 T2).

## 4. Flow

1. Scheduler: on LoadCompleted for business date D, and on completion of JOB-02 for D, fires JOB-03 Morning allocation and JOB-04 Daily reconciliation for D.
2. Scheduler: fires JOB-05 Timer check every 5 minutes on cron `0 0/5 * * * ?` in Asia/Bangkok. JOB-05 is the Quartz implementation of the TimerScheduler port of RWB-E1-028: schedule, cancel, pause and resume write the timer row, and the fire runs the warning, breach and expiry check.
3. Job runner: takes the cluster lock so only one instance runs a job at a time.
4. Job runner: checks the job run log for job and business date; if a successful run exists, records the skip and stops.
5. Job runner: checks the job's dependency (JOB-02 succeeded for D); if not met, records WAITING and stops.
6. Job runner: records the run start through the P1 job monitor, runs the job body, records the end with status SUCCEEDED or FAILED and the counts.
7. Job runner: on service start, for each business date of a passed COLLINS load with no successful run of JOB-03 or JOB-04, runs the job for that date in date order, up to `jobs.catch-up.max-dates` dates.
8. Deadline watcher: at 07:00 checks JOB-03 for the current business date; if it has not succeeded, alerts the operations channel.
9. Platform administrator: reads runs on SCR-44 and reruns a failed run through `POST /admin/jobs/{jobId}/rerun`.
10. No Quartz job waits on a case: a job runs its own unit of work, a business date or a fire time slot, and returns; no case wait is held in a job (BR9).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A run for the job and business date already succeeded | The run is skipped and recorded as a skip | None | AC3 |
| X2 | A timer check run is still going when the next one is due | The next fire waits; never two at once | None | AC4 |
| X3 | More missed dates than the catch-up limit | No automatic catch-up; an alert names the dates | MSG-P3-031 | AC6 |
| X4 | JOB-02 has not succeeded for the date | JOB-03 waits and is recorded WAITING | MSG-P3-031 | AC7 |
| X5 | The instance running a job stops part way | Another instance recovers the job and runs it again for the date | None | AC8 |
| X6 | JOB-03 has not succeeded by 07:00 | Alert to the operations channel within 15 minutes | MSG-P3-031 | AC9 |
| X7 | A job has no run book | The build fails | None | AC10 |
| X8 | A new Quartz job holds a wait on a case | The build fails on the architecture test; no such job is scheduled | None | AC11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the ACE scheduler and the P1 job monitor; job bodies come from their own stories |
| Negotiable | Schedules, the catch-up limit and the deadline are data |
| Valuable | Allocation, timers and reconciliation run once a day per date, even after an outage |
| Estimable | One job runner, one catch-up step, one deadline check, three job registrations |
| Small | Fits in one sprint with its tests |
| Testable | Two-instance tests against a PostgreSQL test container with a controlled clock |

## 7. Acceptance criteria

```gherkin
Feature: Scheduled jobs on Quartz

  Background:
    Given two service instances "ACE-1" and "ACE-2" share the clustered Quartz job store
    Given the COLLINS load for business date 2026-12-02 passed its checks at 05:20 and JOB-02 succeeded at 05:50

  Scenario: AC1 Runs once
    When the morning allocation is due for business date 2026-12-02
    Then JOB-03 runs once, on one of the two instances
    Then the system logs its run with job "JOB-03", business date 2026-12-02, instance, start, end, status "SUCCEEDED" and the case counts

  Scenario: AC2 Missed run
    Given both instances were down from 04:30 to 09:40 on 2026-12-02
    When the service restarts at 09:40
    Then JOB-03 and JOB-04 run for business date 2026-12-02 after JOB-02 succeeds for that date
    Then the system logs each run with MSG-P3-030 naming the job and 2026-12-02

  Scenario: AC3 Repeated run for the same date
    Given JOB-03 succeeded for business date 2026-12-02
    When JOB-03 is fired again for 2026-12-02
    Then the system allocates no case again
    Then the run log records a skip for JOB-03 and 2026-12-02

  Scenario: AC4 Timer check does not overlap
    Given a JOB-05 run that started at 10:00 takes 7 minutes
    When the 10:05 fire is due
    Then the 10:05 run starts only after the 10:00 run ends
    Then no two JOB-05 runs are in progress at the same time

  Scenario: AC5 Several missed dates
    Given COLLINS loads passed for business dates 2026-12-02, 2026-12-03 and 2026-12-04 while both instances were down
    When the service restarts on 2026-12-04 at 11:00
    Then JOB-03 runs for 2026-12-02, then 2026-12-03, then 2026-12-04
    Then the system logs each run with its business date

  Scenario: AC6 More missed dates than the limit
    Given 7 business dates with passed COLLINS loads and no JOB-03 run
    When the service restarts
    Then no automatic catch-up run starts
    Then an alert with MSG-P3-031 names JOB-03 and the 7 dates

  Scenario: AC7 Dependency not met
    Given JOB-02 failed for business date 2026-12-03
    When JOB-03 is due for 2026-12-03
    Then JOB-03 does not run and its run is recorded "WAITING" with MSG-P3-031 naming "JOB-02"
    Then when JOB-02 succeeds for 2026-12-03 at 08:10 JOB-03 runs for 2026-12-03

  Scenario: AC8 Instance stops part way
    Given JOB-04 is running for 2026-12-02 on "ACE-1"
    When "ACE-1" stops
    Then "ACE-2" runs JOB-04 again for 2026-12-02 within the cluster check-in interval of 20 seconds
    Then the run log shows one "FAILED" run on "ACE-1" and one "SUCCEEDED" run on "ACE-2"

  Scenario: AC9 Allocation late
    Given JOB-03 for 2026-12-02 has not succeeded at 07:00
    When the deadline check runs at 07:00
    Then an alert with MSG-P3-031 naming JOB-03, 2026-12-02 and 07:00 reaches the operations channel by 07:15

  Scenario: AC10 Run book for every job
    Given the run book folder holds run books for JOB-03 and JOB-05 only
    When the build runs
    Then the build fails naming JOB-04

  Scenario: AC11 No new Quartz job holds a case wait
    Given a proposed job class "CaseReminderJob" that sleeps until a case reaches its next stage
    When the architecture test runs in the build
    Then the build fails and names "CaseReminderJob"
    Then JOB-05 passes the same test: it schedules, pauses, resumes and cancels timer rows through TimerScheduler and holds no wait on a case
    Then no Temporal schedule is registered in Epic 1 or Epic 2
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each daily job runs once per business date, on one instance | batch.txt Jobs; REQ-CWC-007 |
| BR2 | JOB-03 and JOB-04 run after JOB-02 succeeds for the same business date | batch.txt Jobs and Daily timeline |
| BR3 | JOB-03 completes by 07:00; a later completion raises an alert | NFR-013; batch.txt JOB-03 |
| BR4 | JOB-05 runs every 5 minutes and a missed fire is not repeated; the next run picks up missed timers | batch.txt JOB-05 |
| BR5 | After an outage, each missed business date runs in date order, up to the catch-up limit (assumed 5; DL11) | batch.txt "If it fails or runs late" |
| BR6 | A run for a job and business date that already succeeded has no further effect | R-UNI-40; events.txt Rules |
| BR7 | Every scheduled job has a run book, monitoring and an alert to the operations channel | NFR-067; NFR-068 |
| BR8 | Job bodies are idempotent for their business date | R-UNI-40 |
| BR9 | No new Quartz job may hold a case wait; case waits move to Temporal in Epic 3 | D-RCV-36 T1, T2; ADR-011 |

## 9. State transitions

None. This story does not change a case status. It changes job run statuses in the P1 job monitor: STARTED to SUCCEEDED or FAILED, WAITING when the dependency is not met, and SKIPPED when the date already succeeded.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Reads runs and reruns a failed run (Platform administration CRUD) |
| RW-DATASTEW, data steward | Reads runs; owns JOB-04 (Platform administration R) |
| RW-TEAMMGR, team manager | Owns JOB-03 per batch.txt; is told by the allocation summary (RWB-E1-020) |
| SY-CASEWF, case workflow module | Runs JOB-03 and JOB-05; JOB-05 is the TimerScheduler implementation |
| SY-DATALOAD, data load from COLLINS | Runs JOB-04 inputs from the COLLINS load |

## 11. Data

No business field. The story writes the job run log of the P1 job monitor through its published interface and uses the `QRTZ_` tables of the ACE common module. Neither is in the Logical Data Model. The job bodies read and write their own fields in their own stories.

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Jobs**

| Item | JOB-03 Morning allocation | JOB-04 Daily reconciliation | JOB-05 Timer check |
|---|---|---|---|
| Trigger | LoadCompleted (EV-26) for D and JOB-02 succeeded for D | LoadCompleted (EV-26) for D and JOB-02 succeeded for D | Cron `0 0/5 * * * ?`, Asia/Bangkok |
| Schedule | Daily after JOB-02, by 07:00 | Daily after JOB-02 | Every 5 minutes |
| Runs on | Quartz (D-RCV-36 T2) | Quartz (D-RCV-36 T2) | Quartz; the Epic 1 implementation of TimerScheduler (D-RCV-36 T2) |
| Input | New cases of D | Accounts at 90 days past due in the load of D and open cases | Timers with `expires_at` or `warn_at` before now |
| Output | Cases placed and owners given (RWB-E1-020) | Reconciliation breaks (RWB-E1-011) | Warnings, escalations, timer events (RWB-E1-028) |
| Events published | CaseAllocated (EV-02), CaseAllocationFailed (EV-03), by the job body | None | TimerDue (EV-18), TimerBreached (EV-19), by the job body |
| Idempotency key | Job ID and business date | Job ID and business date | Job ID and fire time slot |
| Restart behavior | Catch-up per missed date; recovery on another instance | Catch-up per missed date; recovery on another instance | Missed fires not repeated; the next run picks up |

**GET /api/recovery/v1/admin/jobs** (P1) lists runs (`Job[]`: `id`, `type`, `businessDate`, `status`, `startedAt`, `endedAt`, `checks`). Platform administration R. Errors 401, 403 (MSG-P4-002), 503.

**POST /api/recovery/v1/admin/jobs/{jobId}/rerun** (P1) reruns a FAILED or WAITING run for its business date. Platform administration U. Errors 401, 403 (MSG-P4-002), 404 (MSG-P4-003), 409 the run already succeeded (MSG-GEN-004), 503. Idempotent: a rerun of a run that succeeded returns 409 and runs nothing.

**Published interface** (package `recovery.casewf.scheduling.api`):

```java
public interface BusinessDateJob {
    String jobId();                              // for example "JOB-03"
    List<String> dependsOn();                    // for example ["JOB-02"]
    JobOutcome run(LocalDate businessDate);      // idempotent for the business date
}

// P1 job monitor, RWB-E1-056
UUID JobRunRecorder.start(String jobId, LocalDate businessDate, String instance);
void JobRunRecorder.finish(UUID runId, String status, Map<String, Object> counts);
Optional<JobRun> JobRunRecorder.lastSucceeded(String jobId, LocalDate businessDate);
```

**TimerScheduler.** JOB-05 is the Epic 1 implementation of the published TimerScheduler port of RWB-E1-028 (package `recovery.casewf.timers`): `schedule`, `cancel`, `pause` and `resume` write or change the timer row, and the 5-minute Quartz fire runs the check. Epic 3 replaces the implementation with Temporal durable timers and no caller changes (ADR-011). No Temporal schedule is registered in Epic 1 or Epic 2 (D-RCV-36 T2).

**Quartz configuration** (from the ACE pattern):

```properties
org.quartz.jobStore.class=org.springframework.scheduling.quartz.LocalDataSourceJobStore
org.quartz.jobStore.driverDelegateClass=org.quartz.impl.jdbcjobstore.PostgreSQLDelegate
org.quartz.jobStore.isClustered=true
org.quartz.jobStore.clusterCheckinInterval=20000
org.quartz.scheduler.instanceId=AUTO
```

## 13. Solution plan

**Package.** `recovery.casewf.scheduling` in the recovery module; run books in `recovery/docs/runbooks/JOB-03.md`, `JOB-04.md` and `JOB-05.md`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| BusinessDateJobRunner | Job | Quartz job marked `@DisallowConcurrentExecution` and `requestsRecovery`; runs a `BusinessDateJob` with the skip, dependency and run log steps |
| DailyJobTrigger | Listener | Consumes LoadCompleted and the JOB-02 completion; schedules JOB-03 and JOB-04 for the date |
| CatchUpOnStart | Service | On start, finds business dates with a passed load and no successful run; runs them in order up to the limit; alerts beyond it |
| DeadlineWatcher | Job | Cron at 07:00 Asia/Bangkok; alerts when JOB-03 has not succeeded for the business date |
| RecoveryJobRegistry | Service | Schedules JOB-03, JOB-04 and JOB-05 with their triggers and misfire instructions (JOB-05: do nothing); registers JOB-05 as the TimerScheduler implementation of RWB-E1-028 |
| RunBookCheck | Job | Build check that each scheduled job ID has a run book with the six headings: purpose, schedule, owner, failure signs, restart steps, escalation |
| BusinessDateJob | Published interface | The interface in section 12, implemented by the job bodies of RWB-E1-020, RWB-E1-011 and RWB-E1-028 |

**Database.** No new recovery table. Uses the `QRTZ_` tables of the ACE scheduler and the P1 job run log through `JobRunRecorder`.

**Configuration and reference data.** `jobs.catch-up.max-dates` = 5 (assumed; DL11), `jobs.allocation.deadline` = 07:00, `jobs.timer-check.cron` = `0 0/5 * * * ?`, all in the configuration service, loaded by the platform administrator. Job owners from batch.txt in each run book.

**Build steps**

1. Build `BusinessDateJobRunner` with the skip and dependency checks and the run log calls; test with a fake job body.
2. Build `RecoveryJobRegistry` and schedule the three jobs; prove JOB-05 does not overlap and that it is registered as the TimerScheduler implementation.
3. Build `DailyJobTrigger` on LoadCompleted and the JOB-02 completion.
4. Build `CatchUpOnStart` with the date order and the limit.
5. Build `DeadlineWatcher` and the alert through the job monitor.
6. Write the three run books and `RunBookCheck`.
7. Write the two-instance tests in section 16 with a controlled clock.
8. Add the architecture test of AC11 to the build and fail any job class that holds a case wait.

**Feature flag.** `rwb.p3.quartz-jobs`. Off: the three jobs are not scheduled and the job bodies can be run only through the rerun endpoint.

**Done when.** The tests in section 16 pass, and SIT shows one SUCCEEDED run of JOB-03 and JOB-04 per business date for five days in a row with JOB-03 complete by 07:00.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-030 | A job ran for a date after a missed run | {job} ran for {date} after a missed run. |
| MSG-P3-031 | A job waits on a dependency, misses its deadline, or has more missed dates than the catch-up limit | {job} for {date} has not completed: {reason}. |
| MSG-P4-002 | A role without Platform administration reads or reruns a job | You cannot {action} here. Your role does not include it. |

MSG-P3-030 and MSG-P3-031 are new (see Additions). They show on SCR-44 and in the operations channel.

## 15. Screens and states

SCR-44 Interface and job monitor, states Running, Failed and Complete: the platform administrator reads each run of JOB-03, JOB-04 and JOB-05 with its business date and status and reruns a failed run. No new screen in this story.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-007-01 | AC1, BR1 | System | Two instances, business date 2026-12-02 |
| TC-TE-007-02 | AC2, BR2, BR5 | System | Outage 04:30 to 09:40 on 2026-12-02 |
| TC-TE-007-03 | AC3, BR6, BR8 | System | JOB-03 fired twice for one date |
| TC-TE-007-04 | AC4, BR4 | System | JOB-05 run of 7 minutes |
| TC-TE-007-05 | AC5, BR5 | System | Three missed business dates |
| TC-TE-007-06 | AC6, BR5 | System | Seven missed business dates |
| TC-TE-007-07 | AC7, BR2 | System | JOB-02 failed for 2026-12-03, then succeeded at 08:10 |
| TC-TE-007-08 | AC8 | System | ACE-1 stopped during JOB-04 |
| TC-TE-007-09 | AC9, BR3 | System | JOB-03 not complete at 07:00 |
| TC-TE-007-10 | AC10, BR7 | System | Run book folder without JOB-04 |
| TC-TE-007-11 | Access | Access | RW-CASEOWN (no Platform administration right) calls `GET /admin/jobs`; refused with MSG-P4-002 |
| TC-TE-007-12 | AC11, BR9 | Build | Proposed job class "CaseReminderJob" that waits on a case; architecture test |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. Schedules, limits and deadlines come from the configuration service.
- No personal data in logs, tests, workflow history or prompts. Job logs, run books and alerts carry job IDs, dates and counts.
- No read of another module's tables; ACE data only through recovery.v_ace_* views. The job run log is written through the P1 interface; the Quartz tables are used only through the ACE scheduler API.
- A job body never decides its own business date from the clock; it takes the date it is given.
- No new Quartz job holds a case wait; case waits move to Temporal in Epic 3 (D-RCV-36 T1, T2; ADR-011).
- No Temporal schedule is registered in Epic 1 or Epic 2.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Business Requirements Epic 1, section 3.3; Program, section 5.3 | None (technical enabler) | All recovery processes | R-UNI-40 | TC-TE-007-01 to TC-TE-007-03, TC-TE-007-05 to TC-TE-007-07, TC-TE-007-09 |
| REQ-CWC-011 | Service levels held as data and a breach raises an event | Business Requirements Epic 1, section 3.3; Program, section 5.3 | None (technical enabler) | All recovery processes | R-UNI-30 | TC-TE-007-04, TC-TE-007-11, TC-TE-007-12 |
| REQ-RDF-007 | The case list reconciles daily to the ALS count | Business Requirements Epic 1, section 4; Program, sections 5.1 and 6.3 | None (technical enabler) | All recovery processes | CTL-01 | TC-TE-007-08, TC-TE-007-10 |

## 19. Out of scope

- The job bodies: allocation (RWB-E1-020), reconciliation (RWB-E1-011), timer check (RWB-E1-028).
- The COLLINS load and case creation jobs JOB-01 and JOB-02 (P1).
- Daily rebalancing JOB-06 (RWB-E1-030).
- The job monitor screen and the operations alert channel (RWB-E1-056).
- Temporal Schedules (Epic 3+): durable timers and case waits move to Temporal then (ADR-011).
