# RWB-S6-E6008-APP Derecognize and post to the general ledger

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S6-L |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S6-E6008-APP-16); the squad sets size at refinement |
| Contract version | v1 (base path `/api/recovery/debtsale/v1`, RWB-S6-E6008-CON) |
| Depends on (build) | RWB-S6-E6008-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the derecognition and posting slice of RWB-E6-008 in rwb-debtsale. The one legacy criterion this story owns (AC4) is kept word for word with its origin tag; the step applies R-DS-30 to remove the transferred accounts from the book and R-DS-31 to post to ALS and the general ledger and send the provision input to Finance, with R-DS-32 and R-DS-33 on the hold and re-post paths, records each outcome through the local decision-record library before anything leaves (DP-03), reads the account and balance facts on rwb-source-data's contract (DP-05) and the case state and move on rwb-case's, and sends the posting items through rwb-integration's outbound interface; it provides no operation of its own and the posting state is read from the case state behind SCR-26 through the gateway-bff composite route (DP-13, DP-19). AC1 to AC3 are RWB-ITG-E6008-ITG's by the split; no column of `debt_sale_lot` or `debt_sale_account` carries the posting result, so the record and the case state carry it; the plan's C row is None while four consumed surfaces exist. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E6008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (32 resolved, 16 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer**, I want **the Workbench to remove the sold accounts from the book and post the result to ALS and the ledger**, so that **debt sales run on approved lots and masked data**.

In the target, this is the derecognition and posting step of `rwb-debtsale`, which takes the lot whose data transfer is complete, records the decision that removes the balance, sends the posting items for ALS, the general ledger and the Finance provision feed, and answers the case move.

This is the derecognition and posting slice of legacy RWB-E6-008 (FEAT-DBS-12, module S6 Debt sale, priority Must, depends on FEAT-DBS-11). It owns:

- the legacy acceptance criterion AC4 of the key, copied verbatim with its origin tag; AC1, AC2 and AC3 of the key are RWB-ITG-E6008-ITG's by the split the plan fixes, and are asserted there as the cross-service journey (section 7);
- the derecognition step (`derecogniseAccounts`) of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`: R-DS-30 "Derecognise the balance on the account", from `DATA_TRANSFERRED` to `DERECOGNISED`;
- the posting step (`postToLedger`): R-DS-31 "Post to the general ledger and send the provision input to Finance", from `DERECOGNISED` to `GL_POSTED`, with R-DS-32 holding a rejected posting at `POSTING_REJECTED_DS` and raising the exception task, and R-DS-33 re-posting to `GL_POSTED` once the rejection cause is cleared;
- the posting items this service sends out: the ALS balance-removal item, the general ledger entry item and the Finance provision input, each one item on the outbound interface of rwb-integration with an `Idempotency-Key`, and the item reference and result code that come back;
- the local decision record of every outcome — rule ID, package version, inputs reference, item reference, result, case move — written through RWB-PLT-E1027-CON before anything leaves (DP-03), with MSG-P7-003 when it cannot be written (legacy AC4);
- the account and balance facts of the transferred accounts read on rwb-source-data's contract (DP-05), the DEBTSALE package at its version in force read on rwb-decision's, and the case state read and the case move `DERECOGNISED`, `GL_POSTED` or `POSTING_REJECTED_DS` answered to rwb-case;
- the posting state of the lot on SCR-26 Award, in its transferred and posted readings, behind the gateway-bff composite route (DP-19), from the case state and the lot read of this service on base `/api/recovery/debtsale/v1` (DP-13).

It does not own: the published shape of the posting and derecognition elements, the state and list vocabulary, the consumed rows, the rights, the error envelope and the fakes, which are RWB-S6-E6008-CON; the data transfer of R-DS-29 and `AccountsTransferred`, which are RWB-S6-E6007-APP; the award, `LotAwarded` (EV-23) and the settlement, which are RWB-S6-E6005-APP and RWB-S6-E6011-APP; the put-back claim and the lot closure of R-DS-34 to R-DS-39, which are RWB-S6-E6009-APP; the case of record and its route states, which are rwb-case (P3); the account, balance and ALS facts, which are rwb-source-data's (P1); the package and the central ledger, which are rwb-decision's (P7); the ledger interface itself, its files, result codes and exception queue, which are rwb-integration's (P2); the accounting rules of ALS and of the general ledger; the cross-service journey of the key, which is RWB-ITG-E6008-ITG; and the deployment of this build, which is the operations story of the key.

### 2. Business rationale

A sold account that is never removed from the book keeps accruing in ALS after the bank has been paid for it, and a posting that never leaves leaves the recovery out of the ledger and the provision out of Finance's view. The legacy feature did the derecognition and the posting in process against the `recovery` schema with no observable seam between the case, the book and the ledger. The objective, the problem and the metric are unchanged: removes the sold accounts from the book and posts the result to ALS and the ledger (FSD S6 A2.12.1; FEAT-DBS-12), because debt sales run on spreadsheets with no baseline turnaround (FSD S6 A1.3), with the turnaround measured on the decision log and the Workbench records against 45 days, reviewed monthly (FSD S6 A2.12.1).

What D-RCV-60 changes is who owns each half of the sentence.

- **The lot and its population are this service's.** `debt_sale_lot` and `debt_sale_account` are S6's two tables in `rwb_debtsale` (context pack ownership rows; TSD S6 T3.1), so the lot a transfer completes is read here and no other service reads it.
- **The book is ALS's, not this service's.** Derecognition is a book event: this step announces the removal of the balance as an item on rwb-integration's interface and keeps the result; it writes no ALS row and holds no `v_ace_*` grant (ASM-4961, ASM-4963).
- **The account and balance facts stay with rwb-source-data.** The legacy Data table names `v_ace_account` with DF-ACE-001 to DF-ACE-042; in the target only rwb-source-data holds those views, so the facts arrive on the owner's contract and are never joined here (ASM-4961).
- **The case stays with rwb-case.** `recovery_case`, the route states `DERECOGNISED`, `GL_POSTED` and `POSTING_REJECTED_DS` are P3's; this step answers the move with the rule and its version and writes no case row (ASM-4961).
- **The decision is recorded first**, in the transaction that keeps the result, which is what legacy AC4 tests: a posting that cannot be recorded changes nothing and leaves no item behind (DP-03; ADR-022).
- **The posting result has no column of its own.** Neither TSD S6 T3.1 nor the legacy Data table gives `debt_sale_lot` or `debt_sale_account` a posting reference, a result code or a rejection reason, so the record and the case state carry them and this story adds no column (GAP-3006; ASM-4965).
- **The month-end clock is the rule's.** R-DS-31 carries "month-end close" in its timer column and the service owns no job row (context pack, jobs 0), so the wait is a durable timer of the workflow and not a Schedule (ASM-4966).

No business value is invented: the chart of accounts, the entry set of the derecognition and of the posting, the provision input layout, the result codes of ALS and of the general ledger and the posting window are named by no source in the read set, so they stay unstated with the placeholder and the recorded gap and assumptions (GAP-3006; ASM-4960, ASM-4963).

### 3. Preconditions

- RWB-S6-E6008-CON is published: the derecognition and posting elements, the state and list vocabulary, the four consumed rows, the posting item and its result set, the rights, the error envelope and the fakes. This story builds behind that baseline and adds no shape of its own.
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003, so the record and the item commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award reaches this service and rwb-case through the gateway-bff composite route, one hop, read only (DP-19).
- The outbound interface of rwb-integration is callable as a task on queue `rwb-integration` from this service's identity, and its interface identifier, transport, file layout, result codes and retry schedule are rows of the integration's interface configuration read per item. All of them are Not specified in the source documents (GAP-3006; ASM-4960, ASM-4963).
- rwb-source-data answers the account, balance and ALS facts of the transferred accounts, with the as-of date of the product, because this service holds no `v_ace_*` grant and reads no ACE table; the operation name is Not specified in the source documents (GAP-3006; ASM-4961).
- rwb-case answers the case state and accepts the move, with the case reference and the route state; the operation name of the case-move answer is Not specified in the source documents (GAP-3006; ASM-4961).
- rwb-decision answers the DEBTSALE package at its version in force with R-DS-29 to R-DS-33 among its 41 rules over 29 states; the operation name of the package read is Not specified in the source documents (GAP-3006; ASM-4960).
- The transfer of R-DS-29 is complete: the lot is awarded and its data is with the buyer, so the accounts of the lot stand at `DATA_TRANSFERRED` on the case. RWB-S6-E6007-APP writes the transfer and `AccountsTransferred`; this story only reads the state it produced.
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on schema `rwb_debtsale`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_account` or on `rwb_case` is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E6008-CON when its tests pass. No approved baseline exists for the key — FSD S6 v3 and TSD S6 v2 stand at "In review" — so the story proceeds in Draft (realignment v1) and the release 30 April 2027 is copied unchanged and marked tentative (ASM-4967).
- The metadata wave is EP06's wave 4 while the service itself is created in wave 3 (Template and Rules §R5.6), so the step lands with the service's wave 4 build; the Day-1 rule still sets its start because its build dependencies are the contract baseline and two platform contracts (ASM-4968).

