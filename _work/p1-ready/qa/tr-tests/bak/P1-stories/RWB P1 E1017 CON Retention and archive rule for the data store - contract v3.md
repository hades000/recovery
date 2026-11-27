# RWB-P1-E1017-CON Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

### Version 3 changes

- RD-P1-047 (with X-04), RD-P1-001 and RD-P1-004: the two operations and their schemas as published in `rwb-source-data.yaml` 5.1.0, one status and message code table, workflow ID `retention-run-{runDate}` and the rwb-case reads of `rwb-case.yaml` 5.1.0 (findings #1 to #4, #6 to #8, #11).
- RD-P1-048 with RD-P1-024 (X-01): seven tables, ARCHIVE and REVIEW only, periods Pending with Compliance (GAP-1029).
- RD-P1-002 and RD-P1-011: the eight catalogue activities and the provider fake rules; AC14 to AC17 added (findings #9, #12, #14, #16, #17).
- Open items are listed in section 20 (findings #5, #10, #13, #15 in part).
- Finishing pass (requests W2-tests-1065, W3-messages-0043, W5-runtime-0071, F16-affected-0094; test case backfill): every criterion cites its live Test Cases v9 row.

| Item | Value |
|---|---|
| Story key | RWB-P1-E1017-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-E1017-CON-16) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7; base `/api/recovery/source-data/v1`) |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15 |
| Readiness decisions | RD-P1-001; RD-P1-002; RD-P1-004; RD-P1-005; RD-P1-011; RD-P1-024; RD-P1-047; RD-P1-048 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1021-CON; rwb-case.yaml 5.1.0 (held/open exclusions and closure dates) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-028) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-017 for rwb-source-data. The retention run is published as a contract of this service so that P5's JOB-17 can start it on Day 1 without this service being built, and so that a held case is answered by rwb-case over an interface with a fake rather than by a read of its table. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1017-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied RD-P1-001; RD-P1-002; RD-P1-004; RD-P1-005; RD-P1-011; RD-P1-024; RD-P1-047; RD-P1-048.

### 1. Story

As a **solution architect**, I want the REST and Temporal contract for P1's retention action, including `POST /retention-runs`, `GET /retention-runs/{runId}`, the P3 retention-exclusions and closure-dates reads, and the run schemas, so P5 can pass its rule rows to P1 and read the result while P1 applies only the ruled ARCHIVE and REVIEW behavior. Period values remain Pending, owner Compliance, tracked as GAP-1029. The seven P1 tables are `interaction` (ARCHIVE) and `party_ext`, `account_ext`, `contact_point_ext`, `valuation_ext`, `dp_treatment`, `dp_guarantee_claim` (REVIEW only); `case_list_row` is excluded under RD-P1-024 (X-01).

### 2. Business rationale

P5 owns the retention rules, their approval and JOB-17. P1 receives the rule version, run date and rule rows through one REST start, then exposes a run record for P5 and Compliance to read. P1 does not own a retention period. Compliance periods are Pending under GAP-1029.

RD-P1-047 fixes the P1 and P3 contract boundaries. P1 accepts asynchronous starts and P3 supplies the held/open exclusion set and closure dates over its contract. RD-P1-048 limits the P1 action to ARCHIVE for `interaction` and REVIEW for six tables; REVIEW counts selected rows as LISTED and does not archive or delete them. P1 never destroys archive objects. The archive target and layout remain Pending under GAP-0490.

### 3. Preconditions

- The sole REST contract is `rwb-source-data.yaml` 5.1.0 in API Specification v7 (RD-P1-005); this story adds the retention operations to that file rather than creating a second OpenAPI file.
- `RWB-P3-E1021-CON` is the provider dependency for `retention-exclusions` and `closure-dates` (RD-P1-047). Both reads are published in `rwb-case.yaml` 5.1.0 (API Specification v7); RWB-P3-E1021-CON publishes their fake.
- `RWB-PLT-E1071-CON` supplies the Temporal workflow kit, namespace `rwb-recovery` and task queue `rwb-source-data`.
- `RWB-PLT-E1027-CON` supplies the decision-record library; payload, key, transaction timing and failure behavior remain Pending under GAP-2426.
- The two platform contracts above are used as published artefacts; neither blocks writing this contract, so the header lists no build dependency.
- The archive container, identity grant, object path and manifest shape are not fixed for P1; Pending, owner solution architect/storage architect, GAP-0490.
- The six REVIEW tables and `interaction` are P1's; `case_list_row` is excluded because RD-P1-024 (X-01) removes it from P1.
- Compliance periods are Pending under GAP-1029. No period is placed in this contract as a default or example.
- The rwb-document workflow must use an ID that does not collide with P1's ID in namespace `rwb-recovery`; this is Pending under NEW-ASM-X3, owner rwb-document solution architect.

