# RWB-S5-E4025-CON Accept a bid below the floor with a second signature - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4025-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-025, the baseline the below-floor branch of rwb-asset builds against on Day 1. The baseline declares the three asset reads and the round write that answer SCR-23 Listing and price and SCR-21 Asset list on `/api/recovery/asset/v1` (DP-13), the three consumed rows of rwb-source-data and rwb-case (DP-05), the decision-record element of DP-03, the approval item the second signature is raised on and the sale elements of an accepted bid, the rights and the error envelope, and the fakes. The step publishes no event and consumes none, because the owned event of the service is EV-22 `AssetTakenOn` and the bid, the signature and the case state are workflow facts. No source publishes the operation names of the consumed rows (GAP-2912; ASM-4810); no source names a field for the bid or the signature (GAP-2913; ASM-4811); the legacy endpoints table names the listings write while the TSD gives the round write the sale answer (GAP-2914; ASM-4812); no operation raises an approval item (GAP-2915; ASM-4813); the split plan carries no requirement id (GAP-2916; ASM-4814); and the rule package and the approval template are declared without a pattern or platform row of the slice (GAP-2917; ASM-4815). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the below-floor accept step of rwb-asset — its asset and listing reads, its round write, its consumed rows, its decision-record and approval elements, the sale elements of an accepted bid, its rights, its error envelope and its fakes — baselined and tagged before the build starts**, so that **the application story, the rounds story and every consumer can build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-025. It owns:

- the document that fixes the three asset reads and the round write on base `/api/recovery/asset/v1`, with their parameters, their documented answer, their rights and their idempotency (DP-13);
- the three consumed rows: the rwb-source-data appraisal and asset data product, the rwb-case case state read and the rwb-case case-move answer, each with its owner, its use and its placeholder where the operation name is not published (DP-05);
- the decision-record element and the local library dependency that carries it (DP-03);
- the approval element: the item a below-floor bid is routed on, its level, its clock and its outcome, declared as rwb-decision's reference and not as a table or a rule of this service;
- the sale elements of an accepted bid on `asset_sale` and the status element of `listing`, with their fields of TSD S5 T3.1 and their closed lists of T3.2;
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, so that every downstream answer has a stub on Day 1;
- the naming and boundary rules of the baseline: one base, one topic, one queue, no foreign schema, no monolith base, no Schedule for the approval clock.

It does not own: the below-floor behaviour, the rule evaluation, the approval request, the sale write, the decision records and the case moves, which are RWB-S5-E4025-APP; the rounds and their bids, which are the rounds story's (RWB-E4-024); the start price and the floor, which are FEAT-AST-11's; the re-list after a refusal, which is RWB-E4-026; the appraisal and NPA asset facts, which are rwb-source-data's (P1); the approval record, the DoA levels and limits, which are rwb-decision's and rwb-access's; the rule package, which is rwb-decision's; the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

### 2. Business rationale

A contract baseline is what lets the stories of one wave build at once. Without it the below-floor step would be written against whatever shape the round answer happened to expose that week, and the first integration would find the mismatches instead of the review. With it, the application story builds on Day 1 against a tagged document and its fakes, the rounds story knows what its write must carry for the accept to ride on it, and rwb-decision knows which elements of its approval the asset side reads.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner and its use, and where the source documents do not publish an operation name the row carries the placeholder rather than an invented path (GAP-2912; ASM-4810).
- **one hop, one budget.** Every consumed row is a single hop with a 2 s timeout, a breaker and no chain, which is ADR-020; the approval is not a REST row because it runs on rwb-decision's queue over Temporal (Architecture v5 slide 13).
- **additive only.** The baseline moves forward without breaking: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version and a new document (C1).

The business outcome the baseline protects is the one FEAT-AST-16 of the FSD names: a bid under the floor is routed for a second approval before it can be accepted. The baseline does not state that outcome, and no criterion here asserts a business value.

### 3. Preconditions

