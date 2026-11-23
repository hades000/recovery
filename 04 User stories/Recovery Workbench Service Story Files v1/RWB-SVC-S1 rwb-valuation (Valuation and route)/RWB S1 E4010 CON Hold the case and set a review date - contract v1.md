# RWB-S1-E4010-CON Hold the case and set a review date - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4010-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-010 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-010, the baseline the hold step of rwb-valuation builds against on Day 1. The baseline declares the hold element set of the route operation `POST /cases/{caseId}/route` (API-S1-001) on `/api/recovery/valuation/v1` (DP-13), its held-state answer, the four consumed rows of rwb-case, rwb-decision and rwb-access, the decision-record element and the library that carries it (DP-03), the elements of `RouteDecisionWorkflow` and its three hold activities, the reason code list as data, the rights, the error envelope and the fakes; it publishes no event and declares no Schedule, because the ownership rows give S1 no event and no job. Where the hold, its reason and its review date are persisted is not published and the service owns no table (GAP-2638; ASM-4343); the review date has no clock owner and the prerequisite FEAT-CWC-11 no published identity (GAP-2639; ASM-4344, ASM-4347); the reason codes and any date bound are not published and the FSD catalog of the feature carries the valuation fields (GAP-2640; ASM-4346, ASM-4348); the element set of `RouteRequest` and `Approval` and the names of the four consumed rows are not published, and the plan carries no C row (GAP-2641; ASM-4349). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-valuation**, I want **the published contract baseline of the hold slice of rwb-valuation, being its hold element set on the route operation, its four consumed rows, its decision-record element, its workflow elements and timer, its reason-code reference, its rights, its error envelope and its fakes, fixed and tagged before the build starts**, so that **the application story, the wave 3 harness and the three owners it consumes can build and test on Day 1 against one versioned surface instead of guessing the shape of a hold**.

This is the contract slice of legacy RWB-E4-010. It owns:

- the document that fixes `POST /cases/{caseId}/route` (API-S1-001) on base `/api/recovery/valuation/v1` for the hold: `RouteRequest` in, `Approval` out, the `Idempotency-Key`, the rights and the error set (DP-13);
- the hold element set: the hold reason code and the review date in the command, and the held state, the reason, the review date and the record's rule version in the answer, each with its type, its nullability and its source where a source gives one (GAP-2641; ASM-4349);
- the four consumed rows: the case state and the hold-move answer of rwb-case, the rule-in-force, reason-code and ledger read of rwb-decision, and the authorise operation of rwb-access, each with its owner, its use and a placeholder where the name is not published;
- the decision-record element, the library that carries it and the shared topic it reaches (DP-03);
- the elements of `RouteDecisionWorkflow` and its three hold activities on task queue `rwb-valuation`, and the rule that the review date is a workflow timer and not a Schedule;
- the reason-code list as reference data of the business date, referenced by identifier and never enumerated (GAP-2640);
- the subject of SCR-13 Route decision, one hop through the gateway-bff composite route (DP-19);
- the fakes and their documented answers;
- the naming and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no monolith base, no event and no Schedule.

It does not own: the hold behaviour, the record writes, the timer's wake, the case-move answer and the screen's behaviour, which are RWB-S1-E4010-APP; the route recommendation and the approvals of the sibling route stories of this service; the case of record, its held state and FEAT-CWC-11, which are rwb-case's (P3); the rule rows, the package version and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the field list of SCR-13, which are RWB-PLT-N001-CON; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets the teams start together. Legacy RWB-E4-010 asks the case owner to hold a case with a reason and a review date and to have the result recorded with its rule version, so the step reads the case from one service, reads the rule version and the codes from a second, authorises through a third, answers a move to the first and writes one record in a fourth. Without a tagged baseline each of those shapes would be discovered at the first integration instead of at the review.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner, its use and its 2 s budget, and every row whose name is not published carries the placeholder and its gap (GAP-2641; ASM-4349).
- **one hop, one budget.** Each consumed row is a single hop with a 2 s timeout and a breaker, and the case is never read from a table (DP-01, ADR-020).
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document (C1).

