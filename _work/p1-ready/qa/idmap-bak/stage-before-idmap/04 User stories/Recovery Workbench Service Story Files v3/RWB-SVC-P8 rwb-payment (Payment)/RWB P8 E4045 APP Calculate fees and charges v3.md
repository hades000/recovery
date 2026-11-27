# RWB-P8-E4045-APP Calculate fees and charges

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-060, RD-P1-061, RD-P1-066: Use the source-data account, payment and batch-status contracts for the fee calculation.
- EV-26 is cited with its published record key and payload (RD-P1-003); the batch check of this run is unchanged.


| Item | Value |
|---|---|
| Story key | RWB-P8-E4045-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-045 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P8-E4045-APP-16); not yet recorded |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-P8-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Consumes rwb-source-data.yaml 5.1.0 on `/api/recovery/source-data/v1`; other contracts stay on their /v1 paths |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-060, RD-P1-061, RD-P1-066 |
| Integration dependencies | None |
| External dependencies | None |
| Personal data carried | Not specified in the source documents (DOR-RWB-P8-E4045-APP-11); the fields this story reads are classed as Data Classification v5 records them |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 25 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **finance and CFO delegate**, I want **the Workbench to work out partner fees, court fees and charges from the fee tables held as data**, so that **every payment and booking is matched to its case**.

This is the application slice of legacy RWB-E4-045, feature FEAT-PAY-05 of module P8 Payments and posting (FSD P8 A2.5; Epics 3 to 8 Specification v3). It owns:

- the one legacy acceptance criterion this slice keeps, AC2, copied word for word with its origin tag; AC1 of the key is owned by RWB-ITG-E4045-ITG;
- the fee-and-charge step of the payment run in rwb-payment: it takes a fee fact of a case — a partner fee, a court fee or a charge — works the amount out of the fee rows in force, read at their version, and records the answer before anything uses it (DP-03; FSD P8 A2.5; TSD P8 T3.1);
- the account fee facts from `GET /accounts/{accountKey}`, including `collectionsFee` (DF-ACE-024), and receipt facts from `GET /payments?businessDate={date}` (DP-05);
- the money side of the fee: a receipt that settles a fee is carried on the `proceeds` row of schema `rwb_payment` with `matched_to` FEE, one of the values of `LOV-MATCH`, so the fee is tied to its case, its treatment and its posting reference (DF-FIN-005 to DF-FIN-009);
- the record of every calculation — fee row identity, its version, the inputs and the answer, hash-linked to the previous record of the case — written before the row, both or neither (DP-03; R-UNI-39);
- SCR-28 Proceeds matching in its loading, matched and unmatched states with the fee rows in place, reached through the gateway-bff composite route (DP-19).

It does not own: AC1 of the legacy key, the end-to-end evidence of the fee across the services, which is RWB-ITG-E4045-ITG; the published shapes of the service's two operations, its three event schemas and the fakes, which are the baseline of RWB-P8-E2008-CON; the other P8 features, the matching of FEAT-PAY-01 above all, and the sibling stories of RWB-E4-043 to RWB-E4-049; the case, its stages and its tasks (P3); the legal-spend approval and its limit (S4); the work order and the sale behind a vendor or broker fee (S5); the partner (S9); the fee package, the rule rows and the central ledger (P7); and the ACE fee and payment facts (P1).

### 2. Business rationale

Fee arithmetic is where recovery money leaks and where an audit finding starts. A court fee, a panel law firm's fee, a property vendor's charge and a broker fee are worked out today by hand against a table nobody versions, and the FSD states the module's problem in one line: payments are matched to plans and settlements by hand, and broken plans are found late (FSD P8 A1.3, repeated in A2.5.1). The measure is the module's own: receipts matched the same day, rising each month, read from the decision log and the Workbench records (FSD P8 A2.5.1).

The routing logic says exactly when a fee falls due, in four different routes: a court fee or legal expense (R-LIT-41, event FEE_DUE, routed to the approver at D7.4), a work order at the vendor's fee schedule (R-DIS-10), a broker fee at acceptance (R-DIS-64) and an agency fee on a post-charge-off recovery (R-WO-37). Under D-RCV-60 each of those owners knows that a fee is due; none of them may hold the arithmetic, because the fee values are data rows of the Workbench and the money side is this service's. The calculation therefore sits in rwb-payment, reads the ACE fee facts on the service's own read path (DP-05) and records every answer locally (DP-03), so that a route owner, an approver and an auditor can see the fee that was raised, from which row and at which version — which is what the legacy criterion asserts when it says the result is written to the decision log with the rule version.

