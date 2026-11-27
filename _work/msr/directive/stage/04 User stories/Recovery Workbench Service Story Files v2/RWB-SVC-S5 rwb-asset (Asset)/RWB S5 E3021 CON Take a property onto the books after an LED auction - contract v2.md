# RWB-S5-E3021-CON Take a property onto the books after an LED auction - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3021-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S5-E3021-CON-16); deferred to refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (the `/v1` paths named in section 12.2 and the `AssetTakenOn` envelope of section 12.3) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (traced to REQ-S5-001 and FEAT-AST-03) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the LED auction take-on step of rwb-asset, split from RWB-E3-021. It fixes the two read operations on `/api/recovery/asset/v1` (DP-13), the `asset` element with its closed lists and its asset-key link, the `AssetTakenOn` envelope on `rwb.asset.events.v1`, the consumed `AuctionResult` event of `rwb.litigation.events.v1` with its inbox rule, the consumed rwb-source-data and rwb-case rows, the decision-record element of DP-03, the fakes and the absence tests. DP-09 is not in the plan's pattern set although the step consumes one event and publishes one, and the rwb-litigation, rwb-source-data and rwb-case rows are not in the plan's C row (GAP-2847, GAP-2849; ASM-4712, ASM-4714, ASM-4717). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3021-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 15 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Platform administrator (RW-PLATADM)**, I want **the published contract baseline of the LED auction take-on step of rwb-asset — the two asset reads on `/api/recovery/asset/v1`, the `asset` element with its asset-key link and its closed lists, the `AssetTakenOn` envelope, the consumed `AuctionResult` event, the consumed rwb-source-data and rwb-case rows, the decision-record element, the tables and the fakes**, so that **the app story, the two screens and the wave 2 harness build against one fixed, testable contract on Day 1 and an event property, an asset field, a list value or an answer shape can never drift between rwb-asset, rwb-litigation, rwb-source-data and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy take-on of RWB-E3-021 crossed four boundaries at once: an officer screen, the enforcement auction result, the ACE asset fact and a case state. The target splits them: rwb-litigation owns the auction and its result, rwb-source-data owns the ACE asset facts, rwb-case owns the case and its route states, and rwb-asset owns the asset record, the take-on event and its inbox. Each boundary is now a contract that another team builds against, so each has to be fixed before the app story starts: the `asset` fields of the take-on and the asset-key link, the values of `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT` and `LOV-HOLDING`, the `AssetTakenOn` envelope, the `AuctionResult` envelope and its deduplication, the fact the rwb-source-data contract answers, the case state and move of rwb-case and the record of the decision.

