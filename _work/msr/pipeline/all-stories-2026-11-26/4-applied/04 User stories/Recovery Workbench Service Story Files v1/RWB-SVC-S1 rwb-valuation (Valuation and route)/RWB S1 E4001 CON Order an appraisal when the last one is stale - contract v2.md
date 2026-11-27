# RWB-S1-E4001-CON Order an appraisal when the last one is stale - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4001-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-001, the baseline the appraisal-order step of rwb-valuation builds against on Day 1. The baseline declares the route-decision operation `POST /cases/{caseId}/route` (API-S1-001) on `/api/recovery/valuation/v1` (DP-13), the six consumed rows of rwb-source-data, rwb-integration, rwb-case, rwb-decision and rwb-access (DP-05), the decision-record element and the library that carries it (DP-03), the elements of `RouteDecisionWorkflow` and its two activities, the rights, the error envelope and the fakes; it publishes no event, because the ownership rows give S1 none. The operation names of six consumed rows and the SVAF order interface are not published (GAP-2587; ASM-4283); the Ownership Map carries two valuation paths and no appraisal-order operation (GAP-2588; ASM-4284); the Ownership Map gives S1 no table while TSD S1 T3.1 declares one (GAP-2589; ASM-4285). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S1-E4001-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-valuation**, I want **the published contract baseline of the appraisal-order step of rwb-valuation, being its route-decision operation, its six consumed rows, its decision-record element, its workflow elements, its rights, its error envelope and its fakes, fixed and tagged before the build starts**, so that **the application story, the wave 3 harness and the six owners it consumes can build and test on Day 1 against one versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-001. It owns:

- the document that fixes `POST /cases/{caseId}/route` (API-S1-001) on base `/api/recovery/valuation/v1`: `RouteRequest` in, `Approval` out, the `Idempotency-Key` header, the rights and the error set (DP-13);
- the six consumed rows: the appraisal and acceptance data product of rwb-source-data, the SVAF order submission and the interface-run status of rwb-integration, the case state of rwb-case, the rule-in-force and decision-log read of rwb-decision, and the authorise operation of rwb-access, each with its owner, its use and a placeholder where the name is not published (DP-05);
- the decision-record element, the library that carries it and the shared topic it reaches (DP-03);
- the elements of `RouteDecisionWorkflow` and its two activities on task queue `rwb-valuation`;
- the subject of SCR-13 Route decision, one hop through the gateway-bff composite route (DP-19);
- the fakes and their documented answers;
- the naming and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no monolith base.

It does not own: the appraisal-age check, the order content, the decision records, the case-move answer and the screens' behaviour, which are RWB-S1-E4001-APP; the two valuation operations `POST /assets/{assetId}/valuations` and `POST /assets/{assetKey}/valuations`, which are the appraisal-intake baseline RWB-S1-E4002-CON; the ACE appraisal and collateral facts, which are rwb-source-data's (P1); the SVAF interface itself and its transport, which are rwb-integration's (P2); the case of record and its route states, which are rwb-case's (P3); the rule package and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets eight teams start together. Legacy RWB-E4-001 asks for a valuation order raised with no person involved and for the result recorded with its rule version, so the step reads facts from three other services and writes one record in a fourth. Without a tagged baseline each of those shapes would be discovered at the first integration instead of at the review.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner, its use and its 2 s budget, and every row whose name is not published carries the placeholder and its gap (GAP-2587; ASM-4283).
- **one hop, one budget.** Each consumed row is a single hop with a 2 s timeout and a breaker; the appraisal is never read from a table and never chained through a second service (DP-05, ADR-020).
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document (s9).

The business outcome the baseline protects is the one FEAT-VAL-01 and REQ-S1-001 of FSD S1 state: an appraisal older than the limit triggers a new valuation order without a person asking. The baseline states no outcome and no business value of its own, and no criterion here asserts that an order is raised.

### 3. Preconditions

