# RWB-S5-E3024-APP Record and track the asset stock balance

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3024-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-G |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S5-E3024-APP-16) |
| Depends on (build) | RWB-S5-E3024-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | rwb-asset.yaml info.version 5.0.0 (Recovery Workbench API Specification v5); REST base /api/recovery/asset/v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-024 split out for rwb-asset. The four legacy acceptance criteria are kept word for word with their origin tag; the feature now gives the stock balance one accountable owner and one number on SCR-21 and SCR-22, computed from the `asset` rows of `rwb_asset` and confirmed by a step of `AssetDisposalWorkflow` on task queue `rwb-asset`, with the confirmation written to the local decision record before the balance is shown as confirmed (DP-03). The legacy `v_ace_npa_asset` and `v_ace_account` reads are retired as service reads because rwb-asset holds no ACE view grant, so the ACE asset fact arrives on the rwb-source-data data-product contract (DP-05); the base becomes `/api/recovery/asset/v1` (DP-13); SCR-21 and SCR-22 read through the gateway-bff composite route (DP-19). The take-on routes of R-DIS-01 and R-DIS-02 are built by the sibling stories of this service and are carried here because the legacy key restates them (GAP-2860; ASM-4737). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3024-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 22 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **NPA and asset manager (RW-NPAMGR)**, I want **the asset stock balance to have one accountable owner and one number on one screen, and every take-on of an asset to move that number**, so that **the bank stops keeping the NPA stock balance in hand-checked listings and floor prices across several owners and the 1,486-day NPA sales cycle moves to the 1,095-day target**.

This is the application slice of legacy RWB-E3-024. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the messages, screens and rules they depend on;
- the stock-balance figure: for a scope and an as-at date, the count of assets held and the totals of `book_value` and `holding_cost_to_date` of the `asset` rows, grouped by `holding_status`, computed from `rwb_asset` and never stored in a second table (GAP-2860; ASM-4737);
- the accountable owner of the balance: the RW-NPAMGR role of FSD S5 A2.6.3.3, shown on the screen with the figure and with the as-at date, and read from the role matrix of rwb-access — never a person (BR7);
- the confirmation step `confirmStockBalance` of `AssetDisposalWorkflow` on queue `rwb-asset`: the officer task that confirms the figure for a scope and an as-at date;
- the local decision record of the confirmation, written through RWB-PLT-E1027-CON before the figure is shown as confirmed (DP-03);
- the two reads of SCR-21 Asset list and SCR-22 Asset record on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the two reads and of the confirmation, the `AssetStockBalance` element, the consumed rows, the error set and the fakes, which are RWB-S5-E3024-CON; the creation of the `asset` row under R-DIS-01 and R-DIS-02, which is RWB-S5-E3019-APP and RWB-S5-E3020-APP, and the LED route of R-DIS-03, which is RWB-S5-E3021-APP; the holding clocks and the provision steps of R-DIS-06, which are RWB-S5-E3023-APP; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the ACE NPA asset, collateral and account facts, which are rwb-source-data's (P1); the decision ledger rows and the rule rows, which are rwb-decision's (P7); the document and its custody, which are rwb-document's (P5); the money and any posting, which are rwb-payment's (P8); and the deployment of this build, which is the operations story of this legacy key and the wave 2 harness.

The word "owns" above needs one qualification, and it is the same one the sibling story RWB-S5-E3020-APP records: the legacy masters give the same R-DIS-01 and R-DIS-02 criteria to more than one story. This story keeps them word for word because the legacy key RWB-E3-024 lists them, and the write path they describe is the sibling stories' — what this story builds and proves is the balance those writes move (GAP-2860; ASM-4737).

### 2. Business rationale

Legacy RWB-E3-024 gave the Workbench one screen that would give the stock balance an owner and a number "on one screen. It has no owner today" (FSD S5 A2.6.1). The problem statement of the module is unchanged: the NPA sales cycle is 1,486 days and listings and floor prices are checked by hand; the metric is the same, measured on the decision log and the Workbench records, reviewed monthly, moving from 1,486 days to 1,095 days (FSD S5 A1.3 and A2.6.1).

What D-RCV-60 changes is who holds the figure and where it comes from. In the monolith the stock balance was read across the `recovery` schema, with `v_ace_account`, `v_ace_npa_asset` and the case in one query under one owner. In the target:

- **the figure is this service's.** `asset` is S5's table in `rwb_asset` with the holding status, the book value and the holding cost to date (TSD S5 T3.1; the `asset` row is absent from the Ownership Map table list and is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 — GAP-2860; ASM-4737), so the balance is a projection of this service's own rows and needs no cross-service join (DP-01).
- **the ACE asset fact stays with rwb-source-data (P1).** The legacy data table names `v_ace_npa_asset` and `v_ace_account`; in the target only rwb-source-data reads the 30 `recovery.v_ace_*` views (Architecture v5 slides 29, 37 and 45) and the S5 row of slide 13 names no call to P1, so DP-05 applies as a **prohibition** and the fact arrives on the owner's data-product contract (FSD P1 DP06 Collateral and assets — GAP-2860; ASM-4740).
- **the owner is a role, not a person.** FSD S5 A2.6.3.3 makes the NPA and asset manager the primary role of the feature and the Head of NPA the also-user; TSD S5 T6.1 gives both the Asset and disposal rights. The "owner" column of the balance is therefore a role code with scope, and no name of a person enters the figure, the decision record or a log (Template and Rules §R7.2 s17).
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the confirmation, which is what legacy AC1 asks for and what legacy AC4 tests.
- **the number is one deterministic figure.** Two officers on two screens on the same business date confirm the same figure from the same rows, so the count and the totals cannot differ between owners; the as-at date travels with the figure.

