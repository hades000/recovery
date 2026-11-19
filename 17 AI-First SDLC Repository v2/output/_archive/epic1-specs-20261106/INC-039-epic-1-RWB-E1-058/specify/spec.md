# Technical Specification — RWB-E1-058 Agent platform set-up [E1a]

| Field | Value |
|---|---|
| Story | RWB-E1-058 — Agent platform set-up [E1a] |
| Epic / module | E1 / P10 Agent runtime |
| RUN_ID | `INC-039-epic-1-RWB-E1-058` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-019); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 058 Agent platform set up E1a v1.md` |
| Upstream IDs | BRD-RWB-010; FR-RWB-019; AC-RWB-019; BR-RWB-013; REQ-ACA-005, REQ-ACA-010, REQ-DRI-010; US-RWB-E1-058; FEAT-AGT-01, FEAT-AGT-02, FEAT-AGT-05, FEAT-AGT-11; R-UNI-32, R-UNI-38, R-UNI-40; CTL-08, CTL-11; DL11, DL33 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route, label or state. SCR-46 Agent monitor is E2 (RWB-E2-031). |
| Logic In Scope | `YES` — config versions, gateway call, guardrails, masking, evaluation, cost, idempotency and fallback. |
| API In Scope | `YES` — seven admin operations across five paths are implemented for the first time: `GET /admin/agent-runs`, `GET|POST /admin/agent-configs`, `POST /admin/agent-configs/{versionId}/approve`, `POST /admin/agent-samples`, `POST|GET /admin/agent-evaluations`. The OpenAPI contract already exists in `api.yaml`; no new contract authoring is required. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | New tables `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation`; new controllers and services in P10. Reused published interfaces: P4 masking (RWB-E1-037), P7 `DecisionLogWriter` (RWB-E1-027), P3 case read, P5 document read, P1 collateral read. |
| New Nodes Required | `YES` — `AgentRuntimeController`, `AgentConfigController`, `AgentEvaluationController`, `ModelGatewayClient`, `AgentConfigService`, `AgentOrchestrator`, `AgentRuntimeService`, `ToolGateway`, `GuardrailChecker`, `PromptInputMasker`, `EvaluationHarness`, three repositories and six entities. |
| Inherited Existing Behavior | Recovery tables (RWB-E1-001), account/arrears load (RWB-E1-003), masking by role (RWB-E1-037), decision log writer (RWB-E1-027), configuration service (RWB-E1-042), migrations (RWB-E1-044), Quartz job pattern (RWB-TE-007), feature flags (RWB-E1-047). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every model call goes through `ModelGatewayClient` to the INT-23 endpoint; no other component calls it. | SPEC-RWB-E1-058-001, SPEC-RWB-E1-058-003 | DIRECT | Gateway is the only class holding the endpoint client; ArchUnit rule. | COVERED |
| BR2 | The policy and prompt versions in force on the run date with status APPROVED are used; an open run keeps its versions. | SPEC-RWB-E1-058-002, SPEC-RWB-E1-058-014 | DIRECT | Resolve by `valid_from <= runDate < valid_to`; snapshot on `agent_run`. | COVERED |
| BR3 | No answer inside `timeout_seconds` (60, assumed; DL11) ends the run `TIMED_OUT`; the rule result is used. | SPEC-RWB-E1-058-003, SPEC-RWB-E1-058-021 | DIRECT | Gateway timeout from policy; no retry inside the step. | COVERED |
| BR4 | Every answer is checked in order: schema, allowed tool list, confidence floor; the first failure sets status and fallback. | SPEC-RWB-E1-058-004, SPEC-RWB-E1-058-005, SPEC-RWB-E1-058-006, SPEC-RWB-E1-058-007 | DIRECT | `GuardrailChecker` fixed order; later checks not run. | COVERED |
| BR5 | Personal fields are masked through P4 before any value reaches a prompt. | SPEC-RWB-E1-058-008 | DIRECT | `PromptInputMasker` on every input value; log filter test. | COVERED |
| BR6 | The agent runs as `SY-AGENT` and passes the same permission check as a person on every tool call. | SPEC-RWB-E1-058-009 | DIRECT | `ToolGateway` under managed identity; P4 check per tool. | COVERED |
| BR7 | Cost = (tokens in + tokens out) / 1,000 × price per 1,000 tokens, 4 decimals. | SPEC-RWB-E1-058-010 | DIRECT | `BigDecimal`, `HALF_UP`; 1,050 tokens at 0.0500 = 0.0525. | COVERED |
| BR8 | A version is loaded by RW-COE and approved by RW-RISK; the same person may not do both. | SPEC-RWB-E1-058-012 | DIRECT | Compare approver with `loaded_by`; 409 MSG-P7-002. | COVERED |
| BR9 | A run request with a used idempotency key returns the first result. | SPEC-RWB-E1-058-015 | DIRECT | Unique `agent_run.idempotency_key`; return stored result; count hit. | COVERED |
| BR10 | A file load is refused in full if any row fails a check. | SPEC-RWB-E1-058-011 | DIRECT | Validate whole file before insert; no partial row. | COVERED |
| BR11 | No model name, threshold, timeout, price or tool list is written in code. | SPEC-RWB-E1-058-011, SPEC-RWB-E1-058-024 | DIRECT | All values from approved policy/prompt rows; loader JSON schema holds limits only. | COVERED |
| AC1 | A run on the approved endpoint returns `ANSWERED` with versions, latency, tokens, cost and one EV-28. | SPEC-RWB-E1-058-001, SPEC-RWB-E1-058-003, SPEC-RWB-E1-058-010, SPEC-RWB-E1-058-016 | DIRECT | One transaction for row and outbox. | COVERED |
| AC2 | PR2 approved from 2026-11-20 exists as APPROVED; PR1 stays readable with its hash; runs switch on the date. | SPEC-RWB-E1-058-002, SPEC-RWB-E1-058-014 | DIRECT | Effective dating; `body_hash` unchanged. | COVERED |
| AC3 | A missing `summary` fails SCHEMA; status `GUARDRAIL_FAILED`, fallback true, count rises. | SPEC-RWB-E1-058-004, SPEC-RWB-E1-058-005 | DIRECT | JSON Schema 2020-12; check code and field name stored. | COVERED |
| AC4 | An evaluation on 20 labeled rows ends DONE with 20 runs and one score row per label key. | SPEC-RWB-E1-058-017 | DIRECT | One run per distinct subject; scores per label key. | COVERED |
| AC5 | A tool outside the allow-list is refused, not executed; status `GUARDRAIL_FAILED`; fallback reason `TOOL_NOT_ALLOWED`. | SPEC-RWB-E1-058-004, SPEC-RWB-E1-058-006, SPEC-RWB-E1-058-009, SPEC-RWB-E1-058-021 | DIRECT | Allow-list from policy; refusal logged. | COVERED |
| AC6 | No answer in 61 seconds ends at 60,000 ms; status `TIMED_OUT`; fallback `TIMED_OUT`. | SPEC-RWB-E1-058-003, SPEC-RWB-E1-058-021 | DIRECT | Policy timeout; latency recorded at cutoff. | COVERED |
| AC7 | The request, run row and log hold masking tokens, no national ID, phone, name or account number. | SPEC-RWB-E1-058-008 | DIRECT | Mask every input value; log pattern scan. | COVERED |
| AC8 | A policy file with `timeout_seconds` 0 is refused 422 MSG-P10-001; P1 stays in force; no new row. | SPEC-RWB-E1-058-011 | DIRECT | Loader schema 1..120; validate before insert. | COVERED |
| AC9 | The loader cannot approve their own version: 409 MSG-P7-002; version stays LOADED. | SPEC-RWB-E1-058-012 | DIRECT | Separation-of-duty check. | COVERED |
| AC10 | Confidence 0.79 against floor 0.80 gives `BELOW_FLOOR`, fallback true, reason `BELOW_FLOOR`. | SPEC-RWB-E1-058-007, SPEC-RWB-E1-058-021 | DIRECT | Floor from policy; compare 4-decimal confidence. | COVERED |
| AC11 | A repeated key writes no second row, makes no second call and returns the first result. | SPEC-RWB-E1-058-015 | DIRECT | Unique key; repeat counted. | COVERED |
| AC12 | Two simultaneous approvals: one succeeds; the other gets 409 MSG-GEN-004. | SPEC-RWB-E1-058-013 | DIRECT | `If-Match` row version and optimistic lock. | COVERED |
| AC13 | An evaluation on an empty sample is refused 422 MSG-P10-002; no run rows. | SPEC-RWB-E1-058-018 | DIRECT | Count labeled rows before creating the run. | COVERED |
| AC14 | A second evaluation while one is RUNNING is refused 409 MSG-P10-003. | SPEC-RWB-E1-058-019 | DIRECT | Partial unique index on agent, sample, version where RUNNING. | COVERED |
| AC15 | `GET /admin/agent-runs` returns metadata only, no prompt, answer or personal field. | SPEC-RWB-E1-058-020 | DIRECT | Projection excludes `output`, `guardrail_result` and prompt text. | COVERED |
| X1 | Model endpoint silent past the policy timeout. | SPEC-RWB-E1-058-003, SPEC-RWB-E1-058-021 | DIRECT | `TIMED_OUT`, fallback true. | COVERED |
| X2 | Answer fails its output schema. | SPEC-RWB-E1-058-005, SPEC-RWB-E1-058-021 | DIRECT | `SCHEMA`, field name. | COVERED |
| X3 | Agent asks for a tool not on its list. | SPEC-RWB-E1-058-006, SPEC-RWB-E1-058-021 | DIRECT | Refused, not executed, `TOOL_NOT_ALLOWED`. | COVERED |
| X4 | Answer below the confidence floor. | SPEC-RWB-E1-058-007, SPEC-RWB-E1-058-021 | DIRECT | `BELOW_FLOOR`. | COVERED |
| X5 | Prompt or policy file fails a load check. | SPEC-RWB-E1-058-011 | DIRECT | 422 MSG-P10-001; no row. | COVERED |
| X6 | Loader tries to approve their own version. | SPEC-RWB-E1-058-012 | DIRECT | 409 MSG-P7-002. | COVERED |
| X7 | Two approvals at once. | SPEC-RWB-E1-058-013 | DIRECT | 409 MSG-GEN-004. | COVERED |
| X8 | Same run request twice. | SPEC-RWB-E1-058-015 | DIRECT | One row, one call, first result. | COVERED |
| X9 | Evaluation on a sample with no labels. | SPEC-RWB-E1-058-018 | DIRECT | 422 MSG-P10-002. | COVERED |
| X10 | Evaluation already RUNNING for the agent and sample. | SPEC-RWB-E1-058-019 | DIRECT | 409 MSG-P10-003. | COVERED |
| X11 | Role without the right calls an endpoint. | SPEC-RWB-E1-058-023 | DIRECT | 403 MSG-P4-002; nothing changes. | COVERED |

## User story intent interpretation

As a **platform administrator (RW-PLATADM)**, I want **the model gateway, the prompt and policy store, the guardrail checker and the evaluation harness deployed in the recovery module**, so that **every Workbench agent is built, called, checked and scored through one path with its versions recorded**.

The story is the platform under every later agent. It adds no screen. It gives RW-COE a versioned load path, RW-RISK an approval path, every calling module one orchestrator entry, and RW-PLATADM a metadata-only run list. The test agent `ECHO` proves every path without any business agent.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `AgentOrchestrator.run` from a calling module; `POST /admin/agent-evaluations` from RW-COE; admin endpoints from RW-COE, RW-RISK and RW-PLATADM. |
| Preconditions | RWB-E1-001 and RWB-E1-003 done; RWB-E1-037 masking for `SY-AGENT`; `SY-AGENT` managed identity with Case record R, Documents R, Rules and parameters R, Reference data R, Decision log C; INT-23 reachable on the SCB private endpoint; RW-COE and RW-RISK holders exist. |
| Input | Agent code, case/subject ID, trigger event, idempotency key, masked inputs; prompt and policy files; labeled sample CSV. |
| Output | `agent_run` row, guardrail result, fallback result, EV-28 in the outbox; config versions; evaluation run and score rows. |
| Feature flag | `rwb.agent.platform`. Off: orchestrator returns `DISABLED` with fallback true and makes no model call. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `agent_policy` | `status` | `LOADED` on load | `LOADED` → `APPROVED` → `RETIRED` | Only RW-RISK approves; loader ≠ approver. |
| `agent_policy` | `valid_from`, `valid_to` | Load file / retirement | System-written | `valid_from` required; retirement sets `valid_to` to the day before the successor. |
| `agent_policy` | `timeout_seconds` | Policy file | System-written | Integer 1..120; default example 60 (DL11). |
| `agent_policy` | `confidence_floor` | Policy file | System-written | 0..1, 4 decimals. |
| `agent_policy` | `allowed_tools` | Policy file | System-written | JSON array; empty means no tool. |
| `agent_policy` | `config` | Policy file | System-written | Versioned JSON for agent-specific parameters (look-back, ledger window, extraction target); design extension, see SPEC-024. |
| `agent_policy` | `body_hash` | Policy file | System-written | SHA-256 of the canonical file; makes `bodyHash` available for POLICY. |
| `agent_prompt` | `body_hash` | Prompt file | System-written | SHA-256; unchanged when a later version is approved. |
| `agent_run` | `status` | Run request | `ANSWERED`, `TIMED_OUT`, `GUARDRAIL_FAILED`, `BELOW_FLOOR`, `TOOL_UNAVAILABLE`, `MODEL_ERROR`, `DISABLED` | One terminal status per run. |
| `agent_run` | `idempotency_key` | Calling step | System-written | Unique; repeat returns first result. |
| `agent_run` | `cost_thb` | Token counts × price | System-written | 4 decimals. |
| `agent_evaluation_run` | `status` | `RUNNING` | `RUNNING` → `DONE` / `FAILED` | One RUNNING per agent, sample and sample version. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Config file loaded | Every check passes | `LOADED` | New version row; earlier versions readable. |
| None | Config file loaded | A check fails | No row | 422 MSG-P10-001; version in force unchanged. |
| `LOADED` | Approved by RW-RISK | Approver ≠ loader and `If-Match` matches | `APPROVED` | `approved_by`; effective on `valid_from`. |
| `APPROVED` | Later version approved | Later `valid_from` reached | `RETIRED` | `valid_to` = day before the successor. |
| None | Run requested | Every check passes | `ANSWERED` | Run row, EV-28, checked answer. |
| None | Run requested | Timeout, schema, tool or floor failure | `TIMED_OUT` / `GUARDRAIL_FAILED` / `BELOW_FLOOR` | Fallback true; reason returned. |
| None | Evaluation started | Sample has labels; none running | `RUNNING` | Evaluation run row. |
| `RUNNING` | Last sample subject scored | No error | `DONE` | Score rows and counts. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Endpoint silent past the timeout | Call ended at policy timeout; `TIMED_OUT`; fallback `TIMED_OUT` | None to a user |
| X2 | Answer fails the output schema | `GUARDRAIL_FAILED`; check `SCHEMA`; missing field recorded | None to a user |
| X3 | Tool not on the allow-list | Refused and not executed; `GUARDRAIL_FAILED`; `TOOL_NOT_ALLOWED` | None to a user |
| X4 | Confidence below the floor | `BELOW_FLOOR`; fallback true | None to a user |
| X5 | Prompt/policy file fails a check | Whole load refused; no row; version in force unchanged | MSG-P10-001 |
| X6 | Loader approves own version | 409; version stays `LOADED` | MSG-P7-002 |
| X7 | Concurrent approvals | First wins; second 409 | MSG-GEN-004 |
| X8 | Repeated run key | No second row or call; first result returned; hit counted | None to a user |
| X9 | Evaluation on an empty sample | 422; no evaluation or run row | MSG-P10-002 |
| X10 | Evaluation already RUNNING | 409; one RUNNING row remains | MSG-P10-003 |
| X11 | Role without the right | 403; nothing changes | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` — seven admin operations across five paths implemented for the first time; the OpenAPI contract is already in `api.yaml`. |
| Endpoints | `GET /api/recovery/v1/admin/agent-runs` (API-P10-001); `GET|POST /admin/agent-configs` (API-P10-002/003); `POST /admin/agent-configs/{versionId}/approve` (API-P10-004); `POST /admin/agent-samples` (API-P10-005); `POST|GET /admin/agent-evaluations` (API-P10-006/007). |
| Contract delta | `POST /admin/agent-evaluations` answers **202** (story §12, build notes) while `api.yaml` says 201 — the story governs and the spec records the delta (CLAR-001). `AgentConfigVersion.bodyHash` is populated for POLICY from the new `agent_policy.body_hash` (CLAR-003). |
| Backward compatibility | New endpoints; no existing response changes. |
| Authorization | Platform administration R for runs; Rules and parameters R/C/A for configs and evaluations. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 unknown version; 409 duplicate version, self-approval, row change, running evaluation; 422 MSG-P10-001/002; 503 store or endpoint unavailable. |
| Versioning | No version change; additive contract clarifications only. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label. SCR-46 is E2. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-019; SPEC-RWB-E1-058-001..024 | New controllers, services, gateway, guardrail, masker, harness and repositories. | Positive, negative, boundary and error-path tests: config load/approve, effective dates, timeout, schema, tool, floor, masking, cost, idempotency, evaluation, empty sample, concurrency, access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `AgentRuntimeController` | Controller | `GET /admin/agent-runs`; problem responses. |
| `AgentConfigController` | Controller | `GET|POST /admin/agent-configs`; approve. |
| `AgentEvaluationController` | Controller | Samples, evaluations and evaluation read. |
| `ModelGatewayClient` | Service | Sole caller of INT-23; policy model and timeout; returns answer, tokens, latency. |
| `AgentConfigService` | Service | Validate, store, approve, resolve version in force, separation of duty. |
| `AgentOrchestrator` | Published interface | One agent step: resolve, gather, mask, call, check, record. |
| `AgentRuntimeService` | Service | Implements the orchestrator; writes run and EV-28 in one transaction. |
| `ToolGateway` | Service | Executes only allowed tools as `SY-AGENT` through P3/P5/P1 interfaces. |
| `GuardrailChecker` | Service | Schema, tool allow-list and confidence-floor checks with check codes. |
| `PromptInputMasker` | Service | Calls P4 masking for every input value before the prompt is built. |
| `EvaluationHarness` | Service | Runs the agent in shadow per sample subject; scores per label key. |
| `AgentRunRepository`, `AgentConfigRepository`, `AgentEvaluationRepository` | Repository | P10 tables only. |

