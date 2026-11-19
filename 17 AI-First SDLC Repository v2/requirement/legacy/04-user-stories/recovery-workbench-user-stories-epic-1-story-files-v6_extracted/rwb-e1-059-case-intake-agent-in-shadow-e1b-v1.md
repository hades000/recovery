<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 059 Case intake agent in shadow E1b v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 059 Case intake agent in shadow E1b v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-059 Case intake agent in shadow [E1b]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-059 |
| Epic | E1, release 30 November 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-03 Run the case intake agent in shadow |
| Requirement IDs | REQ-ACA-005, REQ-ACA-010 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.4 |
| L3 process | 06 Take over and own the case |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-030, RWB-E1-058, RWB-TE-013 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the case intake agent to build a case file summary and flag gaps for every new Epic 1 case in shadow mode**, so that **the agent is scored against the business analysts' review before any case owner sees its output**.

## 2. Business rationale

A case owner who takes over a case at day 90 reads every account, document and appraisal to find what is missing before deciding the next step. The intake agent prepares that summary and the list of gaps. In Epic 1 it runs in shadow only: its output is stored, compared with the business analysts' review of the same 200 cases and shown to nobody, so the step to autonomy level 1 in RWB-E2-028 is decided on a measured agreement rate. Inputs are masked before the model call (REQ-ACA-005) and the agent reads data as SY-AGENT (REQ-ACA-010).

## 3. Preconditions

- RWB-E1-058 (gateway, policy store, guardrail, evaluation harness) and RWB-TE-013 (client) are done.
- RWB-E1-030 is done, so cases are created and allocated daily and EV-01 CaseCreated is published.
- Approved agent_policy "INTAKE" version "P1" with autonomy_mode SHADOW, timeout 60 seconds, confidence floor 0.80, allowed tools read_case, read_accounts, read_documents, read_valuations, read_contact_points, and output schema "intake-summary-v1".
- Approved agent_prompt "INTAKE" version "PR1".
- The output schema lists the gap types as data: MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT, STALE_INPUT.
- Labeled sample "INTAKE-S1" version 1 is loaded by RW-COE: the business analysts' review of 200 Epic 1 cases, one row per case and gap type with expected value Y or N.

## 4. Flow

1. SY-CASEWF: creates case "RW-2026-000301" and writes EV-01 CaseCreated to the outbox.
2. System (IntakeShadowListener): receives the event and calls the orchestrator for agent "INTAKE" with key "INTAKE:<caseId>:<businessDate>".
3. System: reads the case, accounts, documents, valuations and contact points through the tool gateway as SY-AGENT, masks personal fields and calls the model.
4. System: checks the answer (schema, tools, floor) and stores the summary and gap flags on the agent run with mode SHADOW.
5. System: publishes EV-28 AgentRunCompleted; no screen and no case field changes.
6. RW-COE: starts the evaluation of "INTAKE" on sample "INTAKE-S1" through POST /admin/agent-evaluations.
7. System: runs the agent in shadow on each of the 200 sample cases and compares each gap flag with the label.
8. System: stores one score row per gap type with the agreement rate, precision, recall and sample size.
9. RW-COE: reads the scores through GET /admin/agent-evaluations.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent times out or fails a guardrail on a case | Run stored with status TIMED_OUT or GUARDRAIL_FAILED; counted as a failure type; no retry for that event | None to a user | AC4 |
| X2 | The ACE batch for the day is not COMPLETE | Run proceeds; data_as_of holds the last complete business date and the agent must return gap STALE_INPUT; a run without it fails check SCHEMA_RULE | None to a user | AC5 |
| X3 | The same CaseCreated event arrives twice | One run for the case and business date (R-UNI-40) | None to a user | AC6 |
| X4 | Labels cover fewer cases than the sample | Agreement is computed on labeled cases only; sample size shows the labeled count | None to a user | AC7 |
| X5 | A user endpoint is asked for shadow output | No endpoint returns the output content; GET /admin/agent-runs returns metadata only | None to a user | AC1 |
| X6 | Evaluation started on an empty sample | Refused with 422 | MSG-P10-002 | AC8 |
| X7 | A role without the right starts or reads evaluations | Refused with 403 | MSG-P4-002 | TC-E1-059-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the platform (RWB-E1-058) and the client (RWB-TE-013) |
| Negotiable | Gap types, prompt and floor are data rows; the business analysts may add a gap type by a new schema version |
| Valuable | Gives the measured agreement rate that decides whether the case owner gets the summary in Epic 3 |
| Estimable | One listener, one prompt, one output schema, one sample; no screen |
| Small | One developer and one analyst for two weeks |
| Testable | Each criterion runs against the model stub with synthetic cases |

