# RWB-P8-E4049-APP Apply proceeds to the case balance

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-066: Reuse the existing service listener and inbox for each topic and remove per-story consumer groups.
- `AceDataReady` (EV-26): record key `{sourceSystem}:{businessDate}` and the four-field payload (RD-P1-003).
- Start rule: the JOB-07 run starts only on the event with `sourceSystem` `ALS` and `status` `COMPLETED` (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-P8-E4049-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-049 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P8-L |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement; Not specified in the source documents (DOR-RWB-P8-E4049-APP-16) |
| Depends on (build) | RWB-P8-E4049-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version built against | Recovery Workbench API Specification v5, rwb-payment.yaml, info.version 5.0.0 (REST base /api/recovery/payment/v1) |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-066 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 18 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **case owner**, I want **the Workbench to apply every receipt to the balance in the order the policy sets**, so that **every payment and booking is matched to its case**.

This is the application slice of legacy RWB-E4-049 (FEAT-PAY-10 Apply proceeds to the case balance, module P8 Payments and posting, priority Must, depends on FEAT-PAY-04). It owns:

- the two legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screen, rights and test cases they depend on;
- the application step of JOB-07 Payment matching, an event-started run on task queue `rwb-payment` in namespace `rwb-recovery`, started by `AceDataReady` (EV-26): after a receipt is matched, the step applies its amount to the balance of the case in the order of the policy in force and answers with the amount applied, the match value and the rule version;
- the write of the `proceeds` row in schema `rwb_payment`: `matched_to` from `LOV-MATCH`, `amount`, `received_date`, `case_id`, `treatment_id`, `account_payment_id` and the posting reference of DF-FIN-009 left to the posting stories (TSD P8 T3.1, DF-FIN-001 to DF-FIN-009);
- the receipt and balance facts read on the rwb-source-data contract, because this service holds no `v_ace_*` grant (DP-05);
- the balance application answered to rwb-case on its contract; the case balance and the case of record are P3's;
- the local decision record of every rule outcome, written through RWB-PLT-E1027-CON before the row changes, and MSG-P7-003 when it cannot be written (DP-03; legacy AC1 and AC2);
- the publication of `ProceedsMatched` (EV-25, `rwb.payment.ProceedsMatched.v1`) on `rwb.payment.events.v1` in the same transaction as the row, through the outbox;
- the behaviour behind `GET /proceeds` (API-P8-001) and `POST /proceeds/{proceedsId}/match` (API-P8-002) on base `/api/recovery/payment/v1` (DP-13), and SCR-28 Proceeds matching in its loading, matched and unmatched states through the gateway-bff composite route (DP-19).

It does not own: the published shapes of the two operations, the event schema, the table baseline and the fakes, which are RWB-P8-E4049-CON; the case of record, its balance and its route states, which are rwb-case (P3); the ACE receipt, account and batch-status facts behind the `v_ace_*` views, which are rwb-source-data (P1); the rule package and its rule rows, which are governed in rwb-decision (P7); the posting of the applied amount to ALS and to the general ledger and the posting file, which are the posting stories of this service; and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E4-049 gives the Workbench one step between a receipt and a reduced balance: every receipt, whatever its source, is applied to the balance of its case in the order the policy sets, and the outcome is written to the decision log with the rule version. The FSD keeps the feature as FEAT-PAY-10 with the business objective "applies every receipt to the balance in the order the policy sets", a step that runs unattended with the case owner as the secondary role, and a metric of receipts matched the same day, rising each month (FSD P8 A2.10.1 and A2.10.3.3). The problem it answers is unchanged: payments are matched to plans and settlements by hand and broken plans are found late (FSD P8 A2.10.1). In the Epic 3 to 8 specification the feature is P8 in E4, runs unattended, touches ALS and GL and depends on FEAT-PAY-04 (Epics 3 to 8 Specification v3, E4 row FEAT-PAY-10).

What D-RCV-60 changes is who owns each part of that step.

- **the receipt, the match and the applied amount are this service's.** `proceeds` is P8's table in `rwb_payment` (context pack ownership row `proceeds`), and the two operations of the family are P8's. The amount, its source, its value date and what it was matched to are written here and nowhere else (TSD P8 T3.1).
- **the balance stays with rwb-case.** `recovery_case` and its states are P3's, and the balance the receipt reduces is a case and ACE fact answered on P3's and P1's contracts; this story answers an application and writes no case row, no balance row and no assignment, task or timer.
- **the ACE facts stay with rwb-source-data.** The legacy data table read `v_ace_account` (DF-ACE-001 to DF-ACE-042) and `v_ace_payment` (DF-ACE-043 to DF-ACE-054) in process. In the target only rwb-source-data holds SELECT on the `recovery.v_ace_*` views, so DP-05 applies as a prohibition and the receipts and the balance arrive on P1's contract (GAP-2531; ASM-4184).
- **the order is policy, not code.** The legacy criterion says "in the order the policy sets" and no source publishes that order, its components or its percentages. The step therefore reads the order as a rule row of the PAYMENT_MATCH package at its version in force and carries the missing values as a gap rather than inventing a waterfall (GAP-2530; ASM-4183).
- **the decision is recorded first.** One record per rule outcome, through the local decision-record library and the shared topic `rwb.decision-record.v1`, in the same transaction as the proceeds row; a failed write changes nothing and shows MSG-P7-003. That is what legacy AC1 and legacy AC2 ask for, and it is DP-03 with R-UNI-39 behind it.
- **the application is announced once.** `ProceedsMatched` (EV-25) is the one rwb-payment event that carries a receipt on the service's own topic, and its consumers are rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee (Architecture v5 slides 42 and 43).

The legacy criteria are kept exactly and they are thin: AC1 says "the data and the rule version this feature needs are in place / its trigger arrives" and the legacy test cases carry no receipt, amount, case or business date (GAP-2529; ASM-4182). Everything the legacy does not state is filled from FSD P8 A2.10 and TSD P8 where a source has it, and is held as a placeholder where no source does.

### 3. Preconditions

- RWB-P8-E4049-CON is published: the two operations on `/api/recovery/payment/v1`, the `Proceeds`, `ProceedsPage` and `MatchRequest` elements, the `ProceedsMatched` schema on `rwb.payment.events.v1`, the `proceeds` baseline, the error set and the fakes are baselined and handed to this story.
- `proceeds` exists in schema `rwb_payment` with DF-FIN-001 to DF-FIN-009 and the standard record columns of TSD P8 T3.0, from the DB story of this service; this story adds no table, no column and no migration.
- `AceDataReady` (EV-26) is published by rwb-source-data on `rwb.source-data.events.v1` and, with `sourceSystem` `ALS` and `status` `COMPLETED`, starts the JOB-07 run (Architecture v5 slides 31 and 44); FSD P8 A2.10.4.4 names the completion of the ACE batch for source `ALS` as the trigger of the same matching family.
- The receipts of the business date and the account balance of the case are answered on the rwb-source-data contract, with the freshness stamp of the data product, because this service holds no `v_ace_*` grant (GAP-2531; ASM-4184). The operation name of that read is Not specified in the source documents (GAP-2531; ASM-4184), and the row is not in this story's contract-dependency list, which is None.
- The case reference, its state and the answer that applies an amount to its balance are available on the rwb-case contract for the fake (P3); no case row, stage row or timer row is read as a table.
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- The PAYMENT_MATCH package is in force at its version, and the application order is one of its rule rows; the package code, the rule IDs of the application and the order itself are not published in any source: Not specified in the source documents (GAP-2530; ASM-4183).
- RWB-PLT-N001-CON is published: SCR-28 Proceeds matching reaches this service through the gateway-bff composite route, one hop, and no screen calls the service directly (DP-19).
- The capability area "Write-off and posting" and its rights R and U exist as access rows of rwb-access, and the service runs as its own login on schema `rwb_payment` with no grant on another `rwb_*` schema (TSD P8 T6.1; Architecture v5 slide 29).
- `LOV-MATCH`, `LOV-MATCH-TYPE` and `LOV-PROCEEDS-SRC` are read at their version in force (TSD P8 T3.2), and no list value is a constant of the build.
- No approval is needed to build against a Draft contract baseline, and no human verification stop is part of this run.

### 4. Flow

1. `AceDataReady` for business date D with `sourceSystem` `ALS` and `status` `COMPLETED` arrives on `rwb.source-data.events.v1`; the inbox writes its processed-event row in the same transaction as the service's own change, and a redelivery is a no-op (DP-09; Architecture v5 slides 22 and 31).
2. The JOB-07 event-started run starts on queue `rwb-payment` with the business date and the source `ALS` (Architecture v5 slide 44; FSD P8 A2.10.4.4).
3. The run reads the receipts of the business date and the account balance of each open case on the rwb-source-data contract, one hop with a 2 s budget and a breaker, and holds when the data product is stale (VR-P8-010-1, MSG-P1-001).
4. For each receipt that is matched and not yet applied, the run reads the case on the rwb-case contract and confirms that the case is open; no case row and no balance row is read as a table (DP-01, DP-05).
5. The run loads the PAYMENT_MATCH package version in force, from `RulePackageInForce` (EV-30) or from the rwb-decision contract, and reads the application-order rule row with its components, its order and, where the policy sets one, its cap (BR-P8-010; GAP-2530).
6. The application order is evaluated against the receipt amount, the balance components of the case and the business date, and the step answers the amount applied to each component in the policy's order. No percentage, cap or order is a constant of the build.
7. The decision is written before anything changes: one record through the local decision-record library, with the case reference, the proceeds reference, the rule ID, the package version in force, the inputs reference, the amounts applied, the order and the decided-at time (DP-03).
8. A failed record write stops the step: nothing is written, the receipt stays unapplied, MSG-P7-003 is raised and an incident is opened under R-UNI-39 (legacy AC2; FSD P8 A2.10.4.3).
9. The `proceeds` row is written in one `rwb_payment` transaction with the record, the inbox row and the idempotency row: the match value the matching arm set, the amount, the received date, the case and treatment references and no posting reference (TSD P8 T3.1; the posting reference is the posting story's).
10. The application is answered to rwb-case on its contract, one hop, so the case of record shows the reduced balance; the case move that follows is rwb-case's decision and is not described here (BR6).
11. `ProceedsMatched` (EV-25) is written to the outbox in the same transaction and relayed to `rwb.payment.events.v1` with key `caseId`, the CloudEvents envelope and no personal data (Architecture v5 slides 22 and 42; DP-09).
12. A repeated receipt, a repeated `AceDataReady` or the same `Idempotency-Key` on `POST /proceeds/{proceedsId}/match` writes once, records once and counts the repeat (Architecture v5 slide 11; TSD P8 T-A.2). SCR-28 reads `GET /proceeds` filtered by match status and date range, paginated, through the composite route.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written (library failure, stopped hash chain, outbox failure) | The transaction writes nothing: no proceeds change, no answer to rwb-case, no event; an incident is opened | MSG-P7-003 | AC2, TC-E4-049-02, TC-E4-049-04 |
| X2 | The role does not hold the Write-off and posting right R for `GET /proceeds` or U for `POST /proceeds/{proceedsId}/match` | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC3, TC-E4-049-03, TC-E4-049-05, AC7, TC-E4-049-09 |
| X3 | The ACE data product is stale after a late or failed batch for source `ALS` | The run holds, writes nothing, shows the date of the data and resumes on the next fresh answer | MSG-P1-001 | AC1 |
| X4 | The rwb-source-data, rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own backoff; nothing is written and no event is published; `GET /proceeds` answers 503 with the platform error envelope | None | AC1, AC5 |
| X5 | No application-order rule row is in force, or the receipt is not matched | The step holds and writes nothing; the receipt stays on the exception list of RWB-P8-E2027-APP and the package gap is reported to P7 | None | AC1 |
| X6 | The receipt is already applied, or the operation is repeated with the same `Idempotency-Key` | The stored answer is returned, no second row and no second event, and the repeat is counted | None | AC1 |
| X7 | The amount applied exceeds the receipt amount, or a component refuses a negative amount | The step refuses the answer, writes nothing and raises the invariant to the job monitor; the policy row is corrected in P7 | MSG-GEN-001 | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another `rwb_*` schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC4, TC-E4-049-06, AC8, TC-E4-049-10, Section 17, BR5, BR8 |

X1 and X2 are the exception paths of the legacy key and of FSD P8 A2.10.4.3 carried onto the split; X3 to X7 are the paths the target call types, the consumed event and the rule package add; X8 is the DP-01 and DP-05 boundary. Every threshold, percentage, order and cap is a rule row or reference data in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-P8-E4049-CON, the rwb-source-data, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The run and step names, the consumer group and the shape of the balance answer are this story's choice; the two operations, the list values, the columns, the messages and the screen are fixed |
| Valuable | Every receipt reduces the balance of its case the morning after the ACE load, and the outcome is on the decision log with the rule version the same day |
| Estimable | One run arm, one activity, one event consumer, one evaluator, one record write, one row change, three clients and two read-only screen states |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic receipts and balances through the contract fakes, plus the access case and the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Apply proceeds to the case balance

  Background:
    Given case "RC-2026-000555" holds receipt "PR-2026-000555" of source CUSTOMER for 12,500.00 THB on the business date
    Given the PAYMENT_MATCH package is in force at its version and the lists LOV-MATCH and LOV-PROCEEDS-SRC are read with their version
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Apply proceeds to the case balance (legacy RWB-E4-049 AC1)
    Given the rwb-source-data contract mock returns the receipts of the business date and the account balance of the case
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then applies every receipt to the balance in the order the policy sets
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-049 AC2)
    Given the rwb-decision contract mock returns a failed decision-log write
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Role without the right is refused (legacy X2 path) (new, D-RCV-60)
    Given the role does not hold the Write-off and posting right R for `GET /proceeds` or U for `POST /proceeds/{proceedsId}/match`
    When the role calls the operation
    Then the answer is 403 with MSG-P4-002 before any read or write
    Then nothing changes and no record is written

  Scenario: AC4 Boundary is refused (X8) (new, D-RCV-60)
    Given a component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another `rwb_*` schema
    When the build runs its boundary test
    Then the grant refuses the statement and the boundary test fails the build
    Then nothing is released

  Scenario: AC5 A consumed call fails or does not answer (X4) (new, D-RCV-60)
    Given the rwb-source-data contract mock does not answer inside 2 s
    When the application step runs
    Then the step retries on the workflow's own backoff
    Then nothing is written and no event is published

  Scenario: AC6 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change the model does not allow is requested for a proceeds row
    When the change is requested
    Then the change is refused with an answer Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC11)
    Then nothing changes

  Scenario: AC7 Role without the right is refused on each operation (X2) (new, D-RCV-60)
    Given the role holds the Write-off and posting right R for `GET /proceeds` but not U for `POST /proceeds/{proceedsId}/match`
    When the role calls `POST /proceeds/{proceedsId}/match`
    Then the answer is 403 with MSG-P4-002 before any read or write
    Then nothing changes and no record is written

  Scenario: AC8 Boundary reach is logged by the pipeline (X8) (new, D-RCV-60)
    Given a test reaches a `v_ace_*` view, a `recovery_case` row or another `rwb_*` schema
    When the build runs its boundary test
    Then the boundary test fails the build
    Then the pipeline log records the refused statement

  Scenario: AC9 Every business rule has a criterion or a guardrail test (new, D-RCV-60)
    Given the rules BR1 to BR12 of section 8
    When the story is checked for coverage
    Then each rule is covered by a criterion, a guardrail test or a boundary test

  Scenario: AC10 Error answers carry their status codes (new, D-RCV-60)
    Given the provided operations `GET /proceeds` and `POST /proceeds/{proceedsId}/match`
    When a call has no valid credential, a role without the right, or an unknown proceedsId
    Then the answer is 401, 403 or 404 respectively with the platform error envelope

  Scenario: AC11 A replayed write with the same Idempotency-Key writes once (new, D-RCV-60)
    Given `POST /proceeds/{proceedsId}/match` has answered a call with an Idempotency-Key
    When the same Idempotency-Key is sent again
    Then the write is applied once, with no second row and no second event; the answer to the replay is Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC7)

  Scenario: AC12 A redelivered consumed event is applied once (new, D-RCV-60)
    Given the consumed event `AceDataReady` is delivered a second time
    When the event is consumed
    Then the amount is applied once and no second record or event is written

  Scenario: AC13 A retried or timed-out activity writes at most once (X4) (new, D-RCV-60)
    Given the rwb-source-data contract mock does not answer inside 2 s on an attempt
    When the application step retries on the workflow's own backoff
    Then an attempt that times out writes nothing and the result is written once when an attempt succeeds
    Then no second row and no second event is written
