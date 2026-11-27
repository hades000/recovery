# RWB-ITG-E2013-ITG Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-013 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E2013-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 22 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2013-ITG |
| Size | Sized by the squad at refinement; fits within two weeks |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P3-E1028-APP, RWB-P3-E2013-APP, RWB-P4-E1038-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP, RWB-P7-E2013-APP |
| Contract dependencies | RWB-ITG-E2013-CON |
| Contract version | v1 (path prefix /v1) |
| Integration dependencies | RWB-P4-E1038-APP, RWB-P3-E1028-APP, RWB-P7-E2013-APP, RWB-P3-E2013-APP, RWB-P4-E2013-APP, RWB-P6-E2013-APP |
| External dependencies | None |
| Open decisions | DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL18 (ASM-2569, ASM-2839, ASM-2859, ASM-2883); DL22 (ASM-1162, ASM-1304, ASM-2217, ASM-2569) |
| Harness values | Composite route and merge order, harness environment and seeding, evidence format, retention and pass/fail gate are held as data in the harness pack and agreed at the wave 2 entry check; none are stated in this story |
| DoA outcome values | COVERED, NO_HOLDER, NOT_COVERED, NO_AMOUNT_LIMIT, RELATED_PARTY; a refused authority decision carries requiredLevel; request and response field set frozen at contract review |
| Events published | None by this story. The owning services publish EV-09 ApprovalRequested and EV-08 DecisionRecorded; rwb.decision.ApprovalDecided.v1, consumed in section 12.4, has no event catalogue row |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010, REQ-APD-011) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service harness that routes an approval by the delegation of authority table, decides it, escalates it and holds it through gateway-bff and the owning services**, so that **the wave 2 approval journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production endpoint, table, workflow, schedule or screen. The real behaviour is owned by the I stories RWB-P4-E1038-APP (the delegation of authority table as versioned reference data), RWB-P3-E1028-APP (service levels, timers and escalation), RWB-P7-E2013-APP (the router, the approval workflow and the decision records), RWB-P3-E2013-APP (the case status, the approval task and the timer), RWB-P4-E2013-APP (the authorise answer) and RWB-P6-E2013-APP (the escalation notification), and those six stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-013 journey crosses more than one service: rwb-decision holds the approval, the router and the decision records, rwb-access holds the delegation of authority table and answers the authorise check, rwb-case holds the case status, the approval task and the service level timer, and rwb-comms tells the new approver when an item escalates. Approval and authority governance is an audit finding: approvals today are given by e-mail, sometimes above the approver's limit or by the person who prepared the decision. Until the real services are exercised together through the gateway, the program cannot show that every approval follows the versioned delegation table, that nobody approves their own decision, and that no item waits unseen.

The harness gives one repeatable run per business date that proves the item is routed to the level whose row covers it or to the role named for a decision with no amount limit, that an approval inside the limit is written with its approver, level and limit version, that a breach of the service level or a level with no holder moves the item without moving the case, and that a failure in one service is isolated. It meets REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010 and REQ-APD-011 at the integration level and leaves every business rule and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The six I stories are published and deployed in the SIT environment: RWB-P4-E1038-APP (delegation version and the lookup), RWB-P3-E1028-APP (service level timers and the timer breach), RWB-P7-E2013-APP (approval routing, approve, refuse, return and the decision log), RWB-P3-E2013-APP (case status, approval task and timer), RWB-P4-E2013-APP (authorise) and RWB-P6-E2013-APP (escalation notification).
- gateway-bff is deployed with the composite route of DP-19 available. The gateway-bff composite approval-queue route path and its merge order: Not specified in the source documents (GAP-0397; ASM-0572).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before the I stories land.
- Delegation version DOA-2026.11 with holders U-9201 at L6, U-9202 at L5, U-9203 at L4 and the L3 committee recording holder U-9204, the route parameters rwb.approval.route.D7.1.area=LITIGATION, rwb.approval.route.D7.1.role=RW-LITOFF, rwb.approval.route.D7.1.escalation-role=RW-HEADLIT and rwb.approval.route.D7.1.service-level=1 working day, the capability areas per decision code and the service levels are loaded by the owning stories.
- The harness environment, its seeding of the delegation versions, holders and service level clocks, and its evidence format and retention: Not specified in the source documents (GAP-0397; ASM-0572).

