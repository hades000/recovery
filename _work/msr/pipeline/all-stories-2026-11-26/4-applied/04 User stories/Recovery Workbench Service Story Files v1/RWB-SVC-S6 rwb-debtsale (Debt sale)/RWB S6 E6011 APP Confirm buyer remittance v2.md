# RWB-S6-E6011-APP Confirm buyer remittance

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S6-O |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E6011-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E6-011 split out for rwb-debtsale. The four legacy acceptance criteria are kept word for word with their origin tag; the remittance becomes one step of `DebtSaleWorkflow` on task queue `rwb-debtsale`, which consumes the matched proceeds of rwb-payment, evaluates R-DS-25, R-DS-26 and R-DS-27 on the settlement term of the lot, reads the ACE payment and score facts through the rwb-source-data contract (DP-05), records the outcome through the local decision-record library before anything changes (DP-03), answers rwb-case for the moves to `SETTLED` and `AWARD_CANCELED_DS` and serves the settlement element on `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19). TSD S6 appendix T-A publishes no remittance or settlement operation; the two legacy endpoint rows, the award path and the data room read, belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP, and the derecognition, GL posting and data transfer belong to the sibling stories of FEAT-DBS-12 and FEAT-DBS-11. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E6011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **Credit Administration officer**, I want **the Workbench to match the buyer's payment to the award and close the money side of the lot**, so that **debt sales run on approved lots and masked data**.

This is the application slice of legacy RWB-E6-011, the FEAT-DBS-15 step of the S6 Debt sale module. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- the settle-and-cancel step of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slide 19, "TMP DebtSaleWorkflow (saga, pivot = transfer)"; Temporal and Drools Design slide 13);
- the evaluation of R-DS-25 on the matched proceeds, of R-DS-26 on a recorded cancellation and of R-DS-27 on an absent payment once the settlement term has run, with the Debt sale route set and its package version in force;
- the settlement element of the lot: the awarded lot, the buyer reference, the matched amount, the payment date, the settlement state, the rule ID with its version and the decided-at time, read from the ACE payment facts of rwb-source-data (DP-05) and from the lot's own `payment_terms` (DF-SAL-029);
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before any change (DP-03), which is what legacy AC1 and AC4 test;
- the release of the data transfer under R-DS-25, handed to the transfer step of the saga as its starting signal, and the answer to rwb-case for the case moves `SETTLED` and `AWARD_CANCELED_DS`, with the rule ID and the version that produced each move;
- the closed state of SCR-26 Award, served read only on `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19).

It does not own: the published shape of the settlement element, the consumed rows, the error set and the fakes, which are RWB-S6-E6011-CON; the award operation API-S6-003 `POST /debt-sale-lots/{lotId}/award`, which is RWB-S6-E6005-APP's; the data room read API-S6-004 `GET /partner/data-room/{lotId}`, which is RWB-S6-E5026-APP's; the derecognition of the sold accounts and the posting to ALS and the general ledger of FEAT-DBS-12, which is the sibling story of this legacy key's prerequisite; the transfer of the account data to the buyer of R-DS-29 and FEAT-DBS-11, which is the transfer story of this service; the put-back claim of FEAT-DBS-13; the payment matching and the posting of the proceeds, which are rwb-payment's (P8); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the central decision ledger and the rule rows, which are rwb-decision's (P7); the capability area and the rights, which are rwb-access's (P4); the buyer scorecard, which is rwb-partner's (S9); the ACE views, which are read only by rwb-source-data (P1); the sale documents and the customer notices, which are rwb-document's (P5) and rwb-comms's (P6); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-011 gave the Workbench one step that matched the buyer's payment to the award and closed the money side of the lot, and the FSD keeps the objective and the metric unchanged: the debt sale turnaround is measured on the decision log and the Workbench records, reviewed monthly, with a 45-day target (FSD S6 A2.15.1). The program keeps the requirement as REQ-S6-008, "Data transfer, derecognition and the general ledger posting follow the award without re-keying", owned by Credit Administration (Business Requirements Program v5).

What D-RCV-60 changes is who owns each fact the step stands on. In the monolith the payment row, the case state, the lot, the decision log and the score sat in one `recovery` schema and one process. In the target:

- **the money is rwb-payment's (P8).** Event 25 `ProceedsMatched` is published by Payments and posting with `proceedsId`, `caseId` and `amount` (Event and Messaging Design v5; Architecture v5 slide 19 IN), and the connection matrix puts an event subscription from S6 to P8. This story consumes that event and evaluates the rule; it matches no payment itself, and the connection matrix's Temporal edge from S6 to P8 carries the saga's post-proceeds step, which is the derecognition story's (GAP-3012; ASM-4985).
- **the ACE payment and score facts move behind rwb-source-data.** The legacy Data table reads `v_ace_payment` (DF-ACE-043 to DF-ACE-054) and `v_ace_score` (DF-ACE-270 to DF-ACE-279) in process. DP-05 replaces that with the owner's contract, and the target closes DP-05's second branch, "the service's own ACE views", because the 30 `recovery.v_ace_*` views are read only by rwb-source-data (Architecture v5 slide 8). The read is one hop through that contract and never a view of this service (GAP-3012; ASM-4987).
- **the case of record stays with rwb-case (P3).** `recovery_case`, its route state and the assignment of the officer are P3's, and the states `SETTLEMENT_PENDING`, `SETTLED` and `AWARD_CANCELED_DS` are written there. This story evaluates the rule and **answers** rwb-case for the move (GAP-3012; ASM-4982).
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the lot change, which is what legacy AC1 asked for and what legacy AC4 tested.
- **the settlement fact has no column.** TSD S6 T3.1 declares `debt_sale_lot` and `debt_sale_account` with eleven and seven fields and none of them carries a settlement date, a matched amount or a proceeds reference; `LOV-LOT-STATUS` has no `SETTLED` member. The step therefore records the outcome in the decision record and the case move and writes no business column, and the missing stamp is recorded for the DB story (GAP-3012; ASM-4984).
- **the operation that carries the step is a sibling's.** TSD S6 appendix T-A publishes five operations and none is a remittance or settlement operation. The two endpoint rows of the legacy story are the award path (API-S6-003) and the data room read (API-S6-004), which are RWB-S6-E6005-APP's and RWB-S6-E5026-APP's, so this story declares no operation of its own instead of claiming a sibling's (GAP-3012; ASM-4982).
- **the wave is EP06's and the service is wave 3.** Template and Rules §R5.6 keeps the W-MAP wave of a story when it is later than the service's Arch v5 wave, so this story is wave 4 while rwb-debtsale is created in wave 3; the conflict is recorded once for the service and the business epic (GAP-3012; ASM-4989).
- **the module extract is absent.** `_work/msr/extract/` holds no FSD or TSD S6 text, so the FSD S6 v3 and TSD S6 v2 files stand in as the module sources and the two sets are reconciled when the extract is produced (GAP-3012; ASM-4989).

