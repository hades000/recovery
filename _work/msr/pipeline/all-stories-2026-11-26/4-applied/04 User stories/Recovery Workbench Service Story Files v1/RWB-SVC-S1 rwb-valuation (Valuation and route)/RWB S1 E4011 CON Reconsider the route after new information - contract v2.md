# RWB-S1-E4011-CON Reconsider the route after new information - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4011-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-011 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-011, the baseline the reconsider step of rwb-valuation builds against on Day 1. The baseline declares the route operation `POST /cases/{caseId}/route` (API-S1-001) on `/api/recovery/valuation/v1` as the surface of the reopen (DP-13), the six consumed rows of rwb-source-data, rwb-deviation, rwb-decision, rwb-case and rwb-access with a placeholder where a name is not published (DP-05), the reopen element with its reason, its change reference, its segment before and after and its version, the decision-record element and the library that carries it (DP-03), the elements of `RouteDecisionWorkflow` and its two reopen activities, the rights, the error envelope and the fakes; it publishes no event, because the ownership rows give S1 none. No S1 rule or parameter decides what reopens the route (GAP-2642; ASM-4350); the deviation read, the rule-in-force read and the two product codes are not published with an operation name (GAP-2643; ASM-4351); the value trigger is declared against FEAT-VAL-07 while the value is accepted in FEAT-VAL-04 (GAP-2644; ASM-4352); the retainment of the earlier decision is not fixed (GAP-2645; ASM-4353); no published element carries the change that caused the reopen (GAP-2646; ASM-4354); no source names the change notification (GAP-2647; ASM-4355). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S1-E4011-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-valuation**, I want **the published contract baseline of the reconsider step of rwb-valuation, being its route operation as the surface of a reopen, its consumed rows, its reopen element, its decision-record element, its workflow elements, its rights, its error envelope and its fakes, fixed and tagged before the build starts**, so that **the application story, the wave 3 harness and the five owners it consumes can build and test on Day 1 against one versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-011. It owns:

- the document that fixes `POST /cases/{caseId}/route` (API-S1-001) on base `/api/recovery/valuation/v1` as the operation a reopen is submitted on: `RouteRequest` in, `Approval` out, the `Idempotency-Key` header, the rights and the error set (DP-13);
- the six consumed rows: the two rwb-source-data data products, the deviation read of rwb-deviation, the recommendation and rule-in-force reads of rwb-decision, the case-state read of rwb-case and the authorise operation of rwb-access, each with its owner, its use and a placeholder where the name is not published (DP-05);
- the element that carries a reopen: its reason code, the change reference of each kind of new information, the segment before and after, the outcome state, the rule version it was taken under and the reference of the earlier decision it supersedes;
- the decision-record element, the library that carries it and the shared topic it reaches (DP-03);
- the elements of `RouteDecisionWorkflow` and its two reopen activities on task queue `rwb-valuation`;
- the subject of SCR-13 Route decision that this step answers, one hop through the gateway-bff composite route (DP-19);
- the fakes and their documented answers;
- the naming and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no monolith base, no `v_ace_*` read, no event.

It does not own: the read of the facts, the recompute, the record write, the route answer and the screen behaviour, which are RWB-S1-E4011-APP; the accepted value, which is FEAT-VAL-04's; the expected return, which is FEAT-VAL-05's; the recommendation, which is FEAT-VAL-07's; the ACE facts, which are rwb-source-data's (P1); the payment matching, which is rwb-payment's (P8); the deviation record, which is rwb-deviation's (S8); the rule rows and the ledger, which are rwb-decision's (P7); the case of record, which is rwb-case's (P3); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets the teams start together. Legacy RWB-E4-011 asks for the route decision to reopen when a value, a payment or a deviation changes the picture and for the result to be recorded with its rule version, so the step reads two data products from one owner, a deviation from a second, a recommendation and a rule row from a third, a case state from a fourth and a right from a fifth, and writes one record through a platform library. Without a tagged baseline each of those shapes would be discovered at the first integration instead of at the review.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner, its use and its 2 s budget, and every row whose name is not published carries the placeholder and its gap (GAP-2643; ASM-4351).
- **the facts are other services', the decision is this one's.** The payment and the appraisal are ACE's ingested facts on the data products, the deviation is rwb-deviation's record, and this service declares no `v_ace_*` element and no `deviation` element of its own (DP-05).
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document.

