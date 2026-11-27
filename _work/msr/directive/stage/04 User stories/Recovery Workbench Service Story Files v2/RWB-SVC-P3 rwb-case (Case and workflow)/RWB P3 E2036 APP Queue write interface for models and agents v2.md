# RWB-P3-E2036-APP Queue write interface for models and agents

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2036-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-036 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-AN |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E2036-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2036-CON (contract version Not specified in the source documents (DOR-RWB-P3-E2036-APP-23)); P3 case-read and P4 authorise contract stories at wave 2 entry (GAP-2412) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-024, FR-P3-037) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-036 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E2036-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 14 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **an approved model or agent to place a case on a queue through one command of rwb-case, under its own service identity and the queue's own rules, with the placement written to the decision record in the same transaction**, so that **analytical output reaches a person the next working day instead of through a weekly manual step**.

This slice is the rwb-case build of that behaviour. The legacy interface worked inside the monolith, called the allocation engine in process and left the decision entry to another module; the target keeps the same business behaviour and moves each mechanical part to its new owner:

- the command is served by rwb-case on its own base `/api/recovery/case/v1` as `POST /queues/{queueId}/placements` (operationId `postQueuesQueueidPlacements`, DP-13), because the queue, the case and the assignment are P3 tables under the Ownership Map;
- the caller arrives with its service identity: the rwb-integration contract RWB-P2-E2036-CON maps the caller code and its type to the identity, and this story builds against that contract and its consumer stub (DP-11, one hop, 2 s timeout);
- the person permission is the **Queue and allocation C** right of the caller's identity, read through the rwb-access authorise contract with the platform guard library (DP-08), so a model or an agent passes the same check as a person;
- the approved callers list is data in the parameters of rwb-case (DP-06, key `rwb.casewf.placement.approved-callers`), never a constant in code;
- the owner choice, the caseload cap of 150 and the overflow queue are reused from the allocation and assignment engine of RWB-P3-E1020-APP through `AllocationService.assignInQueue`, so a placement and the morning run obey one set of rules;
- the case row, the assignment row, the outbox rows and the local decision record are written in one `rwb_case` transaction (DP-01, DP-03, DP-09), and the outbox carries `CaseAllocated` and `CaseTransferred` on `rwb.case.events.v1` and the record on `rwb.decision-record.v1` (DP-14);
- the case's own `deviation_open` flag refuses a case with an open deviation, so no call to rwb-deviation is made;
- the migration is one Flyway step in `rwb_case` that adds the unique open-assignment index (DP-15), and there is no front end: a placed case appears in the existing queue and case list screens like any other case.

### 2. Business rationale

Model scores and agent findings reach the queues today through a weekly file that a person loads by hand, so a case flagged on Monday is worked the following week. The interface lets an approved caller place a case on a queue the day the decision is made, while the queue's allocation method, caseload cap and the role to permission matrix apply as they do to any case, and every placement is written to the decision record with the caller and its version. The business measure is the time from a model decision to the case reaching a queue, from up to 7 days today to the same day.

The legacy story assumes three things that the target splits across services: the caller list and the flag are configuration of the case workflow module, the queue and case tables are the workbench's own, and the decision log belongs to another module. In the target the parameter, reference-data and case tables stay with rwb-case (DP-01, DP-06, DP-07); the caller's identity is resolved from the rwb-integration contract RWB-P2-E2036-CON, published by the integration service that owns the interface catalogue and the outside world; the Queue and allocation C right is checked through rwb-access with the platform guard library (DP-08); and the decision entry becomes a local decision record written in the same transaction as the change and then published on the shared `rwb.decision-record.v1` topic for the central ledger in rwb-decision (DP-03). The unit of work is one placement command, not a batch and not a workflow: no Temporal workflow is started here, and CaseWorkflow learns the new queue and owner from `CaseAllocated` or `CaseTransferred` like any other state change.

Nothing about the business answer changes. An approved caller places a case; the queue's own method picks the owner; an owner at the cap is skipped; when every owner is at the cap the case waits in the overflow queue; a closed case, a case already in the queue and a case with an open deviation are refused; and a placement that cannot be recorded is not made.

It meets REQ-CWC-017, REQ-CWC-018 and REQ-CWC-019, and serves control CTL-09 through the role check of REQ-ACA-010. It owns no legacy acceptance criterion: the twelve criteria of RWB-E2-036 are exercised across services by RWB-ITG-E2036-ITG and by the other slices of this key, and the fourteen criteria in section 7 are new for this service change.

### 3. Preconditions

- RWB-P2-E2036-CON is published: the caller-identity resource shape (caller code, caller type MODEL or AGENT, service identity), its read operation, its error envelope and its contract stub. This story builds against that contract and its consumer stub and never resolves a caller identity from an rwb-integration table.
- The `rwb_case` schema baseline exists from the Epic 1 stories: `recovery_case`, `queue`, `queue_member`, `assignment` and `task` from RWB-P3-E1018-APP and RWB-P3-E1019-APP, and the allocation and assignment engine with `AllocationService.assignInQueue`, the owner choice, the cap and the overflow of RWB-P3-E1020-APP.
- The local decision-record library and the shared topic `rwb.decision-record.v1` are published by the platform contract story of DP-03, and the outbox, inbox and idempotency libraries by the platform contract story of DP-09; the platform guard library with the authorise client by DP-08. These platform dependencies are held by the platform stories and are not repeated in the metadata rows, which carry only the build-against contract of the caller identity.
- The parameters of rwb-case are readable through its own parameters contract (DP-06) and hold the approved callers list under `rwb.casewf.placement.approved-callers` and the placement flag under `rwb.casewf.queue-placement`. The list is empty at go-live; RW-COE requests an entry and RW-RISK approves it before it is loaded (GAP-0735; ASM-1308).
- The permission matrix in force gives the caller's service identity Queue and allocation C. The matrix version PM-SIT-02 used in the tests does; the production matrix gives SY-AGENT R only today, so a matrix version change by RW-SECADM is needed before the first caller is switched on (GAP-0735; ASM-1309).
- The target queue exists with its assignment method, caseload cap and overflow queue (DL23; caseload cap 150): queue "MTG-BKK-PRI" of team "MTG-BKK" uses method ROUND_ROBIN with cap 150 and overflow queue "MTG-BKK-OVF".
- The reference-data list LOV-DECISION holds value D6 for a queue placement, read through the reference-data contract of rwb-case (DP-07).
- The migration of section 13 has run in `rwb_case`: the unique index `uk_assignment_open_case` on `assignment (case_id) WHERE ended_at IS NULL AND task_id IS NULL` exists, so a case holds at most one open case assignment whatever two callers do at the same moment.
- A non-human caller is admitted on scope ALL only: the scope of its role must be ALL, the presented team code is recorded in the access entry and compared with nothing, and any other scope is refused with SCOPE_NOT_ALL (GAP-0959).
- The caller code and its type are recorded in the access entry without being resolved to a role; the subject is resolved through the role of the service identity at the matrix version in force, and a subject whose role class is not NON_HUMAN_ACTOR is refused (GAP-0960).
- The command runs as the rwb-case login (DP-02). The per-service login name is held by the platform DB story; its value is Not specified in the source documents (GAP-0735; ASM-1315).