```

The two criteria are the legacy criteria of RWB-E4-049 word for word, with their origin tag added and nothing else changed: the legacy wording of `its trigger arrives`, `the order the policy sets` and `the decision log cannot be written` all stand. One leading `Given` is added to each, and those two lines are the only additions: AC1 needs the receipt and the balance, which are rwb-source-data's facts, and AC2 needs the failed write of the decision-record library, which is the platform and rwb-decision boundary. What the legacy lines describe happens in three places in the target: rwb-source-data answers the receipts and the balance, this story applies the receipt, writes the proceeds row, records the decision and publishes `ProceedsMatched`, and rwb-case shows the reduced balance and moves the case. The order, the components, the percentages and the outcome fields of the application appear in no source and are held as GAP-2530 with ASM-4183, and the missing test data as GAP-2529 with ASM-4182.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| VR-P8-010-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) raises MSG-P1-001 `{product} is from {date}. Today's ACE batch has not arrived.` | FSD P8 A2.10.3.1, copied character for character |
| BR-P8-010 | No value a business person may change is written in code; it is read from reference data with its version | FSD P8 A2.10.3.1, copied character for character |
| BR1 | The receipt, its match and the amount applied are this service's: `proceeds` in `rwb_payment` carries the case, the treatment, the account payment, the source, the amount, the received date, `matched_to` and the posting reference, and no other service writes them | Architecture v5 slide 41; context pack ownership row `proceeds`; TSD P8 T3.1 |
| BR2 | The application order and its components are one rule row of the PAYMENT_MATCH package at the version in force, with the receipt amount, the balance components and the business date as inputs; no order, percentage or cap is a constant of the build | FSD P8 A2.10.1 and A2.10.3.1 (BR-P8-010); GAP-2530; ASM-4183 |
| BR3 | The decision is recorded before the row changes, one record per rule outcome, with the rule ID and the package version in force and the amounts applied; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; legacy RWB-E4-049 AC1 and AC2; FSD P8 A2.10.4.3 |
| BR4 | The trigger is the completion of the ACE batch of source `ALS` read through the batch status of rwb-source-data, and the step runs inside the JOB-07 event-started run, not on a Quartz schedule and not on a shared job table | FSD P8 A2.10.4.4; Architecture v5 slides 31 and 44 |
| BR5 | The ACE facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the receipts, the account and the batch status on the owner's contract only | DP-05; Architecture v5 slide 29; GAP-2531 |
| BR6 | The balance and the case stay with rwb-case: the application is answered on the rwb-case contract, and no `recovery_case`, `assignment`, `task`, `timer` or balance row is written here | context pack ownership row `recovery_case`, owner P3; Architecture v5 slide 41 |
| BR7 | The amount is applied once: a repeated receipt, a repeated event or the same `Idempotency-Key` writes once, records once and counts the repeat | Architecture v5 slide 11; TSD P8 T-A.2 |
| BR8 | The application is announced once: `ProceedsMatched` is written to the outbox in the same transaction as the row and relayed with key `caseId`, and this step publishes no other event | Architecture v5 slides 22, 42 and 43; DP-09 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_payment`; `case_id`, `treatment_id` and `account_payment_id` are identifiers of other services' facts | DP-01; TSD P8 T3.3 |
| BR10 | The posting of the applied amount to ALS and to the general ledger is not this step: DF-FIN-009 stays empty here and is filled by the posting stories of this service | FSD P8 A2.10.2 (integration points ALS and GL); ownership rows of this service |
| BR11 | No person name, address, contact value or identity number enters `rwb_payment`, the decision record, the `ProceedsMatched` payload, a log or a workflow input | Template and Rules v1 s17; Architecture v5 slide 42 notes |
| BR12 | A failed application writes nothing and leaves the receipt on the exception list; the policy row that caused it is corrected in rwb-decision and never in this build | FSD P8 A2.10.4.3 (AC-EXC-P8-010-02); R-UNI-39 of the Business Rules and Routing Logic v4 |

The two rows VR-P8-010-1 and BR-P8-010 are the rows of FSD P8 A2.10.3.1, copied character for character; the rest are the rules the target split fixes. R-UNI-39 is copy of the Business Rules and Routing Logic v4: a decision log that cannot be written blocks the action and raises an incident, which is what BR3 and BR12 carry.

### 9. State transitions

The case route state and the case balance are rwb-case's and are not changed by this story: the step answers an application and rwb-case shows the reduced balance and moves the case (BR6). What this story owns is the application state of the receipt and the state of the step.

| From (`proceeds` row) | Event | Condition | To |
|---|---|---|---|
| The match value the matching arm set, from `LOV-MATCH` | The application rule row fires under the PAYMENT_MATCH package | The receipt is matched and the case is open | The row carries the applied amount, the record and the `ProceedsMatched` outbox row, and its lifecycle state moves to the applied state fixed by the DB story (value Not specified in the source documents (GAP-2530; ASM-4183)) |
| The match value the matching arm set | The application rule row fires | No rule row is in force (X5) | Unchanged, nothing written |
| `UNMATCHED` | The application step reads the receipt | The receipt carries no match (X5) | `UNMATCHED`, nothing written, the exception list of RWB-P8-E2027-APP |
| Any | The decision record cannot be written (X1) | The library refuses | Unchanged, nothing written, MSG-P7-003 and an incident |
| Any | The amount applied exceeds the receipt amount (X7) | The answer breaks the invariant | Unchanged, nothing written, the monitor raised |
| The applied state | The same receipt or the same `Idempotency-Key` again (X6) | The stored answer is returned | The applied state, no second row, the repeat counted |
| The applied state | The posting story writes the posting reference | DF-FIN-009 is filled by the posting step | The applied state, the posting reference set, unchanged by this story |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | `AceDataReady` for business date D | The inbox row is written | Reading the receipts and the balance |
| Reading | The data product answers fresh | The package in force answers | Evaluating |
| Evaluating | The application rule row fires | The decision record is written | Writing |
| Writing | The row, the record, the answer, the inbox row and the outbox row commit | The transaction commits | Waiting for the next fact |
| Writing | The record write or the transaction fails (X1) | No commit | Waiting, nothing changed |
| Reading | The data product is stale (X3) | VR-P8-010-1 | Held, until a fresh answer |

The match values `INSTALLMENT`, `SETTLEMENT`, `FEE`, `SALE_PROCEEDS` and `UNMATCHED` are those of `LOV-MATCH` in TSD P8 T3.2 and are read with their version; this story writes no new list value and invents none.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: applies a receipt and reads the proceeds list |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: applies a receipt, reads the proceeds list and approves where the flow needs it |
| SY-DATALOAD, data load from COLLINS | Write-off and posting U: applies a receipt |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE, RW-FINANCE, RW-PRODHEAD, RW-WOCOMM | Write-off and posting R, and RA where the matrix gives it: read only, in scope, through SCR-28 |
| SY-CASEWF, SY-RULES, SY-AGENT | Write-off and posting R: the service identities run inside the same checks as a person |
| rwb-payment service identity | Runs the JOB-07 step, consumes `AceDataReady` and `RulePackageInForce`, writes the decision record and the proceeds row, answers rwb-case and publishes `ProceedsMatched`; it holds no grant on another schema and no `v_ace_*` grant |
| Case owner | Also uses the feature: reviews the applied and unmatched receipts of the case on SCR-28, with no wider right than the matrix gives |

The rights are the rows of TSD P8 T6.1 and of the legacy permission table of this key, and nothing wider. The step runs unattended under the service identity (FSD P8 A2.10.3.3, "None; runs unattended" as the primary use), and the capability area "Write-off and posting" and its rights are declared per operation. DP-08 is not in this story's pattern set: the right is declared by the contract and checked by the guard of the service template through the rwb-access authorise check on each operation, so it is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-001 to DF-FIN-009 | proceeds (P8, `rwb_payment`) | `id`, `case_id`, `treatment_id`, `account_payment_id`, `source`, `amount`, `received_date`, `matched_to`, `posting_ref` | Write the applied row: the match value, the amount, the received date and the references; the posting reference is left to the posting story |
| TSD P8 T3.0 standard columns | proceeds (P8, `rwb_payment`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, with the optimistic lock of `version` |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | `id`, `case_no`, `product_group`, `primary_person_key`, `status`, `stage_code` and 17 more | Read on the rwb-case contract only, and answer the application there; never as a table |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` (P1) | `account_key`, `account_code`, `account_status`, `contract_no`, `product_category_efs`, `total_balance` and 36 more | Not read: this service holds no `v_ace_*` grant; the balance arrives on the rwb-source-data contract (BR5) |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` (P1) | `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel`, `capital_amount` and 6 more | Not read: the receipt arrives on the rwb-source-data contract (BR5) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_payment`) | rule id, rule version, inputs reference, amounts applied, order, outcome, decided at | Write through the local library, one record per rule outcome, before the row changes |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | `id`, `rule_id`, `rule_version`, `route_set`, `from_state`, `event_code` and 9 more | Not read and not written: the rule rows are governed in rwb-decision and loaded with the package |
| Not specified in the source documents (DOR-RWB-P8-E4049-APP-7) | `payment_match_rule` (P7, by the Temporal and Drools design) | The rule rows of the match and of the application order, replacing the legacy table | Not read as a table: evaluated from the package in force (BR2) |