### Package and boundaries

`recovery.agent` with `gateway`, `config`, `orchestrator`, `guardrail`, `eval`, `api`. The orchestrator is the only published entry; other modules never import `gateway` or repositories. The boundary test (ArchUnit) rejects any import outside `recovery.agent.api`/`orchestrator`. No other module's table is read.

### Data and migration

`V10_001__agent_runtime.sql` creates `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation_run` and `agent_evaluation` in schema `recovery` with the standard record columns. Constraints: unique `(agent_code, policy_version)`, unique `(agent_code, prompt_version)`, unique `(idempotency_key)` on `agent_run`, unique `(agent_code, sample_code, sample_version, subject_id, label_key)` on `agent_sample`, partial unique index on `(agent_code, sample_code, sample_version)` where `status = 'RUNNING'`; index `agent_run (agent_code, run_at)`. The migration adds `agent_policy.config` (jsonb) and `agent_policy.body_hash` (char(64)) as the design extension in SPEC-024. No hard-coded business value.

### Run sequence

1. Resolve the approved policy and prompt in force on the run date.
2. `ToolGateway` executes only allowed tools as `SY-AGENT`; `PromptInputMasker` masks every value.
3. `ModelGatewayClient` calls INT-23 with the policy timeout; no retry inside the step.
4. `GuardrailChecker` runs schema → tool list → floor; first failure wins.
5. Write `agent_run` and EV-28 in one transaction; return the result or fallback.
6. A repeat with the same key returns the stored result and counts the hit.

