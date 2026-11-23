# RWB-S5-E3019-CON Take a repossessed vehicle onto the books — contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3019-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of RWB-E3-019 for rwb-asset (S5, wave 2) is published as its own story so the app slice can build on Day 1. The baseline fixes the two read operations on `/api/recovery/asset/v1` (DP-13), the `asset` element and its four closed lists, the `AssetTakenOn` envelope on `rwb.asset.events.v1`, the consumed rwb-source-data data-product row, the workflow boundary to rwb-case, the decision-record element of DP-03, the error set and the seven fakes. It declares no `v_ace_*` property, no `recovery_case` property and no consumed event. The operation names of the rwb-source-data read and of the case boundary are placeholders because no source publishes them (GAP-2838; ASM-4697, ASM-4700). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **service team and the consumers of rwb-asset (the app story, the two screens, the wave 2 harness and the owners of rwb-source-data, rwb-case, rwb-payment and rwb-decision)**, we want **one tagged contract baseline for the vehicle take-on — its two reads, its `asset` element and lists, its event, its consumed rows, its error set and its fakes**, so that **the take-on can be built and tested in parallel on both sides of every boundary without waiting for the live services**.

This story owns the shapes and nothing else:

- the OpenAPI 3.1 document with `GET /assets` and `GET /assets/{assetId}` on the target base, their filters, their access right and their error statuses (DP-13);
- the `asset` element with the columns of DF-COL-028 to DF-COL-042 and the four closed lists of TSD S5 T3.2;
- the `AssetTakenOn` envelope and its topic, with rwb-case and rwb-payment as its only consumers;
- the consumed rwb-source-data data-product row with its placeholder operation name, its freshness stamp and its one-hop budget (DP-05);
- the workflow boundary to rwb-case as the child's input, signals and stage outcome, and no invented REST case-move operation;
- the decision-record element of DP-03 with its failure behaviour;
- the error envelope and the message set of section 14, and the seven fakes of section 12.8.

It does not own: any business outcome, row, event instance or case move (RWB-S5-E3019-APP); the holding clock and the provision steps (RWB-S5-E3023-APP); the rule rows and their versions (rwb-decision); the case of record (rwb-case); the ACE fact (rwb-source-data); and the implementations of the library, the edge route and the fakes' platforms, which are platform stories.

### 2. Business rationale

A contract baseline is what lets a wave start on Day 1. The take-on step crosses four boundaries — the ACE asset fact, the case, the decision record and the event — and the plan carries no C row for any of them, so without a tagged baseline the app story would wait for the live services and the wave would slip (GAP-2838; ASM-4697, ASM-4700). The baseline also settles the two facts the source documents leave open:

- the `asset` element is rwb-asset's, read from Architecture v5 slides 19 and 41 and TSD S5 T3.1, although the Ownership Map lists only `listing` and `asset_sale` for S5 (ASM-4698);
- the ACE NPA asset fact is consumed and never read as a view, because only rwb-source-data holds the 30 `recovery.v_ace_*` views (DP-05; ASM-4697).

The business effect is the one the legacy story promises — a repossessed vehicle is recorded with its source, its date taken in, its holding cost and its provision step (REQ-S5-001) — and the contract adds nothing to it. No business value is fixed here: the condition codes, the lists and the rule rows stay reference data and rule rows read at their version, so a business person can change them without a contract release.

### 3. Preconditions

- RWB-PLT-E1027-CON is published with its writer schema and stub, so the decision-record element can be declared against the library rather than invented (DP-03).
- RWB-PLT-N001-CON is published, so the two reads are declared once, on the composite route's terms, and no screen contract is duplicated here (DP-19).
- The platform naming and error-library elements are in force: one base, one topic, one queue, one login per service, and one error envelope with one message ID per condition.
- The rwb-source-data data-product catalogue names DP06 Collateral and assets. Its operation names are Not specified in the source documents (GAP-2838; ASM-4697).
- Architecture v5 slide 13 and the Temporal design give the case boundary as a workflow boundary: the S5 row of the connection matrix names Temporal to P7 and listens to S4, with no REST call to P3. rwb-case publishes no REST operation that moves a case state on behalf of a stage (ASM-4700).
- TSD S5 T3.1, T3.2, T-A.1, T6.1 and T5.3 are available as the source of the element, the lists, the two operations, the rights and the event name.
- No approval is needed to publish a Draft baseline; the tag is applied when the contract tests pass and the consumers sign off.