The case state and the take-on are unchanged and stay with their owners: the route states `ASSET_PENDING_TAKE_ON` and `ASSET_ON_BOOKS` are rwb-case's, written on the answer of the sibling take-on stories, and this story only counts the rows those answers produce. Nothing of the metric, of the `LOV-HOLDING` and `LOV-SEGMENT` values or of the one-working-day targets of R-DIS-01 and R-DIS-02 becomes a constant of this build: they are reference data and rule rows, read with their version.

### 3. Preconditions

- RWB-S5-E3024-CON is published: the `AssetStockBalance` element, the confirmation request and answer, the two reads, the consumed rows, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the confirmation and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-22 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The rwb-source-data data-product contract of DP06 Collateral and assets is published with its fake, so the ACE asset fact behind the displayed asset can be read on Day 1. Its operation name is Not specified in the source documents (GAP-2860; ASM-4740), and the row is not in this story's contract-dependency list, which is None.
- The rwb-case case-state read and the case-move answer are available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-2860; ASM-4737).
- The role matrix of rwb-access carries RW-NPAMGR and RW-HEADNPA with the Asset and disposal rights TSD S5 T6.1 gives them, so the owner shown on the screen is a role code the access service can resolve (GAP-2860; ASM-4739).
- `asset` and `listing` exist in schema `rwb_asset` from the DB story of this service, with the columns of DF-COL-028 to DF-COL-042 and DF-SAL-001 to DF-SAL-008 and the standard record columns of TSD S5 T3.0; this story adds no table, no column and no migration (GAP-2860; ASM-4741).
- The DISPOSAL rule package is in force at its version with R-DIS-01, R-DIS-02 and R-DIS-03; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The rule rows themselves are governed there and are not created by this story.
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_asset`, `recovery.v_ace_account` or `rwb_case` is refused by the database and fails the boundary test (DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S5-E3024-CON when its tests pass.

### 4. Flow

1. An asset is taken on by the step of RWB-S5-E3019-APP (R-DIS-01), RWB-S5-E3020-APP (R-DIS-02) or RWB-S5-E3021-APP (R-DIS-03): the `asset` row is inserted in `rwb_asset` with its `holding_status` of `LOV-HOLDING`, its `book_value` and its dates. This story writes no part of that row and adds no second take-on path.
2. The NPA and asset manager opens SCR-21 Asset list or SCR-22 Asset record through the gateway-bff composite route; the route asks rwb-asset for the balance and for the asset rows, rwb-case for the case and its route state, and rwb-source-data for the ACE asset fact (DP-19).
3. `AssetStockBalanceQuery` reads the `asset` rows of the scope in force from `rwb_asset` only, and groups them by `holding_status` (`HELD`, `LISTED`, `UNDER_OFFER`, `SOLD`, `TRANSFERRED`, `RENTED` of `LOV-HOLDING`): the count of assets, the sum of `book_value` (DF-COL-037) and the sum of `holding_cost_to_date` (DF-COL-042), with the as-at date and the segment scope of `LOV-SEGMENT` (GAP-2860; ASM-4737).
4. The answer names the accountable owner as the role code RW-NPAMGR with its scope, resolved from the role matrix, and never as a person (FSD S5 A2.6.3.3; GAP-2860; ASM-4739).
5. The officer confirms the figure for the scope and the as-at date; the confirmation step `confirmStockBalance` of `AssetDisposalWorkflow` on queue `rwb-asset` receives it. Where the read is taken between two take-ons, the figure is the one of the rows in the transaction the read sees, and the as-at date makes the difference visible.
6. `StockBalanceEvaluator` reads the DISPOSAL package version in force from rwb-decision and resolves the rule set of the confirmation (R-DIS-01, R-DIS-02 and R-DIS-03 are in the package of the same stage) with the balance inputs, so the record names the rule and the version that were in force when the figure was confirmed.
7. `StockBalanceDecisionRecordWriter` writes one decision record through the local decision-record library **before any change** (DP-03): the scope, the as-at date, the count, the two totals, the owner role, the rule ID with its version, the inputs reference and the outcome. A failed write changes nothing and the officer sees MSG-P7-003 (legacy AC4).
8. `AssetStockBalance` answers the confirmation with the confirmed figure, its owner, its as-at date and the record reference, and writes the idempotency row so that a repeated confirmation of the same scope and date writes no second record.
9. SCR-21 and SCR-22 show the confirmed figure next to the live figure of the read, the as-at date and the owner, with the loading, list and record states of FSD S5 A2.6 (`Loading; list` on SCR-21 and `Take-on; held; listed; sold` on SCR-22).
10. A take-on by a sibling story changes the live figure on the next read; nothing is pushed and no event is published by this story, so a stale screen shows its as-at date rather than a wrong number.
11. A repeated request with the same `Idempotency-Key`, or a confirmation of the same scope and as-at date twice, writes one record and answers once.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no confirmation, no record and no answer leaves the service | MSG-P7-003 | AC4, TC-E3-024-04, TC-E3-024-06 |
| X2 | The role does not hold the Asset and disposal right of the operation, or the scope excludes the segment | 403 before any read or write; the figure is not shown and no record is written | MSG-P4-002 | AC1, TC-E3-024-05 |
| X3 | A required field of the confirmation is absent or invalid (scope, as-at date, owner) | 422 and nothing is written | MSG-GEN-001 | AC1, TC-E3-024-01 |
| X4 | The as-at date is later than the business date in force | The confirmation is refused with the error envelope and nothing is written; the date is not raised as a business value | MSG-GEN-001 | AC1 |
| X5 | The ACE data product is stale after a late or failed batch | The asset fact of the displayed asset shows its date and the balance keeps its own as-at date; the confirmation is not blocked by a stale ACE batch, and the staleness is shown on the record screen | MSG-P1-001 | AC1 |
| X6 | The rwb-source-data or rwb-case contract does not answer inside 2 s, or its breaker is open | The screen shows the balance from this service's rows with the case and ACE parts marked unavailable; the caller sees 503 with the platform error envelope and nothing is written | None | AC1, AC2 |
| X7 | The asked scope has no `asset` row | 200 with a count of zero and empty totals, with the owner and the as-at date; no record is written until the officer confirms | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `recovery.assignment` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5, TC-E3-024-08, BR3, BR5 |

X1 and X2 are the exception paths of RWB-E3-024 carried onto the split (`Statement` and `Access` in the legacy test cases), X3 to X7 are the paths the target read and the confirmation add, and X8 is the DP-05 and DP-01 boundary. The one-working-day targets of R-DIS-01 and R-DIS-02 and the 12-month appraisal age of MSG-S5-002 stay values in force and are not constants of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3024-CON, the rwb-source-data and rwb-case fakes, the access role fake and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The query and activity names, the decision code and the element names beyond the sources are this story's choice; the rules, the messages, the screens, the reads and the lists are fixed |
| Valuable | One owner and one number for the stock balance, with the as-at date and the decision recorded, on the screens the officers already use |
| Estimable | One query, one evaluator, one confirmation step, one record write, two reads, three clients and two screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic assets and ACE facts through the contract fakes, plus the component cases of the refusal and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Record and track the asset stock balance

  Background:
    Given case "RC-2026-000524" carries asset "AST-2026-000524" in the DISPOSAL stage
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-01, R-DIS-02 and R-DIS-03
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Record and track the asset stock balance (legacy RWB-E3-024 AC1)
    Given the rwb-source-data contract mock returns the ACE NPA asset "AST-2026-000524" with transfer_in_date "2026-11-20" and book value "4500000.00"
    Given the rwb-case contract mock returns the case state "ASSET_ON_BOOKS" for "RC-2026-000524"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then gives the stock balance an owner and a number on one screen. It has no owner today
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DIS-01 (legacy RWB-E3-024 AC2)
    Given the rwb-source-data contract mock returns the RPS repossession result of vehicle "AST-2026-000524" with condition "FAIR", three photographs and location "Bangkok"
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON" for "RC-2026-000524"
    Given a case in state ASSET_PENDING_TAKE_ON
    When repossession completed
    Then create the asset record from RPS with condition, photographs and location
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC3 Rule R-DIS-02 (legacy RWB-E3-024 AC3)
    Given the rwb-source-data contract mock returns the AMIS deed in lieu transfer of property "AST-2026-000524" with the opening book value "4500000.00"
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON" for "RC-2026-000524"
    Given a case in state ASSET_PENDING_TAKE_ON
    When dil transfer registered
    Then create the asset record from AMIS with the opening book value
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded (legacy RWB-E3-024 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 No read outside the service schema (X8, BR3, BR5) (new, D-RCV-60)
    Given a component, a statement or a test reaches a `v_ace_*` view
    When the statement runs under the grant of `rwb_asset`
    Then the grant refuses the statement and the boundary test fails the build

  Scenario: AC6 Rules BR1 to BR9 hold on the balance (new, D-RCV-60)
    Given the `asset` rows of the scope exist in `rwb_asset`
    When the balance is read and confirmed
    Then the balance is computed from the `asset` rows of `rwb_asset` alone and is stored in no second table
    Then the confirmation is recorded before the figure is shown as confirmed
    Then the caller sees the owner as a role code and never as a person

  Scenario: AC7 A consumed call fails or does not answer (X6) (new, D-RCV-60)
    Given the rwb-case contract mock does not answer inside 2 s
    When the balance is read
    Then the screen shows the balance from this service's rows with the case and ACE parts marked unavailable
    Then the caller sees the platform error envelope and nothing is written

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change that the status model does not allow
    When the change is requested
    Then the change is refused and nothing is written

  Scenario: AC9 Error answers 401, 403 and 404 of the provided operations (new, D-RCV-60)
    Given a request to a provided operation carries no valid credential
    When the request is sent
    Then the caller sees 401 with the platform error envelope and nothing is written
    Given a request to a provided operation comes from a role without the Asset and disposal right or from a scope that excludes the segment
    When the request is sent
    Then the caller sees 403 with the platform error envelope and nothing is written
    Given a request to a provided operation names an asset that is not in the scope
    When the request is sent
    Then the caller sees 404 with the platform error envelope and nothing is written

  Scenario: AC10 Replay of a write with the same idempotency key (BR8) (new, D-RCV-60)
    Given a write has been accepted under an Idempotency-Key
    When the same write is sent again with the same Idempotency-Key
    Then the caller gets the same answer and no second decision record is written

  Scenario: AC11 A retried or timed-out activity (new, D-RCV-60)
    Given a step of AssetDisposalWorkflow on task queue rwb-asset is retried or times out
    When the activity runs again or the timeout is reached
    Then the confirmation is written once and the balance is not shown as confirmed before the decision record holds it
```

