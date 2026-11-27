# RWB-P8-E4048-APP Run the deed in lieu rental auto-debit

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-004: Align the Error and Message Standard v6 wording.
- RD-P1-066: Align the ownership of JOB-07 and JOB-08 with the job register amendment.
- `AceDataReady` (EV-26): record key `{sourceSystem}:{businessDate}` and the four-field payload (RD-P1-003).
- Start rule: the JOB-07 run starts only on the event with `sourceSystem` `ALS` and `status` `COMPLETED` (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-P8-E4048-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-048 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not sized; the squad sizes it at refinement (DOR-RWB-P8-E4048-APP-16) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P8-K |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P8-E4048-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Readiness decisions | RD-P1-003, RD-P1-004, RD-P1-040, RD-P1-066 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 23 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **sale officer**, I want **the Workbench to take the rental of a deed in lieu buy-back by auto-debit, issue the receipt as a `proceeds` row of `rwb_payment`, and follow up the arrears as `PaymentMissed` on the payment topic - with the rental terms read from the rwb-treatment contract, the debit facts read from rwb-source-data, the run started by the ACE batch event and the local decision record written with the rule version in the same transaction**, so that **every rental of a buy-back is matched to its case without a person, and a rental that falls behind is found the next morning instead of at month end**.

Inside `rwb-payment`, schema `rwb_payment`, base `/api/recovery/payment/v1`, topic `rwb.payment.events.v1`, queue `rwb-payment` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.payment`:

- The rental arm of the JOB-07 payment matching run: it reads the rentals due on the business date, reads the receipts of that date, matches them with the `payment_match_rule` rows in force and writes the result (DP-13 keeps the base, DP-05 keeps the ACE facts with their owner).
- The receipt: one `proceeds` row of `rwb_payment` with `source` CUSTOMER and `matched_to` INSTALLMENT, from DF-FIN-001 to DF-FIN-009, written by the rental arm and by the manual `POST /proceeds/{proceedsId}/match`.
- The announcement: `ProceedsMatched` (EV-25) on a matched rental and `PaymentMissed` (EV-12) when the rental is not received inside the window in force, both through the outbox in the transaction that writes the row.
- The record: the local decision record of the step, written through the RWB-PLT-E1027-CON library inside the caller's transaction, with the rule identity and version of the `payment_match_rule` row that decided the match (DP-03).
- The service side of SCR-28 Proceeds matching, reached through the gateway-bff composite route (DP-19).

It does not own: the deed in lieu rental record, its amount, its debit day and its arrears limit, which are rwb-treatment's (S2, FEAT-TRT-16, rules R-DIL-32 and R-DIL-34); the ACE receipt, batch and freshness facts, which are rwb-source-data's (P1); the case, the owner's task and the route state, which are rwb-case's (P3); the rule packages, which are rwb-decision's (P7); the rights and scope data, which are rwb-access's (P4); the published shapes, the event schemas, the error envelope and the fakes, which are RWB-P8-E4048-CON; the receipt notice, which is rwb-comms' (P6); the deployment of this build, which is the operations story of this key.

### 2. Business rationale

A deed in lieu ends with the asset on the bank's books and the customer renting it back. The business objective of the feature is fixed and unchanged: take the rental by auto-debit, issue the receipt and follow up the arrears without a person for a standard arrangement (FSD P8 A2.9; FEAT-PAY-09; legacy RWB-E4-048). The legacy story ran that loop as one service method against one `recovery` schema, and the same arrangement was written one epic ahead as FEAT-TRT-16 in rwb-treatment (FSD S2, rule R-DIL-32).

What D-RCV-60 changes is where each half lives. The rental record, its terms, the auto-debit instruction and the arrears limit stay with rwb-treatment, which owns treatments, deed in lieu agreements and plan timers. The money side - the receipt, its match to the case and the treatment, the arrears follow-up and the posting - is rwb-payment's, which owns payment and proceeds matching and the `proceeds` row (TSD P8 T3.1; Ownership Map, `proceeds` owner P8; Architecture v5 slide 4, P8 Payments and posting). The two halves meet at one read and one event: the rental read of rwb-treatment, and `PaymentMissed`, which rwb-treatment consumes to apply R-DIL-34 when the arrears exceed the limit.

The loop reports itself in the open. Instead of a private arrears table, the receipt is a `proceeds` row with `matched_to` INSTALLMENT and the arrears follow-up is `PaymentMissed` with `caseId`, `treatmentId`, `dueDate`, `amountDue` and `daysLate` (Architecture v5 slide 22). That is what lets rwb-case raise the owner's task, rwb-treatment hand the asset to the disposal route under R-DIL-34, rwb-comms notify and the reporting read model count the rental, without one service reading another's table.

The record moves with the write: the local decision record is written in the same transaction as the `proceeds` row, so a rental that cannot be recorded changes nothing (DP-03; ADR-022). AC2 is exactly that rule.

No business value is invented. The rental amount, the debit day and the arrears limit that the legacy text does not state stay unstated here, with the placeholder and the recorded gap, and every list value, field type and message is the value the FSD, the TSD and the legacy story already carry, read in force.

### 3. Preconditions

- RWB-P8-E4048-CON is published: base `/api/recovery/payment/v1`, `GET /proceeds` with `ProceedsPage`, `POST /proceeds/{proceedsId}/match` with `MatchRequest` in and `Proceeds` out, the error set with the problem body, the `Idempotency-Key` header, the `proceeds` DDL template, the `PaymentMissed` and `ProceedsMatched` schemas and the fakes. This story builds against contract version v1 (the `/v1` base) of that contract and its fake.
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` declared with `@Transactional(propagation = MANDATORY)`, failing with MSG-P7-003, and the `decision_record` template applied in this service's own schema (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-28 from the proceeds read, the case read of rwb-case and the treatment read of rwb-treatment, one hop each, read only (DP-19).
- The `rwb_payment` baseline exists from the service template: schema, login, outbox, inbox and idempotency objects, and the per-service Flyway sequence (RWB-PLT-E1044-CON). This story adds no table of its own and never edits an applied migration.
- rwb-source-data publishes the receipt read of the business date for source `ALS`, the batch status of that source and the freshness stamp of the data product, one hop with a 2 s timeout (DP-05; Architecture v5 slide 29). This service holds no `v_ace_*` grant and reads no ACE table.
- rwb-treatment publishes the read of the buy-back rentals due on a business date: the rental reference, the treatment reference, the case reference, the rental amount, the debit day and the due date. The field names of that answer are Not specified in the source documents (GAP-2523; ASM-4173) and are settled with rwb-treatment before the build.
- The `payment_match_rule` rows in force for the business date carry `rule_code`, `rule_version`, `match_type`, `amount_tolerance_pct`, `window_days_before`, `window_days_after`, `grace_days`, `partial_floor_pct` and `priority`, with the match types EXACT, WINDOW and PARTIAL (TSD P8 T3.1, T3.2). The rule code of the rental arm is Not specified in the source documents (GAP-2524; ASM-4181).
- The lists LOV-MATCH and LOV-PROCEEDS-SRC are closed lists per Reference Data v5 Lists; their members are held as the rwb-payment enum and a new member is a code change. The list LOV-MATCH-TYPE is read as data with its version; no member of it is written in code (BR-P8-009; TSD P8 T3.2).
- The workflow kit is provisioned on queue `rwb-payment` in namespace `rwb-recovery`, and the JOB-07 run of a business date is started by the `AceDataReady` event through the inbox of the outbox library, so a redelivered event starts no second run.
- No approval is needed to build against a Draft contract baseline, and a story with only CON build dependencies is Day 1 by rule (Template and Rules R5.7).

### 4. Flow

1. rwb-source-data publishes `AceDataReady` (EV-26) on `rwb.source-data.events.v1` for source `ALS` with status `COMPLETED` and the business date 2026-12-15, record key `ALS:2026-12-15`; the inbox of this service records the event id, so a redelivery starts no second run.
2. The JOB-07 run of that date starts on queue `rwb-payment` and checks the batch status and freshness of the source. A batch that is not complete stops the run before matching, and the plan view shows MSG-P1-001 with the date the product carries.
3. The run loads the `payment_match_rule` rows in force for the date and stops before matching if none is in force (MSG-P8-002).
4. The rental arm reads the rentals due on 2026-12-15 from rwb-treatment: rental `RT-2026-000701` of treatment `DIL-2026-000701` on case `RC-2026-000701` and account `A-0701`, with its rental amount and its due date. The field names of the rental part of the treatment answer are Not specified in the source documents (GAP-1379).
5. It reads the receipts of 2026-12-15 from rwb-source-data: `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel` and the capital columns of the account payment.
6. It matches each rental to a receipt in priority order: EXACT on the amount and the due date, then WINDOW inside `window_days_before`, `window_days_after` and `grace_days`, then PARTIAL above `partial_floor_pct` inside `amount_tolerance_pct`.
7. A rental that matched: in one `rwb_payment` transaction the run writes one `proceeds` row with `case_id`, `treatment_id`, `account_payment_id`, `source` CUSTOMER, `amount`, `received_date`, `matched_to` INSTALLMENT and `posting_ref`, its local decision record with the rule identity and version of the row that decided the match, the outbox row of `ProceedsMatched` (EV-25) and the idempotency row of the step.
8. The receipt is issued: `ProceedsMatched` names the case, the treatment and the receipt, rwb-case applies the money side, rwb-comms issues the notice and SCR-28 shows the rental matched.
9. A rental with no receipt inside the window: no `proceeds` row is written, because no money arrived. The run writes the local decision record and the outbox row of `PaymentMissed` (EV-12) with `caseId`, `treatmentId`, `dueDate` 2026-12-15, the `amountDue` the terms carry and `daysLate`.
10. The arrears follow-up: rwb-case raises the owner's task, rwb-treatment applies R-DIL-34 when the arrears exceed the limit, and rwb-comms notifies. One missed event is published per rental due date, never one per run.
11. The manual path: a sale officer or a Credit Administration officer matches an unmatched rental receipt with `POST /proceeds/{proceedsId}/match` and an `Idempotency-Key`; the same record, row change and event follow, once.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ACE batch of source `ALS` is not complete for the business date | The run stops before matching; no `proceeds` row and no event is written | MSG-P1-001 | AC1 |
| X2 | No `payment_match_rule` row is in force on the business date | The run stops before matching; the job monitor shows the run failed and Credit Administration is alerted | MSG-P8-002 | AC1 |
| X3 | A rental has no receipt inside the window in force | No `proceeds` row; one decision record and one `PaymentMissed` for the due date; the arrears task is rwb-case's | MSG-P8-001 | AC1 |
| X4 | A receipt matches no rental | It is left for the unmatched exception list of the exception-list story; this arm writes no row for it | MSG-P8-001 | AC1 |
| X5 | The same business date, the same receipt or the same event arrives twice | One `proceeds` row, one record and one event; the repeat is counted and the first id answered | None | AC1, AC2 |
| X6 | The decision record cannot be written | The transaction rolls back: no `proceeds` row, no event, and the caller sees MSG-P7-003 | MSG-P7-003 | AC2 |
| X7 | The rwb-treatment or rwb-source-data answer does not arrive inside 2 s | The rental of that answer is left unmatched for the run; the breaker opens and the next run retries | MSG-GEN-006 | AC1 |
| X8 | A role without the Write-off and posting right, or a case outside scope | Refused with MSG-P4-002 or 404, and nothing changes | MSG-P4-002 | AC1 |

The rental-side exceptions of the legacy story - a customer who never debited, an auto-debit refused by the bank and a rental whose arrangement was withdrawn - are decided in rwb-treatment under R-DIL-32 and R-DIL-34 and are proved by that service's stories. This story neither evaluates them nor writes their state.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P8-E4048-CON, the record library of RWB-PLT-E1027-CON and the composite route of RWB-PLT-N001-CON; the rental, receipt, case and package answers are consumed from their owners' published contracts and fakes |
| Negotiable | Nothing business is fixed: the rental amount, the debit day, the arrears limit, the window, the tolerance, the grace and the match priority are rows of the rental read or of `payment_match_rule` |
| Valuable | Every rental of a buy-back is matched to its case without a person, and a rental that falls behind is visible the next morning |
| Estimable | One rental read, one receipt read, one matcher, one writer, one record and two events |
| Small | One sprint with its tests, as the payment slice of a legacy key that rwb-treatment also serves |
| Testable | Both criteria of section 7 are automated on the synthetic rental and receipt fixtures |

### 7. Acceptance criteria

```gherkin
Feature: Run the deed in lieu rental auto-debit

  Background:
    Given case "RC-2026-000701" carries deed in lieu treatment "DIL-2026-000701" with buy-back rental "RT-2026-000701" on account "A-0701", due on 2026-12-15
    Given the business date is 2026-12-15 and the ACE batch for source ALS of that date is COMPLETE in the batch status of rwb-source-data
    Given the payment_match_rule rows in force for 2026-12-15 carry their rule_code, rule_version, match types, windows, grace, tolerance and priority
    Given the lists LOV-MATCH, LOV-PROCEEDS-SRC and LOV-MATCH-TYPE are read with their version

  Scenario: AC1 Run the deed in lieu rental auto-debit (legacy RWB-E4-048 AC1)
    Given the rwb-treatment contract mock returns the buy-back rental "RT-2026-000701" of treatment "DIL-2026-000701" with its rental amount, its debit day and due date 2026-12-15
    Given the rwb-source-data contract mock returns receipt "PAY-90701" of the rental amount on account "A-0701" dated 2026-12-15, and a rental with no receipt at all
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then takes the rental by auto-debit, issues the receipt and follows up arrears
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-048 AC2)
    Given the rwb-decision contract mock returns a failed decision-log write with MSG-P7-003
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Ownership and boundary rules hold (new, D-RCV-60)
    Given the rwb-source-data, rwb-treatment and rwb-case contract stubs are in place
    When the run reads the receipt and the rental, and the same fact is presented twice
    Then no v_ace_* view or ACE table is read, and no rental, debit or arrears rule is evaluated
    Then no task, case state or notice is written, and the repeat of the same fact writes once, records once, publishes once and is counted

  Scenario: AC4 Error answers of the provided operations (new, D-RCV-60)
    Given a caller without a valid credential, a caller without the right, and a request for an unknown identifier
    When each caller calls a provided operation
    Then the operation answers 401, 403 and 404 respectively

  Scenario: AC5 Replay of a write with the same Idempotency-Key (new, D-RCV-60)
    Given a write has been accepted once with its Idempotency-Key
    When the same write is replayed with the same Idempotency-Key
    Then the write is not repeated, no second row or record is written, no second event is published, and the repeat is counted

  Scenario: AC6 Duplicate delivery of a consumed event (new, D-RCV-60)
    Given a consumed event has been processed once through the inbox
    When the same event is redelivered
    Then it is acted on once and the redelivery is counted

  Scenario: AC7 Activity retry and timeout (new, D-RCV-60)
    Given an activity of the run has timed out before it committed
    When the activity is retried
    Then at most one row, one record and one event are written for the fact

  Scenario: AC8 A consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-source-data or rwb-treatment call fails or does not answer
    When the run reads the receipt or the rental
    Then no row, record or event is written for that rental

  Scenario: AC9 A disallowed status change is refused (new, D-RCV-60)
    Given a status change that the state model does not allow for the proceeds row
    When the change is requested
    Then the change is refused and nothing changes
```

The two criteria are the legacy criteria of RWB-E4-048 word for word, with their origin tag added and nothing else changed: the legacy wording of `its trigger arrives`, `the action is taken` and `the decision log cannot be written` all stand. One leading `Given` group is added to each, and those lines are the only additions: AC1 needs the rental read of rwb-treatment and the receipt read of rwb-source-data, which are other services' facts, and AC2 needs the failed write of the record library. What the legacy lines describe happens in five places in the target: rwb-source-data answers the receipts and the batch status, rwb-treatment answers the rental and applies R-DIL-34 on the arrears, this story matches the rental, writes the `proceeds` row, records the decision and publishes `ProceedsMatched` or `PaymentMissed`, rwb-case raises the owner's task, and rwb-comms issues the notice. Because the legacy criteria are generic, the rental detail behind them is filled from FSD P8 A2.9, TSD P8 and the R-DIL rules and is recorded as GAP-2522 with ASM-4172, and every value no source carries is held as GAP-2523 with ASM-4173.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR12 (VR-P8-009-1) | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) raises MSG-P1-001 `{product} is from {date}. Today's ACE batch has not arrived.` | FSD P8 A2.9.3.1, copied character for character |
| BR13 (BR-P8-009) | No value a business person may change is written in code; it is read from reference data with its version | FSD P8 A2.9.3.1, copied character for character |
| BR1 | The receipt and its match are this service's: `proceeds` in `rwb_payment` carries the case, the treatment, the account payment, the source, the amount, the received date, `matched_to` and the posting reference, and no other service writes them | TSD P8 T3.1; Ownership Map (`proceeds` owner P8); Architecture v5 slide 41 |
| BR2 | A rental receipt is one value of LOV-PROCEEDS-SRC and closes to INSTALLMENT of LOV-MATCH; the rental arm writes no other match value, and a rental with no receipt writes no row | TSD P8 T3.2; FSD P8 A2.9; GAP-2528 (no RENTAL value in LOV-MATCH); ASM-4172 |
| BR3 | The match uses only the `payment_match_rule` rows in force for the business date, in `priority` order, with their window, grace, tolerance and floor; a run with no row in force stops before matching | TSD P8 T3.1, T3.2; FSD P8 AC-P8-001-05 (the same stop for the plan arm) |
| BR4 | The decision is recorded in the transaction that writes the row, one record per rule outcome, with the rule identity and version of the row that decided it; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; legacy RWB-E4-048 AC2; ADR-022 |
| BR5 | The ACE receipt, batch and freshness facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table and takes the receipt on the owner's contract only | DP-05; Architecture v5 slide 29; GAP-2524 |
| BR6 | The rental, its amount, its debit day, the auto-debit instruction and the arrears limit stay with rwb-treatment; R-DIL-32 sets the rental and the debit, R-DIL-34 hands the asset to the disposal route when the arrears exceed the limit, and this story evaluates neither | Business Rules and Routing Logic v4 (R-DIL-32, R-DIL-34); FSD P8 A2.9 (prerequisite FEAT-TRT-16) |
| BR7 | The case, the owner's task and the route state stay with rwb-case, and the notice with rwb-comms; this story raises no task and sends no notice | Ownership Map (recovery_case P3); Architecture v5 slide 41 |
| BR8 | The money side is announced once: `ProceedsMatched` on a matched rental and `PaymentMissed` on a rental due date with no receipt, each written to the outbox in the transaction of the row and relayed with key `caseId`; one missed event per due date, never one per run | Architecture v5 slides 22, 42 and 43; DP-09 is the platform library's |
| BR9 | The same fact twice, or the same `Idempotency-Key` twice, writes once, records once and publishes once, and the repeat is counted | Architecture v5 slide 11; TSD P8 T-A.2 |
| BR10 | No cross-schema join and no foreign key leaves `rwb_payment`; `case_id`, `treatment_id` and `account_payment_id` are identifiers of other services' facts | DP-01; TSD P8 T3.3 |
| BR11 | The auto-debit instruction itself is not this story's: FSD P8 A2.9 names ATS and AMIS as integration points while TSD P8 T5.1 names only ALS and GL, so the instruction is placed with FEAT-TRT-16 in rwb-treatment and this story collects, matches and follows up | FSD P8 A2.9.2; TSD P8 T5.1; GAP-2525; ASM-4176 |