The metric of the feature is unchanged and is the review of the settlement records, so no business value moves: the settlement period of `payment_terms` (DF-SAL-029), the `LOV-LOT-STATUS` and `LOV-BUYER-CLASS` members and the conditions of R-DS-25 to R-DS-27 are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S6-E6011-CON is published: the settlement element and its answer shape, the settled and cancelled elements, the closed lists, the consumed rows, the consumed event element, the error set and the fakes are baselined and handed to this story.
- The `ProceedsMatched` event of rwb-payment (P8) is published with its schema and an event fake, so a matched proceeds can be replayed on Day 1. Architecture v5 slide 19 IN gives the subscription and Event and Messaging Design v5 gives the payload `proceedsId`, `caseId`, `amount`; the envelope fields are Not specified in the source documents (GAP-3012; ASM-4985).
- The rwb-source-data contract of the ACE payment and score data products is published with its fake, so the payment date, the channel, the capital amount and the account score of the awarded accounts can be read under DP-05 on Day 1. Its operation names are Not specified in the source documents (GAP-3012; ASM-4987).
- The rwb-case case-state read and the case-move answer are available for the fake. No source publishes an operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome that the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-3012; ASM-4982).
- The rwb-partner scorecard read is published with its fake for the buyer score of R-DS-26; its operation name is Not specified in the source documents (GAP-3012; ASM-4986).
- The Debt sale rule package is in force at its version with R-DS-24, R-DS-25, R-DS-26 and R-DS-27; it is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The rule rows and the reference data of the lot status are governed there and are not listed for this story (GAP-3012; ASM-4983).
- The access contract of rwb-access (P4) answers the capability area and the right of the caller. DP-08 is not in this story's pattern set, so the check is stated here and the guard is a service-template capability (GAP-3012; ASM-4982).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the change and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration of its own (GAP-3012; ASM-4984).
- The service runs as its own login on schema `rwb_debtsale`; it holds no grant on another `rwb_*` schema and no SELECT on a `recovery.v_ace_*` view, so a statement on `rwb_payment`, `rwb_case`, `rwb_source_data` or `recovery.v_ace_payment` is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E6011-CON when its tests pass.

### 4. Flow

1. The lot is awarded under R-DS-23 and the settlement term starts under R-DS-24: the case enters `SETTLEMENT_PENDING`, the term is the `payment_terms` value of the lot (DF-SAL-029) and the award operation is API-S6-003, whose published surface is RWB-S6-E6005-APP's (GAP-3012; ASM-4982).
2. The buyer remits and rwb-payment matches the money to the award and publishes `ProceedsMatched` with `proceedsId`, `caseId` and `amount` (event 25; Event and Messaging Design v5).
3. The settle step of `DebtSaleWorkflow` on queue `rwb-debtsale` receives the event on its subscription, writes the inbox row against the event ID and answers a repeat with the stored result.
4. It reads the lot on its own schema: the lot reference, the buyer reference, the buyer class, the `payment_terms` and the status, which must be `AWARDED`, and it reads the account set with `selling_price` (DF-SAL-036) and `outstanding` (DF-SAL-035).
5. It reads the case state on the rwb-case contract, read only, to confirm that the case is in `SETTLEMENT_PENDING` and to take the case reference (GAP-3012; ASM-4982).
6. It reads the ACE payment facts of the awarded accounts on the rwb-source-data contract under DP-05: the payment code, the payment date, the amount, the channel and the capital amount, one hop with a 2 s budget and a breaker, and no `v_ace_*` view of its own (GAP-3012; ASM-4987).
7. `RemittanceEvaluator` loads the Debt sale package version in force from rwb-decision and tests the condition of R-DS-25, `payment received in full`, against the matched amount of the event and the sale price of the lot.
8. `SettlementDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the lot reference, the buyer reference, the proceeds reference, the rule ID with its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
9. On R-DS-25 the step confirms the settlement, releases the data transfer by signalling the transfer step of the saga and answers rwb-case with the move `SETTLED`, the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither.
10. On a recorded cancellation the evaluator applies R-DS-26 on the reason and answers `AWARD_CANCELED_DS`, and it reads the buyer scorecard of R-DS-26 on the rwb-partner contract and records the score reference with the cancellation in the decision record (GAP-3012; ASM-4986).
11. On an absent payment once the term of `payment_terms` has run, R-DS-27 answers the same `AWARD_CANCELED_DS` with its own reason and rule row; the term telemetry is the workflow's durable timer, not a Schedule of this service.
12. The settlement element is served read only on `/api/recovery/debtsale/v1` for SCR-26 Award through the gateway-bff composite route, with the lot reference, the buyer reference, the settlement state, the matched amount, the rule ID with its version and the decided-at time, and no personal data (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no settlement, no cancellation, no case-move answer leaves the service | MSG-P7-003 | AC1, AC4, TC-E6-011-04, TC-E6-011-06 |
| X2 | The role or the service identity does not hold the Debt sale right of the capability area | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E6-011-05 |
| X3 | The case is not in `SETTLEMENT_PENDING`, or the lot is not `AWARDED` | 409 and nothing is written; the settlement is not re-evaluated on an award that has already moved | MSG-GEN-001 | AC1, AC2 |
| X4 | The ACE payment product is stale after a late or failed batch (VR-S6-015-1) | The step holds, writes nothing and shows the data date; it resumes on the next fresh answer | MSG-P1-001 | AC1, AC2 |
| X5 | The rwb-source-data, rwb-case or rwb-partner contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC2 |
| X6 | The matched amount is neither clearly in full nor clearly short of the sale price | No rule fires: nothing changes, no record is written and the case keeps `SETTLEMENT_PENDING` | None | AC1, AC2 |
| X7 | The same `ProceedsMatched` event arrives twice, or a second proceeds arrives for the same lot | One record, one move and one release; the repeat is answered from the inbox row and counted | None | AC1, AC2 |
| X8 | A cancellation arrives with no recorded reason, or after the case has left `SETTLEMENT_PENDING` | R-DS-26 does not fire: nothing changes and the reason is required | MSG-GEN-001 | AC3 |
| X9 | A component, a statement or a test reaches `rwb_payment`, `rwb_case`, `rwb_source_data` or a `recovery.v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR9 |

