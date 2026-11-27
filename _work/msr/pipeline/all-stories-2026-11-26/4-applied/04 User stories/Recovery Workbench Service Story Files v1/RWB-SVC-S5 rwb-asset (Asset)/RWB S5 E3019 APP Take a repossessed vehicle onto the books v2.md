# RWB-S5-E3019-APP Take a repossessed vehicle onto the books

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-B |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E3019-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-019 is realigned onto rwb-asset (S5, wave 2). The four legacy criteria are kept word for word with their origin tag and only the cross-service `Given` lines are added. The take-on becomes one step of `AssetDisposalWorkflow` on task queue `rwb-asset`: it evaluates R-DIS-01 with the DISPOSAL package in force, writes the `asset` row in `rwb_asset`, records the decision through the local decision-record library before the row changes (DP-03), publishes `AssetTakenOn` from the outbox and answers the case outcome to the parent `CaseWorkflow` of rwb-case. The two reads behind SCR-21 and SCR-22 move to `/api/recovery/asset/v1` (DP-13) and are reached through the gateway-bff composite route (DP-19). The ACE NPA asset fact is consumed on the rwb-source-data data-product contract and no `v_ace_*` view is read (DP-05; GAP-2837; ASM-4697, ASM-4698). The holding clock and the provision steps of R-DIS-06 are built by RWB-S5-E3023-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E3019-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **the Workbench to create the asset record from the repossession result, record the decision with the rule version and start the holding clock**, so that **a repossessed vehicle is on the books the day the repossession completes and starts its holding age, instead of reaching the NPA stock register weeks later and lengthening the 1,486-day sales cycle**.

This story owns:

- the four acceptance criteria of legacy RWB-E3-019, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- one take-on step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, run as the stage child of `CaseWorkflow` (Architecture v5 slides 12 and 13; Temporal and Drools Design slide 13);
- the evaluation of R-DIS-01 on the repossession fact of a case, with the DISPOSAL package version in force;
- the insert of the `asset` row in schema `rwb_asset` with the columns of DF-COL-028 to DF-COL-042;
- the decision record of the outcome, written through the local decision-record library **before** the row changes (DP-03);
- the publication of `AssetTakenOn` on `rwb.asset.events.v1` from the outbox (event 22);
- the stage outcome returned to rwb-case, carrying the rule ID and its version;
- the read-only slices of SCR-21 Asset list and SCR-22 Asset record on base `/api/recovery/asset/v1`, behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the reads, the `asset` element, the `AssetTakenOn` envelope, the error set and the fakes (RWB-S5-E3019-CON); the holding-age and provision-step clocks and the cost of carry of R-DIS-06 (RWB-S5-E3023-APP); the case of record, its route state and its timers (rwb-case, P3); the ACE NPA asset, collateral and score facts (rwb-source-data, P1); the money and any posting (rwb-payment, P8); the document, its retention and the notice (rwb-document P5, rwb-comms P6); and the deployment of this build (the DB, INF and OPS stories of this legacy key and the wave 2 harness).

### 2. Business rationale

The objective and the metric of the feature are the legacy ones and do not move: the NPA sales cycle is measured on the decision log and the Workbench records, reviewed monthly, and goes from 1,486 days to a target of 1,095 days (FSD S5 A1.3 and A2.1.1). The programme requirement is REQ-S5-001, "Every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step" (Business Requirements Program v5; the split plan carries no requirement id, GAP-2837, ASM-4702).

D-RCV-60 changes who owns the record, not what the officer gets:

- **The asset record is this service's.** `asset` is written in `rwb_asset`, and rwb-asset owns assets taken on, holding, floor price, listings and auction rounds (Architecture v5 slides 19 and 41; TSD S5 T3.1). The Ownership Map lists `listing` and `asset_sale` for S5 and no `asset` row, so the ownership of `asset` is read from those two sources and recorded (GAP-2837; ASM-4698).
- **The case stays with rwb-case (P3).** `recovery_case`, its route state and its timers are P3's. The step receives the case reference and the repossession trigger on the Temporal boundary of the parent `CaseWorkflow` and returns the stage outcome with the rule ID and its version; it writes no case row and reads no case table.
- **The ACE fact stays with rwb-source-data (P1).** Only rwb-source-data reads the 30 `recovery.v_ace_*` views, and the S5 row of the connection matrix names no call to P1, so DP-05 applies here as a prohibition plus a contract read: the repossession fact arrives on the owner's data-product contract, whose operation names are not published (GAP-2837; ASM-4697). RPS, AMIS, the Field App, SVAF and HOME.SCB stay behind ACE ingestion, so the external dependency row is None (ASM-4701).
- **The decision is recorded first**, in the same transaction as the asset change, which is what legacy AC1 and AC4 test (DP-03; TSD S5 T2 "writes the decision log entry before any change").
- **The event leaves from the outbox.** Architecture v5 slide 19 gives rwb-asset the topic `rwb.asset.events.v1` with `AssetTakenOn`, and slide 43 row 22 gives it rwb-case and rwb-payment as consumers. The plan's pattern set for this key carries no DP-09, so the outbox and inbox library `RWB-PLT-TE006-CON` is a real dependency that the H row does not name (GAP-2837; ASM-4699).

No business value moves: the condition codes, the transfer-in type, the holding status, the one-working-day target of R-DIS-01 and the provision steps of R-DIS-06 are reference data or rule rows read with their version and never written in code.

### 3. Preconditions

