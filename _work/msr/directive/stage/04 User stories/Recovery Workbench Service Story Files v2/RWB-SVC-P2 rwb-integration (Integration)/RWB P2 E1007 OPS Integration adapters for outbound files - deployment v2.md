# RWB-P2-E1007-OPS Integration adapters for outbound files

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E1007-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP16, DP17, DP19 |
| Parallel lane | L-P2-B |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-16); squad sizes at refinement |
| Depends on (build) | None |
| Contract dependencies | rwb-source-data contract for the INT-14 addressee and contact value; operation and elements: Not specified in the source documents (GAP-1162); rwb-document contract for REST POST /documents (upload link), used for the INT-14 file with a claim-check reference only |
| Contract version | v1 (the /v1 path this story builds against) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-001, FR-P2-002, FR-P2-003, FR-P2-004, FR-P2-005, FR-P2-006, FR-P2-007, FR-P2-008, FR-P2-009, FR-P2-010, FR-P2-011, FR-P2-012, FR-P2-013, FR-P2-014, FR-P2-015, FR-P2-016, FR-P2-017, FR-P2-018, FR-P2-020, FR-P2-021, FR-P2-022) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-007 for rwb-integration. The legacy story assumed a shared Quartz scheduler that ran JOB-10, JOB-11, JOB-13 and JOB-15, a shared database that held every table, and an exception queue that an operator could see by opening the database. This story deploys the outbound-file capability of rwb-integration: one chart and values, the Flyway baseline of `rwb_integration`, the topic and the task queue with retry and `.dlt`, the two Airflow file windows that are not Schedules, the held and failed file alerts, the dashboards and the runbook. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 35 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the rwb-integration outbound-file capability deployed as one Helm release with its values files, its per-service Flyway baseline in `rwb_integration`, its topic and task queue with retry and `.dlt`, its worker scaling on the queue backlog, the WIN 16:00 and per-lot buyer windows carried by the bank Airflow and not by a Schedule, the held-file and failed-file alerts, the dashboards and the runbook**, so that **an operator can see a file that was held or that stopped moving, resend it, and prove that nothing was lost between an outbound request and a party outside the bank without reading code or opening a database**.

The legacy story ran the adapter behind a shared Quartz scheduler and a shared schema: JOB-10 built the WIN file at 16:00, JOB-11 sent due items every minute, and JOB-13 and JOB-15 copied two files to a data lake. In the target that picture splits in three. JOB-10's window is opened by the bank's Airflow, which calls the requesting service and never a `rwb_*` schema; the file is still built and sent by rwb-integration (Arch v5 slides 16, 32 and 44). JOB-11 is the platform outbox relay that runs every minute in every service. JOB-13 and JOB-15 are removed with the data lake: the reporting extract is a `deliverFile` request from rwb-reporting and the decision and outcome feed is continuous Kafka ingest in rwb-decision (DP-17). What is left for this story is a deployment, a topic, a queue, two windows it does not own, four alert rules and a runbook.

Deployment is also where the split is enforced operationally. The release carries the rwb-integration login only, migrates `rwb_integration` only, publishes on its own topic only and subscribes to `rwb.source-data.events.v1` only. It provisions no ACE grant, no view and no data-lake route: an operator cannot reach an ACE fact or a lake file from this deployment, because neither exists in it (DP-01, DP-02, DP-05, DP-17). The observability follows ADR-023 per service: six series, four alerts and five runbook entries, each alert carrying a message identifier and one runbook entry.

### 2. Business rationale

The business measure of this legacy key is "outbound items in the exception queue over one day: zero". A deployment is what makes that measure visible: a held file, a parked item, a retry that keeps failing and a topic that falls behind are all failures that no unit test can see, and all of them are silent unless the release emits them. The busiest hour of this service is 16:00, when the letter window opens and rwb-comms requests the WIN file; the buyer tape arrives per awarded lot and can land at any hour (Arch v5 slides 32 and 33). Both are visible only if the queue, the items and the events are instrumented.

The split changes what an operator does. In the legacy story the operator opened the exception queue in the same database and restarted the Quartz job. In the target the operator reads SCR-09 through the edge, resends an item or a delivery through the admin operation, and checks three things: that the worker polls `rwb-integration`, that the item's next attempt is in the future and moving, and that `FileDelivered` or `FileFailed` reached the requesting service. The runbook is written for that sequence, and the alerts are wired to it, because the difference between a busy hour and an incident is whether the operator has to guess which of the three failed.

