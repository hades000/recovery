# RWB-S6-E6007-APP Transfer the data to the buyer

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-K |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E6007-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E6-007 split out for rwb-debtsale. The four legacy acceptance criteria are kept word for word with their origin tag; the transfer becomes the settlement-and-transfer steps of `DebtSaleWorkflow` on task queue `rwb-debtsale`, which evaluates R-DS-25 on the buyer's settled fact and R-DS-29 on the transfer run, delivers the masked tape of the awarded lot to the buyer through rwb-integration's buyer-file delivery (INT-25, per lot), records the transfer as the lot status `TRANSFERRED` with a decision record written through the local decision-record library before the row changes (DP-03), publishes `rwb.debtsale.AccountsTransferred.v1` on the service topic (DP-14 naming, outbox by the platform library), answers rwb-case for the moves to `SETTLED` and `DATA_TRANSFERRED`, and serves the transfer state on `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19). TSD S6 T-A publishes no transfer operation of its own, and the two legacy endpoint rows, the award path and the data room read, belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E6007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer**, I want **the Workbench to send the awarded account data to the buyer and record the transfer**, so that **debt sales run on approved lots and masked data**.

This is the application slice of legacy RWB-E6-007, the FEAT-DBS-11 step of the S6 Debt sale module (FSD S6 A2.11). It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- the settlement-and-transfer steps of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case, with the transfer as the saga's pivot (Architecture v5 slide 19, "TMP DebtSaleWorkflow (saga, pivot = transfer)");
- the evaluation of R-DS-25 on the buyer's settled fact and of R-DS-29 on the transfer run, with the Debt sale route set and its package version in force;
- the delivery of the lot's masked data tape to the awarded buyer as a file through the data room, per lot, by the buyer-file delivery of rwb-integration (INT-25), built from the tape reference the lot already carries and from the `debt_sale_account` rows of the lot in `rwb_debtsale`;
- the record of the transfer: the lot status `TRANSFERRED` on `debt_sale_lot` (DF-SAL-030 against `LOV-LOT-STATUS`), the decision record of DP-03 and the event `rwb.debtsale.AccountsTransferred.v1` with the lot and buyer references, the transfer time and the account count;
- the answer to rwb-case for the case moves `SETTLED` and `DATA_TRANSFERRED`, with the rule ID and the version that produced each move;
- the transfer element served read only on `/api/recovery/debtsale/v1` (DP-13) for SCR-26 Award and PRT-05 Data room, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the transfer element, the event schema, the consumed rows, the case-move answer, the error set and the fakes, which are RWB-S6-E6007-CON; the award operation API-S6-003 `POST /debt-sale-lots/{lotId}/award` and its `DecisionLogEntry` answer, which are RWB-S6-E6005-APP's; the data room read API-S6-004 `GET /partner/data-room/{lotId}` and its `DataRoom` answer, which are RWB-S6-E5026-APP's; the masked tape build, which is RWB-S6-E5025-APP's; the matching of the buyer's remittance (FEAT-DBS-15) and its own record, which are RWB-S6-E6011-APP's; the derecognition and the general ledger posting of R-DS-30 to R-DS-33, which are RWB-S6-E6008-APP's; the buyer put-back claim of R-DS-34, which is RWB-S6-E6009-APP's; the case of record and its route states, which are rwb-case's (P3); the buyer panel and the buyer's KYC, licence and NDA facts, which are rwb-partner's (S9); the file transport itself and its encryption keys, which are rwb-integration's (P2); the central decision ledger and the rule rows, which are rwb-decision's (P7); the capability area and the rights, which are rwb-access's (P4); the partner gateway in the DMZ and its sign-in, which are the edge stories'; the debt buyers outside the bank, which are reachable only through the data room of the partner channel; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-007 let the Workbench send the awarded account data to the buyer and record the transfer, and the FSD keeps the objective and the metric unchanged: the debt sale turnaround is measured on the decision log and the Workbench records, reviewed monthly, with a 45-day target (FSD S6 A2.11.1). The program keeps the requirement as REQ-S6-008, "Data transfer, derecognition and the general ledger posting follow the award without re-keying" (Business Requirements Program v5; FSD S6 requirements served). The sale completes here: until the buyer holds the accounts, the award is a promise the bank has not kept.

In the monolith the settled state, the tape, the file write, the lot row, the decision log entry and the case stage sat in one `recovery` schema. In the target each is someone's:

- **the file is delivered by rwb-integration (P2), not written here.** Architecture v5 slide 19 gives rwb-debtsale "Integration: deliverFile (buyer file)" and the connection matrix gives S6 a Temporal call to P2; TSD S6 T5.1 keeps INT-25 "Debt buyers, Out, File through the data room, Per lot". The step therefore instructs the delivery and records the outcome, and builds no transport, holds no key and writes no shared directory (GAP-3004; ASM-4953).
- **the settled fact arrives from rwb-payment (P8).** S6 listens to P8's events in the connection matrix; R-DS-25 confirms the settlement and releases the transfer. The match of the buyer's remittance and FEAT-DBS-15 belong to RWB-S6-E6011-APP, and this step takes only the settled fact and its amount evidence (GAP-3004; ASM-4955).
- **the case stays with rwb-case (P3).** `SETTLED` and `DATA_TRANSFERRED` are route states of the case of record; this story evaluates the rules, writes its own rows and **answers** rwb-case for both moves.
- **the buyer stays with rwb-partner (S9).** The buyer reference on the lot (DF-SAL-025) is an identifier; the organisation, its panel status and its delivery contact are read on that contract and are never tables of this service.
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the lot change, which is what legacy AC1 asked for and legacy AC4 tested.
- **the transfer is published as an event.** Architecture v5 gives `rwb.debtsale.events.v1` the events `LotAwarded` and `AccountsTransferred` with consumers rwb-case and rwb-reporting; TSD S6 T5.3 lists `LotAwarded` alone. The event is taken from the Architecture v5 row, which outranks the TSD, and the difference is recorded (GAP-3004; ASM-4952).
- **the operation is not this story's.** TSD S6 T-A publishes five operations for the module and none of them is a transfer operation. The two endpoint rows of the legacy story are the award path (API-S6-003) and the data room read (API-S6-004), which are siblings'; the transfer runs unattended, is released by R-DS-25 and is visible on those two answers (GAP-3004; ASM-4958).

The metric and the business values do not move: the five-working-day target of R-DS-29, the 45-day turnaround, the `LOV-LOT-STATUS` values and the masking rules of the tape are read as rules and reference data with their version and are never written in code. The wave is EP06's wave 4 while rwb-debtsale is created in wave 3; the conflict is already recorded once for the service and the business epic and is not raised again here (GAP-1972; ASM-3194).

### 3. Preconditions

- RWB-S6-E6007-CON is published: the transfer element and the answer shapes it appears in, the `AccountsTransferred` schema, the consumed rows, the case-move answer, the error set and the fakes are baselined and handed to this story.
- The rwb-case case-state read and the case-move answer are available for the fake. No source publishes an operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-3004; ASM-4951).
- The rwb-partner read of the awarded buyer organisation is available for the fake, so the delivery target of the lot is known on Day 1. Its operation name is Not specified in the source documents (GAP-3004; ASM-4951), and the row is not in this story's contract-dependency list, which is None.
- The rwb-integration buyer-file delivery (`deliverFile`, INT-25) is available for the fake, with the delivery identifier, the file reference and the outcome it answers; its request and response shapes are fixed by RWB-S6-E6007-CON (GAP-3004; ASM-4953).
- The settled fact of the award is available for the fake as the release signal of the settlement step, carrying the buyer, the lot, the settled amount and the settled time; the `ProceedsMatched` subscription, its inbox row and the match itself are RWB-S6-E6011-APP's (GAP-3004; ASM-4955).
- The Debt sale rule package is in force at its version with R-DS-25 and R-DS-29; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`.
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the lot change, the outbox row and the record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award and PRT-05 Data room reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037; the platform library creates `decision_record`, `idempotency_key` and `outbox_event` in `rwb_debtsale` by its own migration. This story adds no table, no column and no migration of its own (GAP-3004; ASM-4954).
- The service runs as its own login on `rwb_debtsale` and holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, `rwb_partner`, `rwb_integration`, `rwb_payment` or `rwb_decision` fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E6007-CON when its tests pass.