The four criteria are the legacy criteria of RWB-E3-024 word for word, with their origin tag added and one wording change, `decision log` to `decision record` (CG-ALL-9774): the repetition of `Then`, the legacy wording of `the user acts on the screen`, `It has no owner today`, `the action is taken` and `the decision record cannot be written` (changed from log) all stand, and the sentence of AC1 keeps its place inside `Then`. AC5 is the story's own criterion for the X8 boundary and carries no legacy origin tag. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text; the values they carry are synthetic fixtures and change no legacy value.

What the legacy lines describe happens in three places in the target. rwb-source-data answers the ACE asset fact of the take-on; the take-on step of RWB-S5-E3019-APP or RWB-S5-E3020-APP writes the `asset` row and the sibling answers the case move to rwb-case; and this story reads the `asset` rows, computes the count and the two totals, resolves the owner and writes the confirmation record. Two notes are recorded rather than smoothed over. AC2 and AC3 are the criteria that legacy RWB-E3-019 and RWB-E3-020 also carry, because the legacy masters duplicate the take-on rules across stories; this story keeps its copy word for word and proves it on the balance the take-on moves, while the write path itself is the sibling's (GAP-2860; ASM-4737). AC1 says the screen gives "a number"; no source says which figure that number is, so the count of assets held with the totals of book value and holding cost to date is the default, recorded as an assumption (GAP-2860; ASM-4737).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer | BR ID |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-01 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | REPOSSESSION_COMPLETED | asset_type = vehicle and statutory_notice_proved = Y | Create the asset record from RPS with condition, photographs and location | ASSET_ON_BOOKS | Sale officer | RPS, AMIS, Field App | 1 working day | BR10 |
| R-DIS-02 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | DIL_TRANSFER_REGISTERED | asset_type = property and transfer registered | Create the asset record from AMIS with the opening book value | ASSET_ON_BOOKS | Sale officer | AMIS, the Land Office | 1 working day | BR11 |
| VR-S5-006-1 | Asset disposal | None | Any | The confirmation is submitted | Required field empty | Refuse the request with MSG-GEN-001 | Unchanged | NPA and asset manager | Workbench | None | BR12 |

