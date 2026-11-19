# Technical Specification — RWB-TE-007 Scheduled jobs on Quartz

| Field | Value |
|---|---|
| Story | RWB-TE-007 — Scheduled jobs on Quartz |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-026-epic-1-RWB-TE-007` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-005, FR-RWB-007); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 007 Scheduled jobs on Quartz v1.md` |
| Upstream IDs | BRD-RWB-003; FR-RWB-005, FR-RWB-007; REQ-CWC-007, REQ-CWC-011, REQ-RDF-007; US-RWB-TE-007; CTX-FEATURE-003; NFR-013, NFR-067, NFR-068; R-UNI-40 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — SCR-44 Interface and job monitor already exists and only displays runs. No screen, component, route, label or state is added. |
| Logic In Scope | `YES` — clustered scheduling, one run per business date, dependency, skip, catch-up, deadline alert, recovery and run-book gate. |
| API In Scope | `NO` — no new or changed contract. The story reuses `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` (P1). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | ACE Quartz scheduler and `QRTZ_` tables; P1 job monitor and job run log; SCR-44; JOB-03, JOB-04 and JOB-05 bodies. |
| New Nodes Required | `YES` — `BusinessDateJobRunner`, `DailyJobTrigger`, `CatchUpOnStart`, `DeadlineWatcher`, `RecoveryJobRegistry`, `RunBookCheck`, `BusinessDateJob` interface, three run books. |
| Inherited Existing Behavior | RWB-E1-044 migrations; RWB-E1-056 job monitor and alert channel; RWB-E1-020 allocation; RWB-E1-011 reconciliation; RWB-E1-028 timer check; JOB-01 and JOB-02 (P1). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Each daily job runs once per business date, on one instance. | SPEC-RWB-TE-007-001, SPEC-RWB-TE-007-002 | DIRECT | Clustered JDBC job store; `@DisallowConcurrentExecution`; skip on a successful run. | COVERED |
| BR2 | JOB-03 and JOB-04 run after JOB-02 succeeds for the same business date. | SPEC-RWB-TE-007-002, SPEC-RWB-TE-007-003 | DIRECT | Dependency check; WAITING when not met; JOB-02 completion re-triggers. | COVERED |
| BR3 | JOB-03 completes by 07:00; a later completion raises an alert. | SPEC-RWB-TE-007-006 | DIRECT | `DeadlineWatcher` at 07:00 Asia/Bangkok; alert by 07:15. | COVERED |
| BR4 | JOB-05 runs every 5 minutes; a missed fire is not repeated; the next run picks up missed timers. | SPEC-RWB-TE-007-004 | DIRECT | Cron `0 0/5 * * * ?`; misfire instruction do nothing. | COVERED |
| BR5 | After an outage, each missed business date runs in date order, up to the catch-up limit. | SPEC-RWB-TE-007-005 | DIRECT | `jobs.catch-up.max-dates` = 5 (assumed; DL11); alert beyond. | COVERED |
| BR6 | A run for a job and business date that already succeeded has no further effect. | SPEC-RWB-TE-007-002, SPEC-RWB-TE-007-008 | DIRECT | Run-log lookup before the body; idempotent bodies. | COVERED |
| BR7 | Every scheduled job has a run book, monitoring and an alert to the operations channel. | SPEC-RWB-TE-007-007 | DIRECT | `RunBookCheck` fails the build on a missing run book. | COVERED |
| BR8 | Job bodies are idempotent for their business date. | SPEC-RWB-TE-007-008 | DIRECT | Body contract; the runner still guards the date. | COVERED |
| AC1 | JOB-03 runs once on one instance and logs job, date, instance, start, end, status and counts. | SPEC-RWB-TE-007-001, SPEC-RWB-TE-007-002, SPEC-RWB-TE-007-009 | DIRECT | Two-instance fixture. | COVERED |
| AC2 | After an outage, JOB-03 and JOB-04 run for the missed date and log MSG-P3-030. | SPEC-RWB-TE-007-005 | DIRECT | Restart at 09:40 for 2026-12-02. | COVERED |
| AC3 | A repeated fire allocates nothing again and records a skip. | SPEC-RWB-TE-007-002, SPEC-RWB-TE-007-008 | DIRECT | Run-log skip. | COVERED |
| AC4 | A 7-minute JOB-05 run delays the next fire; no two runs overlap. | SPEC-RWB-TE-007-004 | DIRECT | `@DisallowConcurrentExecution`. | COVERED |
| AC5 | Three missed dates run in date order. | SPEC-RWB-TE-007-005 | DIRECT | 2, 3, 4 December. | COVERED |
| AC6 | Seven missed dates exceed the limit; no automatic catch-up; alert names the dates. | SPEC-RWB-TE-007-005 | DIRECT | MSG-P3-031. | COVERED |
| AC7 | JOB-02 failure makes JOB-03 WAITING; JOB-02 success at 08:10 releases it. | SPEC-RWB-TE-007-002, SPEC-RWB-TE-007-003 | DIRECT | MSG-P3-031 names JOB-02. | COVERED |
| AC8 | ACE-1 stops during JOB-04; ACE-2 reruns it within 20 seconds; one FAILED and one SUCCEEDED. | SPEC-RWB-TE-007-010 | DIRECT | Quartz recovery; cluster check-in 20 s. | COVERED |
| AC9 | JOB-03 not complete at 07:00 alerts the operations channel by 07:15. | SPEC-RWB-TE-007-006 | DIRECT | MSG-P3-031 names job, date and 07:00. | COVERED |
| X1..X7 | Exceptional paths in the table below map to SPEC-002..010. | SPEC-RWB-TE-007-002..010 | DIRECT | Skip, overlap, catch-up limit, dependency, instance loss, late JOB-03, missing run book. | COVERED |

