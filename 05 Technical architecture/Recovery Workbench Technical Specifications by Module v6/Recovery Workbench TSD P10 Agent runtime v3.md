SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P10 Agent runtime

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P10 Agent runtime |
| Document ID | P10-RWB-TSD-v3 |
| Version | 3 |
| Status | Draft |
| Date | 22 November 2026 |
| Supersedes | Version 2, 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads (GAP-1999; ASM-3225: no squad is named per service) |
| Decision | D-RCV-60 microservice realignment |
| Status note | Draft: no approval of version 3 is recorded (GAP-1998; ASM-3217) |
| Change | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P10 Agent runtime | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, endpoint, event, workflow and job in T0 and T5.2 |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

Under D-RCV-60 the scheduler and batch row is delivered by the Temporal layer (ADR-016): Temporal Schedules and event-started workflows in the owning service replace the Quartz and Spring Batch jobs (DP-10). The outbox and retry row is delivered by the Kafka outbox, inbox and retry topics (ADR-015; DP-09).

## T0. Service

P10 Agent runtime is one of the 19 services of Architecture v5: `rwb-agent` (service name Agent, module P10, wave 1, service epic `RWB-SVC-P10`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

P10 is the only caller of the enterprise AI endpoint, and it reaches Workbench data only through the read-only tool gateway (DP-20).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | P10 Agent runtime |
| Service | `rwb-agent` (Agent) |
| Service epic | `RWB-SVC-P10` |
| Wave | 1 |
| Schema | `rwb_agent` |
| Database login | `rwb_agent`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/agent/v1` |
| Kafka topic | `rwb.agent.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.agent.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-agent` |
| Java package | `th.co.scb.ace.workbench.recovery.agent` |
| Edge | gateway-bff for the agent administration and evaluation screens |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-agent.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: agent policies, prompts, runs, guardrails, evaluations. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_agent` | `agent_alert`, `agent_evaluation`, `agent_evaluation_run`, `agent_feedback`, `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample` | 8 |
| REST operations | appendix T-A and `rwb-agent.yaml` | 11 |
| Events published | EV-28 AgentRunCompleted | 1 |
| Workflows and schedules | AgentRunWorkflow | 1 |
| Jobs | none | 0 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_agent`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_agent`, with its own connection pool cap. |
| DP-03 | `…on events from P3 and writes through the decision log.` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-06 | `…api/recovery/v1/admin/agent-configs / Rules and parameters R / E1` | Parameters from the `rwb-case` contract and the client library (H RWB-PLT-E1042-CON). |
| DP-07 | `DF-AGT-002 / agent_code / LOV / varchar(30) / Yes / LOV-AGENT / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-COE Center of excellence analyst / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | `…state machine of its own; the module acts on events from P3 and writes through the decision…` | Outbox and inbox library; CloudEvents on `rwb.agent.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-P10-001 / GET / /api/recovery/v1/admin/agent-runs / Platform administration…` | REST base `/api/recovery/agent/v1`. |
| DP-14 | — | Topic `rwb.agent.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_agent`. |
| DP-19 | `NFR-008 / A screen responds within its target under normal…` | Screens composed by gateway-bff; one composite route per screen (H RWB-PLT-N001-CON). |
| DP-20 | `AgentRuntimeController / REST endpoints in appendix…` | Agent work through the `rwb-agent` contract (C RWB-P10-TE013-CON). |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It reaches no business table: every fact comes through the read-only tool gateway (DP-20).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

P10 Agent runtime is delivered as the service `rwb-agent` (module P10, wave 1, service epic `RWB-SVC-P10`): one repository, one pipeline, one schema `rwb_agent` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: orchestrator, tool gateway, guardrails, prompt store, evaluation, autonomy levels. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| AgentRuntimeController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| AgentRuntimeService | Business logic; calls the rules component; writes the decision log entry before any change |
| AgentRuntimeRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-agent` lives in schema `rwb_agent` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). Every object of T3.1 stays here: the agent estate is P10's alone and no other service reads an agent table (DP-01).

### T3.0 Standard record columns

