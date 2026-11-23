# RWB-S5-E4024-CON Run auction rounds and report bids - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4024-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-024 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-024, the baseline the round branch of rwb-asset builds against on Day 1. The baseline declares the asset reads and the round write that answer SCR-24 Auction rounds and SCR-21 Asset list on `/api/recovery/asset/v1` (DP-13), the four consumed rows of rwb-case, rwb-payment and rwb-partner (DP-05), the decision-record element of DP-03, the rule-package element the round branch evaluates against, the rights and the error envelope, and the fakes. No event is published and none is consumed, because the owned event of the service is EV-22 `AssetTakenOn` and the round and payment facts are workflow signals. No source names an element that holds the bids of a round, while the round write answers the `AssetSale` schema (GAP-2906; ASM-4804); no source publishes the operation names of the consumed rows (GAP-2907; ASM-4805); R-DIS-49 sits across the payment-term story (GAP-2908; ASM-4806); the split plan carries no requirement id for this slice (GAP-2909; ASM-4807); the rule package is declared without the DP-04 platform row (GAP-2910; ASM-4808); and the award and its cancellation have no dedicated element (GAP-2911; ASM-4809). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the auction-round capability of rwb-asset — its asset reads, its round write, its consumed rows, its decision-record and rule-package elements, its rights, its error envelope and its fakes — baselined and tagged before the build starts**, so that **the application story and every consumer of a round can build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-024. It owns:

- the document that fixes the two asset reads and the round write on base `/api/recovery/asset/v1`, with their parameters, their documented answer, their rights and their idempotency (DP-13);
- the four consumed rows: the rwb-case case state read and case-move answer, the rwb-payment payment fact and the rwb-partner vendor score, each with its owner, its use and its placeholder where the name is not published (DP-05);
- the decision-record element and the local library dependency that carries it (DP-03);
- the rule-package element: the DISPOSAL package, its version and the five rows this branch evaluates, declared as a reference and not as a rule table of this service;
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, so that every downstream answer has a stub on Day 1;
- the naming and boundary rules of the baseline: one base, one topic, one queue, no foreign schema, no monolith base, no Schedule for a workflow timer.

It does not own: the round behaviour, the rule evaluation, the round write, the decision records and the case moves, which are RWB-S5-E4024-APP; the start price and the floor, which are FEAT-AST-11's story; the publication of the listing, FEAT-AST-12; the step down on a round with no bid, FEAT-AST-13 and FEAT-AST-17's stories; the second signature of a bid below the floor, FEAT-AST-16's story; the five-day payment term, FEAT-AST-18's story; the payment and its posting, rwb-payment's (P8); the vendor panel and scorecard, rwb-partner's (S9); the case of record and its states, rwb-case's (P3); the rule package, rwb-decision's (P7); the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

### 2. Business rationale

A contract baseline is what lets the stories of one wave build at once. Without it the round write would be written against whatever shape the auction portal happened to send that week, and the first integration would find the mismatches instead of the review. With it, the application story builds on Day 1 against a tagged document and its fakes, the pricing, vendor and payment stories know what the round and the listing must carry for the branch to run, and the consumers of the asset reads know exactly which elements they can rely on.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner and its use, and where the source documents do not publish a name the row carries the placeholder rather than an invented path (GAP-2907; ASM-4805).
- **one hop, one budget.** Every consumed row is a single hop with a 2 s timeout, a breaker and no chain, which is ADR-020 and is what the application story's exception paths assume.
- **additive only.** The baseline moves forward without breaking: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version and a new document (C1).

The business outcome the baseline protects is the one FEAT-AST-15 of the FSD names: the vendor runs each round and the bids come back into the case. The baseline does not state that outcome, and no criterion here asserts a business value.

### 3. Preconditions

