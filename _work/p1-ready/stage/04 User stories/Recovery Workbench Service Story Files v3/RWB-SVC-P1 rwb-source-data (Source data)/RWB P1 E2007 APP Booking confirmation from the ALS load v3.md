# RWB-P1-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-E2007-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P1-T |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2007-CON; rwb-case contract (`rwb-case.yaml`, operation `getCasesCaseidAccounts`) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); base path /api/recovery/source-data/v1 |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-010, RD-P1-011, RD-P1-023, RD-P1-024, RD-P1-041, RD-P1-043, RD-P1-045, RD-P1-063, RD-P1-066, RD-P1-069 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to REQ-CHO-008) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- `case_list_row` is gone from P1: the account keys of the case come from rwb-case `GET /cases/{caseId}/accounts` (RD-P1-024; GAP-0595 fallback). `caseId` is the case uuid (RD-P1-023). Findings #2, #5.
- Facts are served only for the business date that `v_ace_account` is current for, behind `DailyCompletenessGate` for DP01 (RD-P1-010, RD-P1-041). Findings #1, #9.
- Contract rwb-source-data.yaml 5.1.0, the full `DataProductFreshness` record and the shared Problem body (RD-P1-004, RD-P1-005). Findings #3, #8, #11, #12, #13, #18, #20.
- One flag rule, NULL rule, personal-data rule and JOB-08 caller. Findings #6, #7, #10, #16.
- AC1 to AC13 rewritten, AC14 to AC24 added, test case references corrected. Findings #14, #15, #17, #19, #21.
- RD-P1-063, RD-P1-066 and RD-P1-069: the operations are cited as published in rwb-source-data.yaml 5.1.0 (`getBookingFacts`, `getBatchStatus`), `/batch-status` also admits the rwb-payment workload identity and answers `checksum` (AC2, AC20). Test case IDs follow Test Cases v9; message texts follow Error and Message Standard v6.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-007 for rwb-source-data. The two in-process reads the booking match took from the monolith — `AccountQuery.forCase(caseId, businessDate)` over `recovery.v_ace_account` and `BatchStatusQuery.forSource(sourceSystem, businessDate)` over `recovery.v_ace_batch_status` — become two REST operations of this service on base `/api/recovery/source-data/v1` (DP-11, DP-13): `GET /booking-facts` and `GET /batch-status`, with one response entity each and the per-field answer that the three Section B columns need while they do not exist (DP-01, DP-05; TSD P1 T3.10 point 1). The ACE facts stay read-only through this service's own views and are never copied (DP-05; Architecture v5 slides 11 and 29), the DP01 freshness element reuses the record of RWB-P1-E1015-APP so the caller's decision log entry can name the data it used, and the comparison, the outcome, the treatment state, the task, the decision entry and the event stay with the other slices of this legacy key: the BOOKING_MATCH package is rwb-decision's (DP-04), the outcome and the treatment state are rwb-treatment's, the task is rwb-case's, the decision entry is rwb-decision's and `TreatmentBooked` (EV-11) is rwb-payment's. This story evaluates no rule, marks no treatment booked, records no difference, raises no task, publishes no event and writes no row, so its build dependency list is empty and it builds against the published baseline, the view contract and the fake of RWB-P2-E2007-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 44 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)** whose approved settlement or restructure is confirmed from the next ALS batch, I want **the facts that the BOOKING_MATCH evaluation reads — one fact per account of the case with its TDR and settlement terms and its `data_as_of`, and the ALS batch status for the business date — to be two read operations of rwb-source-data, with a per-field "not available" answer before the Section B columns exist and no fact at all for a business date whose ALS batch is not COMPLETE**, so that **every booking confirmation is decided on facts read from one owned place, dated, and only for a day whose batch landed**.

This is the application slice of legacy RWB-E2-007 that serves the match. It owns exactly two things:

- **the booking-facts read** on base `/api/recovery/source-data/v1`: `GET /booking-facts?caseId=&businessDate=` (`caseId` is the case uuid) returns, per account of the case, `account_key`, `product_group`, `tdr_flag`, `last_tdr_date`, `principal_outstanding`, `interest_rate`, `settlement_booked_date`, `settlement_booked_amount` and `data_as_of`, read from `v_ace_account` for the ALS business date, with the DP01 freshness record beside them so the caller can record the data it used (DP01, LOADED or STALE);
- **the batch-status read**: `GET /batch-status?sourceSystem=&businessDate=` returns `status`, `is_complete`, `completed_at`, `started_at`, `record_count`, `feed_version` and `checksum` from `v_ace_batch_status` — the gate the match runs behind, so no fact is read for a business date whose ALS batch is not COMPLETE.

It also carries the Section B availability rule of the legacy key: `principal_outstanding`, `settlement_booked_date` and `settlement_booked_amount` are three of the ALS columns that RWB-ACE-001 adds to ACE `account`, and they reach `v_ace_account` only with the Section B view migration (TSD P1 T3.10 point 1; DL43; FSD P1 AC-EXC-P1-001-06). Before that migration the read answers "not available" per field, the story stays behind its flag, and no booking can be confirmed from a missing field.

It does **not** decide anything. The BOOKING_MATCH package and its rows are rwb-decision's (DP-04; D-RCV-36); the evaluation, the outcome `BOOKED` / `NO_BOOKING` / `TERMS_DIFFER`, the difference and the treatment state are rwb-treatment's (S2); the task `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` or `UNMATCHED_EXCEPTION` is rwb-case's (P3); the decision log entry is rwb-decision's (P7); and `TreatmentBooked` (EV-11) on `rwb.payment.events.v1` is rwb-payment's. This story compares no term, marks no treatment booked, records no difference, raises no task, publishes no event and writes no row. Those criteria sit with the rwb-integration, rwb-treatment, rwb-case, rwb-decision and exception slices of this legacy key and with the cross-service proof of RWB-ITG-E2007-ITG.

### 2. Business rationale

The officer books a restructure or a settlement in ALS by hand (INT-03), and nothing checks today that the booked terms equal the approved terms: 44 percent of TDR cases deviate (R-RES-10). ACE ingests the ALS batch and the booked terms appear on the account, so a comparison over ACE is the only check that needs no file the Workbench has to load (D-RCV-35 U1; DL12). Every approved treatment is confirmed as booked, or raised as missing or differing, by the next batch; the measure is REC-03, approved treatments against bookings, zero after two days. Serves REQ-CHO-008.

The comparison itself is not this story's, and that is the point of the split. In the monolith the match, the facts and the rule evaluation were one service over one schema. In the target the facts come from the service that owns the ACE read path (DP-05; Architecture v5 slides 15 and 29, "only rwb-source-data reads the 30 `recovery.v_ace_*` views"), the package comes from the service that governs rules (DP-04; Temporal and Drools design slide 15, governance central in rwb-decision), the outcome is a treatment fact (S2), the escalation is case work (P3) and the proof is a decision record (P7). The two reads of this story are the seam: everything the match decides is decided on what they answer, and nothing they answer is a decision.

Two properties of that seam are worth naming. The first is **the gate**. BR8 of the legacy key says no missing booking is raised for a business date whose ALS batch is not COMPLETE, and the only place that can enforce it without a race is the read: if the fact is not answered for such a date, no caller can compare against a half-loaded day (BR-P1-014-4; FSD P1 A2.14; AC-EXC-P1-011-01). The second is **the honest blank**. Three of the compared terms arrive only with the Section B columns, so before RWB-ACE-001 lands the read must say so per field rather than return a zero amount or a default date; a booking confirmed from an absent term would be the one failure this story can prevent on its own (TSD P1 T3.10 point 1; DL43; AC-EXC-P1-001-06).

