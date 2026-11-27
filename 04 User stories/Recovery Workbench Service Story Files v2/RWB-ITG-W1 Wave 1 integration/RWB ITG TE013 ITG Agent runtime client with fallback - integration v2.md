# RWB-ITG-TE013-ITG Agent runtime client with fallback — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-TE-013 for RWB-ITG-W1. The in-process AgentOrchestrator becomes rwb-agent (P10) reached through AgentRunWorkflow on queue `rwb-agent` (DP-20), the decision log writer of P7 becomes the local decision record of the calling service collected into the rwb-decision ledger on `rwb.decision-record.v1` (DP-03), the base moves to `/api/recovery/<short>/v1` (DP-13) and the run and policy reads move to the P10 admin contract. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE013-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-TE013-ITG-16); squad sizes at refinement |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P10-TE013-APP, RWB-P7-TE013-APP |
| Contract dependencies | RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON and RWB-P3-E1043-CON as wave 0 contract fakes; RWB-P10-TE013-CON replaces the agent contract fake when it lands; consumes the contracts of P10, P4, P7 and P3 (§12.2, §12.4); the P4 authorise answer of rwb-access is carried with the two reads |
| Contract version | /v1 path version only; semver not specified in the source documents (DOR-RWB-ITG-TE013-ITG-23) |
| Fake library version | Not specified in the source documents (DOR-RWB-ITG-TE013-ITG-22) |
| Integration dependencies | RWB-P10-TE013-APP, RWB-P7-TE013-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **tech lead** (role code Not specified in the source documents (DOR-RWB-ITG-TE013-ITG-1)), I want **the agent runtime client of `recovery.agent.api` exercised on the real wave-1 services: a calling step in its own service building the rule result first, the client starting AgentRunWorkflow on queue `rwb-agent` inside the approved 60 second budget of the agent policy, the autonomy mode SHADOW, L1 or OFF deciding what is applied, the fallback to the rule result on TIMED_OUT, SCHEMA or NO_POLICY, and one decision record written in the calling service's own schema before the step acts and collected into the rwb-decision ledger on `rwb.decision-record.v1`**, so that **an agent is added to a case step without changing the case flow, the agent answer is never the applied result in SHADOW or L1, and the step does not act at all when its decision cannot be recorded**.

### 2. Business rationale

A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The legacy client put every agent call behind one interface: the rule result always exists, the agent answer is used only as the autonomy mode allows, and the decision log entry records the rule, agent and prompt versions and any fallback (REQ-DRI-001); if the entry cannot be written the step does not act (REQ-DRI-005). The measure is unchanged: the agent fallback rate, target below 10 percent per month.

In the target the client is still a published library inside each calling service (`recovery.agent.api`), but the orchestrator is a service of its own: rwb-agent (P10) owns agent policies, prompts, runs, guardrails and evaluations, runs AgentRunWorkflow with the 60 second budget and then the rule result, publishes `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`, and exposes its runs through `GET /api/recovery/agent/v1/admin/agent-runs` (Arch v5 slides 16, 41 and 42 row 28; DP-20). Its tools read case facts from rwb-source-data (P1) and extracted fields from rwb-document (P5) through their published contracts as read-only calls under SY-AGENT (Arch v5 slide 16; REQ-ACA-010). And the decision record no longer lives in one place: each service writes its own record in its own schema in the same transaction as its state change, and rwb-decision collects it into the central ledger (Arch v5 slides 20 and 28; DP-03, ADR-022).

Three of the facts that make the client trustworthy cannot be proved inside one service, and no single service story owns them:

- The rule-first order is a fact about two services: the calling service must hold the rule result of its own embedded rule package (DP-04) before rwb-agent is asked anything, and the applied result must stay that rule result in SHADOW and L1 while the agent answer appears on the run with agent version "INTAKE@P1/PR1" and confidence 0.91.
- The 60 second budget is a fact about the workflow: the budget belongs to AgentRunWorkflow on queue `rwb-agent` and to the approved policy, never to a caller's REST call, and the expiry must return the rule result to the step and the reason TIMED_OUT to the record (R-UNI-32).
- The record-before-action rule is a fact about three services: the local record commits or rolls back with the step's transaction, exactly one `rwb.decision-record.DecisionRecorded.v1` reaches the shared topic, and rwb-decision holds one ledger entry that a Decision log R holder can read back. A local write that fails must leave the case in "NEW", raise DecisionNotRecordedException with MSG-P7-003 and produce no event and no ledger entry (R-UNI-39).

This integration story is those three facts proved together on real services and real contracts, with the legacy values of RWB-TE-013 kept character for character (agent "INTAKE", policy "P1", prompt "PR1", case "RW-2026-000201", route state "NEW", rule R-UNI-32 version 2026.11, timeout 60 seconds, autonomy SHADOW, L1 and OFF, answer in 2,000 ms, confidence 0.91, fallback reasons TIMED_OUT, SCHEMA and NO_POLICY, step key CASEWF:RW-2026-000201:ENTRY:2026-11-30). The component copies are RWB-P10-TE013-APP (the agent runtime and its run contract) and RWB-P7-TE013-APP (the decision-record library and the ledger read); this story builds neither and proves both.

The only thing stubbed is the outside world: the enterprise model endpoint behind the rwb-agent gateway answers through a recorded stub with a clock and two fault switches, because no suite may call a live model endpoint and the 60 second expiry and the schema failure have to be reached deterministically. The five services in the path are the real SIT services on their published contracts.

### 3. Preconditions