### 4. Flow

1. Harness: seeds delegation version DOA-2026.11 and the L3 committee recording holder through the rwb-access contract, and the two approvals (the D7.1 demand notice and the D6.4 settlement "A-1") through the rwb-decision contract or the published fakes.
2. Harness: reads GET /approvals for the holder and asserts the decision, the amount, the level, the limit version and the age of each item.
3. Harness: approves inside the limit with one Idempotency-Key and asserts one decision record with the approver, the approval level, the limit version, the rule ID and version and final_call APPROVED, the approval status APPROVED, the case leaving Waiting approval, the P3 approval task completed and the service level timer closed.
4. Harness: drives a service level breach and asserts that the item moves one level up, or to the escalation role for a role-routed item, with MSG-P7-011 and the case still Waiting approval.
5. Harness: drives each refusal and hold of §5 — the preparer, a change above the limit, the missing reason, the override without a coded reason, the level with no holder, the committee level without a resolution reference, two approvers at once, a product with no covering limit and the decision-log failure — and asserts the status, the message and that nothing moved.
6. Harness: asserts that the DoA answer comes from POST /authorise and from the limit version on the approval, and that no service reads another service's schema.
7. Harness: writes one run report per business date, keyed by story and business date; the report format, the pass/fail gate and the retention are Not specified in the source documents (GAP-0397; ASM-0572).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | The service level passes with no action | The item moves to the next level up, or to the escalation role; the case does not move; one escalation entry is written and the new approver is told | MSG-P7-011 | TC-E2-013-02-ITG | AC3 |
| X2 | The caller prepared the decision | 409; the approval stays WAITING and no decision record is written | MSG-P7-002 | TC-E2-013-06-ITG | AC4 |
| X3 | A change raises the amount above the caller's level | Not approved; the item is rerouted to the level that covers it, with the changed terms and status WAITING, and no approval at the old level is recorded | MSG-P7-001 | TC-E2-013-07-ITG | AC4 |
| X4 | Refuse or return without a reason | 422 for the missing field; the approval keeps its status | MSG-GEN-001 | TC-E2-013-08-ITG | AC8, run by RWB-P7-E2013-APP |
| X5 | A change departs from the recommendation without a coded reason | 422; the recommendation and the terms are unchanged | MSG-P7-005 | TC-E2-013-10-ITG | AC10, run by RWB-P7-E2013-APP |
| X6 | The required level has no holder and no substitute | The item moves one level up at once and the routing entry records reason NO_HOLDER; the case does not move | MSG-P7-011 | TC-E2-013-11-ITG | AC3 |
| X7 | A committee level is approved without a resolution reference or the members present | 422 for the missing field; the entry is written only when both are given | MSG-GEN-001 | TC-E2-013-12-ITG | AC12, run by RWB-P7-E2013-APP |
| X8 | Two approvers act on one item at once | One call succeeds and writes one entry; the other returns 409 and writes nothing | MSG-GEN-004 | TC-E2-013-13-ITG | AC13, run by RWB-P7-E2013-APP |
| X9 | No delegation row covers the decision and product | The approval is stored with status HELD_NO_LIMIT, the case stays Waiting approval and the incident is raised | MSG-P7-010 | TC-E2-013-14-ITG | AC4 |
| X10 | The user holds no A letter in the decision's capability area, or is not the holder, substitute or route role | 403 on a direct call; the composite queue route hides the action | MSG-P4-002 | TC-E2-013-15-ITG | None in section 7 |
| X11 | The decision record cannot be written on an approval | 503; nothing moves — no approval status change, no case status change and no decision record | MSG-P7-003 | TC-E2-013-16-ITG | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the six I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the seeding and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The approval journey is evidenced across services rather than per service, and the delegation table is exercised as data |
| Estimable | One harness project, one journey specification, one fake pack and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Approval routing with the delegation of authority table - wave 2 integration harness

  Background:
    Given the environment is SIT
    Given delegation version "DOA-2026.11" is in force with holder "U-9201" at L6, "U-9202" at L5, "U-9203" at L4 and recording holder "U-9204" at L3 committee for MORTGAGE, all holding RW-PRODHEAD
    Given test user "U-9210" holds RW-RESTRUCT, test users "U-9211" and "U-9212" hold RW-LITOFF and test user "U-9213" holds RW-HEADLIT
    Given a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211"
    Given a settlement on case "RW-2026-000124" at decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent and loss amount 480,000.00, prepared by "U-9210"
    And the contract fakes of the section 12.8 pack are published

  Scenario: AC1 Routed by the delegation table through the owning services (new, D-RCV-60)
    Given the harness seeds the delegation version and the cases that raise the two approvals through the owning contracts
    When the router runs for decision D7.1 at 09:00 on 14 December 2026 and for decision D6.4 on the settlement
    Then an approval is queued for role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026
    And approval "A-1" is assigned to L6 holder "U-9201" with the delegation row and limit version "DOA-2026.11"
    And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6", limit version "DOA-2026.11" and its age
    And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role"
    And case "RW-2026-000124" is in status "Waiting approval"
    And the D7.1 item is never offered to "U-9211", who prepared it

  Scenario: AC2 Approve inside the limit writes the record and moves the case (new, D-RCV-60)
    Given approval "A-1" of AC1 is WAITING with L6 holder "U-9201" at the default service level of 3 working days
    When "U-9201" approves it with Idempotency-Key "k-501"
    Then exactly one decision record exists with approver "U-9201", approval level "L6", limit version "DOA-2026.11", the rule ID and version and final_call "APPROVED"
    And the approval status is "APPROVED" and it keeps level "L6" and limit version "DOA-2026.11"
    And case "RW-2026-000124" leaves "Waiting approval" for "In progress"
    And the P3 approval task is completed and the service level timer is closed
    And the response shows MSG-P7-004 with state "In progress"

  Scenario: AC3 Escalation on breach and the no-holder path move the item, not the case (new, D-RCV-60)
    Given the D7.1 approval of AC1 is still WAITING at 09:00 on 15 December 2026
    And the L6 row for SSME has no holder and no substitute
    When rwb-case publishes TimerBreached for its service level timer
    And an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes
    Then the D7.1 item moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026, and "U-9213" is told with MSG-P7-011
    And the SSME item is assigned to the L5 holder at once and its routing entry records reason "NO_HOLDER" for L6
    And both cases stay "Waiting approval" and no case status changes

  Scenario: AC4 Failure isolation and the refusal answers leave the approval unchanged (new, D-RCV-60)
    Given approval "A-1" of AC1 is WAITING and "U-9210" also holds RW-PRODHEAD at L6 as substitute
    When "U-9210" approves "A-1" and "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves
    Then the preparer call returns 409 with MSG-P7-002 and the change call returns MSG-P7-001 with level "L5" and approver "U-9202"
    And "A-1" is still WAITING, moves to L5 with the changed terms and records no approval at L6
    When an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes
    Then it is stored with status "HELD_NO_LIMIT", the case stays "Waiting approval" and MSG-P7-010 is raised to RW-RISK
    When the rwb-decision fake forces the decision-log write to fail on the approval
    Then the answer is 503 with MSG-P7-003, no decision record is written, and neither the approval nor the case moves

  Scenario: AC15 An outcome the decision log cannot take does not take effect (new, D-RCV-60)
    Given approval "A-1" of AC1 is WAITING with L6 holder "U-9201"
    When "U-9201" approves "A-1" and the decision-log write fails
    Then no decision record is written and the approval status stays "WAITING"
    And case "RW-2026-000124" stays "Waiting approval"

  Scenario: AC16 A redelivered event is applied once (new, D-RCV-60)
    Given the approval event for "A-1" of AC1 has been consumed once
    When the same event is delivered again
    Then no further decision record is written for "A-1" and the case status is unchanged

  Scenario: AC17 A status change the model does not allow is refused (new, D-RCV-60)
    Given approval "A-1" of AC1 is APPROVED
    When a change of "A-1" back to "WAITING" is requested
    Then the request is refused with the error code Not specified in the source documents (NEWAC-RWB-ITG-E2013-ITG-AC17) and "A-1" keeps status "APPROVED"
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A decision with delegation rows routes to the lowest level whose row covers it on the routing date; the item keeps that delegation version | REQ-APD-001; REQ-APD-010; RWB-E1-038; Delegation of authority matrix, rule 9 |
| BR2 | A decision with no amount limit routes to the role named in its route parameters, for D7.1 notices RW-LITOFF | Parameters rwb.approval.route.*; DL22 |
| BR3 | The approver must hold the A letter in the decision's capability area and be the holder or substitute of the required level, or hold the route role | Permission matrix; Key sheet: A works within the delegation table; CTL-04 |
| BR4 | A person may not approve a decision they proposed or prepared | Admin and access model, section 6.2; CTL-05; Delegation of authority matrix, rule 10 |
| BR5 | An approval above the caller's level is refused and sent to the level that covers it, with no silent approval | REQ-APD-004; R-UNI-15 |
| BR6 | A change from the recommendation needs a coded reason; refuse and return need a reason | REQ-APD-005; R-UNI-14; CTL-07 |
| BR7 | An approval not answered inside its service level escalates one level up, or to the escalation role; the case does not move | REQ-APD-007; R-UNI-30; R-UNI-42 |
| BR8 | A level with no holder and no substitute passes the item one level up at once | REQ-APD-011 |
| BR9 | Levels L1 to L3 approve by committee resolution; the entry records the resolution reference, the date and the members present | REQ-APD-008; doa.txt, Levels sheet |
| BR10 | The limit, the rule version and the approver are written with every approval | REQ-APD-009; FEAT-DRI-04 |
| BR11 | A decision that no limit covers is held and raises an incident | Delegation of authority matrix, rule 8 |
| BR12 | An approval outcome that cannot be written to the decision log does not take effect | Principle 5; R-UNI-39 |

