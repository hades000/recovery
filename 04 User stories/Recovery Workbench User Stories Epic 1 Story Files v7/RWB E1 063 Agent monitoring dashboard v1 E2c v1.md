# RWB-E1-063 Agent monitoring dashboard v1 [E2c]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-063 |
| Epic | E1, release 30 November 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-06 Publish the agent monitoring dashboard |
| Requirement IDs | REQ-DRI-009 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.7 |
| L3 process | 15 Manage performance, data and AI |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-061, RWB-E1-007, RWB-E1-014, RWB-E1-058 |
| Status | Ready for build |

## 1. Story

As a **risk and model risk officer (RW-RISK)**, I want **a dashboard with runs, acceptance, override, fallback, latency, cost and evaluation score per agent and version, and an alert when an agent's daily cost passes its limit**, so that **every agent is watched from its first shadow run**.

## 2. Business rationale

An agent in shadow that times out on one case in five, or that spends twice its budget, must be seen in the first week, not at the L1 review. This story copies daily agent run figures to the data lake with the nightly reporting extract, matched by row count (REQ-DRI-009), so the Power BI dashboard reads the copy and not the live tables. A daily check sends an alert when the cost of an agent on a business date is above its policy limit.

## 3. Preconditions

- RWB-E1-058 is done: agent_run and agent_policy exist with cost, latency and status per run.
- RWB-E1-014 is done: the nightly copy path to the data lake exists.
- RWB-E1-007 is done: outbound files and the exception queue use the integration adapters.
- JOB-15 Reporting extract runs nightly at 01:30.
- Each approved agent policy holds daily_cost_cap_thb (assumed 2,000 baht for INTAKE and SCREENING; DL33) and alert_role (assumed RW-COE).
- RW-BIANAL builds the Power BI report on the data lake table; RW-RISK and RW-COE hold Reporting R.

## 4. Flow

1. JOB-15 Reporting extract: at 01:30 calls the P10 step AgentRunExtractStep for the previous business date.
2. System: groups the agent runs of that date by agent, policy version, prompt version and model version: runs, answered, fallback, median and 95th percentile latency, tokens and cost.
3. System: adds the latest DONE evaluation score per agent and version.
4. System: writes the rows to the data lake table agent_run_daily and checks that the row count and the sum of runs match the source.
5. System: compares each agent's cost for the date with daily_cost_cap_thb of its policy; for each breach writes one agent alert and sends MSG-P10-004 through the P6 notification interface to the alert role and to RW-RISK.
6. RW-RISK: opens the Power BI report "Agent monitor v1" and reads each agent by version and date.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Row count or run sum in the data lake does not match the source | The publish is held; the previous day stays visible; the data steward and RW-PLATADM are alerted; JOB-15 reports failed for the step | None to a user | AC3 |
| X2 | JOB-15 runs again for the same business date | Rows for the date are replaced, not added; no second alert is sent | None to a user | AC4 |
| X3 | An agent has no runs on the date | One row with runs 0; no cost alert | None to a user | AC5 |
| X4 | Cost equals the cap exactly | No alert; an alert is sent only when cost is above the cap | None to a user | AC6 |
| X5 | The notification interface is unavailable | The alert row is kept with sent_at empty and retried by JOB-11 Outbox sender (R-UNI-33) | None to a user | AC7 |
| X6 | A role without Reporting R opens the report | The workspace refuses access | MSG-P4-002 | TC-E1-063-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads only P10 tables and writes through the existing copy path and notification interface |
| Negotiable | Caps, alert role and the measures shown are data; the Power BI layout is the analyst's choice |
| Valuable | Shows fallbacks and spend per agent from the first shadow run |
| Estimable | One extract step, one data lake table, one check, one Power BI page |
| Small | One developer and one BI analyst for one week |
| Testable | Each criterion runs on fixed runs for one business date |

