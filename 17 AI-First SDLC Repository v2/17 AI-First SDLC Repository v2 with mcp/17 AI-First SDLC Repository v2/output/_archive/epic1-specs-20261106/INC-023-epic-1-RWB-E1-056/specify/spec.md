# Technical Specification — RWB-E1-056 Run books and monitoring for every Epic 1 job

| Field | Value |
|---|---|
| Story | RWB-E1-056 — Run books and monitoring for every Epic 1 job |
| Epic / module | E1 / P2 Integration |
| RUN_ID | `INC-023-epic-1-RWB-E1-056` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 056 Run books and monitoring for every Epic 1 job v1.md`; REQ-DRI-007; BRD Epic 1 §3.2; BRD Program §5.2 |
| Upstream IDs | REQ-DRI-007; FEAT-DRI-18; R-UNI-40; DL11; RWB-E1-007; Spring Batch and Quartz (ACE pattern) |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Platform administrator; data steward; see `compliance-validation.md` |
## Change Scope Declaration
| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The platform administrator uses the Log Analytics workbook "Recovery jobs" and the admin endpoints; SCR-44 is Epic 2 and Epic 8. |
| Logic In Scope | `YES` — job catalog, run-book completeness check, job run events, last-run view, rerun from a failed step and idempotent rerun. |
| API In Scope | `YES` — one new E1 endpoint `GET /admin/scheduled-jobs`; the story reuses the P1 `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun`. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `job_catalog` (new); Spring Batch execution tables; Quartz jobs; `interface_run`; Log Analytics workbook; `POST /admin/jobs/{jobId}/rerun` (P1). |
| New Nodes Required | `YES` — `JobCatalogController`; `JobOperationsImpl`; `JobRunEventListener`; `JobCatalogRepository`; `JobCatalogEntry`; `RunbookCompletenessTest`; `RecoveryJobsWorkbook`; 13 run books. |
| Inherited Existing Behavior | File adapters and run rows (RWB-E1-007); Spring Batch and Quartz execution tables (ACE pattern); job endpoints (P1); Log Analytics; alert path. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage
| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every scheduled job has a run book, an alert and an owner. | SPEC-RWB-E1-056-001, SPEC-RWB-E1-056-002, SPEC-RWB-E1-056-011 | DIRECT | `job_catalog` row per job; run book file; alert rule. | COVERED |
| BR2 | A run book has six sections: purpose, schedule, owner, failure signs, restart steps, escalation. | SPEC-RWB-E1-056-002, SPEC-RWB-E1-056-003 | DIRECT | `RunbookCompletenessTest` checks the headings. | COVERED |
| BR3 | The owner of each job is the role named in the batch schedule. | SPEC-RWB-E1-056-001 | DIRECT | `owner_role` in the catalog row; role from the batch schedule. | COVERED |
| BR4 | Daily jobs restart in the daily timeline order: JOB-01, then JOB-02, 04, 07, 08, then JOB-03. | SPEC-RWB-E1-056-008 | DIRECT | Run book restart section states the order; the job dependency is not changed. | COVERED |
| BR5 | A rerun is idempotent for the job and business date. | SPEC-RWB-E1-056-010 | DIRECT | Job key; interface runs write DUPLICATE; the job's own key applies. | COVERED |
| BR6 | Owners, thresholds and paths are data rows, never code. | SPEC-RWB-E1-056-001 | DIRECT | Catalog columns; no literal in the job or controller. | COVERED |
| AC2 | JOB-01 fails at 05:20 on 2026-11-26; a rerun at 06:05 restarts from the failed step and completes at 06:25; JOB-02 runs after; no developer action. | SPEC-RWB-E1-056-008, SPEC-RWB-E1-056-009 | DIRECT | Spring Batch restart; run book steps. | COVERED |
| AC3 | Each of the 13 jobs shows last run, status and duration in the workbook; `GET /admin/jobs` returns the same. | SPEC-RWB-E1-056-005, SPEC-RWB-E1-056-006, SPEC-RWB-E1-056-012 | DIRECT | `rwb.job.run`; job repository read. | COVERED |
| AC5 | A rerun while JOB-03 runs returns 409 MSG-P2-006; JOB-03 continues. | SPEC-RWB-E1-056-009 | DIRECT | Running check before restart. | COVERED |
| AC6 | JOB-02 past its 45-minute threshold alerts the data steward and platform administrator; the job is not stopped. | SPEC-RWB-E1-056-011 | DIRECT | Alert rule; no kill. | COVERED |
| AC7 | A rerun of a completed JOB-01 for 2026-11-28 writes DUPLICATE runs and loads nothing. | SPEC-RWB-E1-056-010 | DIRECT | Interface-run idempotency. | COVERED |
| X1 | A job has no catalog row or run book, or a run book lacks a section. | SPEC-RWB-E1-056-003 | DIRECT | Build fails naming job and section; MSG-P2-005. | COVERED |
| X2 | A rerun is requested while the job runs. | SPEC-RWB-E1-056-009 | DIRECT | 409 MSG-P2-006; job continues. | COVERED |
| X3 | A job runs past its alert threshold. | SPEC-RWB-E1-056-011 | DIRECT | Alert; no stop; MSG-P2-004. | COVERED |
| X4 | A rerun of a job already completed for the date. | SPEC-RWB-E1-056-010 | DIRECT | DUPLICATE runs; nothing changes. | COVERED |
| X5 | A role without the right reruns a job. | SPEC-RWB-E1-056-013 | DIRECT | 403 MSG-P4-002. | COVERED |
> **AC cleanup (4 November 2026):** the development-process criteria removed from story §7 are not mapped here. The remaining acceptance criteria are those in the current story.

## User story intent interpretation
As a **platform administrator (RW-PLATADM)**, I want **a run book for every scheduled job (purpose, schedule, owner, failure signs, restart steps, escalation) and monitoring of each job's last run, status and duration**, so that **the operations team can restart any Epic 1 job without the developer**.

The story gives each Epic 1 job a catalog row with an owner, a run book path and alert thresholds, and adds a pipeline check that both exist and the run book has the six sections. Every job writes a structured run event at start and end; the workbook and the admin endpoint show the last run, status and duration; an alert fires on failure or on a run past its threshold. The platform administrator restarts from the failed step using the run book and the existing rerun endpoint. No screen is added.
## Entry trigger and preconditions
| Item | Value |
|---|---|
| Trigger | Every job run (start and end); pipeline on every pull request; alert rule evaluation; administrator rerun. |
| Preconditions | RWB-E1-007 done; Epic 1 jobs built or stubbed (JOB-01..05, 09..15, 17); Spring Batch and Quartz execution tables in the ACE database; RW-PLATADM in the environment; Log Analytics receives application logs. |
| Input | `job_catalog` rows; run book files; Spring Batch execution rows; `interface_run` rows; `rwb.job.run` events. |
| Output | Catalog entries; run books; last-run view; alerts; rerun result; DUPLICATE run rows on a repeat. |
| Feature flag | `rwb.integration.job-monitoring`. Off: no run event is written and the workbook shows no new run; rerun and catalog remain available. |
## Field-level behaviour matrix
| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `job_catalog` | `job_id` | Batch schedule | RW-PLATADM | `^JOB-[0-9]{2}$`; primary key |
| `job_catalog` | `job_name`, `schedule_text` | Batch schedule | RW-PLATADM | Required |
| `job_catalog` | `owner_role` | Batch schedule | RW-PLATADM | Role code from LOV-ROLE |
| `job_catalog` | `runbook_path` | `docs/operations/runbooks/<job ID>.md` | RW-PLATADM | File must exist with six sections |
| `job_catalog` | `expected_minutes`, `alert_after_minutes` | Batch schedule / DL11 | RW-PLATADM | Alert threshold at or after expected |
| `job_catalog` | `first_release` | Batch schedule | RW-PLATADM | `E1` for the 13 rows |
| Run book | six headings | `docs/operations/runbooks/` | Tech lead / platform administrator | Purpose, schedule, owner, failure signs, restart steps, escalation |
| `rwb.job.run` | `jobId`, `businessDate`, `status`, `duration` | Job listener | System writes | No personal data |
## Status-transition matrix
| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| — | Job starts | — | `STARTED` | `rwb.job.run` start event |
| `STARTED` | Job ends | No error | `COMPLETED` | End event with duration; workbook updates |
| `STARTED` | Job ends | Error | `FAILED` | End event; alert MSG-P2-004 |
| `STARTED` | Alert threshold passes | Still running | `RUNNING_OVER` | Alert; job continues |
| `FAILED` | Rerun | Not running | `STARTED` | Restart from the failed step |
| `COMPLETED` | Rerun for the same date | Key already complete | `DUPLICATE` | Interface runs DUPLICATE; nothing loaded |
| No case status change | — | — | — | This story does not touch `recovery_case` |
## Exceptional-case behaviour
| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Missing catalog row, run book or section | Pipeline fails naming job and section | MSG-P2-005 |
| X2 | Rerun while running | Refused; job continues | 409 MSG-P2-006 |
| X3 | Job past alert threshold | Alert owner role and RW-PLATADM; no stop | MSG-P2-004 |
| X4 | Rerun of a completed job | DUPLICATE runs; nothing changes | None |
| X5 | Role without Platform administration U reruns | 403; nothing changes | MSG-P4-002 |
## API change assessment
| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoint | `GET /api/recovery/v1/admin/scheduled-jobs` (Platform administration R) returning `JobCatalogEntry`. |
| Reused endpoints | `GET /api/recovery/v1/admin/jobs` (P1, R); `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (P1, U). |
| Contract delta | New catalog response: `jobId`, `jobName`, `ownerRole`, `schedule`, `runbookPath`, `expectedMinutes`, `alertAfterMinutes`, `firstRelease`. No change to the P1 operations. |
| Backward compatibility | New endpoint; existing operations unchanged. |
| Authorization | Platform administration R for the catalog; U for the rerun; 403 MSG-P4-002. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P2-006; 503. |
| Versioning | No version change; the new operation is first in E1. |
## Unit Test Applicability
| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; the workbook and admin endpoints are the surface. | Existing front-end tests stay green; no new front-end test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR6; SPEC-RWB-E1-056-001..018 | New catalog entity/repository, listener, operations service, completeness test and controller. | Unit tests cover catalog validation, six-section check, last-run mapping, restart, running check, idempotent rerun and alert threshold. |
## Detailed design
### Components
| Component | Type | Responsibility |
|---|---|---|
| `JobCatalogController` | Controller | `GET /admin/scheduled-jobs`; maps errors to Problem responses. |
| `JobOperationsImpl` | Published interface | Catalog, last run from the Spring Batch repository, restart through `JobOperator.restart`. |
| `JobRunEventListener` | Listener | Spring Batch `JobExecutionListener` writing `rwb.job.run` at start and end. |
| `JobCatalogRepository` | Repository | `job_catalog` only. |
| `JobCatalogEntry` | Entity | JPA entity with the standard columns. |
| `RunbookCompletenessTest` | Test | Finds every Quartz `JobDetail` and Spring Batch job bean; checks the catalog row and six headings. |
| `RecoveryJobsWorkbook` | Rule table | Log Analytics workbook and alert rules for FAILED and over-threshold runs. |

