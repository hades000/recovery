# RWB-P3-E2043-APP Temporal and Drools integration pattern and reference case workflow

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2043-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-043 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP14, DP15, DP19 |
| Parallel lane | L-P3-AR |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P3-E2043-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | RWB-P3-E2043-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-043 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **developer**, I want **a test-only reference case workflow that runs on task queue `rwb-case` in namespace `rwb-recovery` and shows signal handling, rule evaluation inside one activity, the decision record and the state change written together by a second activity, and outbound work through the outbox**, so that **Epic 3 builds every case workflow the same way**.

### 2. Business rationale

Epic 3 adds a workflow per case, and each squad would otherwise invent its own order of steps. A workflow that applies a state change before its decision record breaks the decision-first principle (R-UNI-39), and a workflow that calls Drools outside an activity breaks replay. This story fixes both in one small skeleton: the signal arrives through the outbox consumer, the rule is evaluated in an activity, the decision record and the state change are written together by a second activity, and a failure at either step stops the next. It is test-only and runs with no live case, so Epic 3 can copy it without a production risk. It meets REQ-DRI-001, REQ-DRI-005, REQ-CWC-016 and REQ-DRI-007.

In the target the two concerns are the local decision record and the central ledger (DP-03): the owning service writes the record in its own schema in the same transaction as the state change and publishes DecisionRecorded on `rwb.decision-record.v1`, and rwb-decision collects it into the central ledger within five minutes (Arch v5 slide 28). The Temporal and Drools design merges the legacy WriteDecisionLog and ApplyState steps into one RecordAndApply activity for exactly that reason (design slide 14), so this skeleton has two activities where the legacy story had three, and the order evaluate, record, apply is unchanged.

The skeleton is also the carrier of the platform rules that make a workflow safe to replay: deterministic workflow code, worker versioning with `getVersion` for an in-place change, encrypted payloads through PdpaPayloadCodec, and the replay gate of RWB-E2-040 that replays recorded histories against every new build (design slide 27). The measure is that every Epic 3 workflow is a copy of the skeleton and passes that gate.

The skeleton has no screen, no endpoint and no composite route, so gateway-bff (DP-19) is not used by it; the dependency on RWB-PLT-N001-CON is carried only because the service template registers the route of rwb-case.

### 3. Preconditions

- RWB-P3-E2043-CON is published: the workflow interface, the two activity interfaces, the CaseEvent signal schema, the ReferenceCaseInput record and the retry policy of this legacy key.
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, with the task queue `rwb-case`, the worker configuration and the build ID provider.
- RWB-PLT-E1072-CON is published: the embedded Drools kit with one KieBase per package version, first-match semantics and the `NoPackageInForce` outcome (DP-04).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). The central ledger behind it belongs to rwb-decision (P7) and is not written by this story.
- RWB-PLT-TE006-CON is published: the outbox and inbox library with the CloudEvents envelope and the `OutboxConsumer` interface the relay implements (DP-09).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case, with the client library (DP-07). RWB-PLT-E1047-CON is published: the topic and event naming library (DP-14). RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route of the service template. This skeleton declares no route on it.
- Package RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01, with rule R-RES-04 moving IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER; the package is governed and served by rwb-decision and is answered in this story by the rwb-decision contract mock.
- The synthetic case "RW-2026-000777" exists in the DEV and SIT test data and is marked synthetic; no live case is used. The fixture that seeds and removes it is Not specified in the source documents (GAP-0724; ASM-1272).
- The Temporal server and Java SDK versions approved by SCB IT are pinned by the platform, not by this story (RWB-PLT-E1071-CON).
- Feature switch `rwb.p3.temporal` is on in DEV and SIT; `rwb.p3.drools` is on. The switch is read through the platform parameters contract, never from code.

### 4. Flow