X1 to X3 and X8 are the exception paths of RWB-E6-011 carried onto the split, X4 to X7 are the paths the event subscription and the DP-05 read add, and X9 is the DP-01 boundary. The settlement period and the list values are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6011-CON, the rwb-payment event fake, the rwb-source-data, rwb-case, rwb-partner and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P3, P4, P7, P8 or S9 |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the settlement element and the two tables are fixed |
| Valuable | The money side of a sold lot is closed, or the award is cancelled with its reason and its score, and the case moves in the service that owns it |
| Estimable | One workflow step, one event consumer, one evaluator, one record write, one move answer, one release signal, five clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots, proceeds and buyer scores through the fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Confirm buyer remittance

  Background:
    Given case "RC-2026-000842" carries the debt sale lot "LOT-2026-000042" of segment "RETAIL"
    Given the Debt sale rule package is in force at its version and carries R-DS-24, R-DS-25, R-DS-26 and R-DS-27
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Confirm buyer remittance (legacy RWB-E6-011 AC1)
    Given the rwb-payment contract mock returns the matched proceeds of the award for case "RC-2026-000842" with the amount in full
    Given the rwb-source-data contract mock returns the payment rows of the awarded accounts with a payment date and a capital amount
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then matches the buyer's payment to the award and closes the money side of the lot
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-25 (legacy RWB-E6-011 AC2)
    Given the rwb-case contract mock returns the case state "SETTLEMENT_PENDING" for "RC-2026-000842"
    Given the rwb-payment contract mock returns the buyer payment in full for lot "LOT-2026-000042"
    Given a case in state SETTLEMENT_PENDING
    When buyer settled
    Then confirm settlement and release the data transfer
    Then the case moves to SETTLED

  Scenario: AC3 Rule R-DS-26 (legacy RWB-E6-011 AC3)
    Given the rwb-case contract mock returns the case state "SETTLEMENT_PENDING" for "RC-2026-000842"
    Given the rwb-partner contract mock returns the buyer scorecard of "PTR-2026-000031"
    Given a case in state SETTLEMENT_PENDING
    When buyer canceled
    Then cancel the award and score the cancellation against the buyer
    Then the case moves to AWARD_CANCELED_DS

  Scenario: AC4 Not recorded (legacy RWB-E6-011 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E6-011 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written`, `buyer settled`, `buyer canceled` and `its trigger arrives` all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in four places in the target. The money is rwb-payment's (P8): the match of the payment to the award arrives as the `ProceedsMatched` event with `proceedsId`, `caseId` and `amount`, and the event fake stands in for the contract mock named in AC1 and AC2. The ACE payment and score facts of the awarded accounts are rwb-source-data's (P1) and are read on that contract under DP-05, never on a `v_ace_*` view of this service. The case moves `SETTLED` and `AWARD_CANCELED_DS` are **answered** to rwb-case, which writes the `recovery_case` row and its route state. The decision is recorded through the local decision-record library before anything changes, and the data transfer is released to the transfer step of the saga and not performed here. Three further notes are recorded rather than smoothed over. The settlement has no column on `debt_sale_lot` or `debt_sale_account`, so the outcome lives in the decision record, the move answer and the release signal until the DB story adds a stamp (GAP-3012; ASM-4984). The buyer score of R-DS-26 is a scorecard fact of rwb-partner and is referenced, not computed (GAP-3012; ASM-4986). And the legacy endpoint rows, the award path and the data room read, are API-S6-003 and API-S6-004 and belong to two sibling stories, so this step is a system step behind the award and declares no operation of its own (GAP-3012; ASM-4982). The fixtures carry no name, no identity number, no date of birth and no contact value: the buyer is an organisation and the accounts are referenced by their identifiers and their masked tape.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-24 | Debt sale | D8.4 | LOT_AWARDED | SETTLEMENT_TERM_STARTED | Any | Start the settlement term and await payment | SETTLEMENT_PENDING | Buyer | buyer portal, ALS core and GL | per agreed settlement period |
| R-DS-25 | Debt sale | D8.4 | SETTLEMENT_PENDING | BUYER_SETTLED | payment received in full | Confirm settlement and release the data transfer | SETTLED | Workbench | ALS core and GL | None |
| R-DS-26 | Debt sale | D8.4 | SETTLEMENT_PENDING | BUYER_CANCELED | cancellation recorded with a reason | Cancel the award and score the cancellation against the buyer | AWARD_CANCELED_DS | Debt sale officer | Decision Log, Recovery Data Store | None |
| R-DS-27 | Debt sale | D8.4 | SETTLEMENT_PENDING | SETTLEMENT_TERM_EXPIRED | payment absent and the settlement period passed | Cancel the award and score the buyer | AWARD_CANCELED_DS | Debt sale officer | Decision Log, buyer portal | None |

The four rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the case moves to `SETTLED` and `AWARD_CANCELED_DS` are written by rwb-case on this story's answer, the money is matched by rwb-payment, the decision log row is written here through the local library of DP-03 and centralised by rwb-decision (P7), and the buyer scorecard and the Recovery Data Store rows are other owners'. R-DS-24 is tabled because it is the row that opens the state this story works in and the row that carries the settlement period; its start is the award and derecognition story's.

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot and its account set are this service's: the buyer reference, the buyer class, the `payment_terms` and the status are columns of `debt_sale_lot`, and the sale price and the outstanding of each account are columns of `debt_sale_account`, in `rwb_debtsale` | Architecture v5 slide 41 (rwb-debtsale owns lots, data room, buyer terms, bids, award, transfer); TSD S6 T3.1 |
| BR2 | The decision is recorded before anything changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2 ("writes the decision log entry before any change"); legacy RWB-E6-011 AC1 and AC4 |
| BR3 | The money is rwb-payment's (P8): this story consumes the `ProceedsMatched` event and matches no payment, writes no `proceeds` row and posts nothing to the ledger | Event and Messaging Design v5 (EV-25); Architecture v5 slide 19 IN; GAP-3012 |
| BR4 | The case move is answered and not written: `recovery_case`, its route state and the officer's assignment are rwb-case's, and this story sends the move with the rule and its version | TSD S6 T5.2 (P3 for the case); Architecture v5 slide 4; GAP-3012 |
| BR5 | ACE data only through the owner's contract: the payment and score facts of the awarded accounts are read on the rwb-source-data contract, and this service holds no SELECT on any `recovery.v_ace_*` view | DP-05; Architecture v5 slide 8 (30 views read only by rwb-source-data); GAP-3012 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id` (DF-SAL-025) and `account_id` (DF-SAL-033) are identifiers of other services' facts | DP-01; TSD S6 T3.3 (relationships inside the module only) |
| BR7 | Every value a business person may change is reference data or a rule row read with its version: `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT`, `LOV-PUTBACK`, the settlement period of `payment_terms` and the conditions of R-DS-25 to R-DS-27 | TSD S6 T3.2; FSD S6 BR-S6-015; legacy Guardrails |
| BR8 | This story declares no REST operation of its own: it is a system step behind the award operation API-S6-003 and the data room read API-S6-004, which belong to two sibling stories | TSD S6 T-A.1; GAP-3012 |
| BR9 | The same `ProceedsMatched` event twice, or a second proceeds for the same lot, writes once, answers the move once and counts the repeat from its inbox row | Event and Messaging Design v5 (Transactions rule); Architecture v5 slide 11 |
| BR10 | No person name, identity number, date of birth, contact value or unmasked account identifier enters `rwb_debtsale`, the decision record, a log, an event or a workflow input; the buyer is an organisation and the tape is masked | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) |
| BR11 | The settlement is released to the transfer step and not performed here: R-DS-29, the data transfer, the derecognition and the general ledger posting are the sibling stories of this legacy key | Business Rules and Routing Logic v4 rows R-DS-29 to R-DS-31; FSD S6 A2.15.2 (prerequisite FEAT-DBS-12); GAP-3012 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story does own is the settlement state of the lot and the state of the step.