### 3. Preconditions

- The baseline of rwb-source-data is in place: schema `rwb_source_data`, the login `rwb_source_data`, the data dictionary and the data products of P1 (delivered by RWB-P1-E1001-APP), and the per-service sequence of the platform (RWB-PLT-E1044-CON) with its own history table. This story adds no version to that sequence.
- The 16 Section A views and the 14 Section B views exist in schema `recovery`, the login `rwb_source_data` holds SELECT on the 30 `recovery.v_ace_*` views and no privilege outside its own schema, and `v_ace_account` and `v_ace_batch_status` are among them (DP-02, DP-05; RWB-P1-E1069-APP; Architecture v5 slides 11 and 29). The views are the published baseline of this service and not a build dependency of this story.
- `DailyCompletenessGate` and `FreshnessQuery` of RWB-P1-E1015-APP are used as in-service interfaces; until that story is merged this story builds against stubs of both, and it is Done only against the real components (RD-P1-041).
- rwb-case publishes `GET /api/recovery/case/v1/cases/{caseId}/accounts` (operation `getCasesCaseidAccounts`, answering `CaseAccount` with `accountKey`, `linkedFrom` and `linkedTo`); this story builds against its fake. rwb-source-data holds no case list (RD-P1-024; GAP-0595).
- The two operations and the schemas `BookingFact`, `BookingFactsAnswer`, `FieldState` and `BatchStatusAnswer` are added by this story to rwb-source-data.yaml 5.1.0, with the freshness element `DataProductFreshness` of RWB-P1-E1015-CON; RWB-P2-E2007-CON consumes them (GAP-0594; RD-P1-005).
- For the three Section B fields only: `principal_outstanding`, `settlement_booked_date` and `settlement_booked_amount` reach `v_ace_account` with the Section B view migration of RWB-ACE-001 (TSD P1 T3.10 point 1; FSD P1 AC-ALT-P1-001-02; DL43 recommended answer A). In SIT, UAT and PROD the flag `rwb.dataengine.booking-facts` stays off until that migration is applied (RD-P1-043). In DEV and the pipeline the views are built over the Tier 2 fixture, and a view without the three columns proves the `NOT_AVAILABLE` answer.
- The caller is the booking-confirmation slice of this legacy key (RWB-P2-E2007-APP, service rwb-integration) with its workload identity token. JOB-08 is kept with rwb-integration and the rwb-payment owner row of Architecture v5 slide 44 is recorded as superseded for this job (GAP-0657, accepted under D-RCV-60). A case role reads the same facts only through the screens that call this contract (DP-19).
- `/batch-status` has a second caller, the rwb-payment workload identity, whose proceeds reconciliation uses the batch `checksum`; rwb-payment reads no ACE view (RD-P1-066, RD-P1-069). `/booking-facts` keeps the one caller.
- The 2 s budget, the breaker per downstream and the 5 s statement timeout on the views are configuration of the platform (DP-11; Architecture v5 slide 11).
- No approval is needed to build against a Draft contract baseline: the contract is tagged by RWB-P2-E2007-CON when its tests pass, and this story is in Draft status until then (D-RCV-60).

### 4. Flow

