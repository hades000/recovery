# RWB-S5-E4029-CON Record a property transfer at the Land Office - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4029-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-029 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-029, the baseline the title-transfer branch of rwb-asset builds against on Day 1. It declares the two asset reads that answer SCR-21 and SCR-22 on `/api/recovery/asset/v1` (DP-13), the status elements of `listing` and `asset`, the three consumed rows of rwb-case and rwb-document (DP-05), the decision-record element of DP-03, the rule-package element the branch evaluates against, the rights and the error envelope, and the fakes. No event is published and none is consumed: the owned event of the service is EV-22 `AssetTakenOn`, the take-on story's. No operation publishes the officer's registration, so the baseline declares the signal instead of an invented path (GAP-2937; ASM-4833); no element holds the title status or the Land Office reference (GAP-2938; ASM-4834); the document custody release has no published name and the C row of the plan is empty (GAP-2939; ASM-4835); AC3 of the application slice names R-DIS-02, which RWB-S5-E3020-APP builds (GAP-2940; ASM-4836); R-DIS-53 has no owner (GAP-2941; ASM-4837); the plan carries no requirement id (GAP-2942; ASM-4838); the sources are in review (GAP-2943; ASM-4839). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4029-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the Land Office transfer capability of rwb-asset — its asset reads, its status elements, its consumed rows, its decision-record and rule-package elements, its rights, its error envelope and its fakes — baselined and tagged before the build starts**, so that **the application story and every consumer of an asset's sold state can build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-029. It owns:

- the document that fixes the two asset reads on base `/api/recovery/asset/v1`, with their parameters, their documented answer, their rights and their idempotency (DP-13);
- the status elements the branch writes, `listing.status` and `asset.holding_status`, declared against `LOV-LISTING` and `LOV-HOLDING` and never enumerated in code;
- the three consumed rows: the rwb-case case state read, the rwb-case case-move answer and the rwb-document custody release, each with its owner, its use and its placeholder where the name is not published (DP-05, GAP-2939);
- the decision-record element and the local library dependency that carries it (DP-03);
- the rule-package element: the DISPOSAL package, its version and the two rows this branch evaluates with the remaining rows named as other stories' (GAP-2940);
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, so that every downstream answer has a stub on Day 1;
- the naming and boundary rules of the baseline: one base, one topic, one queue, one schema, no foreign base, no monolith base, no Schedule for a workflow timer, no interface to the Land Office (GAP-2937).

It does not own: the transfer behaviour, the rule evaluation, the release call, the status writes, the decision records and the case moves, which are RWB-S5-E4029-APP; the payment term and the award, FEAT-AST-18's story; the vehicle registration, FEAT-AST-19's story; the property take-on, RWB-S5-E3020-APP; the documents and their custody, rwb-document's (P5); the case of record and its states, rwb-case's (P3); the rule rows and the package version, rwb-decision's (P7); the proceeds, rwb-payment's (P8); the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

### 2. Business rationale

A contract baseline is what lets the stories of one wave build at once. Without it the application story would write the sold state against whatever shape the document hub happened to answer that week, and the first integration would find the mismatches instead of the review. With it, the application story builds on Day 1 against a tagged document and its fakes, the payment, vehicle and proceeds stories know what the sold state and the listing must carry, and the consumers of the asset reads know exactly which elements they can rely on.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner and its use, and where the source documents do not publish a name the row carries the placeholder rather than an invented path (GAP-2939; ASM-4835).
- **one hop, one budget.** Every consumed row is a single hop with a 2 s timeout, a breaker and no chain, which is ADR-020 and is what the application story's exception paths assume.
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document (C1).

The business outcome the baseline protects is the one FEAT-AST-20 of the FSD names: the Land Office transfer is tracked and stays a person and officer step. The baseline does not state that outcome, and no criterion here asserts a business value or a title registration.

### 3. Preconditions

