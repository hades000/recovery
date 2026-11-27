# RWB-P7-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P7-U |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2007-CON |
| Contract version | v1 (the /v1 path of RWB-P2-E2007-CON) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CHO-008) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-066 |

**Version 3 changes.**

- RD-P1-066: Backfill the published Test Cases v9 cross-references.
- RD-P1-066: Identify the rwb-integration JOB-08 workflow and distinguish it from the P7 decision treatment.
- RD-P1-040: BookingMatchWorkflow starts only on AceDataReady with `sourceSystem` ALS and `status` COMPLETED, with the system-start ID form and policies; the rerun uses `FAIL`.
- RD-P1-003: the consumed EV-26 row states the record key and the data fields.
- Section 16 cites TC-P7-E2007-APP-03 of Test Cases v9 for AC1 (test case backfill).

**Change log.** D-RCV-60, 22 November 2026: the rwb-decision slice of RWB-E2-007 — the BOOKING_MATCH evaluation of every approved restructure and settlement against the account as ACE holds it after the ALS batch, one hash-chained decision record per treatment and business date, the outcome event, the batch gate, the package-version stamp, the rerun and the read of the decisions of a date — is split from the ALS batch and account read (rwb-integration, RWB-P2-E2007-CON), the treatment booking state and the booking difference (rwb-treatment), the task and the case move (rwb-case), the TreatmentBooked event (rwb-payment) and the posting screen. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 42 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3 aligns the story with RD-P1-003, RD-P1-040. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As a **restructuring officer (RW-RESTRUCT), a Credit Administration officer (RW-CREDITAD), a data steward (RW-DATASTEW) and the rwb-decision service that decides the match**, I want **every approved restructure and settlement compared with the account as ACE holds it after the next ALS batch, the comparison decided by package BOOKING_MATCH version "BKG-2026.12" in force with the outcome BOOKED, NO_BOOKING or TERMS_DIFFER and the row and the package version named, one append-only decision record per treatment and business date, the outcome announced once on the service topic, the run gated on the completed ALS batch, a repeat or a rerun writing nothing twice and no version in force refused rather than defaulted**, so that **every approved decision is confirmed as booked in the core bank without a file the Workbench has to load, and any booking that is missing or differs is explainable the next morning from one read**.

Inside `rwb-decision` this is the decision and record half of RWB-E2-007:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` (DP-03).
- The evaluation: package `BOOKING_MATCH`, version `BKG-2026.12`, with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht, is evaluated through the embedded Drools kit for each treatment and each account of its case (DP-04). The result names the row that decided, the outcome, the difference terms and the package version. The service holds no comparison code and no rule table.
- The record: one `decision_log_entry` per treatment and business date, append only and hash-chained, carrying the decision code from LOV-DECISION, the rule ID of the deciding row, the rule version `BKG-2026.12`, an inputs reference to the account facts of the business date, the recommendation, the final call BOOKED, NO_BOOKING or TERMS_DIFFER, the actions with the difference terms and the accounts without a booking, the actor and the decided time.
- The announcement: `rwb.decision.BookingDecisionMade.v1` on `rwb.decision.events.v1`, key `treatmentId`, once per treatment and business date, carrying the outcome, the row, the package version and the business date, so the treatment owner books, the case owner raises the task and rwb-payment posts.
- The gate: the run starts on `rwb.source-data.AceDataReady.v1` with `sourceSystem` ALS, `status` COMPLETED and business date D and evaluates nothing until the batch for D is COMPLETE through the rwb-integration contract (DP-05, DP-11).
- The run controls: the P7 rule and decision work invoked by the rwb-integration JOB-08 workflow (DP-10), the idempotency key treatment ID and business date, and the rerun operation under platform administration.
- The read: the decisions of a business date or a treatment, with the outcome, the row, the package version and the difference terms, serving the REC-03 break list and the officer's view.

That this slice decides rather than only stores is the Work Package's placement, and it meets DP-04 where DP-04 keeps the evaluation in one service: the package is evaluated here, on the version this service holds, and no other service evaluates `BOOKING_MATCH` (GAP-2485; ASM-4120).

Not this story: the ALS batch read and the account snapshot (rwb-integration, RWB-P2-E2007-CON and RWB-P2-E2007-APP), the treatment booking state with booked at and the difference (rwb-treatment), the task, the route state and the case move by R-RES-22 and R-SET-13 (rwb-case), the TreatmentBooked event and the posting (rwb-payment, Epic 4), the registry and its governance (RWB-P7-E2042-APP, RWB-P7-E1073-APP), and the screens (SCR-14, SCR-01).

### 2. Business rationale

The officer books a restructure or a settlement in ALS by hand and nothing checks today that the booked terms equal the approved terms. In the monolith the comparison was a class beside the rule evaluator, the result was written on the treatment by the same module that read the ACE views, and the only proof of why a booking was confirmed was a rule ID with no version beside it. In the target the three halves separate: rwb-integration reads the completed batch and the account as ACE holds it, rwb-treatment holds the booking state and the difference, and rwb-case owns the task and the route move. What is left, and what this story owns, is the decision itself and its proof.

Both mechanisms fail silently when they are wrong. A decision taken outside a version in force looks like a decision and cannot be reproduced. A decision that leaves before its record is written, or a second run that decides the same treatment again, produces two bookings, two events or a missing booking counted twice, and the officer sees a task or a case move that no rule explains. This story closes both: the package decides, no version in force is a refusal, the record is written before the event leaves, and the key treatment and business date makes a repeat a no-op.

The measure is decision-shaped: one record and one event per treatment and business date; a BOOKED outcome only when every account matches; a task request only when the grace batches are exhausted or a term differs; the run silent for a business date whose batch is not COMPLETE; and every answer naming the row and `BKG-2026.12`. It meets REQ-CHO-008 and gives the treatment, case and payment owners one decision to act on.

The realignment changes the mechanism, not the business rule: the single recovery schema becomes `rwb_decision` (DP-01); the in-process `RuleEvaluator` call becomes the embedded kit on the version this service holds (DP-04); the published treatment interfaces become REST contracts with a mock, one hop and 2 s (DP-11); the Quartz JOB-08 becomes an event-started workflow (DP-10); the monolith base becomes `/api/recovery/decision/v1` (DP-13); and the ACE reads move behind the rwb-integration contract, so no `v_ace_*` view is read here (DP-05).

### 3. Preconditions

- RWB-P2-E2007-CON is published: the ALS batch-status read for a business date with its status and completeness, and the account snapshot of a case at a business date with the restructure and settlement fields, each with its refusals and its fake (DP-11, DP-13).
- Package `BOOKING_MATCH` version `BKG-2026.12` is loaded, tested, approved and IN_FORCE for the business date, with the RESTRUCTURE rows (tdr_flag, last_tdr_date, principal_outstanding, interest_rate against the approved terms) and the SETTLEMENT rows (settlement booked date and amount against the offer amount) and tolerance 0.00 baht. The rows come from RWB-P7-E2042-APP and RWB-P7-E1073-APP; this story evaluates the version and writes none of it.
- The `rwb_decision` baseline is in place: the schema, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` and `decision_log_entry` with `chain_seq`, `prev_hash`, `entry_hash`, the append-only trigger and the idempotency key, plus the outbox and inbox objects of DP-09 and the per-service login (DP-02). The login name is Not specified in the source documents (GAP-2489; ASM-4038).
- RWB-PLT-E1072-CON (embedded Drools kit), RWB-PLT-E1027-CON (record library and `rwb.decision-record.v1`), RWB-PLT-E1071-CON (workflow kit), RWB-PLT-E1042-CON and RWB-PLT-E1043-CON (parameters and reference-data clients), RWB-PLT-TE006-CON (outbox library) and RWB-PLT-N001-CON (composite route) are published with their fakes.
- The treatment owner's contract is published: the approved-not-booked read, the booking write with booked at and booking reference, and the difference write. The case owner's task operation and its parameters and list reads are published. Their paths and payloads are Not specified in the source documents (GAP-2486; ASM-4121).
- `booking.missing.grace_loads` = 1 is in force and is read as a parameter (DP-06); the outcome list BOOKED, NO_BOOKING and TERMS_DIFFER, LOV-DECISION and the version-state list are read as reference data (DP-07). The legacy flag `rwb.integration.booking-confirmation` is read as a parameter, not as a constant.
- Synthetic facts of the tests: case `RW-2026-000701` with accounts `A-0701` to `A-0705`; treatments `TRT-SYN-0701` (settlement, 650,000.00 baht), `TRT-SYN-0702` and `TRT-SYN-0704` (restructure), `TRT-SYN-0703` (restructure, offer 1,800,000.00 baht at 4.2500 percent, booked 4.5000 percent); business dates 2026-12-15 to 2026-12-18.
- No build dependency: the story builds against the published contract fake, the registry rows and the baseline, so it starts on Day 1 in lane L-P7-U (Template and Rules §R5.7 rules 2 and 8).