The baseline also fixes the naming that the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, the consumed topic `rwb.litigation.events.v1`, task queue `rwb-asset` in namespace `rwb-recovery`, consumer group `rwb-asset-led-handover` and Java package `th.co.scb.ace.workbench.recovery.asset`. It records that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case` or `rwb_litigation` (Architecture v5 slides 29, 37 and 45), so DP-05 is declared as a prohibition and the asset fact is consumed on the owner's contract only.

Two points are carried as gaps and assumptions rather than decided quietly: the `asset` table has no Ownership Map row although three sources give the record to S5, and the LED result has no column, no list value and no published event property list, while no source names the story key of the rwb-litigation contract that answers it (GAP-2849; ASM-4714, ASM-4715). The plan's pattern set omits DP-09 although the step consumes and publishes an event, and its C row is None although four owner contracts are read (GAP-2847; ASM-4712, ASM-4717).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topics, the queue, the consumer group and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `listing` and `asset_sale` are S5's, `recovery_case` and `assignment` are P3's, `legal_action` is S4's, `proceeds` is P8's, `document` is P5's, `notice` is P6's, `decision_log_entry` and `rule_row` are P7's. This document never declares another service's table or operation as its own, and it records that the `asset` record has no Ownership Map row while Architecture v5 slides 19 and 41 and TSD S5 T3.1 give it to S5 (GAP-2849; ASM-4714).
- The rwb-litigation contract of the enforcement auction, the rwb-source-data data-product contract of DP06 Collateral and assets and the rwb-case state and move rows are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2847, GAP-2849; ASM-4712, ASM-4714).
- The outbox and inbox library `RWB-PLT-TE006-CON` of DP-09 is the platform dependency of the consumed and the published event; the plan's H row does not carry it, and this baseline keeps the row as the plan states it (GAP-2847; ASM-4717).
- The DISPOSAL rule package and its rule rows for R-DIS-01, R-DIS-02, R-DIS-03 and R-DIS-06 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `asset` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this step: the two reads with their request and answer elements, the filters, the rights and the error responses.
2. Fix the `asset` element: the columns of DF-COL-028 to DF-COL-042, their types, their required flags, the list each of them is declared against and the asset-key link rule of DF-COL-031.
3. Fix the `AssetTakenOn` envelope on `rwb.asset.events.v1`: the required CloudEvents attributes, the data properties of the take-on and the rule version, and the prohibition on personal data.
4. Fix the consumed `AuctionResult` row on `rwb.litigation.events.v1`: the envelope, the consumer group, the inbox deduplication key, the data properties the step needs and the placeholder where the owner publishes none of them.
5. Fix the other consumed rows: the rwb-source-data data-product read with its freshness stamp, and the rwb-case state read and move answer, marking the fields the sources do not give with the placeholder.
6. Record the decision-record element of DP-03, written before the asset row changes.
7. Record the closed vocabulary of the lists, the naming baseline and the rule that no value is a constant of the code.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `litigation` or `recovery_case` write, the drift between a fake and the document, and the deduplication of a redelivered event.
10. Tag the baseline and hand it to RWB-S5-E3021-APP, the two screens and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC4, AC5 |
| X5 | A value outside `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT` or `LOV-HOLDING` appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or a `legal_action` row | The review fails the baseline; the boundary test fails the build | None | AC8 |
| X7 | The document declares a second event, a second topic, a second consumer group or a Schedule | The absence test fails the build | None | AC8 |
| X8 | The rights of an operation are not the ones TSD S5 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC6 |
| X9 | A redelivered `AuctionResult` is treated as a new fact | The deduplication test fails the build | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-litigation, rwb-source-data and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values, the consumer group name and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topics and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S5-E3021-APP, the two screens and the wave 2 harness on Day 1, and the rwb-litigation, rwb-source-data and rwb-case teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, eight fakes and six new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the LED auction take-on step of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing and asset_sale is S5, of recovery_case and assignment is P3, of legal_action is S4, of proceeds is P8 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two asset reads are declared on the asset base with their shapes and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /assets with an AssetPage answer of status 200 and GET /assets/{assetId} with an Asset answer of status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then the list declares the filters type, status, region, page and size, and the single read declares the path parameter assetId
    Then the answers 400 with MSG-GEN-001, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 are declared with one envelope and one message ID per condition, and neither read declares an Idempotency-Key
    Then the ownership rows GET /assets/{assetKey}, the two listing posts and POST /listings/{listingId}/rounds are named as this service's and are declared by the pricing and auction baselines, not here
    Then every other property of the two operations is copied from the baseline of the asset reads and is not redefined here

  Scenario: AC2 The asset element, its asset-key link and its closed lists are fixed for the take-on (new, D-RCV-60)
    Given the asset section of the baseline
    When it is compared with TSD S5 T3.1, T3.2 and A2.6.3.2
    Then the Asset element declares the properties of DF-COL-028 to DF-COL-042: id, case_id, collateral_id, asset_ref, asset_code, asset_type, transfer_in_type, from_segment, transfer_in_date, book_value, auction_purchase_price, repossessed_date, stock_date, holding_status and holding_cost_to_date
    Then asset_ref is declared as the ACE NPA asset business key and the only link to the ACE asset, with no foreign key and no separate asset_key property
    Then asset_type is declared against LOV-ASSET-TYPE with the values DETACHED_HOUSE, TOWNHOUSE, CONDOMINIUM, LAND, COMMERCIAL_BUILDING and VEHICLE, and a property value is the value this route writes
    Then transfer_in_type is declared against LOV-TRANSFER-IN with the values AUCTION_PURCHASE, DEED_IN_LIEU and REPOSSESSION, and AUCTION_PURCHASE is the value this route writes
    Then from_segment is declared against LOV-SEGMENT and holding_status against LOV-HOLDING with the values HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED
    Then id, asset_ref, asset_type, transfer_in_type, transfer_in_date, book_value and holding_status are required and the other properties are optional
    Then auction_purchase_price is declared as the handover price of the auction result and no property is added for the LED round, the ladder percentage, the led result or the receiving submission

  Scenario: AC3 The AssetTakenOn event is declared and the AuctionResult event is consumed with its inbox rule (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with Architecture v5 slide 19 OUT and IN, slide 43 row 22 and slide 13 row S5
    Then AssetTakenOn is declared on the topic rwb.asset.events.v1 with the event name rwb.asset.AssetTakenOn.v1, produced by rwb-asset, with rwb-case and rwb-payment as its only consumers
    Then its data carries the case reference, the asset reference, the asset type, the transfer-in type, the taken-on date and the rule ID with its version, and no amount, balance or posting fact
    Then AuctionResult is declared as consumed from rwb-litigation on rwb.litigation.events.v1 with the event name rwb.litigation.AuctionResult.v1, the consumer group rwb-asset-led-handover and an inbox keyed by the CloudEvents ID
    Then the consumed data the step needs is the case reference, the property reference, the asset key, the led result, the round, the handover price and the handover date, and every property the owner does not publish carries Not specified in the source documents (GAP-2849; ASM-4714)
    Then both topics declare their retry and .dlt topics, the envelope is CloudEvents, and a schema test fails any personal data property
    Then JudgmentRecorded and ProceedsMatched are named as the service's other catalogue events and are not consumed by this step, and no second event, second topic or Schedule is declared

  Scenario: AC4 The consumed rwb-source-data row is declared and the ACE fact stays there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the rwb-source-data data-product contract and Architecture v5 slides 29, 37 and 45
    Then the read of DP06 Collateral and assets is declared as consumed from P1 rwb-source-data, with the asset key, asset reference, asset code, asset type, condition, photographs, location, segment, book value and the freshness stamp of the data product
    Then the operation name of the row is Not specified in the source documents (GAP-2849; ASM-4715) and the row carries the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property and no grant on any rwb_* schema of another owner, and the boundary test fails a build that adds one
    Then the call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The rwb-case rows and the case move are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with rwb-case as the owner of recovery_case
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state and the move ASSET_ON_BOOKS carrying the rule ID and its version
    Then the operation name of the case-move answer is Not specified in the source documents (GAP-2847; ASM-4716) and the row carries the placeholder
    Then the document declares no recovery_case property, no route-state column and no write of a case row from rwb-asset
    Then the answers the step needs are the states ASSET_PENDING_TAKE_ON and ASSET_ON_BOOKS, an accepted move and a refused move

  Scenario: AC6 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access and error sections of the baseline
    When they are compared with TSD S5 T6.1 and T-A.1
    Then both reads declare Asset and disposal right R with the scope applied, and RW-SALEOFF holds CRUA, RW-NPAMGR and RW-ENFORCE hold CRU and every other role of TSD S5 T6.1 holds R or RA as the matrix gives it
    Then a role without the right is answered 403 with MSG-P4-002 and nothing is read, and a request with a missing field is answered 400 or 422 with MSG-GEN-001
    Then a repeated request with the same Idempotency-Key describes no second effect, and no read declares the header
    Then no operation of the document declares a right of another capability area

  Scenario: AC7 The decision-record element and the eight fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the LED result, the round, the rule ID, the package version in force, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the asset row changes, and a failed write leaves the asset unchanged with MSG-P7-003
    Then the rwb-litigation fake answers the handed-over result of property "AST-2026-000521" for case "RC-2026-000521", a result not handed over, a redelivery of the same CloudEvents ID and no event beyond 2 s
    Then the rwb-source-data fake answers the AMIS property with its asset key, condition, photographs, location and segment, a stale product and no answer beyond 2 s
    Then the rwb-case fake answers the two route states, an accepted move and a refused move, and the rwb-decision fake answers the DISPOSAL package at its version with R-DIS-01, R-DIS-02, R-DIS-03 and R-DIS-06
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-21 and SCR-22 answer
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the published topic is rwb.asset.events.v1, the consumed topic is rwb.litigation.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the tables named as owned are asset and the library objects decision_record, idempotency_key, inbox_event and outbox_event, and recovery_case, assignment, legal_action, proceeds, document, notice, decision_log_entry, rule_row and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares one consumed event, one published event and no Schedule, and the absence test fails a build that adds a second of either
    Then the document records that the asset record has no Ownership Map row and that its owner is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 (GAP-2849; ASM-4714)

  Scenario: AC9 Every business rule of section 8 and every table of section 12.7 is held by a named boundary test (new, D-RCV-60)
    Given the rules BR1 to BR13 of section 8 and the tables of section 12.7 of the baseline
    When each rule and each table is compared with the criterion and the test case that hold it
    Then each of BR1 to BR13 names an AC of this story and a test case of section 16, and a rule that is an architecture constraint is held by a guardrail or boundary test
    Then the tables asset, decision_record, idempotency_key, inbox_event and outbox_event are declared with the owner that section 12.7 gives, and no other table is declared as owned
    Then the boundary test fails a build that adds a table, a list value or a published property that section 8 or section 12.7 does not name

  Scenario: AC10 The take-on rule R-DIS-03 is built once in a shared component and named here, not declared (new, D-RCV-60)
    Given the take-on rule R-DIS-03 of the DISPOSAL package
    When it is compared with FSD S5 A2.3.3.1 and Business Rules and Routing Logic v4
    Then the rule moves a case from ASSET_PENDING_TAKE_ON to ASSET_ON_BOOKS when LED_HANDOVER_RECEIVED arrives with led_result equal to handed_over
    Then the take-on is served by one shared take-on component, and the document names R-DIS-03 and declares no rule row for it
    Then the decision package version in force and the rule ID are written to the decision record of AC7
```