The two rule rows are the rows of the Business Rules and Routing Logic v4, copied character for character; VR-S5-006-1 is the validation rule of FSD S5 A2.6.3.1 and has no message of its own beyond MSG-GEN-001. Their owner column is a role of the business and not a service: the case moves of `ASSET_ON_BOOKS` are written by rwb-case on the sibling's answer, the `asset` row is written by the sibling step, and this story reads the row and records the confirmation. R-DIS-03 is in the rule set of the feature (FSD S5 A2.6.3.1) and belongs to RWB-S5-E3021-APP; it is not tabled here because no criterion of this key names it.

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The stock balance is computed from the `asset` rows of `rwb_asset` alone: the count, the sum of `book_value` and the sum of `holding_cost_to_date`, grouped by `holding_status`, for a scope and an as-at date, and it is stored in no second table | TSD S5 T3.1 and T3.2; Architecture v5 slide 41; DP-01; GAP-2860; ASM-4737 | AC1, TC-E3-024-01, AC6 |
| BR2 | The confirmation is recorded before the figure is shown as confirmed, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S5 T2 ("writes the decision log entry before any change"); legacy RWB-E3-024 AC1 and AC4 | AC4, TC-E3-024-04, TC-E3-024-06, AC6 |
| BR3 | The ACE asset and account facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the fact on the owner's data-product contract only | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2860; ASM-4740 | AC5, TC-E3-024-08, AC6 |
| BR4 | The case, its route states and its assignment are rwb-case's: this story reads the case state on its contract and writes no `recovery_case` and no `assignment` row | Ownership Map (recovery_case and assignment owner P3); GAP-2860; ASM-4737 | AC5, TC-E3-024-08, AC6 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id` and `collateral_id` of an `asset` row are identifiers of other services' facts; the `asset` row is this service's own holding record in `rwb_asset`, keyed by the ACE asset key with no foreign key and no copied ACE column, and the ACE asset stays read-only through the source-data contract | DP-01; TSD S5 T3.3 | AC5, TC-E3-024-08, AC6 |
| BR6 | The owner of the balance is a role code with a scope and never a person; the figure, the record, the log and the answer carry identifiers, codes, amounts, dates and a rule version only | Template and Rules §R7.2 (s17); TSD S5 T6.1; FSD S5 A2.6.3.3 | AC1, TC-E3-024-01, AC6 |
| BR7 | Every value a business person may change is reference data or a rule row read with its version: `LOV-HOLDING`, `LOV-SEGMENT`, `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN` and the rule rows of the DISPOSAL package | TSD S5 T3.2; FSD S5 BR-S5-006 | AC1, TC-E3-024-01, AC6 |
| BR8 | The same confirmation twice, or the same `Idempotency-Key` twice, writes one record and answers once | TSD S5 T-A.2; Architecture v5 slide 11 | TC-E3-024-09, AC6 |
| BR9 | This story publishes no event and consumes none: the balance changes on the read after a take-on, and no consumer group, subscription or inbox is created | Architecture v5 slide 19 IN and OUT; GAP-2860; ASM-4742 | TC-E3-024-07, AC6 |
| BR10 | Create the asset record from RPS with condition, photographs and location | Business Rules and Routing Logic v4 (R-DIS-01); legacy RWB-E3-024 AC2 | AC2, TC-E3-024-02 |
| BR11 | Create the asset record from AMIS with the opening book value | Business Rules and Routing Logic v4 (R-DIS-02); legacy RWB-E3-024 AC3 | AC3, TC-E3-024-03 |
| BR12 | Refuse the request with MSG-GEN-001 when a required field is empty | FSD S5 A2.6.3.1 (VR-S5-006-1) | AC1, TC-E3-024-01 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the move `ASSET_ON_BOOKS` is answered by the sibling take-on story and applied to the case of record by the parent `CaseWorkflow` (BR4). What this story owns is the state of the figure and the state of the confirmation.

