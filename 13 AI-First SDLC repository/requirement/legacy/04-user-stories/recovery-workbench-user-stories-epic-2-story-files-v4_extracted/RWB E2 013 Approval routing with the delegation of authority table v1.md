<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 013 Approval routing with the delegation of authority table v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 013 Approval routing with the delegation of authority table v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-013 Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-013 |
| Epic | E2, release 31 December 2026 |
| Module | P7 Decision center and log |
| Feature | FEAT-APD-01 Route a recommendation to the approver by limit; FEAT-APD-02 Approve inside the limit; FEAT-APD-03 Change a recommendation before approving; FEAT-APD-04 Reject a recommendation with a reason; FEAT-APD-05 Escalate above the limit; FEAT-APD-06 Escalate an overdue approval; FEAT-APD-07 Record an override with a coded reason; FEAT-APD-09 Show the approval queue; FEAT-APD-10 Apply the delegation of authority limits; FEAT-APD-11 Record the outcome of an approved decision |
| Requirement IDs | REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010, REQ-APD-011 |
| BRD section | Business Requirements Epic 2, section 3.7; Business Requirements Program, section 5.7 |
| L3 process | 17 Run the decision center |
| Decision | D7.1 |
| Priority | Must |
| Depends on | RWB-E1-038, RWB-E1-028, RWB-E1-027, RWB-E1-037 |
| Status | Ready for build |

## 1. Story

As an **approver, for example a product head (RW-PRODHEAD)**, I want **every decision that needs approval routed to the approval level the delegation of authority table names, or to the role named for a decision with no amount limit, with one queue of what waits on me and escalation when an item passes its service level**, so that **the right person approves within the limit, nobody approves their own decision, and no item waits unseen**.

## 2. Business rationale

Approval and authority governance is an audit finding: approvals today are given by e-mail, sometimes above the approver's limit or by the person who prepared the decision. This story routes each approval by the versioned delegation table (RWB-E1-038), records the limit, the rule version and the approver with every outcome, refuses an approval above the caller's limit or by its preparer, and escalates rather than stalls when the service level passes or no holder exists. It meets REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010 and REQ-APD-011 and puts controls CTL-04, CTL-05 and CTL-07 in place. The measure is decisions within the delegation of authority: target 100 percent.

## 3. Preconditions

- RWB-E1-038 is done: delegation version DOA-2026.11 is in force and the lookup returns the lowest covering level; holders and substitutes are named test users in SIT and UAT (DL18).
- RWB-E1-028 is done: the P3 timer engine starts service level timers, and JOB-05 publishes EV-19 TimerBreached.
- RWB-E1-027 is done: the decision log writer; RWB-E1-037 is done: the permission matrix and scope.
- Approval route parameters are in the catalog for each decision with no amount limit, for D7.1 notices: rwb.approval.route.D7.1.area=LITIGATION, rwb.approval.route.D7.1.role=RW-LITOFF, rwb.approval.route.D7.1.escalation-role=RW-HEADLIT, rwb.approval.route.D7.1.service-level=1 working day (assumed; DL22).
- Service level for limit-based approvals: rwb.approval.service-level.default=3 working days (assumed from the 3 working day approval timers in R-RES-10 and R-SET-05; DL22).
- Capability area per decision code: D5 and D6.x Treatment and offer, D7.x Litigation, D8.2 and D8.3 Asset and disposal, D8.4 Debt sale, D9.x Write-off and posting (parameters rwb.approval.area.<code>).
- LOV-OVERRIDE-REASON is loaded with the coded override reasons (owner RW-COE; new list, recorded in the additions file).

## 4. Flow

