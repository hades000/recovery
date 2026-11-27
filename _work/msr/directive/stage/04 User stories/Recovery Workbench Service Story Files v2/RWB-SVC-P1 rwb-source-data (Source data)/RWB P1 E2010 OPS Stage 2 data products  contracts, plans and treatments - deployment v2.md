# RWB-P1-E2010-OPS Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2010-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P1-V |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-16); squad sizes at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E2010-CON (must reach Done before build) |
| Contract version | /v1 (path version; exact contract version Not specified in the source documents (DOR-RWB-P1-E2010-OPS-23)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-006, FR-P1-024, FR-P1-025, FR-P1-030, FR-P1-031) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-010 for rwb-source-data. The stage 2 step was a stage of the `rwb-case` JOB-02 chain inside one deployable, so its deployment was the deployment of that chain. In the target the build is `Stage2ProductWorkflow` on task queue `rwb-source-data`, started by `rwb.source-data.AceDataReady.v1` and owning no Schedule, and it writes two snapshot tables in `rwb_source_data` (DP-01, DP-10, DP-15). This story deploys that build, proves the trigger, gates the flag, publishes five series and three alerts and writes the runbook. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2010-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the stage 2 product build of rwb-source-data deployed from one chart with a pinned digest and build ID, the worker that registers `Stage2ProductWorkflow` on `rwb-source-data`, the migration step that applies `rwb_source_data` and refuses another schema, the proof that the build starts from `rwb.source-data.AceDataReady.v1` and owns no Schedule, the flag `rwb.dataengine.stage2-products`, five dashboard series and three alerts each with its runbook entry**, so that **an operator can see a stage 2 build that did not start, a business date that was not stamped, a count break that held the publish or a run that failed, and prove that a rerun of the same date leaves no duplicate and that a failed release keeps the previous build**.

### 2. Business rationale

The legacy stage 2 step had no deployment of its own: it ran inside the rwb-case chain over one schema, so a stuck step showed up as a failed job run and an operator had the database in front of them. In the target the step is a workflow of its own service, started by an event, writing two tables in this service's schema, joined at read time to the ACE views, and its result is three facts an operator must be able to see: whether the build for the business date started, whether it was stamped, and whether the count check held it. Without this story the app story can pass its tests while the worker is unregistered, the event is consumed by nobody, the count break sits unread and DP04 turns stale with no alert (DP-10; Architecture v5 slide 44).

