# RWB-S1-E4007-CON Score the routes and recommend one with reasons - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4007-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19, DP20 |
| Parallel lane | CG-W3 |
| Ready to start | After RWB-S1-E4005-APP, RWB-S1-E4006-APP |
| Size | Not specified in the source documents (DOR-RWB-S1-E4007-CON-16); fit to a two-week iteration: Not specified in the source documents (DOR-RWB-S1-E4007-CON-15) |
| Depends on (build) | RWB-S1-E4005-APP, RWB-S1-E4006-APP |
| Contract dependencies | RWB-P10-TE013-CON |
| Contract version | API Specification v5 (rwb-valuation.yaml) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-007, the baseline the route-scoring and recommendation step of rwb-valuation builds against on Day 1. The baseline declares the recommendation elements of the route-decision operation `POST /cases/{caseId}/route` (API-S1-001) on `/api/recovery/valuation/v1` as an additive slice of the operation RWB-S1-E4001-CON baselines (DP-13), the five consumed rows of rwb-source-data, rwb-agent, rwb-case, rwb-decision and rwb-access (DP-05), the recommendation element and the decision-record library that carries it (DP-03), the elements of `RouteDecisionWorkflow` and its two activities, the rights, the error envelope and the fakes; it publishes no event, because the ownership rows give S1 none. The operation names of the five consumed rows are not published (GAP-2621; ASM-4324); the recommendation element set, the reasons and the alternatives are not published and the operation already carries another slice of this service (GAP-2622; ASM-4325); no S1 route-decision rule package, decision code, confidence threshold or route-code mapping is in force (GAP-2623; ASM-4326); the agent client of DP-20 and its C row are outside this key's pattern set (GAP-2625; ASM-4328); no source fixes the store of the recommendation (GAP-2626; ASM-4329); the mapping of `LOV-ROUTE` onto the eight routes is not published (GAP-2628; ASM-4331). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S1-E4007-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 15 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-valuation**, I want **the published contract baseline of the route-scoring and recommendation step of rwb-valuation, being its recommendation elements on the route operation, its five consumed rows, its decision-record element, its workflow elements, its rights, its error envelope and its fakes, fixed and tagged before the build starts**, so that **the application story and the five owners it consumes can build and test on Day 1 against one versioned surface instead of guessing the shape of a neighbour's answer or of the agent's recommendation**.

This is the contract slice of legacy RWB-E4-007. It owns:

- the document that fixes the recommendation elements of `POST /cases/{caseId}/route` (API-S1-001) on base `/api/recovery/valuation/v1`: the recommended route code, the expected return of each route, the reasons, the alternatives, the confidence, the model codes and versions, the rule version, the `Idempotency-Key` header and the scope rule (DP-13);
- the five consumed rows: the COLLINS score data product of rwb-source-data, the route-agent call of rwb-agent, the case state and open route set of rwb-case, the rule-in-force and decision-log read of rwb-decision, and the authorise operation of rwb-access, each with its owner, its use, its budget and a placeholder where the name is not published (DP-05);
- the recommendation element and the decision-record element, the library that carries it and the shared topic it reaches (DP-03);
- the elements of `RouteDecisionWorkflow` and its two activities on task queue `rwb-valuation`;
- the subject of SCR-13 Route decision, one hop through the gateway-bff composite route (DP-19); the no-access state of SCR-13 maps to the 403 of the error set and its error state to the 503 of the error envelope, and its empty and loading states are Not specified in the source documents (DOR-RWB-S1-E4007-CON-10), the screen behaviour being RWB-S1-E4007-APP's;
- the fakes and their documented answers, including the low-confidence, out-of-set and no-answer answers of the agent;
- the reference data the route step reads under the reference-data contract (DP-06, DP-07): the route code list LOV-ROUTE and the parameters in force, which are Not specified in the source documents (DOR-RWB-S1-E4007-CON-20);
- the naming, versioning and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no monolith base, additive only.

