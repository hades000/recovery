# RWB-S2-E2008-APP Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the S2 rwb-treatment slice of legacy RWB-E2-008 is split out of the payment key. The matching engine, the `proceeds` row, the exception list, the `PAYMENT_MATCH` evaluation, JOB-07 and the two events stay with rwb-payment (P8) in `RWB-P8-E2008-APP` and its contract `RWB-P8-E2008-CON`; the `v_ace_payment` and `v_ace_account` reads stay with rwb-source-data (P1). This story delivers only the treatment side of a match and of a miss: the running plan of `rwb_treatment` advanced by the matched installment, the missed installment held on the plan position, the local decision record, the reads of the parameters and lists of rwb-case at their version, the plan-position read on `/api/recovery/treatment/v1` and SCR-14 through the gateway-bff composite route. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S2-E2008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (29 resolved, 58 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-S2-D |
| Ready to start | Day 1 |
| Open decisions | Open decision DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863); each has an assumption and the decision is still open |
| Size | Not specified in the source documents (DOR-RWB-S2-E2008-APP-16); the squad sizes the story at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P8-E2008-CON, RWB-P3-E1043-CON |
| Contract fake library version | Not specified in the source documents (DOR-RWB-S2-E2008-APP-22) |
| Contract version built against | Not specified in the source documents (DOR-RWB-S2-E2008-APP-23); API path /api/recovery/treatment/v1 only |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (FR-S2-024) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the installment a payment matched recorded on the running plan and above all the missed installment held on the treatment record the same morning the match runs**, so that **the plan position on the case is true — the customer is a payment further ahead, or a payment behind and visible — without a person matching receipts to a schedule by hand**. That is the plan half of the legacy intent, "so that a broken plan is known the day after it breaks".

This is the secondary slice of legacy RWB-E2-008. The legacy story owns the matching of payments to plans, the exception list, the missed-payment event and JOB-07, and every one of its ten acceptance criteria is owned by `RWB-P8-E2008-APP` and by the contract `RWB-P8-E2008-CON`, not here. This story owns no legacy criterion and invents none of its values: it tests only what a match and a miss do to the plan, and it takes the plan, the account, the case, the payment codes, the amounts, the dates, the counts, the rule IDs and the package version it uses from the legacy story character for character. Its criteria are therefore new under D-RCV-60 (ASM-4451).

What this story owns:

- the treatment side of the match: `installments_paid` (DF-TRT-032) advanced by one for the installment the event reports, and the plan position — the next due date and the missed installment of the earliest unpaid due date — read from `first_due_date` (DF-TRT-029), `installments` (DF-TRT-009), `installment_amount` (DF-TRT-031) and `installments_paid` (DF-TRT-032) on the `treatment` row of `rwb_treatment` (DP-01, DP-15);
- the subscription to `rwb.payment.ProceedsMatched.v1` (EV-25) and `rwb.payment.PaymentMissed.v1` (EV-12) on `rwb.payment.events.v1` through this service's own consumer groups and inbox, so a redelivery acts once (DP-09);
- `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, started by the consumed event and not by a Quartz row or a polled table, with its `applyProceedsMatched`, `holdMissedInstallment` and `RecordAndApply` activities (DP-10);
- the local decision record of the plan change, written through the RWB-PLT-E1027-CON library in the same `rwb_treatment` transaction (DP-03);
- the evaluation of the plan-position rule with the embedded Drools kit, naming rule R-RES-26 on a match and R-RES-27 on a miss with the package version the result returns (DP-04);
- the reads of the parameters and the reference data of rwb-case at their version (DP-06, DP-07), one hop with a 2 s budget against a fake (DP-11);
- the plan-position read on base `/api/recovery/treatment/v1` (DP-13) and on SCR-14 through the gateway-bff composite route (DP-19).

Not here: the match, the exception list, the `proceeds` table, JOB-07 and the production of the two events (P8, `RWB-P8-E2008-APP` and `RWB-P8-E2008-CON`); the ACE reads that feed the match (P1); the packages and their approval (P7); the shortfall, the break count and the closure of a broken plan (`RWB-S2-E2027-APP`, `RWB-S2-E3011-APP`); the treatment record, offer, approval and booking (`RWB-S2-E3001-APP` to `RWB-S2-E3010-APP`); the case status, `CaseWorkflow`, the assignment and the tasks (P3).

### 2. Business rationale

Payments are matched to plans by hand today, and a missed installment is found weeks later, after the cure period has gone. That gap was measured in the legacy story and it has not moved: the Workbench measures receipts matched the same day (FSD P8 measure, CTL-41) and the restructure turnaround (FSD S2 A2.10), and neither can be measured while the plan on the case is stale. REQ-CHO-007 and REQ-CHO-009 name the two halves of the answer, and this story answers them where the plan lives.

What D-RCV-60 changes is who owns which half. The payment facts, the matching decision, the proceeds row and the missed-payment event are a payment capability and stay with rwb-payment (Architecture v5 slides 3, 17 and 41). The plan is a treatment: `installments`, `first_due_date`, `installment_amount` and `installments_paid` are columns of `treatment` in `rwb_treatment`, and the plan states are the RESTRUCTURE states of TSD S2 T4 (`R-RES-25` sets `PLAN_RUNNING`). Nothing else in the target holds a plan, so nothing else can advance it or show it behind.

Three design consequences follow, and each is designed rather than left to discipline.

- **The plan is written once, by its owner.** rwb-payment reports a match; rwb-treatment applies it to its own row, and no service reads a plan out of a payment or a case table (DP-01).
- **The event is the contract, not a call chain.** The match and the miss arrive on `rwb.payment.events.v1` through the inbox, as the design shows the missed payment reaching `TreatmentWorkflow`; one delivery acts once (DP-09; Temporal and Drools Design slide 9).
- **Every change carries its record and its version.** The plan change, the record naming R-RES-26 or R-RES-27 with the package version, and the inbox row are one transaction, and nothing is polled or scheduled here (DP-03, DP-04, DP-10).

It serves REQ-CHO-007 ("plan timers run from the treatment; a missed payment raises an event") and REQ-CHO-009 ("payments matched to the plan") on the treatment side. No business value is invented or moved: the plan, the amounts, the dates, the counts, the package version and the rule IDs are the ones the legacy story and the design already carry.

### 3. Preconditions

- `RWB-P8-E2008-CON` is published: the `rwb.payment.ProceedsMatched.v1`, `rwb.payment.PaymentMissed.v1` and `rwb.payment.TreatmentBooked.v1` schemas of `rwb.payment.events.v1`, their CloudEvents envelope, and the fakes of the consumed contract, all one hop and no call chain (DP-11). This story builds against the contract and its fake on Day 1 and never against a `proceeds` row.
- `rwb.payment.ProceedsMatched.v1` (EV-25) and `rwb.payment.PaymentMissed.v1` (EV-12) carry the case ID, the treatment ID, the payment code, the amount, the due date and the business date, and no personal data; the topics carry `.retry` and `.dlt` behind them (Architecture v5 slide 42).
- `rwb_treatment` and its login exist from the platform database story, and this service's Flyway sequence is at the version that carries the library tables; this story adds its write key and its index on the same sequence and never edits an applied migration (DP-15).
- `treatment` exists in `rwb_treatment` with the columns of TSD S2 T3.1 (DF-TRT-001 to DF-TRT-033) and the standard record columns of T3.0, including `state` and the list LOV-TRT-OUTCOME; the record and its plan terms arrive with `RWB-S2-E3001-APP` and `RWB-S2-E3004-APP`.
- A restructure plan is in force for the case, booked, with `installments` 24, `installment_amount` 12,500.00 THB, `first_due_date` 2026-12-15 and `installments_paid` 3 — the values the legacy story carries.
- The workflow kit is in place on task queue `rwb-treatment` in namespace `rwb-recovery`, and the parent `CaseWorkflow` of rwb-case routes the match and the miss to this stage (Temporal and Drools Design slide 9).
- The local decision-record library `RWB-PLT-E1027-CON` is published: it writes in the caller's transaction and refuses with MSG-P7-003 when the record cannot be written (DP-03).
- The parameters and reference-data client libraries of rwb-case are published (`RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`): the plan-check values and the list values are read at their version and no member of a list is written in code (DP-06, DP-07).
- The package version in force is announced on `rwb.decision.RulePackageInForce.v1` (EV-30); the packages, their rows and their approval are rwb-decision's, and the embedded Drools runtime is the service template's (DP-04).
- The amounts are BigDecimal with scale 2 and are compared exactly (legacy guardrail); no amount, date or count is a constant of this build.
- No approval is needed to build against a Draft contract baseline: a CON dependency never blocks, and this story starts on Day 1 with only `RWB-P8-E2008-CON` as a contract dependency (ASM-4456).

### 4. Flow

1. rwb-payment matches the payments of business date D to the running plans and, in one transaction, writes the `proceeds` row and the `ProceedsMatched` outbox row, or — for a due date that passed with no matched payment — the `PaymentMissed` outbox row; its relay publishes to `rwb.payment.events.v1` with the case ID as the key (Architecture v5 slide 42; Temporal and Drools Design slide 9).
2. This service's consumer group reads the event, the inbox records the cloud event ID in its consumer group, and a redelivery is dropped before any work is done (DP-09). A signal carries the case ID, the treatment ID, the payment code, the amount, the due date and the business date to the running `TreatmentWorkflow`.
3. `TreatmentWorkflow` resolves the treatment of the event from its own row and checks that it is a treatment with a plan — `installment_amount` and `first_due_date` non-null. A settlement, a deed in lieu or any treatment without a schedule ends the step and writes nothing, because there is no installment to advance or to miss.
4. On `ProceedsMatched`, `applyProceedsMatched` builds the plan facts — the due date of the event, the installment amount, `installments_paid` and the schedule position — and asks the embedded Drools kit for the plan-position rule of the RESTRUCTURE package version in force on the business date (DP-04).
5. The result names the plan-position rule R-RES-26 and the package version, which agree with the rule ID and the version the event carries; the step then advances `installments_paid` by one for that due date and moves the plan position to the next unpaid due date.
6. On `PaymentMissed`, `holdMissedInstallment` does the same evaluation for a miss: the result names rule R-RES-27, and the step holds the missed installment on the plan position — the earliest unpaid due date and the amount due of the event — without changing `installments_paid` and without moving the plan state.
7. `RecordAndApply` writes, in one `rwb_treatment` transaction, the `treatment` row, the local decision record with the rule ID, the package version, the payment code and the due date, and the inbox completion (DP-03); a failed record write rolls the step back with MSG-P7-003 and nothing changes.
8. The activity returns the stage outcome to the parent `CaseWorkflow` — the rule ID, the package version, the plan position and the treatment ID. The parent moves the case status and, on a miss, applies its own cure-period rule; this service writes no case row (DP-01).
9. A repeated delivery of the same cloud event ID, or a second payment code against a due date already advanced, writes no second change and no second record: the inbox row and the write key carry the rule (X4, AC3).
10. SCR-14 Treatment record reads the plan position through the gateway-bff composite route, which composes the case read of rwb-case with this service's treatment read, one hop each; the browser calls no owner service directly and the screen writes nothing (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The event names a treatment with no plan — a settlement or a deed in lieu | The step ends and writes nothing; there is no installment to advance or to miss | None | AC4 |
| X2 | The inbox sees a cloud event ID it has already processed | The delivery is dropped before any activity runs; one change and one record exist | None | AC3 |
| X3 | The local decision record cannot be written | The transaction writes nothing: no plan change, no record, no inbox completion; the event is redelivered under the same ID | MSG-P7-003 | AC5 |
| X4 | A plan advance would be written twice — a redelivery, or the same due date twice | The write key refuses the second write and changes nothing | None | AC3 |
| X5 | The parameters or the reference-data read does not answer inside the budget, or its breaker is open | Nothing is written; the activity retries on the workflow policy of 1 s initial interval, back-off 2, 10 attempts | MSG-GEN-006 | AC8, AC12 |
| X6 | A component, a statement or a test reaches a payment, proceeds, rule, case or timer table | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | AC9, AC13 |

X1 to X4 are the paths this slice adds to the legacy story's own; X5 is the retry policy of the workflow kit on the two reads of rwb-case, and X6 the DP-01 and DP-05 boundary. The legacy exception paths X1 to X6 of RWB-E2-008 (unmatched payment, no open case, incomplete batch, repeated run, window boundary, no package in force) are rwb-payment's and are traced, not restated, in section 18.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-P8-E2008-CON` and its event and contract fakes, the record-writer fake, the parameters and list fakes and the composite-route fake; needs no live rwb-payment, rwb-decision or rwb-case |
| Negotiable | The activity names, the consumer-group names, the write key and the flag name are this story's choice; the rules, the plan states, the list values, the messages and the package version are fixed |
| Valuable | The plan on the case is true the same morning: a payment further ahead, or a missed installment visible before the cure period runs out |
| Estimable | One stage branch, two activities, two consumers with an inbox, one repository, one migration, one library adapter and one read |
| Small | Fits two weeks with its tests, as a secondary slice of the legacy key |
| Testable | Each of the seven criteria of section 7 is one automated test; the payment service, the package and the parent are stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching with the missed payment event — the plan position on the treatment record

  Background:
    Given package "PAYMENT_MATCH" version "PM-2026.12" is in force with row "EXACT": amount tolerance 0 percent, window 10 days before the due date and 0 days after, grace 0 days
    Given case "RC-2026-000555" has account "A-0555" and running restructure plan "T-0701" with installment amount 12,500.00 THB, installments 24 and installments paid 3
    Given account "A-0555" has next installment date 2026-12-15

  Scenario: AC1 The matched installment advances the plan (new, D-RCV-60)
    Given the rwb-payment contract mock returns proceedsMatched for case "RC-2026-000555", treatment "T-0701", payment code "PAY-90001", amount 12,500.00, due date 2026-12-15, rule "R-RES-26" and package version "PM-2026.12"
    When TreatmentWorkflow consumes rwb.payment.ProceedsMatched.v1 for business date 2026-12-14
    Then treatment "T-0701" holds installments_paid 4 and its next due date is 2027-01-15
    Then the local decision record names rule "R-RES-26", package version "PM-2026.12" and payment code "PAY-90001", and it is written in the same transaction as the treatment row
    Then the plan state stays PLAN_RUNNING and this service publishes no business event of its own

  Scenario: AC2 The missed installment is held on the plan position (new, D-RCV-60)
    Given the rwb-payment contract mock returns paymentMissed for case "RC-2026-000555", treatment "T-0701", due date 2026-12-15 and amount due 12,500.00
    Given the rwb-source-data contract fake (DP-01, DP-05) returns no payment on account "A-0555" between 2026-12-05 and 2026-12-15
    When TreatmentWorkflow consumes rwb.payment.PaymentMissed.v1 for business date 2026-12-15 on 2026-12-16
    Then treatment "T-0701" shows the missed installment for due date 2026-12-15 with amount due 12,500.00 and installments_paid stays 3
    Then the case owner sees the missed payment on the treatment record the same morning
    Then the local decision record names rule "R-RES-27" and the package version the evaluation returned
    Then this service writes no case status and moves no plan state

  Scenario: AC3 A repeated event writes the plan once (new, D-RCV-60)
    Given the rwb-payment contract mock returns the proceedsMatched of AC1 for case "RC-2026-000555"
    When rwb.payment.ProceedsMatched.v1 with the same cloud event ID is delivered twice in a row
    Then the inbox holds one processed event for the cloud event ID and the second delivery drops before any activity runs
    Then treatment "T-0701" still holds installments_paid 4 and exactly one decision record exists for "PAY-90001"
    Then a second payment code naming the due date already advanced writes no further advance

  Scenario: AC4 A treatment without a plan writes nothing (new, D-RCV-60)
    Given the rwb-payment contract mock returns proceedsMatched for a treatment of case "RC-2026-000566" whose treatment_type is "SETTLEMENT" and whose installments is null
    When TreatmentWorkflow consumes rwb.payment.ProceedsMatched.v1 for that case
    Then no column of the treatment row changes and no decision record of a plan advance is written
    Then the inbox records the event as processed and no retry is scheduled

  Scenario: AC5 A plan advance that cannot be recorded changes nothing (new, D-RCV-60)
    Given the local decision-record mock refuses the write with MSG-P7-003
    When TreatmentWorkflow consumes the proceedsMatched of AC1
    Then no column of treatment "T-0701" changes and no inbox row is completed
    Then the step answers MSG-P7-003 and the event is redelivered under the same cloud event ID
    Then the second attempt, with the record store healthy, advances the plan once

  Scenario: AC6 The plan position shows on SCR-14 through the composite route (new, D-RCV-60)
    Given treatment "T-0701" holds installments_paid 3 and the missed installment for due date 2026-12-15 with amount due 12,500.00
    Given the gateway-bff composite route serves SCR-14 Treatment record from the case read of rwb-case and the treatment read of this service, one hop each
    When an officer holding Treatment and offer R opens SCR-14 for case "RC-2026-000555"
    Then SCR-14 shows the plan terms, installments_paid 3, the next due date 2026-12-15 and the missed installment for 2026-12-15 with 12,500.00
    Then the browser calls no owner service directly and the screen writes nothing

  Scenario: AC7 No personal data in the row, the record, the event or the logs (new, D-RCV-60)
    Given a proceedsMatched arrives for case "RC-2026-000555" carrying the case ID, the treatment ID, payment code "PAY-90001", the amount 12,500.00 and due date 2026-12-15
    When TreatmentWorkflow applies the plan advance
    Then the treatment row, the local decision record, the workflow history, the log lines and the span attributes carry IDs, codes, amounts, dates and a rule version only
    Then no name, address, telephone number, national identity number or account holder name is written, logged or put on a message

  Scenario: AC8 A parameters or list read that does not answer changes nothing (new, D-RCV-60)
    Given the rwb-case parameters and reference-data fakes answer beyond the budget of X5 for case "RC-2026-000555"
    When TreatmentWorkflow consumes the proceedsMatched of AC1
    Then no column of treatment "T-0701" changes and no decision record is written
    Then the step answers MSG-GEN-006 and the activity retries on the workflow policy of 1 s initial interval, back-off 2, 10 attempts

  Scenario: AC9 A statement that reads a payment, proceeds, rule, case or timer table is refused (new, D-RCV-60)
    Given a test statement of this service names the `proceeds` table of rwb_payment
    When the boundary test of section 12.7 runs in the build
    Then the grant refuses the statement and the boundary test fails the build

  Scenario: AC10 The match window and grace come from the package row (new, D-RCV-60)
    Given the plan-position and package fixture holds a second version of package "PAYMENT_MATCH" with a changed window for row "EXACT"
    When TreatmentWorkflow evaluates the plan position for business date 2026-12-14
    Then the window and grace applied are those of the version in force and no window or grace value is a constant of this build

  Scenario: AC11 The plan position is derived from the plan terms (new, D-RCV-60)
    Given treatment "T-0701" holds installments 24, installment_amount 12,500.00 and installments_paid 3
    When TreatmentWorkflow applies the plan advance of AC1
    Then the next due date and the installment are derived from first_due_date, installments, installment_amount and installments_paid, and no frequency, amount or date is a constant of this build

  Scenario: AC12 The parameters or the reference-data breaker is open and nothing is written (new, D-RCV-60)
    Given the rwb-case parameters and reference-data breaker is open for case "RC-2026-000555"
    When TreatmentWorkflow consumes the proceedsMatched of AC1
    Then no column of treatment "T-0701" changes and no decision record is written
    Then the step answers MSG-GEN-006 and the activity retries on the workflow policy of 1 s initial interval, back-off 2, 10 attempts

  Scenario: AC13 A component that reaches a payment, proceeds, rule, case or timer table fails the build (new, D-RCV-60)
    Given a component of this service queries a payment, proceeds, rule, case or timer table of another owner
    When the boundary test of section 12.7 runs in the build
    Then the grant refuses the access and the boundary test fails the build

  Scenario: AC14 The plan-position read answers 401, 403 and 404 (new, D-RCV-60)
    Given a request on /api/recovery/treatment/v1 carries no credential
    When the plan-position read is called
    Then it answers 401 and returns no plan data
    Given a request on /api/recovery/treatment/v1 carries a credential without Treatment and offer R
    When the plan-position read is called
    Then it answers 403 and returns no plan data
    Given a request on /api/recovery/treatment/v1 names a treatment ID with no treatment record
    When the plan-position read is called
    Then it answers 404 and returns no plan data

  Scenario: AC15 A consumed call that fails changes nothing (new, D-RCV-60)
    Given the rwb-source-data contract fake answers the read of account "A-0555" with an error
    When TreatmentWorkflow consumes the proceedsMatched of AC1
    Then no column of treatment "T-0701" changes and no decision record is written
    Then the activity retries on the workflow policy of 1 s initial interval, back-off 2, 10 attempts

  Scenario: AC16 A case status or plan state change the model does not allow is refused (new, D-RCV-60)
    Given treatment "T-0701" is in state PLAN_RUNNING
    When a step of this service attempts to write a case status or to move the plan state to a state the model does not allow
    Then the write is refused, no column of treatment "T-0701" changes and no decision record is written