Deployment is also where the split is enforced operationally. The release carries the `rwb_source_data` login only, applies the `rwb_source_data` migration only, and reads no other service's schema and no ACE table directly: the contract and plan facts come through this service's own views, and the treatment and guarantee facts come through their contracts at run time (DP-01, DP-02, DP-05). The observability follows ADR-023 per service: five series with the environment, release and build ID as dimensions, three alerts each carrying a message ID, and three runbook entries.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The rwb-source-data baseline chart and login are deployed, with the REST base `/api/recovery/source-data/v1` and the relay of `rwb_source_data` (DP-02, DP-13).
- The Kafka event platform provides `rwb.source-data.events.v1` with its retry and `.dlt` topics and the ACLs of this service's principal (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The Temporal workflow kit and the `rwb-recovery` namespace exist, with worker versioning, the build ID provider and the payload codec (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The platform error envelope and the message catalogue are in force, so every alert can carry a message ID.
- The three environments DEV, SIT and UAT exist and the production namespace exists for the release date; the flag `rwb.dataengine.stage2-products` exists in the flag library.
- The chart of the app story is published with `Stage2ProductWorkflow` and its four activities, and the migration version that creates `dp_treatment` and `dp_guarantee_claim` sits on the service sequence (RWB-P1-E2010-APP; DP-15).
- The gateway-bff composite route for SCR-45 and SCR-03 is published (RWB-PLT-N001-CON, DP-19).
- The replica counts, the resource sizes, the lag and stale thresholds, the alert thresholds and the probe timings are environment values fixed by no source document (GAP-0513; ASM-0705).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the API deployment and the workflow worker with the `rwb_source_data` login reference, namespace `rwb-recovery`, task queue `rwb-source-data`, the payload codec and the build ID of the release.
3. The worker registration step confirms that `Stage2ProductWorkflow` and the activities `snapshot(page)`, `writeDp04Page`, `checkActiveCount` and `stampDp04` are registered on `rwb-source-data` and on no other queue.
4. The migration step applies the `rwb_source_data` sequence of this release, including the version that creates `dp_treatment` and `dp_guarantee_claim`, and refuses to run when the target schema is not `rwb_source_data`.
5. The trigger step confirms that the build is started by `rwb.source-data.AceDataReady.v1` and registers no Schedule for it, and publishes one synthetic event to prove the start.
6. The flag step sets `rwb.dataengine.stage2-products` from the values of the environment.
7. The dashboards are published with the five series and the environment, release and build ID as dimensions.
8. The three alerts are wired to their message identifiers and to their runbook entries: MSG-P1-002 for the count break, MSG-P1-001 for DP04 stale and MSG-GEN-006 for a workflow failure.
9. A smoke step writes DP04 for a synthetic business date in DEV, reads it back through the DP04 contract, and reruns the same date to prove that no duplicate row appears.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready, the pipeline stops, and no traffic and no offset is committed | None | AC1 |
| X2 | The migration target is a schema other than `rwb_source_data` | The step refuses the target and the release stops before any table is created | Pipeline error, no message id | AC1 |
| X3 | The worker registers the workflow on another queue, or registers no worker | The registration check fails the release and names the queue and the workflow | None | AC1 |
| X4 | The flag is off in an environment | The worker is not deployed, no build starts on a new `AceDataReady` and DP04 keeps its previous rows | None | AC3 |
| X5 | A synthetic `AceDataReady` starts no execution | The trigger check fails the smoke run and the workflow-failure alert condition is demonstrated on the synthetic event | MSG-GEN-006 | AC2, AC5 |
| X6 | The active count differs from the count written | The stamp is held, the break is listed and the count-break alert fires | MSG-P1-002 | AC5 |
| X7 | DP04 is not stamped by its expected-by time | The product turns stale and the stale alert fires | MSG-P1-001 | AC5 |
| X8 | A dashboard series is missing, or an alert carries no message ID or no runbook link | The observability check fails the release | None | AC4, AC5 |
| X9 | A new build is promoted while an execution of the business date is running | The old build drains its execution and the new build takes the next start; the dashboards show both build IDs | None | AC6 |

