# RWB-P3-E1020-CON Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1020-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not sized; the squad sizes it at refinement |
| Epic design sign-off | Confirmed by the programme directive |
| Contract version | v1 (REST /api/recovery/case/v1; events rwb.case.<Event>.v1) |
| Depends on (build) | None |
| Contract dependencies | C RWB-P7-E1073-CON (rwb-decision rule-model contract, §13 DP-04) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-009, FR-P3-010, FR-P3-011, FR-P3-012, FR-P3-030) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-020 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 22 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **the queue placement, the case-by-queue read, the my-tasks read and the task update of the allocation and assignment engine published as versioned contracts before any code is written**, so that **the engine, the screens and the other services build against one agreed description of the same behaviour**.

This is the contract baseline of the legacy RWB-E1-020 behaviour in rwb-case. It is Day 1 work with no build dependency: it publishes

- the **OpenAPI 3.1** document for the allocation-related operations of rwb-case: `POST /api/recovery/case/v1/queues/{queueId}/placements`, `GET /api/recovery/case/v1/queues/{queueId}/cases`, `GET /api/recovery/case/v1/me/tasks` and `PATCH /api/recovery/case/v1/tasks/{taskId}`;
- the **AsyncAPI** document for `CaseAllocated`, `CaseAllocationFailed` and `CaseStateChanged` on topic `rwb.case.events.v1`, with event names `rwb.case.<Event>.v1` and CloudEvents 1.0 in binary mode, key caseId;
- the shape of the **RuleResult** the embedded Drools kit hands to the allocation activity, and the shape of the fetched rule model;
- the **problem-details** error envelope, the **Idempotency-Key** rule on every POST, and the versioning rule for the path and for the event schemas;
- the nine contract tables of section 12, so that the fake services and the contract tests are generated from one place.

The contract describes only the artefact. No business value is invented here: queue codes, rule IDs, package versions, methods, caps and parameters are the data values named by the legacy story and the design, and where a value is missing the placeholder is used.

### 2. Business rationale

Every consumer of the allocation behaviour needs the same description on day one. The build story RWB-P3-E1020-APP writes the engine; the queue, task and my-work screens and the gateway-bff composite route read the same operations; rwb-decision supplies the rule model the engine evaluates. Without a published contract the consumers would each invent a payload, and a change of a field would break a screen instead of a version.

The legacy story described its contract in prose, in Java interfaces inside one module (`AllocationService`, `RuleEvaluator`, `DecisionLogWriter`) and in a single monolith base path. The target publishes the same semantics as an OpenAPI 3.1 document under the service base path, an AsyncAPI document per topic, and a typed contract for the rule answer, so that the one hop from gateway-bff and the Kafka facts are enforceable in a contract test on every build.

It meets REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and REQ-CWC-016 by making the allocation outcome, the assignment reason and the rule version observable on a published interface.

### 3. Preconditions

- The service naming of the template is fixed: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- The operation list of rwb-case is agreed in the ownership map: `POST /queues/{queueId}/placements`, `GET /queues/{queueId}/cases`, `GET /me/tasks`, `PATCH /tasks/{taskId}` all belong to P3 rwb-case.
- The event list of rwb-case is agreed: `CaseCreated`, `CaseAllocated`, `CaseAllocationFailed`, `CaseTransferred`, `CaseStateChanged`, `TimerBreached`.
- The platform contract libraries are available: OpenAPI 3.1 and AsyncAPI as the standard, CloudEvents 1.0 as the event envelope, RFC 9457 for errors (RWB-PLT-E1047-CON for the naming library).
- The rule model is governed in rwb-decision, so the contract refers to `GET /api/recovery/decision/v1/rule-models/{n}/{v}` and never to a table.
- No build dependency: the story can be finished before any engine code exists, and the fakes of 12.8 are generated from the documents.

### 4. Flow