```

The sixteen criteria are new under D-RCV-60 and test only the S2 deliverable of this story: the plan advanced by the matched installment, the missed installment held on the plan position, the inbox dedupe and the write key, the treatment without a plan, the failed record which changes nothing, the SCR-14 read and the no-PII rule. The ten legacy criteria AC1 to AC10 of RWB-E2-008 and the legacy test cases TC-E2-008-01 to TC-E2-008-10 belong to `RWB-P8-E2008-APP`, where the matching, the window, the exception list, the repeated run and the no-version-in-force rules are written word for word with their origin tags; they are not restated here and no criterion of this story claims them. Every value is the legacy story's own: plan "T-0701", account "A-0555", case "RC-2026-000555", 12,500.00 THB, 24 installments, 3 paid, due dates 2026-12-15 and 2027-01-15, payment "PAY-90001" dated 2026-12-14, package version "PM-2026.12", rules R-RES-26 and R-RES-27.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A payment the match reports for the plan's due date advances `installments_paid` by one and moves the plan position to the next unpaid due date | legacy BR1; R-RES-26; REQ-CHO-009 |
| BR2 | A due date that passes with no matched payment is held on the plan position as the missed installment, with its due date and its amount due, and `installments_paid` does not move | legacy BR2; R-RES-27; REQ-CHO-007 |
| BR3 | One advance per payment code and due date; one missed installment per plan and due date; the inbox and the write key carry the rule | legacy BR6; R-UNI-40; DP-09 |
| BR4 | The plan is this service's own row: the proceeds row, the rule rows, the case status and the timers are answers of their owners and are never read as tables | DP-01; Ownership Map (`treatment` S2) |
| BR5 | Every plan change is written with its local decision record naming R-RES-26 or R-RES-27 and the package version, in one transaction | legacy BR9; DP-03, DP-04 |
| BR6 | A parameters or list read that fails changes nothing, and the step retries on the workflow policy | DP-06, DP-07; TSD S2 T7 |
| BR7 | Window, tolerance, grace days and match types are columns of the package rows with a version, never code of this service | legacy BR7; D-RCV-36 T10 |
| BR8 | The plan position is derived from `first_due_date`, `installments`, `installment_amount` and `installments_paid`; no frequency, no amount and no date is a constant of this build | TSD S2 T3.1; legacy section 11 |

**Where each rule lives in the target.** BR1 and BR2 are `applyProceedsMatched` and `holdMissedInstallment` with the evaluated plan-position rule. BR3 is the inbox row and the write key of `RecordAndApply`. BR4 is the schema boundary of section 11. BR5 is the record library and the one transaction. BR6 is the retry policy of section 12.5. BR7 is the package read, so no threshold is a constant here. BR8 is the derivable plan position of section 11, recorded as ASM-4453.

### 9. State transitions

None of the case. The case status is rwb-case's and is moved by the parent `CaseWorkflow` from the stage outcome this service reports (DP-01). The rows below are the plan position on this service's own `treatment` row; the plan states are the RESTRUCTURE states of TSD S2 T4, and this story moves none of them.

| From (plan position) | Event | Condition | To |
|---|---|---|---|
| `installments_paid` n, earliest unpaid due date D | PAYMENT_MATCHED | The match reports the installment of D | `installments_paid` n+1, next due date D+1 period, plan state unchanged (R-RES-26) |
| `installments_paid` n, earliest unpaid due date D | PAYMENT_MISSED | No matched payment for D and the due date has passed | Unchanged `installments_paid`; the missed installment D and its amount due held on the plan position (R-RES-27), through the activity Not specified in the source documents (GAP-2693; ASM-4452) |
| A treatment without a plan | PAYMENT_MATCHED or PAYMENT_MISSED | `installments` or `first_due_date` is null | No change; the step ends (X1) |
| Any | A repeated delivery or the same due date again | The inbox or the write key refuses | No change; the repeat is counted (X2, X4) |

The plan state `PLAN_RUNNING`, the cure period of R-RES-27, the break count and the closure of a broken plan are `RWB-S2-E2027-APP` and `RWB-S2-E3011-APP` and are named here only as the context the plan position is read in. The stage execution itself is RUNNING, COMPLETED or FAILED in the workflow history, and a failed execution is retried on the platform policy with the record failure of X3 redelivered under the same cloud event ID (ASM-4455).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-treatment service identity (login `rwb_treatment`) | Consumes the two events, evaluates the plan-position rule, writes `treatment`, the record and the inbox row, and calls the parameters and list reads; holds no grant on another `rwb_*` schema |
| SY-RULES, the embedded Drools kit | Evaluates the RESTRUCTURE package version in force for the plan position and returns the rule ID and the version (DP-04) |
| The local decision-record library (RWB-PLT-E1027-CON) | Writes the plan change record in the caller's transaction and publishes `DecisionRecorded` on `rwb.decision-record.v1` (DP-03) |
| RW-CASEOWN, case owner | Reads the plan position and the missed payment on the cases in scope (Treatment and offer CRU) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads the plan position and the missed payment on the cases in scope (Treatment and offer CRUA) |
| SY-CASEWF, case workflow module; SY-AGENT, agent platform | Read the treatment record across the contract with right R, as TSD S2 T6.1 lists them; the case status and the exception list are theirs |
| RW-CREDITAD, Credit Administration officer | Reads the matched and unmatched receipts on SCR-28 as rwb-payment serves them (Write-off and posting CRUA); no write here |
| RW-AUDIT, internal audit; RW-COE, center of excellence analyst | Read the plan position, the record and the version it was taken under (R) |
| No delegation of authority level applies | The story applies a match and holds a miss; it approves nothing |

The rights are the rows of TSD S2 T6.1 and nothing wider. The step is unattended: no officer task sits on the happy path, and it runs under the service identity of the service. The REST operation on `/api/recovery/treatment/v1` is authorised by the rwb-access check, whose name is Not specified in the source documents (DOR-RWB-S2-E2008-APP-6; DP-08).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-001, DF-TRT-002 | treatment (S2, `rwb_treatment`) | id, case_id | Read, as the plan and the case the event names |
| DF-TRT-003 | treatment (S2, `rwb_treatment`) | decision_log_id | Write, the ID of the local record written with this change |
| DF-TRT-004 | treatment (S2, `rwb_treatment`) | treatment_type | Read, to know that the treatment carries a plan |
| DF-TRT-009 | treatment (S2, `rwb_treatment`) | installments | Read, the count of the schedule |
| DF-TRT-029 | treatment (S2, `rwb_treatment`) | first_due_date | Read, the start of the schedule |
| DF-TRT-031 | treatment (S2, `rwb_treatment`) | installment_amount | Read, the amount due of a missed installment |
| DF-TRT-032 | treatment (S2, `rwb_treatment`) | installments_paid | Write, increased by one for the due date the match reports |
| DF-TRT-033 | treatment (S2, `rwb_treatment`) | installment_shortfall | Not written: a full match holds no shortfall, and a partial one is `RWB-S2-E2027-APP`'s |
| DF-TRT-013, DF-TRT-014 | treatment (S2, `rwb_treatment`) | outcome, outcome_at | Not written: the outcome of a plan is `RWB-S2-E2027-APP`'s |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, `rwb_treatment`) | all fields, through `DecisionRecordWriter.record` | Write, in the same transaction (DP-03) |
| DF-FIN-002, DF-FIN-003, DF-FIN-004, DF-FIN-006, DF-FIN-008 | proceeds (P8, `rwb_payment`) | case_id, treatment_id, payment_code, amount, matched_to | Not read as a table: they arrive on the event of `RWB-P8-E2008-CON` (DP-01) |
| DF-ACE-028, DF-ACE-043 to DF-ACE-046, DF-ACE-054, DF-ACE-178, DF-ACE-179, DF-ACE-182 | `v_ace_account`, `v_ace_payment`, `v_ace_batch_status` (P1 views) | next_installment_date, the payment fields, the batch fields | Not read here and no view is granted: rwb-source-data serves them to rwb-payment (DP-05) |
| DF-REF-002, DF-REF-003, DF-REF-296, DF-REF-297, DF-REF-298 | `rule_row` (P7, `rwb_decision`) | rule_id, rule_version, package_version_id, drools_rule_name, outputs | Not read as a table: the evaluated result returns them (DP-04) |
| DF-CAS-001 to DF-CAS-023 | recovery_case, timer, assignment (P3, `rwb_case`) | the case, its status, its timers | Not read and not written: the status is the parent's and the plan clock is not this story's |
| Standard column | treatment (S2, `rwb_treatment`) | state, version, created_at, created_by, updated_at, updated_by | Read `state`; write the audit columns as TSD S2 T3.0 defines them |
| processed_event, outbox_event, idempotency_key | PLT library, created in `rwb_treatment` | the inbox row and the write key of the step | Write through the library, in the step's transaction (DP-09) |

`treatment` is the only table this story writes, and it writes one column of it — `installments_paid` — plus the audit columns and its `decision_log_id`. The plan position is not a stored column set: `first_due_date`, `installments`, `installment_amount` and `installments_paid` already carry it, and the earliest unpaid due date and its amount due are derived from them; the payment frequency of a plan is Not specified in the source documents (GAP-2693; ASM-4453). The legacy rows of `proceeds`, of the ACE views and of the rule rows are their owners' and are not read here (DP-01, DP-05). No foreign key leaves `rwb_treatment`, and `case_id` and `decision_log_id` are identifiers, not keys across schemas. Field identifiers are those of TSD S2 T3.1 and the Logical Data Model.

**No new table and no new column of another schema.** This story's Flyway version adds the write key that makes one advance per due date and one miss per due date — a unique key on the treatment and the due date the record names, plus the index the plan-position read uses — on `rwb_treatment`, and it adds no business column (DP-15). No personal data is written: identifiers, codes, amounts, dates and a rule version only.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). The two operations are the ones TSD S2 T-A.1 lists and RWB-S2-E3001-CON publishes; this story supplies the plan-position behaviour and adds no path.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/treatments/{treatmentId}` (API-S2-002) | `Treatment` out, including the plan terms DF-TRT-009, DF-TRT-029 and DF-TRT-031 and `installments_paid` DF-TRT-032, plus the plan-position elements of the read | Treatment and offer R, scope applied, through the guard library | Not applicable |
| PATCH | `/treatments/{treatmentId}` (API-S2-003) | `TreatmentUpdate` in, `Treatment` out; the installment-paid write of the legacy `TreatmentApi.recordInstallmentPaid` where the contract freeze chooses the REST route for the match | Treatment and offer U, scope applied | The write key on the treatment and the due date |

