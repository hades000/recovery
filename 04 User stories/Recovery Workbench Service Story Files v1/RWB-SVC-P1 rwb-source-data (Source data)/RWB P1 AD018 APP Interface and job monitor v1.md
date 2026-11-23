# RWB-P1-AD018-APP Interface and job monitor

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-AD018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1069-APP |
| Depends on (build) | RWB-P1-AD018-CON, RWB-PLT-N001-CON, RWB-P1-E1069-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | RWB-P1-AD018-OPS, RWB-PLT-E1056-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-018 for rwb-source-data. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **every Workbench job and outbound action with its status, business date, duration and checks, and the last complete ACE business date per source beside it, served by rwb-source-data from its own schema behind its own base `/api/recovery/source-data/v1`**, so that **a failed job is found and rerun the same morning and a late ACE batch is not mistaken for a failed job**.

The monitor keeps the legacy intent and changes only where it sits: the catalogue and the run record are rows of `rwb_source_data` (DP-13), the ACE business date is read through the service's own `v_ace_*` read path (DP-05), and the screen is reached through the gateway-bff composite route (DP-19). No ACE batch is started, stopped or rerun from the Workbench: a dependent job waits.

### 2. Business rationale

The legacy screen was one read across three live tables of the single schema. After the split, the job catalogue, the run record and the freshness stamp have one owner each, and the read must not reach into another service's schema (DP-01). This story therefore serves the same screen from the service that owns the catalogue and the run record, and it takes the ACE business date only from `v_ace_batch_status`, never from a row count, a file or a view's `data_as_of` (BR-P1-014-2, FSD A2.14).

Two operational failures are the reason the screen exists. A failed job that is not seen before 09:00 delays the case list for the whole bank. A late ACE batch that is shown as a failed Workbench job invites the operator to rerun work that never started, and to rerun an ACE feed the Workbench does not own: the dependent run is recorded **WAITING** and is not rerun (NFR-015, legacy guardrail). The run record keeps both runs of a rerun, so the morning's second attempt is evidence and not an overwrite (legacy AC2).

The catalogue itself is data, not code: the Epic 1 baseline is loaded as rows by RWB-PLT-E1056-OPS, so a new job or a changed expected duration needs no release of this story (NFR-067, NFR-068).

### 3. Preconditions

- RWB-P1-AD018-CON is published: the `Job` and `DataProductFreshness` resources, the three operations, the error envelope, the 409 conditions, the Idempotency-Key rule and the fakes.
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-44 (DP-19). This story fixes only the answers rwb-source-data returns.
- RWB-P1-E1069-APP is done: the read path over `recovery.v_ace_*` and the grant, so `v_ace_batch_status` is readable by the service login and nothing in `public` is (DP-05). The view is Section B of RWB-ACE-001 (OQ-P1-01); until it lands every source reads as unknown and no run starts on its own.
- RWB-P1-E1015-APP publishes the freshness stamp in `data_product_load` and raises `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1`; this story reads the stamp and never writes it.
- The job catalogue rows are loaded as data by RWB-PLT-E1056-OPS (its 16-row Epic 1 baseline); this story reads them and holds no job name, cadence or threshold in code.
- The run record has no table in the logical model: the catalogue carries no run column and `load_run` left with the inbound load. Its shape is Not specified in the source documents (GAP-2162; ASM-3464).
- The outbound actions of the screen are produced by rwb-integration; no operation of that service is listed as a dependency of this story (GAP-2162; ASM-3465) and AC1 is proved against its contract mock.
- The Platform administration right is taken from the platform session (ACE Common sign-in and access checks, INT-34); the rwb-access authorise contract is not claimed here (GAP-2162; ASM-3466).
- The login is the rwb-source-data login (DP-02): one login, one pool, grants on schema `rwb_source_data` only.

### 4. Flow

