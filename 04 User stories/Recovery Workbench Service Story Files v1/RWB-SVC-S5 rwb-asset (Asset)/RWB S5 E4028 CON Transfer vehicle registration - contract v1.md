# RWB-S5-E4028-CON Transfer vehicle registration - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4028-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-028 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-028, the baseline the title-transfer branch of rwb-asset builds against on Day 1. The baseline declares the two asset reads that answer SCR-21 Asset list and SCR-22 Asset record on `/api/recovery/asset/v1` (DP-13), the four consumed rows of rwb-integration (the SCIS transfer, INT-28), rwb-source-data (the asset and sale product, DP-05) and rwb-case (the state read and the move answer), the decision-record element of DP-03, the rule-package element the branch evaluates against, the rights and the error envelope, and the fakes. No event is published and none is consumed, because the owned event of the service is EV-22 `AssetTakenOn` and the transfer facts are workflow signals. No source gives the SCIS interface a row in TSD S5 T5.1 or a call type, and DP-16 is outside the pattern set (GAP-2931; ASM-4828); the FSD makes the step a system submission while INT-28 has the officer prepare it (GAP-2932; ASM-4829); no element holds the vehicle registration particulars or the submission reference (GAP-2933; ASM-4830); R-DIS-53 has no owning story (GAP-2934; ASM-4831); the rule package is declared without the DP-04 platform row (GAP-2935; ASM-4796); and REQ-S5-008 is claimed twice (GAP-2936; ASM-4832). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the vehicle-registration transfer capability of rwb-asset — its two asset reads, its four consumed rows, its decision-record and rule-package elements, its rights, its error envelope and its fakes — baselined and tagged before the build starts**, so that **the application story and every consumer of a transfer can build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer or of an interface no source describes**.

This is the contract slice of legacy RWB-E4-028. It owns:

- the document that fixes the two asset reads on base `/api/recovery/asset/v1`, with their parameters, documented answer, right and idempotency (DP-13);
- the four consumed rows: the rwb-integration SCIS transfer (INT-28), the rwb-source-data asset and sale product, the rwb-case state read and the case-move answer, each with its owner, its use and a placeholder where no name is published (DP-05; GAP-2931);
- the decision-record element and the local library dependency that carries it (DP-03);
- the rule-package element: the DISPOSAL package, its version and R-DIS-51, declared as a reference and not as a rule table of this service;
- the capability area, the right and the error envelope of the operations it declares;
- the fakes and their documented answers, one per consumed row, so that every downstream answer has a stub on Day 1;
- the naming and boundary rules of the baseline: one base, one topic, one queue, no foreign schema, no monolith base, no direct external call and no Schedule for a workflow timer.

It does not own: the branch behaviour, the pack, the submission, the record, the row writes and the case answer, which are RWB-S5-E4028-APP; the payment term and its confirmation, FEAT-AST-18's story; the property transfer at the Land Office, FEAT-AST-20's story; the rejected transfer R-DIS-53, which no story row owns (GAP-2934); the proceeds, FEAT-AST-21; the SCIS adapter itself, rwb-integration (P2); the case, rwb-case (P3); the rules, rwb-decision (P7); the documents, rwb-document (P5); the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

### 2. Business rationale

A contract baseline is what lets the stories of one wave build at once. Here it matters more than usual, because the SCIS interface has no technical entry: the FSD names SCIS as an integration point of A2.19, INT-28 records it as "Not available today; prepared by the officer", and the TSD S5 T5.1 table does not list it at all. Without a tagged baseline the branch would be written against whatever the adapter happened to answer, and the first integration would find the mismatch instead of the review. With it, the application story builds on Day 1 against a tagged document and its fakes, and rwb-integration, rwb-source-data and rwb-case know exactly which elements the transfer needs.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner and its use, and where no name is published the row carries the placeholder rather than an invented path (GAP-2931; ASM-4828).
- **one hop, one budget.** Every consumed row is a single hop with a 2 s timeout, a breaker and no chain, which is ADR-020 and what the application story's exception paths assume.
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document (C1).

The business outcome the baseline protects is the one FEAT-AST-19 of the FSD and BR-029 of the Epic 4 BRD name: the title transfer is prepared and submitted for a vehicle through SCIS. The baseline does not state that outcome, and no criterion here asserts a business value.

