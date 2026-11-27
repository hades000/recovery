# RWB-S5-E3023-CON Track holding age against the provision steps - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3023-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-023 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the holding-age and provision-step step of rwb-asset, split from RWB-E3-023. It fixes the two read operations on `/api/recovery/asset/v1` with the holding section (DP-13), the holding-age and provision-step elements with their placeholder where no source gives a field name, the provision input element handed to the Finance provision feed, the durable timer contract of `AssetDisposalWorkflow`, the consumed rwb-source-data, rwb-case and rwb-payment rows, the decision-record element of DP-03, the fakes and the absence tests. The plan's C row is None although four owner contracts are consumed, no source gives the thresholds or the feed route, and DP-09, DP-10 and DP-14 are held as prohibitions (GAP-2855, GAP-2856; ASM-4726, ASM-4727, ASM-4730). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E3023-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the holding-age and provision-step step of rwb-asset — the two asset reads with the holding section, the holding-age and provision-step elements, the provision input element, the timer contract, the consumed rwb-source-data, rwb-case and rwb-payment rows, the decision-record element, the tables and the fakes**, so that **the app story, the two screens and the wave 2 harness build against one fixed, testable contract on Day 1 and a holding field, a threshold, a provision input or an answer shape can never drift between rwb-asset, rwb-source-data, rwb-case, rwb-decision and rwb-payment without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy holding step of RWB-E3-023 crossed four boundaries at once: an officer screen, the ACE asset fact, the case state and a monthly charge. The target splits them: rwb-source-data owns the ACE asset fact, rwb-case owns the case and its route states, rwb-payment owns the charge and the ledger, rwb-decision governs the thresholds, and rwb-asset owns the holding age, the provision step and the decision that applies it. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset`. It records that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case` or `rwb_payment`, so DP-05 is declared as a prohibition and the asset fact is consumed on the owner's contract only.

