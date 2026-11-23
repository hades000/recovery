# RWB-P10-E2028-OPS Case intake agent live at L1 [E3a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2028-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP07, DP09, DP10, DP13, DP15, DP19 |
| Parallel lane | L-P10-E |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: deployment slice of RWB-E2-028 for rwb-agent, split from the legacy key. This story deploys the L1 intake capability and builds no behaviour: the `rwb-agent` api deployment and worker deployment from one chart with one values file per environment, the pre-deploy migration job of `V10_008__agent_feedback.sql` in the service's own Flyway sequence on the `rwb_agent` login and schema (DP-15), the Temporal worker on the task queue `rwb-agent` in namespace `rwb-recovery` with the release build ID on the version set, the registration of the event-started `AgentRunWorkflow` with no Schedule for a cadence (DP-10), the topic `rwb.agent.events.v1` with its retry and `.dlt` topics and the consumer groups of its consumers (DP-09), the rights of the `rwb.decision-record.v1` record (DP-03), the reference-data and freshness reads wired by contract (DP-07), the feature switch of the legacy `rwb.agent.intake-l1` flag, the secrets and the egress, the probes and the KEDA scaling, the dashboards and the alerts for the L1 acceptance and override rates, the publication of the two operations behind the gateway-bff route (DP-19), the runbook, the rollback and the capacity plan. It deploys no Schedule and no job table, because the run is event-started. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **rwb-agent deployed from the service template with its api and worker deployments, its `agent_feedback` migration job on the `rwb_agent` login and schema, its probes, its Temporal worker and KEDA scaling on the `rwb-agent` task queue in namespace `rwb-recovery`, the event-started `AgentRunWorkflow` registered with no Schedule for a cadence, the topic `rwb.agent.events.v1` with its retry and `.dlt` topics and its consumer groups, the rights of the decision-record feed, the reference-data and freshness reads wired by contract, the feature switch, the secrets and egress, the dashboards and alerts that carry the L1 acceptance and override rates, the publication of the two operations behind the gateway-bff route, the runbook, the rollback and the capacity plan**, so that **the L1 intake capability is produced, watched and repeatable in every environment, and an operator can see and act on a fallen acceptance rate, a rising override rate, a `.dlt` message, a worker backlog and a failed migration without reading code**.

### 2. Business rationale

The legacy story depends on a scheduler chain, a shared job table, an in-process mode loader and a panel that called the service directly. In the target a service is a Helm release built by one pipeline with its own schema, login, topic and queue (DP-02, DP-09, DP-10, DP-15), the panel is reached only through the gateway-bff route (DP-19), and the decision record leaves through the local library and the shared record topic (DP-03). Deployment is therefore part of the capability:

- Without the migration job on the `rwb_agent` login there is no `agent_feedback` table, and a verdict has nowhere to be stored or counted.
- Without the worker on `rwb-agent` in namespace `rwb-recovery` and without the event-started registration, a new case starts no run and the panel has nothing to show.
- Without the topic, its retry and `.dlt` topics and the rights of its consumers, the monitor and the reporting projections have no feed and the acceptance rate of a segment lags a day behind.
- Without the alerts on the acceptance and override rates, a segment that should drop back to shadow keeps being served at L1 and nobody sees it.
- Without the route publication, the two operations exist but no screen can reach them.