| Column | Type | Meaning |
|---|---|---|
| is_active | boolean | The active or inactive status of the record |
| state | varchar(40) | Record lifecycle state |
| version | integer | Optimistic lock version |
| created_at | timestamptz | When the record was created |
| created_by | uuid | Who or which service identity created it |
| updated_at | timestamptz | When the record last changed |
| updated_by | uuid | Who or which service identity last changed it |

### T3.1 Object and field definitions

**agent_policy** (NEW). A version of an agent's policy: model, tools, autonomy, limits and fallback.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-AGT-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-AGT-002 | agent_code | LOV | varchar(30) | Yes | LOV-AGENT | Workbench |
| DF-AGT-003 | policy_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-AGT-004 | model_code | TEXT | varchar(40) | Yes | None | Workbench |
| DF-AGT-005 | model_version | TEXT | varchar(40) | Yes | None | Workbench |
| DF-AGT-006 | output_schema_ref | TEXT | varchar(400) | Yes | None | Workbench |
| DF-AGT-007 | allowed_tools | TEXT | jsonb | No | None | Workbench |
| DF-AGT-008 | autonomy_mode | LOV | varchar(10) | Yes | LOV-AUTONOMY | Workbench |
| DF-AGT-009 | segment_product_group | LOV | varchar(15) | No | LOV-PRODUCT | Workbench |
| DF-AGT-010 | segment_region_code | LOV | varchar(10) | No | LOV-REGION | Workbench |
| DF-AGT-011 | confidence_floor | NUMBER | numeric(5,4) | Yes | None | Workbench |
| DF-AGT-012 | timeout_seconds | NUMBER | integer | Yes | None | Workbench |
| DF-AGT-013 | daily_cost_cap_thb | NUMBER | numeric(12,2) | Yes | None | Workbench |
| DF-AGT-014 | price_per_1k_tokens_thb | NUMBER | numeric(10,4) | Yes | None | Workbench |
| DF-AGT-015 | alert_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-AGT-016 | review_date | DATE | date | No | None | Workbench |
| DF-AGT-017 | evaluation_run_id | CROSS_REF | uuid | No | None | Workbench |
| DF-AGT-018 | promotion_conditions | TEXT | jsonb | No | None | Workbench |
| DF-AGT-019 | watch_measures | TEXT | jsonb | No | None | Workbench |
| DF-AGT-020 | fallback_rule | TEXT | varchar(20) | No | None | Workbench |
| DF-AGT-021 | status | LOV | varchar(12) | Yes | LOV-CONFIG-STATUS | Workbench |
| DF-AGT-022 | valid_from | DATE | date | Yes | None | Workbench |
| DF-AGT-023 | valid_to | DATE | date | No | None | Workbench |
| DF-AGT-024 | loaded_by | USER_REF | uuid | Yes | None | Workbench |
| DF-AGT-025 | approved_by | USER_REF | uuid | No | None | Workbench |

**agent_prompt** (NEW). A version of an agent's prompt text.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-AGT-026 | id | TEXT | uuid | Yes | None | Workbench |
| DF-AGT-027 | agent_code | LOV | varchar(30) | Yes | LOV-AGENT | Workbench |
| DF-AGT-028 | prompt_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-AGT-029 | body_text | TEXT | text | Yes | None | Workbench |
| DF-AGT-030 | body_hash | TEXT | char(64) | Yes | None | Workbench |
| DF-AGT-031 | status | LOV | varchar(12) | Yes | LOV-CONFIG-STATUS | Workbench |
| DF-AGT-032 | valid_from | DATE | date | Yes | None | Workbench |
| DF-AGT-033 | valid_to | DATE | date | No | None | Workbench |
| DF-AGT-034 | loaded_by | USER_REF | uuid | Yes | None | Workbench |
| DF-AGT-035 | approved_by | USER_REF | uuid | No | None | Workbench |

