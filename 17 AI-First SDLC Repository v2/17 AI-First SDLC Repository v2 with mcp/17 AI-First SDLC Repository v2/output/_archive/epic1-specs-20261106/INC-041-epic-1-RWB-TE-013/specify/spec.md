# Technical Specification — RWB-TE-013 Agent runtime client with fallback

| Field | Value |
|---|---|
| Story | RWB-TE-013 — Agent runtime client with fallback |
| Epic / module | E1 / P10 Agent runtime (technical enabler) |
| RUN_ID | `INC-041-epic-1-RWB-TE-013` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-019); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 013 Agent runtime client with fallback v1.md` |
| Upstream IDs | BRD-RWB-010; FR-RWB-019; AC-RWB-019; BR-RWB-013; REQ-DRI-001, REQ-DRI-005, REQ-ACA-010; US-RWB-TE-013; FEAT-AGT-11; R-UNI-32, R-UNI-39, R-UNI-40; DL33 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `ENHANCEMENT_LOGIC_ONLY` — enabler on the agent platform delivered by RWB-E1-058. |
| UI In Scope | `NO` — no screen, component, route, label or state. |
| Logic In Scope | `YES` — autonomy mode, timed call, shadow/L1 handling, fallback, decision log mapping and idempotency. |
| API In Scope | `NO` — no new or changed REST contract. The story adds an internal published Java interface and reuses `GET /api/recovery/v1/admin/agent-runs` for read. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `agent_run` gains `decision_log_id`; `agent_policy` is read; `decision_log_entry` is written through P7. New client package in P10. |
| New Nodes Required | `YES` — `AgentStepClient` (published interface), `AgentStepClientImpl`, `AutonomyModeResolver`, `DecisionLogMapper`, `AgentRunRepository` update. |
| Inherited Existing Behavior | Agent platform (RWB-E1-058), decision log writer and hash chain (RWB-E1-027), Quartz job pattern (RWB-TE-007), case state machine (P3), feature flags (RWB-E1-047). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The rule result is computed before the agent call and is always the applied result in SHADOW and L1. | SPEC-RWB-TE-013-002, SPEC-RWB-TE-013-005, SPEC-RWB-TE-013-006 | DIRECT | `AgentStepOutcome.appliedResult` is always `ruleResult`. | COVERED |
| BR2 | If the agent does not answer within `timeout_seconds`, the rule result is used and the fallback is recorded. | SPEC-RWB-TE-013-004 | DIRECT | Client-side wait bounded by the policy timeout; reason `TIMED_OUT`. | COVERED |
| BR3 | A step acts only after its decision log entry is written. | SPEC-RWB-TE-013-009, SPEC-RWB-TE-013-010 | DIRECT | Write is the last step before return; failure throws and no action proceeds. | COVERED |
| BR4 | The entry holds rule ID/version, agent version `<agent>@<policy>/<prompt>`, model version and the recommendation. | SPEC-RWB-TE-013-008 | DIRECT | `DecisionLogMapper` maps every field. | COVERED |
| BR5 | The agent run idempotency key is the step key. | SPEC-RWB-TE-013-011 | DIRECT | Same key passed to `AgentOrchestrator` and used for the repeat lookup. | COVERED |
| BR6 | The client runs under the calling module identity; the orchestrator runs tools as `SY-AGENT`. | SPEC-RWB-TE-013-012 | DIRECT | No identity switch in the client; P7 write through `SY-DECLOG`. | COVERED |
| AC1 | SHADOW: answer stored on the run; rule result applied; one log entry with agent version, rule ID/version, recommendation null, fallback false; no agent output to caller. | SPEC-RWB-TE-013-005, SPEC-RWB-TE-013-008 | DIRECT | `recommendation` omitted in SHADOW; `AgentStepOutcome.recommendation` null. | COVERED |
| AC2 | No answer in 60 s: rule result applied, step continues, log actions fallback true reason `TIMED_OUT`, run `TIMED_OUT`, fallback true. | SPEC-RWB-TE-013-004 | DIRECT | Timeout at policy value; latency recorded at cutoff. | COVERED |
| AC3 | L1: rule result applied; answer returned as recommendation; log recommendation carries confidence 0.91. | SPEC-RWB-TE-013-006, SPEC-RWB-TE-013-008 | DIRECT | Confidence inside `recommendation` jsonb (DF-DEC-009). | COVERED |
| AC4 | Guardrail failure: rule result applied; log fallback true reason `SCHEMA`. | SPEC-RWB-TE-013-007 | DIRECT | Fallback reason is the check code. | COVERED |
| AC5 | No approved policy: no orchestrator call; rule result applied; log fallback true reason `NO_POLICY`. | SPEC-RWB-TE-013-003 | DIRECT | Resolver returns empty; no run row. | COVERED |
| AC6 | Decision log write fails: step does not act; case stays `NEW`; `DecisionNotRecordedException` with MSG-P7-003; incident; run link empty. | SPEC-RWB-TE-013-010 | DIRECT | Throw after rollback; run link not set. | COVERED |
| AC7 | Repeated step key: one run and one log entry; second call returns first outcome. | SPEC-RWB-TE-013-011 | DIRECT | Unique key plus decision log idempotency key. | COVERED |
| AC8 | Mode OFF: no call and no run row; log entry agent version null, fallback false. | SPEC-RWB-TE-013-003 | DIRECT | Flag/mode short-circuit. | COVERED |
| X1 | Agent does not answer in 60 s. | SPEC-RWB-TE-013-004 | DIRECT | `TIMED_OUT`; step continues. | COVERED |
| X2 | Answer fails a guardrail check. | SPEC-RWB-TE-013-007 | DIRECT | Rule result applied; check code as reason. | COVERED |
| X3 | No approved policy for the business date. | SPEC-RWB-TE-013-003 | DIRECT | `NO_POLICY`; no call. | COVERED |
| X4 | Decision log write fails. | SPEC-RWB-TE-013-010 | DIRECT | No action; incident; MSG-P7-003. | COVERED |
| X5 | Same step key twice. | SPEC-RWB-TE-013-011 | DIRECT | First outcome returned. | COVERED |
| X6 | Mode OFF or flag off. | SPEC-RWB-TE-013-003 | DIRECT | No call, no run, fallback false. | COVERED |
| X7 | Role without the right reads runs. | SPEC-RWB-TE-013-013 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **platform administrator (RW-PLATADM)**, I want **one client in the recovery module that calls the agent orchestrator, applies the autonomy mode, runs shadow mode and falls back to the rule result**, so that **agents are added to a case step without changing the case flow, and every step records what the agent did**.

The story is the adapter between a case step and the platform. It never decides a case outcome: the
calling step computes its rule result first, the client adds the agent answer as evidence, and the
decision log entry is written before the step acts. In SHADOW the answer is stored and not returned;
in L1 it is returned as a recommendation for the person who decides.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | A calling step invokes `AgentStepClient.runStep` after evaluating its rule. |
| Preconditions | RWB-TE-007 job pattern; RWB-E1-058 orchestrator, policy and run tables; RWB-E1-027 `DecisionLogWriter`; an approved policy with mode SHADOW or L1 and a timeout; the calling module identity exists. |
| Input | `agentCode`, `caseId`, `decisionCode`, `stepKey`, `RuleResult` (rule ID, version, next state, result), masked inputs. |
| Output | `AgentStepOutcome` with decision log entry ID, applied rule result, recommendation (L1 only), fallback flag and reason, autonomy mode, agent run ID. |
| Feature flag | `rwb.agent.client`. Off: no agent call; rule result applied; agent version null in the log. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `agent_policy` | `autonomy_mode` | Approved policy | Read-only | `OFF`, `SHADOW` or `L1`; the mode in force on the run date. |
| `agent_policy` | `timeout_seconds` | Approved policy | Read-only | 1..120; client wait bound. |
| `agent_policy` | `status`, `valid_from` | Approved policy | Read-only | Only APPROVED and effective rows are used. |
| `agent_run` | `idempotency_key` | Step key | System-written | Unique; max 120 chars. |
| `agent_run` | `status`, `fallback` | Orchestrator | Read-only | Terminal status per run. |
| `agent_run` | `decision_log_id` | Decision log write | System-written | Null until the entry is written. |
| `decision_log_entry` | `agent_version` | Run | System-written | `<agent>@<policy>/<prompt>` or null. |
| `decision_log_entry` | `model_version` | Run | System-written | Null when no call. |
| `decision_log_entry` | `recommendation` | Run | System-written | jsonb; L1 only, with confidence; null in SHADOW/OFF. |
| `decision_log_entry` | `final_call` | Rule result | System-written | `ruleResult.toState`. |
| `decision_log_entry` | `actions` | Client | System-written | `agentRunId`, `mode`, `fallback`, `fallbackReason`. |
| `decision_log_entry` | `idempotency_key` | Step key | System-written | Unique; max 80 chars. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| `ANY_ACTIVE` | `AGENT_UNAVAILABLE` | Agent or model does not answer inside the timeout | `RESUME_STATE` | Rule result applied; fallback true; log entry written. |
| `ANY_ACTIVE` | `DECISION_LOG_WRITE_FAILED` | Entry cannot be written | `EXCEPTION_QUEUE` (raised by the calling step) | No action; incident; MSG-P7-003. |
| None | Step called | Mode OFF / flag off / no policy | No change | Rule result applied; log entry written; no run. |

The client changes no case status itself; the calling step moves the case on the applied result.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No answer inside the timeout | Rule result applied; `TIMED_OUT`; step continues | None to a user |
| X2 | Guardrail failure | Rule result applied; reason is the check code | None to a user |
| X3 | No approved policy | No call; `NO_POLICY`; no run row | None to a user |
| X4 | Decision log write fails | Step does not act; case unchanged; incident | MSG-P7-003 |
| X5 | Repeated step key | One run and one entry; first outcome returned | None to a user |
| X6 | Mode OFF or flag off | No call, no run; log agent version null, fallback false | None to a user |
| X7 | Role without Platform administration R | 403; nothing changes | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/agent-runs` (read fallbacks and run metadata). |
| Contract delta | None. `AgentStepClient` is an internal published Java interface, documented under detailed design, not a REST contract. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R for the run list; the client is called in-process under the calling module identity. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 503 store unavailable; `DecisionNotRecordedException` with MSG-P7-003. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-019; SPEC-RWB-TE-013-001..014 | New published interface, client, resolver, mapper and run-link update. | Positive, negative and error-path tests: SHADOW, L1, OFF, no policy, timeout, guardrail, log failure, repeat key, access, boundary of the step-key length. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `AgentStepClient` | Published interface | The only way another module calls an agent. |
| `AgentStepClientImpl` | Service | Mode check, timed call, fallback, decision log write, run link. |
| `AutonomyModeResolver` | Service | Reads the approved policy in force for the agent and date. |
| `DecisionLogMapper` | Service | Builds the P7 entry from the request, rule result and run. |
| `AgentRunRepository` | Repository | Sets `agent_run.decision_log_id`. |