### 4. Flow

1. The buyer of lot `LOT-2026-000042` pays in full inside the settlement term of R-DS-24. rwb-payment (P8) publishes `rwb.payment.ProceedsMatched.v1` and the settlement step of `DebtSaleWorkflow` receives it, matches it to the award and answers `SETTLED`; that step, its consumer group and its inbox row are RWB-S6-E6011-APP's (GAP-3004; ASM-4955).
2. The settlement-and-transfer branch of `DebtSaleWorkflow` on queue `rwb-debtsale` receives the release signal with the settled amount and time, reads the case state on the rwb-case contract to confirm `SETTLEMENT_PENDING`, reads the buyer organisation on the rwb-partner contract and loads the Debt sale package version in force.
3. `TransferEvaluator` confirms the settlement under R-DS-25: `payment received in full`. It records the confirmation and answers rwb-case with the move `SETTLED`, the rule ID, the version and the decided-at time. rwb-case writes the case row; this service writes neither the case nor its state. R-DS-25 is evaluated once per case: the settlement step made the same call on the same fact, and the confirmation here is the release the transfer needs, which the legacy story owns (ASM-4955).
4. With the case answered and the release given under R-DS-25, the transfer run of R-DS-29 is due within its five-working-day target, which is a timer of the workflow and a value of the rule row, not of the build.
5. `TransferRecordWriter` writes one decision record through the local decision-record library **before any change**: the case, the lot, the buyer, the rule ID with its version, the asset taken (the accounts of the lot), the outcome and the case move. A failed write stops the step with nothing changed (DP-03).
6. `BuyerFileClient` instructs the delivery of the lot's masked tape and its awarded account data through rwb-integration's `deliverFile` (INT-25, per lot), one activity on `rwb-integration`'s queue with the lot, the buyer, the tape reference and the account count. The file is encrypted, masked under PDPA and delivered through the data room; this service builds no transport and holds no key (GAP-3004; ASM-4953).
7. On the delivery answer the step writes, in one `rwb_debtsale` transaction: `status = TRANSFERRED` on `debt_sale_lot` (DF-SAL-030 against `LOV-LOT-STATUS`) with the optimistic lock of `version`, the delivery reference in the decision record, the outbox row and the idempotency row.
8. The outbox relay publishes `rwb.debtsale.AccountsTransferred.v1` with the CloudEvents envelope, carrying the lot and buyer references, the transfer time and the account count, and no account number, no name and no amount per account (GAP-3004; ASM-4952).
9. The step answers rwb-case with the move `DATA_TRANSFERRED`, the rule ID, the version and the decided-at time.
10. The transfer element is served read only on `/api/recovery/debtsale/v1` for SCR-26 Award and PRT-05 Data room through the gateway-bff composite route: lot, buyer, transfer state, delivery reference, transfer time, rule version. The buyer reads its own lot only, on the data room read API-S6-004, whose published surface is RWB-S6-E5026-APP's (DP-19).
11. A repeated settled fact or a repeated transfer run with the same lot, buyer and `Idempotency-Key` writes nothing, publishes no second event and answers no second move; the repeat is counted.
12. Where the delivery fails or the buyer asks for the file again inside the retention window, the step retries on the workflow's own schedule and records each attempt in the decision record; the put-back claim of R-DS-34 and the claim window belong to RWB-S6-E6009-APP.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no lot change, no outbox row and no case-move answer leaves the service | MSG-P7-003 | AC1, AC4, TC-E6-007-04, TC-E6-007-06 |
| X2 | The caller's role or partner identity does not hold the Debt sale or the Partner portal right | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E6-007-05 |
| X3 | The case is not in the state the rule expects (`SETTLEMENT_PENDING` for R-DS-25, `SETTLED` for R-DS-29) | 409 and nothing is written; no transfer is released twice | None | AC2, AC3 |
| X4 | The buyer-file delivery fails, or its answer carries no delivery reference | Nothing is written, the lot keeps `AWARDED`, the attempt is recorded and the step retries on the workflow's schedule inside the five-working-day target | None | AC1, AC2 |
| X5 | The rwb-case, rwb-partner or rwb-integration call does not answer inside 2 s, or its breaker is open, or the release signal of the settlement step is late | The step waits and retries on the workflow's own schedule; nothing is written and no case move is answered; a caller sees 503 with the platform error envelope | None | AC1, AC3 |
| X6 | The settled fact arrives for a lot whose award was cancelled under R-DS-26 or R-DS-27 | No rule fires, nothing changes and no transfer is released; the cancellation and the buyer score are the award and settlement stories' | None | AC3 |
| X7 | A required value of the delivery request is absent, or the lot carries no tape reference | The step holds, writes nothing and reports the missing value to the parent | MSG-GEN-001 | AC1, AC2 |
| X8 | A repeated settled fact or transfer run for the same lot, buyer and `Idempotency-Key` | One row, one event and one answer; the repeat is counted | None | AC2, AC3 |
| X9 | A component, a statement or a test reaches `rwb_case`, `rwb_partner`, `rwb_integration`, `rwb_payment` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR9 |