| Figure state | Event | Condition | To |
|---|---|---|---|
| Live | A take-on writes an `asset` row | Any holding status of `LOV-HOLDING` | Live, with a new count and new totals on the next read |
| Live | The officer opens SCR-21 or SCR-22 | The role holds Asset and disposal R and the scope covers the segment | Shown with the owner and the as-at date |
| Shown | The officer confirms the figure | The request is valid and the record is written | Confirmed, with its record reference and as-at date |
| Confirmed | A later take-on writes an `asset` row | Any | Live again, with the confirmed figure kept as the previous as-at figure |
| Shown | The record cannot be written | X1 | Unchanged, nothing confirmed |
| Any | The contract of rwb-source-data or rwb-case does not answer inside 2 s | X6 | Shown from this service's rows only, with the case and ACE parts marked unavailable |

| Confirmation execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The officer submits a scope and an as-at date | The role and the scope check passes | Validating |
| Validating | The required fields are present and the date is not in the future | X3, X4 do not fire | Deciding |
| Deciding | The package in force is loaded and the rule set resolves | The record is written | Confirmed |
| Confirmed | The transaction commits | The idempotency row and the record are written | Waiting for the next confirmation |

The holding status values are those of `LOV-HOLDING` in TSD S5 T3.2 and the segment values those of `LOV-SEGMENT`; the figure has no state of its own in any source, so the three states above are this story's design and are recorded as such (GAP-2860; ASM-4742). The case route states, including `ASSET_PENDING_TAKE_ON` and `ASSET_ON_BOOKS`, belong to rwb-case and are not added to `LOV-HOLDING` or `LOV-SEGMENT` by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU in TSD S5 T6.1: the primary role of the feature and the accountable owner of the balance; confirms the figure for a scope and an as-at date; its scope is resolved from the rwb-access matrix |
| RW-HEADNPA, Head of NPA | Asset and disposal RA: reads the balance and approves where the figure is taken to the head of NPA; confirms through the approval path where the officer's scope does not cover the segment |
| RW-SALEOFF, sale officer | Asset and disposal CRUA: reads the balance and the asset rows of its own scope |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the balance of the enforcement assets |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-PRODHEAD, RW-HEADLIT, RW-HEADASL, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| PT-VALUER, PT-AUCTION, PT-RAMC | Asset and disposal R or RU as the TSD S5 T6.1 matrix gives it: a partner reads the assets of its own scope through the partner gateway and never the balance of a segment |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R or C as the matrix gives it: the service identities read and are subject to the same checks |
| rwb-asset service identity | Runs the confirmation step, resolves the rule version, writes the decision record and answers the reads; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S5 T6.1 and the capability rows of FSD S5 A2.6.3.3 and nothing wider: the FSD gives Asset and disposal R to RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF "and 23 more", and C to RW-ENFORCE, RW-SALEOFF, RW-NPAMGR and SY-DATALOAD, which the matrix covers. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here. The authorise check is the rwb-access authorise call of each operation in §12 against the capability area Asset and disposal and its right, made before any read or write (X2). The owner of the balance is resolved from the role matrix and not from a parameter, because DP-06 is not in the pattern set either (GAP-2860; ASM-4739).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-028 | asset (S5, `rwb_asset`) | id | Read, the identifier of the asset in the balance and of the record |
| DF-COL-029 | asset (S5, `rwb_asset`) | case_id | Read, to link the row to the case the screen shows |
| DF-COL-031, DF-COL-032 | asset (S5, `rwb_asset`) | asset_ref, asset_code | Read, the identifiers the balance list shows |
| DF-COL-033, DF-COL-034 | asset (S5, `rwb_asset`) | asset_type, transfer_in_type | Read, against `LOV-ASSET-TYPE` and `LOV-TRANSFER-IN`; the asset class of the grouping |
| DF-COL-035 | asset (S5, `rwb_asset`) | from_segment | Read, against `LOV-SEGMENT`; the scope of the balance and of the owner |
| DF-COL-036, DF-COL-039, DF-COL-040 | asset (S5, `rwb_asset`) | transfer_in_date, repossessed_date, stock_date | Read, the dates the screen shows next to the age of the asset |
| DF-COL-037 | asset (S5, `rwb_asset`) | book_value | Read, summed into the balance total |
| DF-COL-041 | asset (S5, `rwb_asset`) | holding_status | Read, against `LOV-HOLDING`; the grouping of the balance |
| DF-COL-042 | asset (S5, `rwb_asset`) | holding_cost_to_date | Read, summed into the balance total; written by RWB-S5-E3023-APP, never here |
| DF-SAL-001, DF-SAL-008 | listing (S5, `rwb_asset`) | id, status | Read only, the sale status of a listed asset in the balance list |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the figure is shown as confirmed |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more | Not read: this service holds no `v_ace_*` grant, and DP-05 applies as a prohibition (BR3) |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` (P1) | account_key, account_code, total_balance and 36 more | Not read: listed by the legacy story and owned by P1; no path of this story needs it |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and 17 more | Not read as a table: the case state arrives on the rwb-case answer |
| DF-WRK-009 to DF-WRK-016 | assignment (P3) | id, case_id, task_id and 2 more | Not read and not written: the assignment is P3's and no path of this story needs it |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set and 9 more | Not read as a table: the rule set arrives with the DISPOSAL package on `RulePackageInForce` |

Field IDs are those of TSD S5 T3.1 and T3.2 and the Logical Data Model and Data Dictionary v9; the ACE, case, assignment and rule rows are the rows the legacy story lists in its Data table, with their owners changed to P1, P3 and P7 by the target. **No new table, no new column and no migration**: `asset` and `listing` arrive with the DB story of this service, this story reads fourteen of their columns, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_asset` by the library's own migration (DP-03). The `asset` row is not in the Ownership Map table list; its owner is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 (GAP-2860; ASM-4737).

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_asset`, the decision record, a log, a screen answer or a workflow input, and every fixture is synthetic. The customer of the case is never named on the balance: the figure is an asset figure, and the case reference is the handle to the person only inside rwb-case.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the three operations RWB-S5-E3024-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, with the `AssetStockBalance` element: the count, the book-value total and the holding-cost total per `holding_status`, the owner role, the as-at date; filtered by type, status, region, page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| POST | Not specified in the source documents (GAP-2860): path reserved, to be published with the next API Specification version, on the base `/api/recovery/asset/v1` | The confirmation of the stock balance for a scope and an as-at date: one decision record and one answer, with the rule ID and the package version (BR2, BR8) | Asset and disposal, right C, scope applied | Idempotency-Key |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its holding status, its book value, its cost to date and its listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |
| POST | The confirmation of the balance: Not specified in the source documents (GAP-2860; ASM-4738) | `StockBalanceConfirmation` in, `AssetStockBalance` out with its record reference | Asset and disposal, right C, scope applied | `Idempotency-Key` header |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for an invalid field or an as-at date in the future, 409 for a repeated confirmation without the key and 503 when the decision library or a consumed contract does not answer. The two read operation IDs are those of TSD S5 T-A.1 and are not redefined here. `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's under the Ownership Map ruling ASM-0043; `POST /assets/{assetId}/listings` (API-S5-004) and `POST /listings/{listingId}/rounds` (API-S5-005) belong to the pricing and auction stories of this service, and `GET /assets/{assetKey}` is the key read of the same list. The confirmation has no operation in any source — the legacy endpoint table names only the valuation and the record read — so its path is carried as the placeholder and fixed by the assumption of the pattern table below (GAP-2860; ASM-4738).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2860; ASM-4740)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE NPA asset fact of the displayed asset: asset reference, asset code, asset type, transfer-in type, segment, taken-on date, book value and the freshness stamp of the data product; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the account link of the asset row; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2860; ASM-4737)) | rwb-case (P3) | P3 rwb-case | The answer that carries `ASSET_ON_BOOKS` with the rule and its version, consumed by the sibling take-on step on the workflow boundary; faked for the two criteria of §7 |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2860 with ASM-4740 and ASM-4737.