BR2, BR3 and BR10 run in the loader and the matcher. BR4 runs in the writer, where the record, the row and the outbox are one transaction. BR5, BR6 and BR7 run at the boundary, before any row is written. BR8 runs in the outbox and the relay. BR9 runs in the idempotency table and the inbox.

### 9. State transitions

The lifecycle of a rental receipt, not of the case:

| From | Event | Condition | To |
|---|---|---|---|
| None | the run of the business date | No receipt for the rental due date | No row; one `PaymentMissed` for the due date |
| None | the run of the business date | A receipt inside the window in force and the record written | One `proceeds` row with `matched_to` INSTALLMENT; `ProceedsMatched` |
| INSTALLMENT | the same receipt or the same event again | The idempotency key repeats | No change; the first id is answered and the repeat counted |
| UNMATCHED | `POST /proceeds/{proceedsId}/match` with a valid `Idempotency-Key` | The officer matches the receipt to the rental | INSTALLMENT; one record and one `ProceedsMatched` |
| Pending | the record cannot be written | MSG-P7-003 | None; the row, the record and the event are all absent |
| INSTALLMENT | the run of a later date | The same receipt appears again in the source | No change; no second row and no second event |

The case state machine is not this service's (TSD P8 T4): rwb-treatment moves `RENTAL_RUNNING` by R-DIL-32 and hands the asset to `HANDED_TO_DISPOSAL` by R-DIL-34, rwb-case holds the case status, the task and the timer, and this service only writes the receipt and announces the miss.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-payment service identity, schema `rwb_payment`, own login (DP-02) | Reads the rental and the receipts on their owners' contracts, writes `proceeds`, the decision record and the outbox rows; the login name is Not specified in the source documents (GAP-2524; ASM-4175) |
| SY-DATALOAD, data load identity | Holds right U on the match operation, which is how the ACE-driven path posts a receipt (TSD P8 T6.1) |
| RW-WRITEOFF, RW-CREDITAD | Hold right U on the match operation and right R on the receipts of the cases in scope |
| RW-CASEOWN, RW-TEAMMGR, RW-CREDITAD and the other holders of right R | Read the receipts and their match state for the cases in scope (TSD P8 T6.1) |
| Sale officer (FSD P8 A2.9.3.3) | Uses the rental result on the case; the run itself is unattended and holds the primary use |
| rwb-access (P4) | Owns the rights, the roles and the scope data; each operation calls rwb-access's authorise check (DP-08) for the right it declares, and this story holds no role row |
| rwb-treatment (S2), rwb-source-data (P1), rwb-case (P3), rwb-decision (P7) | Own the rental, the receipts, the case and the rule packages; this service reads their answers and writes none of their rows |

