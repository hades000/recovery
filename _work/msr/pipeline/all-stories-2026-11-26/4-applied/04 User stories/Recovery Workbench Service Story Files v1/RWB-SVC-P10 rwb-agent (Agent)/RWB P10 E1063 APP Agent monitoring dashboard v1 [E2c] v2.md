# RWB-P10-E1063-APP Agent monitoring dashboard v1 [E2c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1063-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-063 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1058-APP |
| Depends on (build) | RWB-P10-E1063-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-E1058-APP, RWB-P10-E1061-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P2-E1007-CON |
| Integration dependencies | None |
| External dependencies | RWB-P10-E1063-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to REQ-DRI-009) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E1-063 for rwb-agent. Two decisions change the shape of the legacy story and are applied here explicitly. **DP-17 (no data lake):** there is no data lake in Architecture v5 (slide 37; ADR-018), so the legacy data-lake write of section 4 step 4, the legacy table `agent_run_daily`, the nightly copy path of RWB-E1-014 and the interfaces INT-19 and INT-20 are removed. Legacy AC3 becomes the reporting feed built from `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` into rwb-reporting, with no lake write anywhere, and the count check of AC3 now holds the reporting feed for the business date instead of holding a lake publish. **DP-10 (Quartz to Temporal):** the legacy Quartz entry of JOB-15 for the agent step becomes the Temporal Schedule `AgentRunDailyRollup` in namespace `rwb-recovery` on task queue `rwb-agent`, with the business date as its input, the 01:30 Asia/Bangkok time of the legacy job, overlap policy SKIP, the one-business-date catch-up window and the rerun behaviour of AC4; the legacy job table is not read. The metric reads are served on the base `/api/recovery/agent/v1` (DP-13), the rows stay in schema `rwb_agent` (DP-01), the cost cap and the alert role are read through the rwb-case parameters contract (DP-06) and the lists through the reference-data contract (DP-07), the alert is dispatched through the outbox with retry (DP-09), the dashboard read is reached through the gateway-bff route (DP-19), and the one new table arrives with the service's own Flyway sequence (DP-15). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P10-E1063-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer (RW-RISK)**, I want **the agent monitoring dashboard built inside rwb-agent - one aggregate per agent, policy version, prompt version, model version and business date with runs, answered, fallback, median and 95th percentile latency, tokens, cost and the latest evaluation score, served on `/api/recovery/agent/v1/admin/agent-metrics` and read through the gateway-bff route; a nightly Temporal Schedule `AgentRunDailyRollup` that closes the business date, holds it when its row count or run sum does not match, and raises one cost alert with MSG-P10-004 when an agent's cost on a business date is above the cap it reads through the rwb-case parameters contract; and a reporting feed built from `rwb.agent.AgentRunCompleted.v1` into rwb-reporting with no data lake copy anywhere**, so that **every agent is watched from its first shadow run, an agent that falls back on one case in five or spends twice its budget is seen on the first business date rather than at the L1 review, and the same figures are read by the steering measures of rwb-reporting without a lake table that no longer exists**.

### 2. Business rationale

An agent in shadow that times out on one case in five, or that spends twice its budget, must be seen in the first week, not at the L1 review. The legacy story copied daily agent run figures to the data lake with the nightly reporting extract, matched by row count (REQ-DRI-009), so a Power BI dashboard read the copy and not the live tables, and a daily check sent an alert when the cost of an agent on a business date was above its policy limit.

Architecture v5 removes the data lake and the Power BI feed (slide 37: INT-19 and INT-20 removed; ADR-018), and with them the copy the legacy dashboard read. The reason is stated in the decision: reports come from rwb-reporting, built from events, and no service writes a lake table. So the behaviour of this story is kept and its plumbing changes:

- The daily aggregate is computed and served by rwb-agent from its own rows, `agent_run`, `agent_evaluation` and `agent_policy`, in schema `rwb_agent`, on `GET /api/recovery/agent/v1/admin/agent-metrics` (DP-01, DP-13; BR1, BR10).
- The reporting feed is `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1`, published by the run path of RWB-P10-E1058-APP through the outbox relay, and consumed by rwb-reporting, which builds its measures from it; this story writes no lake table and no extract, and the count check of AC3 holds the feed for the business date instead of holding a lake publish (DP-17; BR2, BR7).
- The nightly trigger is the Temporal Schedule `AgentRunDailyRollup` in namespace `rwb-recovery` on task queue `rwb-agent`, at the 01:30 Asia/Bangkok time of the legacy JOB-15 agent step, with overlap policy SKIP, the one-business-date catch-up window and a rerun for any business date; the legacy job table, its `GET /admin/jobs` admin and the Quartz entry are not read (DP-10; BR8).
- The cost cap and the alert role are values of the approved `agent_policy` row, read at run time through the rwb-case parameters contract and never written in code (DP-06; BR3).
- The alert message MSG-P10-004 leaves through the rwb-comms notification path, its row in `agent_alert` carrying `sent_at` empty until the outbox relay succeeds (DP-09; BR6, BR9).
- The dashboard is reached through the gateway-bff route, so no screen calls rwb-agent directly (DP-19).

