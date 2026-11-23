# RWB-S1-E4008-CON Approve a route inside the limit - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4008-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-008, the baseline the route-approval step of rwb-valuation builds against on Day 1. The baseline declares the route-decision operation `POST /cases/{caseId}/route` (API-S1-001) on `/api/recovery/valuation/v1` (DP-13), the approval element set of `RouteRequest` and `Approval`, the four consumed rows of rwb-case, rwb-decision and rwb-access (DP-05 is not part of this pattern set), the delegation-of-authority limit as a governed element read with its version, the decision-record element and the library that carries it (DP-03), the elements of `RouteDecisionWorkflow` and its two approval activities, the rights, the error envelope and the fakes; it publishes no event, because the ownership rows give S1 none. The limit, its boundaries and the authority-matrix row are not published (GAP-2629; ASM-4332); the operation names of the four consumed rows are not published (GAP-2630; ASM-4333); the element lists of `RouteRequest`, `Approval` and the recommendation are not published (GAP-2631; ASM-4334); no S1 rule package is in force and no rule id or parameter is named for the step (GAP-2632; ASM-4335). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-valuation**, I want **the published contract baseline of the route-approval step of rwb-valuation, being its route-decision operation, its approval element set, its four consumed rows, its limit and decision-record elements, its workflow elements, its rights, its error envelope and its fakes, fixed and tagged before the build starts**, so that **the application story, the wave 3 harness and the four owners it consumes can build and test on Day 1 against one versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-008. It owns:

- the document that fixes `POST /cases/{caseId}/route` (API-S1-001) on base `/api/recovery/valuation/v1`: `RouteRequest` in, `Approval` out, the `Idempotency-Key` header, the rights and the error set (DP-13);
- the approval element set: the chosen route, the expected return, the reasons, the confidence, the alternatives, the override reason, the limit applied and its version, the rule id and the rule version (GAP-2631);
- the four consumed rows: the case state and the case-move answer of rwb-case, the rule-in-force, limit and decision-log read of rwb-decision, and the authorise operation of rwb-access, each with its owner, its use and a placeholder where the name is not published (GAP-2630);
- the delegation-of-authority limit element, with its version and the matrix row it comes from, declared as governed data and never as a constant (GAP-2629);
- the decision-record element, the library that carries it and the shared topic it reaches (DP-03);
- the elements of `RouteDecisionWorkflow` and its two approval activities on task queue `rwb-valuation`;
- the subject of SCR-13 Route decision, one hop through the gateway-bff composite route (DP-19);
- the fakes and their documented answers;
- the naming and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no monolith base.

It does not own: the approval behaviour, its checks, the decision records, the case-move answer and the screens' behaviour, which are RWB-S1-E4008-APP; the recommendation of FEAT-VAL-05 to FEAT-VAL-07, which is the sibling scoring baseline and stories; the above-limit committee approval of FEAT-VAL-09; the case of record and its route states, which are rwb-case's (P3); the rule package, the authority matrix, the limit versions and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets the teams start together. Legacy RWB-E4-008 asks the case owner to approve the recommended route inside their delegated limit and to have the result recorded with its rule version, so the step reads facts from three other services, compares a governed limit and writes one record in a fourth. Without a tagged baseline each of those shapes would be discovered at the first integration instead of at the review.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner, its use and its 2 s budget, and every row whose name is not published carries the placeholder and its gap (GAP-2630; ASM-4333).
- **the limit is data, not a number.** The limit element is declared with its source, its version and its matrix row; the document carries no value, no boundary and no default, because BR-S1-008 forbids a business value in code (GAP-2629; ASM-4332).
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document (s9).

The business outcome the baseline protects is the one FEAT-VAL-08 and REQ-S1-006 of FSD S1 state: the route decision is approved inside the delegation of authority, and above the limit it reaches the committee. The baseline states no outcome and no business value of its own, and no criterion here asserts that a route is approved.

### 3. Preconditions