- The Ownership Map rows are in force: S5 owns `GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds`; `asset_sale` and `listing` are S5's tables.
- The service naming is fixed: schema `rwb_asset`, login `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with `.retry` and `.dlt`, task queue `rwb-asset` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.asset`.
- The published shapes of the declared operations are the API Specification v4: `AssetPage`, `Asset`, `AuctionRoundRequest` with roundNo, heldOn, result and price, and `AssetSale` as the answer of the round write (API-S5-005).
- The owned event row of the service is EV-22 `AssetTakenOn` (TSD S5 T5.3), and the assets of the baseline touch none of the events of the service: the round due and payment-term facts are signals of `AssetDisposalWorkflow`.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). DP-04 is not in the pattern set of this slice, so no platform row for the rules kit is claimed and the package is referenced as rwb-decision's (GAP-2910; ASM-4808).
- No approval is needed to publish a Draft baseline; the document is baselined by this story's own review, and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map, the TSD S5 T-A.1 operations, the TSD S5 T3.1 tables and the lists of T3.2.
2. Every operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The decision-record element is declared with the library dependency that carries it, and the rule-package element with its owner and its version.
5. The fakes are declared with their documented answers, one per consumed row and one for the composite route and the round reports.
6. The schema, the open lists and the closed lists are published, and the compatibility check runs: a breaking change fails the check.
7. The document goes to review as Draft; the reviewers are the owners of the consumed rows and the tech lead of the service.
8. On the review's close the document is tagged and baselined; the application story starts against the tag and the fakes.
9. A defect found in the build that needs a shape change is raised against this document, and the document moves to a new minor or major version; the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and the gap; no path is invented and no field is guessed | C2, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails, the version becomes a new major and the document is re-reviewed | C1 |
| X3 | A declared operation reaches another service's data or base | The review refuses the baseline and the boundary test fails the build | C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged; the application story cannot start | C6 |
| X5 | The rights of an operation are not one of the rows of the access matrix | The operation is not declared and the error set of the operation is incomplete | C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a new version, this document follows with a minor or major version, and the application story re-tests against the new fake | X2 |
| X7 | Two documents claim the same path or queue, or a document invents a bid element that no table names | The naming rule and the placeholder rule resolve it: the owner in the Ownership Map keeps the path, and the bid list stays Not specified in the source documents | C2, C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 are the paths of a baseline moving under a build, and X7 is the naming and placeholder boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the order of the sections and the fake data are this story's choice; the paths, the owners, the base, the error set and the element names are fixed by their sources |
| Valuable | The stories of wave 3 build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, three provided operations, four consumed rows, two library elements, eight fakes and one compatibility check |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the auction-round capability

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema and the open and closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The elements and the closed lists are published as declared (new, D-RCV-60)
    Given the baseline document of this story
    When the element list, the required and optional flags and the closed lists are read
    Then every element carries its type, its nullability and its source
    And every closed list is referenced with its identifier and its version and is not enumerated in code
    And the bids of a round carry the placeholder and its gap identifier because no table or request element holds them

  Scenario: C3 The asset reads and the round write are declared with their rights (new, D-RCV-60)
    Given the operations the baseline provides on base /api/recovery/asset/v1
    When the method, path, documented answer, right and idempotency of each are read
    Then the two asset reads carry the Asset and disposal right R with scope applied and no idempotency
    And POST /listings/{listingId}/rounds carries the right U with the Idempotency-Key header and the 409 conflict
    And POST /assets/{assetId}/listings is named as the pricing story's and is not declared here

  Scenario: C4 The consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-case, rwb-payment and rwb-partner are read
    Then each row names its owner, its use and its 2 s budget
    And where the name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C5 The error envelope is declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the error set and the rights of each operation are read
    Then the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 or MSG-S5-001 and 503 in one problem envelope
    And the capability area and the right of each operation are the rows of the access matrix

  Scenario: C6 The decision-record, rule-package and fake elements are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the rule-package element and the fake table are read
    Then the decision-record element names RWB-PLT-E1027-CON as its library and the transaction it joins
    And the rule-package element names the DISPOSAL package, its owner, its version in force and the five rules, and declares no rule row
    And every consumed row has a fake with a documented answer, including the stopped stub, the stale payment fact and the unanswered vendor score

  Scenario: C7 The naming and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue and the schema of the baseline
    When the document is checked against the naming rule and the ownership map
    Then the base /api/recovery/asset/v1, the queue rwb-asset and the topic rwb.asset.events.v1 are the only ones declared as this service's own
    And no foreign schema, no foreign topic, no monolith base /api/recovery/v1 and no Schedule for the round timer is declared
    And no event is published or consumed by the round branch