- The Ownership Map rows are in force: S5 owns `GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds`; `asset_sale` and `listing` are S5's tables, and `asset` is read as S5 from TSD S5 T3.1 while the map names no row for it (GAP-2938; ASM-4834).
- The service naming is fixed: schema `rwb_asset`, login `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with `.retry` and `.dlt`, task queue `rwb-asset` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.asset`.
- The published shapes of the declared operations are the API Specification v5: `AssetPage` and `Asset` (API-S5-001, API-S5-002).
- The owned event row of the service is EV-22 `AssetTakenOn` (TSD S5 T5.3); the title branch touches no event of the service.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19).
- The lists `LOV-HOLDING`, `LOV-LISTING`, `LOV-ASSET-TYPE` and `LOV-SALE-CHANNEL` are reference data with their version (TSD S5 T3.2), referenced and never enumerated.
- The sources of the slice are In review with empty sign-off tables; a Draft baseline is published without approval and the build waits only for its tag (GAP-2943; ASM-4839).

### 4. Flow

1. The author drafts the baseline from the Ownership Map, the TSD S5 T-A.1 operations, the TSD S5 T3.1 elements and the lists of T3.2.
2. Every operation is declared with its method, path, documented answer, rights, idempotency and error set; the registration itself is declared as a workflow signal because no source gives it an operation (GAP-2937; ASM-4833).
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The decision-record element is declared with the library dependency that carries it, and the rule-package element with its owner, its version and the rows this branch evaluates.
5. The fakes are declared with their documented answers, one per consumed row, one for the composite route and one for the registration signal.
6. The schema, the open lists and the closed lists are published, and the compatibility check runs: a breaking change fails the check.
7. The document goes to review as Draft; the reviewers are the owners of the consumed rows and the tech lead of the service.
8. On the review's close the document is tagged and baselined; the application story starts against the tag and the fakes.
9. A defect found in the build that needs a shape change is raised against this document, and the document moves to a new minor or major version; the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and the gap; no path is invented and no field is guessed | C2, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails, the version becomes a new major and the document is re-reviewed | C1 |
| X3 | A declared surface reaches another service's data, base or queue | The review refuses the baseline and the boundary test fails the build | C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged; the application story cannot start | C6 |
| X5 | The rights of an operation are not one of the rows of the access matrix | The operation is not declared and the error set of the operation is incomplete | C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a new version, this document follows with a minor or major version, and the application story re-tests against the new fake | X2 |
| X7 | A draft declares a Land Office interface, a title column or an event for the transfer | The baseline is refused: no source names an interface, a column or an event for this step | C2, C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 are the paths of a baseline moving under a build, and X7 is the boundary this slice must not cross.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the order of the sections and the fake data are this story's choice; the paths, the owners, the base, the error set and the element names are fixed by their sources |
| Valuable | The stories of wave 3 build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, two provided operations, three consumed rows, two library elements, seven fakes and one compatibility check |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the Land Office transfer capability

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema and the open and closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The elements, the status elements and the closed lists are published as declared (new, D-RCV-60)
    Given the baseline document of this story
    When the element list, the required and optional flags and the closed lists are read
    Then every element carries its type, its nullability and its source
    And listing status and asset holding status are declared against LOV-LISTING and LOV-HOLDING and are not enumerated in code
    And the title status and the Land Office registration reference carry the placeholder and its gap identifier because no element holds them

  Scenario: C3 The asset reads are declared with their rights (new, D-RCV-60)
    Given the operations the baseline provides on base /api/recovery/asset/v1
    When the method, path, documented answer, right and idempotency of each are read
    Then both asset reads carry the Asset and disposal right R with scope applied and no idempotency
    And no write operation is declared for the registration, and POST /assets/{assetId}/valuations and POST /assets/{assetId}/listings are named as other stories'

  Scenario: C4 The consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-case and rwb-document are read
    Then each row names its owner, its use and its 2 s budget
    And where the name is not published the row carries the placeholder and the gap identifier and no invented path

  Scenario: C5 The error envelope is declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the error set and the rights of each operation are read
    Then the error set names 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 in one problem envelope
    And the capability area and the right of each operation are the rows of the access matrix

  Scenario: C6 The decision-record, rule-package and fake elements are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the rule-package element and the fake table are read
    Then the decision-record element names RWB-PLT-E1027-CON as its library and the transaction it joins
    And the rule-package element names the DISPOSAL package, its owner, its version in force and R-DIS-52 with R-DIS-02, and declares no rule row
    And every consumed row has a fake with a documented answer, including the stopped stub, the refused release and the repeated registration

  Scenario: C7 The naming and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue and the schema of the baseline
    When the document is checked against the naming rule and the ownership map
    Then the base /api/recovery/asset/v1, the queue rwb-asset and the topic rwb.asset.events.v1 are the only ones declared as this service's own
    And no Land Office interface, no title column, no foreign schema, no monolith base and no Schedule for the transfer timer is declared
    And no event is published or consumed by the title branch