1. Calling module (for example the litigation route after R-LIT-03 generates a notice): calls ApprovalRouter.request with the case, decision, regulation item, product, amounts, preparer, source reference and the rule ID and version that asked for approval.
2. Workbench (ApprovalRoutingService): for a decision with delegation rows, calls DelegationOfAuthority.lowestLevel and assigns the item to the holder of that level; for a decision with no amount limit, assigns it to the route role from the parameters.
3. Workbench: where the level has no holder and no substitute, moves the item one level up at once and records why; where the lookup returns NOT_COVERED, holds the item and raises the incident.
4. Workbench: stores the approval with status WAITING, the level, the delegation row and version, and the due time; asks P3 to open the decision task and start the service level timer; writes the routing entry to the decision log; publishes EV-09 ApprovalRequested.
5. Approver: opens SCR-10 Approval queue (GET /approvals) and sees the items waiting on them with decision, amount, level, limit and age.
6. Approver: approves, changes and approves, refuses or returns the item through the approval endpoints.
7. Workbench (ApprovalDecisionService): checks the A letter in the decision's capability area, the caller's level against the required level, that the caller did not prepare the item, the reason or coded reason where needed, and the record version.
8. Workbench: writes the decision entry with approver, approval level, limit version, rule ID and version and final call; sets the approval status; publishes EV-08 DecisionRecorded; P3 moves the case from Waiting approval to In progress and the source module acts (for a notice, release to dispatch, RWB-E2-014).
9. Workbench (ApprovalEscalationListener): on EV-19 TimerBreached for an approval, moves the item one level up, or to the escalation role for a role-routed item, restarts the timer, writes the escalation entry and tells the new approver.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The service level passes with no action | The item moves to the next level up or the escalation role; the case does not move; entry written | MSG-P7-011 | AC2 |
| X2 | The caller prepared the decision | Refused with 409 | MSG-P7-002 | AC6 |
| X3 | A change raises the amount above the caller's level | Not approved; the item is sent to the level that covers it | MSG-P7-001 | AC7 |
| X4 | Refuse or return without a reason | Refused with 422 | MSG-GEN-001 | AC8 |
| X5 | A change departs from the recommendation without a coded reason | Refused with 422 | MSG-P7-005 | AC10 |
| X6 | The required level has no holder and no substitute | The item moves one level up at once; it never waits on nobody | MSG-P7-011 | AC11 |
| X7 | A committee level is approved without a resolution reference or the members present | Refused with 422 | MSG-GEN-001 | AC12 |
| X8 | Two approvers act on one item at once | One succeeds; the other gets 409 and writes nothing | MSG-GEN-004 | AC13 |
| X9 | No delegation row covers the decision and product | The item is held; incident to Risk | MSG-P7-010 | AC14 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the delegation lookup (RWB-E1-038), timers (RWB-E1-028), the writer (RWB-E1-027) and the matrix (RWB-E1-037) |
| Negotiable | Levels, holders, route roles, service levels and override reasons are data |
| Valuable | Every Epic 2 approval follows the delegation table and is recorded with its limit |
| Estimable | One router, one decision service, one escalation listener, one queue screen |
| Small | Fits in two weeks with its tests; the notice screen is RWB-E2-014 |
| Testable | Each criterion below is one test in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Approval routing with the delegation of authority table

  Background:
    Given the environment is SIT
    Given delegation version "DOA-2026.11" is in force with holder "U-9201" at L6, "U-9202" at L5 and "U-9203" at L4 for MORTGAGE, all holding RW-PRODHEAD
    Given test user "U-9210" holds RW-RESTRUCT and test users "U-9211" and "U-9212" hold RW-LITOFF and test user "U-9213" holds RW-HEADLIT

  Scenario: AC1 Routed
    Given a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211"
    When the router runs for decision D7.1 at 09:00 on 14 December 2026
    Then an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026
    Then the system does not show it to "U-9211", who prepared it
    Then the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role"
    Then the case status becomes "Waiting approval"

  Scenario: AC2 Escalated
    Given the approval of AC1 is still WAITING at 09:00 on 15 December 2026
    When JOB-05 publishes TimerBreached for its service level timer
    Then the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026
    Then the system writes one entry with final call "ESCALATED" and "U-9213" is told with MSG-P7-011
    Then the case stays "Waiting approval"

  Scenario: AC3 Limit changed
    Given approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11"
    Given version "DOA-2027.01" from 1 January 2027 moves that amount to L5
    When a new D6.4 approval with the same amounts routes on 2 January 2027
    Then the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01"
    Then approval "A-1" stays with L6 and "DOA-2026.11"

  Scenario: AC4 Routed by limit
    Given restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00
    When the router runs
    Then the system assigns the approval to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11"
    Then GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age

  Scenario: AC5 Approve inside the limit
    Given the approval of AC4 is WAITING
    When "U-9201" approves it with Idempotency-Key "k-501"
    Then the approval status becomes "APPROVED"
    Then the system writes one entry with approver "U-9201", approval level "L6", limit version "DOA-2026.11", the rule ID and version and final call "APPROVED"
    Then the system publishes decisionRecorded and the response shows MSG-P7-004 with state "In progress"

  Scenario: AC6 The preparer cannot approve
    Given "U-9210" also holds RW-PRODHEAD at L6 as substitute
    When "U-9210" approves the approval of AC4
    Then the system refuses the call with status 409 and message MSG-P7-002 and the approval stays "WAITING"

  Scenario: AC7 A change above the limit goes up
    Given the approval of AC4 is WAITING with "U-9201"
    When "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves
    Then the call returns MSG-P7-001 with level "L5" and approver "U-9202"
    Then the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded

  Scenario: AC8 Refuse needs a reason
    Given the approval of AC4 is WAITING
    When "U-9201" refuses it with no reason
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "reason"
    Then when "U-9201" refuses it with reason "Collateral appraisal older than one year"
    Then the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names

  Scenario: AC9 Return with a question
    Given the approval of AC4 is WAITING
    When "U-9201" returns it with reason "Attach the latest income statement"
    Then the system opens the status becomes "RETURNED", a task for preparer "U-9210", and the entry records the question

  Scenario: AC10 An override needs a coded reason
    Given the recommendation on the approval of AC4 is a settlement of 1,920,000.00
    When "U-9201" changes it to 1,800,000.00 and approves with no reason code
    Then the system refuses the call with status 422 and message MSG-P7-005

  Scenario: AC11 No holder means escalation, not a stall
    Given the L6 row for SSME has no holder and no substitute
    When an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes
    Then the system assigns it to the L5 holder at once
    Then the routing entry records reason "NO_HOLDER" for L6

  Scenario: AC12 A committee level needs the resolution
    Given an approval for D6.4 item 2.1.1, MORTGAGE, principal 800,000,000.00, loss 20.00 percent, routed to L3, Problem Asset Resolution Committee, whose recording holder is "U-9204"
    When "U-9204" approves it with no resolution reference
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "resolutionReference"
    Then when "U-9204" approves with resolution reference "PARC-2026-14" and members present "M-01, M-02, M-03, M-04"
    Then the entry records the resolution reference, the members present, level "L3" and final call "APPROVED"

  Scenario: AC13 Two approvals at once
    Given the approval of AC4 is WAITING and visible to holder "U-9201" and substitute "U-9205"
    When both approve it at the same moment
    Then one call succeeds and one entry is written
    Then the other call returns status 409 with message MSG-GEN-004

  Scenario: AC14 No limit covers the decision
    Given "DOA-2026.11" holds no row for HIRE_PURCHASE
    When an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes
    Then the system stores the approval with status "HELD_NO_LIMIT" and the case stays "Waiting approval"
    Then the system raises an incident to RW-RISK with message MSG-P7-010