- The nine wave-1 services are deployed in SIT on their published contracts, each with its own schema and login: rwb_source_data, rwb_case, rwb_access, rwb_document, rwb_comms, rwb_decision, rwb_reporting, rwb_agent and rwb_integration (Arch v5 slide 41, wave 1).
- RWB-P10-TE013-APP is done: rwb-agent is deployed with schema `rwb_agent`, `agent_policy`, `agent_prompt` and `agent_run`, the tool gateway, the run read and the two configuration operations of section 12.2, and AgentRunWorkflow is registered on queue `rwb-agent` in namespace `rwb-recovery`.
- RWB-P7-TE013-APP is done: the decision-record library is published, the calling service holds `decision_record` in its own schema with the append-only rule, and rwb-decision holds `decision_log_entry` with its ingest and the `GET /api/recovery/decision/v1/decision-log/{entryId}` read.
- The topic `rwb.decision-record.v1` exists with its retry and `.dlt` topics, and `rwb.agent.events.v1` exists the same way (RWB-PLT-EVT).
- Agent "INTAKE" has approved policy "P1" with timeout 60 seconds, autonomy mode SHADOW, L1 and OFF reachable through the P10 configuration contract, and prompt "PR1" approved (RWB-P10-TE013-APP).
- The identity SY-AGENT exists with its read rights on case facts and extracted document fields, and rwb-access holds the test roles with their Platform administration R and Decision log letters, including RW-CASEOWN without Platform administration R (RWB-P4-E1037-APP).
- The synthetic case "RW-2026-000201" exists in rwb-case in route state "NEW" and status "New", with the facts the agent tools read (RWB-P3-E1018-APP, RWB-P1-E1001-APP).
- The calling steps of the run are the real write paths of rwb-case and rwb-document through the published client library `recovery.agent.api`, with an ArchUnit boundary test that a calling service imports only that package.
- The INT-23 stub of the enterprise model endpoint is deployed with its OpenAPI 3.1 document, its 2,000 ms answer, its clock and its two fault switches.
- The call type between the client and rwb-agent is fixed for this story (GAP-0381; ASM-0551): the client builds the rule result first, starts AgentRunWorkflow on queue `rwb-agent` through the P10 contract with the policy timeout, treats the expiry as TIMED_OUT with the rule result applied, and reads the run, its status and its fallback through `GET /api/recovery/agent/v1/admin/agent-runs`.
- The guardrail check codes used by the fallback are **Not specified in the source documents (GAP-0381; ASM-0552)**: this story treats the codes the agent returns as the fallback reasons, with "SCHEMA" and "TIMED_OUT" as the two the legacy story names.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the two integration dependencies and is run when they are in SIT; a fake is never used in the place of a real service.
- The release date 30 November 2026 is tentative and is copied unchanged.
- Open decisions DL11 and DL33: this story runs on their assumptions, confirmed by the programme directive (DL11: ASM-0553, ASM-0703, ASM-1051, ASM-1104; DL33: ASM-0135, ASM-0140, ASM-0890). The agent timeout is 60 seconds (BR2), and the model endpoint is INT-23, called by rwb-agent only.

### 4. Flow