Field IDs are those of TSD P8 Payments and posting v2 T3.1 and of the legacy data table of RWB-E4-049, with their owners changed by the target. **No new table, no new column and no migration**: `proceeds` arrives with the DB story of this service, and `decision_record`, `outbox_event`, `processed_event` and `idempotency_key` are platform library objects created in `rwb_payment` by the library's own migration (DP-03, DP-09). The order, the components, the percentages and the applied state value of the application are Not specified in the source documents (GAP-2530; ASM-4183) and stay rule rows, reference data or the DB story's enum, never columns invented here.

**No personal data.** The rows this story writes carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_payment`, the decision record, the `ProceedsMatched` payload, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8); base `/api/recovery/payment/v1` (DP-13). This story supplies the behaviour behind the two operations whose shapes are declared by RWB-P8-E4049-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | `ProceedsPage` out, filtered by `matched`, `from` and `to`, paginated by `page` and `size` (API-P8-001) | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | `MatchRequest` in, `Proceeds` out with the match and the amount applied (API-P8-002) | Write-off and posting, right U, scope applied | `Idempotency-Key` header required; the answer is stored |

The two operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope proceeds reference, 409 on a receipt that is already applied, 422 with MSG-GEN-001 for an invalid field and 503 when the decision library or a consumed contract does not answer. The identifiers, paths and rights are those of TSD P8 T-A.1 and T-A.2, and the base is the target form of the monolith path.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The receipt and balance read of the ACE batch (operation name Not specified in the source documents (GAP-2531; ASM-4184)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The receipts of the business date for source `ALS` and the account balance of the case, with the freshness stamp of the data product; faked |
| The case read and the balance-application answer (operation names Not specified in the source documents (GAP-2532; ASM-4185)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its product group and state, and the answer that records the amount applied to the case balance; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-2530; ASM-4183)) | `/api/recovery/decision/v1` | P7 rwb-decision | The PAYMENT_MATCH package at the version in force and its application-order rule row; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, so this story builds against their published documents and fakes on Day 1 (GAP-2531, GAP-2532; ASM-4184, ASM-4185).

#### 12.3 Events published

| Event | Topic | Payload used | When |
|---|---|---|---|
| `ProceedsMatched` (`rwb.payment.ProceedsMatched.v1`, EV-25) | `rwb.payment.events.v1`, with its `.retry` and `.dlt` topics | The case reference, the proceeds reference, the treatment reference, the receipt amount, the amount applied, the value date, the match value and the rule ID with its version; CloudEvents 1.0, key `caseId`, no personal data | In the same transaction as the proceeds row, through the outbox, when the application commits |

`ProceedsMatched` is event 25 of Architecture v5 slide 43, produced by rwb-payment and consumed by rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee. The schema is declared once by RWB-P8-E4049-CON and this step is its publisher for the applied receipt. `TreatmentBooked` (EV-11) and `PaymentMissed` (EV-12) are published by the booking and plan-matching arm of JOB-07, which is RWB-P8-E2008-APP, and this step publishes neither.

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When | Owner |
|---|---|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1`, with its `.retry` and `.dlt` topics | `rwb-payment.rwb.source-data.events.v1` | Record key `{sourceSystem}:{businessDate}`; payload `sourceSystem`, `businessDate`, `status`, `completedAt`; the run starts only on `sourceSystem` `ALS` and `status` `COMPLETED`; CloudEvents envelope; deduped in the inbox on the event id | On the outbox relay of rwb-source-data; starts the JOB-07 run | rwb-source-data |
| `RulePackageInForce` (EV-30) | `rwb.decision.events.v1` | `rwb-payment.rwb.decision.events.v1` | The package code and the version in force, so the application order is evaluated at the released version; deduped in the inbox | On the outbox relay of rwb-decision, and at every step start from the package read | rwb-decision |

