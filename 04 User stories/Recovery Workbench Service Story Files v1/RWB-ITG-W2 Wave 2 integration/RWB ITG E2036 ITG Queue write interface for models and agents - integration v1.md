# RWB-ITG-E2036-ITG Queue write interface for models and agents

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-036 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2036-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-036 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1019-APP, RWB-P3-E1020-APP, RWB-P2-E2036-APP, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-S8-E2036-APP, RWB-P7-E2036-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-016, FR-PLT-019) |
| Status | Draft (realignment v1) |

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that places a case on a queue as an approved model or agent, through gateway-bff and the owning services, under a service identity and the queue's own allocation, cap and access rules**, so that **the wave 2 queue write journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production endpoint, screen, table, workflow or schedule, it serves no operation and it owns no table. The real behaviour is owned by the I stories RWB-P3-E2036-APP (the placement operation, the queue, the assignment, the cap, the overflow queue and the events), RWB-P3-E1019-APP and RWB-P3-E1020-APP (the queue and allocation engine the placement reuses), RWB-P2-E2036-APP (the integration path the caller enters), RWB-P4-E2036-APP (the authorisation check the service identity passes), RWB-S8-E2036-APP (the open deviation that refuses a placement) and RWB-P7-E2036-APP (the decision record and the central ledger), and those stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-036 journey crosses more than one service: rwb-case holds the case, the queue, the assignment, the caseload cap, the overflow queue and the placement events; rwb-access answers the role, scope and right check that the caller's service identity passes; rwb-deviation holds the open deviation that keeps a case with its handler; rwb-decision holds the decision record, the central decision ledger and the rule version in force; and gateway-bff is the single edge the caller enters. Until the real services are exercised together, the program cannot show that analytical output reaches a person the day the decision is made and not through a weekly manual file.

The harness gives one repeatable run per business date that proves an approved caller places a case through the edge under its service identity, that the queue's assignment method and the caseload cap still decide the owner and that the overflow queue still catches a queue at its cap, that the case status follows the placement, that one decision log entry with the caller, the reason and the model version commits in one transaction with the case change, the assignment and the outbox row, and that a refusal or a failed decision log write changes nothing while a repeat with the same Idempotency-Key has no further effect. It meets REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020 and REQ-ACA-010 at the integration level and leaves every business rule, every message and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The seven I stories are published and deployed in the SIT environment: RWB-P3-E2036-APP (the placement operation, the queue, the assignment, the cap, the overflow queue and the events), RWB-P3-E1019-APP and RWB-P3-E1020-APP (the queue and allocation engine it reuses), RWB-P2-E2036-APP (the integration path), RWB-P4-E2036-APP (the authorisation answer), RWB-S8-E2036-APP (the open deviation) and RWB-P7-E2036-APP (the decision record and the ledger).
- gateway-bff is deployed with the composite route of DP-19 available and makes one REST hop to rwb-case. The gateway-bff composite placement route path and its merge order: Not specified in the source documents (GAP-0419; ASM-0594).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before the I stories land.
- The approved callers list of the legacy configuration key `rwb.casewf.placement.approved-callers` holds caller MDL-SYN-PRIORITY of type MODEL for service identity SY-AGENT, and the permission matrix in force gives SY-AGENT Queue and allocation C; queue MTG-BKK-PRI carries method ROUND_ROBIN, caseload cap 150 and overflow queue MTG-BKK-OVF, all loaded by the owning stories and read by the harness, never held by it.
- The harness environment, its test-data seeding and its evidence format and retention: Not specified in the source documents (GAP-0419; ASM-0594).

### 4. Flow

