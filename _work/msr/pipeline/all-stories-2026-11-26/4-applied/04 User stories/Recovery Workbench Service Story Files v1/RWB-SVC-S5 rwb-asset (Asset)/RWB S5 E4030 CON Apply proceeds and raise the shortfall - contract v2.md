# RWB-S5-E4030-CON Apply proceeds and raise the shortfall - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4030-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-030 |
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

**Change log.** D-RCV-60, 23 November 2026: the contract slice of RWB-E4-030, the baseline the proceeds-and-shortfall branch of rwb-asset builds against on Day 1. The baseline declares the two asset reads that answer SCR-21 and SCR-22 on `/api/recovery/asset/v1` (DP-13), the four consumed rows of rwb-case, rwb-payment and rwb-source-data (DP-05), the `ProceedsMatched` subscription on `rwb.payment.events.v1`, the decision-record element of DP-03, the rule-package element the branch evaluates, the rights, the error envelope and the fakes. No write operation and no published event are declared, because the step runs unattended and the service's owned event EV-22 `AssetTakenOn` belongs to the take-on story. Gaps: the consumed names are not published and no C row exists (GAP-2944; ASM-4840); EV-25's consumer list does not name this service (GAP-2945; ASM-4841); no S5-to-P1 edge exists for the two ACE facts (GAP-2946; ASM-4842); no element holds the residual (GAP-2947; ASM-4843); the balance application is FEAT-PAY-10's (GAP-2948; ASM-4844); the vendor fee has no element here (GAP-2949; ASM-4845); five adjacent rules own no legacy criterion (GAP-2950; ASM-4846); no requirement id (GAP-2951; ASM-4847); the screen states do not match the lists (GAP-2952; ASM-4848); DP-09 and DP-04 sit outside the pattern set (GAP-2953; ASM-4849). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4030-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the proceeds-and-shortfall capability of rwb-asset — its two reads, its one consumed event, its consumed operation rows, its decision-record and rule-package elements, its rights, its error envelope and its fakes — baselined and tagged before the build starts**, so that **the application story and every consumer of the sale outcome build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-030. It owns:

- the document that fixes `GET /assets` and `GET /assets/{assetId}` on base `/api/recovery/asset/v1`, with their parameters, their documented answer, their rights and their idempotency (DP-13);
- the subscription: EV-25 `ProceedsMatched` on `rwb.payment.events.v1` as `rwb.payment.ProceedsMatched.v1`, its CloudEvents envelope, its consumer group, its inbox row, its retry and `.dlt` topics and its dedupe;
- the four consumed rows: the rwb-case case-state read and case-move answer, the rwb-payment proceeds-fact activity and the rwb-source-data data product, each with its owner, its use and its placeholder where the name is not published (DP-05);
- the decision-record element and the library that carries it (DP-03);
- the rule-package element: the DISPOSAL package, its version and the two rows this branch evaluates, declared as a reference and not as a rule table of this service;
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, one per consumed row and one for the event;
- the naming and boundary rules: one base, one topic, one queue, no foreign schema, no monolith base, no Schedule for an event-started step.

It does not own: the branch behaviour, the rule evaluation, the sale write, the records and the case moves, which are RWB-S5-E4030-APP; the sale and its award, FEAT-AST-18 to FEAT-AST-20's stories; the balance application and the posting, which are FEAT-PAY-10 of rwb-payment (P8) (GAP-2948); the case of record and its states, rwb-case's (P3); the ACE facts, rwb-source-data's (P1); the rule package, rwb-decision's (P7); the screen field list and the composite route, which are RWB-PLT-N001-CON.

### 2. Business rationale