- The Ownership Map rows for S1 are in force: `POST /assets/{assetId}/valuations`, `POST /assets/{assetKey}/valuations` and `POST /cases/{caseId}/route`; no table, no event, no job, and one workflow, `RouteDecisionWorkflow`. Only the route operation belongs to this baseline.
- The service naming is fixed: schema `rwb_valuation`, one login of its own, base `/api/recovery/valuation/v1`, topic `rwb.valuation.events.v1` with `.retry` and `.dlt`, task queue `rwb-valuation` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.valuation`.
- TSD S1 is the shape of record for the service: T-A.1 gives API-S1-001 with right Treatment and offer U; T-A.2 gives `RouteRequest` in, `Approval` out, errors 401, 403, 404, 409, 422 and 503 and the `Idempotency-Key`; T6.1 gives the capability area and its rights.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions of this baseline and not in its H row.
- The delegation-of-authority limit, its boundaries, the matrix row that carries it and its owner are Not specified in the source documents (GAP-2629; ASM-4332); the baseline declares the element, its source and its version, and no value.
- The operation names of the four consumed rows are Not specified in the source documents (GAP-2630; ASM-4333); each row is declared by its owner, its use and a placeholder.
- The element lists of `RouteRequest`, `Approval` and the FEAT-VAL-07 recommendation are Not specified in the source documents beyond the two type names (GAP-2631; ASM-4334); the baseline declares the elements the requirements name and marks the rest open.
- No S1 rule package is in force and no rule id or parameter is named for the approval step (GAP-2632; ASM-4335); the rule element is declared with its version and no value.
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag (ASM-4336).

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S1 T-A.1, T-A.2 and T6.1, the FSD S1 A2.8 rules and the DP table.
2. Every provided operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. The approval element set is declared with its type, its nullability and its source; the recommendation elements it echoes are named as elements of this answer and not redefined.
4. The limit element is declared with its source, its version and its matrix row; no value, boundary or default is written.
5. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
6. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins.
7. The workflow and its two approval activities are declared with their input, their signals and their outcome elements.
8. The schema, the open lists and the closed lists are published; a closed list is referenced with its identifier and its version and is never enumerated in code.
9. The fakes are declared with their documented answers, one per consumed row and one for the composite route.
10. The compatibility check runs on the draft against the previous tag; a breaking change fails it.
11. The document goes to review as Draft; the reviewers are the owners of the four consumed rows and the tech lead of the service.
12. On the review's close the document is tagged; the application story and the wave 3 harness start against the tag and the fakes, and the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and its gap; no path and no element is invented | C3, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails and the document needs a new major version | C1 |
| X3 | A declared operation reaches another service's data, base or table | The review refuses the baseline and the boundary test fails the build | C6 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C5 |
| X5 | The rights of an operation are not a row of the access matrix | The operation is not declared and the error set stays incomplete | C5 |
| X6 | A limit value, a boundary or a default appears in the baseline | The review refuses the document: the limit is an element of governed data with its version, not a number | C7 |
| X7 | An owner changes its documented answer after the tag | The owner publishes a version, this document follows in a minor or major version, and the fake is updated | X2, s9 |
| X8 | Two documents claim the same base, topic, queue or path | The owner named in the Ownership Map keeps it and the other document changes | C6 |

X1 to X3 are the paths of an incomplete source, X4 to X7 the paths of a baseline moving under a build, and X8 the naming boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order and the fake data are this story's choice; the path, the request, the answer, the rights, the limit element and the error set are fixed by TSD S1 and FSD S1 |
| Valuable | Four teams build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, one provided operation, four consumed rows, one limit element, one decision-record element, one workflow with two activities, one subject of SCR-13 and six fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the route-approval step

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The route-decision operation and the approval elements are published as declared (new, D-RCV-60)
    Given the operation table of the baseline
    When POST /cases/{caseId}/route on /api/recovery/valuation/v1 is read
    Then it names RouteRequest in, Approval out, the Idempotency-Key header and the scope rule of T-A.2
    And the approval elements name the route, the expected return, the reasons, the confidence, the alternatives, the override reason, the limit applied and the rule version

  Scenario: C3 The four consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-case, rwb-decision and rwb-access are read
    Then each row names its owner, its use, one hop and a 2 s budget
    And where the operation name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C4 The consumed rows are declared as reads and no foreign table is declared (new, D-RCV-60)
    Given the consumed table and the table-ownership table of the baseline
    When the case, the rule, the limit and the authorise rows are read
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
    And RouteDecisionWorkflow and its two approval activities name their input, their signals and their task queue
    And every consumed row has a fake with a documented answer, including the stopped decision-record stub

  Scenario: C7 The delegation limit is declared as governed data and the naming boundary holds (new, D-RCV-60)
    Given the limit element, the base, the topic, the queue, the schema and the outbox of the baseline
    When the document is checked against the limit rule, the naming rule and the event list
    Then the limit carries its source, its matrix row and its version, and no value, boundary or default appears
    And one base, one topic, one queue and one login are declared, with no monolith base, no foreign topic and no published event
```

