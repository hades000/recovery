# RWB-S2-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the S2 rwb-treatment slice of legacy RWB-E2-007 is split out of the integration match. The match, the JOB-08 run, the awarded rows of package `BOOKING_MATCH`, the task texts and the REC-03 result stay with rwb-integration (P2) in `RWB-P2-E2007-APP` and its contract `RWB-P2-E2007-CON`; the ACE account and batch-status read stays with rwb-source-data (P1) and the package registry with rwb-decision (P7). This story delivers the treatment-side consequence of a confirmed or differing booking only: the approved-not-booked read, the mark-booked write that stamps `booked_at` (DF-TRT-012) and moves the treatment to `BOOKED`, the difference write into `booking_difference` (DF-TRT-028), the embedded Drools evaluation of `BOOKING_MATCH` inside `TreatmentWorkflow` on queue `rwb-treatment` (DP-04, DP-10), the local decision record written in the same `rwb_treatment` transaction (DP-03), the base `/api/recovery/treatment/v1` (DP-13) and SCR-14 through the gateway-bff composite route (DP-19). The eleven legacy test case IDs are kept in order. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E2007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-S2-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2007-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to REQ-CHO-008) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (RW-RESTRUCT) and a Credit Administration officer (RW-CREDITAD)** working the restructure and settlement routes of the case, I want **the treatment-side half of the booking confirmation — the read that lists the approved restructures and settlements not yet booked for a business date, the write that stamps `booked_at` and moves the treatment to `BOOKED` with its own decision record in one `rwb_treatment` transaction, and the write that holds the approved-against-booked difference on the treatment when a term differs**, so that **every approved decision is confirmed as booked on the record that carries it, without a person comparing ALS printouts, and without another service writing this service's state and this service's decision**.

This is the secondary slice of legacy RWB-E2-007. The legacy story owns the comparison itself — package `BOOKING_MATCH`, its RESTRUCTURE and SETTLEMENT rows, the tolerance, the outcomes, JOB-08, the task codes and the REC-03 break list — and every one of its nine acceptance criteria is owned by `RWB-P2-E2007-APP`, by `RWB-P3-E2007-APP` for the case move and the tasks, or by `RWB-P4-E2007-APP` for the rerun refusal. This story owns no legacy criterion and restates none of their values: it copies the identifiers, amounts, dates and messages of the legacy story character for character and tests only the treatment-side consequence.

What this story owns:

- the approved-not-booked read for a set of treatment types and a business date, which the JOB-08 run of `RWB-P2-E2007-APP` consumes (DP-11; shape declared by `RWB-P2-E2007-CON`);
- the mark-booked write and the booking-difference write of the treatment resource, the only two writes of this key on `treatment` (DP-11);
- the evaluation of the `BOOKING_MATCH` version in force with the embedded Drools runtime, inside an activity of `TreatmentWorkflow` (DP-04);
- the columns `booked_at` (DF-TRT-012), `booking_difference` (DF-TRT-028) and the standard `state` on the `treatment` row of `rwb_treatment`, with this story's per-service Flyway version for their rule (DP-01, DP-15 as the service's own sequence);
- the local decision record of the confirmation, written through the RWB-PLT-E1027-CON library in the same transaction as the state change (DP-03);
- `TreatmentWorkflow`, the stage child of `CaseWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, and the inbound dedupe of the package-announcement event (DP-09, DP-10);
- the parameters read `booking.missing.grace_loads` and the reference-data read of the treatment types and outcome codes (DP-06, DP-07);
- the treatment read on base `/api/recovery/treatment/v1` and SCR-14 through the gateway-bff composite route (DP-13, DP-19).

It does not own: the match, the row order of the package, the built facts, JOB-08 and its rerun operation, the run summary and the REC-03 result (`RWB-P2-E2007-APP`); the ACE account and batch-status read through `recovery.v_ace_*` (`RWB-P1-E2007-APP`); the package rows, their load, their approval and the version in force (`RWB-P7-E2007-APP` behind `RWB-P3-E2042-CON`); the case route state, its move by R-RES-22 or R-SET-13, the task rows and the case-side decision record (`RWB-P3-E2007-APP`); `TreatmentBooked` (EV-11), which rwb-payment publishes for a confirmation and which no story of this key builds (section 19); the rights and the scope data (`RWB-P4-E2007-APP`).

### 2. Business rationale

The officer books restructures and settlements by hand in ALS (INT-03) and nothing checks that the booked terms equal the approved terms (legacy section 2; REQ-CHO-008). The legacy story closed that gap by comparing each approved treatment with the account as ACE holds it after the next ALS batch and measuring the result as REC-03. Nothing in that value changes here; what changes is which service owns which half of the write.

The treatment is this service's record: `treatment_type`, `offer_amount`, `interest_rate`, `booked_at` and `booking_difference` are columns of `treatment` in `rwb_treatment` (TSD S2 T3.1), and the state APPROVED to BOOKED is a state of the treatment, not of the case. Architecture v5 gives every service one transaction of its own in which it writes its state change, its decision record and its outbox row together (slide 11), and R-UNI-39 forbids a change without its record. A confirmation therefore cannot be a single write made by the integration job: the service that holds the treatment must make the change, record the decision and stamp the version under which it moved.

Three consequences are designed rather than left to discipline.

- **The rule set stays data, the state change stays here.** The compared terms, the tolerance and the outcome are rows of the `BOOKING_MATCH` package version in force, read at evaluation time (DP-04; legacy BR10; D-RCV-36 T3, T5). This module holds no threshold, no term list and no comparison code; the row that fires names itself and its version on this service's own record.
- **Two services, two records, one answer.** rwb-integration decides the match for the run and records its own decision (its `RWB-P2-E2007-APP`); this service re-evaluates the same package for the treatment it is about to move, so no caller can move a treatment without a record held beside it (DP-03, DP-04). Both stamp the version in force, and an earlier answer keeps its own version (R-UNI-38).
- **No ACE view and no second read.** The account facts and the batch answer arrive on the caller's request, which carries them from the rwb-source-data contract; this module reads no `v_ace_*` view and holds no grant on one (DP-05; ADR-010). No data lake exists in the target (DP-17) and nothing here builds, sends or reads a lake file.

It serves REQ-CHO-008 on the treatment side and carries R-UNI-39 (nothing moves without its record) and R-UNI-41 (no package in force is a refusal, never a default match). No business value is invented or moved: the amounts, the rates, the dates, the treatment identifiers, the package version and the message texts are the ones the legacy story already carries.

### 3. Preconditions

- `RWB-P2-E2007-CON` is published: the booking-confirmation contract baseline of this key, with the approved-not-booked read, the mark-booked write, the booking-difference write, the outcome codes `BOOKED`, `NO_BOOKING` and `TERMS_DIFFER`, the booking-reference rule and the fakes for rwb-treatment (DP-11). The operation names and the payload element names are Not specified in the source documents (GAP-2691; ASM-4444). This story builds against the contract and its fake on Day 1.
- The `rwb_treatment` schema and login exist from the platform database story, and this service's Flyway sequence is at the version that carries the library tables; this story adds the booking columns and their rule on the same sequence and never edits an applied migration (DP-01; GAP-2691; ASM-4443).
- `treatment` exists in `rwb_treatment` with the columns of TSD S2 T3.1 (DF-TRT-001 to DF-TRT-033) and the standard record columns of T3.0, including `state`, `booked_at` and `booking_difference`, written by `RWB-S2-E3001-APP` and its siblings.
- Package `BOOKING_MATCH` version `BKG-2026.12` is in force for the business date, with a RESTRUCTURE row comparing `tdr_flag`, `last_tdr_date` and `principal_outstanding` against `offer_amount` and `interest_rate` against the approved rate, a SETTLEMENT row comparing `settlement_booked_date` and `settlement_booked_amount` against `offer_amount`, and tolerance 0.00 baht (DL25). The rows are loaded, approved and promoted by `RWB-E2-042` and `RWB-P7-E2007-APP`; this story evaluates them and holds no copy of them.
- The version in force is announced on `rwb.decision.RulePackageInForce.v1` (EV-30), which this service consumes through its own inbox (DP-09).
- The parameters read of rwb-case carries `booking.missing.grace_loads` = 1, and the reference-data read carries LOV-TREATMENT with `RESTRUCTURE` and `SETTLEMENT` and the outcome codes; no member of either list is written in code (DP-06, DP-07; GAP-2691; ASM-4447).
- The workflow kit is in place on task queue `rwb-treatment` in namespace `rwb-recovery`, `CaseWorkflow` of rwb-case starts this stage as a child on that queue, and the parent moves the case state from the stage outcome this service reports (DP-10).
- The local decision-record library `RWB-PLT-E1027-CON` is published with `DecisionRecordWriter.record`, refusing with MSG-P7-009 and failing with MSG-P7-003 (DP-03).
- No approval is needed to build against a Draft contract baseline and a contract dependency never blocks: this story starts on Day 1 with `RWB-P2-E2007-CON` as its only contract dependency (§R5.7 of the Template and Rules; ASM-4444; ASM-4450).

### 4. Flow

1. rwb-source-data publishes the ALS batch-ready event for business date D and the JOB-08 run of `RWB-P2-E2007-APP` starts on queue `rwb-integration` (its own story; this service neither reads the batch nor starts the run).
2. The run asks this service for the approved RESTRUCTURE and SETTLEMENT treatments not yet booked for D through the approved-not-booked read of `RWB-P2-E2007-CON`; the treatment types come from the reference-data LOV rows in force and the grace count from `booking.missing.grace_loads` (DP-06, DP-07).
3. The run builds the facts, evaluates the package and calls the mark-booked write of this story with the treatment ID, the business date and the booking reference (`account_key` + business date) when the outcome for every account is `BOOKED`; it calls the booking-difference write with the differing terms when the outcome is `TERMS_DIFFER`; it calls neither write when the outcome is `NO_BOOKING`.
4. The API handler hands the write to `TreatmentWorkflow` on queue `rwb-treatment` as a signal to the running stage child, or starts the child when the stage is not running, under the workflow ID rule of the kit (DP-10).
5. `evaluateBookingMatch` activity reads the treatment row of the request from `rwb_treatment`, checks that it is `APPROVED`, that its type matches the request and that its approval date is before the business date, and builds the facts: the treatment type, the approved terms (`offer_amount`, `interest_rate`), the account facts on the request and the business date.
6. The same activity asks the embedded Drools runtime for the `BOOKING_MATCH` version in force on D and evaluates it; the `RuleResult` names the row that fired, the package version, the outcome `BOOKED`, `NO_BOOKING` or `TERMS_DIFFER` and the differing terms. Drools is called only inside the activity, so a replay reuses the recorded answer (DP-04).
7. A missing version in force raises `NoPackageInForce` and is non-retryable; the write is refused with MSG-P3-027 and nothing changes (legacy BR11; R-UNI-41).
8. `recordAndApply` activity writes, in one `rwb_treatment` transaction: `booked_at` with the business date and the state `BOOKED` for a `BOOKED` answer, or `booking_difference` with the approved and booked value of each differing term for `TERMS_DIFFER`; the local decision record through `DecisionRecordWriter.record` with the row ID, the package version and the booking reference; the outbox row of the record publication; and the idempotency row of the treatment ID and business date (DP-03, DP-09).
9. The activity returns the stage outcome — the treatment ID, the state, `booked_at` or the difference, the row ID and the package version — to the parent `CaseWorkflow`, which moves the route state by R-RES-22 or R-SET-13 and raises the task when the outcome is `NO_BOOKING` or `TERMS_DIFFER`; this service writes no case, task or route row.
10. A repeated write for the same treatment and business date, or a redelivered event, finds the idempotency row and returns the recorded answer: no second state change, no second record and no second outbox row.
11. A `NO_BOOKING` answer writes nothing at all on the treatment, which stays `APPROVED`; the durable timer of the stage waits for the next ALS batch through the grace count read in step 2, and no Quartz job and no Schedule of this service is involved.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The treatment is not `APPROVED`, its type is not the request's, or it does not exist | The write is refused with 409 or 404, nothing changes and no record is written | MSG-P4-003 | AC2, AC7 |
| X2 | No `BOOKING_MATCH` version is in force on the business date | The step ends with `NoPackageInForce`, non-retryable; no column changes, no record and no outbox row is written | MSG-P3-027 | AC6 |
| X3 | The local decision record cannot be written | The transaction rolls back: no `booked_at`, no state change, no difference, no outbox row; the call is retried under the same key | MSG-P7-003 | AC5 |
| X4 | The same mark-booked write arrives twice for the same treatment and business date | The idempotency row drops the repeat and returns the recorded answer; one state change and one record exist | None | AC4 |
| X5 | The answer is `NO_BOOKING` | No column of the treatment changes; the treatment stays `APPROVED` and the task is the parent's | None | AC3 |
| X6 | The answer is `TERMS_DIFFER` | Only `booking_difference` is written; the state stays `APPROVED` and the task is the parent's | MSG-P2-012 | AC2 |
| X7 | The parameters read or the reference-data read does not answer inside 2 s, or its breaker is open | The step ends with MSG-GEN-006 and the kit retries: 1 s initial interval, back-off 2, 10 attempts; nothing is written | MSG-GEN-006 | AC7 |
| X8 | The identity has no Treatment and offer right on the treatment read | The read answers 403 with MSG-P4-002 and nothing changes | MSG-P4-002 | AC8 |
| X9 | A component, a statement or a test reaches a case, task, account or rule table, or an ACE view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | BR9 |

X1 to X4 are the legacy refusal, no-package, record-failure and repeat paths of RWB-E2-007 carried onto the two treatment writes; X5 and X6 are the legacy missing and differing outcomes seen from the treatment row; X7 to X9 are the paths the contract read and the schema boundary add. A refusal under X1, X2 or X7 writes nothing at all, because the evaluation and the reads run before the transaction opens.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-P2-E2007-CON` and its fake, the record-writer fake, the package fixture and the parameters and reference fakes; needs no live rwb-integration, rwb-case, rwb-decision or rwb-source-data |
| Negotiable | The activity names, the module shape, the write key and the flag name are this story's choice; the rows, the outcomes, the states, the list values, the messages and the package version are fixed |
| Valuable | Every approved restructure and settlement is confirmed as booked on its own record, and a differing term is held where the officer and Credit Administration already look |
| Estimable | One stage branch, two activities, two writes, one repository, one migration, one consumer with an inbox and one library adapter |
| Small | Fits two weeks with its tests, as a secondary slice of the legacy key |
| Testable | Each of the nine criteria of section 7 is one automated test; the caller and the package are stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Booking confirmation from the ALS load — the treatment-side write

  Background:
    Given package "BOOKING_MATCH" version "BKG-2026.12" is in force with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht
    Given case "RW-2026-000701" carries treatment "TRT-SYN-0701" of type SETTLEMENT with offer amount 650,000.00 baht, approved on 2026-12-15, in state APPROVED

  Scenario: AC1 A confirmed booking stamps booked_at and moves the treatment to BOOKED (new, D-RCV-60)
    Given the rwb-integration contract mock returns the mark-booked write for treatment "TRT-SYN-0701" with business date 2026-12-16 and booking reference "A-0701|2026-12-16"
    And the request carries, for synthetic account "A-0701", settlement booked date 2026-12-16 and settlement booked amount 650,000.00 baht as ACE holds them at 2026-12-16
    When TreatmentWorkflow consumes the write on queue "rwb-treatment"
    Then the SETTLEMENT row of package "BOOKING_MATCH" version "BKG-2026.12" is the row that fired
    Then treatment "TRT-SYN-0701" holds booked_at 2026-12-16 and state "BOOKED"
    Then one local decision record names the row, the package version "BKG-2026.12" and the booking reference, and it is written in the same transaction as the treatment row
    Then the stage outcome returned to the parent carries the treatment ID, the state "BOOKED" and the business date, and no case, task or route row is written by this service

  Scenario: AC2 Differing terms are held on the treatment and the state does not move (new, D-RCV-60)
    Given treatment "TRT-SYN-0703" of type RESTRUCTURE is approved with offer amount 1,800,000.00 baht and rate 4.2500 percent
    Given the rwb-integration contract mock returns the booking-difference write for "TRT-SYN-0703" with approved rate 4.2500 and booked rate 4.5000 for business date 2026-12-16
    When TreatmentWorkflow consumes the write
    Then the RESTRUCTURE row of package "BOOKING_MATCH" returns the outcome "TERMS_DIFFER" with approved rate 4.2500 and booked rate 4.5000
    Then booking_difference on treatment "TRT-SYN-0703" holds term "interest_rate", approved 4.2500 and booked 4.5000
    Then the treatment state stays "APPROVED", booked_at stays empty and one local decision record names row and package version
    Then the stage outcome carries the differing term, and the task "UNMATCHED_EXCEPTION" for role "RW-CREDITAD" with MSG-P2-012 is raised by the parent, not here

  Scenario: AC3 A missing booking writes nothing on the treatment (new, D-RCV-60)
    Given the rwb-integration contract mock makes no booking write for treatment "TRT-SYN-0702" of type RESTRUCTURE on business date 2026-12-16
    When the stage of case "RW-2026-000701" runs for the batch of 2026-12-16
    Then no column of treatment "TRT-SYN-0702" changes and it stays "APPROVED" with booked_at empty and no booking_difference
    Then no local decision record and no outbox row exists for that treatment and business date

  Scenario: AC4 A repeated write is deduped and returns the recorded answer (new, D-RCV-60)
    Given the mark-booked write of AC1 has been applied for "TRT-SYN-0701" and business date 2026-12-16
    When the same write is delivered again for the same treatment and business date
    Then one idempotency row exists for the treatment ID and business date and the second delivery returns the recorded answer
    Then treatment "TRT-SYN-0701" still holds one booked_at value and the state "BOOKED", and exactly one decision record and one outbox row exist for it

  Scenario: AC5 A failed record write rolls the whole step back (new, D-RCV-60)
    Given the decision-record writer mock reports the store unavailable with MSG-P7-003
    When the mark-booked write of AC1 is consumed
    Then no `booked_at`, no state change and no booking_difference is written and no outbox row exists
    Then the step ends with MSG-P7-003 and the treatment stays "APPROVED"

  Scenario: AC6 No package version in force is a refusal and nothing changes (new, D-RCV-60)
    Given the BOOKING_MATCH fixture reports that no version is in force on 2026-12-17
    When the mark-booked write for "TRT-SYN-0701" with business date 2026-12-17 is consumed
    Then the step ends with NoPackageInForce and MSG-P3-027 for package "BOOKING_MATCH" and business date 2026-12-17
    Then no column of the treatment changes, no record and no outbox row is written, and the refusal is not retried

  Scenario: AC7 The approved-not-booked read serves the run for a business date (new, D-RCV-60)
    Given the rwb-integration contract mock asks for the approved RESTRUCTURE and SETTLEMENT treatments not yet booked at business date 2026-12-16
    When the read is served on base "/api/recovery/treatment/v1"
    Then the answer lists "TRT-SYN-0701", "TRT-SYN-0702", "TRT-SYN-0703" and "TRT-SYN-0704" with their type, offer amount, approval date and state, and no treatment that is already booked
    Then the treatment types are the LOV-TREATMENT members in force read through the reference-data contract and the grace count is "booking.missing.grace_loads" in force, with no member and no count in code

  Scenario: AC8 The booked treatment and its difference show on SCR-14 through the composite route (new, D-RCV-60)
    Given treatment "TRT-SYN-0701" holds booked_at 2026-12-16 and state "BOOKED", and "TRT-SYN-0703" holds the booking difference with approved 4.2500 and booked 4.5000
    Given the gateway-bff composite route serves SCR-14 Treatment record from the case read of rwb-case and the treatment read of this service, one hop each
    When an officer holding Treatment and offer R opens SCR-14
    Then SCR-14 shows booked at 2026-12-16 for "TRT-SYN-0701" and, for "TRT-SYN-0703", each term with its approved and booked value
    Then a role without the right reads 403 with MSG-P4-002, the browser calls no owner service directly and the screen writes nothing

  Scenario: AC9 No personal data in the request, the record, the row or the logs (new, D-RCV-60)
    Given a request carries the treatment ID, the case ID, the account key "A-0701", the business date, the amounts, the rates and the package version
    When the treatment row, the local decision record and the log lines of the step are written
    Then they carry identifiers, codes, amounts and dates only, and no name, address, telephone number, national identity number, account number or account holder name
    Then no personal field of the case or the party is written to rwb_treatment by this story
