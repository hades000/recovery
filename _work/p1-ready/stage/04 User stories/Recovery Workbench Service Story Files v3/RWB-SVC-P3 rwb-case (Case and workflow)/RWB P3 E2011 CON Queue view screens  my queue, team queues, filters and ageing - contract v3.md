# RWB-P3-E2011-CON Queue view screens: my queue, team queues, filters and ageing

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2011-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-011 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P3-E2011-CON-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P3-E2011-CON-14) |
| Contract version | /v1 (REST base /api/recovery/case/v1) |
| Patterns applied | DP01, DP06, DP07, DP08, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-017, FR-P3-018, FR-P3-019, FR-P3-021, FR-P3-022, FR-P3-025, FR-P3-040) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-005, RD-P1-040, RD-P1-041, RD-P1-062 |

**Version 3 changes.**

- D-RCV-60 finishing pass: RD-P1-062.

- RD-P1-005 and RD-P1-041: the consumed freshness row states the status values, the stamp in use and the never-stamped answer.
- RD-P1-062 fixes the no-date behaviour and fixture dates. Omit X-Data-As-Of and show the stale banner. MSG-P1-001 wording for an empty date remains Pending (GAP-3284).
- RD-P1-003 and RD-P1-040: no text change; this read path subscribes to no event.

**Change log.** D-RCV-60, 22 November 2026: moved from RWB-E2-011 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 11 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3 aligns the story with RD-P1-003, RD-P1-005, RD-P1-040, RD-P1-041. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As a **tech lead**, I want **the published query contract of the queue views as rwb-case serves it — `GET /api/recovery/case/v1/cases` for My queue with its filters, sort and age, `GET /api/recovery/case/v1/queues` for the team queue summary with its count, oldest age, breach count and per-owner spread against the cap, and `GET /api/recovery/case/v1/queues/{queueId}/cases` for the drill down — together with the paging and page-size rules, the order that makes a page stable, the error envelope and its message codes, the right each answer requires, the 2 s one-hop budget, the nine contract tables and the contract fakes**, so that **the app, operations and test stories of this legacy key build against a fixed, testable contract on Day 1, and a field, an order or a count can never drift between rwb-case, the composite route and the case list without a failing build**.

The legacy key is moved with no business change: the operations, the filters, the sort, the counts, the page limits and the message texts are the ones RWB-E2-011 fixed. What this story adds is the contract form of them: one document owner, one shape per answer, one order per list, one error envelope and one fake per consumed answer.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The queue views are the most-consumed read surface of rwb-case: the My queue screen, the Team queues screen, the case list and its export, the review queue of the document hub and the steering dashboard all read the same two or three answers, and the composite route at the edge merges them with the answers of other services (DP-19). Three things therefore drift silently if no contract holds them: the computed row fields (`ageDays`, `serviceLevelDueAt`, `serviceLevelState`), the queue summary fields and their cap rule, and the order and paging that make two readers of the same list agree on what "page 2" is. A renamed queue count would empty a team screen without a failing build; a list whose order is not fixed would show one case twice across two pages and hide another.

