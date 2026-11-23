# RWB-P3-E2013-APP Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P3-AF |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P7-E2013-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010, REQ-APD-011) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-013 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner, and the service that holds the case**, I want **the case set to Waiting approval and a decision task opened for the routed approver with its due time as soon as a decision on that case goes for approval, the case held there while the item escalates, and the case returned to the state its routing rule names when the approver refuses or returns it**, so that **a case shows the truth about who is deciding it, and no case sits in the wrong state or with an owner who is not the decider while someone else approves**.

Inside `rwb-case` this is the case-side capability of the approval routing of legacy RWB-E2-013:

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- The capability runs as two activities of `CaseWorkflow`, reached by the case router from a Kafka event on `rwb.decision.events.v1`: `openApprovalTask` when a decision goes for approval, and `applyApprovalDecision` when the approver acts.
- The approval record, the delegation of authority lookup, the approval decision endpoints and the decision log entry stay in `rwb-decision` (P7); the DoA table stays in `rwb-access` (P4). This story owns the case status, the decision task and the service level clock projection on the case, and it re-derives no level and no limit.
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-0732; ASM-1295); this story uses the phrase "the rwb-case login (DP-02)" and never the shared monolith login.

The legacy behaviour carried into the case service is unchanged: the same case status names, the same status a refused case returns to, the same decision task per case, the same escalation on a service level breach, and the same refusal to stall a case when a level has no holder or when no limit covers the decision.

### 2. Business rationale

Approval and authority governance is an audit finding: approvals today are given by e-mail, sometimes above the approver's limit or by the person who prepared the decision. The decision side of that finding is routed by the delegation of authority table in `rwb-decision`, but the case side matters just as much: while a decision is being approved the case must say so, the person who has to decide must have the task on the case with the time it is due, and when the outcome arrives the case must return to the state its routing rule names, not to a state that a person typed. This story puts controls CTL-04, CTL-05 and CTL-07 in place on the case, supports the measure decisions within the delegation of authority (target 100 percent), and meets REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010 and REQ-APD-011 on the case.

Under Architecture v5 the approval is the `ApprovalWorkflow` of the workflow kit, running on `rwb-decision` and routed by the DoA table of `rwb-access`; `rwb-decision` publishes `ApprovalRequested` and `ApprovalDecided` on `rwb.decision.events.v1`, and `rwb-case` reacts to them. The realignment changes the mechanism, not the business rule:

1. The in-process call `ApprovalRouter.request` of the monolith becomes a Kafka fact: `rwb-decision` publishes `ApprovalRequested`, and `rwb-case` consumes it through the case router and its inbox (DP-09) instead of being called synchronously. A case is never left waiting on a call that failed.
2. The P3 task and timer interfaces of the monolith become this service's own `task` and `timer` rows: `openApprovalTask` writes them in the same transaction as the case status, and `applyApprovalDecision` closes them, so the case and its task can never disagree.
3. The decision log writer of another module becomes the local decision-record library of DP-03 for the case status change, hash-chained and published on `rwb.decision-record.v1`; the routing entry and the approval outcome entry stay with `rwb-decision`, which owns the approval.
4. The Quartz timer of JOB-05 becomes a durable timer in the workflow that owns the approval (`rwb-decision`), and the `timer` row of the case becomes the projection behind the case timer read. JOB-05 stays a legacy reference only.
5. The reference lists of status, task element type and role are read through this service's own reference-data contract of DP-07, and the permission check behind the case reads comes from the guard library and the authorise contract of DP-08.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P7-E2013-CON | The published approval contract: the approval resource with its level, limit version, status and due time, the `ApprovalRequested` and `ApprovalDecided` events on `rwb.decision.events.v1`, and the contract fakes. Which fields of an approval request the case consumes is Not specified in the source documents (GAP-0732; ASM-1297) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the case status change |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and `rwb-case`'s own parameters contract (DP-06): the case-side feature switch and the approval route and service level parameter rows |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and `rwb-case`'s reference-data contract (DP-07): LOV-CASE-STATUS, LOV-ELEMENT, LOV-TASK-STATUS, LOV-TIMER and LOV-ROLE, with the version in force |
| RWB-PLT-E1037-CON | The guard library and the `rwb-access` authorise contract (DP-08): the cached permission decision behind the case reads, refusing with MSG-P4-002 |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one `ApprovalRequested` or `ApprovalDecided` handled once |
| RWB-PLT-E1071-CON | The workflow kit in namespace `rwb-recovery`: `CaseWorkflow`, activity registration, retry policy and durable timers (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves the case record and my-work screens (DP-19) |

Business preconditions carried from RWB-E2-013:

- Delegation version DOA-2026.11 is in force and the lookup returns the lowest covering level (legacy RWB-E1-038). In the target the DoA table is `rwb-access` (P4) and the lookup is its DoA-limits contract; holders and substitutes are named test users in SIT and UAT (DL18).
- Approval route parameters exist for each decision with no amount limit; for D7.1 notices: `rwb.approval.route.D7.1.area`=LITIGATION, `rwb.approval.route.D7.1.role`=RW-LITOFF, `rwb.approval.route.D7.1.escalation-role`=RW-HEADLIT, `rwb.approval.route.D7.1.service-level`=1 working day (assumed; DL22). Under the R-PREC default ruling these are parameter rows of `rwb-case`, read by `rwb-decision` through the parameters contract of DP-06.
- Service level for limit-based approvals: `rwb.approval.service-level.default`=3 working days (assumed from the 3 working day approval timers in R-RES-10 and R-SET-05; DL22).
- Capability area per decision code: D5 and D6.x Treatment and offer, D7.x Litigation, D8.2 and D8.3 Asset and disposal, D8.4 Debt sale, D9.x Write-off and posting (parameters `rwb.approval.area.<code>`).
- LOV-OVERRIDE-REASON is loaded with the coded override reasons (owner RW-COE); it is read by `rwb-decision`, not by this story.
- The case is in an active status when the request arrives. A case already on hold keeps `ON_HOLD` and the status it paused in is written to `status_before_hold` (R-UNI-20, R-UNI-21); a closed case takes no decision task.
- The login is the rwb-case login (DP-02): Not specified in the source documents (GAP-0732; ASM-1295).

### 4. Flow

1. `rwb-decision` (P7): the `ApprovalWorkflow` of the kit routes the decision by the DoA table of `rwb-access`, stores the approval as WAITING or HELD_NO_LIMIT, and publishes `rwb.decision.ApprovalRequested.v1` on `rwb.decision.events.v1` with the approval reference, the case, the decision code, the capability area, the routed role or holder, the approval level, the limit version, the due time and the approval status. The payload is Not specified in the source documents (GAP-0732; ASM-1297).
2. `rwb-case` case router: reads the event into the inbox of DP-09, deduplicates by event ID (R-UNI-40), and calls `signalWithStart` on `CaseWorkflow` with workflow ID equal to the case ID, on task queue `rwb-case`.
3. `CaseWorkflow`: forwards the request to the `openApprovalTask` activity with the case snapshot: case ID, status, `route_state`, `legal_hold`, and the approval facts of the event. A closed case is refused here (X10) and takes no task.
4. `openApprovalTask`: reads the status value, the task element type, the task status and the role from the reference-data contract of DP-07, with the version in force; no status name, element type or role code is written in code (BR-P3-006).
5. `openApprovalTask`, one `RecordAndApply` transaction in `rwb_case`: the `task` row is written with element type `DECISION_TASK`, `owner_role` set to the routed role, `due_at` set to the approval due time, status `OPEN`, the approval reference, and the preparer reference so the approval cannot be seen by the person who prepared it. The task shape is Not specified in the source documents (GAP-0732; ASM-1297). A role-routed task has no person on it, so no `assignment` row is written; a request that names a holder carries that holder reference in the same assumed shape.
6. `openApprovalTask`, same transaction: the `timer` row is written with `timer_type` `SERVICE_LEVEL`, `started_at` at the request time, `expires_at` at the approval due time, status `RUNNING` and `escalation_level` 0. The clock itself is the durable timer of the workflow that owns the approval; the row is the projection behind the case timer read.
7. `openApprovalTask`, same transaction: `recovery_case.status` becomes `WAITING_APPROVAL`, or stays `ON_HOLD` with `status_before_hold` set to `WAITING_APPROVAL` when a hold is in force; the local decision record of DP-03 is written with the from and to status, the approval reference, the approval level and the limit version; the outbox row for `rwb.case.CaseStateChanged.v1` is written.
8. A request with approval status HELD_NO_LIMIT (AC14) moves the case to `WAITING_APPROVAL` and opens no decision task, because the event names neither a role nor a holder; the incident to RW-RISK with MSG-P7-010 is raised by `rwb-decision`. The mapping from an approval status to a case status is Not specified in the source documents (GAP-0732; ASM-1298).
9. Approver accepts: `rwb-decision` publishes `rwb.decision.ApprovalDecided.v1` with final call APPROVED; the case router hands it to `applyApprovalDecision`, which in one transaction closes the open decision task (`DONE`, outcome `APPROVED`, `completed_at`), stops the service level timer, sets the case to `IN_PROGRESS`, writes the decision record and the `CaseStateChanged` outbox row. The source module then acts on its own (a notice is released to dispatch in RWB-E2-014); this story takes no action there.
10. Approver changes and accepts: the same path as step 9; the decided event carries the changed terms and the coded reason, which this story records on the decision task outcome and does not interpret.
11. Approver refuses: final call REFUSED; `applyApprovalDecision` closes the task with outcome `REFUSED`, stops the timer, sets the case to `IN_PROGRESS` and writes `recovery_case.route_state` from the resume state the routing rule names, with the rule ID and version carried by the decided event (for a settlement below the floor, rule R-SET-07 and state DECLINED_BY_APPROVER_SET). Which case status accompanies the rule-named state is Not specified in the source documents (GAP-0732; ASM-1298).
12. Approver returns with a question: final call RETURNED; `applyApprovalDecision` closes the task with outcome `RETURNED`, stops the timer, sets the case to `IN_PROGRESS`, and opens one human task for the preparer named in the event (element type `HUMAN_TASK`, owner the preparer user reference, due time absent). The task code of that task is Not specified in the source documents (GAP-0732; ASM-1297).
13. Service level passes with no action: the durable timer of the approval workflow breaches and `rwb-decision` re-publishes `ApprovalRequested` for the same approval reference with the escalation level raised by one and a new due time; `openApprovalTask` reassigns the open decision task (new `owner_role`, new `due_at`) and moves `timer.escalation_level`, `escalated_to_role` and `escalated_at`. The case status does not change and no `CaseStateChanged` is published (BR7). The escalation signal is Not specified in the source documents (GAP-0732; ASM-1299).
14. No holder at the required level: the request arrives already routed one level up with reason NO_HOLDER; the case opens the decision task for the covering level at once and waits, so no case waits on nobody (AC11).
15. Case owner: opens the case record through gateway-bff, which calls `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/me/tasks` on `rwb-case` and merges the answers into the screen model; the case shows `WAITING_APPROVAL` and the decision task with its role and due time.

Every case status change is written in one transaction with its local decision record and its outbox row (R-UNI-39), so a failure leaves the case, the task and the record unchanged and the event is redelivered.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The service level passes with no action | The open decision task is reassigned to the next level or the escalation role, the timer row moves with it; the case does not move | MSG-P7-011 | AC2 |
| X2 | The caller prepared the decision | Refused by `rwb-decision` with 409; no decided event, so the case is unchanged | MSG-P7-002 | AC6 (carried by the P7 slice) |
| X3 | A change raises the amount above the caller's level | The item is sent to the level that covers it; the case stays `WAITING_APPROVAL` and the task moves up | MSG-P7-001 | AC7 (carried by the P7 slice) |
| X4 | Refuse or return without a reason | Refused with 422; no decided event, so the case is unchanged | MSG-GEN-001 | AC8 |
| X5 | A change departs from the recommendation without a coded reason | Refused with 422; the case is unchanged | MSG-P7-005 | AC10 (carried by the P7 slice) |
| X6 | The required level has no holder and no substitute | The request arrives routed one level up; the task opens for the covering level at once; the case waits | MSG-P7-011 | AC11 |
| X7 | A committee level is approved without a resolution reference or the members present | Refused with 422; the case is unchanged | MSG-GEN-001 | AC12 (carried by the P7 slice) |
| X8 | Two approvers act on one item at once | One call succeeds and one decided event is published; the case applies it once through the inbox and the version check; the other call gets 409 | MSG-GEN-004 | AC13 (carried by the P7 slice) |
| X9 | No delegation row covers the decision and product | The approval is held as HELD_NO_LIMIT, the case waits with no decision task and Risk is told; the incident is `rwb-decision`'s | MSG-P7-010 | AC14 |
| X10 | A request arrives for a closed case | No decision task is opened and the status is not changed; the mismatch is recorded with the message | MSG-P3-005 | BR14 |
| X11 | A decided event arrives for a case with no open decision task | The event is dropped with its ID recorded in the inbox and an entry in the log; no status changes | None | BR12 |
| X12 | The local decision record cannot be written | Nothing changes: the task, the timer and the status are not written, MSG-P7-003 is recorded, and the event stays on the topic for redelivery | MSG-P7-003 | BR12 |
| X13 | A role without Case record R reads the case or the task list | Refused with 403 by the guard behind the endpoint | MSG-P4-002 | TC-E2-013-15 |

A stale record at commit (zero rows updated on `recovery_case.version`) is MSG-GEN-004 and the event is retried, never applied twice; the case and its task are always written together, so a partial state cannot be read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the approval contract of RWB-P7-E2013-CON, the platform contract stories of its H list and the fakes; the DoA answer, the approval record and the permission decision never arrive as a direct call |
| Negotiable | Status names, element types, roles and the switch are data; the story fixes the case-side behaviour only |
| Valuable | The case tells the truth about who is deciding it, and no case waits in the wrong state or on nobody |
| Estimable | Two activities, one case router path, one task and timer projection, two read endpoints already in the case contract, one migration |
| Small | Fits two weeks with its tests |
| Testable | Every owned criterion has a test case in section 16; the approval side is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Approval routing with the delegation of authority table

  Background:
    Given the environment is SIT
    Given delegation version "DOA-2026.11" is in force with holder "U-9201" at L6, "U-9202" at L5 and "U-9203" at L4 for MORTGAGE, all holding RW-PRODHEAD
    Given test user "U-9210" holds RW-RESTRUCT and test users "U-9211" and "U-9212" hold RW-LITOFF and test user "U-9213" holds RW-HEADLIT

  Scenario: AC1 Routed (legacy RWB-E2-013 AC1)
    Given a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211"
    Given the rwb-decision contract mock returns approval "A-1" requested for case "RW-2026-000123" with decision D7.1, area "LITIGATION", route role RW-LITOFF and due at 09:00 on 15 December 2026
    When the router runs for decision D7.1 at 09:00 on 14 December 2026
    Then an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026
    Then the system does not show it to "U-9211", who prepared it
    Then the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role"
    Then the case status becomes "Waiting approval"

  Scenario: AC2 Escalated (legacy RWB-E2-013 AC2)
    Given the approval of AC1 is still WAITING at 09:00 on 15 December 2026
    Given the rwb-decision contract mock returns approval "A-1" requested again for case "RW-2026-000123" with route role RW-HEADLIT, escalation level 1 and due at 09:00 on 16 December 2026
    When JOB-05 publishes TimerBreached for its service level timer
    Then the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026
    Then the system writes one entry with final call "ESCALATED" and "U-9213" is told with MSG-P7-011
    Then the case stays "Waiting approval"

  Scenario: AC5 Approve inside the limit (legacy RWB-E2-013 AC5)
    Given the approval of AC4 is WAITING
    Given the rwb-decision contract mock returns approval "A-1" for case "RW-2026-000124" decided "APPROVED" by "U-9201" at level "L6" under limit version "DOA-2026.11"
    When "U-9201" approves it with Idempotency-Key "k-501"
    Then the approval status becomes "APPROVED"
    Then the system writes one entry with approver "U-9201", approval level "L6", limit version "DOA-2026.11", the rule ID and version and final call "APPROVED"
    Then the system publishes decisionRecorded and the response shows MSG-P7-004 with state "In progress"

  Scenario: AC8 Refuse needs a reason (legacy RWB-E2-013 AC8)
    Given the approval of AC4 is WAITING
    Given the rwb-decision contract mock returns approval "A-1" for case "RW-2026-000124" refused with reason "Collateral appraisal older than one year" and route state "DECLINED_BY_APPROVER_SET" under rule "R-SET-07"
    When "U-9201" refuses it with no reason
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "reason"
    Then when "U-9201" refuses it with reason "Collateral appraisal older than one year"
    Then the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names

  Scenario: AC9 Return with a question (legacy RWB-E2-013 AC9)
    Given the approval of AC4 is WAITING
    Given the rwb-decision contract mock returns approval "A-1" for case "RW-2026-000124" returned with reason "Attach the latest income statement"
    When "U-9201" returns it with reason "Attach the latest income statement"
    Then the system opens the status becomes "RETURNED", a task for preparer "U-9210", and the entry records the question

  Scenario: AC11 No holder means escalation, not a stall (legacy RWB-E2-013 AC11)
    Given the L6 row for SSME has no holder and no substitute
    Given the rwb-decision contract mock returns approval "A-2" routed to the L5 holder at once with reason "NO_HOLDER" for L6
    When an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes
    Then the system assigns it to the L5 holder at once
    Then the routing entry records reason "NO_HOLDER" for L6

  Scenario: AC14 No limit covers the decision (legacy RWB-E2-013 AC14)
    Given "DOA-2026.11" holds no row for HIRE_PURCHASE
    Given the rwb-decision contract mock returns approval "A-3" for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 with status "HELD_NO_LIMIT"
    When an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes
    Then the system stores the approval with status "HELD_NO_LIMIT" and the case stays "Waiting approval"
    Then the system raises an incident to RW-RISK with message MSG-P7-010
```

AC3, AC4, AC6, AC7, AC10, AC12 and AC13 are cited in the flow and the exception table but are carried by the P7 slice of this legacy key under RWB-P7-E2013-CON, where the delegation version, the limit, the preparer check, the committee resolution and the concurrency are proved; the seven criteria above are the ones this story owns.

In AC1 the case-side assertions are the last line and the decision task: the task is open for role RW-LITOFF with due time 09:00 on 15 December 2026, carries no person, and carries the preparer reference, so the work list does not show it to "U-9211", who prepared it. In AC2 and AC11 the case stays in `WAITING_APPROVAL` and only the task and the timer move. In AC5 the approved decision closes the task and moves the case to `IN_PROGRESS`. In AC8 the case returns to the state its routing rule names, which is written to `route_state`. In AC9 the return closes the decision task and opens one task for the preparer. In AC14 no decision task is opened because no approver is named, and the case waits.

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
| BR13 | A case in `WAITING_APPROVAL` has exactly one open decision task, and a case in any other status has none | REQ-CWC-005 (one state at a time); TSD P3 v3 T3.1 `task` |
| BR14 | Only a case in an active status may enter `WAITING_APPROVAL`; a closed case takes no decision task and a case on hold keeps its hold | FSD P3 v4 A2.3 VR-P3-003-1; R-UNI-20; R-UNI-21 |

Target-service statements that make the rules hold in `rwb-case`:

- BR1, BR2, BR3, BR4, BR5, BR6, BR9 and BR11 are executed in `rwb-decision`; this story consumes their result and never computes a level. `rwb-case` holds no copy of the DoA table and reads no `delegation_limit` row (the table is `rwb-access`, P4).
- BR7 on the case is the absence of a status change: an escalation request updates the open task and the timer row only, and publishes no `CaseStateChanged`. The escalation of the item itself is `rwb-decision`'s.
- BR8 is visible on the case as a decision task opened for the covering level, never as a task with no role.
- BR4 is also enforced on the case read: a decision task carries the preparer reference, and the work list does not show it to that user, so the preparer never sees the item as an approver.
- BR10 on the case is the decision task and the local decision record carrying the approval reference, the approval level and the limit version as they arrive in the event; the case never holds the limit itself.
- BR12 is executed by one `RecordAndApply` transaction with the decision-record library of DP-03; a failure rolls the status, the task and the timer back and the event is redelivered.
- BR13 is a partial unique index in `rwb_case` and a check in the activity.
- BR14 is the status check of the activity against LOV-CASE-STATUS read through DP-07; no status name is written in code (BR-P3-006; FSD P3 v4 A2.6).

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| In progress | Recommendation routed for approval | Approval stored WAITING or HELD_NO_LIMIT | Waiting approval |
| Waiting approval | Approver accepts | Caller within the required level, not the preparer | In progress |
| Waiting approval | Approver changes and accepts | Changed terms within the caller's level, coded reason given | In progress |
| Waiting approval | Approver rejects | Reason given | In progress, at the state the rule names |
| Waiting approval | SLA_BREACHED (R-UNI-30) | Service level timer breached | Waiting approval, with the next approver |
| Waiting approval | LEGAL_HOLD_PLACED (R-UNI-20) | A hold is placed while the item waits | On hold, with `status_before_hold` = WAITING_APPROVAL |
| On hold | LEGAL_HOLD_LIFTED (R-UNI-21) | The hold is lifted | Waiting approval, while the item still waits |

The approval record itself moves WAITING to APPROVED, REFUSED or RETURNED and stays WAITING with a new approver on escalation or on a change above the limit; that record is `rwb-decision`'s, and this story holds no copy of it.

In `rwb_case` the status codes are the LOV-CASE-STATUS values `IN_PROGRESS`, `WAITING_APPROVAL`, `ON_HOLD` and so on; the legacy story writes the same states in words. On a refusal the status returns to `IN_PROGRESS` and `route_state` takes the resume state the routing rule names (for example `DECLINED_BY_APPROVER_SET` under R-SET-07 for a settlement); which status accompanies that state is Not specified in the source documents (GAP-0732; ASM-1298).

Workflow states of the capability itself:

| From | Event | To |
|---|---|---|
| `CaseWorkflow` running | `ApprovalRequested` arrives through the case router | `openApprovalTask` scheduled |
| `openApprovalTask` done | Task, timer and status written | waiting on the next signal; the durable approval timer runs in `rwb-decision` |
| Waiting | `ApprovalRequested` arrives with a higher escalation level | `openApprovalTask` schedules the reassignment only |
| Waiting | `ApprovalDecided` arrives | `applyApprovalDecision` scheduled |
| `applyApprovalDecision` committed | Task closed, timer stopped, status written, record and outbox written | waiting on the next signal or stage |
| An activity refused by the status or record check | Error recorded with its message ID | waiting; the case is unchanged |
| Stage ends or 28 days pass | Continue-As-New | `CaseWorkflow` continues with the same workflow ID |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Holders and substitutes of levels L4 to L6, and the route roles, named by `rwb-decision` | See the decision task on their work list and act on the approval through the `rwb-decision` endpoints; they do not change the case directly |
| Recording holder of levels L1 to L3 | Records the committee resolution through `rwb-decision`; the case takes the outcome |
| Preparer of an item (for example RW-RESTRUCT on a settlement, RW-LITOFF on a notice) | Receives the return task on the case; may not approve |
| RW-CASEOWN and every role with Case record R | Read the case, its status `WAITING_APPROVAL` and its open decision task within their scope |
| SY-CASEWF (the `rwb-case` service identity) | Consumes the approval events, opens and closes the decision task, writes the status and the timer projection |
| SY-DECLOG (the decision-record library identity) | Writes the local decision record and publishes it on `rwb.decision-record.v1` |
| RW-AUDIT | Reads the case and its task and, through `rwb-decision`, the approval and the central ledger |

The authorisation decision is taken by `rwb-access` (Recovery roles as data, scope, masking and DoA in `rwb_access`) and is consumed as the cached permission decision that the guard library of DP-08 holds. This story adds no REST operation of its own; the refusal shape stays 403 with MSG-P4-002 on the case reads. The DoA lookup is `rwb-decision`'s call to `rwb-access`, not this service's.

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-0732; ASM-1295); the story refers to "the rwb-case login (DP-02)".

### 11. Data

| BR Field ID | Table in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` | id | Read |
| DF-CAS-005 | `recovery_case` | status | Write |
| DF-CAS-006 | `recovery_case` | stage_code | Read |
| DF-CAS-007 | `recovery_case` | route_state (the resume state on a refusal) | Write |
| DF-CAS-008 | `recovery_case` | route_code | Read |
| DF-CAS-021 | `recovery_case` | rule_version | Read |
| DF-CAS-055 | `recovery_case` | status_before_hold | Write |
| DF-WRK-017 to DF-WRK-026 | `task` | all fields, including task_code, element_type, owner_role, due_at, status, completed_at and outcome_code | Write |
| DF-WRK-027 to DF-WRK-036 | `timer` | all fields, including timer_type, started_at, expires_at, status and escalation_level | Write |
| DF-WRK-043, DF-WRK-044 | `timer` | escalated_to_role, escalated_at | Write |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` | LOV-CASE-STATUS, LOV-ELEMENT, LOV-TASK-STATUS, LOV-TIMER and LOV-ROLE versions in force | Read through the reference-data contract |
| DF-REF-132 to DF-REF-158 | `parameter_catalog`, `parameter_value` | the case-side switch; the approval route and service level rows read by `rwb-decision` | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | all fields of the case status change | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_case` | the `CaseStateChanged` row and the record row | Write |

No row of the approval table, the delegation limit table or the decision log entry is copied into `rwb_case`: `approval` and `decision_log_entry` are `rwb-decision`'s (P7) and `delegation_limit` is `rwb-access`'s (P4), and their fields DF-DEC-032 to DF-DEC-053 and DF-REF-018 to DF-REF-025 arrive only as facts in the approval events. Field IDs are those in the Logical Data Model and Data Dictionary v8.

The task shape this story assumes is Not specified in the source documents (GAP-0732; ASM-1297): TSD P3 v3 T3.1 gives `task_code`, `element_type`, `owner_role`, `due_at`, `status`, `completed_at` and `outcome_code`, and no column of its own for the approval reference or the approval level.

### 12. Contract

#### 12.1 REST operations provided

None new in this story. The waiting status and the decision task are read through the case service's existing case contract: `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/me/tasks` on base `/api/recovery/case/v1`, owner rwb-case (P3), with Case record R and the scope applied, refusing with 401, 403 (MSG-P4-002), 404 (MSG-P4-003) and 503. The work list omits a decision task whose preparer is the caller. This story changes no request, response or error shape; the fields it fills are `status` on the case and `taskCode`, `elementType`, `ownerRole`, `dueAt` and `status` on the task.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 | The cached role, scope and right decision behind the case and task reads (DP-08) | One hop, 2 s (DP-11) |

`rwb-decision` is reached by event, not by REST: this story calls no approval endpoint. The one operation it consumes is `POST /api/recovery/access/v1/authorise`. The parameters and reference-data contracts of DP-06 and DP-07 are read in process through their client libraries, not over REST.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | caseId | caseId, fromStatus, toStatus, eventCode, approvalRef |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | caseId | the hash-chained record of the case status change |

CloudEvents 1.0 envelope; no personal data in either payload. A refusal, a return and an escalation publish no event of their own: each is the one `CaseStateChanged` written when the status changes, and nothing when it does not.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision.ApprovalRequested.v1` (EV-09) | `rwb.decision.events.v1` | P7 | Case router, inbox dedupe, `signalWithStart` of `CaseWorkflow`, then `openApprovalTask` (open or reassign) |
| `rwb.decision.ApprovalDecided.v1` | `rwb.decision.events.v1` | P7 | Case router, inbox dedupe, then `applyApprovalDecision` |

`TimerBreached` (EV-19) and `JOB-05` stay legacy references: in the target the approval service level is a durable timer inside the workflow that owns the approval, and its breach reaches the case as a new `ApprovalRequested` with a higher escalation level. The escalation event type is Not specified in the source documents (GAP-0732; ASM-1299).

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `CaseWorkflow` | Parent workflow, one per case, workflow ID = case ID | `rwb-case` | Forwards the approval request and the decision to its activities; Continue-As-New at each stage end and at least every 28 days |
| `openApprovalTask` | Activity | `rwb-case` | Opens or reassigns the decision task, writes the timer projection and the status, with the decision record and the outbox in one transaction |
| `applyApprovalDecision` | Activity | `rwb-case` | Closes the decision task, stops the timer, writes the status and the resume state, opens the preparer task on a return, with the record and the outbox in one transaction |
| `RecordAndApply` | Activity, from the kit | `rwb-case` | Writes the state change, the local decision record and the outbox rows in one transaction |

`ApprovalWorkflow` and the DoA lookup are `rwb-decision`'s and `rwb-access`'s; this story neither starts nor signals them.

#### 12.6 Schedules

None for this story. The approval service level is not a case Schedule: it is a durable timer in the approval workflow, and the `timer` row is the projection read by `GET /cases/{caseId}/timers`. JOB-05 is a legacy reference only.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `recovery_case` | P3 (`rwb_case`) | Status, route state on a refusal, status before hold, optimistic lock version |
| `task` | P3 (`rwb_case`) | The decision task and, on a return, the task for the preparer |
| `timer` | P3 (`rwb_case`) | The service level projection with its escalation level and escalated role |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | Status, element type, task status, timer type and role lists, read through the contract |
| `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | The case-side switch and the approval parameters, read through the contract |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_case` | Outbox, inbox and idempotency objects (DP-09) |
| `assignment` | P3 (`rwb_case`) | Not written: a decision task is owned by a role, not by a person |

`approval` and `decision_log_entry` are `rwb-decision`'s and `delegation_limit` is `rwb-access`'s; no table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision approval WireMock | RWB-P7-E2013-CON | `ApprovalRequested` for approval "A-1" of AC1, for "A-2" with reason NO_HOLDER and for "A-3" with status HELD_NO_LIMIT; the re-request of "A-1" with escalation level 1; `ApprovalDecided` with APPROVED, REFUSED with route state DECLINED_BY_APPROVER_SET under R-SET-07, and RETURNED |
| decision-record fake | RWB-PLT-E1027-CON | The local record write and the publish on `rwb.decision-record.v1` |
| authorise fake | RWB-PLT-E1037-CON | The right decision behind the case and task reads, including the refusal for a role without Case record R |
| parameters and reference-data fakes | RWB-P3-E1042-CON, RWB-P3-E1043-CON | The status, element type, task status, timer type and role lists with their versions, and the case-side switch |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (2 existing case reads used), consumed 1 | The authorise call of DP-08; no approval endpoint |
| Kafka | Published 1 event and 1 decision record; consumed 2 events | `rwb.case.events.v1` and `rwb.decision-record.v1` published; `rwb.decision.events.v1` consumed |
| Temporal | 1 workflow, 3 activities | `CaseWorkflow` with `openApprovalTask`, `applyApprovalDecision` and `RecordAndApply` |
| File | None | No file input or output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `case/approval`, Java package `th.co.scb.ace.workbench.recovery.case.approval`.

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

The single legacy in-process interface the DP-11 row replaces is the synchronous `ApprovalRouter.request` call of the monolith: the approval arrives as a Kafka fact through RWB-P7-E2013-CON and the mockable boundary is the event, not a Java call. DP-08's contract dependency RWB-P4-E1037-CON is carried by the guard library's own contract (H RWB-PLT-E1037-CON) in this story's dependency list; the build-time C dependency recorded on the story is the approval contract RWB-P7-E2013-CON.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ApprovalRequestListener | Kafka consumer with the inbox | Reads `ApprovalRequested` and `ApprovalDecided`, deduplicates by event ID, calls `signalWithStart` on `CaseWorkflow` |
| OpenApprovalTaskActivity | Temporal activity | Status check, reference-list read, task open or reassign, timer projection, status and route state, record and outbox in one transaction |
| ApplyApprovalDecisionActivity | Temporal activity | Final call mapping, task close, timer stop, status and route state, preparer task on a return, record and outbox in one transaction |
| ApprovalTaskService | Service | The shared logic behind both activities: one open decision task per case, no task for a held-no-limit item, no task for a closed case, and no decision task shown to its own preparer |
| CaseApprovalRepository | Repository | `task`, `timer`, `recovery_case` in schema `rwb_case`, with the version lock; no foreign table |
| StatusCatalog | Service | Reads LOV-CASE-STATUS, LOV-ELEMENT, LOV-TASK-STATUS, LOV-TIMER and LOV-ROLE through the reference-data contract; no Java enum of statuses or element types |
| AccessCheckClient | Client | The cached authorise decision of DP-08 behind the case and task reads |
| CaseTimerProjection | Service | Writes and updates the `timer` row so `GET /cases/{caseId}/timers` shows the approval clock and its escalation level |

**Database and migrations**

- Writes `task` (the decision task and the preparer task on a return), `timer` (the service level projection), `recovery_case` (`status`, `route_state`, `status_before_hold`, `version`), the inbox `processed_event` and the outbox.
- Update `recovery_case` with `WHERE id = ? AND version = ?`; zero rows updated means the record changed (MSG-GEN-004).
- Constraint: partial unique index `ux_task_open_decision ON task (case_id) WHERE element_type = 'DECISION_TASK' AND status IN ('OPEN','IN_PROGRESS')`, so a case in `WAITING_APPROVAL` has exactly one open decision task (BR13).
- Constraint: partial unique index `ux_timer_open_approval ON timer (case_id, timer_type) WHERE status = 'RUNNING' AND timer_type = 'SERVICE_LEVEL'`, so an escalation updates the running row instead of adding a second one.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V2013_1__case_approval_task.sql` creates the two partial unique indexes and adds the approval reference column the task shape needs; the task shape is Not specified in the source documents (GAP-0732; ASM-1297), so the column is written from the assumed shape and renamed at the contract review if the shape differs.

**Configuration and reference data**

- LOV-CASE-STATUS (`WAITING_APPROVAL`, `IN_PROGRESS`, `ON_HOLD`), LOV-ELEMENT (`DECISION_TASK`, `HUMAN_TASK`), LOV-TASK-STATUS (`OPEN`, `DONE`, `CANCELED`), LOV-TIMER (`SERVICE_LEVEL`) and LOV-ROLE through the reference-data contract of DP-07 (RWB-P3-E1043-CON).
- The approval route and service level parameters of section 3 are parameter rows of this service's catalog under the R-PREC default ruling, loaded and owned by RW-COE through RWB-P3-E1042-CON and read by `rwb-decision`; their values are the DL22 open items and this story sets none of them.
- The database login is the rwb-case login (DP-02): Not specified in the source documents (GAP-0732; ASM-1295).

**Build steps**

1. `ApprovalRequestListener` with the inbox, the dedupe by event ID and `signalWithStart`; tests for a repeated event and for X11.
2. `StatusCatalog` over the reference-data contract; test that a new status or element type value is accepted as data with no code change.
3. `OpenApprovalTaskActivity` with the status check, the task and timer writes and the status change in one transaction; tests for AC1, AC11 and AC14, for the preparer not seeing the task and for X10.
4. `ApplyApprovalDecisionActivity` for APPROVED, REFUSED and RETURNED, with the resume state, the preparer task and the timer stop; tests for AC5, AC8 and AC9.
5. The reassignment path for an escalated request: task owner role, due time and timer escalation fields; test for AC2 with a fixed clock.
6. The partial unique indexes and the version lock; test that a second decision on one approval changes the case once.
7. The contract-fake run of both events in isolation, so the story builds before the approval story exists in the environment.
8. The denial test through the guard library for a role without Case record R; test TC-E2-013-15.
9. The decision-record failure path: the record is written last in the transaction and a failure changes nothing; test TC-E2-013-16.

**Feature switch.** The legacy flag name `rwb.decision.approval-routing` is kept as the legacy reference; it was the flag of the approval capability, which now sits in `rwb-decision`. In the target the case-side switch is a parameter read through the parameters contract of DP-06: off means the case router does not subscribe to `rwb.decision.events.v1`, no decision task is opened and no case status is moved, while the approvals themselves keep running.

**Done when.** The tests in section 16 pass, a case enters and leaves `WAITING_APPROVAL` once per approval in SIT, every case in `WAITING_APPROVAL` has exactly one open decision task with its due time, an escalation changes the task and the timer and no status, and every case status change carries a local decision record naming the approval reference, the approval level and the limit version.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P3-005 | The case cannot move to the status the event asks for | This case cannot move to {state} from {current}. | This story, on the case |
| MSG-P4-002 | Read without Case record R | You cannot {action} here. Your role does not include it. | This story, through the guard |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the case |
| MSG-P7-001 | Approval above the caller's level | This needs approval at level {level}. It has been sent to {approver}. | `rwb-decision` |
| MSG-P7-002 | Preparer tries to approve | You prepared this decision, so you cannot approve it. | `rwb-decision` |
| MSG-P7-004 | Approved | Approved. The case moves to {state}. | `rwb-decision`, with the case state filled from this story's outcome |
| MSG-P7-005 | Change from the recommendation without a coded reason | Enter the reason you are not following the recommendation. | `rwb-decision` |
| MSG-P7-010 | No limit covers the decision and product | No approval limit covers {decision} for {product}. The item is held and Risk has been told. | `rwb-decision` |
| MSG-P7-011 | Item escalated to a new approver | {decision} on case {caseNo} passed its service level and is now with you for approval. | `rwb-decision` |
| MSG-GEN-001 | Reason, resolution reference or members present missing | Enter {field}. | `rwb-decision` |
| MSG-GEN-004 | Item changed by another approver | Someone else changed this record. Reload it to see their change. | `rwb-decision`, and this story on a stale case record |

For MSG-P3-005 the {state} value is the LOV-CASE-STATUS value the event asks for and {current} is the case status in force. Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request; the event path answers no caller, it records the error on the activity and lets the retry policy act.

### 15. Screens and states

The approval queue SCR-10 and the decision screen SCR-11 are `rwb-decision`'s and are not built here. On the case side three screens show this story's states, through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON):

