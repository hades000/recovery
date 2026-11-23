# RWB-S6-E6002-APP Qualify a buyer against KYC and licensing

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E6002-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E6-002 in rwb-debtsale. The four legacy criteria are kept word for word with their origin tag; the qualification becomes the `qualifyBuyer` step of `DebtSaleWorkflow` on task queue `rwb-debtsale`, which evaluates R-DS-14 on the access request, R-DS-15 and R-DS-16 on the KYC and licence answer and R-DS-18 on the bid, records the outcome through the local decision-record library before any row changes (DP-03), answers rwb-case for the moves `BUYER_PENDING_KYC`, `BUYER_CLEARED`, `BUYER_REJECTED` and `BIDS_RECEIVED`, and answers the qualification element on base `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19). No bid table and no qualification operation exist in the sources, the buyer facts belong to rwb-partner, and the story is wave 4 while the service is wave 3. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer (RW-DEBTSALE)**, I want **the Workbench to run the KYC, licensing and eligibility checks before a buyer can bid**, so that **debt sales run on approved lots and masked data**.

This is the application slice of legacy RWB-E6-002, feature FEAT-DBS-06 of the S6 Debt sale module. It owns:

- the four legacy criteria of the key (AC1 to AC4), copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- the `qualifyBuyer` step of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`, run as the stage child of `CaseWorkflow` owned by rwb-case (Temporal and Drools Design slide 12, saga runner for S6; slide 13);
- the evaluation of R-DS-14 on the access request, R-DS-15 and R-DS-16 on the KYC, licence and panel answer of the bidder, and R-DS-18 on the bid, against the Debt sale package version in force (FSD S6 A2.6.3.1; TSD S6 T4);
- the bid fact of R-DS-18 as one decision record per bid — lot, buyer, account set, amount and bid window — because no table of this service carries a bid (GAP-2984; ASM-4914);
- the local decision record of every outcome, written through RWB-PLT-E1027-CON before anything changes (DP-03), which is what AC1 and AC4 test;
- the answer to rwb-case for the four moves, with the rule ID and the package version that produced each;
- the qualification element served behind the data room read of API-S6-004 and on SCR-26 Award, on `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19).

It does not own: the published shape of the qualification, buyer and bid elements, the consumed rows, the closed lists, the error set and the fakes, which are RWB-S6-E6002-CON; the data room read API-S6-004 and its `DataRoom` answer, which are RWB-S6-E5026-APP's; the bid operation API-S6-005, which is RWB-S6-E6004-APP's; the award API-S6-003, which is RWB-S6-E6005-APP's; the buyer panel, the NDA, the KYC, licence and panel facts, which are rwb-partner's (S9); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the rule rows and their version, which are rwb-decision's (P7); the rights and scope, which are rwb-access's (P4); the documents and the notices, which are rwb-document's (P5) and rwb-comms's (P6); the remediation window of R-DS-40 and the panel removal of R-DS-41, which are the bar story of this service; and the deployment of this build, which is the operations story of this key.

### 2. Business rationale

The objective, the problem and the metric are unchanged: the Workbench runs the KYC, licensing and eligibility checks on a bidder before it can bid (FSD S6 A2.6.1), because debt sales run on spreadsheets with no baseline turnaround (FSD S6 A1.3), and the turnaround is measured on the decision log and the Workbench records against a 45-day target, reviewed monthly (FSD S6 A2.6.1). The requirement is REQ-S6-004, "Buyers pass a know your customer, licensing and eligibility check before they bid", with REQ-S6-005 keeping the remediation window behind it (Business Requirements Program v4 §5.13). What D-RCV-60 changes is who owns each fact the check stands on.

- **The buyer is rwb-partner's.** The NDA date of R-DS-14, and the `kyc_status`, `licence_expiry` and `panel_status` of R-DS-15 and R-DS-16, are facts of the partner service (S9) in the target, read here on its contract and never as a table. The context pack gives rwb-debtsale no arrow to rwb-partner, so the row is a recorded conflict (GAP-2984; ASM-4912).
- **The case stays with rwb-case.** `recovery_case` and the route states `DATA_ROOM_OPEN`, `BUYER_PENDING_KYC`, `BUYER_CLEARED`, `BUYER_REJECTED`, `BIDDING_OPEN` and `BIDS_RECEIVED` are P3's: the step answers the move as the stage outcome and never writes the row (ASM-4915).
- **The decision is recorded first**, in the same transaction as the step's own writes, which is what AC1 asked for and AC4 tested.
- **The bid has no home.** R-DS-18 records the bid against the lot and the buyer, and the service owns bids, yet the two tables of the service (context pack; TSD S6 T3.1) carry no bid amount, bid time or bid reference, and no bid operation is published in T-A. The bid is therefore one decision record, and the missing table is raised rather than invented (GAP-2984; ASM-4914).
- **The qualification has no operation of its own.** TSD S6 T-A publishes five operations for the module and none is a KYC or qualification operation; the two endpoint rows of the legacy story are the award (API-S6-003) and the data room read (API-S6-004), which belong to two sibling stories. The step answers behind them and claims neither (GAP-2984; ASM-4917).
- **The package is read, not embedded.** The Debt sale route set is 41 rules over 29 states (TSD S6 T4), governed in rwb-decision; DP-04 is not in this key's pattern set, so the version in force arrives on the owner's activity contract and is recorded with the outcome (ASM-4913).
- **The wave is EP06's.** The W-MAP wave of EP06 is 4 and the service's Arch v5 wave is 3; the story keeps wave 4 (Template and Rules §R5.6; ASM-4916).

No business value moves: the NDA condition, the `kyc_status`, `licence_expiry` and `panel_status` values, the three-working-day target of R-DS-14 and the `LOV-BUYER-CLASS` values are reference data and rule rows, read with their version and never written in code.

### 3. Preconditions

- RWB-S6-E6002-CON is published: the qualification, buyer and bid elements, the closed lists, the consumed rows, the case-move answer, the error set and the fakes are baselined and handed to this story.
- The rwb-partner buyer contract is published with its fake, answering the NDA date, the KYC status, the licence expiry, the panel status and the buyer class of the bidder organisation; its operation name is Not specified in the source documents (GAP-2984; ASM-4912).
- The rwb-case state read and the case-move answer are available for the fake. No source publishes a REST operation that moves a case state for a stage; on the boundary the move is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes such an operation its name is Not specified in the source documents (GAP-2984; ASM-4915).
- The rwb-decision package activity answers the Debt sale package at its version in force, with R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26 among its 41 rules over 29 states; its activity name is Not specified in the source documents (GAP-2984; ASM-4913).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: the data room and SCR-26 Award reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard columns of TSD S6 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on `rwb_debtsale` and holds no grant on another `rwb_*` schema, so a statement on `rwb_partner`, `rwb_case`, `rwb_decision` or `rwb_access` is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E6002-CON when its tests pass, and the In review status of FSD S6 and TSD S6 is carried as a recorded assumption (GAP-2984; ASM-4919).

### 4. Flow

1. The data room of a lot is open under R-DS-13 and a partner organisation that has signed the non-disclosure agreement requests access to the lot; the request reaches this service on the data room read of API-S6-004, whose surface is RWB-S6-E5026-APP's (ASM-4917).
2. The `qualifyBuyer` step of `DebtSaleWorkflow` receives its trigger on `rwb-debtsale` and reads the case state the parent forwards, to confirm the case is in `DATA_ROOM_OPEN` and to take the lot and case references (ASM-4915).
3. The step reads the buyer organisation on the rwb-partner contract: the partner reference, the `nda_signed_at` date, the `kyc_status`, the `licence_expiry`, the `panel_status` and the buyer class, one hop with a 2 s budget and a breaker. The buyer is an organisation and no personal data of a person is read (ASM-4912).
4. The step takes the Debt sale package version in force from rwb-decision on its activity contract, one hop, and `BuyerQualificationEvaluator` evaluates R-DS-14 on `nda_signed_at present` (FSD S6 A2.6.3.1).
5. Where the NDA date is absent no rule fires: nothing changes, no record is written and the reason is reported to the parent.
6. `BuyerDecisionRecordWriter` writes one decision record through the local library **before any change**: the case and lot references, the buyer reference, the rule ID with its package version, the inputs reference, the outcome and the move. A failed write stops the step with nothing changed (DP-03; AC1, AC4).
7. The step answers rwb-case with the move `BUYER_PENDING_KYC`, the rule ID, the version and the decided-at time; rwb-case writes the `recovery_case` row and its route state, and this service writes neither.
8. The KYC and licence answer arrives on the rwb-partner contract and the evaluator applies R-DS-15 when `kyc_status = passed and licence_expiry after today and panel_status = active`, otherwise R-DS-16 when `kyc_status = failed or license expired or panel_status = suspended`; each writes its record and answers `BUYER_CLEARED` or `BUYER_REJECTED` with the recorded reason.
9. The bid arrives on the bid operation of API-S6-005, whose surface is RWB-S6-E6004-APP's. Under R-DS-18 the step records the bid — lot reference, buyer reference, the account set of the lot, the amount and the bid window — as one decision record, and answers rwb-case for `BIDS_RECEIVED`. The lot row and its status are not changed: no bid column and no bidding status exist in the two tables (GAP-2984; ASM-4914).
10. A repeated request, a repeated KYC answer or a repeated bid for the same lot, buyer and `Idempotency-Key` writes no second record, answers no second move and counts the repeat.
11. The qualification element is served read only on `/api/recovery/debtsale/v1` for the data room and SCR-26 Award through the gateway-bff composite route, with the buyer reference, the buyer class, the qualification state, the rule ID with its version and the decided-at time, and no personal data (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no record, no lot write and no case-move answer leaves the service | MSG-P7-003 | AC1, AC4, TC-E6-002-04, TC-E6-002-06 |
| X2 | The role or the partner identity lacks the Debt sale or the Partner portal right | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E6-002-05 |
| X3 | The case is not in the state the rule expects (`DATA_ROOM_OPEN` for R-DS-14, `BIDDING_OPEN` for R-DS-18) | The step holds and writes nothing; a case that has already moved is not re-evaluated | None | AC2, AC3 |
| X4 | The case data product is stale after a late or failed ACE batch | The step holds, writes nothing and shows the data date; it resumes on the next fresh answer | MSG-P1-001 | AC1, X5 |
| X5 | The rwb-partner, rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform envelope | None | AC1, X3 |
| X6 | The NDA date is absent, or the KYC condition is neither clearly met nor clearly failed | No rule fires: no record, no write and no move, and the case keeps its state | None | AC1, AC2 |
| X7 | A repeated request, KYC answer or bid with the same lot, buyer and `Idempotency-Key` | One record and one answer per outcome; the repeat is counted | None | AC3 |
| X8 | A component, a statement or a test reaches `rwb_partner`, `rwb_case`, `rwb_decision`, `rwb_access` or another `rwb_*` schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17, BR4, BR7 |

X1 to X3 are the legacy exception paths carried onto the slice, X4 to X7 are the paths the target call types and the repeated partner answer add, and X8 is the schema boundary of DP-01. The deviation codes X1 to X7 of the Debt sale route set are not the path identifiers of this table.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6002-CON, the rwb-partner, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P3, P7 or S9 |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the elements and the two tables are fixed |
| Valuable | A bidder is qualified, or refused with its reason, before it can bid, and the case moves in the service that owns it, so the 45-day turnaround is measurable |
| Estimable | One workflow step, one evaluator, one record writer, three clients, one case-move answer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic lot, case and buyer organisation through the contract fakes, plus the access and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Qualify a buyer against KYC and licensing

  Background:
    Given case "RC-2026-000842" carries the debt sale lot "LOT-2026-000042" of segment "RETAIL"
    Given the Debt sale rule package is in force at its version and carries R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Qualify a buyer against KYC and licensing (legacy RWB-E6-002 AC1)
    Given the rwb-partner contract mock returns the buyer organisation "PTR-2026-000031" with the non-disclosure agreement signed, KYC passed, a licence in date and an active panel status
    Given the rwb-case contract mock returns the case state "DATA_ROOM_OPEN" for "RC-2026-000842"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then runs the KYC, licensing and eligibility checks before a buyer can bid
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-14 (legacy RWB-E6-002 AC2)
    Given the rwb-partner contract mock returns the buyer organisation "PTR-2026-000031" with the non-disclosure agreement signed
    Given the rwb-case contract mock returns the case state "DATA_ROOM_OPEN" for "RC-2026-000842" and accepts the move "BUYER_PENDING_KYC"
    Given a case in state DATA_ROOM_OPEN
    When buyer requested access
    Then run the KYC, licensing and eligibility check on the bidder
    Then the case moves to BUYER_PENDING_KYC

  Scenario: AC3 Rule R-DS-18 (legacy RWB-E6-002 AC3)
    Given the rwb-partner contract mock returns the buyer organisation "PTR-2026-000031" cleared and admitted to the data room of "LOT-2026-000042"
    Given the rwb-case contract mock returns the case state "BIDDING_OPEN" for "RC-2026-000842" and accepts the move "BIDS_RECEIVED"
    Given a case in state BIDDING_OPEN
    When bid submitted
    Then record the bid against the lot and the buyer
    Then the case moves to BIDS_RECEIVED

  Scenario: AC4 Not recorded (legacy RWB-E6-002 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E6-002 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `its trigger arrives`, `buyer requested access`, `bid submitted`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry the `Given the <service> contract mock returns <x>` lines and those are the only additions. What the legacy lines describe happens in four places now: rwb-partner owns the NDA, KYC, licence and panel facts; rwb-case owns the case and writes the move; rwb-decision holds the package at its version; and this story evaluates the rules, writes the record and answers the move. Two points are recorded rather than smoothed over: the `decision log` of the legacy text is the local record of DP-03 in `rwb_debtsale`, with the central ledger of rwb-decision behind it; and AC3 records the bid as a decision record because no table of the service carries a bid (GAP-2984; ASM-4914).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-14 | Debt sale | D8.4 | DATA_ROOM_OPEN | BUYER_REQUESTED_ACCESS | nda_signed_at present | Run the KYC, licensing and eligibility check on the bidder | BUYER_PENDING_KYC | Workbench | Rules component, buyer portal | 3 working days |
| R-DS-15 | Debt sale | D8.4 | BUYER_PENDING_KYC | KYC_PASSED | kyc_status = passed and licence_expiry after today and panel_status = active | Admit the buyer to the data room | BUYER_CLEARED | Buyer | buyer portal | None |
| R-DS-16 | Debt sale | D8.4 | BUYER_PENDING_KYC | KYC_FAILED | kyc_status = failed or license expired or panel_status = suspended | Refuse access and record the reason | BUYER_REJECTED | Debt sale officer | Decision Log, buyer portal | None |
| R-DS-18 | Debt sale | D8.4 | BIDDING_OPEN | BID_SUBMITTED | Any | Record the bid against the lot and the buyer | BIDS_RECEIVED | Workbench | buyer portal | None |
| R-DS-26 | Debt sale | D8.4 | SETTLEMENT_PENDING | BUYER_CANCELED | cancellation recorded with a reason | Cancel the award and score the cancellation against the buyer | AWARD_CANCELED_DS | Debt sale officer | Decision Log, Recovery Data Store | None |

The five rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: "Rules component" is the Debt sale package read from rwb-decision (P7) and evaluated here, "buyer portal" is PRT-05, the "Decision Log" is this service's local record plus the central ledger, and "Recovery Data Store" is `rwb_debtsale`. The four moves are written by rwb-case on this story's answer. R-DS-26 is tabled because the cancellation scores the buyer of the same lot; its cancellation path belongs to the award and settlement stories and no path of this story cancels an award.

| ID | Rule | Source |
|---|---|---|
| BR1 | The qualification outcome and the bid fact are this service's: they are written in `rwb_debtsale` as decision records, and no other service writes them | TSD S6 T2, T3.1; context pack ownership rows (both S6); GAP-2984 |
| BR2 | The decision is recorded before anything changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2; legacy AC1 and AC4 |
| BR3 | The buyer panel and the NDA, KYC, licence and panel facts stay with rwb-partner (S9): this story reads no `partner` table and takes the facts on the owner's contract only | ASM-4912; FSD S6 A2.6.2 (integration points) |
| BR4 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and the move crosses the workflow boundary as the stage outcome | ASM-4915; TSD S6 T4 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id` and `account_id` are identifiers of other services' facts | DP-01; TSD S6 T3.3 |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: the NDA condition, the `kyc_status`, `licence_expiry` and `panel_status` values, the three-working-day target and `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-SEGMENT`, `LOV-PUTBACK` | TSD S6 T3.2; FSD S6 BR-S6-006; legacy Guardrails |
| BR7 | This story declares no REST operation of its own: the step answers behind API-S6-004 and API-S6-005, whose surfaces belong to two sibling stories | TSD S6 T-A.1; GAP-2984; ASM-4917 |
| BR8 | The same request, KYC answer or bid twice, or the same `Idempotency-Key` twice, writes one record and answers one move | TSD S6 T-A.2 |
| BR9 | No person name, identity number, date of birth, address or contact value enters `rwb_debtsale`, the record, a log or a workflow input; the buyer is an organisation | Template and Rules §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) |
| BR10 | No bid row is invented: the bid is recorded in the decision record, and the missing table is raised for the DB story rather than added here | GAP-2984; ASM-4914 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the qualification state of a bidder on a lot and the state of the step.