### 3. Preconditions

- The service runs unattended as primary; the Finance and CFO delegate uses the result (FSD P8 A2.5.3.3). A person reading the fee rows on SCR-28 holds right R in the capability area Write-off and posting (TSD P8 T6.1, T6.2); the legacy permission table of the key gives the same intent as right R on Case record.
- The fee fact identifies the source and business date. Read its batch row through `GET /batch-status` when needed. A late or failed batch holds the fee without raising an amount (VR-P8-005-1).
- The case and workflow capability the feature depends on is in place (legacy Depends on FEAT-CWC-23; FSD P8 A2.5 Prerequisites): the case, its product group and its stage are read on rwb-case's contract, never from its tables.
- The fee rows of the fee type are readable at a version, and no rate, flat amount, cap or validity is written in code (FSD P8 A2.5.3.1 BR-P8-005; GAP-2543; ASM-4202).
- The build dependencies are tagged: RWB-PLT-E1027-CON for the local decision record, RWB-PLT-N001-CON for the composite route of SCR-28.
- The fakes of the consumed reads answer the documented shapes, so the build never waits for another service (ADR-020; GAP-2543; ASM-4202).

### 4. Flow

1. Trigger. A fee fact arrives for a case: a court fee or legal expense falls due (R-LIT-41, FEE_DUE), a work order is raised on a held asset (R-DIS-10), a broker sale is agreed (R-DIS-64), or a post-charge-off recovery is placed with an agency (R-WO-37). The fact is consumed into the inbox of `rwb_payment` and deduped on its key (R-UNI-40).
2. The step reads the case on rwb-case's contract — product group, stage, amount basis — one hop with a 2 s timeout and a breaker (ADR-020).
3. It reads the fee rows of that fee type in force on the fee date, with the rate or flat amount, the cap, the validity and the version, and keeps the row identity (GAP-2543; ASM-4202).
4. Read the account fee facts through `GET /accounts/{accountKey}`, including `collectionsFee` (DF-ACE-024). Where the fee is settled by a receipt, read that receipt through `GET /payments?businessDate={date}` (DF-ACE-043 to DF-ACE-054). Read `GET /batch-status` when the fee guard needs the batch row. Exercise all three operations through the P1 contract fake.
5. It computes the amount from the fee row and the read facts alone. Every threshold, rate, cap and tolerance is a row read at run time; a constant that changes an answer fails review (BR-P8-005).
6. It writes the decision record first — fee row identity, version, inputs, answer, hash-linked to the previous record of the case — and the `proceeds` row in the same transaction. A failure of either leaves neither, and the fact stays on the inbox for the next attempt (DP-03; R-UNI-39).
7. The row carries `matched_to` FEE, with `case_id`, `treatment_id` when the fee belongs to a treatment, `source` from `LOV-PROCEEDS-SRC`, `amount`, `received_date` and `posting_ref` when the ACE record carries one (DF-FIN-002 to DF-FIN-009).
8. No amount is raised that an approver has not cleared: where the court fee or legal expense needs approval inside the D7.4 limit, the approved fact is read on the route owner's contract and the calculation uses it (R-LIT-41, R-LIT-42). Where the answer needs a person, a task is raised on rwb-case's contract (FSD P8 A2.5.2 step 3).
9. SCR-28 shows the fee rows of the case with their match status, merged by gateway-bff from this service and the case label of rwb-case (DP-19). Its states are: empty, loading, error (message Not specified in the source documents (DOR-RWB-P8-E4045-APP-10)), and no access (MSG-P4-002).

### 5. Exception paths

