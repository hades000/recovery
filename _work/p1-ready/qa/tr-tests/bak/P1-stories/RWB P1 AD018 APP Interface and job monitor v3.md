# RWB-P1-AD018-APP Interface and job monitor

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Applied RD-P1-001, RD-P1-004, RD-P1-012, RD-P1-020, RD-P1-021, RD-P1-024, RD-P1-040, RD-P1-042 and RD-P1-045 to job ownership, run storage, run triggers, errors and rerun behaviour.
- Fixed the review findings AD018-APP#1–26: waiting runs, rerun states and concurrency, error answers, access rights, dependencies, test cases and traceability. Added AC12–AC18.
- Open: NEW-GAP-S9-1, NEW-GAP-S9-2, NEW-GAP-S9-7, NEW-GAP-A1 and the remaining part of GAP-2162. Unregistered gap numbers of the earlier draft are replaced by temporary IDs or settled.
- Applied RD-P1-065 (a repeated readiness call starts nothing once the date is closed; reruns are of FAILED runs only), cited the Test Cases v9 IDs of AC12–AC18 and moved the message standard citation to version 6.

| Item | Value |
|---|---|
| Story key | RWB-P1-AD018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Size | Not specified |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-AD018-CON, RWB-P1-E1011-APP, RWB-P1-E1015-APP and RWB-P1-E1069-APP |
| Depends on (build) | RWB-P1-AD018-CON, RWB-P1-E1011-APP, RWB-P1-E1015-APP, RWB-P1-E1069-APP |
| Contract dependencies | RWB-P2 rwb-integration scheduled-jobs contract; RWB-P1-E1011-CON; RWB-P1-E1015-CON; platform flag library |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-001; RD-P1-004; RD-P1-012; RD-P1-020; RD-P1-021; RD-P1-024; RD-P1-040; RD-P1-042; RD-P1-045; RD-P1-065 |
| Integration dependencies | None |
| External dependencies | RWB-P1-AD018-OPS, RWB-PLT-E1056-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v3.md (no FR mapped; no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-018 for rwb-source-data. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-AD018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 14 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: P1 developer readiness (RD-P1 register); story editor S9-stories.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **a paged history of rwb-source-data runs and a controlled rerun of a failed run, with ACE source completeness and freshness visible**, so that **I can find and recover failed P1 work without rerunning ACE or operating another service's jobs**.

RWB-P1-AD018-CON is the sole publisher of the job operations. The list contains one item per run for `AceIngestCheck`, `ReconciliationWorkflow` (type `JOB-04`), `Stage2ProductWorkflow` and `RetentionRunWorkflow`. The case list is owned by rwb-case; P1 creates no case-list table, workflow, schedule or publish state (RD-P1-012, RD-P1-020, RD-P1-024).

### 2. Business rationale

The monitor supports operational recovery of P1 workflows. One item per run preserves attempt history; `job_run` and `job_run_check` provide the durable status and check records required by RD-P1-020. P2 owns `job_catalog`; the app reads it through the P2 scheduled-jobs contract under RD-P1-021. P1 does not operate other services' jobs.

A waiting run records a missing ACE source completion, not a failed job. An accepted rerun is limited to a FAILED run and uses the run uuid and its business date. The case list remains with rwb-case under RD-P1-024.

### 3. Preconditions

- RWB-P1-AD018-CON publishes the job operations against `rwb-source-data.yaml` 5.1.0.
- The rwb-integration contract publishes `GET /api/recovery/integration/v1/admin/scheduled-jobs`; `job_catalog` remains owned by P2 and is read through that operation, one hop with a 2 s budget and one jittered GET retry (RD-P1-021).
- RWB-P1-E1015-CON owns the freshness answer. RWB-P1-E1015-APP writes `data_product_load`; this story reads the answer and does not stamp freshness.
- RWB-P1-E1069-APP provides read-only `recovery.v_ace_*` access. ACE status `COMPLETED` is read from `v_ace_batch_status`.
- RWB-P1-E1011-APP provides the JOB-04 `ReconciliationWorkflow`. The case list is owned by rwb-case; P1 creates no case-list table, workflow, schedule, or publish state (RD-P1-022, RD-P1-024).
- `job_run` and `job_run_check` are created by this story's one Flyway step `V<seq>__rwb_p1_ad018_job_run.sql` with their dictionary rows (`sys_objects` 2 rows and `sys_fields` 19 rows through the governed load of RWB-P1-E1064-APP), as specified in RD-P1-020. ASM-0722 (no job-run table) is superseded by RD-P1-020.
- Rerun uses the uuid of a FAILED run, has no request body, and requires UUID `Idempotency-Key` (RD-P1-001, RD-P1-012).
- P1 serves its own runs only. The gateway-bff composite handles other owners' job reads; that cross-service gap is NEW-GAP-A1.
- The platform flag library holds `rwb.p1.jobmonitor`, which gates the two job operations (RD-P1-045). It starts and stops no P1 workflow and does not gate the freshness read of RWB-P1-E1015-CON. Pending: initial value and enabling role per environment, and whether the run-record writer writes rows while the flag is off, owner solution architect with the release owner, tracked as NEW-GAP-S9-2.

### 4. Flow

1. A P1 run is due when its workflow starts (RD-P1-040): `AceIngestCheck` from the readiness call, the 05:30 Schedule or the fallback poll; `ReconciliationWorkflow` and `Stage2ProductWorkflow` as children of `AceIngestCheck` after the ALS stamp; `RetentionRunWorkflow` from `POST /retention-runs`. While a source mapped through `data_product_source` to a product the run reads is not `COMPLETED` in `v_ace_batch_status` for the business date, the run row is `WAITING` and the job's work does not start (RD-P1-020 E). The open run moves the same row to RUNNING once every mapped source is `COMPLETED`; a start after a run has closed writes a new row with the next `run_no`. A repeated `POST /business-days/{date}/ready` for a date whose `business_day_readiness` row is DONE or LATE starts nothing, so a second `ReconciliationWorkflow` run of a date exists only through the rerun of a FAILED run (RD-P1-065).
2. The job runner, a workflow-kit interceptor on the P1 workflows, writes one `job_run` row per run (`run_no` 1 for the first run of a type and business date). It records PENDING or WAITING, then RUNNING with `started_at`; completion or failure records `finished_at`, whole-minute duration and any message ID raised. A completed execution is COMPLETE, also when a reconciliation check is BREAK (message ID `MSG-P1-012`); an execution that fails is FAILED. Each check result (REC-01, REC-02, REC-05) is written to `job_run_check` in the same activity transaction that records it (RD-P1-020 D).
3. `GET /admin/jobs` returns one item per run, ordered by `startedAt` descending, with query filters and paging from RD-P1-012. Job metadata comes from the P2 scheduled-jobs contract, never from a local `job_catalog` table.
4. `lastAceBusinessDate` is the one optional ACE date of the published `Job`; freshness per data product and source is read from `GET /data-products/freshness` of RWB-P1-E1015-CON, whose schema this story does not restate. A value that cannot be read (`jobName` from P2, `lastAceBusinessDate` from the view) is omitted and the run items are still returned. Pending: the date `lastAceBusinessDate` holds when a job reads several sources, the rounding of `durationMinutes`, and the `check_count` and `expected_count` totals of each check, owner contract owner with the data owner, tracked as NEW-GAP-S9-7.
5. `POST /admin/jobs/{jobId}/rerun` treats `{jobId}` as the uuid `job_run.id` of a FAILED run. It requires `Idempotency-Key`, accepts no body, and takes type and business date from that run.
6. An accepted rerun writes a new row with `run_no` + 1 and `rerun_of_id`; it never updates the earlier row. The new row holds `requested_by` and `idempotency_key`. It starts the P1 workflow for the run type using Temporal conflict policy FAIL and reuse policy `ALLOW_DUPLICATE_FAILED_ONLY`. Of two reruns of one run with different keys, `uk_job_run` lets one write the next `run_no`; the other answers 409 `MSG-P1-011`.
7. No P1 operation starts, stops or reruns an ACE batch, feed or file. There is no P1 case-list operation or workflow. Outbound actions of rwb-integration are not in the P1 list; the gateway-bff composite reads them from their owner (the outbound-action part of GAP-2162 stays open).
8. Rerunning only after the cause is fixed is an operator step in the job's run book; the run book path stays in the P2 catalogue and is not a `Job` field. The service checks the run state, the open-run condition and the ACE batch only.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Unknown or non-P1 run id | 404 in Problem envelope; no write | MSG-P4-003 | AC5 |
| X2 | Target run is not FAILED or same type/date has a PENDING or RUNNING run | 409; no new row | MSG-P1-011 | AC5 |
| X3 | ACE batch is not `COMPLETED` | 409; no workflow starts | MSG-P1-001 | AC5 |
| X4 | Idempotency key is missing or not a UUID, or reused on another run path | 400 for the first, 409 for the second; no new run | MSG-PLT-N009-03 / MSG-PLT-N009-05 | AC6 |
| X5 | Run store unavailable or refuses the write | 503; no workflow starts and no row is written | MSG-GEN-006 | AC17, AC18 |
| X6 | P2 scheduled-jobs read fails or exceeds 2 s twice | 200 with the run items; `jobName` is omitted | None | AC17 |
| X7 | Freshness stamp absent | RWB-P1-E1015-CON answers STALE with a null business date; never LOADED | MSG-P1-001 | AC9 |
| X8 | No session or Workbench role, or the right is missing | 401 or 403 before any read or write | MSG-P4-001 / MSG-P4-002 | AC7 |
| X9 | `rwb.p1.jobmonitor` is off | GET and POST rerun answer 404; no run row is written by the request | MSG-P4-003 | AC16 |
| X10 | Query value malformed, outside its list or range, or `from` later than `to` | 400 or 422; nothing is read | MSG-GEN-001, -002, -003, -007 | AC15 |
| X11 | Two reruns of one FAILED run arrive together with different keys | One is accepted; the other answers 409 | MSG-P1-011 | AC14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against its own contract baseline, the platform route and the ACE read path of its own service; builds nothing against rwb-integration |
| Negotiable | Cadences, expected durations and thresholds are catalogue and values rows; the story fixes the behaviour |
| Valuable | A failed job is found before the working day and a late ACE batch is not chased as a failed job |
| Estimable | Two operations, one job-runner interceptor, two tables in one Flyway step and their tests |
| Small | Fits one sprint with its tests |
| Testable | All 18 acceptance criteria assert data, status or message; cross-service composition is proved by RWB-ITG-AD018-ITG |

### 7. Acceptance criteria

```gherkin
Feature: P1 job history and rerun

  Scenario: AC1 P1 job history returns one item per run
    Given runs exist for `AceIngestCheck`, `ReconciliationWorkflow`, `Stage2ProductWorkflow` and `RetentionRunWorkflow`
    When RW-PLATADM requests `GET /admin/jobs` for 2026-11-24 through 2026-11-30
    Then the page contains one item per run, ordered by `startedAt` descending, with id, type, businessDate, runNo, status, startedAt, endedAt, durationMinutes and checks
    And the response applies type, status, date, page and size filters from RD-P1-012
    And job metadata is read through `GET /api/recovery/integration/v1/admin/scheduled-jobs`

  Scenario: AC2 P1 list excludes other owners and the case list
    Given job metadata and run rows exist
    When the P1 job list is read
    Then it lists P1 run types only
    And it contains no `CaseListBuildWorkflow`, `DailyCaseList`, case-list table, or run from another service

  Scenario: AC3 Incomplete mapped source leaves a WAITING run
    Given one source mapped through `data_product_source` for a product read by JOB-04 is not `COMPLETED` for 2026-11-30
    When the JOB-04 run for that date starts
    Then its `job_run` row has status WAITING and the reconciliation activity does not run
    And started_at, finished_at and duration_minutes are null

  Scenario: AC4 Failed run is rerun once
    Given FAILED run id `00000000-0000-4000-8000-000000000018` for 2026-11-30 and its ACE batch is `COMPLETED`
    When RW-PLATADM posts `/admin/jobs/00000000-0000-4000-8000-000000000018/rerun` with a UUID Idempotency-Key and no body
    Then the response is 202 with a new Job in PENDING and runNo increased by one
    And rerun_of_id names the failed run and its row is unchanged

  Scenario: AC5 Rerun errors follow the contract
    Given an unknown or non-P1 run, a run not in FAILED, an open same-type/date run, and an ACE batch not `COMPLETED`
    When each rerun is requested
    Then unknown or non-P1 run answers 404 MSG-P4-003
    And non-FAILED or open-run answers 409 MSG-P1-011
    And incomplete batch answers 409 MSG-P1-001
    And no refused request creates a row

  Scenario: AC6 Rerun idempotency is enforced
    Given the first rerun used UUID key K on run path P and returned 202
    When the same key and same path are replayed within 24 hours
    Then the stored 202 response is returned and no second run is created
    And when key K is used on another run path, the answer is 409 MSG-PLT-N009-05
    And a missing, blank or non-UUID key answers 400 MSG-PLT-N009-03

  Scenario: AC7 Access is checked before job data is read
    Given one caller has no session and another lacks Platform administration R for the list or U for the rerun
    When each caller requests the operation
    Then the first is answered 401 `MSG-P4-001` and the second 403 `MSG-P4-002`
    And no run row is read or written

  Scenario: AC8 Run outcomes and check rows are persisted
    Given a RUNNING JOB-04 run for 2026-11-30 with checks REC-01, REC-02 and REC-05
    When the execution completes with every check PASS
    Then `job_run` is COMPLETE with finished_at and duration_minutes and `job_run_check` holds one PASS row per check code
    And for an execution that completes with REC-01 BREAK, `job_run` is COMPLETE with message_id `MSG-P1-012` and the REC-01 row is BREAK
    And for an execution that fails, `job_run` is FAILED with finished_at and duration_minutes

  Scenario: AC9 Freshness uses its owning contract
    Given a data product has no freshness stamp and the caller has Case record R
    When `GET /data-products/freshness` of RWB-P1-E1015-CON is read for the monitor
    Then the product has status STALE with a null businessDate and is never LOADED

  Scenario: AC10 P1 neither operates ACE batches nor reads another service schema
    Given a request to start, stop or rerun an ACE batch, feed or file
    When the request is made to P1
    Then P1 performs no ACE operation and database grants allow only the service's recovery.v_ace_* views and owned tables

  Scenario: AC11 Rerun actor and key fields are retained
    Given a privileged rerun request is accepted
    When the new job_run row is written
    Then requested_by and idempotency_key are stored
    And whether a decision record or audit entry is also written, and whether a refused rerun is logged, is Pending, owner product owner with compliance, tracked as NEW-GAP-S9-1

  Scenario: AC12 A waiting run proceeds or is followed by a new run
    Given the JOB-04 run for 2026-11-30 is open with a WAITING row of run_no 1
    When every mapped source becomes `COMPLETED`
    Then the same row moves to RUNNING with started_at and no second row is written
    And when instead the run closed while WAITING, a new start writes run_no 2 and leaves run_no 1 unchanged

  Scenario: AC13 Rerun is refused for every state except FAILED
    Given runs in PENDING, RUNNING, COMPLETE and WAITING
    When each is rerun with a new Idempotency-Key
    Then each answers 409 `MSG-P1-011` and no row is written

  Scenario: AC14 Concurrent reruns create one run
    Given a FAILED run with run_no 1 and a `COMPLETED` ACE batch
    When two reruns with different Idempotency-Keys arrive together
    Then one answers 202 and the other 409 `MSG-P1-011`
    And exactly one row with run_no 2 exists

  Scenario: AC15 Query validation and empty result
    Given RW-PLATADM calls `GET /admin/jobs`
    When the query is `status=DONE`, `from=2026-13-01`, `from=2026-11-30&to=2026-11-01` or `size=201`
    Then the answers are 400 `MSG-GEN-007`, 400 `MSG-GEN-001`, 422 `MSG-GEN-003` and 422 `MSG-GEN-002`
    And a well-formed range with no run answers 200 with empty items and total 0

  Scenario: AC16 Feature flag off
    Given `rwb.p1.jobmonitor` is off
    When the job list and the rerun are called
    Then each answers 404 `MSG-P4-003` and no run row is written

  Scenario: AC17 Unavailable sources of data
    Given a stored run for 2026-11-30
    When the P2 scheduled-jobs read exceeds 2 s on both attempts
    Then the list answers 200 with the run and no jobName
    And when the `v_ace_batch_status` read fails, the run is returned without lastAceBusinessDate
    And when the run store is unavailable, both operations answer 503 `MSG-GEN-006`

  Scenario: AC18 A refused run write starts nothing
    Given the run store refuses the insert of the new run row
    When a rerun of a FAILED run is posted
    Then the answer is 503 `MSG-GEN-006`, no workflow starts and the failed row is unchanged
```

Test references: AC1 TC-AD-018-01; AC2 TC-AD-018-02; AC3 TC-AD-018-05; AC4 TC-AD-018-04; AC5 TC-AD-018-08; AC6 TC-AD-018-09; AC7 TC-AD-018-10 and TC-AD-018-03; AC8 TC-AD-018-11; AC9 TC-AD-018-12; AC10 TC-AD-018-13; AC11 TC-P1-AD018-APP-01. Test Cases v9 holds the rows for the changed texts of AC3, AC7, AC8, AC9 and AC11.

AC12 TC-P1-AD018-APP-02; AC13 TC-P1-AD018-APP-03; AC14 TC-P1-AD018-APP-04; AC15 TC-P1-AD018-APP-05; AC16 TC-P1-AD018-APP-06; AC17 TC-P1-AD018-APP-07; AC18 TC-P1-AD018-APP-08 (Test Cases v9).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | P1 lists its own four run types only, one item per run ordered by `startedAt` descending | RD-P1-012 |
| BR2 | `job_catalog` belongs to P2 rwb-integration and is read through its scheduled-jobs contract | RD-P1-021 |
| BR3 | A run starts only when each source mapped to each product it reads is `COMPLETED`; otherwise it remains WAITING | RD-P1-020 E |
| BR4 | Rerun targets a FAILED run uuid, has no body, requires UUID `Idempotency-Key`, answers 202 and writes a new row; fixing the cause first is a run book step, not a service check | RD-P1-001; RD-P1-012 |
| BR5 | Refuse rerun when the target is not FAILED, a same-type/date run is open, or the batch is not `COMPLETED` | RD-P1-012; RD-P1-040 |
| BR6 | `job_run` and `job_run_check` are P1-owned and written by the P1 runner | RD-P1-020 A–E |
| BR7 | P1 has no case-list table, workflow, schedule, state or check | RD-P1-024 |
| BR8 | ACE reads use only `recovery.v_ace_*`; no other service schema is read directly | D-RCV-60; RD-P1-021 |
| BR9 | The two job operations need Platform administration R or U; the freshness read needs Case record R as published by RWB-P1-E1015-CON | RWB-P1-E1015-CON; `rwb-source-data.yaml` 5.1.0 |
| BR10 | A WAITING row belongs to its open run; a new run_no is written only by a rerun of a FAILED run or by a start after the earlier run closed | RD-P1-040 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | Run due | All mapped sources of all products read are `COMPLETED` | PENDING, then RUNNING |
| None | Run due | Any mapped source is not `COMPLETED` | WAITING; the job's work does not start |
| WAITING | Every mapped source becomes `COMPLETED` | The run is still open | RUNNING (same row) |
| WAITING | The run closes | A source is still not `COMPLETED` | WAITING (row kept; a later start writes the next `run_no`) |
| RUNNING | Execution completes | Check results persisted, PASS or BREAK | COMPLETE with `finished_at` and duration |
| RUNNING | Execution fails | Failure recorded | FAILED with `finished_at`, duration and any message ID |
| FAILED | Rerun accepted | No same-type/date run is PENDING or RUNNING; batch is `COMPLETED` | New PENDING row with `run_no` + 1 and `rerun_of_id`; old row unchanged |
| Any non-FAILED state | Rerun requested | — | Refused with 409 `MSG-P1-011` |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM (Platform administration R) | Read P1 job history |
| Roles with Case record R | Read freshness through RWB-P1-E1015-CON |
| RW-PLATADM, RW-SECADM (Platform administration U) | Request rerun of a FAILED P1 run |
| P1 job runner identity | Write P1 run and check rows; start the P1 workflow for the run type |
| P2 rwb-integration | Own `job_catalog` and provide scheduled-job metadata through its contract |
| RWB-P1-E1015-APP | Own freshness stamps and ACE readiness events |
| Every other role | No read or write unless granted by the published access contract |
| No role | Starts, stops or reruns an ACE batch, feed or file through P1 |

### 11. Data

| Field IDs | Entity | Fields | Read or write |
|---|---|---|---|
| DF-OPS-233 to DF-OPS-245 | `job_run` (`rwb_source_data`) | `id` uuid, `job_type` varchar(60), `business_date` date, `run_no` integer, `status` varchar(10), `workflow_id` varchar(200), `started_at`, `finished_at`, `duration_minutes`, `message_id` varchar(20), `requested_by` uuid, `idempotency_key` varchar(120), `rerun_of_id` uuid | Write by P1 runner; read by monitor |
| DF-OPS-246 to DF-OPS-251 | `job_run_check` (`rwb_source_data`) | `id` uuid, `job_run_id` uuid, `check_code` varchar(30), `check_result` varchar(8), `check_count` integer, `expected_count` integer | Write by P1 runner; read by monitor |
| DF-OPS-224 to DF-OPS-232 | `job_catalog` (`rwb_integration`) | P2 scheduled-job catalogue fields | Read through P2 contract only |
| DF-OPS-001 to DF-OPS-009 | `data_product_load` (`rwb_source_data`) | Freshness stamp fields | Read through E1015-CON; written by E1015-APP |
| DF-REF-300 to DF-REF-302 | `data_product_source` (`rwb_source_data`) | `id`, `product_code`, `source_system` | Read by completeness gate |
| DF-ACE-178 to DF-ACE-186 | `v_ace_batch_status` | ACE source and batch fields | Read only through `recovery.v_ace_*` |

`job_run` constraints: `uk_job_run UNIQUE (job_type, business_date, run_no)`, `uk_job_run_idempotency UNIQUE (idempotency_key)`, `ix_job_run_latest ON (job_type, business_date, status)`, and `fk_job_run_rerun_of`. `job_run_check` has `uk_job_run_check UNIQUE (job_run_id, check_code)`. JOB-04 checks are REC-01, REC-02 and REC-05. The checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED are withdrawn from P1 (RD-P1-020, RD-P1-024).

### 12. Contract

#### 12.1 REST operations provided

Publisher: RWB-P1-AD018-CON. Base `/api/recovery/source-data/v1`; contract version `rwb-source-data.yaml` 5.1.0. Both operations are gated by `rwb.p1.jobmonitor`; when off, they answer 404 `MSG-P4-003` and no row is written (RD-P1-045).

| Method | Path | Purpose | Access |
|---|---|---|---|
| GET | `/admin/jobs` | Paged P1 run history, one item per run ordered by `startedAt` descending; query `type`, `status`, `from`, `to`, `page`, `size` | Platform administration R |
| POST | `/admin/jobs/{jobId}/rerun` | Rerun a FAILED run; path id is the run uuid; no body; UUID `Idempotency-Key` required | Platform administration U |

`JobPage` contains `items`, `page`, `size` and `total`; one item is returned per run in `startedAt` descending order. Query fields are `type`, `status`, `from`, `to`, `page` and `size`. `from` and `to` are inclusive business dates in Asia/Bangkok; defaults are today minus 7 days and today; page defaults to 0; size defaults to 50 and is bounded 1–200. `Job` fields are `id` uuid, `type`, `jobName`, `workflowId`, `runNo`, `businessDate`, `status`, `startedAt`, `endedAt`, `durationMinutes`, `lastAceBusinessDate` and `checks`. `id`, `type`, `businessDate` and `status` are required. `endedAt` and `durationMinutes` are nullable; another optional property is omitted while it has no value. Checks are keyed by check code and each value is `{expected:number, actual:number, passed:boolean}`.

Rerun answers follow RD-P1-012: 202 new PENDING Job; 400 `MSG-PLT-N009-03`; 404 `MSG-P4-003`; 409 `MSG-P1-011`, `MSG-P1-001` or `MSG-PLT-N009-05`; 503 `MSG-GEN-006`. Both operations answer 401 `MSG-P4-001` and 403 `MSG-P4-002`; list query errors follow section 14. Freshness remains the operation and schema of RWB-P1-E1015-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/integration/v1/admin/scheduled-jobs` | P2 rwb-integration | Read P2-owned `job_catalog` metadata | One hop, 2 s; GET retried once with jitter |
| GET | Pending: per-service job reads for the other owners are outside P1; NEW-GAP-A1 | Each owning service | Gateway-bff composite only; not called by P1 | Per owner contract |

#### 12.3 Events published

None. `AceDataReady` and `AceDataLate` are event types published by E1015-APP on topic `rwb.source-data.events.v1`.

#### 12.4 Events consumed

None by this story; no P1 Kafka consumer is added.

#### 12.5 Workflows and activities

No new workflow type is registered. Rerun starts the workflow of the P1 run type: `AceIngestCheck`, `ReconciliationWorkflow` (JOB-04), `Stage2ProductWorkflow` or `RetentionRunWorkflow`. The runner writes job-run records per RD-P1-020.

#### 12.6 Schedules

No case-list Schedule is registered in P1; there is no `CaseListBuildWorkflow` or `DailyCaseList` in this service (RD-P1-024).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `job_run` | P1 `rwb_source_data` | One row per run attempt |
| `job_run_check` | P1 `rwb_source_data` | One row per run check |
| `data_product_source` | P1 `rwb_source_data` | Product-to-source map for completeness gate |
| `data_product_load` | P1 `rwb_source_data` | Freshness stamp; written by E1015-APP |

#### 12.8 Contract fakes

| Fake | Serves | Required stubs |
|---|---|---|
| rwb-integration scheduled-jobs fake | P2 contract | P1 metadata and unavailable response |
| `v_ace_batch_status` fixture | P1 ACE view path | `COMPLETED`, missing source, FAILED and unavailable cases |
| P1 run-store fixture | P1 tables | FAILED/open runs, check rows, concurrent requests and failed write |
| Session and role fake | Platform session | R and U granted; no session and refused right |

Provider and consumed fakes are WireMock mappings pinned to the provider contract version; the P1 fake is published at `fakes/rwb-source-data/5.1.0/` in RWB-PLT-LIB (RD-P1-011).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided; one consumed | P1 job list/rerun; P2 metadata call |
| Kafka | None | No consumer added |
| Temporal | Existing P1 workflows by run type | No case-list workflow or schedule |
| File | None | No file read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.jobs`.

**Feature switch.** `rwb.p1.jobmonitor` gates GET `/admin/jobs` and POST `/admin/jobs/{jobId}/rerun` (404 `MSG-P4-003` when off, RD-P1-045). It gates no workflow start. Initial value, enabling role and gating of the run-record writer: NEW-GAP-S9-2.

| Component | Type | Responsibility |
|---|---|---|
| JobsController | Controller | Paged P1 run history and rerun operation |
| JobRunner | Service | Apply run states, start the owning workflow and write both run tables |
| JobCatalogClient | Client | Read P2 `job_catalog` through scheduled-jobs contract |
| AceBatchDateReader | Client | Read `v_ace_batch_status` through `recovery.v_ace_*` |
| RunLogRepository | Repository | P1 `job_run` and `job_run_check` only |

**Database.** Create `job_run` and `job_run_check` in one per-service Flyway step with the fields, constraints and dictionary IDs of RD-P1-020. Do not create `job_catalog` or a case-list table.

**Build steps.** Generate AD018-CON types; implement the P2 metadata client; create the two P1 run tables; implement the mapped-source completeness gate; implement the one-item-per-run list and paging; implement rerun validation and idempotency; verify check persistence for REC-01, REC-02 and REC-05.

**Done when.** A failed P1 run can be rerun into a new row, all P1 workflow types can be listed, and no P2-owned or case-list table is created.

### 14. Validation and messages

| Condition | Response |
|---|---|
| Invalid rerun key | 400 `MSG-PLT-N009-03` |
| Unknown or non-P1 run id | 404 `MSG-P4-003` |
| Target not FAILED or same-type/date run open | 409 `MSG-P1-011` |
| ACE batch is not `COMPLETED` | 409 `MSG-P1-001` |
| Reused idempotency key | 409 `MSG-PLT-N009-05` |
| Store unavailable | 503 `MSG-GEN-006` |
| No session or no Workbench role | 401 `MSG-P4-001` |
| Missing right | 403 `MSG-P4-002` |
| Query: malformed date or number; value outside its list | 400 `MSG-GEN-001`; 400 `MSG-GEN-007` |
| Query: value out of range; `from` later than `to` | 422 `MSG-GEN-002`; 422 `MSG-GEN-003` |
| `rwb.p1.jobmonitor` off | 404 `MSG-P4-003` |

Problem properties and text follow Error and Message Standard v6 and RD-P1-001/RD-P1-004. This story invents no message text.

### 15. Screens and states

SCR-44 is composed by gateway-bff. P1 provides run history and rerun. The screen shows PENDING, RUNNING, COMPLETE, FAILED and WAITING (waiting for the ACE batch) with timestamps, duration and checks; it shows no P1 case-list state. Empty, loading, error and access-denied states are built by the screen and route stories; their behaviour is listed in RWB-P1-AD018-OPS section 15.

### 16. Test cases

| AC | Test reference |
|---|---|
| AC1, AC2, AC3, AC4 | TC-AD-018-01, TC-AD-018-02, TC-AD-018-05, TC-AD-018-04 |
| AC5, AC6, AC7 | TC-AD-018-08, TC-AD-018-09, TC-AD-018-10, TC-AD-018-03 |
| AC8, AC9, AC10, AC11 | TC-AD-018-11, TC-AD-018-12, TC-AD-018-13, TC-P1-AD018-APP-01 |
| Section 12 operations and tables | TC-AD-018-06, TC-AD-018-07 |
| AC12, AC13, AC14, AC15 | TC-P1-AD018-APP-02, TC-P1-AD018-APP-03, TC-P1-AD018-APP-04, TC-P1-AD018-APP-05 |
| AC16, AC17, AC18 | TC-P1-AD018-APP-06, TC-P1-AD018-APP-07, TC-P1-AD018-APP-08 |

Test Cases v9 holds the rows of the changed criteria (AC3, AC7, AC8, AC9, AC11).

### 17. Guardrails

- P1 job types only; job list returns one item per run.
- `job_catalog` is P2-owned and accessed only through its contract.
- Run rows are append-only; a rerun adds a row.
- Every mapped source of every product read must be `COMPLETED` before a workflow starts.
- ACE is read only through `recovery.v_ace_*`; no ACE batch, feed or file is operated by P1.
- P1 creates no case-list table, schedule, workflow, checks or publish state.
- No personal data is written to run records, logs or fixtures.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| NFR-015 | The Workbench operates no ACE batch, feed or file | Program BRD; AC10 | TC-AD-018-13 |
| NFR-067 | Scheduled job has monitoring and a run book | Program BRD | TC-AD-018-01 |
| NFR-068 | Failing job alerts its owner within the target (alert deployed per RWB-P1-AD018-OPS) | Program BRD; AD018-OPS | TC-P1-AD018-OPS-05 |
| REQ-DRI-008 | P1 does not load or rerun source batches | Program BRD; RD-P1-012 | TC-AD-018-02, TC-AD-018-13 |
| BR-P1-014-2 | ACE status comes from `v_ace_batch_status` | FSD P1 A2.14; RD-P1-020 | TC-AD-018-05 |

### 19. Out of scope

- Publishing the job operations (RWB-P1-AD018-CON).
- Deploying the service, running the APP migration, dashboards and runbooks (RWB-P1-AD018-OPS).
- Cross-service job reads and composition by gateway-bff (NEW-GAP-A1).
- Freshness writes and ACE events (RWB-P1-E1015-APP).
- Reconciliation workflow implementation (RWB-P1-E1011-APP).
- Case list and case-list schedule (rwb-case; RD-P1-024).

### Remaining delivery steps

- Size: Pending squad refinement; owner delivery lead.
- Epic design sign-off: Pending; owner solution architect.
- CON Done: Pending; owner contract owner.
- Contract fake published at the approved version: Pending; owner contract owner.
- Synthetic test data in DEV: Pending; owner test data owner.