1. Harness: runs the preflight against the OpenAPI documents of P10, P7, P4 and P3 and the AsyncAPI document of `rwb.agent.events.v1`, and fails before any assertion if a path, a field, a status code or an event schema has drifted, or if a fake is configured for any of the five services.
2. Harness: seeds case "RW-2026-000201" in route state "NEW" and status "New" through the W1J01 synthetic set, and confirms through `GET /api/recovery/case/v1/cases/{caseId}` that the route state is "NEW".
3. Calling step of rwb-case: evaluates its own rule package through the embedded kit and builds the rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE" (DP-04).
4. Calling step: calls `AgentStepClient.runStep` of `recovery.agent.api` with agent "INTAKE", the case ID, the decision code, step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the rule result and the masked inputs.
5. Client: reads the autonomy mode of the policy in force through the P10 configuration contract; on OFF or on a switched-off flag it skips the agent and returns the rule result with fallback false and agent version null.
6. Client: starts AgentRunWorkflow on queue `rwb-agent` with the step key as the workflow ID and the idempotency key, and waits at most the 60 seconds of the policy (ASM-0551).
7. rwb-agent: resolves the approved policy "P1" and prompt "PR1", runs its tool gateway read-only calls to rwb-source-data and rwb-document as SY-AGENT, calls the model endpoint through its gateway, checks the answer, records one run row with agent version "INTAKE@P1/PR1" and publishes `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` in the same transaction (DP-09).
8. Client: in SHADOW it keeps the rule result as the applied result and records the answer on the run only; in L1 it keeps the rule result as the applied result and returns the checked answer with confidence 0.91 as the recommendation for the person who decides.
9. Client: on the 60 second expiry, on a failed guardrail check or on no approved policy, it keeps the rule result and marks the fallback true with reason TIMED_OUT, SCHEMA or NO_POLICY (R-UNI-32).
10. Client: writes one decision record through the decision-record library of RWB-P7-TE013-APP in the calling service's own schema, in the same transaction as the step's state change, with the rule ID and version, agent version "INTAKE@P1/PR1", model version, the recommendation, and actions holding the agent run ID, the mode, fallback and the fallback reason (DP-03).
11. Calling service: the outbox relay publishes exactly one `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed caseId; rwb-decision ingests it into `decision_log_entry` in rwb_decision within 5 minutes (Arch v5 slides 20 and 28).
12. Harness: reads the run through `GET /api/recovery/agent/v1/admin/agent-runs` as a Platform administration R holder, and the record through `GET /api/recovery/decision/v1/decision-log/{entryId}` as a Decision log R holder, and reconciles one run, one event and one entry per step key (R-UNI-40).
13. Harness: forces the local decision-record append to fail inside the step's transaction, confirms that the state change rolls back, that case "RW-2026-000201" stays in "NEW", that DecisionNotRecordedException carries MSG-P7-003, and that no event and no ledger entry exist (R-UNI-39).
14. Harness: repeats the same step key, and confirms one agent run, one decision record and one ledger entry, with the first outcome returned (R-UNI-40).
15. Harness: calls the run read as RW-CASEOWN, confirms the refusal comes from rwb-access through `POST /api/recovery/access/v1/authorise` and answers 403 with MSG-P4-002, cleans up the synthetic set and writes the run report.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent does not answer within 60 seconds | The run ends TIMED_OUT, fallback true, the rule result is applied and the step continues to "RESUME_STATE" | None to a user | AC2 |
| X2 | The answer fails a guardrail check | The rule result is applied, fallback true with the check code the agent returns, for example "SCHEMA" | None to a user | AC4 |
| X3 | No approved policy exists for the agent on the business date | No agent call and no run row; the rule result is applied with fallback true and reason "NO_POLICY" | None to a user | AC5 |
| X4 | The decision record write fails | The step does not act, the case stays in "NEW", no event reaches the topic and no ledger entry exists; an incident is raised | MSG-P7-003 | AC3 |
| X5 | The same step key arrives twice | One agent run, one decision record and one ledger entry; the repeat returns the first outcome | None to a user | AC1 |
| X6 | The autonomy mode is OFF or the flag `rwb.agent.client` is off | No agent call and no run row; the rule result is applied with fallback false and agent version null | None to a user | AC5 |
| X7 | A role without Platform administration R reads agent runs | rwb-access refuses the authorise call and the read answers 403 | MSG-P4-002 | AC5 |
| X8 | A consumed contract drifts from the published one | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1 |

X1 to X7 are the exception paths of the legacy story carried onto the real services, with the decision log entry renamed as the decision record of the calling service; X8 is the failure that only appears when the run leaves one service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test module of its own; it needs rwb-agent, rwb-decision and the published contracts of P4 and P3, not their source code, and it owns no schema and no table |
| Negotiable | Fixture size, wait intervals, poll intervals and report layout are configuration; the agent, the policy and prompt versions, the case, the rule and its version, the timeout, the modes, the confidence, the fallback reasons and the message IDs are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: rule first, the workflow budget, the applied result in SHADOW and L1, three fallbacks, the local record with its event, the ledger entry and the record-before-action rule |
| Estimable | One harness module, six test classes, four fixtures, one fault switch pair, one transaction-failure step and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a response, an event, a run row, a ledger entry, a workflow status, a case state or a message ID |

### 7. Acceptance criteria

```gherkin
Feature: Agent runtime client with fallback, proven across the calling service, rwb-agent and rwb-decision

  Background:
    Given the SIT environment runs rwb-agent (P10), rwb-decision (P7), rwb-access (P4) and the wave-1 calling services on their published contracts
    Given agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1"
    Given case "RW-2026-000201" is in route state "NEW" and status "New" in rwb-case
    Given the calling step has rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE"
    Given the published client library recovery.agent.api is the only agent package a calling service imports

  Scenario: AC1 The client starts AgentRunWorkflow and SHADOW keeps the rule result applied (new, D-RCV-60)
    Given the policy of "INTAKE" has autonomy mode "SHADOW"
    When the calling step calls the client with step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30"
    Then AgentRunWorkflow runs on queue "rwb-agent" with the 60 second budget of policy "P1" and the step key as its workflow ID
    Then the agent answers in 2,000 ms and the run holds agent version "INTAKE@P1/PR1" and confidence 0.91
    Then the client returns the rule result as the applied result, with no agent output to the step, and fallback false
    Then GET /api/recovery/agent/v1/admin/agent-runs shows one run for case "RW-2026-000201" with fallback false, read as a Platform administration R holder
    Then no REST call from the calling service to rwb-agent exists in the trace of the step
    When the same step key is presented again
    Then one agent run and one decision record exist for the key and the repeat returns the first outcome (R-UNI-40)

  Scenario: AC2 The 60 second budget expires and the rule result is applied with TIMED_OUT (new, D-RCV-60)
    Given the agent does not answer within 60 seconds
    When the step runs
    Then the run ends at 60,000 ms with status "TIMED_OUT" and fallback true
    Then the client returns the rule result and the step continues to "RESUME_STATE"
    Then the decision record holds actions fallback true, reason "TIMED_OUT" and the agent run ID (R-UNI-32)
    Then GET /api/recovery/agent/v1/admin/agent-runs shows the same run with status "TIMED_OUT" and fallback true
    Then case "RW-2026-000201" is no longer in route state "NEW" and the step's own state change is the only cause

  Scenario: AC3 One decision record is written before the step acts and collected into the ledger (new, D-RCV-60)
    Given the calling service holds its decision record in its own schema table decision_record, append only
    When the client returns the applied result
    Then the state change of the step, its decision_record row and its outbox row commit in one transaction in the calling service's schema
    Then exactly one rwb.decision-record.DecisionRecorded.v1 event is on rwb.decision-record.v1, keyed caseId
    Then rwb-decision ingests it and decision_log_entry in rwb_decision holds one entry for step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30"
    When a holder of the R right on the decision ledger reads GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the decision record entry holds rule "R-UNI-32" version "2026.11", agent version "INTAKE@P1/PR1" and finalCall "RESUME_STATE"
    When the decision record append fails inside the transaction
    Then the state change rolls back, the step does not act and case "RW-2026-000201" stays in "NEW"
    Then the client raises DecisionNotRecordedException carrying MSG-P7-003 and an incident is raised (R-UNI-39)
    Then no DecisionRecorded event for that step is on the topic and the ledger holds no entry for the step key

  Scenario: AC4 L1 returns the answer as a recommendation and a guardrail failure falls back (new, D-RCV-60)
    Given the policy of "INTAKE" has autonomy mode "L1"
    When the agent answers in 2,000 ms with confidence 0.91
    Then the rule result is the applied result and the outcome returns the agent answer as the recommendation for the person who decides
    Then the decision record holds the agent answer in recommendation with confidence 0.91 and fallback false
    When another call of the client for case "RW-2026-000201" receives an answer that fails check "SCHEMA"
    Then the run holds status "GUARDRAIL_FAILED" with check code "SCHEMA" and fallback true
    Then the applied result stays the rule result and the decision record holds reason "SCHEMA"

  Scenario: AC5 OFF and NO_POLICY make no agent call, and a role without the right is refused (new, D-RCV-60)
    Given the policy of "INTAKE" has autonomy mode "OFF"
    When the step runs
    Then the client makes no agent call and no agent run row exists for case "RW-2026-000201"
    Then the decision record holds agent version null and fallback false
    Given agent "INTAKE" has no approved policy on 2026-11-30
    When the step runs on 2026-11-30
    Then the client makes no agent call and applies the rule result with fallback true and reason "NO_POLICY"
    When synthetic user "RW-CASEOWN" calls GET /api/recovery/agent/v1/admin/agent-runs
    Then rwb-access refuses through POST /api/recovery/access/v1/authorise and the answer is 403 with MSG-P4-002
