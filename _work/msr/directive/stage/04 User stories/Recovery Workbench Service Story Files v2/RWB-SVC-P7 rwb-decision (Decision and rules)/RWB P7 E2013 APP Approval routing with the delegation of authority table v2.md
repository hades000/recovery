# RWB-P7-E2013-APP Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P7-E2013-APP-16) |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P7-X |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P7-E2013-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P7-E1027-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P3-E1028-CON |
| Integration dependencies | None |
| External dependencies | RWB-P7-E2013-OPS (build dependency, not done yet) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-017, FR-P7-018, FR-P7-020, FR-P7-021, FR-P7-022, FR-P7-023, FR-P7-024, FR-P7-025, FR-P7-026, FR-P7-035) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-013 for rwb-decision; the delegation of authority table is read from rwb-access through its contract, the decision record is written through the local decision-record library, and the approval clock and the escalation are Temporal and not JOB-05. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 32 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **approver, for example a product head (RW-PRODHEAD)**, I want **every decision that needs approval in rwb-decision routed to the approval level the delegation of authority table names, or to the role named for a decision with no amount limit, with one queue of what waits on me and escalation when an item passes its service level**, so that **the right person approves within the limit, nobody approves their own decision, and no item waits unseen — while the delegation table stays with its owner in rwb-access and the decision record is written in rwb_decision in the same transaction as the outcome**.

### 2. Business rationale

Approval and authority governance is an audit finding: approvals are given by e-mail, sometimes above the approver's limit or by the person who prepared the decision. In the target this is not one monolith transaction. rwb-access (P4) owns the delegation of authority table and the authorise decision, rwb-case (P3) owns the case, its status, the queue, the tasks and the parameters and reference data, rwb-decision (P7) owns the approval, the routing, the decision record and the central ledger, and rwb-reporting follows the decision-record events (Architecture v5 slides 14, 27, 28 and 41; TSD P7 Decision center and log v2 T3.1 and T3.3). The story therefore reads the limits through the P4 contract and never by a join, records the outcome through the local decision-record library, and holds the service level clock as a durable Temporal timer instead of the retired JOB-05.

This story is the rwb-decision app slice of legacy RWB-E2-013 and it owns all fourteen legacy criteria: AC1 routed, AC2 escalated, AC3 limit versioned, AC4 routed by limit, AC5 approve inside the limit, AC6 the preparer cannot approve, AC7 a change above the limit goes up, AC8 refuse needs a reason, AC9 return with a question, AC10 an override needs a coded reason, AC11 no holder means escalation, AC12 a committee level needs the resolution, AC13 two approvals at once and AC14 no limit covers the decision. Every one of them is a behaviour of this service; the cross-service facts each criterion names — the delegation rows and holders, the case and its parameters, the reference lists — arrive as contract mocks, so the criteria are proved here and not only end to end.

The decoupling is the one the target fixes: the approval is a `rwb_decision` row and no other service reads it (DP-01); the outcome is a local decision record relayed on the shared topic `rwb.decision-record.v1` (DP-03); the route parameters, the capability area per decision and the service levels are parameters of rwb-case (DP-06); LOV-OVERRIDE-REASON, LOV-APPROVAL-LEVEL and LOV-APPROVAL-STATUS are reference data of rwb-case (DP-07); the capability area and the right of the caller are the authorise contract of rwb-access (DP-08); the two events go through the outbox in the same transaction as the state change (DP-09); the service level clock and the escalation are a workflow and its durable timer, not a Quartz row (DP-10); every cross-service call is one hop with a 2 s budget (DP-11); the base is `/api/recovery/decision/v1` (DP-13); the migration is one per-service Flyway step in `rwb_decision` (DP-15); and the queue screen reaches the answer through the gateway-bff composite route (DP-19). It serves REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010 and REQ-APD-011, carries CTL-04, CTL-05 and CTL-07, and gives the FSD P7 measure "decisions within the delegation of authority, 100 percent" its service-side evidence.

### 3. Preconditions

- RWB-P7-E2013-CON is published: the five operations on base `/api/recovery/decision/v1`, the Approval resource, the outcome and authority elements, the escalation fields, the error mapping, the two event envelopes and the fakes, so this story builds against a fixed contract on Day 1.
- The delegation of authority table is in force in rwb-access (P4) with version `DOA-2026.11` on the routing date, and its level lookup returns the lowest covering level; holders and substitutes are named test users in SIT and UAT (DL18). The read is the P4 contract `RWB-P4-E1037-CON` (DP-08, DP-11); the table itself is never read by this service (DP-01).
- The parameters and reference data of rwb-case are live (RWB-P3-E1042-CON, RWB-P3-E1043-CON, DP-06, DP-07): `rwb.approval.route.<decision>.role`, `.escalation-role`, `.area` and `.service-level`, `rwb.approval.service-level.default`, `rwb.approval.area.<code>`, LOV-APPROVAL-LEVEL, LOV-APPROVAL-STATUS, LOV-CAPABILITY, LOV-PRODUCT and LOV-OVERRIDE-REASON.
- The case read of rwb-case is live (RWB-P3-E1028-CON) for the case, its status, its preparer and the source facts of the item; the case status move itself is rwb-case's.
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with RWB-PLT-E1027-CON and the same-service contract RWB-P7-E1027-CON (DP-03); the outbox and inbox library is live with RWB-PLT-TE006-CON (DP-09).
- The Temporal workflow kit, the namespace `rwb-recovery` and task queue `rwb-decision` are live with RWB-PLT-E1071-CON (DP-10), so the approval clock is a durable timer and not the retired JOB-05.
- The `rwb_decision` baseline is in place from RWB-P7-E1008-APP and RWB-P7-E1027-APP: the schema, its login, `decision_log_entry` and the library objects exist and the per-service Flyway sequence runs (DP-15).
- The gateway-bff composite route of RWB-PLT-N001-CON serves the queue screen (DP-19).
- The composite approval-queue route path and its merge order, the harness environment, its seeding of delegation versions, holders and service-level clocks, the evidence format and retention, and the pass/fail gate are held as data in the harness pack, not in this story; the integration lead agrees them with the platform edge owner and with QA at the wave 2 entry check (GAP-0397).
- The DoA lookup and authority decision carry the outcome values COVERED, NO_HOLDER, NOT_COVERED, NO_AMOUNT_LIMIT and RELATED_PARTY, and requiredLevel on a refused authority decision; the request and response field set of section 12 is frozen at the contract review of RWB-P4-E1037-CON (GAP-0929).
- The notice and message operations, their base path and their field sets are Not specified in the source documents (GAP-1222); the rwb-comms contract review fixes them, and the unique key of migration V2013_1 follows the confirmed shape.
- The escalation notice of MSG-P7-011 is one row of the rwb-comms template catalogue with the placeholders {decision} and {caseNo} and a channel from LOV-CHANNEL, in version Approved. Its template code and channel value are Not specified in the source documents (GAP-1220) and are agreed at the wave 2 design review; the story builds against ASM-B-P6-05-E2013-1 until they are loaded. The send retry is read from the platform outbox policy of RWB-PLT-TE006-CON.
- The service level values in force are `rwb.approval.route.D7.1.service-level` = 1 working day and `rwb.approval.service-level.default` = 3 working days, both assumed from DL22 and both data; the number of escalation levels and the behaviour at the last level are Not specified in the source documents (GAP-1253; ASM-2217).
- No build dependency outside rwb-decision and the platform contract stories: the H rows are CON stories; the C rows never block the build (Template and Rules §R5.7).
- No production data is used in any example, fixture or test: every case number, user key, delegation row and amount is synthetic.

