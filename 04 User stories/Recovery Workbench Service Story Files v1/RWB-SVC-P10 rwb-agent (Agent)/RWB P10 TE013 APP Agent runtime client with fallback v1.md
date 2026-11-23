# RWB-P10-TE013-APP Agent runtime client with fallback

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-TE013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1058-APP |
| Depends on (build) | RWB-P10-TE013-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-E1058-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | RWB-P10-TE013-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-018, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-TE-013 for rwb-agent. In the monolith the key is one published Java interface in `recovery.agent.api`, an `AgentOrchestrator.run` call in the same JVM, a P7 `DecisionLogWriter` of the same deployment and a Quartz job step (RWB-TE-007) that brought it into a case step. The target turns each of those into a boundary: the client becomes the rwb-agent contract reached through the `recovery.agent.api` library (**DP-20**), the orchestrator becomes AgentRunWorkflow on queue `rwb-agent` (**DP-10**), the entry becomes the local decision-record library plus the topic `rwb.decision-record.v1` (**DP-03**, **DP-09**), the shared `RuleEvaluator` becomes the embedded Drools kit with packages from rwb-decision (**DP-04**), and the step and link operations are served on `/api/recovery/agent/v1` (**DP-13**) with rows in `rwb_agent` only (**DP-01**), lists from the rwb-case reference-data contract (**DP-07**), the run read behind the gateway-bff route (**DP-19**) and the one migration in the service's own Flyway sequence (**DP-15**). Every legacy value, ID, message ID, timeout, threshold and test case ID is kept. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one agent runtime client in rwb-agent - the `AgentStepClient` operation on `/api/recovery/agent/v1/agent-steps` plus the `recovery.agent.api` library that every calling step uses - that applies the autonomy mode of the approved policy in force, runs shadow mode, falls back to the rule result with reason TIMED_OUT, SCHEMA or NO_POLICY inside the 60 second budget, records the decision through the local decision-record library before the step acts, and links the run to that record**, so that **agents are added to a case step without changing the case flow, every step records what the agent did and why the rule result was applied, and no step acts on an answer whose decision could not be recorded**.

### 2. Business rationale

A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The legacy client put every agent call behind one interface: the rule result always exists, the agent answer is used only as the autonomy mode allows, and the decision log entry records the rule, agent and prompt versions and any fallback (REQ-DRI-001). If the entry cannot be written, the step does not act (REQ-DRI-005). The measure is the agent fallback rate, target below 10 percent per month.

In the target every element of that interface is a boundary:

- The orchestrator is rwb-agent's `AgentRunWorkflow` on its own task queue, with the approved policy's 60 second budget inside it (Arch v5 slide 16, "AgentRunWorkflow: 60 s, then rule result"; DP-20).
- The interface a caller compiles against is still `recovery.agent.api`, but it is a library over a REST contract with a fake, one hop, on the owner's base (DP-11, DP-13).
- The record is no longer one service's writer: the step writes its own record in its own schema through the shared library, and rwb-decision owns the type and collects the central ledger (DP-03).
- The rule result is not taken from a shared bean: the calling step evaluates its package through the embedded Drools kit with the packages published from rwb-decision (DP-04).
- The Quartz job step is retired with RWB-TE-007 and becomes a Temporal step of the calling service through the workflow kit (DP-10).

What does not change is the order the legacy story fixes: rule first, agent second, record before action. The seven legacy exception paths keep their triggers, reasons and messages, the eight legacy criteria are kept word for word with their origin tags, and the legacy test cases keep their IDs and data. The cross-service behaviour of this key is proved by RWB-ITG-TE013-ITG, which is why this story carries no integration dependency (I = None).

### 3. Preconditions

