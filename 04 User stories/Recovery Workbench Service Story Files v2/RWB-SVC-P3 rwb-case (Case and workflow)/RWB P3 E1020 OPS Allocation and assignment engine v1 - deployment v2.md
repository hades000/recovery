# RWB-P3-E1020-OPS Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1020-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-I |
| Ready to start | Day 1 |
| Size | To be sized by the squad at refinement (DOR-RWB-P3-E1020-OPS-16) |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| Contract version | v1 (REST path suffix /v1, DP-13); the published contract version number is Not specified in the source documents (DOR-RWB-P3-E1020-OPS-23) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-009, FR-P3-010, FR-P3-011, FR-P3-012, FR-P3-030) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-020 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 25 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the allocation worker of rwb-case, its DailyCaseRun schedule, its topic with retry and dead-letter topics, its metrics, its alerts, its runbook and its feature-flag rollout deployed as code**, so that **the morning allocation runs by itself by 07:00 with no Quartz table, no manual start and no silent failure**.

This is the deployment slice of legacy RWB-E1-020 in rwb-case. It delivers, all through the platform Helm chart and the service pipeline:

- the **worker deployment** of rwb-case that polls task queue `rwb-case` in namespace `rwb-recovery` and scales on backlog;
- the **DailyCaseRun** Temporal Schedule registration, and the event-started run that `AceDataReady` triggers; the legacy job name **JOB-03 Morning allocation** is kept in the runbook, the dashboards and the alerts, and the legacy Quartz trigger is gone;
- the **topic provisioning** of `rwb.case.events.v1` with its retry topics (1 min, 10 min, 1 h) and its `.dlt`, the ACLs for the consumers, and the producer side of `rwb.decision-record.v1`;
- the **allocation metrics and alerts**: cases read, assigned, overflow, exception, failed, skipped, the four family messages, the stuck-run alert and the dead-letter alert;
- the **runbook** for the morning run, carrying the legacy RWB-E1-056 job monitoring content;
- the **feature-flag rollout** of `rwb.case.allocation`, with the flag as data in the platform library.

### 2. Business rationale

The legacy story depended on a Quartz job on a shared scheduler and on a job monitor that a person had to read. Nothing was deployed per service and nothing scaled on load. In the target the allocation engine is one worker of one service, with its own task queue, its own topic and its own dashboards, so the morning run either finishes by 07:00 or raises an alarm that names the run, the case count and the reason.

The cost of a silent failure is high: if the morning allocation does not run, every new case stays NEW with no queue and no owner, and the service level of the whole book starts to slip on the first day. The alerts and the runbook are therefore part of the story, not an afterthought.

### 3. Preconditions

- The rwb-case service is created from the service template with its Helm chart, its golden pipeline and its `api` and `worker` deployments (RWB-PLT-TPL, RWB-PLT-LIB).
- Schema `rwb_case` and the service login exist (RWB-PLT-DB); the per-service login name is Not specified in the source documents (GAP-0684; ASM-1231), so the chart takes it from a Key Vault reference and never from a value in the repository.
- The Temporal cluster is at 1.30 or later, namespace `rwb-recovery` exists and task queue `rwb-case` is agreed (RWB-PLT-WF).
- The Kafka platform accepts the topic definitions of the service (RWB-PLT-EVT); Azure Event Hubs Premium is the fallback.
- The workflow kit is available for the Schedule and the event-started workflow (RWB-PLT-E1071-CON), and the outbox and inbox library for the producer side (RWB-PLT-TE006-CON).
- The feature-flag library is available (platform library), and the contract of 12.1 is published (RWB-P3-E1020-CON).
- The build of the allocation engine can be absent: this story deploys and wires, and the flag keeps the path closed until the build story is accepted.

### 4. Flow

