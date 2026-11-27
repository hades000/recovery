# RWB-P8-E4046-APP Post a settlement booking to ALS

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P8-E4046-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-046 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-P8-I |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-046 for rwb-payment. The legacy story sent the agreed settlement terms to ALS through the outbound interface, tracked the item in `outbound_item` and read the booked position back from the ACE views inside one deployable. This story keeps the rwb-payment half: the booking step after an accepted settlement, the outbound booking request to rwb-integration, the read-back of the booked position and the settlement payment, the local decision record and the `TreatmentBooked` event, with the legacy AC2 "Not recorded". The ALS interface row, the `outbound_item` lifecycle and the retry and exception behaviour are RWB-P2-E4046-APP; AC1 and the cross-service evidence are RWB-ITG-E4046-ITG; the accepted terms and their state stay with rwb-treatment; the ACE read-back stays with rwb-source-data; the case state stays with rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P8-E4046-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer**, I want **the accepted settlement terms of a treatment to leave the Workbench for ALS as one outbound booking item, and the booked position and the settlement payment to be read back from ACE data before the case moves, with the decision record written with the rule version at each move**, so that **a settlement that has passed its point of no return is provably booked in the core bank, and the customer's money never arrives against a case that has nothing to receive it**.

This is the application slice of legacy RWB-E4-046 (FEAT-PAY-06 Post a settlement booking to ALS, module P8 Payments and posting, priority Must, depends on FEAT-CHO-08). It owns:

- the legacy acceptance criterion AC2 "Not recorded", copied verbatim with its origin tag, and the message and test cases it needs;
- the booking step of this service after an accepted settlement — `SettlementBookingWorkflow` on task queue `rwb-payment` in namespace `rwb-recovery`, started by `rwb.treatment.TreatmentApproved.v1` (EV-10), running the `postBooking` and `readBackBooking` activities;
- the outbound booking request, which is the `deliverFile(manifest)` activity of rwb-integration (P2) called as a task on queue `rwb-integration`, one booking request per treatment and `Idempotency-Key`, with the item tracked in P2's `outbound_item`;
- the read-back of the booked position against `v_ace_account` and of the settlement payment against `v_ace_payment` through the rwb-source-data data product, one hop after the next `AceDataReady`;
- the local decision record of every rule outcome, written through RWB-PLT-E1027-CON before the request leaves and before the event is published, and MSG-P7-003 when it cannot be written (DP-03; legacy AC2);
- the publication of `rwb.payment.TreatmentBooked.v1` (EV-11) on `rwb.payment.events.v1` in the same transaction as the confirmation, through the outbox;
- SCR-29 Posting in its loading, booked and rejected states, served by the gateway-bff composite route over this service's existing proceeds read, P2's item state and P3's case (DP-19).

It does not own: the ALS interface row, the transport, the retry schedule, the exception queue and the `outbound_item` lifecycle, which are RWB-P2-E4046-APP; the published event schema and the fakes, which no contract story of this key owns; the accepted settlement terms and the treatment state, which are rwb-treatment (S2); the case of record and its route state, which are rwb-case (P3); the ACE account and payment facts, which are rwb-source-data (P1); the rule package, its version and its rule rows, which are governed in rwb-decision (P7); the settlement payment matching and the posting to the general ledger, which are RWB-P8-E4043-APP and the ledger story of this service; and the cross-service evidence of the legacy key, which is RWB-ITG-E4046-ITG.

### 2. Business rationale

A settlement that is signed and accepted but never booked in ALS leaves the agreement unenforceable and the payment due date unset (R-SET-13), so the customer's money arrives against a case that has nothing to receive it. The booking is also the point of no return of the settlement, so the fact that the terms left the bank, what they were, and the booked position that came back have to be provable afterwards (Temporal and Drools Design slide 18). Legacy RWB-E4-046 answered that with one step in one module: send the terms through the outbound interface, track the item, read the booked position back from `v_ace_account` and `v_ace_payment`, and record the result on the decision log with the rule version. The FSD keeps the feature as FEAT-PAY-06 with the objective "writes the agreed settlement terms to ALS and reads the booked position back" (FSD P8 A2.6.1), a step that runs unattended with the Credit Administration officer also using it (FSD P8 A2.6.3.3), and the same metric of receipts matched the same day (FSD P8 A2.6.1). The problem it answers is unchanged (FSD P8 A2.6.1).

What D-RCV-60 changes is who owns each part of that step.

- **the booking and the posting are this service's.** rwb-payment owns payment and posting, the booking and the posting files (Architecture v5 slides 4 and 8; Ownership Map, P8). This story runs the booking step; the settlement payment match that follows it is RWB-P8-E4043-APP and the ledger posting is the ledger story.
- **the outbound leg is rwb-integration's.** The Workbench writes nothing to ALS directly: the terms leave as one outbound item whose interface row, transport, attempts, intervals, exception queue and resend live in rwb-integration (RWB-P2-E4046-APP), and this story calls that service's `deliverFile(manifest)` activity, one booking request per treatment and `Idempotency-Key`.
- **the ACE facts stay with rwb-source-data (P1).** The legacy data table reads `v_ace_account` (DF-ACE-001 to DF-ACE-042) and `v_ace_payment` (DF-ACE-043 to DF-ACE-054) in process, and the Workbench holds no account or payment copy (D-RCV-35 U1 and U4). In the target only rwb-source-data holds SELECT on the `recovery.v_ace_*` views, so DP-05 applies as a prohibition and the booked position and the payment arrive on P1's data product; the conflict is GAP-2549 with ASM-4208.
- **the terms stay with rwb-treatment (S2) and the case with rwb-case (P3).** The accepted terms, the treatment state and the payment due date are S2's; the route state and the move to `AWAITING_PAYMENT` on R-SET-13 are P3's, applied by the parent `CaseWorkflow` on the event this story publishes.
- **the decision is recorded first.** One record per rule outcome, through the local decision-record library and the shared topic `rwb.decision-record.v1`, in the same transaction as the confirmation, and a failed write changes nothing and shows MSG-P7-003 — what legacy AC2 asks for, and the rule of DP-03.
- **the booking is announced once.** `TreatmentBooked` (EV-11) is this service's event, published after the read-back confirms the booked position, so the case moves on ACE data and not on a delivery receipt.

