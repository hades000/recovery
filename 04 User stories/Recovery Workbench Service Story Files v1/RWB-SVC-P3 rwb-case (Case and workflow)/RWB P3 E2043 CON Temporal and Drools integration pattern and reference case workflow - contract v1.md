# RWB-P3-E2043-CON Temporal and Drools integration pattern and reference case workflow

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2043-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-043 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract of the reference case workflow for rwb-case: the workflow interface with its input and signal records, the two activity interfaces, the retry policy, the determinism and versioning declarations, the contract tables of section 12 and the replay fixture**, so that **the app story, the operations story and every Epic 3 squad can build against a fixed, testable workflow contract on Day 1 without waiting for the worker to be deployed**.

### 2. Business rationale

A Temporal contract is not a REST document: it is a typed workflow interface, a typed activity interface and a set of serialisable records that are published as a contract jar, so a caller imports only the interface and calls the owner's task queue (Arch v5 slide 11). Get it wrong and two costs follow immediately: a workflow that cannot be replayed after a deploy, because the activity contract or the record shape changed under a running history, and a second squad inventing a different order of steps for its own case.

This baseline fixes both in one place. It names the workflow, its input record and its signal record; it names the two activities, with the rule answer in one and the decision record plus the state change in the other; it fixes the retry policy and the one non-retryable outcome; and it declares the determinism rule and the versioning rule that the replay gate of RWB-E2-040 enforces on every build (Temporal and Drools design slides 14 and 27).

The baseline has no REST path, no event of its own and no table. The skeleton is test-only, so the contract states that scope explicitly: the workflow ID prefix is `ref-case-`, the input carries `synthetic`, and the task queue is `rwb-case` in namespace `rwb-recovery` because the queue belongs to the owning service (Arch v5 slides 24 and 41). The legacy queue `rwb-platform` is not part of this contract.

### 3. Preconditions