### Package and boundaries

`recovery.agent.api` holds the interface and records; `recovery.agent.client` holds the implementation.
Other modules import only `recovery.agent.api`; an ArchUnit test enforces it. The client calls the
orchestrator interface and the P7 `DecisionLogWriter`; it reads no table owned by another module.

### Data and migration

`V10_002__agent_run_decision_link.sql` adds `agent_run.decision_log_id` (uuid, nullable) and an index.
The column already exists in the logical data model (DF-AGT-058); this migration makes it present in
the physical schema. No new table. Reads: `agent_policy` (`autonomy_mode`, `timeout_seconds`, `status`,
`valid_from`), `agent_run` (`id`, `status`, `fallback`, `idempotency_key`). Writes:
`agent_run.decision_log_id`; `decision_log_entry` through P7.

### Mode resolution

| Mode | Behaviour | Caller receives |
|---|---|---|
| `OFF` | No orchestrator call, no run row; log entry with agent version null, fallback false. | Rule result only. |
| `SHADOW` | Call; store answer; rule result applied. | Rule result only; recommendation null. |
| `L1` | Call; store answer; rule result applied. | Rule result plus checked answer as recommendation. |
| No policy / flag off | No call; fallback true, reason `NO_POLICY` or `DISABLED`. | Rule result only. |

