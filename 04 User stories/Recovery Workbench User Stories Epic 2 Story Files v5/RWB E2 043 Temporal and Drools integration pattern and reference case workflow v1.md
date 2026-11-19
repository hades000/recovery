# RWB-E2-043 Temporal and Drools integration pattern and reference case workflow

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-043 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-DRI-07 Run the Drools evaluator on versioned rule packages |
| Requirement IDs | REQ-DRI-001, REQ-DRI-005, REQ-CWC-016 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, sections 5.2 and 5.7 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1, T2, T7); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-071, RWB-E1-072, RWB-TE-006 |
| Status | Ready for build |

## 1. Story

As a **developer**, I want **a reference case-workflow skeleton that shows signal handling, rule evaluation in an activity, the decision log before the action, state rows updated by an activity and outbound work through the outbox**, so that **Epic 3 builds every case workflow the same way**.

## 2. Business rationale

Epic 3 will add a workflow per case, and each squad would otherwise invent its own order of steps. A workflow that applies a state change before its decision log entry breaks Principle 5, and a workflow that calls Drools outside an activity breaks replay. This story fixes both in one small skeleton: the signal arrives, the rule is evaluated in an activity, the decision log entry is written in its own activity, the state is applied in a third, and a failure at any step stops the next. It is test-only and runs with no live case, so Epic 3 can copy it without a production risk. It meets REQ-DRI-001, REQ-DRI-005 and REQ-CWC-016. The measure is that every Epic 3 workflow is a copy of the skeleton and passes the replay gate of RWB-E2-040.

## 3. Preconditions

- RWB-E1-071 is done: the worker on `rwb-platform`, PdpaPayloadCodec, WorkflowGateway, PlatformSmokeWorkflow and the boundary test.
- RWB-E1-072 is done: `RuleEvaluator.evaluate`, `RuleResult` with `packageVersion` and `RuleCatalog.row`.
- RWB-TE-006 is done: `outbox_event`, `outbox_delivery` and the JOB-11 sender step.
- RWB-E1-027 is done: `DecisionLogWriter.write` runs in the caller's transaction with an idempotency key.
- Package RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01, with R-RES-04 moving IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER.
- The synthetic case "RW-2026-000777" exists in the DEV and SIT test data and is marked synthetic; no live case is used.
- The Temporal server and Java SDK versions approved by SCB IT are pinned in Environment and Deployment Design v4.
- Feature flag `rwb.p3.temporal` is on in DEV and SIT; `rwb.p3.drools` is on.

## 4. Flow

1. Test harness: starts ReferenceCaseWorkflow with workflow ID "ref-case-RW-2026-000777" on task queue `rwb-platform`, with the synthetic case and the reference package code.
2. Workflow: waits for the CaseEvent signal; no activity runs before it.
3. CaseEventSignalRelay: reads the outbox event "EV-CASE-0777-01" and calls `WorkflowGateway.signal(workflowId, "CaseEvent", payload)`.
4. Workflow: calls EvaluateRulesActivity with the package code, the case facts and the business date; the activity calls `RuleEvaluator.evaluate` and returns `RuleResult` with the rule ID, the package version and the outputs.
5. Workflow: calls WriteDecisionLogActivity with the event key; the activity calls `DecisionLogWriter.write` in its own transaction and returns the entry reference.
6. Workflow: only after a successful entry calls ApplyStateActivity with the same key; the activity calls the P3 case state service and writes one state row.
7. Workflow: completes. A failed decision log write leaves the state untouched, fails the workflow with MSG-P7-003 and raises an incident.
8. Platform administrator: reads the run in the Temporal Web UI; internal audit reads the same history and sees encrypted payloads only.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision log write fails | The state activity is not called; the workflow fails after its retries; an incident | MSG-P7-003 | AC2 |
| X2 | Temporal is unavailable when the signal is sent | The signal fails; the outbox event and its delivery stay for the next attempt | MSG-P3-036 | AC5 |
| X3 | An activity commits and then times out before it returns | The retry uses the same idempotency key and finds the first row | None | AC3 |
| X4 | A new package version is in force while the workflow waits | The recorded activity result keeps the version chosen at evaluation time; replay takes the same path | None | AC4 |
| X5 | `rwb.p3.temporal` is off | No worker and no reference workflow; nothing runs | None | AC6 |
| X6 | A second CaseEvent arrives while the first is processing | Temporal buffers it and the first path completes in signal order | None | AC1 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the worker of RWB-E1-071, the evaluator of RWB-E1-072 and the outbox of RWB-TE-006; it adds one test-only workflow and three activities |
| Negotiable | Retry values are configuration; the step order is fixed |
| Valuable | Epic 3 copies one proven order instead of inventing one per workflow |
| Estimable | One workflow, three activities, one signal record, one relay, one retry policy |
| Small | Fits one sprint with its tests |
| Testable | Each criterion runs with TestWorkflowEnvironment time skipping and a synthetic case |

