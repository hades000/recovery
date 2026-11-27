# RWB-P1-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 22 November 2026.
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
| Contract dependencies | RWB-P2-E2007-CON |
| Contract version | v1 (base path /api/recovery/source-data/v1); contract baseline RWB-P2-E2007-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to REQ-CHO-008) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-007 for rwb-source-data. The two in-process reads the booking match took from the monolith — `AccountQuery.forCase(caseId, businessDate)` over `recovery.v_ace_account` and `BatchStatusQuery.forSource(sourceSystem, businessDate)` over `recovery.v_ace_batch_status` — become two REST operations of this service on base `/api/recovery/source-data/v1` (DP-11, DP-13): `GET /booking-facts` and `GET /batch-status`, with one response entity each and the per-field answer that the three Section B columns need while they do not exist (DP-01, DP-05; TSD P1 T3.10 point 1). The ACE facts stay read-only through this service's own views and are never copied (DP-05; Architecture v5 slides 11 and 29), the DP01 freshness element reuses the record of RWB-P1-E1015-APP so the caller's decision log entry can name the data it used, and the comparison, the outcome, the treatment state, the task, the decision entry and the event stay with the other slices of this legacy key: the BOOKING_MATCH package is rwb-decision's (DP-04), the outcome and the treatment state are rwb-treatment's, the task is rwb-case's, the decision entry is rwb-decision's and `TreatmentBooked` (EV-11) is rwb-payment's. This story evaluates no rule, marks no treatment booked, records no difference, raises no task, publishes no event and writes no row, so its build dependency list is empty and it builds against the published baseline, the view contract and the fake of RWB-P2-E2007-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 44 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)** whose approved settlement or restructure is confirmed from the next ALS batch, I want **the facts that the BOOKING_MATCH evaluation reads — one fact per account of the case with its TDR and settlement terms and its `data_as_of`, and the ALS batch status for the business date — to be two read operations of rwb-source-data, with a per-field "not available" answer before the Section B columns exist and no fact at all for a business date whose ALS batch is not COMPLETE**, so that **every booking confirmation is decided on facts read from one owned place, dated, and only for a day whose batch landed**.

This is the application slice of legacy RWB-E2-007 that serves the match. It owns exactly two things:

- **the booking-facts read** on base `/api/recovery/source-data/v1`: `GET /booking-facts?caseId=&businessDate=` returns, per account of the case, `account_key`, `product_group`, `tdr_flag`, `last_tdr_date`, `principal_outstanding`, `interest_rate`, `settlement_booked_date`, `settlement_booked_amount` and `data_as_of`, read from `v_ace_account` for the ALS business date, with the DP01 business date, status and load time beside them so the caller can record the data it used (DP01, LOADED or STALE);
- **the batch-status read**: `GET /batch-status?sourceSystem=&businessDate=` returns `status`, `is_complete`, `completed_at`, `started_at`, `record_count` and `feed_version` from `v_ace_batch_status` — the gate the match runs behind, so no fact is read for a business date whose ALS batch is not COMPLETE.

It also carries the Section B availability rule of the legacy key: `principal_outstanding`, `settlement_booked_date` and `settlement_booked_amount` are three of the ALS columns that RWB-ACE-001 adds to ACE `account`, and they reach `v_ace_account` only with the Section B view migration (TSD P1 T3.10 point 1; DL43; FSD P1 AC-EXC-P1-001-06). Before that migration the read answers "not available" per field, the story stays behind its flag, and no booking can be confirmed from a missing field.

It does **not** decide anything. The BOOKING_MATCH package and its rows are rwb-decision's (DP-04; D-RCV-36); the evaluation, the outcome `BOOKED` / `NO_BOOKING` / `TERMS_DIFFER`, the difference and the treatment state are rwb-treatment's (S2); the task `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` or `UNMATCHED_EXCEPTION` is rwb-case's (P3); the decision log entry is rwb-decision's (P7); and `TreatmentBooked` (EV-11) on `rwb.payment.events.v1` is rwb-payment's. This story compares no term, marks no treatment booked, records no difference, raises no task, publishes no event and writes no row. Those criteria sit with the rwb-integration, rwb-treatment, rwb-case, rwb-decision and exception slices of this legacy key and with the cross-service proof of RWB-ITG-E2007-ITG.

### 2. Business rationale

The officer books a restructure or a settlement in ALS by hand (INT-03), and nothing checks today that the booked terms equal the approved terms: 44 percent of TDR cases deviate (R-RES-10). ACE ingests the ALS batch and the booked terms appear on the account, so a comparison over ACE is the only check that needs no file the Workbench has to load (D-RCV-35 U1; DL12). Every approved treatment is confirmed as booked, or raised as missing or differing, by the next batch; the measure is REC-03, approved treatments against bookings, zero after two days. Serves REQ-CHO-008.

The comparison itself is not this story's, and that is the point of the split. In the monolith the match, the facts and the rule evaluation were one service over one schema. In the target the facts come from the service that owns the ACE read path (DP-05; Architecture v5 slides 15 and 29, "only rwb-source-data reads the 30 `recovery.v_ace_*` views"), the package comes from the service that governs rules (DP-04; Temporal and Drools design slide 15, governance central in rwb-decision), the outcome is a treatment fact (S2), the escalation is case work (P3) and the proof is a decision record (P7). The two reads of this story are the seam: everything the match decides is decided on what they answer, and nothing they answer is a decision.

Two properties of that seam are worth naming. The first is **the gate**. BR8 of the legacy key says no missing booking is raised for a business date whose ALS batch is not COMPLETE, and the only place that can enforce it without a race is the read: if the fact is not answered for such a date, no caller can compare against a half-loaded day (BR-P1-014-4; FSD P1 A2.14; AC-EXC-P1-011-01). The second is **the honest blank**. Three of the compared terms arrive only with the Section B columns, so before RWB-ACE-001 lands the read must say so per field rather than return a zero amount or a default date; a booking confirmed from an absent term would be the one failure this story can prevent on its own (TSD P1 T3.10 point 1; DL43; AC-EXC-P1-001-06).

### 3. Preconditions