The legacy criteria are thin: AC2 is generic and the four legacy test cases carry no booking data (GAP-2547; ASM-4206). Everything the legacy does not state — the trigger, the outbound manifest, the read-back fields, the rule IDs, the interface values — is filled from FSD P8 A2.6 and TSD P8 where a source has it, and held as a placeholder where no source does (GAP-2548; ASM-4207). The story is issued in Draft with its date copied unchanged and marked tentative, because no approval gate is met in this run and none is required (ASM-4212).

### 3. Preconditions

- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, seals the record into the chain and relays it on `rwb.decision-record.v1`; a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-29 reaches this service through the gateway-bff composite route, one hop, and no screen calls the service directly (DP-19).
- `rwb.treatment.TreatmentApproved.v1` (EV-10) is published by rwb-treatment and carries the case reference, the treatment reference, its type and the accepted amount; the settlement treatment `T-0001` at 820000 for account `A-0001` is the data set of the legacy key (legacy RWB-E4-046 AC1; ASM-4206).
- `GET /treatments/{treatmentId}` of rwb-treatment answers the accepted settlement terms with their state and amount for the fake (Ownership Map row `GET /treatments/{treatmentId}`, owner S2).
- `deliverFile(manifest)` of rwb-integration is available on queue `rwb-integration` under the activity contract of RWB-P2-E1007-CON, with the ALS booking interface row loaded for the environment; the interface id, transport, layout, attempts, intervals and owner role are all values of that row (RWB-P2-E4046-APP; GAP-2548; ASM-4207).
- The rwb-source-data data product over `v_ace_account` and `v_ace_payment` answers the booked position and the payment of the account for business date D+1, with its freshness stamp; the product code is Not specified in the source documents (GAP-2548; ASM-4207).
- `AceDataReady` (EV-26) for business date D+1 is published by rwb-source-data and starts the read-back of the booking (Architecture v5 slide 44; Architecture v5 slide 9, step 2, where the same event starts payment matching).
- The route set that governs the booking is in force at its version: R-SET-10 sends a signed settlement to operations, R-SET-13 sets the payment due date once the terms are booked in ALS, R-RES-22 records the booking reference when ALS and NLEADS acknowledge, and R-RES-23 puts a rejection on the officer queue (Business Rules and Routing Logic v4). The package, its rule rows and its version are authored, tested and approved in rwb-decision (P7); no source publishes the package code (GAP-2548; ASM-4207).
- The case reference and its route state on the rwb-case contract (P3) are available for the fake, and no case row is read as a table (Ownership Map row `recovery_case`, owner P3).
- The service runs as its own login on schema `rwb_payment` with no grant on another `rwb_*` schema and no grant on `recovery` (TSD P8 T6.2; Architecture v5 slide 29; DP-01, DP-02).
- No approval is needed to build against a Draft baseline, and no human verification stop is part of this run.

### 4. Flow

