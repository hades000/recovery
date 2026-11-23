# RWB-P10-E1063-OPS Agent monitoring dashboard v1 [E2c] - deployment v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1063-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-063 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P10-D |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to REQ-DRI-009) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-063 for rwb-agent. This story deploys the monitoring capability: the `rwb-agent` api and worker deployments with the migration job of `agent_alert` under the per-service Flyway sequence, the Temporal worker on the task queue `rwb-agent` with the release build ID, the registration of the `AgentRunDailyRollup` Schedule at the 01:30 Asia/Bangkok time of the legacy JOB-15 agent step (DP-10), the reporting feed of `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` with its retry and `.dlt` topics (DP-09), the configuration of the cost cap and the alert role by contract (DP-06, DP-07), the feature switch of the legacy `rwb.agent.monitor` flag, the probes, the dashboards, the alerts including the notification-down path of legacy AC7, the publication of the dashboard route through gateway-bff (DP-19), the runbook, the rollback and the capacity. It deploys no lake credential, no extract file and no data-set job: the data lake is removed (DP-17), and a release that carries one fails the guard. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **rwb-agent deployed from the service template with its api and worker deployments, its `agent_alert` migration job, its probes, its Temporal worker and KEDA scaling on the `rwb-agent` task queue, the `AgentRunDailyRollup` Schedule registered in namespace `rwb-recovery` at 01:30 Asia/Bangkok with overlap policy SKIP and the one-business-date catch-up window, the reporting feed of `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` with its retry and `.dlt` topics and the outbox relay, the cost cap and alert role wired through the rwb-case parameter and reference-data contracts, the feature switch, the dashboards and the alerts that carry MSG-P10-004 and the held-date and notification-down paths, the publication of the dashboard read through the gateway-bff route, the runbook, the rollback and the capacity plan**, so that **the daily agent figures, the cost alerts and the reporting feed are produced, watched and repeatable in every environment, and an operator can see and act on a held business date, a Schedule that did not fire, an alert whose notification never left and a worker backlog without reading code or a lake file that no longer exists**.

### 2. Business rationale

The legacy story depends on a Quartz chain, the shared job table with its admin read, a data lake table, a Power BI refresh and an in-process notification call. In the target a service is a Helm release built by one pipeline with its own schema, login, topic, queue and Schedules (DP-02, DP-10, DP-15), the reporting figures come from events into rwb-reporting instead of a lake (DP-17), and the notification leaves through rwb-comms with the retry of the outbox (DP-09). Deployment is therefore part of the capability:

- Without the registered `AgentRunDailyRollup` Schedule there is no daily aggregate and no cost alert for a business date, and a missing date is invisible on the dashboard.
- Without the topic, its retry and `.dlt` topics and the outbox relay, rwb-reporting has no feed and the published measures fall behind the runs.
- Without the alert on the notification-down path of legacy AC7, an `agent_alert` row with `sent_at` empty looks like a delivered alert and the cost breach is never seen by its holders.
- Without the route publication, the dashboard read is unreachable from a screen and the figures exist but nobody sees them.

This story makes the capability observable and repeatable so the app story can be proven in SIT and the on-call rota can operate it. It deploys and watches; it changes no business behaviour and holds no business value.

### 3. Preconditions