```

**Target reading.** The agent, the policy and prompt versions, the case, the rule and its version, the timeout, the three autonomy modes, the confidence, the fallback reasons and the step key are the legacy values of RWB-TE-013, copied character for character. The in-process `AgentOrchestrator` of the legacy section 12 becomes AgentRunWorkflow on queue `rwb-agent` behind the P10 contract (DP-20), so the client starts a workflow and reads the run back through `GET /api/recovery/agent/v1/admin/agent-runs` rather than calling a Java interface; the client reaches the workflow through the P10 contract, and when the 60 second budget expires it treats the run as TIMED_OUT, applies the rule result and reads the run and its fallback through the same read (GAP-0381; ASM-0551). The legacy `DecisionLogWriter` of P7 becomes the local decision record of the calling service collected into the rwb-decision ledger (DP-03), so AC3 asserts both the local write and the ledger entry, and the link between the run and the record is held in the record's actions (ASM-0552) and is also set on `agent_run.decision_log_id` by the calling step through the link operation of the P10 contract, not by a direct table write (GAP-0619). The guardrail check codes the agent returns are the fallback reasons, because no source set lists them (ASM-0552). The agent platform of DL33 is rwb-agent (P10), and its task queue `rwb-agent` is the only place a model call is made; no other service and no workflow code calls the model endpoint. The two read-only tools of rwb-agent are case facts and score through the data-product contract of rwb-source-data (P1), and extracted document fields through the REST contract of rwb-document (P5). The fallback-rate measure of RWB-TE-013 (below 10 percent per month) belongs to rwb-reporting under Architecture v5 slide 41; this story asserts only the agent version and the fallback fact on each entry. The operation and parameter names of the measure are Not specified in the source documents (GAP-1316); its definition, target and window take effect as rwb-reporting rows only when approved at the measures review of wave 1. The deployment values, the rwb-agent login name and its secret, the alert thresholds, the runbook text and the route path are Not specified in the source documents (GAP-2189); they are carried as chart values with one reviewed copy per environment, and the login is referenced through a platform secret.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The rule result is computed before the agent is called and is always the applied result in SHADOW and L1 | Agent catalog autonomy levels; agent_policy.autonomy_mode; DP-04 |
| BR2 | If the agent does not answer within agent_policy.timeout_seconds (60, assumed; DL11), the rule result is used and the fallback is recorded on the decision | R-UNI-32; NFR-010; AgentRunWorkflow |
| BR3 | A step acts only after its decision record is written, in the same transaction as its state change | Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR4 | The decision record holds the rule ID, the rule version, the agent version as "<agent>@<policy>/<prompt>", the model version and the recommendation | REQ-DRI-001; decision_log_entry.agent_version |
| BR5 | The idempotency key of the agent run is the step key | R-UNI-40 |
| BR6 | The client runs under the identity of the calling service; rwb-agent runs its tools as SY-AGENT, read only | REQ-ACA-010; Arch v5 slide 16 |
| BR7 | The agent is reached only through AgentRunWorkflow on queue `rwb-agent` and the P10 contract; no calling service calls rwb-agent by REST inside a step, and no caller holds the model budget | Arch v5 slides 12, 16 and 41; DP-20; ASM-0551 |
| BR8 | The 60 second budget is the workflow budget of the agent run and never a REST budget of a caller; every REST call of the harness is one hop with a 2 s client budget | ADR-020; DP-11 |
| BR9 | The run and its fallback are read through `GET /api/recovery/agent/v1/admin/agent-runs`; a caller never reads `agent_run`, `agent_policy` or `decision_log_entry` in another service's schema | DP-01; DP-11 |
| BR10 | One local decision record per step, one `DecisionRecorded` on `rwb.decision-record.v1` and one ledger entry; the record is append only and a correction is a new record naming the one it corrects | DP-03; Arch v5 slides 20 and 28; ADR-022 |
| BR11 | No business value (mode, timeout, threshold, prompt version, fallback reason text) is written in code; the client and the harness read every one of them from the approved policy through the P10 contract | Principle 1; DT02; DP-07 |
| BR12 | The agent answer is never the applied result in SHADOW or L1, and the recommendation returned to a person carries the confidence the guardrail checked | Legacy BR1 and section 17; agent_policy.autonomy_mode |

### 9. State transitions

None of its own for a case status: the client changes no case status, and the calling step moves the case on the applied result.

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | AGENT_UNAVAILABLE | The agent or the model does not answer inside the timeout (R-UNI-32) | RESUME_STATE, with the rule result applied |
| ANY_ACTIVE | DECISION_RECORD_WRITE_FAILED | The record cannot be written (R-UNI-39) | EXCEPTION_QUEUE, raised by the calling step |

The states the harness observes across the services:

| Item | States |
|---|---|
| Agent run (`agent_run`, rwb_agent) | ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, each with fallback true or false |
| AgentRunWorkflow | Running while the 60 second budget holds, Completed with an answer, Completed with the rule result |
| Local decision record (`decision_record`, calling service schema) | Appended with the step's transaction; committed or rolled back with it, never present alone |
| Shared topic | No event for the step, one `DecisionRecorded`, or a retried delivery that the consumer inbox ignores |
| Ledger (`decision_log_entry`, rwb_decision) | No entry, one ingested entry, or an entry appended under the chain |
| Step and case | Step not acted and case still "NEW", or step acted and case moved on the rule result |
| Harness run | Not started, preflight failed, running, passed, failed with the failing criterion named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of this harness | Owns the module, the fixtures, the fault switches, the transaction-failure step and the run report |
| Calling service teams (rwb-case, rwb-document) | Own their step, their rule result, their local decision record and the publish of DecisionRecorded |
| rwb-agent owner (RWB-P10-TE013-APP) | Owns the policies, prompts, runs, guardrails, AgentRunWorkflow, the topic `rwb.agent.events.v1` and the run and configuration reads |
| rwb-decision owner (RWB-P7-TE013-APP) | Owns the decision-record library, the ledger, the ingest and the decision-log read |
| rwb-access owner | Owns the Platform administration R and Decision log R checks and the refusal with MSG-P4-002 |
| RW-PLATADM, RW-COE, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs and fallbacks (Platform administration R) |
| RW-AUDIT, RW-COMPLY, RW-COE and every role holding Decision log R | Read the ledger entry of the step inside their scope |
| SY-CASEWF and the other calling identities | Call the client; write the local decision record through the library |
| SY-AGENT | Runs the agent and its read-only tool calls |
| No role | Reads a service schema directly, writes `agent_run` from outside rwb-agent, or takes production data into the run |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` (rwb_case) | id | Read through the P3 contract; seeded synthetically |
| DF-CAS-007 | `recovery_case` (rwb_case) | route_state | Read through the P3 contract, before and after the step |
| DF-REF-002 | `rule_row` (rwb_decision) | rule_id | Read from the rule result passed in by the calling step |
| DF-REF-003 | `rule_row` (rwb_decision) | rule_version | Read from the rule result passed in by the calling step |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (calling service schema) | all fields | Write (append) by the calling service; read back through the P7 read |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` (rwb_decision) | all fields | Written by rwb-decision on ingest; read through the P7 read |
| DF-AGT-008 | `agent_policy` (rwb_agent) | autonomy_mode | Read through the P10 contract |
| DF-AGT-012 | `agent_policy` (rwb_agent) | timeout_seconds | Read through the P10 contract |
| DF-AGT-021 | `agent_policy` (rwb_agent) | status | Read through the P10 contract |
| DF-AGT-022 | `agent_policy` (rwb_agent) | valid_from | Read through the P10 contract |
| DF-AGT-036 | `agent_run` (rwb_agent) | id | Read through the P10 run read |
| DF-AGT-045 | `agent_run` (rwb_agent) | idempotency_key | Read through the P10 run read |
| DF-AGT-046 | `agent_run` (rwb_agent) | status | Read through the P10 run read |
| DF-AGT-047 | `agent_run` (rwb_agent) | fallback | Read through the P10 run read |
| DF-AGT-058 | `agent_run` (rwb_agent) | decision_log_id | Set by the link operation `PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record`; read through the P10 run read; the caller also writes the run ID into the record's actions (GAP-0619; ASM-0552) |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-TE-013. `agent_policy` and `agent_run` are the P10 tables of schema `rwb_agent`; `decision_log_entry` is the P7 ledger of schema `rwb_decision`; `decision_record` is the append-only local record that every calling service holds in its own schema (DP-03); it is the library table of the P7 decision-record library and is recorded as an object of RWB-P7-TE013-APP, not as an entity of the Logical Data Model or the Data Classification. The harness owns no field and no table: it reads through the operations of section 12 and writes only through the calling services' own write paths, with synthetic values.

The fallback reasons are **Not specified in the source documents (GAP-0381; ASM-0552)** beyond the three the legacy story names ("TIMED_OUT", "SCHEMA", "NO_POLICY"); the harness asserts those three and treats any other guardrail code the agent returns as the reason, without inventing one.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test module and provides no REST operation. The reserved names of P2 rwb-integration — base `/api/recovery/integration/v1`, topic `rwb.integration.events.v1`, queue `rwb-integration`, schema `rwb_integration` — are not used by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | AC1, AC2, AC5: the run listing of case "RW-2026-000201" with status, fallback, agentVersion and idempotency key, and the refusal of RW-CASEOWN |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | AC1, AC4, AC5: policy "P1" and prompt "PR1" in force, the autonomy mode and the 60 second timeout, and the absence of an approved policy on 2026-11-30 |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | AC5: the Platform administration R check behind the run read, and its refusal |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | AC3: the ledger entry of the step, read as a Decision log R holder |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC2, AC3: route state "NEW" of case "RW-2026-000201" before the step and after the rollback |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget. The 60 second budget is not a REST budget: it belongs to AgentRunWorkflow and to policy "P1" (BR8).

#### 12.3 Events published

None. The harness publishes no business event. Every event asserted in this story is produced by a calling service or by rwb-agent and is listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Exactly one event per run, written to the outbox in the same transaction as the run row; run ID, agent "INTAKE", the case ID, status "ANSWERED", "TIMED_OUT" or "GUARDRAIL_FAILED", fallback and agent version "INTAKE@P1/PR1"; CloudEvents 1.0, key caseId, no personal field |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by the calling service; ledger owned by P7 rwb-decision | Exactly one event per step, keyed caseId, written to the outbox in the same transaction as the local record; carries the rule ID and version, agent version "INTAKE@P1/PR1", the mode, fallback and reason in actions, and no personal field |

A consumer dedupes on the event ID through its inbox `processed_event` (DP-09, ADR-015). The payload of the shared decision-record event is the contract of RWB-P7-TE013-APP; where a field is missing from the source set the harness asserts the envelope and the fields of 11 and 12.4 only (GAP-0381). The client reaches the agent through `POST /api/recovery/agent/v1/agent-steps`, which rwb-agent runs as AgentRunWorkflow, and, after the 60 second budget, reads the run through `GET /api/recovery/agent/v1/admin/agent-runs` (GAP-0381; GAP-0619; ASM-0551).

**Client operations of the step.** As fixed by RWB-P10-TE013-CON, the calling step, not the harness, calls `POST /api/recovery/agent/v1/agent-steps` and `PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record`; the harness proves this real cross-service hop through CallerDriver. The step request carries agentCode, caseId, decisionCode, stepKey, ruleResult {ruleId, ruleVersion, toState, result} and inputs (masked). The answer carries decisionLogEntryId, appliedResult {ruleId, ruleVersion, toState, result}, recommendation, fallback, fallbackReason, autonomyMode and agentRunId. The step operation is the one exception to the 2 s client budget: its budget is the policy timeout of 60 seconds. The link body is the record reference, and the link is stored on `agent_run.decision_log_id`. The member types beyond the legacy Java types, the detail text of each refusal, the refusal set of the step operation as reviewed with its owners and the identifier the record reference carries are Not specified in the source documents (GAP-2188). The route is named when RWB-PLT-N001-CON is baselined.

**Decision record event.** The calling service appends the record locally in its own schema and transaction through the DP-03 library and publishes DecisionRecorded on `rwb.decision-record.v1` from its outbox; rwb-decision collects it into the ledger. This supersedes the legacy RWB-TE-013 sentence on the client and the decision log writer: the client of rwb-agent publishes no DecisionRecorded event (GAP-2422).

**Decision entry of an agent step.** The entry carries the decision code in force from LOV-DECISION, read with its version; the fixtures carry "D6". `actions` holds agentRunId, mode, fallback and fallbackReason, and recommendation and finalCall stay separate fields (GAP-1315; GAP-2417). The code of an agent step is settled with the reference-data owner before the first joint environment. The field set of the ledger read answer is Not specified in the source documents (GAP-1315).

**Refused record.** A record that rwb-decision refuses is answered with MSG-P7-009 naming the field, is held for the retry and dead-letter path with an alert, and adds nothing to the ledger (GAP-1317).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (started by the client, P10) | `rwb-agent` | One run: resolve the approved policy and prompt, run the read-only tool calls, mask, call the model gateway with the 60 s budget, check the answer, record the run row and its outbox event; on expiry it ends and hands the rule result back (Arch v5 slide 16: "AgentRunWorkflow: 60 s, then rule result"; DP-10; DP-20) |
| Decision-record ingest of rwb-decision | Activity (observed, P7) | `rwb-decision` | Appends the record of the calling service to `decision_log_entry` within 5 minutes; owned by RWB-P7-TE013-APP and observed here through the decision-log read |

The harness starts no workflow of its own: the calling step reaches AgentRunWorkflow through the client of the platform contract, and the harness observes it through the Temporal visibility query with the step key as workflow ID (ASM-0551). The tool calls and the gateway call are activities of rwb-agent and are asserted through the run row and the event, never started by the harness.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story. The step that calls the client is started by the case flow, not on a cadence, so the harness triggers nothing on a schedule and registers none.

#### 12.7 Tables owned

None. The harness owns no table and never reads a service schema (DP-01). It exercises `agent_policy`, `agent_run` and `agent_prompt` of `rwb_agent` (owner P10), `decision_record` of the calling service's schema (owner that service, library of P7), and `decision_log_entry` of `rwb_decision` (owner P7), every one of them through a contract of section 12.

#### 12.8 Contract fakes

None for the nineteen services: rwb-agent, rwb-decision, rwb-access and rwb-case are the real SIT services on their published contracts, and a run configured with a fake for any of them fails the preflight. The only stub is outside the services:

| Stub | Purpose |
|---|---|
| INT-23 stub of the enterprise model endpoint, with its OpenAPI 3.1 contract | Stands in for the live endpoint behind the rwb-agent gateway; returns the 2,000 ms answer with confidence 0.91 for AC1, AC3 and AC4 |
| Clock | Holds the business date at 2026-11-30 for AC1, AC3 and AC5 and moves the call across the policy validity for AC5 |
| Fault switch: timeout | Makes the stub silent for 61 seconds, so the workflow budget of 60 seconds expires, for AC2 |
| Fault switch: schema | Returns an answer that fails check "SCHEMA", for AC4 |

The policy states are reached through the P10 configuration contract, never through a stub: the OFF and L1 modes are approved policy versions, and the NO_POLICY branch is reached by retiring the approved policy so that none is in force on 2026-11-30.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 5 | The two P10 reads, the P4 authorise call, the P7 decision-log read and the P3 case read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 2 event types | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` and `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`; CloudEvents 1.0, key caseId (DP-09, DP-14) |
| Temporal | None | 1 workflow started, 1 activity observed | AgentRunWorkflow on queue `rwb-agent` in namespace `rwb-recovery`; the P7 ingest activity observed through the ledger |
| File | None | None | No file in this story |