These ten criteria are new for the contract baseline. AC1 to AC9 test the artefact only; AC10 is the one take-on rule of the feature that this story builds once in a shared component so that the app stories do not duplicate it. They restate no other business outcome owned by RWB-S5-E3021-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source | Covered by AC | Covered by test |
|---|---|---|---|---|
| BR1 | The asset record is rwb-asset's, and the contract declares its fields, its lists, its required flags and its asset-key link on the `asset` element only | Architecture v5 slide 41; TSD S5 T3.1, T3.2 and A2.6.3.2; ASM-4714 | AC2 | TC-S5-E3021-CON-02 |
| BR2 | The decision record is declared as an element written before the asset row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S5 T2; legacy RWB-E3-021 AC1 and AC4 | AC7 | TC-E3-021-06, TC-S5-E3021-CON-04 |
| BR3 | The ACE asset fact stays with rwb-source-data: the contract declares the data-product read as consumed, declares no `v_ace_*` property and describes no ACE table read of rwb-asset | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2849 | AC4 | TC-E3-021-01, TC-S5-E3021-CON-04 |
| BR4 | The case move is answered and not written: the contract declares the state read and the answer, and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); GAP-2847 | AC5 | TC-E3-021-02, TC-S5-E3021-CON-04 |
| BR5 | The auction result is consumed, not owned: the contract declares `AuctionResult` as an inbound event with its consumer group and its inbox, and declares no `legal_action` property | Architecture v5 slide 13 row S5 and slide 19 IN; GAP-2847 | AC3 | TC-E3-021-01, TC-S5-E3021-CON-03 |
| BR6 | The published event is declared once: `AssetTakenOn` on `rwb.asset.events.v1` with rwb-case and rwb-payment as its only consumers, published from the outbox | Architecture v5 slide 19 OUT and slide 43 row 22 | AC3 | TC-S5-E3021-CON-03 |
| BR7 | A redelivered event is deduplicated by the CloudEvents ID and describes no second effect; a POST declares the `Idempotency-Key` and a GET declares none | Architecture v5 slide 11; TSD S5 T-A.2; ASM-4717 | AC3 | TC-S5-E3021-CON-03 |
| BR8 | The vocabulary is closed: `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT` and `LOV-HOLDING` are published as enumerated values and no list value is a constant of the code | TSD S5 T3.2; FSD S5 BR-S5-003 | AC2 | TC-E3-021-02, TC-S5-E3021-CON-02 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) | AC1 | TC-S5-E3021-CON-01 |
| BR10 | One REST base, one published topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 | AC1 | TC-S5-E3021-CON-01 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) | AC1 | TC-S5-E3021-CON-01 |
| BR12 | The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 | AC4 | TC-S5-E3021-CON-04 |
| BR13 | The rule rows of R-DIS-01, R-DIS-02, R-DIS-03 and R-DIS-06, the ladder of 100, 90, 80 then 70 percent and the `handed_over` result are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; GAP-2849; ASM-4718 | AC4 | TC-S5-E3021-CON-04 |

