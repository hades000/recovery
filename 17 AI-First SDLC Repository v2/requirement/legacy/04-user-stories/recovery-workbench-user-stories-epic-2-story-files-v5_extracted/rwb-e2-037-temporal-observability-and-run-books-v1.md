<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 037 Temporal observability and run books v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 037 Temporal observability and run books v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-037 Temporal observability and run books

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-037 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None (platform enabler) |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Epic 2, section 3.2; Business Requirements Program, section 6.12 |
| L3 process | All recovery processes |
| Decision | D-RCV-36 (T1); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-070, RWB-E1-071, RWB-E1-056 |
| Status | Ready for build |

## 1. Story

As a **platform administrator (RW-PLATADM)**, I want **Temporal metrics, an alert for every failed or stuck workflow and a dashboard that shows workflow volume by type and status, each alert with its own run book**, so that **a workflow problem is seen before a case waits**.

## 2. Business rationale

Case workflows from Epic 3 wait for days on durable timers, and a workflow that has stopped moving looks exactly like a workflow that is waiting. Nothing in the Workbench watches a workflow execution today: the job monitor of RWB-E1-056 watches Quartz jobs, and the platform dashboard of RWB-E1-070 watches the five Temporal services, not the workflows those services run. Without this story the first sign of a workflow that cannot progress is a case owner asking why the case has not moved.

This story adds the three signals that cover the ways a workflow stops: an execution that closes FAILED or TIMED_OUT, an execution with no progress for temporal.stuck.hours (24, assumed), and a schedule-to-start latency above its threshold. It adds one Grafana dashboard grouped by workflow type and status with no personal data, and a run book for each alert so that the platform administrator acts without the developer. It meets REQ-DRI-007 (a named owner and a tested way back for every failure). The measure is that every alert reaches the on-call rota within 5 minutes in SIT and names a run book.

## 3. Preconditions

- RWB-E1-070 is done: the Temporal cluster, the namespace rwb-recovery, mTLS, the Web UI and the metrics scrape to the ACE monitoring stack exist in DEV and SIT.
- RWB-E1-071 is done: the worker polls rwb-platform, carries a build ID, runs PlatformSmokeWorkflow daily and writes its PLATFORM_SMOKE decision log entry.
- RWB-E1-056 is done: job_catalog, the run book catalog, RunbookCompletenessTest and its eight run book headings exist and accept a new job and a new run book.
- Prometheus, Alertmanager and Grafana run in the ACE monitoring namespace, and the platform on-call rota and the incident queue of the operations team exist.
- The parameter temporal.stuck.hours = 24 is in the catalog through RWB-E1-042; the value is assumed until the platform administrator confirms it with the operations team.
- The SIT worker registers the test-only workflow CaseHoldWorkflow on rwb-platform, which can be held with no progress or left on a timer; it is not deployed to UAT or PROD.
- The scanner runs as SY-CASEWF with the client certificate of RWB-E1-070 and holds no grant on the Temporal databases.
- Feature flag rwb.p3.temporal is on in SIT.

## 4. Flow

1. Prometheus: scrapes the Temporal server metrics of RWB-E1-070 and the worker SDK metrics of RWB-E1-071 every 15 seconds.
2. TemporalAlertRules: evaluate TemporalWorkflowFailed when an execution closes FAILED or TIMED_OUT, and TemporalScheduleToStartLatency when the p95 schedule-to-start latency on a task queue is above 60 seconds for 10 minutes.
3. StuckWorkflowScanner (Quartz, every 15 minutes): calls ListWorkflowExecutions for RUNNING workflows whose StartTime is older than temporal.stuck.hours, then reads the history summary of each candidate through the frontend.
4. StuckWorkflowScanner: marks a candidate stuck only when it has no history event for temporal.stuck.hours, no open timer and no activity in retry, and publishes the count as workflow_stuck by workflow type.
5. TemporalWorkflowStuck: fires on a stuck count above zero with MSG-P3-037, the workflow ID and the hours since the last event.
6. Alertmanager: routes each alert to the platform on-call rota and the incident queue, with the run book path in the annotation and one alert per workflow and condition.
7. Platform administrator: opens the dashboard, reads the workflow type, task queue and build ID, and follows the run book for the check, restart or drain step.
8. Dashboard "Temporal workflows": shows running, failed, completed and timed-out counts by type, schedule-to-start latency by task queue, task queue backlog, stuck workflows and worker build IDs, all from the four search attributes.
9. StuckWorkflowScanner: records its last successful run; a failed scan marks the stuck panel stale and raises an incident, and never publishes a zero.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The Temporal frontend is unreachable from the scanner, so the visibility query fails | No stuck value is published and no stuck alert is raised; the scanner failure counter rises; the stuck panel shows data stale since the last good scan; an incident reaches RW-PLATADM | None (incident and metric only) | AC6 |
| X2 | An alert rule has no run book, or its run book lacks one of the eight sections | The pipeline fails naming the alert and the missing section; the rule file is not deployed | None (build log) | AC7 |
| X3 | A workflow makes progress between the scan and the delivery of its alert | The alert resolves at the next evaluation; no page is sent and no incident is opened | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds alerts, one Quartz scanner, one dashboard and three run books on the platform of RWB-E1-070 and the worker of RWB-E1-071 |
| Negotiable | Thresholds, the stuck window, the repeat interval, the panels and the routing rota are configuration; the three signals and the run book rule are fixed |
| Valuable | A workflow problem reaches a named owner before a case owner notices the case has stopped |
| Estimable | Three alert rules, one scanner, one dashboard, one run book map and three run books |
| Small | Fits two weeks with its checks |
| Testable | Each criterion in section 7 has one test in section 16, on fixed workflows and fixed thresholds |