The business outcome the baseline protects is the one FEAT-VAL-10 of FSD S1 states: the owner holds a case where no route is right yet, with a date the hold is reviewed. The baseline states no outcome and no business value of its own, and no criterion here asserts that a case is held or that a date is reached.

### 3. Preconditions

- The Ownership Map rows for S1 are in force: `POST /assets/{assetId}/valuations`, `POST /assets/{assetKey}/valuations` and `POST /cases/{caseId}/route`; no table, no event, no job, and one workflow, `RouteDecisionWorkflow`.
- The service naming is fixed: schema `rwb_valuation`, one login of its own, base `/api/recovery/valuation/v1`, topic `rwb.valuation.events.v1` with `.retry` and `.dlt`, task queue `rwb-valuation` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.valuation`.
- TSD S1 is the shape of record for the service: T-A.1 gives API-S1-001 with right Treatment and offer U; T-A.2 gives `RouteRequest` in, `Approval` out, errors 401, 403, 404, 409, 422 and 503 and the `Idempotency-Key`; T6.1 gives the capability area and its rights. T-A.2 publishes no field table for either type (GAP-2641; ASM-4349).
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions of this baseline and not in its H row.
- The hold has no published durable home: the ownership rows give S1 no table, the legacy Data table of the key names `recovery_case`, `assignment`, `decision_log_entry` and `rule_row` and no hold field, and TSD S1 T3.1 declares `valuation` and `score` only (GAP-2638; ASM-4343).
- The review date has no published clock: the ownership rows give S1 no job, no route-decision rule row fires a review date, and FSD S1 A2.10.4.4 declares no background event, so the baseline declares a workflow timer and no Schedule (GAP-2639; ASM-4344).
- The reason code list and any bound on the review date are not published; the field catalog of FSD S1 A2.10.3.2 carries the valuation fields of A2.4 and no hold field (GAP-2640; ASM-4346, ASM-4348).
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S1 T-A.1, T-A.2 and T6.1, FSD S1 A2.10 rules and field catalog, the features sheet of the Epics 3 to 8 specification and the DP table.
2. Every provided operation is declared with its method, path, request, documented answer, rights, idempotency and error set; the hold is declared as an element set of the one operation the legacy Endpoints table names.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The hold element set is declared with the type and the nullability a source gives, marked optional where no source gives one, and never made required by this baseline.
5. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins.
6. The workflow, its three hold activities and its review timer are declared with their input, their signals, their timing and their outcome elements.
7. The reason-code reference is declared as a list of the business date with its identifier, and the list is never enumerated.
8. The fakes are declared with their documented answers, one per consumed row, one for the timer and one for the composite route.
9. The compatibility check runs on the draft against the previous tag of this service's baseline family: a breaking change fails it.
10. The document goes to review as Draft; the reviewers are the owners of the three consumed services and the tech lead of the service.
11. On the review's close the document is tagged; the application story and the wave 3 harness start against the tag and the fakes, and the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for an element or a shape the sources do not publish | The row carries the placeholder and its gap and is marked optional; no type and no element is invented | C2, C3 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails and the document needs a new major version | C1 |
| X3 | A declared operation reaches another service's data, base or table | The review refuses the baseline and the boundary test fails the build | C5 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C6 |
| X5 | The rights of an operation are not a row of the access matrix | The operation is not declared and the error set stays incomplete | C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a version, this document follows in a minor or major version, and the fake is updated | X2 |
| X7 | Two documents claim the same base, topic, queue or path | The owner named in the Ownership Map keeps it and the other document changes | C5 |
| X8 | The baseline is asked to declare a Schedule, a job or a polling row for the review date | The row is refused: the review date is a workflow timer and the ownership rows give S1 no job | C4 |

X1, X6 and X8 are the paths of an incomplete or conflicting source, X4 and X5 the paths of a baseline moving under a build, and X2, X3 and X7 the compatibility and naming boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order and the fake data are this story's choice; the path, the request, the answer, the rights and the error set are fixed by TSD S1 |
| Valuable | The application story, the harness and three owners build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, one provided operation with a hold element set, four consumed rows, one decision-record element, one workflow with three activities and one timer, one reference list and eight fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the hold slice

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the reference identifiers of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The route operation and its hold element set are published as declared (new, D-RCV-60)
    Given the operation table of the baseline
    When POST /cases/{caseId}/route on /api/recovery/valuation/v1 is read
    Then it names RouteRequest in, Approval out, the Idempotency-Key header and the scope rule of T-A.2
    And the hold elements carry their type, their nullability, their source and a placeholder where no source publishes one
    And the reason code is declared as a reference of the business date and is not enumerated

  Scenario: C3 The four consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-case, rwb-decision and rwb-access are read
    Then each row names its owner, its use, one hop and a 2 s budget
    And where the operation name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C4 The timer, the decision-record element and the empty publication are declared as stated (new, D-RCV-60)
    Given the workflow table, the schedule table and the publication tables of the baseline
    When the review date, the decision-record element and the events are read
    Then the review date is declared as a timer of RouteDecisionWorkflow on rwb-valuation and no Schedule and no job is declared
    And the decision-record element names RWB-PLT-E1027-CON, the shared topic and the transaction it joins
    And no event is published and no event is consumed

  Scenario: C5 The rights, the error envelope and the naming boundary are declared (new, D-RCV-60)
    Given the operations and the naming section of the baseline
    When the rights, the error set and the base, topic, queue and schema are read
    Then each operation names the capability area Treatment and offer and the right of the access matrix
    And the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503 in one problem envelope
    And one base, one topic, one queue and one login are declared and no foreign schema and no foreign table appear

  Scenario: C6 The fakes are declared for every consumed row and the timer (new, D-RCV-60)
    Given the fake table of the baseline
    When the fakes and their documented answers are read
    Then every consumed row has a fake, including the stopped decision-record stub and the timer environment
    And no fake answers a field its owner's document does not name
```