### Guardrail order

| Order | Check | Failure code | Run status |
|---|---|---|---|
| 1 | JSON Schema 2020-12 against `output_schema_ref` | `SCHEMA` + field name | `GUARDRAIL_FAILED` |
| 2 | Requested tools against `allowed_tools` | `TOOL_NOT_ALLOWED` | `GUARDRAIL_FAILED` |
| 3 | Confidence against `confidence_floor` | `BELOW_FLOOR` | `BELOW_FLOOR` |

### Evaluation harness

One agent run per **distinct sample subject** (case or document), not per label row; one score row per label key and approach. This reconciles AC4 (20 subjects → 20 runs) with RWB-E1-059 (200 cases → 200 runs) and RWB-E1-060 (one run per document). The run row carries `evaluation_run_id`; scores carry sample size, TP, FP, FN, agreement, precision and recall. Score reads join the policy, prompt and model versions from the run.

### Transaction, events and cost

`agent_run` and the EV-28 outbox row are written in one transaction. Cost is `(tokens_in + tokens_out) / 1000 × price_per_1k_tokens_thb`, `HALF_UP`, 4 decimals. Prompt text and model answers never enter the application log or this story's API responses.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-COE | Rules and parameters CRUD | All |
| RW-RISK | Rules and parameters A; read | All |
| RW-PLATADM | Platform administration R | All |
| RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Platform administration R | All |
| `SY-AGENT` | Case record R, Documents R, Rules and parameters R, Reference data R, Decision log C | All |