### 4. Flow

1. A calling module — the litigation route after R-LIT-03 generates a notice, the treatment route after R-SET-05 prepares a settlement — calls the approval request of this service with the case, the decision, the regulation item, the product group, the amounts, the preparer, the source reference and the rule ID and version that asked for approval.
2. ApprovalRoutingService reads the capability area of the decision code (`rwb.approval.area.<code>`) and asks rwb-access for the lowest covering level of the decision, the product and the amounts on the routing date; for a decision with no amount limit it reads the route role of the parameters instead.
3. Where the level has no holder and no substitute the item moves one level up at once and the routing entry records reason `NO_HOLDER`; where the lookup answers that no row covers the decision and product, the item is stored `HELD_NO_LIMIT` and an incident goes to RW-RISK with MSG-P7-010.
4. The service stores the approval with status `WAITING`, the level, the delegation row reference, the limit version and the due time, starts `ApprovalWorkflow` on task queue `rwb-decision` with the due time as its durable timer input, writes the routing entry through the local decision-record library and publishes `rwb.decision.ApprovalRequested.v1`; the case status move to Waiting approval is asked of rwb-case.
5. The approver opens SCR-10 Approval queue through the gateway-bff composite route and reads `GET /api/recovery/decision/v1/approvals`; each item shows the decision, the amount, the level, the limit version and its age.
6. The approver approves, changes and approves, refuses or returns the item through `POST /approvals/{approvalId}/approve`, `/refuse` and `/return`, each with an `Idempotency-Key`.
7. ApprovalDecisionService checks, in this order: the authorise answer of rwb-access for the capability area of the decision (the A letter), the caller's level against the required level, that the caller is not the preparer, the reason or the coded reason where one is needed, and the record version.
8. The service writes the outcome entry through the local decision-record library with the approver, the approval level, the limit version, the rule ID and version and the final call, sets the approval status, publishes `rwb.decision.DecisionRecorded.v1` and asks rwb-case for the case status the rule names; the source module then acts on its own case (for a notice, release to dispatch in RWB-P7-E2014-APP).
9. When the durable timer of `ApprovalWorkflow` fires, the escalation step moves the item one level up, or to the escalation role for a role-routed item, restarts the timer for the next service level, writes one entry with final call `ESCALATED` and tells the new approver with MSG-P7-011; the case stays Waiting approval.
10. `rwb.access.DoaLimitChanged.v1` refreshes the cached delegation version, so the next routing decision of the day reads the version in force and the version already written on an open approval is unchanged.
11. A repeat of an outcome call with the same `Idempotency-Key` returns the stored answer and writes no second entry; a call with a stale record version answers 409 with MSG-GEN-004.
12. A read of an approval outside the caller's scope or capability area answers 404 with MSG-P4-003 or 403 with MSG-P4-002, and nothing is written.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The service level passes with no action | The item moves to the next level up or the escalation role; the case does not move; one entry is written | MSG-P7-011 | AC2 |
| X2 | The caller prepared the decision | Refused with 409 | MSG-P7-002 | AC6 |
| X3 | A change raises the amount above the caller's level | Not approved; the item is sent to the level that covers it | MSG-P7-001 | AC7 |
| X4 | Refuse or return without a reason | Refused with 422 | MSG-GEN-001 | AC8 |
| X5 | A change departs from the recommendation without a coded reason | Refused with 422 | MSG-P7-005 | AC10 |
| X6 | The required level has no holder and no substitute | The item moves one level up at once; it never waits on nobody | MSG-P7-011 | AC11 |
| X7 | A committee level is approved without a resolution reference or the members present | Refused with 422 | MSG-GEN-001 | AC12 |
| X8 | Two approvers act on one item at once | One succeeds; the other gets 409 and writes nothing | MSG-GEN-004 | AC13 |
| X9 | No delegation row covers the decision and product | The item is held; incident to RW-RISK | MSG-P7-010 | AC14 |
| X10 | The rwb-access delegation read does not answer inside 2 s | The item is not assigned, nothing is stored as covered, and the call answers 503 | MSG-GEN-006 | AC4, AC5 |
| X11 | The decision record cannot be written | The outcome does not take effect: status unchanged, no event, incident raised under R-UNI-39 | MSG-P7-003 | AC5 |

X10 and X11 are the two failure paths the target adds to the legacy table: a missing delegation answer never produces a silent approval, and an outcome that cannot be recorded does not stand (Principle 5, R-UNI-39). Both are proved by their own tests in section 16.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P7-E2013-CON, the decision-record library and the platform contracts; the delegation of rwb-access, the case, the parameters and the lists arrive as contract fakes from the first run |
| Negotiable | Levels, holders, route roles, areas, service levels, override reasons and the escalation roles are data; the story fixes the routing order and the outcome checks |
| Valuable | Every Epic 2 approval follows the delegation table, is recorded with its limit version and escalates instead of stalling |
| Estimable | One router, one decision service, one workflow with its escalation step, one queue operation set and one screen read |
| Small | Fits one sprint with its tests, as the app slice of the legacy key; the D7.1 screen is RWB-P7-E2014-APP |
| Testable | Each of the fourteen criteria runs against the contract fakes, and the two failure paths of X10 and X11 have their own tests |

### 7. Acceptance criteria

