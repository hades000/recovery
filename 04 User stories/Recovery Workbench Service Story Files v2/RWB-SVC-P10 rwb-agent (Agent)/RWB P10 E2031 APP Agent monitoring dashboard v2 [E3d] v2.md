# RWB-P10-E2031-APP Agent monitoring dashboard v2 [E3d]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2031-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not sized; the squad sizes it at refinement; the point value is Not specified in the source documents (DOR-RWB-P10-E2031-APP-16) |
| Patterns applied | DP03, DP07, DP10, DP13, DP15, DP19 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1063-APP (not done yet) |
| Depends on (build) | RWB-P10-E2031-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-E1063-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P7-E2005-CON |
| Integration dependencies | None |
| External dependencies | RWB-P10-E2031-OPS (not done yet) |
| Open decisions | DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL25 (assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602) are still open; each open decision is paired with its assumption until it is decided |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-018, FR-P10-026) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E2-031 for rwb-agent, and the v2 of the dashboard that RWB-P10-E1063-APP already builds. The legacy key is not re-based on a new aggregate, so this change log names the four things v2 adds and the rest of the document does not restate the v1 story. **(1) The L1 measures:** acceptance, correction, override and the feedback count per agent, policy version, prompt version, model version, segment and business date, read from `agent_feedback` and from the decision records of rwb-decision (BR1, BR2). **(2) The segment filter:** the screen filters by agent, segment and date range, with the from-after-to refusal of MSG-GEN-003 and the 92-day refusal of MSG-GEN-002, and the segment is the product group and the region the run row carries (BR6). **(3) The drift check:** the legacy step `agentDrift` of JOB-15 becomes the `agentDrift` activity of the Temporal Schedule `AgentRunDailyRollup` that v1 registered (DP-10); it compares the acceptance of the last 7 days with the 7 days before for each L1 agent and segment, writes one `agent_alert` row of type DRIFT on the unique key and sends MSG-P10-006 through the rwb-comms notification path. **(4) The reconciliation:** a month is reconciled when the daily rows of the date and the run sums agree, and a month that does not reconcile shows the token difference (BR4). The lake copy of the legacy story leaves with the data lake (Architecture v5 slide 37; ADR-018) and with the event feed that v1 already put in its place: this story reads the rows of `rwb_agent` and the published measures of rwb-reporting and writes no lake table, no extract and no data-set job. The read keeps the base `/api/recovery/agent/v1` (DP-13), the rows stay in the schema `rwb_agent`, the lists come through the rwb-case reference-data contract (DP-07), the record of a recommendation and of its override through the rwb-decision ledger and the local decision-record library (DP-03), the one index arrives with the service's own Flyway sequence (DP-15) and the screen is reached through the gateway-bff route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E2031-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 17 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the v2 of the agent monitor dashboard inside rwb-agent - the aggregate of RWB-P10-E1063-APP extended with acceptance, correction, override and the segment of the case, served on `/api/recovery/agent/v1/admin/agent-metrics` with the segment filter, the 92-day range and the two refusals of the legacy screen; a drift check added as the `agentDrift` activity of the `AgentRunDailyRollup` Schedule that compares the acceptance of the last 7 days with the 7 days before for each L1 agent and segment, writes one `agent_alert` row of type DRIFT and sends MSG-P10-006 to the policy alert role and to RW-RISK; a monthly reconciliation of the daily rows against the run sums that shows "not reconciled" with the token difference; and the override reasons per agent and month read through the rwb-decision decision log and composed on SCR-46 by the gateway-bff route**, so that **every agent at L1 is watched daily and a fall in acceptance is acted on within a day**.

### 2. Business rationale

At L1 a case owner reads the agent's output and accepts, corrects or rejects it. A fall in acceptance on one segment is the first sign that a prompt, a model version or the data has changed. This story puts acceptance, override, fallback, latency and cost per agent, version and segment on the agent monitor screen SCR-46, reconciles tokens and cost to the per-call figures the endpoint returns, reports override reasons (REQ-APD-005) and checks drift daily from the same figures used for reporting (REQ-DRI-009).

The v1 story of this key, RWB-P10-E1063-APP, already serves the aggregate of a business date - runs, answered, fallback, latency, tokens, cost and the latest evaluation score - on `/api/recovery/agent/v1/admin/agent-metrics`, computes it from `agent_run`, `agent_evaluation` and `agent_policy` in `rwb_agent`, and publishes the reporting feed `rwb.agent.AgentRunCompleted.v1` through the outbox. This story does not restate that aggregate. It adds the L1 measures, the segment filter, the drift check and the reconciliation on top of it, and it explains here why each one is now a service matter rather than a monolith one:

- **The L1 measures.** Acceptance and correction are read from `agent_feedback`, the table the L1 slices own (verdict ACCEPTED, CORRECTED or REJECTED; BR1). The override rate and the override reasons are the decision records of the agent's recommendation - `decision_log_entry` in the legacy story - and in the target that ledger is rwb-decision's, so the figures are read through the rwb-decision decision-log contract with one hop and the 2 s budget (BR2; ASM-0960).
- **The segment.** The legacy story read `recovery_case.product_group` and `recovery_case.region_code`. In the target the run row carries the segment as `agent_run.segment_product_group` and `segment_region_code` (DF-AGT-059, DF-AGT-060), set at run time by the run path of RWB-P10-E1058-APP from the case read, so this story reads its own table and never reads `rwb_case` (BR6; ASM-0959).
- **The drift check.** The legacy step `agentDrift` ran inside JOB-15 after the `agentRunDaily` step of the monolith at 01:30. In the target there is no shared job table and no Quartz entry: the nightly work of the key is the Temporal Schedule `AgentRunDailyRollup` in namespace `rwb-recovery` on the task queue `rwb-agent` that v1 registered at 01:30 with overlap policy SKIP and the one-business-date catch-up window, and this story adds the `agentDrift` activity after the aggregate inside the same workflow identity (DP-10; ASM-0958).
- **The reconciliation.** The legacy story compared `agent_run_daily` with the sum of `agent_run` for a month. There is no `agent_run_daily` in the target, because there is no data lake: the daily rows are the aggregate of the business date on the read, and the published measures are built by rwb-reporting from `rwb.agent.AgentRunCompleted.v1`, so the month is reconciled against the daily rows and the run sums and the published measures are shown beside them (BR4; Architecture v5 slide 37; ADR-018).
- **The notice.** MSG-P10-006 leaves through the rwb-comms notification path with the outbox retry of the platform library, and the `agent_alert` row keeps `sent_at` empty until the path accepts the notice (ASM-0961).
- **The screen.** SCR-46 Agent monitor is a Workbench screen, and in the target a screen reaches a service only through the gateway-bff composite route (DP-19; ASM-0967).

The behaviour of the key is kept: the acceptance, override, fallback, latency and cost of an agent, version and segment on one screen; the state of each agent as Shadow, live or paused; the drift check after the daily rows; one DRIFT alert and one notice on a fall of 10 points or more; the minimum of 20 feedback entries per week and segment; the override reasons per agent and month; and the three refusals of the screen (MSG-GEN-003, MSG-GEN-002, MSG-P4-002). The seven acceptance criteria AC1 to AC7 of RWB-E2-031 are kept word for word with their origin tags, and the two places where the legacy text names an object that has no target - `agent_run_daily` in AC3 and the step of JOB-15 in AC2 and AC7 - are read against the served aggregate and the Schedule step (section 7, Target reading).

The cross-service behaviour of this key - that the read through the route, the decision log of rwb-decision, the measures of rwb-reporting and the notice of rwb-comms really agree with what rwb-agent serves - is proved by RWB-ITG-E2031-ITG, which is why this story carries no integration dependency (I = None) and claims none. This story builds and unit-tests its own deliverables against the published contracts and their fakes.