Every endpoint carries a Spring Security method check; every tool call repeats the P4 permission check for `SY-AGENT`.

### Observability, performance and rollback

- Metrics: runs by status, fallback rate, guardrail failures by code, latency, tokens, cost, idempotency hits, evaluation duration.
- Alerts: endpoint unavailable, fallback rate above 10 percent, cost cap breach (RWB-E1-063), guardrail spike.
- Performance: answer target under 60 seconds (NFR-010); the gateway adds one call and one run insert.
- Feature flag `rwb.agent.platform`: off returns `DISABLED` with fallback true and makes no model call.
- Rollback: flag off; redeploy the previous tag; the migration is forward-only and the new tables are inert.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-058-01 | AC1, BR1, BR7 | System | ECHO, case RW-2026-000101, 1,200 ms, 900/150 tokens | `ANSWERED`; versions, latency, tokens, cost 0.0525; EV-28 |
| TC-E1-058-02 | AC2, BR2 | System | PR1 then PR2 from 2026-11-20; runs on 19 and 20 November | PR1 on 19th, PR2 on 20th; PR1 hash unchanged |
| TC-E1-058-03 | AC3, BR4 | System | Stub answer missing `summary` | `GUARDRAIL_FAILED`, `SCHEMA`, field name, count +1 |
| TC-E1-058-04 | AC4 | System | ECHO-S1 v1, 20 subjects | DONE; 20 runs; one score row per label key |
| TC-E1-058-05 | AC5, BR4, BR6 | System | Tool `propose_deviation` with allow-list `read_case` | Refused, not executed; `TOOL_NOT_ALLOWED` |
| TC-E1-058-06 | AC6, BR3 | System | Stub silent 61 s | Ends at 60,000 ms; `TIMED_OUT`; fallback |
| TC-E1-058-07 | AC7, BR5 | System | Synthetic national ID and mobile | Masking tokens only; no personal pattern in request, row or log |
| TC-E1-058-08 | AC8, BR10 | System | Policy with `timeout_seconds` 0 | 422 MSG-P10-001; no row; P1 in force |
| TC-E1-058-09 | AC9, BR8 | System | `coe.user01` approves own P2 | 409 MSG-P7-002; P2 stays LOADED |
| TC-E1-058-10 | AC10, BR4 | System | Confidence 0.79, floor 0.80 | `BELOW_FLOOR`; fallback |
| TC-E1-058-11 | AC11, BR9 | System | Key `ECHO:RW-2026-000101:2026-11-30` twice | One row, one call, first result, hit counted |
| TC-E1-058-12 | AC12 | System | Two parallel approvals, row version 1 | One APPROVED; one 409 MSG-GEN-004 |
| TC-E1-058-13 | AC13 | System | ECHO-S2 with 0 rows | 422 MSG-P10-002; no run rows |
| TC-E1-058-14 | AC14 | System | ECHO-S1 v1 already RUNNING | 409 MSG-P10-003; one RUNNING |
| TC-E1-058-15 | AC15 | System | Three ECHO runs, 30 Nov–1 Dec | Three metadata items; no prompt, answer or personal field |
| TC-E1-058-16 | X11 | Security | RW-CASEOWN calls both admin endpoints | 403 MSG-P4-002; nothing changes |
| TC-E1-058-17 | BR2, AC2 | Unit | Effective-date resolver at boundaries | Correct version on the day before, on and after `valid_from` |

