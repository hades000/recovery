<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 036 Queue write interface for models and agents v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 036 Queue write interface for models and agents v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-036 Queue write interface for models and agents

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-036 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | FEAT-CWC-29 Accept a queue placement from a model or an agent |
| Requirement IDs | REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020 |
| BRD section | Business Requirements Epic 2, section 3.2 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-019, RWB-E1-020, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **an interface through which an approved model or agent places a case on a queue, under its own service identity and the queue's own rules**, so that **analytical output reaches a person the next working day instead of through a weekly manual step**.

## 2. Business rationale

Model scores and agent findings reach the queues today through a weekly file that a person loads by hand, so a case flagged on Monday is worked the following week. The interface lets an approved caller place a case on a queue the day the decision is made, while the queue's allocation method, caseload cap and the role to permission matrix apply as they do to any case, and every placement is written to the decision log with the caller and its version. It meets REQ-CWC-017, REQ-CWC-018 and REQ-CWC-019; the business measure is the time from a model decision to the case reaching a queue, from up to 7 days today to the same day.

## 3. Preconditions

- RWB-E1-019 (roles, teams and queues as data), RWB-E1-020 (allocation and assignment engine) and RWB-E1-027 (decision log writer) are done.
- The caller is listed in the approved callers list (configuration key rwb.casewf.placement.approved-callers) with its caller code, its type MODEL or AGENT and its service identity. The list is empty at go-live (assumed); RW-COE requests an entry and RW-RISK approves it.
- The permission matrix in force gives the caller's service identity Queue and allocation C. The matrix today gives SY-AGENT R only, so a matrix version change by RW-SECADM is needed before the first caller is switched on.
- The target queue exists with its assignment method, caseload cap and overflow queue (DL23; caseload cap 150, assumed).
- Feature flag `rwb.casewf.queue-placement` is off in every environment except DEV and SIT test runs.

## 4. Flow

1. Caller (model job or agent under its service identity): sends POST /api/recovery/v1/queues/{queueId}/placements with caseId, reason, modelOrAgent and version.
2. PlacementController: returns 404 with MSG-P2-025 when the feature flag is off.
3. PlacementController: checks Queue and allocation C through the common module access check.
4. PlacementController: validates the four fields and checks that modelOrAgent is in the approved callers list for this service identity.
5. PlacementService: reads the queue and the case; refuses a closed case, a case with an open deviation and a case already in this queue.
6. PlacementService: builds the decision log record with the caller, reason, model or agent version and target queue (BR5).
7. PlacementService: sets the case queue and calls AllocationService.assignInQueue, which applies the queue's method and caseload cap and uses the overflow queue when every owner is at the cap.
8. PlacementService: ends any previous assignment, writes the new assignment with reason ALLOCATION, publishes CaseAllocated (and CaseTransferred when the case had an owner) to the outbox and calls DecisionLogWriter.write as the last step, all in one transaction. If the write fails, nothing commits.
9. PlacementController: returns 201 with the placement result.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Feature flag off | 404; nothing changes | MSG-P2-025 | AC4 |
| X2 | Caller is not in the approved callers list | 422; nothing changes | MSG-P2-020 | AC5 |
| X3 | caseId, reason, modelOrAgent or version empty | 422 naming the field | MSG-GEN-001 | AC6 |
| X4 | The case is already in the target queue, including a repeated call | 409; no second entry | MSG-P2-024 | AC7 |
| X5 | The case is closed | 409 | MSG-P3-005 | AC8 |
| X6 | The case has an open deviation | 409; the case stays with the deviation handler (R-DEV-01) | MSG-P2-021 | AC9 |
| X7 | The queue or the case does not exist | 404 | MSG-P4-003 | AC10 |
| X8 | Every owner in the queue is at the caseload cap | Case placed in the overflow queue with status unchanged | None | AC2 |
| X9 | Two placements of the same case commit at the same time | One commits; the other gets 409 | MSG-GEN-004 | AC11 |
| X10 | The caller's identity lacks Queue and allocation C | 403 | MSG-P4-002 | Access test TC-E2-036-13 |
| X11 | The decision log write fails | 503; nothing changes; incident raised (R-UNI-39) | MSG-P7-003 | Principle 5 test TC-E2-036-14 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the allocation engine and decision log writer of Epic 1; no model is needed to build or test it |
| Negotiable | Which callers are approved is configuration; caps and methods are queue data |
| Valuable | A daily model decision reaches a person the same day |
| Estimable | One endpoint, one service, one configuration list, reuse of the allocation engine |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below has one test with a synthetic caller |

## 7. Acceptance criteria