1. **Chart and values.** The worker deployment, the service account, the Key Vault references, the resource requests and limits, the horizontal autoscaling on task-queue backlog, the pod disruption budget, the readiness and liveness probes, the OpenTelemetry exporter and the log format are set in the Helm values of the service.
2. **Database access.** The chart mounts the service login and connection pool from Key Vault; the login name is Not specified in the source documents (GAP-3207) see RWB-PLT-DB; the Flyway migration of the allocation columns runs as a pre-deploy job in the rwb-case sequence (DP-15). No schema outside `rwb_case` is granted.
3. **Temporal.** The worker connects to namespace `rwb-recovery` and polls only `rwb-case`; the payload codec keys come from Key Vault; the build ID is published to the worker versioning record so a new build takes new runs while the old drains.
4. **Schedules.** The DailyCaseRun Schedule is created by the deployment, idempotently, with overlap policy SKIP, a catch-up window and the business-date input; the JOB-06 rebalancing Schedule at 06:30 is registered on the same queue. The primary trigger is the event start on AceDataReady, and one catch-up Schedule is registered per business date with overlap policy SKIP. The exact schedule expression of the date-based run is Not specified in the source documents (GAP-0686; ASM-1233; GAP-3208), so it is a value in the chart and not a constant in code; the 07:00 Asia/Bangkok deadline is the time the alert measures.
5. **Kafka.** The topic `rwb.case.events.v1` is created with the platform defaults (12 partitions, replication factor 3, 7-day retention, key caseId, CloudEvents binary mode), with `rwb.case.events.v1.retry.1m`, `.retry.10m`, `.retry.1h` and `rwb.case.events.v1.dlt`; ACLs allow rwb-case to produce, and the documented consumers to read; the producer side of `rwb.decision-record.v1` is granted.
6. **Observability.** Counters and histograms for cases read, assigned, overflow, exception, failed and skipped; a timer for the run duration; a gauge for the last successful run per business date; counters for the four message identifiers and for the dead-letter topic; one trace from the event to the transaction, with the case number as an attribute and no personal data.
7. **Alerts.** Alert on: no successful DailyCaseRun for the current business date by the agreed deadline; a run with any FAILED_LOG case; a non-empty dead-letter topic; `NoPackageInForce` raised by the activity; the workflow stuck for longer than the agreed window; the schedule not registered after a deployment. Thresholds live in the chart values and are reviewed with the service owner.
8. **Runbook.** One page: what the run is, when it runs, how to see the run in the Temporal UI, how to see the counts, how to retry a business date, how to check the rule model version, how to re-drive the dead-letter topic, whom to call for the rule package and for the database. The legacy RWB-E1-056 job monitoring content is carried into it, including the JOB-03 entry and the MSG-P1-001 waiting state.
9. **Rollout.** The flag `rwb.case.allocation` is created off, switched on in DEV, then SIT, then UAT, then PROD, each step after the alerts are proven by a forced failure in that environment; the legacy flag name `rwb.p3.allocation` is retired.
10. **Rollback.** Turn the flag off: DailyCaseRun stops and cases stay NEW, as in the legacy behaviour. The Schedule is paused, not deleted, so the run can be resumed without a deployment.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| D1 | The worker cannot reach the Temporal frontend | The pod fails readiness and is restarted; runs stay on the queue and are not lost | None | AC1 |
| D2 | The schedule is missing after a deployment | The deployment fails its post-deploy check; an alert fires; the schedule is recreated idempotently | None | AC2 |
| D3 | A message fails three retries | It lands on the dead-letter topic and the alert fires with the case number | None | AC3 |
| D4 | The dead-letter topic has messages | The alert fires; the runbook re-drive step is used after the fix | None | AC3, AC4 |
| D5 | The connection pool or the login secret is unavailable | The pod does not start; the pre-deploy check stops the release | None | AC1 |
| D6 | `NoPackageInForce` is raised by the activity | The run stops at once and the alert fires; the last good model is kept | MSG-P3-027 | AC4 |
| D7 | The run has not finished by the deadline | The alert fires with the business date and the cases still NEW | MSG-P1-001 where the cause is a late batch | AC4 |
| D8 | The flag is switched off during a run | The run in flight completes; no new run starts | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the platform pieces of wave 0, the service template chart, the contract of RWB-P3-E1020-CON and the naming of rwb-case; no engine code |
| Negotiable | Replica counts, resource sizes and alert thresholds are values; the schedule, the topic names, the metric names and the runbook steps are fixed |
| Valuable | Turns a person-read job monitor into an alarm that names the run, and removes the shared Quartz dependency from the morning chain |
| Estimable | One chart, one schedule registration, six topics, one dashboard, six alerts, one runbook |
| Small | Two weeks or less including the environment rollout |
| Testable | Five criteria, each with an NFR-level test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the allocation worker and the DailyCaseRun schedule

  Background:
    Given the rwb-case service chart of the template and the golden pipeline
    Given namespace rwb-recovery, task queue rwb-case and topic rwb.case.events.v1

  Scenario: AC1 The Helm chart and values deploy the allocation worker (new, D-RCV-60)
    Given the chart values of rwb-case for the environment
    When the release is installed in that environment
    Then the worker deployment polls only task queue rwb-case in namespace rwb-recovery and runs under the rwb-case login taken from a Key Vault reference
    Then the deployment sets resource requests and limits, a readiness probe, a liveness probe, a pod disruption budget and a horizontal autoscaler bound to the task-queue backlog
    Then the replica bounds, the node pool, the connection pool size and the closed-history archive are chart values, and SIT sizes them
    Then the worker publishes its build ID for worker versioning and reads its payload codec keys from Key Vault
    Then the pre-deploy job applies the rwb-case Flyway sequence and fails the release if the schema grant reaches any schema other than rwb_case
    Then the deployment exports traces and metrics through OpenTelemetry and logs without personal data

  Scenario: AC2 The DailyCaseRun schedule is registered and is idempotent (new, D-RCV-60)
    Given the deployment of the worker has completed
    When the post-deploy check runs twice
    Then exactly one DailyCaseRun Schedule exists for rwb-case, with overlap policy SKIP, a catch-up window and the business date as input
    Then the JOB-06 rebalancing Schedule at 06:30 Asia/Bangkok is registered on the same queue
    Then a second deployment does not create a duplicate schedule and does not reset the last run
    Then an `AceDataReady` event for the same business date starts nothing new while the run for that date exists

  Scenario: AC3 The topic, the retry topics and the dead-letter topic are provisioned (new, D-RCV-60)
    Given the topic definitions of the service
    When the topic provisioning runs
    Then rwb.case.events.v1 exists with 12 partitions, replication factor 3, 7-day retention, key caseId, CloudEvents binary mode, and rwb.case.events.v1.retry.1m, rwb.case.events.v1.retry.10m, rwb.case.events.v1.retry.1h and rwb.case.events.v1.dlt exist with the same settings
    Then the ACLs let rwb-case produce on its topic and on rwb.decision-record.v1 and let the documented consumers read, and let no other principal write
    Then a message that fails three retries lands on the dead-letter topic and no message is lost
    Then the consumer side dedupes through its inbox table and a duplicate delivery changes nothing

  Scenario: AC4 The allocation metrics and alerts are live (new, D-RCV-60)
    Given the dashboards and the alert rules of the service
    When the morning run completes, and when a run is forced to fail
    Then the dashboard shows cases read, assigned, overflow, exception, failed and skipped for the business date, the run duration and the last successful run
    Then an alert fires when no run has succeeded for the current business date by the agreed deadline, when any case ends FAILED_LOG, when the dead-letter topic is not empty, when NoPackageInForce is raised, and when the run is stuck past the agreed window
    Then every alert names the service, the environment, the business date and the run, and links to the runbook
    Then no metric, log line or trace attribute carries personal data

  Scenario: AC5 The runbook and the feature-flag rollout are in place (new, D-RCV-60)
    Given the runbook and the feature flag of the service
    When the release is promoted from DEV to SIT, UAT and PROD
    Then rwb.case.allocation exists in the platform flag library, off by default, and is the only switch that starts or stops DailyCaseRun
    Then each environment proves the alerts with a forced failure before the flag is switched on
    Then switching the flag off pauses the schedule, starts no new run and leaves cases NEW, and switching it on resumes the schedule without a deployment
    Then the runbook carries the JOB-03 entry and the MSG-P1-001 waiting state from legacy RWB-E1-056, and the steps to retry a business date, re-drive the dead-letter topic and check the rule model version

  Scenario: AC6 The business rules of section 8 hold in the chart, the grants, the topics and the telemetry (new, D-RCV-60)
    Given the chart values, the grants, the topic definitions and the telemetry of rwb-case
    When the release is reviewed against section 8
    Then no value that a business person may change is a constant in the chart, and the worker polls only task queue rwb-case and writes only schema rwb_case
    Then no credential is written in the repository or a values file, and the topic follows the platform standard with retries at 1 min, 10 min and 1 h and a dead-letter topic
    Then the Schedule runs with overlap policy SKIP, a duplicate AceDataReady starts nothing new, and a case stays NEW while the flag is off
    Then every alert names the run and links a runbook step, no metric, log line or trace attribute carries personal data, and JOB-03 and the legacy message identifiers stay in the runbook and dashboards

  Scenario: AC7 The provided operations answer 401, 403 and 404 (new, D-RCV-60)
    Given the provided operations of section 12
    When a call carries no valid token, a call lacks the required scope, and a call names a resource that does not exist
    Then the operation answers 401 for no valid token, 403 for a missing scope and 404 for a resource that does not exist

  Scenario: AC8 A consumed call that fails or gets no answer does not assign a case (new, D-RCV-60)
    Given a case awaiting assignment and a consumed call that the allocation run makes
    When the call fails or does not answer
    Then the case is not written as assigned and the run counts the failure in the failed figure of AC4
    Then the failure is logged without personal data

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case in a status and the status model of the service
    When a status change that the model does not allow is requested
    Then the change is refused and the case keeps its current status
    Then the refusal is logged without personal data
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No value in the chart that a business person may change: the schedule expression, the deadline, the alert thresholds, the replica bounds and the topic names are values, not constants | Principle 1; DP-06 |
| BR2 | The worker polls only its own task queue and writes only its own schema; no grant reaches another schema | DP-01; Arch v5 slide 11 |
| BR3 | Secrets come from Key Vault by reference; no credential is written in the repository or in a values file | Arch v5 slide 8 |
| BR4 | The topic follows the platform standard: 12 partitions, replication factor 3, 7-day retention, key caseId, CloudEvents binary mode, retry at 1 min, 10 min and 1 h, then the dead-letter topic with an alert | Arch v5 slide 9 |
| BR5 | The Schedule uses overlap policy SKIP and a catch-up window, and a duplicate `AceDataReady` starts nothing new | DP-10; Arch v5 slide 44 |
| BR6 | With the flag off, DailyCaseRun does not run and cases stay NEW; the schedule is paused, not deleted | Legacy `rwb.p3.allocation`; DP-06 |
| BR7 | Every alert is actionable and names the run; an alert without a runbook step is not accepted | Arch v5 slide 35; JOB-21 |
| BR8 | No personal data in metrics, logs or trace attributes: the case number is the identifier | Arch v5 slide 11; PDPA |
| BR9 | The legacy job name JOB-03 and the legacy message identifiers stay in the runbook and the dashboards after the Quartz trigger is removed | Template §R6; legacy RWB-E1-020 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Release installed | Chart and values valid, pre-deploy migration passed | Deployed, flag off |
| Deployed, flag off | Flag switched on | Alerts proven in the environment | Live, schedule active |
| Live | Flag switched off | Rollback decided | Paused, schedule paused |
| Live | Run started | Schedule fired or `AceDataReady` received | Run in progress |
| Run in progress | Run finished | Every selected case handled | Run succeeded or run failed, alert raised |