- The Ownership Map rows for S1 are in force: `POST /assets/{assetId}/valuations`, `POST /assets/{assetKey}/valuations` and `POST /cases/{caseId}/route`; no table, no event, no job, and one workflow, `RouteDecisionWorkflow`. The map carries two valuation paths and no source says which is current (GAP-2588; ASM-4284).
- The service naming is fixed: schema `rwb_valuation`, one login of its own, base `/api/recovery/valuation/v1`, topic `rwb.valuation.events.v1` with `.retry` and `.dlt`, task queue `rwb-valuation` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.valuation`.
- TSD S1 is the shape of record for the service: T-A.1 gives API-S1-001 with right Treatment and offer U; T-A.2 gives `RouteRequest` in, `Approval` out, errors 401, 403, 404, 409, 422 and 503 and the `Idempotency-Key`; T6.1 gives the capability area and its rights.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions of this baseline and not in its H row.
- The ownership rows give S1 no table, while TSD S1 T3.1 declares `valuation` as a NEW Workbench table with DF-COL Field IDs and the FSD holds the acceptance in `recovery.valuation_ext`; the baseline declares no table of its own on that reading (GAP-2589; ASM-4285).
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S1 T-A.1, T-A.2 and T6.1, the FSD S1 A2.1 rules and the DP table.
2. Every provided operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins.
5. The workflow and its two activities are declared with their input, their signals and their outcome elements.
6. The schema, the open lists and the closed lists are published; a closed list is referenced with its identifier and its version and is never enumerated in code.
7. The fakes are declared with their documented answers, one per consumed row and one for the composite route.
8. The compatibility check runs on the draft against the previous tag: a breaking change fails it.
9. The document goes to review as Draft; the reviewers are the owners of the six consumed rows and the tech lead of the service.
10. On the review's close the document is tagged; the application story and the wave 3 harness start against the tag and the fakes, and the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and its gap; no path and no element is invented | C3, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails and the document needs a new major version | C1 |
| X3 | A declared operation reaches another service's data, base or table | The review refuses the baseline and the boundary test fails the build | C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C6 |
| X5 | The rights of an operation are not a row of the access matrix | The operation is not declared and the error set stays incomplete | C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a version, this document follows in a minor or major version, and the fake is updated | X2, s9 |
| X7 | Two documents claim the same base, topic, queue or path | The owner named in the Ownership Map keeps it and the other document changes | C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 the paths of a baseline moving under a build, and X7 the naming boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order and the fake data are this story's choice; the path, the request, the answer, the rights and the error set are fixed by TSD S1 |
| Valuable | Eight teams build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, one provided operation, six consumed rows, one decision-record element, one workflow with two activities, one subject of SCR-13 and eight fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the appraisal-order step

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The route-decision operation and its elements are published as declared (new, D-RCV-60)
    Given the operation table of the baseline
    When POST /cases/{caseId}/route on /api/recovery/valuation/v1 is read
    Then it names RouteRequest in, Approval out, the Idempotency-Key header and the scope rule of T-A.2
    And every element carries its type, its nullability and its source

  Scenario: C3 The six consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-source-data, rwb-integration, rwb-case, rwb-decision and rwb-access are read
    Then each row names its owner, its use, one hop and a 2 s budget
    And where the operation name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C4 The consumed rows are declared as reads and no foreign table is declared (new, D-RCV-60)
    Given the consumed table and the table-ownership table of the baseline
    When the appraisal, the acceptance and the interface-run rows are read
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
    And every consumed row has a fake with a documented answer, including the stopped decision-record stub

  Scenario: C7 The naming, the publication and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue, the schema and the outbox of the baseline
    When the document is checked against the naming rule, the ownership rows and the event list
    Then one base, one topic, one queue and one login are declared and no monolith base and no foreign topic appear
    And no event is published, because the ownership rows give S1 none, and no Schedule is declared
```