1. Reference harness: starts ReferenceCaseWorkflow with workflow ID "ref-case-RW-2026-000777" on task queue `rwb-case` in namespace `rwb-recovery`, with the synthetic case, the reference package code and the business date, and with synthetic true.
2. Workflow: waits for the CaseEvent signal; no activity runs before it.
3. CaseEventSignalRelay: reads the outbox delivery "EV-CASE-0777-01" of type CASE_PICKED_UP and calls `WorkflowGateway.signal(workflowId, "CaseEvent", payload)`; a failed call leaves the delivery PENDING or RETRYING for the next attempt (DP-09).
4. Workflow: calls EvaluateRulesActivity with the package code, the case facts and the business date; the activity calls `RuleEvaluator.evaluate` and returns `RuleResult` with the package code, the package version, the rule ID and the outputs.
5. Workflow: calls RecordAndApplyActivity with the event key; the activity writes, in one transaction in schema rwb_case, the decision record through the local decision-record library and the state change through the P3 case state service, plus the outbox row of DecisionRecorded.
6. Workflow: completes. A failed write leaves the state untouched because nothing committed, fails the workflow with MSG-P7-003 after its retries and raises an incident; the stuck-workflow scan of the platform (JOB-21) reports a workflow that waits on a non-retryable failure.
7. Workflow: a second CaseEvent that arrives while the first is processing is buffered by Temporal and handled in signal order.
8. Platform administrator: reads the run in the Temporal Web UI; internal audit reads the same history and sees encrypted payloads and references only.
9. Epic 3 squad: copies the workflow, the two activity interfaces and the retry policy, replaces the synthetic fixture with the real case, and keeps the order.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record write fails | The state change does not commit either, because both are one transaction; the workflow fails after its retries and an incident is raised | MSG-P7-003 | AC2 |
| X2 | Temporal is unavailable when the signal is sent | The signal fails; the outbox event and its delivery stay for the next attempt | MSG-P3-036 | AC5 |
| X3 | The RecordAndApply activity commits and then times out before it returns | The retry uses the same idempotency key and finds the first record and the first state row | None | AC3 |
| X4 | A new package version is in force while the workflow waits | The recorded activity result keeps the version chosen at evaluation time; replay takes the same path | None | AC4 |
| X5 | `rwb.p3.temporal` is off | No worker on `rwb-case`, no reference workflow deployed and the relay idle; outbox deliveries stay PENDING | None | AC6 |
| X6 | A second CaseEvent arrives while the first is processing | Temporal buffers it and the first path completes in signal order | None | AC1 |
| X7 | No package version is in force at evaluation time | EvaluateRulesActivity fails with NoPackageInForce; the policy does not retry and the workflow fails at once | MSG-P3-027 | AC4 |
| X8 | A non-synthetic case ID is passed as the workflow input | The workflow refuses to run and fails before any activity; nothing is read or written | None | AC6 |
| X9 | The reference data read of the case status list fails | RecordAndApplyActivity is not called; the workflow retries the evaluation step only, never a partial record | MSG-P3-027 | AC1, AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the workflow kit of RWB-PLT-E1071-CON, the evaluator of RWB-PLT-E1072-CON, the record library of RWB-PLT-E1027-CON and the outbox of RWB-PLT-TE006-CON; it adds one test-only workflow, two activities and one relay |
| Negotiable | Retry values are configuration; the order of the two steps is fixed |
| Valuable | Epic 3 copies one proven order instead of inventing one per workflow |
| Estimable | One workflow, two activities, one signal record, one input record, one relay, one retry policy |
| Small | Fits one sprint with its tests |
| Testable | Each criterion runs with TestWorkflowEnvironment time skipping and the synthetic case; no WireMock is needed because no REST call is made |

### 7. Acceptance criteria

