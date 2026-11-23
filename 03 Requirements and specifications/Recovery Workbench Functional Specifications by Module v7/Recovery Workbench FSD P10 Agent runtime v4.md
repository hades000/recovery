SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P10 Agent runtime

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P10 Agent runtime |
| Document ID | P10-RWB-FSD-v4 |
| Service | `rwb-agent` (Agent) |
| Version | 4 |
| Status | Draft |
| Classification | Confidential |
| Date | 15 November 2026 |
| Change note | v3, 15 November 2026: re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only. Everything else unchanged from v2. |
| FSD owner | Business analyst, P10 |
| Business owner | Business lead |
| Change | 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Module code | Module name | First in |
|---|---|---|
| P10 | Agent runtime | E1 shadow; E2 L1 |

**Feature scope.** Orchestrator, tool gateway, guardrails, prompt store, evaluation, autonomy levels.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P10 Agent runtime | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |

### Note, Architecture v5 (D-RCV-60)

| Item | Value |
|---|---|
| Service | `rwb-agent` (Agent) |
| Owns in Architecture v5 | agent policies, prompts, runs, guardrails, evaluations |
| Service epic | `RWB-SVC-P10` |
| Wave | 1 |
| Schema | `rwb_agent` |
| REST base | `/api/recovery/agent/v1` |
| Kafka topic | `rwb.agent.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.agent.<Event>.v1` |
| Temporal task queue | `rwb-agent` |
| Java package | `th.co.scb.ace.workbench.recovery.agent` |

Version 4 adds the Service row, the Change row and this note above; nothing else in this document changes. Under Architecture v5 the module is delivered as the service `rwb-agent` of the 19 services inside ACE (ADR-013), with its own schema `rwb_agent` and login (ADR-014), in wave 1, service epic `RWB-SVC-P10`; the realignment is D-RCV-60 (DL44), and DL46 keeps team-type ownership soft. The functional content of this document is the content of version 3, kept word for word: every feature, requirement, rule, field, list, message, screen, count and date.

Every owner named in this document is the owner recorded in the Microservice Ownership Map v1, and where the map carries a ruling of Template and Rules §R3 the ruling is followed: parameters and reference data with `rwb-case` (DP-06, DP-07), the rule package registry with `rwb-decision` (DP-04), the interaction ledger with `rwb-source-data` (DP-18) and feature flags with the platform library. Where this document names a table, endpoint, event, job, workflow or screen that the map gives to another service, that service owns it and this module reaches it only through the owner's contract (DP-01, DP-11; ADR-020).

The extracts, feeds and copies this document addresses to a data lake are removed by Architecture v5: reporting reads events into `rwb-reporting` (DP-17, ADR-018). The wording of those extracts is kept as written and carried by GAP-1861.

Release dates stay as written and are tentative (DL48). No approval of version 4 is recorded (ASM-3046); the version is Draft.

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the P3 interfaces |
| Notification path | REUSE | ACE notification path | Recovery templates only |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from P3 |
| Decision record and audit trail | REUSE | Audit and Logging Design | Writes through P7 |
| Attachments and evidence | REUSE | Document Management Design | Through P5 |
| Role and permission matrix | REUSE | Users Roles and Permissions | Capability areas from P4 |
| Restructure calculator | REUSE | ACE common module | Not used |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** Orchestrator, tool gateway, guardrails, prompt store, evaluation, autonomy levels.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-AGT-01; FEAT-AGT-03; FEAT-AGT-05; FEAT-AGT-06; FEAT-AGT-07; FEAT-AGT-12; FEAT-CWC-22; FEAT-DCM-09

**Constraints.** Built in the ACE service as part of the recovery module; source data read only from the ACE database through the SELECT-only `recovery.v_ace_*` views, landed by ACE's own ingestion, with no inbound load in the Workbench (D-RCV-35); every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P10 | FEAT-AGT-01 | Set up the agent platform with the gateway and prompt store | System | Sets up the agent runtime, the model gateway, the prompt and policy store and the tool gateway. | E1 | A2.1 |
| P10 | FEAT-AGT-02 | Run the guardrail checker on every agent output | System | Tests every agent answer against the schema, the allowed action list and the confidence threshold. | E1 | A2.2 |
| P10 | FEAT-AGT-03 | Run the case intake agent in shadow | System | Runs the intake agent on 200 cases with its answers recorded and not acted on. | E1 | A2.3 |
| P10 | FEAT-AGT-04 | Evaluate document extraction quality | System | Measures extraction accuracy against the reviewed set, which sets the confidence threshold. | E1 | A2.4 |
| P10 | FEAT-AGT-05 | Run the agent evaluation harness | System | Scores each agent against a fixed set before any autonomy change. | E1 | A2.5 |
| P10 | FEAT-AGT-06 | Publish the agent monitoring dashboard | User | Shows acceptance, override, latency and cost per agent. | E1 | A2.6 |
| P10 | FEAT-AGT-07 | Run the case intake agent at L1 | System | Puts the intake agent live at autonomy level 1, with its summaries visible and acceptance measured. | E2 | A2.7 |
| P10 | FEAT-AGT-08 | Run the deviation screening agent at L1 | System | Puts the screening agent live on one segment at autonomy level 1. | E2 | A2.8 |
| P10 | FEAT-AGT-09 | Run the legal document agent in shadow | System | Runs the legal document agent against Epic 1 data with its output recorded and not acted on. | E2 | A2.9 |
| P10 | FEAT-AGT-10 | Expose the TDR offer-suggestion model through the gateway | System | Serves the Enterprise AI TDR model through the model gateway, if the TDR team has built it. | E2 | A2.10 |
| P10 | FEAT-AGT-11 | Fall back to the rule result when an agent is unavailable | System | Uses the rule answer and continues when the agent does not reply inside the timeout, and records the fallback. | E1 | A2.11 |
| P10 | FEAT-AGT-12 | Change an autonomy level | Admin | Changes the autonomy level for one agent and one decision, as a versioned configuration row. | E3 | A2.12 |
| P10 | FEAT-AGT-13 | Detect model drift and raise a decision | System | Watches calibration and drift, and raises a decision with an owner and a date on a breach. | E3 | A2.13 |
| P10 | FEAT-AGT-14 | Run a champion and challenger test | Admin | Runs two rule or model versions side by side and compares the outcome. | E8 | A2.14 |
| P10 | FEAT-AGT-15 | Raise or lower an autonomy level with approval | Admin | Steps an agent up on measured evidence, and drops it on a breach, with the approval each needs. | E8 | A2.15 |
| P10 | FEAT-AGT-16 | Review agent risk at the committee | User | Puts agent performance, overrides and incidents in front of the strategy and model committee. | E8 | A2.16 |

