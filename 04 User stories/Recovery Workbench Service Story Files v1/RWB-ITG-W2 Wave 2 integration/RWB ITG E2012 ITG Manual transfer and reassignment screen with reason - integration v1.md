# RWB-ITG-E2012-ITG Manual transfer and reassignment screen with reason

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-012 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2012-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2012-APP, RWB-S8-E2012-APP, RWB-P7-E2012-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-020) |
| Status | Draft (realignment v1) |

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that moves a case by hand through gateway-bff and the owning services, with a reason code, a rule decision and a decision record**, so that **the wave 2 manual transfer and reassignment journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production screen, endpoint, table, workflow or schedule, it serves no operation, it owns no table and it starts no workflow. The real behaviour is owned by the I stories RWB-P3-E2012-APP (the case, queue, assignment and timeline behaviour of the move), RWB-S8-E2012-APP (the X1 deviation that blocks a move) and RWB-P7-E2012-APP (the decision record and the TRANSFER rule package in force), and those three stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-012 journey crosses more than one service: rwb-case holds the case, the queue, the assignment, the timeline and the CaseTransferred event, rwb-decision holds the TRANSFER rule package and the central decision ledger, rwb-deviation holds the open X1 deviation that stops a move, and rwb-access answers the role, scope and authority check. Until the real services are exercised together through the gateway, the program cannot show that a hand-off is one action with one record, which is the outcome the program targets at 5 days from 23 days.

The harness gives one repeatable run per business date that proves the composite screen route composes the transfer form from the case and the queue, that the decision record is written before the assignment and the case update, that exactly one event and one outbox row leave the move, that the queue history is visible on the case, that a refusal or a validation answer changes nothing, and that a failure in the decision log is isolated and a repeat with the same Idempotency-Key is answered from the first result. It meets REQ-WKM-003, REQ-WKM-007, REQ-WKM-008, REQ-CWC-010 and REQ-CWC-016 at the integration level and leaves every business rule, every message and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The three I stories are published and deployed in the SIT environment: RWB-P3-E2012-APP (case, queue, assignment, timeline and CaseTransferred), RWB-S8-E2012-APP (X1 screening and the open deviation) and RWB-P7-E2012-APP (decision record, ledger and the TRANSFER package in force).
- gateway-bff is deployed with the composite route of DP-19 available. The gateway-bff composite transfer route path and its merge order: Not specified in the source documents (GAP-0396; ASM-0571).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness can run from Day 1 before the I stories land.
- LOV-TRANSFER-REASON and the queue caps are loaded by the owning stories: reason codes R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral, R06 Wrong queue, and the queue cap of 150 on LIT-BKK-01.
- The harness environment, its test-data seeding, its evidence format and its retention: Not specified in the source documents (GAP-0396; ASM-0571).

### 4. Flow

