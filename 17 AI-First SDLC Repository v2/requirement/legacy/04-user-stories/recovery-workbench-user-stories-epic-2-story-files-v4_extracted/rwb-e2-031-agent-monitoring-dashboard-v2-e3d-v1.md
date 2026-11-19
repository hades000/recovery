<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 031 Agent monitoring dashboard v2 E3d v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 031 Agent monitoring dashboard v2 E3d v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-031 Agent monitoring dashboard v2 [E3d]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-031 |
| Epic | E2, release 31 December 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-06 Publish the agent monitoring dashboard |
| Requirement IDs | REQ-DRI-009, REQ-APD-005 |
| BRD section | Business Requirements Epic 2, section 3.10; Business Requirements Program, section 5.7 |
| L3 process | 15 Manage performance, data and AI |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-063, RWB-E2-005 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the agent monitor screen to show acceptance, override, fallback, latency and cost per agent, version and segment, with a drift alert when acceptance falls**, so that **every agent at L1 is watched daily and a fall in acceptance is acted on within a day**.

## 2. Business rationale

At L1 a case owner reads the agent's output and accepts, corrects or rejects it. A fall in acceptance on one segment is the first sign that a prompt, a model version or the data has changed. This story puts acceptance, override, fallback, latency and cost per agent, version and segment on the agent monitor screen SCR-46, reconciles tokens and cost to the per-call figures the endpoint returns, reports override reasons (REQ-APD-005) and checks drift daily from the same copied figures used for reporting (REQ-DRI-009).

## 3. Preconditions

- RWB-E1-063 is done: agent_run_daily is written by JOB-15 and agent_alert exists.
- RWB-E2-005 is done: the P7 decision log query interface returns entries by agent version and date.
- Agent runs carry the segment (product group and region) of their case.
- Feedback on L1 output is recorded in agent_feedback (verdict ACCEPTED, CORRECTED or REJECTED) by RWB-E2-028; until then acceptance shows "no L1 runs".
- Each L1 policy holds watch_measures with drift_points 10 (assumed) and minimum feedback 20 per week per segment (assumed).
- The user holds Platform administration R.

## 4. Flow

1. RW-COE: opens SCR-46 Agent monitor from the Administration menu.
2. System: checks Platform administration R, then calls GET /admin/agent-metrics for the last 30 days.
3. System: returns one row per agent, policy version, prompt version, model version, segment and day: runs, fallback rate, acceptance rate, correction rate, override rate, median and 95th percentile latency, tokens and cost.
4. RW-COE: filters by agent, segment and date range; the screen shows the state of each agent: Shadow, live (L1) or paused (mode OFF).
5. JOB-15 Reporting extract: after the daily rows, runs the drift check for each L1 agent and segment: acceptance of the last 7 days against the 7 days before.
6. System: on a fall of 10 points or more, writes one DRIFT alert and sends MSG-P10-006 to the policy alert role and RW-RISK.
7. RW-COE: opens the override reasons for an agent and month and sees the count per coded reason.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Fewer than 20 feedback entries in either week for a segment | No drift check for that segment; the screen shows "not enough feedback" | None to a user | AC4 |
| X2 | Filter "from" after "to" | Refused with 422 | MSG-GEN-003 | AC5 |
| X3 | Filter range longer than 92 days | Refused with 422 | MSG-GEN-002 | AC6 |
| X4 | Drift check runs again for the same date | No second alert (unique key) | None to a user | AC7 |
| X5 | Token sum in agent_run_daily does not match the sum of agent_run for a month | The month shows "not reconciled" with the difference | None to a user | AC3 |
| X6 | A role without Platform administration R opens SCR-46 | Refused with 403 | MSG-P4-002 | TC-E2-031-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the daily rows of RWB-E1-063 and the decision log query of RWB-E2-005 |
| Negotiable | Drift points, minimum feedback and window are policy values |
| Valuable | Turns acceptance and override into a daily alert for each L1 agent and segment |
| Estimable | One endpoint, one screen, one daily check, one reconciliation query |
| Small | One back end and one front end developer for one week |
| Testable | Each criterion uses fixed runs, feedback and decisions over two weeks |