### A1.3 Background

Officers gather and check facts by hand before every decision.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Set up the agent platform with the gateway and prompt store

#### A2.1.1 Intent

**Business objective.** Sets up the agent runtime, the model gateway, the prompt and policy store and the tool gateway.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Sets up the agent runtime, the model gateway, the prompt and policy store and the tool gateway.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Set up the agent platform with the gateway and prompt store | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway, ACE

**Prerequisites.** None

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-001-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-001-01 | Approved endpoint | the approved model endpoint on the private endpoint of the SCB tenant | the orchestrator runs agent "ECHO" for case "RW-2026-000101" | the call succeeds with run status "ANSWERED" And one agent run row holds agent "ECHO", policy version "P1", prompt version "PR1", model version "MODEL-A-2026-10", latency 1,200 ms, tokens in 900, tokens out 150 and cost 0.0525 baht And one AgentRunCompleted event is written to the outbox with the run ID, agent "ECHO", the case ID, outcome "ANSWERED" and fallback false | RWB-E1-058 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-001-01 | Prompt versions | prompt version "PR1" is in force for agent "ECHO" | RW-COE loads prompt version "PR2" and RW-RISK approves it with valid from 2026-11-20 | prompt version "PR2" exists with status "APPROVED" And prompt version "PR1" stays readable through GET /admin/agent-configs with its text hash unchanged And a run on 2026-11-19 uses "PR1" and a run on 2026-11-20 uses "PR2" | RWB-E1-058 |
| AC-ALT-P10-001-02 | Schema check | the model stub returns an answer with field "summary" missing from the output schema of "ECHO" | the guardrail runs | the output is rejected with run status "GUARDRAIL_FAILED" and fallback true And the guardrail result holds check code "SCHEMA" with the missing field name And the count of check code "SCHEMA" failures for "ECHO" on the business date rises by 1 | RWB-E1-058 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-001-01 | The model does not answer inside the timeout | the model stub does not answer for 61 seconds | the orchestrator runs agent "ECHO" for case "RW-2026-000102" | the call is ended at 60 seconds And the agent run holds status "TIMED_OUT", fallback true and latency 60,000 ms And the orchestrator returns a fallback result with reason "TIMED_OUT" (R-UNI-32) | RWB-E1-058 |
| AC-EXC-P10-001-02 | A configuration file that fails a check is refused | a policy file for agent "ECHO" with timeout_seconds 0 | RW-COE loads it through POST /admin/agent-configs | the load is refused with 422 and MSG-P10-001 naming check "timeout_seconds between 1 and 120" And policy version "P1" stays in force and no new version row exists | RWB-E1-058 |
| AC-EXC-P10-001-03 | The loader cannot approve their own version | user "coe.user01" loaded policy version "P2" for agent "ECHO" | user "coe.user01" calls POST /admin/agent-configs/{versionId}/approve for "P2" | the approval is refused with 409 and MSG-P7-002 And version "P2" keeps status "LOADED" | RWB-E1-058 |
| AC-EXC-P10-001-04 | A repeated run request has no further effect | agent "ECHO" ran for case "RW-2026-000101" with idempotency key "ECHO:RW-2026-000101:2026-11-30" | the same request arrives again with the same key | no second agent run row and no second model call exist And the first result is returned and the idempotency hit is counted (R-UNI-40) | RWB-E1-058 |
| AC-EXC-P10-001-05 | An evaluation on an empty sample is refused | sample "ECHO-S2" has 0 labeled rows for agent "ECHO" | RW-COE starts the evaluation of "ECHO" on "ECHO-S2" | the request is refused with 422 and MSG-P10-002 And no evaluation run and no agent run row exist | RWB-E1-058 |
| AC-EXC-P10-001-06 | A second evaluation while one is running is refused | the evaluation of "ECHO" on "ECHO-S1" version 1 has status "RUNNING" | RW-COE starts the same evaluation again | the request is refused with 409 and MSG-P10-003 And one evaluation run exists for "ECHO" on "ECHO-S1" version 1 with status "RUNNING" | RWB-E1-058 |
| AC-EXC-P10-001-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-001-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Run the guardrail checker on every agent output

#### A2.2.1 Intent

**Business objective.** Tests every agent answer against the schema, the allowed action list and the confidence threshold.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Tests every agent answer against the schema, the allowed action list and the confidence threshold.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the guardrail checker on every agent output | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway

**Prerequisites.** FEAT-AGT-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-002-1 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| BR-P10-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Risk and model risk officer | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-002-01 | Approved endpoint | the approved model endpoint on the private endpoint of the SCB tenant | the orchestrator runs agent "ECHO" for case "RW-2026-000101" | the call succeeds with run status "ANSWERED" And one agent run row holds agent "ECHO", policy version "P1", prompt version "PR1", model version "MODEL-A-2026-10", latency 1,200 ms, tokens in 900, tokens out 150 and cost 0.0525 baht And one AgentRunCompleted event is written to the outbox with the run ID, agent "ECHO", the case ID, outcome "ANSWERED" and fallback false | RWB-E1-058 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-002-01 | Prompt versions | prompt version "PR1" is in force for agent "ECHO" | RW-COE loads prompt version "PR2" and RW-RISK approves it with valid from 2026-11-20 | prompt version "PR2" exists with status "APPROVED" And prompt version "PR1" stays readable through GET /admin/agent-configs with its text hash unchanged And a run on 2026-11-19 uses "PR1" and a run on 2026-11-20 uses "PR2" | RWB-E1-058 |
| AC-ALT-P10-002-02 | Schema check | the model stub returns an answer with field "summary" missing from the output schema of "ECHO" | the guardrail runs | the output is rejected with run status "GUARDRAIL_FAILED" and fallback true And the guardrail result holds check code "SCHEMA" with the missing field name And the count of check code "SCHEMA" failures for "ECHO" on the business date rises by 1 | RWB-E1-058 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-002-01 | The model does not answer inside the timeout | the model stub does not answer for 61 seconds | the orchestrator runs agent "ECHO" for case "RW-2026-000102" | the call is ended at 60 seconds And the agent run holds status "TIMED_OUT", fallback true and latency 60,000 ms And the orchestrator returns a fallback result with reason "TIMED_OUT" (R-UNI-32) | RWB-E1-058 |
| AC-EXC-P10-002-02 | A configuration file that fails a check is refused | a policy file for agent "ECHO" with timeout_seconds 0 | RW-COE loads it through POST /admin/agent-configs | the load is refused with 422 and MSG-P10-001 naming check "timeout_seconds between 1 and 120" And policy version "P1" stays in force and no new version row exists | RWB-E1-058 |
| AC-EXC-P10-002-03 | The loader cannot approve their own version | user "coe.user01" loaded policy version "P2" for agent "ECHO" | user "coe.user01" calls POST /admin/agent-configs/{versionId}/approve for "P2" | the approval is refused with 409 and MSG-P7-002 And version "P2" keeps status "LOADED" | RWB-E1-058 |
| AC-EXC-P10-002-04 | A repeated run request has no further effect | agent "ECHO" ran for case "RW-2026-000101" with idempotency key "ECHO:RW-2026-000101:2026-11-30" | the same request arrives again with the same key | no second agent run row and no second model call exist And the first result is returned and the idempotency hit is counted (R-UNI-40) | RWB-E1-058 |
| AC-EXC-P10-002-05 | An evaluation on an empty sample is refused | sample "ECHO-S2" has 0 labeled rows for agent "ECHO" | RW-COE starts the evaluation of "ECHO" on "ECHO-S2" | the request is refused with 422 and MSG-P10-002 And no evaluation run and no agent run row exist | RWB-E1-058 |
| AC-EXC-P10-002-06 | A second evaluation while one is running is refused | the evaluation of "ECHO" on "ECHO-S1" version 1 has status "RUNNING" | RW-COE starts the same evaluation again | the request is refused with 409 and MSG-P10-003 And one evaluation run exists for "ECHO" on "ECHO-S1" version 1 with status "RUNNING" | RWB-E1-058 |
| AC-EXC-P10-002-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-002-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Run the case intake agent in shadow

#### A2.3.1 Intent

**Business objective.** Runs the intake agent on 200 cases with its answers recorded and not acted on.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Runs the intake agent on 200 cases with its answers recorded and not acted on.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the case intake agent in shadow | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway, Workbench

**Prerequisites.** FEAT-AGT-01

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-003-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-003-01 | Shadow run | 200 Epic 1 cases created between 2026-11-30 and 2026-12-04 | the agent runs on each CaseCreated event | 200 agent runs with mode "SHADOW" store a summary and gap flags And no case field, task, queue or decision log entry changes And GET /cases/{caseId} and GET /cases/{caseId}/timeline return no agent output And GET /admin/agent-runs returns the 200 runs without the summary or the gap flags | RWB-E1-059 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-003-01 | Agreement rate | the business analysts' review of the same 200 cases in sample "INTAKE-S1" version 1 | the comparison runs | one score row per gap type holds the agreement rate, precision, recall and sample size 200 And for MISSING_DOCUMENT with 182 agreeing cases the agreement rate is 0.9100 And each score row holds policy "P1", prompt "PR1" and the model version | RWB-E1-059 |
| AC-ALT-P10-003-02 | A new case starts one shadow run | case "RW-2026-000301" is created on 2026-11-30 | EV-01 CaseCreated is processed | one agent run exists with key "INTAKE:<caseId>:2026-11-30", trigger "CaseCreated" and mode "SHADOW" | RWB-E1-059 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-003-01 | A failed run is counted and not retried | the model stub does not answer for case "RW-2026-000302" | the agent runs | the run holds status "TIMED_OUT" and fallback true And no second run is made for that event And the failure count for type "TIMED_OUT" on 2026-11-30 is 1 | RWB-E1-059 |
| AC-EXC-P10-003-02 | A repeated event has no further effect | EV-01 CaseCreated for case "RW-2026-000301" was processed on 2026-11-30 | the same event arrives again with the same event ID | one agent run exists for the case and date and the repeat is counted (R-UNI-40) | RWB-E1-059 |
| AC-EXC-P10-003-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-003-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Evaluate document extraction quality

#### A2.4.1 Intent

**Business objective.** Measures extraction accuracy against the reviewed set, which sets the confidence threshold.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Measures extraction accuracy against the reviewed set, which sets the confidence threshold.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Evaluate document extraction quality | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway

**Prerequisites.** FEAT-DCM-09

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-004-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Center of excellence analyst | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-004-01 | Scores per field | the labeled sample | the three approaches run | one score row exists per field and approach: 3 fields x 3 approaches for "COURT_NOTICE" And for field hearing_date with approach OCR_TEMPLATE, 34 true positives, 2 false positives and 4 false negatives give precision 0.9444 and recall 0.8947 And each score row holds the model version and the prompt version "PR1" where the approach calls the model | RWB-E1-060 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-004-01 | Decision recorded | the scores for "COURT_NOTICE" | the proposal is built | the evaluation run names, for "COURT_NOTICE", the approach with the highest mean F1 and its precision and recall per field And it names the proposed confidence threshold: the lowest confidence at which every chosen field reaches precision 0.95 And the export lists one row per document type for the solution architect's architecture decision | RWB-E1-060 |
| AC-ALT-P10-004-02 | A type with too few labels | type "TITLE_DEED" has 12 labeled documents | the evaluation runs | "TITLE_DEED" is scored and marked "insufficient sample" And no approach and no threshold are proposed for "TITLE_DEED" | RWB-E1-060 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-004-01 | A model failure counts against the model approaches | the model stub times out on document 7 of 40 | the approach MODEL runs | each labeled field of document 7 counts as a false negative for MODEL And the evaluation run holds failure count TIMED_OUT 1 | RWB-E1-060 |
| AC-EXC-P10-004-02 | A sample row for a document that does not exist | the sample file has a row for a document ID that the P5 interface does not return | RW-COE loads the file | the load is refused with 422 and MSG-P10-001 naming the row number And no row of the file is stored | RWB-E1-060 |
| AC-EXC-P10-004-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-004-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Run the agent evaluation harness

#### A2.5.1 Intent

**Business objective.** Scores each agent against a fixed set before any autonomy change.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Scores each agent against a fixed set before any autonomy change.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the agent evaluation harness | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway

**Prerequisites.** FEAT-AGT-01

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-005-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Risk and model risk officer | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-005-01 | Approved endpoint | the approved model endpoint on the private endpoint of the SCB tenant | the orchestrator runs agent "ECHO" for case "RW-2026-000101" | the call succeeds with run status "ANSWERED" And one agent run row holds agent "ECHO", policy version "P1", prompt version "PR1", model version "MODEL-A-2026-10", latency 1,200 ms, tokens in 900, tokens out 150 and cost 0.0525 baht And one AgentRunCompleted event is written to the outbox with the run ID, agent "ECHO", the case ID, outcome "ANSWERED" and fallback false | RWB-E1-058 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-005-01 | Prompt versions | prompt version "PR1" is in force for agent "ECHO" | RW-COE loads prompt version "PR2" and RW-RISK approves it with valid from 2026-11-20 | prompt version "PR2" exists with status "APPROVED" And prompt version "PR1" stays readable through GET /admin/agent-configs with its text hash unchanged And a run on 2026-11-19 uses "PR1" and a run on 2026-11-20 uses "PR2" | RWB-E1-058 |
| AC-ALT-P10-005-02 | Schema check | the model stub returns an answer with field "summary" missing from the output schema of "ECHO" | the guardrail runs | the output is rejected with run status "GUARDRAIL_FAILED" and fallback true And the guardrail result holds check code "SCHEMA" with the missing field name And the count of check code "SCHEMA" failures for "ECHO" on the business date rises by 1 | RWB-E1-058 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-005-01 | The model does not answer inside the timeout | the model stub does not answer for 61 seconds | the orchestrator runs agent "ECHO" for case "RW-2026-000102" | the call is ended at 60 seconds And the agent run holds status "TIMED_OUT", fallback true and latency 60,000 ms And the orchestrator returns a fallback result with reason "TIMED_OUT" (R-UNI-32) | RWB-E1-058 |
| AC-EXC-P10-005-02 | A configuration file that fails a check is refused | a policy file for agent "ECHO" with timeout_seconds 0 | RW-COE loads it through POST /admin/agent-configs | the load is refused with 422 and MSG-P10-001 naming check "timeout_seconds between 1 and 120" And policy version "P1" stays in force and no new version row exists | RWB-E1-058 |
| AC-EXC-P10-005-03 | The loader cannot approve their own version | user "coe.user01" loaded policy version "P2" for agent "ECHO" | user "coe.user01" calls POST /admin/agent-configs/{versionId}/approve for "P2" | the approval is refused with 409 and MSG-P7-002 And version "P2" keeps status "LOADED" | RWB-E1-058 |
| AC-EXC-P10-005-04 | A repeated run request has no further effect | agent "ECHO" ran for case "RW-2026-000101" with idempotency key "ECHO:RW-2026-000101:2026-11-30" | the same request arrives again with the same key | no second agent run row and no second model call exist And the first result is returned and the idempotency hit is counted (R-UNI-40) | RWB-E1-058 |
| AC-EXC-P10-005-05 | An evaluation on an empty sample is refused | sample "ECHO-S2" has 0 labeled rows for agent "ECHO" | RW-COE starts the evaluation of "ECHO" on "ECHO-S2" | the request is refused with 422 and MSG-P10-002 And no evaluation run and no agent run row exist | RWB-E1-058 |
| AC-EXC-P10-005-06 | A second evaluation while one is running is refused | the evaluation of "ECHO" on "ECHO-S1" version 1 has status "RUNNING" | RW-COE starts the same evaluation again | the request is refused with 409 and MSG-P10-003 And one evaluation run exists for "ECHO" on "ECHO-S1" version 1 with status "RUNNING" | RWB-E1-058 |
| AC-EXC-P10-005-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-005-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Publish the agent monitoring dashboard

#### A2.6.1 Intent