### 9. State transitions

The lifecycle of this document, not of an asset:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the element, the lists, the two events, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 2 harness and the rwb-litigation, rwb-source-data, rwb-case and rwb-payment owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new filter or a new optional asset field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC4 and AC8 fail: a `v_ace_*` view, a `recovery_case` or `legal_action` property, a second event, a second topic or a Schedule | In review |

The holding-status machine that the document describes is the app story's: `LOV-HOLDING` is HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED, and this baseline fixes the vocabulary and the take-on value `HELD` and moves no asset.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the correction of the Ownership Map rows the baseline consumes, including the missing `asset` row, and the confirmation of the rwb-litigation event properties |
| Consuming teams (the app story, the two screens, the wave 2 harness and the owners of rwb-litigation, rwb-source-data, rwb-case, rwb-decision, rwb-access and rwb-payment) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or an event |

The per-service login behind the security scheme of the document is named "the rwb-asset login (DP-02)" and is not part of this baseline.

The rwb-access authorise check that guards the two reads and the Asset and disposal right is Not specified in the source documents (DOR-RWB-S5-E3021-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Asset element | The columns of DF-COL-028 to DF-COL-042: `id`, `case_id`, `collateral_id`, `asset_ref`, `asset_code`, `asset_type`, `transfer_in_type`, `from_segment`, `transfer_in_date`, `book_value`, `auction_purchase_price`, `repossessed_date`, `stock_date`, `holding_status` and `holding_cost_to_date` |
| Asset-key link | `asset_ref` (DF-COL-031) is the ACE NPA asset business key and the only link to the ACE asset; there is no foreign key and no separate `asset_key` property (BR1); the record is this service's own holding record in schema `rwb_asset` and copies no ACE column |
| Required flags | `id`, `asset_ref`, `asset_type`, `transfer_in_type`, `transfer_in_date`, `book_value` and `holding_status` required; the other eight optional |
| Lists | `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT` and `LOV-HOLDING`, published as enumerations and read as reference data at their version |
| Published event data | The case reference, the asset reference, the asset type, the transfer-in type, the taken-on date and the rule ID with its version |
| Consumed event data | The case reference, the property reference, the asset key, the led result, the round, the handover price and the handover date; the property names the owner does not publish carry the placeholder |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the asset row changes (DP-03) |
| ACE asset fact | DF-ACE-208 to DF-ACE-219 of `v_ace_npa_asset` in P1, read only through the owner's data product and never written, copied or joined here |
| Not declared here | `recovery_case` and `assignment` (P3), `legal_action` (S4), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7), `listing` and `asset_sale` (S5, the pricing and sale stories') |
| Consumed fields with no source | The operation names of the rwb-source-data read and of the rwb-case move answer, the producer story key of the consumed event and its LED property names: Not specified in the source documents (GAP-2847, GAP-2849; ASM-4714, ASM-4715, ASM-4716) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the asset-key link, the vocabulary of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

Each of the ten rows above has no BR Field ID: Not specified in the source documents (DOR-RWB-S5-E3021-CON-7). The names `collateral_id`, `holding_status`, `holding_cost_to_date` and `handed_over` are not fields or entities in LDM v9 or Data Classification v5 (DOR-RWB-S5-E3021-CON-7).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated by page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, condition, valuations, costs and listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |

The two operations answer 400 with MSG-GEN-001, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S5 T-A.1 and the paths are those of the target base, not the monolith form. The ownership rows `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds` are this service's and are declared by the pricing and auction baselines of the epic; API-S5-003 `POST /assets/{assetId}/valuations` is rwb-valuation's under the Ownership Map ruling recorded by RWB-S5-E3019-CON. None of them is declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2849; ASM-4715)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE NPA asset fact of the case: asset key, asset reference, asset code, asset type, condition, photographs, location, segment, book value and the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the account link the asset row carries; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2847; ASM-4716)) | rwb-case (P3) | P3 rwb-case | The move `ASSET_ON_BOOKS` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2847 and GAP-2849 with ASM-4712, ASM-4715 and ASM-4716. Every asset, collateral and score read is made on the rwb-source-data row above; its contract fields and freshness response are confirmed with P1 before wave 2 system test.