The platform H rows and the consumed contracts the patterns add — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON and RWB-PLT-N001-CON, and C RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON and the treatment and task contracts — are not repeated in the metadata rows, which name None and RWB-P2-E2007-CON (GAP-2488; ASM-4123).

### 4. Flow

1. `rwb.source-data.AceDataReady.v1` with `sourceSystem` ALS, `status` COMPLETED and business date D starts `BookingMatchWorkflow` on queue `rwb-integration`; one run per business date, started again only by the rerun operation.
2. Batch gate: `BatchGate` reads the ALS batch for D through the rwb-integration contract. Unless the batch is COMPLETED and complete, the workflow names the source and the date, ends and writes nothing.
3. `BookingCandidateReader` reads the approved RESTRUCTURE and SETTLEMENT treatments not yet booked through the treatment contract, and the accounts of each case at D through the account contract, which carries the account set and the product group of the case. No `v_ace_account` column and no `rwb_case.case_account` row is read.
4. `BookingMatchFactsBuilder` builds the facts of one treatment and one account: the treatment type, the approved terms, the account fields, the business date and the run's grace count.
5. `BookingRuleEvaluator` evaluates package `BOOKING_MATCH` on version `BKG-2026.12` through the embedded kit and returns the row that decided, the outcome BOOKED, NO_BOOKING or TERMS_DIFFER, the difference terms and the package version. No comparison code and no rule table exists in this service.
6. `BookingDecisionService` reduces the per-account results to one treatment outcome: BOOKED when every account matches, NO_BOOKING when an account shows no booking, TERMS_DIFFER when a booked term differs.
7. `BookingRecordAppender`, one transaction: appends the `decision_log_entry` with the decision code, the rule ID, the rule version `BKG-2026.12`, the inputs reference, the recommendation, the final call, the actions and the actor, and writes the `rwb.decision.BookingDecisionMade.v1` outbox row.
8. On commit, the outcome leaves as `rwb.decision.BookingDecisionMade.v1` on `rwb.decision.events.v1`, keyed by treatmentId, one per treatment and business date, carrying the outcome, the row, the package code and version, the business date and the difference terms. The treatment owner books with booked at and the booking reference (account key and business date) or records the difference; the case owner raises one task WITH_OPS_BOOKING, WITH_OPS_SETTLEMENT or UNMATCHED_EXCEPTION for the role and message it is given; rwb-payment posts and publishes its own event.
9. A task request is sent only when the outcome is NO_BOOKING with no grace batch left, or TERMS_DIFFER; the request is deduplicated on the case, the task code and the treatment, so an open task is never doubled.
10. Rerun: `POST /api/recovery/integration/v1/admin/jobs/{jobId}/rerun` for a business date. A batch that is not complete is refused; a run in flight is refused with MSG-P2-006; a treatment already decided for D is skipped by the idempotency key.
11. Any time: `GET /api/recovery/decision/v1/booking-decisions` answers the decisions of a business date, a treatment or a case with the outcome, the row, the package version, the difference terms and the decided time, and a repeat count where a repeat arrived.
12. Nothing in this flow writes a treatment row, a task row, a case state, an account copy or a `v_ace_*` view: the record, the event and the read are the whole deliverable.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ALS batch for business date D is not COMPLETE | The workflow ends before the evaluation, names the source and the date, and writes no record, no event and no task request | MSG-P1-001 | AC5 |
| X2 | No `BOOKING_MATCH` version is IN_FORCE on the business date | `NoPackageInForce`; no treatment is decided, no record and no event are written, no task request is sent, the run ends as failed and alerts RW-PLATADM | MSG-P3-027 | AC6 |
| X3 | The decision record cannot be appended | Nothing leaves: no event, no booking write, no task request, no difference write; one incident is raised and the run resumes with the next batch | MSG-P7-003 | AC8 |
| X4 | The same treatment is returned again for the same business date, or the workflow is rerun for it | No second record and no second event; the first entry ID is answered and the repeat count is raised for R-UNI-40 | None | AC7 |
| X5 | A rerun is asked for while the run of that business date is in flight | 409; one run continues and nothing is written twice | MSG-P2-006 | AC7 |
| X6 | A caller without platform administration asks for a rerun | 403; nothing runs and nothing changes | MSG-P4-002 | AC7 |
| X7 | Only some accounts of the case show a booking | The outcome is NO_BOOKING; the record names the accounts without a booking; one task request only | MSG-P2-011 | AC4 |
| X8 | A booked term differs from the approved term | The outcome is TERMS_DIFFER; the difference terms are on the record and on the event; one task request for Credit Administration | MSG-P2-012 | AC3 |
| X9 | The account or the treatment contract answers slowly, refuses or is unavailable | The treatment is left undecided for that run, no record is written, and the next batch retries; the answer arrives within one hop and 2 s | MSG-GEN-006 | AC5, AC8 |

A missing version is never a default match, a missing batch is never an empty account set, and an unavailable contract is never a NO_BOOKING outcome: where the facts are not known the treatment stays undecided and the next batch retries. The treatment state, the route move and the task text are the owners' and are proved by their stories and by RWB-ITG-E2007-ITG.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P2-E2007-CON and its fake, the treatment and task contracts with their fakes, the `rwb_decision` baseline and the `BOOKING_MATCH` rows; it evaluates in its own service and calls no rule engine elsewhere |
| Negotiable | The rows, the terms compared, the tolerance, the grace and the outcome list are package rows, parameters and reference data; the story fixes only the decision, the record, the event and the gates |
| Valuable | Every approved restructure and settlement is confirmed as booked or raised, and every answer names the row and the version that made it |
| Estimable | One workflow with six activities, one facts builder, one evaluator call, one decision service, one appender, one reader and two operations |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Each criterion is a run, a decision, a record, an event, a rerun or a read, with fixed synthetic values |

### 7. Acceptance criteria