**agent_run** (NEW). One call of an agent or model, with its versions, checks, answer, cost and fallback.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-AGT-036 | id | TEXT | uuid | Yes | None | Workbench |
| DF-AGT-037 | agent_code | LOV | varchar(30) | Yes | LOV-AGENT | Workbench |
| DF-AGT-038 | agent_version | TEXT | varchar(40) | Yes | None | Workbench |
| DF-AGT-039 | prompt_version | TEXT | varchar(20) | No | None | Workbench |
| DF-AGT-040 | model_version | TEXT | varchar(40) | Yes | None | Workbench |
| DF-AGT-041 | case_id | CROSS_REF | uuid | No | None | Workbench |
| DF-AGT-042 | subject_id | CROSS_REF | uuid | No | None | Workbench |
| DF-AGT-043 | autonomy_mode | LOV | varchar(10) | Yes | LOV-AUTONOMY | Workbench |
| DF-AGT-044 | trigger_event | TEXT | varchar(30) | Yes | None | Workbench |
| DF-AGT-045 | idempotency_key | TEXT | varchar(120) | Yes | None | Workbench |
| DF-AGT-046 | status | LOV | varchar(20) | Yes | LOV-AGENT-RUN | Workbench |
| DF-AGT-047 | fallback | BOOLEAN | boolean | Yes | None | Workbench |
| DF-AGT-048 | guardrail_result | TEXT | jsonb | No | None | Workbench |
| DF-AGT-049 | output | TEXT | jsonb | No | None | Workbench |
| DF-AGT-050 | confidence | NUMBER | numeric(5,4) | No | None | Workbench |
| DF-AGT-051 | latency_ms | NUMBER | integer | No | None | Workbench |
| DF-AGT-052 | tokens_in | NUMBER | integer | No | None | Workbench |
| DF-AGT-053 | tokens_out | NUMBER | integer | No | None | Workbench |
| DF-AGT-054 | cost_thb | NUMBER | numeric(12,4) | No | None | Workbench |
| DF-AGT-055 | data_as_of | DATE | date | No | None | Workbench |
| DF-AGT-056 | run_at | DATE | timestamptz | Yes | None | Workbench |
| DF-AGT-057 | evaluation_run_id | CROSS_REF | uuid | No | None | Workbench |
| DF-AGT-058 | decision_log_id | CROSS_REF | uuid | No | None | Workbench |
| DF-AGT-059 | segment_product_group | LOV | varchar(15) | No | LOV-PRODUCT | Workbench |
| DF-AGT-060 | segment_region_code | LOV | varchar(10) | No | LOV-REGION | Workbench |

**agent_sample** (NEW). One labeled subject in a versioned evaluation sample.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-AGT-061 | id | TEXT | uuid | Yes | None | Workbench |
| DF-AGT-062 | agent_code | LOV | varchar(30) | Yes | LOV-AGENT | Workbench |
| DF-AGT-063 | sample_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-AGT-064 | sample_version | NUMBER | integer | Yes | None | Workbench |
| DF-AGT-065 | subject_type | LOV | varchar(15) | Yes | LOV-SUBJECT-TYPE | Workbench |
| DF-AGT-066 | subject_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-AGT-067 | label_key | TEXT | varchar(60) | Yes | None | Workbench |
| DF-AGT-068 | expected_value | TEXT | varchar(1000) | No | None | Workbench |
| DF-AGT-069 | labeled_by | USER_REF | uuid | Yes | None | Workbench |

**agent_evaluation_run** (NEW). One evaluation of an agent version against a sample.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-AGT-070 | id | TEXT | uuid | Yes | None | Workbench |
| DF-AGT-071 | agent_code | LOV | varchar(30) | Yes | LOV-AGENT | Workbench |
| DF-AGT-072 | sample_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-AGT-073 | sample_version | NUMBER | integer | Yes | None | Workbench |
| DF-AGT-074 | policy_version | TEXT | varchar(20) | No | None | Workbench |
| DF-AGT-075 | prompt_version | TEXT | varchar(20) | No | None | Workbench |
| DF-AGT-076 | model_version | TEXT | varchar(40) | No | None | Workbench |
| DF-AGT-077 | status | LOV | varchar(12) | Yes | LOV-EVAL-STATUS | Workbench |
| DF-AGT-078 | started_at | DATE | timestamptz | Yes | None | Workbench |
| DF-AGT-079 | finished_at | DATE | timestamptz | No | None | Workbench |
| DF-AGT-080 | requested_by | USER_REF | uuid | Yes | None | Workbench |
| DF-AGT-081 | total_cost_thb | NUMBER | numeric(12,4) | No | None | Workbench |
| DF-AGT-082 | p95_latency_ms | NUMBER | integer | No | None | Workbench |
| DF-AGT-083 | failure_counts | TEXT | jsonb | No | None | Workbench |
| DF-AGT-084 | proposal | TEXT | jsonb | No | None | Workbench |
| DF-AGT-085 | review_count | NUMBER | integer | No | None | Workbench |