> **AC cleanup (4 November 2026):** the development-process criteria removed from story §7 are not mapped here. The remaining acceptance criteria are those in the current story.

## User story intent interpretation

As a **platform administrator (RW-PLATADM)**, I want **the timer check, the morning allocation run and the daily reconciliation run as Quartz jobs with a run book each**, so that **scheduled work runs once, on time and visibly, and a missed run is caught up for its business date**.

The story is the scheduling spine for Epic 1. It does not implement the job bodies; it makes them run once per business date on the clustered ACE scheduler, wait for their dependency, catch up after an outage, alert when late, and carry a run book. The platform administrator reads and reruns them on SCR-44.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `LoadCompleted` (EV-26) and JOB-02 completion for JOB-03/JOB-04; cron `0 0/5 * * * ?` Asia/Bangkok for JOB-05; service start for catch-up; 07:00 for the deadline watcher. |
| Preconditions | RWB-E1-044 done; RWB-E1-056 job monitor done; ACE Quartz runs with a clustered JDBC job store; JOB-01 publishes LoadCompleted with the business date; JOB-02 records its run; the three job bodies exist; `jobs.catch-up.max-dates` = 5 (assumed; DL11) and the 07:00 deadline are in the configuration service. |
| Input | Business date, job ID, dependency list, run log, job body outcome. |
| Output | One run record per job and date; status and counts; catch-up runs; alerts; run books. |
| Feature flag | `rwb.p3.quartz-jobs`. Off: the three jobs are not scheduled; bodies can be run only through the rerun endpoint. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| Job run record | `jobId`, `businessDate`, `instance` | Runner | System-written | One successful run per job and business date. |
| Job run record | `status` | Runner | STARTED → SUCCEEDED / FAILED / WAITING / SKIPPED | WAITING and SKIPPED are terminal for that fire. |
| Job run record | `startedAt`, `endedAt`, `counts` | Runner / body | System-written | Counts carry case counts only; no PII. |
| `QRTZ_` tables | job, trigger, lock, fire state | Quartz | Tool-managed | ACE common module owns them; the recovery module uses the scheduler API only. |
| Run book | six headings | Author | Versioned in the repository | Purpose, schedule, owner, failure signs, restart steps, escalation. |
| Configuration | `jobs.catch-up.max-dates`, `jobs.allocation.deadline`, `jobs.timer-check.cron` | RWB-E1-042 | Data | No schedule or limit in code. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Fire | Dependency met, no successful run | STARTED | Lock taken; run record written. |
| STARTED | Body returns | No error | SUCCEEDED | Counts and end time recorded. |
| STARTED | Body throws | Error | FAILED | Error recorded; alert; recovery on another instance. |
| None | Fire | JOB-02 not succeeded for the date | WAITING | Run record WAITING; released by JOB-02 completion. |
| None | Fire | A successful run already exists | SKIPPED | No body call; skip recorded. |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | A successful run exists for the job and date | Skip; no body call | None |
| X2 | JOB-05 still running when the next fire is due | Next fire waits; no overlap | None |
| X3 | More missed dates than the limit | No automatic catch-up; alert names dates | MSG-P3-031 |
| X4 | JOB-02 not succeeded for the date | JOB-03 WAITING; released on JOB-02 success | MSG-P3-031 |
| X5 | Instance running a job stops | Another instance recovers and reruns for the date | None |
| X6 | JOB-03 not succeeded by 07:00 | Alert to operations by 07:15 | MSG-P3-031 |
| X7 | A scheduled job has no run book | Build fails naming the job | Build output |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs` (list runs); `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (rerun a FAILED or WAITING run). |
| Contract delta | None. `Job` already carries id, type, businessDate, status, startedAt, endedAt and checks; the rerun returns the run. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R to read; U to rerun. 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-GEN-004 when the run already succeeded; 503. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | SCR-44 is an existing screen; no component, route, state or label changes. | Existing SCR-44 tests remain green. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-005, FR-RWB-007; SPEC-RWB-TE-007-001..012 | New runner, trigger, catch-up, deadline watcher, registry and build check. | Positive, negative, boundary and error-path tests: once, skip, dependency, catch-up, limit, overlap, recovery, late alert, missing run book. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `BusinessDateJobRunner` | Job | Quartz job marked `@DisallowConcurrentExecution` and `requestsRecovery`; runs a `BusinessDateJob` with skip, dependency and run-log steps. |
| `DailyJobTrigger` | Listener | Consumes `LoadCompleted` and JOB-02 completion; schedules JOB-03 and JOB-04 for the date. |
| `CatchUpOnStart` | Service | On start, finds dates with a passed load and no successful run; runs them in order up to the limit; alerts beyond. |
| `DeadlineWatcher` | Job | Cron at 07:00 Asia/Bangkok; alerts when JOB-03 has not succeeded. |
| `RecoveryJobRegistry` | Service | Schedules JOB-03, JOB-04 and JOB-05 with triggers and misfire instructions (JOB-05: do nothing). |
| `RunBookCheck` | Build job | Fails when a scheduled job ID has no run book with the six headings. |
| `BusinessDateJob` | Published interface | `jobId`, `dependsOn`, `run(businessDate)`. |