- The Ownership Map rows are in force: S5 owns `GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds`; `asset_sale` and `listing` are S5's tables; the `asset` extension is named only.
- The service naming is fixed: schema `rwb_asset`, login `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with `.retry` and `.dlt`, task queue `rwb-asset` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.asset`.
- The owned event row of the service is EV-22 `AssetTakenOn` (TSD S5 T5.3), and the elements of this baseline touch none of the events of the service: the round, the bid and the signature are workflow facts.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). The rules kit and the approval template of the workflow kit are platform capabilities and add no H row to this slice (GAP-2917; ASM-4815).
- The approval record `approval` and the delegation facts `delegation_limit` are P7's and P4's; the baseline names them and declares none of their fields (GAP-2915; ASM-4813).
- The accept surface is fixed at `POST /listings/{listingId}/rounds` (API-S5-005) because its documented answer is the `AssetSale` and its right is U, which the legacy endpoints table does not say (GAP-2914; ASM-4812).
- The bid amount and the signature have no column in TSD S5 T3.1, so their elements carry the placeholder until an owner names them (GAP-2913; ASM-4811).
- No approval is needed to publish a Draft baseline; the document is baselined by this story's own review, and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map, the TSD S5 T-A.1 operations, the TSD S5 T3.1 fields and the lists of T3.2.
2. Every operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the operation name is not published.
4. The decision-record element is declared with the library that carries it, and the approval element with its owner, its level, its clock and its outcome — as a reference, never as a table or a rule of this service.
5. The sale elements of an accepted bid and the listing status element are declared with their field IDs and their closed lists.
6. The fakes are declared with their documented answers, one per consumed row, one for the approval and one for the composite route.
7. The schema, the open lists and the closed lists are published, and the compatibility check runs: a breaking change fails the check.
8. The document goes to review as Draft; the reviewers are the owners of the consumed rows, the rounds story owner and the tech lead of the service.
9. On the review's close the document is tagged and baselined; the application story starts against the tag and the fakes.
10. A defect found in the build that needs a shape change is raised against this document, and the document moves to a new minor or major version; the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row or element carries the placeholder and the gap; no path and no field is invented | C2, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails, the version becomes a new major and the document is re-reviewed | C1 |
| X3 | A declared operation reaches another service's data or base | The review refuses the baseline and the boundary test fails the build | C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged; the application story cannot start | C6 |
| X5 | The rights of an operation are not one of the rows of the access matrix | The operation is not declared and the error set of the operation is incomplete | C5 |
| X6 | An owner changes its documented answer after the tag, or the rounds story claims the round write differently | The owner publishes a new version, this document follows with a minor or major version, and the application story re-tests against the new fake | X2 |
| X7 | Two documents claim the same path, or a document claims a column the sources do not name | The naming rule and the placeholder rule resolve it: the owner in the Ownership Map keeps the path, and the column stays Not specified in the source documents | C2, C3, C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 the paths of a baseline moving under a build, and X7 the naming and placeholder boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the order of the sections and the fake data are this story's choice; the paths, the owners, the base, the error set and the element names are fixed by their sources |
| Valuable | The stories of wave 3 build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, four provided operations, three consumed rows, three element groups, seven fakes and one compatibility check |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the below-floor accept step

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema and the open and closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The elements and the closed lists are published as declared (new, D-RCV-60)
    Given the baseline document of this story
    When the sale elements of an accepted bid, the listing status and the element lists are read
    Then every element carries its type, its nullability, its source field ID and its closed list
    And the sale elements are the fields DF-SAL-009 to DF-SAL-019 and the status is the LOV-LISTING list, referenced with its identifier and version and never enumerated in code
    And the bid amount and the signature reference carry the placeholder and its gap identifier because no source names a column for them

  Scenario: C3 The provided reads and the round write are declared once with their rights (new, D-RCV-60)
    Given the operations the baseline provides on base /api/recovery/asset/v1
    When the method, path, documented answer, right and idempotency of each are read
    Then the three asset reads carry the Asset and disposal right R with scope applied and no idempotency
    And POST /listings/{listingId}/rounds carries the right U, the Idempotency-Key header, the AssetSale answer and the 409 and 422 errors
    And the round write is named as shared with the rounds story of RWB-E4-024 and the legacy endpoints table of RWB-E4-025 is recorded as the conflicting row

  Scenario: C4 The consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-source-data and rwb-case are read
    Then each row names its owner, its use and its 2 s budget
    And where the operation name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C5 The error envelope is declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the error set and the rights of each operation are read
    Then the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001, MSG-S5-001 or MSG-S5-002 and 503 in one problem envelope
    And the capability area and the right of each operation are the rows of the access matrix

  Scenario: C6 The decision-record, approval and fake elements are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the approval element and the fake table are read
    Then the decision-record element names RWB-PLT-E1027-CON as its library and the transaction it joins
    And the approval element names rwb-decision as its owner, the level and the two-working-day clock as values in force and the outcome as its only answer, and declares no approval table and no rule row
    And every consumed row and the approval have a fake with a documented answer, including the stopped decision-record stub, the refused signature and the expired clock

  Scenario: C7 The naming and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue and the schema of the baseline
    When the document is checked against the naming rule and the ownership map
    Then the base /api/recovery/asset/v1, the queue rwb-asset and the topic rwb.asset.events.v1 are the only ones declared as this service's own
    And no foreign schema, no foreign topic, no monolith base /api/recovery/v1 and no Schedule for the approval clock is declared
    And no event is published or consumed by the step and no approval row is declared as this service's
