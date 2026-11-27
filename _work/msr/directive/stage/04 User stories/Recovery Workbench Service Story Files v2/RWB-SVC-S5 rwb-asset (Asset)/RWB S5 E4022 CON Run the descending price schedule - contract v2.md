# RWB-S5-E4022-CON Run the descending price schedule - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4022-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S5-E4022-CON-16) |
| Contract version | v1 (base /api/recovery/asset/v1) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | Pending (C1); traced to FEAT-AST-13 of FSD S5 A2.13 and BR-027 of the epic BRD until the PRD allocates requirement IDs |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-022, the baseline the price-ladder step of rwb-asset builds against on Day 1. The baseline declares the asset and listing reads and the listings write that answer SCR-23 Listing and price and SCR-21 Asset list on `/api/recovery/asset/v1` (DP-13), the three consumed rows of rwb-source-data and rwb-case (DP-05), the decision-record element of DP-03, the rule-package element the step evaluates against, the rights and the error envelope, and the fakes. The step publishes no event and consumes none, because the owned event of the service is EV-22 `AssetTakenOn` and the round-close fact is a workflow signal. No source publishes the operation names of the consumed rows (GAP-2895; ASM-4792); `listing` names no column for the per-round price (GAP-2896; ASM-4793); API-S5-004 serves both the pricing story and this step (GAP-2897; ASM-4794); the split plan carries no requirement id for this slice (GAP-2898; ASM-4795); and the rule package is declared without the DP-04 platform row (GAP-2899; ASM-4796). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E4022-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 10 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the price-ladder step of rwb-asset — its asset and listing reads, its listings write, its consumed rows, its decision-record and rule-package elements, its rights, its error envelope and its fakes — baselined and tagged before the build starts**, so that **the application story, the rounds story and every consumer can build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-022. It owns:

- the document that fixes the asset and listing reads and the listings write on base `/api/recovery/asset/v1`, with their parameters, their documented answer, their rights and their idempotency (DP-13);
- the three consumed rows: the rwb-source-data appraisal and asset data product, the rwb-case case state read and the rwb-case case-move answer, each with its owner, its use and its placeholder where the operation name is not published (DP-05);
- the decision-record element and the local library dependency that carries it (DP-03);
- the rule-package element: the DISPOSAL package, its version and the rows this step evaluates, declared as a reference and not as a rule table of this service;
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, so that every downstream answer has a stub on Day 1;
- the naming and boundary rules of the baseline: one base, one topic, one queue, no foreign schema, no monolith base, no Schedule for a workflow timer.

It does not own: the ladder behaviour, the rule evaluation, the listing write, the decision records and the case moves, which are RWB-S5-E4022-APP; the setting of the start price and the floor and its approval, which is FEAT-AST-11's story; the listing publication, which is FEAT-AST-12's; the rounds and the bids, which are the rounds story's; the appraisal and NPA asset facts, which are rwb-source-data's (P1); the case of record and its route states, which are rwb-case's (P3); the rule package, which is rwb-decision's (P7); the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

INVEST Small: the contract slice fits one iteration; the iteration length is Not specified in the source documents (DOR-RWB-S5-E4022-CON-15).

### 2. Business rationale

A contract baseline is what lets the stories of one wave build at once. Without it the ladder step would be written against whatever shape the asset read happened to expose that week, and the first integration would find the mismatches instead of the review. With it, the application story builds on Day 1 against a tagged document and its fakes, the rounds and publication stories know what the listing must carry for the ladder to step it, and the consumers of the asset reads know exactly which elements they can rely on.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner and its use, and where the source documents do not publish an operation name the row carries the placeholder rather than an invented path (GAP-2895; ASM-4792).
- **one hop, one budget.** Every consumed row is a single hop with a 2 s timeout, a breaker and no chain, which is ADR-020 and is what the application story's exception paths assume.
- **additive only.** The baseline moves forward without breaking: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version and a new document (C1).

The business outcome the baseline protects is the one FEAT-AST-13 of the FSD names: the price stepping down the ladder until a bid clears the floor. The baseline does not state that outcome, and no criterion here asserts a business value.

### 3. Preconditions

