# RWB-P8-E4043-APP Match a settlement payment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P8-E4043-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-043 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P8-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P8-E4043-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **case owner**, I want **the Workbench to match a settlement payment to the treatment and close the money side**, so that **every payment and booking is matched to its case**.

This is the application slice of legacy RWB-E4-043 (FEAT-PAY-03 Match a settlement payment, module P8 Payments and posting, priority Must, depends on FEAT-PAY-01). It owns:

- the two legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and test cases they depend on;
- the settlement arm of JOB-07 Payment matching — an event-started workflow on task queue `rwb-payment` in namespace `rwb-recovery`, started by `AceDataReady` (EV-26) and running the `matchPayments` activity of Architecture v5 slides 17, 22, 31 and 44;
- the match of a `proceeds` receipt to the settlement treatment of the case, written in schema `rwb_payment`: `matched_to` moves to `SETTLEMENT` of `LOV-MATCH` from the source in `LOV-PROCEEDS-SRC` of DF-FIN-005 (TSD P8 T3.1 and T3.2);
- the read of the settlement treatment on the rwb-treatment contract `GET /treatments/{treatmentId}` (S2) and of the case reference on the rwb-case contract (P3), one hop each;
- the local decision record of every rule outcome, written through RWB-PLT-E1027-CON before the proceeds row changes, and MSG-P7-003 when it cannot be written (DP-03; legacy AC1 and AC2);
- the publication of `ProceedsMatched` (EV-25, `rwb.payment.ProceedsMatched.v1`) on `rwb.payment.events.v1` in the same transaction as the row, through the outbox;
- the behaviour behind `GET /proceeds` (API-P8-001) and `POST /proceeds/{proceedsId}/match` (API-P8-002) on base `/api/recovery/payment/v1` (DP-13), and SCR-28 Proceeds matching in its loading, matched and unmatched states through the gateway-bff composite route (DP-19).

It does not own: the published shapes of the two operations, the event schemas, the error set and the fakes, which are RWB-P8-E4043-CON; the treatment, the settlement agreement and its plan timers, which are rwb-treatment (S2); the case of record and its route states, which are rwb-case (P3); the ACE payment facts behind `v_ace_payment`, which are rwb-source-data (P1); the rule package, its version and its rule rows, which are governed in rwb-decision (P7); the posting of the booking to ALS and to the general ledger and the posting file, which are the posting stories of this service; and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E4-043 gave the Workbench one step between a signed settlement and a closed money side: the receipt that arrives after the agreement is matched to the treatment, the money side closes, and the outcome is recorded on the decision log with the rule version. The FSD keeps the feature as FEAT-PAY-03 in module P8 with the business objective "matches a settlement payment to the treatment and closes the money side", a matching step that runs unattended and a case owner who also uses it (FSD P8 A2.3.1 and A2.3.3.3), and a metric of receipts matched the same day, rising each month (FSD P8 A2.3.1). The problem it answers is unchanged: payments are matched to plans and settlements by hand, and broken plans are found late (FSD P8 A2.3.1).

What D-RCV-60 changes is who owns each part of that step.

- **the money and the match are this service's.** `proceeds` is P8's table in `rwb_payment` (Ownership Map row `proceeds`, owner P8; Architecture v5 slide 41, "payment and proceeds matching, fees, bookings, posting files"). The receipt, its source, its amount, its value date and what it was matched to are written here and nowhere else (TSD P8 T3.1, DF-FIN-001 to DF-FIN-009).
- **the treatment stays with rwb-treatment (S2).** The settlement agreement, its terms and its plan timers are S2's (Architecture v5 slide 41; Ownership Map row `treatment`, owner S2). This story reads the treatment on the owner's contract and writes no treatment row and no plan timer.
- **the case stays with rwb-case (P3).** `recovery_case` and its route states are P3's. This story evaluates the rules, writes the proceeds row, records the decision and answers, and the parent `CaseWorkflow` moves the case of record.
- **the ACE facts stay with rwb-source-data (P1).** The legacy data table reads `v_ace_payment` (DF-ACE-043 to DF-ACE-054) in process. In the target only rwb-source-data holds SELECT on the `recovery.v_ace_*` views (Architecture v5 slide 29), so DP-05 applies as a prohibition and the receipt facts arrive on P1's contract; the conflict is recorded as GAP-2512 with ASM-4161.
- **the decision is recorded first.** One record per rule outcome, through the local decision-record library and the shared topic `rwb.decision-record.v1`, in the same transaction as the proceeds row, and a failed write changes nothing and shows MSG-P7-003. That is what legacy AC1 and legacy AC2 ask for, and it is the rule of DP-03.
- **the money side is announced once.** Architecture v5 slide 42 (row 11 and row 12) and slide 43 (row 25) give rwb-payment three events; the settlement match produces `ProceedsMatched`, which rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee consume. `TreatmentBooked` and `PaymentMissed` belong to the booking and plan-matching arm of JOB-07, which is RWB-P8-E2008-APP.

The legacy criteria are kept exactly, and they are thin: the legacy AC1 says "the data and the rule version this feature needs are in place / its trigger arrives", and the legacy test cases carry no settlement-specific data (GAP-2510; ASM-4159). Everything the legacy does not state — the trigger, the outcome fields, the rule package and its rule IDs, the thresholds — is filled from FSD P8 A2.3 and TSD P8 where a source has it, and is held as a placeholder where no source does (GAP-2511; ASM-4160).

