# RWB-P1-E1011-OPS Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1011-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P1-G |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-008, FR-P1-010, FR-P1-018, FR-P1-019, FR-P1-020, FR-P1-021, FR-P1-022, FR-P1-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-011 for rwb-source-data. The reconciliation deploys as one api and one Temporal worker on task queue `rwb-source-data` in namespace `rwb-recovery`, scaled by KEDA on backlog and started by `rwb.source-data.AceDataReady.v1` or by the rerun path (DP-10; Architecture v5 slides 15 and 44). The lake extract job, the 07:30 Power BI refresh and the shared Quartz scheduler are removed from the release (DP-17; GAP-0495; ASM-0687). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the reconciliation of rwb-source-data deployed as one api and one worker from the service template, with its chart and values, its Flyway migration job, the Temporal worker and its build ID, the KEDA scaling rule on the task queue backlog, the `AceDataReady` consumer group with its retry and dead-letter path, the rerun path bound to `ReconciliationWorkflow`, the four parameters as data, the two legacy alerts mapped to the new signals, the dashboards on `reconciliation_result` and a runbook**, so that **the daily reconciliation runs predictably in every environment and an operator can see and act on a held case list or a failed run without reading code**.

### 2. Business rationale

The legacy story depended on a Quartz job in a shared job table, a shared schema and a lake extract that a report read at 07:30. In the target a service is a Helm release built by one pipeline, with its own schema, login and task queue, and a job is either a Temporal Schedule or an event-started workflow (DP-02, DP-10, DP-15). Deployment is therefore part of the capability: a worker that polls no queue, a consumer without a dead-letter path or an alert that only fires on a job exception silently leaves a case list held, and the business only learns of it when a team works an old list.

This story makes the run observable and repeatable: one artefact promoted through the environments, one worker scaled on the queue, one rerun path with an idempotency key, one alert per failure class, and a dashboard built on `reconciliation_result` instead of a lake file (DP-17). It also carries the two parameters that decide a break and the two that belong to the sibling slices, so that no environment value is a constant in an image.

### 3. Preconditions