The story also carries the retirement explicitly. No Schedule is registered for the two windows, no lake target is provisioned, and no inbound consumer exists: the deployment would fail its own checks if it created one, because the topic list, the migration target and the queue subscription are all fixed by the release checklist (BR1, BR2, BR12).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Kafka event platform provides `rwb.integration.events.v1` with its retry and `.dlt` topics and the shared topic `rwb.decision-record.v1`, and the ACLs of this service's principals (RWB-PLT-EVT, RWB-PLT-TE006-CON; DP-09, DP-14).
- The Temporal workflow kit and the namespace `rwb-recovery` exist, with worker versioning, the build ID provider and the payload codec (RWB-PLT-WF, RWB-PLT-E1071-CON; DP-10).
- The per-service Flyway sequence and the migration conventions of `rwb_integration` are published (RWB-PLT-E1044-CON; DP-15).
- The platform error envelope and the message catalogue are in force, so an alert can carry a message identifier.
- The three environments DEV, SIT and UAT exist and the production namespace exists for the release date; the feature flag `rwb.integration.file-adapters` exists in the platform flag library.
- The two MFT/SFTP endpoints, the keys and the staging area exist in each environment (RWB-P2-E1007-INF).
- The gateway-bff composite route for SCR-09 is published (RWB-PLT-N001-CON; DP-19).
- The bank Airflow owns the WIN window at 16:00 and the debt-buyer window per lot and calls the services through their APIs only (Arch v5 slides 16, 32 and 44; ASM-1074).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The baseline it deploys is RWB-P2-E1007-APP's and the values it injects are RWB-P2-E1007-INF's; both are declared before the release and neither blocks the chart work.

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the API deployment and the worker deployment with the rwb-integration login, the namespace `rwb-recovery`, the task queue `rwb-integration`, the codec, the build ID of the release and the endpoint references of RWB-P2-E1007-INF.
3. The worker scaling step enables KEDA on the queue backlog of `rwb-integration`, so the back grows with the 16:00 window and the per-lot buyer tape and the front stays at its fixed replica count.
4. The migration step applies the `rwb_integration` sequence of the release, starting with the V0001 baseline of the three P2 tables and the library objects, and refuses to run when the target schema is not `rwb_integration`.
5. The topic step creates or verifies `rwb.integration.events.v1` with its partitions, its replication factor, its retention, its retry topics at 1 minute, 10 minutes and 1 hour and its `.dlt` topic, and records the ACL of the producer and of the requesting services' consumer groups.
6. The window step confirms that the WIN window at 16:00 and the debt-buyer window per lot are opened by the bank Airflow, that the deployment registers no Schedule for either, and that the interface row of each environment holds the file pattern and the folder.
7. The flag step sets `rwb.integration.file-adapters` from the values of the environment.
8. The dashboards are published with the six series and the environment, release and build ID as dimensions.
9. The four alerts are wired to their message identifiers and to their runbook entries: MSG-P2-001 for a parked item, `FileFailed` for a failed file, the held-item series for a held file, and the identifier the Error and Message Standard has yet to name for the topic lag, carried as Not specified in the source documents (GAP-0650; ASM-1085).
10. A smoke step in DEV requests one synthetic INT-14 file for a synthetic business date, follows it to ACKNOWLEDGED against the MFT stub, forces one transfer failure to EXCEPTION with `FileFailed`, resends it through the admin operation, and confirms that no second file exists and that the environment is restored.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready and the pipeline stops; no traffic, no offset and no migration is left half applied | None | AC1 |
| X2 | The migration step is pointed at a schema other than `rwb_integration` | The step refuses and the release stops | None | AC1 |
| X3 | A consumer group of `rwb.integration.events.v1` lags past its threshold | The lag series rises and the lag alert fires; the runbook entry names the group, the topic and the partition | Not specified in the source documents (GAP-0650; ASM-1085) | AC2, AC4 |
| X4 | The feature flag is off in an environment | No worker is deployed, the queue holds no poller and `deliverFile` refuses, so no item and no file exist | None | AC1 |
| X5 | A transfer fails on its last allowed attempt | The item is EXCEPTION, `FileFailed` is published and the failed-file alert fires with MSG-P2-001 | MSG-P2-001 | AC4, AC6 |
| X6 | The ACE batch of the business date is not complete, so the request is held | No item and no file exist; the held-file alert fires on the held-item series and the runbook names the freshness check | MSG-P1-001 | AC4 |
| X7 | The 16:00 window or a per-lot buyer window does not start | The window check fails the smoke run and the runbook entry names the Airflow DAG and the requesting service | Not specified in the source documents (GAP-0650; ASM-1086) | AC3, AC6 |
| X8 | A dashboard series is missing, or an alert carries no message identifier or no runbook link | The observability check fails the release | None | AC5, AC6 |
| X9 | A new build is promoted while items are in RETRY | The workflow of each item replays on the new build from its history; the dashboards show both build IDs | None | AC1, AC5 |
| X10 | The MFT/SFTP endpoint is unreachable | The attempts fail, the retry ladder of the interface row runs out, the item is EXCEPTION and the alert fires; nothing is lost and nothing is duplicated | MSG-GEN-006 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the topic provisioning, the migration conventions and the flag library; no application code is built here |
| Negotiable | Replica counts, resource sizes, lag and alert thresholds, intervals and consumer quotas are environment values |
| Valuable | Makes the outbound path observable, resendable and provable at the 16:00 window and per buyer lot before the release date |
| Estimable | One chart, one migration step, one topic, one queue, two windows it does not own, six series, four alerts and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the migration refuses a foreign schema, the groups hold offsets, an alert fires on a synthetic metric, the windows start, the smoke run passes |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the outbound-file capability for rwb-integration

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-integration is rwb-integration
    Given the target environment is SIT

  Scenario: AC1 One chart, one login, one schema and one queue are deployed (new, D-RCV-60)
    Given the rwb-integration chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the API and the worker deployments carry the rwb-integration login and no other service's credential
    Then the worker polls only the task queue rwb-integration in namespace rwb-recovery and KEDA scales it on the queue backlog
    Then the migration step applies the rwb_integration sequence from its V0001 baseline and refuses a target schema other than rwb_integration
    Then worker versioning is enabled and a new workflow goes to the new build while the old build drains

  Scenario: AC2 The topic and its retry and dead-letter topics are provisioned with their ACLs (new, D-RCV-60)
    Given the release of this story and the platform event epic
    When the topic step runs
    Then rwb.integration.events.v1 exists with its partitions, its replication factor and its retention
    Then the retry topics at 1 minute, 10 minutes and 1 hour and the .dlt topic exist for it
    Then the producer ACL is granted to the rwb-integration principal only
    Then the consumer ACL of the topic is granted to the requesting services that listen for FileDelivered and FileFailed
    Then a topic outside rwb.integration.events.v1 and rwb.decision-record.v1 is refused by the release
    Then the deployment subscribes to rwb.source-data.events.v1 only and to no topic of this service

  Scenario: AC3 The two file windows belong to the bank Airflow and not to a Schedule (new, D-RCV-60)
    Given the deployed release and the bank Airflow DAGs
    When the bank Airflow DAG calls the WIN window at 16:00 or the debt-buyer window of an awarded lot
    Then the WIN window at 16:00 is opened by the Airflow DAG that calls the requesting service
    Then the debt-buyer window per awarded lot is opened by the same kind of DAG call
    Then the deployment registers no Temporal Schedule and no timer for either window
    Then the Airflow interface uses the service APIs only and reads or writes no rwb_* schema
    Then a repeated window call for the same interface and business date builds no second file, because the idempotency key of the interface row is unchanged
    Then the exact trigger contract of the two windows is Not specified in the source documents and is carried as GAP-0650

  Scenario: AC4 The held-file and failed-file alerts fire with their identifiers (new, D-RCV-60)
    Given the published alert rules of the deployment
    When one synthetic request is held by the freshness check and one synthetic item fails its last attempt
    Then the held-file alert fires on the held-item series with MSG-P1-001
    Then the failed-file alert fires on FileFailed and on the EXCEPTION status with MSG-P2-001
    Then each alert names the interface, the business date, the attempt count and the build ID
    Then each alert carries a message identifier and one runbook link
    Then no alert payload carries an address, an identity number or a file content

  Scenario: AC5 The dashboards show the six series with their dimensions (new, D-RCV-60)
    Given the published dashboards of the deployment
    When a synthetic window, a retry ladder and a set of failures are produced
    Then the dashboards show items by status, attempts per item, the age of the oldest EXCEPTION item, files delivered and failed per interface, requests held by the freshness check, and consumer lag by group and partition
    Then each series carries the environment, the release and the build ID as dimensions
    Then a held file, a parked item and a lagging group are visible on the dashboards before any alert is read

  Scenario: AC6 The runbook and the smoke run cover the operational failures (new, D-RCV-60)
    Given the published runbook and the smoke run of the release
    When a held file, a parked item, a stuck retry, an unreachable endpoint and a lagging group are simulated
    Then each condition maps to one runbook entry with the check, the owner role and the recovery step
    Then the smoke run delivers one synthetic INT-14 file to the MFT stub, parks one item in EXCEPTION with FileFailed and resends it with MSG-GEN-005
    Then the smoke run ends with one file per interface and business date, no duplicate file and the environment restored
    Then no threshold and no interval is hard-coded and no secret appears in a values file, a dashboard or the runbook

  Scenario: AC7 The business rules of section 8 hold in the release (new, D-RCV-60)
    Given the release of this story and its chart and values files
    When the release is checked against the business rules BR1 to BR12
    Then BR1 holds: one login, the task queue rwb-integration and the schema rwb_integration only
    Then BR2 holds: the release publishes on two topics only and subscribes to rwb.source-data.events.v1 only
    Then BR3 holds: the two windows are opened by the bank Airflow and no Schedule is registered for them
    Then BR4 holds: JOB-11 is deployed with the library and is not a job of this service
    Then BR5 holds: no data-lake target, route or delivery row exists
    Then BR6 holds: every alert carries a message identifier and one runbook entry
    Then BR7 holds: no environment value is hard-coded
    Then BR8 holds: dashboard series, alert payloads and the runbook carry no address, identity number or file content
    Then BR9 holds: the four admin operations are exposed through the chart and its ingress and declare no path of their own
    Then BR10 holds: a failing release leaves the previous build in force
    Then BR11 holds: an exhausted item is never deleted and a resend sets PENDING with attempt count 0
    Then BR12 holds: no ACE grant, no view and no inbound consumer is provisioned
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one task queue and one schema per service: the release carries the rwb-integration login, polls `rwb-integration` only and migrates `rwb_integration` only | Arch v5 slide 41; DP-02; DP-15 |
| BR2 | The release publishes on `rwb.integration.events.v1` and on `rwb.decision-record.v1` only, and subscribes to `rwb.source-data.events.v1` only | Arch v5 slides 16, 42 and 43; DP-09; DP-14 |
| BR3 | The two file windows belong to the bank Airflow, which opens them and calls the service APIs only; the deployment registers no Schedule for them | Arch v5 slides 16, 32 and 44; ASM-1074 |
| BR4 | JOB-11 is the platform outbox relay on its one-minute interval and is deployed with the library, not as a job of this service | Arch v5 slide 44; DP-09 |
| BR5 | There is no data-lake target, no lake route and no lake delivery row: the reporting extract is a `deliverFile` request and the decision feed is Kafka ingest in rwb-decision | DP-17; Arch v5 slides 37 and 44 |
| BR6 | Every alert carries a message identifier and the agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | No environment value is hard-coded: replicas, resources, thresholds, intervals, quotas and the flag come from values files and parameters | Template and Rules §R7.2 s17 |
| BR8 | Dashboard series, alert payloads and the runbook carry counts, identifiers, interface codes, business dates and build IDs only, never an address, an identity number or a file content | ADR-023; CTL-11 |
| BR9 | The release exposes the four admin operations through the chart and its ingress and declares no path of its own; SCR-09 is reached through the gateway-bff composite route | DP-19; TSD P2 v3 T-A.1 |
| BR10 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run | DP-10 |
| BR11 | An exhausted item is never deleted: it is EXCEPTION with a task for the owner role, and a resend sets PENDING with attempt count 0 | Legacy AC7; TSD P2 v3 T4 |
| BR12 | The deployment provisions no ACE grant, no view and no inbound consumer, because there is no inbound adapter and only rwb-source-data reads the ACE views | D-RCV-35 U1; ADR-010; DP-05 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Migration applied and worker registered | The `rwb_integration` sequence applied and the worker polls `rwb-integration` | Ready |
| Ready | Release superseded | A new chart version passes its tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open workflows | Ready |
| Ready | Flag off | `rwb.integration.file-adapters` is turned off in the environment | Not deployed |
| Ready | Smoke run failed | The window check, the delivery or the resend step of the smoke run fails | Blocked |
| Blocked | Previous build restored | The previous chart is redeployed or a later build passes the smoke run | Ready |

