# RWB-ITG-E2031-ITG Agent monitoring dashboard v2 [E3d]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2031-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP07, DP10, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P7-E2005-APP, RWB-P10-E2031-APP, RWB-P4-E2031-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-031 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **a repeatable cross-service journey harness for the agent monitor — one metrics row set, one drift alert and one override count that describe the same agent, policy version, segment and business date across rwb-agent, rwb-access and rwb-decision — with the evidence pack attached to the wave 2 release**, so that **every agent at L1 is watched daily and a fall in acceptance is acted on within a day before RWB-P10-E2031-APP, RWB-P4-E2031-APP and RWB-P7-E2005-APP claim Done**.

This story builds the harness, its contract fakes, its seed pack, its evidence pack and its pass or fail gate. It builds no production endpoint, no screen, no table and no migration. Nothing it writes is deployed to a service.

No single app story can prove the journey. RWB-P10-E2031-APP proves the metrics operation, the drift check and the alert row inside rwb-agent; it can show a DRIFT alert that rwb-agent wrote, but not that the acceptance it measured is the acceptance the case owners gave. RWB-P4-E2031-APP proves the session read and the Platform administration right; it can show that a role was refused, but not that the figures behind the refusal describe the agent the reader asked about. RWB-P7-E2005-APP proves that the override counts and the coded reasons are read from the decision log; it can show the counts of one agent version, but not that they are the counts of the runs the monitor reports. Only their agreement — one dashboard row, one drift alert and one override count naming the same agent, version, segment and business date — proves that the monitor the business reads is the monitor the three services actually feed. That proof is this story, and only this story.

### 2. Business rationale

RWB-E2-031 split into three app stories and this integration story. The app stories build the metrics endpoint, the drift check and the alert inside rwb-agent, the session and the Platform administration right inside rwb-access, and the decision-log read that the override counts come from inside rwb-decision. What no app story can prove alone is the chain the business relies on, and the harness asserts it in one order:

- agent runs carry the segment of their case, so a row is per agent, version and segment rather than per service;
- feedback gives acceptance and correction, and its verdict is the only source of those two rates;
- decisions give the override rate and the coded reasons, counted per agent version and month;
- the daily rows reconcile to the runs, so tokens and cost are the sums of what the endpoint returned on each call;
- the drift check compares the last 7 days with the 7 days before, per L1 agent and segment;
- a fall of 10 points or more with enough feedback in each week writes one DRIFT alert and sends MSG-P10-006 to the policy alert role and to RW-RISK.

The journey carries two requirements. Copied daily for reporting with row counts matched (REQ-DRI-009): the harness asserts that the daily rows it reads and the runs behind them agree, and it reads the reporting copy of the figures — the copy rwb-reporting projects from the events — rather than any lake copy, because the target has no data lake. An override needs a coded reason, reported monthly (REQ-APD-005): the harness asserts that every override figure it reads is matched by coded reasons whose counts add up to it, and it reads those reasons through rwb-decision's own contract, never from the decision tables.

Architecture v5 changes the path, not the business. In the monolith the monitor endpoint, the feedback table, the scope check and the decision log sat in one deployment and one schema. In the target:

- the decision records and the shared topic `rwb.decision-record.v1` carry every override, and the harness reads the ledger through rwb-decision's contract (DP-03);
- the mode per segment, the verdict labels and the coded reason list are reference data of the owning services, seeded as data and never values in harness code (DP-07);
- the drift check is a Temporal Schedule in rwb-agent, so the legacy agentDrift step of JOB-15 now belongs to the owning service and the harness only triggers and observes it (DP-10);
- every path is on the owner's base `/api/recovery/<short>/v1`, so the harness never calls a monolith base (DP-13);
- each service migrates its own schema through its own Flyway sequence, and the harness runs no migration at all (DP-15);
- the monitor row reaches the screen through the gateway-bff composite route, so the harness drives the same route the SCR-46 reader uses (DP-19).

The measure is the journey evidence: for each owned criterion, one pass or fail, with the metric rows, the runs, the override counts, the alert row, the notification and the reconciliation captured in one report that can be re-run for any build.