## Guardrails and out of scope

- No business value in code: model, prompt, timeout, floor, tool list, price and cap are approved version rows.
- No personal data in logs, tests, prompts or responses; test data is synthetic in DEV and masked in SIT.
- No read of another module's table; case and document facts come through P3/P5, the decision log through P7.
- The model endpoint is reached only through `ModelGatewayClient` on the private endpoint.
- Out of scope: the rule fallback and decision log entry in a case step (RWB-TE-013); the intake, extraction and screening agents (RWB-E1-059/060/062); the dashboard and cost alert (RWB-E1-063); autonomy screens and drift (E3); the choice of endpoint (DL33).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-010 | Agents run under service identities with the same role checks as people | Program 5.4 | FEAT-AGT-01, FEAT-AGT-02 | All recovery processes | R-UNI-32, R-UNI-40 | TC-E1-058-01, 05, 16 |
| REQ-ACA-005 | Personal data masked by role in every agent call | Program 5.4 | FEAT-AGT-01 | All recovery processes | CTL-11 | TC-E1-058-07 |
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | Program 5.7 | FEAT-AGT-01, 05, 11 | 15 Manage performance, data and AI | R-UNI-38 | TC-E1-058-02, 04, 06, 08, 09 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Contract; SPEC-019 | Does `POST /admin/agent-evaluations` answer 201 or 202? | Status code and async semantics. | 202 per story §12 and the build notes; `api.yaml` says 201 and is corrected as a documentation defect (F-01). | RESOLVED | SPEC-019 |
| CLAR-002 | AC4; SPEC-017 | Does a score row carry the policy, prompt and model versions, or does the run? | Normalisation and read join. | Versions live on `agent_evaluation_run`; the score read joins them so each returned score row carries them. | RESOLVED | SPEC-017 |
| CLAR-003 | AC15; SPEC-024 | What is `bodyHash` for a POLICY version, since only prompts have a hash? | API field completeness. | Add `agent_policy.body_hash` and populate it with the canonical policy file hash; prompt hashes unchanged. | RESOLVED | SPEC-024 |
| CLAR-004 | AC4; SPEC-017 | Does the harness run once per sample row or per subject? | Run count, cost and report denominators. | Once per distinct subject; scores per label key. ECHO-S1 has 20 subjects; INTAKE has 200 cases; EXTRACT has one run per document. | RESOLVED | SPEC-017 |
| CLAR-005 | BR3, BR7; SPEC-003, 010 | Are 60 seconds and 0.0500 baht approved values? | Timeout and cost. | 60 seconds (DL11) and 0.0500 baht (DL33) are assumed policy values; tests use them as fixtures, not constants. | RESOLVED | SPEC-003, 010 |
| CLAR-006 | BR10; SPEC-011 | Where do the loader limits live? | Validation. | Policy JSON schema versioned with the loader: timeout 1..120, floor 0..1. | RESOLVED | SPEC-011 |
| CLAR-007 | BR11; SPEC-024 | Where do agent-specific parameters with no column live? | Schema extension. | Add `agent_policy.config` (jsonb) for look-back, ledger window and extraction target; loaded and approved with the policy. TSD T3 update required (F-02). | RESOLVED | SPEC-024 |
| CLAR-008 | AC1; SPEC-001 | Is `ECHO` a real agent or a test fixture? | Seed data. | Test agent seeded from `src/test/resources/agent/`; not a LOV-AGENT business agent. | RESOLVED | SPEC-001 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the build notes, the TSD or the decision log. No item changes a business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend platform story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New agent runtime platform: seven admin operations, gateway, versioned prompt/policy store, guardrails, masking and evaluation harness; no screen.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: first implementation of seven P10 admin operations with no UI]
REQUIREMENT_COVERAGE_SUMMARY: All 11 business rules, 15 acceptance criteria, 11 exception paths and 8 run/config states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 11] [COVERED_RULES: 11] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