1. Harness: seeds the case, the two queues, the owners and the TRANSFER package version through the owning contracts or the published fakes, and reads the case back to assert the seeded state.
2. Harness: calls the gateway-bff composite transfer route for case RW-2026-000401 and asserts that the transfer form carries the case, the target queues of the team and the reason list.
3. Harness: drives POST /api/recovery/case/v1/cases/{caseId}/transfer through gateway-bff with a new Idempotency-Key per case, to queue LIT-BKK-01 with reason R02.
4. Harness: asserts one decision record with rule TRF-010 and package version TRF-2026.12, and asserts by timestamp order that it precedes the new assignment and the case update.
5. Harness: asserts one CaseTransferred event on rwb.case.events.v1, one outbox row on the case, the new assignment with reason code R02, and that the case status, route state and stage clock are unchanged.
6. Harness: reads GET /api/recovery/case/v1/cases/{caseId}/timeline and asserts the queue history of the move is visible (REQ-WKM-008).
7. Harness: seeds a case with an open X1 deviation and drives a second move; asserts the TRANSFER refusal TRF-010 with MSG-P3-033 and that case, assignment and decision log are unchanged.
8. Harness: forces each failure of §5 through the fakes, asserts the message and that nothing moved, then returns the fake to its healthy answer.
9. Harness: drives a bulk move of ten cases with two refusals and asserts the per-case results with MSG-P3-035; repeats the first move with the same Idempotency-Key and asserts the first assignment is returned with no second record.
10. Harness: writes one run report per business date, keyed by story and business date; the report format and retention are Not specified in the source documents (GAP-0396; ASM-0571).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A move is sent with no reason code | 422 from the direct call; the case, the assignment and the decision log are unchanged | MSG-P3-001 | TC-E2-012-04-ITG |
| X2 | A TRANSFER package rule refuses the move (TRF-010 on an open X1 deviation) | 409 with the refusing rule ID; no assignment, no case update and no decision log entry | MSG-P3-033 | TC-E2-012-02-ITG |
| X3 | The target owner is at the caseload cap | 422 naming the owner; the case stays with its owner | MSG-P3-002 | TC-E2-012-05-ITG |
| X4 | Every owner of the target queue is at the caseload cap | 422 naming every owner of the queue; the case stays in its queue | MSG-P3-002 | TC-E2-012-12-ITG |
| X5 | Reason R04 and the target owner is outside the case's team | 409 naming rule R-UNI-18; nothing moves | MSG-P3-033 | TC-E2-012-06-ITG |
| X6 | The case is closed or under a legal hold | 409 naming the state and the current state; nothing moves | MSG-P3-005 | TC-E2-012-07-ITG |
| X7 | Two moves of one case at the same second | Exactly one queue and one new assignment on the case; the other call gets 409 | MSG-GEN-004 | TC-E2-012-08-ITG |
| X8 | The same request is repeated with the same Idempotency-Key | The first assignment is returned; still one assignment, one decision record and one event | None | TC-E2-012-09-ITG |
| X9 | The decision log write fails | 503; the case stays in queue MTG-BKK-CO with owner U-CO-01, no new assignment, no event and no outbox row | MSG-P7-003 | TC-E2-012-10-ITG |
| X10 | Some cases in a bulk move are refused | Eight of ten move; each refused case carries its own message and the summary carries the count | MSG-P3-035 | TC-E2-012-11-ITG |
| X11 | No TRANSFER package version is in force on the business date | 422 for the package in force check; nothing changes and no decision log entry is written | MSG-P3-027 | TC-E2-012-15-ITG |
| X12 | The user holds RW-CASEOWN (Queue and allocation R only) | 403 on a direct call; the composite route hides the action | MSG-P4-002 | TC-E2-012-13-ITG |
| X13 | Principle 5: the decision record cannot be written | The move does not proceed; case, assignment and outbox are unchanged and the run raises the incident assertion | MSG-P7-003 | TC-E2-012-14-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the three I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the data seeding and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The hand-off is evidenced across services rather than per service, and the rule that decided it is on the evidence |
| Estimable | One harness project, one journey specification, one fake pack and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Manual transfer and reassignment screen with reason - wave 2 integration harness

  Background:
    Given the business date is 2026-12-15
    Given TRANSFER package version "TRF-2026.12" is in force, and row "TRF-010" refuses a move while a deviation is open
    Given user "U-TM-01" holds RW-TEAMMGR for team "MTG-BKK"
    Given case "RW-2026-000401" in queue "MTG-BKK-CO" owned by "U-CO-01", status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Given queue "LIT-BKK-01" uses "ROUND_ROBIN" with a caseload cap of 150 and owners "U-LO-01" with 80 cases and "U-LO-02" with 95 cases, next in turn "U-LO-02"

  Scenario: AC1 The composite transfer route through gateway-bff (new, D-RCV-60)
    Given the harness calls the composite transfer route at "Not specified in the source documents (GAP-0396; ASM-0571)" for "RW-2026-000401"
    When gateway-bff composes the answer from rwb-case and rwb-access
    Then the route returns the transfer form with queue "MTG-BKK-CO", owner "U-CO-01", the target queue "LIT-BKK-01" and the reason list carrying "R02" and "R04"
    And every call in the composition is one hop with the 2 s budget
    And no service reads another service's schema
    And the run report holds one trace spanning the gateway and each owning service

  Scenario: AC2 The move writes the decision record first, then the assignment, the case and one event (new, D-RCV-60)
    Given the harness sends the transfer of "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02" and Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000001"
    When rwb-case accepts the move
    Then one decision record exists with rule "TRF-010" and package version "TRF-2026.12" before the assignment and the case update
    And the assignment of "U-CO-01" has ended and one new assignment exists with reason "TRANSFER", reason code "R02" and queue "LIT-BKK-01"
    And the case carries queue "LIT-BKK-01", owner "U-LO-02", status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    And one CaseTransferred event is on rwb.case.events.v1 and one outbox row is on the case
    And the queue history of the move is visible on GET /cases/{caseId}/timeline

  Scenario: AC3 Refusals and validation answers leave everything unchanged (new, D-RCV-60)
    Given case "RW-2026-000402" with deviation "X1" open and owned by the complaint officer under rule "R-DEV-02"
    When the harness moves "RW-2026-000402" to queue "LIT-BKK-01" with reason "R05"
    Then the answer is 409 with MSG-P3-033 naming rule "TRF-010"
    And the case, its assignment and the decision log are unchanged
    When the harness sends a move with no reason code, a move to an owner at the cap and a move of a case under a legal hold
    Then the answers are 422 with MSG-P3-001, 422 with MSG-P3-002 and 409 with MSG-P3-005
    And no assignment, no decision record and no CaseTransferred event exists for any of the three

  Scenario: AC4 Failure isolation and the idempotent repeat (new, D-RCV-60)
    Given rwb-decision returns "UNAVAILABLE" for the decision record write
    When the harness moves "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02"
    Then the answer is 503 with MSG-P7-003
    And the case stays in queue "MTG-BKK-CO" with owner "U-CO-01" and no new assignment
    And no CaseTransferred event and no outbox row exists
    When the same request with Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000001" is repeated after rwb-decision recovers
    Then the first assignment is returned and still one assignment, one decision record and one event exist
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A manual move needs a reason code from LOV-TRANSFER-REASON | REQ-WKM-003; REQ-CWC-010 |
| BR2 | A move the TRANSFER package refuses is not made, and the refusing rule ID returned by RuleEvaluator is shown | REQ-CWC-010; RWB-E1-021; D-RCV-36 T5 |
| BR3 | A queue transfer takes its owner from the target queue's assignment method | Queue field assignment_method; RWB-E1-020 |
| BR4 | An owner at or above the queue's cap cannot receive a case | Queue field capacity_cap; DL23 |
| BR5 | A reassignment for an absent owner stays inside the case's team | R-UNI-18 |
| BR6 | A move keeps the case status, route state, stage clock and timers | R-UNI-18; R-UNI-46 |
| BR7 | A case under a legal hold or closed is not moved | R-UNI-20 |
| BR8 | A move that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR9 | A repeated request with the same Idempotency-Key has no further effect | R-UNI-40 |
| BR10 | A case with an open deviation stays with the owner the deviation rule named | R-DEV-02; R-DEV-03 |
| BR11 | The TRANSFER version in force on the business date decides the move, and the decision log records the rule ID and that package version; a case keeps the version it was moved under | D-RCV-36 T5, T7; R-UNI-38 |
| BR12 | No TRANSFER version in force is a refusal (NoPackageInForce), never a default decision | D-RCV-36 T3; R-UNI-41 |