### 13. Solution plan

**Deliverables.** One harness module `integration/recovery-w1/agent-client`, with the six test classes `ClientContractIT`, `RuleFirstShadowIT`, `TimeoutFallbackIT`, `DecisionRecordIT`, `ModeAndGuardrailIT` and `AccessRefusalIT`, the fixture files, the fault switches and the run report writer. No service code and no schema change: the module builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight against the four OpenAPI documents and the AsyncAPI document, run order, report and exit code |
| PolicyFixture | Service | Loads and approves policy "P1" with timeout 60 seconds and prompt "PR1", sets the modes SHADOW, L1 and OFF, and retires the policy for the NO_POLICY branch, all through the P10 contract |
| CallerDriver | Service | Drives the real write path of rwb-case and rwb-document through `recovery.agent.api`, with the step key and the rule result of the fixture |
| WorkflowProbe | Service | Reads AgentRunWorkflow on queue `rwb-agent` through the visibility query and asserts the workflow ID, the 60 second budget, the status and the rule result handed back |
| RunProbe | Service | Reads the run through `GET /admin/agent-runs` and asserts status, fallback, agent version, confidence and the idempotency key |
| EventProbe | Service | Consumes `rwb.agent.events.v1` and `rwb.decision-record.v1` and asserts one event per run and per step, the outbox fact, the envelope and the absence of a personal field |
| RecordProbe | Service | Reads the ledger entry through `GET /api/recovery/decision/v1/decision-log/{entryId}` and compares the rule, the version, the agent version, the actions and the final call |
| TransactionFailureTool | Service | Forces the local append of `decision_record` to fail inside the step's transaction, then confirms the rollback and the refused state change |
| AccessProbe | Service | Calls the run read as RW-CASEOWN after the P4 authorise call and asserts 403 with MSG-P4-002 |
| ModelStubControl | Service | Deploys the INT-23 stub from its OpenAPI 3.1 document, sets the 2,000 ms answer, the clock and the two fault switches |
| ReportWriter | Service | One row per test case, with the evidence and the elapsed times |