## 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v1 [E2c]

  Background:
    Given agents "INTAKE" (policy "P1", prompt "PR1") and "SCREENING" (policy "P1", prompt "PR1") run in shadow
    Given on business date 2026-12-01 "INTAKE" has 120 runs, 9 with fallback, cost 1,840.0000 baht
    Given on 2026-12-01 "SCREENING" has 150 runs, 21 with fallback, cost 2,310.5000 baht
    Given both policies have daily_cost_cap_thb 2,000 and alert_role "RW-COE"

  Scenario: AC1 Per agent
    Given two agents in shadow
    When the dashboard opens for 2026-12-01
    Then each agent shows runs, fallback rate, median and 95th percentile latency, cost and the latest evaluation score by policy and prompt version
    Then "INTAKE" shows 120 runs and fallback rate 0.0750
    Then acceptance and override show "no L1 runs" for both agents, because no agent runs at L1 in Epic 1

  Scenario: AC2 Alert
    Given cost above the daily parameter for "SCREENING"
    When JOB-15 completes for 2026-12-01
    Then one agent alert row exists for "SCREENING", type "COST_CAP", date 2026-12-01, measured 2,310.5000 and threshold 2,000
    Then the system sends MSG-P10-004 to the holders of RW-COE and RW-RISK through the notification path
    Then no alert exists for "INTAKE"

  Scenario: AC3 A copy that does not match is held
    Given the data lake write for 2026-12-01 stores 1 row for 2 agent and version groups
    When the count check runs
    Then the system holds the publish for 2026-12-01 and the report shows 2026-11-30
    Then the step reports failed in GET /admin/jobs and the data steward is alerted

  Scenario: AC4 A rerun for the same date
    Given JOB-15 completed for 2026-12-01 and sent the "SCREENING" alert
    When RW-PLATADM reruns JOB-15 for 2026-12-01
    Then agent_run_daily holds the same 2 rows for 2026-12-01
    Then no second alert row or notification exists

  Scenario: AC5 An agent with no runs
    Given agent "EXTRACT" has an approved policy and no runs on 2026-12-01
    When JOB-15 completes for 2026-12-01
    Then "EXTRACT" shows runs 0 and cost 0.0000 for 2026-12-01 and no alert

  Scenario: AC6 Cost equal to the cap
    Given "INTAKE" cost is 2,000.0000 baht on 2026-12-02
    When JOB-15 completes for 2026-12-02
    Then no cost alert exists for "INTAKE" on 2026-12-02

  Scenario: AC7 The notification path is down
    Given the P6 notification interface is unavailable at 01:40
    When the "SCREENING" alert is raised
    Then the system keeps the alert row with sent_at empty
    Then the system sends it when the outbox sender succeeds (R-UNI-33, R-UNI-35)
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The dashboard reads the data lake copy, never the live tables | REQ-DRI-009; integration INT-20 pattern |
| BR2 | A copy is published only when its row count and run sum match the source | REQ-DRI-009; DL25 (zero tolerance) |
| BR3 | A cost alert is raised when the cost of an agent on a business date is above agent_policy.daily_cost_cap_thb (2,000 baht, assumed; DL33) | agent_policy.daily_cost_cap_thb (New) |
| BR4 | One alert per agent, type and business date | agent_alert unique key (New); R-UNI-40 |
| BR5 | Fallback rate = runs with fallback / runs, 4 decimals | agent_run.fallback (New) |
| BR6 | Alerts go to the policy alert role and to RW-RISK within 15 minutes of the end of the step (target, DL11) | agent_policy.alert_role (New); NFR-068 |

## 9. State transitions

None. This story does not change a case status. It writes agent alerts (sent_at empty, then set when sent) and daily rows in the data lake.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RISK | Reads the dashboard (Reporting R); receives alerts |
| RW-COE | Reads the dashboard (Reporting R); receives alerts as the policy alert role |
| RW-BIANAL | Builds and maintains the Power BI report (Reporting CRUD) |
| RW-PLATADM | Reruns JOB-15 (Platform administration U through POST /admin/jobs/{jobId}/rerun) |
| RW-DATASTEW | Receives the count mismatch alert |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-AGT-037 | agent_run | agent_code | Read |
| DF-AGT-038 | agent_run | agent_version | Read |
| DF-AGT-039 | agent_run | prompt_version | Read |
| DF-AGT-040 | agent_run | model_version | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-047 | agent_run | fallback | Read |
| DF-AGT-051 | agent_run | latency_ms | Read |
| DF-AGT-052 | agent_run | tokens_in | Read |
| DF-AGT-053 | agent_run | tokens_out | Read |
| DF-AGT-054 | agent_run | cost_thb | Read |
| DF-AGT-056 | agent_run | run_at | Read |
| DF-AGT-002 | agent_policy | agent_code | Read |
| DF-AGT-003 | agent_policy | policy_version | Read |
| DF-AGT-013 | agent_policy | daily_cost_cap_thb | Read |
| DF-AGT-015 | agent_policy | alert_role | Read |
| DF-AGT-089 | agent_evaluation | label_key | Read |
| DF-AGT-094 | agent_evaluation | agreement_rate | Read |
| DF-AGT-095 | agent_evaluation | precision_value | Read |
| DF-AGT-096 | agent_evaluation | recall_value | Read |
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

**Job:** JOB-15 Reporting extract (batch.txt), nightly 01:30 Asia/Bangkok. This story adds step "agentRunDaily" after the existing steps.
- Trigger: Quartz schedule of JOB-15; manual rerun through POST /admin/jobs/{jobId}/rerun.
- Input: agent_run rows with run_at on the business date; agent_policy in force; latest DONE agent_evaluation per agent and version.
- Output: data lake table agent_run_daily (business_date, agent_code, policy_version, prompt_version, model_version, runs, answered, fallback, latency_p50_ms, latency_p95_ms, tokens, cost_thb, eval_score); agent_alert rows.
- Events published: none from events.txt; alerts go through the P6 notification interface and the outbox (JOB-11 Outbox sender).
- Idempotency key: business_date for the data lake rows (replace); agent_code, alert_type, segment and business_date for alerts.
- Restart: the step restarts from the start for the date; earlier rows for the date are deleted in the same transaction as the new write.