The harness asserts these twelve rules against the owning services and re-implements none of them, so no BR row is changed by this story.

### 9. State transitions

None. The harness changes no case status, route state, stage clock or timer, and it writes no assignment, decision record or event itself. The table is what it observes on the case after a call to the owning service.

| Observed on the case | Before the call | After a successful move | After a refusal |
|---|---|---|---|
| queue, owner, team | MTG-BKK-CO, U-CO-01, MTG-BKK | LIT-BKK-01, U-LO-02, LIT-BKK | unchanged |
| assignment | one open assignment for U-CO-01 | that assignment ended, one new assignment with reason code R02 | unchanged |
| status, route state, stage clock start | IN_PROGRESS, WITH_FCR_OFFICER, 2026-12-01 | unchanged | unchanged |
| decision records for the move | none | one, with rule TRF-010 and package version TRF-2026.12 | none |

A failed move leaves every row exactly as it was before the call.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | The synthetic user the harness drives: transfers and reassigns cases in the team's scope (Queue and allocation CRUA) |
| RW-CAPACITY, capacity and workforce planner | Reassigns cases for capacity in scope All (Queue and allocation RU); used by the cap cases |
| SY-CASEWF, case workflow module | Writes the assignment and updates the case (Queue and allocation CRU); the harness asserts its result, it does not act for it |
| SY-RULES, Drools evaluator | Evaluates the TRANSFER package and returns the rule ID and the package version |
| SY-DECLOG, decision log writer | Writes the entry the harness reads back (Decision log C) |
| RW-CASEOWN, case owner | Reads the result only (Queue and allocation R); cannot transfer, and the access case proves the refusal |