The baseline also fixes the naming the checks require: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, task queue `rwb-case` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.case`. It records that the counts these answers show move only through the events of `rwb.case.events.v1`, so no operation of this contract writes and no operation of this contract publishes (DP-14).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- The parameters contract of rwb-case (RWB-P3-E1042-CON, DP-06) and its reference-data contract (RWB-P3-E1043-CON, DP-07) are published, so the page-size limits, the caps and the list labels are declared as data and never as values in this document.
- The case list contract RWB-P3-E1031-CON and the queue contract RWB-P3-E1019-CON are published, so the Case page resource and the Queue resource this story extends have one owner document each and the added fields are an additive change to them.
- The timer contract RWB-P3-E1028-CON is published, so the meaning of `timer.status`, `timer.paused` and `timer.expires_at` behind `serviceLevelState`, `breachCount` and the sort is fixed by the story that writes them and not by this one.
- The Ownership Map gives `GET /cases`, `GET /queues` and `GET /queues/{queueId}/cases` to P3 rwb-case; this document declares no other service's operation as provided and names no operation the map does not already give P3.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive change to the rwb-case OpenAPI 3.1 document for the three read operations: the case row fields, the queue row fields, the paging parameters and the `X-Data-As-Of` header.
2. Fix the sort of the case list (`serviceLevelDueAt`, with the four groups of BR2 of the app story) and the tiebreaker, so two readers never sort differently.
3. Fix the paging rule: `page` and `size` with `total`, the default and maximum page size, and the stable order that makes a walk of pages complete and free of duplicates; declare no cursor token, because no source gives one.
4. State the summary rule of a queue: the count, the oldest entry date, the oldest age, the breach count and the per-owner spread against the cap, and that the count equals the case list count for the same filter (GAP-0707; GAP-0708; ASM-1254; ASM-1255).
5. Record the two consumed operations with their owner, their use and the 2 s budget, and map every failure to the error envelope and a message ID.
6. Record the event and workflow elements the answers depend on: the case events that move the counts, and the durable timer inside CaseWorkflow that writes the timer state the sort reads.
7. Publish the nine contract tables of section 12 and the contract fakes.
8. Add the contract tests: schema validation, the order, the paging walk, the error mapping, the rights, the budget, the drift between a fake and the document and the retired element.
9. Tag the baseline and hand it to RWB-P3-E2011-APP, to the operations story of this legacy key and to the consumers of the list.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the platform error envelope | None | AC1 |
| X2 | A field is renamed, retyped or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC9 |
| X4 | A page size outside 1 to 200 reaches the operation | 422 with MSG-GEN-002 naming the field, the minimum and the maximum | MSG-GEN-002 | AC6 |
| X5 | An age range arrives inverted | 422 with MSG-GEN-003 naming the two fields | MSG-GEN-003 | AC6 |
| X6 | A caller reads a queue outside its teams | 404 with MSG-P4-003 and not an empty page | MSG-P4-003 | AC4 |
| X7 | The freshness answer does not arrive inside the budget | The list is returned without the current business date and the header is omitted; no row is dropped and no count changes | None | AC8 |
| X8 | An operation of another service is written into this document as provided | The review fails: the document lists only rwb-case's own operations | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the same-service contracts it extends and the Ownership Map only |
| Negotiable | Field-level types and lengths are settled with the consumers; the three operations, the orders, the paging rule and the two consumed answers are fixed by the target architecture |
| Valuable | Unblocks the app and test stories of this legacy key on Day 1 and every consumer of the list and the queue rows |
| Estimable | One document, one additive change, two consumed operations, nine contract tables, three fakes and nine contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the queue views

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-case read surface is published under the base /api/recovery/case/v1
    Given the ownership map gives GET /cases, GET /queues and GET /queues/{queueId}/cases to rwb-case

  Scenario: AC1 The three read operations are declared with their owner (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /cases with the Case page resource, GET /queues with the Queue array and GET /queues/{queueId}/cases with the Case page resource, all under the base /api/recovery/case/v1 and owned by rwb-case
    Then the document names no other service's operation as provided
    Then every added property is optional in the schema, so a consumer of the previous version keeps working
    Then it declares the response header X-Data-As-Of on the two case answers

  Scenario: AC2 The case answer fixes the My queue filters, the sort and the row fields (new, D-RCV-60)
    Given the GET /cases operation declared in the document
    When its parameters and its row fields are reviewed
    Then the request takes owner, stage, route, status, ageFrom, ageTo, queue, page, size and sort
    Then sort takes serviceLevelDueAt as the My queue default and the order is breached first, then running by due date earliest first, then paused, then the cases with no service level, with the case ID as the tiebreaker
    Then each row carries the existing case fields plus ageDays, serviceLevelDueAt and serviceLevelState, and serviceLevelState takes one of BREACHED, RUNNING, PAUSED and NONE
    Then the document states that ageDays is the calendar days from the entry date to the business date and that serviceLevelState is read from the timer projection and never recomputed by a consumer

  Scenario: AC3 The queue answer fixes the team summary and the spread against the cap (new, D-RCV-60)
    Given the GET /queues operation declared in the document
    When its row fields are reviewed against the queue contract and the parameters contract
    Then each row carries the queue identity and the computed openCaseCount, oldestEntryDate, oldestAgeDays, breachCount and owners[]
    Then owners[] carries ownerUserId, openCaseCount and atCap, and atCap is a boolean against the cap in force
    Then the document states that openCaseCount counts the cases whose status is not Closed and equals the case list total for the same queue, that oldestAgeDays is the calendar days from oldestEntryDate to the business date, and that breachCount counts the open cases whose service level timer has status EXPIRED
    Then the cap is declared as data read from the queue row or from the member's personal capacity (GAP-0707; ASM-1254)
    Then the summary is declared either live from recovery_case and timer or from the reconciled queue_measure snapshot (GAP-0708; ASM-1255)

  Scenario: AC4 The queue-scoped answer fixes the page and the out-of-scope response (new, D-RCV-60)
    Given the GET /queues/{queueId}/cases operation declared in the document
    When its path, its query and its error responses are reviewed
    Then it takes the path parameter queueId and the query page, size and sort
    Then its rows are the rows of GET /cases with the same computed fields and the same order
    Then a queue that is unknown or outside the caller's teams answers 404 with MSG-P4-003 and never an empty page
    Then it requires Queue and allocation R where GET /cases requires Case record R

  Scenario: AC5 Paging, page size and the order that stands in place of a cursor (new, D-RCV-60)
    Given the paging parameters declared on the two case answers
    When the paging rule is reviewed
    Then page is zero-based and defaults to 0, size defaults to 50 and takes 1 to 200, and the answer carries page, size and total
    Then the document declares no cursor token, because no source gives one, and fixes the order and the tiebreaker so that a walk of pages is complete and free of duplicates
    Then a size outside 1 to 200 answers 422 with MSG-GEN-002 and an inverted age range answers 422 with MSG-GEN-003
    Then the default and the maximum are declared as parameter rows of parameter_catalog and not as values in the document (DP-06)

  Scenario: AC6 The error envelope and the message codes (new, D-RCV-60)
    Given the error responses declared on the three operations
    When each condition is mapped to its status and its message ID
    Then 401 no session maps to MSG-P4-001, 403 a missing right to MSG-P4-002, 404 a queue out of scope to MSG-P4-003, 422 an inverted age range to MSG-GEN-003 and an out-of-range size to MSG-GEN-002, and 503 a store failure to the envelope
    Then MSG-P3-017 is declared as the empty-list state of GET /cases and not as an error
    Then MSG-P1-001 is declared as the stale-data banner with the date carried in X-Data-As-Of, and MSG-P3-004 as the paused marker of a row with serviceLevelState PAUSED
    Then every text is the legacy text unchanged and the envelope is the platform envelope, never a local one

  Scenario: AC7 The rights each answer requires and the scope rule (new, D-RCV-60)
    Given the security and scope statements of the three operations
    When they are compared with the roles and the right names of the target
    Then GET /cases requires Case record R, and GET /queues and GET /queues/{queueId}/cases require Queue and allocation R
    Then every row is filtered by the caller's scope before it is counted, so a count never includes a case the caller cannot read
    Then the authorisation is declared as the rwb-access authorise contract through the guard library, cached per request (DP-08)
    Then a refusal is declared as 403 and a scope miss as 404, and neither as an empty answer

  Scenario: AC8 The two consumed answers and the 2 s one-hop budget (new, D-RCV-60)
    Given the consumed operations of the document
    When they are compared with the Ownership Map
    Then POST /api/recovery/access/v1/authorise names P4 rwb-access as its owner and is marked faked
    Then GET /api/recovery/source-data/v1/data-products/freshness names P1 rwb-source-data as its owner and is marked faked (GAP-0709; ASM-1256)
    Then every consumed row states one hop, the 2 s timeout, the GET retry once with jitter and the breaker per downstream
    Then a freshness answer that does not arrive inside the budget omits the header and drops no row, and a failed authorise answers 403 or 503 and never an empty page
    Then the two operations the app story reads as data, the parameters and the reference data of rwb-case, are declared as in-process library reads and not as cross-service rows

  Scenario: AC9 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map or None where the element is empty
    Then 12.3 and 12.4 record None and name the case events that move the counts as published by their own stories
    Then 12.6 records None and names the retired job as replaced by CaseWorkflow, with its decision record and run record held in the workflow
    Then the three contract fakes answer the paths and the payloads of 12.2 and the shapes of 12.1, and the contract tests compare each fake with the document and fail on any drift

  Scenario: AC10 The ten business rules of section 8 are each held by the artefact (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8 are in force
    When the document is reviewed against each rule
    Then each of BR1 to BR10 is met by the document or is covered by a guardrail or boundary test
    Then each rule ID of section 8 is traced to a test case in section 16

  Scenario: AC11 A status change the model does not allow is refused (new, D-RCV-60)
    Given every operation of the rwb-case read surface in this baseline is a read
    When the document is reviewed for an operation that changes a case status
    Then the document declares no status-changing operation, so a status change the model does not allow has no path and is refused
```