The errors of both are 401, 403 with MSG-P4-002, 404, 409, 422 and 503 with MSG-GEN-006, in the RFC 9457 problem body. The operation names, their payload elements and the element names of the plan position are Not specified in the source documents (GAP-2693; ASM-4452), and this story reads the plan position on the GET as it stands.

#### 12.2 REST operations consumed

| Operation | Base / contract | Owner | Use |
|---|---|---|---|
| The plan-check values in force (name Not specified in the source documents (GAP-2693; ASM-4452)) | RWB-P3-E1042-CON | P3 rwb-case | The parameters the plan-position step reads at their version, cached; no period, threshold or amount in code (DP-06) |
| The list values of the plan and the miss reasons (name Not specified in the source documents (GAP-2693; ASM-4452)) | RWB-P3-E1043-CON | P3 rwb-case | LOV-TREATMENT and LOV-TRT-OUTCOME at their version; no member is written in code (DP-07) |
| Not specified in the source documents (GAP-1346) | Not specified in the source documents (GAP-1346) | P7 rwb-decision | Legacy `RuleEvaluator.evaluate`, called in process; becomes a one-hop REST contract of its owner (DP-11) |
| Not specified in the source documents (GAP-1346) | Not specified in the source documents (GAP-1346) | P1 rwb-source-data | Legacy `RecoveryDataApi.paymentsLoaded`, called in process; becomes a one-hop REST contract of its owner (DP-11) |
| Not specified in the source documents (GAP-1346) | Not specified in the source documents (GAP-1346) | P3 rwb-case | Legacy `CaseWorkflowApi.openCaseForAccount`, called in process; becomes a one-hop REST contract of its owner (DP-11) |
| Not specified in the source documents (GAP-1346) | Not specified in the source documents (GAP-1346) | rwb-treatment (this service) | Legacy `TreatmentApi.runningPlans`, called in process; becomes a one-hop REST contract of its owner (DP-11) |
| Not specified in the source documents (GAP-1346) | Not specified in the source documents (GAP-1346) | rwb-treatment (this service) | Legacy `TreatmentApi.recordInstallmentPaid`, called in process; becomes a one-hop REST contract of its owner (DP-11) |
| Not specified in the source documents (GAP-1346) | Not specified in the source documents (GAP-1346) | P1 rwb-source-data | Legacy `RecoveryDataApi.nextInstallmentDate`, called in process; becomes a one-hop REST contract of its owner (DP-11) |
| Not specified in the source documents (GAP-1346) | Not specified in the source documents (GAP-1346) | P1 rwb-source-data | Legacy `BatchStatusQuery.forSource`, called in process; becomes a one-hop REST contract of its owner (DP-11) |