**Database.** None of its own. The harness writes only through the calling services' own write paths, and its single direct write is the DEV-only transaction failure of AC3, which is refused outside DEV and SIT.

**Configuration and reference data**

- The SIT endpoints of P10, P7, P4 and P3, the topics `rwb.agent.events.v1` and `rwb.decision-record.v1`, queue `rwb-agent` and namespace `rwb-recovery`, all as configuration.
- The agent "INTAKE", the policy "P1", the prompt "PR1", the timeout 60 seconds, the confidence 0.91, the answer 2,000 ms, the three autonomy modes, case "RW-2026-000201", rule "R-UNI-32" version "2026.11", the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" and the business date 2026-11-30, read through the P10 contract and never written in the harness code (BR11).
- The decision codes and the reference values the fixtures use, read through the rwb-case reference-data contract (DP-07).
- The 2 s client budget, the 60 s workflow budget, the 5 minute ledger catch-up and the poll interval.
- The environment values of the rwb-agent deployment of RWB-P10-TE013-OPS, held as reviewed values per environment and never as template constants, with the login taken through a secret reference and granted on `rwb_agent` only. The login and secret name; the partitions, replication factor, retention, retry topic name, `.dlt` topic name and producer credential owner of `rwb.decision-record.v1`; the worker concurrency, pollers, activity timeouts and identity; the alert thresholds; the route path; and the capacity figures are Not specified in the source documents (GAP-0621).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