The harness asserts these rules against the owning services; it does not re-implement them. No BR row is changed by this story. BR12 is asserted by AC15 and by AC4 (the decision-log write fails: no decision record, neither the approval nor the case moves).

### 9. State transitions

The states below are the states the harness observes. The harness changes no approval status and no case status itself; every transition is caused by a call to the owning service or by the timer breach the owning service publishes.

| From | Event | Condition | To |
|---|---|---|---|
| IN_PROGRESS | Recommendation routed for approval | A delegation row covers the decision, product and amount on the routing date | WAITING_APPROVAL, approval WAITING |
| IN_PROGRESS | Recommendation routed for approval | No delegation row covers the decision and product | WAITING_APPROVAL, approval HELD_NO_LIMIT |
| WAITING_APPROVAL | Approver accepts | Caller within the required level, not the preparer, decision record written | IN_PROGRESS, approval APPROVED |
| WAITING_APPROVAL | Approver changes and accepts | Changed terms within the caller's level, coded reason given, decision record written | IN_PROGRESS, approval APPROVED |
| WAITING_APPROVAL | Approver refuses or returns | Reason given | IN_PROGRESS at the state the rule names, approval REFUSED or RETURNED |
| WAITING_APPROVAL | TimerBreached | Service level breached | WAITING_APPROVAL, with the next level or the escalation role |
| WAITING_APPROVAL | A change raises the amount above the caller's level | A level covers the changed terms | WAITING_APPROVAL, with the covering level |