### 4. Flow

1. Extend `rwb-source-data.yaml` 5.1.0 with the two operations on `/api/recovery/source-data/v1` and the schemas in section 11.
2. Define the required start body `{ruleVersion, runDate, rules[]}`; each rule has `productCode`, `tableName`, `recordClass`, integer `retentionMonths`, `ageBasis` and `endAction` (`ARCHIVE` or `REVIEW`). The request carries the Compliance-owned period; the contract sets no period value.
3. Require a UUID `Idempotency-Key` on POST. Apply the platform response-store rule: same key and request replays the stored response, a changed endpoint/body answers 409 MSG-PLT-N009-05, and a missing or non-UUID key answers 400 MSG-PLT-N009-03 (RD-P1-001).
4. On an accepted start, answer `202 {runId, status: ACCEPTED}`. A run date already RUNNING or COMPLETED answers 409 MSG-P2-006. A new key after FAILED may start a new execution with 202. The workflow ID is `retention-run-{runDate}`, conflict policy FAIL and reuse policy ALLOW_DUPLICATE_FAILED_ONLY (RD-P1-001; RD-P1-047).
5. On a refused rule set, answer 422 with the code of section 5 and `field` as a JSON Pointer to the first failing input, for example `/rules/0/retentionMonths`, and do not start the run. The body is the published Problem schema with no member added (RD-P1-004).
6. `GET /retention-runs/{runId}` returns the status and `countsPerTable[] {tableName, selected, archived, deleted, listed, held}`, plus `archiveLocation` and `holdReport`. Status values are RUNNING, COMPLETED or FAILED (ACCEPTED belongs to the POST answer only). Pending: `holdReport` fields, owner solution architect, NEW-GAP-S5-1.
7. P1 consumes `GET /api/recovery/case/v1/cases/retention-exclusions?page=&size=` and `GET /api/recovery/case/v1/cases/closure-dates?closedBefore=&page=&size=` from P3. Each call has a one-hop 2 s budget. P1 reads exclusions at run start and again before every interaction delete unit; unreadable answers fail the run before the affected selection/deletion (RD-P1-047; RD-P1-048).
8. P1 archives only `interaction`, verifies its archive copy, then deletes corresponding live rows. It lists the six REVIEW tables as LISTED and neither archives nor deletes them. Archive path and manifest shape remain Pending under GAP-0490.
9. The P1 `RetentionRunWorkflow` is started by the REST handler and runs on task queue `rwb-source-data` in namespace `rwb-recovery`; P5's Schedule remains in rwb-document. P1 publishes no retention domain event. The DP-03 decision-record details remain Pending under GAP-2426.

### 5. Exception paths

| ID | Trigger | Contract answer or run result | Message | Covered by |
|---|---|---|---|---|
| X1 | Missing or non-UUID `Idempotency-Key` | 400 Problem; handler is not invoked | MSG-PLT-N009-03 | AC5 |
| X2 | Same UUID key with a different request body | 409 Problem; stored response is unchanged | MSG-PLT-N009-05 | AC5 |
| X3 | A new key starts a run date whose run is RUNNING or COMPLETED | 409 Problem; `detail` holds the stored `runId` | MSG-P2-006 | AC6 |
| X4 | A table, table and action pairing or `ageBasis` check fails | 422 Problem; no run starts | MSG-P1-002 | AC7, AC16 |
| X5 | POST or GET caller has no valid token | 401 Problem | MSG-P4-001 | AC11 |
| X6 | Caller has no Platform administration U right on POST, or R right on GET | 403 Problem | MSG-P4-002 | AC11 |
| X7 | A requested runId does not exist | GET answers 404 Problem | MSG-P4-003 | AC12 |
| X8 | An rwb-case exclusion or closure-date answer cannot be read within 2 s | Accepted run ends FAILED before the affected selection or delete | None on the wire; Pending: run failure detail on GET, NEW-GAP-S5-10 | AC8 |
| X9 | An authorise or other required dependency is unavailable before the 202 | 503 Problem; no start is accepted | MSG-GEN-006 | AC11 |
| X10 | The request body cannot be read | 400 Problem | MSG-GEN-001 | AC17 |
| X11 | A required value is missing or `rules` is empty | 422 Problem; no run | MSG-GEN-001 | AC16 |
| X12 | `retentionMonths` outside 1 to 600 | 422 Problem; no run | MSG-GEN-002 | AC17 |
| X13 | `productCode` or `endAction` not in its list | 422 Problem; no run | MSG-GEN-007 | AC16 |