1. `rwb.treatment.TreatmentApproved.v1` arrives for a settlement treatment; the inbox writes its `processed_event` row in the same transaction as this service's own change, and a redelivery is a no-op (DP-09).
2. `SettlementBookingWorkflow` starts on queue `rwb-payment` with the case reference, the treatment reference, the account key and the accepted amount (Architecture v5 slide 44 pattern).
3. `postBooking` reads the accepted terms on `GET /treatments/{treatmentId}` of rwb-treatment, one hop with a 2 s budget and a breaker; no treatment row is read as a table (DP-01; ADR-020).
4. The activity loads the route set at the version in force, from the rwb-decision package or from `RulePackageInForce` (EV-30), and evaluates R-SET-10 and R-SET-13 against the treatment state, the accepted amount and the case (DP-04; BR-P8-006).
5. The decision is written before anything leaves: one record with the case reference, the treatment reference, the rule ID, the version in force, the inputs reference, the outcome and the decided-at time (DP-03).
6. A failed record write stops the step: nothing is sent, no item is created, no event is published, MSG-P7-003 is shown and an incident is opened (legacy AC2; FSD P8 A2.6.4.3).
7. `postBooking` calls the `deliverFile(manifest)` activity on queue `rwb-integration` with the ALS interface reference, the business date, the treatment reference, the case references, the account key, the accepted amount, the claim-check reference of the signed terms document and the `Idempotency-Key`; rwb-integration owns the item, its attempts and its exception path (BR1; Architecture v5 slide 16).
8. The workflow waits on a durable timer for the item to be acknowledged, and reads its state with `GET /api/recovery/integration/v1/admin/outbound-items`; the item in `EXCEPTION` ends the wait with no read-back (X5).
9. `AceDataReady` for the next business date signals the workflow; `readBackBooking` reads the booked position and the settlement payment on the rwb-source-data data product, holding when the product is stale (VR-P8-006-1, MSG-P1-001).
10. The activity compares the booked position and the payment with the accepted terms; a mismatch ends the step with a task for the case owner and no event (X6).
11. The confirmation record is written in one `rwb_payment` transaction with the outbox row: the rule ID and version, the item reference, the business date, the booked amount and the outcome (DP-03, DP-09).
12. `TreatmentBooked` (EV-11) is relayed to `rwb.payment.events.v1` with key `caseId`, the CloudEvents envelope and no personal data; rwb-case and rwb-treatment move the case and the treatment on it (R-SET-13), and the payment due date stays rwb-treatment's field (DP-09).
13. A repeated `TreatmentApproved` or the same `Idempotency-Key` creates no second item, publishes no second event and counts the repeat (Architecture v5 slide 11).
14. SCR-29 Posting reads the booking and its confirmation through the gateway-bff composite route; the service provides no new REST operation of its own (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written (library failure, stopped hash chain, outbox failure) | The transaction writes nothing: no outbound request, no item, no event, no confirmation; an incident is opened | MSG-P7-003 | AC2, TC-E4-046-02, TC-E4-046-04 |
| X2 | The treatment is not an accepted settlement, or its state is not the one R-SET-10 allows | The step does not fire, nothing is written and nothing leaves | None | TC-E4-046-01 |
| X3 | The ACE data product is stale after a late or failed batch | The read-back holds, writes nothing, shows the data date and resumes on the next fresh answer | MSG-P1-001 | TC-E4-046-01 |
| X4 | The rwb-treatment, rwb-source-data, rwb-integration or rwb-case contract does not answer inside 2 s, or its breaker is open | The activity retries on the workflow's own backoff; nothing is written and no event is published | None | TC-E4-046-01 |
| X5 | The outbound item reaches `EXCEPTION`, or the interface row is not in force | No read-back and no `TreatmentBooked`; the exception queue and the owner task are rwb-integration's, and the case stays with operations | MSG-P2-001 (P2's) | TC-E4-046-01 |
| X6 | The booked position or the settlement payment does not match the accepted terms | No `TreatmentBooked`; one task for the case owner and the difference recorded | None | TC-E4-046-01 |
| X7 | The same `TreatmentApproved` or the same `Idempotency-Key` arrives twice | The stored answer is returned, no second item, no second event, the repeat counted | None | TC-E4-046-01 |
| X8 | A component, a statement or a test reads a `v_ace_*` view, another `rwb_*` schema or a `recovery_*` table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR7 |

X1 is the path of the legacy key and of FSD P8 A2.6.4.3; X2 to X7 are the paths the target call types, the read-back and the rule set add; X8 is the DP-01 and DP-05 boundary. Every threshold, interval and list value is reference data or a rule row in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the platform decision-record library, the edge route and the rwb-treatment, rwb-integration, rwb-source-data and rwb-case fakes; needs no live S2, P2, P1 or P3 |
| Negotiable | The workflow and activity names, the consumer group and the confirmation record shape are this story's choice; the rule rows, the interface values, the products and the screens are fixed |
| Valuable | An accepted settlement is provably on its way to ALS, and the case moves only on the booked position that came back from ACE |
| Estimable | One workflow, two activities, one inbox consumer, one cross-service activity call, one record writer, one publisher, four clients and three read-only screen states |
| Small | Fits in one sprint with its tests on the fakes |
| Testable | Runs on synthetic terms and a synthetic ACE read-back through the contract fakes, plus the forced record failure and the boundary test |

### 7. Acceptance criteria