X1 to X3 are the deployment paths of the release; X4 to X7 are the four conditions the flag and the three alerts exist for; X8 is the observability gate; X9 is the worker-versioning path of the workflow kit.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the topic provisioning and the flag library; no application code is built here |
| Negotiable | Replica counts, resource sizes, thresholds and probe timings are environment values |
| Valuable | Makes a stage 2 build observable, provable and rerunnable before the Epic 3 screens depend on DP04 |
| Estimable | One chart, one worker registration, one migration step, one trigger step, five series, three alerts and three runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the worker registers, the migration refuses a foreign schema, an alert fires on a synthetic condition, the smoke run leaves one row per date |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the stage 2 product build for rwb-source-data

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-source-data is rwb-source-data
    Given the target environment is SIT

  Scenario: AC1 The chart, the worker and the migration step are deployed and pinned (new, D-RCV-60)
    Given the rwb-source-data chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release carries the build ID of the release commit
    Then the worker registers Stage2ProductWorkflow and its four activities on task queue rwb-source-data in namespace rwb-recovery and on no other queue
    Then the release declares the rwb_source_data login and no other service's credential
    Then the migration step applies the rwb_source_data sequence and refuses a target schema other than rwb_source_data
    Then worker versioning is enabled and a new workflow goes to the new build while the old build drains

  Scenario: AC2 The build is event-started and owns no Schedule (new, D-RCV-60)
    Given the deployed worker and the flag on
    When a synthetic rwb.source-data.AceDataReady.v1 for a synthetic business date is published
    Then Stage2ProductWorkflow starts once with the business date and the source of the event
    Then a duplicate of the same message starts no second execution and the hit count rises in the inbox
    Then the deployment registers no Schedule for the stage 2 build and no legacy Quartz trigger for it
    Then the trigger step fails the release when the event starts no execution

  Scenario: AC3 The flag turns the build on and off (new, D-RCV-60)
    Given the flag rwb.dataengine.stage2-products in the flag library
    When the flag is on in an environment
    Then the worker is deployed and a new AceDataReady starts a build
    When the flag is off in the same environment
    Then the worker is not deployed, no build starts, and dp_treatment and dp_guarantee_claim keep the rows of the last stamped date
    Then the flag value comes from the values file of the environment and never from code

  Scenario: AC4 The five dashboard series carry the environment, the release and the build ID (new, D-RCV-60)
    Given the published dashboard of the deployment
    When a synthetic build, a count break, a stale product and a failed execution are produced
    Then the dashboard shows the rows written per product, the load status per product, the count breaks, the stale products and the workflow failures
    Then each series carries the environment, the release and the build ID as dimensions
    Then a stale product and a failed execution are both visible on the dashboard before any alert is read

  Scenario: AC5 The three alerts carry their message ID and one runbook entry each (new, D-RCV-60)
    Given the published alert rules and the runbook
    When a count break, a stale DP04 and a failed execution are simulated
    Then the count break raises its alert with MSG-P1-002
    Then the stale DP04 raises its alert with MSG-P1-001
    Then the workflow failure raises its alert with MSG-GEN-006
    Then every alert links one runbook entry with the check, the owner role and the recovery step
    Then no alert threshold and no probe timing is hard-coded, and no secret appears in a values file, a dashboard or the runbook

  Scenario: AC6 The smoke run writes, reads and reruns one business date, and rollback keeps the previous build (new, D-RCV-60)
    Given the DEV environment and a synthetic business date
    When the smoke run publishes AceDataReady for that date
    Then dp_treatment and dp_guarantee_claim hold the rows of the date and the DP04 stamp is present
    Then the DP04 read through /data-products/{productCode}/records answers the rows of the date
    When the smoke run publishes the same event again for the same date
    Then the row count per table is unchanged and no duplicate record exists for the date
    When the release is rolled back
    Then the previous chart version and its build ID serve the queue and the smoke run passes on it

  Scenario: AC7 A retried or timed-out activity follows its chart-set policy and writes no duplicate (new, D-RCV-60)
    Given the deployed worker and the four activities of Stage2ProductWorkflow
    When an activity of the build fails and is retried, or exceeds its timeout
    Then the retry policy and the timeout come from the values file of the environment and are not hard-coded
    Then a retried activity runs again for the same business date and writes no duplicate row
    Then an activity that still fails or times out after the retries of that policy ends as a failed execution and raises the workflow failure alert with MSG-GEN-006

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given the deployed worker and a product of rwb_source_data at its current status
    When a status change that the model does not allow is submitted
    Then the change is refused and the status stays as it was
    Then no product row changes as a result of the refused change

  Scenario: AC9 A failing release never replaces the working build, and the deployment writes no stamp (new, D-RCV-60)
    Given the previous build in force and a release whose tests or smoke run fail
    When the release is promoted
    Then the previous build stays in force until the new build passes its tests and its smoke run
    When the row count of a business date matches
    Then the stamp of that date is present and was written by the freshness story, not by this deployment
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one task queue and one schema per service: the release carries the `rwb_source_data` login, polls `rwb-source-data` only and migrates `rwb_source_data` only | Architecture v5 slides 29 and 41; DP-02; DP-15 |
| BR2 | The stage 2 build is started by `rwb.source-data.AceDataReady.v1` and owns no Schedule; the freshness cut-off Schedules belong to RWB-P1-E1015-OPS | DP-10; Architecture v5 slide 44 |
| BR3 | Every worker carries the build ID of its release and worker versioning is enabled, so a new build takes new executions while the old build drains | Temporal and Drools design slide 11; RWB-PLT-E1071-CON |
| BR4 | Every alert carries a message ID and links one runbook entry with the check, the owner role and the recovery step | Template and Rules §R7.2 s14 |
| BR5 | No environment value is hard-coded: replicas, resources, thresholds, probe paths and timings and the flag come from a named chart value set per environment and from parameters; the fixture owner is named at the wave 2 entry check (GAP-0513) | Template and Rules §R7.2 s17 |
| BR6 | Dashboard series, alert payloads and the runbook carry counts, product codes, business dates, statuses and build IDs only, never a treatment amount, a claim amount or a personal value | ADR-023; Template and Rules §R7.2 s17 |
| BR7 | The release writes no ACE data and reads no other service's schema or table; the ACE facts are read through this service's own views and the treatment and guarantee facts through their contracts | DP-01; DP-05 |
| BR8 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run | DP-10 |
| BR9 | The stamp is written by the freshness story and never by this deployment; the deployment only proves that the stamp of a business date appears when the count matches | RWB-P1-E1015-APP; BR4 of the legacy story |