### 3. Preconditions

- The wave 2 harness environment (SIT) is available with the gateway route for `/api/recovery/*`, the topic `rwb.agent.events.v1`, the shared topic `rwb.decision-record.v1`, the Temporal namespace `rwb-recovery` with the queue `rwb-agent`, and a clock control that fixes "today" and the drift date. Not specified in the source documents (GAP-0413; ASM-0588): the harness environment, its seed pack, its fixed clock and its evidence format.
- The three integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-P10-E2031-APP (rwb-agent, the metrics, the runs and the configs), RWB-P4-E2031-APP (rwb-access, the session and the Platform administration right) and RWB-P7-E2005-APP (rwb-decision, the decision-log read the override counts come from).
- Agents "INTAKE" (policy "P2", mode "L1") and "SCREENING" (policy "P2", mode "L1" for MORTGAGE and BKK, Shadow for every other segment) are live (legacy section 7 Background).
- Each L1 policy holds watch_measures with drift points 10 and at least 20 feedback entries in each week: the drift rule is a fall of 10 points or more with at least 20 feedback entries in each week (legacy sections 3 and 7).
- The two weeks are seeded: 2026-12-01 to 2026-12-07 and 2026-12-08 to 2026-12-14, with "INTAKE" for MORTGAGE and BKK holding 140 feedback entries of which 119 are accepted, acceptance 0.8500, and "SCREENING" for MORTGAGE and BKK holding 12 feedback entries in the week to 2026-12-14 (legacy AC1 and AC4).
- November 2026 is seeded for "INTAKE": 3,100 runs with 2,945,000 input tokens and 465,000 output tokens, and a second month whose daily rows differ from the runs (legacy AC3).
- The filter fixtures are present: a from after to, and a range of 2026-08-01 to 2026-12-14; the metric window the harness reads is 2026-12-01 to 2026-12-14 and the filter limit is 92 days (legacy AC5 and AC6).
- A test user of role RW-CASEOWN holds no Platform administration right, and the seed carries counts, rates, times and amounts only: no customer name, account number, national identifier or contact detail enters the harness, the seed pack or the evidence pack (legacy sections 10 and 17).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date, the drift date 2026-12-14 and the versions of the five operations it is about to exercise.
2. Harness: seeds agents "INTAKE" and "SCREENING", their policies (P2, mode L1 for MORTGAGE and BKK, Shadow elsewhere), the runs and feedback of the two weeks, the decisions with their coded override reasons, and the November 2026 runs with their token counts.
3. Harness: calls the P4 session operation against the rwb-access fake and records the role, the Platform administration right and the refusal answer the journey runs under.
4. Harness: reads the configs through `GET /api/recovery/agent/v1/admin/agent-configs` and records the policy versions, the modes per segment and the watch measures, then subscribes to `rwb.agent.events.v1` and `rwb.decision-record.v1` with its own consumer group.
5. Harness: reads `GET /api/recovery/agent/v1/admin/agent-metrics` for 2026-12-01 to 2026-12-14 and asserts one row per agent, version and segment with acceptance, override, fallback, latency and cost.
6. Harness: asserts "INTAKE" MORTGAGE/BKK at 140 feedback entries, 119 accepted and acceptance 0.8500, and "SCREENING" at state "live" for MORTGAGE and BKK and "Shadow" for every other segment.
7. Harness: reads the runs through `GET /api/recovery/agent/v1/admin/agent-runs` and the override counts and coded reasons through `GET /api/recovery/decision/v1/decision-log`, then asserts that every metric row's override count equals the decision-log count for the same agent version and month.
8. Harness: runs the drift check for 2026-12-14 on the acceptance 0.8600 then 0.7500 of "INTAKE" MORTGAGE/BKK, twice in a row.
9. Harness: asserts exactly one alert of type "DRIFT" for "INTAKE", segment "MORTGAGE/BKK", date 2026-12-14 with measured 0.7500 and threshold 0.7600, that MSG-P10-006 went to the holders of RW-COE and RW-RISK, and that the second run added no alert row and no notification.
10. Harness: runs the drift check over the 12-feedback week of "SCREENING" MORTGAGE/BKK and asserts no alert for that segment and the state "not enough feedback" on its row.
11. Harness: runs the filter refusals — a from after to answering 422 with MSG-GEN-003, a range over 92 days answering 422 with MSG-GEN-002 naming 1 and 92 days — and the RW-CASEOWN read answering 403 with MSG-P4-002.
12. Harness: runs the cost reconciliation for November 2026 (3,410,000 tokens and 170.5000 baht at 0.0500 baht per 1,000 tokens) and for the month whose daily rows differ, then writes the per-scenario evidence into one run report keyed by story key and business date, evaluates the gate, attaches the report to the wave 2 release record, releases the lock and restores the seed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Fewer than 20 feedback entries in either week for a segment | No drift check for that segment; the monitor row shows "not enough feedback" and the harness records the count it found | None to a user | AC4 |
| X2 | Filter "from" after "to" | The metrics read is refused with 422 and no row is returned | MSG-GEN-003 | AC5 |
| X3 | Filter range longer than 92 days | The metrics read is refused with 422 naming the minimum and the maximum | MSG-GEN-002 | AC6 |
| X4 | The drift check runs again for the same date | No second alert row and no second notification; the scenario passes only when the alert count stays 1 | None to a user | AC7 |
| X5 | The token sum in the daily rows does not match the sum of the runs for a month | The month answers "not reconciled" with the token difference, and the harness records both figures | None to a user | AC3 |
| X6 | A role without Platform administration R calls the metrics operation | The read is refused with 403 and no row is returned | MSG-P4-002 | AC8 |
| X7 | The seed pack cannot be loaded (agent absent, policy version absent, segment missing, counts off) | The run refuses to start and names the missing seed item; no scenario is reported | None | All |
| X8 | A fake answers a contract version other than the one the run locked | The run fails and the evidence records the locked version and the answered version | None | All |
| X9 | The evidence pack cannot be attached to the release record | The run is marked failed; the local evidence file is kept for rerun | None | All |
| X10 | A metric row's override count and the decision-log count differ for the same agent version and month | The run fails and names both figures, so the disagreement is read before the release, not after it | None | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the three published contracts or their fakes, the two-week seed and the November token seed; it builds no service feature and has no build dependency |
| Negotiable | The drift points, the minimum feedback, the window, the fixture counts and the fake set are data files, never code |
| Valuable | The monitor journey is proven once across three services, with the metric row, the drift alert, the override count and the reconciliation in one evidence pack |
| Estimable | One journey runner, one fake set, one fixture pack, three assertion helpers, one evidence collector, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a fixed Given, When and Then and a recorded pass or fail in the report |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v2 [E3d]

  Background:
    Given agents "INTAKE" (policy "P2", mode "L1") and "SCREENING" (policy "P2", mode "L1" for MORTGAGE and BKK) are live
    Given the drift rule is a fall of 10 points or more with at least 20 feedback entries in each week

  Scenario: AC1 Per-agent rows for the two-week window (new, D-RCV-60)
    Given the two weeks 2026-12-01 to 2026-12-07 and 2026-12-08 to 2026-12-14 are seeded with runs, feedback and decisions
    When the harness reads GET /api/recovery/agent/v1/admin/agent-metrics for 2026-12-01 to 2026-12-14
    Then every row carries acceptance, override, fallback, latency and cost for its agent, version and segment
    Then "INTAKE" for segment MORTGAGE and BKK shows 140 feedback entries with 119 accepted and acceptance rate 0.8500
    Then "SCREENING" shows state "live" for MORTGAGE and BKK and "Shadow" for every other segment

  Scenario: AC2 One drift alert and one notification (new, D-RCV-60)
    Given "INTAKE" acceptance for MORTGAGE and BKK is 0.8600 for 2026-12-01 to 2026-12-07 and 0.7500 for 2026-12-08 to 2026-12-14
    When the drift check runs for 2026-12-14
    Then one alert of type "DRIFT" for "INTAKE", segment "MORTGAGE/BKK" and date 2026-12-14 holds measured 0.7500 and threshold 0.7600
    Then MSG-P10-006 goes to the holders of RW-COE and RW-RISK
    Then the alert row is read back through the P10 contract and the harness reads no table of rwb-agent

  Scenario: AC3 Tokens and cost reconciled to the runs (new, D-RCV-60)
    Given November 2026 holds 3,100 runs for "INTAKE" with 2,945,000 input tokens and 465,000 output tokens
    When the harness reads the metrics for November 2026 and the runs behind them
    Then the tokens and cost of the month match the sum of the runs, which hold the token counts the endpoint returned on each call
    Then "INTAKE" shows 3,410,000 tokens and cost 170.5000 baht at 0.0500 baht per 1,000 tokens
    Then a month whose daily rows and runs differ shows "not reconciled" with the token difference

  Scenario: AC4 Not enough feedback for a segment (new, D-RCV-60)
    Given "SCREENING" for MORTGAGE and BKK has 12 feedback entries in the week to 2026-12-14
    When the drift check runs for 2026-12-14
    Then no drift alert exists for that agent and segment
    Then the metric row for that segment and week shows "not enough feedback"

  Scenario: AC5 Dates in the wrong order (new, D-RCV-60)
    When the harness reads the metrics from 2026-12-14 to 2026-12-01
    Then the answer is 422 with MSG-GEN-003

  Scenario: AC6 A range that is too long (new, D-RCV-60)
    When the harness reads the metrics from 2026-08-01 to 2026-12-14
    Then the answer is 422 with MSG-GEN-002 naming 1 and 92 days

  Scenario: AC7 The drift check runs twice (new, D-RCV-60)
    Given the DRIFT alert for "INTAKE", "MORTGAGE/BKK" and 2026-12-14 exists
    When the drift check runs a second time for 2026-12-14
    Then no second alert row and no second notification exist

  Scenario: AC8 A role without Platform administration R (new, D-RCV-60)
    Given a test user holds RW-CASEOWN and no Platform administration right
    When that user requests GET /api/recovery/agent/v1/admin/agent-metrics
    Then the answer is 403 with MSG-P4-002

  Scenario: AC9 The override count agrees across services (new, D-RCV-60)
    Given November 2026 holds decisions recorded with the "INTAKE" agent version whose final call differs from the recommendation, each carrying a coded override reason
    When the harness compares every metric row's override count with the decision-log count for the same agent version and month
    Then every count is equal, and the coded reasons carry counts that add up to the override count of the row