#### 12.3 Events published

None. The balance is a projection of this service's own rows and its confirmation writes a decision record, not an event; DP-09 is not in the pattern set of this key, and Architecture v5 slide 19 OUT gives the topic `rwb.asset.events.v1` to the take-on and sale events, which the sibling stories publish. A build that publishes from this story would need the outbox library and a new event name, and neither is in scope here (GAP-2860; ASM-4742).

#### 12.4 Events consumed

None. The balance needs no trigger of its own: it is read on demand and recomputed from the rows, and a take-on by a sibling story changes it without any message. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test (BR9).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the holding | `rwb-asset` | The stage that hosts the confirmation step; its signals and its outcome for the parent are declared by the sibling story, not redefined here |
| `confirmStockBalance` | Activity, the one confirmation step of this story | `rwb-asset` | In: the scope, the as-at date and the officer reference. Out: the confirmed `AssetStockBalance`, the record reference and the rule version |

The activity name is a target design choice of this story and is fixed by no source document. The confirmation is a human task of the officer, so the step runs on the officer's action and not on a timer; the read itself is a query and is not a workflow step.

The workflow ID form and start rule of `AssetDisposalWorkflow` are Not specified in the source documents (CG-ALL-9769): the Temporal Catalog v1 Workflows row gives neither a workflow ID form nor a duplicate-start policy.

#### 12.6 Schedules

