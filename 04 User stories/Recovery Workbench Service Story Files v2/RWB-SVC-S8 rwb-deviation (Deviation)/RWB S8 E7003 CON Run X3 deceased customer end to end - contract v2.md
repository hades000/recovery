# RWB-S8-E7003-CON Run X3 deceased customer end to end - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7003-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S8-E7003-CON-16); the squad sizes the story at refinement |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (path /api/recovery/deviation/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E7-003, the baseline the X3 branch of rwb-deviation builds against on Day 1. The baseline declares the two deviation operations `POST /cases/{caseId}/deviations` (API-S8-001) and `PATCH /deviations/{deviationId}` (API-S8-002) on `/api/recovery/deviation/v1` (DP-13), the four consumed rows of rwb-source-data, rwb-case, rwb-access and rwb-decision (DP-05), the decision-record element and the library that carries it (DP-03), the one publication `rwb.deviation.DeviationRaised.v1` (EV-06) on `rwb.deviation.events.v1` and the one subscription, the elements of `DeviationWorkflow` and its five activities, the rights, the error envelope and the fakes; it publishes no Schedule, because the ownership rows give S8 no job. The consumed operation names and the case event name are not published (GAP-3056; ASM-5154); the matrix shows no REST edge from S8 to P7 while the branch reads the DEV rows and the claim approval there (GAP-3056; ASM-5155). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E7003-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 17 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-deviation**, I want **the published contract baseline of the X3 branch of rwb-deviation, being its two operations, its four consumed rows, its decision-record element, its one event and one subscription, its workflow elements, its rights, its error envelope and its fakes, fixed and tagged before the build starts**, so that **the application story, the wave 4 harness and the four owners it consumes can build and test on Day 1 against one versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E7-003. It owns:

- the document that fixes `POST /cases/{caseId}/deviations` (API-S8-001) and `PATCH /deviations/{deviationId}` (API-S8-002) on base `/api/recovery/deviation/v1`: `DeviationRequest` and `DeviationOutcome` in, `Deviation` out, the `Idempotency-Key` header, the rights and the error set (DP-13);
- the four consumed rows: the customer and deceased-status data product of rwb-source-data, the case state, timer state and case event of rwb-case, the authorise operation of rwb-access and the rule package and claim approval of rwb-decision, each with its owner, its use and a placeholder where the name is not published (DP-05);
- the one publication of the branch, `rwb.deviation.DeviationRaised.v1` (EV-06), its topic, its envelope, its payload and its consumers, and the one subscription of the case event;
- the decision-record element, the library that carries it and the shared topic it reaches (DP-03);
- the elements of `DeviationWorkflow` and its five activities on task queue `rwb-deviation`;
- the subject of SCR-06 Raise deviation and SCR-08 Deviation queue, one hop through the gateway-bff composite route (DP-19);
- the fakes and their documented answers;
- the naming and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no monolith base, no Schedule.

It does not own: the raise, the routing, the contact stop, the estate path, the claim approval and the outcome behaviour, which are RWB-S8-E7003-APP; the case, its timers and its assignments, which are rwb-case's (P3); the customer facts of `v_ace_customer`, which are rwb-source-data's (P1); the notice and heir templates, which are rwb-comms' (P6); the evidence documents, which are rwb-document's (P5); the rule rows, the package, the approval and the ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; the cross-service journey, which is RWB-ITG-E7003-ITG; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets teams start together. Legacy RWB-E7-003 asks for a death that stops contact, notifies the heirs, files the insurance claim and settles the estate position, with the result recorded with its rule version, so the branch writes one row of its own and reads facts from four other services. Without a tagged baseline each of those shapes would be discovered at the first integration instead of at the review.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner, its use and its 2 s budget, and every row whose name is not published carries the placeholder and its gap (GAP-3056; ASM-5154).
- **one hop, one budget.** Each REST row is a single hop with a 2 s timeout and a breaker; the customer is never read from a view and the case never from a table (DP-05, ADR-020).
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document.