- The baseline of rwb-source-data is in place: schema `rwb_source_data`, the login `rwb_source_data`, the data dictionary and the data products of P1 (delivered by RWB-P1-E1001-APP), and the per-service sequence of the platform (RWB-PLT-E1044-CON) with its own history table. This story adds no version to that sequence.
- The 16 Section A views and the 14 Section B views exist in schema `recovery`, the login `rwb_source_data` holds SELECT on the 30 `recovery.v_ace_*` views and no privilege outside its own schema, and `v_ace_account` and `v_ace_batch_status` are among them (DP-02, DP-05; RWB-P1-E1069-APP; Architecture v5 slides 11 and 29). The views are the published baseline of this service and not a build dependency of this story.
- RWB-P1-E1015-APP is done: `data_product_load` is written for every product and business date a COMPLETE ALS batch feeds, so the DP01 freshness element of the answer has a row to read, and the stale flag is set by the cut-off when the batch is late (DP-01; TSD P1 T3.7).
- RWB-P1-E1002-APP is done: `case_list_row` carries one row per case account and business date, with `case_id`, `account_key`, `product_group` and `business_date` (DF-RPT-002, DF-RPT-003, DF-RPT-005, DF-RPT-007; TSD P1 T3.1).
- RWB-P2-E2007-CON is published with its fakes: the shapes `BookingFact`, `BookingFactsAnswer`, `FieldState` and `BatchStatusAnswer`, the error envelope and the fixture rows. The shapes are those of section 12.1 and the contract story of the booking-confirmation slice publishes them, the freshness element being the `DataProductFreshness` record of RWB-P1-E1015-CON (GAP-0594), and this story builds against that contract and never against a second draft of it.
- For the three Section B fields only: RWB-ACE-001 is deployed and the Section B view migration has appended the 12 Tier 2 columns to the three views it re-creates (`account`, `customer` and `efs_action`), so `principal_outstanding`, `settlement_booked_date` and `settlement_booked_amount` exist in `v_ace_account` (TSD P1 T3.10 point 1; FSD P1 AC-ALT-P1-001-02; DL43). Until then the read stays behind its flag `rwb.dataengine.booking-facts`, which stays off until the Section B view migration is applied, and answers per field: `NOT_AVAILABLE` with no value, never a zero amount and never a default date.
- The caller is the booking-confirmation slice of this legacy key (RWB-P2-E2007-APP, service rwb-integration), whose event-started workflow JOB-08 Architecture v5 slide 44 lists under rwb-payment; that owner row is superseded for this job, and the slice holds a workload identity token (Architecture v5 slides 11 and 41). A case role reads the same facts only through the screens that call this contract (DP-19).
- The 2 s budget, the breaker per downstream and the 5 s statement timeout on the views are configuration of the platform (DP-11; Architecture v5 slide 11).
- No approval is needed to build against a Draft contract baseline: the contract is tagged by RWB-P2-E2007-CON when its tests pass, and this story is in Draft status until then (D-RCV-60).

### 4. Flow