1. A catalogued job starts, on `AceDataReady` processed in-service or on a rerun request; the job runner opens a run row with `job_id`, `business_date`, `run_no` 1 and status PENDING.
2. The runner reads `v_ace_batch_status` for the source systems of the job and the requested business date; when no source row is COMPLETE the run is set **WAITING** with MSG-P1-001 and the job is not started.
3. The runner sets the run RUNNING with `started_at` and hands the work to the owning job of the service; each check writes its code, its result and its count against the run.
4. On the last check the runner sets the run COMPLETE with `finished_at` and the duration; an error sets it FAILED and keeps the failed check, its message ID and the count reached.
5. `JobsController` serves `GET /api/recovery/source-data/v1/admin/jobs` from the catalogue joined to the latest run per job and business date, and adds the last complete business date of each source from `v_ace_batch_status`.
6. `JobsController` serves `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun`: it checks the Platform administration U right, that the job exists, that no run of the job is RUNNING, and that the business date is complete in `v_ace_batch_status`; otherwise 409.
7. A permitted rerun writes a **new** run row with `run_no` + 1 and the Idempotency-Key of the request; the earlier row is unchanged, so both runs are in the run log.
8. `FreshnessController` serves `GET /api/recovery/source-data/v1/data-products/freshness` from `data_product_load`, with the business date, the status LOADED or STALE and the ACE completion time of the stamp.
9. A STALE product carries MSG-P1-001 with its last complete ACE date; the monitor shows it beside the jobs rather than as a job failure.
10. No operation of this service starts, stops or reruns an ACE batch; the service holds no ACE run path and no credential on `public`.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The job code is unknown | 404 with the error envelope; no partial job list | MSG-GEN-001 | Contract test of RWB-P1-AD018-CON |
| X2 | A rerun is asked while a run of the job is RUNNING | 409; no second run row is written | None | AC2, contract test |
| X3 | The business date is not complete in `v_ace_batch_status` | 409 with MSG-P1-001 for the source; the run stays WAITING | MSG-P1-001 | AC1, AC2 |
| X4 | The caller holds Platform administration R and not U | 403; nothing is written and no run is created | MSG-P4-002 | TC-AD-018-04 |
| X5 | `v_ace_batch_status` does not answer | The last complete business date is shown as unknown and never as today; the job list still answers | None | AC1 |
| X6 | The run row cannot be written at start | The job is not started; the failure is returned, never hidden behind a started run | None | AC2 |
| X7 | A freshness stamp is missing for a product | The product shows STALE with no business date and MSG-P1-001, never "fresh" | MSG-P1-001 | AC1 |
| X8 | The rwb-integration mock answers late or fails | The outbound columns of the row are empty with their own marker; the job columns still answer | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against its own contract baseline, the platform route and the ACE read path of its own service; builds nothing against rwb-integration |
| Negotiable | Cadences, expected durations and thresholds are catalogue and values rows; the story fixes the behaviour |
| Valuable | A failed job is found before the working day and a late ACE batch is not chased as a failed job |
| Estimable | Two controllers, one runner hook, one run-log table, one Flyway step, three reads and their tests |
| Small | Fits one sprint with its tests |
| Testable | Both owned criteria have a test case; the cross-service compose and the late-batch journey are proved by RWB-ITG-AD018-ITG |

### 7. Acceptance criteria

```gherkin
Feature: Interface and job monitor

  Background:
    Given the job catalogue rows of the Epic 1 baseline are loaded as data
    Given the base is /api/recovery/source-data/v1 and the login is the rwb-source-data login
    Given v_ace_batch_status is read through the service's own v_ace_* read path

  Scenario: AC1 Workbench jobs and their ACE date (legacy RWB-AD-018 AC1)
    Given the jobs of the job catalog and the outbound actions for 2026-11-30
    Given the rwb-integration contract mock returns the outbound actions for 2026-11-30 with their status, business date, duration and the result of each check
    When I open the monitor
    Then each shows its job ID, business date, status, duration and the result of each check
    And each job that reads ACE shows the last complete business date of its source from v_ace_batch_status

  Scenario: AC2 Rerun a Workbench job (legacy RWB-AD-018 AC2)
    Given a failed Workbench job
    Given v_ace_batch_status shows the business date of that job complete for its source
    When I rerun it from its run book after the cause is fixed
    Then the job runs again and both runs are in the job log
```