A failed decision-record write leaves the approval and the case exactly as they were.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Holders and substitutes of levels L4 to L6 (synthetic test users at DL18) | The approvers the harness drives at their level: approve, change, refuse or return an item |
| Recording holder of levels L1 to L3 | Records the committee resolution with its reference and the members present; driven by the harness in the committee case |
| RW-RESTRUCT, RW-CREDCOMM | Treatment and offer preparers; the synthetic preparer U-9210 holds RW-RESTRUCT and may not approve what it prepared |
| RW-LITOFF Litigation officer, RW-LEGAL Legal counsel, RW-HEADLIT Head of Litigation | Approve D7.x items routed to their role, and receive the escalation of a role-routed item |
| RW-PRODHEAD Product head | Approves items of their product at their level, in Treatment and offer, Litigation, Asset and disposal, Debt sale, Write-off and posting |
| RW-SALEOFF, RW-HEADNPA, RW-HEADASL, RW-DEBTSALE | Approve Asset and disposal or Debt sale items at their level |
| RW-CREDITAD, RW-WOCOMM, RW-FINANCE | Approve Write-off and posting items at their level |
| SY-RULES, SY-CASEWF | Call the router, start and close the service level timer and publish the timer breach; driven by the harness through the owning contract |
| RW-AUDIT | Reads approvals and outcomes through the decision log |
| Approval levels | L1 Board of Directors to L6 Recovery executive, department level, per the delegation of authority table |