Four points are carried as gaps and assumptions rather than decided quietly: no source available to this WP prints the provision thresholds, the step percentages or the cost-of-carry rate, and the FSD S5 and TSD S5 files named by the WP are absent from `_work/msr/extract` (GAP-2855), the provision input element, the Finance feed route and the rwb-payment activity have no published name (GAP-2856), the plan's C row is None although four owner contracts are consumed (GAP-2856), and the clocks replace Quartz jobs without a Schedule, so DP-10 is a prohibition rather than a dependency (ASM-4726).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `listing` and `asset_sale` are S5's, `recovery_case`, `timer` and `task` are P3's, `proceeds` is P8's, `document` is P5's, `decision_log_entry`, `rule_row` and `rule_package` are P7's. This document never declares another service's table or operation as its own.
- The rwb-source-data data-product contract of DP06 Collateral and assets, the rwb-case state and move rows and the rwb-payment activity are published with their fakes, so the consumed rows name a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2856; ASM-4730).
- The DISPOSAL rule package and its rule rows for R-DIS-06 and R-DIS-09 are governed in rwb-decision (P7); this baseline names them, declares none of them and prints none of their values.
- The `asset` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration (GAP-2855).
- The Finance provision feed publishes its own interface; where it does not, the row carries the placeholder and the fake derives from this document (ASM-4729).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), and the missing approval of the sources is recorded rather than waited on (GAP-2858; ASM-4734).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this step: the two reads with their request and answer elements, the filters, the rights and the error responses.
2. Fix the holding section of the `Asset` element: the fields the Logical Data Model and Data Dictionary v9 gives (DF-COL-031 to DF-COL-040) and the holding age, the cost to date and the next provision step date, each with the placeholder where no source gives a name or a type.
3. Fix the provision input element: what leaves for the Finance provision feed, with the case reference, the asset reference, the threshold, the step applied, the rule ID with its version and no personal data.
4. Fix the timer contract of `AssetDisposalWorkflow`: the two timer names, their start dates, their end dates, their rearm rule and their pause behaviour, and state that they are durable timers and not Schedules.
5. Fix the consumed rows: the rwb-source-data asset read, the rwb-case state read and move answer, and the rwb-payment cost-of-carry activity, marking the fields the sources do not give with the placeholder.
6. Record the decision-record element of DP-03, written before the asset changes.
7. Record the closed vocabulary, the naming baseline and the rule that no threshold, percentage or rate is a constant of the code.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the placeholder rule, the error envelope, the absence of a `v_ace_*` read, of a `recovery_case` write, of a `timer` write, of an event and of a Schedule, and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-S5-E3023-APP, the two screens and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | A consumed row or a holding property has a name or a type the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC3, AC4 |
| X5 | A threshold, a step percentage or a rate appears as a schema default, an enumeration member or an example value | The vocabulary test fails the build; a value that is not in the package is never published | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case`, `timer` or `proceeds` row | The review fails the baseline; the boundary test fails the build | None | AC5 |
| X7 | The document declares a consumed or published event, a second topic or a Temporal Schedule | The absence test fails the build | None | AC5 |
| X8 | The rights of an operation are not the ones the legacy permission table and the access matrix declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map, the Logical Data Model and the published owner contracts of rwb-source-data, rwb-case and rwb-payment only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the base, the queue, the timers and the prohibitions are fixed by the target architecture |
| Valuable | Unblocks RWB-S5-E3023-APP, the two screens and the wave 2 harness on Day 1, and the rwb-source-data, rwb-case, rwb-payment and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI absence statement, nine contract tables, eight fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the holding-age and provision-step step of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing and asset_sale is S5, of recovery_case, timer and task is P3, of proceeds is P8 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two asset reads are declared on the asset base with their shapes and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /assets with an AssetPage answer of status 200 and GET /assets/{assetId} with an Asset answer of status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then the list declares the filters type, status, region, page and size, and the single read declares the path parameter assetId
    Then the answers 400, 401, 403, 404, 422 and 503 are declared with one envelope and one message ID per condition, and neither read declares an Idempotency-Key
    Then every other property of the two operations is copied from the published baseline of the asset reads and is not redefined here

  Scenario: AC2 The holding section, the age and the provision-step elements are fixed with their placeholders (new, D-RCV-60)
    Given the asset and holding sections of the baseline
    When they are compared with the Logical Data Model and Data Dictionary v9 and with FEAT-AST-05
    Then the Asset element declares the properties of DF-COL-031 to DF-COL-040 as the dictionary gives them
    Then the holding section declares a holding start date, a holding age in days, a cost to date and a next provision step date, read only, and each property whose name or type no source gives carries the placeholder Not specified in the source documents (GAP-2855; ASM-4726)
    Then the provision-step element declares the threshold, the step applied, the rule ID, the package version in force and the Finance input reference, and carries the placeholder for every name the sources do not give
    Then no threshold, no step percentage and no rate is declared as a schema default, an enumeration member or an example value, and the test profile reads them from the rule package
    Then no property is added for a document or a custody fact, and those stay the documents of their owners

  Scenario: AC3 The provision input and the timers are declared without an event and without a Schedule (new, D-RCV-60)
    Given the event, workflow and schedule sections of the baseline
    When they are compared with Architecture v5 slide 19 and with the Temporal and Drools Design slide 13
    Then the provision input is declared as an element handed to the Finance provision feed with the case reference, the asset reference, the threshold, the step applied and the rule ID with its version, and no amount, balance or personal data
    Then the feed route and the element name are Not specified in the source documents (GAP-2856; ASM-4729) and the row carries the placeholder
    Then the baseline declares the holding age timer and the provision step timer as durable timers of AssetDisposalWorkflow on rwb-asset, with their start date, their end date, their rearm rule and their pause behaviour on R-DIS-66 and R-DIS-68 (ASM-4726, ASM-4732), and declares no Temporal Schedule and no Quartz row
    Then the baseline declares no published event and no consumed event on rwb.asset.events.v1, and no second topic
    Then the absence test fails a build that adds an event, a topic, a Schedule or a job row

  Scenario: AC4 The consumed rows stay with their owners and carry their placeholders (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the published owner contracts and Architecture v5 slides 13, 29, 37 and 45
    Then the read of DP06 Collateral and assets is declared as consumed from P1 rwb-source-data, with the stock date, the book value, the asset type, the transfer-in type and the freshness stamp of the data product
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state, the title status and the move ASSET_HELD carrying the rule ID and its version
    Then the monthly cost of carry is declared as a Temporal activity on queue rwb-payment with the case, the asset, the month, the book value and the rule version, and its activity name is Not specified in the source documents (GAP-2856; ASM-4729)
    Then the document declares no v_ace_* path, no recovery_case, timer or proceeds property and no grant on any other owner's schema, and the boundary test fails a build that adds one
    Then each call is one hop with a 2 s budget and a breaker, and no row is retried more than once by this service

  Scenario: AC5 The decision-record element, the rights and the eight fakes answer the document (new, D-RCV-60)
    Given the decision section, the access section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the rule ID, the package version in force, the inputs reference, the holding start date or the threshold, the outcome and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the asset changes, and a failed write leaves the asset unchanged with MSG-P7-003
    Then both reads declare Asset and disposal right R with the scope applied, and the roles the legacy permission table and the access matrix give that right hold it, with no C right declared by this step
    Then the fakes answer the asset fact, the three case states with three title statuses, the accepted and refused move, the cost-of-carry answer, the accepted and refused provision input, the package, a healthy and a stopped record chain, and the composite route
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the tables named as owned are asset and the library objects decision_record and idempotency_key, and recovery_case, timer, task, proceeds, document, decision_log_entry, rule_row, rule_package, listing, asset_sale and every v_ace_* view are named as other owners' and are reachable only through their contracts
    Then the document declares no Schedule, and records that the clocks replace the legacy Quartz jobs without a job table and that the timer row is P3's (ASM-4726, ASM-4728)
    Then the document records that the FSD S5 and TSD S5 files named by this WP are not in the extract set and that the field set is the dictionary's ten asset fields plus the placeholders (GAP-2855; ASM-4726)
```