Two reads, one hop each with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020, DP-11). No payment, proceeds or rule read is made: those facts arrive on the contract's events (DP-01).

#### 12.3 Events published

None of this service's business events. `TreatmentApproved` (EV-10) is the event of this service's approval story and is not produced here. The local decision-record library writes its own `DecisionRecorded` row on the shared topic `rwb.decision-record.v1` inside the transaction of the change (DP-03), and the outbox relay of the service template publishes it.

#### 12.4 Events consumed

| Event | Topic | Owner service | Consuming service | Consumer group | Payload used | When |
|---|---|---|---|---|---|---|
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1`, owner P8 | rwb-payment (P8) | rwb-treatment | `rwb-treatment.payment-proceeds-matched.v1` | the case ID, the treatment ID, the payment code, the amount, the due date and the business date; starts the plan advance through the activity Not specified in the source documents (GAP-2693; ASM-4452) | on the relay of rwb-payment, deduped in the inbox |
| `rwb.payment.PaymentMissed.v1` (EV-12) | `rwb.payment.events.v1`, owner P8 | rwb-payment (P8) | rwb-treatment | `rwb-treatment.payment-missed.v1` | the same payload; holds the missed installment on the plan position | on the relay of rwb-payment, deduped in the inbox |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1`, owner P7 | rwb-decision (P7) | rwb-treatment | `rwb-treatment.rule-package-in-force.v1` | announces the RESTRUCTURE package version in force; the stage swaps it in and stamps it on the record | once per published version |

