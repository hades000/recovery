<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 058 Agent platform set up E1a v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 058 Agent platform set up E1a v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-058 Agent platform set-up [E1a]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-058 |
| Epic | E1, release 30 November 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-01 Set up the agent platform with the gateway and prompt store; FEAT-AGT-02 Run the guardrail checker on every agent output; FEAT-AGT-05 Run the agent evaluation harness; FEAT-AGT-11 Fall back to the rule result when an agent is unavailable |
| Requirement IDs | REQ-ACA-010, REQ-ACA-005, REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, sections 5.4 and 5.7 |
| L3 process | All recovery processes; 15 Manage performance, data and AI |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-003, RWB-E1-037 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the model gateway, the prompt and policy store, the guardrail checker and the evaluation harness deployed in the recovery module**, so that **every Workbench agent is built, called, checked and scored through one path with its versions recorded**.

## 2. Business rationale

Officers gather and check case facts by hand before every decision, and no agent can help until there is one controlled way to call a model. This story gives every later agent the same gateway, the same versioned prompts and policies, the same output checks and the same scoring, so that an agent runs under a service identity (REQ-ACA-010), sees only masked personal data (REQ-ACA-005) and reads every threshold from a versioned row (REQ-DRI-010). The measure is the agent fallback rate, target below 10 percent per month, read from the agent run table.

## 3. Preconditions

- RWB-E1-001 (recovery tables) and RWB-E1-003 (account and arrears load) are done, so synthetic cases exist in DEV and SIT.
- RWB-E1-037 is done: the P4 masking service masks personal fields by role, including for SY-AGENT.
- The service identity SY-AGENT exists with the Entra ID managed identity RWB-DEV-SY-AGENT (and the SIT, UAT and PROD equivalents) and the permissions seeded in Recovery Workbench Physical Schema v4.sql (Case record R, Documents R, Rules and parameters R, Reference data R, Decision log C).
- The model endpoint INT-23 is reachable on a private endpoint in the SCB tenant. Assumed option B of DL33: the endpoint ACE uses through AAL.
- A person holding RW-COE loads prompts, policies and labeled samples; a person holding RW-RISK approves them.

## 4. Flow

1. RW-COE: loads a prompt file and a policy file for agent "INTAKE" through POST /admin/agent-configs.
2. System: validates each file, stores it as a new version with status "LOADED" and keeps every earlier version readable.
3. RW-RISK: approves the version through POST /admin/agent-configs/{versionId}/approve; the version takes effect on its valid from date.
4. Calling step (any module, through RWB-TE-013): asks the orchestrator to run agent "INTAKE" for one case with an idempotency key.
5. System: reads the approved policy and prompt in force, reads the inputs through the tool gateway, masks personal fields through the P4 masking service and calls the model endpoint with the policy timeout.
6. System: runs the guardrail checker on the answer: output schema, allowed tool list and confidence floor.
7. System: writes one agent run row with the agent, policy, prompt and model versions, status, latency, tokens and cost, and publishes AgentRunCompleted.
8. System: returns the checked answer, or a fallback result with its reason, to the calling step.
9. RW-COE: loads a labeled sample through POST /admin/agent-samples and starts the evaluation harness through POST /admin/agent-evaluations.
10. System: runs the agent on every sample row in shadow, scores it against the labels and stores the scores with the policy, prompt and model versions.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The model endpoint does not answer within the policy timeout of 60 seconds | Run status TIMED_OUT, fallback true; the caller uses the rule result (R-UNI-32) | None to a user | AC6 |
| X2 | The answer fails its output schema | Run status GUARDRAIL_FAILED, failure counted by check code; fallback true | None to a user | AC3 |
| X3 | The agent asks for a tool that is not on its allowed list | The tool call is refused and logged; run status GUARDRAIL_FAILED; fallback true | None to a user | AC5 |
| X4 | The answer confidence is below the policy confidence floor | Run status BELOW_FLOOR; fallback true | None to a user | AC10 |
| X5 | A prompt or policy file fails a load check | The load is refused in full; the version in force is unchanged | MSG-P10-001 | AC8 |
| X6 | The person who loaded a version tries to approve it | Approval refused; version stays LOADED | MSG-P7-002 | AC9 |
| X7 | Two approvals of the same version arrive at once | The first approves; the second is refused with 409 | MSG-GEN-004 | AC12 |
| X8 | The same run request arrives twice with the same idempotency key | One run row; the repeat returns the first result and is counted (R-UNI-40) | None to a user | AC11 |
| X9 | An evaluation is started on a sample with no labeled rows for the agent | Refused with 422; no run starts | MSG-P10-002 | AC13 |
| X10 | An evaluation is started while one for the same agent and sample is running | Refused with 409 | MSG-P10-003 | AC14 |
| X11 | A role without the right calls an endpoint | Refused with 403; nothing changes | MSG-P4-002 | TC-E1-058-16 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the recovery tables (RWB-E1-001, RWB-E1-003) and the masking service (RWB-E1-037); no agent story is needed to test it, because a test agent "ECHO" with a fixed prompt proves every path |
| Negotiable | The model, prompts, thresholds, timeout, tool lists and prices are data rows; the story fixes the behavior only |
| Valuable | Every later agent (RWB-E1-059 to RWB-E2-032) is built on it, and every model call carries its versions from the first call |
| Estimable | Six new tables, four components (gateway client, orchestrator, guardrail checker, evaluation harness), six endpoints, no screen |
| Small | Fits in two weeks for two developers with its tests |
| Testable | Each criterion below is one automated test against a stubbed model endpoint in DEV |