## 7. Acceptance criteria

```gherkin
Feature: Temporal and Drools integration pattern and reference case workflow

  Background:
    Given the environment is SIT with synthetic data and no live case
    Given rwb.p3.temporal is on and the worker polls "rwb-platform"
    Given RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01
    Given rule R-RES-04 moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER
    Given the synthetic case "RW-2026-000777" has status IN_PROGRESS and route state IN_FCR_QUEUE

  Scenario: AC1 The four steps run in order
    Given the reference workflow "ref-case-RW-2026-000777" is running and waits for a CaseEvent
    Given outbox event "EV-CASE-0777-01" of type CASE_PICKED_UP
    When CaseEventSignalRelay calls WorkflowGateway.signal with "CaseEvent" and the event payload
    Then the workflow history shows EvaluateRulesActivity, then WriteDecisionLogActivity, then ApplyStateActivity
    Then EvaluateRulesActivity returns rule "R-RES-04" and package version "RES-2026.12"
    Then WriteDecisionLogActivity writes one entry with rule "R-RES-04" and rule version "RES-2026.12"
    Then ApplyStateActivity moves the route state to "WITH_FCR_OFFICER"
    Then no case row is written before the decision log entry

  Scenario: AC2 A failed decision log write stops the state change
    Given the decision log store is unavailable
    When the CaseEvent "EV-CASE-0777-02" is processed
    Then WriteDecisionLogActivity throws DecisionLogUnavailableException
    Then the workflow does not call ApplyStateActivity
    Then the route state of "RW-2026-000777" stays "IN_FCR_QUEUE"
    Then the workflow fails with MSG-P7-003 after its retries and an incident is raised

  Scenario: AC3 Activity retries are idempotent
    Given ApplyStateActivity commits the state row and then times out before it returns
    When Temporal retries the activity with idempotency key "CASE_EVENT:EV-CASE-0777-03"
    Then the second attempt returns the first result and changes nothing
    Then one case state row exists for "EV-CASE-0777-03"
    Then WriteDecisionLogActivity ran once and one decision_log_entry row exists with that key
    Then the workflow completes once

  Scenario: AC4 The rule version is pinned in the result and replay is stable
    Given EvaluateRulesActivity returned package version "RES-2026.12" and rule "R-RES-04" for "EV-CASE-0777-04"
    Given package version "RES-2027.01" is in force from 2027-01-01 while the workflow waits for the next event
    When the workflow is replayed from its recorded history on 2027-01-05
    Then the recorded result still carries "RES-2026.12" and "R-RES-04"
    Then the replay reads the recorded activity result and never calls RuleEvaluator again
    Then the replay reaches the same activity path and the same state move

  Scenario: AC5 Temporal unavailable keeps the case event in the outbox
    Given the Temporal frontend is unreachable
    When the outbox sender delivers "EV-CASE-0777-05"
    Then WorkflowGateway.signal fails with MSG-P3-036
    Then outbox event "EV-CASE-0777-05" stays in the outbox and its delivery is RETRYING with the next attempt time
    Then the sender retries on its schedule
    When Temporal is available at the next attempt
    Then the signal is delivered and the delivery is DELIVERED

  Scenario: AC6 The skeleton runs behind the flag with no live case
    Given rwb.p3.temporal is off in DEV
    When the application starts
    Then no worker is registered on "rwb-platform" and ReferenceCaseWorkflow is not deployed
    When the flag is on and the reference harness starts "ref-case-RW-2026-000777" with synthetic "true"
    Then the skeleton runs the four steps with no live case
    Then no recovery_case row outside the synthetic fixture is read or written
    Then the workflow ID starts "ref-case-" and never "case-"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code is deterministic: no clock, random or I/O; Drools is called only inside EvaluateRulesActivity | D-RCV-36 T7; ADR-011 |
| BR2 | The order is signal, evaluate, decision log, state; no state row is written without its decision log entry | REQ-DRI-005; Principle 5; R-UNI-39 |
| BR3 | Every activity is idempotent by the event idempotency key; a retry gives one row | REQ-DRI-005; R-UNI-40 |
| BR4 | The package version is chosen at evaluation time, pinned in RuleResult and written to the decision log; replay uses the recorded result | D-RCV-36 T7; R-UNI-38 |
| BR5 | Payloads are encrypted by PdpaPayloadCodec; history and logs hold references and codes only | D-RCV-36 T1; NFR-034 |
| BR6 | When Temporal is unavailable the signal fails with MSG-P3-036 and the outbox event stays for retry | REQ-DRI-007; RWB-TE-006 |
| BR7 | The reference skeleton is test-only: it runs only under `rwb.p3.temporal` and only with a synthetic case | D-RCV-36 T1; ADR-011 |
| BR8 | Retry policy: initial interval 1s, backoff 2, max attempts 10; NoPackageInForce is non-retryable | D-RCV-36 T1, T7 |
| BR9 | State change goes through ApplyStateActivity and the P3 case state service; no direct table write | REQ-DRI-005; D-RCV-36 T1 |

## 9. State transitions

This story changes no live case. It writes the route state of the synthetic fixture through the P3 service and moves the workflow through its own states.

| From | Event | Condition | To |
|---|---|---|---|
| RUNNING | CaseEvent | Evaluate, log and apply all succeed | COMPLETED |
| RUNNING | CaseEvent | Decision log write fails after 10 attempts | FAILED |
| RUNNING | CaseEvent | NoPackageInForce | FAILED, no retry |
| IN_FCR_QUEUE | CASE_PICKED_UP | R-RES-04 fires | WITH_FCR_OFFICER |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs ReferenceCaseWorkflow and its three activities |
| SY-RULES, Drools evaluator | Evaluates the package inside EvaluateRulesActivity |
| SY-DECLOG, decision log writer | Writes the entry inside WriteDecisionLogActivity |
| RW-PLATADM, platform administrator | Runs the worker and reads the Temporal Web UI (Platform administration CRUD) |
| RW-AUDIT, internal audit | Reads the recorded history with encrypted payloads (Platform administration R) |
| RW-COE, center of excellence analyst | Owns the RESTRUCTURE version used by the reference |
| No delegation of authority level applies | The skeleton takes no credit decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P7 writer |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, read |
| DF-OPS-189 to DF-OPS-197 | outbox_event | all fields | Read, by the relay |
| DF-OPS-198 to DF-OPS-206 | outbox_delivery | all fields | Read and write status, through RWB-TE-006 |
| DF-CAS-001 | recovery_case | id | Read, synthetic fixture only |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Write, through the P3 case state service |

Field IDs are those in the Logical Data Model and Data Dictionary. The skeleton writes no table of its own and no new field. The fixture row is inserted by the test harness in DEV and SIT only and removed after the test.

## 12. Contract

**No Workbench endpoint.** The skeleton is started by the reference test harness in DEV and SIT only; it has no REST path, no schedule and no admin operation.

**Workflow interface** (package `recovery.casewf.workflow.reference`)

```java
@WorkflowInterface
public interface ReferenceCaseWorkflow {
    @WorkflowMethod void run(ReferenceCaseInput input);
    @SignalMethod void onCaseEvent(CaseEventSignal event);
}
// ReferenceCaseInput: caseId, packageCode, businessDate, synthetic (true only)
// CaseEventSignal: eventId, caseId, eventType, occurredAt, idempotencyKey, synthetic
```

**Activities** (package `recovery.casewf.workflow.reference.activities`)

```java
RuleResult EvaluateRulesActivity.evaluate(String packageCode, CaseFacts facts, LocalDate onDate);
DecisionLogRef WriteDecisionLogActivity.write(DecisionLogRequest request);   // throws DecisionLogUnavailableException
void ApplyStateActivity.apply(CaseStateChange change, String idempotencyKey); // returns the first result when the key exists
```

**Signal path.** `CaseEventSignalRelay` implements the RWB-TE-006 `OutboxConsumer` for the case event types and calls `WorkflowGateway.signal(workflowId, "CaseEvent", payload)` from RWB-E1-071. A failed call returns FAILED and leaves the delivery for the next attempt.

**Retry policy**

| Item | Value |
|---|---|
| Initial interval | 1 second |
| Backoff coefficient | 2 |
| Maximum attempts | 10 |
| Non-retryable | NoPackageInForce |
| Applies to | EvaluateRulesActivity, WriteDecisionLogActivity, ApplyStateActivity |

**Published interfaces called**

```java
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate);  // P3
RuleRow RuleCatalog.row(String ruleId, String packageVersion);                          // P3
DecisionLogRef DecisionLogWriter.write(DecisionLogRecord record);                       // P7
void WorkflowGateway.signal(String workflowId, String signal, Object payload);           // P3
```

No events are published by the skeleton; the outbox events it reads belong to RWB-TE-006.

## 13. Solution plan

**Package.** `recovery.casewf.workflow.reference` and `.activities`; the relay in `recovery.integration.outbox.reference`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReferenceCaseWorkflow | Workflow (test-only scope) | Waits for CaseEvent, calls the three activities in order, completes |
| EvaluateRulesActivity | Activity | Calls RuleEvaluator and returns RuleResult; reads no case row and writes none |
| WriteDecisionLogActivity | Activity | Calls DecisionLogWriter in its own transaction and returns the entry reference |
| ApplyStateActivity | Activity | Calls the P3 case state service with the idempotency key; one state row |
| CaseEventSignal | Record | eventId, caseId, eventType, occurredAt, idempotencyKey, synthetic |
| CaseEventSignalRelay | Outbox consumer | Reads the delivery, signals the workflow, leaves the event on failure |
| ActivityRetryPolicies | Configuration | Initial 1s, backoff 2, max attempts 10, non-retryable NoPackageInForce |
| ReferenceCaseFixture | Test fixture | Synthetic case row and RESTRUCTURE version for DEV and SIT |
| ReferenceCaseWorkflowTest | Test | Time-skipping, signal order, failure and replay tests |
| No controller | - | The skeleton has no endpoint |

**Database.** No migration and no new table. The skeleton writes `decision_log_entry` through RWB-E1-027 and the case route state through the P3 case state service. The fixture is a JSON seed in the test resources; it is inserted and removed by the harness.

**Configuration and reference data**

- Task queue `rwb-platform` and workflow ID prefix `ref-case-` for the skeleton; Epic 3 case workflows use `rwb-case` and `case-{caseId}`.
- Retry values of section 12 (assumed; confirmed with DL11).
- `rwb.p3.temporal` and `rwb.p3.drools` flags.
- The RESTRUCTURE version is owned by RW-COE.

**Build steps**

1. Define ReferenceCaseWorkflow, ReferenceCaseInput and CaseEventSignal; test that no activity runs before the signal (AC1).
2. Build EvaluateRulesActivity against RuleEvaluator; test the rule ID and package version in the result (AC1, AC4).
3. Build WriteDecisionLogActivity; test the refusal when the store is down (AC2).
4. Build ApplyStateActivity with the idempotency key; test the timeout after commit and the retry (AC3).
5. Add ActivityRetryPolicies and the NoPackageInForce do-not-retry rule; test the failure path (AC2).
6. Build CaseEventSignalRelay and test the Temporal-unavailable path with the outbox (AC5).
7. Add the flag checks and the synthetic guard; test AC6 and the worker registration.
8. Add the replay test with a recorded history and a later package version (AC4).

**Feature flag.** `rwb.p3.temporal`. Off: no worker on `rwb-platform`, ReferenceCaseWorkflow is not deployed and the relay does not run; outbox deliveries stay PENDING. Nothing else changes.

**Done when.** The tests in section 16 pass, a recorded reference history replays with the same path, and SIT shows no live case read or written by the skeleton.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-036 | The Temporal frontend is unreachable at signal time | The workflow service is not available. Try again in a few minutes. |
| MSG-P7-003 | The decision log write fails | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No package is in force at evaluation time (NoPackageInForce) | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-009 | The decision record is refused for a missing field | The decision record was refused: {field} is missing or not valid. |

MSG-P3-027 is not retried by ActivityRetryPolicies; the workflow fails at once. Thai text for each message follows DL10.

## 15. Screens and states

No screen in this story. The reference workflow is read in the Temporal Web UI by RW-PLATADM and RW-AUDIT, by workflow ID "ref-case-RW-2026-000777"; payloads are decoded only through the codec server (RWB-E2-038). The workflow states RUNNING, COMPLETED and FAILED and the activity attempt count are shown there. SCR-44 Interface and job monitor is not used.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-043-01 | AC1, BR1, BR2 | System | Signal EV-CASE-0777-01, R-RES-04, RES-2026.12 |
| TC-E2-043-02 | AC2, BR2, BR9 | System | Decision log store unavailable |
| TC-E2-043-03 | AC3, BR3 | Resilience | ApplyStateActivity timeout after commit, key CASE_EVENT:EV-CASE-0777-03 |
| TC-E2-043-04 | AC4, BR4 | System | Replay on 2027-01-05 with RES-2027.01 in force |
| TC-E2-043-05 | AC5, BR6 | System | Temporal frontend unreachable, then available |
| TC-E2-043-06 | AC6, BR7 | System | Flag off, then on with a synthetic case |
| TC-E2-043-07 | AC6, BR7, BR8 | Operational | Worker registration and task queue rwb-platform with the flag off and on; no live case |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. Action text, owner role and timer come from rule packages; retry values are configuration.
- No personal data in logs, tests, workflow history or prompts. Payloads are encrypted by PdpaPayloadCodec and the reference case is synthetic.
- No read of another module's tables; ACE data only through recovery.v_ace_* views.
- Workflow code is deterministic: no clock, random or I/O; every call to Drools, the decision log or the case service is in an activity.
- The decision log entry is written before the state change; no state row without its entry.
- Every activity is idempotent by the event key; a retry never writes a second row.
- The skeleton is test-only: it never runs against a live case and never writes a non-synthetic case row.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision is recorded with the rule and version that made it | Epic 2, 3.2; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-RES-04; R-UNI-38 | TC-E2-043-01, TC-E2-043-04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Epic 2, 3.2; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-39 | TC-E2-043-02, TC-E2-043-03 |
| REQ-CWC-016 | Rules are evaluated by Drools from a versioned package | Epic 2, 3.2; Program, 5.3 | FEAT-DRI-07 | All recovery processes | R-RES-04 | TC-E2-043-01, TC-E2-043-04, TC-E2-043-05 |

## 19. Out of scope

- The case workflows, their timers and their outbound chains (Epic 3).
- Workflow versioning and the replay test gate (RWB-E2-040).
- The worker, the payload codec and the smoke workflow (RWB-E1-071).
- Rule package authoring and approval (RWB-E1-073); the Epic 2 package content (RWB-E2-042).
- The outbox sender schedule and the consumer list (RWB-TE-006).
- The Temporal platform, its observability and its DR (RWB-E1-070, RWB-E2-037, RWB-E2-039).
- The case lifecycle and the full state model (Epic 3).