### 3. Preconditions

- RWB-P10-E1063-APP is done and is the dashboard this story extends: the daily aggregate of a business date is served on `GET /api/recovery/agent/v1/admin/agent-metrics`, the Schedule `AgentRunDailyRollup` writes it at 01:30 Asia/Bangkok, and `agent_alert` exists in `rwb_agent` with its unique key of agent, type, segment and business date (legacy precondition "RWB-E1-063 is done: agent_run_daily is written by JOB-15 and agent_alert exists").
- RWB-P7-E2005-CON is published: the decision-log read of the central ledger answers the entries of a date range with their recommendation, final call and override reason. The agent-version filter and the three elements the override figures need are the additive change of ASM-0960, because the published contract declares neither (GAP-0629).
- RWB-P10-E2031-CON is published: the v2 element, the two filter refusals, the DRIFT alert shape and the Schedule contract with the `agentDrift` step (ASM-0964).
- Agent runs carry the segment (product group and region) of their case: `agent_run.segment_product_group` and `agent_run.segment_region_code` (DF-AGT-059, DF-AGT-060), written at run time by the run path of RWB-P10-E1058-APP (ASM-0959).
- Feedback on L1 output is recorded in `agent_feedback` (verdict ACCEPTED, CORRECTED or REJECTED, LOV-FEEDBACK) by RWB-P10-E2028-APP; until then acceptance shows "no L1 runs".
- Each L1 policy holds `watch_measures` with `drift_points` 10 (assumed) and minimum feedback 20 per week per segment (assumed), with `window_days` 7 (assumed), in `agent_policy.watch_measures` (DF-AGT-019), loaded by RW-COE and approved by RW-RISK (ASM-0962).
- The user holds the right of the read: TSD P10 Agent runtime v2 T-A.1 API-P10-009 declares Rules and parameters R, while the legacy story names Platform administration R; the two names describe the same roles and the refusal is MSG-P4-002 either way (GAP-0629; ASM-0970).
- RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are published: the decision-record library and its shared topic, the reference-data client library, the Temporal workflow kit with namespace `rwb-recovery`, the per-service Flyway sequence and the gateway-bff route contract with its stub.
- The deployment values (route path, per-service login secret reference, topology, budget, Schedule registration, notification operation and the single model-gateway egress) are fixed in the deployment and edge stories with the defaults of GAP-2200; this story sets none of them.
- The rwb-case reference-data contract of RWB-P3-E1043-CON is published for LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE, and the rwb-reporting measures read answers the published measures for a business date.
- The release date 31 December 2026 is tentative and is copied unchanged.
- Signed epic design: Not specified in the source documents (DOR-RWB-P10-E2031-APP-14).

### 4. Flow

1. RW-COE opens SCR-46 Agent monitor from the Administration menu; the screen and its data are reached through the gateway-bff route and never from the screen to rwb-agent (DP-19; flow step 1 of the legacy story).
2. The route checks the right of the read, then the screen calls `GET /api/recovery/agent/v1/admin/agent-metrics` for the last 30 days, the legacy default range (BR9; the legacy step 2).
3. The read answers one element per agent, policy version, prompt version, model version, segment and day: runs, fallback rate, acceptance rate, correction rate, override rate, feedback count, median and 95th percentile latency, tokens, cost and the reconciled flag (BR1, BR2; AC1).
4. RW-COE filters by agent, segment and date range; the screen shows the state of each agent - Shadow, live (L1) or paused (mode OFF) - read from `agent_policy.autonomy_mode` (DF-AGT-008; ASM-0965; AC1).
5. After the daily rows of a business date, the `agentDrift` activity of `AgentRunDailyRollupWorkflow` runs the drift check for each L1 agent and segment: the acceptance of the last 7 days against the 7 days before, both windows of 7 calendar days ending on the business date, with at least 20 feedback entries in each week (DP-10; BR3; ASM-0962; AC2, AC4).
6. On a fall of 10 points or more it writes one `agent_alert` row of type DRIFT with the business date, `measured_value`, `threshold_value` - the acceptance of the earlier week less 10 points - `segment` and `sent_to_role`, on the unique key of agent, type, segment and business date, so a rerun adds no second row (BR5; AC2, AC7).
7. The `dispatchAgentAlerts` activity sends MSG-P10-006 to the holders of the policy alert role (DF-AGT-015) and to RW-RISK through the rwb-comms notification path and writes the outbox row in the same transaction; `sent_at` stays empty until the relay confirms the send (ASM-0961; AC2).
8. A segment with fewer than 20 feedback entries in either week is not checked: no row is written and the screen shows "not enough feedback" (BR3; AC4).
9. RW-COE opens the override reasons for an agent and month: the v2 element carries the override rate, and the count per coded reason is read from the rwb-decision decision-log read and composed on the screen by the gateway-bff route, because the reason codes are the ledger's (BR2; REQ-APD-005).
10. The monthly reconciliation compares, per agent and month, the daily rows of the dates with the sum of `agent_run` for the same dates; when they differ the month shows "not reconciled" with the token difference, and the published measures of rwb-reporting are shown beside the figures rather than read as a second source (BR4; AC3).
11. Every figure comes from the rows of `rwb_agent` by the aggregates of the v1 story and from the decision records read through the rwb-decision contract; the reporting measures are built by rwb-reporting from `rwb.agent.AgentRunCompleted.v1`; this story writes no lake table, no extract and no data-set job (section 17).
12. SCR-46 states (section 15): empty - when the range holds no row the screen shows "No agent runs in this period."; loading - skeleton rows until the read answers; error - the message is shown at the top; no access - the read is refused with 403 and MSG-P4-002, and the screen state is Not specified in the source documents (CG-ALL-2790).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Fewer than 20 feedback entries in either week for a segment | No drift check for that segment; the screen shows "not enough feedback" | None to a user | AC4 |
| X2 | Filter "from" after "to" | Refused with 422 | MSG-GEN-003 | AC5 |
| X3 | Filter range longer than 92 days | Refused with 422 | MSG-GEN-002 | AC6 |
| X4 | Drift check runs again for the same date | No second alert (unique key) | None to a user | AC7 |
| X5 | The token sum of the daily rows does not match the sum of agent_run for a month (the legacy text names agent_run_daily, which has no target) | The month shows "not reconciled" with the difference | None to a user | AC3 |
| X6 | A role without Platform administration R opens SCR-46 | Refused with 403 | MSG-P4-002 | AC8 |
| X7 | The rwb-decision decision-log read is unavailable or answers beyond the 2 s budget | The row still shows acceptance, fallback, latency and cost, marks the override figures as not available and guesses no figure | None to a user | AC1 |
| X8 | The approved policy row holds no `watch_measures`, or a value the drift rule needs is missing | No drift check runs for that segment, no alert is raised with a default value, the run ends failed and RW-PLATADM starts it again | None to a user | AC2 |
| X9 | The migration `V<version>__agent_monitor_index.sql` fails in the service's Flyway sequence | The new version does not start and the version in force keeps serving; no drift row is written | None | AC2 |
| X10 | The `agentDrift` activity is not registered by the worker, or the Schedule does not fire for a business date | No DRIFT row exists for the date; the run is started by hand for the same workflow identity and the registration is corrected by the deployment of RWB-P10-E2031-OPS | None | AC7 |