Refusals are 403 with MSG-P4-002 and 503 with MSG-P7-003; a case outside scope answers 404.

### 11. Data

| BR Field ID | Table in rwb_payment | Field | Read or write |
|---|---|---|---|
| DF-FIN-001 | proceeds | id | Write |
| DF-FIN-002 | proceeds | case_id (an identifier, no foreign key into `rwb_case`) | Write |
| DF-FIN-003 | proceeds | treatment_id (the deed in lieu treatment, an identifier) | Write |
| DF-FIN-004 | proceeds | account_payment_id (the receipt, an identifier) | Write |
| DF-FIN-005 | proceeds | source (CUSTOMER) | Write |
| DF-FIN-006 | proceeds | amount | Write |
| DF-FIN-007 | proceeds | received_date | Write |
| DF-FIN-008 | proceeds | matched_to (INSTALLMENT) | Write |
| DF-FIN-009 | proceeds | posting_ref | Write |
| DF-REF-261 to DF-REF-273 | payment_match_rule | rule_code, rule_version, match_type, amount_tolerance_pct, window_days_before, window_days_after, grace_days, partial_floor_pct, priority, valid_from, valid_to | Read |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, DP-03) | the record of the step: case, decision code, rule id, rule version, inputs, final call, actions, decided at, actor | Write |
| outbox_event, processed_event, idempotency_key | objects of the service template | all fields | Write |
| DF-ACE-043 to DF-ACE-054 | not held | the receipt of `v_ace_payment` | Read on rwb-source-data's contract |
| DF-ACE-001 to DF-ACE-042 | not held | the account of `v_ace_account` | Read on rwb-source-data's contract |
| DF-CAS-001 to DF-CAS-023 | not held | the case and its route state | Read on rwb-case's contract |
| DF-REF-001 to DF-REF-015 | not held | the rule row of the package | Read on rwb-decision's contract |