### Package and boundaries

`recovery.casewf.scheduling` in the recovery module; run books in
`recovery/docs/runbooks/JOB-03.md`, `JOB-04.md` and `JOB-05.md`. The job run log is written through
the P1 `JobRunRecorder`; the `QRTZ_` tables are used only through the ACE scheduler API.

### Scheduling and dependency

- JOB-03 and JOB-04 are triggered by `LoadCompleted` and by JOB-02 completion for the same date.
- The runner takes the cluster lock, checks the run log for a successful run, checks `dependsOn`,
  then records STARTED, runs the body and records SUCCEEDED or FAILED with counts.
- If JOB-02 has not succeeded, the runner records WAITING and stops; JOB-02 completion fires the job
  again.
- JOB-05 runs on cron `0 0/5 * * * ?`; a missed fire is not repeated and the next run picks up missed
  timers.

### Catch-up and recovery

- On service start, `CatchUpOnStart` finds business dates with a passed COLLINS load and no successful
  JOB-03 or JOB-04 run.
- It runs them in ascending date order, up to `jobs.catch-up.max-dates` (5). Beyond the limit it starts
  nothing automatically and alerts with the dates.
- Quartz `requestsRecovery` and the 20-second cluster check-in let another instance recover a job whose
  instance stopped; the run log shows the failed run and the successful recovery.

### Deadline and run books

- `DeadlineWatcher` runs at 07:00 Asia/Bangkok and alerts if JOB-03 has not succeeded for the current
  business date; the alert must reach the operations channel by 07:15.
- Every scheduled job has a run book with purpose, schedule, owner, failure signs, restart steps and
  escalation. `RunBookCheck` fails the build when one is missing.

### Events and transaction

The job bodies publish their own events (`CaseAllocated`, `CaseAllocationFailed`, `TimerDue`,
`TimerBreached`). The runner itself publishes none. Each run record is written in its own short
transaction; the job body owns its data transaction.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-PLATADM | Platform administration CRUD; reads and reruns | All |
| RW-DATASTEW | Platform administration R; owns JOB-04 | All |
| RW-TEAMMGR | Owns JOB-03 per batch.txt; receives the allocation summary | Team |
| SY-CASEWF | Runs JOB-03 and JOB-05 | All |
| SY-DATALOAD | Supplies JOB-04 inputs from COLLINS | All |

A role without Platform administration R receives 403 MSG-P4-002 on the job endpoints.

### Observability and operations

- SCR-44: each run with job, business date, instance, status, start/end and counts.
- Metrics: runs, skips, waits, failures, duration, catch-up count, deadline breaches.
- Alerts: JOB-03 late, job failed, catch-up limit exceeded, dependency not met.
- Run books are the operations procedure; they name roles, never people.

### Performance

- JOB-03 must complete by 07:00 (NFR-013); the body target is in RWB-E1-020.
- The runner adds one run-log read, one lock and two run-log writes per fire.
- JOB-05 runs every 5 minutes; a 7-minute run delays the next fire rather than overlapping.

### Feature flag and rollback