The H/C/X dependencies the DPs name (notably DP-20 C RWB-P10-TE013-CON, DP-03, DP-04, DP-09, DP-10) stay with the service and platform stories this harness proves; this story carries no H, C or X dependency and its I list names the two stories whose behaviour it exercises (§R5.4).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Policy set | Policy "P1" of agent "INTAKE" with timeout 60 seconds and prompt "PR1", approved in SHADOW, in L1 and in OFF, and retired for the NO_POLICY branch | AC1 to AC5 |
| Stub answers | The 2,000 ms answer with confidence 0.91, the 61 second silence and the answer that fails check "SCHEMA", held by ModelStubControl | AC1, AC2, AC4 |
| Synthetic case | Case "RW-2026-000201" in route state "NEW" and status "New", with a step that calls the client through the real write path of rwb-case and one through rwb-document | AC1 to AC5 |
| Rule result | Rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE", built by the calling step through the embedded kit | AC1 to AC5 |
| Role set | RW-PLATADM, RW-AUDIT and RW-COMPLY with Platform administration R, RW-COE with Decision log R, and RW-CASEOWN without Platform administration R | AC1, AC3, AC5 |

**Run order.** Preflight; policy and mode fixture; SHADOW run with the workflow and the run read (AC1); L1 and the guardrail failure (AC4); the timeout (AC2); the local record, its event and the ledger entry, then the forced transaction failure (AC3); OFF, NO_POLICY and the refused run read (AC5); cleanup of the synthetic case, the retired policy version and the stub. A failing step stops the run and the report names the criterion, the service and the evidence.