```gherkin
Feature: Booking confirmation from the ALS load, decided in rwb-decision

  Background:
    Given the rwb-integration contract mock returns the ALS batch for business date 2026-12-16 with status "COMPLETED" and isComplete true
    Given the rwb-integration contract mock returns account "A-0701" of case "RW-2026-000701" at business date 2026-12-16
    Given the rwb-case parameters contract mock returns booking.missing.grace_loads 1
    Given package "BOOKING_MATCH" version "BKG-2026.12" is IN_FORCE with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht
    Given the business date is 2026-12-17

  Scenario: AC1 A settlement whose accounts match is decided BOOKED and recorded once (new, D-RCV-60)
    Given settlement treatment "TRT-SYN-0701" on case "RW-2026-000701" was approved on 2026-12-15 with offer amount 650,000.00 baht
    Given the rwb-integration contract mock returns settlement booked date 2026-12-16 and settlement booked amount 650,000.00 baht for account "A-0701" at business date 2026-12-16
    When BookingMatchWorkflow runs for business date 2026-12-16
    Then the SETTLEMENT row of package "BOOKING_MATCH" version "BKG-2026.12" decides the outcome "BOOKED"
    Then one decision_log_entry exists for case "RW-2026-000701" and business date 2026-12-16 with rule_version "BKG-2026.12", final_call "BOOKED" and the row ID in its actions
    Then rwb.decision.BookingDecisionMade.v1 is published once with treatmentId, businessDate 2026-12-16, outcome "BOOKED", the row ID and the package version
    Then the inputs reference names the account facts of business date 2026-12-16 and carries no account number

  Scenario: AC2 A missing booking is decided NO_BOOKING only after the grace batches, and the grace is a parameter (new, D-RCV-60)
    Given restructure treatment "TRT-SYN-0702" was approved on 2026-12-15
    Given the rwb-integration contract mock returns tdr_flag false for account "A-0702" at business date 2026-12-16
    When the workflow runs for 2026-12-16 with booking.missing.grace_loads 1
    Then the RESTRUCTURE row returns the outcome "NO_BOOKING" and no grace batch remains for the treatment
    Then one record with final_call "NO_BOOKING" and one event are written for the treatment and the date
    Then the task request for "WITH_OPS_BOOKING", role "RW-RESTRUCT" and MSG-P2-011 is sent to the case owner and this service writes no task row
    When the rwb-case parameters contract mock returns booking.missing.grace_loads 2 and the run is repeated for the same date
    Then no record, no event and no task request is produced while a grace batch remains

  Scenario: AC3 A booked term that differs is decided TERMS_DIFFER with the terms on the record (new, D-RCV-60)
    Given restructure treatment "TRT-SYN-0703" was approved with offer amount 1,800,000.00 baht and rate 4.2500 percent
    Given the rwb-integration contract mock returns tdr_flag true, last TDR date 2026-12-16, principal 1,800,000.00 baht and rate 4.5000 percent for "A-0703"
    When the workflow runs for 2026-12-16
    Then the RESTRUCTURE row returns the outcome "TERMS_DIFFER" with approved rate 4.2500 and booked rate 4.5000
    Then the actions of the record carry interest rate approved 4.2500 and booked 4.5000
    Then the task request for "UNMATCHED_EXCEPTION", role "RW-CREDITAD" and MSG-P2-012 is sent to the case owner
    Then the treatment state is not changed by this service

  Scenario: AC4 Only some accounts of the case are booked (new, D-RCV-60)
    Given restructure treatment "TRT-SYN-0704" covers accounts "A-0704" and "A-0705"
    Given the rwb-integration contract mock returns the booking for "A-0704" only at business date 2026-12-16
    When the workflow runs for 2026-12-16
    Then the outcome is "NO_BOOKING" and the actions of the record name account "A-0705" as not booked
    Then one task request names "A-0705" and no second task request is sent for the same treatment, code and case

  Scenario: AC5 No decision is taken for a business date whose batch is not complete (new, D-RCV-60)
    Given the rwb-integration contract mock returns the ALS batch for business date 2026-12-17 with status "FAILED" and isComplete false
    When the workflow is due for 2026-12-17
    Then the workflow ends before the evaluation and names the source "ALS" and the date 2026-12-17
    Then no decision_log_entry, no event and no task request exists for 2026-12-17
    Then the treatment stays undecided and its missing booking count is not advanced

  Scenario: AC6 No version in force is a refusal, never a default (new, D-RCV-60)
    Given no "BOOKING_MATCH" version is IN_FORCE on 2026-12-17
    When the workflow runs for business date 2026-12-16
    Then NoPackageInForce is raised with MSG-P3-027 naming "BOOKING_MATCH" and the business date only
    Then no treatment is decided, no record and no event are written and no task request is sent
    Then the run ends as failed and alerts role "RW-PLATADM"

  Scenario: AC7 A repeat or a rerun writes no second record and publishes no second event (new, D-RCV-60)
    Given a record with final_call "BOOKED" exists for "TRT-SYN-0701" and business date 2026-12-16
    When the workflow is rerun for 2026-12-16, or the same treatment is returned again by the treatment contract mock
    Then no second decision_log_entry and no second rwb.decision.BookingDecisionMade.v1 are written
    Then the first entry ID is answered and the repeat count is raised for R-UNI-40
    When RW-PLATADM calls POST /api/recovery/integration/v1/admin/jobs/{jobId}/rerun while the run of that date is in flight
    Then the call is refused with 409 and MSG-P2-006
    When RW-CASEOWN calls the same operation
    Then the call is refused with 403 and MSG-P4-002

  Scenario: AC8 The record is written before the decision leaves, so a failed record stops the decision (new, D-RCV-60)
    Given the decision log store is unavailable
    When the workflow decides "BOOKED" for "TRT-SYN-0701"
    Then no rwb.decision.BookingDecisionMade.v1 is published and no booking write is sent to the treatment owner
    Then one incident is raised with MSG-P7-003 and the treatment, the task and the route state are untouched
    When the store is available again and the next batch runs
    Then the decision is taken once and recorded once

  Scenario: AC9 The read serves the decisions of a date and no personal data leaves (new, D-RCV-60)
    Given records of business date 2026-12-16 exist for the outcomes "BOOKED", "NO_BOOKING" and "TERMS_DIFFER"
    When a reader holding Decision log R calls GET /api/recovery/decision/v1/booking-decisions?businessDate=2026-12-16
    Then each item carries the treatmentId, the caseId, the outcome, the row ID, the package version and the decided time
    Then no name, account number, mobile number or e-mail address appears in any item, any event payload or any log line
    Then a role without Decision log R is refused with 403 and MSG-P4-002

  Scenario: AC10 This service writes no row of another owner (new, D-RCV-60)
    Given settlement treatment "TRT-SYN-0701" on case "RW-2026-000701" was decided "BOOKED" for business date 2026-12-16
    When the decision is recorded and published
    Then no row of the treatment state, the booking difference, the task, the route move or the posting is written by this service
    Then the service holds only the treatment identifier, the case identifier and the record of the decision

  Scenario: AC11 An unauthenticated read is refused with 401 and an unknown job with 404 (new, D-RCV-60)
    When a caller without a token calls GET /api/recovery/decision/v1/booking-decisions?businessDate=2026-12-16
    Then the answer is 401 and no decision is returned
    When a caller with platform administration calls POST /api/recovery/integration/v1/admin/jobs/{jobId}/rerun with a jobId that does not exist
    Then the answer is 404 and no run starts

  Scenario: AC12 A replayed write with the same idempotency key answers the first result and writes nothing new (new, D-RCV-60)
    Given a decision for "TRT-SYN-0701" and business date 2026-12-16 was written with an idempotency key
    When the same write is replayed with the same idempotency key
    Then the first entry ID is answered and no second decision_log_entry and no second rwb.decision.BookingDecisionMade.v1 are written

  Scenario: AC13 A retried or timed-out decision activity takes the decision once (new, D-RCV-60)
    Given the decision activity for "TRT-SYN-0701" on business date 2026-12-16 times out before it returns
    When the activity is retried
    Then one decision_log_entry and one rwb.decision.BookingDecisionMade.v1 exist for the treatment and the date
    Then the retry writes no second record
```