## 7. Acceptance criteria

```gherkin
Feature: Agent platform set-up [E1a]

  Background:
    Given the test agent "ECHO" has policy version "P1" approved with model "MODEL-A-2026-10", timeout 60 seconds, confidence floor 0.80 and allowed tools "read_case"
    Given prompt version "PR1" is approved for agent "ECHO"
    Given the model endpoint stub answers in 1,200 milliseconds with 900 input tokens and 150 output tokens
    Given the policy price is 0.0500 baht per 1,000 tokens

  Scenario: AC1 Approved endpoint
    Given the approved model endpoint on the private endpoint of the SCB tenant
    When the orchestrator runs agent "ECHO" for case "RW-2026-000101"
    Then the call succeeds with run status "ANSWERED"
    Then one agent run row holds agent "ECHO", policy version "P1", prompt version "PR1", model version "MODEL-A-2026-10", latency 1,200 ms, tokens in 900, tokens out 150 and cost 0.0525 baht
    Then the system writes one AgentRunCompleted event to the outbox with the run ID, agent "ECHO", the case ID, outcome "ANSWERED" and fallback false

  Scenario: AC2 Prompt versions
    Given prompt version "PR1" is in force for agent "ECHO"
    When RW-COE loads prompt version "PR2" and RW-RISK approves it with valid from 2026-11-20
    Then prompt version "PR2" exists with status "APPROVED"
    Then prompt version "PR1" stays readable through GET /admin/agent-configs with its text hash unchanged
    Then a run on 2026-11-19 uses "PR1" and a run on 2026-11-20 uses "PR2"

  Scenario: AC3 Schema check
    Given the model stub returns an answer with field "summary" missing from the output schema of "ECHO"
    When the guardrail runs
    Then the system rejects the output with run status "GUARDRAIL_FAILED" and fallback true
    Then the guardrail result holds check code "SCHEMA" with the missing field name
    Then the count of check code "SCHEMA" failures for "ECHO" on the business date rises by 1

  Scenario: AC4 Evaluation suite
    Given labeled sample "ECHO-S1" version 1 with 20 rows for agent "ECHO"
    When RW-COE starts the evaluation of "ECHO" on "ECHO-S1"
    Then one evaluation run ends with status "DONE" and 20 agent run rows with trigger "EVALUATION" and mode "SHADOW"
    Then one score row per label key holds sample size, true positives, false positives, false negatives, precision and recall
    Then each score row holds policy version "P1", prompt version "PR1" and model version "MODEL-A-2026-10"

  Scenario: AC5 Guardrails
    Given an agent with the allowed tool list "read_case"
    When it calls the tool "propose_deviation", which is not on its list
    Then the system refuses the tool call and not executed
    Then the agent run holds status "GUARDRAIL_FAILED", check code "TOOL_NOT_ALLOWED" and fallback true
    Then the orchestrator returns a fallback result with reason "TOOL_NOT_ALLOWED" so the calling step takes the rule path

  Scenario: AC6 The model does not answer inside the timeout
    Given the model stub does not answer for 61 seconds
    When the orchestrator runs agent "ECHO" for case "RW-2026-000102"
    Then the system ends the call at 60 seconds
    Then the agent run holds status "TIMED_OUT", fallback true and latency 60,000 ms
    Then the orchestrator returns a fallback result with reason "TIMED_OUT" (R-UNI-32)

  Scenario: AC7 Personal data is masked before the model call
    Given case "RW-2026-000103" has a borrower with a synthetic national ID number and a synthetic mobile number
    When the orchestrator builds the request to the model endpoint
    Then the request body holds the masking tokens returned by the P4 masking service for SY-AGENT
    Then the request body, the agent run row and the application log hold no national ID number, phone number, name or account number

  Scenario: AC8 A configuration file that fails a check is refused
    Given a policy file for agent "ECHO" with timeout_seconds 0
    When RW-COE loads it through POST /admin/agent-configs
    Then the system refuses the load with 422 and MSG-P10-001 naming check "timeout_seconds between 1 and 120"
    Then policy version "P1" stays in force and no new version row exists

  Scenario: AC9 The loader cannot approve their own version
    Given user "coe.user01" loaded policy version "P2" for agent "ECHO"
    When user "coe.user01" calls POST /admin/agent-configs/{versionId}/approve for "P2"
    Then the system refuses the approval with 409 and MSG-P7-002
    Then version "P2" keeps status "LOADED"

  Scenario: AC10 An answer below the confidence floor falls back
    Given the model stub returns a valid answer with confidence 0.79
    When the guardrail runs with confidence floor 0.80
    Then the agent run holds status "BELOW_FLOOR" and fallback true
    Then the orchestrator returns a fallback result with reason "BELOW_FLOOR"

  Scenario: AC11 A repeated run request has no further effect
    Given agent "ECHO" ran for case "RW-2026-000101" with idempotency key "ECHO:RW-2026-000101:2026-11-30"
    When the same request arrives again with the same key
    Then no second agent run row and no second model call exist
    Then the system returns the first result and the idempotency hit is counted (R-UNI-40)

  Scenario: AC12 Two approvals of one version at the same time
    Given policy version "P2" for agent "ECHO" has status "LOADED" and row version 1
    When two RW-RISK users approve "P2" at the same time
    Then one approval succeeds and "P2" has status "APPROVED"
    Then the system refuses the other with 409 and MSG-GEN-004

  Scenario: AC13 An evaluation on an empty sample is refused
    Given sample "ECHO-S2" has 0 labeled rows for agent "ECHO"
    When RW-COE starts the evaluation of "ECHO" on "ECHO-S2"
    Then the system refuses the request with 422 and MSG-P10-002
    Then no evaluation run and no agent run row exist

  Scenario: AC14 A second evaluation while one is running is refused
    Given the evaluation of "ECHO" on "ECHO-S1" version 1 has status "RUNNING"
    When RW-COE starts the same evaluation again
    Then the system refuses the request with 409 and MSG-P10-003
    Then one evaluation run exists for "ECHO" on "ECHO-S1" version 1 with status "RUNNING"

  Scenario: AC15 Agent runs are listed without their content
    Given 3 runs of agent "ECHO" between 2026-11-30 and 2026-12-01
    When RW-PLATADM calls GET /admin/agent-runs with agent "ECHO", from "2026-11-30" and to "2026-12-01"
    Then 3 AgentRun items return with id, agent, agentVersion, caseId, outcome, fallback and latencyMs
    Then no item holds the prompt text, the model answer or a personal field
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every model call goes through the model gateway client to the endpoint chosen under DL33; no other component calls the endpoint | DL33; integration INT-23 |
| BR2 | The orchestrator uses the policy and prompt versions in force on the run date with status APPROVED; open runs keep the version they started with | agent_policy.valid_from (New); R-UNI-38 |
| BR3 | If the endpoint does not answer within agent_policy.timeout_seconds (60, assumed; DL11), the run ends TIMED_OUT and the rule result is used | R-UNI-32; NFR-010 |
| BR4 | Every answer is checked in this order: output schema, allowed tool list, confidence floor; the first failed check sets the status and fallback is true | agent_policy.output_schema_ref, allowed_tools, confidence_floor (New) |
| BR5 | Personal fields are masked through the P4 masking service before any value reaches a prompt | CTL-11; REQ-ACA-005 |
| BR6 | The agent runs as SY-AGENT and passes the same permission check as a person on every tool call | REQ-ACA-010; role SY-AGENT |
| BR7 | Cost of a run = (tokens in + tokens out) / 1,000 x agent_policy.price_per_1k_tokens_thb, rounded to 4 decimals | agent_policy.price_per_1k_tokens_thb (New); price assumed 0.0500 baht, DL33 |
| BR8 | A prompt or policy version is loaded by RW-COE and approved by RW-RISK; the same person may not do both | CTL-08; separation of duty, center of excellence analyst and risk and model risk officer |
| BR9 | A run request with an idempotency key already used returns the first result | R-UNI-40 |
| BR10 | A file load is refused in full if any row fails a check | Principle 1; CTL-08 |
| BR11 | No business value (model name, threshold, timeout, price, tool list) is written in code | Principle 1; DT02 |

## 9. State transitions

None. This story does not change a case status. It changes the status of an agent configuration version and of an agent run:

| From | Event | Condition | To |
|---|---|---|---|
| None | Configuration file loaded | Every check passes | LOADED (agent_policy.status or agent_prompt.status) |
| None | Configuration file loaded | A check fails | No row; load refused |
| LOADED | Approved by RW-RISK | Approver is not the loader | APPROVED |
| APPROVED | A later version is approved | Later valid from date reached | RETIRED (valid_to set to the day before) |
| None | Run requested | Answer passes every check | ANSWERED (agent_run.status) |
| None | Run requested | Timeout, check failure or floor | TIMED_OUT, GUARDRAIL_FAILED or BELOW_FLOOR, fallback true |
| None | Evaluation started | Sample has rows; none running | RUNNING (agent_evaluation_run.status) |
| RUNNING | Last sample row scored | None | DONE |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads prompt, policy and sample files; starts evaluations; reads versions and scores (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves prompt and policy versions (Rules and parameters A); reads scores |
| RW-PLATADM, platform administrator | Reads agent runs (Platform administration CRUD; R used here); runs the gateway configuration per environment |
| RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs (Platform administration R) |
| SY-AGENT, agent platform | Runs agents; reads case, documents and reference data through the tool gateway (R) |
| Approval levels | No delegation of authority level applies; the approval is the Rules and parameters A right |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read (through the P3 interface) |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-REF-012 | rule_row | valid_from | Read (version-in-force pattern only; no rule row is written) |
| DF-AGT-001 | agent_policy | id | Write |
| DF-AGT-002 | agent_policy | agent_code | Write |
| DF-AGT-003 | agent_policy | policy_version | Write |
| DF-AGT-004 | agent_policy | model_code | Write |
| DF-AGT-005 | agent_policy | model_version | Write |
| DF-AGT-006 | agent_policy | output_schema_ref | Write |
| DF-AGT-007 | agent_policy | allowed_tools | Write |
| DF-AGT-008 | agent_policy | autonomy_mode | Write |
| DF-AGT-009 | agent_policy | segment_product_group | Write |
| DF-AGT-010 | agent_policy | segment_region_code | Write |
| DF-AGT-011 | agent_policy | confidence_floor | Write |
| DF-AGT-012 | agent_policy | timeout_seconds | Write |
| DF-AGT-013 | agent_policy | daily_cost_cap_thb | Write |
| DF-AGT-014 | agent_policy | price_per_1k_tokens_thb | Write |
| DF-AGT-015 | agent_policy | alert_role | Write |
| DF-AGT-016 | agent_policy | review_date | Write |
| DF-AGT-021 | agent_policy | status | Write |
| DF-AGT-022 | agent_policy | valid_from | Write |
| DF-AGT-023 | agent_policy | valid_to | Write |
| DF-AGT-024 | agent_policy | loaded_by | Write |
| DF-AGT-025 | agent_policy | approved_by | Write |
| DF-AGT-026 | agent_prompt | id | Write |
| DF-AGT-027 | agent_prompt | agent_code | Write |
| DF-AGT-028 | agent_prompt | prompt_version | Write |
| DF-AGT-029 | agent_prompt | body_text | Write |
| DF-AGT-030 | agent_prompt | body_hash | Write |
| DF-AGT-031 | agent_prompt | status | Write |
| DF-AGT-032 | agent_prompt | valid_from | Write |
| DF-AGT-033 | agent_prompt | valid_to | Write |
| DF-AGT-034 | agent_prompt | loaded_by | Write |
| DF-AGT-035 | agent_prompt | approved_by | Write |
| DF-AGT-036 | agent_run | id | Write |
| DF-AGT-037 | agent_run | agent_code | Write |
| DF-AGT-038 | agent_run | agent_version | Write |
| DF-AGT-039 | agent_run | prompt_version | Write |
| DF-AGT-040 | agent_run | model_version | Write |
| DF-AGT-041 | agent_run | case_id | Write |
| DF-AGT-042 | agent_run | subject_id | Write |
| DF-AGT-043 | agent_run | autonomy_mode | Write |
| DF-AGT-044 | agent_run | trigger_event | Write |
| DF-AGT-045 | agent_run | idempotency_key | Write |
| DF-AGT-046 | agent_run | status | Write |
| DF-AGT-047 | agent_run | fallback | Write |
| DF-AGT-048 | agent_run | guardrail_result | Write |
| DF-AGT-049 | agent_run | output | Write |
| DF-AGT-050 | agent_run | confidence | Write |
| DF-AGT-051 | agent_run | latency_ms | Write |
| DF-AGT-052 | agent_run | tokens_in | Write |
| DF-AGT-053 | agent_run | tokens_out | Write |
| DF-AGT-054 | agent_run | cost_thb | Write |
| DF-AGT-055 | agent_run | data_as_of | Write |
| DF-AGT-056 | agent_run | run_at | Write |
| DF-AGT-057 | agent_run | evaluation_run_id | Write |
| DF-AGT-061 | agent_sample | id | Write |
| DF-AGT-062 | agent_sample | agent_code | Write |
| DF-AGT-063 | agent_sample | sample_code | Write |
| DF-AGT-064 | agent_sample | sample_version | Write |
| DF-AGT-065 | agent_sample | subject_type | Write |
| DF-AGT-066 | agent_sample | subject_id | Write |
| DF-AGT-067 | agent_sample | label_key | Write |
| DF-AGT-068 | agent_sample | expected_value | Write |
| DF-AGT-069 | agent_sample | labeled_by | Write |
| DF-AGT-070 | agent_evaluation_run | id | Write |
| DF-AGT-071 | agent_evaluation_run | agent_code | Write |
| DF-AGT-072 | agent_evaluation_run | sample_code | Write |
| DF-AGT-073 | agent_evaluation_run | sample_version | Write |
| DF-AGT-074 | agent_evaluation_run | policy_version | Write |
| DF-AGT-075 | agent_evaluation_run | prompt_version | Write |
| DF-AGT-076 | agent_evaluation_run | model_version | Write |
| DF-AGT-077 | agent_evaluation_run | status | Write |
| DF-AGT-078 | agent_evaluation_run | started_at | Write |
| DF-AGT-079 | agent_evaluation_run | finished_at | Write |
| DF-AGT-080 | agent_evaluation_run | requested_by | Write |
| DF-AGT-081 | agent_evaluation_run | total_cost_thb | Write |
| DF-AGT-082 | agent_evaluation_run | p95_latency_ms | Write |
| DF-AGT-083 | agent_evaluation_run | failure_counts | Write |
| DF-AGT-086 | agent_evaluation | id | Write |
| DF-AGT-087 | agent_evaluation | evaluation_run_id | Write |
| DF-AGT-088 | agent_evaluation | approach | Write |
| DF-AGT-089 | agent_evaluation | label_key | Write |
| DF-AGT-090 | agent_evaluation | sample_size | Write |
| DF-AGT-091 | agent_evaluation | true_positive | Write |
| DF-AGT-092 | agent_evaluation | false_positive | Write |
| DF-AGT-093 | agent_evaluation | false_negative | Write |
| DF-AGT-094 | agent_evaluation | agreement_rate | Write |
| DF-AGT-095 | agent_evaluation | precision_value | Write |
| DF-AGT-096 | agent_evaluation | recall_value | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/admin/agent-runs** (API-P10-001, in api.yaml)
- Request: query agent, from, to (dates, ISO 8601).
- Response: 200, array of AgentRun (id, agent, agentVersion, caseId, outcome, fallback, latencyMs). outcome carries agent_run.status. agentVersion is "<agent>@<policy_version>/<prompt_version>", for example "ECHO@P1/PR1".
- Errors: 401 no session (MSG-P4-001); 403 role without Platform administration R (MSG-P4-002); 503 store unavailable.
- Authorization: Platform administration, R, scope applied.
- Idempotency: not applicable (read).

**GET /api/recovery/v1/admin/agent-configs** (new, see additions)
- Request: query agent, kind (PROMPT or POLICY), status.
- Response: 200, array of AgentConfigVersion (versionId, agent, kind, version, status, validFrom, validTo, loadedBy, approvedBy, bodyHash).
- Errors: 401, 403, 503. Authorization: Rules and parameters, R.

**POST /api/recovery/v1/admin/agent-configs** (new)
- Request: multipart/form-data: file (JSON), kind (PROMPT or POLICY), agent, validFrom.
- Response: 201 AgentConfigVersion with status LOADED.
- Errors: 401; 403; 409 version number already exists for the agent and kind; 422 a check fails (MSG-P10-001 with the check text); 503.
- Authorization: Rules and parameters, C. Idempotency: agent, kind and version number are unique; a repeat load of the same version returns 409.

**POST /api/recovery/v1/admin/agent-configs/{versionId}/approve** (new)
- Request: path versionId (uuid); header If-Match with the row version.
- Response: 200 AgentConfigVersion with status APPROVED.
- Errors: 401; 403; 404 unknown version; 409 approver is the loader (MSG-P7-002), version not LOADED, or row changed (MSG-GEN-004); 503.
- Authorization: Rules and parameters, A. Idempotency: a second approval of an APPROVED version returns 409.

**POST /api/recovery/v1/admin/agent-samples** (new)
- Request: multipart/form-data: file (CSV: subject_type, subject_id, label_key, expected_value), agent, sampleCode.
- Response: 201 AgentSample (sampleCode, sampleVersion, rows).
- Errors: 401; 403; 422 a row fails a check (MSG-P10-001); 503.
- Authorization: Rules and parameters, C. Idempotency: each load creates the next sample version.

**POST /api/recovery/v1/admin/agent-evaluations** (new)
- Request: AgentEvaluationRequest (agent, sampleCode, sampleVersion, approaches; approaches default ["AGENT"]).
- Response: 202 AgentEvaluationRun with status RUNNING.
- Errors: 401; 403; 409 the same evaluation is running (MSG-P10-003); 422 sample empty (MSG-P10-002); 503.
- Authorization: Rules and parameters, C. Idempotency: one RUNNING run per agent, sample and sample version.

**GET /api/recovery/v1/admin/agent-evaluations** (new)
- Request: query agent, from, to. Response: 200, array of AgentEvaluationRun with its AgentEvaluation score rows.
- Errors: 401, 403, 503. Authorization: Rules and parameters, R.

**Published interface inside P10** (used by RWB-TE-013, not by other modules directly):

```java
package recovery.agent.orchestrator;
public interface AgentOrchestrator {
    AgentRunResult run(AgentRunRequest request); // agentCode, caseId, subjectId, triggerEvent, idempotencyKey, inputs
}
// AgentRunResult: runId, status, fallback, fallbackReason, output (JsonNode), confidence, agentVersion, modelVersion
```

**Event published:** EV-28 AgentRunCompleted (runId, agent, caseId, outcome, fallback), written to the outbox in the same transaction as the agent run row.

**External call:** INT-23 model endpoint, OpenAPI 3.1, per request; request holds the prompt version, masked inputs and the output schema.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/`, Java package `recovery.agent` with sub-packages `gateway`, `config`, `orchestrator`, `guardrail`, `eval`, `api`. Front end: none.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentRuntimeController | Controller | GET /admin/agent-runs; maps errors to problem responses |
| AgentConfigController | Controller | GET and POST /admin/agent-configs, POST approve |
| AgentEvaluationController | Controller | POST /admin/agent-samples, POST and GET /admin/agent-evaluations |
| ModelGatewayClient | Service | Calls INT-23 with the policy model and timeout; returns answer, tokens and latency; no retry inside a step |
| AgentConfigService | Service | Validates and stores prompt and policy versions; resolves the version in force for a date; enforces loader is not approver |
| AgentOrchestrator | Published interface | Runs one agent step: resolve config, gather inputs through tools, mask, call, check, record |
| AgentRuntimeService | Service | Implements AgentOrchestrator; writes agent_run and the outbox event in one transaction |
| ToolGateway | Service | Executes allowed tools only, as SY-AGENT, through other modules' published interfaces (P3 case read, P5 document read) |
| GuardrailChecker | Service | Schema check (JSON Schema draft 2020-12), tool allow-list check, confidence floor check; returns check codes |
| PromptInputMasker | Service | Calls the P4 masking service for every input value before the prompt is built |
| EvaluationHarness | Service | Runs the agent in shadow on each sample row, scores against labels, writes score rows |
| AgentRunRepository, AgentConfigRepository, AgentEvaluationRepository | Repository | Read and write the P10 tables only |
| AgentRun, AgentPolicy, AgentPrompt, AgentSample, AgentEvaluationRun, AgentEvaluation | Entity | JPA entities for the new tables |