### 3. Preconditions

- RWB-P8-E4043-CON is published: the two operations on `/api/recovery/payment/v1`, the `Proceeds`, `ProceedsPage` and `MatchRequest` elements, the three event schemas on `rwb.payment.events.v1`, the table baseline, the error set and the fakes are baselined and handed to this story.
- `proceeds` exists in schema `rwb_payment` with DF-FIN-001 to DF-FIN-009 and the standard record columns of TSD P8 T3.0, from the DB story of this service; this story adds no table, no column and no migration.
- `AceDataReady` (EV-26) is published by rwb-source-data on `rwb.source-data.events.v1` and starts the JOB-07 workflow (Architecture v5 slides 31 and 44); the source `ALS` of the batch is the one FSD P8 A2.3.4.4 names.
- The payment and receipt facts of the case are answered on the rwb-source-data contract, because this service holds no `v_ace_*` grant (Architecture v5 slide 29; GAP-2512; ASM-4161). The operation name of that read is Not specified in the source documents (GAP-2511; ASM-4160) and the row is not in this story's contract-dependency list, which is None.
- `GET /treatments/{treatmentId}` of rwb-treatment (S2) answers the settlement treatment of the case, with the treatment type, its terms and its status, for the fake (Ownership Map row `GET /treatments/{treatmentId}`, owner S2; TSD P8 T3.3).
- The case reference and its state on the rwb-case contract (P3) are available for the fake, and no case row is read as a table (Ownership Map row `recovery_case`, owner P3).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- The PAYMENT_MATCH package is in force at its version; the Settlement package rules R-SET-13, R-SET-14, R-SET-21, R-SET-23 and R-SET-24 are the rows that touch the settlement money side, of which R-SET-14 is the transition that matches the payment (AWAITING_PAYMENT to PAYMENT_CLEARED, amount_received = settlement_amount) (Business Rules and Routing Logic v4). The package, its rule rows and its version are authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce` (EV-30). No source gives the package code or the rule IDs of the settlement match itself: Not specified in the source documents (GAP-2511; ASM-4160).
- RWB-PLT-N001-CON is published: SCR-28 reaches this service through the gateway-bff composite route, one hop, and no screen calls the service directly (DP-19).
- The capability area "Write-off and posting" and its rights R and U exist as access rows of rwb-access, and the service runs as its own login on schema `rwb_payment` with no grant on another `rwb_*` schema (TSD P8 T6.1; Architecture v5 slide 29).
- No approval is needed to build against a Draft contract baseline, and no human verification stop is part of this run.

### 4. Flow

1. `AceDataReady` for business date D arrives on `rwb.source-data.events.v1`; the inbox of this service writes its processed-event row in the same transaction as its own change, and a redelivery is a no-op (DP-09; Architecture v5 slides 22 and 31).
2. The JOB-07 event-started workflow starts on queue `rwb-payment` with the business date and the source `ALS` (Architecture v5 slide 44; FSD P8 A2.3.4.4).
3. The `matchPayments` activity reads the receipts of the business date on the rwb-source-data contract, one hop with a 2 s budget and a breaker, and holds when the data product is stale (VR-P8-003-1, MSG-P1-001).
4. For each receipt whose `matched_to` is `UNMATCHED`, the activity reads the candidate case and, where the receipt is a settlement, the settlement treatment on `GET /treatments/{treatmentId}` of rwb-treatment; no treatment row and no case row is read as a table (DP-01, DP-05).
5. The activity loads the PAYMENT_MATCH package version in force, from `RulePackageInForce` or from the rwb-decision contract, and evaluates the settlement arm against the receipt, the treatment, the case and the reference data of `LOV-MATCH` and `LOV-PROCEEDS-SRC` (DP-04; BR-P8-003).
6. The decision is written before anything changes: one record through the local decision-record library, with the case reference, the proceeds reference, the treatment reference, the rule ID, the package version in force, the inputs reference, the outcome and the decided-at time (DP-03).
7. A failed record write stops the step: nothing is written, the receipt stays unmatched, MSG-P7-003 is raised and an incident is opened (legacy AC2; FSD P8 A2.3.4.3).
8. The proceeds row is written in one `rwb_payment` transaction with the record, the inbox row and the idempotency row: `matched_to` = `SETTLEMENT`, the `treatment_id` of DF-FIN-003, the `account_payment_id` of DF-FIN-004 where the receipt carries one, and the posting reference of DF-FIN-009 left to the posting story (TSD P8 T3.1).
9. `ProceedsMatched` (EV-25) is written to the outbox in the same transaction and relayed to `rwb.payment.events.v1` by the outbox relay, with key `caseId`, the CloudEvents envelope and no personal data (Architecture v5 slides 22 and 42; DP-09).
10. The step answers the money-side close with the rule ID and the version that produced it. No source publishes a case move, a state name or an outcome code for the settlement arm: Not specified in the source documents (GAP-2511; ASM-4160), and the answer is held to the rule ID, the version and the decided-at time until rwb-case confirms one.
11. A repeated `ProceedsMatched` source fact, a repeated `AceDataReady` or the same `Idempotency-Key` on `POST /proceeds/{proceedsId}/match` writes once, records once and counts the repeat (Architecture v5 slide 11; TSD P8 T-A.2).
12. SCR-28 Proceeds matching reads `GET /proceeds` filtered by match status and date range, paginated, through the gateway-bff composite route, and the manual match on the screen calls `POST /proceeds/{proceedsId}/match` with a `MatchRequest` and an `Idempotency-Key` (DP-13, DP-19; TSD P8 T-A.2).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written (library failure, stopped hash chain, outbox failure) | The transaction writes nothing: no proceeds change, no event, no answer; an incident is opened | MSG-P7-003 | AC2, TC-E4-043-02, TC-E4-043-04 |
| X2 | The role does not hold the Write-off and posting right R for `GET /proceeds` or U for `POST /proceeds/{proceedsId}/match` | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E4-043-03 |
| X3 | The ACE data product is stale after a late or failed batch for source `ALS` | The step holds, writes nothing, shows the data date and resumes on the next fresh answer | MSG-P1-001 | AC1 |
| X4 | The rwb-treatment, rwb-case or rwb-source-data contract does not answer inside 2 s, or its breaker is open | The activity retries on the workflow's own backoff; nothing is written and no event is published; `GET /proceeds` answers 503 with the platform error envelope | None | AC1 |
| X5 | No settlement treatment answers for the case, or the receipt is not of a settlement source | The settlement arm does not fire, the receipt stays `UNMATCHED` for the exception list of RWB-P8-E2027-APP, and nothing is written | None | AC1 |
| X6 | The receipt is already matched, or the operation is repeated with the same `Idempotency-Key` | The stored answer is returned, no second row and no second event, and the repeat is counted | None | AC1 |
| X7 | The rule package in force carries no settlement arm, or its version cannot be loaded | The step holds and writes nothing; the package and its release are P7's | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case`, `treatment` or `decision_log_entry` row, or another `rwb_*` schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR8 |