## 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v2 [E3d]

  Background:
    Given agents "INTAKE" (policy "P2", mode "L1") and "SCREENING" (policy "P2", mode "L1" for segment MORTGAGE and BKK) are live
    Given the drift rule is a fall of 10 points or more with at least 20 feedback entries in each week

  Scenario: AC1 Per agent
    Given two agents at L1
    When the dashboard loads for 2026-12-01 to 2026-12-14
    Then acceptance, override, fallback, latency and cost show per agent, version and segment
    Then "INTAKE" for segment MORTGAGE and BKK shows 140 feedback entries with 119 accepted, acceptance rate 0.8500
    Then "SCREENING" shows state "live" for MORTGAGE and BKK and "Shadow" for every other segment

  Scenario: AC2 Drift
    Given "INTAKE" acceptance for MORTGAGE and BKK is 0.8600 for 2026-12-01 to 2026-12-07 and 0.7500 for 2026-12-08 to 2026-12-14
    When the check runs after JOB-15 for 2026-12-14
    Then one alert of type "DRIFT" for "INTAKE", segment "MORTGAGE/BKK" and date 2026-12-14 holds measured 0.7500 and threshold 0.7600
    Then MSG-P10-006 goes to the holders of RW-COE and RW-RISK

  Scenario: AC3 Cost
    Given a month of calls in November 2026 for "INTAKE": 3,100 runs with 2,945,000 input tokens and 465,000 output tokens
    When the dashboard loads for November 2026
    Then tokens and cost per agent match the sum of the agent runs, which hold the token counts the endpoint returned on each call
    Then "INTAKE" shows 3,410,000 tokens and cost 170.5000 baht at 0.0500 baht per 1,000 tokens
    Then a month where the daily rows and the runs differ shows "not reconciled" with the token difference

  Scenario: AC4 Not enough feedback
    Given "SCREENING" for MORTGAGE and BKK has 12 feedback entries in the week to 2026-12-14
    When the check runs
    Then the system raises no drift alert for that segment and the screen shows "not enough feedback"

  Scenario: AC5 Dates in the wrong order
    When RW-COE filters from 2026-12-14 to 2026-12-01
    Then the system refuses the request with 422 and MSG-GEN-003

  Scenario: AC6 A range that is too long
    When RW-COE filters from 2026-08-01 to 2026-12-14
    Then the system refuses the request with 422 and MSG-GEN-002 naming 1 and 92 days

  Scenario: AC7 The check runs twice
    Given the DRIFT alert for "INTAKE", "MORTGAGE/BKK" and 2026-12-14 exists
    When JOB-15 is rerun for 2026-12-14
    Then no second alert row or notification exists
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Acceptance rate = accepted / (accepted + corrected + rejected) of L1 feedback; correction rate = corrected / the same total | agent_feedback.verdict (New) |
| BR2 | Override rate = decisions with the agent version where final_call differs from the recommendation / decisions with the agent version; reasons counted from override_reason codes | REQ-APD-005; decision_log_entry.override_reason; CTL-07 |
| BR3 | Drift = acceptance of the last 7 days at least 10 points below the 7 days before, with at least 20 feedback entries in each week (assumed values in watch_measures) | agent_policy.watch_measures (New) |
| BR4 | Token and cost totals come from agent_run; a month is reconciled when the daily rows equal the run sums | REQ-DRI-009; DL25 |
| BR5 | One alert per agent, type, segment and business date | agent_alert unique key (New) |
| BR6 | A segment is the case product group and region at run time | recovery_case.product_group, recovery_case.region_code |

## 9. State transitions