This story makes the capability observable and repeatable so the app story can be proven in SIT and the on-call rota can operate it. It deploys and watches; it changes no business behaviour and holds no business value.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), and the Temporal workflow kit with namespace `rwb-recovery` is in place (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The ACE database administrator has created schema `rwb_agent` and its login, with rights on `rwb_agent` only and no grant on any other schema (DP-02).
- The platform error envelope, the message catalogue and the alert routing are in force, so an alert carries a message ID where one exists.
- The contract baseline of RWB-P10-E2028-CON is published: the two operations, the answer and request members, the eligibility answer, the record mapping, the two events, the registration and the four fakes.
- The reference-data contract of RWB-P3-E1043-CON, the case record contract of RWB-P3-E1035-CON, the decision-log entry read of RWB-P7-E1027-CON and the freshness read of rwb-source-data are published, so the release can start against their contracts and their fakes.
- The monitor read of RWB-P10-E2031-APP is known, because it counts the acceptance and override rates this release alerts on.
- The three environments DEV, SIT and UAT exist with the parameter scope of LOV-ENVIRONMENT.
- The per-service login name the chart references is Not specified in the source documents (GAP-0624; ASM-0916); the chart references it through a secret and never a literal.
- No build dependency: this story is Day 1 by rule (§R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from one commit, runs the unit, component and contract tests, scans the image and its dependencies, and publishes the chart.
2. The chart deploys the api deployment and the worker deployment with the `rwb_agent` login reference and the platform secret references, and the pre-deploy migration job that runs the per-service Flyway sequence and applies `V10_008__agent_feedback.sql` before the rollout is marked ready (DP-15; AC1, AC2).
3. The provisioning step registers the Temporal task queue `rwb-agent` in namespace `rwb-recovery`, checks that the worker polls only that queue with the release build ID on the version set, and sets the KEDA minimum and maximum from the values file (DP-10; AC3).
4. The registration step registers the event-started `AgentRunWorkflow` with `ResolveIntakeMode` and `RecordIntakeFeedback`, subscribes it to `rwb.case.CaseCreated.v1` through the service's own consumer group, and asserts that no Schedule exists for the capability, because a run starts from an event and a verdict from a person (DP-10; AC4).
5. The provisioning step creates or verifies the topic `rwb.agent.events.v1` with its retry topic and its `.dlt` topic, the publish right of rwb-agent, the publish right of the decision-record library on `rwb.decision-record.v1`, the consume right of rwb-agent on `rwb.case.events.v1`, and the consume rights of the four consumers of the agent topic on it, each of which belongs to its own release (DP-03, DP-09; AC5).
6. The configuration step wires the seven lists through the reference-data contract and the business date through the freshness read; no list value and no policy value is written into a values file (DP-07; AC6).
7. The secret and egress step binds the database credential, the Kafka client credential and the Temporal mTLS material from the platform secret store, and opens egress only to the database, the Kafka brokers, the Temporal frontend, the gateway-bff route and the model endpoint the agent platform calls (AC6).
8. The feature switch of the legacy `rwb.agent.intake-l1` flag is wired to the platform flag library: off by default in DEV and outside the L1 segment, on in SIT and UAT only after the smoke read answers (§R3 default ruling: feature flags to the platform library; BR12).
9. The dashboards are published: runs started, completed and failed by mode, L1 acceptance rate and override rate by segment and business date, fallback rate, tool read failures, `.dlt` messages, feed lag, worker backlog, refused reads and the migration state (AC8).
10. The alerts are wired to the acceptance rate below its floor, the override rate above its ceiling, the `.dlt` route, the worker backlog, the failed migration and the stale business date, each linked to one runbook entry (AC8).
11. The route publication step registers the two operations behind the gateway-bff pass-through route, one hop, and checks the health of the route target (DP-19; AC9).
12. A smoke step starts one run for a synthetic case in a test namespace against the four fakes, reads the answer through the route, records a verdict, and checks the feedback row, the record, the two events at the outbox, the dashboards and the probes (AC7, AC8).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job of `V10_008__agent_feedback.sql` fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC2 |
| X2 | The readiness probe fails after the start-up window | The pod is removed from the service and the pipeline marks the release failed | None | AC7 |
| X3 | The task queue is not registered, or the worker build ID is not on the version set | The release fails; otherwise a new case would start no run | None | AC3 |
| X4 | A Schedule for the capability is found in the namespace | The pipeline fails the release, because the run is event-started and no cadence belongs to it | None | AC4 |
| X5 | The topic or one of its retry and `.dlt` topics is missing, or a consumer right is absent | The release fails on the provisioning check; a missing `.dlt` is escalated before the first run | None | AC5 |
| X6 | The `rwb_agent` login holds a grant on another schema | The release fails the grant check | None | AC2, AC6 |
| X7 | The acceptance rate of an L1 segment falls below its floor, or the override rate rises above its ceiling | The acceptance or override alert carries the segment, the business date, the rate and the review action | None | AC8 |
| X8 | A message lands in the `.dlt` topic of the agent topic | The `.dlt` alert carries the message type and its registry subject, and one runbook entry opens | None | AC5, AC8 |
| X9 | The business date is stale against the runs of the day | The stale-date alert carries the business date and the data date, and the panel shows MSG-P1-001 | MSG-P1-001 | AC8 |
| X10 | The route publication fails or the route target is not healthy | The release fails and the panel stays unreachable; no partial route is left | None | AC9 |
| X11 | A secret value is found in a values file, a chart template, a dashboard or the runbook | The pipeline fails the release on the secret scan | None | AC6 |
| X12 | A role without the Case record right opens the panel | The refused-read count rises on the dashboard with MSG-P4-002 and never pages the on-call rota | MSG-P4-002 | AC8 |

X1 to X12 are the deployment failures of this capability; none is a legacy exception path, because the legacy story carried no chart, no queue, no topic and no alert rule of its own. The legacy business refusals of RWB-E2-028 are the app story's and are not re-tested here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the published contracts; no application code is built here |
| Negotiable | Replica counts, resource sizes, alert thresholds, topic partitions and retention and the cluster topology are environment values, not story decisions |
| Valuable | Makes the L1 capability deployable, observable and repeatable, and gives the on-call rota a signal when a segment must drop back to shadow |
| Estimable | One chart, one pipeline stage, one migration job, two deployments, two probes, two provisioning steps, one registration step, one route publication, eight dashboard panels, six alert rules and six runbook entries |
| Small | Fits one sprint with the runbook and the capacity plan |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the queue is registered, the registration answers an event, the topic and its rights exist, the alerts fire on a synthetic metric, the route answers within 2 s |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-agent L1 intake capability

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart deploys the api and the worker from one artefact (new, D-RCV-60)
    Given the rwb-agent Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the api deployment and the worker deployment, the pre-deploy migration job, the service, the config map and the platform secret references
    Then no replica count, resource size, log level, feature switch or environment name is hard-coded in the template
    Then one artefact is promoted through the three environments and is never rebuilt between them

  Scenario: AC2 The rwb_agent login and the Flyway run are in place (new, D-RCV-60)
    Given the login and schema of the service, provisioned with rights on rwb_agent only
    When the migration job runs
    Then it applies V10_008__agent_feedback.sql in the per-service Flyway sequence and reports the schema at the expected version before the rollout is marked ready
    Then agent_feedback exists with unique (agent_run_id, item_key) and the verdict check, and the library tables outbox_event, processed_event and idempotency_key exist in the same schema
    Then the login holds no grant on another schema and no migration of this release touches one
    Then a failed migration leaves the release unready and no traffic reaches the new version

  Scenario: AC3 The worker polls rwb-agent in namespace rwb-recovery and scales on backlog (new, D-RCV-60)
    Given the provisioning step and the worker deployment
    When a synthetic backlog is queued on rwb-agent
    Then the worker polls only its own task queue in namespace rwb-recovery with the release build ID on the version set
    Then KEDA scales the worker on the task-queue backlog between the minimum and the maximum of the values file
    Then no worker of this release polls another service's queue

  Scenario: AC4 The L1 run is registered as an event-started workflow and no Schedule exists (new, D-RCV-60)
    Given the registration step
    When it runs
    Then AgentRunWorkflow with ResolveIntakeMode and RecordIntakeFeedback is registered on the queue rwb-agent in namespace rwb-recovery
    Then a synthetic rwb.case.CaseCreated.v1 starts one run for the case and the event, and a repeat of the same event ID starts no second run
    Then no Schedule is registered for the capability, because a run starts from an event and a verdict from a person
    Then a Schedule found in the namespace fails the release

  Scenario: AC5 The topic, the record feed and the consumer groups are provisioned (new, D-RCV-60)
    Given the provisioning step
    When it runs
    Then rwb.agent.events.v1 exists with its retry topic and its .dlt topic and the publish right of rwb-agent
    Then rwb.decision-record.v1 is reachable by the decision-record library with its retry and .dlt topics
    Then rwb-agent holds the consume right on rwb.case.events.v1 through its own consumer group, and the consume rights of rwb-decision, rwb-document, rwb-deviation and rwb-reporting on rwb.agent.events.v1 are verified and created by their own releases
    Then the outbox relay of the release publishes within its interval and a message that fails its registry subject lands in .dlt

  Scenario: AC6 The reads are wired by contract, secrets are references and egress is closed (new, D-RCV-60)
    Given the values files, the configuration step and the secret and egress step
    When the release is rendered and started
    Then LOV-PRODUCT, LOV-REGION, LOV-AUTONOMY, LOV-FEEDBACK, LOV-DECISION, LOV-AGENT and LOV-AGENT-RUN are read through the rwb-case reference-data contract and the business date through the rwb-source-data freshness read
    Then no list value, no mode, no segment, no confidence floor and no decision code appears in a values file or in the chart template
    Then every secret is a reference to the platform secret store, and no secret value appears in the chart, a dashboard or the runbook
    Then egress is open only to the ACE database, the Kafka brokers, the Temporal frontend, the gateway-bff route and the model endpoint of the agent platform
    Then the rwb.agent.intake-l1 switch is off in DEV and on in SIT and UAT only after the smoke read answers

  Scenario: AC7 Probes, scaling and the smoke read answer (new, D-RCV-60)
    Given a running pod of the api and of the worker
    When the readiness probe is called before the migration job and the start-up window complete
    Then the pod is not marked ready
    When the readiness and liveness endpoints are called after start-up
    Then both answer healthy without a database write
    Then the smoke read of GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs for a synthetic case answers within the 2 s budget through the route, and the smoke verdict answers 200 with the feedback set
    Then the worker minimum and maximum, the connection cap of the login and the relay interval are the values of the environment plan

  Scenario: AC8 The dashboards, the alerts and the runbook cover the L1 gate (new, D-RCV-60)
    Given the published dashboards and the runbook
    When a synthetic day is replayed with a fallen acceptance rate, a risen override rate, a .dlt message, a backlog and a stale business date
    Then the dashboards show runs by mode, the L1 acceptance and override rates by segment and business date, the fallback rate, tool read failures, .dlt messages, feed lag, worker backlog and refused reads
    Then the acceptance alert fires below its floor, the override alert above its ceiling, the .dlt alert on the message type and the stale-date alert with MSG-P1-001
    Then the refused-read count carries MSG-P4-002 and does not page the on-call rota
    Then every alert links one runbook entry with the check, the owner role and the recovery step
    Then the alert thresholds, the window of the backlog rule and the retention of the dashboard series are Not specified in the source documents (GAP-0624; ASM-0927)

  Scenario: AC9 The route is published and the runbook, the rollback and the capacity plan are accepted (new, D-RCV-60)
    Given the route publication step, the runbook, the rollback plan and the capacity plan
    When the two operations are called through the gateway-bff route and the rollback is rehearsed in SIT
    Then the route makes one hop to rwb-agent and returns the answer unchanged within the 2 s budget, with the If-Match header and the refusals passed through
    Then no screen calls rwb-agent directly and the route is published for the three environments
    Then the rollback redeploys the previous chart version, re-registers the workflows from the previous release and leaves the schema at its forward-only version
    Then the capacity plan states the runs of a peak business date, the worker minimum and maximum, the connection cap of the login and the relay interval
    Then the route path and the deployment topology detail are Not specified in the source documents (GAP-0624; ASM-0923; ASM-0928)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_agent` login reference and no other service's credential, and the login holds rights on `rwb_agent` only | DP-02; Arch v5 slide 16 |
| BR2 | The migration of `agent_feedback` is a per-service Flyway sequence in schema `rwb_agent` and runs before the rollout is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every topic has a retry topic and a `.dlt` topic, and the outbox relay publishes within its interval | DP-09; Arch v5 slide 11 |
| BR4 | The intake run is an event-started workflow on the queue `rwb-agent` in namespace `rwb-recovery`; the release registers no Schedule for a cadence | DP-10; Arch v5 slides 16, 31 and 44 |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, probe timings, alert thresholds, the KEDA minimum and maximum and the switch state come from values files and from contracts | DP-07; §R7.2 s17 |
| BR6 | An alert carries a message ID where one exists and links one runbook entry | §R7.2 s14 |
| BR7 | A refused read is counted on the dashboard and never pages the on-call rota | MSG-P4-002 |
| BR8 | The release writes only schema `rwb_agent` and reads other services only through their contracts, one hop and 2 s each | DP-01 |
| BR9 | The decision record leaves through the local library on `rwb.decision-record.v1`; the release provisions the right and no copy, no lake write and no daily file | DP-03 |
| BR10 | The two operations are published only behind the gateway-bff pass-through route, and a screen never reaches the service | DP-19; ADR-019 |
| BR11 | The release carries no Schedule, no job table and no Quartz artefact of any kind | DP-10; Arch v5 slide 44 |
| BR12 | The feature switch `rwb.agent.intake-l1` is a data row of the platform flag library: off, the read answers an empty list and the panel is hidden | §R3 default ruling (feature flags to the platform library) |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version, the worker has polled and both probes answer | Ready |
| Ready | Workflows registered | The registration accepts `AgentRunWorkflow` and a synthetic event starts one run | Ready with the L1 path live |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is on the version set | Ready |
| Ready | Migration failed, a probe failed, the registration rejected or a Schedule found | The schema is not at the expected version, a probe is unready, the namespace refused the registration or a cadence Schedule exists | Failed |
| Failed | Rollback | The previous chart version is redeployed and the workflows are re-registered from the previous release | Ready |

The states of a run (ANSWERED, TIMED_OUT, GUARDRAIL_FAILED and the rest of LOV-AGENT-RUN) and the states of a verdict (ACCEPTED, CORRECTED, REJECTED) are the app story's and are only watched here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning and registration steps, the route publication, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the registration rights |
| ACE database administrator | Owns the `rwb_agent` schema, its login, its grants and the migration job approval |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the six runbook entries and opens an incident when an acceptance alert, a `.dlt` alert, a backlog alert or a failed migration persists |
| RW-PLATADM | Reads the runs and the metrics in the running service, not in the cluster |
| RW-COE, RW-RISK | Read the acceptance and override rates the alerts speak of |

The per-service login name used by the chart is Not specified in the source documents (GAP-0624; ASM-0916); the chart references it through a secret reference and never a literal password.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switches, environment name |
| Schema and login | `rwb_agent` and its login, migrated by the per-service Flyway sequence; `agent_feedback` from this release and the library tables |
| Topics | `rwb.agent.events.v1` published with its retry and `.dlt` topics; `rwb.decision-record.v1` for the record; `rwb.case.events.v1` consumed through the service's own group |
| Queue | Temporal task queue `rwb-agent` in namespace `rwb-recovery`, event-started |
| Workflow registration | `AgentRunWorkflow` with `ResolveIntakeMode` and `RecordIntakeFeedback`; no Schedule |
| Parameters and reference data | LOV-PRODUCT, LOV-REGION, LOV-AUTONOMY, LOV-FEEDBACK, LOV-DECISION, LOV-AGENT and LOV-AGENT-RUN through the reference-data contract, never held as deployment values |
| Dashboard series | Runs by mode, L1 acceptance rate, override rate, fallback rate, tool read failures, `.dlt` messages, feed lag, worker backlog, refused reads, migration state |
| Runbook entries | Acceptance below floor, override above ceiling, `.dlt` message, worker backlog, failed migration, route unavailable |
| Secrets | The `rwb_agent` login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class, exact probe timings), the alert thresholds, the topic partition count, replication factor and retention, the dashboard series retention, the host, the SKU and the budget of the release are Not specified in the source documents (GAP-0624; ASM-0926; ASM-0927; ASM-0928); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded.

### 12. Contract

#### 12.1 REST operations provided

The release publishes the two L1 operations behind the gateway-bff pass-through route, one hop: `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` and `POST /api/recovery/agent/v1/agent-runs/{runId}/feedback`, owner rwb-agent (P10), with the rights, the headers and the refusal codes fixed by RWB-P10-E2028-CON. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Item | Owner | Deployment need |
|---|---|---|
| `rwb_agent` schema and its login, with the grant list of the service only | ACE database team, on the P10 ownership of the eight agent tables and `agent_feedback` | The migration job, the read, the verdict and the relay run as this identity; no grant on another schema (DP-02, DP-15) |
| ACE PostgreSQL connection and its pool | ACE database team | One connection pool per deployment; the cap is a value of the environment (DP-01) |
| Kafka cluster and topic provisioning, with the retry and `.dlt` convention | Platform event team (RWB-PLT-EVT) | `rwb.agent.events.v1`, its retry and `.dlt` topics, `rwb.decision-record.v1` and `rwb.case.events.v1` (DP-03, DP-09) |
| Temporal cluster, namespace `rwb-recovery` and the task queue `rwb-agent` | Platform workflow team (RWB-PLT-WF, RWB-PLT-E1071-CON) | The worker, the event-started registration and the worker version set (DP-10) |
| Platform secret store | Platform library (RWB-PLT-LIB) | The database, Kafka and Temporal material, referenced and never inlined |
| Platform feature-flag library | Platform library (§R3 default ruling) | The `rwb.agent.intake-l1` switch as a data row (BR12) |
| gateway-bff route | Edge team (RWB-PLT-N001-CON) | The pass-through route in front of the two operations (DP-19) |
| rwb-case reference-data contract | P3 rwb-case (RWB-P3-E1043-CON) | The seven lists at run time (DP-07) |
| rwb-case case record contract | P3 rwb-case (RWB-P3-E1035-CON) | The case facts, the scope and the case-decision proposal |
| rwb-decision decision-log entry read | P7 rwb-decision (RWB-P7-E1027-CON) | The entry of a verdict, read back for the monitor |
| rwb-source-data freshness read | P1 rwb-source-data | The business date the stale check compares (the `GET /freshness` of Arch v5 slide 15) |
| Model endpoint INT-23 of the agent platform | Enterprise AI interface, through the agent platform of the earlier P10 stories | The egress rule the run needs; no credential of it is held by this release |

Every operation is one hop with a 2 s client budget. No lake credential, no extract file, no data-set job and no job table is consumed or created.

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) and `rwb.agent.AgentFeedbackRecorded.v1` | `rwb.agent.events.v1` | The topic, its retry topic and its `.dlt` topic, the publish right of rwb-agent and the relay interval of the outbox are provisioned and verified by this release; the events belong to the run path and the verdict path of RWB-P10-E2028-APP |
| DecisionRecorded, the decision-record type of the library | `rwb.decision-record.v1` | The topic, its retry and `.dlt` topics and the publish right of the library are verified by this release; the record belongs to the same verdict path (DP-03) |

No daily copy, no extract and no lake write exists: the feed is these topics only.

#### 12.4 Events consumed

| Event | Topic | Consumer group | Provisioning |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | The consumer group of rwb-agent, created by this release | The consume right, the group and the inbox table of the service; dedupe on the event ID |

The consumer groups of `rwb.agent.events.v1` belong to rwb-decision, rwb-document, rwb-deviation and rwb-reporting (Arch v5 slide 43) and are created by their own releases; this story verifies that each consume right exists and puts the feed lag of the topic on the dashboard, and creates none of them inside rwb-agent (GAP-0624; ASM-0926).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| AgentRunWorkflow | Workflow, event-started, one execution per case and event (no Schedule) | `rwb-agent` in namespace `rwb-recovery` | Worker deployment with the release build ID on the version set; registered by the registration step |
| ResolveIntakeMode | Activity | `rwb-agent` | Registered by the same worker; reads the policy and the case contract |
| RecordIntakeFeedback | Activity (workflow kit, one transaction) | `rwb-agent` | Registered by the same worker; writes the record, the feedback and the outbox row |
| KEDA scaling | Worker scaler | `rwb-agent` | Scales on the task-queue backlog between the minimum and the maximum of the values file |

The release carries no Temporal Schedule: a run starts from `rwb.case.CaseCreated.v1` and a verdict comes from a person (BR4, BR11).

#### 12.6 Schedules

None. The release registers no Temporal Schedule, and a Schedule found in namespace `rwb-recovery` for this capability fails the release: the intake run is event-started and no cadence belongs to it (DP-10; BR4, BR11). The legacy Quartz entry of the intake job is retired with the stage and no job table is deployed or read.

#### 12.7 Tables owned

| Item | Owner | Deployment element |
|---|---|---|
| login of rwb-agent, with rights on schema `rwb_agent` only | ACE database team on the P10 ownership | The secret reference the api and worker deployments and the migration job use (DP-02) |
| schema `rwb_agent` and its Flyway history table | P10 | Created by the earlier P10 migrations; the migration job brings it to the expected version (DP-15) |
| agent_feedback | P10 (`rwb_agent`) | Created by `V10_008__agent_feedback.sql` in the migration job, with unique (agent_run_id, item_key) and the verdict check |
| agent_run, agent_policy, agent_prompt | P10 (`rwb_agent`) | Created by the earlier P10 migrations; read by the read and the verdict |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | Created by the same migration job; used by the relay and the inbox |

No table of another schema is created, read or granted by this release (DP-01).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-case WireMock (RWB-P3-E1035-CON, RWB-P3-E1043-CON) | Runs in the pipeline and in the SIT smoke profile so the release can start without rwb-case, with the case facts, the scope, the seven lists and the case-decision proposal |
| rwb-decision WireMock and decision-record stub (RWB-P7-E1027-CON, RWB-PLT-E1027-CON) | The same, answering the sealed entry of a verdict and accepting the record |
| rwb-source-data WireMock | The same, answering the business date of the smoke case |
| gateway-bff route stub (RWB-PLT-N001-CON) | The same, a pass-through of one hop in front of the two operations with the `If-Match` header preserved |

The fakes are test-only workloads; they are not deployed into UAT or production. Every fixture is synthetic and holds no personal data.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided behind the route, 5 consumed | The two operations on `/api/recovery/agent/v1`; the case read, the case-decision proposal, the lists, the entry read and the freshness read consumed, one hop and 2 s each |
| Kafka | 3 published, 1 consumed by this release | `AgentRunCompleted`, `AgentFeedbackRecorded` and the decision record, each with retry and `.dlt`; `CaseCreated` through the service's own group; the consumer groups of the agent topic belong to their own releases |
| Temporal | 1 workflow, 2 activities, 0 Schedules | AgentRunWorkflow with ResolveIntakeMode and RecordIntakeFeedback on the queue `rwb-agent`, event-started, with KEDA on backlog |
| File | None | The release carries no file, no extract and no data-set job |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The four H rows of the platform and the C row of rwb-case are the ones the release consumes as published artefacts; the metadata rows of this story declare no build dependency, because a CON dependency never blocks and a deployment story is Day 1 by rule (§R5.7). DP-09 and DP-10 carry the topic and the queue; DP-15 carries the migration job; DP-19 carries the route; DP-13 fixes the base the route publishes.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-agent/` | Chart with the api deployment, the worker deployment, the service, the migration job, the config map, the secret references, the probes and the workflow registration hook |
| `helm/rwb-agent/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switches, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | `rwb.agent.events.v1` with its retry and `.dlt` topics and the publish right; `rwb.decision-record.v1` verified; `rwb.case.events.v1` consume right and group; task queue `rwb-agent` in namespace `rwb-recovery` |
| Registration step | `AgentRunWorkflow` event-started with its two activities; the assertion that no Schedule exists |
| Route publication | The two operations registered behind the gateway-bff pass-through route, one hop |
| KEDA scaling | Worker scaled on the task-queue backlog with a minimum and a maximum from the values file |
| Dashboards | Eight panels: runs by mode, L1 acceptance rate, override rate, fallback rate, tool read failures, `.dlt` messages, feed lag, worker backlog and refused reads |
| Alerts | Six rules: acceptance below floor, override above ceiling, `.dlt` message, worker backlog, failed migration, stale business date |
| Runbook | Six entries: acceptance below floor, override above ceiling, `.dlt` message, worker backlog, failed migration, route unavailable |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the worker has polled, the relay is running and the last reference-data read answered; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database. Exact paths and timings are values.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_agent` with the service login as a pre-deploy job with a backoff limit; `V10_008__agent_feedback.sql` applies in order with the earlier P10 migrations, a failed job blocks the rollout and the release, and the sequence is forward only (DP-15; GAP-0624; ASM-0921).

**Alert mapping.**

| Check | Condition | Alert | Route |
|---|---|---|---|
| Acceptance below floor | The L1 acceptance rate of a segment and business date falls below its floor | Acceptance alert with the agent, the segment, the date and the rate, and the review action | RW-COE and RW-RISK, ticket |
| Override above ceiling | The correction plus rejection rate of the segment rises above its ceiling | Override alert with the segment, the date and the rate | RW-COE and RW-RISK, ticket |
| `.dlt` | A message lands in the `.dlt` topic of the agent topic | `.dlt` alert with the message type and its registry subject | Platform on-call, page |
| Backlog | The task-queue backlog passes its window | Backlog alert with the queue and the age of the oldest task | Platform on-call, ticket |
| Failed migration | The migration job fails | Release alert with the schema version reached | Platform on-call, page |
| Stale business date | The business date of the runs is older than the day | Stale-date alert with the business date and the data date, and MSG-P1-001 on the panel | Data steward, ticket |
| MSG-P4-002 | A read without the Case record right | Refused-read count on the dashboard | No page |

The floors and ceilings of the acceptance and override alerts are Not specified in the source documents (GAP-0624; ASM-0927) and are reviewed values per environment.

**Capacity.** The plan states, per environment, the runs of a peak business date, the pages served to the panel, the worker minimum and maximum, the connection cap of the login and the relay interval. The target is the legacy measure: the panel answers a case within the 2 s budget of NFR-009 and a verdict is stored before the owner leaves the screen.

**Rollback.** The previous chart version is redeployed and the workflows are re-registered from the previous release; the Flyway sequence is forward only, so `agent_feedback` stays and no down-migration is run; the topic, its retry and `.dlt` topics and the publish right stay in place, because removing them would break the feed of the monitor and of the projections; a rollback is rehearsed in SIT before UAT.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer, the queue, the topic and the rights are verified by a test, the event-started registration answers one run per case and event and no Schedule exists, the six alerts fire on synthetic conditions, the route answers within 2 s, the capacity plan is reviewed, the rollback is rehearsed and the six runbook entries are accepted by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The business date of the runs is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A read without the Case record right | You cannot {action} here. Your role does not include it. |
| MSG-P10-005 | The panel shows no summary because the run failed | The agent summary is not available for this case. Work from the case record. |

The three texts appear in the sources of this key and keep their wording character for character; the deployment adds the alert routing and the runbook link, never a new wording. The acceptance, override, `.dlt`, backlog and migration alerts have no message ID in the legacy story and keep none.

### 15. Screens and states

The deployment serves the panel "Agent summary" of SCR-03 Case record of RWB-P10-E2028-APP through the gateway-bff pass-through route (DP-19) and publishes the two operations on it. The operator-facing surfaces of this story are the pipeline run view, the release view, the dashboards and the runbook. The screen field list and the composition of SCR-03 belong to the app story and to the edge story, and SCR-46 Agent monitor belongs to RWB-P10-E2031-APP; neither is changed here. The exact path of the route is Not specified in the source documents (GAP-0624; ASM-0923).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E2028-OPS-01 | AC1 | NFR | Chart renders for DEV, SIT and UAT with the digest pinned, the two deployments, the migration job, the config map and the secret references |
| TC-P10-E2028-OPS-02 | AC2, BR1, BR2 | NFR | The migration job applies `V10_008__agent_feedback.sql`, the schema reaches the expected version, the unique key and the check exist, and the login holds no other grant |
| TC-P10-E2028-OPS-03 | AC3, BR4 | End to end | A synthetic backlog scales the worker on `rwb-agent` in `rwb-recovery` with the build ID on the version set, and no other queue is polled |
| TC-P10-E2028-OPS-04 | AC4, BR4, BR11 | End to end | One event starts one run, a repeat starts none, and a Schedule inserted into the namespace fails the release |
| TC-P10-E2028-OPS-05 | AC5, BR3, BR9 | NFR | The topic, its retry and `.dlt` topics, the record topic, the rights and the consumer groups of the four consumers verified; a refused payload lands in `.dlt` |
| TC-P10-E2028-OPS-06 | AC6, BR5, BR12 | NFR | The seven lists and the business date come from the contracts, no list or policy value is in a values file, every secret is a reference, egress is limited, and the switch state per environment |
| TC-P10-E2028-OPS-07 | AC7 | End to end | Probes false before the migration, true after; the smoke read and the smoke verdict answer within 2 s through the route against the four fakes |
| TC-P10-E2028-OPS-08 | AC8, BR6, BR7 | NFR | Six synthetic conditions raise the mapped alerts with MSG-P1-001 and MSG-P4-002 where they apply, and each links one runbook entry |
| TC-P10-E2028-OPS-09 | AC9, BR10 | End to end | The route answers one hop within 2 s with the header preserved; the rollback is rehearsed with the workflows re-registered and the schema forward only; the capacity figures stated |

The nine test cases are this story's own (D-RCV-60) and test the deployment artefacts rather than the business outcomes, which are the app story's: the eleven legacy test cases TC-E2-028-01 to TC-E2-028-11 stay with RWB-P10-E2028-APP and are not copied here. The legacy System level maps to End to end where the registration and the route answer are proved, and to NFR where a rendered artefact or a threshold is asserted.

### 17. Guardrails

- No business value in a values file: the lists, the mode, the segment, the confidence floor, the decision code and the acceptance floors are contract and registration values, never deployment values (DP-07, BR5).
- No personal data in logs, dashboard series, alert payloads or the runbook: counts, identifiers, dates and durations only.
- No other service's table is read and no grant crosses a schema: the login holds rights on `rwb_agent` only (DP-01, DP-02).
- Every topic has a retry topic and a `.dlt` topic, and the relay publishes within its interval (DP-09).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.
- The release registers no Schedule and carries no job table; a cadence Schedule fails the release (DP-10, BR11).
- The two operations are published only behind the gateway-bff route, one hop, and a screen never reaches the service (DP-19, BR10).
- Every fixture is synthetic; no production case, summary, verdict or record is copied into a schema, a payload or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision records the agent and prompt versions | The verdict path runs as the `rwb_agent` identity and writes its record through the library; the dashboards count the entries per agent version | TC-P10-E2028-OPS-02, TC-P10-E2028-OPS-07 |
| REQ-ACA-005 | Personal data masked by role on every screen and every agent call | No personal field in a dashboard series, an alert payload or the runbook, and the smoke fixtures are synthetic | TC-P10-E2028-OPS-07, TC-P10-E2028-OPS-08 |
| D-RCV-60 DP-03 | Decision record written locally and sealed centrally | The right and the retry and `.dlt` topics of `rwb.decision-record.v1`, verified by the release | TC-P10-E2028-OPS-05 |
| D-RCV-60 DP-07 | Reference data read from rwb-case | The seven lists and the business date wired by contract and absent from the values | TC-P10-E2028-OPS-06 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | Topic provisioning, the retry and `.dlt` topics, the publish right, the relay interval and the feed-lag panel | TC-P10-E2028-OPS-05 |
| D-RCV-60 DP-10 | Event-started workflows replace Quartz | The queue, the namespace, the registration and the assertion that no Schedule exists | TC-P10-E2028-OPS-03, TC-P10-E2028-OPS-04 |
| D-RCV-60 DP-15 | Per-service Flyway and migration ownership | The migration job, the forward-only rollback and the grant check | TC-P10-E2028-OPS-02, TC-P10-E2028-OPS-09 |
| D-RCV-60 DP-19 | gateway-bff composite route | The route publication and the one-hop smoke read | TC-P10-E2028-OPS-09 |
| ADR-021 | Per-service Flyway and migration ownership | The migration job and the forward-only schema | TC-P10-E2028-OPS-02, TC-P10-E2028-OPS-09 |
| ADR-023 | Observability per service | Eight dashboard panels, six alert rules and six runbook entries | TC-P10-E2028-OPS-08 |
| NFR-009 | The case record view loads for a case with 50 documents, under 2 s | The smoke read through the route within the 2 s budget | TC-P10-E2028-OPS-07 |

The gap GAP-0624 records the areas the sources leave open for this deployment — the login name, the migration order, the route path, the topology and every threshold, the topic partitions and retention, the dashboard retention and the consumer groups of the agent topic — and each default it raises is settled by ASM-0916, ASM-0921, ASM-0923, ASM-0926, ASM-0927 and ASM-0928.

### 19. Out of scope

- The application code of the mode resolver, the read, the verdict path and the record (RWB-P10-E2028-APP).
- The contract documents and the fakes as published artefacts (RWB-P10-E2028-CON); this story deploys the test copies only.
- The agent platform, the shadow run path and the model gateway of the earlier P10 stories (RWB-P10-E1058-APP and its contract baseline).
- The L1 proposal payload and the configuration operations (RWB-P10-E1061-CON) and the metric read (RWB-P10-E2031-APP).
- The platform topic provisioning implementation, the Temporal cluster, the KEDA operator and the secret store (the platform epics RWB-PLT-EVT, RWB-PLT-WF, RWB-PLT-OBS and RWB-PLT-LIB).
- The case, the case-decision proposal and the reference data (P3 rwb-case), the entry and the ledger (P7 rwb-decision) and the freshness read (P1 rwb-source-data).
- The panel and the screen composition of SCR-03 and SCR-46 (RWB-P10-E2028-APP, RWB-P10-E2031-APP).
- The exact deployment topology, the host, the SKU, the budget, the replica counts, the resource sizes, the probe timings, the alert thresholds, the topic partitions and retention (GAP-0624).
- The end-to-end run of the nine legacy criteria across services (RWB-ITG-W2).