```gherkin
Feature: Temporal and Drools integration pattern and reference case workflow

  Background:
    Given the environment is SIT with synthetic data and no live case
    Given rwb.p3.temporal is on and the worker polls "rwb-case"
    Given the rwb-decision contract mock returns package "RESTRUCTURE" version "RES-2026.12" and rule "R-RES-04"
    Given RESTRUCTURE version "RES-2026.12" is in force from 2026-12-01
    Given rule R-RES-04 moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER
    Given the synthetic case "RW-2026-000777" has status IN_PROGRESS and route state IN_FCR_QUEUE

  Scenario: AC1 The four steps run in order (legacy RWB-E2-043 AC1)
    Given the rwb-decision contract mock returns package "RESTRUCTURE" version "RES-2026.12" and rule "R-RES-04"
    Given the reference workflow "ref-case-RW-2026-000777" is running and waits for a CaseEvent
    Given outbox event "EV-CASE-0777-01" of type CASE_PICKED_UP
    When CaseEventSignalRelay calls WorkflowGateway.signal with "CaseEvent" and the event payload
    Then the workflow history shows EvaluateRulesActivity, then WriteDecisionLogActivity, then ApplyStateActivity
    Then EvaluateRulesActivity returns rule "R-RES-04" and package version "RES-2026.12"
    Then WriteDecisionLogActivity writes one entry with rule "R-RES-04" and rule version "RES-2026.12"
    Then ApplyStateActivity moves the route state to "WITH_FCR_OFFICER"
    Then no case row is written before the decision log entry

  Scenario: AC2 A failed decision log write stops the state change (legacy RWB-E2-043 AC2)
    Given the rwb-decision contract mock returns package "RESTRUCTURE" version "RES-2026.12" and rule "R-RES-04"
    Given the decision log store is unavailable
    When the CaseEvent "EV-CASE-0777-02" is processed
    Then WriteDecisionLogActivity throws DecisionLogUnavailableException
    Then the workflow does not call ApplyStateActivity
    Then the route state of "RW-2026-000777" stays "IN_FCR_QUEUE"
    Then the workflow fails with MSG-P7-003 after its retries and an incident is raised

  Scenario: AC3 Activity retries are idempotent (legacy RWB-E2-043 AC3)
    Given ApplyStateActivity commits the state row and then times out before it returns
    When Temporal retries the activity with idempotency key "CASE_EVENT:EV-CASE-0777-03"
    Then the second attempt returns the first result and changes nothing
    Then one case state row exists for "EV-CASE-0777-03"
    Then WriteDecisionLogActivity ran once and one decision_log_entry row exists with that key
    Then the workflow completes once

  Scenario: AC4 The rule version is pinned in the result and replay is stable (legacy RWB-E2-043 AC4)
    Given EvaluateRulesActivity returned package version "RES-2026.12" and rule "R-RES-04" for "EV-CASE-0777-04"
    Given the rwb-decision contract mock returns package "RESTRUCTURE" version "RES-2027.01"
    Given package version "RES-2027.01" is in force from 2027-01-01 while the workflow waits for the next event
    When the workflow is replayed from its recorded history on 2027-01-05
    Then the recorded result still carries "RES-2026.12" and "R-RES-04"
    Then the replay reads the recorded activity result and never calls RuleEvaluator again
    Then the replay reaches the same activity path and the same state move

  Scenario: AC5 Temporal unavailable keeps the case event in the outbox (legacy RWB-E2-043 AC5)
    Given the Temporal frontend is unreachable
    When the outbox sender delivers "EV-CASE-0777-05"
    Then WorkflowGateway.signal fails with MSG-P3-036
    Then outbox event "EV-CASE-0777-05" stays in the outbox and its delivery is RETRYING with the next attempt time
    Then the sender retries on its schedule
    When Temporal is available at the next attempt
    Then the signal is delivered and the delivery is DELIVERED

  Scenario: AC6 The skeleton runs behind the flag with no live case (legacy RWB-E2-043 AC6)
    Given rwb.p3.temporal is off in DEV
    When the application starts
    Then no worker is registered on "rwb-case" and ReferenceCaseWorkflow is not deployed
    When the flag is on and the reference harness starts "ref-case-RW-2026-000777" with synthetic "true"
    Then the skeleton runs the four steps with no live case
    Then no recovery_case row outside the synthetic fixture is read or written
    Then the workflow ID starts "ref-case-" and never "case-"
```