### Timed call and fallback

The client waits at most `timeout_seconds` for the orchestrator. The orchestrator enforces the same
policy timeout at the gateway. A timeout, a guardrail failure or a tool failure returns the rule
result and a fallback reason. The client never retries the step; the calling job's normal retry policy
applies to the whole step, not to the agent call.

### Decision log mapping

| P7 field | Source |
|---|---|
| `case_id` | `caseId` |
| `decision_code` | `decisionCode` |
| `rule_id`, `rule_version` | `ruleResult` |
| `agent_version` | `<agent>@<policy_version>/<prompt_version>` or null |
| `model_version` | Run; null when no call |
| `inputs_ref` | Reference to the masked inputs snapshot |
| `recommendation` | Agent answer in L1 with confidence; null otherwise |
| `final_call` | `ruleResult.toState` |
| `actions` | `agentRunId`, `mode`, `fallback`, `fallbackReason` |
| `idempotency_key` | Step key |

### Transaction and failure

1. Resolve the mode. OFF/flag off: write the log entry and return the rule result.
2. Call the orchestrator with the step key; wait at most the policy timeout.
3. Map and write the decision log entry through P7. This is the last step before return.
4. On success, set `agent_run.decision_log_id` and return the outcome.
5. If the write throws, roll back the run link, throw `DecisionNotRecordedException` with MSG-P7-003,
   and raise an incident. The calling step does not act.

