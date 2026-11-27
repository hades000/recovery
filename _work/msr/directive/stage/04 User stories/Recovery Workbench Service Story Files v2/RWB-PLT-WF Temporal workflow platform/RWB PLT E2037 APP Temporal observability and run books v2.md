# RWB-PLT-E2037-APP Temporal observability and run books

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E2037-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | L-PLT-WF-F |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement; not yet sized (DOR-RWB-PLT-E2037-APP-16) |
| Contract version | v1 (path /v1 of RWB-PLT-E2037-CON) |
| Depends on (build) | RWB-PLT-E2037-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-PLT-E1070-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-E1056-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-037 for the workflow platform epic; the stuck workflow scanner is now JOB-21, a Temporal Schedule every five minutes on task queue `rwb-platform`, and the legacy 15-minute Quartz cadence is recorded as superseded (GAP-1446). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-PLT-E2037-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (8 resolved, 30 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **Temporal metrics, an alert for every failed or stuck workflow and a dashboard that shows workflow volume by type and status, each alert with its own run book**, so that **a workflow problem is seen before a case waits**.

This is the app story of legacy key RWB-E2-037 under epic RWB-PLT-WF, the Temporal workflow platform of the realignment. It watches the workflows the shared platform runs, not the cluster that runs them: the three signals (an execution that closes FAILED or TIMED_OUT, an execution with no progress for `temporal.stuck.hours`, a schedule-to-start latency above its threshold), one Grafana dashboard grouped by workflow type and status with no personal data, and one run book for each alert so that the platform administrator acts without the developer.

The platform is **not one of the 19 services**. Template and Rules §R4 has no platform row, so this story owns no `rwb_*` schema, no `rwb.<short>.events.v1` topic and no `/api/recovery/<short>/v1` base; the namespace is `rwb-recovery` and the platform task queue is task queue `rwb-platform` (Architecture v5 slides 8 and 24; Ownership Map jobs). The scanner is **JOB-21**, a Temporal Schedule every 5 minutes on task queue `rwb-platform` that reads visibility and history through the frontend API (Architecture v5 slide 44; Ownership Map jobs JOB-21; Temporal and Drools Design slide 28 notes), so the legacy Quartz job on a 15-minute interval is replaced by a Schedule (DP-10). That cadence change is recorded as a conflict with the legacy story (GAP-1446; ASM-2541).

The platform identity, meaning its login, its task queue provisioning record and its admin base for the catalogue read, is named by no read source: Not specified in the source documents (GAP-1444; ASM-2539). The dashboard names, the panel titles and the alert routing labels are fixed by the contract of RWB-PLT-E2037-CON and are used here exactly as published.

### 2. Business rationale

Case workflows from Epic 3 wait for days on durable timers, and a workflow that has stopped moving looks exactly like a workflow that is waiting. Nothing in the Workbench watches a workflow execution today: the job monitor of RWB-PLT-E1056-OPS watches the Workbench jobs, and the platform dashboard of RWB-PLT-E1070-APP watches the five Temporal services, not the workflows those services run. Without this story the first sign of a workflow that cannot progress is a case owner asking why the case has not moved.

This story adds the three signals that cover the ways a workflow stops: an execution that closes FAILED or TIMED_OUT, an execution with no progress for `temporal.stuck.hours` (24, assumed), and a schedule-to-start latency above its threshold. It adds one Grafana dashboard grouped by workflow type and status with no personal data, and a run book for each alert so that the platform administrator acts without the developer. It meets REQ-DRI-007 (a named owner and a tested way back for every failure). The measure is that every alert reaches the on-call rota within 5 minutes in SIT and names a run book.

The split changes the scan and only the scan. In the monolith the scanner was a Quartz job on a 15-minute interval inside one process; in the target no service and no platform runs Quartz, and each recurring job is a Temporal Schedule in the process that owns it (DP-10; Architecture v5 slide 44; Temporal and Drools Design slide 32 item 6). JOB-21 is therefore a Schedule on task queue `rwb-platform` every 5 minutes, and its candidate list still comes from one visibility query and one history summary read through the frontend API over mTLS, with no grant on the Temporal databases. The five-minute cadence is the target and the legacy fifteen minutes is recorded as superseded, not silently changed (GAP-1446). Everything else in the legacy story keeps its values: the three alerts, the thresholds of the rule file, the four search attributes, the eight run book sections, MSG-P3-037 and the 5-minute delivery target.

### 3. Preconditions

- RWB-PLT-E2037-CON is published: the metric names and labels, the three alert rules and their annotation contract, the dashboard data contract, the alert-to-run-book map contract and the scanner query contract, with the metric fixtures, the Alertmanager fake and the Grafana provisioning fake.
- RWB-PLT-E1070-CON is published: the namespace `rwb-recovery`, its 30-day retention, the four Keyword search attributes, the client certificate profile and the frontend API subset (`ListWorkflowExecutions`, `GetWorkflowExecutionHistory`, `DescribeWorkflowExecution`) with its typed errors (DP-13, DP-14).
- RWB-PLT-E1071-CON is published: the worker and SDK contract, the platform worker on task queue `rwb-platform`, its build ID and its SDK metrics (DP-10).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). The platform worker is built from the same template, so the library is on the classpath even though the observability path writes no decision record.
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the platform parameters contract and the reference-data contract, with the client library, so `temporal.stuck.hours` and the severity vocabulary are data and not literals (DP-06, DP-07).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence (DP-15). This story runs no migration: the scanner's catalogue row is a data change through the P2 admin operation.
- RWB-PLT-E1047-CON and RWB-PLT-N001-CON are published: the topic and event naming library (DP-14) and the gateway-bff route surface (DP-19). The dashboard is not a Workbench screen and this story adds no route to the edge.
- RWB-PLT-E1070-APP is done: the cluster, the namespace `rwb-recovery`, mTLS, the Web UI and the metrics scrape to the ACE monitoring stack exist in DEV and SIT.
- RWB-PLT-E1071-APP is done: the worker polls task queue `rwb-platform` with build ID "9f3c2a1-418" and reports the SDK metrics through the same scrape.
- Prometheus, Alertmanager and Grafana run in the ACE monitoring namespace, and the platform on-call rota and the incident queue of the operations team exist.
- The parameter `temporal.stuck.hours` = 24 is in the catalogue through the parameters contract; the value is assumed until the platform administrator confirms it with the operations team (ASM-2541).
- The SIT worker registers the test-only workflow CaseHoldWorkflow on task queue `rwb-platform`, which can be held with no progress or left on a timer; it is not deployed to UAT or PROD.
- The scanner runs as SY-CASEWF with the client certificate of RWB-PLT-E1070 and holds no grant on the Temporal databases.
- The feature flag `rwb.p3.temporal` is on in SIT, read through the parameters contract.
- The platform identity, meaning the platform login, the task queue provisioning record and the admin base the catalogue read uses, is named by no read source: Not specified in the source documents (GAP-1444; ASM-2539).