- The service naming rule of the platform library is in force: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case` (DP-14, RWB-PLT-E1047-CON).
- The workflow kit is available as a published library, with the contract-jar convention, the payload codec and the build ID provider (RWB-PLT-E1071-CON, DP-10).
- The outbox and inbox library is available as the reference for the `OutboxConsumer` interface the relay implements, and for the delivery states PENDING, RETRYING and DELIVERED (RWB-PLT-TE006-CON, DP-09).
- The local decision-record library and the shared topic `rwb.decision-record.v1` are published, so the contract can state who publishes DecisionRecorded (RWB-PLT-E1027-CON, DP-03).
- The embedded Drools kit is published, so the activity contract can name `RuleResult` and `NoPackageInForce` without redefining them (RWB-PLT-E1072-CON, DP-04).
- The operations and their owners are taken from the Ownership Map only; the contract documents no operation owned by another service.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the workflow interface: one workflow method, one signal method, and nothing else public.
2. Draft the two records: `ReferenceCaseInput` for the start and `CaseEventSignal` for the signal, with the field list and the `synthetic` flag fixed.
3. Draft the two activity interfaces against the rule evaluator and the case state service, and state the idempotency key and the transaction boundary in the contract text.
4. Declare the retry policy as configuration with its four values and the non-retryable outcome.
5. Declare the determinism rule and the versioning rule: build ID per worker, `getVersion` for an in-place change, the replay gate on every build.
6. State the scope: test-only, workflow ID prefix `ref-case-`, no REST path, no topic, no table, no Schedule.
7. Publish the nine contract tables of section 12, each with its owner from the Ownership Map, and state that no fake is required.
8. Add the contract tests: interface shape, signal schema, activity signatures, retry values, determinism boundary, and a recorded history that replays.
9. Tag the baseline and hand it to the app story, the operations story and every Epic 3 squad.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The workflow interface declares a second workflow method or a query that returns a mutable type | The contract check fails and the baseline is not tagged | None | AC1 |
| X2 | A signal record carries a personal-data field | The review refuses the record and no baseline is published | None | AC2 |
| X3 | An activity signature changes a parameter type or its order | The compatibility check fails; a breaking change needs a new contract version | None | AC3 |
| X4 | A workflow class places an I/O call or a Drools call inside workflow code | The boundary test fails the build | None | AC5 |
| X5 | A recorded history no longer replays against the build | The replay gate fails the release and the contract is not declared compatible | MSG-P3-038 | AC6 |
| X6 | The contract declares a REST path, a topic or a table of its own | The review fails the baseline, because the skeleton owns none of the three | None | AC6 |
| X7 | The retry values differ between the contract text and the worker configuration | The contract test fails on the drift | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the workflow kit, the record library and the naming rule only |
| Negotiable | Field-level detail of the records is settled with the consumers; the two-activity form, the retry values and the determinism rule are fixed by the target design |
| Valuable | Unblocks the app, operations and test work of this legacy key on Day 1 and gives every Epic 3 squad the same order of steps |
| Estimable | One interface, two records, two activity interfaces, one retry policy, nine contract tables and six contract tests |
| Small | Fits one sprint with the contract tests and the replay fixture |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Workflow and activity contract for the reference case workflow of rwb-case

  Background:
    Given the service naming rule of the platform library is in force
    Given the namespace is rwb-recovery and the task queue of rwb-case is rwb-case
    Given the workflow kit publishes its interfaces as a contract jar per service

  Scenario: AC1 The workflow interface is one method, one signal and nothing else (new, D-RCV-60)
    Given the published contract of ReferenceCaseWorkflow
    When it is validated against the workflow kit contract rules
    Then it declares exactly one workflow method run(ReferenceCaseInput)
    Then it declares exactly one signal method onCaseEvent(CaseEventSignal)
    Then it declares no other public method, no query and no update handler
    Then the contract states the task queue rwb-case in namespace rwb-recovery and the workflow ID prefix ref-case-
    Then the contract jar is published with a version and the consumer imports only the interface

  Scenario: AC2 The CaseEvent signal schema is fixed and carries no personal data (new, D-RCV-60)
    Given the CaseEventSignal record of the contract
    When its fields are read
    Then it carries eventId, caseId, eventType, occurredAt, idempotencyKey and synthetic, and no other field
    Then it carries no name, address, identity number or contact point
    Then synthetic is required and is true for every reference run
    When a payload omits idempotencyKey or carries an unknown field
    Then the contract test refuses the payload and the signal is not accepted

  Scenario: AC3 The two activity contracts replace the legacy three (new, D-RCV-60)
    Given the activity interfaces of the contract
    When they are read
    Then EvaluateRulesActivity declares evaluate(packageCode, facts, onDate) and returns packageCode, packageVersion, ruleId and outputs
    Then RecordAndApplyActivity declares apply(request) with the event idempotency key in the request
    Then the contract states that the record write and the state change are one transaction and a retry returns the first result
    Then no WriteDecisionLog or ApplyState activity is declared for the target
    Then a changed parameter type or order fails the compatibility check and needs a new contract version

  Scenario: AC4 The retry policy is declared and matches the worker configuration (new, D-RCV-60)
    Given the retry policy of the contract
    When its values are compared with the worker configuration
    Then the initial interval is 1 second, the back-off coefficient is 2 and the maximum attempts is 10
    Then NoPackageInForce is listed as non-retryable for both activities
    Then the policy applies to EvaluateRulesActivity and RecordAndApplyActivity only
    When a value in the configuration differs from the contract text
    Then the contract test fails on the drift

  Scenario: AC5 The deterministic build and the versioning declarations are enforced (new, D-RCV-60)
    Given the workflow package of the contract
    When the boundary test and the determinism check run
    Then no workflow class reads a clock, a random source, a database or the network
    Then no workflow class calls Drools or the case state service outside an activity
    Then the contract declares the build ID of the worker and the getVersion change identity for an in-place change
    Then a workflow class placed outside the workflow package fails the boundary test

  Scenario: AC6 A recorded history replays and the nine contract tables are complete (new, D-RCV-60)
    Given the recorded reference history of the contract fixture
    When it is replayed against the build
    Then the replay reaches the same activity path and reads the recorded activity result
    Then the replay calls no rule evaluator and no case state service
    Then the replay result is reported to the gate of RWB-E2-040 with the build ID
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then the contract declares no REST path, no topic of its own, no table and no Schedule
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A workflow and its activities are published as a typed contract jar; a caller imports only the interface and calls the owner's task queue | Arch v5 slide 11 (Temporal contract row); Design slide 12 |
| BR2 | One workflow interface has one workflow method and one signal method for this skeleton; a second public method is a new contract version | Design slide 13; RWB-PLT-E1071-CON |
| BR3 | The task queue is `rwb-case` in namespace `rwb-recovery`; the legacy queue `rwb-platform` is not declared | Arch v5 slides 24 and 41; DP-10 |
| BR4 | The workflow ID of the skeleton starts `ref-case-` and never `case-`, and the input carries `synthetic`; the skeleton is test-only | Legacy RWB-E2-043 BR7; ASM-1272 |
| BR5 | The signal record carries identifiers, a type, a timestamp, a key and the synthetic flag only; no personal data | Design slide 27 (PDPA); Template and Rules §R7.2 s17 |
| BR6 | The record write and the state change are one transaction in one activity; the legacy separate WriteDecisionLog and ApplyState activities are not declared | Design slide 14; DP-03; R-UNI-39 |
| BR7 | The retry policy is data: initial 1 s, back-off 2, maximum 10 attempts, NoPackageInForce non-retryable; the contract text and the configuration are checked for drift | Design slides 14 and 28 |
| BR8 | Workflow code is deterministic and all I/O is in an activity; the boundary test fails any class outside the workflow package | Design slide 27; ADR-011 |
| BR9 | A breaking change to an activity or a record needs a new contract version; a compatible addition is allowed within the current one | Arch v5 slide 11 (contract per service) |
| BR10 | The contract declares no REST path, no event of its own, no table and no Schedule, because the skeleton owns none of them | Section 12 of this story; DP-11; DP-19 note |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The interface, the two records and the two activity interfaces are described | In review |
| In review | Consumer sign-off | The app, operations and test work accepts the contract and the replay fixture | Baselined |
| Baselined | Compatible addition | An optional field is added to a record and existing histories still replay | Baselined |
| Baselined | Breaking change | A parameter type, the parameter order or a required field changes | New contract version drafted |
| Baselined | Replay failure | A recorded history no longer replays against the build | In review |
| Baselined | Drift between the contract and the worker configuration | The retry or the build ID declaration differs | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the contract, the records, the retry policy and the replay fixture; tags the baseline |
| Solution architect | Approves a breaking change and a new contract version |
| Platform workflow kit owner | Owns the contract-jar convention, the payload codec, the build ID provider and the replay gate mechanism |
| Consuming teams (the app story, the operations story and the Epic 3 squads) | Review and sign off the parts they use |
| Data steward | Confirms that no record declares a personal-data field and that search attributes stay identifiers only |
| RW-COE | Confirms the package code and rule ID used by the reference fixture |

The worker runs as the rwb-case service identity (DP-02), carried by the chart as a secret reference; the contract fixes no literal login name.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| `ReferenceCaseInput` | caseId, packageCode, businessDate, synthetic; no other field |
| `CaseEventSignal` | eventId, caseId, eventType, occurredAt, idempotencyKey, synthetic |
| `RuleResult` | packageCode, packageVersion, ruleId, outputs, as published by the embedded Drools kit |
| `RecordAndApplyRequest` | the event idempotency key, the rule result, the state change and the business date |
| `RecordAndApplyResult` | the record reference, the state reference and whether the call created the row or found it |
| Search attributes | CaseId, Stage, ProductGroup, QueueCode only; no personal data |
| History | references, codes, IDs, dates and amounts only; payloads pass through the payload codec |

The exact field-level detail of `RecordAndApplyRequest` and of the outputs map (types, cardinality, which rule output is mandatory per package) is Not specified in the source documents (GAP-0727; ASM-1275); this story fixes the field names above and leaves the detail to the baseline review.

### 12. Contract

#### 12.1 REST operations provided

None. The skeleton has no REST path, no admin operation and no health contract beyond the platform probes of RWB-P3-E2043-OPS; it is started by the reference harness in DEV and SIT only.

#### 12.2 REST operations consumed

None. The only remote call is `WorkflowGateway` to the Temporal frontend, which is a gRPC contract of the workflow kit (RWB-PLT-E1071-CON), and the in-process calls to the rule evaluator, the local decision-record library and the case state service.

#### 12.3 Events published

None. The skeleton publishes nothing. The outbox deliveries it reads belong to RWB-PLT-TE006-CON, and the only event written on its path is DecisionRecorded on `rwb.decision-record.v1`, published by the local decision-record library (DP-03) and owned by P7.

#### 12.4 Events consumed

| Event type | Topic | Owner of the type | Contract element |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 | CaseEventSignal, eventType CaseCreated |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 | CaseEventSignal, eventType CaseAllocated |
| `rwb.case.CaseAllocationFailed.v1` | `rwb.case.events.v1` | P3 | CaseEventSignal, eventType CaseAllocationFailed |
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 | CaseEventSignal, eventType CaseTransferred |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 | CaseEventSignal, eventType CaseStateChanged |
| `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | P3 | CaseEventSignal, eventType TimerBreached |