- The Ownership Map rows are in force: S5 owns `GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds`; `POST /assets/{assetId}/valuations` is S1's under ASM-0043 and the business-key paths come from ASM-0052; `asset_sale` and `listing` are S5's tables.
- The service naming is fixed: schema `rwb_asset`, login `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with `.retry` and `.dlt`, task queue `rwb-asset` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.asset`.
- The owned event row of the service is EV-22 `AssetTakenOn` (TSD S5 T5.3), and the assets of the baseline touch none of the events of the service: the round-close fact is a signal of `AssetDisposalWorkflow`.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). DP-04 is not in the pattern set of this slice, so no platform row for the rules kit is claimed and the package is referenced as rwb-decision's (GAP-2899; ASM-4796).
- No approval is needed to publish a Draft baseline; the document is baselined by this story's own review, and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map, the TSD S5 T-A.1 operations, the TSD S5 T3.1 tables and the lists of T3.2.
2. Every operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the operation name is not published.
4. The decision-record element is declared with the library dependency that carries it, and the rule-package element with its owner and its version.
5. The fakes are declared with their documented answers, one per consumed row and one for the composite route.
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
| X7 | Two documents claim the same path or queue, or a document claims the per-round price column that the sources do not name | The naming rule and the placeholder rule resolve it: the owner in the Ownership Map keeps the path, and the column stays Not specified in the source documents | C2, C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 are the paths of a baseline moving under a build, and X7 is the naming and placeholder boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the order of the sections and the fake data are this story's choice; the paths, the owners, the base, the error set and the element names are fixed by their sources |
| Valuable | The stories of wave 3 build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, five provided operations, three consumed rows, two library elements, seven fakes and one compatibility check |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the price-ladder step
  # Acceptance criteria C1 to C18 are the AC IDs of this section

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
    And the per-round price carries the placeholder and its gap identifier because listing names no column for it

  Scenario: C3 The provided reads and the listings write are declared with their rights (new, D-RCV-60)
    Given the operations the baseline provides on base /api/recovery/asset/v1
    When the method, path, documented answer, right and idempotency of each are read
    Then the three asset reads carry the Asset and disposal right R with scope applied and no idempotency
    And the two listings writes carry the right C with the Idempotency-Key header and the 409 conflict
    And POST /listings/{listingId}/rounds is named as the rounds story's and is not declared here

  Scenario: C4 The consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-source-data and rwb-case are read
    Then each row names its owner, its use and its 2 s budget
    And where the operation name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C5 The error envelope is declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the error set and the rights of each operation are read
    Then the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 or MSG-S5-001 and 503 in one problem envelope
    And the capability area and the right of each operation are the rows of the access matrix

  Scenario: C6 The decision-record, rule-package and fake elements are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the rule-package element and the fake table are read
    Then the decision-record element names RWB-PLT-E1027-CON as its library and the transaction it joins
    And the rule-package element names the DISPOSAL package, its owner and its version in force and declares no rule row
    And every consumed row has a fake with a documented answer, including the stopped decision-record stub and the floor case

  Scenario: C7 The naming and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue and the schema of the baseline
    When the document is checked against the naming rule and the ownership map
    Then the base /api/recovery/asset/v1, the queue rwb-asset and the topic rwb.asset.events.v1 are the only ones declared as this service's own
    And no foreign schema, no foreign topic, no monolith base /api/recovery/v1 and no Schedule for the ladder timer is declared
    And no event is published or consumed by the step