```gherkin
Feature: Approval routing with the delegation of authority table

  Background:
    Given the environment is SIT
    Given delegation version "DOA-2026.11" is in force with holder "U-9201" at L6, "U-9202" at L5 and "U-9203" at L4 for MORTGAGE, all holding RW-PRODHEAD
    Given test user "U-9210" holds RW-RESTRUCT and test users "U-9211" and "U-9212" hold RW-LITOFF and test user "U-9213" holds RW-HEADLIT
    Given the rwb-access contract mock returns delegation version "DOA-2026.11" with the levels, holders and substitutes named in each scenario
    Given the rwb-case contract mock returns the case, the parameters and the reference lists named in each scenario

  Scenario: AC1 Routed (legacy RWB-E2-013 AC1)
    Given the rwb-access contract mock returns no delegation row for decision D7.1 and the route role RW-LITOFF for parameter "rwb.approval.route.D7.1.role"
    Given the rwb-case contract mock returns case "RW-2026-000123" at status "In progress" and parameter "rwb.approval.route.D7.1.service-level" = 1 working day, and accepts the approval request fact
    Given a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211"
    When the router runs for decision D7.1 at 09:00 on 14 December 2026
    Then an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026
    Then the system does not show it to "U-9211", who prepared it
    Then the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role"
    Then the case status becomes "Waiting approval"

  Scenario: AC2 Escalated (legacy RWB-E2-013 AC2)
    Given the approval workflow of AC1 holds the service level timer as a durable Temporal timer that expires at 09:00 on 15 December 2026, in place of the retired JOB-05
    Given the rwb-access contract mock returns role RW-HEADLIT as the escalation role of parameter "rwb.approval.route.D7.1.escalation-role" and "U-9213" as its holder
    Given the approval of AC1 is still WAITING at 09:00 on 15 December 2026
    When ApprovalWorkflow publishes TimerBreached for its service level timer
    Then the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026
    Then the system writes one entry with final call "ESCALATED" and "U-9213" is told with MSG-P7-011
    Then the case stays "Waiting approval"

  Scenario: AC3 Limit changed (legacy RWB-E2-013 AC3)
    Given the rwb-access contract mock returns "DOA-2026.11" in force to 31 December 2026 and "DOA-2027.01" from 1 January 2027, with the same amount at L6 in the first and at L5 in the second
    Given approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11"
    Given version "DOA-2027.01" from 1 January 2027 moves that amount to L5
    When a new D6.4 approval with the same amounts routes on 2 January 2027
    Then the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01"
    Then approval "A-1" stays with L6 and "DOA-2026.11"

  Scenario: AC4 Routed by limit (legacy RWB-E2-013 AC4)
    Given the rwb-access contract mock returns the L6 row of "DOA-2026.11" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 with holder "U-9201"
    Given restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00
    When the router runs
    Then the system assigns the approval to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11"
    Then GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age

  Scenario: AC5 Approve inside the limit (legacy RWB-E2-013 AC5)
    Given the rwb-access contract mock returns the A letter in "TREATMENT_AND_OFFER" for "U-9201" with level L6
    Given the rwb-case contract mock accepts the case status "In progress"
    Given the approval of AC4 is WAITING
    When "U-9201" approves it with Idempotency-Key "k-501"
    Then the approval status becomes "APPROVED"
    Then the system writes one entry with approver "U-9201", approval level "L6", limit version "DOA-2026.11", the rule ID and version and final call "APPROVED"
    Then the system publishes decisionRecorded and the response shows MSG-P7-004 with state "In progress"

  Scenario: AC6 The preparer cannot approve (legacy RWB-E2-013 AC6)
    Given the rwb-access contract mock returns "U-9210" holding RW-PRODHEAD at L6 as substitute
    Given "U-9210" also holds RW-PRODHEAD at L6 as substitute
    When "U-9210" approves the approval of AC4
    Then the system refuses the call with status 409 and message MSG-P7-002 and the approval stays "WAITING"

  Scenario: AC7 A change above the limit goes up (legacy RWB-E2-013 AC7)
    Given the rwb-access contract mock returns the L5 row for principal 120,000,000.00 with holder "U-9202"
    Given the approval of AC4 is WAITING with "U-9201"
    When "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves
    Then the call returns MSG-P7-001 with level "L5" and approver "U-9202"
    Then the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded

  Scenario: AC8 Refuse needs a reason (legacy RWB-E2-013 AC8)
    Given the rwb-case contract mock returns case "RW-2026-000124" at the state the rule names after a refusal
    Given the approval of AC4 is WAITING
    When "U-9201" refuses it with no reason
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "reason"
    Then when "U-9201" refuses it with reason "Collateral appraisal older than one year"
    Then the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names

  Scenario: AC9 Return with a question (legacy RWB-E2-013 AC9)
    Given the rwb-case contract mock accepts the return task for preparer "U-9210"
    Given the approval of AC4 is WAITING
    When "U-9201" returns it with reason "Attach the latest income statement"
    Then the system opens the status becomes "RETURNED", a task for preparer "U-9210", and the entry records the question

  Scenario: AC10 An override needs a coded reason (legacy RWB-E2-013 AC10)
    Given the rwb-case contract mock returns LOV-OVERRIDE-REASON with "CUSTOMER_REVISED_OFFER"
    Given the recommendation on the approval of AC4 is a settlement of 1,920,000.00
    When "U-9201" changes it to 1,800,000.00 and approves with no reason code
    Then the system refuses the call with status 422 and message MSG-P7-005

  Scenario: AC11 No holder means escalation, not a stall (legacy RWB-E2-013 AC11)
    Given the rwb-access contract mock returns no holder and no substitute on the L6 row for SSME and holder "U-9202" on L5
    Given the L6 row for SSME has no holder and no substitute
    When an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes
    Then the system assigns it to the L5 holder at once
    Then the routing entry records reason "NO_HOLDER" for L6

  Scenario: AC12 A committee level needs the resolution (legacy RWB-E2-013 AC12)
    Given the rwb-access contract mock returns the L3 row, Problem Asset Resolution Committee, with recording holder "U-9204"
    Given an approval for D6.4 item 2.1.1, MORTGAGE, principal 800,000,000.00, loss 20.00 percent, routed to L3, Problem Asset Resolution Committee, whose recording holder is "U-9204"
    When "U-9204" approves it with no resolution reference
    Then the system refuses the call with status 422 and message MSG-GEN-001 for field "resolutionReference"
    Then when "U-9204" approves with resolution reference "PARC-2026-14" and members present "M-01, M-02, M-03, M-04"
    Then the entry records the resolution reference, the members present, level "L3" and final call "APPROVED"

  Scenario: AC13 Two approvals at once (legacy RWB-E2-013 AC13)
    Given the rwb-access contract mock returns "U-9205" as the substitute at L6 for "U-9201"
    Given the approval of AC4 is WAITING and visible to holder "U-9201" and substitute "U-9205"
    When both approve it at the same moment
    Then one call succeeds and one entry is written
    Then the other call returns status 409 with message MSG-GEN-004

  Scenario: AC14 No limit covers the decision (legacy RWB-E2-013 AC14)
    Given the rwb-access contract mock returns no row for HIRE_PURCHASE in "DOA-2026.11"
    Given "DOA-2026.11" holds no row for HIRE_PURCHASE
    When an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes
    Then the system stores the approval with status "HELD_NO_LIMIT" and the case stays "Waiting approval"
    Then the system raises an incident to RW-RISK with message MSG-P7-010

  Scenario: AC15 Architecture rules BR12 to BR19 hold on every approval (added by this story, D-RCV-60) (new, D-RCV-60)
    Given the approval of AC4 is WAITING
    Given the decision record write is forced to fail during an approval
    When "U-9201" approves the approval of AC4
    Then the approval does not take effect, its status stays "WAITING" and no DecisionRecorded event is published (BR12)
    Then the outcome entry is written in the same transaction as the status change and relayed on rwb.decision-record.v1 (BR15, BR19)
    Then the delegation table is read only through the rwb-access contract with no join across schemas (BR13)
    Then the approval clock is a durable timer in ApprovalWorkflow on task queue "rwb-decision" (BR14)
    Then every cross-service call is one hop with a 2 s budget (BR16)
    Then the route parameters and reference data are read with the version in force (BR17)
    Then the case status and the preparer task move only through the rwb-case contract (BR18)

  Scenario: AC16 Errors answer 401, 403 and 404 of the provided operations (added by this story, D-RCV-60) (new, D-RCV-60)
    Given a call to a provided operation carries no credential
    When the call is made
    Then the system refuses it with status 401 and message Not specified in the source documents (NEWAC-RWB-P7-E2013-APP-AC16)
    When "U-9210", who holds RW-RESTRUCT only, approves the approval of AC4
    Then the system refuses it with status 403 and message MSG-P4-002
    When "U-9201" approves an approval id that does not exist
    Then the system refuses it with status 404 and message Not specified in the source documents (NEWAC-RWB-P7-E2013-APP-AC16)

  Scenario: AC17 A redelivered event is applied once (added by this story, D-RCV-60) (new, D-RCV-60)
    Given the approval of AC4 is WAITING
    Given the consumed event is delivered once and applied
    When the same event is delivered again
    Then the second delivery is acknowledged and no second entry or status change is written

  Scenario: AC18 A retried or timed-out activity leaves the approval unchanged (added by this story, D-RCV-60) (new, D-RCV-60)
    Given the approval of AC4 is WAITING
    When an activity of ApprovalWorkflow fails with a retryable error
    Then the activity is retried under its retry policy Not specified in the source documents (NEWAC-RWB-P7-E2013-APP-AC18)
    When the activity exceeds its timeout of Not specified in the source documents (NEWAC-RWB-P7-E2013-APP-AC18)
    Then the approval stays "WAITING" and no entry is written until the activity succeeds

  Scenario: AC19 A consumed call that fails or does not answer produces no approval (added by this story, D-RCV-60) (new, D-RCV-60)
    Given the rwb-access contract mock fails or does not answer within 2 s
    When the router runs for a decision
    Then no approval is produced and the case does not move
```

