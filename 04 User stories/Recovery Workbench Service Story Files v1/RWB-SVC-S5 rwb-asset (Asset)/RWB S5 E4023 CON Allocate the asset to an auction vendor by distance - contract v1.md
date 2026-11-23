# RWB-S5-E4023-CON Allocate the asset to an auction vendor by distance - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4023-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-023 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-023, the baseline the vendor-allocation step of rwb-asset builds against on Day 1. The baseline declares the two asset reads that answer SCR-21 and SCR-23 on `/api/recovery/asset/v1` (DP-13), the three consumed REST rows of rwb-case and rwb-source-data (DP-05), the vendor-panel activity element of rwb-partner on the call type the connection matrix gives S5→S9, the workflow signal elements `VENDOR_REQUIRED` and `VENDOR_UNAVAILABLE`, the decision-record element of DP-03, the rights and the error envelope, and the fakes. No event is published or consumed, and no Schedule is declared. No source names a published operation for the allocation step itself, and the panel element of the partner activity, the four-vendor list and the allocation reference have no published field (GAP-2905; ASM-4803); the split plan carries no requirement id for this slice (GAP-2903; ASM-4801). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the vendor-allocation step of rwb-asset — its two asset reads, its consumed rows, its two workflow signals, its panel element, its rights, its error envelope and its fakes — baselined and tagged before the build starts**, so that **the application story, the pricing and auction stories and every consumer can build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-023. It owns:

- the document that fixes the two reads of the asset and its allocation on base `/api/recovery/asset/v1`, with their parameters, their documented answer, their rights and their idempotency (DP-13);
- the three consumed REST rows: the rwb-case case state read, the rwb-case case-move answer and the rwb-source-data asset and scorecard data product, each with its owner, its use and its placeholder where the operation name is not published (DP-05);
- the vendor-panel element of the rwb-partner activity on queue `rwb-partner`, the call type the connection matrix gives S5→S9, with its request, its documented answer and its timeout;
- the two workflow signal elements, `VENDOR_REQUIRED` at `FLOOR_APPROVED` and `VENDOR_UNAVAILABLE` at `VENDOR_ALLOCATED`, with the fields the rules R-DIS-30 and R-DIS-31 test;
- the decision-record element and the local library dependency that carries it (DP-03);
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, so that every downstream answer has a stub on Day 1;
- the naming and boundary rules of the baseline: one base, one topic, one queue, no foreign schema, no monolith base, no consumed event, no Schedule.

It does not own: the allocation behaviour, the rule evaluation, the decision records and the case moves, which are RWB-S5-E4023-APP; the panel, its capacity, its panel status and the partner instruction, which are rwb-partner's (S9); the case of record and its route states, which are rwb-case's (P3); the ACE asset and scorecard facts, which are rwb-source-data's (P1); the rule package, which is rwb-decision's (P7); the listing, the floor price and the auction rounds, which are the pricing and auction stories of this service; the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

### 2. Business rationale

A contract baseline is what lets ten teams build at once. Without it the allocation step would be written against whatever shape the partner panel or the data product happened to expose that week, and the first integration would find the mismatches instead of the review. With it, the application story builds on Day 1 against a tagged document and its fakes, the listing stories know what the asset answer must carry for the allocation to be shown, and rwb-partner and rwb-source-data see exactly which facts of theirs this service consumes.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner and its use, and where the source documents do not publish an operation name, a field or a list value, the row carries the placeholder rather than an invented surface (GAP-2905; ASM-4803).
- **the call type is the matrix's.** The panel is reached by a Temporal activity on the owner's queue and not by REST, because the connection matrix gives S5→S9 a Temporal call only and the architecture notes say route services reach shared capabilities through Temporal, never REST (Architecture v5 slide 13).
- **additive only.** The baseline moves forward without breaking: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version and a new document (s9).

The business outcome the baseline protects is the one FEAT-AST-14 of the FSD names: one of the four vendors is chosen by the rule so that the NPA sales cycle shortens. The baseline does not state that outcome, and no criterion here asserts a business value or a chosen vendor.

### 3. Preconditions