These nine criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P3-E2011-APP, which keeps the twelve legacy criteria with their own tags.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/case/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | A read declares no Idempotency-Key and writes nothing; a command declares it and stores its response | Architecture v5 slide 11; DP-09 |
| BR4 | Error responses use one envelope and one message ID per condition; the business message texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR6 | The document lists only operations owned by rwb-case; a consumed operation is described as consumed and faked, never as provided | Ownership Map v1 |
| BR7 | The count of a queue is the count of the same filter through the case list, so the two answers can never disagree on the same rows | REQ-WKM-006; NFR-018 |
| BR8 | No business value is fixed in the contract: the page-size default and maximum, the caps and the labels stay parameters, queue rows or reference data | Template and Rules §R7.2 s17; DP-06; DP-07 |
| BR9 | No personal data is declared in an answer: rows carry case numbers, codes, dates, counts and staff user IDs only, and the deviation code of a paused row is composed at the edge from the S8 answer | DP-19; REQ-WKM-002 |
| BR10 | The list order is part of the contract: a consumer that sorts differently from the document has a defect, not a preference | REQ-WKM-001; R-UNI-30 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the paging rule and the orders are described | In review |
| In review | Consumer sign-off | The app and test stories and the rwb-access and rwb-source-data owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new service level state | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or an order changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | An operation of another owner appears as provided | The review of AC1 fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the OpenAPI document and the fakes of the three operations; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Consuming teams (app and test stories, the composite route, the case list, the review queue and the dashboard) | Review and sign off the parts they consume |
| rwb-access owner | Signs off the authorise row, the right names and the scope rule |
| rwb-source-data owner | Signs off the freshness row, the header and the stale-data rule |
| Platform library owner | Owns the error envelope, the CloudEvents envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Case row | The Case resource of RWB-P3-E1031-CON plus `ageDays`, `serviceLevelDueAt` and `serviceLevelState`, from `recovery_case` DF-CAS-001, DF-CAS-002, DF-CAS-003, DF-CAS-005, DF-CAS-006, DF-CAS-008, DF-CAS-009, DF-CAS-010, DF-CAS-011 and DF-CAS-013, and from the open `timer` DF-WRK-028, DF-WRK-030, DF-WRK-032, DF-WRK-034 and DF-WRK-035 | Not specified in the source documents (DOR-RWB-P3-E2011-CON-7) |
| Case page | `items[]`, `page`, `size`, `total`, and the `X-Data-As-Of` header, set from the freshness answer of `source-data` and omitted when that answer does not arrive inside the budget (GAP-0709) | Not specified in the source documents (DOR-RWB-P3-E2011-CON-7) |
| Queue row | The Queue resource of RWB-P3-E1019-CON plus `openCaseCount`, `oldestEntryDate`, `oldestAgeDays`, `breachCount` and `owners[]` with `ownerUserId`, `openCaseCount` and `atCap` (GAP-0707; GAP-0708; ASM-1254; ASM-1255). `openCaseCount` and `breachCount` are integers, `oldestAgeDays` an integer, `oldestEntryDate` a date, `owners[].openCaseCount` an integer and `atCap` a boolean; the five summary fields are computed live from `recovery_case` and the open timer of each case | Not specified in the source documents (DOR-RWB-P3-E2011-CON-7) |
| Queue identity | `id`, `queueCode`, `queueName`, `teamCode`, `roleCode` and the cap, from `queue` DF-WRK-001 to DF-WRK-007 | Not specified in the source documents (DOR-RWB-P3-E2011-CON-7) |
| Cap | `queue.capacity_cap` or `queue_member.capacity` DF-WRK-048, whichever the queue in force uses (GAP-0707; ASM-1254) | Not specified in the source documents (DOR-RWB-P3-E2011-CON-7) |
| Snapshot | `queue_measure` DF-RPT-021 to DF-RPT-030, read only as a reconciliation check (GAP-0708; ASM-1255) | Not specified in the source documents (DOR-RWB-P3-E2011-CON-7) |
| Parameters and labels | `queueview.page-size.default` 50 and `queueview.page-size.max` 200 as parameter rows; LOV-STAGE, LOV-ROUTE and LOV-CASE-STATUS through the reference-data contract | Not specified in the source documents (DOR-RWB-P3-E2011-CON-7) |
| Error envelope | The platform envelope with one message ID per condition; the texts of section 14 | Not specified in the source documents (DOR-RWB-P3-E2011-CON-7) |

