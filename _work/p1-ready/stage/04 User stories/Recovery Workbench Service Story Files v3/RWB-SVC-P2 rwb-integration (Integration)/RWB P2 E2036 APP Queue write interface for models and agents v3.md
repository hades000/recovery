# RWB-P2-E2036-APP Queue write interface for models and agents

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- D-RCV-60 finishing pass: updated the section 16 reference to Recovery Workbench Test Cases v9.

- The decision event type reads `rwb.decision.DecisionRecorded.v1`; the topic `rwb.decision-record.v1` is unchanged (RD-P1-008).

| Item | Value |
|---|---|
| Story key | RWB-P2-E2036-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-036 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P2-K |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P2-E2036-APP-16); the squad sets size at refinement |
| Depends on (build) | RWB-P2-E2036-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P3-E1019-CON, RWB-P3-E1020-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020, REQ-ACA-010) |
| Readiness decisions | RD-P1-008 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-036 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E2036-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 17 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **an integration adapter through which an approved model or agent places a case on a queue under its own service identity, with the feature flag checked first, the caller checked against the approved callers list, the four request fields validated, the request replayed from the adapter's own idempotency table and the placement forwarded to rwb-case as one hop**, so that **analytical output reaches a person the next working day instead of through a weekly manual file, while the queue's own allocation method, caseload cap and access rules keep deciding the owner**.

The legacy story held the whole journey in one P2 Integration service: the endpoint, the queue and case tables, the allocation engine, the assignment, the decision log entry and the two events. Under D-RCV-60 the journey crosses three services. **rwb-integration** owns the model and agent queue-write adapter: the caller-facing operation, the feature flag, the caller admission check, the field validation, the admission decision record, the idempotent replay and the forwarding. **rwb-case** owns the queue, the allocation engine, the caseload cap, the overflow queue, the assignment, the placement decision entry and the CaseAllocated and CaseTransferred events (Arch v5 slide 41: rwb-case owns case, CMMN state, queues, tasks, allocation, timers). **rwb-access** owns the role, scope and right answer that the caller's service identity passes (Arch v5 slide 14: rwb-access IN `POST /authorise`).

The Ownership Map keeps `POST /queues/{queueId}/placements` with P3 rwb-case, and this realignment also gives the legacy key a P2 story. The two are reconciled rather than duplicated: rwb-case serves and keeps `POST /api/recovery/case/v1/queues/{queueId}/placements`, which is the placement contract this adapter calls; rwb-integration serves the caller-facing admission and forwarding operation `POST /api/recovery/integration/v1/queues/{queueId}/placements`, which is a different operation on a different base, owned by rwb-integration and named in RWB-P2-E2036-CON. The adapter writes no `recovery_case`, no `assignment` and no `queue` row and publishes neither CaseAllocated nor CaseTransferred, because those belong to the case owner (DP-01). The reconciliation and its evidence are recorded as GAP-0670.