```

The seven criteria are new to this run and are tagged as such: they test the contract deliverable only — the schema, the elements, the lists, the operations, the consumed rows, the rights, the envelope, the two library elements, the fakes and the boundary. No criterion states a business outcome or a business value of the application story, and none asserts that a rule fires, that a round opens or that a case moves.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, event and table: the baseline declares only the rows the Ownership Map gives to S5, and names every other row with its owner | Ownership Map; Architecture v5 slide 41 |
| BR2 | A consumed row with no published name carries the placeholder and its gap, and never an invented path | Template and Rules v1 §R9; GAP-2907 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; C1 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain | ADR-020 |
| BR5 | No event is published and none is consumed by the round branch: the owned event is EV-22 `AssetTakenOn`, the take-on story's, and the round and payment facts are workflow signals | TSD S5 T5.3 |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR7 | The rule package is referenced, never redefined: the DISPOSAL package, its version and the five rules are rwb-decision's rows and no rule table of this service is declared | DP-04 (not claimed); GAP-2910 |
| BR8 | No business value is declared in the baseline: the price schedule, the floor, the re-list limit, the codes and the thresholds are referenced with their identifier and version | Template and Rules v1 §R7.2 (s16); legacy Guardrails |
| BR9 | No personal data in any element, fake or example of the baseline; a bidder is a code, never a person | Template and Rules v1 §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

### 9. State transitions

The document itself is the object of this section: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, row, element, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the consumed rows are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | New optional element only, compatibility check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer | X6 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name | X1 | The row carries the placeholder and the gap and the draft continues |
| In review | A row reaches a foreign schema, base or topic | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Authors the baseline, resolves the shape of the service's own operations and signs the tag |
| Owner of rwb-case (P3) | Reviews the case state and case-move rows and publishes the operation names when they exist |
| Owner of rwb-payment (P8) | Reviews the payment-fact row, its due date and its freshness stamp |
| Owner of rwb-partner (S9) | Reviews the vendor-score row and publishes the operation name when it exists |
| Owner of rwb-decision (P7) | Reviews the rule-package element, the DISPOSAL package version and the decision-record element with the platform library |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the rights of each declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The asset page of `GET /assets` | S5 (`rwb_asset`) | The paginated asset list with its filters, its paging elements and the round of each listing | Read by the screens |
| The asset answer of `GET /assets/{assetId}` | S5 (`rwb_asset`) | The asset of status 200 with its title, its listing, the round number and the round price | Read by the screens; written by the application story |
| The listing elements (DF-SAL-001 to DF-SAL-008) | S5 (`rwb_asset`) | sale_channel, start_price, floor_price, round_no, listed_at, status, referenced with `LOV-SALE-CHANNEL` and `LOV-LISTING` | Written by the application story |
| The sale elements (DF-SAL-009 to DF-SAL-019) | S5 (`rwb_asset`) | id, asset_key, listing_id, contract_date, sale_date, sale_price and the fee and tax elements, as `AssetSale` | Written by the application story |
| The bids of a round | none | Not specified in the source documents for the element they occupy (GAP-2906; ASM-4804); declared only once their owner names it | Reported through the round write |
| The case elements of the consumed read | P3 (`rwb_case`) | The case reference, the case state and the stage outcome; referenced, not redefined | Consumed |
| The payment elements of the consumed row | P8 (`rwb_payment`) | The payment due date and whether the payment arrived, in place of the legacy `v_ace_payment` read | Consumed |
| The vendor-score elements of the consumed row | S9 (`rwb_partner`) | The score of the vendor whose award was cancelled, in place of the legacy `v_ace_score` read | Consumed |
| The decision-record elements | PLT library, created in `rwb_asset` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time (DF-DEC-001 to DF-DEC-018) | Written through the library |
| The rule-package elements | P7 (`rwb_decision`) | The package name, its version in force and the five rows (DF-REF-001 to DF-REF-015) | Referenced only |

The baseline declares no new table, no new column and no migration, and it enumerates no business value: every list, code and threshold is referenced with its identifier and its version. **No personal data** appears in any element, fake or example; the fixture identifiers are synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). These are the reads that answer SCR-24 and SCR-21 and the write the vendor reports a round with.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the round of each listing (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, its listing, the round number and the round price (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |
| POST | `/listings/{listingId}/rounds` | AuctionRoundRequest in — roundNo, heldOn, result, price — and `AssetSale` out at 200, the sale record the round opens; 409 when the listing is not live or the round is out of order (API-S5-005) | Asset and disposal, right U, scope applied | Idempotency-Key header |

The listings write `POST /assets/{assetId}/listings` (API-S5-004) belongs to the pricing story of FEAT-AST-11 and is not declared here; `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's and is not declared here. The round write's answer is the published `AssetSale` schema, so the sale record it opens carries the mandatory contract, sale and price elements: where a reported round has no contract or sale date yet, the value is Not specified in the source documents and the accept and award stories complete it (GAP-2911; ASM-4809).