```

The seven criteria are new to this run and are tagged as such: they test the contract deliverable only — the schema, the elements, the lists, the operations, the consumed rows, the rights, the envelope, the two library elements, the fakes and the boundary. No criterion states a business outcome or a business value of the application story, and none asserts that a rule fires, that a signature is given or that a case moves.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, event and table: the baseline declares only the rows the Ownership Map gives to S5, and names every other row with its owner | Ownership Map; Architecture v5 slide 41 |
| BR2 | A consumed row or element with no published name carries the placeholder and its gap, and never an invented path or field | Template and Rules v1 §R9; GAP-2912; GAP-2913 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; C1 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain | ADR-020 |
| BR5 | No event is published and none is consumed by the step: the owned event is EV-22 `AssetTakenOn`, the take-on story's, and the bid, the signature and the case state are workflow facts | TSD S5 T5.3; C7 |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR7 | The approval is rwb-decision's and the delegation facts are rwb-access's: the baseline names the item, the level and the clock and declares no approval table, no DoA row and no approval operation | DP-01; Ownership Map rows `approval` and `delegation_limit`; GAP-2915 |
| BR8 | No business value is declared in the baseline: the floor, the approver's limit, the two clocks, the codes and the thresholds are referenced with their identifier and version | Template and Rules v1 §R7.2 (s16); legacy Guardrails |
| BR9 | No personal data in any element, fake or example of the baseline: the bidder and the approver are references, never names | Template and Rules v1 §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

### 9. State transitions

The document itself is the object of this section: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, row, element, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the consumed rows and the rounds story owner are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | New optional element only, compatibility check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer, or the rounds baseline claims the round write differently | X6 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name, or an element has no column | X1 | The row or element carries the placeholder and the gap and the draft continues |
| In review | A row reaches a foreign schema, base or topic, or declares an approval table | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row or the approval has no fake | X4 | Not tagged, the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Authors the baseline, resolves the shape of the service's own operations and signs the tag |
| Owner of rwb-source-data (P1) | Reviews the appraisal and asset data-product row and its freshness stamp |
| Owner of rwb-case (P3) | Reviews the case state and case-move rows and publishes the operation names when they exist |
| Owner of rwb-decision (P7) | Reviews the approval element, the level and the clock, the rule package and the decision-record element with the platform library |
| Owner of the rounds story (RWB-E4-024) | Agrees the shared round write and the fields it must carry for the accept to ride on it |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the rights of each declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The asset answer of `GET /assets/{assetId}` and of `GET /assets/{assetKey}` | S5 (`rwb_asset`) | The asset of status 200 with its title, its listing, the round price, the floor and the round number | Read by the screens; written by the application story |
| The asset page of `GET /assets` | S5 (`rwb_asset`) | The paginated asset list with its filters and its paging elements | Read by the screens |
| The sale elements of `asset_sale` (DF-SAL-009 to DF-SAL-019) | S5 (`rwb_asset`) | sale id, asset id, listing id, contract date, sale date, sale price, transfer fee, specific business tax, corporate income tax, gain or loss, incentive | Written by the application story |
| The listing elements of `listing` (DF-SAL-001 to DF-SAL-008) | S5 (`rwb_asset`) | sale_channel, start_price, floor_price, round_no, listed_at, status, referenced with `LOV-SALE-CHANNEL` and `LOV-LISTING` | Read, and the status written, by the application story |
| The bid amount and the signature reference | S5 (`rwb_asset`), and P7 for the signature | Not specified in the source documents for the elements they occupy (GAP-2913; ASM-4811); declared only once their owner names them | Read by the step, where a column is named |
| The appraisal elements of the consumed read | P1 (`rwb_source_data`) | The appraised value, the appraisal date, the outlier flag and the book value; referenced, not redefined | Consumed |
| The case elements of the consumed read | P3 (`rwb_case`) | The case reference, the case state and the stage outcome; referenced, not redefined | Consumed |
| The decision-record elements | PLT library, created in `rwb_asset` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time (DF-DEC-001 to DF-DEC-018) | Written through the library |
| The approval elements | P7 (`rwb_decision`) | The approval reference, the level, the clock, the outcome and the approver role (DF-REF-001 to DF-REF-015 with the approval record) | Referenced only |
| The rule-package elements | P7 (`rwb_decision`) | The package name, its version in force and the rows R-DIS-41 and R-DIS-42 | Referenced only |

The baseline declares no new table, no new column and no migration, and it enumerates no business value: every list, code and threshold is referenced with its identifier and its version. **No personal data** appears in any element, fake or example; the fixture identifiers are synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). These are the reads that answer SCR-23 and SCR-21 and the write the accepted bid rides on.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, its listing, the round price, the floor and the round number (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetKey}` | Asset of status 200 out on the business key of the Ownership Map | Asset and disposal, right R, scope applied | Not applicable |
| POST | `/listings/{listingId}/rounds` | AuctionRoundRequest in; AssetSale out on a recorded round and an accepted bid; 409 when the round or the listing is not in the state the write expects; 422 on a missing field or a floor under the approver's limit (API-S5-005) | Asset and disposal, right U, scope applied | Idempotency-Key header |