```

The seven criteria are new to this run and are tagged as such: they test the contract deliverable only — the schema, the elements, the lists, the operations, the consumed rows, the rights, the envelope, the two library elements, the fakes and the boundary. No criterion states a business outcome or a business value of the application story, and none asserts that a rule fires, that a document is released or that a case moves.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, event and table: the baseline declares only the rows the Ownership Map gives to S5, and names every other row with its owner | Ownership Map; Architecture v5 slide 41; GAP-2938 |
| BR2 | A consumed row with no published name carries the placeholder and its gap, and never an invented path | §R9; GAP-2939 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; C1 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain | ADR-020 |
| BR5 | No event is published and none is consumed by the title branch: the owned event is EV-22 `AssetTakenOn`, the take-on story's, and the registration is a workflow signal | TSD S5 T5.3 |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR7 | The rule package is referenced, never redefined: the DISPOSAL package, its version and the rows are rwb-decision's, and no rule table of this service is declared | GAP-2940 |
| BR8 | No business value and no business list is enumerated: the ten working days, the statuses and the types are referenced with their identifier and version | §R7.2 (s16); legacy Guardrails |
| BR9 | No personal data in any element, fake or example of the baseline; a buyer is a code and the property address stays an ACE fact | §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation, topic or interface as its own, and it declares no Land Office interface at all | DP-01, DP-13, DP-14; GAP-2937 |

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
| In review | A row reaches a foreign schema, base, queue or the Land Office | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Authors the baseline, resolves the shape of the service's own operations and signs the tag |
| Owner of rwb-case (P3) | Reviews the case state and case-move rows and publishes the operation names when they exist |
| Owner of rwb-document (P5) | Reviews the custody release row, its key, its answer and its refusal, and publishes the operation name when it exists |
| Owner of rwb-decision (P7) | Reviews the rule-package element, the DISPOSAL package version and the decision-record element with the platform library |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the rights of each declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The asset page of `GET /assets` | S5 (`rwb_asset`) | The paginated asset list with its filters, its paging elements, the holding status and the listing status of each asset | Read by the screens |
| The asset answer of `GET /assets/{assetId}` | S5 (`rwb_asset`) | The asset of status 200 with its title, its sale, its holding status and the status of its listing | Read by the screens; written by the application story |
| The asset elements (DF-COL-028 to DF-COL-042) | S5 (`rwb_asset`) | id, case_id, asset_ref, asset_type, transfer_in_type, transfer_in_date, book_value, holding_status and the rest, referenced with `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN` and `LOV-HOLDING` | Written by the application story |
| The listing elements (DF-SAL-001 to DF-SAL-008) | S5 (`rwb_asset`) | sale_channel, start_price, floor_price, round_no, listed_at and status, referenced with `LOV-SALE-CHANNEL` and `LOV-LISTING` | Written by the application story |
| The sale elements (DF-SAL-009 to DF-SAL-019) | S5 (`rwb_asset`) | id, asset_key, listing_id, contract_date, sale_date, sale_price, the fee and tax elements and gain_loss | Referenced and read; not written here |
| The title status and the Land Office registration reference | none | Not specified in the source documents for the element they occupy (GAP-2938; ASM-4834); declared only once an element names them | Carried as a record fact and a signal element |
| The case elements of the consumed read | P3 (`rwb_case`) | The case reference, the case state and the stage outcome; referenced, not redefined | Consumed |
| The custody elements of the consumed row | P5 (`rwb_document`) | The document set of the asset, its custody state and the release answer, in place of the legacy `document_custody` write | Consumed |
| The decision-record elements | PLT library, created in `rwb_asset` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time (DF-DEC-001 to DF-DEC-018) | Written through the library |
| The rule-package elements | P7 (`rwb_decision`) | The package name, its version in force and the rows R-DIS-52 and R-DIS-02 (DF-REF-001 to DF-REF-015) | Referenced only |

The baseline declares no new table, no new column and no migration, and it enumerates no business value: every list, code and threshold is referenced with its identifier and its version. **No personal data** appears in any element, fake or example; the fixture identifiers are synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). These are the reads that answer SCR-21 and SCR-22.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the holding status and the listing status of each asset (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, its sale, its holding status and the status of its listing (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

No write operation is declared for the registration. `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's, `POST /assets/{assetId}/listings` (API-S5-004) is the pricing story's and `POST /listings/{listingId}/rounds` (API-S5-005) is the auction story's; the title transfer enters as a workflow signal because no source publishes an operation for it (GAP-2937; ASM-4833).

