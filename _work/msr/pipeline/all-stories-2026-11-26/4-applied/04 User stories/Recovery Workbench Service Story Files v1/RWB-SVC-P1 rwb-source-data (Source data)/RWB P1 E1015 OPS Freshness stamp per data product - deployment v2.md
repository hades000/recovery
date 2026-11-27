# RWB-P1-E1015-OPS Freshness stamp per data product

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1015-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | L-P1-I |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-015 for rwb-source-data. The freshness capability is deployed as the api and worker of the service with its own login, its listener and KEDA scaling on `v_ace_batch_status`, its topic with retry and `.dlt`, one cut-off Schedule per data product, the configuration rows behind `expected_by`, `refresh_cycle` and the product-to-source map, the feature flag until RWB-ACE-001 lands, the dashboards and alerts of the legacy story and its runbook (DP-02, DP-09, DP-10, DP-15). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-E1015-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **rwb-source-data's freshness capability deployed as an api and a worker from the service template, with its own login and schema migration job, its probes, its listener on `v_ace_batch_status` with KEDA scaling, the topic `rwb.source-data.events.v1` with a retry and a `.dlt` topic, one cut-off Schedule per data product registered from `data_product.expected_by`, the configuration rows and the feature flag that gate it, the dashboards and alerts of the legacy story, and a runbook with the capacity it needs**, so that **every daily job chain starts on a complete ACE batch in every environment and an operator can see and act on a late, failed or duplicated batch without reading code**.

### 2. Business rationale

In the legacy story the freshness step is a Quartz trigger and an in-process listener inside one deployable; a missing trigger or a stopped listener silently stops every daily job behind it, and the only signal is a job exception. In the target the capability is a helm release with two workloads, its own schema, login, topic and queue (DP-02, DP-09, DP-10, DP-15). Deployment is therefore part of the capability: an unregistered cut-off Schedule leaves a product never flagged stale, a topic without a dead-letter path loses `AceDataLate` and the stale banner never reaches the screen, and no alert on `duplicate_count` hides a listener that replays the same batch. This story makes the freshness pipeline observable and repeatable, so the app story can be proven in SIT and the on-call rota can operate it.

The capability also carries a guard that has to be visible in operations: the daily completeness gate is the one thing standing between a half-loaded ACE day and a published case list (BR8 in the app story). A gate that holds silently is worse than a gate that fails loudly, so the hold is alerted with MSG-P1-001 and named in the runbook.

### 3. Preconditions