| From (settlement of the lot) | Event | Condition | To |
|---|---|---|---|
| Awarded, settlement pending | `ProceedsMatched` under R-DS-25 | payment received in full | Settled, with the move answer `SETTLED` and the data transfer released |
| Awarded, settlement pending | `ProceedsMatched` under R-DS-25 | amount neither clearly in full nor clearly short | Unchanged, no record and no answer |
| Awarded, settlement pending | A recorded cancellation under R-DS-26 | cancellation recorded with a reason | Award cancelled, with the move answer `AWARD_CANCELED_DS` and the buyer score referenced |
| Awarded, settlement pending | The term of `payment_terms` runs out under R-DS-27 | payment absent and the settlement period passed | Award cancelled, with the move answer `AWARD_CANCELED_DS` |
| Settled | The transfer step under R-DS-29 | The transfer has run | Not this story: `DATA_TRANSFERRED` in the transfer story |
| Settled, Award cancelled | Any repeated event for the same lot | X7 | Unchanged, the repeat is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The `ProceedsMatched` event arrives for a case in `SETTLEMENT_PENDING` | The package in force is loaded | Evaluating |
| Evaluating | The rule fires | The decision record is written | Applying |
| Applying | The move answer is sent and the transfer step is signalled | The transaction commits | Waiting for the transfer and the case closure |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | The rwb-source-data answer is stale or absent | X4, X5 | Held, until a fresh answer |