**Business objective.** Shows acceptance, override, latency and cost per agent.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Shows acceptance, override, latency and cost per agent.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Risk and model risk officer | Opens the screen and publish the agent monitoring dashboard | Checks the role, the capability area and the scope |
| 2 | Risk and model risk officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Power BI, Model gateway

**Prerequisites.** FEAT-AGT-05

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-006-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P10-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| agent_policy.agent_code | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER | varchar(30) | Yes | LOV-AGENT | No |
| agent_policy.policy_version | Policy version, for example P1 | varchar(20) | Yes | None | No |
| agent_policy.model_code | Model deployment the agent calls through the gateway | varchar(40) | Yes | None | No |
| agent_policy.model_version | Model version the policy uses | varchar(40) | Yes | None | No |
| agent_policy.output_schema_ref | Reference to the JSON Schema the answer must meet | varchar(400) | Yes | None | No |
| agent_policy.allowed_tools | Tools the agent may call through the tool gateway | jsonb | No | None | No |
| agent_policy.autonomy_mode | Off, shadow or L1 | varchar(10) | Yes | LOV-AUTONOMY | No |
| agent_policy.segment_product_group | Product group the mode applies to; empty for all | varchar(15) | No | LOV-PRODUCT | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| Risk and model risk officer | Primary |
| Center of excellence analyst, Reporting and BI analyst | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-006-01 | Per agent | two agents in shadow | the dashboard opens for 2026-12-01 | each agent shows runs, fallback rate, median and 95th percentile latency, cost and the latest evaluation score by policy and prompt version And "INTAKE" shows 120 runs and fallback rate 0.0750 And acceptance and override show "no L1 runs" for both agents, because no agent runs at L1 in Epic 1 | RWB-E1-063 |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-006-01 | Alert | cost above the daily parameter for "SCREENING" | JOB-15 completes for 2026-12-01 | one agent alert row exists for "SCREENING", type "COST_CAP", date 2026-12-01, measured 2,310.5000 and threshold 2,000 And MSG-P10-004 is sent to the holders of RW-COE and RW-RISK through the notification path And no alert exists for "INTAKE" | RWB-E1-063 |
| AC-ALT-P10-006-02 | A rerun for the same date | JOB-15 completed for 2026-12-01 and sent the "SCREENING" alert | RW-PLATADM reruns JOB-15 for 2026-12-01 | agent_run_daily holds the same 2 rows for 2026-12-01 And no second alert row or notification exists | RWB-E1-063 |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-006-01 | A copy that does not match is held | the data lake write for 2026-12-01 stores 1 row for 2 agent and version groups | the count check runs | the publish for 2026-12-01 is held and the report shows 2026-11-30 And the step reports failed in GET /admin/jobs and the data steward is alerted | RWB-E1-063 |
| AC-EXC-P10-006-02 | An agent with no runs | agent "EXTRACT" has an approved policy and no runs on 2026-12-01 | JOB-15 completes for 2026-12-01 | "EXTRACT" shows runs 0 and cost 0.0000 for 2026-12-01 and no alert | RWB-E1-063 |
| AC-EXC-P10-006-03 | The notification path is down | the P6 notification interface is unavailable at 01:40 | the "SCREENING" alert is raised | the alert row is kept with sent_at empty And it is sent when the outbox sender succeeds (R-UNI-33, R-UNI-35) | RWB-E1-063 |
| AC-EXC-P10-006-04 | Not enough feedback | "SCREENING" for MORTGAGE and BKK has 12 feedback entries in the week to 2026-12-14 | the check runs | no drift alert is raised for that segment and the screen shows "not enough feedback" | RWB-E2-031 |
| AC-EXC-P10-006-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-006-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Run the case intake agent at L1

#### A2.7.1 Intent

**Business objective.** Puts the intake agent live at autonomy level 1, with its summaries visible and acceptance measured.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Puts the intake agent live at autonomy level 1, with its summaries visible and acceptance measured.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the case intake agent at L1 | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway

**Prerequisites.** FEAT-AGT-03

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-007-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-007-01 | Report | the shadow results | the report is written | it holds sample size 200, the agreement rate per gap type, failure counts 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR And it holds total cost 412.6000 baht, cost per case 2.0630 baht, median latency 4,100 ms and 95th percentile 9,800 ms And it holds policy "P1", prompt "PR1" and the model version, and no personal field | RWB-E1-061 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-007-01 | Proposal | the report | RW-COE loads policy "INTAKE" version "P2" with mode "L1", evaluation run "EV-INTAKE-001", conditions "agreement at least 0.85 for every gap type", fallback "rule result per R-UNI-32" and measures "acceptance, correction rate, fallback rate below 0.10" | version "P2" is stored with status "LOADED" and holds the conditions, the fallback and the measures to watch And "P1" stays in force until RW-RISK approves "P2" | RWB-E1-061 |
| AC-ALT-P10-007-02 | Report on an unfinished evaluation | evaluation run "EV-INTAKE-002" has status "RUNNING" | RW-COE requests its report | the request is refused with 409 and MSG-P10-008 | RWB-E1-061 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-007-01 | The loader cannot approve the proposal | user "coe.user01" loaded version "P2" | user "coe.user01" approves "P2" | the approval is refused with 409 and MSG-P7-002 | RWB-E1-061 |
| AC-EXC-P10-007-02 | The decision cannot be recorded | the decision log writer fails | "owner.user07" chooses Accept | the request is refused with 503 and MSG-P7-003 And no agent_feedback row exists for the run and the controls stay on the panel | RWB-E2-028 |
| AC-EXC-P10-007-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-007-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Run the deviation screening agent at L1

#### A2.8.1 Intent

**Business objective.** Puts the screening agent live on one segment at autonomy level 1.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Puts the screening agent live on one segment at autonomy level 1.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the deviation screening agent at L1 | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway

**Prerequisites.** FEAT-AGT-07

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-008-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Conduct and QA officer | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-008-01 | Shadow flags | 200 cases with their call notes and documents | the agent runs | each run stores its proposed codes with reasons and source references in mode "SHADOW" And no deviation record exists, deviation_open stays false on every case and no contact stop is set And no user-facing endpoint returns a proposal | RWB-E1-062 |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-008-01 | Compared | the business analysts' flags for the same 200 cases in sample "SCREEN-S1" version 1 | the comparison runs | one score row per code X1 to X7 holds precision, recall and sample size 200 And for X6 with 18 true positives, 2 false positives and 6 false negatives precision is 0.9000 and recall is 0.7500 | RWB-E1-062 |
| AC-ALT-P10-008-02 | A new document starts a run | open case "RW-2026-000401" receives a document of type "DEATH_CERTIFICATE" | EV-16 DocumentStored is processed | one shadow run exists with key "SCREENING:<caseId>:<eventId>" and trigger "DocumentStored" | RWB-E1-062 |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-008-01 | A repeated event | EV-16 for document "D-1001" on case "RW-2026-000401" was processed | the same event ID arrives again | one run exists for the case and event and the repeat is counted (R-UNI-40) | RWB-E1-062 |
| AC-EXC-P10-008-02 | The rejection cannot be recorded | the decision log writer fails | the owner rejects X6 with a reason | the request is refused with 503 and MSG-P7-003 and no agent_feedback row exists | RWB-E2-029 |
| AC-EXC-P10-008-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-008-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Run the legal document agent in shadow

#### A2.9.1 Intent

**Business objective.** Runs the legal document agent against Epic 1 data with its output recorded and not acted on.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Runs the legal document agent against Epic 1 data with its output recorded and not acted on.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the legal document agent in shadow | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway

**Prerequisites.** FEAT-AGT-01

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-009-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Litigation officer | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-009-01 | Shadow pack | litigation case "RW-2026-000901" with 14 documents and an open legal action | the agent runs | a pack listing document IDs for each of the 9 items and a completeness list with PRESENT, MISSING or DEFECT per item are stored on the agent run And no document, legal action, task or case field changes And no user-facing endpoint returns the pack | RWB-E2-030 |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-009-01 | Scored | 50 shadow packs for sample "LEGAL-S1" version 1 | the evaluation runs | agreement with the officers' packs is stored per item with sample size 50 And for "DEMAND_NOTICE_PROOF" with 46 agreeing cases the agreement rate is 0.9200 | RWB-E2-030 |
| AC-ALT-P10-009-02 | Promotion proposal | the score | RW-COE loads policy "LEGAL_DOC" version "P2" with mode "SHADOW", review date 2027-03-15 and the evaluation run ID, and RW-RISK approves it | the decision to keep shadow is recorded on version "P2" with the approver and the approval date And a proposal with mode "L1" is accepted only when every stated condition is met by the evaluation | RWB-E2-030 |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-009-01 | The document interface is down | the P5 document interface is unavailable for case "RW-2026-000903" | the agent runs | the run holds status "TOOL_UNAVAILABLE" and fallback true And the evaluation lists the case as not run and scores 49 cases | RWB-E2-030 |
| AC-EXC-P10-009-02 | The loader cannot approve | user "coe.user01" loaded version "P2" | user "coe.user01" approves it | the approval is refused with 409 and MSG-P7-002 | RWB-E2-030 |
| AC-EXC-P10-009-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-009-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Expose the TDR offer-suggestion model through the gateway

#### A2.10.1 Intent

**Business objective.** Serves the Enterprise AI TDR model through the model gateway, if the TDR team has built it.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Serves the Enterprise AI TDR model through the model gateway, if the TDR team has built it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Expose the TDR offer-suggestion model through the gateway | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway, ACE and TDR

**Prerequisites.** FEAT-AGT-01

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-010-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Restructuring officer (FCR) | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-010-01 | Exposed | the model deployed by the TDR team with policy "TDR_OFFER" version "P2", mode "L1" and model version "TDR-OFFER-1.0" | the gateway calls it | the suggestion returns with 84 installments of 18,900.00 baht and model version "TDR-OFFER-1.0" And one agent run row and one decision log entry with decision "D5", model version "TDR-OFFER-1.0" and final call "SUGGESTION_RECORDED" are written | RWB-E2-032 |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-010-01 | Logged | a suggestion on treatment "T-1001" | the record is read | the decision log entry linked to the suggestion holds model version "TDR-OFFER-1.0", the inputs reference and the suggested terms And SCR-14 shows "Suggested by TDR_OFFER, version TDR-OFFER-1.0" | RWB-E2-032 |
| AC-ALT-P10-010-02 | The same treatment asks twice | a suggestion was recorded for treatment "T-1001" | the treatment service asks again for "T-1001" | the first suggestion and its decision log entry ID return and no second model call is made | RWB-E2-032 |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-010-01 | Not available | the model not yet built and policy "TDR_OFFER" version "P1" with mode "OFF" and review date 2027-02-28 | the treatment service asks for a suggestion | the gateway stub returns no suggestion and makes no model call And SCR-14 shows MSG-P10-007 and no decision log entry is written And GET /admin/agent-configs shows version "P1" with review date 2027-02-28 | RWB-E2-032 |
| AC-EXC-P10-010-02 | The model does not answer | the TDR model stub does not answer for 61 seconds | the treatment service asks for a suggestion | the agent run holds status "TIMED_OUT" and fallback true And no suggestion and no decision log entry exist and SCR-14 shows MSG-P10-007 | RWB-E2-032 |
| AC-EXC-P10-010-03 | An answer that fails the schema | the model returns installments -12 | the guardrail runs | the agent run holds status "GUARDRAIL_FAILED" with check "SCHEMA" and no suggestion is returned | RWB-E2-032 |
| AC-EXC-P10-010-04 | The decision cannot be recorded | the decision log writer fails | the model answers | no suggestion is returned and the treatment service receives DecisionNotRecordedException with MSG-P7-003 And the agent run has no decision log entry ID | RWB-E2-032 |
| AC-EXC-P10-010-05 | Not a restructure | treatment "T-1002" has type "SETTLEMENT" | the treatment service asks for a suggestion | no model call is made and no suggestion returns | RWB-E2-032 |
| AC-EXC-P10-010-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-010-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.11 Fall back to the rule result when an agent is unavailable