- The ownership rows are in force: S5 owns the six operations of the Ownership Map, of which `GET /assets` and `GET /assets/{assetId}` are declared here; `POST /assets/{assetId}/valuations` is rwb-valuation's under ASM-0043; `POST /assets/{assetId}/listings` and `POST /listings/{listingId}/rounds` are the listing and auction stories' (API-S5-004, API-S5-005); `asset_sale` and `listing` are S5's tables (GAP-2905; ASM-4803).
- The service naming is fixed: schema `rwb_asset`, login `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with `.retry` and `.dlt`, task queue `rwb-asset` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.asset`.
- Architecture v5 slides 13 and 19 are in force: S5→S9 is a Temporal call and an event subscription, and rwb-asset publishes `AssetTakenOn` and `AssetSold` only; this baseline touches neither event.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19).
- The rwb-partner (S9) vendor-panel activity is declared by its owner as reachable on that owner's queue; where the owner has not published it, the fake carries its documented answer and the row keeps its placeholder (GAP-2901; ASM-4799).
- No approval is needed to publish a Draft baseline, and the missing approval of the realigned stories is recorded rather than waited for (GAP-2904; ASM-4802); the document is baselined by this story's own review, and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the ownership rows, Architecture v5 slides 13 and 19, the TSD S5 T-A.1 operations and the TSD S5 T3.1 tables.
2. Every operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. Every consumed REST row is declared with its owner, its use, its budget and a placeholder where the operation name is not published.
4. The panel element is declared with the call type of the matrix, the request fields, the documented answer fields and the timeout.
5. The two workflow signals are declared with the fields the rules test: the case reference, the asset reference and, on the re-allocation, the allocated vendor with its capacity flag and its panel status.
6. The decision-record element is declared with the library dependency that carries it.
7. The fakes are declared with their documented answers, one per consumed row and one for the composite route.
8. The schema, the open lists and the closed lists are published, and the compatibility check runs: a breaking change fails the check.
9. The document goes to review as Draft; the reviewers are the owners of the consumed rows and the tech lead of the service.
10. On the review's close the document is tagged and baselined; the application story starts against the tag and the fakes.
11. A defect found in the build that needs a shape change is raised against this document, and the document moves to a new minor or major version; the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and the gap; no path, field or list value is invented | C4, C5 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails, the version becomes a new major and the document is re-reviewed | C1 |
| X3 | A declared operation or activity reaches another service's data, base or queue as its own | The review refuses the baseline and the boundary test fails the build | C2, C7 |
| X4 | A consumed row or the panel activity has no fake, or its fake has no documented answer | The baseline is not tagged; the application story cannot start | C6 |
| X5 | The rights of an operation are not one of the rows of the access matrix, or a right is widened | The operation is not declared and the error set of the operation is incomplete | C3 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a new version, this document follows with a minor or major version, and the application story re-tests against the new fake | X2, s9 |
| X7 | Two documents claim the same path, queue, table or event | The naming and boundary rule resolves it: the owner named in the ownership rows keeps it, and the other document changes | C7 |