The route states `SETTLEMENT_PENDING`, `SETTLED`, `AWARD_CANCELED_DS`, `BIDDING_OPEN` and `DATA_TRANSFERRED` are those of the DEBTSALE machine of TSD S6 T4 and of the legacy criteria, and they live on the case of record. The lot status values are those of `LOV-LOT-STATUS` in TSD S6 T3.2, and none of them is `SETTLED`: the settlement is a money state of the case and of the decision record, not a lot status (GAP-3012; ASM-4984).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| None; runs unattended (the primary role of the feature) | The step itself: it reads the case, the lot, the payment and the score, evaluates the rule, writes the record and answers the move, under the service identity (FSD S6 A2.15.3.3) |
| RW-CREDITAD, Credit Administration officer | Debt sale R in TSD S6 T6.1: the legacy role of the feature; reads the settlement element and the cancelled award with its reason |
| RW-DEBTSALE, debt sale officer | Debt sale CRUA: records a cancellation with its reason under R-DS-26 and reads the settlement element |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Debt sale RA: reads the settlement element and the cancelled award; the approval itself is `ApprovalWorkflow` of rwb-decision (P7) |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: reads the settlement element and the cancelled award of the sale it approved |
| PT-BUYER, debt buyer and AMC | Partner portal RU, own lots only and scoped: remits outside this service and sees its own settlement state through the partner channel |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the TSD S6 T6.1 matrix gives the service identities: the step runs under the service identity and is subject to the same checks |
| rwb-debtsale service identity | Runs the step, consumes the event, evaluates the rules, writes the decision record, answers the case move and serves the settlement element; it holds no grant on another schema and no view of ACE |