| Condition | What happens | Message or reference | Covered by |
|---|---|---|---|
| The decision record cannot be written | Nothing changes; no fee row and no amount; an incident is raised | MSG-P7-003; R-UNI-39; AC2 | AC2; TC-E4-045-02 |
| No fee row is in force for the fee type on the fee date | No amount and no row; the fact is held for the fee owner with the date it needs | Not specified in the source documents (GAP-2544; ASM-4203) | Not specified in the source documents (DOR-RWB-P8-E4045-APP-3) |
| The ACE batch of the source is late or failed | The step does not compute; the product is shown with its date | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. (VR-P8-005-1) | Not specified in the source documents (DOR-RWB-P8-E4045-APP-3) |
| The same fee fact arrives twice | The second one is ignored and the idempotency hit is recorded | R-UNI-40 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-3) |
| The partner is recalled for insolvency | Fee payments to that partner stop and no new amount is raised against its work | R-UNI-28 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-3) |
| A person without the right opens the fee rows | Refused, nothing changes | MSG-P4-002 | TC-E4-045-03 |
| The case of the fee is unknown or out of the caller's scope | One problem document, no change | HTTP 404 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-3) |
| A required fact of the amount basis is missing | Refused, nothing changes | MSG-GEN-001 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-3) |
| A consumed read does not answer inside 2 s | The step stops for that fact and retries; the breaker opens per downstream | HTTP 503; ADR-020 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-3) |
| The fee row version is replaced between the read and the record | The row is recorded at the version read; the next fact is computed at the new version | BR-P8-005 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-3) |

### 6. INVEST check

| Letter | Verdict | Result |
|---|---|---|
| Independent | Yes. It builds against two platform contract stories; no other service's build blocks it. | Pass |
| Negotiable | The fee values, their version and the approval limits stay with their owners; the story fixes only the step, the record and the row. | Pass |
| Valuable | Yes. A fee is worked out from data, recorded with the row and version that produced it, and tied to its case. | Pass |
| Estimable | Yes. One step, one activity, one record, one row and one screen state set. | Pass |
| Small | Yes. One calculation, one write path, no new operation and no new event. | Pass |
| Testable | Yes. The legacy criterion, the four legacy cases and the documented refusals. | Pass |

### 7. Acceptance criteria

```gherkin
Feature: Calculate fees and charges

  Scenario: AC2 Not recorded (legacy RWB-E4-045 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Error answers of the provided operations (new, D-RCV-60)
    Given a caller that is not authenticated or not authorised for a provided operation
    When the caller invokes the operation
    Then the error answer carries status 401 or 403

  Scenario: AC4 Duplicate delivery of a consumed event (new, D-RCV-60)
    Given an event that has already been consumed
    When the same event is delivered again
    Then the event is not applied a second time

  Scenario: AC5 Activity retry and timeout (new, D-RCV-60)
    Given an activity that is retried or times out
    When the activity completes after the retry or the timeout
    Then the action completes with no duplicate effect

  Scenario: AC6 A consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed call that fails or does not answer
    When the call is made
    Then nothing changes

  Scenario: AC7 A disallowed status change is refused (new, D-RCV-60)
    Given a status change that the model does not allow
    When the change is attempted
    Then the change is refused and nothing changes
```

The criterion is the legacy AC2 of the key, with its decision-log term replaced by decision record, and is the only legacy criterion this slice owns; AC3 to AC7 are added from the NEWAC items and carry no legacy wording. AC1 of the same key — "Then works out partner fees, court fees and charges from the fee tables held as data / Then the system writes the result to the decision log with the rule version" — is owned by RWB-ITG-E4045-ITG, which carries the cross-service journey of the key in wave 3; the calculation behind it is built here and stated in sections 4, 8 and 16. The fee facts both criteria are exercised on are the synthetic set of ASM-4201 and are used in section 16 only.

### 8. Business rules

| ID | Rule | Message | BR ID |
|---|---|---|---|
| BR-P8-005 | No value a business person may change is written in code; it is read from reference data with its version | None | BR-P8-005 |
| VR-P8-005-1 | Data product stale after a late or failed ACE batch for its source (source-data batch status) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |
| R-LIT-41 | A court fee or legal expense falls due: route the fee to the approver inside the D7.4 limit | None | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |
| R-LIT-42 | Inside the limit, or approved above it: raise the fee and post it against the case | None | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |
| R-DIS-10 | Storage, property tax, insurance, security or eviction required: raise the work order on the portal at the vendor's fee schedule | None | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |
| R-DIS-54 | On proceeds posted: apply the proceeds to the case and the loan account, and match the vendor fee | None | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |
| R-DIS-64 | Sale price at or above the approved floor: complete the sale and pay the broker fee on acceptance | None | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |
| R-WO-37 | A payment is matched after charge-off: post it as post charge-off income and calculate the agency fee | None | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |
| R-UNI-28 | The partner enters insolvency: recall the work, secure cash held and stop fee payments | None | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None | Not specified in the source documents (DOR-RWB-P8-E4045-APP-4) |