X1 and X2 are the exception paths of the legacy key and of FSD P8 A2.3.4.3 carried onto the split; X3 to X7 are the paths the target call types, the consumed event and the rule package add; X8 is the DP-01 and DP-05 boundary. Every threshold, list value and tolerance is reference data or a rule row in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-P8-E4043-CON, the rwb-source-data, rwb-treatment and rwb-case fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P7 or S2 |
| Negotiable | The workflow and activity names, the consumer group, the outcome code and the shape of the money-side answer are this story's choice; the two operations, the LOV values, the columns, the messages and the screens are fixed |
| Valuable | The settlement receipt is matched and the money side closes the morning after the ACE load, and the outcome is on the decision log with the rule version the same day |
| Estimable | One workflow arm, one activity, one event consumer, one evaluator, one record write, one row change, four clients and two read-only screen states |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic receipts and treatments through the contract fakes, plus the access case and the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Match a settlement payment

  Background:
    Given case "RC-2026-000431" carries settlement treatment "TR-2026-000431" with receipt "PR-2026-000431" of source CUSTOMER on the business date
    Given the PAYMENT_MATCH package is in force at its version and the lists LOV-MATCH and LOV-PROCEEDS-SRC are read with their version
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Match a settlement payment (legacy RWB-E4-043 AC1)
    Given the rwb-treatment contract mock returns the settlement treatment for the case
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then matches a settlement payment to the treatment and closes the money side
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-043 AC2)
    Given the rwb-decision contract mock returns a failed decision-log write
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E4-043 word for word, with their origin tag added and nothing else changed: the legacy wording of `its trigger arrives`, `the action is taken` and `the decision log cannot be written` all stand. One leading `Given` is added to each, and those two lines are the only additions: AC1 needs the settlement treatment, which is rwb-treatment's fact, and AC2 needs the failed write of the decision-record library, which is the rwb-decision and platform library boundary. What the legacy lines describe happens in four places in the target: rwb-source-data answers the receipt of the ACE batch, rwb-treatment answers the settlement treatment, this story matches the receipt, writes the proceeds row, records the decision and publishes `ProceedsMatched`, and rwb-case applies the money-side answer to the case of record. Because the legacy criteria are generic, the settlement detail behind them is filled from FSD P8 A2.3 and TSD P8 and is recorded as GAP-2510 with ASM-4159, and every value no source carries is held as GAP-2511 with ASM-4160.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| VR-P8-003-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) raises MSG-P1-001 `{product} is from {date}. Today's ACE batch has not arrived.` | FSD P8 A2.3.3.1, copied character for character |
| BR-P8-003 | No value a business person may change is written in code; it is read from reference data with its version | FSD P8 A2.3.3.1, copied character for character |
| BR1 | The receipt and its match are this service's: `proceeds` in `rwb_payment` carries the case, the treatment, the account payment, the source, the amount, the received date, `matched_to` and the posting reference, and no other service writes them | Architecture v5 slide 41 (rwb-payment owns payment and proceeds matching); Ownership Map (`proceeds` owner P8); TSD P8 T3.1 |
| BR2 | A settlement receipt closes to `SETTLEMENT` of `LOV-MATCH` and its source is one value of `LOV-PROCEEDS-SRC`; no other match value may be written by this step | TSD P8 T3.2; FSD P8 A2.3.2 |
| BR3 | The decision is recorded before the row changes, one record per rule outcome, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; legacy RWB-E4-043 AC1 and AC2; FSD P8 A2.3.4.3 |
| BR4 | The trigger is the completion of the ACE batch of source `ALS`, read through the batch status of rwb-source-data; the settlement arm runs inside the JOB-07 event-started workflow, not on a Quartz schedule and not on a shared job table | FSD P8 A2.3.4.4; Architecture v5 slides 31 and 44 |
| BR5 | The payment facts of ACE stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the receipt on the owner's contract only | DP-05; Architecture v5 slide 29; GAP-2512 |
| BR6 | The treatment stays with rwb-treatment and the case with rwb-case: the treatment is read on `GET /treatments/{treatmentId}`, and no `treatment`, `recovery_case`, `assignment`, `task` or `timer` row is written here | Ownership Map (treatment owner S2, recovery_case owner P3); Architecture v5 slide 41 |
| BR7 | The money side is announced once: `ProceedsMatched` is written to the outbox in the same transaction as the row and relayed with key `caseId`, and this step publishes no other event | Architecture v5 slides 22, 42 and 43; DP-09 |
| BR8 | No cross-schema join and no foreign key leaves `rwb_payment`; `case_id`, `treatment_id` and `account_payment_id` are identifiers of other services' facts | DP-01; TSD P8 T3.3 |
| BR9 | The same fact twice, or the same `Idempotency-Key` twice, writes once, records once and counts the repeat | Architecture v5 slide 11; TSD P8 T-A.2 |
| BR10 | The rule rows of the settlement arm — R-SET-14, the transition that matches the payment and posts it, and R-SET-13, R-SET-21, R-SET-23 and R-SET-24 around it — are governed in rwb-decision and named here, never declared here; the package code, the rule IDs of the matching mechanism and its tolerance and window rows appear in no source: Not specified in the source documents (GAP-2511; ASM-4160) | Business Rules and Routing Logic v4; Temporal and Drools Design slide 18 (PAYMENT_MATCH replaces payment_match_rule); GAP-2511 |
| BR11 | No person name, address, contact value or identity number enters `rwb_payment`, the decision record, the `ProceedsMatched` payload, a log or a workflow input | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |

The two rows VR-P8-003-1 and BR-P8-003 are the rows of FSD P8 A2.3.3.1, copied character for character; the rest are the rules the target split fixes. The rule rows of the settlement arm are P7's, and the match itself has no published rule ID or package code, which is why BR10 carries the placeholder rather than an invented rule.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers and the parent `CaseWorkflow` applies the move to the case of record (BR6). What this story owns is the match state of the receipt and the state of the step.

| From (`proceeds.matched_to`) | Event | Condition | To |
|---|---|---|---|
| `UNMATCHED` | The settlement arm fires under the PAYMENT_MATCH package | The settlement treatment answers and the source is a value of `LOV-PROCEEDS-SRC` | `SETTLEMENT`, with the record and the `ProceedsMatched` outbox row |
| `UNMATCHED` | The settlement arm fires | The treatment does not answer for the case (X5) | `UNMATCHED`, nothing written |
| `UNMATCHED` | The decision record cannot be written (X1) | The library refuses | `UNMATCHED`, nothing written, MSG-P7-003 and an incident |
| `UNMATCHED` | The rule package or its version cannot be loaded (X7) | The package in force carries no settlement arm | `UNMATCHED`, held |
| `SETTLEMENT` | The same receipt or the same `Idempotency-Key` again (X6) | The stored answer is returned | `SETTLEMENT`, no second row, the repeat counted |
| `SETTLEMENT` | The posting story writes the posting reference | DF-FIN-009 is filled by the posting step | `SETTLEMENT`, the posting reference set, unchanged by this story |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | `AceDataReady` for business date D | The inbox row is written | Reading the receipts |
| Reading the receipts | The data product answers fresh | The settlement treatment answers | Evaluating |
| Evaluating | The settlement arm fires | The decision record is written | Writing |
| Writing | The row, the record, the inbox row and the outbox row commit | The transaction commits | Waiting for the next fact |
| Writing | The record write or the transaction fails (X1) | No commit | Waiting, nothing changed |
| Reading the receipts | The data product is stale (X3) | VR-P8-003-1 | Held, until a fresh answer |

The match values `INSTALLMENT`, `SETTLEMENT`, `FEE`, `SALE_PROCEEDS` and `UNMATCHED` are those of `LOV-MATCH` in TSD P8 T3.2 and are read with their version; this story writes `SETTLEMENT` only.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: matches a receipt and reads the proceeds list |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: matches a receipt, reads the proceeds list and approves where the flow needs it |
| SY-DATALOAD, data load from COLLINS | Write-off and posting U: matches a receipt |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE, RW-FINANCE, RW-PRODHEAD, RW-WOCOMM | Write-off and posting R, and RA where the matrix gives it: read only, in scope, through SCR-28 |
| SY-CASEWF, SY-RULES, SY-AGENT | Write-off and posting R: the service identities run inside the same checks as a person |
| rwb-payment service identity | Runs the workflow and the activity, consumes `AceDataReady`, writes the decision record, the proceeds row and the outbox row, and publishes `ProceedsMatched`; it holds no grant on another schema and no `v_ace_*` grant |
| Case owner | Also uses the feature: reviews the matched and unmatched receipts of the case on SCR-28, with no wider right than the matrix gives |

The rights are the rows of TSD P8 T6.1 and of the legacy permission table of this key, and nothing wider. The step runs unattended under the service identity (FSD P8 A2.3.3.3, "None; runs unattended" as the primary use), and the capability area "Write-off and posting" and its rights are declared per operation. DP-08 is not in this story's pattern set: the right is declared by the contract and checked by the guard of the service template, so it is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-001 to DF-FIN-009 | proceeds (P8, `rwb_payment`) | `id`, `case_id`, `treatment_id`, `account_payment_id`, `source`, `amount`, `received_date`, `matched_to`, `posting_ref` | Write the match: `matched_to`, `treatment_id` and `account_payment_id`; the posting reference is left to the posting story |
| TSD P8 T3.0 standard columns | proceeds (P8, `rwb_payment`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, with the optimistic lock of `version` |
| DF-TRT-001 to DF-TRT-014 | treatment (S2) | `id`, `case_id`, `decision_log_id`, `treatment_type`, `proposed_by`, `proposed_at` and 8 more | Read on `GET /treatments/{treatmentId}` only; never as a table |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | `id`, `case_no`, `product_group`, `primary_person_key`, `status`, `stage_code` and 17 more | Read on the rwb-case contract only; never as a table |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` (P1) | `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel`, `capital_amount` and 6 more | Not read: this service holds no `v_ace_*` grant; the receipt arrives on the rwb-source-data contract (BR5) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_payment`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, one record per rule outcome, before the row changes |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | `id`, `rule_id`, `rule_version`, `route_set`, `from_state`, `event_code` and 9 more | Not read and not written: the rule rows are governed in rwb-decision and loaded with the package |
| - | `payment_match_rule` (P7, by the Temporal and Drools design) | The rule rows of the match, replacing the legacy table | Not read as a table: evaluated from the package in force (BR10) |

Field IDs are those of TSD P8 Payments and posting v2 T3.1 and of the legacy data table of RWB-E4-043, with their owners changed by the target. **No new table, no new column and no migration**: `proceeds` arrives with the DB story of this service, and `decision_record`, `outbox_event`, `processed_event` and `idempotency_key` are platform library objects created in `rwb_payment` by the library's own migration (DP-03, DP-09). The outcome fields, the match thresholds, the tolerance and the window of the settlement arm are Not specified in the source documents (GAP-2511; ASM-4160) and are held as rule rows and reference data, never as columns invented here.

**No personal data.** The rows this story writes carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_payment`, the decision record, the `ProceedsMatched` payload, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8); base `/api/recovery/payment/v1` (DP-13). This story supplies the behaviour behind the two operations whose shapes are declared by RWB-P8-E4043-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | `ProceedsPage` out, filtered by `matched`, `from` and `to`, paginated by `page` and `size` (API-P8-001) | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | `MatchRequest` in, `Proceeds` out with the match outcome (API-P8-002) | Write-off and posting, right U, scope applied | `Idempotency-Key` header required; the answer is stored |