### 4. Flow

1. The baseline is drafted from TSD S5 T-A.1: the two read operations with their purposes, filters, answers and error sets, moved onto `/api/recovery/asset/v1` (DP-13).
2. The `asset` element is written from DF-COL-028 to DF-COL-042 with the required flags of T3.1 and the closed lists of T3.2.
3. The `AssetTakenOn` envelope is written on `rwb.asset.events.v1` with the CloudEvents wrapper, the retry and `.dlt` topics and the consumer list of Architecture v5 slide 43 row 22.
4. The consumed rwb-source-data row is recorded with its owner, its fields, its freshness stamp, its 2 s budget and a placeholder for its operation name (ASM-4697).
5. The rwb-case boundary is recorded as the stage child's input, signal and outcome, with the rule ID and version in the outcome and no case property in any schema (ASM-4700).
6. The decision-record element is recorded against the library schema, with the write-before-change rule and the MSG-P7-003 failure path.
7. The error set, the rights of the two reads and the message texts are recorded.
8. Seven fakes are published, each answering the paths its consumers exercise, and the drift test compares each one with the document.
9. The baseline is reviewed by the app story, the two screens, the wave 2 harness and the four consuming owners, tagged, and handed over.
10. A later additive change is published inside major version 1; a removal, a rename or a retype opens a new major version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A consumer asks for a property this document does not declare | The answer fails schema validation at the consumer, not at the service | MSG-GEN-001 | AC2 |
| X2 | A fake drifts from the document | The drift test fails and the baseline returns to review | None (pipeline log) | AC6 |
| X3 | A `v_ace_*` property, a `recovery_case` property or an ACE table read is added to the document | The absence test fails the build and the change is refused | None (pipeline log) | AC4, AC5 |
| X4 | A second topic, a consumed event or a Schedule is declared | The absence test fails the build | None (pipeline log) | AC3, AC6 |
| X5 | A breaking change is proposed inside major version 1 | The review refuses it and a new major version is opened | None | AC1 |
| X6 | A property carries personal data | The schema test fails and the property is removed | None (pipeline log) | AC3 |