The error envelope of the declared operations: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope asset or listing, 409 for a listing that is not live or a round that is out of order, 422 with MSG-GEN-001 for a missing field and with MSG-S5-001 for a bid or a floor under the approver's limit, and 503 when the decision library or a consumed boundary does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state the rules check before they fire; faked |
| The case-move answer (name Not specified in the source documents (GAP-2907; ASM-4805)) | rwb-case (P3) | P3 rwb-case | The answer that carries the stage outcome with its rule version; on the workflow boundary it is the outcome the parent applies; faked |
| The payment-fact activity (name Not specified in the source documents (GAP-2907; ASM-4805)) | queue `rwb-payment` | P8 rwb-payment | The payment due date and whether the payment arrived, in place of the legacy `v_ace_payment` read (DP-05); faked |
| The vendor-score activity (name Not specified in the source documents (GAP-2907; ASM-4805)) | queue `rwb-partner` | S9 rwb-partner | The score of the vendor whose award was cancelled, in place of the legacy `v_ace_score` read (DP-05); faked |

Each row is one hop or one activity, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag rather than inventing a surface (BR2).

#### 12.3 Events published

None. The owned event row of this service is EV-22 `AssetTakenOn`, published by the take-on story when the asset record opens, and the sale event is the sale stories'. This baseline declares neither as its own, adds nothing to `rwb.asset.events.v1`, and the round branch writes no outbox row: its outward surface is the case-move answer and its own reads.

#### 12.4 Events consumed

None. The round due fact, the payment-term expiry and the vendor score arrive as signals and activities of `AssetDisposalWorkflow`, so the baseline declares no topic subscription, no consumer group and no inbox row; the rwb-payment subscription of the connection matrix belongs to FEAT-AST-18's story, and a build that subscribes to a topic not listed by Architecture v5 fails the naming check (BR5, DP-14).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference, the listing reference and the rule package in force; signals: the round due fact, the reported round, the payment-term expiry and the rule package in force |
| `reportAuctionRound` | Activity, the round write | `rwb-asset` | The listing, the round and the report in; the rule IDs with their versions, the round number, the status, the sale record reference and the stage outcome out, in one transaction |