The types of the five queue summary fields are set in the Queue row; the lengths and required flags of the other added properties are settled in the baseline review; this story fixes the names, the optionality rule of AC1, the orders of AC2 to AC5 and the summary rule of AC3.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-case (P3); base `/api/recovery/case/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/cases` | Case page: filters by owner, stage, route, status, age, queue; `page`, `size`, `sort`; rows with `ageDays`, `serviceLevelDueAt` and `serviceLevelState`; header `X-Data-As-Of` | Case record R, scope applied |
| GET | `/queues` | Queue array: the queue identity plus `openCaseCount`, `oldestEntryDate`, `oldestAgeDays`, `breachCount` and `owners[]` with `ownerUserId`, `openCaseCount` and `atCap` | Queue and allocation R, scope applied |
| GET | `/queues/{queueId}/cases` | Case page of one queue: `page`, `size`, `sort`, the same rows and header as `/cases` | Queue and allocation R, scope applied |

The three operations answer 401, 403 and 503; the two case answers also answer 422, and the queue-scoped answer also answers 404. None takes an Idempotency-Key and none writes. Paging is `page` and `size` with `total`, size 1 to 200 and default 50; the document declares no cursor token and fixes the order and the tiebreaker instead.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and right check on the three operations, cached per request, faked with a grant and two refusals (DP-08) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The business date of the case data, for the header and the stale banner, faked with the current date, an earlier date and a slow answer (GAP-0709; ASM-1256). The answer is `DataProductFreshness` of rwb-source-data.yaml 5.1.0: `status` is `LOADED` or `STALE` and the row is the stamp in use (the latest stamped business date); a product never stamped answers `STALE` with `businessDate` null (RD-P1-005, RD-P1-041). For a null businessDate omit X-Data-As-Of and show the stale banner. MSG-P1-001 supplies the product and an empty date (wording Pending, GAP-3284) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream. The parameters and reference data of rwb-case are in-process library reads of the same service, not consumed rows.