The seven criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the limit, the consumed rows, the rights, the envelope, the decision-record element, the workflow, the fakes and the boundary. No criterion states a business outcome of the application story, and none asserts that a route is recommended, that a limit is met or that a rule fires.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, row, element and table: the baseline declares the route operation that the Ownership Map gives S1 and names every other row with its owner | Ownership Map rows of S1; TSD S1 T-A.1 |
| BR2 | A consumed row with no published operation name carries the placeholder and its gap and never an invented path, an invented parameter or an invented transport | Template and Rules v1 §R9; GAP-2630 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; s9 |
| BR4 | The delegation-of-authority limit is declared as an element of governed data with its source, its matrix row and its version; its value, boundaries and defaults are never written in the baseline | FSD S1 A2.8.3.1 BR-S1-008; GAP-2629 |
| BR5 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain; the case, the rule and the limit arrive on their owners' contracts and not on a table of this service | ADR-020; DP-01 |
| BR6 | No event is published by this baseline: the ownership rows give S1 no event, and the decision record reaches the ledger on the shared topic through the library of DP-03 | DP-03; context pack S1 ownership rows |
| BR7 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03; R-UNI-39 |
| BR8 | No business value is declared in the baseline: the route codes, the limit and the rule are referenced with their identifier, their list or their version | TSD S1 T3.2; FSD S1 A2.8.3.1 BR-S1-008 |
| BR9 | No personal data in any element, fake, example or log of the baseline | Template and Rules v1 §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

### 9. State transitions