```gherkin
Feature: Queue write interface for models and agents

  Background:
    Given feature flag "rwb.casewf.queue-placement" is on
    Given the permission matrix version "PM-SIT-02" gives service identity SY-AGENT Queue and allocation C
    Given the approved callers list holds caller "MDL-SYN-PRIORITY" of type MODEL for service identity SY-AGENT
    Given queue "MTG-BKK-PRI" of team "MTG-BKK" uses method ROUND_ROBIN with caseload cap 150 and overflow queue "MTG-BKK-OVF"
    Given case "RW-2026-000501" has status NEW, no owner, no open deviation

  Scenario: AC1 A non-engine writer can place a case
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then the response is 201
    Then the case is in queue "MTG-BKK-PRI"
    Then the assignment and the case record show SY-AGENT as the identity that made the change

  Scenario: AC2 The same rules still apply
    Given queue "MTG-BKK-PRI" holds owners "U-5001" with 150 open cases and "U-5002" with 149 open cases
    When the model places case "RW-2026-000501" on it
    Then the system gives the case to "U-5002" by round robin, skipping "U-5001" at the cap
    Then the case status becomes ASSIGNED
    When both owners hold 150 open cases and the model places case "RW-2026-000502"
    Then case "RW-2026-000502" is in queue "MTG-BKK-OVF" with no owner and status NEW

  Scenario: AC3 Every placement is logged
    When the model places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then one decision log entry exists with decision code D6, model version "MDL-SYN-PRIORITY 1.4.0", the reason "High cure score", the caller identity SY-AGENT and final call "PLACED MTG-BKK-PRI"
    Then the entry, the case change, the assignment and the events commit in one transaction

  Scenario: AC4 It is off until a consumer exists
    Given feature flag "rwb.casewf.queue-placement" is off
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the response is 404 with message MSG-P2-025
    Then the case and the decision log are unchanged
    Then the contract test and the tests of this story pass with the flag on in SIT

  Scenario: AC5 A caller that is not approved is refused
    When SY-AGENT places a case with modelOrAgent "MDL-SYN-UNLISTED"
    Then the response is 422 with message MSG-P2-020
    Then nothing changes

  Scenario: AC6 A required field is empty
    When SY-AGENT places case "RW-2026-000501" with no reason
    Then the response is 422 with message MSG-GEN-001 for field reason
    Then nothing changes

  Scenario: AC7 A case already in the queue
    Given case "RW-2026-000501" was placed on queue "MTG-BKK-PRI" at 08:10
    When the same request is sent again at 08:11
    Then the response is 409 with message MSG-P2-024
    Then there is still one assignment and one decision log entry for the placement

  Scenario: AC8 A closed case is refused
    Given case "RW-2026-000503" has status CLOSED
    When the model places it on queue "MTG-BKK-PRI"
    Then the response is 409 with message MSG-P3-005
    Then nothing changes

  Scenario: AC9 A case with an open deviation stays with its handler
    Given case "RW-2026-000504" has deviation X2 open and is in the deviation handler's queue
    When the model places it on queue "MTG-BKK-PRI"
    Then the response is 409 with message MSG-P2-021
    Then the case stays in the deviation handler's queue

  Scenario: AC10 An unknown queue or case
    When the model places case "RW-2026-000501" on a queue ID that does not exist
    Then the response is 404 with message MSG-P4-003

  Scenario: AC11 Two placements at the same time
    When two placements of case "RW-2026-000501" to queues "MTG-BKK-PRI" and "MTG-BKK-CO" commit at the same time
    Then one succeeds with 201
    Then the system refuses the other with 409 and message MSG-GEN-004
    Then the case is in exactly one queue with one open assignment

  Scenario: AC12 A case that already has an owner
    Given case "RW-2026-000505" has status IN_PROGRESS, owner "U-5100" and queue "MTG-BKK-CO"
    When the model places it on queue "MTG-BKK-PRI"
    Then the assignment of "U-5100" ends and a new owner is chosen by the queue's method
    Then the case status stays IN_PROGRESS
    Then events CaseAllocated and CaseTransferred are written to the outbox
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a caller in the approved callers list, under the service identity listed for it, may place a case | REQ-CWC-019; configuration key rwb.casewf.placement.approved-callers |
| BR2 | The caller passes the same access check as a person: Queue and allocation C in the permission matrix in force | REQ-CWC-018; REQ-ACA-010; CTL-09 |
| BR3 | The owner is chosen by the queue's assignment method within its caseload cap; when every owner is at the cap the case goes to the overflow queue | queue.assignment_method, capacity_cap, overflow_queue_id; DL23 |
| BR4 | A case with an open deviation stays with the deviation handler | R-DEV-01 |
| BR5 | Every placement writes one decision log entry in the same transaction as the change, with the caller identity, the reason and the model or agent version | NFR-078; Principle 5; CTL-06 |
| BR6 | A decision that cannot be written to the decision log does not proceed | R-UNI-39; Principle 5 |
| BR7 | A case closed or already in the target queue is not placed | LOV-CASE-STATUS; MSG-P3-005 |
| BR8 | The interface is off by feature flag until the first caller is approved | REQ-CWC-019; DT11 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| New | Allocation rule matched (placement) | An owner below the cap | Assigned |
| New | Allocation rule matched (placement) | Every owner at the cap | New, in the overflow queue |
| Assigned, In progress, Waiting customer, Waiting partner, Waiting approval | Placement on another queue | An owner below the cap | Unchanged status, new owner |
| On hold | Placement | deviation_open = true | On hold, refused (MSG-P2-021) |
| Closed | Placement | Always | Closed, refused (MSG-P3-005) |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Places cases once the matrix gives it Queue and allocation C and its caller is approved |
| SY-CASEWF, case workflow module | Updates the case, writes the assignment, publishes the events |
| SY-DECLOG, decision log writer | Writes the placement entry |
| RW-TEAMMGR, team manager | Holds Queue and allocation CRUA; reads placed cases in team queues |
| RW-COE, center of excellence analyst | Requests a caller entry in the approved callers list |
| RW-RISK, risk and model risk officer | Approves a caller entry before it is loaded |
| RW-PLATADM, platform administrator | Switches the feature flag on after approval |
| RW-SECADM, security administrator | Loads the permission matrix version that grants the caller's identity Queue and allocation C |
| No approval level from the delegation of authority applies | A placement moves work; it does not approve a treatment |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-005 | recovery_case | status | Read and write |
| DF-CAS-009 | recovery_case | owner_user_id | Write |
| DF-CAS-010 | recovery_case | queue_id | Read and write |
| DF-CAS-011 | recovery_case | team_code | Write |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-006 | queue | assignment_method | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-008 | queue | overflow_queue_id | Read |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Write |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |
| DF-REF-042 | permission | capability_area | Read |
| DF-REF-043 | permission | letters | Read |

The service identity of the caller is written to the standard column created_by of the assignment and to updated_by of the case. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/queues/{queueId}/placements** (operationId postQueuesQueueidPlacements)

| Item | Value |
|---|---|
| Path | queueId (uuid) |
| Request | PlacementRequest: caseId (uuid, required), reason (text, required, 1 to 1,000 characters), modelOrAgent (required, a caller code in the approved list), version (required, 1 to 40 characters) |
| Response 201 | Assignment of the new owner. When every owner is at the cap no owner is set; the response is then the placement result with the overflow queue ID and no assignment (response change recorded in the additions file) |
| 401 | No valid session (MSG-P4-001) |
| 403 | Identity lacks Queue and allocation C (MSG-P4-002) |
| 404 | Flag off (MSG-P2-025); queue or case not found (MSG-P4-003) |
| 409 | Case already in the queue (MSG-P2-024), case closed (MSG-P3-005), open deviation (MSG-P2-021), version changed (MSG-GEN-004) |
| 422 | Field empty (MSG-GEN-001), length out of range (MSG-GEN-002), caller not approved (MSG-P2-020) |
| 503 | Decision log write failed (MSG-P7-003) |
| Authorization | Queue and allocation, right C; scope All for service identities |
| Idempotency | One placement per case and queue while the case is in that queue; a repeat returns 409 MSG-P2-024 and writes nothing |
| Events published | EV-02 CaseAllocated; EV-04 CaseTransferred when the case had an owner; both through the outbox in the same transaction |

**Interfaces called**

```java
// P7, package recovery.decision.writer (RWB-E1-027); Propagation.MANDATORY
DecisionLogEntryRef DecisionLogWriter.write(DecisionLogRecord record)
    throws DecisionLogRecordInvalidException, DecisionLogUnavailableException;