The six criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the reference identifier, the consumed rows, the timer, the publication, the rights, the envelope, the naming and the fakes. No criterion states a business outcome of the application story, and none asserts that a case is held, that a date is reached or that a rule fires.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, row, element and table: the baseline declares the route operation that the Ownership Map gives S1 and names every other row and element with its owner | Ownership Map rows of S1; TSD S1 T-A.1 |
| BR2 | A consumed row or an element with no published shape carries the placeholder and its gap, is marked optional, and never receives an invented path, parameter, type or transport | Template and Rules v1 §R9; GAP-2641 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; C1 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain; the case is never read from a table | DP-01; ADR-020 |
| BR5 | No event is published and no event is consumed by this baseline: the ownership rows give S1 no event, and the decision record reaches the ledger on the shared topic through the library of DP-03 | DP-03; context pack S1 ownership rows |
| BR6 | The review date is declared as a timer of `RouteDecisionWorkflow`; the baseline declares no Schedule, no Quartz job and no polling row, because the ownership rows give S1 no job | ASM-4344; Template and Rules v1 §R5.5 |
| BR7 | The reason code and its list are referenced by identifier and version and are never enumerated; no bound is declared on the review date, because no source publishes one | FSD S1 A2.10.3.1 BR-S1-010; GAP-2640 |
| BR8 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any answer, and its element is declared once for the service | DP-03 |
| BR9 | No personal data in any element, fake, example or log of the baseline; the caller is declared as an identifier and not as a name | Template and Rules v1 §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

### 9. State transitions