The four route rules are the rows whose events carry a fee, and they are the four triggers of section 4: the fee amount this story works out is their input, and the approval and the case move stay with the route owners (Business Rules and Routing Logic v4). BR-P8-005 and VR-P8-005-1 are the two rows of FSD P8 A2.5.3.1.

### 9. State transitions

| From | Trigger | To | Rule |
|---|---|---|---|
| No `proceeds` row | A fee fact is computed from the fee row in force | `proceeds` row with `matched_to` FEE, and one decision record | R-LIT-42; R-DIS-10 |
| No `proceeds` row | No fee row is in force for the fee type and date | No row; the fact is held for the fee owner | GAP-2544 |
| FEE row | A receipt of the same case settles the fee | The same row, its `posting_ref` written by the posting story | DF-FIN-008, DF-FIN-009 |
| FEE row | The partner is recalled for insolvency | No further fee payment to that partner | R-UNI-28 |
| Any | The decision record or the row write fails | No change; nothing is published and the fact stays on the inbox | R-UNI-39 |

The case state, its route stage, its tasks and its timers are not moved here: this story writes one row of its own schema and one local record, and rwb-case decides what the case does with the fee.

### 10. Authority

The step runs unattended as primary; the Finance and CFO delegate is the role that uses its result (FSD P8 A2.5.3.3). The person-facing part is the read of the fee rows on SCR-28, under capability area **Write-off and posting**, right R (TSD P8 T6.1, T6.2).

| Right | Roles that hold it (TSD P8 T6.1) |
|---|---|
| R (read) | RW-FRAUD, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-CONDUCT, RW-PRODHEAD, RW-WOCOMM, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE, SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT |
| No write right on this path | The step writes with the service identity of the run, under the same role checks as a person (NFR-051) |

The legacy permission table of the key gives right R on **Case record** with an open role list; the module matrix is the authority for the list and the legacy line for the intent. The right is checked on the object: a caller scoped away from the case gets 404, not 403.

### 11. Data

| Element | Type | Source | Note | BR Field ID |
|---|---|---|---|---|
| Fee row of the fee type | reference data, read at a version | rwb-case, reference data (consumed read) | Rate or flat amount, cap, validity, version; the row identity is recorded — the element names are Not specified in the source documents (GAP-2543; ASM-4202) | Not specified in the source documents (DOR-RWB-P8-E4045-APP-7) |
| `proceeds.id` | uuid | Workbench | DF-FIN-001 | DF-FIN-001 |
| `case_id` | uuid | rwb-case reference | DF-FIN-002 | DF-FIN-002 |
| `treatment_id` | uuid, optional | rwb-treatment reference | DF-FIN-003 | DF-FIN-003 |
| `source` | `LOV-PROCEEDS-SRC` | Workbench | DF-FIN-005: CUSTOMER, LED, AUCTION, BUYER, AGENCY, INSURER, GUARANTOR | DF-FIN-005 |
| `amount` | numeric(18,2) | the calculation | DF-FIN-006 | DF-FIN-006 |
| `received_date` | date | ACE payment fact or the fee date | DF-FIN-007 | DF-FIN-007 |
| `matched_to` | `LOV-MATCH` | Workbench | DF-FIN-008, FEE on this path | DF-FIN-008 |
| `posting_ref` | varchar(40), optional | ACE payment fact | DF-FIN-009 | DF-FIN-009 |
| `collectionsFee` | number | `GET /accounts/{accountKey}` | Read through the P1 contract | DF-ACE-024 |
| `fees_outstanding` | number | Account fee input (DF-ACC-011) | Pending publication of the field in the P1 account answer, owner P1 contract owner with the payment owner (NEW-GAP-G7-1) | DF-ACC-011 |
| Partner facts: code, type, panel status, contract end | read | rwb-partner (consumed read) | DF-PRT-001 to DF-PRT-007; the legacy key reads them, this story does not copy them | DF-PRT-001 to DF-PRT-007 |
| Case facts: product group, stage, amount basis | read | rwb-case (consumed read) | DF-CAS-001 to DF-CAS-023; never read from `rwb_case` tables | DF-CAS-001 to DF-CAS-023 |