These six criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E3023-APP and they copy no criterion of the legacy story, whose three criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The holding section, the age and the provision-step elements are rwb-asset's, and the contract declares them on the `Asset` element and on the provision input only | Architecture v5 slide 41; FEAT-AST-05; REQ-S5-003 |
| BR2 | The decision record is declared as an element written before the asset changes, through the local library on the shared topic; a failed write changes nothing | DP-03; legacy RWB-E3-023 AC1 and AC3 |
| BR3 | The clocks are declared as durable timers of the workflow: no Schedule, no Quartz row and no job table is declared, and the `timer` row stays P3's | DP-10 as a prohibition; ASM-4726, ASM-4728 |
| BR4 | The ACE asset fact stays with rwb-source-data: the contract declares the data-product read as consumed, declares no `v_ace_*` property and describes no ACE table read of rwb-asset | DP-05; Architecture v5 slides 29, 37 and 45; ASM-4731 |
| BR5 | The case move is answered and not written: the contract declares the state read and the answer, and no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); ASM-4730 |
| BR6 | The money is rwb-payment's: the cost of carry and the ledger effect of the provision step are declared as its activity and its feed, never as a property of this service | Architecture v5 slide 13 (S5 to P8, Temporal and events); ASM-4729 |
| BR7 | The vocabulary is closed and the values are not published: the thresholds, the step percentages and the rate are package and reference values, named as inputs and never printed as defaults or members | FEAT-AST-05; BR2; GAP-2855 |
| BR8 | A property whose name or type no source gives carries the placeholder and one gap row; a placeholder is resolved by its owner and never by a guess | Template and Rules v1 §R9; GAP-2855, GAP-2856 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | Template and Rules v1 §R7.2 (s17) |
| BR10 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or queue as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Platform versioning rule |
| BR12 | The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |

### 9. State transitions

The lifecycle of this document, not of an asset:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the holding section, the provision input, the timers, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 2 harness and the rwb-source-data, rwb-case, rwb-payment and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new filter or a new optional holding field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the meaning of a timer changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC6 fail: an event, a topic, a Schedule, a job row, a `v_ace_*` view, a `recovery_case` or `timer` property | In review |
| Baselined | A value is published | The vocabulary test of AC2 fails because a threshold or a rate appears in the document | In review |