The run result is `FAILED` for an error after the asynchronous 202; the POST answer already sent does not change. The status and code rows follow the table of RD-P1-004.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Contract-first work against API Specification v7, the Temporal kit and the P3 contract dependency |
| Negotiable | Retention periods, archive layout and DP-03 mapping remain assigned to their owners and are not invented here |
| Valuable | P5 can start P1 over the published REST surface and read P1's run record |
| Estimable | Two REST operations, schemas, one workflow contract, P3 dependency, Problem mapping and fake fixtures |
| Small | Contract and fake work for one service capability |
| Testable | Each acceptance criterion checks a schema, answer, fake, compatibility rule or named dependency |

### 7. Acceptance criteria

```gherkin
Feature: Retention-run contract for rwb-source-data

  Scenario: AC1 The published YAML has the retention operations and response codes
    Given `rwb-source-data.yaml` version 5.1.0 in API Specification v7
    When the OpenAPI document is checked against its declared schema
    Then it has POST `/retention-runs` and GET `/retention-runs/{runId}` on the P1 base
    And POST declares 202, 400, 401, 403, 409, 422 and 503 responses
    And GET declares 200, 400, 401, 403, 404 and 503 responses
    And every 4xx and 5xx response is `application/problem+json` with the published Problem schema
    TC: TC-P1-E1017-CON-01

  Scenario: AC2 The start request carries the ruled property names
    Given the published `RetentionRunRequest` schema
    When a request schema is inspected
    Then it requires `ruleVersion`, date-formatted `runDate` and `rules`
    And each rule requires `productCode`, `tableName`, `recordClass`, integer `retentionMonths`, `ageBasis` and `endAction`
    And `endAction` has only ARCHIVE and REVIEW
    And no retention period is set in this contract
    TC: TC-P1-E1017-CON-02

  Scenario: AC3 The start returns the ruled asynchronous answer
    Given a request with a UUID `Idempotency-Key` and a ruled table/action combination
    When POST `/retention-runs` accepts the request
    Then it answers 202 with UUID `runId` and status ACCEPTED
    And the response has no business counts
    TC: TC-P1-E1017-CON-03

  Scenario: AC4 The GET schema carries the P1 run facts
    Given the fake in each status RUNNING, COMPLETED and FAILED
    When GET `/retention-runs/{runId}` reads the run
    Then each body validates against `RetentionRun`, which requires `status`, `countsPerTable`, `archiveLocation` and `holdReport`
    And `countsPerTable` items require `tableName`, `selected`, `archived`, `deleted`, `listed` and `held`
    And a table of endAction REVIEW shows `listed` with `archived` 0 and `deleted` 0
    And `holdReport` is an object whose fields are Pending, NEW-GAP-S5-1
    TC: TC-P1-E1017-CON-06

  Scenario: AC5 Idempotency follows RD-P1-001
    Given a POST with a UUID key and request body
    When the same key and request are replayed within the platform response window
    Then the stored response status and body are replayed without a second effect
    When the key is reused with a changed endpoint or body
    Then it answers 409 with MSG-PLT-N009-05 and leaves the stored response unchanged
    And a missing or non-UUID key answers 400 with MSG-PLT-N009-03
    TC: TC-P1-E1017-CON-08

  Scenario: AC6 A new start for a running or completed date is refused
    Given a run date whose run is RUNNING or COMPLETED
    When POST uses a new UUID key for that date
    Then it answers 409 with MSG-P2-006 and includes the stored runId in Problem detail
    And a new key after FAILED can start a new execution with 202
    TC: TC-P1-E1017-CON-15

  Scenario: AC7 A refused rule set does not create a run
    Given in separate requests a rule for decision_log_entry, a rule for retention_rule, a rule for case_list_row and a rule with endAction ARCHIVE for party_ext
    When POST `/retention-runs` receives each request
    Then each answers 422 with MSG-P1-002 and a `detail` naming the refused table
    And it does not create a runId or read a table row
    TC: TC-P1-E1017-CON-03, TC-P1-E1017-CON-05, TC-P1-E1017-CON-08

  Scenario: AC8 The P3 reads are published as a dependency
    Given the P3 contract dependency RWB-P3-E1021-CON
    When section 12.2 is compared with the RD-P1-047 interface
    Then it names the retention-exclusions and closure-dates paths and query parameters
    And it states a one-hop 2 s budget and exclusion re-read before every interaction delete unit
    And it does not name a SQL read from `rwb_case`
    TC: TC-P1-E1017-CON-16

  Scenario: AC9 The workflow starts behind REST on the ruled queue
    Given the P1 Temporal contract
    When the workflow contract is inspected
    Then it names `RetentionRunWorkflow`, queue `rwb-source-data`, namespace `rwb-recovery` and ID `retention-run-{runDate}`
    And it declares FAIL and ALLOW_DUPLICATE_FAILED_ONLY
    And POST is the only cross-service start described by this story
    And it names the eight activities of section 12.5
    TC: TC-P1-E1017-CON-12

  Scenario: AC10 The fake covers the published outcomes
    Given the P1 retention-run fake used by P5
    When it is checked against the OpenAPI schema and workflow contract
    Then it returns 202, same-key replay, 400, 401, 403, 409 date conflict, 409 key conflict, 422 refusal, a timeout and 503 on POST
    And on GET it returns RUNNING, COMPLETED, FAILED and 404 for an unknown runId
    And no mapping has a schema violation
    TC: TC-P1-E1017-CON-13

  Scenario: AC11 Access failures use the shared Problem schema
    Given a call with a token that fails verification, without the required right, or while the authorise dependency is unavailable
    When POST or GET is called
    Then the answer is 401 MSG-P4-001, 403 MSG-P4-002 or 503 MSG-GEN-006 respectively
    And no run starts when the POST fails before its 202
    TC: TC-P1-E1017-CON-14

  Scenario: AC12 An unknown runId returns 404
    Given a UUID runId that is not present
    When GET `/retention-runs/{runId}` is called
    Then it answers 404 with MSG-P4-003 in the API Specification v7 Problem response
    TC: TC-P1-E1017-CON-17

  Scenario: AC13 The P5 caller is compatible with the published contract
    Given the P5 retention caller's request and response fixtures
    When they are checked against `rwb-source-data.yaml` 5.1.0
    Then every path, required property, status and response schema matches
    TC: TC-P1-E1017-CON-18

  Scenario: AC14 The consumed rwb-case fake matches the published schemas
    Given the retention-exclusions and closure-dates fake of RWB-P3-E1021-CON
    When it is checked against `rwb-case.yaml` 5.1.0 for no case held, one case held, one open case, one closed case and a 503
    Then every answer validates against `RetentionExclusionsPage`, `ClosureDatesPage` or Problem
    TC: TC-P1-E1017-CON-19

  Scenario: AC15 A breaking change is blocked
    Given a change that removes or retypes a property of the retention schemas within v1
    When the pipeline compares the document with the tagged baseline
    Then the build fails
    TC: TC-P1-E1017-CON-20

  Scenario: AC16 Missing values and values outside a list
    Given in separate requests an empty `rules` list, a body without `runDate`, a `productCode` outside its list and an `endAction` "DELETE"
    When POST `/retention-runs` receives each
    Then the first two answer 422 with MSG-GEN-001 and `field` "/rules" and "/runDate"
    And the last two answer 422 with MSG-GEN-007
    And no run is created
    TC: TC-P1-E1017-CON-21

  Scenario: AC17 Range and readability of the request
    Given requests with `retentionMonths` 1, 600, 0 and 601, and a body that is not readable JSON
    When POST `/retention-runs` receives each
    Then 1 and 600 are accepted with 202
    And 0 and 601 answer 422 with MSG-GEN-002 and `field` "/rules/0/retentionMonths"
    And the unreadable body answers 400 with MSG-GEN-001
    TC: TC-P1-E1017-CON-22
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | P5 owns the rule rows, their approval and JOB-17; P1 accepts the rows in its request and does not set a period | RD-P1-047; RD-P1-048; ASM-0076 |
| BR2 | ARCHIVE is allowed only for `interaction`; the six other in-scope tables are REVIEW only, counted as LISTED without archive or delete | RD-P1-048 final ruling |
| BR3 | `case_list_row` is excluded from P1; the in-scope list is seven tables | RD-P1-024 (X-01); RD-P1-048 final ruling |
| BR4 | P1 reads P3 held/open exclusions and closure dates through the named contract; it never reads `rwb_case` tables | RD-P1-047; DP-01 |
| BR5 | P1 reads exclusions at run start and before each interaction delete unit; a newly held or reopened case is dropped from the unit | RD-P1-048 |
| BR6 | Interaction age uses P3 `closedAt`; the boundary row is kept, dates compare as dates and timestamptz values compare in Asia/Bangkok | RD-P1-048 |
| BR7 | Interaction selection filters `retention_class = recordClass`; correction chains are archived/deleted together, sequence gaps are accepted for closed cases, and deleted idempotency keys are not reused | RD-P1-048 item 6 |
| BR8 | A refused rule set is refused in full; the start is asynchronous and the run is read from GET | RD-P1-047 |
| BR9 | P1 uses the UUID Idempotency-Key and response-store behavior of RD-P1-001 | RD-P1-001 |
| BR11 | `retentionMonths` is a whole number from 1 to 600 | RWB-E1-017 AC4; MSG-GEN-002 |
| BR10 | Decision-record mapping is not inferred by this contract story; its payload/key/timing/failure behavior are Pending under GAP-2426 | D-RCV-60 review; GAP-2426 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No run for the date | POST answered 202 ACCEPTED | Rules pass whole-set validation | RUNNING |
| RUNNING | All units finish | `interaction` archive units verify and REVIEW rows are counted as LISTED | COMPLETED |
| RUNNING | A unit or required rwb-case read fails | No unverified interaction row is deleted; prior committed units stay recorded | FAILED |
| FAILED | New POST key | The previous execution for that date is FAILED | RUNNING; new run execution |
| RUNNING or COMPLETED | New POST key for the same date | RD-P1-047 conflict rule | No state change; 409 MSG-P2-006 |

### 10. Authority

| Caller or owner | Contract right or responsibility |
|---|---|
| rwb-document service identity | Starts a retention run through POST and reads it through GET; exact identity grant is managed through rwb-access under GAP-2429 |
| RW-PLATADM | Platform administration U for POST and R for GET, as declared in API Specification v7 |
| RW-COMPLY | Reads a run through GET; does not set periods in this P1 contract |
| rwb-case (P3) | Owns held/open exclusions and closure dates through RWB-P3-E1021-CON |
| Compliance | Owns the retention periods; Pending under GAP-1029 |
| Solution architect | Owns unresolved request/response design and DP-03 mapping items identified in this story |

### 11. Data

The wire names below follow `rwb-source-data.yaml` 5.1.0 (API Specification v7). Retention periods are not defaults or examples; they are supplied in rules owned by P5 and remain Pending with Compliance under GAP-1029.

| Contract object | Properties and source |
|---|---|
| `RetentionRunRequest` | Required `ruleVersion` (string), `runDate` (date), `rules` (array). Each rule requires `productCode` (string), `tableName` (string), `recordClass` (string), `retentionMonths` (integer), `ageBasis` (string), and `endAction` (ARCHIVE or REVIEW). |
| Idempotency header | `Idempotency-Key`, required UUID in canonical lowercase 8-4-4-4-12 form; response store scope and 24-hour expiry follow RD-P1-001. |
| `RetentionRunAccepted` | Required `runId` (UUID) and `status` (constant ACCEPTED). |
| `RetentionRun` | Required `status` (RUNNING, COMPLETED or FAILED), `countsPerTable` (array), `archiveLocation` (string) and `holdReport` (object). No failure member is published. |
| `RetentionTableCount` | Required `tableName`, integer `selected`, `archived`, `deleted`, `listed` and `held`. |
| `holdReport` | Object. Field details Pending, owner solution architect, NEW-GAP-S5-1. |
| `archiveLocation` | String; concrete container, path and manifest layout Pending, owner solution architect/storage architect, GAP-0490. |
| `Problem` | Required `type`, `title`, `status`, `messageCode`, `traceId`; optional `detail`, `instance`, `messageTh`, `field`, `errors[]` `{field, messageCode, detail}`; no other member (RD-P1-004). |
| P3 `retention-exclusions` item | `{caseId, caseNumber, reason: LEGAL_HOLD|OPEN, closedAt (null unless reason is absent), accountKeys[], personKeys[]}`; paged by `page` and `size`. |
| P3 `closure-dates` item | `{caseId, closedAt, accountKeys[], personKeys[]}` for closed, unheld cases; paged by `closedBefore`, `page` and `size`. |
| Table/action boundary | Seven tables only: ARCHIVE `interaction`; REVIEW only `party_ext`, `account_ext`, `contact_point_ext`, `valuation_ext`, `dp_treatment`, `dp_guarantee_claim`; `case_list_row` excluded under RD-P1-024 (X-01). |

No period, policy row, table outside this seven-table boundary, archive object key or hold-report subfield is added by this story. String lengths are not declared in the yaml; `retentionMonths` runs 1 to 600. The exact DP-03 decision-record shape and write-failure effect remain Pending under GAP-2426.

### 12. Contract

#### 12.1 REST operations provided

Base: `/api/recovery/source-data/v1`; sole source: `rwb-source-data.yaml` 5.1.0 (API Specification v7).

| Method | Path | Answer and access |
|---|---|---|
| POST | `/retention-runs` | 202 `{runId, status: ACCEPTED}`; 400, 401, 403, 409, 422 and 503 Problem responses. Platform administration U. |
| GET | `/retention-runs/{runId}` | 200 run record; 400, 401, 403, 404 and 503 Problem responses. Platform administration R. |

POST requires UUID `Idempotency-Key`. Same key and same endpoint/body within the 24-hour response window replays the stored response; changed endpoint/body answers 409 MSG-PLT-N009-05. A new key for a run date whose run is RUNNING or COMPLETED answers 409 MSG-P2-006. A new key after FAILED may start a new execution. A refused rule set answers 422 with the code of section 5. Missing or non-UUID key answers 400 MSG-PLT-N009-03 (RD-P1-001; RD-P1-004; RD-P1-047). The caller identity of rwb-document is granted through rwb-access, GAP-2429.

The response schemas are `RetentionRunAccepted`, `RetentionRun`, `RetentionTableCount` and the shared `Problem`. Pending: `holdReport` fields, owner solution architect, NEW-GAP-S5-1; `archiveLocation` path and manifest layout are Pending under GAP-0490.

#### 12.2 REST operations consumed

| Operation | Owner | Use and limit |
|---|---|---|
| `GET /api/recovery/case/v1/cases/retention-exclusions?page=&size=` | RWB-P3-E1021-CON (`rwb-case.yaml` 5.1.0) | Paged cases whose reason is LEGAL_HOLD or OPEN; items include caseId, caseNumber, reason, closedAt, accountKeys and personKeys. Page size 1 to 1,000 with `cursor`. 400, 401, 403, 503. Fake version equals 5.1.0. |
| `GET /api/recovery/case/v1/cases/closure-dates?closedBefore=&page=&size=` | RWB-P3-E1021-CON | Paged closure dates and account/person keys for closed, unheld cases. |

Each call is one hop with a 2 s budget. P1 reads exclusions at run start and before each interaction delete unit. P1 reads no `rwb_case` table. The two reads settle GAP-0491 under RD-P1-047.

#### 12.3 Events published

No retention domain event is published by this story. The service topic `rwb.source-data.events.v1` and its ACE events remain owned by their existing stories. The separate DP-03 decision-record payload, key, transaction timing and failure behavior remain Pending, owner solution architect, GAP-2426; this contract does not claim an event shape.

#### 12.4 Events consumed

None. P5 starts the P1 run through REST. The P1 workflow is internal to rwb-source-data.

#### 12.5 Workflow and activities

| Name | Type | Queue/contract |
|---|---|---|
| `RetentionRunWorkflow` | P1 workflow started by POST | Task queue `rwb-source-data`, namespace `rwb-recovery`; ID `retention-run-{runDate}`; conflict policy FAIL; reuse policy ALLOW_DUPLICATE_FAILED_ONLY |
| `validateRules` | Activity | Refuses the full rule set before row selection if a rule is outside the seven-table/action boundary |
| `casesOnLegalHold` | Activity | Reads P3 retention-exclusions and closure-dates; exclusions are re-read before each interaction delete unit |
| `caseNumbers` | Activity | Reads the case numbers of the held cases for the hold report |
| `selectRows(page)` | Activity | Selects interaction rows by case `closedAt` and recordClass; REVIEW rows are counted as LISTED only |
| `archiveTable` | Activity | Archives selected interaction rows; target path and manifest format Pending under GAP-0490 |
| `verifyManifest` | Activity | Verifies archive copy before live interaction delete |
| `deleteArchivedRows` | Activity | Deletes only verified interaction rows after exclusion re-read |
| `recordRun` | Activity | Records the run status and table counts |

Each of the eight activities is retried with 1 s initial interval, back-off 2 and 10 attempts (Temporal Workflow and Activity Catalog). Activities pass page references and counts, never row content. Pending: start-to-close and heartbeat values, GAP-0143 (ASM-0229). Pending: activity signatures and non-retryable errors, owner workflow architect, NEW-GAP-S5-9. P5's workflow must not reuse P1's workflow ID in the shared namespace (NEW-ASM-X3).

#### 12.6 Schedules

None in P1. JOB-17 belongs to rwb-document (ASM-0076); the P1 action begins with the REST call.

#### 12.7 Tables

| Table | Owner | Retention action in this contract |
|---|---|---|
| `interaction` | P1 | ARCHIVE only; verify the archive copy, re-read P3 exclusions, then delete live rows |
| `party_ext`, `account_ext`, `contact_point_ext`, `valuation_ext`, `dp_treatment`, `dp_guarantee_claim` | P1 | REVIEW only; count selected rows as LISTED; no archive or delete |
| `case_list_row` | Not created in P1 | Excluded by RD-P1-024 (X-01) |
| `retention_rule`, `retention_action` | P5 | Never read or written by P1; rules arrive in the request |
| `decision_log_entry` | P7 | Not a retention target of P1 |

#### 12.8 Contract fakes

**Provider fakes** (published under RD-P1-011 in RWB-PLT-LIB, path `fakes/rwb-source-data/5.1.0/`; the fake version equals the contract version and no consumer edits it).

| Artefact | Contract version | Fixtures |
|---|---|---|
| `postRetentionRuns`, `getRetentionRunsRunid` (WireMock) | `rwb-source-data.yaml` 5.1.0 | POST: 202, same-key replay, 400, 401, 403, 409 date conflict, 409 key mismatch, 422 refusal, 503, timeout. GET: RUNNING, COMPLETED, FAILED, 400, 401, 403, 404, 503 |

**Consumed fakes.**

| Fake | Required answers |
|---|---|
| rwb-case retention-exclusions and closure-dates fake (RWB-P3-E1021-CON, 5.1.0) | Empty set, held case, open case, closed unheld case, timeout and 5xx |
| Archive container stub | Write and read manifest and synthetic interaction rows; refusal and manifest mismatch; exact path and manifest fixture Pending, GAP-0490 |
| Clock fixture | Synthetic runDate and closedAt boundary values; no regulatory period value is fixed |

Fake publication stays Pending until released, owner contract owner (CDC-02994).

#### 12.9 Call-type summary

| Call type | Provided or consumed |
|---|---|
| REST | Two P1 operations provided; two P3 reads consumed, one hop and 2 s |
| Kafka | No retention domain event; DP-03 decision-record details Pending under GAP-2426 |
| Temporal | `RetentionRunWorkflow` on `rwb-source-data` in `rwb-recovery`; activity signatures pending as stated in 12.5 |
| File | `interaction` archive only; target path/manifest Pending under GAP-0490 |
| SQL | P1 tables only; no cross-schema or `rwb_case` reads |

### 13. Solution plan

**Contract artefact.** Add the retention fragment and schemas to `rwb-source-data.yaml` 5.1.0 in API Specification v7. Do not create a story-local OpenAPI or contract YAML as a second REST source.

**Pattern application**

| Pattern | Application |
|---|---|
| DP-01 | P1 reads its own schema; held/open and closure facts come from P3 REST, not SQL |
| DP-03 | Decision-record payload, key, transaction timing and failure effect Pending under GAP-2426 |
| DP-07 | P1 owns no retention policy table; P5's rules arrive in the request |
| DP-10 | P5 owns JOB-17; P1 workflow starts behind its REST endpoint |
| DP-11 | P3 calls are one hop with a 2 s budget |
| DP-13 | Base `/api/recovery/source-data/v1` |
| DP-15 | P1's per-service Flyway migration belongs to the APP/OPS stories |

**Contract build steps**

1. Add the POST and GET operations and schemas to API Specification v7, with the Problem responses listed in section 12.1.
2. Align wire names and required properties with `rwb-source-data.yaml` 5.1.0.
3. Publish the typed P1 workflow contract and align its ID, queue and reuse/conflict policies with RD-P1-047 and RD-P1-001.
4. Verify the rwb-case operations, item schemas and fake of RWB-P3-E1021-CON against `rwb-case.yaml` 5.1.0.
5. Build the fakes in section 12.8 and compare them against the API and workflow contracts.
6. Run the Test Cases v9 rows of section 16 against the contract and the fake.
7. Record consumer compatibility for P5, OPS, APP and integration stories.

**Done when.** The API fragment, workflow contract and fakes match the criteria and P5's request/response fixtures; fake publication and sign-offs remain Pending in section 20.

### 14. Validation and messages

| Code | Contract condition |
|---|---|
| MSG-PLT-N009-03 | Missing, blank or non-UUID `Idempotency-Key`; 400 |
| MSG-PLT-N009-05 | Key reused with another request, or in flight; 409 |
| MSG-P2-006 | A new key starts a run date whose run is RUNNING or COMPLETED; 409 |
| MSG-GEN-001 | Body unreadable (400), or a required value missing or an empty `rules` list (422) |
| MSG-GEN-002 | `retentionMonths` outside 1 to 600; 422 |
| MSG-GEN-007 | `productCode` or `endAction` not in its list; 422 |
| MSG-P1-002 | A table, table and action pairing or `ageBasis` check fails; 422 |
| MSG-P4-001 | No valid token; 401 |
| MSG-P4-002 | Caller lacks the operation right; 403 |
| MSG-P4-003 | Unknown runId; 404 |
| MSG-GEN-006 | Dependency unavailable before the 202 (503), or a run unit fails after it (run status FAILED) |
| MSG-P7-003 | Decision-record failure mapping and effect Pending under GAP-2426 |

Texts are those of Error and Message Standard v6. Pending: the refused-check names of MSG-P1-002, owner product owner, NEW-GAP-S5-2. The MSG-P1-020 alert rendering and routing belong to the APP and OPS stories.

### 15. Screens and states

The contract serves no screen of its own: the run is read on the platform administration surface that another P1 story owns, and the Compliance summary arrives as the MSG-P1-020 alert. The retention classes that the rule refers to show on SCR-47 Personal data from Epic 8. The states of SCR-47 for this contract are: loading, as Screen Specifications v1 holds it; empty, error and no access, Not specified in the source documents (CG-ALL-2203). The gateway-bff composite route (DP-19) is not on this path, because the start is a service-to-service call.

### 16. Test cases

- Test Cases v9 holds TC-P1-E1017-CON-01 to -22 for this story (-09 and -10 retired); the criteria of section 7 cite the row that covers them.
- The GET status list of the rows for AC4 and AC10 is RUNNING, COMPLETED and FAILED.
- TC-P1-E1017-CON-17 to -22 cover AC12 to AC17.

### 17. Guardrails

- No retention period or numeric policy value is embedded in this contract; periods are Pending with Compliance under GAP-1029.
- P1 accepts only the seven-table ARCHIVE/REVIEW boundary in section 12.7; `case_list_row` is excluded by RD-P1-024 (X-01).
- REVIEW counts rows as LISTED and performs no archive or delete.
- Only verified `interaction` archive copies may precede live-row deletion; P1 does not destroy archive objects.
- Held/open exclusions and closure dates are read from P3; P1 never reads `rwb_case`.
- The archive target/manifest and DP-03 decision record remain Pending under GAP-0490 and GAP-2426.
- The workflow ID is date-scoped as ruled; P5 must not reuse it in the shared Temporal namespace (NEW-ASM-X3).

### 18. Traceability

| Requirement or decision | Contract element | Test coverage |
|---|---|---|
| REQ-RDF-013 | Seven-table retention request, run status/counts, ARCHIVE/REVIEW boundary | TC-P1-E1017-CON-01 to TC-P1-E1017-CON-03, TC-P1-E1017-CON-05, TC-P1-E1017-CON-06, TC-P1-E1017-CON-08, TC-P1-E1017-CON-12 to TC-P1-E1017-CON-22 |
| RD-P1-047 | P1 start/read and P3 retention-exclusions/closure-dates interface | TC-P1-E1017-CON-01 to TC-P1-E1017-CON-03, TC-P1-E1017-CON-06, TC-P1-E1017-CON-12, TC-P1-E1017-CON-16, TC-P1-E1017-CON-19 |
| RD-P1-048 | Periods Pending; interaction ARCHIVE; six REVIEW-only tables; P3 age/hold behavior | TC-P1-E1017-CON-03, TC-P1-E1017-CON-05, TC-P1-E1017-CON-08 |
| RD-P1-024 (X-01) | `case_list_row` excluded from P1 | TC-P1-E1017-CON-03, TC-P1-E1017-CON-05, TC-P1-E1017-CON-08 |
| RD-P1-001 | UUID idempotency, response replay, conflict and expiry behavior | TC-P1-E1017-CON-08 |
| NFR-075 / DL26 | Ledger retention period remains Pending with Compliance | No test row until Compliance sets the period (GAP-1029) |
| GAP-0490, GAP-2426, NEW-GAP-S5-1 | Archive layout, DP-03 mapping and holdReport fields remain Pending | Delivery follow-up |

### 19. Out of scope

- The implementation of the run, the selection, the archive writer, the manifest check and the delete (RWB-P1-E1017-APP).
- The deployment, the container mount and credential, the KEDA scaling, the dashboards and the runbook (RWB-P1-E1017-OPS).
- The retention rule, the retention action table, their load and approval and the monthly Schedule (RWB-P5-E1017-APP).
- The legal hold itself and the case number (rwb-case, P3); this baseline consumes the interface and fakes it.
- The write-once container's own contract, its immutability policy and its credential scope (RWB-PLT-TE012-APP; GAP-0490).
- The decision log retention (rwb-decision, P7).
- The cross-service proof of the rule, the hold and the archive (RWB-ITG-E1017-ITG).
- The archive identity/path and manifest (GAP-0490), DP-03 decision-record mapping (GAP-2426), and holdReport fields (NEW-GAP-S5-1).

### 20. Remaining delivery steps

- Size: Not specified; pending refinement. Owner: squad.
- Epic design sign-off: Pending. Owner: solution architect.
- CON Done: Pending. Owner: contract owner.
- Fake published: Pending. Owner: contract owner.
- Test data in DEV: Pending. Owner: QA.
- Archive container identity, path and manifest format: Pending, GAP-0490. Owner: solution architect/storage architect.
- `holdReport` field details: Pending, NEW-GAP-S5-1. Owner: solution architect.
- Refused-check names: Pending, NEW-GAP-S5-2. Owner: product owner.
- Run failure detail on GET: Pending, NEW-GAP-S5-10. Owner: contract owner.
- Retention run record table (RWB-P1-E1017-APP): Pending, NEW-GAP-S5-8. Owner: data architect.
- DP-03 decision-record mapping and failure behavior: Pending, GAP-2426. Owner: solution architect.
- Activity signatures and non-retryable errors: Pending, NEW-GAP-S5-9; timeouts, GAP-0143. Owner: workflow architect.
- Fake library/version publication: Pending, CDC-02994. Owner: contract owner.