The only table written is `proceeds` in schema `rwb_payment`, with the seven standard record columns (TSD P8 T3.0, T3.1). The legacy data table also names `decision_log_entry` and `rule_row`: the decision record is the local record of DP-03 and the central `decision_log_entry` is rwb-decision's, and `rule_row` is not read here because the fee values are data rows of the fee tables, at their own version, not a rule package (GAP-2544; ASM-4203).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8); base `/api/recovery/payment/v1` (DP-13). The service declares no fee operation: the two operations of the service are the only ones, and their shapes are the frozen baseline of RWB-P8-E2008-CON. This story supplies the behaviour behind them for a fee row.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | `ProceedsPage` out, query `matched`, `from`, `to`, `page`, `size`, paginated (API-P8-001); the FEE rows of a case are read with the case scope applied | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | `MatchRequest` in, `Proceeds` out (API-P8-002); a fee receipt matched by hand carries the same answer block | Write-off and posting, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat |

The answers: 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope proceeds reference, 409 on an already matched receipt under a new key, 422 with MSG-GEN-001 for an invalid element, 503 when the decision library or a consumed read does not answer. The service plan gives this story no build dependency on that baseline: it is Day 1 work of the same service and this story builds against its shapes.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (name Not specified in the source documents (GAP-2543; ASM-4202)) | `/api/recovery/case/v1` | P3 rwb-case | The product group, the stage and the amount basis of the case; faked |
| The reference-data and fee-row read (name Not specified in the source documents (GAP-2543; ASM-4202)) | `/api/recovery/case/v1` | P3 rwb-case, as the owner of parameters and reference data | The fee rows of the fee type in force on the fee date, with their version; faked |
| The partner read (name Not specified in the source documents (GAP-2543; ASM-4202)) | `/api/recovery/partner/v1` | S9 rwb-partner | The partner of a partner fee, its type, its panel status and its contract end; faked |
| The approved legal-spend fact (name Not specified in the source documents (GAP-2543; ASM-4202)) | Not specified in the source documents (GAP-2543; ASM-4202) | the litigation route (S4) as R-LIT-42 scopes it | That a court fee or legal expense is approved, and inside which limit; faked |
| GET `/accounts/{accountKey}` | `/api/recovery/source-data/v1` | P1 rwb-source-data | Account fee facts, including `collectionsFee`. `fees_outstanding` availability remains Pending (NEW-GAP-G7-1). |
| GET `/payments?businessDate={date}` | `/api/recovery/source-data/v1` | P1 rwb-source-data | Date-form PaymentsAnswer, one row per paymentCode ordered by paymentCode, interim unpaged. 409 MSG-P1-001 when gated. Builder RWB-P1-E1013-APP, contract RWB-P1-E1015-CON. |
| GET `/batch-status` | `/api/recovery/source-data/v1` | P1 rwb-source-data | BatchStatusAnswer for the source and business date, using the rwb-payment workload identity. |

Each row is one hop with a 2 s timeout, one retry on a GET and a breaker per downstream (ADR-020). The plan gives this slice no C dependency, so every row is built against its fake and the owner confirms the name before the contract tag.

#### 12.3 Events published

None. The service owns three events — `TreatmentBooked` (EV-11), `PaymentMissed` (EV-12) and `ProceedsMatched` (EV-25) — and no source declares a fee event for it, so this story publishes nothing and adds no topic, no event name and no outbox row (GAP-2545; ASM-4204). The answer of the calculation is the local decision record of DP-03 plus the `proceeds` row with `matched_to` FEE, which the posting and matching stories of the service read on their own paths.

#### 12.4 Events consumed

| Event | Read or topic | Payload used | When | Owner or service |
|---|---|---|---|---|
| The fee-due fact of the litigation route (FEE_DUE, R-LIT-41) | topic of the owner, name Not specified in the source documents (GAP-2543; ASM-4202) | the case, the fee type and the fee date | A court fee or legal expense falls due | Not specified in the source documents (DOR-RWB-P8-E4045-APP-24) |
| The work-order fact of the asset route (WORK_ORDER_RAISED, R-DIS-10) | topic of the owner, name Not specified in the source documents (GAP-2543; ASM-4202) | the case, the work type and the fee schedule in force | A work order is raised on a held asset | Not specified in the source documents (DOR-RWB-P8-E4045-APP-24) |
| The sale-agreed fact of the asset and debt-sale routes (BROKER_SOLD, R-DIS-64) | topic of the owner, name Not specified in the source documents (GAP-2543; ASM-4202) | the case, the sale reference and the agreed price basis | A broker sale is agreed at or above its floor | Not specified in the source documents (DOR-RWB-P8-E4045-APP-24) |
| The matched-payment fact after charge-off (PAYMENT_RECEIVED_AFTER_CHARGEOFF, R-WO-37) | topic of the owner, name Not specified in the source documents (GAP-2543; ASM-4202) | the case, the placement and the amount matched | A recovery is matched on a placed case | Not specified in the source documents (DOR-RWB-P8-E4045-APP-24) |
The fee facts above trigger the calculation. The batch row used by the freshness guard is a P1 REST answer under section 12.2.