**Done when.** The fifteen test cases of section 16 pass on the real services in SIT, the five criteria of section 7 are signed off, AgentRunWorkflow is observed on queue `rwb-agent` with the 60 second budget, exactly one run, one event and one ledger entry exist per step key, the forced failure leaves case "RW-2026-000201" in "NEW" with MSG-P7-003, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right reads agent runs | You cannot {action} here. Your role does not include it. |
| MSG-P7-009 | A record is refused for a missing or invalid field (written to the service log and the incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. |

The texts of MSG-P7-003 and MSG-P4-002 are copied unchanged from RWB-TE-013, and the text of MSG-P7-009 is copied unchanged from RWB-PLT-E1027-APP; this story creates no new message ID. Report lines of the harness are for developers and are not part of the message standard.

The Error and Message Standard v4 carries the chain verifier break as MSG-P7-008. The identifier and text of the not-found answer of the decision-log read are Not specified in the source documents (GAP-2418). This harness asserts neither outcome.

### 15. Screens and states

No screen in this story. A fallback shows in `GET /api/recovery/agent/v1/admin/agent-runs` (fallback true) and on the decision record of the case, which a Decision log R holder reads through the P7 read. The listing states the harness asserts are an empty result for a case with no run, a list of runs with id, agent, agentVersion, caseId, status, fallback and latency, and one run in each of the three statuses. The agent monitor screen SCR-46 and the autonomy-level screen come with RWB-E2-031 and Epic 3 and are out of scope; the Screen Specifications give SCR-46 the states Shadow, live and paused, and for no access Platform administration is checked on every request and an action outside the role shows MSG-P4-002; the SCR-46 empty, loading and error states are Not specified in the source documents (DOR-RWB-ITG-TE013-ITG-10; CG-ALL-512); no gateway-bff composite route is exercised (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-013-01-ITG | legacy AC1, BR1, BR4 | Integration | Case RW-2026-000201, mode SHADOW, agent answers in 2,000 ms, agent version INTAKE@P1/PR1 |
| TC-TE-013-02-ITG | legacy AC2, BR2 | Integration | Agent silent for 61 seconds; run TIMED_OUT at 60,000 ms, fallback true, rule result applied |
| TC-TE-013-03-ITG | legacy AC3, BR1 | Integration | Mode L1, confidence 0.91, recommendation returned and recorded |
| TC-TE-013-04-ITG | legacy AC4 | Integration | Answer fails check SCHEMA; fallback true with reason SCHEMA |
| TC-TE-013-05-ITG | legacy AC5 | Integration | No approved policy on 2026-11-30; no agent call, reason NO_POLICY |
| TC-TE-013-06-ITG | legacy AC6, BR3 | Integration (run by RWB-P10-TE013-APP) | Decision record write throws; step does not act; MSG-P7-003; no event and no entry |
| TC-TE-013-07-ITG | legacy AC7, BR5 | Integration (run by RWB-P10-TE013-APP) | Step key CASEWF:RW-2026-000201:ENTRY:2026-11-30 twice; one run and one record (R-UNI-40) |
| TC-TE-013-08-ITG | legacy AC8 | Integration (run by RWB-P10-TE013-APP) | Mode OFF; no agent call, no run row, agent version null, fallback false |
| TC-TE-013-09-ITG | Access | Integration | RW-CASEOWN calls GET /admin/agent-runs; refused through P4 with MSG-P4-002 |
| TC-TE-013-10-ITG | Principle 5 | Integration | Decision record write forced to fail during a step in SHADOW mode; the step does not act; MSG-P7-003 |
| TC-ITG-TE013-01 | AC1, BR7, BR9 | End to end | One step in rwb-case through the client; AgentRunWorkflow observed on rwb-agent; one run read back; no direct REST from the caller |
| TC-ITG-TE013-02 | AC2, BR2, BR8 | End to end | Stub silent for 61 seconds; the workflow budget of 60 seconds expires; rule result applied; reason TIMED_OUT in the record |
| TC-ITG-TE013-03 | AC3, BR3, BR10 | Integration | One local decision_record row, one DecisionRecorded on rwb.decision-record.v1 and one ledger entry read through the P7 read; then the local append forced to fail |
| TC-ITG-TE013-04 | AC4, BR1, BR12 | Component | Mode L1 with confidence 0.91, then an answer failing check SCHEMA; applied result unchanged |
| TC-ITG-TE013-05 | AC5, BR5, BR6, BR11 | Contract | Mode OFF, no approved policy on 2026-11-30, and RW-CASEOWN refused with MSG-P4-002 |

The legacy acceptance criteria of RWB-TE-013 (AC1 to AC8 and the access and principle-5 checks of TC-TE-013-09 and TC-TE-013-10) are owned by RWB-P10-TE013-APP; RWB-P7-TE013-APP owns no legacy criterion of this key and carries the decision-record part of sections 11 and 12, and both are re-exercised here on the real services; the legacy test case IDs are kept as ITG copies with the suffix `-ITG` and their Covers cell names the legacy criterion and rule, and the five new criteria AC1 to AC5 carry TC-ITG-TE013-01 to TC-ITG-TE013-05. Rows TC-TE-013-01-ITG to TC-TE-013-10-ITG are ITG copies of legacy criteria owned by RWB-P10-TE013-APP; this story owns only AC1 to AC5.

### 17. Guardrails

- No business value in code: the mode, the timeout, the prompt version, the confidence and the fallback reason text come from the approved policy through the P10 contract, and the decision codes from the rwb-case reference-data contract (DP-07).
- No personal data in events, workflow inputs, logs, fixtures or the report: case IDs, agent codes, version labels, rule IDs, step keys, statuses and codes only, and every case and identity of the run is synthetic.
- No cross-service table read: the run and the policy are read through the P10 contract, the ledger through the P7 read and the case state through the P3 read, and a pipeline scan fails any change that adds a schema connection (DP-01).
- The agent answer is never the applied result in SHADOW or L1 (BR12), and no caller holds the 60 second model budget as a REST budget (BR8).
- One decision record, one event and one ledger entry per step key: the local append is inside the caller's transaction and is the last statement before the step acts (BR3, BR10, R-UNI-39).
- The client is reached only through the published package `recovery.agent.api`, with an ArchUnit boundary test that a calling service imports nothing else of rwb-agent (DP-20).
- One hop and a 2 s client budget on every REST call of the harness; the harness calls no service through another service (ADR-020).
- No production access and no production namespace: the run is pinned to SIT with the synthetic set and refuses to start against any other environment; the transaction failure of AC3 runs in DEV and SIT only.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | `decision_record` in the calling service schema, `rwb.decision-record.DecisionRecorded.v1`, `decision_log_entry`, `GET /api/recovery/decision/v1/decision-log/{entryId}` | TC-TE-013-01-ITG, TC-TE-013-03-ITG, TC-ITG-TE013-03 |
| REQ-DRI-005 | No action proceeds if its decision record cannot be written | The append in the caller's transaction, DecisionNotRecordedException, MSG-P7-003 | TC-TE-013-06-ITG, TC-TE-013-10-ITG, TC-ITG-TE013-03 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | SY-AGENT tool path, `POST /api/recovery/access/v1/authorise`, MSG-P4-002 | TC-TE-013-05-ITG, TC-TE-013-07-ITG, TC-TE-013-08-ITG, TC-TE-013-09-ITG, TC-ITG-TE013-05 |
| DP-03 | Local decision record and the shared topic | `rwb.decision-record.v1`, the append-only local record, the ledger read | TC-TE-013-06-ITG, TC-ITG-TE013-03 |
| DP-04 | Embedded Drools kit and rule packages from rwb-decision | The rule result rule "R-UNI-32" version "2026.11" built before the client is called | TC-TE-013-01-ITG, TC-ITG-TE013-01 |
| DP-09 | Outbox, inbox and CloudEvents | One event per step and per run, key caseId | TC-ITG-TE013-01, TC-ITG-TE013-03 |
| DP-10 | Workflow kit and the task queue | AgentRunWorkflow on queue `rwb-agent` with the 60 second budget | TC-ITG-TE013-01, TC-ITG-TE013-02 |
| DP-11 | One hop and a 2 s timeout | The five calls of 12.2 and the preflight contract test | TC-TE-013-05-ITG, TC-ITG-TE013-05 |
| DP-13 | `/api/recovery/<short>/v1` | `/api/recovery/agent/v1`, `/api/recovery/decision/v1`, `/api/recovery/access/v1`, `/api/recovery/case/v1` | Every test case, at the preflight |
| DP-20 | Agent client through the rwb-agent contract | `recovery.agent.api` and AgentRunWorkflow on queue `rwb-agent` | TC-TE-013-01-ITG, TC-ITG-TE013-01, TC-ITG-TE013-02 |
| ASM-0551 | The client starts AgentRunWorkflow on queue `rwb-agent` through the P10 contract, treats the 60 s expiry as TIMED_OUT and reads the run and its fallback through the admin run read | AgentRunWorkflow and `GET /api/recovery/agent/v1/admin/agent-runs` | TC-ITG-TE013-01, TC-ITG-TE013-02 |
| ASM-0552 | The guardrail failure reasons are the codes the agent returns, and the link from the run to the record is held in the record's actions | The actions of the decision record and the run read | TC-TE-013-04-ITG, TC-ITG-TE013-04 |
| RWB-TE-013 (legacy story) | The client, the modes, the fallback and the record-before-action rule: AC1 to AC8 and the two checks | The five operations, the two events and the started workflow of section 12 | The fifteen test cases of section 16 |
| RWB-P10-TE013-APP (component copy) | The agent runtime of rwb-agent: policies, prompts, runs, guardrails and AgentRunWorkflow | The P10 contract and queue `rwb-agent` | TC-ITG-TE013-01, TC-ITG-TE013-02 |
| RWB-P7-TE013-APP (component copy) | The decision-record library, the local record, the ledger and its read | `decision_record`, `rwb.decision-record.v1`, `decision_log_entry`, the decision-log read | TC-ITG-TE013-03 |

### 19. Out of scope

- The agent runtime, its tables, AgentRunWorkflow and the run and configuration reads (RWB-P10-TE013-APP), and its contract (RWB-P10-TE013-CON).
- The decision-record library, the local record, the ledger, the ingest and the decision-log read (RWB-P7-TE013-APP).
- The deployment, the topic provisioning and the queue registration (RWB-P10-TE013-OPS).
- The model endpoint and its gateway choice (DL33), the guardrail checker (RWB-E1-058 and RWB-ITG-E1058-ITG) and the masking path (RWB-E1-037).
- Agent answers acted on without a person: autonomy L2 and above (Epic 8, FEAT-AGT-15).
- The case steps that call the client: case intake (RWB-E2-028) and deviation screening (RWB-E2-029); this story drives the step through the published library and owns none of it.
- The agent monitor screen SCR-46, the cost alert and the autonomy-level screen (RWB-E1-063, RWB-E2-031, Epic 3).
- Building the harness RWB-ITG-W1J01-ITG itself and the non-functional epic RWB-ITG-NFR.