```

The nine criteria are new under D-RCV-60 and test only the S2 deliverable: the booked state with `booked_at`, the difference on the treatment, the missing booking which writes nothing, the dedupe, the failed record, the no-package refusal, the read the run consumes, the SCR-14 answer and the no-PII rule. The legacy criteria AC1 to AC9 and the legacy test cases TC-E2-007-01 to TC-E2-007-11 belong to `RWB-P2-E2007-APP`, `RWB-P3-E2007-APP` and `RWB-P4-E2007-APP`, where the rows, the tolerance, the tasks, the batch gate, the rerun refusal and the REC-03 result are written with their origin tags; they are not restated here and no criterion claims them. Two readings are stated rather than hidden in the code: the treatment state value `BOOKED` is not a member of any list in the sources and is carried on the standard `state` column with a check constraint (GAP-2691; ASM-4443), and the difference is a jsonb object keyed by term with the approved and the booked value of each (GAP-2691; ASM-4446).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A booking is confirmed only from the next ACE batch for ALS, never from the officer's word and never from a file the Workbench loads | legacy BR1; INT-03; DL12; D-RCV-35 U1 |
| BR2 | A restructure is confirmed as booked when every account matches the RESTRUCTURE row in force: `tdr_flag` true, a last TDR date on or after the approval date, and the terms equal | legacy BR2; DF-ACE-031, DF-ACE-030; CTL-26; D-RCV-36 T5 |
| BR3 | A settlement is confirmed as booked when the account matches the SETTLEMENT row in force: a booked date on or after the approval date and a booked amount equal to the offer amount | legacy BR3; R-SET-13; D-RCV-36 T5 |
| BR4 | The tolerance on amounts and rates is the tolerance column of the row in force and is not a constant here | legacy BR4; DL25 |
| BR5 | A confirmed booking sets `booked_at` to the business date and moves the treatment state to `BOOKED`; a missing or a differing booking leaves the state `APPROVED` | legacy BR7 and section 9; R-RES-22, R-SET-13; ASM-4443 |
| BR6 | A differing term is written to `booking_difference` with its approved and booked value; the treatment state does not move | legacy BR6; REQ-CHO-008; ASM-4446 |
| BR7 | The package version in force decides and is stamped on the record; an earlier confirmation keeps its own version | legacy BR10; R-UNI-38; D-RCV-36 T3, T5, T7 |
| BR8 | A decision that cannot be recorded does not proceed: the state change, the record and the outbox row are one transaction | legacy BR9; Principle 5; R-UNI-39 |
| BR9 | No `BOOKING_MATCH` version in force is a refusal, never a default match, and it is not retried | legacy BR11; R-UNI-41 |
| BR10 | The treatment is this service's own record: this story writes no case, task, account or rule table and holds no cross-schema key or foreign key | DP-01; ownership of `treatment` only |

**Where each rule lives in the target.** BR1 is the read the run makes and the request the write arrives on; this service never calls ALS. BR2 and BR3 are the package rows, evaluated inside `evaluateBookingMatch`, so no compared term is a constant. BR4 is the tolerance column of the row. BR5 and BR6 are `recordAndApply` and its state guard. BR7 is the version read and the record columns. BR8 is the single transaction and the MSG-P7-003 rollback. BR9 is the `NoPackageInForce` path, non-retryable. BR10 is the schema boundary of sections 11 and 17.

### 9. State transitions

None of the route states in the legacy table is this story's: `WITH_OPS_BOOKING` to `BOOKED_IN_ALS_NLEADS` by R-RES-22 and `WITH_OPS_SETTLEMENT` to `AWAITING_PAYMENT` by R-SET-13 are the case states of rwb-case, moved by the parent `CaseWorkflow` from the stage outcome this service reports (`RWB-P3-E2007-APP`). The rows below are the states of this service's own `treatment` row.

| From (treatment state) | Event | Condition | To |
|---|---|---|---|
| APPROVED | BOOKING_CONFIRMED | The package row returns `BOOKED` for every account and the request matches the treatment | BOOKED, with `booked_at` the business date |
| APPROVED | BOOKING_MISSING | The package row returns `NO_BOOKING` | APPROVED, no column written |
| APPROVED | TERMS_DIFFER | The package row returns `TERMS_DIFFER` | APPROVED, with `booking_difference` written |
| BOOKED | BOOKING_CONFIRMED | A repeat of the same request for the same business date | BOOKED, unchanged (X4) |
| BOOKED, or APPROVED with a difference | Any later write for the same treatment and business date | The idempotency row exists | Unchanged, recorded answer returned |

The submit operation of the treatment resource is not reopened here: `POST /treatments/{treatmentId}/submit` belongs to the treatment and offer stories and this story only reads the state it guards. The stage execution itself is RUNNING, COMPLETED or FAILED in the workflow history, and a failed execution is retried on the platform policy of 1 s initial interval with back-off 2 and 10 attempts, with `NoPackageInForce` non-retryable.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-treatment service identity (login `rwb_treatment`) | Serves the read, applies the two writes, evaluates the package, writes `treatment`, the record and the outbox rows, and runs the stage step |
| rwb-integration (P2) | Owns the match, JOB-08, the run summary, the REC-03 result and the rerun operation; calls the read and the two writes of this story; never written by this story |
| rwb-source-data (P1) | Owns the ACE account and batch-status read; the facts arrive on the caller's request and no view is read here |
| rwb-decision (P7) | Owns the `BOOKING_MATCH` package, its rows, its versions and its approval, and announces the version in force |
| rwb-case (P3) | Owns the case route state, its move, the tasks, the assignment and the case-side decision record; the parent raises the tasks of MSG-P2-011 and MSG-P2-012 |
| rwb-payment (P8) | Publishes `TreatmentBooked` (EV-11) for a confirmed booking; not called and not written here |
| RW-RESTRUCT, restructuring officer | Reads the treatment, its booked date or its difference on the cases in scope (Treatment and offer CRUA); books in ALS, outside the Workbench |
| RW-CREDITAD, Credit Administration officer | Reads the differing terms on the cases in scope (Write-off and posting CRUA) |
| RW-DATASTEW, data steward | Reads the REC-03 break list, which rwb-integration writes and this story does not produce |
| RW-AUDIT, internal audit | Reads the record of a confirmation and the version it was taken under (R) |
| No delegation of authority level applies | The story confirms a booking another person made in ALS; it approves nothing and overrides no floor |

No credential and no personal name appears in the request, the row, the workflow input, the record or the logs. Where a person must be identified the row carries the user identifier, never a name, and the masking of the personal fields of the case is the platform edge's.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment (S2, `rwb_treatment`) | id | Read, as the treatment the write names |
| DF-TRT-002 | treatment (S2, `rwb_treatment`) | case_id | Read, as the case key of the stage outcome |
| DF-TRT-003 | treatment (S2, `rwb_treatment`) | decision_log_id | Write, the ID of the local decision record written with this change |
| DF-TRT-004 | treatment (S2, `rwb_treatment`) | treatment_type | Read, to match the request and to build the facts |
| DF-TRT-007 | treatment (S2, `rwb_treatment`) | offer_amount | Read, as the approved amount the booked amount is compared with |
| DF-TRT-012 | treatment (S2, `rwb_treatment`) | booked_at | Write, the business date of a confirmed booking |
| DF-TRT-027 | treatment (S2, `rwb_treatment`) | interest_rate | Read, as the approved rate compared with the booked rate |
| DF-TRT-028 | treatment (S2, `rwb_treatment`) | booking_difference | Write, the term keys with their approved and booked value |
| Standard column | treatment (S2, `rwb_treatment`) | state, version, created_at, created_by, updated_at, updated_by | Write `state` as section 9 defines it; the rest as TSD S2 T3.0 defines them |
| DF-CAS-026 | case_account (P3, `rwb_case`) | account_key | Not read: the account keys arrive on the request as the booking reference |
| DF-ACE-001, DF-ACE-025, DF-ACC-009, DF-ACE-030, DF-ACE-031, DF-ACE-036, DF-ACC-030, DF-ACC-031 | `v_ace_account` (P1 views) | account_key, interest_rate, principal_outstanding, last_tdr_date, tdr_flag, data_as_of, settlement_booked_date, settlement_booked_amount | Not read and no grant: they arrive on the request from the rwb-source-data contract (DP-05) |
| DF-ACE-178, DF-ACE-179, DF-ACE-182, DF-ACE-186 | `v_ace_batch_status` (P1 view) | source_system, business_date, status, is_complete | Not read: the batch gate is rwb-integration's and the business date arrives on the request |
| DF-REF-002, DF-REF-003 | rule_row (P7, `rwb_decision`) | rule_id, rule_version | Not read directly: the evaluated package returns the row ID and the version |
| DF-WRK-018, DF-WRK-019, DF-WRK-022, DF-WRK-023 | task (P3, `rwb_case`) | case_id, task_code, status, owner_role | Not written: the task codes `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` and `UNMATCHED_EXCEPTION` leave on the stage outcome (ASM-4448) |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result (P1/P2) | all fields (REC-03) | Not written: the run summary is rwb-integration's |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, `rwb_treatment`) | all fields, through `DecisionRecordWriter.record` | Write, in the same transaction (DP-03) |
| processed_event, outbox_event, idempotency_key | PLT library, created in `rwb_treatment` | the inbox row, the outbox row and the write key of the step | Write through the library, in the step's transaction (DP-09) |

`treatment` is the only table this story writes, and it writes three of its columns (`booked_at`, `booking_difference` and the standard `state`) with the standard record columns. The legacy read of the ACE views is not repeated here: `v_ace_account` and `v_ace_batch_status` are named in no statement of this module, the login holds no grant on `recovery`, and the account facts and the batch answer arrive on the request built from the rwb-source-data contract (DP-05; ADR-010). `recovery_case`, `task`, `case_account`, `rule_row` and the `reconciliation_result` table are reached only through their owners and are not read or written. Field identifiers are those of TSD S2 T3.1, TSD S2 T3.0 and the Logical Data Model and Data Dictionary.

**No new table.** This story's Flyway version adds the booking rule on `treatment` in `rwb_treatment`: the check that `booked_at` is set only in the `BOOKED` state, the check constraint of the state values of section 9, the uniqueness that one booking confirmation exists per treatment and business date, and the index the approved-not-booked read uses (GAP-2691; ASM-4443). The table itself arrives with `RWB-S2-E3001-APP`, and no applied migration is edited.

**No personal data.** The request, the row, the record and the logs carry the treatment ID, the case ID, the account key, the business date, the amounts, the rates, the row ID and the package version. No name, address, telephone number, national identity number, account number or account holder name is written, logged or put on a message; the booking reference is `account_key` + business date and never an account number (legacy guardrail).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13); the shapes are those `RWB-P2-E2007-CON` declares for its calls, and the operation names and payload element names are Not specified in the source documents (GAP-2691; ASM-4444).

| Method | Path | Request and response | Access | Idempotency |
|---|---|---|---|---|
| GET | `/treatments/{treatmentId}` | `Treatment` out, including `booked_at` (DF-TRT-012), `booking_difference` (DF-TRT-028), the state and the approved terms of DF-TRT-007 and DF-TRT-027 | Treatment and offer R, scope applied, through the guard library | Not applicable |
| GET | The approved-not-booked list of a treatment type set and a business date; name Not specified (GAP-2691; ASM-4444) | `BookingCandidateList` out: treatment ID, case ID, type, offer amount, interest rate, approval date and state | Treatment and offer R, service identity | Not applicable |
| POST | The mark-booked write: treatment ID, business date, booking reference, the account facts of the business date, the row ID and the package version; name Not specified (GAP-2691; ASM-4444) | `BookingConfirmation` out: the treatment ID, the state, `booked_at`, the row ID and the package version | Treatment and offer U, service identity | `Idempotency-Key` of the treatment ID and business date |
| POST | The booking-difference write: treatment ID, business date, the differing terms with their approved and booked value, the row ID and the package version; name Not specified (GAP-2691; ASM-4444) | `BookingDifference` out: the treatment ID, the state `APPROVED`, the difference terms, the row ID and the package version | Treatment and offer U, service identity | `Idempotency-Key` of the treatment ID and business date |

The errors are 401, 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-P2-006 for a step already running and for a treatment that is not `APPROVED`, 422 with MSG-P3-027 for a refused version check, and 503 with MSG-P7-003 or MSG-GEN-006, in the RFC 9457 problem body.

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use in this story |
|---|---|---|---|
| The parameters read of `booking.missing.grace_loads`; name Not specified (GAP-2691; ASM-4444) | `/api/recovery/case/v1` | P3 rwb-case (`RWB-P3-E1042-CON`) | The grace count the stage waits through, at its version, cached; no count in code (DP-06) |
| The reference-data read of LOV-TREATMENT and the outcome codes; name Not specified (GAP-2691; ASM-4444) | `/api/recovery/case/v1` | P3 rwb-case (`RWB-P3-E1043-CON`) | The list members `RESTRUCTURE` and `SETTLEMENT` and the outcome codes, at their version; no member in code (DP-07) |

Both are one hop with a 2 s timeout behind a breaker and neither calls another service. The H rows of DP-06 and DP-07 and the C rows they add stand in no build row of this story's plan (GAP-2692; ASM-4445).

#### 12.3 Events published

| Event | Topic | Trigger | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` (DP-03) | Every confirmation and every recorded difference, written by the record library in the step's transaction | `caseId` | The case ID, the treatment ID, the entity, the row ID, the package version and the outcome; no personal data |