### 4. Flow

1. The transfer step completes: the awarded lot's data is with the buyer and the cases of the lot stand at `DATA_TRANSFERRED` under R-DS-29. The parent `CaseWorkflow` forwards the move to the `DebtSaleWorkflow` child of the case on queue `rwb-debtsale` (Temporal and Drools Design slide 13).
2. The derecognition step of `DebtSaleWorkflow` receives its trigger `DERECOGNITION_RUN` for the lot and reads the version of the DEBTSALE package in force on rwb-decision's contract, one hop with a 2 s budget and a breaker.
3. `TransferredAccountReader` reads the accounts of the lot on rwb-source-data's contract: the account reference, the account code, its status, the contract number, the total balance and the outstanding the sale was priced on, with the as-of date of the product. A product that is stale after a late or failed ACE batch holds the step with VR-S6-012-1 and MSG-P1-001 and nothing is written.
4. `DerecognitionEvaluator` evaluates R-DS-30 for each account: where the trigger is the derecognition run of a transferred lot, the balance on the account is removed. The rule answers its ID, the package version, the action and the case move `DERECOGNISED`.
5. `DebtSaleDecisionRecordWriter` writes one decision record per outcome through the local decision-record library, **before anything leaves**: the case reference, the lot reference, the account reference, the rule ID with its package version, the inputs reference with the as-of date of the product, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC4).
6. `PostingItemBuilder` assembles the three posting items of the lot from data: the ALS balance-removal item, the general ledger entry item and the Finance provision input. The entry set, the chart-of-accounts reference and the provision layout are data of the interface rows and of the ledger, never constants of this service (GAP-3006; ASM-4963).
7. `PostingSender` sends each item through the outbound interface of rwb-integration as a task with a manifest — interface reference, business date, case, lot, account set, amount, the posting facts block and an `Idempotency-Key` — and receives the item reference and the result code.
8. The posting step evaluates R-DS-31 at the month-end close: where the items are accepted, the step writes its own decision record with the item references and the result codes in its outcome and **answers the case move `GL_POSTED`**. rwb-case writes the case row; this service writes neither the row nor the state.
9. Where ALS or the general ledger rejects an item, R-DS-32 holds the posting: the rejection code and the item reference are written to the record, the exception task is raised for the Credit Administration officer, the case move `POSTING_REJECTED_DS` is answered, and no second item is sent until the cause is cleared.
10. Where the rejection cause is cleared, R-DS-33 re-posts: a new item is built from the corrected facts with a new `Idempotency-Key`, its record names R-DS-33 and the previous item reference, and the case move `GL_POSTED` is answered. The re-post is one step under the service identity, because the rights matrix gives the officer read only (section 10).
11. A repeated trigger for the same lot, business date and package version writes no second record, sends no second item and answers no second move; the item key answers the item that exists.
12. SCR-26 Award shows the lot in its transferred, posted and rejected readings: the lot and its accounts from this service, the case state from rwb-case, merged by the gateway-bff composite route, one hop, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes and no item leaves: no record, no sending, no case move; an incident is raised | MSG-P7-003 | AC4, TC-E6-008-04, TC-E6-008-06 |
| X2 | The role does not hold the Debt sale right of the surface | 403 before any read; nothing changes and no record is written | MSG-P4-002 | AC5, TC-E6-008-05, TC-E6-008-26 |
| X3 | The case is not at `DATA_TRANSFERRED` when the run arrives, or has left the lot since it was read | 409 and nothing is written for that case; a case that has already moved is not derecognised twice | None | AC4, X7 |
| X4 | The account or balance product is stale after a late or failed ACE batch | The step holds, writes nothing and shows the data date; the run resumes on the next fresh answer | MSG-P1-001 | AC6, TC-E6-008-27 |
| X5 | rwb-source-data, rwb-case or rwb-decision does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | AC7, TC-E6-008-09 |
| X6 | ALS or the general ledger rejects the posting | R-DS-32 holds the posting at `POSTING_REJECTED_DS`, writes the rejection code to the record, raises the exception task and sends no further item | Not specified in the source documents (DOR-RWB-S6-E6008-APP-9) | AC8, TC-E6-008-10 |
| X7 | The same lot, business date and package version arrive twice, or the same `Idempotency-Key` twice | One record, one item set and one answer per case; the repeat is counted and the key answers the item that exists | None | AC9, TC-E6-008-11 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC10, TC-E6-008-12, Section 17, BR5, BR8 |
| X9 | The interface row has been changed since the last item, or no interface row is in force at the business date | The next item obeys the new version, or no item is created and the lot stays unposted with the refusal in the run log | MSG-GEN-001 | AC11, TC-E6-008-13 |

