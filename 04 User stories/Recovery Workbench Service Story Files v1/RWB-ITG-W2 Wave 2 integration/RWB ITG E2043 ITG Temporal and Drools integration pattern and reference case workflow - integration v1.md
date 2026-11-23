# RWB-ITG-E2043-ITG Temporal and Drools integration pattern and reference case workflow

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2043-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-043 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2043-APP, RWB-P7-E2043-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-014, FR-PLT-015, FR-PLT-020, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-043 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable harness that proves the one order every case workflow must follow — the signal arrives, the rules are evaluated in an activity against the package version in force, the decision record is written in its own activity, the state change is applied in a third, and a failure at any step stops the next — on the reference workflow of the target platform, with the version chosen at evaluation time pinned and replayable**, so that **Epic 3 copies one proven order and one proven replay behaviour instead of inventing them per workflow, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production workflow, no activity, no table, no schedule, no endpoint and no screen; it serves no operation, it owns no table and it starts no workflow of its own. The real behaviour is owned by the two I stories RWB-P3-E2043-APP (the reference case workflow on `rwb-case` in namespace `rwb-recovery`, its signal handling, its three activities, the reference fixture, the `ref-case-` prefix, the synthetic guard and the state change through the rwb-case state service) and RWB-P7-E2043-APP (the rule evaluation against the package version in force, the pinned version in the result, the local decision-record library and its publication on `rwb.decision-record.v1`), and those two stories block the ITG run.

The harness also reads the case, the record and the two topics through the published contracts, because the order of the four steps can only be asserted across the workflow history, the record and the case state together. Those reads are asserted through the published contracts and the §12.8 fakes; they are not claimed as work of this story.

### 2. Business rationale

The legacy RWB-E2-043 skeleton showed the pattern inside one module: the signal, the evaluator, the decision log writer and the case state service were called in process against one runtime. In the target architecture the same loop crosses services: rwb-case holds the case, its status and route state and the reference workflow on its own task queue; rwb-decision holds the rule package versions in force, the local decision-record library and the central ledger behind `rwb.decision-record.v1`; rwb-source-data serves the case facts the evaluation reads; and Kafka carries the case event that starts the run. Until those are exercised together, the program cannot show that Epic 3 can copy one order onto the target call types.

Epic 3 will add a workflow per case, and each squad would otherwise invent its own order of steps. A workflow that applies a state change before its decision record breaks the record-first principle, and a workflow that calls Drools outside an activity breaks replay. The harness fixes both in one test-only skeleton that runs with no live case, so Epic 3 can copy it without a production risk.

The target edition also moves the loop onto the target patterns: DP-09 (outbox and inbox with CloudEvents) instead of the monolith's direct publish, DP-10 (Temporal and Schedules on the owning service's queue) instead of Quartz and the shared job table, DP-11 (one-hop REST with a mock and the 2 s timeout) instead of the in-process call, and DP-14 (the `rwb.<short>.events.v1` topic naming) instead of the monolith's topic names. The same loop is therefore proven on the call types the target architecture actually uses, not on the monolith's. It meets REQ-DRI-001, REQ-DRI-005, REQ-CWC-016 and REQ-DRI-007 at the integration level and leaves every business rule, every message and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The two I stories are published and deployed in the SIT environment: RWB-P3-E2043-APP (the reference workflow, its three activities, the fixture and the synthetic guard) and RWB-P7-E2043-APP (the evaluation against the version in force, the pinned result and the decision-record library).
- The namespace is `rwb-recovery` and the case task queue is `rwb-case`; the skeleton keeps the workflow ID prefix `ref-case-` while production case workflows use `case-{caseId}`.
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents and the event schemas, so the harness runs green from Day 1 before the I stories land.
- Package RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01, with rule R-RES-04 moving IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER; later version "RES-2027.01" is in force from 2027-01-01.
- The synthetic case "RW-2026-000777" exists in the DEV and SIT test data, is marked synthetic, has status IN_PROGRESS and route state IN_FCR_QUEUE; no live case is used.
- The case events "EV-CASE-0777-01" to "EV-CASE-0777-05" are published or replayed on `rwb.case.events.v1` with the CloudEvents headers and the event key.
- The retry policy is the legacy value: initial interval 1 s, backoff coefficient 2, maximum 10 attempts, and NoPackageInForce is not retryable.
- The production switch `rwb.p3.temporal` is on in the harness environment; with it off no worker polls `rwb-case` and the reference workflow is not registered.
- The harness repository, the SIT environment, the seeding set of the synthetic case and the package versions, the evidence format and its retention, and the pass or fail gate: Not specified in the source documents (GAP-0422; ASM-0597).