### 4. Flow

1. An approved caller — a model job or an agent under its service identity — sends `POST /api/recovery/case/v1/queues/{queueId}/placements` with `caseId`, `reason`, `modelOrAgent` and `version`. The request carries the session of the caller's service identity; the identity is resolved from the caller code and its type through the consumer stub of RWB-P2-E2036-CON, and no call to rwb-integration is made at run time (GAP-0735; ASM-1311).
2. PlacementController reads the placement flag through the parameters of rwb-case. Flag off: the response is 404 with MSG-P2-025 and nothing is read from the case or written anywhere.
3. AccessGuard checks the Queue and allocation C right of the resolved service identity through `POST /api/recovery/access/v1/authorise` with the platform guard library: one hop, 2 s timeout, answer cached per identity and right (DP-08).
4. PlacementController validates the four fields: `caseId` and `reason` and `modelOrAgent` and `version` are required, `reason` is 1 to 1,000 characters, `version` is 1 to 40 characters. An empty field fails at once with MSG-GEN-001 naming that field and a length outside the range with MSG-GEN-002.
5. ApprovedCallerList answers whether `modelOrAgent` is an approved caller code for the resolved service identity, from the parameters list of rwb-case. A caller code that is not in the list for this identity is refused with 422 and MSG-P2-020; a caller code approved for another identity is refused the same way.
6. PlacementService reads the queue row from `rwb_case.queue` — method, cap, overflow queue, team — and the case row from `rwb_case.recovery_case` with its optimistic lock version, and refuses in this order: a queue or a case that does not exist (404, MSG-P4-003); a closed case (409, MSG-P3-005); a case already in the target queue (409, MSG-P2-024, which also covers a repeated call); a case whose own `deviation_open` flag is true (409, MSG-P2-021), which stays with the deviation handler of R-DEV-01.
7. PlacementService builds the decision record content: decision code D6, the caller code with its version as "model version", the reason, the caller's service identity and the target queue code; the content is not yet written.
8. PlacementService sets the case queue and team and calls `AllocationService.assignInQueue(caseId, queueId, sourceIdentity)`, which reuses the owner choice, the caseload cap of 150 and the overflow of RWB-P3-E1020-APP. The answer is either a new owner — the case status becomes ASSIGNED when it was NEW — or no owner, in which case the case goes to the overflow queue, keeps its status and raises no assignment.
9. In one `rwb_case` transaction: the previous open assignment of the case is ended (`ended_at`, status), the new assignment row is written with reason ALLOCATION and `created_by` set to the caller's service identity, `recovery_case` is updated (queue, team, owner where one was chosen, status, `updated_by`, version), the outbox rows are inserted for `CaseAllocated` and, when the case had an owner before the call, `CaseTransferred`, and the local decision record is written last with propagation MANDATORY so it joins the caller's transaction. Any failure rolls the whole placement back.
10. On commit the response is 201: the assignment of the new owner, or, when every owner was at the cap, the placement result with the overflow queue ID, `overflow` true, no assignment and the decision record reference (GAP-0735; ASM-1310).
11. The outbox relay publishes `rwb.case.CaseAllocated.v1` and `rwb.case.CaseTransferred.v1` on `rwb.case.events.v1` keyed by caseId, and the same decision record on `rwb.decision-record.v1` through the CloudEvents envelope; no personal data is in any payload and the caller is named by its code and its service identity only (DP-09, DP-14).
12. CaseWorkflow, the parent workflow of the case, observes the new queue and owner through the case events and its own case read; it is not started by this command and no workflow instance is created, signalled or updated here.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The placement flag is off | 404 at the first check; nothing is read and nothing changes | MSG-P2-025 | AC4 |
| X2 | The caller code is not in the approved callers list of the resolved identity | 422; nothing changes | MSG-P2-020 | AC5 |
| X3 | `caseId`, `reason`, `modelOrAgent` or `version` is empty | 422 naming the field; nothing changes | MSG-GEN-001 | AC6 |
| X4 | The case is already in the target queue, including a repeated call | 409; no second assignment, no second decision record | MSG-P2-024 | AC7 |
| X5 | The case is closed | 409; nothing changes | MSG-P3-005 | AC8 |
| X6 | The case has an open deviation (`deviation_open = true`) | 409; the case stays in the deviation handler's queue and keeps its owner (R-DEV-01) | MSG-P2-021 | AC9 |
| X7 | The queue or the case does not exist, or the case is out of the caller's scope | 404; nothing changes | MSG-P4-003 | AC10 |
| X8 | Every owner in the queue is at the caseload cap | The case is placed in the overflow queue with no owner and its status unchanged; the response carries the overflow queue ID and no assignment | None | AC2 |
| X9 | Two placements of the same case commit at the same time | One commits with 201; the other is refused by the unique open-assignment index or the optimistic version and gets 409 | MSG-GEN-004 | AC11 |
| X10 | The caller's service identity lacks Queue and allocation C | 403 before any read of the case; nothing changes | MSG-P4-002 | AC13 |
| X11 | The decision record write fails inside the transaction | 503; the whole placement rolls back: no assignment, no case change, no outbox row; an incident is raised (R-UNI-39) | MSG-P7-003 | AC14 |