The cross-service behaviour of this key - that the published measure of rwb-reporting agrees with the aggregate rwb-agent serves, that the notification really leaves rwb-comms, and that the route returns the aggregate unchanged - is proved by RWB-ITG-E1063-ITG, which is why this story carries no integration dependency (I = None) and claims none. This story builds and unit-tests its own deliverables against the published contracts and their fakes, keeps the seven legacy acceptance criteria AC1 to AC7 word for word with their origin tags, and adapts only the two places where the legacy text names the data lake or the retired job admin (AC3 and AC4's `agent_run_daily`; section 7, Target reading).

### 3. Preconditions

- RWB-P10-E1058-APP is done: `agent_run`, `agent_evaluation` and `agent_policy` exist in `rwb_agent` with cost, latency, status and fallback per run, the run path publishes EV-28 through the outbox, and an agent can run in mode SHADOW.
- RWB-P10-E1061-CON is published: the shape of the evaluation score the aggregate carries for the latest DONE evaluation per agent and version.
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters client library and the reference-data client library with parameterized schema names. RWB-PLT-E1044-CON is published: the per-service Flyway sequence. RWB-PLT-TE006-CON is published: the outbox and inbox library, the relay and the `.dlt` rule. RWB-PLT-E1071-CON is published: the Temporal workflow kit and the Schedule registration contract with namespace `rwb-recovery`. RWB-PLT-N001-CON is published: the gateway-bff route contract and its stub.
- The `rwb_agent` schema baseline exists with the standard record columns and the Flyway history table of the service; `agent_alert` is created by this story's own migration.
- The rwb-case contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: the parameters contract for `agent_policy.daily_cost_cap_thb` and `agent_policy.alert_role`, and `GET /api/recovery/case/v1/admin/lists/{listCode}` for LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT.
- The rwb-reporting contract of RWB-P9-E1055-CON is published for the published measures: `GET /api/recovery/reporting/v1/reports/measures` returns the measure rows with their business date, their definition and their value; the measure "Agent fallback rate" is named by FSD P10 v3 A2.6.1.
- The rwb-comms contract of RWB-P6-E1063-APP is published for the notification path: it takes one notice request for the alert role and returns an accepted reference or a refusal. Its operation is Not specified in the source documents (GAP-0616; ASM-0892).
- Each approved agent policy holds `daily_cost_cap_thb` (assumed 2,000 baht for INTAKE and SCREENING; DL33) and `alert_role` (assumed RW-COE; DL33), read through the parameters contract and never from code.
- RW-BIANAL maintains the published measure set with rwb-reporting; RW-RISK and RW-COE hold the reporting read and receive the alerts; RW-PLATADM may rerun the rollup for a business date.
- The legacy precondition "RWB-E1-014 is done: the nightly copy path to the data lake exists" is removed: RWB-E1-014 is retired under §R6 and DP-17, and no copy path exists in the target (GAP-0616; ASM-0889).
- The schedule name `AgentRunDailyRollup` is the name this story gives the Schedule, because no source names it: Not specified in the source documents (GAP-0616; ASM-0888).
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. `AgentRunDailyRollup` fires at 01:30 Asia/Bangkok for the previous business date, or is started by hand for any business date that RW-PLATADM names; the workflow ID is the business date, so a rerun for the same date joins the same workflow identity and never duplicates the day (DP-10; BR8; AC4).
2. `aggregateAgentRuns` reads the `agent_run` rows of the date and groups them by agent, policy version, prompt version and model version: runs, answered, fallback, median and 95th percentile latency, tokens and cost (BR1, BR5; AC1).
3. It joins the latest DONE `agent_evaluation` score of each agent and version, read through the shape published by RWB-P10-E1061-CON (AC1).
4. It writes the daily rows of the date for the feed and the dashboard and checks that two facts agree: the number of daily rows equals the number of agent and version groups with runs on the date, and the sum of runs in the daily rows equals the count of `agent_run` rows on the date. A disagreement holds the date: the previous published date stays visible, the rollup run ends failed and the data steward is alerted (BR2; AC3).
5. `raiseCostAlerts` compares the cost of each agent on the date with `daily_cost_cap_thb` of its policy, read through the parameters contract, and applies the strict greater-than rule: cost equal to the cap raises nothing (DP-06; BR3; AC2, AC6).
6. For each breach it writes one `agent_alert` row of type "COST_CAP" with the business date, `measured_value`, `threshold_value`, `segment` and `sent_to_role`, on the unique key of agent, type, segment and business date, so a rerun adds no second row (BR4; AC2, AC4).
7. `dispatchAgentAlerts` sends MSG-P10-004 through the rwb-comms notification path for the alert role and for RW-RISK, and writes the outbox row in the same transaction; `sent_at` stays empty until the relay confirms the send (DP-09; BR6, BR9; AC2, AC7).
8. A business date with no runs for an agent that holds an approved policy still produces its daily row with runs 0 and cost 0.0000 and raises no alert (AC5).
9. RW-RISK opens the dashboard through the gateway-bff route: `GET /api/recovery/agent/v1/admin/agent-metrics` with query agent, segment, version, from and to answers one element per agent, version and business date; each element shows runs, fallback rate at four decimals, median and 95th percentile latency, cost and the latest evaluation score, and acceptance and override show "no L1 runs" because no agent runs at L1 in Epic 1 (DP-19; AC1).
10. The published measures are read through `GET /api/recovery/reporting/v1/reports/measures`, one hop and within the 2 s budget, so the dashboard shows the measure rwb-reporting published from the same events and not a second calculation (DP-11, DP-17; AC1).
11. A rerun for a date that is already complete rewrites the same daily rows for that date in one transaction, raises no second alert and sends no second notification (AC4).
12. The story writes no lake table, no lake credential and no extract file: the only rows it writes are `agent_alert` and the daily aggregate rows of the date in `rwb_agent`, and the reporting feed is the EV-28 topic that RWB-P10-E1058-APP already publishes (DP-17; section 17).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The row count or the run sum of the date does not match the source, or the reporting feed cannot be built from the events of the date | The feed is held for the date; the previous date stays visible on the dashboard; the data steward and the platform administrator are alerted; the rollup run reports failed | None to a user | AC3 |
| X2 | The rollup runs again for the same business date | The rows for the date are replaced, not added; no second alert and no second notification | None to a user | AC4 |
| X3 | An agent has no runs on the date | One daily row with runs 0 and cost 0.0000; no cost alert | None to a user | AC5 |
| X4 | The cost equals the cap exactly | No alert; an alert is sent only when the cost is above the cap | None to a user | AC6 |
| X5 | The notification path is unavailable | The `agent_alert` row is kept with `sent_at` empty and retried by the outbox relay (R-UNI-33, R-UNI-35) | None to a user | AC7 |
| X6 | A role without the reporting read opens the dashboard | The route refuses the read with 403 and the refusal is proved by the access slice of this key, RWB-P4-E1063-APP, not by a criterion of this story | MSG-P4-002 | TC-E1-063-08 |
| X7 | The parameters contract does not answer inside the 2 s budget, or the approved policy row holds no `daily_cost_cap_thb` | No alert is raised for the date and none is raised with a code default; the missing value is named on the run record and the run ends failed; RW-PLATADM starts it again | None to a user | AC2 |
| X8 | The rwb-reporting measures read fails or answers beyond the 2 s budget | The dashboard still shows the aggregate rwb-agent serves for the date, marks the published measure as unavailable and never falls back to reading a measure table | None to a user | AC1 |
| X9 | The migration `V10_006__agent_alert.sql` fails in the service's Flyway sequence | The new version does not start and the version in force keeps serving; no run and no alert is written | None | AC3 |
| X10 | The Schedule registration is rejected by the namespace, or the Schedule does not fire for a business date | No `AgentRunDailyRollup` run exists for the date; the run is started by hand for that date through the same workflow ID and the registration is corrected by the deployment of RWB-P10-E1063-OPS | None | AC4 |

X1 to X6 are the legacy exception paths of RWB-E1-063 carried onto the service; X7 to X10 are the failures that appear when the reads leave the service, when the parameters become a contract and when the Schedule replaces the Quartz entry. X6 is not reached by a criterion of this story: it is proved by the legacy test case TC-E1-063-08 and by the access slice RWB-P4-E1063-APP, and the message is kept so a reader finds the legacy set complete.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the platform contract stories, the published P3, P9 and P6 contracts with their fakes, and the in-lane story RWB-P10-E1058-APP; it owns its own table and its own Schedule |
| Negotiable | The package layout, the component and activity names, the export column order and the paging of the read are design; the agents, the policy and prompt versions, the business date, the counts, the cap, the alert role, the message IDs and the time of the schedule are fixed by the legacy story |
| Valuable | Shows fallbacks and spend per agent from the first shadow run and keeps the steering measures fed without a data lake |
| Estimable | One table, one migration, one operation, one Schedule with three activities, six components, four contract clients and four fakes |
| Small | In the legacy estimate one developer and one BI analyst for one week; the same size here, with the BI page replaced by the served aggregate |
| Testable | Each of the seven criteria of section 7 is one automated test on an observable: a REST answer, a stored row, a daily row, an alert row, a sent timestamp, a held date or a scan of the source |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v1 [E2c]

  Background:
    Given agents "INTAKE" (policy "P1", prompt "PR1") and "SCREENING" (policy "P1", prompt "PR1") run in shadow
    Given on business date 2026-12-01 "INTAKE" has 120 runs, 9 with fallback, cost 1,840.0000 baht
    Given on 2026-12-01 "SCREENING" has 150 runs, 21 with fallback, cost 2,310.5000 baht
    Given both policies have daily_cost_cap_thb 2,000 and alert_role "RW-COE"

  Scenario: AC1 Per agent (legacy RWB-E1-063 AC1)
    Given the rwb-reporting contract mock returns the published measure "Agent fallback rate" for 2026-12-01
    Given two agents in shadow
    When the dashboard opens for 2026-12-01
    Then each agent shows runs, fallback rate, median and 95th percentile latency, cost and the latest evaluation score by policy and prompt version
    Then "INTAKE" shows 120 runs and fallback rate 0.0750
    Then acceptance and override show "no L1 runs" for both agents, because no agent runs at L1 in Epic 1

  Scenario: AC2 Alert (legacy RWB-E1-063 AC2)
    Given the rwb-case parameters contract mock returns daily_cost_cap_thb 2,000 and alert_role "RW-COE"
    Given cost above the daily parameter for "SCREENING"
    When JOB-15 completes for 2026-12-01
    Then one agent alert row exists for "SCREENING", type "COST_CAP", date 2026-12-01, measured 2,310.5000 and threshold 2,000
    Then the system sends MSG-P10-004 to the holders of RW-COE and RW-RISK through the notification path
    Then no alert exists for "INTAKE"

  Scenario: AC3 A copy that does not match is held (legacy RWB-E1-063 AC3)
    Given the rwb-comms contract mock returns an accepted reference for the data steward alert for 2026-12-01
    Given the reporting feed for 2026-12-01 stores 1 row for 2 agent and version groups
    When the count check runs
    Then the system holds the publish for 2026-12-01 and the report shows 2026-11-30
    Then the rollup run reports failed and the data steward is alerted

  Scenario: AC4 A rerun for the same date (legacy RWB-E1-063 AC4)
    Given the rwb-case parameters contract mock returns daily_cost_cap_thb 2,000 and alert_role "RW-COE"
    Given JOB-15 completed for 2026-12-01 and sent the "SCREENING" alert
    When RW-PLATADM reruns JOB-15 for 2026-12-01
    Then the daily rollup rows hold the same 2 rows for 2026-12-01
    Then no second alert row or notification exists

  Scenario: AC5 An agent with no runs (legacy RWB-E1-063 AC5)
    Given the rwb-case parameters contract mock returns daily_cost_cap_thb 2,000 for "EXTRACT"
    Given agent "EXTRACT" has an approved policy and no runs on 2026-12-01
    When JOB-15 completes for 2026-12-01
    Then "EXTRACT" shows runs 0 and cost 0.0000 for 2026-12-01 and no alert

  Scenario: AC6 Cost equal to the cap (legacy RWB-E1-063 AC6)
    Given the rwb-case parameters contract mock returns daily_cost_cap_thb 2,000 for "INTAKE"
    Given "INTAKE" cost is 2,000.0000 baht on 2026-12-02
    When JOB-15 completes for 2026-12-02
    Then no cost alert exists for "INTAKE" on 2026-12-02

  Scenario: AC7 The notification path is down (legacy RWB-E1-063 AC7)
    Given the rwb-comms contract mock returns 503 for the notification of the "SCREENING" alert
    Given the P6 notification interface is unavailable at 01:40
    When the "SCREENING" alert is raised
    Then the system keeps the alert row with sent_at empty
    Then the system sends it when the outbox sender succeeds (R-UNI-33, R-UNI-35)
```

**Target reading.** The agents, their policy and prompt versions, the business dates 2026-12-01 and 2026-12-02, the counts 120, 9, 150 and 21, the fallback rate 0.0750, the costs 1,840.0000, 2,310.5000 and 2,000.0000, the cap 2,000, the alert role "RW-COE", the alert type "COST_CAP", the measured and threshold values 2,310.5000 and 2,000, the group and row counts 1 and 2, the previous date 2026-11-30, the time 01:40, the rules R-UNI-33 and R-UNI-35 and the message IDs are the legacy values of RWB-E1-063, copied character for character; the seven scenario titles and every legacy Given, When and Then are kept, and each scenario carries the origin tag of its legacy criterion. Each scenario gained one inserted Given, `Given the <owner> contract mock returns <x>`, because the criterion reads across a service boundary: AC1 reads the published measure of rwb-reporting, AC2, AC4, AC5 and AC6 read the cost cap and the alert role through the parameters contract of rwb-case, and AC3 and AC7 read the notification path of rwb-comms. Nothing the service owns - its own runs, evaluations, alerts and daily rows - is mocked.

Three legacy statements are adapted, all of them because the target removes the object they name, and each carries the same values as before. **AC3:** the legacy sentence "the data lake write for 2026-12-01 stores 1 row for 2 agent and version groups" becomes "the reporting feed for 2026-12-01 stores 1 row for 2 agent and version groups"; the hold, the previous date 2026-11-30 and the alert to the data steward are unchanged; the legacy third Then, "the step reports failed in GET /admin/jobs", becomes "the rollup run reports failed", because the shared job table and its admin read are retired with the Quartz entries (DP-10) and the run is read from the Schedule's own run history. **AC4:** the lake table `agent_run_daily` becomes "the daily rollup rows", with the same 2 rows and the same single alert. **Section 4 step 4 and the legacy BR1** keep the row-count and run-sum check on the feed instead of on the lake copy. Everything else is the legacy behaviour: the aggregate per agent and version of section 4 step 2, the latest DONE evaluation score of step 3, the strict greater-than rule of X4, the unique key of BR4, the fallback rate at four decimals of BR5 and the 15-minute alerting target of BR6.

The legacy in-process `AgentRunExtractSource` and its two methods become the Temporal workflow and its three activities behind the workflow kit of RWB-PLT-E1071-CON (DP-10), the legacy Spring Batch step becomes `aggregateAgentRuns`, and the legacy `POST /admin/jobs/{jobId}/rerun` becomes a manual start of the same workflow for the business date, so a rerun keeps the legacy semantics: replace by date, no second alert. The lake write, its credential and its extract leave the story with DP-17 (GAP-0616; ASM-0889).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The dashboard reads the aggregate rwb-agent serves from its own rows - `agent_run`, `agent_evaluation` and `agent_policy` in `rwb_agent` - and the published measure of rwb-reporting; it never reads a table of another service and there is no data lake copy (DP-17) | REQ-DRI-009; DP-01; DP-17; legacy BR1 |
| BR2 | A business date is published to the reporting feed only when the number of its daily rows and the sum of its runs match the source | REQ-DRI-009; DL25 (zero tolerance); legacy BR2 |
| BR3 | A cost alert is raised when the cost of an agent on a business date is above `agent_policy.daily_cost_cap_thb` (2,000 baht, assumed; DL33), read through the parameters contract at run time | agent_policy.daily_cost_cap_thb (DF-AGT-013, read through DP-06); legacy BR3 |
| BR4 | One alert per agent, type, segment and business date | `agent_alert` unique key (DF-AGT-103 to DF-AGT-111); R-UNI-40; legacy BR4 |
| BR5 | Fallback rate = runs with fallback / runs, four decimals | `agent_run.fallback` (DF-AGT-047); legacy BR5 |
| BR6 | Alerts go to the policy alert role and to RW-RISK within 15 minutes of the end of the rollup (target, DL11) | `agent_policy.alert_role` (DF-AGT-015); NFR-068; legacy BR6 |
| BR7 | No data lake exists: the reporting feed is built from `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` into rwb-reporting, this story writes no lake table, no extract and no lake credential, and INT-19 and INT-20 are not called | DP-17; ADR-018; Arch v5 slide 37 |
| BR8 | The nightly rollup is the Temporal Schedule `AgentRunDailyRollup` in namespace `rwb-recovery` on task queue `rwb-agent`, with the business date as its input, overlap policy SKIP and the one-business-date catch-up window; the legacy job table, its admin read and the Quartz entry are not used | DP-10; Arch v5 slides 31 and 44; ASM-0888 |
| BR9 | An alert is kept with `sent_at` empty until the notification path accepts it, and the outbox relay retries it with the `.dlt` route on a permanent failure | DP-09; R-UNI-33; R-UNI-35 |
| BR10 | This story writes one table of its own, `agent_alert`, and the daily aggregate rows of the business date in `rwb_agent`, and creates its table by `V10_006__agent_alert.sql` in the rwb-agent Flyway sequence | DP-01; DP-15; Ownership Map (P10 owns `agent_alert`) |
| BR11 | One aggregate shape serves the metric read and the rollup: agent, policy version, prompt version, model version and business date, with runs, answered, fallback, fallback rate, latency p50, latency p95, tokens, cost and the latest evaluation score | TSD P10 Agent runtime v2 T-A.2 API-P10-009; legacy section 4 step 2 |

### 9. State transitions

The state of the alert of one agent, type, segment and business date:

| From | Event | Condition | To |
|---|---|---|---|
| None | The rollup raises a cost alert | Cost above the cap | One `agent_alert` row with `sent_at` empty (DF-AGT-111) |
| None | The rollup evaluates the cost | Cost equal to or below the cap | No row |
| `sent_at` empty | The outbox relay confirms the send through rwb-comms | The notification path accepts the message | `sent_at` set |
| `sent_at` empty | The relay fails | A 5xx or a timeout | `sent_at` stays empty and the message is retried; a permanent failure goes to the `.dlt` topic with an alert |
| Any | A rerun for the same business date | The unique key of agent, type, segment and date already holds the row | The row is kept, no second row and no second notification |

The state of a business date of the feed and of the rollup run:

| From | Event | Condition | To |
|---|---|---|---|
| None | The Schedule fires, or RW-PLATADM starts the workflow for a date | No rows for the date | RUNNING |
| RUNNING | The aggregate is written and the count check passes | Daily rows and run sum match the source | COMPLETE, the date is published and the dashboard shows it |
| RUNNING | The count check fails | One row for two groups, or a run sum that differs | HELD; the previous date stays visible; the run reports failed; the data steward is alerted |
| HELD | A rerun for the same date | The source is corrected | COMPLETE, with the rows of the date replaced |

No case state transition. This story does not change a case status and touches no case of record. It writes one alert row per agent, type, segment and date in `rwb_agent` and the daily aggregate rows of the date, and it sends notices to roles.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RISK, risk and model risk officer | Reads the dashboard and the published measures; receives the alerts |
| RW-COE, centre of excellence analyst | Reads the dashboard and the published measures; receives the alerts as the policy alert role |
| RW-BIANAL, Reporting and BI analyst | Maintains the published measure set with rwb-reporting; reads the dashboard |
| RW-PLATADM, platform administrator | Starts or reruns the rollup for any business date through the same workflow ID; reads the run record |
| RW-DATASTEW, data steward and data product owner | Receives the count mismatch alert of a held date |
| rwb-agent service identity (the rwb-agent login, DP-02) | Runs the rollup, writes `agent_alert` and the daily rows in `rwb_agent`, reads its own tables, calls the parameters and reference-data contracts of rwb-case, the measures of rwb-reporting and the notification path of rwb-comms |
| rwb-reporting (P9) | Owns the measure definitions and the published measures, and builds its projections from `rwb.agent.events.v1` |
| rwb-comms (P6) | Owns the notification path and the delivery of MSG-P10-004; its slice of this key is RWB-P6-E1063-APP |
| rwb-case (P3) | Owns the parameter values and the reference lists, read through its contracts |
| No role | Reads `rwb_case`, `rwb_reporting` or any other service's schema, edits an `agent_run` or `agent_evaluation` row, or reads production data |

The login of the service is Not specified in the source documents (GAP-0616; ASM-0869); the story names it "the rwb-agent login (DP-02)" until it is agreed. Approval levels: no delegation of authority level applies; the approval of a policy version and its cap is the Rules and parameters A right of RWB-P10-E1058-APP, as in the legacy story.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-037, DF-AGT-038, DF-AGT-039, DF-AGT-040 | agent_run | agent_code, agent_version, prompt_version, model_version | Read |
| DF-AGT-046, DF-AGT-047 | agent_run | status, fallback | Read |
| DF-AGT-051, DF-AGT-052, DF-AGT-053, DF-AGT-054 | agent_run | latency_ms, tokens_in, tokens_out, cost_thb | Read |
| DF-AGT-056 | agent_run | run_at | Read, for the business date of the run |
| DF-AGT-002, DF-AGT-003 | agent_policy | agent_code, policy_version | Read |
| DF-AGT-013, DF-AGT-015 | agent_policy | daily_cost_cap_thb, alert_role | Read through the parameters contract at run time (DP-06) |
| DF-AGT-089, DF-AGT-094, DF-AGT-095, DF-AGT-096 | agent_evaluation | label_key, agreement_rate, precision_value, recall_value | Read, for the latest DONE evaluation per agent and version |
| DF-AGT-103, DF-AGT-104, DF-AGT-105 | agent_alert | id, agent_code, alert_type | Write |
| DF-AGT-106, DF-AGT-107 | agent_alert | segment, business_date | Write |
| DF-AGT-108, DF-AGT-109 | agent_alert | measured_value, threshold_value | Write |
| DF-AGT-110, DF-AGT-111 | agent_alert | sent_to_role, sent_at | Write; `sent_at` empty until the send succeeds |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value (rwb_case, owner P3) | the daily cost cap and the alert role of the approved policy version, with the version in force | Read through the parameters contract |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row (rwb_case, owner P3) | LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT with the version in force | Read through the reference-data contract |
| P9 measures | measure_definition, measure_publish, measure_snapshot (rwb_reporting, owner P9) | the published measure "Agent fallback rate" with its business date, its definition and its value | Read through the measures operation |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-E1-063. `agent_run`, `agent_evaluation`, `agent_policy` and `agent_alert` are the P10 tables of schema `rwb_agent` in the Ownership Map. The legacy lake table `agent_run_daily` has no target and is not created: the daily aggregate rows live in `rwb_agent` and the reporting feed is the event topic (DP-17; GAP-0616). No field of another service's table is written or read as a table. The daily aggregate of the date is the element the metric read answers, so no separate data product is declared here.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/agent-metrics` | Read agent measures per agent, version, segment and business date for the agent monitor: query agent, segment, version, from and to; 200 AgentMetric[], one element per agent, policy version, prompt version, model version and business date, with runs, answered, fallback, fallback rate, latency p50, latency p95, tokens, cost and the latest evaluation score; a date that is HELD answers its status and its previous published date | Rules and parameters R, scope applied | Not applicable: the call writes nothing |

Errors: 401 no session, 403 no Rules and parameters right (MSG-P4-002), 422 a query the service cannot accept, 503 the store or a consumed contract unavailable. The shape of this operation, its paging and its member names are fixed by RWB-P10-E1063-CON and its contract tests.

Two further rwb-agent operations are used by the dashboard and are provided by the service under the baseline of RWB-P10-E1058-CON, not re-declared here: `GET /api/recovery/agent/v1/admin/agent-runs` with query agent, from and to answering AgentRun[], and `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` answering AgentOutput[] under the Case record read.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | AC2, AC4, AC5 and AC6: `daily_cost_cap_thb` and `alert_role` of the approved policy version in force, read at run time and never from code | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The check of LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT before a daily row or an alert is written | One hop, 2 s |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | AC1: the published measure "Agent fallback rate" for the business date, with its definition and its value | One hop, 2 s |
| POST | the rwb-comms notification operation: Not specified in the source documents (GAP-0616; ASM-0892) | P6 rwb-comms | AC2, AC3 and AC7: one notice for MSG-P10-004 to the alert role and to RW-RISK, and one notice to the data steward for a held date | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11); rwb-agent calls no service through another service and holds no schema client of another service. The delivery of a notice by rwb-comms through rwb-integration is the contract RWB-P2-E1007-CON and is not called by this service.