No approval level from the delegation of authority applies: a transfer moves work, not money. Authorisation is answered by rwb-access through the authorise operation of §12.2.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-005 | recovery_case | status | Read through rwb-case contract |
| DF-CAS-007 | recovery_case | route_state | Read through rwb-case contract |
| DF-CAS-009 | recovery_case | owner_user_id | Read through rwb-case contract |
| DF-CAS-010 | recovery_case | queue_id | Read through rwb-case contract |
| DF-CAS-011 | recovery_case | team_code | Read through rwb-case contract |
| DF-CAS-019 | recovery_case | deviation_open | Read through rwb-case contract |
| DF-CAS-020 | recovery_case | legal_hold | Read through rwb-case contract |
| DF-WRK-001 | queue | id | Read through rwb-case contract |
| DF-WRK-004 | queue | team_code | Read through rwb-case contract |
| DF-WRK-006 | queue | assignment_method | Read through rwb-case contract |
| DF-WRK-007 | queue | capacity_cap | Read through rwb-case contract |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Read through rwb-case contract |
| DF-WRK-039 | assignment | queue_id | Read through rwb-case contract |
| DF-WRK-040 | assignment | transfer_reason_code | Read through rwb-case contract |
| DF-REF-002 | rule_row | rule_id | Read through rwb-decision contract |
| DF-REF-281 | rule_package_version | version_label | Read through rwb-decision contract |
| DF-REF-282 | rule_package_version | status | Read through rwb-decision contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through rwb-decision contract |

The rule row and the package version are read only through the rwb-decision contract; the harness reads no workbook, no drl_source and no rule_row row directly. Test data is synthetic. No production case, party or assignment is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Case status, route state, stage clock, owner, queue, team, legal hold and deviation flag after the move |
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | P3 rwb-case | The queue and transfer history of the case (REQ-WKM-008) |
| POST | `/api/recovery/case/v1/cases/{caseId}/transfer` | P3 rwb-case | The move itself, through the composite route and directly; Idempotency-Key required |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | The queue membership, the assignment method and the cap used by the form |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision records of the move, with the rule ID and the package version |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The TRANSFER version in force on the business date and its status |
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The X1 deviation seeded for the refusal case; an open X1 blocks the move |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and DoA check used by the composite route and by the direct call (Architecture v5 slide 14: rwb-access IN POST /authorise) |