A duplicate is deduped in `inbox_event` of `rwb_payment` on the key of the fact (R-UNI-40; DP-09 library). No other subscription is added, and the fee values themselves are read on the reference-data contract rather than on an event.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| The fee-calculation run (name Not specified in the source documents (GAP-2546; ASM-4205)) | Workflow, event-started per fee fact | `rwb-payment` in namespace `rwb-recovery` | Input: the fee fact and its business date. Signals: none in this slice |
| The calculation activity (name Not specified in the source documents (GAP-2546; ASM-4205)) | Activity | `rwb-payment` | In: the fee fact. Out: the record and row references, in one transaction |

Drools is not called: the fee values are data rows read at their version, not a rule package, so no rule answer has to be replayed (DP-04 is not applied by this story). The retry policy is 1 s initial interval, back-off 2, 10 attempts; a fee row missing in force is a non-retryable answer.

#### 12.6 Schedules

None. The run starts on a fee fact of a route, and the JOB-07 and JOB-08 run in rwb-integration are event-started (FSD P8 A2.5.4.4 AC-BG-P8-005-01 gives the ACE batch of source ALS as the daily cadence), so no Temporal Schedule, no Quartz row and no shared job table is declared here (DP-10 is not applied by this story).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `proceeds` | P8, schema `rwb_payment` | The table of TSD P8 T3.1 with the standard record columns; the FEE row of a fee |
| `decision_record` | Platform library, created in `rwb_payment` | The local decision record of DP-03, one per calculation |
| `inbox_event` | Platform library, created in `rwb_payment` | The dedup of a fee fact (R-UNI-40) |

No fee table is declared in `rwb_payment`: the ownership map gives this service one table, `proceeds`, and the fee rows live with their owner (GAP-2543; ASM-4202). The Flyway baseline of the service is a `V0001` sequence in `rwb_payment`, owned by the DB story of the service (DP-15 is not applied by this story).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case read | The case `RC-2026-000555` of account `A-0555`, product group and stage; no case for an unknown reference; an answer slower than 2 s | AC2, TC-E4-045-01, -03 |
| rwb-case fee-row read | The fee rows of the fee type in force on the fee date, with their version, and a replaced version | TC-E4-045-01 |
| rwb-partner read | A partner in the panel with a valid contract, and one recalled for insolvency (R-UNI-28) | TC-E4-045-01 |
| Decision-record stub (RWB-PLT-E1027-CON) | A healthy chain, a stopped chain and a hash break | AC2, TC-E4-045-02, -04 |
| gateway-bff composite route fake | The merged SCR-28 answer for the case and its fee rows | TC-E4-045-01 |
| Authorise stub of the service template | Right R held, and a caller without it | TC-E4-045-03 |
| rwb-source-data contract fake | Account, payment and batch-status answers for the fee date, including a held batch | DP-05; VR-P8-005-1 |

Each fake answers only what its owner documents; a fake that answers more than the document fails the review. Every name that is not published carries the placeholder of GAP-2543 until its owner confirms it.

Fake library version: Not specified in the source documents (DOR-RWB-P8-E4045-APP-22); no version is published.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 7 consumed | `GET /proceeds` and `POST /proceeds/{proceedsId}/match` on `/api/recovery/payment/v1`; the rwb-case case read, the rwb-case fee-row read, the rwb-partner read and the approved-spend read, P1 account, payment and batch status; one hop, 2 s |
| Kafka | 0 published, 4 consumed | The four fee facts of the routes (FEE_DUE, WORK_ORDER_RAISED, BROKER_SOLD, PAYMENT_RECEIVED_AFTER_CHARGEOFF); the batch guard reads the source-data API |
| Temporal | 1 workflow, 1 activity | The fee-calculation run and its activity on `rwb-payment`; no Schedule |
| File | None | No file is produced or consumed by this slice |

### 13. Solution plan