The adapter is a decoupling device, not a second business rule engine. It applies four checks only: the feature flag, the caller admission, the field validation and the idempotent replay. Every business rule of the placement (the queue's method, the cap, the overflow queue, the closed case, the open deviation, the one-open-assignment constraint, the decision entry and the events) stays with the placement contract and the case, exactly as the legacy story had them, and is proved in RWB-P3-E2036-APP. The local decision record (DP-03) is written before the forward, so a caller that is admitted and then refused still leaves the record of its admission and of the answer.

### 2. Business rationale

Model scores and agent findings reach the queues today through a weekly file that a person loads by hand, so a case flagged on Monday is worked the following week (legacy RWB-E2-036). The interface lets an approved caller place a case on a queue the day the decision is made, while the queue's allocation method, caseload cap and the role to permission matrix apply as they do to any case, and every placement is written to the decision record with the caller and its version. It meets REQ-CWC-017, REQ-CWC-018 and REQ-CWC-019; the business measure is the time from a model decision to the case reaching a queue, from up to 7 days today to the same day.

The target adds a second reason. The Workbench is no longer one deployable with one schema: nineteen services each own their tables and publish their contracts, and no service reads another service's tables (Arch v5 slides 20 and 41; DP-01). A model job or an agent is a non-engine caller with a service identity, and it must not be handed a path into the case schema. It calls one stable, versioned operation, on a base of its own (`/api/recovery/integration/v1`, DP-13), with an `Idempotency-Key` (Arch v5 slide 11) and a recorded answer, and the service that owns the case decides the placement. That is what makes the interface safe to switch on for an outside caller: the caller cannot reach the queue, the case or the assignment, only the adapter.

The adapter also carries the audit half of the legacy BR5. The legacy wrote one decision log entry with the caller, the reason and the model or agent version. In the target two records exist and both are needed: rwb-case writes the placement entry with final call "PLACED {queue}" in the same transaction as the case change, the assignment and the outbox rows (proved in RWB-P3-E2036-APP), and rwb-integration writes its own admission record through the local decision-record library of DP-03, with the caller identity, the caller type, the reason, the model or agent version, the target queue and the answer it returned. A decision that cannot be recorded does not proceed (R-UNI-39; Principle 5).

It applies REQ-ACA-010 as well: a model or agent passes the same role, scope and right checks as a person, through the rwb-access authorise contract and its guard library, with no bypass for a non-engine caller (CTL-09; NFR-051).

### 3. Preconditions

- RWB-P2-E2036-CON is published: the contract of this adapter, with the placement operation on the integration base, the three consumed contracts, the idempotent replay and the fakes. It is a same-service contract story and is therefore a build dependency.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). The library writes the record and publishes `rwb.decision.DecisionRecorded.v1` (EV-08) on the service's behalf.
- RWB-PLT-E1043-CON is published: the reference-data client library that reads a row by key with the version in force (DP-07), used for the approved callers list.
- RWB-PLT-E1037-CON is published: the rwb-access guard library that performs the authorise call and caches the answer per session and per workload identity (DP-08).
- RWB-PLT-TE006-CON is published: the idempotency, outbox and inbox library, with the stored-response table and the 24-hour retention rule (DP-09).
- RWB-PLT-E1047-CON is published: the naming library that fixes the base, the topic and the event names (DP-14), and RWB-PLT-E1044-CON the per-service Flyway sequence and migration conventions of `rwb_integration` (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff route that lets an approved caller reach the integration base, and that serves the reading screens the placed case appears on (DP-19).
- The `rwb_integration` library tables `idempotency_key` and `decision_record` exist from the rwb-integration baseline, created by the DB story of this epic on the per-service Flyway sequence.
- The caller is listed in the approved callers list (legacy configuration key `rwb.casewf.placement.approved-callers`) with its caller code, its type MODEL or AGENT and its service identity. The list is empty at go-live (assumed in the legacy story); RW-COE requests an entry and RW-RISK approves it.
- The caller code and its type are recorded in the access entry and are not resolved as a role; the caller code narrows no right. The caller is resolved through the role of its service identity at the matrix version in force, and the role class rule for a service identity is Not specified in the source documents (GAP-0960). This service holds no copy of the approved callers list.
- The permission matrix in force gives the caller's service identity Queue and allocation C through the rwb-access authorise contract. The matrix today gives SY-AGENT R only, so a matrix version change by RW-SECADM is needed before the first caller is switched on.
- The target queue exists with its assignment method, caseload cap and overflow queue (DL23; caseload cap 150, assumed), and the case exists with a status and no open deviation. Both facts are read by rwb-case, never by this service.
- Feature flag `rwb.casewf.queue-placement` is off in every environment except DEV and SIT test runs. The flag value is read from the platform flag library (Template and Rules §R3 default ruling); off returns 404 with MSG-P2-025 and touches nothing.
- The service runs as its own login on the ACE database (DP-02). The login name is Not specified in the source documents (GAP-0670; ASM-1190).

### 4. Flow

1. Caller (model job or agent, under its service identity): sends `POST /api/recovery/integration/v1/queues/{queueId}/placements` with `caseId`, `reason`, `modelOrAgent` and `version`, an `Idempotency-Key` and its workload token.
2. gateway-bff: routes the call to rwb-integration on the integration base; it composes nothing for this path, because the caller is not a screen (DP-19).
3. PlacementAdapterController: resolves the caller identity from the workload token and reads the feature flag `rwb.casewf.queue-placement` from the platform flag library. Off returns 404 with MSG-P2-025 and touches nothing.
4. PlacementAdapterController: checks for a stored answer with the same `Idempotency-Key` for this endpoint in `idempotency_key`; a hit within 24 hours returns the stored status and body unchanged, and no second forward is made.
5. AccessCheckClient: checks Queue and allocation right C for the caller's service identity through the rwb-access authorise contract, cached per workload identity with the matrix version that answered (DP-08). The admitting role's scope must be ALL; any other scope is refused with SCOPE_NOT_ALL, and the queue's team code is recorded in the access entry and compared with nothing (GAP-0959).
6. PlacementAdapterController: validates the four fields (presence, type, `reason` 1 to 1,000 characters, `version` 1 to 40 characters) and returns 422 naming the field and the rule, with MSG-GEN-001 or MSG-GEN-002.
7. ApprovedCallerCatalog: reads the approved callers list from the rwb-case reference-data contract under the key `rwb.casewf.placement.approved-callers`, with the version in force (DP-07), and checks that `modelOrAgent` is listed for this caller's service identity with its type. An unlisted caller returns 422 with MSG-P2-020.
8. PlacementAdmissionService: derives the request hash from the method, the path and the canonical body and writes the admission record through the local decision-record library (DP-03): decision code D6, the caller identity and type, the caller code, the version, the reason, the target queue and the outcome that will be recorded.
9. CasePlacementClient: forwards the placement to the rwb-case contract `POST /api/recovery/case/v1/queues/{queueId}/placements` with the same body plus the caller service identity, in one hop with a 2 s timeout and a circuit breaker (DP-11).
10. rwb-case: applies the queue, the allocation method, the cap, the overflow queue, the access rule of the case and the case state; this front end writes nothing of that (proved in RWB-P3-E2036-APP).
11. PlacementAdmissionService: records the answer in the admission record and stores the status and the response body against the `Idempotency-Key` in `idempotency_key` for 24 hours, so a repeat replays it.
12. PlacementAdapterController: returns the rwb-case answer unchanged: 201 with the placement result, or 403, 404, 409, 422 or 503 with the rwb-case problem. This adapter adds no message of its own to a forwarded refusal.
13. Repeat of the same request with the same `Idempotency-Key` inside 24 hours: the stored answer is returned with no second admission record, no second forward and no second effect.
14. A request refused by the adapter's own checks (flag, right, fields, approved callers, local record) is stored too, so the caller's retry replays the refusal instead of producing a second decision record.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Feature flag off | 404; nothing changes, nothing is recorded | MSG-P2-025 | AC4 |
| X2 | Caller is not in the approved callers list for its service identity | 422; nothing is forwarded | MSG-P2-020 | AC5 |
| X3 | `caseId`, `reason`, `modelOrAgent` or `version` empty | 422 naming the field; nothing is forwarded | MSG-GEN-001 | AC6 |
| X4 | `reason` or `version` outside its length range | 422 naming the field and the range | MSG-GEN-002 | AC6 |
| X5 | The case is already in the target queue, including a repeated call without an `Idempotency-Key` | 409 from rwb-case, returned unchanged; no second entry, no second assignment | MSG-P2-024 | AC7 |
| X6 | The case is closed | 409 from rwb-case, returned unchanged | MSG-P3-005 | AC8 |
| X7 | The case has an open deviation | 409 from rwb-case; the case stays with the deviation handler | MSG-P2-021 | AC9 |
| X8 | The queue or the case does not exist | 404 from rwb-case or from the authorise call, returned unchanged | MSG-P4-003 | AC10 |
| X9 | Every owner in the queue is at the caseload cap | 201 with the overflow queue and no owner; this adapter returns the answer unchanged | None | AC2 |
| X10 | Two placements of the same case commit at the same time | One commits with 201; the other gets 409, returned unchanged | MSG-GEN-004 | AC11 |
| X11 | The caller's identity lacks Queue and allocation C | 403 before any forward; nothing is recorded as placed | MSG-P4-002 | AC13, TC-E2-036-13 |
| X12 | The admission record cannot be written | 503; nothing is forwarded and nothing changes; an incident is raised (R-UNI-39) | MSG-P7-003 | AC14, TC-E2-036-14 |
| X13 | rwb-case, rwb-access or the rwb-case reference-data contract does not answer inside the REST budget | One hop, 2 s timeout and breaker; 503 and nothing forwarded | MSG-GEN-006 | AC1 |
| X14 | The same request arrives twice with the same `Idempotency-Key` inside 24 hours | The stored answer is replayed; no second admission record, no second forward | None | AC1 |
| X15 | The same request arrives with the same `Idempotency-Key` after 24 hours | Treated as a new request; rwb-case's own one-open-assignment rule decides, and a repeat inside the queue is refused with 409 | MSG-P2-024 | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published contracts: its own contract story, the decision-record library, the reference-data and authorise libraries, the idempotency library, the naming rule, the migrations and the edge route. The rwb-case and rwb-access answers come from their contract fakes, so no case service is needed to build or test this service |
| Negotiable | Which callers are approved is configuration; the caps, methods and overflow queues are queue data of rwb-case; the adapter fixes only the flag, the admission, the validation, the replay and the forward |
| Valuable | A daily model or agent decision reaches a person the same day without giving a non-engine caller a path into the case schema |
| Estimable | One endpoint, one admission service, three consumed contracts, two library tables, one flag and one fake pack |
| Small | Fits one sprint with its tests |
| Testable | Each owned criterion has one test with a synthetic caller; every cross-service answer is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Queue write interface for models and agents

  Background:
    Given feature flag "rwb.casewf.queue-placement" is on
    Given the permission matrix version "PM-SIT-02" gives service identity SY-AGENT Queue and allocation C
    Given the approved callers list holds caller "MDL-SYN-PRIORITY" of type MODEL for service identity SY-AGENT
    Given queue "MTG-BKK-PRI" of team "MTG-BKK" uses method ROUND_ROBIN with caseload cap 150 and overflow queue "MTG-BKK-OVF"
    Given case "RW-2026-000501" has status NEW, no owner, no open deviation
    Given the rwb-case placement mock and the rwb-access authorise mock are in force

  Scenario: AC1 A non-engine writer can place a case (legacy RWB-E2-036 AC1)
    Given the rwb-case contract mock returns 201 with case "RW-2026-000501" placed in queue "MTG-BKK-PRI", owner "U-5002" and identity SY-AGENT
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then the response is 201
    Then the case is in queue "MTG-BKK-PRI"
    Then the assignment and the case record show SY-AGENT as the identity that made the change

  Scenario: AC2 The same rules still apply (legacy RWB-E2-036 AC2)
    Given queue "MTG-BKK-PRI" holds owners "U-5001" with 150 open cases and "U-5002" with 149 open cases
    Given the rwb-case contract mock returns owner "U-5002" for case "RW-2026-000501" by round robin, and case "RW-2026-000502" placed in queue "MTG-BKK-OVF" with no owner
    When the model places case "RW-2026-000501" on it
    Then the system gives the case to "U-5002" by round robin, skipping "U-5001" at the cap
    Then the case status becomes ASSIGNED
    Then when both owners hold 150 open cases and the model places case "RW-2026-000502", that case is in queue "MTG-BKK-OVF" with no owner and status NEW

  Scenario: AC3 Every placement is logged (legacy RWB-E2-036 AC3)
    Given the rwb-case contract mock returns 201 with the placement decision entry of decision code D6 committed in the same transaction
    When the model places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then one decision log entry exists with decision code D6, model version "MDL-SYN-PRIORITY 1.4.0", the reason "High cure score", the caller identity SY-AGENT and final call "PLACED MTG-BKK-PRI"
    Then the entry, the case change, the assignment and the events commit in one transaction

  Scenario: AC4 It is off until a consumer exists (legacy RWB-E2-036 AC4)
    Given feature flag "rwb.casewf.queue-placement" is off
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the response is 404 with message MSG-P2-025
    Then the case and the decision log are unchanged

  Scenario: AC5 A caller that is not approved is refused (legacy RWB-E2-036 AC5)
    When SY-AGENT places a case with modelOrAgent "MDL-SYN-UNLISTED"
    Then the response is 422 with message MSG-P2-020
    Then nothing changes

  Scenario: AC6 A required field is empty (legacy RWB-E2-036 AC6)
    When SY-AGENT places case "RW-2026-000501" with no reason
    Then the response is 422 with message MSG-GEN-001 for field reason
    Then nothing changes

  Scenario: AC7 A case already in the queue (legacy RWB-E2-036 AC7)
    Given case "RW-2026-000501" was placed on queue "MTG-BKK-PRI" at 08:10
    Given the rwb-case contract mock returns 409 with message MSG-P2-024 for the second request
    When the same request is sent again at 08:11
    Then the response is 409 with message MSG-P2-024
    Then there is still one assignment and one decision log entry for the placement

  Scenario: AC8 A closed case is refused (legacy RWB-E2-036 AC8)
    Given case "RW-2026-000503" has status CLOSED
    Given the rwb-case contract mock returns 409 with message MSG-P3-005
    When the model places it on queue "MTG-BKK-PRI"
    Then the response is 409 with message MSG-P3-005
    Then nothing changes

  Scenario: AC9 A case with an open deviation stays with its handler (legacy RWB-E2-036 AC9)
    Given case "RW-2026-000504" has deviation X2 open and is in the deviation handler's queue
    Given the rwb-case contract mock returns 409 with message MSG-P2-021
    When the model places it on queue "MTG-BKK-PRI"
    Then the response is 409 with message MSG-P2-021
    Then the case stays in the deviation handler's queue

  Scenario: AC10 An unknown queue or case (legacy RWB-E2-036 AC10)
    Given the rwb-case contract mock returns 404 with message MSG-P4-003 for a queue ID that does not exist
    When the model places case "RW-2026-000501" on a queue ID that does not exist
    Then the response is 404 with message MSG-P4-003

  Scenario: AC11 Two placements at the same time (legacy RWB-E2-036 AC11)
    Given the rwb-case contract mock answers the first placement with 201 and the second with 409 and message MSG-GEN-004
    When two placements of case "RW-2026-000501" to queues "MTG-BKK-PRI" and "MTG-BKK-CO" commit at the same time
    Then one succeeds with 201
    Then the system refuses the other with 409 and message MSG-GEN-004
    Then the case is in exactly one queue with one open assignment

  Scenario: AC12 A case that already has an owner (legacy RWB-E2-036 AC12)
    Given case "RW-2026-000505" has status IN_PROGRESS, owner "U-5100" and queue "MTG-BKK-CO"
    Given the rwb-case contract mock returns 201 with the assignment of "U-5100" ended, a new owner, status IN_PROGRESS and the two outbox rows
    When the model places it on queue "MTG-BKK-PRI"
    Then the assignment of "U-5100" ends and a new owner is chosen by the queue's method
    Then the case status stays IN_PROGRESS
    Then events CaseAllocated and CaseTransferred are written to the outbox

  Scenario: AC13 The caller's identity lacks Queue and allocation C (exception X11) (new, D-RCV-60)
    Given the rwb-access authorise mock returns identity SY-AGENT without Queue and allocation C
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then the response is 403 with message MSG-P4-002
    Then nothing is forwarded to rwb-case
    Then nothing is recorded as placed

  Scenario: AC14 The admission record cannot be written (exception X12) (new, D-RCV-60)
    Given the decision record write is forced to fail
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then the response is 503 with message MSG-P7-003
    Then nothing is forwarded to rwb-case
    Then the case, the assignment and the outbox are unchanged
    Then an incident is raised under R-UNI-39

  Scenario: AC15 A repeat is replayed with no second effect, and the boundary rules hold (BR9, BR10, BR11; BR6 is proved by AC14) (new, D-RCV-60)
    Given SY-AGENT placed case "RW-2026-000501" on queue "MTG-BKK-PRI" at 08:10 and the stored answer is kept under its Idempotency-Key
    When the same request with the same Idempotency-Key is sent at 08:11
    Then the stored answer is replayed with no second admission record and no second forward to rwb-case
    Then rwb-integration writes no recovery_case, assignment or queue row and publishes neither CaseAllocated nor CaseTransferred
    Then each cross-service call is one hop with a 2 s timeout and a circuit breaker

  Scenario: AC16 A request without valid credentials is refused with 401, and an identity without the access check is refused with 403 (new, D-RCV-60)
    Given the request carries no valid credentials
    When SY-AGENT places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then the response is 401 with message Not specified in the source documents (NEWAC-RWB-P2-E2036-APP-AC16)
    Then nothing is forwarded to rwb-case
    Then the same request under an identity without Queue and allocation C is refused with 403 and message MSG-P4-002, as in AC13
    Then nothing is forwarded to rwb-case
```

AC1 to AC12 are the twelve criteria of the legacy story, copied with every value unchanged; the only additions are the mock Givens that stand in for the rwb-case contract. The queue, the allocation method and cap, the overflow queue, the assignment, the placement decision entry with final call "PLACED MTG-BKK-PRI", the case status and the CaseAllocated and CaseTransferred outbox rows are written by rwb-case and are proved in RWB-P3-E2036-APP; here the rwb-case mock returns those outcomes, and this story proves the adapter's own part: the flag check, the caller admission, the field validation, the identity that is forwarded, the idempotent replay, the admission record and the forward. AC2, AC7, AC8, AC9, AC10, AC11 and AC12 are therefore mostly cross-service outcomes: this story proves that the adapter returns the rwb-case answer unchanged and adds no effect of its own, and the P3 story proves the outcome itself.

AC13 and AC14 are added by this story for exceptions X11 and X12, which were covered only by test cases; they are the adapter's own checks. AC15 is added for BR9, BR10 and BR11, and AC16 for the 401 and 403 answers.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a caller in the approved callers list, under the service identity listed for it, may place a case, and the adapter checks the list before it forwards anything | REQ-CWC-019; legacy BR1; configuration key `rwb.casewf.placement.approved-callers` |
| BR2 | The caller passes the same access check as a person: Queue and allocation C in the permission matrix in force, through the rwb-access authorise contract | REQ-CWC-018; REQ-ACA-010; CTL-09; legacy BR2; DP-08 |
| BR3 | The owner is chosen by the queue's assignment method within its caseload cap, and when every owner is at the cap the case goes to the overflow queue; the adapter never chooses an owner | queue.assignment_method, capacity_cap, overflow_queue_id; DL23; legacy BR3; Arch v5 slide 41 |
| BR4 | A case with an open deviation stays with the deviation handler | R-DEV-01; legacy BR4 |
| BR5 | Every admitted placement writes one local admission record in the same transaction as its stored answer, with the caller identity, the caller type, the reason and the model or agent version, and rwb-case writes the placement decision entry | NFR-078; Principle 5; CTL-06; legacy BR5; DP-03 |
| BR6 | A decision that cannot be written to the decision record does not proceed: nothing is forwarded and nothing changes | R-UNI-39; Principle 5; legacy BR6 |
| BR7 | A case closed or already in the target queue is not placed; the adapter returns the refusal it receives and writes nothing of its own for the placement | LOV-CASE-STATUS; MSG-P3-005; MSG-P2-024; legacy BR7 |
| BR8 | The interface is off by feature flag until the first caller is approved, and off returns 404 with MSG-P2-025 before anything is read or written | REQ-CWC-019; DT11; legacy BR8 |
| BR9 | The operation is idempotent: one stored answer per `Idempotency-Key` and endpoint, replayed for 24 hours, and a repeat inside the window has no second effect | Arch v5 slide 11; DP-09 |
| BR10 | rwb-integration writes no `recovery_case`, no `assignment` and no `queue` row and publishes neither CaseAllocated nor CaseTransferred; the case facts are read only through the rwb-case contract | Arch v5 slide 41; DP-01; ownership map (`recovery_case`, `assignment`, `queue` are P3) |
| BR11 | Every cross-service call is one hop with a 2 s timeout and a circuit breaker; no call chain and no service reads another service's tables | DP-11; ADR-020; Arch v5 slide 11 |

### 9. State transitions

The adapter holds no case state machine. The case transitions of the placement are the case owner's (RWB-P3-E2036-APP), copied here from the legacy story for traceability only.

| From | Event | Condition | To |
|---|---|---|---|
| New | Allocation rule matched (placement) | An owner below the cap | Assigned |

The adapter's own record has four transitions, all in `rwb_integration`.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | Request received | Flag on, right present, fields valid, caller approved | Admitted |
| (none) | Request refused | Flag off, right absent, field invalid or caller not approved | Refused, stored for replay |
| Admitted | rwb-case answer recorded | Any answer from the placement contract | Answered, stored for replay |
| Answered, Refused | Same `Idempotency-Key` inside 24 hours | Any | Replayed, unchanged |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Places cases once the matrix gives it Queue and allocation C and its caller is approved |
| SY-CASEWF, the rwb-case service identity | Updates the case, writes the assignment, publishes the events (RWB-P3-E2036-APP) |
| SY-DECLOG, decision record writer | Writes the placement entry in rwb-case; the admission record is written by the rwb-integration identity through the library |
| RW-TEAMMGR, team manager | Holds Queue and allocation CRUA; reads placed cases in team queues |
| RW-COE, center of excellence analyst | Requests a caller entry in the approved callers list |
| RW-RISK, risk and model risk officer | Approves a caller entry before it is loaded |
| RW-PLATADM, platform administrator | Switches the feature flag on after approval |
| RW-SECADM, security administrator | Loads the permission matrix version that grants the caller's identity Queue and allocation C |
| No approval level from the delegation of authority applies | A placement moves work; it does not approve a treatment |

The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0670; ASM-1190).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| Not specified in the source documents (GAP-0670; ASM-1191) | placement request of the integration operation | caseId, reason, modelOrAgent, version | Read |
| DF-OPS-184 to DF-OPS-188 | idempotency_key (library table in rwb_integration) | id, idempotency_key, endpoint, request_hash, response | Write and read |
| DF-DEC-001 to DF-DEC-018 | decision_record (library table in rwb_integration; TSD P2 v3 T3.1, not an LDM v9 entity) | all fields, including decision code, final call, actions and the actor | Write |
| Not specified in the source documents (GAP-0670; ASM-1192) | approved callers row through the rwb-case reference-data contract | caller code, caller type, service identity, approval state | Read |
| Not specified in the source documents (GAP-0670; ASM-1193) | authorise answer through the rwb-access contract | permitted, matrix version, right code | Read |
| DF-CAS-001, DF-CAS-005, DF-CAS-010, DF-WRK-001, DF-WRK-006 to DF-WRK-009 | recovery_case, queue and assignment, read through the rwb-case contract only | case id, status, queue id; queue code, method, cap, overflow; the open assignment | Read through the contract; written only by rwb-case |

Field IDs are those in the Logical Data Model and Data Dictionary v9, except the library tables whose field IDs are those of TSD P2 v3 T3.1. No case, queue or assignment row is copied into `rwb_integration` (DP-01): the adapter holds the request, its stored answer and its own decision record, and nothing else. The caller's service identity is the `actor_ref` of the admission record; it is also forwarded to rwb-case, which writes it to `created_by` of the assignment and `updated_by` of the case (RWB-P3-E2036-APP).

### 12. Contract

Operation ownership (GAP-0670, GAP-0671): The owner of the placement path is Not specified in the source documents (GAP-0671); the adapter takes the four body fields caseId, reason, modelOrAgent and version with a required Idempotency-Key, and answers 201 with the placement result or returns the rwb-case status and body unchanged. The case-base operation POST /api/recovery/case/v1/queues/{queueId}/placements is owned by P3 rwb-case and is consumed here. The JSON element names of the consumed contracts (the rwb-case placement, the rwb-case reference-data contract for rwb.casewf.placement.approved-callers and the rwb-access authorise contract) are Not specified in the source documents (GAP-0671) until their owners publish them. The idempotency_key columns follow TSD P2 v3 T3.1; the decision_record columns are Not specified in the source documents (GAP-0671). The replay window is 24 hours, the platform rule. The authorise call carries the request elements caller code, caller type, service identity, target queue, queue team code, case, product group, reason, model or agent version and field IDs (GAP-0957); the caller type is a carried value of the approved callers list and rwb_access holds no list of caller types. Refusal codes RIGHT_NOT_HELD, CALLER_KIND and SCOPE_NOT_ALL answer 403 with MSG-P4-002 as the message of every 403; the 422 and 503 codes are Not specified in the source documents (GAP-0958) and keep MSG-GEN-001, MSG-GEN-002 and MSG-P7-003 as their messages; the adapter maps the code to its own refusal without restating the text.

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2). The full shape is fixed in RWB-P2-E2036-CON.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/queues/{queueId}/placements` | Accepts a placement from an approved model or agent under its service identity: flag, right, field and caller checks, admission record, forward to rwb-case and replay of the answer | Queue and allocation, right C; scope All for service identities, through the rwb-access contract | `Idempotency-Key` required; one stored answer per key and endpoint for 24 hours |

Responses: 201 with the placement result returned by rwb-case (assignment of the new owner, or the overflow queue with no owner); 401 no valid session (MSG-P4-001); 403 the identity lacks Queue and allocation C (MSG-P4-002); 404 flag off (MSG-P2-025) or queue or case not found (MSG-P4-003); 409 already in the queue (MSG-P2-024), closed (MSG-P3-005), open deviation (MSG-P2-021) or version changed (MSG-GEN-004); 422 field empty (MSG-GEN-001), length out of range (MSG-GEN-002) or caller not approved (MSG-P2-020); 503 admission record not written (MSG-P7-003) or a consumed service not answering (MSG-GEN-006). The JSON field names of the request and of the response are Not specified in the source documents (GAP-0670; ASM-1191).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/case/v1/queues/{queueId}/placements` | rwb-case (P3) | The placement itself: the queue, the allocation method, the cap, the overflow queue, the access rule, the assignment, the placement decision entry and the two events. The Ownership Map keeps this operation with P3 | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/admin/parameters` | rwb-case (P3) | The approved callers list under the key `rwb.casewf.placement.approved-callers`, read as a configured row with the version in force (DP-07) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Queue and allocation right C for the caller's service identity, with the matrix version that answered (DP-08) | One hop, 2 s (DP-11) |

The rwb-case placement contract is declared in RWB-P3-E1019-CON and RWB-P3-E1020-CON and its behaviour is built in RWB-P3-E2036-APP; this story consumes it and restates none of it as its own. The reference-data and parameter contract of rwb-case is RWB-P3-E1043-CON, and the authorise contract is RWB-P4-E1037-CON. The exact JSON field names of the three consumed contracts are Not specified in the source documents (GAP-0670; ASM-1191); the parameters key and the caller row fields are Not specified in the source documents (GAP-0670; ASM-1192).

#### 12.3 Events published

None by this service's own topic. The local decision-record library publishes `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` from the same transaction as the stored answer, with decision code D6, the caller identity and type, the model or agent version, the reason and the target queue (DP-03; H RWB-PLT-E1027-CON).

`rwb.integration.events.v1` carries FileDelivered and FileFailed (Arch v5 slides 16 and 43) and is not used by this slice. This service publishes no business event of the placement and never publishes CaseAllocated or CaseTransferred, which are rwb-case's on `rwb.case.events.v1` (DP-01, DP-14).

#### 12.4 Events consumed

None. The adapter is called synchronously by the caller; it subscribes to no topic and consumes no case event.

#### 12.5 Workflows and activities

None. The adapter is a synchronous REST admission and forward; it starts no workflow, adds no activity and holds no durable timer. The placement's own workflow signal, if any, is rwb-case's (RWB-P3-E2036-APP).

#### 12.6 Schedules

None. The adapter is caller-driven; no Temporal Schedule and no timer is created by this story.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| idempotency_key | rwb_integration | PLT library, created in rwb_integration by the rwb-integration DB story | The stored answer of an admitted or refused request, per key and endpoint, for 24 hours (DP-09) |
| decision_record | rwb_integration | PLT library, created in rwb_integration by the rwb-integration DB story | The admission record written before the forward and completed with the answer (DP-03) |

`processed_event` is not used: the adapter consumes no event, so its inbox stays empty for this slice. rwb-integration reads no table of another service and holds no foreign key across services (DP-01); the queue, the case and the approved callers list are read through their owners' contracts, never through a table.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case placement WireMock | The P3 placement contract | 201 with an owner and with the overflow queue; 409 for the queue repeat, the closed case, the open deviation and the version change; 404 for an unknown queue; 503 for the failed decision entry |
| rwb-case reference-data WireMock | The P3 reference-data and parameter contract | The approved callers list with caller MDL-SYN-PRIORITY of type MODEL for SY-AGENT, without MDL-SYN-UNLISTED, and the empty-list answer at go-live |
| rwb-access WireMock | The P4 authorise contract | Queue and allocation C granted for SY-AGENT under matrix PM-SIT-02 and refused under the production matrix |
| Decision-record library stub | The DP-03 library | A successful write, and a forced failure that makes the transaction roll back with MSG-P7-003 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | The placement on the integration base provided; the rwb-case placement, the rwb-case parameters and the rwb-access authorise consumed; one hop, 2 s timeout, breaker per downstream |
| Kafka | None published by this service, 1 published by the decision-record library | `rwb.decision-record.v1` carries DecisionRecorded on the service's behalf (DP-03); `rwb.integration.events.v1` and `rwb.case.events.v1` are not used by this slice |
| Temporal | None | No workflow, no activity and no signal |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `placement`, Java package `th.co.scb.ace.workbench.recovery.integration.placement`.

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

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PlacementAdapterController | Controller | `POST /queues/{queueId}/placements`; the flag check, the replay lookup, the validation and the problem responses |
| PlacementAdmissionService | Service | BR1, BR5, BR6 and BR9: admission, record, forward, store the answer; one transaction per request |
| ApprovedCallerCatalog | Service | Reads the approved callers list through the rwb-case reference-data contract and matches the caller code, its type and the service identity (DP-07) |
| AccessCheckClient | Client | Calls the rwb-access authorise contract through the guard library, cached per workload identity (DP-08) |
| CasePlacementClient | Client | Calls the rwb-case placement contract with the body plus the caller service identity; one hop, 2 s timeout, breaker (DP-11) |
| ParameterClient | Client | Reads the configured rows of the rwb-case contract with the version in force (DP-07) |
| IdempotencyStore | Repository | `idempotency_key` in `rwb_integration`: the stored status and body per key and endpoint, and the 24-hour retention (DP-09) |
| DecisionRecordWriter | Library client | Calls the local decision-record library with decision code D6, the caller, the reason, the version and the answer; a failure fails the transaction (DP-03) |
| FeatureFlagClient | Client | Reads `rwb.casewf.queue-placement` from the platform flag library; off returns 404 with MSG-P2-025 |

**Database and migrations**

- Writes `idempotency_key` and `decision_record` in schema `rwb_integration`, through the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0670; ASM-1190).
- No business table is added: the case, the queue and the assignment belong to rwb-case (DP-01).
- One migration in the rwb-integration sequence: `V<nnnn>__placement_adapter.sql`, where `<nnnn>` is the next free number of the service's own Flyway sequence (V0001 to Vnnnn, Service Template Specification v1 §3.1) when the migration is merged, adds the unique index on `idempotency_key (endpoint, idempotency_key)` and the index on `decision_record (occurred_at)` that the replay and the audit read use (DP-15). The table field names and the retention index are taken from TSD P2 v3 T3.1; the exact column names of `decision_record` are Not specified in the source documents (GAP-0670; ASM-1194).