A contract baseline is what lets the stories of a wave build at once. Without it the sale outcome would be written against whatever shape the payment service happened to publish that week, and the first integration would find the mismatches instead of the review. With it, the application story builds on Day 1 against a tagged document and its fakes, the sale, pricing and payment stories know what the sale and the residual must carry for the branch to run, and the consumers of the two reads know exactly which elements they can rely on.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row and the event name its owner, and where the sources do not publish a name the row carries the placeholder rather than an invented path (GAP-2944; GAP-2946).
- **one hop, one budget.** Every consumed row is a single hop or one activity with a 2 s timeout, a breaker and no chain, which is ADR-020 and what the application story's exception paths assume.
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document (C1).

The business outcome the baseline protects is the one FEAT-AST-21 of the FSD names: the sale money is applied and any residual is raised to the next decision. The baseline does not state that outcome, and no criterion here asserts a business value.

### 3. Preconditions

- The Ownership Map rows are in force: S5 owns `GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds`; `asset_sale` and `listing` are S5's tables.
- The naming is fixed: schema `rwb_asset`, login `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with `.retry` and `.dlt`, task queue `rwb-asset` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.asset` (Template and Rules v1 §R4).
- The published shapes of the declared reads are the API Specification v5: `AssetPage` and `Asset`, with the sale, the fee, the proceeds state and the residual named by the baseline (API-S5-001, API-S5-002).
- EV-25 `ProceedsMatched` is the event of Payments and posting on `rwb.payment.events.v1`, with an envelope, an event id and an idempotency key (Event and Messaging Design v5, EV-25; Template and Rules v1 §R4).
- The owned event of this service is EV-22 `AssetTakenOn`, the take-on story's; no event is published by this capability.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). DP-09 and DP-04 are outside the pattern set, so the inbox and the package load are declared as platform capabilities with no new H row (GAP-2953; ASM-4849).
- No approval is needed to publish a Draft baseline; the document is baselined by this story's own review and the build waits only for its tag (ASM-4850).

### 4. Flow

