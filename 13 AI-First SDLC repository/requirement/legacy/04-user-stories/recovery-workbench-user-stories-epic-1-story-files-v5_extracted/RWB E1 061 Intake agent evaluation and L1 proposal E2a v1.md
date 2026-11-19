<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 061 Intake agent evaluation and L1 proposal E2a v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 061 Intake agent evaluation and L1 proposal E2a v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-061 Intake agent evaluation and L1 proposal [E2a]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-061 |
| Epic | E1, release 30 November 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-07 Run the case intake agent at L1 |
| Requirement IDs | REQ-DRI-010, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.7 |
| L3 process | 06 Take over and own the case |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-059 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the evaluation report of the case intake agent and the proposal to run it at autonomy level 1, built from the stored shadow results**, so that **the risk and model risk officer approves the step to L1 on measured results**.

## 2. Business rationale

The step from shadow to L1 puts agent output in front of case owners, so the approver needs the agreement rate, the failure types, the cost and the latency on a stated sample before deciding. This story produces that report from the evaluation run of RWB-E1-059 and holds the L1 proposal as a versioned policy row with its conditions, fallback and measures to watch (REQ-DRI-010), approved and dated like any other reference row (REQ-DRI-011). Nothing goes to L1 until RW-RISK approves the row.

## 3. Preconditions

- RWB-E1-059 is done: evaluation run of "INTAKE" on sample "INTAKE-S1" version 1 has status DONE with 200 labeled cases.
- Policy "INTAKE" version "P1" (SHADOW) is in force.
- RW-COE holds Rules and parameters C; RW-RISK holds Rules and parameters A.

## 4. Flow

1. RW-COE: requests the report for the evaluation run through GET /admin/agent-evaluations/{evaluationId}/report.
2. System: builds the report from the stored runs and scores: sample size, agreement rate per gap type, failure counts by type, total and per-case cost, median and 95th percentile latency, policy, prompt and model versions.
3. RW-COE: exports the report as CSV and PDF for the steering committee pack.
4. RW-COE: loads policy "INTAKE" version "P2" with autonomy mode L1, the evaluation run ID, the conditions, the fallback and the measures to watch through POST /admin/agent-configs.
5. System: checks that the evaluation run is DONE, that its scores meet every stated condition and that the fallback and measures are present; stores the version as LOADED.
6. RW-RISK: approves version "P2" with a valid from date through POST /admin/agent-configs/{versionId}/approve after the committee agrees.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The report is requested for an evaluation that is still running | Refused with 409 | MSG-P10-008 | AC3 |
| X2 | The L1 proposal has no conditions, no fallback or no measures | Load refused in full | MSG-P10-001 | AC4 |
| X3 | The evaluation scores do not meet a stated condition | Load refused, naming the gap type and the score | MSG-P10-001 | AC5 |
| X4 | The sample size is below the minimum of 200 cases | Load refused | MSG-P10-001 | AC6 |
| X5 | The loader tries to approve the proposal | Refused with 409 | MSG-P7-002 | AC7 |
| X6 | A role without the right | Refused with 403 | MSG-P4-002 | TC-E1-061-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads only the stored results of RWB-E1-059 |
| Negotiable | Conditions and measures are values in the proposal row; the story fixes their presence and the check against scores |
| Valuable | Gives the approver one report and one row to approve for the first autonomy step |
| Estimable | One report query, one export, one extra check in the policy loader |
| Small | Three to four days |
| Testable | Each criterion runs on a stored evaluation fixture |

## 7. Acceptance criteria