```

The eighteen criteria C1 to C18 are new to this run and are tagged as such: they test the contract deliverable only — the schema, the elements, the lists, the operations, the consumed rows, the rights, the envelope, the two library elements, the fakes and the boundary. No criterion states a business outcome or a business value of the application story, and none asserts that a rule fires, that a price steps or that a case moves.

Scenario: C8 Every owned operation, event and table is declared once for S5, and no other service's table, operation or topic is declared as its own (new, D-RCV-60)

Scenario: C9 A consumed row with no published operation name carries the placeholder and its gap, and never an invented path (new, D-RCV-60)

Scenario: C10 A new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version (new, D-RCV-60)

Scenario: C11 Every consumed row is one hop with a 2 s timeout, a breaker and no chain (new, D-RCV-60)

Scenario: C12 The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change (new, D-RCV-60)

Scenario: C13 The rule package is referenced and never redefined, and no rule table of this service is declared (new, D-RCV-60)

Scenario: C14 No business value is declared; the ladder, the floor rule, the codes and the thresholds are referenced with their identifier and version (new, D-RCV-60)

Scenario: C15 No personal data appears in any element, fake or example of the baseline (new, D-RCV-60)

Scenario: C16 Every business rule of section 8 has a criterion and a test case, and an architecture rule may use a boundary test (new, D-RCV-60)

Scenario: C17 A consumed call that times out is stopped at its 2 s budget and answered with the error of C5; the retry count is Not specified in the source documents (NEWAC-RWB-S5-E4022-CON-AC6) (new, D-RCV-60)

Scenario: C18 A status change the allowed transitions do not list is refused with an error of C5 and the status stays unchanged; the transition list is Not specified in the source documents (NEWAC-RWB-S5-E4022-CON-AC7) (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, event and table: the baseline declares only the rows the Ownership Map gives to S5, and names every other row with its owner | Ownership Map; Architecture v5 slide 41 |
| BR2 | A consumed row with no published operation name carries the placeholder and its gap, and never an invented path | Template and Rules v1 §R9; GAP-2895 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; C1 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain | ADR-020 |
| BR5 | No event is published and none is consumed by the step: the owned event is EV-22 `AssetTakenOn`, the take-on story's, and the round-close fact is a workflow signal | TSD S5 T5.3; GAP-2898 |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR7 | The rule package is referenced, never redefined: the DISPOSAL package, its version and the two rules are rwb-decision's rows and no rule table of this service is declared | DP-04 (not claimed); GAP-2899 |
| BR8 | No business value is declared in the baseline: the ladder, the floor rule, the outlier test, the codes and the thresholds are referenced with their identifier and version | Template and Rules v1 §R7.2 (s16); legacy Guardrails |
| BR9 | No personal data in any element, fake or example of the baseline | Template and Rules v1 §R7.2 (s17) |
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
| Owner of rwb-source-data (P1) | Reviews the appraisal and asset data-product row and its freshness stamp |
| Owner of rwb-case (P3) | Reviews the case state and case-move rows and publishes the operation names when they exist |
| Owner of rwb-decision (P7) | Reviews the rule-package element, the DISPOSAL package version and the decision-record element with the platform library |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the rights of each declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

Every declared operation's rights are checked through the rwb-access authorise check (DP-08) before the operation runs.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write | BR Field ID |
|---|---|---|---|---|
| The asset answer of `GET /assets/{assetId}` and of `GET /assets/{assetKey}` | S5 (`rwb_asset`) | The asset of status 200 with its title, its listing, the price of the round, the floor and the round number | Read by the screens; written by the application story | Not specified in the source documents (DOR-RWB-S5-E4022-CON-7) |
| The asset page of `GET /assets` | S5 (`rwb_asset`) | The paginated asset list with its filters and its paging elements | Read by the screens | Not specified in the source documents (DOR-RWB-S5-E4022-CON-7) |
| The listing elements of `listing` (DF-SAL-001 to DF-SAL-008) | S5 (`rwb_asset`) | sale_channel, start_price, floor_price, round_no, listed_at, status, referenced with `LOV-SALE-CHANNEL` and `LOV-LISTING` | Written by the application story | Not specified in the source documents (DOR-RWB-S5-E4022-CON-7) |
| The per-round price element | S5 (`rwb_asset`) | Not specified in the source documents (GAP-2896; ASM-4793); declared only once its owner names the column | Written by the application story where a column is named | Not specified in the source documents (DOR-RWB-S5-E4022-CON-7) |
| The appraisal elements of the consumed read | P1 (`rwb_source_data`) | The appraised value, the appraisal date, the outlier flag and the book value; referenced, not redefined | Consumed | Not specified in the source documents (DOR-RWB-S5-E4022-CON-7) |
| The case elements of the consumed read | P3 (`rwb_case`) | The case reference, the case state and the stage outcome; referenced, not redefined | Consumed | Not specified in the source documents (DOR-RWB-S5-E4022-CON-7) |
| The decision-record elements | PLT library, created in `rwb_asset` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time (DF-DEC-001 to DF-DEC-018) | Written through the library | Not specified in the source documents (DOR-RWB-S5-E4022-CON-7) |
| The rule-package elements | P7 (`rwb_decision`) | The package name, its version in force and the rows R-DIS-38 and R-DIS-17 (DF-REF-001 to DF-REF-015) | Referenced only | Not specified in the source documents (DOR-RWB-S5-E4022-CON-7) |

The baseline declares no new table, no new column and no migration, and it enumerates no business value: every list, code and threshold is referenced with its identifier and its version. **No personal data** appears in any element, fake or example; the fixture identifiers are synthetic.

Screen states of SCR-21 Asset list and SCR-23 Listing and price: the states the screen specification v1 does not give are Not specified in the source documents (CG-ALL-9990; CG-ALL-9991); section 15 states them.

Reference data: the lists and parameters the reads use are read through the reference-data contract (DP-06) and named by their identifier in the parameter catalogue (DP-07); the baseline declares no parameter value.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). These are the reads that answer SCR-23 and SCR-21 and the write the ladder steps the price with.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, its listing, the price of the round, the floor and the round number (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetKey}` | Asset of status 200 out on the business key of the Ownership Map | Asset and disposal, right R, scope applied | Not applicable |
| POST | `/assets/{assetId}/listings` | ListingRequest in, the listing and its round out, 409 when the listing is not in the state the write expects (API-S5-004) | Asset and disposal, right C, scope applied | Idempotency-Key header |
| POST | `/assets/{assetKey}/listings` | The same write on the business key of the Ownership Map | Asset and disposal, right C, scope applied | Idempotency-Key header |