X1 to X6 are the legacy exception paths of RWB-E2-031 carried onto the service, with X5 read against the daily rows of the served aggregate instead of the lake copy. X7 to X10 are the failures that appear when the reads leave the service, when the policy becomes the only source of the rule, when the migration becomes the service's own and when the Schedule step replaces the JOB-15 step. X6 is reached by AC8 and proved through the route by TC-E2-031-09 and by the legacy test case TC-E2-031-08, and the message is kept so a reader finds the legacy set complete.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the in-lane story RWB-P10-E1063-APP, the platform contracts, and the published P3 and P7 contracts with their fakes; it owns its own activity, its own index and its own read extension |
| Negotiable | Drift points, minimum feedback and the window are policy values; the package layout, the component names and the panel order are design; the agents, the segment, the dates, the counts, the rates, the threshold, the messages and the refusals are fixed by the legacy story |
| Valuable | Turns acceptance and override into a daily alert for each L1 agent and segment, on the dashboard that already exists |
| Estimable | One read extension, one activity, one alert row type on an existing table, one index migration, one reconciliation query, six components, four contract clients and five fakes |
| Small | One back end and one front end developer for one week in the legacy estimate; the same size here, with the aggregate of the date already served |
| Testable | Each of the seven criteria of section 7 is one automated test on an observable: a read answer, a rate, an alert row, a measured and a threshold value, a notice, a refusal code or a reconciled flag |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v2 [E3d]

  Background:
    Given agents "INTAKE" (policy "P2", mode "L1") and "SCREENING" (policy "P2", mode "L1" for segment MORTGAGE and BKK) are live
    Given the drift rule is a fall of 10 points or more with at least 20 feedback entries in each week

  Scenario: AC1 Per agent (legacy RWB-E2-031 AC1)
    Given the rwb-decision contract mock returns the decision records of agent version "P2" for 2026-12-01 to 2026-12-14
    Given two agents at L1
    When the dashboard loads for 2026-12-01 to 2026-12-14
    Then acceptance, override, fallback, latency and cost show per agent, version and segment
    Then "INTAKE" for segment MORTGAGE and BKK shows 140 feedback entries with 119 accepted, acceptance rate 0.8500
    Then "SCREENING" shows state "live" for MORTGAGE and BKK and "Shadow" for every other segment

  Scenario: AC2 Drift (legacy RWB-E2-031 AC2)
    Given the rwb-comms contract mock returns an accepted reference for MSG-P10-006
    Given "INTAKE" acceptance for MORTGAGE and BKK is 0.8600 for 2026-12-01 to 2026-12-07 and 0.7500 for 2026-12-08 to 2026-12-14
    When the check runs after the daily rows in AgentRunDailyRollupWorkflow for 2026-12-14
    Then one alert of type "DRIFT" for "INTAKE", segment "MORTGAGE/BKK" and date 2026-12-14 holds measured 0.7500 and threshold 0.7600
    Then MSG-P10-006 goes to the holders of RW-COE and RW-RISK

  Scenario: AC3 Cost (legacy RWB-E2-031 AC3)
    Given the rwb-reporting contract mock returns the published token and cost measures for "INTAKE" for November 2026
    Given a month of calls in November 2026 for "INTAKE": 3,100 runs with 2,945,000 input tokens and 465,000 output tokens
    When the dashboard loads for November 2026
    Then tokens and cost per agent match the sum of the agent runs, which hold the token counts the endpoint returned on each call
    Then "INTAKE" shows 3,410,000 tokens and cost 170.5000 baht at 0.0500 baht per 1,000 tokens
    Then a month where the daily rows and the runs differ shows "not reconciled" with the token difference

  Scenario: AC4 Not enough feedback (legacy RWB-E2-031 AC4)
    Given "SCREENING" for MORTGAGE and BKK has 12 feedback entries in the week to 2026-12-14
    When the check runs
    Then the system raises no drift alert for that segment and the screen shows "not enough feedback"

  Scenario: AC5 Dates in the wrong order (legacy RWB-E2-031 AC5)
    When RW-COE filters from 2026-12-14 to 2026-12-01
    Then the system refuses the request with 422 and MSG-GEN-003

  Scenario: AC6 A range that is too long (legacy RWB-E2-031 AC6)
    When RW-COE filters from 2026-08-01 to 2026-12-14
    Then the system refuses the request with 422 and MSG-GEN-002 naming 1 and 92 days

  Scenario: AC7 The check runs twice (legacy RWB-E2-031 AC7)
    Given the DRIFT alert for "INTAKE", "MORTGAGE/BKK" and 2026-12-14 exists
    When AgentRunDailyRollupWorkflow is started manually again for 2026-12-14
    Then no second alert row or notification exists

  Scenario: AC8 A role without Platform administration R (legacy RWB-E2-031 X6) (new, D-RCV-60)
    Given a role without Platform administration R
    When the role opens SCR-46 through the route
    Then the system refuses the request with 403 and MSG-P4-002

  Scenario: AC9 Rules with no legacy criterion (BR7 to BR12) (new, D-RCV-60)
    Given the drift check is the agentDrift activity of the Schedule "AgentRunDailyRollup" and the read is served on "/api/recovery/agent/v1"
    When the rules of this story are checked against the service
    Then the agentDrift activity runs after the aggregate inside the same workflow identity and no separate Schedule exists
    Then the v2 element adds members to the v1 element and no v1 member is removed, renamed or retyped
    Then the read is reached only through the gateway-bff route and no screen calls rwb-agent directly
    Then the two filter limits are configuration values and not literals in code
    Then the story creates no table and V<version>__agent_monitor_index.sql runs in the rwb-agent Flyway sequence
    Then a role without the right of the read is refused with 403 and MSG-P4-002 through the route

  Scenario: AC10 Error answers of the provided operations (new, D-RCV-60)
    Given the read of rwb-agent is provided on "/api/recovery/agent/v1" behind the gateway-bff route
    When a request to a provided operation is refused
    Then the system answers 401 with MSG-P4-001 when there is no session and 403 with MSG-P4-002 for a role without the right, and answers 404 where the operation defines it, with the trigger of 404 Not specified in the source documents (NEWAC-RWB-P10-E2031-APP-AC10)

  Scenario: AC11 Activity retry and timeout (new, D-RCV-60)
    Given the agentDrift activity of the Schedule "AgentRunDailyRollup" is started for a business date
    When the activity fails or exceeds its timeout
    Then the activity is retried with the retry count and the timeout Not specified in the source documents (NEWAC-RWB-P10-E2031-APP-AC11)
    Then a retry writes no second DRIFT row for the same date

  Scenario: AC12 A consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-decision decision-log read is unavailable or answers beyond the 2 s budget
    When the dashboard loads
    Then the row still shows acceptance, fallback, latency and cost, marks the override figures as not available and guesses no figure