**GET /api/recovery/v1/admin/jobs** and **POST /api/recovery/v1/admin/jobs/{jobId}/rerun** (api.yaml, P1): show and rerun JOB-15; Platform administration R and U.

**Published interface used by JOB-15:**

```java
package recovery.agent.api;
public interface AgentRunExtractSource {
    List<AgentRunDailyRow> dailyRows(LocalDate businessDate);
    List<AgentAlert> raiseCostAlerts(LocalDate businessDate);
}
```

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/monitor/`, Java package `recovery.agent.monitor`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentRunExtractSource | Published interface | Daily rows and cost alerts for JOB-15 |
| AgentMonitorService | Service | Aggregates runs; joins the latest evaluation score |
| AgentRunExtractStep | Job | Spring Batch step in JOB-15: write, count check, publish or hold |
| CostAlertService | Service | Compares cost with the cap; writes agent_alert; calls the P6 notification interface |
| AgentAlertRepository | Repository | agent_alert reads and writes |
| Agent monitor v1 | Power BI report | One page per agent with version filters, built by RW-BIANAL on agent_run_daily |

**Database:** migration `V10_006__agent_alert.sql` creates agent_alert with the standard record columns and unique (agent_code, alert_type, segment, business_date). Index agent_run (run_at).

**Configuration and reference data:** daily_cost_cap_thb and alert_role in agent_policy (RW-COE loads, RW-RISK approves). Notification template "agent cost alert" for MSG-P10-004 in the P6 template set.

**Build steps**
1. Write the agent_alert migration and entity.
2. Build AgentMonitorService aggregates on a fixture of 270 runs (AC1, AC5).
3. Build AgentRunExtractStep with the replace-by-date write and the count check (AC3, AC4).
4. Build CostAlertService with the strict greater-than rule and the unique key (AC2, AC6).
5. Send through the P6 interface with the outbox retry (AC7).
6. RW-BIANAL builds the Power BI page on agent_run_daily; check the figures against the fixture.

**Feature flag:** `rwb.agent.monitor`. Off: JOB-15 skips the step.

**Done when:** the tests in section 16 pass and the Power BI page shows the fixture figures for 2026-12-01.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-004 | Agent cost on a business date above its daily limit | {agent} used {amount} baht of model calls on {date}, above the daily limit of {limit} baht. |
| MSG-P1-001 | The report shows the previous day after a held publish | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No Workbench screen in this story. The Power BI report "Agent monitor v1" in the Workbench reporting workspace has states: loaded (figures for the latest published date) and stale (MSG-P1-001 banner with the date shown). The agent monitor screen SCR-46 comes in RWB-E2-031.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-063-01 | AC1, BR5 | System | INTAKE 120 runs, 9 fallback; SCREENING 150 runs, 21 fallback on 2026-12-01 |
| TC-E1-063-02 | AC2, BR3, BR6 | System | SCREENING cost 2,310.5000 baht, cap 2,000 |
| TC-E1-063-03 | AC3, BR2 | System | Data lake write with 1 row for 2 groups |
| TC-E1-063-04 | AC4, BR4 | System | JOB-15 rerun for 2026-12-01 |
| TC-E1-063-05 | AC5 | System | EXTRACT with no runs on 2026-12-01 |
| TC-E1-063-06 | AC6, BR3 | System | INTAKE cost 2,000.0000 baht on 2026-12-02 |
| TC-E1-063-07 | AC7 | System | Notification interface down at 01:40 |
| TC-E1-063-08 | Access | Access | RW-CASEOWN without Reporting access to the agent workspace page; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: caps and alert roles come from the agent policy.
- No personal data in logs, tests, the data lake table or the alert; rows hold counts, times and amounts only.
- No read of another module's tables; JOB-15 calls the P10 interface.
- The dashboard never reads the live agent tables.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-009 | Copied to the data lake daily for reporting, with row counts matched | Business Requirements Program, section 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | R-UNI-33, R-UNI-35, R-UNI-40 | TC-E1-063-01, TC-E1-063-02, TC-E1-063-03, TC-E1-063-04, TC-E1-063-05, TC-E1-063-06, TC-E1-063-07, TC-E1-063-08 |

## 19. Out of scope

- Acceptance and override per segment, drift alerts and the SCR-46 agent monitor screen (RWB-E2-031).
- Drift detection with a raised decision (FEAT-AGT-13, Epic 3).
- The steering dashboard (RWB-E2-009).