The object of this section is the document, not a case: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, row, element, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the three consumed services are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story and the harness |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | A new optional element only, and the check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer | X6 | Draft of a new minor or major version, and the fake is updated |
| Baselined | A Schedule or a job is requested for the review date | X8 | Refused, and the timer row stands |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A row or an element has no published shape | X1 | It carries the placeholder and the gap, and the draft continues |
| In review | A row reaches a foreign schema, base or topic | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-valuation | Authors the baseline, resolves the shape of the service's own operation and hold elements where no owner speaks, and signs the tag |
| Owner of rwb-case (P3) | Reviews the case-state row, the hold-move answer, the lift back to the route decision and the task answer, and publishes FEAT-CWC-11 identifiers when they exist |
| Owner of rwb-decision (P7) | Reviews the rule-in-force row, the reason-code reference and the decision-record element with the platform library |
| Owner of rwb-access (P4) | Reviews the authorise row and the capability area and rights of each declared operation |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of every declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of this section |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The case reference, its route state and the move answers (DF-CAS-001 to DF-CAS-023) | P3 (`rwb_case`) | The case reference and its state, the hold move and the lift move; referenced, not redefined | Consumed |
| The reason code list | Reference data of the business date | Referenced by its identifier and its version, never enumerated (GAP-2640; ASM-4346) | Consumed as data |
| The hold reason and the review date | The record of the hold | Declared as elements of the command and of the decision record; no Field ID, no type and no column is published (GAP-2638; ASM-4343) | Written through the library |
| The rule elements of `rule_row` (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | The rule id, the rule version and the route set in force; referenced, not redefined | Consumed |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_valuation` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time | Written through the library |
| The task and assignment elements (DF-WRK-009 to DF-WRK-016) | P3 (`rwb_case`) | The task the review date raises; referenced as the move answer and never declared as a row of this service | Consumed as an answer |

The baseline declares no table of its own, because the Ownership Map gives S1 none while the legacy Data table of this key names four entities of other owners and no hold field (GAP-2638; ASM-4343). It declares no column, no index, no migration and no bound on the review date: every list, code and rule is referenced with its identifier and its version. **No personal data** appears in any element, fake or example: the caller is an identifier, and every fixture identifier is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This is the operation the legacy story names in its Endpoints table, and the only one this baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, carrying the hold reason code and the review date in the command and the held state, the reason, the review date and the record's rule version in the answer (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat |
| None | The hold write of its own | No source names an operation that writes the hold, its reason or its review date: the ownership rows give S1 no table, so the row carries Not specified in the source documents (GAP-2641; ASM-4349) and no path is declared | Not applicable | Not applicable |

The hold element set of `RouteRequest` is declared as the reason code and the review date, and of `Approval` as the held state, the reason, the review date and the rule version; each is optional in the baseline, because TSD S1 T-A.2 publishes the two type names and no field table and no source states how the hold enters them (GAP-2641; ASM-4349). The two valuation operations of the map belong to the appraisal-intake slice of RWB-S1-E4002-CON and are not declared here.

The error envelope of the declared operation: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid or unknown element, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state, its route state and the scope check, which the step tests before a hold is recorded; faked |
| The hold-move and lift-move answer (operation name Not specified in the source documents (GAP-2641; ASM-4349)) | `/api/recovery/case/v1` | P3 rwb-case | The move to the held state with the review date, the lift back to the route decision and the task answer; faked |
| The rule-in-force, reason-code and decision-log read (operation name Not specified in the source documents (GAP-2641; ASM-4349)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force, the reason codes of the business date and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag instead of inventing a surface (BR2). The reason-code reference is administered as data of the business date and no source says which answer carries it, so the baseline references it as an element of the rule-in-force answer and asserts no value (GAP-2640; ASM-4346). The plan gives this slice no C dependency, so every row is built against its fake.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event: the topic `rwb.valuation.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this baseline declares no event, no event name and no outbox row on it (BR5). The only publication of this step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service.

#### 12.4 Events consumed

None declared. The hold is started by the case owner's command on the route operation and woken by its own timer; FSD S1 A2.10.4.4 declares no background event for the feature and the ownership rows give S1 no event and no job, so the baseline declares no subscription and no consumer group. The lift on a reconsideration of FEAT-VAL-11 is a case move and not a subscription of this baseline.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the route set and the rule package in force; signals: the hold command, the review-date wake and the case-move answer; one durable timer to the review date |
| `holdRouteDecision` | Activity | `rwb-valuation` | The case, the reason code, the review date, the rule id and the version in force in; the held outcome and the move out |
| `recordHold` | Activity | `rwb-valuation` | The decision record, the idempotency row and the case-move answer out, in one transaction |
| `liftHold` | Activity | `rwb-valuation` | The case, the review date and the record of the hold in; the lift record, the move back to the route decision and the task answer out |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1. This baseline fixes its input, its three signals, its review timer and the three activities the hold adds; the remaining activities of the route decision are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S1 no job, and the review date is a durable timer of `RouteDecisionWorkflow` rather than a Temporal Schedule or a legacy Quartz job (BR6; ASM-4344). No source names a Schedule, a cut-off or a batch for the hold or for the review of a held case, and the timer is the only clock the baseline declares (GAP-2639).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table, so the hold, its reason and its review date are carried by the decision record and the case of record (GAP-2638; ASM-4343) |
| decision_record | PLT library, created in `rwb_valuation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7) and `deviation` (P3) are named by their owner and never declared here. If a data owner confirms a hold or review-date column, the DB story of this service creates it in its own Flyway sequence and this baseline declares its elements in a minor version.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | Case `RC-2026-000410` at the route decision with no route approved; the same case with a route approved; a case out of the caller's scope; no answer beyond 2 s | C3, C6 |
| rwb-case move-answer fake | The move to the held state with the review date accepted with its reference, the lift back to the route decision accepted, and each refused with its reason | C3, C6 |
| rwb-decision rule and log fake | The rule id, the reason codes and their version in force for the business date; the record the ledger holds, once and twice | C2, C6 |
| rwb-access authorise fake | The capability area Treatment and offer, right U accepted and refused | C5 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C4, C6 |
| Temporal test environment fake | A workflow whose clock is skipped to the review date, and a wake that arrives on a decided case | C4, C6 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000410`, with the held state, the reason and the review date read once | C2, C6 |
| Placeholder fake for an unpublished row | The documented use of the row and no field the source does not name, so the consumer can tell a published from an unpublished shape | C3 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2641; ASM-4349).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-case state and move rows, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no declared subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow, 3 activities and 1 timer | `RouteDecisionWorkflow`, `holdRouteDecision`, `recordHold` and `liftHold` on `rwb-valuation`; the review date is a workflow timer and the baseline declares no Schedule |
| File | None declared | The hold is command-driven and this service writes no file, and no source names a document for it |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S1 rwb-valuation (Valuation and route)/RWB S1 E4010 CON Hold the case and set a review date - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S1-E4010.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in eight parts: the provided operation with its hold elements, the four consumed rows, the publication, the workflow, its activities and its timer, the tables, the fakes, the call-type summary and the data elements. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3). The hold elements are declared optional, so the first tag does not break a consumer that does not carry them.

