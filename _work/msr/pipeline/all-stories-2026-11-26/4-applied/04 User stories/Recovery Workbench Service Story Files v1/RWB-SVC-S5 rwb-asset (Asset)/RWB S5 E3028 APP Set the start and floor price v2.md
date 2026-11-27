# RWB-S5-E3028-APP Set the start and floor price

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3028-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-K |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E3028-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-028 split out for rwb-asset. The four legacy acceptance criteria are kept word for word with their origin tag, and the pricing step becomes one step of `AssetDisposalWorkflow` on task queue `rwb-asset` that requests the pricing proposal of R-DIS-28, takes the officer's opening price and floor on SCR-23, routes the floor to the head of NPA through the approval child workflow on rwb-decision (R-DIS-29), records the decision through the local decision-record library before any change (DP-03), writes the `listing` row with its start and floor price in `rwb_asset`, resets the price inputs on a value accepted under R-DIS-17, answers the case moves `PRICE_PROPOSED`, `FLOOR_APPROVED` and `ASSET_HELD` to rwb-case, and publishes no event of its own. The base becomes `/api/recovery/asset/v1` (DP-13), SCR-21 and SCR-23 read through the gateway-bff composite route (DP-19), and the legacy `v_ace_valuation`, `v_ace_npa_asset` and `v_ace_score` reads are retired as service reads (DP-05). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E3028-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **to set the opening price and the floor, with the head of NPA approving the floor**, so that **assets sell sooner at approved prices**.