### 4. Flow

1. Harness: seeds the synthetic case "RW-2026-000777" at IN_PROGRESS with route state IN_FCR_QUEUE and package RESTRUCTURE version "RES-2026.12" in force from 2026-12-01 through the owners' published operations or the §12.8 fakes, and reads the case back through the rwb-case contract to assert the seeded state.
2. Harness: publishes the case event "EV-CASE-0777-01" of type CASE_PICKED_UP on `rwb.case.events.v1` with the event key and asserts that the relay signals `CaseEvent` to the workflow "ref-case-RW-2026-000777" with that payload.
3. Harness: reads the workflow history and asserts the four steps in order — the signal handled, then EvaluateRulesActivity, then WriteDecisionLogActivity, then ApplyStateActivity — with no activity scheduled before the signal and no other order.
4. Harness: asserts rule "R-RES-04" and package version "RES-2026.12" in the recorded result of the evaluation, one decision record on `rwb.decision-record.v1` for the event key, and the route state WITH_FCR_OFFICER read back through the rwb-case contract.
5. Harness: drives the failure path — the decision record unavailable, the record refused for a missing field and no package in force — and asserts that the state activity is never called, that the route state stays IN_FCR_QUEUE and that the workflow fails with the message of §14 after its retries, or at once for the non-retryable case.
6. Harness: drives the idempotent retry on the same key after an activity commits and times out, and asserts one state row, one record and one completion; then repeats the same event key from the topic and asserts the inbox drops it.
7. Harness: asserts the pinned version — the evaluation recorded "RES-2026.12" — then lets "RES-2027.01" take effect from 2027-01-01 while the workflow waits, and replays the recorded history on 2027-01-05, asserting the same version, the same activity path and the same state move with no second evaluation.
8. Harness: asserts the flag-off and flag-on behaviour with no live case: off, no worker on `rwb-case` and no reference workflow; on, the four steps run with the synthetic flag true, the `ref-case-` prefix holds and no `recovery_case` row outside the fixture is read or written.
9. Harness: writes one run report per business date, keyed by story and business date, with the trace of every history event, contract call and topic assertion; the report format, its retention and the pass or fail gate are Not specified in the source documents (GAP-0422; ASM-0597).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | The decision record store of rwb-decision is unavailable when WriteDecisionLogActivity runs | The state activity is not called; the route state stays IN_FCR_QUEUE; the workflow is FAILED after the last attempt and an incident is raised | MSG-P7-003 | TC-E2-043-02-ITG |
| X2 | The Temporal frontend is unreachable when the relay sends the signal | The signal fails; the case event stays on `rwb.case.events.v1` with the same event key and its delivery RETRYING with the next attempt time; the history gains no activity attempt | MSG-P3-036 | TC-E2-043-05-ITG |
| X3 | An activity commits and then times out before it returns | The retry with the same idempotency key finds the first row and returns it; one state row, one record and one completion exist | None | TC-E2-043-03-ITG |
| X4 | A new package version is in force while the workflow waits ("RES-2027.01" from 2027-01-01) | The recorded result keeps the version chosen at evaluation time, "RES-2026.12"; the replay on 2027-01-05 reads it and never calls the evaluator again | None | TC-E2-043-04-ITG |
| X5 | `rwb.p3.temporal` is off | No worker polls `rwb-case`, the reference workflow is not registered and nothing runs; the outbox deliveries of the case topic stay PENDING | None | TC-E2-043-06-ITG |
| X6 | A second CaseEvent arrives while the first is processing | The signal is buffered and the first path completes in signal order; each key gives one state row and one record | None | TC-E2-043-01-ITG |
| X7 | No package is in force for RESTRUCTURE at evaluation time (NoPackageInForce) | The activity fails at once with no retry; the workflow is FAILED and the route state stays IN_FCR_QUEUE | MSG-P3-027 | TC-E2-043-02-ITG |
| X8 | The decision record is refused for a missing field (rule version) | The record is not written, the refusal is not retried, the state activity is not called and nothing moves | MSG-P7-009 | TC-E2-043-02-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the two I stories are deployed; until then it runs against the §12.8 fakes and the case-event stub |
| Negotiable | The harness pack, the seeding set and the evidence format are agreed with QA; no business value and no retry value is fixed by the harness |
| Valuable | Epic 3 copies one proven order and one proven replay behaviour instead of inventing them per workflow |
| Estimable | One harness project, one reference workflow, seven assertions, one fake pack and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated run with synthetic data and a machine-checkable history and result |