1. Harness: seeds case RW-2026-000501 with status NEW, no owner and no open deviation, queue MTG-BKK-PRI with method ROUND_ROBIN, caseload cap 150 and overflow queue MTG-BKK-OVF, and the approved caller MDL-SYN-PRIORITY under service identity SY-AGENT, through the owning contracts or the §12.8 fakes, and reads the case back to assert the seeded state.
2. Harness: sends the placement through gateway-bff to the placement operation for queue MTG-BKK-PRI under service identity SY-AGENT, with reason "High cure score", modelOrAgent MDL-SYN-PRIORITY and version 1.4.0, and a new Idempotency-Key.
3. Harness: asserts 201, the case in queue MTG-BKK-PRI, the owner chosen by ROUND_ROBIN with no owner above the caseload cap 150, and SY-AGENT on the case record and on the assignment as the identity that made the change.
4. Harness: reads GET /api/recovery/case/v1/queues and asserts the assignment method, the caseload cap and the overflow queue the owner choice used, and reads GET /api/recovery/case/v1/cases/{caseId} and asserts status ASSIGNED and the new owner.
5. Harness: seeds owners "U-5001" at 150 open cases and "U-5002" at 149, sends the placement of case RW-2026-000501 and asserts U-5002 receives it by round robin; then seeds both owners at 150 and sends the placement of case RW-2026-000502, and asserts the case in queue MTG-BKK-OVF with no owner and status NEW.
6. Harness: reads GET /api/recovery/decision/v1/decision-log and asserts exactly one entry with decision code D6, the caller SY-AGENT, the reason "High cure score", model version "MDL-SYN-PRIORITY 1.4.0" and final call "PLACED MTG-BKK-PRI".
7. Harness: asserts by timestamp order that the entry, the case change, the assignment and the outbox row commit in one transaction, that one CaseAllocated event is on rwb.case.events.v1, and that the DecisionRecorded record reaches the ledger within 5 minutes of the call.
8. Harness: reads GET /api/recovery/case/v1/cases/{caseId}/timeline and asserts the allocation of the placement is the newest queue-history entry with reason ALLOCATION.
9. Harness: forces each failure and refusal of §5 through the fakes and the owning services, asserts the message and that nothing was written, including the closed case, the open deviation, the unapproved caller, the empty field, the duplicate placement, the unknown queue, the rights refusal and the failed decision log write.
10. Harness: repeats the first placement with the same Idempotency-Key and asserts the first result is returned with no second assignment, no second decision log entry and no second event.
11. Harness: writes one run report per business date, keyed by story and business date; the report format and retention are Not specified in the source documents (GAP-0419; ASM-0594).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | The feature flag is off | 404; the case, the assignment and the decision log are unchanged | MSG-P2-025 | TC-E2-036-04-ITG |
| X2 | The caller is not in the approved callers list | 422; nothing changes | MSG-P2-020 | TC-E2-036-05-ITG |
| X3 | caseId, reason, modelOrAgent or version is empty | 422 naming the field; nothing changes | MSG-GEN-001 | TC-E2-036-06-ITG |
| X4 | The case is already in the target queue, including a repeated call | 409; still one assignment and one decision log entry | MSG-P2-024 | TC-E2-036-07-ITG |
| X5 | The case is closed | 409; nothing changes | MSG-P3-005 | TC-E2-036-08-ITG |
| X6 | The case has an open deviation | 409; the case stays in the deviation handler's queue | MSG-P2-021 | TC-E2-036-09-ITG |
| X7 | The queue or the case does not exist | 404 on the direct call and on the composite route | MSG-P4-003 | TC-E2-036-10-ITG |
| X8 | Every owner in the queue is at the caseload cap | The case is placed in the overflow queue with status unchanged and no owner | None | TC-E2-036-02-ITG |
| X9 | Two placements of the same case commit at the same time | One commits with 201; the other is refused with 409, and the case is in exactly one queue with one open assignment | MSG-GEN-004 | TC-E2-036-11-ITG |
| X10 | The caller's identity holds Queue and allocation R only | 403 on the direct call and on the composite route; the refusal is the answer, not an empty result | MSG-P4-002 | TC-E2-036-13-ITG |
| X11 | The decision log write fails | 503; the case stays where it was, with no new assignment, no event and no outbox row, and the run raises the incident assertion | MSG-P7-003 | TC-E2-036-14-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the seven I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the data seeding and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The placement is evidenced across services rather than per service, including the identity, the cap, the overflow queue and the decision record |
| Estimable | One harness project, one journey specification, one fake pack and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Queue write interface for models and agents - wave 2 integration harness

  Background:
    Given the business date is 2026-12-20
    Given feature flag "rwb.casewf.queue-placement" is on
    Given the permission matrix in force gives service identity "SY-AGENT" Queue and allocation C
    Given the approved callers list holds caller "MDL-SYN-PRIORITY" of type MODEL for service identity "SY-AGENT"
    Given queue "MTG-BKK-PRI" uses method ROUND_ROBIN with caseload cap 150 and overflow queue "MTG-BKK-OVF"
    Given case "RW-2026-000501" has status NEW, no owner and no open deviation

  Scenario: AC1 An approved model places a case through the edge under its service identity (new, D-RCV-60)
    Given the harness sends the placement through gateway-bff, the single edge of DP-19, to the placement operation for queue "MTG-BKK-PRI" under service identity "SY-AGENT"
    When "SY-AGENT" places case "RW-2026-000501" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then the answer is 201 and the case is in queue "MTG-BKK-PRI"
    And the owner is chosen by the queue's method ROUND_ROBIN and no owner holds more than the caseload cap 150
    And the case record and the assignment show "SY-AGENT" as the identity that made the change
    And each call in the composition is one hop with the 2 s budget
    And no service reads another service's schema
    And the run report holds one trace spanning the gateway and rwb-case

  Scenario: AC2 The queue rules and the overflow queue still apply (new, D-RCV-60)
    Given queue "MTG-BKK-PRI" holds owners "U-5001" with 150 open cases and "U-5002" with 149 open cases
    When "SY-AGENT" places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the case is given to "U-5002" by round robin, skipping "U-5001" at the cap
    And the case status becomes ASSIGNED
    When both owners hold 150 open cases and "SY-AGENT" places case "RW-2026-000502"
    Then the case is in queue "MTG-BKK-OVF" with no owner
    And the case status is NEW
    And no owner in "MTG-BKK-PRI" receives a case above the caseload cap 150

  Scenario: AC3 One decision log entry with the caller, the reason and the version, in one transaction (new, D-RCV-60)
    When "SY-AGENT" places case "RW-2026-000501" on queue "MTG-BKK-PRI" with reason "High cure score", modelOrAgent "MDL-SYN-PRIORITY" and version "1.4.0"
    Then one decision log entry exists with decision code D6, the caller identity "SY-AGENT", the reason "High cure score", the model version "MDL-SYN-PRIORITY 1.4.0" and final call "PLACED MTG-BKK-PRI"
    And the harness reads exactly one entry for the placement through GET /api/recovery/decision/v1/decision-log
    And the entry, the case change, the assignment and the outbox row commit in one transaction
    And one CaseAllocated event is on rwb.case.events.v1 with one outbox row on the case
    And one DecisionRecorded record reaches the ledger within 5 minutes of the call

  Scenario: AC4 Failure isolation and refusals (new, D-RCV-60)
    Given the feature flag "rwb.casewf.queue-placement" is off
    When "SY-AGENT" places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the answer is 404 with MSG-P2-025 and nothing changes
    When "SY-AGENT" places a case with modelOrAgent "MDL-SYN-UNLISTED"
    Then the answer is 422 with MSG-P2-020 and nothing changes
    When "SY-AGENT" places case "RW-2026-000501" with no reason
    Then the answer is 422 with MSG-GEN-001 for field reason and nothing changes
    Given case "RW-2026-000501" is already in queue "MTG-BKK-PRI"
    When the same request is sent again
    Then the answer is 409 with MSG-P2-024 and there is still one assignment and one decision log entry
    Given case "RW-2026-000501" has status CLOSED
    When "SY-AGENT" places it on queue "MTG-BKK-PRI"
    Then the answer is 409 with MSG-P3-005 and nothing changes
    Given case "RW-2026-000501" has an open deviation and is in the deviation handler's queue
    When "SY-AGENT" places it on queue "MTG-BKK-PRI"
    Then the answer is 409 with MSG-P2-021 and the case stays in the deviation handler's queue
    When "SY-AGENT" places case "RW-2026-000501" on a queue that does not exist
    Then the answer is 404 with MSG-P4-003
    When "SY-AGENT" places a case under a matrix that gives it Queue and allocation R only
    Then the answer is 403 with MSG-P4-002 and nothing changes
    When two placements of case "RW-2026-000501" commit at the same time
    Then one succeeds with 201 and the other is refused with 409 and MSG-GEN-004
    And the case is in exactly one queue with one open assignment
    Given the decision log write is forced to fail
    When "SY-AGENT" places case "RW-2026-000501" on queue "MTG-BKK-PRI"
    Then the answer is 503 with MSG-P7-003 and no assignment, no event and no outbox row exists
    When the same request with Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000036" is repeated after the decision log recovers
    Then the first placement result is returned and still one assignment, one decision log entry and one event exist
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a caller in the approved callers list, under the service identity listed for it, may place a case | REQ-CWC-019; configuration key rwb.casewf.queue-placement |
| BR2 | The caller passes the same access check as a person: Queue and allocation C in the permission matrix in force | REQ-CWC-018; REQ-ACA-010; CTL-09 |
| BR3 | The owner is chosen by the queue's assignment method within its caseload cap; when every owner is at the cap the case goes to the overflow queue | queue.assignment_method, capacity_cap, overflow_queue_id; DL23 |
| BR4 | A case with an open deviation stays with the deviation handler | R-DEV-01 |
| BR5 | Every placement writes one decision log entry in the same transaction as the change, with the caller identity, the reason and the model or agent version | NFR-078; Principle 5; CTL-06 |
| BR6 | A decision that cannot be written to the decision log does not proceed | R-UNI-39; Principle 5 |
| BR7 | A case closed or already in the target queue is not placed | LOV-CASE-STATUS; MSG-P3-005 |
| BR8 | The interface is off by feature flag until the first caller is approved | REQ-CWC-019; DT11 |

