# RWB-P1-E1002-OPS Case list v1 with case ID, owner and queue - deployment v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1002-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P1-F |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1002-CON |
| Contract version | v1 (REST path /api/recovery/case/v1) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P1-E1002-OPS-22) |
| Integration dependencies | None |
| External dependencies | None |
| Size | Not specified in the source documents (DOR-RWB-P1-E1002-OPS-16) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017, FR-P1-018, FR-P1-019, FR-P1-020, FR-P1-021, FR-P1-022) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-002 for rwb-source-data. This story deploys the case-list capability: the api and worker deployments of `rwb-source-data`, the Temporal worker for `CaseListBuildWorkflow` with its KEDA scaling, the `DailyCaseList` Schedule registration at 07:15 Asia/Bangkok, the configuration of the three parameters by contract, the read path of rwb-case and rwb-reporting, the dashboards, the MSG-P1-001 and PUBLISHED NO alerts, the runbook and the capacity. It deploys no lake credential, no file adapter and no data set (DP-17; GAP-0485, ASM-0677). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 19 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **rwb-source-data deployed from the service template with its api and worker deployments, its Flyway migration job, its probes, its Temporal worker and KEDA scaling on the `rwb-source-data` task queue, the `DailyCaseList` Schedule registered at 07:15 Asia/Bangkok, the three case-list parameters read from the rwb-case parameter contract, the read path that serves the released case list to rwb-case and rwb-reporting, the dashboards and the MSG-P1-001 and PUBLISHED NO alerts, the runbook and the capacity plan**, so that **the case list of every business date is built, released and read predictably in every environment, and an operator can see and act on a late batch, a failed run or a date that never released without reading code or a lake file**.

### 2. Business rationale

The legacy story depends on a Quartz chain, one shared schema, an outbound file adapter and a Power BI refresh at 07:30. In the target a service is a Helm release built by one pipeline with its own schema, login, topic, queue and Schedules (DP-02, DP-10, DP-15), and the list is read by contract instead of by a lake file (DP-17). Deployment is therefore part of the capability: an unregistered Schedule means a business date with no list when the ACE event is late, a worker without KEDA means a backlog that misses the 07:30 measure, and an alert that fires only on an exception misses a date that is HELD by reconciliation and never releases. This story makes the run observable and repeatable so the app story can be proven in SIT and the on-call rota can operate it.

### 3. Preconditions