`DecisionRecorded` (EV-08) is written by all nineteen services on the shared topic `rwb.decision-record.v1`, and its consumers are rwb-decision and rwb-reporting (Architecture v5 slide 42, row 08). This service is a **producer** of that topic through the local library of DP-03 and not a consumer of it, so 12.4 carries no row for it.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| The JOB-07 event-started run (name Not specified in the source documents (GAP-2530; ASM-4183)) | Workflow, one execution per business date and source, started by `AceDataReady` | `rwb-payment` in namespace `rwb-recovery` | Input: the business date, the source and the package in force; signals: `AceDataReady`, `RulePackageInForce`; the application is one stage of it |
| The application step of JOB-07 (activity name Not specified in the source documents (GAP-2530; ASM-4183)) | Activity | `rwb-payment` | The receipts, the balance and the package in; the rule ID with its version, the amounts applied, the record, the row, the balance answer and the outbox event out, in one transaction |

`matchPayments` and `postProceeds` are the activities Architecture v5 slide 17 names on the same queue and belong to the matching and posting stories; this story neither renames them nor claims them. The run and activity names above are left as placeholders because no source names the application step, and the placeholder is carried as GAP-2530 with ASM-4183 rather than invented.

#### 12.6 Schedules

None. JOB-07 is an event-triggered run started by `AceDataReady` and not a Temporal Schedule (Architecture v5 slide 44), so this story declares no Schedule, no Quartz row and no shared job table. JOB-08 runs in rwb-integration.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| proceeds | P8 (`rwb_payment`) | The receipt, its match and the amount applied; this story writes the match value, the amount and the references |
| decision_record | PLT library, created in `rwb_payment` | The local hash-linked decision record, one per rule outcome (DP-03) |
| outbox_event | PLT library, created in `rwb_payment` | The `ProceedsMatched` row of the same transaction (DP-09) |
| processed_event | PLT library, created in `rwb_payment` | The inbox row of each consumed event and its dedupe key (DP-09) |
| idempotency_key | PLT library, created in `rwb_payment` | The key of the repeated `POST /proceeds/{proceedsId}/match` and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task`, `timer` and the case balance (P3), `decision_log_entry`, `rule_row` and `payment_match_rule` (P7), the `v_ace_*` views (P1), and the fee, booking and posting tables of this service, which are the sibling stories'. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data receipt and balance fake | The receipts of business date D for source `ALS`, one of them receipt `PR-2026-000555` of case `RC-2026-000555` for 12,500.00 THB, and the balance of the case; a stale product with its date; no answer beyond 2 s | AC1, X3, X4 |
| rwb-case application fake | The case `RC-2026-000555` with its product group and state, and an accepted and a refused balance-application answer | AC1, X4 |
| rwb-decision package fake | The PAYMENT_MATCH package at its version in force with the application-order row; a package without the row | AC1, X5 |
| rwb-source-data event fake | `AceDataReady` for business date D and source `ALS`, the same event twice, and an event for an empty batch | AC1, X6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-28 answer for the case, with the proceeds list of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data read, of the rwb-case application answer and of the rwb-decision package read are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2531, GAP-2532; ASM-4184, ASM-4185).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | `GET /proceeds` and `POST /proceeds/{proceedsId}/match` on `/api/recovery/payment/v1`; the rwb-source-data receipt and balance read, the rwb-case case read and application answer and the rwb-decision package read; one hop, 2 s |
| Kafka | 1 published, 2 consumed | `ProceedsMatched` on `rwb.payment.events.v1`; `AceDataReady` and `RulePackageInForce` through the shared service groups in section 12.4; the decision record is relayed by the library on `rwb.decision-record.v1` |
| Temporal | 1 run and 1 activity | The JOB-07 run and its application step on `rwb-payment`; no Schedule |
| File | None | No file is read, built or delivered here; the posting file is the posting story's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `application`, Java package `th.co.scb.ace.workbench.recovery.payment.application`; front end `src/modules/recovery/payment/ProceedsMatching.tsx`, the fragment SCR-28 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: rwb-payment holds no `v_ace_*` grant, because only rwb-source-data has SELECT on the views (Architecture v5 slide 29), so the receipt and the balance arrive on the owner's contract and the legacy reads of `v_ace_account` and `v_ace_payment` are retired (GAP-2531; ASM-4184). DP-03 is the transaction rule of the step: the record, the row, the inbox row and the outbox row commit together or not at all. DP-13 moves the base of the two operations and nothing else, and DP-19 is how SCR-28 reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The pattern table adds the two H rows `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, which the plan already carries for this story, and the plan's own H row `RWB-P8-E4049-CON` carries the shapes. The three consumed rows of 12.2 are contract dependencies of class C that the plan's C row does not list, because that row is None, so they are built against their documents and fakes on Day 1 and the difference is recorded (GAP-2531, GAP-2532; ASM-4184, ASM-4185).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| The JOB-07 application stage (name placeholder) | Workflow stage | Waits for the receipts of the business date and reports the outcome to its caller |
| The application step (name placeholder) | Activity | The one step: read the receipts, the case and the balance, evaluate the order, write the record, the row, the answer and the outbox event |
| `PaymentEventConsumer` | Inbox adapter | Consumes `AceDataReady` and `RulePackageInForce` through the shared service groups in section 12.4, writes the `processed_event` row and dedupes |
| `ProceedsApplicationEvaluator` | Service | The application-order row of the PAYMENT_MATCH package, against the receipt, the balance components and the business date |
| `PaymentDecisionRecordWriter` | Library adapter | Writes one decision record per rule outcome before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `ProceedsWriter` | Repository | Writes `proceeds` in one `rwb_payment` transaction, with the idempotency row and the optimistic lock |
| `ProceedsMatchedPublisher` | Outbox adapter | Writes the `ProceedsMatched` outbox row in the same transaction and leaves the relay to the library (DP-09) |
| `CaseBalanceClient` | Client | The case read and the balance-application answer, one hop, 2 s, breaker |
| `PaymentFactClient` | Client | The receipt and balance read of rwb-source-data, one hop, 2 s, with the freshness stamp |
| `RulePackageClient` | Client | The PAYMENT_MATCH package read of rwb-decision, one hop, 2 s |
| `ProceedsController` | Controller | The two operations, the capability area and right, the pagination, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `ProceedsMatching` | React component | Shows the applied and unmatched receipts on SCR-28, read only, with the refusal, the hold and the not-recorded states |