### 4. Flow

1. Prometheus: scrapes the Temporal server metrics of RWB-PLT-E1070 and the worker SDK metrics of RWB-PLT-E1071 every 15 seconds; the scrape source is the ACE monitoring namespace only.
2. TemporalAlertRules: evaluate `TemporalWorkflowFailed` when an execution closes FAILED or TIMED_OUT, and `TemporalScheduleToStartLatency` when the p95 schedule-to-start latency on a task queue is above 60 seconds for 10 minutes.
3. StuckWorkflowScanner, on the JOB-21 Temporal Schedule every 5 minutes on task queue `rwb-platform`: calls `ListWorkflowExecutions` for RUNNING workflows whose StartTime is older than `temporal.stuck.hours`, then reads the history summary of each candidate through the frontend.
4. StuckWorkflowScanner: marks a candidate stuck only when it has no history event for `temporal.stuck.hours`, no open timer and no activity in retry, and publishes the count as `workflow_stuck` by workflow type.
5. TemporalWorkflowStuck: fires on a stuck count above zero with MSG-P3-037, the workflow ID and the hours since the last event.
6. Alertmanager: routes each alert to the platform on-call rota and the incident queue, with the run book path in the annotation and one alert per workflow and condition.
7. Platform administrator: opens the dashboard, reads the workflow type, task queue and build ID, and follows the run book for the check, restart or drain step.
8. Dashboard "Temporal workflows": shows running, failed, completed and timed-out counts by type, schedule-to-start latency by task queue, task queue backlog, stuck workflows and worker build IDs, all from the four search attributes.
9. StuckWorkflowScanner: records its last successful run in job_catalog through the P2 admin operation; a failed scan marks the stuck panel stale and raises an incident, and never publishes a zero.

The scanner is a Schedule-started workflow run, not a Quartz job and not a long-running daemon: each 5-minute run is one short workflow on task queue `rwb-platform`, with overlap policy SKIP, so a slow run never stacks behind itself (DP-10). The three alerts, the routing, the dashboard and the run book map are the legacy behaviour unchanged.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The Temporal frontend is unreachable from the scanner, so the visibility query fails | No stuck value is published and no stuck alert is raised; the scanner failure counter rises; the stuck panel shows data stale since the last good scan; an incident reaches RW-PLATADM | None (incident and metric only) | AC6 |
| X2 | An alert rule has no run book, or its run book lacks one of the eight sections | The pipeline fails naming the alert and the missing section; the rule file is not deployed | None (build log) | AC7 |
| X3 | A workflow makes progress between the scan and the delivery of its alert | The alert resolves at the next evaluation; no page is sent and no incident is opened | None | AC8 |
| X4 | A value the build needs is named by no read source (the platform login, the task queue provisioning record, the admin base, the dashboard name) | The value is used as the working read of the assumption, the placeholder is written where the value is still open, and the gap stays open | Not specified in the source documents (GAP-1444; ASM-2539) | AC4, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds the three alerts, one Schedule-started scanner, one dashboard and three run books on the platform of RWB-PLT-E1070 and the worker of RWB-PLT-E1071; builds against RWB-PLT-E2037-CON and its fakes |
| Negotiable | Thresholds, the stuck window, the repeat interval, the panels and the routing rota are configuration; the three signals, the five-minute cadence and the run book rule are fixed |
| Valuable | A workflow problem reaches a named owner before a case owner notices the case has stopped |
| Estimable | Three alert rules, one scanner Schedule, one dashboard, one run book map and three run books |
| Small | Fits two weeks with its checks |
| Testable | Each criterion in section 7 has one test in section 16, on fixed workflows and fixed thresholds |