The fourteen criteria are the legacy criteria of RWB-E2-013, copied with their values, their identifiers, their amounts, their user keys, their roles, their days and their message IDs unchanged, and one origin tag on each scenario line. One `Given` line is added to each criterion where the fact belongs to another owner — the delegation rows and holders of rwb-access, the case, the parameters and the lists of rwb-case — and the state of that owner is a contract mock, so the criterion is proved in this service as well as end to end. AC2 keeps the legacy trigger wording (`JOB-05 publishes TimerBreached`) because that is what the legacy criterion says and what the legacy test case TC-E2-013-02 asserts; in the target the clock is the durable timer of `ApprovalWorkflow` on task queue `rwb-decision`, JOB-05 is retired (DP-10, Architecture v5 slides 42 and 44), and the added `Given` names the timer that replaces it.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A decision with delegation rows routes to the lowest level whose row covers it on the routing date; the item keeps that delegation version | REQ-APD-001; REQ-APD-010; Delegation of authority matrix, rule 9 |
| BR2 | A decision with no amount limit routes to the role named in its route parameters, for D7.1 notices RW-LITOFF | Parameters `rwb.approval.route.*`; DL22 |
| BR3 | The approver must hold the A letter in the decision's capability area and be the holder or substitute of the required level, or hold the route role | Permission matrix; Key sheet: A works within the delegation table; CTL-04 |
| BR4 | A person may not approve a decision they proposed or prepared | Admin and access model, section 6.2; CTL-05; Delegation of authority matrix, rule 10 |
| BR5 | An approval above the caller's level is refused and sent to the level that covers it, with no silent approval | REQ-APD-004; R-UNI-15 |
| BR6 | A change from the recommendation needs a coded reason; refuse and return need a reason | REQ-APD-005; R-UNI-14; CTL-07 |
| BR7 | An approval not answered inside its service level escalates one level up, or to the escalation role; the case does not move | REQ-APD-007; R-UNI-30; R-UNI-42 |
| BR8 | A level with no holder and no substitute passes the item one level up at once | REQ-APD-011 |
| BR9 | Levels L1 to L3 approve by committee resolution; the entry records the resolution reference, the date and the members present | REQ-APD-008; Delegation of authority matrix, Levels sheet |
| BR10 | The limit, the rule version and the approver are written with every approval | REQ-APD-009; FEAT-DRI-04 |
| BR11 | A decision that no limit covers is held and raises an incident | Delegation of authority matrix, rule 8 |
| BR12 | An approval outcome that cannot be written to the decision log does not take effect | Principle 5; R-UNI-39 |
| BR13 | The delegation table and the authorise decision are rwb-access's and are read on its contract; the approval, its routing and its version stamp are `rwb_decision` rows, and no join crosses the two schemas | Architecture v5 slides 14 and 41; DP-01; DP-08 |
| BR14 | The approval clock, its escalation and its restart are a durable timer in `ApprovalWorkflow`; no Quartz row, no shared job table and no JOB-05 row is read or written | Architecture v5 slides 42 and 44; DP-10 |
| BR15 | The outcome entry is written through the local decision-record library in the same transaction as the status change and is relayed on `rwb.decision-record.v1`; no second ledger is written by this service | Architecture v5 slide 28; DP-03 |
| BR16 | Every cross-service call is one hop with a 2 s budget; a delegation read or an authorise read that does not answer never produces an approval | ADR-020; DP-11 |
| BR17 | The route parameters, the capability area per decision code, the service levels and the escalation roles are parameters of rwb-case, and the levels, the statuses, the products and the override reasons are its reference data, each read with the version in force | FSD P7 A2.15 BR-P7-015; TSD P7 T3.2; DP-06; DP-07 |
| BR18 | The case status, the case queue and the preparer task are rwb-case's; this service sends the facts and reads the answers, and moves no case state itself | R-PREC default ruling; TSD P7 T4 |
| BR19 | The approval outcome leaves this service only as DecisionRecorded on rwb.decision-record.v1; no data lake copy, lake partition, manifest or watermark is written (INT-19 and INT-20 are retired) | Architecture v5 slide 37; DP-17; ADR-018 |

Open decisions: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL18 (assumptions ASM-2569, ASM-2839, ASM-2859, ASM-2883); DL22 (assumptions ASM-1162, ASM-1304, ASM-2217, ASM-2569). Each decision is still open; each assumption is confirmed by the programme directive.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| In progress | Recommendation routed for approval | Approval stored `WAITING` or `HELD_NO_LIMIT` | Waiting approval |
| Waiting approval | Approver accepts | Caller within the required level, holds the A letter, is not the preparer | In progress |
| Waiting approval | Approver changes and accepts | Changed terms within the caller's level, coded reason given | In progress |
| Waiting approval | Approver rejects | Reason given | Not specified in the source documents (CG-ALL-7149) |
| Waiting approval | Approver returns with a question | Reason given | Not specified in the source documents (CG-ALL-7150) |
| Waiting approval | SLA_BREACHED (R-UNI-30) | The durable timer of the approval workflow fires | Not specified in the source documents (CG-ALL-7151) |

The approval record moves `WAITING` to `APPROVED`, `REFUSED` or `RETURNED`, and stays `WAITING` with a new approver on escalation or on a change above the limit. An escalation is a decision entry with final call `ESCALATED` and an incremented `escalation_level`, not a status value: LOV-APPROVAL-STATUS carries `WAITING`, `HELD_NO_LIMIT`, `APPROVED`, `REFUSED` and `RETURNED` only (TSD P7 T3.2). The case status column of this table is rwb-case's projection of the facts this service sends (BR18); the approval status column is this service's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Holders and substitutes of levels L4 to L6 (named per DL18) | Approve, change, refuse or return items at their level |
| Recording holder of levels L1 to L3 | Records the committee resolution with its reference and members present |
| RW-LITOFF Litigation officer, RW-LEGAL Legal counsel, RW-HEADLIT Head of Litigation | Approve D7.x items routed to their role (Litigation A) |
| RW-PRODHEAD Product head | Approves items of their product at their level (A in Treatment and offer, Litigation, Asset and disposal, Debt sale, Write-off and posting) |
| RW-RESTRUCT, RW-CREDCOMM | Approve Treatment and offer items at their level (A) |
| RW-SALEOFF, RW-HEADNPA, RW-HEADASL, RW-DEBTSALE | Approve Asset and disposal or Debt sale items at their level (A) |
| RW-CREDITAD, RW-WOCOMM, RW-FINANCE | Approve Write-off and posting items at their level (A) |
| RW-RISK | Receives the incident of a decision that no limit covers |
| Preparer of an item | May not approve it |
| SY-RULES, SY-CASEWF | Call the approval request (Decision log C) |
| RW-AUDIT | Reads approvals through the decision log |
| Approval levels | L1 Board of Directors to L6 Recovery executive, department level, per the delegation table |