The run row may exist from step 2 even when the log write fails; its `decision_log_id` stays empty, which
is the evidence AC6 requires. The run is not deleted, because the model call and cost happened.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| Calling module identity (e.g. `SY-CASEWF`) | Calls the client; Decision log C through P7 | All |
| `SY-AGENT` | Case record R, Documents R | All |
| `SY-DECLOG` | Decision log C | All |
| RW-PLATADM, RW-COE, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Platform administration R | All |

### Observability, performance and rollback

- Metrics: steps by mode, fallback rate and reason, decision log failures, run-link failures, latency.
- Alerts: fallback rate above 10 percent, decision log failure (incident), P7 unavailable.
- Performance: the client adds one policy read, one orchestrator call and one log write; the case step
  waits at most the policy timeout (NFR-010).
- Feature flag `rwb.agent.client`: off means no call and the rule result is applied and logged.
- Rollback: flag off; redeploy the previous tag; the added nullable column is harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-013-01 | AC1, BR1, BR4 | System | Case RW-2026-000201, SHADOW, answer 2,000 ms | Answer stored; rule applied; log recommendation null; no output to caller |
| TC-TE-013-02 | AC2, BR2 | System | Orchestrator silent 61 s | Rule applied; `TIMED_OUT`; log fallback true; step continues |
| TC-TE-013-03 | AC3, BR1 | System | L1, confidence 0.91 | Rule applied; recommendation with 0.91; log recommendation |
| TC-TE-013-04 | AC4 | System | Answer fails `SCHEMA` | Rule applied; log fallback reason `SCHEMA` |
| TC-TE-013-05 | AC5 | System | No approved policy on 2026-11-30 | No call; `NO_POLICY`; no run row |
| TC-TE-013-06 | AC6, BR3 | System | Decision log writer throws | No action; case stays NEW; MSG-P7-003; run link empty |
| TC-TE-013-07 | AC7, BR5 | System | Step key `CASEWF:RW-2026-000201:ENTRY:2026-11-30` twice | One run, one entry, first outcome |
| TC-TE-013-08 | AC8 | System | Mode OFF | No call, no run; log agent version null, fallback false |
| TC-TE-013-09 | X7 | Security | RW-CASEOWN calls `GET /admin/agent-runs` | 403 MSG-P4-002 |
| TC-TE-013-10 | BR3, X4 | Resilience | Log write forced to fail in SHADOW | Step does not act; MSG-P7-003; incident |
| TC-TE-013-11 | BR5, CLAR-003 | Unit | Step key of 80 and 81 chars | 80 accepted; 81 rejected before the call |