None. The balance is read on demand and the confirmation is the officer's action; this story owns no Temporal Schedule and no legacy Quartz job, and it registers no Job of Architecture v5 slide 44. The single Schedule of this service is JOB-19 Re-appraisal monthly, which belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`) | The taken-on assets whose rows the balance counts; this story reads them and writes none |
| listing | S5 (`rwb_asset`) | The listing and its sale status shown next to a listed asset; read only here |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the confirmed figure (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated confirmation and the answer it holds |

Not owned and never read as a table: `recovery_case` and `assignment` (P3), `v_ace_npa_asset`, `v_ace_account` and the other `v_ace_*` views (P1), `document` (P5), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7). `asset_sale` is S5's and belongs to the sale stories; this story writes no sale. No foreign key leaves the schema and `asset.case_id` is an identifier, not a foreign key across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The ACE NPA asset `AST-2026-000524` with transfer-in date `2026-11-20` and book value `4500000.00`; the repossession result of a vehicle with condition `FAIR`, three photographs and location `Bangkok`; the deed in lieu transfer of a property with its opening book value; a stale product with its date; no answer beyond 2 s | AC1, AC2, AC3, X5, X6 |
| rwb-case case-state fake | The states `ASSET_PENDING_TAKE_ON`, `ASSET_ON_BOOKS` and `ASSET_HELD` of case `RC-2026-000524`; a case that is not in the state the rule expects | AC1, AC2, AC3 |
| rwb-case case-move fake | The move `ASSET_ON_BOOKS` accepted and refused | AC2, AC3 |
| rwb-access role fake | RW-NPAMGR and RW-HEADNPA with their Asset and disposal rights and scopes; a role without the right; a scope that excludes the segment | AC1, X2 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-01, R-DIS-02 and R-DIS-03 | AC1, AC4 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000524`, with the balance read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data read and of the case-move answer are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2860; ASM-4740).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The balance and the asset on `/api/recovery/asset/v1` and the confirmation; the rwb-source-data data-product read, the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event is published or consumed by this story |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and `confirmStockBalance` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `stock`, Java package `th.co.scb.ace.workbench.recovery.asset.stock`; front end `src/modules/recovery/asset/AssetStockBalance.tsx`, the fragment SCR-21 and SCR-22 embed.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the asset and account facts are the ones the rwb-source-data contract answers (Architecture v5 slides 29 and 41; GAP-2860; ASM-4740). DP-03 is the transaction rule of the confirmation: the record and the answer commit together or not at all. DP-13 moves the base of the two reads and of the confirmation and nothing else. DP-19 is how SCR-21 and SCR-22 reach this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The two H rows the pattern table adds are the ones the plan already carries. The three consumed rows (the rwb-source-data data product, the rwb-case state and the case-move answer) are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (GAP-2860; ASM-4740). No event is published, so no platform event library is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` confirmation branch | Workflow | The officer task that receives the scope and the as-at date and reports the confirmed figure |
| `confirmStockBalance` | Activity | The one step: validate, resolve the package in force, write the record, answer the figure |
| `AssetStockBalanceQuery` | Service | The projection: count, book-value total and holding-cost total per `holding_status`, for a scope and an as-at date, from `rwb_asset` only |
| `StockBalanceEvaluator` | Service | The rule set and the package version in force, with the segment and holding-status lists |
| `StockBalanceDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `AssetController` | Controller | The two reads, the confirmation, the capability area and right, the scope filter, the pagination and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `SourceDataProductClient` | Client | The ACE asset fact of `RWB-P1`, one hop, 2 s, breaker |
| `CaseStateClient` | Client | The case state read of rwb-case, one hop, 2 s |
| `AssetStockBalance` | React component | Shows the figure, its owner, its as-at date, the confirmed figure and the refusal, stale-data and unavailable-part states on SCR-21 and SCR-22 |

**Database and migrations.** No Flyway file. `asset` and `listing` arrive with the DB story of this service and the decision record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). No table and no column is added for the balance: the figure is computed, and the confirmed figure lives in its decision record (GAP-2860; ASM-4741).

**Configuration and reference data.**

- `LOV-HOLDING`, `LOV-SEGMENT`, `LOV-ASSET-TYPE` and `LOV-TRANSFER-IN` at their version in force (TSD S5 T3.2), read as reference data and never as constants.
- The reference-data contract that answers these lists: Not specified in the source documents (DOR-RWB-S5-E3024-APP-20); DP-06 and DP-07 are not in this story's pattern set.
- The DISPOSAL package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`.
- The capability area "Asset and disposal" and its rights, and the role codes RW-NPAMGR and RW-HEADNPA, are access rows of rwb-access read through the guard and the role matrix.
- The 2 s budget and the single hop are the platform rule of ADR-020; no parameter of the feature is named in any source (GAP-2860; ASM-4739).

**Build steps**