The case states are unchanged by this story; it only controls whether the run that moves them is deployed, active or paused.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DEVOPS, platform engineering | Owns the chart, the values, the pipeline, the topic provisioning and the alerts |
| RW-PLATADM, platform administrator | Starts or pauses the run and reads the run monitor (Platform administration U) |
| ACE team, DBA | Grants the schema and the login; owns the connection budget |
| Platform team, Temporal | Owns the cluster, the namespace and the task queue quota |
| Enterprise Architecture, ACE platform team | Owns the Kafka platform and the topic policy |
| The service owner (process owner for L1 18, Shared operations) | Approves the schedule, the deadline and the alert thresholds |
| Not specified in the source documents (DOR-RWB-P3-E1020-OPS-6) | Passes each REST operation of rwb-case through the rwb-access authorise check (DP-08) |

### 11. Data

| Item | Where it lives | Read or write | Note | BR Field ID |
|---|---|---|---|---|
| Chart values | Service repository | Write | Environment values per DEV, SIT, UAT, PROD | Not specified in the source documents (DOR-RWB-P3-E1020-OPS-7) |
| Schedule definition | Temporal namespace `rwb-recovery` | Write | DailyCaseRun and JOB-06 | Not specified in the source documents (DOR-RWB-P3-E1020-OPS-7) |
| Topic definitions | Kafka platform | Write | `rwb.case.events.v1` with retry and `.dlt` | Not specified in the source documents (DOR-RWB-P3-E1020-OPS-7) |
| ACLs | Kafka platform | Write | Producer and consumer principals | Not specified in the source documents (DOR-RWB-P3-E1020-OPS-7) |
| Schema and login | ACE PostgreSQL, Key Vault | Write (reference) | `rwb_case`; the login name is Not specified in the source documents (GAP-0684; ASM-1231) | Not specified in the source documents (DOR-RWB-P3-E1020-OPS-7) |
| Metrics, traces, logs | Observability platform | Write | Case number as identifier only | Not specified in the source documents (DOR-RWB-P3-E1020-OPS-7) |
| Feature flag | Platform flag library | Write | `rwb.case.allocation` | Not specified in the source documents (DOR-RWB-P3-E1020-OPS-7) |
| Runbook | Service documentation folder | Write | One page, with the JOB-03 entry | Not specified in the source documents (DOR-RWB-P3-E1020-OPS-7) |