### 7. Acceptance criteria

```gherkin
Feature: Temporal observability and run books

  Background:
    Given the Temporal cluster of RWB-PLT-E1070 runs in SIT with namespace rwb-recovery
    Given the worker of RWB-PLT-E1071 polls task queue `rwb-platform` with build ID "9f3c2a1-418"
    Given the parameter temporal.stuck.hours is 24
    Given Alertmanager routes the Workbench platform alerts to the platform on-call rota

  Scenario: AC1 A failed workflow raises an alert within five minutes (legacy RWB-E2-037 AC1)
    Given workflow "platform-smoke-20261116" started at 07:00 on 16 November 2026 on task queue `rwb-platform`
    When the workflow closes FAILED at 10:12
    Then the rule TemporalWorkflowFailed is FIRING at the 10:13 evaluation with severity "page"
    Then the alert annotation carries MSG-P3-037 with workflowId "platform-smoke-20261116" and hours 3
    Then Alertmanager delivers the alert to the platform on-call rota within 5 minutes of the close
    Then the dashboard count of failed PlatformSmokeWorkflow executions for the day is 1

  Scenario: AC2 A workflow with no progress raises an alert, and a timed wait does not (legacy RWB-E2-037 AC2)
    Given workflow "case-RW-2026-000123" of type CaseHoldWorkflow on task queue `rwb-platform` is RUNNING
    Given its last history event is at 09:00 on 15 November 2026 and it has no open timer and no activity in retry
    Given workflow "case-RW-2026-000124" of the same type is RUNNING and started timer "wait-30-days" at 10:00 on 14 November 2026
    When StuckWorkflowScanner runs at 09:05 on 16 November 2026
    Then "case-RW-2026-000123" is marked stuck with 24 hours since its last progress
    Then TemporalWorkflowStuck is FIRING with MSG-P3-037, workflowId "case-RW-2026-000123" and hours 24
    Then "case-RW-2026-000124" is not marked stuck and no alert exists for it

  Scenario: AC3 Schedule-to-start latency raises an alert (legacy RWB-E2-037 AC3)
    Given the worker stops polling task queue `rwb-platform` at 11:00 on 16 November 2026
    Given the rule threshold is a p95 schedule-to-start latency of 60 seconds for 10 minutes
    When 12 tasks wait on task queue `rwb-platform` and the p95 reaches 120 seconds at 11:12
    Then TemporalScheduleToStartLatency is FIRING with taskQueue `rwb-platform` and p95 "120s"
    Then Alertmanager delivers the alert to the platform on-call rota
    Then the dashboard panel "Schedule-to-start latency" shows the spike for task queue `rwb-platform`
    When the worker resumes at 11:20 and the p95 returns below 60 seconds
    Then the alert resolves at the next evaluation

  Scenario: AC4 The dashboard shows volume by type and status with no personal data (legacy RWB-E2-037 AC4)
    Given the dashboard "Temporal workflows" is provisioned from ops/monitoring/temporal/workflow-dashboard.json
    When U-70 opens it for the rwb-recovery namespace
    Then it shows running, failed, completed and timed-out counts by workflow type
    Then it shows schedule-to-start latency by task queue, task queue backlog, stuck workflows and worker build IDs
    Then every panel query uses the search attributes CaseId, Stage, ProductGroup and QueueCode only
    Then DashboardPersonalDataCheck finds no person field and no payload field in the 40 panel queries
    Then no panel shows a workflow input, a workflow output or a history event payload

  Scenario: AC5 Every alert has a run book (legacy RWB-E2-037 AC5)
    Given the rule file holds TemporalWorkflowFailed, TemporalWorkflowStuck and TemporalScheduleToStartLatency
    When RunbookCompletenessTest runs in the pipeline
    Then each alert names a run book in docs/operations/runbooks with the eight sections
    Then each run book names the alert, the check, the restart or drain step and the escalation
    Then the build passes with the three run books

  Scenario: AC6 The scanner cannot reach the frontend (legacy RWB-E2-037 AC6)
    Given the Temporal frontend is unreachable from the scanner at 09:05 on 16 November 2026
    When StuckWorkflowScanner runs
    Then it publishes no workflow_stuck value and raises no TemporalWorkflowStuck alert
    Then temporal_scanner_failures_total increases by one
    Then the dashboard panel "Stuck workflows" shows "data stale since 09:05"
    Then an incident reaches RW-PLATADM naming the scanner error
    Then no workflow is marked stuck

  Scenario: AC7 An alert with no run book fails the build (legacy RWB-E2-037 AC7)
    Given a branch adds the alert TemporalWorkerDown to the rule file with no entry in the alert-to-run-book map
    When RunbookCompletenessTest runs
    Then the build fails naming "TemporalWorkerDown" and the missing run book
    Then the rule file is not deployed to SIT or PROD

  Scenario: AC8 An alert clears before it is delivered (legacy RWB-E2-037 AC8)
    Given TemporalWorkflowStuck is PENDING for "case-RW-2026-000125" at 09:05 with 25 hours since its last event
    When the worker picks up the workflow and it records a new history event at 09:06
    Then the alert resolves at the 09:10 evaluation
    Then Alertmanager sends no page and opens no incident
    Then the alert history keeps the PENDING and RESOLVED states with their times

  Scenario: AC9 The scanner reads through the frontend API only and every threshold is configuration (BR6, BR10) (new, D-RCV-60)
    Given the StuckWorkflowScanner code and its deployment configuration are under review
    When the scanner reads visibility and history for a run
    Then it reads through the Temporal frontend API over mTLS and never connects to the Temporal databases
    Then the scanner identity holds no grant on the Temporal databases
    Then the stuck window, the repeat interval, the panel list and the routing rota are read from configuration and none is hard-coded

  Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
    Given the workflow state is not specified in the source documents (NEWAC-RWB-PLT-E2037-APP-AC10)
    When a status change the model does not allow is applied to it
    Then the change is refused
    Then the workflow status is unchanged
```