The letters above are read from the permission matrix and the delegation of authority matrix named in the legacy story, through the authorise contract of rwb-access (DP-08); the capability area and the right of each operation are declared in RWB-P7-E2013-CON and enforced at gateway-bff, which asks rwb-access. The service re-checks the same answer for the decisive calls, so a call that reaches it directly is refused as well. The per-service login of `rwb_decision` carries no person identity (DP-02).

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-032 | approval | id | Write on create, read |
| DF-DEC-033 | approval | case_id | Write on create, read |
| DF-DEC-034 | approval | decision_code | Write on create, read |
| DF-DEC-035 | approval | regulation_item | Write on create, read |
| DF-DEC-036 | approval | capability_area | Write on create, read |
| DF-DEC-037 | approval | route_role_code | Write on a role-routed item, read |
| DF-DEC-038 | approval | approval_level | Write on routing and on escalation, read |
| DF-DEC-039 | approval | delegation_limit_id | Write as the reference of the row read from rwb-access, never a foreign key |
| DF-DEC-040 | approval | limit_version | Write on routing, never updated by a later version |
| DF-DEC-041 | approval | product_group | Write on create, read |
| DF-DEC-042 | approval | amount | Write on create and on an accepted change, read |
| DF-DEC-043 | approval | terms | Write on create and on an accepted change, read |
| DF-DEC-044 | approval | prepared_by | Write on create, read by the preparer check |
| DF-DEC-045 | approval | assigned_user_id | Write on routing, escalation and a change above the limit, read |
| DF-DEC-046 | approval | status | Write on every status move, read |
| DF-DEC-047 | approval | due_at | Write on routing and on escalation, read |
| DF-DEC-048 | approval | escalation_level | Write on escalation, read |
| DF-DEC-049 | approval | source_type | Write on create, read |
| DF-DEC-050 | approval | source_ref | Write on create, read |
| DF-DEC-051 | approval | rule_id | Write on create, read |
| DF-DEC-052 | approval | rule_version | Write on create, read |
| DF-DEC-053 | approval | decision_log_id | Write with the outcome entry, read |
| DF-DEC-001 to DF-DEC-018, DF-DEC-028 to DF-DEC-030 | decision_log_entry, through the local library | The routing, escalation and outcome entries: rule, version, inputs, approver, level, final call, hashes and chain position | Write through the decision-record library, never a table read of another service |
| DF-REF-018, DF-REF-023, DF-REF-024 | delegation_limit, owned by P4 rwb-access | approval_level, holder_user_id, substitute_user_id | Read through the RWB-P4-E1037-CON contract, never a table and never a join |
| DF-WRK-019, DF-WRK-020, DF-WRK-023 | task, owned by P3 rwb-case | task_code, element_type, owner_role | Written through the rwb-case contract on a return; the task row is rwb-case's |
| DF-WRK-030, DF-WRK-032, DF-WRK-036 | timer, owned by P3 rwb-case | timer_type, expires_at, escalation_level | Not read and not written here: the approval clock is the durable timer of `ApprovalWorkflow` (DP-10) |

Field IDs are those in the Logical Data Model and Data Dictionary. The approval table is created by this story with `case_id uuid`, `decision_code varchar(8)`, `regulation_item varchar(10)`, `capability_area varchar(30)`, `route_role_code varchar(20)`, `approval_level varchar(4)`, `delegation_limit_id uuid`, `limit_version varchar(20)`, `product_group varchar(15)`, `amount numeric(18,2)`, `terms jsonb`, `prepared_by uuid`, `assigned_user_id uuid`, `status varchar(20)`, `due_at timestamptz`, `escalation_level integer default 0`, `source_type varchar(20)`, `source_ref varchar(60)`, `rule_id varchar(20)`, `rule_version varchar(20)`, `decision_log_id uuid` and the standard columns; the migration is `V2013_1__approval.sql` in the `rwb_decision` sequence (DP-15). The indexes are `ix_approval_assignee` on `(assigned_user_id, status)`, `ix_approval_role` on `(route_role_code, status)`, `ix_approval_due` on `(status, due_at)` for the escalation step, and a partial unique index on `(source_type, source_ref)` where `status in ('WAITING','HELD_NO_LIMIT')`, which is the optimistic lock of AC13 together with the record version column. `delegation_limit_id` is a reference and never a foreign key: the table is in `rwb_access` and a foreign key would be a cross-schema dependency (DP-01, BR13). The `approval` row carries no name, no e-mail address and no account number; the user keys are identifiers, and the members present of a committee are member references.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-decision (P7); base `/api/recovery/decision/v1`. The shapes are those fixed in RWB-P7-E2013-CON; this story implements them and adds no path. Contract version: Not specified in the source documents (DOR-RWB-P7-E2013-APP-23).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P7-002 | GET | `/approvals` | List the items waiting on the caller's level or role, with decision, product, page and size as query parameters | Decision log, right A, scope applied | Not applicable |
| API-P7-008 | GET | `/approvals/{approvalId}` | Read one approval with its routing details, the limit version, the rule and the due time | Decision log, right A, scope applied | Not applicable |
| API-P7-003 | POST | `/approvals/{approvalId}/approve` | Approve, or change and approve, inside the caller's level | Decision log, right A, scope applied | `Idempotency-Key` required |
| API-P7-004 | POST | `/approvals/{approvalId}/return` | Return the item to the preparer with a question | Decision log, right A, scope applied | `Idempotency-Key` required |
| API-P7-005 | POST | `/approvals/{approvalId}/refuse` | Refuse the item with a reason | Decision log, right A, scope applied | `Idempotency-Key` required |

Errors: 401 no session (message ID: Not specified in the source documents (CG-ALL-7154)); 403 the role lacks the A letter in the decision's capability area or is not the holder, the substitute or the route role (MSG-P4-002); 404 the approval is absent or outside the caller's scope (MSG-P4-003); 409 the caller prepared the item (MSG-P7-002), the change is above the caller's level and the item has moved (MSG-P7-001), or the record changed (MSG-GEN-004); 422 a missing reason, reason code, resolution reference or members present (MSG-GEN-001, MSG-P7-005); 503 the decision record was not written (MSG-P7-003) or a consumed call did not answer inside 2 s (MSG-GEN-006). The request body `ApprovalAction` carries `reason`, `resolutionReference`, `reasonCode`, `changes` and `membersPresent` as the legacy names them; its types, lengths, the optionality of each property and the page shape of `ApprovalPage` are Not specified in the source documents (GAP-1255; ASM-2219).

#### 12.2 REST operations consumed