## 7. Acceptance criteria

```gherkin
Feature: Temporal observability and run books

  Background:
    Given the Temporal cluster of RWB-E1-070 runs in SIT with namespace rwb-recovery
    Given the worker of RWB-E1-071 polls rwb-platform with build ID "9f3c2a1-418"
    Given the parameter temporal.stuck.hours is 24
    Given Alertmanager routes the Workbench platform alerts to the platform on-call rota

  Scenario: AC1 A failed workflow raises an alert within five minutes
    Given workflow "platform-smoke-20261116" started at 07:00 on 16 November 2026 on task queue rwb-platform
    When the workflow closes FAILED at 10:12
    Then the rule TemporalWorkflowFailed is FIRING at the 10:13 evaluation with severity "page"
    Then the alert annotation carries MSG-P3-037 with workflowId "platform-smoke-20261116" and hours 3
    Then Alertmanager delivers the alert to the platform on-call rota within 5 minutes of the close
    Then the dashboard count of failed PlatformSmokeWorkflow executions for the day is 1

  Scenario: AC2 A workflow with no progress raises an alert, and a timed wait does not
    Given workflow "case-RW-2026-000123" of type CaseHoldWorkflow on task queue rwb-platform is RUNNING
    Given its last history event is at 09:00 on 15 November 2026 and it has no open timer and no activity in retry
    Given workflow "case-RW-2026-000124" of the same type is RUNNING and started timer "wait-30-days" at 10:00 on 14 November 2026
    When StuckWorkflowScanner runs at 09:05 on 16 November 2026
    Then "case-RW-2026-000123" is marked stuck with 24 hours since its last progress
    Then TemporalWorkflowStuck is FIRING with MSG-P3-037, workflowId "case-RW-2026-000123" and hours 24
    Then "case-RW-2026-000124" is not marked stuck and no alert exists for it

  Scenario: AC3 Schedule-to-start latency raises an alert
    Given the worker stops polling rwb-platform at 11:00 on 16 November 2026
    Given the rule threshold is a p95 schedule-to-start latency of 60 seconds for 10 minutes
    When 12 tasks wait on rwb-platform and the p95 reaches 120 seconds at 11:12
    Then TemporalScheduleToStartLatency is FIRING with taskQueue "rwb-platform" and p95 "120s"
    Then Alertmanager delivers the alert to the platform on-call rota
    Then the dashboard panel "Schedule-to-start latency" shows the spike for rwb-platform
    When the worker resumes at 11:20 and the p95 returns below 60 seconds
    Then the alert resolves at the next evaluation

  Scenario: AC4 The dashboard shows volume by type and status with no personal data
    Given the dashboard "Temporal workflows" is provisioned from ops/monitoring/temporal/workflow-dashboard.json
    When U-70 opens it for the rwb-recovery namespace
    Then it shows running, failed, completed and timed-out counts by workflow type
    Then it shows schedule-to-start latency by task queue, task queue backlog, stuck workflows and worker build IDs
    Then every panel query uses the search attributes CaseId, Stage, ProductGroup and QueueCode only
    Then DashboardPersonalDataCheck finds no person field and no payload field in the 40 panel queries
    Then no panel shows a workflow input, a workflow output or a history event payload

  Scenario: AC5 Every alert has a run book
    Given the rule file holds TemporalWorkflowFailed, TemporalWorkflowStuck and TemporalScheduleToStartLatency
    When RunbookCompletenessTest runs in the pipeline
    Then each alert names a run book in docs/operations/runbooks with the eight sections
    Then each run book names the alert, the check, the restart or drain step and the escalation
    Then the build passes with the three run books

  Scenario: AC6 The scanner cannot reach the frontend
    Given the Temporal frontend is unreachable from the scanner at 09:05 on 16 November 2026
    When StuckWorkflowScanner runs
    Then it publishes no workflow_stuck value and raises no TemporalWorkflowStuck alert
    Then temporal_scanner_failures_total increases by one
    Then the dashboard panel "Stuck workflows" shows "data stale since 09:05"
    Then an incident reaches RW-PLATADM naming the scanner error
    Then no workflow is marked stuck

  Scenario: AC7 An alert with no run book fails the build
    Given a branch adds the alert TemporalWorkerDown to the rule file with no entry in the alert-to-run-book map
    When RunbookCompletenessTest runs
    Then the build fails naming "TemporalWorkerDown" and the missing run book
    Then the rule file is not deployed to SIT or PROD

  Scenario: AC8 An alert clears before it is delivered
    Given TemporalWorkflowStuck is PENDING for "case-RW-2026-000125" at 09:05 with 25 hours since its last event
    When the worker picks up the workflow and it records a new history event at 09:06
    Then the alert resolves at the 09:10 evaluation
    Then Alertmanager sends no page and opens no incident
    Then the alert history keeps the PENDING and RESOLVED states with their times
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A workflow that closes FAILED or TIMED_OUT raises TemporalWorkflowFailed with MSG-P3-037, and the alert reaches the on-call rota within 5 minutes of the close | REQ-DRI-007; AC1 |
| BR2 | A RUNNING workflow with no history event for temporal.stuck.hours (24, assumed), no open timer and no activity in retry raises TemporalWorkflowStuck; a workflow that waits on a durable timer is never stuck | AC2 |
| BR3 | A p95 schedule-to-start latency above 60 seconds for 10 minutes on a task queue raises TemporalScheduleToStartLatency; both values are rule-file configuration | AC3 |
| BR4 | The dashboard groups by workflow type and status and reads the four search attributes only; no panel reads a payload, a history event or a case table | D-RCV-36 T1; AC4 |
| BR5 | Every alert names a run book with the eight sections of RWB-E1-056; RunbookCompletenessTest fails the build when one is missing or incomplete | RWB-E1-056; AC5 |
| BR6 | The scanner reads visibility and history through the Temporal frontend API over mTLS and never reads the Temporal databases; it holds no grant on them | D-RCV-36 T1 |
| BR7 | A failed scan publishes no stuck value and marks the panel stale; it never publishes zero in place of a result | AC6 |
| BR8 | One alert per workflow and condition; a repeated evaluation updates the same alert and opens no second incident | AC8 |
| BR9 | An alert resolves when its condition clears, and a resolved alert leaves no open incident and no open page | AC8 |
| BR10 | Thresholds, the stuck window, the repeat interval, the panel list and the routing rota are configuration, never code | REQ-DRI-007 |

## 9. State transitions

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

The workflow states COMPLETED, FAILED and TIMED_OUT are Temporal's; no recovery case status changes.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM | Reads the alerts, the dashboard and the scanner status; works the incident and follows the run book; silences an alert for the duration of an open incident and records the silence in it (Platform administration, R) |
| RW-AUDIT | Reads the dashboard and the alert history (Platform administration, R) |
| RW-TRIBE | Writes the rule file, the dashboard JSON and the run books through the change process; may not silence an alert in PROD |
| RW-CASEOWN and the other case roles | No access to the alerts or the dashboard; they see the case, not the engine |
| SY-CASEWF | Runs the scanner and publishes the metrics; holds no screen right |
| SY-RULES | No part in this story |
| No delegation of authority level applies | An operational alert is not a credit decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| None (platform enabler) | None in the recovery schema | None | None |

Alert state lives in Prometheus and Alertmanager, and workflow, timer and task state lives in Temporal persistence and visibility (RWB-E1-070). The scanner's last run, its owner and the alert-to-run-book map live in job_catalog through RWB-E1-056. No DF-REF, DF-CAS or DF-DEC field is added or changed, and the dashboard reads the search attributes CaseId, Stage, ProductGroup and QueueCode only. The Physical Schema v6 is unchanged.

## 12. Contract

No Workbench endpoint. This story adds no path under /api/recovery/v1. The interfaces are the monitoring stack and the Temporal frontend.

| Interface | Method | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| Prometheus scrape | HTTPS GET /metrics, port 9090 | Scrape of the Temporal server and worker SDK metrics | OpenMetrics text | None | Network policy from the ACE monitoring namespace only | Read only |
| Alertmanager | HTTPS POST /api/v2/alerts | Alert name, labels, annotations with MSG-P3-037 and the run book path | 200 when accepted | 400 malformed alert; 503 receiver down | Alertmanager API from the Prometheus pods only | Alert fingerprint: a repeat updates the same alert and opens no second incident |
| Temporal frontend | gRPC over mTLS, port 7233: ListWorkflowExecutions, GetWorkflowExecutionHistory, DescribeWorkflowExecution | namespace rwb-recovery, query RUNNING and StartTime older than 24 hours, workflow ID | WorkflowExecution and history summary | TLS handshake failure; PERMISSION_DENIED; NOT_FOUND namespace; UNAVAILABLE | Client certificate of SY-CASEWF with the namespace claim | Read only |
| Grafana provisioning | HTTPS 443, dashboard JSON from the repository | Dashboard definition and the data sources | 200 when provisioned | 400 malformed JSON; 403 data source refused | Grafana administrator through the pipeline; viewers RW-PLATADM and RW-AUDIT | Repeat provisioning of the same JSON changes nothing |

The scanner never receives a Workbench JWT and never reads the Temporal databases. The dashboard reads Prometheus and the Temporal data source, not a Workbench table.

## 13. Solution plan

**Package.** No Java business package. The rule file and the dashboard live in `ops/monitoring/temporal/`; the scanner lives in `recovery/integration/ops/temporal` (Java package `recovery.integration.ops.temporal`); the run books live in `docs/operations/runbooks/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemporalAlertRules | Prometheus rule file | The three alerts, their thresholds, their annotations and the repeat interval (BR1 to BR3, BR8) |
| AlertRoutingConfig | Alertmanager configuration | Routes each alert to the platform on-call rota and the incident queue with the run book path |
| WorkflowVisibilityClient | Client | Lists RUNNING workflows and reads a history summary through the frontend gRPC with mTLS; reads no database (BR6) |
| StuckWorkflowScanner | Job | Quartz, every 15 minutes: the candidate query, the stuck test and the workflow_stuck metric (BR2, BR7) |
| TemporalScannerMetrics | Service | Publishes workflow_stuck by workflow type, temporal_scanner_failures_total and the last successful scan time |
| TemporalWorkflowDashboard | Dashboard | Grafana JSON for the five panel groups, from the four search attributes (BR4) |
| DashboardPersonalDataCheck | Test | Scans every panel query and the provisioned JSON for a person field or a payload field and fails the build (BR4) |
| AlertRunBookMap | Configuration | Alert name to run book path, read by RunbookCompletenessTest (BR5) |
| TemporalObservabilityRunBooks | Document | Three run books with the eight sections of RWB-E1-056 |
| CaseHoldWorkflow | Test workflow | Test scope only: a workflow that can be held with no progress or left on a 30-day timer, for the scanner tests and the SIT fixture (AC2, AC8) |