1. The booking-confirmation slice calls `GET /api/recovery/source-data/v1/booking-facts?caseId=&businessDate=` with its workload identity, once per business date and case (DP-11, DP-13).
2. `BookingFactsController` validates the two parameters and refuses a malformed case reference or business date with 400 and MSG-GEN-001 (12.1).
3. `BatchStatusGate` reads `recovery.v_ace_batch_status` for source `ALS` and the requested business date; a row that is absent, `RUNNING`, `FAILED` or `is_complete` false ends the call with 409 and MSG-P1-001 and no fact is read (AC2, AC3; BR8).
4. `CaseAccountReader` reads `case_list_row` in `rwb_source_data` for the case and the business date and takes the account keys and the product group of the case (DP-01; DF-RPT-003, DF-RPT-005, DF-RPT-007). The case list row is the accepted source of the case account set, so the story reads no `case_account` of `rwb_case` and needs no contract of rwb-case (GAP-0595).
5. `BookingFactRepository` reads `recovery.v_ace_account` for those account keys, SELECT only, with the 5 s statement timeout, and never a second statement against `public` (DP-05; BR-P1-001-2).
6. `BookingFactsAssembler` builds one `BookingFact` per account with the nine values of section 11; `FieldAvailability` marks `principal_outstanding`, `settlement_booked_date` and `settlement_booked_amount` as `AVAILABLE` with their value, or `NOT_AVAILABLE` with no value when the Section B migration has not appended the column — never a zero amount and never a default date (AC1, AC5).
7. `FreshnessReader` reads the DP01 stamp from `data_product_load` in `rwb_source_data` and attaches the freshness element, so the caller's decision log entry can record the product, the business date, the status and the load time it used (AC1; TSD P1 T3.7 "Display").
8. The call answers 200 with the freshness element and the facts in account-key order; a case with no case-list row for the business date answers an empty fact list and the freshness element, so no account is invented (X4).
9. The call writes nothing, publishes nothing and records nothing: no outbox row, no decision record, no treatment write, no task (AC4, AC6; BR5).
10. The caller builds BookingMatchFacts from its own treatment contract (the approved terms and the treatment type) and these account facts, and calls the rule evaluator; that step, its outcome and its consequences are the other slices of this legacy key (DP-04; §19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ALS batch for the business date is absent, `RUNNING`, `FAILED` or not `is_complete` | 409; no fact is read for any account; no booking can be confirmed for that date | MSG-P1-001 | AC3 |
| X2 | `v_ace_account` or `v_ace_batch_status` does not answer, or the 5 s statement timeout fires | 503; the answer carries no fact and no partial page | MSG-GEN-006 | AC7, AC10 |
| X3 | A Section B column is absent from `v_ace_account` | 200; the three fields answer `NOT_AVAILABLE` with no value; the story stays behind its flag | None | AC5 |
| X4 | The case has no case-list row for the business date | 200 with an empty fact list and the freshness element; no account key is invented | None | AC1 (empty case), Section 12.1 |
| X5 | The same read is made twice | The second answer carries the same values; nothing is written | None | AC4 |
| X6 | A malformed case reference or business date | 400; nothing is read | MSG-GEN-001 | AC8, AC11 |
| X7 | A caller without the read right, or without a session | 403 with MSG-P4-002, or 401 with MSG-P4-001, at the edge of this service | MSG-P4-002, MSG-P4-001 | AC9, AC12 |

X1 and X3 are the two exception paths this slice owns: the legacy X4 (a batch that is not COMPLETE) carried onto the read, and the Section B absence the legacy key states in its preconditions. X2, X4, X5, X6 and X7 are the ordinary paths of a read contract. The legacy exception paths X1, X2, X3, X5, X6, X7, X8 and X9 — the missing booking, the differing term, the partly booked case, the second run, the repeated missing booking, the failed decision log write, the rerun right and the absent package version — belong to the slices that raise the task, mark the booking and write the decision entry, and are not restated here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds from Day 1 against the published baseline, the 30 views and the fake of RWB-P2-E2007-CON; needs no live rwb-payment, rwb-treatment, rwb-case or rwb-decision, and no H dependency |
| Negotiable | The internal class split, the ordering of the facts, the statement timeout and the shape of the availability marker are the squad's choice behind the contract; the nine values, the gate and the per-field answer are fixed |
| Valuable | One read of the ACE facts and one read of the batch status for the whole booking-confirmation slice, dated, gated and honest about a field the view does not hold |
| Estimable | Two controllers, two repositories, one gate, one assembler, one availability map and one freshness reader |
| Small | Fits one sprint with its tests, as the read slice of the legacy key |
| Testable | Every criterion in section 7 is one call against a view fixture and the contract fake, plus one boundary assertion on the SQL |

### 7. Acceptance criteria

```gherkin
Feature: The facts of the booking confirmation, read from the ALS batch

  Background:
    Given synthetic case "RW-2026-000701" holds accounts "A-0701", "A-0702" and "A-0703"
    Given the case list rows of case "RW-2026-000701" for business date 2026-12-16 name the three accounts with product group "MORTGAGE"
    Given package "BOOKING_MATCH" version "BKG-2026.12" is in force for the slice of this legacy key that calls these reads

  Scenario: AC1 The booking facts of the case's accounts (new, D-RCV-60)
    Given v_ace_account at business date 2026-12-16 shows for "A-0701" tdr_flag true, last TDR date 2026-12-16, principal outstanding 650,000.00 baht, interest rate 4.2500, settlement booked date 2026-12-16, settlement booked amount 650,000.00 baht and data_as_of 2026-12-16
    Given v_ace_account at business date 2026-12-16 shows for "A-0702" tdr_flag false and for "A-0703" tdr_flag true, last TDR date 2026-12-16, principal outstanding 1,800,000.00 baht and interest rate 4.5000
    When a caller reads GET /booking-facts?caseId=RW-2026-000701&businessDate=2026-12-16
    Then the answer holds one fact per account, each with account_key, product_group, tdr_flag, last_tdr_date, principal_outstanding, interest_rate, settlement_booked_date, settlement_booked_amount and data_as_of
    Then the fact for "A-0701" carries settlement_booked_date 2026-12-16 and settlement_booked_amount 650,000.00 baht
    Then the fact for "A-0703" carries interest_rate 4.5000 as ACE holds it
    Then the answer carries the DP01 business date 2026-12-16, status "LOADED" and load time 2026-12-17T05:40+07:00
    Then the answer carries no outcome, no compared term, no difference and no package version

  Scenario: AC2 The batch status the match runs behind (new, D-RCV-60)
    Given the ALS batch for business date 2026-12-16 is COMPLETED, started 2026-12-16T23:30+07:00, completed 2026-12-17T05:40+07:00, with record count 184,500 and feed version "ALS-2026.12"
    Given the ALS batch for business date 2026-12-17 ended "FAILED" at 2026-12-18T05:20+07:00
    When a caller reads GET /batch-status?sourceSystem=ALS&businessDate=2026-12-16
    Then the answer holds status "COMPLETED", is_complete true, completed_at 2026-12-17T05:40+07:00 and record_count 184,500
    Then the answer holds started_at 2026-12-16T23:30+07:00 and feed_version "ALS-2026.12"
    When a caller reads GET /batch-status?sourceSystem=ALS&businessDate=2026-12-17
    Then the answer holds status "FAILED" and is_complete false

  Scenario: AC3 A business date whose ALS batch is not complete (new, D-RCV-60)
    Given the ALS batch for business date 2026-12-17 ended "FAILED" at 2026-12-18T05:20+07:00
    When a caller reads GET /booking-facts?caseId=RW-2026-000701&businessDate=2026-12-17
    Then the system refuses the call with status 409 and MSG-P1-001
    Then the answer holds no booking fact for any account
    Then no booking is confirmed for the business date 2026-12-17

  Scenario: AC4 The same read twice (new, D-RCV-60)
    Given the booking facts of case "RW-2026-000701" at 2026-12-16 have been read once
    When the same read is made again
    Then the answer carries the same nine values for every account and the same data_as_of
    Then the answer carries the same DP01 business date, status and load time
    Then no row of v_ace_account, v_ace_batch_status, case_list_row or data_product_load is written

  Scenario: AC5 A Section B field the view does not hold (new, D-RCV-60)
    Given the Section B view migration is not applied, so v_ace_account carries no principal_outstanding, no settlement_booked_date and no settlement_booked_amount column
    Given the two reads are enabled on the pre-V0003 fixture for this test only, while flag "rwb.dataengine.booking-facts" stays off in that deployment
    When the booking facts of case "RW-2026-000701" are read for 2026-12-16 on the pre-V0003 view
    Then principal_outstanding, settlement_booked_date and settlement_booked_amount each answer "NOT_AVAILABLE" and carry no value
    Then the fact carries account_key, product_group, tdr_flag, last_tdr_date, interest_rate and data_as_of as the view holds them
    Then the fact carries no zero amount and no default date for the three fields
    Then no booking is confirmed from a missing term

  Scenario: AC6 The answer is facts and nothing else (new, D-RCV-60)
    Given the answer of GET /booking-facts?caseId=RW-2026-000701&businessDate=2026-12-16
    When the answer and the SQL of the call are inspected
    Then the answer carries no treatment state, no booking outcome, no difference, no task and no decision-log entry
    Then the answer carries no package version and no tolerance
    Then the call names only recovery.v_ace_account, recovery.v_ace_batch_status, case_list_row and data_product_load
    Then the call writes no row and publishes no message

  Scenario: AC7 A view that does not answer (new, D-RCV-60)
    Given the statement timeout of 5 s fires on recovery.v_ace_account for case RW-2026-000701 at business date 2026-12-16
    When a caller reads GET /booking-facts?caseId=RW-2026-000701&businessDate=2026-12-16
    Then the system refuses the call with status 503 and MSG-GEN-006
    Then the answer carries no fact and no partial page

  Scenario: AC8 A malformed case reference or business date (new, D-RCV-60)
    When a caller reads GET /booking-facts?caseId=RW-2026-000701&businessDate=not-a-date
    Then the system refuses the call with status 400 and MSG-GEN-001
    Then no view is read for the call

  Scenario: AC9 A caller without a session or without the read right (new, D-RCV-60)
    Given a caller holds no session
    When the caller reads GET /booking-facts?caseId=RW-2026-000701&businessDate=2026-12-16
    Then the system refuses the call with status 401 and MSG-P4-001
    Given a signed-in caller whose identity does not include the read right
    When the caller reads GET /booking-facts?caseId=RW-2026-000701&businessDate=2026-12-16
    Then the system refuses the call with status 403 and MSG-P4-002
    Then no view is read for the call

  Scenario: AC10 A batch-status view that does not answer (new, D-RCV-60)
    Given the statement timeout of 5 s fires on recovery.v_ace_batch_status for source ALS at business date 2026-12-16
    When a caller reads GET /batch-status?sourceSystem=ALS&businessDate=2026-12-16
    Then the system refuses the call with status 503 and MSG-GEN-006
    Then the answer carries no batch status and no partial page
    Then no fact is read for any account

  Scenario: AC11 A malformed case reference (new, D-RCV-60)
    When a caller reads GET /booking-facts?caseId=<malformed case reference>&businessDate=2026-12-16
    Then the system refuses the call with status 400 and MSG-GEN-001
    Then no view is read for the call

  Scenario: AC12 A caller without a session or without the read right on the batch-status read (new, D-RCV-60)
    Given a caller holds no session
    When the caller reads GET /batch-status?sourceSystem=ALS&businessDate=2026-12-16
    Then the system refuses the call with status 401 and MSG-P4-001
    Given a signed-in caller whose identity does not include the read right
    When the caller reads GET /batch-status?sourceSystem=ALS&businessDate=2026-12-16
    Then the system refuses the call with status 403 and MSG-P4-002
    Then no view is read for the call

  Scenario: AC13 The error answers of the provided operations carry their status codes (new, D-RCV-60)
    Given recovery.v_ace_batch_status holds no row for source ALS at business date 2026-12-16
    When a caller reads GET /batch-status?sourceSystem=ALS&businessDate=2026-12-16
    Then the system answers with status 404 and MSG-P1-001
    Then the 401 and 403 answers of AC9 and AC12 carry MSG-P4-001 and MSG-P4-002 as stated there
```

**Target reading.** The thirteen criteria above are new, and each of them tests only the deliverable of this story; the legacy criteria that AC1 to AC6 come from are shown here so that the reader can follow the split, while AC7 to AC13 come from the exceptions of section 5 and the error answers of section 12.1. `AccountQuery.forCase(caseId, businessDate)` of legacy §12 is `GET /booking-facts` on base `/api/recovery/source-data/v1`, and `BatchStatusQuery.forSource(sourceSystem, businessDate)` is `GET /batch-status` on the same base (DP-11, DP-13); the shapes are the published ones of RWB-P2-E2007-CON (C), because no source document names them (GAP-0594; ASM-0836). The two views are read in-process in this service under the `rwb_source_data` login, SELECT only, with the 5 s statement timeout (DP-02, DP-05; Architecture v5 slides 11 and 29), and no value is copied into a table of this service. The account set and the product group of AC1 are not read from `v_ace_account`: the link from a case to its accounts is rwb-case's `case_account` in the target, and the Work Package lists no C dependency on rwb-case, so the read takes them from this service's own daily projection `case_list_row` for the case and business date (DF-RPT-002, DF-RPT-003, DF-RPT-005, DF-RPT-007; GAP-0595; ASM-0837). The DP01 freshness element of AC1 carries the same four values as the `DataProductFreshness` record of RWB-P1-E1015-CON, so no second freshness shape is defined: the product, the business date, the status `LOADED` or `STALE` and the load time, which is `v_ace_batch_status.completed_at` (FSD P1 A2.14.2; TSD P1 T3.7). The three Section B values of AC1 and AC5 come with the Section B view migration of RWB-ACE-001, which appends the 12 Tier 2 columns to `v_ace_account` (TSD P1 T3.10 point 1; FSD P1 AC-ALT-P1-001-02), and AC5 states what the read answers before it: `NOT_AVAILABLE` per field, no value, no zero and no default (GAP-0596; ASM-0838). AC2 and AC3 are the legacy AC5 carried onto the read: the batch row is answered as it is (`COMPLETED`, `FAILED` or `RUNNING`, with `is_complete`), and the facts are refused for any date whose row is not COMPLETE, so no missing booking can be raised for it (BR8; BR-P1-014-4; TSD P1 T3.7; GAP-0597; ASM-0839). AC4 is the legacy AC6 seen from the read: the same call answers the same facts and writes nothing, so a repeated run of the caller cannot produce a second fact. AC6 is the boundary the split rests on: the legacy `BookingMatchFacts` carried the treatment terms and the outcome was the rule answer, while the read carries account facts only, and the package, the outcome, the difference, the task, the decision entry and the event belong to rwb-decision, rwb-treatment, rwb-case and rwb-payment (DP-04; GAP-0598; ASM-0840). Legacy AC1, AC2, AC3, AC4, AC7, AC8 and AC9 are owned by those other slices and by RWB-ITG-E2007-ITG, and this story claims none of them.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A booking is made by the officer in ALS and confirmed only from the next ACE batch; the Workbench never reads ALS and never times its own load | INT-03; DL12; D-RCV-35 U1 |
| BR2 | No fact is read for a business date whose ALS batch is not COMPLETE, and no missing booking is raised for such a date | BR8 of RWB-E2-007; BR-P1-014-4; FSD P1 A2.14; CTL-02 |
| BR3 | The terms read are the account facts ACE holds: `tdr_flag`, `last_tdr_date`, `principal_outstanding`, `interest_rate`, `settlement_booked_date` and `settlement_booked_amount`, each with `data_as_of` | DF-ACE-030, DF-ACE-031, DF-ACE-025, DF-ACC-009, DF-ACC-030, DF-ACC-031, DF-ACE-036; legacy BR2, BR3 |
| BR4 | A fact carries the account key, the product group of the case and the six account facts, and nothing a decision needs to be compared with | DF-RPT-005, DF-RPT-007; legacy BR10 |
| BR5 | The comparison, the tolerance and the outcome are rows of package BOOKING_MATCH evaluated through the rule evaluator; this read holds no comparison code, no rule table and no tolerance | D-RCV-36 T3, T5; ADR-012; legacy BR10 |
| BR6 | A Section B field that the view does not hold answers not available; no zero amount, no default date and no inferred value is substituted | TSD P1 T3.10 point 1; FSD P1 AC-EXC-P1-001-06; DL43 |
| BR7 | Freshness is read from `v_ace_batch_status` only, and every read of source data shows the business date and the status of its product | BR-P1-014-2; TSD P1 T3.7 "Display"; legacy BR9 |
| BR8 | No value a business person may change is written in code: the source system is a request parameter, the product group is a row of the case list, and the status values are those ACE writes | BR-P1-001, BR-P1-002; DP-07 |
| BR9 | The answer carries no personal data: the account key is the business key, never the account number, and no customer field is read | legacy §17; FSD P1 BR-P1-001-6 |

**Where each rule lives in the target.** BR1 and BR2 are answerable inside this service: the facts are read from the views of a business date whose ALS row is COMPLETE, and the refusal is the read's own 409 and not the caller's check (AC2, AC3). BR3 and BR4 are the projection of the answer: six account columns of `recovery.v_ace_account`, `data_as_of` beside them, and the account key and product group of the case from this service's `case_list_row`. BR5 is a prohibition, and it is the reason the answer carries no outcome: the row that decides, its version and the tolerance stay in the package in rwb-decision, and the evaluator that runs it belongs to the calling slice (DP-04; D-RCV-36). BR6 is the availability map of the three Section B fields; the columns themselves and the view that appends them are RWB-ACE-001's and RWB-P1-E1069-APP's, and this story only refuses to invent a value for them (AC5). BR7 is the freshness element of the answer, read from this service's own stamp and not from `data_as_of`, which is the view's own date and can differ (FSD P1 BR-P1-014-2). BR8 and BR9 are answered by the shape of the request and the answer: no coded value is a constant, and the only customer-adjacent value returned is an account key.

### 9. State transitions

None in the case model: this story changes no case status, no treatment state and no booking outcome. It does not even move a freshness status; it reads the stamp that RWB-P1-E1015-APP writes.

| From | Event | Condition | To |
|---|---|---|---|
| no answer for the case and business date | a booking-facts call | The ALS row for the date is COMPLETE | An answer with one fact per case-list account and the DP01 freshness element |
| no answer for the case and business date | a booking-facts call | The ALS row is absent, `RUNNING`, `FAILED` or not complete | A refusal with 409 and MSG-P1-001; nothing is read |
| an answer with the three Section B fields available | the same call | The Section B view migration is applied | The same answer, the three fields carrying their values |
| an answer with the three Section B fields not available | the same call | The Section B view migration is not applied | The same answer, the three fields marked `NOT_AVAILABLE` with no value |
| any answer | a second identical call | The views and the stamp are unchanged | The identical answer; nothing is written |
| a batch row `COMPLETED` | the cut-off of DP01 | The batch for the expected date does not complete | The stamp turns `STALE` through RWB-P1-E1015-APP; this read reports it and changes nothing |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-source-data service identity (`rwb_source_data` login) | Reads the two views and its own two tables; writes nothing, and holds no privilege outside `rwb_source_data` and the 30 views |
| The booking-confirmation slice of this legacy key, as a workload identity (JOB-08, rwb-payment per Architecture v5 slide 44) | Calls the two reads; builds its own facts; evaluates the package; takes every consequence |
| RW-RESTRUCT, restructuring officer | Reads the facts through the treatment record screen of rwb-treatment and the case record data panel, which call this contract through gateway-bff |
| RW-CREDITAD, Credit Administration officer | Reads the facts on the differing-terms task of the rwb-case slice |
| RW-DATASTEW, data steward | Reads the DP01 stamp and the batch status; owns the freshness rows the element reports |
| RW-PLATADM, platform administrator | Operates the deployment and the flag; reads the metrics and the traces of the two operations |
| rwb-decision (P7) | Owns the BOOKING_MATCH package, its rows and versions, and the decision log entry the caller writes |
| rwb-treatment (S2) | Owns the outcome, the difference and the treatment state; this read returns none of them |
| rwb-case (P3) | Owns the case, its accounts and the tasks the caller raises; this read takes the account set from its own case list row and never from P3 |
| rwb-payment (P8) | Owns the workflow that runs JOB-08 and the event `TreatmentBooked` |

The read runs as the service identity of rwb-source-data (DP-02; Architecture v5 slides 11 and 29), and the caller's identity travels in the workload token so that a refusal is made for the caller and not for the service. No delegation limit and no approval level applies: this story takes no decision. The edge check that refuses a caller without the read right is the rwb-access authorise check of DP-08; its operation name is Not specified in the source documents (DOR-RWB-P1-E2007-APP-6).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-RPT-002 | case_list_row | business_date | Read |
| DF-RPT-003 | case_list_row | case_id | Read |
| DF-RPT-005 | case_list_row | account_key | Read |
| DF-RPT-007 | case_list_row | product_group | Read |
| DF-ACE-001 | v_ace_account | account_key | Read |
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
| DF-ACE-185 | v_ace_batch_status | feed_version | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-OPS-002 | data_product_load | product_code | Read |
| DF-OPS-004 | data_product_load | business_date | Read |
| DF-OPS-006 | data_product_load | loaded_at | Read |
| DF-OPS-007 | data_product_load | status | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. The three Section B fields keep their frozen field-gap IDs until the LDM assigns `DF-ACE` IDs to the 12 added columns (legacy §11 note; TSD P1 T3.10 point 1). Decision DL43 is still open (assumptions ASM-0193, ASM-0737, ASM-0748 and ASM-0816), and decision DL12 is still open (assumptions ASM-0189, ASM-2559 and ASM-2608).

**Which side is this story's.** Every row above is a read, and this story owns no write: it creates no table, adds no column and no index, and inserts nothing. The four `case_list_row` columns and the six account facts are the content of the answer; `data_as_of` travels with each fact and says how old the ACE row is, while the freshness element says how old the product is, and the two are different facts (FSD P1 BR-P1-014-2). `data_product_load` is this service's own stamp, written by RWB-P1-E1015-APP and read here; `case_list_row` is this service's own daily projection, built by RWB-P1-E1002-APP and read here (DP-01; the Ownership Map ruling on `case_list_row`). Nothing of `case_account`, `treatment`, `task` or `decision_log_entry` is read, and no foreign key crosses a schema.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13). The two reads the booking-confirmation slice calls, with their shapes declared by RWB-P2-E2007-CON (C).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/booking-facts` | The booking facts of one case for one ALS business date, with the DP01 freshness element | A workload identity of the booking-confirmation slice with the booking-facts right, or a Workbench role with the same right through gateway-bff | Idempotent by case and business date |
| GET | `/batch-status` | The batch row of one source and business date — the gate the facts are read behind | As above | Idempotent by source and business date |

**Query.** `/booking-facts`: `caseId` (required, the case reference), `businessDate` (required, the ALS business date). `/batch-status`: `sourceSystem` (required, the ACE source code as `v_ace_batch_status` holds it), `businessDate` (required).

**Response entities.** `BookingFactsAnswer` carries `freshness` — the `DataProductFreshness` record of RWB-P1-E1015-CON with `productCode` DP01, `businessDate`, `status` (`LOADED` or `STALE`) and `loadedAt` — and `facts`, a list of `BookingFact` with `accountKey`, `productGroup`, `tdrFlag`, `lastTdrDate`, `principalOutstanding`, `interestRate`, `settlementBookedDate`, `settlementBookedAmount`, `dataAsOf` and `fieldState`, where `fieldState` names each of the three Section B fields as `AVAILABLE` or `NOT_AVAILABLE` and a field that is not available carries no value. `BatchStatusAnswer` carries `sourceSystem`, `businessDate`, `status`, `isComplete`, `startedAt`, `completedAt`, `recordCount` and `feedVersion`. The `/batch-status` answer is the gate read of the match, and the freshness reads of RWB-P1-E1015-APP remain the product reads; a source and date with no batch row answers 404 with MSG-P1-001 (GAP-0597).

**Errors.** 400 with MSG-GEN-001 for a malformed case reference or business date; 401 with MSG-P4-001 without a session; 403 with MSG-P4-002 without the right; 404 with MSG-P1-001 from `/batch-status` for a source and business date with no batch row; 409 with MSG-P1-001 from `/booking-facts` for a business date whose row is absent, `RUNNING`, `FAILED` or not complete — the same answer the job rerun gives for a date that is not complete (TSD P1 API-P1-002); 503 with MSG-GEN-006 when a view does not answer inside the 5 s statement timeout. The property names of the two entities are those of section 11, the shape of `fieldState` and the 404 of `/batch-status` are as stated above, and RWB-P2-E2007-CON publishes them with both operations added to the next API Specification version (GAP-0594; GAP-0597).

#### 12.2 REST operations consumed

None. The read calls no other service at run time: the ACE facts are read in this service's own views (DP-01, DP-05), the account set and the product group are read from this service's own case list row, and the freshness element from its own stamp. RWB-P2-E2007-CON is a build-time contract dependency and its fake, not a run-time call. A call to the rwb-case case contract for the accounts of the case would be one more hop and a C dependency the Work Package does not list, and the assumption of GAP-0595 avoids it (ASM-0837).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slide 43, rows 26 and 27). This story publishes no event and writes no outbox row. `TreatmentBooked` (EV-11) on `rwb.payment.events.v1` is rwb-payment's, published by the slice that marks the booking.