The round write is declared once for two stories: the rounds story of RWB-E4-024 records the round and its bids, and this slice records the accepted bid and the sale it agrees. No source splits the operation. The legacy endpoints table of RWB-E4-025 names `POST /assets/{assetId}/listings` (API-S5-004) instead, which the TSD documents as the price-and-floor write answered with an `Approval`; the TSD outranks the story master under §R3, so the accept rides API-S5-005 and the conflict is recorded as GAP-2914 with ASM-4812. `POST /assets/{assetId}/listings` is declared by the pricing story and by RWB-S5-E4022-CON and is not declared here.

The error envelope of the declared operations: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope asset or listing, 409 for a round or a listing not in the state the write expects, 422 with MSG-GEN-001 for a missing field, with MSG-S5-001 for a floor under the approver's limit and with MSG-S5-002 for an appraisal more than a year old, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The appraisal and asset data product (operation name Not specified in the source documents (GAP-2912; ASM-4810)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The appraised value, the appraisal date, the outlier flag and the book value, with the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state the rules check before they fire; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2912; ASM-4810)) | rwb-case (P3) | P3 rwb-case | The answer that carries the stage outcome with its rule version; on the workflow boundary it is the outcome the parent applies; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag rather than inventing a surface (BR2). The second signature is not a consumed row: it is raised and answered on rwb-decision's queue over Temporal (§12.5).

#### 12.3 Events published

None. The owned event row of this service is EV-22 `AssetTakenOn`, published by the take-on story when the asset record opens, and no source names an `AssetSold` event. This baseline declares neither as its own, adds nothing to `rwb.asset.events.v1`, and the step writes no outbox row: its outward surface is the sale row, the approval request and the case-move answer.

#### 12.4 Events consumed

None. The round, the bid, the signature and the accepted appraisal arrive as signals of `AssetDisposalWorkflow`, so the baseline declares no topic subscription, no consumer group and no inbox row, and a build that subscribes to a topic not listed by Architecture v5 fails the naming check (BR5, DP-14).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference, the listing reference and the rule package in force; signals: the round and its bid, the second signature, the accepted re-appraisal |
| The below-floor branch activity | Activity, one per outcome, named by the application story | `rwb-asset` | The case, the listing and the bid in; the rule IDs with their versions, the approval request, the sale reference and the stage outcome out, in one transaction |
| `ApprovalWorkflow` | Child workflow, the workflow kit's approval | rwb-decision (P7) | The item: the amount, the floor, the asset reference, the rule and its version, the level and the two-working-day clock of R-DIS-41 |

The workflow is the same execution the take-on, holding, sale and ladder stories of this service use; this baseline fixes its input and signal elements, the shape of the approval request it raises and the sale it agrees, and it declares no second queue. The activity name is a design choice of the application story, and the baseline leaves it open.

#### 12.6 Schedules