**Where each rule lives in the target.** BR1 is the chart, the values and the migration step. BR2 is the trigger step and the fact that the release registers no Schedule. BR3 is the worker versioning and the build ID of the release. BR4 is the alert wiring and the runbook. BR5 is the values files. BR6 is the series definition and the alert payload. BR7 is the migration scope and the ACLs. BR8 is the rollback rule. BR9 is the smoke run, which reads the stamp rather than writing it.

**Wave difference of the guarantee copy (GAP-2739).** The dated copy `dp_guarantee_claim` stays with rwb-source-data in `rwb_source_data` and the live claim record stays with rwb-guarantee in `rwb_guarantee`. This story is wave 2 and the claim record is wave 3: until the claim stories of wave 3 land, the build runs against the published fake of the claim read, which answers an empty list, so the DP04 guarantee part stays empty rather than stale. The DP04 release note records this wave difference as a dependency.

**Case link of the claim rows (GAP-2740).** The claim read answers every claim in the window with its `case_id`, and no case is resolved on that read. The References check, the data quality break list and the retry stay with RWB-P1-E2010-APP, which owns the case-existence answer of the DP04 build. This deployment adds no case-existence read, no consumed case contract and no dependency for it.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Worker registered and probes healthy | The worker polls `rwb-source-data` only and the registration check passes | Ready |
| Ready | Release superseded | A new chart version passes its tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open executions | Ready |
| Ready | Flag off | `rwb.dataengine.stage2-products` is turned off in the environment | Not deployed |
| Ready | Smoke run failed | The trigger, the read-back or the rerun step of the smoke run fails | Blocked |
| Blocked | Previous build restored | The previous chart version is redeployed with its build ID | Ready |

The DP04 freshness states LOADED and STALE and the workflow execution states RUNNING, COMPLETED and FAILED belong to the product and the app story; they are not states of this deployment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the registration step, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic ACLs, the consumer quotas and the flag library |
| Platform workflow owner | Owns the task queue, the namespace, the worker registration and the versioning policy |
| Platform event owner | Owns `rwb.source-data.events.v1`, its retry and `.dlt` topics and the schema registry |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the three runbook entries and opens an incident when a count break, a stale product or a failed execution persists |
| RW-DATASTEW, data steward | Reads the DP04 status and the breaks the alerts point at |
| RW-AUDIT, internal audit | Reads the runbook, the alert history and the release record |

The worker runs as the `rwb_source_data` service identity (DP-02), carried by the chart as a secret reference and never as a literal name. No credential and no personal name appears in a values file, a dashboard, an alert payload or the runbook.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, flag value | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Task queue | `rwb-source-data` in namespace `rwb-recovery`, polled by the rwb-source-data worker only | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Trigger | `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1`, consumed by this service's own inbox | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Schema | `rwb_source_data`, migrated by its own per-service Flyway sequence; this release applies the version that creates `dp_treatment` and `dp_guarantee_claim` | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Tables behind the series | `dp_treatment`, `dp_guarantee_claim`, `data_product_load`; the series read counts and statuses only | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Dashboard series | Rows written per product, load status per product, count breaks, stale products, workflow failures; dimensions environment, release, build ID | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Alerts | Three rules with one message ID and one runbook entry each: MSG-P1-002 for a count break, MSG-P1-001 for DP04 stale and MSG-GEN-006 for a workflow failure | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Runbook entries | Count break held the publish, DP04 stale, workflow failed or did not start; each with the check, the owner role and the recovery step | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Secrets | The `rwb_source_data` login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Test data | One synthetic `AceDataReady` for a synthetic business date, the 40-treatment fixture of the app story and one count break; the fixture owner is Not specified in the source documents (GAP-0513; ASM-0705) | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded (GAP-0513; ASM-0705).