| Screen | State | What the user sees |
|---|---|---|
| SCR-02 Case list | List, filtered | The case with status `WAITING_APPROVAL` and the time it has waited, read from the case and its timer |
| SCR-03 Case record | Read only | The status `WAITING_APPROVAL`, the route state, the open decision task with its role and due time, and the approval reference |
| SCR-01 My work | List, empty | The decision task on the approver's work list with the case number, the decision code and the due time; empty when nothing waits |

The composite route, its field list and the field-level masking of the case and task model are Not specified in the source documents (GAP-0732; ASM-1296); the full case record view is RWB-P3-E1023-APP and the approver queue is RWB-E2-014.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-013-01 | AC1, BR2 | End to end | Synthetic demand notice under R-LIT-03 |
| TC-E2-013-02 | AC2, BR7 | End to end | Approval timer breached at 09:00 next day |
| TC-E2-013-03 | AC3, BR1 | End to end | Delegation versions DOA-2026.11 and DOA-2027.01 |
| TC-E2-013-04 | AC4, BR1 | End to end | D6.4 Mortgage at 2.4 million baht |
| TC-E2-013-05 | AC5, BR3, BR10 | End to end | L6 holder approving |
| TC-E2-013-06 | AC6, BR4 | End to end | Preparer who is also a substitute |
| TC-E2-013-07 | AC7, BR5 | End to end | Principal changed to 120 million baht |
| TC-E2-013-08 | AC8, BR6 | End to end | Refuse without and with a reason |
| TC-E2-013-09 | AC9, BR6 | End to end | Return with a question |
| TC-E2-013-10 | AC10, BR6 | End to end | Change without a reason code |
| TC-E2-013-11 | AC11, BR8 | End to end | SSME L6 row with no holder |
| TC-E2-013-12 | AC12, BR9 | End to end | L3 committee approval with resolution PARC-2026-14 |
| TC-E2-013-13 | AC13 | End to end | Holder and substitute approving at once |
| TC-E2-013-14 | AC14, BR11 | End to end | Hire purchase with no delegation rows |
| TC-E2-013-15 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E2-013-16 | Principle 5 | NFR | The decision log write forced to fail during an approval |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR. The whole legacy set is kept in this story because the case-side build carries the key's test set; the tests of AC3, AC4, AC6, AC7, AC10, AC12 and AC13 exercise the approval side in `rwb-decision` and use this story's case assertions where they apply.