The item states PENDING, SENT, RETRY, EXCEPTION and ACKNOWLEDGED and the delivery states PENDING, RETRYING, DELIVERED and EXCEPTION are the app story's runtime and are not states of this deployment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the migration step, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic ACLs, the consumer quotas, the flag library and the resend of an item or a delivery |
| Platform event owner | Owns `rwb.integration.events.v1`, its retry and `.dlt` topics, its schema subject and its retention |
| Bank Airflow owner | Owns the DAGs that open the WIN window at 16:00 and the debt-buyer window per lot and that call the service APIs only |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the five runbook entries and opens an incident when a held file, a parked item or a lag persists |
| MFT team | Owns the endpoint, the key and the receiver agreement that the values point to |
| RW-AUDIT | Reads the items, the deliveries, the resend record and the run summaries |

The worker runs as the rwb-integration service identity (DP-02), carried by the chart as a secret reference and never as a literal. The login name is Not specified in the source documents (GAP-0650; ASM-1070).

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts for the API and the worker, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, feature switch, KEDA backlog threshold | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Task queue | `rwb-integration` in namespace `rwb-recovery`, polled by the worker of this service only | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Topic | `rwb.integration.events.v1` with its partitions, replication factor, retention and key, its retry topics at 1 minute, 10 minutes and 1 hour and its `.dlt` topic; `rwb.decision-record.v1` published by the library; `rwb.source-data.events.v1` the only subscription | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Schema | `rwb_integration`, migrated by its own per-service Flyway sequence from the V0001 baseline of `interface_config`, `outbound_item` and `job_catalog` plus the four library objects | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Interface rows | The INT-14 and INT-25 rows with direction OUTBOUND, max attempts 3 and retry intervals 5, 15 and 45 minutes, loaded as reference data by RW-REFADM | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Endpoint values | The WIN and debt-buyer endpoint references, the key identifiers and the staging path of RWB-P2-E1007-INF, injected as values and never as literals | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Dashboard series | Items by status, attempts per item, the age of the oldest EXCEPTION item, files delivered and failed per interface, requests held by the freshness check, consumer lag by group and partition; dimensions environment, release, build ID | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Runbook entries | Held file, parked item, stuck retry, unreachable endpoint, lagging group; each with the check, the owner role and the recovery step | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Alerts | Four rules and one runbook entry each: MSG-P2-001 for a parked item, `FileFailed` for a failed file, the held-item series for a held file, and the identifier placeholder of GAP-0650 for the lag alert | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Secrets | The rwb-integration login secret, the Kafka client credential, the Temporal mTLS material and the MFT credential reference, all from the platform secret store | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |
| Test data | One synthetic INT-14 request for a synthetic business date, one forced transfer failure and one resend; synthetic keys only | Not specified in the source documents (DOR-RWB-P2-E1007-OPS-7) |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded.