The business outcome the baseline protects is the one FEAT-DVF-03, REQ-DVH-008 and REQ-S8-001 of FSD S8 state. The baseline states no outcome and no business value of its own, and no criterion here asserts that a death is confirmed, that contact stops or that a claim is filed.

### 3. Preconditions

- The Ownership Map rows for S8 are in force: the table `deviation`, the operations `PATCH /deviations/{deviationId}` and `POST /cases/{caseId}/deviations`, the events EV-06 and EV-07, no job, and one workflow, `DeviationWorkflow`.
- The service naming is fixed: schema `rwb_deviation`, one login of its own, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with `.retry` and `.dlt`, task queue `rwb-deviation` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.deviation`.
- TSD S8 is the shape of record for the service: T-A.1 gives API-S8-001 and API-S8-002 with right Case record U; T-A.2 gives `DeviationRequest` and `DeviationOutcome` in, `Deviation` out, errors 401, 403, 404, 409, 422 and 503 and the `Idempotency-Key`; T6.1 gives the capability area and its rights.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions of this baseline and not in its H row.
- The API Specification v5 carries `Deviation`, `DeviationRequest` and `DeviationOutcome` and the two paths, and the ownership rows carry the two operations of the service, so the provided surface is published and no placeholder is needed for it.
- The customer data product, the case read, the authorise row, the rule package and the claim approval are named by no published operation, and the connection matrix shows no REST edge from S8 to P7; every such row carries the placeholder (GAP-3056; ASM-5154; ASM-5155).
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag (ASM-5161).

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S8 T-A.1, T-A.2, T3.1, T3.2 and T6.1, the FSD S8 A2.12 rules and the DP table.
2. Every provided operation is declared with its method, path, request, documented answer, rights, idempotency and error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The one publication is declared with its topic, its envelope, its payload and its consumers, and EV-07 is declared as the clearing story's and not this branch's.
5. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins.
6. The workflow and its five activities are declared with their input, their signals and their outcome elements.
7. The schema, the open fields and the two lists of values are published; a list is referenced with its identifier and its version and is never enumerated in code.
8. The fakes are declared with their documented answers, one per consumed row, one for the outbox and one for the composite route.
9. The compatibility check runs on the draft against the previous tag: a breaking change fails it.
10. The document goes to review as Draft; the reviewers are the owners of the four consumed rows and the tech lead of the service.
11. On the review's close the document is tagged; the application story and the wave 4 harness start against the tag and the fakes, and the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The row carries the placeholder and its gap; no path and no element is invented | C3, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails and the document needs a new major version | C1 |
| X3 | A declared operation reaches another service's data, base or table | The review refuses the baseline and the boundary test fails the build | C6 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C6 |
| X5 | The rights of an operation are not a row of the access matrix | The operation is not declared and the error set stays incomplete | C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a version, this document follows in a minor or major version, and the fake is updated | X2 |
| X7 | Two documents claim the same base, topic, queue or path | The owner named in the Ownership Map keeps it and the other document changes | C6 |
| X8 | A declared element carries a personal value | The review refuses the element; the payload holds identifiers only | C4, C6 |

X1 to X3 are the paths of an incomplete source, X4 to X6 the paths of a baseline moving under a build, X7 the naming boundary and X8 the personal-data boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order and the fake data are this story's choice; the paths, the requests, the answers, the rights and the error set are fixed by TSD S8 |
| Valuable | Five teams build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, two provided operations, four consumed rows, one event, one subscription, one decision-record element, one workflow with five activities and eight fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the X3 branch of rwb-deviation

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the lists of values of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The two deviation operations are published as declared (new, D-RCV-60)
    Given the operation table of the baseline
    When POST /cases/{caseId}/deviations and PATCH /deviations/{deviationId} on /api/recovery/deviation/v1 are read
    Then they name DeviationRequest and DeviationOutcome in, Deviation out, the Idempotency-Key header and the scope rule of T-A.2
    And every element carries its type, its nullability and its source

  Scenario: C3 The four consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-source-data, rwb-case, rwb-access and rwb-decision are read
    Then each row names its owner, its use, one hop and a 2 s budget
    And where the operation or event name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C4 The one publication and the one subscription are declared with no personal data (new, D-RCV-60)
    Given the event tables of the baseline
    When rwb.deviation.DeviationRaised.v1 on rwb.deviation.events.v1 is read
    Then it names EV-06, the outbox, the CloudEvents envelope and the payload caseId, deviationCode and raisedBy
    And the payload carries no name, address, contact value or identity number
    And DeviationCleared (EV-07) is declared as the clearing story's and not published by this branch

  Scenario: C5 The rights and the error envelope are declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the rights and the error set of each operation are read
    Then each names the capability area Case record and the right of the access matrix
    And the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503 in one problem envelope

  Scenario: C6 The decision-record element, the workflow elements, the fakes and the boundary hold (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the workflow table, the fake table and the naming rule are read
    Then the element names RWB-PLT-E1027-CON as its library, the shared topic and the transaction it joins
    And DeviationWorkflow and its five activities name their input, their signals and their task queue rwb-deviation
    And every consumed row has a fake with a documented answer, including the stopped decision-record stub
    And one base, one topic, one queue and one login are declared, with no monolith base, no foreign topic and no Schedule

  Scenario: C7 Each business rule BR1 to BR10 holds or is held by a guardrail or boundary test (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8
    When the baseline is read against each rule
    Then each rule holds in the baseline
    And a rule that is an architecture constraint is held by a guardrail or boundary test named in section 16

  Scenario: C8 The redelivery of a consumed event is declared (new, D-RCV-60)
    Given the one subscription of the baseline
    When a consumed event is delivered a second time
    Then the baseline declares how the redelivery is handled
    And where the handling is not published the row carries Not specified in the source documents (NEWAC-RWB-S8-E7003-CON-AC6)

  Scenario: C9 The retry and the timeout of each workflow activity are declared (new, D-RCV-60)
    Given the five activities of DeviationWorkflow
    When the retry and the timeout of each activity are read
    Then each names its retry and its timeout
    And a value the source documents do not give is Not specified in the source documents (NEWAC-RWB-S8-E7003-CON-AC7)

  Scenario: C10 A status change the model does not allow is refused (new, D-RCV-60)
    Given the status of a deviation and the transitions the model allows
    When a status change the model does not allow is requested through an operation Not specified in the source documents (NEWAC-RWB-S8-E7003-CON-AC8)
    Then the request is refused with one error of the error set of C5
    And no change is written
```