X1 is the legacy exception path carried onto this slice (legacy AC4), X2 to X5 and X7 are the paths the target call types add, X6 is rwb-integration's rejection path, and X8 and X9 are the boundary and the interface-configuration paths.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6008-CON, the rwb-source-data, rwb-case and rwb-decision fakes, the rwb-integration interface fake and the decision-record stub, on its own schema, and needs no live P1, P2, P3 or P7 |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the states, the lists and the four consumed surfaces are fixed |
| Valuable | The sold accounts leave the book and the posting, the provision input and the record of both exist, so a sale is provably complete and the 45-day turnaround is measurable |
| Estimable | Two workflow steps, one evaluator, one record write, one item builder and sender, one reader, one case-move answer and one read-only screen reading |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | AC4 runs on the fakes with the record stub stopped; the derecognition, the posting, the rejection, the re-post and the repeat are each one component case |

### 7. Acceptance criteria

```gherkin
Feature: Derecognize and post to the general ledger

  Scenario: AC4 Not recorded (legacy RWB-E6-008 AC4)
    Given the rwb-integration contract mock returns the posting item of the derecognized accounts and its acknowledgement
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Role without the Debt sale right is refused (X2) (new, D-RCV-60)
    Given a role without the Debt sale right of the surface reads the lot
    When the read is made
    Then the request is refused with 403 before any read, nothing is written and the user sees MSG-P4-002

  Scenario: AC6 Stale account or balance product holds the step (X4) (new, D-RCV-60)
    Given the account or balance product is stale after a late or failed ACE batch
    When the derecognition run reads the lot
    Then the step holds, writes nothing and the user sees MSG-P1-001 with the data date

  Scenario: AC7 A dependency does not answer inside 2 s (X5) (new, D-RCV-60)
    Given rwb-source-data, rwb-case or rwb-decision does not answer inside 2 s or its breaker is open
    When the step calls it
    Then the step retries on the workflow's own schedule, nothing is written, no move is answered and the caller sees 503 with the platform error envelope

  Scenario: AC8 ALS or the general ledger rejects the posting (X6) (new, D-RCV-60)
    Given ALS or the general ledger rejects the posting item
    When the rejection is received
    Then the posting is held at POSTING_REJECTED_DS, the rejection code is written to the record, the exception task is raised and no further item is sent

  Scenario: AC9 The same lot, business date and package version, or the same Idempotency-Key, arrives twice (X7) (new, D-RCV-60)
    Given the same lot, business date and package version arrive twice, or the same Idempotency-Key arrives twice
    When the run is triggered again
    Then one record, one item set and one answer per case exist, the repeat is counted and the key answers the item that exists

  Scenario: AC10 A statement reaches a v_ace_* view, a recovery_case row or another service's schema (X8) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case row or another service's schema
    When the build runs
    Then the grant refuses the statement, the boundary test fails the build and nothing is released

  Scenario: AC11 The interface row has changed or is absent at the business date (X9) (new, D-RCV-60)
    Given the interface row has been changed since the last item, or no interface row is in force at the business date
    When the posting run prepares the item
    Then the next item obeys the new version, or no item is created, the lot stays unposted and the refusal is in the run log

  Scenario: AC12 The rules BR1 to BR11 hold at build (section 8) (new, D-RCV-60)
    Given the rules BR1 to BR11 of section 8 are the architecture constraints of this service
    When the build runs the guardrail and boundary tests
    Then each rule passes its covering test and the build fails when one does not

  Scenario: AC13 A consumed activity is retried or times out (new, D-RCV-60)
    Given a consumed activity call times out or is retried by the workflow
    When the step calls the activity again
    Then the retry follows the workflow's own schedule, the timed-out activity writes nothing and the same Idempotency-Key answers the item that exists

  Scenario: AC14 A consumed call fails or does not answer (new, D-RCV-60)
    Given rwb-source-data, rwb-case or rwb-decision fails or does not answer
    When the step calls it
    Then nothing is written, no move is answered and the caller sees 503 with the platform error envelope

  Scenario: AC15 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case is at a state from which the requested status change is not a rule row of section 8
    When the run requests the change
    Then the request is refused with 409, nothing is written for that case and the case state does not change
```