It does not own: the scoring, the ranking, the recommendation, the decision records and the screen behaviour, which are RWB-S1-E4007-APP; the appraisal slice of the same operation, which is RWB-S1-E4001-CON; the COLLINS call and the return it records per route, which are RWB-S1-E4005-CON; the payoff and the settlement range, which are RWB-S1-E4006-CON; the approval elements of the operation, which are RWB-S1-E4008-CON and its siblings; the agent runtime, its models and its autonomy, which are rwb-agent's (P10) and its own baseline; the ACE score, collateral and account facts, which are rwb-source-data's (P1); the case of record and its route states, which are rwb-case's (P3); the rule rows and the central ledger, which are rwb-decision's (P7); the roles and scopes, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets two teams and five owners start together. Legacy RWB-E4-007 asks for a recommendation with its reasons and its alternatives, recorded with the rule version, so the step reads a score per route from one service, calls an agent in another, checks the case in a third, reads the rule version in a fourth and writes one record. Without a tagged baseline each of those shapes would be discovered at the first integration instead of at the review.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner, its use and its 2 s budget, and every row whose name is not published carries the placeholder and its gap (GAP-2621; ASM-4324).
- **one hop, one budget, one check.** Each consumed row is a single hop with a 2 s timeout and a breaker, the score is never read from a table, and no chain runs through a second service (DP-05, ADR-020). The agent answer is declared with the schema check and the confidence element the caller applies, so the shape of a refusal is part of the surface (NFR-055).
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document. The recommendation elements are added to the operation another baseline declares as exactly such a minor version, and no path, no base and no queue changes (GAP-2622).

The business outcome the baseline protects is the one FEAT-VAL-07 states: the route agent recommends a route and states the reasons and the alternatives. The baseline states no outcome and no business value of its own, and no criterion here asserts that a route is recommended.

### 3. Preconditions