The open deviation of X6 is read from `recovery_case.deviation_open` (DF-CAS-019), the flag that rwb-deviation sets through its own events and that the full case record view already shows (RWB-P3-E2015-APP); this story makes no synchronous call to rwb-deviation (GAP-0735; ASM-1314). X9 is refused twice over: the unique open-assignment index of section 13 makes a second open case assignment impossible, and the optimistic version on `recovery_case` makes a second write against the same version fail.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the consumer stub of RWB-P2-E2036-CON and the platform guard, decision-record and outbox libraries; the owner choice, the cap and the overflow arrive with RWB-P3-E1020-APP, so no work order sits inside another team's lane |
| Negotiable | The approved callers, the flag, the queues, the methods, the caps and the overflow queues are rows; the story fixes the behaviour of the command, not the values |
| Valuable | A daily model or agent decision reaches a person the same day instead of the following week |
| Estimable | One endpoint, one controller, one service, one list read, one allocation call, one transaction, one migration, no screen |
| Small | Fits two weeks with its tests |
| Testable | Each of the fourteen criteria of section 7 is one automated test; the caller identity and the access answer are stubbed by the contract fakes of section 12.8 |

The patterns of section 13 add H and C dependencies — the platform kits of DP-03, DP-08, DP-09, DP-14 and DP-15 and the rwb-access, rwb-decision and rwb-case contract stories. They are held by the platform and service contract stories and are not repeated in the metadata rows, which carry only the legacy contract dependency RWB-P2-E2036-CON (GAP-0735; ASM-1313).

### 7. Acceptance criteria

```gherkin
Feature: Queue write interface for models and agents

  Background:
    Given feature flag "rwb.casewf.queue-placement" is on
    Given the permission matrix version "PM-SIT-02" gives service identity SY-AGENT Queue and allocation C
    Given the approved callers list holds caller "MDL-SYN-PRIORITY" of type MODEL for service identity SY-AGENT
    Given queue "MTG-BKK-PRI" of team "MTG-BKK" uses method ROUND_ROBIN with caseload cap 150 and overflow queue "MTG-BKK-OVF"
    Given the rwb-integration contract mock returns caller "MDL-SYN-PRIORITY" of type MODEL for service identity SY-AGENT
    Given case "RW-2026-000501" has status NEW, no owner, no open deviation

  Scenario: AC1 A placement is accepted and the owner is chosen by the queue method (new, D-RCV-60)
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then the response is 201 with the assignment of the new owner
    Then the case is in queue "MTG-BKK-PRI" with that owner and status "ASSIGNED"
    Then the assignment and the case record show SY-AGENT in created_by and updated_by
    Then no Temporal workflow instance is created or signalled by the command

  Scenario: AC2 The cap and the overflow still apply (new, D-RCV-60)
    Given queue "MTG-BKK-PRI" holds owners "U-5001" with 150 open cases and "U-5002" with 149 open cases
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the system gives the case to "U-5002" by round robin, skipping "U-5001" at the cap
    Then the case status becomes "ASSIGNED"
    Given both owners now hold 150 open cases
    When SY-AGENT places case "RW-2026-000502" on queue "MTG-BKK-PRI"
    Then the response is the placement result with overflow queue ID "MTG-BKK-OVF", overflow true and no assignment
    Then case "RW-2026-000502" is in queue "MTG-BKK-OVF" with no owner and status "NEW"

  Scenario: AC3 One decision record is written in the same transaction (new, D-RCV-60)
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then one decision record exists with decision code D6, model version "MDL-SYN-PRIORITY 1.4.0", reason "High cure score", caller identity SY-AGENT and final call "PLACED MTG-BKK-PRI"
    Then the decision record, the case change, the assignment and the outbox rows commit in one rwb_case transaction
    Then the record is published on rwb.decision-record.v1 after the commit

  Scenario: AC4 It is off until a consumer exists (new, D-RCV-60)
    Given feature flag "rwb.casewf.queue-placement" is off
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the response is 404 with message MSG-P2-025
    Then the case and the decision record are unchanged
    Then no assignment row is written

  Scenario: AC5 A caller that is not approved is refused (new, D-RCV-60)
    Given the rwb-integration contract mock returns caller "MDL-SYN-UNLISTED" of type MODEL for service identity SY-AGENT
    When SY-AGENT places a case with modelOrAgent "MDL-SYN-UNLISTED"
    Then the response is 422 with message MSG-P2-020
    Then nothing changes

  Scenario: AC6 A required field is empty (new, D-RCV-60)
    When SY-AGENT places case "RW-2026-000501" with no reason
    Then the response is 422 with message MSG-GEN-001 for field reason
    Then nothing changes

  Scenario: AC7 A case already in the queue (new, D-RCV-60)
    Given case "RW-2026-000501" was placed on queue "MTG-BKK-PRI" at 08:10
    When the same request is sent again at 08:11
    Then the response is 409 with message MSG-P2-024
    Then there is still one assignment and one decision record for the placement

  Scenario: AC8 A closed case is refused (new, D-RCV-60)
    Given case "RW-2026-000503" has status CLOSED
    When SY-AGENT places it on queue "MTG-BKK-PRI"
    Then the response is 409 with message MSG-P3-005
    Then nothing changes

  Scenario: AC9 A case with an open deviation stays with its handler (new, D-RCV-60)
    Given case "RW-2026-000504" has deviation X2 open and is in the deviation handler's queue
    When SY-AGENT places it on queue "MTG-BKK-PRI"
    Then the response is 409 with message MSG-P2-021
    Then the case stays in the deviation handler's queue with its own owner
    Then no call to rwb-deviation is made

  Scenario: AC10 An unknown queue or case (new, D-RCV-60)
    When SY-AGENT places case "RW-2026-000501" on a queue ID that does not exist
    Then the response is 404 with message MSG-P4-003
    Then nothing changes
    When SY-AGENT places a case ID that does not exist on queue "MTG-BKK-PRI"
    Then the response is 404 with message MSG-P4-003

  Scenario: AC11 Two placements at the same time (new, D-RCV-60)
    When two placements of case "RW-2026-000501" to queues "MTG-BKK-PRI" and "MTG-BKK-CO" commit at the same time
    Then one succeeds with 201
    Then the system refuses the other with 409 and message MSG-GEN-004
    Then the case is in exactly one queue with one open assignment
    Then exactly one decision record exists for the pair of calls

  Scenario: AC12 A case that already has an owner (new, D-RCV-60)
    Given case "RW-2026-000505" has status IN_PROGRESS, owner "U-5100" and queue "MTG-BKK-CO"
    When SY-AGENT places it on queue "MTG-BKK-PRI"
    Then the open assignment of "U-5100" ends and a new owner is chosen by the queue's method
    Then the case status stays "IN_PROGRESS"
    Then events CaseAllocated and CaseTransferred are written to the outbox in the same transaction

  Scenario: AC13 The identity lacks Queue and allocation C (new, D-RCV-60)
    Given the rwb-access contract mock returns Queue and allocation R only for service identity SY-AGENT
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the response is 403 with message MSG-P4-002
    Then the case is not read and nothing changes

  Scenario: AC14 The decision record write fails (new, D-RCV-60)
    Given the decision-record store is unavailable for the placement
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the response is 503 with message MSG-P7-003
    Then the case queue, the case owner and the case status are unchanged
    Then no assignment row and no outbox row is written for the placement

  Scenario: AC15 The decision code and the identity come from the contracts (new, D-RCV-60)
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the decision code of the placement is D6 of LOV-DECISION, read through the reference-data contract
    Then the caller identity is resolved through the rwb-integration contract and the right through rwb-access
    Then the command reads no table outside rwb_case

  Scenario: AC16 A call without a valid service identity is refused (new, D-RCV-60)
    When a placement of case "RW-2026-000501" on queue "MTG-BKK-PRI" is sent without a valid service identity
    Then the response is 401 with message Not specified in the source documents (NEWAC-RWB-P3-E2036-APP-AC16)
    Then nothing changes
```