The rights above are the rows of TSD S6 T6.1 and FSD S6 A2.15.3.3 and nothing wider. The legacy permission table gives Debt sale A to RW-DEBTSALE, RW-PRODHEAD and RW-HEADASL and Partner portal R to a long role list; in the target the partner read is the buyer's own, scoped to its lots, and the internal roles read the settlement element under their Debt sale right. DP-08 is not in this story's pattern set: the capability area and the right are declared per surface and the guard of the access service is a service-template capability, so the check is stated here and not built here (GAP-3012; ASM-4982).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot the proceeds are matched against |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Read, the lot reference of the screen answer |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Read, against `LOV-SEGMENT` |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Read only where the settlement is tested against the award price |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Read, the buyer the proceeds and the score belong to |
| DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_class | Read, against `LOV-BUYER-CLASS` |
| DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | payment_terms | Read, the agreed settlement period of R-DS-24 and R-DS-27 |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Read, against `LOV-LOT-STATUS`: the lot must be `AWARDED`; this story writes no status |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read, the account set: `selling_price` (DF-SAL-036) is the money the settlement is tested against |
| Standard columns | debt_sale_lot (S6, `rwb_debtsale`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Read; this story writes no row of the lot (GAP-3012; ASM-4984) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, reason, case move, decided at | Write through the local library, before anything changes (DP-03) |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment (P1 rwb-source-data) | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount and the rest | Not read as a view: the facts arrive on the rwb-source-data contract (DP-05) (GAP-3012; ASM-4987) |
| DF-ACE-270 to DF-ACE-279 | v_ace_score (P1 rwb-source-data) | score_key, account_key, model_code, model_version, score_value, estimate_value and the rest | Not read here: the account score is not a condition of R-DS-25 to R-DS-27, and the buyer score is a scorecard fact of S9 (GAP-3012; ASM-4986) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case contract and the move is answered to it |
| DF-WRK-009 to DF-WRK-016 | assignment (P3) | id, case_id, assignee_user_id, assigned_at, ended_at and the rest | Not read as a table: the officer of a cancellation is taken from the caller of the rwb-case contract (GAP-3012; ASM-4982) |
| DF-TRT-001 to DF-TRT-014 | treatment (S2) | id, case_id, decision_log_id, treatment_type and the rest | Not read as a table: the route of the case arrives on the rwb-case contract and the treatment is rwb-treatment's (GAP-3012; ASM-4982) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule id, rule version, route set, from state, event code | Not read as a table: the rule rows arrive in the package in force from rwb-decision |
| DF-REF-034 to DF-REF-038 | role (P4) | id, role_code, role_name, role_class, default_scope | Not read as a table: the capability area and the right are answered by rwb-access |

Field IDs are those of TSD S6 T3.1 and the Logical Data Model and Data Dictionary v9, and the five rows of the legacy Data table, `recovery_case`, `assignment`, `treatment`, `decision_log_entry` and the two ACE views, are the rows of other owners in the target. **No new table, no new column and no migration**: `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, the step reads their columns, and `decision_record`, `inbox_event`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_debtsale` by the library's own migration (DP-03). The missing settlement stamp is recorded rather than added (GAP-3012; ASM-4984).

**No personal data.** The rows this story writes and reads carry identifiers, codes, amounts, dates and a rule version. The buyer is a partner organisation: no name, no identity number, no date of birth, no address and no contact value enters `rwb_debtsale`, the decision record, a log, an event or a workflow input, and the fixture data of the tests is synthetic. Where the rwb-source-data contract returns a payment reference, it is an ACE reference and is stored as a reference, not copied with its narrative fields.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module and none of them is a remittance or settlement operation: API-S6-001 and API-S6-002 are the lot create and the lot read, API-S6-003 is the award, API-S6-004 is the data room read and API-S6-005 is the bid submission. The two endpoint rows of the legacy story are the award path (API-S6-003 `POST /debt-sale-lots/{lotId}/award`) and the data room read (API-S6-004 `GET /partner/data-room/{lotId}`), and they belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP. This story therefore provides no operation, claims no sibling's operation, and is a system step triggered by the `ProceedsMatched` event of rwb-payment. The absence is recorded as GAP-3012 with ASM-4982.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of the ACE payment data product of the awarded accounts (operation name Not specified in the source documents (GAP-3012; ASM-4987)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The payment code, payment date, payment amount, payment channel and capital amount of the account set; read only, faked, DP-05 |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the route `SETTLEMENT_PENDING` or otherwise; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3012; ASM-4982)) | rwb-case (P3) | P3 rwb-case | The answer that carries `SETTLED` or `AWARD_CANCELED_DS` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The buyer scorecard read (operation name Not specified in the source documents (GAP-3012; ASM-4986)) | `/api/recovery/partner/v1` | S9 rwb-partner | The buyer score of R-DS-26 for the buyer organisation of the lot; read only, faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-3012; ASM-4982)) | `/api/recovery/access/v1` | P4 rwb-access | The capability area "Debt sale", the right of the caller and the scope of its lots; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-24, R-DS-25, R-DS-26 and R-DS-27; read only, faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-3012 with ASM-4982.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (event 23) and `AccountsTransferred`, and neither is produced by this step: `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's. This story writes no outbox row, opens no producer and declares no event of its own, and a build that publishes one fails the absence test. The settlement outcome reaches rwb-case on the move answer, the transfer step on its release signal and the buyer on the read of the settlement element.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.payment.ProceedsMatched.v1` (event 25) | `rwb.payment.events.v1` and its `.dlt` topic | P8 rwb-payment | The matched proceeds of the award: `proceedsId`, `caseId` and `amount`; the trigger of the settle step, with the inbox row against the event ID |

The payload is the one Event and Messaging Design v5 gives for EV-25; the CloudEvents envelope fields (`id`, `source`, `type`, `time`, `subject`, `datacontenttype`) are Not specified in the source documents for this event (GAP-3012; ASM-4985). One consumer group, one subscription and one inbox row per event, and no second topic and no retry topic of this story's own beyond the service's retry and `.dlt` pair.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer and continues-as-new across the settlement and the put-back window | `rwb-debtsale` in namespace `rwb-recovery` | Input: the lot, the case, the route and the rule package in force; signals: the case state answered by rwb-case, the `ProceedsMatched` event, the rule package in force and the cancellation; the release of the transfer step out |
| `confirmRemittance` | Activity, the one settle-and-cancel step of this story | `rwb-debtsale` | The lot, the case, the matched proceeds and the package in force in; the rule ID with its package version, the settlement state, the decision record, the case move and the transfer release out |

No child workflow for the case and no workflow for the money exists in this service. The activity name is a target design choice of this story and is fixed by no source document; the trigger is read as the `ProceedsMatched` event because the architecture and the event set give it, while FSD S6 A2.15.4.4 declares "No background event" for the feature and is recorded as the loser of the precedence (GAP-3012; ASM-4985). The saga steps of the workflow, reserve accounts, approve sale, buyer pays, post proceeds, transfer accounts, close cases and tell customers, belong to the award, derecognition, transfer and case-closure stories of this service; this story owns the settle-and-cancel step alone.

#### 12.6 Schedules

None. The step runs from the `ProceedsMatched` event and the settlement term is a durable timer inside `DebtSaleWorkflow`, not a Temporal Schedule and not a legacy Quartz job: TSD S6 T2 lists jobs the module owns and the feature declares "No background event" (FSD S6 A2.15.4.4). No Job of Architecture v5 slide 44 is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer reference, its buyer class, its `payment_terms` and its status; read only here (GAP-3012; ASM-4984) |
| debt_sale_account | S6 (`rwb_debtsale`) | The account set with its `selling_price` and `outstanding`; read only here |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| inbox_event | PLT library, created in `rwb_debtsale` | The event ID of the consumed `ProceedsMatched` and the answer it holds |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of a repeated event or request and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object exists; this step writes no row to it |

Not owned and never read as a table: `recovery_case`, `timer` and `assignment` (P3), `proceeds` and `posting` (P8), `partner` and the scorecard (S9), `treatment` (S2), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6) and every `recovery.v_ace_*` view (P1). No foreign key leaves the schema and `debt_sale_lot.buyer_partner_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment `ProceedsMatched` event fake | The matched proceeds of lot `LOT-2026-000042` with `proceedsId`, `caseId` `RC-2026-000842` and the amount in full; a short amount; the same event twice; a malformed envelope; no event beyond the workflow timer | AC1, AC2, X5, X6, X7 |
| rwb-source-data payment fake | The payment rows of the awarded accounts of case `RC-2026-000842` with a payment date, a channel and a capital amount; a stale product; no answer beyond 2 s | AC1, AC2, X4, X5 |
| rwb-case case-state fake | The states `SETTLEMENT_PENDING`, `SETTLED` and `AWARD_CANCELED_DS` of case `RC-2026-000842`; a case that is not in the state the rule expects | AC1, AC2, AC3, X3 |
| rwb-case case-move fake | The moves `SETTLED` and `AWARD_CANCELED_DS` accepted; a move refused because the case is not in the state the rule expects | AC2, AC3, X3 |
| rwb-partner scorecard fake | The buyer scorecard of `PTR-2026-000031` with its score band; a buyer with no scorecard | AC3, X5 |
| rwb-access authorise fake | The capability area "Debt sale" with right R, C, U or A for the TSD S6 T6.1 roles; a role or a service identity without the right | AC1, X2 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-24, R-DS-25, R-DS-26 and R-DS-27 | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-26 Award answer for lot `LOT-2026-000042`, with the settlement element of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data payment read, the rwb-case move answer, the rwb-partner scorecard read and the rwb-access authorise call are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3012; ASM-4982).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | The rwb-source-data payment read, the rwb-case state read and the case-move answer, the rwb-partner scorecard read, the rwb-access authorise call and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 1 consumed | `rwb.payment.ProceedsMatched.v1` on `rwb.payment.events.v1`, one consumer group and one inbox row; `LotAwarded` and `AccountsTransferred` are sibling stories' |
| Temporal | 1 workflow and 1 activity | `DebtSaleWorkflow` and its `confirmRemittance` step on `rwb-debtsale`; the settlement term is a durable timer, no Schedule |
| File | None | No file is read, built or delivered here; INT-25 Debt buyers is reached through the data room of a sibling story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `settlement`, Java package `th.co.scb.ace.workbench.recovery.debtsale.settlement`; front end `src/modules/recovery/debtsale/LotSettlement.tsx`, the fragment SCR-26 Award embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the outcome commit together or not at all. DP-05 moves the two legacy ACE reads, `v_ace_payment` and `v_ace_score`, behind the rwb-source-data contract; its second branch, a service's own ACE views, is closed because the 30 `recovery.v_ace_*` views are read only by rwb-source-data (Architecture v5 slide 8) (GAP-3012; ASM-4987). DP-13 moves the base of the settlement element and nothing else. DP-19 is how SCR-26 Award reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The six consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-3012. DP-09 is not in the pattern set although the step consumes an event and needs the inbox library `RWB-PLT-TE006-CON`, and DP-04 is not in it although the step evaluates the Debt sale route set; neither is added to the metadata rows and both are named here and in the registers (GAP-3012; ASM-4983). The legacy feature dependency FEAT-DBS-12, the derecognition and general ledger posting, is a sibling story of this service whose identifier the plan's H row does not carry, so the dependency is tracked rather than added (GAP-3012; ASM-4988).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` settlement branch | Workflow | The branch that waits for the `ProceedsMatched` event and the cancellation, loads the package in force and reports the outcome to the parent |
| `confirmRemittance` | Activity | The one step: read the lot, the case, the payment and the score, evaluate R-DS-25, R-DS-26 or R-DS-27, write the record, answer the move and release the transfer |
| `ProceedsEventConsumer` | Consumer | The `rwb.payment.events.v1` listener, its inbox row, its dead-letter path and the workflow signal |
| `RemittanceEvaluator` | Service | The rule evaluation against the Debt sale package version in force, with the settlement period of `payment_terms` and the lot status list |
| `SettlementDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before anything changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `SettlementReader` | Repository | Reads `debt_sale_lot` and `debt_sale_account` in `rwb_debtsale`; writes no business column (GAP-3012; ASM-4984) |
| `PaymentFactsClient` | Client | The ACE payment read of rwb-source-data (P1) under DP-05, one hop, 2 s, breaker, no retry of its own |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case, one hop, 2 s |
| `BuyerScoreClient` | Client | The buyer scorecard read of rwb-partner (S9) for R-DS-26, one hop, 2 s |
| `AccessGuardClient` | Client | The capability area and the right of rwb-access (P4), through the service-template guard |
| `SettlementController` | Controller | The read of the settlement element on the service base, the capability area and right, and the problem mapping of 400, 401, 403, 404, 422 and 503; it declares no operation that TSD S6 T-A does not publish |
| `LotSettlement` | React component | Shows the settlement state, the cancelled award and its reason on SCR-26 Award, read only |