AC1 records the three legacy steps; in the target the same order is carried by two activities — EvaluateRulesActivity, then RecordAndApplyActivity, which writes the decision record and the state change in one transaction (Temporal and Drools design slide 14, DP-03) — so the recorded three steps are read as evaluate, record, apply. The target task queue is `rwb-case` in namespace `rwb-recovery`, because the queue belongs to the owning service (Arch v5 slides 24 and 41); the legacy queue `rwb-platform` is retired for this skeleton. A Given naming a package, a rule or a version in force is preceded by the parallel rwb-decision contract mock Given, because the registry is owned by rwb-decision and is answered by its fake in this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Workflow code is deterministic: no clock, random or I/O; Drools is called only inside EvaluateRulesActivity | Design slide 27; ADR-011; DP-04 |
| BR2 | The order is signal, evaluate, record and apply; no state row is written without its decision record, because both are one transaction | REQ-DRI-005; R-UNI-39; design slide 14; DP-03 |
| BR3 | Every activity is idempotent by the event idempotency key; a retry gives one record and one state row | REQ-DRI-005; R-UNI-40 |
| BR4 | The package version is chosen at evaluation time, pinned in RuleResult and written to the decision record; replay uses the recorded result | Design slides 15 and 27; R-UNI-38 |
| BR5 | Payloads are encrypted by PdpaPayloadCodec; history, search attributes and logs hold references and codes only | Design slide 27; NFR-034 |
| BR6 | When Temporal is unavailable the signal fails with MSG-P3-036 and the outbox event stays for retry | REQ-DRI-007; DP-09; RWB-PLT-TE006-CON |
| BR7 | The reference skeleton is test-only: it runs only under `rwb.p3.temporal` and only with a synthetic case, and its workflow ID starts `ref-case-` | Legacy RWB-E2-043 BR7; ASM-1272 |
| BR8 | Retry policy: initial interval 1 s, back-off 2, maximum 10 attempts; NoPackageInForce is non-retryable | Design slides 14 and 28 |
| BR9 | The state change goes through the P3 case state service inside RecordAndApplyActivity; the workflow writes no table and calls no repository | REQ-DRI-005; DP-01; design slide 11 |
| BR10 | The build passes the replay gate of RWB-E2-040 and the worker is versioned: a new build takes new workflows while the old build drains, and an in-place change uses `Workflow.getVersion` | Design slide 27; RWB-PLT-E1071-CON |
| BR11 | A reference-data or parameter value is read through the rwb-case contract with the version in force; no status, route or timer value is written in code | DP-07; Template and Rules §R7.2 s17 |
| BR12 | The skeleton calls no REST operation and declares no route on gateway-bff; its only remote call is WorkflowGateway to the Temporal frontend | DP-11; DP-19 note in section 2 |

### 9. State transitions

This story changes no live case. It writes the route state of the synthetic fixture through the P3 case state service and moves the workflow through its own states.

| From | Event | Condition | To |
|---|---|---|---|
| RUNNING | CaseEvent | Evaluate and record-and-apply both succeed | COMPLETED |
| RUNNING | CaseEvent | The record and the state change fail after 10 attempts | FAILED |
| RUNNING | CaseEvent | NoPackageInForce | FAILED, no retry |
| RUNNING | CaseEvent | The input is not synthetic | FAILED, no activity run |
| IN_FCR_QUEUE | CASE_PICKED_UP | R-RES-04 fires | WITH_FCR_OFFICER |

A FAILED workflow is reported by the stuck-workflow scan of the platform (JOB-21) and is visible in the Temporal Web UI; it is never retried by a later signal, because the signal has already been consumed.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow identity | Runs ReferenceCaseWorkflow on `rwb-case` in namespace `rwb-recovery` and registers its two activities |
| SY-RULES, Drools evaluator identity | Evaluates the package inside EvaluateRulesActivity (Rules and parameters R) |
| Decision-record library identity | Writes the local record and its outbox row in the same transaction as the state change (Decision log C) |
| RW-PLATADM, platform administrator | Runs the worker and reads the Temporal Web UI (Platform administration CRUD) |
| RW-AUDIT, internal audit | Reads the recorded history with encrypted payloads and references only (Platform administration R) |
| RW-COE, center of excellence analyst | Owns the RESTRUCTURE version used by the reference |
| No delegation of authority level applies | The skeleton takes no credit decision |

