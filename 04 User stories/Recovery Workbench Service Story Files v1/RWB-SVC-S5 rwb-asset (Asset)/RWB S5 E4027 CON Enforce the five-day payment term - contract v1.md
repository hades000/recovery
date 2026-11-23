# RWB-S5-E4027-CON Enforce the five-day payment term - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4027-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-027 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-027, the baseline the payment branch of rwb-asset builds against on Day 1. The baseline declares the two asset reads that carry the sale, the award and the term to SCR-22 and SCR-21 on `/api/recovery/asset/v1` (DP-13), the four consumed rows — the rwb-case state read, the case-move answer and the rwb-payment payment fact on its queue and its event on `rwb.payment.events.v1` (DP-05, DP-09) — the decision-record element of DP-03, the rule-package element the branch evaluates, the rights and the error envelope, and the fakes. No event is published, because the owned event of the service is EV-22 `AssetTakenOn`. No source names an element for the award, its payment due date, the received-at time, the buyer or the term (GAP-2925; ASM-4822); the term rules sit across this story and RWB-S5-E4024-APP (GAP-2926; ASM-4823); AC2 and AC3 name rules of other features (GAP-2927; ASM-4824); no requirement row names the term (GAP-2928; ASM-4825); no source publishes the names of the consumed rows or of the payment event (GAP-2929; ASM-4826); and the package is declared without the DP-04 platform row (GAP-2930; ASM-4827). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the five-day payment-term capability of rwb-asset — the asset reads that carry the sale and the term, the consumed rows of rwb-case and rwb-payment, the decision-record and rule-package elements, the rights, the error envelope and the fakes — baselined and tagged before the build starts**, so that **the application story and every consumer of a sale can build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-027. It owns:

- the document that fixes the two asset reads on base `/api/recovery/asset/v1`, with their parameters, their documented answer, their rights and their idempotency (DP-13);
- the four consumed rows: the rwb-case case state read and case-move answer, the rwb-payment payment fact and the rwb-payment payment event, each with its owner, its use and its placeholder where the name is not published (DP-05, DP-09);
- the decision-record element and the local library dependency that carries it (DP-03);
- the rule-package element: the DISPOSAL package, its version and the four rules this branch evaluates, declared as a reference and not as a rule table of this service;
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, so that every downstream answer has a stub on Day 1;
- the naming and boundary rules of the baseline: one base, one topic, one queue, no foreign schema, no monolith base, no Schedule for a term that is a workflow timer.

It does not own: the term behaviour, the rule evaluation, the sale write, the decision records and the case moves, which are RWB-S5-E4027-APP; the award cancellation, the vendor score and the reopened round, which are RWB-S5-E4024-APP; the agreed sale and the bid acceptance, FEAT-AST-16's story; the title transfer, FEAT-AST-19 and FEAT-AST-20's stories; the payment and its posting, rwb-payment's (P8); the case of record, rwb-case's (P3); the rule package, rwb-decision's (P7); the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

### 2. Business rationale

A contract baseline is what lets the stories of one wave build at once. Without it the term would be written against whatever payment answer the service happened to receive that week, and the first integration would find the mismatches instead of the review. With it, the application story builds on Day 1 against a tagged document and its fakes, the rounds and title-transfer stories know what the sale record must carry for the term to run, and the consumers of the asset reads know exactly which elements they can rely on.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner and its use, and where the source documents do not publish a name the row carries the placeholder rather than an invented path or payload (GAP-2929; ASM-4826).
- **one hop, one budget.** Every consumed row is a single hop or a single activity with a 2 s timeout, a breaker and no chain, which is ADR-020 and is what the application story's exception paths assume.
- **additive only.** The baseline moves forward without breaking: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version and a new document (C1).

The business outcome the baseline protects is the one FEAT-AST-18 of the FSD names: the winning bidder's payment is tracked against the term and the asset is released if it is missed. The baseline does not state that outcome, and no criterion here asserts a business value.

### 3. Preconditions