1. The author drafts the baseline from the Ownership Map, the TSD S5 T-A.1 operations, the TSD S5 T3.1 tables, the lists of T3.2 and the event catalogue.
2. Every read is declared with its method, path, request, documented answer, rights, idempotency and error set; no write operation is declared.
3. The one consumed event is declared with its topic, its event name, its envelope, its consumer group, its inbox row, its retry and `.dlt` topics and its dedupe rule.
4. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
5. The decision-record element is declared with the library that carries it, and the rule-package element with its owner, its version and the two rows the branch evaluates.
6. The fakes are declared with their documented answers, one per consumed row, one for the event, one for the composite route and one for the record chain.
7. The schema, the open and closed lists and the compatibility check are published; a breaking change fails the check.
8. The document goes to review as Draft; the reviewers are the owners of the consumed rows and the tech lead of the service.
9. On the review's close the document is tagged and baselined; the application story starts against the tag and the fakes. A defect that needs a shape change is raised against this document and the code never moves ahead of it.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and its gap; no path and no field is invented | C2, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails, the version becomes a new major and the document is re-reviewed | C1 |
| X3 | A declared read reaches another service's data or base | The review refuses the baseline and the boundary test fails the build | C3, C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C6 |
| X5 | The rights of a read are not one of the rows of the access matrix | The read is not declared and its error set is incomplete | C3, C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a new version, this document follows with a minor or major version and the fakes are re-cut | C1, C6 |
| X7 | The event and a consumed row claim different owners or topics | The owner in the Ownership Map keeps the topic and the row is corrected | C6, C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 the paths of a baseline moving under a build, and X7 the naming boundary of the event.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the order of the sections and the fake data are this story's choice; the paths, the owners, the base, the envelope, the error set and the element names are fixed by their sources |
| Valuable | The wave 3 stories build at once against one tagged surface and the first integration finds behaviour, not shape |
| Estimable | One document, two provided reads, one subscription, four consumed rows, two library elements, ten fakes and one compatibility check |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the proceeds-and-shortfall capability

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
    And the residual, its route and its D9 hand-off carry the placeholder and its gap identifier because no element holds them

  Scenario: C3 The two reads are declared with their rights and no write is declared (new, D-RCV-60)
    Given the operations the baseline provides on base /api/recovery/asset/v1
    When the method, path, documented answer, right and idempotency of each are read
    Then GET /assets and GET /assets/{assetId} carry the Asset and disposal right R with scope applied and no idempotency
    And no write operation is declared, because the step runs unattended inside the workflow
    And POST /assets/{assetId}/listings, POST /assets/{assetKey}/listings and POST /listings/{listingId}/rounds are named as other stories' and are not declared

  Scenario: C4 The consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-case, rwb-payment and rwb-source-data are read
    Then each row names its owner, its use and its 2 s budget
    And where the name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C5 The error envelope is declared per read (new, D-RCV-60)
    Given the operations the baseline provides
    When the error set and the rights of each read are read
    Then the error set names 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 in one problem envelope
    And the capability area and the right of each read are the rows of the access matrix
    And MSG-P7-003 is declared as the record-chain message and not as a message of a read

  Scenario: C6 The event, the decision-record, rule-package and fake elements are declared (new, D-RCV-60)
    Given the baseline document
    When the subscription, the decision-record element, the rule-package element and the fake table are read
    Then the subscription names EV-25 ProceedsMatched, the topic rwb.payment.events.v1, the event rwb.payment.ProceedsMatched.v1 and the consumer group rwb-asset with its inbox, retry and .dlt topics
    And the decision-record element names RWB-PLT-E1027-CON as its library and the transaction it joins
    And the rule-package element names the DISPOSAL package, its owner, its version in force and the two rules, and declares no rule row
    And every consumed row and the event have a fake with a documented answer, including the stopped stub, the stale proceeds fact, the unmatched fee and the repeated event

  Scenario: C7 The naming and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue and the schema of the baseline
    When the document is checked against the naming rule and the ownership map
    Then the base /api/recovery/asset/v1, the queue rwb-asset, the schema rwb_asset and the topic rwb.asset.events.v1 are the only ones declared as this service's own
    And rwb.payment.events.v1 is declared as consumed and never as this service's
    And no foreign schema, no foreign topic, no monolith base /api/recovery/v1 and no Schedule for an event-started step is declared
    And no event is published by this capability