**Probes.** Readiness answers healthy only after the worker has polled `rwb-integration` once and the API has answered its health path; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database or commits an offset, and a failing dependency is reported as not ready, never as live-and-broken.

### 12. Contract

#### 12.1 REST operations provided

None from this story. The four admin operations — `GET /api/recovery/integration/v1/admin/outbound-items`, `POST /api/recovery/integration/v1/admin/outbound-items/{itemId}/resend`, `GET /api/recovery/integration/v1/admin/outbox/deliveries` and `POST /api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend` — are declared by RWB-P2-E1007-CON and implemented by RWB-P2-E1007-APP; this deployment exposes them through the chart and its ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None from the deployment. The worker calls the rwb-source-data, rwb-comms, rwb-document, rwb-case and rwb-access contracts at run time as the app story's client; the chart carries no REST client of its own and no outbound call at start-up beyond the Temporal frontend, the Kafka brokers and the MFT endpoint.

#### 12.3 Events published

None of its own. `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` are published by the app story on `rwb.integration.events.v1`; `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library through the relay when an item moves to EXCEPTION or is resent (DP-03, DP-09).

#### 12.4 Events consumed

| Event type | Topic | Deployment element | Service |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | The worker group with the inbox, the retry topic and the `.dlt` routing; releases a held request | rwb-integration |

The topic and its retry and `.dlt` topics are provisioned by the platform event epic; this deployment configures the group, the inbox, the offsets and the relay that hands an event to the worker.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `OutboundFileWorkflow` | Workflow, one execution per interface and business date | `rwb-integration` | Registered by the worker of this release, with the build ID and worker versioning |
| `deliverFile(manifest)` and `receiveFile` | Provided activities | `rwb-integration` | Registered by the same worker; `receiveFile` is called by no flow |
| buildOutboundFile, storeOutboundFile, sendFileOverMft, parkItemInException | Activities | `rwb-integration` | Registered with the kit's retry policy; the file-level ladder is the interface row, not the activity retry |
| Outbox relay | Platform relay | not a worker | Deployed with the library; publishes `rwb.integration.events.v1` and `rwb.decision-record.v1` on its one-minute interval (JOB-11) |

**Build ID and versioning.** The build ID is the one supplied by the workflow kit for the release commit; worker versioning is enabled and a new build takes new workflows while the old build drains. The build ID format and the versioning policy are Not specified in the source documents (GAP-0650; ASM-1085).

#### 12.6 Schedules

None. The deployment registers no Temporal Schedule. The WIN window at 16:00 and the debt-buyer window per lot are opened by the bank Airflow, which calls the requesting services and never a `rwb_*` schema (Arch v5 slides 16, 32 and 44; BR3). The outbox relay runs on the platform's one-minute interval (BR4), and JOB-13 and JOB-15 are removed with the data lake (BR5). The trigger contract of the two windows is a bank Airflow call to the requesting service's own API. Its parameters, the missed-window behaviour and the lag and window alert message identifiers are Not specified in the source documents (GAP-0650; ASM-1086); they are to be confirmed with the Airflow owner and the platform observability owner.

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| `interface_config` | P2 (rwb_integration) | Created by the V0001 baseline; the interface rows are loaded as reference data, never as a chart value |
| `outbound_item` | P2 (rwb_integration) | Created by the V0001 baseline; read by the worker, the sender and the exception queue |
| `job_catalog` | P2 (rwb_integration) | Created by the V0001 baseline; the loading of the JOB-10 and JOB-11 rows is Not specified in the source documents (GAP-0650; ASM-1079) |
| `outbox_event` | PLT library, created in rwb_integration | Created by the library migration in the same schema; written by the app story |
| `outbox_delivery` | PLT library, created in rwb_integration | Created by the library migration; read by the relay and the delivery read |
| `processed_event` | PLT library, created in rwb_integration | Created by the library migration; the inbox of the consumed event |
| `idempotency_key` | PLT library, created in rwb_integration | Created by the library migration; the stored response of the two POST operations |
| `decision_record` | PLT library, created in rwb_integration | Created by the library migration; published to `rwb.decision-record.v1` |

The release applies the `rwb_integration` migration of this key and no other: no ACE view, no other service's table and no lake object is created, altered or read (DP-01, DP-05, DP-15, DP-17).

#### 12.8 Contract fakes

None. No fake is deployed. The MFT endpoint of the smoke run is the infrastructure stub of RWB-P2-E1007-INF, and the contract fakes of the consumed services are in-process test doubles of the app story and of RWB-P2-E1007-CON.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The four admin operations are the app story's; the probes are cluster-internal |
| Kafka | 0 published, 1 type consumed through 1 group | `rwb.integration.events.v1` provisioned with retry and `.dlt`; `rwb.source-data.events.v1` the only subscription; `rwb.decision-record.v1` published by the library |
| Temporal | 1 workflow, 6 activities, 0 Schedules | Worker on `rwb-integration` with a pinned build ID, worker versioning and KEDA scaling |
| File | 2 interfaces | INT-14 WIN and INT-25 buyer tape through the endpoint values of RWB-P2-E1007-INF; no data lake and no inbound folder |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_integration` only and reads no other schema | none |
| DP-02 | `recovery_svc` login | One login per service, carried as a secret reference | none |
| DP-03 | DecisionLogWriter, decision log | The local record library is deployed with the relay and publishes to `rwb.decision-record.v1` | H RWB-PLT-E1027-CON; build against a fake until published |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE grant, no view and no route in this release | none |
| DP-07 | Reference data, LOV | The interface rows and the lists stay reference data; no chart value carries them | H RWB-PLT-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The topic with its retry and `.dlt` topics, the inbox and the relay | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue and worker versioning from the kit; no Schedule and no Quartz job | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The release declares no REST path and no client of its own | none |
| DP-16 | `recovery.integration.adapter` | The release exposes the rwb-integration contract and adds no path of its own | C RWB-P2-E1007-CON |
| DP-17 | Data lake, INT-19, INT-20 | No lake target, route or delivery row is deployed; INT-19 and INT-20 are removed with no target in this service; JOB-13 and JOB-15 are gone | none |
| DP-19 | Screen, ace-web | The ingress registers the service base for the gateway-bff edge; no screen is deployed | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-integration/` overlay | API deployment, worker deployment, config map, secret references, probes, task queue, namespace, build ID, KEDA rule and flag |
| `helm/rwb-integration/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, build ID, consumer group name, intervals, endpoint references (ASM-1085) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration step, topic step, window check, smoke run, promotion |
| Migration step | The `rwb_integration` sequence from the V0001 baseline; a target schema other than `rwb_integration` is refused |
| Topic step | `rwb.integration.events.v1` with its retry and `.dlt` topics, the producer ACL and the consumer ACLs of the requesting services |
| Window step | Confirms the two Airflow windows and that no Schedule is registered for either |
| Dashboards | The six series of section 11 with the three dimensions |
| Alerts | Four rules, each with a message identifier or its placeholder and one runbook entry |
| Runbook | Five entries: held file, parked item, stuck retry, unreachable endpoint, lagging group |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-001 | A request is held because the ACE batch of the business date is not complete | Held-file alert naming the interface, the business date and the source date | Platform on-call and the data steward, ticket |
| MSG-P2-001 | An item moved to EXCEPTION after its last allowed attempt | Failed-file alert naming the interface, the business date, the attempt count and the build ID, with the count of items in EXCEPTION | Platform on-call, page |
| Not specified in the source documents (GAP-0650; ASM-1085) | The consumer group of `rwb.integration.events.v1` or of `rwb.source-data.events.v1` lags past its threshold | Lag alert naming the group, the topic, the partition and the lag | Platform on-call, page in the 16:00 window, else ticket |
| Not specified in the source documents (GAP-0650; ASM-1086) | A file window did not start, or the endpoint refused every connection | Window and endpoint alert naming the interface, the window and the endpoint health | Platform on-call and the MFT team, ticket |