#### 12.3 Events published

| Event | Topic | Documented data | Consumers |
|---|---|---|---|
| `AssetTakenOn` (`rwb.asset.AssetTakenOn.v1`) | `rwb.asset.events.v1`, with `.retry` and `.dlt` | The case reference, the asset reference, the asset type, the transfer-in type `AUCTION_PURCHASE`, the taken-on date and the rule ID with its version; CloudEvents envelope; no personal data | rwb-case and rwb-payment (Architecture v5 slide 43 row 22), and no other consumer |

`AssetSold` is the second event of the service and belongs to the sale and auction stories; this baseline declares it as the catalogue's and not as an element of this step. The outbox that relays `AssetTakenOn` is the platform library object of DP-09, which the plan's pattern set for this key does not carry (GAP-2847; ASM-4717).

#### 12.4 Events consumed

| Event | Topic | Producer | Documented data |
|---|---|---|---|
| `AuctionResult` (`rwb.litigation.AuctionResult.v1`) | `rwb.litigation.events.v1`, with `.retry` and `.dlt` | S4 rwb-litigation | The case reference, the property reference, the asset key, the led result, the round, the handover price and the handover date; CloudEvents envelope; no personal data; read from the inbox keyed by the CloudEvents ID under consumer group `rwb-asset-led-handover` |

