# RWB-S5-E4021-CON Evict occupants from a held property - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4021-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-021 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-021, the baseline the eviction step of rwb-asset builds against on Day 1. The baseline declares the asset reads that answer SCR-21 and SCR-22 on `/api/recovery/asset/v1` (DP-13), the stage signal and the case-move answer of rwb-case, the eviction element of the asset answer, the decision-record element of DP-03, the rights and the error envelope, and the fakes. The step publishes no event, because `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold` only. No ownership row and no other source publishes an operation for the eviction itself, so the baseline declares it as None with its gap (GAP-2892; ASM-4789); no source publishes the element names of the eviction or the operation names of the consumed rows (GAP-2893; ASM-4790); the split plan carries no requirement row for this slice (GAP-2894; ASM-4791). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4021-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the eviction step of rwb-asset — its asset reads, its stage signal, its case-move answer, its eviction element, its rights, its error envelope and its fakes — baselined and tagged before the build starts**, so that **the application story, the sibling holding and pricing stories and every consumer can build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-021. It owns:

- the document that fixes the two reads of the asset and its eviction state on base `/api/recovery/asset/v1`, with their parameters, their documented answer, their rights and their idempotency (DP-13);
- the stage signal the parent forwards, with the occupancy fact and the possession result as its documented elements, and the case-move answer it returns (GAP-2893; ASM-4790);
- the eviction element of the asset answer: the occupancy state, the eviction status and the instruction reference (GAP-2892; ASM-4789);
- the decision-record element and the local library dependency that carries it (DP-03);
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, so that every downstream answer has a stub on Day 1;
- the naming and boundary rules of the baseline: one base, one topic, one queue, no foreign schema, no monolith base.

It does not own: the eviction behaviour, the rule evaluation, the eviction record and the case move, which are RWB-S5-E4021-APP; the case of record and its route states, which are rwb-case's (P3); the legal act, which is rwb-litigation's (S4); the ACE asset facts, which are rwb-source-data's (P1); the rule package, which is rwb-decision's (P7); the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

### 2. Business rationale

A contract baseline is what lets ten teams build at once. Without it the eviction step would be written against whatever shape a neighbour happened to expose that week, and the first integration would find the mismatches instead of the review. With it, the application story builds on Day 1 against a tagged document and its fakes, the holding and pricing stories know what the asset answer carries for the eviction, and the consumers of this service's two events know that this baseline adds nothing to them.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner and its use, and where the source documents do not publish an element or an operation name the row carries the placeholder rather than an invented one (GAP-2893; ASM-4790).
- **one hop, one budget.** Every consumed row is a single hop with a 2 s timeout, a breaker and no chain, which is ADR-020 and is what the application story's exception paths assume.
- **additive only.** The baseline moves forward without breaking: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version and a new document (C1).

The business outcome the baseline protects is the one FEAT-AST-08 of the FSD names: the eviction opened and tracked, and the file reaching Legal with its decision on record. The baseline does not state that outcome, and no criterion here asserts a business value.

### 3. Preconditions