The relay implements the `OutboxConsumer` interface of RWB-PLT-TE006-CON, reads the delivery of one of these types and calls `WorkflowGateway.signal(workflowId, "CaseEvent", payload)`. The topic and the six event types are the property of RWB-PLT-TE006-CON and of the case event contract; this story only fixes how each type maps onto the signal. A failed call leaves the delivery PENDING or RETRYING with its next attempt time.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| ReferenceCaseWorkflow | Workflow, test-only scope, workflow ID prefix `ref-case-` | `rwb-case` | `run(ReferenceCaseInput)`, `onCaseEvent(CaseEventSignal)` |
| EvaluateRulesActivity | Activity | `rwb-case` | Package code, facts and date in; package code, package version, rule ID and outputs out |
| RecordAndApplyActivity | Activity | `rwb-case` | Event key, rule result and state change in; record reference, state reference and created-or-found out |
| CaseEventSignalRelay | Outbox consumer | not a worker | Delivery reference in; the signal call and the delivery status out |

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

| Item | Value | Declared as |
|---|---|---|
| Initial interval | 1 second | Configuration, checked against the contract text |
| Back-off coefficient | 2 | Configuration |
| Maximum attempts | 10 | Configuration |
| Non-retryable | NoPackageInForce | Contract text and activity configuration |
| Applies to | EvaluateRulesActivity, RecordAndApplyActivity | Contract text |