```gherkin
Feature: Intake agent evaluation and L1 proposal [E2a]

  Background:
    Given evaluation run "EV-INTAKE-001" of "INTAKE" on sample "INTAKE-S1" version 1 has status "DONE"
    Given it holds 200 shadow runs: 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR
    Given the 200 runs cost 412.6000 baht in total with median latency 4,100 ms and 95th percentile 9,800 ms

  Scenario: AC1 Report
    Given the shadow results
    When the report is written
    Then it holds sample size 200, the agreement rate per gap type, failure counts 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR
    Then it holds total cost 412.6000 baht, cost per case 2.0630 baht, median latency 4,100 ms and 95th percentile 9,800 ms
    Then it holds policy "P1", prompt "PR1" and the model version, and no personal field

  Scenario: AC2 Proposal
    Given the report
    When RW-COE loads policy "INTAKE" version "P2" with mode "L1", evaluation run "EV-INTAKE-001", conditions "agreement at least 0.85 for every gap type", fallback "rule result per R-UNI-32" and measures "acceptance, correction rate, fallback rate below 0.10"
    Then the system stores version "P2" with status "LOADED" and holds the conditions, the fallback and the measures to watch
    Then "P1" stays in force until RW-RISK approves "P2"

  Scenario: AC3 Report on an unfinished evaluation
    Given evaluation run "EV-INTAKE-002" has status "RUNNING"
    When RW-COE requests its report
    Then the system refuses the request with 409 and MSG-P10-008

  Scenario: AC4 A proposal without its measures
    Given a policy file with mode "L1" and no measures to watch
    When RW-COE loads it
    Then the system refuses the load with 422 and MSG-P10-001 naming check "measures to watch present"

  Scenario: AC5 Scores below a stated condition
    Given gap type NO_CONTACT_POINT has agreement 0.8150 in "EV-INTAKE-001"
    When RW-COE loads a proposal with condition "agreement at least 0.85 for every gap type"
    Then the system refuses the load with 422 and MSG-P10-001 naming "NO_CONTACT_POINT 0.8150 below 0.85"

  Scenario: AC6 Sample below the minimum
    Given evaluation run "EV-INTAKE-003" has sample size 150
    When RW-COE loads a proposal that names it
    Then the system refuses the load with 422 and MSG-P10-001 naming check "sample size at least 200"

  Scenario: AC7 The loader cannot approve the proposal
    Given user "coe.user01" loaded version "P2"
    When user "coe.user01" approves "P2"
    Then the system refuses the approval with 409 and MSG-P7-002
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An L1 proposal names one DONE evaluation run, the conditions, the fallback and the measures to watch | agent_policy.promotion_conditions, watch_measures, evaluation_run_id (New) |
| BR2 | Every stated condition is checked against the scores of the named run before the version is stored | Principle 1; CTL-08 |
| BR3 | The minimum sample for an autonomy step is 200 cases (assumed; set in the policy loader schema) | FEAT-AGT-03 |
| BR4 | Cost per case = total cost / runs, 4 decimals; latency percentiles are computed over all runs including timeouts at 60,000 ms | agent_run.cost_thb, latency_ms (New) |
| BR5 | The fallback of an L1 agent is the rule result | R-UNI-32 |
| BR6 | The loader and the approver are different people | Separation of duty, center of excellence analyst and risk and model risk officer |

## 9. State transitions

None. This story does not change a case status. Policy version "P2" moves from no row to LOADED, and to APPROVED when RW-RISK approves it.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Requests and exports the report; loads the proposal (Rules and parameters CRUD) |
| RW-RISK | Reads the report; approves the proposal (Rules and parameters A) |
| RW-AUDIT | Reads the report and the versions (Rules and parameters R) |
| Approval levels | No delegation of authority level applies |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-AGT-070 | agent_evaluation_run | id | Read |
| DF-AGT-077 | agent_evaluation_run | status | Read |
| DF-AGT-072 | agent_evaluation_run | sample_code | Read |
| DF-AGT-073 | agent_evaluation_run | sample_version | Read |
| DF-AGT-074 | agent_evaluation_run | policy_version | Read |
| DF-AGT-075 | agent_evaluation_run | prompt_version | Read |
| DF-AGT-076 | agent_evaluation_run | model_version | Read |
| DF-AGT-081 | agent_evaluation_run | total_cost_thb | Read |
| DF-AGT-082 | agent_evaluation_run | p95_latency_ms | Read |
| DF-AGT-083 | agent_evaluation_run | failure_counts | Read |
| DF-AGT-089 | agent_evaluation | label_key | Read |
| DF-AGT-090 | agent_evaluation | sample_size | Read |
| DF-AGT-094 | agent_evaluation | agreement_rate | Read |
| DF-AGT-095 | agent_evaluation | precision_value | Read |
| DF-AGT-096 | agent_evaluation | recall_value | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-051 | agent_run | latency_ms | Read |
| DF-AGT-054 | agent_run | cost_thb | Read |
| DF-AGT-002 | agent_policy | agent_code | Write |
| DF-AGT-003 | agent_policy | policy_version | Write |
| DF-AGT-008 | agent_policy | autonomy_mode | Write |
| DF-AGT-021 | agent_policy | status | Write |
| DF-AGT-022 | agent_policy | valid_from | Write |
| DF-AGT-024 | agent_policy | loaded_by | Write |
| DF-AGT-017 | agent_policy | evaluation_run_id | Write |
| DF-AGT-018 | agent_policy | promotion_conditions | Write |
| DF-AGT-019 | agent_policy | watch_measures | Write |
| DF-AGT-020 | agent_policy | fallback_rule | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/admin/agent-evaluations/{evaluationId}/report** (new, see additions)
- Request: path runId (uuid); Accept application/json, text/csv or application/pdf.
- Response: 200 AgentEvaluationReport (agent, sampleSize, versions, agreementByLabel[], failureCounts, totalCostThb, costPerCaseThb, latencyP50Ms, latencyP95Ms).
- Errors: 401; 403; 404 unknown run; 409 run not DONE (MSG-P10-008); 503.
- Authorization: Rules and parameters, R. Idempotency: read only; the same run gives the same report.

**POST /api/recovery/v1/admin/agent-configs** (new, RWB-E1-058): kind POLICY, agent "INTAKE"; this story adds the L1 checks (BR1 to BR3); 201 AgentConfigVersion; errors 401, 403, 409, 422 (MSG-P10-001), 503; Rules and parameters C.

**POST /api/recovery/v1/admin/agent-configs/{versionId}/approve** (new): 200; errors 401, 403, 404, 409 (MSG-P7-002, MSG-GEN-004), 503; Rules and parameters A.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/eval/report/`, Java package `recovery.agent.eval.report`; policy checks in `recovery.agent.config`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentEvaluationController | Controller | Adds GET /admin/agent-evaluations/{evaluationId}/report |
| EvaluationReportService | Service | Aggregates runs and scores into the report |
| EvaluationReportExporter | Service | Writes CSV and PDF from the same report object |
| PromotionProposalValidator | Service | BR1 to BR3 checks inside AgentConfigService for mode L1 |