**Note.** The two criteria are the legacy ones with their values unchanged, each carrying its origin tag. The added Givens stand in for the two answers rwb-source-data does not produce itself: the outbound actions of rwb-integration, taken from its contract mock (GAP-2162; ASM-3465), and the ACE batch row of `v_ace_batch_status`, read through the service's own view path (DP-05). "The job log" of AC2 is the run log of `rwb_source_data` in the target: one row per run, so a rerun adds a row and changes none (GAP-2162; ASM-3464). Legacy AC3, the late ACE batch that is recorded WAITING and shown STALE with MSG-P1-001, is owned by RWB-ITG-AD018-ITG and is proved there across the two services.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The monitor lists each catalogued Workbench job with its latest run: job ID, business date, status, duration and the result of each check | RWB-AD-018 AC1; FSD A2.12 |
| BR2 | Each job that reads ACE shows the last complete business date of its source, from `v_ace_batch_status` and from nothing else | FSD A2.14; BR-P1-014-2 |
| BR3 | A job whose source batch is not complete for the business date is recorded WAITING, is not started and is not rerun | RWB-AD-018 AC3 and guardrail; NFR-015 |
| BR4 | A rerun is allowed only on a failed job, only after the cause is fixed, and only from its run book; both runs stay in the run log | RWB-AD-018 AC2; FSD A2.11 |
| BR5 | A rerun is refused with 409 while a run of the job is RUNNING or when the business date is not complete in `v_ace_batch_status` | TSD API-P1-002 errors |
| BR6 | Platform administration R reads the monitor; Platform administration U reruns; a role without the right is refused with MSG-P4-002 | RWB-AD-018 permission checks |
| BR7 | No ACE batch, feed or file is started, stopped or rerun from the Workbench | RWB-AD-018 guardrail; NFR-015 |
| BR8 | A missing or stale freshness stamp is shown STALE with MSG-P1-001 and its last complete ACE date, never as fresh | FSD A2.14; VR-P1-001-1 |
| BR9 | One run row per attempt: a rerun adds a row and never updates the earlier one | RWB-AD-018 AC2; decision D-RCV-60 |

### 9. State transitions

The run row moves as follows; the job row of the catalogue never moves.