The workflow is the same execution the take-on, holding and sale stories of this service use; this baseline fixes its input and signal elements and the one activity it adds, and it declares no child workflow and no second queue. The activity name is a design choice of the application story, and the baseline carries it so that the workflow's history is stable.

#### 12.6 Schedules

None. R-DIS-36 runs "per schedule" as a durable timer inside the workflow, so the baseline declares no Temporal Schedule and no legacy Quartz job for the round. The single Schedule of the service is JOB-19, which the re-appraisal story of this service owns and which is not declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| listing | S5 (`rwb_asset`) | The listing record; the baseline declares the elements of its round and status, not its schema |
| asset_sale | S5 (`rwb_asset`) | The sale a round opens; the baseline declares the `AssetSale` answer, not its schema |
| decision_record | PLT library, created in `rwb_asset` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated report and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `valuation` (S1), `document` (P5), `deviation` (S8), the payment tables (P8), the partner tables (S9) and every `v_ace_*` view (P1) are named by their owner and never declared here. No bids table exists and none is declared (GAP-2906; ASM-4804).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state and case-move fake | The case states `ROUND_OPEN`, `BID_RECEIVED`, `SALE_AGREED` and `AWAITING_PAYMENT` of the fixture cases; the moves accepted and a move refused for an unexpected state | C3, C4, C6 |
| rwb-payment payment-fact fake | No payment by the due date; a payment received before it; a stale fact with its date; no answer inside 2 s | C4, C6 |
| rwb-partner vendor-score fake | The score of vendor `VN-2026-0012`; no answer inside 2 s | C4, C6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with the five rules | C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-24 and SCR-21 answer for case `RC-2026-000541`, with the round and its price read once | C2, C6 |
| Round report fake | A report at or above the floor, one below it, one out of order and one repeated on the same key | C2, C3, C5 |
| Sale answer fake | The `AssetSale` answer with its mandatory dates and price, and one with those values absent | C2, C3 |

Each fake answers only what its owner documents, and a fake that answers more than the document fails the review. The names that are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2907; ASM-4805).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | The two asset reads and the round write on `/api/recovery/asset/v1`; the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The round and payment facts are workflow signals; nothing is published |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and `reportAuctionRound` on `rwb-asset`; the consumed payment and vendor-score activities on their owners' queues; no Schedule |
| File | None | No file element is declared; the publication of the listing is FEAT-AST-12's |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4024 CON Run auction rounds and report bids - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S5-E4024.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operations, the consumed rows, the published and consumed events, the workflow and its activity, the schedules, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Open shapes carried into the tag.** Three shapes are carried as placeholders and not invented: the bids of a round (GAP-2906; ASM-4804), the names of the four consumed rows (GAP-2907; ASM-4805) and the sale elements a reported round leaves open (GAP-2911; ASM-4809). A placeholder is a declared forthcoming shape, not a permission to guess.

**Done when.** The seven criteria pass, the reviewers of the three consumed owners have closed their comments, the compatibility check passes on the tag, the fakes are published with their documented answers, and RWB-S5-E4024-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Asset and disposal right calls one of the declared operations | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of a declared request is absent or invalid | Enter {field}. |
| MSG-S5-001 | A declared write carries a bid or a floor under the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | A declared read carries an appraisal more than a year old | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published name | Not specified in the source documents (GAP-2907; ASM-4805). |