- The ownership rows of the context pack are in force: S5 provides `GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds`, and owns `asset_sale` and `listing`; the `asset` record the eviction is held against is read as S5's from Architecture v5 slide 13 and TSD S5 T3.1 although the ownership table list names the two sale tables only (GAP-2892; ASM-4789).
- The service naming is fixed: schema `rwb_asset`, login `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with `.retry` and `.dlt`, task queue `rwb-asset` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.asset`.
- Architecture v5 slide 13 is in force: a stage runs as a child workflow on the owner's queue, the case router sends the facts of other services to the case, the parent forwards them to the running child, and the stage answers its outcome to the parent.
- Architecture v5 slides 19 and 43 are in force: rwb-asset publishes `AssetTakenOn` and `AssetSold` only; this baseline touches no event and declares no subscription.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19).
- No approval is needed to publish a Draft baseline; the document is baselined by this story's own review, and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the ownership rows, Architecture v5 slide 13, the TSD S5 T-A.1 operations and the TSD S5 T3.1 tables.
2. Every operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. The stage signal is declared with its elements, its direction and its dedupe key, and the case-move answer with its elements and its rule-version element.
4. The eviction element of the asset answer is declared with its type, its nullability and its source, and with the placeholder where no column is named (GAP-2892).
5. The decision-record element is declared with the library dependency that carries it.
6. The fakes are declared with their documented answers, one per consumed row and one for the composite route.
7. The schema, the open lists and the closed lists are published, and the compatibility check runs: a breaking change fails the check.
8. The document goes to review as Draft; the reviewers are the owners of the consumed rows and the tech lead of the service.
9. On the review's close the document is tagged and baselined; the application story starts against the tag and the fakes.
10. A defect found in the build that needs a shape change is raised against this document, and the document moves to a new minor or major version; the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for an element the sources do not publish | The element carries the placeholder and the gap; no field is invented and no type is guessed | C2, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails, the version becomes a new major and the document is re-reviewed | C1 |
| X3 | A declared operation or element reaches another service's data or base | The review refuses the baseline and the boundary test fails the build | C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged; the application story cannot start | C6 |
| X5 | The rights of an operation are not one of the rows of the access matrix | The operation is not declared and the error set of the operation is incomplete | C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a new version, this document follows with a minor or major version, and the application story re-tests against the new fake | X2 |
| X7 | Two documents claim the same path, topic or queue | The naming and boundary rule resolves it: the owner named in the ownership rows keeps it, and the other document changes | C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 are the paths of a baseline moving under a build, and X7 is the naming boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the order of the sections and the fake data are this story's choice; the paths, the owners, the queue, the error set and the rule reference are fixed by their sources |
| Valuable | The service team and its neighbours build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, two provided operations, two consumed rows, one stage signal, one case answer, one library element, six fakes and one compatibility check |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the eviction step

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

  Scenario: C3 The stage signal and the case-move answer are declared (new, D-RCV-60)
    Given the workflow boundary section of the baseline
    When the signal and the answer are read
    Then the signal names its elements, its direction and its dedupe key on the fact reference
    And the answer names the case reference, the asset reference, the move, the instruction reference, the rule id and the rule version

  Scenario: C4 The consumed rows carry their owners and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rwb-case rows and the eviction element are read
    Then each row names its owner, its use and its 2 s budget
    And where the operation name or the element name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C5 The rights and the error envelope are declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the rights and the error set of each operation are read
    Then each operation names the capability area and the right of the access matrix
    And the error set names 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 in one problem envelope

  Scenario: C6 The decision-record element and the fakes are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element and the fake table are read
    Then the element names RWB-PLT-E1027-CON as its library and the transaction it joins
    And every row the application story consumes has a fake with a documented answer, including the stopped decision-record stub

  Scenario: C7 The naming and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue and the schema of the baseline
    When the document is checked against the naming rule and the ownership rows
    Then no foreign schema, no foreign topic and no monolith base /api/recovery/v1 is declared
    And no Schedule is declared, no event is published and no subscription of this service is declared by this step
