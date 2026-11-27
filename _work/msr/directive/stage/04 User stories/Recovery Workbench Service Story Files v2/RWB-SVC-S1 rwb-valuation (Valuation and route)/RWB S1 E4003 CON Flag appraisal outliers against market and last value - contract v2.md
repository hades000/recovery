# RWB-S1-E4003-CON Flag appraisal outliers against market and last value - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4003-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Size | Set by the squad at refinement; not specified in the source documents (DOR-RWB-S1-E4003-CON-16). Fit to two weeks: not specified in the source documents (DOR-RWB-S1-E4003-CON-15) |
| Contract version | v1, base `/api/recovery/valuation/v1` (DP-13) |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | Missing: the four consumed operations of rwb-source-data, rwb-case, rwb-decision and rwb-access are not published (GAP-2600; ASM-4301); recorded as missing, not absent by design |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-003, the baseline the outlier step of rwb-valuation builds against on Day 1. The baseline declares the route-decision operation `POST /cases/{caseId}/route` (API-S1-001) on `/api/recovery/valuation/v1` (DP-13), the outlier element of its answer under a draft name with a placeholder for its published shape, the six consumed rows including the market benchmark and the gap rule (DP-05), the decision-record element and the library that carries it (DP-03), the elements of `RouteDecisionWorkflow` and its two activities, the rights, the error envelope and the fakes; it publishes no event, because the ownership rows give S1 none. The gap rule and its value are not stated and no S1 rule package carries them (GAP-2596; ASM-4297); the market benchmark has no published owner, operation or element (GAP-2597; ASM-4298); the store of the flag is not fixed (GAP-2599; ASM-4300); the names of the consumed operations are not published (GAP-2600; ASM-4301); the outlier element of the route answer is in no published schema (GAP-2602; ASM-4303). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S1-E4003-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 15 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **solution architect**, I want **the published contract baseline of the outlier step of rwb-valuation, being its route-decision operation, its outlier element, its six consumed rows, its decision-record element, its workflow elements, its rights, its error envelope and its fakes, fixed and tagged before the build starts**, so that **the application story, the wave 3 harness and the six owners it consumes can build and test on Day 1 against one versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-003. It owns:

- the document that fixes `POST /cases/{caseId}/route` (API-S1-001) on base `/api/recovery/valuation/v1`: `RouteRequest` in, `Approval` out, the `Idempotency-Key` header, the rights and the error set, plus the outlier element the answer needs (DP-13);
- the outlier element itself: a draft name, the two gaps, the flag and its reasons, its rule version, and the placeholder that says its published shape is not in any schema (GAP-2602);
- the six consumed rows: the appraisal, acceptance and previous-value data product of rwb-source-data, the market benchmark, the gap rule of rwb-case reference data, the case state of rwb-case, the rule-in-force and decision-log read of rwb-decision, and the authorise operation of rwb-access, each with its owner, its use and a placeholder where the name is not published (DP-05);
- the decision-record element, the library that carries it and the shared topic it reaches (DP-03);
- the elements of `RouteDecisionWorkflow` and its two activities on task queue `rwb-valuation`;
- the subject of SCR-13 Route decision, one hop through the gateway-bff composite route (DP-19), with its loading state and its empty, error and no-access states Not specified in the source documents (DOR-RWB-S1-E4003-CON-10; CG-ALL-7995);
- the fakes and their documented answers, including an absent benchmark and an unresolvable rule;
- the naming and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no monolith base.

It does not own: the comparison of the two values, the flag, the decision records and the screens' behaviour, which are RWB-S1-E4003-APP; the appraisal order and the appraisal intake, which are RWB-S1-E4001-CON and RWB-S1-E4002-CON; the acceptance of the value, which is RWB-S1-E4004-CON; the ACE appraisal and acceptance facts, which are rwb-source-data's (P1); the market model, which is rwb-agent's (P10); the case of record, its route states and its reference data, which are rwb-case's (P3); the rule package and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets six teams start together. Legacy RWB-E4-003 asks for the new value to be compared with the market and with the previous value and the gap flagged for a person, with the result on the decision log; the step therefore reads four kinds of fact from four owners, writes one record in a fifth and answers one operation whose published answer carries none of its elements. Without a tagged baseline each of those shapes would be discovered at the first integration instead of at the review.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner, its use and its 2 s budget, and every row whose name is not published carries the placeholder and its gap (GAP-2597, GAP-2600; ASM-4298, ASM-4301).
- **one hop, one budget.** Each consumed row is a single hop with a 2 s timeout and a breaker; the appraisal is never read from a table and never chained through a second service (DP-05, ADR-020).
- **the answer is extended, not reinterpreted.** The published `Approval` carries no appraisal, market or outlier element, so the baseline declares one additive element under a draft name and keeps every published element as it is (GAP-2602; ASM-4303).