**Database and migrations.** No Flyway file of this story. `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, and the decision record, the inbox, the idempotency key and the outbox are library objects created in `rwb_debtsale` by the library's migration (DP-03). No settlement date, matched amount or proceeds reference column is added here; the absence is recorded for the DB story (GAP-3012; ASM-4984).

**Configuration and reference data.**

- `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The Debt sale package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the settlement period of `payment_terms` and the conditions of R-DS-25 to R-DS-27 are values of the package and of the lot, not of this build. No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The settlement branch of `DebtSaleWorkflow` and its input record, registered on `rwb-debtsale` as the stage child of `CaseWorkflow` (AC1).
2. `ProceedsEventConsumer` with its subscription, its inbox row, its repeat path and its dead-letter path (AC1, X7).
3. `PaymentFactsClient`, `CaseStateClient` and `BuyerScoreClient` against their fakes, with the 2 s budget, the breaker, the stale-data path and the no-answer path (AC1, AC2, AC3, X4, X5).
4. `AccessGuardClient` and the capability area, with the refusal path (AC1, X2).
5. `RemittanceEvaluator` over the Debt sale package, with R-DS-25, R-DS-26 and R-DS-27, the settlement period and the no-fire path (AC1, AC2, AC3, X6).
6. `SettlementDecisionRecordWriter` against the library stub, with the failed-write path (AC1, AC4, X1).
7. `CaseMoveAnswer` and the parent signal, with the two moves, and the release of the transfer step (AC2, AC3).
8. `SettlementReader` and the read-only path of the lot and its account set, with no business column written (AC1, BR8).
9. `SettlementController` and `LotSettlement` through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_debtsale`, no read of `recovery.v_ace_payment`, `recovery_case`, `proceeds`, `partner` or `treatment`, and no write to another service's schema (X9, BR5, BR9).

**Feature flag.** `rwb.debtsale.buyer-remittance-v1`, read as a flag of the platform library; off means the step holds the event, writes nothing and answers no move, and the award and transfer stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic `ProceedsMatched` event in SIT, each of the three rules produces its record and its move, a repeated event writes once, a forced record failure changes nothing, no `v_ace_*` read and no `recovery_case` row exists in the build, and SCR-26 Award answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the request or of the case state is absent or invalid (X3, X8) | Enter {field}. |
| MSG-P4-002 | A role or a service identity without the right of the capability area reads the settlement or records a cancellation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE payment product is stale after a late or failed batch (X4, VR-S6-015-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The five message IDs are those of the legacy message set and of FSD S6 A2.15.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S6-001 is carried because it is in the message set of the feature, and no path of this story raises it.

### 15. Screens and states

SCR-26 Award, "Bids against the reserve and the award decision" (FSD S6 Screens), is served through the gateway-bff composite route (DP-19) in its open, closed, awarded and transferred states, and this story produces the **closed** state of the money side and the cancelled state of the award. The route calls rwb-debtsale for the lot and the settlement element, rwb-case for the case and its route state and rwb-partner for the buyer; this story fixes the settlement element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The partner side reads its own settlement state through the partner channel, whose story row the plan does not carry (GAP-3012; ASM-4982).

The states of the settlement element are the pending, settled and cancelled states of §9, with the matched amount, the cancellation reason and the rule version, and it shows the failure states it reads: refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001 and a refused state with MSG-GEN-001. The award, transfer and put-back states of SCR-26 belong to the award, transfer and put-back stories of this service and are read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-011-01 | AC1 | Component | Lot `LOT-2026-000042` and case `RC-2026-000842` with a full matched proceeds; the record, the move and the transfer release asserted on the fakes |
| TC-E6-011-02 | AC2 | Component | The case at `SETTLEMENT_PENDING` with the payment in full; R-DS-25 evaluated, `SETTLED` answered and the transfer step released |
| TC-E6-011-03 | AC3 | Integration | The case at `SETTLEMENT_PENDING` with a recorded cancellation; R-DS-26 evaluated, the score referenced and `AWARD_CANCELED_DS` answered end to end on the fakes |
| TC-E6-011-04 | AC4 | Component | The decision-record stub stopped; nothing written, no move and MSG-P7-003 shown |
| TC-E6-011-05 | Access | Component | A role and a service identity without the Debt sale right; 403 with MSG-P4-002 and no read |
| TC-E6-011-06 | Principle 5 | Component | A forced decision log write failure at the moment of the settlement; no record, no release, no move and no second attempt |

The six legacy cases are the legacy cases of RWB-E6-011 in their legacy order, with the Level column added: `System` maps to `Component` where the step is tested on its fakes, and TC-E6-011-03 maps to `Integration` because it crosses the rwb-partner and rwb-case boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and no `-ITG` copy is written here.

### 17. Guardrails

- No business value in code: the settlement period, the lot status and buyer class members, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_debtsale`, in a workflow input, in an event or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic; the buyer is a partner organisation and the account tape is masked.
- ACE data only through the owner's contract: this service reads no `recovery.v_ace_*` view and holds no grant on `rwb_source_data`, and a build that adds one fails the boundary test (DP-05, BR5).
- The case stays with rwb-case, the money with rwb-payment, the ledger with rwb-decision and the score with rwb-partner: no `recovery_case` row, no `proceeds` row, no posting, no `decision_log_entry` row and no scorecard row is written here (BR3, BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13).
- No operation of a sibling is claimed: the award path is RWB-S6-E6005-APP's and the data room read is RWB-S6-E5026-APP's, and a story that declares them as its own fails the review (BR8).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no data-lake feed and no second event on the topic.
- The decision is recorded before the change and the move is answered, not written; a build that writes a case row or records after the outcome fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying (Business Requirements Program v5; owner Credit Administration); the split plan carries no requirement id for this slice (GAP-3012; ASM-4982) | The settle step, R-DS-25, the decision record, the `SETTLED` answer and the release of the data transfer | TC-E6-011-01, TC-E6-011-02, TC-E6-011-04 |
| REQ-S6-006 | The award of a lot is approved and recorded with the price achieved against the reserve; this story settles or cancels that award and references its price | The `payment_terms` and `selling_price` reads, and the cancelled award with its reason | TC-E6-011-02, TC-E6-011-03 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the lot settlement state | TC-E6-011-01 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login, with no ACE view | TC-E6-011-06 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `ProceedsMatched` consumer, its inbox row and the repeat path | TC-E6-011-01, TC-E6-011-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget | TC-E6-011-01, TC-E6-011-03 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the outcome | TC-E6-011-04, TC-E6-011-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-011, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E6-011-01 to TC-E6-011-06 |
| Feature and screens | FEAT-DBS-15 Confirm buyer remittance, SCR-26 Award |
| Rules | R-DS-25, R-DS-26 and R-DS-27, with R-DS-24 as the row that opens the state, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the settlement element, the consumed rows, the consumed event element, the error set and the fakes: RWB-S6-E6011-CON.
- The award of a lot and its `DecisionLogEntry` answer, API-S6-003: RWB-S6-E6005-APP.
- The data room read and its `DataRoom` answer, API-S6-004: RWB-S6-E5026-APP.
- The derecognition of the sold accounts and the posting to ALS and the general ledger, FEAT-DBS-12: the sibling story of this legacy key's prerequisite (GAP-3012; ASM-4988).
- The transfer of the account data to the buyer under R-DS-29 and FEAT-DBS-11, and the closure of the case in the sold lot under FEAT-DBS-14: the transfer and case-closure stories of this service.
- The put-back claim of FEAT-DBS-13 and the re-offer of R-DS-28: the put-back and re-offer stories of this service.
- The matching of the buyer's payment, the posting of the proceeds and the daily money reconciliation, FEAT-PAY-04, FEAT-PAY-07 and FEAT-PAY-11: rwb-payment (P8) (GAP-3012; ASM-4985).
- The ACE payment and score views and their data products: rwb-source-data (P1), read on its contract only (GAP-3012; ASM-4987).
- The case of record, its route states, its assignment and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes.
- The capability area, the rights and the scope rows, and the authorise call: rwb-access (P4) (GAP-3012; ASM-4982).
- The central decision ledger, the rule rows, their approval and their versioning: rwb-decision (P7).
- The buyer scorecard, the partner panel and the partner channel: rwb-partner (S9) (GAP-3012; ASM-4986).
- The sale agreement and the customer notices: rwb-document (P5) and rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-26, and the partner gateway: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