#### 12.4 Events consumed

None. The read is called over REST by the booking-confirmation slice, which is itself started by `rwb.source-data.AceDataReady.v1`; the consumption of that event and the workflow that runs JOB-08 are that slice's and not this story's (Architecture v5 slides 43 and 44). The writes of the match — the treatment state, the difference, the task, the decision entry and the event — are not this story's either: this read writes nothing at all.

#### 12.5 Workflows and activities

None. Both reads are synchronous REST steps and neither writes a row. JOB-08 Booking confirmation is an event-started workflow in rwb-payment (Architecture v5 slide 44) and the Temporal activities `listEligibleAccounts` and `snapshot(page)` and the workflows `AceIngestCheck` and `reconciliation` of Architecture v5 slide 15 are other P1 stories; the task queue of this service is `rwb-source-data` in namespace `rwb-recovery`, and this story starts no workflow and no activity on it.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: the caller is started by `AceDataReady` and this story answers when called.

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `v_ace_account` | `recovery` | View owner `ace_view_owner`; contract owner P1 rwb-source-data (Ownership Map: a data product of ACE read through the views; RWB-P1-E1069-APP) | None new: read only, SELECT through the `rwb_source_data` login, 5 s statement timeout; the three Section B columns only after the Section B view migration |
| `v_ace_batch_status` | `recovery` | View owner `ace_view_owner`; contract owner P1 rwb-source-data (Ownership Map: the freshness of every product; RWB-P1-E1015-APP) | None new: read only; the gate |
| `case_list_row` | `rwb_source_data` | P1 rwb-source-data (Ownership Map ruling on the daily published projection; RWB-P1-E1002-APP) | None new: read for the account set and the product group |
| `data_product_load` | `rwb_source_data` | P1 rwb-source-data (Ownership Map: the freshness stamp; RWB-P1-E1015-APP writes it) | None new: read for the DP01 freshness element |