The two operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope proceeds reference, 409 on a receipt that is already matched, 422 with MSG-GEN-001 for an invalid field and 503 when the decision library or a consumed contract does not answer. The identifiers, paths and rights are those of TSD P8 T-A.1 and T-A.2, and the base is the target form of the monolith path and not the monolith form. `GET /cases/{id}/payments` of Architecture v5 slide 17 and the manual `POST /proceeds/{id}/allocate` of the same slide are read as this family: `/allocate` is the manual form of the match of API-P8-002 and `GET /cases/{id}/payments` is a case-scoped view of the same receipts, whose operation is Not specified in the source documents (GAP-2511; ASM-4160).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /treatments/{treatmentId}` | `/api/recovery/treatment/v1` | S2 rwb-treatment | The settlement treatment of the case: its type, its terms and its status; faked |
| The case read and the money-side answer (operation names Not specified in the source documents (GAP-2511; ASM-4160)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its product group and its route state; the answer that carries the rule ID and the version that closed the money side; faked |
| The payment-fact read of the ACE batch (operation name Not specified in the source documents (GAP-2511; ASM-4160)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The receipts of the business date for source `ALS`, with the freshness stamp of the data product; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-2511; ASM-4160)) | `/api/recovery/decision/v1` | P7 rwb-decision | The PAYMENT_MATCH package at the version in force and its rules; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, so this story builds against their published documents and fakes on Day 1 (GAP-2513; ASM-4162).

#### 12.3 Events published

| Event | Topic | Payload used | When |
|---|---|---|---|
| `ProceedsMatched` (`rwb.payment.ProceedsMatched.v1`, EV-25) | `rwb.payment.events.v1`, with its `.retry` and `.dlt` topics | The case reference, the proceeds reference, the treatment reference, the amount, the value date, the match value `SETTLEMENT` and the rule ID with its version; CloudEvents 1.0, key `caseId`, no personal data | In the same transaction as the proceeds row, through the outbox, when the settlement arm closes the money side |

`ProceedsMatched` is event 25 of Architecture v5 slide 43, produced by rwb-payment and consumed by rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee. `TreatmentBooked` (EV-11) and `PaymentMissed` (EV-12) are published by the booking and plan-matching arm of JOB-07, which is RWB-P8-E2008-APP, and this step publishes neither. The enqueue is the outbox row of the same transaction and the relay publishes with an idempotent producer (Architecture v5 slide 22).

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When |
|---|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1`, with its `.retry` and `.dlt` topics | `rwb-payment.match-run.v1` | The business date and the source `ALS` of the completed batch; CloudEvents envelope; deduped in the inbox on the event id | On the outbox relay of rwb-source-data; starts the JOB-07 workflow |
| `TreatmentApproved` (EV-10) | `rwb.treatment.events.v1` | `rwb-payment.match-run.v1` | The case reference, the treatment reference and its type, so a settlement treatment that arrives after the batch is matched without waiting for the next load; deduped in the inbox | On the outbox relay of rwb-treatment |
| `RulePackageInForce` (EV-30) | `rwb.decision.events.v1` | `rwb-payment.match-run.v1` | The package code and the version in force; deduped in the inbox | On the outbox relay of rwb-decision, and at every step start from the package read |