### 17. Guardrails

- No business value in code: status names, element types, task statuses, timer types and role codes are data in the reference lists; route and service level values are parameter rows (BR-P3-006).
- No personal data in logs, tests, workflow history, event payloads or prompts. The story reads and writes user references and case numbers only; the approver, the preparer and the holders enter as user references, never as names. Workflow payloads pass the payload codec of the kit.
- No read of another service's tables (DP-01): the approval arrives as an event, the DoA table and the level stay in `rwb-access` and `rwb-decision`, and no `approval`, `delegation_limit` or `decision_log_entry` row is copied into `rwb_case`.
- ACE data only through the owner's contract or its own `v_ace_*` views: this story reads no ACE data at all and links the case to its accounts by business key.
- One writer for the case status: only `rwb-case` writes `recovery_case.status`. Neither the approval request nor the decision writes it, so the DoA lookup and the approver's call can never leave the case in a state of their own.
- A case status change, its task and timer change, its local decision record and its outbox row commit in one transaction (R-UNI-39); a failure changes nothing.
- The decision task is idempotent twice over: the inbox on the event and the one-open-decision-task index on the case.
- The feature switch removes the capability without a schema rollback, and it never blocks the approval itself, which runs in `rwb-decision`.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-001 | Route to the approver named by the delegation table | Epic 2, 3.7; Program, 5.7 | FEAT-APD-01, FEAT-APD-10 | 17 Run the decision center | BR1, BR2 | TC-E2-013-01, TC-E2-013-04 |
| REQ-APD-003 | Accept, change, reject or return, each recorded | Epic 2, 3.7; Program, 5.7 | FEAT-APD-02, FEAT-APD-03, FEAT-APD-04 | 17 Run the decision center | BR3, BR6 | TC-E2-013-05, TC-E2-013-08, TC-E2-013-09 |
| REQ-APD-004 | Above the limit refused and raised, no silent approval | Epic 2, 3.7; Program, 5.7 | FEAT-APD-05 | 17 Run the decision center | BR4, BR5 | TC-E2-013-06, TC-E2-013-07 |
| REQ-APD-005 | Override needs a coded reason | Epic 2, 3.7; Program, 5.7 | FEAT-APD-07 | 17 Run the decision center | BR6 | TC-E2-013-10 |
| REQ-APD-007 | Unanswered approval escalates to the named role | Epic 2, 3.7; Program, 5.7 | FEAT-APD-06 | 17 Run the decision center | BR7 | TC-E2-013-02 |
| REQ-APD-008 | Committee decision recorded with members present | Epic 2, 3.7; Program, 5.7 | FEAT-APD-07 | 17 Run the decision center | BR9 | TC-E2-013-12 |
| REQ-APD-009 | Limit, rule version and approver written with every approval | Epic 2, 3.7; Program, 5.7 | FEAT-APD-11 | 17 Run the decision center | BR10, BR12 | TC-E2-013-05, TC-E2-013-13, TC-E2-013-16 |
| REQ-APD-010 | Open items keep the delegation version they were decided under | Epic 2, 3.7; Program, 5.7 | FEAT-APD-10 | 17 Run the decision center | BR1 | TC-E2-013-03, TC-E2-013-14 |
| REQ-APD-011 | Routing escalates rather than stalls with no person in a role | Epic 2, 3.7; Program, 5.7 | FEAT-APD-06 | 17 Run the decision center | BR8 | TC-E2-013-11 |