The composite screen route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0396; ASM-0571).

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.case.CaseTransferred.v1 | rwb.case.events.v1 | P3 rwb-case | One event per successful move with caseId, fromOwner, toOwner, reasonCode and ruleId, and one outbox row written in the same transaction as the assignment and the case update |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The record of the move reaches the ledger within 5 minutes of the call and names rule TRF-010 and package version TRF-2026.12 |
| rwb.deviation.DeviationRaised.v1 | rwb.deviation.events.v1 | S8 rwb-deviation | The X1 deviation of the refusal case is an open deviation on the case that blocks the move under TRF-010 |

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity; it drives REST only and observes the transfer step of CaseWorkflow through the case contract.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-case | case, timeline, transfer, queues/{queueId}/cases | RW-2026-000401 in MTG-BKK-CO owned by U-CO-01, status IN_PROGRESS, route state WITH_FCR_OFFICER, stage clock 2026-12-01; LIT-BKK-01 ROUND_ROBIN cap 150 with U-LO-01 at 80 and U-LO-02 at 95; 200 with the assignment on a transfer; 409 for TRF-010, for R-UNI-18, for a legal hold and for a second move; 422 for no reason, for a cap and for no package in force; the stored response per Idempotency-Key |
| rwb-decision | decision-log, admin/rule-packages/{packageCode}/versions | TRANSFER version TRF-2026.12 in force from 2026-12-01 with row TRF-010 refusing while a deviation is open; the record of the move with rule TRF-010 and version TRF-2026.12; no version in force on 2026-12-20; a forced write failure for the 503 case |
| rwb-deviation | cases/{caseId}/deviations | X1 open on RW-2026-000402 with the complaint officer as owner under R-DEV-02; a cleared answer for every other case |
| rwb-access | authorise | Allow RW-TEAMMGR with Queue and allocation U in team MTG-BKK; refuse RW-CASEOWN for Queue and allocation U with MSG-P4-002 |

The fakes are replaced by the real service as each I story lands, contract by contract. The harness repository and its environment: Not specified in the source documents (GAP-0396; ASM-0571).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Eight consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.case.CaseTransferred.v1, rwb.decision-record.DecisionRecorded.v1 and rwb.deviation.DeviationRaised.v1; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity or Nexus operation; it observes the transfer step through the case contract |
| File | No | Reads and writes no file itself; the outbox row is asserted through the case contract |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the three I stories.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| CompositeRouteClient | Harness adapter | Calls the gateway-bff composite transfer route and the eight consumed operations of §12.2, with a new Idempotency-Key per case where the operation requires one |
| FakePack | WireMock project | Serves rwb-case, rwb-decision, rwb-deviation and rwb-access from the published OpenAPI documents of §12.8 |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference found in the trace, so a service never reads another service's tables |
| DecisionOrderCheck | Assertion | Reads the decision record, the assignment and the case update and fails the run when the record does not precede the change, or when there is more than one record for one move |
| IdempotencyVerifier | Assertion | Repeats a request with the same key and fails the run on a second assignment, a second record or a second event |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0396; ASM-0571) |

**Environment and test data**