#### 12.3 Events published

None by this story. The reporting feed is `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` with its retry topic and its `.dlt` topic, published by the run path of RWB-P10-E1058-APP through the outbox relay, keyed by the case ID and carrying run facts only. This story adds no event of its own, because the daily aggregate is computed from rows the service already owns and is served on its own read (DP-17; ASM-0889).

#### 12.4 Events consumed

None. The rollup reads the rows of `rwb_agent` for the business date and its values through the contracts of 12.2; it subscribes to no topic. The consumers of EV-28 are rwb-decision, rwb-document, rwb-deviation and rwb-reporting, not this service.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunDailyRollupWorkflow | Workflow, one per business date, workflow ID = the business date | `rwb-agent` | Input: business date, the requested-by role and the flag of a manual start. Ends COMPLETE, HELD or FAILED with the counts of the date |
| aggregateAgentRuns | Activity | `rwb-agent` | Output: the daily aggregate rows of the date, per agent, policy version, prompt version and model version, with the count check result |
| raiseCostAlerts | Activity | `rwb-agent` | Output: the `agent_alert` rows of the date, one per agent and segment, on the unique key |
| dispatchAgentAlerts | Activity | `rwb-agent` | Output: the notice requests and the outbox rows; no partial write |

The workflow runs on the queue and in the namespace of the service (§R4); the names are this story's and are accepted by RWB-P10-E1063-CON.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| AgentRunDailyRollup | Daily at 01:30 Asia/Bangkok for the previous business date; overlap policy SKIP; catch-up window one business date; a manual start for any business date through the same workflow ID | Registered and updated by RWB-P10-E1063-OPS through the workflow kit of RWB-PLT-E1071-CON in namespace `rwb-recovery`; the name is Not specified in the source documents (GAP-0616; ASM-0888) | The legacy Quartz entry of JOB-15 at 01:30 and its `agentRunDaily` step (legacy sections 3, 4 and 12) |