- The Ownership Map rows for S1 are in force: `POST /assets/{assetId}/valuations`, `POST /assets/{assetKey}/valuations` and `POST /cases/{caseId}/route`; no table, no event, no job, and one workflow, `RouteDecisionWorkflow`. This baseline declares the third operation only, and only its recommendation slice.
- The service naming is fixed: schema `rwb_valuation`, one login of its own, base `/api/recovery/valuation/v1`, topic `rwb.valuation.events.v1` with `.retry` and `.dlt`, task queue `rwb-valuation` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.valuation`.
- TSD S1 is the shape of record for the service: T-A.1 gives API-S1-001 with right Treatment and offer U; T-A.2 gives `RouteRequest` in, `Approval` out, errors 401, 403, 404, 409, 422 and 503 and the `Idempotency-Key`; T3.1 gives `score` as REUSE ACE with DF-DEC-019 to DF-DEC-027; T3.2 gives `LOV-ROUTE`; T6.1 gives the capability area and its rights.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions of this baseline and not in its H row.
- RWB-S1-E4001-CON has baselined the same operation with the appraisal and approval elements; this baseline adds the recommendation elements to it in a minor version and declares no second path (GAP-2622; ASM-4325).
- The agent row names rwb-agent as its owner, the route agent as its subject and D6.3 as the sub-decision it serves; its client contract of DP-20, `RWB-P10-TE013-CON`, is not in this key's pattern set, so the row is declared with the placeholder and the gap (GAP-2625; ASM-4328).
- No S1 route-decision rule package, decision code or confidence threshold is in force, and the mapping of `LOV-ROUTE` onto the eight routes is not published; the baseline references each with its identifier and asserts none (GAP-2623, GAP-2628; ASM-4326, ASM-4331).
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S1 T-A.1, T-A.2, T3.1, T3.2 and T6.1, the FSD S1 A2.7 rules, the Agent Catalog row of the route agent and the DP table.
2. The recommendation elements are declared against the operation RWB-S1-E4001-CON already publishes, as an additive minor version of it.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The agent row is declared with the sub-decision it serves, the check the caller applies to its answer and the refusal shapes the caller must recognise.
5. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins.
6. The workflow and its two activities are declared with their input, their signals and their outcome elements.
7. The schema, the open lists and the closed lists are published; a closed list is referenced with its identifier and its version and is never enumerated in code.
8. The fakes are declared with their documented answers, one per consumed row, one per agent refusal shape and one for the composite route.
9. The compatibility check runs on the draft against the previous tag of the operation: a breaking change fails it, and the additive slice passes.
10. The document goes to review as Draft; the reviewers are the owners of the five consumed rows, the tech lead of the service and the reviewer of the access matrix.
11. On the review's close the document is tagged; the application story starts against the tag and the fakes, and the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and its gap; no path, no element and no model code is invented | C3, C4 |
| X2 | A change removes, renames, retypes or newly requires an element of the operation | The compatibility check fails and the document needs a new major version | C1 |
| X3 | The recommendation slice is declared as a second operation, a second path or a second base | The review refuses the baseline: one operation, one base, additive only | C2, C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C6 |
| X5 | The rights of the operation are not a row of the access matrix | The recommendation elements are not declared and the error set stays incomplete | C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a version, this document follows in a minor or major version, and the fake is updated | X2 |
| X7 | A row declares a model code, a threshold, a weight, a return or a route mapping the sources do not publish | The element is declared as a reference with its identifier and its version, and never as a literal | C4, C5 |

X1 to X3 are the paths of an incomplete or misplaced slice, X4 to X6 the paths of a baseline moving under a build, and X7 the no-invented-value rule.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order and the fake data are this story's choice; the path, the request, the answer, the rights and the error set are fixed by TSD S1 |
| Valuable | Two teams and five owners build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, one provided operation and one additive element group, five consumed rows, one decision-record element, one workflow with two activities, one subject of SCR-13 and seven fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the route-scoring and recommendation step

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The recommendation elements are published as an additive slice of the route operation (new, D-RCV-60)
    Given the operation table of the baseline
    When POST /cases/{caseId}/route on /api/recovery/valuation/v1 is read
    Then it names RouteRequest in, Approval out, the recommendation elements, the Idempotency-Key header and the scope rule of T-A.2
    And it declares no second path, no second base and no second operation

  Scenario: C3 The five consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-source-data, rwb-agent, rwb-case, rwb-decision and rwb-access are read
    Then each row names its owner, its use, one hop and a 2 s budget
    And where the operation name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C4 The recommendation, the alternatives and the reasons are declared as elements with their sources (new, D-RCV-60)
    Given the recommendation elements and the data-element table of the baseline
    When the recommended route, the return of each route, the reasons, the alternatives, the confidence and the versions are read
    Then each element carries its type, its nullability and its source
    And the route code references LOV-ROUTE and no model code, return, weight or threshold is declared as a literal

  Scenario: C5 The rights, the error envelope and the refusal shapes of the agent are declared (new, D-RCV-60)
    Given the operations and the consumed rows the baseline provides
    When the rights, the error set and the agent refusal shapes are read
    Then the operation names the capability area Treatment and offer and the right of the access matrix
    And the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503 in one problem envelope
    And the agent row names the schema check, the confidence element and the fallback the caller applies

  Scenario: C6 The decision-record element, the workflow elements and the fakes are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the workflow table and the fake table are read
    Then the element names RWB-PLT-E1027-CON as its library, the shared topic and the transaction it joins
    And RouteDecisionWorkflow and its two activities name their input, their signals and their task queue
    And every consumed row has a fake with a documented answer, including the low-confidence, out-of-set and no-answer answers of the agent and the stopped decision-record stub

  Scenario: C7 The naming, the publication and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue, the schema and the outbox of the baseline
    When the document is checked against the naming rule, the ownership rows and the event list
    Then one base, one topic, one queue and one login are declared and no monolith base and no foreign topic appear
    And no event is published, because the ownership rows give S1 none, and no Schedule is declared

  Scenario: C8 Each business rule BR1 to BR10 is held by a criterion or a boundary test (new, D-RCV-60)
    Given the business rules table of section 8
    When the baseline is checked against each rule
    Then each rule BR1 to BR10 is held by a criterion of this story or by a boundary test
    And a rule with neither a criterion nor a boundary test fails the check

  Scenario: C9 A retried or timed-out activity repeats the same request under the same key (new, D-RCV-60)
    Given the two activities of RouteDecisionWorkflow and the consumed rows of the baseline
    When an activity is retried or a consumed call reaches its 2 s timeout
    Then the retry sends the same request with the same Idempotency-Key header
    And the timed-out call is not chained to a second consumed row

  Scenario: C10 A status change the closed list does not allow is refused (new, D-RCV-60)
    Given the closed lists and the operation table of the baseline
    When a request asks for a status change the closed list does not allow
    Then the operation refuses it in the problem envelope of C5
```