**Fakes.** One per consumed row plus the decision-record stub, the timer environment, the composite route and the placeholder, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C6).

**Done when.** The six criteria pass, the four reviewer roles have closed their comments, the compatibility check passes on the tag, the eight fakes are published with their documented answers, and RWB-S1-E4010-APP and the wave 3 harness can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Treatment and offer right calls the declared operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `RouteRequest` is absent or invalid, or the reason code is not in the list of the business date | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row or an element has no published shape | Not specified in the source documents (GAP-2641; ASM-4349). |

The three message IDs are those of the legacy message set of the key and of FSD S1 A2.10.3.1, copied unchanged. The two document rules are checks of this story and are not service messages; no freshness message is declared here, because this baseline reads no ACE data product.

### 15. Screens and states

The baseline serves SCR-13 Route decision through the gateway-bff composite route (DP-19). What this story fixes is the element list of the hold part of the route answer and the states the screen can show from this service's answer.

| Screen | States | What the route reads on this service |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | The hold action with the reason and the review date, the held state with both, the record's rule version, the refused and invalid states of the operation, and the lift back to the route decision |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The route itself, its merge order and its field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-010-01 | C2: the hold elements, the reason-code reference and the held-state answer of the route operation | Contract | The published schema and the recorded answers of case `RC-2026-000410` |
| TC-E4-010-02 | C4, C6: the decision-record element and the stopped chain | Contract | The decision-record element, a healthy stub and a stopped stub |
| TC-E4-010-03 | C5: the rights and the error envelope of the declared operation | Contract | One request per right, including a role without it; one request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-010-04 | C4: the principle-5 declaration, that no record is needed and no event is published for a refused hold | Contract | A refused command and an outbox declaration that must stay empty |
| TC-S1-E4010-CON-01 | C3: the placeholder and the gap of an unpublished operation name | Contract | The four consumed rows, each with and without a published name |
| TC-S1-E4010-CON-02 | C4: the review timer, the activities and the absent Schedule | Contract | The workflow table, a draft that declares a Schedule, and a draft that declares the timer |
| TC-S1-E4010-CON-03 | C1, C6: the compatibility check and the fakes | Contract | The previous tag, an additive draft, a breaking draft and a fake that answers more than its document |