```gherkin
Feature: Post a settlement booking to ALS

  Background:
    Given treatment "T-0001" is accepted at a settlement amount of 820000 for account "A-0001"
    Given the ALS booking interface is configured in rwb-integration and the booking runs for business date 2027-02-26
    Given the route set R-SET-10 and R-SET-13 is in force at its version
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E4-046 AC2)
    Given the rwb-decision contract mock returns a failed decision-log write
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC2 is the criterion of RWB-E4-046 that this story owns, word for word with its origin tag and nothing else changed: the legacy wording of `the action is taken` and `the decision log cannot be written` both stand, and the one leading `Given` is the only addition, because the failed write is faked on the rwb-decision boundary of DP-03. AC1 of the legacy key ("Post a settlement booking to ALS") is owned by RWB-ITG-E4046-ITG and is not restated here. What legacy AC2 describes happens in two places in the target — the local record written in `rwb_payment` and the ledger collection in rwb-decision within 5 minutes — and the step has no side effect in either case. The booking detail behind the story is filled from FSD P8 A2.6 and TSD P8 and is recorded as GAP-2547 with ASM-4206, and every value no source carries is held as GAP-2548 with ASM-4207.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| VR-P8-006-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) raises MSG-P1-001 `{product} is from {date}. Today's ACE batch has not arrived.` | FSD P8 A2.6.3.1, copied character for character |
| BR-P8-006 | No value a business person may change is written in code; it is read from reference data with its version | FSD P8 A2.6.3.1, copied character for character |
| BR1 | The Workbench writes nothing to ALS directly: the agreed terms leave as one outbound request on the ALS interface of rwb-integration, and this story creates no interface row, no transport and no file | Legacy RWB-E4-046 (Story); REQ-DRI-006; RWB-P2-E4046-APP |
| BR2 | The booking step runs after an accepted settlement and before the case moves: the read-back of the booked position and of the settlement payment is what confirms the booking | R-SET-13; FSD P8 A2.6.2; RWB-ITG-E4046-ITG section 1 |
| BR3 | The decision is recorded before the request leaves and before the event is published, one record per rule outcome, with the rule ID and the version in force; a failed write changes nothing and the user sees MSG-P7-003 | DP-03; legacy RWB-E4-046 AC2; FSD P8 A2.6.4.3 |
| BR4 | The trigger is `TreatmentApproved` of an accepted settlement, not a Quartz schedule and not a shared job table; the read-back is triggered by `AceDataReady` of the next business date | Architecture v5 slides 44 and 9 |
| BR5 | The account and payment facts of ACE stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the booked position and the payment on the owner's data product only | DP-05; Architecture v5 slide 29; GAP-2549 |
| BR6 | The accepted terms, the treatment state and the payment due date stay with rwb-treatment, and the case state with rwb-case: no `treatment`, `recovery_case`, `assignment`, `task` or `timer` row is written here | Ownership Map (`treatment` S2, `recovery_case` P3); R-SET-13 |
| BR7 | The outbound item and its lifecycle stay with rwb-integration: this story holds no `outbound_item` row, and it tracks the item by its reference on P2's contract | Ownership Map (`outbound_item` P2); GAP-2551; ASM-4210 |
| BR8 | The booking is announced once: `TreatmentBooked` is written to the outbox in the same transaction as the confirmation and relayed with key `caseId`, and this step publishes no other event | Architecture v5 slides 42 and 43 (EV-11); DP-09 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_payment`; `case_id`, `treatment_id` and the account key are identifiers of other services' facts | DP-01; TSD P8 T3.3 |
| BR10 | The same treatment or the same `Idempotency-Key` twice creates one item, one event and one confirmation, and counts the repeat | Architecture v5 slide 11; TSD P8 T-A.2 |
| BR11 | No person name, address, contact value or identity number enters `rwb_payment`, the decision record, the `TreatmentBooked` payload, a log or a workflow input | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |

VR-P8-006-1 and BR-P8-006 are the rows of FSD P8 A2.6.3.1, copied character for character; the rest are the rules the split fixes. The rule rows behind the booking — R-SET-10, R-SET-13 with R-RES-22 and R-RES-23 around them — are governed in rwb-decision and named here, never declared here.

### 9. State transitions

The treatment state, the case route state and the payment due date are their owners' and are not changed by this story (BR6). What this story owns is the state of its own step and the confirmation behind it.

| From (step) | Event | Condition | To |
|---|---|---|---|
| Waiting | `TreatmentApproved` for an accepted settlement | The inbox row is written and R-SET-10 allows the booking | Reading the terms |
| Reading the terms | The accepted terms answer | The record is written | Requesting the booking |
| Requesting the booking | `deliverFile(manifest)` answers with an item reference | The item is not in `EXCEPTION` | Waiting for the batch |
| Requesting the booking | The record cannot be written (X1) | The library refuses | Waiting, nothing sent, MSG-P7-003 |
| Waiting for the batch | `AceDataReady` for business date D+1 | The item is acknowledged | Reading back |
| Reading back | The booked position and the payment match the terms | The confirmation record commits | Booked, `TreatmentBooked` published |
| Reading back | The data product is stale (X3) | VR-P8-006-1 | Held, until a fresh answer |
| Reading back | The position or the payment does not match (X6) | The comparison fails | Held, task for the case owner, no event |
| Booked | The same treatment or the same `Idempotency-Key` again (X7) | The stored answer is returned | Booked, no second item, the repeat counted |

| Owner's state (not changed here) | Event | Rule |
|---|---|---|
| `WITH_OPS_SETTLEMENT` to `AWAITING_PAYMENT` | `TreatmentBooked` — the terms are booked in ALS | R-SET-13, applied by rwb-case and rwb-treatment |
| `WITH_OPS_BOOKING` to `BOOKED_IN_ALS_NLEADS` | The booking reference is recorded when ALS and NLEADS acknowledge | R-RES-22 |
| A rejection keeps the case with operations | The item is rejected or in the exception queue | R-RES-23, with no settlement row of its own (GAP-2552; ASM-4211) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: reads the booking and its confirmation on SCR-29 and acts where the flow needs it |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: reads the booking and its confirmation |
| SY-DATALOAD, data load from COLLINS | Write-off and posting U |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE, RW-FINANCE, RW-PRODHEAD, RW-WOCOMM | Write-off and posting R, and RA where the matrix gives it: read only, in scope, through SCR-29 |
| SY-CASEWF, SY-RULES, SY-AGENT | Write-off and posting R: the service identities run inside the same checks as a person |
| Case record, right R | The legacy row of the key: the roles of the case record read the booking of their case, with no wider right than the matrix gives |
| rwb-payment service identity | Runs the workflow and the activities, consumes the three events, writes the decision record and the outbox row, and calls `deliverFile` on queue `rwb-integration`; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD P8 T6.1 and the legacy permission table of this key, and nothing wider. The step runs unattended under the service identity (FSD P8 A2.6.3.3, "None; runs unattended" as the primary use). DP-08 is not in this story's pattern set: the right is declared by the contract and checked by the guard of the service template, so it is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 to DF-TRT-014 | treatment (S2) | `id`, `case_id`, `decision_log_id`, `treatment_type`, `proposed_by`, `proposed_at` and 8 more | Read on `GET /treatments/{treatmentId}` only; never as a table |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` (P1) | `account_key`, `account_code`, `account_status`, `contract_no`, `product_category_efs`, `total_balance` and 36 more | Not read here: the booked position arrives on the rwb-source-data data product (BR5) |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` (P1) | `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel`, `capital_amount` and 6 more | Not read here: the settlement payment arrives on the same product (BR5) |
| DF-OPS-168 to DF-OPS-177 | `outbound_item` (P2) | `id`, `interface_id`, `idempotency_key`, `payload_ref`, `case_ids`, `attempt_count` and 4 more | Not read as a table: the item is read by its reference on the rwb-integration contract (BR7) |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | `id`, `case_no`, `product_group`, `primary_person_key`, `status`, `stage_code` and 17 more | Read on the rwb-case contract only; never as a table |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_payment`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, one record per rule outcome, before the request and before the event |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | `id`, `rule_id`, `rule_version`, `route_set`, `from_state`, `event_code` and 9 more | Not read and not written: loaded with the package in force |
| DF-FIN-009 | proceeds (P8, `rwb_payment`) | `posting_ref` | Not written here: the settlement payment match and its posting reference are RWB-P8-E4043-APP and the ledger story |