The worker runs as the rwb-case service identity (DP-02) and the chart carries it as a secret reference; the story fixes no literal login name.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | Local decision record (rwb_case) | all fields, through the local library | Write |
| DF-DEC-030 | Local decision record | actor_user_id | Write, the service identity only |
| DF-DEC-031 | Local decision record | idempotency_key | Write, read |
| DF-OPS-189 to DF-OPS-197 | outbox_event (rwb_case) | all fields | Read, by the relay |
| DF-OPS-198 to DF-OPS-206 | outbox_delivery (rwb_case) | all fields | Read, and write the status through RWB-PLT-TE006-CON |
| DF-CAS-001 | recovery_case | id | Read, synthetic fixture only |
| DF-CAS-005 | recovery_case | status | Read, through the P3 case state service |
| DF-CAS-007 | recovery_case | route_state | Write, through the P3 case state service |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-CASE-STATUS and LOV-ROUTE versions | Read, through the reference-data contract |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The skeleton writes no table of its own and no new field: the local decision record, the outbox, the inbox and the idempotency objects are library objects created in schema rwb_case by its own DB story (DP-09, DP-15). No row of `rwb_decision` and no central ledger row is written by this story; the central ledger is filled by rwb-decision from `rwb.decision-record.v1` and is the subject of RWB-P7-E2043-APP. The fixture row is inserted and removed by the harness in DEV and SIT only; the seed file and its owner are Not specified in the source documents (GAP-0724; ASM-1272).

### 12. Contract

#### 12.1 REST operations provided

None. The skeleton is started by the reference harness in DEV and SIT only; it declares no path under `/api/recovery/case/v1`, no admin operation and no health contract beyond the platform probes.

#### 12.2 REST operations consumed

None. The only remote call of the skeleton is `WorkflowGateway` to the Temporal frontend, which is a gRPC contract of the workflow kit (RWB-PLT-E1071-CON) and not a REST operation. The rule package and the reference data are read in-process through their published Java interfaces and the contract mocks of this story.

#### 12.3 Events published

None. The skeleton publishes no event of its own; DecisionRecorded on `rwb.decision-record.v1` is published by the local decision-record library through the outbox in the same transaction as the record and the state change (DP-03), and that event type belongs to P7.

#### 12.4 Events consumed

None at the Kafka level. The case event types of `rwb.case.events.v1` are read from the outbox delivery by `CaseEventSignalRelay`, which implements the `OutboxConsumer` interface of RWB-PLT-TE006-CON and turns each delivery into a CaseEvent signal; the event types and the ownership of the type stay with that contract, and this story consumes no topic of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| ReferenceCaseWorkflow | Workflow, test-only scope, workflow ID prefix `ref-case-` | `rwb-case` | Waits for the CaseEvent signal, calls EvaluateRules then RecordAndApply, completes |
| EvaluateRulesActivity | Activity | `rwb-case` | Calls `RuleEvaluator.evaluate(packageCode, facts, onDate)`, returns RuleResult |
| RecordAndApplyActivity | Activity | `rwb-case` | Writes the decision record and the state change in one transaction, idempotent by the event key |
| CaseEventSignalRelay | Outbox consumer | not a worker | Signals the workflow; a failed call leaves the delivery PENDING or RETRYING |

```java
@WorkflowInterface
public interface ReferenceCaseWorkflow {
    @WorkflowMethod void run(ReferenceCaseInput input);
    @SignalMethod void onCaseEvent(CaseEventSignal event);
}
// ReferenceCaseInput: caseId, packageCode, businessDate, synthetic (true only)
// CaseEventSignal: eventId, caseId, eventType, occurredAt, idempotencyKey, synthetic
```

```java
RuleResult EvaluateRulesActivity.evaluate(String packageCode, CaseFacts facts, LocalDate onDate);
RecordAndApplyResult RecordAndApplyActivity.apply(RecordAndApplyRequest request); // record + state + outbox, one transaction
```

**Retry policy**