The envelope is CloudEvents 1.0 keyed `caseId`, and the payload carries IDs, codes, amounts and dates only. A replayed workflow reuses the recorded result of the activity, so no second evaluation and no second write happens on replay (DP-04, DP-09).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage, with the four steps receive, evaluate, record and apply | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, treatment ID, payment code, amount, due date, business date and the event ID; output: the stage outcome of section 9. Workflow ID form: Not specified in the source documents (CG-ALL-8326). Start rule (Temporal Catalog v1): ROUTE_APPROVED with route R1 (restructure), R2 (settlement) or R3 (deed in lieu). Duplicate-start policy: Not specified in the source documents (CG-ALL-8326). |
| `applyProceedsMatched` (name Not specified in the source documents (GAP-2693; ASM-4452)) | Activity | `rwb-treatment` | The plan facts and the event in; the rule ID, the package version and the advanced plan position out |
| `holdMissedInstallment` (name as above) | Activity | `rwb-treatment` | The plan facts and the event in; the rule ID, the package version and the missed installment out |
| `RecordAndApply` (the design's activity) | Activity | `rwb-treatment` | One transaction: the treatment column, the decision record, the inbox completion and the outbox row of the record library |

The plan-position rule is evaluated inside the activity with the embedded Drools kit and never from workflow code (DP-04). The two activity names beyond the design's `RecordAndApply` are this story's design choice and are fixed by no source document (ASM-4452). `TreatmentWorkflow` is the one workflow the S2 ownership row carries.

#### 12.6 Schedules

None. The step is started by the consumed event through the workflow kit and is not a Temporal Schedule: this service owns no cron, no overlap policy and no catch-up window for the match (DP-10). The daily cadence belongs to the bank's Airflow edge that runs the ACE ingestion, and the plan clock of a running plan is `RWB-S2-E3010-APP`'s durable timer, not a task of this story. The outbox relay runs as a library component in every service and is not a Schedule of this one.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Writes `installments_paid`, the audit columns and `decision_log_id`; the table arrives with RWB-S2-E3001-APP and this story's Flyway version adds the write key and the index (DP-15) |
| `decision_record` | `rwb_treatment` | PLT library applied in this schema | Written through `DecisionRecordWriter.record` in the caller's transaction; the central `decision_log_entry` is P7's and is never touched (DP-03) |
| `processed_event`, `outbox_event`, `idempotency_key` | `rwb_treatment` | PLT library applied in this schema | The inbox row of the two consumed events, the record library's outbox row and the write key of the step (DP-09) |

Not owned and never read as a table: `proceeds` (P8, `rwb_payment`), `rule_row`, `rule_package`, `rule_package_version` and `decision_log_entry` (P7, `rwb_decision`), `recovery_case`, `timer`, `assignment` and `task` (P3, `rwb_case`), and every `v_ace_*` view (P1). No foreign key leaves the schema and no cross-schema join exists (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment event fixture (`RWB-P8-E2008-CON`) | `ProceedsMatched` for "T-0701", "PAY-90001", 12,500.00, due 2026-12-15, rule R-RES-26, version "PM-2026.12"; `PaymentMissed` for the same plan with due 2026-12-15 and amount due 12,500.00; the same cloud event ID twice; an event naming a SETTLEMENT treatment | AC1, AC2, AC3, AC4, AC7 |
| RWB-PLT-E1027-CON writer fake | An accepted record with chain sequence and entry hash, and a refusal with MSG-P7-003 | AC1, AC2, AC5 |
| Plan-position and package fixture | The RESTRUCTURE package version in force with the R-RES-26 and R-RES-27 rows, a second version, and a business date with no version in force | AC1, AC2, AC5 |
| rwb-case parameters and reference-data fakes (`RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`) | The plan-check values and the list values at their version, and an answer beyond the 2 s budget | AC1, AC6, X5 |
| gateway-bff composite route fake (`RWB-PLT-N001-CON`) | The merged SCR-14 answer for case "RC-2026-000555" with the case read of rwb-case and the treatment read of this service, one hop each | AC6 |
| rwb-source-data contract fake, ID Not specified in the source documents (CG-ALL-8333) | no payment on account "A-0555" appears between 2026-12-05 and 2026-12-15 | AC2 |

The fakes are test-only and are replaced by the real services in SIT; a drift between a fake and the published contract is a build failure of `RWB-P8-E2008-CON` or of the platform story that owns the fake. The element names of the plan position and of the two consumed operations carry the placeholder until their owners confirm them (GAP-2693; ASM-4452). The platform and consumed contracts of section 13 that have no fake row above (`RWB-PLT-E1072-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-TE006-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1044-CON`, `RWB-P7-E1073-APP`, `RWB-P4-E1037-CON`) are built as contract fakes from Day 1; their fake answers are Not specified in the source documents (ASM-4454).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | `GET` and `PATCH /treatments/{treatmentId}` on `/api/recovery/treatment/v1`; the parameters and list reads of rwb-case, one hop and 2 s each |
| Kafka | 0 published, 3 consumed | the two P8 events on `rwb.payment.events.v1` and `RulePackageInForce` on `rwb.decision.events.v1`; the record library's `DecisionRecorded` on `rwb.decision-record.v1`; inbox dedupe by cloud event ID |
| Temporal | 1 workflow, 3 activities | `TreatmentWorkflow` with `applyProceedsMatched`, `holdMissedInstallment` and `RecordAndApply` on `rwb-treatment`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, module `planposition`; front end `src/modules/recovery/treatment/PlanPosition.tsx`, the fragment SCR-14 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_treatment`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/treatment/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is the schema rule of section 11 and BR4. DP-03 is the transaction the story is built on: the record is a local row written with the change or not at all. DP-04 is the evaluation of the plan-position rule with the package version in force, inside the activity, so a replay reuses the recorded answer. DP-05 is a prohibition here: the payment and installment facts arrive on the P8 contract, so this module reads no `v_ace_*` view. DP-06 and DP-07 are the two reads of 12.2, cached. DP-09 is the inbox of the two consumed events, the write key and the record library's outbox row. DP-10 is the event-started stage on queue `rwb-treatment`, with no Quartz row and nothing polled. DP-11 is the contract-with-a-fake rule: the legacy in-process `TreatmentApi` calls become one-hop contracts with mocks, so this story builds on Day 1 with no payment table; where the match is delivered as a REST write instead of the event, it is served by `PATCH /treatments/{treatmentId}` (ASM-4452). DP-13 puts the read on the service base, DP-15 is the service's own Flyway version, and DP-19 reaches SCR-14 through the gateway-bff composite route.

**Dependencies the table adds and the build list does not hold.** The table adds eight H rows and four C rows (`RWB-PLT-E1027-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-TE006-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`; `RWB-P7-E1073-APP`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON`). Every one is a platform library or a contract of wave 0 and of the rule programme that the service template already carries, so the metadata keeps `Depends on (build)` None and the contract dependencies `RWB-P8-E2008-CON` and `RWB-P3-E1043-CON` — and the story builds against the published contracts and their fakes from Day 1, while step D1 decides whether the eight H rows and the four consumed contracts enter the dependency map (ASM-4454).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (plan-position branch) | Workflow | The four steps of the stage, the branch on the two events and the outcome report to the parent |
| `PaymentEventConsumer` | Consumer | Reads the two P8 events through the inbox, resolves the treatment and signals the child; a redelivery is dropped |
| `applyProceedsMatched` | Activity | The plan facts, the evaluated plan-position rule and the advance of `installments_paid` (DP-04) |
| `holdMissedInstallment` | Activity | The plan facts, the evaluated miss rule and the missed installment on the plan position |
| `PlanPositionGuard` | Service | Refuses a treatment without a plan, a second advance for the same due date and a change on a refused record |
| `RecordAndApply` | Activity | One transaction: the treatment column, the decision record, the inbox completion and the record library's outbox row |
| `TreatmentPlanRepository` | Repository | Reads and writes the plan columns of `treatment` in `rwb_treatment` only |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with the rule ID and the package version (DP-03) |
| `ParametersClient`, `ReferenceDataClient` | Clients | The two rwb-case reads, one hop, 2 s, a breaker (DP-06, DP-07, DP-11) |
| `Migrations` | Migration | The write key and the index on the service's own Flyway sequence (DP-15) |

**Build steps.** (1) The Flyway version with the write key and the index, and the migration test against the TSD types. (2) `PaymentEventConsumer` and the inbox path, with the doubled event and the dropped redelivery; test AC3 and X2. (3) `applyProceedsMatched` with the plan facts and the package fixture; test AC1, AC4 and the write key. (4) `holdMissedInstallment`; test AC2. (5) `PlanPositionGuard`, `RecordAndApply` and the rollback path; test AC5 and X3. (6) The plan position on the GET through the composite route fake; test AC6. (7) The boundary and no-PII tests; test AC7 and BR4. **Done when** the tests of section 16 pass, a synthetic month of matches advances each plan once per due date, every miss is held once with its due date and amount, every change has a record naming R-RES-26 or R-RES-27 and the package version, and SCR-14 shows both through the composite route in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The local decision record cannot be written (X3) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The identity has no right on the treatment read or write (section 12.1) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A parameters or list read did not answer inside the budget (X5) | {system} is not available. Your request is queued and will be retried. |

MSG-P7-003 and MSG-P4-002 are the texts the FSD S2 exception flows and the legacy story carry; MSG-GEN-006 is the platform text of the error standard for an unavailable dependency, where {system} is "Reference data" or "Parameters". Each error is an RFC 9457 problem response with `messageId`, `detail` and `instance`; the status mapping is 403 for MSG-P4-002, 422 for a refused record check and 503 for MSG-GEN-006. Thai text for each message follows decision DL10. The two messages of the match itself, MSG-P8-001 and MSG-P8-002, are rwb-payment's run summary and are not produced here.

### 15. Screens and states

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-14 Treatment record | Loading | The placeholder while the composite route answers |
| SCR-14 Treatment record | Plan running | The plan terms, `installments_paid` and the next due date, read only |
| SCR-14 Treatment record | Installment missed | The missed installment with its due date and amount due, and the next due date, read only |
| SCR-14 Treatment record | Refused | A role without Treatment and offer R reads MSG-P4-002 and nothing changes |
| SCR-14 Treatment record | Plan not yet available | The treatment without a plan shows its terms and no plan position |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-8334) |
| SCR-14 Treatment record | Error | Not specified in the source documents (CG-ALL-8334) |
| SCR-14 Treatment record | No access | Not specified in the source documents (CG-ALL-8334) |