The ten criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the consumed rows, the publication, the rights, the envelope, the workflow, the fakes and the boundary. No criterion states a business outcome of the application story, and none asserts that a death is confirmed, that contact stops, that a claim is approved or that a rule fires.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, row, element and table: the baseline declares the two operations the Ownership Map gives S8 and names every other row with its owner | Ownership Map rows of S8; TSD S8 T-A.1 |
| BR2 | A consumed row with no published name carries the placeholder and its gap and never an invented path, an invented parameter or an invented transport | Template and Rules v1 §R9; GAP-3056 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | s9; ADR-020 |
| BR4 | Every REST row is one hop with a 2 s timeout, a breaker and no chain; ACE facts arrive on the rwb-source-data data product and never on a view of this service | DP-05; ADR-020 |
| BR5 | One publication and one subscription: EV-06 is declared with its payload and its consumers, EV-07 is the clearing story's, and no other event is declared on the topic | TSD S8 T5.3; Event and Messaging Design v5, EV-06 and EV-07 |
| BR6 | No personal data in any element, fake, example or log; the event payload holds the case, the code and the raised-by and nothing else | Template and Rules v1 §R7.2 (s17) |
| BR7 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any change, and its element is declared once for the service | DP-03 |
| BR8 | No business value is declared in the baseline: the codes, the outcomes and the service level are referenced with their list or their version | TSD S8 T3.2; FSD S8 A2.12.3.1 BR-S8-012 |
| BR9 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |
| BR10 | No Schedule is declared: the ownership rows give S8 no job, and the escalation is a durable timer inside the workflow | context pack S8 ownership rows (jobs: none) |