| From (qualification of a bidder) | Event | Condition | To |
|---|---|---|---|
| No bidder | The access request under R-DS-14 | nda_signed_at present | Pending KYC, with the answer `BUYER_PENDING_KYC` |
| No bidder | The access request under R-DS-14 | nda_signed_at absent | Unchanged, no record and no answer (X6) |
| Pending KYC | The KYC and licence answer under R-DS-15 | kyc_status = passed and licence_expiry after today and panel_status = active | Cleared, with the answer `BUYER_CLEARED` |
| Pending KYC | The KYC and licence answer under R-DS-16 | kyc_status = failed or license expired or panel_status = suspended | Rejected with its reason, with the answer `BUYER_REJECTED` |
| Cleared | The bid under R-DS-18 | The case is in `BIDDING_OPEN` for the lot | Bid recorded, with the answer `BIDS_RECEIVED` |
| Cleared, Rejected | A repeated answer for the same lot and buyer | X7 | Unchanged, the repeat is counted |
| Rejected | Later evidence inside the window | R-DS-40, the bar and remediation story of this service | Re-opened there, not here |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The access request, the KYC answer or the bid arrives | The package in force is read | Evaluating |
| Evaluating | R-DS-14, R-DS-15, R-DS-16 or R-DS-18 fires | The decision record is written | Applying |
| Applying | The record commits and the move is answered | The transaction commits | Waiting for the next answer |
| Applying | The record write fails | X1 | Waiting, nothing changed |
| Waiting | A consumed contract does not answer, or the case data is stale | X4, X5 | Held until a fresh answer |