**Versioning and replay.** Each worker carries the build ID of its build; an in-place code change uses `Workflow.getVersion(changeId, DEFAULT_VERSION, 1)`; the replay gate of RWB-E2-040 replays the recorded histories against every new build before release. The build ID format and the versioning policy are Not specified in the source documents (GAP-0725; ASM-1273); the size of the replay corpus and the text of MSG-P3-038 are Not specified in the source documents (GAP-0726; ASM-1274).

#### 12.6 Schedules

None. The reference workflow is started by the harness and is never started by a Schedule; the Schedules of rwb-case are declared by their own stories.

#### 12.7 Tables owned

None. The contract names no table as its own: the local decision record, the outbox, the inbox and the idempotency objects are library objects created in schema rwb_case by its own DB story, and the case row is written by the P3 case state service. No table of another service is read or written (DP-01).

#### 12.8 Contract fakes

None. There is no WireMock mapping and no HTTP stub: the workflow tests run on TestWorkflowEnvironment with time skipping, and the rule evaluator, the decision-record library and the case state service are replaced by in-process test doubles of their published interfaces. The package facts of the reference (RESTRUCTURE "RES-2026.12", rule R-RES-04) come from the contract mock of rwb-decision named in the app story.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | No path, no admin operation and no client |
| Kafka | 0 published, 6 types consumed through the relay | The six `rwb.case.*` types of `rwb.case.events.v1` map onto CaseEventSignal; the topic belongs to RWB-PLT-TE006-CON |
| Temporal | 1 workflow, 2 activities, 0 Schedules | ReferenceCaseWorkflow, EvaluateRulesActivity, RecordAndApplyActivity on `rwb-case` |
| File | None | The recorded history used by the replay test is a test resource, not runtime data |