**Retry and offsets.** The file-level retry ladder is the `max_attempts` and `retry_intervals_min` of the interface row, applied by `OutboundFileWorkflow` as timers; the activity retry is the kit's three attempts with back-off and never multiplies the ladder. The deployment adds no retry of its own. Offsets are committed after the inbox row is marked, so a crash replays the `AceDataReady` handling and the inbox makes the replay harmless (DP-09).

**Rollback.** A release that fails the smoke run is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open workflows until they finish; items in RETRY are replayed from their history and the inbox makes the replay harmless. No data repair is needed, because the release writes no row of its own and the migration is additive.

**Feature switch.** `rwb.integration.file-adapters`. On: the worker polls `rwb-integration`, `deliverFile` accepts a request and the file path runs. Off: no worker, no item and no file; the flag is not a way to stop a running ladder, which is what the exception queue and the resend are for.

**Done when.** The chart renders for DEV, SIT and UAT with a pinned digest and the build ID, the migration step refuses a foreign schema, the topic and its retry and `.dlt` topics exist with their ACLs, the two windows are confirmed as Airflow's with no Schedule registered, the smoke run delivers one file, parks one item and resends it, the six series and the four alerts are published with their identifiers or placeholders and their runbook links, and the five runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A request is held because the ACE batch is not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-001 | An item is in the exception queue after its last allowed attempt | {item} was not delivered to {interface} after {count} attempts. It is in the exception queue. |
| MSG-GEN-006 | The endpoint is unreachable and the attempt is retried | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-005 | A resend is accepted in the smoke run | Saved. |
| Identifier pending | The consumer group lags past its threshold | Not specified in the source documents (GAP-0650; ASM-1085) |
| Identifier pending | A file window did not start, or the endpoint refused every connection | Not specified in the source documents (GAP-0650; ASM-1086) |