1. **Collect.** Take the behaviour of legacy RWB-E1-020 — the placement outcome, the assignment record with reason ALLOCATION, the rule ID and package version pairs, the overflow and exception outcomes — and the operation list and event list of rwb-case.
2. **Model.** Write the request and response schemas for the four operations, with the outcome enumeration ASSIGNED, OVERFLOW, EXCEPTION, DEVIATION_QUEUE, SKIPPED, FAILED_LOG taken from the legacy `OutcomeType`, and the fields caseId, queueId, ownerUserId, ruleId, ruleVersion, reason.
3. **Describe the events.** Write the AsyncAPI document for `rwb.case.CaseAllocated.v1` (caseId, queueId, ownerId, ruleId, ruleVersion), `rwb.case.CaseAllocationFailed.v1` (caseId, reason, ruleGap) and `rwb.case.CaseStateChanged.v1` (caseId, fromStatus, toStatus, ruleId, ruleVersion), key caseId, no personal data.
4. **Describe the rule answer.** Write the RuleResult schema: packageCode, packageVersion, ruleId, outputs; and the rule-model response: packageCode, packageVersion, checksum, rules with ruleId, row order and outputs.
5. **Describe the failures.** Write the RFC 9457 problem-details envelope and the error codes of the legacy contract: 401 no session (MSG-P4-001), 403 role lacks the right (MSG-P4-002), 404 not found or outside scope (MSG-P4-003), 409 the run is already in progress (MSG-GEN-004), 422 the request is not valid, 503 the store is unavailable.
6. **Fix the rules that every operation follows.** `Idempotency-Key` required on every POST and stored with its response; GET retried once with jitter; 2 s timeout; one hop only; `/v1` in the path; event schemas backward compatible.
7. **Publish and freeze.** Publish the documents in the service contract folder, register the event schemas in the registry with BACKWARD compatibility, and generate the fakes and the contract tests from them.
8. **Keep it true.** Every build runs the contract tests; a change is a new version of the document, never an edit of a published one.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| C1 | A published document is edited in place | The build fails the contract check; a change is a new version of the document and a new event schema version | None | AC5 |
| C2 | An operation is published without the `Idempotency-Key` header on POST | The contract test fails and the document is not released | None | AC4 |
| C3 | An event schema drops or renames a field | The registry refuses the version because compatibility is BACKWARD | None | AC2 |
| C4 | A rule model response has no checksum | The document is rejected; RWB-P3-E1020-APP cannot verify the model it swaps in | None | AC3 |
| C5 | A consumer needs a field that the document does not carry | A gap is raised against the document, not a field added silently | None | AC6 |
| C6 | The base path of an operation is not `/api/recovery/case/v1` | The contract test fails; the legacy monolith base path is not allowed | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses only the naming of the template, the operation and event lists of rwb-case, the legacy RWB-E1-020 contract section and the rule-model decision; no engine code and no build dependency |
| Negotiable | Field naming and examples are open to review; the operations, the events and the outcome enumeration are fixed by the behaviour |
| Valuable | Four consumers (engine, screens through gateway-bff, rwb-decision rule model, contract tests) build against one description from day one |
| Estimable | Two documents, one rule-answer schema, one error envelope, one versioning rule |
| Small | One week or less including the generated fakes, so it fits within the two-week iteration |
| Testable | Seven criteria, each tested by a contract test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Published contracts of the allocation and assignment engine

  Background:
    Given the rwb-case service naming of the template: schema rwb_case, base /api/recovery/case/v1, topic rwb.case.events.v1, queue rwb-case
    Given the service is P3 rwb-case and the owner of the four allocation operations

  Scenario: AC1 The OpenAPI 3.1 document describes the four allocation endpoints (new, D-RCV-60)
    Given the published OpenAPI 3.1 document of rwb-case
    When the document is validated against OpenAPI 3.1
    Then it declares POST /api/recovery/case/v1/queues/{queueId}/placements, GET /api/recovery/case/v1/queues/{queueId}/cases, GET /api/recovery/case/v1/me/tasks and PATCH /api/recovery/case/v1/tasks/{taskId}
    Then every operation declares its path and query parameters, its request schema where it has a body, and its 200 or 202 response schema
    Then the placement request schema carries caseId, reason and the optional named owner, and the placement response carries the outcome from ASSIGNED, OVERFLOW, EXCEPTION, DEVIATION_QUEUE, SKIPPED and FAILED_LOG with caseId, queueId, ownerUserId, ruleId, ruleVersion and reason
    Then the case-by-queue read returns caseId, caseNo, queueId, teamCode, ownerUserId, status, exposureBand and lastAllocationDate, and never a personal field
    Then the my-tasks read returns taskId, caseId, taskCode, status, dueAt and priority, scoped to the caller
    Then the task update accepts only status, outcomeCode and a comment, and answers with the task and its new status

  Scenario: AC2 The AsyncAPI document describes the three allocation events (new, D-RCV-60)
    Given the published AsyncAPI document of rwb-case
    When the document is validated against AsyncAPI 3 and the registry
    Then it declares rwb.case.CaseAllocated.v1, rwb.case.CaseAllocationFailed.v1 and rwb.case.CaseStateChanged.v1 on topic rwb.case.events.v1
    Then CaseAllocated carries caseId, queueId, ownerId, ruleId and ruleVersion, where ruleVersion is the ALLOCATION package version label
    Then CaseAllocationFailed carries caseId, reason and ruleGap, and reason uses the values of the exception table, including NO_ROW_MATCHED and NO_OVERFLOW_QUEUE
    Then CaseStateChanged carries caseId, fromStatus, toStatus, ruleId and ruleVersion
    Then every message uses CloudEvents 1.0 in binary mode with key caseId and no personal data, and the schema registry accepts the version with BACKWARD compatibility

  Scenario: AC3 The RuleResult and rule-model shape is published (new, D-RCV-60)
    Given the rule answer that the embedded Drools kit hands to the allocation activity
    When the RuleResult schema is reviewed against the governance contract of rwb-decision
    Then it carries packageCode, packageVersion, ruleId and outputs, and packageVersion is the version label of the package in force on the business date
    Then the rule-model response of GET /api/recovery/decision/v1/rule-models/{n}/{v} carries packageCode, packageVersion, checksum and the ordered rows, each with ruleId, rowOrder and outputs
    Then the outputs of the allocation row carry the target queue code and the owner role, and the outputs of the assignment row carry the method from ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER and SKILL, the cap and the overflow queue code where one exists
    Then the document states that the checksum is verified before a model is swapped in, and that the last good model is kept on failure

  Scenario: AC4 The error envelope and the Idempotency-Key rule are published (new, D-RCV-60)
    Given the problem-details envelope of the standard
    When the OpenAPI document is reviewed
    Then every operation declares the problem-details responses 401, 403, 404, 409 where the run can be in progress, 422 and 503, with type, title, status, detail and instance
    Then the title of 403 carries the MSG-P4-002 text and the title of 409 carries the MSG-GEN-004 text
    Then every POST declares the Idempotency-Key header as required, and the document states that the key is stored with its response and replayed unchanged
    Then every GET is declared retryable once with jitter and every operation declares the 2 s timeout and the one-hop rule

  Scenario: AC5 Versioning is published and enforced (new, D-RCV-60)
    Given a published document and a published event schema
    When a change is proposed
    Then the path carries /v1 and a breaking change is a new path version, never an edit of the published document
    Then an event change is a new schema version that the registry accepts as BACKWARD compatible, and a removed or renamed field is refused
    Then the published documents are read only, and the build fails if a published file changes hash

  Scenario: AC6 The nine contract tables are published with the documents (new, D-RCV-60)
    Given the contract section of this story
    When the contract pack is reviewed
    Then the pack contains the REST operations provided and consumed, the events published and consumed, the workflows and activities, the schedules, the tables owned, the contract fakes and the call-type summary
    Then every row names an owner taken from the ownership map and no other owner
    Then the fakes of the rule model, the decision record, the AceDataReady event and the ACE notification path are generated from the documents

  Scenario: AC7 Each of the nine business rules is carried by a published element of the contract (new, D-RCV-60)
    Given the nine business rules BR1 to BR9 of section 8
    When the published documents and the contract tests are reviewed rule by rule
    Then each rule names the published element that carries it: the Idempotency-Key of the placement, the case-by-queue read, the three events, the rule answer, the rule-model read, the problem-details envelope, the service base path, the versioning note and the owner column of the contract tables
    Then a rule that is an architecture constraint is proved by a guardrail check or a boundary test instead of a payload test
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The queue placement is a POST with an Idempotency-Key; the same key returns the stored outcome and never places a case twice | Arch v5 slide 11; template §R4 |
| BR2 | The case-by-queue read returns the queue, the team, the owner, the status and the last allocation date, and never a personal field | Arch v5 slide 11; template §R4 |
| BR3 | The three allocation events are facts on `rwb.case.events.v1`, key caseId, CloudEvents 1.0 binary mode, no personal data, backward-compatible schemas | Arch v5 slides 11 and 42 |
| BR4 | The rule answer names the package code, the package version label, the rule ID and the outputs; the version is the one in force on the business date | Drools design slides 14 and 16 |
| BR5 | The rule model is fetched over the contract from rwb-decision and verified by checksum; no service reads a rule table | DP-01, DP-04 |
| BR6 | Errors use RFC 9457 problem details and keep the legacy message identifiers MSG-P4-002 and MSG-GEN-004 where they still apply | Arch v5 slide 11; legacy RWB-E1-020 |
| BR7 | Every operation sits under the service base path and one hop from gateway-bff; a call chain is not allowed | DP-13; Arch v5 slide 12 |
| BR8 | A published document is versioned, never edited; a breaking change is a new version | Arch v5 slide 11; template §R8.2 |
| BR9 | The owner of every row of the contract tables comes from the ownership map only | Template §R3 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Published | A compatible field is added | The registry accepts the version as BACKWARD compatible | Published, new minor version |
| Published | A field is renamed or removed | The registry refuses the version | Refused, previous version stays published |
| Draft | Review passed | The contract tests and the review pass | Published v1 |
| Published | A breaking behaviour change is needed | The change cannot be expressed compatibly | Draft of the next path version |