The business outcome the baseline protects is the one FEAT-VAL-11 and AC-S1-011-01 of FSD S1 state: the route decision is live while the facts move and every reopen is proven with its reason and its version. The baseline states no outcome and no business value of its own, and no criterion here asserts that a route is reopened or that a rule fires.

### 3. Preconditions

- The Ownership Map rows for S1 are in force: `POST /assets/{assetId}/valuations`, `POST /assets/{assetKey}/valuations` and `POST /cases/{caseId}/route`; no table, no event, no job, and one workflow, `RouteDecisionWorkflow`.
- The service naming is fixed: schema `rwb_valuation`, one login of its own, base `/api/recovery/valuation/v1`, topic `rwb.valuation.events.v1` with `.retry` and `.dlt`, task queue `rwb-valuation` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.valuation`.
- TSD S1 is the shape of record for the service: T-A.1 gives API-S1-001 with right Treatment and offer U; T-A.2 gives `RouteRequest` in, `Approval` out, errors 401, 403, 404, 409, 422 and 503 and the `Idempotency-Key`; T6.1 gives the capability area and its rights; T3.1 gives `valuation` and `score`; T3.2 gives `LOV-ROUTE`.
- The API Specification v5 publishes `RouteRequest` with `route`, `overrideReasonCode` and `note`, `Approval` with `id`, `caseId`, `decision`, `preparedBy`, `level`, `amount` and `status`, the recommendation with `expectedReturnByRoute`, `reasons`, `ruleVersion` and `agentVersion`, and `GET /data-products/{productCode}/records`; it publishes no element for a reopen on `Approval` and no read of the deviations of a case (GAP-2646; ASM-4354).
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions of this baseline and not in its H row.
- The ownership rows give S1 no table, while TSD S1 T3.1 declares `valuation` as a new Workbench table of the module with no route-decision object; the baseline declares no table of its own and no place for the earlier decision on that reading (GAP-2645; ASM-4353).
- No S1 rule is in force and no source names the rule, the parameter or the threshold that decides what reopens the route; the baseline declares the rule row as a consumed element by reference and states no rule id (GAP-2642; ASM-4350).
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S1 T-A.1, T-A.2, T3.1 and T3.2, the API Specification v5 schemas, the FSD S1 A2.11 rules and the DP table.
2. Every provided operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The reopen element is declared with its reason code, its change reference, its segment before and after, its outcome state, its rule version and the reference of the earlier decision.
5. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins.
6. The workflow and its two reopen activities are declared with their input, their signals and their outcome elements.
7. The closed lists are published by reference: the reason codes of the reopen and `LOV-ROUTE` with its identifier and its version, never enumerated in code.
8. The fakes are declared with their documented answers, one per consumed row and one for the composite route.
9. The compatibility check runs on the draft against the previous tag: a breaking change fails it.
10. The document goes to review as Draft; the reviewers are the owners of the six consumed rows and the tech lead of the service. On the review's close it is tagged, and the application story and the wave 3 harness start against the tag and the fakes.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and its gap; no path and no element is invented | C3, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails and the document needs a new major version | C1 |
| X3 | A declared operation reaches another service's data, base or table | The review refuses the baseline and the boundary test fails the build | C6 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C3, C4 |
| X5 | A document declares a reopen element that no source supports | The element is declared by reference to the row that carries it, or it is not declared at all | C4, C5 |
| X6 | A document declares a `v_ace_*` element, a `deviation` element or a `rule_row` element as this service's own | The review refuses it: DP-05 and DP-01 forbid it and the boundary test fails | C6 |
| X7 | Two documents claim the same base, topic, queue or path | The owner named in the Ownership Map keeps it and the other document changes | C6 |

X1 and X5 are the paths of an incomplete or unsupported source, X2 to X4 the paths of a baseline moving under a build, and X6 and X7 the naming and boundary rules.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order and the fake data are this story's choice; the path, the request, the answer, the rights and the error set are fixed by TSD S1 and the API Specification |
| Valuable | Five owners and two build teams start at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, one provided operation, six consumed rows, one reopen element, one decision-record element, one workflow with two activities and nine fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the reconsider step

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The route operation and the reopen submission are published as declared (new, D-RCV-60)
    Given the operation table of the baseline
    When POST /cases/{caseId}/route on /api/recovery/valuation/v1 is read
    Then it names RouteRequest in, Approval out, the Idempotency-Key header and the scope rule of T-A.2
    And the reopen submission names the route, the override reason code and the note as its request elements

  Scenario: C3 The six consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-source-data, rwb-deviation, rwb-decision, rwb-case and rwb-access are read
    Then each row names its owner, its use, one hop and a 2 s budget
    And where the operation name or the product code is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C4 The reopen element, the record element, the workflow and the fakes are declared (new, D-RCV-60)
    Given the baseline document
    When the reopen element, the decision-record element, the workflow table and the fake table are read
    Then the reopen element names its reason code, its change reference, its segment before and after, its outcome state, its rule version and the earlier decision reference
    And the record element names RWB-PLT-E1027-CON as its library, the shared topic and the transaction it joins
    And every consumed row has a fake with a documented answer, including the stopped decision-record stub

  Scenario: C5 The rights and the error envelope are declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the rights and the error set of each operation are read
    Then each names the capability area Treatment and offer and the right of the access matrix
    And the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503 in one problem envelope

  Scenario: C6 The naming, the publication and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue, the schema and the outbox of the baseline
    When the document is checked against the naming rule, the ownership rows, the event list and the ACE data rule
    Then one base, one topic, one queue and one login are declared and no monolith base and no foreign topic appear
    And no event is published and no Schedule is declared, because the ownership rows give S1 none
    And no v_ace_* element, no deviation element and no rule_row element is declared as this service's own
```

