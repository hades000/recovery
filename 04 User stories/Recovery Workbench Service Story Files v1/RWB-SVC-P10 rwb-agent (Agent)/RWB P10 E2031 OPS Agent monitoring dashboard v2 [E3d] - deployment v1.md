# RWB-P10-E2031-OPS Agent monitoring dashboard v2 [E3d] - deployment v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2031-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP07, DP10, DP13, DP15, DP19 |
| Parallel lane | L-P10-F |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-018, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: deployment slice of RWB-E2-031 for rwb-agent and the deployment of the version 2 monitoring capability that RWB-P10-E2031-CON fixes and RWB-P10-E2031-APP builds. The release carries the api and the worker of rwb-agent on one image and one chart, with a values file per environment, the `rwb_agent` login reference, the pre-deploy migration job of the service's own Flyway sequence including the index migration of this key (DP-15), no grant on any other schema, and no lake credential, extract or data-set job anywhere. It registers the Temporal task queue `rwb-agent` in namespace `rwb-recovery` with the release build ID on the version set and KEDA on the backlog, and it registers and updates the Schedule `AgentRunDailyRollup` at 01:30 Asia/Bangkok with overlap policy SKIP, the one-business-date catch-up window, the manual start on the same workflow identity and the four steps of the contract - the daily rollup, the cost sweep, the drift check and the notice (DP-10). It provisions the topic `rwb.agent.events.v1` with its retry topic and its `.dlt` topic and verifies the consumer groups of rwb-decision, rwb-document, rwb-deviation and rwb-reporting without creating one (DP-03). It wires the reference-data read of rwb-case by contract and no literal (DP-07), publishes the read and the two baseline reads behind the gateway-bff route (DP-19), and publishes the dashboards and the alert rules for the fallback rate, the override rate, the decision-quality score, the cost, the drift, the held business date and the undelivered notice, each linked to one runbook entry, with the runbook, the rollback and the capacity plan. It deploys and watches; it changes no business behaviour and holds no business value. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **rwb-agent deployed from the service template with its api and worker deployments, its values file per environment, its `rwb_agent` login and migration job, its worker on the task queue `rwb-agent` in namespace `rwb-recovery` with KEDA on the backlog, the Schedule `AgentRunDailyRollup` registered with the daily rollup and the cost sweep at 01:30 Asia/Bangkok under overlap policy SKIP and the one-business-date catch-up window, the topic `rwb.agent.events.v1` with its retry and `.dlt` topics and the consume rights of its four consumers, the reference-data read wired by contract, the read published behind the gateway-bff route, the probes, the dashboards and the alert rules for the fallback rate, the override rate, the decision-quality score, the cost, the drift, a held business date and an undelivered notice, the secrets and the single egress to the model gateway of the run path, the runbook, the rollback and the capacity plan**, so that **the daily agent figures, the drift and cost alerts and the published measures are produced, watched and repeatable in every environment, and an on-call operator can see and act on a Schedule that did not fire, a held business date, a drift alert whose notice never left and a worker backlog without reading code, and without a lake file, a lake credential or a lake job that no longer exists**.

### 2. Business rationale

The legacy key depends on a Quartz chain, the shared job table with its admin read, a data lake table, a Power BI refresh and an in-process notification call. In the target a service is a Helm release built by one pipeline with its own schema, login, topic, queue and Schedules (DP-02, DP-10, DP-15); the reporting figures come from events into rwb-reporting; and the notice leaves through rwb-comms with the retry of the outbox. Deployment is therefore part of the capability:

- Without the registered Schedule there is no daily rollup, no cost sweep and no drift check for a business date, and a missing date is invisible on the dashboard.
- Without the worker on its own queue and in its own namespace the four steps never run, and the run record that a reader trusts shows nothing.
- Without the topic, its retry and `.dlt` topics and the relay, rwb-reporting has no feed, the published measures fall behind the runs, and the dashboard and the steering measures disagree.
- Without the alert on the undelivered notice, an `agent_alert` row with `sent_at` empty looks like a delivered alert and a drift or cost breach is never seen by its holders.
- Without the route publication, the read is unreachable from a screen and the figures exist but nobody sees them.