```

**Target reading.** The agents "INTAKE" and "SCREENING", their policy "P2" and mode "L1", the segment MORTGAGE and BKK and the segment form "MORTGAGE/BKK", the drift rule of 10 points and 20 feedback entries, the dates 2026-12-01 to 2026-12-14, the feedback count 140 and the accepted count 119 with the rate 0.8500, the acceptance 0.8600 and 0.7500 over the two weeks, the alert type "DRIFT", the measured value 0.7500 and the threshold 0.7600, the November 2026 figures of 3,100 runs with 2,945,000 input and 465,000 output tokens, the total 3,410,000 tokens, the cost 170.5000 baht at 0.0500 baht per 1,000 tokens, the shortage of 12 feedback entries, the refused orders of 2026-12-14 to 2026-12-01 and 2026-08-01 to 2026-12-14, the range 1 to 92 days and the message IDs are the legacy values of RWB-E2-031, copied character for character; the seven scenario titles and every legacy Given, When and Then are kept, except that the When lines of AC2 and AC7 name the target workflow, and each of those seven `Scenario:` lines carries the origin tag of its legacy criterion; AC8 to AC12 are added criteria.

Three scenarios gained one inserted Given, `Given the <service> contract mock returns <x>`, because the criterion reads across a service boundary. **AC1** reads the decision records that carry the agent version, the recommendation and the override reason: the legacy `decision_log_entry` of the P7 query interface is the central ledger of rwb-decision in the target, so the mock is the rwb-decision contract mock (ASM-0960). **AC2** sends MSG-P10-006 to the holders of RW-COE and RW-RISK: the notice leaves through rwb-comms in the target exactly as it left through the P6 notification interface in the legacy story, so the mock is the rwb-comms contract mock (ASM-0961). **AC3** shows the published token and cost measures beside the reconciled figures: those measures are rwb-reporting's and are read through its contract, so the mock is the rwb-reporting contract mock. AC4, AC5, AC6 and AC7 stay inside the service - the feedback rows, the alerts and the two refusals are rwb-agent's own - so they are not mocked. Nothing the service owns is mocked: `agent_feedback`, `agent_run`, `agent_policy` and `agent_alert` are the rows of `rwb_agent`.

Three legacy statements are read against an object that has no target, and each keeps the same values. The legacy **AC2 and AC7** say "after JOB-15" and "JOB-15 is rerun", and the scenarios here name `AgentRunDailyRollupWorkflow` instead: JOB-15 is the reporting extract of rwb-reporting in the target job map (Architecture v5 slide 44) and holds no agent step, so the `agentDrift` step of the legacy JOB-15 is the `agentDrift` activity of the Schedule `AgentRunDailyRollup`, and a rerun is a manual start of the same workflow identity for the business date (DP-10; ASM-0958). **AC3** compares "the daily rows" with the runs: `agent_run_daily` has no target because there is no data lake, and the daily rows are the aggregate of the business date that the v1 story serves (BR4). Everything else is the legacy behaviour: the one row per agent, version, segment and day with the five measures; the state words Shadow, live and paused; the check after the daily rows; the fall of 10 points or more; the minimum of 20 feedback entries per week; the unique key; the strict refusal of the two filter rules; and the override reasons per agent and month.

The legacy in-process `AgentRunExtractSource`, the Spring Batch step and the `DriftCheckStep` of the legacy roll-up become the `agentDrift` activity of `AgentRunDailyRollupWorkflow` behind the workflow kit of RWB-PLT-E1071-CON (DP-10), and the legacy `P7 DecisionLogQuery.byAgentVersion(agentVersion, from, to)` becomes the rwb-decision decision-log read with one hop and the 2 s budget (BR2). The lake copy, its credential and its extract have no target (GAP-0629).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Acceptance rate = accepted / (accepted + corrected + rejected) of L1 feedback; correction rate = corrected / the same total | `agent_feedback.verdict` (DF-AGT-100; LOV-FEEDBACK) |
| BR2 | Override rate = decisions with the agent version where final_call differs from the recommendation / decisions with the agent version; reasons counted from override_reason codes, read from the ledger through the rwb-decision decision-log contract (the legacy `decision_log_entry` read) | REQ-APD-005; DF-DEC-007, DF-DEC-009, DF-DEC-012, DF-DEC-013; CTL-07; ASM-0960 |
| BR3 | Drift = acceptance of the last 7 days at least 10 points below the 7 days before, with at least 20 feedback entries in each week (assumed values in watch_measures) | `agent_policy.watch_measures` (DF-AGT-019); ASM-0962 |
| BR4 | Token and cost totals come from agent_run; a month is reconciled when the daily rows equal the run sums, and the published measures of rwb-reporting are shown beside them | REQ-DRI-009; DL25 |
| BR5 | One alert per agent, type, segment and business date | `agent_alert` unique key (DF-AGT-103 to DF-AGT-111); R-UNI-40 |
| BR6 | A segment is the case product group and region at run time, carried on the run row as `agent_run.segment_product_group` and `agent_run.segment_region_code` and set by the run path (the legacy read `recovery_case.product_group` and `recovery_case.region_code`) | DF-AGT-059, DF-AGT-060; ASM-0959 |
| BR7 | The drift check is the `agentDrift` activity of the Schedule `AgentRunDailyRollup` in namespace `rwb-recovery` on the task queue `rwb-agent`, run after the aggregate of the business date inside the same workflow identity; there is no separate Schedule, no Quartz entry and no shared job table | DP-10; Architecture v5 slides 31 and 44; ASM-0958 |
| BR8 | The v2 element adds the segment, the mode, the acceptance, correction and override rates (four decimals), the feedback count and the reconciled flag to the v1 element as an additive change within major version 1; no v1 member is removed, renamed or retyped, and the paging of RWB-P10-E1063-CON stays unchanged | RWB-P10-E1063-CON; ASM-0964 |
| BR9 | The read is served on the base `/api/recovery/agent/v1` and reached only through the gateway-bff route; no screen calls rwb-agent directly | DP-13; DP-19; ADR-019 |
| BR10 | A from after a to is refused with 422 and MSG-GEN-003, and a range above 92 days with 422 and MSG-GEN-002; the two limits are configuration values and not literals in code | legacy AC5, AC6; ASM-0968 |
| BR11 | This story creates no table: it writes `agent_alert` rows of type DRIFT on the table v1 created and adds its two indexes by `V<version>__agent_monitor_index.sql`, where `<version>` is the next free version of the rwb-agent Flyway sequence (V0001 to Vnnnn, Service Template Specification v1) | DP-15; Ownership Map (P10 owns `agent_alert`); ASM-0963 |
| BR12 | A role without the right of the read is refused with 403 and MSG-P4-002; the right check is rwb-access's and the story proves the refusal through the route | legacy X6; TC-E2-031-08; ASM-0970 |

### 9. State transitions

None. This story does not change a case status. It writes agent alerts of type DRIFT and shows each agent's mode as Shadow, live or paused.

The state of a DRIFT alert of one agent, segment and business date, derived from BR5 and the alert row:

| From | Event | Condition | To |
|---|---|---|---|
| None | `agentDrift` evaluates a segment | Acceptance of the last 7 days is 10 points or more below the 7 days before, with at least 20 feedback entries in each week | One `agent_alert` row of type DRIFT with `sent_at` empty (DF-AGT-111) |
| None | `agentDrift` evaluates a segment | The fall is below 10 points, or either week holds fewer than 20 feedback entries | No row; "not enough feedback" is shown where the week is short |
| `sent_at` empty | The outbox relay confirms the send through rwb-comms | The notification path accepts MSG-P10-006 | `sent_at` set |
| `sent_at` empty | The relay fails | A 5xx or a timeout | `sent_at` stays empty and the notice is retried; a permanent failure goes to the `.dlt` topic with an alert |
| Any | A rerun for the same business date | The unique key of agent, type, segment and date already holds the row | The row is kept, no second row and no second notification |

The drift outcome of a business date follows the run of the workflow that the v1 story owns: the date is COMPLETE when the aggregate and the count check pass, HELD when the count check fails, and the `agentDrift` outcome of the date is recorded beside it as checked, not enough feedback, or failed. The screen state of an agent and segment is not a transition: it is the mode of the approved policy row (SHADOW, L1 or OFF, shown as Shadow, live or paused; ASM-0965).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Opens SCR-46 and calls `GET /api/recovery/agent/v1/admin/agent-metrics` under the right of the read; loads and reads `watch_measures`; receives the drift alerts as the policy alert role |
| RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Open SCR-46 and call the metric read under the same right (TSD P10 Agent runtime v2 T6.1) |
| RW-RISK, risk and model risk officer | Receives drift alerts; reads the published measures of rwb-reporting (Reporting R), because the Power BI copy of the legacy story is removed; does not hold the right of the read |
| RW-PLATADM, platform administrator | Starts or reruns the rollup for any business date through the same workflow identity; reads the run record |
| RW-CASEOWN, case owner | Records the verdict on an L1 output, which is the feedback this story reads; holds no right on SCR-46 |
| rwb-agent service identity (the rwb-agent login, DP-02) | Serves the read, runs `agentDrift`, writes `agent_alert`, reads its own tables, calls the rwb-decision decision-log read, the rwb-case reference-data read, the rwb-reporting measures read and the rwb-comms notice path |
| rwb-decision (P7) | Owns the ledger, the recommendation, the final call and the override reason, read through its contract |
| rwb-case (P3) | Owns the reference lists, read through its contract |
| rwb-comms (P6) | Owns the notification path and the delivery of MSG-P10-006 |
| SY-AGENT | None in this story |
| No role | Reads `rwb_case`, `rwb_decision`, `rwb_reporting` or any other service's schema, edits an `agent_run` or `agent_feedback` row, or reads production data |

The login of the service is Not specified in the source documents (GAP-0629; ASM-0966); the story references it through a secret reference as "the rwb-agent login (DP-02)". The screen route checks Platform administration R at the door of SCR-46, and the rwb-access authorise check (DP-08) runs before the read; the metric read checks Rules and parameters R as the right of the measure. A refusal is 403 with MSG-P4-002 (BR12), and the access-review run of wave 2 records which roles hold both rights. Approval levels: no delegation of authority level applies; the approval of a policy version and of its `watch_measures` is the Rules and parameters A right of RWB-P10-E1058-APP, as in the legacy story.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-DEC-007 | the decision record of rwb-decision (owner P7) | agent_version | Read through the rwb-decision decision-log contract (ASM-0960) |
| DF-DEC-009 | the decision record of rwb-decision (owner P7) | recommendation | Read through the rwb-decision decision-log contract |
| DF-DEC-012 | the decision record of rwb-decision (owner P7) | final_call | Read through the rwb-decision decision-log contract |
| DF-DEC-013 | the decision record of rwb-decision (owner P7) | override_reason | Read through the rwb-decision decision-log contract |
| DF-DEC-016 | the decision record of rwb-decision (owner P7) | decided_at | Read through the rwb-decision decision-log contract |
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
| DF-AGT-056 | agent_run | run_at | Read, for the business date of the run |
| DF-AGT-098 | agent_feedback | agent_run_id | Read |
| DF-AGT-100 | agent_feedback | verdict | Read |
| Standard column | agent_feedback | created_at | Read, for the two 7-day windows |
| DF-AGT-059 | agent_run | segment_product_group | Read here; set at run time by the run path of RWB-P10-E1058-APP (the legacy story writes it in the orchestrator) |
| DF-AGT-060 | agent_run | segment_region_code | Read here; set at run time by the run path of RWB-P10-E1058-APP |
| DF-AGT-008 | agent_policy | autonomy_mode | Read, for the state Shadow, live or paused |
| DF-AGT-009 | agent_policy | segment_product_group | Read |
| DF-AGT-010 | agent_policy | segment_region_code | Read |
| DF-AGT-019 | agent_policy | watch_measures | Read; `drift_points`, `min_feedback` and `window_days` are keys of the watch_measures value, not dictionary fields |
| DF-AGT-015 | agent_policy | alert_role | Read, for the notice of MSG-P10-006 |
| DF-AGT-103, DF-AGT-104, DF-AGT-105 | agent_alert | id, agent_code, alert_type | Write |
| DF-AGT-106, DF-AGT-107 | agent_alert | segment, business_date | Write |
| DF-AGT-108, DF-AGT-109 | agent_alert | measured_value, threshold_value | Write |
| DF-AGT-110, DF-AGT-111 | agent_alert | sent_to_role, sent_at | Write; `sent_at` empty until the send succeeds |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row (rwb_case, owner P3) | LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE with the version in force | Read through the reference-data contract |
| P9 measures | measure_definition, measure_publish, measure_snapshot (rwb_reporting, owner P9) | the published token and cost measures with their business date, their definition and their value | Read through the measures operation |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-E2-031. `agent_run`, `agent_feedback`, `agent_policy` and `agent_alert` are the P10 tables of schema `rwb_agent` in the Ownership Map. The legacy lake table `agent_run_daily` has no target, is not a field or entity in LDM v9 or Data Classification v5, and is not created: the daily rows are the aggregate of the business date that the v1 story serves, and the reporting feed is the event topic (Architecture v5 slide 37; ADR-018). No field of another service's table is written or read as a table: the decision records are read through the rwb-decision contract, the lists through the rwb-case contract and the measures through the rwb-reporting read.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10). Contract version built against: API Specification v5 `rwb-agent.yaml` version 5.0.0, with the additive v2 element of `/admin/agent-metrics` fixed by RWB-P10-E2031-CON.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/agent-metrics` | Read the agent measures per agent, policy version, prompt version, model version, segment and business date for the agent monitor, v2 of the element RWB-P10-E1063-CON fixed: query agent, segment, version, from and to; 200 AgentMetric[] with the v1 members - runs, answered, fallback, fallback rate, latency p50, latency p95, tokens, cost and the latest evaluation score - and the v2 members segment, mode, acceptance rate, correction rate, override rate, feedback count and reconciled; a from after a to is refused with 422 and MSG-GEN-003 and a range above 92 days with 422 and MSG-GEN-002; a date that is HELD answers its status and its previous published date | Rules and parameters R, scope applied (TSD P10 Agent runtime v2 T-A.1 API-P10-009); the legacy story names Platform administration R (ASM-0970) | Not applicable: the call writes nothing |