```

The seven criteria are new to this run and are tagged as such: they test the contract deliverable only — the schema, the elements, the lists, the reads, the consumed rows, the rights, the envelope, the subscription, the two library elements, the fakes and the boundary. No criterion states a business outcome, and none asserts that a rule fires or that a case moves.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, event and table: the baseline declares only the rows the Ownership Map gives to S5 and names every other row with its owner | Ownership Map; Architecture v5 slide 41 |
| BR2 | A consumed row with no published name carries the placeholder and its gap, and never an invented path | Template and Rules v1 §R9; GAP-2944 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; C1 |
| BR4 | Every consumed row is one hop or one activity with a 2 s timeout, a breaker and no chain | ADR-020 |
| BR5 | Exactly one event is consumed and none is published: EV-25 `ProceedsMatched` is the proceeds fact and EV-22 `AssetTakenOn` is another story's | Event and Messaging Design v5 (EV-22, EV-25); Architecture v5 slide 13 |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR7 | The rule package is referenced, never redefined: the DISPOSAL package, its version and the two rules are rwb-decision's rows and no rule table of this service is declared | DP-04 (not claimed); GAP-2953 |
| BR8 | No business value is declared in the baseline: every list, code, amount and threshold is referenced with its identifier and version | Template and Rules v1 §R7.2 (s17); legacy Guardrails |
| BR9 | No personal data in any element, fake or example of the baseline; a buyer is a code, never a person | Template and Rules v1 §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

### 9. State transitions

The document itself is the object of this section: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every read, row, element, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the consumed rows are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | New optional element only, the check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer | X6 | Draft of a new minor or major version, and the fakes are re-cut |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name | X1 | The row carries the placeholder and the gap and the draft continues |
| In review | A read reaches a foreign schema, base or topic | X3 | The baseline is refused |
| Ready to tag | A consumed row or the event has no fake | X4 | Not tagged, the review reopens |
| Ready to tag | The event and a row disagree on the owner or the topic | X7 | The row is corrected and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Authors the baseline, fixes the shape of the service's own reads and signs the tag |
| Owner of rwb-case (P3) | Reviews the case-state and case-move rows and publishes the operation names when they exist |
| Owner of rwb-payment (P8) | Reviews the proceeds-fact row and the `ProceedsMatched` event, its envelope and its idempotency |
| Owner of rwb-source-data (P1) | Reviews the account and NPA-sale data-product row and publishes its shape when it exists |
| Owner of rwb-decision (P7) | Reviews the rule-package element, the DISPOSAL package version and the decision-record element with the platform library |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of each declared read |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The asset page of `GET /assets` | S5 (`rwb_asset`) | The paginated asset list with its filters, its paging elements, the sale and the proceeds state of each asset | Read by the screens |
| The asset answer of `GET /assets/{assetId}` | S5 (`rwb_asset`) | The asset of status 200 with its sale, its fee, its proceeds state and its residual | Read by the screens; written by the application story |
| The sale elements (DF-SAL-009 to DF-SAL-019) | S5 (`rwb_asset`) | id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee, the two taxes, gain_loss and incentive_amount, as the sale answer | Written by the application story |
| The listing elements (DF-SAL-001 to DF-SAL-008) | S5 (`rwb_asset`) | sale_channel, start_price, floor_price, round_no, listed_at and status, referenced with `LOV-SALE-CHANNEL` and `LOV-LISTING` | Read by the baseline |
| The residual, its route and its D9 hand-off | none | Not specified in the source documents for the element they occupy (GAP-2947; ASM-4843); declared only once an owner names it | Recorded with the outcome |
| The event elements of EV-25 `ProceedsMatched` | P8 (`rwb_payment`) | proceedsId, caseId and amount, with the event id, the idempotency key and the envelope version | Consumed |
| The payment elements of the consumed row | P8 (`rwb_payment`) | The proceeds, the vendor fee and the balance state, in place of the legacy `v_ace_account` read | Consumed |
| The case elements of the consumed read | P3 (`rwb_case`) | The case reference, the case state and the stage outcome; referenced, not redefined | Consumed |
| The account and NPA-sale elements of the consumed row | P1 (`rwb_source_data`) | The account balance and the NPA sale facts, in place of the legacy `v_ace_account` and `v_ace_npa_sale` reads | Consumed |
| The decision-record elements | PLT library, created in `rwb_asset` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time (DF-DEC-001 to DF-DEC-018) | Written through the library |
| The rule-package elements | P7 (`rwb_decision`) | The package name, its version and the two rows (DF-REF-001 to DF-REF-015) | Referenced only |

The baseline declares no new table, no new column and no migration, and it enumerates no business value. **No personal data** appears in any element, fake or example; the fixture identifiers are synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). These are the reads that answer SCR-21 and SCR-22.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the sale and the proceeds state of each asset (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its sale, its fee, its proceeds state and its residual (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

No write operation is declared: the step is event-started and unattended, and its writes belong to the `applyProceeds` activity. `POST /assets/{assetId}/listings` (API-S5-004) and `POST /listings/{listingId}/rounds` (API-S5-005) are the pricing and round stories' and `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's; the `{assetKey}` variants of the Ownership Map have no API Specification entry and are not declared. The error envelope: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for a missing or invalid parameter and 503 when the decision library or a consumed boundary does not answer, in one problem document with a code, a message ID and a correlation reference. The residual element of the asset answer carries its placeholder until its owner names it (GAP-2947; ASM-4843).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (activity on queue `rwb-case`) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state the rules check before they fire; faked |
| The case-move answer (name Not specified in the source documents (GAP-2944; ASM-4840)) | rwb-case (P3), Temporal | P3 rwb-case | The stage outcome with its rule version, applied by the parent; faked |
| The proceeds-fact activity (name Not specified in the source documents (GAP-2944; ASM-4840)) | queue `rwb-payment` | P8 rwb-payment | The proceeds, the vendor fee and the balance state, in place of the legacy `v_ace_account` read (DP-05); faked |
| The account and NPA-sale data product (name Not specified in the source documents (GAP-2946; ASM-4842)) | rwb-source-data (P1) | P1 rwb-source-data | The account balance and the NPA sale facts, in place of the legacy `v_ace_account` and `v_ace_npa_sale` reads (DP-05); faked |