The criterion is the legacy criterion of RWB-E6-008, word for word, with its origin tag added and nothing else changed: the legacy wording of "the decision log cannot be written" is read as "the decision record cannot be written", "the action is taken", "nothing changes" and "the user sees MSG-P7-003" all stand. The single leading `Given` is the only addition, and it names the cross-service part the criterion leaves open — the posting item of rwb-integration, which is the only other service the action touches at its exit. AC1 (the derecognition, the posting and the record with the rule version), AC2 (R-DS-31) and AC3 (R-DS-33) belong to RWB-ITG-E6008-ITG by the split the plan fixes and are asserted there as the cross-service journey; this story supplies the two steps that journey drives, and their component proof is TC-E6-008-01 to TC-E6-008-03 in section 16. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_debtsale`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer | BR ID |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-29 | Debt sale | D8.4 | SETTLED | DATA_TRANSFER_RUN | Any | Transfer the account data to the buyer | DATA_TRANSFERRED | Workbench | buyer portal | 5 working days | BR12 |
| R-DS-30 | Debt sale | D8.4 | DATA_TRANSFERRED | DERECOGNITION_RUN | Any | Derecognise the balance on the account | DERECOGNISED | Workbench | ALS core and GL | None | BR13 |
| R-DS-31 | Debt sale | D8.4 | DERECOGNISED | GL_POSTING_RUN | Any | Post to the general ledger and send the provision input to Finance | GL_POSTED | Credit Administration | ALS core and GL, Finance provision feed | month-end close | BR14 |
| R-DS-32 | Debt sale | D8.4 | DERECOGNISED | POSTING_REJECTED | ALS or the general ledger rejects the posting | Hold the posting and raise an exception task | POSTING_REJECTED_DS | Credit Administration | integration adapters | 2 working days | BR15 |
| R-DS-33 | Debt sale | D8.4 | POSTING_REJECTED_DS | POSTING_CORRECTED | the rejection cause is cleared | Re-post to ALS and the general ledger | GL_POSTED | Credit Administration | ALS core and GL | None | BR16 |

The five rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target "ALS core and GL" is the ledger interface of rwb-integration (P2), "Finance provision feed" is a second item on the same interface, "integration adapters" is rwb-integration, "buyer portal" is the partner route of the transfer story and "Workbench" is this service. R-DS-29 is tabled only because it produces the state this step starts from; it belongs to RWB-S6-E6007-APP. Derecognition is recorded as this service's decision (R-DS-30); the posting file is built and sent as items on rwb-integration's outbound interface, and the posted position is read back through the data path; no direct ALS or general ledger interface is opened here (GAP-1779).

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The book, the general ledger and the Finance provision feed are reached only as items on rwb-integration's outbound interface; this service writes no ALS row, no ledger entry and no provision file | R-DS-30 to R-DS-33 (Systems column); ASM-4963 | TC-E6-008-14 |
| BR2 | The decision is recorded before anything leaves, with the rule ID and the package version in force; a failed write changes nothing, sends no item and answers no move, and the caller sees MSG-P7-003 | DP-03; TSD S6 T2; legacy AC4 | AC4, TC-E6-008-04, TC-E6-008-06 |
| BR3 | The account, balance and ALS facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the facts on the owner's contract with the as-of date | DP-05 as the owner's contract; FSD S6 A2.12.2; ASM-4961 | TC-E6-008-12 |
| BR4 | The case move is answered and not written: `recovery_case` and the states `DERECOGNISED`, `GL_POSTED` and `POSTING_REJECTED_DS` are rwb-case's | ASM-4961; TSD S6 T4 | TC-E6-008-12 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_debtsale`; the account identifier and `lot_id` are identifiers of other services' facts | DP-01; TSD S6 T3.3 | TC-E6-008-12 |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: the entry set, the chart of accounts, the provision layout, the result codes, the posting window and `LOV-LOT-STATUS`, `LOV-SEGMENT`, `LOV-BUYER-CLASS` and `LOV-PUTBACK` | TSD S6 T3.2; FSD S6 BR-S6-012; legacy Guardrails | TC-E6-008-13 |
| BR7 | One posting item set per lot and business date: a rejection is held at `POSTING_REJECTED_DS` under R-DS-32 and only a cleared cause produces the re-post of R-DS-33 | R-DS-32; R-DS-33 | AC8, TC-E6-008-10, TC-E6-008-11 |
| BR8 | The posting result and its references are held in the decision record and in the case state, because no column of this service's tables carries them; this story adds no column | GAP-3006; ASM-4965 | TC-E6-008-14 |
| BR9 | The month-end close of R-DS-31 is a durable timer of `DebtSaleWorkflow` and not a Schedule; the service owns no job row | R-DS-31 (Timer column); context pack, jobs 0; ASM-4966 | TC-E6-008-15 |
| BR10 | No person name, address, contact value or identity number enters `rwb_debtsale`, the decision record, an item manifest, a log or a workflow input; `borrower_code` is a code and not an identity | Template and Rules §R7.2 (s17); TSD S6 T6.2 | TC-E6-008-16 |
| BR11 | The same lot, business date and package version twice, or the same `Idempotency-Key` twice, produces one record, one item set and one answer per case | TSD S6 T-A.2; R-UNI-40 | AC9, TC-E6-008-11 |
| BR12 | The account is transferred to the buyer under R-DS-29, the state this step starts from | R-DS-29 (rule table, BR ID column) | RWB-S6-E6007-APP (precondition, not this story) |
| BR13 | The derecognition under R-DS-30 is this service's decision, recorded before anything leaves | R-DS-30 (rule table, BR ID column) | TC-E6-008-01, TC-E6-008-02 |
| BR14 | The posting under R-DS-31, with the provision input, is sent as items on rwb-integration's outbound interface | R-DS-31 (rule table, BR ID column) | TC-E6-008-02, TC-E6-008-03 |
| BR15 | A rejected posting is held at `POSTING_REJECTED_DS` with the rejection code and the exception task | R-DS-32 (rule table, BR ID column) | AC8, TC-E6-008-10 |
| BR16 | A cleared rejection cause produces the re-post under R-DS-33 | R-DS-33 (rule table, BR ID column) | AC8, TC-E6-008-10 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the state of its two steps and the posting item.

| From (case route state) | Event | Condition | To | Rule |
|---|---|---|---|---|
| DATA_TRANSFERRED | DERECOGNITION_RUN | Any | DERECOGNISED | R-DS-30 |
| DERECOGNISED | GL_POSTING_RUN | Any | GL_POSTED | R-DS-31 |
| DERECOGNISED | POSTING_REJECTED | ALS or the general ledger rejects the posting | POSTING_REJECTED_DS | R-DS-32 |
| POSTING_REJECTED_DS | POSTING_CORRECTED | the rejection cause is cleared | GL_POSTED | R-DS-33 |
| GL_POSTED | CLAIM_WINDOW_CLOSED | no put-back claim inside the claim window | LOT_CLOSED | R-DS-34, RWB-S6-E6009-APP |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The transfer of the lot completes | The package in force is read | Derecognising |
| Derecognising | R-DS-30 fires on the accounts of the lot | The record is written | Posting |
| Posting | R-DS-31 fires at the month-end close and the items are accepted | The record with the item references is written | Waiting for the next lot |
| Posting | An item is rejected | R-DS-32 | Held at `POSTING_REJECTED_DS`, exception task open |
| Held | The rejection cause is cleared | R-DS-33 | Posting, one new item |
| Derecognising or Posting | The record write, the item or a consumed read fails | X1, X5 | Waiting, nothing changed |

The route states are those of the DEBTSALE machine of TSD S6 T4 and live on the case of record. The lot status of `LOV-LOT-STATUS` stays `TRANSFERRED` through this step: `CLOSED` is written by the put-back and lot-closure story (R-DS-34 to R-DS-39).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-debtsale service identity, login on schema `rwb_debtsale` (DP-02) | Runs the derecognition and the posting under the service identity with no officer task on the happy path; holds the primary use of the feature (FSD S6 A2.12.3.3 "None; runs unattended") |
| Credit Administration officer, RW-CREDITAD | Debt sale R in TSD S6 T6.1: reads the lot, its accounts and the posting state on SCR-26, and works the exception task of R-DS-32; the also-user of FSD S6 A2.12.3.3 |
| RW-DEBTSALE, debt sale officer | Debt sale CRUA: reads the lot and its posting state in scope; the run itself is not theirs |
| RW-PRODHEAD and RW-HEADASL | Debt sale RA: read the posting state inside their scope |
| RW-SALEOFF, RW-NPAMGR, RW-WRITEOFF, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Debt sale R: read only, in scope |
| PT-BUYER, PT-RAMC | No right in this step: the buyer sees the transferred lot in the data room, never the posting |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the matrix gives it: the service identities run the step and are subject to the same checks |