The listings write is declared once for two stories: the pricing story of FEAT-AST-11 sets the start price and the floor and takes the approval, and the application story of this key steps the price at each round. No source splits the operation, and the split is recorded as GAP-2897 with ASM-4794. `POST /listings/{listingId}/rounds` (API-S5-005) is the rounds story's and is not declared here; `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's under ASM-0043.

The error envelope of the declared operations: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope asset, 409 for a listing that is not in the state the write expects, 422 with MSG-GEN-001 for a missing field and with MSG-S5-001 for a floor under the approver's limit, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The appraisal and asset data product (operation name Not specified in the source documents (GAP-2895; ASM-4792)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The appraised value, the appraisal date, the outlier flag and the book value, with the freshness stamp; the asset, collateral and score fields carried by their FSD names (v_ace_npa_asset.asset_key, asset_ref, asset_code, transfer_in_type, from_segment, transfer_in_date; v_ace_collateral.asset_key; v_ace_asset.asset_type; v_ace_score) as the source field names the contract returns; read only through this row, with no direct ACE view read; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state the rules check before they fire; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2895; ASM-4792)) | rwb-case (P3) | P3 rwb-case | The answer that carries the stage outcome with its rule version; on the workflow boundary it is the outcome the parent applies; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag rather than inventing a surface (BR2).

#### 12.3 Events published

None. The owned event row of this service is EV-22 `AssetTakenOn`, published by the take-on story when the asset record opens, and the sale event is the sale story's. This baseline declares neither as its own, adds nothing to `rwb.asset.events.v1`, and the step writes no outbox row: its outward surface is the case-move answer and its own reads.

#### 12.4 Events consumed

None. The round-close fact and the accepted appraisal arrive as signals of `AssetDisposalWorkflow`, so the baseline declares no topic subscription, no consumer group and no inbox row, and a build that subscribes to a topic not listed by Architecture v5 fails the naming check (BR5, DP-14).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new | `rwb-asset` | Input: the case, the route, the asset reference, the listing reference and the rule package in force; signals: the round-close fact, the accepted re-appraisal and the rule package in force |
| `stepDownPrice` | Activity, the price-ladder step | `rwb-asset` | The case, the listing and the round-close or appraisal fact in; the rule IDs with their versions, the price before and after, the round number and the stage outcome out, in one transaction |

The workflow is the same execution the take-on, holding and sale stories of this service use; this baseline fixes its input and signal elements and the one activity it adds, and it declares no child workflow and no second queue. The activity name is a design choice of the application story, and the baseline carries it so that the workflow's history is stable.

Workflow ID form: Not specified in the source documents (CG-ALL-9987). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-9987).

#### 12.6 Schedules