**Configuration and reference data**

- The approved callers list stays in rwb-case under the legacy key `rwb.casewf.placement.approved-callers` (empty at go-live, assumed; loaded by RW-REFADM after RW-RISK approval). rwb-integration holds no copy.
- The feature flag `rwb.casewf.queue-placement` is a flag of the platform flag library (Template and Rules §R3 default ruling), default off, on in DEV and SIT test runs only.
- The decision code of the admission record is D6, as the legacy story has it, read from the decision list of the reference data in force; the code is data, not a literal in code.
- The permission matrix version is rwb-access's; the caller's service identity is the only value the adapter forwards.
- Held values (GAP-0735): the approved callers list is a parameter, empty at go-live; the matrix version that grants Queue and allocation C is loaded by RW-SECADM; the overflow 201 field list and the caller mapping are in RWB-P2-E2036-CON; the login name is in the platform DB story; the legacy criteria are in RWB-ITG-E2036-ITG.

**Build steps**

1. PlacementAdapterController with the flag check, the replay lookup and the problem responses; AC4, AC1.
2. Field validation and its two messages; AC6.
3. ApprovedCallerCatalog over the rwb-case reference-data contract, with the empty list and the unlisted caller; AC5.
4. AccessCheckClient over the rwb-access contract, with the granted and the refused right; the access test TC-E2-036-13.
5. DecisionRecordWriter before the forward, with decision code D6 and the rollback path; TC-E2-036-14.
6. CasePlacementClient over the rwb-case placement contract, with the answer returned unchanged and the timeout mapping; AC1, AC2, AC7 to AC12.
7. IdempotencyStore with the 24-hour replay, and the test that a repeat returns the first answer with no second record and no second forward; AC1.
8. The contract-fake run of every cross-service answer in isolation, so the story builds before rwb-case and rwb-access exist.
9. The architecture test that no class of this module writes `recovery_case`, `assignment` or `queue`, and that none publishes on `rwb.case.events.v1`; BR10.