Errors: 401 no session (MSG-P4-001), 403 no right of the read (MSG-P4-002), 422 a query the service cannot accept (MSG-GEN-002, MSG-GEN-003), 503 the store or a consumed contract unavailable (MSG-GEN-006). The shape of the v2 element, its member types, its paging and its held-date status are fixed by RWB-P10-E2031-CON and its contract tests (ASM-0964).

Two further rwb-agent operations are used by the screen and are provided under the baseline of RWB-P10-E1063-CON, not re-declared here: `GET /api/recovery/agent/v1/admin/agent-runs` with query agent, from and to answering AgentRun[], the drill-down of a metric row, and `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` answering AgentOutput[] under the Case record read.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision (RWB-P7-E2005-CON) | AC1 and the override panel: the decision records of an agent version over a date range with the recommendation, the final call and the override reason; the agent-version filter is Not specified in the source documents (GAP-0629; ASM-0960) | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | The check of LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE before a segment filter is applied and before a DRIFT row is written | One hop, 2 s |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | AC1 and AC3: the published measures of the business date or month, with their definition and their value, shown beside the aggregate | One hop, 2 s |
| POST | the rwb-comms notification operation: Not specified in the source documents (GAP-0629; ASM-0961) | P6 rwb-comms | AC2: one notice of MSG-P10-006 to the policy alert role and to RW-RISK | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (ADR-020); rwb-agent calls no service through another service and holds no schema client of another service. The override panel is composed on the screen by the gateway-bff route from this read and the decision-log read, because the element carries the rate and the reason codes are the ledger's (DP-19).

#### 12.3 Events published

None by this story. The reporting feed stays `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` with its retry topic and its `.dlt` topic, published by the run path of RWB-P10-E1058-APP through the outbox relay and consumed by rwb-reporting: this story adds no member to the agent topic, because a DRIFT alert is one `agent_alert` row and one notice, not an event, and LOV-AGENT-ALERT already holds DRIFT and COST_CAP (ASM-0961).

#### 12.4 Events consumed

None. The drift check reads the rows of `rwb_agent` for the two 7-day windows and the values through the contracts of 12.2; it subscribes to no topic. The consumers of EV-28 are rwb-decision, rwb-document, rwb-deviation and rwb-reporting, not this service.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunDailyRollupWorkflow | Workflow, one per business date, workflow ID = the business date; the v1 workflow, extended by this story | `rwb-agent` | Input: the business date, the requested-by role and the manual-start flag. It runs `agentRunDaily` and then `agentDrift`. Ends COMPLETE, HELD or FAILED with the counts of the date and the drift outcome |
| aggregateAgentRuns (the legacy `agentRunDaily` step) | Activity | `rwb-agent` | Output: the daily aggregate rows of the date, per agent, policy version, prompt version, model version and segment, with the count-check result |
| agentDrift (the legacy `agentDrift` step) | Activity, new in this story | `rwb-agent` | Output: the DRIFT rows of the date, one per agent, segment and date on the unique key, and the segments that were not checked for want of feedback |
| dispatchAgentAlerts | Activity, reused | `rwb-agent` | Output: the notice requests of MSG-P10-006 and the outbox rows; no partial write |

