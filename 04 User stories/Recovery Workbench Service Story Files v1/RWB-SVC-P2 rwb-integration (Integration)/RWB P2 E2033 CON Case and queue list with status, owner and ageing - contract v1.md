# RWB-P2-E2033-CON Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2033-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-WKM-002, REQ-DVH-006, REQ-ACA-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-033 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-integration side of the composed case and queue list fixed as a contract: the two read-only operations on the service base, the page shape, the filter set, the breach and clock fields, the error envelope, the read-only idempotency statement, the P3 and P4 operations it consumes and the fakes that stand in for them**, so that **the app story of this legacy key builds on Day 1 against one agreed, testable shape and no team waits for rwb-case or rwb-access to land**.

The legacy story had no contract of its own: the case list, its ageing, its breach filter, its extract and the access-log call sat in one monolith module over one schema, so the shape of a page was whatever `CaseListQueryService` returned. Under D-RCV-60 the case, the queue and the timer belong to rwb-case (Arch v5 slide 41), the rights, the scope and the access log belong to rwb-access, the parameters and the reference data belong to rwb-case (R-PREC default ruling), and the composition that stays with rwb-integration is a consumer of all of them. A composition needs its contract more than an owner does: it has to say what page it answers, which filter values it accepts, which fields it carries, what it does when a source does not answer, and what it never writes.

The contract also fixes the seam the split creates, and the seam is a duplication. The Ownership Map keeps `GET /cases` and `GET /cases/export` with P3 and ADR-020 with DP-19 serves SCR-02 from the owner through gateway-bff; the WP still splits a P2 APP slice that owns AC1 to AC11 of the legacy key. The resolution is the one RWB-P2-E2006-APP recorded for the credit approval pack: the composed read and the export exist as an additional, read-only composition on the integration base, the owner keeps the system-of-record read and its own export, and the duplication is stated in this document and in the gap and assumption rows rather than hidden (GAP-0661; ASM-1133; ASM-1134).

The third thing this document fixes is the second duplication, inside the composition. The ageing and service-level rules of the legacy story run case-side, in the P3 ageing contract, and they run again here, in `AgeingAndBreachCalculator`, so that a page can be filtered by breach and ordered consistently over one page rather than one case at a time. Both evaluations read the same owner fields; the document says which answer is the record and which is the composition, so the two can be tested against each other (ASM-1145).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling rule (ADR-020) and it only pays off if the seam is written down once. Here the seam is wide: a page over the manager's whole scope, six filter values, twelve columns, two computed clock states, a breach flag, a paging envelope, an Excel file with a row limit and one access-log entry, over six consumed operations in two other services.

If the shape is agreed and faked on Day 1, three things move at once. The app story builds the controller, the composition, the calculator, the clock reader, the validator, the export writer and the screen support against the fakes. The test stories of RWB-E2-033 read one page shape and one column set, so the same assertion runs against the composed page and against the case-side screen. The P3 and P4 contract stories learn exactly which fields and which rights the composition needs, which is the only way the owner's contract gets published with the fields a consumer actually reads.