**Feature switch.** The legacy flag name `rwb.casewf.queue-placement` is kept as the legacy reference for the switch and is read from the platform flag library. Off returns 404 with MSG-P2-025 and touches nothing; on in SIT only, until RW-RISK approves the first caller and RW-SECADM loads the matrix version that grants its identity Queue and allocation C.

**Done when.** The tests in section 16 pass with the flag on in SIT, the flag is off in UAT and production at the release, no row of `recovery_case`, `assignment` or `queue` is written by rwb-integration, no CaseAllocated or CaseTransferred is published by it, and a repeat of an admitted request inside 24 hours returns the first answer with no second effect.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is empty | Enter {field}. |
| MSG-GEN-002 | reason or version outside its length | {field} must be between {min} and {max}. |
| MSG-P2-024 | The case is already in the target queue | This case is already in {queue}. |
| MSG-P2-025 | The feature flag is off | Queue placement by models and agents is switched off. |
| MSG-P2-020 | The caller is not in the approved callers list | {caller} is not approved to place cases on queues. |
| MSG-P2-021 | The case has an open deviation | This case has an open deviation and stays with the deviation handler. |
| MSG-P3-005 | The case is closed | This case cannot move to {state} from {current}. |
| MSG-GEN-004 | The case changed during the placement | Someone else changed this record. Reload it to see their change. |
| MSG-P4-001 | The identity has no role (standard meaning of MSG-P4-001 in rwb-access) | Not specified in the source documents (GAP-0670; ASM-1195). |
| MSG-P4-002 | Identity lacks Queue and allocation C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Queue or case not found | This case is not in your scope. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | A consumed service does not answer inside the 2 s budget | Platform catalogue text, not restated here. |

