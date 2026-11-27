# RWB-S6-E6005-APP Award the lot and test the price

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S6-I |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E6005-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the award slice of RWB-E6-005 split out for rwb-debtsale. The four legacy acceptance criteria are kept word for word with their origin tag; the price test, the award route and the winning buyer are now the award branch of `DebtSaleWorkflow` on task queue `rwb-debtsale`, which applies R-DS-19 and R-DS-20 of the DS package, tests the best bid against the reserve and the 54 percent cap, asks the P4 DoA limit and, where the limit requires it, the P7 approval chain, records the decision through the local decision-record library before the lot row changes (DP-03), reads the model score through the rwb-source-data contract (DP-05), writes `buyer_partner_id` and `buyer_class`, publishes `rwb.debtsale.LotAwarded.v1` (EV-23), answers rwb-case for `AWARD_PENDING` and serves API-S6-003 on base `/api/recovery/debtsale/v1` (DP-13) through the gateway-bff composite route (DP-19). The plan's C row is empty although four services are consumed, and DP-09 is absent although the step publishes (GAP-2990, GAP-2991; ASM-4938, ASM-4939). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E6005-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Debt sale officer**, I want **to compare the best bid to the reserve and the model, and award with the approval the limit requires**, so that **debt sales run on approved lots and masked data**.

This is the award slice of legacy RWB-E6-005. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag;
- the award branch of `DebtSaleWorkflow` on queue `rwb-debtsale` in namespace `rwb-recovery`, the saga child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-DS-19 and R-DS-20 on the bidding-window close, with the DS package version in force, and the price test against the reserve and the 54 percent cap;
- the DoA test of the award and, where the officer's limit requires it, the P7 approval chain started as a kit child workflow;
- the write of `buyer_partner_id` (DF-SAL-025) and `buyer_class` (DF-SAL-026) on `debt_sale_lot` in `rwb_debtsale`, and of no other lot column;
- one decision record per award outcome, written before the row changes (DP-03);
- the answer to rwb-case for `AWARD_PENDING` and `BID_BELOW_RESERVE`, with the rule and its version;
- the publication of `rwb.debtsale.LotAwarded.v1` (EV-23) from the outbox, with no personal data;
- API-S6-003 `POST /debt-sale-lots/{lotId}/award` on base `/api/recovery/debtsale/v1`, its `AwardRequest` and its `DecisionLogEntry` answer, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the operation, the elements, the closed lists, the consumed rows, the error set and the fakes, which are RWB-S6-E6005-CON; the lot build, the pricing estimate and R-DS-04's effect, which are RWB-S6-E5024-APP's and the committee story's; the committee approval of the reserve and the tiered terms, which is RWB-S6-E6001-APP's; the sale agreement, the customer notices and the move to `LOT_AWARDED` under R-DS-23, which are RWB-S6-E6006-APP's; the bids and the data room, which are RWB-S6-E5026-APP's; the buyer qualification, which is RWB-S6-E6002-APP's; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the rule package, the approval chain and the ledger, which are rwb-decision's (P7); the DoA table, which is rwb-access's (P4); the model score, which is rwb-source-data's (P1); the transfer of the data to the buyer, which is RWB-S6-E6007-APP's; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E6-005 gave the Workbench one step in which the officer compared the best bid to the reserve and the model and awarded with the approval the limit required. The FSD keeps the objective and the metric unchanged: "Compares the best bid to the reserve and the model, and awards with the approval the limit requires", against a debt sale turnaround of 45 days measured on the decision log and the Workbench records and reviewed monthly (FSD S6 A2.9.1). The problem is unchanged (debt sales run on spreadsheets with no baseline turnaround), and the programme keeps the requirement: REQ-S6-006, "The award of a lot is approved and recorded with the price achieved against the reserve" (Must, E6).

What D-RCV-60 changes is where each fact lives:

- **the lot and the winning buyer are this service's.** `debt_sale_lot` and `debt_sale_account` are S6's tables in `rwb_debtsale` (context pack, Ownership rows; TSD S6 T3.1), so `buyer_partner_id` and `buyer_class` are written here and nowhere else.
- **the price test is a rule of the DS package.** R-DS-19 and R-DS-20 are rows of the Debt sale route set (41 rules, package Phase 2), governed in rwb-decision and evaluated in this service's activity, never in workflow code (Temporal and Drools Design slides 5, 12 and 13).
- **the approval is not this service's.** Where the award exceeds the officer's DoA limit, the chain is the kit's `ApprovalWorkflow` on the P7 queue under the P4 `delegation_limit` row; this story asks and reads the answer and writes no approval row and no ledger entry (GAP-2990).
- **the model score is read, not queried.** The legacy step read `v_ace_score`; in the target the 30 `recovery.v_ace_*` views are read by rwb-source-data alone, so the score and its model version arrive on that owner's contract (DP-05), and rwb-debtsale holds no view grant.
- **the case of record stays with rwb-case (P3).** `BIDS_RECEIVED`, `AWARD_PENDING` and `BID_BELOW_RESERVE` are case route states; this story evaluates the rule and answers the move.
- **the decision is recorded first**, through the DP-03 library in the same transaction as the lot change, which is what legacy AC1 and AC4 require.
- **the award is published once.** The service's topic carries `LotAwarded` (EV-23), consumed by rwb-payment and rwb-reporting (context pack, slide 13 matrix); the payload carries identifiers, codes and a rule version only.
- **the confirmation is the next story's.** R-DS-23 confirms the award, generates the agreement and the notices and moves the case to `LOT_AWARDED` under RWB-S6-E6006-APP; the lot keeps `OFFERED` until then (GAP-2994).