- The service template, chart skeleton and pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The observability platform provides the dashboard, the alert rules and the runbook link convention (RWB-PLT-OBS, ADR-023).
- The three environments DEV, SIT and UAT exist with the parameter scope of LOV-ENVIRONMENT.
- RWB-P1-E1015-CON is baselined, so the chart, the provisioning step and the Schedule registration render from the published contract rather than from a local choice.
- The product-to-source map, the refresh cycles and the expected-by values are available as reference rows loaded through the rwb-case reference-data contract (DP-07); the cut-offs beyond 08:00 and MON 08:00 are Not specified in the source documents (GAP-0494; ASM-0686).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image, runs the unit and contract tests, scans the image and the dependencies, and publishes one Helm chart version from the same commit.
2. The chart deploys an api workload and a worker workload with the `rwb_source_data` login, the migration job on the service's own Flyway sequence and the probes; the migration job runs before the deployment is marked ready.
3. The provisioning step creates `rwb.source-data.events.v1` with its retry topic and its `.dlt` topic, the consumer group of the listener and the Temporal task queue `rwb-source-data` in namespace `rwb-recovery`.
4. The worker starts the `BatchStatusListener` against `v_ace_batch_status`; KEDA scales the worker on the lag and depth of the listener's own work queue.
5. The Schedule registration step reads `data_product` for the source-fed products and creates or updates one cut-off Schedule per product at `expected_by`, in Asia/Bangkok, with overlap policy SKIP and the catch-up window.
6. The configuration step confirms the reference rows behind `expected_by`, `refresh_cycle` and the product-to-source map, and the property `rwb.dataengine.freshness.alert-channel`.
7. The feature switch `rwb.dataengine.freshness-stamp` is published off, and turned on only when RWB-ACE-001 and the view are reported deployed.
8. The dashboards are published: stamps written, products stale, gate results, listener lag, event lag, duplicate count, Schedule fires and workflow failures.
9. The alerts are wired to the message IDs of section 14 and to the runbook entries, and the capacity plan is set as values.
10. A smoke step posts a synthetic business date to the ready signal in a test namespace and checks that the gate answer and the probes are healthy.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod leaves the service and the pipeline marks the release failed | None | AC1 |
| X3 | The listener stops and the batch view is never read | The listener-lag alert fires on the stalled offset and the runbook entry is opened | MSG-GEN-006 | AC2 |
| X4 | The topic is missing its retry or `.dlt` topic | The provisioning step fails the release; the relay refuses to start | None | AC3 |
| X5 | The Schedule registration is rejected by the namespace | The release fails; a product would otherwise never be checked at its cut-off | None | AC4 |
| X6 | A cut-off Schedule fires while the previous run is still open | The run is skipped by the overlap policy; the skip is counted, not alerted | None | AC4 |
| X7 | A product is stale at its cut-off | The alert carries MSG-P1-001 with the product and the date, and the runbook entry for the cut-off | MSG-P1-001 | AC6 |
| X8 | The same COMPLETED batch row is read again | `duplicate_count` rises; the alert fires above its threshold and names the source and the date | None | AC6 |
| X9 | Products stay STALE past the threshold | The stale-duration alert fires with the product list and the last complete business date | MSG-P1-001 | AC6 |
| X10 | The gate holds a business date | The hold alert fires with the product and the source that hold it, and the case list stays as published | MSG-P1-001 | AC6 |
| X11 | The feature switch is off and a read arrives | The response carries no stamp rather than a guessed one; the state is visible on the dashboard | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the observability platform; no application code is built here |
| Negotiable | Replica counts, resource sizes, KEDA thresholds, alert thresholds and the catch-up window are environment values, not story decisions |
| Valuable | Makes the freshness pipeline deployable, observable and repeatable, and makes a silent gate hold impossible |
| Estimable | One chart with two workloads, one pipeline stage, one migration job, two probes, one provisioning step, one registration step, one configuration step, two dashboards and six alert rules |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the listener scales, the topic and its retry path exist, the Schedules are registered, the alerts fire on a synthetic metric |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-source-data freshness capability

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT and the namespace is rwb-recovery

  Scenario: AC1 The chart deploys the api and the worker with the migration job (new, D-RCV-60)
    Given the rwb-source-data Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then it declares one api workload and one worker workload, each with a readiness and a liveness probe
    Then it declares the rwb_source_data login and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_source_data before the deployment is marked ready
    Then no replica count, resource size, KEDA threshold or catch-up window is hard-coded in the template

  Scenario: AC2 The listener reads v_ace_batch_status and the worker scales on it (new, D-RCV-60)
    Given the worker deployment and its KEDA scaler
    When a synthetic batch row is written to v_ace_batch_status and the listener lag rises
    Then the listener starts AceIngestCheckWorkflow for that source system and business date
    Then the worker scales out on the lag and back in when the queue is empty
    Then a second delivery of the same row starts no second workflow run for that source system and business date
    Then the listener-lag series is on the dashboard and the stalled-offset alert fires when the lag stops moving

  Scenario: AC3 The topic and its dead-letter path are provisioned (new, D-RCV-60)
    Given the provisioning step for rwb-source-data
    When it runs against the environment
    Then the topic rwb.source-data.events.v1 exists with its retry topic and its .dlt topic
    Then the consumer groups of rwb-case, rwb-payment, rwb-deviation and rwb-writeoff are declared for AceDataReady, and the alert and banner consumers for AceDataLate
    Then the shared topic rwb.decision-record.v1 is reused as provided and is not recreated
    Then the Temporal task queue rwb-source-data is registered in namespace rwb-recovery
    Then the outbox relay and the listener are configured with the retry topic and the .dlt topic

  Scenario: AC4 One cut-off Schedule per data product is registered and fires (new, D-RCV-60)
    Given the Schedule registration step and the data_product rows of the environment
    When it runs
    Then one cut-off Schedule exists for each source-fed product DP01, DP02, DP05, DP06, DP07, DP11 and DP13
    Then each Schedule fires at its expected_by value in Asia/Bangkok, 08:00 or MON 08:00 for the seeded rows, with overlap policy SKIP and the catch-up window
    Then a second run for the same business date is skipped and the skip is counted
    Then no product without sources has a cut-off Schedule, and no cadence is written in a template

  Scenario: AC5 The configuration rows and the feature switch are in force (new, D-RCV-60)
    Given the reference rows behind expected_by, refresh_cycle and the product-to-source map, and the property rwb.dataengine.freshness.alert-channel
    When the environment is provisioned
    Then every source-fed product reads its cut-off and its sources from those rows and no value is in code
    Then the feature switch rwb.dataengine.freshness-stamp is off until RWB-ACE-001 and the view are reported deployed
    Then with the switch off a freshness read answers no stamp and no job is held on a guessed one
    Then with the switch on the same read answers the stamp of the last complete business date

  Scenario: AC6 The dashboards, the alerts and the runbook cover the legacy signals (new, D-RCV-60)
    Given the published dashboards and runbook
    When a synthetic run is replayed with a stale product, a failed batch, a repeated batch, a long stale duration and a held gate
    Then each condition raises the alert that carries MSG-P1-001 with the legacy text and the product and date fields
    Then the duplicate_count alert fires above its threshold and names the source system and the business date
    Then the stamps-written, stale-product, gate-result, listener-lag, event-lag and Schedule-fire series are on the dashboard
    Then every alert links one runbook entry with the check, the owner role and the recovery step, and the capacity per environment is stated as a values entry
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_source_data` login and no other service's credential | DP-02; Arch v5 slide 29 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_source_data` and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every topic has a retry topic and a `.dlt` topic; a consumer never acknowledges an event it could not process | DP-09; Arch v5 slide 11 |
| BR4 | A cut-off Schedule is registered per source-fed product from `data_product.expected_by`, with overlap policy SKIP and a catch-up window; a cadence is never a value in a template or in code | DP-10; Arch v5 slide 44 |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, KEDA thresholds, alert thresholds and the catch-up window come from values files and parameters | DP-06; Template and Rules §R7.2 s17 |
| BR6 | An alert carries a message ID and the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | The feature switch keeps the capability off until the ACE batch record and the view exist; with the switch off no stamp is guessed and no job is held on one | DL43; legacy RWB-E1-015 section 13 |
| BR8 | The service writes only schema `rwb_source_data` and reads ACE only through the `recovery.v_ace_*` views | DP-01, DP-05 |
| BR9 | The deployment carries no personal data into a log, a dashboard series, an alert payload or the runbook: product codes, source codes, dates, counts and durations only | CTL-11; ADR-023 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version and both probes answer | Ready |
| Ready | Switch off | The environment is provisioned before RWB-ACE-001 lands | Ready, capability dark |
| Ready, capability dark | Switch on | RWB-ACE-001 and the view are reported deployed and the smoke run passes | Ready, capability live |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the Schedules are unchanged | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning, registration and configuration steps, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning, the Schedule registration rights and the feature switch |
| ACE database administrator | Owns the `rwb_source_data` schema, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments |
| Data steward (RW-DATASTEW) | Receives the stale and gate-hold alerts; confirms the reference rows behind the cut-offs and the map |
| On-call operator | Runs the runbook entries and opens an incident when a stale product or a gate hold persists |