None. This story does not change a case status. It writes agent alerts of type DRIFT and shows each agent's mode as Shadow, live or paused.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Open SCR-46 and call GET /admin/agent-metrics (Platform administration R) |
| RW-RISK | Receives drift alerts; reads the Power BI copy (Reporting R); does not hold Platform administration |
| SY-AGENT | None in this story |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-007 | decision_log_entry | agent_version | Read (through the P7 query interface) |
| DF-DEC-009 | decision_log_entry | recommendation | Read |
| DF-DEC-012 | decision_log_entry | final_call | Read |
| DF-DEC-013 | decision_log_entry | override_reason | Read |
| DF-DEC-016 | decision_log_entry | decided_at | Read |
| DF-AGT-037 | agent_run | agent_code | Read |
| DF-AGT-038 | agent_run | agent_version | Read |
| DF-AGT-040 | agent_run | model_version | Read |
| DF-AGT-043 | agent_run | autonomy_mode | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-047 | agent_run | fallback | Read |
| DF-AGT-051 | agent_run | latency_ms | Read |
| DF-AGT-052 | agent_run | tokens_in | Read |
| DF-AGT-053 | agent_run | tokens_out | Read |
| DF-AGT-054 | agent_run | cost_thb | Read |
| DF-AGT-056 | agent_run | run_at | Read |
| DF-AGT-098 | agent_feedback | agent_run_id | Read |
| DF-AGT-100 | agent_feedback | verdict | Read |
| Standard column | agent_feedback | created_at | Read |
| DF-AGT-059 | agent_run | segment_product_group | Write (set at run time by the orchestrator) |
| DF-AGT-060 | agent_run | segment_region_code | Write (set at run time by the orchestrator) |
| DF-AGT-008 | agent_policy | autonomy_mode | Read |
| DF-AGT-009 | agent_policy | segment_product_group | Read |
| DF-AGT-010 | agent_policy | segment_region_code | Read |
| DF-AGT-019 | agent_policy | watch_measures | Read |
| DF-AGT-015 | agent_policy | alert_role | Read |
| DF-AGT-103 | agent_alert | id | Write |
| DF-AGT-104 | agent_alert | agent_code | Write |
| DF-AGT-105 | agent_alert | alert_type | Write |
| DF-AGT-106 | agent_alert | segment | Write |
| DF-AGT-107 | agent_alert | business_date | Write |
| DF-AGT-108 | agent_alert | measured_value | Write |
| DF-AGT-109 | agent_alert | threshold_value | Write |
| DF-AGT-110 | agent_alert | sent_to_role | Write |
| DF-AGT-111 | agent_alert | sent_at | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/admin/agent-metrics** (new, see additions)
- Request: query agent, segment (for example "MORTGAGE/BKK"), from, to (dates), version.
- Response: 200, array of AgentMetric (agent, policyVersion, promptVersion, modelVersion, segment, mode, date, runs, fallbackRate, acceptanceRate, correctionRate, overrideRate, feedbackCount, latencyP50Ms, latencyP95Ms, tokens, costThb, reconciled).
- Errors: 401; 403 (MSG-P4-002); 422 from after to (MSG-GEN-003) or range over 92 days (MSG-GEN-002); 503.
- Authorization: Platform administration, R, scope applied.
- Idempotency: read only.

**GET /api/recovery/v1/admin/agent-runs** (api.yaml): drill-down to runs from a metric row; Platform administration R.

**Job:** JOB-15 Reporting extract, nightly 01:30; this story adds step "agentDrift" after "agentRunDaily". Input: agent_feedback rows of the last 14 days per L1 agent and segment. Output: agent_alert rows type DRIFT and MSG-P10-006 through the P6 notification interface. Idempotency key: agent_code, alert_type, segment, business_date. Restart: the step reruns for the date with no new alert where one exists.

**Interface called:** P7 DecisionLogQuery.byAgentVersion(agentVersion, from, to), from RWB-E2-005.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/monitor/`; front end `src/modules/recovery/agent/monitor/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentMetricsController | Controller | GET /admin/agent-metrics with filter checks |
| AgentMetricsService | Service | Builds metric rows from agent_run_daily, agent_feedback and the P7 override counts |
| DriftCheckStep | Job | Step in JOB-15 applying BR3 per L1 agent and segment |
| CostReconciliationQuery | Repository | Compares daily rows with run sums per month |
| AgentMonitorPage | React component | SCR-46 with agent, segment and date filters, state badges Shadow, live and paused |
| OverrideReasonPanel | React component | Count of override reasons per agent and month |