- RWB-S5-E3019-CON is published and tagged: the two reads, the `asset` element, the four closed lists, the `AssetTakenOn` envelope, the consumed rows, the error set and the fakes are baselined and handed to this story.
- The rwb-source-data data-product contract of DP06 Collateral and assets is published with its fake, so the ACE NPA asset fact of the case can be read on Day 1. Its operation name is Not specified in the source documents (GAP-2837; ASM-4697); the plan's contract-dependency row is None.
- The rwb-case workflow boundary is available for the fake: the case reference and the repossession trigger arrive as child-workflow input, and the outcome is the child result the parent applies. No source publishes a REST operation that moves a case state on behalf of a stage (Architecture v5 slide 13; ASM-4700).
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-22 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `asset` exists in `rwb_asset` from the DB story of this service with the columns of DF-COL-028 to DF-COL-042 and the standard record columns of TSD S5 T3.0; this story adds no table, no column and no migration (DP-15 is the DB story's).
- The DISPOSAL rule package is in force at its version with R-DIS-01 and R-DIS-06; it is authored, tested and approved in rwb-decision (P7) and loaded here. The rule rows and the reference data of the condition codes are governed there.
- The service runs as its own login on `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_asset` or `rwb_case` is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S5-E3019-CON when its tests pass.

### 4. Flow

1. The repossession of a vehicle completes in RPS and ACE ingests the result into its own NPA asset data; the Workbench runs no inbound load, no load run and no data quality exception in this module (FSD S5 A1.1; D-RCV-35).
2. The parent `CaseWorkflow` starts, or signals, the take-on step of `AssetDisposalWorkflow` on queue `rwb-asset` for a case in `ASSET_PENDING_TAKE_ON`, passing the case reference and the repossession fact reference.
3. The step reads the ACE asset fact of the case on the rwb-source-data data-product contract: asset reference, asset code, asset type, transfer-in type, segment, taken-on date, book value, repossessed date, condition, photographs, location and the freshness stamp. One hop, 2 s budget, breaker, no retry of its own (ASM-4697).
4. `AssetTakeOnEvaluator` loads the DISPOSAL package version in force and evaluates R-DIS-01 on the fact: asset_type = vehicle and statutory_notice_proved = Y (FSD S5 A2.1.3.1; Business Rules and Routing Logic v4).
5. Where no rule fires, the step changes nothing, writes no decision record and returns an outcome that names no move to the parent.
6. `AssetDecisionRecordWriter` writes one decision record through the local library, **before any change**: case reference, asset reference, rule ID with its package version, inputs reference, outcome and the stage outcome. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
7. `AssetTakeOnWriter` inserts one `asset` row in a single `rwb_asset` transaction with the decision record, the outbox row and the idempotency row: `id`, `case_id`, `collateral_id`, `asset_ref`, `asset_code`, `asset_type` (VEHICLE of `LOV-ASSET-TYPE`), `transfer_in_type` (REPOSSESSION of `LOV-TRANSFER-IN`), `from_segment`, `transfer_in_date`, `book_value`, `auction_purchase_price`, `repossessed_date`, `stock_date` and `holding_status` = HELD of `LOV-HOLDING`. `holding_cost_to_date` stays empty until RWB-S5-E3023-APP writes it.
8. The outbox writer publishes `AssetTakenOn` on `rwb.asset.events.v1` in the same transaction, with identifiers, codes, the taken-on date and the rule version, and no personal data.
9. The step returns the stage outcome `ASSET_ON_BOOKS` to the parent with the rule ID, the version and the decided-at time. The confirmation of the record under R-DIS-06 is RWB-S5-E3023-APP's step; this story answers the confirmation and runs no clock of its own.
10. A repeated fact with the same case, asset reference and taken-on date writes nothing, publishes no second event, returns the same outcome and counts the repeat.
11. SCR-21 and SCR-22 read the asset, its holding status and its cost to date from this service through the gateway-bff composite route, read only, next to the case and the route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing is written: no asset row, no event and no stage outcome leaves the service | MSG-P7-003 | AC4, TC-E3-019-04, TC-E3-019-06 |
| X2 | The role does not hold the Asset and disposal right of the read | 403 before any read; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E3-019-05 |
| X3 | The case is not in `ASSET_PENDING_TAKE_ON` | The step returns without a move and writes nothing; a case that has already moved is not re-evaluated | None | AC3 |
| X4 | The data product is stale after a late or failed ACE batch | The step holds, writes nothing and shows the product date; it resumes on the next fresh answer | MSG-P1-001 | AC1, AC3 |
| X5 | The rwb-source-data contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no outcome is returned, and the caller sees 503 with the platform error envelope | None | AC1 |
| X6 | The fact does not satisfy the rule condition: the asset is not a vehicle or the statutory notice is not proved | No rule fires: no row, no record, no event and no move (the notice path is RWB-S5-E3022-APP's, R-DIS-04) | None | AC3 |
| X7 | An asset row already exists for the case and the asset reference | One row, one event and one outcome; the repeat is counted and no second decision record is written | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR4 |

X1 to X3 are the paths of RWB-E3-019 carried onto the split; X4 to X7 are the paths the target call types and the take-on event add; X8 is the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3019-CON, the rwb-source-data data-product fake, the rwb-case workflow fake and the decision-record stub, on its own schema, and needs no live P1, P3, P7 or P8 |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the two reads and the `asset` columns are fixed |
| Valuable | A repossessed vehicle is on the books with its decision recorded on the day the repossession completes, and the case moves in the service that owns it |
| Estimable | One workflow step, one evaluator, one record write, one row insert, one event, one stage outcome and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and ACE asset facts through the contract fakes, plus the access refusal and the forced record-write failure |

### 7. Acceptance criteria

```gherkin
Feature: Take a repossessed vehicle onto the books

  Background:
    Given case "RC-2026-000511" carries the repossession of vehicle "AST-2026-000511" in progress
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-01 and R-DIS-06
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Take a repossessed vehicle onto the books (legacy RWB-E3-019 AC1)
    Given the rwb-source-data contract mock returns the repossession result of asset "AST-2026-000511" with condition "FAIR", three photographs and location "Bangkok"
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON" for "RC-2026-000511"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then creates the asset record from the repossession result and starts the holding clock
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-06 (legacy RWB-E3-019 AC2)
    Given the rwb-case contract mock returns the case state "ASSET_ON_BOOKS" for "RC-2026-000511"
    Given the rwb-payment contract mock returns the monthly cost of carry posted for "RC-2026-000511"
    Given a case in state ASSET_ON_BOOKS
    When asset record confirmed
    Then start the holding age clock and the provision step clock, and charge cost of carry monthly
    Then the case moves to ASSET_HELD

  Scenario: AC3 Rule R-DIS-01 (legacy RWB-E3-019 AC3)
    Given the rwb-source-data contract mock returns the RPS repossession result of vehicle "AST-2026-000511" with statutory notice proved
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON" for "RC-2026-000511"
    Given a case in state ASSET_PENDING_TAKE_ON
    When repossession completed
    Then create the asset record from RPS with condition, photographs and location
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded (legacy RWB-E3-019 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are those of RWB-E3-019 word for word: the repeated `Then`, `the action is taken`, `the decision log cannot be written` and `its trigger arrives` all stand, and the only additions are the Background lines and the `Given the <service> contract mock returns <x>` lines that mock the cross-service parts. What the legacy lines describe happens in three places: rwb-source-data answers the ACE asset fact, this story evaluates the rule, records the decision, writes the `asset` row and publishes `AssetTakenOn`, and rwb-case applies the case move `ASSET_ON_BOOKS` or `ASSET_HELD` on the stage outcome. Two notes are recorded rather than smoothed over. AC1 says the step starts the holding clock and AC2 says the clock starts when the record is confirmed: the step starts it through the confirmation owned by RWB-S5-E3023-APP and never runs a second clock. AC2 is the same criterion that legacy RWB-E3-023 carries for R-DIS-06, so the build must not clock twice (GAP-2837; ASM-4703).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-01 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | REPOSSESSION_COMPLETED | asset_type = vehicle and statutory_notice_proved = Y | Create the asset record from RPS with condition, photographs and location | ASSET_ON_BOOKS | Sale officer | RPS, AMIS, Field App | 1 working day |
| R-DIS-06 | Asset disposal | D8.1 to D8.3 | ASSET_ON_BOOKS | ASSET_RECORD_CONFIRMED | title_status in (clear, under_transfer) | Start the holding age clock and the provision step clock, and charge cost of carry monthly | ASSET_HELD | Sale officer | Workbench, Finance provision feed | None |

Both rows are the rows of Business Rules and Routing Logic v4, copied character for character, and R-DIS-03 is tabled in the same set and bound to the LED auction story (RWB-S5-E3021-APP). The owner column is a business role, not a service: the route states are rwb-case's, the asset row is here, the clocks are RWB-S5-E3023-APP's and the cost of carry is posted by rwb-payment.

| ID | Rule | Source |
|---|---|---|
| BR1 | The `asset` record is this service's: its reference, type, transfer-in type, dates, book value and holding status are columns of `asset` in `rwb_asset`, and no other service writes them | Architecture v5 slides 19 and 41; TSD S5 T3.1; ASM-4698 |
| BR2 | The decision is recorded before the asset row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S5 T2; legacy AC1 and AC4 |
| BR3 | The ACE asset fact stays with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the fact on the owner's data-product contract only | DP-05; Architecture v5 slides 29, 37 and 45; ASM-4697 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and this story returns the stage outcome with the rule and its version | Ownership Map (`recovery_case` owner P3); Architecture v5 slide 13; ASM-4700 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id` and `collateral_id` are identifiers of other services' facts | DP-01; TSD S5 T3.3 (relationships inside the module only) |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT`, `LOV-HOLDING`, the condition codes and the provision steps | TSD S5 T3.2; FSD S5 BR-S5-001; legacy guardrails |
| BR7 | One event per confirmed take-on, published from the outbox in the transaction of the row, carrying identifiers, codes, dates and the rule version only | Architecture v5 slide 19 OUT and slide 43 row 22; ASM-4699 |
| BR8 | The same fact twice, or the same `Idempotency-Key` twice, writes once, publishes once and returns one outcome | TSD S5 T-A.2; Architecture v5 slide 11 |
| BR9 | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, a log or an event | Template and Rules v1 §R7.2 s17; Architecture v5 slide 42 notes |

### 9. State transitions

The case route state is rwb-case's and this story does not change it: the step returns the outcome and the parent applies it (BR4). What this story owns is the holding status of the asset and the state of the step.

| From (`asset.holding_status`) | Event | Condition | To |
|---|---|---|---|
| None, no row | The take-on fact under R-DIS-01 | asset_type = vehicle and statutory_notice_proved = Y | One row in HELD, with the outcome `ASSET_ON_BOOKS` |
| HELD and every later status | Any take-on fact for the same asset | X7 | Unchanged; the repeat is counted |
| None, no row | A fact that does not satisfy the rule condition | X6 | No row, no record, no outcome |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The repossession fact arrives for a case in `ASSET_PENDING_TAKE_ON` | The package in force is loaded | Evaluating |
| Evaluating | The rule fires | The decision record is written | Applying |
| Applying | The asset row and the outbox row are written and the outcome is returned | The transaction commits | Waiting for the next fact |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | The data product is stale | X4 | Held, until a fresh answer |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Sale officer (RW-SALEOFF) | Holds CRUA in Asset and disposal and reads SCR-21 and SCR-22; the take-on itself runs unattended |
| Head of NPA and NPA and asset manager (RW-HEADNPA, RW-NPAMGR) | Read the asset record and its holding status with RA and CRU (TSD S5 T6.1); no rule value is theirs here |
| rwb-case (P3) | Owns the case of record, its route state and its timers, and applies the stage outcome this story returns |
| rwb-decision (P7) | Owns the DISPOSAL package, its rule rows and its version; this story only evaluates it |
| Solution architect | Confirms the `asset` ownership row, the rwb-source-data operation name and the case boundary reading (GAP-2837) |

The step raises no approval and no officer task: the FSD records the feature as "None; runs unattended" with the sale officer as a secondary user (FSD S5 A2.1.3.3).

### 11. Data

| Table | Owner | Use in this story |
|---|---|---|
| `asset` | S5, `rwb_asset` | The taken-on asset: one row per confirmed take-on, read by the two screens. Owner read from Architecture v5 slides 19 and 41 and TSD S5 T3.1 (ASM-4698) |
| `decision_record` | Platform library, created in `rwb_asset` | The hash-linked record of the rule outcome, written before the row (DP-03) |
| `idempotency_key`, `outbox_event` | Platform library, created in `rwb_asset` | The repeat key with its answer and the `AssetTakenOn` row relayed to the topic (DP-09 library) |
| `listing`, `asset_sale` | S5, `rwb_asset` | S5's other tables; they belong to the pricing, listing and auction stories and are not written here |
| `recovery_case`, `timer` | P3 rwb-case | The case of record, its route state and its clocks; consumed as the stage boundary only |
| `v_ace_npa_asset` and the 29 other `v_ace_*` views | P1 rwb-source-data | The ACE asset fact; read only on the owner's data-product contract (DF-ACE-208 to DF-ACE-219) |
| `decision_log_entry`, `rule_row` | P7 rwb-decision | The central ledger and the rule rows; named, never written or read here |

The owned row writes the columns of DF-COL-028 to DF-COL-042: `id`, `case_id`, `collateral_id`, `asset_ref`, `asset_code`, `asset_type`, `transfer_in_type`, `from_segment`, `transfer_in_date`, `book_value`, `auction_purchase_price`, `repossessed_date`, `stock_date`, `holding_status` and `holding_cost_to_date` (TSD S5 T3.1). The legacy `timer` row is not written here because the holding clock is RWB-S5-E3023-APP's, and the legacy read of `v_ace_npa_asset` is replaced by the rwb-source-data contract with the operation name Not specified in the source documents (GAP-2837; ASM-4697).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). Both rows are read-only and serve the two screens; the take-on itself is driven by the workflow, not by a REST call.

| Method | Path | Shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | `AssetPage`, filtered by type, status and region, paged by page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetId}` | `Asset` with its holding status and cost to date (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |

Both answer 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, each in the platform error envelope; the shapes and the exact status list are RWB-S5-E3019-CON's.

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The read of DP06 Collateral and assets; operation name Not specified in the source documents (GAP-2837; ASM-4697) | P1 rwb-source-data | The ACE NPA asset fact of the case: asset reference, code, type, transfer-in type, segment, taken-on date, book value, repossessed date, condition, photographs, location and freshness (DF-ACE-208 to DF-ACE-219); faked on Day 1 |

One hop, 2 s timeout, breaker and no retry of its own (DP-11, ADR-020). The row is a contract dependency in fact and not in the metadata row, which is None (GAP-2837).

#### 12.3 Events published

| Event | Topic | Data | Consumers |
|---|---|---|---|
| `AssetTakenOn` (`rwb.asset.AssetTakenOn.v1`) | `rwb.asset.events.v1`, with `.retry` and `.dlt` | Case reference, asset reference, asset type, transfer-in type, taken-on date, rule ID and version; CloudEvents envelope; no personal data | rwb-case and rwb-payment (Architecture v5 slide 43 row 22), and no other consumer |

`AssetSold` is the service's second event and belongs to the sale stories. The outbox and inbox library that relays the row is `RWB-PLT-TE006-CON`, which the plan's H row for this key does not name (ASM-4699).

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them carries a repossession result or a case state; the take-on is driven by the stage child's input and signal. The service consumes those three events for the litigation, auction and proceeds stories, with no inbox declared here.

#### 12.5 Workflows and activities

| Name | Type | Queue | Element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Hosts the take-on step; its input, its signals and its stage outcome to the parent |
| `takeOnAsset` | Activity, the one take-on step | `rwb-asset` | Case reference and repossession fact in; rule ID with package version, asset reference, event and stage outcome out |

#### 12.6 Schedules

None. The step runs from the repossession fact forwarded by the parent; no Temporal Schedule, Quartz row, shared job table or batch table is declared. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `asset` | S5, `rwb_asset` | The taken-on asset, its fields, its lists and its holding status |
| `decision_record` | Platform library in `rwb_asset` | The local decision record written before the row (DP-03) |
| `idempotency_key` | Platform library in `rwb_asset` | The key of the repeated fact and its answer |
| `outbox_event` | Platform library in `rwb_asset` | The `AssetTakenOn` row relayed to `rwb.asset.events.v1` |

`listing` and `asset_sale` are S5's and not this story's; `recovery_case`, `timer`, `decision_log_entry`, `rule_row` and every `v_ace_*` view belong to other owners and are named only.

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The repossession result of `AST-2026-000511` for `RC-2026-000511` with condition, photographs, location and statutory notice proved; the same fact with the notice not proved; a stale product; no answer inside 2 s | AC1, AC3, X4, X5 |
| rwb-case workflow fake | The states `ASSET_PENDING_TAKE_ON`, `ASSET_ON_BOOKS` and `ASSET_HELD`; an accepted outcome and a refused one | AC1, AC2, AC3 |
| rwb-payment cost-of-carry fake | The monthly cost of carry posted for `RC-2026-000511` with its posting reference | AC2 |
| rwb-decision package fake | The DISPOSAL package at its version with R-DIS-01 and R-DIS-06 | AC1, AC2 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox; a stopped chain | AC4 |
| Outbox relay stub (`RWB-PLT-TE006-CON`) | A relayed `AssetTakenOn`; a relay that fails and retries | AC1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for `RC-2026-000511` | AC1, AC2 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-source-data data-product read; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `AssetTakenOn` on `rwb.asset.events.v1`; the decision record rides the library's `rwb.decision-record.v1` and is not this service's event |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and `takeOnAsset` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered by this step |

### 13. Solution plan

**Deliverables.** The take-on activity behind the stage child, the R-DIS-01 evaluator with the DISPOSAL package version, the decision-record writer, the `asset` insert with its outbox and idempotency rows, the `AssetTakenOn` publisher, the stage outcome, and the two read-only query handlers behind the screens.

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data through rwb-source-data's contract; no view grant here | None (C in fact; ASM-4697) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/asset/v1` | None |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

DP-05 is applied as a prohibition plus a contract read: the service holds no `v_ace_*` grant, so the fact can only arrive from the owner. DP-09 is not in the pattern set of this key although the published event needs its library (ASM-4699).

**Build steps.** (1) Wire the stage child and the activity on `rwb-asset`. (2) Read the repossession fact through the data-product client with the 2 s budget and the breaker. (3) Evaluate R-DIS-01 with the package version and write the decision record first. (4) Insert the `asset` row with its outbox and idempotency rows in one transaction. (5) Publish `AssetTakenOn` and return the stage outcome. (6) Add the two query handlers on the target base. (7) Prove the four criteria and the eight exception paths on the fakes.

**Done when.** The four criteria pass at component level on the fakes, the boundary test shows no `v_ace_*` read and no `rwb_case` statement, the repeat path writes once, and the screens answer through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record cannot be written before the asset row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Asset and disposal right of the read (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | The ACE data product of the case is stale (X4, VR-S5-001-1) | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | A required value of a read request is absent or invalid | Enter {field}. |
| MSG-S5-001 | Carried from the legacy message set of this key; it names the floor percentage and the approval limit, which are the pricing story's, so no path here raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key; it names the age of an appraisal, which is the re-appraisal story's, so no path here raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |

The text is the legacy and FSD wording, copied unchanged; no message is reworded and none is added.

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-22 Asset record | Take-on; held; listed; sold | The asset, its holding status and its cost to date on `GET /assets/{assetId}` through the composite route |
| SCR-21 Asset list | Loading; list | The paged asset list with type, status and region filters on `GET /assets` |

The screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case and its route state, rwb-source-data for the ACE fact and rwb-valuation for the valuation references; this story fixes only its own answers. The refusal, not-recorded and stale-data states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-019-01 | AC1 | Component | Synthetic case `RC-2026-000511` and asset fact `AST-2026-000511` on the fakes; one `asset` row and one `AssetTakenOn` |
| TC-E3-019-02 | AC2 | Component | Case at `ASSET_ON_BOOKS` confirmed; the outcome `ASSET_HELD` and the confirmation handed to RWB-S5-E3023-APP |
| TC-E3-019-03 | AC3 | Component | The RPS fact with statutory notice proved; row created with condition, photographs and location |
| TC-E3-019-04 | AC4 | Component | The decision-record stub stopped; no row, no event, no outcome, MSG-P7-003 |
| TC-E3-019-05 | AC1, X2 | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no decision record |
| TC-E3-019-06 | AC1, AC4, X1 | Component | A forced decision-record write failure stops the action with MSG-P7-003 |

The six ids are the legacy cases of RWB-E3-019 in their legacy order, carried as the application proof; the business outcome of each is proved here and its contract half is RWB-S5-E3019-CON's. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same id; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in code: the condition codes, the provision steps, the one-working-day target, the lists and the rule rows stay reference data or the rule package, read with their version.
- No personal data in the asset row, the decision record, an event, a workflow input, a log or a prompt: identifiers, codes, amounts, dates and a rule version only.
- ACE data only through the owner's contract: no `v_ace_*` view, no ACE table and no other service's schema (DP-01, DP-05).
- One base, one topic, one queue and one login per service; no second topic and no Schedule is added here (DP-13, DP-14).
- The decision record is written before the change and in its transaction; a failure rolls the row back (DP-03).

### 18. Traceability

| Legacy | Story | Test |
|---|---|---|
| RWB-E3-019 AC1 | AC1 (verbatim, with the mock lines) | TC-E3-019-01, TC-E3-019-05, TC-E3-019-06 |
| RWB-E3-019 AC2 | AC2 (verbatim; the clocks belong to RWB-S5-E3023-APP) | TC-E3-019-02 |
| RWB-E3-019 AC3 | AC3 (verbatim) | TC-E3-019-03 |
| RWB-E3-019 AC4 | AC4 (verbatim) | TC-E3-019-04, TC-E3-019-06 |

| Source | What it supplies |
|---|---|
| REQ-S5-001 (Business Requirements Program v5) | The recorded asset with source, date taken in, holding cost and provision step |
| FSD S5 A2.1 | The feature, its metric, R-DIS-01 and R-DIS-06, VR-S5-001-1 and the roles |
| TSD S5 T2, T3.1, T3.2, T5.3, T6.1 and T-A.1 | The decision-first rule, the `asset` columns and lists, the published event and the two operations |
| Architecture v5 slides 12, 13, 19, 29, 37, 41, 43 and 45 | The stage child, the inbound and outbound calls, the event and the ACE boundary |
| Split plan, slice RWB-S5-E3019-APP | H, C, I, X, the lane, the wave and the release (GAP-2837) |

### 19. Out of scope

- The contract surface: the OpenAPI document, the `asset` element, the lists, the event envelope, the error set and the fakes (RWB-S5-E3019-CON).
- The holding-age clock, the provision steps and the monthly cost of carry of R-DIS-06 (RWB-S5-E3023-APP), and every later disposal story of this service.
- The case of record, its route state, its timers and its parent workflow (rwb-case, P3); the ACE ingestion of RPS, AMIS and SVAF and the 30 `v_ace_*` views (rwb-source-data, P1); any posting or balance (rwb-payment, P8); the documents, the notice and the letters (P5, P6).
- The schema and migration of `rwb_asset`, the login, the deployment, the observability and the pipeline (the DB, INF and OPS stories of this legacy key); the ITG harness of wave 2.
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.