The rights are the rows of TSD S6 T6.1 and nothing wider. R-DS-31 and R-DS-33 name "Credit Administration" in their owner column, which is the business owner of the decision and not an operator right: the matrix gives RW-CREDITAD R only, so the re-post of R-DS-33 runs unattended when the corrected cause arrives and the officer works the exception task and reads the outcome (ASM-4964). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation by the service template, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 to DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | the lot, its number, its cut-off date, its segment, its reserve, its buyer, its buyer class, its signing date, its authority, its terms and its `status` | Read: no column changes at this step; `status` stays `TRANSFERRED` and `CLOSED` is RWB-S6-E6009-APP's |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | the account of the lot, its lot, its account reference, its borrower code, its outstanding, its selling price and its `put_back_status` | Read: the accounts of the lot and their balance at the cut-off; no column changes here |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | the rule ID, the package version, the inputs reference, the item reference, the result code, the outcome and the decided-at time | Write through the local library, before anything leaves |
| Standard columns | both tables (S6, `rwb_debtsale`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Read; the optimistic lock is not taken because no column changes |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` (P1) | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and the rest | Not read as a view and not written: the facts arrive on rwb-source-data's contract with the as-of date |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the state arrives on the rwb-case contract and the move is answered |
| DF-INT-001 to DF-INT-013 | interaction (P1, interaction ledger) | id, case_id, person_key, occurred_at, channel, direction and 7 more | Not used by this step: the ledger is rwb-source-data's and this step records its own decision |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the package arrives on rwb-decision's contract |
| DF-DEC ledger | decision_log_entry (P7) | the central ledger entry | Not written here: the local record is this service's and the library relays it |

Field IDs are those of TSD S6 T3.1 and the Logical Data Model and Data Dictionary, and the ACE, case and ledger rows are the rows the legacy Data table lists, with their owners changed to P1, P3 and P7 by the target. **No new table, no new column and no migration**: the two tables arrive with the DB story of this service, and this story writes no business column of either — its state is the record, the item and the case move. The missing posting reference, result code and rejection reason columns are recorded (GAP-3006; ASM-4965). The decision record, `idempotency_key` and `outbox_event` are library objects created in `rwb_debtsale` by the library's migration (DP-03); this step writes no outbox row because it publishes no event (§12.3).

**No personal data.** The records and the item manifests carry references, codes, amounts, dates, list values, a result code and a rule version. No name, address, contact value or identity number enters `rwb_debtsale`, a record, a manifest, a log or a workflow input, and every fixture is synthetic. `primary_person_key` is P3's and is never copied here; `borrower_code` is a code of the source system. Data Classification v5 classes `primary_person_key` as an indirect identifier (DF-CAS-004), so it is named here only as P3's field and is not carried.

### 12. Contract

#### 12.1 REST operations provided

None of its own. The derecognition and the posting run unattended as steps of `DebtSaleWorkflow`, and TSD S6 appendix T-A publishes no derecognition or posting operation: its five operations are API-S6-001 `POST /debt-sale-lots`, API-S6-002 `GET /debt-sale-lots/{lotId}`, API-S6-003 `POST /debt-sale-lots/{lotId}/award`, API-S6-004 `GET /partner/data-room/{lotId}` and API-S6-005 `POST /partner/data-room/{lotId}/bids`. The two endpoint rows of the legacy story are API-S6-001 and API-S6-002, whose shapes are the lot builder's and the data room's (RWB-S6-E5024-APP, RWB-S6-E5026-APP); this story adds no operation and redefines neither. The posting state is read from the case state of rwb-case and from the lot read of this service behind the composite route (§15). The absence is recorded as GAP-3006 with ASM-4964.

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use |
|---|---|---|---|
| The account and balance read (operation name Not specified in the source documents (GAP-3006; ASM-4961)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The accounts of the transferred lot with their status, contract, balance and outstanding, and the as-of date of the product; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its route state and its lot link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3006; ASM-4961)) | rwb-case (P3) | P3 rwb-case | The moves `DERECOGNISED`, `GL_POSTED` and `POSTING_REJECTED_DS` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent applies; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEBTSALE package at its version with R-DS-29 to R-DS-33; faked |
| The outbound posting item (activity name Not specified in the source documents (GAP-3006; ASM-4960)) | `rwb-integration` (P2), activity on queue `rwb-integration` | P2 rwb-integration | The ALS balance-removal item, the general ledger entry item and the Finance provision input; the item reference and the result code back; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four reads and the interface call are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3006; ASM-4960).

#### 12.3 Events published

None. The service publishes on `rwb.debtsale.events.v1`, and the catalogue holds one event of this service, `LotAwarded` (EV-23, payload `lotId`, `buyerId`, `price`), which is RWB-S6-E6005-APP's, with `AccountsTransferred` beside it in the service's event set and RWB-S6-E6007-APP's. No posting-result or derecognition event exists in the catalogue, so this story declares no event, no producer group and no outbox row of its own, and a build that publishes one fails the absence test. The local decision record travels on the shared `rwb.decision-record.v1` through the library of RWB-PLT-E1027-CON, not through this story's topic (ASM-4962).

#### 12.4 Events consumed

None. Architecture v5 slide 19 gives rwb-debtsale the event `ProceedsMatched` (EV-25), which is the settlement and remittance story's (RWB-S6-E6011-APP) and not this one: the derecognition starts from the transfer of the lot and the posting from the month-end timer of the rule. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test (ASM-4962).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow`, a saga whose pivot is the transfer and which continues-as-new across the settlement, posting and put-back window | `rwb-debtsale` | Input: the lot, the cut-off date, the case set and the package in force; this step sits after the pivot, so no compensation is declared for it |
| `derecogniseAccounts` | Activity, the R-DS-30 step | `rwb-debtsale` | The lot, its accounts and the balance in; the rule ID, the package version, the record id, the `DERECOGNISED` move and the account set out |
| `postToLedger` | Activity, the R-DS-31, R-DS-32 and R-DS-33 step | `rwb-debtsale` | The account set, the amounts, the business date and the items in; the item references, the result codes, the record id and the `GL_POSTED` or `POSTING_REJECTED_DS` move out |
| The outbound item call (name Not specified in the source documents (GAP-3006; ASM-4960)) | Activity provided by rwb-integration, called as a task | `rwb-integration` | The manifest of section 4 step 7 in; the item reference and the result code out |

No child workflow for the case and none for the money exists in this service. The start rule of `DebtSaleWorkflow` is the catalog's: the monthly sale cycle opens, or a residual arrives from disposal (R-DS-01). Its workflow ID form and its duplicate-start policy are Not specified in the source documents (CG-ALL-10656). The account and balance facts are read only on rwb-source-data's contract, with the source field names carried from the FSD (v_ace_score.*, v_ace_account.*, v_ace_batch_status.*); no view and no ACE table is read here, and the path to P1 (REST for the screen, activity inside the workflow) is confirmed before the wave 3 system test. The activity names are target design choices fixed by no source document; the retry is 1 s initial interval, back-off 2, 10 attempts, and a rule that is not in force is non-retryable.

#### 12.6 Schedules

None. R-DS-31 carries "month-end close" in its timer column and the service owns no job row (context pack, jobs 0), so the wait is a durable timer inside `DebtSaleWorkflow` on `rwb-debtsale` and not a Temporal Schedule. No Quartz row, no shared job table and no batch table is declared or moved here (ASM-4966).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot and its accounts; read at this step; `status` stays `TRANSFERRED` |
| debt_sale_account | S6 (`rwb_debtsale`) | An account in a lot; read at this step; no column changes |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked record of each rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the lot, the business date and each item |
| outbox_event | PLT library, created in `rwb_debtsale` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `v_ace_account` and every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), `interface_config` and `outbound_item` (P2), and the ALS and general ledger tables. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data account and balance fake | The accounts of lot `LOT-2026-000042` with their status, contract, total balance and outstanding, as-of `2026-12-31`; a stale product with its date; no answer beyond 2 s | TC-E6-008-01, X4, X5 |
| rwb-case state and move fake | Cases `RC-2026-000842` and its siblings at `DATA_TRANSFERRED`; an accepted move and a refused move for each of `DERECOGNISED`, `GL_POSTED` and `POSTING_REJECTED_DS` | TC-E6-008-01, TC-E6-008-02, X3 |
| rwb-decision rule-package fake | The DEBTSALE package at its version in force with R-DS-29 to R-DS-33 | TC-E6-008-02, TC-E6-008-03 |
| rwb-integration outbound-interface fake | One ALS item and one general ledger item accepted with a reference; one item rejected by ALS; one item rejected by the general ledger; one manifest refused; no answer beyond 2 s | TC-E6-008-01, TC-E6-008-03, X6, X9 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, TC-E6-008-04, TC-E6-008-06 |
| Authorise stub of the service template | Right R held and not held | TC-E6-008-05 |
| gateway-bff composite route fake | The merged SCR-26 answer for lot `LOT-2026-000042`: the lot, its accounts and the case state | TC-E6-008-01 |