### 3. Preconditions

- The Ownership Map rows are in force: S5 owns `GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds`; `asset_sale` and `listing` are S5's tables, and `asset` is the service's ACE extension table of TSD S5 T3.1.
- The service naming is fixed: schema `rwb_asset`, login `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with `.retry` and `.dlt`, task queue `rwb-asset` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.asset`.
- The published shapes of the declared operations are the API Specification v4: `AssetPage` and `Asset`.
- The owned event row of the service is EV-22 `AssetTakenOn` (TSD S5 T5.3); the transfer facts are signals of `AssetDisposalWorkflow`.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). DP-04 is not in the pattern set, so no platform row for the rules kit is claimed (GAP-2935; ASM-4796), and DP-16 is not in it either, so no C row to rwb-integration is claimed (GAP-2931; ASM-4828).
- No approval is needed to publish a Draft baseline; the document is baselined by this story's own review, and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map, the TSD S5 T-A.1 operations, the TSD S5 T3.1 tables and the lists of T3.2.
2. Every operation is declared with its method, path, documented answer, right, idempotency and error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where no name is published, including the SCIS row that TSD S5 T5.1 omits (GAP-2931; ASM-4828).
4. The decision-record element is declared with the library that carries it, and the rule-package element with its owner and version.
5. The fakes are declared with their documented answers, one per consumed row and one per screen route and pack shape.
6. The schema, the open lists and the closed lists are published, and the compatibility check runs: a breaking change fails it.
7. The document goes to review as Draft; the reviewers are the owners of the consumed rows and the tech lead of the service.
8. On the review's close the document is tagged and baselined; the application story starts against the tag and the fakes.
9. A defect in the build that needs a shape change is raised against this document; the document moves to a new minor or major version and the code never moves ahead of it.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and the gap; no path is invented and no field is guessed | C2, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails, the version becomes a new major and the document is re-reviewed | C1 |
| X3 | A declared operation reaches another service's data or base, or the service calls SCIS directly | The review refuses the baseline and the boundary test fails the build | C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged; the application story cannot start | C6 |
| X5 | The right of an operation is not one of the rows of the access matrix | The operation is not declared and its error set is incomplete | C3, C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a new version, this document follows, and the application story re-tests against the new fake | X2 |
| X7 | Two documents claim the same path or queue, or a document invents a registration element that no table names | The owner in the Ownership Map keeps the path and the placeholder rule resolves the element | C2, C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 the paths of a baseline moving under a build, and X7 the naming and placeholder boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the order and the fake data are this story's choice; the paths, the owners, the base, the error set and the element names are fixed by their sources |
| Valuable | The stories of wave 3 build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, two provided operations, four consumed rows, two library elements, eight fakes and one compatibility check |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the vehicle-registration transfer capability

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
    And the vehicle registration particulars and the submission reference carry the placeholder and the gap identifier because no table or request element holds them

  Scenario: C3 The asset reads are declared with their right and the submission is declared as an activity (new, D-RCV-60)
    Given the operations the baseline provides on base /api/recovery/asset/v1
    When the method, path, documented answer, right and idempotency of each are read
    Then the two asset reads carry the Asset and disposal right R with scope applied and no idempotency
    And no REST operation is declared for the transfer submission, because the step runs unattended in the workflow
    And GET /assets/{assetKey} and the listings and rounds writes are named as the sibling stories' and are not declared here

  Scenario: C4 The consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-integration, rwb-source-data and rwb-case are read
    Then each row names its owner, its use and its 2 s budget
    And the SCIS row is declared although TSD S5 T5.1 lists no interface row for it, and its call type is an activity on the owner's queue
    And where no name is published the row carries the placeholder and the gap identifier and no path

  Scenario: C5 The error envelope is declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the error set and the right of each operation are read
    Then the error set names 400, 401, 403 with MSG-P4-002, 404 and 503 in one problem envelope
    And the capability area and the right of each operation are the row of the access matrix

  Scenario: C6 The decision-record, rule-package and fake elements are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the rule-package element and the fake table are read
    Then the decision-record element names RWB-PLT-E1027-CON as its library and the transaction it joins
    And the rule-package element names the DISPOSAL package, its owner, its version in force and R-DIS-51, and declares no rule row
    And every consumed row has a fake with a documented answer, including the stopped stub, the stale product, the rejected transfer and the unanswered adapter

  Scenario: C7 The naming and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue and the schema of the baseline
    When the document is checked against the naming rule and the ownership map
    Then the base /api/recovery/asset/v1, the queue rwb-asset and the topic rwb.asset.events.v1 are the only ones declared as this service's own
    And no foreign schema, no foreign topic, no monolith base /api/recovery/v1 and no Schedule for the transfer timer is declared
    And no external call to SCIS is declared from this service and no event is published or consumed by the branch