No approval level and no holder is created by this story; the delegation data is owned by RWB-P4-E1038-APP and the authorise answer is owned by RWB-P4-E2013-APP, through POST /authorise. No names of people appear in the harness, its data or its report.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-032 to DF-DEC-053 | approval | id, case_id, decision_code, regulation_item, capability_area, route_role_code, approval_level, delegation_limit_id, limit_version, product_group, amount, terms, prepared_by, assigned_user_id, status, due_at, escalation_level, source_type, source_ref, rule_id, rule_version, decision_log_id | Read through the rwb-decision contract |
| DF-REF-018 | delegation_limit | approval_level | Read through the rwb-access contract |
| DF-REF-023 | delegation_limit | holder_user_id | Read through the rwb-access contract |
| DF-REF-024 | delegation_limit | substitute_user_id | Read through the rwb-access contract |
| DF-WRK-019 | task | task_code | Read through the rwb-case contract |
| DF-WRK-020 | task | element_type | Read through the rwb-case contract |
| DF-WRK-023 | task | owner_role | Read through the rwb-case contract |
| DF-WRK-030 | timer | timer_type | Read through the rwb-case contract |
| DF-WRK-032 | timer | expires_at | Read through the rwb-case contract |
| DF-WRK-036 | timer | escalation_level | Read through the rwb-case contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the rwb-decision contract |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read through the rwb-decision contract |