- The service template, chart skeleton and pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace exist, and KEDA is installed on the cluster (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions a topic with a retry topic and a `.dlt` topic, and the `rwb.source-data.events.v1` topic is owned by this service's event story (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The platform error envelope and the message catalogue are in force, so an alert carries a message ID and its agreed text.
- The three environments DEV, SIT and UAT exist with the parameter scope of `LOV-ENVIRONMENT`, and the parameter catalog of RWB-P3-E1042-CON is reachable from each.
- The ACE database login `rwb_source_data` exists with SELECT on the eight `recovery.v_ace_*` views and no privilege in `public` (DP-02, DP-05; RWB-P1-E1069-DB).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from a commit, runs the unit, component and contract tests, scans the image and the dependencies, and promotes the same artefact through DEV, SIT and UAT.
2. The chart deploys the api and the worker with the `rwb_source_data` login reference, the migration job and the two probes; the migration job runs the per-service Flyway sequence before the deployment is marked ready.
3. The worker is registered with the build ID of the release on task queue `rwb-source-data`, and the KEDA rule scales it on the queue backlog and on the consumer lag of the `AceDataReady` consumer group.
4. The provisioning step creates the consumer group for `rwb.source-data.AceDataReady.v1` with its retry topic and `.dlt` topic, and checks that the inbox table is migrated; it registers no Temporal Schedule, because the step is event-started and the daily fallback belongs to `DailyCaseList` of RWB-P1-E1002-CON.
5. The rerun path is bound: `POST /admin/jobs/{jobId}/rerun` with an Idempotency-Key starts `ReconciliationWorkflow` for the business date when the job code is the reconciliation and the batch record shows the date complete.
6. The parameter check reads `recon.tolerance.pct`, `recon.treatment.days`, `recon.payment.days` and `case.entry.dpd` from the catalog and fails the release if one is missing for the environment; no value is written into a values file.
7. The dashboards and the two alert rules are published, each alert linked to one runbook entry.
8. A smoke run posts a synthetic business date to the workflow in a test namespace and checks the run record, the probes and the two read operations.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready, the rollout stops and no traffic reaches the new version | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod leaves the service and the release is marked failed | None | AC1 |
| X3 | The worker polls no queue or a stale build ID | The release fails the worker check; the run would otherwise never start | None | AC2 |
| X4 | The consumer group lacks its retry or `.dlt` topic | The provisioning step fails the release and the consumer refuses to start | None | AC3 |
| X5 | A rerun is posted for a date the batch record does not show complete | 409 and no workflow start; the runbook names the batch owner | MSG-P1-001 | AC4 |
| X6 | A product breaks the tolerance and the publish is held | The alert carries MSG-P1-012 with the product, the date, the variance and the percent | MSG-P1-012 | AC6 |
| X7 | A view is unavailable during the run | The run is FAILED, no row is written for the date, and the alert carries MSG-GEN-006 naming "ACE database" | MSG-GEN-006 | AC6 |
| X8 | A parameter is missing for the environment | The release fails the parameter check and names the parameter and the environment | None | AC5 |
| X9 | The queue backlog crosses the scaling threshold | KEDA adds a worker; the run continues from history and no work is lost | None | AC2 |

X1 to X4 and X8 are deployment paths; X5 to X7 are run paths; X9 is the scaling path. No new message identifier is introduced: MSG-P1-012, MSG-P1-001 and MSG-GEN-006 are the legacy ones and keep their text.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the event platform and the parameter catalog; no application code is built here |
| Negotiable | Replica counts, resource sizes, the scaling threshold and the alert windows are environment values |
| Valuable | Makes the run deployable, observable and repeatable, and gives the operator one rerun path and one alert per failure class |
| Estimable | One chart, one pipeline stage, one migration job, two probes, one worker registration, one provisioning step, one rerun binding, four dashboards panels, two alerts and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the worker registers, the topic and consumer exist, the rerun starts one run, the alerts fire on a synthetic metric |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-source-data reconciliation

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart deploys the api and the worker with its migration job (new, D-RCV-60)
    Given the rwb-source-data chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release runs the migration job on the per-service Flyway sequence in schema rwb_source_data before the deployment is marked ready
    Then the release declares the rwb_source_data login reference and no other service's credential
    Then the readiness and liveness probes answer after the migration without a database write

  Scenario: AC2 The Temporal worker is registered and KEDA scales it (new, D-RCV-60)
    Given the worker deployment of the release
    When the worker starts
    Then it polls task queue rwb-source-data in namespace rwb-recovery with the build ID of the release
    Then the KEDA rule scales the worker on the queue backlog and the consumer lag, with a minimum of one worker per environment
    Then a synthetic backlog of runnable work adds a worker and no task is lost when the worker restarts

  Scenario: AC3 The AceDataReady consumer is provisioned and no Schedule is registered (new, D-RCV-60)
    Given the provisioning step of the release
    When it runs against the environment
    Then the consumer group for rwb.source-data.AceDataReady.v1 exists with its retry topic and its .dlt topic
    Then the inbox table is present and the consumer dedupes on the event id
    Then no Schedule and no Quartz job is registered by this release, and the daily fallback is the DailyCaseList Schedule of RWB-P1-E1002-CON

  Scenario: AC4 The rerun path starts one run per business date (new, D-RCV-60)
    Given a held case list for 2026-11-30 and a reconciliation job that is not running
    When the platform administrator posts POST /admin/jobs/{jobId}/rerun with an Idempotency-Key
    Then one ReconciliationWorkflow starts for 2026-11-30 and the response carries the job
    Then a replay with the same key returns the stored response and starts nothing
    Then a rerun for a date the batch record does not show complete is refused with 409 and MSG-P1-001

  Scenario: AC5 The four parameters are read as data and never as values (new, D-RCV-60)
    Given the parameter check of the release
    When it reads the catalog for the environment
    Then recon.tolerance.pct, recon.treatment.days, recon.payment.days and case.entry.dpd are present with a version
    Then the release fails and names the parameter and the environment when one is missing
    Then no value of the four appears in a chart, a values file or an image

  Scenario: AC6 The two alerts fire with their message IDs and every alert links one runbook entry (new, D-RCV-60)
    Given the published alert rules and the runbook
    When a synthetic run holds the publish for SSME and a second run fails on the ACE database
    Then the hold raises the alert that carries MSG-P1-012 with the product, the date, the variance and the percent
    Then the failure raises the alert that carries MSG-GEN-006 naming "ACE database"
    Then each alert links one runbook entry with the check, the owner role and the recovery step, and neither pages on a single refused read

  Scenario: AC7 The dashboards read reconciliation_result and the release keeps no lake path (new, D-RCV-60)
    Given the published dashboards
    When a run completes for 2026-11-30
    Then the panels show rows written per rec_code and product_group, the variance, the tolerance, the publish state and the orphan count
    Then no panel reads a lake extract and no release step writes a file (DP-17)
    Then the capacity panels show run duration, rows per run and worker count against the queue backlog
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_source_data` login and no other service's credential | DP-02; Arch v5 slides 11 and 29 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_source_data` and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every consumer group has a retry topic and a `.dlt` topic, and the consumer never acknowledges an event it could not process | DP-09; Arch v5 slide 42 notes |
| BR4 | The reconciliation is event-started; no Temporal Schedule and no Quartz job is registered by this release, and the daily fallback is `DailyCaseList` of RWB-P1-E1002-CON | DP-10; Arch v5 slide 44 |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, the scaling threshold and the alert windows come from values files and parameters | DP-06; Template and Rules §R7.2 s17 |
| BR6 | An alert carries a message ID with its agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | The rerun requires an Idempotency-Key and starts one run per business date; a date the batch record does not show complete is refused with 409 | DP-09; TSD P1 v3 T-A.2 |
| BR8 | The service writes only schema `rwb_source_data` and reads no other service's tables | DP-01 |
| BR9 | No lake path exists in the release: no extract job, no lake target, no Power BI refresh (DP-17) | Arch v5 slides 2 and 37; DP-17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart, the migration job and the worker check pass | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version and both probes answer | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker re-registers with the new build ID | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the worker registration, the provisioning, the rerun binding, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the rerun right (Platform administration U) |
| ACE database administrator | Owns schema `rwb_source_data`, the login, its grants on the views, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the runbook entries and opens an incident when MSG-GEN-006 persists or a held publish is not cleared by the rerun |
| RW-PLATADM | Reads and operates the run in the running service, not in the cluster |

The chart carries the login as a secret reference and never a literal name; the login is `rwb_source_data` (DP-02; Architecture v5 slide 29).

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, api and worker replica counts and ranges, resource requests and limits, probe paths and timings, log level, feature switches, KEDA backlog and lag thresholds |
| Schema | `rwb_source_data`, migrated by the per-service Flyway sequence; `reconciliation_result`, `case_list_row`, `data_product_load`, `interaction` and the four extension tables |
| Topics | `rwb.source-data.events.v1` consumed through one consumer group with a retry topic and a `.dlt` topic; no topic published by this story |
| Queue | Temporal task queue `rwb-source-data` in namespace `rwb-recovery`, one worker deployment |
| Rerun | `POST /admin/jobs/{jobId}/rerun` with an Idempotency-Key; the stored response lives in `idempotency_key` |
| Parameters | `recon.tolerance.pct`, `recon.treatment.days`, `recon.payment.days`, `case.entry.dpd`; read from the catalog, never written in a values file |
| Dashboard series | rows written per `rec_code` and `product_group`, variance and tolerance, publish state RELEASED or HELD, orphan count, run duration, rows per run, worker count and queue backlog |
| Runbook entries | held publish, failed run on a view, batch not complete, worker not polling, migration failure |
| Secrets | The `rwb_source_data` login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |

The cluster topology detail (node pools, exact replica counts, resource sizes, zone spread, ingress class and probe timings) is Not specified in the source documents (GAP-0497; ASM-0689); the chart exposes them as values and this story fixes only their names and the rule that they are never hard-coded.

### 12. Contract

#### 12.1 REST operations provided

The api of this release serves the two reconciliation reads on base `/api/recovery/source-data/v1`: `GET /admin/reconciliation/results` (API-P1-003) and `GET /admin/reconciliation/results/{resultId}`, owner rwb-source-data (P1), access Platform administration R. The rerun operation `POST /admin/jobs/{jobId}/rerun` (API-P1-002) is published by RWB-P1-E1002-CON and is bound here to `ReconciliationWorkflow`; this story deploys it and does not redefine its shape. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| POST | the case query operation of the rwb-case contract | P3 rwb-case | The exclusion count of REC-01 at run time; 2 s client budget (DP-11) |
| GET | the parameter read of the rwb-case contract | P3 rwb-case | The four parameters and their version |
| GET | the reference-data read of the rwb-case contract | P3 rwb-case | `LOV-PRODUCT` and `LOV-REC-RESULT` |

#### 12.3 Events published

None. `rwb.source-data.events.v1` and its two events belong to RWB-P1-E1013-APP; this release provisions the consumer side only.

#### 12.4 Events consumed

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | One consumer group for rwb-source-data with the inbox, a retry topic and a `.dlt` topic; the message starts `ReconciliationWorkflow` for the business date |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `ReconciliationWorkflow` | Workflow, one run per business date, workflow ID `recon-{businessDate}` | `rwb-source-data` | Worker deployment with the build ID of the release; started by the event or by the rerun |
| `reconciliation` | Activity | `rwb-source-data` | Registered by the same worker; mTLS to the Temporal frontend |

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| None | — | This release registers no Schedule and no Quartz job; the step is event-started and the daily fallback is the `DailyCaseList` Schedule of RWB-P1-E1002-CON (DP-10) | JOB-04 Daily reconciliation, now an event-triggered workflow |

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| `reconciliation_result`, `case_list_row`, `data_product_load`, `interaction` | P1 (`rwb_source_data`) | Created or extended by the per-service Flyway sequence in the migration job |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_source_data` | Created by the same migration job; used by the consumer and the stored rerun response |

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| RWB-P1-E1002-CON fake | Runs in the pipeline and in the SIT smoke profile: a `case_list_row` set, an `AceDataReady` event and the rerun answer |
| RWB-P3-E1042-CON fake | Runs in the pipeline and the SIT smoke profile with the four parameters |
| RWB-P3-E1043-CON fake | Same, with `LOV-PRODUCT` and `LOV-REC-RESULT` |
| View fixture | Same, with the eight views and a failing `v_ace_account` stub for AC6 |

The fakes are test-only workloads and are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed in the deployment path | Result reads; case query, parameters and reference data; one hop, 2 s |
| Kafka | None published, 1 consumed | `rwb.source-data.AceDataReady.v1` with retry and `.dlt` |
| Temporal | 1 workflow, 1 activity, no Schedule | `ReconciliationWorkflow` and `reconciliation` on `rwb-source-data` |
| File | None | No extract and no lake path in the release (DP-17) |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is the deployment pattern of this story: a shared Quartz step becomes an event-started workflow with one worker and a KEDA rule. DP-17 is a removal that the release proves: no extract job, no lake target, no report refresh. DP-19 is registered only as the route target of the admin surface that calls 12.1.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-source-data/` | Chart with the api and worker deployments, service, migration job, config map, secret references and probes |
| `values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replica ranges, resources, probe timings, log level, scaling thresholds, feature switches |
| Pipeline stage | Build, unit, component and contract tests, image and dependency scan, chart publish, promotion of one artefact |
| Worker registration | Task queue `rwb-source-data` in namespace `rwb-recovery`, build ID of the release, KEDA rule on queue backlog and consumer lag |
| Provisioning step | Consumer group for `rwb.source-data.events.v1` with retry and `.dlt`, inbox table check |
| Rerun binding | `POST /admin/jobs/{jobId}/rerun` starts `ReconciliationWorkflow` for the business date; no Schedule |
| Dashboards | Rows written, variance, tolerance, publish state, orphan count, run duration, rows per run, worker count and backlog |
| Alerts | Two rules, each with a message ID and one runbook entry |
| Runbook | Five entries: held publish, failed run, batch not complete, worker not polling, migration failure |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the worker has polled the queue and the consumer is joined; liveness answers healthy when the process is up and its loop responds. Neither probe writes to the database. Exact paths and timings are values.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_source_data` with the `rwb_source_data` login, as a pre-deploy job with a backoff limit; a failed job blocks the rollout and the release.

**Alert mapping carried over from the legacy story.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-012 | A product breaks the tolerance and the case list is held | Hold alert with product, business date, variance and percent | Data steward and platform on-call, ticket |
| MSG-GEN-006 | A view or the store is unavailable during the run | Failed-run alert naming the system and the business date | Platform on-call, page |

MSG-P1-001 is carried as the third signal of the runbook entry for a date the batch record does not show complete; it is raised by the completeness gate of RWB-P1-E1015-APP and is not a new alert of this story.

**Done when.** The chart renders in the three environments, the pipeline promotes one artefact, the migration job and both probes pass, the worker registers and scales on a synthetic backlog, the consumer group has its retry and `.dlt` topics, the rerun starts one run per date, the parameter check refuses a missing parameter, the two alerts fire on synthetic metrics and the five runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A product breaks the tolerance and the publish is held | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | The batch for the date is not complete | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | A view or the store is unavailable during the run | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A rerun by a role without Platform administration U | You cannot {action} here. Your role does not include it. |

The texts are copied unchanged from the legacy story; the deployment adds the alert routing and the runbook link, never a new wording.

### 15. Screens and states

The deployment serves no screen of its own. The admin result list is rendered through the gateway-bff composite route (DP-19) and the operator-facing surfaces of this story are the pipeline run view, the release view, the dashboard and the runbook. The states an operator sees are Ready, Rolling and Failed at the release, and PASS, BREAK and NOT_RUN with the publish RELEASED or HELD at the run. No Power BI report and no lake refresh exists.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-07 | AC4; the refused rerun | NFR | A rerun by RW-CASEOWN refused with MSG-P4-002; a rerun by RW-PLATADM accepted |
| TC-E1-011-01 | AC1, AC7 | NFR | Three environment renders with pinned digest; a clean run for 2026-11-30 on the dashboards |
| TC-E1-011-02 | AC6, AC7 | NFR | A synthetic hold for SSME and a failed run on the ACE database; the two alerts and their runbook entries |
| TC-E1-011-03 | AC5 | NFR | The four parameters present with a version; one removed and the release refused |
| TC-E1-011-04 | AC3, AC5 | NFR | No COMPLETED ALS row for 2026-11-30; the consumer group and the batch runbook entry |
| TC-E1-011-05 | AC4 | NFR | A rerun with a key, a replay with the same key, and a rerun on an incomplete date |
| TC-E1-011-06 | AC2, AC4 | NFR | Two workers and a synthetic backlog; one run per business date |
| TC-E1-011-08 | AC7 | NFR | An orphan count on the dashboard and no lake panel |
| TC-E1-011-09 | AC6 | NFR | A failing view in the fixture; MSG-GEN-006 naming "ACE database" |

This story owns no legacy acceptance criterion, so the nine rows are the legacy test cases of RWB-E1-011 listed against the new criteria the release proves: their IDs, their order and their data are kept, the legacy level "System" maps to "NFR" for a deployment test, and the Covers column names this story's own criteria only where the legacy case exercises a deployment artefact. The business outcome of each case is proven in RWB-P1-E1011-APP and end to end in RWB-ITG-E1011-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code or in a values file: the tolerance, the entry threshold and the waiting periods are parameters of the catalog, never a deployment value.
- No personal data in events, workflow inputs or logs and none in a dashboard series, an alert payload or the runbook: business dates, product groups, counts, amounts and durations only.
- One login per service: the chart carries the `rwb_source_data` login reference and no other service's credential (DP-02).
- ACE data only through the owner's contract or `recovery.v_ace_*` views: the release grants the login SELECT on the views and nothing in `public` (DP-01, DP-05).
- No cross-schema read and no cross-schema key: the migration job touches schema `rwb_source_data` only (DP-01).
- Every consumer group has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- No lake path: no extract job, no lake target and no report refresh in the release (DP-17).
- No secret is written into a values file, a chart template, a dashboard or the runbook; every secret comes from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count in `v_ace_account`, and every business key resolves to an ACE row | Worker registration, rerun binding, rows-written and variance panels | TC-E1-011-01, TC-E1-011-06, TC-E1-011-09 |
| REQ-RDF-008 | Reconciliation breaks and referential completeness are reported to the data product owner | MSG-P1-012 hold alert, orphan panel and the runbook entry | TC-E1-011-02, TC-E1-011-08 |
| REQ-CWC-004 | Exclusion rules are data | Parameter check and the consumed case query budget | TC-E1-011-03 |
| ADR-023 | Observability per service | Dashboard series, two alerts and five runbook entries | TC-E1-011-02, TC-E1-011-08 |

### 19. Out of scope

- The application code of the checks, the workflow, the activity and the read operations (RWB-P1-E1011-APP).
- The contract documents and the fakes as published artefacts (RWB-P1-E1011-CON); this story deploys the test copies only.
- The platform topic provisioning implementation, the Temporal cluster and KEDA itself (platform epics RWB-PLT-EVT and RWB-PLT-WF).
- The exact cluster topology, node pools, replica counts, resource sizes, probe timings and scaling thresholds (GAP-0497).
- The jobs and case-list operations and the `DailyCaseList` Schedule (RWB-P1-E1002-CON and RWB-P1-E1002-OPS).
- The lake extract job, the Power BI data set and the 07:30 refresh, which the target removes (DP-17).
- The dashboards and alerts of the sibling slices RWB-P3-E1011-APP, RWB-S5-E1011-APP and RWB-P6-E1011-APP.