| Method and path | Owner | Contract | Use in this story |
|---|---|---|---|
| GET `/api/recovery/access/v1/doa-limits` | P4 rwb-access | RWB-P4-E1037-CON | The lowest covering level for the decision, the product and the amounts on the routing date, with the delegation row reference, the level, the holder and the substitute; the table stays rwb-access's while the routing rules sit here (GAP-1251; ASM-2215), and the path has no row in the Ownership Map API catalogue (GAP-1252; ASM-2216) |
| POST `/api/recovery/access/v1/authorise` | P4 rwb-access | RWB-P4-E1037-CON | The A letter of the capability area and the level or route role of the caller, re-checked on every decisive call (DP-08) |
| GET `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | RWB-P3-E1028-CON | The case, its status, the preparer and the source facts of the item; the status move this story asks for has no named operation in the Ownership Map (GAP-1255; ASM-2219) |
| GET `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | RWB-P3-E1042-CON | `rwb.approval.route.*`, `rwb.approval.area.*` and `rwb.approval.service-level.*`, read with the version in force (DP-06) |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | RWB-P3-E1043-CON | LOV-APPROVAL-LEVEL, LOV-APPROVAL-STATUS, LOV-CAPABILITY, LOV-PRODUCT and LOV-OVERRIDE-REASON (DP-07) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (DP-11). No row reads a table and no row reads a `v_ace_*` view: the delegation rows and the case facts arrive through the owner's contract (DP-01, DP-05 is not claimed because this service reads no ACE view).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs, codes and facts only) |
|---|---|---|---|---|
| `rwb.decision.ApprovalRequested.v1` (EV-09) | `rwb.decision.events.v1` | P7 rwb-decision | caseId | approval ID, case ID, decision code, capability area, approval level or route role, amount and limit version, rule ID and version, due time and business date |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | decision code, rule ID and version, limit version, approval level, final call, approval ID, concluded at, record reference |