The harness asserts these eight rules against the owning services and re-implements none of them, so no BR row is changed by this story.

### 9. State transitions

None. The harness changes no case status, no assignment and no queue itself; it drives the placement operation and reads the records back. The table is what it observes on the case after a call to the owning service.

| Observed on the case | Before the call | After a successful placement | After a refusal |
|---|---|---|---|
| queue | none, status NEW | MTG-BKK-PRI, or MTG-BKK-OVF when every owner is at the cap | unchanged |
| owner and status | none, NEW | an owner by ROUND_ROBIN, status ASSIGNED; no owner and status NEW in the overflow queue | unchanged |
| assignment | none | one open assignment with reason ALLOCATION | unchanged |
| decision log entries for the placement | none | one entry with decision code D6, the caller and the model version | none |
| events and outbox | none | one CaseAllocated event and one outbox row in the same transaction | none |

A failed or refused placement leaves every row exactly as it was before the call.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | The service identity the harness drives: places cases once the matrix gives it Queue and allocation C and its caller is approved |
| SY-CASEWF, case workflow module | Updates the case, writes the assignment and publishes the events; the harness asserts its result, it does not act for it |
| SY-DECLOG, decision log writer | Writes the placement entry the harness reads back (Decision log C) |
| RW-TEAMMGR, team manager | Holds Queue and allocation CRUA; reads the placed case in the team queue |
| RW-COE, center of excellence analyst | Requests a caller entry in the approved callers list; used by the seeded approved caller |
| RW-RISK, risk and model risk officer | Approves a caller entry before it is loaded |
| RW-PLATADM, platform administrator | Switches the feature flag on after approval |
| RW-SECADM, security administrator | Loads the permission matrix version that grants the caller's identity Queue and allocation C |