// P3, package recovery.casewf.allocation (RWB-E1-020); this story adds the method below,
// reusing the owner choice, cap and overflow logic of allocate()
AllocationOutcome AllocationService.assignInQueue(UUID caseId, UUID queueId, String sourceIdentity);
```

## 13. Solution plan

**Package.** The story is in the P2 backlog. The endpoint is P3 in the API specification and the queue and case tables are P3's, so the code is in folder `recovery/casewf/placement`, Java package `<ACE base package>.recovery.casewf.placement`. No front end change.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PlacementController | Controller | Implements postQueuesQueueidPlacements; flag check, validation, error mapping |
| PlacementService | Service | BR1 and BR4 to BR7; the case, the assignment, the events and the decision log entry in one transaction |
| ApprovedCallerList | Service | Reads the approved callers list from the configuration service |
| AllocationService | Published interface | From RWB-E1-020; this story adds assignInQueue for a given queue |
| DecisionLogWriter | Published interface | From RWB-E1-027 |
| PlacementRepository | Repository | Reads and writes recovery_case and assignment with the optimistic lock version |

**Database.** Reads queue; reads and writes recovery_case (status, owner_user_id, queue_id, team_code, version); writes assignment. Adds `CREATE UNIQUE INDEX uk_assignment_open_case ON assignment (case_id) WHERE ended_at IS NULL AND task_id IS NULL` through a migration in the P3 folder, so a case has one open case assignment. No new table.

**Configuration and reference data.** Approved callers list rwb.casewf.placement.approved-callers (empty at go-live, assumed; loaded by RW-REFADM after RW-RISK approval); queue table with methods, caps and overflow queues (DL23); permission matrix version (RW-SECADM); LOV-DECISION value D6.

**Build steps**

1. Regenerate the server interface for postQueuesQueueidPlacements with the result variant for overflow.
2. Write ApprovedCallerList and the controller validation (AC5, AC6) and the flag check (AC4).
3. Write PlacementService with the decision log write in the same transaction and the refusals (AC3, AC7 to AC10).
4. Add AllocationService.assignInQueue and test the cap and overflow (AC2) and the case with an owner (AC12).
5. Add the unique open assignment index and the optimistic lock test (AC11).
6. Add the access test with the matrix in force and the decision log failure test.

**Feature flag.** `rwb.casewf.queue-placement`, default off. Off returns 404 with MSG-P2-025 and touches nothing.

**Done when.** The tests in section 16 pass with the flag on in SIT, and the flag is off in UAT and production at the release.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is empty | Enter {field}. |
| MSG-GEN-002 | reason or version outside its length | {field} must be between {min} and {max}. |
| MSG-P2-024 | The case is already in the target queue (new) | This case is already in {queue}. |
| MSG-P2-025 | The feature flag is off (new) | Queue placement by models and agents is switched off. |
| MSG-P2-020 | The caller is not in the approved callers list (new) | {caller} is not approved to place cases on queues. |
| MSG-P2-021 | The case has an open deviation (new) | This case has an open deviation and stays with the deviation handler. |
| MSG-P3-005 | The case is closed | This case cannot move to {state} from {current}. |
| MSG-GEN-004 | The case changed during the placement | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Identity lacks Queue and allocation C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Queue or case not found | This case is not in your scope. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. A placed case appears in its queue on SCR-07 Team queues and SCR-02 Case list like any other case; the decision log query (SCR-38) shows the placement entry with the caller and version.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-036-01 | AC1, BR1, BR2 | System | Approved caller MDL-SYN-PRIORITY under SY-AGENT; NEW case |
| TC-E2-036-02 | AC2, BR3 | System | Owners at 150 and 149; then both at 150 |
| TC-E2-036-03 | AC3, BR5 | System | One placement; decision log entry fields checked |
| TC-E2-036-04 | AC4, BR8 | System | Flag off |
| TC-E2-036-05 | AC5, BR1 | System | Caller MDL-SYN-UNLISTED |
| TC-E2-036-06 | AC6 | System | Request with no reason |
| TC-E2-036-07 | AC7, BR7 | System | Same request sent twice |
| TC-E2-036-08 | AC8, BR7 | System | CLOSED case |
| TC-E2-036-09 | AC9, BR4 | System | Case with X2 open |
| TC-E2-036-10 | AC10 | System | Queue ID that does not exist |
| TC-E2-036-11 | AC11 | System | Two placements against one case version |
| TC-E2-036-12 | AC12, BR3 | System | IN_PROGRESS case with owner U-5100 |
| TC-E2-036-13 | Access | Access | SY-AGENT under the production matrix (Queue and allocation R); refused with MSG-P4-002 |
| TC-E2-036-14 | Principle 5 | Resilience | Decision log write forced to fail; 503 MSG-P7-003; case, assignment and outbox unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: approved callers, caps, methods and overflow queues are data.
- No personal data in logs, tests or prompts; the reason text is the caller's code or phrase and holds no customer data.
- No read of another module's tables: the decision log is written through DecisionLogWriter.
- A model or agent never bypasses the allocation engine or the access check.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-017 | A queue accepts a write from a model or an agent with the case and the reason | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-DEV-01 | TC-E2-036-01, TC-E2-036-02, TC-E2-036-06 to TC-E2-036-12 |
| REQ-CWC-018 | A model or agent passes the same permission checks and its write is logged with its version | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-UNI-39 | TC-E2-036-03, TC-E2-036-13, TC-E2-036-14 |
| REQ-CWC-019 | The interface ships behind a feature flag | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-04, TC-E2-036-05 |
| REQ-CWC-020 | Model and rule work in the same queue, in one priority order | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-01 |

## 19. Out of scope

- Score and priority on the placement and queue order by priority (REQ-CWC-020): added with the first approved model consumer, in the epic that switches the flag on.
- The model or agent that calls the interface: the P10 agent runtime stories, for example RWB-E2-028.
- Granting SY-AGENT Queue and allocation C in the production matrix: a permission matrix change under RWB-E1-037.