The placement outcome is an enumeration of the contract, not a case state: the case states stay those of RWB-P3-E1020-APP, and the contract only names them in `CaseStateChanged`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| TechX, service team | Authors and publishes the documents, the schemas and the fakes |
| RW-REFADM, reference data administrator | Confirms the list values the schemas refer to (outcome enumeration, case status, assignment reason) |
| Process owner for L1 18, Shared operations | Approves the behaviour the contract describes; no delegation of authority level applies |
| Consumers (gateway-bff, screens, contract tests) | Read the published documents; may raise a gap, not change a published version |
| P7 rwb-decision | Owns the rule-model operation the document consumes |
| Every caller of the four REST operations | Passes the rwb-access authorise check (DP-08) before the operation runs; a refused call returns MSG-P4-002 |

### 11. Data

| Item | Schema element | Read or write | Note | BR Field ID |
|---|---|---|---|---|
| Case identity | `caseId`, `caseNo` | Described | Case number format RW-YYYY-NNNNNN | Not specified in the source documents (DOR-RWB-P3-E1020-CON-7) |
| Queue and team | `queueId`, `queueCode`, `teamCode`, `roleCode` | Described | Queue data is reference data of rwb-case | Not specified in the source documents (DOR-RWB-P3-E1020-CON-7) |
| Owner | `ownerUserId` | Described | Never a name, never an email | Not specified in the source documents (DOR-RWB-P3-E1020-CON-7) |
| Case status | `status` | Described | LOV-CASE-STATUS | Not specified in the source documents (DOR-RWB-P3-E1020-CON-7) |
| Allocation outcome | `outcome`, `reason` | Described | ASSIGNED, OVERFLOW, EXCEPTION, DEVIATION_QUEUE, SKIPPED, FAILED_LOG | Not specified in the source documents (DOR-RWB-P3-E1020-CON-7) |
| Rule identity | `ruleId`, `ruleVersion`, `packageCode`, `packageVersion` | Described | Version label such as ALLOC-2026.11 | Not specified in the source documents (DOR-RWB-P3-E1020-CON-7) |
| Assignment record | `reason` of the assignment | Described | LOV-ASSIGN-REASON: ALLOCATION, TRANSFER, REBALANCE, MANUAL, ESCALATION | Not specified in the source documents (DOR-RWB-P3-E1020-CON-7) |
| Task | `taskId`, `taskCode`, `status`, `dueAt`, `outcomeCode` | Described | LOV-TASK-STATUS | Not specified in the source documents (DOR-RWB-P3-E1020-CON-7) |
| Idempotency | `Idempotency-Key`, stored response | Described | Stored by the platform library, key caseId and business date | Not specified in the source documents (DOR-RWB-P3-E1020-CON-7) |