- The service template, chart skeleton and pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), and the Temporal workflow kit with namespace `rwb-recovery` is in place (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The ACE database administrator has created schema `rwb_source_data` and the login, with SELECT on the 30 `recovery.v_ace_*` views and no grant on any other schema (DP-02, DP-05).
- The platform error envelope, the message catalogue and the alert routing are in force, so an alert can carry a message ID.
- The three environments DEV, SIT and UAT exist with the parameter scope of LOV-ENVIRONMENT.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from one commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys the api deployment and the worker deployment with the `rwb_source_data` login reference, the pre-deploy migration job and the probes; the migration job runs on the per-service Flyway sequence before the rollout is marked ready.
3. The provisioning step creates the consumer group for `rwb.source-data.events.v1` with its retry and `.dlt` paths and registers the Temporal task queue `rwb-source-data` in namespace `rwb-recovery`.
4. The Schedule registration step creates or updates `DailyCaseList` at 07:15 Asia/Bangkok with overlap policy SKIP and the catch-up window, takes the 07:15 time from a parameter that is Not specified in the source documents (GAP-0487), and checks that `rwb.source-data.AceDataReady.v1` starts the same `CaseListBuildWorkflow` with workflow ID equal to the business date (GAP-0487).
5. The configuration step wires the three parameters through the rwb-case parameter contract and the reference lists through the reference-data contract; no parameter value is written into a values file.
6. The dashboards are published: runs started and finished, rows written, rows below entry, allocation complete, publish status by date, run duration, activity retries, consumer lag.
7. The alerts are wired to MSG-P1-001 and to the PUBLISHED NO check, and to the runbook entries.
8. A smoke step starts `CaseListBuildWorkflow` for a synthetic business date in a test namespace against the four fakes and checks the run record, the released date and the probes.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod is removed from the service and the pipeline marks the release failed | None | AC3 |
| X3 | The task queue is not registered or the worker build ID is not on the version set | The release fails; a case list would otherwise never be built | None | AC4 |
| X4 | The Schedule registration is rejected by the namespace | The release fails | None | AC5 |
| X5 | A run waits for a complete ALS batch | The alert carries MSG-P1-001 with the product and the last completed date, and the batch-gate runbook entry | MSG-P1-001 | AC6 |
| X6 | A date is reconciled but never released | The alert carries the PUBLISHED NO check with the business date and opens a ticket for the data steward | None (check PUBLISHED NO) | AC6 |
| X7 | A run fails on the case query contract | The failed-run alert carries the run ID and the contract name, and the runbook entry restarts through the rerun operation | None | AC6 |
| X8 | A role without Platform administration R lists the runs | The refused-read count is visible on the dashboard only and never pages the on-call rota | MSG-P4-002 | AC6 |
| X9 | A lake credential, a file adapter or a data set is found in the chart or the values | The pipeline fails the release on the DP-17 guard | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning and the workflow kit; no application code is built here |
| Negotiable | Replica counts, resource sizes and alert thresholds are environment values, not story decisions |
| Valuable | Makes the case-list run deployable, observable and repeatable in every environment, and removes the lake dependency from the release |
| Estimable | One chart, one pipeline stage, one migration job, two deployments, two probes, one provisioning step, one Schedule registration, six dashboard panels, four alert rules and five runbook entries |
| Small | Fits one sprint with the runbook and the capacity plan |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the queue is registered, the Schedule fires, the alerts fire on a synthetic metric |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-source-data case-list capability

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart deploys the api and worker with no lake artefact (new, D-RCV-60)
    Given the rwb-source-data Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the api deployment and the worker deployment, the pre-deploy migration job and the platform secret references
    Then the migration job runs the per-service Flyway sequence in schema rwb_source_data before the rollout is marked ready
    Then the release declares no lake credential, no file adapter, no outbound mount and no data-set job
    Then no replica count, resource size, Schedule cadence or parameter value is hard-coded in the template

  Scenario: AC2 The pipeline builds, tests and promotes one artefact (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit, component and contract tests and fails the build on a contract drift
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 Readiness and liveness probes answer (new, D-RCV-60)
    Given a running pod of the api and of the worker
    When the readiness probe is called before the migration job and the start-up window complete
    Then the pod is not marked ready
    When the readiness and liveness endpoints are called after start-up
    Then both answer healthy without a database write
    Then a failing dependency, including the ACE views or the rwb-case contract, is reported as not ready and never as live-and-broken

  Scenario: AC4 The Temporal worker, the task queue and KEDA scaling are in place (new, D-RCV-60)
    Given the provisioning step and the worker deployment
    When a synthetic backlog is queued on rwb-source-data in namespace rwb-recovery
    Then the worker polls only its own task queue with the release build ID on the version set
    Then KEDA scales the worker on backlog and returns to the minimum when the backlog clears
    Then CaseListBuildWorkflow, listEligibleAccounts and snapshot(page) are registered by the same worker
    Then the consumer group of rwb.source-data.events.v1 is configured with the retry topic, the .dlt topic and the inbox dedupe

  Scenario: AC5 The DailyCaseList Schedule is registered and fires once per business date (new, D-RCV-60)
    Given the Schedule registration step
    When it runs
    Then DailyCaseList is registered at 07:15 Asia/Bangkok with overlap policy SKIP and the one-business-date catch-up window
    Then a synthetic business date starts one run through the Schedule and one through rwb.source-data.AceDataReady.v1, and only one run exists for that date
    Then a second start for a running or complete date starts nothing and answers MSG-P1-011
    Then the run record carries rows written, rows below entry, allocation complete and publish status

  Scenario: AC6 Dashboards, alerts and the runbook cover the legacy controls (new, D-RCV-60)
    Given the published dashboard and the runbook
    When a synthetic run is replayed with a late batch, a failed case query call and a date held by reconciliation
    Then each condition raises the alert that carries MSG-P1-001 for the late batch, the run ID for the failure and the PUBLISHED NO check for the held date, with the legacy text where a message exists
    Then the refused-read count carries MSG-P4-002 and does not page the on-call rota
    Then every alert links one runbook entry with the check, the owner role and the recovery step
    Then the dashboard shows the publish status of every date of the last 30 days

  Scenario: AC7 The read path serves the released list to rwb-case and rwb-reporting (new, D-RCV-60)
    Given a released business date and a held business date
    When rwb-case reads the date operation for SCR-02 and rwb-reporting reads the paged rows for its measures, both through the gateway-bff composite route
    Then the released date answers its row count and its rows in the 19-column order within the 2 s budget
    Then the held date answers its status and no rows
    Then no reader is given a file path, a lake location or a data-set name
    Then the route target and the health check of the two read operations are registered and answer

  Scenario: AC8 The capacity plan covers the peak business date (new, D-RCV-60)
    Given the capacity plan of the service
    When it is checked against the peak figures of the case-list run
    Then it states the rows of a peak date, the pages served to rwb-case and rwb-reporting, the worker maximum and the database connection cap of the login
    Then the plan keeps the run inside the 07:30 measure with the worker at its maximum and the migration job idle
    Then the plan records no lake throughput and no file window, because both are removed

  Scenario: AC9 The release holds the business rules BR1 to BR6 and BR8 (new, D-RCV-60)
    Given the rendered release and the service code
    When the release is checked against the business rules of section 8
    Then the release uses only the rwb_source_data login reference and no other service credential
    Then the migration is the per-service Flyway sequence in rwb_source_data and runs before the rollout is ready
    Then every topic has a retry topic and a .dlt topic, and the consumer dedupes through the inbox
    Then DailyCaseList uses overlap policy SKIP with a catch-up window and takes the business date as its input
    Then no environment value is hard-coded and every alert carries its message ID where one exists, the agreed text and one runbook entry
    Then the service writes only schema rwb_source_data and reads ACE only through the recovery.v_ace_* views

  Scenario: AC10 A consumed call fails or does not answer (new, D-RCV-60)
    Given a synthetic run that consumes a call which fails or does not answer
    When the call fails or no answer arrives
    Then the run records the failure against its run ID and the business date is not released
    Then a failing dependency is reported as not ready and never as live-and-broken
    Then the failure raises the alert of AC6 with the run ID and links one runbook entry
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_source_data` login reference and no other service's credential | DP-02; Arch v5 slide 29 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_source_data` and runs before the rollout is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every topic has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox | DP-09; Arch v5 slide 11 |
| BR4 | A Temporal Schedule uses overlap policy SKIP with a catch-up window, and the event-started workflow takes the business date as its input | DP-10; Arch v5 slide 44 |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, thresholds, cadences and the three parameters come from values files and contracts | DP-06; Template and Rules §R7.2 s17 |
| BR6 | An alert carries a message ID where one exists, the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | A refused read is counted on the dashboard and never pages the on-call rota | MSG-P4-002 |
| BR8 | The service writes only schema `rwb_source_data` and reads ACE only through the `recovery.v_ace_*` views | DP-01, DP-05 |
| BR9 | The release carries no lake credential, file adapter or data-set job; a chart that does fails the DP-17 guard | DP-17; GAP-0485 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version, the worker has polled and both probes answer | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is on the version set | Ready |
| Ready | Migration job failed or the Schedule rejected | The schema is not at the expected version or the namespace refused the Schedule | Failed |
| Failed | Rollback | The previous chart version is redeployed; the Schedule is re-registered from the previous release | Ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning and Schedule registration steps, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the Schedule registration rights |
| ACE database administrator | Owns the `rwb_source_data` schema, the login, its grants and the migration job approval |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the runbook entries and opens an incident when the PUBLISHED NO check or MSG-P1-001 persists |
| RW-PLATADM | Reads and reruns the case list in the running service, not in the cluster |

The per-service login name used by the chart is the fixed name `rwb_source_data` (DP-02); the chart references it through a secret reference and never a literal password.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switches, environment name |
| Schema | `rwb_source_data`, migrated by the per-service Flyway sequence; `case_list_row`, `data_product_load` and the library objects |
| Topics | `rwb.source-data.events.v1` consumed with retry and `.dlt`; nothing published by this capability |
| Queue | Temporal task queue `rwb-source-data` in namespace `rwb-recovery` |
| Schedule | DailyCaseList at 07:15 Asia/Bangkok with overlap policy SKIP and the catch-up window |
| Parameters | `case.entry.dpd`, `recon.caselist.tolerance.pct` and `caselist.allocation.wait.until`, read through the rwb-case parameter contract and never held as deployment values |
| Dashboard series | runs started, runs finished, rows written, rows below entry, allocation complete, publish status by date, run duration, activity retries, consumer lag, refused reads |
| Runbook entries | late ACE batch, failed case query call, held date never released, Schedule not fired, migration failure |
| Secrets | The `rwb_source_data` login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and exact probe timings) is Not specified in the source documents (GAP-0487; ASM-0679); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded. There is no lake path, no extract file and no data-set refresh time to document (DP-17; GAP-0485).

The released rows are read by contract, not by file: GET /case-list/dates/{businessDate} answers the publish status and the row count, and GET /case-list/rows answers the paged rows; the column order is Not specified in the source documents (GAP-0485).

BR Field ID for each of the nine rows of the table above (Deployment values, Schema, Topics, Queue, Schedule, Parameters, Dashboard series, Runbook entries, Secrets): Not specified in the source documents (DOR-RWB-P1-E1002-OPS-7).

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the four operations of the contract baseline behind gateway-bff: `GET /api/recovery/source-data/v1/admin/jobs`, `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun`, `GET /api/recovery/source-data/v1/case-list/dates/{businessDate}` and `GET /api/recovery/source-data/v1/case-list/rows`. Owner rwb-source-data (P1). The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The open case accounts; 2 s client budget (DP-11) |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | Allocation state, owner and queue |
| GET | `/api/recovery/case/v1/parameters/{key}` | P3 rwb-case | The three case-list parameters with their version |
| GET | `/api/recovery/case/v1/reference-data/{lovCode}` | P3 rwb-case | LOV-PUBLISH-STATUS, LOV-PRODUCT and LOV-CASE-STATUS |

No operation of rwb-integration is consumed: the outbound file adapter of RWB-P2-E1007-CON is not deployed, because the publish path it served is removed (DP-17).

#### 12.3 Events published

None. This capability publishes no event; `AceDataReady` and `AceDataLate` on `rwb.source-data.events.v1` belong to RWB-P1-E1015-APP and are provisioned by its own release.

#### 12.4 Events consumed

| Event | Topic | Provisioning | Owner |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | Consumer group for rwb-source-data with the inbox, the retry topic and the `.dlt` topic; starts `CaseListBuildWorkflow` | rwb-source-data |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| CaseListBuildWorkflow | Workflow, one per business date, workflow ID = business date | `rwb-source-data` | Worker deployment with the release build ID on the version set |
| listEligibleAccounts | Activity | `rwb-source-data` | Registered by the same worker; mTLS to the Temporal frontend |
| snapshot(page) | Activity | `rwb-source-data` | Registered by the same worker; read only |

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| DailyCaseList | Daily at 07:15 Asia/Bangkok, with AceDataReady as the primary trigger; overlap policy SKIP; catch-up window one business date | The release registers or updates the Schedule and fails if the namespace rejects it | JOB-04 case list step and the 07:15 wait |

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| case_list_row, data_product_load | P1 (rwb_source_data) | Created by the per-service Flyway sequence in the migration job |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_source_data | Created by the same migration job; used by the consumer and the rerun operation |

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-case case query fake (RWB-P3-E1018-CON) | Runs in the pipeline and in the SIT smoke profile so the release can start without rwb-case |
| rwb-case allocation fake (RWB-P3-E1020-CON) | Same, answering allocation complete YES and NO |
| rwb-case parameters fake (RWB-P3-E1042-CON) | Same, with the three keys |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | Same, with the three lists |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 4 consumed in the run path | Case-list reads and admin jobs; case query, allocation, parameters and reference data; one hop, 2 s |
| Kafka | 0 published, 1 consumed | AceDataReady with retry and `.dlt`; inbox dedupe |
| Temporal | 1 workflow, 2 activities, 1 Schedule | CaseListBuildWorkflow, listEligibleAccounts, snapshot(page), DailyCaseList with KEDA on backlog |
| File | None | The release carries no file, no lake credential and no data-set job (DP-17) |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-source-data/` | Chart with the api deployment, the worker deployment, the service, the migration job, the config map, the secret references, the probes and the Schedule registration hook |
| `helm/rwb-source-data/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switches, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Consumer group and retry path for `rwb.source-data.events.v1`, task queue `rwb-source-data` in namespace `rwb-recovery` |
| Schedule registration | DailyCaseList at 07:15 Asia/Bangkok with overlap policy SKIP and the catch-up window; idempotent create or update |
| KEDA scaling | Worker scaled on the task-queue backlog with a minimum and a maximum from the values file |
| Dashboards | Six panels: run counts, run duration, rows written and below entry, publish status by date, activity retries, consumer lag |
| Alerts | Four rules: MSG-P1-001, PUBLISHED NO, failed run, refused read |
| Runbook | Five entries: late ACE batch, failed case query call, held date never released, Schedule not fired, migration failure |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the consumer is running, the worker has polled and the last view read answered; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database. Exact paths and timings are values.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_source_data` with the `rwb_source_data` login as a pre-deploy job with a backoff limit; a failed job blocks the rollout and the release.

**Alert mapping carried over from the legacy story.**

| Message ID or check | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-001 | The workflow waits for a complete ALS batch | Batch-gate alert with the product and the last completed date | Platform on-call, ticket |
| PUBLISHED NO | A date is reconciled but not released | Publish alert with the business date, the publish status and the run ID | Data steward, ticket |
| None (run failure) | A run fails on the case query contract or on the views | Failed-run alert with the run ID and the contract or view name | Platform on-call, page |
| MSG-P1-011 | A second start for a running or complete date | Counted on the dashboard and in the run log | No page |
| MSG-P4-002 | Read without Reporting R | Refused-read count on the dashboard | No page |

**Capacity.** The plan states, per environment, the rows of a peak date, the pages served to rwb-case and rwb-reporting, the worker minimum and maximum, the PgBouncer connection cap of the login and the run duration at maximum. The target is the legacy measure: the list built and released by 07:30 on 99 percent of days. No lake throughput and no file window appear in the plan, because both are removed (DP-17).

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer, the queue and the consumer group are verified by a test, KEDA scales on backlog, `DailyCaseList` is registered and fires once per business date, the four alerts fire on synthetic metrics, the capacity plan is reviewed and the five runbook entries are accepted by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The workflow waits for a complete ALS batch | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-011 | A second start for a running or complete date | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Read without Reporting R | You cannot {action} here. Your role does not include it. |

MSG-P1-001 carries the Error and Message Standard v4 text and the other texts are copied unchanged from the legacy story; the deployment adds the alert routing and the runbook link, never a new wording. The PUBLISHED NO and failed-run conditions have no message ID in the legacy story and keep none.

### 15. Screens and states

The deployment serves the SCR-02 Case list screen of rwb-case (Loading; empty; list; filtered; error: Not specified in the source documents (CG-ALL-2047); no access: Not specified in the source documents (CG-ALL-2047)) and the reporting screens of rwb-reporting, both through the gateway-bff composite route (DP-19). The operator-facing surfaces of this story are the pipeline run view, the release view, the dashboards and the runbook. This story registers the route target and the health check of the two case-list read operations only; the screen field list and the composite route specification belong to the edge and rwb-case stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-002-01 | AC1, AC8 | NFR | Chart renders for DEV, SIT and UAT with pinned digest, the login reference, the migration job and the capacity plan |
| TC-E1-002-02 | AC1, BR9 | NFR | Rendered manifests contain no lake credential, no file adapter, no mount and no data-set job |
| TC-E1-002-03 | AC2 | NFR | One pipeline run produces one image and one chart version and fails on a contract drift or a critical scan finding |
| TC-E1-002-04 | AC3 | NFR | Readiness is false before the migration and the start-up window, then true; liveness stays true; neither probe writes |
| TC-E1-002-05 | AC4 | NFR | Backlog on `rwb-source-data` scales the worker, the build ID is on the version set, the three activities are registered and the consumer group has retry and `.dlt` |
| TC-E1-002-06 | AC5 | NFR | DailyCaseList registered at 07:15 Asia/Bangkok and fired once for one business date; a second start answers MSG-P1-011 |
| TC-E1-002-07 | AC6 | NFR | Four synthetic conditions raise the four mapped alerts with the section 14 text and one runbook entry each |
| TC-E1-002-08 | AC7 | NFR | A released date and a held date answer through gateway-bff within 2 s; the held date returns no rows |
| TC-E1-002-09 | AC7, BR7 | Component | A refused read increments the dashboard count and raises no page |
| TC-E1-002-10 | AC1, AC6 | NFR | A held date appears on the publish-status panel for the last 30 days |
| TC-E1-002-11 | Access | Component | A role without Platform administration R is refused with MSG-P4-002 on the jobs operation |
| TC-E1-002-12 | AC4 | Component | Contract test: the operations, events and activities of section 12 match the catalogued contracts |
| TC-E1-002-13 | AC1 | NFR | Boundary test: each table of section 12.7 is created once by the migration job (ASM-3438) |
| TC-E1-002-14 | BR1 | Component | The release uses the `rwb_source_data` login reference and no other service credential |
| TC-E1-002-15 | BR2 | NFR | The per-service Flyway sequence in `rwb_source_data` runs before the rollout is ready |
| TC-E1-002-16 | BR3 | Component | Every topic has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox |
| TC-E1-002-17 | BR4 | Component | DailyCaseList uses overlap policy SKIP with a catch-up window and takes the business date as input |
| TC-E1-002-18 | BR5 | NFR | No environment value is hard-coded: replica counts, sizes, thresholds, cadences and the three parameters come from values files and contracts |
| TC-E1-002-19 | BR6 | NFR | An alert carries a message ID where one exists, the agreed text and one runbook entry |
| TC-E1-002-20 | BR8 | Component | The service writes only schema `rwb_source_data` and reads ACE only through the `recovery.v_ace_*` views |
| TC-E1-002-21 | AC9 | NFR | Release is checked against BR1 to BR6 and BR8: one login reference, Flyway order, retry and .dlt topics with inbox, SKIP schedule, no hard-coded values, alert content, schema and view access |
| TC-E1-002-22 | AC10 | Component | A synthetic consumed call fails or does not answer; the run records the failure, the date is not released and the AC6 alert is raised |

The 11 legacy TC IDs are kept in legacy order and character for character, with new Covers, because the deployment proves the same conditions as artefacts rather than as business outcomes: a row still named AC2 or AC9 of the legacy story where the legacy named it. The legacy Level "System" maps to "NFR" for the deployment checks, and "Access" to "Component".

### 17. Guardrails

- No business value in a values file: the entry threshold, the tolerance and the wait time are parameters read through the rwb-case contract, never deployment values (DP-06).
- No personal data in logs, dashboard series, alert payloads or the runbook: run counts, IDs, dates and durations only.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: the release holds SELECT on the 30 views and no grant on `public` (DP-02, DP-05).
- No cross-schema read and no cross-schema key: the migration job writes `rwb_source_data` only and never touches another schema (DP-01).
- Every topic has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.
- No lake credential, file adapter or data-set job is deployed, and the DP-17 guard fails a release that carries one.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-007 | Case list reconciled daily to the count of accounts at 90 days past due or more | Run counts and rows-written panels, DailyCaseList registration, capacity plan | TC-E1-002-01, TC-E1-002-06 |
| REQ-RDF-009 | Every screen and API that shows source data shows its fresh status | Publish-status panel by date, PUBLISHED NO alert | TC-E1-002-07, TC-E1-002-10 |
| REQ-DRI-007 | A delivery that fails after its retry limit is parked with a task for its owner | Failed-run alert and the rerun runbook entry | TC-E1-002-05, TC-E1-002-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Read path through gateway-bff within 2 s; the four consumed contracts | TC-E1-002-08 |
| ADR-023 | Observability per service | Six dashboard panels, four alerts and the runbook | TC-E1-002-07 |
| ADR-018 | No data lake; reporting from events | The DP-17 guard and the absent file window in the capacity plan | TC-E1-002-02 |

### 19. Out of scope

- The application code of the workflow, the activities and the contract controller (RWB-P1-E1002-APP).
- The contract documents, the contract jar and the fakes as published artefacts (RWB-P1-E1002-CON); this story deploys the test copies only.
- The platform topic provisioning implementation, the Temporal cluster and the KEDA operator (platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The exact cluster topology, node pools, replica counts, resource sizes and probe timings (GAP-0487).
- The reconciliation and the hold of the publish (RWB-P1-E1011-APP) and the freshness stamp (RWB-P1-E1015-APP).
- The SCR-02 case list screen and the reporting screens with their composite route specification (RWB-P3-E1002-APP and the edge story).
- The `rwb_source_data` schema design and the logical model of the P1 tables (RWB-P1-E1001-APP and the DB stories of the service epic).
- Any lake credential, extract file, outbound adapter, data-set job or 07:30 refresh, which DP-17 removes (GAP-0485).
- The end-to-end run of the legacy criteria AC1, AC3, AC4, AC5 and AC10 (RWB-ITG-E1002-ITG).
