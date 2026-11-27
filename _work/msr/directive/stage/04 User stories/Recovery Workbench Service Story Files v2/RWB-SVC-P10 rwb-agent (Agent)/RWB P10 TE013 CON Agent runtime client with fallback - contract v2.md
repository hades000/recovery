# RWB-P10-TE013-CON Agent runtime client with fallback

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-TE013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent (P10; the agent platform of DL33) |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement (DOR-RWB-P10-TE013-CON-16) |
| Contract version | API Specification v5, rwb-agent.yaml, path /api/recovery/agent/v1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-018, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract slice of RWB-TE-013 for rwb-agent. The legacy key is a published Java interface inside one deployment - `AgentStepClient`, `AgentStepRequest`, `RuleResult` and `AgentStepOutcome` in package `recovery.agent.api`, an `AgentOrchestrator.run` method call, a P7 `DecisionLogWriter` of the same process and a Quartz job step of RWB-TE-007. This document fixes that seam as a contract on Day 1: two operations on `/api/recovery/agent/v1` (**DP-13**, **DP-20**), their members in the legacy names, the step key as the idempotency key, the refusal set, the record payload written by the calling step through the local decision-record library and published as EV-08 (**DP-03**, **DP-09**), the workflow and activity contract on queue `rwb-agent` (**DP-10**), the two consumed boundaries of P3 and P7 (**DP-07**, **DP-03**) with one hop and 2 s (**DP-11**), the run read restated behind the gateway-bff route (**DP-19**) and the three fakes. Tables stay in `rwb_agent` only (**DP-01**) and the migration sequence stays the service's own (**DP-15**). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 24 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the agent runtime client fixed as a contract on Day 1: the `AgentStepClient` operation on `/api/recovery/agent/v1/agent-steps` with its request members - agent code, case ID, decision code, step key, rule result and masked inputs - its answer members - record reference, applied result, recommendation, fallback, fallback reason, autonomy mode and run ID - its idempotency on the step key and its refusal set 401, 403, 409, 422 and 503; the link operation that sets the record reference on the run; the record payload written through the local decision-record library in the calling step's transaction; the run read restated from the baseline; and the three contract fakes**, so that **the app story, the deployment story, the calling stories and the integration copy build against one agreed, testable seam on Day 1, a repeat of a step key can never produce a second run or a second record, and no caller is offered an orchestrator call it is not allowed to see**.

### 2. Business rationale

The legacy key was written against objects inside the monolith: `AgentStepClient` and `AgentStepRequest` were Java types in the same deployment as their caller, `AgentOrchestrator.run` was a method call, `DecisionLogWriter` was the P7 interface of the same process, and the step arrived through a Quartz job of RWB-TE-007 (legacy sections 4, 12 and 13). In the target each is a boundary or is gone:

- The orchestrator is `AgentRunWorkflow` on the rwb-agent task queue in namespace `rwb-recovery`, with the approved policy's 60 second budget inside it (Arch v5 slide 16; DP-20).
- The published interface becomes a REST contract with a fake, one hop, under `/api/recovery/agent/v1` (DP-11, DP-13; ADR-020).
- The `DecisionLogWriter` becomes the local decision-record library: the step writes its own record in its own schema and transaction, and rwb-decision collects it into the central ledger on `rwb.decision-record.v1` (DP-03; ADR-022).
- The rule result is not a shared bean: the embedded Drools kit evaluates the package published from rwb-decision and the caller passes the result in (DP-04; ADR-017).
- The Quartz job step is retired with RWB-TE-007 and becomes a Temporal step through the workflow kit (DP-10; ADR-016).

Contract-first only works if the seam is written down once. The seam is small and load-bearing: one operation whose request and answer are the legacy records, one link operation that keeps run and record joined, one idempotency rule on a key the whole legacy story is built on (R-UNI-40), one refusal set, one record payload with no personal data, and one fake set that makes the app and the deployment testable on Day 1.

With the shape agreed and faked on Day 1, four teams move at once: RWB-P10-TE013-APP builds the mode resolution, the timed run, the fallback, the record write and the link against these fakes; every calling story of wave 1 compiles against `recovery.agent.api`; RWB-P7-E1027-CON fixes the record type the contract names; and RWB-P10-TE013-OPS deploys the operations and the wiring against the same names. Without it each caller invents its own request, the idempotency of the step key is lost at the seam, and a record with no run or a run with no record becomes normal.

This story defines the provided side of the two operations and the record payload, and never restates what another owner holds: the eleven platform operations are baselined in RWB-P10-E1058-CON, the lists are rwb-case's, the record type and ledger are rwb-decision's and the run read is the baseline's (DP-01).

The legacy measure of this key is an agent fallback rate below 10 percent per month. rwb-reporting owns the measure definition and keeps that threshold. This contract only makes the facts countable: the agent version and the fallback fact are on the record of the step (12.3), so the count by agent version and month is readable from the ledger. The operation name, the period grain and the parameter names of the measure are left to the reporting contract and the measures review of wave 1, and this document names none of them.

### 3. Preconditions