The contract carries identifiers and facts only. It carries no personal data, no document content and no free text beyond a comment field on the task update. The caseload cap appears in the assignment outputs; whether its value comes from a parameter row or from reference data is Not specified in the source documents (GAP-0685; ASM-1232), so the schema names the field and does not fix its source or its value.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Document |
|---|---|---|---|
| POST | /api/recovery/case/v1/queues/{queueId}/placements | P3 rwb-case | OpenAPI 3.1, Idempotency-Key required, 202 accepted with the outcome |
| GET | /api/recovery/case/v1/queues/{queueId}/cases | P3 rwb-case | OpenAPI 3.1, paged list of case summaries |
| GET | /api/recovery/case/v1/me/tasks | P3 rwb-case | OpenAPI 3.1, the caller's open tasks |
| PATCH | /api/recovery/case/v1/tasks/{taskId} | P3 rwb-case | OpenAPI 3.1, status update with outcome code |

#### 12.2 REST operations consumed

| Operation | Path | Owner | Document |
|---|---|---|---|
| GET | /api/recovery/decision/v1/rule-models/{n}/{v} | P7 rwb-decision | Rule-model response schema, checksum verification, 2 s timeout, one retry |

#### 12.3 Events published

| Event name | Topic | Key | Schema |
|---|---|---|---|
| rwb.case.CaseAllocated.v1 | rwb.case.events.v1 | caseId | AsyncAPI 3 message, caseId, queueId, ownerId, ruleId, ruleVersion |
| rwb.case.CaseAllocationFailed.v1 | rwb.case.events.v1 | caseId | AsyncAPI 3 message, caseId, reason, ruleGap |
| rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | caseId | AsyncAPI 3 message, caseId, fromStatus, toStatus, ruleId, ruleVersion |