## 7. Acceptance criteria

```gherkin
Feature: Case intake agent in shadow [E1b]

  Background:
    Given agent "INTAKE" has approved policy "P1" with mode "SHADOW" and prompt "PR1"
    Given the gap types in output schema "intake-summary-v1" are MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT and STALE_INPUT

  Scenario: AC1 Shadow run
    Given 200 Epic 1 cases created between 2026-11-30 and 2026-12-04
    When the agent runs on each CaseCreated event
    Then 200 agent runs with mode "SHADOW" store a summary and gap flags
    Then no case field, task, queue or decision log entry changes
    Then GET /cases/{caseId} and GET /cases/{caseId}/timeline return no agent output
    Then GET /admin/agent-runs returns the 200 runs without the summary or the gap flags

  Scenario: AC2 Agreement rate
    Given the business analysts' review of the same 200 cases in sample "INTAKE-S1" version 1
    When the comparison runs
    Then one score row per gap type holds the agreement rate, precision, recall and sample size 200
    Then for MISSING_DOCUMENT with 182 agreeing cases the agreement rate is 0.9100
    Then each score row holds policy "P1", prompt "PR1" and the model version

  Scenario: AC3 A new case starts one shadow run
    Given case "RW-2026-000301" is created on 2026-11-30
    When EV-01 CaseCreated is processed
    Then one agent run exists with key "INTAKE:<caseId>:2026-11-30", trigger "CaseCreated" and mode "SHADOW"

  Scenario: AC4 A failed run is counted and not retried
    Given the model stub does not answer for case "RW-2026-000302"
    When the agent runs
    Then the run holds status "TIMED_OUT" and fallback true
    Then the system makes no second run for that event
    Then the failure count for type "TIMED_OUT" on 2026-11-30 is 1

  Scenario: AC5 Stale input is flagged
    Given v_ace_batch_status holds a COMPLETED ALS row for 2026-11-28 and none for 2026-11-30
    When the agent runs for case "RW-2026-000303"
    Then the run holds data_as_of 2026-11-28
    Then the stored gap flags include STALE_INPUT
    Then an answer without STALE_INPUT fails check "SCHEMA_RULE" with fallback true

  Scenario: AC6 A repeated event has no further effect
    Given EV-01 CaseCreated for case "RW-2026-000301" was processed on 2026-11-30
    When the same event arrives again with the same event ID
    Then one agent run exists for the case and date and the repeat is counted (R-UNI-40)

  Scenario: AC7 Partly labeled sample
    Given sample "INTAKE-S1" version 2 has labels for 180 of 200 cases
    When the comparison runs
    Then each score row holds sample size 180
    Then the system lists the 20 unlabeled cases as unlabeled on the evaluation run

  Scenario: AC8 Empty sample
    Given sample "INTAKE-S3" has no labeled rows for "INTAKE"
    When RW-COE starts the evaluation
    Then the system refuses the request with 422 and MSG-P10-002
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | In SHADOW mode the output is stored and never shown, and nothing on the case changes | agent_policy.autonomy_mode (New) = SHADOW |
| BR2 | The agent runs once per case per business date on EV-01 CaseCreated | R-UNI-40; event EV-01 |
| BR3 | Gap types are the enum in the approved output schema, not code | Principle 1; agent_policy.output_schema_ref (New) |
| BR4 | When an input is older than the business date, the answer must include STALE_INPUT | VR-P10-003-1; MSG-P1-001 rule of the data products |
| BR5 | Agreement rate per gap type = cases where agent flag equals label / labeled cases, 4 decimals | agent_evaluation.agreement_rate (New) |
| BR6 | A run that times out or fails a check is not retried for the same event | R-UNI-32; INT-23 retry rule |
| BR7 | Personal fields are masked before the model call | CTL-11 |

## 9. State transitions

None. This story does not change a case status. It writes agent runs (status ANSWERED, TIMED_OUT, GUARDRAIL_FAILED or BELOW_FLOOR) and one evaluation run (RUNNING to DONE).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT | Reads case, accounts, documents, valuations and contact points (Case record R, Documents R) |
| SY-CASEWF | Publishes CaseCreated |
| RW-COE | Loads the labeled sample, starts the evaluation, reads scores (Rules and parameters CRUD) |
| RW-RISK | Reads scores (Rules and parameters R) |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read run metadata (Platform administration R) |
| RW-CASEOWN | Sees nothing from this story |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-016 | recovery_case | total_outstanding_at_entry | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-DOC-001 | document | id | Read |
| DF-DOC-002 | document | case_id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-008 | document | review_status | Read |
| DF-ACE-191 | v_ace_valuation | appraised_value | Read |
| DF-ACE-193 | v_ace_valuation | appraisal_date | Read |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-080 | v_ace_contact | usage_code | Read |
| DF-AGT-036 | agent_run | id | Write |
| DF-AGT-037 | agent_run | agent_code | Write |
| DF-AGT-038 | agent_run | agent_version | Write |
| DF-AGT-039 | agent_run | prompt_version | Write |
| DF-AGT-040 | agent_run | model_version | Write |
| DF-AGT-041 | agent_run | case_id | Write |
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
| DF-AGT-063 | agent_sample | sample_code | Read |
| DF-AGT-064 | agent_sample | sample_version | Read |
| DF-AGT-066 | agent_sample | subject_id | Read |
| DF-AGT-067 | agent_sample | label_key | Read |
| DF-AGT-068 | agent_sample | expected_value | Read |
| DF-AGT-070 to DF-AGT-085 | agent_evaluation_run | all fields | Write |
| DF-AGT-087 | agent_evaluation | evaluation_run_id | Write |
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

**Event consumed:** EV-01 CaseCreated (caseId, caseNo, productGroup, accounts, businessDate). Listener is idempotent on the event ID and on the run key "INTAKE:<caseId>:<businessDate>".

**Event published:** EV-28 AgentRunCompleted (runId, agent "INTAKE", caseId, outcome, fallback).

**Tools on the allowed list** (each calls a published interface as SY-AGENT): read_case (P3 CaseQueryService.getCase), read_accounts (P3 CaseQueryService.getAccounts), read_documents (P5 DocumentQueryService.listByCase), read_valuations (P1 CollateralQueryService.listValuations), read_contact_points (P3 CaseQueryService.getContactPoints).

**Output schema "intake-summary-v1":** summary (string, at most 1,500 characters, masked tokens only), gaps (array of {gapType from the enum, reason, sourceRef}), confidence (0 to 1).

**POST /api/recovery/v1/admin/agent-evaluations** (new, RWB-E1-058): request agent "INTAKE", sampleCode "INTAKE-S1", sampleVersion 1; 202 AgentEvaluationRun; errors 401, 403, 409 (MSG-P10-003), 422 (MSG-P10-002), 503; Rules and parameters C; one RUNNING run per agent and sample version.

**GET /api/recovery/v1/admin/agent-evaluations** (new): query agent, from, to; 200 AgentEvaluationRun[]; errors 401, 403, 503; Rules and parameters R.

**GET /api/recovery/v1/admin/agent-runs** (api.yaml): query agent "INTAKE", from, to; 200 AgentRun[]; errors 401, 403, 503; Platform administration R.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/intake/`, Java package `recovery.agent.intake`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| IntakeShadowListener | Listener | Consumes EV-01 from the outbox; calls AgentOrchestrator with the run key |
| IntakeInputAssembler | Service | Builds the masked input set from the five tools |
| IntakeOutputScorer | Service | Compares gap flags with labels per gap type for the evaluation harness |
| intake-summary-v1.json | Rule table | Output schema with the gap type enum, versioned with the policy |
| prompt INTAKE PR1 | Rule table | Prompt text, loaded through POST /admin/agent-configs |