The deployment topology of the service — how many worker replicas, whether the api and the worker share a node pool, and where the run history is archived — is Not specified in the source documents (GAP-0687; ASM-1234). The chart therefore exposes it as values with a documented default; nothing in the story fixes it.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Deployment note |
|---|---|---|---|
| GET | /api/recovery/case/v1/queues/{queueId}/cases | P3 rwb-case | Served by the api deployment behind gateway-bff; readiness probe on the health path |
| GET | /api/recovery/case/v1/me/tasks | P3 rwb-case | Served by the api deployment; the run monitor reads the run state, not this operation |

#### 12.2 REST operations consumed

| Operation | Path | Owner | Deployment note |
|---|---|---|---|
| GET | /api/recovery/decision/v1/rule-models/{n}/{v} | P7 rwb-decision | Egress through the mesh; 2 s timeout, circuit breaker, one retry |

#### 12.3 Events published

| Event name | Topic | Provisioned | Note |
|---|---|---|---|
| rwb.case.CaseAllocated.v1 | rwb.case.events.v1 | Yes | Producer ACL for rwb-case only |
| rwb.case.CaseAllocationFailed.v1 | rwb.case.events.v1 | Yes | Dead-letter alert covers the failure path |
| rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | Yes | Consumed by rwb-comms and rwb-reporting |
| rwb.case.DecisionRecorded.v1 (decision record) | rwb.decision-record.v1 | Producer grant | Collected by rwb-decision |