- The service template and naming library are available (RWB-PLT-TPL), so the REST base, the error envelope and the CloudEvents envelope follow the platform rule (§R4; DP-13, DP-14).
- The agent platform contract of RWB-P10-E1058-CON is in force: the eleven operations, the eight agent tables, the EV-28 payload, the error taxonomy and AgentRunWorkflow with its six activities, on queue `rwb-agent` in namespace `rwb-recovery`.
- RWB-PLT-E1027-CON publishes the record shape, the local write in the calling transaction and `rwb.decision-record.v1` (DP-03); RWB-PLT-E1072-CON publishes the rule-package client and the rule-result shape, with packages and versions from rwb-decision (DP-04); RWB-PLT-TE006-CON publishes the envelope, the relay, the retry topic and the `.dlt` rule (DP-09); RWB-PLT-E1071-CON publishes the namespace, the queue rule and the activity contract (DP-10).
- RWB-P3-E1043-CON is published with its client library, and LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT are the values of TSD P10 Agent runtime v2 T3.2 (DP-07).
- The record read of rwb-decision is known: `GET /api/recovery/decision/v1/decision-log/{entryId}` answers one record by its reference (DP-03).
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W1.
- The operation paths, the member names beyond the legacy Java record members, the member types and the refusal semantics are fixed by this document, because no source names a run-submit operation among the eleven P10 operations (GAP-0620; ASM-0908).

### 4. Flow

