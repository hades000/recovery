# RWB-P1-AD018-OPS Interface and job monitor

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-AD018-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | L-P1-B |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | rwb-source-data.yaml info.version 5.0.0 (05 Technical architecture/Recovery Workbench API Specification v5), path /v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-018 for rwb-source-data. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 11 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the monitor capability of rwb-source-data deployed from the service template with its own login, its migration for the run log, no new topic and no new consumer group, the panels for job status, wait state, duration against the expected minutes and stale products, the alerts wired to MSG-P1-001 and MSG-P4-002 within the 15-minute target, and the run books for a failed job, a job waiting for the ACE batch and a refused rerun**, so that **an operator finds a failed job or a late ACE batch before the working day without reading code, and no release can quietly add an ACE rerun path or a second source of truth for the wait state**.

This story deploys an existing capability. It adds no topic, no consumer group, no Schedule and no endpoint: the catalogue and the run log are rows of `rwb_source_data`, the ACE business date is read through the service's own `v_ace_*` path, and the screen is reached through the gateway-bff route.

### 2. Business rationale

The legacy monitor had one deployment and one operator, and its failure signals were a row in a table that nobody watched outside office hours. In the target the monitor is part of a service with its own release, its own login and its own alerting (DP-02, ADR-023), and the operational question changes from "is the screen up" to four separate questions: did the job start, is it waiting for an ACE batch, did it finish inside its expected minutes, and is a product stale (NFR-067, NFR-068).