The per-service login name used by the chart is Not specified in the source documents (GAP-0493; ASM-0685); the chart references "the `rwb_source_data` login (DP-02)" through a secret reference and never a literal name.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts of the api and the worker, KEDA thresholds, resource requests and limits, probe paths and timings, log level, feature switches |
| Schema | `rwb_source_data`, migrated by the per-service Flyway sequence; `data_product_load` and `data_product` plus the library objects |
| Views | `recovery.v_ace_batch_status` and the other `v_ace_*` views, read-only through the `rwb_source_data` login |
| Topics | `rwb.source-data.events.v1` with retry and `.dlt`; `rwb.decision-record.v1` reused as provided |
| Queue | Temporal task queue `rwb-source-data` in namespace `rwb-recovery` |
| Schedules | One cut-off check per source-fed data product, from `data_product.expected_by` |
| Dashboard series | stamps written, products stale, stale duration, gate results COMPLETE and HOLD, listener lag, event lag, duplicate count, Schedule fires, skipped runs, workflow failures, switch state |
| Runbook entries | cut-off missed, batch failed, repeated batch, long stale duration, gate hold, listener stalled, migration failure, probe failure, switch left off |
| Secrets | The `rwb_source_data` login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |

The stamp columns the dashboards date a product by are the ones the app story writes: `source_extracted_at` from `started_at` and `loaded_at` from `completed_at` (GAP-0492; ASM-0684), so a series never dates a stamp by a column the API does not read.

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class, the exact probe timings and the KEDA thresholds) is Not specified in the source documents (GAP-0494; ASM-0686); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded.

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the three operations of the contract baseline behind gateway-bff: `GET /api/recovery/source-data/v1/data-products/freshness`, `GET /api/recovery/source-data/v1/freshness` and `POST /api/recovery/source-data/v1/business-days/{date}/ready`. Owner rwb-source-data (P1). The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Access check before a stamp is returned; 2 s client budget (DP-11) |
| POST | The rwb-case reference-data contract | P3 rwb-case | The reference rows behind the cut-offs, the cycles and the map (DP-07) |

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | Topic plus retry topic and `.dlt` topic; outbox relay |
| `rwb.source-data.AceDataLate.v1` | `rwb.source-data.events.v1` | Same topic, same retry and `.dlt` path |