AC1 to AC16 are new for the rwb-case slice: the legacy AC1 to AC12 of RWB-E2-036 are exercised across services by RWB-ITG-E2036-ITG and the other slices of this key, and no slice of this key was allocated the legacy acceptance criteria (GAP-0735; ASM-1307).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a caller in the approved callers list, under the service identity listed for it, may place a case | REQ-CWC-019; configuration key rwb.casewf.placement.approved-callers |
| BR2 | The caller passes the same access check as a person: Queue and allocation C in the permission matrix in force | REQ-CWC-018; REQ-ACA-010; CTL-09 |
| BR3 | The owner is chosen by the queue's assignment method within its caseload cap; when every owner is at the cap the case goes to the overflow queue | queue.assignment_method, capacity_cap, overflow_queue_id; DL23 |
| BR4 | A case with an open deviation stays with the deviation handler | R-DEV-01 |
| BR5 | Every placement writes one decision record in the same transaction as the change, with the caller identity, the reason and the model or agent version | NFR-078; Principle 5; CTL-06 |
| BR6 | A decision that cannot be written to the decision record does not proceed | R-UNI-39; Principle 5 |
| BR7 | A case closed or already in the target queue is not placed | LOV-CASE-STATUS; MSG-P3-005 |
| BR8 | The interface is off by feature flag until the first caller is approved | REQ-CWC-019; DT11 |
| BR9 | The caller's service identity is resolved from the caller code and its type through the rwb-integration contract; rwb-case holds no interface catalogue | DP-11; RWB-P2-E2036-CON |
| BR10 | The open deviation is read from the case's own `deviation_open` flag, not from a call to rwb-deviation | DF-CAS-019; DP-01 |
| BR11 | A case holds at most one open case assignment; the unique index `uk_assignment_open_case` enforces it whatever two callers do at the same moment | Legacy RWB-E2-036 section 13; DP-15 |
| BR12 | The placement is one synchronous command: no workflow is started, signalled or updated by it, and the case events are the only hand-over to CaseWorkflow | DP-09; Architecture v5 slide 14 |
| BR13 | The decision code of a placement is D6 of LOV-DECISION, read through the reference-data contract | LOV-DECISION; DP-07 |
| BR14 | The command writes nothing outside `rwb_case` and reads no other service's table; the right comes from rwb-access and the caller identity from the rwb-integration contract | DP-01, DP-08; ADR-010 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| New | Allocation rule matched (placement) | An owner below the cap | Assigned |

These are case statuses (`recovery_case.status`, LOV-CASE-STATUS); the change of queue and owner is not a status change of its own, and a case placed in the overflow queue keeps the status it had. The transition to Assigned writes the case row, the assignment row, the outbox row and the decision record in one transaction; a placement on the overflow queue writes the case row, the decision record and the `CaseAllocated` outbox row and no assignment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Places cases once the matrix gives it Queue and allocation C and its caller is in the approved callers list |
| SY-CASEWF, case workflow module of rwb-case | Updates the case, writes the assignment, writes the outbox rows and the decision record (Case record CRU; Queue and allocation CRU) |
| The decision-record library identity (DP-03) | Writes the local decision record inside the caller's transaction and publishes it for the central ledger (Decision log C) |
| The rwb-access guard (DP-08) | Answers the Queue and allocation C right and the scope of the caller's service identity (Access R) |
| RW-TEAMMGR, team manager | Holds Queue and allocation CRUA; reads placed cases in the team queues |
| RW-COE, center of excellence analyst | Requests a caller entry in the approved callers list |
| RW-RISK, risk and model risk officer | Approves a caller entry before it is loaded |
| RW-PLATADM, platform administrator | Switches the feature flag on after approval |
| RW-SECADM, security administrator | Loads the permission matrix version that grants the caller's identity Queue and allocation C |
| No approval level from the delegation of authority applies | A placement moves work; it does not approve a treatment |