#### 12.4 Events consumed

| Event name | Topic | Owner | Schema impact |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | The placement read model is refreshed for the business date |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 rwb-decision | A new package version becomes the one the placement outcome names |

#### 12.5 Workflows and activities

| Item | Kind | Task queue | Owner | Contract artefact |
|---|---|---|---|---|
| CaseWorkflow | Parent workflow | rwb-case | P3 | Workflow input and output schemas of the contract pack |
| DailyCaseRun | Workflow started by schedule and by `AceDataReady` | rwb-case | P3 | Run summary schema: cases read, assigned, overflow, exception, failed, skipped |
| allocate | Activity | rwb-case | P3 | Activity interface schema: caseId and businessDate in, outcome out |
| transfer | Activity | rwb-case | P3 | Registered on the queue; interface owned by RWB-P3-E1021-CON |
| rebalance | Activity | rwb-case | P3 | Registered on the queue; interface owned by the E1-030 rebalancing contract |

#### 12.6 Schedules

| Schedule | Cron (Asia/Bangkok) | Overlap policy | Owner | Contract artefact |
|---|---|---|---|---|
| DailyCaseRun | Date-based run after the business date is ready | SKIP | P3 rwb-case | Run input schema with businessDate; the exact expression is Not specified in the source documents (GAP-0686; ASM-1233) |
| JOB-06 rebalancing | 06:30 | SKIP | P3 rwb-case | Registered here; behaviour and interface owned by the E1-030 story |