## Guardrails and out of scope

- No business value in code: mode and timeout come from the approved policy.
- No personal data in logs, tests or prompts; the inputs snapshot is masked before it is referenced.
- No read of another module's table; the decision log is written only through P7.
- The client never applies an agent answer as the case result in SHADOW or L1.
- Out of scope: the orchestrator, gateway and guardrail checker (RWB-E1-058); L2+ autonomy (E8); the
  case steps that call the client (RWB-E2-028, RWB-E2-029).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records rule, model, agent and prompt versions | Program 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-01..04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Program 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-39 | TC-TE-013-06, 10 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | Program 5.4 | FEAT-AGT-01 | All recovery processes | R-UNI-40 | TC-TE-013-05, 07, 08, 09 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC3; SPEC-008 | Where is the confidence 0.91 stored, since the decision log has no confidence column? | Log mapping. | Inside `decision_log_entry.recommendation` jsonb, whose definition includes confidence (DF-DEC-009). | RESOLVED | SPEC-008 |
| CLAR-002 | BR1, AC3; SPEC-006 | Does L1 apply the agent answer or only recommend it? | Case outcome. | Only recommend; the rule result is always the applied result (BR1). | RESOLVED | SPEC-006 |
| CLAR-003 | BR5, AC7; SPEC-011 | The step key is used for `agent_run.idempotency_key` (120) and `decision_log_entry.idempotency_key` (80). What if it is longer than 80? | Repeat lookup and write failure. | The client validates the step key at 80 characters and rejects a longer key before any call; callers use the documented format. | RESOLVED | SPEC-011 |
| CLAR-004 | AC8; SPEC-003 | Does mode OFF still write a decision log entry? | Audit completeness. | Yes, with agent version null and fallback false; the decision is still recorded. | RESOLVED | SPEC-003 |
| CLAR-005 | BR2; SPEC-004 | Is the timeout enforced by the client, the orchestrator or both? | Double timeout and latency. | Both use the same policy value; the client bounds its wait, the orchestrator bounds the gateway call. | RESOLVED | SPEC-004 |
| CLAR-006 | BR6; SPEC-012 | Which identity writes the decision log? | Authority. | The calling module calls P7; P7 writes under `SY-DECLOG`. | RESOLVED | SPEC-012 |
| CLAR-007 | X3; SPEC-003 | What reason is recorded when no policy exists? | Fallback reason. | `NO_POLICY`; the story names it in AC5. | RESOLVED | SPEC-003 |
| CLAR-008 | AC6; SPEC-010 | Is the agent run kept when the log write fails? | Evidence and cost. | Yes; the run stays with `decision_log_id` empty, proving the call happened and the action did not. | RESOLVED | SPEC-010 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the TSD or the decision
log. No item changes a business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend enabler.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New internal agent-step client on the existing agent platform; no REST or screen change; run read endpoint reused.
CHANGE_CLASSIFICATION_RESULT: ENHANCEMENT_LOGIC_ONLY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: internal published interface and decision log mapping on an existing capability]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 8 acceptance criteria, 7 exception paths and 3 modes are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