The thirteen criteria are new under D-RCV-60 and test only this deliverable: the evaluation of the version in force, the record, the event, the batch gate, the no-version refusal, the repeat, the fail-closed write, the read, the boundary of the owners' rows, the error answers, the replay of a write and the retry of an activity. They own no legacy criterion, because the eleven criteria of RWB-E2-007 are carried by the slices that own the treatment, the case, the payment and the screens, with their origin tag. The values inside them are the legacy values — the package code, the version label, the tolerance, the grace, the cases, the accounts, the treatments, the amounts and the rates — so the decision is proved on the same data the legacy story used. That the eleven legacy test cases stay with this slice while no legacy criterion does is the Work Package's ruling on a secondary slice (GAP-2490; ASM-4124).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Bookings are made by the officer in ALS and confirmed only from the next ACE batch; this story never calls ALS and reads only what the completed batch holds | INT-03; DL12 (open; assumptions ASM-0189, ASM-2559, ASM-2608); D-RCV-35 U1; legacy BR1 |
| BR2 | A restructure is decided BOOKED when every account matches the RESTRUCTURE rows of the version in force: tdr_flag true with a last TDR date on or after the approval date and the terms equal | DF-ACE-031; DF-ACE-030; CTL-26; D-RCV-36 T5; legacy BR2 |
| BR3 | A settlement is decided BOOKED when the account matches the SETTLEMENT rows: a settlement booked date on or after the approval date and a booked amount equal to the offer amount | R-SET-13; D-RCV-36 T5; legacy BR3 |
| BR4 | The tolerance on amounts and rates is zero, taken from the row of the version in force and never from code | DL25 (open; assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602); legacy BR4 |
| BR5 | A missing booking raises one task request only after `booking.missing.grace_loads` batches, read as a parameter; the treatment stays approved | REC-03; parameter booking.missing.grace_loads; DP-06; legacy BR5 |
| BR6 | A difference in terms raises one task request for Credit Administration and puts the difference terms on the record and on the event | REC-03; FEAT-CHO-08; legacy BR6 |
| BR7 | The package decides through the embedded kit and the result names the row and the package version; this service holds no comparison code and no rule table | D-RCV-36 T3, T5; ADR-012, ADR-017; DP-04; legacy BR10 |
| BR8 | No version in force is a refusal (NoPackageInForce) with MSG-P3-027, never a default match and never an older version | R-UNI-41; D-RCV-36 T7; legacy BR11 |
| BR9 | The record is written in the same transaction as the outbox row and before anything leaves; a decision whose record cannot be written does not proceed | Principle 5; R-UNI-39; MSG-P7-003; legacy BR9 |
| BR10 | One decision per treatment and business date: the key makes a repeat and a rerun a no-op, the first entry ID is answered and the repeat is counted | R-UNI-40; legacy AC6 |
| BR11 | No decision is taken for a business date whose ALS batch is not COMPLETE, and no account set is assumed empty | JOB-08; CTL-02; legacy BR8 |
| BR12 | The treatment state, the booking difference, the task, the route move and the posting are the owners'; this service holds their identifiers and the record of the decision, never the case | DP-01; DP-03; DP-11; legacy section 10 |
| BR13 | BookingMatchWorkflow starts on the AceDataReady event with sourceSystem ALS and status COMPLETED for business date D on queue rwb-integration, with workflow ID in the form `booking-match-{businessDate}`, conflict policy `USE_EXISTING`, reuse policy `ALLOW_DUPLICATE` for the system start and `FAIL` for the rerun (RD-P1-040); the timezone, overlap, retry, fallback and flag-off behaviour are Not specified in the source documents (GAP-2491) | GAP-2491 (R-28728) |
| BR14 | The run writes no reconciliation_result table: each decision and its outcome are published as events and recorded in decision_log_entry; the owner of the REC-03 break list is Not specified in the source documents (GAP-2492) | GAP-2492 (R-28729) |

BR1 to BR4 run in `BookingMatchFactsBuilder` and in the package rows it feeds; BR7 runs in `BookingRuleEvaluator`, which contains no comparison of its own; BR8 runs before any candidate is read, so a refusal costs no account read. BR5, BR6 and BR12 run in `BookingDecisionService`, which turns the per-account results into one outcome and sends a request rather than writing another service's row. BR9 and BR10 run in `BookingRecordAppender`, where the append, the chain lock and the outbox row are one transaction and the key on the treatment and the business date decides the repeat. BR11 runs in `BatchGate` ahead of the workflow's evaluation step.

### 9. State transitions

This story changes no case status, no route state and no treatment state; it owns the decision and its record.

| From | Event | Condition | To |
|---|---|---|---|
| No decision for the treatment and the business date | The evaluation step | The batch is complete, a version is in force and every account matches | One record with final_call `BOOKED` and one event |
| No decision for the treatment and the business date | The evaluation step | The batch is complete and an account shows no booking, with no grace batch left | One record with final_call `NO_BOOKING` and one task request |
| No decision for the treatment and the business date | The evaluation step | The batch is complete and a booked term differs | One record with final_call `TERMS_DIFFER` and one task request |
| No decision for the treatment and the business date | The evaluation step | The batch is complete and a grace batch remains, or a contract answer is missing | Nothing: the treatment stays undecided and the next batch retries |
| No decision for the treatment and the business date | The evaluation step | No version is in force, or the batch is not complete | Nothing; the run ends as failed with MSG-P3-027 or MSG-P1-001 |
| Recorded | A repeat, a rerun or the same treatment returned again | The key treatment and business date matches | Unchanged; the first entry ID is answered and the repeat is counted |
| `LOADED`, `APPROVED`, `SUPERSEDED`, `ROLLED_BACK` or `REFUSED` | The evaluation step | The version is not in force | Nothing; the run is refused with MSG-P3-027 and no decision is taken |
| `IN_FORCE` | The evaluation step | The version is in force for the date | `IN_FORCE`, unchanged; only its rows are evaluated |

The treatment state (APPROVED to BOOKED), the route state (WITH_OPS_SETTLEMENT to AWAITING_PAYMENT by R-SET-13, WITH_OPS_BOOKING to BOOKED_IN_ALS_NLEADS) and the task state are the treatment and case owners' and are never written here. The version states are the registry's and change only through the promotion and the rollback of RWB-P7-E1073-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-decision service identity and the `rwb-decision` login (DP-02) | Runs the decision step of the integration workflow, reads the contracts, evaluates the package, appends the record, writes the outbox row and answers the read. The login name is Not specified in the source documents (GAP-2489; ASM-4038) |
| SY-RULES, the embedded Drools evaluator inside this service | Evaluates package `BOOKING_MATCH` on the version in force and returns the row, the outcome, the difference terms and the package version (DP-04) |
| RW-RESTRUCT, restructuring officer | Receives the missing booking task and books in ALS; reads the decisions of the cases in scope (Decision log R, scope applied) |
| RW-CREDITAD, Credit Administration officer | Receives the differing terms task and reads the difference terms of the case in scope |
| RW-DATASTEW, data steward | Reads the decisions of a date as the REC-03 break list (Decision log R) |
| RW-PLATADM, platform administrator | Calls the rerun operation for a business date (Platform administration, U) and reads the incidents of a failed run |
| RW-AUDIT, internal audit; RW-COMPLY, Compliance and PDPA officer | Read the records of the booking decisions with their chain state; change nothing |
| RW-COE, center of excellence analyst; RW-RISK, risk and model risk officer | Author, test and approve the package versions through RWB-P7-E1073-APP and RWB-P7-E2042-APP; this story evaluates the version they put in force |
| rwb-integration (P2); rwb-treatment (S2); rwb-case (P3); rwb-payment (P8) | Own the batch and account read, the booking state, the task and the route move, the posting and its event; this service reads their contracts and writes none of their rows |

The rights are the matrix's and the guard's (RWB-P4-E1037-CON); this story declares them and holds no role row. Each REST operation of this story calls the rwb-access authorise check of DP-08 before it acts; the check's name is Not specified in the source documents (DP-08). Refusals are 403 with MSG-P4-002 for a right or a role, 409 with MSG-P2-006 for a run in flight, and 503 with MSG-P7-003 when the record cannot be written. No person is named: the actors are roles, service identities and user references.

### 11. Data