X1 to X6 are the failure paths of the artefact, not of a business transaction; the business failure paths are RWB-S5-E3019-APP's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; it starts on Day 1 from TSD S5 and the two platform baselines and needs no running service |
| Negotiable | The element names, the wording of the descriptions and the shape of the fakes are the author's choice; the operations, the fields, the lists, the event and the consumers are fixed by the sources |
| Valuable | The app story, the two screens and the wave 2 harness build on Day 1 against a tagged document and seven fakes |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, one contract README and seven fake mapping sets |
| Small | Finished inside one week with the consumer sign-off |
| Testable | Each criterion is a validation of the document or a drift test of a fake, run in the pipeline |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the vehicle take-on step of rwb-asset

  Background:
    Given the platform naming and error library is in force
    Given ownership is read from the Ownership Map and Architecture v5: listing and asset_sale are S5, recovery_case and timer are P3, proceeds is P8, every v_ace_* view is P1

  Scenario: AC1 The two provided reads are declared on the asset base with their shapes and errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is produced with this change
    When it is validated against the OpenAPI 3.1 schema and the additive rule
    Then it validates with no error
    Then it declares GET /assets answering AssetPage with status 200 and GET /assets/{assetId} answering Asset with status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then the list declares the filters type, status, region, page and size, and the single read declares the path parameter assetId
    Then the answers 400, 401, 403, 404, 422 and 503 are declared with the one error envelope and one message ID per condition of section 14
    Then neither read declares an Idempotency-Key and neither declares a write method

  Scenario: AC2 The asset element, its required flags and its four closed lists are fixed (new, D-RCV-60)
    Given the asset section of the document
    When it is compared with TSD S5 T3.1 and T3.2
    Then the Asset element declares id, case_id, collateral_id, asset_ref, asset_code, asset_type, transfer_in_type, from_segment, transfer_in_date, book_value, auction_purchase_price, repossessed_date, stock_date, holding_status and holding_cost_to_date, which are DF-COL-028 to DF-COL-042
    Then id, asset_ref, asset_type, transfer_in_type, transfer_in_date, book_value and holding_status are required and the other properties are optional
    Then asset_type is published against LOV-ASSET-TYPE with its six values, transfer_in_type against LOV-TRANSFER-IN with its three values, from_segment against LOV-SEGMENT and holding_status against LOV-HOLDING with its six values
    Then no property is added for a condition, a photograph, a location, a provision step or a case route state, and those facts are named as other owners' or later stories'
    Then no property carries personal data and no schema default carries a business value

  Scenario: AC3 The AssetTakenOn event is declared with its envelope, its consumers and its prohibitions (new, D-RCV-60)
    Given the event section of the document
    When it is compared with Architecture v5 slide 19 OUT and slide 43 row 22
    Then AssetTakenOn is declared on the topic rwb.asset.events.v1 with the event name rwb.asset.AssetTakenOn.v1, produced by rwb-asset, consumed by rwb-case and rwb-payment and by no other consumer
    Then its data carries the case reference, the asset reference, the asset type, the transfer-in type, the taken-on date and the rule ID with its version, and no amount, balance or posting fact
    Then the envelope is CloudEvents and the topic declares its retry and .dlt topics
    Then the schema test fails any property that is personal data
    Then the document declares no consumed event, no second topic and no Schedule

  Scenario: AC4 The consumed rwb-source-data row is declared and the ACE fact stays with its owner (new, D-RCV-60)
    Given the consumed rows of the document
    When they are compared with the rwb-source-data data-product catalogue and Architecture v5 slides 29, 37 and 45
    Then one row declares the read of DP06 Collateral and assets as consumed, with the asset reference, asset code, asset type, transfer-in type, segment, taken-on date, book value, repossessed date, condition, photographs, location and the freshness stamp
    Then the operation name of the row is Not specified in the source documents (GAP-2838; ASM-4697) and the row carries the placeholder
    Then the row is one hop with a 2 s budget and a breaker, and declares no retry of its own
    Then the document declares no v_ace_* path, no v_ace_* property and no grant on another owner's schema, and the boundary test fails a build that adds one

  Scenario: AC5 The case boundary and the decision-record element are fixed without inventing an operation (new, D-RCV-60)
    Given the workflow section and the decision section of the document
    When they are compared with Architecture v5 slide 13 and the decision-record library schema
    Then the case boundary is declared as the stage child's input, its signals and its stage outcome, carrying the case reference, the route state and the rule ID with its version
    Then the document declares no REST operation consumed from rwb-case and no recovery_case property, and records that the routing is Temporal and not REST (ASM-4700)
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the rule ID, the package version, the inputs reference, the outcome and the decided-at time, written before the asset row changes
    Then the element declares the failure behaviour MSG-P7-003 and one healthy and one stopped chain in its stub
    Then the two reads declare the Asset and disposal right R with the scope applied, and the rights of TSD S5 T6.1 are not restated

  Scenario: AC6 The seven fakes and the naming baseline answer the document and hold the boundary (new, D-RCV-60)
    Given the fakes and the naming section of the document
    When each fake is compared with the operation or the element it serves, and each name with the platform naming rule
    Then seven fakes answer the rwb-source-data read, the rwb-case states and outcome, the rwb-payment cost of carry, the rwb-decision package, the decision-record chain, the outbox relay and the composite route
    Then the drift test compares every fake with the document and fails the build on any difference
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the document names recovery_case, timer, proceeds, decision_log_entry, rule_row and every v_ace_* view as other owners' and consumes them only through their contracts or the workflow boundary
```

These six criteria are new under D-RCV-60 and test the artefact only. They restate no business outcome of RWB-S5-E3019-APP and copy no legacy criterion: the four legacy criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The asset record is rwb-asset's, and the document declares its fields, its lists and its required flags on the `asset` element only | Architecture v5 slides 19 and 41; TSD S5 T3.1 and T3.2; ASM-4698 |
| BR2 | The decision record is declared as an element written before the asset row changes, through the local library; a failed write changes nothing | DP-03; TSD S5 T2; legacy AC1 and AC4 |
| BR3 | The ACE asset fact stays with rwb-source-data: the document declares the data-product read as consumed, no `v_ace_*` property and no ACE table read | DP-05; Architecture v5 slides 29, 37 and 45; ASM-4697 |
| BR4 | The case move is answered and not written: the document declares the workflow boundary and no `recovery_case` property and invents no REST case-move operation | Ownership Map (`recovery_case` owner P3); Architecture v5 slide 13; ASM-4700 |
| BR5 | The event is declared once: `AssetTakenOn` on `rwb.asset.events.v1` with rwb-case and rwb-payment as its only consumers | Architecture v5 slide 19 OUT and slide 43 row 22; ASM-4699 |
| BR6 | A POST declares the `Idempotency-Key`; neither read of this baseline declares it, and no write method is declared here | Architecture v5 slide 11; TSD S5 T-A.2 |
| BR7 | The vocabulary is closed: the four lists are published as enumerations and read at their version, and no list value is a constant of the code | TSD S5 T3.2; FSD S5 BR-S5-001 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 s17 |
| BR9 | One base, one topic, one queue and one login per service; the document declares no other service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A change is additive inside major version 1; a removal, a rename or a retype opens a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |

### 9. State transitions

The lifecycle of the document, not of an asset:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the element, the lists, the event, the consumed row, the case boundary and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 2 harness and the owners of rwb-source-data, rwb-case, rwb-payment and rwb-decision accept the document and the fakes | Baselined |
| Baselined | Additive change | A property or a filter is added inside major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | A `v_ace_*` property, a `recovery_case` property, a consumed event, a second topic or a Schedule | In review |

The holding-status machine the document describes is the app story's: HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED, with HELD the take-on value; this baseline fixes the vocabulary and moves no asset.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI and AsyncAPI documents and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change and the correction of the Ownership Map rows the baseline consumes, including the missing `asset` row |
| Consuming teams (the app story, the two screens, the wave 2 harness and the owners of rwb-source-data, rwb-case, rwb-payment and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library this document reuses |
| Data steward | Confirms that no personal data property is declared in an answer, an element or a fake |

### 11. Data

The baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Asset element | `id`, `case_id`, `collateral_id`, `asset_ref`, `asset_code`, `asset_type`, `transfer_in_type`, `from_segment`, `transfer_in_date`, `book_value`, `auction_purchase_price`, `repossessed_date`, `stock_date`, `holding_status`, `holding_cost_to_date` (DF-COL-028 to DF-COL-042) |
| Required flags | `id`, `asset_ref`, `asset_type`, `transfer_in_type`, `transfer_in_date`, `book_value` and `holding_status`; the other eight optional |
| Lists | `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT` and `LOV-HOLDING`, published as enumerations and read as reference data at their version |
| Event data | Case reference, asset reference, asset type, transfer-in type, taken-on date, rule ID and version |
| Decision record | The library element of DP-03, written before the asset row changes |
| Consumed fields | The ACE asset fact of DF-ACE-208 to DF-ACE-219, read on the rwb-source-data contract and never written, copied or joined here |
| Not declared here | `recovery_case`, `timer`, `decision_log_entry`, `rule_row`, `proceeds`, `document`, `notice` and every `v_ace_*` view; `listing` and `asset_sale` belong to later stories of this service |
| Consumed with no source | The operation name of the rwb-source-data read and the name of the case boundary element: Not specified in the source documents (GAP-2838; ASM-4697, ASM-4700) |

No table, no column and no migration is declared by this story; the schema and its Flyway sequence belong to the DB story of this service (DP-15).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paged by page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its holding status and cost to date (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |

Both answer 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, each in the platform error envelope. The operation ids are those of TSD S5 T-A.1 and the paths are the target base, not the monolith form. API-S5-003 to API-S5-005 belong to the pricing, listing and auction stories of this service and are not declared here.

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The read of DP06 Collateral and assets; operation name Not specified in the source documents (GAP-2838; ASM-4697) | P1 rwb-source-data | The ACE NPA asset fact of the case with its freshness stamp; faked |

One hop, 2 s budget, a GET retried once with jitter and a breaker per downstream (DP-11, ADR-020). No other REST call is consumed: the case is reached on the Temporal boundary of section 12.5.

#### 12.3 Events published

| Event | Topic | Documented data | Consumers |
|---|---|---|---|
| `AssetTakenOn` (`rwb.asset.AssetTakenOn.v1`) | `rwb.asset.events.v1`, with `.retry` and `.dlt` | Case reference, asset reference, asset type, transfer-in type, taken-on date, rule ID and version; CloudEvents envelope; no personal data | rwb-case and rwb-payment (Architecture v5 slide 43 row 22), and no other consumer |

`AssetSold` is the second event of the service and belongs to the sale stories; the outbox that relays `AssetTakenOn` is the platform library of DP-09, which the pattern set of this key does not carry (ASM-4699).

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them is a repossession result or a case state. The take-on is triggered on the workflow boundary, so this baseline declares no consumer group, no subscription and no inbox, and fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | The child's input, its signals and its stage outcome; the case reference, the route state and the rule ID with its version cross this boundary |
| `takeOnAsset` | Activity, the one take-on step | `rwb-asset` | The case and the repossession fact in; rule ID with package version, asset reference, event and stage outcome out |

The case boundary is declared here and not as a REST row because the S5 row of the Architecture v5 connection matrix names Temporal to P7 and listening to S4, with no REST call to P3 (ASM-4700).

#### 12.6 Schedules

None. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `asset` | S5, `rwb_asset` | The taken-on asset, its fields, its lists and its holding status; the table the two reads answer from |
| `decision_record` | Platform library in `rwb_asset` | The local hash-linked record of the rule outcome (DP-03) |
| `idempotency_key` | Platform library in `rwb_asset` | The key of the repeated fact and the answer it holds |
| `outbox_event` | Platform library in `rwb_asset` | The `AssetTakenOn` row relayed to `rwb.asset.events.v1` (DP-09 library) |
| `listing`, `asset_sale` | S5, `rwb_asset` | S5's other tables; this baseline names them and declares no shape of theirs |

`recovery_case`, `timer`, `decision_log_entry`, `rule_row`, `proceeds`, `document`, `notice` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The repossession result of `AST-2026-000511` for `RC-2026-000511` with condition, photographs, location and the notice proved; the same fact with the notice not proved; a stale product; no answer inside 2 s; an unreadable answer | AC2, AC4, AC6 |
| rwb-case workflow fake | The states `ASSET_PENDING_TAKE_ON`, `ASSET_ON_BOOKS` and `ASSET_HELD`; an accepted outcome and a refused one | AC5 |
| rwb-payment cost-of-carry fake | The monthly cost of carry posted for `RC-2026-000511` with its posting reference | AC6 |
| rwb-decision package fake | The DISPOSAL package at its version with R-DIS-01 and R-DIS-06 | AC6 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox; a stopped chain | AC5 |
| Outbox relay stub (`RWB-PLT-TE006-CON`) | A relayed `AssetTakenOn`; a relay that fails and retries | AC3 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for `RC-2026-000511` | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The two placeholder names are carried until their owners confirm them (GAP-2838; ASM-4697, ASM-4700).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-source-data data-product read; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `AssetTakenOn` on `rwb.asset.events.v1`; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 1 activity declared | `AssetDisposalWorkflow` and `takeOnAsset` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml`, the `Asset` and `AssetPage` elements, the `AssetTakenOn` envelope in `asyncapi/rwb-asset-v1.yaml`, the vocabulary of the four lists as published enumerations, the contract README rows for the consumed row and the case boundary with their placeholders, the decision-record element against the library schema, and the seven WireMock mapping sets.

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract; no view grant here | None (C in fact; ASM-4697) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/asset/v1` | None |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

DP-05 is applied as a prohibition: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on another owner's schema. DP-13 moves the base and nothing else. DP-19 puts the two reads behind SCR-21 and SCR-22.

**Build steps.** (1) Write the two reads and validate the additive rule. (2) Write the `Asset` element, its required flags and its four lists. (3) Write the `AssetTakenOn` envelope with the no-personal-data and no-second-topic tests. (4) Record the consumed row with its owner, its budget, its freshness stamp and its placeholder. (5) Record the case boundary, the rights and the error envelope. (6) Record the decision-record element and validate it against the library schema. (7) Publish the seven fakes and the drift test. (8) Record the naming baseline and the absence tests, tag the baseline and collect the sign-off.

**Done when.** The document validates in the pipeline, the six contract tests pass, the seven fakes answer every declared path, the drift and absence tests are green, and the consumers have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the asset row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of the case is stale after a late or failed batch (VR-S5-001-1); the check is the owner's | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-S5-001 | Carried from the legacy message set of this key; it names the floor percentage and the approval limit, which are the pricing story's, so no path here raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key; it names the age of an appraisal, which is the re-appraisal story's, so no path here raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |

The six message ids are contract elements and their text is the legacy and FSD wording, copied unchanged.

### 15. Screens and states

| Screen | States served | What the baseline fixes |
|---|---|---|
| SCR-22 Asset record | Take-on; held; listed; sold | The `Asset` answer and its holding status on `GET /assets/{assetId}` |
| SCR-21 Asset list | Loading; list | The `AssetPage` answer and its filters on `GET /assets` |

The composite route is RWB-PLT-N001-CON's and also calls rwb-case, rwb-source-data and rwb-valuation; this baseline fixes the rwb-asset answers only. The refusal, not-recorded and stale-data states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-019-01 | AC1, AC2 | Contract | The repossession result of `AST-2026-000511`; the contract half answers the two reads and the `Asset` element with its lists |
| TC-E3-019-02 | AC2, AC5 | Contract | Case `RC-2026-000511` at `ASSET_ON_BOOKS`; the contract half answers the holding status and the `ASSET_HELD` outcome shape |
| TC-E3-019-03 | AC4 | Contract | The RPS fact with statutory notice proved; the contract half answers the consumed row and its placeholder |
| TC-E3-019-04 | AC5 | Contract | A role without the Asset and disposal right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E3-019-05 | AC5 | Contract | RW-SALEOFF holds CRUA, RW-NPAMGR and RW-ENFORCE hold CRU and every other role of TSD S5 T6.1 holds R; the contract half answers the rights |
| TC-E3-019-06 | AC5, AC6 | Contract | The decision-record stub stopped and a stale product; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S5-E3019-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the filters and the six answers are present |
| TC-S5-E3019-CON-02 | AC3 | Contract | The `AssetTakenOn` envelope validates against CloudEvents and the topic catalogue; the no-personal-data and no-second-topic tests |
| TC-S5-E3019-CON-03 | AC4, AC6 | Contract | The consumed row and its placeholder; the seven fakes match the document, a drifted fake fails the build, and the no-`v_ace_*` and no-`recovery_case` tests |

The six legacy ids are the legacy cases of RWB-E3-019 in their legacy order, carried as the contract half: each Covers value names the criterion that fixes the surface it exercises, and its business outcome is proved by RWB-S5-E3019-APP. The legacy level `System` maps to `Contract` here because the artefact under test is the contract. `TC-S5-E3019-CON-01` to `-03` are new. The full test text is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ids; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the condition codes, the ladder and provision steps, the lists and the rule rows stay data, reference data or the rule package, never a schema default or a code constant.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; every example is synthetic.
- The ACE fact stays with rwb-source-data and the case with rwb-case: no `v_ace_*` path, no `recovery_case` property, no case row write and no invented case-move REST operation (BR3, BR4).
- The money stays with rwb-payment: the document declares no posting, no balance and no cost-of-carry property.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a consumed event, a second topic, a Schedule, a Quartz row or a shared job table.

### 18. Traceability

| Legacy | Contract | Test |
|---|---|---|
| RWB-E3-019 AC1 | AC1, AC2 (the reads and the element that record it) | TC-E3-019-01, TC-S5-E3019-CON-01 |
| RWB-E3-019 AC2 | AC2, AC5 (holding status and outcome shape) | TC-E3-019-02 |
| RWB-E3-019 AC3 | AC4 (the consumed fact that opens the record) | TC-E3-019-03, TC-S5-E3019-CON-03 |
| RWB-E3-019 AC4 | AC5, AC6 (the decision element and its failure path) | TC-E3-019-04, TC-E3-019-06 |

| Source | What it supplies |
|---|---|
| TSD S5 T3.1, T3.2, T-A.1, T6.1 and T5.3 | The `asset` element and lists, the two operations, the rights and the published event |
| Architecture v5 slides 11, 13, 19, 29, 37, 41, 42, 43 and 45 | The additive rule, the call matrix, the topic and consumers, the ACE boundary and the event rules |
| FSD S5 A2.1 | The feature, its rules, its messages and its roles |
| Split plan, slice RWB-S5-E3019-CON | The lane, the wave, the release and the empty dependency rows (GAP-2838) |

### 19. Out of scope

- Any business outcome: the row, the event instance, the decision record instance and the case move (RWB-S5-E3019-APP).
- The holding clock, the provision steps and the cost of carry (RWB-S5-E3023-APP), and the pricing, listing and auction shapes of this service.
- The case of record, its route state and its timers (rwb-case); the ACE ingestion and the `v_ace_*` views (rwb-source-data); any posting or balance (rwb-payment); the rule rows and their versions (rwb-decision); the documents, the notice and the letters (P5, P6).
- The schema, the login, the deployment, the observability and the pipeline (the DB, INF and OPS stories of this legacy key); the composite route and the platform libraries, which are RWB-PLT-N001-CON's and the platform's.
- Any change to a legacy file, to a master or to built Epic 1 and Epic 2 code.