This story adds no event type on `rwb.treatment.events.v1`: `TreatmentApproved` (EV-10) is published by the treatment and offer stories, and `TreatmentBooked` (EV-11) is published by rwb-payment for a confirmation, as the legacy story states. The record publication is the library's and the outbox row is written in the same `rwb_treatment` transaction as the treatment row (DP-09, DP-03).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | Announces the `BOOKING_MATCH` version in force; the stage swaps it in and stamps it on the record |

The event is consumed through this service's own consumer group and the inbox of the platform event library, so a redelivery acts once and a repeated cloud event ID is dropped (DP-09). A replayed workflow reuses the recorded result of the activity, so no second evaluation happens on replay.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (booking branch) | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, treatment ID, business date, the request facts and the package in force; holds the wait for the next batch as a durable timer; output: the stage outcome of section 9 |
| `evaluateBookingMatch` | Activity | `rwb-treatment` | Reads the treatment row, checks the state and the type, builds the facts and evaluates the `BOOKING_MATCH` version in force; returns the row, the version, the outcome and the differing terms |
| `recordAndApply` | Activity | `rwb-treatment` | One transaction: `booked_at` or `booking_difference` with the state, the decision record, the outbox row and the idempotency row (the `RecordAndApply` activity contract of the design) |

Drools is called only inside `evaluateBookingMatch` and never from workflow code. The activity names beyond the design's `TreatmentWorkflow` and `RecordAndApply` are this story's design choice and are fixed by no source document (GAP-2691; ASM-4444).