The command runs as the rwb-case login (DP-02); its name, its grants and its secret reference are Not specified in the source documents (GAP-0735; ASM-1315).

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read; the row carries the optimistic lock version, read and written on every placement |
| DF-CAS-002 | recovery_case | case_no | Read, for the decision record content |
| DF-CAS-005 | recovery_case | status | Read and write |
| DF-CAS-009 | recovery_case | owner_user_id | Write |
| DF-CAS-010 | recovery_case | queue_id | Read and write |
| DF-CAS-011 | recovery_case | team_code | Write |
| DF-CAS-019 | recovery_case | deviation_open | Read, for the refusal of X6 |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-006 | queue | assignment_method | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-008 | queue | overflow_queue_id | Read |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields, including case_id and ended_at of the ended previous assignment | Write, and read for the open-assignment check |
| DF-WRK-018 | task | case_id (the task-less term of the open-assignment index) | Read |
| DF-REF-042 | permission | capability_area | Read, through the rwb-access contract only |
| DF-REF-043 | permission | letters | Read, through the rwb-access contract only |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | `rwb.casewf.placement.approved-callers`, `rwb.casewf.queue-placement` | Read |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-DECISION value D6 | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision) | all fields | Write locally; the central entry is sealed by rwb-decision |
| The outbox (DP-09 library) | outbox_event | event name, payload, key caseId | Write |

The service identity of the caller is written to the standard column `created_by` of the assignment and to `updated_by` of the case. The permission fields DF-REF-042 and DF-REF-043 are not read from a table by this story: the right arrives as the answer of `POST /api/recovery/access/v1/authorise`, and `permission` is owned by rwb-access (P4) under the Ownership Map. The caller code, its type and its version are request values and are copied into the decision record; no copy of an interface catalogue row is written into `rwb_case`, and no foreign key crosses a schema (DP-01).

Field IDs are those in the Logical Data Model and Data Dictionary v9. `decision_log_entry` is owned by rwb-decision (P7) and is reached only through the shared topic; the local record is the library object of DP-03, written in `rwb_case`. The name `uk_assignment_open_case` is a unique index, not a field or entity; `permission_matrix` and `interface_catalogue` are tables of rwb-access and rwb-integration that this story reads through no statement, and they are held by their owning services.

### 12. Contract

Contract baseline (GAP-0670, GAP-0671, GAP-0957). The placement path `POST /api/recovery/case/v1/queues/{queueId}/placements` is provided by rwb-case under this story and keeps the behaviour of sections 4 and 12.1; the rwb-integration story RWB-P2-E2036-CON consumes it and does not own it. The rwb-integration admission operation forwards to this path and is not part of this story. The three consumed contracts are the rwb-case placement, the rwb-case parameters contract under the key `rwb.casewf.placement.approved-callers` and the rwb-access authorise contract; their JSON element names are Not specified in the source documents (GAP-0671; GAP-0957) until their owners publish them. The element names of section 12.1 are the realignment baseline for the access call; they are carried in RWB-P4-E1037-CON. The caller type is a carried value of the approved callers list; rwb_access holds no list of caller types. The idempotency replay window is 24 hours, the platform rule.

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3); operationId `postQueuesQueueidPlacements`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/queues/{queueId}/placements` | Places a case on a queue from a model or an agent: `PlacementRequest` with `caseId`, `reason` (1 to 1,000 characters), `modelOrAgent` and `version` (1 to 40 characters); 201 returns the assignment of the new owner, or, when every owner is at the cap, the placement result with the overflow queue ID and no assignment | Queue and allocation C, scope All for service identities | One placement per case and queue while the case is in that queue; a repeat returns 409 MSG-P2-024 and writes nothing |

Errors: 401 no valid session (message ID Not specified in the source documents (CG-ALL-4342)); 403 the identity lacks Queue and allocation C (MSG-P4-002); 404 the placement flag is off (MSG-P2-025), or the queue or the case is not found (MSG-P4-003); 409 the case is already in the queue (MSG-P2-024), the case is closed (MSG-P3-005), the case has an open deviation (MSG-P2-021), the case changed during the placement (MSG-GEN-004); 422 a field is empty (MSG-GEN-001) or outside its length (MSG-GEN-002), or the caller is not approved (MSG-P2-020); 503 the decision record write failed (MSG-P7-003).

The overflow answer is one response shape with `overflow` true, the overflow queue ID, no assignment object and the decision record reference. It is the response change the legacy additions file records; the API specification description of this path names it, and the shape and the field names of the variant are Not specified in the source documents beyond that description (GAP-0735; ASM-1310).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Queue and allocation C right and the scope of the caller's service identity before the command, through the platform guard library and cached per identity and right (DP-08) | One hop, 2 s |

RWB-P2-E2036-CON is not called at run time. It is the build-against edge of this story: the caller code and its type are resolved to a service identity by the consumer stub of the contract in build and test, and in an environment the session of the caller's service identity carries the identity. The story therefore reaches no rwb-integration operation, and the direction of this hand-over is a default reading recorded as GAP-0735 and ASM-1311.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseAllocated.v1` (EV-02) | `rwb.case.events.v1` | P3 | caseId | caseid, queueid, ownerid (absent on the overflow path), ruleid, ruleversion |
| `rwb.case.CaseTransferred.v1` (EV-04) | `rwb.case.events.v1` | P3 | caseId | caseid, fromowner, reasoncode, toowner |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | caseId | decision record reference, decision code D6, caller code and version, target queue code, business date |

