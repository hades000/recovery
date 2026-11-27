# RWB-S6-E6001-APP Approve lots, reserve and tiered terms

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S6-E6001-APP-16); the squad sizes it at refinement |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-E |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E6001-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | Five consumed contracts, listed in section 12.2 (GAP-2981) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-S6-E6001-APP-22) |
| Contract version | v1, base path /api/recovery/debtsale/v1; no contract version number is stated in the source documents (DOR-RWB-S6-E6001-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the committee-approval slice of RWB-E6-001 is built in rwb-debtsale. The four legacy criteria are kept word for word with their origin tag; the approval becomes the committee branch of `DebtSaleWorkflow` on task queue `rwb-debtsale`, which asks rwb-decision for the approval answer, applies R-DS-04 and R-DS-06 of the DS package, records the decision before the `debt_sale_lot` row changes (DP-03), writes the approved authority and terms, answers rwb-case for the case move and answers API-S6-002 on base `/api/recovery/debtsale/v1` (DP-13), reached through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (31 resolved, 19 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Head of Asset Liquidity**, I want **to take the lot, the reserve price and the terms to the committee for approval**, so that **debt sales run on approved lots and masked data**.

This is the committee-approval slice of legacy RWB-E6-001. It owns the four legacy criteria, copied verbatim with their origin tag, and the rules, messages and screens they depend on; the committee branch of `DebtSaleWorkflow` on queue `rwb-debtsale`, the saga child of `CaseWorkflow` owned by rwb-case; the evaluation of R-DS-04 on the priced lot and R-DS-06 on the answer, with the DS package version in force; the write of `approval_authority` (DF-SAL-028), `payment_terms` (DF-SAL-029) and, where the answer carries it, `signing_date` (DF-SAL-027) on the `debt_sale_lot` row, and of no other column; the local decision record, written through RWB-PLT-E1027-CON before the row changes (DP-03), which legacy AC1 and AC4 require; the answer to rwb-case for `LOT_WITH_COMMITTEE` and `LOT_APPROVED` with the rule ID and its version; and the read API-S6-002 `GET /debt-sale-lots/{lotId}` on base `/api/recovery/debtsale/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own the contract, element, lists, rights, errors and fakes (RWB-S6-E6001-CON); the award operation; the lot build, the price estimate and the reserve; the approval chain, the approval rows and the decision log (rwb-decision, P7); the DoA limit (rwb-access, P4); the case, its route states and the parent workflow (rwb-case, P3); the data room, tape, bids and buyer qualification; the document (rwb-document, P5); the notices (rwb-comms, P6); or the deployment of this build.

### 2. Business rationale

The feature and the problem are unchanged: "Takes the lot, the reserve price and the terms to the committee for approval", measured against a debt sale turnaround of 45 days on the decision log and the Workbench records, reviewed monthly (FSD S6 A2.5.1); debt sales run on spreadsheets with no baseline turnaround. What D-RCV-60 changes is where the approval lives. In the monolith one process wrote the lot row, the case stage and the decision log row in one `recovery` schema. In the target:

- **the lot is this service's.** `debt_sale_lot` and `debt_sale_account` are the two tables of S6 in `rwb_debtsale`, so the approved authority, the approved terms and the signature date are written here and nowhere else.
- **the approval is not this service's.** The kit's Approval template runs the maker-checker chain and the DoA lookup and is named for the DoA approvals of S2, S3, S5, S6 and S7 (context pack, Temporal slide 12). The chain, the act, the ledger entry and the limit are rwb-decision's and rwb-access's; this story asks and reads the answer (GAP-2980; ASM-4908).
- **the case of record stays with rwb-case.** `LOT_BUILT`, `LOT_WITH_COMMITTEE`, `LOT_APPROVED` and `LOT_WITHDRAWN` are case route states of P3 (TSD S6 T4); this story evaluates the rule, writes the lot columns and answers the move.
- **the decision is recorded first**, in the same transaction as the lot change, which is what TSD S6 T2 states and what legacy AC4 tested.
- **the reserve is approved, not recomputed**, so the pricing story stays the only writer of `reserve_price`.
- **no event leaves this step.** The service publishes one event, EV-23 `LotAwarded`, and it belongs to the award story; the approved lot reaches the case on the answer and its consumers on the read (ASM-4910).

Every threshold the step tests is reference data read with its version: the who-approves rule of the DS package and the DoA rows of P4. The key is EP06 and therefore wave 4, while rwb-debtsale is created in wave 3, so one service delivers its earlier keys in wave 3 and this key in wave 4, with the date copied unchanged and marked tentative.

### 3. Preconditions

- RWB-S6-E6001-CON is published: the read operation, the element with its approval fields, the closed lists, the consumed rows, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-decision approval contract is available as a fake: the chain read, the approver's act and the rule-package read. The act is named `POST /approvals/{id}/decide` in the architecture slides and carried as separate approve, return and refuse rows in the ownership rows; the three rows are used and the difference is recorded (GAP-2980; ASM-4909).
- The rwb-access DoA read is available as a fake: the delegation-limit rows of P4 that the approval chain tests the reserve and the terms against.
- The rwb-case state read and the case-move answer are available as a fake; where rwb-case publishes no REST operation for a move, the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-2980; ASM-4909).
- RWB-PLT-E1027-CON is published with its writer fake: the library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-25 Lot builder and SCR-26 Award reach this service through the gateway-bff composite route, one hop each (DP-19).
- `debt_sale_lot` exists in `rwb_debtsale` with the columns of DF-SAL-020 to DF-SAL-030 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration.
- The DS package is in force at its version with R-DS-04, R-DS-06, R-DS-07 and R-DS-08; the package is authored and approved in rwb-decision.
- The service runs as its own login on `rwb_debtsale` and holds no grant on another `rwb_*` schema, so a statement on `rwb_decision.approval`, `rwb_access.delegation_limit` or `rwb_case.recovery_case` is refused and fails the boundary test (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; the contract is tagged when its tests pass.

### 4. Flow

1. The lot is priced under R-DS-04: the lot builder proposes the lots, the tiered buyer terms and the reserve price, and the case sits in `LOT_BUILT`. This story receives the priced lot and does not price it.
2. The committee branch of `DebtSaleWorkflow` receives the priced lot, reads the case state and the case reference on the rwb-case read, one hop with a 2 s budget and a breaker.
3. The branch reads the lot and its accounts from `debt_sale_lot` and `debt_sale_account`, and the rule version in force from rwb-decision, so R-DS-04 can be applied to the fact the lot builder produced.
4. `CommitteeApprovalEvaluator` applies R-DS-04 (from `LOT_BUILT` on `LOT_PRICED`) and the branch answers the case move `LOT_WITH_COMMITTEE`; it writes no case row.
5. The branch submits the lot, the reserve and the tiered terms to the approval: it starts the kit's child `ApprovalWorkflow` on the rwb-decision queue with the maker-checker parameters and the DoA lookup as a parameter. P7 owns the chain, the approver's act and the ledger entry; this story holds the correlation and waits.
6. The committee answers. R-DS-06 is applied when "reserve and terms approved inside the delegation" holds and yields `LOT_APPROVED_BY_COMMITTEE`; R-DS-07 is applied when the committee raises the reserve and returns the lot to the committee; R-DS-08 is applied when the committee withdraws the lot.
7. `DebtSaleDecisionRecordWriter` writes one decision record **before any change**: the case and lot references, the rule ID with its version, the approval reference, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. `DebtSaleApprovalWriter` updates the lot row in one `rwb_debtsale` transaction with the record, the idempotency row and the optimistic lock: `approval_authority` from the who-approves answer, `payment_terms` from the terms the committee approved, and `signing_date` where the answer carries it. `reserve_price`, `status` and the buyer columns are not written here.
9. `CaseMoveAnswer` answers rwb-case with `LOT_APPROVED` (or `LOT_WITH_COMMITTEE` on R-DS-07, or `LOT_WITHDRAWN` on R-DS-08), the rule ID, the version and the decided-at time. rwb-case writes the case row.
10. A repeat of the same answer for the same lot, approval reference and outcome writes nothing, answers no second move and counts the repeat.
11. SCR-25 in its priced and approved states and SCR-26 in its open state read the lot, its reserve, its terms, its authority and its accounts on API-S6-002 through the gateway-bff route, read only.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no lot column and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E6-001-04, TC-E6-001-06 |
| X2 | The role does not hold the Debt sale right of the read | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC1, TC-E6-001-05 |
| X3 | The case is not in `LOT_BUILT` when the priced lot arrives, or not in `LOT_WITH_COMMITTEE` when the answer arrives | 409 and nothing is written; the step is not re-evaluated on a case that has already moved | None | AC2, AC3 |
| X4 | The committee approves outside the delegation, or the DoA read does not answer | R-DS-06 does not fire: the lot keeps its columns, no authority is written and the case keeps its state; the exception is raised on the approval chain in P7 | None | AC2, TC-E6-001-02 |
| X5 | A consumed contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's schedule; nothing is written and the caller sees 503 with the platform error envelope | None | AC1, AC2, AC3 |
| X6 | The committee raises the reserve (R-DS-07) or withdraws the lot (R-DS-08) | The outcome is recorded and the move the rule names is answered; no approval column is written | None | AC2 |
| X7 | The same answer arrives twice for the same lot, approval reference and outcome | One record, one update and one answer; the repeat is counted | None | AC1 |
| X8 | A statement reaches `rwb_decision`, `rwb_access`, `rwb_case` or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | AC5, BR7 |

X1 to X3 are the legacy exception paths carried onto the split; X4 to X7 are the paths the approval boundary adds, and X8 is the DP-01 and DP-02 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6001-CON, the P7, P4 and P3 fakes and the decision-record stub, on its own schema |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, messages, screens, read and columns are fixed |
| Valuable | A lot reaches the committee with its reserve and its tiered terms, is approved by the authority the DoA table names, and is read as approved by the case and by the screen |
| Estimable | One workflow branch, one evaluator, three clients, one record write, one row update, one answer, one controller and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every criterion runs on a synthetic lot and committee answer through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Approve lots, reserve and tiered terms

  Background:
    Given lot "LOT-2027-000041" carries accounts, a reserve price and tiered buyer terms for case "RC-2027-000611"
    Given the DS rule package is in force at its version and carries R-DS-04, R-DS-06, R-DS-07 and R-DS-08
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Approve lots, reserve and tiered terms (legacy RWB-E6-001 AC1)
    Given the rwb-decision contract mock returns the DS package in force and the approval chain of lot "LOT-2027-000041"
    Given the rwb-case contract mock returns the case state "LOT_WITH_COMMITTEE" for "RC-2027-000611"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes the lot, the reserve price and the terms to the committee for approval
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DS-06 (legacy RWB-E6-001 AC2)
    Given the rwb-decision contract mock returns the committee approval decided inside the delegation for lot "LOT-2027-000041"
    Given the rwb-access contract mock returns the DoA limit that lets the committee approve the reserve and the tiered terms
    Given the rwb-case contract mock returns the case state "LOT_WITH_COMMITTEE" for "RC-2027-000611"
    Given a case in state LOT_WITH_COMMITTEE
    When lot approved by committee
    Then approve the lot, the reserve and the tiered terms, and record the decision
    Then the case moves to LOT_APPROVED

  Scenario: AC3 Rule R-DS-04 (legacy RWB-E6-001 AC3)
    Given the rwb-decision contract mock returns the DS package in force with R-DS-04 for lot "LOT-2027-000041"
    Given a case in state LOT_BUILT
    When lot priced
    Then propose the lots, the tiered buyer terms and the reserve price
    Then the case moves to LOT_WITH_COMMITTEE

  Scenario: AC4 Not recorded (legacy RWB-E6-001 AC4)
    Given the rwb-decision contract mock returns the committee approval decided inside the delegation for lot "LOT-2027-000041"
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 No statement reaches another schema (DP-01, DP-02) (new, D-RCV-60)
    Given the rwb-debtsale service identity holds the grants of this story
    When a statement names `rwb_decision`, `rwb_access`, `rwb_case` or another service's schema
    Then the grant refuses the statement and the boundary test fails the build

  Scenario: AC6 A status change the model does not allow is refused (new, D-RCV-60)
    Given the rwb-case contract mock returns the case state "LOT_BUILT"
    Given a case in state LOT_BUILT
    When a status change is requested that the rule table does not allow
    Then nothing changes and the caller sees Not specified in the source documents (NEWAC-RWB-S6-E6001-APP-AC10)

  Scenario: AC7 The business rules of section 8 hold (BR1 to BR10) (new, D-RCV-60)
    Given the rwb-decision contract mock returns the committee approval decided inside the delegation for lot "LOT-2027-000041"
    Given the rwb-access contract mock returns the DoA limit that lets the committee approve the reserve and the tiered terms
    When lot approved by committee
    Then the write changes only `approval_authority`, `payment_terms` and `signing_date` of `debt_sale_lot` (BR1, BR6)
    Then the DoA limit is read on its contract and the who-approves thresholds are read with their version (BR4, BR8)

  Scenario: AC8 Error answers 401, 403 and 404 of the provided operations (new, D-RCV-60)
    Given the caller presents no valid token
    When API-S6-002 is called
    Then the answer is 401 and nothing is written
    Then the answer is 403 for a caller who holds no Debt sale right
    Then the answer is 404 for a lot that does not exist, and nothing is written

  Scenario: AC9 Activity retry and timeout (NEWAC-RWB-S6-E6001-APP-AC8) (new, D-RCV-60)
    Given an activity of `DebtSaleWorkflow` on task queue `rwb-debtsale` is retried or times out
    When the activity is retried or its timeout expires
    Then the outcome is Not specified in the source documents (NEWAC-RWB-S6-E6001-APP-AC8)

  Scenario: AC10 A consumed call fails or does not answer (NEWAC-RWB-S6-E6001-APP-AC9) (new, D-RCV-60)
    Given a consumed contract call is made by this story
    When the call fails or does not answer
    Then the outcome is Not specified in the source documents (NEWAC-RWB-S6-E6001-APP-AC9)
```

The four criteria are the legacy criteria of RWB-E6-001 with the origin tag added: the repetition of `Then`, and the legacy wording `the user acts on the screen`, `lot approved by committee`, `lot priced` and `the action is taken` all stand; the decision-log wording is replaced by decision record (CG-ALL-10439). Each criterion carries one or more `Given the <service> contract mock returns <x>` lines, and those lines are the only additions. What they describe happens in four places in the target: rwb-decision owns the chain, the act and the package, and the DoA limit is rwb-access's; rwb-case owns the route states and applies the move this story answers; this story evaluates R-DS-04 and R-DS-06, records the decision and writes the three lot columns; and the read that shows the approved lot on SCR-25 and SCR-26 is API-S6-002 on this service's base. Legacy AC2 moves the case to `LOT_APPROVED` and legacy AC3 moves it to `LOT_WITH_COMMITTEE`: both stand, the first is the answer and the second is the submission. This story publishes no event: the approval leaves the service on the case-move answer and on the read, and EV-23 LotAwarded stays with the award story (GAP-2982).

### 8. Business rules

| Rule | Route set | From state | Event | Condition | Action | To state |
|---|---|---|---|---|---|---|
| R-DS-06 | Debt sale | LOT_WITH_COMMITTEE | LOT_APPROVED_BY_COMMITTEE | reserve and terms approved inside the delegation | Approve the lot, the reserve and the tiered terms, and log the decision | LOT_APPROVED |
| R-DS-04 | Debt sale | LOT_BUILT | LOT_PRICED | lot agent estimate returned with COLLINS | Propose the lots, the tiered buyer terms and the reserve price | LOT_WITH_COMMITTEE |
| R-DS-07 | Debt sale | LOT_WITH_COMMITTEE | RESERVE_RAISED | committee raises the reserve | Reprice the lot and return it to the committee | LOT_WITH_COMMITTEE |
| R-DS-08 | Debt sale | LOT_WITH_COMMITTEE | LOT_REFUSED | committee withdraws the lot | Withdraw the lot with a recorded reason | LOT_WITHDRAWN |

The rows are those of the Business Rules and Routing Logic v4 for the Debt sale route set, copied unchanged. Their owner is a business role and not a service: the case states are written by rwb-case on this story's answer, the approval is decided on the P7 chain, the limit it is tested against is P4's, and the lot columns are written here. R-DS-07 and R-DS-08 are tabled because they are the other two answers of the same committee on the same lot row. R-DS-04 is tabled with the state and the fields it produces (LOT_BUILT to LOT_WITH_COMMITTEE); its criterion is AC3 of this story, and the split with RWB-S6-E5024 is recorded here (GAP-1956). The Credit approval committee member is not a Workbench role in this story: the committee's act arrives as the approval-chain answer and is read under the P4 DoA limit, and rwb-access publishes the committee level and its delegation limits (GAP-2983).

| ID | Rule | Source |
|---|---|---|
| BR1 | The approval columns of the lot are this service's: `approval_authority`, `payment_terms` and `signing_date` are columns of `debt_sale_lot`, and no other service writes them | Context pack ownership rows; TSD S6 T3.1 |
| BR2 | The decision is recorded before the lot row changes, with the rule ID and the package version; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2; legacy AC1 and AC4 |
| BR3 | The approval chain, the approver's act and the ledger entry stay with rwb-decision: this story starts the child approval, reads its answer and writes no approval row | GAP-2980; ASM-4908 |
| BR4 | The DoA limit is rwb-access's, read on its contract, and the who-approves rule is a row of the DS package, never a constant | Context pack ownership rows; DP-08 boundary |
| BR5 | The case move is answered and not written: `recovery_case` and its route states are rwb-case's | GAP-2980; ASM-4909 |
| BR6 | The reserve is approved and not recomputed: this step writes no `reserve_price`, no `status` and no buyer column | TSD S6 T3.1, T3.2 |
| BR7 | No cross-schema join and no foreign key leaves `rwb_debtsale`; the case, buyer and account references are identifiers of other services' facts | DP-01; TSD S6 T3.3 |
| BR8 | Every value a business person may change is reference data or a rule row read with its version: `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-PUTBACK`, the who-approves thresholds | TSD S6 T3.2; FSD S6 A2.5.3.1 BR-S6-005 |
| BR9 | The same answer twice, or the same `Idempotency-Key` twice, writes once and answers the move once | TSD S6 T-A.2 |
| BR10 | No person name, contact value or identity number enters the schema, the record, a log or a workflow input | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is not changed here: the step answers the move (BR5). What this story owns is the approval fact of the lot and the state of the step.

| From (case route state) | Event | Condition | To |
|---|---|---|---|
| `LOT_BUILT` | `LOT_PRICED` under R-DS-04 | lot agent estimate returned with COLLINS | `LOT_WITH_COMMITTEE`, submitted to the committee |
| `LOT_WITH_COMMITTEE` | `LOT_APPROVED_BY_COMMITTEE` under R-DS-06 | reserve and terms approved inside the delegation | `LOT_APPROVED`, with the authority and the terms written |
| `LOT_WITH_COMMITTEE` | `RESERVE_RAISED` under R-DS-07 | committee raises the reserve | `LOT_WITH_COMMITTEE`, no approval column written |
| `LOT_WITH_COMMITTEE` | `LOT_REFUSED` under R-DS-08 | committee withdraws the lot | `LOT_WITHDRAWN`, no approval column written |
| Any state the rule does not name | Any answer for the same lot | X3, X4 | Unchanged, the repeat or the exception is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The priced lot arrives for a case in `LOT_BUILT` | The package in force is loaded | Evaluating |
| Evaluating | R-DS-04 fires and the move is answered | The approval is submitted | Waiting for the committee |
| Waiting for the committee | The answer arrives | R-DS-06, R-DS-07 or R-DS-08 fires | Applying |
| Applying | The record, the lot columns and the answer are written | The transaction commits | Waiting for the next lot |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |

The route states are those of the DEBTSALE machine of TSD S6 T4 and of the legacy criteria. The lot's own status is `LOV-LOT-STATUS` — BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED — and no value of that list is the approval: approval is a case route state plus the three lot columns, and the lot stays `BUILDING` at approval.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: reads the lot and submits it to the committee; the A right it holds is exercised on the award story |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: the primary role of the feature, reads the lot and approves through the approval path where the DoA table names the level |
| RW-PRODHEAD, product head | Debt sale RA: reads the lot and approves through the approval path |
| RW-SALEOFF, RW-NPAMGR | Debt sale R: read the lot and its approval outcome |
| RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Debt sale R: read only, in scope |
| PT-BUYER, PT-RAMC | Debt sale R: the partner sees its own lot through the partner gateway, never the committee's approval authority |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R: service identities run the step under the same checks |
| rwb-debtsale service identity | Runs the branch, evaluates the rules, writes the record and the lot columns, answers the move; no grant on another schema |

The rights are the rows of TSD S6 T6.1 and of the legacy Permission checks table, and nothing wider. The legacy table gives the A right to RW-DEBTSALE, RW-PRODHEAD and RW-HEADASL, which is what T6.1's CRUA and RA rows say. FSD S6 A2.5.3.3 also names "Credit approval committee member", which has no row in T6.1; the act is taken on the P7 approval chain under the P4 DoA limit, this story writes only the authority it is told, and the difference is recorded (GAP-2983; ASM-4911). The authorise check on rwb-access for each REST operation of this story is Not specified in the source documents (DOR-RWB-S6-E6001-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot reference of the row, the record and the answer |
| DF-SAL-021 | debt_sale_lot (S6) | lot_no | Read, shown on the approval view |
| DF-SAL-022 | debt_sale_lot (S6) | cut_off_date | Read |
| DF-SAL-023 | debt_sale_lot (S6) | segment | Read, against `LOV-SEGMENT` |
| DF-SAL-024 | debt_sale_lot (S6) | reserve_price | Read and approved, never written here |
| DF-SAL-025 | debt_sale_lot (S6) | buyer_partner_id | Not written here: the award step writes it |
| DF-SAL-026 | debt_sale_lot (S6) | buyer_class | Not written here, against `LOV-BUYER-CLASS` |
| DF-SAL-027 | debt_sale_lot (S6) | signing_date | Write where the answer carries the sale date; otherwise left as it was |
| DF-SAL-028 | debt_sale_lot (S6) | approval_authority | Write, from the who-approves answer of the approval |
| DF-SAL-029 | debt_sale_lot (S6) | payment_terms | Write, the tiered buyer terms the committee approved |
| DF-SAL-030 | debt_sale_lot (S6) | status | Read, against `LOV-LOT-STATUS`; unchanged here (BR6) |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read only, as the accounts of the lot the read answers |
| Standard columns | debt_sale_lot (S6) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write `updated_at`, `updated_by` and the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, decided at | Write through the library, before the lot row changes |
| approval rows | approval (P7, `rwb_decision`) | the chain, the approver's act, the DoA level tested | Not read as a table: the answer arrives on the contract (GAP-2980) |
| `delegation_limit` | delegation_limit (P4, `rwb_access`) | the DoA limit of the level | Not read as a table: the limit arrives on the contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the state arrives on the read and the move is answered |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, from_state, event_code and the rest | Not read as a table: the package in force is loaded from rwb-decision |

Field IDs are those of TSD S6 T3.1 and the Logical Data Model v8. The `recovery_case` and `rule_row` rows are the legacy rows with their owner moved to P3 and P7, and the legacy `decision_log_entry` is read as the local record of DP-03 plus the ledger entry P7 writes. **No new table, no new column and no migration**: the two tables arrive with the DB story, this story writes three existing columns, and the record, the key and the outbox are library objects. The FSD catalog of A2.5.3.2 omits `payment_terms` and `status`; the TSD stands under R-PREC.

**No personal data.** The rows carry identifiers, codes, amounts, dates and a rule version; no name, address, contact value or identity number enters the schema, the record, a log or a workflow input, and test data is synthetic.

**Reference data.** This story reads the lists `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` and the who-approves thresholds as parameters, each read with its version (BR8). The reference-data contract that serves them is Not specified in the source documents (DOR-RWB-S6-E6001-APP-20); the parameter keys are not named in the source documents.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13). This story supplies the behaviour behind the one read whose shape is declared by RWB-S6-E6001-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/debt-sale-lots/{lotId}` | `DebtSaleLot` of status 200 out, with its accounts, reserve and bids (API-S6-002) | Debt sale, right R, scope applied | Not applicable |

Errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope lot, 409 for a case in the wrong state on the answer, and 503 when a consumed contract does not answer. The operation is a read and declares no `Idempotency-Key` (TSD S6 T-A.2). The committee view of SCR-25 and the award view of SCR-26 are composed on the gateway-bff route from this read, from the approval rows of rwb-decision and from the case state of rwb-case; this service provides no approval operation of its own. `POST /debt-sale-lots` and `POST /debt-sale-lots/{lotId}/award` belong to other S6 keys and are not built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The approval chain read and the approver's act (three act rows; the architecture names one `POST /approvals/{id}/decide`) | `/api/recovery/decision/v1` | P7 rwb-decision | The chain of the lot, the act and the DoA level tested; faked (GAP-2980; ASM-4909) |
| The read of the DS rule package version in force (operation name Not specified in the source documents (GAP-2980; ASM-4909)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows of R-DS-04, R-DS-06, R-DS-07 and R-DS-08; faked |
| `GET /doa-limits` | `/api/recovery/access/v1` | P4 rwb-access | The `delegation_limit` row of the approver's level; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the stage; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2980; ASM-4909)) | rwb-case (P3) | P3 rwb-case | The answer carrying `LOT_WITH_COMMITTEE`, `LOT_APPROVED` or `LOT_WITHDRAWN` with the rule and its version; on the workflow boundary the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter, a breaker per downstream and no retry of its own (ADR-020). The five rows are class C contract dependencies that the plan's C row does not carry, so they are built against their documents and fakes on Day 1 (GAP-2981; ASM-4907).

#### 12.3 Events published

None. The service publishes one event, EV-23 `rwb.debtsale.LotAwarded.v1` (TSD S6 T5.3 `LotAwarded`), and it is the award story's; the approval step writes no outbox row and holds no producer of its own (ASM-4910).

#### 12.4 Events consumed

None. The approval answer arrives on the chain this story starts and on the rwb-case contract, not on a topic; this story holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per case per stage, the saga child of `CaseWorkflow` | `rwb-debtsale` | Input: the case, the lot, the reserve, the tiered terms and the package in force; signals: the approval answer and the case state |
| Committee steps inside `DebtSaleWorkflow` | Steps of the catalogued workflow, from the priced lot to the committee's answer (no separate workflow) | `rwb-debtsale` | Applies R-DS-04 (its priced-lot step is built by RWB-S6-E5024-APP and approved here under RWB-S6-E6001-APP), starts the child approval, applies R-DS-06, R-DS-07 or R-DS-08 and reports the stage outcome |
| `ApprovalWorkflow` | Child workflow, the kit's Approval template, owned and run by rwb-decision | `rwb-decision` (P7) | The maker-checker chain with the DoA lookup as a parameter; started here, owned by P7 (GAP-2980); this story holds the correlation record and confirms the child input, correlation and return signal with rwb-decision before the contract is tagged (GAP-1964) |
| `recordCommitteeApproval` | Activity, the one step of this story | `rwb-debtsale` | The case, the lot and the answer in; the rule ID with its version, the three approval columns (the approval is a case route state, not a LOV-LOT-STATUS value), the record and the move out, in one transaction |

No child workflow for the case and no workflow for the money exists here. R-DS-23 (the award, the sale agreement and the notices, with the move to LOT_AWARDED) is RWB-S6-E6006-APP's and is not built here (GAP-2994). The activity name is a target design choice of this story; the trigger is the arrival of the priced lot, because the FSD declares no background event for the feature (FSD S6 A2.5.4.4).

Workflow ID form: Not specified in the source documents (CG-ALL-10434). Start rule: the catalog trigger reads 'The monthly sale cycle opens, or a residual arrives from disposal (R-DS-01)'; the start or signalWithStart choice and the duplicate-start policy are Not specified in the source documents (CG-ALL-10434). The operation names of the P7 decide act, the DS rule-package read and the case-move answer are Not specified in the source documents (GAP-2980) and carry the section R9 placeholder until rwb-decision and rwb-case publish them.

#### 12.6 Schedules

None. The step runs from the priced lot and from the answer, and owns no Temporal Schedule and no legacy job. No job of the architecture's job list is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot; this story updates `approval_authority`, `payment_terms` and, where the answer carries it, `signing_date` |
| debt_sale_account | S6 (`rwb_debtsale`) | The accounts of the lot; read for the answer of API-S6-002, written only by the lot-building stories |
| decision_record | PLT library, in `rwb_debtsale` | The local hash-linked decision record (DP-03) |
| idempotency_key | PLT library, in `rwb_debtsale` | The key of the repeated answer and the outcome it holds |
| outbox_event | PLT library, in `rwb_debtsale` | Created by the library; this step writes no row of it (12.3) |

Not owned and never read as a table: `recovery_case` (P3), `approval`, `decision_log_entry` and `rule_row` (P7), `delegation_limit` (P4), `document` (P5), `notice` (P6), `proceeds` (P8) and every `v_ace_*` view (P1). No foreign key leaves the schema and `buyer_partner_id` is an identifier, not a cross-schema foreign key (DP-01). Reads of ACE data go through the rwb-source-data contract, which returns the source field names v_ace_score.*, v_ace_account.* and v_ace_batch_status.*; no view and no ACE table is read here. The path is confirmed with P1 (REST for the screen, activity inside the workflow); the timing of that confirmation is Not specified in the source documents (GAP-1770).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision approval-chain fake | The chain of `LOT-2027-000041` for `RC-2027-000611`: decided inside the delegation, decided outside it, returned for a raised reserve, and refused; no answer beyond 2 s | AC1, AC2, AC4, X4, X5 |
| rwb-decision rule-package fake | The DS package at its version with R-DS-04, R-DS-06, R-DS-07, R-DS-08 and the who-approves rows | AC1, AC2, AC3 |
| rwb-access DoA fake | The `delegation_limit` rows that let a level approve the reserve and the terms, and a level whose limit is below the reserve; no answer beyond 2 s | AC2, X4, X5 |
| rwb-case state fake | The states `LOT_BUILT`, `LOT_WITH_COMMITTEE`, `LOT_APPROVED` and `LOT_WITHDRAWN` of the case; a case in a state the rule does not name | AC1, AC2, AC3, X3 |
| rwb-case case-move fake | The three moves accepted, and a move refused because the case is not in the expected state | AC2, AC3, X3 |
| Local decision-record stub (RWB-PLT-E1027-CON) | A healthy chain, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-25 and SCR-26 answer for the lot, with the lot facts read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished names of the rule-package read and of the case-move answer are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2980; ASM-4909).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | The lot read on `/api/recovery/debtsale/v1`; the approval chain, the rule package, the DoA read, the case read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-23 `LotAwarded` is the award story's; this step holds no producer and no consumer |
| Temporal | 1 workflow, 1 branch, 1 activity, 1 child workflow | `DebtSaleWorkflow` and its committee branch on `rwb-debtsale`, `recordCommitteeApproval`, and the P7 child on `rwb-decision`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `approval`, package `th.co.scb.ace.workbench.recovery.debtsale.approval`; front end `src/modules/recovery/debtsale/DebtSaleLotApproval.tsx`, the fragment SCR-25 and SCR-26 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the lot update commit together or not at all. DP-13 moves the base of the read. DP-19 is how SCR-25 and SCR-26 reach the service. No other pattern is claimed: the approval chain, the DoA limit and the case state are consumed contracts, so DP-08 and DP-09 stay off this table.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` committee branch | Workflow | Waits for the priced lot, submits it, loads the package, applies the answer and reports the outcome |
| `recordCommitteeApproval` | Activity | The one step: read the case, evaluate the rules, write the record and the columns, answer the move |
| `CommitteeApprovalEvaluator` | Service | Rule evaluation against the package version in force, thresholds as package values |
| `CommitteeDecisionClient` | Client | The chain of rwb-decision: start the child approval, read the answer, read the package version; one hop, 2 s |
| `DoaLimitClient` | Client | The `delegation_limit` read for the approver's level |
| `DebtSaleDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and version before any change, and refuses the step when the write fails |
| `DebtSaleApprovalWriter` | Repository | Updates the three columns in one transaction with the idempotency row and the optimistic lock |
| `CaseStateClient` | Client | The case read and the case-move answer |
| `DebtSaleLotController` | Controller | The lot read, the right, the scope and the problem mapping |
| `DebtSaleLotApproval` | React component | Shows the lot, its reserve, its terms and its approval outcome on SCR-25 and SCR-26, with the refusal and failed-record states |

**Database and migrations.** No Flyway file. The two tables arrive with the DB story of this service and the record, the idempotency key and the outbox are library objects created by the library's migration. No column is added: the three approved columns already exist as DF-SAL-027 to DF-SAL-029.

**Configuration and reference data.** `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` at their version (TSD S6 T3.2); the DS package and its version, authored and approved in rwb-decision; the who-approves rows, the 45-day turnaround target and the timers as package and reference values, not code.

**Tests.** Unit tests of the evaluator per rule and per outcome; component tests of the writer, the client and the controller; contract tests against the CON fakes; the legacy test cases below at component and integration level.

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. | An account with an open deviation is presented in the lot; raised by the eligibility and lot-build step and shown on the approval view |
| MSG-GEN-001 | Error | Enter {field}. | A required field of the lot or of the answer is empty (VR-S6-005-1) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | The role does not hold the right of the read (X2; FSD A2.5.4.3) |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The decision record cannot be written (AC4, X1) |

Validation follows the order of the step: the right and the scope, the required fields, the case state, the rule, the record, the rows, the answer. The messages are the legacy messages of RWB-E6-001 and of the FSD, copied unchanged; this story invents none.

### 15. Screens and states

| Screen | States | What this story puts there |
|---|---|---|
| SCR-25 Lot builder | Draft; priced; approved; empty, loading, error, no access: Not specified in the source documents (CG-ALL-10440) | The lot, its segment, its cut-off date, its reserve, its tiered terms and its approval authority, read on API-S6-002; the approved state is the R-DS-06 outcome |
| SCR-26 Award | Open; closed; awarded; transferred; empty, loading, error, no access: Not specified in the source documents (CG-ALL-10441) | The lot and its approved reserve and terms as the award view reads them; the award act itself is the award story's; API-S6-003, its AwardRequest and its DecisionLogEntry answer are RWB-S6-E6005-APP's, and so is the A right (GAP-1966) |

The screens reach the service through the gateway-bff composite route and call no service directly (DP-19). The approval act is taken on the P7 approval path, not on a screen of this service. The refusal and the failed-record states are shown with MSG-P4-002 and MSG-P7-003, and nothing on the screen changes when either fires.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-001-01 | AC1 | Component | Synthetic lot with accounts, reserve and terms, case in `LOT_WITH_COMMITTEE`, package in force |
| TC-E6-001-02 | AC2 | Component | The same lot, an approval decided inside the delegation, the DoA row of the level |
| TC-E6-001-03 | AC3 | Component | The same lot priced, case in `LOT_BUILT`, R-DS-04 in force |
| TC-E6-001-04 | AC4 | Component | The same lot with the decision-record stub stopped |
| TC-E6-001-05 | Access | Component | A caller whose role holds no Debt sale right |
| TC-E6-001-06 | Principle 5 | Component | A forced decision-record write failure on an otherwise valid answer |
| TC-E6-001-07 | §12 operations, events and activities | Contract | Contract check of the operations, events and activities of §12 against the API and catalog |
| TC-E6-001-08 | §12.7 tables (ASM-3438) | Component | Boundary values of each table of §12.7 |
| TC-E6-001-09 | AC5 | Component | A service identity holding the grants of this story and a statement naming `rwb_decision`, `rwb_access`, `rwb_case` or another service's schema |
| TC-E6-001-10 | AC6 | Component | A case in `LOT_BUILT` and a status change the rule table does not allow |
| TC-E6-001-11 | AC7 | Component | The same lot approved by committee inside the delegation, the DoA row of the level, and the write captured |
| TC-E6-001-12 | AC8 | Component | A caller without a valid token, a caller with no Debt sale right, and a lot that does not exist |
| TC-E6-001-13 | AC9 | Component | Not specified in the source documents (NEWAC-RWB-S6-E6001-APP-AC8) |
| TC-E6-001-14 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-S6-E6001-APP-AC9) |

TC-E6-001-01 to TC-E6-001-06 are the legacy test cases of RWB-E6-001, kept by ID with the level column added. The integration copies of the two cross-service cases, `TC-E6-001-01-ITG` and `TC-E6-001-02-ITG`, are the wave 4 harness's and are not built here.

### 17. Guardrails

- No business value in code: the reserve, the terms, the who-approves rows, the list values and the timers are reference data or rule rows read with their version.
- No personal data in the schema, the decision record, the logs, the workflow inputs or the answers; test data is synthetic.
- ACE data only through the owner's contract or `v_ace_*` views; this service reads no ACE view and no other service's table (DP-01, DP-02).
- One hop per call, 2 s, no retry of its own, a breaker per downstream.
- No decision without a record: the record and the change commit together or not at all.
- Every answer carries the rule ID, its version and the decided-at time; no rule is applied without its version.
- The service identity holds no grant outside `rwb_debtsale`; a boundary test fails the build on a cross-schema statement.

### 18. Traceability

| L3 process | Legacy | Legacy AC | Legacy TC | New story | New AC | Requirement |
|---|---|---|---|---|---|---|
| Not specified in the source documents (DOR-RWB-S6-E6001-APP-2) | RWB-E6-001 | AC1 | TC-E6-001-01 | RWB-S6-E6001-APP | AC1 | REQ-S6-004 (FSD S6 A2.5) |
| Not specified in the source documents (DOR-RWB-S6-E6001-APP-2) | RWB-E6-001 | AC2 | TC-E6-001-02 | RWB-S6-E6001-APP | AC2 | REQ-S6-005 |
| Not specified in the source documents (DOR-RWB-S6-E6001-APP-2) | RWB-E6-001 | AC3 | TC-E6-001-03 | RWB-S6-E6001-APP | AC3 | REQ-S6-006 |
| Not specified in the source documents (DOR-RWB-S6-E6001-APP-2) | RWB-E6-001 | AC4 | TC-E6-001-04 | RWB-S6-E6001-APP | AC4 | REQ-S6-007 |
| Not specified in the source documents (DOR-RWB-S6-E6001-APP-2) | RWB-E6-001 | Access | TC-E6-001-05 | RWB-S6-E6001-APP | AC1 | REQ-S6-008 |
| Not specified in the source documents (DOR-RWB-S6-E6001-APP-2) | RWB-E6-001 | Principle 5 | TC-E6-001-06 | RWB-S6-E6001-APP | AC4 | REQ-S6-009 |

Feature FEAT-DBS-05 of the FSD S6 (A2.5); epic E6 of the story master; business epic EP06; service epic RWB-SVC-S6; PRD reference Pending (C1). The requirement IDs are the TSD S6 T8 rows that name FEAT-DBS-05.

### 19. Out of scope

- The award operation API-S6-003, its request, its answer and its event; the award story owns them.
- The lot build, the price estimate, the COLLINS read and the reserve price; the lot-building stories own them.
- The approval chain, the approver's act, the approval rows, the decision log and the rule package; rwb-decision owns them.
- The DoA table and the delegation limits; rwb-access owns them.
- The case of record, its route states and the parent `CaseWorkflow`; rwb-case owns them.
- The data room, the tape, the bids and the buyer qualification; the other S6 keys own them.
- The document, its custody and its retention, and the customer notices; rwb-document and rwb-comms own them.
- The deployment, the configuration of the environments and the wave 4 harness; the operations story of this key and the integration epics own them.