The business outcome the baseline protects is the one FEAT-VAL-03 and REQ-S1-002 of FSD S1 state: a valuation that is an outlier against the market and the last value is flagged before it is accepted. The baseline states no outcome and no business value of its own, and no criterion here asserts that a value is flagged.

### 3. Preconditions

- The Ownership Map rows for S1 are in force: `POST /assets/{assetId}/valuations`, `POST /assets/{assetKey}/valuations` and `POST /cases/{caseId}/route`; no table, no event, no job, and one workflow, `RouteDecisionWorkflow`.
- The service naming is fixed: schema `rwb_valuation`, one login of its own, base `/api/recovery/valuation/v1`, topic `rwb.valuation.events.v1` with `.retry` and `.dlt`, task queue `rwb-valuation` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.valuation`.
- TSD S1 is the shape of record for the service: T-A.1 gives API-S1-001 with right Treatment and offer U; T-A.2 gives `RouteRequest` in, `Approval` out, errors 401, 403, 404, 409, 422 and 503 and the `Idempotency-Key`; T6.1 gives the capability area and its rights; API Specification v5 gives the same operation with `RouteRequest` of route, override reason code and note and `Approval` of decision, level, amount and status.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions of this baseline and not in its H row.
- The outlier element is in no published schema, and the gap rule has no rule id in force: both are declared by this baseline as a draft element and a versioned reference, with a placeholder where a source is silent (GAP-2602, GAP-2596).
- The ownership rows give S1 no table, while TSD S1 T3.1 declares `valuation` as a NEW Workbench table and the FSD holds the acceptance in `recovery.valuation_ext`; the baseline declares no table of its own on that reading (GAP-2599; ASM-4300).
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S1 T-A.1, T-A.2 and T6.1, API Specification v5, the FSD S1 A2.3 rules and the DP table.
2. Every provided operation is declared with its method, path, request, documented answer, the added outlier element, the rights, the idempotency and the error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published, and the market benchmark row declares that its owner is not published before it declares a shape.
4. The outlier element is declared as additive: a draft name, the two gaps, the flag, its reasons and the rule version, marked as not published, with the placeholder of GAP-2602.
5. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins.
6. The workflow and its two activities are declared with their input, their signals and their outcome elements.
7. The schema, the open lists and the closed lists are published; a closed list is referenced with its identifier and its version and is never enumerated in code.
8. The fakes are declared with their documented answers: one per consumed row, one for the composite route and one for the stopped decision-record chain.
9. The compatibility check runs on the draft against the previous tag: a breaking change fails it, and the draft element is checked as an addition and never as a replacement of a published one.
10. The document goes to review as Draft; the reviewers are the owners of the six consumed rows and the tech lead of the service. On the review's close the document is tagged and RWB-S1-E4003-APP and the wave 3 harness start against the tag and the fakes.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and its gap; no path, element or value is invented | C3, C4, C5 |
| X2 | A change removes, renames, retypes or newly requires a published element | The compatibility check fails and the document needs a new major version | C1 |
| X3 | The outlier element is declared as a replacement of a published element instead of an addition | The review refuses the baseline and the compatibility check fails | C1, C2 |
| X4 | A declared operation reaches another service's data, base or table | The review refuses the baseline and the boundary test fails the build | C7 |
| X5 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C6 |
| X6 | The rights of an operation are not a row of the access matrix | The operation is not declared and the error set stays incomplete | C5 |
| X7 | Two documents claim the same base, topic, queue or path | The owner named in the Ownership Map keeps it and the other document changes | C7 |

X1 to X3 are the paths of an incomplete or extended source, X4 to X6 the paths of a baseline moving under a build, and X7 the naming boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order, the draft name of the outlier element and the fake data are this story's choice; the path, the request, the answer, the rights and the error set are fixed by TSD S1 |
| Valuable | Six teams build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, one provided operation, one added element, six consumed rows, one decision-record element, one workflow with two activities, one subject of SCR-13 and nine fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the outlier step

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The route-decision operation and the outlier element are published as declared (new, D-RCV-60)
    Given the operation table of the baseline
    When POST /cases/{caseId}/route on /api/recovery/valuation/v1 is read
    Then it names RouteRequest in, Approval out, the Idempotency-Key header, right U and the scope rule of T-A.2
    And the outlier element is declared as an addition carrying the two gaps, the flag, its reasons and the rule version

  Scenario: C3 The six consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-source-data, the market benchmark, rwb-case, rwb-decision and rwb-access are read
    Then each row names its owner, its use, one hop and a 2 s budget
    And where the owner, the operation or the element is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C4 The consumed rows are declared as reads and no foreign table is declared (new, D-RCV-60)
    Given the consumed table and the table-ownership table of the baseline
    When the appraisal, the previous value, the benchmark and the gap-rule rows are read
    Then each is declared as a consumed read of its owner and never as a table of this service
    And no v_ace_* object, no foreign schema and no foreign foreign key is declared

  Scenario: C5 The rights and the error envelope are declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the rights and the error set of each operation are read
    Then each names the capability area Treatment and offer and the right of the access matrix
    And the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503 in one problem envelope

  Scenario: C6 The decision-record element, the workflow elements and the fakes are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the workflow table and the fake table are read
    Then the element names RWB-PLT-E1027-CON as its library, the shared topic and the transaction it joins
    And RouteDecisionWorkflow and its two activities name their input, their signals and their task queue
    And every consumed row has a fake with a documented answer, including the absent benchmark, the unresolvable rule and the stopped decision-record chain

  Scenario: C7 The naming, the publication and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue, the schema and the outbox of the baseline
    When the document is checked against the naming rule, the ownership rows and the event list
    Then one base, one topic, one queue and one login are declared and no monolith base and no foreign topic appear
    And no event is published, because the ownership rows give S1 none, and no Schedule is declared

  Scenario: C8 The business rules BR1 to BR9 of the baseline hold (new, D-RCV-60)
    Given the business rules of section 8 and the published baseline
    When each rule is checked against the element list, the operation table and the boundary checks
    Then every rule BR1 to BR9 has a passing check under its test case of section 16
    And a draft that breaks a rule fails the check and the build

  Scenario: C9 An activity that is retried or times out is declared and its repeated write is absorbed (new, D-RCV-60)
    Given the activity table of RouteDecisionWorkflow and the idempotency key of the baseline
    When checkAppraisalOutlier or flagAppraisalOutlier is retried or exceeds its timeout
    Then each activity declares its retry policy and its timeout in the baseline
    And a repeated write of the decision record is absorbed by the idempotency key and no second decision record is written

  Scenario: C10 A status change the case state does not allow is refused (new, D-RCV-60)
    Given the rwb-case state row of the baseline and the route operation
    When a route request asks for a status change that the case state does not allow
    Then the request is refused with a code of the declared error set of C5
    And no decision record is written and no outlier element is returned
```

