# RWB-TE-013 Agent runtime client with fallback

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-013 |
| Epic | E1, release 30 November 2026 |
| Module | P10 Agent runtime |
| Feature | None |
| Requirement IDs | REQ-DRI-001, REQ-DRI-005, REQ-ACA-010 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, sections 5.4 and 5.7 |
| L3 process | All recovery processes |
| Decision | DL33 |
| Priority | Must |
| Depends on | RWB-TE-007, RWB-E1-058, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one client in the recovery module that calls the agent orchestrator, applies the autonomy mode, runs shadow mode and falls back to the rule result**, so that **agents are added to a case step without changing the case flow, and every step records what the agent did**.

## 2. Business rationale

A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The client puts every agent call behind one interface: the rule result always exists, the agent answer is used only as the autonomy mode allows, and the decision log entry records the rule, agent and prompt versions and any fallback (REQ-DRI-001). If the entry cannot be written, the step does not act (REQ-DRI-005). The measure is the agent fallback rate, target below 10 percent per month.

## 3. Preconditions

- RWB-TE-007 is done: Quartz jobs and their run books exist, so a job step can call the client.
- RWB-E1-058 is done: AgentOrchestrator, agent_policy and agent_run exist.
- RWB-E1-027 is done: the P7 DecisionLogWriter interface writes entries and throws on failure.
- An approved agent_policy row exists for the agent, with autonomy_mode SHADOW or L1 and timeout_seconds 60.
- The calling module runs under its own service identity (for example SY-CASEWF) and has evaluated its rule before it calls the client.

## 4. Flow

1. Calling step (for example SY-CASEWF): evaluates its rule package through RuleEvaluator and builds the rule result (rule ID, rule version, next state).
2. Calling step: calls AgentStepClient.runStep with the agent code, case ID, decision code, step key and rule result.
3. Client: reads the autonomy mode from the agent policy in force; if it is OFF or the flag is off, it skips the agent.
4. Client: calls AgentOrchestrator.run with the idempotency key built from the step key and waits at most timeout_seconds.
5. Client: in SHADOW mode, keeps the rule result as the applied result and records the agent answer only.
6. Client: in L1 mode, keeps the rule result as the applied result and returns the checked agent answer as the recommendation for the person who decides.
7. Client: on a timeout or a guardrail failure, keeps the rule result and marks fallback true with the reason (R-UNI-32).
8. Client: writes one decision log entry through DecisionLogWriter with the rule ID and version, agent version, model version, recommendation and fallback, then links it to the agent run.
9. Calling step: acts on the applied result only after the entry is written.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent does not answer within 60 seconds | Rule result applied; fallback true with reason TIMED_OUT; step continues | None to a user | AC2 |
| X2 | The answer fails a guardrail check | Rule result applied; fallback true with the check code | None to a user | AC4 |
| X3 | No approved policy exists for the agent on the business date | No agent call; rule result applied; fallback true with reason NO_POLICY | None to a user | AC5 |
| X4 | The decision log write fails | The step does not act; the case stays in its state; an incident is raised (R-UNI-39) | MSG-P7-003 | AC6 |
| X5 | The same step key arrives twice | One agent run and one decision log entry; the repeat returns the first outcome (R-UNI-40) | None to a user | AC7 |
| X6 | Autonomy mode OFF or flag `rwb.agent.client` off | No agent call; rule result applied; fallback false; no agent run row | None to a user | AC8 |
| X7 | A role without the right reads agent runs | Refused with 403 | MSG-P4-002 | TC-TE-013-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the orchestrator (RWB-E1-058), the decision log writer (RWB-E1-027) and the job pattern (RWB-TE-007); no agent story |
| Negotiable | The mode and timeout per agent are data; the client fixes only the order: rule first, agent second, log before action |
| Valuable | Every agent from RWB-E1-059 onward plugs into case steps through this one interface |
| Estimable | One published interface, one service, one decision log mapping, no screen, no table of its own beyond one link column |
| Small | One developer, under one week with its tests |
| Testable | Each criterion is a unit or component test with a stubbed orchestrator and a stubbed decision log writer |

## 7. Acceptance criteria

