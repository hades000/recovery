# RWB-P8-E2008-APP Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P8-E2008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P8-C |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P8-E2008-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E2004-CON, RWB-P3-E2042-CON |
| Integration dependencies | None |
| External dependencies | RWB-P8-E2008-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (FR-P8-001, FR-P8-002, FR-P8-004, FR-P8-005, FR-P8-006, FR-P8-007, FR-P8-010, FR-P8-011, FR-P8-012, FR-P8-013, FR-P8-015, FR-P8-016, FR-P8-017, FR-P8-027, FR-P8-028, FR-P8-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E2-008 for rwb-payment — payment matching against the running plans with the package `PAYMENT_MATCH` in force, the proceeds row in `rwb_payment`, the local decision record, and `ProceedsMatched` (EV-25) and `PaymentMissed` (EV-12) on `rwb.payment.events.v1` — is split from the published shapes (RWB-P8-E2008-CON) and from the deployment of the build (RWB-P8-E2008-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **payments posted in ALS and read from v_ace_payment matched to the running plans each day, with a missed payment event when a due installment has not arrived by the time the ACE batch completes**, so that **a broken plan is known the day after it breaks**.

Inside rwb-payment this is the matching half of RWB-E2-008:

- service `rwb-payment`, schema `rwb_payment`, REST base `/api/recovery/payment/v1`, topic `rwb.payment.events.v1` with event names `rwb.payment.<Event>.v1`, Temporal task queue `rwb-payment` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.payment` (R4, DP-13);
- JOB-07 as the event-started workflow `matchPayments` started by `AceDataReady` (EV-26) for the ALS source and a business date, with no Schedule and no Quartz row (DP-10);
- the evaluation of package `PAYMENT_MATCH` on the embedded Drools kit, with the version in force supplied by rwb-decision (DP-04);
- the proceeds row in `rwb_payment.proceeds`, written on the service's own Flyway sequence (DP-01, DP-15);
- one local decision record per match and per missed payment, hash-linked and written before the row changes, published on `rwb.decision-record.v1` (DP-03);
- the `ProceedsMatched` and `PaymentMissed` outbox rows written in the same transaction as the proceeds row and relayed with a CloudEvents envelope (DP-09);
- the ACE facts — payments, next installment date and batch status — read on the rwb-source-data contract or on the read-only `v_ace_*` views granted to this login (DP-05);
- `GET /proceeds` on the per-service base behind the gateway-bff composite route that serves SCR-28 (DP-19).

Not here: the published shapes and the fakes (RWB-P8-E2008-CON); the deployment, topics and runbook (RWB-P8-E2008-OPS); booking confirmation JOB-08 and `TreatmentBooked` (EV-11), which are the other story of this service; the manual and settlement matching of Epic 4; the reference-data story RWB-E2-027 (RWB-P8-E2027); the plan states `PLAN_RUNNING` and `PLAN_CURE_PERIOD` and R-RES-27, which are rwb-case (P3); and the package, its authoring and its approval, which are rwb-decision (P7).

### 2. Business rationale

Payments are matched to plans by hand today, and a missed installment is found weeks later, after the cure period has gone. ACE ingests the ALS payments and the Workbench reads them through v_ace_payment, keyed by payment_code and account_key. This story matches each payment to the plan installment it pays, keeps anything unmatched on the exception list, and raises PaymentMissed the morning after a due date passes with no payment in a completed ACE batch, which R-RES-27 and the transfer rules act on. It serves REQ-CHO-007 and REQ-CHO-009, control CTL-41 and the FSD P8 measure "receipts matched the same day" (FSD P8 A2.1).

Payment matching is package PAYMENT_MATCH under ADR-012, fixed by D-RCV-36 T10 on 16 November 2026; the EXACT, PARTIAL and WINDOW rows carry match type, amount tolerance, window, grace and partial floor as decision-table columns, and the decision log names rule R-RES-26 with the package version. Under D-RCV-60 four things move:

- **the money stays here.** `proceeds` is P8's table in `rwb_payment` and this story is its only writer (DP-01).
- **the scheduler is gone.** JOB-07 is no longer a Quartz row or a Spring Batch job: it is an event-started workflow on queue `rwb-payment`, started by `AceDataReady`, and the daily cadence comes from the bank's Airflow edge (DP-10).
- **the record is written here, first.** DP-03 replaces the central DecisionLogWriter with the local decision-record library, so the record and the proceeds row commit together or not at all — which is what legacy AC9 asks (DP-03).
- **the call graph is one hop.** The legacy in-process interfaces become REST contracts with a fake, one hop and a 2 s budget, so the story is buildable on Day 1 against the rwb-source-data, rwb-case and treatment fakes (DP-11, ADR-020).

### 3. Preconditions

- RWB-P8-E2008-CON is published: both operations on `/api/recovery/payment/v1`, the schemas `rwb.payment.TreatmentBooked.v1`, `rwb.payment.PaymentMissed.v1` and `rwb.payment.ProceedsMatched.v1`, the consumed-contract fakes, the error model and the `rwb_payment` baseline.
- RWB-PLT-E1027-CON is published with its writer fake: the library writes in the caller's transaction and stops the action when the record cannot be written (DP-03).
- RWB-PLT-E1072-CON is published: the embedded kit loads a package, evaluates a decision table and returns the row, the outputs and the package version (DP-04).
- RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and their client library are published, and the four P3 contracts the plan names are readable for their fakes. The plan scopes the legacy treatment record of RWB-E2-004 as RWB-P3-E2004-CON and the package surface of RWB-E2-042 as RWB-P3-E2042-CON, while the treatment entity is published by S2 rwb-treatment and the package by P7 rwb-decision: where the two readings part, the operation names are Not specified in the source documents (GAP-2503; ASM-4140).
- RWB-PLT-TE006-CON (outbox, inbox, relay, dedupe key), RWB-PLT-E1071-CON (event-started workflow, retry policy, visibility query), RWB-PLT-E1044-CON (Flyway sequence and drift gate) and RWB-PLT-N001-CON (gateway-bff composite route) are published.
- `proceeds` exists in `rwb_payment` with the field set of TSD P8 T3.1 (DF-FIN-001 to DF-FIN-009) and the standard record columns of TSD P8 T3.0. The legacy story's `payment_code` and its `payment_missed_event_key` are not in that field set, which carries `account_payment_id` instead; the value and the home of the payment code are Not specified in the source documents (GAP-2503; ASM-4141).
- The service runs as login `rwb_payment` on schema `rwb_payment`, holds no grant on another `rwb_*` schema, and reads `v_ace_payment`, `v_ace_account` and `v_ace_batch_status` only where the environment grants those read-only views to this login, the alternative being the rwb-source-data contract (DP-05).
- `AceDataReady` (EV-26) is published by rwb-source-data on `rwb.source-data.events.v1` with the source, the business date and the batch status.
- Package `PAYMENT_MATCH` is in force with an EXACT row: amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days (assumed in the legacy story, DL25). The values are rows of the package and never constants of this build.
- `rwb.payments.matching` is the feature flag of the platform library; off means the workflow writes its inbox row and holds the business date, writes no proceeds row and publishes no event.

### 4. Flow

1. `AceDataReady` (EV-26) arrives for the ALS source with business date D; the inbox writes its row in consumer group `rwb-payment.ace-data-ready.v1` and dedupes on the event id (DP-09).
2. The event starts `matchPayments` on queue `rwb-payment` with the source, the business date and the event id as input; the execution id is derived from the source and the date, so a rerun joins the same execution (DP-10).
3. `readFacts` checks the batch status of the ALS source for D. A status other than COMPLETE ends the run with MSG-P1-001 and writes nothing, so no missed payment is raised from stale data.
4. `readFacts` reads the payments of business date D — payment_code, account_key, payment_date, payment_amount, data_as_of — from `v_ace_payment` on the owner's contract or the granted view, and the next installment date per account from `v_ace_account` (DP-05).
5. For each payment the workflow asks rwb-case for the open case of the `account_key`; a payment on an account with no open case is listed on the REC-05 business-key break and gets no proceeds row.
6. The workflow reads the running plans of the case — installment amount, installments, installments paid, treatment type and next due date — on the treatment record contract the plan scopes as RWB-P3-E2004-CON.
7. `evaluateMatch` builds the facts of one payment against one running plan and evaluates `PAYMENT_MATCH` on the embedded kit: a payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment through the EXACT row (DP-04).
8. `recordAndApply` writes one decision record — decision code D5, rule R-RES-26, the package version of the result, the inputs reference and the answer — and only after that write succeeds writes the proceeds row, calls the treatment contract to record the installment paid and writes the `ProceedsMatched` outbox row, all in one transaction (DP-03, DP-09). A failed record write rolls the step back and the run shows MSG-P7-003.
9. A payment that matches no plan installment is written with `matched_to` UNMATCHED and appears on the exception list for the reconciliation agent (R-UNI-03).
10. After the payments, `raiseMissedPayment` walks the running plans: where the next due date plus the grace days is before the business date of the completed batch and no matched payment exists for that due date, it writes the record and the `PaymentMissed` outbox row once per plan and due date.
11. The relay publishes `ProceedsMatched` and `PaymentMissed` to `rwb.payment.events.v1`, with `rwb.payment.events.v1.retry` and `rwb.payment.events.v1.dlt` behind it, keyed on the case id and wrapped in a CloudEvents 1.0 envelope with no personal data (DP-09).
12. rwb-case consumes `PaymentMissed`, applies R-RES-27 and records the case movement for reason "payment missed". This service moves no case state and writes no case row.
13. The run closes with its summary — payments read, matched, unmatched, missed events — visible on the workflow run view to Credit Administration, on the visibility query of the kit.
14. `GET /proceeds` answers the matched and unmatched receipts on `/api/recovery/payment/v1` through the gateway-bff composite route, one hop with a 2 s budget (DP-13, DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A payment matches no plan installment | The proceeds row is written with `matched_to` UNMATCHED and appears on the exception list | MSG-P8-001 | AC7, BR3 |
| X2 | A payment is on an account with no open case | It is listed on the REC-05 business-key break; no proceeds row is written | None | BR4 |
| X3 | The ACE batch for ALS is not COMPLETE for the business date | The workflow ends before matching; no missed payment is raised from stale data | MSG-P1-001 | BR5 |
| X4 | The workflow is started twice for one business date | The second start joins the existing execution; the proceeds key and the idempotency row stop a second row and a second event | None | AC6 |
| X5 | A payment arrives on the last day of the window, or one day before it opens | The first matches the installment; the second is held UNMATCHED | MSG-P8-001 | AC7 |
| X6 | No `PAYMENT_MATCH` version is in force on the business date | The evaluation refuses with NoPackageInForce (never retried), the run stops before matching, and no proceeds row and no event are written | MSG-P3-027, MSG-P8-002 | AC8 |
| X7 | The local decision record cannot be written | The transaction writes nothing: no proceeds row, no treatment update, no outbox row | MSG-P7-003 | AC9, BR12 |
| X8 | A consumed contract does not answer inside 2 s, or its breaker is open | The activity retries on the workflow policy (1 s initial, back-off 2, 10 attempts); nothing is written until an answer arrives | None | BR9 |
| X9 | A component, a statement or a test reaches another service's schema or a view this login does not hold | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17 |

X1 to X6 are the exception paths of RWB-E2-008 carried onto the split; AC1, AC3, AC4 and AC5 of the legacy story are owned by no story of this split and their paths are traced in section 18 and not restated here. X7 is the transaction rule of DP-03, X8 the retry policy of the workflow kit, and X9 the DP-01 and DP-05 boundary. The window, the tolerance and the grace days are values of the package in force, so none of them is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-P8-E2008-CON, the platform contracts and the rwb-source-data, rwb-case and treatment fakes, on its own schema, with no live neighbour |
| Negotiable | The workflow, activity and consumer-group names and the run-summary shape are this story's choice; the rules, messages, package, events and proceeds field set are fixed |
| Valuable | A missed installment is known the morning after the due date, and the match is decided by a versioned package and recorded before the money row moves |
| Estimable | One workflow, four activities, one record writer, one row, two events, five consumed contracts and one read |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against synthetic rows in the data-product fake or the ACE view and synthetic plans in the case and treatment fakes |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching with the missed payment event

  Background:
    Given package "PAYMENT_MATCH" version "PM-2026.12" is in force with row "EXACT": amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days
    Given case "RC-2026-000555" has account "A-0555" and running restructure plan "T-0701" with installment amount 12,500.00 THB, installments 24 and installments paid 3
    Given account "A-0555" has next installment date 2026-12-15

  Scenario: AC2 Missed payment (legacy RWB-E2-008 AC2)
    Given the rwb-case contract mock returns PLAN_CURE_PERIOD for "T-0701"
    Given no payment on account "A-0555" appears in v_ace_payment between 2026-12-05 and 2026-12-15
    When JOB-07 runs on 2026-12-16 for business date 2026-12-15
    Then the system writes paymentMissed to the outbox with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00
    Then P3 moves plan "T-0701" from "PLAN_RUNNING" to "PLAN_CURE_PERIOD" under rule R-RES-27
    Then the transfer rule records the case movement for reason "payment missed"

  Scenario: AC6 Repeated run (legacy RWB-E2-008 AC6)
    Given JOB-07 completed for business date 2026-12-14 with 1 matched and 1 unmatched payment
    When JOB-07 is rerun for business date 2026-12-14 from SCR-44
    Then the proceeds table still has 2 rows for business date 2026-12-14
    Then no second ProceedsMatched or PaymentMissed is written

  Scenario: AC7 Window boundary (legacy RWB-E2-008 AC7)
    Given plan "T-0702" on account "A-0666" of case "RC-2026-000566" has installment amount 12,500.00 THB and next installment date 2026-12-16
    Given v_ace_payment holds payment "PAY-90004" of 12,500.00 THB on account "A-0555" dated 2026-12-05
    Given v_ace_payment holds payment "PAY-90005" of 12,500.00 THB on account "A-0666" dated 2026-12-05
    When JOB-07 runs on 2026-12-06
    Then "PAY-90004", 10 days before its due date, is matched to "INSTALLMENT" for "T-0701" by the EXACT row
    Then "PAY-90005", 11 days before its due date, is matched to "UNMATCHED"

  Scenario: AC8 No PAYMENT_MATCH version in force (legacy RWB-E2-008 AC8)
    Given no PAYMENT_MATCH version is IN_FORCE on 2026-12-15
    When JOB-07 starts for business date 2026-12-15
    Then the evaluation refuses with NoPackageInForce and MSG-P3-027 for package "PAYMENT_MATCH"
    Then it stops before matching with MSG-P8-002
    Then no proceeds row and no event is written
    Then the job monitor shows JOB-07 as failed with an alert to Credit Administration

  Scenario: AC9 Decision log names the rule and the package version (legacy RWB-E2-008 AC9)
    Given payment "PAY-90001" matches the installment of "T-0701" on 2026-12-15
    When JOB-07 writes the match
    Then the decision log entry holds decision code "D5", rule "R-RES-26" and rule version "PM-2026.12"
    Then the proceeds row is written only after the decision log entry succeeds
    Then the run summary counts the match under version "PM-2026.12"
```

The five criteria are those of RWB-E2-008 that this slice owns, copied word for word with the origin tag added to the `Scenario` line: the repeated `Then`, the legacy reference to JOB-07, the legacy names "decision log entry" and "job monitor" all stand. AC2 carries one added line because its last two steps are rwb-case's: `Given the rwb-case contract mock returns PLAN_CURE_PERIOD for "T-0701"`. The facts of the `Background` and of AC7 come from the rwb-case, treatment and rwb-source-data fakes or from the service's own granted views. Where the legacy text says the decision log entry, this build writes the local decision record of DP-03; where it says the job monitor, this build shows the run on the workflow visibility view. AC1, AC3, AC4 and AC5 of the legacy story belong to no story of this split (GAP-2503; ASM-4142).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A payment on the plan account for the installment amount, dated inside the window before the next due date, matches that installment | R-RES-26; row EXACT of package PAYMENT_MATCH |
| BR2 | A due date that passes, plus the grace days, with no matched payment raises PaymentMissed once | R-RES-27; REQ-CHO-007 |
| BR3 | A payment that matches no plan, sale or lot is held on the exception list for the reconciliation agent | R-UNI-03; CTL-41 |
| BR4 | A payment on an account with no open case is listed on the REC-05 business-key break and gets no proceeds row | REC-05; DQ-012 |
| BR5 | Matching runs only on a COMPLETE ACE batch; no missed payment is raised from stale data | JOB-07; CTL-02 |
| BR6 | One proceeds row per payment; one PaymentMissed per plan and due date | R-UNI-40; idempotency row of DP-09 |
| BR7 | Window, tolerance, grace days, partial floor and match types are columns of the package rows with a version | Principle 1; D-RCV-36 T10 |
| BR8 | Payments in `v_ace_payment` reconcile to proceeds by count and amount daily | REC-04 |
| BR9 | The match is decided by package PAYMENT_MATCH on the embedded kit; the result names R-RES-26 and the package version, and the local record holds both before the row changes | D-RCV-36 T5, T7; ADR-012; ADR-017; DP-03, DP-04 |
| BR10 | No PAYMENT_MATCH version in force is a refusal, never a default match | R-UNI-41; D-RCV-36 T7 |
| BR11 | The proceeds row is written in `rwb_payment` only; `recovery_case`, the route state and the assignment are rwb-case's and are answered, never written | DP-01; Ownership Map (`proceeds` P8, `recovery_case` P3) |
| BR12 | The proceeds row, the treatment update, the record and the outbox row commit together or not at all; a failed record write changes nothing and answers MSG-P7-003 | DP-03; legacy AC9 |
| BR13 | The same business date twice writes once and publishes once; the execution id, the proceeds key and the idempotency row carry the rule | Legacy AC6; DP-09, DP-10 |

### 9. State transitions

None of the case. The legacy story says so, and this slice keeps it: the states here are the match state of the proceeds row and the execution state of the workflow. `PLAN_RUNNING` and `PLAN_CURE_PERIOD` belong to rwb-case and are named only as the answer `PaymentMissed` produces under R-RES-27.

| From (`proceeds.matched_to`) | Event | Condition | To |
|---|---|---|---|
| Not existing | `PAYMENT_MATCHED` | The EXACT row fires on the plan account inside the window | INSTALLMENT, with the treatment update and the `ProceedsMatched` outbox row |
| Not existing | `PAYMENT_HELD` | No package row fires, or the amount or date falls outside the window | UNMATCHED, with the exception-list entry |
| Not existing | `PAYMENT_NO_CASE` | The `account_key` has no open case | No row; the REC-05 break lists the payment |
| Any | The same business date again | AC6, X4 | Unchanged; the repeat is counted |

The `matched_to` values are those of LOV-MATCH in TSD P8 T3.2 (INSTALLMENT, SETTLEMENT, FEE, SALE_PROCEEDS, UNMATCHED); this story writes INSTALLMENT and UNMATCHED only, and the other three belong to the Epic 4 stories of this service.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery service identity of rwb-payment (`rwb_payment`) | Runs the workflow and its activities, evaluates the package, reads the ACE facts on the contract or the granted views, writes the proceeds row, the record and the outbox, and calls the neighbours; holds no grant on another `rwb_*` schema |
| SY-RULES, the embedded Drools kit | Evaluates package PAYMENT_MATCH for each payment and returns the row, the outputs and the package version (DP-04) |
| SY-CASEWF, case workflow module | Consumes PaymentMissed and ProceedsMatched and applies R-RES-27 and the transfer rule on the case of record |
| The local decision-record library (RWB-PLT-E1027-CON) | Writes the match and the missed-payment record in the caller's transaction and publishes `DecisionRecorded` on `rwb.decision-record.v1` (DP-03) |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent, right R in Write-off and posting |
| RW-CREDITAD, Credit Administration officer | Reads matched and unmatched receipts on SCR-28 and the failed runs of JOB-07, right CRUA in Write-off and posting |
| RW-CASEOWN, case owner | Reads the plan position on SCR-14, right R in Treatment and offer |
| RW-COE, center of excellence analyst | Owns package PAYMENT_MATCH and loads a new version through the authoring route of rwb-decision; this story only evaluates the package in force |

The rights are the rows of TSD P8 T6.1 and of the legacy authority table, and nothing wider. The run is unattended: no officer task sits on the happy path, and the step runs under the service identity of the service.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-ACE-043, DF-ACE-044, DF-ACE-045, DF-ACE-046, DF-ACE-054 | `v_ace_payment` (P1) | payment_code, account_key, payment_date, payment_amount, data_as_of | Read, on the owner's contract or the granted view |
| DF-ACE-028 | `v_ace_account` (P1) | next_installment_date | Read |
| DF-ACE-178, DF-ACE-179, DF-ACE-182 | `v_ace_batch_status` (P1) | source_system, business_date, status | Read |
| DF-CAS-025, DF-CAS-026 | `case_account` (P3) | case_id, account_key | Not read as a table; the open case arrives on the rwb-case contract |
| DF-TRT-001, DF-TRT-004, DF-TRT-009, DF-TRT-031 | treatment record (contract the plan scopes as RWB-P3-E2004-CON) | id, treatment_type, installments, installment_amount | Read on the contract |
| DF-TRT-032 | treatment record | installments_paid | Write, on the contract and never as a table write |
| DF-FIN-001 to DF-FIN-009 | `proceeds` (P8, `rwb_payment`) | id, case_id, treatment_id, account_payment_id, source, amount, received_date, matched_to, posting_ref | Write, this story's own row |
| DF-REF-002, DF-REF-003, DF-REF-296, DF-REF-297, DF-REF-298 | `rule_row` (P7) | rule_id, rule_version, package_version_id, drools_rule_name, outputs | Read only through the evaluation result of the kit; no `drl_source` and no workbook |
| DF-DEC-004, DF-DEC-005 | decision record (PLT library, created in `rwb_payment`) | rule_id, rule_version | Write through the local library, before the row changes |
| DF-OPS-118 to DF-OPS-129 | reconciliation result (REC-04) | all fields | Write on the run summary of the workflow |

Field IDs are those of the Logical Data Model and Data Dictionary and of TSD P8 T3.1. DF-REF-261 to DF-REF-273 were the `payment_match_rule` fields and are retired by D-RCV-36 (T10); they are not in Physical Schema v6 and no story reads or writes them.

The legacy `payment_code` and `payment_missed_event_key` have no column in the TSD field set, which carries `account_payment_id` (DF-FIN-004) instead: their value and home are Not specified in the source documents (GAP-2503; ASM-4141). No new table of business data is added: `proceeds` arrives with the CON baseline, and `decision_record`, `inbox_event`, `outbox_event` and `idempotency_key` are library objects created in `rwb_payment` by the library's own migration (DP-03, DP-09, DP-15). No personal data is written: identifiers, codes, amounts, dates and a rule version only, and no name, address, contact value or identity number enters the schema, the record, an event, a workflow input or a log.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8), base `/api/recovery/payment/v1` (DP-13). The published shape, the error model and the fakes are RWB-P8-E2008-CON; this story supplies the behaviour.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | API-P8-001: a page of receipts with their match status, filtered by `matched`, `from`, `to`, `page` and `size` | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | API-P8-002: a manual match of a receipt to a case and account, body `MatchRequest`, response `Proceeds` | Write-off and posting, right U, scope applied | `Idempotency-Key` header |

`GET /proceeds` is the read this story's criteria use; the manual match is declared by the CON baseline and built by the Epic 4 stories of this service, and neither operation is redeclared here. Architecture v5 lists `GET /cases/{id}/payments` among the IN operations of rwb-payment and the Ownership Map carries no row for it: the case payment list is answered through `GET /proceeds` with the case scope applied, and the extra operation is not published by this story (GAP-2503; ASM-4140).

#### 12.2 REST operations consumed

| Operation | Base / contract | Owner | Use |
|---|---|---|---|
| The payments of the business date (operation name Not specified in the source documents (GAP-2503; ASM-4140)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | payment_code, account_key, payment_date, payment_amount, data_as_of of business date D; faked, or the granted `v_ace_payment` view (DP-05) |
| The next installment date of an account (name Not specified in the source documents (GAP-2503; ASM-4140)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | `next_installment_date` at the same business date; faked, or the granted view |
| The batch status of the ALS source (name Not specified in the source documents (GAP-2503; ASM-4140)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | source_system, business_date, status; faked, or the granted view |
| The open case of an account (name Not specified in the source documents (GAP-2503; ASM-4140)) | `/api/recovery/case/v1` | P3 rwb-case | the case id of an `account_key`, absent where the account is on no open case; faked |
| The running plans of a case (name Not specified in the source documents (GAP-2503; ASM-4140)) | RWB-P3-E2004-CON | P3 as the plan scopes it; the entity is published by S2 rwb-treatment | installment amount, installments, installments paid, treatment type, next due date; faked |
| `recordInstallmentPaid` (name Not specified in the source documents (GAP-2503; ASM-4140)) | RWB-P3-E2004-CON | P3 as the plan scopes it; S2 publishes the entity | treatment id, proceeds id, due date, amount; faked |
| The parameters of the run (name Not specified in the source documents (GAP-2503; ASM-4140)) | RWB-P3-E1042-CON | P3 rwb-case | the flag and the run window keys; faked |
| The lists of the run (name Not specified in the source documents (GAP-2503; ASM-4140)) | RWB-P3-E1043-CON | P3 rwb-case | LOV-MATCH and LOV-PROCEEDS-SRC; faked |
| The package in force (name Not specified in the source documents (GAP-2503; ASM-4140)) | RWB-P3-E2042-CON | P3 as the plan scopes it; the package is published by P7 rwb-decision | package code `PAYMENT_MATCH`, the version in force and its rows; the evaluation itself runs on the embedded kit (DP-04) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020, DP-11).

#### 12.3 Events published

| Event | Topic | Trigger | Payload used |
|---|---|---|---|
| `ProceedsMatched` (EV-25), `rwb.payment.ProceedsMatched.v1` | `rwb.payment.events.v1`, with `.retry` and `.dlt` | The match commits: proceedsId, caseId, amount, and the matched treatment and business date where the envelope allows (GAP-2503; ASM-4143) | CloudEvents 1.0, key caseId, no personal data |
| `PaymentMissed` (EV-12), `rwb.payment.PaymentMissed.v1` | the same topic and its retry and DLT topics | The missed-payment step commits: treatmentId, dueDate, amountDue (GAP-2503; ASM-4143) | CloudEvents 1.0, key caseId, no personal data |

`TreatmentBooked` (EV-11) is the third event of this topic and belongs to the booking story of this service; this story publishes no `TreatmentBooked`. `DecisionRecorded` is written by the local library to this service's outbox on the shared topic `rwb.decision-record.v1`, whose owner is rwb-decision (DP-03). Each outbox row is written in the same transaction as the proceeds row, and the relay publishes it (DP-09).

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When |
|---|---|---|---|---|
| `AceDataReady` (EV-26), `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | `rwb-payment.ace-data-ready.v1` | the source, the business date and the batch status; starts `matchPayments` | on the relay of rwb-source-data, deduped in `inbox_event` |
| `DecisionRecorded` (EV-08) | `rwb.decision-record.v1` | none | produced by this service's library and consumed by rwb-decision and rwb-reporting; this service subscribes to none of its own records | named only |

The other subscriptions of the service — `TreatmentApproved` (EV-10), `LotAwarded` (EV-23), `AssetTakenOn` (EV-22), `AssetSold`, `WriteOffApproved` (EV-24) and `RulePackageInForce` (EV-30) — serve the booking and Epic 4 stories of the service and are registered by the CON and OPS stories. This story's workflow consumes `AceDataReady` only.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `matchPayments` (JOB-07; name Not specified in the source documents (GAP-2503; ASM-4139)) | Workflow, one execution per source and business date, event-started by `AceDataReady` | `rwb-payment`, namespace `rwb-recovery` | input: source, business date, event id; the execution id is derived so a rerun joins it |
| `readFacts` (name as above) | Activity | `rwb-payment` | the batch check, the payments, the next installment dates and the running plans in; the facts and the freshness stamp out |
| `evaluateMatch` (name as above) | Activity | `rwb-payment` | the facts in; the row, the outputs and the package version out, or `NoPackageInForce` (not retried) |
| `recordAndApply` (name as above) | Activity | `rwb-payment` | the record, the proceeds row, the treatment update, the outbox row and the inbox row in one transaction |
| `raiseMissedPayment` (name as above) | Activity | `rwb-payment` | the plans and the business date in; the record and the `PaymentMissed` outbox row out, once per plan and due date |

`confirmBookings` (JOB-08) and `postProceeds` (the debt-sale saga step) are the other activities the architecture lists for this queue; they belong to the booking story and to RWB-P8-E4044 and the debt-sale journey, and neither is built here. The five names are a design choice of this story: the sources name JOB-07 and the queue, and no source names the workflow or its activities (GAP-2503; ASM-4139).

#### 12.6 Schedules

None. JOB-07 is an event-started workflow and not a Temporal Schedule; the daily cadence is delivered by the bank's Airflow edge, which runs the ACE ingestion and signals `AceDataReady`. This service owns no cron, no overlap policy and no catch-up window for it. The outbox relay runs as a library component in every service and is not a Schedule of this one.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `proceeds` | P8 (`rwb_payment`) | The receipt of a case and what it was matched to; this story writes INSTALLMENT and UNMATCHED rows and reads them back for `GET /proceeds` |
| `decision_record` | PLT library, created in `rwb_payment` | The local hash-linked record, one per match and one per missed payment (DP-03) |
| `inbox_event` | PLT library, created in `rwb_payment` | The `AceDataReady` row and its dedupe key (DP-09) |
| `outbox_event` | PLT library, created in `rwb_payment` | The `ProceedsMatched`, `PaymentMissed` and `DecisionRecorded` rows and the relay cursor (DP-09) |
| `idempotency_key` | PLT library, created in `rwb_payment` | The per-payment and per-due-date keys that make a rerun write once (DP-09) |
| `payment_missed_event_key` | Not created | The legacy story's own key table is replaced by `idempotency_key`; the value and home of the key are Not specified in the source documents (GAP-2503; ASM-4141) |

Never read as a table: `recovery_case`, `case_account`, `assignment`, `task` and `timer` (P3), the treatment record, `rule_row`, `rule_package` and `rule_package_version` (P7), `account_payment` (S6), every `v_ace_*` view (P1, and this login holds three of them only where the environment grants them) and `notification` (P6). No foreign key leaves the schema: `case_id`, `treatment_id` and `account_payment_id` are identifiers, not cross-schema keys (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment OpenAPI fake | `GET /proceeds` returning a page of matched and unmatched receipts; `POST /proceeds/{proceedsId}/match` accepted, refused with MSG-P4-002 and refused on a replayed `Idempotency-Key` | AC7, AC9 |
| rwb-source-data payments fake | the payments of 2026-12-14 and 2026-12-05 with `data_as_of`, the next installment date of `A-0555` and `A-0666`, and a batch status COMPLETE, FAILED and absent | AC2, AC7, X3 |
| rwb-case open-case fake | case `RC-2026-000555` for `A-0555`, case `RC-2026-000566` for `A-0666`, no case for `A-0999` | AC2, AC7, BR4 |
| rwb-case plan fake | the running plans of the case: 12,500.00 THB, installments 24, paid 3, next due 2026-12-15, and plan `T-0702` due 2026-12-16 | AC2, AC7 |
| rwb-case state fake | the answer `PLAN_CURE_PERIOD` for `T-0701` under R-RES-27 and the case movement for reason "payment missed" | AC2 |
| rwb-decision package fake | `PAYMENT_MATCH` at version PM-2026.12 with the EXACT row of the `Background`, a second version, and no version in force | AC7, AC8, AC9 |
| `AceDataReady` fake | the ALS business date 2026-12-14 and 2026-12-15 with COMPLETE and FAILED batches, and the same event twice | AC2, AC6, AC8 |
| Local decision-record library stub | a healthy chain returning the sequence and the entry hash, and a stopped chain returning MSG-P7-003 | AC9, X7 |
| gateway-bff composite route fake | the merged SCR-28 answer for case `RC-2026-000555`, with the receipts of this service read once | AC7, AC9 |

The fakes are test-only and are replaced by the real services in SIT. The consumed operation names are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2503; ASM-4140).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 9 consumed | the two operations on `/api/recovery/payment/v1`; three rwb-source-data reads, two rwb-case reads, two treatment-record calls, the parameters and lists reads and the rwb-decision package read; one hop, 2 s |
| Kafka | 3 published, 1 consumed here | `ProceedsMatched`, `PaymentMissed` and the library's `DecisionRecorded` on `rwb.payment.events.v1` and `rwb.decision-record.v1`; `AceDataReady` consumed; the service's other six subscriptions are registered elsewhere |
| Temporal | 1 workflow, 4 activities | `matchPayments` with `readFacts`, `evaluateMatch`, `recordAndApply` and `raiseMissedPayment` on `rwb-payment`; no Schedule |
| File | None | no file is read, built or delivered here; the posting file is the Epic 4 posting story's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `matching`; front end `src/modules/recovery/payment/ProceedsMatching.tsx`, the fragment SCR-28 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>`, recovery schema | Owner's schema `rwb_payment`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/payment/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-06 and DP-07 are the parameters and the two LOV sets the story reads, and no value of the package ever becomes a constant, because the window, the tolerance and the grace days live in the rows of DP-04. DP-15 is the service's own Flyway sequence: the migration takes the next number of `rwb_payment` and is not the monolith's `V2_008__payment_matching.sql`, whose name is Not specified for this service (GAP-2503; ASM-4141). DP-04 adds the C row RWB-P7-E1073-CON that the plan's C column does not carry; the story builds against the published package document and its fake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `matchPayments` | Workflow | JOB-07: waits for the business date, loads the package in force, runs the steps and reports the run summary |
| `readFacts` | Activity | the batch check, the payment read, the next installment dates and the running plans, with the freshness stamp |
| `PaymentMatchFacts` | Fact builder | installment amount, next due date, payment date, payment amount and treatment type, in the shape the package expects |
| `evaluateMatch` | Activity | one payment against one running plan on the embedded kit (DP-04) |
| `recordAndApply` | Activity | the one transaction: record, proceeds row, treatment update, outbox row and inbox row (DP-03, DP-09) |
| `raiseMissedPayment` | Activity | BR2 at the grace boundary, one record and one `PaymentMissed` per plan and due date |
| `ProceedsController` | Controller | `GET /proceeds` on the per-service base (DP-13) |

**Build steps.** (1) Take the CON baseline and the migration; test the keys. (2) Confirm the PAYMENT_MATCH version and its EXACT row in SIT through the fakes. (3) Build `PaymentMatchFacts` and `evaluateMatch`; test AC7 and AC9. (4) Build `raiseMissedPayment`; test AC2 and the grace boundary. (5) Build the workflow with the REC-05 path, the no-package path and the run summary; test AC6 and AC8. (6) Build `ProceedsController` for the SCR-28 skeleton and the access test. **Done when** the tests of section 16 pass and a synthetic month shows every payment in `v_ace_payment` as a proceeds row or a held exception, with R-RES-26 and the package version on every match record.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | Run summary with unmatched payments | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P8-002 | No PAYMENT_MATCH version in force | Payment matching for {date} did not run: no matching rule is in force. |
| MSG-P3-027 | No PAYMENT_MATCH version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P1-001 | The ACE batch is late or not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | The role lacks Write-off and posting R | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "PAYMENT_MATCH" and the business date only, never a payment or an account fact.

### 15. Screens and states

SCR-28 Proceeds matching (skeleton in E2; states Loading, matched, unmatched) lists receipts from `GET /proceeds` for the Credit Administration officer, filtered by matched or unmatched, and reaches the service through the gateway-bff composite route (DP-19). The case owner sees the plan position on SCR-14 Treatment record and the missed payment on SCR-04 Case timeline; SCR-44 shows the JOB-07 run summary from the workflow visibility query. No screen is built here beyond the fragment the CON baseline publishes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-008-02 | AC2, BR2 | Component | no payment on `A-0555` between 2026-12-05 and 2026-12-15 |
| TC-E2-008-06 | AC6, BR6, BR13 | End to end | JOB-07 rerun for 2026-12-14 |
| TC-E2-008-07 | AC7, BR1, BR7 | Component | `PAY-90004` 10 days and `PAY-90005` 11 days before their due dates |
| TC-E2-008-08 | AC8, BR10 | Component | no PAYMENT_MATCH version in force on 2026-12-15 |
| TC-E2-008-09 | AC9, BR9, BR12 | Component | `PAY-90001` matched under version PM-2026.12 |

The five are the legacy test cases of the criteria this story owns, with the legacy Level "System" mapped to the levels of the template; the full Given, When and Then stay in Recovery Workbench Test Cases v7.xlsx under the same ID. TC-E2-008-01, -03, -04, -05 and -10 cover AC1, AC3, AC4, AC5 and the access check, which no story of this split owns: they are not copied here and stay with their legacy owner (GAP-2503; ASM-4142). Integration copies of these IDs end in `-ITG` and belong to RWB-ITG-E2008-ITG.

### 17. Guardrails

- No business value in code: the window, the tolerance, the grace days, the partial floor and the match types are columns of the rows of package PAYMENT_MATCH; the LOV values are reference data of RWB-P3-E1043-CON.
- No personal data in logs, tests, workflow history or prompts: payments are identified by payment_code and account_key, and account numbers are never logged.
- No read of another service's tables: ACE data only on the rwb-source-data contract or through the granted `v_ace_*` views, and case, treatment and package facts only on their owners' contracts.
- Amounts use BigDecimal with scale 2 and are compared exactly; no float, no rounding rule of this story.
- Nothing of the package is read from a workbook or a `drl_source`: the package is evaluated in force, and the version on the record is the one the kit returned.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-008-02, TC-E2-008-06 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40 | TC-E2-008-07, TC-E2-008-08, TC-E2-008-09 |

Legacy AC1, AC3, AC4, AC5 and TC-E2-008-01, -03, -04, -05, -10 are owned by no story of this split and are not restated here (GAP-2503; ASM-4142); their requirement rows stay in the RTM against the legacy key. The legacy story and this file are linked one way: the legacy key is carried in the metadata and in every `Scenario` tag.

### 19. Out of scope

- Partial payments and late payments inside a window after the due date (RWB-E2-027, RWB-P8-E2027).
- Settlement, auction and enforcement proceeds (FEAT-PAY-03, FEAT-PAY-04; Epic 4).
- Manual matching of an unmatched receipt (`POST /proceeds/{proceedsId}/match`, Epic 4).
- The cure period and the broken-plan rules R-RES-28 to R-RES-31 (rwb-treatment and rwb-case).
- Booking confirmation JOB-08, `TreatmentBooked` (EV-11) and the posting file — the other stories of this service and the debt-sale journey.
- Authoring, approval and rollback of package PAYMENT_MATCH (rwb-decision), the published contract shapes and the fakes (RWB-P8-E2008-CON), and the deployment of the build (RWB-P8-E2008-OPS).