**Database.** No migration. The scanner gets one job_catalog row through RWB-E1-056 as a data change, with its owner role, schedule, run book path and alert threshold. No table is created or changed.

**Configuration and reference data**

- Parameter through RWB-E1-042: temporal.stuck.hours = 24 (assumed).
- Rule-file values: the 5-minute failure window, the 60-second p95 latency threshold and the 10-minute duration, owned by RW-PLATADM.
- Alertmanager route, repeat interval and on-call rota from the ACE monitoring configuration.
- No business parameter and no reference table in this story.

**Build steps**

1. Add the three alert rules and the run book annotations; unit test the expressions with synthetic metric series for AC1 and AC3.
2. Build WorkflowVisibilityClient against the SIT frontend with mTLS; prove it reads no database and returns the candidate list.
3. Build StuckWorkflowScanner with the candidate query, the timer and retry exclusions and the stale marker; test AC2 and AC6.
4. Add the workflow_stuck and scanner failure metrics and the last-successful-run time.
5. Import the dashboard, run DashboardPersonalDataCheck over every panel query, and test AC4.
6. Write the three run books, add the alert-to-run-book map and pass RunbookCompletenessTest; test AC5 and AC7.
7. Run the alert drill in SIT: fail a smoke workflow, hold a test workflow, stop the worker and clear each alert; test AC8.