### 13. Solution plan

**Deliverables.** `contract/rwb-case-reference-workflow-v1.jar` with the workflow interface, the two activity interfaces and the records; `contract/reference-workflow.md` with the determinism, versioning and retry rules; `contract/replay/` with the recorded reference history; the six contract tests.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the contract names no table and reads no other service's table | none |
| DP-03 | DecisionLogWriter, decision log | The record and the state change in one transaction, plus `rwb.decision-record.v1`; two activities replace the legacy three | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | The activity contract names `RuleResult` and `NoPackageInForce` from the embedded kit; the package model comes from rwb-decision | H RWB-PLT-E1072-CON (registry side is RWB-P7-E1073) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The contract carries no ACE field; an Epic 3 copy reads ACE data through the rwb-source-data contract | none |
| DP-07 | Reference data, LOV | The reference data of the case status and route lists is read through the rwb-case contract inside RecordAndApply | H RWB-PLT-E1043-CON; RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The relay implements the `OutboxConsumer` of the outbox library; CloudEvents envelope and delivery states | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The workflow kit provides the queue, the codec, the build ID and the versioning; no Schedule is declared | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | No REST hop is declared at all; the workflow reaches the rules and the state through activities | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | The contract reuses `rwb.case.events.v1` and `rwb.case.<Event>.v1` through the naming library and adds no topic | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | No migration in this contract; the library objects arrive with the rwb_case baseline | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff is not used by this contract: no route, no screen and no endpoint are declared | H RWB-PLT-N001-CON |

**Build steps**

1. Publish the workflow interface and the two records with the field list of section 11; test the interface shape (AC1, AC2).
2. Publish the two activity interfaces against `RuleResult` and the case state service; test the compatibility rule (AC3).
3. Write the retry policy as a configuration fragment and state the non-retryable outcome; test the drift check (AC4).
4. Add the determinism boundary test and the package rule, and declare the build ID and `getVersion` identity (AC5).
5. Record the reference history and add the replay test with a later package version (AC6).
6. State the scope rule of BR10 and assert in the review that no REST path, topic, table or Schedule is declared (AC6).
7. Tag the baseline and circulate it to the app, operations and Epic 3 consumers.

**Done when.** The contract jar builds, the six contract tests pass, the recorded history replays with no rule evaluation, and the app and operations stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-036 | The Temporal frontend is unreachable when the relay signals | The workflow service is not available. Try again in a few minutes. |
| MSG-P3-027 | No package version is in force at evaluation time | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-003 | The decision record write fails inside the activity | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-038 | A recorded history does not replay against this build | Not specified in the source documents (GAP-0726; ASM-1274) |

The business message IDs keep the text of the legacy story and of the message catalogue; this contract only states where each one is produced on the workflow path. The text of MSG-P3-038 and the size of the replay corpus are not fixed by any source read for this story.

### 15. Screens and states