Test data is synthetic: case numbers, user IDs, amounts, delegation versions and reasons. No production case, party or approval is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/approvals` | P7 rwb-decision | The approval queue of the holder: decision, amount, level, limit version and age |
| GET | `/api/recovery/decision/v1/approvals/{approvalId}` | P7 rwb-decision | One approval with limit version, rule ID and version, due time and escalation level |
| POST | `/api/recovery/decision/v1/approvals/{approvalId}/approve` | P7 rwb-decision | Approve, or change and approve; Idempotency-Key required |
| POST | `/api/recovery/decision/v1/approvals/{approvalId}/return` | P7 rwb-decision | Return an item with a question; reason required |
| POST | `/api/recovery/decision/v1/approvals/{approvalId}/refuse` | P7 rwb-decision | Refuse an item with a reason |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The routing, escalation and outcome records of the run |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and DoA check behind a direct call (Architecture v5 slide 14: rwb-access IN POST /authorise) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case status, including Waiting approval |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The service level timer and its state after an approval or an escalation |
| PATCH | `/api/recovery/case/v1/tasks/{taskId}` | P3 rwb-case | The approval task, asserted completed after an approval |
| POST | `/api/recovery/comms/v1/cases/{caseId}/messages` | P6 rwb-comms | The escalation notification to the new approver |

The DoA answer is asserted through POST /authorise and through the limit version on the approval; the harness reads no delegation operation of its own. The composite approval-queue route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON; its path and merge order are Not specified in the source documents (GAP-0397; ASM-0572).

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.decision.ApprovalRequested.v1 | rwb.decision.events.v1 | P7 rwb-decision | One event per routed item, with the approval ID, case ID, level and amount, and no personal data |
| rwb.decision.ApprovalDecided.v1 | rwb.decision.events.v1 | P7 rwb-decision | One event per decided item, after the decision record |
| rwb.case.TimerBreached.v1 | rwb.case.events.v1 | P3 rwb-case | The service level breach that drives the escalation, with the approval reference |
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The routing, escalation and outcome records reach the ledger within 5 minutes of the call |

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity; it drives REST and observes the workflow that rwb-decision already owns.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow; the escalation clock is driven by a fixed clock in the harness.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-decision | approvals, approvals/{approvalId}, approve, return, refuse, decision-log | "A-1" at L6 with limit version DOA-2026.11; the D7.1 item at role RW-LITOFF; 409 preparer, 409 two approvers, 422 missing reason, 422 missing resolution reference, 422 missing coded reason; HELD_NO_LIMIT for HIRE_PURCHASE; a forced write failure for the 503 case |
| rwb-access | authorise, delegation data behind it | Allow the holder, substitute and route role; do not cover HIRE_PURCHASE under DOA-2026.11; an L6 SSME row with no holder and no substitute; DOA-2027.01 in force from 1 January 2027 |
| rwb-case | cases/{caseId}, cases/{caseId}/timers, tasks/{taskId} | Case status Waiting approval and In progress; the service level timer open and then closed; a timer breach at 09:00 on 15 December 2026 |
| rwb-comms | cases/{caseId}/messages | ACCEPTED for the escalation notification, with one message per escalated item |

The fakes are published from the owning services' OpenAPI documents and are replaced by the real service as each I story lands, contract by contract. The harness repository, its environment and its evidence format: Not specified in the source documents (GAP-0397; ASM-0572).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Eleven consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.decision.ApprovalRequested.v1 and rwb.decision.ApprovalDecided.v1 on rwb.decision.events.v1, rwb.case.TimerBreached.v1 on rwb.case.events.v1 and rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity or Nexus operation; it observes the approval and timer behaviour of the owning services |
| File | No | Reads and writes no file |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the I stories.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| ApprovalRouteClient | Harness adapter | Calls the eleven consumed operations of §12.2 with the Idempotency-Key header where the operation requires one |
| FakePack | WireMock project | Serves rwb-decision, rwb-access, rwb-case and rwb-comms from the published OpenAPI documents of §12.8 |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference found in the trace, so a service never reads another service's tables |
| DecisionOrderCheck | Assertion | Fails the run when an approval status changes before its decision record, or when a second record exists for one action and one Idempotency-Key |
| EscalationClock | Harness driver | Drives the fixed clock to the service level due time and starts the timer breach through the owning service, so the escalation is repeatable |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0397; ASM-0572) |

**Environment and test data**

- Environment: SIT, one namespace, the owning services deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment and data seeding: Not specified in the source documents (GAP-0397; ASM-0572).
- Data: delegation version DOA-2026.11 and, for the version case, DOA-2027.01 from 1 January 2027; holders U-9201 at L6, U-9202 at L5, U-9203 at L4 and the L3 committee recording holder U-9204; preparer U-9210; litigation users U-9211, U-9212 and U-9213; case RW-2026-000123 with the D7.1 demand notice under R-LIT-03 version LIT-2026.12; case RW-2026-000124 with the D6.4 MORTGAGE settlement at principal 2,400,000.00, loss 20.00 percent and loss amount 480,000.00. No production record is copied.
- Clocks: the escalation clock is a fixed clock in the harness, set to 09:00 on 14 December 2026 and advanced to the due time; the service level values themselves are read from the owning service.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and ApprovalRouteClient against the published OpenAPI documents of the owning services.
2. Publish FakePack for the four owning services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Add the routing assertion of AC1, including the level, the limit version, the routing entry and the queue answer.
4. Add the approval journey of AC2, asserting the decision record before the case status, the task completion and the closed timer.
5. Add the escalation and no-holder journey of AC3 with the EscalationClock, and assert that the case does not move.
6. Add the refusal and hold answers of AC4, then the decision-log failure, keeping the same assertions.
7. Replace each fake with the real service as its I story lands, contract by contract.
8. Publish the run report per business date and add the pass/fail gate agreed with QA; the gate definition: Not specified in the source documents (GAP-0397; ASM-0572).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.decision.approval-routing` from the legacy solution plan; the harness asserts the disabled state and the enabled state of the approval endpoints.