#### 12.4 Events consumed

| Event | Topic | Provisioning |
|---|---|---|
| None | None | The capability polls `v_ace_batch_status`; the listener's work queue is internal and no consumer group of another service is created |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| AceIngestCheckWorkflow | Workflow, one run per source system and business date | `rwb-source-data` | Worker deployment with the build ID of the release |
| stampProducts, markStale | Activities | `rwb-source-data` | Registered by the same worker |
| publishAceDataReady, publishAceDataLate | Activities (event library) | `rwb-source-data` | Registered by the same worker; the outbox relay is a separate process |
| checkDailyCompleteness | Activity | `rwb-source-data` | Registered by the same worker; called by the reconciliation workflow |

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| One cut-off check per source-fed data product, DP01, DP02, DP05, DP06, DP07, DP11 and DP13 | At `data_product.expected_by` in Asia/Bangkok; overlap policy SKIP; catch-up window | The release registers or updates each Schedule from the `data_product` rows and fails if the namespace rejects it | The legacy Quartz trigger per product |

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| data_product_load, data_product | P1 (`rwb_source_data`) | Created by the per-service Flyway sequence in the migration job |
| outbox_event, processed_event | PLT library, created in `rwb_source_data` | Created by the same migration job; used by the relay and the listener |
| decision_log_entry | P7 (`rwb_decision`) | Not created, not read and not granted here (DP-01) |

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-access WireMock | Runs in the pipeline and in the SIT smoke profile so the release can start without rwb-access |
| rwb-case reference-data WireMock | Same, carrying the two seeded cut-offs and the product-to-source map |
| rwb-decision WireMock | Same, carrying the inputs snapshot fixture of the app story's AC3 |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed in the deployment path | Freshness reads and the ready signal; authorise and reference data; one hop, 2 s |
| Kafka | 2 published, 0 consumed | `rwb.source-data.events.v1` with retry and `.dlt`; `rwb.decision-record.v1` reused |
| Temporal | 1 workflow, 5 activities, 7 Schedules | AceIngestCheckWorkflow on `rwb-source-data` |
| File | None | The release reads no file; values files are build inputs, not runtime data |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-source-data/` | Chart with the api and worker deployments, service, migration job, config map, secret references, probes, KEDA scaler and the Schedule registration hook |
| `helm/rwb-source-data/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, KEDA thresholds, probe timings, log level, feature switches, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Topic `rwb.source-data.events.v1` with retry and `.dlt`, consumer groups, task queue `rwb-source-data` in namespace `rwb-recovery` |
| Schedule registration | One cut-off check per source-fed product from `data_product`, idempotent create or update, overlap policy SKIP and catch-up window |
| Configuration step | The reference rows behind `expected_by`, `refresh_cycle` and the product-to-source map, and the property `rwb.dataengine.freshness.alert-channel` |
| Dashboards | Stamps written, stale products and duration, gate results, listener lag, event lag, duplicate count, Schedule fires and skips, workflow failures, switch state |
| Alerts | Six rules, each with a message ID and one runbook entry |
| Runbook | Nine entries: cut-off missed, batch failed, repeated batch, long stale duration, gate hold, listener stalled, migration failure, probe failure, switch left off |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running and the Temporal worker has polled; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database. Exact paths and timings are values.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_source_data` with the `rwb_source_data` login, as a pre-deploy job with a backoff limit; a failed job blocks the rollout and the release.

**Alert mapping carried over from the legacy story.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-001 | A product is stale at its cut-off, or the gate holds a business date | Cut-off and gate alert with the product and date fields | Data steward queue, ticket |
| None (duplicate count) | `duplicate_count` above its threshold on one product and business date | Repeated-batch alert with the source system and the business date | Platform on-call, ticket |
| None (stale duration) | A product STALE past the threshold with no later COMPLETED batch | Long-stale alert with the product list and the last complete business date | Data steward and platform on-call, page |
| MSG-GEN-006 | The store or the view is unavailable, or the listener has stalled | Dependency alert with the object and the trace identifier | Platform on-call, page |

The legacy story's stale warning to the case owner is carried by the panel and by `AceDataLate`, not by a second alert; the alert here is the operations side of the same condition, and its text is copied unchanged.

**Capacity.** The worker is sized on the number of source systems times the batch frequency, not on the case volume: one workflow run per source system and business date for stamping, plus one per source-fed product at its cut-off, with the reconciliation activity of the neighbouring story sharing the same queue. The per-environment capacity (replica counts, KEDA thresholds, resource requests and limits, and the maximum concurrent workflow runs) is a values entry, and its numbers are Not specified in the source documents (GAP-0494; ASM-0686).

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer, the topic with its retry path and the queue are verified by a test, the worker scales on the listener lag, one Schedule per source-fed product is registered and fires once per business date, the six alerts fire on synthetic metrics, the switch is proven off and on, and the runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A product is stale at its cut-off, or the gate holds a business date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | The store or the view is unavailable, or the listener has stalled | {system} is not available. Your request is queued and will be retried. |
| MSG-GEN-001 | A malformed product code or date reaches a read | Enter {field}. |
| MSG-P4-002 | Read without Case record R | You cannot {action} here. Your role does not include it. |

The texts are copied unchanged from the legacy story; the deployment adds the alert routing and the runbook link, never a new wording.

### 15. Screens and states

The deployment serves SCR-03 Case record, state Read only, whose data panel shows each product's business date and load time, and state Stale input, which shows MSG-P1-001 next to a stale product, behind the gateway-bff composite route (DP-19). The operator-facing surfaces of this story are the pipeline run view, the release view, the two dashboards and the runbook. The composite route specification and the panel field list are Not specified in the source documents (GAP-0494; ASM-0686); the deployment registers the route target and the health check of the freshness endpoints only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-015-09 | AC1, AC3; regression evidence for legacy Access | NFR | The chart renders for DEV, SIT and UAT with pinned digest, the login reference and the migration job; a refused read is counted, not paged |
| TC-E1-015-01 | AC2, AC3 | NFR | ALS batch row for 2026-11-30 in the SIT view; listener lag rises and falls; one workflow run |
| TC-E1-015-02 | AC4, AC6 | NFR | No COMPLETED ALS row at 08:00; test clock on the DP01 cut-off Schedule; the stale alert |
| TC-E1-015-03 | AC1, AC6 | NFR | Decision for RW-2026-000101 reading DP01 and DP06; the event-lag panel |
| TC-E1-015-04 | AC3, AC6 | NFR | ALS batch row FAILED at 05:20; the failed-batch runbook entry |
| TC-E1-015-05 | AC2, AC6 | NFR | Same COMPLETED row delivered twice; duplicate count 1 and the repeated-batch alert above its threshold |
| TC-E1-015-06 | AC3 | NFR | Late ALS batch at 08:40 after the stale flag; the retry path and the .dlt topic |
| TC-E1-015-07 | AC4 | NFR | ALS batch at 07:59; the DP01 Schedule fires at 08:00 and skips the second run |
| TC-E1-015-08 | AC4 | NFR | Weekly DP06 batch on Monday; the MON 08:00 Schedule fires on Thursday and the run is not stale |
| TC-E1-015-10 | AC5, AC6 | NFR | EFS batch FAILED at the 08:00 cut-off; the gate-hold alert with DP05 and EFS |
| TC-E1-015-11 | AC5 | NFR | Every source COMPLETED for 2026-11-30; the switch off and on |
| TC-E1-015-12 | AC4, AC6 | NFR | CCMS COMPLETED 2026-11-27; SVAF only to 2026-11-20; the long-stale alert |

This story owns no legacy acceptance criterion, so the twelve rows above are the legacy test cases of RWB-E1-015 with their IDs kept in legacy order; the Covers column names this story's own criteria, because the deployment is what each case now exercises: the chart, the listener and its scaling, the topic and its dead-letter path, the Schedules, the configuration and the switch, and the alerts with the runbook. The legacy level "System" maps to "NFR" and "Access" to "NFR". The criteria themselves are proven in RWB-P1-E1015-APP for AC3 and AC8 and are listed as regression evidence here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in a values file: the expected-by times, the refresh cycles, the product-to-source map and the alert channel are reference rows and parameters, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, workflow inputs or the runbook: product codes, source codes, dates, counts and durations only (DP-09, ADR-023).
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: the listener reads `v_ace_batch_status` through the `rwb_source_data` login and writes nothing to ACE (DP-05).
- No cross-schema read and no cross-schema key: the service writes only `rwb_source_data`, holds no grant elsewhere and creates no constraint into another schema (DP-01, DP-02).
- One login per service; the chart carries the `rwb_source_data` login reference and no other service's credential.
- Every topic has a retry topic and a `.dlt` topic, and the listener dedupes through the inbox (DP-09).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.
- The switch is off until the ACE batch record exists, and a read with the switch off answers no stamp rather than a guessed one (DL43).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-009 | Every data product carries a freshness stamp from the ACE batch record; every decision records the freshness of the data it used | The worker and the listener, the stamps-written series, the cut-off Schedules | TC-E1-015-01, TC-E1-015-02, TC-E1-015-03 |
| FEAT-RDF-14 | Stamp each data product with its freshness | The cut-off Schedules, the stale-product series and the MSG-P1-001 alert | TC-E1-015-06, TC-E1-015-07, TC-E1-015-08 |
| FEAT-DRI-12 | Carry a freshness stamp on every decision input | The event-lag panel and the `AceDataReady` consumer groups | TC-E1-015-03 |
| BR-P1-014-4 | No data job starts until every source it reads is complete | The gate-hold alert and the runbook entry | TC-E1-015-10 |
| ADR-023 | Observability per service | Two dashboards, six alerts and the runbook | TC-E1-015-05, TC-E1-015-12 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | One cut-off Schedule per product, registered from data | TC-E1-015-07, TC-E1-015-08 |

### 19. Out of scope

- The application code of the stamp, the stale flag, the gate, the listener and the panel (RWB-P1-E1015-APP).
- The contract documents, the contract jar and the fakes as published artefacts (RWB-P1-E1015-CON); this story only deploys the test copies.
- The platform topic provisioning implementation, the Temporal cluster and the observability platform (platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The exact cluster topology, node pools, replica counts, KEDA thresholds and probe timings (GAP-0494).
- The table design and the logical model of `rwb_source_data` (RWB-P1-E1001-APP and the DB stories of the service epic).
- The ACE batch record and the view behind it (RWB-ACE-001, RWB-P1-E1069-APP); this story only consumes them.
- The composite route specification and the screen field list (platform edge story and RWB-P1-E1015-APP).