None. R-DIS-41's two-working-day clock belongs to the approval routing on rwb-decision's side and the stage's wait is a durable timer inside the workflow, so the baseline declares no Temporal Schedule and no legacy Quartz job for the accept. The single Schedule of the service is JOB-19, which the re-appraisal story of this service owns and which is not declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset_sale | S5 (`rwb_asset`) | The agreed sale; the baseline declares the elements of DF-SAL-009 to DF-SAL-019, not its schema |
| listing | S5 (`rwb_asset`) | Read, and the status written; the baseline declares the elements of its price, round and status |
| decision_record | PLT library, created in `rwb_asset` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated signal or request and the answer it holds |
| asset | S5 (`rwb_asset`), named only | The ACE asset extension of TSD S5 T3.1; read on the asset answer, never written here |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `approval`, `delegation_limit`, `decision_log_entry` and `rule_row` (P7 and P4), `valuation` (S1), `document` (P5), `deviation` (S8) and every `v_ace_*` view (P1) are named by their owner and never declared here. No bid table and no signature column is declared: both are Not specified in the source documents and are declared only once their owner names them (GAP-2913; ASM-4811).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data appraisal and asset fake | The appraisal `AP-2026-000541` of asset `AST-2026-000541` with its value, its date and a clear outlier flag, and the NPA asset with its book value; an appraisal more than a year old; a stale product with its date; no answer beyond 2 s | C4, C6 |
| rwb-case case-state and case-move fake | The case states `BID_RECEIVED` and `SECOND_SIGNATURE_PENDING` of the fixture cases; the moves accepted and a move refused for a state the rule does not expect | C4, C6 |
| rwb-decision approval fake | An approval item open with its level and its clock; a given signature with the approver role; a refused signature; an expired clock | C6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-41 and R-DIS-42 | C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-23 and SCR-21 answer for case `RC-2026-000541`, with the listing, the round price and the approval state read once | C2, C6 |
| Bid and floor data fake | A bid under the floor, a bid at the floor and a bid above it, with a floor under the approver's limit (MSG-S5-001) | C2, C5, C6 |

Each fake answers only what its owner documents, and a fake that answers more than the document fails the review. The operation names that are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2912; ASM-4810).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 2 consumed | The three asset reads and the round write on `/api/recovery/asset/v1`; the rwb-source-data data-product row and the rwb-case state and case-move rows; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The bid, the signature and the case state are workflow facts; nothing is published |
| Temporal | 1 workflow, 1 activity, 1 approval child | `AssetDisposalWorkflow` on `rwb-asset` and the approval on rwb-decision's queue; no Schedule |
| File | None | No file element is declared; the portal and HOME.SCB publication is FEAT-AST-12's |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4025 CON Accept a bid below the floor with a second signature - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S5-E4025.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operations, the consumed rows, the published and consumed events, the workflow, its activity and the approval child, the schedules, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Open shapes carried into the tag.** Four shapes are carried as placeholders and not invented: the operation names of the rwb-source-data product and of the case-move answer (GAP-2912; ASM-4810), the bid and signature elements (GAP-2913; ASM-4811), the shared round write against the legacy endpoints row (GAP-2914; ASM-4812) and the approval item's create path (GAP-2915; ASM-4813). A placeholder is a declared forthcoming shape, not a permission to guess.

**Done when.** The seven criteria pass, the reviewers of the three consumed owners and of the rounds story have closed their comments, the compatibility check passes on the tag, the fakes are published with their documented answers, and RWB-S5-E4025-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Asset and disposal right calls one of the declared operations | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of a declared request is absent or invalid | Enter {field}. |
| MSG-S5-001 | A declared write carries a floor under the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | A declared write carries an appraisal more than a year old | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published operation name, or an element no column | Not specified in the source documents (GAP-2912; ASM-4810). |