MSG-P1-001 and MSG-P2-001 use the Error and Message Standard v4 wording. The other business texts are the legacy ones and are unchanged. The lag alert and the window alert have no identifier in the source set, so both carry the placeholder until the Error and Message Standard names them. An alert payload names counts, interface codes, business dates, attempt counts, group names and the build ID only, never an address, an identity number or a file content.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboards, SCR-09 Exception queue through the gateway-bff composite route, and the runbook. SCR-09 is served by the app story and the route of RWB-PLT-N001-CON; the deployment only registers the ingress path. The Temporal Web UI stays behind Entra ID: RW-PLATADM operates and RW-AUDIT reads, and payloads are decoded only through the codec server under break-glass. SCR-44 Interface and job monitor is not used for this service, because the release registers no job of its own and the relay is a platform interval.

States. SCR-09: loading as set in Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-2995). SCR-44: empty, loading, error and no access: Not specified in the source documents (CG-ALL-2996).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E1007-OPS-01 | AC1 | NFR | The chart renders for three environments with a pinned digest, the build ID, the login reference and worker versioning; a foreign migration target is refused; the worker polls only `rwb-integration` |
| TC-P2-E1007-OPS-02 | AC2 | NFR | The topic with its three retry topics and its `.dlt`; producer and consumer ACLs; a fourth topic refused; the only subscription is `rwb.source-data.events.v1` |
| TC-P2-E1007-OPS-03 | AC3 | NFR | A synthetic 16:00 window and a synthetic per-lot window started through the Airflow call; no Schedule registered; a repeated call builds no second file |
| TC-P2-E1007-OPS-04 | AC4 | NFR | One held request and one item failing its last attempt raise the two alerts with MSG-P1-001 and MSG-P2-001, one runbook link each, and no personal data |
| TC-P2-E1007-OPS-05 | AC5 | NFR | The six series with the three dimensions; a held file, a parked item and a lag visible before the alerts |
| TC-P2-E1007-OPS-06 | AC6 | NFR | Five synthetic conditions map to five runbook entries; the smoke run delivers, parks and resends one file with no duplicate and restores the environment |
| TC-P2-E1007-OPS-07 | §12 operations, events and activities | Contract | The consumption of AceDataReady on rwb.source-data.events.v1, the publication of FileDelivered and FileFailed on the topic, and the two POST operations through the ingress; synthetic payloads only |
| TC-P2-E1007-OPS-08 | §12.7 tables | Boundary | The rwb_integration migration creates the §12.7 tables and no other table; a foreign-schema target is refused; no ACE view, other table or lake object is created or altered |
| TC-P2-E1007-OPS-09 | AC7; BR1 to BR12 of section 8 | NFR | Each business rule of section 8 is checked against the release: one login and schema, two topics, windows by Airflow, no lake, no ACE grant, no hard-coded value, and no exhausted item deleted |
| TC-E1-007-05 | Retired inbound load; no AC | NFR | Asserts the absence of FileLoadAdapter, FileCheckRunner, RecordLoader, the inbound folder listing, DQ-057, DQ-059, the missing-file run row, JOB-09 File loads, interface_run and interface_signoff; the behaviour is ACE ingestion and the EV-27 AceDataLate alert; close when RWB-ACE-001 publishes its checks |
| TC-E1-007-06 | Retired inbound load; no AC | NFR | Asserts the same absences as TC-E1-007-05 for a file delivered twice; the behaviour is ACE ingestion and the EV-27 AceDataLate alert; close when RWB-ACE-001 publishes its checks |