The criteria are copied from RWB-E2-037 with every value kept: platform-smoke-20261116, 10:12, 10:13, 09:05, 09:06, 09:10, 24 hours, 60 seconds, 120s, 12 tasks, 40 panel queries, case-RW-2026-000123, case-RW-2026-000124, case-RW-2026-000125, build ID "9f3c2a1-418" and MSG-P3-037. The only change is the queue phrasing, which names task queue `rwb-platform`. The scanner is now JOB-21 on a Temporal Schedule every 5 minutes (Architecture v5 slide 44), so the legacy 15-minute Quartz cadence is superseded (GAP-1446).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A workflow that closes FAILED or TIMED_OUT raises TemporalWorkflowFailed with MSG-P3-037, and the alert reaches the on-call rota within 5 minutes of the close | REQ-DRI-007; AC1 |
| BR2 | A RUNNING workflow with no history event for `temporal.stuck.hours` (24, assumed), no open timer and no activity in retry raises TemporalWorkflowStuck; a workflow that waits on a durable timer is never stuck | AC2 |
| BR3 | A p95 schedule-to-start latency above 60 seconds for 10 minutes on a task queue raises TemporalScheduleToStartLatency; both values are rule-file configuration | AC3 |
| BR4 | The dashboard groups by workflow type and status and reads the four search attributes CaseId, Stage, ProductGroup and QueueCode only; no panel reads a payload, a history event or a case table | ADR-023; AC4 |
| BR5 | Every alert names a run book with the eight sections of the run book catalog of RWB-PLT-E1056-OPS; RunbookCompletenessTest fails the build when one is missing or incomplete | RWB-PLT-E1056-OPS; AC5 |
| BR6 | The scanner reads visibility and history through the Temporal frontend API over mTLS and never reads the Temporal databases; it holds no grant on them | RWB-PLT-E1070-CON; Temporal and Drools Design slide 11; AC9 |
| BR7 | A failed scan publishes no stuck value and marks the panel stale; it never publishes zero in place of a result | AC6 |
| BR8 | One alert per workflow and condition; a repeated evaluation updates the same alert and opens no second incident | AC8 |
| BR9 | An alert resolves when its condition clears, and a resolved alert leaves no open incident and no open page | AC8 |
| BR10 | Thresholds, the stuck window, the repeat interval, the panel list and the routing rota are configuration, never code | REQ-DRI-007; AC9 |
| BR11 | The scanner runs every 5 minutes as JOB-21 on a Temporal Schedule on task queue `rwb-platform`, with overlap policy SKIP; the legacy 15-minute Quartz interval is superseded and is never restored | Architecture v5 slide 44; Ownership Map jobs JOB-21; GAP-1446 |

### 9. State transitions

None for a case. This story changes the status of an alert and reads the status of a workflow execution.

| From | Event | Condition | To |
|---|---|---|---|
| None | Rule evaluates true | A workflow closes FAILED or TIMED_OUT | FIRING |
| None | Rule evaluates true | No progress for 24 hours, no open timer, no activity in retry | FIRING |
| None | Rule evaluates true | p95 latency above 60 seconds for 10 minutes | FIRING |
| PENDING | Rule evaluates true | Condition still true at delivery | FIRING |
| PENDING | Rule evaluates false | Condition cleared before delivery | RESOLVED, no page |
| FIRING | Rule evaluates false | Condition cleared | RESOLVED |
| RUNNING | Execution closes | A workflow ends | COMPLETED, FAILED or TIMED_OUT; alert state follows the rule |

The workflow states COMPLETED, FAILED and TIMED_OUT are Temporal's; no recovery case status changes. Alert state lives in Prometheus and Alertmanager and is never written into a `rwb_*` schema.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Reads the alerts, the dashboard and the scanner status; works the incident and follows the run book; silences an alert for the duration of an open incident and records the silence in it (Platform administration, R) |
| RW-AUDIT | Reads the dashboard and the alert history (Platform administration, R) |
| RW-TRIBE | Writes the rule file, the dashboard JSON and the run books through the change process; may not silence an alert in PROD |
| RW-CASEOWN and the other case roles | No access to the alerts or the dashboard; they see the case, not the engine |
| SY-CASEWF | Runs the scanner and publishes the metrics; holds no screen right |
| SY-RULES | No part in this story |
| No delegation of authority level applies | An operational alert is not a credit decision |