| Step | Work | Done when |
|---|---|---|
| 1 | The calculation activity: read the case, the fee rows and the ACE fee facts; compute the amount from the rows alone | A fee fact produces one amount, with the fee row identity and version in the record |
| 2 | The record-then-row transaction: decision record first, `proceeds` row with `matched_to` FEE second, both or neither | A stopped record leaves no row and the fact on the inbox |
| 3 | The freshness guard on `GET /batch-status` and the stale answer | A late batch produces MSG-P1-001 and no amount |
| 4 | The dedup of a repeated fee fact on the key of the fact | A repeated fact writes no second row and records the hit |
| 5 | The partner guard: a recalled partner raises no new fee | A recalled partner blocks the amount under R-UNI-28 |
| 6 | SCR-28 through the composite route, with the fee rows in loading, matched and unmatched | The three states render from the merged answer |

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data.yaml 5.1.0 with the rwb-payment workload identity | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. | A required fact of the amount basis is missing (422) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | A caller without right R on the fee rows (403) |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The decision record cannot be written (AC2) |
| MSG-P1-001 | Error | {product} is from {date}. Today's ACE batch has not arrived. | The product of the source is stale (VR-P8-005-1) |

These are the three legacy messages of the key plus the stale-data row of the module. No source publishes a message for a fee type with no row in force, so that condition is carried as the placeholder of GAP-2544 rather than invented. Every refusal is one problem document with a code, the message ID and a correlation reference, and no message text is assembled in code (BR-P8-005).

### 15. Screens and states

| Screen | State | What it shows |
|---|---|---|
| SCR-28 Proceeds matching | Loading | The fee rows of the case are being read; a skeleton, no partial total |
| SCR-28 Proceeds matching | Empty | Not specified in the source documents (CG-ALL-7684) |
| SCR-28 Proceeds matching | Error | Not specified in the source documents (CG-ALL-7684); message Not specified in the source documents (DOR-RWB-P8-E4045-APP-10) |
| SCR-28 Proceeds matching | No access | Not specified in the source documents (CG-ALL-7684); refused with MSG-P4-002 |
| SCR-28 Proceeds matching | Matched | One row per fee with its fee type, amount, case, `matched_to` and posting reference when known |
| SCR-28 Proceeds matching | Unmatched | The fee facts that produced no amount, with the reason and the date they need |

The screen is a gateway-bff composite route: the fee rows come from this service, the case label from rwb-case, and the two are merged one hop each, in parallel (DP-19). The screen declares no business value of its own; every list it shows is a reference-data list of its owner.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-045-01 | AC1; run by RWB-ITG-E4045-ITG | Component | Case `RC-2026-000555`, account `A-0555`: a court fee fact with a fee row in force at a stated version produces one decision record and one `proceeds` row with `matched_to` FEE; no value from the fee row is a constant of the build |
| TC-E4-045-02 | AC2 | Component | The same fee fact; the decision-record stub stops the chain, so no row is written and MSG-P7-003 is returned |
| TC-E4-045-03 | Access | Component | A caller without right R on the fee rows is refused with MSG-P4-002, and nothing changes |
| TC-E4-045-04 | Principle 5 | Component | A forced decision-record failure stops the action with MSG-P7-003 and raises one incident under R-UNI-39 |
| TC-E4-045-05 | Contract of each event of section 12.4 and each operation of section 12 | Contract | The synthetic set of ASM-4201, one check per event and per operation |
| TC-E4-045-06 | Boundary of each table of section 12.7 | Boundary | The synthetic set of ASM-4201; writes limited to `proceeds`, `decision_record` and `inbox_event` in `rwb_payment` |
| TC-E4-045-07 | AC3 | Contract | Not specified in the source documents (NEWAC-RWB-P8-E4045-APP-AC3) |
| TC-E4-045-08 | AC4 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4045-APP-AC4) |
| TC-E4-045-09 | AC5 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4045-APP-AC5) |
| TC-E4-045-10 | AC6 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4045-APP-AC6) |
| TC-E4-045-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4045-APP-AC7) |

The four legacy cases keep their legacy IDs and their legacy intent; TC-E4-045-05 and -06 are the contract and boundary cases of section 12; the data column states the synthetic set of ASM-4201 and no business threshold. TC-E4-045-01 is exercised end to end by RWB-ITG-E4045-ITG, whose copy of it takes the `-ITG` suffix.

### 17. Guardrails