The four legacy case IDs are the legacy test cases of RWB-E4-010 in their legacy order, mapped onto this contract deliverable: the hold and its elements (01), the failure of the decision log (02), the access path (03) and the principle-5 record failure (04). The three `TC-S1-E4010-CON-` cases are new and test the parts of the baseline no legacy case touches. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the baseline: the reason codes and the rule version are referenced with their identifier, list or version, and no hold interval, maximum hold or date bound is enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, dates and a rule version only, and every fixture is synthetic; the caller is an identifier.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table.
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case` element and no `rule_row` element is declared as this service's own.
- The wait is Temporal's: a baseline that declares a Schedule, a Quartz job or a polling row for the review date fails the review (BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Quartz row, no foreign schema and no event published by this baseline.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-010, disposition Split (rework); AC1 and AC2 are owned by RWB-S1-E4010-APP; this story carries no legacy criterion and fixes the surface that story and the harness touch | 1, 11, 12, 16 |
| Feature | FEAT-VAL-10 Hold the case and set a review date, module S1, epic E4, depends on FEAT-CWC-11 | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.10.2 steps and integration points; A2.10.3.1 VR-S1-010-1 and BR-S1-010; A2.10.3.2 field catalog; A2.10.3.3 roles; A2.10.4.4 no background event; SCR-13 | 2, 3, 8, 12, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.3 relationships; T4 no state machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 16 |
| Epics 3 to 8 specification v3 | FEAT-VAL-10 with its primary role, its systems and its prerequisite; the APIs sheet gives S1 the one route operation | 1, 12 |
| Logical data model | DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | 11 |
| Routing logic | The `REVIEW_DATE_REACHED` event code; the States sheet carries no route-decision set and no held state; no rule row fires the review date for the route decision | 3, 8, 12.6 |
| Patterns | DP-03, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2638 to -4; ASM-4343 to -7 | 1, 3, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The hold behaviour, the record writes, the timer's wake, the case-move answer and the screen behaviour: RWB-S1-E4010-APP.
- The two valuation operations and the appraisal intake: RWB-S1-E4002-CON and the appraisal stories of this service.
- The route recommendation, the COLLINS return, the payoff, the range and the approvals of FEAT-VAL-05 to FEAT-VAL-09: the sibling route stories of this service; the reconsideration of FEAT-VAL-11 is its own story.
- The case of record, its held state, its name, its timers, `assignment` and `task`, and FEAT-CWC-11: rwb-case (P3) (GAP-2638; ASM-4345, ASM-4347).
- The durable store of the hold reason and the review date, where a column is confirmed: the data owner of this service (GAP-2638).
- The reason code list, its identifiers and its values, and any bound on the review date: the reference-data owner (GAP-2640; ASM-4346, ASM-4348).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