**Database and migrations.** No Flyway file of this story. `proceeds` arrives with the DB story of this service, and the decision record, the outbox, the inbox and the idempotency key are library objects created in `rwb_payment` by the library's migration (DP-03, DP-09). No column is added for the order, the components or the applied state: where the TSD P8 T3.1 names none, the value stays a rule row, reference data or the DB story's enum (GAP-2530; ASM-4183).

**Configuration and reference data.**

- `LOV-MATCH`, `LOV-MATCH-TYPE` and `LOV-PROCEEDS-SRC` at their version in force (TSD P8 T3.2), read as reference data and never as constants.
- The reference-data reads above follow the reference-data contract of DP-06 and DP-07; the lists and the PAYMENT_MATCH package named here are the parameters this story reads.
- The PAYMENT_MATCH package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the application order, its components, its percentages and its caps are values of the package and not of this build.
- The capability area "Write-off and posting" and its rights R and U are access rows of rwb-access, read through the guard.
- The shared service groups declared in section 12.4 and their subscriptions are configuration of the inbox library.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The application stage of the JOB-07 run and its input record, registered on `rwb-payment`, with `AceDataReady` as its trigger (AC1).
2. `PaymentEventConsumer` and the inbox row, with the duplicate and redelivery paths (AC1, X6).
3. `PaymentFactClient`, `CaseBalanceClient` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker, the stale-data path and the no-answer path (AC1, X3, X4).
4. `ProceedsApplicationEvaluator` over the PAYMENT_MATCH package, with the order row, the no-row path and the invariant of X7 (AC1, X5, X7).
5. `PaymentDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
6. `ProceedsWriter` with the one transaction, the applied row, the idempotency row and the optimistic lock (AC1, X6).
7. `ProceedsMatchedPublisher` and the outbox row, with the relay of the library (AC1).
8. The balance-application answer to rwb-case, with the accepted and refused answers of the fake (AC1, X4).
9. `ProceedsController` with the rights, the pagination, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1).
10. `ProceedsMatching` and SCR-28 in its loading, empty, error, no access, matched and unmatched states through the composite route fake (AC1).
11. The boundary test: no statement outside `rwb_payment`, no `v_ace_*` read, no write to `rwb_case` (rwb-case), `rwb_source_data` (rwb-source-data) or `rwb_decision` (rwb-decision), and no Schedule (X8, BR5, BR6).

**Feature flag.** `rwb.payment.proceeds-apply-v1`, read as a flag of the platform library; off means the consumer writes the inbox row and holds the receipts, writes no row, answers no application and publishes no event, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic `AceDataReady` in SIT, a receipt is applied in the order of the package row with its record and its event, a receipt without a rule row stays unapplied, a repeated fact writes once, a forced record failure changes nothing, no `v_ace_*` read and no foreign row write exists in the build, and SCR-28 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the `MatchRequest` is absent or invalid, or the application answer breaks its invariant | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right reads the proceeds list or attempts the application | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the proceeds row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of source `ALS` is stale after a late or failed batch (VR-P8-010-1) | {product} is from {date}. Today's load has not arrived. |

The four message IDs are those of the legacy message set of this key and of FSD P8 A2.10.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P7-003 is the message of legacy AC2 and of FSD AC-EXC-P8-010-02, and MSG-P4-002 is the message of TC-E4-049-03 and of FSD AC-EXC-P8-010-01.

### 15. Screens and states

SCR-28 Proceeds matching is served through the gateway-bff composite route (DP-19). The route calls rwb-payment for the proceeds list and the application, rwb-case for the case, its state and its balance and rwb-source-data for the receipt facts; this story fixes the rwb-payment answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The three states named by the legacy screen are the ones this step produces: **loading** while the receipts of the business date are read on the rwb-source-data contract, **matched** when the application has reduced the balance and the record, the row, the answer and the event are committed, and **unmatched** when no match or no application rule row answers, in which case the receipt goes to the exception list of RWB-P8-E2027-APP. The refusal and failure states shown on the same screen are the refused state with MSG-P4-002, the not-recorded state with MSG-P7-003 and the stale-data state with MSG-P1-001, each read from the same route.

The empty, error and no-access states of SCR-28 are Not specified in the source documents (CG-ALL-7762); the 403 answer of this route is the refused state with MSG-P4-002.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-049-01 | AC1 | Component | Case `RC-2026-000555`, receipt `PR-2026-000555` of source `CUSTOMER` for 12,500.00 THB and the balance of the case; the applied row, the decision record with the rule ID and version, the balance answer and the `ProceedsMatched` outbox row asserted on the fakes |
| TC-E4-049-02 | AC2 | NFR | The decision-record stub stopped; nothing written, no answer to rwb-case, no event, MSG-P7-003 shown and an incident opened |
| TC-E4-049-03 | Access | Contract | A role without the Write-off and posting right R or U; 403 with MSG-P4-002 on both operations and no read |
| TC-E4-049-05 | AC3 | Contract | Scenario AC3: a role without the right gets 403 with MSG-P4-002 before any read or write and no record is written |
| TC-E4-049-06 | AC4 | Pipeline | Scenario AC4: a statement or test reaching a `v_ace_*` view, a `recovery_case` row or another `rwb_*` schema is refused and fails the build |
| TC-E4-049-04 | Principle 5 | NFR | A forced decision-record write failure at the moment of the proceeds write; no row, no answer, no event, and the repeat writes once when the library recovers |
| TC-E4-049-16 | §12.7 table ownership (ASM-3438) | Component | Every table of §12.7 created in `rwb_payment` only; no statement outside `rwb_payment`, no `v_ace_*` read, no write to `rwb_case`, `rwb_source_data` or `rwb_decision`, and no foreign key leaves the schema |
| TC-E4-049-07 | AC5 | NFR | Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC10) |
| TC-E4-049-08 | AC6 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC11) |
| TC-E4-049-09 | AC7 | Contract | Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC3) |
| TC-E4-049-10 | AC8 | Pipeline | Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC4) |
| TC-E4-049-11 | AC9 | Pipeline | Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC5) |
| TC-E4-049-12 | AC10 | Contract | Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC6) |
| TC-E4-049-13 | AC11 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC7) |
| TC-E4-049-14 | AC12 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC8) |
| TC-E4-049-15 | AC13 | NFR | Not specified in the source documents (NEWAC-RWB-P8-E4049-APP-AC9) |

The four test cases TC-E4-049-01 to TC-E4-049-04 are the legacy cases of RWB-E4-049 in their legacy order, with the Level column added (TC-E4-049-16 is the boundary test of the §12.7 tables, added by this story): TC-E4-049-01 is the component proof of the step on its fakes, the two forced-failure cases map to NFR because they prove the atomicity and the no-side-effect property of the transaction, and the access case maps to Contract because the artefact under test is the declared right of the operation. The legacy rows name no receipt, amount, case or date, which is recorded as GAP-2529 with ASM-4182; the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID, and the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the application order, its components, the percentages, the caps, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_payment`, in the `ProceedsMatched` payload, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract or a `v_ace_*` view this service holds: it holds none, because only rwb-source-data has SELECT on the views, so the receipt and the balance arrive on P1's contract and a build that adds a view or an ACE table read fails the boundary test (DP-05; Architecture v5 slide 29).
- The case and its balance stay with rwb-case: no `recovery_case`, `assignment`, `task`, `timer` or balance row is written here, and no posting, no ledger entry and no posting file is produced here (BR6, BR10).
- One base, one topic, one queue and one login per service: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login, and no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- The decision is recorded before the change and every consumed event is deduped in the inbox; a build that publishes or that changes a row before its record fails the review (DP-03, DP-09).
- The amount applied never exceeds the receipt amount and no component takes a negative amount; the invariant is tested, not assumed.
- No retired element is reintroduced: no shared Quartz table, no Quartz job, no monolith API base, no `recovery` schema read, and no data-lake copy of the application.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id for this slice; the requirement is FEAT-PAY-10 of the FSD P8 A2.10 and its main success criterion AC-P8-010-01, that every receipt is applied to the balance in the order the policy sets and the result is recorded with its rule version (GAP-2529; ASM-4182) | The application step, the proceeds row, the decision record and the `ProceedsMatched` event | TC-E4-049-01, TC-E4-049-02 | FEAT-PAY-10 | Not specified in the source documents (DOR-RWB-P8-E4049-APP-2) |
| BR-P8-010 | No value a business person may change is written in code; it is read from reference data with its version (FSD P8 A2.10.3.1) | The order row, the lists and the package values read with their version | TC-E4-049-01 | FEAT-PAY-10 | Not specified in the source documents (DOR-RWB-P8-E4049-APP-2) |
| VR-P8-010-1 | Data product stale after a late or failed ACE batch raises MSG-P1-001 (FSD P8 A2.10.3.1) | The freshness check of the receipt read | TC-E4-049-01, TC-E4-049-04 | FEAT-PAY-10 | Not specified in the source documents (DOR-RWB-P8-E4049-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-payment as the owner of the application and of the proceeds | TC-E4-049-01 | FEAT-PAY-10 | Not specified in the source documents (DOR-RWB-P8-E4049-APP-2) |
| ADR-014 | Schema and login per service | `rwb_payment` and its own login, no cross-schema write | TC-E4-049-04 | FEAT-PAY-10 | Not specified in the source documents (DOR-RWB-P8-E4049-APP-2) |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `ProceedsMatched` outbox row and the inbox of the two consumed events | TC-E4-049-01 | FEAT-PAY-10 | Not specified in the source documents (DOR-RWB-P8-E4049-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-E4-049-01 | FEAT-PAY-10 | Not specified in the source documents (DOR-RWB-P8-E4049-APP-2) |
| ADR-022 | Local decision record plus central ledger | The record written before the row changes, one per rule outcome | TC-E4-049-02, TC-E4-049-04 | FEAT-PAY-10 | Not specified in the source documents (DOR-RWB-P8-E4049-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-049, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Test cases | TC-E4-049-01 to TC-E4-049-16 |
| Feature and screens | FEAT-PAY-10 Apply proceeds to the case balance; SCR-28 Proceeds matching |
| Rules | PAYMENT_MATCH governed in rwb-decision, and R-UNI-39 of the Business Rules and Routing Logic v4 where the decision log blocks the action; the package code, the application order and its rule IDs are not published (GAP-2530; ASM-4183) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the two operations, the `Proceeds`, `ProceedsPage` and `MatchRequest` elements, the `ProceedsMatched` schema, the table baseline, the error set and the fakes: RWB-P8-E4049-CON.
- The booking confirmation and the plan-installment matching that publish `TreatmentBooked` and `PaymentMissed`, and the exception list of an unmatched receipt: RWB-P8-E2008-APP and RWB-P8-E2027-APP.
- The settlement arm and the auction and enforcement arm of the match: RWB-P8-E4043-APP and RWB-P8-E4044-APP, which write the same `proceeds` table under the same contract.
- The posting of the applied amount to ALS and to the general ledger, the posting file and the posted reference of DF-FIN-009: the posting stories of this service.
- The case of record, its route states, its balance, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The ACE receipt, account and batch-status facts and the freshness of the data product: rwb-source-data (P1).
- The PAYMENT_MATCH package, its application-order rule rows, its version and its release: rwb-decision (P7).
- The roles, scopes and masking behind the Write-off and posting right: rwb-access (P4) and the guard of the service template.
- The gateway-bff composite route and the screen field list of SCR-28: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Change log: D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P8-E4049-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