### 7. Acceptance criteria

```gherkin
Feature: Temporal and Drools integration pattern and reference case workflow - wave 2 integration harness

  Background:
    Given the namespace is rwb-recovery and the case task queue is rwb-case
    Given RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01
    Given rule R-RES-04 moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER
    Given the synthetic case "RW-2026-000777" has status IN_PROGRESS and route state IN_FCR_QUEUE
    Given rwb.p3.temporal is on and a worker polls "rwb-case"

  Scenario: AC1 The four steps run in order on the target queue and namespace (new, D-RCV-60)
    Given the reference workflow "ref-case-RW-2026-000777" is running and waits for a CaseEvent
    When the frontend is unreachable and the relay delivers the case event "EV-CASE-0777-05"
    Then WorkflowGateway.signal fails with MSG-P3-036
    And "EV-CASE-0777-05" stays on the topic rwb.case.events.v1 with its delivery RETRYING and the next attempt time
    And the history shows no activity attempt and no state row is written for the key "CASE_EVENT:EV-CASE-0777-05"
    Given the frontend is reachable again and the case event "EV-CASE-0777-01" of type CASE_PICKED_UP is on the topic rwb.case.events.v1
    When the relay signals "CaseEvent" with the payload of "EV-CASE-0777-01" and the key "CASE_EVENT:EV-CASE-0777-01"
    Then the history of "ref-case-RW-2026-000777" shows the CaseEvent signal handled and no activity scheduled before it
    And the history then shows EvaluateRulesActivity, then WriteDecisionLogActivity, then ApplyStateActivity, in no other order
    And the recorded result of EvaluateRulesActivity carries rule "R-RES-04" and package version "RES-2026.12"
    And one decision record exists on rwb.decision-record.v1 with rule "R-RES-04", rule version "RES-2026.12" and the key "CASE_EVENT:EV-CASE-0777-01"
    And the route state read back through GET /api/recovery/case/v1/cases/RW-2026-000777 is WITH_FCR_OFFICER
    And no state row is written before its decision record
    And the workflow is COMPLETED once and the run report holds one trace across rwb-case, rwb-decision and the topics
    And the workflow ID keeps the prefix "ref-case-" and no service reads another service's schema

  Scenario: AC2 A failed decision-record write stops the state change and the workflow fails after its retries (new, D-RCV-60)
    Given the decision record store of rwb-decision is unavailable for the key "CASE_EVENT:EV-CASE-0777-02"
    When the case event "EV-CASE-0777-02" of type CASE_PICKED_UP is signalled to "ref-case-RW-2026-000777"
    Then WriteDecisionLogActivity throws DecisionLogUnavailableException on every attempt
    And the activity is retried 10 times with the initial interval 1 s and the backoff coefficient 2
    And the workflow does not call ApplyStateActivity
    And the route state of "RW-2026-000777" stays IN_FCR_QUEUE
    And no decision record exists for the key and the workflow is FAILED with MSG-P7-003
    And an incident is raised and the run report names the attempt count
    Given the decision record store answers again and refuses the record for a missing rule version
    When the same key is evaluated and recorded again
    Then the record is refused with MSG-P7-009 naming "ruleVersion" and the refusal is not retried
    And no decision record is written and no state row is written
    Given no RESTRUCTURE package is in force on the business date
    When the evaluation of the same key runs again
    Then EvaluateRulesActivity fails with NoPackageInForce and the retry policy does not retry it
    And the workflow is FAILED with MSG-P3-027 and the route state stays IN_FCR_QUEUE

  Scenario: AC3 Idempotent retries on the same event key give one state row, one record and one completion (new, D-RCV-60)
    Given ApplyStateActivity commits the state row for "CASE_EVENT:EV-CASE-0777-03" and then times out before it returns
    When Temporal retries the activity with the same idempotency key
    Then the second attempt returns the first result and changes nothing
    And one state row exists for the key and the route state is WITH_FCR_OFFICER once
    And WriteDecisionLogActivity ran once and one decision record exists on rwb.decision-record.v1 for the key
    And the workflow is COMPLETED once and its history shows one completion event
    Given the same case event "EV-CASE-0777-03" arrives again on the topic with the same key
    When the relay signals it again
    Then the inbox drops the duplicate
    And no second state row, no second decision record and no second completion is written

  Scenario: AC4 The pinned version survives replay after RES-2027.01 takes effect, and the flag guards the skeleton (new, D-RCV-60)
    Given EvaluateRulesActivity recorded package version "RES-2026.12" and rule "R-RES-04" for "CASE_EVENT:EV-CASE-0777-04"
    Given RESTRUCTURE version "RES-2027.01" is in force from 2027-01-01 while the workflow waits for the next event
    When the workflow is replayed from its recorded history on 2027-01-05
    Then the recorded result still carries "RES-2026.12" and "R-RES-04"
    And the replay reads the recorded activity result and never calls the rule evaluator again
    And the replay reaches the same activity path and the same state move
    And the record of the key keeps rule version "RES-2026.12", while a record written after 2027-01-01 for a new key carries "RES-2027.01"
    Given rwb.p3.temporal is off
    When the application starts
    Then no worker polls "rwb-case" and the reference workflow is not registered
    When the flag is on and the harness starts "ref-case-RW-2026-000777" with synthetic "true"
    Then the four steps run with no live case
    And no recovery_case row outside the synthetic fixture is read or written
    And the workflow ID keeps the prefix "ref-case-" and never "case-"
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code is deterministic: no clock, random or I/O; Drools is called only inside EvaluateRulesActivity | D-RCV-36 T7; ADR-011 |
| BR2 | The order is signal, evaluate, record, state; no state row is written without its decision record | REQ-DRI-005; Principle 5; R-UNI-39 |
| BR3 | Every activity is idempotent by the event idempotency key; a retry gives one row | REQ-DRI-005; R-UNI-40 |
| BR4 | The package version is chosen at evaluation time, pinned in the result and written to the decision record; the replay uses the recorded result | D-RCV-36 T7; R-UNI-38 |
| BR5 | Payloads are encrypted by the codec; the history and the logs hold references and codes only | D-RCV-36 T1; NFR-034 |
| BR6 | When Temporal is unavailable the signal fails with MSG-P3-036 and the outbox keeps the case event for the next attempt | REQ-DRI-007; RWB-TE-006 |
| BR7 | The reference skeleton is test-only: it runs only under `rwb.p3.temporal` and only with a synthetic case | D-RCV-36 T1; ADR-011 |
| BR8 | Retry policy: initial interval 1 s, backoff coefficient 2, maximum 10 attempts; NoPackageInForce is not retryable | D-RCV-36 T1, T7 |
| BR9 | The state change goes through the owner's service — ApplyStateActivity calls the rwb-case case state service — and never a direct table write | REQ-DRI-005; D-RCV-36 T1; DP-01 |

The harness asserts these nine rules against the owning services and re-implements none of them, so no BR row is changed by this story.

### 9. State transitions

None caused by the harness. The harness sets nothing by hand: it drives the workflow and the owning services and observes the result in the workflow history and on the case.

| From | Event | Condition | To |
|---|---|---|---|
| RUNNING | CaseEvent | Evaluate, record and apply all succeed | COMPLETED |
| RUNNING | CaseEvent | The decision record write fails after 10 attempts | FAILED |
| RUNNING | CaseEvent | NoPackageInForce | FAILED, no retry |
| IN_FCR_QUEUE | CASE_PICKED_UP | R-RES-04 fires | WITH_FCR_OFFICER |

| Observed fact | Before the run | After the successful path | After a failed step |
|---|---|---|---|
| workflow state | RUNNING | COMPLETED | FAILED after the retries, or FAILED at once for NoPackageInForce |
| route state of the synthetic case | IN_FCR_QUEUE | WITH_FCR_OFFICER | IN_FCR_QUEUE, unchanged |
| decision record for the key | none | one on rwb.decision-record.v1 with rule and version | none, or one written and not applied where the state step failed |
| activity attempt count | 0 | 1 per activity | 10 for a retryable failure, 1 for a refusal |

A refusal or a failure writes no state row and leaves the route state exactly as it was before the call.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs the reference workflow and its three activities on `rwb-case`; the harness asserts its history, it does not act for it |
| SY-RULES, rule evaluator service account | Evaluates the package inside EvaluateRulesActivity; the harness asserts rule "R-RES-04" and version "RES-2026.12" in the recorded result |
| SY-DECLOG, decision record writer | Writes the record inside WriteDecisionLogActivity and publishes it on `rwb.decision-record.v1`; the harness asserts one record per key |
| RW-PLATADM, platform administrator | Reads the run and the history in the Temporal Web UI and receives the incident of a failed workflow |
| RW-AUDIT, internal audit | Reads the recorded history with encrypted payloads only; changes nothing |
| RW-COE, center of excellence analyst | Owns the RESTRUCTURE versions the reference uses; the harness reads them and never changes them |

No delegation of authority level applies: the reference workflow takes no credit decision. This story applies no DP-08, so it consumes no authorise operation: the authorisation of the platform surface is the platform's own, answered inside the platform workflow story RWB-PLT-E2038-APP, and the harness drives no business operation that would need a right.

### 11. Data

The harness owns no table and writes no row directly. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 rwb-decision contract; the row is written by WriteDecisionLogActivity |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read through the P7 rwb-decision contract |
| DF-DEC-031 | decision_log_entry | idempotency_key | Read through the P7 rwb-decision contract; the event key of the case event |
| DF-OPS-189 to DF-OPS-197 | outbox_event | all fields | Read, for the case event that stays on the topic when the signal fails |
| DF-OPS-198 to DF-OPS-206 | outbox_delivery | status, next attempt time | Read, through the owner's contract and the §12.8 fake |
| DF-CAS-001 | recovery_case | id | Read through the P3 rwb-case contract; the synthetic fixture only |
| DF-CAS-005 | recovery_case | status | Read through the P3 rwb-case contract |
| DF-CAS-007 | recovery_case | route_state | Read and written only through the P3 rwb-case contract, by ApplyStateActivity |

The package version in force and the pinned version are read through the rwb-decision contract, and the synthetic case facts through the rwb-source-data data-product contract; the harness holds no copy of either. Test data is synthetic. No production case, party or package version is copied, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services and drives the workflow; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The status and route state of the synthetic case, before and after the state change (Architecture v5 slide 14: rwb-case IN GET /cases/{id}) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision records of the run by case, rule and rule version, including the record of the pinned version (Architecture v5 slide 14: central decision ledger) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The synthetic case facts the evaluation reads, through the data-product contract (DP-05; Architecture v5 slide 15: rwb-source-data IN) |

The case event, the decision record and the package-in-force events of §12.4 are read for assertion only; the harness reads the record through the P7 contract rather than from a topic. The ownership map holds no outbox delivery read for rwb-case, so the retry of X2 is asserted through the absence of the effect and the same event key on `rwb.case.events.v1`, and the missing admin read is carried in GAP-0422.

This story applies no DP-08 and consumes no authorise operation: the authorisation of the platform surface is the platform's own, answered inside the platform workflow story RWB-PLT-E2038-APP, and the harness drives no business operation that would need a right.

#### 12.3 Events published

None. The harness produces no event; the case-event stub of §12.8 publishes the case event for the run.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | P3 rwb-case | The case event carrying eventType CASE_PICKED_UP and the event key reaches the relay, and the relay signals the workflow with it; a duplicate with the same key is dropped and adds no state row |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | One record per decision with rule "R-RES-04", rule version "RES-2026.12" and the event key; no record appears for the key of the failed run |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 rwb-decision | The version in force from 2026-12-01, then the switch to "RES-2027.01" from 2027-01-01, asserted while the recorded result keeps "RES-2026.12" |

#### 12.5 Workflows and activities

None added. The reference workflow and its three activities belong to the two I stories; this story exercises them and asserts their history.

| Workflow or activity | Task queue | Owner | What the harness does |
|---|---|---|---|
| ReferenceCaseWorkflow | rwb-case | P3 rwb-case | Starts it with the workflow ID "ref-case-RW-2026-000777", signals "CaseEvent", reads its history and replays it |
| EvaluateRulesActivity | rwb-case | P3 rwb-case | Asserts the recorded result carries rule "R-RES-04" and version "RES-2026.12", and that a replay never calls the evaluator again |
| WriteDecisionLogActivity | rwb-case | P7 rwb-decision (library), run on rwb-case | Asserts one record per key, MSG-P7-003 on the unavailable store and MSG-P7-009 on the refused record |
| ApplyStateActivity | rwb-case | P3 rwb-case | Asserts one state row per key and the route state WITH_FCR_OFFICER read back through the case contract |

The skeleton keeps the `ref-case-` prefix while production case workflows use `case-{caseId}`; the harness fails the run when a workflow ID leaves the prefix.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow; the skeleton owns no schedule.

#### 12.7 Tables owned

None. The record is a decision_log_entry row owned by P7 rwb-decision, the case and its route state are owned by P3 rwb-case, and the outbox rows are library objects in each service's own schema (DP-09).

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-case | cases/{caseId} | "RW-2026-000777" at IN_PROGRESS with route state IN_FCR_QUEUE, then WITH_FCR_OFFICER after the state change; one state row per key; 404 for a case outside the fixture |
| rwb-decision | decision-log | One record per key with rule "R-RES-04" and rule version "RES-2026.12", then "RES-2027.01" in force from 2027-01-01; an unavailable store, a refused record with MSG-P7-009 naming "ruleVersion", and NoPackageInForce for the evaluation case |
| rwb-source-data | data-products/{productCode}/records | The synthetic case facts of "RW-2026-000777" for the RESTRUCTURE evaluation, with freshness and no personal data field outside the fixture |
| case-event stub | rwb.case.events.v1 | The case events "EV-CASE-0777-01" to "EV-CASE-0777-05" with CloudEvents headers and the event key; a 503 answer to the signal for the frontend-unreachable case, and the same event key replayed once for the duplicate case |

The fakes are replaced by the real service as each I story lands, contract by contract. The harness repository, the seeding set, the evidence format and its retention, the pass or fail gate, and the exact response values of the fakes: Not specified in the source documents (GAP-0422; ASM-0597).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Three consumed operations of §12.2 through the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Reads `rwb.case.events.v1`, `rwb.decision-record.v1` and `rwb.decision.events.v1` for the signal, record and in-force assertions; publishes nothing |
| Temporal | Yes | Starts ReferenceCaseWorkflow on the task queue rwb-case in namespace rwb-recovery, reads its history and replays it; adds no workflow and no activity |
| File | No | Reads and writes no file; every payload is asserted through the history and the contracts, never stored in clear |

### 13. Solution plan

**Microservice move**

The monolith called the evaluator, the decision log and the case state service in process. The target moves each of them: the in-process call becomes a one-hop REST contract with a mock and the 2 s timeout (DP-11), called inside an activity; Quartz and the shared job table give way to a durable Temporal workflow on `rwb-case` in namespace `rwb-recovery` (DP-10); the decision log becomes the local decision-record library and `rwb.decision-record.v1` (DP-03); every topic follows `rwb.<short>.events.v1` (DP-14); the publish runs through outbox and inbox with CloudEvents (DP-09); the rules run as embedded Drools from rwb-decision's packages (DP-04); the ACE facts arrive through rwb-source-data (DP-05) and the reference data through rwb-case (DP-07); each service keeps its own schema and its own Flyway sequence (DP-01, DP-15); and the screen composes through the gateway-bff composite route (DP-19). The harness proves the loop on those call types, not on the monolith's.

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
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the two I stories.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| WorkflowDriver | Harness adapter | Starts ReferenceCaseWorkflow on rwb-case with the workflow ID "ref-case-RW-2026-000777", signals "CaseEvent", reads the history and asks for the replay of the recorded history |
| ContractClient | Harness adapter | Calls the three consumed operations of §12.2 for the case, the record and the case facts, one hop each with the 2 s budget |
| CaseEventStub | Stub publisher | Publishes "EV-CASE-0777-01" to "EV-CASE-0777-05" on `rwb.case.events.v1` with the CloudEvents headers and the event key, and answers 503 to the signal for the frontend-unreachable case |
| FakePack | WireMock project | Serves rwb-case, rwb-decision, rwb-source-data and the case-event stub from the published OpenAPI documents and event schemas of §12.8 |
| StepOrderCheck | Assertion | Fails the run when an activity appears before the signal, when the order is not evaluate, record, state, or when a state row is written with no decision record |
| IdempotencyCheck | Assertion | Fails the run when a retry, or a duplicate event on the same key, adds a second state row, a second record or a second completion |
| ReplayCheck | Assertion | Fails the run when a replay calls the evaluator again, or when a recorded result loses the version chosen at evaluation time |
| SyntheticGuardCheck | Assertion | Fails the run when a workflow ID leaves the `ref-case-` prefix, when the synthetic flag is false, or when a recovery_case row outside the fixture is read or written |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference found in the trace, so no service reads another service's tables |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0422; ASM-0597) |

**Environment and test data**

- Environment: SIT, namespace `rwb-recovery`, task queue `rwb-case`, the two I stories deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, SIT environment and data seeding: Not specified in the source documents (GAP-0422; ASM-0597).
- Data: the synthetic case "RW-2026-000777" at IN_PROGRESS with route state IN_FCR_QUEUE; RESTRUCTURE "RES-2026.12" in force from 2026-12-01 and "RES-2027.01" from 2027-01-01; rule R-RES-04; the case events "EV-CASE-0777-01" to "EV-CASE-0777-05"; the retry policy of BR8; the business date 2026-12-01 and the replay date 2027-01-05. Every row is synthetic and no production record is copied.
- Reset: each run starts from the seeded state and removes the synthetic fixture at the end, so a repeated run is deterministic and the same report is produced; the seeding order and the seeding script: Not specified in the source documents (GAP-0422; ASM-0597).

**Build steps**

1. Build JourneyRunner, WorkflowDriver and ContractClient against the published OpenAPI documents and the workflow interface of the two I stories.
2. Publish FakePack and the case-event stub, and prove the harness runs green from Day 1 on the fakes before the I stories land.
3. Add the signal path and the order assertion of AC1 with StepOrderCheck: the signal, the three activities in order, rule "R-RES-04", version "RES-2026.12", one record and one state move, and the frontend-unreachable case with the same event key kept on the topic.
4. Add the failure set of AC2: the unavailable record store with the 10 attempts and MSG-P7-003, the refused record with MSG-P7-009 and the non-retryable NoPackageInForce with MSG-P3-027, and assert that the route state never moves.
5. Add the idempotency set of AC3: the timeout after commit, the retry on the same key and the duplicate event dropped by the inbox, with one state row, one record and one completion.
6. Add the replay set and the flags of AC4 with ReplayCheck and SyntheticGuardCheck: the pinned version after "RES-2027.01" takes effect, the flag off and on, and the no-live-case guard.
7. Replace each fake with the real service as its I story lands, then publish the run report per business date and the pass or fail gate agreed with QA; the gate definition: Not specified in the source documents (GAP-0422; ASM-0597).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.p3.temporal` from the legacy solution plan: with the flag off no worker polls `rwb-case`, the reference workflow is not registered and the relay does not run, so the case-topic deliveries stay PENDING; the harness asserts the disabled and the enabled state.