```gherkin
Feature: Agent runtime client with fallback

  Background:
    Given agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1"
    Given case "RW-2026-000201" is in route state "NEW" and status "New"
    Given the calling step has rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE"

  Scenario: AC1 Shadow
    Given the policy of "INTAKE" has autonomy mode "SHADOW"
    When the agent answers in 2,000 ms with a valid output
    Then the system stores the agent answer on the agent run and the rule result is the applied result
    Then one decision log entry holds agent version "INTAKE@P1/PR1", the rule ID and version, recommendation null and fallback false in actions
    Then the calling step receives the rule result and no agent output

  Scenario: AC2 No answer
    Given the agent does not answer in 60 seconds
    When the step runs
    Then the system uses the rule result and the step continues to "RESUME_STATE"
    Then the decision log entry holds actions fallback true with reason "TIMED_OUT" and the agent run ID (R-UNI-32)
    Then the agent run holds status "TIMED_OUT" and fallback true

  Scenario: AC3 Assisted mode returns the answer as a recommendation
    Given the policy of "INTAKE" has autonomy mode "L1"
    When the agent answers with confidence 0.91
    Then the rule result is the applied result
    Then the outcome returns the agent answer as the recommendation for the person who decides
    Then the decision log entry holds the agent answer in recommendation with confidence 0.91

  Scenario: AC4 A guardrail failure falls back
    Given the agent answer fails check "SCHEMA"
    When the step runs
    Then the system applies the rule result
    Then the decision log entry holds actions fallback true with reason "SCHEMA"

  Scenario: AC5 No approved policy
    Given agent "INTAKE" has no approved policy on 2026-11-30
    When the step runs on 2026-11-30
    Then the system makes no orchestrator call
    Then the system applies the rule result with fallback true and reason "NO_POLICY" in the decision log entry

  Scenario: AC6 The decision log write fails
    Given the decision log writer throws on write
    When the step runs
    Then the calling step does not act and case "RW-2026-000201" stays in "NEW"
    Then the client raises DecisionNotRecordedException carrying MSG-P7-003 and an incident is raised (R-UNI-39)
    Then the agent run stays with decision_log_id empty

  Scenario: AC7 A repeated step key
    Given the step with key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" ran once
    When it runs again with the same key
    Then one agent run and one decision log entry exist for the key
    Then the second call returns the first outcome (R-UNI-40)

  Scenario: AC8 Agent switched off
    Given the policy of "INTAKE" has autonomy mode "OFF"
    When the step runs
    Then no orchestrator call and no agent run row are made
    Then the decision log entry holds agent version null and fallback false
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The rule result is computed before the agent is called and is always the applied result in SHADOW and L1 | Agent catalog autonomy levels; agent_policy.autonomy_mode (New) |
| BR2 | If the agent does not answer within agent_policy.timeout_seconds (60, assumed; DL11), the rule result is used and the fallback is recorded on the decision | R-UNI-32 |
| BR3 | A step acts only after its decision log entry is written | Principle 5; R-UNI-39; CTL-06 |
| BR4 | The decision log entry holds the rule ID, rule version, agent version as "<agent>@<policy>/<prompt>", model version and the recommendation | REQ-DRI-001; decision_log_entry.agent_version |
| BR5 | The idempotency key of the agent run is the step key | R-UNI-40 |
| BR6 | The client runs under the identity of the calling module; the orchestrator runs tools as SY-AGENT | REQ-ACA-010 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | AGENT_UNAVAILABLE | The agent or the model does not answer inside the timeout (R-UNI-32) | RESUME_STATE, with the rule result applied |
| ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | The entry cannot be written (R-UNI-39) | EXCEPTION_QUEUE, raised by the calling step |

The client does not change a case status itself; the calling step moves the case on the applied result.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF and other calling module identities | Call AgentStepClient; write the decision log entry through P7 (Decision log C) |
| SY-AGENT | Runs the agent and its tools (read only) |
| SY-DECLOG | Writes the entry |
| RW-PLATADM, RW-COE, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs and fallbacks through GET /admin/agent-runs (Platform administration R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-007 | recovery_case | route_state | Read |
| DF-REF-002 | rule_row | rule_id | Read (from the rule result passed in) |
| DF-REF-003 | rule_row | rule_version | Read (from the rule result passed in) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (through the P7 DecisionLogWriter) |
| DF-AGT-008 | agent_policy | autonomy_mode | Read |
| DF-AGT-012 | agent_policy | timeout_seconds | Read |
| DF-AGT-021 | agent_policy | status | Read |
| DF-AGT-022 | agent_policy | valid_from | Read |
| DF-AGT-036 | agent_run | id | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-047 | agent_run | fallback | Read |
| DF-AGT-045 | agent_run | idempotency_key | Read |
| DF-AGT-058 | agent_run | decision_log_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Published interface**

```java
package recovery.agent.api;

public interface AgentStepClient {
    AgentStepOutcome runStep(AgentStepRequest request) throws DecisionNotRecordedException;
}

public record AgentStepRequest(String agentCode, UUID caseId, String decisionCode,
                               String stepKey, RuleResult ruleResult, Map<String, Object> inputs) {}
public record RuleResult(String ruleId, String ruleVersion, String toState, JsonNode result) {}
public record AgentStepOutcome(UUID decisionLogEntryId, RuleResult appliedResult, JsonNode recommendation,
                               boolean fallback, String fallbackReason, String autonomyMode, UUID agentRunId) {}