```

The seven criteria are new to this run and are tagged as such: they test the contract deliverable only — the schema, the elements, the lists, the signal, the answer, the rights, the envelope, the decision-record element, the fakes and the boundary. No criterion states a business outcome or a business value of the application story, and none asserts that a rule fires or that a case moves.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, element and table: the baseline declares only the rows the ownership rows and Architecture v5 give to S5, and names every other row with its owner | Ownership rows of the context pack; Architecture v5 slides 13, 19, 41 and 43 |
| BR2 | A consumed row or an element with no published name carries the placeholder and its gap, and never an invented path or field | Template and Rules v1 §R9; GAP-2892, GAP-2893 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; C1 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain | ADR-020 |
| BR5 | The step publishes no event and subscribes to none: the topic `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold` only, and the facts arrive as stage signals | Architecture v5 slides 13, 19 and 43 |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR7 | No business value is declared in the baseline: the occupancy statuses, the eviction statuses, the instruction period and the thresholds are referenced with their identifier and version | Template and Rules v1 §R7.2 (s17); legacy Guardrails |
| BR8 | No personal data in any element, fake or example of the baseline, and no occupant is identified as a person | Template and Rules v1 §R7.2 (s17) |
| BR9 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

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
| Being authored | An element has no published name | X1 | The element carries the placeholder and the gap and the draft continues |
| In review | A row reaches a foreign schema, base or topic | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, the review reopens |

The eviction states of the asset are the application story's and are not declared here; the baseline declares only their shape, their source and the placeholder where a column is missing (GAP-2892).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Authors the baseline, resolves the shape of the service's own operations and signs the tag |
| Owner of rwb-case (P3) | Reviews the case state row, the stage signal and the case-move answer, and publishes the operation names when they exist |
| Owner of rwb-litigation (S4) | Reviews the eviction instruction reference the answer carries and confirms that no operation of S4 is declared here |
| Owner of rwb-source-data (P1) | Reviews the asset facts the `asset` row holds and the placeholder of the eviction element |
| Owner of rwb-decision (P7) | Reviews the rule package reference and the decision-record element with the platform library |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the rights of each declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The asset answer of `GET /assets/{assetId}` | S5 (`rwb_asset`) | The asset of status 200 with its title, its holding status and its eviction element | Read by the screens; written by the application story |
| The asset page of `GET /assets` | S5 (`rwb_asset`) | The paginated asset list with its filters and its paging elements | Read by the screens |
| The eviction element | S5 (`rwb_asset`) | The occupancy state, the eviction status and the instruction reference, each declared with its type and its source; the column each occupies is Not specified in the source documents (GAP-2892; ASM-4789) | Written by the application story |
| The case elements of the signal and the answer | P3 (`rwb_case`) | The case reference, the case state and the move with its rule id and rule version; referenced, not redefined | Consumed and answered |
| The asset facts of the ACE product | P1 (`rwb_source_data`) | The asset reference, its type, its transfer-in type and its book value; referenced, not redefined | Consumed through the owner's contract |
| The decision-record elements | PLT library, created in `rwb_asset` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time (DF-DEC-001 to DF-DEC-018) | Written through the library |

The baseline declares no new table, no new column and no migration, and it enumerates no business value: every list, code and threshold is referenced with its identifier and its version. **No personal data** appears in any element, fake or example; the fixture identifiers are synthetic and no occupant is identified.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). These are the reads that answer SCR-21 and SCR-22 for this step and carry the eviction element; the step's own surface is the stage signal and the case-move answer.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, its holding status and its eviction element (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |
| None | The step's own operation | No ownership row and no other source names a published operation for the eviction; it is Not specified in the source documents (GAP-2892; ASM-4789) and is not declared as a path here | Not applicable | Not applicable |

The other ownership rows are read as published and not declared here: `GET /assets/{assetKey}` is the same read addressed by the ACE asset business key, and `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds` are the pricing and auction stories' of this service. The error envelope of the two reads: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for an invalid filter, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state the step checks before a rule fires; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2893; ASM-4790)) | rwb-case (P3) | P3 rwb-case | The answer that carries the move `EVICTION_REQUIRED`, the instruction reference, the rule id and the rule version; on the workflow boundary it is the outcome the parent applies; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag rather than inventing a surface (BR2). No operation of rwb-litigation is consumed: the instruction reaches Legal through the case, which is the boundary of Architecture v5 slide 13 and not a call of this service (GAP-2893).

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset exactly two events, `AssetTakenOn` and `AssetSold`; the take-on story publishes the first and the sale story the second, and this baseline declares neither as its own and adds nothing to `rwb.asset.events.v1`. The step's outward surface is the case-move answer and its own two reads, and no outbox row is declared here.

#### 12.4 Events consumed

None. The occupancy refusal and the possession result reach the step as stage signals through the case router of rwb-case (Architecture v5 slide 13), and this service subscribes to no topic for this step. No source names an eviction or possession event for this service, and none is declared (GAP-2893; ASM-4790). The litigation and auction feeds this service listens to belong to the auction and litigation-result stories and are not part of this baseline.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference and the rule package in force; signals: the occupancy fact, the possession result and the rule package in force |
| `openEviction` | Activity, the eviction step | `rwb-asset` | The case, the asset and the occupancy fact in; the rule ID with its version, the eviction status, the instruction reference and the stage outcome out, in one transaction |

The workflow is the same execution the take-on and holding stories use; this baseline fixes its input and signal elements and the one activity it adds, and it declares no child workflow and no second queue. The activity name is a design choice of the application story, and the baseline carries it so that the workflow's history is stable.

#### 12.6 Schedules

None. The step runs from the stage signal the parent forwards, and this baseline declares no Temporal Schedule and no legacy Quartz job. The single Schedule of the service, JOB-19 Re-appraisal monthly, belongs to RWB-S5-E3026-APP and is not declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`) | The held asset; the baseline declares the elements of its eviction state, not its schema |
| decision_record | PLT library, created in `rwb_asset` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| inbox_event | PLT library, created in `rwb_asset` | The row of the forwarded fact and its dedupe key (DP-09) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated fact and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `partner_instruction` (not S5's), `template` (P6), `deviation` (S8), `document` and `document_custody` (P5), `proceeds` (P8) and every `v_ace_*` view (P1) are named by their owner and never declared here. The eviction element's columns are Not specified in the source documents and are declared only once their owner names them (GAP-2892; ASM-4789).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case stage-signal fake | The occupancy fact of case `RC-2026-000521` and asset `AST-2026-000521`; the same fact twice; the possession result; a fact without an occupancy status | C3, C4, C6 |
| rwb-case case-state and case-move fake | The case state of `RC-2026-000521`; the move accepted with its instruction reference and the move refused for a state the rule does not expect | C3, C4, C6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-13 | C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000521`, with the asset and its eviction element read once | C2, C6 |
| The eviction element fake | The occupancy state, the eviction status and the instruction reference, and a variant with the field absent | C2, C4 |

Each fake answers only what its owner documents, and a fake that answers more than the document fails the review. The element names that are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2892, GAP-2893; ASM-4789, ASM-4790).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | Nothing published and nothing subscribed; the facts arrive as stage signals |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and `openEviction` on `rwb-asset`; no Schedule |
| File | None | No file element is declared |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4021 CON Evict occupants from a held property - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S5-E4021.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the two provided operations, the two consumed rows, the published and consumed events, the workflow and its activity, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Fakes.** One fake per consumed row plus the composite route and the eviction element, each built from the document and not from the real service, so that the fake can be published before the owner's build finishes (C6).

**Done when.** The seven criteria pass, the reviewers of the two consumed owners have closed their comments, the compatibility check passes on the tag, the fakes are published with their documented answers, and RWB-S5-E4021-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Asset and disposal right calls one of the declared reads | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of a declared request or of the signal is absent or invalid | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row or an element has no published name | Not specified in the source documents (GAP-2893; ASM-4790). |

The three message IDs are carried from the service and platform sets and are declared only as the envelope rows of the operations in this baseline; the two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-21 Asset list and SCR-22 Asset record through the gateway-bff composite route (DP-19). What this story fixes is the element list of the two asset reads — including the eviction element — and the empty, loading, refused and held states the route can show from this service's answers. The route itself, its merge order and its field list are RWB-PLT-N001-CON, and the screens' transitions are the application stories'.

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The legacy screen list gives SCR-22 four states and no eviction state, so the eviction state's name and presentation are Not specified in the source documents and the element is declared without them (GAP-2892; ASM-4789).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-021-01 | C1, C2: the schema and the elements the step's answers carry | Contract | The published schema and the recorded asset answers of case `RC-2026-000521` |
| TC-E4-021-02 | C2, C5: the elements, the closed lists and the rights of the declared reads | Contract | The element list and one request per declared right, including a role without it |
| TC-E4-021-03 | C3, C4: the stage signal, the case-move answer and the consumed rows | Contract | The two consumed rows, the signal and the answer, each once and twice, with and without a published name |
| TC-E4-021-04 | C5: the error envelope of the two declared reads | Contract | One request per error code, 400, 401, 403, 404, 422 and 503 |
| TC-E4-021-05 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |
| TC-S5-E4021-CON-01 | C4: the placeholder and gap of the eviction element and of the unpublished operation names | Contract | The eviction element with and without a named column; the two consumed rows with and without a published name |
| TC-S5-E4021-CON-02 | C6: the fakes and the decision-record element | Contract | The six fakes, the stopped stub and one fake that answers more than its document |
| TC-S5-E4021-CON-03 | C7: the naming and boundary rule | Contract | The base, the topic, the queue and the schema, plus a draft that names a foreign schema, a monolith base, a Schedule or a subscription |
| TC-S5-E4021-CON-04 | C3, C7: no event published and no subscription declared | Contract | The outbox declaration, empty; no topic of another owner declared as consumed |

The five legacy case IDs are mapped onto this contract deliverable in their legacy order, and their `Covers` names the criterion of this story that fixes the surface each legacy case touches: the eviction and the case answer (01), the rule elements and the rights (02), the signal and the consumed rows (03), the failure and error path (04) and the schema's compatibility (05). The four `TC-S5-E4021-CON-` cases are new and test the parts of the baseline that no legacy case touches: the placeholder rule, the fakes, the naming boundary and the absence of a published event. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the baseline: the occupancy statuses, the eviction statuses, the instruction period and every threshold are referenced with their identifier and version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, statuses and a rule version only, no occupant is identified, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the asset facts appear only as the rwb-source-data product and the service's own `asset` row (DP-05).
- The case stays with rwb-case and the legal act with rwb-litigation: no `recovery_case` element and no instruction operation of another owner is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Schedule, no event published and no subscription by this step.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-006 to REQ-S5-010 | The five requirements TSD S5 T8 maps to FEAT-AST-08; the split plan carries no requirement row for this contract slice, so the trace rests on the module requirement (GAP-2894; ASM-4791) | The baseline, its consumed rows and its fakes | TC-S5-E4021-CON-01, TC-S5-E4021-CON-02 |
| ADR-013 | 19 services inside ACE | The baseline's ownership rows | TC-S5-E4021-CON-03 |
| ADR-014 | Schema and login per service | `rwb_asset` and the declared tables | TC-S5-E4021-CON-03 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | No subscription and no publication; the declared absence | TC-S5-E4021-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows, the compatibility check | TC-E4-021-03, TC-E4-021-05 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its library | TC-S5-E4021-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-021, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 are carried by RWB-S5-E4021-APP; this story carries no legacy criterion and tests the surface they touch |
| Test cases | TC-E4-021-01 to TC-E4-021-05 at Level Contract, and TC-S5-E4021-CON-01 to TC-S5-E4021-CON-04 |
| Feature and screens | FEAT-AST-08, SCR-21 Asset list and SCR-22 Asset record, read through the composite route |
| Rules | R-DIS-13, referenced as a rule-package row and not evaluated here |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The eviction behaviour, the rule evaluation, the eviction record, the decision records and the case move: RWB-S5-E4021-APP.
- The case of record, its route states and the parent workflow: rwb-case (P3).
- The legal act, its deadlines and its outcome: rwb-litigation (S4).
- The ACE asset facts and the freshness of the data product: rwb-source-data (P1).
- The rule package, its version and its approval: rwb-decision (P7).
- The pricing and auction operations of this service and their shapes: the pricing and auction stories and their contracts.
- The composite route, its merge order and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