All three are written to the outbox in the same transaction as the case change and relayed with the CloudEvents envelope; no personal data is carried, the reason text is the caller's phrase and holds no customer data, and the account number is in no payload (DP-09). `CaseTransferred.v1` is published only when the case had an owner before the call; a placement on a case with no owner publishes `CaseAllocated.v1` alone.

#### 12.4 Events consumed

None. The command is called; it consumes no event, holds no consumer and writes no inbox row. The open deviation is read from the case's own `deviation_open` flag, which rwb-deviation sets through `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` consumed by the case router of rwb-case, not by this story (DF-CAS-019; GAP-0735; ASM-1314).

#### 12.5 Workflows and activities

None added. The placement is a synchronous command served on the REST thread with its one transaction; no Temporal workflow instance is started, signalled or updated by it, and no activity is registered for it. CaseWorkflow, the parent workflow of the case, observes the new queue and owner through `CaseAllocated` or `CaseTransferred` on `rwb.case.events.v1` and through its own case read, exactly as it observes any other case change. The allocation activity that chooses an owner belongs to RWB-P3-E1020-APP, and this story calls `AllocationService.assignInQueue` in process, inside its own transaction, without a workflow hop.

#### 12.6 Schedules

None. A placement happens when a caller sends it; no Quartz job, no Temporal Schedule and no five-minute timer check is added, changed or read by this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| queue | P3 (rwb_case) | Read only: method, cap of 150, overflow queue, team |
| recovery_case | P3 (rwb_case) | Read: status, owner, queue, team, `deviation_open`, closed date, version; write: `queue_id`, `team_code`, `owner_user_id`, `status`, `updated_by`, `version` |
| assignment | P3 (rwb_case) | Write: the ended previous open assignment and the new assignment with reason ALLOCATION and `created_by`; read for the open-assignment check |
| task | P3 (rwb_case) | Read only: the `task_id IS NULL` term of the open-assignment index, because a placement writes a case assignment and never a task assignment |
| outbox_event | PLT library, created in rwb_case | Write: `CaseAllocated`, `CaseTransferred`, the decision record (DP-09) |
| processed_event | PLT library, created in rwb_case | Created with the schema; this story consumes no event and writes no row |
| idempotency_key | PLT library, created in rwb_case | Write: one key per placement command, so a repeated request replays the stored answer or is refused with MSG-P2-024 |
| decision record (local) | DP-03 library, created in rwb_case | Write: decision code D6, caller code and version, reason, identity, target queue, hash-linked to the previous record |
| `uk_assignment_open_case` | P3 (rwb_case) | Unique index on `assignment (case_id) WHERE ended_at IS NULL AND task_id IS NULL`, added by the migration of section 13 |

rwb-case reads no table of another service and holds no foreign key across services (DP-01). `permission` and `permission_matrix` are rwb-access tables, `decision_log_entry` is a rwb-decision table, and `interface_catalogue` is an rwb-integration table; all three are reached only through their contracts or their topics.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Consumer stub of RWB-P2-E2036-CON | The caller-identity edge of the rwb-integration contract | "MDL-SYN-PRIORITY" of type MODEL for service identity SY-AGENT; "MDL-SYN-UNLISTED" with no entry; an AGENT caller for the same identity |
| rwb-access WireMock | The P4 authorise contract | `POST /authorise` granting Queue and allocation C under matrix version "PM-SIT-02"; refusing it with R only, which is the production matrix answer today (GAP-0735; ASM-1309); a cached answer and an answer beyond 2 s |
| Outbox relay fake | The DP-09 outbox and the `rwb.case.events.v1` and `rwb.decision-record.v1` topics | Captures `CaseAllocated`, `CaseTransferred` and the decision record of a committed transaction and proves that nothing is relayed when the transaction rolls back |
| Decision-record fake | The local decision-record library of DP-03 | A successful write with a reference; a forced failure for AC14; a record store stopped before the call |
| rwb-case parameters stub | The DP-06 parameters of rwb-case | The approved callers list with "MDL-SYN-PRIORITY" and without "MDL-SYN-UNLISTED"; the placement flag on and off |

The credentials of the fakes and of the deployed sandbox use the rwb-case login (DP-02); its name is Not specified in the source documents (GAP-0735; ASM-1315).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | `POST /queues/{queueId}/placements` provided on `/api/recovery/case/v1`; `POST /api/recovery/access/v1/authorise` consumed through the platform guard library, one hop, 2 s, cached |
| Kafka | 3 published, 0 consumed | `rwb.case.CaseAllocated.v1` and `rwb.case.CaseTransferred.v1` on `rwb.case.events.v1`; `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`; all through the outbox in the same transaction |
| Temporal | None | No workflow and no activity added; CaseWorkflow observes the change through the outbox |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `placement`, Java package `th.co.scb.ace.workbench.recovery.case.placement`. No front end. No screen is served here, so SCR-02, SCR-07 and SCR-38 gain no states in this story; their empty, loading, error and no-access states belong to the screen stories that serve them.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies this table adds are held by the platform and service contract stories and are not repeated in the metadata rows, which carry only the contract dependency of the legacy interface: RWB-P2-E2036-CON (GAP-0735; ASM-1313). DP-19 resolves to no work here: this story serves no screen, and the placed case appears in the existing queue and case list screens of the epic. DP-15 resolves to one migration in `rwb_case`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PlacementController | Controller | Implements `postQueuesQueueidPlacements`: the flag check, the field validation, the caller check, the error mapping of section 12.1 |
| PlacementService | Service | BR1 and BR3 to BR14: the queue and case reads, the refusals, the case change, the assignment call, the outbox rows and the decision record in one transaction |
| ApprovedCallerList | Service | Reads the approved callers list from the parameters of rwb-case through the parameters contract (DP-06, key `rwb.casewf.placement.approved-callers`) and answers whether a caller code is approved for a service identity; holds no list in code |
| CallerIdentityResolver | Client adapter | Resolves the caller code and its type to a service identity from the consumer stub of RWB-P2-E2036-CON; no run-time call to rwb-integration |
| AccessGuard | Library adapter | Calls `POST /api/recovery/access/v1/authorise` with the platform guard library, one hop, 2 s, cached, and answers Queue and allocation C (DP-08) |
| AllocationService.assignInQueue | Published interface (RWB-P3-E1020-APP) | Chooses the owner by the queue's method within the cap of 150, or answers the overflow queue and no owner |
| PlacementRepository | Repository | Reads and writes `recovery_case` and `assignment` in schema `rwb_case` with the optimistic lock version, and reads `queue` |
| DecisionRecordWriter | Library adapter | Writes the local decision record with decision code D6 and the caller content, hash-linked, in the caller's transaction (DP-03) |
| OutboxWriter | Library adapter | Writes `CaseAllocated`, `CaseTransferred` and the decision record into `outbox_event` in the same transaction (DP-09) |