- Environment: SIT, one namespace, the owning services deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment and data seeding: Not specified in the source documents (GAP-0396; ASM-0571).
- Data: synthetic cases RW-2026-000401, RW-2026-000402 and RW-2026-000403, queues MTG-BKK-CO and LIT-BKK-01, owners U-CO-01, U-LO-02 and U-CO-03, reasons R02 and R04, TRANSFER version TRF-2026.12 with row TRF-010, and the key 5b0c7a1e-0000-4000-8000-000000000001. No production record is copied.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and CompositeRouteClient against the published OpenAPI documents of the owning services.
2. Publish FakePack for the four owning services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Add the composite route assertion of AC1, including the 2 s per-call budget and the SchemaBoundaryCheck.
4. Add the move journey of AC2 with DecisionOrderCheck: record, then assignment and case update, then one event and one outbox row, then the timeline read.
5. Add the refusal and validation set of AC3, asserting that nothing moved for TRF-010, no reason, a cap and a legal hold.
6. Add the failure isolation of AC4 with a forced decision-log failure, then the idempotent repeat with IdempotencyVerifier.
7. Add the bulk move of X10 with the per-case results and MSG-P3-035, replace each fake with the real service as its I story lands, then publish the run report per business date and the pass/fail gate; the gate definition: Not specified in the source documents (GAP-0396; ASM-0571).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switches it exercises are `rwb.p3.manual-transfer` and `rwb.p3.drools` from the legacy solution plan; with the manual-transfer flag off the transfer operation answers 403 for every role except SY-CASEWF, and with `rwb.p3.drools` off every move is refused with MSG-P3-027. The harness asserts the disabled and the enabled state of both.

**Done when:** the journey runs green against the three deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, the queue history of the move shows on the case timeline with the rule ID and the package version, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | No reason code | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner, or every owner of the target queue, at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Case closed or under a legal hold | This case cannot move to {state} from {current}. |
| MSG-P3-027 | No TRANSFER package version in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-033 | A TRANSFER rule refuses the move | Rule {rule} does not allow this transfer. |
| MSG-P3-035 | Bulk move with refusals | {done} of {total} cases were moved. The others show the reason on their row. |
| MSG-GEN-004 | Two moves of one case at once | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | Move saved | Saved. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without Queue and allocation U | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values; it does not own the message text. For MSG-P3-027 in this journey {check} is "package in force" and {detail} names the package code TRANSFER and the business date only. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-05 Transfer case | Form | The composite route returns the case, the target queue LIT-BKK-01, the target owners with their loads and the reason list; the transfer action is offered to RW-TEAMMGR |
| SCR-05 Transfer case | At cap warning | The answer carries MSG-P3-002 naming U-CO-04, or every owner of LIT-BKK-01, and the case is unchanged |
| SCR-05 Transfer case | Refused | The answer carries MSG-P3-033 with rule TRF-010, or MSG-P3-027 when no TRANSFER version is in force |
| SCR-05 Transfer case | Saved | The answer carries MSG-GEN-005 with the assignment for a single move, or the per-case results with MSG-P3-035 for a bulk move |
| SCR-07 Team queues | List | The selection of up to 50 cases is returned, and the bulk move is driven from it with one request per case |

The harness opens no screen and renders no page; it asserts the composite route answer that the screen consumes. Screen-level behaviour remains with the owning APP stories. The harness environment and evidence detail: Not specified in the source documents (GAP-0396; ASM-0571).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-012-01-ITG | AC1, BR1, BR3, BR6, BR11 | Integration | RW-2026-000401 to LIT-BKK-01, reason R02, TRANSFER version TRF-2026.12 |
| TC-E2-012-02-ITG | AC2, BR2, BR10 | Integration | RW-2026-000402 with X1 open under R-DEV-02; row TRF-010 refuses |
| TC-E2-012-03-ITG | AC3, BR4, BR5, BR11 | Integration | Ten cases to U-CO-03 with 60 open cases, reason R04 |
| TC-E2-012-04-ITG | AC4, BR1 | Integration | Request with no reason code |
| TC-E2-012-05-ITG | AC5, BR4 | Integration | U-CO-04 at 150 of 150 |
| TC-E2-012-06-ITG | AC6, BR5 | Integration | U-CO-09 in team SME-NTH, reason R04 |
| TC-E2-012-07-ITG | AC7, BR7 | Integration | RW-2026-000403 with legal hold true |
| TC-E2-012-08-ITG | AC8 | Integration | Two parallel requests for one case |
| TC-E2-012-09-ITG | AC9, BR9 | Integration | Same Idempotency-Key twice |
| TC-E2-012-10-ITG | AC10, BR8 | Integration | Decision log store stopped |
| TC-E2-012-11-ITG | AC11 | Integration | Ten cases, two under a legal hold |
| TC-E2-012-12-ITG | AC12, BR4 | Integration | Both LIT-BKK-01 owners at 150 |
| TC-E2-012-13-ITG | Access | Component | RW-CASEOWN (Queue and allocation R) calls the transfer endpoint; refused with MSG-P4-002 |
| TC-E2-012-14-ITG | Principle 5 | NFR | Decision log write forced to fail; case, assignment and outbox unchanged |
| TC-E2-012-15-ITG | AC13, BR12 | Integration | No TRANSFER version in force on 2026-12-20; NoPackageInForce and MSG-P3-027 |