The workflow runs on the queue and in the namespace of the service (§R4); the workflow and the Schedule names are the v1 names, and the `agentDrift` name is the legacy step name (ASM-0958).

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| AgentRunDailyRollup | Daily at 01:30 Asia/Bangkok for the previous business date; overlap policy SKIP; catch-up window one business date; the `agentDrift` activity after `agentRunDaily` inside the same workflow identity; a manual start for any business date through the same identity | Registered by RWB-P10-E1063-OPS through the workflow kit of RWB-PLT-E1071-CON in namespace `rwb-recovery` and re-registered with the added step by RWB-P10-E2031-OPS; the name is the v1 name, and no separate Schedule is created (ASM-0958) | The legacy Quartz entry of JOB-15 at 01:30, its `agentRunDaily` step and its `agentDrift` step (legacy sections 4 and 12) |

The legacy job table is not read and the legacy rerun operation is not called: a rerun for a business date is a manual start of the same workflow identity, which is what AC7 asserts (DP-10).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_alert | P10 (`rwb_agent`) | The DRIFT rows of this story on the table v1 created by `V<version>__agent_alert.sql` (its version in the rwb-agent Flyway sequence); one row per agent, type, segment and business date; `sent_at` empty until the send succeeds |
| agent_run | P10 (`rwb_agent`) | Read for the runs, the fallback, the latency, the tokens, the cost and the segment of the date; no column added |
| agent_feedback | P10 (`rwb_agent`) | Read for the acceptance and correction of the L1 output and for the two 7-day windows; no column added |
| agent_policy | P10 (`rwb_agent`) | Read for the mode, the segment of the policy, `watch_measures` and the alert role; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox and idempotency envelope of the notices (the decision-record and event library of RWB-PLT-E1027-CON) |

No table is created and no lake table exists (DP-15; Architecture v5 slide 37). rwb-agent reads no table of another service and holds no foreign key across services: the decision records come through the rwb-decision contract, the lists through the rwb-case contract and the measures through the rwb-reporting read. `V<version>__agent_monitor_index.sql` creates the index on `agent_run` that the legacy migration named, `(agent_code, segment_product_group, segment_region_code, run_at)`, and one index on `agent_feedback (created_at)` for the two windows, in the rwb-agent Flyway sequence of `rwb_agent`, and touches no other schema (ASM-0963).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision WireMock | The P7 decision-log read of RWB-P7-E2005-CON | The decision records of agent version "P2" for 2026-12-01 to 2026-12-14 with their recommendation, final call and override reason; the two-week acceptance figures 0.8600 and 0.7500; an override reason code with its count; a delay beyond 2 s |
| rwb-case WireMock | The P3 reference-data contract of RWB-P3-E1043-CON | LOV-PRODUCT with MORTGAGE, LOV-REGION with BKK, LOV-AGENT with INTAKE and SCREENING, LOV-AGENT-ALERT with DRIFT and COST_CAP, LOV-ROLE with RW-COE and RW-RISK; a delay beyond 2 s |
| rwb-reporting WireMock | The P9 measures read | The published token and cost measures of November 2026 for INTAKE; a measure that is not published for the date; a delay beyond 2 s |
| rwb-comms WireMock | The P6 notification path | An accepted notice with its reference for MSG-P10-006; a 503; an accepted notice for the data steward |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the metric read, the run drill-down and the decision-log read of the override panel, one hop, with the JSON media type preserved |

Every fixture is synthetic and holds no personal data. No test calls the model endpoint INT-23: the run rows and the feedback rows of the fixture are written by the store, not by a model call.

Contract fake library version: Not specified in the source documents (DOR-RWB-P10-E2031-APP-22).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 provided by the baseline and used, 4 consumed | The v2 metric read provided; the run drill-down and the case agent-outputs read used from the baseline of RWB-P10-E1063-CON; the P7 decision log, the P3 lists, the P9 measures and the P6 notice consumed, one hop and 2 s each |
| Kafka | None published or consumed by this story | The reporting feed is EV-28 on `rwb.agent.events.v1` with the retry and `.dlt` topics, published by the run path of RWB-P10-E1058-APP and consumed by rwb-reporting; a DRIFT alert publishes no event |
| Temporal | 1 workflow, 4 activities, 1 Schedule | AgentRunDailyRollupWorkflow with aggregateAgentRuns, agentDrift and dispatchAgentAlerts on the queue `rwb-agent`, started by AgentRunDailyRollup at 01:30 |
| File | None | No extract, no lake credential and no file path: the figures leave as the body of the read and the feed leaves as events |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.monitor`, module `monitor`, Java package `th.co.scb.ace.workbench.recovery.agent.monitor` inside the rwb-agent service; front end `src/modules/recovery/agent/monitor/`.

**Patterns applied.** DP-03, DP-07, DP-10, DP-13, DP-15 and DP-19, each with the dependency it adds in the table below.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/` with one version segment for every module | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies of this table are the ones in the metadata rows. DP-03 is carried by this key because the legacy `decision_log_entry` read is a decision-log read: the record of an agent recommendation and of its override is written by the flows that record them through the local decision-record library and reaches the central ledger of rwb-decision on `rwb.decision-record.v1`, and this story reads that ledger through the rwb-decision contract; the library contract is the one the story's fixture envelope and its tests are built against (ASM-0960).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentMetricsService | Service | Applies BR1, BR2 and BR8: builds the v2 element per agent, policy version, prompt version, model version, segment and day from `agent_run`, `agent_feedback`, `agent_policy` and the decision records read through the contract |
| DriftCheckStep, `agentDrift` | Service and activity | Applies BR3 and BR5: the two 7-day windows, the minimum feedback, the 10-point fall, the threshold and one DRIFT row per agent, segment and date |
| CostReconciliationQuery | Repository | Applies BR4: compares the daily rows of a month with the sum of `agent_run` and answers the token difference |
| AgentMetricsController | Controller | The v2 read on `/api/recovery/agent/v1`, its query, the two filter refusals, the status of a held date and the error mapping (DP-13) |
| AgentAlertRepository | Repository | Writes and reads `agent_alert` in `rwb_agent` only, on the unique key (DP-15) |
| DecisionLogClient | Client | Reads the decision records of an agent version through the rwb-decision contract, one hop and the 2 s budget (ASM-0960) |
| ReferenceDataReader | Client | Reads LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE through the reference-data contract (DP-07) |
| MeasureReader | Client | Reads the published measures of rwb-reporting beside the aggregate |
| NoticeClient | Client | Calls the rwb-comms notification path for MSG-P10-006 and maps the refusal to the outbox retry |
| AgentMonitorPage, OverrideReasonPanel | React components | SCR-46 with the agent, segment and date filters, the state badges Shadow, live and paused, the reconciliation flag and the count of override reasons per agent and month |

**Database and migrations**

- `V<version>__agent_monitor_index.sql` (the next free version of the rwb-agent Flyway sequence) creates `ix_agent_run_segment` on `agent_run (agent_code, segment_product_group, segment_region_code, run_at)` - the index the legacy migration named - and one index on `agent_feedback (created_at)` for the two windows, in `rwb_agent`, in the rwb-agent Flyway sequence, and touches no other schema (DP-15; BR11; ASM-0963).
- No table is created: the DRIFT rows use `agent_alert` from the v1 migration `V<version>__agent_alert.sql`, whose `alert_type` is LOV-AGENT-ALERT and holds DRIFT beside COST_CAP, and whose unique key is (agent_code, alert_type, segment, business_date).
- No `agent_run_daily` table, no lake table and no extract table is created (Architecture v5 slide 37).