**Feature flag.** None. The alerts and the dashboard are operations assets; with rwb.p3.temporal off, no workflow starts and the scanner reports zero stuck workflows from a successful scan.

**Done when.** The tests in section 16 pass in SIT, the three alerts fire and resolve on the test fixtures, each alert names a complete run book, and the dashboard passes the personal-data check.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-037 | A workflow has failed, or has not moved for the stuck window | Workflow {workflowId} has failed or has not moved for {hours} hours. |

MSG-P3-037 is new and is added to Error and Message Standard v4. It is carried in the annotation of TemporalWorkflowFailed and TemporalWorkflowStuck, with {hours} read from the workflow age at failure or from the scanner. The latency alert has its own summary text and names the task queue and the p95; it uses no new message ID. A failed scan is reported through the incident and the metric, not through a message.

## 15. Screens and states

No Workbench screen in this story. The operational view is the Grafana dashboard "Temporal workflows" with two data states: current, and data stale since the last successful scan. The dashboard shows running, failed, completed and timed-out counts by workflow type, schedule-to-start latency, task queue backlog, stuck workflows and worker build IDs. Alertmanager shows the alert states PENDING, FIRING and RESOLVED. The Workbench job monitor of RWB-E1-056 shows the scanner's last run, status and duration. The platform screens of Epic 8 do not repeat this data.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-037-01 | AC1, BR1 | System | platform-smoke-20261116 failed at 10:12; alert evaluated at 10:13 |
| TC-E2-037-02 | AC2, BR2 | System | case-RW-2026-000123 held 24 hours; case-RW-2026-000124 on a 30-day timer |
| TC-E2-037-03 | AC3, BR3 | System | Worker stopped 11:00 to 11:20; p95 120 seconds at 11:12 |
| TC-E2-037-04 | AC4, BR4 | System | Dashboard JSON with 40 panel queries; search attributes only |
| TC-E2-037-05 | AC5, BR5 | System | Three alert rules and three run books |
| TC-E2-037-06 | AC6, BR7 | System | Frontend unreachable at 09:05; scanner run |
| TC-E2-037-07 | AC7, BR5 | System | Branch adds TemporalWorkerDown with no run book |
| TC-E2-037-08 | AC8, BR8, BR9 | System | Stuck alert PENDING at 09:05; progress at 09:06; delivery at 09:10 |
| TC-E2-037-09 | Operational | Operational | Rule files loaded in the ACE Prometheus; a worker stop raises and clears the latency alert |
| TC-E2-037-10 | Operational | Operational | DashboardPersonalDataCheck over all panel queries and the provisioned JSON |