- RWB-P10-E1058-APP is done: the eight agent tables exist in `rwb_agent`, AgentRunWorkflow is registered on queue `rwb-agent` with its activities, and `agent_run` holds DF-AGT-045 idempotency_key and DF-AGT-058 decision_log_id.
- RWB-P10-TE013-CON is published: the step operation, the link operation, their members, the idempotency rules, the refusal codes and the three fakes.
- RWB-PLT-E1027-CON is published (decision-record library, its outbox write in the caller's transaction and `rwb.decision-record.v1`; DP-03); RWB-PLT-E1072-CON (embedded Drools kit and rule-package client; DP-04); RWB-PLT-E1043-CON (reference-data client library; DP-07); RWB-PLT-TE006-CON (outbox and inbox library, relay and `.dlt` rule; DP-09); RWB-PLT-E1071-CON (workflow kit, namespace `rwb-recovery`; DP-10); RWB-PLT-E1044-CON (per-service Flyway sequence; DP-15); RWB-PLT-N001-CON (gateway-bff route contract and stub; DP-19).
- The `rwb_agent` baseline applies `V10_001__agent_runtime.sql`; this story's `V10_002__agent_run_decision_link.sql` applies after it in the rwb-agent sequence.
- RWB-P3-E1043-CON is published: `GET /api/recovery/case/v1/admin/lists/{listCode}` answers LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT with the version in force (DP-07). RWB-P7-E1027-CON is published: the record read by its reference and the record type and central ledger are P7's (DP-03).
- An approved `agent_policy` row exists for the agent and the business date, with autonomy_mode SHADOW, L1 or OFF, timeout_seconds 60 (legacy value; DL11) and prompt_version PR1; the mode, the timeout and the prompt version are rows of the policy and never code.
- The calling service runs under its own service identity and has evaluated its rule through the embedded Drools kit before it calls the client; rwb-agent runs under the rwb-agent login (DP-02), whose name is Not specified in the source documents (GAP-0619; ASM-0906).
- The step operation `POST /api/recovery/agent/v1/agent-steps` and the link operation `PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record` are this story's names for the two boundaries the legacy Java interface spans; no source names a run-submit operation among the eleven P10 operations (GAP-0619; ASM-0902), and the call type between a calling step and rwb-agent is Not specified in the source documents (GAP-0619; ASM-0904).
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. The calling step evaluates its rule package through the embedded Drools kit with the package published from rwb-decision and builds the rule result: rule ID "R-UNI-32", rule version "2026.11" and the next state (DP-04; legacy step 1).
2. The calling step calls `AgentStepClient.runStep` with the agent code, case ID, decision code, step key and rule result; the library submits to `POST /api/recovery/agent/v1/agent-steps` with the step key as the `Idempotency-Key` and the masked inputs, one hop (DP-11, DP-20; legacy step 2).
3. rwb-agent reads the autonomy mode and the timeout of the approved policy in force from `agent_policy` in `rwb_agent`; when the mode is OFF, or the flag `rwb.agent.client` is off, it skips the agent: no AgentRunWorkflow and no run row (AC8; legacy step 3).
4. Otherwise it starts AgentRunWorkflow on queue `rwb-agent` with the step key as the workflow ID and as the run's idempotency key, and waits at most `agent_policy.timeout_seconds`: 60 seconds (AC1, AC2; DP-10; legacy step 4).
5. SHADOW: it keeps the rule result as the applied result, stores the agent answer on the run and answers recommendation null (AC1; legacy step 5).
6. L1: it keeps the rule result as the applied result and answers the checked agent answer as the recommendation for the person who decides, with its confidence, 0.91 in the fixture (AC3; legacy step 6).
7. On a timeout or a guardrail failure it keeps the rule result and marks fallback true with the reason, TIMED_OUT or the check code SCHEMA (R-UNI-32; AC2, AC4; legacy step 7).
8. The client writes one decision record through the local decision-record library, in the calling service's schema and transaction, with the rule ID and version, the agent version, the model version, the recommendation and the fallback; the library publishes EV-08 on `rwb.decision-record.v1` (DP-03, DP-09; legacy step 8).
9. The client then links the run to the record with `PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record`; rwb-agent sets `agent_run.decision_log_id` (DF-AGT-058) once: the same record answers the same run, a different record is refused with 409 (AC1, AC7; legacy step 8).
10. The calling step acts on the applied result only after the record and the link exist; if the record cannot be written it does not act, case "RW-2026-000201" stays in "NEW", the client raises `DecisionNotRecordedException` carrying MSG-P7-003, an incident is raised (R-UNI-39) and the run keeps `decision_log_id` empty (AC6; legacy step 9).
11. The same step key presented again returns the first outcome: one run row, one record and one link for the key, counted as an idempotency hit (R-UNI-40; AC7).
12. The run read `GET /api/recovery/agent/v1/admin/agent-runs` is the baseline of RWB-P10-E1058-CON and is not re-declared here; a reader reaches it through the gateway-bff route (DP-19; AC2, AC7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent does not answer within 60 seconds | Rule result applied; fallback true with reason TIMED_OUT; step continues | None to a user | AC2 |
| X2 | The answer fails a guardrail check | Rule result applied; fallback true with the check code | None to a user | AC4 |
| X3 | No approved policy exists for the agent on the business date | No agent call; rule result applied; fallback true with reason NO_POLICY | None to a user | AC5 |
| X4 | The decision record write fails | The step does not act; the case stays in its state; an incident is raised (R-UNI-39) | MSG-P7-003 | AC6 |
| X5 | The same step key arrives twice | One agent run, one record and one link; the repeat returns the first outcome (R-UNI-40) | None to a user | AC7 |
| X6 | Autonomy mode OFF or flag `rwb.agent.client` off | No agent call; rule result applied; fallback false; no agent run row | None to a user | AC8 |
| X7 | A role without the right reads agent runs | Refused with 403 | MSG-P4-002 | TC-TE-013-09 |
| X8 | The step operation is called with no step key or no rule result | Refused with 422 and no run is started; proved by RWB-P10-TE013-CON | MSG-GEN-001 | TC-P10-TE013-CON-01 |
| X9 | The same step key is presented while its first run is RUNNING | Refused with 409 while the run is RUNNING; answers the first outcome once the run and the record exist (R-UNI-40) | None to a user | AC7 |
| X10 | The reference-data contract does not answer inside 2 s | No mode is applied and no run is started with a guessed mode; 503 | None to a user | AC1 |
| X11 | The link is refused because the run holds a different record | The first record stands; the link is not overwritten; the mismatch is raised to the data steward | None to a user | AC7 |
| X12 | The migration `V10_002__agent_run_decision_link.sql` fails | The new version does not start; the version in force keeps serving; no run is linked | None | AC1 |

X1 to X7 are the legacy exception paths with the same triggers and messages. X8 to X12 appear when the interface becomes a contract, when the record leaves the service and when the migration owns the link column. X7 is not reached by a criterion of this story: it is proved by TC-TE-013-09 at Contract level.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the platform contract stories, the published P3 and P7 contracts with their fakes and the in-lane story RWB-P10-E1058-APP; owns its two operations and its one migration |
| Negotiable | Package layout, component and activity names, member order and internal timeouts are design; the agent, policy and prompt versions, the rule and version, the case, the step key, the timeout 60, the modes, the confidence 0.91, the 2,000 ms answer, the three reasons and the two message IDs are fixed by the legacy story |
| Valuable | Every agent from RWB-E1-059 onward plugs into case steps through this one boundary, with a record written before the step acts |
| Estimable | Two operations, one client library, three activities, one migration, seven components, two contract clients and three fakes |
| Small | Under one week with its tests, as in the legacy estimate; the in-process orchestrator is replaced by the workflow start |
| Testable | Each of the eight criteria is one automated test on an observable: a stored run, a record reference, a link column, an answered outcome, a refusal or a raised exception |

### 7. Acceptance criteria

```gherkin
Feature: Agent runtime client with fallback

  Background:
    Given agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1"
    Given case "RW-2026-000201" is in route state "NEW" and status "New"
    Given the calling step has rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE"

  Scenario: AC1 Shadow (legacy RWB-TE-013 AC1)
    Given the rwb-decision decision-record contract mock returns a written entry id
    Given the policy of "INTAKE" has autonomy mode "SHADOW"
    When the agent answers in 2,000 ms with a valid output
    Then the system stores the agent answer on the agent run and the rule result is the applied result
    Then one decision log entry holds agent version "INTAKE@P1/PR1", the rule ID and version, recommendation null and fallback false in actions
    Then the calling step receives the rule result and no agent output

  Scenario: AC2 No answer (legacy RWB-TE-013 AC2)
    Given the rwb-decision decision-record contract mock returns a written entry id with fallback true and reason "TIMED_OUT"
    Given the agent does not answer in 60 seconds
    When the step runs
    Then the system uses the rule result and the step continues to "RESUME_STATE"
    Then the decision log entry holds actions fallback true with reason "TIMED_OUT" and the agent run ID (R-UNI-32)
    Then the agent run holds status "TIMED_OUT" and fallback true

  Scenario: AC3 Assisted mode returns the answer as a recommendation (legacy RWB-TE-013 AC3)
    Given the rwb-decision decision-record contract mock returns a written entry id carrying the recommendation
    Given the policy of "INTAKE" has autonomy mode "L1"
    When the agent answers with confidence 0.91
    Then the rule result is the applied result
    Then the outcome returns the agent answer as the recommendation for the person who decides
    Then the decision log entry holds the agent answer in recommendation with confidence 0.91

  Scenario: AC4 A guardrail failure falls back (legacy RWB-TE-013 AC4)
    Given the rwb-decision decision-record contract mock returns a written entry id with fallback true and reason "SCHEMA"
    Given the agent answer fails check "SCHEMA"
    When the step runs
    Then the system applies the rule result
    Then the decision log entry holds actions fallback true with reason "SCHEMA"

  Scenario: AC5 No approved policy (legacy RWB-TE-013 AC5)
    Given the rwb-decision decision-record contract mock returns a written entry id with fallback true and reason "NO_POLICY"
    Given agent "INTAKE" has no approved policy on 2026-11-30
    When the step runs on 2026-11-30
    Then the system makes no orchestrator call
    Then the system applies the rule result with fallback true and reason "NO_POLICY" in the decision log entry

  Scenario: AC6 The decision log write fails (legacy RWB-TE-013 AC6)
    Given the rwb-decision decision-record contract mock returns 503 for the entry of the step
    Given the decision log writer throws on write
    When the step runs
    Then the calling step does not act and case "RW-2026-000201" stays in "NEW"
    Then the client raises DecisionNotRecordedException carrying MSG-P7-003 and an incident is raised (R-UNI-39)
    Then the agent run stays with decision_log_id empty

  Scenario: AC7 A repeated step key (legacy RWB-TE-013 AC7)
    Given the rwb-decision decision-record contract mock returns the first entry for the step key
    Given the step with key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" ran once
    When it runs again with the same key
    Then one agent run and one decision log entry exist for the key
    Then the second call returns the first outcome (R-UNI-40)

  Scenario: AC8 Agent switched off (legacy RWB-TE-013 AC8)
    Given the rwb-decision decision-record contract mock returns a written entry id with agent version null
    Given the policy of "INTAKE" has autonomy mode "OFF"
    When the step runs
    Then no orchestrator call and no agent run row are made
    Then the decision log entry holds agent version null and fallback false
```

**Target reading.** The agent "INTAKE", the policy "P1", the prompt "PR1", the case "RW-2026-000201", the route state "NEW" and status "New", the rule "R-UNI-32" version "2026.11" and next state "RESUME_STATE", the timeout 60 seconds, the 2,000 ms answer, the confidence 0.91, the check code "SCHEMA", the three reasons, the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the business date 2026-11-30, the agent version string "INTAKE@P1/PR1", the empty `decision_log_id` and the two message IDs are the legacy values of RWB-TE-013, copied character for character; the eight scenario titles and every legacy Given, When and Then are kept, and each scenario carries the origin tag of its legacy criterion.

Each scenario gained exactly one inserted Given, `Given the rwb-decision decision-record contract mock returns <x>`, because every criterion ends on a decision record written across a service boundary: AC1, AC3, AC4, AC5 and AC8 read the record the local library writes, AC2 and AC4 read the fallback reason it carries, AC6 reads the refusal of the record store, and AC7 reads the first record of the step key. Nothing this service owns is mocked: the run, the policy row, the mode, the fallback, the run status and the link column are written and read in `rwb_agent` and asserted on the real store; the rwb-agent contract is never mocked in its own tests. The model endpoint INT-23 is stubbed by the baseline RWB-P10-E1058-APP, so 2,000 ms and 60 seconds of silence are fixture timings, never business values.

One legacy statement names an object the target changes hands over: AC6's "the agent run stays with decision_log_id empty" keeps the column and the assertion, and what changes is who sets it - the link operation instead of an in-process repository call. `DecisionNotRecordedException` keeps its name, its message ID MSG-P7-003 and its R-UNI-39 incident, and is now raised when the local record write in the caller's transaction fails.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The rule result is computed before the agent is called and is always the applied result in SHADOW and L1 | Agent catalog autonomy levels; `agent_policy.autonomy_mode` (DF-AGT-008); legacy BR1 |
| BR2 | If the agent does not answer within `agent_policy.timeout_seconds` (60, assumed; DL11), the rule result is used and the fallback is recorded on the decision | R-UNI-32; NFR-010; legacy BR2 |
| BR3 | A step acts only after its decision record and its link are written | Principle 5; R-UNI-39; CTL-06; legacy BR3 |
| BR4 | The record holds the rule ID, the rule version, the agent version as "<agent>@<policy>/<prompt>", the model version and the recommendation | REQ-DRI-001; `decision_log_entry.agent_version`; legacy BR4 |
| BR5 | The idempotency key of the agent run is the step key | R-UNI-40; DF-AGT-045; legacy BR5 |
| BR6 | The client runs under the identity of the calling module; the agent runs its tools as the rwb-agent service identity | REQ-ACA-010; legacy BR6 |
| BR7 | An agent is reached only through the step operation and AgentRunWorkflow on queue `rwb-agent`; no calling step reads `agent_run`, `agent_policy` or a record table in another schema | DP-01; DP-11; DP-20; Arch v5 slides 16 and 41 |
| BR8 | The step operation is one hop under `/api/recovery/agent/v1`; its budget is the policy timeout of 60 seconds, the recorded exception to the 2 s client budget of DP-11, and every other consumed hop keeps 2 seconds | DP-11; NFR-010; ADR-020; ASM-0903 |
| BR9 | The record of a step is written by that step through the local library in the calling service's schema and transaction, never by an agent run; rwb-decision owns the type and the central ledger | DP-03; ADR-022; RWB-P10-E1058-CON BR8 |
| BR10 | The mode, the timeout, the prompt version and the fallback rule are rows of the approved policy in force, read at run time; no mode, timeout, agent code or check code appears in code | Principle 1; DF-AGT-008, DF-AGT-012, DF-AGT-020; legacy section 17 |
| BR11 | The link between a run and a record is written once per run; the same record answers the same run and a different record is refused with 409 | R-UNI-40; DF-AGT-058 |
| BR12 | The values a mode, a run status and a product group may take are read from the rwb-case reference-data contract and never from a literal | DP-07; TSD P10 Agent runtime v2 T3.2 |

### 9. State transitions

The state of a case step that calls the client:

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | AGENT_UNAVAILABLE | The agent or the model does not answer inside the timeout (R-UNI-32) | RESUME_STATE, with the rule result applied |
| ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | The record cannot be written (R-UNI-39) | EXCEPTION_QUEUE, raised by the calling step |

The state of one step key in `rwb_agent`:

| From | Event | Condition | To |
|---|---|---|---|
| None | The step operation arrives | No run holds the step key | RUNNING, one AgentRunWorkflow and one run row |
| None | The step operation arrives | The mode is OFF or the flag is off | No run; the outcome answers fallback false and agent version null |
| None | The step operation arrives | No approved policy for the agent and date | No run, no model call; fallback true with reason NO_POLICY |
| RUNNING | The model answers and the guardrail passes | The answer is inside the timeout | ANSWERED, fallback false, the answer stored on the run |
| RUNNING | The timeout expires | 60 seconds without an answer | TIMED_OUT, fallback true, the rule result applied |
| RUNNING | The guardrail refuses the answer | A check code fails | GUARDRAIL_FAILED, fallback true with the check code |
| ANSWERED | The link stores the record reference | The run holds no record | The run holds `decision_log_id`; the step may act |
| ANSWERED | The link is called again with the same reference | The run holds the same record | The same run is answered; no second write |
| ANSWERED | The link is called with a different reference | The run holds another record | 409; the first record stands and the mismatch is raised |

The client changes no case status itself; the calling step moves the case on the applied result, as in the legacy story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The calling service identity (for example the rwb-case service identity) | Calls the step operation and the link operation; writes the decision record through the local library (Decision log C) |
| The rwb-agent service identity (the rwb-agent login, DP-02) | Runs AgentRunWorkflow, reads `agent_policy`, writes `agent_run` and the link, checks the reference lists, reads the record back through P7 |
| RW-PLATADM, RW-COE, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs and fallbacks through `GET /api/recovery/agent/v1/admin/agent-runs` (Platform administration R), under the baseline of RWB-P10-E1058-CON |
| rwb-decision (P7) | Owns the record type, the central ledger and the record read |
| rwb-case (P3) | Owns the reference lists and answers them through its contract |
| No role | Reads `rwb_case`, `rwb_decision` or another service's schema, edits an `agent_run` row outside the link, or changes a policy row outside RWB-P10-E1058-APP |

The login of the service is Not specified in the source documents (GAP-0619; ASM-0906); the story names it "the rwb-agent login (DP-02)". The approval of a policy version, its mode and its timeout is the Rules and parameters A right of RWB-P10-E1058-APP; no delegation of authority level applies here.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case (rwb_case, owner P3) | id | Read through the Case record contract and carried in the request |
| DF-CAS-007 | recovery_case (rwb_case, owner P3) | route_state | Read through the Case record contract; never read as a table |
| DF-REF-002, DF-REF-003 | rule_row (rwb_decision, owner P7) | rule_id, rule_version | Read from the rule result passed in the request, evaluated through the embedded Drools kit (DP-04) |
| DF-AGT-008, DF-AGT-012, DF-AGT-020 | agent_policy | autonomy_mode, timeout_seconds, fallback_rule | Read, for the approved policy in force on the business date |
| DF-AGT-021, DF-AGT-022 | agent_policy | status, valid_from | Read, to select the policy in force |
| DF-AGT-002, DF-AGT-003 | agent_policy | agent_code, policy_version | Read, to build the agent version string |
| DF-AGT-036, DF-AGT-045, DF-AGT-046, DF-AGT-047 | agent_run | id, idempotency_key, status, fallback | Read and write, on the run of the step key |
| DF-AGT-049, DF-AGT-050 | agent_run | output, confidence | Write, in SHADOW and L1 |
| DF-AGT-058 | agent_run | decision_log_id | Write, once per run, through the link operation |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (owner P7, written in the calling service's schema through the library) | all fields | Write through the local decision-record library, in the calling step's transaction (DP-03) |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row (rwb_case, owner P3) | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT with the version in force | Read through the reference-data contract (DP-07) |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-TE-013. `agent_policy`, `agent_prompt` and `agent_run` are the P10 tables of schema `rwb_agent`. `recovery_case` and `rule_row` are never read as tables: the case is carried in the request and the rule result is passed in, as the legacy client did. The inputs snapshot is masked before it is referenced, and no personal field is stored on the run or in the record.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/agent-steps` | Run one case step through the agent: resolve the mode and timeout of the approved policy in force, skip the agent when the mode is OFF or the flag is off, start AgentRunWorkflow with the step key as workflow ID, wait up to `timeout_seconds`, apply SHADOW or L1, record the fallback, answer the legacy AgentStepOutcome. Request: agentCode, caseId, decisionCode, stepKey, ruleResult {ruleId, ruleVersion, toState, result}, inputs. Answer 200: decisionLogEntryId, appliedResult, recommendation, fallback, fallbackReason, autonomyMode, agentRunId | Rules and parameters C, service identity, scope applied | The step key as the `Idempotency-Key`; a repeat answers the first outcome (R-UNI-40) |
| PUT | `/agent-runs/{runId}/decision-record` | Link one run to the record the calling step wrote: body the record reference; 200 the AgentRun with `decision_log_id` set; 404 no run; 409 the run holds a different record; 422 a reference the service cannot accept | Rules and parameters C, service identity, scope applied | The record reference; the same reference answers the same run and writes nothing twice |

Errors: 401 no session or no service identity, 403 no Rules and parameters right (MSG-P4-002), 409 a repeated step key whose first run is RUNNING or a run holding another record, 422 a request the service cannot accept (MSG-GEN-001), 503 the store, the workflow or a consumed contract unavailable. The two operations and the answer member names are fixed by RWB-P10-TE013-CON.

The run read `GET /api/recovery/agent/v1/admin/agent-runs` with query agent, from and to answering AgentRun[] (API-P10-001) is provided under the baseline of RWB-P10-E1058-CON and is not re-declared here; this story reads it only through its tests.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT checked before a mode is applied or a run row is written | One hop, 2 s |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The read-back of the record the step wrote, before the link is stored | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11); rwb-agent holds no schema client of another service. The model endpoint INT-23 is called inside AgentRunWorkflow by the baseline of RWB-P10-E1058-APP and is not called by this story. The record write is not a REST call: it is the local library and the topic of 12.3 (DP-03).

#### 12.3 Events published

None by rwb-agent through this story. The record of a step is written and published by the calling step through the client library, in the calling service's own schema and transaction, as `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` with the key of the record reference, and rwb-decision owns the type and the ledger (DP-03, DP-09; BR9). The payload members are fixed by RWB-P10-TE013-CON: record reference, decision code, agent version, model version, inputs reference, final call and actions {caseId, agentRunId, mode, fallback, fallbackReason}. This story declares no agent event: `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` belongs to the run path of RWB-P10-E1058-APP, as the legacy story says the orchestrator publishes it and the client publishes none.

#### 12.4 Events consumed

None. The step operation is a request; the mode and the timeout are read from `rwb_agent`, and the case and the rule result are carried in the request rather than consumed as events. This story subscribes to no topic.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow of the baseline of RWB-P10-E1058-APP, started with the step key as workflow ID and as the run's idempotency key | `rwb-agent` | Its activities ResolveAgentConfig, GatherInputs, MaskInputs, CallModelGateway with the 60 s budget, CheckGuardrail and RecordAgentRun are unchanged; this story starts it and waits on it |
| ResolveAutonomyMode | Activity | `rwb-agent` | Output: the mode OFF, SHADOW or L1 and the policy row in force for the agent and the business date, or none |
| ApplyAutonomyMode | Activity | `rwb-agent` | Output: the AgentStepOutcome - applied result, recommendation null in SHADOW and the answer in L1, fallback, reason and mode |
| LinkDecisionRecord | Activity | `rwb-agent` | Output: `agent_run.decision_log_id` set once for the run and the record reference |

The workflow runs on the queue and in the namespace of the service (§R4). The three activity names are this story's and are accepted by RWB-P10-TE013-CON; the baseline activity names are RWB-P10-E1058-APP's and are not changed.

#### 12.6 Schedules

None. This key starts no Schedule and no job: a step is started by its caller. The legacy precondition "RWB-TE-007 is done: Quartz jobs and their run books exist" is retired under §R6, and a job step that called the client is now an event-started or scheduled workflow step of the calling service through the workflow kit of RWB-PLT-E1071-CON (DP-10). No Quartz entry, job table or job admin read is used.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_policy | P10 (`rwb_agent`) | Read for the approved policy in force: mode, timeout, fallback rule and versions; no column added |
| agent_run | P10 (`rwb_agent`) | Read and written for the run of the step key: status, fallback, output, confidence and `decision_log_id` (DF-AGT-058); no column added by this story |
| agent_prompt | P10 (`rwb_agent`) | Read for the prompt version of the policy; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The idempotency envelope of the step key and the link (DP-09) |

No table of another service is read and no foreign key crosses a schema (DP-01). `recovery_case` is P3's, `rule_row` and `decision_log_entry` are P7's, and `reference_version` and `reference_row` are P3's; all are reached through their contracts. DF-AGT-058 is already a field of `agent_run` in TSD P10 Agent runtime v2 T3.1, so `V10_002__agent_run_decision_link.sql` guarantees the column and its index in the rwb-agent sequence and creates no table (DP-15).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Decision-record library stub of RWB-PLT-E1027-CON | The local record write and the record read-back of P7 | A written record with its reference; a record with fallback true and a reason; a record with agent version null; a 503 on write for AC6; the first record of a step key |
| rwb-case WireMock | The P3 reference-data contract of RWB-P3-E1043-CON | LOV-AUTONOMY with OFF, SHADOW and L1; LOV-AGENT with INTAKE; LOV-PRODUCT; a list not in force; a delay beyond 2 s |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the run read, one hop, JSON media type preserved, refusal passed through unchanged |
| Test clock and model stub of RWB-P10-E1058-APP | The 2,000 ms answer and the 60 seconds of silence of the legacy fixtures | One answer at 2,000 ms with confidence 0.91, one silence past 60 seconds, one answer failing check SCHEMA |

Every fixture is synthetic and holds no personal data. No test calls the model endpoint INT-23 directly: the two legacy timing fixtures are produced by the baseline stub of the run path.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 provided by the baseline and read by the tests, 2 consumed | The step and link operations provided; the run read of the baseline used by the tests; the P3 lists and the P7 record read consumed, one hop and 2 s each |
| Kafka | None published by the service, 1 published by the calling step through the library | EV-08 on `rwb.decision-record.v1` with its retry and `.dlt` topics; EV-28 belongs to the run path of RWB-P10-E1058-APP |
| Temporal | 1 workflow of the baseline started and waited on, 3 activities of this story, 0 Schedules | AgentRunWorkflow on queue `rwb-agent` with ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord |
| File | None | No file, no extract and no export |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.client`, module `client`, inside rwb-agent; the published library keeps the legacy package `recovery.agent.api` for `AgentStepClient`, `AgentStepRequest`, `RuleResult` and `AgentStepOutcome`, so a calling module compiles against the same names as before.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON; C RWB-P7-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; the packages and the registry are P7's, and the P7 contract row this key carries is RWB-P7-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency); the step operation is the recorded 60 s exception |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON as the legacy dependency of the pattern, which is an H row here because it is the service's own contract |

The H rows of this table are the rows in the metadata table; DP-11 adds no dependency of its own and sits on the two consumed reads and the provided operation, whose budget is the policy timeout (BR8; ASM-0903).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentStepClient | Published interface | The only way another module calls an agent; the legacy signature and members, unchanged |
| AgentStepClientImpl | Service | Submits the step, applies the mode and the fallback, writes the record through the library, links the run |
| AgentStepController | Controller | `POST /agent-steps` and `PUT /agent-runs/{runId}/decision-record` on `/api/recovery/agent/v1`, their refusals and idempotency (DP-13) |
| AutonomyModeResolver, ResolveAutonomyMode | Service and activity | Reads the policy in force for the agent and the business date and answers OFF, SHADOW, L1 or none (X3, X6) |
| TimedRunInvoker | Service | Starts AgentRunWorkflow with the step key and waits the policy timeout, producing TIMED_OUT on expiry (AC2; R-UNI-32) |
| ApplyAutonomyMode | Activity | Applies SHADOW and L1 to the outcome (AC1, AC3) |
| GuardrailFallbackHandler | Service | Maps a failed check code to fallback true with that code (AC4) |
| DecisionRecordWriter | Service | Writes the record through the local library in the caller's transaction and raises `DecisionNotRecordedException` with MSG-P7-003 on failure (AC1, AC6) |
| LinkDecisionRecord, AgentRunRepository | Activity and repository | Sets `agent_run.decision_log_id` once and answers 409 for a different record (AC7; BR11) |
| ReferenceDataReader, DecisionLogReadClient | Clients | Read LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT through the reference-data contract and the record back through P7 (DP-07, DP-03) |
| AgentPolicyRepository | Repository | Reads `agent_policy` and `agent_prompt` in `rwb_agent` only (DP-01) |

**Database and migrations.** `V10_002__agent_run_decision_link.sql` guarantees DF-AGT-058 on `agent_run` and its index, in `rwb_agent`, after `V10_001__agent_runtime.sql`, and creates no table (DP-15); `ix_agent_run_idempotency_key ON agent_run (idempotency_key)` serves the repeat lookup (DF-AGT-045). No new table, lake table or extract table is created.

**Configuration and reference data.** The approved `agent_policy` rows for the agents of LOV-AGENT, with autonomy_mode SHADOW, L1 or OFF, timeout_seconds 60, prompt_version PR1 and fallback_rule R-UNI-32, loaded by RW-COE and approved by RW-RISK, read at run time; LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT in force in rwb-case; the legacy flag `rwb.agent.client` kept, whose registration is the deployment's (RWB-P10-TE013-OPS); the guardrail check-code list is Not specified in the source documents (GAP-0619; ASM-0907), so the code stays a value of the guardrail result of RWB-P10-E1058-APP.

**Build steps**

1. The `recovery.agent.api` library with the legacy interface and the four records, and an ArchUnit test that other modules import only that package (DP-20).
2. `V10_002__agent_run_decision_link.sql`, the entity and AgentRunRepository in `rwb_agent` (BR11; DP-15).
3. AutonomyModeResolver with tests for OFF, SHADOW, L1 and no policy, against the reference-data fake (AC5, AC8; DP-07).
4. The timed call with a fake clock: 61 seconds of silence produces TIMED_OUT at 60 seconds and the rule result is applied (AC2; R-UNI-32).
5. DecisionRecordWriter and the write before return, with the 503 of AC6 and `DecisionNotRecordedException` carrying MSG-P7-003 (AC1, AC3, AC6; DP-03).
6. The idempotent repeat on the step key and the guardrail fallback (AC4, AC7; R-UNI-40).
7. AgentStepController with the two operations, their refusals 401, 403, 409, 422 and 503, and their idempotency (AC1, AC7; DP-13).
8. Pipeline scans: no literal of a mode, a timeout, an agent code or a check code, and no read of another service's table (BR7, BR10).
9. gateway-bff route contract test in front of the run read (AC2, AC7; DP-19).

**Done when.** The ten test cases of section 16 pass, the step operation answers on `/api/recovery/agent/v1` for the legacy fixture with the run at 2,000 ms and the record reference, a silence past 60 seconds produces TIMED_OUT with the rule result applied, a failed record write leaves case "RW-2026-000201" in "NEW" with MSG-P7-003 and `decision_log_id` empty, a repeated step key answers the first outcome with one run and one record, the boundary test shows other modules depend only on `recovery.agent.api`, and RWB-P10-TE013-OPS has deployed the capability in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right reads agent runs | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required member of the step request is empty | Enter {field}. |

MSG-P7-003 and MSG-P4-002 are copied unchanged from RWB-TE-013 and keep their wording character for character; MSG-GEN-001 is the platform message of an empty required field and this story adds no message ID. Thai text for each message follows decision DL10. In AC6 the message is carried by `DecisionNotRecordedException`; in the access test the {action} value is "read agent runs".

### 15. Screens and states

No screen in this story. A fallback shows in `GET /api/recovery/agent/v1/admin/agent-runs` (fallback true) and on the decision record of the case, which a Decision log R holder reads through the P7 read, as in the legacy story; the run read is reached through the gateway-bff route (DP-19) and its screen belongs to RWB-E2-031. The agent monitor screen SCR-46 and the autonomy-level screen are out of scope. The exact path of the route in front of the run read is Not specified in the source documents (GAP-0620; ASM-0911).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-013-01 | AC1, BR1, BR4 | Component | Case RW-2026-000201, mode SHADOW, answer in 2,000 ms |
| TC-TE-013-02 | AC2, BR2 | Component | AgentRunWorkflow stub silent for 61 seconds on the fake clock; status TIMED_OUT and fallback true |
| TC-TE-013-03 | AC3, BR1 | Component | Mode L1, confidence 0.91, the answer returned as the recommendation |
| TC-TE-013-04 | AC4 | Component | Answer fails check SCHEMA; fallback true with reason SCHEMA |
| TC-TE-013-05 | AC5 | Component | No approved policy on 2026-11-30; no orchestrator call and reason NO_POLICY |
| TC-TE-013-06 | AC6, BR3 | Component | Decision record writer throws; case stays in NEW, MSG-P7-003, `decision_log_id` empty |
| TC-TE-013-07 | AC7, BR5 | Component | Step key CASEWF:RW-2026-000201:ENTRY:2026-11-30 twice; one run, one record, the first outcome |
| TC-TE-013-08 | AC8 | Component | Mode OFF; no agent call and no run row; agent version null and fallback false |
| TC-TE-013-09 | Access | Contract | RW-CASEOWN calls GET /api/recovery/agent/v1/admin/agent-runs through the route; refused with 403 and MSG-P4-002 |
| TC-TE-013-10 | Principle 5 | NFR | Decision record write forced to fail during a step in SHADOW mode; the step does not act; MSG-P7-003 |

TC-TE-013-01 to TC-TE-013-10 are the legacy test cases of RWB-TE-013, kept with their IDs, order and data; the legacy System level maps to Component, Access to Contract because the refusal is proved through the route and the published contract, and Resilience to NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: the mode, the timeout, the fallback rule, the prompt version and the check codes are policy and reference values read at run time (BR10; DP-07).
- No personal data in logs, tests, prompts or records: run rows, IDs, versions, times and codes only; the inputs snapshot is masked before it is referenced and every fixture is synthetic.
- No read of another module's tables and no schema client: the case and the rule result are carried in the request, the lists come through the rwb-case contract and the record through the local library and the P7 read (DP-01, DP-03, DP-07).
- The client never applies an agent answer as the case result in SHADOW or L1 (BR1).
- A step acts only after its record and its link are written; a failed write stops the step with MSG-P7-003 and never falls back to acting (BR3).
- One hop and a 2 s client budget on every consumed REST call; the step operation is the single recorded exception at the policy timeout of 60 seconds (BR8).
- The step operation and the link are idempotent on the step key and on the record reference; a repeat writes nothing twice (BR5, BR11).
- The run read is reached through the gateway-bff route and never from a screen to the service (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records rule, model, agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-01, TC-TE-013-02, TC-TE-013-03, TC-TE-013-04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program, section 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-39 | TC-TE-013-06, TC-TE-013-10 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | Business Requirements Program, section 5.4 | FEAT-AGT-01 | All recovery processes | R-UNI-40 | TC-TE-013-05, TC-TE-013-07, TC-TE-013-08, TC-TE-013-09 |
| D-RCV-60 DP-01 | The run and the policy live in `rwb_agent`; every other service's data is read through its contract | Template and Rules §R5.5 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-01, TC-TE-013-07 |
| D-RCV-60 DP-03 | The record of a step is written through the local decision-record library and collected into the ledger | Template and Rules §R5.5; ADR-022 | FEAT-AGT-11 | All recovery processes | R-UNI-39 | TC-TE-013-01, TC-TE-013-06, TC-TE-013-10 |
| D-RCV-60 DP-04 | The rule result is evaluated through the embedded Drools kit with the packages of rwb-decision | Template and Rules §R5.5; ADR-017 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-02, TC-TE-013-03 |
| D-RCV-60 DP-07 | The autonomy, agent and product lists are read from the rwb-case reference-data contract | Template and Rules §R5.5 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-05, TC-TE-013-08 |
| D-RCV-60 DP-09 | The record leaves through the outbox library and a permanent failure goes to `.dlt` | Template and Rules §R5.5; ADR-015 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-06 |
| D-RCV-60 DP-10 | The Quartz job step of RWB-TE-007 becomes a Temporal step through the workflow kit | Template and Rules §R5.5 and §R6; ADR-016 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-02, TC-TE-013-07 |
| D-RCV-60 DP-11 | The published interface is a REST contract with a mock, one hop, with the policy timeout as its recorded exception | Template and Rules §R5.5; ADR-020 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-01, TC-TE-013-09 |
| D-RCV-60 DP-13 | The step and link operations are served on the base `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-01, TC-TE-013-09 |
| D-RCV-60 DP-15 | The decision link arrives with the service's own Flyway migration in its own schema | Template and Rules §R5.5; ADR-021 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-01, TC-TE-013-07 |
| D-RCV-60 DP-19 | The run read is reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-09 |
| D-RCV-60 DP-20 | The legacy agent client becomes the rwb-agent contract and AgentRunWorkflow on queue `rwb-agent` | Template and Rules §R5.5; Arch v5 slide 16 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-01, TC-TE-013-02, TC-TE-013-07 |
| NFR-010 | An agent returns an answer inside its target, after which the rule result is used and the case still routes | TSD P10 Agent runtime v2 T7 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-02, TC-TE-013-10 |
| RWB-TE-013 (legacy story) | Agent runtime client with fallback: the eight criteria AC1 to AC8 and the access and resilience tests | Business Requirements Epic 1, section 3.9 | FEAT-AGT-11 | All recovery processes | None | The ten legacy test cases of section 16 |
| RWB-ITG-TE013-ITG (integration copy) | The same behaviour proved across rwb-agent, rwb-decision and a real calling step, with the `-ITG` test cases | Business Requirements Epic 1, section 3.9 | FEAT-AGT-11 | All recovery processes | None | The test cases of that story |

The gap GAP-0619 records what the sources leave open for this story - the two operations the legacy interface spans, the call type, the budget of the step operation, the login and the check-code list - and each default it raises is settled by ASM-0902 to ASM-0907; the route path in front of the run read is settled by GAP-0620 and ASM-0911.

### 19. Out of scope

- The cross-service behaviour of this key: RWB-ITG-TE013-ITG, and the harness RWB-ITG-W1J01-ITG.
- The contract of the step and link operations and the record payload as published artefacts with their fakes: RWB-P10-TE013-CON.
- The deployment of this capability - chart values, migration job, worker, reference-data and record wiring, feature switch, probes, alerts, route publication, runbook and rollback: RWB-P10-TE013-OPS.
- The agent runtime baseline: the eight agent tables, the prompt and policy store, the tool gateway, the model gateway call and the publication of EV-28: RWB-P10-E1058-APP.
- The guardrail checker and its check codes: RWB-P10-E1058-APP.
- The decision-record library, its envelope and `rwb.decision-record.v1`: RWB-PLT-E1027-CON; the record type, ledger and record read: RWB-P7-E1027-CON.
- The embedded Drools kit and the rule-package client: RWB-PLT-E1072-CON; the rule registry and package versions: P7 rwb-decision.
- The reference lists and their versions: P3 rwb-case, read through RWB-P3-E1043-CON.
- The agent monitor screen SCR-46 and its dashboard: RWB-E2-031.
- Agent answers acted on without a person (autonomy L2 and above, Epic 8, FEAT-AGT-15).
- The case steps that call the client: case intake (RWB-E2-028), deviation screening (RWB-E2-029) and the other calling stories.