1. The booking-confirmation slice calls `GET /api/recovery/source-data/v1/booking-facts?caseId={caseId}&businessDate=D` with its workload identity, once per business date and case (DP-11, DP-13).
2. The service checks the identity and its right, then the flag `rwb.dataengine.booking-facts`.
3. `BookingFactsController` validates the parameters: `caseId` a uuid, `businessDate` a date. Otherwise 400 with MSG-GEN-001 naming the field and nothing is read (RD-P1-023).
4. `BatchStatusGate` calls `DailyCompletenessGate.check(D, [DP01])`, the ALS row of `v_ace_batch_status` with status `COMPLETED` and `is_complete` true. Otherwise 409 with MSG-P1-001 and nothing else is read (AC3; BR2; RD-P1-041).
5. `CaseAccountReader` calls rwb-case `GET /cases/{caseId}/accounts` with the caller's token, one hop, 2 s, and keeps the links with `linkedFrom` on or before D and `linkedTo` empty or on or after D. rwb-case 404 (unknown case or outside scope) is answered 404 with MSG-P4-003 (RD-P1-024).
6. `BookingFactRepository` reads `recovery.v_ace_account` for those account keys, SELECT only, with the 5 s statement timeout. If a row has `data_as_of` other than D, the call answers 409 with MSG-P1-001 and no fact: the view holds current state only, so no later value is labelled D (the predicate of RD-P1-010 rule 4).
7. `BookingFactsAssembler` builds one `BookingFact` per account; `productGroup` is the ACE `product_category` of the account (DF-ACE-010; RD-P1-010 rule 5). `FieldAvailability` marks the three Section B fields `AVAILABLE` or `NOT_AVAILABLE` from the columns the view exposes.
8. `FreshnessReader` takes the DP01 stamp in use from `FreshnessQuery` and attaches the full `DataProductFreshness` record (RD-P1-005, RD-P1-041).
9. The call answers 200 with the freshness record and the facts in account-key order; a case with no linked account for D answers an empty fact list (X4).
10. The call writes nothing, publishes nothing and records no decision: no outbox row, no treatment write, no task (AC4, AC6; BR5). The caller builds BookingMatchFacts and calls the rule evaluator (DP-04; section 19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ALS row for the business date is absent, `RUNNING`, `FAILED` or not `is_complete` | 409; rwb-case and `v_ace_account` are not read | MSG-P1-001 | AC3 |
| X2 | A view or the freshness stamp does not answer, or the 5 s statement timeout fires | 503; no fact and no partial page | MSG-GEN-006 | AC7, AC10, AC24 |
| X3 | A Section B column is absent from `v_ace_account` | 200; the three fields answer `NOT_AVAILABLE` with no value | None | AC5 |
| X4 | The case has no account link covering the business date | 200 with an empty fact list and the freshness record; no account key is invented | None | AC23 |
| X5 | The same read is made twice | The second answer carries the same values; nothing is written | None | AC4 |
| X6 | A required parameter is missing or empty, `caseId` is not a uuid or `businessDate` is not a date | 400 with `field`; nothing is read | MSG-GEN-001 | AC8, AC11 |
| X7 | A caller without the read right, or without a valid credential | 403 or 401 | MSG-P4-002, MSG-P4-001 | AC9, AC12, AC20 |
| X8 | The business date is not the date `v_ace_account` is current for | 409; no fact | MSG-P1-001 | AC14 |
| X9 | rwb-case does not know the case, or it is outside the caller's scope | 404 | MSG-P4-003 | AC15 |
| X10 | rwb-case does not answer in 2 s or answers an error | 503 naming rwb-case; no fact | MSG-GEN-006 | AC24 |
| X11 | Flag `rwb.dataengine.booking-facts` is off | 404 on both operations (RD-P1-045 item 4); nothing is read | Pending: message ID of the flag-off 404, owner Error and Message Standard owner (GAP-3506) | AC19 |
| X12 | No batch row for the source and date on `/batch-status` | 404 | MSG-P1-001 | AC13 |

X1 and X3 are the two exception paths this slice owns: the legacy X4 (a batch that is not COMPLETE) carried onto the read, and the Section B absence the legacy key states in its preconditions. The others are the ordinary paths of a read contract. The legacy exception paths X1, X2, X3, X5, X6, X7, X8 and X9 belong to the slices that raise the task, mark the booking and write the decision entry, and are not restated here. The 5 s statement timeout is the server limit and the 2 s budget is the caller's, so a caller may see its own client timeout first and X2 is proved at the service. Pending: latency target of `/booking-facts` with its nested rwb-case hop, owner solution architect (GAP-3514).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published baseline, the views, the rwb-case fake and stubs of the gate and freshness interfaces; needs no live rwb-treatment, rwb-case or rwb-decision |
| Negotiable | The internal class split, the ordering of the facts, the statement timeout and the shape of the availability marker are the squad's choice behind the contract; the nine values, the gate and the per-field answer are fixed |
| Valuable | One read of the ACE facts and one read of the batch status for the whole booking-confirmation slice, dated, gated and honest about a field the view does not hold |
| Estimable | Two controllers, one repository, one case-contract client, one gate, one assembler, one availability map and one freshness reader |
| Small | Fits one sprint with its tests, as the read slice of the legacy key |
| Testable | Every criterion in section 7 is one call against a view fixture and the contract fake, plus one boundary assertion on the SQL |

### 7. Acceptance criteria

```gherkin
Feature: The facts of the booking confirmation, read from the ALS batch

  Background:
    Given synthetic case "c0000000-0000-4000-8000-000000000701" (case number "RW-2026-000701") holds accounts "A-0701", "A-0702" and "A-0703" in the rwb-case fake, each linkedFrom 2026-11-01 with no linkedTo
    And the latest COMPLETED ALS batch is for business date 2026-12-16 and every v_ace_account row of the three accounts has data_as_of 2026-12-16 and product_category "MORTGAGE"
    And the DP01 stamp in use is businessDate 2026-12-16, sourceSystem "ALS", sourceExtractedAt 2026-12-17T05:40+07:00, loadedAt 2026-12-17T05:42+07:00, status "LOADED", staleSince null
    And flag "rwb.dataengine.booking-facts" is on and the caller is the booking-confirmation workload identity with the read right

  Scenario: AC1 The booking facts of the case's accounts (new, D-RCV-60)
    Given v_ace_account holds these rows
      | account | tdr_flag | last_tdr_date | principal_outstanding | interest_rate | settlement_booked_date | settlement_booked_amount |
      | A-0701  | true     | 2026-12-16    | 650000.00             | 4.2500        | 2026-12-16             | 650000.00                |
      | A-0702  | false    | null          | 1800000.00            | 4.5000        | null                   | null                     |
      | A-0703  | true     | 2026-12-16    | 1800000.00            | 4.5000        | null                   | null                     |
    When GET /booking-facts?caseId=c0000000-0000-4000-8000-000000000701&businessDate=2026-12-16 is called
    Then the answer is 200 with three facts in account-key order, each equal to its row, with productGroup "MORTGAGE" and dataAsOf 2026-12-16
    And freshness is the DataProductFreshness record of DP01 with the values of the Background
    And the answer carries no outcome, compared term, difference or package version
    And no row, outbox message or decision record is written

  Scenario: AC2 The batch status the match runs behind (new, D-RCV-60)
    Given the ALS batch for 2026-12-16 is COMPLETED, started 2026-12-16T23:30+07:00, completed 2026-12-17T05:40+07:00, record count 184500, feed version "ALS-2026.12"
    And the ALS batch for 2026-12-17 is "FAILED" and the ALS batch for 2026-12-18 is "RUNNING"
    When GET /batch-status?sourceSystem=ALS is called for each of the three business dates
    Then the first answers 200 status "COMPLETED", isComplete true, startedAt, completedAt, recordCount 184500 and feedVersion "ALS-2026.12" as given
    And the second answers 200 status "FAILED" and isComplete false
    And the third answers 200 status "RUNNING", isComplete false and completedAt null
    And each answer holds checksum equal to the checksum of its view row, or null when the row holds none

  Scenario: AC3 A business date whose ALS batch is not complete (new, D-RCV-60)
    Given the ALS batch for 2026-12-17 is "FAILED"
    When GET /booking-facts for the case and 2026-12-17 is called
    Then the answer is 409 with messageCode MSG-P1-001 and the detail names DP01 and the date 2026-12-16
    And the body holds no fact, no statement runs against v_ace_account and rwb-case is not called
    And the same holds when the 2026-12-17 row is "RUNNING" or absent

  Scenario: AC4 The same read twice (new, D-RCV-60)
    Given the view rows, the case account links and the stamp are unchanged between two calls
    When GET /booking-facts for 2026-12-16 is called twice
    Then both bodies are equal
    And no row of schema rwb_source_data is written

  Scenario: AC5 A Section B field the view does not hold (new, D-RCV-60)
    Given a pipeline database whose v_ace_account has no principal_outstanding, settlement_booked_date and settlement_booked_amount column, with the flag on
    When GET /booking-facts for 2026-12-16 is called
    Then the answer is 200 and fieldState marks the three fields "NOT_AVAILABLE" with no value
    And accountKey, productGroup, tdrFlag, lastTdrDate, interestRate and dataAsOf are as the view holds them
    And no zero amount and no default date appears for the three fields

  Scenario: AC6 The answer is facts and nothing else (new, D-RCV-60)
    When GET /booking-facts for 2026-12-16 is called
    Then the response has exactly the properties of section 12.1
    And the boundary test finds only recovery.v_ace_account, recovery.v_ace_batch_status and data_product_load in the SQL of the call and in the two in-service interfaces
    And the call writes no row and publishes no message

  Scenario: AC7 A source of the booking facts that does not answer (new, D-RCV-60)
    Given the 5 s statement timeout fires on recovery.v_ace_account
    When GET /booking-facts for 2026-12-16 is called by a client with no shorter deadline
    Then the answer is 503 with messageCode MSG-GEN-006 naming the ACE database, with no fact and no partial page

  Scenario: AC8 A missing or malformed parameter (new, D-RCV-60)
    When GET /booking-facts is called without caseId, with an empty businessDate and with businessDate=not-a-date
    Then each answers 400 with messageCode MSG-GEN-001 and field naming the parameter
    And neither rwb-case nor a view is read

  Scenario: AC9 A caller without a credential or without the read right (new, D-RCV-60)
    When GET /booking-facts for 2026-12-16 is called with no valid credential
    Then the answer is 401 with messageCode MSG-P4-001
    When it is called by an identity without the read right
    Then the answer is 403 with messageCode MSG-P4-002
    And neither rwb-case nor a view is read

  Scenario: AC10 A batch-status view that does not answer (new, D-RCV-60)
    Given the 5 s statement timeout fires on recovery.v_ace_batch_status
    When GET /batch-status?sourceSystem=ALS&businessDate=2026-12-16 is called by a client with no shorter deadline
    Then the answer is 503 with messageCode MSG-GEN-006 and no batch status

  Scenario: AC11 A case number instead of the case uuid (new, D-RCV-60)
    When GET /booking-facts?caseId=RW-2026-000701&businessDate=2026-12-16 is called
    Then the answer is 400 with messageCode MSG-GEN-001 and field "caseId"
    And neither rwb-case nor a view is read

  Scenario: AC12 A caller without a credential or without the right on the batch-status read (new, D-RCV-60)
    When GET /batch-status?sourceSystem=ALS&businessDate=2026-12-16 is called with no valid credential
    Then the answer is 401 with messageCode MSG-P4-001
    When it is called by an identity without the read right
    Then the answer is 403 with messageCode MSG-P4-002
    And no view is read

  Scenario: AC13 No batch row for the source and date (new, D-RCV-60)
    Given recovery.v_ace_batch_status holds no row for source ALS at 2026-12-19
    When GET /batch-status?sourceSystem=ALS&businessDate=2026-12-19 is called
    Then the answer is 404 with messageCode MSG-P1-001

  Scenario: AC14 A past business date after a later batch (new, D-RCV-60)
    Given ALS is COMPLETED for 2026-12-16 and 2026-12-17 and the v_ace_account rows have data_as_of 2026-12-17
    When GET /booking-facts for the case and 2026-12-16 is called
    Then the answer is 409 with messageCode MSG-P1-001 and no fact

  Scenario: AC15 A case rwb-case does not know (new, D-RCV-60)
    Given rwb-case answers 404 for caseId "c0000000-0000-4000-8000-000000000799"
    When GET /booking-facts for it and 2026-12-16 is called
    Then the answer is 404 with messageCode MSG-P4-003 and no view of account facts is read

  Scenario: AC16 Booked terms that are NULL (new, D-RCV-60)
    Given the three Section B columns exist and A-0702 has NULL settlement_booked_date and settlement_booked_amount
    When GET /booking-facts for 2026-12-16 is called
    Then for A-0702 both properties are null, their fieldState is "AVAILABLE", and no zero or default date appears

  Scenario: AC17 The gate passes before the stamp of the date is written (new, D-RCV-60)
    Given the DP01 stamp in use is still businessDate 2026-12-15 with status "LOADED" while ALS is COMPLETED for 2026-12-16
    When GET /booking-facts for 2026-12-16 is called
    Then the answer is 200 and freshness carries the stamp in use, businessDate 2026-12-15

  Scenario: AC18 A stale stamp (new, D-RCV-60)
    Given the DP01 stamp in use has status "STALE" and the gate answers COMPLETE for 2026-12-16
    When GET /booking-facts for 2026-12-16 is called
    Then the answer is 200 and freshness.status is "STALE"

  Scenario: AC19 The flag off (new, D-RCV-60)
    Given flag "rwb.dataengine.booking-facts" is off
    When either operation is called
    Then the answer is 404 and neither rwb-case nor a view is read

  Scenario: AC20 Only the allowed identity (new, D-RCV-60)
    Given the booking-confirmation workload identity, the rwb-payment workload identity and a third service identity
    When each calls both operations
    Then the booking-confirmation identity is answered on both
    And the rwb-payment identity is answered on /batch-status and gets 403 with MSG-P4-002 on /booking-facts
    And the third identity gets 403 with MSG-P4-002 on both

  Scenario: AC21 Logging of personal fields (new, D-RCV-60)
    Given one successful and one refused booking-facts read
    When the logs and traces are inspected
    Then the access log records caller, operation and time for the successful read
    And no log line or trace attribute holds an account_key

  Scenario: AC22 Several batch rows for one source and date (new, D-RCV-60)
    Given a FAILED run and a later COMPLETED run for ALS on 2026-12-16
    When GET /batch-status for that source and date is called
    Then the values of the later run are answered and the booking-facts gate passes

  Scenario: AC23 A case with no linked account on the date (new, D-RCV-60)
    Given rwb-case answers an empty account list for the case
    When GET /booking-facts for 2026-12-16 is called
    Then the answer is 200 with facts empty and the freshness record

  Scenario: AC24 rwb-case or the stamp unavailable (new, D-RCV-60)
    Given rwb-case does not answer inside 2 s, and in a second run data_product_load does not answer
    When GET /booking-facts for 2026-12-16 is called
    Then each run answers 503 with messageCode MSG-GEN-006 and no fact
```

**Target reading.** Every criterion tests only the two reads. `AccountQuery.forCase(caseId, businessDate)` of legacy §12 is `GET /booking-facts`, and `BatchStatusQuery.forSource(sourceSystem, businessDate)` is `GET /batch-status` (DP-11, DP-13), both published in rwb-source-data.yaml 5.1.0 (GAP-0594; ASM-0836; RD-P1-005). The account set of AC1 comes from rwb-case's `getCasesCaseidAccounts`, the fallback GAP-0595 names, because P1 holds no case list (RD-P1-024); the product group is the ACE `product_category` (RD-P1-010). The views are read in-process under the `rwb_source_data` login, SELECT only, and no value is copied into a table (DP-02, DP-05). The freshness element is the whole `DataProductFreshness` record of RWB-P1-E1015-CON: `loadedAt` is when the Workbench wrote the stamp and `sourceExtractedAt` is the ACE batch completion (RD-P1-005). The three Section B values come with the Section B view migration of RWB-ACE-001; AC5 states the answer when the column is absent and AC16 when it holds NULL (GAP-0596; ASM-0838). AC2, AC3 and AC13 carry the legacy AC5 onto the reads (GAP-0597; ASM-0839); where a source and date have several batch rows the later run decides, as a failed-after-completed date is treated as failed (RD-P1-041 item 6). AC6 is the boundary of the split (DP-04; GAP-0598; ASM-0840). Legacy AC1, AC2, AC3, AC4, AC7, AC8 and AC9 are owned by the other slices and by RWB-ITG-E2007-ITG, and this story claims none of them. Pending: the answer when a linked account has no `v_ace_account` row, owner data architect (GAP-3515).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A booking is made by the officer in ALS and confirmed only from the next ACE batch; the Workbench never reads ALS and never times its own load | INT-03; DL12; D-RCV-35 U1 |
| BR2 | No fact is read for a business date whose ALS batch is not COMPLETE, and no missing booking is raised for such a date | BR8 of RWB-E2-007; BR-P1-014-4; FSD P1 A2.14; CTL-02 |
| BR3 | The terms read are the account facts ACE holds: `tdr_flag`, `last_tdr_date`, `principal_outstanding`, `interest_rate`, `settlement_booked_date` and `settlement_booked_amount`, each with `data_as_of` | DF-ACE-030, DF-ACE-031, DF-ACE-025, DF-ACC-009, DF-ACC-030, DF-ACC-031, DF-ACE-036; legacy BR2, BR3 |
| BR4 | A fact carries the account key, the product group of the case and the six account facts, and nothing a decision needs to be compared with | DF-RPT-005, DF-RPT-007; legacy BR10 |
| BR5 | The comparison, the tolerance and the outcome are rows of package BOOKING_MATCH evaluated through the rule evaluator; this read holds no comparison code, no rule table and no tolerance | D-RCV-36 T3, T5; ADR-012; legacy BR10 |
| BR6 | A Section B field that the view does not hold answers not available; no zero amount, no default date and no inferred value is substituted | TSD P1 T3.10 point 1; FSD P1 AC-EXC-P1-001-06; DL43 |
| BR7 | The completeness gate reads `v_ace_batch_status`; the freshness shown beside the facts is the DP01 stamp in use, read through `FreshnessQuery`, with its business date and status | BR-P1-014-2; TSD P1 T3.7 "Display"; legacy BR9; RD-P1-041 |
| BR8 | No value a business person may change is written in code: the source system is a request parameter, the product group is the ACE `product_category`, and the status values are those ACE writes | BR-P1-001, BR-P1-002; DP-07; RD-P1-010 |
| BR9 | The only personal data in the answer is `account_key`, an indirect identifier classified Confidential: it is never logged or traced, every read is access logged and it is masked in UAT; no account number, name or contact field is read | Data Classification v5; NFR-P1-009; legacy §17; FSD P1 BR-P1-001-6 |
| BR10 | A fact is served only when its `data_as_of` equals the requested business date | RD-P1-010 rule 4 |

**Where each rule lives in the target.** BR1, BR2 and BR10 are enforced by the gate of flow step 4 and the date check of step 6, so the refusal is the read's own 409 and not the caller's check (AC3, AC14). BR3 and BR4 are the projection of the answer: the account columns of `recovery.v_ace_account`, `data_as_of` beside them, and the account keys of the case from the rwb-case contract. BR5 is a prohibition: the row that decides, its version and the tolerance stay in rwb-decision (DP-04; D-RCV-36). BR6 is the availability map of the three Section B fields; this story only refuses to invent a value (AC5, AC16). BR7 is the freshness record, which can differ from `data_as_of` (AC17, AC18). BR8 and BR9 are the shape of the request, the answer and the logs (AC21).

### 9. State transitions

None in the case model: this story changes no case status, no treatment state and no booking outcome. It does not even move a freshness status; it reads the stamp that RWB-P1-E1015-APP writes.

| From | Event | Condition | To |
|---|---|---|---|
| no answer for the case and business date | a booking-facts call | The ALS row for the date is COMPLETED and `data_as_of` equals the date | An answer with one fact per linked account and the DP01 freshness record |
| no answer for the case and business date | a booking-facts call | The ALS row is absent, `RUNNING`, `FAILED` or not complete, or the account data is current as of another date | A refusal with 409 and MSG-P1-001; no fact |
| an answer with the three Section B fields available | the same call | The Section B view migration is applied | The same answer, the three fields carrying their values |
| an answer with the three Section B fields not available | the same call | The Section B view migration is not applied | The same answer, the three fields marked `NOT_AVAILABLE` with no value |
| any answer | a second identical call | The views and the stamp are unchanged | The identical answer; nothing is written |
| a batch row `COMPLETED` | the cut-off of DP01 | The batch for the expected date does not complete | The stamp turns `STALE` through RWB-P1-E1015-APP; this read reports it and changes nothing |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-source-data service identity (`rwb_source_data` login) | Reads the two views and the freshness stamp; calls the rwb-case account read; writes nothing |
| The booking-confirmation slice of this legacy key, as the rwb-integration workload identity (JOB-08, GAP-0657) | Calls the two reads; builds its own facts; evaluates the package; takes every consequence |
| rwb-payment (P8), as its workload identity | Calls `/batch-status` only, for the batch row and its `checksum` (RD-P1-066, RD-P1-069) |
| RW-RESTRUCT, restructuring officer | Reads the facts through the treatment record screen of rwb-treatment and the case record data panel, which call this contract through gateway-bff |
| RW-CREDITAD, Credit Administration officer | Reads the facts on the differing-terms task of the rwb-case slice |
| RW-DATASTEW, data steward | Reads the DP01 stamp and the batch status; owns the freshness rows the element reports |
| RW-PLATADM, platform administrator | Operates the deployment and the flag; reads the metrics and the traces of the two operations |
| rwb-decision (P7) | Owns the BOOKING_MATCH package, its rows and versions, and the decision log entry the caller writes |
| rwb-treatment (S2) | Owns the outcome, the difference and the treatment state; this read returns none of them |
| rwb-case (P3) | Owns the case, its accounts and the tasks the caller raises; serves the account set through `getCasesCaseidAccounts` |
| rwb-payment (P8) | Owns the event `TreatmentBooked` |

The read runs as the service identity of rwb-source-data (DP-02; Architecture v5 slides 11 and 29), and the caller's identity travels in the workload token so that a refusal is made for the caller and not for the service. No delegation limit and no approval level applies: this story takes no decision. The edge check that refuses a caller without the read right is the rwb-access authorise check of DP-08; Pending: the authorise operation name and the allow list of roles that reach the reads through gateway-bff, owner security architect (DOR-RWB-P1-E2007-APP-6; GAP-3513). Until it is fixed only the booking-confirmation workload identity is allowed, and on `/batch-status` also the rwb-payment workload identity (RD-P1-066).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-010 | v_ace_account | product_category | Read (the product group) |
| DF-ACE-030 | v_ace_account | last_tdr_date | Read |
| DF-ACE-031 | v_ace_account | tdr_flag | Read |
| DF-ACE-025 | v_ace_account | interest_rate | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACC-009 | v_ace_account | principal_outstanding | Read (Section B, RWB-ACE-001) |
| DF-ACC-030 | v_ace_account | settlement_booked_date | Read (Section B, RWB-ACE-001) |
| DF-ACC-031 | v_ace_account | settlement_booked_amount | Read (Section B, RWB-ACE-001) |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-180 | v_ace_batch_status | started_at | Read |
| DF-ACE-181 | v_ace_batch_status | completed_at | Read |
| DF-ACE-182 | v_ace_batch_status | status | Read |
| DF-ACE-183 | v_ace_batch_status | record_count | Read |
| DF-ACE-184 | v_ace_batch_status | checksum | Read |
| DF-ACE-185 | v_ace_batch_status | feed_version | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-OPS-002 | data_product_load | product_code | Read |
| DF-OPS-004 | data_product_load | business_date | Read |
| DF-OPS-006 | data_product_load | loaded_at | Read |
| DF-OPS-007 | data_product_load | status | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. The three Section B fields keep their frozen field-gap IDs until the LDM assigns `DF-ACE` IDs to the 12 added columns (legacy §11 note; TSD P1 T3.10 point 1). Decision DL43 is still open and this story builds on its recommended answer A (assumptions ASM-0193, ASM-0737, ASM-0748 and ASM-0816); DL12 is still open and the story builds on its recommended answer A, no legacy enhancement, with source data read only through the views (ASM-0189, ASM-2559 and ASM-2608). Contract types: `tdrFlag` boolean, dates as date, amounts and `interestRate` as decimals at the scale of the view column (`interestRate` numeric(7,4)), `recordCount` integer.

**Which side is this story's.** Every row above is a read, and this story owns no write: it creates no table, adds no column and no index, and inserts nothing. The account facts are the content of the answer; `data_as_of` travels with each fact and says how current the ACE row is, while the freshness record says how current the product is (FSD P1 BR-P1-014-2). `data_product_load` is written by RWB-P1-E1015-APP and read here through `FreshnessQuery`. The account keys of the case are `CaseAccount.accountKey` of the rwb-case contract. Nothing of `case_account`, `treatment`, `task` or `decision_log_entry` is read in SQL, and no foreign key crosses a schema.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13). Build contract rwb-source-data.yaml 5.1.0 (API Specification v7), to which this story adds the two operations; RWB-P2-E2007-CON consumes them (RD-P1-005).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/booking-facts` (`getBookingFacts`) | The booking facts of one case for one ALS business date, with the DP01 freshness record | The booking-confirmation workload identity (rwb-integration); roles through gateway-bff are pending (GAP-3513) | Idempotent read; no `Idempotency-Key` header |
| GET | `/batch-status` (`getBatchStatus`) | The batch row of one source and business date — the gate the facts are read behind | As above, and the rwb-payment workload identity (RD-P1-066) | Idempotent by source and business date |

**Query.** `/booking-facts`: `caseId` (required, uuid of `rwb_case.recovery_case.id`, never the case number), `businessDate` (required, date). `/batch-status`: `sourceSystem` (required, the ACE source code as `v_ace_batch_status` holds it), `businessDate` (required, date). Missing or malformed values answer 400.

**Response entities.** `BookingFactsAnswer`: `freshness`, the `DataProductFreshness` record of RWB-P1-E1015-CON for DP01 with all its properties (`productCode`, `productName`, `sourceSystem`, `businessDate`, `sourceExtractedAt`, `loadedAt`, `status`, `staleSince`), and `facts`, a list of `BookingFact` with `accountKey`, `productGroup`, `tdrFlag`, `lastTdrDate`, `principalOutstanding`, `interestRate`, `settlementBookedDate`, `settlementBookedAmount`, `dataAsOf` and `fieldState`. `fieldState` names each of the three Section B fields `AVAILABLE` or `NOT_AVAILABLE`; `NOT_AVAILABLE` means the view has no such column and the value is null; a column that exists and holds NULL is `AVAILABLE` with value null. `tdrFlag`, `lastTdrDate`, `principalOutstanding`, `interestRate`, `settlementBookedDate` and `settlementBookedAmount` are nullable. `BatchStatusAnswer`: `sourceSystem`, `businessDate`, `status` (`COMPLETED`, `FAILED`, `RUNNING`), `isComplete`, `startedAt`, `completedAt` (null while running), `recordCount`, `feedVersion`, `checksum` (string of at most 64 characters, nullable; `v_ace_batch_status.checksum`; RD-P1-069).

**Errors.** `application/problem+json` with the shared `Problem` schema (RD-P1-004): 400 MSG-GEN-001 with `field`; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003 from `/booking-facts` for a case rwb-case does not know or outside scope; 404 MSG-P1-001 from `/batch-status` for a source and date with no batch row (GAP-0597); 409 MSG-P1-001 from `/booking-facts` when the gate does not answer COMPLETE or the account data is current as of another date, with the detail naming DP01 and the date; 503 MSG-GEN-006 naming the ACE database or rwb-case.

#### 12.2 REST operations consumed

| Provider | Operation | Use | Budget | Failure |
|---|---|---|---|---|
| rwb-case | `GET /api/recovery/case/v1/cases/{caseId}/accounts` (`getCasesCaseidAccounts`, `CaseAccount[]`; Case record R), called with the caller's token | The account keys linked to the case on the business date | 2 s, one hop | 404 answered as 404 MSG-P4-003; timeout or error answered as 503 MSG-GEN-006 |

The consumer build runs against the rwb-case fake of the same contract version (RD-P1-011). The ACE facts are read in this service's own views, and the gate and the freshness stamp are in-service components (DP-01, DP-05). RWB-P2-E2007-CON is a build-time contract, not a run-time call.

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slide 43, rows 26 and 27). This story publishes no event and writes no outbox row. `TreatmentBooked` (EV-11) on `rwb.payment.events.v1` is rwb-payment's, published by the slice that marks the booking.