#### 12.6 Schedules

None registered as a Temporal Schedule and no Quartz job. JOB-08 runs as an event-started workflow on queue `rwb-integration` in `RWB-P2-E2007-APP` (DP-10); this service runs no scan over treatments. The wait between two ALS batches is a durable timer inside `TreatmentWorkflow`, bounded by the grace count read from the parameters contract, so a treatment is never discovered late by a poll and no row of rwb-case's `timer` table is read (GAP-2692; ASM-4448).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Writes `booked_at`, `booking_difference` and `state`; the table arrives with `RWB-S2-E3001-APP` and this story's Flyway version adds the booking rule (DP-01) |
| `decision_record` | `rwb_treatment` | PLT library object applied in this schema | Written through `DecisionRecordWriter.record` in the caller's transaction; the central `decision_log_entry` is P7's and is never touched (DP-03) |
| `processed_event`, `outbox_event`, `idempotency_key` | `rwb_treatment` | PLT library, applied in this schema | The inbox row, the outbox row of the record and the write key of the step, written by the library in the step's transaction (DP-09) |

Not owned and never read as a table: `recovery_case`, `task`, `case_account` (P3, `rwb_case`), `rule_package`, `rule_package_version`, `rule_row` and `decision_log_entry` (P7, `rwb_decision`), `reconciliation_result` and every `v_ace_*` view (P1). No foreign key leaves the schema and no cross-schema join exists.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `RWB-P2-E2007-CON` treatment fake | The mark-booked write for `TRT-SYN-0701` with `A-0701` booked 2026-12-16 at 650,000.00 baht; the difference write for `TRT-SYN-0703` with 4.2500 approved and 4.5000 booked; no write for `TRT-SYN-0702`; the approved-not-booked list of 2026-12-16 | AC1, AC2, AC3, AC4, AC7 |
| `BOOKING_MATCH` package fixture | Version `BKG-2026.12` with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00, and a business date with no version in force | AC1, AC2, AC6 |
| RWB-PLT-E1027-CON writer fake | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009; an unavailable store raising MSG-P7-003 | AC1, AC5 |
| rwb-case parameters and reference-data fakes (`RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`) | `booking.missing.grace_loads` = 1 at its version, LOV-TREATMENT and the outcome codes at their version, and a delayed answer beyond 2 s | AC7, X7 |
| gateway-bff composite route fake (`RWB-PLT-N001-CON`) | The merged SCR-14 answer for case `RW-2026-000701` with the case read of rwb-case and the treatment read of this service, one hop each | AC8 |