None. R-DIS-38 runs "per schedule" as a durable timer inside the workflow, so the baseline declares no Temporal Schedule and no legacy Quartz job for the ladder. The single Schedule of the service is JOB-19, which the re-appraisal story of this service owns and which is not declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| listing | S5 (`rwb_asset`) | The listing record; the baseline declares the elements of its price and round, not its schema |
| asset | S5 (`rwb_asset`) | Read only; the baseline declares the elements the screens read |
| decision_record | PLT library, created in `rwb_asset` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated signal or request and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `asset_sale` (S5, the sale story's), `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `valuation` (S1), `document` (P5), `deviation` (S8) and every `v_ace_*` view (P1) are named by their owner and never declared here. The per-round price column is Not specified in the source documents and is declared only once its owner names it (GAP-2896; ASM-4793).

The auction round, the bid, the award, the holding-cost movement and the work order are entity groups of this service (S5, `rwb_asset`), named here without their physical table names; each needs its Ownership Map row added by the data architect (GAP-1752).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data appraisal and asset fake | The appraisal `AP-2026-000531` of asset `AST-2026-000531` with its value, its date and a clear outlier flag, and the NPA asset with its book value; an appraisal more than a year old; a stale product with its date; no answer beyond 2 s | C4, C6 |
| rwb-case case-state and case-move fake | The case states `ROUND_OPEN` and `REAPPRAISAL_RECEIVED` of the fixture cases; the moves accepted and a move refused for a state the rule does not expect | C4, C6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-38 and R-DIS-17 | C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-23 and SCR-21 answer for case `RC-2026-000531`, with the listing and price elements read once | C2, C6 |
| Floor and ladder data fake | A listing whose price of the round is above the floor, one at the floor and one below the approver's limit (MSG-S5-001) | C2, C5, C6 |

Each fake answers only what its owner documents, and a fake that answers more than the document fails the review. The operation names that are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2895; ASM-4792).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 2 consumed | The asset reads and the listings write on `/api/recovery/asset/v1`; the rwb-source-data data-product row and the rwb-case state and case-move rows; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The round-close fact is a workflow signal; nothing is published |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and `stepDownPrice` on `rwb-asset`; no Schedule |
| File | None | No file element is declared; the portal and HOME.SCB publication is FEAT-AST-12's |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4022 CON Run the descending price schedule - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S5-E4022.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operations, the consumed rows, the published and consumed events, the workflow and its activity, the schedules, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Open shapes carried into the tag.** Three shapes are carried as placeholders and not invented: the operation names of the rwb-source-data product and of the case-move answer (GAP-2895; ASM-4792), the per-round price column (GAP-2896; ASM-4793) and the ownership of the listings write across the two stories (GAP-2897; ASM-4794). A placeholder is a declared forthcoming shape, not a permission to guess.

**Done when.** The seven criteria pass, the reviewers of the three consumed owners have closed their comments, the compatibility check passes on the tag, the fakes are published with their documented answers, and RWB-S5-E4022-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Asset and disposal right calls one of the declared operations | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of a declared request is absent or invalid | Enter {field}. |
| MSG-S5-001 | A declared write carries a floor under the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | A declared read carries an appraisal more than a year old | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published operation name | Not specified in the source documents (GAP-2895; ASM-4792). |

The five message IDs are carried from the service and platform sets and are declared only as the envelope rows of the operations in this baseline; the two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-23 Listing and price and SCR-21 Asset list through the gateway-bff composite route (DP-19). What this story fixes is the element list of the declared responses and the empty, loading, refused, conflict, at-floor and stale states the route can show from this service's answers. The route itself, its merge order and its field list are RWB-PLT-N001-CON, and the screens' transitions are the application and pricing stories'.

SCR-21 Asset list: the screen specification v1 gives no empty, error or no access state, so those states are Not specified in the source documents (CG-ALL-9990). SCR-23 Listing and price: the screen specification v1 gives no empty, loading, error or no access state, so those states are Not specified in the source documents (CG-ALL-9991).

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-022-01 | C2: the elements and the closed lists the declared answers carry | Contract | The published schema and a recorded asset answer of case `RC-2026-000531` |
| TC-E4-022-02 | C3, C5: the provided operations, their rights and their error set | Contract | One request per operation and per right, including a role without it and a 409 conflict |
| TC-E4-022-03 | C4: the consumed rows of rwb-source-data and rwb-case | Contract | The three consumed rows, each with and without a published operation name |
| TC-E4-022-04 | C5: the error envelope of the declared operations | Contract | One request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-022-05 | C7: the naming and the boundary rule | Contract | The base, the topic, the queue and the schema, plus a draft that names a foreign schema, a monolith base or a Schedule |
| TC-E4-022-06 | C6: the decision-record and rule-package elements | Contract | The element list, the stopped stub and a package declared with a rule table |
| TC-S5-E4022-CON-01 | C2: the per-round price placeholder | Contract | The element list with and without a named column |
| TC-S5-E4022-CON-02 | C6: the fakes and their documented answers | Contract | The six fakes, the stopped stub and one fake that answers more than its document |
| TC-S5-E4022-CON-03 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |
| TC-S5-E4022-CON-04 | C7, BR5: no event published and none consumed | Contract | The outbox declaration, empty, and the absent subscription row |
| TC-S5-E4022-CON-05 | C2, §12.7: the boundary of the owned tables | Contract | The owned table rows, the read-only asset row, and a draft that declares a column of another owner |
| TC-S5-E4022-CON-06 | C8, BR1, BR10: one owner per row, no other service's row declared | Contract | The Ownership Map rows of S5, and a draft that declares another service's table, operation or topic |
| TC-S5-E4022-CON-07 | C9, BR2: the placeholder for a consumed row | Contract | A consumed row with no published operation name, and one with a name |
| TC-S5-E4022-CON-08 | C10, BR3: the versioning rule | Contract | An optional element added, and a removal and a new required element drafted |
| TC-S5-E4022-CON-09 | C11, BR4: the one-hop rule | Contract | A consumed row call with a 2 s timeout and a breaker, and a draft that chains a second call |
| TC-S5-E4022-CON-10 | C12, BR6: the decision record in the caller's transaction | Contract | A declared change with the decision record written first, and one with it written after |
| TC-S5-E4022-CON-11 | C13, BR7: the rule package is referenced | Contract | The DISPOSAL package reference, and a draft that declares a rule table |
| TC-S5-E4022-CON-12 | C14, BR8: no business value declared | Contract | The element list with identifiers and versions, and a draft that declares a threshold value |
| TC-S5-E4022-CON-13 | C15, BR9: no personal data | Contract | The fixtures and examples, and a draft that carries a personal data value |
| TC-S5-E4022-CON-14 | C16: each section 8 rule has a criterion and a test | Contract | The business rules of section 8 and the criteria list, with one rule drafted that has no criterion |
| TC-S5-E4022-CON-15 | C17: a consumed call that times out | Contract | A consumed row call that exceeds its 2 s budget, and a call that fails and is retried |
| TC-S5-E4022-CON-16 | C18: a disallowed status change is refused | Contract | A status change the allowed transitions list, and one they do not list, each sent to the operation that changes status |