`DecisionRecorded` (EV-08) is written by all nineteen services on the shared topic `rwb.decision-record.v1`, and its consumers are rwb-decision and rwb-reporting (Architecture v5 slide 42, row 08). This service is a **producer** of that topic through the local library of DP-03 and not a consumer of it: 12.3 carries no row for it, because the record is relayed by the library and is not an event of this service's own topic.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `PaymentMatchingWorkflow` | Workflow, one execution per business date and source, event-started by `AceDataReady` (the JOB-07 replacement of Architecture v5 slide 44) | `rwb-payment` in namespace `rwb-recovery` | Input: the business date, the source and the package in force; signals: `AceDataReady`, `TreatmentApproved`, `RulePackageInForce`; the settlement arm is one stage of it |
| `matchPayments` | Activity, the one matching step of this story (Architecture v5 slide 17, "Act: matchPayments") | `rwb-payment` | The receipts, the case and the treatment in; the rule ID with its package version, the match outcome, the record, the row and the outbox event out, in one transaction |

`postProceeds` is the saga step named on the same queue (Architecture v5 slide 17; Temporal and Drools Design, activity contracts `Payment.postProceeds`), and it is the posting story's activity and not this one's: the settlement money side closes here and the posting to ALS and to the general ledger happens there, which is why this step writes no posting reference. The workflow name and the consumer group name are this story's choice; no source document names them, and the activity name is the one the architecture gives.