- The service template, chart skeleton and pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), and the Temporal workflow kit with namespace `rwb-recovery` is in place (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The ACE database administrator has created schema `rwb_agent` and the login, with rights on `rwb_agent` only and no grant on any other schema (DP-02).
- The platform error envelope, the message catalogue and the alert routing are in force, so an alert can carry a message ID.
- The contract baseline of RWB-P10-E1063-CON is published: the metric read, the aggregate element, the EV-28 payload, the Schedule contract and the four fakes.
- The rwb-reporting release of RWB-P9-E1063-APP is known, because it owns the consumer group of `rwb.agent.events.v1` and the measure projection this deployment feeds.
- The rwb-comms contract of RWB-P6-E1063-APP is available for the notification path, and the rwb-case contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON are published for the cap, the alert role and the lists.
- The three environments DEV, SIT and UAT exist with the parameter scope of LOV-ENVIRONMENT.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from one commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys the api deployment and the worker deployment with the `rwb_agent` login reference, the pre-deploy migration job of `V10_006__agent_alert.sql` on the per-service Flyway sequence, and the probes; the migration job runs before the rollout is marked ready.
3. The provisioning step creates the topic `rwb.agent.events.v1` with its retry topic and its `.dlt` topic, the publish right of rwb-agent and the consume right of rwb-reporting, and registers the Temporal task queue `rwb-agent` in namespace `rwb-recovery`.
4. The Schedule registration step creates or updates `AgentRunDailyRollup` at 01:30 Asia/Bangkok with overlap policy SKIP and the one-business-date catch-up window, and checks that a manual start for a business date joins the same workflow identity (DP-10; AC2).
5. The configuration step wires `daily_cost_cap_thb` and `alert_role` through the rwb-case parameters contract and LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT through the reference-data contract; no parameter value is written into a values file (DP-06, DP-07).
6. The feature switch of the legacy `rwb.agent.monitor` flag is wired to the platform flag library, off by default in DEV and on in SIT and UAT only after the smoke read answers.
7. The dashboards are published: rollup runs started and finished by state, held dates, alert rows raised and sent, `sent_at` empty older than the agreed window, feed lag on `rwb.agent.events.v1`, agent run fallbacks and cost per agent, worker backlog, refused reads.
8. The alerts are wired to MSG-P10-004, to the held-date check, to the notification-down path of legacy AC7 and to the failed migration, each linked to one runbook entry.
9. The route publication step registers the dashboard read `GET /api/recovery/agent/v1/admin/agent-metrics` behind the gateway-bff pass-through route, one hop, and checks the health of the route target (DP-19).
10. A smoke step starts the rollup for a synthetic business date in a test namespace against the four fakes, reads the aggregate through the route, and checks the run record, the alert row and the probes (AC5, AC7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job of `V10_006__agent_alert.sql` fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod is removed from the service and the pipeline marks the release failed | None | AC1 |
| X3 | The task queue is not registered or the worker build ID is not on the version set | The release fails; a business date would otherwise never roll up | None | AC3 |
| X4 | The Schedule registration is rejected by the namespace, or the Schedule did not fire for a business date | The release fails on the rejection; a missing date is raised by the Schedule-not-fired alert and the date is started by hand on the same workflow identity | None | AC2 |
| X5 | A business date is held by the count check | The held-date alert carries the business date and the previous published date 2026-11-30, and opens a ticket for the data steward | MSG-P1-001 (banner) | AC4 |
| X6 | The reporting feed falls behind, or the `.dlt` topic receives a message | The feed-lag alert carries the date and the lag, and the `.dlt` alert carries the message type and its registry subject failure; one runbook entry each | None | AC3 |
| X7 | The notification path is unavailable and an alert row keeps `sent_at` empty | The sent-empty alert fires after the agreed window and carries MSG-P10-004 and the runbook entry of the retry path; the row is sent when the outbox relay succeeds (R-UNI-33, R-UNI-35) | MSG-P10-004 | AC6 |
| X8 | The route publication fails or the route target is not healthy | The release fails and the dashboard read stays unreachable; no partial route is left | None | AC7 |
| X9 | A lake credential, an extract file or a data-set job is found in the chart or the values | The pipeline fails the release on the DP-17 guard | None | AC1 |
| X10 | A role without the reporting read opens the dashboard | The refused-read count rises on the dashboard with MSG-P4-002 and never pages the on-call rota | MSG-P4-002 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the published contracts; no application code is built here |
| Negotiable | Replica counts, resource sizes, alert thresholds and the cluster topology are environment values, not story decisions |
| Valuable | Makes the daily aggregate, the cost alerts and the reporting feed deployable, observable and repeatable, and keeps every lake artefact out of the release |
| Estimable | One chart, one pipeline stage, one migration job, two deployments, two probes, one provisioning step, one Schedule registration, one route publication, seven dashboard panels, four alert rules and six runbook entries |
| Small | Fits one sprint with the runbook and the capacity plan |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the queue is registered, the Schedule fires, the alerts fire on a synthetic metric, the route answers within 2 s |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-agent agent monitoring capability

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart deploys the api and worker with no lake artefact (new, D-RCV-60)
    Given the rwb-agent Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the api deployment and the worker deployment, the pre-deploy migration job of V10_006__agent_alert.sql and the platform secret references
    Then the migration job runs the per-service Flyway sequence in schema rwb_agent before the rollout is marked ready
    Then the release declares no lake credential, no extract file, no outbound mount and no data-set job
    Then no replica count, resource size, Schedule cadence or parameter value is hard-coded in the template

  Scenario: AC2 The AgentRunDailyRollup Schedule is registered and fires once per business date (new, D-RCV-60)
    Given the Schedule registration step
    When it runs
    Then AgentRunDailyRollup is registered in namespace rwb-recovery on the task queue rwb-agent at 01:30 Asia/Bangkok with overlap policy SKIP and the one-business-date catch-up window
    Then a synthetic business date starts one rollup through the Schedule and one through a manual start on the same workflow identity, and only one run exists for that date
    Then a rerun for a complete date replaces the rows of that date and raises no second alert
    Then the run record carries the state COMPLETE, HELD or FAILED and the counts of the date
    Then the legacy job table and its admin read are used by nothing in the release

  Scenario: AC3 The reporting feed and the worker are in place (new, D-RCV-60)
    Given the provisioning step and the worker deployment
    When a synthetic backlog is queued on rwb-agent in namespace rwb-recovery
    Then the worker polls only its own task queue with the release build ID on the version set and KEDA scales it on backlog
    Then the topic rwb.agent.events.v1 exists with its retry topic and its .dlt topic, and the outbox relay of the release publishes EV-28 within its relay interval
    Then the consume right of rwb-reporting on the topic is granted and the feed lag is on the dashboard
    Then AgentRunDailyRollupWorkflow, aggregateAgentRuns, raiseCostAlerts and dispatchAgentAlerts are registered by the same worker
    Then no consumer group of this release reads a topic of another service

  Scenario: AC4 Configuration, reference data and the feature switch are wired by contract (new, D-RCV-60)
    Given the values files and the configuration step
    When the release is rendered and started
    Then daily_cost_cap_thb and alert_role are read through the rwb-case parameters contract and LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT through the reference-data contract
    Then no parameter value, no cap and no role literal appears in a values file or in the chart template
    Then the rwb.agent.monitor switch is off in DEV and on in SIT and UAT only after the smoke read answers, and off starts no rollup activity
    Then every secret is a reference to the platform secret store, and no secret value is in the chart, the dashboards or the runbook

  Scenario: AC5 Health, probes and the smoke read answer (new, D-RCV-60)
    Given a running pod of the api and of the worker
    When the readiness probe is called before the migration job and the start-up window complete
    Then the pod is not marked ready
    When the readiness and liveness endpoints are called after start-up
    Then both answer healthy without a database write
    Then the smoke read of GET /api/recovery/agent/v1/admin/agent-metrics for a synthetic business date answers the aggregate within the 2 s budget against the four fakes

  Scenario: AC6 Alerts and the runbook cover the cost path, the held date and the notification-down path (new, D-RCV-60)
    Given the published dashboards and the runbook
    When a synthetic rollup is replayed with a cost breach, a held date and a notification path that answers 503 at 01:40
    Then the cost alert carries MSG-P10-004 with the agent, the amount, the date and the limit of the legacy text
    Then the held-date alert carries the business date and the previous published date 2026-11-30, and the stale banner carries MSG-P1-001
    Then the sent-empty alert fires after the agreed window for the alert row whose sent_at stays empty, and the row is sent when the relay succeeds
    Then the .dlt alert fires on a refused payload with its message type and its registry subject
    Then the refused-read count carries MSG-P4-002 and does not page the on-call rota
    Then every alert links one runbook entry with the check, the owner role and the recovery step

  Scenario: AC7 The dashboard publication route is registered and answers (new, D-RCV-60)
    Given the route publication step
    When the dashboard read is called through the gateway-bff route
    Then the route makes one hop to rwb-agent and returns the answer unchanged within the 2 s budget
    Then the route target and the health check of the read are registered and answer
    Then no screen calls rwb-agent directly and the route is published for the three environments
    Then the route path is Not specified in the source documents (GAP-0618; ASM-0898)

  Scenario: AC8 The runbook, the rollback and the capacity plan are accepted (new, D-RCV-60)
    Given the runbook, the rollback plan and the capacity plan
    When the on-call rota walks the six entries and the rollback is rehearsed in SIT
    Then the rollback redeploys the previous chart version, re-registers the Schedule from the previous release and leaves the schema at its forward-only version
    Then the capacity plan states the rollup duration, the runs of a peak date, the worker minimum and maximum and the database connection cap of the login
    Then the plan records no lake throughput and no extract window, because both are removed
    Then the deployment topology detail, the host, the SKU and the budget are Not specified in the source documents (GAP-0618; ASM-0900)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_agent` login reference and no other service's credential | DP-02; Arch v5 slide 16 |
| BR2 | The migration of `agent_alert` is a per-service Flyway sequence in schema `rwb_agent` and runs before the rollout is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every topic has a retry topic and a `.dlt` topic, and the outbox relay publishes within its interval | DP-09; Arch v5 slide 11 |
| BR4 | A Temporal Schedule uses overlap policy SKIP with a catch-up window, and its workflow identity is the business date | DP-10; Arch v5 slide 44 |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, alert thresholds, cadences, the cap and the alert role come from values files and contracts | DP-06; Template and Rules §R7.2 s17 |
| BR6 | An alert carries a message ID where one exists, the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | A refused read is counted on the dashboard and never pages the on-call rota | MSG-P4-002 |
| BR8 | The release writes only schema `rwb_agent` and reads other services only through their contracts | DP-01 |
| BR9 | The release carries no lake credential, extract file or data-set job; a chart that does fails the DP-17 guard, and no data lake exists | DP-17; ADR-018; Arch v5 slide 37 |
| BR10 | An alert row whose `sent_at` stays empty past the agreed window raises its own alert, so an undelivered cost breach is never mistaken for a delivered one | R-UNI-33; R-UNI-35; legacy AC7 |
| BR11 | The dashboard read is published behind the gateway-bff pass-through route, one hop, and a screen never calls rwb-agent directly | DP-19; ADR-019 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version, the worker has polled and both probes answer | Ready |
| Ready | Schedule registered | The namespace accepts `AgentRunDailyRollup` and a synthetic date fires once | Ready with the rollup live |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is on the version set | Ready |
| Ready | Migration job failed, probes failed or the Schedule rejected | The schema is not at the expected version, a probe is unready or the namespace refused the Schedule | Failed |
| Failed | Rollback | The previous chart version is redeployed and the Schedule is re-registered from the previous release | Ready |

The states of a business date of the rollup - COMPLETE, HELD and FAILED - are the app story's and are only watched here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning and Schedule registration steps, the route publication, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the Schedule registration rights |
| ACE database administrator | Owns the `rwb_agent` schema, the login, its grants and the migration job approval |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the six runbook entries and opens an incident when a held date, a missing date or a sent-empty alert persists |
| RW-PLATADM | Starts or reruns the rollup for a business date in the running service, not in the cluster |
| RW-DATASTEW | Receives the held-date ticket |

The per-service login name used by the chart is Not specified in the source documents (GAP-0618; ASM-0899); the chart references it through a secret reference and never a literal password.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switches, environment name |
| Schema | `rwb_agent`, migrated by the per-service Flyway sequence; `agent_alert` from this release and the library objects |
| Topics | `rwb.agent.events.v1` published with the retry topic and the `.dlt` topic; the relay interval of the outbox |
| Queue | Temporal task queue `rwb-agent` in namespace `rwb-recovery` |
| Schedule | `AgentRunDailyRollup` at 01:30 Asia/Bangkok with overlap policy SKIP and the one-business-date catch-up window |
| Parameters | `agent_policy.daily_cost_cap_thb` 2,000 and `agent_policy.alert_role` "RW-COE" for INTAKE and SCREENING, read through the rwb-case parameters contract and never held as deployment values |
| Reference data | LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT through the reference-data contract |
| Dashboard series | rollup runs by state, held dates, alerts raised and sent, `sent_at` empty, feed lag, fallbacks and cost per agent, worker backlog, refused reads |
| Runbook entries | held date, missing date or Schedule not fired, feed lag or `.dlt` message, sent-empty alert, failed migration, route unavailable |
| Secrets | The `rwb_agent` login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class, exact probe timings), the host, the SKU and the budget of the release are Not specified in the source documents (GAP-0618; ASM-0900); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded. There is no lake path, no extract file and no data-set refresh time to document (DP-17; GAP-0618).

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the metric read behind gateway-bff: `GET /api/recovery/agent/v1/admin/agent-metrics` with its query and its answer, owner rwb-agent (P10), as fixed by RWB-P10-E1063-CON. The run read `GET /api/recovery/agent/v1/admin/agent-runs` and the case read `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` are served by the same release under the baseline of RWB-P10-E1058-CON and are registered on the route with the metric read. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The daily cost cap and the alert role of the approved policy row; 2 s client budget (DP-06, DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT with their version (DP-07) |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | The published measure of the dashboard read, checked during the smoke step |
| POST | the rwb-comms notification operation: Not specified in the source documents (GAP-0618; ASM-0897) | P6 rwb-comms | The notification path of the alerts, with its refusal and retry path |

No operation of rwb-integration is deployed here: the delivery beyond rwb-comms is RWB-P2-E1007-CON and belongs to the communications release.

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | The topic, its retry topic and its `.dlt` topic, the publish right of rwb-agent and the relay interval of the outbox are provisioned by this release; the event belongs to the run path of RWB-P10-E1058-APP |

No lake copy and no extract event exists: the feed is this topic only (DP-17).

#### 12.4 Events consumed

None by this release. The consumer group of `rwb.agent.events.v1` belongs to rwb-reporting and is created by its own release; this story verifies that the consume right exists and that the feed lag is on the dashboard, and creates no consumer group inside rwb-agent.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| AgentRunDailyRollupWorkflow | Workflow, one per business date, workflow ID = the business date | `rwb-agent` | Worker deployment with the release build ID on the version set |
| aggregateAgentRuns | Activity | `rwb-agent` | Registered by the same worker; reads the schema and the P3 contracts |
| raiseCostAlerts | Activity | `rwb-agent` | Registered by the same worker; writes `agent_alert` |
| dispatchAgentAlerts | Activity | `rwb-agent` | Registered by the same worker; writes the notice and the outbox row |
| KEDA scaling | Worker scaler | `rwb-agent` | Scales on the task-queue backlog with a minimum and a maximum from the values file |

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| AgentRunDailyRollup | Daily at 01:30 Asia/Bangkok for the previous business date; overlap policy SKIP; catch-up window one business date; a manual start for any business date on the same identity | The release registers or updates the Schedule in namespace `rwb-recovery` and fails if the namespace rejects it; the name is Not specified in the source documents (GAP-0618; ASM-0901) | The legacy Quartz entry of JOB-15 at 01:30 and its `agentRunDaily` step |

The legacy job table, its admin read and its rerun operation are not deployed and are not read (DP-10).

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| agent_alert | P10 (`rwb_agent`) | Created by `V10_006__agent_alert.sql` in the migration job, with its unique key |
| agent_run, agent_evaluation, agent_policy | P10 (`rwb_agent`) | Created by the earlier P10 migrations; read by the rollup and the read |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | Created by the same migration job; used by the relay and the alerts |

No `agent_run_daily` and no lake table is created by the migration job (DP-17).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-case parameters and reference-data fake (RWB-P3-E1042-CON, RWB-P3-E1043-CON) | Runs in the pipeline and in the SIT smoke profile so the release can start without rwb-case, with the cap, the role and the three lists |
| rwb-reporting measures fake (RWB-P9-E1055-CON) | Same, answering the published measure for a synthetic date |
| rwb-comms notification fake (RWB-P6-E1063-APP) | Same, with an accepted notice and the 503 of the notification-down path |
| gateway-bff route stub (RWB-PLT-N001-CON) | Same, a pass-through of one hop in front of the three reads |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided in the run path, 4 consumed | The metric read and the two baseline reads on `/api/recovery/agent/v1`; the parameters, the lists, the measures and the notice consumed, one hop and 2 s each |
| Kafka | 1 published, 0 consumed by this release | EV-28 on `rwb.agent.events.v1` with its retry and `.dlt` topics through the outbox relay; the consumer group is rwb-reporting's |
| Temporal | 1 workflow, 3 activities, 1 Schedule | AgentRunDailyRollupWorkflow with aggregateAgentRuns, raiseCostAlerts and dispatchAgentAlerts on the queue `rwb-agent`, started by AgentRunDailyRollup at 01:30, with KEDA on backlog |
| File | None | The release carries no file, no lake credential and no data-set job (DP-17) |

### 13. Solution plan

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

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-agent/` | Chart with the api deployment, the worker deployment, the service, the migration job, the config map, the secret references, the probes and the Schedule registration hook |
| `helm/rwb-agent/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switches, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | `rwb.agent.events.v1` with its retry and `.dlt` topics and the publish and consume rights; task queue `rwb-agent` in namespace `rwb-recovery` |
| Schedule registration | `AgentRunDailyRollup` at 01:30 Asia/Bangkok with overlap policy SKIP and the catch-up window; idempotent create or update |
| Route publication | The metric read and the two baseline reads registered behind the gateway-bff pass-through route, one hop |
| KEDA scaling | Worker scaled on the task-queue backlog with a minimum and a maximum from the values file |
| Dashboards | Seven panels: rollup runs by state, held dates, alerts raised and sent, sent-empty age, feed lag, fallbacks and cost per agent, refused reads |
| Alerts | Four rules: MSG-P10-004, held date, sent-empty, feed lag or `.dlt` message |
| Runbook | Six entries: held date, missing date or Schedule not fired, feed lag or `.dlt` message, sent-empty alert, failed migration, route unavailable |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the worker has polled, the relay is running and the last parameters read answered; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database. Exact paths and timings are values.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_agent` with the service login as a pre-deploy job with a backoff limit; `V10_006__agent_alert.sql` applies in order with the earlier P10 migrations, a failed job blocks the rollout and the release, and the sequence is forward only (DP-15).

**Alert mapping carried over from the legacy story.**

| Message ID or check | Condition | Alert | Route |
|---|---|---|---|
| MSG-P10-004 | The cost of an agent on a business date is above its cap | Cost alert with the agent, the amount, the date and the limit of the legacy text | Platform on-call and the alert role, no page outside the window |
| None (held date) | The count check of a date fails and the date is HELD | Held-date alert with the business date and the previous published date 2026-11-30, and the MSG-P1-001 stale banner | Data steward, ticket |
| None (sent-empty) | An `agent_alert` row keeps `sent_at` empty past the agreed window | Sent-empty alert with the agent, the type and the date, and the retry runbook entry | Platform on-call, ticket |
| None (feed) | The feed lag passes its threshold, or a message lands in `.dlt` | Feed alert with the date, the lag and the message type | Platform on-call, page |
| MSG-P4-002 | A read without the reporting right | Refused-read count on the dashboard | No page |

**Capacity.** The plan states, per environment, the rollup duration for a peak business date, the runs of that date, the pages served to the dashboard, the worker minimum and maximum, the connection cap of the login and the relay interval. The target is the legacy measure: the aggregate of a business date available before the officers start, and the cost alert sent within 15 minutes of the end of the rollup (DL11). No lake throughput and no extract window appear in the plan, because both are removed (DP-17).

**Rollback.** The previous chart version is redeployed and the Schedule is re-registered from the previous release; the Flyway sequence is forward only, so `agent_alert` stays and no down-migration is run; the topic, its retry and `.dlt` topics and the published right are left in place, because removing them would break the feedback to rwb-reporting; a rollback is rehearsed in SIT before UAT.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer, the queue, the topic and the rights are verified by a test, KEDA scales on backlog, `AgentRunDailyRollup` is registered and fires once per business date, the four alerts fire on synthetic conditions including the notification-down path, the route answers within 2 s, the capacity plan is reviewed, the rollback is rehearsed and the six runbook entries are accepted by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-004 | The cost of an agent on a business date is above its daily limit | {agent} used {amount} baht of model calls on {date}, above the daily limit of {limit} baht. |
| MSG-P1-001 | The dashboard shows the previous day after a held date | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A read without the reporting right | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-E1-063; the deployment adds the alert routing and the runbook link, never a new wording. The held-date, sent-empty and feed conditions have no message ID in the legacy story and keep none.

### 15. Screens and states

The deployment serves the agent monitoring dashboard of RWB-P10-E1063-APP through the gateway-bff pass-through route (DP-19) and publishes the metric read and the two baseline reads on it. The operator-facing surfaces of this story are the pipeline run view, the release view, the dashboards and the runbook. SCR-46 Agent monitor belongs to RWB-E2-031 and is not changed here, and the screen field list and the composite route specification belong to the edge story. The exact path of the route is Not specified in the source documents (GAP-0618; ASM-0898).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E1063-OPS-01 | AC1 | NFR | Chart renders for DEV, SIT and UAT with pinned digest, the login reference and the migration job of `V10_006__agent_alert.sql` |
| TC-P10-E1063-OPS-02 | AC1, BR9 | NFR | Rendered manifests contain no lake credential, no extract file, no outbound mount and no data-set job |
| TC-P10-E1063-OPS-03 | AC2, BR4 | End to end | `AgentRunDailyRollup` registered at 01:30 Asia/Bangkok with SKIP and the catch-up window; one run per business date from the Schedule and from a manual start; a rerun replaces the date |
| TC-P10-E1063-OPS-04 | AC3, BR3 | NFR | Backlog scales the worker, the build ID is on the version set, the four activities are registered, the topic has its retry and `.dlt` topics and the relay publishes |
| TC-P10-E1063-OPS-05 | AC4, BR5 | NFR | The cap, the role and the three lists come from the contracts; the switch off starts no rollup activity; every secret is a reference |
| TC-P10-E1063-OPS-06 | AC5, AC7 | End to end | Probes false before the migration, true after; the smoke read through the route answers the aggregate within 2 s against the four fakes |
| TC-P10-E1063-OPS-07 | AC6, BR6, BR10 | NFR | Four synthetic conditions raise the mapped alerts with the legacy text, the sent-empty path after a 503 at 01:40, and one runbook entry each |
| TC-P10-E1063-OPS-08 | AC8, BR1 | NFR | The six runbook entries walked, the rollback rehearsed with the Schedule re-registered and the schema forward only, and the capacity plan figures stated |

The eight test cases are this story's own (D-RCV-60) and test the deployment artefacts of the legacy criteria rather than the business outcomes, which are the app story's: the legacy ids TC-E1-063-01 to TC-E1-063-08 stay with RWB-P10-E1063-APP and are not copied here. The legacy Level "System" maps to NFR for a deployment check and to End to end where the run of the Schedule and the route answer are proved.

### 17. Guardrails

- No business value in a values file: the cap, the alert role, the lists and the cadence are contract and registration values, never deployment values (DP-06, DP-07).
- No personal data in logs, dashboard series, alert payloads or the runbook: run counts, IDs, dates and durations only.
- No other service's table is read and no grant crosses a schema: the login holds rights on `rwb_agent` only (DP-01, DP-02).
- Every topic has a retry topic and a `.dlt` topic, and the relay publishes within its interval (DP-09).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.
- No lake credential, extract file or data-set job is deployed, and the DP-17 guard fails a release that carries one (BR9).
- The Schedule is registered by the release and never by hand, and the legacy job table and its admin read are not used (DP-10).
- The dashboard read is published only through the gateway-bff route, one hop, and a screen never reaches the service (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched (the legacy text names the data lake copy, which DP-17 removes; the copy becomes the event feed) | The topic, its retry and `.dlt` topics and the relay; the held-date alert; the absent lake artefacts | TC-P10-E1063-OPS-02, TC-P10-E1063-OPS-03, TC-P10-E1063-OPS-07 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | Topic provisioning, the publish right, the relay interval and the feed lag panel | TC-P10-E1063-OPS-04 |
| D-RCV-60 DP-10 | Temporal Schedules replace Quartz | The Schedule registration step and the once-per-date check | TC-P10-E1063-OPS-03 |
| D-RCV-60 DP-17 | No data lake; reporting from events | The DP-17 release guard and the absent extract window in the capacity plan | TC-P10-E1063-OPS-02, TC-P10-E1063-OPS-08 |
| D-RCV-60 DP-19 | gateway-bff composite route | The route publication and the one-hop smoke read | TC-P10-E1063-OPS-06 |
| ADR-023 | Observability per service | Seven dashboard panels, four alerts and six runbook entries | TC-P10-E1063-OPS-07 |
| ADR-021 | Per-service Flyway and migration ownership | The migration job and the forward-only rollback | TC-P10-E1063-OPS-01, TC-P10-E1063-OPS-08 |
| NFR-068 | An alert reaches its holders inside the agreed window | The MSG-P10-004 route and the sent-empty alert | TC-P10-E1063-OPS-07 |

### 19. Out of scope

- The application code of the aggregate, the count check, the alerts and the read (RWB-P10-E1063-APP).
- The contract documents and the fakes as published artefacts (RWB-P10-E1063-CON); this story deploys the test copies only.
- The agent runtime, the run path and the publication of EV-28 in the application (RWB-P10-E1058-APP).
- The platform topic provisioning implementation, the Temporal cluster and the KEDA operator (the platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The consumer group, the measure projection and the published measures of rwb-reporting (RWB-P9-E1063-APP, the reporting slice of this key).
- The notification path and its template (RWB-P6-E1063-APP), and the delivery beyond it (RWB-P2-E1007-CON).
- The right check and the refusal of a role without the reporting read (RWB-P4-E1063-APP).
- The screen field list and the composite route specification of SCR-46 and of the dashboard screen (RWB-E2-031 and the edge story).
- The exact deployment topology, the host, the SKU, the budget, the replica counts, the resource sizes and the probe timings (GAP-0618).
- Any lake credential, extract file, data-set job or lake refresh, which DP-17 removes (GAP-0618).
- The end-to-end run of the legacy criteria AC1 to AC7 across services (RWB-ITG-E1063-ITG).