The legacy job table is not read and the legacy `POST /admin/jobs/{jobId}/rerun` is not called: a rerun is a manual start of the same workflow for the business date, which is what AC4 asserts (DP-10).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_alert | P10 (`rwb_agent`) | One cost or drift alert per agent, type, segment and business date; created by `V10_006__agent_alert.sql`; `sent_at` empty until the send succeeds |
| agent_run | P10 (`rwb_agent`) | Read for the aggregate of the date and the count check; no column added |
| agent_evaluation | P10 (`rwb_agent`) | Read for the latest DONE score per agent and version; no column added |
| agent_policy | P10 (`rwb_agent`) | Read for the approved policy version of the agent; its cap and alert role are read through the parameters contract |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox and idempotency envelope of the notices (DP-09) |

No lake table is created and `agent_run_daily` has no target (DP-17). rwb-agent reads no table of another service and holds no foreign key across services (DP-01). `parameter_catalog`, `parameter_value`, `reference_version` and `reference_row` are P3's and `measure_definition`, `measure_publish` and `measure_snapshot` are P9's, and all are read through their contracts. `V10_006__agent_alert.sql` runs in the rwb-agent Flyway sequence of `rwb_agent` and touches no other schema (DP-15).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock | The P3 parameters contract of RWB-P3-E1042-CON and the reference-data contract of RWB-P3-E1043-CON | `daily_cost_cap_thb` 2,000 and `alert_role` "RW-COE" for INTAKE, SCREENING and EXTRACT; a policy row with no cap; LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT; a delay beyond 2 s |
| rwb-reporting WireMock | The P9 measures contract of RWB-P9-E1055-CON | The published measure "Agent fallback rate" for 2026-12-01 and for 2026-11-30; a measure that is not published for the date; a delay beyond 2 s |
| rwb-comms WireMock | The P6 notification path of RWB-P6-E1063-APP | An accepted notice with its reference for MSG-P10-004; a 503 at 01:40 for AC7; an accepted notice for the data steward |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the three reads, one hop, with the JSON media type preserved |