The object of this section is the document, not a case: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, row, element, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the four consumed rows are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story and the harness |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | A new optional element only, and the check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer | X7 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name | X1 | The row carries the placeholder and the gap, and the draft continues |
| Being authored | A limit value or a boundary appears | X6 | The baseline is refused and the element is restated as governed data |
| In review | A row reaches a foreign schema, base or topic | X3, X8 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-valuation | Authors the baseline, resolves the shape of the service's own operation, the approval elements, the workflow elements and the decision-record element, and signs the tag |
| Owner of rwb-case (P3) | Reviews the case-state and case-move rows and the route states of the answer |
| Owner of rwb-decision (P7) | Reviews the rule-in-force, the authority-matrix limit and the decision-log rows, and the decision-record element with the platform library |
| Owner of rwb-access (P4) | Reviews the authorise row and the capability area and rights of the declared operation |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of every declared operation |
| Reviewer of the authority matrix | Confirms the source, the row and the version of the limit element, and that no value is declared |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The case reference and its state (DF-CAS-001 to DF-CAS-023) | P3 (`rwb_case`) | The case reference, its state and the asset link; referenced, not redefined | Consumed |
| The route codes of `LOV-ROUTE` (R1 to R8) | P7 (`rwb_decision`) | The chosen route and the recommended route as codes of the closed list, with the list's version | Consumed from the list |
| The rule id and the rule version (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | The rule id and the version in force; referenced, not redefined | Consumed |
| The delegation-of-authority limit and its matrix row (no Field ID published) | P7 (`rwb_decision`), by the default ruling on parameters and reference data; the row and the owner are Not specified in the source documents (GAP-2629; ASM-4332) | The limit applied to the caller, its matrix row and its version; no value, boundary or default | Consumed |
| The route recommendation of FEAT-VAL-07 (no Field ID published) | FEAT-VAL-05 to FEAT-VAL-07, in the workflow state of this service | The route, the expected return, the reasons, the confidence and the alternatives; their element set is Not specified in the source documents (GAP-2631; ASM-4334) | Read from the workflow state and echoed in the answer |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_valuation` | The rule id, the rule version, the limit applied with its version, the inputs reference, the outcome and the decided-at time | Written through the library |

The baseline declares no value of its own and no column, index or migration. It declares no table of another owner: `recovery_case` and `assignment` (P3), `decision_log_entry`, `rule_row` and the authority matrix (P7) and every `v_ace_*` view (P1) are named by their owner and never declared here. Every element carries a type, a nullability and a source; where the source is not published, the element carries the placeholder (GAP-2631; ASM-4334). **No personal data** appears in any element, fake or example, and every fixture identifier is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This is the operation the legacy story names in its Endpoints table, and the only one this baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, carrying the chosen route, the override reason where the answer departs from the recommendation, the reasons and the limit applied with its version (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat |

The purpose of the operation is the TSD's: submit the route decision for approval, with an override reason where it departs from the recommendation. The error envelope: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element or a missing override reason, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

The two valuation operations of the map, `POST /assets/{assetId}/valuations` and `POST /assets/{assetKey}/valuations`, are S1's and are not declared here: they are the appraisal-intake slice of RWB-S1-E4002-CON. The recommendation of FEAT-VAL-05 to FEAT-VAL-07 adds no operation: it is an element of the workflow state and of the answer (BR3).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state at the route decision, the recommended route and the asset link; read only; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2630; ASM-4333)) | `/api/recovery/case/v1` | P3 rwb-case | The move from `ROUTE_D6` on `ROUTE_APPROVED` or `ROUTE_OVERRIDDEN`, applied by the case of record; faked |
| The rule-in-force, limit and decision-log read (operation name Not specified in the source documents (GAP-2630; ASM-4333)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and version in force, the authority-matrix row and the limit with its version, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag instead of inventing a surface (BR2). The plan gives this slice no C dependency, so every row is built against its fake.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event: the topic `rwb.valuation.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this baseline declares no event, no event name and no outbox row on it. The only publication of this step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service (BR6).

#### 12.4 Events consumed

None declared. The approval is started by the case owner's command on the route operation and by nothing else; FSD S1 A2.8.4.4 declares no background event for the feature, the ownership rows give S1 no job and no event, and no source publishes a name for a route-recommended notice. The recommendation arrives in the workflow state of FEAT-VAL-07 and not as a subscription. A duplicate of the command is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the asset key, the route set and the rule package in force; signals: the recommendation ready and the case-move answer |
| `approveRouteInsideLimit` | Activity | `rwb-valuation` | The case, the recommended route, the expected return, the rule and the limit in force, the caller and the override reason in; the route, the limit applied with its version and the step outcome out |
| `recordRouteApproval` | Activity | `rwb-valuation` | The decision record, the idempotency row and the case-move answer out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1. This baseline fixes its input, its two signals and the two approval activities; the scoring and intake activities of the route decision are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S1 no job, and this baseline declares no Temporal Schedule and no legacy Quartz job. The approval starts from the case owner's command and no timer or re-review is part of this key.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the limit applied and the override reason are elements of the decision record and of the answer |
| decision_record | PLT library, created in `rwb_valuation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and the authority matrix (P7) and every `v_ace_*` view (P1) are named by their owner and never declared here.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | Case `RC-2026-000408` at `ROUTE_D6` with its asset link and recommended route; a case in another state | C3, C4 |
| rwb-case move-answer fake | The move from `ROUTE_D6` on `ROUTE_APPROVED` accepted with its reference, and on `ROUTE_OVERRIDDEN` with its reason; refused with its reason | C3, C5 |
| rwb-decision rule and limit fake | The rule id and the version in force, the authority-matrix row and the limit with its version for `RW-CASEOWN`, a limit below the route, and the record the ledger holds | C3, C5, C7 |
| rwb-access authorise fake | The capability area Treatment and offer, right U accepted and refused | C5 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000408`, with the recommendation, the reasons and the approval elements read once | C2, C6 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2630; ASM-4333). The limit fake carries versions and no value of the business limit in the document; its documented answer is a governed row and not a constant (GAP-2629; ASM-4332).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-case case-state and move rows, the rwb-decision rule and limit row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no declared subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `approveRouteInsideLimit` and `recordRouteApproval` on `rwb-valuation`; no Schedule |
| File | None declared | The route recommendation is computed in the workflow and no file is read or written by this service |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S1 rwb-valuation (Valuation and route)/RWB S1 E4008 CON Approve a route inside the limit - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S1-E4008.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operation, the approval elements, the limit element, the four consumed rows, the workflow and its activities, the tables, the fakes, the call-type summary and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Fakes.** One per consumed row plus the composite route, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C6).

**Done when.** The seven criteria pass, the reviewer roles have closed their comments, the compatibility check passes on the tag, the six fakes are published with their documented answers, and RWB-S1-E4008-APP and the wave 3 harness can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Treatment and offer right calls the declared operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `RouteRequest` is absent or invalid, or the override reason is missing | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published operation name | Not specified in the source documents (GAP-2630; ASM-4333). |
| Document rule | A limit value, boundary or default appears | Not specified in the source documents (GAP-2629; ASM-4332). |