#### 12.4 Events consumed

| Event name | Topic | Owner | Deployment note |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | Consumer group `rwb-case`; inbox dedupe; starts DailyCaseRun |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 rwb-decision | Consumer group `rwb-case`; triggers a model refresh |

#### 12.5 Workflows and activities

| Item | Kind | Task queue | Deployment note |
|---|---|---|---|
| CaseWorkflow | Parent workflow | rwb-case | Worker versioning; build ID published |
| DailyCaseRun | Workflow started by schedule and by event | rwb-case | Registered in the namespace by the deployment; overlap policy SKIP |
| allocate | Activity | rwb-case | Heartbeat and start-to-close timeouts set in the chart values |
| transfer | Activity | rwb-case | Registered on the same queue; owned by RWB-P3-E1021-OPS |
| rebalance | Activity | rwb-case | Registered on the same queue; owned by the E1-030 deployment story |

#### 12.6 Schedules

| Schedule | Cron (Asia/Bangkok) | Overlap policy | Owner | Deployment note |
|---|---|---|---|---|
| DailyCaseRun | Created by the deployment as a value; date-based run after the business date is ready | SKIP | P3 rwb-case | The exact cadence is Not specified in the source documents (GAP-0686; ASM-1233) |
| JOB-06 rebalancing | 06:30 | SKIP | P3 rwb-case | Registered here, owned by the E1-030 deployment story |

#### 12.7 Tables owned