The row is read from Architecture v5 slide 13, whose S5 row listens to S4's events, and from slide 19 IN, which gives rwb-asset the consumed events `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`. This baseline declares `AuctionResult` only; the other two are the service's catalogue events for other steps and are named, not consumed. The producer story key and the LED property names are the owner's and are not published, so the row carries the placeholder (GAP-2849; ASM-4714). The inbox is the platform library object of DP-09, which the plan's pattern set does not carry (GAP-2847; ASM-4717).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` | The stage that hosts the take-on step; its signals, including the `AuctionResult` signal, and its outcome for the parent are declared, not built |
| `takeOnLedAuctionAsset` | Activity, the one take-on step | `rwb-asset` | The case and the auction result in; the rule ID with its package version, the asset reference, the event and the case move out |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice and the trigger is read as the arrival of the `AuctionResult` event for a case in `ASSET_PENDING_TAKE_ON`, because the FSD declares no background event for the feature (FSD S5 A2.3.4.4). No activity is registered by this story. The workflow ID form and the duplicate-start policy of `AssetDisposalWorkflow` are Not specified in the source documents (CG-ALL-9689).

#### 12.6 Schedules

None. The step runs from the consumed event and from the case signal the parent forwards; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to the holding and re-appraisal story of this service.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| asset | S5 (`rwb_asset`) | The taken-on property, its fields, its lists, its asset-key link and its holding status; the table the two reads answer from |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated request and the answer it holds |
| inbox_event | PLT library, created in `rwb_asset` | The deduplication row of the consumed `AuctionResult` (DP-09) |
| outbox_event | PLT library, created in `rwb_asset` | The `AssetTakenOn` row relayed to `rwb.asset.events.v1` (DP-09) |

`recovery_case` and `assignment` (P3), `legal_action` (S4), `proceeds` (P8), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7), `listing` and `asset_sale` (S5, later stories') and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

The reference data this baseline reads is the closed lists of the `asset` element (LOV-SEGMENT and LOV-HOLDING), governed by the reference-data contract of DP-06 and DP-07; the parameters it reads are Not specified in the source documents (DOR-RWB-S5-E3021-CON-20).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-litigation auction-result fake | The `AuctionResult` of property `AST-2026-000521` for case `RC-2026-000521` with result `handed_over`, round and handover price 3500000.00; a result not handed over; a redelivery of the same CloudEvents ID; no event beyond 2 s | AC3, AC7, X9 |
| rwb-source-data data-product fake | The AMIS property `AST-2026-000521` with its asset key, condition, photographs, location, segment, book value and the freshness stamp; a stale product with its date; no answer beyond 2 s; an unreadable answer | AC1, AC4, AC7 |
| rwb-case state and move fake | The states `ASSET_PENDING_TAKE_ON` and `ASSET_ON_BOOKS` of case `RC-2026-000521`; an accepted move and a refused move | AC5, AC7 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-01, R-DIS-02, R-DIS-03 and R-DIS-06 | AC7 |
| rwb-payment proceeds fake | The `ProceedsMatched` answer of the catalogue for case `RC-2026-000521`, named only and not consumed by this step | AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC7 |
| Outbox and inbox stubs (`RWB-PLT-TE006-CON`) | A relayed `AssetTakenOn`, a relay that fails and retries, and a deduplicated redelivery | AC3, AC7 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000521` | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The producer story key of the consumed event, its LED property names and the operation names of the rwb-source-data read and of the case-move answer are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2847, GAP-2849; ASM-4714, ASM-4715, ASM-4716).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-source-data data-product read, the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 1 published, 1 consumed | `AssetTakenOn` on `rwb.asset.events.v1` from the outbox; `AuctionResult` from `rwb.litigation.events.v1` into the inbox; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `AssetDisposalWorkflow` and `takeOnLedAuctionAsset` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no asset, no case, no auction and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment with an inbound and an outbound channel, nine contract tables and eight fakes.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml`, the `Asset` and `AssetPage` elements, the `AssetTakenOn` envelope and the `AuctionResult` subscription in `asyncapi/rwb-asset-v1.yaml`, the vocabulary of the four lists as published enumerations, the contract README rows for the consumed rows and their placeholders, and the eight WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on any other owner's schema, because rwb-asset holds none (Architecture v5 slides 29, 37 and 45; GAP-2849; ASM-4715). DP-13 moves the base and nothing else. DP-19 is behind SCR-21 and SCR-22, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, which is why the outbox and inbox library is recorded as an absent H row rather than declared (GAP-2847; ASM-4717).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries, and it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the consumed and the published event need. The three consumed REST rows and the consumed event row are C dependencies in fact and not in the metadata row (GAP-2847, GAP-2849; ASM-4712).

**Build steps**

1. Write the two reads and validate the additive rule of AC1 in the pipeline.
2. Write the `Asset` element, its required flags, its asset-key link and its four lists of AC2 with the placeholder where a type is unstated.
3. Write the `AssetTakenOn` and `AuctionResult` channels of AC3, with the no-personal-data schema test, the deduplication test and the no-second-event test.
4. Record the consumed rwb-source-data row of AC4 with its owner, its budget, its freshness stamp and its placeholder.
5. Record the rwb-case rows and the move answer of AC5.
6. Record the rights and the error envelope of AC6.
7. Record the decision-record element of AC7 and validate it against the library schema, then publish the eight fakes and the drift test.
8. Record the naming baseline and the boundary of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the six new contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the two screens and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the asset row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of the case is stale after a late or failed batch (VR-S5-003-1); the check is the owner's and this service holds no ACE batch status read | {product} is from {date}. Today's load has not arrived. |

The six message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged except MSG-P1-001, whose text is copied from the Error and Message Standard v4 (CG-ALL-9691); no other message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and the check itself belongs to rwb-source-data (GAP-2849; ASM-4715).

### 15. Screens and states

The contract serves SCR-21 Asset list in its loading and list states, and in its empty, error and no access states (Not specified in the source documents (CG-ALL-9693)), and SCR-22 Asset record in its take-on, held, listed and sold states, and in its loading, empty, error and no access states (Not specified in the source documents (CG-ALL-9694)), all through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its handover price and its holding status, rwb-case for the case and its route state, rwb-source-data for the ACE asset fact and rwb-valuation for the valuation references; this baseline fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal, not-recorded and stale-data states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-021-01 | AC1, AC3, AC4 | Contract | The `AuctionResult` and the AMIS property `AST-2026-000521`; the contract half answers the two reads, the consumed event and the data-product row |
| TC-E3-021-02 | AC2, AC5 | Contract | The repossession route's fact of the sibling story; the contract half answers the `Asset` element, the vocabulary and the move shape |
| TC-E3-021-03 | AC2, AC5 | Contract | The deed in lieu route's fact of the sibling story; the contract half answers the opening book value property and the `ASSET_ON_BOOKS` move |
| TC-E3-021-04 | AC1, AC6 | Contract | A role without the Asset and disposal right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E3-021-05 | AC6 | Contract | RW-SALEOFF holds CRUA and RW-NPAMGR holds CRU; the contract half answers the rights of the two reads |
| TC-E3-021-06 | AC7, AC8 | Contract | The decision-record stub stopped and a stale data product; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S5-E3021-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the filters and the six error answers are present |
| TC-S5-E3021-CON-02 | AC2 | Contract | The `Asset` element validates with its fifteen properties, its seven required flags, the asset-key link and the four closed lists |
| TC-S5-E3021-CON-03 | AC3 | Contract | The `AssetTakenOn` and `AuctionResult` channels validate against CloudEvents and the catalogue, with the consumer group, the inbox key and the deduplication case |
| TC-S5-E3021-CON-04 | AC4, AC5, AC6, AC7, AC8 | Contract | The four consumed rows and their placeholders; the eight fakes match the document and a drifted fake fails the build; the no-`v_ace_*`, no-`legal_action` and no-`recovery_case` boundary |
| TC-S5-E3021-CON-05 | AC9 | Contract | The rules BR1 to BR13 of section 8 and the tables of section 12.7; the boundary test fails on an unnamed rule or table. Data: Not specified in the source documents (NEWAC-RWB-S5-E3021-CON-AC9) |
| TC-S5-E3021-CON-06 | AC10 | Contract | The rule R-DIS-03 of the DISPOSAL package at its version, with the state ASSET_PENDING_TAKE_ON, LED_HANDOVER_RECEIVED with led_result handed_over and the move to ASSET_ON_BOOKS |

The six legacy cases are the legacy cases of RWB-E3-021 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E3021-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The six cases `TC-S5-E3021-CON-01` to `-06` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the LED result, the ladder percentages, the one-working-day target, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; every example is synthetic.
- The ACE asset fact stays with rwb-source-data, the case with rwb-case and the auction with rwb-litigation: the document declares no `v_ace_*` path, no `recovery_case` or `legal_action` property, no case row write and no ACE table read (BR3, BR4, BR5).
- The money stays with rwb-payment: the document declares no posting, no balance and no cost-of-carry property.
- One base, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a second event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S5-001 | Every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step; the LED auction purchase is a third take-on route of the same record (Business Requirements Program v5; FSD S5 requirements served). The plan's reqs list for this slice is empty and TSD S5 T8 names no requirement for FEAT-AST-03 (GAP-2850; ASM-4715) | The `Asset` element, the asset-key link, the `AssetTakenOn` envelope and the three consumed REST rows | TC-E3-021-01, TC-S5-E3021-CON-01, TC-S5-E3021-CON-02 |
| FEAT-AST-03 | Links the case to the property in `v_ace_npa_asset`, which ACE ingests from AMIS, by asset key when the bank takes the property at the enforcement auction (Epics 3 to 8 Specification v3) | The asset-key link of AC2 and the consumed `AuctionResult` of AC3 | TC-S5-E3021-CON-02, TC-S5-E3021-CON-03 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `AssetTakenOn` and `AuctionResult` channels and the inbox and outbox rows | TC-S5-E3021-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed REST rows with their budget and breaker | TC-S5-E3021-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-021, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S5-E3021-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S5-E3021-CON-01 to -04 |
| Feature and screens | FEAT-AST-03, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-03 of this feature, with R-DIS-01, R-DIS-02 and R-DIS-06 named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two reads, the evaluation of R-DIS-03, the decision record, the `asset` row, the published event, the consumed event and the case-move answer: RWB-S5-E3021-APP.
- The enforcement auction, the LED result and the litigation facts: rwb-litigation (S4), whose event this baseline declares as consumed and faked (GAP-2849).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked (GAP-2847).
- The ACE NPA asset, collateral and score facts and the freshness of the data product: rwb-source-data (P1) (GAP-2849).
- The vehicle repossession route and the deed in lieu route of the same step: the CON baselines of RWB-S5-E3019 and RWB-S5-E3020, which declare their own element values and consumed rows.
- The holding-age clock, the provision steps, the monthly cost of carry and the re-appraisal Schedule JOB-19: the holding and re-appraisal stories of this service, with the posting itself in rwb-payment (P8).
- The start and floor price, the listing and the auction rounds of the bank's own sale: the pricing and auction baselines and stories, API-S5-004 and API-S5-005 and the `GET /assets/{assetKey}` row.
- The valuations of the asset: rwb-valuation (S1) under API-S5-003 and the Ownership Map ruling.
- The authoring, testing, approval and versioning of the DISPOSAL package and of the rule rows of R-DIS-01, R-DIS-02, R-DIS-03 and R-DIS-06: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