Each row is one hop or one activity, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag rather than inventing a surface (BR2). The plan carries no C row for this pair; the legacy "Depends on FEAT-PAY-10" is a consumed contract and not a build gate (GAP-2944; ASM-4840).

#### 12.3 Events published

None. The owned event of this service is EV-22 `AssetTakenOn`, published by the take-on story, and the sale event belongs to the sale and auction stories. This capability writes no outbox row, adds nothing to `rwb.asset.events.v1` and a build that publishes here fails the absence test (BR5).

#### 12.4 Events consumed

| Element | Declared value |
|---|---|
| Event | EV-25 `ProceedsMatched`, payload proceedsId, caseId and amount |
| Topic and event name | `rwb.payment.events.v1`, event `rwb.payment.ProceedsMatched.v1`, with the `.retry` and `.dlt` topics of the platform |
| Envelope | CloudEvents, schema version, event id, idempotency key, correlation reference, no personal data |
| Subscription | Consumer group `rwb-asset`, inbox row in `rwb_asset`, then a signal to `AssetDisposalWorkflow` |
| Dedupe and failure | A repeated event id or key is ignored and counted (R-UNI-40); after the retry limit the event goes to `.dlt` with its owner |
| Versioning | The consumer accepts the current and the previous schema version |

EV-25 stands as published by Payments and posting with "Case and workflow" as its only named consumer, while Architecture v5 slide 13 gives S5 an event subscription to P8; the catalogue slide wins under R-PREC and the subscription is declared here (GAP-2945; ASM-4841). No other topic is consumed by this capability: the litigation events of the matrix's S4 column serve other steps of the service.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference, the sale reference and the rule package in force; signals: `ProceedsMatched`, residual computed and the package in force |
| `applyProceeds` | Activity, the proceeds-and-shortfall step | `rwb-asset` | The case, the sale and the proceeds fact in; the rule IDs with their versions, the sale outcome, the residual and the stage outcome out, in one transaction |

This baseline fixes the input and signal elements and the one activity it adds, and it declares no child workflow and no second queue. The activity name is a design choice of the application story, and the baseline carries it so the workflow's history stays stable.

#### 12.6 Schedules

None. The step is event-started from the inbox, so the baseline declares no Temporal Schedule and no legacy Quartz job for it. The single Schedule of the service is JOB-19, which the re-appraisal story owns and which is not declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset_sale | S5 (`rwb_asset`) | The settled sale; the baseline declares the elements of the sale answer, not its schema |
| listing | S5 (`rwb_asset`) | The listing of the sale; the baseline declares the elements it reads |
| asset | S5 (`rwb_asset`) | The asset of the sale; the baseline declares the elements it reads |
| decision_record | PLT library, created in `rwb_asset` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key, inbox | PLT library, created in `rwb_asset` | The dedupe of the event and the key of a repeated call |