- The Ownership Map rows are in force: S5 owns `GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds`; `asset_sale` and `listing` are S5's tables.
- The service naming is fixed: schema `rwb_asset`, login `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with `.retry` and `.dlt`, task queue `rwb-asset` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.asset`.
- The published shapes of the declared operations are the API Specification v4: `AssetPage` and `Asset`, the two reads of API-S5-001 and API-S5-002.
- The owned event row of the service is EV-22 `AssetTakenOn` (TSD S5 T5.3); the assets of this baseline touch none of the events of the service, and the term and the payment arrive as signals and as the P8 event.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). DP-04 is not in the pattern set of this slice, so no platform row for the rules kit is claimed and the package is referenced as rwb-decision's (GAP-2930; ASM-4827).
- The term elements — the award, the due date, the received-at time, the buyer and the term length — have no column in TSD S5 T3.1, so the baseline declares them as open shapes (GAP-2925; ASM-4822).
- No approval is needed to publish a Draft baseline; the document is baselined by this story's own review, and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map, the TSD S5 T-A.1 operations, the TSD S5 T3.1 tables and the lists of T3.2.
2. Every operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The decision-record element is declared with the library dependency that carries it, and the rule-package element with its owner and its version.
5. The fakes are declared with their documented answers, one per consumed row, one for the composite route and one for the award signal.
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
| X7 | Two documents claim the same path or queue, or a document invents an award element that no table names | The naming rule and the placeholder rule resolve it: the owner in the Ownership Map keeps the path, and the award stays Not specified in the source documents | C2, C7 |
| X8 | The term rule set is claimed twice, by this baseline and by the rounds baseline | The rule rows stay single in the package and each baseline references the same four rows with the same versions | C5, C6 |

X1 to X3 are the paths of an incomplete source, X4 to X6 are the paths of a baseline moving under a build, and X7 and X8 are the naming and rule-ownership boundaries.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the order of the sections and the fake data are this story's choice; the paths, the owners, the base, the error set and the element names are fixed by their sources |
| Valuable | The stories of wave 3 build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, two provided operations, four consumed rows, two library elements, eight fakes and one compatibility check |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the five-day payment-term capability

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema and the open and closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The term elements and the closed lists are published as declared (new, D-RCV-60)
    Given the baseline document of this story
    When the element list, the required and optional flags and the closed lists of the sale read are read
    Then every element carries its type, its nullability and its source
    And every closed list is referenced with its identifier and its version and is not enumerated in code
    And the award, payment_due_date, payment_received_at, the buyer and the term length carry the placeholder and its gap identifier because no table or request element holds them

  Scenario: C3 The asset reads are declared with their rights and no write is added (new, D-RCV-60)
    Given the operations the baseline provides on base /api/recovery/asset/v1
    When the method, path, documented answer, right and idempotency of each are read
    Then GET /assets and GET /assets/{assetId} carry the Asset and disposal right R with scope applied and no idempotency
    And the baseline declares no write, because the term starts and is confirmed inside AssetDisposalWorkflow
    And POST /assets/{assetId}/valuations is named as rwb-valuation's and POST /listings/{listingId}/rounds as RWB-S5-E4024's, and neither is declared here

  Scenario: C4 The consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation and event tables of the baseline
    When the rows of rwb-case and rwb-payment are read
    Then each row names its owner, its use and its 2 s budget or its consumer group
    And where the name is not published the row carries the placeholder and the gap identifier and no path
    And the payment event row names the topic rwb.payment.events.v1 and the consumer group of this service

  Scenario: C5 The error envelope and the rule ownership are declared per operation (new, D-RCV-60)
    Given the operations the baseline provides and the rule-package element
    When the error set, the rights and the rule rows of each operation are read
    Then the error set names 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 in one problem envelope
    And the rule-package element names R-DIS-11, R-DIS-37, R-DIS-47 and R-DIS-48 only, and R-DIS-49 and R-DIS-50 are named as RWB-S5-E4024-APP's
    And the capability area and the right of each operation are the rows of the access matrix

  Scenario: C6 The decision-record, rule-package and fake elements are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the rule-package element and the fake table are read
    Then the decision-record element names RWB-PLT-E1027-CON as its library and the transaction it joins
    And the rule-package element names the DISPOSAL package, its owner, its version in force and the four rules, and declares no rule row
    And every consumed row has a fake with a documented answer, including the stopped stub, the stale payment fact, the duplicate event and the award signal without its sale date

  Scenario: C7 The naming and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue and the schema of the baseline
    When the document is checked against the naming rule and the ownership map
    Then the base /api/recovery/asset/v1, the queue rwb-asset, the topic rwb.asset.events.v1 and the consumed topic rwb.payment.events.v1 are the only ones declared
    And no foreign schema, no foreign topic as this service's own, no monolith base /api/recovery/v1 and no Schedule for the term timer is declared
    And no event is published by the payment branch