The six criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the lists, the consumed rows, the rights, the envelope, the record element, the workflow, the fakes and the boundary. No criterion states a business outcome of the application story, and none asserts that a route is reopened or that a payment or a deviation exists.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, row, element and table: the baseline declares the route operation that the Ownership Map gives S1 and names every other row with its owner | Ownership Map rows of S1; TSD S1 T-A.1 |
| BR2 | A consumed row with no published operation name or product code carries the placeholder and its gap and never an invented path, parameter or transport | Template and Rules v1 §R9; GAP-2643 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain; ACE facts arrive on the rwb-source-data data products and never on a view of this service | DP-05; ADR-020 |
| BR5 | The reopen element states no threshold and no rule id: it carries the rule id and version it was taken under as values read at the tag | FSD S1 A2.11.3.1 BR-S1-011; GAP-2642 |
| BR6 | No event is published by this baseline: the ownership rows give S1 no event, and the decision record reaches the ledger on the shared topic through the library of DP-03 | DP-03; context pack S1 ownership rows |
| BR7 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before the outcome is reported, and its element is declared once for the service | DP-03; R-UNI-39 |
| BR8 | No business value is declared in the baseline: the reason codes, the route codes and the segment dimensions are referenced with their list and their version | TSD S1 T3.2; FSD S1 A2.11.3.1 |
| BR9 | No personal data in any element, fake, example or log of the baseline | Template and Rules v1 §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

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
| Baselined | An owner publishes a name or a product code that was a placeholder | X1 | Draft of a new minor version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name or product code | X1 | The row carries the placeholder and the gap, and the draft continues |
| In review | A row reaches a foreign schema, base or topic | X3, X7 | The baseline is refused |
| In review | A document declares a `v_ace_*`, `deviation` or `rule_row` element as its own | X6 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-valuation | Authors the baseline, resolves the shape of the service's own operation, the reopen element, the workflow elements and the record element, and signs the tag |
| Owner of rwb-source-data (P1) | Reviews the two data-product rows, the payment and appraisal elements and the freshness stamp, and publishes the product codes when they exist |
| Owner of rwb-deviation (S8) | Reviews the deviation row and publishes the read operation when it exists |
| Owner of rwb-decision (P7) | Reviews the recommendation row, the rule-in-force row and the record element with the platform library |
| Owner of rwb-case (P3) | Reviews the case-state row and the route state the operation answers |
| Owner of rwb-access (P4) | Reviews the authorise row and the capability area and right of the declared operation |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of the declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of section 9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The payment elements of `v_ace_payment` (DF-ACE-043 to DF-ACE-054) | P1 (`rwb_source_data`) | The payment code, the account key, the payment date, the payment amount, the capital, interest, expense and commission amounts, the channel, the description, the comments and the data-as-of date; referenced as the data product and not redefined | Consumed |
| The appraisal elements of `valuation` and `v_ace_valuation` (DF-COL-021 to DF-COL-025) | P1, accepted by FEAT-VAL-04 | The appraisal number, the type, the appraised value, the forced sale value and the appraisal date; referenced with their types and nullability | Consumed |
| The deviation elements of `deviation` (DF-CAS-036 to DF-CAS-045) | S8 (`rwb_deviation`) | The deviation code, the raised-at time, the raised-by code, the paused state, the contact stop, the cleared-at time and the outcome; referenced, not redefined | Consumed |
| The recommendation elements of `Recommendation` | P7 (`rwb_decision`) | `recommended`, `reasons`, `expectedReturnByRoute`, `ruleVersion`, `agentVersion`; referenced with their types and nullability | Consumed |
| The rule elements of `rule_row` (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | The rule id, the rule version, the segment dimensions and the gate thresholds in force; referenced, not redefined | Consumed |
| The case elements of the route operation | P3 (`rwb_case`) | The case reference and its route state; referenced, not redefined | Consumed |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_valuation` | The rule id, the rule version, the inputs reference, the outcome, the decided-at time, the reason code, the change reference and the earlier decision reference | Written through the library |

The baseline declares no table of its own, because the Ownership Map gives S1 none while TSD S1 T3.1 declares `valuation` and `score` and no route-decision object (GAP-2645; ASM-4353). The value element is the appraisal FEAT-VAL-04 accepts, which is why the baseline names it by reference (GAP-2644; ASM-4352). It declares no column, no index and no migration, and it enumerates no business value: the reason codes, the route codes and the segment dimensions are referenced with their list and their version. **No personal data** appears in any element, fake or example, and every fixture identifier is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This is the operation the legacy story names in its Endpoints table, and the only one this baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in, being `route` of `LOV-ROUTE`, `overrideReasonCode` and `note`; `Approval` out, being `id`, `caseId`, `decision`, `preparedBy`, `level`, `amount` and `status` (API-S1-001; API Specification v5) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat |
| None | The reopen itself | No source publishes an operation of this service for a reopen: the submission is the operation above, and the outcome is recorded and read on the recommendation row, so the row carries Not specified in the source documents (GAP-2646; ASM-4354) and no path is declared | Not applicable | Not applicable |

The error envelope of the declared operation: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed row does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /data-products/{productCode}/records` | `/api/recovery/source-data/v1` | P1 rwb-source-data | The payments of `v_ace_payment` since the last decision and the accepted appraisal value with its type and date; the two product codes are Not specified in the source documents (GAP-2643; ASM-4351); faked |
| The deviation read of a case (operation name Not specified in the source documents (GAP-2643; ASM-4351)) | `/api/recovery/deviation/v1` | S8 rwb-deviation | The deviations of the case, their code, paused state, outcome and cleared-at time; faked |
| `GET /cases/{caseId}/recommendation` | `/api/recovery/decision/v1` | P7 rwb-decision | The recommendation with `recommended`, `reasons`, `expectedReturnByRoute`, `ruleVersion` and `agentVersion`, as the ledger projects the earlier answer; faked |
| The rule-in-force, segment and gate read (operation name Not specified in the source documents (GAP-2643; ASM-4351)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id, the rule version, the segment dimensions and the gate thresholds in force for the business date; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state and its route state; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name or a product code is not published the row carries the placeholder and no path, so the consumer adapts at the tag instead of inventing a surface (BR2). The plan gives this slice no C dependency, so every row is built against its fake.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event: the topic `rwb.valuation.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this baseline declares no event, no event name and no outbox row on it. The only publication of this step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service.

#### 12.4 Events consumed

None declared. FSD S1 A2.11.4.4 declares "None, No background event", and the ownership rows give S1 no job and no event, so the baseline declares no subscription and the trigger is carried by the application story as GAP-2647 with ASM-4355. The freshness of the two data products is an element of the rwb-source-data rows and not a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the route set and the rule package in force; signals: the freshness answer of each data product and the outcome of the reconsider step |
| `collectRouteChange` | Activity | `rwb-valuation` | The case, the reason and the business date in; the segment before and after, the gate results, the change reference of each kind and the freshness answer out |
| `reopenRouteDecision` | Activity | `rwb-valuation` | The reopen and its versions in; the decision record, the idempotency row and the step outcome out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1. This baseline fixes its input, its two signals and the two reopen activities the step adds; the remaining activities of the route decision are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S1 no job, and this baseline declares no Temporal Schedule and no legacy Quartz job. A change-notification Schedule would be a Schedule of this service and no source names one (GAP-2647; ASM-4355).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 none, while TSD S1 T3.1 declares `valuation` and `score` and no route-decision object (GAP-2645; ASM-4353) |
| decision_record | PLT library, created in `rwb_valuation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `deviation` (S8), `decision_log_entry`, `rule_row` and `approval` (P7), `proceeds` (P8), `template` (P6), `document` and `document_custody` (P5) and every `v_ace_*` view (P1), `v_ace_payment` and `v_ace_valuation` included. If the S1 data owner confirms a table for the earlier decision, the DB story of this service creates it in its own Flyway sequence and this baseline declares its elements in a minor version.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data payment fake | Account `ACC-2026-001111` with one part payment that moves the exposure band, one inside the band, no payment since the decision, a stale product with its date and no answer beyond 2 s | C3, C4 |
| rwb-source-data appraisal fake | The accepted appraisal of asset `AST-2026-001111` at its value, type and date; an appraisal not yet accepted; a stale product | C3, C4 |
| rwb-deviation fake | Case `RC-2026-001111` with a deviation cleared after a pause, a deviation still open, and no deviation | C3, C4 |
| rwb-decision recommendation fake | The recommendation of the earlier decision with `expectedReturnByRoute`, `reasons`, `ruleVersion` and `agentVersion`; a case with no recommendation yet | C2, C4 |
| rwb-decision rule-in-force fake | The rule id and version, the segment dimensions and the gate thresholds at their version in force; a business date with no rule row | C3, C4 |
| rwb-case case-state fake | Case `RC-2026-001111` at a route state that may reopen; a case closed, cancelled or in a legal hold | C3, C4 |
| rwb-access authorise fake | The capability area Treatment and offer, right U accepted and refused | C5 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C4 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-001111`, with the reopen elements read once | C2, C4 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The rows whose names or product codes are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2643; ASM-4351).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed rows (7 calls) | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; two rwb-source-data data products, the rwb-deviation row, the two rwb-decision rows, the rwb-case state row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no declared subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `collectRouteChange` and `reopenRouteDecision` on `rwb-valuation`; no Schedule |
| File | None declared | The payments and the appraisal arrive through ACE ingestion and REST data products; no file is declared |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S1 rwb-valuation (Valuation and route)/RWB S1 E4011 CON Reconsider the route after new information - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S1-E4011.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition in this baseline: it references the payments and the appraisal as the rwb-source-data data products and declares no `v_ace_*` element and no ACE table. DP-03 declares the record element and the transaction it joins. DP-13 moves the base of the one operation. DP-19 declares the route SCR-13 reads the answer through.

**Sections and owners of the review.** The document is written in seven parts: the provided operation, the six consumed rows, the reopen and record elements, the workflow and its activities, the tables, the fakes, and the naming and boundary rule. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Fakes.** One per consumed row plus the composite route, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C4).

**Done when.** The six criteria pass, the six reviewer roles have closed their comments, the compatibility check passes on the tag, the nine fakes are published with their documented answers, and RWB-S1-E4011-APP can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Treatment and offer right calls the declared operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `RouteRequest` is absent or invalid | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the payments or the appraisal is stale | {product} is from {date}. Today's ACE batch has not arrived. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published operation name or product code | Not specified in the source documents (GAP-2643; ASM-4351). |

The four message IDs are those of FSD S1 A2.11.3.1 and of the platform set, copied unchanged. The two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-13 Route decision through the gateway-bff composite route (DP-19). What this story fixes is the element list of the reopen answer and the states the screen can show from this service's answer.

| Screen | States | What the route reads on this service |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | The reopen reason code, the change reference of the value, the payment and the deviation, the segment before and after, the record with its rule version, and the override reason of the submission |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The route itself, its merge order and its field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-011-01 | C2, C4: the operation and the reopen element with its versions | Contract | The published schema and the recorded answers of case `RC-2026-001111` |
| TC-E4-011-02 | C4: the record element and the stopped chain | Contract | The record element, a healthy stub and a stopped stub |
| TC-E4-011-03 | C5: the rights and the error envelope of the declared operation | Contract | One request per right, including a role without it; one request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-011-04 | C3, C6: the six consumed rows, the boundary and the empty publication | Contract | The six rows with and without a published name or product code; the base, the topic, the queue and the schema; an outbox declaration that must stay empty |
| TC-S1-E4011-CON-01 | C3: the placeholder and the gap of an unpublished name or product code | Contract | The six consumed rows, each with and without a published name |
| TC-S1-E4011-CON-02 | C6: the naming, the boundary and the absent foreign element | Contract | A draft that names a foreign schema, a monolith base, a foreign topic, a Schedule, a `v_ace_*` element, a `deviation` element or a `rule_row` element |
| TC-S1-E4011-CON-03 | C1: the compatibility check on the published schema | Contract | The previous tag, an additive draft and a breaking draft |

The four legacy case IDs are the legacy test cases of RWB-E4-011 in their legacy order, mapped onto this contract deliverable: the main path and its elements (01), the failure of the decision log (02), the access path (03) and the principle-5 record failure (04). The three `TC-S1-E4011-CON-` cases are new and test the parts of the baseline no legacy case touches. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the baseline: the reason codes, the route codes of `LOV-ROUTE`, the segment dimensions and the rule version are referenced with their list, their version or their row, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and versions only, and every fixture is synthetic.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the payment and the appraisal appear only as the rwb-source-data data products (DP-05).
- The case stays with rwb-case, the deviation with rwb-deviation and the rules with rwb-decision: no `recovery_case` element, no `deviation` element and no `rule_row` element is declared as this service's own (BR10).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Quartz row, no Schedule, no foreign schema and no event published by this baseline.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-011, disposition Split (rework); AC1 and AC2 are owned by RWB-S1-E4011-APP; this story carries no legacy criterion and fixes the surface both touch | 1, 11, 12, 16 |
| Feature | FEAT-VAL-11 Reconsider the route after new information, module S1, epic E4, depends on FEAT-VAL-07 | 1, 2, 3 |
| FSD S1 v3 | A2.11.2 steps and prerequisites; A2.11.3.1 VR-S1-011-1 and BR-S1-011; A2.11.3.3 roles; AC-S1-011-01; AC-EXC-S1-011-01 and -02; SCR-13 | 2, 3, 8, 12, 14, 15 |
| TSD S1 v2 | T2 components; T3.1 `valuation` and `score`; T3.2 `LOV-ROUTE`; T3.3 relationships; T5.1 to T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 16 |
| API specification v4 | `POST /cases/{caseId}/route` with `RouteRequest` and `Approval`; `GET /cases/{caseId}/recommendation` with `Recommendation`; `GET /data-products/{productCode}/records`; `POST /cases/{caseId}/deviations` (S8) | 3, 11, 12.1, 12.2, 12.8 |
| Logical data model | DF-ACE-043 to DF-ACE-054, DF-COL-021 to DF-COL-025, DF-CAS-036 to DF-CAS-045, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | 11 |
| Routing logic | R-UNI-02, R-UNI-22, R-UNI-38, R-UNI-39 and R-UNI-40, R-DEV-19 (Business Rules and Routing Logic v4); no S1 route rule is in force, because the S1 package is Phase 2 | 8, 14 |
| Epics 3 to 8 specification | E4 FEAT-VAL-11 row, depends on FEAT-VAL-07 | 1, 3 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2642 to -6; ASM-4350 to -6 | 1, 3, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The read of the facts, the recompute, the record write, the route answer and the screen behaviour: RWB-S1-E4011-APP.
- The valuation order and acceptance (FEAT-VAL-01 to FEAT-VAL-04), the expected return (FEAT-VAL-05), the payoff and range (FEAT-VAL-06) and the recommendation (FEAT-VAL-07): the sibling route stories of this service.
- The ACE payment and appraisal facts and the freshness of the two data products: rwb-source-data (P1). The payment matching and posting: rwb-payment (P8).
- The deviation, its code, its handler and its clocks: rwb-deviation (S8) (GAP-2643). The retainment of the earlier decision and its versions: the data owner of this service (GAP-2645).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the segment dimensions, the gate thresholds, the package version, its approval, the recommendation projection and the central ledger: rwb-decision (P7) (GAP-2642).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The approval inside and above the limit, the hold, the forced litigation review, the reopen of a closed case and the route flow start of this module: the sibling route and case stories.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