#### 12.3 Events published

None. The contract publishes no event type. The counts and the order the answers show move only through the five events that their own stories publish on `rwb.case.events.v1` — CaseCreated, CaseAllocated, CaseTransferred, CaseStateChanged and TimerBreached — and this baseline declares them as depended on, not as published here.

#### 12.4 Events consumed

None. `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` on `rwb.source-data.events.v1` are P1's and are consumed by the case workflow stories and by gateway-bff for the banner; `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` are consumed by RWB-P3-E1028-APP to pause and resume the timer this contract reads. This read path subscribes to none of them.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case-{caseId} | `rwb-case` | Holds the durable service level timer and writes the `timer` rows whose status, pause flag and expiry the sort and the breach count read; owned by RWB-P3-E1028-APP, and this baseline registers no activity and no child workflow |

No activity is registered by this story; the row fixes what the read path may assume about the writer.

#### 12.6 Schedules

None. The five-minute timer check (JOB-05) is retired with the TimerDue event (Architecture v5 slides 42 and 44), the 06:30 rebalancing Schedule (JOB-06) belongs to RWB-P3-E1030-APP, and this baseline registers no Schedule, no cron entry and no job name.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| recovery_case | P3 (rwb_case) | The case row behind every list row: number, product group, status, stage, route, owner, queue, team and entry date |
| queue | P3 (rwb_case) | The queue identity and the cap a queue row carries |
| queue_member | P3 (rwb_case) | The personal capacity of an owner, when that is the cap in force (GAP-0707; ASM-1254) |
| timer | P3 (rwb_case) | The open SERVICE_LEVEL timer of a case: due date, pause flag and status |
| queue_measure | P3 (rwb_case) | The reconciled snapshot, read only when it is the source in force (GAP-0708; ASM-1255) |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The envelope of the events the counts depend on; not written by the read path |