```

**Decision log mapping** (DecisionLogWriter.write): case_id = caseId; decision_code = decisionCode; rule_id and rule_version from ruleResult; agent_version = "<agent>@<policy_version>/<prompt_version>" or null; model_version from the run; inputs_ref = reference to the masked inputs snapshot; recommendation = agent answer in L1, null otherwise; final_call = ruleResult.toState; actions = {"agentRunId", "mode", "fallback", "fallbackReason"}.

**GET /api/recovery/v1/admin/agent-runs** (api.yaml): query agent, from, to; response AgentRun[] with fallback; errors 401, 403, 503; Platform administration R; read only.

**Events:** EV-28 AgentRunCompleted is published by the orchestrator (RWB-E1-058); the client publishes none.

**Idempotency:** stepKey, used as the agent run idempotency key and as the decision log lookup key for repeats.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/api/` and `.../recovery/agent/client/`, Java packages `recovery.agent.api` (interface and records) and `recovery.agent.client` (implementation).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentStepClient | Published interface | The only way another module calls an agent |
| AgentStepClientImpl | Service | Mode check, timed orchestrator call, fallback, decision log write, link to run |
| AutonomyModeResolver | Service | Reads the policy in force for the agent and date |
| DecisionLogMapper | Service | Builds the P7 entry from the request, the rule result and the run |
| AgentRunRepository | Repository | Sets agent_run.decision_log_id |

**Database:** reads agent_policy and agent_run; adds column decision_log_id uuid to agent_run in migration `V10_002__agent_run_decision_link.sql`. No new table.

**Configuration and reference data:** agent_policy rows (RW-COE loads, RW-RISK approves). Feature flag in the ACE flag service.

**Build steps**
1. Write the interface and records in `recovery.agent.api`, with an ArchUnit test that other modules import only this package.
2. Build AutonomyModeResolver with tests for OFF, SHADOW, L1 and no policy (AC5, AC8).
3. Build the timed call with a CompletableFuture and the policy timeout; test with a stub that sleeps 61 seconds on a fake clock (AC2).
4. Build DecisionLogMapper and the write before return; test write failure (AC1, AC3, AC6).
5. Build the idempotent repeat on the step key (AC7) and the guardrail fallback (AC4).

**Feature flag:** `rwb.agent.client`. Off: no agent call; the rule result is applied and logged with agent version null.

**Done when:** the tests in section 16 pass and the boundary test shows other modules depend only on `recovery.agent.api`.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision log write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right reads agent runs | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. A fallback shows in GET /admin/agent-runs (fallback true) and on the decision log entry of the case.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-013-01 | AC1, BR1, BR4 | System | Case RW-2026-000201, mode SHADOW, answer in 2,000 ms |
| TC-TE-013-02 | AC2, BR2 | System | Orchestrator stub silent for 61 seconds |
| TC-TE-013-03 | AC3, BR1 | System | Mode L1, confidence 0.91 |
| TC-TE-013-04 | AC4 | System | Answer fails check SCHEMA |
| TC-TE-013-05 | AC5 | System | No approved policy on 2026-11-30 |
| TC-TE-013-06 | AC6, BR3 | System | Decision log writer throws |
| TC-TE-013-07 | AC7, BR5 | System | Step key CASEWF:RW-2026-000201:ENTRY:2026-11-30 twice |
| TC-TE-013-08 | AC8 | System | Mode OFF |
| TC-TE-013-09 | Access | Access | RW-CASEOWN calls GET /admin/agent-runs; refused with MSG-P4-002 |
| TC-TE-013-10 | Principle 5 | Resilience | Decision log write forced to fail during a step in SHADOW mode; step does not act; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: mode and timeout come from the approved agent policy.
- No personal data in logs, tests or prompts; the inputs snapshot is masked before it is referenced.
- No read of another module's tables; the decision log is written only through the P7 interface.
- The client never applies an agent answer as the case result in SHADOW or L1.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records rule, model, agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-01, TC-TE-013-02, TC-TE-013-03, TC-TE-013-04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program, section 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-39 | TC-TE-013-06, TC-TE-013-10 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | Business Requirements Program, section 5.4 | FEAT-AGT-01 | All recovery processes | R-UNI-40 | TC-TE-013-05, TC-TE-013-07, TC-TE-013-08, TC-TE-013-09 |

## 19. Out of scope

- The orchestrator, gateway and guardrail checker (RWB-E1-058).
- Agent answers acted on without a person (autonomy L2 and above, Epic 8, FEAT-AGT-15).
- The case steps that call the client: case intake (RWB-E2-028), deviation screening (RWB-E2-029).