The platform identity that runs the scanner and writes the catalogue row is Not specified in the source documents (GAP-1444; ASM-2539); the story names it "the platform identity" and the scanner runs as SY-CASEWF with the certificate of RWB-PLT-E1070.

### 11. Data

| BR Field ID | Entity | Field | Read or write | Owner |
|---|---|---|---|---|
| None (platform enabler) | None in a `rwb_*` schema | None | None | None |
| DF-OPS-224 to DF-OPS-232 | job_catalog | The JOB-21 row: job ID, name, owner role, schedule text, run book path, expected minutes, alert threshold, first release | Read and write through the P2 admin operation | P2 rwb-integration |
| DF-OPS-229 | job_catalog | runbook_path, the alert-to-run-book map entry for each of the three alerts | Read and write through the P2 admin operation | P2 rwb-integration |

Alert state lives in Prometheus and Alertmanager, and workflow, timer and task state lives in Temporal persistence and visibility (RWB-PLT-E1070). The names `workflow_stuck` and `temporal_scanner_failures_total` are Prometheus metric names published by RWB-PLT-E2037-CON; they are not fields or entities in LDM v9 or Data Classification v5 and are held in no table. The scanner's last run, its owner role, its schedule text and the alert-to-run-book map live in job_catalog, which is owned by P2 rwb-integration and is read and written only through its admin operation, `GET /api/recovery/integration/v1/admin/scheduled-jobs` (Ownership Map: job_catalog, api). No DF-REF, DF-CAS or DF-DEC field is added or changed, this story creates no table and runs no migration, and the dashboard reads the search attributes CaseId, Stage, ProductGroup and QueueCode only. The Physical Schema is unchanged. No business value and no personal data are held by this story: workflow identifiers, timestamps, counts, durations and role codes only.

### 12. Contract

#### 12.1 REST operations provided