| Legacy reference | Where it is kept |
|---|---|
| Case statuses "Waiting approval" and "In progress" | Metadata, sections 4, 9, 15 |
| Status the rule names on a refusal | Sections 4, 8, 9, 11 |
| Decision task per case and escalation on a breach | Sections 4, 5, 7, 9, 13 |
| MSG-P3-005, MSG-P4-002, MSG-P7-001 to MSG-P7-005, MSG-P7-010, MSG-P7-011, MSG-GEN-001, MSG-GEN-004 | Section 14, exception paths |
| Rule IDs R-UNI-20, R-UNI-21, R-UNI-30, R-UNI-39, R-UNI-42, R-SET-07 | Sections 4, 5, 8, 9 |
| Delegation version DOA-2026.11, holders and roles RW-PRODHEAD, RW-RESTRUCT, RW-LITOFF, RW-HEADLIT | Background, AC1, AC2, AC5, AC8, AC9, AC11 |
| Legacy key RWB-E2-013, story RWB-P3-E2013-APP, contract RWB-P7-E2013-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The approval record, the delegation of authority lookup, the approval decision endpoints, the approval queue SCR-10 and the decision screen SCR-11 (the P7 slice of this legacy key under RWB-P7-E2013-CON; the first use of the full approval with a notice is RWB-E2-014).
- The DoA table, roles, scope and masking as data (`rwb-access`, P4); the right decision behind the case reads is inherited from the guard library.
- The committee pack screen SCR-12 with each member's vote (Epic 4).
- The recommendation with reasons and expected return by route (Epic 4, the `rwb-decision` recommendation read).
- The monthly override reason report (Epic 8) and the reporting of approvals (rwb-reporting).
- The case record view in full (RWB-P3-E1023-APP) and the case timer read (its own story).
- The contract document, its event schemas and its fakes (RWB-P7-E2013-CON).
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
- The other slices of RWB-E2-013 in `rwb-decision`, `rwb-access`, `rwb-comms`, `rwb-treatment` and the wave-2 integration harness.