This story makes the capability observable and repeatable so the app slice can be proven in SIT and the on-call rota can operate it. It deploys and watches; it changes no business behaviour and holds no business value.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), and the Temporal workflow kit with namespace `rwb-recovery` is in place (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions a topic with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The ACE database administrator has created schema `rwb_agent` and the login, with rights on `rwb_agent` only and no grant on any other schema (DP-02).
- The achievement of the monitoring baseline release of RWB-P10-E1063-OPS is known: the `agent_alert` table, the Schedule `AgentRunDailyRollup` and the topic already exist in the environments this release promotes into, and this release updates them rather than creating them again.
- The platform error envelope, the message catalogue and the alert routing are in force, so an alert can carry a message ID.
- The contract baseline of RWB-P10-E2031-CON is published: the version 2 read, the element, the restated reads, the boundary, the Schedule contract and the four fakes.
- The rwb-reporting release of RWB-P9-E1063-APP is known, because it owns the consumer group of `rwb.agent.events.v1` and the measure projection this deployment feeds.
- The rwb-decision contract of RWB-P7-E2005-CON, the reference-data contract of RWB-P3-E1043-CON and the notification path of rwb-comms are available for the boundaries the release configures.
- The three environments DEV, SIT and UAT exist with the scope of the environment list, and the egress policy of the tenant allows the private endpoint of the model gateway for the run path of the service.
- The names of the per-service login and of the route path are Not specified in the source documents (GAP-0631; ASM-0966; ASM-0967); the chart references both and holds neither as a value.
- No build dependency: this story is Day 1 by rule (§R5.7). The release date 31 December 2026 is tentative and is copied unchanged.

### 4. Flow

1. The pipeline builds one image and one chart version from one commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys the api deployment and the worker deployment with the `rwb_agent` login reference, the pre-deploy migration job of the service's Flyway sequence, the config map, the secret references, the probes and the Schedule registration hook.
3. The migration job runs the sequence in schema `rwb_agent` in order, including the index migration of this key, before the rollout is marked ready; the sequence is forward only.
4. The provisioning step verifies the topic `rwb.agent.events.v1` with its retry topic and its `.dlt` topic, the publish right of rwb-agent and the consume rights of the four consumers, and registers the Temporal task queue `rwb-agent` in namespace `rwb-recovery`.
5. The Schedule registration step creates or updates `AgentRunDailyRollup` at 01:30 Asia/Bangkok for the previous business date with overlap policy SKIP and the one-business-date catch-up window, checks the four steps of the contract on the run, and checks that a manual start for a business date joins the same workflow identity (DP-10; AC3).
6. The configuration step wires the reference-data read of rwb-case for LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE, and the two range limits of the screen as values of the environment; no list value and no limit is written into a chart template (DP-07).
7. The feature switch of the legacy flag of the key is wired to the platform flag library, off in DEV and on in SIT and UAT only after the smoke read answers.
8. The egress step declares the single outbound dependency of the release - the private endpoint of the model gateway used by the run path - and no other; a lake egress, an extract mount and a data-set job are absent and a release that carries one fails the guard.
9. The dashboards are published: rollup runs started and finished by state, held dates, drift rows raised and sent, `sent_at` empty older than the agreed window, feed lag on the topic, fallback rate, override rate, decision-quality score and cost per agent and segment, worker backlog and refused reads.
10. The alerts are wired to MSG-P10-006, to the held-date check, to the undelivered notice, to the failed migration and to the route being unavailable, each linked to one runbook entry.
11. The route publication step registers the version 2 read and the two baseline reads behind the gateway-bff pass-through route, one hop, and checks the health of the route target (DP-19).
12. A smoke step starts the rollup for a synthetic business date in a test namespace against the four fakes, reads the element through the route, and checks the run record, the alert rows and the probes (AC6, AC7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails, including the index migration of this key | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1, AC5 |
| X2 | The readiness probe fails after the start-up window | The pod is removed from the service and the pipeline marks the release failed | None | AC1 |
| X3 | The task queue is not registered, or the worker build ID is not on the version set | The release fails; a business date would otherwise never roll up | None | AC2 |
| X4 | The Schedule registration is rejected by the namespace, or the Schedule did not fire for a business date | The release fails on the rejection; a missing date is raised by the Schedule-not-fired alert and the date is started by hand on the same workflow identity | None | AC3 |
| X5 | The topic, its retry topic, its `.dlt` topic or a consume right is missing | The release fails on the provisioning check; a relay that cannot publish is visible on the feed-lag panel | None | AC4 |
| X6 | A business date is held by the count check | The held-date alert carries the business date and the previous published date, and opens a ticket for the data steward | MSG-P1-001 (banner) | AC7 |
| X7 | The notification path is unavailable and an alert row keeps `sent_at` empty | The undelivered-notice alert fires after the agreed window and carries the alert type, the agent, the date and the runbook entry of the retry path; the row is sent when the relay succeeds | MSG-P10-006 | AC7 |
| X8 | The route publication fails or the route target is not healthy | The release fails and the read stays unreachable; no partial route is left | None | AC7 |
| X9 | A lake credential, an extract file or a data-set job is found in the chart, the values or the egress rules | The pipeline fails the release on the guard | None | AC1, AC6 |
| X10 | A role without the right of the read calls the read | The refused-read count rises on the dashboard with its message ID and never pages the on-call rota | MSG-P4-002 | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the published contracts; no application code is built here |
| Negotiable | Replica counts, resource sizes, alert thresholds, probe timings and the cluster topology are environment values, not story decisions |
| Valuable | Makes the daily rollup, the cost sweep, the drift check, the published measures and the read deployable, observable and repeatable, and keeps every lake artefact out of the release |
| Estimable | One chart with three values files, one migration job, two deployments, two probes, one provisioning check, one Schedule registration, one egress declaration, one route publication, nine dashboard panels, five alert rules and seven runbook entries |
| Small | Fits one sprint with the runbook and the capacity plan |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the queue is registered, the Schedule fires once, the topic and its rights exist, the alerts fire on a synthetic condition, the route answers within 2 s |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-agent agent monitoring capability version 2

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart renders the api and the worker from one artefact per environment with no lake artefact (new, D-RCV-60)
    Given the rwb-agent Helm chart and its values files for DEV, SIT and UAT
    When the chart is rendered for each environment
    Then each render succeeds with the chart version and the image digest pinned, and no value is rebuilt between environments
    Then the release declares the api deployment, the worker deployment, the pre-deploy migration job and the platform secret references, and each environment differs only in the values file
    Then no replica count, resource size, probe timing, cadence or list value is hard-coded in the template
    Then the release declares no lake credential, no extract file, no outbound mount, no data-set job and no lake egress rule

  Scenario: AC2 The task queue and the worker are registered in the namespace and scale on backlog (new, D-RCV-60)
    Given the provisioning step and the worker deployment
    When a synthetic backlog is queued on rwb-agent in namespace rwb-recovery
    Then the task queue rwb-agent is registered in namespace rwb-recovery and the worker polls only its own queue
    Then the release build ID is on the version set and the worker is scaled by KEDA on the task-queue backlog with a minimum and a maximum from the values file
    Then AgentRunDailyRollupWorkflow, aggregateAgentRuns, raiseCostAlerts, agentDrift and dispatchAgentAlerts are registered by the same worker
    Then no worker of this release polls a task queue of another service

  Scenario: AC3 The Schedule for the daily rollup and the cost sweep is registered and fires once per business date (new, D-RCV-60)
    Given the Schedule registration step
    When it runs
    Then AgentRunDailyRollup is registered in namespace rwb-recovery on the task queue rwb-agent at 01:30 Asia/Bangkok for the previous business date with overlap policy SKIP and the one-business-date catch-up window
    Then the registered run executes the daily rollup, the cost sweep, the drift check and the notice as the four steps of the contract
    Then a synthetic business date starts one run through the Schedule and one through a manual start on the same workflow identity, and only one run exists for that date
    Then a rerun for a complete date replaces the rows of that date, raises no second alert and sends no second notice
    Then the run record carries the state COMPLETE, HELD or FAILED and the counts of the date
    Then no second Schedule is registered for the cost sweep and the legacy job table and its admin read are used by nothing in the release

  Scenario: AC4 The topic, its retry and dead-letter topics and the consume rights are in place (new, D-RCV-60)
    Given the provisioning step
    When the release is promoted to SIT
    Then the topic rwb.agent.events.v1 exists with its retry topic and its .dlt topic, the publish right of rwb-agent and the relay interval of the outbox
    Then the consume rights of rwb-decision, rwb-document, rwb-deviation and rwb-reporting on the topic are verified
    Then no consumer group is created inside rwb-agent by this release, and the four consumer groups belong to their own releases
    Then the feed lag of the topic is on the dashboard and a message that lands in .dlt raises its alert with the message type and its registry subject

  Scenario: AC5 The schema, the login and the migration job are correct and forward only (new, D-RCV-60)
    Given the rwb_agent schema and the per-service login
    When the migration job runs as a pre-deploy step
    Then the job runs the service's Flyway sequence in schema rwb_agent in order, including the index migration of this key, before the rollout is marked ready
    Then the login holds rights on rwb_agent only, and no grant on any other schema exists
    Then a failed migration blocks the rollout and the release, and the sequence is forward only with no down-migration
    Then no table, column, lake table or extract table is created by the migration job beyond the indexes of this key

  Scenario: AC6 Secrets, egress and the reference-data wiring are by reference (new, D-RCV-60)
    Given the values files, the config map and the egress declaration of the release
    When the release is rendered and started
    Then every secret - the login, the Kafka client credential and the Temporal mTLS material - is a reference to the platform secret store and no secret value appears in the chart, the values, a dashboard or the runbook
    Then the single outbound dependency declared for the release is the private endpoint of the model gateway used by the run path, and no lake endpoint, no extract target and no file share is declared
    Then LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE are read through the rwb-case reference-data contract at run time and appear in no values file
    Then the two range limits of the screen are values of the environment and appear in no chart template
    Then the legacy flag of the key is off in DEV and on in SIT and UAT only after the smoke read answers

  Scenario: AC7 The probes, the dashboards and the alerts cover the figures and the failure paths (new, D-RCV-60)
    Given a running pod of the api and of the worker, the published dashboards and the alert rules
    When the readiness probe is called before the migration job and the start-up window complete, and after them
    Then the pod is not ready before, both probes answer healthy after, and neither writes to the database
    Then the dashboards carry the rollup runs by state, the held dates, the drift and cost rows raised and sent, the age of a row whose sent_at is empty, the feed lag, the fallback rate, the override rate, the decision-quality score, the cost per agent and segment, the worker backlog and the refused reads
    Then the smoke read of the version 2 read for a synthetic business date answers the element within the 2 s budget against the four fakes
    Then a synthetic drift row raises the MSG-P10-006 alert with the agent, the segment, the two acceptance figures and the date of the legacy text
    Then the held-date alert carries the business date and the previous published date with the stale banner, the undelivered-notice alert fires after the agreed window for a row whose sent_at stays empty, and the refused-read count carries its message and does not page the on-call rota
    Then every alert links one runbook entry with the check, the owner role and the recovery step

  Scenario: AC8 The route publication, the runbook, the rollback and the capacity plan are accepted (new, D-RCV-60)
    Given the route publication step, the runbook, the rollback plan and the capacity plan
    When the read is called through the gateway-bff route and the on-call rota walks the entries
    Then the route makes one hop to rwb-agent and returns the version 2 element and the two restated reads unchanged within the 2 s budget, with the refusal passed through
    Then no screen calls rwb-agent directly and the route is published for the three environments
    Then the rollback redeploys the previous chart version, re-registers the Schedule from the previous release and leaves the schema at its forward-only version
    Then the capacity plan states the rollup duration, the runs of a peak date, the pages served to the dashboard, the worker minimum and maximum, the connection cap of the login and the relay interval, and records no lake throughput and no extract window
    Then the route path, the deployment topology, the host, the SKU and the budget are Not specified in the source documents (GAP-0631; ASM-0967; ASM-0969)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_agent` login reference and no other service's credential | DP-02; Arch v5 slide 16 |
| BR2 | The migration of the release is a per-service Flyway sequence in schema `rwb_agent`, forward only, and it runs before the rollout is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every topic has a retry topic and a `.dlt` topic, and the relay publishes within its interval | DP-09 at the library; Arch v5 slide 11 |
| BR4 | A Temporal Schedule uses overlap policy SKIP with a catch-up window, and its workflow identity is the business date; one identity serves the daily rollup, the cost sweep, the drift check and the notice | DP-10; Arch v5 slide 44 |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, probe timings, alert thresholds, the two range limits and the cadences come from values files, and the reference lists from their contract | Template and Rules §R7.2 s17; DP-07 |
| BR6 | An alert carries a message ID where one exists, the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | A refused read is counted on the dashboard and never pages the on-call rota | MSG-P4-002 |
| BR8 | The release writes only schema `rwb_agent` and reads other services only through their contracts | DP-01 |
| BR9 | The release carries no lake credential, extract file, data-set job or lake egress rule; a chart that does fails the guard, and no data lake exists | Arch v5 slide 37; ADR-018 |
| BR10 | An alert row whose `sent_at` stays empty past the agreed window raises its own alert, so an undelivered drift or cost alert is never mistaken for a delivered one | R-UNI-33; R-UNI-35 |
| BR11 | The read and the two baseline reads are published behind the gateway-bff pass-through route, one hop, and a screen never calls rwb-agent directly | DP-19; ADR-019 |
| BR12 | The single outbound dependency of the release is the private endpoint of the model gateway used by the run path; the monitor capability itself makes no model call | TSD P10 Agent runtime v2 T5.1 INT-23; Arch v5 slide 16 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version, the worker has polled and both probes answer | Ready |
| Ready | Schedule registered | The namespace accepts the Schedule and a synthetic date fires once | Ready with the rollup live |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is on the version set | Ready |
| Ready | Migration job failed, probes failed, the Schedule rejected or the topic right missing | The schema is not at the expected version, a probe is unready, the namespace refused the Schedule or a right is absent | Failed |
| Failed | Rollback | The previous chart version is redeployed and the Schedule is re-registered from the previous release | Ready |

The states of a business date of the rollup - COMPLETE, HELD and FAILED - and the state of a drift or cost alert row belong to RWB-P10-E2031-APP and are only watched here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning check, the Schedule registration, the egress declaration, the route publication, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the Schedule registration rights |
| ACE database administrator | Owns the `rwb_agent` schema, the login, its grants and the migration job approval |
| Security administrator | Owns the egress policy to the model gateway and the secret store references |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the seven runbook entries and opens an incident when a held date, a missing date, a drift alert or an undelivered notice persists |
| RW-PLATADM | Starts or reruns the rollup for a business date in the running service, not in the cluster |
| RW-DATASTEW | Receives the held-date ticket |
| RW-COE, RW-RISK | Read the dashboard and receive the alerts; they hold no deployment right |

The per-service login name used by the chart is Not specified in the source documents (GAP-0631; ASM-0972); the chart references it through a secret reference and never a literal password.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switch, the two range limits of the screen, environment name |
| Schema | `rwb_agent`, migrated by the per-service Flyway sequence; the library objects, `agent_alert` and the indexes of this key |
| Topics | `rwb.agent.events.v1` with the retry topic and the `.dlt` topic; the relay interval of the outbox |
| Queue | Temporal task queue `rwb-agent` in namespace `rwb-recovery` |
| Schedule | `AgentRunDailyRollup` at 01:30 Asia/Bangkok with overlap policy SKIP, the one-business-date catch-up window and the four steps of the contract |
| Reference data | LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE through the reference-data contract, never as deployment values |
| Dashboard series | rollup runs by state, held dates, drift and cost rows raised and sent, age of a row with `sent_at` empty, feed lag, fallback rate, override rate, decision-quality score, cost per agent and segment, worker backlog, refused reads |
| Runbook entries | held date, missing date or Schedule not fired, drift alert without notice, feed lag or `.dlt` message, failed migration, route unavailable, model gateway egress refused |
| Secrets | The `rwb_agent` login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |
| Egress | The private endpoint of the model gateway, used by the run path only |

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class, exact probe timings), the host, the SKU and the budget of the release are Not specified in the source documents (GAP-0631; ASM-0969); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded. There is no lake path, no extract file and no data-set refresh time to document.

### 12. Contract

#### 12.1 REST operations provided

The deployment publishes the version 2 read and the two baseline reads behind the gateway-bff route, owner rwb-agent (P10), as fixed by RWB-P10-E2031-CON and baselined by RWB-P10-E1063-CON:

| Method | Path | Publication |
|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | Registered behind the gateway-bff pass-through route, one hop, with its query, its element and its four refusal codes |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | The baseline drill-down read, registered on the same route |
| GET | `/api/recovery/agent/v1/cases/{caseId}/agent-outputs` | The baseline case read, registered on the same route |

The probes are cluster-internal and are not part of the API surface. The route path is Not specified in the source documents (GAP-0631; ASM-0967).

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision (RWB-P7-E2005-CON) | The decision-quality and override read; 2 s client budget and a breaker |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | The five reference lists with their version, read at run time |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | The published measures shown beside the aggregate, checked during the smoke step |
| POST | the rwb-comms notification operation: Not specified in the source documents (GAP-0631; ASM-0961) | P6 rwb-comms | The notification path of the drift and cost alerts, with its refusal and retry path |

No parameter read is configured by this release: DP-06 is not one of the key's patterns, the cap, the alert role and the drift values are approved policy rows of `agent_policy` and the two range limits are values of the environment (BR5). No operation of rwb-integration is deployed here: the delivery beyond rwb-comms is RWB-P2-E1007-CON and belongs to the communications release.

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | The topic, its retry topic and its `.dlt` topic, the publish right of rwb-agent and the relay interval of the outbox are verified by this release; the event belongs to the run path of RWB-P10-E1058-APP and this key adds no member to it |

No lake copy and no extract event exists: the feed is this topic only.

#### 12.4 Events consumed

None by this release. The four consumer groups of `rwb.agent.events.v1` belong to rwb-decision, rwb-document, rwb-deviation and rwb-reporting and are created by their own releases; this story verifies that the consume rights exist and that the feed lag is on the dashboard, and creates no consumer group inside rwb-agent.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| AgentRunDailyRollupWorkflow | Workflow, one per business date, workflow ID = the business date | `rwb-agent` | Worker deployment with the release build ID on the version set |
| aggregateAgentRuns | Activity, the daily rollup step | `rwb-agent` | Registered by the same worker; reads the schema |
| raiseCostAlerts | Activity, the cost sweep step | `rwb-agent` | Registered by the same worker; writes the cost and reconciled figures and the COST_CAP rows |
| agentDrift | Activity, the drift step | `rwb-agent` | Registered by the same worker; writes the DRIFT rows and calls the decision-log read |
| dispatchAgentAlerts | Activity, the notice step | `rwb-agent` | Registered by the same worker; writes the notice and the outbox row |
| KEDA scaling | Worker scaler | `rwb-agent` | Scales on the task-queue backlog with a minimum and a maximum from the values file |

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| AgentRunDailyRollup, carrying the daily rollup and the cost sweep | Daily at 01:30 Asia/Bangkok for the previous business date; overlap policy SKIP; catch-up window one business date; a manual start for any business date on the same identity; the four steps of the contract | The release registers or updates the Schedule in namespace `rwb-recovery` and fails if the namespace rejects it; the name is the baseline name and no second Schedule is registered (GAP-0631; ASM-0973) | The legacy Quartz entry of JOB-15 at 01:30 with its rollup and drift steps |

The legacy job table, its admin read and its rerun operation are not deployed and are not read. A rerun for a business date is a manual start of the same workflow identity, which is what AC3 asserts (DP-10).

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| agent_alert | P10 (`rwb_agent`) | Created by the baseline migration with its unique key of agent, type, segment and date; this release writes DRIFT and COST_CAP rows into it and creates no column |
| agent_run | P10 (`rwb_agent`) | Created by the earlier P10 migrations; the index of this key is added by the migration job |
| agent_feedback | P10 (`rwb_agent`) | Created by the earlier P10 migrations; the index of this key is added by the migration job |
| agent_policy, agent_prompt, agent_sample, agent_evaluation, agent_evaluation_run | P10 (`rwb_agent`) | Created by the earlier P10 migrations; read by the steps of the release |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | Created by the same migration job; used by the relay and the notices |

The release creates no table, no lake table and no extract table: the only schema change it applies is the index migration of this key in the service's own sequence (DP-15; BR2, BR9).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-decision fake (RWB-P7-E2005-CON) | Runs in the pipeline and in the SIT smoke profile so the release can start without rwb-decision, answering the decision records of an agent version and the null page |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | Same, answering the five lists with their version and a list that is not in force |
| rwb-reporting measures fake | Same, answering the published measures for a synthetic date |
| rwb-comms notification fake | Same, with an accepted notice, the 503 of the notification-down path and an accepted notice for the data steward |
| gateway-bff route stub (RWB-PLT-N001-CON) | Same, a pass-through of one hop in front of the three reads |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided behind the route, 4 consumed | The version 2 read and the two baseline reads on `/api/recovery/agent/v1`; the decision log, the lists, the measures and the notice consumed, one hop and 2 s each |
| Kafka | 1 published, 0 consumed by this release | `rwb.agent.events.v1` with its retry and `.dlt` topics through the outbox relay; the four consumer groups are their owners' |
| Temporal | 1 workflow, 4 activities, 1 Schedule | AgentRunDailyRollupWorkflow with aggregateAgentRuns, raiseCostAlerts, agentDrift and dispatchAgentAlerts on the queue `rwb-agent`, started by AgentRunDailyRollup at 01:30, with KEDA on backlog |
| File | None | The release carries no file, no lake credential and no data-set job |

### 13. Solution plan

**Package.** The chart and the pipeline of the service; the Java module of the capability stays under `th.co.scb.ace.workbench.recovery.agent.monitor` and this story changes no line of it.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON; C RWB-P7-E2005-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-agent/` | Chart with the api deployment, the worker deployment, the service, the migration job, the config map, the secret references, the probes and the Schedule registration hook |
| `helm/rwb-agent/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switch, the two range limits, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning check | `rwb.agent.events.v1` with its retry and `.dlt` topics, the publish right and the four consume rights; task queue `rwb-agent` in namespace `rwb-recovery` |
| Schedule registration | `AgentRunDailyRollup` at 01:30 Asia/Bangkok with overlap policy SKIP, the catch-up window and the four steps; idempotent create or update |
| Egress declaration | The private endpoint of the model gateway for the run path, and nothing else |
| Route publication | The version 2 read and the two baseline reads registered behind the gateway-bff pass-through route, one hop |
| KEDA scaling | Worker scaled on the task-queue backlog with a minimum and a maximum from the values file |
| Dashboards | Nine panels: rollup runs by state, held dates, drift and cost rows raised and sent, sent-empty age, feed lag, fallback rate, override rate, decision-quality score and cost per agent and segment, worker backlog, refused reads |
| Alerts | Five rules: MSG-P10-006, held date, undelivered notice, feed lag or `.dlt` message, route or migration failure |
| Runbook | Seven entries: held date, missing date or Schedule not fired, drift alert without notice, feed lag or `.dlt` message, failed migration, route unavailable, model gateway egress refused |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the worker has polled, the relay is running and the last reference-data read answered; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database. Exact paths and timings are values.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_agent` with the service login as a pre-deploy job with a backoff limit; the baseline migrations and the index migration of this key apply in order, a failed job blocks the rollout and the release, and the sequence is forward only (DP-15).

**Alert mapping of the key.**

| Message ID or check | Condition | Alert | Route |
|---|---|---|---|
| MSG-P10-006 | Acceptance of a segment falls by 10 points or more against the week before | Drift alert with the agent, the segment, the two acceptance figures and the date of the legacy text | Platform on-call and the alert role, no page outside the window |
| None (held date) | The count check of a date fails and the date is HELD | Held-date alert with the business date and the previous published date, and the stale banner | Data steward, ticket |
| None (undelivered notice) | An `agent_alert` row keeps `sent_at` empty past the agreed window | Undelivered-notice alert with the alert type, the agent and the date, and the retry runbook entry | Platform on-call, ticket |
| None (feed) | The feed lag passes its threshold, or a message lands in `.dlt` | Feed alert with the date, the lag and the message type | Platform on-call, page |
| MSG-P4-002 | A read without the right of the read | Refused-read count on the dashboard | No page |
| None (cost) | The cost of an agent on a business date is above the approved cap | Cost alert with the agent, the amount, the date and the limit | Platform on-call and the alert role |

**Capacity.** The plan states, per environment, the rollup duration for a peak business date and the duration of the drift step over the two 7-day windows, the runs of that date, the pages served to the dashboard, the worker minimum and maximum, the connection cap of the login and the relay interval. The target is the legacy measure: the aggregate and the drift verdict of a business date available before the officers start, and the alert sent within 15 minutes of the end of the rollup (DL11). No lake throughput and no extract window appear in the plan, because both are removed.

**Rollback.** The previous chart version is redeployed and the Schedule is re-registered from the previous release; the Flyway sequence is forward only, so the indexes and `agent_alert` stay and no down-migration is run; the topic, its retry and `.dlt` topics and the publish right are left in place, because removing them would break the feed to rwb-reporting; a rollback is rehearsed in SIT before UAT.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer, the queue, the topic and the four consume rights are verified by a test, KEDA scales on backlog, the Schedule is registered and fires once per business date with the four steps, the five alert rules fire on synthetic conditions including the undelivered notice, the route answers within 2 s, the capacity plan is reviewed, the rollback is rehearsed and the seven runbook entries are accepted by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-006 | Acceptance of a segment falls by 10 points or more | {agent} acceptance for {segment} fell from {from} to {to} percent in the week to {date}. |
| MSG-P1-001 | The dashboard shows the previous day after a held date | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A read without the right of the read | You cannot {action} here. Your role does not include it. |
| MSG-GEN-002 | A filter range above the limit of the read | {field} must be between {min} and {max}. |
| MSG-GEN-003 | A filter with the from date after the to date | {field} cannot be before {other}. |

The five texts are copied unchanged from RWB-E2-031; the deployment adds the alert routing and the runbook link, never a new wording, and adds no message ID. The held-date, undelivered-notice, feed, cost and route conditions keep the message IDs the legacy story gives them and none where it gives none. In MSG-P10-006 the {agent} value is "INTAKE", {segment} is "MORTGAGE/BKK", {from} is 0.8600, {to} is 0.7500 and {date} is 2026-12-14. In MSG-GEN-002 {min} is 1 and {max} is 92.

### 15. Screens and states

The deployment serves the agent monitoring dashboard of RWB-P10-E2031-APP through the gateway-bff pass-through route (DP-19) and publishes the version 2 read and the two baseline reads on it. The four states the release must keep answerable are the ones the contract fixes: loaded, empty, held business date and error. The operator-facing surfaces of this story are the pipeline run view, the release view, the nine dashboards and the runbook. SCR-46 Agent monitor belongs to the app slice and is not changed here, and the screen field list and the composite route specification belong to the app slice and the edge story. The exact path of the route is Not specified in the source documents (GAP-0631; ASM-0966).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E2031-OPS-01 | AC1, BR9 | NFR | Chart renders for DEV, SIT and UAT with the pinned digest, the login reference and the migration job; the rendered manifests carry no lake credential, extract, mount, data-set job or lake egress rule |
| TC-P10-E2031-OPS-02 | AC2, BR4 | NFR | The queue `rwb-agent` registered in `rwb-recovery`, the build ID on the version set, the five registrations of the worker, KEDA scaling on a synthetic backlog and no queue of another service polled |
| TC-P10-E2031-OPS-03 | AC3, BR4 | End to end | `AgentRunDailyRollup` at 01:30 Asia/Bangkok with SKIP and the catch-up window; one run per business date from the Schedule and from a manual start; the four steps on the run; a rerun replaces the date with no second alert; no second Schedule |
| TC-P10-E2031-OPS-04 | AC4, BR3 | NFR | The topic with its retry and `.dlt` topics, the publish right, the four consume rights, the feed lag panel and the `.dlt` alert with the message type and its registry subject |
| TC-P10-E2031-OPS-05 | AC5, BR2 | NFR | The migration job order, the forward-only sequence, the login rights on `rwb_agent` only, a failed migration blocking the rollout and no table beyond the indexes |
| TC-P10-E2031-OPS-06 | AC6, BR5, BR12 | NFR | Every secret a reference, the single egress to the model gateway, the five lists read by contract, the two range limits as values, the flag off in DEV and the absent lake egress |
| TC-P10-E2031-OPS-07 | AC7, BR6, BR7, BR10 | End to end | Probes false before the migration and true after; the nine dashboard panels; the smoke read through the route within 2 s against the four fakes; the five alert rules on synthetic conditions with one runbook entry each |
| TC-P10-E2031-OPS-08 | AC8, BR1, BR11 | NFR | The route in front of the three reads, one hop and the refusal passed through; the seven runbook entries walked; the rollback with the Schedule re-registered and the schema forward only; the capacity plan figures stated |

The eight test cases are this story's own (D-RCV-60) and test the deployment artefacts of the legacy criteria rather than the business outcomes, which are the app slice's: the legacy ids TC-E2-031-01 to TC-E2-031-08 stay with RWB-P10-E2031-APP and are not copied here. The legacy Level "System" maps to NFR for a deployment check and to End to end where the run of the Schedule and the route answer are proved.

### 17. Guardrails

- No business value in a values file: the cap, the alert role, the lists and the drift values are policy and contract values, and the two range limits are environment values that no template holds as a literal (BR5).
- No personal data in logs, dashboard series, alert payloads or the runbook: run counts, identifiers, dates, rates and durations only.
- No other service's table is read and no grant crosses a schema: the login holds rights on `rwb_agent` only (BR1, BR8).
- Every topic has a retry topic and a `.dlt` topic, and the relay publishes within its interval (BR3).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.
- No lake credential, extract file, data-set job or lake egress rule is deployed, and the guard fails a release that carries one (BR9).
- The Schedule is registered by the release and never by hand, one identity serves the rollup, the cost sweep, the drift check and the notice, and the legacy job table and its admin read are not used (BR4).
- The read and the two baseline reads are published only through the gateway-bff route, one hop, and a screen never reaches the service (BR11).
- The only outbound dependency is the private endpoint of the model gateway used by the run path, declared once and owned by the security administrator (BR12).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched (the legacy text names the data lake copy, which has no target; the copy becomes the event feed) | The topic, its retry and `.dlt` topics and the relay; the held-date alert; the reconciled figure in the capacity plan; the absent lake artefacts | TC-P10-E2031-OPS-01, TC-P10-E2031-OPS-03, TC-P10-E2031-OPS-04, TC-P10-E2031-OPS-07 |
| REQ-APD-005 | An override of a recommendation needs a coded reason, and the reason is reported monthly | The override-rate and decision-quality panels and the decision-log read the release configures | TC-P10-E2031-OPS-06, TC-P10-E2031-OPS-07 |
| D-RCV-60 DP-03 | Local decision record plus central ledger | The decision-log read configured at the boundary and the topic right of the ledger's consumer | TC-P10-E2031-OPS-04, TC-P10-E2031-OPS-06 |
| D-RCV-60 DP-07 | Reference data through the owner's contract | The five lists read by contract and the range limits as values | TC-P10-E2031-OPS-06 |
| D-RCV-60 DP-10 | Temporal Schedules replace Quartz | The Schedule registration step, the four steps and the once-per-date check | TC-P10-E2031-OPS-03 |
| D-RCV-60 DP-13 | One REST base per service | The published base `/api/recovery/agent/v1` behind the route | TC-P10-E2031-OPS-08 |
| D-RCV-60 DP-15 | Per-service Flyway and migration ownership | The migration job and the forward-only rollback | TC-P10-E2031-OPS-05, TC-P10-E2031-OPS-08 |
| D-RCV-60 DP-19 | gateway-bff composite route | The route publication and the one-hop smoke read | TC-P10-E2031-OPS-08 |
| ADR-023 | Observability per service | Nine dashboard panels, five alert rules and seven runbook entries | TC-P10-E2031-OPS-07 |
| NFR-008 | A screen responds under 2 seconds | The smoke read through the route within the 2 s budget | TC-P10-E2031-OPS-07 |

The gap GAP-0631 records the areas the sources leave open for this deployment - the route path, the login name, the topology and budget, the notice operation, the Schedule registration details and the egress detail - and each default it raises is settled by ASM-0961, ASM-0966, ASM-0967, ASM-0969 and ASM-0972 to ASM-0974.

### 19. Out of scope

- The application code of the version 2 read, the drift check, the cost reconciliation, the alerts and the screen (RWB-P10-E2031-APP).
- The contract documents and the fakes as published artefacts (RWB-P10-E2031-CON); this story deploys the test copies only.
- The agent runtime, the run path and the publication of the run event (RWB-P10-E1058-APP, RWB-P10-E1063-APP).
- The platform topic provisioning implementation, the Temporal cluster and the KEDA operator (the platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The consumer groups, the measure projections and the published measures of rwb-reporting (P9 rwb-reporting).
- The decision log, the decision-quality record and the override reason codes (P7 rwb-decision, RWB-P7-E2005-CON).
- The notification path and its template (rwb-comms), and the delivery beyond it (RWB-P2-E1007-CON).
- The right check and the refusal of a role without the right of the read (rwb-access).
- The screen field list and the composite route specification of SCR-46 (the app slice and the edge story).
- The exact deployment topology, the host, the SKU, the budget, the replica counts, the resource sizes and the probe timings (GAP-0631).
- Any lake credential, extract file, data-set job or lake refresh, of which none is deployed (BR9).
- The end-to-end run of the legacy criteria AC1 to AC7 across services (RWB-ITG-E2031-ITG).