X1 to X3 and X8 are the exception paths of RWB-E6-007 carried onto the split, X4 to X7 are the paths the target call types and the file delivery add, and X9 is the DP-01 boundary. MSG-S6-001 is in the message set of the legacy story and names an open deviation on an account, which is the eligibility story's; no path here raises it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6007-CON and the rwb-case, rwb-partner, rwb-integration, rwb-payment and rwb-access fakes, on its own schema, and needs no live P3, P8, P2 or S9 |
| Negotiable | The step names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the transfer element and the two tables are fixed |
| Valuable | The buyer holds the accounts it bought and the bank has a recorded, evidenced transfer; the derecognition and the ledger posting can start from it |
| Estimable | Two workflow steps, one evaluator, one record write, one lot update, one outbox event, four clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots, buyers and deliveries through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Transfer the data to the buyer

  Background:
    Given case "RC-2026-000842" carries the debt sale lot "LOT-2026-000042" of segment "RETAIL", awarded to the buyer organisation "PTR-2026-000031"
    Given the Debt sale rule package is in force at its version and carries R-DS-25 and R-DS-29
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Transfer the data to the buyer (legacy RWB-E6-007 AC1)
    Given the rwb-payment contract mock returns the buyer remittance of lot "LOT-2026-000042" settled in full
    Given the rwb-integration contract mock returns the buyer file of lot "LOT-2026-000042" delivered with its delivery reference
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the awarded account data to the buyer and records the transfer
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-29 (legacy RWB-E6-007 AC2)
    Given the rwb-integration contract mock returns the buyer file of lot "LOT-2026-000042" delivered with its delivery reference
    Given the rwb-case contract mock returns the case state "SETTLED" for "RC-2026-000842"
    Given a case in state SETTLED
    When data transfer run
    Then transfer the account data to the buyer
    Then the case moves to DATA_TRANSFERRED

  Scenario: AC3 Rule R-DS-25 (legacy RWB-E6-007 AC3)
    Given the rwb-payment contract mock returns the buyer remittance of lot "LOT-2026-000042" settled in full
    Given the rwb-case contract mock returns the case state "SETTLEMENT_PENDING" for "RC-2026-000842"
    Given a case in state SETTLEMENT_PENDING
    When buyer settled
    Then confirm settlement and release the data transfer
    Then the case moves to SETTLED

  Scenario: AC4 Not recorded (legacy RWB-E6-007 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E6-007 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written`, `buyer settled`, `data transfer run` and `its trigger arrives` all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions. What the legacy lines describe happens in five places in the target. The settled fact is rwb-payment's (P8): this service listens to its `ProceedsMatched` event and takes the settled amount and time, while the match and the remittance record are RWB-S6-E6011-APP's. The delivery is rwb-integration's (P2): the masked tape and the awarded account data leave the bank as an encrypted file through the data room, per lot (INT-25), and this service instructs it and records its reference. The buyer is rwb-partner's (S9): the organisation and its delivery target are read on that contract and are never tables here. The case moves `SETTLED` and `DATA_TRANSFERRED` are **answered** to rwb-case, which writes the `recovery_case` row and its route state. The decision is recorded through the local decision-record library before the lot changes. Two notes are recorded rather than smoothed over. The legacy story lists two endpoint rows, the award path and the data room read; TSD S6 T-A publishes no transfer operation, so the step runs unattended on the settled fact and the rule timer and claims no operation of its own (GAP-3004; ASM-4958). `debt_sale_account` carries no transfer timestamp and no file reference, so the transfer is recorded on the lot status, the decision record and the event, and the missing column set is recorded (GAP-3004; ASM-4954). The fixtures carry organisation references, lot references, amounts and a rule version; no person name, no identity number, no date of birth and no account number of a person appears in them.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-25 | Debt sale | D8.4 | SETTLEMENT_PENDING | BUYER_SETTLED | payment received in full | Confirm settlement and release the data transfer | SETTLED | Workbench | ALS core and GL | None |
| R-DS-29 | Debt sale | D8.4 | SETTLED | DATA_TRANSFER_RUN | Any | Transfer the account data to the buyer | DATA_TRANSFERRED | Workbench | buyer portal | 5 working days |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the case moves to `SETTLED` and `DATA_TRANSFERRED` are written by rwb-case on this story's answer, the lot row, the delivery instruction and the event are this service's, the money behind `payment received in full` is rwb-payment's (P8), and the decision log row is written here through the local library of DP-03 and centralised by rwb-decision (P7). R-DS-30 to R-DS-33 (derecognition and the ledger) and R-DS-34 (the claim window) follow this step and belong to RWB-S6-E6008-APP and RWB-S6-E6009-APP.

| ID | Rule | Source |
|---|---|---|
| BR1 | The transfer fact is this service's: the lot status, the delivery reference and the transfer time are recorded in `rwb_debtsale`, and no other service writes them | Architecture v5 slide 19 (rwb_debtsale owns lots, data room, buyer terms, bids, award, transfer); TSD S6 T3.1 |
| BR2 | The decision is recorded before the lot row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2 ("writes the decision log entry before any change"); legacy RWB-E6-007 AC1 and AC4 |
| BR3 | The buyer panel and the buyer's organisation data stay with rwb-partner (S9): this story reads no `partner` row and takes the organisation on the owner's contract only | Architecture v5 slide 41; Ownership Map (`partner` and `partner_user` owner S9); GAP-3004 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (recovery_case owner P3); GAP-3004 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id` and `account_id` are identifiers of other services' facts | DP-01; TSD S6 T3.3 |
| BR6 | The file is delivered by rwb-integration's `deliverFile` (INT-25, per lot, encrypted, masked under PDPA); this service builds no transport, holds no key and writes no shared directory | Architecture v5 slide 19 (deliverFile, buyer file); TSD S6 T5.1; GAP-3004 |
| BR7 | The event is `rwb.debtsale.AccountsTransferred.v1` on `rwb.debtsale.events.v1`, written through the outbox in the same transaction as the lot row, with no account number, no name and no per-account amount | Architecture v5 event row (AccountsTransferred, consumers rwb-case and rwb-reporting); DP-09 library, DP-14 naming; GAP-3004 |
| BR8 | The five-working-day target of R-DS-29 and the lists `LOV-LOT-STATUS` (`BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED`, `CLOSED`), `LOV-SEGMENT` and `LOV-PUTBACK` are rule and reference values read with their version, never constants | TSD S6 T3.2; Business Rules and Routing Logic v4 R-DS-29; FSD S6 BR-S6-011 |
| BR9 | No person name, identity number, date of birth, contact value or unmasked account number enters `rwb_debtsale`, the event, the decision record, a log or a workflow input | Template and Rules v1 §R7.2 (s17); REQ-S6-003; FSD S6 A2.3 |
| BR10 | The same settled fact, transfer run or delivery answer twice, or the same `Idempotency-Key` twice, writes once, publishes one event and answers the case move once | TSD S6 T-A.2; Architecture v5 slide 11 |
| BR11 | The partner channel reads the transfer element through the partner gateway in the DMZ and the staff screens through the gateway-bff composite route; no screen calls a service directly | Architecture v5 slide notes (partner gateway in front of rwb-partner); DP-19 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story owns is the lot's sale state and the state of the step.

| From (lot) | Event | Condition | To |
|---|---|---|---|
| AWARDED | The buyer settles under R-DS-25 | payment received in full | AWARDED, the settlement recorded and `SETTLED` answered |
| AWARDED | The settled fact arrives | The case is in `SETTLEMENT_PENDING` for the lot | SETTLED, the transfer released |
| AWARDED | The settled fact arrives | The award was cancelled under R-DS-26 or R-DS-27 | Unchanged, no record and no answer (X6) |
| SETTLED | The transfer run under R-DS-29 | The delivery answers with its reference | TRANSFERRED, `AccountsTransferred` published and `DATA_TRANSFERRED` answered |
| SETTLED | The transfer run under R-DS-29 | The delivery fails or answers no reference | SETTLED, the attempt recorded, the retry inside the five-working-day target (X4) |
| TRANSFERRED | A later derecognition under R-DS-30 | RWB-S6-E6008-APP | Not this story: `DERECOGNISED` there |
| TRANSFERRED | A repeated settled fact or transfer run | X8 | Unchanged, the repeat is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The settled fact arrives for a case in `SETTLEMENT_PENDING` | The package in force is loaded | Evaluating |
| Evaluating | R-DS-25 fires | The decision record is written | Applying |
| Applying | The settlement is recorded and `SETTLED` answered | The transaction commits | Waiting for the transfer run |
| Waiting for the transfer run | R-DS-29 is due inside the five-working-day target | The delivery is instructed | Transferring |
| Transferring | The delivery answers with its reference | The lot row, the outbox row and the record commit together | Waiting for the next stage or closure |
| Transferring | The delivery fails, or the record write fails | X1, X4 | SETTLED, nothing changed, retry |

The states `SETTLEMENT_PENDING`, `SETTLED` and `DATA_TRANSFERRED` are those of the DEBTSALE machine of TSD S6 T4 and of the legacy criteria, and they live on the case of record. The lot status values are those of `LOV-LOT-STATUS` in TSD S6 T3.2, and the lot's own value is `TRANSFERRED` when this step ends.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: the primary role of the feature, holding the Debt sale right A on the lot that legacy RWB-E6-007 names, and reading the transfer state |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Debt sale RA: reads the transfer state and holds the Debt sale right A of the legacy permission table |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: reads the transfer state and holds the Debt sale right A of the legacy permission table |
| RW-CREDITAD, Credit Administration officer | Debt sale R: reads the transfer state, which is the fact the derecognition of R-DS-30 stands on |
| PT-BUYER, debt buyer and AMC | Partner portal RU, own lots only and scoped: reads its own lot and its delivered tape; sees no other buyer's |
| PT-RAMC | Partner portal R: reads its own lots and their transfer state |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the TSD S6 T6.1 matrix gives the service identities: the step runs under the service identity and is subject to the same checks |
| rwb-debtsale service identity | Runs the step, evaluates the rules, instructs the delivery, writes the decision record, the lot row and the outbox row, answers the case moves and serves the transfer element; it holds no grant on another schema |

The rights above are the rows of TSD S6 T6.1 and nothing wider. The legacy permission table gives the Partner portal right R to a long list of internal case roles; in the target the internal roles read the same transfer element on SCR-26 Award under their Debt sale right and the partner reads its own lot only. DP-08 is not in this story's pattern set: the capability area and the right are declared per surface and the guard of the access service is a service-template capability, so the check is stated here and not built here (GAP-3004; ASM-4951).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot the transfer is recorded against |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Read, the lot reference of the file and of the screen answer |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Read, the cut-off of the tape that is delivered |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Read, against `LOV-SEGMENT`, the population of the lot |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Not written here; read for the award comparison the buyer already passed |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Read, the awarded buyer the file is delivered to |
| DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_class | Read, against `LOV-BUYER-CLASS` |
| DF-SAL-027 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date | Not written here: the award story owns it |
| DF-SAL-028 | debt_sale_lot (S6, `rwb_debtsale`) | approval_authority | Not written here: the approval and award stories own it |
| DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | payment_terms | Read, the settlement term the R-DS-25 fact is tested against |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Write, against `LOV-LOT-STATUS`, to `TRANSFERRED` under R-DS-29 |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read, the awarded account set that is delivered; no column carries a transfer time or a file reference (GAP-3004; ASM-4954) |
| Standard columns | debt_sale_lot (S6, `rwb_debtsale`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, reason, case move, delivery reference, decided at | Write through the local library, before the lot row changes |
| DF-SAL-032, DF-SAL-035 | The delivered file (INT-25) | lot reference, account count, outstanding | Not stored here: the file is delivered by rwb-integration and its content is the masked tape of the lot (GAP-3004; ASM-4953) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case contract and the move is answered to it |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule id, rule version, route set, from state, event code | Not read as a table: the rule rows arrive in the package in force from rwb-decision |
| The awarded buyer | partner and partner_user (S9) | partner reference, organisation name, panel status, delivery target | Not read as a table: the organisation arrives on the rwb-partner contract and no personal data of any person is read (GAP-3004; ASM-4951) |

Field IDs are those of the TSD S6 Debt sale v2 T3.1 and the Logical Data Model and Data Dictionary v8, and the five rows of the legacy Data table, `recovery_case`, `assignment`, `treatment`, `decision_log_entry` and `rule_row`, are the rows of other owners in the target: `assignment` and `treatment` carry no fact of this step and are not read at all. **No new table, no new column and no migration**: `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_debtsale` by the library's own migration (DP-03).

**No personal data.** The rows this story writes carry identifiers, codes, amounts, dates, a count and a rule version. The file carries the masked tape of the lot and no unmasked personal data (REQ-S6-003); no name, identity number, date of birth, address or contact value of a person enters `rwb_debtsale`, the event, the decision record, a log or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module, API-S6-001 to API-S6-005, and none of them is a transfer operation: API-S6-001 and API-S6-002 are the lot create and the lot read, API-S6-003 the award, API-S6-004 the data room read and API-S6-005 the bid submission. The two endpoint rows of the legacy story are API-S6-003 `POST /debt-sale-lots/{lotId}/award` (Debt sale A) and API-S6-004 `GET /partner/data-room/{lotId}` (Partner portal R), which belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP. The transfer runs unattended, is released by R-DS-25 and is visible on those two answers, so this story provides no operation, claims no sibling's operation and adds no endpoint. The absence is recorded as GAP-3004 with ASM-4958.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the lot link; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3004; ASM-4951)) | rwb-case (P3) | P3 rwb-case | The answer that carries `SETTLED` or `DATA_TRANSFERRED` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The buyer organisation read (operation name Not specified in the source documents (GAP-3004; ASM-4951)) | `/api/recovery/partner/v1` | S9 rwb-partner | The organisation behind `buyer_partner_id`, its panel status and its delivery target; read only, faked. The panel family of the Ownership Map is `GET /partners` |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-3004; ASM-4951)) | `/api/recovery/access/v1` | P4 rwb-access | The capability areas "Debt sale" and "Partner portal", the right of the caller and the scope of its own lot; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-25 and R-DS-29; read only, faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-3004 with ASM-4951. The file delivery is not a REST row: it is the `deliverFile` activity of rwb-integration, a Temporal call that the connection matrix gives S6 to P2 and that carries the workflow's own retry policy (§12.5). DP-16 is not in the pattern set of this key although the delivery is rwb-integration's, so `RWB-P2-E1007-CON` is a tracked dependency and not a metadata row (GAP-3004; ASM-4953).

#### 12.3 Events published

| Event | Topic | Key | Consumers | Payload |
|---|---|---|---|---|
| `rwb.debtsale.AccountsTransferred.v1` (AccountsTransferred) | `rwb.debtsale.events.v1`, with its retry and `.dlt` topics | lot ID | P3 rwb-case, P9 rwb-reporting | The CloudEvents envelope and the transfer fact: lot reference, lot number, buyer reference, buyer class, account count, transfer time, delivery reference, rule ID and rule version. No account number, no name and no per-account amount (GAP-3004; ASM-4952) |

One event per lot and transfer, written to `outbox_event` in the same `rwb_debtsale` transaction as the lot row and relayed by the platform event library; the publication is not a second write. Architecture v5 gives the topic the events `LotAwarded` and `AccountsTransferred`, `LotAwarded` being RWB-S6-E6005-APP's; TSD S6 T5.3 lists `LotAwarded` alone, and the event catalogue publishes a payload for `LotAwarded` and none for `AccountsTransferred`, so the payload above is fixed by the contract baseline. The difference is recorded as GAP-3004 with ASM-4952. DP-09 is not in the pattern set of this key, so `RWB-PLT-TE006-CON` is a tracked dependency and not an H row.

#### 12.4 Events consumed

None of its own. Architecture v5 slide 19 IN gives rwb-debtsale one consumed event, `rwb.payment.ProceedsMatched.v1` (event 25) on `rwb.payment.events.v1`, and its consumer group and inbox row belong to the settlement step, RWB-S6-E6011-APP. The settled fact reaches this step as the release signal of `DebtSaleWorkflow` (the buyer, the lot, the settled amount and the settled time), so this story holds no subscription, no consumer group and no inbox row of its own, and a build that adds one fails the absence test (GAP-3004; ASM-4955).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer, continues-as-new across the settlement, the transfer and the put-back window | `rwb-debtsale` in namespace `rwb-recovery` | Input: the lot, the case, the route, the buyer and the rule package in force; signals: the settled fact, the case state answered by rwb-case, the delivery answer and the rule package in force |
| `settleAward` | Activity, the R-DS-25 step of this story | `rwb-debtsale` | The lot, the case and the settled fact in; the rule ID with its version, the settlement record and the `SETTLED` answer out |
| `transferAccounts` | Activity, the R-DS-29 step of this story | `rwb-debtsale` | The lot, the buyer, the tape reference and the account count in; the delivery reference, the lot status, the outbox row, the decision record and the `DATA_TRANSFERRED` answer out, in one transaction |

No child workflow for the case and no workflow for the money exists in this service. The activity names are target design choices of this story and are fixed by no source document. The trigger is read as the settled fact for R-DS-25 and the rule timer for R-DS-29, because the FSD declares the feature unattended and no background event (FSD S6 A2.11.3.3, "None; runs unattended"; A2.11.4.4, "No background event"). The saga steps of reserve, approval, payment match, derecognition, ledger posting, case closure and customer notices belong to the award, settlement, derecognition, closure and notice stories of this service; this story owns the settlement and transfer steps.

#### 12.6 Schedules

None. The five-working-day target of R-DS-29 is a durable timer of `DebtSaleWorkflow`, not a Temporal Schedule; the step owns no Schedule, no legacy Quartz job and no shared job table, and no Job of Architecture v5 slide 44 is owned or moved here. The monthly sale cycle is triggered from the case and the ACE data of the lot building and award stories, not from this step.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer reference, its payment terms and its status; this story writes `status` and the standard columns |
| debt_sale_account | S6 (`rwb_debtsale`) | The awarded account set that is delivered; read only here (GAP-3004; ASM-4954) |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the settlement and of the transfer (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated settled fact, transfer run or delivery answer |
| outbox_event | PLT library, created in `rwb_debtsale` | The `AccountsTransferred` row, written in the lot's transaction and relayed by the platform (DP-09) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `partner`, `partner_user` and the panel tables (S9), `role`, `permission` and the scope rows (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` and the remittance rows (P8), the file and delivery tables of rwb-integration (P2) and every `v_ace_*` view (P1). No foreign key leaves the schema and `debt_sale_lot.buyer_partner_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Settled-fact signal fake (the fact of `rwb.payment.ProceedsMatched.v1`, event 25, replayed as the settlement step's signal) | The settlement of lot `LOT-2026-000042` for buyer `PTR-2026-000031` in full at `2026-11-18T10:00:00Z`; a partial amount; a settled fact for a cancelled award; a late signal | AC1, AC3, X5, X6 |
| rwb-integration delivery fake | The buyer file of `LOT-2026-000042` delivered with reference `DLV-2026-000118`; a failed delivery; an answer with no reference; no answer beyond 2 s | AC1, AC2, X4, X5 |
| rwb-case case-state fake | The states `SETTLEMENT_PENDING`, `SETTLED` and `AWARDED` of case `RC-2026-000842`; a case that is not in the state the rule expects | AC2, AC3, X3 |
| rwb-case case-move fake | The moves `SETTLED` and `DATA_TRANSFERRED` accepted; a move refused because the case is not in the state the rule expects | AC2, AC3, X3 |
| rwb-partner buyer fake | The organisation `PTR-2026-000031` on the panel, active, with its delivery target; an organisation suspended after the award; no answer beyond 2 s | AC1, X5 |
| rwb-access authorise fake | The capability area "Debt sale" with right A, R or U and "Partner portal" with right R or U for `PT-BUYER`, scoped to its own lot; a caller without the right | AC1, X2 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-25 and R-DS-29 | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-26 Award answer for lot `LOT-2026-000042` and case `RC-2026-000842`, with the transfer element read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-partner buyer read, the rwb-case move answer, the rwb-access authorise call and the rwb-integration delivery activity are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3004; ASM-4951).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 5 consumed | The rwb-case state read and move answer, the rwb-partner buyer read, the rwb-access authorise call and the rwb-decision package read; one hop and 2 s each |
| Kafka | 1 published, 0 consumed | `AccountsTransferred` on `rwb.debtsale.events.v1` for rwb-case and rwb-reporting; `rwb.payment.ProceedsMatched.v1` is consumed by the settlement step, RWB-S6-E6011-APP's, and reaches this step as a signal |
| Temporal | 1 workflow, 2 local activities and 1 remote activity | `DebtSaleWorkflow` with `settleAward` and `transferAccounts` on `rwb-debtsale`, and the `deliverFile` activity on `rwb-integration`; no Schedule |
| File | 1 out | The masked tape and the awarded account data of the lot, delivered by rwb-integration as an encrypted file through the data room, per lot (INT-25) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `transfer`, Java package `th.co.scb.ace.workbench.recovery.debtsale.transfer`; front end `src/modules/recovery/debtsale/Transfer.tsx`, the fragment SCR-26 Award and PRT-05 Data room embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of both steps: the record and the lot update commit together or not at all. DP-13 moves the base of the transfer element and nothing else. DP-19 is how SCR-26 Award and PRT-05 reach this service, one hop through the gateway, and it is also the boundary of the partner channel, which reads the same element through the partner gateway. The naming of the event follows DP-14 and the outbox follows DP-09; neither is in the pattern set of this key and both are tracked, not added to the metadata rows (GAP-3004; ASM-4952).

**Dependencies the tables add and the plan does not hold.** The six consumed rows and the file delivery are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-3004. DP-08 is not in the pattern set although the surfaces declare a capability area and a right; DP-09 is not in it although an event is published; DP-16 is not in it although the file delivery is rwb-integration's. None is added to the metadata rows and all three are named in the text and in the registers (ASM-4952, ASM-4953).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` settlement and transfer branch | Workflow | Waits for the settled fact, releases the transfer under R-DS-25 and R-DS-29, holds the five-working-day timer and reports the outcome to the parent |
| `settleAward` | Activity | Reads the case and the settled fact, evaluates R-DS-25, writes the settlement record and answers `SETTLED` |
| `transferAccounts` | Activity | Reads the lot, the tape and the account set, instructs the delivery, writes the record, the lot status and the outbox row and answers `DATA_TRANSFERRED` |
| `TransferEvaluator` | Service | The rule evaluation against the Debt sale package version in force, with the settlement and lot-status values of the closed lists |
| `TransferRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `TransferRepository` | Repository | Updates `debt_sale_lot`, reads the `debt_sale_account` rows, writes the outbox row and the idempotency row in one `rwb_debtsale` transaction, with the optimistic lock |
| `BuyerFileClient` | Client | The `deliverFile` instruction of rwb-integration (P2) as a Temporal activity, with the workflow retry policy and the delivery reference |
| `PartnerBuyerClient` | Client | The buyer organisation read of rwb-partner (S9), one hop, 2 s, breaker, no retry of its own |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case, one hop, 2 s |
| `AccessGuardClient` | Client | The capability area and the right of rwb-access (P4), through the service-template guard |
| `TransferController` | Controller | The read of the transfer element on the service base, the capability area and right, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503; it declares no operation that TSD S6 T-A does not publish (GAP-3004; ASM-4958) |
| `Transfer` | React component | Shows the transfer state, the delivery reference and the transfer time on SCR-26 Award and PRT-05 Data room, read only |

**Database and migrations.** No Flyway file of this story. `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, the decision record, the idempotency key and the outbox are library objects created in `rwb_debtsale` by the library's migration (DP-03, DP-09), and no transfer timestamp and no file reference column is added to `debt_sale_account` (GAP-3004; ASM-4954).

**Configuration and reference data.**

- `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The Debt sale package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the five-working-day target and the settlement condition of R-DS-25 are values of the package, not of this build.
- The capability areas "Debt sale" and "Partner portal" and their rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the steps themselves; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The settlement and transfer branch of `DebtSaleWorkflow` and its input record, registered on `rwb-debtsale` as the stage child of `CaseWorkflow`.
2. The release signal of the settlement step and the settled fact it carries, with the cancelled-award path (AC1, AC3, X6).
3. `PartnerBuyerClient` and `CaseStateClient` against their fakes, with the 2 s budget, the breaker and the no-answer path (AC1, AC2, AC3, X5).
4. `AccessGuardClient` and the two capability areas, with the refusal path (AC1, X2).
5. `TransferEvaluator` over the Debt sale package, with R-DS-25 and R-DS-29, the closed lists and the no-fire path (AC2, AC3, X6).
6. `TransferRecordWriter` against the library stub, with the failed-write path (AC1, AC4, X1).
7. `BuyerFileClient` and the delivery instruction, with the failure and no-reference paths (AC1, AC2, X4).
8. `TransferRepository` with the one transaction, the lot status, the outbox row, the idempotency row and the optimistic lock (AC2, X8).
9. The outbox relay and the `AccountsTransferred` schema, with the no-personal-data test (AC1, AC2, BR7, BR9).
10. `CaseMoveAnswer` and the parent signal, with the two moves (AC2, AC3).
11. `TransferController` and `Transfer` through the composite route fake (AC1).
12. The boundary test: no statement outside `rwb_debtsale`, no read of `partner`, `recovery_case`, `role`, `rule_row` or a delivery table, and no write to another service's schema (X9, BR5, BR9).

**Feature flag.** `rwb.debtsale.transfer-v1`, read as a flag of the platform library; off means the step holds the settled fact, writes nothing, publishes no event and answers no move, and the award and derecognition stories are unaffected.

**Done when.** The tests of section 16 pass, the steps run from a synthetic settled fact in SIT, each rule produces its record, its lot change, its event and its move, a repeated fact or run writes once, a forced record or delivery failure changes nothing, no `partner`, `recovery_case` or delivery row and no `v_ace_*` read exists in the build, and SCR-26 Award and PRT-05 answer through the composite route and the partner gateway.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the delivery request or of the lot fact is absent or invalid (X3, X7) | Enter {field}. |
| MSG-P4-002 | A role or a partner identity without the right of the capability area reads the transfer element or requests the delivery (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are those of the legacy message set and of FSD S6 A2.11.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S6-001 is carried because it is in the message set of the feature, and no path of this story raises it. The failure of the file delivery carries no message of the set: it is an internal path that holds the step and records the attempt (X4).

### 15. Screens and states

SCR-26 Award in its open, closed, awarded and transferred states is served through the gateway-bff composite route (DP-19), and PRT-05 Data room, "lot data tapes and documents for admitted buyers, with bids" (FSD S6 Screens), is served to the partner on the same service base through the partner gateway in the DMZ. The route calls rwb-debtsale for the lot and the transfer element, rwb-case for the case and its route state and rwb-partner for the buyer organisation; this story fixes the transfer element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are `SETTLED` with the settlement recorded and `TRANSFERRED` with the delivery reference and the transfer time, and it shows the failure states it reads: refused with MSG-P4-002, not recorded with MSG-P7-003, and an incomplete request with MSG-GEN-001. The award, settlement and put-back states of SCR-26 belong to the award, settlement and put-back stories of this service and are read from the same route. The buyer's own view is PRT-05, scoped to its lots, where the delivered tape and the transfer state appear once the step has answered.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-007-01 | AC1 | Component | Lot `LOT-2026-000042` settled in full for buyer `PTR-2026-000031`; the delivery instructed, the record, the lot change and the event asserted on the fakes |
| TC-E6-007-02 | AC2 | Integration | Case `RC-2026-000842` at `SETTLED`; the delivery answered with `DLV-2026-000118` and `DATA_TRANSFERRED` answered end to end on the fakes |
| TC-E6-007-03 | AC3 | Component | Case `RC-2026-000842` at `SETTLEMENT_PENDING` with the settlement in full; R-DS-25 evaluated and `SETTLED` answered |
| TC-E6-007-04 | AC4 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E6-007-05 | Access | Component | A role and a partner identity without the Debt sale or the Partner portal right; 403 with MSG-P4-002 and no read |
| TC-E6-007-06 | Principle 5 | Component | A forced decision log write failure at the moment of the lot update; no lot change, no event and no second attempt |

The six legacy cases are the legacy cases of RWB-E6-007 in their legacy order, with the Level column added: `System` maps to `Component` where the step is tested on its fakes, and TC-E6-007-02 maps to `Integration` because it crosses the rwb-integration and rwb-case boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and no `-ITG` copy is written here.

### 17. Guardrails

- No business value in code: the five-working-day target, the settlement condition, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_debtsale`, in the event, in a workflow input or in a log: identifiers, codes, counts, dates and a rule version only, and the delivered file is the masked tape of the lot. Every fixture is synthetic.
- ACE data only through the owner's contract: this service reads no ACE table and no `v_ace_*` view, and a build that adds one fails the boundary test.
- The case stays with rwb-case, the buyer with rwb-partner, the file transport with rwb-integration and the central ledger with rwb-decision: no `recovery_case` row, no `partner` row, no delivery row and no `decision_log_entry` row is written here (BR3, BR4, BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13).
- No operation of a sibling is claimed: the award path is RWB-S6-E6005-APP's and the data room read is RWB-S6-E5026-APP's, and a story that declares them as its own fails the review (GAP-3004).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no second event and no local file directory.
- The decision is recorded before the change and the move is answered, not written; a build that writes a case row or records after the update fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying (Business Requirements Program v5; FSD S6 requirements served); the split plan carries no requirement id for this slice (GAP-3004; ASM-4951) | The settlement and transfer steps, R-DS-25 and R-DS-29, the delivery instruction, the decision records, the event and the two case moves | TC-E6-007-01, TC-E6-007-02, TC-E6-007-03, TC-E6-007-04 |
| REQ-S6-003 | The data room holds a masked data tape, and no unmasked personal data leaves the bank | The delivered file is the masked tape of the lot and the event carries no per-account data | TC-E6-007-01, TC-E6-007-02 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the lot and of the transfer fact | TC-E6-007-02 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E6-007-06 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `AccountsTransferred` outbox row and the CloudEvents envelope; the `ProceedsMatched` inbox row is the settlement step's | TC-E6-007-01, TC-E6-007-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed rows with their budget | TC-E6-007-01, TC-E6-007-03 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the lot changes | TC-E6-007-04, TC-E6-007-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-007, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E6-007-01 to TC-E6-007-06 |
| Feature and screens | FEAT-DBS-11 Transfer the data to the buyer, SCR-26 Award and PRT-05 Data room |
| Rules | R-DS-25 and R-DS-29, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the transfer element, the event schema, the consumed rows, the error set and the fakes: RWB-S6-E6007-CON.
- The award operation API-S6-003 and its `DecisionLogEntry` answer: RWB-S6-E6005-APP (GAP-3004).
- The data room read API-S6-004 and its `DataRoom` answer: RWB-S6-E5026-APP.
- The masked data tape and its build: RWB-S6-E5025-APP.
- The matching of the buyer's remittance, the remittance record and FEAT-DBS-15: RWB-S6-E6011-APP (GAP-3004).
- The derecognition and the general ledger posting of R-DS-30 to R-DS-33: RWB-S6-E6008-APP.
- The buyer put-back claim of R-DS-34 and the claim window: RWB-S6-E6009-APP.
- The cancellation of an award under R-DS-26 and R-DS-27 and the buyer score: the award and settlement stories of this service.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes.
- The buyer panel, the partner users and the buyer's KYC, licence and NDA facts: rwb-partner (S9) (GAP-3004).
- The file transport, its encryption, its keys and its retention: rwb-integration (P2) and the platform security stories (GAP-3004).
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4).
- The central decision ledger, the rule rows, their approval and their versioning: rwb-decision (P7).
- The partner gateway in the DMZ and its sign-in, and the gateway-bff composite route with the screen field lists of SCR-26 and PRT-05: the edge stories and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