No approval level from the delegation of authority applies: a placement moves work, it does not approve a treatment. Authorisation is answered by rwb-access through POST /api/recovery/access/v1/authorise on every call, and the harness asserts the refusal of an identity that holds Queue and allocation R only.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the rwb-case contract |
| DF-CAS-005 | recovery_case | status | Read and asserted through the rwb-case contract |
| DF-CAS-009 | recovery_case | owner_user_id | Asserted through the rwb-case contract |
| DF-CAS-010 | recovery_case | queue_id | Asserted through the rwb-case contract |
| DF-CAS-011 | recovery_case | team_code | Asserted through the rwb-case contract |
| DF-CAS-019 | recovery_case | deviation_open | Read through the rwb-case contract |
| DF-CAS-022 | recovery_case | closed_date | Read through the rwb-case contract |
| DF-WRK-001 | queue | id | Read through the rwb-case contract |
| DF-WRK-002 | queue | queue_code | Read through the rwb-case contract |
| DF-WRK-004 | queue | team_code | Read through the rwb-case contract |
| DF-WRK-006 | queue | assignment_method | Read through the rwb-case contract |
| DF-WRK-007 | queue | capacity_cap | Read through the rwb-case contract |
| DF-WRK-008 | queue | overflow_queue_id | Read through the rwb-case contract |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Asserted through the rwb-case contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the rwb-decision contract |
| DF-REF-042 | permission | capability_area | Read through the rwb-access contract |
| DF-REF-043 | permission | letters | Read through the rwb-access contract |