#### A2.11.1 Intent

**Business objective.** Uses the rule answer and continues when the agent does not reply inside the timeout, and records the fallback.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Uses the rule answer and continues when the agent does not reply inside the timeout, and records the fallback.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Fall back to the rule result when an agent is unavailable | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Model gateway

**Prerequisites.** FEAT-DRI-07

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-011-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-011-01 | Approved endpoint | the approved model endpoint on the private endpoint of the SCB tenant | the orchestrator runs agent "ECHO" for case "RW-2026-000101" | the call succeeds with run status "ANSWERED" And one agent run row holds agent "ECHO", policy version "P1", prompt version "PR1", model version "MODEL-A-2026-10", latency 1,200 ms, tokens in 900, tokens out 150 and cost 0.0525 baht And one AgentRunCompleted event is written to the outbox with the run ID, agent "ECHO", the case ID, outcome "ANSWERED" and fallback false | RWB-E1-058 |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P10-011-01 | Prompt versions | prompt version "PR1" is in force for agent "ECHO" | RW-COE loads prompt version "PR2" and RW-RISK approves it with valid from 2026-11-20 | prompt version "PR2" exists with status "APPROVED" And prompt version "PR1" stays readable through GET /admin/agent-configs with its text hash unchanged And a run on 2026-11-19 uses "PR1" and a run on 2026-11-20 uses "PR2" | RWB-E1-058 |
| AC-ALT-P10-011-02 | Schema check | the model stub returns an answer with field "summary" missing from the output schema of "ECHO" | the guardrail runs | the output is rejected with run status "GUARDRAIL_FAILED" and fallback true And the guardrail result holds check code "SCHEMA" with the missing field name And the count of check code "SCHEMA" failures for "ECHO" on the business date rises by 1 | RWB-E1-058 |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-011-01 | The model does not answer inside the timeout | the model stub does not answer for 61 seconds | the orchestrator runs agent "ECHO" for case "RW-2026-000102" | the call is ended at 60 seconds And the agent run holds status "TIMED_OUT", fallback true and latency 60,000 ms And the orchestrator returns a fallback result with reason "TIMED_OUT" (R-UNI-32) | RWB-E1-058 |
| AC-EXC-P10-011-02 | A configuration file that fails a check is refused | a policy file for agent "ECHO" with timeout_seconds 0 | RW-COE loads it through POST /admin/agent-configs | the load is refused with 422 and MSG-P10-001 naming check "timeout_seconds between 1 and 120" And policy version "P1" stays in force and no new version row exists | RWB-E1-058 |
| AC-EXC-P10-011-03 | The loader cannot approve their own version | user "coe.user01" loaded policy version "P2" for agent "ECHO" | user "coe.user01" calls POST /admin/agent-configs/{versionId}/approve for "P2" | the approval is refused with 409 and MSG-P7-002 And version "P2" keeps status "LOADED" | RWB-E1-058 |
| AC-EXC-P10-011-04 | A repeated run request has no further effect | agent "ECHO" ran for case "RW-2026-000101" with idempotency key "ECHO:RW-2026-000101:2026-11-30" | the same request arrives again with the same key | no second agent run row and no second model call exist And the first result is returned and the idempotency hit is counted (R-UNI-40) | RWB-E1-058 |
| AC-EXC-P10-011-05 | An evaluation on an empty sample is refused | sample "ECHO-S2" has 0 labeled rows for agent "ECHO" | RW-COE starts the evaluation of "ECHO" on "ECHO-S2" | the request is refused with 422 and MSG-P10-002 And no evaluation run and no agent run row exist | RWB-E1-058 |
| AC-EXC-P10-011-06 | A second evaluation while one is running is refused | the evaluation of "ECHO" on "ECHO-S1" version 1 has status "RUNNING" | RW-COE starts the same evaluation again | the request is refused with 409 and MSG-P10-003 And one evaluation run exists for "ECHO" on "ECHO-S1" version 1 with status "RUNNING" | RWB-E1-058 |
| AC-EXC-P10-011-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-011-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.12 Change an autonomy level

#### A2.12.1 Intent

**Business objective.** Changes the autonomy level for one agent and one decision, as a versioned configuration row.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Changes the autonomy level for one agent and one decision, as a versioned configuration row.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Risk and model risk officer | Opens the screen and change an autonomy level | Checks the role, the capability area and the scope |
| 2 | Risk and model risk officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Model gateway

**Prerequisites.** FEAT-CWC-22

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-012-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P10-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| agent_policy.agent_code | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER | varchar(30) | Yes | LOV-AGENT | No |
| agent_policy.policy_version | Policy version, for example P1 | varchar(20) | Yes | None | No |
| agent_policy.model_code | Model deployment the agent calls through the gateway | varchar(40) | Yes | None | No |
| agent_policy.model_version | Model version the policy uses | varchar(40) | Yes | None | No |
| agent_policy.output_schema_ref | Reference to the JSON Schema the answer must meet | varchar(400) | Yes | None | No |
| agent_policy.allowed_tools | Tools the agent may call through the tool gateway | jsonb | No | None | No |
| agent_policy.autonomy_mode | Off, shadow or L1 | varchar(10) | Yes | LOV-AUTONOMY | No |
| agent_policy.segment_product_group | Product group the mode applies to; empty for all | varchar(15) | No | LOV-PRODUCT | No |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| Risk and model risk officer | Primary |
| Center of excellence analyst | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-012-01 | Change an autonomy level | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-012-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-012-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.13 Detect model drift and raise a decision