**Done when:** the journey runs green against the two deployed I stories in SIT, a recorded reference history replays with the same version, the same activity path and the same state move, the run report for the business date holds every assertion of §7 and §16 with its trace, SIT shows no live case read or written by the skeleton, and the pass or fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record write fails on every attempt | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-036 | The Temporal frontend is unreachable at signal time | The workflow service is not available. Try again in a few minutes. |
| MSG-P3-027 | No package is in force at evaluation time (NoPackageInForce) | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-009 | The decision record is refused for a missing field | The decision record was refused: {field} is missing or not valid. |

The harness asserts the message ID and the substituted values, including "ruleVersion" in MSG-P7-009; it does not own the message text. MSG-P3-027 is not retried, so the workflow fails at once. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| Temporal Web UI, workflow history | Running | The signal and the activity attempts of the run are visible, with the attempt count of a failed activity |
| Temporal Web UI, workflow history | Completed or failed | The three activities in order, the completion or the failure of the run, and the message the failure carries |
| Temporal Web UI, payload panel | Encoded | The payloads are encrypted and readable only through the platform codec server; the harness holds no clear payload |

The harness opens no Workbench screen and renders no page; it asserts the history the platform shows. SCR-44 Interface and job monitor is not used. Screen-level behaviour remains with the owning APP stories, and the harness environment and evidence detail: Not specified in the source documents (GAP-0422; ASM-0597).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-043-01-ITG | AC1, BR1, BR2; ITG AC1 | Integration | Case event EV-CASE-0777-01, rule R-RES-04, RES-2026.12, one record and one state move |
| TC-E2-043-02-ITG | AC2, BR2, BR8, BR9; ITG AC2 | Integration | Decision record store unavailable, refused record for a missing rule version, NoPackageInForce |
| TC-E2-043-03-ITG | AC3, BR3; ITG AC3 | NFR | ApplyStateActivity timeout after commit, key CASE_EVENT:EV-CASE-0777-03 |
| TC-E2-043-04-ITG | AC4, BR4; ITG AC4 | Integration | Replay on 2027-01-05 with RES-2027.01 in force |
| TC-E2-043-05-ITG | AC5, BR6; ITG AC1 | Integration | Temporal frontend unreachable, then available; event EV-CASE-0777-05 kept on the topic |
| TC-E2-043-06-ITG | AC6, BR7; ITG AC4 | Integration | Flag off, then on with the synthetic case |
| TC-E2-043-07-ITG | AC6, AC7, BR7, BR8; ITG AC1, ITG AC4 | Component | Worker registration on the task queue rwb-case with the flag off and on; no live case read or written |