X1 to X3 are the paths of an incomplete or a leaking source, X4 to X6 are the paths of a baseline moving under a build, and X7 is the naming boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the order of the sections and the fake data are this story's choice; the paths, the owners, the queue, the signals and the error set are fixed by their sources |
| Valuable | Ten teams build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, two provided operations, three consumed rows, one panel element, two signals, one library element, seven fakes and one compatibility check |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the vendor-allocation step

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema and the open and closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The two declared reads carry their elements, their rights and their error envelope (new, D-RCV-60)
    Given the operations the baseline provides on base /api/recovery/asset/v1
    When the element list, the rights and the error set of each operation are read
    Then each element carries its type, its nullability and its source
    And each operation names the capability area and the right of the access matrix, and the error set names 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 in one problem envelope

  Scenario: C3 The three consumed REST rows name their owners, their use and their budget (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-case and rwb-source-data are read
    Then each row names its owner, its use and its 2 s budget
    And where the operation name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C4 The vendor-panel element is declared on the call type of the matrix (new, D-RCV-60)
    Given the consumed activity table of the baseline
    When the vendor-panel row is read
    Then it names queue rwb-partner, the request fields of the asset and the documented answer fields of the four vendors with their capacity, their panel status and their distance
    And it declares no REST path of rwb-partner and no table of another service
    And where a field is not published the row carries the placeholder and the gap identifier

  Scenario: C5 The two workflow signals carry the fields the rules test (new, D-RCV-60)
    Given the workflow element table of the baseline
    When the signals VENDOR_REQUIRED and VENDOR_UNAVAILABLE are read
    Then VENDOR_REQUIRED carries the case and asset references and the rule package in force at FLOOR_APPROVED
    And VENDOR_UNAVAILABLE carries the case reference and the allocated vendor with its capacity flag and its panel status at VENDOR_ALLOCATED
    And the closed lists of the capacity flag and the panel status are referenced with their identifier and version and are not enumerated in code

  Scenario: C6 The decision-record element and the fakes are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element and the fake table are read
    Then the element names RWB-PLT-E1027-CON as its library and the transaction it joins
    And every consumed row and the panel activity have a fake with a documented answer, including the stopped decision-record stub

  Scenario: C7 The naming and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queues and the schema of the baseline
    When the document is checked against the naming rule and the ownership rows
    Then no foreign schema, no foreign topic and no monolith base /api/recovery/v1 is declared
    And no Schedule is declared, no event is published and none is consumed by this step
```

The seven criteria are new to this run and are tagged as such: they test the contract deliverable only — the schema, the elements, the consumed rows, the panel element, the two signals, the rights, the envelope, the decision-record element, the fakes and the boundary. No criterion states a business outcome or a business value of the application story, and none asserts that a rule fires, that a vendor is chosen or that a case moves.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, activity, event and table: the baseline declares only the rows the ownership rows and Architecture v5 give to S5, and names every other row with its owner | Ownership rows of S5; Architecture v5 slide 13 |
| BR2 | A consumed row, a field or a list value with no published name carries the placeholder and its gap, and never an invented surface | Template and Rules v1 §R9; GAP-2905 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; s9 |
| BR4 | The panel is reached by a Temporal activity on queue `rwb-partner` and never by REST or a table, because the connection matrix gives S5→S9 a Temporal call only | Architecture v5 slide 13 and its notes |
| BR5 | Every consumed REST row is one hop with a 2 s timeout, a breaker and no chain, and the panel activity carries the workflow kit's timeout | ADR-020 |
| BR6 | The step publishes no event and consumes none: the topic `rwb.asset.events.v1` carries `AssetTakenOn` (EV-22) and `AssetSold`, and the two triggers are workflow signals | Architecture v5 slide 19; TSD S5 T5.3 |
| BR7 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before the case-move answer, and its element is declared once for the service | DP-03 |
| BR8 | No business value is declared in the baseline: the panel size, the capacity codes, the panel statuses and every threshold are referenced with their identifier and version | Template and Rules v1 §R7.2 (s16); legacy Guardrails |
| BR9 | No personal data in any element, fake or example of the baseline | Template and Rules v1 §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation, queue or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

### 9. State transitions

The document itself is the object of this section: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, row, element, signal, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the consumed rows are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | New optional element only, compatibility check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer | X6 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row or a panel field has no published name | X1 | The row carries the placeholder and the gap and the draft continues |
| In review | A row reaches a foreign schema, base or queue | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row or the panel activity has no fake | X4 | Not tagged, the review reopens |

The route states `FLOOR_APPROVED` and `VENDOR_ALLOCATED` of the rules appear in this document only as the from-state and to-state of the two declared signals; their transitions belong to rwb-case and to RWB-S5-E4023-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Authors the baseline, resolves the shape of the service's own operations and signals and signs the tag |
| Owner of rwb-case (P3) | Reviews the case state and case-move rows and publishes the operation names when they exist |
| Owner of rwb-source-data (P1) | Reviews the asset and scorecard data-product row and its freshness stamp |
| Owner of rwb-partner (S9) | Reviews the vendor-panel activity element and publishes its name and its answer fields |
| Owner of rwb-decision (P7) | Reviews the rule package reference and the decision-record element with the platform library |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the rights of each declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The asset answer of `GET /assets/{assetId}` | S5 (`rwb_asset`) | The asset of status 200 with its type, its transfer-in type, its book value and its allocation, the chosen vendor and the basis | Read by the screens; the allocation facts are written by the application story |
| The asset page of `GET /assets` | S5 (`rwb_asset`) | The paginated asset list with its filters and its paging elements | Read by the screens |
| The allocation element | S5 (`rwb_asset`) | The vendor reference, the basis and the distance; Not specified in the source documents (GAP-2902; ASM-4800) for the column it occupies, so the element is declared only as a decision-record fact and the read answers it where the record holds it | Written by the application story as a record fact |
| The asset elements of the data product | P1 (`rwb_source_data`) | The asset reference, its type, its transfer-in type, its book value and the freshness stamp; referenced, not redefined | Consumed |
| The scorecard elements of the data product | P1 (`rwb_source_data`) | The predicted price of each vendor with its model code and its version; referenced, not redefined | Consumed |
| The case elements of the consumed read | P3 (`rwb_case`) | The case reference and the case state; referenced, not redefined | Consumed |
| The vendor-panel elements | S9 (`rwb_partner`) | The four vendors with their capacity flag, their panel status and their distance; referenced, not redefined; the field names are Not specified in the source documents (GAP-2901; ASM-4799) | Consumed |
| The decision-record elements | PLT library, created in `rwb_asset` | The rule id, the rule version, the inputs reference, the chosen vendor, the basis, the outcome and the decided-at time (DF-DEC-001 to DF-DEC-018) | Written through the library |

The baseline declares no new table, no new column and no migration, and it enumerates no business value: every list, code and threshold is referenced with its identifier and its version. **No personal data** appears in any element, fake or example; the fixture identifiers are synthetic and the fixture data of the contract tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). These are the reads that answer SCR-21 and SCR-23 for this step; the step's own surface is the two workflow signals and the case-move answer.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its type, its book value, its allocation, the chosen vendor and the basis (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |
| None | The step's own operation | No source names a published operation for the allocation step; it is Not specified in the source documents (GAP-2905; ASM-4803) and is not declared as a path here | Not applicable | Not applicable |

The legacy endpoint row `POST assets/{assetId}/listings` of this key (written in the monolith on base `/api/recovery/v1`) becomes `POST /assets/{assetId}/listings` (API-S5-004) in the target and is declared by the listing and pricing baseline of this service, not by this one, because the allocation step creates no listing; `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's under ASM-0043.

The error envelope of the two reads: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for an invalid filter, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state the rule checks before it fires; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2905; ASM-4803)) | rwb-case (P3) | P3 rwb-case | The answer that carries `VENDOR_ALLOCATED` with the rule, the vendor reference and its version; on the workflow boundary it is the stage outcome the parent applies; faked |
| The asset and scorecard data product (operation name Not specified in the source documents (GAP-2905; ASM-4803)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset fact and the predicted price of each vendor with its model version, and the freshness stamp; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag rather than inventing a surface (BR2).

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset exactly two events, `AssetTakenOn` (EV-22) and `AssetSold`; the take-on is the take-on story's and the sale the sale story's, and this baseline declares neither as its own and adds nothing to `rwb.asset.events.v1`. The step's outward surface is the case-move answer and its own two reads, and no outbox row is declared here.

#### 12.4 Events consumed

None. No source gives the allocation step a Kafka event: the four events Architecture v5 slide 19 IN gives rwb-asset (`JudgmentRecorded`, `AuctionResult`, `ProceedsMatched`, `PartnerResultSubmitted`) serve the litigation, auction, proceeds and partner-result steps, and the two triggers of this step are signals of the DISPOSAL machine forwarded by the parent `CaseWorkflow`. The baseline therefore declares no consumer group, no inbox row and no dedupe key for this step, and DP-09 is held as a prohibition (GAP-2901; ASM-4798).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference and the rule package in force; signals: `VENDOR_REQUIRED`, `VENDOR_UNAVAILABLE` and the rule package in force |
| `allocateVendor` | Activity, the vendor-allocation step | `rwb-asset` | The case and the asset reference in; the chosen vendor, the basis, the score, the rule IDs with their versions and the stage outcome out, in one transaction |
| The rwb-partner vendor-panel activity (name Not specified in the source documents (GAP-2901; ASM-4799)) | Activity on the owner's queue, called by this step | `rwb-partner` | The asset reference, its region and its type in; the four vendors with their capacity flag, their panel status and their distance out; one call per evaluation, no child workflow and no Nexus |

The workflow is the same execution the take-on and holding stories use; this baseline fixes its input, its two signals and the two activities it adds, and it declares no child workflow and no second queue of this service. The activity names are design choices of the application story and of rwb-partner, and the baseline carries them so that the workflow's history is stable.

#### 12.6 Schedules

None. The step runs from the signals the parent forwards, and this baseline declares no Temporal Schedule and no legacy Quartz job. The single Schedule of the service, JOB-19 Re-appraisal monthly, belongs to the re-appraisal story of this service and is not declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| decision_record | PLT library, created in `rwb_asset` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON and holding the chosen vendor, the basis and the score |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated signal and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case` and `assignment` (P3), `decision_log_entry` and `rule_row` (P7), `proceeds` (P8), the vendor panel (S9), every `v_ace_*` view (P1) and `asset_sale` and `listing` — which are this service's but not this step's — are named by their owner and never declared here. The allocation's column is Not specified in the source documents and is declared only once its owner names it (GAP-2902; ASM-4800).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data asset and score data-product fake | The asset `AST-2026-000623` with its type and book value and the predicted price of each vendor with its model version; a stale product with its date; no answer beyond 2 s | C3, C4, C6 |
| rwb-case case-state and case-move fake | The case state of `RC-2026-000623`; the move accepted and the move refused for a state the rule does not expect | C2, C3, C6 |
| rwb-partner vendor-panel fake | The four vendors with their capacity flag, their panel status and their distance; a panel where every vendor is unavailable; an activity that fails | C4, C6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-30 and R-DIS-31 and the panel and capacity reference rows | C5, C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for case `RC-2026-000623`, with the asset and its allocation read once | C2, C6 |

Each fake answers only what its owner documents, and a fake that answers more than the document fails the review. The operation names and the panel field names that are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2901, GAP-2905; ASM-4799, ASM-4803).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-case state row and the case-move row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step and no consumer group; the two triggers are workflow signals |
| Temporal | 1 workflow, 1 owned activity, 1 partner activity | `AssetDisposalWorkflow`, `allocateVendor` and the rwb-partner vendor-panel activity; no Schedule |
| File | None | No file element is declared |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4023 CON Allocate the asset to an auction vendor by distance - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S5-E4023.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the two provided operations, the three consumed rows, the panel element, the two signals, the published and consumed events, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Fakes.** One fake per consumed row plus the panel activity and the composite route, each built from the document and not from the real service, so that the fake can be published before the owner's build finishes (C6).

**Done when.** The seven criteria pass, the reviewers of the three consumed owners and of the panel have closed their comments, the compatibility check passes on the tag, the fakes are published with their documented answers, and RWB-S5-E4023-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Asset and disposal right calls one of the declared reads | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of a declared request or of a signal is absent or invalid | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The declared data product is stale and the step declares that it holds | {product} is from {date}. Today's ACE batch has not arrived. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row or a panel field has no published name | Not specified in the source documents (GAP-2905; ASM-4803). |

The four message IDs are carried from the service and platform sets and are declared only as the envelope and element rows of the operations in this baseline; the two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-21 Asset list and SCR-23 Listing and price through the gateway-bff composite route (DP-19). What this story fixes is the element list of the two asset reads, including the allocation element, and the empty, loading, refused, stale and held states the route can show from this service's answers.

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The draft, below-limit, approved and published states of SCR-23 belong to the pricing and listing story, and the route itself, its merge order and its field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-023-01 | C1, C2: the schema and the elements the asset answers carry, including the allocation element | Contract | The published schema and the recorded asset answers of case `RC-2026-000623` |
| TC-E4-023-02 | C2, C3: the rights and the consumed rows of rwb-case and rwb-source-data | Contract | One request per declared right, including a role without it, and the three consumed rows with and without a published name |
| TC-E4-023-03 | C4: the vendor-panel element and its call type | Contract | The panel request and answer, once with published field names and once with the placeholder; a declared REST path for rwb-partner that must fail the review |
| TC-E4-023-04 | C5: the two workflow signals and their fields | Contract | `VENDOR_REQUIRED` at `FLOOR_APPROVED` and `VENDOR_UNAVAILABLE` at `VENDOR_ALLOCATED`, each with and without the capacity flag and the panel status |
| TC-E4-023-05 | C2: the error envelope of the two declared reads | Contract | One request per error code, 400, 401, 403, 404, 422 and 503 |
| TC-E4-023-06 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |
| TC-S5-E4023-CON-01 | C3, C4: the placeholder and gap of an unpublished operation name, panel field and list value | Contract | The three consumed rows and the panel element, each with and without a published name |
| TC-S5-E4023-CON-02 | C6: the fakes and the decision-record element | Contract | The six fakes, the stopped stub and one fake that answers more than its document |
| TC-S5-E4023-CON-03 | C7: the naming and boundary rule | Contract | The base, the topic, the two queues and the schema, plus a draft that names a foreign schema, a monolith base or a Schedule |
| TC-S5-E4023-CON-04 | C7: no event published and none consumed | Contract | The outbox declaration, empty; the consumed-event table, empty; a draft that adds a consumer group |

The six legacy case IDs are mapped onto this contract deliverable in their legacy order, and their `Covers` names the criterion of this story that fixes the surface each legacy case touches: the asset answer and the allocation element (01), the rights and the consumed rows (02), the panel element (03), the signal fields (04), the error envelope (05) and the compatibility check (06). The four `TC-S5-E4023-CON-` cases are new and test the parts of the baseline that no legacy case touches: the placeholder rule, the fakes, the naming boundary and the absence of published and consumed events. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the baseline: the panel size, the capacity codes, the panel statuses, the score rules and every threshold are referenced with their identifier and version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, a score, a basis, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the asset and scorecard facts appear only as the rwb-source-data data product (DP-05).
- The panel stays with rwb-partner and the case with rwb-case: no panel element, no case row and no assignment row is declared as this service's own, and the panel is a Temporal activity and never a REST path or a table (BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base, topic or queue as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Schedule, no consumed event and no outbox row.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id for this slice and no requirement of the module names vendor allocation; the requirement the baseline serves is FEAT-AST-14 of the FSD S5 A2.14, that one of the four vendors is chosen by the rule so that the NPA sales cycle shortens (GAP-2903; ASM-4801) | The baseline, its consumed rows and its fakes | TC-S5-E4023-CON-01, TC-S5-E4023-CON-02 |
| ADR-013 | 19 services inside ACE | The baseline's ownership rows | TC-S5-E4023-CON-03 |
| ADR-014 | Schema and login per service | `rwb_asset` and the declared tables | TC-S5-E4023-CON-03 |
| ADR-016 | Reusable Temporal layer | The two signals and the partner activity element | TC-E4-023-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows, the compatibility check | TC-E4-023-02, TC-E4-023-06 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its library | TC-S5-E4023-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-023, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 are carried by RWB-S5-E4023-APP; this story carries no legacy criterion and tests the surface they touch |
| Test cases | TC-E4-023-01 to TC-E4-023-06 at Level Contract, and TC-S5-E4023-CON-01 to TC-S5-E4023-CON-04 |
| Feature and screens | FEAT-AST-14, SCR-21 Asset list and SCR-23 Listing and price, read through the composite route |
| Rules | R-DIS-30 and R-DIS-31, referenced as rule-package rows and not evaluated here |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The allocation behaviour, the rule evaluation, the decision records and the case moves: RWB-S5-E4023-APP.
- The vendor panel, its capacity, its panel status, its distance, the partner instruction and the vendor scorecard: rwb-partner (S9) (GAP-2901; ASM-4799).
- The case of record, its route states and the parent workflow: rwb-case (P3).
- The asset and scorecard facts of ACE and the freshness of the data product: rwb-source-data (P1).
- The rule package, its version and its approval: rwb-decision (P7).
- The floor price, the listing and the auction rounds: the pricing, listing and auction stories of this service, API-S5-004 and API-S5-005.
- The composite route, its merge order and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