**Database:** Flyway migration `V10_001__agent_runtime.sql` creates agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run and agent_evaluation in schema `recovery` with the standard record columns (is_active, state, version, created_at, created_by, updated_at, updated_by). Constraints: unique (agent_code, policy_version) on agent_policy; unique (agent_code, prompt_version) on agent_prompt; unique (idempotency_key) on agent_run; unique (agent_code, sample_code, sample_version, subject_id, label_key) on agent_sample; partial unique index on agent_evaluation_run (agent_code, sample_code, sample_version) where status = 'RUNNING'. Index agent_run (agent_code, run_at). No other module's table is read or written.

**Configuration and reference data:** agent_policy and agent_prompt rows, loaded by RW-COE and approved by RW-RISK. Test agent "ECHO" seed files in `src/test/resources/agent/`. Environment properties (not business values): `rwb.agent.gateway.base-url`, `rwb.agent.gateway.identity` (managed identity of SY-AGENT). Policy check limits (timeout 1 to 120 seconds, confidence floor 0 to 1) are held in the policy JSON schema file versioned with the policy loader.

**Build steps**
1. Write the Flyway migration and the entities; test the constraints with Testcontainers PostgreSQL.
2. Build AgentConfigService and AgentConfigController: load, check, store, approve, version in force by date (AC2, AC8, AC9, AC12).
3. Build ModelGatewayClient against a WireMock stub of INT-23, with the timeout from the policy (AC1, AC6).
4. Build PromptInputMasker over the P4 masking interface and a log filter test that fails on any personal pattern (AC7).
5. Build GuardrailChecker and ToolGateway with the allow-list (AC3, AC5, AC10).
6. Build AgentRuntimeService: orchestrate, record agent_run, outbox EV-28, idempotency (AC1, AC11).
7. Build EvaluationHarness and AgentEvaluationController (AC4, AC13, AC14).
8. Build AgentRuntimeController for GET /admin/agent-runs (AC15) and the access tests.