None. The platform has no service short (Template and Rules §R4 has no platform row), so it publishes no path under `/api/recovery/<short>/v1` and no Workbench endpoint. The operator surfaces are the Grafana dashboard, the Alertmanager alert list and the run books, none of which is a Workbench route (DP-13, DP-19).

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/integration/v1/admin/scheduled-jobs` | P2 rwb-integration | The JOB-21 and JOB-22 catalogue rows: the scanner's owner role, schedule text, run book path, expected minutes and alert threshold, and the alert-to-run-book map entries; read by the scanner run and by the pipeline gate | One hop, 2 s client budget (DP-11) |

The catalogue read is the only Workbench call this story makes; it never reads the `job_catalog` table directly. The run book gate of RWB-PLT-E1056-OPS reads the same operation, so the catalogue is the one record and is not copied.

#### 12.3 Events published

None. The platform publishes no `rwb.<short>.events.v1` topic and no event schema (DP-14). The stuck count is a metric, the alert is an Alertmanager object, and the scan result is a catalogue row; none of them is a business event, and the v5 event catalogue carries no observability event.

#### 12.4 Events consumed

None. The scanner reads the Temporal visibility and history API, not a Kafka topic; no other service's event reaches this story.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| StuckWorkflowScanner | Workflow started by the JOB-21 Schedule, one short run per scan | `rwb-platform` | Runs the visibility query, the history summary read, the stuck test and the metric publication; overlap policy SKIP, so a slow run never stacks |
| scanStuckWorkflows | Activity | `rwb-platform` | Calls `ListWorkflowExecutions` and `GetWorkflowExecutionHistory` on the frontend over mTLS for the RUNNING candidates |
| publishScannerMetrics | Activity | `rwb-platform` | Publishes `workflow_stuck` by workflow type, `temporal_scanner_failures_total` and the last successful scan time |
| recordScanRun | Activity | `rwb-platform` | Records the run and the alert-to-run-book map through the P2 catalogue operation; a failed scan records a failure and no zero |

The scanner is started by the Schedule and is not a daemon: the platform worker of RWB-PLT-E1071 polls task queue `rwb-platform` and one run ends before the next begins. No workflow of the 19 services is started or claimed here. The Schedule ID is not specified in the source documents (GAP-2022); catch-up after downtime is off, the Schedule does not pause on failure, and a failed run raises the E2-037 alert.

#### 12.6 Schedules

| Schedule | Cadence | Trigger | Legacy reference |
|---|---|---|---|
| JOB-21 Stuck workflow scan | Every 5 minutes, with overlap policy SKIP and a catch-up window | Temporal Schedule on task queue `rwb-platform` | JOB-21 Stuck workflow scan; the legacy Quartz job ran every 15 minutes and is superseded (GAP-1446) |
| Stuck-window reconciliation | Every 5 minutes, at each JOB-21 run | The same Schedule; each run reconciles the RUNNING candidates older than `temporal.stuck.hours` | Legacy StuckWorkflowScanner step 3 |

JOB-22, the platform smoke workflow at 06:00, belongs to the smoke story of the same epic and is named here only because the catalogue read returns both platform rows.

#### 12.7 Tables owned

None. `job_catalog` is owned by P2 rwb-integration (Ownership Map) and this story reads and writes it only through the P2 admin operation; the Temporal persistence stores belong to RWB-PLT-E1070 and hold no `rwb_*` table. This story creates no table and runs no Flyway migration (DP-15).

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Metric fixtures (RWB-PLT-E2037-CON) | Synthetic Prometheus series for `workflow_stuck`, `temporal_scanner_failures_total` and the last successful scan time, in the declared name and label shape | The rule-expression unit tests of AC1 and AC3 and the dashboard panel tests of AC4 |
| Alertmanager fake (RWB-PLT-E2037-CON) | The alert receive endpoint, the routing result and the alert states PENDING, FIRING and RESOLVED with their times | The routing and delivery tests of AC1, AC6, AC7 and AC8 |
| Grafana provisioning fake (RWB-PLT-E2037-CON) | The dashboard provisioning endpoint and the data-source answers for the declared queries | The provisioning and personal-data tests of AC4 |
| P2 rwb-integration contract fake | `GET /admin/scheduled-jobs` returning the JOB-21 and JOB-22 rows and the run book map | The catalogue read and the pipeline gate before the P2 service exists |

The fakes are test-only; they are not deployed into SIT, UAT or production, and no environment value points at one.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 1 | `GET /api/recovery/integration/v1/admin/scheduled-jobs`; one hop, 2 s budget (DP-11) |
| Kafka | 0 | 0 | The platform owns no topic and consumes none; an alert is not an event (DP-14) |
| Temporal | 1 workflow on a Schedule, 3 activities | 0 | StuckWorkflowScanner on task queue `rwb-platform`, JOB-21 every 5 minutes; visibility and history are read through the frontend API, never through the databases |
| File | 0 | 0 | The rule file, the dashboard JSON and the run books are repository content, provisioned through the pipeline and not read as files at runtime |

### 13. Solution plan

**Package.** No Java business package. The rule file and the dashboard live in `ops/monitoring/temporal/`; the scanner lives in `ops/temporal/observability` on the platform worker of RWB-PLT-E1071; the run books live in `docs/operations/runbooks/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemporalAlertRules | Prometheus rule file | The three alerts, their thresholds, their annotations and the repeat interval (BR1 to BR3, BR8) |
| AlertRoutingConfig | Alertmanager configuration | Routes each alert to the platform on-call rota and the incident queue with the run book path |
| WorkflowVisibilityClient | Client | Lists RUNNING workflows and reads a history summary through the frontend gRPC with mTLS; reads no database (BR6) |
| StuckWorkflowScanner | Workflow started by the JOB-21 Schedule, every 5 minutes on task queue `rwb-platform` | The candidate query, the stuck test and the `workflow_stuck` metric (BR2, BR7, BR11) |
| TemporalScannerMetrics | Service | Publishes `workflow_stuck` by workflow type, `temporal_scanner_failures_total` and the last successful scan time |
| TemporalWorkflowDashboard | Dashboard | Grafana JSON for the five panel groups, from the four search attributes (BR4) |
| DashboardPersonalDataCheck | Test | Scans every panel query and the provisioned JSON for a person field or a payload field and fails the build (BR4) |
| AlertRunBookMap | Configuration | Alert name to run book path, held in job_catalog and read through the P2 admin operation (BR5) |
| TemporalObservabilityRunBooks | Document | Three run books with the eight sections of RWB-PLT-E1056-OPS |
| CaseHoldWorkflow | Test workflow | Test scope only: a workflow that can be held with no progress or left on a 30-day timer, for the scanner tests and the SIT fixture (AC2, AC8) |
| ScanScheduleBootstrap | Configuration | Registers the JOB-21 Schedule on task queue `rwb-platform` every 5 minutes with overlap policy SKIP; idempotent, so a second run changes nothing (BR11) |

**Database.** No migration. The scanner gets its job_catalog row through the P2 admin operation as a data change, with its owner role, schedule, run book path and alert threshold; the alert-to-run-book map is the same row family. No table is created or changed (DP-01, DP-15).

**Configuration and reference data**

- Parameter through the parameters contract (DP-06): `temporal.stuck.hours` = 24 (assumed; ASM-2541).
- Rule-file values: the 5-minute failure window, the 60-second p95 latency threshold, the 10-minute duration and the 5-minute scan cadence, owned by RW-PLATADM and published by RWB-PLT-E2037-CON.
- Alertmanager route, repeat interval and on-call rota from the ACE monitoring configuration; the severity vocabulary is read through the reference-data contract and is not a Java literal (DP-07).
- No business parameter and no reference table of its own in this story.

**Build steps**