#### 12.7 Tables owned

| Table | Schema | Owner | Role in the contract |
|---|---|---|---|
| recovery_case | rwb_case | P3 rwb-case | Source of the case summary fields |
| queue | rwb_case | P3 rwb-case | Source of queueCode, teamCode, roleCode, cap and overflow queue |
| queue_member | rwb_case | P3 rwb-case | Source of the owner candidate list |
| assignment | rwb_case | P3 rwb-case | Source of the assignment reason and rule IDs |
| parameter_catalog | rwb_case | P3 rwb-case | Source of the parameter keys the placement reads |
| parameter_value | rwb_case | P3 rwb-case | Source of the approved parameter values |
| lov_value | rwb_case | P3 rwb-case | Source of the enumerations the schemas publish |
| reference_row | rwb_case | P3 rwb-case | Source of the reference rows the placement reads |
| reference_version | rwb_case | P3 rwb-case | Source of the reference version labels |
| outbox_event | rwb_case | PLT (library object in the service schema) | Producer side of the three events |

#### 12.8 Contract fakes

| Fake | Contract | Used for |
|---|---|---|
| rwb-decision rule-model fake | GET /api/recovery/decision/v1/rule-models/{n}/{v} | Returns package ALLOCATION "ALLOC-2026.11" and package ASSIGNMENT "ASSIGN-2026.11" with the ordered rows and the checksum |
| rwb-decision decision-record fake | rwb.decision-record.v1 | Accepts a decision record and answers with a ledger reference |
| rwb-source-data event fake | rwb.source-data.events.v1 | Publishes `AceDataReady` for a business date, including a duplicate |
| ACE notification path fake | ACE Common notification (INT-34) | Captures the allocation summary; ACE Common is outside the 19 services and has no ownership row |

The fake and sandbox credentials use the rwb-case login (DP-02); its name is Not specified in the source documents (GAP-0684; ASM-1231).

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 1 consumed | Four operations documented under `/api/recovery/case/v1`; one rule-model read from rwb-decision |
| Kafka | 3 published, 2 consumed | Three events on `rwb.case.events.v1`; consumes `AceDataReady` and `RulePackageInForce` |
| Temporal | 2 workflows, 3 activities | CaseWorkflow and DailyCaseRun; allocate, transfer, rebalance on queue rwb-case |
| File | None | No file contract in this story |

### 13. Solution plan

**Deliverables.** One OpenAPI 3.1 file for the four operations; one AsyncAPI 3 file for the three events; one JSON Schema set for RuleResult and the rule model; one problem-details schema; one versioning and compatibility note; the nine tables of section 12 in the contract pack.

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Draft the operation list from the rwb-case operation set and the legacy contract section; agree it with the screen consumers and gateway-bff.
2. Write the request and response schemas, including the outcome enumeration and the assignment reason list.
3. Write the AsyncAPI messages for the three events with examples that carry IDs only.
4. Write the RuleResult and rule-model schemas, with the checksum field and the ordered rows.
5. Write the problem-details envelope and map the legacy message identifiers that still apply.
6. Write the versioning and compatibility note; set the published files read only and add the hash check to the pipeline.
7. Generate the fakes and the contract tests; run them in the build.
8. Publish the contract pack with the nine tables of section 12.

**Feature flag.** None. The contract is published on Day 1 and the build story is what sits behind `rwb.case.allocation`.

**Done when.** The documents validate against OpenAPI 3.1 and AsyncAPI 3; the registry accepts the three event schemas as BACKWARD compatible; the contract tests run green against the fakes; the nine contract tables are published; the review by the consuming teams and by the process owner is recorded.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role lacks the right for the operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P3-013 | The decision record could not be written | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| MSG-P3-027 | A reference data or rule version load fails a check (schema, valid from in the past, duplicate key, removed product with open cases, overlap, unreachable or default row, test cases), or no version is in force for a table an engine needs (RWB-E1-073, RWB-E1-043, RWB-E1-025) | The {table} load was refused: {check}. The version in force is unchanged. |