```

No legacy acceptance criterion is owned by this story: the nine above are new and test only the integration deliverable, using the legacy values of RWB-E2-031 and no other.

### 8. Business rules

| ID | Rule | Source | AC |
|---|---|---|---|
| BR1 | Acceptance rate = accepted / (accepted + corrected + rejected) of L1 feedback; correction rate = corrected / the same total | agent_feedback.verdict | AC1 |
| BR2 | Override rate = decisions with the agent version where final_call differs from the recommendation / decisions with the agent version; reasons counted from override_reason codes | REQ-APD-005; decision_log_entry.override_reason; CTL-07 | AC1, AC9 |
| BR3 | Drift = acceptance of the last 7 days at least 10 points below the 7 days before, with at least 20 feedback entries in each week | agent_policy.watch_measures | AC2, AC4 |
| BR4 | Token and cost totals come from agent_run; a month is reconciled when the daily rows equal the run sums | REQ-DRI-009; DL25 | AC3 |
| BR5 | One alert per agent, type, segment and business date | agent_alert unique key | AC7 |
| BR6 | A segment is the case product group and region at run time | recovery_case.product_group, recovery_case.region_code | AC1, AC2 |
| BR7 | Only a role with Platform administration R reads the monitor; a role without it is refused before any row is built | Platform administration R | AC8 |

The rules are unchanged by the split. The harness asserts them across the service boundaries and restates none of them in code: the drift points, the minimum feedback, the window, the coded reason list and the mode per segment are seeded data.

### 9. State transitions

None for the case. This story changes no case status and moves no case field; the harness asserts that no status, task or assignment moves because a metric was read or an alert was written.

The story writes agent alerts of type DRIFT and shows each agent's mode as Shadow, live or paused: Shadow (mode SHADOW: runs, fallbacks and evaluation scores, no acceptance), live (mode L1: all measures), paused (mode OFF: history only). The harness asserts the mode it seeded through the configs read and never sets one.

The harness adds a run state of its own only: Not started, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Reads acceptance, override, fallback, latency and cost per agent, version and segment, and opens the override reasons (Platform administration R) |
| RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same measures through the metrics operation only (Platform administration R) |
| RW-RISK | Receives drift alerts; reads the reporting copy of the measures (Reporting R); does not hold Platform administration |
| RW-CASEOWN | Refused at the metrics operation with MSG-P4-002; holds no Platform administration right |
| Integration lead | Agrees the fake set, the clock control, the drift date and the run window with the three service owners |
| QA lead | Owns the seed pack, the evidence format and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-007 | decision_log_entry | agent_version | Read through the P7 decision-log operation |
| DF-DEC-009 | decision_log_entry | recommendation | Read through the P7 decision-log operation |
| DF-DEC-012 | decision_log_entry | final_call | Read through the P7 decision-log operation |
| DF-DEC-013 | decision_log_entry | override_reason | Read through the P7 decision-log operation |
| DF-DEC-016 | decision_log_entry | decided_at | Read through the P7 decision-log operation |
| DF-AGT-037 | agent_run | agent_code | Read through the P10 runs operation |
| DF-AGT-038 | agent_run | agent_version | Read through the P10 runs operation |
| DF-AGT-040 | agent_run | model_version | Read through the P10 runs operation |
| DF-AGT-043 | agent_run | autonomy_mode | Read through the P10 runs and configs operations |
| DF-AGT-046 | agent_run | status | Read through the P10 runs operation |
| DF-AGT-047 | agent_run | fallback | Read through the P10 runs operation |
| DF-AGT-051 | agent_run | latency_ms | Read through the P10 runs operation |
| DF-AGT-052 | agent_run | tokens_in | Read through the P10 runs operation |
| DF-AGT-053 | agent_run | tokens_out | Read through the P10 runs operation |
| DF-AGT-054 | agent_run | cost_thb | Read through the P10 runs operation |
| DF-AGT-056 | agent_run | run_at | Read through the P10 runs operation |
| DF-AGT-059 | agent_run | segment_product_group | Read through the P10 runs operation (rwb-agent sets it at run time) |
| DF-AGT-060 | agent_run | segment_region_code | Read through the P10 runs operation (rwb-agent sets it at run time) |
| DF-AGT-098 | agent_feedback | agent_run_id | Read through the P10 metrics operation |
| DF-AGT-100 | agent_feedback | verdict | Read through the P10 metrics operation |
| DF-AGT-008 | agent_policy | autonomy_mode | Read through the P10 configs operation |
| DF-AGT-009 | agent_policy | segment_product_group | Read through the P10 configs operation |
| DF-AGT-010 | agent_policy | segment_region_code | Read through the P10 configs operation |
| DF-AGT-015 | agent_policy | alert_role | Read through the P10 configs operation |
| DF-AGT-019 | agent_policy | watch_measures | Read through the P10 configs operation |
| DF-AGT-103 to DF-AGT-111 | agent_alert | id, agent_code, alert_type, segment, business_date, measured_value, threshold_value, sent_to_role, sent_at | Read through the P10 metrics operation (rwb-agent writes every alert row, never the harness) |

The harness owns no table in any schema and no schema at all: no table, no view, no migration and no seed table is created by this story. Every field above is read or written through the operation of the service that owns it, and the two writes the legacy story names — the segment on a run and the alert row — are made by rwb-agent in its own schema, never by the harness. Per-service Flyway (DP-15) applies to the services under test, not to the harness: the harness runs no migration and asserts the seeded state through the contracts. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | P10 rwb-agent | Reads the metric rows for the window and for November: acceptance, override, fallback, latency, tokens, cost, feedback count, mode and reconciled flag (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | Reads the runs behind a metric row: agent and agent version, model version, autonomy mode, status, fallback, latency, tokens, cost and segment (AC1, AC3) |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | Reads the policy versions, the modes per segment and the watch measures the drift rule comes from (AC1, AC2, AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | Reads the role and the Platform administration right of the reader, and the RW-CASEOWN refusal (AC8) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Reads the override counts and the coded reasons per agent version and month (AC9) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout, and every call is a read with a key per scenario. The scope check that rwb-agent makes inside its own process is not a path in the Ownership Map, so the harness seeds it through the role and scope of the rwb-access fake (12.8) and reads the resulting answer through the P10 operation instead of calling an access path.

#### 12.3 Events published

None. The harness publishes no Kafka event on a production topic; its seed goes in through the services' own operations and its evidence goes to the release record through the pipeline.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Closes the run window of a seeded run and gives the run ID, the status and the fallback flag before the metrics read (DP-10) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | Asserts that the override decisions reached the shared topic inside the run window, alongside the ledger read of 12.2 (DP-03) |

The harness consumes with its own consumer group and never reads a producer's outbox, inbox or schema.

#### 12.5 Workflows and activities

None built. The harness starts no workflow and adds no activity. The drift check it triggers and observes runs in rwb-agent; the agent call to the Enterprise AI private endpoint, the guardrail check and the writing of the alert row belong to RWB-P10-E2031-APP.

#### 12.6 Schedules

None added. Observed: the drift check as a Temporal Schedule in rwb-agent — the legacy JOB-15 "agentDrift" step moved to the owning service under DP-10 — and JOB-15 Reporting extract in rwb-reporting at 01:30, which is the reporting copy the monitor's daily rows come from. The harness triggers the drift check for a fixed business date through the schedule's own trigger and adds no schedule of its own.

#### 12.7 Tables owned

None. The harness owns no table in any schema and no schema of its own; it reads and writes through the operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-agent | The three P10 operations of 12.2 | OpenAPI of P10 | The metric rows for 2026-12-01 to 2026-12-14 and for November 2026, the runs behind them, the configs with the P1 and P2 versions and the modes per segment, 422 MSG-GEN-003 and 422 MSG-GEN-002, 403 MSG-P4-002, the DRIFT alert row read back, and the "not reconciled" month with its token difference; keeps the request journal for the window and ordering assertions |
| WireMock rwb-access | The P4 session operation | OpenAPI of P4 | The role, the scope and the Platform administration right of the reader, and the RW-CASEOWN answer with no Platform administration right (MSG-P4-002) |
| WireMock rwb-decision | `GET /api/recovery/decision/v1/decision-log` | OpenAPI of P7 | The override counts and coded reasons per agent version and month, matching the runs of the seed, so AC9 can pass and X10 can be reproduced on purpose |
| Clock control | The harness clock | A harness asset, not a service contract | Fixes "today" and the drift date at 2026-12-14 and moves the two weeks of the seed into the past, so a drift check for 2026-12-14 always compares the same two weeks |

Each fake is replaced by the real service as its integration dependency lands, without a change to the scenarios. Not specified in the source documents (GAP-0413; ASM-0588): the fake set, the concrete fixture values, the clock control, the harness environment and the evidence format.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 5 consumed, one hop on the owner's base with the 2 s timeout; the P4 session operation is called against the fake only and is not a production path of this story |
| Kafka | 2 events consumed on `rwb.agent.events.v1` and `rwb.decision-record.v1`; none published on a production topic |
| Temporal | Observed only: the drift check as a Temporal Schedule in rwb-agent, and JOB-15 Reporting extract in rwb-reporting at 01:30; no workflow, activity or schedule added |
| File | None |

### 13. Solution plan

**Package.** Folder `integration/recovery-agent-monitor` in the ACE repository, package `<ACE base package>.recovery.integration.agentmonitor`. Not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | The override counts are read through rwb-decision's contract and the `DecisionRecorded` event is read on the shared topic; the harness never reads a decision table |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The mode per segment, the verdict labels and the coded override reasons are seeded reference data, never values in the harness code |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | The drift check is the Temporal Schedule in rwb-agent that the legacy JOB-15 step became; the harness triggers it for 2026-12-14 and observes it, and adds no workflow and no schedule |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 uses the owner's base, so the harness never calls a monolith base |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The harness runs no migration and reads no schema; it asserts that each service migrates its own schema by reading the seeded state through the contracts only |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the SCR-46 reader uses, on the same bases |

The platform H dependencies in the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the three I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date and holds the run lock |
| FakeRegistry | Configuration | WireMock mappings for rwb-agent, rwb-access and rwb-decision, one set per contract version, plus the clock control that fixes "today" and 2026-12-14 |
| MonitorFixturePack | Data | The two agents and their policies, the two weeks of runs, feedback and decisions, the November 2026 runs and tokens, the 12-feedback week, the filter fixtures and the RW-CASEOWN user |
| MetricAssertion | Service | Compares each metric row with the fixture: acceptance 0.8500, 140 feedback and 119 accepted for INTAKE MORTGAGE/BKK, the mode per segment, and the override count against the decision-log count |
| DriftAssertion | Service | Triggers the drift check for 2026-12-14, asserts one DRIFT alert with measured 0.7500 and threshold 0.7600, the MSG-P10-006 recipients, the "not enough feedback" week and the second run that adds nothing |
| CostAssertion | Service | Sums the runs of November 2026, compares them with the monthly row at 3,410,000 tokens and 170.5000 baht at 0.0500 baht per 1,000 tokens, and reads the not-reconciled month with its token difference |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with the metric rows, the runs, the override counts, the alert row, the notification, the reconciliation and the message of each refusal |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached |

**Environment and test data.** SIT, the wave 2 harness profile, the fixed clock at 2026-12-14, synthetic agents and synthetic segments only. The seeded values are the legacy section 7 Background, the two weeks of section 3, the 12-feedback week and the November 2026 token counts; no other value is added. Not specified in the source documents (GAP-0413; ASM-0588): the environment, the seed pack, the clock control and the evidence format.

**Build steps**

1. Write the MonitorFixturePack with the Background, the two agents and their policies, the two weeks of runs, feedback and decisions, the November 2026 runs and the 12-feedback week; test that a bad seed stops the run (X7).
2. Write the FakeRegistry with the three WireMock mapping sets and the clock control fixing 2026-12-14, with the modes, the verdict labels and the coded override reasons loaded from files, and fail on a version mismatch (X8).
3. Write JourneyRunner for AC1: the configs read, the metrics read for 2026-12-01 to 2026-12-14, the per-agent and per-segment rows, the 140 feedback and 119 accepted at 0.8500, and the SCREENING states.
4. Add AC9 with the runs read and the decision-log counts, sweeping every metric row of the two months against the same agent version and month.
5. Add AC2 and AC7 with the drift check for 2026-12-14 run twice: one DRIFT alert, measured 0.7500, threshold 0.7600, MSG-P10-006 to the holders of RW-COE and RW-RISK, and no second row or notification.
6. Add AC4, AC5, AC6 and AC8 with the 12-feedback week, the two 422s naming the fields and the 1 and 92 days, and the 403 with MSG-P4-002.
7. Add AC3 with the November reconciliation and the not-reconciled month, then write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record and rerun the nine scenarios on the release build.

**Feature switch.** `rwb.agent.monitor-v2` is on in the harness profile, as the legacy story sets it. Off, the monitor answers runs and fallbacks only and the drift check is skipped, and the harness reports the journey as not applicable rather than as passed. The harness itself is a pipeline stage selected by the run profile, not by a business flag.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all nine owned scenarios, and each fake has been replaced by the real service where its I story has landed in SIT. The fixture pack, the clock control and the evidence sign-off wait for the values of the gap and assumption rows cited in sections 3, 12.8 and 13.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-006 | Acceptance falls by 10 points or more | {agent} acceptance for {segment} fell from {from} to {to} percent in the week to {date}. |
| MSG-GEN-003 | Filter dates in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-002 | Filter range above 92 days | {field} must be between {min} and {max}. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The harness asserts these messages and never rewrites them. Its own report text — including the state "not enough feedback" and the state "not reconciled" — is for the release team and is not part of the message standard.

### 15. Screens and states

SCR-46 Agent monitor, from the Administration menu, states per agent and segment: Shadow (mode SHADOW: runs, fallbacks and evaluation scores, no acceptance), live (mode L1: all measures) and paused (mode OFF: history only). Common states: loading (skeleton rows), empty ("No agent runs in this period.") and error (message at the top). The reader filters by agent, segment and dates — the range limit is 92 days — opens a row to see the runs behind it, and opens the override reasons per agent and month.

No screen is built by this story. The harness drives the operations behind those states and asserts them through the contracts: a live segment with all measures, a Shadow segment with no acceptance, a week with too little feedback, a month that does not reconcile, and the three refusals. Not specified in the source documents (GAP-0413; ASM-0588): the harness environment, its seed pack, its fixed clock and its evidence format. The screen and its states belong to RWB-P10-E2031-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-031-08-ITG | Access, BR7 | Component | RW-CASEOWN calls the metrics operation; refused with MSG-P4-002 |
| TC-E2-031-01-ITG | AC1, AC9, BR1, BR2, BR6, BR7 | Integration | 2026-12-01 to 2026-12-14; INTAKE MORTGAGE/BKK 140 feedback, 119 accepted; the override counts against the decision log |
| TC-E2-031-02-ITG | AC2, BR3, BR5 | Integration | Acceptance 0.8600 then 0.7500, check for 2026-12-14 |
| TC-E2-031-03-ITG | AC3, BR4 | Integration | November 2026: 3,100 runs, 2,945,000 and 465,000 tokens |
| TC-E2-031-04-ITG | AC4, BR3 | Integration | SCREENING MORTGAGE/BKK, 12 feedback entries in the week |
| TC-E2-031-05-ITG | AC5 | Integration | From 2026-12-14 to 2026-12-01 |
| TC-E2-031-06-ITG | AC6 | Integration | From 2026-08-01 to 2026-12-14, over the 92-day limit |
| TC-E2-031-07-ITG | AC7, BR5 | Integration | The drift check run a second time for 2026-12-14 |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the legacy story, run across the three contracts and the clock control. The app stories keep the unit and component copies of the same cases. TC-E2-031-01-ITG carries AC9 as well, because the cross-service agreement is asserted on the same two-week window and the same month. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the drift points, the minimum feedback, the window, the 92-day filter limit and the alert recipients are policy and reference data in the seed pack, never values in the harness.
- No personal data in events, workflow inputs, logs, evidence or the reporting copy. The metrics hold counts, rates, times and amounts; the seed holds synthetic agents and synthetic segments only.
- No read of another service's schemas: the override figures come through the P7 contract and the metric rows through the P10 contract, and the harness runs no migration and owns no schema.
- The harness never changes a policy or an autonomy level: it seeds them, reads them back through the configs operation and asserts the mode it did not set.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.
- The harness never runs against UAT or production, and a value that must change changes in the seed pack through a reviewed change, never by an exception in a scenario.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched | Business Requirements Program, section 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | R-UNI-40 | TC-E2-031-08-ITG, TC-E2-031-01-ITG, TC-E2-031-02-ITG, TC-E2-031-03-ITG, TC-E2-031-04-ITG, TC-E2-031-05-ITG, TC-E2-031-06-ITG, TC-E2-031-07-ITG |
| REQ-APD-005 | An override needs a coded reason, reported monthly | Business Requirements Program, section 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-01-ITG |

### 19. Out of scope

- Drift detection that raises a decision with an owner and a date (FEAT-AGT-13, Epic 3).
- Changing an autonomy level from SCR-46 (FEAT-AGT-12, Epic 3; FEAT-AGT-15, Epic 8).
- Agent risk review at the committee (FEAT-AGT-16, Epic 8).
- Production code of any service in the journey: the metrics, the drift check and the alert row of rwb-agent, the session and the right of rwb-access, the ledger read of rwb-decision, and the SCR-46 screen belong to their own stories.

The harness, the fakes and the evidence pack cover the four items above only as a caller and a consumer would see them; building any of them is out of scope for this story.