The service identity of the caller is written by the owning service to the standard column created_by of the assignment and to updated_by of the case; the harness asserts both and writes neither. Test data is synthetic, no production case, party or assignment is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/case/v1/queues/{queueId}/placements` | P3 rwb-case | The placement itself, through gateway-bff and directly under a service identity; Idempotency-Key required |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Case status, owner, queue, team and the open-deviation flag before and after the placement |
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | P3 rwb-case | The allocation the placement wrote, as the newest queue-history entry |
| GET | `/api/recovery/case/v1/queues` | P3 rwb-case | The queue's assignment method, caseload cap and overflow queue that decided the owner |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The one decision log entry of the placement, with the caller, the reason and the model version |
| GET | `/api/recovery/decision/v1/admin/rule-versions` | P7 rwb-decision | The rule version in force on the business date, read to assert the placement takes no rule decision of its own |
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The open deviation the refusal case is seeded with; an open deviation keeps the case with its handler |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and right check used by the edge and by the direct call (Architecture v5 slide 14: rwb-access IN POST /authorise) |

The composite route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0419; ASM-0594).

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.case.CaseAllocated.v1 | rwb.case.events.v1 | P3 rwb-case | One event per successful placement with the case, the queue and the new owner, and one outbox row written in the same transaction as the case change, the assignment and the decision log entry |
| rwb.case.CaseTransferred.v1 | rwb.case.events.v1 | P3 rwb-case | One event when the case already had an owner; the previous assignment has ended and the case keeps its status |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The decision record of the placement reaches the ledger within 5 minutes of the call and names decision code D6 and model version MDL-SYN-PRIORITY 1.4.0 |

The events are consumed for assertion only; order per case is guaranteed by the case key on the topic, and the harness reads the ledger through the P7 contract rather than from a topic.

#### 12.5 Workflows and activities

None. The harness starts no workflow and adds no activity; it drives REST only and observes the allocation step of CaseWorkflow, which runs on the Temporal task queue rwb-case in the namespace rwb-recovery, through the case contract.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow.

#### 12.7 Tables owned

None. Every table read or asserted is owned by rwb-case, rwb-decision, rwb-access or rwb-deviation; the harness never reads another service's schema and never reads a queue or a case table directly.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-case | placements, case, timeline, queues | Case RW-2026-000501 in status NEW with no owner and no open deviation; queue MTG-BKK-PRI with ROUND_ROBIN, caseload cap 150 and overflow queue MTG-BKK-OVF; 201 with the assignment, or with the overflow queue and no assignment when every owner is at the cap; 409 for a duplicate placement, a closed case and a case already in the queue; 422 for an unapproved caller and an empty field; 404 for an unknown queue and for the flag off; the stored response per Idempotency-Key |
| rwb-decision | decision-log, admin/rule-versions | The one entry of the placement with decision code D6, the caller, the reason and the model version; the ledger answer for the DecisionRecorded assertion; the rule version in force on the business date; a forced write failure for the 503 case |
| rwb-deviation | cases/{caseId}/deviations | An open deviation on the refusal case with the deviation handler as its queue; a cleared answer for every other case |
| rwb-access | authorise | Allow SY-AGENT with Queue and allocation C; refuse SY-AGENT with Queue and allocation R only, with MSG-P4-002; refuse a case outside the caller's scope with MSG-P4-003 |

The fakes are published from the owning services' OpenAPI documents and are replaced by the real service as each I story lands, contract by contract. The harness repository, its environment and its seeding: Not specified in the source documents (GAP-0419; ASM-0594).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Eight consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.case.CaseAllocated.v1, rwb.case.CaseTransferred.v1 and rwb.decision-record.DecisionRecorded.v1 for assertion; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity or Nexus operation; it observes the allocation step through the case contract |
| File | No | Reads and writes no file itself; the outbox row is asserted through the case contract |

### 13. Solution plan

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

DP-01 is applied by reading every case, queue and assignment field through the rwb-case contract and every ledger field through the rwb-decision contract, never from `rwb_case` or `rwb_decision` directly. DP-03 is applied by asserting the decision record and the DecisionRecorded record the owning service publishes. DP-07 is applied by reading the decision code list and the queue reference data through the owning contracts. DP-08 is applied through the authorise operation of rwb-access on every call. DP-09 is applied by asserting the outbox row and the CloudEvent of the placement. DP-11 is applied by one hop per call with the 2 s timeout and a breaker per downstream. DP-13 and DP-14 are applied to the paths and topic names the harness calls. DP-15 is applied by holding the harness seeding as data and asserting the migrated schema of the owner rather than creating one. DP-19 is applied through the gateway-bff composite route.

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the seven I stories.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| PlacementClient | Harness adapter | Calls the gateway-bff composite placement route and the eight consumed operations of §12.2, with a new Idempotency-Key per case and the service identity in the call |
| FakePack | WireMock project | Serves rwb-case, rwb-decision, rwb-deviation and rwb-access from the published OpenAPI documents of §12.8 |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference in the trace, so no service reads another service's tables |
| PlacementCheck | Assertion | Fails the run when the owner is not chosen by the queue's method, when an owner passes the caseload cap, when the overflow queue is not used, or when the case status does not follow the placement |
| DecisionOrderCheck | Assertion | Fails the run when the decision log entry does not commit with the case change, the assignment and the outbox row, or when there is more than one entry for one placement |
| IdempotencyVerifier | Assertion | Repeats a request with the same key and fails the run on a second assignment, a second entry or a second event |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0419; ASM-0594) |

**Environment and test data**

- Environment: SIT, one namespace, the seven I stories deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment, seeding and the composite route detail: Not specified in the source documents (GAP-0419; ASM-0594).
- Data: synthetic case RW-2026-000501 in status NEW, case RW-2026-000502 for the overflow step, then the closed and open-deviation states of §5; queue MTG-BKK-PRI with ROUND_ROBIN, caseload cap 150 and overflow queue MTG-BKK-OVF; owners U-5001 and U-5002; the approved caller MDL-SYN-PRIORITY version 1.4.0 under service identity SY-AGENT; the reason "High cure score"; decision code D6; the key 5b0c7a1e-0000-4000-8000-000000000036; the business date 2026-12-20. No production record is copied.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and PlacementClient against the published OpenAPI documents of the owning services, with the service identity in the call.
2. Publish FakePack for the four owning services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Add the placement journey of AC1 through gateway-bff, with the one-hop check, the 2 s per-call budget, the SchemaBoundaryCheck and the single trace.
4. Add the queue-rule assertions of AC2 with PlacementCheck: the method, the caseload cap 150, the overflow queue and the case status.
5. Add the decision record assertions of AC3 with DecisionOrderCheck, the outbox row, the CaseAllocated event and the five-minute ledger assertion.
6. Add the refusals and the failure isolation of AC4, including the rights refusal, the closed case, the open deviation, the duplicate, the unapproved caller, the empty field, the unknown queue, the flag off and the forced decision log failure.
7. Add IdempotencyVerifier for the repeat with the same key, replace each fake with the real service as its I story lands, then publish the run report per business date and the pass/fail gate; the gate definition: Not specified in the source documents (GAP-0419; ASM-0594).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.casewf.queue-placement` from the legacy solution plan; the harness asserts the disabled state, where the answer is 404 with MSG-P2-025 and nothing changes, and the enabled state, where an approved caller places a case and a caller that is not approved is refused.