The delivery is the plan's: this key is EP06 and therefore wave 4 with release 30 April 2027, while rwb-debtsale is created in wave 3, so the date is copied unchanged and marked tentative (GAP-2993; ASM-4940).

### 3. Preconditions

- RWB-S6-E6005-CON is published: API-S6-003, `AwardRequest`, the `DecisionLogEntry` answer, the event schema, the consumed rows, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-case state read and the case-move answer are available for the fake. No source publishes an operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies, and the operation name is Not specified in the source documents (GAP-2990; ASM-4938).
- The rwb-decision DS package read is available for the fake with R-DS-19, R-DS-20 and the 54 percent cap as a rule value; the operation name is Not specified in the source documents (GAP-2990; ASM-4938).
- The rwb-decision approval chain is available for the fake: `GET /approvals` and `POST /approvals/{approvalId}/approve`, `/return`, `/refuse`; the chain, the act and the ledger stay with P7.
- The rwb-access DoA read is available for the fake: the `delegation_limit` rows of P4 (`GET /doa-limits`), which the award is tested against.
- The rwb-source-data model-score read is available for the fake; the operation name and the field IDs of the data product are Not specified in the source documents (GAP-2995; ASM-4942).
- RWB-PLT-E1027-CON is published with its writer fake: the decision record is written in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037; this story adds no table, no column and no migration.
- The DS rule package is in force at its version with R-DS-19 and R-DS-20; the package is authored, tested and approved in rwb-decision.
- The service runs as its own login on `rwb_debtsale`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on another schema is refused by the database and fails the boundary test (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E6005-CON when its tests pass.

### 4. Flow

1. The bidding window closes on a lot whose case is in `BIDS_RECEIVED`; the bids were taken on API-S6-005 by the data-room step, which this story does not build.
2. The award branch of `DebtSaleWorkflow` on queue `rwb-debtsale` receives the lot reference and reads the lot and its accounts from `debt_sale_lot` and `debt_sale_account` in `rwb_debtsale`, and the case state on the rwb-case contract, read only, one hop, 2 s.
3. The branch reads the DS package version in force from rwb-decision and the model score on the rwb-source-data contract (DP-05), so the price test can compare the best bid to the reserve and the model.
4. `AwardPriceEvaluator` applies R-DS-19 when the best bid is at or above the reserve: it tests the price against the reserve and the 54 percent cap and routes the award. R-DS-20 fires when the best bid is below the reserve and routes the below-reserve outcome to the committee instead.
5. The award is tested against the officer's DoA limit on the rwb-access `delegation_limit` read. Where the limit requires an approval, the branch starts the kit child `ApprovalWorkflow` on the P7 queue and waits; where it does not, the step continues without a chain.
6. `DebtSaleDecisionRecordWriter` writes one decision record through the local library, **before any change**: the case reference, the lot reference, the best-bid reference, the rule ID with its package version, the model version, the DoA level, the outcome and the case move. A failed write stops the step with nothing changed (DP-03).
7. `DebtSaleAwardWriter` updates the `debt_sale_lot` row in one `rwb_debtsale` transaction with the decision record, the idempotency row and the optimistic lock of `version`: `buyer_partner_id` (DF-SAL-025) and `buyer_class` (DF-SAL-026). `reserve_price`, `status`, `signing_date`, `approval_authority` and `payment_terms` are not written here.
8. `LotAwardedWriter` writes one outbox row in the same transaction for `rwb.debtsale.LotAwarded.v1` on topic `rwb.debtsale.events.v1`, with the CloudEvents envelope and no personal data (DP-09 as an absent plan row, GAP-2991).
9. `CaseMoveAnswer` answers rwb-case with `AWARD_PENDING` (R-DS-19) or `BID_BELOW_RESERVE` (R-DS-20), the rule ID, the version and the decided-at time. rwb-case writes the case row; this service writes neither.
10. A repeated award for the same lot, decision and `Idempotency-Key` writes nothing, publishes no second event, answers no second move and counts the repeat.
11. SCR-26 Award in its open and closed states reads the lot, its reserve, the bids and the award decision through the gateway-bff composite route on API-S6-002 and API-S6-003, next to the approval rows of rwb-decision (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no lot column, no outbox row and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E6-005-04, TC-E6-005-06 |
| X2 | The role does not hold the Debt sale A right | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E6-005-05 |
| X3 | The case is not in `BIDS_RECEIVED`, or the lot has no bid | 409 and nothing is written; the step is not re-evaluated on a case that has already moved | None | AC2 |
| X4 | The best bid is below the reserve | R-DS-19 does not fire; R-DS-20 fires, the award is not recorded and the below-reserve outcome is answered | None | AC2 |
| X5 | The award is above the officer's DoA limit and the chain is refused or returns | R-DS-19's award is not recorded, the lot keeps its columns and the refusal is recorded on the P7 chain | None | AC1 |
| X6 | A consumed contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's schedule; nothing is written, no event is published and the caller sees 503 with the platform error envelope | None | AC1, AC2 |
| X7 | The same award is repeated for the same lot and key | One record, one update, one event and one case-move answer; the repeat is counted | None | AC1 |
| X8 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or another service's table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17 |

X1 to X4 are the exception paths of RWB-E6-005 carried onto the split, X5 to X7 are the paths the target approval boundary and the call types add, and X8 is the DP-01, DP-02 boundary. The cap and the DoA limits are values in force in the package and the DoA table, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E6005-CON, the rwb-case, rwb-decision, rwb-access and rwb-source-data fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P4 or P7 |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screen, the operation and the lot columns are fixed |
| Valuable | A lot is priced against the reserve and the model, awarded inside the officer's limit, recorded and published once, and read as awarded by the case and the screen |
| Estimable | One workflow branch, one evaluator, one DoA client, one optional approval client, one score client, one record write, one row update, one outbox write, one case-move answer and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots and bids through the contract fakes, plus the access, below-reserve and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Award the lot and test the price

  Background:
    Given lot "LOT-2027-000041" carries accounts, a reserve price and a best bid for case "RC-2027-000611"
    Given the DS rule package is in force at its version and carries R-DS-19 and R-DS-20
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Award the lot and test the price (legacy RWB-E6-005 AC1)
    Given the rwb-decision contract mock returns the DS package in force with R-DS-19 and the 54 percent cap
    Given the rwb-access contract mock returns the DoA limit that lets the officer award the lot
    Given the rwb-source-data contract mock returns the model score of lot "LOT-2027-000041"
    Given the rwb-case contract mock returns the case state "BIDS_RECEIVED" for "RC-2027-000611"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then compares the best bid to the reserve and the model, and awards with the approval the limit requires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-19 (legacy RWB-E6-005 AC2)
    Given the rwb-case contract mock returns the case state "BIDS_RECEIVED" for "RC-2027-000611"
    Given the rwb-decision contract mock returns R-DS-19 with the 54 percent cap
    Given the rwb-source-data contract mock returns the model score and the best bid of lot "LOT-2027-000041"
    Given a case in state BIDS_RECEIVED
    When bidding window closed
    Then test the price against the reserve and the 54 percent cap, and route the award
    Then the case moves to AWARD_PENDING

  Scenario: AC3 Rule R-DS-04 (legacy RWB-E6-005 AC3)
    Given the rwb-decision contract mock returns the DS package in force with R-DS-04
    Given the rwb-source-data contract mock returns the COLLINS estimate of lot "LOT-2027-000041"
    Given a case in state LOT_BUILT
    When lot priced
    Then propose the lots, the tiered buyer terms and the reserve price
    Then the case moves to LOT_WITH_COMMITTEE

  Scenario: AC4 Not recorded (legacy RWB-E6-005 AC4)
    Given the rwb-decision contract mock returns the DS package in force with R-DS-19
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E6-005 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the user acts on the screen`, `bidding window closed`, `lot priced`, `the action is taken` and `the decision log cannot be written` all stand. The `Given the <service> contract mock returns <x>` lines are the only additions, one to four per criterion. What the legacy lines describe happens in four places in the target: rwb-decision owns the package, the approval chain and the ledger; rwb-access owns the DoA limit; rwb-source-data owns the model score; rwb-case owns the route states and applies the move this story answers; and this story evaluates R-DS-19 and R-DS-20, writes the winning buyer, records the decision and publishes `LotAwarded`. Two boundaries are recorded rather than smoothed over. AC3's rule R-DS-04 is the priced-lot step: this story carries the criterion word for word because the legacy key owns it, but its effect is the lot that RWB-S6-E5024-APP builds and RWB-S6-E6001-APP approves, so no field of that step is claimed here (GAP-2994; ASM-4941). AC1's "approval the limit requires" is the P4 DoA test and the P7 chain, while R-DS-23's confirmation and the move to `LOT_AWARDED` are RWB-S6-E6006-APP's (GAP-2994; ASM-4941).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-19 | Debt sale | D8.4 | BIDS_RECEIVED | BIDDING_WINDOW_CLOSED | best_bid at or above reserve_price | Test the price against the reserve and the 54 percent cap, and route the award | AWARD_PENDING | Debt sale officer | Case Workspace, Committee View | 2 working days |
| R-DS-20 | Debt sale | D8.4 | BIDS_RECEIVED | BEST_BID_BELOW_RESERVE | best_bid below reserve_price | Raise the below-reserve outcome to the committee | BID_BELOW_RESERVE | Debt sale officer | Committee View | None |
| R-DS-04 | Debt sale | D8.4 | LOT_BUILT | LOT_PRICED | lot agent estimate returned with COLLINS | Propose the lots, the tiered buyer terms and the reserve price | LOT_WITH_COMMITTEE | Committee | Agent Runtime, COLLINS, Case Workspace | 5 working days |
| R-DS-23 | Debt sale | D8.4 | AWARD_PENDING | AWARD_CONFIRMED | price tested against the reserve and the 54 percent cap, and recorded | Award the lot and generate the sale agreement and the customer notices | LOT_AWARDED | Debt sale officer | Document Hub, buyer portal | None |

The four rows are copied character for character from the Business Rules and Routing Logic v4. Their owner column is a business role, not a service: this story evaluates R-DS-19 and R-DS-20, the case moves are answered to rwb-case, the DoA limit is P4's, and the approval and the ledger are P7's. R-DS-04 is tabled because legacy AC3 owns it and because the priced lot is this story's input; its effect is built by RWB-S6-E5024-APP and approved by RWB-S6-E6001-APP. R-DS-23 is tabled because it follows this step in the same machine and belongs to RWB-S6-E6006-APP (GAP-2994).

| ID | Rule | Source |
|---|---|---|
| BR1 | `buyer_partner_id` and `buyer_class` are columns of `debt_sale_lot` in `rwb_debtsale`, and no other service writes them | Architecture v5 slide 41; TSD S6 T3.1; context pack Ownership rows |
| BR2 | The decision is recorded before the lot row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2; legacy AC1 and AC4 |
| BR3 | The award is tested against the DoA limit of rwb-access and, above it, approved on the P7 chain; this service writes no approval row and no ledger entry | DP-03; context pack slide 13; GAP-2990 |
| BR4 | The model score is read on the rwb-source-data contract; rwb-debtsale holds no `v_ace_*` grant and reads no ACE table | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2995 |
| BR5 | The case move is answered and not written: `BIDS_RECEIVED`, `AWARD_PENDING` and `BID_BELOW_RESERVE` are rwb-case's | Ownership Map `recovery_case` owner P3; GAP-2990 |
| BR6 | The lot status is not passed by this step: the lot stays `OFFERED` until R-DS-23 sets `AWARDED` under RWB-S6-E6006-APP | TSD S6 T3.2 and T4; GAP-2994 |
| BR7 | The 54 percent cap, the reserve and the DoA limits are values in force in the DS package and the P4 table, read with their version; none is a constant of this build | FSD S6 A2.9.3.1 (BR-S6-009); Template and Rules v1 §R7.2 (s17) |
| BR8 | The award is published once per lot and decision on `rwb.debtsale.events.v1` as `rwb.debtsale.LotAwarded.v1`, with no personal data | TSD S6 T5.3; context pack slide 13; DP-09 |
| BR9 | The same award twice, or the same `Idempotency-Key` twice, writes once, publishes once and answers once | TSD S6 T-A.2; Architecture v5 slide 11 |
| BR10 | No person name, contact value or identity number enters `rwb_debtsale`, the decision record, a log, the event or a workflow input | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR5). The lot's own status is this service's, but this step does not pass it (BR6).

| From (case route state) | Event | Condition | To |
|---|---|---|---|
| `BIDS_RECEIVED` | `BIDDING_WINDOW_CLOSED` under R-DS-19 | best_bid at or above reserve_price | `AWARD_PENDING`, with the winning buyer written |
| `BIDS_RECEIVED` | `BEST_BID_BELOW_RESERVE` under R-DS-20 | best_bid below reserve_price | `BID_BELOW_RESERVE`, with no buyer written |
| `AWARD_PENDING` | `AWARD_CONFIRMED` under R-DS-23 | price tested against the reserve and the 54 percent cap, and recorded | `LOT_AWARDED` under RWB-S6-E6006-APP |
| Any state the rule does not name | Any award for the same lot | X3, X4 | Unchanged, the repeat or the exception is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The bidding window closes for a case in `BIDS_RECEIVED` | The package in force is loaded | Evaluating |
| Evaluating | R-DS-19 fires and the DoA test passes or the chain approves | The award is recorded | Applying |
| Applying | The decision record, the lot columns, the outbox row and the case-move answer are written | The transaction commits | Waiting for the confirmation |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |

`LOV-LOT-STATUS` is BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED (TSD S6 T3.2); the lot is `OFFERED` at the award and becomes `AWARDED` only under R-DS-23. The route states above are the DEBTSALE machine of TSD S6 T4 and the legacy criteria, and they live on the case of record.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: reads the lot and its bids, runs the price test and awards inside the DoA limit |
| RW-PRODHEAD, product head | Debt sale RA: reads the lot and awards where the DoA table names the level |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: reads the lot and awards where the DoA table names the level |
| RW-SALEOFF, sale officer | Debt sale R: reads the lot and its award outcome |
| RW-NPAMGR, NPA and asset manager | Debt sale R: reads the lot and its award outcome |
| RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Debt sale R: read only, in scope |
| PT-BUYER, PT-RAMC | No right on this operation: the partner sees its own lot and its own bids in the data room through the partner gateway, never the award decision |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R: the service identities run the step and are subject to the same checks |
| rwb-debtsale service identity | Runs the branch, evaluates the rules, writes the decision record, the buyer columns and the outbox row, and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S6 T6.1 and the two legacy Permission checks rows. The legacy table gives the A right to RW-DEBTSALE, RW-PRODHEAD and RW-HEADASL, which T6.1 gives as CRUA and RA. Above the officer's limit the act is an approval-chain answer under the P4 DoA limit, not a wider Workbench right, and this story writes no approval row (GAP-2990; ASM-4938).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read, the lot reference of the row, the record and the event |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Read, shown on the award view and carried in the event |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Read |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Read, against `LOV-SEGMENT` |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Read, the price the best bid is tested against; never written here |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Write, the winning buyer of the award |
| DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_class | Write, against `LOV-BUYER-CLASS` |
| DF-SAL-027 to DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date, approval_authority, payment_terms, status | Read; not written here (BR6, RWB-S6-E6001-APP and RWB-S6-E6006-APP write them) |
| DF-SAL-031 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code, outstanding, selling_price, put_back_status | Read only, as the accounts of the lot; no account write in this story |
| Standard columns | debt_sale_lot (S6, `rwb_debtsale`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write `updated_at`, `updated_by` and the optimistic lock of `version` on the update |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, model version, inputs reference, outcome, decided at | Write through the local library, before the lot row changes |
| `delegation_limit` | delegation_limit (P4, `rwb_access`) | the DoA limit of the officer's level | Not read as a table: the limit arrives on the rwb-access contract (GAP-2990) |
| score data product | rwb-source-data (P1) | score_key, account_key, model_code, model_version, score_value, estimate_value | Not read as a table or view: the score arrives on the rwb-source-data contract (DP-05; GAP-2995) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case read and the move is answered (GAP-2990) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, from_state, event_code and the rest | Not read as a table: the rule rows are governed in rwb-decision and loaded here as the package in force |
| bid and award price | no column in TSD S6 T3.1 | the best bid amount, its time and the price achieved | Not specified in the source documents (GAP-2995; ASM-4942) |

Field IDs are those of TSD S6 v2 T3.1 and the Logical Data Model and Data Dictionary v9. The `recovery_case`, `rule_row` and `v_ace_score` rows are the rows the legacy Data table lists, with their owner moved to P3, P7 and P1 by the target. **No new table, no new column and no migration**: this story writes two existing lot columns and no account column, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_debtsale` by the library's own migration (DP-03, DP-09).

**No personal data.** The rows and the event carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_debtsale`, the decision record, a log, the event or a workflow input, and the test fixtures are synthetic. `borrower_code` and the account facts are read for the lot answer and are not copied into the event.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13). This story supplies the behaviour behind the one write whose shape is declared by RWB-S6-E6005-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/debt-sale-lots/{lotId}/award` | `AwardRequest` in, `DecisionLogEntry` of status 200 out (API-S6-003) | Debt sale, right A, scope applied | `Idempotency-Key` header |

The errors are 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope lot, 409 for a case or lot not in `BIDS_RECEIVED`, 422 for a missing or invalid field, and 503 when the decision library or a consumed contract does not answer (TSD S6 T-A.2). The operation ID is API-S6-003 of TSD S6 T-A.1 and is not redefined here. `POST /debt-sale-lots` (API-S6-001) and the data-room reads are sibling stories' and are neither built nor declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state `BIDS_RECEIVED` and the case reference; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2990; ASM-4938)) | rwb-case (P3) | P3 rwb-case | The answer that carries `AWARD_PENDING` or `BID_BELOW_RESERVE` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The read of the DS rule package version in force (operation name Not specified in the source documents (GAP-2990; ASM-4938)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows of R-DS-19, R-DS-20 and R-DS-04 with the 54 percent cap; faked |
| `GET /approvals` and `POST /approvals/{approvalId}/approve`, `/return`, `/refuse` | `/api/recovery/decision/v1` | P7 rwb-decision | The approval chain started above the DoA limit; the act is P7's and this story reads the answer; faked |
| `GET /doa-limits` | `/api/recovery/access/v1` | P4 rwb-access | The `delegation_limit` row of the officer's level, which the award is tested against; faked |
| The read of the model score and its model version (operation name Not specified in the source documents (GAP-2990; ASM-4938)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The score and estimate of the lot's accounts with their as-of date; DP-05; faked (field IDs Not specified in the source documents (GAP-2995; ASM-4942)) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter, a breaker per downstream and no retry of its own (ADR-020). The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-2990; ASM-4938).

#### 12.3 Events published

| Event | Topic | Envelope | Payload | Consumers |
|---|---|---|---|---|
| `rwb.debtsale.LotAwarded.v1` (EV-23, LotAwarded) | `rwb.debtsale.events.v1`, with its retry and `.dlt` topics | CloudEvents, from the outbox in the same transaction as the lot update | Lot id, lot_no, case reference, buyer_partner_id, buyer_class, decision reference, rule ID with its package version, awarded-at | rwb-payment (P8) and rwb-reporting (P9), which listen to this service's events (context pack slide 13) |

The event is published once per lot and decision, with no personal data: identifiers, codes, a date and a rule version only. DP-09 and its outbox library are absent from the plan's pattern set, and the absence is recorded (GAP-2991; ASM-4939).

#### 12.4 Events consumed

None. The S6 row of the connection matrix listens to rwb-payment (`ProceedsMatched`), which is the settlement fact of RWB-S6-E6011-APP's step, not the award; the bids arrive on API-S6-005 and the case state on the rwb-case contract. This story holds no consumer group, no subscription and no inbox row of its own, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per case per stage, the saga child of `CaseWorkflow`, pivot = transfer | `rwb-debtsale` in namespace `rwb-recovery` | Input: the lot, the case, the bidding-window result and the package in force; signals: the approval answer, the case state and the package version |
| The award branch of `DebtSaleWorkflow` | Workflow branch, from the closed bidding window to the award outcome | `rwb-debtsale` | Applies R-DS-19 or R-DS-20, tests the DoA limit, optionally starts the child approval, records and applies the award, reports the stage outcome |
| `ApprovalWorkflow` | Child workflow, the kit's Approval template, owned by rwb-decision and started on its queue where the DoA limit requires an approval | `rwb-decision` (P7) | The maker-checker chain with the DoA lookup as a parameter; started by this story, owned and run by P7 |
| `testAwardPrice` | Activity | `rwb-debtsale` | The lot, the bids and the package in; the rule ID with its version, the price-test outcome and the DoA test out |
| `recordAward` | Activity, the one write step | `rwb-debtsale` | The case, the lot and the award outcome in; the two lot columns, the decision record, the outbox row and the case move out, in one transaction |

The activity names are target design choices and are fixed by no source document. The trigger is the bidding-window close on a case in `BIDS_RECEIVED`, because the FSD declares no background event for the feature (FSD S6 A2.9.4.4).

#### 12.6 Schedules

None. The step runs from the bidding-window close and the approval answer, and owns no Temporal Schedule and no legacy Quartz job; the monthly sale cycle is the lot-building story's clock, not a Schedule of this step.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot; this story updates `buyer_partner_id` and `buyer_class` |
| debt_sale_account | S6 (`rwb_debtsale`) | The accounts of the lot; read for the price test and the answer, written by the lot-building stories |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated award and the outcome it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The outbox row of `LotAwarded`, written in the same transaction as the lot update (DP-09) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `approval`, `decision_log_entry` and `rule_row` (P7), `delegation_limit` (P4), `document` (P5), `notice` (P6), `proceeds` (P8), the score data product (P1) and every `v_ace_*` view (P1). No foreign key leaves the schema; `buyer_partner_id` and `account_id` are identifiers, not foreign keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | The case state `BIDS_RECEIVED` of case `RC-2027-000611`, the moves `AWARD_PENDING` and `BID_BELOW_RESERVE` accepted, and a move refused because the case is not in the state the rule expects | AC1, AC2, X3 |
| rwb-decision rule-package fake | The DS package at its version in force with R-DS-19, R-DS-20 and R-DS-04 and the 54 percent cap | AC1, AC2, AC3 |
| rwb-decision approval-chain fake | The chain of lot `LOT-2027-000041` decided inside and outside the DoA limit, and no answer beyond 2 s | AC1, X5 |
| rwb-access DoA fake | The `delegation_limit` rows that let the officer award, and a limit below the award | AC1, X5 |
| rwb-source-data score fake | The score and estimate of the lot's accounts with their model version and as-of date; no answer beyond 2 s | AC1, AC2, AC3, X6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-26 answer for lot `LOT-2027-000041`, with the lot facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished operation names and the score field IDs are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2990, GAP-2995; ASM-4938, ASM-4942).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | The award write on `/api/recovery/debtsale/v1`; the rwb-case state read and move answer, the rwb-decision package and approval chain, the rwb-access DoA read and the rwb-source-data score read; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.debtsale.LotAwarded.v1` on `rwb.debtsale.events.v1`; no consumed event at this step |
| Temporal | 1 workflow, 1 branch, 2 activities, 1 conditional child workflow | `DebtSaleWorkflow` and its award branch with `testAwardPrice` and `recordAward` on `rwb-debtsale`, and the P7 `ApprovalWorkflow` child when the DoA limit requires it; no Schedule |
| File | None | No file is read, built or delivered here; the tape and the data room pack are the data-room stories' |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `award`, Java package `th.co.scb.ace.workbench.recovery.debtsale.award`; front end `src/modules/recovery/debtsale/DebtSaleAward.tsx`, the fragment SCR-26 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the lot update commit together or not at all, and the failed write is MSG-P7-003. DP-05 replaces the legacy `v_ace_score` read with the rwb-source-data contract. DP-13 moves the base of the operation and nothing else. DP-19 is how SCR-26 reaches the service, one hop through the gateway. DP-09 is absent from the pattern set although this story publishes, and the absence is recorded rather than smoothed over (GAP-2991; ASM-4939).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` award branch | Workflow | Waits for the bidding-window close, tests the price, tests the limit, optionally starts the approval, applies the outcome and reports it to the parent |
| `testAwardPrice` | Activity | Reads the lot, the bids and the package, evaluates R-DS-19 or R-DS-20 and tests the DoA limit |
| `recordAward` | Activity | Writes the record, the two lot columns, the outbox row and the case-move answer in one transaction |
| `AwardPriceEvaluator` | Service | The rule evaluation over the DS package in force, with the cap, the reserve and the DoA values read as package and reference data |
| `DoaLimitClient` | Client | The `delegation_limit` read of rwb-access; one hop, 2 s, breaker |
| `ApprovalClient` | Client | The P7 chain start and the answer read; one hop, 2 s, breaker |
| `ScoreClient` | Client | The rwb-source-data score read with its as-of date and model version; DP-05 |
| `DebtSaleDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, and refuses the step when the write fails (DP-03) |
| `DebtSaleAwardWriter` | Repository | Updates the two lot columns in one `rwb_debtsale` transaction, with the idempotency row and the optimistic lock |
| `LotAwardedPublisher` | Outbox adapter | Writes the outbox row for `rwb.debtsale.LotAwarded.v1` in the same transaction |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case |
| `DebtSaleAwardController` | Controller | The award write, the capability area and right, the scope and the problem mapping of 401, 403, 404, 409, 422 and 503 |
| `DebtSaleAward` | React component | Shows the lot, its reserve, the bids and the award decision on SCR-26, with the refusal, below-reserve and failed-record states |

**Database and migrations.** No Flyway file. `debt_sale_lot` and `debt_sale_account` arrive with the DB story, and the decision record, the idempotency key and the outbox are library objects created in `rwb_debtsale` by the library's migration (DP-03, DP-09). No column is added for the award: `buyer_partner_id` and `buyer_class` already exist as DF-SAL-025 and DF-SAL-026.

**Configuration and reference data.**

- `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The DS package and its version, authored, tested and approved in rwb-decision; the 54 percent cap, the reserve rule and the 45-day target are values of the package, not of this build.
- The DoA limits are `delegation_limit` rows of rwb-access, read on its contract.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The award branch of `DebtSaleWorkflow` and its input record, registered on `rwb-debtsale` as the stage child of `CaseWorkflow`, with the bidding-window close as its trigger.
2. `CaseStateClient`, `DoaLimitClient`, `ApprovalClient` and `ScoreClient` against their fakes, with the 2 s budget and the breaker (AC1, AC2, X6).
3. `AwardPriceEvaluator` over the DS package with R-DS-19 and R-DS-20 and the below-reserve path (AC2, X4).
4. `DebtSaleDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `DebtSaleAwardWriter` and `LotAwardedPublisher` with the one transaction, the two columns, the idempotency row and the outbox row (AC2, X7).
6. `CaseMoveAnswer` with the two moves (AC2, X3).
7. `DebtSaleAwardController` with the rights, the scope and the problem mapping (AC1).
8. `DebtSaleAward` on SCR-26 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_debtsale`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_access` (X8, BR4, BR5).

**Feature flag.** `rwb.debtsale.award-v1`, read as a flag of the platform library; off means the branch holds the closed window, writes nothing, publishes nothing and answers no move, and the other stories of the service are unaffected.

**Done when.** The tests of section 16 pass, the branch runs from a synthetic closed bidding window in SIT, R-DS-19 and R-DS-20 each produce their record and their case-move answer, R-DS-19 writes the two lot columns and one `LotAwarded` event, the DoA limit and the approval answer are honoured, a repeated award writes once, a forced record failure changes nothing, no foreign table and no `v_ace_*` read exists in the build, and SCR-26 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the exclusion path of RWB-S6-E5023-APP, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the request is absent or invalid, or the award arrives without the bid, the reserve or the buyer (VR-S6-009-1) | Enter {field}. |
| MSG-P4-002 | A role without the Debt sale A right calls the award, or a role without the approval right of the chain tries the approval act (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are those of the legacy message set of this key and of FSD S6 A2.9.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S6-001 is carried because it is in the message set of the feature, and no path of this story raises it.

### 15. Screens and states

SCR-26 Award in its open and closed states is the screen of this step on the FSD reading — "Bids against the reserve and the award decision", first in E6 — and SCR-25 Lot builder provides the priced input the award works from. Both are served through the gateway-bff composite route (DP-19): the route calls rwb-debtsale for the lot, its reserve, its bids and its award decision, rwb-decision for the approval chain and the decision record, and rwb-case for the case and its route state. This story fixes the rwb-debtsale answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the closed bidding window with the price tested, the award held for approval above the limit, the award recorded with the winning buyer, and the below-reserve outcome. The refusal with MSG-P4-002 and the not-recorded state with MSG-P7-003 are shown on the same screen. The open, closed, awarded and transferred states of the legacy screen table are read as the case route state and the lot status together; the awarded and transferred states belong to RWB-S6-E6006-APP and RWB-S6-E6007-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-005-01 | AC1 | Component | The lot `LOT-2027-000041` of case `RC-2027-000611` with a best bid; the price test, the DoA test, the decision record, the two lot columns and the case move on the fakes |
| TC-E6-005-02 | AC2 | Integration | A case at `BIDS_RECEIVED` and the window closed; R-DS-19 fires, the price is tested against the reserve and the 54 percent cap, and the `AWARD_PENDING` move is asserted across the rwb-case, rwb-decision and rwb-source-data fakes |
| TC-E6-005-03 | AC3 | Component | A case at `LOT_BUILT` with the COLLINS estimate; the R-DS-04 row and the `LOT_WITH_COMMITTEE` shape are answered by the fakes, and no field of the priced lot is written here |
| TC-E6-005-04 | AC4 | Component | The decision-record stub stopped; nothing written, no event published, no move answered and MSG-P7-003 shown |
| TC-E6-005-05 | Access | Component | A role without the Debt sale A right; 403 with MSG-P4-002 and no read or write |
| TC-E6-005-06 | Principle 5 | Component | A forced decision log write failure at the moment of the lot update; no column changed, no event and no move |

The six legacy cases are the legacy cases of RWB-E6-005 in their legacy order, with the Level column added: `System` maps to `Component` where the step is tested on its fakes, and TC-E6-005-02 maps to `Integration` because it crosses the rwb-case, rwb-decision and rwb-source-data boundaries. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the 54 percent cap, the reserve rule, the 45-day target, the DoA limits, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_debtsale`, in a workflow input, in the event or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- The ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table or view, and a build that adds one fails the boundary test (DP-01, DP-05).
- The case stays with rwb-case, the approval and the ledger with rwb-decision, and the DoA table with rwb-access: no `recovery_case` row, no `approval` row, no ledger entry and no `delegation_limit` row is written here (BR3, BR5).
- The sale agreement, the notices and the move to `LOT_AWARDED` stay with RWB-S6-E6006-APP, and the transfer with RWB-S6-E6007-APP: this story declares neither (BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no data lake and no second topic.
- The decision is recorded before the change and the record, the lot update and the outbox row commit together; a build that writes the lot first fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S6-006 | The award of a lot is approved and recorded with the price achieved against the reserve (Must, E6; FSD S6); TSD S6 T8 maps REQ-S6-006 to FEAT-DBS-05 while the FSD gives the award as FEAT-DBS-09, and the difference is recorded (GAP-2994; ASM-4941) | The price test, the DoA limit, the two lot columns, the decision record and the case move | TC-E6-005-01, TC-E6-005-02 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the lot, the award and its columns | TC-E6-005-01 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E6-005-06 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `LotAwarded` outbox row and envelope | TC-E6-005-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget | TC-E6-005-02 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the change, with the ledger entry in P7 | TC-E6-005-04, TC-E6-005-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-005, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E6-005-01 to TC-E6-005-06 |
| Feature and screens | FEAT-DBS-09, SCR-26 Award and SCR-25 Lot builder |
| Rules | R-DS-19, R-DS-20, R-DS-04 and R-DS-23, from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |
| Source text | FSD S6 Debt sale v3 A2.9; TSD S6 Debt sale v2 T3.1, T3.2, T4, T5.3, T6.1 and T-A; legacy RWB-E6-005 |

### 19. Out of scope

- The published shape of the award operation, `AwardRequest`, the `DecisionLogEntry` answer, the event schema, the closed lists, the consumed rows, the rights, the error set and the fakes: RWB-S6-E6005-CON.
- The lot build, the agent estimate, the reserve price and API-S6-001: RWB-S6-E5024-APP; the eligible-account selection and R-DS-01 to R-DS-03: RWB-S6-E5023-APP.
- The committee approval of the reserve and the tiered terms and the approval columns: RWB-S6-E6001-APP.
- The sale agreement, the customer notices, R-DS-23 and the move to `LOT_AWARDED`: RWB-S6-E6006-APP.
- The data room, the tape, the masking and the bid operation API-S6-005: RWB-S6-E5026-APP; the buyer qualification: RWB-S6-E6002-APP.
- The approval chain, the approver's act, the decision log entry and the rule package: rwb-decision (P7) (GAP-2990).
- The DoA table and its limits: rwb-access (P4) (GAP-2990).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes.
- The model score and its data product: rwb-source-data (P1) (GAP-2995).
- The transfer of the awarded data to the buyer: RWB-S6-E6007-APP; the settlement and `ProceedsMatched`: RWB-S6-E6011-APP (P8).
- The document, its custody and its retention: rwb-document (P5); the notices: rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-26: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
