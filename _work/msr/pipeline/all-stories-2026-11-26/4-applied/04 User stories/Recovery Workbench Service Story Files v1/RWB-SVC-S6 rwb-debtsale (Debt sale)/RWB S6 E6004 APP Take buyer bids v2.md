# RWB-S6-E6004-APP Take buyer bids

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E6004-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the bid-taking application slice of RWB-E6-004 split out for rwb-debtsale. The three legacy acceptance criteria are kept word for word with their origin tag; the step becomes two activities of `DebtSaleWorkflow` on task queue `rwb-debtsale`, which takes the bid on `POST /partner/data-room/{lotId}/bids` under R-DS-18, answers rwb-case for the move to `BIDS_RECEIVED`, and closes the lot on the claim window under R-DS-34 with realized recovery recorded by lot and by buyer and the move to `LOT_CLOSED`. The bid fact, the lot status and the realized recovery are written in `rwb_debtsale` with the decision recorded first through the local decision-record library (DP-03), and the bid element is served on `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route and the partner gateway (DP-19). The two legacy endpoint rows, the award path and the data room read, belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP, and the bid submission operation is published here with the publish-first question recorded. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E6004-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt buyer and AMC**, I want **the Workbench to let a qualified buyer bid on a lot through the portal, inside the bid window**, so that **debt sales run on approved lots and masked data**.

This is the application slice of legacy RWB-E6-004, the FEAT-DBS-08 step of the S6 Debt sale module. It owns:

- the three legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- the bid submission operation API-S6-005 `POST /partner/data-room/{lotId}/bids` on the service base, its `Bid` answer, its `Idempotency-Key` and its capability area (GAP-2988; ASM-4930);
- the evaluation of R-DS-18 on the bid and of R-DS-34 on the claim window of a lot already posted, with the Debt sale route set and its package version in force;
- the bid fact recorded against the lot and the account set of the lot in `rwb_debtsale`, and the lot status and the realized recovery of a closed lot on the columns of `debt_sale_lot` and `debt_sale_account` (DF-SAL-020 to DF-SAL-037);
- the local decision record of each outcome, written through RWB-PLT-E1027-CON before any row changes (DP-03), which is what legacy AC1 and AC3 test;
- the answer to rwb-case for the case moves `BIDS_RECEIVED` and `LOT_CLOSED`, with the rule ID and the version that produced each move;
- the bid and lot-closure element served read only on `/api/recovery/debtsale/v1` (DP-13) for SCR-26 Award and PRT-05 Data room, reached through the gateway-bff composite route and, for the buyer, through the partner gateway (DP-19).

It does not own: the published shape of the bid element, the lot element, the consumed rows, the case-move answer, the error set and the fakes, which are RWB-S6-E6004-CON; the award operation API-S6-003 and its `DecisionLogEntry` answer, which are RWB-S6-E6005-APP's; the data room read API-S6-004 and its `DataRoom` answer, which are RWB-S6-E5026-APP's; the lot create and lot read API-S6-001 and API-S6-002, which are the lot builder's; the buyer panel, the buyer's KYC, licence and non-disclosure evidence and the panel status, which are rwb-partner's (S9); the put-back claim and its review, R-DS-35, R-DS-36 and R-DS-39, which are RWB-S6-E6009-APP's; the case of record and its route states, which are rwb-case's (P3); the central decision ledger and the rule rows, which are rwb-decision's (P7); the capability area, the rights and the scope, which are rwb-access's (P4); the documents and the notices of the sale, which are rwb-document's (P5) and rwb-comms's (P6); the posting of the proceeds, which is rwb-payment's (P8); the read model of realized recovery, which is rwb-reporting's (P9); the partner gateway in the DMZ and the gateway-bff route, which are the edge stories' and RWB-PLT-N001-CON's; the debt buyers outside the bank, INT-25, which are reached through the partner portal; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-004 let a qualified buyer bid on a lot inside the bid window and, once the window and the claim window had passed, closed the lot with the realized recovery recorded. The FSD keeps the objective and the metric unchanged: the debt sale turnaround is measured on the decision log and the Workbench records, reviewed monthly, with a 45-day target (FSD S6 A2.8.1). The programme carries no requirement row for the bid itself; the nearest rows, REQ-S6-004 and REQ-S6-006, belong to the sibling keys (GAP-2988; ASM-4935).

What D-RCV-60 changes is where each fact lives and who may write it. In the monolith the lot, the bid, the case state, the decision log row and the rule row sat in one `recovery` schema and one process. In the target:

- **the lot, the bid and the realized recovery are this service's.** The service owns `debt_sale_lot` and `debt_sale_account` and the five debt sale operations (context pack S6), and TSD S6 T3.1 makes the lot and its account set the only tables of the module. No other service writes them (DP-01).
- **the bid amount has no contracted column.** R-DS-18 says the bid is recorded against the lot and the buyer, and R-DS-34 records realized recovery by lot and by buyer, yet TSD S6 T3.1 declares no bid amount, bid time or bid reference on either table and no realized-recovery column beyond `selling_price`. The step records the buyer reference and the lot state on the existing columns, the realized recovery on `selling_price` per account, and holds the amount, the time and the reference in the decision record and the idempotency row until the column set is added (GAP-2988; ASM-4931).
- **the case of record stays with rwb-case (P3).** `recovery_case` and the states `BIDDING_OPEN`, `BIDS_RECEIVED`, `GL_POSTED` and `LOT_CLOSED` are P3's; this story evaluates the rule, writes its own rows, records the decision and **answers** rwb-case for the move (GAP-2988; ASM-4928).
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the lot change, which is what legacy AC1 and AC3 test, and the central ledger row is rwb-decision's.
- **the operation set is tabled by TSD, not by the legacy story.** TSD S6 T-A.1 publishes five operations with the first-epic column: API-S6-005 `POST /partner/data-room/{lotId}/bids` is the bid submission with the Partner portal C right, and it is the surface of this key. The two endpoint rows of the legacy story, the award path API-S6-003 and the data room read API-S6-004, are the published surfaces of RWB-S6-E6005-APP and RWB-S6-E5026-APP, so the legacy table is recorded as two sibling rows and one operation is published here (GAP-2988; ASM-4930).
- **two rule rows are claimed twice.** Legacy RWB-E6-002 AC3 names R-DS-18 and its split story claims it, and legacy RWB-E6-009 AC3 names R-DS-34 and its split story claims it; the legacy criteria of this key are AC1, AC2 (R-DS-34) and AC3, and the bid operation, the bid fact and the close of a lot with no claim are this story's deliverable. This story owns R-DS-18 and the no-claim branch of R-DS-34, the claim branch and the close after a refused claim stay with RWB-S6-E6009-APP, and RWB-S6-E6002-APP keeps R-DS-18 tabled; one writer per rule is fixed at assembly and the reconciliation is recorded (GAP-2988; ASM-4932).
- **R-DS-34 names two systems that do not exist in the target.** The rule row carries "Recovery Data Store, Power BI" and a "per claim window" timer. There is no data lake and no Power BI feed (DP-17), no catalogue event carries a lot closure, and rwb-reporting builds its read model from events, so the realized recovery is written to this service's rows and the reporting destination is recorded rather than invented (GAP-2988; ASM-4933).
- **the wave is EP06's and the service is wave 3.** Template and Rules §R5.6 keeps the W-MAP wave of a story when it is later than the service's Arch v5 wave, so this story is wave 4 while rwb-debtsale is created in wave 3; the conflict is recorded once for the service and the business epic (GAP-2988; ASM-4934).
- **the buyer bids from outside the bank.** The legacy permission table gives the Partner portal right R to internal roles and the RBAC matrix gives `PT-BUYER` RU scoped to its own lots; the bid arrives through the partner gateway in the DMZ in front of rwb-partner, and that channel has no story row in the plan, so it is recorded as a missing row (GAP-2988; ASM-4937).

No business value moves: the bid window, the claim window, the reserve, the tiered terms and the list values are rows of the rule package and reference data, read with their version and never written in code.

### 3. Preconditions

- RWB-S6-E6004-CON is published: the bid element and its answer shape, the lot element, the closed lists, the consumed rows, the case-move answer, the error set and the fakes are baselined and handed to this story.
- The rwb-partner contract of the buyer clearance and the panel facts is published with its fake, so a buyer can be admitted to the window on Day 1. Its operation name is Not specified in the source documents (GAP-2988; ASM-4928), and the row is not in this story's contract-dependency list, which is None.
- The rwb-case case-state read and the case-move answer are available for the fake. No source publishes an operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-2988; ASM-4928).
- The Debt sale rule package is in force at its version with R-DS-17, R-DS-18, R-DS-34, R-DS-35 and R-DS-39; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The bid window, the claim window and the tiered terms are values of the package, not of this build (GAP-2988; ASM-4936).
- The access contract of rwb-access (P4) answers the capability area and the right of the caller, so a buyer identity without the Partner portal right C on the lot is refused before any write. DP-08 is not in this story's pattern set, so the check is stated here and the guard is a service-template capability (GAP-2988; ASM-4929).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the lot change and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award and PRT-05 Data room reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration of its own.
- The service runs as its own login on schema `rwb_debtsale`; it holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, `rwb_partner`, `rwb_decision`, `rwb_access` or `rwb_reporting` is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E6004-CON when its tests pass.

### 4. Flow

1. R-DS-17 opens bidding on an approved lot at the tiered terms, the case enters `BIDDING_OPEN` and the data room of API-S6-004 is open to admitted buyers; the window opening and the terms belong to the terms and data room stories of this service, and this step reads the state it needs.
2. A partner organisation admitted by rwb-partner submits a bid on `POST /partner/data-room/{lotId}/bids` (API-S6-005) through the partner gateway in the DMZ, with an `Idempotency-Key` and the lot reference (GAP-2988; ASM-4930).
3. The controller resolves the caller on the rwb-access contract: the capability area "Partner portal", the right C and the scope of the caller's own lots. A caller without the right is refused with 403 and MSG-P4-002 before any read.
4. The step reads the case state on the rwb-case contract, read only, and requires `BIDDING_OPEN`; a bid outside the window is refused with 409 and nothing is written.
5. It reads the buyer clearance and the buyer class on the rwb-partner contract, one hop with a 2 s budget and a breaker; no personal data of any person is read, and the buyer is an organisation (GAP-2988; ASM-4928).
6. `BidEvaluator` loads the Debt sale package version in force from rwb-decision and evaluates R-DS-18 on the fact: the bid is against the lot and a cleared buyer, and the window is open. Where no rule fires, nothing changes and the reason is reported to the parent.
7. `BidDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the lot reference, the partner reference, the rule ID with its version, the bid amount, the bid time, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
8. `BidWriter` writes the bid fact in one `rwb_debtsale` transaction with the decision record, the idempotency row and the outbox-free commit: `buyer_partner_id` (DF-SAL-025) and `buyer_class` (DF-SAL-026) on `debt_sale_lot`, the bid bound to the `debt_sale_account` rows of the lot (DF-SAL-031 to DF-SAL-037), and no amount column because TSD S6 T3.1 declares none (GAP-2988; ASM-4931).
9. The step answers rwb-case with the move `BIDS_RECEIVED`, the rule ID, the version and the decided-at time; rwb-case writes the `recovery_case` row and its route state, and this service writes neither.
10. When the claim window of a posted lot closes with no put-back claim, R-DS-34 fires on `GL_POSTED` with the event `CLAIM_WINDOW_CLOSED`: the step closes the lot, records the realized recovery by lot and by buyer and answers `LOT_CLOSED`. The wait is a durable timer of the workflow, and the window length is a value of the package (GAP-2988; ASM-4936).
11. `LotCloseWriter` writes the realized recovery on `debt_sale_account.selling_price` (DF-SAL-036) per account of the lot, sets `debt_sale_lot.status` to `CLOSED` against `LOV-LOT-STATUS` (DF-SAL-030) and keeps the buyer reference it already holds (DF-SAL-025), in one transaction with the decision record and the optimistic lock of `version`.
12. A repeated bid, a repeated claim-window answer or the same `Idempotency-Key` writes nothing, answers no second move and counts the repeat. A put-back claim inside the window is R-DS-35 and belongs to RWB-S6-E6009-APP: this step stops, writes nothing and leaves the lot in `GL_POSTED`.
13. The bid and lot-closure element is served read only on `/api/recovery/debtsale/v1` for SCR-26 Award and PRT-05 Data room through the gateway-bff composite route, with the lot reference, the buyer reference, the buyer class, the lot status, the realized recovery and the rule ID with its version, and no personal data (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no bid, no lot change, no realized recovery and no case-move answer leaves the service | MSG-P7-003 | AC1, AC3, TC-E6-004-03, TC-E6-004-05 |
| X2 | The role or the partner identity does not hold the Partner portal right C or the Debt sale right of the capability area | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E6-004-04 |
| X3 | The case is not in `BIDDING_OPEN` for a bid, or not in `GL_POSTED` for the claim-window close | 409 and nothing is written; no rule is re-evaluated on a case that has already moved | None | AC1, AC2 |
| X4 | A required field of the bid is absent or invalid | 422 with the field named and nothing written | MSG-GEN-001 | AC1 |
| X5 | The buyer is not cleared for the lot, or its panel status is not active | The bid is refused, the reason is recorded, and no move is answered; the qualification and bar paths are RWB-S6-E6002-APP's and RWB-S6-E6003-APP's | None | AC1 |
| X6 | The rwb-partner, rwb-case, rwb-access or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no case move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC2 |
| X7 | The bid window has not opened, or it has already closed | The bid is refused with 409 and the lot state is returned; nothing is written | None | AC1 |
| X8 | A put-back claim is raised inside the claim window | R-DS-35 fires and the lot stays in `GL_POSTED`; the claim, its review and the closure on refusal are RWB-S6-E6009-APP's | None | AC2 |
| X9 | A repeated bid, a repeated claim-window answer or the same `Idempotency-Key` arrives twice | One row, one answer and one decision record; the repeat is counted | None | AC1, AC2 |
| X10 | A component, a statement or a test reaches `rwb_case`, `rwb_partner`, `rwb_decision`, `rwb_access`, `rwb_reporting` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR1, BR9 |

X1 to X3 are the exception paths of RWB-E6-004 carried onto the split, X4 to X9 are the paths the target call types and the partner channel add, and X10 is the DP-01 boundary. The window lengths and the list values are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6004-CON, the rwb-partner, rwb-case, rwb-access and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P3, P4, P7 or S9 |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the bid element and the two tables are fixed |
| Valuable | A cleared buyer bids inside the window and the lot closes with realized recovery by lot and by buyer, with the case moving in the service that owns it |
| Estimable | Two workflow steps, two evaluator paths, two record writes, one bid operation, two case-move answers, four clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots and buyer organisations through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Take buyer bids

  Background:
    Given case "RC-2026-000842" carries the debt sale lot "LOT-2026-000042" of segment "RETAIL"
    Given the Debt sale rule package is in force at its version and carries R-DS-17, R-DS-18, R-DS-34, R-DS-35 and R-DS-39
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Take buyer bids (legacy RWB-E6-004 AC1)
    Given the rwb-partner contract mock returns the buyer organisation "PTR-2026-000031" cleared for the lot
    Given the rwb-case contract mock returns the case state "BIDDING_OPEN" for "RC-2026-000842"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets a qualified buyer bid on a lot through the portal, inside the bid window
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-34 (legacy RWB-E6-004 AC2)
    Given the rwb-case contract mock returns the case state "GL_POSTED" for "RC-2026-000842"
    Given a case in state GL_POSTED
    When claim window closed
    Then close the lot and record realized recovery by lot and by buyer
    Then the case moves to LOT_CLOSED

  Scenario: AC3 Not recorded (legacy RWB-E6-004 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E6-004 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written`, `claim window closed` and `the user acts on the screen` all stand. The cross-service parts are mocked, so AC1 and AC2 each carry a `Given the <service> contract mock returns <x>` line, and those added lines are the only additions to the legacy text. What the legacy lines describe happens in four places in the target. The bid arrives on API-S6-005, which this story publishes on `/api/recovery/debtsale/v1` through the partner gateway; the legacy endpoint rows are the award path and the data room read, and both are sibling stories' (GAP-2988; ASM-4930). The bid fact, the lot status and the realized recovery are written in `rwb_debtsale`, and the bid amount, time and reference are held in the decision record because no column carries them (GAP-2988; ASM-4931). The moves `BIDS_RECEIVED` and `LOT_CLOSED` are **answered** to rwb-case, which writes the case row and its route state. The decision is recorded through the local decision-record library before any row changes. The buyer is a partner organisation and never a person: the fixtures carry no name, no identity number, no date of birth and no contact value. One further note is recorded rather than smoothed over: R-DS-18 is named by legacy RWB-E6-002 AC3 as well and R-DS-34 by legacy RWB-E6-009 AC3, and this story owns both for its key because the bid operation, the bid fact and the close of a lot with no claim are its deliverable, while the claim branch stays with RWB-S6-E6009-APP (GAP-2988; ASM-4932).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-17 | Debt sale | D8.4 | BUYER_CLEARED | BIDDING_WINDOW_OPENED | Any | Open bidding on the lot at the tiered terms | BIDDING_OPEN | Buyer | buyer portal | per cycle |
| R-DS-18 | Debt sale | D8.4 | BIDDING_OPEN | BID_SUBMITTED | Any | Record the bid against the lot and the buyer | BIDS_RECEIVED | Workbench | buyer portal | None |
| R-DS-34 | Debt sale | D8.4 | GL_POSTED | CLAIM_WINDOW_CLOSED | no put-back claim inside the claim window | Close the lot and record realized recovery by lot and by buyer | LOT_CLOSED | Debt sale officer | Recovery Data Store, Power BI | per claim window |
| R-DS-35 | Debt sale | D8.4 | GL_POSTED | PUTBACK_CLAIMED | buyer raises a claim inside the sale terms | Record the claim and review it against the terms | PUTBACK_RAISED | Debt sale officer | buyer portal, Decision Log | 10 working days |
| R-DS-39 | Debt sale | D8.4 | PUTBACK_REFUSED | CLAIM_CLOSED | Any | Close the lot with realized recovery recorded | LOT_CLOSED | Debt sale officer | Recovery Data Store | None |

The five rows are the rows of the Business Rules and Routing Logic v4, copied character for character. R-DS-18 and R-DS-34 are this story's: the bid is recorded here and the claim-window close is here. R-DS-17 is tabled because it opens the window a bid stands on, and it belongs to the terms and data room stories. R-DS-35 and R-DS-39 are tabled because they are the other branch of the same gate: a put-back claim inside the window keeps the lot in `GL_POSTED` and the claim path is RWB-S6-E6009-APP's. The owner column is a role of the business and not a service: the two case moves are written by rwb-case on this story's answer, the lot and its accounts are written here, the decision ledger is centralised by rwb-decision (P7), and "Recovery Data Store" and "Power BI" have no target owner (GAP-2988; ASM-4933). R-DS-34 is named by the legacy criterion of RWB-E6-009 as well: this story owns its no-claim branch and the close, and the claim branch of R-DS-35 and the close after a refused claim, R-DS-39, are RWB-S6-E6009-APP's (GAP-2988; ASM-4932).

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot, the bid and the realized recovery are this service's: `buyer_partner_id`, `buyer_class`, `status` and `selling_price` are columns of `debt_sale_lot` and `debt_sale_account` in `rwb_debtsale`, and no other service writes them | Context pack S6 (tables and operations of rwb-debtsale); TSD S6 T3.1; GAP-2988 |
| BR2 | The decision is recorded before the row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2 ("writes the decision log entry before any change"); legacy RWB-E6-004 AC1 and AC3 |
| BR3 | The bid is accepted only inside the window and only from a cleared buyer: the window and the tiered terms are package values and the clearance is read on the rwb-partner contract | R-DS-17, R-DS-18; FSD S6 A2.8.3.1; GAP-2988 |
| BR4 | The case move is answered and not written: `recovery_case` and the states `BIDDING_OPEN`, `BIDS_RECEIVED`, `GL_POSTED` and `LOT_CLOSED` are rwb-case's, and this story sends the move with the rule and its version | Context pack S6 (P3 owns the case); TSD S6 T4; GAP-2988 |
| BR5 | No bid amount, bid time, bid reference or realized-recovery total is invented: the amount, the time and the reference are held in the decision record and the idempotency row, and the realized recovery is written on `selling_price` per account until the column set is added | TSD S6 T3.1; GAP-2988; ASM-4931 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id`, `account_id` and the case reference are identifiers of other services' facts | DP-01; TSD S6 T3.3 |
| BR7 | Every value a business person may change is reference data or a rule row read with its version: `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT`, `LOV-PUTBACK`, the bid window, the claim window, the reserve and the tiered terms | TSD S6 T3.2; FSD S6 BR-S6-008; legacy Guardrails |
| BR8 | The bid operation is API-S6-005 on the service base with the Partner portal right C and a required `Idempotency-Key`; a repeat with the same key writes once | TSD S6 T-A.1 and T-A.2; DP-13 |
| BR9 | No person name, identity number, date of birth, contact value or unmasked account identifier enters `rwb_debtsale`, the decision record, a log or a workflow input; the buyer is an organisation | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) |
| BR10 | The claim-window close publishes no event: the one event of the module, `LotAwarded`, is the award story's, and no catalogue entry carries a lot closure, so rwb-reporting's read model is fed by the award and transfer events, not by this step | TSD S6 T5.3; GAP-2988; ASM-4933 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story does own is the lot status of the closed lot and the state of the two steps.

| From (lot status, `LOV-LOT-STATUS`) | Event | Condition | To |
|---|---|---|---|
| OFFERED | The bid under R-DS-18 | The window is open and the buyer is cleared | Unchanged, the bid recorded against the lot and its account set |
| OFFERED, AWARDED | The claim-window close under R-DS-34 | No put-back claim inside the claim window | CLOSED, with the realized recovery on `selling_price` and the case-move answer `LOT_CLOSED` |
| OFFERED, AWARDED | The put-back claim under R-DS-35 | A claim inside the sale terms | Unchanged here: PUTBACK_RAISED is RWB-S6-E6009-APP's |
| CLOSED | Any repeated bid or claim-window answer | X9 | Unchanged, the repeat is counted |
| Any | A bid outside the window | X7 | Unchanged, 409 and no record |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A bid arrives for a case in `BIDDING_OPEN` | The package in force is loaded | Evaluating |
| Waiting | The claim window closes on a case in `GL_POSTED` | The durable timer fires | Evaluating |
| Evaluating | The rule fires | The decision record is written | Applying |
| Applying | The lot row and the idempotency row are written and the case-move answer is sent | The transaction commits | Waiting for the next bid or the claim window |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | A consumed contract is absent or its breaker is open | X6 | Held, until a fresh answer |

The states `BIDDING_OPEN`, `BIDS_RECEIVED`, `GL_POSTED` and `LOT_CLOSED` are those of the DEBTSALE machine of TSD S6 T4 and of the legacy criteria, and they live on the case of record. The lot status values are those of `LOV-LOT-STATUS` in TSD S6 T3.2.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| PT-BUYER, debt buyer and AMC | Partner portal RU, own lots only and scoped: submits the bid on its lot inside the window and reads its own bid state; the primary role of the feature (FSD S6 A2.8.3.3 "Debt buyer and AMC, primary") |
| RW-DEBTSALE, debt sale officer | Debt sale CRUA: reads the bid and the lot on SCR-26 Award and holds the close of the lot under R-DS-34 |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Debt sale RA: reads the bid outcome and the closed lot; the approval itself is `ApprovalWorkflow` of rwb-decision (P7) |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: reads the bid outcome and the realized recovery of the closed lot |
| PT-RAMC | Partner portal R: reads its own lots and the state of its own bids |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the TSD S6 T6.1 matrix gives the service identities: the step runs under the service identity and is subject to the same checks |
| rwb-debtsale service identity | Runs the two steps, evaluates the rules, writes the decision record, the bid and the realized recovery, answers the case moves and serves the element; it holds no grant on another schema |

The rights above are the rows of TSD S6 T6.1 and nothing wider. The legacy permission table gives the Partner portal right R to the internal case roles with a long role list; in the target that read is the partner's own, scoped to its lots, and the internal roles read the same element on SCR-26 Award under their Debt sale right. DP-08 is not in this story's pattern set: the capability area and the right are declared per surface and the guard of the access service is a service-template capability, so the check is stated here and not built here (GAP-2988; ASM-4929).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot the bid and the closure are recorded against |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Read, the lot reference of the screen answer |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Not written here |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Read, against `LOV-SEGMENT` |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Read for the closure answer; the terms and award stories own it |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Write, the partner reference of the bidder under R-DS-18 |
| DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_class | Write, against `LOV-BUYER-CLASS` (`AMC` or `NON_AMC`) |
| DF-SAL-027 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date | Not written here: the award story owns it |
| DF-SAL-028 | debt_sale_lot (S6, `rwb_debtsale`) | approval_authority | Not written here: the approval and award stories own it |
| DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | payment_terms | Not written here: the terms story owns it |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Write, against `LOV-LOT-STATUS`: `status` set to `CLOSED` on the R-DS-34 close |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read, the account set of the lot; `selling_price` (DF-SAL-036) is written with the realized recovery per account on the close (GAP-2988; ASM-4931) |
| Standard columns | debt_sale_lot (S6, `rwb_debtsale`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, bid amount, bid time, outcome, reason, case move, decided at | Write through the local library, before the row changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case contract and the move is answered to it |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule id, rule version, route set, from state, event code | Not read as a table: the rule rows arrive in the package in force from rwb-decision |
| DF-REF-034 to DF-REF-038 | role (P4) | id, role_code, role_name, role_class, default_scope | Not read as a table: the capability area and the right are answered by rwb-access |
| The bid amount, time and reference | no column in TSD S6 T3.1 | Not specified in the source documents (GAP-2988; ASM-4931) | Held in the decision record and the idempotency row until the column set is added |

Field IDs are those of the TSD S6 Debt sale v2 T3.1 and the Logical Data Model and Data Dictionary v9, and the three rows of the legacy Data table, `recovery_case`, `decision_log_entry` and `rule_row`, are the rows of other owners in the target. **No new table, no new column and no migration**: the two tables arrive with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_debtsale` by the library's own migration (DP-03).

**No personal data.** The rows this story writes carry identifiers, codes, amounts, dates and a rule version. The buyer is a partner organisation: no name, no identity number, no date of birth, no address and no contact value enters `rwb_debtsale`, the decision record, a log, an event or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/partner/data-room/{lotId}/bids` | `BidRequest` in, `Bid` of status 201 out (API-S6-005) | Partner portal, right C, scope applied | `Idempotency-Key` required |

The operation answers 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope lot, 409 for a lot outside the window, 422 with MSG-GEN-001 and 503 when a consumed contract or the library does not answer, each with the error envelope and one message ID of section 14. API-S6-001 `POST /debt-sale-lots` and API-S6-002 `GET /debt-sale-lots/{lotId}` are the lot builder's, API-S6-004 `GET /partner/data-room/{lotId}` is RWB-S6-E5026-APP's and API-S6-003 `POST /debt-sale-lots/{lotId}/award` is RWB-S6-E6005-APP's; the two endpoint rows of the legacy story are the last two, so this story publishes one operation and claims no sibling's. TSD S6 T-A.1 gives API-S6-005 "first in E5" while the data room story names the bid as a later story's; the publish-first question is recorded (GAP-2988; ASM-4930).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of the buyer clearance, the panel status and the buyer class (operation name Not specified in the source documents (GAP-2988; ASM-4928)) | `/api/recovery/partner/v1` | S9 rwb-partner | The clearance of the organisation for the lot, the panel status and the `LOV-BUYER-CLASS` value; read only, faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state `BIDDING_OPEN` or `GL_POSTED`, the case reference and the lot link; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2988; ASM-4928)) | rwb-case (P3) | P3 rwb-case | The answer that carries `BIDS_RECEIVED` or `LOT_CLOSED` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-2988; ASM-4928)) | `/api/recovery/access/v1` | P4 rwb-access | The capability area "Partner portal" and "Debt sale", the right of the caller and the scope of its own lots; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-17, R-DS-18, R-DS-34, R-DS-35 and R-DS-39; read only, faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2988 with ASM-4928.

#### 12.3 Events published

None. TSD S6 T5.3 declares one published event for the module, `LotAwarded` on `rwb.debtsale.events.v1`, and the award story owns it; the account transfer event is the transfer story's. Neither the bid nor the claim-window close is in the event set, so this story writes no outbox row, opens no producer and declares no event of its own, and the reported realized recovery has no event to travel on: that absence is recorded rather than filled with an invented event (GAP-2988; ASM-4933). A build that publishes an event here fails the absence test.

#### 12.4 Events consumed

None. The only consumed event of the service in the target is the payment match of the settlement step, which RWB-S6-E6011-APP owns, and no event carries a bid, a window opening or a claim-window close: the close is driven by the workflow's durable timer. This story therefore holds no consumer group, no subscription and no inbox row of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer and continues-as-new across the settlement, the claim window and the put-back window | `rwb-debtsale` in namespace `rwb-recovery` | Input: the lot, the case, the route and the rule package in force; signals: the case state answered by rwb-case, the buyer answer of rwb-partner, the rule package in force and the claim-window timer |
| `takeBid` | Activity, the bid step of this story | `rwb-debtsale` | The lot, the case, the buyer organisation and the bid in; the rule ID with its package version, the bid fact, the case move and the decision record out, in one transaction |
| `closeLotAfterClaimWindow` | Activity, the claim-window close of this story | `rwb-debtsale` | The lot, the case and the timer outcome in; the realized recovery, the lot status `CLOSED`, the case move and the decision record out, in one transaction |

The activity names are target design choices of this story and are fixed by no source document; the workflow, its queue and its saga shape come from TSD S6 T4 and the service row of the context pack. The saga steps of reserve, approval, award, buyer payment, transfer, proceeds, case closure and customer notices belong to the other stories of this service; this story owns the bid and the claim-window close.

#### 12.6 Schedules

None. The claim window is a durable timer inside `DebtSaleWorkflow`, not a Temporal Schedule, and TSD S6 publishes no job for the module: the timer row of R-DS-34 ("per claim window") is a value of the rule package, and the window length is Not specified in the source documents (GAP-2988; ASM-4936). No Quartz row, no shared job table and no batch table is owned here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer reference, its buyer class and its status; this story writes the columns of §11 |
| debt_sale_account | S6 (`rwb_debtsale`) | The account set of the lot; `selling_price` is written with the realized recovery on the close |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of each outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated bid or claim-window answer and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object exists; this story writes no row to it |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `partner`, `partner_user` and every panel or evidence table (S9), `role`, `permission` and the scope rows (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), the reporting read model (P9) and every `v_ace_*` view (P1). No foreign key leaves the schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner clearance fake | The organisation `PTR-2026-000031` cleared for lot `LOT-2026-000042` with an active panel status and the class `AMC`; the same organisation not cleared, with a suspended panel and with the class `NON_AMC`; no answer beyond 2 s | AC1, X5, X6 |
| rwb-case case-state fake | The states `BIDDING_OPEN` and `GL_POSTED` of case `RC-2026-000842`; a case in `BIDS_RECEIVED` and a case already `LOT_CLOSED` | AC1, AC2, X3 |
| rwb-case case-move fake | The moves `BIDS_RECEIVED` and `LOT_CLOSED` accepted; a move refused because the case is not in the state the rule expects | AC1, AC2, X3 |
| rwb-access authorise fake | The capability area "Partner portal" with right C or R for `PT-BUYER`, scoped to its own lot, and "Debt sale" with right A for `RW-DEBTSALE`; a caller without the right | AC1, X2 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-17, R-DS-18, R-DS-34, R-DS-35 and R-DS-39 | AC1, AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-26 Award answer for lot `LOT-2026-000042` and case `RC-2026-000842`, with the bid and lot-closure element read once | AC1, AC2 |
| Partner gateway route fake | The same bid element read and the bid submitted for `PTR-2026-000031`, scoped to its own lot, with no internal field | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-partner clearance read, the rwb-case move answer and the rwb-access authorise call are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2988; ASM-4928). The partner gateway fake stands in for a channel that has no plan row (GAP-2988; ASM-4937).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | The bid submission provided; the rwb-partner clearance read, the rwb-case state read and the case-move answer, the rwb-access authorise call and the rwb-decision package read consumed; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` is the award story's; no event carries a bid or a lot closure |
| Temporal | 1 workflow and 2 activities | `DebtSaleWorkflow` with `takeBid` and `closeLotAfterClaimWindow` on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here; INT-25 Debt buyers is reached through the partner portal and no file of this step leaves the bank |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `bid`, Java package `th.co.scb.ace.workbench.recovery.debtsale.bid`; front end `src/modules/recovery/debtsale/BidTake.tsx`, the fragment SCR-26 Award and PRT-05 Data room embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of both steps: the record and the lot change commit together or not at all. DP-13 moves the base of the bid operation and of the bid element and nothing else. DP-19 is how SCR-26 Award and PRT-05 reach this service, one hop through the gateway, and it is also the boundary of the partner channel, which reaches the same operation through the partner gateway (GAP-2988; ASM-4937).

**Dependencies the tables add and the plan does not hold.** The five consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2988. DP-08 is not in the pattern set although the bid operation declares a capability area and a right, and DP-09 is not in the pattern set although the library object `outbox_event` exists in the schema and the service owns a topic; neither is added to the metadata rows, and both are named in the text and in the registers (ASM-4929). DP-17 is not in the pattern set although R-DS-34 names a reporting destination that does not exist; the replacement is recorded (ASM-4933).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` bid and close branches | Workflow | The branches that wait for a bid and for the claim-window timer, load the package in force and report each outcome to the parent |
| `takeBid` | Activity | The bid step: read the case and the buyer, evaluate R-DS-18, write the record and the bid fact, answer `BIDS_RECEIVED` |
| `closeLotAfterClaimWindow` | Activity | The close step: evaluate R-DS-34 on the timer, write the record, the realized recovery and the lot status, answer `LOT_CLOSED` |
| `BidEvaluator` | Service | The rule evaluation against the Debt sale package version in force, with the window, the panel and the class values of the lists and the package |
| `BidDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `BidWriter` | Repository | Writes the bid fact and binds it to the `debt_sale_account` rows in one `rwb_debtsale` transaction, with the idempotency row and the optimistic lock |
| `LotCloseWriter` | Repository | Writes `selling_price` per account, sets the lot status to `CLOSED` and keeps the buyer reference, in one transaction with the record |
| `PartnerClearanceClient` | Client | The clearance, panel and class read of rwb-partner (S9), one hop, 2 s, breaker, no retry of its own |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case, one hop, 2 s |
| `AccessGuardClient` | Client | The capability area and the right of rwb-access (P4), through the service-template guard |
| `BidController` | Controller | The provided operation, its `Idempotency-Key`, the capability area and right, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `BidTake` | React component | Shows the bid state, the window state and the closure state on SCR-26 Award and PRT-05 Data room, read only |

**Database and migrations.** No Flyway file of this story: `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_debtsale` by the library's migration (DP-03). No bid amount, bid time or bid reference column is added here; the absence of that column set is recorded (GAP-2988; ASM-4931).

**Configuration and reference data.**

- `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The Debt sale package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the bid window, the claim window, the reserve and the tiered terms are values of the package, not of this build (ASM-4936).
- The capability areas "Partner portal" and "Debt sale" and their rights are access rows of rwb-access, read through the guard.
- The 2 s budget and the single hop are the platform rule of ADR-020; no parameter is named in the sources for either step.

**Build steps**

1. `BidController` and the provided operation on the service base, with the `Idempotency-Key`, the capability area and the problem mapping (AC1, X2, X4, X7).
2. `PartnerClearanceClient` and `CaseStateClient` against their fakes, with the 2 s budget, the breaker and the no-answer path (AC1, AC2, X5, X6).
3. `BidEvaluator` over the Debt sale package with R-DS-18, and its no-fire path (AC1, X7).
4. `BidDecisionRecordWriter` against the library stub, with the failed-write path (AC1, AC3, X1).
5. `BidWriter` with the one transaction, the two columns, the account binding and the idempotency row (AC1, X9).
6. `takeBid` and the `BIDS_RECEIVED` answer to the parent (AC1).
7. `closeLotAfterClaimWindow` with the durable timer, R-DS-34, `LotCloseWriter` and the `LOT_CLOSED` answer (AC2, X3, X8).
8. `BidTake` and the fragments of SCR-26 Award and PRT-05 through the composite route and partner gateway fakes (AC1, AC2).
9. The boundary test: no statement outside `rwb_debtsale`, no read of `partner`, `recovery_case`, `role` or `rule_row`, and no write to another service's schema (X10, BR1, BR6, BR9).

**Feature flag.** `rwb.debtsale.take-bids-v1`, read as a flag of the platform library; off means the operation answers 503, the workflow holds both branches, nothing is written and no move is answered, and the award and data room stories are unaffected.

**Done when.** The tests of section 16 pass, a synthetic bid on a lot in `BIDDING_OPEN` writes one record, the bid fact and the `BIDS_RECEIVED` answer, a claim-window close writes the realized recovery, the lot status `CLOSED` and the `LOT_CLOSED` answer, a repeated bid writes once, a forced record failure changes nothing, no `partner` or `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-26 Award and PRT-05 answer through their routes.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's and the eligibility rule's, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the bid request is absent or invalid (X4) | Enter {field}. |
| MSG-P4-002 | A role or a partner identity without the right of the capability area bids, reads the element or closes a lot (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are those of the legacy message set and of FSD S6 A2.8.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S6-001 is carried because it is in the message set of the feature, and no path of this story raises it.

### 15. Screens and states

SCR-26 Award in its open, closed, awarded and transferred states is served through the gateway-bff composite route (DP-19), and PRT-05 Data room, "lot data tapes and documents for admitted buyers, with bids" (FSD S6 Screens), is served to the partner on the same service base through the partner gateway in the DMZ. The route calls rwb-debtsale for the lot, the bid and the closure, rwb-case for the case and its route state and rwb-partner for the buyer organisation; this story fixes the bid and lot-closure element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The partner channel has no story row in the plan, and its gateway and identity are recorded as GAP-2988 with ASM-4937.

The states this story produces are the bid recorded on the lot, the lot status `CLOSED` with its realized recovery, and the two case-move answers; it shows the refusal and failure states it reads: refused with MSG-P4-002, out of the window with 409, not recorded with MSG-P7-003. The award, settlement and transfer states of SCR-26 belong to the award, settlement and transfer stories of this service and are read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-004-01 | AC1 | Component | The buyer organisation `PTR-2026-000031` and lot `LOT-2026-000042`; the recorded bid, the lot columns and the `BIDS_RECEIVED` answer asserted on the fakes |
| TC-E6-004-02 | AC2 | Component | Case `RC-2026-000842` at `GL_POSTED` with the claim window closed; R-DS-34 evaluated, `selling_price` written per account, the lot status `CLOSED` and `LOT_CLOSED` answered |
| TC-E6-004-03 | AC3 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E6-004-04 | Access | Component | A role and a partner identity without the Partner portal or the Debt sale right; 403 with MSG-P4-002 and no read |
| TC-E6-004-05 | Principle 5 | Component | A forced decision log write failure at the moment of the lot update; no lot change, no realized recovery, no answer and no second attempt |

The five cases are the legacy cases of RWB-E6-004 in their legacy order, with the Level column added: the legacy `System` level maps to `Component` because both steps are tested on their fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and none is written here.

### 17. Guardrails

- No business value in code: the bid window, the claim window, the reserve, the tiered terms, the panel values and the lists stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_debtsale`, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic. The buyer is a partner organisation.
- ACE data only through the owner's contract: this service reads no ACE table and no `v_ace_*` view, and a build that adds one fails the boundary test.
- The case stays with rwb-case, the buyer with rwb-partner, the access with rwb-access, the ledger with rwb-decision and the read model with rwb-reporting: no `recovery_case` row, no partner row, no role row, no `decision_log_entry` row and no reporting row is written here (BR4, BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13).
- No operation of a sibling is claimed: the award path is RWB-S6-E6005-APP's and the data room read is RWB-S6-E5026-APP's, and a story that declares them as its own fails the review.
- No value is invented to fill a missing column or a missing system: the bid amount is held in the decision record and the reporting destination is recorded, not guessed (GAP-2988).
- The decision is recorded before the change and each move is answered, not written; a build that writes a case row or records after the update fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| Not specified in the source documents (GAP-2988; ASM-4935) | No programme requirement row covers taking the bid or closing the lot; the nearest rows, REQ-S6-004 (a buyer check before bidding) and REQ-S6-006 (the award), belong to RWB-S6-E6002-APP and RWB-S6-E6005-APP, and the PRD (C1) allocates one for this slice | The bid operation, R-DS-18 and R-DS-34 with their two case moves | TC-E6-004-01, TC-E6-004-02 |
| R-DS-34 | Close the lot and record realized recovery by lot and by buyer (Business Rules and Routing Logic v4) | The claim-window close, the realized recovery on `selling_price` and the `LOT_CLOSED` answer | TC-E6-004-02 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the lot, the bid and the realized recovery | TC-E6-004-01 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E6-004-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The provided operation and the five consumed rows with their budget | TC-E6-004-01, TC-E6-004-02 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the lot changes | TC-E6-004-03, TC-E6-004-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-004, disposition Split (rework) |
| Legacy criteria | AC1 to AC3, owned word for word by this story |
| Test cases | TC-E6-004-01 to TC-E6-004-05 |
| Feature and screens | FEAT-DBS-08 Take buyer bids, SCR-26 Award and PRT-05 Data room |
| Rules | R-DS-18 and R-DS-34 owned; R-DS-17, R-DS-35 and R-DS-39 tabled, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the bid element, the lot element, the closed lists, the consumed rows, the case-move answer, the error set and the fakes: RWB-S6-E6004-CON.
- The award of a lot and its `DecisionLogEntry` answer, API-S6-003: RWB-S6-E6005-APP.
- The data room read and its `DataRoom` answer, API-S6-004: RWB-S6-E5026-APP.
- The lot create and lot read API-S6-001 and API-S6-002, and the reserve and the tiered terms: the lot builder and the terms stories of this service.
- The bidding window opening under R-DS-17 and its terms: the terms and data room stories of this service.
- The buyer panel, the KYC, licence and non-disclosure evidence and the panel status: rwb-partner (S9) (GAP-2988).
- The qualification of a buyer under R-DS-14, R-DS-15 and R-DS-16 and the bar under R-DS-40 and R-DS-41: RWB-S6-E6002-APP and RWB-S6-E6003-APP.
- The put-back claim and its review, R-DS-35, R-DS-36, R-DS-38 and R-DS-39: RWB-S6-E6009-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes (GAP-2988).
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4) (GAP-2988).
- The central decision ledger, the rule rows, their approval and their versioning: rwb-decision (P7).
- The sale agreement, the customer notices and their retention: rwb-document (P5) and rwb-comms (P6).
- The posting of the proceeds and the derecognition: rwb-payment (P8) and RWB-S6-E6008-APP.
- The reporting read model of realized recovery and the removed data lake: rwb-reporting (P9) and DP-17 (GAP-2988; ASM-4933).
- The partner gateway in the DMZ and its sign-in, and the gateway-bff composite route and the screen field list of SCR-26 and PRT-05: the edge stories and RWB-PLT-N001-CON (GAP-2988; ASM-4937).
- The debt buyers outside the bank, INT-25, which are reached through the partner portal and no adapter of this service.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