The two failures that matter are separated on purpose. A **failed** job is an incident of this service and pages the owner role of the catalogue row. A **waiting** run is a signal about ACE: it pages nobody, it raises MSG-P1-001 to the data steward and the operations channel, and the run book says in one line that no Workbench action will make the batch arrive (NFR-015, BR3 of the app story). Deployment is part of the capability because a chart that carries a second credential, or a release that adds an ACE rerun path, would break the two guardrails the story set was built on.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across the composite route and the service.
- The Kafka event platform is available (RWB-PLT-EVT, RWB-PLT-TE006-CON); `rwb.source-data.events.v1` and its retry and `.dlt` topics are provisioned by RWB-P1-E1015-OPS, and this story subscribes to none of them.
- RWB-P1-AD018-CON is published, so the smoke profile and the drift test run against the three operations and the four fakes of that baseline.
- RWB-PLT-E1056-OPS loads the catalogue baseline with its `owner_role`, `expected_minutes`, `alert_after_minutes` and `runbook_path`, so every alert and every run book link has an owner without a code change.
- The three environments DEV, SIT and UAT exist with their platform session, their database endpoint and their Temporal endpoint. The alert thresholds have no value in the source documents (GAP-2164; ASM-3468).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-source-data with the rwb-source-data login, the pre-deploy migration job for `rwb_source_data` that creates the run log, and the readiness and liveness probes of the api deployment.
3. The provisioning step asserts that this release declares no topic, no consumer group and no Schedule of its own, and that `rwb.source-data.events.v1` is used exactly as RWB-P1-E1015-OPS provisioned it.
4. The provisioning step asserts that no ACE endpoint, credential or job name is reachable from the chart: the service has no path to `public`, to an ACE feed or to an ACE batch rerun.
5. The dashboards are published: runs by job and business date, status counts including WAITING, duration against `expected_minutes`, rerun count by job, the MSG-P1-001 rate, the STALE product count, the monitor read latency and its error rate.
6. The alerts are wired to the message IDs of section 14 and to the run book entries of section 13; each threshold is a values-file entry and each alert resolves its owner role from `job_catalog.owner_role`.
7. A smoke step calls the two admin operations and the freshness read of a synthetic catalogue through gateway-bff in the SIT profile, exercises a rerun of a synthetic failed job, and asserts that the second run is visible beside the first.
8. The run books are published and reviewed with the on-call rota: a failed job, a run waiting for the ACE batch, a refused rerun, a stale product with no business date, and a monitor read that fails.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | A release declares a topic, a consumer group or a Schedule of its own | The provisioning assertion fails the release | None | AC3 |
| X3 | A release adds a path to `public`, to an ACE feed or to an ACE batch rerun | The boundary assertion fails the release | None | AC3, AC6 |
| X4 | A job fails | The failed-job alert fires within the 15-minute target to the owner role of the catalogue row | None | AC5 |
| X5 | A run waits because the ACE batch is late | The wait-state panel rises, MSG-P1-001 is raised to the data steward and the operations channel, no page is sent | MSG-P1-001 | AC5 |
| X6 | A rerun is refused with 409 | The refused-rerun count rises and the run book entry explains the two allowed causes | MSG-P1-001 | AC5 |
| X7 | A product shows STALE with no business date | The stale panel rises and the entry for a product with no business date is opened | MSG-P1-001 | AC5 |
| X8 | The monitor read fails or is slow | The read-error-rate and latency alerts fire; the composite route is checked before the service | None | AC5, AC6 |
| X9 | The smoke step cannot see the second run after a rerun | The release stops; the run log and the Idempotency-Key are checked | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform provisioning, the observability stack and the published contract baseline; builds no application code |
| Negotiable | Replica counts, resource sizes, retention and alert thresholds are environment values, not story decisions |
| Valuable | Turns the monitor into an operated capability with an owner, a signal and a run book for each of its four questions |
| Estimable | One chart, one pipeline stage, one migration job, two probes, nine panels, six alert rules and five run-book entries |
| Small | Fits one sprint with the run books |
| Testable | Every criterion tests an artefact: the chart renders, the assertions pass, the panels carry data, an alert fires on a synthetic metric, a run-book entry resolves |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the interface and job monitor

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart and values deploy rwb-source-data with its own login and its run-log migration (new, D-RCV-60)
    Given the rwb-source-data Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-source-data login reference and no other service's credential and no ACE credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_source_data and creates the run log with its unique key on job_id, business_date and run_no, before the deployment is marked ready
    Then the api deployment answers its readiness and liveness probes on the health operation of the template
    Then no replica count, resource size, timeout or threshold is hard-coded in the template

  Scenario: AC2 The pipeline promotes one artefact and runs the contract tests (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit and component tests of RWB-P1-AD018-APP and the contract tests of RWB-P1-AD018-CON and fails the build on a drift between a fake and the document
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 The release adds no topic, no consumer group and no ACE path (new, D-RCV-60)
    Given the provisioning step of rwb-source-data for the monitor capability
    When it runs against the environment
    Then the release declares no topic of its own and rwb.source-data.events.v1 keeps the partitions, the retention and the retry and .dlt topics that RWB-P1-E1015-OPS provisioned
    Then the release declares no consumer group for the monitor and consumes no event
    Then the release declares no Temporal Schedule and no Quartz trigger
    Then the assertion fails the release when any of the three appears
    Then the assertion fails the release when the chart carries a path, a credential or a job name that can start, stop or rerun an ACE batch, a feed or a file

  Scenario: AC4 The nine panels show the four operational questions (new, D-RCV-60)
    Given the published dashboard of rwb-source-data
    When it is opened for a business date
    Then it shows runs by job and business date with their status and duration
    Then it shows the count of runs in WAITING and the last complete ACE business date of each source
    Then it shows the duration of each job against its expected_minutes from the catalogue and the count past alert_after_minutes
    Then it shows the rerun count by job and the number of attempts per business date
    Then it shows the MSG-P1-001 rate, the STALE product count and the monitor read latency and error rate
    Then every panel reads an identifier, a code, a date, a count or a duration and no customer field

  Scenario: AC5 The alerts fire to the catalogue owner within the 15-minute target (new, D-RCV-60)
    Given the alert rules of the capability and their values-file thresholds
    When a synthetic metric crosses each rule
    Then a failed job alerts the owner_role of its catalogue row within 15 minutes of the failure
    Then a run in WAITING past its cut-off raises MSG-P1-001 to the data steward and the operations channel and pages nobody
    Then a refused rerun with 409 raises its count alert and links the run-book entry for the two allowed causes
    Then a product STALE with no business date raises its own alert and links the same entry
    Then a monitor read error or latency above its threshold alerts the platform administrator role
    Then every threshold is a values-file entry and no threshold, owner or channel is written in the chart or the code

  Scenario: AC6 The run books and the smoke profile prove the two guardrails (new, D-RCV-60)
    Given the run books of section 13 and the SIT smoke profile
    When the smoke step runs through gateway-bff
    Then it reads the job list and the freshness answer of a synthetic catalogue for a synthetic business date
    Then it reruns a synthetic failed job once and sees two runs, run 1 and run 2, in the same answer
    Then it receives a 409 with MSG-P1-001 for a business date whose source row is not complete in v_ace_batch_status
    Then each of the five run-book entries names its message ID, its first check, its owner role and its escalation
    Then every entry states that no ACE batch, feed or file is restarted from the Workbench and no data lake is involved

  Scenario: AC7 The release holds the nine business rules of section 8 (new, D-RCV-60)
    Given the rendered chart, the migration job, the provisioning step, the alert rules, the panels and the logs and traces of the release
    When the release is checked against BR1 to BR9
    Then the service has one login, the release carries no ACE credential and the grants are on rwb_source_data only
    Then the per-service Flyway sequence owns the schema objects the release needs and no other service's schema is touched
    Then the release declares no topic, consumer group or Schedule of its own and the service topic stays as its owner provisioned it
    Then no path, credential or job name can start, stop or rerun an ACE batch, a feed or a file
    Then a failed job alerts its catalogue owner role within 15 minutes and a waiting run raises MSG-P1-001 and pages nobody
    Then every threshold, channel and owner is a values-file or catalogue entry and never code
    Then one artefact is promoted through DEV, SIT and UAT without a rebuild
    Then no personal data reaches a panel, a log line or a trace
    Then no data lake, ADF job or inbound load path is deployed for this capability
```

These seven criteria are new for the deployment of the capability and test artefacts only; they restate no business outcome owned by RWB-P1-AD018-APP. The wave 4 harness RWB-ITG-AD018-ITG consumes the deployed capability and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login per service and no ACE credential in the release; grants on `rwb_source_data` only | DP-02; RWB-P1-E1069-APP |
| BR2 | The per-service Flyway sequence owns the schema objects the release needs, and no other service's schema is touched | DP-15; ADR-021 |
| BR3 | The release declares no topic, consumer group or Schedule of its own; the service topic stays as its owner provisioned it | DP-09, DP-14; RWB-P1-E1015-OPS |
| BR4 | No release adds a path, a credential or a job name that can start, stop or rerun an ACE batch, a feed or a file | RWB-AD-018 guardrail; NFR-015 |
| BR5 | A failed job alerts its catalogue owner role within 15 minutes; a waiting run raises MSG-P1-001 and pages nobody | NFR-068; RWB-P1-AD018-APP BR3 |
| BR6 | Every threshold, channel and owner is a values-file or catalogue entry, never code; apart from the 15-minute failed-job alert of BR5, which comes from NFR-068, the alert thresholds, panel baselines, channels, replica counts and resource sizes are Not specified in the source documents (GAP-2164), so each is held per environment in the values file | NFR-067; Template and Rules §R7.2 s17; GAP-2164 |
| BR7 | One artefact is promoted through the three environments without a rebuild | ADR-023; Template and Rules §R8 |
| BR8 | The monitor reads identifiers, codes, dates, counts and durations only; no personal data reaches a panel, a log line or a trace | Template and Rules §R7.2 s17 |
| BR9 | No data lake, no ADF job and no inbound load path is deployed for this capability | DP-17; RWB-P1-E1069-APP; FSD P1 v3 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Pipeline run | The pipeline and the boundary assertions pass | Deployed to DEV |
| Deployed to DEV | Promotion | The smoke profile passes | Deployed to SIT |
| Deployed to SIT | Promotion | The smoke profile, the panels and one alert per rule pass | Deployed to UAT |
| Deployed | Failed job or waiting run | The alert rule fires | Alerted, run book entry opened |
| Alerted | Run book completed | The job is rerun and both runs are visible, or the ACE batch arrives | Recovered, the alert closes |
| Deployed | Release declares a topic, a consumer group, a Schedule or an ACE path | The assertion fails | Release refused; the previous version keeps running |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps team | Owns the chart, the values files, the pipeline stage, the panels, the alert rules and the run books |
| RW-PLATADM, RW-SECADM | Operate the monitor and the rerun in the environment (Platform administration U) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read the monitor and receive the MSG-P1-001 alert on a stale product |
| Owner role of a catalogue row | Receives the failed-job alert of that job |
| Platform observability owner | Owns the metrics, panels, alerts and traces this story consumes |
| No role | Reruns an ACE batch, a feed or a file, or deploys a second source of truth for the wait state |

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Tables deployed | The run log in `rwb_source_data` (name pending, GAP-2164; ASM-3464), one row per attempt, with its unique key on `job_id`, `business_date` and `run_no`; `data_product_load` is read only; the `job_catalog` fields are read through the rwb-integration contract only, never by table | Not specified in the source documents (DOR-RWB-P1-AD018-OPS-7) |
| Catalogue rows | Read through the rwb-integration contract only, never written here: `job_id`, `owner_role`, `expected_minutes`, `alert_after_minutes` and `runbook_path` DF-OPS-224 to DF-OPS-232 | DF-OPS-224 to DF-OPS-232 |
| Freshness rows | Read only: DF-OPS-001 to DF-OPS-008 of `data_product_load` | DF-OPS-001 to DF-OPS-008 |
| ACE rows | `v_ace_batch_status` DF-ACE-178 to DF-ACE-186, read through the service's own `recovery.v_ace_*` path only | DF-ACE-178 to DF-ACE-186 |
| Values files | Replica counts, resource sizes, probes, thresholds, channels and retention per environment; no business value | Not specified in the source documents (DOR-RWB-P1-AD018-OPS-7) |

The capability stores nothing personal and copies no ACE row: the panels, the alerts and the run books read identifiers, codes, dates, counts and durations.

The run status is one of five values: PENDING, RUNNING, COMPLETE, FAILED or WAITING. The monitor lists the Workbench jobs it owns from its own job map and the ACE batch record. The freshness answer is served by this monitor and owned by RWB-P1-E1015-CON; no field is restated here.

### 12. Contract

#### 12.1 REST operations provided

None by this story. It deploys the three operations of RWB-P1-AD018-CON — `GET /api/recovery/source-data/v1/admin/jobs`, `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` and `GET /api/recovery/source-data/v1/data-products/freshness` — and declares no operation of its own. The composite route is the platform's (RWB-PLT-N001-CON, DP-19).

#### 12.2 REST operations consumed

None deployed or consumed by this story. The outbound-action mock of RWB-P1-AD018-CON is loaded in the SIT smoke profile only, so the smoke step exercises the same answer the app story builds on.

#### 12.3 Events published

None. The two events of the service, `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1`, are published by RWB-P1-E1015-APP; this release publishes nothing and declares no producer of its own.

#### 12.4 Events consumed

None. The release declares no consumer group and binds no subscription; the events of the service are consumed by the inbox of RWB-P1-E1015-APP.

#### 12.5 Workflows and activities

None new. The worker deployment continues to poll task queue `rwb-source-data` in namespace `rwb-recovery` with the build ID of the release, so the jobs this monitor shows run on their own workflows, for example `ReconciliationWorkflow` of RWB-P1-E1011-APP.

#### 12.6 Schedules

None. The release registers no Temporal Schedule and no Quartz trigger; the jobs shown by the monitor start on the ACE batch record as their own stories state, and `JOB-01` and `JOB-09` stay retired.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| run log (name pending, GAP-2164) | P1 (rwb_source_data) | Created and migrated by this release; the app story writes and reads it |
| job_catalog, data_product_load | P1 (rwb_source_data) | Read only here; loaded by RWB-PLT-E1056-OPS and stamped by RWB-P1-E1015-APP |
| Flyway history of the service | P1 (rwb_source_data) | The per-service migration record of this release |

`v_ace_batch_status` belongs to ACE and is reached only through `recovery.v_ace_*`; the release holds no grant on `public` and no cross-schema access (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Environment | Use |
|---|---|---|
| rwb-integration outbound-action mock | SIT and UAT smoke only | Makes the outbound columns of the answer present in the smoke profile |
| `v_ace_batch_status` fixture | SIT and UAT smoke only | A complete source, a source with no complete row and a FAILED source |
| Session and role fake | SIT only | The R and U rights granted and the U right refused |
| Run-log seed of a synthetic failed job | SIT and UAT smoke only | Proves the rerun and the two visible runs of AC6 |

The fakes never run in production: in the production environment every answer is the real one, and a missing answer is shown as unknown rather than faked.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 deployed, none declared here | The two admin operations and the freshness answer of RWB-P1-AD018-CON |
| Kafka | None | No topic, producer or consumer group declared by this release |
| Temporal | 1 worker on `rwb-source-data`, no Schedule | The jobs of the service run on their own workflows |
| File | None | No file path is deployed and no data lake is reached |

### 13. Solution plan

**Deliverables.** The Helm chart with its three values files, the pipeline stage, the pre-deploy migration job, the nine panels, the six alert rules, the five run-book entries and the SIT smoke profile.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none; the release assert that no `public` path exists |
| DP-13 | `/api/recovery/v1` | `/api/recovery/source-data/v1` | none; the smoke profile uses the per-service base |
| DP-19 | Screen, ace-web | gateway-bff composite route | none for the deployment; the route is RWB-PLT-N001-CON |

No pattern is claimed for the outbox, Drools or a Schedule: this release publishes no event, evaluates no rule and registers no timer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Chart and values | Deployment artefact | api and worker deployments, the login reference, probes, resources and thresholds per environment |
| Migration job | Pre-deploy job | Runs the per-service Flyway sequence in `rwb_source_data` and creates the run log |
| Boundary assertion | Pipeline step | Fails a release that declares a topic, a consumer group, a Schedule or an ACE path |
| Dashboard set | Observability artefact | The nine panels of AC4 |
| Alert rules | Observability artefact | The six rules of AC5, each with a values threshold and a catalogue owner |
| Run books | Operations artefact | The five entries listed below, one per failure an operator sees |
| Smoke profile | Test artefact | The SIT and UAT journey of AC6 through the composite route |

**Run-book entries.** (1) A job failed: read its failed check and message ID, fix the cause, rerun from the run book and confirm two runs. (2) A run is WAITING: read the last complete ACE date of its source, raise MSG-P1-001 to the data steward, and take no Workbench action on the ACE feed. (3) A rerun is refused: check a running run, then the business date in `v_ace_batch_status`. (4) A product is STALE with no business date: confirm the Section B view and the batch row before raising it as an incident. (5) The monitor read fails: check the composite route, then the service health, then the database session.

**Build steps**

1. Chart and values with the login reference, the probes and the pinned image digest; tests for AC1.
2. The pre-deploy migration job and the run-log creation; a failed migration stops the release.
3. The boundary assertion of AC3, including the ACE path, the data lake and the retired `JOB-01` and `JOB-09`.
4. The nine panels of AC4 and the six alert rules of AC5, each threshold from the values file and each owner from the catalogue.
5. The five run-book entries with their message IDs, first checks and escalation.
6. The SIT smoke profile through the composite route, with one rerun and one 409; tests for AC6.
7. The alert rehearsal: one synthetic metric per rule, with its owner and its channel recorded.

**Done when.** The chart renders in the three environments, the boundary assertion passes on the release and fails on a deliberate breach, the nine panels carry data for a synthetic business date, each of the six alerts fires in the rehearsal, and the smoke profile proves two runs of a rerun and the 409.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A run waits for its ACE batch, or a product is STALE | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A required field is missing, or the job code is unknown | Enter {field}. |
| MSG-P4-002 | A role lacks Platform administration R or U | You cannot {action} here. Your role does not include it. |

MSG-P1-001 is copied from the Error and Message Standard v4 and the other two texts are copied unchanged from the legacy story; no threshold, channel or owner name is written here. The Platform administration right is taken from the platform session, and MSG-P4-002 is the refusal. The alert thresholds are Not specified in the source documents (GAP-2164; ASM-3468) and are values-file entries; the 15-minute target of a failed job comes from NFR-068.

### 15. Screens and states

SCR-44 Interface and job monitor in its four states — Running, failed, waiting for the ACE batch, complete — is served through the gateway-bff composite route (DP-19). This story proves the four states in the SIT smoke profile and in the panels; it builds no screen and fixes no field, and the panels of the app story are its only consumer. The other states of SCR-44 are these. Empty: a plain sentence saying there is nothing to show, and the action to take if one applies. Loading: skeleton rows while data arrives, with no spinner over the whole page. Error: the message from the error and message standard next to the field or at the top. No access: a role without the Platform administration right is refused with MSG-P4-002. This story registers the gateway-bff composite route for SCR-44 and its alerts; RWB-P1-AD018-APP serves the reads and RWB-P1-AD018-CON publishes them (GAP-0516).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-AD018-OPS-01 | AC1 | Component | The chart rendered for three environments; the migration job; the probes; the login reference |
| TC-P1-AD018-OPS-02 | AC2 | Component | One pipeline run; the contract tests of the baseline; the scan; the promotion without a rebuild |
| TC-P1-AD018-OPS-03 | AC3 | Component | The assertion passes on the release and fails on a declared topic, consumer group, Schedule or ACE path |
| TC-P1-AD018-OPS-04 | AC4 | Component | A synthetic business date with a complete run, a failed run and a waiting run; nine panels |
| TC-P1-AD018-OPS-05 | AC5 | NFR | One synthetic metric per rule; the owner role from the catalogue; the 15-minute failed-job target |
| TC-P1-AD018-OPS-06 | AC6 | End to end | The SIT smoke through the composite route; two runs after a rerun; a 409 with MSG-P1-001 |
| TC-P1-AD018-OPS-07 | §12.7 tables (ASM-3438) | Component | The tables of section 12.7 at their boundary values |
| TC-P1-AD018-OPS-08 | AC7, BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 | Component | One synthetic check per rule in section 8 |

The four legacy test cases TC-AD-018-01 to TC-AD-018-04 are owned by RWB-P1-AD018-APP and RWB-ITG-AD018-ITG, which copies them with the `-ITG` suffix; a deployment story owns no business outcome and therefore no legacy test case.

### 17. Guardrails

- No business value in the chart or the code: job names, cadences, expected durations, alert minutes, owners and thresholds are catalogue or values rows.
- No personal data in a panel, a log line, a trace or a run book: identifiers, codes, dates, counts and durations only.
- One login for the service and no ACE credential; no grant on `public` and no cross-schema access (DP-01, DP-02, DP-05).
- No release adds a path, a credential or a job name that can start, stop or rerun an ACE batch, a feed or a file.
- No topic, consumer group or Schedule is declared by this release; the service topic stays as its owner provisioned it.
- No data lake, no ADF job and no inbound load path is deployed (DP-17).
- Every threshold, channel and owner is a values-file or catalogue entry, and the assertion of AC3 fails a release that writes one in the chart.

### 18. Traceability

| Requirement ID | Requirement (short) | Artefact | Test cases |
|---|---|---|---|
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel | The nine panels, the six rules and the five run-book entries | TC-P1-AD018-OPS-04, TC-P1-AD018-OPS-05, TC-P1-AD018-OPS-06 |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target | The failed-job rule with the catalogue owner role and the 15-minute target | TC-P1-AD018-OPS-05 |
| REQ-DRI-007 | Every outbound file is logged, retried and placed in a named exception queue on failure | The outbound columns on the panel and the mock of the smoke profile | TC-P1-AD018-OPS-04, TC-P1-AD018-OPS-06 |
| REQ-DRI-008 | The Workbench runs no inbound batch; work starts when ACE records the batch complete | The wait-state panel, the boundary assertion and the run-book entry for a waiting run | TC-P1-AD018-OPS-03, TC-P1-AD018-OPS-05 |
| ADR-023 | Observability per service: metrics, traces and logs with one trace | The chart, the dashboard set and the alert rules | TC-P1-AD018-OPS-01, TC-P1-AD018-OPS-04 |

### 19. Out of scope

- The implementation of the two reads, the rerun and the run log (RWB-P1-AD018-APP) and the contract baseline that fixes them (RWB-P1-AD018-CON).
- The catalogue baseline, the run books' content and the Epic 1 monitoring workbook (RWB-PLT-E1056-OPS).
- The freshness stamp and its events (RWB-P1-E1015-APP, RWB-P1-E1015-OPS), the reconciliation behind JOB-04 (RWB-P1-E1011-APP) and the ACE read path (RWB-P1-E1069-APP).
- The screen composition and the composite route (RWB-PLT-N001-CON).
- The Platform administration roles and their assignment (RWB-P4-AD001 to RWB-P4-AD016).
- The cross-service journey with the real ACE batch and the real outbound actions (RWB-ITG-AD018-ITG).