SCR-14 Treatment record is first in E2 for the treatment record (FSD S2 screens table) and is served by the gateway-bff composite route, which composes the case read of rwb-case with the treatment read of this service, one hop each, read only (DP-19); the browser calls no owner service directly and the screen writes nothing. SCR-28 Proceeds matching, its exception list and the JOB-07 run summary on SCR-44 are rwb-payment's and are not built or read here, beyond the running balance the Credit Administration officer already reads there. The screen field list, the route specification and the layout belong to the platform edge story and the screen owners; this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-008-01 | AC1, BR1, BR5 | Component | `PAY-90001` 12,500.00 on A-0555 dated 2026-12-14; T-0701 due 2026-12-15 |
| TC-E2-008-02 | AC2, BR2 | Component | no payment 2026-12-05 to 2026-12-15 |
| TC-S2-E2008-APP-01 | AC3, BR3 | Component | the same `ProceedsMatched` delivered twice in one consumer group |
| TC-S2-E2008-APP-02 | AC4, BR4 | Component | a SETTLEMENT treatment with `installments` null |
| TC-S2-E2008-APP-03 | AC5, BR5 | Component | the record mock refusing with MSG-P7-003, then a healthy retry |
| TC-S2-E2008-APP-04 | AC6, BR2 | Component | the composite route fake merging SCR-14 with the missed installment |
| TC-S2-E2008-APP-05 | AC7 | Contract | a property check over a synthetic party name in the event and the answer; no personal field in the row, the record, the log lines or the span attributes |
| TC-S2-E2008-APP-06 | AC9, BR4, X6 | Contract | a statement reading the `proceeds` table of rwb_payment from this service; the grant refuses it and the build fails |
| TC-S2-E2008-APP-07 | AC8, BR6 | Component | the parameters read answering beyond the budget of X5, then the retry policy of the workflow kit |
| TC-S2-E2008-APP-08 | AC10, BR7 | Component | a second package version with a changed window for row "EXACT" |
| TC-S2-E2008-APP-09 | AC11, BR8 | Component | treatment "T-0701" with installments 24, installment_amount 12,500.00 and installments_paid 3 |
| TC-S2-E2008-APP-10 | AC12, BR6, X5 | Component | the rwb-case parameters and reference-data breaker open for case RC-2026-000555 |
| TC-S2-E2008-APP-11 | AC13, X6 | Contract | a component query of a payment, proceeds, rule, case or timer table of another owner; the grant refuses it and the build fails |
| TC-S2-E2008-APP-12 | AC14 | Contract | a request on /api/recovery/treatment/v1 with no credential, with a credential lacking Treatment and offer R, and for a treatment ID with no treatment record |
| TC-S2-E2008-APP-13 | AC15 | Component | the rwb-source-data contract fake answering the read of account A-0555 with an error |
| TC-S2-E2008-APP-14 | AC16 | Component | treatment T-0701 in PLAN_RUNNING and a write of a case status or a plan state the model does not allow |