#### 12.6 Schedules

None. JOB-07 is an event-triggered workflow started by `AceDataReady` and not a Temporal Schedule (Architecture v5 slide 44), so this story declares no Schedule, no Quartz row and no shared job table. The Schedules of this service belong to the batch stories of the service and are not owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| proceeds | P8 (`rwb_payment`) | The receipt and its match; this story writes the match, the treatment reference and the account payment reference |
| decision_record | PLT library, created in `rwb_payment` | The local hash-linked decision record, one per rule outcome (DP-03) |
| outbox_event | PLT library, created in `rwb_payment` | The `ProceedsMatched` row of the same transaction (DP-09) |
| processed_event | PLT library, created in `rwb_payment` | The inbox row of each consumed event and its dedupe key (DP-09) |
| idempotency_key | PLT library, created in `rwb_payment` | The key of the repeated `POST /proceeds/{proceedsId}/match` and the answer it holds |

Not owned and never read as a table: `treatment` (S2), `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `payment_match_rule` (P7), the ACE views (P1), and the fee, booking and posting tables of this service, which are the sibling stories'. No foreign key leaves the schema and `proceeds.case_id`, `proceeds.treatment_id` and `proceeds.account_payment_id` are identifiers, not foreign keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data payment-fact fake | The receipts of business date D for source `ALS`, one of them a settlement receipt for case `RC-2026-000431` and treatment `TR-2026-000431`; a stale product with its date; no answer beyond 2 s | AC1, X3, X4 |
| rwb-treatment settlement fake | The settlement treatment `TR-2026-000431` of case `RC-2026-000431` with its type, terms and status; no treatment for a case without one | AC1, X5 |
| rwb-case case fake | The case `RC-2026-000431` with its product group and route state; an accepted and a refused money-side answer | AC1, X4 |
| rwb-decision package fake | The PAYMENT_MATCH package at its version in force with the settlement arm; a package without a settlement arm | AC1, X7 |
| rwb-source-data event fake | `AceDataReady` for business date D and source `ALS`, the same event twice, and an event for an empty batch | AC1, X6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-28 answer for the case, with the proceeds list of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data payment read, of the rwb-case answer and of the rwb-decision package read are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2511; ASM-4160).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | `GET /proceeds` and `POST /proceeds/{proceedsId}/match` on `/api/recovery/payment/v1`; the rwb-treatment treatment read, the rwb-case case read and answer, the rwb-source-data receipt read and the rwb-decision package read; one hop, 2 s |
| Kafka | 1 published, 3 consumed | `ProceedsMatched` on `rwb.payment.events.v1`; `AceDataReady`, `TreatmentApproved` and `RulePackageInForce` in consumer group `rwb-payment.match-run.v1`; the decision record is relayed by the library on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity | `PaymentMatchingWorkflow` and `matchPayments` on `rwb-payment`; no Schedule |
| File | None | No file is read, built or delivered here; the posting file is the posting story's (Architecture v5 slide 17, "Integration: deliverFile (posting file)") |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `matching`, Java package `th.co.scb.ace.workbench.recovery.payment.matching`; front end `src/modules/recovery/payment/ProceedsMatching.tsx`, the fragment SCR-28 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: rwb-payment holds no `v_ace_*` grant, because only rwb-source-data has SELECT on the views (Architecture v5 slide 29), so the receipt facts arrive on the owner's contract and the legacy `v_ace_payment` read is retired (GAP-2512; ASM-4161). DP-03 is the transaction rule of the step: each record, the proceeds row, the inbox row and the outbox row commit together or not at all. DP-13 moves the base of the two operations and nothing else, and DP-19 is how SCR-28 reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The pattern table adds the two H rows `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, which the plan already carries for this story; the four consumed rows of 12.2 are contract dependencies of class C that the plan's C row does not list, because that row is None, so they are built against their documents and fakes on Day 1 and the difference is recorded (GAP-2513; ASM-4162). The inbox and the outbox of the consumed and published events are the platform library of DP-09, which adds no H row to this list.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PaymentMatchingWorkflow` settlement arm | Workflow | The stage of JOB-07 that waits for the receipts of the business date and reports the outcome to its caller |
| `matchPayments` | Activity | The one step: read the receipts, the case and the treatment, evaluate the settlement arm, write the record, the row and the outbox event |
| `PaymentEventConsumer` | Inbox adapter | Consumes `AceDataReady`, `TreatmentApproved` and `RulePackageInForce` in group `rwb-payment.match-run.v1`, writes the `processed_event` row and dedupes |
| `SettlementMatchEvaluator` | Service | The settlement arm of the PAYMENT_MATCH package, against the receipt, the treatment and the case |
| `PaymentDecisionRecordWriter` | Library adapter | Writes one decision record per rule outcome before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `ProceedsWriter` | Repository | Writes `proceeds` in one `rwb_payment` transaction, with the idempotency row and the optimistic lock |
| `ProceedsMatchedPublisher` | Outbox adapter | Writes the `ProceedsMatched` outbox row in the same transaction and leaves the relay to the library (DP-09) |
| `CaseAnswerClient` | Client | The case read and the money-side answer, one hop, 2 s, breaker |
| `TreatmentClient` | Client | `GET /treatments/{treatmentId}` of rwb-treatment, one hop, 2 s |
| `PaymentFactClient` | Client | The receipt read of rwb-source-data, one hop, 2 s, with the freshness stamp |
| `RulePackageClient` | Client | The PAYMENT_MATCH package read of rwb-decision, one hop, 2 s |
| `ProceedsController` | Controller | The two operations, the capability area and right, the pagination, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `ProceedsMatching` | React component | Shows the matched and unmatched receipts on SCR-28, read only, with the refusal, the hold and the not-recorded states |