| BR Field ID | Table in rwb_decision | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write |
| DF-DEC-002 | decision_log_entry | case_id (a value from the record, with no foreign key into `rwb_case`) | Write |
| DF-DEC-003 | decision_log_entry | decision_code (a value of LOV-DECISION in force) | Write |
| DF-DEC-004, DF-DEC-005 | decision_log_entry | rule_id (the row that decided), rule_version ("BKG-2026.12") | Write |
| DF-DEC-008 | decision_log_entry | inputs_ref, naming the snapshot with the account facts of the business date and the approved terms | Write |
| DF-DEC-009 | decision_log_entry | recommendation (the outcome the package recommends) | Write |
| DF-DEC-010, DF-DEC-011 | decision_log_entry | approver_user_id, approval_level (empty: the match runs unattended) | Write |
| DF-DEC-012 | decision_log_entry | final_call ("BOOKED", "NO_BOOKING" or "TERMS_DIFFER") | Write |
| DF-DEC-013 | decision_log_entry | override_reason (empty: no person overrides a match) | Write |
| DF-DEC-014 | decision_log_entry | actions (the difference terms, the accounts without a booking, the business date) | Write |
| DF-DEC-015 | decision_log_entry | outcome (the counts of the treatment: accounts read, matched, unmatched) | Write |
| DF-DEC-016, DF-DEC-030 | decision_log_entry | decided_at, actor_user_id (the service identity) | Write |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | decision_log_entry | prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key (treatment ID and business date) | Write |
| DF-REF-274 to DF-REF-278 | rule_package | package code, title, owner role, hit policy | Read |
| DF-REF-279 to DF-REF-286 | rule_package_version | id, version label "BKG-2026.12", status, source reference, generated DRL, checksum, valid from | Read |
| DF-REF-001, DF-REF-003, DF-REF-008, DF-REF-010, DF-REF-011, DF-REF-298 | rule_row | rule_id, rule_version, action_text, owner_role, timer_spec, outputs (the parsed rows evaluated) | Read |
| outbox_event, processed_event, idempotency_key | outbox and inbox objects of DP-09 | all fields | Write |
| DF-TRT-001, DF-TRT-002, DF-TRT-004, DF-TRT-007, DF-TRT-012, DF-TRT-027, DF-TRT-028 | treatment | id, case_id, treatment_type, offer_amount, booked_at, interest_rate, booking_difference | Not read and not written: they arrive as values of the treatment contract and are written by the treatment owner |
| DF-CAS-026 | case_account | account_key | Not read: the account keys arrive in the account answer |
| DF-ACE-001, DF-ACE-025, DF-ACE-030, DF-ACE-031, DF-ACE-036, DF-ACC-009, DF-ACC-030, DF-ACC-031 | v_ace_account | account_key, interest_rate, last_tdr_date, tdr_flag, data_as_of, principal_outstanding, settlement_booked_date, settlement_booked_amount | Not read: no ACE view is read here (DP-05); they arrive in the account answer of the rwb-integration contract |
| DF-ACE-178, DF-ACE-179, DF-ACE-182, DF-ACE-186 | v_ace_batch_status | source_system, business_date, status, is_complete | Not read: they arrive in the batch answer of the rwb-integration contract |
| DF-WRK-018, DF-WRK-019, DF-WRK-022, DF-WRK-023 | task | case_id, task_code, status, owner_role | Not written: sent as the task request and written by rwb-case |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | all fields | Not written: no table of this name exists in `rwb_decision` (GAP-2492; ASM-4126) |

`decision_log_entry` is the only table this story writes, and it is rwb-decision's under DP-01; `rule_package`, `rule_package_version` and `rule_row` are read, and their state is written only by the registry and governance stories. The account, batch, treatment, task and report fields above are the legacy field IDs of the sources, carried as values of a contract answer or a record, never as a column here. No foreign key crosses a schema. The physical shape of the inputs snapshot and of the actions payload is Not specified in the source documents (GAP-2486; ASM-4121).

### 12. Contract

The base is `/api/recovery/decision/v1` (DP-13), the topic is `rwb.decision.events.v1` (DP-14 naming), the queue is `rwb-decision`, the schema is `rwb_decision`, the Java package is `th.co.scb.ace.workbench.recovery.decision`, and the namespace is `rwb-recovery`.

The account answer is account facts only: no treatment term, outcome, difference, tolerance or package version. This slice builds BookingMatchFacts from its treatment contract and those facts, and a contract test fails on any outcome-shaped field in the account answer.

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST (rwb-integration) | `/admin/jobs/{jobId}/rerun` | Rerun a FAILED JOB-08 run for one business date using Idempotency-Key. An already decided treatment is skipped. A completed or running execution returns 409 MSG-P2-006. | Platform administration, U | Per business date; a run in flight answers 409 with MSG-P2-006 |
| GET | `/booking-decisions` | Read the booking decisions of a business date, a treatment or a case: query `businessDate`, `treatmentId`, `caseId`, `outcome`, `page`, `size`; each item carries the outcome, the row ID, the package version, the difference terms, the decided time and the repeat count | Decision log R, scope applied | Not applicable, read only |