MSG-GEN-006 is the platform message for a consumed service that does not answer inside the 2 s budget; its text is the platform catalogue text and is not restated here. MSG-P2-020, MSG-P2-021, MSG-P2-024, MSG-P2-025, MSG-P3-005, MSG-P4-002, MSG-P4-003 and MSG-P7-003 are the legacy texts, unchanged; the adapter returns a forwarded message of rwb-case or rwb-access verbatim and adds no wording of its own. Thai text for each message follows decision DL10. Open decisions: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL23 (assumptions ASM-1232, ASM-1237, ASM-1259, ASM-1560), both still open; each holds its assumptions until it is closed.

### 15. Screens and states

No screen in this story. A placed case appears in its queue on SCR-07 Team queues and SCR-02 Case list like any other case; the decision log query (SCR-38) shows the placement entry with the caller and version, and the integration admission record is read by the platform team on the operation log, not on a business screen. The caller is a job or an agent: it receives the problem response and needs no screen state. The replay state is internal to the adapter and is exposed as a metric and a log line, not as a screen.

Screen states (CG-ALL-3308, CG-ALL-3309, CG-ALL-3310): SCR-02 Case list has empty and loading as Screen Specifications v1 gives them, and error and no access: Not specified in the source documents (CG-ALL-3308). SCR-07 Team queues has loading as Screen Specifications v1 gives it; empty, error and no access: Not specified in the source documents (CG-ALL-3309). SCR-38 decision log query has loading as Screen Specifications v1 gives it; empty, error and no access: Not specified in the source documents (CG-ALL-3310).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-036-13 | Access, AC13 | Component | SY-AGENT under the production matrix (Queue and allocation R); refused with MSG-P4-002 |
| TC-E2-036-14 | Principle 5, AC14 | NFR | Decision record write forced to fail; 503 MSG-P7-003; case, assignment and outbox unchanged |
| TC-E2-036-15 | Section 12 operations, events, activities | Contract | Placement operation and the rwb-case, rwb-access and reference-data calls against their published contracts |
| TC-E2-036-16 | Section 12.7 tables | Component | idempotency_key and decision_record at the 24 hour replay limit and at the reason length of 1,000 characters |
| TC-E2-036-17 | BR6 (R-UNI-39) | Component | A decision record write failure forwards nothing and changes nothing |
| TC-E2-036-18 | BR9 (Arch v5 slide 11; DP-09) | Component | A repeat with the same Idempotency-Key inside 24 hours returns the stored answer with no second effect |
| TC-E2-036-19 | BR10 (DP-01) | Component | No class of rwb_integration writes recovery_case, assignment or queue, and none publishes on rwb.case.events.v1 |
| TC-E2-036-20 | BR11 (DP-11) | Component | Each cross-service call is one hop with a 2 s timeout and a circuit breaker |
| TC-E2-036-21 | AC15, BR6, BR9, BR10, BR11 | Component | Repeat with the same Idempotency-Key inside 24 hours returns the stored answer with no second effect; no recovery_case, assignment or queue write and no CaseAllocated or CaseTransferred publish; each cross-service call one hop with 2 s timeout and breaker; BR6 as AC14 |
| TC-E2-036-22 | AC16 | Component | Request with no valid credentials refused with 401 (message not specified in source); identity without Queue and allocation C refused with 403 MSG-P4-002; nothing forwarded |
| TC-E2-036-01 | AC1, BR1, BR2 | End to end | Approved caller MDL-SYN-PRIORITY under SY-AGENT; NEW case |
| TC-E2-036-02 | AC2, BR3 | End to end | Owners at 150 and 149; then both at 150 |
| TC-E2-036-03 | AC3, BR5 | End to end | One placement; decision log entry fields checked |
| TC-E2-036-04 | AC4, BR8 | End to end | Flag off |
| TC-E2-036-05 | AC5, BR1 | End to end | Caller MDL-SYN-UNLISTED |
| TC-E2-036-06 | AC6 | End to end | Request with no reason |
| TC-E2-036-07 | AC7, BR7 | End to end | Same request sent twice |
| TC-E2-036-08 | AC8, BR7 | End to end | CLOSED case |
| TC-E2-036-09 | AC9, BR4 | End to end | Case with X2 open |
| TC-E2-036-10 | AC10 | End to end | Queue ID that does not exist |
| TC-E2-036-11 | AC11 | End to end | Two placements against one case version |
| TC-E2-036-12 | AC12, BR3 | End to end | IN_PROGRESS case with owner U-5100 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID; TC-E2-036-21 and TC-E2-036-22 are added by this story for AC15 and AC16 and are described by those criteria and their rows above. Legacy levels map System to End to end, Access to Component and Resilience to NFR. This adapter runs TC-E2-036-01 to TC-E2-036-07, TC-E2-036-13 to TC-E2-036-22 against its own operation and the contract fakes; TC-E2-036-08 to TC-E2-036-12 are cited for the legacy key and are carried by RWB-P3-E2036-APP, which owns the case state, the queue and the events those tests assert.