Field IDs are those of the Logical Data Model and TSD P8 T3.1. `proceeds` is the only table this story writes that holds business facts, and no column, key, join or view leaves `rwb_payment` (DP-01). The rental terms of DF-FIN-003 travel inside the receipt as identifiers and are never copied as columns; the rental amount is the amount of the receipt, read from the source, and is not a column of this schema. The rental amount, the debit day and the arrears threshold are read from rwb-treatment's rental terms and from reference data in force, and are never held as constants in code; the NPA and asset manager confirm their value set before the wave 3 test entry.

### 12. Contract

Base `/api/recovery/payment/v1` (DP-13), topic `rwb.payment.events.v1` (DP-14 is the naming library's), queue `rwb-payment`, schema `rwb_payment`, Java package as section 1.

Reference data read: the `payment_match_rule` parameters of DF-REF-261 to DF-REF-273 in force for the business date, read on the reference-data contract (DP-06, DP-07); the contract's operation names are Not specified in the source documents (DOR-RWB-P8-E4048-APP-20).

#### 12.1 REST operations provided

| Method | Path | Purpose | Authorization |
|---|---|---|---|
| GET | `/proceeds` | The receipts of a case or a date range with their match state: query `matched`, `from`, `to`, `page`, `size`; `ProceedsPage` out | Write-off and posting, right R, scope applied |
| POST | `/proceeds/{proceedsId}/match` | Match an unmatched rental receipt to its case and treatment; `MatchRequest` in, `Proceeds` out; `Idempotency-Key` required | Write-off and posting, right U, scope applied |

The two operations are API-P8-001 and API-P8-002 of TSD P8 T-A.1 and T-A.2, and their shapes are RWB-P8-E4048-CON's. This story implements the rental arm behind them and declares no third operation; the exception list of a receipt that matches no rental is FEAT-PAY-02's story.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| The rental read of the business date (path and field names Not specified in the source documents (GAP-2523; ASM-4173)) | `/api/recovery/treatment/v1` | rwb-treatment (S2) | The rentals due on the business date: rental, treatment, case, rental amount, debit day and due date | One hop, 2 s (DP-11 is the pattern; the row itself is class C in fact, GAP-2524) |
| The receipt read of the ACE batch (name Not specified in the source documents (GAP-2524; ASM-4175)) | `/api/recovery/source-data/v1` | rwb-source-data (P1) | The receipts of the business date for source `ALS`, the batch status and the freshness stamp | One hop, 2 s |
| The case read and money-side answer (name Not specified) | `/api/recovery/case/v1` | rwb-case (P3) | The case reference and the answer that applies the money side | One hop, 2 s |
| The rule-package read (name Not specified) | `/api/recovery/decision/v1` | rwb-decision (P7) | The version in force for the business date, the same one the record names | One hop, 2 s |

The four rows are contract dependencies of class C in fact, and the plan's C row for this story is None, so they are built against the owners' published documents and fakes from Day 1 (GAP-2524; ASM-4175). Each is a GET retried once with jitter and a breaker per downstream.

#### 12.3 Events published

Topic `rwb.payment.events.v1` with the `.retry` and `.dlt` topics, key `caseId`, CloudEvents 1.0 binary, `ce_source` `/rwb-payment`.

| Event | Schema name | Consumers | Payload used here |
|---|---|---|---|
| `ProceedsMatched` (EV-25) | `rwb.payment.ProceedsMatched.v1` | rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee | The case, the proceeds and the treatment references, the amount, the value date, the match value INSTALLMENT and the rule identity with its version |
| `PaymentMissed` (EV-12) | `rwb.payment.PaymentMissed.v1` | rwb-case, rwb-treatment, rwb-comms | `caseId`, `treatmentId`, `dueDate`, `amountDue` and `daysLate`, as the published example of Architecture v5 slide 22 |

Both are written to the outbox in the transaction of the write and relayed after the commit, and the record on `rwb.decision-record.v1` is the library's (DP-03). `TreatmentBooked` (EV-11) is the booking story's and is not published by the rental arm.

#### 12.4 Events consumed

| Event | Topic | Used for | Owner |
|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1` | Record key `{sourceSystem}:{businessDate}`; payload `sourceSystem`, `businessDate`, `status`, `completedAt`; starts the JOB-07 run of the business date only on `sourceSystem` `ALS` and `status` `COMPLETED`; the inbox deduplicates on the event id | rwb-source-data (P1) |
| `TreatmentApproved` (EV-10) | `rwb.treatment.events.v1` | Names the deed in lieu treatment that carries the buy-back rental, so the rental read of the date has an arrangement to match | rwb-treatment (S2) |
| `RulePackageInForce` (EV-30) | `rwb.decision.events.v1` | The package and version in force for the business date | rwb-decision (P7) |

Consumed through the inbox with the retry and dead-letter topics. `DecisionRecorded` (EV-08) is the record this service writes through the library on the shared topic, so this story is a producer of it and adds no consumer group.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Owner |
|---|---|---|---|
| The JOB-07 event-started run (`PaymentMatchingWorkflow` in the matching story; the name is a target design choice) | Workflow | `rwb-payment` in `rwb-recovery` | RWB-P8-E2008-APP |
| `matchPayments` | Activity | `rwb-payment` | RWB-P8-E2008-APP |
| The rental arm of the run (a step of `matchPayments` in the app design of this story) | Activity step | `rwb-payment` | This story |

This story registers no workflow, no child workflow and no Nexus operation: the ownership rows of P8 hold no workflow of its own, and the rental arm is a step of the run that already exists.

#### 12.6 Schedules

None. JOB-07 in rwb-payment and JOB-08 in rwb-integration are event-triggered runs and not Temporal Schedules (Architecture v5 slide 44), and the rental due date is a fact of the rental read, not a timer of this service. The legacy Quartz marker of the key becomes the `AceDataReady` start, and no Schedule, Quartz row or shared job table is added.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `proceeds` | P8 (`rwb_payment`) | The receipt and its match; the only business table this story writes |
| `payment_match_rule` | P8 (`rwb_payment`) | The match rules read in force; written by the matching-rule story of this service |
| `decision_record` | PLT library, created in `rwb_payment` | The local record of the step (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_payment` | Outbox, inbox and idempotency objects of the service template |

`treatment` and the rental record are S2's, `recovery_case`, `task` and `timer` are P3's, the `v_ace_*` views and the ACE batch are P1's and `rule_row` is P7's. This story creates no table and no column.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-treatment rental fake (RWB-P8-E4048-CON) | The rental read | Rental `RT-2026-000701` of treatment `DIL-2026-000701` on case `RC-2026-000701`; a treatment with no rental; an answer beyond 2 s |
| rwb-source-data receipt fake | The receipt and batch reads | Receipt `PAY-90701` for the rental amount on 2026-12-15; a receipt 3 days after the due date; no receipt; a batch that is not complete with MSG-P1-001 |
| rwb-case fake | The case read and money-side answer | The case with its route state; an accepted and a refused money-side answer |
| rwb-decision package fake | The package read | The version in force for 2026-12-15 |
| Decision-record library stub (RWB-PLT-E1027-CON) | The record write | A healthy write; a refused write with MSG-P7-003 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two operations of `/api/recovery/payment/v1`; the rental, receipt, case and package reads, one hop within 2 s |
| Kafka | 2 published, 3 consumed | `ProceedsMatched` and `PaymentMissed` on `rwb.payment.events.v1`; `AceDataReady`, `TreatmentApproved` and `RulePackageInForce` |
| Temporal | None created | The rental arm is a step of the JOB-07 run on `rwb-payment` |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `rental`.

| Component | Type | Responsibility |
|---|---|---|
| RentalDueReader | Service | The rentals due on the business date, from the rwb-treatment contract, with their amount and due date |
| ReceiptReader | Service | The receipts of the business date and the batch freshness, from the rwb-source-data contract |
| RentalMatcher | Service | The `payment_match_rule` rows in force, in priority order, and the EXACT, WINDOW and PARTIAL comparison |
| ProceedsWritingStep | Service | The one transaction: the `proceeds` row, the local decision record, the outbox row and the idempotency row |
| RentalArrearsStep | Service | The `PaymentMissed` of a due date with no receipt, once per due date |
| ProceedsMatchResource | Controller | The two operations of section 12.1, their rights, their `Idempotency-Key` and their errors |

**Database and migrations.** Writes `proceeds` and the library objects and reads `payment_match_rule`; index `(case_id, received_date)` and `(matched_to, received_date)`, and a unique key on the idempotency key of business date, treatment and due date. Per-service Flyway in `rwb_payment`: the table is RWB-P8-E4048-CON's template and the migration is the DB story of this service, so this story adds no migration and no row.

**Configuration.** No business value: the window, the grace, the tolerance, the floor, the priority and the rule version are rows of `payment_match_rule` read in force, and every list value comes from the lists (BR-P8-009). Two settings only, the page size of the read and the retry count of the run, neither fixed by a source in the read set (GAP-2524; ASM-4175).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is applied as the owner's contract: the service holds no `v_ace_*` grant, so the receipt and the account of DF-ACE-001 to DF-ACE-054 are read on rwb-source-data's contract. DP-03 fixes the record written in the transaction of the row. DP-13 moves the base and nothing else. DP-19 is behind SCR-28. The outbox and inbox objects and the Flyway sequence come with the service template and are named as library objects, not as a pattern of this key (RWB-PLT-TE006-CON and RWB-PLT-E1044-CON are the platform stories that own them).

**Dependencies the table adds and the plan does not hold.** The two H rows of DP-03 and DP-19 are the ones the metadata carries, with this key's CON; the four consumed reads are class C in fact and are built against their owners' documents and fakes from Day 1 (GAP-2524; ASM-4175).

**Build steps.** (1) The readers against the two contract fakes, AC1. (2) The matcher over the `payment_match_rule` fixtures, AC1. (3) The writing step with the record, the row, the outbox and the idempotency row in one transaction, AC1 and AC2. (4) The arrears step, one `PaymentMissed` per due date, AC1. (5) The manual `POST /proceeds/{proceedsId}/match`, AC1. (6) The absence assertions: no `v_ace_*` grant, no cross-schema key, no Schedule.

**Done when.** The tests of section 16 pass, the contract tests of RWB-P8-E4048-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON stay green, and a SIT week shows the rental of 2026-12-15 matched once with a receipt and an INSTALLMENT row, a rental with no receipt leaving one `PaymentMissed` for its due date and no row, a repeat writing nothing, and a stopped record leaving the row and the event absent with MSG-P7-003.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of `MatchRequest` is absent or invalid | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written, or the ledger refuses it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE batch of the source is late or failed, which is VR-P8-009-1 | {product} is from {date}. Today's load has not arrived. |
| MSG-P8-001 | The run summary of a date with an unmatched receipt | Not specified in the source documents (GAP-2522; ASM-4179) |
| MSG-P8-002 | No `payment_match_rule` row is in force on the business date | Not specified in the source documents (GAP-2522; ASM-4179) |
| MSG-GEN-006 | A consumed answer does not arrive inside 2 s | {system} is not available. Try again in a few minutes. |

MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are copied unchanged from the legacy story and the FSD, MSG-P1-001 is aligned to the Error and Message Standard v4 text, and MSG-GEN-006 is the platform timeout message. An error is the problem body of the platform envelope; the reads and the match answer 400, 401, 403, 404, 409, 422 and 503 as the contract declares.

SCR-28 states: empty when no rental is due or matched on the business date, with its text Not specified in the source documents (DOR-RWB-P8-E4048-APP-10); loading while the match or the read is in progress; error on a timeout with Not specified in the source documents (DOR-RWB-P8-E4048-APP-9) and on a failed read with the problem body; no access for a role without right U, with MSG-P4-002.

### 15. Screens and states

No new screen. The rental result shows on SCR-28 Proceeds matching: the receipts of the case in empty, loading, error, no access, matched and unmatched states, each row with the amount, the received date, the treatment, the match state and the rule identity of the record. An unmatched rental receipt shows in the unmatched list with the manual match action; a rental with no receipt shows on the case as the `PaymentMissed` of rwb-case, not here. The screen is one gateway answer through the composite route, which calls this service for the receipts and rwb-case and rwb-treatment for the header (DP-19); its field list, its path and its merge order are RWB-PLT-N001-CON's, and the screen writes only through the match operation.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-048-01 | Legacy AC1 (BR1, BR2, BR3, BR4, BR8); the rental read and the receipt read are the owners'; the rental is matched once, the row and the record name the rule version, and a due date with no receipt leaves one `PaymentMissed` | End to end | Synthetic rental RT-2026-000701 on case RC-2026-000701, receipt PAY-90701 dated 2026-12-15, and a rental with no receipt |
| TC-E4-048-02 | Legacy AC2 (BR4); the record cannot be written and the caller sees MSG-P7-003 | Component | The record library stub refuses the write |
| TC-E4-048-03 | Legacy Access criterion; the right is P4's; a role without right U is refused with MSG-P4-002 on the match operation | Component | A role without Write-off and posting U calls POST /proceeds/{proceedsId}/match |
| TC-E4-048-04 | Legacy Principle 5 (BR4); a forced record failure stops the action with MSG-P7-003 and leaves no row and no event | NFR | The record store stopped during the run of 2026-12-15 |
| TC-E4-048-05 | Contract of section 12: the operation POST /proceeds/{proceedsId}/match and the base /api/recovery/payment/v1 (DP-13), with the schemas of rwb_payment | Component | The contract document and its schemas |
| TC-E4-048-06 | Event envelope of section 12: topic rwb.payment.events.v1 with the .retry and .dlt topics, key caseId, CloudEvents 1.0 binary, ce_source /rwb-payment; the events of section 12.4 consumed through the inbox | Component | The published event and the consumed events of section 12.4 |
| TC-E4-048-07 | Boundary of the section 12.7 tables: each table is written only by its owner, and the DDL template applies in rwb_payment | Component | The rwb_payment schema and its DDL template |
| TC-E4-048-08 | BR5; the receipt is read only on rwb-source-data's contract, and no v_ace_* view or ACE table is read | Component | An ACE receipt stub on the owner's contract |
| TC-E4-048-09 | BR6; the rental, its amount and its debit day are read only, and no rental, debit or arrears rule is evaluated | Component | A rental stub from rwb-treatment with an arrears limit |
| TC-E4-048-10 | BR7; no task, case state or notice is written and no notice is sent | Component | A matched rental on a case in scope |
| TC-E4-048-11 | BR9; a repeated fact or Idempotency-Key writes once, records once and publishes once, and the repeat is counted | Component | The same receipt posted twice with one Idempotency-Key |
| TC-E4-048-12 | BR10; no cross-schema join and no foreign key is held in rwb_payment | Component | The rwb_payment schema after a run |
| TC-E4-048-13 | BR11; the auto-debit instruction is not written by this story, which collects, matches and follows up | Component | A rental whose auto-debit instruction sits in rwb-treatment |
| TC-E4-048-14 | AC3 (BR5, BR6, BR7, BR9, BR10, BR11); the ownership and boundary rules hold on each run and the repeat is counted | Component | The rwb-source-data, rwb-treatment and rwb-case contract stubs of TC-E4-048-08 to TC-E4-048-10 |
| TC-E4-048-15 | AC4; the provided operations answer 401, 403 and 404 on their error cases | Component | Not specified in the source documents (NEWAC-RWB-P8-E4048-APP-AC4) |
| TC-E4-048-16 | AC5 (BR9); a replay of a write with the same Idempotency-Key writes, records and publishes nothing again | Component | Not specified in the source documents (NEWAC-RWB-P8-E4048-APP-AC5) |
| TC-E4-048-17 | AC6 (BR9); a redelivered consumed event is acted on once | Component | Not specified in the source documents (NEWAC-RWB-P8-E4048-APP-AC6) |
| TC-E4-048-18 | AC7; a retried or timed-out activity writes at most one row, one record and one event | Component | Not specified in the source documents (NEWAC-RWB-P8-E4048-APP-AC7) |
| TC-E4-048-19 | AC8; a failed or unanswered consumed call writes no row, record or event | Component | Not specified in the source documents (NEWAC-RWB-P8-E4048-APP-AC8) |
| TC-E4-048-20 | AC9; a disallowed status change is refused and nothing changes | Component | Not specified in the source documents (NEWAC-RWB-P8-E4048-APP-AC9) |

Every legacy test case of RWB-E4-048 appears once. Origin tag: the legacy criteria AC1 and AC2 of RWB-E4-048 and the four legacy test case IDs are kept here verbatim as placeholder text (GAP-1377, GAP-1380) and are read against this flow; the business analyst replaces the placeholder with named values in a later legacy master version. AC1: the data and the rule version are in place, the trigger arrives and the rental is taken by auto-debit. AC2: the decision log cannot be written and the user sees MSG-P7-003. The contract is tested by TC-E4-048-05 to TC-E4-048-07. System maps to End to end, Access to Component and Resilience to NFR. The rental and receipt values are synthetic, built on the pattern of the FSD case RC-2026-000555, treatment T-0701 and payment PAY-90001, and the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the rental amount, the debit day, the arrears limit, the window, the grace, the tolerance, the floor, the priority and the rule version are rows of the rental read or of `payment_match_rule`, and every list value comes from LOV-MATCH, LOV-PROCEEDS-SRC and LOV-MATCH-TYPE.
- No personal data in events, workflow inputs, logs or tests: an event carries a case identifier, a treatment identifier, a due date, an amount and a day count, never a name, an address, a contact value or an identity number. Test data is synthetic.
- No cross-schema read (DP-01): no `rwb_treatment`, `rwb_case` or other service's table is read and no foreign key points into one.
- ACE data only through the owner's contract: the receipt and the account come from the rwb-source-data operations; no `v_ace_*` view and no ACE table is read by this service.
- The rental, the auto-debit instruction and the arrears limit are rwb-treatment's, and no rule of that service is evaluated here.
- No Quartz job, no Schedule and no shared job table: the run is event-started, and the due date is a fact of the rental read.
- No topic or event name is typed in code, and no message is reworded.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| FEAT-PAY-09 | Takes the rental by auto-debit, issues the receipt and follows up arrears (FSD P8 A2.9 and AC-P8-009-01); the legacy story master carries no requirement id (GAP-2522; ASM-4172) | Epic 4, P8 Payments and posting; Program BR-008 | FEAT-PAY-09, FEAT-TRT-16 | 7.4 Deed in lieu and the buy-back rental | R-DIL-32, R-DIL-34 | TC-E4-048-01 |
| BR-P8-009 | No value a business person may change is written in code; it is read from reference data with its version (FSD P8 A2.9.3.1) | Epic 4, P8 | FEAT-PAY-09 | 7.4 Deed in lieu and the buy-back rental | R-DIL-32 | TC-E4-048-01 |
| VR-P8-009-1 | Data product stale after a late or failed ACE batch raises MSG-P1-001 (FSD P8 A2.9.3.1) | Epic 4, P8 | FEAT-PAY-09 | 7.4 Deed in lieu and the buy-back rental | R-UNI-39 | TC-E4-048-01, TC-E4-048-04 |
| ADR-014 | Schema and login per service | Platform | FEAT-PAY-09 | 7.4 | None | TC-E4-048-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Platform | FEAT-PAY-09 | 7.4 | None | TC-E4-048-01 |
| ADR-022 | Local decision record plus central ledger | Platform | FEAT-PAY-09 | 7.4 | R-UNI-39 | TC-E4-048-02, TC-E4-048-04 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E4-048, disposition Split (rework) | Metadata; sections 1, 19 |
| Legacy AC1 and AC2 | Section 7, word for word with their origin tags |
| The receipt, the arrears follow-up and the rule version on the record (legacy AC1) | Sections 4 (7 to 10), 8 (BR2, BR3, BR4, BR8), 11, 12.3 |
| The failed record changes nothing (legacy AC2) | Sections 7 (AC2), 8 (BR4), 9, 14 |
| Data entities of the legacy story: recovery_case, v_ace_account, v_ace_payment, decision_log_entry, proceeds, rule_row | Section 11, each with its owner |
| Endpoint POST /proceeds/{proceedsId}/match and SCR-28 | Sections 12.1, 15 |
| Permission right U of Write-off and posting | Sections 10, 12.1, 16 (TC-E4-048-03) |
| Messages MSG-GEN-001, MSG-P4-002, MSG-P7-003 | Section 14, exception paths |
| Legacy test cases TC-E4-048-01 to -04 | Section 16 |
| The rental side of the key (rental record, auto-debit instruction, arrears limit) | Sections 1, 8 (BR6), 19 |

### 19. Out of scope

- The deed in lieu arrangement, the rental record, its amount and debit day, the auto-debit instruction to ATS and AMIS and the arrears limit: rwb-treatment (S2, FEAT-TRT-16, R-DIL-32, R-DIL-34).
- The step that hands the asset to the disposal route when the arrears exceed the limit: rwb-treatment and rwb-asset (R-DIL-34, R-DIS-25).
- The ACE receipts, the account facts, the batch status and the freshness of the data product: rwb-source-data (P1).
- The case, its route state, the owner's task and the timer: rwb-case (P3).
- The rule packages, their rows and their versions: rwb-decision (P7).
- The rights, the roles and the scope check: rwb-access (P4).
- The receipt notice and the arrears letters: rwb-comms (P6).
- The exception list of a receipt that matches no rental, and the plan-installment matching: FEAT-PAY-02's story and RWB-P8-E2008-APP.
- The settlement, auction and enforcement arms of the matching, which publish the same `ProceedsMatched` with other match values: RWB-P8-E4043-APP, RWB-P8-E4044-APP.
- The posting of the receipt to ALS and to the general ledger, and the posting file: the posting stories of this service.
- The published shapes, the event schemas, the error envelope, the table template and the fakes: RWB-P8-E4048-CON.
- The gateway-bff composite route and the screen field list of SCR-28: RWB-PLT-N001-CON.
- The deployment, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
- The cross-service journey of the key and its evidence: the wave 3 harness.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