The six legacy case IDs are mapped onto this contract deliverable in their legacy order, and their `Covers` names the criterion of this story that fixes the surface each legacy case touches: the answers the step returns (01), the operations and rights (02), the consumed rows (03), the failure and error path (04), the naming boundary (05) and the decision-record element (06). The sixteen `TC-S5-E4022-CON-` cases are new and test the parts of the baseline that no legacy case touches: the per-round price placeholder, the fakes, the compatibility check, the absence of an event, the boundary of the owned tables, the ownership, placeholder, versioning, one-hop, decision-record, rule-package, business-value and personal-data rules, the section 8 rule coverage, the consumed-call timeout and the disallowed status change. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the baseline: the ladder, the floor rule, the outlier test, the codes and every threshold are referenced with their identifier and version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the appraisal and asset facts appear only as the rwb-source-data data product (DP-05).
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case` element and no rule row is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Schedule for the ladder, no event published or consumed by this step.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id for this slice; the requirement the baseline serves is FEAT-AST-13 of the FSD S5 A2.13 and BR-027 of the epic BRD, that a round with no bid re-lists at the next step of the ladder (GAP-2898; ASM-4795) | The baseline, its consumed rows and its fakes | TC-S5-E4022-CON-01, TC-E4-022-03 |
| ADR-013 | 19 services inside ACE | The baseline's ownership rows | TC-E4-022-05 |
| ADR-014 | Schema and login per service | `rwb_asset` and the declared tables | TC-E4-022-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows and the compatibility check | TC-E4-022-03, TC-S5-E4022-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its library | TC-E4-022-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-022, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 are carried by RWB-S5-E4022-APP; this story carries no legacy criterion and tests the surface they touch |
| Test cases | TC-E4-022-01 to TC-E4-022-06 at Level Contract, and TC-S5-E4022-CON-01 to TC-S5-E4022-CON-04 |
| Feature and screens | FEAT-AST-13, SCR-23 Listing and price and SCR-21 Asset list, read through the composite route |
| Rules | R-DIS-38 and R-DIS-17, referenced as rule-package rows and not evaluated here |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The ladder behaviour, the rule evaluation, the listing write, the decision records and the case moves: RWB-S5-E4022-APP.
- The setting of the start price and the floor and the approval of the floor: the pricing story of FEAT-AST-11.
- The publication of the listing to HOME.SCB, the EASY app and the auction portal: FEAT-AST-12.
- The rounds, the bids and the award, and API-S5-005: the rounds story of legacy key RWB-E4-024.
- The appraisal order and the valuer's report: rwb-valuation (S1) and the re-appraisal story of this service.
- The appraisal and asset facts and the freshness stamp: rwb-source-data (P1).
- The case of record, its route states and the parent workflow: rwb-case (P3).
- The rule package, its version and its approval: rwb-decision (P7) (GAP-2899).
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The composite route, its merge order and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