The ten criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the consumed rows, the rights, the envelope, the decision-record element, the workflow, the fakes and the boundary. No criterion states a business outcome of the application story, and none asserts a threshold, a market value or a flag.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One owner per operation, row, element and table: the baseline declares the route operation that the Ownership Map gives S1 and names every other row with its owner | Ownership Map rows of S1; TSD S1 T-A.1 | TC-E4-003-01, TC-S1-E4003-CON-01, TC-S1-E4003-CON-07 |
| BR2 | A consumed row with no published owner, operation or element carries the placeholder and its gap and never an invented path, value or transport; the market benchmark row is such a row | Template and Rules v1 §R9; GAP-2597 | TC-S1-E4003-CON-01, TC-S1-E4003-CON-07 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; s9 | TC-S1-E4003-CON-02, TC-S1-E4003-CON-07 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain; ACE facts arrive on the rwb-source-data data product and never on a view of this service | DP-05; ADR-020 | TC-S1-E4003-CON-06, TC-S1-E4003-CON-07 |
| BR5 | The outlier element carries no business value of its own: the gap limit, its unit and the appraisal types are referenced with an identifier and a version and never declared as a number | FSD S1 A2.3.3.1 BR-S1-003; GAP-2596 | TC-S1-E4003-CON-06, TC-S1-E4003-CON-07 |
| BR6 | No event is published by this baseline: the ownership rows give S1 no event, and the decision record reaches the ledger on the shared topic through the library of DP-03 | DP-03; context pack S1 ownership rows | TC-E4-003-04, TC-S1-E4003-CON-07 |
| BR7 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before anything is presented, and its element is declared once for the service | DP-03; legacy RWB-E4-003 AC2 | TC-E4-003-02, TC-S1-E4003-CON-07 |
| BR8 | No personal data in any element, fake, example or log of the baseline | Template and Rules v1 §R7.2 (s17) | TC-S1-E4003-CON-06, TC-S1-E4003-CON-07 |
| BR9 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 | TC-S1-E4003-CON-04, TC-S1-E4003-CON-05, TC-S1-E4003-CON-07 |