The error envelope of the declared operations: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for a missing field, and 503 when the decision library or a consumed boundary does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state the rule checks before it fires; faked |
| The case-move answer (name Not specified in the source documents (GAP-2939; ASM-4835)) | rwb-case (P3) | P3 rwb-case | The answer that carries `ASSET_SOLD` with its rule version; on the workflow boundary it is the outcome the parent applies; faked |
| The custody release (name Not specified in the source documents (GAP-2939; ASM-4835)) | `/api/recovery/document/v1` | P5 rwb-document | The release of the documents of the asset from custody, with an idempotency key, in place of the legacy `document_custody` write (DP-05); faked |

Each row is one hop or one activity, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag rather than inventing a surface (BR2, GAP-2939).

#### 12.3 Events published

None. The owned event row of this service is EV-22 `AssetTakenOn`, published by the take-on story when the asset record opens (TSD S5 T5.3). This baseline declares it as another story's, adds nothing to `rwb.asset.events.v1`, and the title branch writes no outbox row: its outward surface is the case-move answer and its own reads.

#### 12.4 Events consumed

None. The registration, the case state and the package in force arrive as signals of `AssetDisposalWorkflow`, so the baseline declares no topic subscription, no consumer group and no inbox row; a build that subscribes to a topic not listed by Architecture v5 fails the naming check (BR5, DP-14).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference, the listing reference and the rule package in force; signals: the registration recorded, the case state and the rule package in force |
| `recordLandOfficeTransfer` | Activity, the title-transfer step | `rwb-asset` | The registration and the case in; the rule IDs with their versions, the listing and holding statuses, the release answer and the stage outcome out, in one transaction |

The workflow is the same execution the take-on, holding and sale stories of this service use; this baseline fixes its input and signal elements and the one activity it adds, and it declares no child workflow and no second queue. The activity name is a design choice of the application story, and the baseline carries it so that the workflow's history is stable.

#### 12.6 Schedules