| From | Event | Condition | To |
|---|---|---|---|
| None | The job is due on `AceDataReady`, or a permitted rerun is accepted | The source batch is COMPLETE for the business date | PENDING, then RUNNING |
| None | The job is due | No source row is COMPLETE for the business date | WAITING, MSG-P1-001, no run started |
| WAITING | The source batch completes for the business date | None | PENDING, then RUNNING on the new `run_no` |
| RUNNING | The last check passes | None | COMPLETE, `finished_at` and duration written |
| RUNNING | A check fails or the job errors | None | FAILED, the failed check and its message ID kept |
| FAILED | A permitted rerun is accepted | No run RUNNING and the business date complete | A new row PENDING with `run_no` + 1; the FAILED row is unchanged |
| COMPLETE | A rerun is requested | None | Refused with 409; a completed date is not rerun |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the monitor, the run rows and the freshness stamp (Platform administration R) |
| RW-PLATADM, RW-SECADM | Rerun a failed Workbench job (Platform administration U) |
| SY-JOBRUN, job runner identity | Opens, checks, completes and fails a run row; starts the job |
| RWB-PLT-E1056-OPS | Loads the catalogue baseline and owns the run books the screen links to |
| Every other role | Reads nothing here; the screen is not served outside the six R roles |
| No role | Reruns an ACE batch, a feed or a file, or edits a completed run row |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-224 to DF-OPS-232 | job_catalog (rwb_source_data) | id, job_id, job_name, owner_role, schedule_text, runbook_path, expected_minutes, alert_after_minutes, first_release | Read |
| DF-OPS-001 to DF-OPS-008 | data_product_load (rwb_source_data) | product_code, source_system, business_date, source_extracted_at, loaded_at, status, stale_flagged_at | Read |
| DF-ACE-178 to DF-ACE-186 | v_ace_batch_status (ACE, through the service's view path) | source_system, business_date, started_at, completed_at, status, record_count and 3 more | Read, through `recovery.v_ace_*` |
| Not specified in the source documents (GAP-2162; ASM-3464) | run log (rwb_source_data) | job_id, business_date, run_no, status, started_at, finished_at, duration_minutes, check code, check result, check count, message_id | Write |

The run log is the one table this story adds; the logical model names the catalogue but no run record, and `load_run` left with the inbound load (TSD P1 T7). The catalogue and the freshness stamp are read, never written here: the rows are loaded by RWB-PLT-E1056-OPS and stamped by RWB-P1-E1015-APP. No `v_ace_*` view of another module is read and no table of another schema is touched (DP-01, DP-05).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1`; owner rwb-source-data (P1).

| Method | Path | Purpose | Access |
|---|---|---|---|
| GET | `/admin/jobs` | The catalogue joined to the latest run per job and business date, with the last complete business date of each source; query `jobCode`, `status`, `from`, `to` | Platform administration R, scope applied |
| POST | `/admin/jobs/{jobId}/rerun` | One new run of a failed job for a business date the ACE batch record shows complete; Idempotency-Key required | Platform administration U, scope applied |
| GET | `/data-products/freshness` | The freshness stamp of each product: business date, LOADED or STALE, ACE completion time; query `product`, `asOf` | Platform administration R here; the baseline of RWB-P1-E1015-APP is the same operation |

Errors: 400 on a malformed query, 401 no session (MSG-P4-001), 403 right missing (MSG-P4-002), 404 unknown job (MSG-GEN-001), 409 on a running job or an incomplete business date, 503 store down. The freshness shape is not redefined by this story: RWB-P1-E1015-CON owns the resource and this story serves it with the stale flag the monitor shows.

#### 12.2 REST operations consumed

None by the dependency classes of this story. The one cross-service answer the screen shows is the outbound actions of rwb-integration:

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-2162; ASM-3465) | P2 rwb-integration | The outbound actions of the business date with their status, duration and checks; mocked in AC1 | One hop, 2 s, GET retried once with jitter |

The row is tracked and is not a build dependency: the story is proved against the rwb-integration contract mock, and the real journey is RWB-ITG-AD018-ITG. The Platform administration right is read from the platform session, not by a call of this story.

#### 12.3 Events published

None. The monitor and the run record publish no event: `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` are published by RWB-P1-E1015-APP when the ACE batch record changes, and this story neither duplicates nor consumes them.

#### 12.4 Events consumed

None. The WAITING transition reads the ACE batch record in-service and is not driven by a consumed event; the freshness events of this service are consumed by their own story.

#### 12.5 Workflows and activities

None registered. The rerun starts the owning job of the service through the job runner, for example `ReconciliationWorkflow` of RWB-P1-E1011-APP for JOB-04; that workflow and its task queue `rwb-source-data` belong to its own story, and this story adds no workflow, activity or timer.

#### 12.6 Schedules

None. The service registers no Schedule and no Quartz trigger for the monitor; JOB-04 and the case-list steps still start on the ACE batch record as their own stories state, and `JOB-01` and `JOB-09` stay retired (FSD P1 v3).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| job_catalog | P1 (rwb_source_data) | The catalogue row of each Workbench job, read by both admin operations |
| run log (name pending, GAP-2162) | P1 (rwb_source_data) | One row per attempt: status, business date, duration, checks and message ID |
| data_product_load | P1 (rwb_source_data) | The freshness stamp read by the freshness operation; written by RWB-P1-E1015-APP |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_source_data | The Idempotency-Key of the rerun and the inbox dedupe |

`v_ace_batch_status` belongs to ACE and is read only through `recovery.v_ace_*` (DP-01, DP-05). No table of another service is read.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration outbound-action mock | The P2 contract | Two outbound actions for 2026-11-30, one COMPLETE with its checks and one FAILED; a delayed answer beyond 2 s |
| `v_ace_batch_status` fixture | The ACE read path | Sources COMPLETE for 2026-11-30, one source with no COMPLETE row, one with FAILED, and an unavailable answer |
| Session and role stub | The platform session | Platform administration R granted; U granted; U refused for a read-only role |
| Run-log fixture | The service's own store | A FAILED run with a failing check, a COMPLETE run, and a run log that refuses its write |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 1 consumed as a mock | The two admin operations and the freshness read provided; the outbound actions of P2 mocked, one hop, 2 s |
| Kafka | None | No event is published or consumed by this story |
| Temporal | None registered | The rerun starts the owning job's workflow; this story adds no workflow |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.sourcedata.jobs`, module `jobs`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none; RWB-P1-E1069-APP is class H |
| DP-13 | `/api/recovery/v1` | `/api/recovery/source-data/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The same-service CON baseline RWB-P1-AD018-CON and the ACE view story RWB-P1-E1069-APP are class H dependencies and are not DP rows. No pattern is claimed for Drools, for the outbox or for a Schedule: this story evaluates no rule, publishes no event and registers no timer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| JobsController | Controller | The job list and the rerun, the right check, the 404 and the two 409 cases |
| FreshnessController | Controller | The freshness read of the service's own stamp |
| JobRunner | Service | Opens, checks, completes and fails a run row and starts the owning job |
| AceBatchDateReader | Client | Reads `v_ace_batch_status` for a source and a business date through the service's own view path |
| RunLogRepository | Repository | Reads and writes the run log and reads the catalogue in `rwb_source_data` only |
| OutboundActionView | Adapter (mock at wave 4) | Projects the outbound actions of P2 into the row; empty with its own marker when the call fails |

**Database.** One Flyway step in the per-service sequence of `rwb_source_data` (DP-15): the run-log table with `job_id`, `business_date`, `run_no`, `status`, `started_at`, `finished_at`, `duration_minutes`, the check columns and `message_id`; unique `ux_jobrun ON (job_id, business_date, run_no)`; `ix_jobrun_latest ON (job_id, business_date, status)`. The catalogue table is not created or altered here.

**Configuration.** Whether the outbound columns are shown, the 2 s budget and the retry policy are service configuration values, never code. Job names, cadences, expected durations and alert minutes are catalogue rows, never code.

**Build steps**

1. Extend the generated types and the contract tests against RWB-P1-AD018-CON; the three operations answer from the catalogue, the run log and the stamp.
2. Flyway step and the run-log repository with the one-row-per-attempt rule; tests for AC2 both-runs.
3. `JobRunner` with the PENDING, RUNNING, COMPLETE, FAILED and WAITING moves and the check rows; tests for AC1 checks and for X3 and X6.
4. `AceBatchDateReader` over the service's view path, with the unknown answer of X5; tests for AC1 last complete date.
5. The rerun validation: right, job, running run and complete business date, with 409 and the Idempotency-Key; tests for AC2 and X2.
6. The freshness read with the STALE marker and MSG-P1-001 on the missing stamp of X7.
7. The outbound adapter against the P2 mock, with the empty-column marker of X8.
8. The boundary test that fails a class outside the module reading `public` or another schema, and the check that no ACE run path exists.

**Feature switch.** `rwb.p1.jobmonitor`. Off: the two admin operations answer 404 and no run row is written; on: the behaviour above.

**Done when.** Both owned test cases and the component tests pass, the catalogue of the Epic 1 baseline renders with its ACE business date in SIT, a rerun of a failed job leaves two rows, and the contract tests of RWB-P1-AD018-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product is STALE, or a job waits for its ACE batch | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | A required field is missing, or the job code is unknown | Enter {field}. |
| MSG-P4-002 | A role without Platform administration R or U | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from the legacy story; the error and message standard wording of MSG-P1-001 is under OQ-P1-07 and is not changed here. Thai text follows DL10. This story adds no message ID.

### 15. Screens and states

SCR-44 Interface and job monitor in its four states: **Running** (a run of the job is in progress, with its start and duration so far), **failed** (a FAILED run with its failed check and message ID, and the rerun action for a U role), **waiting for the ACE batch** (a WAITING run with the last complete ACE date and MSG-P1-001), **complete** (the latest run COMPLETE with its duration and checks). The screen is composed by the gateway-bff route of RWB-PLT-N001-CON (DP-19); this story fixes the three answers it reads and no screen of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-018-01 | AC1, BR1, BR2, BR8 | End to end | Catalogue baseline rows; jobs and outbound actions for 2026-11-30; one source complete, one stale |
| TC-AD-018-02 | AC2, BR4, BR5, BR9 | End to end | A FAILED run for 2026-11-30; a rerun after the fix; two rows with `run_no` 1 and 2 |
| TC-AD-018-04 | Access, BR6 | Component | RW-AUDIT calls the rerun and is refused with MSG-P4-002; RW-PLATADM succeeds |

Legacy TC-AD-018-03 proves legacy AC3, the late ACE batch that is recorded WAITING and shown STALE, and is owned by RWB-ITG-AD018-ITG, which copies all four legacy cases with the `-ITG` suffix. The legacy level "System" maps to End to end and "Access" to Component, as the rest of this story set maps it. The full text of each test is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: job names, cadences, expected durations, alert minutes and thresholds are catalogue or values rows.
- No personal data in the run log, an event, a log line or a test: job IDs, source systems, business dates, counts and durations only.
- No ACE data outside the owner's path: `v_ace_batch_status` only through `recovery.v_ace_*`, never a `public` table, never a cross-schema join (DP-01, DP-05).
- No ACE batch, feed or file is started, stopped or rerun from the Workbench; a late batch makes the run WAITING.
- A completed run row is never updated; a rerun adds a row.
- One hop and 2 s per call, a breaker per downstream, GET retried once with jitter.
- The monitor names IDs, codes, dates, counts and durations only; no amount and no customer field is shown on this screen.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel | Program BRD, NFR table; FSD P1 A2.12 | TC-AD-018-01 |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target | Program BRD, NFR table; RWB-P1-AD018-OPS AC5 | TC-AD-018-01, TC-AD-018-02 |
| REQ-DRI-007 | Every outbound file is logged, retried on a defined schedule and placed in a named exception queue on failure | Program BRD; FSD P2 | TC-AD-018-01 |
| REQ-DRI-008 | The Workbench runs no inbound batch or file load; work that depends on a source starts when ACE records the batch complete | Program BRD; FSD P1 A2.14 | TC-AD-018-01, TC-AD-018-02 |
| BR-P1-014-2 | Freshness is read from `v_ace_batch_status` only | FSD P1 A2.14 | TC-AD-018-01 |

### 19. Out of scope

- The contract baseline of the three operations, the two resources and the fakes (RWB-P1-AD018-CON).
- The deployment, the migration in the pipeline, the dashboards, the alerts and the run books (RWB-P1-AD018-OPS, RWB-PLT-E1056-OPS).
- The freshness stamp and the two ACE batch events (RWB-P1-E1015-APP), the reconciliation behind JOB-04 (RWB-P1-E1011-APP) and the case-list steps (their own stories).
- The read path, the grant and the boundary test over `recovery.v_ace_*` (RWB-P1-E1069-APP).
- Legacy AC3, the late ACE batch seen end to end across ACE, rwb-source-data and the screen, and the cross-service compose with the outbound actions (RWB-ITG-AD018-ITG).
- The screen field list and the composite route (RWB-PLT-N001-CON) and the run books themselves (RWB-PLT-E1056-OPS).
- The Platform administration roles and their assignment (RWB-P4-AD001 to RWB-P4-AD016 and the access stories).
