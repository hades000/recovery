# RWB-P1-AD018-CON Interface and job monitor

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Applied RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-021, RD-P1-024 and RD-P1-040: sole P1 publisher, contract shapes, errors and fakes.
- Fixed the review findings AD018-CON#1–23: field-level schema, status and message table, rights, ownership, fakes, state transitions, test cases and citations. Added AC10–AC15.
- Open: NEW-GAP-S9-2, NEW-GAP-S9-7, NEW-GAP-A1 and the remaining part of GAP-2162 (outbound actions and right-enforcement path).
- Cited the Test Cases v9 IDs of AC10–AC15 and moved the message standard citations to version 6, where MSG-P4-001 covers a missing session or role.

| Item | Value |
|---|---|
| Story key | RWB-P1-AD018-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-001; RD-P1-004; RD-P1-005; RD-P1-011; RD-P1-012; RD-P1-020; RD-P1-021; RD-P1-024; RD-P1-040 |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified |
| Depends on (build) | P2 rwb-integration scheduled-jobs contract provider; RWB-P1-E1015-CON |
| Contract dependencies | P2 rwb-integration scheduled-jobs contract; RWB-P1-E1015-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v3.md (no FR mapped; no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-018 for rwb-source-data. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 8 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: P1 developer readiness (RD-P1 register); story editor S9-stories.

### 1. Story

As a **rwb-source-data contract owner**, I want **one contract for P1 job run history and reruns, with the P2 catalogue and E1015 freshness boundaries explicit**, so that **the APP and OPS stories build against the same published schemas and ownership**.

RWB-P1-AD018-CON is the sole publisher of the job list and rerun operations (RD-P1-012 X-17). The contract describes one item per run for the four P1 workflow types and the run tables owned by rwb-source-data. `job_catalog` remains P2-owned. The case list and its checks are outside P1 (RD-P1-020, RD-P1-021, RD-P1-024).

### 2. Business rationale

The contract fixes the P1 run history and rerun surface once. The list is one item per run, so each retry remains visible; the run uuid is the resource id used by rerun. The P1 runner owns the run records, while P2 owns the job catalogue and E1015 owns freshness (RD-P1-012, RD-P1-020, RD-P1-021).

This story is the sole publisher by X-17. It does not republish E1002-CON operations, other services' jobs, or the rwb-case list. Case-list checks and statuses are absent from the contract (RD-P1-024).

### 3. Preconditions

- API Specification v7 contract baseline is the published version `rwb-source-data.yaml` 5.1.0.
- The P2 scheduled-jobs contract is available for `job_catalog`; P1 does not own or publish that table (RD-P1-021).
- RWB-P1-E1015-CON owns freshness schemas; this contract references them without restating fields.
- RD-P1-020 defines `job_run` and `job_run_check` fields, constraints and dictionary identifiers.
- RD-P1-012 defines one item per run, P1 job set, Job shape, query fields and rerun responses.
- Shared Problem schema and Error and Message Standard v6 govern error envelopes and messages.

### 4. Flow

1. Publish the two P1 operations on `/api/recovery/source-data/v1`: `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun`.
2. Define `JobPage`, one Job item per P1 run, query parameters and paging exactly as RD-P1-012.
3. Define the five run states and the `job_run` / `job_run_check` shapes from RD-P1-020.
4. Define rerun by FAILED run uuid, no body, UUID Idempotency-Key, 202 response and the status/message IDs in RD-P1-012.
5. Reference P2 scheduled-jobs and E1015 freshness contracts; publish no schemas for their tables or responses.
6. Publish version-pinned provider/consumer fakes and compatibility checks for the app, operations and harness stories.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | Rerun key missing, blank or not a UUID | 400 Problem response | MSG-PLT-N009-03 |
| X2 | Unknown or non-P1 run uuid | 404 Problem response | MSG-P4-003 |
| X3 | Target run is not FAILED or an open same-type/date run exists | 409 Problem response | MSG-P1-011 |
| X4 | ACE batch is not `COMPLETED` | 409 Problem response | MSG-P1-001 |
| X5 | Idempotency key is reused | 409 Problem response | MSG-PLT-N009-05 |
| X6 | P1 store unavailable | 503 Problem response | MSG-GEN-006 |
| X7 | No session or Workbench role; missing right | 401; 403 Problem response | MSG-P4-001; MSG-P4-002 |
| X8 | List query malformed or outside its list | 400 Problem response | MSG-GEN-001; MSG-GEN-007 |
| X9 | List query out of range, or `from` later than `to` | 422 Problem response | MSG-GEN-002; MSG-GEN-003 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reuses the platform envelopes and the published documents of rwb-source-data and rwb-integration |
| Negotiable | Examples and fixture values; the two operations, the status list and the error table are fixed by RD-P1-012 and RD-P1-004 |
| Valuable | Unblocks the app, operations and test stories and fixes the meaning of a wait state for the operator |
| Estimable | Two operations, two run tables, one consumed operation, its fakes and contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: AD018 P1 job contract

  Scenario: AC1 Job list contract is complete and paged
    Given OpenAPI 3.1 document `rwb-source-data.yaml` version 5.1.0
    When the schema and compatibility checks run
    Then GET /admin/jobs declares `JobPage {items, page, size, total}` and one Job item per run ordered by startedAt descending
    And the query is type, status, from, to, page and size with RD-P1-012 defaults and bounds
    And Job fields include id, type, jobName, workflowId, runNo, businessDate, status, startedAt, endedAt, durationMinutes, lastAceBusinessDate and checks
    And id, type, businessDate and status are required and endedAt and durationMinutes are nullable

  Scenario: AC2 Job types and run checks match the rulings
    Given the P1 job set and the JOB-04 results
    When contract schemas and examples are validated
    Then types are AceIngestCheck, JOB-04 ReconciliationWorkflow, Stage2ProductWorkflow and RetentionRunWorkflow
    And JOB-04 checks use REC-01, REC-02 and REC-05
    And no case-list workflow, table, check or status is declared
    And migration runs are excluded; each migration owner reads its own Flyway history (RD-P1-012)

  Scenario: AC3 Rerun contract matches RD-P1-012
    Given POST /admin/jobs/{jobId}/rerun
    When its request and responses are validated
    Then jobId is the run uuid of a FAILED run, the operation has no body, and UUID Idempotency-Key is required
    And accepted response is 202 with a new PENDING Job and runNo increased by one
    And 400, 404, 409 and 503 message IDs match section 14

  Scenario: AC4 Run and check schemas match RD-P1-020
    Given schemas for `job_run` and `job_run_check`
    When names, types, nullability, keys and dictionary IDs are compared to RD-P1-020
    Then all DF-OPS-233 to DF-OPS-251 fields and constraints match
    And each Job checks object is backed by one row per check

  Scenario: AC5 Ownership boundaries are explicit
    Given contract paths and table ownership rows
    When compared with RD-P1-021 and RD-P1-024
    Then job_catalog is P2-owned and read through `GET /api/recovery/integration/v1/admin/scheduled-jobs`
    And freshness schema is referenced from E1015-CON without restating it
    And no P1 case-list artifact is present
    And no outbound-action property is declared on the job list

  Scenario: AC6 Provider and consumed fakes are pinned
    Given the P2 scheduled-jobs fake, ACE batch fixture, run-store fixture and role fixture
    When contract drift checks run against `rwb-source-data.yaml` 5.1.0
    Then every fake uses the published shapes and drift fails the build

  Scenario: AC7 Problem responses use the shared schema
    Given each documented rerun error condition
    When the OpenAPI response schemas are checked
    Then the published Problem properties and message IDs match RD-P1-001 and RD-P1-004
    And no unapproved message text or ID is introduced

  Scenario: AC8 All changed contract examples validate
    Given one example for each run state and rerun response
    When OpenAPI validation runs
    Then each well-formed example passes and malformed enum, UUID and paging values fail with the documented response

  Scenario: AC9 Job monitor feature switch is published
    Given the `rwb.p1.jobmonitor` switch is off
    When the job list or rerun operation is requested
    Then the operation answers 404 `MSG-P4-003` and a refused rerun creates no run row
    And the switch starts and stops no workflow and does not gate the freshness operation

  Scenario: AC10 Rerun refused by run state
    Given contract examples of runs in PENDING, RUNNING, COMPLETE and WAITING
    When each is rerun
    Then the declared answer is 409 with messageCode MSG-P1-011 and no Job body

  Scenario: AC11 Idempotent replay
    Given a rerun accepted with key K
    When K is sent again to the same path within 24 hours, and then to another run path
    Then the first answer is the stored 202 Job
    And the second is 409 MSG-PLT-N009-05

  Scenario: AC12 Query boundaries
    Given the list parameters
    When status is unknown, from is malformed, from is later than to, or size is 201
    Then the declared answers are 400 MSG-GEN-007, 400 MSG-GEN-001, 422 MSG-GEN-003 and 422 MSG-GEN-002
    And a well-formed range with no run answers 200 with empty items and total 0

  Scenario: AC13 Two runs of one job are readable
    Given a FAILED run_no 1 and a run_no 2 for 2026-11-30
    When the list example is validated
    Then both items are present, ordered by startedAt descending

  Scenario: AC14 Access answers
    Given a caller with no session and a caller without the required right
    When either operation is called
    Then the declared answers are 401 MSG-P4-001 and 403 MSG-P4-002

  Scenario: AC15 Consumer compatibility
    Given the recorded expectations of RWB-ITG-AD018-ITG, RWB-PLT-E1056-OPS and RWB-P1-AD018-OPS
    When they are verified against the 5.1.0 document and fake
    Then no path, field, filter, status value or message ID they use is missing
```

Test references: AC1–AC6 TC-P1-AD018-CON-01 to -06; AC7 TC-P1-AD018-CON-08; AC8 TC-P1-AD018-CON-09; AC9 TC-P1-AD018-CON-10. Test Cases v9 holds the rows for the changed texts of AC1, AC5 and AC9.

AC10 TC-P1-AD018-CON-11; AC11 TC-P1-AD018-CON-12; AC12 TC-P1-AD018-CON-13; AC13 TC-P1-AD018-CON-14; AC14 TC-P1-AD018-CON-15; AC15 TC-P1-AD018-CON-16 (Test Cases v9).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service; AD018-CON publishes only its P1 job list and rerun operations | DP-13; RD-P1-012 |
| BR2 | P1 job list contains one item per P1 run, ordered by `startedAt` descending | RD-P1-012 |
| BR3 | Rerun targets a FAILED run uuid, has no body, requires UUID Idempotency-Key and returns 202 | RD-P1-001; RD-P1-012 |
| BR4 | Rerun errors use the IDs and status codes of RD-P1-012 and RD-P1-001 | RD-P1-001; RD-P1-012 |
| BR5 | Run status is PENDING, RUNNING, COMPLETE, FAILED or WAITING | RD-P1-012 |
| BR6 | `job_run` / `job_run_check` shapes and constraints follow RD-P1-020 | RD-P1-020 |
| BR7 | `job_catalog` is P2-owned; P1 reads it only through the P2 contract | RD-P1-021 |
| BR8 | No case-list operation, table, schedule or check is declared in P1 | RD-P1-024 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, `JobPage`, `Job`, the run tables and the run states are described | In review |
| In review | Consumer sign-off | The app, operations and integration-test stories, RWB-PLT-E1056-OPS, RWB-P1-E1015-CON and RWB-PLT-N001-CON accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or the status list changes | New major version drafted |
| Baselined | Drift in a fake | The drift test of AC6 fails | In review |
| Baselined | Retired element reappears | The absence checks of AC2 or AC5 fail | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the OpenAPI document and the provider fake; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the field-level detail of the run log |
| Consuming teams (app, operations, test, the P2, P4 and P1 sibling owners, RWB-PLT-N001-CON) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the CloudEvents envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer or a fake |

The published security scheme is `entraId` (openIdConnect). The list needs Platform administration R and the rerun Platform administration U; the right-enforcement path stays open under GAP-2162.

### 11. Data

| Entity | Schema | Fields and IDs | Owner and role |
|---|---|---|---|
| `job_run` | `rwb_source_data` | DF-OPS-233 to DF-OPS-245; `id`, `job_type`, `business_date`, `run_no`, `status`, `workflow_id`, `started_at`, `finished_at`, `duration_minutes`, `message_id`, `requested_by`, `idempotency_key`, `rerun_of_id` | P1 operational run record |
| `job_run_check` | `rwb_source_data` | DF-OPS-246 to DF-OPS-251; `id`, `job_run_id`, `check_code`, `check_result`, `check_count`, `expected_count` | P1 check record |
| `job_catalog` | `rwb_integration` | DF-OPS-224 to DF-OPS-232 | P2 catalogue, read through P2 contract only |
| `data_product_load` | `rwb_source_data` | E1015 freshness schema | P1-owned, written by E1015-APP; schema owned by E1015-CON |

`job_run` constraints are `uk_job_run`, `uk_job_run_idempotency`, `ix_job_run_latest` and `fk_job_run_rerun_of`; `job_run_check` has `uk_job_run_check`. Field lengths and rules follow RD-P1-020 exactly. `job_catalog` is not a P1 table. `case_list_row` and its retired dictionary entry are not a P1 runtime table (RD-P1-024).

`Job` has no run book property. The NFR-067 run book path (DF-OPS-229) stays in the P2 catalogue and is read through the P2 contract.

### 12. Contract

#### 12.1 REST operations provided

Owner RWB-P1-AD018-CON; base `/api/recovery/source-data/v1`; `rwb-source-data.yaml` 5.1.0.

| Method | Path | Response and query | Access |
|---|---|---|---|
| GET | `/admin/jobs` | `JobPage {items: Job[], page, size, total}`; one run per item; query `type`, `status`, `from`, `to`, `page`, `size` | Platform administration R |
| POST | `/admin/jobs/{jobId}/rerun` | `jobId` is failed run uuid; no request body; UUID `Idempotency-Key`; 202 returns new PENDING Job | Platform administration U |

`Job` fields: `id` uuid (required), `type` string (required), `jobName` string, `workflowId` string, `runNo` integer, `businessDate` date (required), `status` enum (required), `startedAt` date-time, `endedAt` date-time or null, `durationMinutes` integer or null, `lastAceBusinessDate` date, and `checks` object. `endedAt` and `durationMinutes` are nullable; another optional property is omitted while it has no value (a WAITING run has no `startedAt`). `checks` is keyed by check code; each value is `{expected:number, actual:number, passed:boolean}`, all three required, projected from `job_run_check` as `expected_count`, `check_count` and `check_result` = PASS. JOB-04 check codes are REC-01, REC-02 and REC-05. Status is PENDING, RUNNING, COMPLETE, FAILED or WAITING.

Errors are the shared `Problem` schema as `application/problem+json`: required `type`, `title`, `status`, `messageCode` and `traceId`; optional `detail`, `instance`, `messageTh`, `field` and `errors` (RD-P1-004). Pending: the derivation of `lastAceBusinessDate` for several sources, the rounding of `durationMinutes` and the control totals per check, owner contract owner with the data owner, tracked as NEW-GAP-S9-7.

Query fields are `type`, `status`, `from`, `to`, `page` and `size`; dates are inclusive business dates in Asia/Bangkok. `from` defaults to today minus 7 days; `to` defaults to today; `page` defaults to 0; `size` defaults to 50, minimum 1 and maximum 200. `JobPage` has `items`, `page`, `size` and `total`. Sorting is `startedAt` descending.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/admin/scheduled-jobs` | P2 rwb-integration | Read P2-owned `job_catalog`, one hop, 2 s, GET retried once with jitter; on failure the run items are returned without `jobName` |

#### 12.3 Events published

None. Event types `AceDataReady` and `AceDataLate` are published by E1015-APP on topic `rwb.source-data.events.v1`.

#### 12.4 Events consumed

None by AD018; no Kafka consumer is declared.

#### 12.5 Workflows and activities

Rerun starts the workflow for the failed P1 run type: `AceIngestCheck`, `ReconciliationWorkflow` (JOB-04), `Stage2ProductWorkflow` or `RetentionRunWorkflow`. No case-list workflow is registered.

#### 12.6 Schedules

None for job monitoring or the case list. No `DailyCaseList` schedule exists in P1.

#### 12.7 Tables owned

| Table | Owner | Purpose |
|---|---|---|
| `job_run` | P1 `rwb_source_data` | One row per attempt |
| `job_run_check` | P1 `rwb_source_data` | One row per check |
| `data_product_source` | P1 `rwb_source_data` | Product-to-source map |
| `data_product_load` | P1 `rwb_source_data` | Freshness stamp; E1015-APP writes |

#### 12.8 Contract fakes

Provider fake for the two P1 operations: WireMock mappings generated from `rwb-source-data.yaml` 5.1.0, one per declared status, released at `fakes/rwb-source-data/5.1.0/` in RWB-PLT-LIB and never edited by a consumer (RD-P1-011). The consumed fake for the P2 scheduled-jobs contract pins its published provider version. Fixtures cover the four P1 run types, each run status, two runs of one job and date, REC-01/02/05 checks, an empty page, the rerun errors, ACE `COMPLETED` and incomplete states, and missing session or right.

#### 12.9 Call-type summary

| Call type | Detail |
|---|---|
| REST | Two P1 operations provided; one P2 scheduled-jobs operation consumed |
| Kafka | None |
| Temporal | Rerun targets existing P1 workflows; no case-list workflow |
| File | None |

### 13. Solution plan

**Provider artifacts:** `rwb-source-data.yaml` 5.1.0 with the P1 job history and rerun operations, `JobPage`, `Job`, shared Problem responses, provider fake and compatibility checks.

**Consumed artifact:** P2 scheduled-jobs contract for `job_catalog` metadata. Freshness remains the E1015-CON contract and is not restated.

**Data artifacts:** `job_run` and `job_run_check` with DF-OPS-233 to DF-OPS-251 from RD-P1-020. The contract creates no `job_catalog` or case-list entity.

### 14. Validation and messages

| Condition | Status and message ID |
|---|---|
| Invalid Idempotency-Key | 400 `MSG-PLT-N009-03` |
| Unknown or non-P1 run uuid | 404 `MSG-P4-003` |
| Target not FAILED or same-type/date run is open | 409 `MSG-P1-011` |
| ACE batch not `COMPLETED` | 409 `MSG-P1-001` |
| Reused key | 409 `MSG-PLT-N009-05` |
| Store unavailable | 503 `MSG-GEN-006` |
| No session or no Workbench role; missing right | 401 `MSG-P4-001`; 403 `MSG-P4-002` |
| List query malformed; value outside its list | 400 `MSG-GEN-001`; 400 `MSG-GEN-007` |
| List query value out of range; `from` later than `to` | 422 `MSG-GEN-002`; 422 `MSG-GEN-003` |
| Switch `rwb.p1.jobmonitor` off | 404 `MSG-P4-003` |

No message text is copied from stale v4 guidance or invented here.

### 15. Screens and states

SCR-44 Interface and job monitor is served through the gateway-bff composite route (DP-19). This contract supplies the run list (all five statuses) and the rerun; freshness comes from RWB-P1-E1015-CON. The screen composition and field list belong to RWB-PLT-N001-CON, and RWB-P1-AD018-OPS registers the route and its alerts. The empty, loading, error and no-access states are listed in RWB-P1-AD018-OPS section 15.

### 16. Test cases

| AC | Test reference |
|---|---|
| AC1–AC6 | TC-P1-AD018-CON-01 to TC-P1-AD018-CON-06 |
| AC7, AC8, AC9 | TC-P1-AD018-CON-08, TC-P1-AD018-CON-09, TC-P1-AD018-CON-10 |
| AC10, AC11, AC12 | TC-P1-AD018-CON-11, TC-P1-AD018-CON-12, TC-P1-AD018-CON-13 |
| AC13, AC14, AC15 | TC-P1-AD018-CON-14, TC-P1-AD018-CON-15, TC-P1-AD018-CON-16 |

Test Cases v9 holds the rows of the changed criteria (AC1, AC5, AC9).

### 17. Guardrails

- Publish only operations owned by rwb-source-data.
- Keep `job_catalog` with P2 and use its contract; no local P1 copy.
- Keep P1 run tables and fields aligned with RD-P1-020.
- Use E1015-CON for freshness fields.
- Do not declare case-list paths, tables, checks, schedules or messages in P1.
- Use shared Problem schema and current Error and Message Standard v6.

### 18. Traceability

| Requirement | Source | Test reference |
|---|---|---|
| One P1 contract owner and one item per run | RD-P1-012 X-17 | TC-P1-AD018-CON-01 |
| P1 run table schema and checks | RD-P1-020 | TC-P1-AD018-CON-04 |
| P2 job catalogue ownership | RD-P1-021 | TC-P1-AD018-CON-05 |
| Case list remains outside P1 | RD-P1-024 | TC-P1-AD018-CON-02 |
| NFR-067 run book path stays in the P2 catalogue | LDM DF-OPS-229 | TC-P1-AD018-CON-05 |

### 19. Out of scope

- The implementation of the two reads, the rerun and the run log (RWB-P1-AD018-APP).
- The deployment, the migration, the dashboards, the alerts and the run books (RWB-P1-AD018-OPS, RWB-PLT-E1056-OPS).
- The freshness resource and its stamp semantics (RWB-P1-E1015-CON, RWB-P1-E1015-APP) and the ACE read path (RWB-P1-E1069-CON).
- The screen field list and the composite route (RWB-PLT-N001-CON).
- The P2 outbound-action contract itself: consumed and faked, never defined here; the real journey is RWB-ITG-AD018-ITG.
- The Platform administration roles and their assignment (RWB-P4-AD001 to RWB-P4-AD016).

### Remaining delivery steps

- Size: Pending squad refinement; owner delivery lead.
- Epic design sign-off: Pending; owner solution architect.
- CON Done: Pending; owner contract owner.
- Contract fake published at the approved version: Pending; owner contract owner.
- Synthetic test data in DEV: Pending; owner test data owner.