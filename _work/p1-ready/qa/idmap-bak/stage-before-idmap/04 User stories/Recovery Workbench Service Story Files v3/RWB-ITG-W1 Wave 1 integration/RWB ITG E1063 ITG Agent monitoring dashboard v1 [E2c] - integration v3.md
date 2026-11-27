# RWB-ITG-E1063-ITG Agent monitoring dashboard v1 [E2c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- The JOB-15 run record and rerun belong to its owner rwb-reporting, not to rwb-source-data, whose job operations serve only its own runs (RD-P1-012; findings #1, #2); the owner operations are pending (GAP-3271).
- The rwb-source-data freshness read is stated with its published values `LOADED` and `STALE` and is not the source of the held state of the report (RD-P1-005, RD-P1-041; finding #3).
- ASM-0527 is superseded in part; contract version stated and AC18 added (findings #4, #6).
- Left pending: rerun of a completed JOB-15 date (finding #5, NEW-GAP-F03-3).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1063-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-063 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P2-E1007-APP, RWB-P10-E1063-APP, RWB-P4-E1063-APP, RWB-P6-E1063-APP |
| Contract dependencies | C RWB-P10-E1063-CON, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON |
| Contract version | /v1 path of each contract in section 18 (DP13); rwb-source-data.yaml 5.1.0 (API Specification v7) for the freshness read; no other minor version is specified in the source documents (DOR-RWB-ITG-E1063-ITG-23) |
| Integration dependencies | RWB-P2-E1007-APP, RWB-P10-E1063-APP, RWB-P4-E1063-APP, RWB-P6-E1063-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-012, RD-P1-041 |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-063 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 12 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register): version 3, JOB-15 run record and rerun moved from rwb-source-data to its owner (GAP-3271); freshness values aligned with RD-P1-005 and RD-P1-041.

### 1. Story

As a **QA integration engineer** proving the legacy agent monitoring dashboard end to end on the real SIT services of the plan's integration list - rwb-integration (P2), rwb-agent (P10), rwb-access (P4) and rwb-comms (P6), with rwb-source-data (P1) and rwb-reporting (P9) as wave-1 published-contract preconditions - I want **one suite that runs the JOB-15 daily extract for 2026-12-01, reads the daily agent measures from the reporting read model, raises and reads the one cost alert, reruns the same business date, refuses the two roles that hold no right, and proves that no data lake exists**, so that **every agent is still watched from its first shadow run on real services, with the dashboard proved through published contracts and not through a lake copy**.

### 2. Business rationale

An agent in shadow that times out on one case in five, or that spends twice its budget, must be seen in the first week, not at the L1 review. RWB-E1-063 gave the risk and model risk officer one dashboard with runs, acceptance, override, fallback, latency, cost and evaluation score per agent and version, and one alert when an agent's daily cost passed its policy limit. The legacy story reached that by copying the daily agent runs to the data lake table agent_run_daily inside JOB-15 at 01:30, matching the row count against the source, and letting the Power BI page read the copy rather than the live tables (REQ-DRI-009). The copy, the count check and the alert all lived in one module.

The target removes the data lake. Arch v5 slide 37 replaces "Data lake and Power BI feed (INT-19/20)" with "Removed: reports from rwb-reporting", and DP-17 records it as a decoupling with no dependency added. The legacy agent_run_daily lake table therefore has no target, and the Power BI claim of a lake copy has no source. What replaces it is a read model in P9 rwb-reporting, built from `rwb.agent.AgentRunCompleted.v1` published by P10 rwb-agent and from the daily step that P10 runs, and read by the dashboard through `GET /api/recovery/reporting/v1/reports/measures`. The nightly job is still JOB-15 at 01:30, but Arch v5 slide 44 makes it an Airflow trigger owned by rwb-reporting that calls the P10 daily step once per business date, and the job record and the rerun are read and requested through P1 rwb-source-data at `GET /api/recovery/source-data/v1/admin/jobs` and `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun`. The cost alert stays where it was: the alert row is P10 data, and MSG-P10-004 reaches the policy alert role and RW-RISK through the P6 rwb-comms notification contract, kept and retried by the JOB-11 outbox relay when P6 is unavailable.

The component copies are RWB-P10-E1063-APP, which builds the measure read, the alert and the daily step inside rwb-agent, RWB-P4-E1063-APP, which publishes the rights and the session read, RWB-P6-E1063-APP, which publishes the notification contract, and RWB-P2-E1007-APP, whose outbound-item read proves that the extract produces no file. This integration story exists because the facts that make the dashboard trustworthy cannot be proved inside one service. The daily row is built in one service (P9) from an event and a step of another (P10), and only a run that reads both can assert that the figures the dashboard shows equal the counts of the agent runs. The count check is a comparison between two services, so a held publish is a joint fact. The alert is raised in P10 and delivered by P6, so the delivery, the single delivery and the retry after an outage are joint facts. The rerun is requested through P1 while the work happens in P9 and P10. And the removal of the data lake is an absence, which can only be proved by a preflight that fails if a lake table, a lake schema, INT-19 or INT-20 or an outbound file appears anywhere in the environment.

The suite therefore carries no legacy criterion: every criterion of this story is new (D-RCV-60) and is written to prove the deliverable in the title on real services, with the legacy values of RWB-E1-063 (agents "INTAKE" and "SCREENING", policy "P1", prompt "PR1", business date 2026-12-01, INTAKE 120 runs with 9 fallbacks and 1,840.0000 baht, SCREENING 150 runs with 21 fallbacks and 2,310.5000 baht, daily_cost_cap_thb 2,000, alert_role "RW-COE", fallback rate 0.0750, alert type "COST_CAP", measured 2,310.5000, threshold 2,000, agent "EXTRACT" with no runs, 2,000.0000 baht on 2026-12-02, the previous report date 2026-11-30, MSG-P10-004, MSG-P1-001 and MSG-P4-002, JOB-15 at 01:30 and the JOB-11 outbox relay under R-UNI-33, R-UNI-35 and R-UNI-40) so that a reader can follow the legacy story beside it.

The only thing that is faked is the outside world: the notification path that P6 calls is recorded by a capture stub, so that MSG-P10-004 can be read without an SMS or a LINE message leaving the building, a clock places the suite between 2026-11-30 and 2026-12-02, a switch makes the notification interface unavailable at 01:40, and the W1J01 synthetic fixture set supplies the runs, the policies and the identities. P1, P2, P4, P6, P9 and P10 are the real services on their published SIT contracts, and a run that needs a fake for any of them fails the preflight, because a fake would defeat the purpose of the run (ASM-0528).

The measures the suite asserts are the legacy measures by name - runs, answered, fallback, median and 95th percentile latency, tokens, cost and the latest evaluation score per agent, policy version and prompt version - because the P9 read model row shape is not specified in the sources and only the legacy column list is (ASM-0526). The Power BI page itself has no source without a lake, so for this suite the dashboard is the P9 report read of the same measures, and the Workbench reporting workspace, its stale banner and the SCR-46 agent monitor screen stay for Epic 2 (ASM-0530). Where the daily read model, the reporting read and the job record owner are not named for the target, the story cites GAP-0372 and proceeds on the defaults recorded in ASM-0525, ASM-0527 and ASM-0529.

### 3. Preconditions

- RWB-P2-E1007-APP is done: rwb-integration (P2) is deployed and serves `GET /api/recovery/integration/v1/admin/outbound-items`, which lets the suite assert that the daily extract produced no outbound item and no file.
- RWB-P10-E1063-APP is done: rwb-agent (P10) serves the measure read, the run read, the evaluation read and the configuration read of section 12.2, writes agent_alert, runs the daily step that hands the measures to P9, and publishes `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`.
- RWB-P4-E1063-APP is done: rwb-access (P4) serves `GET /api/recovery/access/v1/me/session` and refuses a right the caller does not hold with MSG-P4-002.
- RWB-P6-E1063-APP is done: rwb-comms (P6) serves the case message send and the notice read of section 12.2 through its published notification contract.
- The wave-1 published contracts the run needs are preconditions, not integration dependencies: P9 rwb-reporting serves `GET /api/recovery/reporting/v1/reports/measures` over its own read model, and P1 rwb-source-data serves the data-product freshness read of section 12.2 (ASM-0525). The job view and rerun of JOB-15 are not rwb-source-data operations (RD-P1-012).
- Agent "INTAKE" and agent "SCREENING" have policy version "P1" approved with daily_cost_cap_thb 2,000 and alert_role "RW-COE", and prompt version "PR1" approved; agent "EXTRACT" has an approved policy and no runs on 2026-12-01.
- JOB-15 exists as an Airflow trigger at 01:30 Asia/Bangkok that calls the P10 daily step once per business date, and its run record is readable through the job operations of its owner rwb-reporting (Pending: paths and shapes, owner solution architect, tracked as GAP-3271).
- The JOB-11 outbox relay runs in every service every minute, so an alert whose notification failed is retried without a second alert row (ASM-0528).
- The P6 notification capture stub is deployed and records the MSG-P10-004 message and its recipients at the outside notification path that P6 calls (ASM-0528).
- The harness RWB-ITG-W1J01-ITG is available with the synthetic run fixture of 2026-12-01, the policy fixture, the identity set and the topic, queue and namespace wiring of wave 1.
- The SIT environment is available with `rwb.agent.events.v1` and its retry and `.dlt` topics, the schema registry, queue `rwb-agent`, namespace `rwb-recovery` and the reporting read model of P9.
- No production data is read, copied or connected to; every agent code, business date, cost amount, role holder and identity used by the run is synthetic or a legacy fixture value.
- The release date 30 November 2026 is tentative and is copied unchanged.
- No data lake, no lake schema, no INT-19 and no INT-20 connection exists in SIT, and the preflight asserts it before the first measurement (GAP-0372).

### 4. Flow

1. QA integration engineer: runs the preflight, which reads the OpenAPI documents of P1, P2, P4, P6, P9 and P10 and the AsyncAPI document of `rwb.agent.events.v1`, fails before any assertion if a path, a field, a status code or an event schema has drifted, confirms that no fake is configured for any of the six services, and asserts the absence of a data lake: no agent_run_daily table, no lake schema, no lake connection string, no INT-19 or INT-20 connector and no Power BI dataset in the environment (AC8, AC12).
2. Harness: places the clock on 2026-12-02 and seeds the fixture through the W1J01 set - agent "INTAKE" 120 runs with 9 fallbacks and 1,840.0000 baht on 2026-12-01, agent "SCREENING" 150 runs with 21 fallbacks and 2,310.5000 baht on 2026-12-01, agent "EXTRACT" an approved policy and no runs, and the two policies with daily_cost_cap_thb 2,000 and alert_role "RW-COE" (AC1, AC5).
3. Harness: reads the policy and prompt versions in force through `GET /api/recovery/agent/v1/admin/agent-configs` and asserts policy "P1", prompt "PR1", cap 2,000 and alert role "RW-COE" for both agents, and an approved policy for "EXTRACT" (AC2, AC5, AC6).
4. Harness: fires the JOB-15 Airflow trigger for business date 2026-12-01 at 01:30 and asserts that it calls the P10 daily step once for that date and no other date (AC10).
5. Harness: reads the run record of JOB-15 for 2026-12-01 through the rwb-reporting job operation (path pending, GAP-3271) and asserts one run for the business date with its trigger, its start time and its status (AC10, AC3).
6. Harness: asserts that P10 published one `rwb.agent.AgentRunCompleted.v1` per finished run on `rwb.agent.events.v1`, and that P9 built its daily read model from those events plus the P10 daily step; it then reads the daily measures of 2026-12-01 through `GET /api/recovery/reporting/v1/reports/measures` and asserts runs, fallback rate, median and 95th percentile latency, cost and the latest evaluation score per agent, policy version and prompt version, with "INTAKE" at 120 runs and fallback rate 0.0750 and acceptance and override at "no L1 runs" for both agents (AC1, AC8, AC12).
7. Harness: reads the P10 source counts through `GET /api/recovery/agent/v1/admin/agent-metrics` for 2026-12-01 and compares the row count and the sum of runs with the P9 read; equality is the publish condition and the figures must equal the source (AC8, AC9).
8. Harness: reads the evaluation score of the two agents through `GET /api/recovery/agent/v1/admin/agent-evaluations` and the runs per agent and version through `GET /api/recovery/agent/v1/admin/agent-runs`, and asserts that the score the dashboard shows is the latest one and that the runs and their fallbacks are the fixture ones (AC1, AC12).
9. Harness: reads the alert of 2026-12-01 through `GET /api/recovery/agent/v1/admin/agent-metrics`, asserts exactly one alert row for "SCREENING" of type "COST_CAP" with measured 2,310.5000 and threshold 2,000, asserts that no alert exists for "INTAKE", and asserts that MSG-P10-004 reached the holders of RW-COE and RW-RISK by reading the captured message at the P6 boundary and the notice through `GET /api/recovery/comms/v1/notices/{noticeId}` (AC2, AC6, AC12).
10. Harness: runs the count-mismatch path - a reporting write for 2026-12-01 that stores one row for two agent and version groups - asserts that the publish is held, that the report still shows 2026-11-30, that the step reports failed on the rwb-reporting job operation (path pending, GAP-3271), that MSG-P1-001 reaches the report reader and that the data steward is alerted (AC3, AC9).
11. Harness: reruns JOB-15 for 2026-12-01 through the rwb-reporting job operation (path pending, GAP-3271) as RW-PLATADM, and asserts that the daily rows hold the same two rows for the date and that no second alert row and no second notification exist (AC4).
12. Harness: reruns JOB-15 for 2026-12-02 with "INTAKE" cost 2,000.0000 baht, equal to the cap, and asserts that no cost alert exists for "INTAKE" on that date (AC6).
13. Harness: switches the notification interface unavailable at 01:40, raises the "SCREENING" alert again for a fresh business date, asserts that the alert row is kept with sent_at empty, then lets the JOB-11 outbox sender succeed and asserts that one message is sent and that the alert is marked sent (AC7).
14. Harness: calls the report read as synthetic user "RW-CASEOWN", confirms on `GET /api/recovery/access/v1/me/session` that the role holds no Reporting R, and asserts the refusal with 403 and MSG-P4-002; then calls the job rerun as a role that holds no Platform administration U and asserts the same refusal (AC11, AC10).
15. Harness: reads `GET /api/recovery/integration/v1/admin/outbound-items` for the whole run window and asserts that the daily extract produced no outbound item and no file, so no lake copy and no reporting file left a service (AC8, AC12).
16. Harness: scans the daily rows, the alert, the P6 message and the application logs for personal patterns, cleans up the fixture, the alerts of the synthetic dates and the capture stub, and writes the evidence report with one verdict per test case (AC13).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The row count or the sum of runs in the reporting write does not match the P10 source | The publish for the date is held, the previous date stays visible, JOB-15 reports failed on the job read of its owner (GAP-3271) and the data steward is alerted | None to a user | AC3, AC9 |
| X2 | JOB-15 runs again for the same business date | The rows of the date are replaced, not added, and no second alert is raised | None to a user | AC4 |
| X3 | An agent has no runs on the business date | One row with runs 0 and cost 0.0000, and no cost alert | None to a user | AC5 |
| X4 | Cost equals the cap exactly | No alert: an alert is raised only when the cost is above the cap | None to a user | AC6 |
| X5 | The notification interface is unavailable | The alert row is kept with sent_at empty and is sent when the JOB-11 outbox sender succeeds (R-UNI-33, R-UNI-35) | None to a user | AC7 |
| X6 | A role without Reporting R reads the report | The P9 read is refused | MSG-P4-002 | AC11 |
| X7 | A role without Platform administration U reruns a job | The rerun of the owner is refused and no job runs | MSG-P4-002 | AC10 |
| X8 | A consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC12 |
| X9 | A fake is configured for P1, P2, P4, P6, P9 or P10 | The preflight refuses the run: only the outside notification capture, the clock and the fixture set may stand outside the services | None | AC14, Section 12.8 |
| X10 | The W1J01 fixture set, or an identity or policy it carries, is missing or does not match the run | The run fails as a fixture fault and names the missing element; no production value is substituted | None | AC1, AC5 |
| X11 | A suite step tries to read a service schema directly | The step does not exist: the suite is built with no client for a service schema, and the pipeline scan fails any change that adds one | None | AC15, Section 17 |
| X12 | An outbound item or a file appears for the daily extract | The suite fails the absence assertion at the P2 boundary: a lake copy or a reporting file is not part of this story | None | AC8 |
| X13 | A data lake table, a lake schema, an INT-19 or an INT-20 connector appears in the environment | The preflight fails and names the objected artefact, so no measurement is taken against an environment that still holds the removed lake | None | AC8, GAP-0372 |
| X14 | The notification is retried more than once after the outage | The send is keyed on the alert row, so exactly one message exists for the alert and the repeat is counted (R-UNI-40) | None to a user | AC7 |

X1 to X7 are the legacy exception paths of RWB-E1-063 carried onto the real services; X8 to X14 are the failures that only appear when the run leaves one service, and X13 is the one that watches the removal of the data lake itself.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the four integration dependencies and the published contracts of P1, P2, P4, P6, P9 and P10, not their source code, and it owns no schema, no table and no operation |
| Negotiable | The fixture composition, the poll interval, the report layout and the capture-stub control are configuration; the agents, the policy and prompt versions, the dates, the run counts, the costs, the cap, the role, the alert type and the message IDs are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: a daily row built in one service from an event of another and equal to its source, a held publish on a count mismatch, one alert delivered once through another service and retried after an outage, a rerun that replaces instead of adding, two refusals, and the absence of the data lake |
| Estimable | One suite module, one job trigger control, one clock, one notification capture, six contract probes, one absence probe and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a REST response, a Kafka event, an alert read through the contract, a captured message, a job run record, a log scan or a preflight that fails on a named artefact |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v1 [E2c], proven across the wave 1 services

  Background:
    Given agents "INTAKE" (policy "P1", prompt "PR1") and "SCREENING" (policy "P1", prompt "PR1") run in shadow on 2026-12-01
    Given on business date 2026-12-01 "INTAKE" has 120 runs, 9 with fallback, cost 1,840.0000 baht
    Given on 2026-12-01 "SCREENING" has 150 runs, 21 with fallback, cost 2,310.5000 baht
    Given both policies have daily_cost_cap_thb 2,000 and alert_role "RW-COE"
    Given all involved services are deployed in SIT with their published contracts and the RWB-ITG-W1J01-ITG synthetic set is loaded with no production value

  Scenario: AC1 The dashboard shows runs, fallback, latency, cost and the evaluation score per agent and version (new, D-RCV-60)
    Given two agents in shadow on 2026-12-01
    When the dashboard reads the daily measures for 2026-12-01 through `GET /api/recovery/reporting/v1/reports/measures`
    Then the read shows runs, fallback rate, median and 95th percentile latency, cost and the latest evaluation score by policy and prompt version
    Then "INTAKE" shows 120 runs and fallback rate 0.0750
    Then acceptance and override show "no L1 runs" for both agents, because no agent runs at L1 in Epic 1

  Scenario: AC2 A cost above the cap raises one alert and notifies RW-COE and RW-RISK (new, D-RCV-60)
    Given the cost of "SCREENING" on 2026-12-01 is above the daily cap of 2,000 baht
    When JOB-15 completes for 2026-12-01
    Then one agent alert exists for "SCREENING" with type "COST_CAP", business date 2026-12-01, measured 2,310.5000 and threshold 2,000
    Then MSG-P10-004 is sent to the holders of RW-COE and RW-RISK through the P6 notification contract
    Then no alert exists for "INTAKE"

  Scenario: AC3 A copy whose counts do not match is held and the report keeps the previous date (new, D-RCV-60)
    Given the reporting write for 2026-12-01 stores 1 row for 2 agent and version groups
    When the count check runs
    Then the system holds the publish for 2026-12-01 and the report shows 2026-11-30
    Then the JOB-15 run record of rwb-reporting for 2026-12-01 reports failed and the data steward is alerted
    # Pending: the path of the job read, owner solution architect (GAP-3271)

  Scenario: AC4 A rerun for the same date replaces the rows and raises no second alert (new, D-RCV-60)
    Given JOB-15 completed for 2026-12-01 and sent the "SCREENING" alert
    When RW-PLATADM reruns JOB-15 for 2026-12-01 through the job rerun operation of rwb-reporting
    # Pending: the path of the rerun operation (GAP-3271)
    # Pending: whether the owner of JOB-15 allows a rerun of a completed business date, since the job rerun standard of RD-P1-012 refuses a run that is not FAILED with 409, owner solution architect with the rwb-reporting service owner, tracked as NEW-GAP-F03-3
    Then the daily rows hold the same 2 rows for 2026-12-01
    Then no second alert row and no second notification exist

  Scenario: AC5 An agent with no runs shows zero (new, D-RCV-60)
    Given agent "EXTRACT" has an approved policy and no runs on 2026-12-01
    When JOB-15 completes for 2026-12-01
    Then "EXTRACT" shows runs 0 and cost 0.0000 for 2026-12-01
    Then no alert exists for "EXTRACT"

  Scenario: AC6 Cost equal to the cap raises no alert (new, D-RCV-60)
    Given "INTAKE" cost is 2,000.0000 baht on 2026-12-02
    When JOB-15 completes for 2026-12-02
    Then no cost alert exists for "INTAKE" on 2026-12-02

  Scenario: AC7 A notification outage keeps the alert for the outbox retry (new, D-RCV-60)
    Given the P6 notification interface is unavailable at 01:40
    When the "SCREENING" alert is raised
    Then the alert row is kept with sent_at empty
    Then the alert is sent when the JOB-11 outbox sender succeeds (R-UNI-33, R-UNI-35)

  Scenario: AC8 The daily measures live in rwb-reporting and no data lake is used (new, D-RCV-60)
    Given the daily rows of 2026-12-01 in the P9 read model
    When the dashboard reads `GET /api/recovery/reporting/v1/reports/measures`
    Then the rows hold the legacy measures by name and equal the P10 source counts
    Then no agent_run_daily table, no data lake and no INT-19 or INT-20 connection exists, and the preflight proves the absence

  Scenario: AC9 The count check compares the reporting read to the P10 source (new, D-RCV-60)
    Given the count check for 2026-12-01
    When the row count and the sum of runs read through P9 are compared with `GET /api/recovery/agent/v1/admin/agent-metrics`
    Then a difference holds the publish and raises MSG-P1-001 to the report reader

  Scenario: AC10 JOB-15 is an Airflow trigger and its run and rerun are served by its owner (new, D-RCV-60)
    Given JOB-15 runs at 01:30 Asia/Bangkok
    When the Airflow trigger fires for 2026-12-01
    Then it calls the P10 daily step once for that business date
    Then the run record is read and the rerun is requested through the job operations of rwb-reporting
    # Pending: paths of the two operations, owner solution architect (GAP-3271)
    Then a role without Platform administration U is refused with 403 and MSG-P4-002

  Scenario: AC11 A role without Reporting R is refused on the report read (new, D-RCV-60)
    Given synthetic user "RW-CASEOWN" holds no Reporting R, confirmed on `GET /api/recovery/access/v1/me/session`
    When "RW-CASEOWN" calls `GET /api/recovery/reporting/v1/reports/measures`
    Then the read is refused with 403 and MSG-P4-002
    Then no measure row is returned

  Scenario: AC12 The alert and the measures are read through contracts only (new, D-RCV-60)
    Given the suite reads only the operations of section 12.2
    When every figure and alert fact is asserted
    Then each one comes from the P9, P10, P1, P6, P2 or P4 contract
    Then the suite holds no schema client and reads no agent_run, agent_alert, agent_policy or reporting table

  Scenario: AC13 No personal data in the daily rows, the alert or the dashboard (new, D-RCV-60)
    Given the daily rows, the alert, the P6 message and the logs of 2026-12-01
    When the scan runs
    Then they hold counts, times and amounts only
    Then the scan finds no national ID number, phone number, name or account number

  Scenario: AC14 A fake configured for P1, P2, P4, P6, P9 or P10 is refused by the preflight (new, D-RCV-60)
    Given a run is configured with a fake for one of P1, P2, P4, P6, P9 or P10
    When the preflight runs
    Then the run is refused before any assertion and only the outside notification capture, the clock and the fixture set stand outside the services

  Scenario: AC15 The suite has no client for a service schema (new, D-RCV-60)
    Given the suite and the pipeline scan of section 17
    When a suite step tries to read a service schema directly
    Then the step does not exist and the pipeline scan fails any change that adds a schema client

  Scenario: AC16 Business values come from a contract at run time, each call is one hop, the stale state is shown and the run is pinned to SIT (new, D-RCV-60)
    Given the suite and the Workbench run in SIT with the RWB-ITG-W1J01-ITG synthetic set
    When the run reads the agent codes, the cap, the alert role, the dates and the run counts
    Then each value comes from a contract at run time and no business value is held in code or in the suite
    Then every REST call is one hop to its owning service with a 2 s client budget
    Then the P9 report read returns the daily measures with the loaded and stale state, and the stale state carries MSG-P1-001
    Then the run refuses to start against any environment other than SIT and reads no production value

  Scenario: AC17 A redelivered AgentRunCompleted event changes no row and sends no second alert (new, D-RCV-60)
    Given the event rwb.agent.AgentRunCompleted.v1 for SCREENING on 2026-12-01 has been consumed once
    When the same event is delivered again
    Then the daily rows of 2026-12-01 are unchanged and no second alert row exists
    Then no second notification is sent

  Scenario: AC18 The suite uses no rwb-source-data job operation (new, RD-P1-012)
    Given the suite records every REST call it makes
    When the suite has run AC1 to AC17
    Then no call of the suite goes to a path under /api/recovery/source-data/v1/admin/jobs
```

**Target reading.** There is no data lake in this story. The daily figure of an agent is a read model in P9 rwb-reporting built from `rwb.agent.AgentRunCompleted.v1` and from the daily step that P10 runs, and it is read through `GET /api/recovery/reporting/v1/reports/measures` (DP-17; Arch v5 slide 37; ASM-0525). JOB-15 is the Airflow trigger at 01:30 owned by P9 that calls the P10 daily step once per business date, and its run record and rerun are read and requested through the job operations of rwb-reporting (RD-P1-012; ASM-0527 superseded in part; paths pending, GAP-3271). The cost alert is a P10 row and its message goes through the P6 notification contract with the JOB-11 outbox retry (ASM-0528, ASM-0529). Every path of section 12.2 sits on the base of its owner (DP-13), every call is one hop with a 2 s client budget (DP-11), and the Power BI page is replaced for this suite by the P9 read of the same measures (ASM-0530). The legacy values are copied character for character; only the carrier of the daily row, the owner of the job record and the reader of the dashboard change, and that is the change recorded in GAP-0372.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | There is no data lake: the daily agent measures are a P9 rwb-reporting read model built from `rwb.agent.AgentRunCompleted.v1` and the P10 daily step; no agent_run_daily table, no lake schema, no INT-19 and no INT-20 exist in the target | DP-17; Arch v5 slide 37; GAP-0372 |
| BR2 | The dashboard reads the daily measures through `GET /api/recovery/reporting/v1/reports/measures` only, by measure name: runs, answered, fallback, latency p50 and p95, tokens, cost, evaluation score, policy version, prompt version and business date | REQ-DRI-009; ASM-0526 |
| BR3 | A daily copy is published only when its row count and the sum of its runs match the P10 source of the same business date; otherwise the publish is held and the previous date stays visible | REQ-DRI-009; DL25 zero tolerance (assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602) |
| BR4 | A cost alert is raised when the cost of an agent on a business date is above agent_policy.daily_cost_cap_thb (2,000 baht, assumed; DL33, assumptions ASM-0135, ASM-0140, ASM-0890); a cost equal to the cap raises none | agent_policy.daily_cost_cap_thb (DF-AGT-013); ASM-0529 |
| BR5 | One alert per agent, alert type and business date, so a rerun of the same date raises no second alert | agent_alert unique key; R-UNI-40 |
| BR6 | Fallback rate = runs with fallback divided by runs, to 4 decimals; "INTAKE" at 9 of 120 is 0.0750 | agent_run.fallback (DF-AGT-047) |
| BR7 | MSG-P10-004 goes to the holders of the policy alert role and to RW-RISK through the P6 notification contract; the alert is not case-bound, so the message is proved at the P6 boundary | agent_policy.alert_role (DF-AGT-015); ASM-0528 |
| BR8 | When P6 is unavailable the alert row is kept with sent_at empty and is sent by the JOB-11 outbox relay; the send is keyed on the alert so exactly one message results | R-UNI-33; R-UNI-35; R-UNI-40 |
| BR9 | JOB-15 is an Airflow trigger at 01:30 Asia/Bangkok owned by P9 that calls the P10 daily step once per business date; it is not a Quartz job and not a Temporal Schedule | Arch v5 slide 44; ASM-0527; GAP-0616 |
| BR10 | The JOB-15 run record is read and the rerun is requested through the job operations of its owner rwb-reporting, and the rerun needs Platform administration U; rwb-source-data serves only its own runs | RD-P1-012; GAP-3271 |
| BR11 | No business value in code or in the suite: agent codes, the cap, the alert role, the dates and the run counts are read through a contract at run time | Principle 1; DT02 |
| BR12 | Every REST call of the run is one hop to the owning service with a 2 s client budget; the daily step is a step of the Airflow-triggered job and never a REST call of another service | ADR-020; DP-11 |
| BR13 | The daily rows, the alert, the P6 message and the log hold counts, times and amounts only; no national ID number, phone number, name or account number appears in any of them | Legacy section 17; CTL-11; AC13 |
| BR14 | No cross-service table read: the suite and every service read another service's data through its contract, and no agent_run, agent_alert, agent_policy or reporting table is read by the suite | DP-01; ADR-020; AC12 |
| BR15 | The Workbench reports the daily measures with the loaded and the stale state, the stale state carrying MSG-P1-001; the Power BI page and the SCR-46 screen are not built in this story | ASM-0530; legacy section 15 |
| BR16 | No production value is read, copied or connected to; the run is pinned to SIT with the synthetic set and refuses to start against any other environment | Legacy section 17; Guardrail |

### 9. State transitions

The state transitions of the JOB-15 run record:

| From | Event | Condition | To |
|---|---|---|---|
| None | Airflow trigger fires at 01:30 for a business date | The P10 daily step starts | RUNNING |
| RUNNING | P10 daily step ends | The reporting write matches the P10 source | COMPLETED |
| RUNNING | P10 daily step ends | The row count or the sum of runs differs | FAILED, with the publish held (MSG-P1-001 to the report reader) |
| FAILED | RW-PLATADM reruns the date through the owner's rerun operation | None | RUNNING, then the same two outcomes |
| COMPLETED | RW-PLATADM reruns the date through the owner's rerun operation | Pending, NEW-GAP-F03-3 | RUNNING, then COMPLETED with the rows of the date replaced |

The state transitions of an agent alert:

| From | Event | Condition | To |
|---|---|---|---|
| None | The daily step finds cost above the cap | No alert row exists for the agent, type and date | RAISED, sent_at empty |
| None | The daily step finds cost at or below the cap | None | No row |
| RAISED | The P6 notification contract accepts the message | None | SENT, sent_at set |
| RAISED | P6 is unavailable | None | RAISED, sent_at empty, waiting for the JOB-11 outbox relay |
| RAISED | The same business date is rerun | An alert row already exists for the agent, type and date | No transition and no second row |

The state transitions of the reporting read and of the dashboard read:

| From | Event | Condition | To |
|---|---|---|---|
| None | The daily step writes the date and the count check passes | None | LOADED for the business date |
| None | The count check fails | None | HELD, and the read keeps the previous business date |
| HELD | The date is rerun and the check passes | None | LOADED for the business date |
| LOADED | A later load is held | None | STALE for the reader, with MSG-P1-001 naming the date shown |

The states the run observes across the services:

| Item | States |
|---|---|
| JOB-15 run record | RUNNING, COMPLETED, FAILED |
| Agent alert | RAISED with sent_at empty, SENT with sent_at set, absent |
| Reporting read | LOADED for 2026-12-01, HELD, STALE at 2026-11-30 |
| Notification capture | No message, one message to RW-COE and RW-RISK, unavailable at 01:40 |
| Suite run | Not started, preflight failed, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixture, the clock, the notification capture, the absence probe, the cleanup and the evidence report |
| RW-RISK, risk and model risk officer | Reads the dashboard measures (Reporting R); receives the cost alert |
| RW-COE, centre of excellence analyst | Reads the dashboard measures (Reporting R); receives the cost alert as the policy alert role |
| RW-BIANAL, BI analyst | Reads the dashboard measures (Reporting R); the Power BI page itself is out of scope |
| RW-PLATADM, platform administrator | Reads the JOB-15 run record (Platform administration R) and reruns a business date (Platform administration U) |
| RW-DATASTEW, data steward | Receives the count-mismatch alert of a held publish |
| RW-CASEOWN, case owner | Nothing in this story; the report read is refused with 403 and MSG-P4-002 |
| Service owner of rwb-agent (P10) | Owns the agent tables, the daily step, the alert, the measure read, the run and evaluation reads and the topic `rwb.agent.events.v1` |
| Service owner of rwb-reporting (P9) | Owns the daily read model, the measures and the report read, the JOB-15 Airflow trigger, and the JOB-15 job view and rerun (paths pending, GAP-3271) |
| Service owner of rwb-source-data (P1) | Owns the data-product freshness read |
| Service owner of rwb-comms (P6) | Owns the notification contract, the notice and the outside notification path |
| Service owner of rwb-integration (P2) | Owns the outbound-item read that proves no file was produced |
| Service owner of rwb-access (P4) | Owns the session read and the refusal of MSG-P4-002 |
| No role | Reads a service schema directly, writes an agent or reporting table from outside its owner, connects a data lake, or takes production data into the run |

Approval levels: no delegation of authority level applies. The policy, its cap and its alert role are approved by their owners before the run; this story approves nothing.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-AGT-002 | agent_policy | agent_code | Read through the P10 contract; the fixture values are INTAKE, SCREENING and EXTRACT |
| DF-AGT-003 | agent_policy | policy_version | Read through the P10 contract; "P1" for both agents |
| DF-AGT-013 | agent_policy | daily_cost_cap_thb | Read through the P10 contract; 2,000 for both policies |
| DF-AGT-015 | agent_policy | alert_role | Read through the P10 contract; "RW-COE" |
| DF-AGT-037 | agent_run | agent_code | Read through the P10 contract and aggregated in P9 |
| DF-AGT-039 | agent_run | prompt_version | Read through the P10 contract; "PR1" |
| DF-AGT-047 | agent_run | fallback | Read through the P10 contract; 9 of 120 for INTAKE |
| DF-AGT-051 | agent_run | latency_ms | Read through the P10 contract, for the median and the 95th percentile |
| DF-AGT-052 | agent_run | tokens_in | Read through the P10 contract, for the cost |
| DF-AGT-053 | agent_run | tokens_out | Read through the P10 contract, for the cost |
| DF-AGT-054 | agent_run | cost_thb | Read through the P10 contract; 1,840.0000 for INTAKE and 2,310.5000 for SCREENING on 2026-12-01 |
| DF-AGT-056 | agent_run | run_at | Read through the P10 contract, to place a run on the business date |
| DF-AGT-089 | agent_evaluation | label_key | Read through the P10 contract and shown as the latest evaluation score |
| DF-AGT-094 | agent_evaluation | agreement_rate | Read through the P10 contract |
| DF-AGT-095 | agent_evaluation | precision_value | Read through the P10 contract |
| DF-AGT-096 | agent_evaluation | recall_value | Read through the P10 contract |
| DF-AGT-103 | agent_alert | id | Written by P10; read through the P10 measure and alert read, never the table |
| DF-AGT-104 | agent_alert | agent_code | Written by P10; read through the P10 alert read; SCREENING |
| DF-AGT-105 | agent_alert | alert_type | Written by P10; read through the P10 alert read; "COST_CAP" |
| DF-AGT-107 | agent_alert | business_date | Written by P10; read through the P10 alert read; 2026-12-01 |
| DF-AGT-108 | agent_alert | measured_value | Written by P10; read through the P10 alert read; 2,310.5000 |
| DF-AGT-109 | agent_alert | threshold_value | Written by P10; read through the P10 alert read; 2,000 |
| DF-AGT-110 | agent_alert | sent_to_role | Written by P10; read through the P10 alert read; RW-COE and RW-RISK |
| DF-AGT-111 | agent_alert | sent_at | Written by P10; read through the P10 alert read; empty until the send succeeds |
| No BR field ID in the legacy dictionary | P9 daily measure rows | runs, answered, fallback, latency_p50, latency_p95, tokens, cost, eval score, policy version, prompt version, business date | Read by name through `GET /api/recovery/reporting/v1/reports/measures`; ASM-0526 records that the P9 row shape is not specified |
| No BR field ID in the legacy dictionary | P9 job run record | job id, business date, status, start and end time | Read through the job read of rwb-reporting (pending, GAP-3271); ASM-0527 superseded in part |

Field IDs are those of RWB-E1-063 and are copied unchanged. The suite owns no field and no table: it reads every row of this table through a contract of section 12 and writes nothing. The table agent_run_daily of the legacy story is not listed because it has no target: the data lake is removed and the daily row is a P9 read model (DP-17; GAP-0372).

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation and no operation of its own. The reserved names of P2 rwb-integration - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` - are used only to read the outbound-item list of section 12.2, and no `rwb_integration` table is written. The measures belong to P9 rwb-reporting, base `/api/recovery/reporting/v1`, topic `rwb.reporting.events.v1` and schema `rwb_reporting`; the runs, the evaluations and the alert belong to P10 rwb-agent, base `/api/recovery/agent/v1`, topic `rwb.agent.events.v1` and schema `rwb_agent`.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | AC1, AC3, AC8, AC9, AC11 and AC12: the daily measures of 2026-12-01 by agent, policy version and prompt version, and the previous date 2026-11-30 when a publish is held | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | P10 rwb-agent | AC2, AC5, AC6, AC9 and AC12: the P10 source counts, the sums of runs and the alert rows of the business date | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | AC1, AC4, AC5, AC7 and AC12: the runs per agent and version with fallback, latency and cost, and no prompt text or personal field | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | AC1 and AC12: the latest evaluation score per agent and version that the dashboard shows | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | AC2, AC5, AC6 and AC12: policy "P1" and prompt "PR1" in force, daily_cost_cap_thb 2,000 and alert_role "RW-COE" | 2 s |
| GET | Pending (GAP-3271) | P9 rwb-reporting | AC3, AC4 and AC10: the JOB-15 run record per business date and its failed or completed status | 2 s |
| POST | Pending (GAP-3271) | P9 rwb-reporting | AC4 and AC10: the rerun of JOB-15 for 2026-12-01, Platform administration U, and the refusal of a role without it | 2 s |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | AC3 and AC8: `productCode`, `businessDate` and `status` (`LOADED` or `STALE`) per data product; the held and stale state of the agent measures comes from the P9 report read, not from this operation | 2 s |
| POST | `/api/recovery/comms/v1/cases/{caseId}/messages` | P6 rwb-comms | AC2, AC7 and AC12: the notification send through which MSG-P10-004 reaches RW-COE and RW-RISK, read at the P6 boundary (ASM-0528) | 2 s |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | AC2 and AC7: the notice the send produced, with its recipients and its sent time | 2 s |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | AC8 and AC12: asserts that the daily extract produced no outbound item and no file | 2 s |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | AC10 and AC11: the rights of the caller, which prove that RW-CASEOWN holds no Reporting R and that the rerun role holds no Platform administration U | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the suite calls no service through another service. The daily step is not a call of the suite: it runs inside the Airflow-triggered JOB-15 and hands its measures to P9 (ASM-0527).

#### 12.3 Events published

None. The suite publishes no business event; it observes the event of the owning service listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | What the suite asserts |
|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | One event per finished run, written to the outbox in the same transaction as the run row; run ID, agent "INTAKE", "SCREENING" or "EXTRACT", the policy and prompt versions, the business date, outcome, fallback, latency, tokens and cost, and no personal field; CloudEvents 1.0, key caseId; these events plus the P10 daily step are the only input of the P9 daily read model (AC1, AC8, AC12) |
| No lake or outbound file event | `rwb.reporting.events.v1` and `rwb.integration.events.v1` | P9 rwb-reporting and P2 rwb-integration | Asserted absent for the whole run window: no lake copy event, no `rwb.integration.FileDelivered.v1` and no reporting file event, so the daily measures never leave a service as a file (AC8, AC12) |

A consumer dedupes on the event ID through its inbox (ADR-015, DP-09). The payload of the event is the owner's published schema; the suite asserts the envelope and the fields above and never the whole body of a prompt or an answer.

#### 12.5 Workflows and activities

None. JOB-15 is an Airflow trigger that calls the P10 daily step once per business date, and the P10 daily step is a job step and not a Temporal workflow; the story starts no workflow, observes no workflow and adds no activity. The cost alert is written by the same step, and its delivery is the outbox relay of JOB-11 in every service (12.6). No AgentRunWorkflow is started by this story, because the agent runs of 2026-12-01 are fixture rows, not runs of the suite.

#### 12.6 Schedules

| Job | Owner | When | Mechanism | What the suite asserts |
|---|---|---|---|---|
| JOB-15 Reporting extract | P9 rwb-reporting | 01:30 Asia/Bangkok, once per business date | Airflow trigger that calls the P10 daily step; no Quartz table and no Temporal Schedule | The trigger of 2026-12-01 calls the P10 daily step once for that date, and the run record and rerun are read and requested through P1 (AC3, AC4, AC10; ASM-0527) |
| JOB-11 Outbox sender | every service | every minute | outbox relay to Kafka | The alert kept with sent_at empty after the P6 outage is retried until one message is sent, with no second alert row (AC7; R-UNI-33, R-UNI-35) |

No Temporal Schedule belongs to this story, and the ACE shared Quartz tables are not used (Arch v5 slides 31 and 44).

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The P9 measure tables of schema `rwb_reporting` are owned by rwb-reporting and are read through `GET /api/recovery/reporting/v1/reports/measures`; agent_run, agent_alert, agent_evaluation and agent_policy of schema `rwb_agent` are owned by rwb-agent and are read through the P10 operations of section 12.2; the job record is P1, the notice is P6, the outbound item is P2 and the session is P4. No reporting table, no agent table and no lake table is read (AC12).

#### 12.8 Contract fakes

None for a service contract. The only elements outside the nineteen services are:

| Stub | Purpose |
|---|---|
| P6 notification capture stub | Records the MSG-P10-004 message and its recipients at the outside notification path that P6 calls, so the send can be read without an SMS or a LINE message leaving the building; P6 itself is the real service (AC2, AC7; ASM-0528) |
| Clock control | Places the suite on 2026-11-30, 2026-12-01 and 2026-12-02 and sets the 01:30 and 01:40 marks of the job and of the outage, for AC2 to AC10 |
| Notification-outage switch | Makes the notification interface unavailable at 01:40, for AC7 |
| W1J01 synthetic fixture set | Supplies the 270 runs of 2026-12-01, the three policies, the two prompt versions, the two evaluation scores and the identity set; it is a fixture set, not a fake of a service |

P1 rwb-source-data, P2 rwb-integration, P4 rwb-access, P6 rwb-comms, P9 rwb-reporting and P10 rwb-agent are the real SIT services on their published contracts and are not faked in any path; a run configured with a fake for any of them fails the preflight (X9). The notification capture stands in for the outside notification path of Arch v5 slide 17, not for P6.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 12 | The P9 report read, the four P10 reads, the P1 freshness read, the two P9 job operations (pending, GAP-3271), the two P6 operations, the P2 outbound read and the P4 session read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 1 event type consumed, 2 absences asserted | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`; no lake copy event and no `rwb.integration.FileDelivered.v1`; CloudEvents 1.0, key caseId (DP-09) |
| Temporal | None | None | JOB-15 is an Airflow trigger and the P10 daily step is a job step; no workflow is started or observed (12.5) |
| File | None | None | No file in this story: the outbound-item read proves that the extract produced none (AC8) |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a job trigger control for the JOB-15 Airflow trigger and its clock, a fixture builder for the 270 runs and the three policies, a set of contract probes over P1, P2, P4, P6, P9 and P10, a notification capture and its outage switch, a count-check probe, an absence probe over the lake and the outbound items, a personal-data scan, and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns, and it builds no data lake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published OpenAPI and AsyncAPI documents, run order, report and exit code |
| JobTriggerControl | Test harness | Fires the JOB-15 Airflow trigger for a business date, places the 01:30 and 01:40 marks, and exports the call count of the P10 daily step |
| FixtureBuilder | Test harness | Loads the 270 runs of 2026-12-01, the three policies, the two prompt versions and the two evaluation scores from the W1J01 set; asserts that no production value is substituted |
| ReportProbe | Test harness | Reads the daily measures of a business date through P9 and asserts the measures by name, the figures of both agents, "EXTRACT" at zero, the fallback rate 0.0750 and the previous date 2026-11-30 when a publish is held |
| CountCheckProbe | Test harness | Compares the row count and the sum of runs of the P9 read with the P10 source, drives the mismatch path, and asserts the held publish, the stale date and MSG-P1-001 |
| AlertProbe | Test harness | Reads the alert of the business date through the P10 measure read; asserts one COST_CAP row for SCREENING at 2,310.5000 against 2,000, none for INTAKE, none for EXTRACT, none at 2,000.0000 on 2026-12-02 and none duplicated after a rerun |
| JobAdminProbe | Test harness | Reads the JOB-15 run record and requests the rerun for the same date through the operations of rwb-reporting (pending, GAP-3271), and asserts the one-run-per-date fact and the 403 refusal of a role without Platform administration U |
| NotificationProbe | Test harness | Owns the P6 capture stub and its outage switch, asserts one message per alert, the recipients RW-COE and RW-RISK, the kept alert with sent_at empty during the outage and the single send after the JOB-11 retry |
| AbsenceProbe | Test harness | Asserts at the preflight that no agent_run_daily table, lake schema, lake connection, INT-19 or INT-20 connector exists, and reads the P2 outbound-item list to prove that no file was produced |
| AccessProbe | Test harness | Reads the caller session through P4 and asserts the 403 with MSG-P4-002 for RW-CASEOWN on the report read and for the rerun role on the job rerun |
| PiiScanProbe | Test harness | Scans the daily rows, the alert, the captured P6 message and the application logs for national ID number, phone number, name and account number patterns |
| ReportWriter | Test harness | One row per test case with the evidence and the elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table, no schema object and no migration; it creates no lake table and no reporting file. The P9 measure tables and the P10 agent_alert table are the owners' own migrations (DP-15).

**Configuration and reference data**

- The SIT endpoints of P1, P2, P4, P6, P9 and P10, the topic `rwb.agent.events.v1`, the schema-registry address and the namespace `rwb-recovery`, all as configuration.
- The agents INTAKE, SCREENING and EXTRACT, policy "P1", prompt "PR1", daily_cost_cap_thb 2,000, alert_role "RW-COE", the alert type "COST_CAP", the business dates 2026-11-30, 2026-12-01 and 2026-12-02, the run counts 120 and 150, the fallback counts 9 and 21 and the costs 1,840.0000, 2,310.5000 and 2,000.0000, all read through the contracts of section 12.2 and never written in the suite code (BR11).
- The 2 s client budget, the job poll interval and the outbox retry window.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | Every figure and alert fact is a contract call: the measures through P9, the runs, evaluations and alert through P10, the job record through P1, the notice through P6, the outbound item through P2 and the session through P4; no agent table and no reporting table is read (12.7, AC12) |
| DP06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The cap 2,000 and the alert role RW-COE are policy values read through the P10 configuration read, not parameters written in code; this story needs no P3 parameter call (AC2, AC6, BR11) |
| DP07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The agent codes INTAKE, SCREENING and EXTRACT, the alert type COST_CAP and the roles RW-COE and RW-RISK are read as data through the P10 and P4 reads; the suite holds no code list of its own (AC2, AC5, AC11) |
| DP09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` is the only consumed event type and the input of the P9 read model; the alert waits for the JOB-11 outbox relay when P6 is down, and no lake copy event exists (AC2, AC7, AC8) |
| DP10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | No Quartz table and no Temporal Schedule: Arch v5 slide 44 makes JOB-15 an Airflow trigger at 01:30 owned by P9 that calls the P10 daily step, and JOB-11 stays the every-minute outbox relay of every service (AC7, AC10; ASM-0527) |
| DP11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The twelve calls of 12.2 are one hop with the 2 s client budget; the P10 daily step is a job step reached by the Airflow trigger and is never a REST call of another service (AC9, AC10; BR12) |
| DP13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 sits on the base of its owner - reporting, agent, source-data, comms, integration and access - and the preflight asserts the six bases (AC10, AC11, AC12) |
| DP15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The suite owns no schema and no migration; the P9 measure tables and the P10 agent_alert table are their owners' own sequences (12.7) |
| DP17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data | The data lake, INT-19 and INT-20 are removed (Arch v5 slide 37); the daily measures are a P9 read model built from `rwb.agent.AgentRunCompleted.v1` and the P10 daily step and read through `GET /api/recovery/reporting/v1/reports/measures`; the absence is proved at the preflight and at the P2 outbound read, and the ownership the sources do not name is GAP-0372 (AC8) |
| DP19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | No screen in this story: the SCR-46 agent monitor screen and the Power BI page stay out of scope, and the P9 report read with its loaded and stale states stands in for the dashboard (section 15; ASM-0530) |

The H and C dependencies of the table stay with the service, platform and operations stories that own them; this story carries none of its own, and an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7). The I list names the four builds whose behaviour the run exercises: the integration outbound read, the agent measures, the alert and the daily step, the access session and refusals, and the notification contract.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Agent run fixture | 270 runs on 2026-12-01: INTAKE 120 runs with 9 fallbacks and 1,840.0000 baht, SCREENING 150 runs with 21 fallbacks and 2,310.5000 baht, and "EXTRACT" with no run; the runs carry policy "P1", prompt "PR1", latency and token counts | AC1, AC5, AC8, AC9, AC12, AC13 |
| Policy fixture | Policy "P1" for INTAKE and SCREENING with daily_cost_cap_thb 2,000 and alert_role "RW-COE", an approved policy for EXTRACT, prompt "PR1" for both agents, the INTAKE cost of 2,000.0000 baht on 2026-12-02, and the two evaluation scores the dashboard shows | AC1, AC2, AC5, AC6 |
| Notification capture | The P6 capture stub that records the MSG-P10-004 message and its recipients, and the outage switch at 01:40 | AC2, AC7, AC13 |
| Date clock | 2026-11-30 as the previous report date, 2026-12-01 as the business date of the run, and 2026-12-02 for the cap-equal case | AC3, AC4, AC6, AC8, AC9, AC10 |
| Identity set | RW-PLATADM for the rerun, RW-CASEOWN without Reporting R, RW-COE and RW-RISK as the alert recipients, RW-DATASTEW for the count-mismatch alert, and RW-BIANAL as a Reporting R holder | AC3, AC4, AC7, AC10, AC11 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P1, P2, P4, P6, P9 and P10 and to the topic, with the contract preflight that fails on any drift and refuses a fake for any of the six (AC12, X8, X9).
2. Build AbsenceProbe first: assert that no agent_run_daily table, lake schema, lake connection, INT-19 or INT-20 connector exists, and read the P2 outbound-item list to assert that no file is produced (AC8, X12, X13).
3. Build FixtureBuilder and the clock: the 270 runs, the three policies, the two prompt versions and the two evaluation scores on 2026-11-30, 2026-12-01 and 2026-12-02 (AC1, AC5, AC6).
4. Build JobTriggerControl and JobAdminProbe: fire JOB-15 at 01:30 for 2026-12-01, assert one call of the P10 daily step, read the run record through the owner's job read, request the rerun and assert the 403 of a role without Platform administration U (AC3, AC4, AC10).
5. Build ReportProbe over the P9 read: runs, fallback rate 0.0750, median and 95th percentile latency, cost, evaluation score, "no L1 runs", "EXTRACT" at 0 and 0.0000, and the previous date 2026-11-30 when the publish is held (AC1, AC3, AC5, AC8).
6. Build CountCheckProbe: compare the row count and the sum of runs with the P10 source, drive the one-row-for-two-groups mismatch, and assert the held publish, the stale date and MSG-P1-001 (AC3, AC9).
7. Build AlertProbe over the P10 measure read: one COST_CAP alert for SCREENING at measured 2,310.5000 and threshold 2,000, none for INTAKE, none for EXTRACT, none at 2,000.0000 on 2026-12-02, and no second row after the rerun (AC2, AC4, AC5, AC6).
8. Build NotificationProbe: the capture stub, the one message per alert with recipients RW-COE and RW-RISK, the outage at 01:40 with sent_at empty, and the single send after the JOB-11 retry (AC2, AC7).
9. Build AccessProbe and PiiScanProbe: the 403 with MSG-P4-002 on the report read and on the job rerun, and the scan of the daily rows, the alert, the captured message and the logs (AC11, AC13).
10. Build ReportWriter, clean up the fixture, the alerts of the synthetic dates and the capture stub, and write the evidence report; run the suite twice to prove that a second pass adds no row and sends no second message.

**Done when.** The test cases of section 16 pass on the real services in SIT, the criteria of section 7 are signed off against the contracts, the P9 read shows the fixture figures for 2026-12-01 (INTAKE 120 runs at 0.0750 and 1,840.0000 baht, SCREENING 150 runs at 2,310.5000 baht, "EXTRACT" at 0), exactly one COST_CAP alert and one notification exist, the rerun replaces the two rows and raises no second alert, no data lake and no INT-19 or INT-20 artefact exists anywhere in the run, the scan finds no personal data, the fixture is cleaned up, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-004 | Agent cost on a business date above its daily limit | {agent} used {amount} baht of model calls on {date}, above the daily limit of {limit} baht. |
| MSG-P1-001 | The report shows the previous day after a held publish | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-E1-063 and this story adds no message ID. Thai text for each message follows decision DL10. In AC2 the {agent} value is "SCREENING", the {amount} value is 2,310.5000, the {date} value is 2026-12-01 and the {limit} value is 2,000; in AC3 the {product} value is the daily agent measures and the {date} value is 2026-11-30; in AC11 the {action} value is reading the agent measures.

### 15. Screens and states

No Workbench screen in this story. The dashboard is read through `GET /api/recovery/reporting/v1/reports/measures`, and the states the suite asserts through that read are: loaded, with the measures of the latest published business date, and stale, with the previous date 2026-11-30 shown and MSG-P1-001 naming it after a held publish. The Power BI report "Agent monitor v1" of the legacy story has no source in the target, because the lake it was built on is removed, and it is not built here (ASM-0530). The agent monitor screen SCR-46 and its states come in RWB-E2-031 and are out of scope, as is the steering dashboard of Epic 2. The SCR-46 empty, loading, error and no access states are Not specified in the source documents (CG-ALL-392).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-063-01-ITG | AC1, BR2, BR6 | Integration | INTAKE 120 runs, 9 fallbacks, 1,840.0000 baht and SCREENING 150 runs, 21 fallbacks, 2,310.5000 baht on 2026-12-01; the P9 read shows the measures by name, INTAKE at 0.0750 and "no L1 runs"; end to end on the real services |
| TC-E1-063-02-ITG | AC2, BR4, BR5, BR7 | Integration | SCREENING cost 2,310.5000 baht against cap 2,000; one COST_CAP alert with measured 2,310.5000 and threshold 2,000; MSG-P10-004 to RW-COE and RW-RISK; no INTAKE alert; end to end on the real services |
| TC-E1-063-03-ITG | AC3, BR3 | Integration | Reporting write with 1 row for 2 agent and version groups on 2026-12-01; publish held, report at 2026-11-30, JOB-15 failed on the owner's job read (pending, GAP-3271), MSG-P1-001 to the reader and the data steward alerted; end to end on the real services |
| TC-E1-063-04-ITG | AC4, BR5 | Integration | JOB-15 completed for 2026-12-01 with the SCREENING alert sent; rerun of the same date through the owner's rerun (pending, GAP-3271); the same 2 rows and no second alert or notification; end to end on the real services |
| TC-E1-063-05-ITG | AC5 | Integration | EXTRACT with an approved policy and no runs on 2026-12-01; runs 0 and cost 0.0000; no alert; end to end on the real services |
| TC-E1-063-06-ITG | AC6, BR4 | Integration | INTAKE cost 2,000.0000 baht on 2026-12-02, equal to the cap; no cost alert for that date; end to end on the real services |
| TC-E1-063-07-ITG | AC7, BR8 | Integration | Notification interface unavailable at 01:40; the SCREENING alert kept with sent_at empty; one send after the JOB-11 outbox relay succeeds (R-UNI-33, R-UNI-35); end to end on the real services |
| TC-E1-063-08-ITG | AC11, BR14 | Integration | RW-CASEOWN holds no Reporting R, confirmed on the P4 session read; the P9 report read refused with 403 and MSG-P4-002; end to end on the real services |
| TC-ITG-E1063-ITG-09 | AC8, BR1, BR2 | End to end | The daily rows of 2026-12-01 read through P9 equal the P10 source counts; no agent_run_daily table, no data lake, no INT-19 or INT-20 connection, and no outbound item or file on the P2 read |
| TC-ITG-E1063-ITG-10 | AC9, BR3 | Integration | The row count and the sum of runs of the P9 read compared with the P10 measure read for 2026-12-01; a difference holds the publish and raises MSG-P1-001 |
| TC-ITG-E1063-ITG-11 | AC10, BR9, BR10 | Contract | JOB-15 at 01:30 fires through Airflow and calls the P10 daily step once; the run record read and the rerun requested through the owner's job operations (pending, GAP-3271); 403 with MSG-P4-002 for a role without Platform administration U |
| TC-ITG-E1063-ITG-12 | AC12, BR14 | Contract | Every assertion read through the twelve operations of section 12.2; no schema client and no read of agent_run, agent_alert, agent_policy or a reporting table |
| TC-ITG-E1063-ITG-13 | AC13, BR13 | NFR | Scan of the daily rows, the alert, the captured P6 message and the logs for national ID number, phone number, name and account number patterns |
| TC-ITG-E1063-ITG-14 | AC14, X9 | Contract | A run configured with a fake for P1, P2, P4, P6, P9 or P10 is refused by the preflight before any assertion; only the notification capture, the clock and the fixture set stand outside the services |
| TC-ITG-E1063-ITG-15 | AC15, BR14 | Contract | A suite step that reads a service schema directly does not exist; the pipeline scan fails a change that adds a schema client |
| TC-ITG-E1063-ITG-16 | AC16, BR11, BR12, BR15, BR16 | Contract | Business values read through a contract at run time; every REST call one hop with a 2 s client budget; the P9 report read returns the loaded and stale state with MSG-P1-001; the run refuses any environment other than SIT with the synthetic set |
| TC-ITG-E1063-ITG-17 | AC17 | Integration | AgentRunCompleted.v1 for SCREENING on 2026-12-01 consumed once and delivered again; the daily rows unchanged, no second alert row and no second notification |
| TC-E1-063-09-ITG | AC18 | Contract | Suite call log; no call to the rwb-source-data job operations |

TC-E1-063-01-ITG to TC-E1-063-08-ITG are the copies of the legacy test cases of RWB-E1-063, kept with their legacy IDs and given the `-ITG` suffix; TC-E1-063-08-ITG carries the legacy access test onto the report read. TC-ITG-E1063-ITG-09 to -13 are new (D-RCV-60): 9 carries the P9 read model and the absent data lake, 10 the count check between the reporting read and the P10 source, 11 the Airflow trigger and the P1 job record and rerun, 12 the contract-only reads and 13 the personal-data scan. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, the P9 read and the absent lake are End to end, the job record and the contract-only reads are Contract, and the personal-data scan is NFR.

### 17. Guardrails

- No business value in code or in the suite: the agent codes, the cap, the alert role, the alert type, the business dates, the run counts, the fallback counts and the costs are read through a contract at run time (BR11).
- No personal data in logs, events, fixtures or the report: the daily rows, the alert, the P6 message and the logs hold counts, times and amounts only, and no national ID number, phone number, name or account number appears in any artefact of the run (AC13).
- No cross-service table read and no schema client in the suite: every fact is read through a contract of section 12.2 or 12.4, and a pipeline scan fails any change that adds a schema connection (DP-01, AC12).
- No data lake and no live agent table read: the suite creates no lake table, connects to no lake, asserts at the preflight that no agent_run_daily table, lake schema, INT-19 or INT-20 connector exists, and reads no agent_run, agent_alert or agent_policy row directly (DP-17, AC8, X13).
- The alert is delivered once: the send is keyed on the alert row, MSG-P10-004 goes to the holders of RW-COE and RW-RISK only, and a rerun or a retry adds no second notification (BR5, BR8, R-UNI-40).
- One hop and a 2 s client budget on every REST call; the daily step runs inside the Airflow-triggered JOB-15 and is never a REST call of another service; a service that reaches another service through a second service fails the run (ADR-020, DP-11).
- The notification path is recorded, not delivered: the capture stub stands in for the outside SMS and LINE path that P6 calls, and no message leaves the building during the run (ASM-0528).
- The report is read, not rebuilt: the measures come from the P9 read model that P10 feeds, so the suite never recomputes a figure it then compares with itself (AC1, AC9).
- No production access and no production namespace: the run is pinned to SIT with the synthetic set and refuses to start against any other environment (BR16).
- Clean-up in the same run: the fixture runs, the alerts of the synthetic dates, the capture stub and the clock control are removed or retired, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-009 | The daily agent measures are available for reporting, with the row counts matched against the source | `GET /api/recovery/reporting/v1/reports/measures`, `GET /api/recovery/agent/v1/admin/agent-metrics`, `rwb.agent.AgentRunCompleted.v1` and the P9 daily read model | TC-E1-063-01-ITG, TC-E1-063-02-ITG, TC-E1-063-03-ITG, TC-E1-063-04-ITG, TC-E1-063-05-ITG, TC-E1-063-06-ITG, TC-ITG-E1063-ITG-09, TC-ITG-E1063-ITG-10 |
| DP01 | Owner's schema per service; no cross-service table read | The P9 measures, the P10 runs, evaluations and alert, the P9 job record, the P6 notice, the P2 outbound item and the P4 session, all behind their contracts | TC-E1-063-01-ITG, TC-ITG-E1063-ITG-09, TC-ITG-E1063-ITG-12 |
| DP06 | Parameters contract of rwb-case and the client library | The cap 2,000 and the alert role RW-COE read through the P10 configuration read, never a value in code | TC-E1-063-02-ITG, TC-E1-063-06-ITG |
| DP07 | Reference-data contract of rwb-case | The agent codes, the alert type COST_CAP and the roles read as data through the P10 and P4 reads | TC-E1-063-02-ITG, TC-E1-063-05-ITG, TC-E1-063-08-ITG |
| DP09 | Outbox, inbox and CloudEvents | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`, the agent alert event, whose name is Not specified in the source documents (GAP-1211), the JOB-11 outbox retry and the absent lake copy event | TC-E1-063-02-ITG, TC-E1-063-07-ITG, TC-ITG-E1063-ITG-09 |
| DP10 | Quartz jobs become the workflow kit, and Arch v5 slide 44 sets the mechanism per job | JOB-15 as the reporting extract of rwb-reporting, an Airflow trigger at 01:30, and JOB-11 as the every-minute outbox relay, with no Quartz table and no Temporal Schedule; the agent daily aggregation step runs once per business date after the run record closes, with its job ID Not specified in the source documents (GAP-1519) | TC-ITG-E1063-ITG-11, TC-E1-063-07-ITG |
| DP11 | One hop and a 2 s timeout | The twelve calls of 12.2 and the preflight contract test | TC-E1-063-03-ITG, TC-E1-063-08-ITG, TC-ITG-E1063-ITG-12 |
| DP13 | `/api/recovery/<short>/v1` | `/api/recovery/reporting/v1`, `/api/recovery/agent/v1`, `/api/recovery/source-data/v1`, `/api/recovery/comms/v1`, `/api/recovery/integration/v1` and `/api/recovery/access/v1` | Every test case, at the preflight |
| DP15 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; the P9 measure tables and P10 agent_alert are their owners' sequences | Every test case, at the preflight |
| DP17 | Data lake, INT-19 and INT-20 removed; reporting from events into rwb-reporting | The P9 daily read model and the preflight and P2 absence assertions; GAP-0372 names what the sources do not | TC-ITG-E1063-ITG-09, TC-E1-063-01-ITG |
| DP19 | Screen route through gateway-bff | No screen in this story; the target dashboard is SCR-46, served from the P10 daily measures and the P9 read model and out of scope here (RWB-E2-031); its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-392); the P9 report read with its loaded and stale states stands in for the dashboard | TC-E1-063-01-ITG, TC-E1-063-03-ITG |
| ASM-0525 | No data lake; the daily measures are a P9 read model from events and the P10 step, read through `GET /reports/measures`; the daily measure is a projection over the run record for the business date, produced once per agent and version and idempotent on the date, with its physical table Not specified in the source documents (GAP-1517) | The P9 report read, the daily read model and the absence probe | TC-ITG-E1063-ITG-09, TC-E1-063-01-ITG |
| ASM-0526 | The P9 report read is the only reporting read and the measures are asserted by name, because the row shape is not specified | `GET /api/recovery/reporting/v1/reports/measures` and the measure names of section 11 | TC-E1-063-01-ITG, TC-ITG-E1063-ITG-09 |
| ASM-0527 (superseded in part by RD-P1-012) | JOB-15 is an Airflow trigger and its run record and rerun belong to its owner rwb-reporting, with no Quartz | The owner's job operations (pending, GAP-3271) | TC-ITG-E1063-ITG-11, TC-E1-063-03-ITG, TC-E1-063-04-ITG |
| ASM-0528 | The alert goes through the P6 notification contract with the alert reference in the case position and no case lookup, the JOB-11 outbox retry, read back at the P6 boundary | `POST /api/recovery/comms/v1/cases/{caseId}/messages`, `GET /api/recovery/comms/v1/notices/{noticeId}` and the capture stub | TC-E1-063-02-ITG, TC-E1-063-07-ITG |
| ASM-0529 | The alert and its cost facts are read through the P10 measure read, never through a table | `GET /api/recovery/agent/v1/admin/agent-metrics` | TC-E1-063-02-ITG, TC-E1-063-04-ITG, TC-E1-063-05-ITG, TC-E1-063-06-ITG |
| ASM-0530 | The P9 read replaces the Power BI page for this suite; SCR-46, served from the P10 daily measures and the P9 read model (GAP-1516), stays out of scope | `GET /api/recovery/reporting/v1/reports/measures` and section 15 | TC-E1-063-01-ITG, TC-E1-063-03-ITG |
| GAP-0372 | The daily read model, the reporting read and the job record owner are not named for the target | The P9 read, the P9 job record (path pending, GAP-3271) and the absence proof of section 12 | TC-ITG-E1063-ITG-09, TC-ITG-E1063-ITG-11, TC-E1-063-01-ITG |
| GAP-1516 | FSD P10 v3 data lake write and Power BI publish removed by Architecture v5; the target dashboard is SCR-46, fed from the measures and the read model and out of scope in this story, with the row count checked on the measure hand-over | `GET /api/recovery/reporting/v1/reports/measures`, `GET /api/recovery/agent/v1/admin/agent-metrics` and the P9 daily read model | TC-ITG-E1063-ITG-09, TC-ITG-E1063-ITG-10 |

### 19. Out of scope

- The application builds this run depends on: RWB-P2-E1007-APP, RWB-P10-E1063-APP, RWB-P4-E1063-APP and RWB-P6-E1063-APP.
- The contract, database, operations and infrastructure stories of the legacy key.
- The wave-1 builds the suite stands on without depending on them: RWB-P1-E1064-APP, and the P9 job operations, reporting read model and measures build; they are published-contract preconditions, not integration dependencies.
- Building the P9 daily read model, the P10 daily step and the JOB-15 Airflow trigger, which are the owners' builds; this story proves them, it does not create them.
- The Power BI page "Agent monitor v1", the Workbench reporting workspace and the SCR-46 agent monitor screen (RWB-E2-031), and the steering dashboard of Epic 2.
- Acceptance and override per segment, drift alerts and drift detection (FEAT-AGT-13, Epic 3).
- The regulatory extract and the regulatory reports of JOB-15 beyond the daily agent measures, and every other measure of P9.
- The choice of model endpoint, the agent runs themselves and the evaluation harness, which belong to RWB-ITG-E1058-ITG, RWB-ITG-E1059-ITG, RWB-ITG-E1060-ITG and RWB-ITG-E1062-ITG.
- The build of the harness RWB-ITG-W1J01-ITG itself and the non-functional epic RWB-ITG-NFR.

### 20. Remaining delivery steps

- Publish the JOB-15 run read and rerun operations of rwb-reporting and name their paths (GAP-3271): Pending (owner: solution architect).
- Decide the rerun of a completed business date (NEW-GAP-F03-3): Pending (owner: solution architect with the rwb-reporting service owner).
- Size, contract versions and fake library version: Pending (owner: squad and contract owners).
- Update the TC-E1-063 and TC-ITG-E1063 rows for AC3, AC4, AC10 and add AC18 in Test Cases v9: Pending (owner: QA).
- Fixture set loaded in SIT: Pending (owner: QA).