BR1 to BR10 are the rules of this baseline. The consuming rules of the branch, R-DEV-01, R-DEV-03, R-DEV-06 and R-DEV-20 with the three universal rules, are the application story's to apply; the baseline declares their identifiers and versions and asserts none of their values.

### 9. State transitions

The object of this section is the document, not a case: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, row, element, event, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the four consumed rows are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story and the harness |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | A new optional element only, and the check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer | X6 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name | X1 | The row carries the placeholder and the gap, and the draft continues |
| In review | A row reaches a foreign schema, base or topic | X3, X7 | The baseline is refused |
| In review | An element carries a personal value | X8 | The element is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-deviation | Authors the baseline, resolves the shape of the service's own two operations, the event, the workflow elements and the decision-record element, and signs the tag |
| Owner of rwb-source-data (P1) | Reviews the customer and deceased-status row and publishes the operation name when it exists |
| Owner of rwb-case (P3) | Reviews the case state, the timer state and the case event of the subscription |
| Owner of rwb-access (P4) | Reviews the authorise row and the capability area and right of each declared operation |
| Owner of rwb-decision (P7) | Reviews the rule-package row, the claim approval and the decision-record element with the platform library |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of every declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write | BR Field ID |
|---|---|---|---|---|
| The deviation elements (DF-CAS-036 to DF-CAS-045) | S8 (`rwb_deviation`) | id, caseId, deviationCode, raisedAt, raisedBy, pausedState, handlerUserId, contactStop, clearedAt, outcome, with their types and nullability | Written by the application story, declared here | Not specified in the source documents (DOR-RWB-S8-E7003-CON-7) |
| The customer elements of `v_ace_customer` (DF-ACE-055 to DF-ACE-074) | P1 (`rwb_source_data`) | The person key, the customer status and the policy link; referenced as the data product and not redefined (ASM-5157) | Consumed | Not specified in the source documents (DOR-RWB-S8-E7003-CON-7) |
| The case and timer elements (DF-CAS-001 to DF-CAS-023, DF-WRK-027 to DF-WRK-036) | P3 (`rwb_case`) | The case reference, its state, the paused state, the stage timer and the prescription date; referenced, not redefined | Consumed | Not specified in the source documents (DOR-RWB-S8-E7003-CON-7) |
| The assignment elements (DF-WRK-009 to DF-WRK-016) | P3 (`rwb_case`) | The handler and the task; the handler is written on the deviation and the task stays with rwb-case | Consumed, not declared as a table | Not specified in the source documents (DOR-RWB-S8-E7003-CON-7) |
| The document elements (DF-DOC-001 to DF-DOC-011) | P5 (`rwb_document`) | The document identifiers of the request; the evidence and its storage reference are the document hub's | Consumed as identifiers only | Not specified in the source documents (DOR-RWB-S8-E7003-CON-7) |
| The rule elements of `rule_row` (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | The rule id, the version and the route set in force, and the claim approval result; referenced, not redefined | Consumed | Not specified in the source documents (DOR-RWB-S8-E7003-CON-7) |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_deviation` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time | Written through the library | Not specified in the source documents (DOR-RWB-S8-E7003-CON-7) |

The baseline declares the one table of the service, `deviation`, and no column beyond TSD S8 T3.1: the claim reference and the heir notification reference are carried in `outcome` and in the decision record, and no source names a column for either (GAP-3056; ASM-5159). It enumerates no business value: `LOV-DEVIATION`, `LOV-RAISED-BY`, `LOV-DEV-OUTCOME` and the service level are referenced with their identifier and version. The parameters and the reference-data contract that the branch reads are named by DP-06 and DP-07. **No personal data** appears in any element, fake or example, and every fixture identifier is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). These are the two operations the legacy story names in its Endpoints table, and the only ones this baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/deviations` | `DeviationRequest` in (`deviationCode`, `reason`, `documentIds`), `Deviation` out (API-S8-001) | Case record, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat |
| PATCH | `/deviations/{deviationId}` | `DeviationOutcome` in (`outcome`, `note`), `Deviation` out (API-S8-002) | Case record, right U, scope applied | Not applicable; the state guards a repeat |

The error envelope of each operation: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope case or deviation, 409 for a second open X3, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The customer and deceased-status read (operation name Not specified in the source documents (GAP-3056; ASM-5154)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The customer of the case, the deceased status, the policy link and the freshness stamp; faked |
| `GET /cases/{caseId}` family and the timer read (operation names Not specified in the source documents (GAP-3056; ASM-5154)) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the paused state, the stage timer and the prescription date; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |
| The rule-package and claim-approval read (operation name Not specified in the source documents (GAP-3056; ASM-5154)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEV rows and the version in force, and the approval of an insurance claim; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag instead of inventing a surface (BR2). The plan gives this slice no C dependency, so every row is built against its fake, and the absence is recorded as GAP-3056 with ASM-5154. The connection matrix shows no REST edge from S8 to P7, so that row is declared with the placeholder and its owner settles it (ASM-5155).

#### 12.3 Events published

| Event | Topic | Payload (no personal data) | Consumers |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | caseId, deviationCode, raisedBy | rwb-comms (contact stop) and rwb-case (clock pause and banner) |

One event, in the CloudEvents envelope, through the outbox in the caller's transaction, keyed by the case. The event name follows the naming rule `rwb.<short>.<Event>.v1`; the ownership rows give S8 EV-06 and EV-07 and the catalogue publishes neither target name, so the name above is the rule's form and the payload is the one Event and Messaging Design v5 gives EV-06. `rwb.deviation.DeviationCleared.v1` (EV-07) is the clearing story's and is not published by this branch (BR5). The contact stop is the rwb-comms subscription to this event and not a call of this service (ASM-5156).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| The case event that opens or resumes a stage (name Not specified in the source documents (GAP-3056; ASM-5154)) | the topic of rwb-case | P3 rwb-case | Starts the deviation branch when a case of this service's scope changes stage; faked |

One subscription, through the inbox with the duplicate rule R-UNI-40. The raise and the outcome are commands of this service and not events.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per deviation, continues-as-new | `rwb-deviation` | Input: the case, the deviation, the code, the paused state and the rule package in force; signals: the approval result and the outcome command |
| `raiseDeviation` | Activity | `rwb-deviation` | The case, the code, the raised-by and the evidence identifiers in; the deviation, the record, the outbox row and the step outcome out |
| `routeToOwner` | Activity | `rwb-deviation` | The code and the rule rows in force in; the handler, the team and the flags for Legal and the approval out |
| `applyContactStop` | Activity | `rwb-deviation` | The case and the code in; `contact_stop` and the event element out |
| `openEstatePath` | Activity | `rwb-deviation` | The case, the policy link and the heir path in; the claim reference and the notification reference out |
| `recordOutcome` | Activity | `rwb-deviation` | The outcome, the note and the rule version in; the deviation, the case move and the record out |

`DeviationWorkflow` is the one workflow the ownership rows give S8. This baseline fixes its input, its two signals and the five activities the branch adds; the other branches of the workflow are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable. The stage timer's pause is applied by rwb-case on the EV-06 subscription and is not an activity of this service. The approval of a deviation is a step inside `DeviationWorkflow`, taken by the role the code assigns; the decision-record library writes the entry, and no ApprovalWorkflow edge to rwb-decision (P7) is added while that question is open (GAP-1820). The workflow is started when an agent or officer flags the deviation (EV-06 starts screening) or when universal rules R-UNI-04 to 09 fire; its workflow ID form is Not specified in the source documents (CG-ALL-11487) and its duplicate-start policy is Not specified in the source documents (CG-ALL-11487).

#### 12.6 Schedules

None. The ownership rows give S8 no job, and this baseline declares no Temporal Schedule and no legacy Quartz job. The escalation of R-DEV-20 is a durable timer inside `DeviationWorkflow` and not a Schedule, and its level is a rule row read at its version (BR10).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `deviation` | S8, in `rwb_deviation` | The one table of the Ownership Map rows of S8; its elements are those of TSD S8 T3.1 |
| `decision_record` | PLT library, created in `rwb_deviation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| `idempotency_key` | PLT library, created in `rwb_deviation` | The key of the repeated raise and the answer it holds |
| `outbox`, `inbox` | PLT library, created in `rwb_deviation` | The one publication and the one subscription of the branch |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `document` (P5), `template` (P6), every `v_ace_*` view and `v_ace_customer` (P1) are named by their owner and never declared here. No foreign key leaves `rwb_deviation`: the case, the person, the document and the rule are identifiers, not keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data customer fake | Case `RW-2026-000502` with a customer marked deceased, its policy link and a fresh stamp; the same case with a stale product and its date; no answer beyond 2 s | C3, C6 |
| rwb-case case and timer fake | The case at `WITH_FCR_OFFICER` with a running stage timer and a prescription date; a case at another state | C3, C6 |
| rwb-case event fake | One stage event for the case, delivered once and then repeated with the same key | C3, C4 |
| rwb-access authorise fake | Case record, right U accepted and refused | C5 |
| rwb-decision rule and approval fake | The DEV rows of R-DEV-03, R-DEV-06 and R-DEV-20 at their version in force; the claim approved, refused and not taken | C3, C6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| Outbox and inbox stub | The outbox row committed with the record, and a rollback that leaves neither | C4, C6 |
| gateway-bff composite route fake | The merged SCR-06 and SCR-08 answers for `RW-2026-000502`, with the deviation, the handler and the contact stop read once | C2, C6 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-3056; ASM-5154).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` on `/api/recovery/deviation/v1`; the rwb-source-data customer row, the rwb-case rows, the rwb-access row and the rwb-decision row; one hop, 2 s |
| Kafka | 1 published, 1 consumed | `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1`; the rwb-case stage event; the shared `rwb.decision-record.v1` is the library's publication |
| Temporal | 1 workflow and 5 activities | `DeviationWorkflow`, `raiseDeviation`, `routeToOwner`, `applyContactStop`, `openEstatePath` and `recordOutcome` on `rwb-deviation`; no Schedule |
| File | None declared | The claim pack and the heir letter are rwb-document's and rwb-comms' and are referenced by identifier only |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S8 rwb-deviation (Deviation)/RWB S8 E7003 CON Run X3 deceased customer end to end - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S8-E7003.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition as much as a pattern: no `v_ace_*` grant, no ACE table and no ACE view for this service, and the customer arrives on the data product. DP-03 fixes the transaction of the raise and of the outcome. DP-13 moves the base of the two operations. DP-19 is how the two screens reach this service. DP-04, DP-09 and DP-10 are not in the plan's pattern set although the branch evaluates the DEV rows, publishes EV-06 and runs a workflow, so the rule read, the outbox and inbox and the workflow kit are tracked and not added to the metadata (GAP-3056; ASM-5155).

**Sections and owners of the review.** The document is written in nine parts: the two operations, the four consumed rows, the publication and the subscription, the workflow and its activities, the tables, the fakes, the call-type summary, the data elements and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Fakes.** One per consumed row, one for the outbox and inbox and one for the composite route, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C6).

**Done when.** The six criteria pass, the four reviewer roles have closed their comments, the compatibility check passes on the tag, the eight fakes are published with their documented answers, and RWB-S8-E7003-APP and RWB-ITG-E7003-ITG can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Case record right calls a declared operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `DeviationRequest` or `DeviationOutcome` is absent or invalid | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S8-001 | The raise has succeeded and the case is with its handler | {deviation} was raised. The case is with {handler}. |
| MSG-P1-001 | The ACE data product behind the customer row is stale | {product} is from {date}. Today's load has not arrived. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row has no published operation name | Not specified in the source documents (GAP-3056; ASM-5154). |
| Document rule | An error code of the two operations has no bound message ID | Not specified in the source documents (GAP-3056). |

The five message IDs are those of FSD S8 A2.12.3.1, of the legacy set of the key and of the platform set, copied unchanged. The two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-06 Raise deviation and SCR-08 Deviation queue through the gateway-bff composite route (DP-19). What this story fixes is the element list of the two answers and the states the screens can show from this service's answer.

| Screen | States (sources) | What the screen reads on this service |
|---|---|---|
| SCR-06 Raise deviation | Form; saved; empty, loading, error and no access: Not specified in the source documents (CG-ALL-11495) | The code list, the reason, the document identifiers, the customer and deceased status read once, the handler and the message |
| SCR-08 Deviation queue | Loading; list; empty, error and no access: Not specified in the source documents (CG-ALL-11496) | The open deviations by code, handler and age, the contact stop and the claim state |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The layout, the merge order and the field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-003-01 | C2, C3: the two operations and the consumed rows of the X3 journey | Contract | The published schema and the recorded answers for case `RW-2026-000502` |
| TC-E7-003-02 | C2, C5: the shape of `DeviationRequest` and the answer, and the rights of the raise | Contract | Valid, invalid, duplicate and unauthorised raise requests |
| TC-E7-003-03 | C2, C5: the shape of `DeviationOutcome` and the three outcome codes | Contract | The three codes of `LOV-DEV-OUTCOME`, a code outside the list and a refused call |
| TC-E7-003-04 | C1, C6: the decision-record element and the stopped chain | Contract | The element, a healthy stub and a stopped stub |
| TC-E7-003-05 | C5: the error envelope of the two operations | Contract | One request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E7-003-06 | C4, C6: the publication, the payload and the personal-data boundary | Contract | EV-06 with and without a forbidden field; an outbox that must hold one event only |
| TC-S8-E7003-CON-01 | C3: the placeholder and the gap of an unpublished operation or event name | Contract | The four consumed rows, each with and without a published name |
| TC-S8-E7003-CON-02 | C6: the fakes, the workflow elements and the boundary | Contract | The eight fakes, one fake that answers more than its document, and the base, topic, queue and schema check |
| TC-S8-E7003-CON-03 | BR1, BR9: the tables of §12.7 at the owner boundary | Contract | The tables of §12.7 each named by its owner, and one table of another owner declared as its own |
| TC-S8-E7003-CON-04 | BR1: one owner per operation, row, element and table | Contract | The two operations, and each other row named with its owner |
| TC-S8-E7003-CON-05 | BR2: the placeholder for a consumed row with no published name | Contract | Each consumed row with and without a published name |
| TC-S8-E7003-CON-06 | BR3: additive minor and breaking major versions | Contract | A new optional element, and a removal, a rename, a type change and a new required element |
| TC-S8-E7003-CON-07 | BR4: one hop, 2 s timeout, breaker and no chain | Contract | A REST call that exceeds 2 s, and a call that would chain a second hop |
| TC-S8-E7003-CON-08 | BR5: one publication and one subscription | Contract | EV-06 with its payload and consumers, and a second event declared on the topic |
| TC-S8-E7003-CON-09 | BR6: no personal data in any element, fake, example or log | Contract | The elements, fakes and examples with and without a personal-data field |
| TC-S8-E7003-CON-10 | BR7: decision record written in the caller's transaction before any change | Contract | The decision-record element, and a write that fails before the change |
| TC-S8-E7003-CON-11 | BR8: no business value declared; codes referenced with list or version | Contract | The three codes of LOV-DEV-OUTCOME referenced by identifier and version |
| TC-S8-E7003-CON-12 | BR9: no other service's table, operation or topic declared as own | Contract | A declaration that names another service's table, operation or topic |
| TC-S8-E7003-CON-13 | BR10: no Schedule declared; escalation is a durable timer | Contract | The baseline with no job, and the escalation as a timer inside the workflow |
| TC-S8-E7003-CON-14 | C7: BR1 to BR10 each hold, or a guardrail or boundary test holds them | Contract | Each rule BR1 to BR10, with the rule held and with the rule broken |
| TC-S8-E7003-CON-15 | C8: the redelivery of a consumed event is declared | Contract | Not specified in the source documents (NEWAC-RWB-S8-E7003-CON-AC6) |
| TC-S8-E7003-CON-16 | C9: the retry and the timeout of each workflow activity are declared | Contract | Not specified in the source documents (NEWAC-RWB-S8-E7003-CON-AC7) |
| TC-S8-E7003-CON-17 | C10: a status change the model does not allow is refused | Contract | A status change the model does not allow is requested |

The six legacy case IDs are the legacy cases of RWB-E7-003 in their legacy order, carried here at Contract level because the baseline publishes the shapes they exercise; the application story carries the same IDs at Component level, and the `-ITG` copies belong to RWB-ITG-E7003-ITG. The two `-CON` cases are this story's own.

### 17. Guardrails

- No business value in the baseline: the codes, the outcomes and the service level are referenced with their list and their version, never enumerated as constants.
- No personal data in any element, fake, example or log; the event payload is the case, the code and the raised-by, and nothing else (BR6).
- ACE data only through the owner's contract: no `v_ace_*` grant, no ACE table and no ACE view is declared or read (DP-05).
- One base, one topic, one queue and one login per service, no monolith base, no foreign topic and no foreign operation (DP-13, DP-14).
- One publication and one subscription, and EV-07 left to the clearing story; a baseline that declares a second event fails the review (BR5).
- The decision record is written before any change and the raise is idempotent; the element is declared once and the library is the only writer (DP-03, BR7).
- No Schedule and no Quartz row is declared, because the ownership rows give S8 no job (BR10).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E7-003, disposition Split (rework); no legacy criterion owned by this slice, whose criteria are new; AC1 is RWB-ITG-E7003-ITG's and AC2 to AC4 are RWB-S8-E7003-APP's | 1, 7, 16 |
| Feature | FEAT-DVF-03 Run X3 deceased customer end to end, module S8, epic E7, depends on FEAT-DVH-04 | 1, 2 |
| FSD S8 v3 | A1.4 preconditions; A2.12.2 integration points; A2.12.3.1 VR-S8-012-1 and BR-S8-012; A2.12.3.3 roles; requirements REQ-DVH-008 and REQ-S8-001; SCR-06 and SCR-08 | 2, 3, 8, 14, 15 |
| TSD S8 v2 | T2 components; T3.0 standard columns; T3.1 `deviation`; T3.2 the lists of values; T3.3 relationships; T4 the DEVIATION machine; T5.2 and T5.3; T6.1 and T6.2; T-A.1 and T-A.2 API-S8-001 and API-S8-002 | 3, 8, 11, 12, 13, 16 |
| API specification v4 | `Deviation`, `DeviationRequest`, `DeviationOutcome` and the two paths; the required list of the answer | 11, 12.1 |
| Events and patterns | EV-06 DeviationRaised and EV-07 DeviationCleared; DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5); the naming rule of §R4; no Schedule | 12, 13 |
| Gaps and assumptions | GAP-3056 for this story; ASM-5154, -2, -3, -4, -6 and -8; the application gap GAP-3055 is cited here where the behaviour is read | 1, 3, 12, 13, 16 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The behaviour of the branch: the raise, the routing, the contact stop, the estate path, the claim approval and the outcome: RWB-S8-E7003-APP.
- AC1 of the legacy key and the cross-service journey that evidences it: RWB-ITG-E7003-ITG.
- The other branches of `DeviationWorkflow` and the other deviation codes: the sibling stories of rwb-deviation.
- The case of record, its states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3), whose operation and event names are placeholders.
- The ACE customer and policy facts and the freshness of the data product: rwb-source-data (P1).
- The notice and heir templates and the contact-stop suppression: rwb-comms (P6), which is a subscriber of EV-06.
- The claim pack and the evidence documents: rwb-document (P5).
- The rule rows, the package, the approval of an insurance claim and the central ledger: rwb-decision (P7), whose row carries the placeholder.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-06 and SCR-08: RWB-PLT-N001-CON and the edge stories.
- The deployment of the baseline's behaviour, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