**Database and migrations**

- One migration, `V2036_1__placement_index.sql`, in the rwb-case Flyway sequence (DP-15): `CREATE UNIQUE INDEX uk_assignment_open_case ON assignment (case_id) WHERE ended_at IS NULL AND task_id IS NULL`, so a case has one open case assignment whatever two callers do at the same moment.
- No new table. The queue, the case, the assignment, the task and the parameter and reference tables already exist in `rwb_case`; the outbox, inbox, idempotency and decision-record objects come from their platform libraries.
- Reads use `ix_case_owner_status` of RWB-P3-E1020-APP for the owner load and the primary key of `queue` and `recovery_case`; no scan is added by this story.
- The migration touches no other schema, and the service reads no table outside `rwb_case` (DP-01).

**Configuration and reference data**

- Approved callers list `rwb.casewf.placement.approved-callers` (empty at go-live, assumed; loaded by RW-REFADM after RW-RISK approval): caller code, type MODEL or AGENT, service identity (GAP-0735; ASM-1308).
- Placement flag `rwb.casewf.queue-placement`, default off; on in the DEV and SIT test runs only (GAP-0735; ASM-1312).
- Queues, methods, caps and overflow queues from RWB-P3-E1019-APP and RWB-P3-E1020-APP: queue "MTG-BKK-PRI" with ROUND_ROBIN, cap 150 and overflow queue "MTG-BKK-OVF" (DL23).
- Permission matrix version (RW-SECADM): "PM-SIT-02" in the tests, since the production matrix gives SY-AGENT R only today (GAP-0735; ASM-1309).
- LOV-DECISION value D6 (RW-COE), read through the reference-data contract (DP-07).
- Open decisions, both still open: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL23 (assumptions ASM-1232, ASM-1237, ASM-1259, ASM-1560).

**Build steps**

1. Regenerate the server interface for `postQueuesQueueidPlacements`, including the overflow variant of the 201 answer, from the OpenAPI document of RWB-P2-E2036-CON and the API specification description of the path.
2. ApprovedCallerList over the parameters of rwb-case, and the controller validation and flag check; tests for AC4, AC5 and AC6.
3. CallerIdentityResolver against the consumer stub of RWB-P2-E2036-CON, and AccessGuard against the rwb-access fake with matrix version "PM-SIT-02"; tests for AC1 and AC13.
4. PlacementService with the queue and case reads, the refusals, the case change, the outbox rows and the decision record in one transaction; tests for AC3, AC7, AC8, AC9, AC10 and AC12.
5. `AllocationService.assignInQueue` reused for a given queue, with the cap and the overflow; tests for AC1 and AC2.
6. The unique open-assignment index and the optimistic lock; the concurrent test for AC11.
7. The forced decision-record failure and the rollback assertion; test for AC14.
8. The outbox relay contract test, proving that `CaseAllocated`, `CaseTransferred` and the record are relayed after the commit and nothing is relayed after a rollback.
9. A run of the whole suite with the flag off in UAT and production settings, and on in SIT, so the release keeps the interface dark outside the test environments.

**Feature flag.** `rwb.casewf.queue-placement`, default off. Off returns 404 with MSG-P2-025 and touches nothing: the case is not read, no assignment is written and no decision record is made. On in the DEV and SIT test runs only.

**Done when.** The tests in section 16 pass with the flag on in SIT; the flag is off in UAT and production at the release; every placement of the suite writes exactly one assignment, one decision record and its outbox rows; and no caller outside the approved callers list obtains a placement.

### 14. Validation and messages

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
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Thai text for each message follows decision DL10. For MSG-GEN-001 and MSG-GEN-002 the {field} value is the request field name only ("caseId", "reason", "modelOrAgent" or "version"), never a case fact. For MSG-P2-020 the {caller} value is the caller code of the request. For MSG-P2-024 the {queue} value is the queue code. For MSG-P4-002 the {action} value is "place a case on a queue". Error responses use the RFC 9457 problem-details envelope published in the contract of the service.

### 15. Screens and states