### Data and migration
Flyway `V2026_11_56__p2_job_catalog.sql` creates `job_catalog` (primary key `job_id`, check `^JOB-[0-9]{2}$`) and inserts the 13 Epic 1 rows from the batch schedule. No other table. Reads Spring Batch execution tables through the framework repository; reads `interface_run` for file-job status.

### Rules
1. Every Quartz job and Spring Batch job in the service has a catalog row and a run book with the six headings; a missing item fails the build (, ).
2. Every job writes `rwb.job.run` at start and end with job ID, business date, status and duration.
3. `GET /admin/jobs` and the workbook show the same last run, status, start and end (AC3).
4. A rerun restarts from the failed step through `JobOperator.restart`; if the job is running, return 409 (AC5).
5. A rerun of a completed job for the same business date is idempotent: interface runs write DUPLICATE and nothing is loaded (AC7).
6. A FAILED run or a run past `alert_after_minutes` emails `owner_role` and RW-PLATADM with MSG-P2-004; the job is not stopped (AC6).
7. Daily jobs restart in the timeline order JOB-01, JOB-02, JOB-04, JOB-07, JOB-08, JOB-03; the run book states it.

### Transaction and events
The run event is written at the start and end of each execution. The rerun and the DUPLICATE outcome are one transaction per job key. No case event is published. The catalog is read-only at run time.