The seven criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the lists, the consumed rows, the rights, the envelope, the decision-record element, the workflow, the fakes and the boundary. No criterion states a business outcome of the application story, and none asserts that an appraisal is stale, that an order leaves or that a rule fires.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, row, element and table: the baseline declares the route operation that the Ownership Map gives S1 and names every other row with its owner | Ownership Map rows of S1; TSD S1 T-A.1 |
| BR2 | A consumed row with no published operation name carries the placeholder and its gap and never an invented path, an invented parameter or an invented transport | Template and Rules v1 §R9; GAP-2587 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; s9 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain; ACE facts arrive on the rwb-source-data data product and never on a view of this service | DP-05; ADR-020 |
| BR5 | No event is published by this baseline: the ownership rows give S1 no event, and the decision record reaches the ledger on the shared topic through the library of DP-03 | DP-03; context pack S1 ownership rows |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR7 | No business value is declared in the baseline: the appraisal types, the route codes and the age limit are referenced with their identifier, their list or their version | TSD S1 T3.2; FSD S1 A2.1.3.1 BR-S1-001 |
| BR8 | No personal data in any element, fake, example or log of the baseline | Template and Rules v1 §R7.2 (s17) |
| BR9 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

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
| Baselined | An owner changes its answer | X6 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name | X1 | The row carries the placeholder and the gap, and the draft continues |
| In review | A row reaches a foreign schema, base or topic | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-valuation | Authors the baseline, resolves the shape of the service's own operation, the workflow elements and the decision-record element, and signs the tag |
| Owner of rwb-source-data (P1) | Reviews the appraisal, the acceptance and the freshness rows, and publishes the operation names when they exist |
| Owner of rwb-integration (P2) | Reviews the SVAF order submission and the interface-run row, and publishes the interface identity and the operation names when they exist |
| Owner of rwb-case (P3) | Reviews the case-state row and the case-move answer of the route operation |
| Owner of rwb-decision (P7) | Reviews the rule-in-force row and the decision-record element with the platform library |
| Owner of rwb-access (P4) | Reviews the authorise row and the capability area and rights of each declared operation |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of every declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The appraisal elements of `v_ace_valuation` (DF-ACE-187 to DF-ACE-195) | P1 (`rwb_source_data`) | The appraisal number, type, appraised value, forced sale value and appraisal date, plus the asset key; referenced as the data product and not redefined | Consumed |
| The acceptance elements of `valuation_ext` (DF-EXT-036 to DF-EXT-049) | P1 data product, acceptance owned by the accept story of S1 | `accepted`, `accepted_at`, `accepted_by`, `stale_flag`, `age_days`; referenced with their types and nullability | Consumed |
| The collateral elements of `v_ace_collateral` (DF-ACE-091 to DF-ACE-098) | P1 (`rwb_source_data`) | The collateral number, the asset key and the valuation link; referenced only | Consumed |
| The order elements of the SVAF order | P2 (`rwb_integration`) | The case, the asset key, the appraisal number being replaced and the order reference; the layout and the transport are Not specified in the source documents (GAP-2587; ASM-4283) | Consumed |
| The interface-run elements | P2 (`rwb_integration`) | The interface run reference, its status and its failure reason; referenced only | Consumed |
| The case elements of the route operation | P3 (`rwb_case`) | The case reference and its state; referenced, not redefined | Consumed |
| The rule elements of `rule_row` (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | The rule id, the rule version and the route set in force; referenced, not redefined | Consumed |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_valuation` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time | Written through the library |

The baseline declares no table of its own, because the Ownership Map gives S1 none while TSD S1 T3.1 declares `valuation` as a NEW Workbench table and the FSD holds the acceptance in `recovery.valuation_ext` (GAP-2589; ASM-4285). It declares no column, no index and no migration, and it enumerates no business value: every list, code and limit is referenced with its identifier and its version. **No personal data** appears in any element, fake or example, and every fixture identifier is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This is the operation the legacy story names in its Endpoints table, and the only one this baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, carrying the assessment command and an override reason where the answer departs from the recommendation (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat |
| None | The appraisal order itself | No source names a published operation for the order: it leaves as an outbound interface run of rwb-integration, so the row carries the placeholder Not specified in the source documents (GAP-2587; ASM-4283) and no path is declared | Not applicable | Not applicable |

The two valuation operations of the map, `POST /assets/{assetId}/valuations` and `POST /assets/{assetKey}/valuations`, are S1's and are not declared here: they are the appraisal-intake slice of RWB-S1-E4002-CON. The map carries both and no source says which is current, so the baseline reads the business-key path as current and the id path as superseded and records it (GAP-2588; ASM-4284).

The error envelope of the declared operation: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The appraisal and acceptance data-product read (operation name Not specified in the source documents (GAP-2587; ASM-4283)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The appraisal of the asset, its date, its value and its type, the acceptance of `valuation_ext`, the collateral link and the freshness stamp; faked |
| The SVAF order submission (operation name Not specified in the source documents (GAP-2587; ASM-4283)) | `/api/recovery/integration/v1` | P2 rwb-integration | The order raised to SVAF, logged, retried and placed in an exception queue after the retry limit; faked |
| The interface-run read (operation name Not specified in the source documents (GAP-2587; ASM-4283)) | `/api/recovery/integration/v1` | P2 rwb-integration | The status of the order as an interface run, keyed by case and appraisal; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state the step checks before it raises an order; faked |
| The rule-in-force and decision-log read (operation name Not specified in the source documents (GAP-2587; ASM-4283)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force for the step, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag instead of inventing a surface (BR2). The plan gives this slice no C dependency, so every row is built against its fake.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event: the topic `rwb.valuation.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this baseline declares no event, no event name and no outbox row on it (ASM-4286). The only publication of this step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service.

#### 12.4 Events consumed

None declared. FSD S1 A2.1.2 names three possible triggers of the step, "a completed ACE batch, an event or a timer", and no source publishes an event name for any of them; the ownership rows give S1 no job and no event, so the baseline declares no subscription and the trigger is carried by the application story as GAP-2593 with ASM-4290. The freshness of the ACE data product is read as an element of the rwb-source-data row and not as a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the asset key, the route set and the rule package in force; signals: the freshness answer of the data product and the interface-run status of the order |
| `checkAppraisalAge` | Activity | `rwb-valuation` | The appraisal date and the limit in force in; the age, the stale flag and the limit version out |
| `orderAppraisal` | Activity | `rwb-valuation` | The case, the asset and the appraisal being replaced in; the interface-run reference, the decision record and the step outcome out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1. This baseline fixes its input, its two signals and the two activities the step adds; the remaining activities of the route decision are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S1 no job, and this baseline declares no Temporal Schedule and no legacy Quartz job. A batch-completion trigger would be a Schedule of this service and no source names one (GAP-2587; ASM-4283).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table, while TSD S1 T3.1 declares `valuation` as a NEW Workbench table and the FSD holds the acceptance in `recovery.valuation_ext` (GAP-2589; ASM-4285) |
| decision_record | PLT library, created in `rwb_valuation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `proceeds` (P8), `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), every `v_ace_*` view (P1) and `valuation_ext` as an ACE-schema object are named by their owner and never declared here. If the S1 table owner confirms `valuation`, the DB story of this service creates it in its own Flyway sequence and this baseline declares its elements in a minor version.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The appraisal of asset `AST-2026-000401` from `2025-10-02` with its value and its type, the acceptance fields of `valuation_ext`, the collateral link and a fresh stamp; the same asset with a stale product and its date; no answer beyond 2 s | C3, C4, C6 |
| rwb-integration order-submission fake | The order accepted and its interface-run reference; a rejected order with its reason; no answer beyond 2 s | C3, C6 |
| rwb-integration interface-run fake | The run of the order in status delivered, and in status failed after the retry limit | C3, C6 |
| rwb-case case-state fake | Case `RC-2026-000401` at the route decision; a case in another state | C3, C6 |
| rwb-decision rule and log fake | The rule id and the version in force for the step; the record the ledger holds, once and twice | C3, C6 |
| rwb-access authorise fake | The capability area Treatment and offer, right U accepted and refused | C5 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000401`, with the appraisal, the order and the route elements read once | C2, C6 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2587; ASM-4283).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data data-product row, the two rwb-integration rows, the rwb-case state row, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no declared subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `checkAppraisalAge` and `orderAppraisal` on `rwb-valuation`; no Schedule |
| File | None declared | Where the configured SVAF interface of rwb-integration is a file, the order travels as an interface run and not as a file of this service (GAP-2587; ASM-4283) |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S1 rwb-valuation (Valuation and route)/RWB S1 E4001 CON Order an appraisal when the last one is stale - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S1-E4001.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operation, the six consumed rows, the publication, the workflow and its activities, the tables, the fakes, the call-type summary, the data elements and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Fakes.** One per consumed row plus the composite route, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C6).

**Done when.** The seven criteria pass, the six reviewer roles have closed their comments, the compatibility check passes on the tag, the eight fakes are published with their documented answers, and RWB-S1-E4001-APP and RWB-ITG-E4001-ITG can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Treatment and offer right calls the declared operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `RouteRequest` is absent or invalid | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the appraisal row is stale | {product} is from {date}. Today's ACE batch has not arrived. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published operation name | Not specified in the source documents (GAP-2587; ASM-4283). |

The four message IDs are those of FSD S1 A2.1.3.1 and of the platform set, copied unchanged. The two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-13 Route decision through the gateway-bff composite route (DP-19). What this story fixes is the element list of the route answer and the states the screen can show from this service's answer.

| Screen | States | What the route reads on this service |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | The appraisal and its age, the order it raised and the interface run, the decision record with its rule version, and the override reason of the submission |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The route itself, its merge order and its field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-001-01 | C1, C2: the schema, the elements and the closed lists of the route answer | Contract | The published schema and the recorded answers of case `RC-2026-000401` |
| TC-E4-001-02 | C4, C6: the decision-record element and the stopped chain | Contract | The decision-record element, a healthy stub and a stopped stub |
| TC-E4-001-03 | C5: the rights and the error envelope of the declared operation | Contract | One request per right, including a role without it; one request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-001-04 | C3, C7: the six consumed rows, the boundary and the empty publication | Contract | The six consumed rows with and without a published name; the base, the topic, the queue and the schema; an outbox declaration that must stay empty |
| TC-S1-E4001-CON-01 | C3: the placeholder and the gap of an unpublished operation name | Contract | The six consumed rows, each with and without a published name |
| TC-S1-E4001-CON-02 | C6: the fakes, the workflow elements and the decision-record element | Contract | The eight fakes and one fake that answers more than its document |
| TC-S1-E4001-CON-03 | C7: the naming and boundary rule | Contract | A draft that names a foreign schema, a monolith base, a foreign topic or a Schedule |
| TC-S1-E4001-CON-04 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |

The four legacy case IDs are the legacy test cases of RWB-E4-001 in their legacy order, mapped onto this contract deliverable: the primary path and its elements (01), the failure of the decision log (02), the access path (03) and the principle-5 record failure (04). The four `TC-S1-E4001-CON-` cases are new and test the parts of the baseline no legacy case touches. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the baseline: the appraisal types of `LOV-APPRAISAL`, the route codes of `LOV-ROUTE` and the age limit are referenced with their identifier, list or version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the appraisal and the acceptance appear only as the rwb-source-data data product (DP-05).
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case` element and no `rule_row` element is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Quartz row, no Schedule, no foreign schema and no event published by this baseline.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-001, disposition Split (rework); AC1 is owned by RWB-ITG-E4001-ITG and AC2 by RWB-S1-E4001-APP; this story carries no legacy criterion and fixes the surface both touch | 1, 11, 12, 16 |
| Feature | FEAT-VAL-01 Order an appraisal when the last one is stale, module S1, epic E4, depends on FEAT-RDF-06 | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.1.2 steps and integration points; A2.1.3.1 VR-S1-001-1 and BR-S1-001; A2.1.3.3 roles; requirements REQ-S1-001 to REQ-S1-008; SCR-13 | 2, 3, 8, 12, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.2 `LOV-APPRAISAL` and `LOV-ROUTE`; T5.1 to T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 16 |
| Logical data model | DF-ACE-091 to DF-ACE-098, DF-ACE-187 to DF-ACE-195, DF-EXT-036 to DF-EXT-049, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-COL-018 to DF-COL-027 and DF-COL-043 to DF-COL-044 | 11 |
| Routing logic | R-UNI-38, R-UNI-39 and R-UNI-40 (Business Rules and Routing Logic v4); no S1 route rule is in force, because the S1 package is Phase 2 | 8, 14 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2587 to -3; ASM-4283 to -4 | 1, 3, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The appraisal-age check, the order content, the decision records, the case-move answer and the screen behaviour: RWB-S1-E4001-APP.
- The two valuation operations and the appraisal intake: RWB-S1-E4002-CON and the appraisal stories of this service.
- The SVAF interface itself, its identity, its transport, its order layout and its failure codes: rwb-integration (P2) (GAP-2587).
- The ACE appraisal, collateral and acceptance facts and the freshness of the data product: rwb-source-data (P1); the store of `valuation_ext` and of any `valuation` table: the data owner of this service (GAP-2589).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, RWB-ITG-E4001-ITG.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