The checks are run by the platform administrator in SIT and recorded in the release evidence; there is no Workbench endpoint and no Access test in this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the stuck window, the thresholds, the repeat interval and the routing rota are configuration.
- No personal data in logs, tests, workflow history or prompts: the dashboard reads the four search attributes only; the tests use synthetic workflow IDs.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: this story reads no case and no ACE table.
- The scanner reads visibility and history through the frontend API and holds no grant on the Temporal databases.
- No panel reads a payload, a history event or a case field, and no alert annotation carries a payload.
- A failed scan never publishes zero, and the panel says the data is stale.
- No alert without a run book, and no run book that names a person.
- No silencing of an alert outside an open incident.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner and has a tested way back | Epic 2, 3.2; Program, 6.12 | None (platform enabler) | All recovery processes | R-UNI-40 | TC-E2-037-01, TC-E2-037-02, TC-E2-037-03, TC-E2-037-05, TC-E2-037-06, TC-E2-037-07, TC-E2-037-08 |

## 19. Out of scope

- The Temporal cluster, namespace, mTLS, Web UI and platform dashboard (RWB-E1-070).
- The worker, the codec and the smoke workflow (RWB-E1-071).
- The codec server, decode and the Temporal admin audit (RWB-E2-038).
- Backup, point-in-time restore, zone failover, upgrade procedure and archive (RWB-E2-039).
- The replay gate, history export for tests and build ID rollout (RWB-E2-040).
- Case-level service level alerts and the next action overdue marker (RWB-E2-015).
- Application performance monitoring of the Workbench API and the Quartz job alerts (RWB-E1-056).
- Temporal Schedules and any Temporal alerting on a schedule (Epic 3).
