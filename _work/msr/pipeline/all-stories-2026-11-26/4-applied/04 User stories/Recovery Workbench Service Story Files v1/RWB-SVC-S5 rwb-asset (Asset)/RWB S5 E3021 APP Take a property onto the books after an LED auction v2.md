# RWB-S5-E3021-APP Take a property onto the books after an LED auction

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-D |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E3021-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-021 split out for rwb-asset. The four legacy acceptance criteria are kept word for word with their origin tag, and one new criterion covers the rule of the feature that the legacy text does not name. The take-on runs as one step of `AssetDisposalWorkflow` on task queue `rwb-asset`, triggered by the LED handover result consumed as the `AuctionResult` event of rwb-litigation (S4), and creates the `asset` row in `rwb_asset` linked to the ACE NPA asset by its asset key. The decision is recorded through the local library before the row changes (DP-03), the case move to `ASSET_ON_BOOKS` is answered to rwb-case, and `AssetTakenOn` is published from the outbox. The legacy `v_ace_npa_asset` read is retired as a service read because rwb-asset holds no ACE view grant, so the ACE facts arrive on the rwb-source-data data-product contract (DP-05); the base becomes `/api/recovery/asset/v1` (DP-13); SCR-21 and SCR-22 read through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E3021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **the Workbench to create the asset record when the bank takes the property at the enforcement auction, record the decision with its rule version and open the record on the ACE NPA asset**, so that **a property the bank wins at the Legal Execution Department auction is on the books the day the handover is recorded, linked to the asset ACE already knows, and can be held and sold without a re-keying step**.

This is the application slice of legacy RWB-E3-021. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- one take-on step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-DIS-03 on the LED handover, with the DISPOSAL package version in force; R-DIS-01 and R-DIS-02 are the other two take-on routes of the same step and are tabled in §8 with the note that their behaviour is built once;
- the creation of the `asset` row in schema `rwb_asset` with the columns of DF-COL-028 to DF-COL-042, `transfer_in_type` set to `AUCTION_PURCHASE` and `auction_purchase_price` carrying the handover price;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the row changes (DP-03);
- the publication of `AssetTakenOn` on `rwb.asset.events.v1` from the outbox, for rwb-case and rwb-payment;
- the answer to rwb-case for the case move `ASSET_ON_BOOKS`, with the rule ID and the version that produced it;
- the two reads behind SCR-21 and SCR-22 on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the two reads, the `asset` element, the `AssetTakenOn` envelope, the consumed rows, the error set and the fakes, which are RWB-S5-E3021-CON; the enforcement auction, the LED result and the litigation facts around it, which are rwb-litigation's (S4); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the ACE NPA asset facts, which are rwb-source-data's (P1); the holding clocks of R-DIS-06 and the provision steps, which are later stories of this service; the money and any posting, which are rwb-payment's (P8); and the deployment of this build, which is the operations story of this legacy key and the wave 2 harness.

### 2. Business rationale

Legacy RWB-E3-021 gave the Workbench one step that opened the asset record when the bank took the property at the enforcement auction, and the FSD keeps the objective unchanged: the NPA sales cycle is measured on the decision log and the Workbench records, reviewed monthly, and moves from 1,486 days to a target of 1,095 days (FSD S5 A2.3.1). The thin story adds the fact the legacy text leaves implicit: the record is linked to the property in `v_ace_npa_asset`, which ACE ingests from AMIS, **by its asset key**, when the bank takes the property at the enforcement auction (Epics 3 to 8 Specification v3, FEAT-AST-03).

What D-RCV-60 changes is who owns the auction result, the asset record and the case. In the monolith the take-on wrote the asset row, the case stage and the decision log row in one `recovery` schema and one process. In the target:

- **the enforcement auction and its result are rwb-litigation's.** Architecture v5 slide 3 gives litigation "court, judgment, enforcement, auction" and slide 13 makes rwb-asset listen to rwb-litigation's events, so the handover result arrives as the consumed event `AuctionResult` on `rwb.litigation.events.v1`, one hop with a 2 s budget and a breaker. The plan's C and I rows for this slice are None and the absence is recorded (GAP-2847; ASM-4712).
- **the asset record is this service's.** `asset` is S5's own record in `rwb_asset` (Architecture v5 slides 19 and 41; TSD S5 T3.1) and it links to the ACE asset by key, with no foreign key (TSD S5 A2.6.3.2 field catalog; TSD S5 T3.3).
- **the ACE facts stay with rwb-source-data (P1).** The legacy data table names `v_ace_npa_asset`, and the FSD names the AMIS fact behind it; in the target only rwb-source-data reads the 30 `recovery.v_ace_*` views (Architecture v5 slides 29, 37 and 45), so DP-05 applies as a prohibition (GAP-2849; ASM-4715).
- **the case of record stays with rwb-case (P3).** `recovery_case` and the route states are P3's; this story evaluates the rule, creates the asset row, records the decision and answers the case move (GAP-2847; ASM-4716).
- **the decision is recorded first**, through the local decision-record library of DP-03, which is what legacy AC1 asked for and what legacy AC4 tests.
- **the event is published from the outbox.** Architecture v5 slide 19 OUT gives rwb-asset the topic `rwb.asset.events.v1` with `AssetTakenOn`, and slide 43 row 22 gives the event the consumers rwb-case and rwb-payment. The plan's pattern set does not carry DP-09, so `RWB-PLT-TE006-CON` is a real dependency the plan's H row does not name (GAP-2847; ASM-4717).