Every fixture is synthetic and holds no personal data. No test calls the model endpoint INT-23: the run rows of the fixture are written by the store, not by a model call.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 provided by the baseline and used, 4 consumed | The metric read provided; the run read and the case agent-outputs read used from the baseline of RWB-P10-E1058-CON; the P3 parameters, the P3 lists, the P9 measures and the P6 notice consumed, one hop and 2 s each |
| Kafka | None published or consumed by this story | The reporting feed is EV-28 on `rwb.agent.events.v1` with the retry and `.dlt` topics, published by the run path of RWB-P10-E1058-APP and consumed by rwb-reporting; no lake write exists (DP-17) |
| Temporal | 1 workflow, 3 activities, 1 Schedule | AgentRunDailyRollupWorkflow with aggregateAgentRuns, raiseCostAlerts and dispatchAgentAlerts on the queue `rwb-agent`, started by AgentRunDailyRollup at 01:30 |
| File | None | No extract, no lake credential and no file path: the aggregate leaves as the body of the read and the feed leaves as events (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.monitor`, module `monitor`, Java package `th.co.scb.ace.workbench.recovery.agent.monitor` inside the rwb-agent service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies of this table are the ones in the metadata rows; DP-17 adds no dependency and closes the legacy lake dependency; DP-11 sits on the four consumed reads and adds no dependency of its own, because the legacy in-process calls are reached through the C contracts of the key.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentMetricAggregator | Service | Applies BR1, BR5 and BR11: groups the `agent_run` rows of the business date by agent, policy version, prompt version and model version, joins the latest DONE score and builds the aggregate element the read answers |
| AgentRunDailyRollupWorkflow, aggregateAgentRuns | Workflow and activity | Runs the date, computes the daily rows and applies the count check of BR2, ending COMPLETE, HELD or FAILED |
| CostAlertService, raiseCostAlerts | Service and activity | Applies BR3 and BR6: compares the cost of the date with the cap read through the parameters contract and writes one `agent_alert` row per agent and segment |
| AgentAlertDispatcher, dispatchAgentAlerts | Service and activity | Applies BR9: writes the notice request, the outbox row and the `sent_to_role`, and leaves `sent_at` empty until the relay confirms |
| AgentMetricController | Controller | The metric read on `/api/recovery/agent/v1`, its query, the status of a held date and the error mapping (DP-13) |
| ParameterValueReader | Client | Reads the daily cost cap and the alert role of the approved policy row through the parameters contract (DP-06) |
| ReferenceDataReader | Client | Reads LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT through the reference-data contract (DP-07) |
| MeasureReader | Client | Reads the published measures of rwb-reporting with one hop and the 2 s budget (DP-11, DP-17) |
| NoticeClient | Client | Calls the rwb-comms notification path and maps the refusal to the outbox retry (DP-09) |
| AgentAlertRepository | Repository | Writes and reads `agent_alert` in `rwb_agent` only (DP-01) |

**Database and migrations**

- `V10_006__agent_alert.sql` creates `agent_alert` with the standard record columns, the columns DF-AGT-103 to DF-AGT-111 and the unique key (agent_code, alert_type, segment, business_date), in `rwb_agent`, in the rwb-agent Flyway sequence, and touches no other schema (DP-15; BR4, BR10).
- One index for the read of the date: `ix_agent_run_business_date ON agent_run (run_at)`, which the legacy story also names, so the aggregate of a date is answered without a scan; the index is created by this story's migration if the earlier P10 migrations do not hold it.
- No `agent_run_daily` table, no lake table and no extract table is created (DP-17).

**Configuration and reference data**

- `agent_policy.daily_cost_cap_thb` 2,000 and `agent_policy.alert_role` "RW-COE" for INTAKE and SCREENING (assumed values; DL33), loaded by RW-COE and approved by RW-RISK, read at run time through the parameters contract and appearing nowhere in the source (DP-06; GAP-0616; ASM-0890).
- LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT, in force in rwb-case and read through its reference-data contract (DP-07; ASM-0890).
- The Schedule `AgentRunDailyRollup`, its 01:30 Asia/Bangkok cadence, its overlap policy SKIP and its catch-up window, registered by the deployment story of this key (DP-10; ASM-0888).
- The notification template of MSG-P10-004 in the rwb-comms template set, with the text of section 14 unchanged.
- The legacy feature flag `rwb.agent.monitor` is kept as the legacy reference: off, the Schedule starts no rollup activity and the metric read answers the last published date with its status.

**Build steps**

1. Flyway migration `V10_006__agent_alert.sql`, the entity and AgentAlertRepository in `rwb_agent` (AC3; BR4, BR10).
2. ParameterValueReader and ReferenceDataReader against the P3 contract fakes, with the missing-cap path of X7 (AC2, AC5, AC6).
3. AgentMetricAggregator with the fixture of 270 runs - INTAKE 120 with 9 fallbacks and SCREENING 150 with 21 - and the fallback rate 0.0750 (AC1; BR5, BR11).
4. AgentRunDailyRollupWorkflow and aggregateAgentRuns with the replace-by-date write and the count check (AC3, AC4; BR2).
5. CostAlertService and raiseCostAlerts with the strict greater-than rule and the unique key (AC2, AC6; BR3, BR4).
6. AgentAlertDispatcher, dispatchAgentAlerts and NoticeClient with the outbox retry and the `sent_at` rule against the rwb-comms fake (AC7; BR9).
7. AgentMetricController and the metric read on `/api/recovery/agent/v1`, with the status of a held date, and MeasureReader against the rwb-reporting fake (AC1, AC3; DP-11, DP-13).
8. Pipeline scans: no lake table, no lake credential, no `agent_run_daily`, no other service's table name and no cost literal in the source (BR7, BR10).
9. Schedule registration against the workflow kit stub, one run per business date from the Schedule and from a manual start, and the rerun of AC4 (DP-10).
10. gateway-bff route contract test in front of the metric read (AC1; DP-19).

**Done when.** The eight test cases of section 16 pass, the metric read answers on `/api/recovery/agent/v1` with the fixture figures for 2026-12-01, the rollup writes one `agent_alert` row for SCREENING and none for INTAKE, the rerun for the date leaves the same two rows and no second alert, the notification is retried after a 503 at 01:40, the schedule is registered and fires once for a business date, the pipeline scan finds no lake artefact and no literal of the cap, and RWB-P10-E1063-OPS has registered the Schedule and the feed in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-004 | Agent cost on a business date above its daily limit | {agent} used {amount} baht of model calls on {date}, above the daily limit of {limit} baht. |
| MSG-P1-001 | The report shows the previous day after a held publish | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-E1-063 and this story adds no message ID. Thai text for each message follows decision DL10. In AC2 the {agent} value is "SCREENING", {amount} is 2,310.5000, {date} is 2026-12-01 and {limit} is 2,000. In AC3 the stale banner carries the previous business date 2026-11-30. In the access test the {action} value is "open the agent monitoring dashboard". MSG-P1-001 is P1's message and is kept as the legacy text of the stale banner.

### 15. Screens and states

No Workbench screen in this story; SCR-46 Agent monitor comes in RWB-E2-031 and is not changed here. The legacy Power BI report "Agent monitor v1" is replaced by the served aggregate: the dashboard reads `GET /api/recovery/agent/v1/admin/agent-metrics` through the gateway-bff route, which is the only route a screen uses (DP-19; AC1). Its states are loaded (the figures of the latest published date), held (the previous date with the MSG-P1-001 banner and the date shown), empty (a date with no runs) and unavailable (a consumed contract down, the aggregate still shown and the measure marked unavailable). The exact path of the gateway-bff route in front of the metric read is Not specified in the source documents (GAP-0616; ASM-0891).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-063-01 | AC1, BR5 | Component | INTAKE 120 runs, 9 fallback; SCREENING 150 runs, 21 fallback on 2026-12-01; fallback rate 0.0750 |
| TC-E1-063-02 | AC2, BR3, BR6 | Component | SCREENING cost 2,310.5000 baht, cap 2,000; one COST_CAP alert row and one notice for RW-COE and RW-RISK |
| TC-E1-063-03 | AC3, BR2 | Component | The reporting feed for 2026-12-01 with 1 row for 2 groups; the date held, the report showing 2026-11-30 and the data steward alerted |
| TC-E1-063-04 | AC4, BR4 | Component | A rerun for 2026-12-01; the same 2 daily rows and no second alert or notification |
| TC-E1-063-05 | AC5 | Component | EXTRACT with no runs on 2026-12-01; runs 0, cost 0.0000 and no alert |
| TC-E1-063-06 | AC6, BR3 | Component | INTAKE cost 2,000.0000 baht on 2026-12-02; no cost alert |
| TC-E1-063-07 | AC7, BR9 | Component | The rwb-comms fake answers 503 at 01:40; the alert row keeps `sent_at` empty and the relay sends it |
| TC-E1-063-08 | Access | Contract | RW-CASEOWN without the reporting read opens the dashboard; refused with 403 and MSG-P4-002 through the route |

TC-E1-063-01 to TC-E1-063-08 are the legacy test cases of RWB-E1-063, kept with their legacy IDs, their legacy order and their legacy data; the legacy System level maps to Component, and TC-E1-063-08 keeps its Access coverage at Contract level because the refusal is proved through the route and the published contract. The lake wording of TC-E1-063-03 and TC-E1-063-04 is the one adaptation, and its values - 1 row, 2 groups, 2026-12-01 and 2 rows - are the legacy ones. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the cap, the alert role, the agent list, the alert types and the schedule cadence are configuration and contract values read at run time, and a missing cap stops the alert instead of falling back to a default (BR3).
- No personal data in logs, tests, events, notices or alerts: rows hold counts, times and amounts only, the fixtures are synthetic, and no account number, name or national ID appears in a payload (legacy section 17).
- No read of another service's tables and no schema client: the parameters and lists come through the rwb-case contracts, the measures through the rwb-reporting contract, the notices through the rwb-comms contract and the route through gateway-bff (DP-01, DP-06, DP-07, DP-11, DP-19).
- No data lake anywhere: no lake table, no lake credential, no extract file and no INT-19 or INT-20 call, and the pipeline fails a release that carries one (DP-17; BR7).
- One table of its own, `agent_alert`, in `rwb_agent`, created only by `V10_006__agent_alert.sql`; no `agent_run` or `agent_evaluation` row is edited by this story (BR10, DP-15).
- One hop and a 2 s client budget on every consumed REST call; the run of an agent keeps its own 60-second budget inside the service (DP-11; NFR-010).
- The dashboard reads are reached through the gateway-bff route and never from a screen to the service (DP-19).
- The rollup is idempotent on the business date: the workflow ID is the date, the alert key is the agent, type, segment and date, and a rerun replaces the rows of the date in one transaction (BR4, BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched (the legacy text names the data lake copy, which DP-17 removes; the copy becomes the event feed into rwb-reporting) | Business Requirements Program, section 5.7; Business Requirements Epic 1, section 3.9 | FEAT-AGT-06 | 15 Manage performance, data and AI | R-UNI-33, R-UNI-35, R-UNI-40 | TC-E1-063-01, TC-E1-063-02, TC-E1-063-03, TC-E1-063-04, TC-E1-063-05, TC-E1-063-06, TC-E1-063-07, TC-E1-063-08 |
| D-RCV-60 DP-01 | `agent_alert` is owned by rwb-agent in `rwb_agent`, and every other service's data is read through its contract | Business Requirements Epic 1, section 3.9; Template and Rules §R5.5 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E1-063-01, TC-E1-063-03 |
| D-RCV-60 DP-06 | The cost cap and the alert role are parameters read at run time, never values in code | Template and Rules §R5.5; ADR-021 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E1-063-02, TC-E1-063-05, TC-E1-063-06 |
| D-RCV-60 DP-07 | The agent, alert-type and product lists are read from the rwb-case reference-data contract | Template and Rules §R5.5 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E1-063-02, TC-E1-063-03 |
| D-RCV-60 DP-09 | The alert notice is written through the outbox and retried, and a permanent failure goes to `.dlt` | Template and Rules §R5.5; ADR-015 | FEAT-AGT-06 | 15 Manage performance, data and AI | R-UNI-33, R-UNI-35 | TC-E1-063-07 |
| D-RCV-60 DP-10 | The nightly rollup is the Temporal Schedule `AgentRunDailyRollup`, and the legacy job table is not read | Template and Rules §R5.5; ADR-016 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E1-063-02, TC-E1-063-04 |
| D-RCV-60 DP-11 | The consumed reads are REST contracts with a fake, one hop and a 2 s budget | Template and Rules §R5.5; ADR-020 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E1-063-01, TC-E1-063-07 |
| D-RCV-60 DP-13 | The metric read is served on the base `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E1-063-01 |
| D-RCV-60 DP-15 | `agent_alert` arrives with the service's own Flyway migration in its own schema | Template and Rules §R5.5; ADR-021 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E1-063-02, TC-E1-063-03 |
| D-RCV-60 DP-17 | No data lake: the reporting feed is built from `rwb.agent.events.v1` into rwb-reporting and no lake write exists | Template and Rules §R5.5; ADR-018; Arch v5 slide 37 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E1-063-03, TC-E1-063-04 |
| D-RCV-60 DP-19 | The dashboard read is reached through the gateway-bff route, and SCR-46 is unchanged here | Template and Rules §R5.5; ADR-019 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E1-063-08 |
| NFR-068 | An alert reaches its holders inside the agreed window | Business Requirements Program, section 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | R-UNI-33 | TC-E1-063-02, TC-E1-063-07 |
| RWB-E1-063 (legacy story) | Agent monitoring dashboard v1 [E2c]: the seven criteria AC1 to AC7 and the access test | Business Requirements Epic 1, section 3.9 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | The eight legacy test cases of section 16 |
| RWB-ITG-E1063-ITG (integration copy) | The same behaviour proved across rwb-agent, rwb-reporting, rwb-comms and rwb-case on the real services, with the `-ITG` test cases | Business Requirements Epic 1, section 3.9 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | The test cases of that story |

The gap GAP-0616 records the areas the sources leave open for this story - the removed lake and its replacement by the event feed, the schedule name, the login, the route path and the notification operation of rwb-comms - and each default it raises is settled by ASM-0888 to ASM-0869.

### 19. Out of scope

- The cross-service behaviour of this key: RWB-ITG-E1063-ITG, and the harness RWB-ITG-W1J01-ITG.
- The contract of the two reads and of the aggregate shape as a published artefact with its fakes: RWB-P10-E1063-CON.
- The deployment of this capability - chart values, Schedule registration, consumer group, dashboards, alerts, runbook and the route publication: RWB-P10-E1063-OPS.
- The agent runtime, the policy and prompt store, the configuration operations and the publication of EV-28: RWB-P10-E1058-APP.
- The evaluation harness and the score rows: RWB-P10-E1060-APP and RWB-P10-E1061-CON.
- The right check and the refusal of a role without the reporting read: RWB-P4-E1063-APP, the access slice of this key.
- The notification path, the message template and the delivery of MSG-P10-004: RWB-P6-E1063-APP, the communications slice of this key.
- The delivery of a notice through rwb-integration: RWB-P2-E1007-CON.
- The measure definitions, the snapshots and the published measures: P9 rwb-reporting, and the steering dashboard of RWB-E2-009.
- The agent monitor screen SCR-46 and its dashboard: RWB-E2-031.
- Drift detection with a raised decision (FEAT-AGT-13, Epic 3).
- Any lake table, extract file, lake credential, data-set job or data-lake copy, which DP-17 removes (GAP-0616).