Both are written to the outbox in the same transaction as the state change and relayed with the CloudEvents 1.0 envelope (DP-09, DP-03). `ApprovalRequested` is event 09 of the catalogue and its consumer in the catalogue is the gateway-bff inbox; the case status move to Waiting approval is therefore asked of rwb-case on its contract and is not read from this event. `ApprovalDecided` is named on the service contract slide but carries no catalogue row and no event ID, so this story publishes no such event (GAP-1257; ASM-2221).

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.access.DoaLimitChanged.v1` | `rwb.access.events.v1` | P4 rwb-access | Refreshes the cached delegation version so the next routing decision reads the version in force; an open approval keeps the version already written on it (BR1, AC3); deduped through the inbox |

No other event is consumed. `TimerBreached` of rwb-case is not consumed for approvals: the approval clock is the durable timer of `ApprovalWorkflow` in this service (DP-10, BR14).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| ApprovalWorkflow | Workflow, one run per approval, workflow ID from the approval ID | `rwb-decision` | Holds the service level as a durable timer, signals the outcome from the decision calls, runs the escalation step when the timer fires and repeats it for the next service level |
| readDelegation | Activity, in rwb-decision | `rwb-decision` | The rwb-access delegation read of one decision, product and amount set, with the 2 s budget; a failure fails the step and no approval is stored as covered |
| routeApproval | Activity, in rwb-decision | `rwb-decision` | The routing rule of BR1, BR2, BR8 and BR11: level or route role, the no-holder rule, the `HELD_NO_LIMIT` hold |
| recordOutcome | Activity, in rwb-decision through the library | `rwb-decision` | The outcome entry, the status change, the outbox row; a failure fails the step and nothing moves (BR12, BR15) |
| escalateApproval | Activity, in rwb-decision | `rwb-decision` | One level up or the escalation role, the restart of the timer, the `ESCALATED` entry and the notification request of MSG-P7-011 |

The workflow input is the approval ID, the decision code, the level or role, the limit version, the due time and the business date; it carries no name, no account number and no document. The escalation timer is a durable timer inside the workflow, not a Schedule and not a cron entry (DP-10).

#### 12.6 Schedules

None. This capability declares no Schedule: the approval clock is the durable timer of `ApprovalWorkflow`, and JOB-05, the legacy timer job, is retired (Architecture v5 slides 42 and 44). The two Schedules of the service — JOB-14 the hash-chain check at 02:00 and JOB-20 the rule promote at 00:01 — belong to RWB-P7-E1008-APP and the rule-version story, and are registered by RWB-P7-E2013-OPS and not created here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| approval | P7 (rwb_decision) | The approval, its routing, its level, its limit version, its status, its due time and its escalation level; the state machine of section 9 |
| decision_log_entry and the local decision record | P7 (rwb_decision), written through the library | The routing, escalation and outcome entries of this story (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | The two published events, the one consumed event and the stored `Idempotency-Key` answer (DP-09) |

Not owned and never read: `delegation_limit`, `role`, `permission` and `masking_rule` (P4 rwb-access, read through RWB-P4-E1037-CON), `recovery_case`, `case_party`, `task`, `timer`, `queue`, `parameter_catalog`, `parameter_value`, `reference_row` and `reference_version` (P3 rwb-case, read through RWB-P3-E1028-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON), `rule_package` and `rule_row` (P7, but not this story), `notice` (P6). No foreign key crosses a service boundary (DP-01, BR13).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-access delegation fake | `GET /api/recovery/access/v1/doa-limits` | `DOA-2026.11` with L6 holder `U-9201`, L5 holder `U-9202`, L4 holder `U-9203` for MORTGAGE and the D6.4 row 2.1.1 at 2,400,000.00; no L6 holder for SSME; no row for HIRE_PURCHASE; the L3 committee row with recording holder `U-9204`; `U-9205` as the L6 substitute; `DOA-2027.01` from 1 January 2027; a delayed answer beyond 2 s; an unavailable answer |
| rwb-access authorise fake | `POST /api/recovery/access/v1/authorise` | The A letter for `U-9201` in TREATMENT_AND_OFFER at L6, for `U-9213` in LITIGATION as RW-HEADLIT, for `U-9204` at L3; a refusal for a role without the area; a delayed answer beyond 2 s |
| rwb-case fake | The case read and the case facts this story sends | Case `RW-2026-000123` at `In progress` with preparer `U-9211`, case `RW-2026-000124` at `In progress` with preparer `U-9210`; the status `Waiting approval`, `In progress` and the state of a refusal; the return task for `U-9210` |
| rwb-case parameter fake | `GET /api/recovery/case/v1/admin/parameters` | `rwb.approval.route.D7.1.area` = LITIGATION, `.role` = RW-LITOFF, `.escalation-role` = RW-HEADLIT, `.service-level` = 1 working day; `rwb.approval.service-level.default` = 3 working days; `rwb.approval.area.D6.4` = TREATMENT_AND_OFFER; a delayed answer beyond 2 s |
| rwb-case reference-data fake | `GET /api/recovery/case/v1/admin/lists/{listCode}` | LOV-APPROVAL-LEVEL, LOV-APPROVAL-STATUS, LOV-CAPABILITY, LOV-PRODUCT with MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED, and LOV-OVERRIDE-REASON with CUSTOMER_REVISED_OFFER; a delayed answer beyond 2 s |
| rwb-decision record fake | The local decision-record library and the shared topic | A healthy chain and outbox; a stopped chain for AC5, TC-E2-013-16 and X11 |

The values are the legacy values of RWB-E2-013 section 7 and its background, kept unchanged so the component and integration assertions read the same fixtures; the fake set is the one fixed in RWB-P7-E2013-CON, and the drift test of that story fails a build in which a fake and the document disagree.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 5 consumed | API-P7-002, API-P7-008, API-P7-003, API-P7-004 and API-P7-005 provided; the delegation read, the authorise call, the case read, the parameters and the lists consumed; one hop, 2 s |
| Kafka | 2 published, 1 consumed | `ApprovalRequested` and `DecisionRecorded` published; `DoaLimitChanged` consumed |
| Temporal | 1 workflow and 4 activities | `ApprovalWorkflow` with `readDelegation`, `routeApproval`, `recordOutcome` and `escalateApproval` on task queue `rwb-decision` in namespace `rwb-recovery` |
| File | None | No file element in this capability |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `approval`, Java package `th.co.scb.ace.workbench.recovery.decision.approval`; front end `recovery/decision/approval`.

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

No pattern is claimed for DP-02 (the login is the platform's, declared in the contract), DP-04 (no rule package is evaluated here), DP-05 (no ACE view is read), DP-12 (the approval is a child workflow of the case and not a case workflow of its own), DP-14 (the topic names follow the rule already), DP-16 (no integration adapter), DP-17 (no data lake), DP-18 (no interaction ledger) or DP-20 (no agent).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ApprovalController | Controller | The five operations, the `Idempotency-Key`, the validation and the error mapping for 401, 403, 404, 409, 422 and 503 |
| ApprovalRouter | Service | The request of a caller: the area, the level or route role, the no-holder rule, the hold, the store, the workflow start and `ApprovalRequested` |
| ApprovalDecisionService | Service | BR3 to BR6 and BR9 in the order of section 4, step 7; the status, the entry, the event and the case facts |
| ApprovalEscalationStep | Workflow step | The timer outcome: next level or escalation role, the restart, the `ESCALATED` entry and MSG-P7-011 |
| ApprovalQueueQuery | Service | The queue and the detail read with the scope filter, the age and the due time |
| DelegationClient | Adapter | The delegation read of rwb-access with one hop and 2 s, and the cache refreshed by `DoaLimitChanged` |
| AuthoriseClient | Adapter | The authorise answer of rwb-access for the area and the level or role |
| CaseFactClient | Adapter | The case read and the case facts this story sends, on the rwb-case contract |
| ParameterCatalog and ReferenceCatalog | Service | The route parameters, the areas, the service levels and the five lists, read with the version in force |
| ApprovalRepository | Repository | The `approval` row with optimistic locking on the record version |
| ApprovalWorkflowImpl | Workflow | The durable timer, the signal from the decision calls and the escalation step |

**Database and migrations**

- Creates `approval` and its four indexes in `rwb_decision` with `V2013_1__approval.sql`; writes the local decision record and the library objects; reads no other schema (section 11, DP-15).
- `delegation_limit_id` is a reference to a row of rwb-access and not a foreign key; the level, the holder and the substitute are read at routing time and never copied except for the reference, the level and the version (BR13).
- No personal data is a column: no name, no e-mail address and no account number; a committee is recorded as member references.

**Configuration and reference data**

- Route parameters per decision: `rwb.approval.route.D7.1.area` = LITIGATION, `.role` = RW-LITOFF, `.escalation-role` = RW-HEADLIT and `.service-level` = 1 working day, owned by RW-COE (DL22).
- Limit-based service level: `rwb.approval.service-level.default` = 3 working days (DL22).
- Capability area per decision code: `rwb.approval.area.<code>`, for D5 and D6.x TREATMENT_AND_OFFER, D7.x LITIGATION, D8.2 and D8.3 ASSET_AND_DISPOSAL, D8.4 DEBT_SALE and D9.x WRITE_OFF_AND_POSTING.
- The five lists of section 12.8 and LOV-OVERRIDE-REASON, owned by RW-COE and loaded as reference data (DP-07).
- The escalation ceiling and the behaviour at the last level: Not specified in the source documents (GAP-1253; ASM-2217); the parameter `rwb.approval.escalation.max-levels` is carried as data with no value until the register closes the point.
- Feature switch `rwb.decision.approval-routing`, read as a parameter: off refuses a new routing request with a closed answer and changes no approval.

**Build steps**

1. Create the `approval` migration, entity and repository with the optimistic lock and the partial unique index; test the two-approver case of AC13.
2. Build DelegationClient and AuthoriseClient against the contract fakes, with the 2 s budget, the breaker and the cache refreshed by `DoaLimitChanged`; test AC4, AC6, AC11 and the delayed answer of X10.
3. Build ApprovalRouter for the limit-based and the role-based route, the no-holder rule and the `HELD_NO_LIMIT` hold; tests for AC1, AC3, AC4, AC11 and AC14.
4. Wire the case read and the case facts, and the two events; test the case status of AC1 and the event payload.
5. Build ApprovalDecisionService for approve, change, refuse and return with all the checks in order; tests for AC5 to AC10 and AC12.
6. Add the idempotency rule and the concurrency test of AC13.
7. Build ApprovalWorkflowImpl with the durable timer and ApprovalEscalationStep; test AC2 with a fixed clock, the restart of the timer and the `ESCALATED` entry.
8. Prove the version change of AC3 with two delegation versions and one open approval.
9. Prove the fail-closed path of X11: a stopped record chain leaves the status unchanged and raises the incident.
10. Build the queue and detail reads with the scope filter, and hand the queue screen to the gateway-bff composite route (DP-19).

**Done when.** The tests in section 16 pass, the contract tests of RWB-P7-E2013-CON stay green, no approval is ever assigned to its preparer, and a SIT week shows every routed item with a level or a role and a limit version, every escalation with its `ESCALATED` entry and its new due time, every `HELD_NO_LIMIT` item with its incident, and no routing decision taken on a delegation version other than the one in force.

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
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | No A letter in the decision's area | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The approval is outside the caller's scope | This case is not in your scope. |

MSG-P7-001, MSG-P7-002, MSG-P7-003, MSG-P7-004, MSG-P7-005, MSG-P7-010, MSG-P7-011, MSG-GEN-001, MSG-GEN-004 and MSG-P4-002 are copied unchanged from RWB-E2-013 section 14; MSG-P4-003 and MSG-GEN-006 are the platform messages of the authorise and consumed-call paths. The Thai text of each follows DL10; the proposed Thai of MSG-P7-011 stays with the additions file until the catalog publishes it.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-10 Approval queue | Loading | Waits while the items load through the gateway-bff composite route |
| SCR-10 Approval queue | List | Sees each item waiting on them with decision, case, amount, level, limit version, age and due time; opens an item in SCR-11 |
| SCR-10 Approval queue | Empty | Not specified in the source documents (CG-ALL-7166) |
| SCR-10 Approval queue | Escalated item | An item that passed its service level appears with its new level or role, its escalation level and its new due time |
| SCR-10 Approval queue | Held, no limit | An item with status `HELD_NO_LIMIT` is not in an approver's list; it is visible to RW-RISK through the same read with its incident message |
| SCR-10 Approval queue | Error | Not specified in the source documents (CG-ALL-7166) |
| SCR-10 Approval queue | No access | Not specified in the source documents (CG-ALL-7166) |
| SCR-11 Decision screen | Empty | Not specified in the source documents (CG-ALL-7167) |
| SCR-11 Decision screen | Loading | Not specified in the source documents (CG-ALL-7167) |
| SCR-11 Decision screen | Error | Not specified in the source documents (CG-ALL-7167) |
| SCR-11 Decision screen | No access | Not specified in the source documents (CG-ALL-7167) |

SCR-11 Decision screen is built for its first use, the D7.1 notices, in RWB-P7-E2014-APP and is not part of this story. The composite route, its field list, its masking and its timeout budget belong to RWB-PLT-N001-CON (DP-19).

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
| TC-E2-013-16 | Principle 5 | NFR | The decision record write forced to fail during an approval |
| TC-E2-013-17 | AC15, BR12 to BR19 | Contract | Approval with the decision record write forced to fail; rules checked against the fakes of section 12.8 |
| TC-E2-013-18 | AC16 | Contract | Call with no credential; call without the right; approval id that does not exist |
| TC-E2-013-19 | AC17 | Component | Consumed event delivered twice |
| TC-E2-013-20 | AC18 | Component | Activity with a retryable failure and an activity that times out |
| TC-E2-013-21 | AC19, BR16 | Contract | rwb-access call that fails or does not answer within 2 s |

The sixteen cases TC-E2-013-01 to TC-E2-013-16 are the legacy cases of this key, kept in the legacy order with their covers and data unchanged; TC-E2-013-17 to TC-E2-013-21 are added by this story for AC15 to AC19; legacy level System maps to End to end, Access to Component and Resilience to NFR. Each row runs against the contract fakes of section 12.8, so the cross-service facts of a criterion are supplied by the fake of their owner and the assertion is made on this service. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: levels, limits, holders, route roles, areas, service levels, the escalation ceiling and the override reasons are data rows and parameters read with the version in force.
- No personal data in events, workflow inputs, logs, tests or prompts: approval IDs, case IDs, user keys, amounts, levels and dates only; a committee is recorded as member references, not names.
- No read of another service's tables and no `v_ace_*` read of this service: the delegation, the authorise answer, the case and the parameters arrive on the owner's contract (DP-01, DP-08).
- The delegation table stays in rwb-access: this service stores the row reference, the level and the version and never a copy of the limit table (BR13).
- No approval without its decision record in the same transaction: a failed record leaves the status unchanged, writes no event and raises the incident (BR12, R-UNI-39).
- No item is ever assigned to its preparer, and an escrow of two approvers yields one entry and one 409 (CTL-05, AC13).
- The approval clock is a durable timer of the workflow and never a Quartz row, a JOB-05 row or a shared job table (DP-10, BR14).
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb-decision` in namespace `rwb-recovery`; the decision record leaves on the shared topic `rwb.decision-record.v1` and never as a new event of this service (DP-03, DP-13).
- One hop and 2 s on every call; a missing delegation or authorise answer never produces an approval (DP-11, X10).
- Every example and fixture is synthetic; no production payload is copied into a test or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-001 | Route to the approver named by the delegation table | Epic 2, 3.7 | FEAT-APD-01, FEAT-APD-10 | 17 Run the decision center | BR1, BR2 | TC-E2-013-01, TC-E2-013-04 |
| REQ-APD-003 | Accept, change, reject or return, each recorded | Epic 2, 3.7 | FEAT-APD-02, FEAT-APD-03, FEAT-APD-04 | 17 Run the decision center | BR3, BR6 | TC-E2-013-05, TC-E2-013-08, TC-E2-013-09 |
| REQ-APD-004 | Above the limit refused and raised, no silent approval | Epic 2, 3.7 | FEAT-APD-05 | 17 Run the decision center | BR4, BR5 | TC-E2-013-06, TC-E2-013-07 |
| REQ-APD-005 | Override needs a coded reason | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR6 | TC-E2-013-10 |
| REQ-APD-007 | Unanswered approval escalates to the named role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR7 | TC-E2-013-02 |
| REQ-APD-008 | Committee decision recorded with members present | Epic 2, 3.7 | FEAT-APD-07 | 17 Run the decision center | BR9 | TC-E2-013-12 |
| REQ-APD-009 | Limit, rule version and approver written with every approval | Epic 2, 3.7 | FEAT-APD-11 | 17 Run the decision center | BR10, BR12, BR15 | TC-E2-013-05, TC-E2-013-13, TC-E2-013-16 |
| REQ-APD-010 | Open items keep the delegation version they were decided under | Epic 2, 3.7 | FEAT-APD-10 | 17 Run the decision center | BR1, BR13 | TC-E2-013-03, TC-E2-013-14 |
| REQ-APD-011 | Routing escalates rather than stalls with no person in a role | Epic 2, 3.7 | FEAT-APD-06 | 17 Run the decision center | BR8 | TC-E2-013-11 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-013, disposition Split (rework) |
| Legacy criteria owned here | AC1 to AC14, each tagged (legacy RWB-E2-013 ACn) |
| Test cases | TC-E2-013-01 to TC-E2-013-21: the sixteen legacy cases in the legacy order, and TC-E2-013-17 to TC-E2-013-21 added by this story |
| Decoupling patterns | DP01, DP03, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-016 (reusable Temporal layer, Schedules replace Quartz), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger), ADR-023 (observability per service) |
| Rules | R-UNI-14, R-UNI-15, R-UNI-30, R-UNI-39, R-UNI-42 |
| Controls | CTL-04, CTL-05, CTL-07 |