The contract also states what this service does not own. The case rows, the queue list, the timer projection, the parameters and the reference data are rwb-case's; the right, the scope, the default scope and the access log are rwb-access's. This document defines the consumed side of each and restates none of them as its own. Nothing is copied into `rwb_integration`, and no foreign key leaves the schema.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the REST base, the topic and the event names follow the platform rule and not a local choice (DP-13, DP-14).
- The platform error envelope and the message catalogue are the platform baseline; this document narrows them where it must and says so (ADR-020).
- The parameter and reference-data contracts of rwb-case are as published (RWB-P3-E1042-CON, RWB-P3-E1043-CON; DP-06, DP-07). This document consumes them and fakes them; it defines neither.
- The case-list, ageing and case-record contracts of rwb-case are as published (RWB-P3-E1031-CON, RWB-P3-E2011-CON, RWB-P3-E1018-CON). This document consumes them and names the fields the composition reads.
- The authorise contract and the guard library of rwb-access are as published (RWB-P4-E1037-CON; DP-08), including the access-log operation of an export.
- The gateway-bff composite route that serves SCR-02 Case list is as published (RWB-PLT-N001-CON; DP-19).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the two provided operations: method, path, purpose, right, idempotency and the response of each.
2. Fix the page shape: the row of the composed page, the paging envelope and the twelve columns of the legacy story.
3. Fix the filter set and the validation source of each value: the reference-data lists, the queue list and the parameter bounds.
4. Fix the breach and clock fields: `ageDays`, `serviceLevelDueAt`, `serviceLevelState`, `prescriptionDate` and `prescriptionClockStatus`, with the rule identifiers that produce them.
5. Fix the order and the breach filter, so that two pages of one list are stable and the export with the same filters returns the same row set.
6. Fix the error envelope: 401, 403, 422, 503 and the unavailable answer, with the message identifier of each.
7. Publish the six consumed operations with the element each read needs and the fakes that stand in for them.
8. State the read-only rule: no table, no row, no event, no workflow and no Schedule, and the one access-log entry per export asked of its owner.
9. State the duplication: the P3 case list and export remain the owner's, and this composed read and export are an additional composition with the same fields from the same contracts.
10. Publish the fakes and the drift test, then tag the baseline and hand it to the app story and the test stories of this key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A filter value is not in the list its owner publishes, or a page size is outside the bounds the parameter contract returns | The contract names the answer as 422 with the field and the list version, so the app can refuse before any case is read | MSG-GEN-007; MSG-GEN-002 | AC3 |
| X2 | A consumed operation has no field in its owner's published contract for an element this document declares | The element carries the placeholder, one gap row and one assumption row, and the fake is written to the assumed shape | None | AC1, AC5 |
| X3 | A fake drifts from this document, or the app calls a path this document does not declare | The contract test fails and the merge is blocked | None | AC5 |
| X4 | A code path reads a case, queue, timer, role, parameter or reference row of another service, or an ACE view | The architecture boundary test fails the build | None | AC6 |
| X5 | A consumed contract removes, renames or retypes an element this document declares | The contract goes back to review with that owner and the app and test stories are re-baselined | None | AC2, AC3 |
| X6 | The export is asked for above the row limit the parameter contract returns | The contract names 422 with the limit before any file is built, so no partial file can be produced | MSG-P3-021 | AC3 |
| X7 | The access-log entry of an export cannot be recorded | The contract names the answer as 503 with no file, so the app cannot produce a file that has no entry | MSG-P7-003 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and the owners' published operations and declares none of theirs as its own |
| Negotiable | The JSON field names and the problem body are settled with the owners and the app story; the operation set, the columns, the filter set and the read-only rule are fixed by this realignment |
| Valuable | Unblocks the app story and the test stories of this key on Day 1 and tells the P3 and P4 contract stories which fields and rights a consumer reads |
| Estimable | Two provided operations, one page shape, six consumed operations, one error envelope and six fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the OpenAPI document, the fake, this file — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Composed case and queue list contract for rwb-integration

  Background:
    Given the service naming rule of the platform library is in force
    Given the parameter and reference-data contracts of rwb-case are as published
    Given the case, the queue and the timer are owned by rwb-case and the rights and the access log by rwb-access

  Scenario: AC1 The nine contract tables are complete and attributed (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.1 names the two read-only operations on the base /api/recovery/integration/v1
    Then 12.2 names the case-list, ageing, case-record, queue, parameter, reference-data, authorise and access-log operations
    Then 12.3 and 12.4 are None, 12.5 and 12.6 are None, and 12.8 names the fakes
    Then 12.7 states that this service owns no table for this read and that the access log is rwb-access's
    Then a sub-table that names another service's operation as provided fails the review

  Scenario: AC2 The page shape is fixed with its row, its envelope and its columns (new, D-RCV-60)
    Given the page contract of this story
    When a page is validated against it
    Then the answer carries the rows, the page number, the size and the total count of the legacy page
    Then each row carries caseNo, product, queue, owner, status, stage, ageDays, serviceLevelState, serviceLevelDueAt, prescriptionDate, prescriptionClockStatus and deviationOpen
    Then the owner column carries the text "Unassigned" when the case has no owner and no row carries a customer personal field
    Then a row that lacks a declared element, or that carries an element outside the twelve, fails the contract test

  Scenario: AC3 The filter set, the breach and clock fields and the order are fixed (new, D-RCV-60)
    Given the filter and order contract of this story
    When a list is requested with a filter set
    Then the accepted filters are product, stage, status, owner, queue, page, size, sort and breached, and the export takes the same set without page and size
    Then each value is validated against LOV-PRODUCT, LOV-CASE-STATUS, LOV-STAGE or the queue codes in force, and the page size against the bounds the parameter contract returns
    Then serviceLevelState is one of BREACHED, RUNNING, PAUSED and NONE, and prescriptionClockStatus one of RUNNING, EXPIRED and NONE
    Then the rows are ordered by breach, then age in state descending, then case number, so two pages of one list are stable
    Then an export with the same filters returns the same row set as the pages it covers, and above the row limit it answers 422 with MSG-P3-021

  Scenario: AC4 The error envelope and the read-only idempotency are fixed (new, D-RCV-60)
    Given the error and idempotency contract of this story
    When each documented answer is reached in a fake
    Then the answers are 200, 401 with MSG-P4-001, 403 with MSG-P4-002, 422 with MSG-GEN-007, MSG-GEN-002 or MSG-P3-021, and 503 with MSG-GEN-006 or MSG-P7-003
    Then the problem body of every error is the platform error envelope, and no answer carries a stack trace, a payload or a personal value
    Then both operations are declared read-only, so a repeat of the same request on unchanged data returns the same rows in the same order and stores no response
    Then the export declares one access-log entry per export, asked of rwb-access, and a refused entry produces no file

  Scenario: AC5 The six fakes match this document and drift fails the build (new, D-RCV-60)
    Given the fakes of 12.8
    When each fake is compared with the element it serves
    Then every consumed path and payload is answered with the shape of this document
    Then every documented answer of AC4 is reachable in a fake, including the slow answer for the 2 s budget
    Then a drift between a fake and this document fails the contract test and blocks the merge

  Scenario: AC6 No cross-schema read, no foreign key and the duplication is declared (new, D-RCV-60)
    Given the code and the migrations of the app story of this key
    When the architecture boundary test runs
    Then no statement reads a table of another service or an ACE view, and the only cross-service calls are the declared paths of 12.2, one hop each with a 2 s budget
    Then rwb_integration holds no foreign key into another schema and no copy of a case, a queue, a timer, a role, a parameter or a reference row
    Then the document states that GET /cases and GET /cases/export stay with rwb-case and that this composed read and export are an additional read-only composition
    Then no event is published, no workflow is started and no Schedule is created by this slice
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/integration/v1`; a document never declares another service's path as its own | DP-13; Arch v5 slide 41 |
| BR2 | One topic per service: `rwb.integration.events.v1` with the events FileDelivered and FileFailed, and this slice publishes neither and declares no event name | DP-14; Arch v5 slides 16 and 43; ASM-1143 |
| BR3 | The two provided operations are read-only: a page and an Excel file, no business table, no row, no event and no workflow | Legacy RWB-E2-033 section 9 and section 12; Template and Rules §R7.2 s17 |
| BR4 | The case, the queue, the timer projection, the parameters and the reference data are read only through the rwb-case contracts, and the rights, the scope and the access log only through the rwb-access contract | DP-01; DP-06; DP-07; DP-08; Arch v5 slides 13, 41 and 45 |
| BR5 | `ageDays`, `serviceLevelState`, the breach flag and `prescriptionClockStatus` are computed from the owner's timer and clock fields by the rule identifiers BR2 to BR5 of the app story, and no value is stored | Legacy BR2 to BR5; R-UNI-30; R-DEV-01 |
| BR6 | The order is breach, then age in state descending, then case number, and the export returns the same row set as the pages it covers | Legacy AC1 and AC11; legacy flow step 7 |
| BR7 | Every filter value is a row of its owner's reference data or of the queue list, and the page bounds and the export row limit are parameter rows; no limit and no list value is in the contract as a constant | Legacy BR6 and BR7; DP-06; DP-07 |
| BR8 | The export records one access-log entry, through the rwb-access contract, before the file is made; a refused entry produces no file | Legacy BR7; CTL-11; REQ-ACA-006 |
| BR9 | The page is composed twice by design: rwb-case keeps `GET /cases` and `GET /cases/export`, and this document fixes the additional read-only composition on the integration base | Ownership Map `GET /cases` and `GET /cases/export`; ADR-020; DP-19; GAP-0661; ASM-1133 |
| BR10 | The ageing and service-level rules are evaluated on both sides on the same owner fields; the case-side answer is the record and this one is the composition | Legacy BR2 to BR5; ASM-1145 |
| BR11 | No contract element names a person: the page carries the case number and the owner reference, and no customer field | Legacy guardrail 2; CTL-11 |
| BR12 | The file is produced on request and is never a data-lake file; the data lake is removed | DP-17; Arch v5 slide 37 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The nine sub-tables, the page shape, the filter set and the fakes are described | In review |
| In review | Consumer sign-off | The app story and the test stories of this key accept the document and the fakes | Baselined |
| Baselined | Additive change | A field, an answer or a fake is added without removing one | Baselined |
| Baselined | Breaking change to a consumed operation | An owner removes, renames or retypes an element this document declares | In review, with that owner |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A new filter or column is declared | The owner publishes the row or the parameter it reads, and this document adds one element | Baselined (new element) |

The page states of the screen — Loading, List, Filtered, Empty, Breached marker, Paused marker and Extract — are the app story's and are not states of this document.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-integration | Owns this document and the six fakes; tags the baseline |
| Solution architect | Approves a breaking change to a consumed contract and any change to the duplicate-composition statement |
| The rwb-case owner | Owns the case list, the ageing, the case record, the queue list, the parameters and the reference data this contract calls; signs off the shapes taken from its document |
| The rwb-access owner | Owns the right, the scope, the default scope and the access log behind the two provided operations |
| The rwb-integration app story and the test stories of this key | Review and accept the parts they consume |
| Data steward | Confirms that no customer personal field is declared in a page, a filter or a file |

The deployment identity that calls the owners' contracts is Not specified in the source documents (GAP-0661; ASM-1135); the document names it "the rwb-integration login (DP-02)" and leaves the name to the app and platform stories.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Page answer | The rows of the caller's scope, the page number, the size and the total count of the legacy page |
| Page row | `caseNo`, `product`, `queue`, `owner` (the text "Unassigned" when empty), `status`, `stage`, `ageDays`, `serviceLevelState`, `serviceLevelDueAt`, `prescriptionDate`, `prescriptionClockStatus`, `deviationOpen` |
| Filter set | `product`, `stage`, `status`, `owner`, `queue`, `page`, `size`, `sort`, `breached`; the export takes the same set without `page` and `size` |
| Validation source | LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE from the reference-data contract, the queue codes from the queue list, the page bounds and `caselist.export.maxrows` from the parameter contract, each with the version in force |
| Ageing element | `ageDays`, `stageClockStart`, `serviceLevelDueAt`, `serviceLevelState`, `prescriptionDate`, `prescriptionClockStatus` as the ageing contract publishes them for a page of case ids |
| Authorise element | The Case record right, the caller's scope and its default scope, cached per session |
| Access-log element | The user, the time, the filters and the row count of one export, written by rwb-access |
| Error element | The platform error envelope with the message identifier of each answer in AC4 |
| Export file | The Excel column set of the legacy story: case number, product, queue, owner, status, stage, age in state, service level state, service level due, prescription date, prescription clock, deviation open |

The physical names, lengths and required flags of the page, the ageing element and the access-log element are Not specified in the source documents (GAP-0661; ASM-1136; ASM-1137; ASM-1140); this document fixes the element names above and leaves the physical names to the review with the rwb-case and rwb-access owners. The exact form of the two provided paths and of the column order of the file are Not specified in the same way.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2). Two operations, both read-only.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/case-list` | The composed case and queue list page: the rows of the caller's scope with the twelve columns of 11, the filter set, the breach filter, the stable order and the paging envelope | Case record R, scope applied, through the rwb-access authorise contract | Read only: the same request on unchanged data returns the same rows in the same order; no response is stored |
| GET | `/case-list/export` | The same filters without page and size, written as an Excel file with the legacy export column set, after one access-log entry is recorded through rwb-access | Case record R, scope applied | Read only on the data; one access-log entry per export |

The Ownership Map keeps `GET /cases` and `GET /cases/export` with P3, so these two paths are not its rows and are fixed here under the service base of DP-13; their exact form and the JSON field names are Not specified in the source documents (GAP-0661; ASM-1134; ASM-1136). Errors: 401 no session or no Recovery role (MSG-P4-001); 403 no Case record right (MSG-P4-002); 404 a case read that names no case; 422 a filter value outside its list (MSG-GEN-007), a page size outside the bounds (MSG-GEN-002) or an export above its row limit (MSG-P3-021); 503 a consumed contract that does not answer inside the budget (MSG-GEN-006), a database that is unavailable (E503) or an access-log entry that cannot be recorded (MSG-P7-003), which produces no file.

The two operations are the legacy contract shape, kept for the integration base, and they are an additional composition: rwb-case keeps the system-of-record read of the case list and its own export, and the two answers agree on the row, the queue, the owner, the age and the service level state because they read the same contracts (BR9, ASM-1133).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the contract |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The case rows of the caller's scope with the filters and the paging of the legacy operation; the case-list contract of RWB-P3-E1031-CON |
| GET | The ageing and service-level read of the RWB-P3-E2011-CON contract, for a page of case ids | P3 rwb-case | `ageDays`, `stageClockStart`, `serviceLevelDueAt`, `serviceLevelState`, `prescriptionDate` and `prescriptionClockStatus`, batched so that one page is one hop |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case record read of RWB-P3-E1018-CON, for a field a list row does not carry |
| GET | `/api/recovery/case/v1/queues` | P3 rwb-case | The queue codes in force with their team code and role, for the queue filter and its validation |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The page bounds and `caselist.export.maxrows` with the version in force (DP-06) |
| GET | The reference-data read of the RWB-P3-E1043-CON contract | P3 rwb-case | LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE with the version in force (DP-07) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Case record right, the caller's scope and its default scope, cached per session by the guard library (DP-08) |
| POST | The access-log operation of the RWB-P4-E1037-CON contract | P4 rwb-access | One access-log entry per export: the user, the time, the filters and the row count |

Every operation is one hop with a 2 s client budget and no retry on a 4xx (ADR-020). The ageing read, the reference-data read and the access-log operation are named by their owner contract only; their paths, query parameters and JSON field names are Not specified in the source documents (GAP-0661; ASM-1137; ASM-1139; ASM-1140). The case-list, queue and parameter paths are the Ownership Map rows of P3 under the service base of DP-13, and the authorise path is the one Architecture v5 slide 14 gives rwb-access. The per-case timer projection the Ownership Map names, `GET /cases/{caseId}/timers`, is read only through the batched ageing element of this contract, so that one page is one hop.

#### 12.3 Events published

None. This slice publishes no event, writes no outbox row and holds no decision record. `rwb.integration.events.v1` carries FileDelivered and FileFailed from the outbound file side of this service (Arch v5 slide 16 and slide 43; ASM-1143), and the decision-record topic `rwb.decision-record.v1` is not used here because the read takes no decision.

#### 12.4 Events consumed

None. The page is composed per request, so this slice subscribes to no topic and holds no inbox: a case that changes is seen on the next read, not through a projection of `CaseStateChanged`, `DeviationRaised` or `TimerBreached`.

#### 12.5 Workflows and activities

None. Both operations are synchronous and served inside the request; this document declares no workflow, no activity and no timer. The stage and prescription clocks belong to the case workflow of rwb-case.

#### 12.6 Schedules

None. Neither operation is scheduled: the page is read on request and the export is officer-driven. No Schedule, no Temporal timer and no batch window is declared here (Arch v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| None | — | This read declares no table of its own: nothing is copied into `rwb_integration` and no row is written (DP-01) |
| `recovery_case`, `queue`, `timer`, `parameter_value`, `reference_row` | P3 rwb-case, in `rwb_case` | Read only through the contracts of 12.2; never read directly and never copied |
| `role`, the access log | P4 rwb-access, in `rwb_access` | Read and written only through the contracts of 12.2; the access-log entry of an export is the owner's row |

The platform library objects `outbox_event`, `processed_event`, `outbox_delivery` and `idempotency_key` exist in `rwb_integration` from the service baseline and this slice writes no row in any of them, because a read-only operation stores no response. `interface_config`, `outbound_item` and `job_catalog` stay the file stories' and are untouched here. No foreign key leaves the schema (DP-15 applies to the baseline only; ASM-1142).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock — case list and queues | Case `RW-2026-000101` to `RW-2026-000105` and `RW-2026-000201` with their product, queue, owner, status and stage clock start; queues `MTG-BKK-CO` and `MTG-BKK-LIT` with their team and role; no case for product SSME; 120 cases of equal age; 10,001 cases | App story, contract tests |
| rwb-case WireMock — ageing | The SERVICE_LEVEL and PRESCRIPTION timers of those cases, the paused timer, the boundary timer due 10 December 2026 09:00 and the absent timer, and one slow answer beyond 2 s | App story, contract tests |
| rwb-case WireMock — parameters and reference data | Page bounds 1 and 200, `caselist.export.maxrows` 10,000; LOV-PRODUCT, LOV-CASE-STATUS and LOV-STAGE with a version, and LOV-PRODUCT without `CAR` | App story, AC3 |
| rwb-access WireMock | Allow RW-TEAMMGR with Case record R and Team scope; refuse RW-REFADM with MSG-P4-002; scope over `MTG-BKK` and none over `HP-NE-CO`; the access-log entry recorded, and refused for X7 | App story, contract tests |
| gateway-bff composite route stub | The SCR-02 route and the merged screen model (DP-19) | App story |
| A 2 s delay stub per downstream | One slow answer per consumed contract, so the breaker and the unavailable answer are reachable | Contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 8 consumed | The page and the export provided; the case list, the ageing read, the case record, the queues, the parameters, the reference-data read, the authorise check and the access-log entry consumed; one hop, 2 s timeout |
| Kafka | 0 published, 0 consumed | `rwb.integration.events.v1` is the file stories' and no topic is used by this slice |
| Temporal | 0 workflows, 0 activities | Both operations are synchronous |
| File | 1 written on request | The Excel export of the legacy column set; no file is read and no lake file exists (DP-17) |

### 13. Solution plan

**Deliverables.** `contract/case-list.yaml` (the OpenAPI document of the page: the operation, the filter set, the row, the paging envelope and the error answers), `contract/case-list-export.yaml` (the operation, the column set, the row limit and the file answer), `contract/case-list-consumed.yaml` (the eight consumed operations with the element each read needs), and the six WireMock mappings with their fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library; no event and no topic is added | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence; this slice adds no migration | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Write the page document: the operation, the filter set, the twelve columns, the paging envelope and the problem body.
2. Write the export document: the same filters without page and size, the column set, the row limit and the file answer.
3. Write the consumed document for the eight operations, with the element each read needs and the placeholder where the source names no path or field.
4. State the read-only rule and the access-log rule: no table, no row, no event, no workflow, one entry per export.
5. State the duplication: the P3 read and export remain the owner's, and this composition is additional and read-only.
6. Build the six WireMock mappings and their fixtures.
7. Add the six contract tests of section 16, including the drift test between each fake and this document.
8. Tag the baseline and collect the sign-off of the app story and the test stories of this key.

**Done when.** The three contract files validate in the pipeline, the six contract tests pass, the six fakes answer every consumed path, every answer of AC4 and the slow answer, and the app story of this legacy key has accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-007 | A filter value is not in its list | {value} is not a valid value for {field}. |
| MSG-GEN-002 | Page size outside its bounds | {field} must be between {min} and {max}. |
| MSG-P3-020 | No case matches the filters | No cases match these filters. Change a filter to see more. |
| MSG-P3-021 | Extract above the row limit | The export holds at most {max} rows. Narrow the filters and try again. |
| MSG-P4-001 | No valid session, or a session with no Recovery role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The export access event cannot be recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | A consumed contract does not answer inside the budget | Not specified in the source documents (GAP-0661; ASM-1136) |

The texts of the legacy story are copied unchanged and this contract adds no wording of its own. MSG-GEN-006 is the platform unavailable message and its text is fixed by the Error and Message Standard, so the placeholder stands here. MSG-P1-001 does not arise, because the composed page carries no ACE data product.

### 15. Screens and states

None in this story. The two provided operations serve SCR-02 Case list, whose states, markers and behaviour belong to the app story of this key, and the screen is reached through the gateway-bff composite route (DP-19). This contract fixes only the answers a screen may show — the page, the empty page, the row-limit refusal and the unavailable answer — and the states they carry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2033-CON-01 | AC1 | Contract | The nine sub-tables present; 12.3 to 12.6 None; no table of another owner named; a sub-table naming another owner's operation fails |
| TC-P2-E2033-CON-02 | AC2 | Contract | One page validated against the row and the envelope; a row missing an element and a row with a thirteenth element both fail |
| TC-P2-E2033-CON-03 | AC3 | Component | A filter set with a valid and an invalid value of each list; the page size bounds; the order over three rows; an export above the row limit answering 422 |
| TC-P2-E2033-CON-04 | AC4 | Contract | Every answer of the envelope reached in a fake; the problem body shape; a repeated read returning the same rows; an export with the entry recorded and one with it refused |
| TC-P2-E2033-CON-05 | AC5 | Contract | Each of the six fakes compared with its element; every documented answer reachable, including the slow answer; one injected drift fails the test |
| TC-P2-E2033-CON-06 | AC6 | Component | The boundary test finds no cross-schema statement, no ACE view, no undeclared path, no foreign key out of `rwb_integration` and no event or workflow in this slice |

### 17. Guardrails

- No business value in the contract: the page bounds, the export row limit, the lists and the service levels are rows of their owners' parameter and reference data, read with the version in force.
- No personal data in a page, a filter, a file or a fake: the case number, the owner reference and the codes only, and every fixture is synthetic.
- The contract names only rwb-integration's own operations as provided; the P3 and P4 operations are consumed and are never restated as this service's (DP-01, DP-13).
- One REST base and one topic per service; a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- The case, the queue and the timer appear nowhere as objects of this service, and no foreign key leaves `rwb_integration` (DP-01, DP-15).
- The read is declared read-only, so a contract that lets the app write a row, publish an event or start a workflow fails this document.
- The duplication with the P3 case list and export is stated in 12.1, 12.7 and BR9, and a change that hides it fails the review.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-WKM-002 | Team manager sees every team queue, filters by status, product and ageing, exports the view | The two provided operations, the filter set and the export column set | TC-P2-E2033-CON-02, TC-P2-E2033-CON-03 |
| REQ-DVH-006 | Deviation flag visible in every queue view | `deviationOpen` on the page row and in the export columns | TC-P2-E2033-CON-02 |
| REQ-ACA-006 | Every read of the case store is written to the access log | The access-log operation consumed and one entry per export declared | TC-P2-E2033-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The eight consumed operations with the 2 s client budget and the unavailable answer | TC-P2-E2033-CON-06 |

### 19. Out of scope

- The controller, the composition service, the calculator, the clock reader, the validator, the export writer, the clients and the screen support (RWB-P2-E2033-APP).
- The case list of rwb-case, its own export and the SCR-02 screen work of the owner's list (RWB-P3-E2033-APP and the Ownership Map rows that stay with P3).
- The case-list, ageing, case-record, queue, parameter and reference-data contracts themselves and their fakes as artefacts (RWB-P3-E1031-CON, RWB-P3-E2011-CON, RWB-P3-E1018-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON).
- The authorise contract, the guard library and the access-log operation (RWB-P4-E1037-CON and the rwb-access stories of this legacy key).
- The gateway-bff composite route, its path and its merge order (RWB-PLT-N001-CON).
- The service baseline, the problem mapping and the contract-test harness of rwb-integration (RWB-P2-E1007-CON and RWB-P2-E1007-APP).
- Any data-lake copy of the list or of the file (DP-17).
- The real cross-service journey with all services live (RWB-ITG-E2033-ITG).
- The field-level completeness of the consumed contracts (GAP-0661).