### 17. Guardrails

- No business value in code: the approved callers list, the caps, the methods, the overflow queues and the decision code are data read through their owners' contracts; the adapter fixes only the behaviour.
- No personal data in logs, tests, events or prompts. The reason text is the caller's code or phrase and holds no customer data; the admission record carries the caller code, the service identity, the version and the answer, never a name, an address or an account number.
- Classed field names: Data Classification v5 (Fields) classes `interaction.actor_ref`, `interaction.idempotency_key` and `decision_log_entry.idempotency_key` as Confidential / Customer data, and `created_by` and `updated_by` of `account_ext`, `contact_point_ext` and `party_ext` as Internal / Staff identifier. This story names `actor_ref`, `created_by`, `updated_by` and `idempotency_key` (§11), so the statement that no personal data is carried does not declassify these names. The codec or masking rule for them in this story is Not specified in the source documents (CG-ALL-3306).
- No read of another service's tables: the queue, the case, the assignment and the placement outcome come only through the rwb-case contract, the approved callers list only through the rwb-case reference-data contract, and the right only through the rwb-access contract (DP-01, DP-11).
- No write of a case, a queue or an assignment row, and no publish of CaseAllocated or CaseTransferred: those belong to rwb-case, and the architecture test fails the build if this module writes or publishes them (BR10).
- The admission record is written in the same transaction as the stored answer; a failure blocks the forward and raises an incident (R-UNI-39).
- A model or agent never bypasses the allocation engine or the access check: the adapter forwards the caller identity and its own answer is never the authorisation.
- One REST base and one topic per service: this story declares `/api/recovery/integration/v1` only and consumes the rwb-case and rwb-access bases (DP-13, DP-14).
- Every example and fixture is synthetic; no production caller, case number or payload is copied into a test or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-017 | A queue accepts a write from a model or an agent with the case and the reason | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-DEV-01 | TC-E2-036-01, TC-E2-036-02, TC-E2-036-06 to TC-E2-036-12 |
| REQ-CWC-018 | A model or agent passes the same permission checks and its write is logged with its version | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | R-UNI-39 | TC-E2-036-03, TC-E2-036-13, TC-E2-036-14 |
| REQ-CWC-019 | The interface ships behind a feature flag | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-04, TC-E2-036-05 |
| REQ-CWC-020 | Model and rule work in the same queue, in one priority order | Business Requirements Epic 2, section 3.2 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-01 |
| REQ-ACA-010 | A model or agent identity passes the same role and scope checks as a person | Not specified in the source documents (GAP-0670; ASM-1196) | FEAT-CWC-29 | All recovery processes | CTL-09 | TC-E2-036-13 |

### 19. Out of scope

- The placement itself, with the queue, the allocation method, the caseload cap, the overflow queue, the assignment, the placement decision entry and the CaseAllocated and CaseTransferred events: RWB-P3-E2036-APP.
- The queue, team and role rows and the allocation engine that the placement reuses: RWB-P3-E1019-APP and RWB-P3-E1020-APP.
- The role, scope and right answer and the permission matrix versions: RWB-P4-E1037-CON and the rwb-access stories; this story only consumes the contract.
- The central decision ledger and the decision log query: RWB-P7-E2036-APP; this story writes only its local admission record.
- The open deviation that refuses a placement: RWB-S8-E2036-APP; the adapter returns the refusal it receives.
- Score and priority on the placement and queue order by priority (REQ-CWC-020): added with the first approved model consumer, in the epic that switches the flag on.
- The model or agent that calls the interface: the P10 agent runtime stories, for example RWB-E2-028.
- Granting SY-AGENT Queue and allocation C in the production matrix: a permission matrix change under RWB-E1-037.
- The real cross-service proof of the journey through gateway-bff: RWB-ITG-E2036-ITG.
- The deployment, the flag change, the alerts and the runbook of this adapter: the operations story of this epic.