The two legacy identifiers TC-E2-008-01 and TC-E2-008-02 are kept with their Covers and Data, because their scenarios are the match and the miss this slice applies to the plan; the legacy Level "System" maps to "Component" and the legacy Level "Access" maps to "Contract", as ruled for this story (D-RCV-60). TC-E2-008-03 to TC-E2-008-10 cover the unmatched payment, the account with no open case, the failed batch, the repeated run, the window boundary, the package in force and the access check on `/proceeds`, which `RWB-P8-E2008-APP` owns; they are not copied here. The fourteen new cases prove the criteria no legacy row exercises. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID, and the integration copies of these rows end in `-ITG` and belong to RWB-ITG-E2008-ITG.

### 17. Guardrails

- No business value in code: the window, the tolerance, the grace days, the match types and the plan-check values are rows of the packages and of the parameters read at their version; a build check fails on any of them in the Java source or the module configuration (BR7, BR8).
- No personal data in logs, tests, workflow inputs, events or records: the row, the record, the workflow history, the log lines and the span attributes carry the case ID, the treatment ID, the payment code, the rule ID, the package version, amounts and dates only, and no account number is logged.
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE view and holds no grant on one, and the payment and installment facts arrive on the P8 contract (DP-05, DP-01).
- No read of another service's tables and no cross-schema join: `proceeds` (P8), `rule_row` and `rule_package` (P7), `recovery_case`, `timer` and `assignment` (P3) are reached only through their owners' contracts, and the boundary test fails the build on any statement outside `rwb_treatment`.
- Amounts use BigDecimal with scale 2 and are compared exactly; no float and no rounding rule of this story.
- The decision record is written in the same transaction as the plan change, and a failed write rolls the whole step back with MSG-P7-003 (X3, AC5).
- One advance per due date and one miss per due date: the write key and the inbox carry the rule, and a redelivery writes nothing (BR3, AC3).
- Nothing is polled and no timer row is read: the step is event-started and the plan clock is not this story's (DP-10).
- The case status and the plan state are not written here; the parent moves the case and the plan states are the other stories' (DP-01, section 9).
- An applied migration is never edited: the write key and the index are a new version on the service's own Flyway sequence (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event — this story holds the missed installment on the plan the event names | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-008-02, TC-S2-E2008-APP-04 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list — this story advances the plan by the match rwb-payment reports | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-40 | TC-E2-008-01, TC-S2-E2008-APP-01, TC-S2-E2008-APP-02, TC-S2-E2008-APP-03, TC-S2-E2008-APP-05 |

The two requirement rows are the legacy traceability rows of RWB-E2-008, kept unchanged; features FEAT-OCC-10 ("Match a payment to the plan"), FEAT-OCC-11 ("Raise the plan payment missed event") and FEAT-PAY-01 ("Match a payment to a plan installment") and L3 process 7.3 are the legacy key's, and this story answers them on the treatment side of the same key.

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E2-008 | The treatment-side deliverable: the plan advanced by the matched installment, the missed installment held on the plan position, the inbox dedupe and write key, the treatment without a plan, the failed record, the SCR-14 read and the no-PII rule |
| RWB-P8-E2008-APP, RWB-P8-E2008-CON | The match, the exception list, JOB-07, the `proceeds` row, the two events and the ten legacy criteria AC1 to AC10 word for word; this story writes nothing of it |
| RWB-P1-E2008-APP | The payments, the next installment date and the batch status reads of ACE that feed the match |
| P7 rwb-decision, P3 rwb-case | The packages and their versions announced on `RulePackageInForce`; the case status, `CaseWorkflow`, the assignment and the timers |
| RWB-S2-E2027-APP, RWB-S2-E3011-APP, RWB-S2-E3001-CON, RWB-S2-E3004-APP, RWB-S2-E3010-APP | The shortfall, the break count and the closure this story does not build; the treatment read shape, the plan terms and the booking with its durable timer |
| RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON | The library and contract rows the pattern table adds, which stand in no build row of this story (ASM-4454) |
| DP-01, DP-05, DP-13, DP-09, DP-10, DP-11, DP-19 | The owner's schema, no ACE view, the service base, the inbox, the event-started stage, the contract-with-a-fake rule and SCR-14 behind the composite route |
| ADR-013, ADR-014, ADR-015, ADR-016, ADR-017, ADR-020, ADR-022 | 19 services inside ACE, a schema and a login per service, Kafka with outbox and inbox, the reusable Temporal layer, embedded Drools per service, contract-first REST with one hop, and the local decision record |

### 19. Out of scope

- The payment and proceeds matching, the row order, the window, the tolerance, the grace, the exception list, the `proceeds` table, JOB-07 and the production of the two events: `RWB-P8-E2008-APP` and `RWB-P8-E2008-CON`.
- The ACE payment, installment-date and batch-status reads and the data-product freshness: `RWB-P1-E2008-APP` and rwb-source-data.
- The packages, their rows, their versions, their load and their approval: rwb-decision (P7).
- The plan states, the cure period (R-RES-27 to R-RES-31), the shortfall and the closure of a broken plan: `RWB-S2-E2027-APP`, `RWB-S2-E3011-APP` and rwb-case (P3).
- The treatment record, the offer, the approval, the plan offer, the booking and the schedule: `RWB-S2-E3001-APP` to `RWB-S2-E3010-APP`.
- The case status, `CaseWorkflow`, the assignment, the officer tasks and the queues: rwb-case (P3).
- The rights, the roles, the scope data and the guard library: rwb-access (P4) and the platform library stories.
- SCR-28 Proceeds matching, its exception list, the manual match and the SCR-44 run summary: rwb-payment (P8) and Epic 4.
- The gateway-bff composite route, the SCR-14 field list and the layout: `RWB-PLT-N001-CON` and the screen owners (DP-19).
- Partial and late payments inside a window (RWB-E2-027), settlement, auction and enforcement proceeds, the posting file and the application of proceeds to the case balance (Epic 4).
- The real cross-service proof against live rwb-payment, rwb-case and rwb-decision (the wave 2 integration harness, RWB-ITG-E2008-ITG), and the deployment of this build.