Field IDs are those of TSD P8 T3.1 and of the legacy data table of RWB-E4-046, with their owners changed by the target. **No new table, no new column and no migration**: `proceeds` arrives with the DB story of this service, and `decision_record`, `outbox_event`, `processed_event` and `idempotency_key` are platform library objects created in `rwb_payment` by the library's own migration (DP-03, DP-09). The fields of the outbound manifest and of the `TreatmentBooked` payload that no source gives are Not specified in the source documents (GAP-2548; ASM-4207).

**No personal data.** The rows this story writes carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_payment`, the decision record, the manifest, the `TreatmentBooked` payload, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The legacy key names no endpoint ("None. The work runs as a service or a scheduled job inside the recovery module"), the two operations this service owns are the proceeds list and the proceeds match of RWB-P8-E4043-CON, and the booking is raised by the consumed event and answered by an event. The screen evidence of the booking is the existing `GET /proceeds` (API-P8-001) filtered on the settlement match, declared by RWB-P8-E4043-CON and exercised by RWB-P8-E4043-APP: this story adds the booking reference of the settlement to the `TreatmentBooked` payload and no path to `/api/recovery/payment/v1` (DP-13 not in its pattern set), and provides no REST operation of its own.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /treatments/{treatmentId}` | `/api/recovery/treatment/v1` | S2 rwb-treatment | The accepted settlement terms, their type, their state and the accepted amount; faked |
| The data product read, `GET /data-products/{productCode}/records` (product code Not specified in the source documents (GAP-2548; ASM-4207)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The booked position from `v_ace_account` and the settlement payment from `v_ace_payment` for business date D+1, with the freshness stamp; faked (DP-05) |
| `GET /admin/outbound-items` | `/api/recovery/integration/v1` | P2 rwb-integration | The state of the booking item: acknowledged, retrying or in the exception queue, by its reference and the treatment; faked |
| The case reference and its route state (operation name Not specified in the source documents (GAP-2548; ASM-4207)) | `/api/recovery/case/v1` | P3 rwb-case | The case identity and its route state at the booking; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The outbound booking is not a REST path: it is the `deliverFile(manifest)` activity of rwb-integration called as a task (12.5). The four rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, so this story builds against their published documents and fakes on Day 1 (GAP-2550; ASM-4209).

#### 12.3 Events published

| Event | Topic | Payload used | When |
|---|---|---|---|
| `TreatmentBooked` (`rwb.payment.TreatmentBooked.v1`, EV-11) | `rwb.payment.events.v1`, with its `.retry` and `.dlt` topics | The case reference, the treatment reference, the business date, the accepted and the booked amount, the outbound item reference as the booking reference, the rule ID with its version and the outcome; CloudEvents 1.0, key `caseId`, no personal data | In the same transaction as the confirmation record, through the outbox, after the read-back confirms the booked position |

`TreatmentBooked` is event 11 of Architecture v5 slide 43, produced by rwb-payment and declared published in TSD P8 T5.3; its consumers are the owners that move on it — rwb-case and rwb-treatment for R-SET-13, and the reporting and ledger consumers the event catalogue of Architecture v5 slide 43 names. `PaymentMissed` (EV-12) and `ProceedsMatched` (EV-25) are the other two events of this service and belong to RWB-P8-E2008-APP and RWB-P8-E4043-APP; this step publishes neither. The enqueue is the outbox row of the same transaction and the relay publishes with an idempotent producer (Architecture v5 slide 22).

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When |
|---|---|---|---|---|
| `TreatmentApproved` (EV-10) | `rwb.treatment.events.v1`, with its `.retry` and `.dlt` topics | `rwb-payment.settlement-booking.v1` | The case reference, the treatment reference, its type and the accepted amount; deduped in the inbox on the event id | On the outbox relay of rwb-treatment; starts the booking workflow |
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1` | `rwb-payment.settlement-booking.v1` | The business date and the source of the completed batch; deduped in the inbox | On the outbox relay of rwb-source-data; signals the read-back |
| `RulePackageInForce` (EV-30) | `rwb.decision.events.v1` | `rwb-payment.settlement-booking.v1` | The package code and the version in force; deduped in the inbox | On the outbox relay of rwb-decision, and at every step start from the package read |

`DecisionRecorded` (EV-08) is written by all nineteen services on the shared topic `rwb.decision-record.v1`, and its consumers are rwb-decision and rwb-reporting (Architecture v5 slide 42, row 08). This service is a **producer** of that topic through the local library of DP-03 and not a consumer of it, so 12.3 carries no row for it.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `SettlementBookingWorkflow` | Workflow, one execution per accepted settlement, event-started by `TreatmentApproved` | `rwb-payment` in namespace `rwb-recovery` | Input: the case reference, the treatment reference, the account key, the accepted amount and the business date; signals: `TreatmentApproved`, `AceDataReady`, `RulePackageInForce` |
| `postBooking` | Activity, the booking step of this story: read the terms, evaluate the route set, write the record, call `deliverFile` | `rwb-payment` | Terms in; the item reference and its state, the record and the outbox row out |
| `readBackBooking` | Activity, the read-back and confirmation step | `rwb-payment` | The data product answer and the terms in; the comparison, the confirmation record and the `TreatmentBooked` outbox row out, in one transaction |
| `deliverFile(manifest)` | Activity, **consumed** from rwb-integration and declared by RWB-P2-E1007-CON; its ALS branch is RWB-P2-E4046-APP | `rwb-integration` | Input: the interface reference, business date, treatment and case references, account key, accepted amount, claim-check reference, `Idempotency-Key`. Output: the item reference and its state |

No source names the two activities of this story, so their names are this story's choice; `deliverFile` is the name the architecture gives the outbound leg (Architecture v5 slide 17, "Integration: deliverFile (posting file)") and `postProceeds` is the saga step of the ledger story on the same queue, not this one's. The workflow input and its history carry identifiers, amounts, dates and codes only.

#### 12.6 Schedules

None. The booking is triggered by the accepted treatment and the confirmation by `AceDataReady`, and neither is a Temporal Schedule (Architecture v5 slide 44). This story declares no Schedule, no Quartz row and no shared job table; the only time behaviour it owns is the durable timer that bounds the wait for the batch, and its value is Not specified in the source documents (GAP-2548; ASM-4207).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| decision_record | PLT library, created in `rwb_payment` | The local hash-linked record of the booking and of its confirmation, one per rule outcome (DP-03) |
| outbox_event | PLT library, created in `rwb_payment` | The `TreatmentBooked` row of the confirmation transaction (DP-09) |
| processed_event | PLT library, created in `rwb_payment` | The inbox row of each consumed event and its dedupe key (DP-09) |
| idempotency_key | PLT library, created in `rwb_payment` | The `Idempotency-Key` of the booking request and the answer it holds |

Not owned and never read as a table: `outbound_item` and `interface_config` (P2), `treatment` (S2), `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), and the ACE views (P1). `proceeds`, the one table of this service, is not written by this step: the settlement payment match and its posting reference are RWB-P8-E4043-APP. No foreign key leaves the schema and the cross-service references are identifiers, not foreign keys (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-treatment terms fake | The settlement treatment `T-0001` of case `RC-2026-000431` with its accepted amount 820000, its type and its state; a treatment that is not an accepted settlement | AC2, X2 |
| rwb-integration `deliverFile` fake and item fake | One item per treatment and `Idempotency-Key`, its state at each point, an item in `EXCEPTION`, and an interface row not in force | X5, X7 |
| rwb-source-data read-back fake | The booked position of `A-0001` and the settlement payment on business date D+1; a stale product with its date; a position that does not match the terms | X3, X6 |
| rwb-case case fake | The case `RC-2026-000431` with its product group and route state | AC2 |
| rwb-source-data event fake | `AceDataReady` for business date D+1, the same event twice | X7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-29 answer for the case, with the booking of this service read once | AC2 |

The fakes are test-only and are replaced by the real services in SIT. The manifest element set, the `TreatmentBooked` payload and the data product code are stubbed from the published documents and carry the placeholder until their owners publish them (GAP-2548; ASM-4207).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-treatment terms read, the rwb-source-data read-back, the rwb-integration item read and the rwb-case case read; one hop, 2 s |
| Kafka | 1 published, 3 consumed | `TreatmentBooked` on `rwb.payment.events.v1`; `TreatmentApproved`, `AceDataReady` and `RulePackageInForce` in consumer group `rwb-payment.settlement-booking.v1`; the decision record is relayed by the library on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 2 activities owned, 1 activity consumed | `SettlementBookingWorkflow`, `postBooking` and `readBackBooking` on `rwb-payment`; `deliverFile(manifest)` on `rwb-integration`; no Schedule |
| File | None | No file is built, read or delivered here: the ALS file, where the interface is a file, is built and sent by rwb-integration (RWB-P2-E4046-APP) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `booking`, Java package `th.co.scb.ace.workbench.recovery.payment.booking`; front end `src/modules/recovery/payment/Posting.tsx`, the fragment SCR-29 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: rwb-payment holds no `v_ace_*` grant, because only rwb-source-data has SELECT on the views (Architecture v5 slide 29), so the booked position and the payment arrive on the owner's data product and the legacy `v_ace_account` and `v_ace_payment` reads are retired (GAP-2549; ASM-4208). DP-03 is the transaction rule of both steps: the record, the state and the outbox row commit together or not at all. DP-19 is how SCR-29 reaches the booking, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The pattern table adds the two H rows `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, which the plan already carries for this story. The four consumed rows of 12.2 and the consumed `deliverFile` activity contract are class C dependencies that the plan's C row does not list, because that row is None, so they are built against their documents and fakes on Day 1 (GAP-2550; ASM-4209). This key has **no contract story of its own** (there is no `RWB-P8-E4046-CON` in the plan), so the event schema and the fakes come from the published documents as they stand and carry the placeholder where they are silent (GAP-2548; ASM-4207). The inbox and the outbox are the platform library of DP-09, which adds no H row.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `SettlementBookingWorkflow` | Workflow | The booking step after an accepted settlement, the wait for the batch and the confirmation |
| `postBooking` | Activity | Reads the terms, evaluates R-SET-10 and R-SET-13, writes the record, calls `deliverFile` and keeps the item reference |
| `readBackBooking` | Activity | Reads the booked position and the payment, compares them with the terms, writes the confirmation record and the outbox row |
| `BookingEventConsumer` | Inbox adapter | Consumes `TreatmentApproved`, `AceDataReady` and `RulePackageInForce` in group `rwb-payment.settlement-booking.v1`, writes the `processed_event` row and dedupes |
| `BookingRuleEvaluator` | Service | The booking arm of the route set against the treatment state, the accepted amount and the case |
| `BookingDecisionRecordWriter` | Library adapter | Writes one record per rule outcome before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `TreatmentBookedPublisher` | Outbox adapter | Writes the `TreatmentBooked` outbox row in the confirmation transaction and leaves the relay to the library (DP-09) |
| `OutboundBookingRequester` | Activity client | Calls `deliverFile(manifest)` on `rwb-integration` with the manifest and the `Idempotency-Key`, and reads the item state |
| `TreatmentTermsClient` | Client | `GET /treatments/{treatmentId}` of rwb-treatment, one hop, 2 s, breaker |
| `BookingReadBackClient` | Client | The data product read of rwb-source-data, one hop, 2 s, with the freshness stamp |
| `CaseAnswerClient` | Client | The case read and the answer that follows the confirmation, one hop, 2 s |
| `RulePackageClient` | Client | The route set read of rwb-decision, one hop, 2 s |
| `Posting` | React component | Shows the bookings and their confirmation on SCR-29, read only, with the hold, the rejected and the not-recorded states |

**Database and migrations.** No Flyway file of this story. `proceeds` arrives with the DB story of this service, and the decision record, the outbox, the inbox and the idempotency key are library objects created in `rwb_payment` by the library's migration (DP-03, DP-09). No column is added for the booking reference or the confirmation: where no source names a field, the value stays on P2's item or on the event and is never an invented column (GAP-2548; ASM-4207).

**Configuration and reference data.**

- The route set and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the values of R-SET-10 and R-SET-13 are values of the package and not of this build.
- The ALS interface reference used in the manifest, read from the interface row in force for the business date; every one of its values is a row of rwb-integration and not a constant here (GAP-2548; ASM-4207).
- The capability area "Write-off and posting" and its rights are access rows of rwb-access, read through the guard.
- The consumer group `rwb-payment.settlement-booking.v1` and the three subscriptions are configuration of the inbox library.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. `SettlementBookingWorkflow` and its input record, registered on `rwb-payment`, with `TreatmentApproved` as its trigger (AC2).
2. `BookingEventConsumer` and the inbox row, with the duplicate and redelivery paths (X7).
3. `TreatmentTermsClient`, `BookingReadBackClient`, `CaseAnswerClient` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker, the stale-data path and the no-answer path (X3, X4).
4. `BookingRuleEvaluator` over the route set, with the not-an-accepted-settlement path (X2).
5. `BookingDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
6. `OutboundBookingRequester` against the `deliverFile` fake, with the item reference, the exception path and the repeat (X5, X7).
7. `readBackBooking` with the comparison, the mismatch task and the confirmation (X6).
8. `TreatmentBookedPublisher` and the outbox row, with the relay of the library.
9. `Posting` and SCR-29 in its loading, booked and rejected states through the composite route fake.
10. The boundary test: no statement outside `rwb_payment`, no `v_ace_*` read, no write to `rwb_case`, `rwb_treatment`, `rwb_integration` or `rwb_decision`, and no Schedule (X8, BR5, BR6, BR7).

**Feature flag.** `rwb.payment.settlement-booking-v1`, read as a flag of the platform library; off means the consumer writes the inbox row and holds the treatment, no request leaves and no event is published, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the booking runs from a synthetic `TreatmentApproved` in SIT, one item is requested per treatment and key, the confirmation follows the read-back of the next batch, `TreatmentBooked` is published once, a forced record failure changes nothing, no `v_ace_*` read and no foreign row write exists in the build, and SCR-29 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the manifest is absent or invalid, or the treatment reference cannot be read | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right reads the booking screen | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the request leaves or before the confirmation | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product is stale after a late or failed batch (VR-P8-006-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The four message IDs are those of the legacy message set of this key and of FSD P8 A2.6.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P7-003 is the message of legacy AC2 and of FSD AC-EXC-P8-006-02, and MSG-P4-002 is the message of TC-E4-046-03 and of FSD AC-EXC-P8-006-01. The booking rejection carries no message of its own: R-RES-23 sets the officer queue, and the message the queue shows is rwb-case's.

### 15. Screens and states

SCR-29 Posting (FSD P8, "Approved bookings and postings, with the confirmation from the next ACE batch", first in E4) is the screen of this feature, and the legacy row names SCR-28 Proceeds matching with its loading, matched and unmatched states, which stays the list of the matching story. Both are served through the gateway-bff composite route (DP-19): the route reads this service's existing `GET /proceeds` for the settlement rows and their confirmation, rwb-integration for the item state, rwb-case for the case and its route state and rwb-treatment for the terms; this story fixes the settlement rows of the proceeds answer only, and the route specification and the field list belong to RWB-PLT-N001-CON.

- **Loading** while the terms are read on the rwb-treatment contract, the record is written and the item is requested.
- **Booked** when the read-back of the business date has confirmed the booked position and the settlement payment and the confirmation record is committed with the outbox row.
- **Rejected** when the item is in the exception queue or the read-back does not match the terms, with the item reference and the difference shown and the case kept with operations.
- **Hold** when the data product is stale (MSG-P1-001), **refused** when the role lacks the right (MSG-P4-002) and **not recorded** when the record cannot be written (MSG-P7-003), each read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-046-01 | AC1 (owned by RWB-ITG-E4046-ITG) | Component | Treatment `T-0001` accepted at 820000 for account `A-0001`; one item requested per treatment and key, the booked position and the payment read back from the product fake, and the `TreatmentBooked` outbox row asserted |
| TC-E4-046-02 | AC2 | NFR | The decision-record stub stopped; nothing requested, no item, no event, MSG-P7-003 shown and an incident opened |
| TC-E4-046-03 | Access | Contract | A role without the Write-off and posting right R; 403 with MSG-P4-002 and no read |
| TC-E4-046-04 | Principle 5 | NFR | A forced decision-log write failure at the moment of the confirmation; no record, no event, no answer, and the repeat publishes once when the library recovers |

The four test cases are the legacy cases of RWB-E4-046 in their legacy order, with the Level column added. TC-E4-046-01 covers AC1, which the harness story owns, and it is kept here because it is the component proof of the booking step on its own fakes; the `-ITG` copies of all four belong to RWB-ITG-E4046-ITG. The two forced-failure cases map to NFR because they prove the atomicity and the no-side-effect property of the transaction, and the access case maps to Contract because the artefact under test is the declared right. The legacy rows name no booking-specific data, which is recorded as GAP-2547 with ASM-4206; the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the route set, its rule rows, the interface values, the manifest width and the comparison tolerance stay data, reference data or the package, never a constant, a default or a branch of the build.
- No personal data in `rwb_payment`, in the manifest, in the `TreatmentBooked` payload, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's data product or a `v_ace_*` view this service holds: it holds none, because only rwb-source-data has SELECT on the views, so a build that adds a view or an ACE table read fails the boundary test (DP-05; Architecture v5 slide 29).
- The Workbench writes nothing to ALS: no statement of this story opens a transport, holds a credential or builds a file, and the ALS interface values are P2's rows (BR1, BR7).
- The terms stay with rwb-treatment and the case with rwb-case: no `treatment`, `recovery_case`, `assignment`, `task` or `timer` row is written here, and no due date is computed here.
- One base, one topic, one queue and one login per service: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login, and no document, module or test names another service's base or topic as its own (DP-14).
- The decision is recorded before the change and every consumed event is deduped in the inbox; a build that publishes or changes a row before its record fails the review (DP-03, DP-09).
- No retired element is reintroduced: no shared Quartz table, no Quartz job, no monolith API base, no `recovery` schema read, no account or payment copy and no data-lake copy of the booking.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id for this slice; the requirement is FEAT-PAY-06 of the FSD P8 A2.6 and its main success criterion AC-P8-006-01, that the agreed settlement terms are written to ALS and the booked position is read back with the result recorded with its rule version (GAP-2547; ASM-4206) | The booking step, the outbound request, the read-back, the decision record and the `TreatmentBooked` event | TC-E4-046-01, TC-E4-046-02 |
| REQ-S2-008, REQ-CHO-008, REQ-DRI-001 and REQ-DRI-007 | The booked terms reach their system of record without re-keying; the booking is confirmed from the next business date's ACE account data; every decision writes one record with the rule and its version; every outbound is logged, retried and excepted. The chain is carried by RWB-ITG-E4046-ITG, which owns these rows for the legacy key | The confirmation behind BR2, the record of BR3 and the outbound request of BR1 | TC-E4-046-01, TC-E4-046-02 |
| BR-P8-006 | No value a business person may change is written in code; it is read from reference data with its version (FSD P8 A2.6.3.1) | The route set and the interface values read with their version | TC-E4-046-01 |
| VR-P8-006-1 | Data product stale after a late or failed ACE batch raises MSG-P1-001 (FSD P8 A2.6.3.1) | The freshness check of the read-back | TC-E4-046-01, TC-E4-046-04 |
| ADR-013 | 19 services inside ACE | rwb-payment as the owner of the booking and of the posting | TC-E4-046-01 |
| ADR-014 | Schema and login per service | `rwb_payment` and its own login, no cross-schema write | TC-E4-046-04 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `TreatmentBooked` outbox row and the inbox of the three consumed events | TC-E4-046-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows and the activity contract with their budget and breaker | TC-E4-046-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the request and before the event | TC-E4-046-02, TC-E4-046-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-046, disposition Split (rework) |
| Legacy criteria | AC2, owned word for word by this story; AC1 is owned by RWB-ITG-E4046-ITG |
| Test cases | TC-E4-046-01 to TC-E4-046-04, with the `-ITG` copies in the wave 3 harness |
| Feature and screens | FEAT-PAY-06 Post a settlement booking to ALS; SCR-29 Posting, with SCR-28 Proceeds matching kept by the matching story |
| Rules | R-SET-10 and R-SET-13 governed in rwb-decision, with R-RES-22 and R-RES-23 around them; the package code is not published (GAP-2548; ASM-4207) |
| Decoupling patterns | DP03, DP05, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The ALS interface row, its transport, format, attempts, retry intervals, exception queue, resend and the `outbound_item` lifecycle: RWB-P2-E4046-APP.
- AC1 of the legacy key and the cross-service evidence of the booking journey: RWB-ITG-E4046-ITG, which copies none of AC2.
- The published event schema, the fakes and the error set of this key: no contract story is allocated to it in the plan (GAP-2548; ASM-4207).
- The accepted settlement terms, the treatment state and the payment due date: rwb-treatment (S2).
- The case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The ACE account and payment facts, the batch status and the freshness of the data product: rwb-source-data (P1).
- The route set, its rule rows, its version and its release: rwb-decision (P7).
- The settlement payment match, the posting of the proceeds to the case balance and to the general ledger, and the posting file: RWB-P8-E4043-APP and the ledger story of this service.
- The roles, scopes and masking behind the Write-off and posting right: rwb-access (P4) and the guard of the service template.
- The gateway-bff composite route and the screen field lists of SCR-29 and SCR-28: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