The fakes are test-only and are replaced by the real services in SIT; a drift between a fake and the published contract is a build failure of `RWB-P2-E2007-CON` or of the platform story that owns the fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 2 consumed | The treatment read, the approved-not-booked read and the two booking writes on `/api/recovery/treatment/v1`; the parameters and reference-data reads of rwb-case, one hop and 2 s each |
| Kafka | 1 published, 1 consumed | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` through the library; `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1`; inbox dedupe by cloud event ID |
| Temporal | `TreatmentWorkflow` and 2 activities | Queue `rwb-treatment` in namespace `rwb-recovery`; one child per case and stage; one durable wait; no Schedule |
| File | None | No file is read, built or delivered; the ALS load is rwb-integration's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, module `booking`, Java package `th.co.scb.ace.workbench.recovery.treatment.booking`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

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

DP-01 is the schema rule of sections 11 and 17: the treatment is this service's and the account, batch, rule, case and task facts are answers of contracts or of the caller. DP-03 is the transaction the story is built on. DP-04 is the evaluation of the version in force inside an activity, so the answer is recorded and a replay reuses it. DP-05 is a prohibition here: the ACE facts arrive on the request, so this module reads no `v_ace_*` view and the login holds no grant on one. DP-06 and DP-07 are the parameter and list reads of 12.2, cached. DP-09 is the inbox of the package announcement and the outbox row of the record. DP-10 is the stage step and its durable wait, with no Quartz job and no Schedule in this service. DP-11 is the contract pair the legacy in-process `TreatmentCommands` and `TreatmentQuery` calls become: one hop, a 2 s timeout, a fake, no call chain. DP-13 puts the operations on the service base. DP-19 is SCR-14 behind the gateway-bff composite route.

**Dependencies the table adds and the plan does not hold.** The table adds the H rows `RWB-PLT-E1027-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-TE006-CON`, `RWB-PLT-E1071-CON` and `RWB-PLT-N001-CON`, and the C rows `RWB-P7-E1073-CON`, `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON`, while the plan's lists hold `Depends on (build)` `None`, `Contract dependencies` `RWB-P2-E2007-CON` and no integration or external dependency. The metadata keeps the plan's lists because every added row is a platform library or a contract the service template already carries of wave 0; the story builds against the fakes until those stories publish, and the difference is recorded as GAP-2692 with ASM-4445.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (booking branch) | Workflow | The step, its state guard, the durable wait and the stage outcome report to the parent |
| `BookingWriteController` | REST controller | The approved-not-booked read and the two writes of 12.1, their validation and their problem mapping |
| `BookingCandidateQuery` | Service | The approved RESTRUCTURE and SETTLEMENT treatments not yet booked for a business date, from this schema only |
| `evaluateBookingMatch` | Activity | Reads the row, builds the facts and evaluates the `BOOKING_MATCH` version in force |
| `BookingStateGuard` | Service | Refuses a write on a treatment that is not `APPROVED`, does not match the request or is already booked for the business date |
| `recordAndApply` | Activity | One transaction: the treatment columns, the decision record, the outbox row and the idempotency row |
| `TreatmentBookingRepository` | Repository | Reads and writes `booked_at`, `booking_difference` and `state` of `treatment` in `rwb_treatment` only |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with the row ID, the package version and the booking reference (DP-03) |
| `RulePackageListener` | Consumer | The inbox of `rwb.decision.RulePackageInForce.v1`; a redelivery is dropped before any work (DP-09) |
| `Migrations` | Migration | The booking rule on `treatment` on the per-service Flyway sequence |

**Database.** No table is added: `treatment` arrives with `RWB-S2-E3001-APP`. This story's Flyway version adds the booking rule to `rwb_treatment` — `booked_at timestamptz`, `booking_difference jsonb`, the state check of section 9, the rule that `booked_at` is set only in `BOOKED`, one confirmation per treatment and business date, and the index of the approved-not-booked read — typed as TSD S2 T3.1 and T3.0 type them, with no edit of an applied migration. `decision_record`, `processed_event`, `outbox_event` and `idempotency_key` are library objects applied in this schema by the library's own migrations. No row of another service's table is copied and no key crosses a schema.

**Configuration and reference data.** The package `BOOKING_MATCH` and its rows are rwb-decision's and arrive through the evaluated version; this story stores no rule text, no threshold and no term list (BR4, BR7). The grace count is read through the parameters client library and the treatment types and outcome codes through the reference-data client library at their version (DP-06, DP-07). The capability area "Treatment and offer" and its rights are rwb-access data and the story declares the right only. The feature switch `rwb.treatment.booking-confirmation` is a flag of the platform library: off means the two writes are refused with 404 and the read is unchanged.

**Build steps**

1. The Flyway version with the booking rule on `treatment`, and the migration test against the TSD types.
2. `BookingCandidateQuery` and the approved-not-booked read; test AC7 and the read of a booked treatment.
3. `BookingWriteController` and `BookingStateGuard`, with the 403, 404 and 409 paths; test X1 and AC8.
4. `evaluateBookingMatch` with the package fixture: the RESTRUCTURE and SETTLEMENT rows, both differing terms and no version in force; test AC1, AC2, AC6.
5. `recordAndApply` in one transaction, with the rollback path and the once-only rule; test AC1, AC2, AC5, X3, X4.
6. `RulePackageListener` and the inbox path, with the doubled event; test the dedupe of AC4.
7. The stage outcome report and the durable wait through the grace count; test AC3.
8. The treatment read and the difference on SCR-14 through the composite route fake; test AC8.
9. The boundary and no-PII tests: no statement outside `rwb_treatment`, no `v_ace_*` read, no personal field in the request, the record or the logs; test AC9 and BR10.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-P2-E2007-CON` stay green, a synthetic week of business dates confirms every approved synthetic treatment once with one record naming its package version, a differing term is held once with its approved and booked value, a forced record failure leaves no change and no outbox row, and SCR-14 shows the booked date and the difference through the composite route in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-011 | Task text of a missing booking, rendered by the parent from the stage outcome and not produced here | No booking for treatment {treatment} was found in the ALS batch for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | Task text and treatment note of a differing term, raised by the parent | The booked {term} is {booked}. The approved {term} is {approved}. |
| MSG-P7-003 | The local decision record cannot be written (X3) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No `BOOKING_MATCH` version is in force (X2) | The rule version was refused at the {check} check: {detail}. |
| MSG-P2-006 | The same treatment is already being confirmed, or is not in a state the write allows (X1) | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | The identity has no right on the treatment read (X8) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The treatment does not exist or lies outside the scope (X1) | This case is not in your scope. |
| MSG-GEN-006 | The parameters read or the reference-data read did not answer inside the budget (X7) | {system} is not available. Your request is queued and will be retried. |