The clock and step states the document describes are the app story's, and this baseline fixes only their names, their inputs and their pause rule; it moves no asset and arms no timer itself.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the removal of a placeholder when its owner publishes the name |
| Consuming teams (the app story, the two screens, the wave 2 harness and the owners of rwb-source-data, rwb-case, rwb-payment, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the timer kit, the decision-record library and the workflow platform this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element, a provision input or a fake |

The per-service login behind the security scheme of the document is named "the rwb-asset login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Asset element | The properties of DF-COL-031 to DF-COL-040: `asset_ref`, `asset_code`, `asset_type`, `transfer_in_type`, `from_segment`, `transfer_in_date`, `book_value`, `auction_purchase_price`, `repossessed_date` and `stock_date` |
| Holding section | A holding start date, a holding age in days, a cost to date and a next provision step date, read only; the names and types not given by a source carry the placeholder Not specified in the source documents (GAP-2855; ASM-4726) |
| Provision-step element | The threshold, the step applied, the rule ID, the package version in force and the Finance input reference, with the placeholder for the names the sources do not give |
| Provision input | The case reference, the asset reference, the threshold, the step applied and the rule ID with its version; the element name and the feed route are Not specified in the source documents (GAP-2856; ASM-4729) |
| Timers | The holding age timer and the provision step timer of `AssetDisposalWorkflow`: start date, end date, rearm rule and pause behaviour (ASM-4726) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the asset changes (DP-03) |
| Not declared here | `recovery_case`, `timer` and `task` (P3), `document` (P5), `proceeds` (P8), `decision_log_entry`, `rule_row` and `rule_package` (P7), `listing` and `asset_sale` (S5, later stories'), every `v_ace_*` view (P1) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the placeholders, the vocabulary rule of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated by page and size | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its holding section, its cost to date and its next provision step date | Asset and disposal, right R, scope applied | Not declared |

The two operations answer 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The paths are those of the target base, not the monolith form. `POST /assets/{assetId}/listings` and `POST /listings/{listingId}/rounds` belong to the pricing and auction stories of this service and are not declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2856; ASM-4730)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE NPA asset fact: stock date, book value, asset type, transfer-in type and the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the title status the confirmation carries; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2856; ASM-4730)) | rwb-case (P3) | P3 rwb-case | The move `ASSET_HELD` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2856 with ASM-4730. The cost-of-carry request and the Finance provision input are not REST rows of this service: the first is a Temporal activity (12.5) and the second leaves on the feed (12.3).

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset `AssetTakenOn` and `AssetSold`, and neither is a holding-age or provision-step event; the provision input leaves on the Finance provision feed and not on a Kafka topic. This baseline therefore declares no published event, no consumer group of its own and no outbox row, and the absence test of AC3 fails a build that adds one (GAP-2856; ASM-4727).

| Element published outside Kafka | Owner of the target | Documented content |
|---|---|---|
| The provision input to the Finance provision feed | The feed's owner; the route is Not specified in the source documents (GAP-2856; ASM-4729) | The case reference, the asset reference, the threshold, the step applied and the rule ID with its version; no amount, balance or personal data |

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them starts a holding-age or provision-step step; the step is started by the confirmation signal the parent forwards and by its own durable timer. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC3 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the holding | `rwb-asset` in namespace `rwb-recovery` | The stage that hosts the holding and provision steps; its signals, its two timers and its outcome for the parent are declared, not built |
| `applyHoldingStep` | Activity, the confirmation step | `rwb-asset` | The case and the confirmation in; the rule ID with its package version, the holding start date, the next provision step date, the cost to date and the case move out |
| `applyProvisionStep` | Activity, the provision step | `rwb-asset` | The case, the threshold and the asset in; the rule ID with its package version, the step applied, the provision input reference and the next threshold out |
| `requestCostOfCarry` | Activity, on the owner's queue, activity name Not specified in the source documents (GAP-2856; ASM-4729) | `rwb-payment` | The case, the asset, the month, the book value and the rule version in; the posted amount and its posting reference out |

