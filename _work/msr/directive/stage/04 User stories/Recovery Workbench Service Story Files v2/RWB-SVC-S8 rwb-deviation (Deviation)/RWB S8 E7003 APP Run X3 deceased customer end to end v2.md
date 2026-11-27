# RWB-S8-E7003-APP Run X3 deceased customer end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S8-E7003-APP-16) |
| Contract version | Not specified in the source documents (DOR-RWB-S8-E7003-APP-23); base path /api/recovery/deviation/v1 only |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S8-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S8-E7003-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E7-003 split out for rwb-deviation. The three legacy criteria this story owns are copied word for word with their origin tags; the X3 raise, the routing by rule, the contact stop, the heir and estate path and the claim approval run as the X3 branch of `DeviationWorkflow` on task queue `rwb-deviation`, read the customer facts on the rwb-source-data data product (DP-05), write the decision record locally before anything changes (DP-03), answer the two deviation operations on base `/api/recovery/deviation/v1` (DP-13) reached by SCR-06 and SCR-08 through the gateway-bff composite route (DP-19), and publish `rwb.deviation.DeviationRaised.v1` (EV-06) on `rwb.deviation.events.v1`, which is how rwb-comms stops contact and rwb-case pauses the stage clock. The consumed operation names are not published (GAP-3055; ASM-5154); the rule package, the outbox library and the workflow kit are absent from the plan's pattern rows (GAP-3055; ASM-5155); the contact stop is the comms subscription and not a call of this service (ASM-5156); R-DEV-06 is published for X6 and X7 while AC3 of the key pairs it with X3 (GAP-3055; ASM-5160). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E7003-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (36 resolved, 18 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **hardship and vulnerability specialist**, I want **to stop contact, notify heirs, file the insurance claim and settle the estate position**, so that **every deviation has a handler and a clock**.

This is the application slice of legacy RWB-E7-003 and the X3 branch of FEAT-DVF-03. It owns:

- the three legacy criteria AC2, AC3 and AC4 of the key, copied verbatim, and the rules, messages and screens they depend on;
- the raise of X3 on a case through `POST /cases/{caseId}/deviations` on `/api/recovery/deviation/v1`, its validation, its `Idempotency-Key` and its answer (DP-13);
- the routing of X3 by rule: R-DEV-03 to the specialist with Legal on the estate claim, and R-DEV-06 to the agent within policy with a person approving the insurance claim (AC2, AC3);
- the contact stop of X3, set on the deviation row and carried outward as `rwb.deviation.DeviationRaised.v1` (EV-06) for rwb-comms to act on;
- the stage-clock pause: this service raises the deviation and the case owner pauses the stage timer and keeps the prescription clock running, because the timers and the case stay with rwb-case;
- the heir and estate path: the notification to heirs through the comms templates and the insurance claim with its approval, each with a reference, in the order the rules give;
- the outcome through `PATCH /deviations/{deviationId}`: return to the paused state, re-route to the route decision, or close the case when the insurance clears the balance;
- the decision record of every one of those steps, written through RWB-PLT-E1027-CON in the caller's transaction before anything else changes, with the rule id and the version in force (DP-03);
- the states of SCR-06 Raise deviation and SCR-08 Deviation queue that this branch produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the two operations, the consumed rows, the event envelope, the workflow elements, the rights, the error set and the fakes, which are RWB-S8-E7003-CON; the cross-service journey of the key and its evidence, which is RWB-ITG-E7003-ITG and owns AC1; the case, its timers, its tasks and its assignments, which are rwb-case's (P3); the customer facts of `v_ace_customer`, which are rwb-source-data's (P1); the notice, letter and heir-notification templates and the contact-stop suppression, which are rwb-comms' (P6); the evidence documents, which are rwb-document's (P5); the rule rows, the package version, the approval and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

A death stops the ordinary recovery route. Letters and calls to a dead customer are a conduct breach, the estate clock runs whether the bank is ready or not, and an unclaimed insurance policy is money the estate and the bank both lose. FSD S8 keeps the feature as FEAT-DVF-03: stop contact, notify heirs, file the insurance claim and settle the estate position, with the result recorded with its rule version. The requirement it serves is REQ-DVH-008, a death stops all contact, notifies the heirs and the estate and starts the insurance claim path; REQ-S8-001 makes X3 run end to end with its own flow, approver, contact rules and return point.

Under D-RCV-60 the ownership of the facts this feature touches changes, and that is what the story carries.

- **the customer is ACE's, not this service's.** `v_ace_customer` is an ACE view and only rwb-source-data reads the `recovery.v_ace_*` views, so the deceased status and the identity reference arrive on the owner's data product and are never read as a table or a view here (DP-05; Architecture v5 slide 8).
- **the contact stop is an event, not a call.** `DeviationRaised` is published with the case, the code and the raised-by, and rwb-comms is the subscriber that suppresses letters and calls; this service sets the flag and sends nothing itself (ASM-5156).
- **the clock stays with the case.** The timers, their pause and the prescription clock are rwb-case's; this service says the deviation is open and the case owner pauses only the stage timer (R-DEV-01, Architecture v5 and the Temporal design slide 8).
- **the decision is recorded first.** AC4 is the rule that makes the branch trustworthy: when the record cannot be written nothing changes and the user sees MSG-P7-003. Under DP-03 the record is local and written in the same transaction as the step.
- **the events are the service's own two.** The ownership rows give S8 EV-06 and EV-07; this branch publishes EV-06 only, and EV-07 DeviationCleared belongs to the clearing story of the same key.

Every value here is data in force: the deviation codes of `LOV-DEVIATION`, the outcome codes of `LOV-DEV-OUTCOME`, the escalation at the deviation service level and the claim approval are read with their version, and no amount, limit or code is written in code.

### 3. Preconditions