1. Draft the step operation that replaces the legacy `AgentStepClient.runStep` call: method, path under `/api/recovery/agent/v1`, request members, answer members, idempotency on the step key and refusals (AC1, AC2, AC3).
2. Fix the call type and the budget at the boundary: one REST hop with a fake, and the policy timeout of 60 seconds as the recorded exception to the 2 s budget of DP-11, because the run is bounded by `agent_policy.timeout_seconds` and NFR-010 allows the full wait before the rule result is used (AC1; BR4).
3. Fix the two outcomes the caller depends on: the applied result always the rule result in SHADOW and L1, the recommendation only in L1, and the fallback with its reason TIMED_OUT, SCHEMA or NO_POLICY (AC2, AC3).
4. Fix the link operation and the rule that a run holds one record reference and a different reference is refused (AC4; BR6).
5. Declare the record payload written through the local library: record reference, decision code, agent version, model version, inputs reference, final call and actions {caseId, agentRunId, mode, fallback, fallbackReason}, published as EV-08 on `rwb.decision-record.v1`, with no personal field (AC5; DP-03, DP-09).
6. Restate the run read the callers and tests use from the baseline of RWB-P10-E1058-CON and declare the gateway-bff route in front of it (AC6; DP-19).
7. Write the three fakes with their answers, refusals and timings: the decision-record library and read, the rwb-case lists and the gateway-bff route (AC6).
8. Publish the nine sub-tables of section 12 and the contract tests, and tag the baseline for the app and deployment stories.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of the request or the answer drifts from this document | The contract test fails and the merge is blocked | None | AC1, AC2, AC3 |
| X2 | The request carries no step key, no rule result or a member the contract does not declare | The operation refuses with 422 and names the member; no run is started | MSG-GEN-001 | AC1 |
| X3 | The contract declares an orchestrator method, a Java call or another service's table as its own | The review refuses the document: the seam is one REST hop to rwb-agent and nothing else | None | AC6 |
| X4 | A payload gains a personal field, or fails its registry subject | The data-steward review and the contract test refuse the payload; a produced message that fails is routed to `.dlt` with an alert | None | AC5 |
| X5 | The record payload drifts from the type of rwb-decision or the library shape | The contract test between this document and RWB-P7-E1027-CON fails and this document is aligned, because P7 owns the type | None | AC5 |
| X6 | A restated operation drifts from the baseline | The contract test fails on the baseline and this document is aligned, because the baseline owns it | None | AC6 |
| X7 | A member type, a page size or a timing is missing from the source material | The member carries the placeholder, one gap row and one assumption row, and the fake is written to the assumed shape | None | AC1, AC5, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the workflow kit, the outbox library, the agent platform contract, the record library and the rwb-case reference-data contract as published |
| Negotiable | Member types beyond the legacy Java types, the error detail text and the fake timings are settled with their owners; the operation set, the idempotency rule, the refusal set, the record payload and the boundary mapping are fixed by this realignment |
| Valuable | Unblocks the app, deployment, calling and integration stories of this key on Day 1 and gives every caller one shape for a step and its record |
| Estimable | Two provided operations, one restated read, one record payload, two consumed boundaries and three fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact - the schema file, the payload, the fake, the document - and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Agent runtime client contract slice for rwb-agent

  Background:
    Given the service naming rule and the platform error envelope of the platform library are in force
    Given the agent platform contract of RWB-P10-E1058-CON is in force
    Given the decision-record library of RWB-PLT-E1027-CON and the workflow kit of RWB-PLT-E1071-CON are in force

  Scenario: AC1 The AgentStepClient operation is contracted on the agent base (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When a calling step submits agent "INTAKE" for case "RW-2026-000201" with step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30"
    Then one operation answers on POST /api/recovery/agent/v1/agent-steps with 200 and an AgentStepOutcome in the member names and types of this document
    Then the request declares agentCode, caseId, decisionCode, stepKey, ruleResult {ruleId, ruleVersion, toState, result} and inputs, and a request that omits the step key or the rule result is refused with 422 and MSG-GEN-001
    Then the refusals are 401 without a session, 403 without the Rules and parameters right with MSG-P4-002, 409 for a step key whose first run is still RUNNING, 422 for a request the service cannot accept and 503 when the store, the workflow or a consumed contract is unavailable
    Then the operation is one hop under the base /api/recovery/agent/v1, and its budget is the policy timeout of 60 seconds as the recorded exception to the 2 s client budget of DP-11
    Then the call type between a calling step and rwb-agent is one REST hop with a fake, and RWB-ITG-TE013-ITG proves the real hop across services

  Scenario: AC2 The answer members keep the legacy outcome (new, D-RCV-60)
    Given the answer element declared in this document
    When the outcome of the step of case "RW-2026-000201" is read
    Then it carries decisionLogEntryId, appliedResult, recommendation, fallback, fallbackReason, autonomyMode and agentRunId
    Then in mode SHADOW the appliedResult is rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE", recommendation is null and fallback is false
    Then in mode L1 the appliedResult is the same rule result and recommendation carries the agent answer with confidence 0.91
    Then a run that did not answer inside 60 seconds answers fallback true with reason TIMED_OUT and the run ID
    Then a run whose answer failed a guardrail answers fallback true with the check code, and a run with no approved policy answers fallback true with reason NO_POLICY and no agentRunId
    Then every value is the legacy value of RWB-TE-013 and no member is dropped or renamed without a new version

  Scenario: AC3 The step key is the idempotency key and the repeat answers the first outcome (new, D-RCV-60)
    Given a step with key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" that ran once
    When the same request arrives again with the same key
    Then the operation answers the first outcome with the same agentRunId and the same decisionLogEntryId, one run row and one record exist for the key, and the repeat is counted as an idempotency hit (R-UNI-40)
    Then the key is declared as the Idempotency-Key of the operation and as the workflow ID of AgentRunWorkflow
    Then a repeat that arrives while the first run is RUNNING is refused with 409 and writes nothing

  Scenario: AC4 The link operation keeps one record per run (new, D-RCV-60)
    Given a run of agent "INTAKE" for case "RW-2026-000201" and the record the step wrote
    When the link operation is called on PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record with the record reference
    Then the answer is 200 with the run and its decision_log_id set to that reference
    Then the same reference answers the same run and writes nothing twice, a different reference is refused with 409, an unknown run answers 404 and a reference the service cannot accept answers 422
    Then the run and the record are joined by reference only, no foreign key crosses a schema and no table of another service is read

  Scenario: AC5 The record payload is declared and carries no personal field (new, D-RCV-60)
    Given a step of case "RW-2026-000201" in mode SHADOW with rule "R-UNI-32" version "2026.11"
    When the record is written through the local library
    Then the payload carries the record reference, the decision code, agent version "INTAKE@P1/PR1", the model version, the inputs reference, the final call "RESUME_STATE" and actions {caseId, agentRunId, mode, fallback, fallbackReason}
    Then it is published as rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1, keyed by the record reference, in the transaction of the calling step, with the retry topic and the .dlt topic of the platform
    Then rwb-decision owns the type and the central ledger, and a payload that fails its registry subject is refused before the relay and routed to .dlt with an alert
    Then no account number, customer name or personal field is declared, and no agent event is declared by this document

  Scenario: AC6 The run read is restated and the three fakes are complete (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables and the three fakes are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then GET /api/recovery/agent/v1/admin/agent-runs with query agent, from and to answering AgentRun[] is restated from RWB-P10-E1058-CON and is declared as the baseline's, not this story's
    Then the fakes of the decision-record library and its read, of the rwb-case reference lists and of the gateway-bff route answer every consumed path and payload of this document
    Then the route in front of the run read is a pass-through of one hop, and its name is agreed with the route contract RWB-PLT-N001-CON
    Then a drift between a fake and this document fails the contract test, and every fixture is synthetic

  Scenario: AC7 The time budgets are fixed and no business value is declared (new, D-RCV-60)
    Given the contract file and the schema of this story
    When the time budgets and the declared values are reviewed and tested
    Then the budget of the step operation is the policy timeout of 60 seconds, the single recorded exception to the 2 s client budget of DP-11, and every other hop expires at 2 seconds
    Then the modes, the timeout, the agent codes, the check codes and the reason codes stay rows of the policy, the reference data and the library, and the contract only names them
```

**Target reading.** The agent "INTAKE", the policy "P1", the prompt "PR1", the case "RW-2026-000201", the rule "R-UNI-32" version "2026.11", the next state "RESUME_STATE", the timeout 60 seconds, the confidence 0.91, the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the reasons TIMED_OUT, SCHEMA and NO_POLICY and the agent version string "INTAKE@P1/PR1" are the legacy values of RWB-TE-013, copied into the contract as the fixture values of its tests; the member names of the request and the answer are the legacy `AgentStepRequest` and `AgentStepOutcome` members, renamed only into the JSON spelling this document fixes and never dropped. The seven criteria are new (D-RCV-60) and test the artefact alone: the operation, its members, its refusals, its idempotency, the link, the record payload, the fakes, the time budgets and the absence of business values. No criterion asserts a business outcome, which is the app story's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The step operation is one operation under `/api/recovery/agent/v1` and is the only way a calling step reaches an agent; no caller reads `agent_run`, `agent_policy` or a record table | DP-11; DP-13; DP-20; legacy section 12 |
| BR2 | The request and the answer keep the legacy members - agentCode, caseId, decisionCode, stepKey, ruleResult, inputs; decisionLogEntryId, appliedResult, recommendation, fallback, fallbackReason, autonomyMode, agentRunId - and no member is dropped or renamed without a new version | Legacy section 12; TSD P10 Agent runtime v2 T-A.1 |
| BR3 | The step key is the idempotency key of the operation and the workflow ID of AgentRunWorkflow; a repeat answers the first outcome and writes nothing twice | R-UNI-40; legacy BR5 |
| BR4 | The budget of the step operation is the policy timeout of 60 seconds, the single recorded exception to the 2 s client budget of DP-11, and every other hop keeps 2 seconds | DP-11; NFR-010; ADR-020; ASM-0903 |
| BR5 | The answer carries the applied result, always the rule result in SHADOW and L1, and the recommendation only in L1 | Legacy BR1; `agent_policy.autonomy_mode` (DF-AGT-008) |
| BR6 | A run holds one record reference; the same reference answers the same run, a different reference is refused with 409 and the join is by reference only | R-UNI-40; DF-AGT-058; ASM-0910 |
| BR7 | The record of a step is written by that step through the local library in its own schema and transaction, and rwb-decision owns the type, the ledger and the record read | DP-03; ADR-022; RWB-P10-E1058-CON BR8 |
| BR8 | No business value in the contract: the modes, the timeout, the agent codes, the check codes and the reason codes stay rows of the policy, the reference data and the library, and the contract only names them | Template and Rules §R7.2 s17; DP-07 |
| BR9 | Every message is a CloudEvents 1.0 message on the owner's topic, keyed by the record reference, validated against its registry subject before the relay and routed to `.dlt` on failure | DP-09; DP-14; Arch v5 slide 42 |
| BR10 | One base per service: this contract declares `/api/recovery/agent/v1` and never another service's base or topic, and it restates the run read of the baseline without owning it | DP-13; Arch v5 slide 41; RWB-P10-E1058-CON |
| BR11 | The refusal set is the platform one: 401, 403, 409, 422 and 503, each with the platform problem response and the message ID where a business message applies | Platform error envelope; legacy X4, X5; ASM-0909 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the members, the idempotency, the record payload, the restated read and the fakes are described | In review |
| In review | Consumer sign-off | The app, deployment, calling and integration stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a refusal detail or a payload field is added without removing one | Baselined |
| Baselined | Breaking change | A request or answer member is removed, renamed or retyped, or the idempotency rule changes | In review, with the owner of the affected caller |
| Baselined | Drift in a fake or against the baseline | A contract test fails | In review |
| Baselined | The baseline publishes a new run-read shape, or the record type changes | RWB-P10-E1058-CON or RWB-P7-E1027-CON publishes a new version | Baselined, aligned to the owner |

These are the states of this document, not of a step, a run or a case. The step and run states - ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, NO_POLICY and the link - belong to RWB-P10-TE013-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the operations, the members, the idempotency rule, the record payload mapping, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to an operation, a member or the payload, and any change to the budget exception |
| The rwb-decision owner | Owns the record type, the central ledger, the record read and the `rwb.decision-record.v1` topic, and signs off the payload taken from the library |
| The rwb-case owner | Owns the reference lists named in the contract and signs off the list codes taken from its document |
| The app and deployment stories of this key | Review and accept the parts they consume |
| The calling stories of wave 1 | Compile against `recovery.agent.api` and its fake, and accept the request and answer shapes |
| Platform library owner | Owns the error envelope, the naming rule, the outbox library, the record library, the workflow kit and the Drools kit this document reuses |
| Data steward | Confirms that no personal data field is declared in the record payload or in the answer |

The calling identity is a calling service identity and the answering one is the rwb-agent service identity (DP-02); the rwb-agent login is Not specified in the source documents (GAP-0620; ASM-0913) and is fixed with the deployment story.

Both operations are authorised for the calling service identity by the rwb-access authorise check of DP-08; the check code is Not specified in the source documents (DOR-RWB-P10-TE013-CON-6).

### 11. Data

The contract declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Step request | Not specified in the source documents (DOR-RWB-P10-TE013-CON-7) | agentCode, caseId, decisionCode, stepKey, ruleResult {ruleId, ruleVersion, toState, result}, inputs (masked) |
| Step answer | Not specified in the source documents (DOR-RWB-P10-TE013-CON-7) | decisionLogEntryId, appliedResult {ruleId, ruleVersion, toState, result}, recommendation, fallback, fallbackReason, autonomyMode, agentRunId |
| Link request and answer | Not specified in the source documents (DOR-RWB-P10-TE013-CON-7) | record reference in the body; the AgentRun with decision_log_id set |
| Refusal | Not specified in the source documents (DOR-RWB-P10-TE013-CON-7) | the platform problem response: status, code, detail, the member name or the message ID when a business message applies |
| Record payload | Not specified in the source documents (DOR-RWB-P10-TE013-CON-7) | record reference, decision code, agent version, model version, inputs reference, final call, actions {caseId, agentRunId, mode, fallback, fallbackReason} |
| Restated run read | Not specified in the source documents (DOR-RWB-P10-TE013-CON-7) | AgentRun[] as published by RWB-P10-E1058-CON; the members this key reads are the run ID, the agent, the agent version, the case, the status, fallback, latency and the run time |
| Idempotency | Not specified in the source documents (DOR-RWB-P10-TE013-CON-7) | the step key as `Idempotency-Key` and as the workflow ID; the record reference as the idempotency of the link |
| Named values | Not specified in the source documents (DOR-RWB-P10-TE013-CON-7) | LOV-AUTONOMY (OFF, SHADOW, L1), LOV-AGENT and LOV-PRODUCT through the reference-data contract; the timeout as a policy value; the check codes and reason codes as library and policy values |

The member types are fixed here and confirmed at the review with the owners of rwb-decision and rwb-case: the legacy UUID members are strings in UUID format, the legacy String members are strings, `fallback` is a boolean, `ruleResult.result` and `recommendation` are free JSON values (legacy JsonNode), `inputs` is a JSON object (legacy map), `confidence` is a number with 4 decimal places (numeric(5,4), DF-AGT-050) and a cost value has 4 decimal places (`cost_thb` numeric(12,4), DF-AGT-054). The exact detail text of each refusal is Not specified in the source documents (GAP-0620; ASM-0908). No table of any schema is declared as an answer source: the operations answer from `rwb_agent`, and the record is written by the caller's library into the caller's schema (DP-01, DP-03).

The extractor provider, model name, model version, field-extraction route and answer field names of extraction_method MODEL are Not specified in the source documents (GAP-1005; GAP-1009); the route stays a property of rwb-document with no model name in code. The link operation is the PUT of 12.1, and the record write has its home in the calling service (12.3). The client builds the rule result first, starts AgentRunWorkflow on queue `rwb-agent` through this contract with the policy timeout of BR4, treats an expiry as TIMED_OUT with the rule result applied, and reads the run, its status and its fallback through GET /api/recovery/agent/v1/admin/agent-runs. The guardrail check codes are Not specified in the source documents (GAP-0381) and are to be published with the policy schema, so that a fallback reason is always a code the agent returns.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Rights |
|---|---|---|---|
| POST | `/agent-steps` | Run one case step through the agent and answer the legacy AgentStepOutcome; request agentCode, caseId, decisionCode, stepKey, ruleResult, inputs; 200 the outcome; idempotency key stepKey, idempotent on the step key | Rules and parameters C, service identity, scope applied; errors 401, 403, 409, 422, 503 |
| PUT | `/agent-runs/{runId}/decision-record` | Link one run to the decision record the calling step wrote; body the record reference; 200 the AgentRun with decision_log_id set; idempotency key runId (path), decision_log_id set once | Rules and parameters C, service identity, scope applied; errors 401, 403, 404, 409, 422, 503 |

The run read `GET /api/recovery/agent/v1/admin/agent-runs` (API-P10-001) is provided by rwb-agent and baselined in RWB-P10-E1058-CON; that document owns its full shape and this contract restates only the members this key reads. No other operation is declared here, and no orchestration method, Java interface or table read is offered as an answer source (BR1, BR10).

The refusal set of the two operations is the one in the table above. A 409 answers a step key whose first run is still RUNNING and a link on a run that already holds another record. The record reference (`decisionLogEntryId`, and the body of the link) is the UUID given by the decision-record library, and it is read back through the record read of rwb-decision before the link is stored. The route in front of the run read is a pass-through of one hop, and its name is agreed with the route contract RWB-PLT-N001-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT, checked before a mode is applied or a run row is written (DP-07) |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The read-back of the record the step wrote, before the link is stored (DP-03) |

Every operation is one hop with a 2 s client budget (DP-11, ADR-020); the step operation's own budget is the policy timeout of 60 seconds (BR4). The record write is not a consumed REST operation: it is the local library of DP-03 and the topic of 12.3.

The model endpoint is reached only through the agent platform's tool gateway, which holds the permissions while the agent holds no credential. rwb-agent has two read-only tools: case facts and score through the data-product contract of rwb-source-data (P1), and extracted document fields through the REST contract of rwb-document (P5) (Architecture v5 slide 16; AI and Agent Architecture v2 slide 8). Both contracts stay their owners' and are not operations of this contract.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` with the retry topic and the `.dlt` topic of the platform | P7 rwb-decision owns the type and the ledger; the record is written by the step through the local library | the record reference | record reference, decision code, agent version, model version, inputs reference, final call, actions {caseId, agentRunId, mode, fallback, fallbackReason} |

The event is inserted in the outbox in the same transaction as the record, by the local library, and relayed by the outbox library; the payload is validated against its registry subject before the relay (DP-09; BR9). This document declares no agent event: `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` belongs to the run path of RWB-P10-E1058-APP and is unchanged here.

The calling service appends the record locally in its own schema and transaction and publishes DecisionRecorded on `rwb.decision-record.v1` from its outbox, and rwb-decision collects it into the ledger (DP-03). This supersedes the legacy statement that the client publishes no event and writes through the P7 writer: the record event leaves from the outbox of the calling service, and rwb-agent publishes no event for the record.

The decision code of an agent step is the code in force from LOV-DECISION, carried in the request member `decisionCode`; the fixtures carry D6, and no agent-step sub-decision code is declared (GAP-1315). The agent run ID, the mode, the fallback and its reason are members of `actions`; `recommendation` and the final call stay separate fields. The code of an agent step is settled with the reference-data owner before the first joint environment.

A record that the ledger ingest refuses is answered with MSG-P7-009 naming the field and is held for the retry and dead-letter path with an alert; nothing is added to the ledger (GAP-1317). MSG-P7-009 carries the refusals of the decision code, the rule version, the agent version, the inputs reference and the decided time, with the legacy field names kept character for character. Its wording is the one published in RWB-P7-E1027-CON (section 14).

#### 12.4 Events consumed

None. The step operation is a request and the link operation is a write; the service subscribes to no topic for this key. The consumers of EV-08 are rwb-decision and rwb-reporting, and the EV-28 consumers are rwb-decision, rwb-document and rwb-deviation (Arch v5 slides 42 and 43); all are other owners' projections.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow of the baseline of RWB-P10-E1058-APP, one execution per step key with the key as workflow ID | `rwb-agent` | Input: the resolved policy and prompt, the case, the step key and the masked inputs. Output: the run row and its outcome, or the expiry that hands the rule result back |
| ResolveAutonomyMode | Activity | `rwb-agent` | Output: OFF, SHADOW, L1 or none, with the policy row in force |
| ApplyAutonomyMode | Activity | `rwb-agent` | Output: the outcome element of 12.1 |
| LinkDecisionRecord | Activity | `rwb-agent` | Output: `decision_log_id` set once, on the run and the record reference |

The workflow identity, queue and namespace are the platform rule of §R4; the three activity names are this story's and are accepted by RWB-P10-TE013-APP, and the six baseline activities of AgentRunWorkflow are RWB-P10-E1058-CON's and are not redefined.

#### 12.6 Schedules

None. This key starts no Schedule: a step is started by its caller, and the legacy dependence on the Quartz entry of RWB-TE-007 is retired under §R6 and points to the workflow kit of RWB-PLT-E1071-CON (DP-10). The contract declares no job table, job admin read or cron expression.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_policy | P10 (`rwb_agent`) | The approved policy in force: mode, timeout, fallback rule, agent and prompt versions; no column added here |
| agent_run | P10 (`rwb_agent`) | The run of a step key, its status, fallback, output, confidence and `decision_log_id`; no column added here |
| agent_prompt | P10 (`rwb_agent`) | The prompt version the policy names; no column added here |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The idempotency envelope of the step key and the link (DP-09) |

No table of another service is declared and no foreign key crosses a schema (DP-01). `decision_log_entry` is P7's type and is written by the calling step in the calling service's schema through the library; `reference_version` and `reference_row` are P3's and are reached through its contract (DP-03, DP-07).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Decision-record library and record-read fake (RWB-PLT-E1027-CON, RWB-P7-E1027-CON) | A written record with its reference; a record with fallback true and a reason; a record with agent version null; a 503 on write; the first record of a step key; a read-back by reference and a reference that is not found | Contract tests, app story, integration copy |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | LOV-AUTONOMY with OFF, SHADOW and L1; LOV-AGENT with INTAKE; LOV-PRODUCT; a list that is not in force; a delay beyond 2 s | Contract tests, app story |
| gateway-bff route stub (RWB-PLT-N001-CON) | A pass-through route in front of the run read, one hop, JSON media type preserved, the refusal passed through unchanged | Contract tests, app story, deployment story |

The outbox stub, the workflow kit stub, the Drools kit stub and the model stub of the baseline are the platform's and RWB-P10-E1058-APP's; they are used but not declared here. Every fixture is synthetic and holds no personal data.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 restated and read by the tests, 2 consumed | The step and link operations provided; the run read restated from the baseline; the P3 lists and the P7 record read consumed, one hop and 2 s each |
| Kafka | 1 declared, 0 consumed | EV-08 on `rwb.decision-record.v1` with the retry and `.dlt` topics, written by the local library in the caller's transaction; EV-28 stays with the baseline and is not re-declared |
| Temporal | 1 workflow of the baseline, 3 activities of this story, 0 Schedules | AgentRunWorkflow on queue `rwb-agent` with ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord |
| File | None | No file is read or written and no extract exists |

### 13. Solution plan

**Deliverables.** `contract/agent-step-client.yaml` (the two operations, their members, their rights, their refusals and their idempotency), `contract/agent-step-outcome.md` (request and answer members with the legacy names and the fixture values), `contract/agent-decision-record.asyncapi.yaml` (EV-08 on `rwb.decision-record.v1`, its envelope, key, subject and `.dlt` route), `contract/agent-run-read.md` (the run read restated), `contract/agent-client-boundaries.md` (the lists and the record read with their budgets) and the three WireMock mappings with their fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON for the app story; C RWB-P7-E1027-CON; the payload and the topic are declared here |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON for the app story; the rule result arrives in the request |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON for the app story; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON for the app story |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | H RWB-P10-TE013-CON for the app story; none here |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON as the legacy dependency of the pattern; this document is that contract |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts it names are those its consumers add, and the C rows of the key are the published contracts of rwb-case and rwb-decision. DP-20 is the pattern this document realises, so the dependency it carries is the row the app story builds against (BR1).

**Build steps**

1. Write the step operation contract: the method, the path under the base, the five request members and the seven answer members with their types, the idempotency on the step key and the refusal set.
2. Write the answer document with the legacy fixture values of AC2 and the rule that a member is removed only with a new version.
3. Write the link operation with its body, its answers 200, 404, 409 and 422 and its idempotency on the record reference.
4. Write the EV-08 AsyncAPI document: envelope, key, payload members, registry subject and `.dlt` route, with the statement that rwb-decision owns the type and the ledger.
5. Restate the run read against the baseline and declare the route in front of it.
6. Write the boundary document for the lists and the record read, with one hop and the 2 s budget, and the budget exception of the step operation.
7. Build the three WireMock mappings and their synthetic fixtures, including the 503 of the record write and the silent list read.
8. Add the contract tests of section 16, including the drift test between each fake and this document and the drift test against the baseline.
9. Tag the baseline and collect the sign-off of the app, deployment and calling stories.

**Done when.** The five contract files validate in the pipeline, the six contract tests pass, the three fakes answer every consumed path and payload, the record payload carries no personal field, and the app and deployment stories of this key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The record write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A caller without the right calls the step operation or the link | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required request member is empty | Enter {field}. |
| MSG-P7-009 | The ledger ingest of rwb-decision refuses a record; the message names the field | The decision record was refused: {field} is missing or not valid. |

MSG-P7-003 and MSG-P4-002 are the legacy messages of RWB-TE-013 and keep their wording character for character; MSG-GEN-001 is the platform message of an empty required field. This contract adds no message of its own.

### 15. Screens and states

None in this story. The contract serves no screen: a fallback shows on the decision record of the case, which a Decision log R holder reads through the P7 read, and on the run read of the baseline, reached through the gateway-bff route (DP-19). The agent monitor screen SCR-46 belongs to RWB-E2-031 and the autonomy-level screen to Epic 3; the contract fixes no screen field, order or masking rule. The SCR-46 states empty, loading, error and no access are Not specified in the source documents (CG-ALL-2927). The route in front of the run read is a pass-through of one hop, and its name is agreed with the route contract RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-TE013-CON-01 | AC1, BR1, BR2, BR11 | Contract | The step operation validated against its schema: the five request members, a request with no step key refused with 422 and MSG-GEN-001, and the refusal codes 401, 403, 409, 422 and 503 |
| TC-P10-TE013-CON-02 | AC2, BR2, BR5 | Contract | The answer for case "RW-2026-000201": SHADOW with rule "R-UNI-32" version "2026.11" and recommendation null; L1 with confidence 0.91; TIMED_OUT after 60 seconds; a failed check code; NO_POLICY with no run ID |
| TC-P10-TE013-CON-03 | AC3, BR3 | Contract | Step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" twice: one run, one record and the first outcome; a repeat while RUNNING refused with 409 |
| TC-P10-TE013-CON-04 | AC4, BR6 | Contract | The link operation: 200 with the record reference, the same reference again, a different reference refused with 409, an unknown run 404 and an unacceptable reference 422 |
| TC-P10-TE013-CON-05 | AC5, BR7, BR9 | Contract | The record of a SHADOW step: agent version "INTAKE@P1/PR1", final call "RESUME_STATE", the actions, decision code D6, a registry refusal and the `.dlt` route, and a record refused by the ledger ingest with MSG-P7-009 naming the field, an alert and no ledger entry |
| TC-P10-TE013-CON-06 | AC6, BR10 | Contract | The nine sub-tables with None where empty, the run read aligned to the baseline, and the three fakes answering every consumed path and payload |
| TC-P10-TE013-CON-07 | 12.7 (ASM-3438) | Contract | Each table of 12.7 read or written at its boundary: an access outside its contracted use refused, a write to another service's schema refused, and no foreign key crossing a schema |
| TC-P10-TE013-CON-08 | AC7, BR4 | Contract | The step operation answering after the 60-second policy timeout as the one exception, and every other hop expiring at 2 seconds |
| TC-P10-TE013-CON-09 | AC7, BR8 | Contract | The modes, the timeout, the agent codes, the check codes and the reason codes read from the policy, the reference data and the library, and none of them written as a value in the contract or the schema |

The nine test cases are new (D-RCV-60) and test the artefact, not the business behaviour: the legacy ten test cases stay with RWB-P10-TE013-APP, and the `-ITG` copies with RWB-ITG-TE013-ITG. The legacy criterion AC5 of RWB-E1-059 (stale input flagged from a COMPLETED ALS row) is not owned by this story; it and test case TC-E1-059-05 stay with RWB-ITG-E1059-ITG (wave 1).

### 17. Guardrails

- No business value in the contract: the modes, the timeout, the agent codes, the check codes and the reason codes stay rows of the policy, the reference data and the library, and the contract only names them (BR8).
- No personal data in an event, an answer, an example or a fake: identifiers and facts only, the inputs are a masked reference and every fixture is synthetic (BR9).
- The contract names the agent base as rwb-agent's and consumes every other operation; a document that declares another service's base or topic as provided fails the review (BR10).
- The record is declared as the calling step's write through the local library, never as an agent run's write (BR7).
- The record type and the ledger stay with rwb-decision; a drift between this document and RWB-P7-E1027-CON is corrected against the owner.
- The run read is restated, never redefined: the baseline RWB-P10-E1058-CON owns it.
- Every payload is validated against its registry subject before the relay, and a refusal is routed to `.dlt` and alerted (DP-09).
- The contract never names the legacy job table, its admin read or its rerun operation (DP-10).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision records rule, model, agent and prompt versions | The record payload of 12.3 and the answer member decisionLogEntryId | TC-P10-TE013-CON-02, TC-P10-TE013-CON-05 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | The 503 of the record write and the refusal set of the step operation | TC-P10-TE013-CON-01, TC-P10-TE013-CON-05 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | The service identity and the Rules and parameters right of both operations | TC-P10-TE013-CON-01 |
| D-RCV-60 DP-01 | The run and the policy live in `rwb_agent` and every other service's data is read through its contract | The tables of 12.7 and the consumed reads of 12.2 | TC-P10-TE013-CON-04, TC-P10-TE013-CON-06, TC-P10-TE013-CON-07 |
| D-RCV-60 DP-07 | No business value in the contract | The modes, the timeout, the codes and the reason codes named, not declared (BR8) | TC-P10-TE013-CON-09 |
| D-RCV-60 DP-03 | Local decision record plus central ledger | EV-08, its payload and the record read | TC-P10-TE013-CON-05 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | The EV-08 AsyncAPI document, its subject and its `.dlt` route | TC-P10-TE013-CON-05 |
| D-RCV-60 DP-10 | Temporal replaces Quartz | The workflow and activity contract of 12.5 and the absent Schedule of 12.6 | TC-P10-TE013-CON-06 |
| D-RCV-60 DP-11 | Contract-first REST, one hop, 2 s timeout | The two provided operations, the consumed reads and the 60 s budget exception | TC-P10-TE013-CON-01, TC-P10-TE013-CON-06, TC-P10-TE013-CON-08 |
| D-RCV-60 DP-13 | One REST base per service | The base `/api/recovery/agent/v1` and the restated run read | TC-P10-TE013-CON-01, TC-P10-TE013-CON-06 |
| D-RCV-60 DP-20 | Agent client through the rwb-agent contract | The step operation, the link and the legacy member names | TC-P10-TE013-CON-02, TC-P10-TE013-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The operation shapes, the refusals and the fakes | TC-P10-TE013-CON-01, TC-P10-TE013-CON-06 |
| RWB-TE-013 (legacy story) | Agent runtime client with fallback | The members, the step key and the record mapping taken from legacy section 12 | The legacy test cases stay with RWB-P10-TE013-APP |

The gap GAP-0620 records what the sources left open for this document - the member types, the refusal detail, the record reference and the route - and this document fixes them as ASM-0908 to ASM-0911 settle them; only the refusal detail text and the route name wait for their owners.

### 19. Out of scope

- The implementation of the mode resolution, the timed run, the fallback, the record write and the link (RWB-P10-TE013-APP).
- The chart, the migration job, the worker, the wiring, the probes, the alerts, the route publication and the runbook (RWB-P10-TE013-OPS).
- The whole agent platform contract, the eleven operations, the eight tables and the full shape of the run read (RWB-P10-E1058-CON).
- The record library, its envelope and the topic (RWB-PLT-E1027-CON); the record type, the ledger and the record read (RWB-P7-E1027-CON).
- The embedded Drools kit and the rule-package client (RWB-PLT-E1072-CON), and the rule registry and its packages (P7 rwb-decision).
- The reference lists and their versions (P3 rwb-case).
- The agent monitor screen SCR-46 and its dashboard (RWB-E2-031), and the autonomy-level screen (Epic 3).
- The end-to-end proof across services, including the real call type between a calling step and rwb-agent (RWB-ITG-TE013-ITG).
- The case steps that call the client (RWB-E2-028, RWB-E2-029 and the other calling stories).