The Covers column names the legacy AC of RWB-E2-043 that the ITG copy is derived from and the criterion of §7 it asserts at integration level. The Level column maps the legacy System level to Integration, the legacy Resilience level to NFR and the legacy Operational level to Component. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the rule ID, the package versions, the route states and the event types are data held by rwb-decision and rwb-case; the harness reads them and never holds a copy.
- No personal data in logs, tests, workflow history or reports: the payloads are encrypted by the platform codec, the synthetic case carries no customer data, and no clear personal data field is written to a run report.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services, the topics and their fakes, never a production endpoint, and it never opens a live case.
- Deterministic workflow code: no clock, random or I/O in workflow code, and every call to the evaluator, the record writer or the case state service is in an activity.
- No record, no state: the harness fails the run when a state row is written without its decision record, or when a failed record write still moves the route state.
- One row per key: IdempotencyCheck fails the run when a retry or a duplicate event adds a second state row, a second record or a second completion.
- The version is pinned: ReplayCheck fails the run when a replay calls the evaluator again or when a recorded result loses the version chosen at evaluation time.
- The skeleton is test-only: SyntheticGuardCheck fails the run when the flag is off and the workflow runs, when the synthetic flag is false, or when a workflow ID leaves the `ref-case-` prefix.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision is recorded with the rule and the version that made it | Business Requirements Epic 2, section 3.2; Program, section 5.7 | FEAT-DRI-07 | All recovery processes | R-RES-04; R-UNI-38 | TC-E2-043-01-ITG, TC-E2-043-02-ITG, TC-E2-043-04-ITG |
| REQ-DRI-005 | No action proceeds if its decision record cannot be written | Business Requirements Epic 2, section 3.2; Program, section 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-39 | TC-E2-043-02-ITG, TC-E2-043-03-ITG |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it | Business Requirements Epic 2, section 3.2; Program, section 5.3 | FEAT-DRI-07 | All recovery processes | R-RES-04; R-UNI-40 | TC-E2-043-01-ITG, TC-E2-043-04-ITG, TC-E2-043-06-ITG |
| REQ-DRI-007 | Every outbound item is logged and retried on a defined schedule, and a failure becomes an exception with an owner | Business Requirements Epic 2, section 3.2; Program, section 5.2 | FEAT-DRI-07 | All recovery processes | RWB-TE-006 | TC-E2-043-05-ITG, TC-E2-043-07-ITG |

The requirement IDs and their BRD sections are those of the legacy story; this story adds no requirement ID of its own. REQ-DRI-007 carries the outbox and retry behaviour of BR6 at the integration level, and TC-E2-043-02-ITG carries the non-retryable NoPackageInForce rule of BR8.

### 19. Out of scope

- The two owning I stories RWB-P3-E2043-APP and RWB-P7-E2043-APP, the real reference workflow build, its three activities and every endpoint, table, workflow and schedule they build.
- Production code in any service: the harness is test and evidence only.
- The worker, the payload codec, the gateway and the smoke workflow (RWB-E1-071) and the platform Temporal cluster.
- Rule package authoring and approval (RWB-E1-073) and the Epic 2 package content (RWB-E2-042).
- Workflow versioning, Worker Versioning and the replay gate (RWB-E2-040).
- The Temporal platform, its observability and its disaster recovery (RWB-E1-070, RWB-E2-037, RWB-E2-039), and the codec server, the payload guard and the administrative audit (RWB-PLT-E2038-APP).
- The case lifecycle, the case state model and the production case workflows of Epic 3, and the `case-{caseId}` workflow IDs they use.
- Any production code, table, workflow, schedule, endpoint or screen.