### 9. State transitions

The object of this section is the document, not a case: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, row, element, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the six consumed rows are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story and the harness |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | A new optional element only, and the check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | The outlier element gets a published shape | The owner publishes the schema and the draft name is replaced | Baselined, new minor version, and the fakes are updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name or element | X1 | The row carries the placeholder and the gap, and the draft continues |
| In review | A row reaches a foreign schema, base or topic | X4, X7 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X5 | Not tagged, and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-valuation | Authors the baseline, resolves the shape of the service's own operation, the draft outlier element, the workflow elements and the decision-record element, and signs the tag |
| Owner of rwb-source-data (P1) | Reviews the appraisal, acceptance, previous-value and freshness rows, and publishes the operation names when they exist |
| Owner of rwb-case (P3) | Reviews the case-state row, the gap-rule reference row and the case-move answer of the route operation |
| Owner of rwb-decision (P7) | Reviews the rule-in-force row and the decision-record element with the platform library |
| Owner of rwb-access (P4) | Reviews the authorise row and the capability area and rights of the declared operation |
| Owner of rwb-agent (P10) | Publishes the market benchmark row and its owner when the model gateway is contracted; until then the row carries the placeholder |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of the declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write | BR Field ID |
|---|---|---|---|---|
| The appraisal elements of `v_ace_valuation` (DF-ACE-187 to DF-ACE-195) | P1 (`rwb_source_data`) | The appraisal number, type, appraised value and date, the asset key and the prior appraisal used as the previous value; referenced as the data product and not redefined | Consumed | DF-ACE-187 to DF-ACE-195 |
| The acceptance elements of `valuation_ext` (DF-EXT-036 to DF-EXT-049) | P1 data product, acceptance owned by RWB-S1-E4004-APP | `accepted`, `accepted_at`, `accepted_by`, `stale_flag`, `age_days`; referenced with their types and nullability | Consumed | DF-EXT-036 to DF-EXT-049 |
| The market benchmark element | Not specified in the source documents (GAP-2597; ASM-4298) | The market value of the asset, its source name, its source date and its version, declared as an input element of the outlier step under the placeholder and not by a path | Consumed | Not specified in the source documents (GAP-2597; ASM-4298) |
| The gap-rule element | P3 (`rwb_case`) by the default ruling; the row is Not specified in the source documents (GAP-2596; ASM-4297) | The limit, its unit, its valid-from date and its version; declared as a reference and never as a value | Consumed | Not specified in the source documents (GAP-2596; ASM-4297) |
| The case elements of the route operation | P3 (`rwb_case`) | The case reference and its state; referenced, not redefined | Consumed | Not specified in the source documents (DOR-RWB-S1-E4003-CON-7) |
| The rule elements of `rule_row` (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | The rule id, the rule version and the route set in force; referenced, not redefined | Consumed | DF-REF-001 to DF-REF-015 |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_valuation` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time | Written through the library | DF-DEC-001 to DF-DEC-018 |
| The outlier element of the answer | S1, declared here | The two gaps, the flag, its reasons and the rule version, under a draft name with the placeholder of GAP-2602 | Declared | Not specified in the source documents (GAP-2602; ASM-4303) |

The baseline declares no table of its own, because the Ownership Map gives S1 none while TSD S1 T3.1 declares `valuation` as a NEW Workbench table (GAP-2599; ASM-4300). It declares no column, no index and no migration, and it enumerates no business value. **No personal data** appears in any element, fake or example, and every fixture identifier is synthetic.

The reference-data parameters are read under DP-06 and DP-07 and named here: the gap-rule parameters (the limit, its unit, its valid-from date and its version) under DP-06, and the rule_row parameters (the rule id, the rule version and the route set in force) under DP-07; both are referenced and never declared as values.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This is the operation the legacy story names in its Endpoints table, and the only one this baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in, being route, override reason code and note, and `Approval` out, being the decision, its level, its amount and its status, plus the outlier element below (API-S1-001; TSD S1 T-A.2) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat |
| The outlier element of the answer | Part of `Approval` | The two gaps, the flag, its reasons, the threshold version and the rule version; declared as an additive optional element of `Approval` under the draft name `appraisalOutlier`, typed and nullable, renamable at the tag, with its shape published in the S1 API file; the shape is marked Not specified in the source documents (GAP-2602; ASM-4303) | As the operation | As the operation |

The two valuation operations of the map, `POST /assets/{assetId}/valuations` and `POST /assets/{assetKey}/valuations`, are S1's and are not declared here: they are the appraisal-intake slice of RWB-S1-E4002-CON. The error envelope of the declared operation: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The appraisal, acceptance and previous-value data-product read (operation name Not specified in the source documents (GAP-2600; ASM-4301)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The new value, its date and type, the acceptance of `valuation_ext`, the previous appraisal and the freshness stamp; faked |
| The market benchmark read (owner, operation and path Not specified in the source documents (GAP-2597; ASM-4298)) | Not published; the FSD names a model gateway | Not specified (GAP-2597) | The market value of the asset, its source and its date; faked |
| The gap-rule reference read (operation name Not specified in the source documents (GAP-2600; ASM-4301)) | `/api/recovery/case/v1` | P3 rwb-case, by the default ruling | The limit in force with its unit and its version; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state and its asset link, checked before the step runs; faked |
| The rule-in-force and decision-log read (operation name Not specified in the source documents (GAP-2600; ASM-4301)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name or a path is not published the row carries the placeholder and no path, so the consumer adapts at the tag instead of inventing a surface (BR2). The plan gives this slice no C dependency, so every row is built against its fake.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event: the topic `rwb.valuation.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this baseline declares no event, no event name and no outbox row on it (ASM-4301). The only publication of this step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service.

#### 12.4 Events consumed

None declared. FSD S1 A2.3.2 names three possible triggers of the step, "a completed ACE batch, an event or a timer", and R-DIS-16 has the valuer report the value; no source publishes an event name for any of them and the ownership rows give S1 no job, so the baseline declares no subscription; the check starts from the value step of `RouteDecisionWorkflow` and from the re-assessment that follows a new or corrected appraisal (GAP-2601; ASM-4302). The freshness of the ACE data product is read as an element of the rwb-source-data row and not as a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` | Input: the case, the asset key, the route set and the rule package in force; signals: the freshness answer of the data product and the outcome of the value step |
| `checkAppraisalOutlier` | Activity | `rwb-valuation` | The new value, the market benchmark, the previous value and the gap rule in force in; the two gaps, the flag, the threshold version and the rule version out |
| `flagAppraisalOutlier` | Activity | `rwb-valuation` | The appraisal, the two gaps and the flag in; the decision record, the idempotency row and the step outcome out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1. This baseline fixes its input, its two signals and the two activities the step adds; the remaining activities of the route decision are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable. Its workflow ID form is Not specified in the source documents (CG-ALL-7990); it is started by CaseWorkflow as a child (Temporal Catalog v1, Workflows), and its duplicate-start policy is Not specified in the source documents (CG-ALL-7990).

#### 12.6 Schedules

None. The ownership rows give S1 no job, and this baseline declares no Temporal Schedule and no legacy Quartz job. A batch-completion or valuer-report trigger would be a Schedule or a subscription of this service and no source names one (GAP-2601; ASM-4302).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table, while TSD S1 T3.1 declares `valuation` as a NEW Workbench table and the FSD holds the acceptance in `recovery.valuation_ext` (GAP-2599; ASM-4300) |
| decision_record | PLT library, created in `rwb_valuation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `proceeds` (P8), `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), every `v_ace_*` view (P1) and `valuation_ext` as an ACE-schema object are named by their owner and never declared here. If the S1 table owner confirms `valuation`, the DB story of this service creates it in its own Flyway sequence and this baseline declares its elements in a minor version. Until the data owner of rwb-valuation decides, the flag, its reasons and the two gaps are kept in the local decision record for wave 3 (GAP-2599; ASM-4300).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | Asset `AST-2026-000403` with its new appraisal, its value, its acceptance and its previous appraisal; an asset with no previous appraisal; a stale product with its date; no answer beyond 2 s | C3, C4, C6 |
| Market benchmark fake | The market value of asset `AST-2026-000403` with its source and its date; an asset with no benchmark, answered under the placeholder | C3, C6 |
| rwb-case reference-data fake | The gap rule in force with its unit and its version; a rule that cannot be resolved, answered under the placeholder | C3, C6 |
| rwb-case case-state fake | Case `RC-2026-000403` at the route assessment with its asset link; a case in another state | C3, C6 |
| rwb-decision rule and log fake | The rule id and the version in force; the record the ledger holds, once and twice | C3, C6 |
| rwb-access authorise fake | The capability area Treatment and offer, right U accepted and refused | C5 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000403`, with the value, the two gaps and the flag read once | C2, C6 |
| Compatibility corpus | The previous tag, an additive draft and a breaking draft | C1, C7 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The rows whose owners, names and elements are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2597, GAP-2600).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data data-product row, the market benchmark row, the gap-rule row, the rwb-case state row, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no declared subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `checkAppraisalOutlier` and `flagAppraisalOutlier` on `rwb-valuation`; no Schedule |
| File | None declared | The appraisal report travels through SVAF and rwb-integration, and this baseline declares no file of this service (GAP-2597) |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S1 rwb-valuation (Valuation and route)/RWB S1 E4003 CON Flag appraisal outliers against market and last value - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S1-E4003.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operation and its added element, the six consumed rows, the publication, the workflow and its activities, the tables, the fakes, the call-type summary, the data elements and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Fakes.** One per consumed row plus the composite route, the stopped chain and the compatibility corpus, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C6).