**Done when:** the journey runs green against the six deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-001 | Approval above the caller's level | This needs approval at level {level}. It has been sent to {approver}. |
| MSG-P7-002 | Preparer tries to approve | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | Entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-004 | Approved | Approved. The case moves to {state}. |
| MSG-P7-005 | Change from the recommendation without a coded reason | Enter the reason you are not following the recommendation. |
| MSG-P7-010 | No limit covers the decision and product | No approval limit covers {decision} for {product}. The item is held and Risk has been told. |
| MSG-P7-011 | Item escalated to a new approver (new) | {decision} on case {caseNo} passed its service level and is now with you for approval. |
| MSG-GEN-001 | Reason, resolution reference or members present missing | Enter {field}. |
| MSG-GEN-004 | Item changed by another approver | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | No A letter in the decision's area | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values; it does not own the message text. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-10 Approval queue | Loading | The composite route is called once and the answer is returned inside the 2 s budget |
| SCR-10 Approval queue | List | Each item waiting on the holder is returned with decision, case, amount, level, limit version, age and due time, and the item prepared by the caller is absent |
| SCR-10 Approval queue | Empty | An approver with nothing waiting gets an empty list, not an error |
| SCR-10 Approval queue | Refused action | A user without the A letter in the area, or not the holder, substitute or route role, is refused with MSG-P4-002 |
| SCR-10 Approval queue | Error | Not specified in the source documents (CG-ALL-645) |
| SCR-10 Approval queue | No access | Not specified in the source documents (CG-ALL-645) |

The harness opens no screen and renders no page; it asserts the composite route answer and the direct endpoint answers that the screen consumes. Screen-level behaviour remains with the owning APP stories, and the decision screen is out of scope. The harness environment and evidence detail: Not specified in the source documents (GAP-0397; ASM-0572).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-013-01-ITG | AC1, BR2 | Integration | Synthetic demand notice under R-LIT-03 |
| TC-E2-013-02-ITG | AC2, BR7 | Integration | Approval timer breached at 09:00 next day |
| TC-E2-013-03-ITG | AC3, BR1 | Integration | Delegation versions DOA-2026.11 and DOA-2027.01 |
| TC-E2-013-04-ITG | AC4, BR1 | Integration | D6.4 Mortgage at 2.4 million baht |
| TC-E2-013-05-ITG | AC5, BR3, BR10; run by RWB-P7-E2013-APP | Integration | L6 holder approving |
| TC-E2-013-06-ITG | AC6, BR4; run by RWB-P7-E2013-APP | Integration | Preparer who is also a substitute |
| TC-E2-013-07-ITG | AC7, BR5; run by RWB-P7-E2013-APP | Integration | Principal changed to 120 million baht |
| TC-E2-013-08-ITG | AC8, BR6; run by RWB-P7-E2013-APP | Integration | Refuse without and with a reason |
| TC-E2-013-09-ITG | AC9, BR6; run by RWB-P7-E2013-APP | Integration | Return with a question |
| TC-E2-013-10-ITG | AC10, BR6; run by RWB-P7-E2013-APP | Integration | Change without a reason code |
| TC-E2-013-11-ITG | AC11, BR8; run by RWB-P7-E2013-APP | Integration | SSME L6 row with no holder |
| TC-E2-013-12-ITG | AC12, BR9; run by RWB-P7-E2013-APP | Integration | L3 committee approval with resolution PARC-2026-14 |
| TC-E2-013-13-ITG | AC13; run by RWB-P7-E2013-APP | Integration | Holder and substitute approving at once |
| TC-E2-013-14-ITG | AC14, BR11; run by RWB-P7-E2013-APP | Integration | Hire purchase with no delegation rows |
| TC-E2-013-15-ITG | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E2-013-16-ITG | Principle 5 | NFR | The decision log write forced to fail during an approval |
| TC-E2-013-17-ITG | AC15, BR12 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E2013-ITG-AC15) |
| TC-E2-013-18-ITG | AC16 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E2013-ITG-AC16) |
| TC-E2-013-19-ITG | AC17 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E2013-ITG-AC17) |

