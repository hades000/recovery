# RWB-S5-E3029-APP Publish the listing

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3029-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-L |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-S5-E3029-APP-16) |
| Depends on (build) | RWB-S5-E3029-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | rwb-integration for the publication to the EASY app and the pause; rwb-partner for the auction portal publication; consumed as a placeholder until the contract exists (GAP-2886; GAP-1756) |
| Contract version | v1, base `/api/recovery/asset/v1` (DP-13); the round is the sub-resource `POST /listings/{listingId}/rounds` of the listing, and the architecture slide's `POST /auction-rounds` names the same resource (GAP-1754) |
| Integration dependencies | HOME.SCB (officer step until INT-27 exists), EASY app and auction portal (GAP-1756; GAP-2886) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-029 split out for rwb-asset. The four legacy acceptance criteria are kept word for word with their origin tag; the publication is now one step of `AssetDisposalWorkflow` on task queue `rwb-asset` that evaluates R-DIS-33 on the evidence of the case, opens one `listing` row per channel in `rwb_asset` with `LIVE` status and its price and schedule, records the decision through the local decision-record library before the row changes (DP-03), sends the publication to the three channels of the criterion, and answers the case move to rwb-case. R-DIS-67 pauses the live listing and its price schedule. The legacy `v_ace_npa_asset`, `recovery_case`, `deviation` and `rule_row` reads are retired as service reads because this service holds no ACE view grant and no grant on another owner's schema, so those facts arrive on their owners' contracts (DP-05); the base becomes `/api/recovery/asset/v1` (DP-13); SCR-21 and SCR-23 read through the gateway-bff composite route (DP-19). The `listing` row is absent from the legacy Data table and its channels, schedule and pause have no column, no list value and no adapter owner (GAP-2885, GAP-2887; ASM-4781, ASM-4783, ASM-4784). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3029-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 19 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **the Workbench to publish an approved asset listing to the bank's channel, the EASY app and the auction portal in one action, with its price and schedule and with the floor withheld, and to pause it when a deviation is raised**, so that **an approved asset reaches the market the same day instead of waiting on a manual re-key into each channel, and the bank stops advertising assets while a deviation is open**.

This is the application slice of legacy RWB-E3-029. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- one publication step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slide 19, `AssetDisposalWorkflow`);
- the evaluation of R-DIS-33 on the evidence of the case and of R-DIS-67 on an open deviation, with the DISPOSAL package version in force;
- one `listing` row per published channel in schema `rwb_asset`, with the columns of DF-SAL-001 to DF-SAL-008 and no new column;
- the publication of the price and the price schedule to HOME.SCB, the EASY app and the auction portal, with the floor withheld, through the integration contract;
- the pause command of R-DIS-67 and the pause marker of the live listing and its price schedule;
- the local decision record of each outcome, written through RWB-PLT-E1027-CON before any row changes (DP-03);
- the answer to rwb-case for the two case moves `LISTING_LIVE` and `DISPOSAL_PAUSED_DEVIATION`, with the rule ID and the version that produced them;
- the two reads behind SCR-21 Asset list and SCR-23 Listing and price on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the operation and the two reads, the `Listing` element, the channel set, the case-move answer, the error set and the fakes, which are RWB-S5-E3029-CON; the start and floor price and their approval, which are FEAT-AST-11 and its story; the descending ladder, the rounds and the re-listing, which are FEAT-AST-13 and its stories; the case of record, its route states `FLOOR_APPROVED`, `LISTING_LIVE` and `DISPOSAL_PAUSED_DEVIATION` and the parent `CaseWorkflow`, which are rwb-case (P3); the document set of the evidence, which is rwb-document (P5); the ACE NPA asset fact, which is rwb-source-data's (P1); the deviation and its codes, which are rwb-deviation's (S8); the external channel adapters, which are rwb-integration's (P2); and the deployment of this build, which is the operations story of this legacy key and the wave 2 harness.

### 2. Business rationale

Legacy RWB-E3-029 gave the Workbench one action that put an approved asset on the market, and the program keeps the requirement unchanged: REQ-S5-005, "Listings are published to the bank's channel and the auction portal from one action" (Business Requirements Program v5, Must, owner Head of NPA). The feature keeps the same sentence: FEAT-AST-12 "puts the asset on HOME.SCB and the auction portal with its price and schedule", runs unattended, and depends on FEAT-AST-11 (Epics 3 to 8 Specification v3). The value of the story is therefore not a new business outcome but the loss of a manual re-key across three channels and the loss of a listing that keeps advertising an asset while a deviation is open.

What D-RCV-60 changes is who owns each fact of the publication. In the monolith the step read the case, the deviation, the ACE asset and the rule row inside one `recovery` schema and wrote the listing, the case stage and the decision log row in one process. In the target:

- **the listing record is this service's.** `listing` and `asset_sale` are S5's tables in `rwb_asset`, and Architecture v5 slide 41 gives rwb-asset "assets taken on, holding, floor price, listings, auction rounds" (Ownership Map: `listing` and `asset_sale` owner S5). `listing` is the table the legacy story never names in its Data table although the feature writes it (GAP-2885; ASM-4781).
- **the case of record stays with rwb-case (P3).** `recovery_case` and the route states are P3's; this story evaluates the rule, writes the listing, records the decision and **answers** rwb-case for the case move (GAP-2885; ASM-4781).
- **the evidence stays with its owners.** `photographs_count`, `inspection_report` and `title_status` are the condition facts of R-DIS-33: the photograph set and the inspection report are documents of rwb-document (P5), and the title status is an asset fact of rwb-source-data (P1). Neither is copied into `rwb_asset` (GAP-2885; ASM-4781).
- **the deviation stays with rwb-deviation (S8).** `deviation_open` in (X1, X4, X5) is S8's fact; Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched` and no deviation event, so the fact reaches the step on the case signal the parent forwards and on the rwb-deviation contract (GAP-2885; ASM-4781).
- **the publication leaves the service through the integration contract.** HOME.SCB, the EASY app and the auction portal are outside systems; the plan's pattern set for this key carries no DP-16 and no C row, so the adapter is named as a consumed contract with a placeholder rather than decided in code (GAP-2885; ASM-4781).
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the listing change, which is what legacy AC1 asked for and what legacy AC4 tested.