`POST /admin/jobs/{jobId}/rerun` is the legacy rerun of section 12 of RWB-E2-007 on the per-service base of DP-13, and `GET /booking-decisions` is the read the REC-03 break list and the officer's view use. The legacy treatment read `GET /treatments/{treatmentId}` is the treatment owner's operation and is not published here. Error answers: 401 no session; 403 the role lacks the right (MSG-P4-002); 404 an unknown business date or treatment; 409 a run in flight (MSG-P2-006) or a batch that is not complete; 503 the record cannot be written (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId`. The exact filters of the read beyond the four named, and the count item's field names, are Not specified in the source documents (GAP-2486; ASM-4121).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/batches/{source}/{businessDate}` | P2 rwb-integration, under RWB-P2-E2007-CON | The ALS batch status and completeness for the business date; the gate of BR11 (DP-05, DP-11, one hop, 2 s) |
| GET | `/api/recovery/integration/v1/cases/{caseId}/accounts?businessDate=` | P2 rwb-integration, under RWB-P2-E2007-CON | The account facts of the case at the business date: the restructure and settlement fields the package compares |
| GET | `/api/recovery/treatment/v1/treatments?type=&state=APPROVED&booked=false` | S2 rwb-treatment | The approved restructure and settlement treatments not yet booked |
| POST | `/api/recovery/treatment/v1/treatments/{treatmentId}/booking` | S2 rwb-treatment | The booking with booked at and the booking reference, or the difference terms; sent only after the record commits |
| POST | `/api/recovery/case/v1/cases/{caseId}/tasks` | P3 rwb-case | One task request for the code, the role and the message, deduplicated on the case, the code and the treatment |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case, under RWB-P3-E1042-CON | `booking.missing.grace_loads` and the legacy flag, through the client library (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, under RWB-P3-E1043-CON | The outcome list, LOV-DECISION and the version-state list with the version in force (DP-07) |

The metadata names one contract dependency, RWB-P2-E2007-CON; the treatment, task, parameters and reference-data operations are the published contracts of their own epics, consumed as fakes (GAP-2488; ASM-4123). Their paths and payloads are Not specified in the source documents (GAP-2486; ASM-4121): the shapes are the legacy published interfaces of section 12 of RWB-E2-007 restated as REST, one hop with a 2 s timeout and a breaker. No ACE view and no other service schema is read.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.BookingDecisionMade.v1` | `rwb.decision.events.v1` | P7 | treatmentId | treatmentId, caseId, businessDate, outcome (`BOOKED`, `NO_BOOKING` or `TERMS_DIFFER`), row ID, package code, package version, difference terms, accounts without a booking, decided at |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` (shared) | P7 record library | entryId | The hash-chained record of the decision: decision code, rule ID, rule version, inputs reference, actor, final call, decided at |

Both rows are written to the outbox in the transaction of the append and relayed with the CloudEvents 1.0 envelope (DP-09). Consumers map the outcome to their own state, task, route move and event; the legacy `TreatmentBooked` (EV-11) stays rwb-payment's and `CaseStateChanged` (EV-05) stays rwb-case's, and this service publishes neither. The event name is Not specified in the source documents (GAP-2487; ASM-4122). No event carries a name, an account number, a mobile number, an e-mail address or a national identity number.

#### 12.4 Events consumed

| Event | Topic | Owner service | Used for |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26, consumed by rwb-integration) | `rwb.source-data.events.v1` | P1 rwb-source-data | Starts `BookingMatchWorkflow` for business date D, only on the event with `sourceSystem` ALS and `status` COMPLETED. Record key `{sourceSystem}:{businessDate}`; data `sourceSystem`, `businessDate`, `status`, `completedAt` (nullable) |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | The approval date a restructure compares its last TDR date against, and the candidate the next run reads |

rwb-integration consumes AceDataReady through `rwb-integration.rwb.source-data.events.v1`. The rwb-decision treatment listener consumes TreatmentApproved through the service-wide group for that topic. Each service dedupes by event ID in its own inbox and uses the retry and `.dlt` topics of DP-09. `TreatmentApproved` is used at run time only; the run never depends on having received it, because the candidate read returns the approval date as well. The payload field names of both events are the owners'.

#### 12.5 Workflows and activities

| Name | Kind | Queue | What it does in this story |
|---|---|---|---|
| BookingMatchWorkflow | Workflow, JOB-08, owned by RWB-P2-E2007-APP | `rwb-integration` | One run per business date: the batch gate, the candidates, the accounts, the evaluation, the decision, the append and the dispatch |
| ReadBatchStatus | Activity | `rwb-decision` | The batch answer of 12.2 and the completeness decision |
| ReadBookingCandidates, ReadCaseAccounts | Activities | `rwb-decision` | The treatment and account reads of 12.2 for one business date |
| EvaluateBookingMatch | Activity | `rwb-decision` | Builds the facts, evaluates the version in force through the embedded kit, and returns the row, the outcome, the difference terms and the version |
| AppendBookingDecision | Activity | `rwb-decision` | One transaction: the `decision_log_entry` append and the outbox row |
| DispatchBookingOutcome | Activity | `rwb-decision` | The booking write or the difference write on the treatment, the task request, and the read-back that confirms the dispatch |

The workflow is event-started (DP-10) and registers no Schedule. The batch of one business date is one workflow run, so the overlap policy is one run per date and a second start is refused with MSG-P2-006.

#### 12.6 Schedules

None. The legacy Quartz JOB-08 becomes the event-started `BookingMatchWorkflow` of 12.5, started by `rwb.source-data.AceDataReady.v1` for source ALS (DP-10). No Temporal Schedule is created by this story, and a fallback sweep is not specified in any source (GAP-2491; ASM-4125). The registry's JOB-20 at 00:01 and the chain check JOB-14 at 02:00 are RWB-P7-E1073-APP's and RWB-P7-E1008-APP's.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | One append-only, hash-chained record per treatment and business date, with the outcome, the row and the version |
| `rule_package`, `rule_package_version`, `rule_row` | P7 (`rwb_decision`) | The package `BOOKING_MATCH` and the version in force, read only |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |
| `rule_test_case` | P7 (`rwb_decision`) | Not used here: the test cases of the version are the authoring story's |

Not owned and not read: `treatment` and its booking columns (S2); `recovery_case`, `case_account`, `task`, `timer` and `queue` (P3); `proceeds` (P8); `parameter_catalog`, `parameter_value`, `reference_version`, `reference_row` and `lov_value` (P3, read through DP-06 and DP-07); `reconciliation_result` (no such table in this schema). No other service reads `rwb_decision`. No migration is added by this story: the table, its chain columns, the append-only trigger and the unique key on the idempotency key arrive with the baseline and RWB-P7-E1008-APP, and an index this read needs is requested from that story.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration contract fake | RWB-P2-E2007-CON | The ALS batch COMPLETED and complete for 2026-12-16; FAILED and not complete for 2026-12-17; an unavailable answer with MSG-GEN-006; the account sets of `A-0701` to `A-0705` with the restructure and settlement fields of the legacy scenarios |
| rwb-treatment contract fake | The treatment contract of S2 | `TRT-SYN-0701` to `TRT-SYN-0704` approved and not booked, with their offer amounts, rates and approval dates; a booking write and a difference write; a treatment returned twice |
| rwb-case contract fake | The task, parameters and lists of P3 | `booking.missing.grace_loads` 1 and then 2; the outcome list, LOV-DECISION and the version states; a task request answered with the open task |
| Registry fixture | RWB-P7-E1073-APP, RWB-P7-E2042-APP | `BKG-2026.12` IN_FORCE with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00; `BKG-2026.13` APPROVED and not in force; a date with no version in force |
| decision-record library fake | RWB-PLT-E1027-CON | The append and the chain, the `DecisionRecorded` outbox row and a forced failure for MSG-P7-003 |
| Drools kit fake | RWB-PLT-E1072-CON | The compile of the version, first-match semantics, the row that decided and a `NoPackageInForce` answer |
| gateway-bff composite route | DP-19 | The decisions page composed with the case header; the path and the merge order are Not specified in the source documents (GAP-2486; ASM-4121) |

Each fake is replaced by the real contract as its story lands, without a change to the scenarios. The fakes carry synthetic IDs, codes, dates and amounts only.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 7 | The rerun and the decisions read provided; the batch, account, treatment, booking, task, parameters and list operations consumed, one hop and 2 s |
| Kafka | Published 2 event types, consumed 1 here | `rwb.decision.events.v1` with `BookingDecisionMade` and `rwb.decision-record.v1` with `DecisionRecorded`; `TreatmentApproved` consumed here. rwb-integration consumes `AceDataReady` |
| Temporal | 1 workflow, 6 activities | `BookingMatchWorkflow` on queue `rwb-decision`, event-started, one run per business date |
| File | None | No file is read or written; the account facts arrive over REST, never as a load |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, modules `bookingdecision` and `bookingdecision.evaluate`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-APP |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How this story applies each row. **DP-01**: the record sits in `rwb_decision`, no other service reads it, and the treatment, account and task values travel as contract answers and payload values, never as columns or foreign keys. **DP-03**: the decision writes one local record and its outbox row in the same transaction, and a record that cannot be written stops the decision (BR9). **DP-04**: the package is evaluated here, on the version this service holds, through the platform kit; the kit is a library and this story embeds it, and the registry's authoring, approval and promotion stay RWB-P7-E1073-APP's and RWB-P7-E2042-APP's. **DP-05**: no `v_ace_*` view is read; the account and batch facts arrive on the rwb-integration contract. **DP-06**: `booking.missing.grace_loads` = 1, the legacy flag and the page size are parameters, never constants. **DP-07**: the outcome list, LOV-DECISION and the version states are read with the version in force. **DP-09**: the outbox row, the inbox dedupe and the CloudEvents envelope carry the outcome and the record. **DP-10**: JOB-08 is the event-started workflow, not a Quartz row and not a Schedule. **DP-11**: the six consumed operations replace the six in-process interfaces of the legacy section 12, one hop with 2 s and a fake. **DP-13**: every path of section 12 uses `/api/recovery/decision/v1`. **DP-19**: no screen is served here; the decisions page reads through the composite route.

The platform H rows and the four consumed contracts the table adds are not in the metadata rows (GAP-2488; ASM-4123): they are wave 0 platform contracts and published contracts of other epics, none of them blocks the build, and an APP story builds against the published set and its fake, so Ready to start stays Day 1.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| BookingDecisionController | Controller | The rerun and the decisions read, with the guard, the scope, the paging and the problem mapping |
| BookingMatchWorkflow | Workflow | One run per business date: gate, candidates, accounts, evaluation, decision, append, dispatch |
| BatchGate | Service | The batch answer, the completeness check of BR11, and the refusal of a run for an incomplete date |
| BookingCandidateReader, AccountFactsReader | Clients | The treatment and account reads of 12.2, one hop, 2 s, breaker |
| BookingMatchFactsBuilder | Service | The facts of one treatment and one account: type, approved terms, account fields, business date, grace count |
| BookingRuleEvaluator | Service | Evaluates `BOOKING_MATCH` through the embedded kit on the version in force; names the row, the outcome, the difference terms and the version; holds no comparison |
| BookingDecisionService | Service | The per-account results to one treatment outcome, the grace rule, the difference rule and the task request |
| BookingRecordAppender | Service | The `decision_log_entry` append with the chain columns, the idempotency key and the outbox row, in one transaction |
| BookingOutcomeDispatcher | Service | The booking write or the difference write on the treatment and the task request, after the commit, with read-back |
| BookingDecisionReader | Service | The read of 12.1: filters, the outcome list, the difference terms, the repeat count, the scope |
| ParameterClient, ReferenceDataClient | Clients | The two platform clients of 12.2 |

**Database and migrations**

- Writes `decision_log_entry` and the outbox, inbox and idempotency objects; reads `rule_package`, `rule_package_version` and `rule_row`. No new table and no new column: `treatment`, `task`, `recovery_case` and `reconciliation_result` do not exist in this schema.
- The record is written with `WHERE` on the idempotency key of the treatment and the business date; a second append for the same key answers the first entry ID and raises the repeat count.
- No migration of this story. The ledger baseline, the append-only trigger, the chain lock and the unique key on the idempotency key are RWB-P7-E1008-APP's; an index on `(decision_code, decided_at)` for the read of 12.1 is requested from that story rather than added here (GAP-2486; ASM-4121).

**Configuration and reference data**

- `booking.missing.grace_loads` = 1 through DP-06; the legacy flag `rwb.integration.booking-confirmation` is read as a parameter and is no longer a code constant.
- The package code `BOOKING_MATCH`, the version `BKG-2026.12`, the RESTRUCTURE and SETTLEMENT rows and the tolerance 0.00 baht are registry rows of RWB-P7-E2042-APP and RWB-P7-E1073-APP; this story reads them and writes none of them.
- The outcome list, the decision code and the version states are reference data with the version in force (DP-07); the decision code of a booking decision is Not specified in the source documents (GAP-2486; ASM-4121).
- The read page size, 50 by default, and the read's ordering are Not specified in the source documents (GAP-2486; ASM-4121). The login phrase is "the rwb-decision login (DP-02)"; the name is Not specified in the source documents (GAP-2489; ASM-4038).

**Build steps**

1. `BookingRecordAppender` with the chain columns and the idempotency key; tests for AC1, AC7 and AC8.
2. `BookingMatchFactsBuilder` and `BookingRuleEvaluator` over the registry fixture and the kit fake; tests for AC1, AC2 and AC3, including a version not in force.
3. `BatchGate` and the account read; tests for AC5 and for an unavailable contract.
4. `BookingCandidateReader` and the grace rule over the parameter mock; tests for AC2 with grace 1 and grace 2.
5. `BookingDecisionService` for the several-account case and the difference case; tests for AC3 and AC4.
6. `BookingOutcomeDispatcher` with the booking write, the difference write, the task request and the dedupe; tests for AC2, AC3 and AC4.
7. The workflow with its six activities on queue `rwb-decision`; tests for one run per business date and the repeat of AC7.
8. `BookingDecisionController` with the rerun and the read, the scope and the two refusals; tests for AC7 and AC9.
9. The privacy test: the records, the event payloads, the logs and the read items hold treatment IDs, case IDs, dates, amounts, rates and codes only.

**Feature switch.** The legacy flag `rwb.integration.booking-confirmation` is read through DP-06. Off: the workflow does not start on `AceDataReady`, the rerun answers as unavailable, and the records already written stay readable — the exact answer with the switch off is Not specified in the source documents (GAP-2491; ASM-4125).

**Done when.** The tests of section 16 pass; a SIT week shows one record and one event per approved treatment and business date; `BOOKED` only when every account matches; `NO_BOOKING` and `TERMS_DIFFER` each with one task request and the terms on the record; no record for a date whose batch failed; `NoPackageInForce` with MSG-P3-027 for a date with no version in force; a rerun writing nothing twice; and no comparison code and no rule table in the service.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P2-011 | The task text of a missing booking | No booking for treatment {treatment} was found in the ALS load for {date}. Book it in ALS. Accounts not booked: {accounts}. | Sent as the task parameters of the request; rendered by rwb-case |
| MSG-P2-012 | The task text and the difference note of a booked term that differs | The booked {term} is {booked}. The approved {term} is {approved}. | Sent as the task and difference parameters; rendered by rwb-case |
| MSG-P1-001 | The ALS batch is late, failed or not complete | {product} is from {date}. Today's load has not arrived. | Raised by the batch answer of RWB-P2-E2007-CON and shown as it arrives |
| MSG-P3-027 | No `BOOKING_MATCH` version is in force on the business date | The {table} load was refused: {check}. The version in force is unchanged. | This story, on the run and the rerun |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the append and the read |
| MSG-P2-006 | A rerun while the run of that date is in flight | {job} is already running. Wait for it to finish before you run it again. | This story, on the rerun |
| MSG-P4-002 | A role without the right calls the rerun or the read | You cannot {action} here. Your role does not include it. | This story, through the guard of the P4 story |
| MSG-P4-003 | The treatment or the case is outside the caller's scope | This case is not in your scope. | This story, on the read |
| MSG-GEN-006 | A consumed contract is unavailable or answers beyond 2 s | Not specified in the source documents (GAP-2486; ASM-4121) | This story, on the dispatch and the gate |

For MSG-P3-027 the {check} value is "no package in force" and the {table} value names the package code "BOOKING_MATCH" and the business date only, never a case or account fact. MSG-P2-011 and MSG-P2-012 are the legacy texts copied unchanged and are rendered by the case owner, because the task is its row; this story supplies the parameters. MSG-GEN-006 is a platform message and its text is Not specified in the source documents (GAP-2486; ASM-4121); the code is used and no text is invented. Thai text for each message follows decision DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863).