- `rwb.p3.quartz-jobs`: off means the three jobs are not scheduled and bodies run only through the
  rerun endpoint.
- Rollback: turn the flag off; redeploy the previous tag. No schema change is involved.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-007-01 | AC1, BR1 | System | Two instances, 2026-12-02 | JOB-03 once; run log complete |
| TC-TE-007-02 | AC2, BR2, BR5 | System | Outage 04:30–09:40 | JOB-03 and JOB-04 for the date; MSG-P3-030 |
| TC-TE-007-03 | AC3, BR6, BR8 | System | JOB-03 fired twice | No second allocation; skip recorded |
| TC-TE-007-04 | AC4, BR4 | System | JOB-05 run of 7 minutes | 10:05 waits; no overlap |
| TC-TE-007-05 | AC5, BR5 | System | Three missed dates | Runs 2, 3, 4 December in order |
| TC-TE-007-06 | AC6, BR5 | System | Seven missed dates | No catch-up; MSG-P3-031 names dates |
| TC-TE-007-07 | AC7, BR2 | System | JOB-02 fails, then succeeds 08:10 | WAITING then runs for the date |
| TC-TE-007-08 | AC8 | System | ACE-1 stops during JOB-04 | ACE-2 recovers; FAILED then SUCCEEDED |
| TC-TE-007-09 | AC9, BR3 | System | JOB-03 not done at 07:00 | Alert by 07:15; MSG-P3-031 |
| TC-TE-007-10 | BR7 | System | Run book folder without JOB-04 | Build fails naming JOB-04 |
| TC-TE-007-11 | Authority | Security | RW-CASEOWN calls `GET /admin/jobs` | 403; MSG-P4-002 |
| TC-TE-007-12 | BR6 | Unit | Rerun of a SUCCEEDED run | 409; nothing runs |

## Guardrails and out of scope

- No business value in code. Schedules, limits and deadlines come from the configuration service.
- No personal data in job logs, run books, alerts, tests or prompts. Logs carry job IDs, dates and
  counts.
- The job run log is written through the P1 interface; the Quartz tables are used only through the ACE
  scheduler API.
- A job body never decides its own business date from the clock; it takes the date it is given.
- Out of scope: the job bodies (RWB-E1-020, RWB-E1-011, RWB-E1-028); JOB-01 and JOB-02 (P1); daily
  rebalancing JOB-06 (RWB-E1-030); the job monitor screen and alert channel (RWB-E1-056).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR5, X3; SPEC-005 | Is the catch-up limit 5? | Determines how many dates run after an outage. | Yes, `jobs.catch-up.max-dates` = 5 (assumed; DL11); the test uses 7 to prove the limit. | RESOLVED | SPEC-005 |
| CLAR-002 | BR2, flow 1; SPEC-003 | Does `LoadCompleted` alone trigger JOB-03, or only JOB-02 completion? | Double trigger risk. | Both trigger; the dependency check makes the first WAITING until JOB-02 succeeds. The run is idempotent. | RESOLVED | SPEC-003 |
| CLAR-003 | BR4, AC4; SPEC-004 | What is the misfire instruction for JOB-05? | A repeated fire could double-process timers. | Do nothing; the next run picks up missed timers. | RESOLVED | SPEC-004 |
| CLAR-004 | AC8; SPEC-010 | How quickly must another instance recover a job? | Recovery target. | Within the Quartz cluster check-in interval of 20 seconds. | RESOLVED | SPEC-010 |
| CLAR-005 | AC9; SPEC-006 | Which timezone applies to 07:00? | Alert timing. | Asia/Bangkok, as the batch timeline. | RESOLVED | SPEC-006 |
| CLAR-006 | Contract; SPEC-009 | Does a rerun of a succeeded run do anything? | Idempotency. | No; it returns 409 MSG-GEN-004 and runs nothing. | RESOLVED | SPEC-009 |
| CLAR-007 | §10; SPEC-007 | Who owns each job? | Run-book content and escalation. | JOB-03 RW-TEAMMGR, JOB-04 RW-DATASTEW, JOB-05 the platform administrator; batch.txt is the source. | RESOLVED | SPEC-007 |
| CLAR-008 | §13; SPEC-012 | Are the schedule values data? | Hard-coding risk. | Yes; `jobs.timer-check.cron`, `jobs.allocation.deadline` and the catch-up limit are configuration entries. | RESOLVED | SPEC-012 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the batch design or the
ACE scheduler pattern. No item changes a business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend scheduling story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New clustered Quartz scheduling capability for three jobs; no UI or API contract change; existing job monitor endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: scheduling, catch-up and alerting with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 9 acceptance criteria, 7 exception paths and 5 run states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
