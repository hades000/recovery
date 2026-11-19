# Increment Card — INC-039-epic-1-RWB-TE-013

**RWB-TE-013 — Agent runtime client with fallback**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-039` |
| Title | Agent runtime client with fallback |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-013` |
| RUN_ID | `INC-039-epic-1-RWB-TE-013` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P10 Agent runtime |
| Story type | Enabler |
| Priority | Must |
| Build order | 39 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-TE-007, RWB-E1-058, RWB-E1-027 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P10 Agent runtime.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **one client in the recovery module that calls the agent orchestrator, applies the autonomy mode, runs shadow mode and falls back to the rule result**, so that **agents are added to a case step without changing the case flow, and every step records what the agent did**.

**Business outcome:** A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The client puts every agent call behind one interface: the rule result always exists, the agent answer is used only as the autonomy mode allows, and the decision log entry records the rule, agent and prompt versions and any fallback (REQ-DRI-001). If the entry cannot be written, the step does not act (REQ-DRI-005). The measure is the agent fallback rate, target below 10 percent per month.

**Main flow:**
1. Calling step (for example SY-CASEWF): evaluates its rule package through RuleEvaluator and builds the rule result (rule ID, rule version, next state).
2. Calling step: calls AgentStepClient.runStep with the agent code, case ID, decision code, step key and rule result.
3. Client: reads the autonomy mode from the agent policy in force; if it is OFF or the flag is off, it skips the agent.
4. Client: calls AgentOrchestrator.run with the idempotency key built from the step key and waits at most timeout_seconds.
5. Client: in SHADOW mode, keeps the rule result as the applied result and records the agent answer only.
6. Client: in L1 mode, keeps the rule result as the applied result and returns the checked agent answer as the recommendation for the person who decides.

**Acceptance criteria:**
- AC1: Shadow
- AC2: No answer
- AC3: Assisted mode returns the answer as a recommendation
- AC4: A guardrail failure falls back
- AC5: No approved policy
- AC6: The decision log write fails
- AC7: A repeated step key
- AC8: Agent switched off

**Out of scope:**
- The orchestrator, gateway and guardrail checker (RWB-E1-058).
- Agent answers acted on without a person (autonomy L2 and above, Epic 8, FEAT-AGT-15).
- The case steps that call the client: case intake (RWB-E2-028), deviation screening (RWB-E2-029).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-013-agent-runtime-client-with-fallback-v1.md` |
| Requirement IDs | REQ-DRI-001, REQ-DRI-005, REQ-ACA-010 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, sections 5.4 and 5.7 |
| Decision | DL33 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF and other calling module identities | Call AgentStepClient; write the decision log entry through P7 (Decision log C) |
| SY-AGENT | Runs the agent and its tools (read only) |
| SY-DECLOG | Writes the entry |
| RW-PLATADM, RW-COE, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs and fallbacks through GET /admin/agent-runs (Platform administration R) |

## Contract extract

**Published interface** ```java package recovery.agent.api; public interface AgentStepClient { AgentStepOutcome runStep(AgentStepRequest request) throws DecisionNotRecordedException; } public record AgentStepRequest(String agentCode, UUID caseId, String decisionCode, String stepKey, RuleResult ruleResult, Map<String, Object> inputs) {} public record RuleResult(String ruleId, String ruleVersion, String toState, JsonNode result) {} public record AgentStepOutcome(UUID decisionLogEntryId, RuleResult appliedResult, JsonNode recommendation, boolean fallback, String fallbackReason, String autonomyMode, UUID agentRunId) {} ``` **Decision log mapping** (DecisionLogWriter.write): case_id = caseId; decision_code = decisionCode; rule_id and rule_version from ruleResult; agent_version = "<agent>@<policy_version>/<prompt_version>" or null; model_version from the run; inputs_ref = reference to the mas…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: mode and timeout come from the approved agent policy. - No personal data in logs, tests or prompts; the inputs snapshot is masked before it is referenced. - No read of another module's tables; the decision log is written only through the P7 interface. - The client never applies an agent answer as the case result in SHADOW or L1.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-013-agent-runtime-client-with-fallback-v1.md` |
| Specification | `output/INC-039-epic-1-RWB-TE-013/specify/spec.md` |
| Compliance validation | `output/INC-039-epic-1-RWB-TE-013/specify/compliance-validation.md` |
| Agent run log | `output/INC-039-epic-1-RWB-TE-013/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-039-epic-1-RWB-TE-013/plan/` |
| Implementation evidence | `output/INC-039-epic-1-RWB-TE-013/implement/` |
| API / functional test reports | `output/INC-039-epic-1-RWB-TE-013/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-039-epic-1-RWB-TE-013/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-013-agent-runtime-client-with-fallback-v1.md` |
| Output run | `output/INC-039-epic-1-RWB-TE-013/` |