**agent_evaluation** (NEW). The score of one approach on one label key in an evaluation run.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-AGT-086 | id | TEXT | uuid | Yes | None | Workbench |
| DF-AGT-087 | evaluation_run_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-AGT-088 | approach | LOV | varchar(20) | Yes | LOV-EXTRACT-APPROACH | Workbench |
| DF-AGT-089 | label_key | TEXT | varchar(60) | Yes | None | Workbench |
| DF-AGT-090 | sample_size | NUMBER | integer | Yes | None | Workbench |
| DF-AGT-091 | true_positive | NUMBER | integer | No | None | Workbench |
| DF-AGT-092 | false_positive | NUMBER | integer | No | None | Workbench |
| DF-AGT-093 | false_negative | NUMBER | integer | No | None | Workbench |
| DF-AGT-094 | agreement_rate | NUMBER | numeric(5,4) | No | None | Workbench |
| DF-AGT-095 | precision_value | FORMULA | numeric(5,4) | No | None | Workbench |
| DF-AGT-096 | recall_value | FORMULA | numeric(5,4) | No | None | Workbench |

**agent_feedback** (NEW). A person's verdict on an agent answer.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-AGT-097 | id | TEXT | uuid | Yes | None | Workbench |
| DF-AGT-098 | agent_run_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-AGT-099 | item_key | TEXT | varchar(20) | Yes | None | Workbench |
| DF-AGT-100 | verdict | LOV | varchar(10) | Yes | LOV-FEEDBACK | Workbench |
| DF-AGT-101 | reason | TEXT | varchar(1000) | No | None | Workbench |
| DF-AGT-102 | decision_log_id | CROSS_REF | uuid | No | None | Workbench |