### 15. Screens and states

No screen is built in this story. The decisions read feeds two existing screens through the gateway-bff composite route of DP-19: SCR-14 Treatment record, where the officer sees booked at or the booking difference with each term approved and booked, and SCR-01 My work, where the officer and the Credit Administration officer see the tasks the case owner raised from this decision. The data steward reads the same values as the REC-03 break list.

| Where | State | What the caller sees |
|---|---|---|
| The decisions read | Loading | The page skeleton; no partial item |
| The decisions read | Results | The outcome per treatment, the row ID, the package version, the difference terms, the decided time and the repeat count |
| The decisions read | Empty | "No booking decisions match this search." with the date and the outcome filter kept |
| The decisions read | Error | MSG-P7-003 when the record store cannot be read, or the refusal of the guard |
| The decisions read | Refused | 403 with MSG-P4-002 for a role without Decision log R; 404 with MSG-P4-003 for a treatment or case outside the scope |
| SCR-14 Treatment record | Approved, booking missing | The approved terms and the task; the booking fields empty (the screen is the treatment owner's) |
| SCR-14 Treatment record | Booked | Booked at and the booking reference, with the row and the version on the linked record |
| SCR-14 Treatment record | Terms differ | Each term approved and booked, from the difference terms of this record |
| SCR-29 Posting (Epic 4) | Not this story | The confirmation for all bookings is the payment epic's screen and reads no value here directly |
| SCR-01 My work | Empty, loading | As Screen Specifications v1 defines them for SCR-01 (CG-ALL-7112) |
| SCR-01 My work | Error, no access | Not specified in the source documents (CG-ALL-7112) |
| SCR-14 Treatment record | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-7113) |
| SCR-29 Posting (Epic 4) | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-7114) |

SCR-14, SCR-01 and SCR-29 are the treatment, case and payment owners' screens; this story supplies the decision values and writes no screen. The empty, loading, error and no-access states of these screens are listed in the table above from Screen Specifications v1; a state that the specification lacks is Not specified in the source documents (CG-ALL-7112, CG-ALL-7113, CG-ALL-7114). The composite path and its merge order are Not specified in the source documents (GAP-2486; ASM-4121).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-01 | AC1 (BR1, BR3, BR7, BR10); the treatment state and the route move are other slices'; BR3, BR9: `BOOKED` decided once with the row and `BKG-2026.12` on the record | Component | Settlement `TRT-SYN-0701`, account `A-0701`, 650,000.00 baht booked 2026-12-16 |
| TC-E2-007-02 | AC2 (BR5); the task row is rwb-case's; BR5: `NO_BOOKING` after the grace batch with one task request | Component | Restructure with tdr_flag false for `A-0702` |
| TC-E2-007-03 | AC3 (BR2, BR4, BR6); BR2, BR4: `TERMS_DIFFER` with 4.5000 booked against 4.2500 approved on the record | Component | Restructure `TRT-SYN-0703`, rate 4.5000 booked against 4.2500 approved |
| TC-E2-007-04 | AC4 (BR2); BR2: several accounts, one booked, the unbooked account named in the actions | Component | Accounts `A-0704` and `A-0705`, one booked |
| TC-E2-007-07 | AC2 (BR5, BR10): a booking missing on two batches gives one task request and a repeat count | Component | Booking missing on 2026-12-16 and 2026-12-17 |
| TC-E2-007-08 | AC8 (BR9): a failed record stops the decision and leaves no event and no booking write | Component | Decision log store stopped |
| TC-E2-007-09 | AC6 (BR8): no version in force is refused with MSG-P3-027 and nothing is decided | Contract | No `BOOKING_MATCH` version in force on 2026-12-17 |
| TC-E2-007-10 | AC7 (refused rerun); the right is rwb-access's: a role without platform administration is refused the rerun with MSG-P4-002 | Contract | RW-CASEOWN calls `POST /admin/jobs/{jobId}/rerun` for JOB-08 |
| TC-E2-007-11 | AC8 (BR9); Principle 5: the record and the outbox row are one transaction, so a failed append leaves nothing behind | NFR | Decision log write forced to fail on the append |
| TC-E2-007-12 | Boundary of the tables of section 12.7 (ASM-3438): each table owned there is read and written only as the section states | Component | Not specified in the source documents (ASM-3438) |
| TC-E2-007-13 | AC10 (BR12); the boundary of the owners' rows, which this service never writes | Component | Settlement `TRT-SYN-0701`, account `A-0701`; no write to the treatment, case, task, route or posting owner |
| TC-E2-007-14 | AC11 (401 and 404 of the provided operations) | Contract | Read of `businessDate=2026-12-16` with no token; `POST /admin/jobs/{jobId}/rerun` with an unknown `jobId` |
| TC-E2-007-15 | AC12 (replay of a write with the same idempotency key) | Component | Decision for `TRT-SYN-0701` and 2026-12-16 replayed with the same idempotency key |
| TC-E2-007-16 | AC13 (retry and timeout of the decision activity) | NFR | Decision activity for `TRT-SYN-0701` timed out on 2026-12-16 and retried |
| TC-P7-E2007-APP-01 | AC5 | Component | ALS load refused for 2026-12-17 |
| TC-P7-E2007-APP-02 | AC6 | Component | JOB-08 rerun for 2026-12-16 |
| TC-P7-E2007-APP-03 | AC1 | Component | Settlement `TRT-SYN-0701`, account `A-0701`, 650,000.00 baht booked 2026-12-16 |