No child workflow for the case and none for the money exists in this service, and this baseline registers no activity. The two activity names of rwb-asset are a target design choice and no source document fixes them (ASM-4735).

#### 12.6 Schedules

None. The clocks are durable timers inside the workflow and not Temporal Schedules; this baseline declares no Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to RWB-S5-E3026-APP (ASM-4726).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| asset | S5 (`rwb_asset`) | The held asset, its properties and its holding section; the table the two reads answer from |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated confirmation and the threshold it holds |

`recovery_case`, `timer` and `task` (P3), `proceeds` (P8), `document` (P5), `notice` (P6), `decision_log_entry`, `rule_row` and `rule_package` (P7), `listing` and `asset_sale` (S5, later stories') and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The asset facts of asset `AST-2026-000511` with stock date, book value, asset type and transfer-in type; a stale product with its date; no answer beyond 2 s; an unreadable answer | AC1, AC4, AC5 |
| rwb-case state fake | The states `ASSET_ON_BOOKS`, `ASSET_HELD` and `DISPOSAL_PAUSED_DEVIATION`, with title status `clear`, `under_transfer` and `encumbered` | AC4, AC5 |
| rwb-case move fake | The move `ASSET_HELD` accepted and the same move refused | AC4, AC5 |
| rwb-payment cost-of-carry fake | The monthly cost of carry recorded with its posting reference; no answer beyond 2 s | AC4, AC5 |
| Finance provision feed fake | The provision input accepted with its reference, and the feed refusing the input and refusing it again after the retry limit | AC3, AC5 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-06 and R-DIS-09, and the thresholds as values of the package | AC2, AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000511` with the holding section read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data read, of the case-move answer, of the Finance feed and of the rwb-payment activity are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2856; ASM-4729, ASM-4730, ASM-4735).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-source-data data-product read, the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event on this step; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 3 activities declared, 0 registered | `AssetDisposalWorkflow` with `applyHoldingStep` and `applyProvisionStep` on `rwb-asset` and `requestCostOfCarry` on `rwb-payment`; two timers; no Schedule |
| File | None | No file is read, built or delivered here; the Finance feed is not a file of this service |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no asset, no case, no balance and no rule package. What it publishes is one OpenAPI 3.1 document, one absence statement for events, nine contract tables and eight fakes.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml`, the `Asset`, `AssetPage`, `HoldingSection` and `ProvisionStep` elements, the provision input element with its placeholder, the timer contract rows of the workflow catalogue entry, the contract README rows for the consumed rows and their placeholders, and the eight WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on any other owner's schema, because rwb-asset holds none (ASM-4731). DP-13 moves the base and nothing else. DP-19 is behind SCR-21 and SCR-22, whose screen model is the edge contract's. DP-09, DP-10 and DP-14 are held as prohibitions and are not declared: no event, no Schedule and no second topic belongs to this step, and the clocks replace the legacy Quartz jobs (ASM-4726, ASM-4727).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. The three REST rows and the rwb-payment activity are C dependencies in fact and not in the metadata row, and the Finance feed has no owner document (GAP-2856; ASM-4729, ASM-4730).

**Build steps**

1. Write the two reads and validate the additive rule of AC1 in the pipeline.
2. Write the `Asset` properties, the holding section and the provision-step element of AC2, with the placeholder where a name or type is unstated and the vocabulary test on every threshold and rate.
3. Write the provision input element, the feed row, the timer contract and the absence statement of AC3.
4. Record the consumed rwb-source-data, rwb-case and rwb-payment rows of AC4 with their owners, budgets and placeholders.
5. Record the decision-record element, the rights and the eight fakes of AC5 with the drift test.
6. Record the naming baseline and the boundary of AC6, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the six contract tests pass, the fakes answer every consumed path and the drift test is green, every placeholder names its gap and assumption, and the app story, the two screens and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the asset changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added. The Finance feed refusal of X6 has no message ID in any source available to this file, so the contract declares only its error code row and the app story raises a task (GAP-2856).

### 15. Screens and states

The contract serves SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its take-on, held, listed and sold states, all through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset and its holding section, rwb-case for the case and its route state, and rwb-source-data for the ACE asset fact; this baseline fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal and not-recorded states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-023-01 | AC1, AC2 | Contract | Asset `AST-2026-000511`; the contract half answers the two reads, the `Asset` properties and the holding section with its placeholders |
| TC-E3-023-02 | AC2, AC3 | Contract | Case `RC-2026-000511` at `ASSET_ON_BOOKS`; the contract half answers the provision-step element, the provision input and the timer rows |
| TC-E3-023-03 | AC3, AC6 | Contract | The absence tests: no event, no second topic, no Schedule, no job row, no `v_ace_*` path and no `recovery_case` or `timer` property |
| TC-E3-023-04 | AC5 | Contract | A role without the Asset and disposal right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E3-023-05 | AC5, AC4 | Contract | The decision-record stub stopped and the consumed rows; the contract half answers the MSG-P7-003 path, the placeholders and the drift test |
| TC-S5-E3023-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the filters and the six error answers are present |
| TC-S5-E3023-CON-02 | AC2 | Contract | The holding section and the provision-step element validate with their placeholders; the vocabulary test fails a published threshold or rate |
| TC-S5-E3023-CON-03 | AC3, AC4 | Contract | The provision input, the timer rows and the three consumed rows validate; the absence test and the placeholder test |
| TC-S5-E3023-CON-04 | AC5, AC6 | Contract | The eight fakes match the document, a drifted fake fails the build, and the naming baseline and boundary rows are complete |

The five legacy cases are the legacy cases of RWB-E3-023 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E3023-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S5-E3023-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the thresholds, the step percentages, the rate, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member.
- No personal data in a schema, an example, a provision input or a fake: identifiers, codes, amounts, dates and a rule version only; every example is synthetic.
- The ACE asset fact stays with rwb-source-data, the case with rwb-case and the money with rwb-payment: the document declares no `v_ace_*` path, no `recovery_case`, `timer` or `proceeds` property and no posting (BR4, BR5, BR6).
- The clocks are durable timers: a document that declares a Schedule, a Quartz row or a job table fails the absence test.
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or queue as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- Every placeholder names its gap and assumption, and no placeholder is filled by a guess.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the timer kit and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S5-003 | Holding age drives re-appraisal and the provision step by rule (Business Requirements Program v5); the contract fixes the holding section, the provision input and the consumed rows on which the rule runs (GAP-2857; ASM-4733) | The holding section, the provision-step element and the provision input | TC-E3-023-01, TC-E3-023-02, TC-S5-E3023-CON-01, TC-S5-E3023-CON-02 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The two timers and the absence of a Schedule | TC-S5-E3023-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S5-E3023-CON-04 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-E3-023-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-023, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S5-E3023-APP; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the four new contract cases TC-S5-E3023-CON-01 to -04 |
| Feature and screens | FEAT-AST-05, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-06 and R-DIS-09, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Temporal layer, Schedules replace Quartz), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two reads, the evaluation of R-DIS-06 and R-DIS-09, the clocks, the decision record, the cost-of-carry request, the provision input and the case-move answer: RWB-S5-E3023-APP.
- The take-on of the asset, the creation of the `asset` row and the confirmation of the record: RWB-S5-E3019-APP, RWB-S5-E3020-APP and RWB-S5-E3021-APP, which declare their own consumed rows.
- The case of record, its route states, the parent `CaseWorkflow` and the `timer` row: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked (GAP-2856).
- The ACE NPA asset fact and the freshness of the data product: rwb-source-data (P1) (ASM-4731).
- The posting, the ledger effect and the balance of the cost of carry and of the provision step, and the transport and ownership of the Finance provision feed: rwb-payment (P8) and the feed's owner, whose names are Not specified in the source documents (GAP-2856).
- The authoring, testing, approval and versioning of the DISPOSAL package and of the rule rows of R-DIS-06 and R-DIS-09, and the values of the thresholds, the percentages and the rate: rwb-decision (P7).
- The re-appraisal cycle and its order: RWB-S5-E3026-APP and rwb-valuation (S1).
- The listing, the floor price and the auction rounds: the pricing and auction stories of this service.
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
