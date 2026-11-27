# RWB-P1-E2010-OPS Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2010-OPS |
| Work type | OPS (DevOps) |
| Document version | v3 |
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
| Ready to start | After RWB-P1-E1015-OPS (base release of the shared chart); checks that need the application image wait for RWB-P1-E2010-APP; switching the feature on in SIT, UAT and PROD waits for the Section B gate (RD-P1-043) |
| Size | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-16); squad sizes at refinement |
| Depends on (build) | RWB-P1-E1015-OPS, RWB-P1-E2010-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON; RWB-P1-E2010-APP for the application image |
| Contract dependencies | RWB-P1-E2010-CON (must reach Done before build) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), path major version /v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-006, FR-P1-024, FR-P1-025, FR-P1-030, FR-P1-031) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-002, RD-P1-012, RD-P1-040, RD-P1-041, RD-P1-043, RD-P1-044, RD-P1-045 |

**Version 3 changes.**

- The build is a child workflow of `AceIngestCheck`: no listener, consumer group, retry topic or synthetic event of this release (RWB-P1-E2010-OPS#4, #6, #7 and #19; RD-P1-040, RD-P1-044).
- The release is a delta on the RWB-P1-E1015-OPS chart; the flag stops only the child start; rerun, retry and rollback follow the rulings; the stale alert of RWB-P1-E1015-OPS is reused (RWB-P1-E2010-OPS#1, #2, #8, #9, #11, #12 and #16; RD-P1-012, RD-P1-044, RD-P1-045).
- AC8 restated, treatment reads on rwb-treatment, smoke and test cases restated (RWB-P1-E2010-OPS#3, #10, #13, #15, #17, #18, #21 and #22).
- Pending: guarantee stub of wave 2 (NEW-GAP-S11-10), metric names (NEW-GAP-S11-11), detection and completion windows (NEW-GAP-S11-12) (RWB-P1-E2010-OPS#5, #14 and #20).
- Readiness decisions: as in the header.
- Test case references follow Test Cases v9: AC15 is TC-P1-E2010-OPS-17 and the legacy TC-E2-010 rows, now rows of RWB-P1-E2010-APP, are no longer listed.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-010 for rwb-source-data. The stage 2 step was a stage of the `rwb-case` JOB-02 chain inside one deployable, so its deployment was the deployment of that chain. In the target the build is `Stage2ProductWorkflow` on task queue `rwb-source-data`, started by `rwb.source-data.AceDataReady.v1` and owning no Schedule, and it writes two snapshot tables in `rwb_source_data` (DP-01, DP-10, DP-15). This story deploys that build, proves the trigger, gates the flag, publishes five series and three alerts and writes the runbook. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: version 3 applies the listed RD-P1 rulings and review corrections.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2010-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **the stage 2 product build of rwb-source-data deployed from one chart with a pinned digest and build ID, the worker that registers `Stage2ProductWorkflow` on `rwb-source-data`, the migration step that applies `rwb_source_data` and refuses another schema, the proof that the build starts as a child of `AceIngestCheck` and owns no Schedule and no consumer group, the flag `rwb.dataengine.stage2-products`, five dashboard series and its count-break and workflow-failure alerts each with a runbook entry**, so that **an operator can see a stage 2 build that did not start, a business date that was not stamped, a count break that held the publish or a run that failed, and prove that a rerun of the same date leaves no duplicate and that a failed release keeps the previous build**.

### 2. Business rationale

The legacy stage 2 step had no deployment of its own: it ran inside the rwb-case chain over one schema, so a stuck step showed up as a failed job run and an operator had the database in front of them. In the target the step is a workflow of its own service, started by `AceIngestCheck` after the ALS stamp, writing two tables in this service's schema, joined at read time to the ACE views, and its result is three facts an operator must be able to see: whether the build for the business date started, whether it was stamped, and whether the count check held it. Without this story the app story can pass its tests while the worker is unregistered, the child is never started, the count break sits unread and DP04 turns stale with no alert (DP-10; Architecture v5 slide 44).

Deployment is also where the split is enforced operationally. The release carries the `rwb_source_data` login only, applies the `rwb_source_data` migration only, and reads no other service's schema and no ACE table directly: the contract and plan facts come through this service's own views, and the treatment and guarantee facts come through their contracts at run time (DP-01, DP-02, DP-05). The observability follows ADR-023 per service: five series with the environment, release and build ID as dimensions, alerts that each carry a message ID, and their runbook entries.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- RWB-P1-E1015-OPS is the base release: it owns the chart skeleton and values, the api and worker Deployments, the probes, the migration job, the `rwb_source_data` secret reference, the KEDA task-queue scaler, the 05:30 Schedule and the Load late, Load failed and stale alerts of every data product; this story adds only its own objects (RD-P1-044).
- The rwb-source-data baseline chart and login are deployed, with the REST base `/api/recovery/source-data/v1` and the relay of `rwb_source_data` (DP-02, DP-13).
- This release declares no topic, consumer group, retry topic or ACL: `Stage2ProductWorkflow` consumes nothing (RD-P1-040, RD-P1-044).
- The Temporal workflow kit and the `rwb-recovery` namespace exist, with worker versioning, the build ID provider and the payload codec (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The platform error envelope and the message catalogue are in force, so every alert can carry a message ID.
- The three environments DEV, SIT and UAT exist and the production namespace exists for the release date; the flag `rwb.dataengine.stage2-products` exists in the flag library.
- The chart of the app story is published with `Stage2ProductWorkflow` and its four activities, and the migration version that creates `dp_treatment` and `dp_guarantee_claim` sits on the service sequence (RWB-P1-E2010-APP; DP-15).
- The gateway-bff composite route for SCR-45 and SCR-03 is published (RWB-PLT-N001-CON, DP-19).
- The replica counts, the resource sizes, the lag and stale thresholds, the alert thresholds and the probe timings are environment values fixed by no source document (GAP-0513; ASM-0705).
- The build dependencies are those of the header.

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the API deployment and the workflow worker with the `rwb_source_data` login reference, namespace `rwb-recovery`, task queue `rwb-source-data`, the payload codec and the build ID of the release.
3. The worker registration step confirms that the shared worker of RWB-P1-E1015-OPS also registers `Stage2ProductWorkflow` and the activities `readDp04SourcePage(businessDate, page)`, `writeDp04Page`, `checkActiveCount` and `stampDp04` on `rwb-source-data` and on no other queue.
4. The migration step applies the `rwb_source_data` sequence of this release, including the version `V<next>__rwb_p1_e2010_dp04.sql` that creates `dp_treatment` and `dp_guarantee_claim`, and refuses to run when the target schema is not `rwb_source_data`.
5. The values step sets the base URLs of rwb-treatment, rwb-guarantee and rwb-case per environment and the pipeline checks that the `rwb_source_data` service identity is accepted by each read.
6. The flag step sets `rwb.dataengine.stage2-products` from the values of the environment. Off: `AceIngestCheck` starts no `Stage2ProductWorkflow`; the shared worker stays deployed.
7. The dashboard panels are published with the five series and the environment, release and build ID as dimensions.
8. The count-break alert (MSG-P1-002) and the workflow-failure alert (MSG-GEN-006) are wired to their runbook entries. DP04 stale uses the stale alert of RWB-P1-E1015-OPS (MSG-P1-001); this release registers no stale or Load late alert.
9. A smoke step in DEV calls `POST /v1/business-days/{date}/ready` for a synthetic business date with a COMPLETED ALS batch, waits for `stage2-dp04-{date}` to complete, reads DP04 back, and calls the ready operation again to prove that no second child starts and no row is duplicated.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The pipeline stops before promotion and the prior build stays active | None | AC1, AC11 |
| X2 | The migration target is a schema other than `rwb_source_data` | The step refuses the target and the release stops before any table is created | Pipeline error, no message id | AC1 |
| X3 | The worker registers the workflow on another queue, or registers no worker | The registration check fails the release and names the queue and the workflow | None | AC1 |
| X4 | The flag is off in an environment | The shared worker stays; `AceIngestCheck` starts no `Stage2ProductWorkflow`; the rows of the earlier dates are kept | None | AC3, AC10 |
| X5 | The ALS stamp commits with the flag on and no `stage2-dp04-{businessDate}` execution exists | The workflow-failure alert names the business date and the build ID; detection window Pending (NEW-GAP-S11-12) | MSG-GEN-006 | AC14 |
| X6 | The active count differs from the count written | No stamp is written, the break is listed and the count-break alert fires | MSG-P1-002 | AC5 |
| X7 | DP04 is not stamped by its expected-by time | The product turns stale and the stale alert of RWB-P1-E1015-OPS fires | MSG-P1-001 | AC5 |
| X8 | A dashboard series is missing, or an alert carries no message ID or no runbook link | The observability check fails the release | None | AC4, AC5 |
| X9 | A new build is promoted while an execution of the business date is running | The old build drains its execution and the new build takes the next start; the dashboards show both build IDs | None | AC6 |

X1 to X3 are the deployment paths of the release; X4 to X7 are the flag, the not-started condition and the two break conditions; X8 is the observability gate; X9 is the worker-versioning path of the workflow kit.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | A delta on the base release, using the workflow kit and the flag library; no application code is built here |
| Negotiable | Replica counts, resource sizes, thresholds and probe timings are environment values |
| Valuable | Makes a stage 2 build observable, provable and rerunnable before the Epic 3 screens depend on DP04 |
| Estimable | One chart delta, one worker registration, one migration step, one smoke step, five series, two own alerts and two runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the worker registers, the migration refuses a foreign schema, an alert fires on a synthetic condition, the smoke run leaves one row per record and date |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the stage 2 product build for rwb-source-data

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-source-data is rwb-source-data
    Given the target environment is SIT

  Scenario: AC1 The chart, the worker and the migration step are deployed and pinned (new, D-RCV-60; TC-P1-E2010-OPS-01, TC-P1-E2010-OPS-07, TC-P1-E2010-OPS-08)
    Given the rwb-source-data chart of RWB-P1-E1015-OPS and the values files of this release
    When the chart is rendered for DEV, SIT, UAT and PROD
    Then each render succeeds with the chart version and the image digest pinned and the build ID of the release commit
    Then the rendered diff against the base release changes no object that RWB-P1-E1015-OPS owns
    Then the worker registers Stage2ProductWorkflow, readDp04SourcePage, writeDp04Page, checkActiveCount and stampDp04 on task queue rwb-source-data in namespace rwb-recovery (RD-P1-002)
    Then the migration creates dp_treatment with key uk_dp_treatment (business_date, treatment_id) and dp_guarantee_claim with key uk_dp_guarantee_claim (business_date, guarantee_claim_id), and no other table
    Then a target schema other than rwb_source_data is refused before any table is created
    Then worker versioning is enabled and a new execution goes to the new build while the old build drains

  Scenario: AC2 The build is a child workflow and owns no Schedule (new, D-RCV-60; TC-P1-E2010-OPS-02)
    Given the deployed worker and the flag on
    When AceIngestCheck commits the ALS stamp for the synthetic date 2026-12-14
    Then exactly one execution "stage2-dp04-2026-12-14" is started as its child with ParentClosePolicy ABANDON (RD-P1-040)
    Then the release declares no consumer group, listener or topic ACL for rwb.source-data.events.v1
    Then the release registers no Schedule and no legacy Quartz trigger

  Scenario: AC3 The flag turns the build on and off (new, D-RCV-60; TC-P1-E2010-OPS-03)
    Given the flag rwb.dataengine.stage2-products set from the values file of SIT
    When the flag is on and AceIngestCheck commits an ALS stamp
    Then Stage2ProductWorkflow starts for that date
    When the flag is off and AceIngestCheck commits an ALS stamp
    Then no Stage2ProductWorkflow starts and the shared worker stays deployed
    Then the rows of the earlier business dates are unchanged

  Scenario: AC4 The five dashboard series carry the environment, the release and the build ID (new, D-RCV-60; TC-P1-E2010-OPS-04)
    Given the published dashboard panels
    When a synthetic build, a count break, a stale DP04 and a failed execution are produced
    Then within one scrape interval the dashboard shows the rows written per product, the load status per product, the count breaks, the stale products and the workflow failures
    Then each series carries the environment, the release and the build ID as dimensions
    # Pending: metric names, types, emitters and labels, owner observability owner, NEW-GAP-S11-11

  Scenario: AC5 Each alert carries its message ID and one runbook entry (new, D-RCV-60; TC-P1-E2010-OPS-05)
    Given the published alert rules and the runbook
    When a count break of 40 rows against 41, a stale DP04 and a failed execution are simulated
    Then one count-break alert carries MSG-P1-002 with source "DP04", the business date and check "Active treatment count 40 against 41"
    Then the stale DP04 raises the stale alert of RWB-P1-E1015-OPS with MSG-P1-001, and this release registers no second stale alert
    Then one workflow-failure alert carries MSG-GEN-006 naming the system whose read failed and the business date
    Then each alert of this release links one runbook entry with the check, the owner role (count break RW-DATASTEW; workflow failure RW-PLATADM) and the recovery step
    Then no alert threshold and no probe timing is hard-coded, and no secret appears in a values file, a dashboard or the runbook

  Scenario: AC6 The smoke run writes and reads one business date without duplicates (new, D-RCV-60; TC-P1-E2010-OPS-06)
    Given DEV with synthetic rows only, a COMPLETED ALS batch for a synthetic date and the 40-treatment fixture
    When the smoke step calls POST /v1/business-days/{date}/ready with an Idempotency-Key
    Then "stage2-dp04-{date}" ends COMPLETED, dp_treatment holds 40 rows for the date and DP04 is stamped LOADED
    Then GET /data-products/DP04/records for a fixture case UUID answers 200 with the rows of that case
    When the smoke step calls the ready operation for the same date again
    Then no second stage 2 execution starts and the row count per table is unchanged
    # Pending: smoke identity, its DP04 access row and the fixture owner, GAP-0513 and GAP-0392

  Scenario: AC7 A failing activity follows the catalog retry policy and writes no duplicate (new, D-RCV-60; TC-P1-E2010-OPS-09)
    Given the deployed worker and an activity set to fail on every attempt
    When the build runs
    Then the activity is attempted 10 times with a 1 s initial interval and back-off 2, and the execution ends FAILED
    Then one workflow-failure alert with MSG-GEN-006 is raised
    Then a retried writeDp04Page writes no duplicate row
    # Pending: start-to-close timeout and heartbeat (GAP-0143) and non-retryable error types (NEW-GAP-W5-002); both are chart values with no value yet

  Scenario: AC8 Promotion without a passing smoke run is refused (new, D-RCV-60; TC-P1-E2010-OPS-10)
    Given a deployment in state Blocked after a failed smoke run
    When a release manager requests its promotion
    Then the pipeline refuses the promotion, the deployment stays Blocked and the previous build stays in force

  Scenario: AC9 A failing release never replaces the working build, and the deployment writes no stamp (new, D-RCV-60; TC-P1-E2010-OPS-11)
    Given the previous build in force and a release whose tests or smoke run fail
    When the release is promoted
    Then the previous build stays in force
    When the smoke run of a passing release has matching counts for the date
    Then data_product_load holds one DP04 row for the date with status LOADED, written through the stamp of RWB-P1-E1015-APP and by no deployment step

  Scenario: AC10 The flag off leaves the other P1 work running (TC-P1-E2010-OPS-12)
    Given rwb.dataengine.stage2-products is off in SIT
    When AceIngestCheck runs for a date with a COMPLETED ALS batch
    Then it stamps the source products and publishes AceDataReady as with the flag on
    Then no Stage2ProductWorkflow execution exists for the date

  Scenario: AC11 A failed migration leaves the prior build active (TC-P1-E2010-OPS-13)
    Given the stage 2 migration fails before completion
    When the release pipeline reaches promotion
    Then promotion stops and the prior build keeps serving

  Scenario: AC12 Rollback runs on the migrated schema (TC-P1-E2010-OPS-14)
    Given the stage 2 migration is applied
    When the flag is switched off and, only if needed, the previous image tag and chart version are redeployed
    Then the previous build passes its smoke test on the migrated schema and no migration is reversed (RD-P1-045)
    Then no running workflow is terminated, no dp_treatment row is removed and the release note names every P1 capability the redeploy reverts

  Scenario: AC13 The service identity is accepted by the reads and by nothing wider (TC-P1-E2010-OPS-15)
    Given the rwb_source_data service identity
    When it calls the treatment window, active-count, guarantee claim, case and reference-data reads
    Then each call is authorised
    When it selects from a table of another service's schema
    Then the database refuses it with SQLSTATE 42501

  Scenario: AC14 A stamp that started no child is alerted (TC-P1-E2010-OPS-16)
    Given the flag on and an ALS stamp for a date with no execution "stage2-dp04-{date}"
    When the detection window ends
    Then the workflow-failure alert fires with MSG-GEN-006 and its runbook link
    # Pending: detection window, owner observability owner, NEW-GAP-S11-12

  Scenario: AC15 Telemetry carries no personal value or amount (TC-P1-E2010-OPS-17)
    Given a failed run over a fixture with known amounts and names
    When logs, series, alerts and workflow history are searched
    Then none of those values appears
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one task queue and one schema per service: the release carries the `rwb_source_data` login, polls `rwb-source-data` only and migrates `rwb_source_data` only | Architecture v5 slides 29 and 41; DP-02; DP-15 |
| BR2 | The stage 2 build is a child of `AceIngestCheck`, started after the ALS stamp with workflow ID `stage2-dp04-{businessDate}`; it consumes no topic and owns no Schedule | DP-10; RD-P1-040; RD-P1-044 |
| BR3 | Every worker carries the build ID of its release and worker versioning is enabled, so a new build takes new executions while the old build drains | Temporal and Drools design slide 11; RWB-PLT-E1071-CON |
| BR4 | Every alert carries a message ID and links one runbook entry with the check, the owner role and the recovery step | Template and Rules §R7.2 s14 |
| BR5 | No environment value is hard-coded: replicas, resources, thresholds, probe paths and timings and the flag come from a named chart value set per environment and from parameters; the fixture owner is named at the wave 2 entry check (GAP-0513) | Template and Rules §R7.2 s17 |
| BR6 | Dashboard series, alert payloads and the runbook carry counts, product codes, business dates, statuses and build IDs only, never a treatment amount, a claim amount or a personal value | ADR-023; Template and Rules §R7.2 s17 |
| BR7 | The release writes no ACE data and reads no other service's schema or table; the ACE facts are read through this service's own views and treatment facts through rwb-treatment and guarantee facts through the rwb-guarantee contract | DP-01; DP-05 |
| BR8 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run | DP-10 |
| BR9 | The stamp is written by the freshness story and never by this deployment; the deployment only proves that the stamp of a business date appears when the count matches | RWB-P1-E1015-APP; BR4 of the legacy story |

**Where each rule lives in the target.** BR1 is the chart, the values and the migration step. BR2 is the child start of AC2 and the fact that the release registers no Schedule and no consumer. BR3 is the worker versioning and the build ID of the release. BR4 is the alert wiring and the runbook. BR5 is the values files. BR6 is the series definition and the alert payload. BR7 is the migration scope and the ACLs. BR8 is the rollback rule. BR9 is the smoke run, which reads the stamp rather than writing it.

**Wave difference of the guarantee copy (GAP-2739).** The dated copy `dp_guarantee_claim` stays with rwb-source-data in `rwb_source_data` and the live claim record stays with rwb-guarantee in `rwb_guarantee`. This story is wave 2 and the claim record is wave 3: until the claim stories of wave 3 land, the build runs against the published fake of the claim read, which answers an empty list, so the DP04 guarantee part stays empty rather than stale. The DP04 release note records this wave difference as a dependency. Pending: whether a stub that serves this read is deployed in SIT, UAT and PROD in wave 2, and its base URL per environment, or whether the call is switched off without an alert, owner solution architect, tracked as NEW-GAP-S11-10.

**Case link of the claim rows (GAP-2740).** The claim read answers every claim in the window with its `case_id`, and no case is resolved on that read. The References check, the data quality break list and the retry stay with RWB-P1-E2010-APP, which owns the case-existence answer of the DP04 build. This deployment adds no case-existence read, no consumed case contract and no dependency for it.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Worker registered and probes healthy | The worker polls `rwb-source-data` only and the registration check passes | Ready |
| Ready | Release superseded | A new chart version passes its tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open executions | Ready |
| Ready | Flag off | `rwb.dataengine.stage2-products` is turned off in the environment | Ready; no child is started |
| Ready | Smoke run failed | The build, the read-back or the repeated ready call of the smoke run fails | Blocked |
| Blocked | Previous build restored | The previous chart version is redeployed with its build ID | Ready |

The DP04 freshness states LOADED and STALE and the workflow execution states RUNNING, COMPLETED and FAILED belong to the product and the app story; they are not states of this deployment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps team | Owns the chart, the values files, the pipeline stages, the registration step, the dashboards and the runbook |
| RW-PLATADM, platform administrator | Owns the `rwb-recovery` namespace and the flag library; runs the workflow-failure runbook entry |
| Platform workflow owner | Owns the task queue, the namespace, the worker registration and the versioning policy |
| Platform event owner | No object of this release |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| RW-PLATADM and RW-DATASTEW on call | Run the runbook entries and open an incident when a count break or a failed execution persists |
| RW-DATASTEW, data steward | Reads the DP04 status and the breaks the alerts point at |
| RW-AUDIT, internal audit | Reads the runbook, the alert history and the release record |

The worker runs as the `rwb_source_data` service identity (DP-02), carried by the chart as a secret reference and never as a literal name. No credential and no personal name appears in a values file, a dashboard, an alert payload or the runbook.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, flag value | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Task queue | `rwb-source-data` in namespace `rwb-recovery`, polled by the rwb-source-data worker only | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Trigger | Child start by `AceIngestCheck` in the workflow task that commits the ALS stamp | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Schema | `rwb_source_data`, migrated by its own per-service Flyway sequence; this release applies the version that creates `dp_treatment` and `dp_guarantee_claim` | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Tables behind the series | `dp_treatment`, `dp_guarantee_claim`, `data_product_load`; the series read counts and statuses only | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Dashboard series | Rows written per product, load status per product, count breaks, stale products, workflow failures; dimensions environment, release, build ID | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Alerts | Two rules of this release: MSG-P1-002 for a count break and MSG-GEN-006 for a workflow failure or a child not started; DP04 stale uses the RWB-P1-E1015-OPS alert (MSG-P1-001) | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Runbook entries | Count break held the stamp; workflow failed or did not start; each with the check, the owner role and the recovery step | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Secrets | The `rwb_source_data` login secret and the Temporal mTLS material, from the platform secret store | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |
| Test data | Synthetic COMPLETED ALS batch, the 40-treatment fixture of the app story and one count break, in DEV; fixture owner Pending (GAP-0513; ASM-0705) | Not specified in the source documents (DOR-RWB-P1-E2010-OPS-7) |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded (GAP-0513; ASM-0705).

**Probes.** Readiness answers healthy only after the worker has polled `rwb-source-data` once and has registered the workflow and its four activities; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database, starts an execution or commits an offset, and a failing dependency is reported as not ready, never as live-and-broken. The paths and timings are values of the environment.

### 12. Contract

#### 12.1 REST operations provided

None from this story. The DP04 branch of `GET /api/recovery/source-data/v1/data-products/{productCode}/records` is declared by RWB-P1-E2010-CON and implemented by RWB-P1-E2010-APP; this deployment exposes it through the chart and its ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None from the deployment. The worker calls the `rwb-treatment`, guarantee claim and rwb-case contracts and reads the ACE views at run time as the app story's client; this release adds their base URLs per environment to the values files and the network and service-identity rights of `rwb_source_data` for those reads, checked by the pipeline. The right names are Pending, owner security owner (NEW-GAP-S3-6).

#### 12.3 Events published

None of its own. `rwb.source-data.events.v1` carries `AceDataReady` and `AceDataLate` from RWB-P1-E1015-APP; this release publishes neither and its smoke run puts no test message on the topic. The smoke run drives the ready operation in DEV, where the events of the real flow stay inside the synthetic environment.

#### 12.4 Events consumed

None. The release configures no consumption, inbox, retry topic or dead-letter routing (RD-P1-040, RD-P1-044).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `Stage2ProductWorkflow` | Child workflow of `AceIngestCheck`, one run per business date, ID `stage2-dp04-{businessDate}` | `rwb-source-data` | Registered by the shared worker, with the build ID and worker versioning; no Schedule |
| `readDp04SourcePage(businessDate, page)` | Activity | `rwb-source-data` | Retry 1 s initial interval, back-off 2, 10 attempts; timeouts as chart values (GAP-0143) |
| `writeDp04Page` | Activity | `rwb-source-data` | Registered with the same policy; idempotent by record ID and business date |
| `checkActiveCount` | Activity | `rwb-source-data` | Registered with the same policy |
| `stampDp04` | Activity | `rwb-source-data` | Registered with the same policy; calls the freshness stamp of RWB-P1-E1015-APP |

**Build ID and versioning.** The build ID is the one supplied by the workflow kit for the release commit; worker versioning is enabled and a new build takes new executions while the old build drains (BR3). The exact build ID format is supplied by the workflow kit. Rollback follows RD-P1-045.

#### 12.6 Schedules

None. The deployment registers no Schedule: the build is a child of `AceIngestCheck`, and the 05:30 Schedule and the freshness timers belong to RWB-P1-E1015-OPS and RWB-P1-E1015-APP (BR2; DP-10).

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| `dp_treatment` | P1 (`rwb_source_data`) | Created by the migration step of this release; the row counts feed the rows-per-product and count-break series; read for reporting only, never as the source of a treatment |
| `dp_guarantee_claim` | P1 (`rwb_source_data`) | Created by the same migration step; its row counts feed the same series |
| `data_product_load` | P1 (`rwb_source_data`) | Read for the load-status and stale-product series; written by RWB-P1-E1015-APP and never by this deployment |

The release applies the stage 2 migration of the app story, which creates `dp_treatment` and `dp_guarantee_claim` only: no treatment table of another service, no guarantee table and no ACE table is created, altered or read directly (DP-01, DP-05, DP-15).

#### 12.8 Contract fakes

None from this release. The contract mocks of the treatment and guarantee reads and the ACE fixture are test doubles of the app story; the guarantee stand-in of wave 2 is Pending (NEW-GAP-S11-10).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The reads are the app story's; base URLs and rights are this release's values |
| Kafka | None | No topic, consumer group or ACL |
| Temporal | 1 workflow, 4 activities, 0 Schedules | Worker on `rwb-source-data` with a pinned build ID and worker versioning |
| File | None | No file is read or written by the deployment |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_source_data` only and reads no other schema | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The ACE facts are read through this service's own views at run time, never from a public table | none |
| DP-07 | Reference data, LOV | The rwb-case reference-data contract is a run-time dependency of the worker, with its keeper library | H RWB-PLT-E1043-CON |
| DP-10 | Quartz, JOB-nn | The shared worker, the task queue and the namespace; the build is a child workflow; no Schedule is registered | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The release declares no REST path and no client of its own; the worker calls the contracts as the app story's client | none |
| DP-13 | `/api/recovery/v1` | The ingress serves `/api/recovery/source-data/v1` and no other base | none |
| DP-15 | V0001 baseline, migration | The per-service Flyway sequence of `rwb_source_data`; the migration step refuses another schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff serves SCR-45 and SCR-03; the composite route belongs to RWB-PLT-N001-CON and this release registers none | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-source-data/` values delta | Workflow registration, base URLs, flag, thresholds; the Deployments, probes, secrets and scaler stay those of RWB-P1-E1015-OPS |
| `helm/rwb-source-data/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml`, `values-prod.yaml` | Flag value, base URLs, activity timeout and heartbeat values, alert thresholds and detection window (GAP-0513; ASM-0705; NEW-GAP-S11-12) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration step, identity check, smoke run, promotion |
| Registration step | `Stage2ProductWorkflow` and its four activities on `rwb-source-data`, with the build ID and worker versioning |
| Migration step | The `rwb_source_data` migration of this release; a target schema other than `rwb_source_data` is refused |
| Child-start check | Proves that the ALS stamp starts `stage2-dp04-{businessDate}` and that no Schedule or consumer is declared |
| Dashboards | The five series of section 11 with the three dimensions |
| Alerts | Two rules, each with a message ID and one runbook entry; the stale alert is reused |
| Runbook | Two entries: count break held the stamp; workflow failed or did not start |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-002 | The active count differs from the count written for the business date, so the stamp is held | Count-break alert naming the product, the business date, the check text and the build ID | Platform on-call and the data steward, ticket |
| MSG-P1-001 | DP04 is not stamped by its expected-by time | The stale alert of RWB-P1-E1015-OPS; no rule of this release | As RWB-P1-E1015-OPS |
| MSG-GEN-006 | An execution of the build failed, or an ALS stamp started none within the window (NEW-GAP-S11-12) | Workflow-failure alert naming the workflow, the business date, the system whose read failed and the build ID | Platform on-call, page |

**Rerun and idempotency.** Only a FAILED run is rerun, through `POST /admin/jobs/{jobId}/rerun` of RWB-P1-AD018-CON (wave 4); a rerun of a run that is not FAILED answers 409 MSG-P1-011 (RD-P1-012). Restart before wave 4 is Pending (NEW-GAP-S11-5) and a COMPLETE run is not run again (NEW-GAP-F05-2). `writeDp04Page` upserts by record ID and business date.

**Rollback (RD-P1-045).** (1) Switch `rwb.dataengine.stage2-products` off. (2) Only if the flag does not cover the fault, redeploy the previous image tag and chart version of rwb-source-data; the chart is shared, so the release note names every P1 capability the redeploy reverts. (3) Never reverse a migration; a faulty one is corrected by a new forward version, and the previous tag must pass its smoke test on the migrated schema. Workers use worker versioning and no running workflow is terminated. The release owner rolls back when the post-deploy checks fail, the platform smoke workflow reports no result for the day, or an incident is attributed to the release.

**Feature switch.** `rwb.dataengine.stage2-products`. On: `AceIngestCheck` starts the child after the ALS stamp. Off: no child execution; the shared worker stays and the rows of earlier dates are kept.

**Done when.** The tests of section 16 pass for AC1 to AC15, the chart diff shows only this release's objects, the smoke run writes and reads back one synthetic business date, and the two runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | A count break held the stamp of the business date | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-001 | DP04 is stale after a build that did not run or did not complete | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | The stage 2 build failed, a treatment or guarantee read could not complete, or a stamp started no child | {system} is not available. Try again in a few minutes. |
| MSG-P1-011 | A rerun of a run that is not FAILED, or while a run of the date is PENDING or RUNNING | The {source} load for {date} is already complete or running. It was not run again. |

Texts are those of Error and Message Standard v6. In the alerts {source} is "DP04", {check} is the break check text and {system} is the system whose read failed ("Treatment" or "Guarantee"), or "Stage 2 build" when no child started. An alert payload names the product, the business date, the check, the failure class, counts and the build ID only. Thai text for each message follows decision DL10; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive.

### 15. Screens and states

The deployment has no screen and registers no route of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard, SCR-45 Data quality through gateway-bff (loading, empty, list, refused) and the runbook. SCR-45 and SCR-03 are served by the app story and the composite route of RWB-PLT-N001-CON. SCR-03 states: loading; empty, error and no access: Not specified in the source documents (CG-ALL-2430). SCR-45 error and no access: Not specified in the source documents (CG-ALL-2432). SCR-44 Interface and job monitor is not used, because the deployment registers no job of its own. SCR-44 states: empty, loading, error and no access: Not specified in the source documents (CG-ALL-2431). The Temporal Web UI stays behind the platform identity provider: RW-PLATADM operates and RW-AUDIT reads, and payloads are decoded only through the codec server under break-glass.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E2010-OPS-01 | AC1 | NFR | The chart renders for three environments with a pinned digest and the build ID; the worker registers on `rwb-source-data`; a foreign migration target is refused |
| TC-P1-E2010-OPS-02 | AC2 | NFR | One ALS stamp starts one child; no consumer and no Schedule is declared |
| TC-P1-E2010-OPS-03 | AC3 | NFR | The flag on and off in one environment; earlier rows are kept |
| TC-P1-E2010-OPS-04 | AC4 | NFR | The five series carry the three dimensions within one scrape interval |
| TC-P1-E2010-OPS-05 | AC5 | NFR | The count-break and workflow-failure alerts, and the reused stale alert |
| TC-P1-E2010-OPS-06 | AC6 | NFR | A synthetic date is written and read back; a repeated ready call starts no second child |
| TC-P1-E2010-OPS-07 | AC1 | NFR | The worker registers exactly the workflow and the four activities of section 12.5 |
| TC-P1-E2010-OPS-08 | AC1 | NFR | The migration creates dp_treatment and dp_guarantee_claim only, with their keys; a table of another schema is refused |
| TC-P1-E2010-OPS-09 | AC7 | NFR | A synthetic activity failure is attempted 10 times; no duplicate row |
| TC-P1-E2010-OPS-10 | AC8 | NFR | Promotion of a Blocked deployment is refused |
| TC-P1-E2010-OPS-11 | AC9, BR8, BR9 | NFR | A failing release keeps the previous build; the DP04 stamp is written by the freshness story |
| TC-P1-E2010-OPS-12 | AC10 | Component | Flag off, AceIngestCheck still stamps and publishes |
| TC-P1-E2010-OPS-13 | AC11 | Component | Failed migration |
| TC-P1-E2010-OPS-14 | AC12 | Component | Rollback on the migrated schema |
| TC-P1-E2010-OPS-15 | AC13 | Component | Service identity grants |
| TC-P1-E2010-OPS-16 | AC14 | Component | ALS stamp with no child execution |
| TC-P1-E2010-OPS-17 | AC15 | Component | Telemetry search over known amounts and names |

The TC-P1-E2010-OPS rows are in Test Cases v9, which holds AC1 to AC15 as worded in this version. The legacy rows TC-P1-E2010-APP-04 to TC-P1-E2010-APP-12 belong there to RWB-P1-E2010-APP, which proves the business behaviour behind them, and are not cited as rows of this story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

**DP04 integration harness (GAP-0392).** The gateway-bff composite DP04 record route path and merge order, and the harness environment, repository, seed pack, evidence format, retention and pass or fail gate, are Not specified in the source documents (GAP-0392). The Integration lead and the QA lead agree them at the wave 2 entry check, the route path and merge order with the platform edge story, and record the result in the DP04 harness pack before the first real-service run.

### 17. Guardrails

- No business value in a values file: the product code, the access roles, the expected-by time and the count tolerance are data rows and decisions, never a deployment value (DP-07).
- No personal data in logs, dashboard series, alert payloads, the runbook or the workflow history: counts, product codes, business dates, statuses, failure classes and build IDs only, and payloads stay encrypted.
- One login per service, one task queue per service and one schema per service: the release carries the `rwb_source_data` login, polls `rwb-source-data` and migrates `rwb_source_data` only (DP-02, DP-15).
- No ACE table is read directly and no ACE data is written: the release names this service's own views and no public table (DP-05).
- The release registers no Schedule and no consumer: the build is a child of `AceIngestCheck`, and the freshness timers belong to RWB-P1-E1015-OPS (DP-10).
- No row of a stamped business date is deleted by an operation: a rerun upserts rows by record ID and business date, smoke rows are synthetic and stay in DEV, and no operator action writes a business row.
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing smoke run never replaces a working build.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | The chart, the worker registration, the migration step, the child-start check and the smoke run | TC-P1-E2010-OPS-01, TC-P1-E2010-OPS-02, TC-P1-E2010-OPS-06 |
| REQ-RDF-010 | Access per data product by role; personal data masked by role under PDPA | The ingress of the DP04 record read and the alert and dashboard payload rule | TC-P1-E2010-OPS-04, TC-P1-E2010-OPS-05 |
| ADR-023 | Observability per service | The five series, the two alerts and the two runbook entries | TC-P1-E2010-OPS-04, TC-P1-E2010-OPS-05 |
| REQ-DRI-006 | No component calls a system of record directly | The migration scope and the read path through this service's own views | TC-P1-E2010-OPS-01 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E2010-APP | App development | The build this story deploys: the workflow, the activities, the tables and the record read |
| RWB-P1-E2010-CON | Contract | The DP04 record shape the smoke run reads back |
| RWB-P1-E1015-OPS | DevOps | Base release of the shared chart: owns the Deployments, probes, migration job, 05:30 Schedule and the stale and Load alerts |
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
- The topics, consumer groups, schema registry and dead-letter handling: none belongs to this release.
- The treatment record (rwb-treatment) and the guarantee claim record (rwb-guarantee); this deployment consumes their contracts at run time and deploys neither.
- The real cross-service proof of the child start, the count break and the rerun against the live owners: RWB-ITG-E2010-ITG.
- The exact cluster topology, node pools, replica counts, thresholds and probe timings; they are set per environment by the platform team (GAP-0513; ASM-0705).

### 20. Remaining delivery steps

- Size: Not specified; owner DevOps team.
- Epic design sign-off: Pending; owner product owner.
- RWB-P1-E2010-CON Done: Pending; owner contract owner.
- Chart values, alert thresholds and routes, migration version number and smoke fixture: Pending where not specified; owner DevOps team (GAP-0513).
- Service identity rights on the treatment, guarantee and case reads: Pending; owner security owner (NEW-GAP-S3-6).
- Guarantee stand-in of wave 2: Pending; owner solution architect, tracked as NEW-GAP-S11-10.
- Metric names, types, emitters and labels: Pending; owner observability owner, tracked as NEW-GAP-S11-11.
- Detection window, alert thresholds and latest completion time of the build: Pending; owner observability owner, tracked as NEW-GAP-S11-12.
- Test data in DEV: Pending; owner QA lead.