No screen in this contract. The contract serves the Temporal Web UI view of the reference run: the workflow state, the activity attempt count, the build ID of the worker and the search attributes CaseId, Stage and QueueCode, read by RW-PLATADM and RW-AUDIT. Payloads are decoded only through the codec server (RWB-E2-038). SCR-44 Interface and job monitor is not used, because the skeleton owns no job and no queue of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2043-CON-01 | AC1 | Contract | The contract jar declares one workflow method, one signal method and no other public member |
| TC-P3-E2043-CON-02 | AC2 | Contract | The six-field CaseEventSignal validates; a payload without the key or with an unknown field is refused |
| TC-P3-E2043-CON-03 | AC3 | Contract | The two activity signatures and the one-transaction statement; a changed parameter order fails the compatibility check |
| TC-P3-E2043-CON-04 | AC4 | Contract | Retry values 1 s, back-off 2, 10 attempts and NoPackageInForce non-retryable; a drift fails the test |
| TC-P3-E2043-CON-05 | AC5 | Component | The boundary and determinism checks; a workflow class outside the package and a clock or Drools call inside workflow code both fail |
| TC-P3-E2043-CON-06 | AC6 | Component | A recorded history replays against the build; the nine contract tables are complete and declare no REST path, topic, table or Schedule |

### 17. Guardrails

- No business value in the contract: the package code, the rule ID and the state values used by the reference are data in the rule packages and the reference tables, never constants in the interface.
- No personal data in a record, an example, a search attribute or the recorded history: identifiers, codes, dates and amounts only, and payloads pass through the payload codec.
- One task queue, one namespace and one Java package per service; the contract names only `rwb-case` and `th.co.scb.ace.workbench.recovery.case` (DP-10, DP-14).
- The contract declares no operation, topic or table owned by another service, and the six event types are used through the ownership of RWB-PLT-TE006-CON (DP-01, DP-09).
- Every example and the recorded history are synthetic; no production payload is copied into a record or a fixture.
- A breaking change to a record or an activity is a new contract version, so a running history is never invalidated in place.
- The retry policy is declared once and checked for drift, so the contract text can never disagree with the worker.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision is recorded with the rule and version that made it | EvaluateRulesActivity result and the record written by RecordAndApplyActivity | TC-P3-E2043-CON-03, TC-P3-E2043-CON-06 |
| REQ-DRI-005 | No action proceeds if its decision record cannot be written | One transaction in RecordAndApplyActivity; the created-or-found result | TC-P3-E2043-CON-03 |
| REQ-CWC-016 | Rules are evaluated by Drools from a versioned package | packageCode and packageVersion in the activity result and the record | TC-P3-E2043-CON-06 |
| REQ-DRI-007 | An outbound step retries on a defined schedule and leaves a visible exception when it fails | Retry policy, the non-retryable outcome and the delivery states of the relay | TC-P3-E2043-CON-04 |
| D-RCV-60 | The pattern runs on the owning service's queue with two activities and one transaction | Task queue `rwb-case`, workflow ID prefix and the two activity interfaces | TC-P3-E2043-CON-01, TC-P3-E2043-CON-03 |

### 19. Out of scope

- The implementation of the workflow, the two activities and the relay (RWB-P3-E2043-APP).
- The deployment of the worker, the flag, the replay gate step and the dashboards (RWB-P3-E2043-OPS).
- The replay gate as a platform capability and its release step (RWB-E2-040, RWB-PLT-E1071-CON); this contract only states that a build passes it.
- The outbox, inbox and CloudEvents library and the six case event schemas, which are owned by RWB-PLT-TE006-CON.
- The local decision-record library and the central ledger (RWB-PLT-E1027-CON, RWB-P7-E2043-APP).
- The rule package governance and the registry contract (RWB-P7-E1073); the Epic 2 package content (RWB-P3-E2042-APP).
- The remaining case workflows of Epic 3 and their own contracts.
- The real cross-service proof of the pattern (RWB-ITG-E2043-ITG).
- gateway-bff, the composite route and every screen; the contract declares none of them.
- The field-level detail of the request record and of the rule outputs map (GAP-0727).