The contract publishes the identifier and the text of each message, and the response schema that carries it. Thai text follows decision DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863) and is part of the published message catalogue.

No-access state of screen SCR-02: the screen shows MSG-P4-002 when a role lacks the right for the operation.

### 15. Screens and states

The contract serves two screens without owning either: SCR-02 Case list (states Loading; empty; list; error, Not specified in the source documents (CG-ALL-3540); no access, stated below) through `GET /queues/{queueId}/cases`, and the my-work view of the officer (states Loading; empty; list; error) through `GET /me/tasks`. The task update screen state (saving; saved; conflict; error) is driven by `PATCH /tasks/{taskId}`. Both screens are reached through the gateway-bff composite route (DP-19); the contract fixes only the payloads and the error envelope, not the layout.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1020-CON-01 | AC1 | Contract | The OpenAPI 3.1 file; a validator run; the four paths and their request and response schemas |
| TC-P3-E1020-CON-02 | AC2 | Contract | The AsyncAPI 3 file; the three messages; a registry compatibility run against the previous version |
| TC-P3-E1020-CON-03 | AC3 | Contract | The RuleResult and rule-model schemas; a model response with packageCode, packageVersion, checksum and ordered rows |
| TC-P3-E1020-CON-04 | AC4 | Component | The problem-details schema; the Idempotency-Key header; a replayed POST with the same key |
| TC-P3-E1020-CON-05 | AC5 | Component | A published document and a proposed breaking change; the hash check; a refused event schema |
| TC-P3-E1020-CON-06 | AC6 | Component | The nine contract tables; the owner column checked against the ownership map; the generated fakes |
| TC-P3-E1020-CON-07 | AC6 | Component | The ten tables of section 12.7; the first and last row of each table; the owner column checked against the ownership map at each boundary |
| TC-P3-E1020-CON-09 | AC7 | Component | The nine business rules of section 8; each rule checked against the published element that carries it; a guardrail check or a boundary test where the rule is an architecture constraint |

### 17. Guardrails

- **G1 No business value in the contract.** Queue codes, rule IDs, package versions, caps, methods and parameters appear as examples or as fields, never as fixed constants in a schema.
- **G2 No personal data.** No name, address, contact point or identity number in any example, event or schema; identifiers only.
- **G3 No other service's tables.** The rule model is described as an operation of rwb-decision, never as a table of rwb_decision.
- **G4 One published version at a time.** A published document is read only; the pipeline fails on a changed hash.
- **G5 The schema names the source of a value, not the value.** Where a source is unknown the placeholder is used, so the build story decides with a gap row.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 18.3.2 | R-DEV-01 | TC-P3-E1020-CON-01, TC-P3-E1020-CON-06, TC-P3-E1020-CON-07 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07, FEAT-CWC-09 | 18.3.2 | R-UNI-41 | TC-P3-E1020-CON-02, TC-P3-E1020-CON-03 |
| REQ-CWC-009 | Round robin, lowest load, named owner, cap and overflow | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-08 | 18.3.2 | R-UNI-19 | TC-P3-E1020-CON-01, TC-P3-E1020-CON-03 |
| REQ-CWC-016 | Every allocation logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 6.1 | R-UNI-39, R-UNI-40 | TC-P3-E1020-CON-04, TC-P3-E1020-CON-05 |

Legacy trace: story RWB-E1-020, contract section; the legacy `AllocationService`, `AllocationOutcome`, `OutcomeType`, `RuleEvaluator` and `RuleResult` interfaces are the source of the published shapes.

### 19. Out of scope

- The engine implementation and its tests (RWB-P3-E1020-APP).
- The deployment of the worker, the schedule and the topics (RWB-P3-E1020-OPS).
- The rule-model governance operations of rwb-decision beyond the consumed read (P7 owns them).
- The transfer and rebalancing contracts (RWB-P3-E1021-CON and the E1-030 rebalancing contract).
- The gateway routes and the screen composition themselves (RWB-PLT-N001-CON and the screen stories).