#### 12.4 Events consumed

None. The read is called over REST by the booking-confirmation slice, which is itself started by `rwb.source-data.AceDataReady.v1`; the consumption of that event and the workflow that runs JOB-08 are that slice's and not this story's (Architecture v5 slides 43 and 44). The writes of the match — the treatment state, the difference, the task, the decision entry and the event — are not this story's either: this read writes nothing at all.

#### 12.5 Workflows and activities

None. Both reads are synchronous REST steps and neither writes a row. JOB-08 Booking confirmation runs in the calling service (GAP-0657); this story starts no workflow and no activity on task queue `rwb-source-data`.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: the caller is started by `AceDataReady` and this story answers when called.

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `v_ace_account` | `recovery` | View owner `ace_view_owner`; contract owner P1 rwb-source-data (Ownership Map: a data product of ACE read through the views; RWB-P1-E1069-APP) | None new: read only, SELECT through the `rwb_source_data` login, 5 s statement timeout; the three Section B columns only after the Section B view migration |
| `v_ace_batch_status` | `recovery` | View owner `ace_view_owner`; contract owner P1 rwb-source-data (Ownership Map: the freshness of every product; RWB-P1-E1015-APP) | None new: read only; the gate |
| `data_product_load` | `rwb_source_data` | P1 rwb-source-data (RWB-P1-E1015-APP writes it) | None new: read through `FreshnessQuery` for the DP01 freshness record |