**Done when.** The seven criteria pass, the reviewers have closed their comments, the compatibility check passes on the tag, the nine fakes are published with their documented answers, and RWB-S1-E4003-APP and the wave 3 harness can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Treatment and offer right calls the declared operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `RouteRequest` is absent or invalid | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the appraisal row is stale | {product} is from {date}. Today's load has not arrived. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A row or an element is not published | Not specified in the source documents (GAP-2602; ASM-4303). |

The four message IDs are those of FSD S1 A2.3.3.1, of the legacy message set of the key and of the platform set, copied unchanged. The two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-13 Route decision through the gateway-bff composite route (DP-19). What this story fixes is the element list of the value part of the answer and the states the screen can show from this service's answer.

| Screen | States | What the route reads on this service |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted; empty, error and no access: Not specified in the source documents (CG-ALL-7995) | The value and its date, the two gaps, the flag and its reasons, the outlier element with its rule version, and the override reason of the submission |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The route itself, its merge order and its field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-003-01 | C2, C3: the route answer with its outlier element and the consumption of the six rows by a consumer built on the fakes | Contract | The published schema, the recorded answers of case `RC-2026-000403` and the six fakes |
| TC-E4-003-02 | C4, C6: the decision-record element and the stopped chain | Contract | The decision-record element, a healthy stub and a stopped stub |
| TC-E4-003-03 | C5: the rights and the error envelope of the declared operation | Contract | A request per right, including a role without it; one request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-003-04 | C1, C7: the compatibility check, the boundary and the empty publication | Contract | The previous tag, an additive draft, a breaking draft and an outbox declaration that must stay empty |
| TC-S1-E4003-CON-01 | C3: the placeholder and the gap of an unpublished owner, operation or element | Contract | The six consumed rows, each with and without a published name, including the market benchmark row |
| TC-S1-E4003-CON-02 | C2: the outlier element as an addition and never as a replacement | Contract | A draft that replaces a published element and a draft that adds one |
| TC-S1-E4003-CON-03 | C6: the fakes and the workflow elements | Contract | The nine fakes and one fake that answers more than its document |
| TC-S1-E4003-CON-04 | C7: the naming and boundary rule | Contract | A draft that names a foreign schema, a monolith base, a foreign topic or a Schedule |
| TC-S1-E4003-CON-05 | C4, §12.7: the table-ownership boundary | Contract | A draft that declares a column, an index, a migration or a table of another owner, and a valuation table before the S1 owner confirms it |
| TC-S1-E4003-CON-06 | BR4, BR5, BR8: the one-hop timeout, no value declared as a number and no personal data | Contract | A consumed row answered after its 2 s timeout; a fake or example holding a number as a gap limit; a fake or example holding a personal-data field |
| TC-S1-E4003-CON-07 | C8: the business rules BR1 to BR9 each with a passing check | Contract | The section 8 rules and the baseline with its element list, operation table and boundary checks |
| TC-S1-E4003-CON-08 | C9: the retry and timeout of each activity and the absorbed repeated write | Contract | The workflow table of the baseline, a retried activity and a repeated write under the same idempotency key |
| TC-S1-E4003-CON-09 | C10: the refused status change | Contract | The rwb-case state row, a route request for a status change the case state does not allow, and the declared error set |