**Done when:** the journey runs green against the seven deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, the placement shows on the case timeline with the decision log entry, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is empty | Enter {field}. |
| MSG-P2-020 | The caller is not in the approved callers list | {caller} is not approved to place cases on queues. |
| MSG-P2-021 | The case has an open deviation | This case has an open deviation and stays with the deviation handler. |
| MSG-P2-024 | The case is already in the target queue | This case is already in {queue}. |
| MSG-P2-025 | The feature flag is off | Queue placement by models and agents is switched off. |
| MSG-P3-005 | The case is closed | This case cannot move to {state} from {current}. |
| MSG-GEN-004 | The case changed during the placement | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Identity lacks Queue and allocation C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Queue or case not found | This case is not in your scope. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values, including "queue", "state", "current", "caller" and "field"; it does not own the message text. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-07 Team queues | List | The placed case appears in queue MTG-BKK-PRI with its owner and status ASSIGNED, and in queue MTG-BKK-OVF with no owner and status NEW when every owner was at the cap |
| SCR-02 Case list | List | The case shows its queue, owner and status after the placement, and the refused case shows no change |
| SCR-38 Decision log query | Read only | The one placement entry shows with decision code D6, the caller identity and the model version |

The harness opens no screen and renders no page; it asserts the answers the screens consume through the owning contracts. Screen-level behaviour remains with the owning APP stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-036-13-ITG | legacy Access, BR2, REQ-ACA-010; ITG AC4 | Component | SY-AGENT under a matrix that gives Queue and allocation R only; refused with MSG-P4-002 |
| TC-E2-036-14-ITG | legacy Principle 5, BR5, BR6; ITG AC3, ITG AC4 | NFR | Decision log write forced to fail; 503 MSG-P7-003; case, assignment and outbox unchanged |
| TC-E2-036-01-ITG | legacy AC1, BR1, BR2; ITG AC1 | Integration | Approved caller MDL-SYN-PRIORITY 1.4.0 under SY-AGENT; NEW case RW-2026-000501 |
| TC-E2-036-02-ITG | legacy AC2, BR3; ITG AC2 | Integration | Owners at 150 each; then an owner below the caseload cap 150 |
| TC-E2-036-03-ITG | legacy AC3, BR5; ITG AC3 | Integration | One placement; the decision log entry fields, the outbox row and the event checked |
| TC-E2-036-04-ITG | legacy AC4, BR8; ITG AC4 | Integration | Feature flag off |
| TC-E2-036-05-ITG | legacy AC5, BR1; ITG AC4 | Integration | Caller MDL-SYN-UNLISTED |
| TC-E2-036-06-ITG | legacy AC6; ITG AC4 | Integration | Request with no reason |
| TC-E2-036-07-ITG | legacy AC7, BR7; ITG AC4 | Integration | Same request sent twice |
| TC-E2-036-08-ITG | legacy AC8, BR7; ITG AC4 | Integration | Case with status CLOSED |
| TC-E2-036-09-ITG | legacy AC9, BR4; ITG AC4 | Integration | Case with an open deviation in the deviation handler's queue |
| TC-E2-036-10-ITG | legacy AC10; ITG AC4 | Integration | Queue ID that does not exist |
| TC-E2-036-11-ITG | legacy AC11; ITG AC4 | Integration | Two placements against one case version |
| TC-E2-036-12-ITG | legacy AC12, BR3; ITG AC2 | Integration | Case with an owner and status IN_PROGRESS placed on queue MTG-BKK-PRI |