**Database and migrations.** No Flyway file of this story. `proceeds` arrives with the DB story of this service, and the decision record, the outbox, the inbox and the idempotency key are library objects created in `rwb_payment` by the library's migration (DP-03, DP-09). No column is added for the outcome, the threshold or the tolerance: where the TSD P8 T3.1 names none, the value is Not specified in the source documents and stays a rule row or reference data rather than an invented column (GAP-2511; ASM-4160).

**Configuration and reference data.**

- `LOV-MATCH` and `LOV-PROCEEDS-SRC` at their version in force (TSD P8 T3.2), read as reference data and never as constants.
- The PAYMENT_MATCH package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the thresholds and the tolerance of the settlement arm are values of the package and not of this build.
- The capability area "Write-off and posting" and its rights R and U are access rows of rwb-access, read through the guard.
- The consumer group `rwb-payment.match-run.v1` and the three subscriptions are configuration of the inbox library.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The settlement arm of `PaymentMatchingWorkflow` and its input record, registered on `rwb-payment`, with `AceDataReady` as its trigger (AC1).
2. `PaymentEventConsumer` and the inbox row, with the duplicate and redelivery paths (AC1, X6).
3. `PaymentFactClient`, `TreatmentClient`, `CaseAnswerClient` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker, the stale-data path and the no-answer path (AC1, X3, X4).
4. `SettlementMatchEvaluator` over the PAYMENT_MATCH package, with the settlement arm, the unmatched path and the missing-arm path (AC1, X5, X7).
5. `PaymentDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
6. `ProceedsWriter` with the one transaction, the match columns, the idempotency row and the optimistic lock (AC1, X6).
7. `ProceedsMatchedPublisher` and the outbox row, with the relay of the library (AC1).
8. `ProceedsController` with the rights, the pagination, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1).
9. `ProceedsMatching` and SCR-28 in its loading, matched and unmatched states through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_payment`, no `v_ace_*` read, no write to `rwb_case`, `rwb_treatment` or `rwb_decision`, and no Schedule (X8, BR5, BR6).