| Table | Schema | Owner | Deployment note |
|---|---|---|---|
| recovery_case | rwb_case | P3 rwb-case | Flyway sequence; no cross-schema grant |
| queue | rwb_case | P3 rwb-case | Reference rows loaded by the reference-data story |
| queue_member | rwb_case | P3 rwb-case | Reference rows loaded by RWB-P3-E1019-APP |
| assignment | rwb_case | P3 rwb-case | Written by the activity |
| parameter_catalog | rwb_case | P3 rwb-case | Read at start-up |
| parameter_value | rwb_case | P3 rwb-case | Read at start-up |
| lov_value | rwb_case | P3 rwb-case | Read at start-up |
| reference_row | rwb_case | P3 rwb-case | Read at start-up |
| reference_version | rwb_case | P3 rwb-case | Read at start-up |
| outbox_event | rwb_case | PLT (library object in the service schema) | Relayed by the outbox sender job |

#### 12.8 Contract fakes

| Fake | Contract | Used for |
|---|---|---|
| rwb-decision rule-model fake | GET /api/recovery/decision/v1/rule-models/{n}/{v} | A stand-in in DEV and SIT so the worker can start before rwb-decision is live |
| rwb-source-data event fake | rwb.source-data.events.v1 | Publishes `AceDataReady` to prove the run starts, and a duplicate to prove it starts nothing new |
| ACE notification path stub | ACE Common notification (INT-34) | Captures the allocation summary in DEV and SIT; ACE Common is outside the 19 services and has no ownership row |

The fake credentials use the rwb-case login (DP-02); its name is Not specified in the source documents (GAP-0684; ASM-1231).

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | Two read operations served by the api deployment; one rule-model read from rwb-decision |
| Kafka | 4 published, 2 consumed | Three events on `rwb.case.events.v1` with retry and `.dlt`; the decision record on `rwb.decision-record.v1`; consumes `AceDataReady` and `RulePackageInForce` |
| Temporal | 2 workflows, 3 activities | CaseWorkflow and DailyCaseRun on queue rwb-case; allocate, transfer, rebalance |
| File | None | No file is produced or consumed by this story |

### 13. Solution plan

**Deliverables.** Service chart and environment values; the schedule registration job; the topic and ACL definitions; the dashboard and the six alert rules; the runbook page; the feature-flag definition and the rollout record per environment.

**Pattern application**

| DP code | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Extend the service chart with the worker deployment, the autoscaler, the probes, the disruption budget and the Key Vault references.
2. Add the pre-deploy migration job and the boundary check on the schema grant.
3. Add the schedule registration as an idempotent post-deploy job for DailyCaseRun and the JOB-06 schedule.
4. Add the topic, retry and dead-letter provisioning and the ACLs to the environment pipeline.
5. Add the dashboard, the metrics and the six alert rules, each with a runbook link.
6. Write the runbook page from the legacy RWB-E1-056 monitoring content and the new run.
7. Roll the flag through DEV, SIT, UAT and PROD, forcing a failure in each environment to prove the alerts.
8. Record the rollout and the rollback rehearsal in the environment log.

**Feature flag.** `rwb.case.allocation` in the platform flag library, off by default, dated for removal once the run has been stable for a full business cycle. The legacy flag `rwb.p3.allocation` is retired.

**Done when.** The release installs in every environment from the pipeline; the schedule exists exactly once after two deployments; the topics and ACLs are as in AC3; the six alerts fire in the forced-failure test and name the run; the runbook is published and reviewed; the flag rollout record is complete.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-011 | Allocation summary, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-012 | Allocation summary, no row matched (RWB-E1-020) | {count} new cases matched no allocation row and are in the exception queue. |
| MSG-P3-013 | Decision record write failed for a case | The case was not allocated because the decision could not be recorded. It will be tried again in the next run. |
| MSG-P3-027 | A reference data or rule version load fails a check (schema, valid from in the past, duplicate key, removed product with open cases, overlap, unreachable or default row, test cases), or no version is in force for a table an engine needs (RWB-E1-073, RWB-E1-043, RWB-E1-025) | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P1-001 | The run is waiting because the ACE batch has not completed | {product} is from {date}. Today's load has not arrived. |

The alert text of each rule is written in the chart values and names the service, the environment, the business date and the run; the message identifiers above stay on the dashboard and in the runbook so the operations team sees the same wording as the screens.

### 15. Screens and states