No screen in this story and no front-end change. A placed case appears in its queue on SCR-07 Team queues and SCR-02 Case list like any other case, in their existing states (empty, loading, error and no access; error and no access are Not specified in the source documents (CG-ALL-4351); for SCR-07 empty, error and no access are Not specified in the source documents (CG-ALL-4352)), and the decision record query SCR-38 shows the placement entry with the caller code, its type and its version. For SCR-38 the empty, error and no access states are Not specified in the source documents (CG-ALL-4353). Those screens are served through the gateway-bff composite route from the rwb-case read operations (DP-19) and belong to the queue and case list stories of the epic (RWB-P3-E1023-APP and the queue stories). A case placed in the overflow queue is shown in the overflow queue, and a case refused in AC7, AC8 or AC9 is shown where it already was; no new state is introduced by this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-036-13 | AC13, BR2 | Component | SY-AGENT under the production matrix (Queue and allocation R); refused with MSG-P4-002 |
| TC-E2-036-14 | AC14, BR6 | NFR | Decision record write forced to fail; 503 MSG-P7-003; case, assignment and outbox unchanged |
| TC-E2-036-01 | AC1, BR1, BR2, BR9 | Component | Approved caller MDL-SYN-PRIORITY under SY-AGENT; NEW case |
| TC-E2-036-02 | AC2, BR3 | Component | Owners at 150 and 149; then both at 150 |
| TC-E2-036-03 | AC3, BR5 | Component | One placement; decision record fields checked |
| TC-E2-036-04 | AC4, BR8 | Component | Flag off |
| TC-E2-036-05 | AC5, BR1 | Component | Caller MDL-SYN-UNLISTED |
| TC-E2-036-06 | AC6 | Component | Request with no reason |
| TC-E2-036-07 | AC7, BR7 | Component | Same request sent twice |
| TC-E2-036-08 | AC8, BR7 | Component | CLOSED case |
| TC-E2-036-09 | AC9, BR4, BR10 | Component | Case with X2 open |
| TC-E2-036-10 | AC10 | Component | Queue ID that does not exist; then a case ID that does not exist |
| TC-E2-036-11 | AC11, BR11 | Component | Two placements against one case version |
| TC-E2-036-12 | AC12, BR3, BR12 | Component | IN_PROGRESS case with owner U-5100 |
| TC-E2-036-15 | Section 12.1 to 12.3, BR9, BR12 | Contract | Each operation, event and activity of section 12 against the RWB-P2-E2036-CON contract |
| TC-E2-036-16 | Section 12.7, BR14 | Component | Each table of section 12.7 at its row limits; no write outside `rwb_case` |
| TC-E2-036-17 | AC15, BR13 | Component | Placement reads decision code D6 of LOV-DECISION through the reference-data contract |
| TC-E2-036-18 | AC15, BR14 | Component | Placement reads no table outside `rwb_case`; the right and the identity come from the contracts |
| TC-E2-036-19 | AC16 | Component | Placement sent without a valid service identity; 401 |

The legacy levels map System to Component, Access to Component and Resilience or Principle 5 to NFR, because the cross-service behaviour of this key is proved by the integration story. The `-ITG` copy of each case is held by RWB-ITG-E2036-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the approved callers, the flag, the caps, the methods, the overflow queues, the length limits and the decision code D6 are rows, parameters or reference data.
- No personal data in logs, tests, workflow history or prompts: logs hold case IDs, queue codes and caller codes, never account numbers, names or identity numbers; the reason text is the caller's code or phrase and holds no customer data.
- No read of another service's tables: the right comes from the rwb-access contract, the caller identity from the rwb-integration contract, the decision ledger from its topic; `rwb_case` holds no foreign key into another schema (DP-01, DP-08).
- The decision record is written inside the caller's transaction, last, with propagation MANDATORY; a failed write rolls the placement back and returns 503 (R-UNI-39).
- A caller never bypasses the access check or the allocation engine: the right is checked before the case is read, and the owner is chosen only by `AllocationService.assignInQueue`.
- A refused placement writes nothing: no assignment, no case change, no outbox row and no decision record.
- The command starts no workflow and reads no clock of its own; the case events are the only hand-over to CaseWorkflow.
- Every outbound event is written to the outbox in the same transaction as the case change and carries IDs and facts only (DP-09).
- The unique open-assignment index is a data guarantee and is never replaced by an application-only check.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-017 | A queue accepts a write from a model or an agent with the case and the reason | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-DEV-01 | TC-E2-036-01, TC-E2-036-03, TC-E2-036-04 |
| REQ-CWC-018 | A model or agent passes the same permission checks and its write is logged with its version | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-UNI-39 | TC-E2-036-01, TC-E2-036-02, TC-E2-036-03, TC-E2-036-13 |
| REQ-CWC-019 | The interface ships behind a feature flag | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-01, TC-E2-036-02, TC-E2-036-03 |
| REQ-CWC-020 | Model and rule work in the same queue, in one priority order | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-01, TC-E2-036-02, TC-E2-036-03 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | CTL-09 | TC-E2-036-01, TC-E2-036-13 |

Legacy trace: story RWB-E2-036 "Queue write interface for models and agents", module P2 Integration in the legacy backlog, feature FEAT-CWC-29, requirements REQ-CWC-017 to REQ-CWC-020 and REQ-ACA-010, rules R-DEV-01, R-UNI-39 and CTL-09. The legacy AC1 to AC12 are covered by the sixteen new criteria of this slice and by RWB-ITG-E2036-ITG, and no slice of this key was allocated the legacy criteria (GAP-0735; ASM-1307). The approved callers list is the parameter rwb.casewf.placement.approved-callers, the production matrix grant is a matrix version change by RW-SECADM, the overflow response shape and the caller-code mapping are in RWB-P2-E2036-CON, and the legacy criteria are in RWB-ITG-E2036-ITG (GAP-0735).

### 19. Out of scope

- Score and priority on the placement and queue order by priority (REQ-CWC-020): added with the first approved model consumer, in the epic that switches the flag on.
- The model or agent that calls the interface and its runtime (the P10 agent stories, for example RWB-E2-028).
- The caller-identity catalogue, its read operation and the outside interfaces it serves (RWB-P2-E2036-CON and its app story in rwb-integration).
- Granting SY-AGENT Queue and allocation C in the production matrix: a permission matrix change under RWB-E1-037, by RW-SECADM.
- The owner choice, the caseload cap, the round-robin cursor and the overflow behaviour themselves (RWB-P3-E1020-APP); this story reuses them.
- The transfer rules and the manual transfer screens (RWB-P3-E1021-APP).
- The queue and team data and their administration screens (RWB-P3-E1019-APP, SCR-07).
- The full read-only case record view and the deviation flag display (RWB-P3-E1023-APP, RWB-P3-E2015-APP).
- The contract documents themselves (RWB-P2-E2036-CON and the case contract story of this epic).
- The deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook.