The three message IDs are those of FSD S1 A2.8.3.1 and of the platform set, copied unchanged. The three document rules are checks of this story and are not service messages. No source publishes a message text for the above-limit refusal, so none is added.

### 15. Screens and states

The baseline serves SCR-13 Route decision through the gateway-bff composite route (DP-19). What this story fixes is the element list of the approval answer and the states the screen can show from this service's answer.

| Screen | States | What the route reads on this service |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | The recommendation with its expected return, reasons, confidence and alternatives; the approved or overridden route; the limit applied with its version; the override reason; the decision record with its rule version |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The route itself, its merge order and its field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-008-01 | C1, C2: the schema, the approval elements and the closed lists of the route answer | Contract | The published schema and the recorded answers of case `RC-2026-000408` |
| TC-E4-008-02 | C5, C6: the decision-record element and the stopped chain | Contract | The decision-record element, a healthy stub and a stopped stub |
| TC-E4-008-03 | C5: the rights and the error envelope of the declared operation | Contract | One request per right, including a role without it; one request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-008-04 | C3, C4: the four consumed rows, the boundary and the empty publication | Contract | The four consumed rows with and without a published name; the base, the topic, the queue and the schema; an outbox declaration that must stay empty |
| TC-S1-E4008-CON-01 | C3: the placeholder and the gap of an unpublished operation name | Contract | The four consumed rows, each with and without a published name |
| TC-S1-E4008-CON-02 | C6: the fakes, the workflow elements and the decision-record element | Contract | The six fakes and one fake that answers more than its document |
| TC-S1-E4008-CON-03 | C6: the naming and boundary rule | Contract | A draft that names a foreign schema, a monolith base, a foreign topic or a Schedule |
| TC-S1-E4008-CON-04 | C7: the limit element and the compatibility check | Contract | The limit element with its source, row and version; a draft carrying a limit value; the previous tag, an additive draft and a breaking draft |

The four legacy case IDs are the legacy test cases of RWB-E4-008 in their legacy order, mapped onto this contract deliverable: the primary approval path and its elements (01), the failure of the decision log (02), the access path (03) and the principle-5 record failure (04). The four `TC-S1-E4008-CON-` cases are new and test the parts of the baseline no legacy case touches. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the baseline: the route codes of `LOV-ROUTE`, the delegation limit and the rule id are referenced with their identifier, list or version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table.
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case` element and no `rule_row` element is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Quartz row, no Schedule, no foreign schema and no event published by this baseline.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).
- The limit is declared as data: a baseline that carries a limit value, a boundary or a default fails the review (BR4, C7).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-008, disposition Split (rework); this story carries no legacy criterion and fixes the surface RWB-S1-E4008-APP and the wave 3 harness touch | 1, 11, 12, 16 |
| Feature | FEAT-VAL-08 Approve a route inside the limit, module S1, epic E4, depends on FEAT-APD-02 and FEAT-VAL-07 | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.8.2 steps and integration points; A2.8.3.1 VR-S1-008-1 and BR-S1-008; A2.8.3.2 field catalog; A2.8.3.3 roles; requirements REQ-S1-006; SCR-13 | 2, 3, 8, 12, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.2 `LOV-ROUTE`; T5.1 to T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 16 |
| Logical data model | DF-CAS-001 to DF-CAS-023, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | 11 |
| Routing logic | R-UNI-14 and R-UNI-15 (inside and outside the delegation); R-UNI-39 and R-UNI-40; no S1 route rule is in force, because the S1 package is Phase 2 | 8, 14 |
| Patterns | DP-03, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2629 to -4; ASM-4332 to -5 | 1, 3, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The approval behaviour, its checks, the decision records, the case-move answer and the screen behaviour: RWB-S1-E4008-APP.
- The recommendation, the expected return by route, the reasons and the alternatives of FEAT-VAL-05 to FEAT-VAL-07: the sibling scoring stories and their baseline.
- The above-limit committee approval of FEAT-VAL-09 and the reconsideration of FEAT-VAL-11: sibling stories of this service.
- The two valuation operations and the appraisal intake: RWB-S1-E4002-CON and the appraisal stories of this service.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the authority matrix, the limit versions, their approval and the central ledger: rwb-decision (P7) (GAP-2629).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