**Feature flag:** `rwb.agent.platform`. Off: the orchestrator returns a fallback result with reason "DISABLED" and makes no model call.

**Done when:** the tests in section 16 pass; the boundary test shows no read of another module's table; the log scan finds no personal data.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | A prompt, policy or sample file fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | Evaluation started on a sample with no labeled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Evaluation started while the same one is running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P7-002 | Loader tries to approve their own version | You prepared this decision, so you cannot approve it. |
| MSG-GEN-004 | Approval of a version that changed since it was read | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required form field is empty (agent, kind, file) | Enter {field}. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. RW-PLATADM and the other Platform administration R holders read runs through GET /admin/agent-runs; RW-COE and RW-RISK read versions and scores through the configuration and evaluation endpoints. The agent monitor screen SCR-46 comes in RWB-E2-031.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-058-01 | AC1, BR1, BR7 | System | Agent ECHO, case RW-2026-000101, stub answer 1,200 ms, 900 and 150 tokens |
| TC-E1-058-02 | AC2, BR2 | System | Prompt PR1 then PR2 valid from 2026-11-20; runs on 2026-11-19 and 2026-11-20 |
| TC-E1-058-03 | AC3, BR4 | System | Stub answer missing field "summary" |
| TC-E1-058-04 | AC4 | System | Sample ECHO-S1 version 1, 20 rows |
| TC-E1-058-05 | AC5, BR4, BR6 | System | Tool call "propose_deviation" with allow-list "read_case" |
| TC-E1-058-06 | AC6, BR3 | System | Stub silent for 61 seconds |
| TC-E1-058-07 | AC7, BR5 | System | Case RW-2026-000103 with synthetic national ID and mobile number |
| TC-E1-058-08 | AC8, BR10 | System | Policy file with timeout_seconds 0 |
| TC-E1-058-09 | AC9, BR8 | System | Loader coe.user01 approves own version P2 |
| TC-E1-058-10 | AC10, BR4 | System | Stub confidence 0.79, floor 0.80 |
| TC-E1-058-11 | AC11, BR9 | System | Key ECHO:RW-2026-000101:2026-11-30 sent twice |
| TC-E1-058-12 | AC12 | System | Two parallel approvals of P2, row version 1 |
| TC-E1-058-13 | AC13 | System | Sample ECHO-S2 with 0 rows |
| TC-E1-058-14 | AC14 | System | Evaluation of ECHO on ECHO-S1 version 1 already RUNNING |
| TC-E1-058-15 | AC15 | System | 3 runs of ECHO from 2026-11-30 to 2026-12-01 |
| TC-E1-058-16 | Access | Access | RW-CASEOWN calls GET /admin/agent-runs and POST /admin/agent-configs; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: model, prompt, timeout, confidence floor, tool list, price and cap are read from approved version rows.
- No personal data in logs, tests or prompts; test data is synthetic in DEV and masked in SIT.
- No read of another module's tables; case and document facts come through the P3 and P5 published interfaces.
- The model endpoint is reached only through ModelGatewayClient and only on the private endpoint.
- Prompt text and model answers never appear in the application log or in an API response of this story.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-010 | Agents run under service identities with the same role checks as people | Business Requirements Program, section 5.4 | FEAT-AGT-01, FEAT-AGT-02 | All recovery processes | R-UNI-32, R-UNI-40 | TC-E1-058-01, TC-E1-058-05, TC-E1-058-16 |
| REQ-ACA-005 | Personal data masked by role in every agent call | Business Requirements Program, section 5.4 | FEAT-AGT-01 | All recovery processes | None | TC-E1-058-07 |
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | Business Requirements Program, section 5.7 | FEAT-AGT-01, FEAT-AGT-05, FEAT-AGT-11 | 15 Manage performance, data and AI | R-UNI-38 | TC-E1-058-02, TC-E1-058-04, TC-E1-058-06, TC-E1-058-08, TC-E1-058-09 |

## 19. Out of scope

- The rule fallback inside a case step and the decision log entry for that step (RWB-TE-013).
- The case intake agent (RWB-E1-059), the extraction evaluation (RWB-E1-060) and the deviation screening agent (RWB-E1-062).
- The monitoring dashboard and cost alert (RWB-E1-063, RWB-E2-031).
- Changing an autonomy level through a screen (FEAT-AGT-12, Epic 3) and drift detection (FEAT-AGT-13, Epic 3).
- The choice of model endpoint (DL33).