The AC column in Covers names the legacy AC of RWB-E2-013 that the copy is derived from. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: delegation versions, levels, limits, holders, route roles, capability areas, service levels and override reasons are data or parameters held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: member references are used instead of names, the synthetic user IDs and case numbers are the only identifiers, and the run report holds IDs and assertions only.
- No read of another service's tables: the delegation is read through the rwb-access contract, the approvals and the decision records through the rwb-decision contract, the case, task and timer through the rwb-case contract and the notification through the rwb-comms contract; the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway, a notification provider or a production endpoint.
- No approval without its decision record: DecisionOrderCheck fails the run when a status moves before its record, and the change is never asserted as applied.
- No item may be assigned to its preparer: the harness asserts the absence of the item in the preparer's queue and the 409 answer.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-001 | Route to the approver named by the delegation table | Epic 2, 3.7 | FEAT-APD-01, FEAT-APD-10 | 17 Run the decision center | BR1, BR2 | TC-E2-013-01-ITG, TC-E2-013-03-ITG, TC-E2-013-04-ITG |
| REQ-APD-003 | Accept, change, reject or return, each recorded | Epic 2, 3.7 | FEAT-APD-02, FEAT-APD-03, FEAT-APD-04 | 17 Run the decision center | BR3, BR6 | TC-E2-013-05-ITG, TC-E2-013-07-ITG, TC-E2-013-09-ITG |
| REQ-APD-004 | Above the limit refused and raised, no silent approval | Epic 2, 3.7 | FEAT-APD-05 | 17 Run the decision center | BR4, BR5 | TC-E2-013-05-ITG, TC-E2-013-07-ITG, TC-E2-013-14-ITG, TC-E2-013-15-ITG |
| REQ-APD-005 | Override needs a coded reason | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR6 | TC-E2-013-07-ITG, TC-E2-013-08-ITG, TC-E2-013-10-ITG |
| REQ-APD-007 | Unanswered approval escalates to the named role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR7 | TC-E2-013-02-ITG, TC-E2-013-04-ITG, TC-E2-013-05-ITG |
| REQ-APD-008 | Committee decision recorded with members present | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR9 | TC-E2-013-01-ITG, TC-E2-013-04-ITG, TC-E2-013-12-ITG |
| REQ-APD-009 | Limit, rule version and approver written with every approval | Epic 2, 3.7 | FEAT-APD-11 | 17 Run the decision center | BR10, BR12 | TC-E2-013-01-ITG, TC-E2-013-04-ITG, TC-E2-013-05-ITG |
| REQ-APD-010 | Open items keep the delegation version they were decided under | Epic 2, 3.7 | FEAT-APD-10 | 17 Run the decision center | BR1 | TC-E2-013-01-ITG, TC-E2-013-03-ITG, TC-E2-013-05-ITG |
| REQ-APD-011 | Routing escalates rather than stalls with no person in a role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR8 | TC-E2-013-01-ITG, TC-E2-013-02-ITG, TC-E2-013-11-ITG |

### 19. Out of scope

- The six I stories RWB-P4-E1038-APP, RWB-P3-E1028-APP, RWB-P7-E2013-APP, RWB-P3-E2013-APP, RWB-P4-E2013-APP and RWB-P6-E2013-APP, and everything they own: the delegation table and its lookup, the router, the approval workflow, the approval and decision-log endpoints, the case status, the task and the timer, the authorise answer and the escalation notification.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-decision, rwb-access, rwb-case and rwb-comms, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The decision screen SCR-11 and the D7.1 demand and recall notice approval with release to dispatch (RWB-E2-014).
- The committee pack screen SCR-12 with each member's vote (Epic 4).
- The recommendation with reasons and expected return by route (Epic 4).
- The monthly override reason report (Epic 8).
- The names of level holders and substitutes (DL18) and the service level values (DL22); the harness uses the synthetic values of §7 and reads the real ones from the owning service.