The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the legacy test case ID. The Covers column names the legacy AC of RWB-E2-012 that the ITG copy is derived from; the Level column maps the legacy System level to Integration, the legacy Access level to Component and the legacy Resilience level to NFR.

### 17. Guardrails

- No business value in code: the reason codes, the caps, the bulk limit and the TRANSFER rows are data held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: the note field is not logged, the events carry IDs and codes only, and the harness uses synthetic parties.
- No read of another service's schema and no direct ACE read: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway or a production endpoint.
- The decision record is written before the case changes; DecisionOrderCheck fails the run when it is not, so a move that cannot be logged does not proceed.
- No second rule engine: the harness reads rule ID and package version through the rwb-decision contract, and no caller reads the workbook, drl_source or rule_row.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-003 | Manual transfer or reassignment only with a reason code from the agreed list | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-DEV-02, R-UNI-20, R-UNI-39, R-UNI-40 | TC-E2-012-01-ITG, TC-E2-012-02-ITG, TC-E2-012-04-ITG, TC-E2-012-07-ITG to TC-E2-012-10-ITG, TC-E2-012-13-ITG, TC-E2-012-14-ITG, TC-E2-012-15-ITG |
| REQ-WKM-007 | An absent or over-cap owner's cases reallocated inside the team, keeping state and clocks | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-04, FEAT-WKM-10 | All recovery processes | R-UNI-18, R-UNI-46 | TC-E2-012-03-ITG, TC-E2-012-05-ITG, TC-E2-012-06-ITG, TC-E2-012-11-ITG, TC-E2-012-12-ITG |
| REQ-WKM-008 | Queue and transfer history visible on the case | Business Requirements Epic 2, section 4; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-UNI-18 | TC-E2-012-01-ITG, TC-E2-012-03-ITG |
| REQ-CWC-010 | Cases move between queues and roles by transfer rules, including a manual request with a reason code | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-01 | All recovery processes | R-UNI-18, R-UNI-20, R-UNI-38, R-UNI-41 | TC-E2-012-01-ITG, TC-E2-012-02-ITG, TC-E2-012-03-ITG, TC-E2-012-11-ITG, TC-E2-012-12-ITG, TC-E2-012-15-ITG |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-01, FEAT-CWC-21 | All recovery processes | R-UNI-38, R-UNI-39 | TC-E2-012-01-ITG, TC-E2-012-02-ITG, TC-E2-012-03-ITG, TC-E2-012-15-ITG |

The rule ID and the package version on the decision record carry REQ-CWC-016 at the integration level; this story adds no requirement ID of its own.

### 19. Out of scope

- The three owning I stories RWB-P3-E2012-APP, RWB-S8-E2012-APP and RWB-P7-E2012-APP, and every screen, endpoint, table, rule and workflow they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-case, rwb-decision, rwb-deviation and rwb-access, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- Automatic reallocation when an owner is absent or over the cap (RWB-E1-030).
- The full case record view with the queue history screen (RWB-E2-016); this story asserts the timeline operation only.
- Rule-driven transfers on stage change, route decision and timer expiry (RWB-E1-021).
- The TRANSFER package rows themselves, their scenarios and their approval (RWB-E1-073).
- Partner placement and recall (Epic 6).