The seven criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the lists, the consumed rows, the rights, the envelope, the agent refusal shapes, the decision-record element, the workflow, the fakes and the boundary. No criterion states a business outcome of the application story, and none asserts that a route is scored, that a recommendation is made or that a rule fires.

```gherkin
Feature: Business rules of the contract baseline

  Scenario: C11 The ownership, the placeholder, the additive version and the single hop hold (new, D-RCV-60)
    Given the ownership rows, the consumed operation table and the version rule of the baseline
    When the rules BR1, BR2, BR3 and BR4 are checked against the document
    Then each operation, row, element and table has one owner and every other row names its owner
    And a consumed row with no published operation name carries the placeholder and its gap, and no invented path, parameter or model code
    And the baseline is additive, a new optional element is a minor version, and every consumed row is one hop with a 2 s timeout and a breaker

  Scenario: C12 The event, the decision record, the value, the agent and the personal-data rules hold (new, D-RCV-60)
    Given the event list, the decision-record element, the value declarations, the agent row and the examples of the baseline
    When the rules BR5 to BR10 are checked against the document
    Then no event is published and the decision record is written through RWB-PLT-E1027-CON in the caller's transaction
    And no business value is declared as a literal and the agent row declares what the caller checks, never what the agent decides
    And no personal data appears in any element, fake, example, prompt or log, and no other service's table, operation or topic is declared
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, row, element and table: the baseline declares the recommendation slice of the route operation that the Ownership Map gives S1 and names every other row with its owner | Ownership Map rows of S1; TSD S1 T-A.1 |
| BR2 | A consumed row with no published operation name carries the placeholder and its gap and never an invented path, an invented parameter or an invented model code | Template and Rules v1 §R9; GAP-2621 |
| BR3 | The baseline is additive and sits on one operation: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version; the recommendation slice is one document family with the baseline of RWB-S1-E4001-CON, as a minor version | ADR-020; GAP-2622 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain; ACE facts arrive on the rwb-source-data data product and never on a view of this service | DP-05; ADR-020 |
| BR5 | No event is published by this baseline: the ownership rows give S1 no event, and the decision record reaches the ledger on the shared topic through the library of DP-03; the route agent's result reaches this service through the agent contract, and EV-28 stays P10's event | DP-03; context pack S1 ownership rows |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service; it holds the routes considered, the values and returns used, the recommendation with its reasons, confidence and alternatives, the approval with its level, and the rule and model versions, and its physical field list stays open | DP-03 |
| BR7 | No business value is declared in the baseline: the route codes, the returns, the weights, the confidence threshold and the open route set are referenced with their identifier, their list or their version; the eight routes are named as Arch v5 slide 3 names them and no route number is printed | TSD S1 T3.2; FSD S1 A2.7.3.1 BR-S1-007; Arch v5 slide 3; GAP-1688 |
| BR8 | The agent row declares what the caller checks and never what the agent decides: the schema check, the confidence element and the fallback are part of the surface, and the autonomy level is the agent's own | NFR-051, NFR-055; Agent Catalog, Route agent |
| BR9 | No personal data in any element, fake, example, prompt or log of the baseline | Template and Rules v1 §R7.2 (s17); NFR-052 |
| BR10 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

### 9. State transitions

The object of this section is the document, not a case: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, row, element, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the five consumed rows are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes on the previous tag of the operation | Baselined, tagged for the application story |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | A new optional element only, and the check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer | X6 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name | X1 | The row carries the placeholder and the gap, and the draft continues |
| Being authored | A row declares a model code, a threshold or a route mapping | X7 | The value is replaced by a reference with its identifier and its version |
| In review | The slice is declared as a second operation or path | X3 | The baseline is refused and the elements move into the operation that exists |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-valuation | Authors the baseline, resolves the shape of the recommendation elements, the workflow elements and the decision-record element, and signs the tag |
| Owner of rwb-source-data (P1) | Reviews the score, the collateral and the freshness rows, and publishes the operation names when they exist |
| Owner of rwb-agent (P10) | Reviews the route-agent row, its model codes, its confidence element and its refusal shapes, and publishes the operation name and the autonomy level when they exist |
| Owner of rwb-case (P3) | Reviews the case-state row, the open route set and the case-move answer of the operation |
| Owner of rwb-decision (P7) | Reviews the rule-in-force row, the decision code of D6.3 and the decision-record element with the platform library |
| Owner of rwb-access (P4) | Reviews the authorise row, the capability area and the rights of the declared operation |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Owner of RWB-S1-E4001-CON | Confirms that the recommendation elements are an additive slice of the operation it declared |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of section 9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write | BR Field ID |
|---|---|---|---|---|
| The score elements of `v_ace_score` (DF-ACE-270 to DF-ACE-279) | P1 (`rwb_source_data`) | score_key, account_key, model_code, model_version, score_value, estimate_value, route_code, scored_at; referenced as the data product and not redefined | Consumed | BR4, BR7 |
| The `score` shape of TSD S1 T3.1 (DF-DEC-019 to DF-DEC-027) | P1 data product, REUSE ACE | The same nine fields, declared as the shape the data product answers and not as a table of this service | Consumed | BR4, BR7 |
| The collateral and valuation elements (DF-ACE-091 to DF-ACE-098, DF-ACE-187 to DF-ACE-195) | P1 (`rwb_source_data`) | The collateral number, the asset key and the accepted value the return rests on; referenced only | Consumed | BR4, BR7 |
| The agent answer elements | P10 (`rwb_agent`) | The recommended route code, the reasons, the alternatives, the figures they rest on, the model codes and versions, the confidence; the operation name is Not specified in the source documents (GAP-2621; ASM-4324) | Consumed | BR2, BR8 |
| The case elements of the route operation | P3 (`rwb_case`) | The case reference, its state, its product group and the open route set; referenced, not redefined | Consumed | BR1, BR4 |
| The rule elements of `rule_row` (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | The rule id, the rule version and the route set in force; referenced, not redefined | Consumed | BR7 |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_valuation` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time | Written through the library | BR6 |
| The recommendation elements | rwb-valuation (S1) | The recommended route code, the return of each route, the reasons, the alternatives, the confidence and the versions; no store is fixed by a source (GAP-2626; ASM-4329) | Provided in the answer and recorded in the decision record only (GAP-2626; ASM-4329) | BR1, BR3 |