No table of another service is read and no foreign key crosses a schema (DP-01). `case_account` stays in `rwb_case` with P3, `treatment` in `rwb_treatment` with S2, `task` in `rwb_case` with P3 and `decision_log_entry` in `rwb_decision` with P7; this read names none of them in SQL (AC6).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P2-E2007-CON fake | The two operations | A completed, a failed and a running batch row; three accounts of one case; a pre-V0003 view without the three Section B columns; an empty fact list; a view error and a timeout |
| `recovery.v_ace_account` fixture | The view | `A-0701` with the settlement booked on 2026-12-16 at 650,000.00 baht, `A-0702` with `tdr_flag` false, `A-0703` with rate 4.5000, each with `data_as_of` 2026-12-16, and a pre-V0003 copy without the three Section B columns |
| `recovery.v_ace_batch_status` fixture | The view | ALS `COMPLETED` for 2026-12-16 (started 2026-12-16T23:30+07:00, completed 2026-12-17T05:40+07:00, record count 184,500, feed version ALS-2026.12), ALS `FAILED` for 2026-12-17 at 2026-12-18T05:20+07:00, a `RUNNING` row and no row for 2026-12-19 |
| `case_list_row` fixture | `rwb_source_data` | The three rows of case RW-2026-000701 for 2026-12-16 with product group MORTGAGE, and a case with no row for the date |
| `data_product_load` fixture | `rwb_source_data` | The DP01 stamp for 2026-12-16 with status LOADED and load time 2026-12-17T05:40+07:00, the same product STALE for a late date, and no row for a date with no batch |