**Database:** writes agent_run, agent_evaluation_run and agent_evaluation (tables from RWB-E1-058); reads agent_sample. No migration.

**Configuration and reference data:** agent_policy INTAKE P1 and agent_prompt INTAKE PR1 loaded by RW-COE and approved by RW-RISK; sample INTAKE-S1 loaded by RW-COE from the business analysts' review file.

**Build steps**
1. Write the output schema and the prompt files; load them in DEV through the configuration endpoint.
2. Build IntakeInputAssembler over the five tools with masked values; test that no personal field reaches the request (AC1).
3. Build IntakeShadowListener with event ID and run key idempotency (AC3, AC6).
4. Add the stale input rule to the guardrail as check SCHEMA_RULE for INTAKE (AC5).
5. Build IntakeOutputScorer and plug it into the harness; test agreement, precision and recall on a 10-case fixture with known counts (AC2, AC7).
6. Test failure counting and no retry (AC4) and the empty sample refusal (AC8).

**Feature flag:** `rwb.agent.intake-shadow`. Off: the listener ignores CaseCreated.

**Done when:** the tests in section 16 pass and a DEV run over the 200 synthetic cases produces 200 runs and one complete evaluation.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-002 | Evaluation started on an empty sample | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Same evaluation already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. No case owner sees the output. RW-COE reads scores through GET /admin/agent-evaluations; run metadata shows through GET /admin/agent-runs.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-059-01 | AC1, BR1 | System | 200 synthetic cases created 2026-11-30 to 2026-12-04 |
| TC-E1-059-02 | AC2, BR5 | System | Sample INTAKE-S1 version 1, 182 agreeing cases for MISSING_DOCUMENT |
| TC-E1-059-03 | AC3, BR2 | System | Case RW-2026-000301 created 2026-11-30 |
| TC-E1-059-04 | AC4, BR6 | System | Model stub silent for case RW-2026-000302 |
| TC-E1-059-05 | AC5, BR4 | System | COMPLETED ALS row of 2026-11-28, business date 2026-11-30 |
| TC-E1-059-06 | AC6, BR2 | System | Same CaseCreated event ID twice |
| TC-E1-059-07 | AC7, BR5 | System | Sample INTAKE-S1 version 2, 180 of 200 labeled |
| TC-E1-059-08 | AC8 | System | Sample INTAKE-S3 with no rows |
| TC-E1-059-09 | Access | Access | RW-CASEOWN calls POST /admin/agent-evaluations; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: gap types, prompt, timeout and floor are versioned rows.
- No personal data in logs, tests or prompts; the summary holds masking tokens only.
- No read of another module's tables; inputs come through the P1, P3 and P5 interfaces.
- No shadow output in any user-facing response.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-005 | Personal data masked in every agent call | Business Requirements Program, section 5.4 | FEAT-AGT-03 | 06 Take over and own the case | None | TC-E1-059-01 |
| REQ-ACA-010 | Agents run under service identities with role checks | Business Requirements Program, section 5.4 | FEAT-AGT-03 | 06 Take over and own the case | R-UNI-32, R-UNI-40 | TC-E1-059-02, TC-E1-059-03, TC-E1-059-04, TC-E1-059-05, TC-E1-059-06, TC-E1-059-07, TC-E1-059-08, TC-E1-059-09 |

## 19. Out of scope

- The evaluation report and the L1 proposal (RWB-E1-061).
- Showing the summary to the case owner (RWB-E2-028, Epic 3).
- Document classification and field extraction (RWB-E1-053, RWB-E1-060).