The five message IDs are carried from the service and platform sets and are declared only as the envelope rows of the operations in this baseline; the two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-23 Listing and price and SCR-21 Asset list through the gateway-bff composite route (DP-19). What this story fixes is the element list of the declared responses and the empty, loading, refused, conflict, below-floor, second-signature, at-floor and stale states the route can show from this service's answers and from the approval state. The route itself, its merge order and its field list are RWB-PLT-N001-CON, and the screens' transitions are the application, pricing and rounds stories'.

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-025-01 | C2: the sale elements, the listing status and the closed lists the declared answers carry | Contract | The published schema and a recorded sale answer of case `RC-2026-000541` |
| TC-E4-025-02 | C3, C5: the provided operations, their rights and their error set | Contract | One request per operation and per right, including a role without it, a 409 conflict and the two 422 floors |
| TC-E4-025-03 | C4: the consumed rows of rwb-source-data and rwb-case | Contract | The three consumed rows, each with and without a published operation name |
| TC-E4-025-04 | C5: the error envelope of the declared operations | Contract | One request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-025-05 | C7: the naming and the boundary rule | Contract | The base, the topic, the queue and the schema, plus a draft that names a foreign schema, a monolith base, a Schedule or an approval table |
| TC-E4-025-06 | C6: the decision-record and approval elements | Contract | The element list, the stopped stub, a refused signature, an expired clock and a package declared with a rule table |
| TC-S5-E4025-CON-01 | C2: the bid and signature placeholders | Contract | The element list with and without a named column |
| TC-S5-E4025-CON-02 | C6: the fakes and their documented answers | Contract | The seven fakes, the stopped stub and one fake that answers more than its document |
| TC-S5-E4025-CON-03 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |
| TC-S5-E4025-CON-04 | C7, BR5: no event published and none consumed, and no approval row declared | Contract | The outbox declaration, empty, the absent subscription row and the absent approval table |

The six legacy case IDs are mapped onto this contract deliverable in their legacy order, and their `Covers` names the criterion of this story that fixes the surface each legacy case touches: the elements and lists an accepted bid carries (01), the operations and rights the accept uses (02), the consumed rows (03), the failure and error path (04), the naming boundary (05) and the decision-record and approval elements (06). The four `TC-S5-E4025-CON-` cases are new and test the parts of the baseline that no legacy case touches: the placeholders, the fakes, the compatibility check and the absence of an event and of an approval table. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the baseline: the floor, the approver's limit, the two clocks, the codes and every threshold are referenced with their identifier and version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the appraisal and asset facts appear only as the rwb-source-data data product (DP-05).
- The case stays with rwb-case, the rules, the approval and the DoA stay with rwb-decision, and the limits with rwb-access: no `recovery_case` element, no rule row, no approval table and no delegation row is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Schedule for the approval clock, no event published or consumed by this step.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id for this slice; the requirement the baseline serves is FEAT-AST-16 of the Epics 3 to 8 Specification v3 and FSD S5 A2.16, that a bid under the floor is routed for a second approval before it can be accepted (GAP-2916; ASM-4814) | The baseline, its consumed rows, its approval element and its fakes | TC-S5-E4025-CON-01, TC-E4-025-03 |
| ADR-013 | 19 services inside ACE | The baseline's ownership rows | TC-E4-025-05 |
| ADR-014 | Schema and login per service | `rwb_asset` and the declared tables | TC-E4-025-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows and the compatibility check | TC-E4-025-03, TC-S5-E4025-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its library | TC-E4-025-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-025, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 are carried by RWB-S5-E4025-APP; this story carries no legacy criterion and tests the surface they touch |
| Test cases | TC-E4-025-01 to TC-E4-025-06 at Level Contract, and TC-S5-E4025-CON-01 to TC-S5-E4025-CON-04 |
| Feature and screens | FEAT-AST-16, SCR-23 Listing and price and SCR-21 Asset list, read through the composite route |
| Rules | R-DIS-41 and R-DIS-42, referenced as rule-package rows and not evaluated here |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The below-floor behaviour, the rule evaluation, the approval request, the sale write, the decision records and the case moves: RWB-S5-E4025-APP.
- The rounds, the bids and the award, and the round and bid rows behind API-S5-005: the rounds story of RWB-E4-024 (GAP-2914).
- The start price and the floor and the approval of the floor: the pricing story of FEAT-AST-11 and RWB-S5-E4022-CON.
- The descending price schedule: RWB-E4-022 and its story pair.
- A refused signature and the return of the asset to the schedule: R-DIS-43 and the re-list story of RWB-E4-026.
- The approval record, the DoA routing, the levels and the limits, the approval screen and its escalation: rwb-decision (P7), rwb-access (P4) and FEAT-APD-01 (GAP-2915).
- The workflow kit's approval template, the rules kit and their platform rows: RWB-PLT-WF and the platform epics (GAP-2917).
- The appraisal and asset facts and the freshness stamp: rwb-source-data (P1).
- The case of record, its route states and the parent workflow: rwb-case (P3).
- The rule package, its version and its approval: rwb-decision (P7).
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The composite route, its merge order and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