The fakes are test-only and are replaced by the real services in SIT. The four operation names and the interface values carry the placeholder until their owners confirm them (GAP-3006; ASM-4960, ASM-4963).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 3 consumed | The rwb-source-data account read, the rwb-case state read and the case-move answer, the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` and `AccountsTransferred` are sibling stories' and `ProceedsMatched` is the remittance story's |
| Temporal | 1 workflow and 2 activities, plus 1 activity of rwb-integration | `DebtSaleWorkflow`, `derecogniseAccounts` and `postToLedger` on `rwb-debtsale`; the outbound item on `rwb-integration`; no Schedule |
| File | None built by this story | The ALS and ledger interface is a file run of rwb-integration's interface row; this story delivers a manifest |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.debtsale`, module `derecognition`; front end `src/modules/recovery/debtsale/Award.tsx`, the fragment SCR-26 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of both steps: the record and the item commit together or not at all. DP-05 is applied as the owner's contract, because this service holds no `v_ace_*` grant. DP-13 fixes the base of the service and this story adds no operation of its own to it. DP-19 is how SCR-26 reaches this service and the case state, one hop through the gateway. The two H rows of the table are the ones the metadata carries, and no DP row of this key adds a contract dependency: the four reads and the interface call are class C in fact while the plan's C row is None (GAP-3006; ASM-4960). The posting and the re-post run under the service identity; the R-DS-32 exception task is read and worked by the Credit Administration role of R-DS-32; the month-end close is a durable timer of `DebtSaleWorkflow` with no Schedule.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` derecognition branch | Workflow | Waits for the transfer, reads the package in force, runs the two steps and reports the outcome to the parent |
| `derecogniseAccounts` | Activity | Reads the accounts, evaluates R-DS-30, writes the record and answers the move |
| `postToLedger` | Activity | Builds and sends the items, evaluates R-DS-31 to R-DS-33, writes the record and answers the move |
| `DerecognitionEvaluator` | Service | The rule evaluation over the package in force, with the account set, the balance and the no-fire path |
| `PostingItemBuilder` | Service | The ALS item, the general ledger item and the provision input, from data and never from a constant |
| `PostingSender` | Client | The outbound call of rwb-integration as a task, with the manifest, the key, the item reference and the result code |
| `TransferredAccountReader` | Client | The account and balance read of rwb-source-data with the as-of date and the stale path |
| `RulePackageClient` | Client | The package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The `DERECOGNISED`, `GL_POSTED` and `POSTING_REJECTED_DS` answers to rwb-case |
| `DebtSaleDecisionRecordWriter` | Library adapter | The record with the rule ID, the version, the item references and the result codes, written before anything leaves |
| `Award` | React component | Shows the lot, its accounts and the posting state on SCR-26, read only, with the refused, rejected and stale readings |

**Database and migrations.** Schemas: this service owns `rwb_debtsale` only; `rwb_case`, `rwb_decision` and `rwb_source_data` belong to rwb-case, rwb-decision and rwb-source-data and are reached only through their contracts. No Flyway file. The two tables arrive with the DB story of this service, and the record, the idempotency key and the outbox are library objects created in `rwb_debtsale` by the library's migration (DP-03). No column is added for the posting reference, the result code or the rejection reason: those are recorded in the decision record (BR8; ASM-4965).

**Configuration and reference data.**

- `LOV-LOT-STATUS`, `LOV-SEGMENT`, `LOV-BUYER-CLASS` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The entry set, the chart-of-accounts reference, the provision layout, the result codes and the retry schedule: rows of rwb-integration's interface configuration and of the ledger, read per item (GAP-3006; ASM-4963).
- The rules R-DS-29 to R-DS-33 and the month-end close: rule rows of the package with their version, never written in code.
- The capability area "Debt sale" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.
- Parameters read: the LOV names above and the interface-configuration and retry keys, whose parameter-catalog keys are Not specified in the source documents (DOR-RWB-S6-E6008-APP-20); reference data is read on the owners' contracts of DP-06 and DP-07.

**Build steps**

1. The derecognition branch of `DebtSaleWorkflow` and its input record, registered on `rwb-debtsale`, with the transfer as its trigger.
2. `TransferredAccountReader` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker, the as-of date and the stale path.
3. `DerecognitionEvaluator` and the `DERECOGNISED` answer, one per account of the lot.
4. `PostingItemBuilder` with the three items from the interface rows, and `PostingSender` with the manifest, the key and the result code.
5. `DebtSaleDecisionRecordWriter` against the stub, in the same transaction as the item, with the failed-write path (AC4, X1).
6. The R-DS-31 posting, the R-DS-32 hold with the exception task, the R-DS-33 re-post and the three case moves (X3, X6).
7. The repeat guard on the lot, the business date and the key (X7), and the interface-configuration read (X9).
8. SCR-26 through the composite route fake, and the boundary test: no statement outside `rwb_debtsale`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_source_data` (X8).