This is the application slice of legacy RWB-E3-028. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and field catalog they depend on;
- one pricing step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slide 19; Temporal and Drools Design slide 13);
- the evaluation of R-DIS-28 on `PRICE_MODEL_RUN` from `ROUTE_APPROVED_AUCTION`, of R-DIS-29 on the officer's approval of the floor, and of R-DIS-17 on `VALUE_ACCEPTED` from `REAPPRAISAL_RECEIVED`, each with the DISPOSAL package version in force;
- the write operation that sets the list price and the floor and sends the floor for approval, `POST /assets/{assetId}/listings` of API-S5-004 and its business-key form (DP-13);
- the `listing` row of the asset in schema `rwb_asset`, in the columns of DF-SAL-001 to DF-SAL-008 and no new column: the channel, `start_price`, `floor_price`, the round, the listed-at time and the status;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the row changes (DP-03);
- the approval of the floor as the kit's approval child workflow on rwb-decision, requested with the asset, the price and the officer's proposal, and answered by the head of NPA;
- the answer to rwb-case for the case moves `PRICE_PROPOSED`, `FLOOR_APPROVED` and `ASSET_HELD`, with the rule ID and the version that produced them, and no `recovery_case` row written here;
- no event of its own: `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold`, and neither is produced by this step;
- the reads behind SCR-21 Asset list and SCR-23 Listing and price on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the operations, the listing and price element, the closed lists, the consumed rows, the decision-record element, the error set and the fakes, which are RWB-S5-E3028-CON; the pricing agent, its model and its proposal, which are rwb-agent's (P10); the appraisal and its value, which are rwb-valuation's (S1) and SVAF's; the NPA asset and COLLINS facts and the freshness of the data product, which are rwb-source-data's (P1); the approval decision, its history and the limit, which are rwb-decision's (P7) and rwb-access's (P4); the case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`, which are rwb-case's (P3); the publication of the listing (R-DIS-33), the descending price schedule (R-DIS-38) and the auction rounds, which are RWB-S5-E3029-APP and the wave 2 auction stories of this service; and the deployment of this build, which is the operations story of this legacy key and the wave 2 harness.

### 2. Business rationale

Legacy RWB-E3-028 gave the Workbench the step that prices a held asset for sale: the sale officer sets the opening price and the floor, and the head of NPA approves the floor, so that no asset goes to market at a price the bank has not signed off. The FSD keeps the feature as FEAT-AST-11 "Set the start and floor price" in module S5, acted by the sale officer, with the head of NPA as the also-user and the floor approval as its condition (FSD S5 A2.11.1, A2.11.3.3; Epics 3 to 8 Specification v3). The requirement is REQ-S5-004, "A start price and a floor price are proposed for every asset, and the floor is approved by the named role" (FSD S5 requirements served). The module objective is unchanged, "assets sell sooner at approved prices", and the metric stays the NPA sales cycle measured on the decision log and the Workbench records, reviewed monthly, from 1,486 days to a target of 1,095 days (FSD S5 A2.11.1, A1.3).

What D-RCV-60 changes is who owns the price, the case, the approval and the facts the price is computed from.

- **the listing and its two prices are this service's.** `listing` is S5's table in `rwb_asset`, and `start_price`, `floor_price`, `sale_channel`, `round_no`, `listed_at` and `status` are its columns (TSD S5 T3.1; Architecture v5 slide 41, "assets taken on, holding, floor price, listings, auction rounds"). No other service writes the row.
- **the case of record stays with rwb-case (P3).** `recovery_case`, `assignment`, `task` and `timer` are P3's, and `ROUTE_APPROVED_AUCTION`, `PRICE_PROPOSED`, `FLOOR_APPROVED` and `ASSET_HELD` live there. This story evaluates the rules, writes the listing and **answers** the moves (GAP-2876; ASM-4772).
- **the approval stays with rwb-decision (P7).** AC1 says "with the head of NPA approving the floor", and R-DIS-29 makes `officer_approved = Y` its condition. The approval is the approval child workflow of the kit on rwb-decision, and the limit behind a floor is a delegated-authority row of rwb-access read at its version (Temporal and Drools Design slides 12 and 13, "Approval (DoA)"; Architecture v5 slide 41). No source gives the percentage or the limit, and this story writes neither (GAP-2879; GAP-2880; ASM-4775; ASM-4776).
- **the pricing agent stays with rwb-agent (P10).** R-DIS-28 has the pricing agent propose the opening price and the floor as the reserve, and its systems are the Agent Runtime and COLLINS (Business Rules and Routing Logic v4). This story requests the proposal and evaluates the rule; it computes no proposal, holds no model and fixes no reserve basis (GAP-2877; GAP-2883; ASM-4773; ASM-4779).
- **the appraisal stays with rwb-valuation (S1) and the party facts with rwb-source-data (P1).** The legacy data table names `v_ace_valuation`, `v_ace_npa_asset` and `v_ace_score`; in the target only rwb-source-data reads the `recovery.v_ace_*` views (Architecture v5 slides 29, 37 and 45), and `POST /assets/{assetId}/valuations` is rwb-valuation's under the Ownership Map ruling ASM-0043. DP-05 therefore applies as a **prohibition**: the asset, the appraisal and the COLLINS economics enter this step on their owners' contracts, and no `v_ace_*` grant exists here (GAP-2877; GAP-2878).
- **nothing is published.** Architecture v5 slide 19 OUT gives rwb-asset exactly two events, `AssetTakenOn` and `AssetSold`; the pricing step changes no state another service subscribes to, so it writes no outbox row and the absence is stated in §12.3.

**Why the price is a row and not a screen value.** The floor a head of NPA approves is the reserve the later steps sell against: R-DIS-29 fixes it and sets the step schedule by asset class, and R-DIS-38 steps the price down to it. If the floor were a screen value it could not be approved, versioned or audited, so it is a `listing` column with its decision record, and the approval reference and the rule version are stored with it.

### 3. Preconditions

- RWB-S5-E3028-CON is published: the two reads and the write, the listing and price element, the closed lists, the consumed rows, the decision-record element, the error set and the fakes are baselined and handed to this story.
- The rwb-case case state read (`GET /cases/{caseId}` family) and the case-move answer are available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome that the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-2876; ASM-4772).
- The rwb-agent pricing proposal is available for the fake with the opening price, the floor as the reserve and the model reference. Its operation name, its call type and its element names are Not specified in the source documents (GAP-2877; ASM-4773).
- The rwb-source-data asset and COLLINS fact and the rwb-valuation appraisal are available for their fakes: the asset key, the asset class, the transfer-in type, the book value, the appraised value, the appraisal date and the outliers flag. Their operation names are Not specified in the source documents, and the connection matrix of Architecture v5 slide 13 carries no arrow from P1 or S1 to S5 (GAP-2877; GAP-2878; ASM-4773; ASM-4774).
- The approval of the floor is available as the approval child workflow of the kit on rwb-decision (P7), with its answered and its refused answers. The element names and the shape of its answer are Not specified in the source documents (GAP-2880; ASM-4776).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the listing row and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-23 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `listing` and `asset` exist in schema `rwb_asset` from the DB story of this service, with the columns of TSD S5 T3.1 and the standard record columns of TSD S5 T3.0; this story adds no table, no column and no migration. The `asset` row is read here, and its ownership is carried as GAP-2884 with ASM-4780.
- The DISPOSAL rule package is in force at its version with R-DIS-28, R-DIS-29 and R-DIS-17; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The rule rows and the reference data of the step schedule are governed there and are not listed for this story (GAP-2881; ASM-4777).
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case` or on a `v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S5-E3028-CON when its tests pass.

### 4. Flow

1. The auction route is approved under R-DIS-21, and the case of record reaches `ROUTE_APPROVED_AUCTION`; the parent `CaseWorkflow` forwards the stage to the disposal workflow (Business Rules and Routing Logic v4; Temporal and Drools Design slide 13). Nothing of the case is read as a table here.
2. The pricing step of `AssetDisposalWorkflow` on queue `rwb-asset` receives the case signal and reads the case state and the case reference on the rwb-case contract, read only, to confirm the case is at `ROUTE_APPROVED_AUCTION` and to take the reference the listing carries (GAP-2876; ASM-4772).
3. `AssetFactClient` reads the asset on the rwb-source-data contract or from the `asset` row of `rwb_asset`: the asset key, the asset class, the transfer-in type and the book value. No `v_ace_*` view is read (DP-05; GAP-2877).
4. `PricingProposalClient` requests the pricing proposal from rwb-agent with the asset, the appraisal and the COLLINS economics reference, one hop with a 2 s budget and a breaker, and takes back the proposed opening price, the floor as the reserve and the model reference with its version. The proposal is the agent's; it is never computed, defaulted or cached here (GAP-2877; GAP-2883; ASM-4773; ASM-4779).
5. `PriceEvaluator` loads the DISPOSAL package version in force from rwb-decision and evaluates R-DIS-28: from `ROUTE_APPROVED_AUCTION`, on `PRICE_MODEL_RUN`, with any condition, the pricing agent proposes the opening price and the floor price as the reserve, and the case moves to `PRICE_PROPOSED`. The step then waits for the sale officer (Business Rules and Routing Logic v4; TSD S5 T4).
6. `AssetDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the asset reference, the model reference and its version, the rule ID with its package version, the inputs reference, the outcome and the decided-at time (DP-03).
7. `ListingWriter` inserts the `listing` row of the asset in one `rwb_asset` transaction with the decision record and the idempotency row: the channel, `start_price` as the officer enters it, `floor_price` as the officer enters it, `round_no` 1, `listed_at` empty and the status the reference data carries for a draft listing. The channel and status values are Not specified in the source documents and are read at their version (GAP-2881; ASM-4777).
8. `CaseMoveAnswer` answers rwb-case with `PRICE_PROPOSED` and the rule ID with its version. rwb-case writes the `recovery_case` row; this service writes neither that row nor an `assignment`, `task` or `timer` row (GAP-2876).
9. The sale officer opens SCR-23 Listing and price, sees the proposal and the asset, and confirms or changes the opening price and the floor; `ListingRequest` carries the asset reference, the channel, both prices and the round. A required field that is absent is refused with MSG-GEN-001 (FSD S5 A2.11.2 step 2).
10. `FloorLimitCheck` applies VR-S5-011-1: where the floor sits below the percentage of fair market value that the approver's level may sign, the request is refused with MSG-S5-001 and nothing is written; `{pct}` and `{limit}` are values of the rule package, of the appraisal read and of the delegated-authority row, never constants (GAP-2879; ASM-4775).
11. `FloorApprovalClient` starts the approval child workflow of the kit on rwb-decision with the case, the asset, the floor and the officer's proposal and waits for the answer; the head of NPA signs there, and this service neither decides the approval nor reads the authority table (GAP-2880; ASM-4776).
12. Where the approval is refused or not answered, nothing changes: the floor is not fixed, no case move is answered and the reason is reported to the parent; R-DIS-27 returns the asset to hold on a refusal and that move is rwb-case's.
13. `PriceEvaluator` evaluates R-DIS-29 on the answered approval: from `PRICE_PROPOSED`, on `FLOOR_APPROVED_BY_OFFICER`, with `officer_approved = Y`, the floor is fixed as the reserve and the step schedule is set by asset class, and the case moves to `FLOOR_APPROVED`. The step schedule is reference data of the rule package, not a table of this build (GAP-2881).
14. `ListingWriter` updates the same `listing` row in one transaction with its decision record: the approved `floor_price`, the reserved status and the approval reference, under the optimistic lock of `version`.
15. Where the case is at `REAPPRAISAL_RECEIVED` and the officer accepts the value, `PriceEvaluator` evaluates R-DIS-17: the appraised value is taken from rwb-valuation's answer and the list and floor price inputs are reset on the asset's next listing, and the case moves to `ASSET_HELD`. The appraised value is not written in `rwb_asset`, because no column of TSD S5 T3.1 holds it (GAP-2878; ASM-4774).
16. No event is published. The outbox holds no row for this step, because `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold` only (§12.3).
17. A repeated request with the same case, asset and proposal version, or the same `Idempotency-Key` twice, writes once, answers the case move once and counts the repeat.
18. SCR-21 Asset list and SCR-23 Listing and price read the asset, its listing and its prices from this service through the gateway-bff composite route, read only, next to the case state and the approval of rwb-case and rwb-decision (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no listing row, no approval reference and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E3-028-04, TC-E3-028-06 |
| X2 | The role does not hold the Asset and disposal right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | TC-E3-028-05 |
| X3 | The case is not at `ROUTE_APPROVED_AUCTION`, `PRICE_PROPOSED` or `REAPPRAISAL_RECEIVED` as the rule expects | 409 and nothing is written; the step reports the state to the parent and no price is fixed on a case that has already moved | None | AC1, AC2 |
| X4 | A required field of the request is absent, or `start_price` and `floor_price` are not numbers | 422 and nothing is written | MSG-GEN-001 | AC1 |
| X5 | The floor sits below the percentage of fair market value the approver's level may sign (VR-S5-011-1) | The floor is not fixed, no approval is requested and no case move is answered | MSG-S5-001 | AC1 |
| X6 | The approval is refused, or it is not answered inside the budget | Nothing is written and no move is answered; the refusal is rwb-decision's answer and the return to hold is R-DIS-27 and rwb-case's | None | AC1 |
| X7 | rwb-case, rwb-agent, rwb-valuation, rwb-source-data or rwb-decision does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no case move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC2, AC3 |
| X8 | The value is rejected under R-DIS-18, or `officer_accepted = N` | No R-DIS-17 record and no reset of the price inputs; the appraisal is re-ordered by rwb-valuation and the case stays at `REAPPRAISAL_RECEIVED` | None | AC3 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR4, BR5 |

X1 to X8 are the paths of RWB-E3-028 carried onto the split and the paths the target call types add, and X9 is the DP-05 and DP-01 boundary. The percentages, the limits, the model reference and the channel and status values are values in force, so none of them is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3028-CON, the rwb-case, rwb-agent, rwb-valuation, rwb-source-data and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P4, P7, P10 or S1 |
| Negotiable | The activity names, the decision code per rule, the shape of the stage outcome and the internal element names are this story's choice; the rules, the messages, the screens, the operations and the listing columns are fixed |
| Estimable | One workflow step, one write and one update of one row, two evaluators, one approval call, one decision record per outcome, five clients and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic assets, proposals and approvals through the contract fakes, plus the access case and the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Set the start and floor price

  Background:
    Given case "RC-2026-000512" holds asset "AST-2026-000512" at "ROUTE_APPROVED_AUCTION"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-28, R-DIS-29 and R-DIS-17
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Set the start and floor price (legacy RWB-E3-028 AC1)
    Given the rwb-decision contract mock returns the approval of the floor by the head of NPA for "RC-2026-000512"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the sale officer set the opening price and the floor, with the head of NPA approving the floor
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-28 (legacy RWB-E3-028 AC2)
    Given the rwb-case contract mock returns the case state "ROUTE_APPROVED_AUCTION" for "RC-2026-000512"
    Given the rwb-agent contract mock returns the proposed opening price and the floor price as the reserve
    Given a case in state ROUTE_APPROVED_AUCTION
    When price model run
    Then pricing agent proposes the opening price and the floor price as the reserve
    Then the case moves to PRICE_PROPOSED

  Scenario: AC3 Rule R-DIS-17 (legacy RWB-E3-028 AC3)
    Given the rwb-case contract mock returns the case state "REAPPRAISAL_RECEIVED" for "RC-2026-000512"
    Given the rwb-valuation contract mock returns the appraised value accepted for "AST-2026-000512"
    Given a case in state REAPPRAISAL_RECEIVED
    When value accepted
    Then update the appraised value and reset the list and floor price inputs
    Then the case moves to ASSET_HELD

  Scenario: AC4 Not recorded (legacy RWB-E3-028 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E3-028 word for word, with their origin tag added and nothing else changed: the repetition of `Then` and the legacy wording of `the user acts on the screen`, `price model run`, `value accepted` and `the action is taken` all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in five places in the target: the case and its route states are rwb-case's and the step reads and answers them; the proposal is rwb-agent's; the appraisal is rwb-valuation's; the asset and COLLINS facts are rwb-source-data's; and the floor approval is rwb-decision's, while this story writes the listing, records the decision and fixes the floor as the reserve.

Three notes are recorded rather than smoothed over. AC1 gives no from state, and the rule that follows it, R-DIS-29, starts at `PRICE_PROPOSED`; the story therefore reads AC1 as the officer's approval of the floor proposed under R-DIS-28, and the approval mock returns the head of NPA's approval of that floor (GAP-2879; GAP-2880; ASM-4775; ASM-4776). AC1 says "the head of NPA approving the floor" and no source gives a percentage or a limit: both are a rule value, an appraisal value and a delegated-authority row read at their version, and the approval is decided by the approver in rwb-decision, never here (GAP-2879; ASM-4775). AC3 says "update the appraised value", and no column of `rwb_asset` holds it: the value is read from rwb-valuation and the update is the reset of this service's own price inputs, which is stated in §9 and §11 (GAP-2878; ASM-4774).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-28 | Asset disposal | D8.1 to D8.3 | ROUTE_APPROVED_AUCTION | PRICE_MODEL_RUN | Any | Pricing agent proposes the opening price and the floor price as the reserve | PRICE_PROPOSED | Sale officer | Agent Runtime, COLLINS | 1 working day |
| R-DIS-29 | Asset disposal | D8.1 to D8.3 | PRICE_PROPOSED | FLOOR_APPROVED_BY_OFFICER | officer_approved = Y | Fix the floor as the reserve and set the step schedule by asset class | FLOOR_APPROVED | Workbench | Rules component | None |
| R-DIS-17 | Asset disposal | D8.1 to D8.3 | REAPPRAISAL_RECEIVED | VALUE_ACCEPTED | outlier_flag = N or officer_accepted = Y | Update the appraised value and reset the list and floor price inputs | ASSET_HELD | Workbench | SVAF, Workbench | None |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the case moves to `PRICE_PROPOSED`, `FLOOR_APPROVED` and `ASSET_HELD` are written by rwb-case on this story's answer, the listing and its two prices are written here, the proposal is rwb-agent's, the appraisal is rwb-valuation's and SVAF's, the approval is the head of NPA's in the approval child workflow of rwb-decision, and the step schedule is a value of the rule package. **AC1's approval is R-DIS-29 and not a rule of its own**: the legacy criterion names the head of NPA, and R-DIS-29 is the rule whose condition is that approval.

The rules that follow the floor are not this story's: R-DIS-30 to R-DIS-32 allocate the vendor, R-DIS-33 publishes the listing, R-DIS-34 blocks a listing whose evidence is missing, R-DIS-38 steps the price down and R-DIS-18 re-orders a rejected appraisal. They share this route set, they are named here for traceability, and none of them is evaluated or answered by this step.

| ID | Rule | Source |
|---|---|---|
| BR1 | The listing and its two prices are this service's: `start_price`, `floor_price`, the channel, the round and the status are columns of `listing` in `rwb_asset`, and no other service writes them | Architecture v5 slide 41; TSD S5 T3.1; Ownership Map (`listing` owner S5) |
| BR2 | The decision is recorded before the listing row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S5 T2 ("writes the decision log entry before any change"); legacy RWB-E3-028 AC1 and AC4 |
| BR3 | The proposal is rwb-agent's and the appraisal is rwb-valuation's: this story requests the proposal, reads the appraised value and computes neither, and holds no model, no reserve basis and no appraisal of its own | R-DIS-28 ("Pricing agent proposes"); R-DIS-17 ("Update the appraised value"); GAP-2877; GAP-2878 |
| BR4 | The case move is answered and not written: `recovery_case`, `assignment`, `task` and `timer` and the route states of this step are rwb-case's, and this story sends each move with the rule and its version | Ownership Map (recovery_case, assignment, task, timer owner P3); Architecture v5 slide 41; GAP-2876 |
| BR5 | The ACE facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and the asset, the appraisal and the COLLINS economics enter on their owners' contracts | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2877 |
| BR6 | The approval is never decided here: the approval child workflow of rwb-decision takes the signature and the limit is a delegated-authority row of rwb-access read at its version, with no percentage and no limit value in code, in a test or in a fixture | Temporal and Drools Design slides 12 and 13; Ownership Map (`approval` owner P7); GAP-2879; GAP-2880 |
| BR7 | Nothing is published by this step: `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold` only, and neither is the pricing step's | Architecture v5 slide 19 OUT and slide 43; Ownership Map events |
| BR8 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id` and `asset_id` are identifiers of other services' facts, and the listing links the asset by key | DP-01; TSD S5 T3.1 ("listing and asset_sale link to it by key, no foreign key") |
| BR9 | Every value a business person may change is reference data, a rule row or an approval row read with its version: the channels, the listing statuses, the step schedule by asset class, the percentage and the limit | TSD S5 T3.2; FSD S5 A2.11.3.1 BR-S5-011; legacy Guardrails; GAP-2881 |
| BR10 | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, a log or a workflow input; the case, the asset and the model are references | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |
| BR11 | The floor is fixed only once per listing and once per approval: the approved floor and its approval reference are written under the optimistic lock of `version`, and a repeat writes nothing | TSD S5 T3.0 (`version`); TSD S5 T2; legacy RWB-E3-028 AC1 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the moves and the parent `CaseWorkflow` applies them to the case of record (BR4). What this story does own is the status of the listing and the state of the step.

| From (`listing.status`) | Event | Condition | To |
|---|---|---|---|
| No listing for the asset | The proposal of R-DIS-28 arrives | The case is at `ROUTE_APPROVED_AUCTION` and the record is written | A listing in the status the reference data carries for a draft (Not specified in the source documents, GAP-2881; ASM-4777), with the officer's `start_price` and `floor_price` and the case-move answer `PRICE_PROPOSED` |
| A draft listing | The head of NPA approves the floor under R-DIS-29 | The approval is answered and the floor sits at or above the approver's percentage | The same row with the approved `floor_price`, the reserved status and the approval reference, and the case-move answer `FLOOR_APPROVED` |
| A draft listing | The approver refuses or does not answer | X6 | Unchanged, no approval reference, no answer; the return to hold is R-DIS-27 and rwb-case's |
| A draft listing | The floor sits below the approver's percentage | X5 | Unchanged and MSG-S5-001; no approval is requested |
| A listing whose value was accepted | R-DIS-17 fires on `VALUE_ACCEPTED` | `outlier_flag = N` or `officer_accepted = Y` | The price inputs are reset on the next listing of the asset and the case-move answer is `ASSET_HELD`; the row's prices are unchanged until the officer prices again |
| A listing whose value was rejected | R-DIS-18 fires on `VALUE_REJECTED` | X8 | Unchanged, no reset and no answer |
| Any | The same request or the same `Idempotency-Key` again | A row already exists for the case, the asset and the proposal version | Unchanged, the repeat is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The auction route is approved and the stage is signalled | The package in force is loaded | Requesting the proposal |
| Requesting the proposal | The rwb-agent answer arrives | The proposal carries both prices and the model reference | Evaluating R-DIS-28 |
| Evaluating R-DIS-28 | The rule fires | The case is at `ROUTE_APPROVED_AUCTION` | Applying |
| Applying | The listing row, the record and the idempotency row commit and the answer is sent | The transaction commits | Waiting for the officer |
| Waiting for the officer | `POST /assets/{assetId}/listings` arrives from SCR-23 | The role holds the right and the floor passes VR-S5-011-1 | Requesting the approval |
| Requesting the approval | The approval of the floor is answered | `officer_approved = Y` | Evaluating R-DIS-29 |
| Requesting the approval | The approval is refused or not answered | X6 | Waiting, nothing changed |
| Evaluating R-DIS-29 | The rule fires | The record is written | Applying the approved floor |
| Applying the approved floor | The row and the record commit and the answer is sent | The transaction commits | Waiting for the next fact |
| Applying any step | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | `VALUE_ACCEPTED` arrives for the asset | R-DIS-17 fires | Resetting the price inputs, then waiting for the officer |

The route states `ROUTE_APPROVED_AUCTION`, `PRICE_PROPOSED`, `FLOOR_APPROVED`, `REAPPRAISAL_RECEIVED` and `ASSET_HELD` are those of the DISPOSAL machine of TSD S5 T4 and of the legacy criteria, and they live on the case of record. The listing statuses are those of `LOV-LISTING` in TSD S5 T3.2 (DRAFT, LIVE, UNDER_OFFER, SOLD, WITHDRAWN); the pricing step's own status values for a draft and for a reserved floor are the ones the reference data is asked for, because the legacy screen states "below limit" and "published" are not list values (GAP-2881; ASM-4777).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA in TSD S5 T6.1: the primary role of the feature, setting the opening price and the floor on SCR-23 and submitting the floor |
| RW-HEADNPA, head of NPA | Asset and disposal RA: reads the asset, its proposal and its floor, and is the role the approval child workflow asks for the floor |
| RW-NPAMGR, NPA and asset manager; RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the asset and its listing, and may create a listing where the operational role needs it |
| RW-PRODHEAD, RW-HEADASL | Asset and disposal RA: read, and approve through the approval path where the delegated limit needs it |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| PT-AUCTION, PT-RAMC, PT-VALUER | Asset and disposal RU or R as the TSD S5 T6.1 matrix gives it: the partner reads its own assets through the partner gateway and never the floor before it is approved |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R, C or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| The approver the delegated-authority row names | Signs the floor in the approval child workflow of rwb-decision; the authority row is P4's and is read at its version, and no percentage or limit value is written here |
| rwb-asset service identity | Runs the step, requests the proposal and the approval, reads the asset and the appraisal, writes the decision record and the listing, and answers the case moves; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S5 T6.1 and the permission table of the legacy story, and nothing wider. The legacy story gives the right C to RW-ENFORCE, RW-SALEOFF, RW-NPAMGR and SY-DATALOAD and the right R to the case owner, the team manager, the field collector, the complaint officer, the litigation officer, the enforcement owner, legal counsel, the sale officer and 23 more, which is the T6.1 matrix read from the other side. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | Write, the listing of the asset: `start_price` and `floor_price` from the officer's request, the approved floor from R-DIS-29 |
| DF-COL-028 to DF-COL-042 | asset (S5, `rwb_asset`; the row is absent from the Ownership Map table list and its owner is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 — GAP-2884; ASM-4780) | id, asset_ref, asset_type, holding_status, book_value and the other columns | Read, the asset the listing is priced for; no column is written here |
| Standard columns | listing (S5, `rwb_asset`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, model version, inputs reference, outcome, decided at | Write through the local library, before the listing row changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table: the case state and its reference arrive on the rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read and not written: the package version in force arrives on the rwb-decision contract |
| DF-ACE-187 to DF-ACE-195 | `v_ace_valuation` (P1) | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, appraisal_date and 3 more | Not read: this service holds no `v_ace_*` grant; the appraisal arrives on rwb-valuation's answer and its ACE source stays with P1 (BR5) |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more | Not read: taken on the rwb-source-data contract where the asset fact is needed (BR5) |
| DF-ACE-270 to DF-ACE-279 | `v_ace_score` (P1) | score_key, account_key, model_code, model_version, score_value, estimate_value and 4 more | Not read: the COLLINS economics arrive as a reference on the rwb-agent and rwb-source-data answers, never as a view read here (BR5) |
| appraisal (S1) | appraisal (S1) | the appraised value, its date, the model version and `outlier_flag` | Not read as a table: read on the rwb-valuation contract, and no column of `rwb_asset` holds the value (GAP-2878) |
| approval (P7) | approval (P7) | id, case_id, route, requested_at, answered_at, approver_role and the answer | Not read and not written: the approval is the child workflow's, and only its reference is stored with the listing |
| the step schedule by asset class (rule package, P7) | rule_row and its reference data (P7) | the step schedule per asset class | Not stored here: a value of the package in force (GAP-2881; ASM-4777) |

Field IDs are those of the TSD S5 Assets and auction v2 T3.1 and the Logical Data Model and Data Dictionary v9, and the case, decision, rule, valuation, NPA asset and score rows are the rows the legacy story lists in its Data table, with their owners changed by the target. **No new table, no new column and no migration**: `listing` and `asset` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_asset` by the library's own migration (DP-03). No `outbox_event` row is written by this step. The appraised value, the channel and the status values and the step schedule have no column or list in the sources, and none is invented here (GAP-2878; GAP-2881).

**No personal data.** The rows this story writes carry identifiers, codes, amounts, dates and rule and model versions. No name, address, contact value or identity number enters `rwb_asset`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, condition, valuations, costs and its listing (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |
| POST | `/assets/{assetId}/listings` | ListingRequest in; Approval out, the floor sent for approval (API-S5-004) | Asset and disposal, right C, scope applied | `Idempotency-Key` header |
| POST | `/assets/{assetKey}/listings` | The business-key form of the same operation, in the Ownership Map row; its request and answer are the same ListingRequest and Approval | Asset and disposal, right C, scope applied | `Idempotency-Key` header |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 409 when the case or the listing is not in the state the rule expects, 422 with MSG-GEN-001 for an invalid field, and 503 when the decision library or a consumed contract does not answer. The operation IDs are those of TSD S5 T-A.1 and are not redefined here. The two paths of the listing create are both declared because the Ownership Map carries the business-key form and TSD S5 T-A.1 carries the `{assetId}` form; the API v2 asset paths are superseded in v3 by the business-key path under the Ownership Map ruling ASM-0052, and both are answered by the same activity. `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's under ASM-0043, `POST /listings/{listingId}/rounds` (API-S5-005) belongs to the auction rounds story of this service, and neither is built or declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the case reference the listing carries; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2876; ASM-4772)) | rwb-case (P3) | P3 rwb-case | The answer that carries `PRICE_PROPOSED`, `FLOOR_APPROVED` or `ASSET_HELD` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The pricing proposal (operation name and call type Not specified in the source documents (GAP-2877; ASM-4773)) | rwb-agent (P10) | P10 rwb-agent | The opening price and the floor as the reserve, with the model reference and its version, for R-DIS-28; faked |
| The asset and COLLINS fact (operation name Not specified in the source documents (GAP-2877; ASM-4773)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset key, asset class, transfer-in type and book value, the COLLINS economics reference and the freshness stamp; read only, faked |
| The appraisal read (operation name Not specified in the source documents (GAP-2878; ASM-4774)) | `/api/recovery/valuation/v1` | S1 rwb-valuation | The appraised value, its date, the model version and `outlier_flag`, for R-DIS-17; read only, faked |
| The approval child workflow of the kit (element names Not specified in the source documents (GAP-2880; ASM-4776)) | rwb-decision (P7), its own task queue | P7 rwb-decision | The approval of the floor by the head of NPA, with its answered and its refused answer and the approval reference; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020); the approval is a Temporal child workflow and not a chained REST call, so it keeps the one-hop rule. The six rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2876, GAP-2877, GAP-2878 and GAP-2880 with their assumptions.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset exactly two events, `AssetTakenOn` and `AssetSold`, and neither is the pricing step's: the take-on is RWB-S5-E3019-APP's and the sale and its `AssetSold` are the sale and auction stories', and the pricing step changes no state that another service subscribes to. No `outbox_event` row is written, no topic is written outside `rwb.asset.events.v1`, and a build that adds an event here fails the absence test of RWB-S5-E3028-CON.

#### 12.4 Events consumed

None. The service consumes `JudgmentRecorded`, `AuctionResult`, `ProceedsMatched` and `PartnerResultSubmitted` (Architecture v5 slides 19 and 43), and none of them starts this step: the proposal is requested as a call, the approval answer comes back on the child workflow, and the stage is signalled by the parent `CaseWorkflow` after the route approval. `DeviationRaised` and `DeviationCleared` are consumed by rwb-case, rwb-comms and rwb-treatment, not by rwb-asset (Architecture v5 slide 42 rows 06 and 07). This story therefore holds no consumer group, no subscription and no inbox row of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference and the rule package in force; signals: the case state answered by rwb-case, the officer's request, the approval answer and the rule package in force |
| `setStartAndFloorPrice` | Activity, the pricing step of this story | `rwb-asset` | The case and the asset in; the rule ID with its package version, the listing reference, the approval reference and the case move out, with the decision record and the listing row written in one transaction |
| `ApprovalWorkflow` (the kit's approval child, owned by rwb-decision) | Child workflow, started by this step and owned by P7 | rwb-decision's queue | The head of NPA's approval of the floor; consumed, never declared as this service's |

No child workflow for the case and no workflow for the money exists in this service. The activity names are target design choices of this story and are fixed by no source document; the trigger is read as the stage signal after the auction route approval, because FEAT-AST-11 is a User feature acted by the sale officer and the FSD declares no background event for it (FSD S5 A2.11.4.4, "No background event").

#### 12.6 Schedules

None. The step runs from the stage signal, the officer's request and the approval answer, and owns no Temporal Schedule and no legacy Quartz job. The single Schedule of this service is JOB-19 Re-appraisal monthly, which belongs to the re-appraisal story of this service and is not registered here (Ownership Map jobs JOB-19).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| listing | S5 (`rwb_asset`) | The listing of the asset and its two prices; this story inserts the row and updates it with the approved floor |
| asset | S5 (`rwb_asset`) | Read only here: the asset reference, the asset class and the book value; the row is absent from the Ownership Map table list and its owner is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 (GAP-2884; ASM-4780) |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated request and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `approval`, `decision_log_entry` and `rule_row` (P7), `deviation` (S8), `appraisal` and `valuation` (S1), `template` and `notice` (P6), `proceeds` (P8), `document` (P5) and every `v_ace_*` view (P1). No foreign key leaves the schema and `listing.asset_id` is the identifier of this service's own asset row, not a foreign key across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state fake | The states `ROUTE_APPROVED_AUCTION`, `PRICE_PROPOSED`, `FLOOR_APPROVED`, `REAPPRAISAL_RECEIVED` and `ASSET_HELD` of case `RC-2026-000512`; a case that is not at `ROUTE_APPROVED_AUCTION` | AC1, AC2, AC3, X3 |
| rwb-case case-move fake | The moves `PRICE_PROPOSED`, `FLOOR_APPROVED` and `ASSET_HELD` accepted; a move refused because the case is not in the state the rule expects | AC1, AC2, AC3, X3 |
| rwb-agent pricing fake | The proposed opening price and the floor as the reserve with the model reference and its version; no answer beyond 2 s | AC2, X7 |
| rwb-source-data asset fake | The asset key, asset class, transfer-in type, book value, COLLINS economics reference and freshness stamp | AC1, AC2, X7 |
| rwb-valuation appraisal fake | The appraised value, its date, the model version and `outlier_flag = N`; a value whose outlier flag is set with `officer_accepted = N` | AC3, X8 |
| rwb-decision approval fake | The approval of the floor by the head of NPA with its reference; the approval refused; an approval not answered inside the budget | AC1, X6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for case `RC-2026-000512`, with the asset, its listing and its prices read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-case answer, the rwb-agent proposal, the rwb-source-data fact, the rwb-valuation appraisal and the approval child workflow are stubbed from the published owner documents and carry the placeholder until their owners confirm them (GAP-2876, GAP-2877, GAP-2878, GAP-2880; ASM-4772, ASM-4773, ASM-4774, ASM-4776).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 5 consumed | The two reads and the listing create in its two path forms on `/api/recovery/asset/v1`; the rwb-case state read, the rwb-case case-move answer, the rwb-agent proposal, the rwb-source-data fact and the rwb-valuation appraisal; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The step writes no outbox row and holds no consumer group; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 1 activity and 1 child workflow | `AssetDisposalWorkflow` and `setStartAndFloorPrice` on `rwb-asset`; the approval child workflow on rwb-decision's queue; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `pricing`, Java package `th.co.scb.ace.workbench.recovery.asset.pricing`; front end `src/modules/recovery/asset/AssetListingPrice.tsx`, the fragment SCR-23 embeds, and the SCR-21 list fragment, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the asset, the appraisal and the COLLINS economics enter on their owners' contracts (Architecture v5 slides 29 and 41; GAP-2877; ASM-4773). DP-03 is the transaction rule of both writes: the record and the listing row commit together or not at all. DP-13 moves the base of the two reads and the listing create and nothing else. DP-19 is how SCR-21 and SCR-23 reach this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The six consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2876, GAP-2877, GAP-2878 and GAP-2880. No event library is needed, because the step publishes nothing and consumes nothing; the outbox and inbox library `RWB-PLT-TE006-CON` of DP-09 is not added to the H row for that reason.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` pricing branch | Workflow | The step that waits for the stage signal and the officer's request, requests the proposal and the approval, loads the package in force and reports the outcome to the parent |
| `setStartAndFloorPrice` | Activity | The step: read the case and the asset, request the proposal, apply VR-S5-011-1, write the record and the listing, request the approval, apply R-DIS-29 and R-DIS-17, answer the moves |
| `CaseStateClient` and `CaseMoveAnswer` | Clients | The read of the case state and the answer of `PRICE_PROPOSED`, `FLOOR_APPROVED` and `ASSET_HELD` with the rule and its version, one hop, 2 s |
| `PricingProposalClient` | Client | The request of the proposal from P10 rwb-agent, one hop, 2 s, breaker; no model and no reserve basis here |
| `AssetFactClient` | Client | The asset and COLLINS fact from P1 rwb-source-data and the appraisal from S1 rwb-valuation, read only |
| `PriceEvaluator` | Service | The evaluation of R-DIS-28, R-DIS-29 and R-DIS-17 against the DISPOSAL package version in force, with the price check of VR-S5-011-1 |
| `FloorApprovalClient` | Child-workflow client | Starts the kit's approval child on rwb-decision and waits for the answered or refused answer, one hop and no chain |
| `AssetDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID, the package version and the model version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `ListingWriter` | Repository | Inserts and updates the `listing` row in one `rwb_asset` transaction, with the idempotency row and the optimistic lock |
| `AssetPriceController` | Controller | The listing create and the two reads, the capability area and right, the `Idempotency-Key` rule and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `AssetListingPrice` | React component | Shows the asset, the proposal and the two prices on SCR-23 and the list on SCR-21, read only, with the below-limit, approved, refused and not-recorded states |

**Database and migrations.** No Flyway file. `listing` and `asset` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). `start_price` and `floor_price` are existing columns of `listing`; no column is added for the appraised value, the model reference, the approval reference or the step schedule, because the appraisal and the model are referenced at their owners' version and the schedule is a value of the rule package (GAP-2878; GAP-2881).

**Configuration and reference data.**

- `LOV-LISTING`, `LOV-SALE-CHANNEL`, `LOV-ASSET-TYPE` and `LOV-HOLDING` at their version in force (TSD S5 T3.2), read as reference data and never as constants. The pricing step's own channel and status values are Not specified in the source documents (GAP-2881; ASM-4777).
- The DISPOSAL package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; R-DIS-28, R-DIS-29, R-DIS-17, the percentage of VR-S5-011-1 and the step schedule by asset class are values of the package, not of this build.
- The delegated-authority rows of rwb-access (P4) at their version, read by the approval and never copied into a constant (GAP-2879; ASM-4775).
- The capability area "Asset and disposal" and its rights are access rows of rwb-access, read through the guard.
- The 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The pricing branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset` as the stage child of `CaseWorkflow`, with the stage signal as its trigger.
2. `CaseStateClient` and `CaseMoveAnswer` against their fakes, with the 2 s budget, the breaker and the state-check path (AC1, AC2, AC3, X3, X7).
3. `AssetFactClient` and `PricingProposalClient` against their fakes (AC1, AC2, X7).
4. `PriceEvaluator` over the DISPOSAL package, with R-DIS-28, R-DIS-29, R-DIS-17 and the percentage check of VR-S5-011-1 (AC1, AC2, AC3, X5, X8).
5. `AssetDecisionRecordWriter` and `ListingWriter`, with the one transaction, the insert and the approved-floor update, the idempotency row and the optimistic lock (AC1, AC4, X1).
6. `FloorApprovalClient` and the kit's approval child, with the answered, the refused and the unanswered paths (AC1, X6).
7. `AssetPriceController` with the listing create in both path forms, the rights, the `Idempotency-Key` rule and the problem mapping (AC1).
8. `AssetListingPrice` and the two screens through the composite route fake (AC1, AC2).
9. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_valuation` (X9, BR4, BR5, BR6).

**Feature flag.** `rwb.asset.start-floor-price-v1`, read as a flag of the platform library; off means the step holds the stage signal, writes nothing and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic stage signal in SIT, an approved floor writes its listing row and its record and answers `FLOOR_APPROVED`, a rejected or unanswered approval changes nothing, a value accepted under R-DIS-17 resets the price inputs and answers `ASSET_HELD`, a repeated request writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-21 and SCR-23 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | The floor sits below the percentage of fair market value the approver's level may sign (VR-S5-011-1, X5); `{pct}` and `{limit}` are read from the package, the appraisal read and the delegated-authority row | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which the re-appraisal rule R-DIS-15 answers in the re-appraisal story of this service, so no path of this story raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of the request, of the stage signal or of the approval request is absent or invalid (X4) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the asset or its listing, or attempts the listing create (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the listing row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are those of the legacy message set, of FSD S5 A2.11.3.1 and of the platform set, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S5-002 is carried because it is in the message set of the feature, and no path of this story raises it.

### 15. Screens and states

SCR-21 Asset list in its loading and list states and SCR-23 Listing and price in its draft, below-limit, approved and published states are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its listing and its prices, rwb-case for the case and its route state, rwb-decision for the approval of the floor and rwb-agent for the proposal; this story fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the draft state of SCR-23, where the officer sees the proposal and enters both prices, the below-limit state, where the floor is refused with MSG-S5-001 and nothing is saved, the approved state, where the approved floor and its approver are shown, and the refusal and not-recorded states with MSG-P4-002 and MSG-P7-003. The published state of the same screen is written by the publication story (R-DIS-33) and is read here from the same route; the auction rounds of SCR-24 belong to the rounds stories and are not part of this screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-028-01 | AC1 | Component | Case `RC-2026-000512` at `PRICE_PROPOSED` with the approval of the floor answered; the `listing` row with `start_price` and `floor_price`, the decision record and the `FLOOR_APPROVED` answer asserted on the fakes |
| TC-E3-028-02 | AC2 | Integration | Case `RC-2026-000512` at `ROUTE_APPROVED_AUCTION`; the proposal of rwb-agent requested and the R-DIS-28 record, the listing insert and the `PRICE_PROPOSED` answer asserted end to end on the fakes |
| TC-E3-028-03 | AC3 | Integration | Case `RC-2026-000512` at `REAPPRAISAL_RECEIVED` with the value accepted; the appraised value read from rwb-valuation, the reset of the price inputs and the `ASSET_HELD` answer asserted, with no appraisal column written here |
| TC-E3-028-04 | AC4 | Component | The decision-record stub stopped; nothing written, no listing row, no answer, and MSG-P7-003 shown |
| TC-E3-028-05 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read and no write |
| TC-E3-028-06 | Principle 5 | Component | A forced decision log write failure at the moment of the listing insert; no row, no approval request and no answer |

The six legacy cases are the legacy cases of RWB-E3-028 in their legacy order, with the Level column added: the legacy `System` level maps to `Component` where the step is tested on its fakes, and TC-E3-028-02 and TC-E3-028-03 map to `Integration` because they cross the rwb-agent, rwb-valuation and rwb-case boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in code: the proposal, the percentage and the limit of the floor check, the step schedule by asset class, the channels, the listing statuses and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_asset`, in a workflow input or in a log: identifiers, codes, amounts, dates and rule and model versions only, and every fixture is synthetic.
- ACE data only through the owner's contract or the service's own `v_ace_*` views: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case, the approval with rwb-decision, the proposal with rwb-agent and the appraisal with rwb-valuation: no `recovery_case`, `assignment`, `task` or `timer` row, no approval answer, no model and no appraisal value is written here (BR3, BR4, BR6).
- The money stays with rwb-payment: no posting, no balance and no proceeds value is written here.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `v_ace_*` read.
- The decision is recorded before the change; a build that changes a row before its record fails the review (DP-03, BR2).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-004 | A start price and a floor price are proposed for every asset, and the floor is approved by the named role (FSD S5 requirements served; Epics 3 to 8 Specification v3 FEAT-AST-11). The split plan carries no requirement id for this slice, so the row is traced from the requirement of the module and the absence is recorded (GAP-2882; ASM-4778) | The pricing step, the proposal of R-DIS-28, the approval of the floor under R-DIS-29, the listing row and its two prices, and the decision record | TC-E3-028-01, TC-E3-028-02, TC-E3-028-06 |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the listing and its prices | TC-E3-028-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login | TC-E3-028-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed REST rows and the approval child workflow | TC-E3-028-02, TC-E3-028-03 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the change | TC-E3-028-04, TC-E3-028-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-028, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E3-028-01 to TC-E3-028-06 |
| Feature and screens | FEAT-AST-11, SCR-21 Asset list and SCR-23 Listing and price |
| Rules | R-DIS-28, R-DIS-29 and R-DIS-17, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the operations, the listing and price element, the closed lists, the consumed rows, the decision-record element, the error set and the fakes: RWB-S5-E3028-CON.
- The pricing agent, its model, its version and the reserve basis: rwb-agent (P10) (GAP-2877; GAP-2883).
- The appraisal, its value, its date and the outliers check: rwb-valuation (S1) and SVAF (GAP-2878).
- The asset, COLLINS and NPA facts and the freshness of the data product: rwb-source-data (P1).
- The approval, its limit and its answer, and the delegated-authority rows: rwb-decision (P7) and rwb-access (P4) (GAP-2879; GAP-2880).
- The case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3) (GAP-2876).
- The publication of the listing and its schedule (R-DIS-33 to R-DIS-35): RWB-S5-E3029-APP.
- The descending price schedule, the vendor allocation and the auction rounds (R-DIS-30 to R-DIS-32, R-DIS-36 to R-DIS-39): the wave 2 auction stories of this service, API-S5-005.
- The sale, the bid acceptances and the `AssetSold` publication (R-DIS-40 to R-DIS-52): the sale stories of this service.
- The re-appraisal cycle and its order (R-DIS-15 and R-DIS-16, JOB-19): the re-appraisal story of this service.
- The rule rows, the package version, its approval and the step schedule: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-23: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