**Configuration and reference data**

- `agent_policy.watch_measures` holds `drift_points` 10, `min_feedback` 20 and `window_days` 7 for each L1 policy (`min_feedback` is a key of the `watch_measures` value, not a dictionary field) (assumed values; the legacy story assumes 10 and 20 and adds the window), loaded by RW-COE and approved by RW-RISK, read at run time and appearing nowhere in the source (ASM-0962).
- LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE, in force in rwb-case and read through its reference-data contract (DP-07).
- The range limits of the screen - 1 and 92 days - as configuration values, named by MSG-GEN-002 and held nowhere as a literal (ASM-0968).
- The notification template of MSG-P10-006 in the rwb-comms template set, with the text of section 14 unchanged.
- The legacy feature flag `rwb.agent.monitor-v2` is kept as the legacy reference: off, SCR-46 shows runs and fallbacks only and the `agentDrift` activity is skipped.

**Build steps**

1. `V<version>__agent_monitor_index.sql`, the two indexes and the AgentAlertRepository write of a DRIFT row on the unique key (AC2, AC7; BR5, BR11).
2. DecisionLogClient against the rwb-decision fake, with the missing-read path of X7 and the override rate of BR2 (AC1).
3. ReferenceDataReader against the rwb-case fake, with the segment check of the filter (AC1, AC5; DP-07).
4. AgentMetricsService with the two-week fixture - INTAKE 140 feedback with 119 accepted and the rate 0.8500, the modes of SCREENING - and the v2 element (AC1; BR1, BR2, BR8).
5. DriftCheckStep and the `agentDrift` activity with the two windows 0.8600 and 0.7500, the threshold 0.7600, the minimum 20 and the "not enough feedback" path (AC2, AC4, AC7; BR3, BR5).
6. CostReconciliationQuery with the November 2026 fixture of 3,100 runs, 2,945,000 and 465,000 tokens and the token difference of a month that does not reconcile (AC3; BR4).
7. AgentMetricsController and the v2 read on `/api/recovery/agent/v1`, with the 422 of MSG-GEN-003 and MSG-GEN-002 and the held-date status (AC5, AC6; BR9, BR10).
8. dispatchAgentAlerts and NoticeClient against the rwb-comms fake, with the outbox retry and the `sent_at` rule (AC2).
9. Pipeline scans: no lake table, no lake credential, no `agent_run_daily`, no other service's table name and no literal of the drift points, the minimum feedback, the window or the range limits (BR3, BR11).
10. The `agentDrift` activity registered in the workflow and the Schedule step verified against the workflow kit stub, with a manual start for the same identity (AC7; DP-10).
11. gateway-bff route contract test in front of the metric read and the override panel (AC1; DP-19).

**Done when.** The eight test cases of section 16 pass, the v2 read answers on `/api/recovery/agent/v1` with the fixture figures for 2026-12-01 to 2026-12-14, `agentDrift` writes one DRIFT row for INTAKE segment MORTGAGE/BKK on 2026-12-14 with measured 0.7500 and threshold 0.7600 and sends MSG-P10-006, a segment with 12 feedback entries raises no row, the rerun for the date leaves the same row and no second notice, the two refusals answer 422 with their messages, the November month answers 3,410,000 tokens and 170.5000 baht or the token difference, the pipeline scan finds no lake artefact and no literal of a policy value, and RWB-P10-E2031-OPS has re-registered the Schedule with the added step in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-006 | Acceptance falls by 10 points or more | {agent} acceptance for {segment} fell from {from} to {to} percent in the week to {date}. |
| MSG-GEN-003 | Filter dates in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-002 | Filter range above 92 days | {field} must be between {min} and {max}. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | 401, no valid session or no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-GEN-006 | 503, the store or a consumed contract unavailable | {system} is not available. Your request is queued and will be retried. |

The texts of MSG-P10-006, MSG-GEN-003, MSG-GEN-002 and MSG-P4-002 are copied unchanged from RWB-E2-031. MSG-P4-001 and MSG-GEN-006 are the existing messages of the Error and Message Standard v4 that API Specification v5 `rwb-agent.yaml` names for 401 and 503; this story adds no new message ID. Thai text for each message follows decision DL10. In AC2 the {agent} value is "INTAKE", {segment} is "MORTGAGE/BKK", {from} is 0.8600, {to} is 0.7500 and {date} is 2026-12-14. In AC5 the {field} value is "from" and {other} is "to". In AC6 the {field} value is the date range, {min} is 1 and {max} is 92. In the access test the {action} value is "open the agent monitoring dashboard".

### 15. Screens and states

SCR-46 Agent monitor, from the Administration menu, served through the gateway-bff route (DP-19). States per agent and segment: Shadow (mode SHADOW: runs, fallbacks and evaluation scores, no acceptance), live (mode L1: all measures), paused (mode OFF: history only). Common states: loading (skeleton rows), empty ("No agent runs in this period."), error (message at the top), not enough feedback (either 7-day window holds fewer than 20 entries), not reconciled (the daily rows and the run sums of a month differ, with the token difference shown), and override unavailable (the rwb-decision read did not answer, so the rate is marked and no figure is guessed; X7). No access: Not specified in the source documents (CG-ALL-2790). The user filters by agent, segment and dates, opens a row to see the runs through `GET /api/recovery/agent/v1/admin/agent-runs`, and opens the override reasons, which the route composes from the rwb-decision decision-log read. The screen shows no prompt text and no agent output content. The exact path of the gateway-bff route in front of the screen is Not specified in the source documents (GAP-0629; ASM-0967).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-031-08 | Access | Contract | RW-CASEOWN opens SCR-46; refused with MSG-P4-002 through the route |
| TC-E2-031-01 | AC1, BR1, BR2, BR6 | Component | INTAKE MORTGAGE/BKK 140 feedback, 119 accepted, rate 0.8500; SCREENING live for MORTGAGE and BKK and Shadow elsewhere |
| TC-E2-031-02 | AC2, BR3 | Component | Acceptance 0.8600 then 0.7500; one DRIFT row measured 0.7500 and threshold 0.7600 on 2026-12-14 and one notice |
| TC-E2-031-03 | AC3, BR4 | Component | November 2026: 3,100 runs, 2,945,000 and 465,000 tokens, 3,410,000 in total and 170.5000 baht; a month that does not reconcile |
| TC-E2-031-04 | AC4, BR3 | Component | 12 feedback entries in the week to 2026-12-14; no DRIFT row and "not enough feedback" |
| TC-E2-031-05 | AC5 | Component | From 2026-12-14 to 2026-12-01; 422 and MSG-GEN-003 |
| TC-E2-031-06 | AC6 | Component | From 2026-08-01 to 2026-12-14; 422 and MSG-GEN-002 naming 1 and 92 days |
| TC-E2-031-07 | AC7, BR5 | Component | AgentRunDailyRollupWorkflow started manually again for 2026-12-14 with the same workflow identity; no second row and no second notice |
| TC-E2-031-09 | AC8, BR12 | Access | A role without Platform administration R opens SCR-46; refused with 403 and MSG-P4-002 through the route |
| TC-E2-031-10 | AC9, BR7 | Component | The agentDrift activity runs after the aggregate inside the same workflow identity of the Schedule AgentRunDailyRollup; no separate Schedule is created |
| TC-E2-031-11 | AC9, BR8 | Contract | The v2 element adds the seven members to the v1 element with four-decimal rates; no v1 member is removed, renamed or retyped |
| TC-E2-031-12 | AC9, BR9 | Contract | The read is served on /api/recovery/agent/v1 and reached only through the gateway-bff route; no screen calls rwb-agent directly |
| TC-E2-031-13 | AC9, BR10 | Component | A from after to is refused with 422 and MSG-GEN-003; a range above 92 days is refused with 422 and MSG-GEN-002; the limits are configuration |
| TC-E2-031-14 | AC9, BR11 | Component | The migration V<version>__agent_monitor_index.sql runs in the rwb-agent Flyway sequence and the story creates no table |
| TC-E2-031-15 | AC9, BR12 | Contract | A role without the right of the read is refused with 403 and MSG-P4-002 through the route |
| TC-E2-031-16 | AC10 | Contract | No session gives 401 and MSG-P4-001; a role without the right gives 403 and MSG-P4-002; the 404 trigger is Not specified in the source documents (NEWAC-RWB-P10-E2031-APP-AC10) |
| TC-E2-031-17 | AC11 | Component | agentDrift fails or exceeds its timeout; retry count and timeout Not specified in the source documents (NEWAC-RWB-P10-E2031-APP-AC11) |
| TC-E2-031-18 | AC12 | Component | The rwb-decision decision-log read is unavailable or beyond the 2 s budget (X7); the row keeps acceptance, fallback, latency and cost and guesses no override figure |
| TC-E2-031-19 | AC2, AC4, BR3 | Component | Exactly 20 feedback entries in each of the two 7-day weeks with a fall of 10 points or more; one DRIFT row is written (boundary of the minimum and the threshold) |