**Probes.** Readiness answers healthy only after the worker has polled `rwb-source-data` once and has registered the workflow and its four activities; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database, starts an execution or commits an offset, and a failing dependency is reported as not ready, never as live-and-broken. The paths and timings are values of the environment.

### 12. Contract

#### 12.1 REST operations provided

None from this story. The DP04 branch of `GET /api/recovery/source-data/v1/data-products/{productCode}/records` is declared by RWB-P1-E2010-CON and implemented by RWB-P1-E2010-APP; this deployment exposes it through the chart and its ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None from the deployment. The worker calls the treatment and guarantee contracts and reads the ACE views at run time as the app story's client; the chart carries no REST client of its own, no composite route and no outbound call at start-up beyond the Temporal frontend and the Kafka brokers.

#### 12.3 Events published

None of its own. `rwb.source-data.events.v1` carries `AceDataReady` and `AceDataLate` from RWB-P1-E1015-APP, and this slice publishes neither; the smoke run publishes one synthetic `AceDataReady` as a test message on the topic and not as a service event.

#### 12.4 Events consumed

| Event type | Topic | Service | Deployment element |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | rwb-source-data | The listener and inbox of this service, starting `Stage2ProductWorkflow`; retry topic and `.dlt` routing on the topic |

The topic, its retry and `.dlt` topics and the event type are provisioned and owned by the platform event epic and by RWB-P1-E1015-APP; this deployment configures the consumption, the inbox and the trigger proof.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `Stage2ProductWorkflow` | Workflow, one execution per business date | `rwb-source-data` | Registered by the worker of this release, with the build ID and worker versioning; no Schedule |
| `snapshot(page)` | Activity | `rwb-source-data` | Registered by the same worker with the kit's retry policy |
| `writeDp04Page` | Activity | `rwb-source-data` | Registered with the same policy; idempotent by record ID and business date |
| `checkActiveCount` | Activity | `rwb-source-data` | Registered with the same policy |
| `stampDp04` | Activity | `rwb-source-data` | Registered with the same policy; calls the freshness stamp of RWB-P1-E1015-APP |

**Build ID and versioning.** The build ID is the one supplied by the workflow kit for the release commit; worker versioning is enabled and a new build takes new executions while the old build drains (BR3). The exact build ID format and the versioning policy are the platform's and are not restated here.

#### 12.6 Schedules

None. The deployment registers no Schedule: the build is started by `AceDataReady` and the freshness cut-off Schedules belong to RWB-P1-E1015-OPS and RWB-P1-E1015-APP (BR2; DP-10).

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| `dp_treatment` | P1 (`rwb_source_data`) | Created by the migration step of this release; the row counts feed the rows-per-product and count-break series; read for reporting only, never as the source of a treatment |
| `dp_guarantee_claim` | P1 (`rwb_source_data`) | Created by the same migration step; its row counts feed the same series |
| `data_product_load` | P1 (`rwb_source_data`) | Read for the load-status and stale-product series; written by RWB-P1-E1015-APP and never by this deployment |

The release applies the stage 2 migration of the app story and no other: no treatment table of another service, no guarantee table and no ACE table is created, altered or read directly (DP-01, DP-05, DP-15).

#### 12.8 Contract fakes