The baseline declares no table of its own, because the Ownership Map gives S1 none while `score` is declared as REUSE ACE in TSD S1 T3.1 (GAP-2626; ASM-4329). It declares no column, no index and no migration, and it enumerates no business value: every list, code, return and threshold is referenced with its identifier and its version, and the mapping of `LOV-ROUTE` onto the eight routes is left open (GAP-2628; ASM-4331). **No personal data** appears in any element, fake or example, and every fixture identifier is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This is the operation the legacy story names in its Endpoints table, and the only one this baseline declares. Its appraisal and approval elements are RWB-S1-E4001-CON's; the recommendation elements below are this baseline's, added in a minor version of the same document family.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, with the recommendation elements: the recommended route code of `LOV-ROUTE`, the expected return of each open route, the reasons, the alternatives with their returns and the figure each rests on, the confidence, the model codes and versions, the rule version and the override reason where the answer departs from the recommendation (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second assessment runs |
| None | The scoring and the agent call | No source names a published operation for the scoring or for the agent call of this service: the score arrives on the rwb-source-data row and the recommendation on the rwb-agent row, so the row carries the placeholder Not specified in the source documents (GAP-2621; ASM-4324) and no path is declared | Not applicable | Not applicable |


The error envelope of the declared operation: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library, the agent or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The COLLINS score data-product read (operation name Not specified in the source documents (GAP-2621; ASM-4324)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The score, its model code and version, the return per route, the account and collateral links and the freshness stamp; faked |
| The route-agent call (operation name Not specified in the source documents (GAP-2621; ASM-4324)) | `/api/recovery/agent/v1` | P10 rwb-agent | The recommended route, the reasons, the alternatives and the confidence, with the model codes and versions, under the caller's service identity; faked; the client contract of DP-20 is outside this key's pattern set (GAP-2625; ASM-4328) |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state, its product group and the open route set the recommendation is bounded by; faked |
| The rule-in-force and decision-log read (operation name Not specified in the source documents (GAP-2621; ASM-4324)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force for the business date, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag instead of inventing a surface (BR2). The plan gives this slice no C dependency, so every row is built against its fake.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event: the topic `rwb.valuation.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this baseline declares no event, no event name and no outbox row on it (ASM-4324). The only publication of this step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service.

#### 12.4 Events consumed

None declared. FSD S1 A2.7.2 names three possible triggers of the step, "a completed ACE batch, an event or a timer", and no source publishes an event name for any of them; the ownership rows give S1 no job and no event, so the baseline declares no subscription; the step runs inside RouteDecisionWorkflow only, started by the route command, and a score-landing or timer trigger is added only if the data owner publishes a readiness event or the service owner adds a Schedule (GAP-2627; ASM-4330). The freshness of the ACE data product is read as an element of the rwb-source-data row and not as a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` | Input: the case, the open route set, the returns of the routes, the range and the rule package in force; signals: the freshness answer, the agent answer and the fallback outcome |
| `scoreRoutes` | Activity | `rwb-valuation` | The open route set, the return of each route and the range in; the ranked routes, the figures and the gaps out |
| `recommendRoute` | Activity | `rwb-valuation` | The ranked routes, the agent request and the rule version in; the recommendation, the reasons, the alternatives, the confidence, the decision record and the step outcome out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1. Workflow ID form: Not specified in the source documents (CG-ALL-8116). Start rule: started by CaseWorkflow as a child when the case reaches route decision D6 or is reopened (ROUTE_D6_REOPEN); duplicate-start policy: Not specified in the source documents (CG-ALL-8116). This baseline fixes its input, its three signals and the two activities the step adds; the remaining activities of the route decision are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S1 no job, and this baseline declares no Temporal Schedule and no legacy Quartz job. A batch-completion trigger would be a Schedule of this service and no source names one (GAP-2627; ASM-4330).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table, and TSD S1 T3.1 declares `score` as REUSE ACE; the store of the recommendation, its reasons and its alternatives is not fixed (GAP-2626; ASM-4329) |
| decision_record | PLT library, created in `rwb_valuation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), every `v_ace_*` view and the `score` object of ACE (P1) are named by their owner and never declared here. If the S1 data owner confirms a table of this service, the DB story creates it in its own Flyway sequence and this baseline declares its elements in a minor version.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | Case `RC-2026-000407` with three open routes and the return of each from model `CRR_RET_380` at its version; one route without a return; a stale product with its date; no answer beyond 2 s | C3, C4, C6 |
| rwb-agent route-agent fake | The recommended route R2 with its reasons, the alternatives, the model codes and versions and a confidence above the threshold; an answer below the threshold; an answer naming a route outside the open set; an answer that fails the schema check; no answer beyond 2 s | C5, C6 |
| rwb-case case-state fake | Case `RC-2026-000407` at the route decision with its product group and open route set; a case with R1 barred; a case in another state | C3, C6 |
| rwb-decision rule and log fake | The rule id and the version in force for the business date; the fallback answer of the rules; the record the ledger holds, once and twice | C3, C6 |
| rwb-access authorise fake | The capability area Treatment and offer, right U accepted and refused | C5 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000407`, with the recommendation, the returns, the reasons and the confidence read once | C2, C6 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2621; ASM-4324). No fake returns a real customer fact.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data data-product row, the rwb-agent route-agent row, the rwb-case state row, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no declared subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `scoreRoutes` and `recommendRoute` on `rwb-valuation`; no Schedule |
| File | None declared | No file leaves or enters this slice; the scores arrive on the rwb-source-data data product and the recommendation on the rwb-agent call (GAP-2621) |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S1 rwb-valuation (Valuation and route)/RWB S1 E4007 CON Score the routes and recommend one with reasons - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S1-E4007.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-20 is named by the DP table for the agent client (`C RWB-P10-TE013-CON`) and is not in this key's pattern set, so the baseline declares the agent row with its placeholder and records the absence rather than adding a contract dependency the plan does not hold (GAP-2625; ASM-4328).

**Sections and owners of the review.** The document is written in nine parts: the provided operation and its additive slice, the five consumed rows, the publication, the workflow and its activities, the tables, the fakes, the call-type summary, the data elements and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag of the operation, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version; the recommendation elements pass as a minor version (C1, BR3).

**Fakes.** One per consumed row, one per agent refusal shape and one for the composite route, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C6).

**Done when.** The seven criteria pass, the six reviewer roles and the owner of RWB-S1-E4001-CON have closed their comments, the compatibility check passes on the tag, the seven fakes are published with their documented answers, and RWB-S1-E4007-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Treatment and offer right calls the declared operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `RouteRequest` or of the recommendation answer is absent or invalid | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the score row is stale | {product} is from {date}. Today's load has not arrived. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published operation name | Not specified in the source documents (GAP-2621; ASM-4324). |

The four message IDs are those of FSD S1 A2.7.3.1 and of the platform set, copied unchanged. The two document rules are checks of this story and are not service messages. The agent's low-confidence and no-answer paths carry no message: the caller records the fallback and, where the rules give no answer, raises the case on the owner's queue with the reasons.

### 15. Screens and states

The baseline serves SCR-13 Route decision through the gateway-bff composite route (DP-19). What this story fixes is the element list of the recommendation answer and the states the screen can show from this service's answer.

| Screen | States | What the route reads on this service |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted; empty: Not specified in the source documents (CG-ALL-8121); error and no access: 503 and 403 as section 1 maps them | The recommended route, the return of each route, the reasons, the alternatives, the confidence, the rule version and the override reason of the submission; plus the held state where a route has no return and the fallback state where the rules answered |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The route itself, its merge order and its field list are RWB-PLT-N001-CON, and the approve action is RWB-S1-E4008-APP's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-007-01 | C1, C2: the schema, the recommendation elements and the closed lists of the route answer | Contract | The published schema and the recorded answers of case `RC-2026-000407` with three open routes |
| TC-E4-007-02 | C4, C6: the decision-record element and the stopped chain | Contract | The decision-record element, a healthy stub and a stopped stub |
| TC-E4-007-03 | C5: the rights and the error envelope of the declared operation | Contract | One request per right, including a role without it; one request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-007-04 | C3, C7: the five consumed rows, the boundary and the empty publication | Contract | The five consumed rows with and without a published name; the base, the topic, the queue and the schema; an outbox declaration that must stay empty |
| TC-S1-E4007-CON-01 | C3: the placeholder and the gap of an unpublished operation name | Contract | The five consumed rows, each with and without a published name |
| TC-S1-E4007-CON-02 | C5: the agent refusal shapes and the check the caller declares | Contract | The above-threshold answer, the low-confidence answer, the out-of-set route, the schema failure and the no-answer case |
| TC-S1-E4007-CON-03 | C6, C7: the fakes, the workflow elements and the naming rule | Contract | The seven fakes, one fake that answers more than its document, and a draft that names a foreign schema, a monolith base, a foreign topic or a Schedule |
| TC-S1-E4007-CON-04 | C1, C2: the compatibility check and the additive slice | Contract | The previous tag of the operation, an additive draft with the recommendation elements and a breaking draft |
| TC-S1-E4007-CON-09 | C11, C12: the business rules BR1 to BR10 of the baseline | Contract | The baseline document, the ownership rows, the consumed operation table and the event list, and one draft per rule that breaks that rule |
| TC-S1-E4007-CON-05 | C7: the tables of section 12.7, with no column, index, migration or foreign table declared | Contract | The two tables this baseline names, decision_record and idempotency_key, and a draft that declares recovery_case, assignment, task, timer, approval or a v_ace_* view |
| TC-S1-E4007-CON-06 | C8: the business rules BR1 to BR10 of section 8 | Contract | Not specified in the source documents (NEWAC-RWB-S1-E4007-CON-AC3) |
| TC-S1-E4007-CON-07 | C9: the retry and the timeout of an activity and of a consumed call | Contract | Not specified in the source documents (NEWAC-RWB-S1-E4007-CON-AC4) |
| TC-S1-E4007-CON-08 | C10: the refusal of a status change the closed list does not allow | Contract | Not specified in the source documents (NEWAC-RWB-S1-E4007-CON-AC5) |

The four legacy case IDs are the legacy test cases of RWB-E4-007 in their legacy order, mapped onto this contract deliverable: the primary path and its elements (01), the failure of the decision log (02), the access path (03) and the principle-5 record failure (04). The four `TC-S1-E4007-CON-` cases are new and test the parts of the baseline no legacy case touches. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the baseline: the route codes of `LOV-ROUTE`, the returns, the weights, the confidence threshold and the open route set are referenced with their identifier, list or version, never enumerated as a constant or a default.
- No personal data in any element, fake, example, prompt or log: identifiers, codes, amounts, dates and versions only, no secret in a prompt, and every fixture is synthetic (NFR-052).
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the score, the collateral and the accepted value appear only as the rwb-source-data data product (DP-05).
- The case stays with rwb-case, the rules with rwb-decision and the model with rwb-agent: no `recovery_case`, `rule_row` or model element is declared as this service's own (BR8).
- One base, one operation, one topic, one queue and one login per service; the recommendation slice is additive and never a second path (DP-13, DP-14, BR3).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Quartz row, no Schedule, no foreign schema and no event published by this baseline.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-007, disposition Split (rework); AC1 and AC2 are owned by RWB-S1-E4007-APP and this story carries no legacy criterion and fixes the surface it touches | 1, 11, 12, 16 |
| Feature | FEAT-VAL-07 Score the routes and recommend one with reasons, module S1, epic E4, depends on FEAT-VAL-05 and FEAT-VAL-06 | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.7.2 steps and integration points (Workbench, Model gateway); A2.7.3.1 VR-S1-007-1 and BR-S1-007; A2.7.3.3 roles; A2.7.4.3 exception flows; SCR-13 | 2, 3, 8, 12, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `score`; T3.2 `LOV-ROUTE`; T5.1 to T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 16 |
| Epics 3 to 8 Specification v3 | E4 row FEAT-VAL-07: system, runs unattended, Workbench and Model gateway, prerequisites FEAT-VAL-05 and FEAT-VAL-06 | 2, 3 |
| Agent Catalog v2 | Route agent; sub-decision D6.3 Advised, L1 at go-live, L2 target; a person approves the route | 1, 2, 3, 8, 11, 12 |
| Logical data model | DF-ACE-270 to DF-ACE-279, DF-ACE-091 to DF-ACE-098, DF-ACE-187 to DF-ACE-195, DF-DEC-019 to DF-DEC-027, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | 11 |
| Routing logic | R-UNI-38 to R-UNI-41 and R-RES-32 (Business Rules and Routing Logic v4); no S1 route-decision rule is in force, because the S1 package is Phase 2 | 2, 8, 9, 14 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5); DP-20 noted and not applied (GAP-2625) | 13 |
| Gaps and assumptions | GAP-2621, -2, -3, -5, -6, -7, -8; ASM-4324, -2, -3, -5, -6, -7, -8 | 1, 3, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The scoring, the ranking, the recommendation, the decision records, the case-move answer and the screen behaviour: RWB-S1-E4007-APP.
- The appraisal and approval elements of the same operation: RWB-S1-E4001-CON, RWB-S1-E4008-CON and their siblings.
- The COLLINS call and the return it records per route: RWB-S1-E4005-CON. The payoff and the settlement range: RWB-S1-E4006-CON.
- The agent runtime, its models, its prompts, its autonomy level, its confidence floor and its own fallback engine, and its client contract of DP-20: rwb-agent (P10) and RWB-P10-TE013-CON (GAP-2625).
- The ACE score, collateral, account and valuation facts and the freshness of the data product: rwb-source-data (P1). The store of the recommendation: the data owner of this service (GAP-2626).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7). The route-decision rule package, its decision code and the confidence threshold as data: GAP-2623.
- The mapping of the route codes R1 to R8 onto the eight named routes: GAP-2628.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