```

## 8. Business rules

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

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| In progress | Recommendation routed for approval | Approval stored WAITING or HELD_NO_LIMIT | Waiting approval |
| Waiting approval | Approver accepts | Caller within the required level, not the preparer | In progress |
| Waiting approval | Approver changes and accepts | Changed terms within the caller's level, coded reason given | In progress |
| Waiting approval | Approver rejects | Reason given | In progress, at the state the rule names |
| Waiting approval | SLA_BREACHED (R-UNI-30) | Service level timer breached | Waiting approval, with the next approver |

The approval record moves WAITING to APPROVED, REFUSED or RETURNED, and stays WAITING with a new approver on escalation or on a change above the limit.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| Holders and substitutes of levels L4 to L6 (named per DL18) | Approve, change, refuse or return items at their level in the Workbench |
| Recording holder of levels L1 to L3 | Records the committee resolution with its reference and members present |
| RW-LITOFF Litigation officer, RW-LEGAL Legal counsel, RW-HEADLIT Head of Litigation | Approve D7.x items routed to their role (Litigation A) |
| RW-PRODHEAD Product head | Approves items of their product at their level (A in Treatment and offer, Litigation, Asset and disposal, Debt sale, Write-off and posting) |
| RW-RESTRUCT, RW-CREDCOMM | Approve Treatment and offer items at their level (A) |
| RW-SALEOFF, RW-HEADNPA, RW-HEADASL, RW-DEBTSALE | Approve Asset and disposal or Debt sale items at their level (A) |
| RW-CREDITAD, RW-WOCOMM, RW-FINANCE | Approve Write-off and posting items at their level (A) |
| Preparer of an item | May not approve it |
| SY-RULES, SY-CASEWF | Call the router (Decision log C) |
| RW-AUDIT | Reads approvals through the decision log |
| Approval levels | L1 Board of Directors to L6 Recovery executive, department level, per doa.txt |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-032 | approval | id | Write |
| DF-DEC-033 | approval | case_id | Write |
| DF-DEC-034 | approval | decision_code | Write |
| DF-DEC-035 | approval | regulation_item | Write |
| DF-DEC-036 | approval | capability_area | Write |
| DF-DEC-037 | approval | route_role_code | Write |
| DF-DEC-038 | approval | approval_level | Write |
| DF-DEC-039 | approval | delegation_limit_id | Write |
| DF-DEC-040 | approval | limit_version | Write |
| DF-DEC-041 | approval | product_group | Write |
| DF-DEC-042 | approval | amount | Write |
| DF-DEC-043 | approval | terms | Write |
| DF-DEC-044 | approval | prepared_by | Write |
| DF-DEC-045 | approval | assigned_user_id | Write |
| DF-DEC-046 | approval | status | Write |
| DF-DEC-047 | approval | due_at | Write |
| DF-DEC-048 | approval | escalation_level | Write |
| DF-DEC-049 | approval | source_type | Write |
| DF-DEC-050 | approval | source_ref | Write |
| DF-DEC-051 | approval | rule_id | Write |
| DF-DEC-052 | approval | rule_version | Write |
| DF-DEC-053 | approval | decision_log_id | Write |
| DF-REF-018 | delegation_limit | approval_level | Read through the P4 DelegationOfAuthority interface |
| DF-REF-023 | delegation_limit | holder_user_id | Read through the P4 DelegationOfAuthority interface |
| DF-REF-024 | delegation_limit | substitute_user_id | Read through the P4 DelegationOfAuthority interface |
| DF-WRK-019 | task | task_code | Write through the P3 task interface |
| DF-WRK-020 | task | element_type | Write through the P3 task interface |
| DF-WRK-023 | task | owner_role | Write through the P3 task interface |
| DF-WRK-030 | timer | timer_type | Write through the P3 timer interface |
| DF-WRK-032 | timer | expires_at | Write through the P3 timer interface |
| DF-WRK-036 | timer | escalation_level | Read from EV-19 |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (routing, escalation and outcome entries) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/approvals** (API-P7-002)

| Item | Value |
|---|---|
| Request | Query: decision, product, page, size |
| Response | ApprovalPage of Approval: id, caseId, decision, preparedBy, level, amount, status |
| Errors | 401; 403 no A letter in any decision area (MSG-P4-002); 503 (MSG-GEN-006) |
| Authorization | api.yaml declares Decision log A, which no bank role holds; the A letter in the decision's capability area is checked instead (additions file) |
| Idempotency | Not applicable, read only |

**GET /approvals/{approvalId}** (new, additions file): Approval plus regulationItem, limitVersion, ruleId, ruleVersion, dueAt, escalationLevel, sourceType, sourceRef, terms; errors 401, 403, 404 (MSG-P4-003).

**POST /approvals/{approvalId}/approve** (API-P7-003)

| Item | Value |
|---|---|
| Request | ApprovalAction: reason, resolutionReference; added in this story: reasonCode (LOV-OVERRIDE-REASON), changes (the changed terms), membersPresent |
| Response | 200 DecisionLogEntry of the approval |
| Errors | 401; 403 no A in the area or not the holder, substitute or route role (MSG-P4-002); 404 (MSG-P4-003); 409 preparer (MSG-P7-002), above the caller's level (MSG-P7-001, the item has moved), record changed (MSG-GEN-004); 422 missing reason code, resolution reference or members (MSG-P7-005, MSG-GEN-001); 503 entry not written (MSG-P7-003) |
| Authorization | A in the decision's capability area, plus level or route role |
| Idempotency | Idempotency-Key header |

**POST /api/recovery/v1/approvals/{approvalId}/refuse** (API-P7-005): ApprovalAction with reason required; response DecisionLogEntry; errors as approve; Idempotency-Key.

**POST /api/recovery/v1/approvals/{approvalId}/return** (API-P7-004): ApprovalAction with reason required; response Approval with status RETURNED; errors as approve; Idempotency-Key.

**Events:** publishes EV-09 ApprovalRequested (approvalId, caseId, level, amount) and EV-08 DecisionRecorded; consumes EV-19 TimerBreached.

**Published interface ApprovalRouter** (package recovery.decision.approval):

```java
ApprovalRef request(ApprovalRequest request) throws DecisionLogUnavailableException;
// ApprovalRequest: caseId, decisionCode, regulationItem, productGroup, amounts (principal, lossPct, lossAmount, pricePctFmv),
//   recommendation, preparedBy, sourceType, sourceRef, ruleId, ruleVersion, idempotencyKey
```

## 13. Solution plan

- Package: folder `recovery/decision/approval` in the recovery module; Java package `recovery.decision.approval`. Front end: `recovery/decision/approval`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| DecisionCenterAndLogController | Controller | GET /approvals, GET /approvals/{approvalId}, approve, refuse, return |
| ApprovalRouter | Published interface | The request method above |
| ApprovalRoutingService | Service | Lookup or route role, no-holder rule, store, P3 task and timer, routing entry, EV-09 |
| ApprovalDecisionService | Service | BR3 to BR6 and BR9 checks, entry, status, EV-08 |
| ApprovalEscalationListener | Listener | EV-19 for approval timers; next level or escalation role; restart timer; entry; notification |
| ApprovalRepository | Repository | Reads and writes the approval table with optimistic locking |
| Approval | Entity | Maps the new approval table |
| ApprovalQueueScreen | React component | SCR-10 Approval queue: decision, case, amount, level, limit, age, due |

- Database: creates table approval (id uuid, case_id uuid, decision_code varchar(8), regulation_item varchar(10), capability_area varchar(30), route_role_code varchar(20), approval_level varchar(4), delegation_limit_id uuid, limit_version varchar(20), product_group varchar(15), amount numeric(18,2), terms jsonb, prepared_by uuid, assigned_user_id uuid, status varchar(20), due_at timestamptz, escalation_level integer default 0, source_type varchar(20), source_ref varchar(60), rule_id varchar(20), rule_version varchar(20), decision_log_id uuid, plus the standard columns) with Flyway migration V_E2_013__approval.sql; index ix_approval_assignee on (assigned_user_id, status); index ix_approval_role on (route_role_code, status); unique index on (source_type, source_ref) where status in ('WAITING','HELD_NO_LIMIT').
- Configuration and reference data: delegation version (RWB-E1-038; holders DL18); route, area and service level parameters (owner RW-COE; values DL22); LOV-OVERRIDE-REASON (RW-COE); notification template for MSG-P7-011 on the ACE notification path.
- Build steps:
  1. Create the approval migration, entity and repository with optimistic locking.
  2. Build ApprovalRoutingService for limit-based and role-based routes, the no-holder rule and the NOT_COVERED hold; tests for AC1, AC4, AC11, AC14.
  3. Wire the P3 task and timer interfaces and EV-09; test the case status in AC1.
  4. Build ApprovalDecisionService for approve, change, refuse and return with all checks; tests for AC5 to AC10 and AC12.
  5. Add idempotency and the concurrency test for AC13.
  6. Build ApprovalEscalationListener; test AC2 with a fixed clock.
  7. Test the version change for AC3 with two delegation versions.
  8. Build SCR-10 with the loading and list states and the queue endpoint.
- Feature flag: `rwb.decision.approval-routing`.
- Done when: the tests in section 16 pass and CTL-04 and CTL-05 tests (approve above the limit, approve own decision) pass in SIT.

## 14. Validation and messages

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

Thai text for each message follows DL10; proposed Thai for MSG-P7-011 is in the additions file.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-10 Approval queue | Loading | Waits while the items load |
| SCR-10 Approval queue | List | Sees each item waiting on them with decision, case, amount, level, limit version, age and due time; opens an item in SCR-11 |
| SCR-10 Approval queue | Empty (common state) | Sees that nothing is waiting |

SCR-11 Decision screen is built for its first use, the D7.1 notices, in RWB-E2-014.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-013-01 | AC1, BR2 | System | Synthetic demand notice under R-LIT-03 |
| TC-E2-013-02 | AC2, BR7 | System | Approval timer breached at 09:00 next day |
| TC-E2-013-03 | AC3, BR1 | System | Delegation versions DOA-2026.11 and DOA-2027.01 |
| TC-E2-013-04 | AC4, BR1 | System | D6.4 Mortgage at 2.4 million baht |
| TC-E2-013-05 | AC5, BR3, BR10 | System | L6 holder approving |
| TC-E2-013-06 | AC6, BR4 | System | Preparer who is also a substitute |
| TC-E2-013-07 | AC7, BR5 | System | Principal changed to 120 million baht |
| TC-E2-013-08 | AC8, BR6 | System | Refuse without and with a reason |
| TC-E2-013-09 | AC9, BR6 | System | Return with a question |
| TC-E2-013-10 | AC10, BR6 | System | Change without a reason code |
| TC-E2-013-11 | AC11, BR8 | System | SSME L6 row with no holder |
| TC-E2-013-12 | AC12, BR9 | System | L3 committee approval with resolution PARC-2026-14 |
| TC-E2-013-13 | AC13 | System | Holder and substitute approving at once |
| TC-E2-013-14 | AC14, BR11 | System | Hire purchase with no delegation rows |
| TC-E2-013-15 | Access | Access | A role without the right is refused with MSG-P4-002 |
| TC-E2-013-16 | Principle 5 | Resilience | The decision log write forced to fail during an approval |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: levels, limits, holders, route roles, areas, service levels and override reasons are data or parameters.
- No personal data in logs, tests or prompts; members present are recorded as member references, not names.
- No read of another module's tables: delegation through the P4 interface, tasks and timers through P3, source actions through the source module's interface.
- No approval without its decision log entry in the same transaction.
- No item may be assigned to its preparer.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-001 | Route to the approver named by the delegation table | Epic 2, 3.7 | FEAT-APD-01, FEAT-APD-10 | 17 Run the decision center | BR1, BR2 | TC-E2-013-01, TC-E2-013-04 |
| REQ-APD-003 | Accept, change, reject or return, each recorded | Epic 2, 3.7 | FEAT-APD-02, FEAT-APD-03, FEAT-APD-04 | 17 Run the decision center | BR3, BR6 | TC-E2-013-05, TC-E2-013-08, TC-E2-013-09 |
| REQ-APD-004 | Above the limit refused and raised, no silent approval | Epic 2, 3.7 | FEAT-APD-05 | 17 Run the decision center | BR4, BR5 | TC-E2-013-06, TC-E2-013-07 |
| REQ-APD-005 | Override needs a coded reason | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR6 | TC-E2-013-10 |
| REQ-APD-007 | Unanswered approval escalates to the named role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR7 | TC-E2-013-02 |
| REQ-APD-008 | Committee decision recorded with members present | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR9 | TC-E2-013-12 |
| REQ-APD-009 | Limit, rule version and approver written with every approval | Epic 2, 3.7 | FEAT-APD-11 | 17 Run the decision center | BR10, BR12 | TC-E2-013-05, TC-E2-013-13, TC-E2-013-16 |
| REQ-APD-010 | Open items keep the delegation version they were decided under | Epic 2, 3.7 | FEAT-APD-10 | 17 Run the decision center | BR1 | TC-E2-013-03, TC-E2-013-14 |
| REQ-APD-011 | Routing escalates rather than stalls with no person in a role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR8 | TC-E2-013-11 |

## 19. Out of scope

- The decision screen SCR-11 and the D7.1 notice approval with release to dispatch (RWB-E2-014).
- The committee pack screen SCR-12 with each member's vote (Epic 4).
- The recommendation with reasons and expected return by route (Epic 4, API-P7-001).
- The monthly override reason report (Epic 8, FEAT-ADM-08 QA sample; reporting stories).
- Names of level holders and substitutes (DL18) and service level values (DL22).