**Database:** migration `V10_007__agent_run_segment.sql` adds segment_product_group varchar(15) and segment_region_code varchar(10) to agent_run, with index (agent_code, segment_product_group, segment_region_code, run_at). Reads agent_run, agent_policy, agent_alert.

**Configuration and reference data:** watch_measures in each L1 policy (drift_points 10, min_feedback 20, window_days 7), loaded by RW-COE and approved by RW-RISK.

**Build steps**
1. Add the segment columns and set them in AgentRuntimeService from the case read (BR6).
2. Build AgentMetricsService and its rates on a two-week fixture (AC1).
3. Build AgentMetricsController with the filter checks (AC5, AC6).
4. Build CostReconciliationQuery (AC3).
5. Build DriftCheckStep with the minimum feedback rule and the unique alert key (AC2, AC4, AC7).
6. Build AgentMonitorPage and OverrideReasonPanel with Radix components and the common states.

**Feature flag:** `rwb.agent.monitor-v2`. Off: SCR-46 shows runs and fallbacks only, and the drift step is skipped.

**Done when:** the tests in section 16 pass and SCR-46 shows the fixture figures.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-006 | Acceptance falls by 10 points or more | {agent} acceptance for {segment} fell from {from} to {to} percent in the week to {date}. |
| MSG-GEN-003 | Filter dates in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-002 | Filter range above 92 days | {field} must be between {min} and {max}. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-46 Agent monitor, from the Administration menu. States per agent and segment: Shadow (mode SHADOW: runs, fallbacks and evaluation scores, no acceptance), live (mode L1: all measures), paused (mode OFF: history only). Common states: loading (skeleton rows), empty ("No agent runs in this period."), error (message at the top). The user filters by agent, segment and dates, opens a row to see the runs through GET /admin/agent-runs, and opens the override reasons.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-031-01 | AC1, BR1, BR2, BR6 | System | INTAKE MORTGAGE/BKK 140 feedback, 119 accepted |
| TC-E2-031-02 | AC2, BR3 | System | Acceptance 0.8600 then 0.7500 |
| TC-E2-031-03 | AC3, BR4 | System | November 2026: 3,100 runs, 2,945,000 and 465,000 tokens |
| TC-E2-031-04 | AC4, BR3 | System | 12 feedback entries in the week |
| TC-E2-031-05 | AC5 | System | From 2026-12-14 to 2026-12-01 |
| TC-E2-031-06 | AC6 | System | From 2026-08-01 to 2026-12-14 |
| TC-E2-031-07 | AC7, BR5 | System | JOB-15 rerun for 2026-12-14 |
| TC-E2-031-08 | Access | Access | RW-CASEOWN opens SCR-46; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: drift points, minimum feedback and window are policy values.
- No personal data in logs, tests or the screen; metrics hold counts, rates, times and amounts.
- No read of another module's tables; override figures come through the P7 query interface.
- The screen shows no prompt text and no agent output content.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched | Business Requirements Program, section 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | R-UNI-40 | TC-E2-031-01, TC-E2-031-02, TC-E2-031-03, TC-E2-031-04, TC-E2-031-05, TC-E2-031-06, TC-E2-031-07, TC-E2-031-08 |
| REQ-APD-005 | An override needs a coded reason, reported monthly | Business Requirements Program, section 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-01 |

## 19. Out of scope

- Drift detection that raises a decision with an owner and a date (FEAT-AGT-13, Epic 3).
- Changing an autonomy level from SCR-46 (FEAT-AGT-12, Epic 3; FEAT-AGT-15, Epic 8).
- Agent risk review at the committee (FEAT-AGT-16, Epic 8).