| Item | Value |
|---|---|
| Initial interval | 1 second |
| Back-off coefficient | 2 |
| Maximum attempts | 10 |
| Non-retryable | NoPackageInForce |
| Applies to | EvaluateRulesActivity, RecordAndApplyActivity |

**Versioning.** Each worker carries the build ID of its build, so a new build takes new workflows while the old build drains; an in-place code change uses `Workflow.getVersion(changeId, DEFAULT_VERSION, 1)`; every build replays the recorded histories under the replay gate of RWB-E2-040 before release. The build ID format and the versioning policy are Not specified in the source documents (GAP-0725; ASM-1273).

**Called in-process, not over REST**

```java
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate);   // rwb-case, embedded kit
void WorkflowGateway.signal(String workflowId, String signal, Object payload);            // rwb-case, workflow kit
```

#### 12.6 Schedules

None. The reference workflow is started by the harness, never by a Schedule; the Schedules of rwb-case belong to their own stories (DP-10).

#### 12.7 Tables owned

None. The skeleton owns no table: it writes through the local decision-record library and the P3 case state service, both of which write schema rwb_case, and the outbox, inbox and idempotency objects are library objects of RWB-PLT-TE006-CON created in rwb_case. No table of another service is read or written (DP-01).

#### 12.8 Contract fakes

None. The workflow test uses TestWorkflowEnvironment with time skipping and the in-process contract mocks of the published interfaces; there is no WireMock mapping, because the skeleton calls no REST operation. The rwb-decision mock answers the package and rule facts named in the acceptance criteria.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | No path and no client; the harness starts the workflow |
| Kafka | 0 published by the workflow, 0 consumed | DecisionRecorded is published by the local library; case events arrive as a signal through the outbox relay |
| Temporal | 1 workflow, 2 activities, 0 Schedules | ReferenceCaseWorkflow, EvaluateRulesActivity, RecordAndApplyActivity on `rwb-case` |
| File | None | The synthetic fixture is a build input, not runtime data |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `workflow.reference`, Java package `th.co.scb.ace.workbench.recovery.case.workflow.reference` and `.activities`; the relay in `th.co.scb.ace.workbench.recovery.case.outbox.reference`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the skeleton writes through the case state service and the record library, never another service's table | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library in the same transaction, plus `rwb.decision-record.v1`; the two legacy activities merge into RecordAndApply | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit inside EvaluateRulesActivity; the package comes from rwb-decision as a model | H RWB-PLT-E1072-CON (the registry side is RWB-P7-E1073) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read in the skeleton: the facts come from the synthetic fixture; an Epic 3 copy reads ACE data through the rwb-source-data contract, never a view | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case for the case status and route lists with their versions | H RWB-PLT-E1043-CON; RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents envelope, the relay as an `OutboxConsumer` | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Durable timers and the workflow kit instead of Quartz; the skeleton starts no Schedule but uses the kit's queue, codec and build ID | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | No REST hop at all; the workflow reaches the rules and the state through activities and in-process interfaces | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | Topic `rwb.case.events.v1` and event names `rwb.case.<Event>.v1` through the naming library; the skeleton adds no topic | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | No migration of its own: the record, outbox and inbox objects arrive with the rwb_case baseline and its per-service Flyway sequence | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff is not used by this skeleton: no screen, no endpoint, no composite route; the dependency is carried by the service template only | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReferenceCaseWorkflow | Workflow (test-only scope) | Waits for CaseEvent, calls the two activities in order, completes; deterministic code only |
| EvaluateRulesActivity | Activity | Calls `RuleEvaluator.evaluate` and returns RuleResult; reads no case row and writes none |
| RecordAndApplyActivity | Activity | The local decision-record library and the P3 case state service in one transaction, plus the DecisionRecorded outbox row |
| CaseEventSignal | Record | eventId, caseId, eventType, occurredAt, idempotencyKey, synthetic |
| ReferenceCaseInput | Record | caseId, packageCode, businessDate, synthetic |
| CaseEventSignalRelay | Outbox consumer | Reads the delivery, calls `WorkflowGateway.signal`, leaves the event for the next attempt on failure |
| SyntheticCaseGuard | Service | Refuses a workflow input that is not marked synthetic, before any activity |
| ActivityRetryPolicies | Configuration | Initial 1 s, back-off 2, maximum 10 attempts, non-retryable NoPackageInForce |
| ReferenceCaseFixture | Test fixture | Synthetic case row and RESTRUCTURE version for DEV and SIT (GAP-0724) |
| ReferenceCaseWorkflowTest | Test | Time skipping, signal order, idempotency, failure, replay and flag tests |
| No controller | - | The skeleton has no endpoint and no route on gateway-bff |