**Feature flag.** `rwb.payment.settlement-match-v1`, read as a flag of the platform library; off means the consumer writes the inbox row and holds the receipts, writes no row and publishes no event, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the settlement arm runs from a synthetic `AceDataReady` in SIT, a settlement receipt closes to `SETTLEMENT` with its record and its event, a non-settlement receipt stays unmatched, a repeated fact writes once, a forced record failure changes nothing, no `v_ace_*` read and no foreign row write exists in the build, and SCR-28 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the `MatchRequest` is absent or invalid, or the receipt cannot be read | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right reads the proceeds list or attempts the match | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the proceeds row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of source `ALS` is stale after a late or failed batch (VR-P8-003-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The four message IDs are those of the legacy message set of this key and of FSD P8 A2.3.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P7-003 is the message of legacy AC2 and of FSD AC-EXC-P8-003-02, and MSG-P4-002 is the message of TC-E4-043-03 and of FSD AC-EXC-P8-003-01.

### 15. Screens and states

SCR-28 Proceeds matching is served through the gateway-bff composite route (DP-19). The route calls rwb-payment for the proceeds list and the match, rwb-case for the case and its route state and rwb-treatment for the settlement treatment; this story fixes the rwb-payment answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The three states named by the legacy screen are the ones this step produces: **loading** while the receipts of the business date are read on the rwb-source-data contract, **matched** when the settlement arm has closed the money side and the record, the row and the event are committed, and **unmatched** when no settlement treatment answers or the receipt is not a settlement, in which case the receipt goes to the exception list of RWB-P8-E2027-APP. The refusal and failure states shown on the same screen are the refused state with MSG-P4-002, the not-recorded state with MSG-P7-003 and the stale-data state with MSG-P1-001, each read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-043-01 | AC1 | Component | Case `RC-2026-000431`, settlement treatment `TR-2026-000431` and receipt `PR-2026-000431` of source `CUSTOMER`; the row closed to `SETTLEMENT`, the decision record with the rule ID and version, and the `ProceedsMatched` outbox row asserted on the fakes |
| TC-E4-043-02 | AC2 | NFR | The decision-record stub stopped; nothing written, no event, MSG-P7-003 shown and an incident opened |
| TC-E4-043-03 | Access | Contract | A role without the Write-off and posting right R or U; 403 with MSG-P4-002 on both operations and no read |
| TC-E4-043-04 | Principle 5 | NFR | A forced decision-log write failure at the moment of the proceeds write; no row, no event, no answer, and the repeat writes once when the library recovers |

The four test cases are the legacy cases of RWB-E4-043 in their legacy order, with the Level column added: TC-E4-043-01 is the component proof of the step on its fakes, the two forced-failure cases map to NFR because they prove the atomicity and the no-side-effect property of the transaction, and the access case maps to Contract because the artefact under test is the declared right of the operation. The legacy rows name no settlement-specific data, which is recorded as GAP-2510 with ASM-4159; the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID, and the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: `LOV-MATCH`, `LOV-PROCEEDS-SRC`, the match thresholds, the tolerance, the window and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_payment`, in the `ProceedsMatched` payload, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract or a `v_ace_*` view this service holds: it holds none, because only rwb-source-data has SELECT on the views, so the receipt arrives on P1's contract and a build that adds a view or an ACE table read fails the boundary test (DP-05; Architecture v5 slide 29).
- The treatment stays with rwb-treatment and the case with rwb-case: no `treatment`, `recovery_case`, `assignment`, `task` or `timer` row is written here, and no posting, no balance and no posting file is produced here (BR6).
- One base, one topic, one queue and one login per service: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login, and no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- The decision is recorded before the change and every consumed event is deduped in the inbox; a build that publishes or that changes a row before its record fails the review (DP-03, DP-09).
- No retired element is reintroduced: no shared Quartz table, no Quartz job, no monolith API base, no `recovery` schema read, and no data-lake copy of the match.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id for this slice; the requirement is FEAT-PAY-03 of the FSD P8 A2.3 and its main success criterion AC-P8-003-01, that a settlement payment is matched to the treatment and the result is recorded with its rule version (GAP-2510; ASM-4159) | The settlement arm, the proceeds row, the decision record and the `ProceedsMatched` event | TC-E4-043-01, TC-E4-043-02 |
| BR-P8-003 | No value a business person may change is written in code; it is read from reference data with its version (FSD P8 A2.3.3.1) | The lists and the package values read with their version | TC-E4-043-01 |
| VR-P8-003-1 | Data product stale after a late or failed ACE batch raises MSG-P1-001 (FSD P8 A2.3.3.1) | The freshness check of the receipt read | TC-E4-043-01, TC-E4-043-04 |
| ADR-013 | 19 services inside ACE | rwb-payment as the owner of the match and of the proceeds | TC-E4-043-01 |
| ADR-014 | Schema and login per service | `rwb_payment` and its own login, no cross-schema write | TC-E4-043-04 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `ProceedsMatched` outbox row and the inbox of the three consumed events | TC-E4-043-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E4-043-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the row changes, one per rule outcome | TC-E4-043-02, TC-E4-043-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-043, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Test cases | TC-E4-043-01 to TC-E4-043-04 |
| Feature and screens | FEAT-PAY-03 Match a settlement payment; SCR-28 Proceeds matching |
| Rules | PAYMENT_MATCH governed in rwb-decision, and R-SET-14 together with R-SET-13, R-SET-21, R-SET-23 and R-SET-24 of the Business Rules and Routing Logic v4 where the settlement money side touches them; the package code and the rule IDs of the matching mechanism are not published (GAP-2511; ASM-4160) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the two operations, the `Proceeds`, `ProceedsPage` and `MatchRequest` elements, the three event schemas, the table baseline, the error set and the fakes: RWB-P8-E4043-CON.
- The booking confirmation and the plan-installment matching that publish `TreatmentBooked` and `PaymentMissed`, and the exception list of an unmatched receipt: RWB-P8-E2008-APP and RWB-P8-E2027-APP.
- The posting of the settlement booking to ALS and to the general ledger, the posting file and the posted reference of DF-FIN-009: the posting stories of this service, API-P8-002 being the match and not the posting.
- The treatment, the settlement agreement, its terms and its plan timers: rwb-treatment (S2).
- The case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The ACE payment facts, the batch status and the freshness of the data product: rwb-source-data (P1).
- The PAYMENT_MATCH package, its rule rows, its version and its release: rwb-decision (P7).
- The roles, scopes and masking behind the Write-off and posting right: rwb-access (P4) and the guard of the service template.
- The gateway-bff composite route and the screen field list of SCR-28: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Change log: D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P8-E4043-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