The legacy story carries two criteria that are not this feature's own rules: AC2 is R-DIS-01, the vehicle repossession, and AC3 is R-DIS-02, the deed in lieu transfer, while the LED rule of FEAT-AST-03 is R-DIS-03 and no legacy criterion names it (FSD S5 A2.3.3.1; Business Rules and Routing Logic v4). The criteria are copied word for word as the rule requires, the behaviour of R-DIS-01 and R-DIS-02 is built once in a shared take-on component and is proved by RWB-S5-E3019-APP and RWB-S5-E3020-APP, and the LED path is proved here by AC5 (GAP-2848; ASM-4713). No business value moves: the ladder of 100, 90, 80 then 70 percent, the `handed_over` result, `AUCTION_PURCHASE` of `LOV-TRANSFER-IN` and the one-working-day target of R-DIS-03 are values of reference data and of the rule package, read with their version and never written in code (GAP-2849; ASM-4718).

### 3. Preconditions

- RWB-S5-E3021-CON is published: the two read operations, the `asset` element, the `AssetTakenOn` envelope, the consumed `AuctionResult` row, the error set and the fakes are baselined and handed to this story.
- The rwb-litigation contract of the enforcement auction is published with its fake, so the LED handover result can be consumed on Day 1. Its story key and its event property list are Not specified in the source documents (GAP-2849; ASM-4714). The row is not in this story's contract-dependency list, which is None, and the absence is recorded (GAP-2847; ASM-4712).
- The rwb-source-data data-product contract of DP06 Collateral and assets is published with its fake, so the ACE NPA asset fact of the case can be read on Day 1. Its operation names are Not specified in the source documents (GAP-2849; ASM-4715).
- The case state read and the case-move answer of rwb-case are available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome that the parent `CaseWorkflow` applies (GAP-2847; ASM-4716).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-22 reach this service through the gateway-bff composite route, one hop each (DP-19).
- `asset` exists in schema `rwb_asset` from the DB story of this service, with the columns of DF-COL-028 to DF-COL-042 and the standard record columns of TSD S5 T3.0; this story adds no table, no column and no migration.
- The DISPOSAL rule package is in force at its version with R-DIS-01, R-DIS-02, R-DIS-03 and R-DIS-06; the package is authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`.
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_asset` or on `rwb_litigation` is refused by the database and fails the boundary test (DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S5-E3021-CON when its tests pass.

### 4. Flow

1. The enforcement case reaches its auction in rwb-litigation; the court, the auction and its result stay there (Architecture v5 slide 3; FSD S5 A2.3.2 integration points, LED portal).
2. The take-on step of `AssetDisposalWorkflow` on queue `rwb-asset` receives the `AuctionResult` event of rwb-litigation for a case in `ASSET_PENDING_TAKE_ON`, through the inbox, deduplicated by its event ID.
3. The step reads the handover result of the event: the case reference, the property reference, the asset key, the result `handed_over`, the round at which it was taken and the handover price. The result is `handed_over` after the 100, 90, 80 then 70 percent ladder (R-DIS-03); the event property names and the ladder values are Not specified in the source documents (GAP-2849; ASM-4714).
4. The step reads the ACE NPA asset fact of the property on the rwb-source-data data-product contract: the asset key, the asset reference, the asset code, the asset type, the condition, the photographs, the location, the segment and the taken-on date, one hop with a 2 s budget (GAP-2849; ASM-4715).
5. The step reads the case state and the account link on the rwb-case contract, read only, to confirm that the case is in `ASSET_PENDING_TAKE_ON`.
6. `AssetTakeOnEvaluator` loads the DISPOSAL package version in force and evaluates R-DIS-03 (`led_result = handed_over`). Where the result is not `handed_over`, or the case is not in `ASSET_PENDING_TAKE_ON`, the step changes nothing and reports the reason to the parent.
7. `AssetDecisionRecordWriter` writes one decision record through the local library, **before any change**: the case reference, the asset reference, the asset key, the LED result, the round, the rule ID with its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. `AssetTakeOnWriter` inserts the `asset` row in one `rwb_asset` transaction with the decision record, the outbox row and the idempotency row: `id` (DF-COL-028), `case_id` (DF-COL-029), `asset_ref` (DF-COL-031, the ACE asset key the record links by), `asset_code` (DF-COL-032), `asset_type` (DF-COL-033 against `LOV-ASSET-TYPE`), `transfer_in_type` (DF-COL-034 = `AUCTION_PURCHASE` of `LOV-TRANSFER-IN`), `from_segment` (DF-COL-035), `transfer_in_date` (DF-COL-036, the handover date), `book_value` (DF-COL-037, from the ACE fact), `auction_purchase_price` (DF-COL-038, the handover price), `repossessed_date` (DF-COL-039), `stock_date` (DF-COL-040) and `holding_status` (DF-COL-041 = `HELD` of `LOV-HOLDING`). `collateral_id` (DF-COL-030) is written where the ACE fact gives it.
9. The outbox writer publishes `AssetTakenOn` on `rwb.asset.events.v1` in the same transaction, with the case reference, the asset reference, the asset type, the transfer-in type, the taken-on date and the rule version, and no personal data.
10. `CaseMoveAnswer` answers rwb-case with the move `ASSET_ON_BOOKS`, the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither (GAP-2847).
11. A repeated `AuctionResult` event with the same event ID, or a second event for the same asset, writes nothing, publishes no second event, sends no second answer and counts the repeat.
12. SCR-21 Asset list and SCR-22 Asset record read the asset, its handover price and its holding status from this service through the gateway-bff composite route, read only, next to the case and the route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no asset row, no event and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E3-021-04, TC-E3-021-06 |
| X2 | The role does not hold the Asset and disposal right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E3-021-05 |
| X3 | The case is not in `ASSET_PENDING_TAKE_ON` | The step changes nothing and reports the reason to the parent; the take-on is not re-evaluated on a case that has already moved | None | AC5 |
| X4 | The LED result is not `handed_over`, or the auction was withdrawn | The step writes nothing and answers no move; the reason is reported to the parent | None | AC5 |
| X5 | The rwb-litigation event, the rwb-source-data read or the rwb-case answer does not arrive inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no case move is answered | None | AC1, AC5 |
| X6 | The ACE data product is stale after a late or failed batch (VR-S5-003-1) | The step holds, writes nothing and shows the data date; the take-on resumes on the next fresh answer | MSG-P1-001 | AC1, AC5 |
| X7 | An asset row already exists for the case and the asset key | One row, one event and one answer; the repeat is counted and no second decision record is written | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `litigation` row, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR4, BR5 |

X1 to X2 and X5 to X7 are the exception paths of RWB-E3-021 carried onto the split, X3 and X4 are the paths the LED result adds, and X8 is the DP-05 and DP-01 boundary. The one-working-day target of R-DIS-03 is a value in force and not a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3021-CON, the rwb-litigation event fake, the rwb-source-data and rwb-case fakes and the decision-record stub, on its own schema |
| Negotiable | The activity name, the decision code, the consumer group name and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the two reads and the `asset` columns are fixed |
| Valuable | A property the bank wins at the enforcement auction is on the books on the day of the handover, linked to the asset ACE already knows |
| Estimable | One workflow step, one evaluator, one record write, one row insert, one event consumed, one event published, one case-move answer, three clients and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases, sale events and ACE asset facts through the contract fakes, plus the access and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Take a property onto the books after an LED auction

  Background:
    Given case "RC-2026-000521" carries the enforcement auction of property "AST-2026-000521"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-01, R-DIS-02, R-DIS-03 and R-DIS-06
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Take a property onto the books after an LED auction (legacy RWB-E3-021 AC1)
    Given the rwb-litigation contract mock returns the auction result "handed_over" for property "AST-2026-000521" at the 100, 90, 80 then 70 percent ladder
    Given the rwb-source-data contract mock returns the AMIS property "AST-2026-000521" with its asset key, condition, photographs and location
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON" for "RC-2026-000521"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then creates the asset record when the bank takes the property at the enforcement auction
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-01 (legacy RWB-E3-021 AC2)
    Given the rwb-source-data contract mock returns the RPS repossession result of vehicle "AST-2026-000513" with statutory notice proved
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON" for "RC-2026-000513"
    Given a case in state ASSET_PENDING_TAKE_ON
    When repossession completed
    Then create the asset record from RPS with condition, photographs and location
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC3 Rule R-DIS-02 (legacy RWB-E3-021 AC3)
    Given the rwb-source-data contract mock returns the AMIS property "AST-2026-000512" with closing book value and the registered transfer date
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON" for "RC-2026-000512"
    Given a case in state ASSET_PENDING_TAKE_ON
    When dil transfer registered
    Then create the asset record from AMIS with the opening book value
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded (legacy RWB-E3-021 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Rule R-DIS-03 on the LED handover (new, D-RCV-60)
    Given the rwb-litigation contract mock returns the auction result "handed_over" for property "AST-2026-000521" with handover price 3500000.00
    Given the rwb-source-data contract mock returns the AMIS property "AST-2026-000521" with its asset key, condition, photographs, location and segment
    Given a case in state ASSET_PENDING_TAKE_ON
    When the LED handover is received
    Then the asset record is created from the AMIS fact with its transfer-in type AUCTION_PURCHASE and the handover price in auction_purchase_price
    Then the case move answered to rwb-case is ASSET_ON_BOOKS with R-DIS-03 and the package version in force
    Then AssetTakenOn is published once on rwb.asset.events.v1 with no personal data
```

The four legacy criteria are the criteria of RWB-E3-021 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written`, `its trigger arrives`, `repossession completed` and `dil transfer registered` all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. AC2 and AC3 name the rules of the other two take-on routes of the same step; their behaviour is built once and is proved in full by RWB-S5-E3019-APP and RWB-S5-E3020-APP, and here they assert the shared component and the contract answers and add no second behaviour (GAP-2848; ASM-4713). AC5 is new and covers R-DIS-03, the rule of FEAT-AST-03, which no legacy criterion names (FSD S5 A2.3.3.1; Business Rules and Routing Logic v4). The legacy `v_ace_npa_asset` read is not reproduced as a service read anywhere in this story (GAP-2849; ASM-4715). All fixture identifiers, dates and amounts are synthetic.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-03 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | LED_HANDOVER_RECEIVED | led_result = handed_over after the 100, 90, 80 then 70 percent ladder | Record the LED result and create the asset record | ASSET_ON_BOOKS | Sale officer | AMIS, the Legal Execution Department | 1 working day |
| R-DIS-01 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | REPOSSESSION_COMPLETED | asset_type = vehicle and statutory_notice_proved = Y | Create the asset record from RPS with condition, photographs and location | ASSET_ON_BOOKS | Sale officer | RPS, AMIS, Field App | 1 working day |
| R-DIS-02 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | DIL_TRANSFER_REGISTERED | asset_type = property and transfer registered | Create the asset record from AMIS with the opening book value | ASSET_ON_BOOKS | Sale officer | AMIS, the Land Office | 1 working day |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the case move to `ASSET_ON_BOOKS` is written by rwb-case on this story's answer, and the asset row is written here. R-DIS-03 is the rule of this feature; R-DIS-01 and R-DIS-02 are tabled because they are the other two take-on routes of the same step and the same `asset` row, and the Legal Execution Department, AMIS and RPS of the systems column are reached through rwb-litigation and rwb-source-data, never directly.

| ID | Rule | Source |
|---|---|---|
| BR1 | The `asset` record is this service's: its reference, key link, type, transfer-in type, dates, book value, handover price and holding status are columns of `asset` in `rwb_asset`, and no other service writes them | Architecture v5 slide 41; slide 19 OUT; TSD S5 T3.1 |
| BR2 | The record links to the ACE NPA asset by its asset key and carries no foreign key: `asset_ref` holds the key and no constraint leaves `rwb_asset` | TSD S5 A2.6.3.2 field catalog; TSD S5 T3.3; DP-01; Epics 3 to 8 Specification v3 FEAT-AST-03 |
| BR3 | The decision is recorded before the asset row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S5 T2; legacy RWB-E3-021 AC1 and AC4 |
| BR4 | The ACE asset fact stays with rwb-source-data: this story reads no `v_ace_*` view and no ACE table | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2849 |
| BR5 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (recovery_case owner P3); GAP-2847 |
| BR6 | The auction, its result and the LED handover stay with rwb-litigation: this story consumes `AuctionResult` and writes no `litigation` row | Ownership Map (S4 rows); Architecture v5 slide 13 row S5 and slide 19 IN; GAP-2847 |
| BR7 | Every value a business person may change is reference data or a rule row read with its version: the asset types, `AUCTION_PURCHASE` of `LOV-TRANSFER-IN`, the segments, the holding status values, the ladder and the `handed_over` result | TSD S5 T3.2; FSD S5 BR-S5-003; GAP-2849 |
| BR8 | One event per confirmed take-on, published from the outbox in the same transaction as the row, carrying identifiers, codes, dates and the rule version only | Architecture v5 slide 19 OUT and slide 43 row 22; GAP-2847 |
| BR9 | The same `AuctionResult` twice, or the same `Idempotency-Key` twice, writes once, publishes once and answers the case move once | TSD S5 T-A.2; Architecture v5 slide 11 |
| BR10 | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, a log, an event or a workflow input | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR5). What this story owns is the holding status of the asset and the state of the step.

| From (`asset.holding_status`) | Event | Condition | To |
|---|---|---|---|
| None, no row | The LED handover under R-DIS-03 | led_result = handed_over | A row in `HELD` with `transfer_in_type` = `AUCTION_PURCHASE`, the handover price and the case-move answer `ASSET_ON_BOOKS` |
| None, no row | A result the rwb-litigation event reports as not handed over, or a withdrawn auction | X4 | No row, no record and no answer |
| HELD | A second event for the same asset key | X7 | Unchanged, the repeat is counted |
| HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED, RENTED | A take-on event for an asset that already has a row | X7 | Unchanged, the repeat is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | `AuctionResult` arrives for a case in `ASSET_PENDING_TAKE_ON` | The package in force is loaded | Evaluating |
| Evaluating | R-DIS-03 fires | The decision record is written | Applying |
| Applying | The asset row and the outbox row are written and the case-move answer is sent | The transaction commits | Waiting for the next fact |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Evaluating | R-DIS-03 does not fire | X3, X4 | Waiting, nothing changed |

The route states `ASSET_PENDING_TAKE_ON` and `ASSET_ON_BOOKS` are those of the DISPOSAL machine of TSD S5 T4 and of the legacy criteria, and they live on the case of record. The holding status values are those of `LOV-HOLDING` in TSD S5 T3.2, and `AUCTION_PURCHASE` is a value of `LOV-TRANSFER-IN`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA in TSD S5 T6.1: the primary role of the feature, holding C, R, U and A on the asset and reading the take-on outcome |
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU: reads the asset, corrects the take-on facts and confirms the record |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the asset and the take-on outcome, and holds the enforcement case in the ledger |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | Asset and disposal RA: read, and approve through the approval path where a floor, a route or a book value needs it |
| PT-VALUER, PT-AUCTION, PT-RAMC | Asset and disposal R or RU as the TSD S5 T6.1 matrix gives it: the partner sees its own assets through the partner gateway |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R, C or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-asset service identity | Consumes the result, evaluates the rule, writes the decision record and the asset row, publishes the event and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S5 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the sale officer as also-user, and both statements hold: the step runs under the service identity with no officer task on the happy path, and the sale officer is the primary role when a person does act, on SCR-22 and on the correction paths of the later stories. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-028 | asset (S5, `rwb_asset`) | id | Write, the asset reference of the row, the event and the answer |
| DF-COL-029 | asset (S5, `rwb_asset`) | case_id | Write, from the case reference of the event and the rwb-case answer |
| DF-COL-030 | asset (S5, `rwb_asset`) | collateral_id | Write where the ACE fact gives the collateral |
| DF-COL-031 | asset (S5, `rwb_asset`) | asset_ref | Write, the ACE NPA asset key the record links by (BR2) |
| DF-COL-032 | asset (S5, `rwb_asset`) | asset_code | Write, from the ACE NPA asset |
| DF-COL-033 | asset (S5, `rwb_asset`) | asset_type | Write, against `LOV-ASSET-TYPE` |
| DF-COL-034 | asset (S5, `rwb_asset`) | transfer_in_type | Write, against `LOV-TRANSFER-IN` (`AUCTION_PURCHASE`) |
| DF-COL-035 | asset (S5, `rwb_asset`) | from_segment | Write, against `LOV-SEGMENT` |
| DF-COL-036 | asset (S5, `rwb_asset`) | transfer_in_date | Write, the handover date of the auction result |
| DF-COL-037 | asset (S5, `rwb_asset`) | book_value | Write, from the ACE asset fact |
| DF-COL-038 | asset (S5, `rwb_asset`) | auction_purchase_price | Write, the handover price of the auction result |
| DF-COL-039 | asset (S5, `rwb_asset`) | repossessed_date | Write where the ACE fact gives it; empty on an auction purchase |
| DF-COL-040 | asset (S5, `rwb_asset`) | stock_date | Write, the date the property enters stock |
| DF-COL-041 | asset (S5, `rwb_asset`) | holding_status | Write, against `LOV-HOLDING` (`HELD`) |
| DF-COL-042 | asset (S5, `rwb_asset`) | holding_cost_to_date | Not written here: the holding story of this service writes it |
| Standard columns | asset (S5, `rwb_asset`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the asset row changes |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value | Not read: this service holds no `v_ace_*` grant, and DP-05 applies as a prohibition (BR4) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case answer |
| DF-WRK-009 to DF-WRK-016 | assignment (P3) | the officer assignment of the take-on | Not read and not written: the assignment is P3's and the step runs unattended |
| DF-SAL-001 to DF-SAL-008 | listing (S5) | the listing of the asset | Not written here: the pricing story of this service writes it |

Field IDs are those of the TSD S5 Assets and auction v2 T3.1 and the Logical Data Model and Data Dictionary v9. **The LED result has no column of its own**: the round, the ladder percentage and the `handed_over` result are facts of the consumed event and of the decision record, and the handover price is written to DF-COL-038 (GAP-2849; ASM-4714). **No new table, no new column and no migration**: `asset` arrives with the DB story of this service, this story writes fifteen of its existing columns, and `decision_record`, `idempotency_key`, `inbox_event` and `outbox_event` are platform library objects created in `rwb_asset` by the library's own migration (DP-03, DP-09).

**No personal data.** The rows this story writes carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_asset`, the decision record, a log, an event or a workflow input, and the fixture data of the tests is synthetic. The property location is an asset fact of the ACE data product and is not copied into this schema.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the two reads whose shapes are declared by RWB-S5-E3021-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, condition, valuations, costs and listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

The errors are 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503. The operation IDs are those of TSD S5 T-A.1 and are not redefined here. The ownership rows `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds` belong to this service and to the pricing and auction stories; none of them is declared by this story. `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's under the Ownership Map ruling recorded by RWB-S5-E3019-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2849; ASM-4715)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE NPA asset fact of the case: asset key, asset reference, asset code, asset type, condition, photographs, location, segment, book value and the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the account link the asset row carries; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2847; ASM-4716)) | rwb-case (P3) | P3 rwb-case | The answer that carries `ASSET_ON_BOOKS` with the rule and its version; on the workflow boundary it is the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2847 and GAP-2849 with ASM-4712, ASM-4715 and ASM-4716.

#### 12.3 Events published

| Event | Topic | Payload | Consumers | When |
|---|---|---|---|---|
| `AssetTakenOn` (`rwb.asset.AssetTakenOn.v1`) | `rwb.asset.events.v1` | The case reference, the asset reference, the asset type, the transfer-in type `AUCTION_PURCHASE`, the taken-on date and the rule ID with its version; CloudEvents envelope; no personal data | rwb-case and rwb-payment (Architecture v5 slide 43 row 22) | In the transaction that inserts the `asset` row, from the outbox |

The topic carries the retry and `.dlt` topics of the platform (DP-14). `AssetSold` is the second event of the service and belongs to the sale and auction stories; this story publishes neither a second event nor an event of another owner. The outbox is the platform library object of DP-09, which the plan's pattern set does not carry (GAP-2847; ASM-4717).

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `AuctionResult` (`rwb.litigation.AuctionResult.v1`) | `rwb.litigation.events.v1`, with `.retry` and `.dlt` | S4 rwb-litigation | The LED handover result of the enforcement auction: the case reference, the property reference, the asset key, the result `handed_over`, the round at which it was taken, the handover price and the handover date. Property names Not specified in the source documents (GAP-2849; ASM-4714) |

The row is read from Architecture v5 slide 13, whose S5 row listens to S4's events, and from slide 19 IN, which gives rwb-asset the consumed events `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`. `AuctionResult` is the one this feature needs; `JudgmentRecorded` belongs to the litigation outcome and `ProceedsMatched` to the money, and neither is consumed by this step. The consumer group is `rwb-asset-led-handover`, the inbox deduplicates on the CloudEvents ID, and a redelivery writes nothing (BR9). The producer's story key and its event property list are the owner's and are not published (GAP-2849; ASM-4714).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route and the rule package in force; signals: the `AuctionResult` event, the case state answered by rwb-case and the approval answer |
| `takeOnLedAuctionAsset` | Activity, the one take-on step of this story | `rwb-asset` | The event and the ACE fact in; the rule ID with its package version, the asset reference, the published event and the case move out, with the decision record, the `asset` row and the outbox row written in one transaction |

The activity name is a target design choice of this story and is fixed by no source document; the trigger is the consumed `AuctionResult` event for a case in `ASSET_PENDING_TAKE_ON`, because the FSD declares no background event for the feature (FSD S5 A2.3.4.4). No child workflow for the auction exists in this service.

#### 12.6 Schedules

None. The step runs from the consumed event, and owns no Temporal Schedule, no Quartz job and no shared job table. The single Schedule of this service is JOB-19 Re-appraisal monthly, which belongs to the holding and re-appraisal story of this service.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`) | The taken-on property; this story inserts the row and writes the columns of §11 |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated event and the answer it holds |
| inbox_event | PLT library, created in `rwb_asset` | The deduplication row of the consumed `AuctionResult` (DP-09) |
| outbox_event | PLT library, created in `rwb_asset` | The `AssetTakenOn` row relayed to `rwb.asset.events.v1` (DP-09) |

Not owned and never read as a table: `legal_action` and `litigation` (S4), `recovery_case` and `assignment` (P3), `collateral` and every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7), `listing` and `asset_sale` (S5, later stories'). No foreign key leaves the schema and `asset.case_id` and `asset.asset_ref` are identifiers, not foreign keys across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-litigation auction-result fake | The `AuctionResult` of property `AST-2026-000521` for case `RC-2026-000521` with result `handed_over`, round and handover price 3500000.00; a result not handed over; a redelivery of the same CloudEvents ID; no event beyond 2 s | AC1, AC5, X4, X5, X7 |
| rwb-source-data data-product fake | The property `AST-2026-000521` with its asset key, condition, photographs, location, segment, book value and the freshness stamp; a stale product with its date; no answer beyond 2 s | AC1, AC2, AC3, AC5, X6 |
| rwb-case state and move fake | The states `ASSET_PENDING_TAKE_ON` and `ASSET_ON_BOOKS` of case `RC-2026-000521`; a case that has already moved; an accepted move and a refused move | AC1, AC2, AC3, AC5, X3 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-01, R-DIS-02, R-DIS-03 and R-DIS-06 | AC1, AC2, AC3, AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| Outbox and inbox stubs (`RWB-PLT-TE006-CON`) | A relayed `AssetTakenOn`, a relay that fails and retries, and a deduplicated redelivery | AC1, AC5 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000521` | AC1, AC5 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data read and of the case-move answer, the producer story key of the event and its property names carry the placeholder until their owners confirm them (GAP-2847, GAP-2849; ASM-4714, ASM-4715, ASM-4716).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two reads of the asset on `/api/recovery/asset/v1`; the rwb-source-data read, the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 1 published, 1 consumed | `AssetTakenOn` on `rwb.asset.events.v1` from the outbox; `AuctionResult` on `rwb.litigation.events.v1` into the inbox |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and its take-on step on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `takeon`, Java package `th.co.scb.ace.workbench.recovery.asset.takeon`; front end `src/modules/recovery/asset/AssetTakeOn.tsx`, the fragment SCR-21 and SCR-22 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant and reads no ACE view, and the asset fact is the one the rwb-source-data contract answers (Architecture v5 slides 29 and 41; GAP-2849; ASM-4715). DP-03 is the transaction rule of the step. DP-13 moves the base of the two reads and nothing else. DP-19 is how SCR-21 and SCR-22 reach this service, one hop through the gateway.

**Dependencies the patterns add and the plan does not hold.** DP-09 is the one pattern this step cannot do without and the plan's set does not carry: the step consumes an event and publishes one, so the outbox and inbox library `RWB-PLT-TE006-CON` is a real H dependency that is recorded rather than added to the H row the plan states (GAP-2847; ASM-4717). The three consumed rows are class C dependencies in fact and not in the metadata row, so the story builds against their documents and fakes on Day 1 (GAP-2847, GAP-2849; ASM-4712).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` take-on branch | Workflow | The step of the journey that waits for the auction result, loads the package in force and reports the outcome to the parent |
| `takeOnLedAuctionAsset` | Activity | The one step: take the event, read the ACE fact and the case, evaluate R-DIS-03, write the record, the row and the event, answer the case move |
| `AssetTakeOnEvaluator` | Service | The rule evaluation against the DISPOSAL package version in force, with the `handed_over` result and the ladder read as values |
| `AssetDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `AssetTakeOnWriter` | Repository | Inserts `asset` and writes its columns in one `rwb_asset` transaction, with the idempotency row and the optimistic lock |
| `AssetEventPublisher` and `AuctionResultListener` | Kafka adapters | The inbox row of the consumed event and the `AssetTakenOn` outbox row in the same transaction as the asset row |
| `SourceDataProductClient` | Client | The read of DP06 Collateral and assets, one hop, 2 s |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case |
| `AssetController` | Controller | The two reads, the capability area and right, the pagination and the problem mapping of 400, 401, 403, 404, 422 and 503 |
| `AssetTakeOn` | React component | Shows the asset, its handover price and its take-on state on SCR-21 and SCR-22, read only |

**Database and migrations.** No Flyway file. `asset` arrives with the DB story of this service, and the decision record, the idempotency key, the inbox and the outbox are library objects created in `rwb_asset` by the library's migration (DP-03, DP-09). No column is added for the LED round, the ladder or the result: they are facts of the event and of the decision record (GAP-2849; ASM-4714).

**Configuration and reference data.**

- `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT` and `LOV-HOLDING` at their version in force (TSD S5 T3.2), read as reference data and never as constants.
- The DISPOSAL package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the ladder of 100, 90, 80 then 70 percent, the `handed_over` result and the one-working-day target are values of the package and of reference data, not of this build.
- The capability area "Asset and disposal" and its rights are access rows of rwb-access, read through the guard.
- The consumer group `rwb-asset-led-handover` and the topic names are naming-library values (DP-14); the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. `AuctionResultListener` and the inbox row, with the redelivery and the no-answer paths (AC1, AC5, X5, X7).
2. The take-on branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset` as the stage child of `CaseWorkflow`.
3. `SourceDataProductClient` and `CaseStateClient` against their fakes, with the 2 s budget, the breaker, the stale path and the no-answer path (AC1, X5, X6).
4. `AssetTakeOnEvaluator` over the DISPOSAL package, with R-DIS-03, the no-fire path and the shared R-DIS-01 and R-DIS-02 branch (AC1, AC2, AC3, AC5).
5. `AssetDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `AssetTakeOnWriter` with the one transaction, the fifteen columns, `AUCTION_PURCHASE`, the handover price, the idempotency row and the optimistic lock (AC5, X7).
7. `AssetEventPublisher` and the `AssetTakenOn` envelope on the outbox (AC1, AC5).
8. `CaseMoveAnswer` and the parent signal, with the `ASSET_ON_BOOKS` move (AC1, AC2, AC3, AC5).
9. `AssetController` with the rights, the pagination and the problem mapping, and `AssetTakeOn` with the two screens through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read, no write to `rwb_litigation`, `rwb_case`, `rwb_decision` or `rwb_payment` (X8, BR4, BR5, BR6).

**Feature flag.** `rwb.asset.led-take-on-v1`, read as a flag of the platform library; off means the step holds the event, writes nothing and answers no move, and the sibling routes are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic `AuctionResult` in SIT, R-DIS-03 produces its record, its row, its event and its move, a redelivered event writes once, a forced record failure changes nothing, no `litigation` row and no `v_ace_*` read exists in the build, and SCR-21 and SCR-22 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this story raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this story raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or of the consumed event is absent or invalid | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the asset list or the asset (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the asset row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of the case is stale after a late or failed batch (X6, VR-S5-003-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs are those of the legacy message set and of FSD S5 A2.3.3.1, and the text is copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and the check itself belongs to rwb-source-data (GAP-2849; ASM-4715).

### 15. Screens and states

SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its take-on, held, listed and sold states are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its handover price and its holding status, rwb-case for the case and its route state, rwb-source-data for the ACE asset fact and rwb-valuation for the valuation references; this story fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the take-on state of SCR-22 — the record created with its handover date, its `AUCTION_PURCHASE` transfer-in type and its handover price — and the states it shows on failure: refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001, and held for a result that is not `handed_over`. The held, listed and sold states belong to the holding, pricing and sale stories of this service.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-021-01 | AC1 | Component | The `AuctionResult` of property `AST-2026-000521` for case `RC-2026-000521`; the asset row, the event and the case move asserted on the fakes |
| TC-E3-021-02 | AC2 | Component | The RPS repossession result of the sibling route; the contract answers and the shared component, with no second behaviour of R-DIS-01 |
| TC-E3-021-03 | AC3 | Component | The AMIS deed in lieu fact of the sibling route; the contract answers and the shared component, with no second behaviour of R-DIS-02 |
| TC-E3-021-04 | AC4 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E3-021-05 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E3-021-06 | Principle 5 | Component | A forced decision log write failure at the moment of the insert; no row, no event and no answer |
| TC-S5-E3021-APP-01 | AC5 | Integration | The LED handover with handover price 3500000.00; the `asset` row, the `AssetTakenOn` outbox row and the `ASSET_ON_BOOKS` move asserted end to end |

The six legacy cases are the legacy cases of RWB-E3-021 in their legacy order, with the Level column added: `System` maps to `Component` where the step is tested on its fakes. TC-E3-021-02 and TC-E3-021-03 assert the shared component and the contract answers only, because the behaviour of R-DIS-01 and R-DIS-02 is proved by the sibling stories (GAP-2848; ASM-4713). TC-S5-E3021-APP-01 is new and covers the LED rule of the feature. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in code: the ladder of 100, 90, 80 then 70 percent, the `handed_over` result, the one-working-day target, the lists and the rule rows stay data, reference data or the rule package, never a constant or a default.
- No personal data in `rwb_asset`, in the `AssetTakenOn` payload, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- The auction and its result stay with rwb-litigation and the ACE facts with rwb-source-data: this story writes no `litigation` row, reads no `v_ace_*` view and no ACE table, and a build that adds one fails the boundary test (DP-01, DP-05).
- The case stays with rwb-case and the money with rwb-payment: no `recovery_case` row, no posting and no balance change is written here (BR5).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- Consume through the inbox and publish through the outbox only; a direct Kafka call, a second consumer group or a second event fails the absence test.
- The event, the decision record and the error envelope come from the platform; this story narrows them but never redefines them.
- Every statement runs in `rwb_asset` under the service login; no grant on another `rwb_*` schema and none on a `v_ace_*` view is requested (DP-02).

### 18. Traceability

| Requirement ID | Requirement (short) | Element | Test cases |
|---|---|---|---|
| REQ-S5-001 | Every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step; the LED auction purchase is the third take-on route of the same record (Business Requirements Program v5; FSD S5 requirements served). The plan's reqs list for this slice is empty and TSD S5 T8 names no requirement for FEAT-AST-03 (GAP-2850; ASM-4715) | The `asset` row, its asset-key link, the `AssetTakenOn` event and the consumed `AuctionResult` | TC-E3-021-01, TC-S5-E3021-APP-01 |
| FEAT-AST-03 | Links the case to the property in `v_ace_npa_asset`, which ACE ingests from AMIS, by asset key when the bank takes the property at the enforcement auction (Epics 3 to 8 Specification v3) | The asset-key link of BR2 and the handover of R-DIS-03 | TC-S5-E3021-APP-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The consumed `AuctionResult` and the published `AssetTakenOn` | TC-S5-E3021-APP-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed REST rows | TC-E3-021-01 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-021, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, copied word for word here; AC5 is new for the LED rule |
| Test cases | TC-E3-021-01 to -06 as the application half, and the new TC-S5-E3021-APP-01 |
| Feature and screens | FEAT-AST-03, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-03 of this feature; R-DIS-01 and R-DIS-02 tabled as the sibling routes, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The published shape of the two reads, the `asset` element, the `AssetTakenOn` envelope, the consumed `AuctionResult` row, the error set and the fakes: RWB-S5-E3021-CON.
- The enforcement auction, its notices, the court steps and the LED result itself: rwb-litigation (S4), whose event this story consumes (GAP-2849).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes (GAP-2847).
- The ACE NPA asset and collateral facts and the freshness of the data product: rwb-source-data (P1) (GAP-2849).
- The vehicle repossession route and the deed in lieu route of the same step: RWB-S5-E3019-APP and RWB-S5-E3020-APP, which build the shared component once and prove R-DIS-01 and R-DIS-02 (GAP-2848).
- The holding-age clock, the provision steps, the monthly cost of carry and the re-appraisal Schedule JOB-19: the holding and re-appraisal stories of this service, with the posting itself in rwb-payment (P8).
- The statutory notice, its delivery proof and the failed-notice queue: RWB-S5-E3022-APP.
- The start and floor price, the listing and the auction rounds of the bank's own sale: the pricing and auction stories of this service.
- The authoring, testing, approval and versioning of the DISPOSAL package and of the rule rows of R-DIS-01, R-DIS-02 and R-DIS-03: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key and the wave 2 harness.