TC-E2-031-01 to TC-E2-031-08 are the legacy test cases of RWB-E2-031, kept with their legacy IDs, their legacy order and their legacy data; the legacy System level maps to Component, and TC-E2-031-08 keeps its Access coverage at Contract level because the refusal is proved through the route and the published contract. The lake wording of TC-E2-031-03 and the JOB-15 wording of TC-E2-031-07 are the two adaptations, and their values - 3,100 runs, 2,945,000 and 465,000 tokens, 3,410,000 in total, 170.5000 baht and 2026-12-14 - are the legacy ones. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: drift points, minimum feedback, the window, the range limits, the alert role and the list codes are configuration and contract values read at run time, and a missing policy value stops the drift check instead of falling back to a default (BR3, BR10).
- No personal data in logs, tests, screen fields or notices: the measures hold counts, rates, times and amounts only, the fixtures are synthetic, and no account number, name or national ID appears in a payload (legacy section 17).
- No read of another service's tables and no schema client: the decision records come through the rwb-decision contract, the lists through the rwb-case contract, the measures through the rwb-reporting read and the notice through the rwb-comms path; the story reads `rwb_agent` only.
- The screen shows no prompt text and no agent output content (legacy section 17), and the override panel shows codes and counts, never a free-text reason.
- One table already exists for the alert and this story creates none: `agent_alert` in `rwb_agent`, written only through its repository, and the two indexes arrive by `V<version>__agent_monitor_index.sql` (BR11).
- One hop and a 2 s client budget on every consumed REST call (ADR-020); the run of an agent keeps its own 60-second budget inside the service (NFR-010).
- The screen and the read are reached through the gateway-bff route and never from a screen to the service (DP-19).
- The drift check is idempotent on the business date: the workflow identity is the date, the alert key is the agent, type, segment and date, and a rerun replaces nothing and raises no second notice (BR5, BR7).
- No lake table, no lake credential, no extract file and no data-set job exists in this story or in its release (Architecture v5 slide 37; ADR-018).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched (the legacy text names the data lake copy, which the target removes; the copy becomes the event feed into rwb-reporting) | Business Requirements Program, section 5.7; Business Requirements Epic 2, section 3.10 | FEAT-AGT-06 | 15 Manage performance, data and AI | R-UNI-40 | TC-E2-031-01, TC-E2-031-02, TC-E2-031-03, TC-E2-031-04, TC-E2-031-05, TC-E2-031-06, TC-E2-031-07, TC-E2-031-08 |
| REQ-APD-005 | An override needs a coded reason, reported monthly | Business Requirements Program, section 5.7; Business Requirements Epic 2, section 3.10 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-01 |
| D-RCV-60 DP-03 | The decision record of a recommendation and of its override reaches the ledger through the local library on `rwb.decision-record.v1`, and is read through the rwb-decision contract | Template and Rules §R5.5 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-01, TC-E2-031-02 |
| D-RCV-60 DP-07 | The product, region, agent, alert-type and role lists are read from the rwb-case reference-data contract | Template and Rules §R5.5 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-01, TC-E2-031-05 |
| D-RCV-60 DP-10 | The drift check is the `agentDrift` activity of the Temporal Schedule `AgentRunDailyRollup`, and no job table is read | Template and Rules §R5.5; ADR-016 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-02, TC-E2-031-07, TC-E2-031-19 |
| D-RCV-60 DP-13 | The v2 read is served on the base `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-01, TC-E2-031-05, TC-E2-031-06 |
| D-RCV-60 DP-15 | The two indexes arrive with the service's own Flyway migration in its own schema | Template and Rules §R5.5; ADR-021 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-02, TC-E2-031-07 |
| D-RCV-60 DP-19 | SCR-46 and the read are reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-08 |
| NFR-008 | A screen responds within its target under normal load, under 2 seconds | TSD P10 Agent runtime v2 T7 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | TC-E2-031-01, TC-E2-031-03 |
| RWB-E2-031 (legacy story) | Agent monitoring dashboard v2 [E3d]: the seven criteria AC1 to AC7 and the access test | Business Requirements Epic 2, section 3.10; Business Requirements Program, section 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | The eight legacy test cases of section 16 |
| RWB-ITG-E2031-ITG (integration copy) | The same behaviour proved across rwb-agent, rwb-decision, rwb-reporting and the edge on the real services, with the `-ITG` test cases | Business Requirements Epic 2, section 3.10 | FEAT-AGT-06 | 15 Manage performance, data and AI | None | The test cases of that story |

The gap GAP-0629 records the areas the sources leave open for this story - the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right - and each default it raises is settled by ASM-0958 to ASM-0970.

### 19. Out of scope

- The aggregate of the business date, the cost-cap alert and the metric read that v1 provides: RWB-P10-E1063-APP.
- The cross-service behaviour of this key: RWB-ITG-E2031-ITG, and the harness RWB-ITG-W1J01-ITG.
- The contract of the v2 element, the drift row, the Schedule step and the fakes as published artefacts: RWB-P10-E2031-CON.
- The deployment of this capability - chart, migration job, worker, topic, Schedule registration, contract wiring, alerts, route, runbook and rollback: RWB-P10-E2031-OPS.
- The agent runtime, the segment on the run row, the policy and prompt store and the publication of EV-28: RWB-P10-E1058-APP.
- The recording of the L1 verdict in `agent_feedback`: RWB-P10-E2028-APP and RWB-P10-E2029-APP.
- The evaluation harness and the score rows: RWB-P10-E1060-APP and RWB-P10-E1061-CON.
- The central ledger, the decision records and the override reason codes: P7 rwb-decision, read through RWB-P7-E2005-CON.
- The measure definitions, the snapshots and the published measures: P9 rwb-reporting, and the steering dashboard of RWB-E2-009.
- The notification path, the template and the delivery of MSG-P10-006: P6 rwb-comms.
- The right check and the refusal of a role without the right of the read, as a behaviour of its own: rwb-access; this story proves it only through the route and TC-E2-031-08.
- Drift detection that raises a decision with an owner and a date (FEAT-AGT-13, Epic 3).
- Changing an autonomy level from SCR-46 (FEAT-AGT-12, Epic 3; FEAT-AGT-15, Epic 8).
- Agent risk review at the committee (FEAT-AGT-16, Epic 8).
- A lake table, an extract file, a lake credential or a data-set job, which have no target (GAP-0629).