`lov_value`, `reference_row` and `parameter_value` are read through the rwb-case contracts and never joined in SQL; no other schema is named (DP-01, DP-06, DP-07).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-access WireMock | `POST /authorise` with a granted answer for Case record R and Queue and allocation R, a refused answer for a role without the right, and a refused scope over SME-NTH for a scope Team in MTG-BKK | App story, contract tests |
| rwb-source-data WireMock | rwb-source-data.yaml 5.1.0 | On test day 2026-12-15, expected D is 2026-12-14. Offer LOADED for D, STALE for the preceding sandbox bank business day with staleSince D, and never stamped (STALE, businessDate and staleSince null). Also offer a timeout. For never stamped, omit X-Data-As-Of and show the stale banner. Assert MSG-P1-001 and product only while no-date wording is Pending (GAP-3284). |
| rwb-case read fake | The three operations with the resource shapes of 12.1, an empty page with `total` 0, a page of 200, a queue out of scope and a paused row | Composite route, case list, review queue, dashboard, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | Cases, queues and queue cases provided; authorise and freshness consumed; one hop, 2 s |
| Kafka | None published, none consumed | The five case events are declared as depended on and are published by their own stories |
| Temporal | None added | The timer behind the status read here lives in CaseWorkflow and belongs to RWB-P3-E1028-APP |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** The additive change to `openapi/rwb-case-v1.yaml` for the three operations, the case row and queue row components shared with RWB-P3-E1031-CON and RWB-P3-E1019-CON, the contract README rows for the order, the paging rule and the stale-data rule, and the three WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the three answers read this service's tables only and name no other schema | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case: the page-size default and maximum are rows of `parameter_catalog` | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case: LOV-STAGE, LOV-ROUTE and LOV-CASE-STATUS | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library, on the three operations | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; the naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in schema `rwb_case`; this baseline names the read-side index the app story adds and owns no migration itself | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-02 and SCR-07 | H RWB-PLT-N001-CON |