**Test fixtures.** The harness environment and its base hosts, the ALS and GL answer shape, the posting reference format, the rejection codes, the retry and back-off settings of the resend operation, the evidence format and retention, the pass or fail gate and the synthetic lot, account and case keys are agreed with the ACE integration path owners at the wave 4 entry check and held as fixtures; until then they are Not specified in the source documents (GAP-0454).

**Feature flag.** `rwb.debtsale.derecognition-v1`, a flag of the platform library; off means the step holds the lot after its transfer, writes nothing and sends no item, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, a SIT run derecognises a transferred lot, posts to ALS, the general ledger and the provision feed once, holds a rejected posting at `POSTING_REJECTED_DS` and re-posts it after the correction, a forced record failure changes nothing and sends no item, a repeated trigger writes once, and no `recovery_case` row and no `v_ace_*` read exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key; it names an open deviation on an account, which is the eligibility story's, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of an item manifest is absent or invalid, or an interface row is not in force at the business date (X9) | Enter {field}. |
| MSG-P4-002 | A role without the Debt sale right reads the lot or its posting state (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything leaves (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The account or balance product is stale after a late or failed ACE batch (X4, VR-S6-012-1) | {product} is from {date}. Today's load has not arrived. |
| Not specified in the source documents (DOR-RWB-S6-E6008-APP-9) | ALS or the general ledger rejects an item; the message is rwb-integration's row and is read from its exception queue (X6) | Not specified in the source documents (GAP-3006; ASM-4963) |

The five named IDs are those of the legacy message set and of FSD S6 A2.12.3.1, and their text is the legacy and FSD wording, copied unchanged, except MSG-P1-001, whose text is that of the Error and Message Standard v4; no message is reworded and no new one is invented. The rejection message is rwb-integration's and takes no ID here (DOR-RWB-S6-E6008-APP-9); it is read from that service's queue.

### 15. Screens and states

SCR-26 Award, in its transferred, posted and rejected readings, is served through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot and its accounts, rwb-case for the case and its route state and rwb-source-data for the balance and its as-of date; this story fixes the rwb-debtsale answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

| State of SCR-26 | What it shows | Where it comes from |
|---|---|---|
| Transferred | The lot, its accounts and the transfer date, awaiting the derecognition | The lot of this service; `DATA_TRANSFERRED` of rwb-case |
| Derecognised | The accounts removed from the book, with the rule ID and version of the record | The record of this service; `DERECOGNISED` of rwb-case |
| Posted | The item references and the result codes of ALS, the general ledger and the provision input | The record of this service; `GL_POSTED` of rwb-case |
| Rejected and held | The rejection code and the two-working-day exception task of R-DS-32 | The record and the item of rwb-integration; `POSTING_REJECTED_DS` of rwb-case |
| Refused, not recorded, stale data | The messages of section 14 | This service |
| Empty, loading, error, no access | Not specified in the source documents (CG-ALL-10667) | Not specified in the source documents (CG-ALL-10667) |

The legacy screen table gives SCR-25 Lot builder and SCR-26 Award with the states "Draft; priced; approved" and "Open; closed; awarded; transferred"; the first four belong to the earlier stories of the module and this story fixes only the readings a posting produces on SCR-26. PRT-05 Data room is the data room story's and reads nothing from this step.
SCR-25 states of empty, loading, error and no access are not in the screen specification and are Not specified in the source documents (CG-ALL-10666).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-008-01 | run by RWB-ITG-E6008-ITG (AC1); component check of the derecognition and the posting (R-DS-30, R-DS-31); the cross-service criterion is RWB-ITG-E6008-ITG's | Component | Lot `LOT-2026-000042` transferred with 12 accounts; the account and balance fake as-of `2026-12-31`; the ALS and general ledger items accepted with a reference; the record asserted |
| TC-E6-008-02 | run by RWB-ITG-E6008-ITG (AC2); component check of R-DS-31: the posting run moves the case to `GL_POSTED` and sends the provision input; the cross-service criterion is RWB-ITG-E6008-ITG's | Component | Case `RC-2026-000842` at `DERECOGNISED`; the package in force; the move `GL_POSTED` asserted on the fake |
| TC-E6-008-03 | run by RWB-ITG-E6008-ITG (AC3); component check of R-DS-33: a held posting is re-posted once the cause is cleared; the cross-service criterion is RWB-ITG-E6008-ITG's | Component | The item rejected by ALS with its result code, then a corrected item accepted; one record per attempt, the re-post naming R-DS-33 |
| TC-E6-008-04 | AC4: the record cannot be written, so nothing changes and the user sees MSG-P7-003 | Component | The record stub stopped; no item, no reference, no move |
| TC-E6-008-05 | Access: a role without the right is refused with MSG-P4-002 | Component | A caller without Debt sale R on the lot read; no read and no record |
| TC-E6-008-26 | AC5: the 403 comes before any read and nothing is written when the Debt sale right is absent | Component | Role without the right; 403 before the read; no record written |
| TC-E6-008-27 | AC6: a stale account or balance product holds the step and shows MSG-P1-001 | Component | Stale answer from the owner's contract; nothing written, no item sent, no move |
| TC-E6-008-09 | AC7: a dependency that does not answer inside 2 s gives 503 and no move | Component | Dependency slower than 2 s or breaker open; retry on schedule; platform error envelope |
| TC-E6-008-10 | AC8 and R-DS-33: a rejected posting is held and re-posted once the cause is cleared | Component | Rejection from the rwb-integration fake; hold at POSTING_REJECTED_DS, rejection code recorded, no further item; re-post after the cleared cause |
| TC-E6-008-11 | AC9: a repeated lot, business date and package version, or a repeated Idempotency-Key, writes once | Component | Same trigger and same key sent twice; one record, one item set, one answer per case |
| TC-E6-008-12 | AC10: a statement reaching a `v_ace_*` view, a `recovery_case` row or another service's schema fails the build | Component | Boundary test with the grant refusal; build fails and nothing is released |
| TC-E6-008-13 | AC11: a changed or absent interface row gives the next version or no item | Component | Interface row changed after the last item; no row in force at the business date |
| TC-E6-008-14 | BR1 and BR8: items only on the outbound interface; the posting result read from the record and the case state | Component | Posting fake; no ALS row, ledger entry or provision file written; result and reference read back |
| TC-E6-008-15 | BR9: the month-end close is a durable timer of DebtSaleWorkflow with no Schedule | Component | Workflow run; close fires as a timer; no job row exists |
| TC-E6-008-16 | BR10: no personal data enters the service's stores, record, manifest, log or workflow input | Component | Synthetic fixtures; scan of the stores, manifest, log and workflow input |
| TC-E6-008-06 | Principle 5: a forced decision record write failure stops the action with MSG-P7-003 and sends no item | NFR | The record store stopped during the posting of a business date; the run is repeated after recovery and writes once |
| TC-E6-008-07 | Contract: the operations of section 12.2 and the activities of section 12.5 match their contract rows | Contract | The contract fakes of rwb-source-data, rwb-case and rwb-integration; each operation and activity called with its inputs, outputs asserted against the contract |
| TC-E6-008-08 | Boundary: the tables of section 12.7 are read or written only as stated, with no column changed and no foreign key (ASM-3438) | Component | The lot and account tables read at this step with `status` staying `TRANSFERRED`; the library objects present in `rwb_debtsale`; no ACE view read |
| TC-E6-008-17 | AC12: the architecture rules BR1 to BR11 of section 8 are proved by the guardrail and boundary tests | Component | Guardrail and boundary test suite of rwb_debtsale; each rule's covering test run; the build fails on a failing rule |
| TC-E6-008-18 | AC13: a retried or timed-out activity writes nothing and follows the workflow's own schedule | Component | Activity timed out on the fake; retry on the workflow's own schedule; retry count Not specified in the source documents (NEWAC-RWB-S6-E6008-APP-AC13) |
| TC-E6-008-19 | AC14: a failed or unanswered consumed call writes nothing, answers no move and gives 503 | Component | Failed or silent answer from the rwb-source-data, rwb-case or rwb-decision fake; no write; no move; 503 with the platform error envelope |
| TC-E6-008-20 | AC15: a status change the model does not allow is refused with 409 | Component | Case at SETTLED offered DERECOGNITION_RUN, which has no rule row for that state in section 8; 409; nothing written |

The six legacy cases are those of RWB-E6-008 in their legacy order, with the Level column added: every case is proved on the fakes, so every case is `Component`, except the forced-failure case which is `NFR`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. No `-ITG` copy is written by this story: the cross-service journey of AC1 to AC3 belongs to RWB-ITG-E6008-ITG, and its copies carry the `-ITG` suffix there.

### 17. Guardrails

- No business value in code: the entry set, the chart-of-accounts reference, the provision layout, the result codes, the posting window, the lists and the rule rows stay data, reference data or the interface configuration, never a constant, a default or a branch.
- No personal data in a record, an item manifest, a workflow input or a log: references, codes, amounts, dates, a result code and a rule version only, `borrower_code` is a code, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR3).
- Nothing leaves except through rwb-integration: no direct ALS write, no direct ledger entry, no provision file and no second interface (BR1).
- The case stays with rwb-case: no `recovery_case` row, no case route-state column and no case write here (BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- The record precedes the item and both or neither; a build that sends an item outside the record's transaction fails the review (DP-03; BR2).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `v_ace_account` view read.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying (FSD S6 Requirements served, E6); the split plan carries no requirement id for this slice (GAP-3006) | The two steps, the items and the case moves | TC-E6-008-01, TC-E6-008-02, TC-E6-008-03 | FEAT-DBS-12 | Not specified in the source documents (DOR-RWB-S6-E6008-APP-2) |
| FEAT-DBS-12 | Derecognize and post to the general ledger, System, runs unattended, systems ALS and GL, depends on FEAT-DBS-11 (Epics 3 to 8 Specification v3) | The whole slice | All | FEAT-DBS-12 | Not specified in the source documents (DOR-RWB-S6-E6008-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the lot and the step | TC-E6-008-01 | FEAT-DBS-12 | Not specified in the source documents (DOR-RWB-S6-E6008-APP-2) |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E6-008-01 | FEAT-DBS-12 | Not specified in the source documents (DOR-RWB-S6-E6008-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E6-008-01, TC-E6-008-02 | FEAT-DBS-12 | Not specified in the source documents (DOR-RWB-S6-E6008-APP-2) |
| ADR-022 | Local decision record plus central ledger | The record written before anything leaves | TC-E6-008-04, TC-E6-008-06 | FEAT-DBS-12 | Not specified in the source documents (DOR-RWB-S6-E6008-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-008, disposition Split (rework); feature FEAT-DBS-12; module S6 Debt sale; release 30 April 2027 (tentative) |
| Legacy criteria | AC4 owned word for word by this story; AC1, AC2 and AC3 owned by RWB-ITG-E6008-ITG |
| Source text | Legacy RWB-E6-008; FSD S6 Debt sale v3 A2.12; TSD S6 Debt sale v2 T3, T4, T6 and T-A; Business Rules and Routing Logic v4 rows R-DS-29 to R-DS-33; Event and Messaging Design v5 EV-23 |
| Test cases | TC-E6-008-01 to TC-E6-008-27 |
| Feature and screens | FEAT-DBS-12, SCR-26 Award |
| Rules | R-DS-30, R-DS-31, R-DS-32 and R-DS-33, with R-DS-29 as their precondition, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the elements, the lists, the consumed rows, the posting item and its result set, the rights, the error envelope and the fakes: RWB-S6-E6008-CON.
- The data transfer of R-DS-29, the masked tape and `AccountsTransferred`: RWB-S6-E6007-APP and the tape story of this service.
- The award, the price test, the settlement term, the confirmation of the buyer remittance and `ProceedsMatched`: RWB-S6-E6005-APP and RWB-S6-E6011-APP.
- The put-back claim, the reversal of the derecognition, the lot closure of R-DS-34 to R-DS-39 and the closing of the case: RWB-S6-E6009-APP and RWB-S6-E6010-APP.
- The ledger interface itself — its identifier, transport, file layout, result codes, retry schedule, exception queue and resend — and the ALS and Finance feeds: rwb-integration (P2).
- The accounting rules of ALS and of the general ledger, the chart of accounts and the entry set: the ledger and Finance.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The account, balance and ALS facts and the freshness of the data product: rwb-source-data (P1).
- The DEBTSALE package, its rule rows and its versions, and the central decision ledger: rwb-decision (P7).
- The rights, the scopes and the masking: rwb-access (P4) and the guard of the service template.
- The composite route and the field list of SCR-26: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence, with the `-ITG` copies of the six cases: RWB-ITG-E6008-ITG.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