The pattern table of section 13 also names the H rows RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON, and the C rows RWB-P7-E1073-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON plus the treatment and task contracts. This story calls none of them (12.2), so it needs no fake for them: they do not change its metadata rows, and it builds from Day 1 against the published contract and the fakes and fixtures above. Their entry in the dependency map is decided there and is not a precondition of this build.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/source-data/v1` | None | OpenAPI 3.1 (DP-13); the shapes are published by RWB-P2-E2007-CON |
| Kafka | None | None | `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP; `TreatmentBooked` is rwb-payment's |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file is read or written |
| SQL view | None | `recovery.v_ace_account` and `recovery.v_ace_batch_status`, with `case_list_row` and `data_product_load` in `rwb_source_data` | SELECT only, 5 s statement timeout, one login `rwb_source_data` (DP-02, DP-05) |

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

- **DP-01** is applied as the boundary of the answer: the two views stay in schema `recovery`, the projection and the stamp stay in `rwb_source_data`, and the case, its accounts, the treatment, the task and the decision entry stay with their owners and are never named in SQL.
- **DP-03** is a statement here and not a dependency of this story: a decision record is written by the caller through the local decision-record library, and this read only supplies the freshness the entry needs so that `inputs_ref` can state the product, the business date, the status and the load time (RWB-PLT-E1027-CON is the caller's dependency; the H list of this story is empty).
- **DP-04** is a prohibition here: the BOOKING_MATCH package is loaded, approved and versioned in rwb-decision and evaluated by the calling slice inside its own activity; this read holds no rule, no package code, no tolerance and no evaluator (D-RCV-36; RWB-PLT-E1072-CON and RWB-P7-E1073-CON are the caller's dependencies).
- **DP-05** is the read path of this story: `v_ace_account` and `v_ace_batch_status` are read in-process through the `rwb_source_data` login, SELECT only, with the 5 s statement timeout, and the same facts reach every other service through this contract and never through a second copy (ADR-010).
- **DP-06** is a statement here: no parameter is read on this path, and the parameter that governs the grace before a missing booking is raised (`booking.missing.grace_loads`) is read by the calling slice through the rwb-case parameters contract (RWB-PLT-E1042-CON and RWB-P3-E1042-CON are its dependencies, not this story's).
- **DP-07** is a statement here: no list is read and no value is validated against a list; the product group is a value of `case_list_row` and the status values are those ACE writes, both returned as they are (RWB-PLT-E1043-CON and RWB-P3-E1043-CON are the caller's dependencies).
- **DP-09** is a prohibition here: nothing is published and no outbox or inbox row is written, because a read produces no fact others may react to.
- **DP-10** is a statement here: JOB-08 is an event-started workflow in rwb-payment (Architecture v5 slide 44) and this story owns no Schedule and no workflow; the caller's workflow kit is its dependency.
- **DP-11** is how the two reads replace the two in-process calls: each is a REST contract with a fake, one hop from the caller, a 2 s budget and a breaker per downstream.
- **DP-13** is the base: every path of this story sits under `/api/recovery/source-data/v1`, and no monolith path is served.
- **DP-19** is a statement here: the treatment record screen and the case record data panel reach these facts through the gateway-bff composite route (RWB-PLT-N001-CON is the edge's dependency), and this story builds no screen and no route.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `BookingFactsController` | Controller | The two operations of 12.1 on `/api/recovery/source-data/v1`; RFC 9457 problem details; the error set |
| `BatchStatusGate` | Service | The COMPLETE rule over `v_ace_batch_status` and the 409 with MSG-P1-001 for any other row |
| `CaseAccountReader` | Repository | Reads `case_list_row` for the case and business date: the account keys and the product group |
| `BookingFactRepository` | Repository | Reads `recovery.v_ace_account` by account key, SELECT only, with the 5 s statement timeout; no write method exists |
| `FieldAvailability` | Service | Marks the three Section B fields `AVAILABLE` or `NOT_AVAILABLE` from the applied view version and the flag, and never substitutes a value |
| `FreshnessReader` | Repository | Reads the DP01 row of `data_product_load` and builds the `DataProductFreshness` element |
| `BookingFact`, `BookingFactsAnswer`, `BatchStatusAnswer` | Entities | The published shapes of 12.1, immutable |
| `BookingFactsBoundaryTest` | Test | Fails the build on any statement outside `rwb_source_data` and `recovery`, on any write method on the two repositories, and on any outcome-shaped field in the answer (treatment term, outcome, difference, tolerance or package version) |

**Migrations.** None. This story creates no table, no column and no index and adds no Flyway version: everything it reads is either a view of `recovery` (created by RWB-P1-E1069-APP's two migrations) or a table of `rwb_source_data` delivered by RWB-P1-E1001-APP, RWB-P1-E1002-APP and RWB-P1-E1015-APP. The three Section B columns arrive with the Section B view migration of RWB-ACE-001, on the same sequence and under the object owner `ace_view_owner` (TSD P1 T3.10 point 1; DL43).

**Configuration and reference data**

- The flag `rwb.dataengine.booking-facts` gates the two reads. It stays off until the deployment carries the views of RWB-P1-E1069-APP, and the three Section B fields answer `NOT_AVAILABLE` whenever the Section B migration is not applied (ASM-0838); the booking-confirmation flag of the calling slice stays off for the same reason.
- The source system is a request parameter and never a constant in code: `ALS` is the caller's value, as `v_ace_batch_status` holds it (BR8).
- The 5 s statement timeout on the views and the 2 s budget with the breaker on the caller's side are platform configuration (DP-11; Architecture v5 slide 11).
- The freshness values are data rows of `data_product_load` and of `data_product`, never constants in the code (DP-07).

**Build steps**

1. `BookingFactsController` and the two operations with the RFC 9457 body and the error set of 12.1 (X6, X7).
2. `BatchStatusGate` over `recovery.v_ace_batch_status`: `COMPLETED` and `is_complete` pass, anything else refuses with 409 and MSG-P1-001 for the facts read and answers a row for the batch-status read (AC2, AC3).
3. `CaseAccountReader` over `case_list_row` for the case and business date, with the empty-list path of X4 (AC1; ASM-0837).
4. `BookingFactRepository` over `recovery.v_ace_account`, keyed by account key, with the 5 s statement timeout and no write method (AC1).
5. `FieldAvailability` for the three Section B fields, with a pre-V0003 fixture that proves no zero and no default date (AC5).
6. `FreshnessReader` for the DP01 stamp and the `DataProductFreshness` element (AC1, AC4).
7. The refusal and failure paths: the view error and the timeout as 503 with MSG-GEN-006 and no partial page (X2).
8. `BookingFactsBoundaryTest`: only `rwb_source_data` and `recovery` are named, and neither repository has a write method (AC4, AC6).
9. Tests for AC1 to AC6 against the fake of RWB-P2-E2007-CON and the view fixtures, plus the regression rows of section 16 where the fixture of the owning slice is available.

**Done when.** The tests in section 16 pass; the two reads answer from the view fixtures with the nine values and the freshness element; a `FAILED` batch yields 409 with MSG-P1-001 and no fact; the pre-V0003 fixture answers `NOT_AVAILABLE` for the three fields and no booking can be read from them; a repeated call answers the identical facts and writes nothing; and the boundary test shows that the call names only `rwb_source_data` and `recovery`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ALS batch for the business date is absent, late, failed or not complete; also the batch-status read for a date with no row | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | A malformed case reference or business date | Enter {field}. |
| MSG-GEN-006 | A view does not answer, or the statement timeout fires | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-001 | No session on the read | Sign in to continue. |
| MSG-P4-002 | An identity without the read right | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10 (still open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863). MSG-P1-001 is the text of FSD P1 v3, which names the ACE batch rather than a load and ACE rather than ALS; the wording change is carried by FSD P1 open point OQ-P1-07 and needs to reach the Error and Message Standard, and the older text of legacy RWB-E2-007 §14 ("Today's load has not arrived.") is not used here. MSG-GEN-001 fills the field name and never a data value; MSG-GEN-006 names the system ("ACE database") and no case fact; MSG-P4-002 is raised by the edge identity check and not by this service.

### 15. Screens and states

No screen in this story. The facts are shown on the treatment record SCR-14 of rwb-treatment, where the officer sees the booked terms or the difference, and in the data panel of the case record SCR-03; both screens reach this contract through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), and their field lists belong to the screen owners. The SCR-03 states are loading (per Screen Specifications v1 SCR-03); empty, error and no access are Not specified in the source documents (CG-ALL-2380), apart from the refusal message stated below. The SCR-14 states are empty, loading, error and no access, all Not specified in the source documents (CG-ALL-2381), apart from the refusal message stated next. When the read refuses, the screen shows MSG-P1-001 in the Error state of the panel and offers no booking confirmation for that date; when the Section B migration is not applied, the three terms show as not available and the screen offers no booking confirmation from them. This story renders none of it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-10 | Access — regression evidence: the access path of the job rerun belongs to the rwb-integration slice of this legacy key | Contract | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun for JOB-08; refused with MSG-P4-002 |
| TC-E2-007-01 | AC1, BR1, BR3, BR7, BR10 — regression evidence: legacy AC1 is owned by the rwb-treatment and rwb-decision slices and by the cross-service proof; this story proves the facts they decide on | Component | Synthetic settlement booked 2026-12-16 at 650,000.00 baht |
| TC-E2-007-02 | AC2, BR5 — regression evidence: legacy AC2 is owned by the rwb-integration and rwb-case slices that raise the missing-booking task | Component | Restructure with tdr_flag false in v_ace_account |
| TC-E2-007-03 | AC3, BR2, BR4, BR6 — regression evidence: legacy AC3 is owned by the rwb-decision slice, which evaluates the row against the rate | Component | Rate 4.5000 booked against 4.2500 approved |
| TC-E2-007-04 | AC4, BR2 — regression evidence: legacy AC4 is owned by the rwb-treatment and rwb-case slices that hold the partly booked case | Component | Two accounts, one booked |
| TC-E2-007-05 | AC5, BR8 — this story's own evidence, run as its AC2 and AC3: the gate is the read's; the JOB-08 behaviour of legacy AC5 is the rwb-integration slice's and the cross-service proof is RWB-ITG-E2007-ITG | Component | ACE batch failed for 2026-12-17 |
| TC-E2-007-06 | AC6 — this story's own evidence, run as its AC4: the read is the repeated step; the second booking, event and task of legacy AC6 belong to the slices that write them | Component | JOB-08 rerun for 2026-12-16 |
| TC-E2-007-07 | Legacy AC7, BR5 — regression evidence, run by the owning rwb-case slice; story key Not specified in the source documents (CG-ALL-2377); not this story's AC7 | Component | Booking missing on two batches |
| TC-E2-007-08 | Legacy AC8, BR9 — regression evidence, run by the owning rwb-decision slice; story key Not specified in the source documents (CG-ALL-2377); not this story's AC8 | Component | Decision log store stopped |
| TC-E2-007-09 | Legacy AC9, BR11 — regression evidence, run by the owning rwb-decision and rwb-integration slices; story key Not specified in the source documents (CG-ALL-2377); not this story's AC9 | Component | No BOOKING_MATCH version in force on 2026-12-17 |
| TC-E2-007-11 | Principle 5 — regression evidence: legacy Principle 5 is proved on `markBooked` by the rwb-treatment and rwb-decision slices | NFR | Decision log write forced to fail on markBooked; treatment stays APPROVED, no event |
| TC-E2-007-12 | Contract — the two operations of section 12, GET /booking-facts and GET /batch-status, with their request, response and envelope against the fakes of RWB-P2-E2007-CON | Contract | Contract fake of RWB-P2-E2007-CON; the requests of AC1 and AC2 |
| TC-E2-007-13 | Boundary — the tables of section 12.7 are read only: no write, no insert, no update and no delete on any object of section 12.7 | Component | Login rwb_source_data; attempted write on v_ace_account, v_ace_batch_status, case_list_row and data_product_load |
| TC-E2-007-14 | AC7 — this story's own evidence: the 503 of a view that does not answer | Component | Statement timeout of 5 s fires on v_ace_account |
| TC-E2-007-15 | AC8 — this story's own evidence: the 400 of a malformed case reference or business date | Component | businessDate=not-a-date |
| TC-E2-007-16 | AC9 — this story's own evidence: the 401 without a session and the 403 without the read right | Component | Caller without a session; caller without the read right |
| TC-E2-007-17 | AC10 — this story's own evidence: the 503 of a batch-status view that does not answer | Component | Statement timeout of 5 s fires on v_ace_batch_status |
| TC-E2-007-18 | AC11 — this story's own evidence: the 400 of a malformed case reference | Component | Malformed caseId; the value is Not specified in the source documents (NEWAC-RWB-P1-E2007-APP-AC11) |
| TC-E2-007-19 | AC12 — this story's own evidence: the 401 without a session and the 403 without the read right on GET /batch-status | Component | Caller without a session; caller without the read right, on sourceSystem ALS |
| TC-E2-007-20 | AC13 — this story's own evidence: the 404 of GET /batch-status for a source and business date with no batch row | Component | No row in v_ace_batch_status for source ALS at 2026-12-16 |

The eleven legacy test case IDs and their Data are kept in the given order and character for character, their Covers are kept except TC-E2-007-07 to TC-E2-007-09, which are restated as regression evidence (CG-ALL-2377), with the level of each row added; the legacy level "System" maps to "Component", "Access" to "Contract" and "Resilience" to "NFR" (GAP-2490). TC-E2-007-05 and TC-E2-007-06 are the two legacy rows this story runs as its own evidence, because the gate and the repeated read are what it ships; TC-E2-007-12 to TC-E2-007-20 are the rows this story adds for its contract, its boundary and its criteria AC7 to AC13; the other nine rows are kept as regression evidence for the slices of this legacy key that own their criteria, and all eleven run again in RWB-ITG-E2007-ITG against the live contracts. The full test of TC-E2-007-01 to TC-E2-007-10, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; TC-E2-007-11 to TC-E2-007-20 are to be added to that tab in its next version.

### 17. Guardrails

- No business value in code: the source system is a request parameter, the status values are those ACE writes, the product group is a value of `case_list_row` and the freshness values are rows of `data_product_load` and `data_product` (DP-07).
- No personal data in the answer, the logs, the tests or the fixture: the read returns an account key and money and date facts, never an account number, a name or a contact point (legacy §17); the fixture is synthetic.
- No read of another service's table: `case_account`, `treatment`, `task` and `decision_log_entry` are named nowhere in SQL and no foreign key crosses a schema (DP-01; AC6).
- ACE data only through the owner's views, and only this service reads them (DP-05; ADR-010); the read holds SELECT and no privilege outside `rwb_source_data` and the 30 views.
- No rule, no comparison and no threshold in this service: the package, the tolerance and the outcome stay in rwb-decision and in the calling slice (DP-04; BR5).
- No write of any kind: no row, no outbox message, no decision record, no task and no event, so a repeated call cannot duplicate a fact (AC4, AC6).
- The read is one hop for the caller, 2 s budget with a breaker, and 5 s statement timeout on the views (DP-11).
- An applied migration is never edited, and this story adds no version at all: the three Section B columns come with the Section B view migration of RWB-ACE-001, on the sequence of this service and under the object owner (TSD P1 T3.10 point 1).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next day's ALS load | Business Requirements Program, section 5.3; Business Requirements Epic 2, section 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39 (evaluated by the calling slice, not here) | TC-E2-007-01 to TC-E2-007-09, TC-E2-007-11 to TC-E2-007-20 |

The requirement is met by the legacy key as a whole: this story supplies the facts and the gate that the confirmation is decided on, and the comparison, the outcome, the state change, the task, the decision entry and the event are the work of the other slices of RWB-E2-007 and of RWB-ITG-E2007-ITG.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P2-E2007-CON | Contract | C build dependency: the contract story of the booking-confirmation slice declares the shapes of the two reads, their envelope and their fakes |
| RWB-P1-E1069-APP | App development | Sibling of the same service, a precondition and not an H dependency: the 30 `recovery.v_ace_*` views, their grants and the boundary rule this read runs under |
| RWB-P1-E1015-APP | App development | Sibling of the same service, a precondition: the DP01 stamp and the `DataProductFreshness` record the answer reuses |
| RWB-P1-E1002-APP | App development | Sibling of the same service, a precondition: `case_list_row`, the account set and the product group of the case |
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
- The report row and the case list publication that carry `case_list_row`: RWB-P1-E1002-APP and RWB-P1-E1011-APP.
- The Section B views themselves, their migration and their dictionary rows: RWB-ACE-001 and RWB-P1-E1069-APP; this story reads what they append and answers per field until they do.
- The freshness stamp, its stale flag and its Schedules: RWB-P1-E1015-APP.
- The treatment record screen SCR-14, the case record data panel SCR-03, the gateway-bff composite route and the screen field lists: rwb-treatment, rwb-case and the platform edge story (DP-19).
- The real cross-service proof of the two reads against the live caller: RWB-ITG-E2007-ITG.