The route states are those of the DEBTSALE machine of TSD S6 T4 and live on the case of record; the buyer class values are those of `LOV-BUYER-CLASS` and the lot status values those of `LOV-LOT-STATUS` in TSD S6 T3.2. This step writes no lot status: `BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED` and `CLOSED` belong to the lot, award and transfer stories.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: primary role of the feature, reading the qualification outcome and the bid of a lot |
| RW-PRODHEAD, product head | Debt sale RA: reads the qualification outcome and the bid; the DoA approval itself is `ApprovalWorkflow` of rwb-decision (P7) |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: reads the qualification outcome and holds the sale authority; the panel removal is the bar story of this service |
| RW-SALEOFF, RW-NPAMGR, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Debt sale R: read only, in scope |
| PT-BUYER, debt buyer and AMC | Partner portal RU: requests access to its own lot, supplies its evidence through rwb-partner and bids; sees its own qualification state and no other buyer's |
| PT-RAMC | Partner portal R: reads its own lots and the qualification state of its own bids |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-debtsale service identity | Runs the step, reads the buyer, the case and the package, writes the record and answers the move; it holds no grant on another schema |

The rights are the rows of TSD S6 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the debt sale officer as also-user (FSD S6 A2.6.3.3), and both statements hold: the step runs under the service identity, and the officer is the primary role when a person reads the outcome. DP-08 is not in this story's pattern set: the capability area and the right are declared per surface and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot the bid and the qualification are recorded against |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Read, the lot reference of the answer |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Read, the cut-off date the bid window is stated against |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Read, against `LOV-SEGMENT` |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Not read here: the award story tests it |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Not written here: the winning buyer is the award's; the bidder is recorded in the decision record (GAP-2984; ASM-4914) |
| DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_class | Read, the class of the lot against `LOV-BUYER-CLASS` |
| DF-SAL-027 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date | Not written here: the award story |
| DF-SAL-028 | debt_sale_lot (S6, `rwb_debtsale`) | approval_authority | Not written here: RWB-S6-E6001-APP |
| DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | payment_terms | Not written here: RWB-S6-E6001-APP |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Not written here: no bidding status exists in `LOV-LOT-STATUS` (GAP-2984; ASM-4914) |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read, the account set of the lot the bid is recorded against; no column of this table carries a bid |
| Standard columns | both tables (S6, `rwb_debtsale`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Not written here: this step changes no row of the two tables |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, reason, case move, decided at | Write through the local library, before anything else, once per outcome and once per bid |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the state arrives as a signal and the move is answered to rwb-case |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule id, rule version, route set, from state, event code | Not read as a table: the rows arrive in the package in force |
| Partner and partner_user (S9) | the buyer organisation | partner reference, nda_signed_at, kyc_status, licence_expiry, panel_status, buyer class | Not read as a table: the facts arrive on the rwb-partner contract, and no personal data of a person is read (ASM-4912) |

Field IDs are those of TSD S6 T3.1 and the Logical Data Model and Data Dictionary, and the four rows of the legacy Data table — `recovery_case`, `decision_log_entry`, `rule_row` and `role` — are other owners' rows in the target. **No new table, no new column and no migration**: the two tables arrive with the DB story of this service, this step changes no row of them, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_debtsale` by the library's own migration (DP-03). The bid table that R-DS-18 needs is missing from every source and is raised, not invented (GAP-2984; ASM-4914).

**No personal data.** The records carry identifiers, codes, amounts, dates, list values and a rule version. The buyer is a partner organisation, so no name, identity number, date of birth, address or contact value enters `rwb_debtsale`, the record, a log or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None published by this story. TSD S6 appendix T-A publishes five operations for the module — the lot create (API-S6-001), the lot read (API-S6-002), the award (API-S6-003), the data room read (API-S6-004) and the bid (API-S6-005) — and none is a qualification operation. The two endpoint rows of the legacy story are the award and the data room read, which belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP; the bid belongs to RWB-S6-E6004-APP. This story answers behind the data room read and the bid on base `/api/recovery/debtsale/v1` (DP-13), supplies the qualification properties of their answers, and claims no operation as its own (GAP-2984; ASM-4917).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of the buyer organisation and its NDA, KYC, licence and panel facts (operation name Not specified in the source documents (GAP-2984; ASM-4912)) | `/api/recovery/partner/v1` | S9 rwb-partner | The partner reference, `nda_signed_at`, `kyc_status`, `licence_expiry`, `panel_status` and the buyer class of the bidder; read only, faked. The context pack gives rwb-debtsale no arrow to rwb-partner, and the row is recorded as a conflict (GAP-2984; ASM-4912) |

One hop, a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The row is a contract dependency of class C that the plan's C row does not carry, and the absence is recorded (GAP-2984; ASM-4912). The rule package and the case are not REST rows: the connection matrix gives rwb-debtsale the Temporal cell for both (context pack, slide 13, row S6), so they are consumed as a package activity and as the parent's signal and stage outcome (§12.5).

#### 12.3 Events published

None. The service owns the topic `rwb.debtsale.events.v1` and its event set carries `LotAwarded` (event `EV-23`) with `AccountsTransferred` beside it (context pack, ownership rows and slide 19 notes), and neither belongs to this step: `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's. This story writes no outbox row, opens no producer group and declares no event, and a build that publishes one fails the absence test. The topic's retry and `.dlt` topics are the platform's (DP-14), and the outbox library of DP-09 is not in this key's pattern set.

#### 12.4 Events consumed

None. The matrix gives the service the `ProceedsMatched` event of rwb-payment (P8) for the settlement and transfer steps, which belong to RWB-S6-E6011-APP, and no event of the module carries an access request, a KYC answer or a bid. This story holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow`, a saga whose pivot is the transfer, continues-as-new at each stage end | `rwb-debtsale` in namespace `rwb-recovery` | The stage that hosts the qualification step; input: the lot, the case and the package in force; signals: the case state from the parent, the buyer answer, the bid |
| `qualifyBuyer` | Activity, the one qualification step | `rwb-debtsale` | The lot, the case and the buyer in; the rule ID with its package version, the qualification state, the bid record and the case move out, with the record written in the same transaction |
| The rule-package activity of rwb-decision (name Not specified in the source documents (GAP-2984; ASM-4913)) | Activity on the owner's queue, invoked once per stage start | `rwb-decision` | The Debt sale package at its version in force with R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26, and the reference data it reads |

The case move is not an activity: it is the stage outcome the child returns and the parent `CaseWorkflow` applies (ASM-4915). No child workflow for the case and none for the money exists in this service, and the activity name is a target design choice fixed by no source document. The trigger is the access request and the bid, because the FSD declares no background event for the feature (FSD S6 A2.6.4.4) and the step runs unattended.

#### 12.6 Schedules

None. The step runs from the access request, the KYC answer and the bid, and owns no Temporal Schedule and no legacy Quartz job. The monthly cycle of the route set is a timer of R-DS-01 and not a Schedule of this story, and no Job identifier of this key is named in the sources.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | Read only here: the lot reference, the segment, the buyer class and the cut-off date |
| debt_sale_account | S6 (`rwb_debtsale`) | Read only here: the account set of the lot the bid is recorded against |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked record of the qualification outcome and of the bid (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated request, answer or bid and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `partner` and `partner_user` (S9), the role and scope rows (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8) and every `v_ace_*` view (P1). No foreign key leaves the schema and `buyer_partner_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner buyer fake | Organisation `PTR-2026-000031` with the NDA signed, `kyc_status` passed, a licence in date and an active panel status; the same organisation with the NDA absent, KYC failed, an expired licence and a suspended panel; no answer beyond 2 s | AC1, AC2, AC3, X4, X5, X6 |
| rwb-case case and move fake | The states `DATA_ROOM_OPEN`, `BUYER_PENDING_KYC`, `BIDDING_OPEN` and `BUYER_CLEARED` of `RC-2026-000842`, and the four moves accepted; a case that is not in the state the rule expects | AC2, AC3, X3 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26 | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC1, AC4, X1 |
| gateway-bff composite route fake | The merged answer for `LOT-2026-000042` and `RC-2026-000842` with the qualification element read once | AC1, AC3 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the buyer read and of the package activity carry the placeholder until their owners confirm them (GAP-2984; ASM-4912, ASM-4913).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 1 consumed | The rwb-partner buyer read on `/api/recovery/partner/v1`; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` and `AccountsTransferred` are later stories' and no event is consumed here (§12.3, §12.4) |
| Temporal | 1 workflow, 1 activity registered, 1 activity invoked | `DebtSaleWorkflow` and `qualifyBuyer` on `rwb-debtsale`, with the package activity on `rwb-decision`; no Schedule |
| File | None | No file is read, built or delivered here; INT-25 is reached through the partner portal |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.debtsale`, module `buyerqualification`; front end `src/modules/recovery/debtsale/BuyerQualification.tsx`, the fragment PRT-05 Data room and SCR-26 Award embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record commits before anything else or the step changes nothing. DP-13 moves the base of the answer and nothing else. DP-19 is how the data room and SCR-26 Award reach this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-08 (the authorise contract) and DP-09 (the outbox library) are real neighbours of this step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-2984; ASM-4912, ASM-4913, ASM-4918).

**Dependencies the tables add and the plan does not hold.** The rwb-partner row is class C in fact and the plan's C row is None, so the story builds against its document and fake on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the package arrives on the owner's activity and is evaluated here, so no kit is declared. DP-08 would add `RWB-PLT-E1037-CON` and `RWB-P4-E1037-CON`; the guard is a service-template capability. The plan's three H rows stand unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` qualification branch | Workflow | Waits for the access request, the buyer answer and the bid, takes the package in force and reports the outcome to the parent |
| `qualifyBuyer` | Activity | The one step: read the buyer and the case, evaluate R-DS-14, R-DS-15, R-DS-16 or R-DS-18, write the record, answer the move |
| `BuyerQualificationEvaluator` | Service | The rule evaluation against the package in force, with the NDA condition, the KYC, licence and panel values, the closed lists and the no-fire path |
| `BuyerDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before anything else, hash-linked; refuses the step when the write fails |
| `BidRecordWriter` | Repository | Writes the bid record of R-DS-18 with the lot, the buyer, the account set, the amount and the window, in one transaction with the idempotency row (ASM-4914) |
| `PartnerBuyerClient` | Client | The buyer organisation and its NDA, KYC, licence and panel facts of rwb-partner, one hop, 2 s, breaker |
| `CaseSignalClient` | Client | The case state signal from the parent and the case-move answer, one hop, 2 s |
| `RulePackageClient` | Client | The package activity of rwb-decision at its version in force |
| `QualificationController` | Controller | The read of the qualification element on the service base, the capability area and right, and the problem mapping; it publishes no operation of its own |
| `BuyerQualification` | React component | Shows the qualification state and the refusal reason on PRT-05 and SCR-26 Award, read only |

**Database and migrations.** No Flyway file. The two tables arrive with the DB story of this service, and the record and the idempotency key are library objects created in `rwb_debtsale` by the library's own migration (DP-03). No bid table, bid column or lot status value is added: the missing bid table is raised for the DB story (GAP-2984; ASM-4914).

**Configuration and reference data.**

- `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-SEGMENT` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The Debt sale package and its version, governed in rwb-decision; the NDA condition, the `kyc_status`, `licence_expiry` and `panel_status` values and the three-working-day target are rule rows and reference data, never code.
- The capability areas "Debt sale" and "Partner portal" and their rights are access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The qualification branch of `DebtSaleWorkflow` and its input record, registered on `rwb-debtsale` as the stage child of `CaseWorkflow`, with the access request and the bid as triggers.
2. `PartnerBuyerClient` and `CaseSignalClient` against their fakes, with the 2 s budget, the breaker, the stale path and the no-answer path (AC1, AC2, X3, X4, X5).
3. `RulePackageClient` against its fake, with the version in force recorded with the outcome (AC1).
4. `BuyerQualificationEvaluator` over the package, with R-DS-14, R-DS-15, R-DS-16 and R-DS-18, the closed lists and the no-fire path (AC1, AC2, AC3, X6).
5. `BuyerDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC4, X1).
6. `BidRecordWriter` with the one transaction and the idempotency row (AC3, X7).
7. The case-move answer and the parent signal, with the four moves (AC2, AC3).
8. `QualificationController` with the rights and the problem mapping, publishing no operation of its own, and `BuyerQualification` on the two screens through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_debtsale`, no read of `partner`, `recovery_case`, `role` or `rule_row`, no `v_ace_*` read (X8, BR4, BR7).

**Feature flag.** `rwb.debtsale.buyer-qualification-v1`, a flag of the platform library; off means the step holds the request, writes nothing and answers no move, and the data room and award stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic access request in SIT, each of the four rules produces its record and its move, a repeated request or bid writes once, a forced record failure changes nothing, no `partner` or `recovery_case` row and no `v_ace_*` read exists in the build, and the two screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the message set of this key, which the legacy story lists. It names an open deviation on an account and is the eligibility story's, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the request or of the buyer fact is absent or invalid (X3, X6) | Enter {field}. |
| MSG-P4-002 | A role or a partner identity without the right of the capability area requests access, reads the outcome or bids (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The case data product is stale after a late or failed ACE batch (X4, VR-S6-006-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The five IDs are those of the legacy message set and FSD S6 A2.6.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S6-001 is carried with its feature and no path here raises it.

### 15. Screens and states

SCR-26 Award, in the legacy states "Open; closed; awarded; transferred", and PRT-05 Data room are served through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot and the qualification element, rwb-case for the case and its route state and rwb-partner for the buyer organisation; this story fixes the qualification element only, and the route specification and the screen field list belong to RWB-PLT-N001-CON. The partner reaches the data room through the partner gateway in the DMZ, whose sign-in and admission are the partner service's and the edge stories'.

The state this story produces on the element is the pending-KYC, cleared or rejected state of §9 with the refusal reason and the rule version, plus the bid recorded state of AC3. The refusal, not-recorded and stale-data states read the messages of §14. The award, settlement and transfer states of SCR-26 belong to the award, settlement and transfer stories and are read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-002-01 | AC1 | Component | Buyer `PTR-2026-000031` for lot `LOT-2026-000042`; the record, the qualification state and the case move asserted on the fakes |
| TC-E6-002-02 | AC2 | Component | Case `RC-2026-000842` at `DATA_ROOM_OPEN` with the NDA signed; R-DS-14 evaluated and `BUYER_PENDING_KYC` answered |
| TC-E6-002-03 | AC3 | Component | Case `RC-2026-000842` at `BIDDING_OPEN` with a cleared buyer; the bid record written and `BIDS_RECEIVED` answered |
| TC-E6-002-04 | AC4 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E6-002-05 | Access | Component | A role and a partner identity without the Debt sale or the Partner portal right; 403 with MSG-P4-002 and no read |
| TC-E6-002-06 | Principle 5 | Component | A forced record write failure at the moment of the bid; no record, no answer and no second attempt |

The six legacy cases are those of RWB-E6-002 in their legacy order, with the Level column added: every case runs on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the NDA condition, the `kyc_status`, `licence_expiry` and `panel_status` values, the three-working-day target, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_debtsale`, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only; the buyer is an organisation and every fixture is synthetic.
- ACE data only through the owner's contract: this service reads no ACE table and no `v_ace_*` view, and a build that adds one fails the boundary test.
- The case stays with rwb-case, the buyer with rwb-partner, the access with rwb-access and the central ledger with rwb-decision: no `recovery_case` row, no `partner` row, no role row and no `decision_log_entry` row is written here (BR3, BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No operation of a sibling is claimed: the data room read is RWB-S6-E5026-APP's, the bid is RWB-S6-E6004-APP's and the award is RWB-S6-E6005-APP's (BR7).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step.
- The decision is recorded before the change and the move is answered, not written; a build that writes a case row or records after the change fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S6-004 | Buyers pass a know your customer, licensing and eligibility check before they bid (Business Requirements Program v4 §5.13; FSD S6 A2.6); the split plan carries no requirement id for this slice (GAP-2984; ASM-4912) | The qualification step, R-DS-14, R-DS-15, R-DS-16 and R-DS-18, the record and the four moves | TC-E6-002-01, TC-E6-002-02, TC-E6-002-04 |
| REQ-S6-005 | A buyer who fails the check is given a remediation window and is removed from the panel if it is not met; the window and the bar are the sibling story's and this story records the rejection that starts them | The `BUYER_REJECTED` answer and its recorded reason | TC-E6-002-02 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the qualification outcome and the bid | TC-E6-002-01 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E6-002-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The rwb-partner row and the package activity with their budget | TC-E6-002-01, TC-E6-002-03 |
| ADR-022 | Local decision record plus central ledger | The record written before the change | TC-E6-002-04, TC-E6-002-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-002, disposition Split (rework); feature FEAT-DBS-06 |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Source text | Legacy RWB-E6-002; FSD S6 Debt sale v3 A2.6 and A1.3; TSD S6 Debt sale v2 T2, T3.1, T3.2, T4, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-DS-14 to R-DS-18 and R-DS-26 |
| Test cases | TC-E6-002-01 to TC-E6-002-06 |
| Feature and screens | FEAT-DBS-06 Qualify a buyer against KYC and licensing; SCR-26 Award, PRT-05 Data room |
| Rules | R-DS-14, R-DS-15, R-DS-16, R-DS-18 and R-DS-26, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the qualification, buyer and bid elements, the closed lists, the consumed rows, the error set and the fakes: RWB-S6-E6002-CON.
- The data room read API-S6-004 and its `DataRoom` answer: RWB-S6-E5026-APP. The bid operation API-S6-005 and the bidding window: RWB-S6-E6004-APP. The award API-S6-003 and the price test: RWB-S6-E6005-APP.
- The buyer panel, the partner users, the NDA, the KYC, licence and panel evidence: rwb-partner (S9) (ASM-4912).
- The remediation window of R-DS-40 and the panel removal of R-DS-41: the bar story of this service.
- The cancelled award and the buyer score under R-DS-26: the award and settlement stories of this service.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3) (ASM-4915).
- The central ledger, the rule rows and their approval: rwb-decision (P7) (ASM-4913). The capability areas, rights and scope: rwb-access (P4).
- The NDA and the sale documents: rwb-document (P5); the notices of the sale: rwb-comms (P6); the proceeds: rwb-payment (P8).
- The bid table that R-DS-18 needs: the DB story of this service, raised and not added here (ASM-4914).
- The partner gateway, the composite route and the screen field lists: the edge stories and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