1. Add the three alert rules and the run book annotations; unit test the expressions with the metric fixtures for AC1 and AC3.
2. Build WorkflowVisibilityClient against the SIT frontend with mTLS; prove it reads no database and returns the candidate list.
3. Build StuckWorkflowScanner as a workflow started by the JOB-21 Schedule on task queue `rwb-platform`, with the candidate query, the timer and retry exclusions and the stale marker; test AC2 and AC6.
4. Add the `workflow_stuck` and scanner failure metrics and the last-successful-run time; assert the declared names and labels of RWB-PLT-E2037-CON.
5. Import the dashboard, run DashboardPersonalDataCheck over every panel query, and test AC4.
6. Write the three run books, add the alert-to-run-book map through the P2 admin operation and pass RunbookCompletenessTest; test AC5 and AC7.
7. Run the alert drill in SIT: fail a smoke workflow, hold a test workflow, stop the worker and clear each alert; test AC8 and confirm the 5-minute cadence in the Schedule history (BR11).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**DP-10** is the substantive row of this story: the legacy `StuckWorkflowScanner` was a Quartz job on a 15-minute interval, and in the target it is JOB-21, a Temporal Schedule on task queue `rwb-platform` every 5 minutes, whose run is a short workflow with overlap policy SKIP (Architecture v5 slide 44; Ownership Map jobs JOB-21). The workflow kit of RWB-PLT-E1071-CON supplies the Schedule and the run, so the scanner needs no scheduler table, no cluster-wide cron and no second job store, and the legacy Quartz interval is superseded rather than re-implemented (GAP-1446).

**DP-03** is declared and not exercised: an alert, a scan and a dashboard panel are operational state, never a credit decision, so this story writes no decision record. The dependency stays because the scanner runs on the platform worker built from the service template, which wires the local decision-record library of RWB-PLT-E1027-CON; the observability path never calls it.

**DP-06** and **DP-07** keep the numbers out of the code: `temporal.stuck.hours`, the p95 threshold, the 10-minute duration and the 5-minute cadence are parameter and rule-file values read through the published contracts, and the severity vocabulary is reference data, so a threshold change is a configuration change and not a release. **DP-01**, **DP-05**, **DP-13**, **DP-14**, **DP-15** and **DP-19** are declared as absences, which is what a platform story owes the split: no `rwb_*` schema is read or written, no ACE view is read, no `/api/recovery` base is published, no topic is owned, no migration runs, and the dashboard is not a Workbench screen and adds no route to the gateway.

**Feature flag.** `rwb.p3.temporal`, read through the parameters contract. The alerts and the dashboard are operations assets and stay in place; with the flag off, no workflow starts and the scanner reports zero stuck workflows from a successful scan.

**Done when.** The tests in section 16 pass in SIT, the three alerts fire and resolve on the test fixtures, the Schedule history shows the 5-minute JOB-21 cadence, each alert names a complete run book, and the dashboard passes the personal-data check.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-037 | A workflow has failed, or has not moved for the stuck window | Workflow {workflowId} has failed or has not moved for {hours} hours. |

MSG-P3-037 is carried in the annotation of TemporalWorkflowFailed and TemporalWorkflowStuck, with {hours} read from the workflow age at failure or from the scanner. The latency alert has its own summary text and names the task queue and the p95; it uses no new message ID. A failed scan is reported through the incident and the metric, not through a message. The scan itself writes no Workbench message and no screen error: the platform has no `/api/recovery` base, so every operator signal is an alert, a metric, a dashboard panel or a run book line. The platform identity and the dashboard names are Not specified in the source documents (GAP-1444; ASM-2539) and are read from the Wave 0 Service Catalog when it is published.

### 15. Screens and states

Screen list: one screen, the Grafana dashboard "Temporal workflows"; no Workbench screen in this story. Its two data states are: current, and data stale since the last successful scan. The dashboard shows running, failed, completed and timed-out counts by workflow type, schedule-to-start latency, task queue backlog, stuck workflows and worker build IDs. Alertmanager shows the alert states PENDING, FIRING and RESOLVED. The job monitor of RWB-PLT-E1056-OPS shows the scanner's last run, status and duration; the platform console of RWB-PLT-E1070-APP shows the cluster and the workers, not the workflows. The platform screens of Epic 8 do not repeat this data, and the dashboard is not composed by gateway-bff (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-037-01 | AC1, BR1 | Integration | platform-smoke-20261116 failed at 10:12; alert evaluated at 10:13; delivery inside 5 minutes |
| TC-E2-037-02 | AC2, BR2 | Integration | case-RW-2026-000123 held 24 hours; case-RW-2026-000124 on a 30-day timer |
| TC-E2-037-03 | AC3, BR3 | Integration | Worker stopped 11:00 to 11:20; p95 120 seconds at 11:12; 12 tasks waiting |
| TC-E2-037-04 | AC4, BR4 | Component | Dashboard JSON with 40 panel queries; the four search attributes only |
| TC-E2-037-05 | AC5, BR5 | Component | Three alert rules and three run books with the eight sections |
| TC-E2-037-06 | AC6, BR7 | Integration | Frontend unreachable at 09:05; scanner run; no zero published |
| TC-E2-037-07 | AC7, BR5 | Component | Branch adds TemporalWorkerDown with no run book in the map |
| TC-E2-037-08 | AC8, BR8, BR9 | Integration | Stuck alert PENDING at 09:05; progress at 09:06; delivery at 09:10 |
| TC-E2-037-09 | AC3, BR3, BR11 | NFR | Rule files loaded in the ACE Prometheus; a worker stop raises and clears the latency alert; the Schedule history shows the 5-minute JOB-21 cadence |
| TC-E2-037-10 | AC4, BR4 | Component | DashboardPersonalDataCheck over all 40 panel queries and the provisioned JSON |
| TC-E2-037-11 | BR2, BR7, BR11 | Contract | Activities scanStuckWorkflows, publishScannerMetrics and recordScanRun and workflow StuckWorkflowScanner of section 12, against the RWB-PLT-E1071-CON and RWB-PLT-E1070-CON fakes; no event, as section 12 declares none |
| TC-E2-037-12 | AC9, BR6, BR10 | Component | Scanner code and deployment configuration; Temporal frontend API over mTLS; no grant on the Temporal databases |
| TC-E2-037-13 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-PLT-E2037-APP-AC10) |