The run monitor replaces the legacy job monitor tile of JOB-03. Its states are: Not scheduled, Scheduled, Waiting for the business date (with MSG-P1-001), Run in progress (with cases read so far), Run succeeded (with counts), Run failed (with the reason and the link to the runbook), Paused by flag. The case screens are unchanged: SCR-02 Case list and SCR-09 Exception queue read the result of the run through the gateway-bff composite route (DP-19). SCR-02 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-3546). SCR-09 states: loading, empty, error and no access are Not specified in the source documents (CG-ALL-3547).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1020-OPS-01 | AC1 | NFR | Chart install in DEV and SIT; rollout restart; a pod killed mid-run; the trace and metric export checked |
| TC-P3-E1020-OPS-02 | AC2 | NFR | Two consecutive deployments; a duplicate `AceDataReady` for the same business date; the schedule list read twice |
| TC-P3-E1020-OPS-03 | AC3 | NFR | Topic list and ACL list after provisioning; a message forced through the three retry topics into the dead-letter topic |
| TC-P3-E1020-OPS-04 | AC4 | NFR | A forced FAILED_LOG case, a forced `NoPackageInForce`, a held schedule and an empty run; each alert observed with its runbook link |
| TC-P3-E1020-OPS-05 | AC5 | NFR | Flag off, on and off again in each environment; a case left NEW after the pause; the runbook walkthrough |
| TC-P3-E1020-OPS-06 | §12 operations, events and activities | Contract | Contract test of each operation, event and activity in section 12 |
| TC-P3-E1020-OPS-07 | §12.7 tables (ASM-3438) | Boundary | Boundary values for each table of section 12.7, per ASM-3438 |
| TC-P3-E1020-OPS-08 | AC6 (§8 BR1 to BR9) | Boundary | Not specified in the source documents (NEWAC-RWB-P3-E1020-OPS-AC6) |
| TC-P3-E1020-OPS-09 | AC7 (§12 operations) | Contract | Not specified in the source documents (NEWAC-RWB-P3-E1020-OPS-AC7) |
| TC-P3-E1020-OPS-10 | AC8 (consumed call fails or does not answer) | Contract | Not specified in the source documents (NEWAC-RWB-P3-E1020-OPS-AC8) |
| TC-P3-E1020-OPS-11 | AC9 (disallowed status change refused) | Contract | Not specified in the source documents (NEWAC-RWB-P3-E1020-OPS-AC9) |

### 17. Guardrails

- **G1 No business value in the chart.** The schedule expression, the deadline, the thresholds, the replica bounds and the topic settings are values with a documented default.
- **G2 No credential in the repository.** Every secret is a Key Vault reference.
- **G3 No cross-schema grant.** The pre-deploy check fails the release if the login can read or write any schema other than `rwb_case`.
- **G4 No personal data in telemetry.** Metrics, logs and trace attributes carry the case number only.
- **G5 Every alert has a runbook step** and names the run, the environment and the business date.
- **G6 The schedule is paused, never deleted,** so a rollback needs no deployment.
- **G7 No shared Quartz table.** The legacy trigger of JOB-03 is removed; nothing in this story writes the ACE shared scheduler tables.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 18.3.2 | R-DEV-01 | TC-P3-E1020-OPS-02, TC-P3-E1020-OPS-04 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07, FEAT-CWC-09 | 18.3.2 | R-UNI-41 | TC-P3-E1020-OPS-03, TC-P3-E1020-OPS-04 |
| REQ-CWC-009 | Round robin, lowest load, named owner, cap and overflow | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-08 | 18.3.2 | R-UNI-19 | TC-P3-E1020-OPS-01, TC-P3-E1020-OPS-04 |
| REQ-CWC-016 | Every allocation logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 6.1 | R-UNI-39, R-UNI-40 | TC-P3-E1020-OPS-03, TC-P3-E1020-OPS-05 |

Legacy trace: story RWB-E1-020, job contract for JOB-03, and the job monitoring runbook of legacy RWB-E1-056, whose content is carried into the new runbook.

### 19. Out of scope

- The engine code and its unit and end-to-end tests (RWB-P3-E1020-APP).
- The contract documents themselves (RWB-P3-E1020-CON).
- The platform pieces owned once in wave 0: the chart template, the workflow kit, the Temporal cluster, the Kafka platform, the observability stack.
- The transfer and rebalancing deployments (RWB-P3-E1021-OPS and the E1-030 deployment story).
- The rule package governance and the rule promotion schedule of rwb-decision (P7).