No business value moves: the channel set, the evidence conditions, the deviation codes and the price schedule are values of the rule package and of reference data, read with their version and never written in code.

### 3. Preconditions

- RWB-S5-E3029-CON is published: the publish operation, the two reads, the `Listing` element, the channel set, the consumed rows, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-source-data contract of DP06 Collateral and assets is published with its fake, so the ACE asset fact and the title status of the case can be read on Day 1. Its operation names are Not specified in the source documents (GAP-2885; ASM-4781), and neither row is in this story's contract-dependency list, which is None.
- The rwb-document document-set contract is published with its fake, so the photograph count and the inspection report of the case can be read. Its operation name is Not specified in the source documents (GAP-2885; ASM-4781).
- The rwb-deviation deviation contract is published with its fake, so the open deviation codes of the case can be read and R-DIS-67 evaluated. Its operation name is Not specified in the source documents (GAP-2885; ASM-4781).
- The rwb-integration channel contract is published with its fake, so a publication and a pause can be sent to HOME.SCB, the EASY app and the auction portal on Day 1. Its operation names, its request shape and its per-channel answer are Not specified in the source documents (GAP-2885; ASM-4781).
- The case state and the case-move answer of rwb-case are available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-2885; ASM-4781).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the listing row and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-23 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `listing` exists in schema `rwb_asset` from the DB story of this service, with the columns of DF-SAL-001 to DF-SAL-008 and the standard record columns of the physical schema; this story adds no table, no column and no migration.
- The DISPOSAL rule package is in force at its version with R-DIS-33 and R-DIS-67; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The rule rows and the LOV values are governed there and are not listed for this story.
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_asset`, `recovery_case` or `deviation` is refused by the database and fails the boundary test (DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S5-E3029-CON when its tests pass.

### 4. Flow

1. The sale officer or the case completes the evidence of the case: at least one photograph, an inspection report and a clear title (R-DIS-33 condition). The evidence is not copied here; the step reads it on the document contract and the source-data contract (GAP-2885; ASM-4781).
2. The publication step of `AssetDisposalWorkflow` on queue `rwb-asset` receives the trigger for a case in `FLOOR_APPROVED` and reads the case state and the case reference on the rwb-case contract, read only.
3. The step reads the asset fact of the case on the rwb-source-data contract: asset reference, asset key, asset type, segment, book value and title status, one hop with a 2 s budget and a breaker.
4. The step reads the evidence of the case on the rwb-document contract: the photograph count and the presence of the inspection report, with the document references.
5. `ListingEvaluator` loads the DISPOSAL package version in force from rwb-decision and evaluates R-DIS-33: `photographs_count` above 0, `inspection_report` present and `title_status` clear (Business Rules and Routing Logic v4).
6. Where the condition does not hold, no rule of this story fires: the step changes nothing, returns the blocking reason to the parent, and the blocked-publication path of R-DIS-34 and R-DIS-35 is not this story's (it belongs to the sibling stories of the feature).
7. `ListingDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the asset reference, the rule ID with its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. `ListingWriter` opens one `listing` row per published channel in one `rwb_asset` transaction with the decision record and the idempotency row: `id` (DF-SAL-001), `asset_key` (DF-SAL-002), `sale_channel` (DF-SAL-003 against `LOV-SALE-CHANNEL`), `start_price` (DF-SAL-004), `floor_price` (DF-SAL-005), `round_no` (DF-SAL-006) at 1, `listed_at` (DF-SAL-007) at the publication time and `status` (DF-SAL-008) at `LIVE`.
9. `ChannelPublisher` sends one publication per channel to HOME.SCB, the EASY app and the auction portal through the integration contract: the asset reference, the channel, the start price, the price schedule and the listing period, **with the floor withheld**, and the answer of each channel is held in the idempotency row.
10. `CaseMoveAnswer` answers rwb-case with the move `LISTING_LIVE`, the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither.
11. On a deviation in (X1, X4, X5) for a case in `LISTING_LIVE`, `pauseListing` evaluates R-DIS-67, records the decision, sends the pause to the three channels, marks the listing row's `state` and answers the move `DISPOSAL_PAUSED_DEVIATION`. The pause marker value is Not specified in the source documents (GAP-2885; ASM-4781).
12. A repeated evidence fact with the same case, asset and rule version writes nothing, publishes no second time, sends no second answer and counts the repeat.
13. SCR-23 Listing and price and SCR-21 Asset list read the listing, its prices, its channel, its status and its schedule from this service through the gateway-bff composite route, read only, next to the case and the route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no listing row, no publication and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E3-029-04, TC-E3-029-06 |
| X2 | The role does not hold the Asset and disposal right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E3-029-05 |
| X3 | The case is not in `FLOOR_APPROVED`, or not in `LISTING_LIVE` for a pause | 409 and nothing is written; the rule is not re-evaluated on a case that has already moved | None | AC2, AC3 |
| X4 | The evidence is incomplete (no photograph, no inspection report or the title not clear) | No rule of this story fires: nothing changes, no publication is sent and the case keeps its state | None | AC2 |
| X5 | A channel refuses the publication or does not answer inside 2 s | The listing row of that channel is not set to `LIVE`, the other channels stand, the refusal is returned with the platform error envelope and the step retries on the workflow's own schedule | None | AC1, X6 |
| X6 | The rwb-source-data, rwb-document or rwb-case contract does not answer inside 2 s, or its breaker is open | The step waits and retries; nothing is written and no case move is answered, and the caller sees 503 | None | AC1, AC3 |
| X7 | The same evidence fact or the same `Idempotency-Key` arrives twice | One row set, one publication set and one answer; the repeat is counted and no second decision record is written | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, `recovery_case`, `deviation` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5, TC-E3-029-08, BR3, BR5 |