```

The seven criteria are new to this run and are tagged as such: they test the contract deliverable only — the schema, the elements, the lists, the operations, the consumed rows, the right, the envelope, the two library elements, the fakes and the boundary. No criterion states a business outcome, and none asserts that R-DIS-51 fires, that a transfer is accepted or that a case moves.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, event and table: the baseline declares only the rows the Ownership Map gives to S5, and names every other row with its owner | Ownership Map; Architecture v5 slide 41 |
| BR2 | A consumed row with no published name carries the placeholder and its gap, and never an invented path | Template and Rules v1 §R9; GAP-2931 |
| BR3 | The baseline is additive: a new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version | ADR-020; C1 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain; the SCIS row is an activity on the owner's queue | ADR-020; Architecture v5 slide 13 |
| BR5 | No event is published and none is consumed by the branch: the owned event is EV-22 `AssetTakenOn`, the take-on story's, and the transfer facts are workflow signals | TSD S5 T5.3 |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR7 | The rule package is referenced, never redefined: the DISPOSAL package, its version and R-DIS-51 are rwb-decision's rows and no rule table of this service is declared | DP-04 (not claimed); GAP-2935 |
| BR8 | The registration particulars and the submission reference are declared only once an owner names them; until then they carry the placeholder | GAP-2933; ASM-4830 |
| BR9 | No personal data in any element, fake or example: a vehicle is a reference and a code, and every fixture is synthetic | Template and Rules v1 §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation or topic as its own, and no document or test declares a direct SCIS call from this service | DP-01, DP-05, DP-13, DP-14 |

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
| In review | A row reaches a foreign schema, base or topic, or a direct SCIS call | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Authors the baseline, resolves the shape of the service's own reads and signs the tag |
| Owner of rwb-integration (P2) | Reviews the SCIS transfer row, publishes its call type and its answer shape, and confirms INT-28's availability (GAP-2931, GAP-2932) |
| Owner of rwb-source-data (P1) | Reviews the asset and sale product row, its dates and its freshness stamp |
| Owner of rwb-case (P3) | Reviews the case state and case-move rows and publishes the operation names when they exist |
| Owner of rwb-decision (P7) | Reviews the rule-package element, the DISPOSAL package version and the decision-record element with the platform library |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of each declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The asset page of `GET /assets` | S5 (`rwb_asset`) | The paginated asset list with its filters, its paging elements and the transfer status of each asset | Read by the screens |
| The asset answer of `GET /assets/{assetId}` | S5 (`rwb_asset`) | The asset of status 200 with its title, its sale, its `holding_status` and its transfer status | Read by the screens; written by the application story |
| The asset elements (DF-COL-028 to DF-COL-042) | S5 (`rwb_asset`) | id, asset_ref, asset_code, asset_type, transfer_in_type, holding_status and the further columns, with `LOV-ASSET-TYPE`, `LOV-HOLDING` and `LOV-TRANSFER-IN` | Read by the pack; `holding_status` written by the application story |
| The sale elements (DF-SAL-009 to DF-SAL-019) | S5 (`rwb_asset`) | id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee and the tax and gain elements | Read by the pack; the transfer status written by the application story |
| The registration particulars and the submission reference | none | Not specified in the source documents for the element they occupy (GAP-2933; ASM-4830); declared only once their owner names it | Held with the submission record |
| The transfer answer of the consumed row | P2 (`rwb_integration`) | The accepted or rejected answer with its submission reference, in place of the direct SCIS call (INT-28) | Consumed |
| The asset and sale elements of the consumed product | P1 (`rwb_source_data`) | The asset, sale and registration facts with their data date, in place of the legacy `v_ace_npa_asset` and `v_ace_npa_sale` reads | Consumed |
| The case elements of the consumed read | P3 (`rwb_case`) | The case reference, the case state and the stage outcome; referenced, not redefined | Consumed |
| The decision-record elements | PLT library, created in `rwb_asset` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time (DF-DEC-001 to DF-DEC-018) | Written through the library |
| The rule-package elements | P7 (`rwb_decision`) | The package name, its version in force and R-DIS-51 (DF-REF-001 to DF-REF-015) | Referenced only |

The baseline declares no new table, no new column and no migration, and it enumerates no business value: every list, code and timer is referenced with its identifier and its version. **No personal data** appears in any element, fake or example; the fixture identifiers are synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). These are the reads that answer SCR-21 and SCR-22.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the transfer status of each asset (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, its sale, its `holding_status` and its transfer status (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

`GET /assets/{assetKey}` is the sibling stories' row of the same base, and the writes `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds` belong to the pricing and round stories; none is declared here. No REST operation is declared for the transfer submission: the step runs unattended in the workflow and reaches SCIS through rwb-integration (C3, BR4).

The error envelope of the declared operations: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope asset, and 503 when the decision library or a consumed boundary does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state the rule checks before it fires; faked |
| The case-move answer (name Not specified in the source documents (GAP-2931; ASM-4828)) | rwb-case (P3) | P3 rwb-case | `ASSET_SOLD` with its rule version; on the workflow boundary it is the outcome the parent applies; faked |
| The asset and sale product (name Not specified in the source documents (GAP-2931; ASM-4828)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset, sale and registration facts with their data date, in place of the legacy `v_ace_npa_asset` and `v_ace_npa_sale` reads (DP-05); faked |
| The SCIS transfer (name Not specified in the source documents (GAP-2931; ASM-4828)) | queue `rwb-integration` | P2 rwb-integration | The transfer pack out and its accepted or rejected answer with the submission reference back (INT-28); faked |

Each row is one hop or one activity, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). The SCIS row is an activity on the owner's queue, because a route service reaches a shared capability through Temporal, never REST (Architecture v5 slide 13), and because INT-28 records the interface as not available today (GAP-2931; GAP-2932). Where no name is published the row carries the placeholder and no path, so the consumer adapts at the tag rather than inventing a surface (BR2).

#### 12.3 Events published

None. The owned event row of this service is EV-22 `AssetTakenOn`, published by the take-on story when the asset record opens. This baseline declares it as no part of its own, adds nothing to `rwb.asset.events.v1`, and the branch writes no outbox row: its outward surface is the case-move answer, its own reads and the consumed adapter (BR5).

#### 12.4 Events consumed

None. The transfer due fact, the payment confirmation and the adapter answer arrive as signals and activity results of `AssetDisposalWorkflow`, so the baseline declares no topic subscription, no consumer group and no inbox row; a build that subscribes to a topic not listed by Architecture v5 fails the naming check (BR5, DP-14).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference, the sale reference and the rule package in force; signals: the transfer due fact, the payment confirmation, the adapter answer and the rule package in force |
| `submitRegistrationTransfer` | Activity, the pack, the submission and the write | `rwb-asset` | The asset, the sale and the case in; the rule ID with its version, `holding_status`, the transfer status, the submission reference and the stage outcome out, in one transaction |
| The SCIS transfer activity (name Not specified in the source documents (GAP-2931; ASM-4828)) | Activity, consumed | `rwb-integration` | The pack in; the accepted or rejected answer with its submission reference out (INT-28) |

The workflow is the same execution the take-on, holding and sale stories of this service use; this baseline fixes its input and signal elements and the one activity it adds, and declares no child workflow and no second queue. The activity names are design choices of the application story, carried here so that the workflow history is stable.

#### 12.6 Schedules

None. The 5 working days of R-DIS-51 run as a durable timer inside the workflow, so the baseline declares no Temporal Schedule and no legacy Quartz job for the transfer. The single Schedule of the service is JOB-19, the re-appraisal story's, and it is not declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`) | The asset record; the baseline declares the elements of `holding_status` and the transfer pack, not its schema |
| asset_sale | S5 (`rwb_asset`) | The sale; the baseline declares the elements the pack reads and the transfer status, not its schema |
| decision_record | PLT library, created in `rwb_asset` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated signal and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `listing` (S5 but the sibling stories'), `document` and `document_custody` (P5), `proceeds` (P8), `deviation` (S8) and every `v_ace_*` view (P1) are named by their owner and never declared here. No element holds the registration particulars or the submission reference and none is declared (GAP-2933; ASM-4830).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state and case-move fake | `TITLE_TRANSFER_PENDING` for the fixture cases; the move accepted and a move refused for an unexpected state | C3, C4, C6 |
| rwb-source-data product fake | Vehicle asset `AST-2026-000541` with its sale at today's date; a stale product with its date; a property asset; no answer inside 2 s | C2, C4, C6 |
| SCIS transfer fake (INT-28) | Accepted with a submission reference; rejected with its reason; unavailable, as INT-28 records the interface today; no answer inside 2 s | C4, C6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-51 | C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000541`, with the transfer status read once | C2, C6 |
| Pack fake | A pack built from a vehicle asset and its sale, and the same pack with a required element absent and with the particulars absent | C2, C3 |
| Read fake | An asset page and an asset answer, and one of each of `404` and `403` | C3, C5 |

Each fake answers only what its owner documents, and a fake that answers more than the document fails the review. The names that are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2931; ASM-4828).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two asset reads on `/api/recovery/asset/v1`; the case state read, the case-move answer and the source-data product; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The transfer facts are workflow signals; nothing is published |
| Temporal | 1 workflow and 2 activities | `AssetDisposalWorkflow` and `submitRegistrationTransfer` on `rwb-asset`; the SCIS transfer activity on `rwb-integration`; no Schedule |
| File | None | INT-28 names no file and no API approach, and the baseline declares neither (GAP-2931) |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4028 CON Transfer vehicle registration - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S5-E4028.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operations, the consumed rows, the published and consumed events, the workflow and its activities, the schedules, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Open shapes carried into the tag.** Three shapes are carried as placeholders and not invented: the names and peculiarities of the four consumed rows (GAP-2931; ASM-4828), whether the submission is automatic or officer-prepared (GAP-2932; ASM-4829) and the registration particulars with the submission reference (GAP-2933; ASM-4830). A placeholder is a declared forthcoming shape, not permission to guess.

**Done when.** The seven criteria pass, the reviewers of the three consumed owners have closed their comments, the compatibility check passes on the tag, the fakes are published with their documented answers, and RWB-S5-E4028-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Asset and disposal right calls one of the declared operations | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of a declared request or of the pack is absent or invalid | Enter {field}. |
| MSG-P1-001 | The consumed asset and sale product is stale at the tag | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S5-001 | A declared read carries a floor under the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | A declared read carries an appraisal more than a year old | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published name | Not specified in the source documents (GAP-2931; ASM-4828). |

The six message IDs are carried from the service and platform sets and are declared only as the envelope rows of the operations in this baseline; the two document rules are checks of this story and are not service messages. No message exists for a rejected transfer at this level (GAP-2934).

### 15. Screens and states

The baseline serves SCR-21 Asset list and SCR-22 Asset record through the gateway-bff composite route (DP-19). What this story fixes is the element list of the declared responses and the empty, loading, refused, not-found, stale and rejected states the route can show from this service's answers. The route itself, its merge order and its field list are RWB-PLT-N001-CON, and the screens' transitions are the application story's.

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-028-01 | C2, C3: the asset elements, the transfer status and the declared reads | Contract | The published schema, an asset and its sale of `AST-2026-000541` |
| TC-E4-028-02 | C4: the four consumed rows of rwb-integration, rwb-source-data and rwb-case | Contract | The four rows, each with and without a published name |
| TC-E4-028-03 | C5: the error envelope of the declared operations | Contract | One request per error code, 400, 401, 403, 404 and 503 |
| TC-E4-028-04 | C3, C5: the right of the declared operations | Contract | One call per right, including a role without it |
| TC-E4-028-05 | C6, C7: the two library elements and the boundary | Contract | A healthy and a stopped stub; a draft that names a foreign schema, a monolith base, a Schedule or a direct SCIS call |
| TC-S5-E4028-CON-01 | C2: the registration placeholder | Contract | The element list with and without a named element for the particulars and the reference |
| TC-S5-E4028-CON-02 | C6: the fakes and their documented answers | Contract | The eight fakes, the stopped stub, the rejected and unavailable transfer, and one fake that answers more than its document |
| TC-S5-E4028-CON-03 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |
| TC-S5-E4028-CON-04 | C7, BR5: no event published, none consumed and no direct external call | Contract | The outbox declaration, empty, the absent subscription row and the absent SCIS client |

The five legacy case IDs are mapped onto this contract deliverable in their legacy order, and their `Covers` names the criterion of this story that fixes the surface each legacy case touches: the asset elements and the reads (01), the consumed rows (02), the error path (03), the right (04) and the boundary (05); the legacy case 05, a forced record failure, is covered by the decision-record element of C6 and TC-S5-E4028-CON-02. The four `TC-S5-E4028-CON-` cases are new and test the parts of the baseline that no legacy case touches: the registration placeholder, the fakes, the compatibility check and the absence of an event. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the baseline: the 5 working days, the asset type, the transfer-in type and the statuses are referenced with their identifier and version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: a vehicle reference, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the asset and sale facts appear only as the P1 row (DP-05).
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case` element and no rule row is declared as this service's own.
- No direct external call: the SCIS submission appears only as the P2 row, and a document or a test that declares a SCIS client in this service fails the boundary check (BR10).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Schedule for the transfer timer, no event published or consumed by this branch.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-008 | The title transfer is prepared and submitted for a vehicle through SCIS (BR-029 of the Epic 4 BRD; the same ID is mapped to FEAT-AST-08 in TSD S5 T8: GAP-2936; ASM-4832) | The baseline, its consumed rows and its fakes | TC-S5-E4028-CON-01, TC-E4-028-02 |
| BR-029 | The title transfer is prepared and submitted for a vehicle through SCIS and recorded for a property at the Land Office | The vehicle half of the requirement, as the surface the baseline fixes | TC-E4-028-01, TC-E4-028-02 |
| ADR-013 | 19 services inside ACE | The baseline's ownership rows | TC-E4-028-05 |
| ADR-014 | Schema and login per service | `rwb_asset` and the declared tables | TC-E4-028-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows and the compatibility check | TC-E4-028-02, TC-S5-E4028-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its library | TC-S5-E4028-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-028, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 are carried by RWB-S5-E4028-APP; this story carries no legacy criterion and tests the surface they touch |
| Test cases | TC-E4-028-01 to TC-E4-028-05 at Level Contract, and TC-S5-E4028-CON-01 to TC-S5-E4028-CON-04 |
| Feature and screens | FEAT-AST-19, SCR-21 Asset list and SCR-22 Asset record, read through the composite route |
| Rules | R-DIS-51, referenced as a rule-package row and not evaluated here; R-DIS-48 and R-DIS-52 belong to the sibling stories and R-DIS-53 has no owner (GAP-2934) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The branch behaviour, the pack, the submission, the record, the row writes and the case answer: RWB-S5-E4028-APP.
- The five-day payment term and the confirmation into `TITLE_TRANSFER_PENDING`: FEAT-AST-18's story (R-DIS-47, R-DIS-48).
- The property transfer at the Land Office and the custody release: FEAT-AST-20's story (R-DIS-52).
- The rejected transfer and `TITLE_BLOCKED`: R-DIS-53, owned by no story row of the split (GAP-2934).
- The proceeds, the vendor fee and the shortfall: FEAT-AST-21's story (R-DIS-54, R-DIS-55).
- The SCIS adapter itself, its protocol and its availability: rwb-integration (P2) and INT-28 (GAP-2931; GAP-2932).
- The vehicle registration particulars and the submission reference: Not specified in the source documents (GAP-2933; ASM-4830).
- The documents of the case: rwb-document (P5).
- The case of record, its states and the parent workflow: rwb-case (P3).
- The rule package, its version and its approval: rwb-decision (P7) (GAP-2935).
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The composite route, its merge order and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The deployment, the flag, the dashboards, the alerts and the runbook: the operations story of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