The supporting features of the legacy key — FEAT-APD-01, FEAT-APD-02, FEAT-APD-03, FEAT-APD-04, FEAT-APD-05, FEAT-APD-06, FEAT-APD-07, FEAT-APD-09, FEAT-APD-10 and FEAT-APD-11 — are answered here for the rwb-decision slice; FEAT-APD-08, the D7.1 approval screen and the release to dispatch, is RWB-P7-E2014-APP, and this story changes none of their designs.

### 19. Out of scope

- The decision screen SCR-11 and the D7.1 notice approval with release to dispatch (RWB-P7-E2014-APP).
- The contract document, its property lists, the event envelopes and the fakes as published artefacts (RWB-P7-E2013-CON).
- The committee pack screen SCR-12 with each member's vote (Epic 4).
- The recommendation with reasons and the expected return by route (Epic 4, API-P7-001).
- The monthly override reason report (Epic 8, FEAT-ADM-08 QA sample; reporting stories).
- The delegation of authority table, its versions, its holders and its substitutes: rwb-access (P4), read through RWB-P4-E1037-CON. The routing rule and the approval are here; the table is not.
- The case, its status, its queue, the return task and the case-level timers: rwb-case (P3). This story sends the facts and reads the answers.
- The parameters, the capability areas and the five lists as catalogues: rwb-case (P3, DP-06, DP-07).
- The central decision ledger, its hash chain, the daily seal and JOB-14: RWB-P7-E1008-APP and RWB-P7-E2005-APP.
- The data lake: there is none (DP-17, ADR-018); the decision-record events feed rwb-reporting, and no lake copy, partition, manifest or watermark belongs to this story, although the legacy decision-log path of FEAT-DRI-06 and INT-19 streamed to a lake (GAP-1254; ASM-2218).
- The deployment, the Temporal worker registration, the dashboards, the alerts and the run book of this capability: RWB-P7-E2013-OPS.
- The PostgreSQL schema, the login and the grants of `rwb_decision`: RWB-PLT-NF06-DB and the per-service DB work.