None. R-DIS-52's ten working days run as a workflow timer and a case SLA, so the baseline declares no Temporal Schedule and no legacy Quartz job for the transfer. The single Schedule of the service is JOB-19, which the re-appraisal story owns and which is not declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`), read as S5 from TSD S5 T3.1 while the map names no row (GAP-2938; ASM-4834) | The baseline declares its status element, not its schema |
| listing | S5 (`rwb_asset`) | The baseline declares its status element, not its schema |
| asset_sale | S5 (`rwb_asset`) | Referenced for the sale of the case; not written by this step |
| decision_record | PLT library, created in `rwb_asset` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated registration and of the release |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `document` and `document_custody` (P5), `decision_log_entry`, `rule_row` and `approval` (P7), `proceeds` (P8) and every `v_ace_*` view (P1) are named by their owner and never declared here. No title column exists and none is declared (GAP-2938).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state and case-move fake | The case states `TITLE_TRANSFER_PENDING` and `ASSET_PENDING_TAKE_ON` of the fixture cases; `ASSET_SOLD` and `ASSET_ON_BOOKS` accepted, and a move refused for an unexpected state | C3, C4, C6 |
| rwb-document custody release fake | Documents released; custody already released; a refusal; no answer inside 2 s | C4, C6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-52 and R-DIS-02 | C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000591`, with the statuses read once | C2, C6 |
| Registration signal fake | A property registration, a vehicle registration and a repeated registration on the same key | C2, C3, C5 |
| Asset answer fake | The `Asset` answer with its mandatory elements and one with an optional element absent | C2, C3 |

Each fake answers only what its owner documents, and a fake that answers more than the document fails the review. The names that are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2939; ASM-4835).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-case state read and move answer and the rwb-document custody release; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The registration is a workflow signal; nothing is published |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and `recordLandOfficeTransfer` on `rwb-asset`; no Schedule |
| File | None | No file element is declared, and the Land Office has no interface (GAP-2937) |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4029 CON Record a property transfer at the Land Office - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S5-E4029.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operations, the consumed rows, the published and consumed events, the workflow and its activity, the schedules, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Open shapes carried into the tag.** Three shapes are carried as placeholders and not invented: the title status and the registration reference (GAP-2938; ASM-4834), the names of the three consumed rows (GAP-2939; ASM-4835) and the registration signal's own elements, which are Not specified in the source documents (GAP-2937; ASM-4833). A placeholder is a declared forthcoming shape, not a permission to guess.

**Done when.** The seven criteria pass, the reviewers of rwb-case and rwb-document have closed their comments, the compatibility check passes on the tag, the fakes are published with their documented answers, and RWB-S5-E4029-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Asset and disposal right calls one of the declared operations | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of a declared request is absent or invalid | Enter {field}. |
| MSG-S5-001 | Carried from the service set and declared as the envelope row it is; no path of this baseline raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the service set and declared as the envelope row it is; no path of this baseline raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published name | Not specified in the source documents (GAP-2939; ASM-4835). |

The five message IDs are carried from the service and platform sets and are declared only as the envelope rows of the operations in this baseline; the two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-21 Asset list and SCR-22 Asset record through the gateway-bff composite route (DP-19). What this story fixes is the element list of the declared responses and the empty, loading, refused, wrong-state, refused-release and repeated-registration states the route can show from this service's answers. The route itself, its merge order and its field list are RWB-PLT-N001-CON, and the screens' transitions are the application story's.

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-029-01 | C2: the status elements and the asset answer the declared reads carry | Contract | The published schema and a recorded asset answer of asset `AST-2026-000591` |
| TC-E4-029-02 | C3, C5: the provided operations, their rights and their error set | Contract | One request per operation and per right, including a role without it and a 404 for an out-of-scope asset |
| TC-E4-029-03 | C4: the consumed rows of rwb-case and rwb-document | Contract | The three consumed rows, each with and without a published name |
| TC-E4-029-04 | C5: the error envelope of the declared operations | Contract | One request per error code, 400, 401, 403, 404, 422 and 503 |
| TC-E4-029-05 | C7: the naming and the boundary rule | Contract | The base, the topic, the queue and the schema, plus a draft that names a foreign schema, a monolith base, a Land Office interface or a Schedule |
| TC-E4-029-06 | C1, C6: the compatibility check, the library elements and the fakes | Contract | The previous tag, an additive draft, a breaking draft, the seven fakes and one fake that answers more than its document |
| TC-S5-E4029-CON-01 | C2: the title status and registration placeholder | Contract | The element list with and without a named element for the title |
| TC-S5-E4029-CON-02 | C7, BR5: no event published and none consumed | Contract | The outbox declaration, empty, and the absent subscription row |
| TC-S5-E4029-CON-03 | C3: no write operation for the registration | Contract | The operation inventory with and without a registration write |
| TC-S5-E4029-CON-04 | C6: the rule-package element and its rows | Contract | The package declaration with R-DIS-52 and R-DIS-02, and a draft that declares a rule row |

The six legacy case IDs are mapped onto this contract deliverable in their legacy order, and their `Covers` names the criterion of this story that fixes the surface each legacy case touches: the answer and its statuses (01), the operations and rights (02), the consumed rows (03), the failure and error path (04), the naming boundary (05) and the record, library and fake elements (06). The four `TC-S5-E4029-CON-` cases are new and test the parts of the baseline that no legacy case touches: the title placeholder, the absence of an event, the absence of a registration write and the rule-package element. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the baseline: the ten working days, the statuses, the types and every threshold are referenced with their identifier and version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the sale facts appear only through `asset_sale` (DP-05).
- The case stays with rwb-case, the documents with rwb-document and the rules with rwb-decision: no `recovery_case` element, no custody element and no rule row is declared as this service's own.
- No interface, file or operation is declared for the Land Office (BR10).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Schedule for the transfer timer, no event published or consumed by this branch.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-008 | Title transfer is prepared and recorded for vehicles and for property (Business Requirements Program v5); the plan carries no requirement id for this slice (GAP-2942; ASM-4838) | The baseline, its consumed rows and its fakes | TC-S5-E4029-CON-01, TC-E4-029-03 |
| ADR-013 | 19 services inside ACE | The baseline's ownership rows | TC-E4-029-05 |
| ADR-014 | Schema and login per service | `rwb_asset` and the declared tables | TC-E4-029-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows and the compatibility check | TC-E4-029-03, TC-E4-029-06 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its library | TC-E4-029-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-029, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 are carried by RWB-S5-E4029-APP; this story carries no legacy criterion and tests the surface they touch |
| Test cases | TC-E4-029-01 to TC-E4-029-06 at Level Contract, and TC-S5-E4029-CON-01 to TC-S5-E4029-CON-04 |
| Feature and screens | FEAT-AST-20, SCR-21 Asset list and SCR-22 Asset record, read through the composite route |
| Rules | R-DIS-52 and R-DIS-02, referenced as rule-package rows and not evaluated here |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The transfer behaviour, the rule evaluation, the release call, the status writes, the decision records and the case moves: RWB-S5-E4029-APP.
- The Land Office itself and any interface, file or operation for it (GAP-2937; ASM-4833).
- Any column, index or migration for the title status or the registration reference (GAP-2938; ASM-4834).
- The documents, their custody and their retention: rwb-document (P5) (GAP-2939; ASM-4835).
- The payment term, the award and the confirmation that starts the transfer: FEAT-AST-18's story.
- The vehicle registration through SCIS: FEAT-AST-19's story.
- The property take-on after a deed in lieu: RWB-S5-E3020-APP (GAP-2940; ASM-4836).
- The rejection of a transfer and the blocked title: R-DIS-53, with no owner in this split (GAP-2941; ASM-4837).
- The proceeds, the shortfall and the vendor fee: FEAT-AST-21's story and rwb-payment (P8).
- The case of record, its states and the parent workflow: rwb-case (P3).
- The rule package, its version and its approval: rwb-decision (P7).
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The composite route, its merge order and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