MSG-P2-011, MSG-P2-012, MSG-P7-003, MSG-P3-027, MSG-P2-006 and MSG-P4-002 are the legacy texts of RWB-E2-007 carried unchanged; MSG-P4-003 and MSG-GEN-006 are the platform texts the access and resilience standards use for a scope refusal and an unavailable dependency. For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "BOOKING_MATCH" and the business date only, never a case, an account or a person. Each error is an RFC 9457 problem response with `messageId`, `detail` and `instance`; the status mapping is 403 for MSG-P4-002, 404 for MSG-P4-003, 409 for MSG-P2-006, 422 for a refused package check and 503 for MSG-P7-003 and MSG-GEN-006. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-14 Treatment record | Loading | The placeholder while the composite route answers |
| SCR-14 Treatment record | Approved, booking awaited | The approved terms, the approval date and the state, read only |
| SCR-14 Treatment record | Booked | `booked_at` 2026-12-16 and the state `BOOKED`, read only |
| SCR-14 Treatment record | Booked with a difference | Each differing term with its approved and its booked value, read only |
| SCR-14 Treatment record | Refused or out of scope | A role without Treatment and offer R reads MSG-P4-002; a case outside the scope reads MSG-P4-003 |
| SCR-01 My work | Task open | The missing-booking and differing-terms tasks the parent raises, with MSG-P2-011 and MSG-P2-012 |

SCR-14 is served by the gateway-bff composite route, which composes the case read of rwb-case with the treatment read of this service, one hop each, read only (DP-19); the browser calls no owner service directly and the screen writes nothing. SCR-01 My work, SCR-29 Posting (Epic 4) and the REC-03 break list are not this story's: the tasks are the parent's and the break list is rwb-integration's. The screen field list, the route specification and the layout belong to the platform edge story and the screen owners; this story fixes the service side of the answer only (GAP-2691; ASM-4449).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-01 | AC1, BR1, BR3, BR7, BR10 | End to end | Synthetic settlement booked 2026-12-16 at 650,000.00 baht |
| TC-E2-007-02 | AC2, BR5 | End to end | Restructure with tdr_flag false in v_ace_account |
| TC-E2-007-03 | AC3, BR2, BR4, BR6 | End to end | Rate 4.5000 booked against 4.2500 approved |
| TC-E2-007-04 | AC4, BR2 | End to end | Two accounts, one booked |
| TC-E2-007-05 | AC5, BR8 | End to end | ACE batch failed for 2026-12-17 |
| TC-E2-007-06 | AC6 | End to end | JOB-08 rerun for 2026-12-16 |
| TC-E2-007-07 | AC7, BR5 | End to end | Booking missing on two batches |
| TC-E2-007-08 | AC8, BR9 | End to end | Decision log store stopped |
| TC-E2-007-09 | AC9, BR11 | End to end | No BOOKING_MATCH version in force on 2026-12-17 |
| TC-E2-007-10 | Access | Component | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun for JOB-08; refused with MSG-P4-002 |
| TC-E2-007-11 | Principle 5 | Component | Decision log write forced to fail on markBooked; treatment stays APPROVED, no event |
| TC-S2-E2007-APP-01 | AC1, BR5, BR7 | Component | The mark-booked write for "TRT-SYN-0701" and 2026-12-16; booked_at 2026-12-16, state BOOKED, one record naming "BKG-2026.12" |
| TC-S2-E2007-APP-02 | AC2, BR6 | Component | Approved rate 4.2500 against booked 4.5000 on "TRT-SYN-0703"; booking_difference written, state APPROVED |
| TC-S2-E2007-APP-03 | AC3, BR5 | Component | No write for "TRT-SYN-0702" on 2026-12-16; no column changes and no record |
| TC-S2-E2007-APP-04 | AC4 | Component | The same write delivered twice for one treatment and business date; one idempotency row and one record |
| TC-S2-E2007-APP-05 | AC5, BR8 | Component | The record writer forced to fail; no booked_at, no state change, no outbox row, MSG-P7-003 |
| TC-S2-E2007-APP-06 | AC6, BR9 | Component | No BOOKING_MATCH version in force on 2026-12-17; NoPackageInForce, MSG-P3-027, no change |
| TC-S2-E2007-APP-07 | AC7 | Contract | The approved-not-booked read of 2026-12-16 with LOV-TREATMENT members and booking.missing.grace_loads = 1 |
| TC-S2-E2007-APP-08 | AC8 | Component | The composite route fake merging SCR-14 with booked_at 2026-12-16 and the difference of 4.2500 against 4.5000 |
| TC-S2-E2007-APP-09 | AC9 | Contract | A property check over a synthetic party name and an account number in the request, the record and the log lines; no personal field stored |