The Covers column names the legacy AC of RWB-E2-036 that the copy is derived from and the ITG criterion of §7 that the copy asserts at integration level; the legacy AC itself stays owned by the APP story. The Level column maps the legacy System level to Integration, the legacy Access level to Component and the legacy Resilience level to NFR. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the approved callers, the caps, the methods, the overflow queues and the decision code list are data held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: the reason text is the caller's code or phrase and holds no customer data, the events carry identifiers and codes only, and the harness uses synthetic parties.
- No read of another service's schema and no direct ACE read: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway or a production endpoint.
- No bypass of the allocation engine or of the access check: the harness fails a run when a placement skips the queue's method, the caseload cap or the authorise call.
- The decision log entry commits with the change: DecisionOrderCheck fails the run when it does not, so a placement that cannot be recorded does not proceed.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-017 | A queue accepts a write from a model or an agent with the case and the reason | Business Requirements Epic 2, sections 3.2 and 4 | FEAT-CWC-29 | All recovery processes | R-DEV-01 | TC-E2-036-01-ITG, TC-E2-036-02-ITG, TC-E2-036-06-ITG, TC-E2-036-07-ITG, TC-E2-036-08-ITG, TC-E2-036-09-ITG, TC-E2-036-10-ITG, TC-E2-036-11-ITG, TC-E2-036-12-ITG |
| REQ-CWC-018 | A model or agent passes the same permission checks and its write is logged with its version | Business Requirements Epic 2, sections 3.2 and 4 | FEAT-CWC-29 | All recovery processes | R-UNI-39 | TC-E2-036-03-ITG, TC-E2-036-13-ITG, TC-E2-036-14-ITG |
| REQ-CWC-019 | The interface ships behind a feature flag | Business Requirements Epic 2, sections 3.2 and 4 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-04-ITG, TC-E2-036-05-ITG |
| REQ-CWC-020 | Model and rule work in the same queue, in one priority order | Business Requirements Epic 2, sections 3.2 and 4 | FEAT-CWC-29 | All recovery processes | None | TC-E2-036-01-ITG, TC-E2-036-02-ITG |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people | Business Requirements Epic 1, section 4 | FEAT-ACA-01 | All recovery processes | CTL-09 | TC-E2-036-13-ITG |

The legacy BRD section and rule text are kept for the four requirements of the legacy story; REQ-ACA-010 is traced at the integration level for the service identity the harness drives. This story adds no requirement ID of its own.

### 19. Out of scope

- The seven owning I stories RWB-P3-E1019-APP, RWB-P3-E1020-APP, RWB-P2-E2036-APP, RWB-P3-E2036-APP, RWB-P4-E2036-APP, RWB-S8-E2036-APP and RWB-P7-E2036-APP, and every screen, endpoint, table, rule and workflow they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-case, rwb-integration, rwb-access, rwb-deviation and rwb-decision, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The score and priority on the placement and the queue order by priority (REQ-CWC-020): added with the first approved model consumer, in the epic that switches the feature flag on.
- The model or agent that calls the interface: the P10 agent runtime stories.
- Granting SY-AGENT Queue and allocation C in the production matrix: a permission matrix change under the access epic.
- The feature flag switch in UAT and production at the release.