**Database and migrations.** No migration and no new table. The skeleton writes the local decision record through RWB-PLT-E1027-CON and the case route state through the P3 case state service, both inside schema rwb_case. The fixture is a JSON seed in the test resources, inserted and removed by the harness; it is never part of a release.

**Configuration and reference data**

- Task queue `rwb-case` in namespace `rwb-recovery`, and workflow ID prefix `ref-case-` for the skeleton; Epic 3 case workflows use `case-{caseId}` on the same queue.
- Retry values of section 12.5 as configuration, not code.
- Feature switches `rwb.p3.temporal` and `rwb.p3.drools`, read through the platform parameters contract.
- The RESTRUCTURE version and rule R-RES-04 are owned by RW-COE and governed in rwb-decision; the skeleton references them, never edits them.
- Reference lists LOV-CASE-STATUS and LOV-ROUTE through the reference-data contract of rwb-case.

**Build steps**

1. Define ReferenceCaseWorkflow, ReferenceCaseInput and CaseEventSignal; test that no activity runs before the signal (AC1).
2. Build EvaluateRulesActivity against the embedded kit; test the rule ID, the package version and the NoPackageInForce path (AC1, AC4).
3. Build RecordAndApplyActivity with the idempotency key; test the rollback when the record write fails and the retry after a commit-then-timeout (AC2, AC3).
4. Add ActivityRetryPolicies and the NoPackageInForce do-not-retry rule (AC2, AC4).
5. Build CaseEventSignalRelay and test the Temporal-unavailable path with the outbox delivery, including the PENDING to RETRYING to DELIVERED sequence (AC5).
6. Add SyntheticCaseGuard and the flag checks; test AC6 and the workflow ID prefix.
7. Add the replay test with a recorded history and a later package version, and the `getVersion` change case (AC4).
8. Run the contract-fake profile so the story builds before rwb-decision and the platform stories are in SIT.

**Feature switch.** `rwb.p3.temporal`. Off: no worker on `rwb-case`, ReferenceCaseWorkflow is not deployed and the relay does not run; outbox deliveries stay PENDING. Nothing else changes; the switch does not affect any other workflow of the service.

**Done when.** The tests in section 16 pass, a recorded reference history replays with the same path and no rule evaluation, the workflow ID prefix is enforced, and SIT shows no live case read or written by the skeleton.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-036 | The Temporal frontend is unreachable at signal time | The workflow service is not available. Try again in a few minutes. |
| MSG-P7-003 | The decision record write fails | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No package is in force at evaluation time (NoPackageInForce) | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-009 | The decision record is refused for a missing field | The decision record was refused: {field} is missing or not valid. |

MSG-P3-027 is not retried by ActivityRetryPolicies; the workflow fails at once and the stuck-workflow scan reports it. For MSG-P3-027 the {check} value is "package in force" and the {detail} names the package code only. Thai text for each message follows DL10.

### 15. Screens and states