The five message IDs are carried from the service and platform sets and are declared only as the envelope rows of the operations in this baseline; the two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-24 Auction rounds and SCR-21 Asset list through the gateway-bff composite route (DP-19). What this story fixes is the element list of the declared responses and the empty, loading, refused, conflict, out-of-order, stale-payment and unanswered-score states the route can show from this service's answers. The route itself, its merge order and its field list are RWB-PLT-N001-CON, and the screens' transitions are the application story's.

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-024-01 | C2: the round elements and the sale answer the declared write carries | Contract | The published schema and a recorded round report of listing `LS-2026-000541` |
| TC-E4-024-02 | C6: the decision-record and rule-package elements | Contract | The element list, the five rules, the stopped stub and a package declared with a rule table |
| TC-E4-024-03 | C5: the error envelope and the not-recorded path | Contract | One request per error code, 400, 401, 403, 404, 409, 422 and 503, and a stopped record chain |
| TC-E4-024-04 | C3: the provided operations, their rights and their idempotency | Contract | One request per operation and per right, including a role without it and a round out of order |
| TC-E4-024-05 | C4: the consumed rows of rwb-case, rwb-payment and rwb-partner | Contract | The four consumed rows, each with and without a published name |
| TC-S5-E4024-CON-01 | C2: the bids placeholder | Contract | The element list with and without a named element for the bids |
| TC-S5-E4024-CON-02 | C6: the fakes and their documented answers | Contract | The eight fakes, the stopped stub and one fake that answers more than its document |
| TC-S5-E4024-CON-03 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |
| TC-S5-E4024-CON-04 | C7, BR5: no event published and none consumed | Contract | The outbox declaration, empty, and the absent subscription row |

The five legacy case IDs are mapped onto this contract deliverable in their legacy order, and their `Covers` names the criterion of this story that fixes the surface each legacy case touches: the round answer and the sale it opens (01), the rule and the record (02), the failure and error path (03), the operations and rights (04) and the consumed rows (05). The four `TC-S5-E4024-CON-` cases are new and test the parts of the baseline that no legacy case touches: the bids placeholder, the fakes, the compatibility check and the absence of an event. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the baseline: the price schedule, the floor, the re-list limit, the codes and every threshold are referenced with their identifier and version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates, a vendor code and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the payment and vendor facts appear only as the P8 and S9 rows (DP-05).
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case` element and no rule row is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Schedule for the round timer, no event published or consumed by this branch.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id for this slice; the requirement the baseline serves is FEAT-AST-15 of FSD S5 A2.15, that the vendor runs each round and the bids come back into the case (GAP-2909; ASM-4807) | The baseline, its consumed rows and its fakes | TC-S5-E4024-CON-01, TC-E4-024-03 |
| ADR-013 | 19 services inside ACE | The baseline's ownership rows | TC-E4-024-05 |
| ADR-014 | Schema and login per service | `rwb_asset` and the declared tables | TC-E4-024-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows and the compatibility check | TC-E4-024-03, TC-S5-E4024-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its library | TC-S5-E4024-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-024, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 are carried by RWB-S5-E4024-APP; this story carries no legacy criterion and tests the surface they touch |
| Test cases | TC-E4-024-01 to TC-E4-024-05 at Level Contract, and TC-S5-E4024-CON-01 to TC-S5-E4024-CON-04 |
| Feature and screens | FEAT-AST-15, SCR-24 Auction rounds and SCR-21 Asset list, read through the composite route |
| Rules | R-DIS-36, R-DIS-37, R-DIS-40, R-DIS-49 and R-DIS-50, referenced as rule-package rows and not evaluated here |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The round behaviour, the rule evaluation, the round write, the decision records and the case moves: RWB-S5-E4024-APP.
- The start price and the floor and the approval of the floor: the pricing story of FEAT-AST-11.
- The publication of the listing to HOME.SCB, the EASY app and the auction portal: FEAT-AST-12.
- The step down on a round with no bid and the re-list: FEAT-AST-13 and FEAT-AST-17's stories.
- The second signature of a bid below the floor: FEAT-AST-16's story.
- The five-day payment term and the title transfer: FEAT-AST-18 to FEAT-AST-20's stories (GAP-2908).
- The payment, its matching and its posting: rwb-payment (P8).
- The vendor panel and the scorecard: rwb-partner (S9).
- The case of record, its states and the parent workflow: rwb-case (P3).
- The rule package, its version and its approval: rwb-decision (P7) (GAP-2910).
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The composite route, its merge order and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