- No business value in code: the rate, the flat amount, the cap, the validity and the fee type are fee rows read at run time; a constant that changes an amount fails review (BR-P8-005).
- No personal data in an event, a workflow input, a log or a test: the calculation carries the case reference, the fee type, the fee row and the amount, and every example is synthetic.
- ACE account, receipt and batch facts are read through the source-data workload contract (DP-05).
- No read of another service's table: the case and the fee rows come from rwb-case's contract, the partner from rwb-partner's, and `rwb_payment` is the only schema written.
- The record precedes the change, and both or neither: the activity writes the decision record and the row in one transaction (R-UNI-39).
- A recalled partner raises no new fee (R-UNI-28), and a repeated fact never raises a second one (R-UNI-40).
- One hop, 2 s, breaker per downstream, and one retry on a GET (ADR-020).
- The service holds one base, one topic, one queue and one login: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login.

### 18. Traceability

| Feature | L3 process | Source | Reference | Used in |
|---|---|---|---|---|
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | Legacy story | RWB-E4-045, AC2 owned word for word by this story; AC1 is owned by RWB-ITG-E4045-ITG | 1, 7, 16 |
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | Feature | FEAT-PAY-05 Calculate fees and charges, module P8 (E4), depends on FEAT-CWC-23 | 1, 2, 3, 18 |
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | FSD P8 v3 | A2.5 (intent, steps, VR-P8-005-1, BR-P8-005, roles); AC-P8-005-01; AC-EXC-P8-005-01 and -02; AC-BG-P8-005-01; SCR-28 | 3, 4, 5, 8, 14, 15 |
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | TSD P8 v2 | T2 components; T3.0 standard columns; T3.1 `proceeds` DF-FIN-001 to DF-FIN-009, `payment_match_rule` named only; T3.2 `LOV-MATCH` and `LOV-PROCEEDS-SRC`; T5.1 INT-02, INT-03, INT-16; T6.1 rights; T-A.1 and T-A.2 API-P8-001 and API-P8-002 | 10, 11, 12, 16 |
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | Logical data model | DF-ACE-024 `collections_fee`, DF-ACC-011 `fees_outstanding`, DF-PRT-001 to DF-PRT-007, DF-CAS-001 to DF-CAS-023 | 11 |
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | Events and jobs | EV-11, EV-12, EV-25 (sibling stories); JOB-07 remains with rwb-payment and JOB-08 with rwb-integration | 12.3, 12.4, 12.6 |
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | Routing logic | R-LIT-41, R-LIT-42, R-DIS-10, R-DIS-54, R-DIS-64, R-WO-37, R-UNI-28, R-UNI-39, R-UNI-40 (Business Rules and Routing Logic v4) | 4, 5, 8, 9 |
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | Patterns | DP-03, DP-05, DP-19 (Template and Rules §R5.5) | 13 |
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | Gaps and assumptions | GAP-2542 to -5; ASM-4201 to -5 | 3, 4, 5, 7, 8, 11, 12, 14, 16 |
| FEAT-PAY-05 | Not specified in the source documents (DOR-RWB-P8-E4045-APP-2) | Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- AC1 of the legacy key and the cross-service journey that evidences it: RWB-ITG-E4045-ITG.
- The published shapes of the two operations, the three event schemas, the consumed rows, the error set and the fakes of the service: the baseline of RWB-P8-E2008-CON.
- The other features and sibling stories of this service: FEAT-PAY-01 (RWB-P8-E2008-APP, RWB-P8-E2027) and RWB-P8-E4043, RWB-P8-E4044, RWB-P8-E4046, RWB-P8-E4047, RWB-P8-E4048, RWB-P8-E4049.
- The approval of a court fee or legal expense and the D7.4 limit: the litigation route (S4) under R-LIT-41 and R-LIT-42. The work order, the holding cost of carry and the sale of an asset: rwb-asset (S5). The lot, the buyer and the award: rwb-debtsale (S6). The write-off scan and the post charge-off placement: rwb-writeoff (S7).
- The partner, its panel status, its contract and its recall: rwb-partner (S9) under R-UNI-28. The fee values, their authoring, their approval and their promotion: rwb-decision (P7) and the reference-data owner (P3).
- The case of record, its stages, tasks and timers, and the parent `CaseWorkflow`: rwb-case (P3). The ACE fee, payment and batch facts and the freshness of the product: rwb-source-data (P1).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template. The composite route, the layout of SCR-28 and its field list: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