1. `AssetStockBalanceQuery` over the `asset` rows, with the grouping, the two totals, the scope and the as-at date (AC1, X7).
2. `AssetController` reads with the rights, the scope filter, the pagination and the problem mapping (AC1, X2, X3).
3. `SourceDataProductClient` and `CaseStateClient` against their fakes, with the 2 s budget, the breaker and the unavailable-part path (AC1, X5, X6).
4. `StockBalanceEvaluator` with the package in force and the lists (AC1).
5. `StockBalanceDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `confirmStockBalance` with the validation, the record, the idempotency row and the answer (AC1, X3, X4).
7. The two criteria of the take-on routes proved on the balance the sibling step moves, with the fake answers of AC2 and AC3 (AC2, AC3).
8. `AssetStockBalance` and the two screens through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read and no write to another service's schema (X8, BR3, BR5).

**Feature flag.** `rwb.asset.stock-balance-v1`, read as a flag of the platform library; off means the reads answer as before without the balance element and the confirmation is refused with the flag state, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the two reads and the confirmation answer in SIT on synthetic assets, the figure equals the count and the totals of the `asset` rows of the scope, a repeated confirmation writes once, a forced record failure changes nothing, no write to another service's table and no `v_ace_*` read exists in the build, and SCR-21 and SCR-22 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the confirmation is absent or invalid, or the as-at date is later than the business date (X3, X4, VR-S5-006-1) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the balance or confirms it, or the scope excludes the segment (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the figure is confirmed (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of the displayed asset is stale after a late or failed batch (X5) | {product} is from {date}. Today's load has not arrived. |
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this story raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this story raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |

The six message IDs are those of the legacy message set and of FSD S5 A2.6.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S5-001 and MSG-S5-002 are carried because they are in the message set of the feature, and no path of this story raises them.

### 15. Screens and states

SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its take-on, held, listed and sold states are served through the gateway-bff composite route (DP-19). The empty, error and no access states of SCR-21 are Not specified in the source documents (CG-ALL-9775); the empty, loading, error and no access states of SCR-22 are Not specified in the source documents (CG-ALL-9776). The route calls rwb-asset for the balance and the asset, rwb-case for the case and its route state and rwb-source-data for the ACE asset fact; this story fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the figure states of §9 on both screens — live, shown and confirmed, each with its owner, its as-at date and, where a take-on has happened since, the previous confirmed figure next to the live one — and the refusal and failure states: refused with MSG-P4-002, not recorded with MSG-P7-003, invalid with MSG-GEN-001, stale ACE data with MSG-P1-001 and the unavailable case or ACE part under X6. The take-on, held, listed and sold states of SCR-22 are those of the rules and are read from the same route; they are produced by the sibling stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-024-01 | AC1 | Component | Asset `AST-2026-000524` of case `RC-2026-000524` in `HELD` with book value `4500000.00`; the balance answers one count, two totals, the owner role and the as-at date, and the confirmation writes one record |
| TC-E3-024-02 | AC2 | Integration | The RPS repossession result of the vehicle with statutory notice proved; the sibling step writes the `asset` row, the case move is answered and the balance count rises by one on the next read |
| TC-E3-024-03 | AC3 | Integration | The AMIS deed in lieu transfer of the property with its opening book value; the `asset` row, the case move and the balance total asserted on the fakes |
| TC-E3-024-04 | AC4 | Component | The decision-record stub stopped; nothing confirmed, no record and MSG-P7-003 shown |
| TC-E3-024-05 | Access | Component | A role without the Asset and disposal right, and a scope that excludes the segment; 403 with MSG-P4-002 and no read |
| TC-E3-024-06 | Principle 5 | Component | A forced decision record write failure at the moment of the confirmation; no record, no confirmed figure and no change |
| TC-E3-024-07 | §12 operations, events and activities | Contract | The published contract of each operation of §12 checked against its fake; no event is published and no consumer group is created (BR9) |
| TC-E3-024-08 | AC5, X8, the tables of §12.7 (ASM-3438) | Boundary | A statement and a `v_ace_*` read attempted from the rwb-asset identity; the grant refuses both, and only the `rwb_asset` tables of §12.7 are read or written |
| TC-E3-024-09 | BR8 | Component | The same confirmation sent twice with the same Idempotency-Key; one decision record and one answer |
| TC-E3-024-10 | AC6, BR1 to BR9 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3024-APP-AC6) |
| TC-E3-024-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3024-APP-AC10) |
| TC-E3-024-12 | AC8 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3024-APP-AC11) |
| TC-E3-024-13 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-S5-E3024-APP-AC7) |
| TC-E3-024-14 | AC10, BR8 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3024-APP-AC8) |
| TC-E3-024-15 | AC11 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3024-APP-AC9) |

The six legacy cases are the legacy cases of RWB-E3-024 in their legacy order, with the Level column added: the two take-on cases map to `Integration` because they cross the rwb-source-data, rwb-case and sibling-step boundaries, and the other four map to `Component` because they are tested on the service and its fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness, which owns the cross-service journey of the key.

### 17. Guardrails

- No business value in code: the lists, the rule rows, the segment scopes, the one-working-day targets and the appraisal age stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_asset`, in the balance answer, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic. The customer of the case is never named on the balance.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case, its route states and its assignment stay with rwb-case, the rule rows with rwb-decision and the money with rwb-payment: no `recovery_case`, `assignment`, `rule_row` or posting is read or written here (BR3, BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no second balance table and no event on the topic.
- The decision is recorded before the figure is confirmed; a build that shows a confirmed figure without its record fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| Not specified in the source documents (GAP-2860; ASM-4737) | No requirement ID is mapped to FEAT-AST-06: TSD S5 T8 maps REQ-S5-001 to REQ-S5-005 to FEAT-AST-01 and REQ-S5-006 to REQ-S5-010 to FEAT-AST-08, and the split plan carries no requirement id for this slice. The feature is FEAT-AST-06 "Record and track the asset stock balance" with the objective, problem and metric of FSD S5 A2.6.1, and the legacy requirement it serves is RWB-E3-024 | The balance read, the owner, the confirmation and its record | TC-E3-024-01, TC-E3-024-04 | FEAT-AST-06 | Not specified in the source documents (DOR-RWB-S5-E3024-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the asset rows the balance counts | TC-E3-024-01 | FEAT-AST-06 | Not specified in the source documents (DOR-RWB-S5-E3024-APP-2) |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login | TC-E3-024-06 | FEAT-AST-06 | Not specified in the source documents (DOR-RWB-S5-E3024-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget | TC-E3-024-02, TC-E3-024-03 | FEAT-AST-06 | Not specified in the source documents (DOR-RWB-S5-E3024-APP-2) |
| ADR-022 | Local decision record plus central ledger | The confirmation record written before the figure is confirmed | TC-E3-024-04, TC-E3-024-06 | FEAT-AST-06 | Not specified in the source documents (DOR-RWB-S5-E3024-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-024, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E3-024-01 to TC-E3-024-15 |
| Feature and screens | FEAT-AST-06, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-01 and R-DIS-02 and VR-S5-006-1, named from the Business Rules and Routing Logic v4 and FSD S5 A2.6.3.1 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two reads and of the confirmation, the `AssetStockBalance` element, the consumed rows, the error set and the fakes: RWB-S5-E3024-CON.
- The creation of the `asset` row under R-DIS-01, R-DIS-02 and R-DIS-03 and the answer of the case move `ASSET_ON_BOOKS`: RWB-S5-E3019-APP, RWB-S5-E3020-APP and RWB-S5-E3021-APP (GAP-2860; ASM-4737).
- The holding-age clock, the provision steps and the monthly cost of carry that feed `holding_cost_to_date`: RWB-S5-E3023-APP, with the posting in rwb-payment (P8).
- The case of record, its route states, its assignment and the parent `CaseWorkflow`: rwb-case (P3), whose state this story consumes and fakes.
- The ACE NPA asset, collateral and account facts and the freshness of the data product: rwb-source-data (P1) (GAP-2860; ASM-4740).
- The authoring, testing, approval and versioning of the DISPOSAL package and of the rule rows: rwb-decision (P7).
- The valuations of the asset: rwb-valuation (S1) under API-S5-003 and ASM-0043.
- The listing, the floor price, the auction rounds and the sale: the pricing and auction stories of this service, API-S5-004 and API-S5-005; the balance shows the sale status and computes no price.
- The document, its custody and its retention: rwb-document (P5).
- The reporting projection of the stock balance: rwb-reporting (P9), which reads the operation and receives no event from this story (BR9).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