```

The seven criteria are new to this run and are tagged as such: they test the contract deliverable only — the schema, the elements, the lists, the operations, the consumed rows, the rights, the envelope, the two library elements, the fakes and the boundary. No criterion states a business outcome or a business value of the application story, and none asserts that a rule fires, that a payment arrives or that a case moves.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, event and table: the baseline declares only the rows the Ownership Map gives to S5, and names every other row with its owner | Ownership Map; Architecture v5 slide 41 |
| BR2 | A consumed row with no published name carries the placeholder and its gap, and never an invented path or payload | Template and Rules v1 §R9; GAP-2929 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; C1 |
| BR4 | Every consumed row is one hop or one activity with a 2 s timeout, a breaker and no chain | ADR-020 |
| BR5 | No event is published: the owned event is EV-22 `AssetTakenOn`, the take-on story's, and the payment event is consumed, never produced here | TSD S5 T5.3 |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR7 | The rule package is referenced, never redefined: the DISPOSAL package, its version and the four rules are rwb-decision's rows and no rule table of this service is declared | DP-04 (not claimed); GAP-2930 |
| BR8 | No business value is declared in the baseline: the term length, the reminder point, the statuses, the codes and the thresholds are referenced with their identifier and version | Template and Rules v1 §R7.2 (s16); legacy Guardrails |
| BR9 | No personal data in any element, fake or example of the baseline; a buyer is a code, never a person | Template and Rules v1 §R7.2 (s17) |
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
| Tagged | A rule row is claimed by the rounds baseline too | X8 | The rule set stays single and the reference is recorded, not duplicated |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Authors the baseline, resolves the shape of the service's own operations and signs the tag |
| Owner of rwb-case (P3) | Reviews the case state and case-move rows and publishes the operation names when they exist |
| Owner of rwb-payment (P8) | Reviews the payment-fact row, the payment-event row, the due date and the freshness stamp |
| Owner of rwb-decision (P7) | Reviews the rule-package element, the DISPOSAL package version and the decision-record element with the platform library |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the rights of each declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The asset page of `GET /assets` | S5 (`rwb_asset`) | The paginated asset list with its filters, its paging elements, the sale status and the term of each asset | Read by the screens |
| The asset answer of `GET /assets/{assetId}` | S5 (`rwb_asset`) | The asset of status 200 with its title, its listing, its sale, the award, the due date and the days remaining | Read by the screens; written by the application story |
| The sale elements (DF-SAL-009 to DF-SAL-019) | S5 (`rwb_asset`) | id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee, the two tax elements and gain_loss, as the declared answer | Written by the application story |
| The listing elements (DF-SAL-001 to DF-SAL-008) | S5 (`rwb_asset`) | sale_channel, start_price, floor_price, round_no, listed_at, status, referenced with `LOV-SALE-CHANNEL` and `LOV-LISTING` | Read in this baseline |
| The asset elements (DF-COL-028 to DF-COL-042) | S5 (`rwb_asset`) | asset_ref, asset_type, book_value, holding_status, referenced with `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN` and `LOV-HOLDING` | Read; the holding status written by the application story |
| The award, payment_due_date, payment_received_at, the buyer and the term length | none | Not specified in the source documents for the element they occupy (GAP-2925; ASM-4822); declared only once their owner names them | Declared as open shapes |
| The case elements of the consumed read | P3 (`rwb_case`) | The case reference, the case state and the stage outcome; referenced, not redefined | Consumed |
| The payment elements of the consumed row | P8 (`rwb_payment`) | The due date, `payment_received_at` and the freshness stamp, in place of the legacy `v_ace_payment` read (DF-ACE-043 to DF-ACE-054) | Consumed |
| The decision-record elements | PLT library, created in `rwb_asset` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time (DF-DEC-001 to DF-DEC-018) | Written through the library |
| The rule-package elements | P7 (`rwb_decision`) | The package name, its version in force and the four rows (DF-REF-001 to DF-REF-015) | Referenced only |

The baseline declares no new table, no new column and no migration, and it enumerates no business value: every list, code and threshold is referenced with its identifier and its version. **No personal data** appears in any element, fake or example; the fixture identifiers are synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). These are the reads that answer SCR-22 and SCR-21 with the sale, the award and the term.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the sale status and the term of each asset (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, its listing, its sale, the award, the due date and the days remaining (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

No write is declared: the term starts at the award (R-DIS-47) and is confirmed on the payment fact (R-DIS-48) inside `AssetDisposalWorkflow`, so the API surface of the service does not grow for this capability. The legacy Endpoints table names `POST /assets/{assetId}/valuations` (API-S5-003), which is rwb-valuation's under ASM-0043, and `POST /listings/{listingId}/rounds` (API-S5-005), which is RWB-S5-E4024's; neither is declared here, and either would need its owner's document before this baseline could carry it.

The error envelope of the declared operations: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for an invalid filter and with MSG-S5-001 where an accepted price is under the limit, and 503 when the decision library or a consumed boundary does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state the rules check before they fire; faked |
| The case-move answer (name Not specified in the source documents (GAP-2929; ASM-4826)) | rwb-case (P3) | P3 rwb-case | The answer that carries `AWAITING_PAYMENT`, `TITLE_TRANSFER_PENDING`, `ASSET_HELD` and `BID_RECEIVED` with the rule version; on the workflow boundary it is the outcome the parent applies; faked |
| The payment-fact activity (name Not specified in the source documents (GAP-2929; ASM-4826)) | queue `rwb-payment` | P8 rwb-payment | The due date, `payment_received_at` and the freshness stamp, in place of the legacy `v_ace_payment` read (DP-05); faked |

Each row is one hop or one activity, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag rather than inventing a surface (BR2).

#### 12.3 Events published

None. The owned event row of this service is EV-22 `AssetTakenOn`, published by the take-on story when the asset record opens, and the sale event is the sale stories'. This baseline declares neither as its own, adds nothing to `rwb.asset.events.v1`, and the payment branch writes no outbox row: its outward surface is the case-move answer and its own reads.

#### 12.4 Events consumed

| Topic | Event | Owner | Use |
|---|---|---|---|
| `rwb.payment.events.v1` | Payment event (name Not specified in the source documents (GAP-2929; ASM-4826)) | P8 rwb-payment | One consumer group of this service, deduplicated by event id through the inbox library (DP-09); the event wakes the workflow and is a signal, never the record of truth, which is the fact |

The row is the one subscription Architecture v5 slide 13 gives the S5 row against the P8 column. The baseline declares no other topic, no other consumer group and no outbox row, and a build that subscribes to a topic not listed by Architecture v5 fails the naming check (BR5, DP-14).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference, the listing reference, the sale reference and the rule package in force; signals: the award made, the payment received, the payment-term expiry and the rule package in force |
| `startPaymentTerm` | Activity, the term start | `rwb-asset` | The sale, the award and the package in; the rule IDs with their versions, the due date, the holding status and the stage outcome out, in one transaction |
| `confirmSalePayment` | Activity, the confirmation | `rwb-asset` | The payment fact in; the rule IDs with their versions, the confirmation, the title-transfer start and the stage outcome out, in one transaction |

The workflow is the same execution the take-on, holding and sale stories of this service use; this baseline fixes its input and signal elements and the two activities it adds, and it declares no child workflow and no second queue. The activity names are design choices of the application story, and the baseline carries them so that the workflow's history is stable. R-DIS-49 and R-DIS-50 are evaluated by RWB-S5-E4024-APP on this story's expiry signal, so the baseline declares them as another story's rules and not as its own activities (GAP-2926).

#### 12.6 Schedules

None. The five calendar days run as a durable timer inside the workflow, so the baseline declares no Temporal Schedule and no legacy Quartz job for the term. The single Schedule of the service is JOB-19, which the re-appraisal story of this service owns and which is not declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset_sale | S5 (`rwb_asset`) | The sale and the award; the baseline declares the elements of the term against it, not its schema |
| asset | S5 (`rwb_asset`) | The holding status while the term runs; declared as an element, not a schema |
| listing | S5 (`rwb_asset`) | Read in this baseline; the reopen is the rounds story's write |
| decision_record | PLT library, created in `rwb_asset` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated signal or fact and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), the payment and posting tables (P8), `valuation` (S1), `document` (P5), `deviation` (S8), the partner tables (S9) and every `v_ace_*` view (P1) are named by their owner and never declared here. No award table exists and none is declared (GAP-2925; ASM-4822).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state and case-move fake | The case states `SALE_AGREED`, `AWAITING_PAYMENT`, `TITLE_TRANSFER_PENDING`, `WORK_ORDER_OPEN` and `ROUND_OPEN` of the fixture cases; the moves accepted and a move refused for an unexpected state | C3, C4, C6 |
| rwb-payment payment-fact fake | No payment by the due date; a payment received one day early; a payment on the due date; a stale fact with its date; no answer inside 2 s | C4, C6 |
| rwb-payment event fake | The payment event of sale `SL-2026-000527`, a duplicate on the same event id and an event that disagrees with the fact | C4, C6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with the four rules | C5, C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-22 and SCR-21 answer for case `RC-2026-000527`, with the term read once | C2, C6 |
| Award signal fake | An award with every field, one without the sale date and one repeated on the same key | C2, C6 |
| Sale answer fake | The declared sale answer with its mandatory dates and price, and one with the term values absent | C2, C3 |

Each fake answers only what its owner documents, and a fake that answers more than the document fails the review. The names that are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2929; ASM-4826).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 1 consumed | `rwb.payment.events.v1`, one consumer group, read as a signal through the inbox library (DP-09) |
| Temporal | 1 workflow and 2 activities | `AssetDisposalWorkflow`, `startPaymentTerm` and `confirmSalePayment` on `rwb-asset`; the payment fact on its owner's queue; no Schedule |
| File | None | No file element is declared; the portal publication is FEAT-AST-12's |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S5 rwb-asset (Asset)/RWB S5 E4027 CON Enforce the five-day payment term - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S5-E4027.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-09 is applied through the service template — the inbox library and the consumer group — and it is not converted into a platform row here, because the outbox and inbox library comes with the template.

**Sections and owners of the review.** The document is written in nine parts: the provided operations, the consumed rows, the published and consumed events, the workflow and its activities, the schedules, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Open shapes carried into the tag.** Three shapes are carried as placeholders and not invented: the award and its term (GAP-2925; ASM-4822), the names of the consumed rows and of the payment event (GAP-2929; ASM-4826) and the rule references of the rounds story (GAP-2926; ASM-4823). A placeholder is a declared forthcoming shape, not a permission to guess.

**Done when.** The seven criteria pass, the reviewers of the two consumed owners have closed their comments, the compatibility check passes on the tag, the fakes are published with their documented answers, and RWB-S5-E4027-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Asset and disposal right calls one of the declared operations | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of a declared request is absent or invalid | Enter {field}. |
| MSG-S5-001 | A declared read carries an accepted price under the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | A declared read carries an appraisal more than a year old | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The payment fact is stale at the due date | {product} is from {date}. Today's ACE batch has not arrived. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published name | Not specified in the source documents (GAP-2929; ASM-4826). |

The six message IDs are carried from the service and platform sets and are declared only as the envelope rows of the operations in this baseline; the two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-22 Asset record and SCR-21 Asset list through the gateway-bff composite route (DP-19), and SCR-24 Auction rounds reads the award from the same answers. What this story fixes is the element list of the declared responses and the empty, loading, refused, invalid-filter, stale-payment and unanswered-fact states the route can show from this service's answers. The route itself, its merge order and its field list are RWB-PLT-N001-CON, and the screens' transitions are the application story's.

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-027-01 | C2: the sale and term elements the declared reads carry | Contract | The published schema and a recorded answer for sale `SL-2026-000527` |
| TC-E4-027-02 | C3, C5: the provided operations, their rights and their error set | Contract | One request per operation and per right, including a role without it and a 422 on an invalid filter |
| TC-E4-027-03 | C4: the consumed rows of rwb-case and rwb-payment and the payment event row | Contract | The four consumed rows, each with and without a published name, and the consumer group on `rwb.payment.events.v1` |
| TC-E4-027-04 | C5: the error envelope of the declared operations | Contract | One request per error code, 400, 401, 403, 404, 422 and 503 |
| TC-E4-027-05 | C7: the naming and the boundary rule | Contract | The base, the topic, the queue and the schema, plus a draft that names a foreign schema, a monolith base or a Schedule |
| TC-E4-027-06 | C6, BR6: the decision-record element and a forced failure | Contract | The healthy chain, the stopped chain and a declared write that reaches the stub |
| TC-S5-E4027-CON-01 | C2: the term placeholder | Contract | The element list with and without a named element for the award and the due date |
| TC-S5-E4027-CON-02 | C6: the fakes and their documented answers | Contract | The eight fakes, the stopped stub and one fake that answers more than its document |
| TC-S5-E4027-CON-03 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |
| TC-S5-E4027-CON-04 | C7, BR5: no event published | Contract | The outbox declaration, empty, and the single consumed topic |

The six legacy case IDs are mapped onto this contract deliverable in their legacy order, and their `Covers` names the criterion of this story that fixes the surface each legacy case touches: the sale and term answer (01), the operations and rights (02), the consumed rows (03), the error path (04), the naming boundary (05) and the forced record failure (06). Their `-ITG` copies belong to the wave 3 harness, which carries the real payment and case calls. The four `TC-S5-E4027-CON-` cases are new and test the parts of the baseline that no legacy case touches: the term placeholder, the fakes, the compatibility check and the absence of an event. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the baseline: the term length, the reminder point, the statuses, the codes and every threshold are referenced with their identifier and version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates, a buyer code and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the payment appears only as the P8 rows (DP-05).
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case` element and no rule row is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Schedule for the term timer, no event published by the payment branch.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id names this slice | The split plan carries no requirement id for this slice; the requirement the baseline serves is FEAT-AST-18 of FSD S5 A2.18, that the winning bidder's payment is tracked against the term (GAP-2928; ASM-4825) | The baseline, its consumed rows and its fakes | TC-S5-E4027-CON-01, TC-E4-027-03 |
| ADR-013 | 19 services inside ACE | The baseline's ownership rows | TC-E4-027-05 |
| ADR-014 | Schema and login per service | `rwb_asset` and the declared tables | TC-E4-027-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows and the compatibility check | TC-E4-027-03, TC-S5-E4027-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its library | TC-S5-E4027-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-027, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 are carried by RWB-S5-E4027-APP; this story carries no legacy criterion and tests the surface they touch |
| Test cases | TC-E4-027-01 to TC-E4-027-06 at Level Contract, and TC-S5-E4027-CON-01 to TC-S5-E4027-CON-04 |
| Feature and screens | FEAT-AST-18, SCR-22 Asset record and SCR-21 Asset list, read through the composite route |
| Rules | R-DIS-47 and R-DIS-48 owned by this capability; R-DIS-11 and R-DIS-37 kept as the AC2 and AC3 gates; R-DIS-49 and R-DIS-50 named as RWB-S5-E4024-APP's |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The term behaviour, the rule evaluation, the sale write, the decision records and the case moves: RWB-S5-E4027-APP.
- The award cancellation, the vendor score and the reopened round (R-DIS-49, R-DIS-50): RWB-S5-E4024-APP.
- The bid acceptance and the agreed sale: FEAT-AST-16's story.
- The vehicle registration transfer and the Land Office transfer: FEAT-AST-19 and FEAT-AST-20's stories.
- The payment, its matching, its posting and its event payload: rwb-payment (P8).
- The case of record, its states and the parent workflow: rwb-case (P3).
- The rule package, its version and its approval: rwb-decision (P7) (GAP-2930).
- The asset valuation write: rwb-valuation (S1) under ASM-0043.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The composite route, its merge order and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