No table of another service is read and no foreign key crosses a schema (DP-01). `case_account` stays in `rwb_case` with P3, `treatment` in `rwb_treatment` with S2, `task` in `rwb_case` with P3 and `decision_log_entry` in `rwb_decision` with P7; this read names none of them in SQL (AC6).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Provider fake of rwb-source-data.yaml 5.1.0, path `fakes/rwb-source-data/5.1.0/` | The two operations, for rwb-integration | One mapping per documented status of both operations. Pending: the P1 contract story that lists this fake, owner solution architect (GAP-3516) |
| rwb-case fake | `getCasesCaseidAccounts` | The three accounts of case c0000000-0000-4000-8000-000000000701, an empty list, 404 and a delay past 2 s |
| `recovery.v_ace_account` fixture | The view | The table of AC1 with `data_as_of` 2026-12-16 and `product_category` MORTGAGE, and a copy without the three Section B columns |
| `recovery.v_ace_batch_status` fixture | The view | ALS `COMPLETED` for 2026-12-16 (values of AC2), `FAILED` for 2026-12-17, `RUNNING` for 2026-12-18, no row for 2026-12-19, and the two runs of AC22 |
| `data_product_load` fixture | `FreshnessQuery` | The DP01 stamp of the Background, a stamp of 2026-12-15 and a `STALE` stamp |