No pattern is claimed outside this list: the contract adds no decision record, no Drools model, no ACE view and no Quartz job.

**Build steps**

1. Add the case row fields, the queue row fields and the `X-Data-As-Of` header to the document; validate the additive rule of AC1 in the pipeline.
2. Fix the orders and the tiebreaker of AC2 to AC5 as schema constraints and README rows, including the page walk and the absence of a cursor token.
3. Write the summary rule of AC3 and the reason of its two gap rows into the document, so a consumer cannot read a count as a snapshot or a snapshot as a count.
4. Record the two consumed rows with their owner, their budget and their failure mapping; map every failure code of AC6.
5. Record the event and workflow rows of AC9 and add the absence test for the retired timer check.
6. Publish the three fakes and the nine contract tests; a drift between a fake and the document fails the build.
7. Baseline tag and the consumer sign-off note, including the rwb-access and rwb-source-data owners and the consumers of the list.

**Done when.** The OpenAPI artefact validates in the pipeline, the nine contract tests pass, the three fakes answer every path and the drift test is green, and the app story and the consumers of the list have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-002 | Page size outside 1 to 200 | {field} must be between {min} and {max}. |
| MSG-GEN-003 | Age to is less than age from | {field} cannot be before {other}. |
| MSG-P3-017 | The list has no case for the person and filters | There are no cases in this queue. |
| MSG-P4-003 | A queue outside the caller's scope | This case is not in your scope. |
| MSG-P1-001 | The case data is from an earlier business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-004 | A case on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P4-001 | Mapping of the three operations (see the paragraph below) | Not specified in the source documents (DOR-RWB-P3-E2011-CON-9) |
| MSG-P4-002 | A role without the right reads one of the three operations | You cannot {action} here. Your role does not include it. |

The message IDs are contract elements and the texts are the agreed legacy texts unchanged. MSG-P4-001 is an id of the rwb-access contract and appears here only in the mapping of the three operations; the other ids are the ones the operations and the header return, and the envelope is the platform envelope. The `{product}` of MSG-P1-001 is the data product name the screen shows (GAP-0709; ASM-1256).

### 15. Screens and states

The contract serves SCR-02 Case list in its My queue view (states Loading, Empty, List, Filtered; error and no access: Not specified in the source documents (CG-ALL-4112)) and SCR-07 Team queues (states Loading, List; empty, error and no access: Not specified in the source documents (CG-ALL-4113)), through the gateway-bff composite route (DP-19). The route calls rwb-case for the list and the queue rows and other owners for the rest of the screen; this baseline fixes the rwb-case answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2011-CON-01 | AC1 | Contract | The document validates; the three operations, their owner and the header are present; every added property is optional |
| TC-P3-E2011-CON-02 | AC2 | Contract | The nine request parameters; the four sort groups and the tiebreaker; the three computed row fields |
| TC-P3-E2011-CON-03 | AC3 | Contract | The queue row fields; `atCap`; counts 412 and 38; the two gap rows present |
| TC-P3-E2011-CON-04 | AC4 | Contract | The queue-scoped path; the same rows and order; 404 with MSG-P4-003 for a queue outside the teams |
| TC-P3-E2011-CON-05 | AC5 | Contract | Page 0 and size 50 defaults; size 1 and 200; size 500 refused; a two-page walk with no duplicate and no gap |
| TC-P3-E2011-CON-06 | AC6 | Contract | Every condition mapped to its status and message ID; the seven texts compared with the legacy text |
| TC-P3-E2011-CON-07 | AC7 | Contract | The two rights; the scope filter before the count; the 403 and the 404 shapes |
| TC-P3-E2011-CON-08 | AC8 | Contract | Two consumed rows with owner, budget, retry and breaker; the freshness answer omitted inside budget; the authorise refusal |
| TC-P3-E2011-CON-09 | AC9 | Component | The nine sub-tables present with owners; three fakes match the document; a drifted fake fails the build |
| TC-P3-E2011-CON-10 | AC9 | Contract | Each table of §12.7 with its owner and contracted use; a table outside §12.7 or with another owner fails the build |
| TC-P3-E2011-CON-11 | BR1 to BR6 | Contract | The REST base, event names and topics, the read with no key, the error envelope and message IDs, the additive change rule and the owned-only operations |
| TC-P3-E2011-CON-12 | BR7 to BR10 | Contract | Queue count equals the case list count under the same filter; no business value fixed; no personal data in an answer; list order as contracted |
| TC-P3-E2011-CON-13 | AC10 | Contract | Not specified in the source documents (NEWAC-RWB-P3-E2011-CON-AC10) |
| TC-P3-E2011-CON-14 | AC11 | Contract | Not specified in the source documents (NEWAC-RWB-P3-E2011-CON-AC11) |