**agent_alert** (NEW). A cost cap or drift alert raised for an agent.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-AGT-103 | id | TEXT | uuid | Yes | None | Workbench |
| DF-AGT-104 | agent_code | LOV | varchar(30) | Yes | LOV-AGENT | Workbench |
| DF-AGT-105 | alert_type | LOV | varchar(12) | Yes | LOV-AGENT-ALERT | Workbench |
| DF-AGT-106 | segment | TEXT | varchar(30) | Yes | None | Workbench |
| DF-AGT-107 | business_date | DATE | date | Yes | None | Workbench |
| DF-AGT-108 | measured_value | NUMBER | numeric(14,4) | Yes | None | Workbench |
| DF-AGT-109 | threshold_value | NUMBER | numeric(14,4) | Yes | None | Workbench |
| DF-AGT-110 | sent_to_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-AGT-111 | sent_at | DATE | timestamptz | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-AGENT | INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| LOV-AGENT-ALERT | COST_CAP, DRIFT |
| LOV-AGENT-RUN | ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, TOOL_UNAVAILABLE, MODEL_ERROR, DISABLED |
| LOV-AUTONOMY | OFF, SHADOW, L1 |
| LOV-CONFIG-STATUS | LOADED, APPROVED, RETIRED |
| LOV-EVAL-STATUS | RUNNING, DONE, FAILED |
| LOV-EXTRACT-APPROACH | AGENT, OCR_TEMPLATE, MODEL, OCR_AND_MODEL |
| LOV-FEEDBACK | ACCEPTED, CORRECTED, REJECTED |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |
| LOV-SUBJECT-TYPE | CASE, DOCUMENT, LEGAL_ACTION |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| agent_policy | evaluation_run_id | agent_evaluation_run | Many to 0 or 1 |
| agent_run | case_id | recovery_case | Many to 0 or 1 |
| agent_run | evaluation_run_id | agent_evaluation_run | Many to 0 or 1 |
| agent_run | decision_log_id | decision_log_entry | Many to 0 or 1 |
| agent_evaluation | evaluation_run_id | agent_evaluation_run | Many to 1 |
| agent_feedback | agent_run_id | agent_run | Many to 1 |
| agent_feedback | decision_log_id | decision_log_entry | Many to 0 or 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-23 | Enterprise AI model endpoint | Both | Private endpoint in the SCB tenant | Per request |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/agent/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | GET | `/admin/agent-runs` | `getAdminAgentRuns` |
| 2 | GET | `/admin/agent-configs` | `getAdminAgentConfigs` |
| 3 | POST | `/admin/agent-configs` | `postAdminAgentConfigs` |
| 4 | POST | `/admin/agent-configs/{versionId}/approve` | `postAdminAgentConfigsVersionidApprove` |
| 5 | POST | `/admin/agent-samples` | `postAdminAgentSamples` |
| 6 | GET | `/admin/agent-evaluations` | `getAdminAgentEvaluations` |
| 7 | POST | `/admin/agent-evaluations` | `postAdminAgentEvaluations` |
| 8 | GET | `/admin/agent-evaluations/{evaluationId}/report` | `getAdminAgentEvaluationsEvaluationidReport` |
| 9 | GET | `/admin/agent-metrics` | `getAdminAgentMetrics` |
| 10 | GET | `/cases/{caseId}/agent-outputs` | `getCasesCaseidAgentOutputs` |
| 11 | POST | `/agent-runs/{runId}/feedback` | `postAgentRunsRunidFeedback` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| AgentRunWorkflow (60 s, then the rule result) | Temporal workflow | P5 rwb-document, S1 rwb-valuation, S8 rwb-deviation | Runs on rwb-agent |
| tool gateway: read-only calls for the agent | Temporal activity | P10 rwb-agent | The only path from the agent to a service |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| AgentRunCompleted | EV-28 | `rwb.agent.events.v1` | rwb-decision, rwb-document, rwb-deviation |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Tool: read case facts (read-only) | REST | P1 rwb-source-data | C | 2 s timeout, breaker; built against the fake (ADR-020) |
| Tool: read extracted document fields (read-only) | REST | P5 rwb-document | C | 2 s timeout, breaker; built against the fake (ADR-020) |
| Enterprise AI endpoint over a private HTTPS endpoint | REST | Enterprise AI platform | X | Tracked only; outside the Workbench; class X |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| DocumentStored (intake) | EV-16 | `rwb.document.events.v1` | P5 rwb-document | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| CaseCreated (screening) | EV-01 | `rwb.case.events.v1` | P3 rwb-case | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 11 | 3 | OpenAPI 3.1, one file per service |
| Kafka (events) | 1 | 2 | AsyncAPI 3.0, one file per service |
| Temporal | 2 | 0 | Workflow and activity interfaces, queue `rwb-agent` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-agent.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| AgentRunCompleted | EV-28 | Published | `rwb.agent.events.v1` |
| DocumentStored (intake) | EV-16 | Consumed | `rwb.document.events.v1` |
| CaseCreated (screening) | EV-01 | Consumed | `rwb.case.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Platform administration |
|---|---|
| RW-COE Center of excellence analyst | R |
| RW-DATASTEW Data steward and data product owner | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | CRUD |
| RW-SECADM Security administrator | CRUDA |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents.

Every operation of T5.2.1 is authorised through the `rwb-access` authorise contract with the role, the scope and the delegation limit of T6.1 (DP-08; C RWB-P4-E1037-CON); the caller caches the answer and refreshes it on AccessPolicyChanged and DoaLimitChanged.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-008 | A screen responds within its target under normal load. | Under 2 seconds | Proposed |
| NFR-009 | The case record view loads for a case with 50 documents. | Under 2 seconds | Proposed |
| NFR-010 | An agent returns an answer within its target, after which the rule result is used and the case still routes. | Under 60 seconds | Proposed |
| NFR-011 | A rule evaluation at a routing decision completes inside the user's wait. | Under 300 milliseconds per rule evaluation at the 95th percentile | Proposed, DL11 |
| NFR-012 | A search across cases and documents returns within its target. | Under 3 seconds for a search across cases; under 5 seconds across documents | Proposed, DL11 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P10-001 | GET | /api/recovery/agent/v1/admin/agent-runs | Platform administration R | E1 |
| API-P10-002 | GET | /api/recovery/agent/v1/admin/agent-configs | Rules and parameters R | E1 |
| API-P10-003 | POST | /api/recovery/agent/v1/admin/agent-configs | Rules and parameters C | E1 |
| API-P10-004 | POST | /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve | Rules and parameters A | E1 |
| API-P10-005 | POST | /api/recovery/agent/v1/admin/agent-samples | Rules and parameters C | E1 |
| API-P10-006 | POST | /api/recovery/agent/v1/admin/agent-evaluations | Rules and parameters C | E1 |
| API-P10-007 | GET | /api/recovery/agent/v1/admin/agent-evaluations | Rules and parameters R | E1 |
| API-P10-008 | GET | /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report | Rules and parameters R | E1 |
| API-P10-009 | GET | /api/recovery/agent/v1/admin/agent-metrics | Rules and parameters R | E2 |
| API-P10-010 | GET | /api/recovery/agent/v1/cases/{caseId}/agent-outputs | Case record R | E3 |
| API-P10-011 | POST | /api/recovery/agent/v1/agent-runs/{runId}/feedback | Case record U | E3 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-P10-001 GET /admin/agent-runs

| Item | Value |
|---|---|
| Purpose | List agent runs with fallbacks and evaluation results |
| Request | Query: agent, from, to |
| Response | AgentRun[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P10-002 GET /admin/agent-configs

| Item | Value |
|---|---|
| Purpose | List prompt and policy versions per agent with status and dates |
| Request | Query: agent, kind, status |
| Response | AgentConfigVersion[] |
| Errors | 401, 403, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P10-003 POST /admin/agent-configs

| Item | Value |
|---|---|
| Purpose | Load a new prompt or policy version for an agent from a checked file |
| Request | Multipart: file, kind, agent, validFrom |
| Response | AgentConfigVersion |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Rules and parameters, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P10-004 POST /admin/agent-configs/{versionId}/approve

| Item | Value |
|---|---|
| Purpose | Approve a loaded prompt or policy version |
| Request | None |
| Response | AgentConfigVersion |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Rules and parameters, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P10-005 POST /admin/agent-samples

| Item | Value |
|---|---|
| Purpose | Load a labeled evaluation sample for an agent |
| Request | Multipart: file, agent, sampleCode |
| Response | AgentSample |
| Errors | 401, 403, 422, 503 |
| Authorization | Rules and parameters, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P10-006 POST /admin/agent-evaluations

| Item | Value |
|---|---|
| Purpose | Start the evaluation harness for an agent on a labeled sample |
| Request | AgentEvaluationRequest |
| Response | AgentEvaluationRun |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Rules and parameters, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P10-007 GET /admin/agent-evaluations

| Item | Value |
|---|---|
| Purpose | List evaluation runs with their scores and proposals, as JSON or CSV |
| Request | Query: agent, from, to |
| Response | AgentEvaluationRun[] |
| Errors | 401, 403, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P10-008 GET /admin/agent-evaluations/{evaluationId}/report

| Item | Value |
|---|---|
| Purpose | Read the report of one evaluation run: sample size, agreement, failures, cost and latency |
| Request | None |
| Response | AgentEvaluationReport |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P10-009 GET /admin/agent-metrics

| Item | Value |
|---|---|
| Purpose | Read agent measures per agent, version, segment and day for the agent monitor |
| Request | Query: agent, segment, version, from, to |
| Response | AgentMetric[] |
| Errors | 401, 403, 422, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P10-010 GET /cases/{caseId}/agent-outputs

| Item | Value |
|---|---|
| Purpose | Read the L1 agent outputs for a case: intake summary and proposed deviations |
| Request | None |
| Response | AgentOutput[] |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P10-011 POST /agent-runs/{runId}/feedback

| Item | Value |
|---|---|
| Purpose | Record a person's verdict on an item of an L1 agent output |
| Request | AgentFeedbackRequest |
| Response | AgentOutput |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Case record, right U, scope applied |
| Idempotency | Idempotency-Key header |

## Appendix T-B. Open technical decisions

| Decision | What is needed |
|---|---|
| DL06 | Which interfaces need same-day data |
| DL11 | Non-functional target values |
| DL35 | Deployment slots |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Solution architect | | | |
| Tech lead | | | |
| ACE team | | | |
| QA lead | | | |