No screen in this story. The reference workflow is read in the Temporal Web UI by RW-PLATADM and RW-AUDIT, by workflow ID "ref-case-RW-2026-000777"; payloads are decoded only through the codec server (RWB-E2-038). The workflow states RUNNING, COMPLETED and FAILED, the activity attempt count and the build ID of the worker are visible there. SCR-44 Interface and job monitor is not used, because the skeleton has no job and no queue of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-043-01 | AC1, BR1, BR2 | End to end | Signal EV-CASE-0777-01, rule R-RES-04, package RES-2026.12 |
| TC-E2-043-02 | AC2, BR2, BR9 | End to end | Local decision-record store unavailable for EV-CASE-0777-02 |
| TC-E2-043-03 | AC3, BR3 | NFR | RecordAndApply commit then timeout, key CASE_EVENT:EV-CASE-0777-03 |
| TC-E2-043-04 | AC4, BR4, BR10 | End to end | Replay on 2027-01-05 with RES-2027.01 in force |
| TC-E2-043-05 | AC5, BR6 | End to end | Temporal frontend unreachable, then available |
| TC-E2-043-06 | AC6, BR7 | End to end | Flag off, then on with a synthetic case |
| TC-E2-043-07 | AC6, BR7, BR8 | NFR | Worker registration and task queue `rwb-case` with the flag off and on; no live case |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Resilience to NFR and Operational to NFR. The cross-service proof of this legacy key is owned by RWB-ITG-E2043-ITG and is not repeated here.

### 17. Guardrails

- No business value in code. Action text, owner role and timer come from rule packages; retry values are configuration.
- No personal data in logs, tests, workflow history, search attributes or prompts. Payloads are encrypted by PdpaPayloadCodec and the reference case is synthetic.
- No read of another service's tables and no ACE view: the facts of the reference come from the synthetic fixture, and an Epic 3 copy reads ACE data only through the rwb-source-data contract (DP-01, DP-05).
- Workflow code is deterministic: no clock, random or I/O; every call to Drools, the record library or the case state service is in an activity.
- The decision record and the state change are one transaction; no state row exists without its record, and a failed record leaves nothing moved.
- Every activity is idempotent by the event key; a retry never writes a second record or a second state row.
- The skeleton is test-only: it never runs against a live case, never writes a non-synthetic case row, and its workflow ID never starts `case-`.
- The skeleton declares no REST path and no gateway-bff route; it writes no topic of its own and publishes no event of its own.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision is recorded with the rule and version that made it | Epic 2, 3.2; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-RES-04; R-UNI-38 | TC-E2-043-01, TC-E2-043-04 |
| REQ-DRI-005 | No action proceeds if its decision record cannot be written | Epic 2, 3.2; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-39 | TC-E2-043-02, TC-E2-043-03 |
| REQ-CWC-016 | Rules are evaluated by Drools from a versioned package | Epic 2, 3.2; Program, 5.3 | FEAT-DRI-07 | All recovery processes | R-RES-04 | TC-E2-043-01, TC-E2-043-04, TC-E2-043-05 |
| REQ-DRI-007 | An outbound step retries on a defined schedule and leaves a visible exception when it fails | Program, 5.2 | FEAT-DRI-07 | All recovery processes | None | TC-E2-043-05, TC-E2-043-07 |
| D-RCV-60 | The reference workflow runs on the owning service's queue and merges record and state into one activity | Template and Rules §R5.5, §R5.7 | FEAT-DRI-07 | All recovery processes | None | TC-E2-043-01, TC-E2-043-03 |

### 19. Out of scope

- The case workflows of Epic 3, their timers and their outbound chains.
- Workflow versioning and the replay gate as a platform capability (RWB-E2-040); this story only passes it.
- The worker, the payload codec and the smoke workflow as platform components (RWB-PLT-E1071-CON).
- Rule package authoring, approval and the registry as a contract (RWB-P7-E1073); the Epic 2 package content (RWB-P3-E2042-APP).
- The outbox sender schedule and the consumer list (RWB-PLT-TE006-CON).
- The Temporal platform, its observability and its DR (RWB-PLT-WF, RWB-PLT-OBS).
- The central decision ledger and the collection of DecisionRecorded into it (RWB-P7-E2043-APP); this story writes the local record only.
- The real cross-service proof of the pattern (RWB-ITG-E2043-ITG).
- The deployment of the worker, the flag, the replay gate step and the dashboards (RWB-P3-E2043-OPS).
- gateway-bff, the composite route and every screen; the skeleton uses none of them.
- The case lifecycle and the full state model (Epic 3).