The checks are run by the platform administrator in SIT and recorded in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the stuck window, the thresholds, the cadence, the repeat interval and the routing rota are configuration.
- No personal data in logs, tests, workflow history or prompts: the dashboard reads the four search attributes only; the tests use synthetic workflow IDs.
- No read of another service's tables and no ACE view: this story reads no case table, no ACE table and no `rwb_*` schema; the catalogue comes through the P2 admin operation (DP-01, DP-05).
- The scanner reads visibility and history through the frontend API and holds no grant on the Temporal databases (BR6).
- No panel reads a payload, a history event or a case field, and no alert annotation carries a payload.
- A failed scan never publishes zero, and the panel says the data is stale.
- No alert without a run book, and no run book that names a person: roles and service identities only.
- No silencing of an alert outside an open incident.
- No Quartz, no scheduler table and no second job store: JOB-21 is a Temporal Schedule on task queue `rwb-platform` every 5 minutes (DP-10, BR11).
- No platform topic, no platform `/api/recovery` base and no `rwb_*` schema: the platform is not one of the 19 services (DP-13, DP-14).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner and has a tested way back | Epic 2, 3.2; Program, 6.12 | None (platform enabler) | All recovery processes | R-UNI-40; ADR-023 | TC-E2-037-01, TC-E2-037-02, TC-E2-037-03, TC-E2-037-05, TC-E2-037-06, TC-E2-037-07, TC-E2-037-08, TC-E2-037-11 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E2037-CON | Contract | H: publishes the metric names and labels, the three alert rules and their annotation, the dashboard data contract, the alert-to-run-book map and the scanner query contract, with the metric fixtures, the Alertmanager fake and the Grafana provisioning fake |
| RWB-PLT-E1070-CON | Contract | H: the namespace `rwb-recovery`, its retention, the four search attributes, the client certificate profile and the frontend API subset the scanner calls |
| RWB-PLT-E1071-CON | Contract | H: the platform worker on task queue `rwb-platform`, its build ID, its SDK metrics and the Schedule and run the scanner uses (DP-10) |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the platform worker template wires; the observability path writes no decision record (DP-03) |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the platform parameters and reference data, so `temporal.stuck.hours` and the severity vocabulary are values (DP-06, DP-07) |
| RWB-PLT-E1047-CON | Contract | H: the topic and event naming library; the platform owns no topic (DP-14) |
| RWB-PLT-E1044-CON | Contract | H: the Flyway convention this story deliberately does not use (DP-15) |
| RWB-PLT-N001-CON | Contract | H: gateway-bff; the dashboard is not a Workbench screen (DP-19) |
| RWB-PLT-E1056-OPS | DevOps | X: holds the run book catalog, the eight run book sections and RunbookCompletenessTest that gate the three run books of this story |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the parameters and reference data built against their published contracts and fakes |
| RWB-PLT-E1070-APP, RWB-PLT-E1071-APP | App development | The cluster and the worker this story watches; they are not changed here |
| RWB-PLT-E2038-APP, RWB-PLT-E2038-CON | Successors of RWB-E2-038 | Out of scope: the codec server, decode and the Temporal admin audit |
| RWB-E2-039, RWB-E2-040 | Legacy successors | Out of scope: backup, restore, zone failover, upgrade and archive; the replay gate and build ID rollout |

### 19. Out of scope

- The Temporal cluster, namespace, mTLS, Web UI and platform dashboard (RWB-PLT-E1070-APP).
- The worker, the codec and the smoke workflow (RWB-PLT-E1071-APP), and the platform smoke Schedule JOB-22.
- The codec server, decode and the Temporal admin audit (RWB-PLT-E2038-APP, RWB-PLT-E2038-CON).
- Backup, point-in-time restore, zone failover, upgrade procedure and archive (the successors of RWB-E2-039).
- The replay gate, history export for tests and build ID rollout (the successor of RWB-E2-040).
- Case-level service level alerts and the next action overdue marker (the successor of RWB-E2-015).
- Application performance monitoring of the Workbench API and the job alerts of the Workbench jobs (RWB-PLT-E1056-OPS).
- The 19 services' own metrics, dashboards and task queues, and any alert on a service's business behaviour.
- Workbench screens and the admin console (Epic 8); the dashboard is an operational view, not a Workbench screen.