The baseline declares no column, no index and no migration, and declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `proceeds` (P8), `decision_log_entry`, `rule_row` and `approval` (P7), `valuation` (S1), `document` (P5), `deviation` (S8) and every `v_ace_*` view (P1) are named by their owner and never declared here. No residual column exists and none is declared (GAP-2947; ASM-4843).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and case-move fake | The case states `ASSET_SOLD` and `PROCEEDS_APPLIED` of the fixture cases; the two moves accepted and one refused | C4, C6 |
| rwb-payment proceeds-fact fake | A posted sale with its fee matched; a fee with no match; a stale fact with its date; no answer inside 2 s | C4, C6 |
| rwb-payment `ProceedsMatched` event fake | One event; the same event id twice; an event with no sale; an event past the retry budget | C4, C6 |
| rwb-source-data data-product fake | The account balance and the NPA sale of the fixture cases; a stale business date | C4, C6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with the two rules | C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C5, C6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000593` | C2, C6 |
| Read answer fake | The asset answer with its sale, its fee, its proceeds state and its residual, and one with the residual absent | C2, C3 |
| Placeholder fake | A consumed row answered with the placeholder name and no path | C2, C4 |

Each fake answers only what its owner documents, and a fake that answers more than the document fails the review. The names that are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2944; GAP-2946).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two asset reads on `/api/recovery/asset/v1`; the case-state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 1 consumed | EV-25 `ProceedsMatched` on `rwb.payment.events.v1` as `rwb.payment.ProceedsMatched.v1`, with the inbox of `rwb-asset`, the retry topic and `.dlt` |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and `applyProceeds` on `rwb-asset`; the consumed proceeds-fact and case activities on their owners' queues; no Schedule |
| File | None | No file element is declared; the sale's papers belong to the document hub |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4030 CON Apply proceeds and raise the shortfall - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S5-E4030.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided reads, the consumed rows, the published and consumed events, the workflow and its activity, the schedules, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Open shapes carried into the tag.** Three shapes are carried as placeholders and not invented: the residual and its D9 hand-off (GAP-2947; ASM-4843), the names of the consumed rows (GAP-2944; GAP-2946) and the vendor-fee match of the sale answer (GAP-2949; ASM-4845). A placeholder is a declared forthcoming shape, not a permission to guess.

**Subscription.** The inbox and the envelope are platform capabilities of the event platform; the subscription is declared here and claims no new H row because DP-09 is outside the pattern set (GAP-2953; ASM-4849). The consumer group name, the retry and `.dlt` topics and the 2 s budget are platform configuration (ADR-020).

**Done when.** The seven criteria pass, the reviewers of the three consumed owners and of the event have closed their comments, the compatibility check passes on the tag, the fakes are published with their documented answers, and RWB-S5-E4030-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Asset and disposal right calls one of the declared reads | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required or invalid parameter of a declared read is supplied | Enter {field}. |
| MSG-S5-001 | A declared read carries a sale price or a floor under the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | A declared read carries an appraisal more than a year old | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published name | Not specified in the source documents (GAP-2944; ASM-4840). |

The five message IDs are carried from the service and platform sets and are declared only as the envelope rows of the reads in this baseline; the two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-21 Asset list and SCR-22 Asset record through the gateway-bff composite route (DP-19). What this story fixes is the element list of the declared responses and the empty, loading, refused, not-recorded, wrong-state and stale-proceeds states the route can show from this service's answers. The route itself, its merge order and its field list are RWB-PLT-N001-CON, and the screens' transitions are the application story's.

No screen is built here and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The legacy screen states and the holding lists do not match one for one, and the contract declares the `LOV-HOLDING` and `LOV-LISTING` identifiers rather than their values (GAP-2952; ASM-4848).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-030-01 | C2: the sale and residual elements and the read answer | Contract | The published schema and one recorded answer of `GET /assets/{assetId}` |
| TC-E4-030-02 | C6: the rule-package and decision-record elements | Contract | The element list, the two rules, the stopped stub and a package declared with a rule table |
| TC-E4-030-03 | C5: the error envelope and the not-recorded path | Contract | One request per error code, 400, 401, 403, 404, 422 and 503, and a stopped record chain |
| TC-E4-030-04 | C3: the two reads, their rights and the absence of a write | Contract | One request per read and per right, including a role without the right, and the operation list with no POST |
| TC-E4-030-05 | C4: the consumed rows of rwb-case, rwb-payment and rwb-source-data | Contract | The four consumed rows, each with and without a published name |
| TC-E4-030-06 | C6: the `ProceedsMatched` subscription and its dedupe | Contract | The envelope, the consumer group, the retry and `.dlt` topics and the same event id twice |
| TC-S5-E4030-CON-01 | C2: the residual placeholder | Contract | The element list with and without a named element for the residual |
| TC-S5-E4030-CON-02 | C6: the fakes and their documented answers | Contract | The nine fakes, the stopped stub and one fake that answers more than its document |
| TC-S5-E4030-CON-03 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |
| TC-S5-E4030-CON-04 | C7, BR5: no event published and none of another topic consumed | Contract | The outbox declaration, empty, and the topic list with one consumed topic |

The six legacy case IDs are mapped onto this contract deliverable in their legacy order, and their `Covers` names the criterion of this story that fixes the surface each legacy case touches: the sale answer (01), the rule and the record (02), the failure and error path (03), the operations and rights (04), the consumed rows (05) and the event subscription (06). The four `TC-S5-E4030-CON-` cases are new and test the parts no legacy case touches: the residual placeholder, the fakes, the compatibility check and the absence of a published event. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the baseline: the package, its version, the fee, the codes and every threshold are referenced with their identifier and version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the account and NPA-sale facts appear only as the P1 row (DP-05).
- The case stays with rwb-case and the money with rwb-payment: no `recovery_case` element and no `proceeds` element is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Schedule for an event-started step.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id; the requirement the baseline serves is FEAT-AST-21 of FSD S5 A2.21 (GAP-2951; ASM-4847) | The baseline, its consumed rows, its event and its fakes | TC-S5-E4030-CON-01, TC-E4-030-03 |
| ADR-013 | 19 services inside ACE | The baseline's ownership rows | TC-E4-030-05 |
| ADR-014 | Schema and login per service | `rwb_asset` and the declared tables | TC-E4-030-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `ProceedsMatched` subscription and its envelope | TC-E4-030-06, TC-S5-E4030-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows and the compatibility check | TC-E4-030-03, TC-S5-E4030-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its library | TC-S5-E4030-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-030, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 are carried by RWB-S5-E4030-APP; this story carries no legacy criterion and tests the surface they touch |
| Test cases | TC-E4-030-01 to TC-E4-030-06 at Level Contract, and TC-S5-E4030-CON-01 to TC-S5-E4030-CON-04 |
| Feature and screens | FEAT-AST-21, SCR-21 Asset list and SCR-22 Asset record, read through the composite route |
| Rules | R-DIS-54 and R-DIS-55, referenced as rule-package rows and not evaluated here |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The branch behaviour, the rule evaluation, the sale write, the records and the case moves: RWB-S5-E4030-APP.
- The sale, its award, the five-day payment term and the title transfer: FEAT-AST-18 to FEAT-AST-20's stories.
- The payment matching, the balance application, the loan-account posting and the vendor-fee posting: FEAT-PAY-04 and FEAT-PAY-10 of rwb-payment (P8) (GAP-2948).
- The no-shortfall close and the residual routing to write-off or debt sale: R-DIS-56 to R-DIS-58 of the write-off route (S7) (GAP-2950).
- The residual-route task and the manual decision: R-DIS-71 and R-DIS-72, adjacent (GAP-2950).
- The case of record, its states and the parent workflow: rwb-case (P3).
- The account and NPA-sale facts of ACE: rwb-source-data (P1) (GAP-2946).
- The rule package, its version and its approval: rwb-decision (P7) (GAP-2953).
- The decision-record library's own schema, its migration and the platform event library: RWB-PLT-E1027-CON and the event platform (GAP-2953).
- The composite route, its merge order and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards, the alerts and the runbook: the operations story of this legacy key.