The four legacy case IDs are the legacy test cases of RWB-E4-003 in their legacy order, mapped onto this contract deliverable: the comparison and its elements on the fakes (01), the failure of the decision log (02), the access path (03) and the principle-5 record failure (04). The four `TC-S1-E4003-CON-` cases are new and test the parts of the baseline no legacy case touches. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the baseline: the gap limit, its unit, the appraisal types of `LOV-APPRAISAL` and the route codes of `LOV-ROUTE` are referenced with their identifier, list or version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the value and the acceptance appear only as the rwb-source-data data product (DP-05).
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case` element and no `rule_row` element is declared as this service's own.
- The market model stays with rwb-agent: the baseline declares the benchmark as an input element with a placeholder and makes no model call a dependency of S1 (GAP-2597).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-003, disposition Split (rework); this story carries no legacy criterion, and AC1 and AC2 are owned by RWB-S1-E4003-APP | 1, 11, 12, 16 |
| Feature | FEAT-VAL-03 Flag appraisal outliers against market and last value, module S1, epic E4, depends on FEAT-VAL-02 | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.3.2 steps and integration points; A2.3.3.1 VR-S1-003-1 and BR-S1-003; A2.3.3.3 roles; requirements REQ-S1-002 and REQ-S1-008; SCR-13 | 2, 3, 8, 12, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation`; T3.2 `LOV-APPRAISAL` and `LOV-ROUTE`; T5.2; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 16 |
| API Specification v5 | `/cases/{caseId}/route`, `RouteRequest` and `Approval`, and the 401, 403, 404, 409, 422 and 503 responses | 3, 12 |
| Logical data model | DF-ACE-187 to DF-ACE-195, DF-EXT-036 to DF-EXT-049, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-COL-018 to DF-COL-027 and DF-COL-043 to DF-COL-044 | 11 |
| Routing logic | R-UNI-38, R-UNI-39 and R-UNI-40; R-DIL-09 and R-DIL-12; R-DIS-16 to R-DIS-18; no S1 route rule is in force, because the S1 package is Phase 2 | 8, 14 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2596, -2, -4, -5, -6 and -7; ASM-4297, -2, -4, -5, -6 and -7 | 1, 3, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The comparison, the flag, the decision records, the idempotency of the command and the screen behaviour: RWB-S1-E4003-APP.
- The appraisal order, the appraisal intake and the acceptance of the value: RWB-S1-E4001-CON, RWB-S1-E4002-CON and RWB-S1-E4004-CON.
- The market model, the model gateway and the valuation agent, their version, their confidence and their fallback: rwb-agent (P10) and the platform (GAP-2597).
- The ACE appraisal, acceptance and previous-value facts and the freshness of the data product: rwb-source-data (P1); the store of `valuation_ext` and of any `valuation` table: the data owner of this service (GAP-2599).
- The case of record, its route states, its reference data and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, the gap rule's value, its approval and the central ledger: rwb-decision (P7) and the business owner (GAP-2596).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, RWB-ITG-E4003-ITG.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