None. No fake is deployed. The contract mocks of the treatment and guarantee reads and the ACE account and plan fixture are in-process test doubles of the app story and of its contract tests; the smoke run of DEV calls the service's own contracts and the DEV stand-ins of rwb-case, rwb-guarantee and the ACE views, never a fake shipped by this release.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The DP04 record read is the app story's; the probes are cluster-internal |
| Kafka | 0 published, 1 type consumed | `rwb.source-data.events.v1` with the inbox, the retry topic and the `.dlt` routing |
| Temporal | 1 workflow, 4 activities, 0 Schedules | Worker on `rwb-source-data` with a pinned build ID and worker versioning |
| File | None | No file is read or written by the deployment |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_source_data` only and reads no other schema | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The ACE facts are read through this service's own views at run time, never from a public table | none |
| DP-07 | Reference data, LOV | The rwb-case reference-data contract is a run-time dependency of the worker, with its keeper library | H RWB-PLT-E1043-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue and the namespace come from the workflow kit; no Schedule is registered | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The release declares no REST path and no client of its own; the worker calls the contracts as the app story's client | none |
| DP-13 | `/api/recovery/v1` | The ingress serves `/api/recovery/source-data/v1` and no other base | none |
| DP-15 | V0001 baseline, migration | The per-service Flyway sequence of `rwb_source_data`; the migration step refuses another schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff serves SCR-45 and SCR-03; the deployment registers the route and no screen of its own | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-source-data/` overlay | API deployment, workflow worker, config map, secret references, probes, task queue, namespace, build ID and flag |
| `helm/rwb-source-data/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, build ID, thresholds (GAP-0513; ASM-0705) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration step, trigger step, smoke run, promotion |
| Registration step | `Stage2ProductWorkflow` and its four activities on `rwb-source-data`, with the build ID and worker versioning |
| Migration step | The `rwb_source_data` migration of this release; a target schema other than `rwb_source_data` is refused |
| Trigger step | Proves that `AceDataReady` starts the workflow and that no Schedule is registered |
| Dashboards | The five series of section 11 with the three dimensions |
| Alerts | Three rules, each with a message ID and one runbook entry |
| Runbook | Three entries: count break held the publish, DP04 stale, workflow failed or did not start |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-002 | The active count differs from the count written for the business date, so the stamp is held | Count-break alert naming the product, the business date, the check text and the build ID | Platform on-call and the data steward, ticket |
| MSG-P1-001 | DP04 is not stamped by its expected-by time | DP04-stale alert naming the product, the business date in use and the stale-since time | Platform on-call, page in the morning window, else ticket |
| MSG-GEN-006 | An execution of the build failed, or the event started none | Workflow-failure alert naming the workflow, the business date, the failure class and the build ID | Platform on-call, page |

**Rerun and idempotency.** A rerun of a business date is refused while an execution of that date is running (MSG-P2-006) and is otherwise started again on the same workflow ID pattern; `writeDp04Page` upserts by record ID and business date, so the rerun replaces the rows of the date and creates no duplicate. The smoke run proves that rule on one synthetic date (AC6).

**Rollback.** A release that fails the smoke run is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open executions until they finish; the rows of a stamped date are left as they are and the previous build reruns the date through the same upsert, so no data repair is needed.

**Feature switch.** `rwb.dataengine.stage2-products`. On: the worker and the listener are deployed, and a new `AceDataReady` starts a build. Off: no worker, no execution, and `dp_treatment` and `dp_guarantee_claim` keep the rows of the last stamped date.

**Done when.** The chart renders for DEV, SIT and UAT with a pinned digest and the build ID, the worker registers `Stage2ProductWorkflow` and its four activities on `rwb-source-data`, the migration step refuses a foreign schema, the trigger step proves the start from `AceDataReady` and registers no Schedule, the five series and the three alerts are published with their message IDs and runbook links, the smoke run writes and reads back one synthetic business date and reruns it without a duplicate, and the three runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | A count break held the stamp of the business date | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-001 | DP04 is stale after a build that did not run or did not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | The stage 2 build failed, or the treatment or guarantee contract was unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | A rerun is asked while the execution of the date is running | {job} is already running. Wait for it to finish before you run it again. |

The first three texts are the legacy texts carried unchanged, MSG-P2-006 carries the text of the Error and Message Standard v4, and each of the first three is the message ID of one alert. An alert payload names the product, the business date, the check, the failure class, counts and the build ID only, never a treatment amount, a claim amount or a personal value. Thai text for each message follows decision DL10; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard, SCR-45 Data quality through gateway-bff (loading, empty, list, refused) and the runbook. SCR-45 and SCR-03 are served by the app story and the composite route of RWB-PLT-N001-CON; the deployment only registers the route. SCR-03 states: loading; empty, error and no access: Not specified in the source documents (CG-ALL-2430). SCR-45 error and no access: Not specified in the source documents (CG-ALL-2432). SCR-44 Interface and job monitor is not used, because the deployment registers no job of its own and the build is event-started. SCR-44 states: empty, loading, error and no access: Not specified in the source documents (CG-ALL-2431). The Temporal Web UI stays behind the platform identity provider: RW-PLATADM operates and RW-AUDIT reads, and payloads are decoded only through the codec server under break-glass.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E2010-OPS-01 | AC1 | NFR | The chart renders for three environments with a pinned digest and the build ID; the worker registers on `rwb-source-data`; a foreign migration target is refused |
| TC-P1-E2010-OPS-02 | AC2 | NFR | One synthetic `AceDataReady` starts one execution; a duplicate starts none; no Schedule is registered |
| TC-P1-E2010-OPS-03 | AC3 | NFR | The flag on and off in one environment; the rows of the last stamped date are kept when it is off |
| TC-P1-E2010-OPS-04 | AC4 | NFR | The five series carry the three dimensions; a stale product and a failed execution are visible before the alerts |
| TC-P1-E2010-OPS-05 | AC5 | NFR | Three synthetic conditions raise the three mapped alerts, each with one runbook entry and no hard-coded threshold |
| TC-P1-E2010-OPS-06 | AC6 | NFR | A synthetic business date is written, read back through the DP04 record and rerun without a duplicate; rollback keeps the previous build |
| TC-P1-E2010-OPS-07 | AC1 | NFR | Each workflow, activity and event named in sections 12.4 and 12.5 is checked against its contract; the worker registers exactly those. Data: the workflow, the four activities and the one event of sections 12.4 and 12.5 |
| TC-P1-E2010-OPS-08 | AC1 | NFR | The migration applies the tables of section 12.7 and no other; a table outside the scope is refused. Data: the three tables of section 12.7 and one table of another service as the foreign target |
| TC-P1-E2010-OPS-09 | AC7 | NFR | A synthetic activity failure and a synthetic timeout are retried under the chart-set policy; no duplicate row is written |
| TC-P1-E2010-OPS-10 | AC8 | NFR | A status change the model does not allow is submitted; it is refused and no product row changes |
| TC-P1-E2010-OPS-11 | AC9, BR8, BR9 | NFR | A failing release keeps the previous build in force; a matching count shows the stamp written by the freshness story |
| TC-E2-010-01 | Legacy AC1, BR1, BR2, BR6, BR7; regression evidence for the deployed build of the snapshot and the ACE facts | End to end | 40 synthetic treatments, 12 plans, 9 approvals |
| TC-E2-010-02 | Legacy AC2, BR1; regression evidence for the deployed guarantee part | End to end | 5 TCG claims for existing cases |
| TC-E2-010-03 | Legacy AC3, BR5; regression evidence for the 403 mapping through the deployed ingress | End to end | RW-PHONECOL reads DP04 |
| TC-E2-010-04 | Legacy AC4, BR3; run by RWB-P1-E2010-APP; regression evidence for the References break of the deployed run | End to end | TCG claim for an unknown case ID |
| TC-E2-010-05 | Legacy AC5; regression evidence for the failed execution and the stale path of the alerts | End to end | The treatment contract answering with an error in the deployed environment |
| TC-E2-010-06 | Legacy AC6; regression evidence for the rerun of a stamped date | End to end | Step run twice for 2026-12-14 |
| TC-E2-010-07 | Legacy AC7, BR4; run by RWB-P1-E2010-APP; regression evidence for the count-break alert | End to end | The active count 41 against 40 rows |
| TC-E2-010-08 | Legacy AC8; run by RWB-P1-E2010-APP; regression evidence for the window of the deployed build | End to end | Changes at 23:59:59 and 00:00:00 |
| TC-E2-010-09 | Legacy Access, BR5; regression evidence for the refused DP04 answer as deployed | Component | RW-TRIBE calls the DP04 read with no DP04 access row; refused with MSG-P4-002 |

The eleven new test cases own this story's nine criteria at NFR level, because each one tests a deployment artefact rather than a business outcome; TC-P1-E2010-OPS-07 and -08 are the contract and boundary tests of sections 12.5 and 12.7. The nine legacy test case IDs, their Covers and their Data are carried onto the split as regression evidence; the legacy level "System" maps to "End to end" and "Access" to "Component". This story owns no legacy acceptance criterion: the business behaviour behind those rows is proven by RWB-P1-E2010-APP, and this story proves that the deployed build reproduces it. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

**DP04 integration harness (GAP-0392).** The gateway-bff composite DP04 record route path and merge order, and the harness environment, repository, seed pack, evidence format, retention and pass or fail gate, are Not specified in the source documents (GAP-0392). The Integration lead and the QA lead agree them at the wave 2 entry check, the route path and merge order with the platform edge story, and record the result in the DP04 harness pack before the first real-service run.

### 17. Guardrails

- No business value in a values file: the product code, the access roles, the expected-by time and the count tolerance are data rows and decisions, never a deployment value (DP-07).
- No personal data in logs, dashboard series, alert payloads, the runbook or the workflow history: counts, product codes, business dates, statuses, failure classes and build IDs only, and payloads stay encrypted.
- One login per service, one task queue per service and one schema per service: the release carries the `rwb_source_data` login, polls `rwb-source-data` and migrates `rwb_source_data` only (DP-02, DP-15).
- No ACE table is read directly and no ACE data is written: the release names this service's own views and no public table (DP-05).
- The release registers no Schedule: the build is event-started and the freshness cut-offs belong to RWB-P1-E1015-OPS (DP-10).
- No row of a stamped business date is deleted by an operation: a rerun replaces rows by record ID and business date, and no operator action writes a business row.
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing smoke run never replaces a working build.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | The chart, the worker registration, the migration step, the trigger step and the smoke run | TC-P1-E2010-OPS-01, TC-P1-E2010-OPS-02, TC-P1-E2010-OPS-06 |
| REQ-RDF-010 | Access per data product by role; personal data masked by role under PDPA | The ingress of the DP04 record read and the alert and dashboard payload rule | TC-P1-E2010-OPS-04, TC-P1-E2010-OPS-05 |
| ADR-023 | Observability per service | The five series, the three alerts and the three runbook entries | TC-P1-E2010-OPS-04, TC-P1-E2010-OPS-05 |
| REQ-DRI-006 | No component calls a system of record directly | The migration scope and the read path through this service's own views | TC-P1-E2010-OPS-01 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E2010-APP | App development | The build this story deploys: the workflow, the activities, the tables and the record read |
| RWB-P1-E2010-CON | Contract | The DP04 record shape the smoke run reads back |
| RWB-P1-E1015-OPS | DevOps | Sibling of the same service: owns the freshness cut-off Schedules, the stale flag and its alerts, which this story reads and never registers |
| RWB-P1-E1015-APP | App development | Owns the stamp the smoke run proves and the two events on the topic |
| RWB-PLT-E1071-CON | Contract | The workflow kit, the namespace, the worker versioning and the build ID provider |
| RWB-PLT-N001-CON | Contract | The gateway-bff composite route of SCR-45 and SCR-03 |

### 19. Out of scope

- The workflow, the four activities, the two snapshot tables, the count check and the record read as code: RWB-P1-E2010-APP.
- The DP04 record shape, its envelope and its fakes: RWB-P1-E2010-CON.
- The freshness stamp, the stale flag, the `data_product_load` writer and their Schedules: RWB-P1-E1015-APP and RWB-P1-E1015-OPS.
- The access rows, the catalog entry and the access answer: RWB-P1-E1016-APP and RWB-P1-E1016-CON.
- The ACE view SQL, the grants and the boundary rule: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The topic provisioning, the schema registry and the `.dlt` retention (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The treatment entity and the guarantee claim record: rwb-case and rwb-guarantee; this deployment consumes their contracts at run time and deploys neither.
- The real cross-service proof of the trigger, the count break and the rerun against the live owners: RWB-ITG-E2010-ITG.
- The exact cluster topology, node pools, replica counts, thresholds and probe timings; they are set per environment by the platform team (GAP-0513; ASM-0705).