#### A2.13.1 Intent

**Business objective.** Watches calibration and drift, and raises a decision with an owner and a date on a breach.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Watches calibration and drift, and raises a decision with an owner and a date on a breach.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Detect model drift and raise a decision | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Model gateway, Power BI

**Prerequisites.** FEAT-AGT-06

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-013-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P10-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Risk and model risk officer | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-013-01 | Detect model drift and raise a decision | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-013-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-013-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.14 Run a champion and challenger test

#### A2.14.1 Intent

**Business objective.** Runs two rule or model versions side by side and compares the outcome.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Runs two rule or model versions side by side and compares the outcome.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Center of excellence analyst | Opens the screen and run a champion and challenger test | Checks the role, the capability area and the scope |
| 2 | Center of excellence analyst | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Model gateway

**Prerequisites.** FEAT-AGT-05

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-014-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P10-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| agent_policy.agent_code | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER | varchar(30) | Yes | LOV-AGENT | No |
| agent_policy.policy_version | Policy version, for example P1 | varchar(20) | Yes | None | No |
| agent_policy.model_code | Model deployment the agent calls through the gateway | varchar(40) | Yes | None | No |
| agent_policy.model_version | Model version the policy uses | varchar(40) | Yes | None | No |
| agent_policy.output_schema_ref | Reference to the JSON Schema the answer must meet | varchar(400) | Yes | None | No |
| agent_policy.allowed_tools | Tools the agent may call through the tool gateway | jsonb | No | None | No |
| agent_policy.autonomy_mode | Off, shadow or L1 | varchar(10) | Yes | LOV-AUTONOMY | No |
| agent_policy.segment_product_group | Product group the mode applies to; empty for all | varchar(15) | No | LOV-PRODUCT | No |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| Center of excellence analyst | Primary |
| Risk and model risk officer | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-014-01 | Run a champion and challenger test | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-014-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-014-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.15 Raise or lower an autonomy level with approval

#### A2.15.1 Intent

**Business objective.** Steps an agent up on measured evidence, and drops it on a breach, with the approval each needs.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Steps an agent up on measured evidence, and drops it on a breach, with the approval each needs.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Risk and model risk officer | Opens the screen and raise or lower an autonomy level with approval | Checks the role, the capability area and the scope |
| 2 | Risk and model risk officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-AGT-12

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-015-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P10-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| agent_policy.agent_code | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER | varchar(30) | Yes | LOV-AGENT | No |
| agent_policy.policy_version | Policy version, for example P1 | varchar(20) | Yes | None | No |
| agent_policy.model_code | Model deployment the agent calls through the gateway | varchar(40) | Yes | None | No |
| agent_policy.model_version | Model version the policy uses | varchar(40) | Yes | None | No |
| agent_policy.output_schema_ref | Reference to the JSON Schema the answer must meet | varchar(400) | Yes | None | No |
| agent_policy.allowed_tools | Tools the agent may call through the tool gateway | jsonb | No | None | No |
| agent_policy.autonomy_mode | Off, shadow or L1 | varchar(10) | Yes | LOV-AUTONOMY | No |
| agent_policy.segment_product_group | Product group the mode applies to; empty for all | varchar(15) | No | LOV-PRODUCT | No |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| Risk and model risk officer | Primary |
| Center of excellence analyst | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-015-01 | Raise or lower an autonomy level with approval | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.16 Review agent risk at the committee

#### A2.16.1 Intent

**Business objective.** Puts agent performance, overrides and incidents in front of the strategy and model committee.

**Problem.** Officers gather and check facts by hand before every decision.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Agent fallback rate | Below 10 percent | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Puts agent performance, overrides and incidents in front of the strategy and model committee.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Risk and model risk officer | Opens the screen and review agent risk at the committee | Checks the role, the capability area and the scope |
| 2 | Risk and model risk officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Power BI

**Prerequisites.** FEAT-AGT-06

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P10-016-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P10-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| agent_policy.agent_code | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER | varchar(30) | Yes | LOV-AGENT | No |
| agent_policy.policy_version | Policy version, for example P1 | varchar(20) | Yes | None | No |
| agent_policy.model_code | Model deployment the agent calls through the gateway | varchar(40) | Yes | None | No |
| agent_policy.model_version | Model version the policy uses | varchar(40) | Yes | None | No |
| agent_policy.output_schema_ref | Reference to the JSON Schema the answer must meet | varchar(400) | Yes | None | No |
| agent_policy.allowed_tools | Tools the agent may call through the tool gateway | jsonb | No | None | No |
| agent_policy.autonomy_mode | Off, shadow or L1 | varchar(10) | Yes | LOV-AUTONOMY | No |
| agent_policy.segment_product_group | Product group the mode applies to; empty for all | varchar(15) | No | LOV-PRODUCT | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Risk and model risk officer | Primary |
| Tribe lead and squad members | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P10-016-01 | Review agent risk at the committee | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P10-016-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P10-016-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-46 Agent monitor | Agent runs, fallbacks, evaluation results and autonomy levels | E2; E8 full |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| FSD owner, business analyst | | | |
| Business owner | | | |
| Solution architect | | | |
| QA lead | | | |

## Appendix A. Business glossary

Terms follow the Recovery Workbench Business Glossary.

| Term | Thai | Meaning |
|---|---|---|
| See the glossary | | |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