Every legacy test case of RWB-E2-007 appears above once and in the order the Work Package fixes, with TC-E2-007-05 and -06 carried as TC-P7-E2007-APP-01 and -02 of Test Cases v9. A legacy level maps as System to Component, Access to Contract and Resilience to NFR; the no-version case is Contract because its assertion here is the refusal. The `-ITG` copies belong to RWB-ITG-E2007-ITG, which proves the same values across rwb-integration, rwb-treatment, rwb-case, rwb-payment and rwb-decision. `BKG-2026.13` and the second account set are synthetic test data built on the pattern of `BKG-2026.12` and `A-0701` to `A-0705`.

### 17. Guardrails

- No business value in code: the package code, the version label, the rows, the terms compared, the tolerance, the grace, the outcome list and the decision code are rows, parameters and reference data; only the four states of a run are fixed by design.
- No personal data in events, workflow inputs, logs, tests or prompts: the record, the event and the read hold treatment IDs, case IDs, dates, amounts, rates, codes and the row and version; no name, address, national identity number, account number, mobile number or e-mail address is written or logged.
- No cross-schema read (DP-01): `rwb_decision` reads no treatment, case, task, payment or report table, and holds no foreign key into another service.
- ACE data only through the owner's contract: the batch and the account arrive from rwb-integration and no `v_ace_*` view is read here (DP-05).
- The package decides: no comparison code, no rule table, no threshold and no tolerance in this service; the evaluator names the row and the version it used (DP-04).
- No version in force is a refusal; a missing batch is a refusal; an unavailable contract is a refusal. None of them becomes a default, an empty account set or a `NO_BOOKING`.
- The record is written before anything leaves, and no decision exists without its record; a repeat is a no-op that answers the first entry.
- An entry is never corrected in place: a correction is a new entry naming the one it corrects, and the append-only trigger refuses an UPDATE and a DELETE.
- Synthetic data only: `RW-2026-000701`, `A-0701` to `A-0705`, `TRT-SYN-0701` to `TRT-SYN-0704`, `BKG-2026.12`.
- No secret in a record, an event or the run material: the rwb-decision login (DP-02) comes from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Booking confirmed from the next day's ALS batch | Program 5.3; Epic 2 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39, R-UNI-40, R-UNI-41 | TC-E2-007-01 to TC-E2-007-04, TC-P7-E2007-APP-01, TC-P7-E2007-APP-02, TC-P7-E2007-APP-03, TC-E2-007-07 to TC-E2-007-09, TC-E2-007-11, TC-E2-007-12 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E2-007; story RWB-P7-E2007-APP; contract RWB-P2-E2007-CON; baseline `rwb_decision` | Metadata; sections 1, 3, 12 |
| Package `BOOKING_MATCH` version `BKG-2026.12`, the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht (legacy BR2, BR3, BR4, BR10) | Sections 1, 3, 7, 8, 11, 12 |
| `booking.missing.grace_loads` = 1 and the grace batches (legacy BR5) | Sections 3, 7 (AC2), 8 (BR5), 13 |
| The three outcomes and the difference terms (legacy AC1 to AC4) | Sections 7, 8, 11, 12.3 |
| The batch gate and the failed batch (legacy AC5, BR8) | Sections 4, 5 (X1), 7 (AC5), 8 (BR11) |
| The idempotency key treatment and business date (legacy AC6, AC7) | Sections 4, 5 (X4), 7 (AC7), 8 (BR10) |
| The record before the decision and MSG-P7-003 (legacy AC8, BR9) | Sections 5 (X3), 7 (AC8), 8 (BR9), 14 |
| No version in force is a refusal (legacy AC9, BR11) | Sections 5 (X2), 7 (AC6), 8 (BR8), 14 |
| The rerun operation and its refusals (legacy section 12, X5, X8) | Sections 5 (X5, X6), 12.1, 16 (TC-E2-007-10) |
| MSG-P2-011, MSG-P2-012, MSG-P1-001, MSG-P7-003, MSG-P3-027, MSG-P2-006, MSG-P4-002 | Section 14 and the exception paths |
| Field IDs DF-DEC-001 to DF-DEC-031 and DF-REF-001, 003, 008, 010, 011, 274 to 286, 298 | Section 11 |
| Synthetic values: case `RW-2026-000701`, accounts `A-0701` to `A-0705`, treatments `TRT-SYN-0701` to `TRT-SYN-0704`, dates 2026-12-15 to 2026-12-18 | Sections 3, 7, 16 |
| Legacy test cases TC-E2-007-01 to TC-E2-007-11 | Section 16 |
| The other slices of RWB-E2-007 | Sections 1, 2, 5, 19 |

The requirement text and the BRD section are those the legacy story cites; no requirement ID and no text changes. This story is the decision and record slice of RWB-E2-007 and states its boundaries in sections 1, 2, 5, 12 and 19 rather than silently widening them.

### 19. Out of scope

- The ALS batch read, the account snapshot and their exceptions: rwb-integration (RWB-P2-E2007-APP, RWB-P2-E2007-CON).
- The treatment booking state, booked at, the booking reference and the persisted booking difference: rwb-treatment.
- The task, the route state, the case move by R-RES-22 and R-SET-13 and the `CaseStateChanged` event: rwb-case.
- `TreatmentBooked` (EV-11), the posting of a settlement to ALS and SCR-29: rwb-payment and FEAT-PAY-06, Epic 4.
- Payment matching to the plan or the settlement: JOB-07 and FEAT-OCC-10, Epic 2.
- The authoring, the load checks, the four-eyes approval, the effective dating, the promotion and the rollback of `BOOKING_MATCH`: RWB-P7-E2042-APP and RWB-P7-E1073-APP.
- The append-only table, the trigger, the chain lock, the verifier, the daily seal and JOB-14: RWB-P7-E1008-APP.
- The generic ledger ingest, the record library and the decision-log reads of other decisions: RWB-P7-E1027-APP and RWB-P7-E2005-APP.
- The REC-03 report itself, the reconciliation table and the data steward's report screen: rwb-reporting (P9) and the reporting stories (GAP-2492; ASM-4126).
- The screens SCR-14, SCR-01, SCR-29, the composite route and the rights behind them: the treatment, case and payment stories, RWB-P4-E1037-CON and the Epic 8 administration stories.
- The cross-service proof of the full booking confirmation across the five services: RWB-ITG-E2007-ITG.
- The `rwb_decision` schema baseline, the topic and queue provisioning, the chart, the dashboards and the runbook of this service.