### Security and authority
| Actor | Right | Scope |
|---|---|---|
| RW-PLATADM | Platform administration U; maintains catalog; reruns | All |
| RW-DATASTEW | Platform administration R; alerts for JOB-01/02/04/09/13 | All |
| RW-TEAMMGR | Alerts for JOB-03/06 by email; no endpoint right | Team |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Platform administration R | All |

Run books name roles and service identities, never a person.

### Observability and operations
- Workbook "Recovery jobs": last run, status, duration, business date, record counts.
- Alerts: FAILED, over threshold, no run in the expected window.
- Metrics: job duration, failure count, over-threshold count.
- Run books: 13 files under `docs/operations/runbooks/`, six sections each.

### Performance
- The workbook queries the job repository; `GET /admin/jobs` reads the same rows.
- No numeric target beyond the job's own expected duration; alert threshold is data (1.5× expected, DL11).
- The completeness test runs in the pipeline; no runtime cost.

### Feature flag and rollback
`rwb.integration.job-monitoring`. Off: no run event and no new workbook row; the catalog and rerun remain. Rollback: turn the flag off; the migration is additive.

### No UI change
No screen. The platform administrator uses the workbook and the admin endpoints. SCR-44 shows the same data from Epic 2.
## Test scenarios
| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-056-01 | BR1, BR2 | System | 13 catalog rows and run books | Every job has a file with six sections |
| TC-E1-056-02 | AC2, BR4 | System | JOB-01 fails on the INT-07 step | Rerun from failed step; COMPLETED 06:25; JOB-02 after; no developer action |
| TC-E1-056-03 | AC3 | System | One run of each job in SIT | Workbook and endpoint agree on last run, status, start/end |
| TC-E1-056-04 | BR2 | System | Run book without Escalation | Build fails; MSG-P2-005 names JOB-12 and Escalation |
| TC-E1-056-05 | AC5 | System | JOB-03 running | 409 MSG-P2-006; JOB-03 continues |
| TC-E1-056-06 | AC6, BR3 | System | JOB-02 slowed past 45 minutes | Alert to data steward and platform administrator; no stop |
| TC-E1-056-07 | AC7, BR5 | System | JOB-01 rerun for a completed date | DUPLICATE runs; no second load |
| TC-E1-056-08 | X5 | Security | RW-CASEOWN calls rerun | 403; MSG-P4-002 |
| TC-E1-056-09 | BR1, BR2 | Unit | Catalog with a missing section; restart with a running job | Test fails; 409 path |
## Guardrails
- No business value in code: owners, thresholds and paths are catalog rows.
- No personal data in logs, tests or prompts; job events hold job IDs, dates, counts and durations only.
- No read of another module's tables; the Spring Batch tables are read through the framework job repository.
- A run book names roles and service identities, never a person.
## Out of scope
- The SCR-44 screen: Epic 2; full monitor in Epic 8.
- Incident handling after a job failure: FEAT-ADM-12, Epic 8.
- The feeds on Control-M and ADF: RWB-E1-051.
## Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner | Program §5.2; Epic 1 §3.2 | FEAT-DRI-18 | All recovery processes | R-UNI-40 | TC-E1-056-01..07, 09 |
## Clarification Log
| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | §3; SPEC-001 | The 13 Epic 1 jobs are assumed from the batch schedule. | A missing or extra job changes the catalog. | Load the 13 rows: JOB-01..05, 09..15, 17; `first_release` records E1. | RESOLVED | SPEC-001 |
| CLAR-002 | SPEC-001 | The story mentions jobs and services, but `job_catalog` is job-only. | A separate service table would be a new entity. | The 13 scheduled jobs are the catalog rows; a service is covered through the job that runs it. | RESOLVED | SPEC-001 |
| CLAR-003 | AC6; SPEC-011 | The 45-minute JOB-02 threshold is assumed. | Determines when the alert fires. | 45 minutes (DL11); `alert_after_minutes` is data. | RESOLVED | SPEC-011 |
| CLAR-004 | §13; SPEC-011 | The default threshold is 1.5× expected duration. | Determines alert timing for other jobs. | Use 1.5× expected as the default; each row can override. | RESOLVED | SPEC-011 |
| CLAR-005 | BR5; SPEC-010 | How is a non-interface job rerun idempotent? | A generic rule is needed. | The job key is job ID + business date; interface jobs write DUPLICATE, other jobs use their own key and change nothing. | RESOLVED | SPEC-010 |
| CLAR-006 | §12; SPEC-008 | Does the rerun endpoint restart the bank scheduler job? | Two different systems. | No — it restarts the Workbench job from its failed step; the bank scheduler is restarted per RWB-E1-051. | RESOLVED | SPEC-008 |

`CLARIFICATION_STATUS: RESOLVED` — all six items are answered from the story, the batch schedule or DL11.
## Status reporting
```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend operations story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New job catalog, run-book completeness check, run monitoring and one admin endpoint; existing P1 job endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new catalog and monitoring, one new endpoint]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 5 acceptance criteria, 5 exception paths and 7 state transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