The nine criteria are tested against the artefact, not against a business outcome; the twelve legacy criteria of RWB-E2-011 are owned and tested by RWB-P3-E2011-APP and are not copied here.

### 17. Guardrails

- No business value in the contract: the page-size limits, the caps, the labels and the states are parameters, queue rows, reference data or enumerations the timer story fixes, never values chosen by this document.
- No personal data in a schema, an example or a fake: case numbers, codes, dates, counts, amounts and staff user IDs only; no customer name, address, identity number or contact point is declared.
- The contract names only rwb-case's tables and only operations owned by rwb-case; the authorise and freshness operations are consumed and faked, never declared as provided (DP-01, DP-08).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- ACE data is reached only through the owner's contract or the `v_ace_*` views; this document declares no ACE view and no cross-schema join.
- No retired element is reintroduced: a build that declares a timer-check Schedule, a timer-check job or a TimerDue event fails the absence test of AC9.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state | The `GET /cases` filters, the sort and the three computed row fields | TC-P3-E2011-CON-02, TC-P3-E2011-CON-05 |
| REQ-WKM-002 | A team manager sees every queue in the team with filters | `GET /queues` and `GET /queues/{queueId}/cases`, the queue row and the scope rule | TC-P3-E2011-CON-03, TC-P3-E2011-CON-04 |
| REQ-WKM-006 | Queue counts, ageing and breaches reconcile to the case list | The summary rule of `openCaseCount`, `breachCount` and `total` against the same filter | TC-P3-E2011-CON-03, TC-P3-E2011-CON-04 |
| REQ-CWC-011 | Service levels are held as data and a breach raises an event without moving the case | `serviceLevelState`, `breachCount` and the timer row the answers read | TC-P3-E2011-CON-02, TC-P3-E2011-CON-03 |
| REQ-WKM-011 | Partner work is visible in the same queue view as internal work | None in this baseline; the partner column arrives with the partner panel in Epic 6 | None |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget, retry rule and breaker | TC-P3-E2011-CON-08 |

### 19. Out of scope

- The implementation of the three read operations, the queries, the computed fields and the two screens (RWB-P3-E2011-APP).
- The deployment, the consumer groups, the dashboards and the runbook of this capability, which belong to the operations story of this legacy key.
- The timer mechanism, the escalation write and the TimerBreached publication (RWB-P3-E1028-CON and RWB-P3-E1028-APP).
- The base Case resource and the case list export (RWB-P3-E1031-CON and RWB-P3-E1031-APP).
- The base Queue resource, the queue load and the queue write interface (RWB-P3-E1019-CON and RWB-P3-E2036-APP).
- The queue measure snapshot and the rebalancing Schedule (RWB-P3-E1030-APP).
- The rwb-access and rwb-source-data contracts themselves: consumed and faked, never defined here.
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON).
- The cross-service journey harness and its evidence, when a journey story is raised for this legacy key.