### 17. Guardrails

- No business value in a values file: the file patterns, the attempt limits, the retry intervals, the owner role and the alert role are `interface_config` and reference-data rows, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the runbook or the workflow history: counts, identifiers, interface codes, business dates and build IDs only, and payloads stay encrypted.
- One login, one task queue and one schema per service: the release carries the rwb-integration login, polls `rwb-integration` and migrates `rwb_integration` only (DP-02, DP-15).
- The release deploys no ACE grant, no view, no inbound consumer and no lake object (DP-05, DP-17, BR12).
- The topic and its retry and `.dlt` topics exist with their ACLs before the worker starts (DP-09, BR2).
- No item is ever deleted: an exhausted item is EXCEPTION with a task for the owner role, and a resend sets PENDING with attempt count 0 (BR11).
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing smoke run never replaces a working build.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store (NFR-052).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly; source data is read through the ACE views and leaves through ACE's paths and the outbound adapters | No ACE grant and no ACE route in the release; the endpoint values of the infrastructure story | TC-P2-E1007-OPS-01, TC-P2-E1007-OPS-02 |
| REQ-DRI-007 | Every outbound file is logged, retried on a defined schedule and raised to a named owner in an exception queue | The retry ladder of the interface row, the exception-queue dashboards, the two alerts and the runbook | TC-P2-E1007-OPS-04, TC-P2-E1007-OPS-05, TC-P2-E1007-OPS-06 |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views; the Workbench runs no file load | No inbound consumer, no inbound folder and no lake object in the release | TC-P2-E1007-OPS-02, TC-P2-E1007-OPS-03 |
| Arch v5 slide 44 | JOB-11 is the outbox relay in every service; JOB-10 is a bank-Airflow file window executed by rwb-integration; JOB-13 and JOB-15 are removed | The relay deployment, the window step and the absence of a lake target | TC-P2-E1007-OPS-02, TC-P2-E1007-OPS-03 |
| DP-17 | No data lake | No lake target, route or delivery row in the values or the dashboards | TC-P2-E1007-OPS-01 |
| ADR-023 | Observability per service | The six series, the four alerts and the five runbook entries | TC-P2-E1007-OPS-04, TC-P2-E1007-OPS-05 |
| NFR-052 | Secrets in the key store and never in code or configuration | Secret references only, and the secret scan of the release | TC-P2-E1007-OPS-01 |

### 19. Out of scope

- The build of the outbound path, the retry policy, the inbox, the four admin operations and the workflow (RWB-P2-E1007-APP).
- The contract documents, the manifest, the event schemas and the fakes (RWB-P2-E1007-CON); this story only deploys and gates them.
- The MFT/SFTP endpoints, the PGP keys, the key store, the network rules, the staging area and the budgets (RWB-P2-E1007-INF).
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The topic provisioning, the schema registry and the `.dlt` retention as platform components (RWB-PLT-EVT, RWB-PLT-TE006-CON); this story configures the ACLs and the group.
- The bank Airflow DAGs themselves and their ownership (bank platform team, for discussion); this story confirms the windows and registers no Schedule.
- The real cross-service journey of the path with all services live (RWB-ITG-E1007-ITG).
- The exact cluster topology, node pools, replica counts, lag thresholds and probe timings, which are set per environment by the platform team (GAP-0650).