The eleven identifiers TC-E2-007-01 to TC-E2-007-11 are legacy-carried, kept in order with their Covers and Data character for character; their Covers name the nine legacy criteria, which `RWB-P2-E2007-APP`, `RWB-P3-E2007-APP` and `RWB-P4-E2007-APP` own and answer, so this slice proves the treatment-side half of each row at the level the row's kind allows — the legacy level "System" maps to "End to end", and "Access" and "Principle 5" to "Component", as in the other stories of this run. The nine cases TC-S2-E2007-APP-01 to TC-S2-E2007-APP-09 are new for the criteria of this story that no legacy row exercises. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies of these rows belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No business value in code: the compared terms, the tolerance, the outcomes, the grace count and the list members are rows of the package and of the contracts read at their version; a build check fails on any of them in the Java source or the module configuration (BR4, BR7).
- No personal data in logs, tests, workflow inputs, events or records: the request, the row, the record and the span attributes carry the treatment ID, the case ID, the account key, the row ID, the package version, amounts and dates only, and the profile codec is on every payload (AC9).
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE view, holds no `v_ace_*` grant and receives the account facts on the request built from the rwb-source-data contract (DP-05; ADR-010).
- No read of another service's tables and no cross-schema join: `recovery_case`, `task`, `case_account` (P3), `rule_package`, `rule_package_version`, `rule_row`, `decision_log_entry` (P7), `reconciliation_result` (P1) are reached only through their owners, and the boundary test fails the build on any statement outside `rwb_treatment`.
- The decision record is written in the same transaction as the state change, and a failed write rolls the whole step back with MSG-P7-003; no confirmation and no difference exists without its record (DP-03; BR8).
- One hop and a 2 s budget on every contract call, with a breaker and no call chain; `NoPackageInForce` is not retried and the state change is applied only from the recorded answer of the activity.
- One confirmation per treatment and business date: the idempotency row and the uniqueness rule refuse a second write, and no second record and no second outbox row exists (X4).
- The case route state, its move by R-RES-22 or R-SET-13, the tasks and the case-side decision record are not written here: they are the parent's (DP-01).
- No Quartz job, no Schedule and no timer row: the stage step and its wait are the workflow's (DP-10).
- An applied migration is never edited: the booking rule is a new version on the service's own Flyway sequence.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Booking confirmed from the next day's ALS batch, which this story answers on the treatment side by holding `booked_at`, the state `BOOKED` and the difference on the record that carries them | Business Requirements Program 5.3; Business Requirements Epic 2, section 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-38, R-UNI-39, R-UNI-41 | TC-E2-007-01, TC-E2-007-03, TC-E2-007-11, TC-S2-E2007-APP-01 to TC-S2-E2007-APP-09 |

REQ-CHO-008 is the requirement list of the legacy key, kept unchanged, and FEAT-CHO-08, the BRD sections and L3 process 7.3 are the legacy traceability row's. The measured result REC-03 (approved treatments against bookings, zero after two days) stays with `RWB-P2-E2007-APP` and the data steward's break list, and no criterion of this story claims it.

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E2-007 | The treatment-side deliverable: the approved-not-booked read, the mark-booked and difference writes, `booked_at`, `booking_difference`, the state `BOOKED`, the local decision record, the package version on it, the dedupe, the refusal and the SCR-14 read |
| RWB-P2-E2007-APP and `RWB-P2-E2007-CON` | The match, the row order, JOB-08, the run summary, the REC-03 result, the task codes and texts, the rerun operation, and the shape and fake of the calls this story serves |
| RWB-P3-E2007-APP | The case route state, its move by R-RES-22 or R-SET-13, the tasks and the case-side decision record |
| RWB-P1-E2007-APP | The ACE account and batch-status read behind `treatment` contract consumers |
| RWB-P7-E2007-APP, `RWB-P3-E2042-CON` | The `BOOKING_MATCH` package, its rows, its versions and the version in force |
| RWB-P4-E2007-APP | The right on the read and the refusal of the rerun |
| RWB-S2-E3001-APP to RWB-S2-E3005-APP | The treatment record, the offer, the below-floor approval, the plan offer and the affordability pre-assessment this story does not build |
| RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON | The library and contract rows the pattern table adds, which stand in no build row of this story (GAP-2692; ASM-4445) |
| DP-01, DP-05, DP-13 | The owner's schema, no ACE view and the base `/api/recovery/treatment/v1` |
| DP-11, DP-19 | One hop with a 2 s timeout on the contract pair, and SCR-14 behind the gateway-bff composite route |
| ADR-013, ADR-014, ADR-015, ADR-016, ADR-017, ADR-020, ADR-022 | 19 services inside ACE, a schema and a login per service, Kafka with outbox and inbox, the reusable Temporal layer with Schedules replacing Quartz, embedded Drools per service, contract-first REST with one hop, and the local decision record |

### 19. Out of scope

- The match, the facts, the row order of the package, JOB-08 and its run, the run summary, the task codes and texts, and the REC-03 break list: `RWB-P2-E2007-APP`.
- The operation names, the payload element names and the fakes of `RWB-P2-E2007-CON`, and the rerun operation `POST /admin/jobs/{jobId}/rerun` (GAP-2691; ASM-4444).
- The ACE account and batch-status read through `recovery.v_ace_*` and the Section B columns of RWB-ACE-001: `RWB-P1-E2007-APP` (DP-05).
- The `BOOKING_MATCH` package, its rows, its load, its tests, its four-eyes approval and its rollback: rwb-decision (P7), `RWB-E2-042` and `RWB-P3-E2042-CON`.
- The case route states `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT`, `BOOKED_IN_ALS_NLEADS` and `AWAITING_PAYMENT`, their move, the tasks `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` and `UNMATCHED_EXCEPTION`, and the case-side decision record: `RWB-P3-E2007-APP`.
- `TreatmentBooked` (EV-11) and any posting to ALS: rwb-payment and FEAT-PAY-06, Epic 4.
- The rights, the roles and the scope data, and the guard library: `RWB-P4-E2007-APP` and the platform library stories.
- The treatment record, the settlement offer, the below-floor approval, the plan offer, the plan timers and the payment matching of the plan: `RWB-S2-E3001-APP` to `RWB-S2-E3011-APP`.
- SCR-29 Posting, the reconciliation agent, the settlement payment matching and the application of proceeds to the case balance: Epic 4.
- The gateway-bff composite route, the SCR-14 and SCR-01 field lists and the layout: `RWB-PLT-N001-CON` and the screen owners (DP-19).
- The real cross-service proof of a confirmation against the live rwb-integration, rwb-source-data, rwb-case and rwb-decision: the wave 2 integration harness.
- The deployment of this build: chart values, the queue and topic provisioning, the flag, dashboards and the runbook.