**Database:** migration `V10_004__policy_promotion.sql` adds evaluation_run_id uuid, promotion_conditions jsonb, watch_measures jsonb and fallback_rule varchar(20) to agent_policy. Reads agent_run, agent_evaluation_run and agent_evaluation.

**Configuration and reference data:** the minimum sample 200 is a value in the policy JSON schema version used by the loader.

**Build steps**
1. Build EvaluationReportService over a fixture of 200 runs with the counts in the Background (AC1).
2. Build the CSV and PDF exporter from the same object (AC1).
3. Add the 409 for a run that is not DONE (AC3).
4. Build PromotionProposalValidator and add it to the policy load (AC2, AC4, AC5, AC6).
5. Reuse the approval check from RWB-E1-058 and test it for an L1 version (AC7).

**Feature flag:** `rwb.agent.promotion`. Off: a policy with mode L1 is refused with 422.

**Done when:** the tests in section 16 pass and the report for "EV-INTAKE-001" is attached to the steering committee pack.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-008 | Report requested before the evaluation is done | The evaluation of {agent} on sample {sample} has not finished. The report is ready when it is done. |
| MSG-P10-001 | The proposal fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P7-002 | Loader approves own proposal | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. RW-COE and RW-RISK read the report through the report endpoint and its CSV or PDF export.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-061-01 | AC1, BR4 | System | Evaluation EV-INTAKE-001, 200 runs, 412.6000 baht |
| TC-E1-061-02 | AC2, BR1, BR5 | System | Policy INTAKE P2 with mode L1 and all three parts |
| TC-E1-061-03 | AC3 | System | Evaluation EV-INTAKE-002 RUNNING |
| TC-E1-061-04 | AC4, BR1 | System | L1 policy file without measures |
| TC-E1-061-05 | AC5, BR2 | System | NO_CONTACT_POINT agreement 0.8150 |
| TC-E1-061-06 | AC6, BR3 | System | Evaluation EV-INTAKE-003 with sample size 150 |
| TC-E1-061-07 | AC7, BR6 | System | Loader coe.user01 approves P2 |
| TC-E1-061-08 | Access | Access | RW-CASEOWN requests the report; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: conditions, measures and the minimum sample are row values.
- No personal data in logs, tests or the report; the report holds counts and rates only.
- No read of another module's tables.
- A proposal never changes the mode in force before it is approved and its valid from date is reached.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | Business Requirements Program, section 5.7 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32 | TC-E1-061-01, TC-E1-061-02, TC-E1-061-03, TC-E1-061-04, TC-E1-061-05, TC-E1-061-06 |
| REQ-DRI-011 | Every versioned table has valid from and to dates, author and approver | Business Requirements Program, section 5.7 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E1-061-02, TC-E1-061-07, TC-E1-061-08 |

## 19. Out of scope

- Showing the intake summary to case owners at L1 (RWB-E2-028).
- Changing an autonomy level from a screen (FEAT-AGT-12, Epic 3).
- The steering committee meeting itself and its minutes.