X1 to X4 are the exception paths of RWB-E3-029 carried onto the split, X5 to X7 are the paths the target call types and the channel publication add, and X8 is the DP-05 and DP-01 boundary. The channel set and the evidence conditions are values in force, so none of them is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3029-CON and the rwb-source-data, rwb-document, rwb-deviation, rwb-case and rwb-integration fakes, on its own schema, and needs no live P1, P2, P3, P5, P7 or S8 |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the channel set and the `listing` columns are fixed |
| Valuable | An approved asset is on the bank's channel, the EASY app and the auction portal the same day with its price and schedule and with the floor withheld, and it stops advertising while a deviation is open |
| Estimable | One workflow step, one pause command, one evaluator, one record write, one row insert per channel, one publication per channel, one case-move answer, four clients and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases, evidence sets and asset facts through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Publish the listing

  Background:
    Given case "RC-2026-000512" carries the approved asset "AST-2026-000512"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-33 and R-DIS-67
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Publish the listing (legacy RWB-E3-029 AC1)
    Given the rwb-source-data contract mock returns the asset fact of asset "AST-2026-000512" with its book value, segment and title status "clear"
    Given the rwb-document contract mock returns three photographs and the inspection report of case "RC-2026-000512"
    Given the rwb-case contract mock returns the case state "FLOOR_APPROVED" for "RC-2026-000512"
    Given the rwb-partner contract mock returns the auction portal accepted the listing
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then puts the asset on HOME.SCB and the auction portal with its price and schedule
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DIS-33 (legacy RWB-E3-029 AC2)
    Given the rwb-source-data contract mock returns title status "clear" for asset "AST-2026-000512"
    Given the rwb-document contract mock returns three photographs and the inspection report of case "RC-2026-000512"
    Given a case in state FLOOR_APPROVED
    When listing evidence complete
    Then publish the listing to HOME.SCB, the EASY app and the auction portal, with the floor not published
    Then the case moves to LISTING_LIVE

  Scenario: AC3 Rule R-DIS-67 (legacy RWB-E3-029 AC3)
    Given the rwb-deviation contract mock returns deviation "X4" open for case "RC-2026-000512"
    Given the rwb-case contract mock returns the case state "LISTING_LIVE" for "RC-2026-000512"
    Given a case in state LISTING_LIVE
    When deviation raised
    Then pause the listing and the price schedule
    Then the case moves to DISPOSAL_PAUSED_DEVIATION

  Scenario: AC4 Not recorded (legacy RWB-E3-029 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Boundary of the schema (X8) (new, D-RCV-60)
    Given a component, a statement or a test reaches a `v_ace_*` view, `recovery_case`, `deviation` or another service's schema
    When the boundary test runs in the build
    Then the grant refuses the statement, the build fails and nothing is released

  Scenario: AC6 A consumed call fails or does not answer (NEWAC-RWB-S5-E3029-APP-AC10) (new, D-RCV-60)
    Given the rwb-integration contract mock does not answer the publication of the listing of asset AST-2026-000512
    When the publication is sent
    Then the case does not move to LISTING_LIVE and the channel is shown as not published after X5

  Scenario: AC7 A status change the model does not allow is refused (NEWAC-RWB-S5-E3029-APP-AC11) (new, D-RCV-60)
    Given a case in state LISTING_LIVE for "RC-2026-000512"
    When the publication of the listing of asset "AST-2026-000512" is requested
    Then the request is refused with 409 and nothing is written

  Scenario: AC8 Rules BR1 to BR10 hold on the publication (NEWAC-RWB-S5-E3029-APP-AC6) (new, D-RCV-60)
    Given a case in state FLOOR_APPROVED for "RC-2026-000512"
    When the publication of the listing of asset "AST-2026-000512" is sent
    Then the listing rows, the decision record and the case move are written on rwb_asset only, the payload carries the start price and the schedule and not the floor, and no person name, address, contact value or identity number is written

  Scenario: AC9 Error answers 401, 403 and 404 of the provided operations (NEWAC-RWB-S5-E3029-APP-AC7) (new, D-RCV-60)
    Given a request to the publish operation without an authenticated identity, from a role without the Asset and disposal right, or for a case id that does not exist
    When the publish operation is called
    Then the answer is 401 without an identity, 403 with MSG-P4-002 for the role, or 404 for the unknown case, and nothing is written in any of the three

  Scenario: AC10 A replayed write with the same Idempotency-Key (NEWAC-RWB-S5-E3029-APP-AC8) (new, D-RCV-60)
    Given the same Idempotency-Key arrives twice for the publication of the listing of asset "AST-2026-000512"
    When the second request is processed
    Then one row set, one publication set and one case-move answer exist, the repeat is counted and no second decision record is written

  Scenario: AC11 A retried or timed-out activity (NEWAC-RWB-S5-E3029-APP-AC9) (new, D-RCV-60)
    Given the rwb-case contract mock does not answer inside 2 s for case "RC-2026-000512"
    When the publication step runs
    Then nothing is written, no case move is answered, the caller sees 503 and the step retries on the workflow's own schedule
```

The four criteria are the legacy criteria of RWB-E3-029 word for word except the origin tag and the replacement of `decision log` by `decision record` (CG-ALL-9931): the legacy wording of `the action is taken`, `the decision record cannot be written`, `its trigger arrives` and `with the floor not published` all stand. The cross-service parts are mocked, so each criterion carries `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in four places in the target: the owners answer the asset fact, the evidence and the deviation; this story evaluates R-DIS-33 or R-DIS-67, writes the decision record and the `listing` rows, sends the publication or the pause and answers the case move; rwb-case writes the move to `LISTING_LIVE` or `DISPOSAL_PAUSED_DEVIATION`; and rwb-integration carries the publication to the EASY app; the auction portal publication is issued through rwb-partner, and the HOME.SCB publication is recorded as an officer step with its date and reference until INT-27 exists (GAP-1756). AC2 names three channels while `listing.sale_channel` holds one value per row and `LOV-SALE-CHANNEL` holds no value for HOME.SCB or the EASY app, so the channel-to-value mapping is read as reference data and is not decided here (GAP-2885; ASM-4781).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-33 | Asset disposal | D8.1 to D8.3 | FLOOR_APPROVED | LISTING_EVIDENCE_COMPLETE | photographs_count above 0 and inspection_report present and title_status = clear | Publish the listing to HOME.SCB, the EASY app and the auction portal, with the floor not published | LISTING_LIVE | Workbench | HOME.SCB, auction portal | per asset class |
| R-DIS-67 | Asset disposal | D8.1 to D8.3 | LISTING_LIVE | DEVIATION_RAISED | deviation_open in (X1, X4, X5) | Pause the listing and the price schedule | DISPOSAL_PAUSED_DEVIATION | Deviation owner | Workbench, auction portal | None |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the listing row is written here, the case moves are written by rwb-case on this story's answer, and the channel publication is executed by rwb-integration. R-DIS-32, R-DIS-34, R-DIS-35 and R-DIS-68 are adjacent rules of the same disposition machine; they are not in the criteria of this story and are not tabled here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The listing record is this service's: its asset key, channel, prices, round, listed time and status are columns of `listing` in `rwb_asset`, and no other service writes them | Architecture v5 slide 41 (rwb-asset owns floor price, listings, auction rounds); physical schema `listing`; ASM-4781 |
| BR2 | The decision is recorded before the listing rows change, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; legacy RWB-E3-029 AC1 and AC4 |
| BR3 | The ACE asset fact, including the title status, stays with rwb-source-data: this story reads no `v_ace_*` view and no ACE table | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2885 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states `FLOOR_APPROVED`, `LISTING_LIVE` and `DISPOSAL_PAUSED_DEVIATION` are rwb-case's | Ownership Map (recovery_case owner P3); GAP-2885 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_asset`; `asset_key` is the ACE business key and `listing_id` stays inside the schema | DP-01; physical schema comment "business key; no foreign key" |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: `LOV-SALE-CHANNEL`, `LOV-LISTING`, the evidence conditions, the deviation codes and the price steps | physical schema `listing`; legacy Guardrails |
| BR7 | One `listing` row per published channel, and one decision record per outcome, not per channel | Legacy AC2 channel set; DP-03 |
| BR8 | The floor is never sent to a channel: the publication payload carries the start price and the schedule only | Legacy RWB-E3-029 AC2, "with the floor not published" |
| BR9 | The same evidence fact twice, or the same `Idempotency-Key` twice, writes once, publishes once and answers the case move once | Architecture v5 slide 11; DP-11 |
| BR10 | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, a log, a publication or a workflow input | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story does own is the status of the listing and the state of the step.

| From (`listing.status`) | Event | Condition | To |
|---|---|---|---|
| None, no row | The evidence fact under R-DIS-33 | photographs_count above 0 and inspection_report present and title_status = clear | One row per channel in `LIVE`, with its `listed_at` and `round_no` 1, and the case-move answer `LISTING_LIVE` |
| None, no row | The evidence fact under R-DIS-33 | The condition does not hold (X4) | No row, no publication and no answer |
| LIVE | A deviation in (X1, X4, X5) under R-DIS-67 | deviation_open in (X1, X4, X5) | `LIVE` unchanged, the pause marker in `state`, the pause sent to the three channels and the case-move answer `DISPOSAL_PAUSED_DEVIATION` |
| LIVE, UNDER_OFFER, SOLD, WITHDRAWN | Any evidence fact for the same asset | X7 | Unchanged, the repeat is counted |
| DRAFT | The evidence fact under R-DIS-33 where the pricing story has already written the draft row | The condition holds | The same row set to `LIVE`, with `listed_at` stamped |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The evidence fact arrives for a case in `FLOOR_APPROVED` | The package in force is loaded | Evaluating |
| Evaluating | The rule fires | The decision record is written | Publishing |
| Publishing | The channels answer and the case-move answer is sent | The transaction commits | Waiting for the next fact |
| Publishing | A channel refuses or does not answer | X5 | Held for that channel, nothing committed for it, retried on the workflow's schedule |
| Publishing | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | A deviation fact arrives for a case in `LISTING_LIVE` | R-DIS-67 fires | Pausing, then back to Waiting |

`LOV-LISTING` gives the listing statuses DRAFT, LIVE, UNDER_OFFER, SOLD and WITHDRAWN, and `LOV-SALE-CHANNEL` gives DUTCH_AUCTION, BROKER, DIRECT, LED_AUCTION and RAMC. The route states `FLOOR_APPROVED`, `LISTING_LIVE` and `DISPOSAL_PAUSED_DEVIATION` are case route states of the DISPOSAL machine; they are not values of `LOV-LISTING` or `LOV-SALE-CHANNEL` and live on the case of record.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA: the primary role of the feature, holding C, R, U and A on the asset and publishing the listing |
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU: reads the listing, corrects the channel and re-publishes after a refusal |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the asset and publishes the listing of an enforced asset |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | Asset and disposal RA: read, and approve through the approval path where a floor needs it; the floor approval itself is FEAT-AST-11 |
| PT-AUCTION, PT-RAMC, PT-VALUER | Asset and disposal R as the access matrix gives it: the partner sees its own listings through the partner gateway, never the publication decision |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal C, R or U as the matrix gives it: the service identities publish and are subject to the same checks |
| rwb-asset service identity | Runs the step and the pause, evaluates the rules, writes the decision record and the listing rows, sends the publication, and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of the legacy permission table of RWB-E3-029 and of the access matrix of the module, and nothing wider. The feature "runs unattended" with the sale officer as also-user, and both statements hold: the step runs under the service identity with no officer task on the happy path, and the sale officer is the primary role when a person does act, on SCR-23 and on the correction paths. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here. The check is the rwb-access authorise call on the capability area and right above; its operation name is Not specified in the source documents (DOR-RWB-S5-E3029-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-001 | listing (S5, `rwb_asset`) | id | Write, the listing reference of the row and the publication |
| DF-SAL-002 | listing (S5, `rwb_asset`) | asset_key | Write, the ACE asset business key of the case |
| DF-SAL-003 | listing (S5, `rwb_asset`) | sale_channel | Write, against `LOV-SALE-CHANNEL`; the value of each published channel is Not specified in the source documents (GAP-2885; ASM-4781) |
| DF-SAL-004 | listing (S5, `rwb_asset`) | start_price | Write, the start price set by FEAT-AST-11 |
| DF-SAL-005 | listing (S5, `rwb_asset`) | floor_price | Write, the approved floor; never sent to a channel (BR8) |
| DF-SAL-006 | listing (S5, `rwb_asset`) | round_no | Write, 1 at publication |
| DF-SAL-007 | listing (S5, `rwb_asset`) | listed_at | Write, the publication time |
| DF-SAL-008 | listing (S5, `rwb_asset`) | status | Write, against `LOV-LISTING` (`LIVE`) |
| `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | listing (S5, `rwb_asset`) | standard record columns | Write, with the optimistic lock of `version`; `state` carries the pause marker of R-DIS-67, whose value is Not specified in the source documents (GAP-2885; ASM-4781) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the listing rows change |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book value, title status | Not read: this service holds no `v_ace_*` grant; the fact arrives on the rwb-source-data contract (BR3) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case answer |
| DF-CAS-036 to DF-CAS-045 | deviation (S8, `rwb_deviation`) | case_id, deviation_code, raised_at, paused_state | Not read as a table: the open deviation codes arrive on the rwb-deviation contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the package is loaded from rwb-decision at its version |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and the physical schema v6; `listing` is the table of the feature and its eight fields are DF-SAL-001 to DF-SAL-008. **No new table, no new column and no migration**: `listing` arrives with the DB story of this service, this story writes its eight columns and the standard record columns, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_asset` by the library's own migration (DP-03). The condition facts `photographs_count`, `inspection_report` and `title_status` are rule inputs of R-DIS-33 carried on the owners' answers and are not fields of the Logical Data Model and Data Dictionary v9 or Data Classification v5; `decision_record` is a platform library object of RWB-PLT-E1027-CON, not an entity of those documents (DOR-RWB-S5-E3029-APP-7). `listing` is absent from the legacy Data table of RWB-E3-029, whose five rows are other owners', and the publication channel, the price schedule and the pause have no column of their own (GAP-2885; ASM-4781). The channel mapping of `sale_channel` and the pause marker of `state` are held as reference data at their version and are not list values of `LOV-SALE-CHANNEL` or `LOV-LISTING` (GAP-2885).

**No personal data.** The rows this story writes carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_asset`, the decision record, a log, a channel publication or a workflow input, and the fixture data of the tests is synthetic. The photograph set and the inspection report are document facts of rwb-document and are referenced, not copied.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the publish operation and the read whose shapes are declared by RWB-S5-E3029-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/assets/{assetId}/listings` | A publish request in; the listing set out with one entry per channel, its prices, its schedule and its state (API-S5-004) | Asset and disposal, right C, scope applied | `Idempotency-Key` required; the stored answer is returned on a repeat |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, condition, valuations, costs and listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 409 where the case is not in the state the rule expects, 422 with MSG-GEN-001 for an invalid field, and 503 when the decision library or a consumed contract does not answer. The operation IDs are those of the module API list and are not redefined here. `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's and `POST /listings/{listingId}/rounds` (API-S5-005) belongs to the descending-schedule story; neither is built or declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2885; ASM-4781)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE NPA asset fact of the case: asset reference, asset key, asset type, segment, book value and title status, with the freshness stamp; faked |
| The document-set read of the case (operation name Not specified in the source documents (GAP-2885; ASM-4781)) | `/api/recovery/document/v1` | P5 rwb-document | The photograph count and the presence of the inspection report of R-DIS-33; faked |
| The deviation read of the case (operation name Not specified in the source documents (GAP-2885; ASM-4781)) | `/api/recovery/deviation/v1` | S8 rwb-deviation | The open deviation codes (X1, X4, X5) of R-DIS-67; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the account link; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2885; ASM-4781)) | rwb-case (P3) | P3 rwb-case | The answer that carries `LISTING_LIVE` or `DISPOSAL_PAUSED_DEVIATION` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The channel publication and pause (operation names Not specified in the source documents (GAP-2885; ASM-4781)) | `/api/recovery/integration/v1` | P2 rwb-integration | The publication of the start price and the schedule to HOME.SCB, the EASY app and the auction portal with the floor withheld, and the pause of R-DIS-67; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2885 with ASM-4781.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives the service the topic `rwb.asset.events.v1` with `AssetTakenOn` and `AssetSold`, and neither belongs to this step: the take-on is RWB-S5-E3019-APP and the sale is the sale story of this service. The listing-live and the pause reach rwb-case on the case-move answer, not on an event, so this story holds no outbox row, no schema and no subscription of its own. A build that publishes a listing event fails the absence test of RWB-S5-E3029-CON.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them is the listing evidence or the deviation. The evidence arrives on the document and source-data contracts, the deviation on the rwb-deviation contract, and the case signal on the parent `CaseWorkflow`. This story therefore holds no consumer group, no subscription and no inbox row of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new, namespace `rwb-recovery`; workflow ID: Not specified in the source documents (CG-ALL-9926); start rule: Not specified in the source documents (CG-ALL-9926) | `rwb-asset` | Input: the case, the route, the asset reference and the rule package in force; signals: the case state answered by rwb-case, the evidence fact, the deviation fact and the approval answer |
| `publishListing` | Activity, the publication step of this story | `rwb-asset` | The case, the asset fact and the evidence in; the rule ID with its package version, the listing references per channel, the channel answers and the case move out, with the decision record, the listing rows and the idempotency rows written together |
| `pauseListing` | Activity, the pause command of R-DIS-67 | `rwb-asset` | The case, the deviation codes and the listing references in; the pause answer per channel, the pause marker and the case move out |

No child workflow for the case and no workflow for the money exists in this service. The two activity names are target design choices of this story and are fixed by no source document; the trigger of the publication is read as the arrival of the evidence fact for a case in `FLOOR_APPROVED`, because the legacy story says the feature runs unattended while the FSD declares no background event.

#### 12.6 Schedules

None. The publication runs from the evidence fact and the pause from the deviation fact; this story owns no Temporal Schedule and no legacy Quartz job. The single Schedule of this service is JOB-19 Re-appraisal monthly, which belongs to the re-appraisal story (Architecture v5 slide 44; Ownership Map jobs JOB-19). The price schedule that is published is a payload of the listing, not a Schedule of the service, and its steps are R-DIS-36 and R-DIS-38's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| listing | S5 (`rwb_asset`) | The published listing, one row per channel; this story inserts or updates the row and writes the columns of §11 |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated fact and the channel answer it holds |

Not owned and never read as a table: `asset` and `asset_sale` (S5, the take-on and sale stories'), `recovery_case` and `timer` (P3), `deviation` (S8), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7), and every `v_ace_*` view (P1). No foreign key leaves the schema: `asset_key` is the ACE business key, and `asset_sale.listing_id` stays inside the schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The asset fact of `AST-2026-000512` for case `RC-2026-000512` with book value, segment `NPA` and title status `clear`; the same asset with the title not clear; a stale product with its date; no answer beyond 2 s | AC1, AC2, X4, X6 |
| rwb-document document-set fake | Three photographs and the inspection report of case `RC-2026-000512`; the same case with no photograph; the same case with the inspection report absent; no answer beyond 2 s | AC1, AC2, X4, X6 |
| rwb-deviation fake | Deviation `X4` open for case `RC-2026-000512`; a deviation `X2` that R-DIS-67 does not carry; no deviation open; no answer beyond 2 s | AC3, X6 |
| rwb-case case-state fake | The case state `FLOOR_APPROVED`, `LISTING_LIVE` and `DISPOSAL_PAUSED_DEVIATION` of case `RC-2026-000512`; a case that is not in the expected state | AC1, AC2, AC3, X3 |
| rwb-case case-move fake | The moves `LISTING_LIVE` and `DISPOSAL_PAUSED_DEVIATION` accepted; a move refused because the case is not in the state the rule expects | AC2, AC3, X3 |
| rwb-integration channel fake | HOME.SCB, the EASY app and the auction portal each accepting a publication; one channel refusing; a pause accepted by the three; no answer beyond 2 s | AC1, AC2, AC3, X5 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-33 and R-DIS-67 | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for case `RC-2026-000512`, with the listing facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the source-data, document, deviation, case-move and channel rows are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2885; ASM-4781).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 6 consumed | The publish operation and the asset read on `/api/recovery/asset/v1`; the source-data, document, deviation, case-state, case-move and channel rows; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The service topic carries `AssetTakenOn` and `AssetSold`, neither of which is this step's |
| Temporal | 1 workflow and 2 activities | `AssetDisposalWorkflow`, `publishListing` and `pauseListing` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here; the channel publication is a REST call |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `listing`, Java package `th.co.scb.ace.workbench.recovery.asset.listing`; front end `src/modules/recovery/asset/AssetListing.tsx`, the fragment SCR-21 and SCR-23 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the asset fact and the title status are the ones the rwb-source-data contract answers (Architecture v5 slides 29 and 41; GAP-2885; ASM-4781). DP-03 is the transaction rule of the step: the record, the listing rows and the idempotency rows commit together or not at all. DP-13 moves the base of the publish operation and the read and nothing else. DP-19 is how SCR-21 and SCR-23 reach this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The six consumed rows (source-data, document, deviation, case state, case-move answer and the channel publication) are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2885. The channel adapter of DP-16 is not in the pattern set of this key either, which is why the publication is consumed as a contract and not built as an adapter here.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` publication branch | Workflow | The step of the journey that waits for the evidence fact, loads the package in force and reports the outcome to the parent |
| `publishListing` | Activity | The one step: read the asset, the evidence and the case, evaluate R-DIS-33, write the record and the listing rows, publish to the three channels, answer the case move |
| `pauseListing` | Activity | The R-DIS-67 step: read the deviation, write the record, send the pause, mark the listing and answer the case move |
| `ListingEvaluator` | Service | The rule evaluation against the DISPOSAL package version in force, with the evidence conditions and the deviation codes |
| `ListingDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `ListingWriter` | Repository | Inserts or updates `listing` in one `rwb_asset` transaction, one row per channel, with the idempotency row and the optimistic lock |
| `ChannelPublisher` | Client | The publication and the pause on the rwb-integration contract, one hop, 2 s, breaker, with the floor withheld from the payload |
| `SourceDataProductClient`, `DocumentSetClient`, `DeviationClient`, `CaseStateClient` | Clients | The four read contracts, one hop, 2 s each, no retry of their own |
| `ListingController` | Controller | The publish operation and the asset read, the capability area and right, the `Idempotency-Key` rule and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `AssetListing` | React component | Shows the listing, its prices, its channel, its status and its schedule on SCR-21 and SCR-23, read only, with the refusal and paused states, the empty state (Not specified in the source documents, section 15), the loading state, the error state (the 503 of the composite route) and the no-access state (the 403 with MSG-P4-002) |

**Database and migrations.** No Flyway file. `listing` arrives with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). No column is added for the channel set, the price schedule or the pause marker: the channel is `sale_channel`, the schedule is a payload, and the pause is held in `state`.

**Configuration and reference data.**

- `LOV-SALE-CHANNEL` and `LOV-LISTING` at their version in force, read as reference data and never as constants; the channel-to-value mapping of HOME.SCB and the EASY app is Not specified in the source documents (GAP-2885; ASM-4781) and is a parameter of the publication.
- The DISPOSAL package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the evidence conditions, the deviation codes and the price steps are values of the package.
- The capability area "Asset and disposal" and its rights are access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; no other parameter is named in the sources for this step.
- Reference-data read (DP-06, DP-07): the lists and parameters above are read through the reference-data contract of their owner; the contract's name and path are Not specified in the source documents (DOR-RWB-S5-E3029-APP-20).

**Build steps**

1. The publication and pause branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset` as the stage child of `CaseWorkflow`.
2. `SourceDataProductClient`, `DocumentSetClient`, `DeviationClient` and `CaseStateClient` against their fakes, with the 2 s budget, the breaker and the stale and no-answer paths (AC1, AC3, X6).
3. `ListingEvaluator` over the DISPOSAL package, with R-DIS-33, R-DIS-67 and the no-fire path (AC2, AC3, X4).
4. `ListingDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `ListingWriter` with the one transaction, the eight columns, one row per channel and the idempotency row (AC1, AC2, X7).
6. `ChannelPublisher` and the publication payload with the floor withheld, plus the pause command (AC1, AC2, AC3, X5, BR8).
7. `CaseMoveAnswer` and the parent signal, with the two moves (AC2, AC3).
8. `ListingController` with the rights, the `Idempotency-Key` rule and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1).
9. `AssetListing` and the two screens through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read, and no write to any other service's schema (X8, AC5, BR3, BR5).

**Feature flag.** `rwb.asset.listing-v1`, read as a flag of the platform library; off means the step holds the evidence fact, writes nothing, publishes nothing and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic evidence fact in SIT, each of the two rules produces its record, its rows, its publication or pause and its move, a channel refusal leaves that channel unpublished and the others standing, a repeated fact writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-21 and SCR-23 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this story raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which the re-appraisal story's, so no path of this story raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or of the evidence fact is absent or invalid (X3, X4) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right publishes a listing or reads the asset (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the listing rows change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are those of the legacy message set, and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added. MSG-S5-001 and MSG-S5-002 are carried because they are in the message set of the feature, and no path of this story raises them.

### 15. Screens and states

SCR-23 Listing and price in its Draft, below-limit, approved and published states, its empty, loading, error and no access states: Not specified in the source documents (CG-ALL-9933), and SCR-21 Asset list in its loading and list states are served through the gateway-bff composite route (DP-19); its empty, error and no access states: Not specified in the source documents (CG-ALL-9932). The route calls rwb-asset for the listing, its prices, its channel, its status and its schedule, rwb-case for the case and its route state, rwb-source-data for the asset fact and rwb-valuation for the valuation references; this story fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the published state of SCR-23 — the listing live on each channel, its start price, its schedule and its floor withheld — and the paused state after R-DIS-67, which shows the pause marker and the channel answers. The refusal and failure states it shows are refused with MSG-P4-002, not recorded with MSG-P7-003 and channel not published after X5. The draft, below-limit and approved states of the same screen belong to the pricing story of this service and are read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-029-01 | AC1 | Component | The evidence set of case `RC-2026-000512` for asset `AST-2026-000512`; the listing rows, the three channel publications and the case move asserted on the fakes |
| TC-E3-029-02 | AC2 | Integration | Case `RC-2026-000512` at `FLOOR_APPROVED` with three photographs, the inspection report and a clear title; the three channels, the withheld floor and the `LISTING_LIVE` move asserted end to end on the fakes |
| TC-E3-029-03 | AC3 | Integration | Case `RC-2026-000512` at `LISTING_LIVE` with deviation `X4` open; the pause accepted by the three channels and the `DISPOSAL_PAUSED_DEVIATION` move asserted |
| TC-E3-029-04 | AC4 | Component | The decision-record stub stopped; nothing written, no publication sent and MSG-P7-003 shown |
| TC-E3-029-05 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E3-029-06 | Principle 5 | Component | A forced decision record write failure at the moment of the insert; no row, no publication and no answer |
| TC-E3-029-07 | §12 operations, events and activities; BR1, BR4 | Contract | Every operation, event and activity of section 12 called against the published contract of its owner and answered by its fake; the listing row and the case-move answer asserted |
| TC-E3-029-08 | AC5, X8, the tables of §12.7 (ASM-3438), BR3, BR5 | Boundary | The statements of the build, the `v_ace_*` views and the schemas outside `rwb_asset`; the grant refuses each, the build fails, and the tables of §12.7 are checked for ownership |
| TC-E3-029-09 | BR2, BR7, BR9 | Component | The same evidence fact and the same `Idempotency-Key` sent twice; one decision record before the change, one row per channel, one publication set and one answer |
| TC-E3-029-10 | BR6, BR8, BR10 | Component | The channel and rule values read with their version, the publication payload with the floor withheld, and no person name, address, contact value or identity number in any output |
| TC-E3-029-11 | AC6 | Component | A consumed rwb-integration call that does not answer on its fake; the listing rows, the case move and the channel-not-published state asserted |
| TC-E3-029-12 | AC7 | Component | A case in `LISTING_LIVE` asked to publish; 409 asserted on the fakes and nothing written |
| TC-E3-029-13 | AC8, BR1 to BR10 | Component | The publication of case `RC-2026-000512` asserted against each of rules BR1 to BR10; the detail of each rule is in TC-E3-029-07 to TC-E3-029-10 |
| TC-E3-029-14 | AC9, X2 | Component | A request without an identity, a role without the Asset and disposal right and an unknown case id; 401, 403 with MSG-P4-002 and 404 asserted, nothing written |
| TC-E3-029-15 | AC10, X7, BR9 | Component | The same `Idempotency-Key` sent twice; one row set, one publication set and one answer asserted, no second decision record |
| TC-E3-029-16 | AC11, X5, X6 | Component | A consumed rwb-case call that does not answer inside 2 s; 503 asserted, nothing written and the step retry asserted |

The six legacy cases are the legacy cases of RWB-E3-029 in their legacy order, with the Level column added: `System` and the screen cases map to `Component` where the step is tested on its fakes, and TC-E3-029-02 and TC-E3-029-03 map to `Integration` because they cross the rwb-document, rwb-source-data, rwb-integration and rwb-case boundaries. The full test, with its Given, When and Then, is in the Recovery Workbench Test Cases workbook, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in code: the channel set, the evidence conditions, the deviation codes, the price steps and the lists stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_asset`, in a channel payload, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case, the document, the deviation and the channels stay with their owners: no `recovery_case` row, no `deviation` row, no `document` row and no adapter is built here (BR3, BR4).
- The floor never leaves the service in a publication payload, whatever the channel asks for (BR8).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, the monolith base is not used, and no event is published on the service topic by this step.
- The decision is recorded before the change; a build that writes the listing row before the record, or that publishes outside the transaction, fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S5-005 | Listings are published to the bank's channel and the auction portal from one action (Business Requirements Program v5, Must, owner Head of NPA); the split plan carries no requirement id for this slice (GAP-2885; ASM-4781) | The publication step, the `listing` rows and the channel publication | TC-E3-029-01, TC-E3-029-02, TC-E3-029-04 | FEAT-AST-12 | Not specified in the source documents (DOR-RWB-S5-E3029-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the listing record | TC-E3-029-01 | FEAT-AST-12 | Not specified in the source documents (DOR-RWB-S5-E3029-APP-2) |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login | TC-E3-029-06 | FEAT-AST-12 | Not specified in the source documents (DOR-RWB-S5-E3029-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget | TC-E3-029-02 | FEAT-AST-12 | Not specified in the source documents (DOR-RWB-S5-E3029-APP-2) |
| ADR-022 | Local decision record plus central ledger | The decision record written before the change | TC-E3-029-04, TC-E3-029-06 | FEAT-AST-12 | Not specified in the source documents (DOR-RWB-S5-E3029-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-029, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E3-029-01 to TC-E3-029-06 |
| Feature and screens | FEAT-AST-12, SCR-21 Asset list and SCR-23 Listing and price |
| Rules | R-DIS-33 and R-DIS-67, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the publish operation and the read, the `Listing` element, the channel set, the consumed rows, the error set and the fakes: RWB-S5-E3029-CON.
- The start price, the floor and their approval: FEAT-AST-11 and the pricing story of this service, which writes the draft listing.
- The descending price schedule, the rounds, the bid handling and the re-listing: FEAT-AST-13, FEAT-AST-15 and FEAT-AST-17 and their stories, with `POST /listings/{listingId}/rounds` (API-S5-005).
- The blocked-publication paths of R-DIS-34 and R-DIS-35 and the document task they raise: the sibling stories of the feature; this story reads the evidence and stops.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes.
- The ACE NPA asset fact and the title status, and the freshness of the data product: rwb-source-data (P1).
- The photograph set, the inspection report and their retention: rwb-document (P5).
- The deviation, its codes and its owner: rwb-deviation (S8), whose fact this story consumes and fakes.
- The channel adapters of HOME.SCB, the EASY app and the auction portal: rwb-integration (P2), whose contract this story consumes and fakes.
- The authoring, testing, approval and versioning of the DISPOSAL package and of the rule rows of R-DIS-33 and R-DIS-67: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-23: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