- RWB-S8-E7003-CON is published: the two operations, the consumed rows, the event envelope, the workflow elements, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-06 and SCR-08 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The rwb-source-data data product that carries the customer of `v_ace_customer` and its deceased status is published with its fake and its freshness stamp. Its operation name is Not specified in the source documents (GAP-3055; ASM-5154), and the row is not in this story's contract-dependency list, which is None.
- The rwb-case case-state read, its timer state and its case events are available for their fakes; its operation and event names carry the placeholder (GAP-3055; ASM-5154).
- rwb-comms publishes the templates of the heir notification and the contact-stop suppression, and the rwb-decision approval row of an insurance claim is available for its fake; both carry the placeholder (GAP-3055; ASM-5154; ASM-5156).
- The service runs as its own login on schema `rwb_deviation`, holds the library objects `decision_record`, `idempotency_key`, `outbox` and `inbox`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_customer`, `rwb_case` or `document` is refused by the database and fails the boundary test (DP-01, DP-05).
- The rule rows of the DEV route set, 22 rules over 9 states, are read at the version in force, and the package and the outbox library are recorded as tracked absences rather than added to the metadata (GAP-3055; ASM-5155).
- No approval is needed to build against a Draft contract baseline and none is needed to start this story, which stays Draft (realignment v1) until the coordinator closes the stage (ASM-5161).

### 4. Flow

1. The specialist or the agent raises X3 through `POST /cases/{caseId}/deviations` on `/api/recovery/deviation/v1` with the code, the reason and the evidence identifiers; a screening confirmation of the same code follows the same path (API-S8-001; DP-13).
2. The operation resolves the case on the rwb-case row, reads the customer of the case on the rwb-source-data data product with its freshness stamp, and reads the rule id and version in force (DP-05).
3. If the data product is stale after a late or failed ACE batch, the raise holds, writes nothing and shows MSG-P1-001 with the data date (VR-S8-012-1).
4. `DeviationWorkflow` starts on task queue `rwb-deviation` in namespace `rwb-recovery` and the first activity records the deviation: the case, the code X3, the raised-by, the time, the paused state it was given, the handler and `contact_stop` true. The record is written before anything else changes (DP-03).
5. `DeviationRaised` (EV-06) reaches `rwb.deviation.events.v1` through the outbox in the same transaction; rwb-comms suppresses every outbound notice and call for the case, and rwb-case shows the case on hold and pauses the stage timer while the prescription timer keeps running (R-DEV-01; ASM-5156).
6. R-DEV-03 runs: X3 routes to the specialist, and Legal joins for the estate claim; the handler is written on the deviation and the task is raised by rwb-case, which owns assignments (AC2).
7. The specialist confirms the death and the path begins: heirs are notified through the comms templates, and the insurance claim is opened on the policy the customer record names. Where the case also qualifies under R-DEV-06, the agent handles within policy and a person approves the insurance claim before it is filed (AC3).
8. The claim, the heir notification and the documents that support them are recorded by reference on the deviation and in the decision record; the documents themselves stay with rwb-document (ASM-5159).
9. The outcome is taken through `PATCH /deviations/{deviationId}`: return to the paused state and resume the clock (R-DEV-18, `RETURNED`), re-route to the route decision against the estate (R-DEV-12, `RE_ROUTED`), or close the case when the insurance clears the balance (R-DEV-11, `CASE_ENDED`) (API-S8-002).
10. `DeviationCleared` (EV-07) is published by the clearing story of this key, not here; this branch ends with the outcome recorded and the case moved by the case owner (ASM-5155).
11. A deviation that stays in the owner's hands beyond the deviation service level escalates to the team manager and the breach is reported (R-DEV-20); the level is read from the rule row and is never a constant.
12. SCR-06 Raise deviation and SCR-08 Deviation queue show the raise, the handler, the contact stop and the outcome, read through the gateway-bff composite route, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, no event leaves and the answer is refused | MSG-P7-003 | AC4, TC-E7-003-04, TC-E7-003-06 |
| X2 | The role does not hold the Case record right of the operation | 403 before any read or write, and no record is written | MSG-P4-002 | AC5, TC-E7-003-05, TC-E7-003-07 |
| X3 | A required element of the request is absent or invalid, or the code is not in `LOV-DEVIATION` | Nothing is raised and the field is named | MSG-GEN-001 | AC6, TC-E7-003-08 |
| X4 | The case is unknown, out of scope, or closed | Nothing is raised and no case row is written | None (404) | AC7, TC-E7-003-09 |
| X5 | The ACE data product behind the customer is stale after a late or failed batch | The raise holds, writes nothing and shows the data date; it resumes on a fresh answer | MSG-P1-001 | AC8, TC-E7-003-10 |
| X6 | X3 is already open on the case | One deviation per code on a case: the second request is refused with the open deviation named | None (409) | AC9, TC-E7-003-11 |
| X7 | The outcome names no next step, or the code has no owner | The case returns to the route decision and the outcome is recorded as unmapped (R-DEV-22), or the case goes to the team manager (R-DEV-21) | None | AC10, TC-E7-003-03, TC-E7-003-12 |
| X8 | The claim approval is refused or is not taken before filing | Nothing is filed, the claim stays open and the decision records the refusal | None | AC11, TC-E7-003-03, TC-E7-003-13 |
| X9 | rwb-case, rwb-source-data or rwb-access does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 | None | AC12, TC-E7-003-02, TC-E7-003-14 |
| X10 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC13, TC-E7-003-15, s17, BR8, BR10 |

X1 to X3 are the paths of the legacy key carried onto the split, X4 to X9 are the paths the target call types add, and X10 is the DP-05 and DP-01 boundary. No percentage, limit or threshold is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S8-E7003-CON, the rwb-case, rwb-source-data, rwb-comms, rwb-decision and rwb-access fakes and the decision-record stub, on its own schema, and needs no live neighbour |
| Negotiable | The activity names, the decision codes and the shape of the step outcome are this story's choice; the operations, the rules, the messages, the screens and the event payload are fixed |
| Valuable | A death stops contact the same day and the estate path starts with a handler, a claim and a record, instead of letters going out to a dead customer |
| Estimable | One workflow branch, five activities, four clients, one table, one event, two operations and two screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic cases through the contract fakes, plus the stopped record write, the stale product, the duplicate code and the refused approval |

### 7. Acceptance criteria

```gherkin
Feature: Run X3 deceased customer end to end

  Scenario: AC2 Rule R-DEV-03 (legacy RWB-E7-003 AC2)
    Given a case in state DEV_FLAGGED
    When owner assigned
    Then assign to the specialist; Legal joins X3 for the estate claim
    Then the case moves to DEV_WITH_OWNER

  Scenario: AC3 Rule R-DEV-06 (legacy RWB-E7-003 AC3)
    Given a case in state DEV_FLAGGED
    When owner assigned
    Then agent handles within policy; a person approves an insurance claim
    Then the case moves to DEV_WITH_OWNER

  Scenario: AC4 Not recorded (legacy RWB-E7-003 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Role without the Case record right (X2) (new, D-RCV-60)
    Given a role without the Case record right of the operation
    When either deviation operation is called
    Then 403 with MSG-P4-002 before any read or write, and no record is written

  Scenario: AC6 Required element absent or invalid (X3) (new, D-RCV-60)
    Given a required element of the request is absent or invalid, or the code is not in LOV-DEVIATION
    When the raise is requested
    Then nothing is raised and the field is named with MSG-GEN-001

  Scenario: AC7 Case unknown, out of scope or closed (X4) (new, D-RCV-60)
    Given the case is unknown, out of scope, or closed
    When the raise is requested
    Then nothing is raised, no case row is written and the answer is 404

  Scenario: AC8 Stale ACE data product (X5) (new, D-RCV-60)
    Given the ACE data product behind the customer is stale after a late or failed batch
    When the raise is requested
    Then the raise holds, writes nothing and shows MSG-P1-001 with the data date, and it resumes on a fresh answer

  Scenario: AC9 X3 already open on the case (X6) (new, D-RCV-60)
    Given X3 is already open on the case
    When a second request is made
    Then it is refused with the open deviation named and the answer is 409

  Scenario: AC10 No next step or no owner (X7) (new, D-RCV-60)
    Given the outcome names no next step, or the code has no owner
    When the outcome is recorded
    Then the case returns to the route decision and the outcome is recorded as unmapped (R-DEV-22), or the case goes to the team manager (R-DEV-21)

  Scenario: AC11 Claim approval refused or not taken (X8) (new, D-RCV-60)
    Given the claim approval is refused or is not taken before filing
    When the claim is about to be filed
    Then nothing is filed, the claim stays open and the decision records the refusal

  Scenario: AC12 Dependency does not answer (X9) (new, D-RCV-60)
    Given rwb-case, rwb-source-data or rwb-access does not answer inside 2 s, or its breaker is open
    When the raise is requested
    Then the step waits and retries on the workflow's own schedule, nothing is written and the caller sees 503

  Scenario: AC13 Boundary reach (X10) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case row or another service's schema
    When the boundary test runs
    Then the grant refuses the statement, the boundary test fails the build and nothing is released

  Scenario: AC14 Business rules BR1 to BR10 (section 8) (new, D-RCV-60)
    Given the rules BR1 to BR10 of section 8
    When the build and the boundary tests run
    Then each rule holds, and a rule that is an architecture constraint is checked by the guardrail or boundary test that names it

  Scenario: AC15 Error answers of the provided operations (401, 403, 404) (new, D-RCV-60)
    Given a request to either deviation operation is unauthenticated, names an unknown case, or is not permitted to the role
    When the operation answers
    Then the answer is 401, 403 or 404 as the failure requires, the message is Not specified in the source documents (NEWAC-RWB-S8-E7003-APP-AC15) and no record is written

  Scenario: AC16 Duplicate delivery of a consumed event (R-UNI-40) (new, D-RCV-60)
    Given the same consumed event arrives twice with the same key
    When the second delivery is received
    Then it is ignored and the idempotency hit is recorded

  Scenario: AC17 Activity retry and timeout (new, D-RCV-60)
    Given an activity of DeviationWorkflow fails or exceeds its timeout
    When the activity is retried
    Then it retries on the workflow's own schedule, the retry and timeout values are Not specified in the source documents (NEWAC-RWB-S8-E7003-APP-AC17) and nothing is written until it succeeds

  Scenario: AC18 Consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed call to rwb-case, rwb-source-data or rwb-access fails
    When the step runs
    Then the step waits and retries on the workflow's own schedule, nothing is written and the caller sees 503

  Scenario: AC19 Disallowed status change refused (new, D-RCV-60)
    Given a status change the model does not allow
    When the change is requested
    Then it is refused, the message is Not specified in the source documents (NEWAC-RWB-S8-E7003-APP-AC19) and nothing changes
```

The three criteria are the legacy AC2, AC3 and AC4 of the key, word for word, with their origin tags added; only the AC4 wording is changed, from decision log to decision record (CG-ALL-11476), and the legacy wording of `the action is taken` and `agent handles within policy` stands. AC1 of the same key, "stops contact, notifies heirs, files the insurance claim and settles the estate position" with "the system writes the result to the decision log with the rule version", is owned by RWB-ITG-E7003-ITG, which carries the cross-service journey of the key and its evidence; the raise, the routing, the contact stop and the claim behind it are built here and are stated in sections 4, 8 and 16. The rule row R-DEV-06 in force names X6 and X7 rather than X3, and AC3 is still copied verbatim: the conflict is carried in the gap and settled by its owner (GAP-3055; ASM-5160). No criterion carries a business value: the codes, the outcome list and the service level are data in force.

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S8-012-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DEV-03 | Assign to the specialist; Legal joins X3 for the estate claim, when deviation_code in (X2,X3) | Moves to DEV_WITH_OWNER |
| R-DEV-06 | Agent handles within policy; a person approves an insurance claim, when deviation_code in (X6,X7) | Moves to DEV_WITH_OWNER |
| BR-S8-012 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-DEV-01 | Pause the stage clock, keep the prescription clock running, route to the named owner, when deviation_code in (X1..X7) | Moves to DEV_FLAGGED |
| R-DEV-20 | Escalate to the team manager and report the breach, when time in DEV_WITH_OWNER exceeds the deviation service level | DEV_WITH_OWNER |
| R-UNI-38 | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |

The VR, R-DEV-03, R-DEV-06 and BR rows are the rows of FSD S8 A2.12.3.1, copied character for character; R-DEV-01 and R-DEV-20 are the rows of the DEV route set that hold the branch, and the three universal rules are the Business Rules and Routing Logic v4 rows the step depends on.

| ID | Rule | Source |
|---|---|---|
| BR1 | The customer, the deceased status and the policy facts are ACE's and are read only on the rwb-source-data data product; this service holds no `v_ace_*` grant and keeps no copy | DP-05; Ownership Map rows of S8 |
| BR2 | Every code, outcome and service level is data in force with its version; no deviation code, outcome code, level or template is a constant of the build | BR-S8-012; TSD S8 T3.2 |
| BR3 | The contact stop is carried by EV-06 to rwb-comms, which suppresses the notices and calls; this service sends no notice and calls no comms operation | ASM-5156; Event and Messaging Design v5, EV-06 |
| BR4 | The case, its timers, its tasks and its assignments stay with rwb-case: the handler is written on the deviation, no `assignment`, `task` or `timer` row is written here, and only the stage timer is paused | Ownership Map (`recovery_case`, `assignment`, `timer` owner P3) |
| BR5 | The decision is recorded before anything changes, with the rule id and the version in force; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-39; legacy AC4 |
| BR6 | One deviation per code per case: a repeated request with the same `Idempotency-Key` and a second open X3 raise no second row and no second event | API-S8-001; R-UNI-40 |
| BR7 | One event of this branch: `DeviationRaised` (EV-06) with the case, the code and the raised-by, no personal data, through the outbox; `DeviationCleared` (EV-07) is the clearing story's | TSD S8 T5.3; Event and Messaging Design v5, EV-06 and EV-07 |
| BR8 | No foreign key leaves `rwb_deviation` and no statement reaches another schema: the case, the person, the document and the rule are identifiers of other owners' facts | DP-01; TSD S8 T3.3 |
| BR9 | The insurance claim is filed only after the approval the rule names is taken; a refused or absent approval files nothing and the claim stays open | Legacy AC3; R-DEV-06; FSD S8 A2.12.3.3 |
| BR10 | No person name, address, contact value or identity number enters `rwb_deviation`, the event, the decision record, a log or a workflow input; heirs are reached by the comms templates and not by data of this service | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case state is rwb-case's and is not changed by this story: the branch reports its outcome and the case owner applies it (BR4). What this story owns is the deviation state, and the states are the nine of the DEVIATION machine of TSD S8 T4.

| From (deviation) | Event | Condition | To |
|---|---|---|---|
| ANY_STATE | DEVIATION_FLAGGED | X3 is raised and validated | DEV_FLAGGED, with the row and EV-06 written (AC2) |
| DEV_FLAGGED | OWNER_ASSIGNED | R-DEV-03 routes to the specialist with Legal | DEV_WITH_OWNER |
| DEV_FLAGGED | OWNER_ASSIGNED | R-DEV-06 routes to the agent, with a person approving the claim | DEV_WITH_OWNER (AC3) |
| DEV_FLAGGED | OWNER_ASSIGNED | The code has no owner, or is not one of X1 to X7 | DEV_WITH_OWNER on the team manager, the unmapped code logged (R-DEV-21) |
| DEV_WITH_OWNER | INSURANCE_SETTLED | X3 and the insurance clears the balance | CASE_ENDED (R-DEV-11) |
| DEV_WITH_OWNER | ESTATE_CONFIRMED | X3 and the insurance does not clear | DEV_REROUTE (R-DEV-12) |
| DEV_WITH_OWNER | SLA_BREACHED | The deviation service level is exceeded | DEV_WITH_OWNER on the team manager (R-DEV-20) |
| DEV_WITH_OWNER | DEVIATION_RESOLVED | The outcome names no next step | DEV_REROUTE, the unmapped outcome recorded (R-DEV-22) |
| DEV_RESOLVED | CLOCK_RESUMED | The owner resumes the clock | RESUMED (R-DEV-18) |
| DEV_REROUTE | ROUTE_REOPENED | The case owner reopens the route decision | ROUTE_D6 (R-DEV-19) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The raise command of a case at any state | The workflow starts on `rwb-deviation` | Reading the case and the customer |
| Reading | The data product answers fresh | The code is valid and no X3 is open | Recording the deviation |
| Recording | The record and the outbox commit | The transaction succeeds | Routed, and waiting on the claim and the estate |
| Routed | The claim approval and the outcome of the case | The outcome is taken | Waiting on the next command |
| Any | The record write or the transaction fails | X1 | Waiting, nothing changed |

The nine states and the 22 rules of the DEV route set are the rows of TSD S8 T4 and of the Business Rules and Routing Logic v4; the branch uses seven of them and asserts none of the values they carry.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SPECIAL Hardship and vulnerability specialist | Case record RU in the legacy permission table of the key and TSD S8 T6.1: raise X3, take the outcome, read the deviation, the claim and the record |
| RW-LEGAL Legal counsel | Case record R: read the deviation, join the estate claim, read the record; takes no outcome |
| RW-CASEOWN Case owner | Case record CRU: raise, take the outcome and return or re-route the case, and own the stage timer's pause |
| RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-RESTRUCT | Case record U in the legacy permission table: raise X3 and read it; the outcome of their own codes is their stories' |
| RW-CONDUCT Conduct and QA officer | Case record R: read the branch for conduct review |
| RW-TEAMMGR Team manager | Case record R: receives the escalated deviation and the breach (R-DEV-20) |
| SY-CASEWF Case workflow module | Case record CRU: reads the deviation state and raises the task |
| SY-RULES Rules component, SY-AGENT Agent platform | Case record R: read the deviation and the record under the same checks as a person |
| rwb-deviation service identity | Runs the branch, reads the data product and the case, publishes EV-06, writes the decision record and answers the two operations; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S8 T6.1 and of the legacy permission table of the key, and nothing wider. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` (S8, `rwb_deviation`) | id, case_id, deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at, outcome | Write, the one table of this service |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code, prescription date | Not read as a table: the case state arrives on the rwb-case row |
| DF-WRK-009 to DF-WRK-016 | `assignment` (P3) | assignee_user_id, assigned_at, ended_at | Not written here: the handler is `deviation.handler_user_id` and the task is rwb-case's |
| DF-WRK-027 to DF-WRK-036 | `timer` (P3) | timer_type, started_at, expires_at, status | Not written here: the pause is signalled to the case owner |
| DF-ACE-055 to DF-ACE-074 | `v_ace_customer` (P1) | person_key, cif_no, customer_status, and the policy link | Read only, on the rwb-source-data data product (DP-05; ASM-5157) |
| DF-DOC-001 to DF-DOC-011 | `document` (P5) | id, case_id, document_type, storage_ref | Not read as a table: the evidence stays with rwb-document and arrives as the request's document identifiers (ASM-5158) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_deviation`) | rule id, rule version, inputs reference, outcome, decided at | Write, one record per step, before anything else changes |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule and its version arrive on the package read |

Field IDs are those of the Logical Data Model and Data Dictionary v9, of TSD S8 T3.1, T3.2 and T3.3 and of the legacy Data table, with the owners changed by the target. **No new table, no new column and no migration**: the schema `rwb_deviation` and its login arrive with the DB story of this service, and the decision record, `idempotency_key`, `outbox` and `inbox` are library objects created in it by the libraries' migrations (DP-03). The claim reference and the heir notification reference are held in `deviation.outcome` and in the decision record; no source names a column for either, so none is added (GAP-3055; ASM-5159).

**No personal data.** The rows this story reads and writes carry identifiers, codes, dates and a rule version. No heir name, address, contact value or identity number enters `rwb_deviation`, the event, the decision record, a log or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). These are the two operations the legacy story names, and their shape is baselined by RWB-S8-E7003-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/deviations` | `DeviationRequest` in (`deviationCode`, `reason`, `documentIds`), `Deviation` out (API-S8-001) | Case record, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat and no second row or event is raised |
| PATCH | `/deviations/{deviationId}` | `DeviationOutcome` in (`outcome`, `note`), `Deviation` out (API-S8-002) | Case record, right U, scope applied | Not applicable; the state guards a repeat |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 for a second open X3, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed row does not answer, in one problem document.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The customer and deceased-status read (operation name Not specified in the source documents (GAP-3055; ASM-5154)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The customer of the case, the deceased status and the policy link, with the freshness stamp; faked |
| `GET /cases/{caseId}` family and the timer read (operation names Not specified in the source documents (GAP-3055; ASM-5154)) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the paused state it is in, the stage timer and the prescription date; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-3055; ASM-5154)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEV rule rows and the version in force, and the approval of an insurance claim; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-3055 with ASM-5154. The connection matrix shows no REST edge from S8 to P7, so the rule-package row and the claim approval carry the placeholder and are settled by their owner (ASM-5155).

#### 12.3 Events published

| Event | Topic | Payload (no personal data) | Consumers |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | caseId, deviationCode, raisedBy | rwb-comms (contact stop) and rwb-case (clock pause and banner) |

One event, written through the outbox in the transaction of the record, in the CloudEvents envelope, keyed by the case. `rwb.deviation.DeviationCleared.v1` (EV-07) is not published here: it belongs to the clearing story of this key (BR7).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| The case event that opens or resumes a stage (name Not specified in the source documents (GAP-3055; ASM-5154)) | the topic of rwb-case | P3 rwb-case | Starts the deviation branch when a case of this service's scope changes stage; faked |

One subscription. The raise and the outcome are commands of this service and not events, and a duplicate is caught by the idempotency row and not by a subscription (R-UNI-40).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per deviation, continues-as-new | `rwb-deviation` | Input: the case, the deviation, the code, the paused state and the rule package in force; signals: the approval result and the outcome command |
| `raiseDeviation` | Activity | `rwb-deviation` | The case, the code, the raised-by and the evidence identifiers in; the deviation, the decision record, the outbox row and the step outcome out, in one transaction |
| `routeToOwner` | Activity | `rwb-deviation` | The code and the rule rows in force in; the handler, the team and the flags for Legal and for the approval out |
| `applyContactStop` | Activity | `rwb-deviation` | The case and the code in; `contact_stop` set on the deviation and the event element out |
| `openEstatePath` | Activity | `rwb-deviation` | The case, the policy link and the heir path in; the claim reference and the notification reference out |
| `recordOutcome` | Activity | `rwb-deviation` | The outcome, the note and the rule version in; the deviation, the case move and the decision record out, in one transaction |

`DeviationWorkflow` is the one workflow the ownership rows give S8, and the five activities are this branch's. The approval the FSD names for a deviation is a step inside `DeviationWorkflow`, taken by the role the FSD code assigns; the decision-record library writes the entry and its hash. No P7 ApprovalWorkflow edge is drawn here; that edge stays an open question for the solution architect. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable. The stage timer's pause is applied by rwb-case on the EV-06 subscription and not by this service (BR4). Workflow ID form: Not specified in the source documents (CG-ALL-11467). Start rule (catalog): An agent or officer flags it (EV-06 starts screening), or universal rules R-UNI-04 to 09 fire. Duplicate-start policy: Not specified in the source documents (CG-ALL-11467).

#### 12.6 Schedules

None. The ownership rows give S8 no job, so this story declares no Temporal Schedule and no legacy Quartz job. The escalation of R-DEV-20 is a durable timer inside `DeviationWorkflow` and not a Schedule, and its level is read from the rule row.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `deviation` | S8, in `rwb_deviation` | The one table of the Ownership Map rows of S8; the code, the raise, the paused state, the handler, the contact stop, the clearing and the outcome |
| Decision record | PLT library, created in `rwb_deviation` | The local hash-linked decision record, one per step (DP-03) |
| `idempotency_key` | PLT library, created in `rwb_deviation` | The key of the repeated command and the answer it holds |
| `outbox`, `inbox` | PLT library, created in `rwb_deviation` | The one publication of this branch and the one subscription (DP-09 capability, tracked and not added to the metadata: ASM-5155) |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `document` and `document_custody` (P5), `template` (P6), every `v_ace_*` view and `v_ace_customer` (P1). No foreign key leaves `rwb_deviation`: the case, the person, the document and the rule are identifiers, not keys across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data customer fake | Case `RW-2026-000502` with a customer marked deceased, its policy link and a fresh stamp; the same case with a stale product and its date; no answer beyond 2 s | AC2, X5, X9 |
| rwb-case case and timer fake | The case at `WITH_FCR_OFFICER` with a running stage timer and a prescription date; a case at another state; no answer beyond 2 s | AC2, AC3, X4 |
| rwb-decision rule and approval fake | The DEV rows of R-DEV-03, R-DEV-06 and R-DEV-20 at their version in force; the claim approved, refused and not taken | AC3, X7, X8 |
| rwb-access authorise fake | Case record, right U accepted and refused | TC-E7-003-05, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| Outbox and inbox stub | The outbox row committed with the record, and a rollback that leaves neither | BR7, X1 |
| gateway-bff composite route fake | The merged SCR-06 and SCR-08 answers for `RW-2026-000502`, with the deviation, the handler and the contact stop read once | AC2, TC-E7-003-01 |
| rwb-comms template fake | The heir notification template rendered from identifiers only, with no personal data of this service | AC3, X8 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-3055; ASM-5154).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` on `/api/recovery/deviation/v1`; the rwb-source-data customer row, the rwb-case rows, the rwb-access row and the rwb-decision row; one hop, 2 s |
| Kafka | 1 published, 1 consumed | `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1` through the outbox; the rwb-case stage event through the inbox; the shared `rwb.decision-record.v1` is the library's publication |
| Temporal | 1 workflow and 5 activities | `DeviationWorkflow`, `raiseDeviation`, `routeToOwner`, `applyContactStop`, `openEstatePath` and `recordOutcome` on `rwb-deviation`; no Schedule |
| File | None of this service | The claim and the heir notification travel as templates and references of rwb-comms and rwb-document, and this service writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.deviation`, module `x3deceased`; front end `src/modules/recovery/deviation/RaiseDeviation.tsx` and `DeviationQueue.tsx`, the fragments SCR-06 and SCR-08 embed.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the customer and the deceased status are the ones the rwb-source-data contract answers. DP-03 is the transaction rule of the branch: the record, the outbox row and the deviation commit together or not at all. DP-13 moves the base of the two operations off the monolith. DP-19 is how SCR-06 and SCR-08 reach this service, one hop through the gateway.

DP-04, DP-09 and DP-10 are not in the plan's pattern set for this key although the branch evaluates the DEV route set, publishes EV-06 and runs a workflow: the rule rows are read as data at their version, the outbox and inbox library and the workflow kit are recorded as tracked absences, and no metadata row is invented (GAP-3055; ASM-5155).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationWorkflow` X3 branch | Workflow | Receives the raise, routes, stops contact, opens the estate path, waits on the approval and the outcome, reports the result |
| `raiseDeviation` | Activity | Writes the deviation, the record and the outbox row in one transaction and returns the step outcome |
| `routeToOwner` | Activity | Applies R-DEV-03 and R-DEV-06 and returns the handler, Legal and the approval flag |
| `applyContactStop` | Activity | Sets `contact_stop` and assembles the EV-06 element |
| `openEstatePath` | Activity | Opens the heir path and the claim on the policy link and holds the filing until the approval |
| `recordOutcome` | Activity | Writes the outcome, the record and the case move |
| `SourceDataClient` | Client | The customer and policy read of rwb-source-data, one hop, 2 s, breaker, with the stale path |
| `CaseStateClient` | Client | The case state, paused state, stage timer and prescription date of rwb-case, one hop, 2 s |
| `AccessClient` | Client | The authorise row of rwb-access, one hop, 2 s |
| `RuleAndApprovalClient` | Client | The DEV rows in force and the claim approval of rwb-decision, one hop, 2 s |
| `DeviationDecisionRecordWriter` | Library adapter | Writes one record per step before anything else changes and refuses the step when the write fails (DP-03) |
| `DeviationController` | Controller | The two operations, their capability area and right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RaiseDeviation`, `DeviationQueue` | React components | Show the raise, the handler, the contact stop and the outcome on SCR-06 and SCR-08, read only; empty, loading, error and no access states are Not specified in the source documents (CG-ALL-11477, CG-ALL-11478) |

**Database and migrations.** No Flyway file. `rwb_deviation` and its login arrive with the DB story of this service, `deviation` is created there from TSD S8 T3.1, and the decision record, the idempotency key and the outbox and inbox are library objects created by the libraries' migrations (DP-03).

**Other schemas.** `rwb_case`, `rwb_decision` and `rwb_document` are owned by other services; this service reads their contracts and writes to none of them.

**Configuration and reference data.**

- `LOV-DEVIATION` (X1 to X7), `LOV-RAISED-BY` (SCREENING_AGENT, RULE, OFFICER, CUSTOMER_CONTACT) and `LOV-DEV-OUTCOME` (RETURNED, RE_ROUTED, CASE_ENDED) at their version in force (TSD S8 T3.2), read as reference data.
- The DEV rule rows of R-DEV-01 to R-DEV-22, with the deviation service level, read at their version and never as constants.
- The capability area Case record and its rights are access rows of rwb-access, read through the guard.
- The heir notification template is a comms row and the claim pack a document row; both are referenced by identifier only.
- No parameter of the escalation level, the claim approval or the notification timing is named with a value in the sources, so each is read with its version. Parameter keys: Not specified in the source documents (DOR-RWB-S8-E7003-APP-20). Reference-data contract: DP-06 and DP-07.

**Build steps**

1. The X3 branch of `DeviationWorkflow` and its input record, registered on `rwb-deviation`.
2. `DeviationController` with the two operations, the right, the `Idempotency-Key` and the problem mapping (TC-E7-003-05).
3. `SourceDataClient`, `CaseStateClient` and `AccessClient` against their fakes, with the 2 s budget, the breaker and the stale path (X5, X9).
4. `RuleAndApprovalClient` and `routeToOwner`, with R-DEV-03, R-DEV-06, the unmapped code and the service-level escalation (AC2, AC3, X7).
5. `raiseDeviation` and `DeviationDecisionRecordWriter`, with the record, the outbox row and the failed-write path (AC4, X1).
6. `applyContactStop` and the EV-06 element, with the outbox rollback path (BR7).
7. `openEstatePath` and the claim approval, with the refused and not-taken paths (X8).
8. `recordOutcome` with the three outcome codes and the case move (TC-E7-003-03).
9. `RaiseDeviation` and `DeviationQueue` through the composite route fake (TC-E7-003-01).
10. The boundary test: no statement outside `rwb_deviation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_document`, and no second published event (X10, BR8, BR10).

**Feature flag.** `rwb.deviation.x3-deceased-v1`, read as a flag of the platform library; off means the raise is recorded with its outcome and the estate path is not opened, and the case owner keeps the case on hold.

**Done when.** The tests of section 16 pass, a confirmed death raises X3 once and publishes one EV-06 in SIT, contact stops for the case, the specialist and Legal are named, a refused approval files no claim, a forced record failure changes nothing and shows MSG-P7-003, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-06 and SCR-08 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | X3 is raised and the case is with its handler | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required element of the request is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the Case record right calls either operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the step changes anything (X1, AC4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the customer is stale after a late or failed batch (X5) | {product} is from {date}. Today's load has not arrived. |

The five message IDs are the rows of FSD S8 A2.12.3.1, of the legacy message set of this key and of the platform set, and the text is the legacy wording, copied unchanged except MSG-P1-001, which takes the Error and Message Standard v4 text; no message is reworded and no new one is added. The on-hold banner of the case record is MSG-P3-004 and is rwb-case's.

### 15. Screens and states

SCR-06 Raise deviation and SCR-08 Deviation queue are served through the gateway-bff composite route (DP-19), and this story fixes the X3 part of their answer and the states it can show.

| Screen | States (sources) | What this story sets |
|---|---|---|
| SCR-06 Raise deviation | Form; saved; empty, loading, error and no access: Not specified in the source documents (CG-ALL-11477) | Form with the code, the reason and the evidence identifiers, the customer and the deceased status read once; saved with MSG-S8-001 and the handler named; refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001, already open with the X3 named |
| SCR-08 Deviation queue | Loading; list; empty, error and no access: Not specified in the source documents (CG-ALL-11478) | Loading while the branch reads the case and the product; list of open deviations by code, handler and age, with the X3 row, the contact stop and the claim state |

The screens' layout, their merge order and their field list belong to RWB-PLT-N001-CON; the X3 element list and the five service states above are this story's. The harness, fixture, answer shapes, heir-notification content, evidence format and gate are Not specified in the source documents (GAP-0468) and are agreed at the wave entry check.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-003-01 | The X3 journey of the key: the raise, the routing, the contact stop and the estate path, evidenced end to end by RWB-ITG-E7003-ITG; here the raise-and-route slice is exercised | Component | Case `RW-2026-000502`, deviation X3 raised 2026-12-10, paused state `WITH_FCR_OFFICER`, contact stop true |
| TC-E7-003-02 | AC2: rule R-DEV-03, the specialist and Legal, and the move to DEV_WITH_OWNER | Component | Case in DEV_FLAGGED with X3, the DEV rows at their version in force |
| TC-E7-003-03 | AC3: rule R-DEV-06, the agent within policy and the person approving the insurance claim | Component | Case in DEV_FLAGGED, the claim approved, refused and not taken |
| TC-E7-003-04 | AC4: the decision record cannot be written | Component | The decision-record stub stopped; nothing written, no event, and MSG-P7-003 shown |
| TC-E7-003-05 | Access: a role without the right | Component | A role without Case record U; 403 with MSG-P4-002 and no read |
| TC-E7-003-07 | AC5: role without the Case record right, 403 and no read or write | Component | A role without Case record U; MSG-P4-002 expected |
| TC-E7-003-08 | AC6: required element absent or invalid, nothing raised and the field named | Component | Request with an absent field and a code not in LOV-DEVIATION |
| TC-E7-003-09 | AC7: case unknown, out of scope or closed, 404 and no case row | Component | Case unknown, out of scope and closed in turn |
| TC-E7-003-10 | AC8: stale ACE data product, raise holds and MSG-P1-001 shows the data date | Component | Data product stale after a late or failed batch |
| TC-E7-003-11 | AC9: X3 already open, second request refused with 409 | Component | Case with X3 open; second request |
| TC-E7-003-12 | AC10: no next step or no owner, route decision or team manager | Component | Outcome with no next step; code with no owner |
| TC-E7-003-13 | AC11: claim approval refused or not taken, nothing filed | Component | Claim approval refused, then not taken |
| TC-E7-003-14 | AC12: rwb-case, rwb-source-data or rwb-access silent past 2 s, 503 and nothing written | Component | Dependency stub silent or breaker open |
| TC-E7-003-15 | AC13: statement on a v_ace_* view, recovery_case or another schema refused, build fails | Component | Boundary test statement against v_ace_* view and recovery_case |
| TC-E7-003-06 | Principle 5: a forced decision log write failure | NFR | A forced failure at the moment of the raise and of the outcome; no row, no event and no answer |
| TC-S8-E7003-APP-01 | The boundary: no `v_ace_*` read, no foreign schema write, one published event only | Component | The build scan of step 10, plus an outbox that holds EV-06 only |
| TC-S8-E7003-APP-02 | Contract: the two deviation operations, the events and the five activities of §12 against their contracts | Contract | Stubs of the two operations and the activities of §12.5 |
| TC-S8-E7003-APP-03 | Boundary of the tables of §12.7 (ASM-3438): only the owned rows and no foreign key leaves `rwb_deviation` | Component | The schema of `rwb_deviation` after migration and the tables of §12.7 |
| TC-E7-003-16 | AC14: business rules BR1 to BR10 hold, architecture constraints checked by the named guardrail or boundary test | Component | Not specified in the source documents (NEWAC-RWB-S8-E7003-APP-AC14) |
| TC-E7-003-17 | AC15: error answers 401, 403, 404 of the provided operations, no record written | Component | Not specified in the source documents (NEWAC-RWB-S8-E7003-APP-AC15) |
| TC-E7-003-18 | AC16: duplicate delivery of a consumed event ignored and the idempotency hit recorded | Component | Not specified in the source documents (NEWAC-RWB-S8-E7003-APP-AC16) |
| TC-E7-003-19 | AC17: activity retried and timed out on the workflow's own schedule, nothing written until success | Component | Not specified in the source documents (NEWAC-RWB-S8-E7003-APP-AC17) |
| TC-E7-003-20 | AC18: consumed call fails or does not answer, 503 and nothing written | Component | Not specified in the source documents (NEWAC-RWB-S8-E7003-APP-AC18) |
| TC-E7-003-21 | AC19: a status change the model does not allow is refused | Component | Not specified in the source documents (NEWAC-RWB-S8-E7003-APP-AC19) |

The six legacy case IDs are the legacy cases of RWB-E7-003 in their legacy order, with the Level column added. TC-E7-003-01 is Component here because the slice is tested on its fakes, and its `-ITG` copy belongs to RWB-ITG-E7003-ITG. The full text of each case, with its Given, When and Then, is in the Test Cases workbook.

### 17. Guardrails

- No business value in code: the deviation codes, the outcome codes, the raised-by list, the service level and the notification timing stay reference data or a rule row read with their version, never a constant or a default.
- No personal data in `rwb_deviation`, in EV-06, in a workflow input or in a log: identifiers, codes, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case and its clocks stay with rwb-case, the notices with rwb-comms and the evidence with rwb-document: no `recovery_case`, `assignment`, `task` or `timer` row, no template and no document is written here (BR3, BR4).
- The decision is recorded before the change and the raise is idempotent; a build that writes a row or publishes EV-06 before its record fails the review (DP-03, BR5, BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no data-lake copy and no `v_ace_*` read.

### 18. Traceability

| Source | Reference | Used in | Feature | L3 process |
|---|---|---|---|---|
| Legacy story | RWB-E7-003, disposition Split (rework); AC2, AC3 and AC4 owned word for word by this story; AC1 is owned by RWB-ITG-E7003-ITG | 1, 7, 16 | FEAT-DVF-03 | Not specified in the source documents (DOR-RWB-S8-E7003-APP-2) |
| Feature | FEAT-DVF-03 Run X3 deceased customer end to end, module S8, epic E7, depends on FEAT-DVH-04 | 1, 2, 3 | FEAT-DVF-03 | Not specified in the source documents (DOR-RWB-S8-E7003-APP-2) |
| FSD S8 v3 | A1.4 preconditions; A2.12.2 steps and integration points; A2.12.3.1 VR-S8-012-1, R-DEV-03, R-DEV-06 and BR-S8-012; A2.12.3.3 roles; A2.12.4.3 exception flows; requirements REQ-DVH-008 and REQ-S8-001; SCR-06 and SCR-08 | 2, 3, 4, 5, 8, 14, 15 | FEAT-DVF-03 | Not specified in the source documents (DOR-RWB-S8-E7003-APP-2) |
| TSD S8 v2 | T2 components; T3.0 standard columns; T3.1 `deviation`; T3.2 the three lists of values; T3.3 relationships; T4 the DEVIATION machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S8-001 and API-S8-002 | 3, 9, 10, 11, 12, 13, 16 | FEAT-DVF-03 | Not specified in the source documents (DOR-RWB-S8-E7003-APP-2) |
| Logical data model | DF-CAS-036 to DF-CAS-045, DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016, DF-WRK-027 to DF-WRK-036, DF-ACE-055 to DF-ACE-074, DF-DOC-001 to DF-DOC-011, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | 11 | FEAT-DVF-03 | Not specified in the source documents (DOR-RWB-S8-E7003-APP-2) |
| Routing logic | R-DEV-01, R-DEV-03, R-DEV-06, R-DEV-11, R-DEV-12, R-DEV-18, R-DEV-19, R-DEV-20, R-DEV-21, R-DEV-22; R-UNI-38, R-UNI-39 and R-UNI-40 | 4, 8, 9, 14 | FEAT-DVF-03 | Not specified in the source documents (DOR-RWB-S8-E7003-APP-2) |
| Events and patterns | EV-06 DeviationRaised and EV-07 DeviationCleared; DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5); no Schedule, because S8 owns no job | 12, 13 | FEAT-DVF-03 | Not specified in the source documents (DOR-RWB-S8-E7003-APP-2) |
| Gaps and assumptions | GAP-3055 for this story; ASM-5154, -2, -3, -6, -7 and -8; the contract gaps GAP-3056 belong to RWB-S8-E7003-CON and are cited here where the surface is read | 1, 3, 4, 11, 12, 13, 14, 16 | FEAT-DVF-03 | Not specified in the source documents (DOR-RWB-S8-E7003-APP-2) |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all | FEAT-DVF-03 | Not specified in the source documents (DOR-RWB-S8-E7003-APP-2) |

### 19. Out of scope

- AC1 of the legacy key and the cross-service journey that evidences it: RWB-ITG-E7003-ITG.
- The published shape of the two operations, the consumed rows, the event envelope, the workflow elements, the error set and the fakes: RWB-S8-E7003-CON.
- The raise of X1, X2, X4 to X7, the clear and resume, the two-deviation case, the override review, the complaint matching and the contact-breach path: the sibling stories of rwb-deviation.
- The case of record, its states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`, and the pause of the stage timer: rwb-case (P3).
- The ACE customer and policy facts and the freshness of the data product: rwb-source-data (P1).
- The notice templates, the heir notification and the contact-stop suppression: rwb-comms (P6).
- The claim pack and the evidence documents: rwb-document (P5).
- The rule rows, the package, the approval of the insurance claim and the central ledger: rwb-decision (P7). The parameter values of the service level: GAP-3055.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-06 and SCR-08: RWB-PLT-N001-CON and the edge stories.
- The deployment of this branch, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