The pattern table of section 13 also names the H rows RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON, and the C rows RWB-P7-E1073-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON plus the treatment and task contracts. This story calls none of them (12.2), so it needs no fake for them: they do not change its metadata rows, and it builds from Day 1 against the published contract and the fakes and fixtures above. Their entry in the dependency map is decided there and is not a precondition of this build.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/source-data/v1` | rwb-case `getCasesCaseidAccounts` | OpenAPI 3.1 (DP-13); published in rwb-source-data.yaml 5.1.0 |
| Kafka | None | None | `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP; `TreatmentBooked` is rwb-payment's |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file is read or written |
| SQL view | None | `recovery.v_ace_account` and `recovery.v_ace_batch_status`, with `data_product_load` in `rwb_source_data` | SELECT only, 5 s statement timeout, one login `rwb_source_data` (DP-02, DP-05) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `bookingfacts`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, views in schema `recovery`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

- **DP-01** is applied as the boundary of the answer: the two views stay in schema `recovery`, the stamp stays in `rwb_source_data`, and the case, its accounts, the treatment, the task and the decision entry stay with their owners and are never named in SQL; the account set arrives over the rwb-case contract.
- **DP-03** is a statement here and not a dependency of this story: a decision record is written by the caller through the local decision-record library, and this read only supplies the freshness the entry needs so that `inputs_ref` can state the product, the business date, the status and the load time (RWB-PLT-E1027-CON is the caller's dependency; the H list of this story is empty).
- **DP-04** is a prohibition here: the BOOKING_MATCH package is loaded, approved and versioned in rwb-decision and evaluated by the calling slice inside its own activity; this read holds no rule, no package code, no tolerance and no evaluator (D-RCV-36; RWB-PLT-E1072-CON and RWB-P7-E1073-CON are the caller's dependencies).
- **DP-05** is the read path of this story: `v_ace_account` and `v_ace_batch_status` are read in-process through the `rwb_source_data` login, SELECT only, with the 5 s statement timeout, and the same facts reach every other service through this contract and never through a second copy (ADR-010).
- **DP-06** is a statement here: no parameter is read on this path, and the parameter that governs the grace before a missing booking is raised (`booking.missing.grace_loads`) is read by the calling slice through the rwb-case parameters contract (RWB-PLT-E1042-CON and RWB-P3-E1042-CON are its dependencies, not this story's).
- **DP-07** is a statement here: no list is read and no value is validated against a list; the product group is the ACE `product_category` and the status values are those ACE writes (RWB-PLT-E1043-CON and RWB-P3-E1043-CON are the caller's dependencies).
- **DP-09** is a prohibition here: nothing is published and no outbox or inbox row is written, because a read produces no fact others may react to.
- **DP-10** is a statement here: JOB-08 runs in the calling service (GAP-0657) and this story owns no Schedule and no workflow.
- **DP-11** is how the two reads replace the two in-process calls: each is a REST contract with a fake, one hop from the caller, a 2 s budget and a breaker per downstream.
- **DP-13** is the base: every path of this story sits under `/api/recovery/source-data/v1`, and no monolith path is served.
- **DP-19** is a statement here: the treatment record screen and the case record data panel reach these facts through the gateway-bff composite route (RWB-PLT-N001-CON is the edge's dependency), and this story builds no screen and no route.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `BookingFactsController` | Controller | The two operations of 12.1 on `/api/recovery/source-data/v1`; RFC 9457 problem details; the error set |
| `BatchStatusGate` | Service | Calls `DailyCompletenessGate.check(businessDate, [DP01])`; checks `data_as_of`; maps a refusal to 409 MSG-P1-001 |
| `CaseAccountReader` | Contract client | Calls rwb-case `getCasesCaseidAccounts` (2 s, breaker) and keeps the links covering the business date |
| `BookingFactRepository` | Repository | Reads `recovery.v_ace_account` by account key, SELECT only, with the 5 s statement timeout; no write method exists |
| `FieldAvailability` | Service | Marks the three Section B fields `AVAILABLE` or `NOT_AVAILABLE` from the columns the view exposes, and never substitutes a value |
| `FreshnessReader` | Service | Takes the DP01 stamp in use from `FreshnessQuery` and builds the `DataProductFreshness` record |
| `BookingFact`, `BookingFactsAnswer`, `BatchStatusAnswer` | Entities | The published shapes of 12.1, immutable |
| `BookingFactsBoundaryTest` | Test | Fails the build on any statement outside `rwb_source_data` and `recovery`, on any write method on the two repositories, and on any outcome-shaped field in the answer (treatment term, outcome, difference, tolerance or package version) |

**Migrations.** None. This story creates no table, no column and no index and adds no Flyway version: everything it reads is either a view of `recovery` (created by RWB-P1-E1069-APP's two migrations) or a table of `rwb_source_data` delivered by RWB-P1-E1001-APP and RWB-P1-E1015-APP. The three Section B columns arrive with the Section B view migration of RWB-ACE-001, on the same sequence and under the object owner `ace_view_owner` (TSD P1 T3.10 point 1; DL43).

**Configuration and reference data**

- The flag `rwb.dataengine.booking-facts` gates both operations; off means 404 and nothing is read (RD-P1-045 item 4). In SIT, UAT and PROD it stays off until the Section B view migration is applied (RD-P1-043; ASM-0838).
- The source system is a request parameter and never a constant in code: `ALS` is the caller's value, as `v_ace_batch_status` holds it (BR8).
- The 5 s statement timeout on the views and the 2 s budget with the breaker on the caller's side are platform configuration (DP-11; Architecture v5 slide 11).
- The freshness values are data rows of `data_product_load` and of `data_product`, never constants in the code (DP-07).

**Build steps**

1. `BookingFactsController` and the two operations with the RFC 9457 body and the error set of 12.1 (X6, X7).
2. `BatchStatusGate` over `DailyCompletenessGate` with the `data_as_of` check, refusing `/booking-facts` with 409; `/batch-status` answers the row (AC2, AC3, AC13, AC14, AC22).
3. `CaseAccountReader` over the rwb-case fake, with the empty-list, 404 and unavailable paths (AC15, AC23, AC24).
4. `BookingFactRepository` over `recovery.v_ace_account`, keyed by account key, with the 5 s statement timeout and no write method (AC1).
5. `FieldAvailability` for the three Section B fields, with a view without the columns and a view with NULL values (AC5, AC16).
6. `FreshnessReader` over `FreshnessQuery` for the `DataProductFreshness` record (AC1, AC17, AC18).
7. The refusal and failure paths: the view error and the timeout as 503 with MSG-GEN-006 and no partial page (X2).
8. `BookingFactsBoundaryTest`: only `rwb_source_data` and `recovery` are named, and neither repository has a write method (AC4, AC6).
9. Tests for AC1 to AC24 against the fakes and fixtures of 12.8, the access log and redaction check (AC21), and provider verification of every fake mapping (RD-P1-011).

**Done when.** The tests in section 16 pass; `/booking-facts` answers the three facts of AC1 with the full freshness record; a FAILED batch or a past business date yields 409 with MSG-P1-001 and no fact; a view without the Section B columns answers `NOT_AVAILABLE`; a repeated call answers identical facts and writes nothing; no account key reaches a log; and the boundary test shows SQL only over `rwb_source_data` and `recovery`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ALS batch for the business date is not COMPLETED, or the account data is current as of another date; also `/batch-status` for a date with no row | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A required parameter is missing or malformed | Enter {field}. |
| MSG-P4-003 | rwb-case does not know the case, or it is outside scope | This case is not in your scope. |
| MSG-GEN-006 | A view does not answer, or the statement timeout fires | {system} is not available. Try again in a few minutes. |
| MSG-P4-001 | No valid credential (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | An identity without the read right | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10, built on its recommended answer A (assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863). The texts are those of Error and Message Standard v6. For a product that has never been stamped, `{date}` is left empty and tests assert the code and the product only; the wording is Pending, owner Error and Message Standard owner, tracked as GAP-3284 (RD-P1-062). MSG-P1-001 fills {product} with DP01 and {date} with the last business date whose ALS batch is COMPLETED (for the date check, the `data_as_of` the view holds). MSG-GEN-001 fills the parameter name and never a data value; MSG-GEN-006 fills {system} with "ACE database" or "rwb-case"; MSG-P4-002 fills {action} with the operation tried.

### 15. Screens and states

No screen in this story. The facts are shown on the treatment record SCR-14 of rwb-treatment, where the officer sees the booked terms or the difference, and in the data panel of the case record SCR-03; both screens reach this contract through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), and their field lists belong to the screen owners. The SCR-03 states are loading (per Screen Specifications v1 SCR-03); empty, error and no access are Not specified in the source documents (CG-ALL-2380), apart from the refusal message stated below. The SCR-14 states are empty, loading, error and no access, all Not specified in the source documents (CG-ALL-2381), apart from the refusal message stated next. When the read refuses, the screen shows MSG-P1-001 in the Error state of the panel and offers no booking confirmation for that date; when the Section B migration is not applied, the three terms show as not available and the screen offers no booking confirmation from them. This story renders none of it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-21 | AC1 | See Test Cases v9 | Fixtures of 12.8 |
| TC-P1-E2007-APP-01 | AC2 | Component | Batch-status fixture |
| TC-P1-E2007-APP-02 | AC3 | Component | FAILED, RUNNING, absent and past date |
| TC-P1-E2007-APP-03 | AC4 | Component | Fixtures of 12.8 |
| TC-P1-E2007-APP-18 | AC5, BR8 | Component | View without the three Section B columns |
| TC-P1-E2007-APP-19 | AC6 | Component | Fixtures of 12.8 |
| TC-P1-E2007-APP-04 | AC7 | Component | Statement timeout |
| TC-P1-E2007-APP-05 | AC8 | Contract | Missing and malformed parameters |
| TC-P1-E2007-APP-06 | AC9 | Contract | No credential, other identity |
| TC-P1-E2007-APP-25 | AC10 | Component | Statement timeout on the batch-status view |
| TC-E2-007-18 | AC11 | Component | A case number as caseId |
| TC-E2-007-19 | AC12 | Component | No credential, other identity |
| TC-E2-007-20 | AC13 | Component | No batch row for the date |
| TC-P1-E2007-APP-07 | AC14 | Component | Past date after a later batch |
| TC-P1-E2007-APP-08 | AC15 | Component | rwb-case 404 |
| TC-P1-E2007-APP-09 | AC16 | Component | NULL values |
| TC-P1-E2007-APP-10 | AC17 | Component | Earlier stamp |
| TC-P1-E2007-APP-11 | AC18 | Component | STALE stamp |
| TC-P1-E2007-APP-12 | AC19 | Component | Flag off |
| TC-P1-E2007-APP-13 | AC20 | Contract | Three workload identities |
| TC-P1-E2007-APP-14 | AC21 | Component | Log and trace inspection |
| TC-P1-E2007-APP-15 | AC22 | Component | Batch-status fixture |
| TC-P1-E2007-APP-16 | AC23 | Component | Empty account list |
| TC-P1-E2007-APP-17 | AC24 | Component | rwb-case delay, stamp failure |
| TC-P1-E2007-APP-20 | Section 12 operations, contract level | Contract | Fakes of RWB-P2-E2007-CON |
| TC-P1-E2007-APP-21 | Section 12.7 tables are read only | See Test Cases v9 | Fixtures of 12.8 |

The IDs follow Test Cases v9. The legacy rows TC-E2-007-01 to -04 and -07 to -10 prove criteria that other slices of RWB-E2-007 own and are not cited by this story; they run again in RWB-ITG-E2007-ITG. TC-P1-E2007-APP-22 to TC-P1-E2007-APP-24 are retired (RD-P1-024).

### 17. Guardrails

- No business value in code: the source system is a request parameter, the status values are those ACE writes, the product group is the ACE `product_category` and the freshness values are rows of `data_product_load` and `data_product` (DP-07).
- `account_key` is personal data (indirect identifier, Confidential): it is never written to a log, a trace or an error body, every read is access logged and it is masked in UAT; no account number, name or contact point is read (Data Classification v5; NFR-P1-009); the fixture is synthetic.
- No read of another service's table: `case_account`, `treatment`, `task` and `decision_log_entry` are named nowhere in SQL and no foreign key crosses a schema (DP-01; AC6).
- ACE data only through the owner's views, and only this service reads them (DP-05; ADR-010); the read holds SELECT and no privilege outside `rwb_source_data` and the 30 views.
- No rule, no comparison and no threshold in this service: the package, the tolerance and the outcome stay in rwb-decision and in the calling slice (DP-04; BR5).
- No write of any kind: no row, no outbox message, no decision record, no task and no event, so a repeated call cannot duplicate a fact (AC4, AC6).
- The read is one hop for the caller, 2 s budget with a breaker, and 5 s statement timeout on the views (DP-11).
- An applied migration is never edited, and this story adds no version at all: the three Section B columns come with the Section B view migration of RWB-ACE-001, on the sequence of this service and under the object owner (TSD P1 T3.10 point 1).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next day's ALS load | Business Requirements Program, section 5.3; Business Requirements Epic 2, section 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39 (evaluated by the calling slice, not here) | TC-P1-E2007-APP-18, TC-P1-E2007-APP-19, TC-P1-E2007-APP-25, TC-E2-007-18 to TC-E2-007-21, TC-P1-E2007-APP-01 to TC-P1-E2007-APP-17; the legacy rows TC-E2-007-01 to -04 and -07 to -10 prove the other slices |

The requirement is met by the legacy key as a whole: this story supplies the facts and the gate that the confirmation is decided on, and the comparison, the outcome, the state change, the task, the decision entry and the event are the work of the other slices of RWB-E2-007 and of RWB-ITG-E2007-ITG.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P2-E2007-CON | Contract | C: consumes the two reads as published in rwb-source-data.yaml 5.1.0 |
| RWB-P1-E1069-APP | App development | Sibling of the same service, a precondition and not an H dependency: the 30 `recovery.v_ace_*` views, their grants and the boundary rule this read runs under |
| RWB-P1-E1015-APP | App development | Sibling of the same service: `DailyCompletenessGate`, `FreshnessQuery` and the `DataProductFreshness` record |
| rwb-case contract (`getCasesCaseidAccounts`) | Contract | C: the account set of the case |
| RWB-P1-E2001-APP | App development | Sibling of the same legacy wave: the EFS hand-over read, which uses the same view and stamp pattern |
| RWB-P1-E2010-APP | App development | Sibling of the same service: the stage 2 data products, which read the same account view live and copy nothing |
| The rwb-integration, rwb-treatment, rwb-case and rwb-decision slices of RWB-E2-007 | App development | The match, the outcome, the task, the decision entry and the event; this story serves them and builds none of it |
| RWB-ITG-E2007-ITG | Integration | I: the cross-service proof of the legacy key against the live owners |

### 19. Out of scope

- The booking confirmation itself: the run of JOB-08, the facts it builds around the approved treatment, the call to the rule evaluator and the skip of a treatment already handled — the rwb-integration slice of RWB-E2-007 (Architecture v5 slide 44; legacy §4).
- Package BOOKING_MATCH, its rows, its tolerance, its version states and the rule evaluator: rwb-decision (P7), DP-04, and RWB-P2-E2007-CON on the caller's side.
- The outcome `BOOKED`, `NO_BOOKING` or `TERMS_DIFFER`, the difference on the treatment, the booked-at value and the treatment state: rwb-treatment (S2), and the recovery plans and the credit approval record on the case are rwb-case's.
- The tasks `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` and `UNMATCHED_EXCEPTION`, their owner roles, their messages MSG-P2-011 and MSG-P2-012 and the one-open-task rule: rwb-case (P3) and the rwb-integration slice.
- The decision log entry, `inputs_ref` and the inputs snapshot: rwb-decision (P7); this story only supplies the freshness the entry records (DP-03).
- `TreatmentBooked` (EV-11), `CaseStateChanged` (EV-05) and every other event: rwb-payment and rwb-case; this story publishes nothing (DP-09).
- The REC-03 result, the run summary and the break list of the match: the slice that runs the match; `reconciliation_result` stays this service's own table (RWB-P1-E1011-APP) and this story writes no row of it.
- The case list, which rwb-case serves; rwb-source-data holds none (RD-P1-024).
- The Section B views themselves, their migration and their dictionary rows: RWB-ACE-001 and RWB-P1-E1069-APP; this story reads what they append and answers per field until they do.
- The freshness stamp, its stale flag and its Schedules: RWB-P1-E1015-APP.
- The treatment record screen SCR-14, the case record data panel SCR-03, the gateway-bff composite route and the screen field lists: rwb-treatment, rwb-case and the platform edge story (DP-19).
- The real cross-service proof of the two reads against the live caller: RWB-ITG-E2007-ITG.

### 20. Remaining delivery steps

- Size the story (DOR-RWB-P1-E2007-APP-16): delivery lead.
- Sign off the epic design: solution architect.
- Publish rwb-source-data.yaml 5.1.0 with `/booking-facts` and `/batch-status` and mark the contract Done: API contract owner.
- Publish the provider fake and confirm the rwb-case fake version: contract story owner (GAP-3516).
- Name the authorise operation and roles: security architect (GAP-3513).
- Load the synthetic view and batch-status fixtures in DEV: data engineer.
- Add the `checksum` assertion to TC-P1-E2007-APP-01 and the rwb-payment identity to TC-P1-E2007-APP-13, and carry the story-level IDs into the traceability matrix: test lead.
