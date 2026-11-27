# RWB-P9-E1013-OPS Baseline measures - deployment

**Version 3 changes.**

- RD-P1-066: Align the JOB-15 start and deployment with the Airflow call and paused Schedule.
- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E1013-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P9-B |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P9-E1013-OPS-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P9-E1013-CON |
| Contract version | Exact contract version Not specified in the source documents (DOR-RWB-P9-E1013-OPS-23) |
| Readiness decisions | RD-P1-004, RD-P1-066 |
| Integration dependencies | None |
| External dependencies | Platform and operations stories register the 05:30 late-check Schedule, its worker, queue and topic (GAP-0561) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (no FR mapped to REQ-RDF-012) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-013 for rwb-reporting. It deploys the measures capability of the service from the template with its own login and its per-service migration for the three tables and the frozen-row trigger, registers the 01:30 run of JOB-15 once as a Temporal Schedule and no Quartz row, publishes the panels for the run, the gate, the publish state and the freshness stamp, wires the alerts to the message IDs of the feature within the 15-minute target, and publishes the run books for a held run, a stale product, a refused rerun and a failed run. It declares no topic, no consumer group, no lake path and no outbound extract (GAP-2566, GAP-2573, GAP-2574, GAP-2575; ASM-4232, ASM-4239, ASM-4240, ASM-4241). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 34 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the measures capability of rwb-reporting deployed from the service template with its own login, its migration for the three tables and the frozen-row trigger, its 01:30 Schedule registered once, the panels for the run, the gate answer, the publish state and the freshness stamp, the alerts wired to MSG-P9-001, MSG-P9-003, MSG-P1-001, MSG-GEN-006 and MSG-P7-003 within the 15-minute target, and the run books for a held run, a stale product, a refused rerun, a failed run and a slow read**, so that **an operator finds a held publish or a late ACE batch before the working day without reading code, and no release can quietly restore the data lake, a Quartz trigger, a second Schedule or a second source of truth for the baseline**.

This story deploys an existing capability. It adds no topic, no consumer group, no endpoint and no measure: the three tables are rows of `rwb_reporting`, the run is the Schedule of DP-10, the facts and the gate are read on the P3 and P1 contracts, and SCR-44 is reached through the gateway-bff route.

### 2. Business rationale

The legacy story had one module, one Quartz row and one operator, and its failure signals were a run record nobody watched outside office hours: a baseline that published twice, a definition loaded without a formula and a lake that did not answer were all found at month end. In the target the measures are a service with its own release, its own login, its own Schedule and its own alerting (DP-02, ADR-023), and the operational question changes from "did the job run" to four separate questions: did the run start, is it waiting for the gate, did it publish or hold, and is the value of a date explained by its definition version (NFR-067, NFR-068).

Two failures are separated on purpose. A **failed** run is an incident of this service and pages the owner role of the catalogue row. A **held** run is a signal about a source: it pages nobody, it raises MSG-GEN-006 or MSG-P1-001 to the data steward and the operations channel, and the run book says in one line that no Workbench action will make the ACE batch arrive. Deployment is part of the capability because a chart that carries a second credential, a release that re-adds a lake egress path, or a Schedule registered twice would break the guardrails the story set was built on (DP-17, DP-10).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across the composite route and the service.
- The workflow kit is available (RWB-PLT-E1071-CON, DP-10) and namespace `rwb-recovery` exists with queue `rwb-reporting`, so the Schedule of the run can be registered and polled.
- The Kafka event platform is available (RWB-PLT-EVT); `rwb.reporting.events.v1` and its retry and `.dlt` topics exist by the naming rule, and this release publishes to none of them and subscribes to none.
- RWB-P9-E1013-CON is published, so the smoke profile and the drift test run against the two reads, the reference-load element and the six fakes of that baseline.
- RWB-PLT-E1056-OPS loads the catalogue baseline with `owner_role`, `expected_minutes`, `alert_after_minutes` and `runbook_path` for JOB-15, so every alert and every run-book link resolves to an owner without a code change. The threshold values have no source and are values-file entries (GAP-2574; ASM-4240).
- The three environments DEV, SIT and UAT exist with their platform session, their database endpoint and their Temporal endpoint.
- The three tables of the capability are created by the app story's migration, and this release runs the same per-service sequence before the deployment is marked ready (DP-15; GAP-2575; ASM-4241).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-reporting with the rwb-reporting login, the pre-deploy migration job that runs the per-service Flyway sequence in `rwb_reporting` — the three tables, their unique keys and the trigger that refuses an UPDATE or a DELETE of a frozen row — and the readiness and liveness probes of the api deployment.
3. The worker deployment polls queue `rwb-reporting` in namespace `rwb-recovery` with the build ID of the release, so the workflow of the 01:30 run is available before the first tick.
4. The provisioning step registers the Schedule of JOB-15 once, paused (RD-P1-066), at 01:30 Asia/Bangkok, one run per business date, catch-up of one missed run, no overlapping execution, and asserts that no Quartz trigger, no shared job table and no second Schedule of this job exists.
5. The provisioning step asserts that the release declares no topic, no consumer group, no event and no lake path: no INT-19 or INT-20 client, no extract writer, no trailer builder, no outbound batch and no route to a data store outside the cluster (DP-17).
6. The dashboards are published: runs by business date with their state, duration against `expected_minutes`, the gate answer by product, the publish state and the hold reason, the freshness stamp lag, the frozen row count, the refused rerun count, and the read latency and error rate of the two operations.
7. The alerts are wired to the message IDs of section 14 and to the run-book entries of section 13; each threshold and each channel is a values-file entry and each owner role comes from the catalogue row of JOB-15.
8. A smoke step in the SIT profile calls the two reads through gateway-bff for a synthetic business date, reruns JOB-15 for the baseline date and asserts that the frozen rows are unchanged and the run record carries MSG-P9-001, and asserts that a forced record failure leaves no snapshot row behind.
9. The run books are published and reviewed with the on-call rota: a held run for a stale product, a refused rerun of a frozen date, a failed run, a slow or failed read, and a publish that stays held after two runs.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails, or the frozen-row trigger is missing after it | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | A release declares a topic, a consumer group, an event or a Schedule of its own | The provisioning assertion fails the release | None | AC3 |
| X3 | A release adds a lake path, an extract writer, a trailer or an outbound batch | The boundary assertion fails the release | None | AC3, AC6 |
| X4 | A run fails | The failed-run alert fires within the 15-minute target to the owner role of the catalogue row | None | AC5 |
| X5 | A run waits because the gate answer is HOLD | The wait panel rises, MSG-P1-001 is raised to the data steward and the operations channel, and no page is sent | MSG-P1-001 | AC5 |
| X6 | A publish stays held after two runs | The hold panel rises with the reason, MSG-GEN-006 follows the run book entry | MSG-GEN-006 | AC4, AC5 |
| X7 | A rerun of the baseline date is refused | The refused-rerun count rises and the run book entry explains the frozen rule | MSG-P9-001 | AC6 |
| X8 | A measure is listed with no definition in force | The run record names it, the panel counts it and the entry names the loader | MSG-P9-003 | AC4, AC5 |
| X9 | A read is slow or fails | The read latency and error-rate alerts fire; the composite route is checked before the service | None | AC4, AC5 |
| X10 | The smoke step cannot see the second run after a rerun, or sees a changed frozen row | The release stops; the run log, the Schedule history and the trigger are checked | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform provisioning, the observability stack and the published contract baseline; builds no application code and no measure |
| Negotiable | Replica counts, resource sizes, retention, thresholds and channel names are environment values, not story decisions |
| Valuable | Turns the measures into an operated capability with an owner, a signal and a run book for each of its five failures |
| Estimable | One chart, one pipeline stage, one migration job, one Schedule registration, two probes, eight panels, six alert rules and five run-book entries |
| Small | Fits one sprint with the run books |
| Testable | Every criterion tests an artefact: the chart renders, the assertions pass, the panels carry data, an alert fires on a synthetic metric, a run-book entry resolves |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the baseline measures of rwb-reporting

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart and values deploy rwb-reporting with its own login and its migration with the frozen-row trigger (new, D-RCV-60)
    Given the rwb-reporting Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-reporting login reference and no other service's credential and no ACE credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_reporting and creates measure_definition, measure_snapshot and measure_publish with their unique keys, the publish row keyed on business_date, and the trigger that refuses an UPDATE or a DELETE where frozen = true
    Then the migration is idempotent and a second run of it changes nothing
    Then the api deployment answers its readiness and liveness probes on the health operation of the template, and the worker deployment polls queue rwb-reporting in namespace rwb-recovery
    Then no replica count, resource size, timeout or threshold is hard-coded in the template

  Scenario: AC2 The pipeline promotes one artefact and runs the contract tests (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit and component tests of RWB-P9-E1013-APP and the contract tests of RWB-P9-E1013-CON and fails the build on a drift between a fake and the document
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 The Schedule is registered once and the release carries no topic, no consumer group and no lake path (new, D-RCV-60)
    Given the provisioning step of rwb-reporting for the measures capability
    When it runs against the environment
    Then exactly one Schedule exists, paused, for the run of JOB-15, at 01:30 Asia/Bangkok, one run per business date, catch-up of one missed run and no overlapping execution, registered on queue rwb-reporting in namespace rwb-recovery
    Then the release declares no Quartz trigger, no shared job table and no second Schedule for the same job, and the assertion fails the release when a second one appears
    Then the release declares no topic of its own, no consumer group and no event, and rwb.reporting.events.v1 keeps the partitions, the retention and the retry and .dlt topics of the platform
    Then the assertion fails the release when the chart carries an INT-19 or INT-20 client, an extract writer, a trailer builder, an outbound batch or any path to a data store outside the cluster
    Then no release adds a credential or a job name that can start or rerun an ACE batch or read an ACE table

  Scenario: AC4 The eight panels show the five operational questions (new, D-RCV-60)
    Given the published dashboard of rwb-reporting
    When it is opened for a business date
    Then it shows the runs of that date with their state, rerun and complete, and the duration of each against its expected_minutes from the catalogue
    Then it shows the gate answer by product with the date of the product and the count of products in HOLD
    Then it shows the publish state of the date with its hold reason and the lag of its freshness stamp
    Then it shows the frozen row count of the baseline date and the count of refused reruns
    Then it shows the runs that wrote no value for a measure with no definition in force, and the read latency and error rate of the two operations
    Then every panel reads an identifier, a code, a date, a count or a duration and no customer field

  Scenario: AC5 The alerts fire to the catalogue owner within the 15-minute target (new, D-RCV-60)
    Given the alert rules of the capability and their values-file thresholds
    When a synthetic metric crosses each rule
    Then a failed run alerts the owner_role of its catalogue row within 15 minutes of the failure
    Then a run in its waiting state past its cut-off raises MSG-P1-001 to the data steward and the operations channel and pages nobody
    Then a publish held for two runs raises MSG-GEN-006 with its reason and links the run-book entry
    Then a measure with no definition in force raises MSG-P9-003 and links the loader run book
    Then a read error or a latency above its threshold alerts the platform administrator role
    Then every threshold is a values-file entry and no threshold, owner or channel is written in the chart or the code

  Scenario: AC6 The run books and the smoke profile prove the frozen baseline and the absent lake (new, D-RCV-60)
    Given the run books of section 13 and the SIT smoke profile
    When the smoke step runs through gateway-bff
    Then it reads the measures and the definitions of a synthetic business date on the two operations of the baseline
    Then it reruns JOB-15 for the baseline date and receives MSG-P9-001, and the frozen rows of measure_snapshot are unchanged and the trigger refuses a direct UPDATE of one of them
    Then a forced record failure leaves no snapshot row, no publish state and no baseline flag behind
    Then the smoke profile and the release manifest name no data lake, no INT-19 extract, no trailer and no outbound batch
    Then each of the five run-book entries names its message ID, its first check, its owner role and its escalation
```

These six criteria are new for the deployment of the capability and test artefacts only; they restate no business outcome owned by RWB-P9-E1013-APP and copy no criterion of the legacy story. The wave 1 harness RWB-ITG-E1013-ITG consumes the deployed capability and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login per service and no ACE credential in the release; grants on `rwb_reporting` only | DP-02; RWB-PLT-TPL |
| BR2 | The per-service Flyway sequence owns the schema objects the release needs, and no other service's schema is touched; the frozen-row trigger is part of the release and an absent trigger fails it; the release replays the migration carried by RWB-P9-E1013-APP | DP-15; ADR-021; legacy BR2 |
| BR3 | The run is one Schedule of this service and no Quartz row, no shared job table and no second Schedule of the same job | DP-10; ADR-016; GAP-2573 |
| BR4 | The release declares no topic, no consumer group and no event; the topic of the service stays as the platform provisioned it | DP-09, DP-14; GAP-2569 |
| BR5 | No release adds a lake path, an extract writer, a trailer or an outbound batch, and no release adds a path that reads an ACE table | DP-17; ADR-018; GAP-2566 |
| BR6 | A failed run alerts its catalogue owner role within 15 minutes; a held run raises its message and pages nobody; the held publish is the one caller of MSG-GEN-006 | NFR-068; RWB-P9-E1013-APP BR8 |
| BR7 | Every threshold, channel and owner is a values-file or catalogue entry, never code | NFR-067; Template and Rules v1 §R7.2 (s17) |
| BR8 | One artefact is promoted through the three environments without a rebuild | ADR-023; Template and Rules §R8 |
| BR9 | The panels, the alerts and the run books read identifiers, codes, dates, counts and durations only; no personal data reaches a panel, a log line or a trace | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Pipeline run | The pipeline and the boundary assertions pass | Deployed to DEV |
| Deployed to DEV | Promotion | The smoke profile passes | Deployed to SIT |
| Deployed to SIT | Promotion | The smoke profile, the panels and one alert per rule pass | Deployed to UAT |
| Deployed | A run fails or waits | The alert rule fires | Alerted, run book entry opened |
| Alerted | Run book completed | The run completes after the gate answers COMPLETE, or the cause is cleared | Recovered, the alert closes |
| Deployed | A release declares a topic, a consumer group, an event, a second Schedule or a lake path | The assertion fails | Release refused; the previous version keeps running |
| Deployed | The Schedule is registered a second time | The provisioning step refuses the second registration | Unchanged, one Schedule |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps team | Owns the chart, the values files, the pipeline stage, the Schedule registration, the panels, the alert rules and the run books |
| RW-PLATADM, platform administrator | Reruns JOB-15 from SCR-44 and reads the run state (Platform administration U) |
| RW-DATASTEW, data steward | Receives the held-publish and stale-product alerts (Reporting CRU) |
| RW-BIANAL, Reporting and BI analyst | Reads the publish state, the freshness stamp and the run history (Reporting CRUD) |
| Owner role of the JOB-15 catalogue row | Receives the failed-run alert of that job |
| Platform observability owner | Owns the metrics, panels, alerts and traces this story consumes |
| No role | Reruns an ACE batch, reads an ACE table, or deploys a lake path or a second Schedule |

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Tables deployed | `measure_definition`, `measure_snapshot` and `measure_publish` in `rwb_reporting` with their unique keys and the frozen-row trigger; created by the app story's migration and replayed by this release (GAP-2575; ASM-4241) | BR1; BR2 |
| Decision record | The library object of DP-03 in `rwb_reporting`, present but neither read nor written by this release | BR2 |
| Catalogue rows | Read, never written here: `job_id`, `owner_role`, `expected_minutes`, `alert_after_minutes` and `runbook_path` of the JOB-15 row (DF-OPS-224 to DF-OPS-232) | BR7 |
| Panel rows | Read only: the run state and duration, the gate answer by product, the publish state and its reason, the freshness stamp, the frozen row count and the refused rerun count | BR9 |
| Values files | Replica counts, resource sizes, probes, thresholds, channels and retention per environment; no business value | BR7 |
| Not present | No lake path, no INT-19 extract, no trailer and no outbound batch (DP-17) | BR5 |

The capability stores nothing personal and copies no case or payment row: the panels, the alerts and the run books read identifiers, codes, dates, counts and durations.

### 12. Contract

#### 12.1 REST operations provided

None by this story. It deploys the two reads and the reference-load element of RWB-P9-E1013-CON — `GET /api/recovery/reporting/v1/reports/measures`, `GET /api/recovery/reporting/v1/measure-definitions` and the reference-load element of table `measure_definition` — and declares no operation of its own. The composite route is the platform's (RWB-PLT-N001-CON, DP-19).

#### 12.2 REST operations consumed

None consumed by this story at run time. The smoke profile calls the two reads through gateway-bff, and the P3 and P1 fakes of RWB-P9-E1013-CON stand behind them in SIT.

#### 12.3 Events published

None. The service topic `rwb.reporting.events.v1` exists by the naming rule with its retry and `.dlt` topics, and this release publishes nothing and declares no producer of its own. The event question that the wave 1 harness raises is recorded in the contract baseline of this key and not resolved here (GAP-2569; ASM-4235).

#### 12.4 Events consumed

None. The release declares no consumer group and binds no subscription; the run starts on the Airflow report-run call while the Schedule is paused (RD-P1-066) and reads its sources on the two contracts.

#### 12.5 Workflows and activities

None new. The worker deployment polls queue `rwb-reporting` in namespace `rwb-recovery` with the build ID of the release, so `MeasureRunWorkflow` and its `measureRun` activity of RWB-P9-E1013-APP are available before the first report-run call and before the Schedule is ever unpaused.

#### 12.6 Schedules

Airflow calls `POST /reports/{id}/run` at 01:30 Asia/Bangkok for the prior business date. Create the JOB-15 Temporal Schedule paused. Pending final trigger owner: solution architect with the rwb-reporting owner (GAP-3573).

One, registered by this story: the run of JOB-15 at 01:30 Asia/Bangkok for the previous business date, one run per date, catch-up of one missed run and no overlapping execution, on `rwb-reporting` in namespace `rwb-recovery` (DP-10). The registration is idempotent and a second one is refused; no Quartz row and no shared job table is deployed. While the Schedule is paused, the one live trigger is the Airflow report-run call (RD-P1-066; GAP-3573; earlier reading GAP-2573, ASM-4239).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| measure_definition | P9 (`rwb_reporting`) | Deployed and migrated here; written by the app story's load |
| measure_snapshot | P9 (`rwb_reporting`) | Deployed and migrated here, with the unique key and the frozen-row trigger |
| measure_publish | P9 (`rwb_reporting`) | Deployed and migrated here, keyed on the business date |
| Flyway history of the service | P9 (`rwb_reporting`) | The per-service migration record of this release |

No table of rwb-case, rwb-source-data or rwb-decision is touched, and the release holds no `v_ace_*` grant (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Environment | Use |
|---|---|---|
| rwb-case case-facts fake | SIT and UAT smoke only | Gives the run a business date of facts to compute from |
| rwb-source-data payments and freshness fake | SIT and UAT smoke only | A gate answer COMPLETE and a HOLD with a stale product |
| gateway-bff composite route fake | SIT only | The merged SCR-44 answer with the run of the baseline date |
| Frozen-row seed | SIT and UAT smoke only | Proves the refused rerun, MSG-P9-001 and the trigger |
| Forced record failure switch | SIT only | Proves that a failed record leaves no snapshot row and no publish state |

The fakes never run in production: in the production environment every answer is the real one, and a missing answer is shown as unknown rather than faked.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 reads deployed, 1 element deployed, none declared here | The measures read, the definitions read and the reference-load element of RWB-P9-E1013-CON |
| Kafka | None | No topic, producer or consumer group declared by this release |
| Temporal | 1 worker on `rwb-reporting` and 1 Schedule | The run of JOB-15 at 01:30 and the workflow of the app story |
| File | None | No file path is deployed; the lake, INT-19 and its extract are removed (DP-17) |

### 13. Solution plan

**Deliverables.** The Helm chart with its three values files, the pipeline stage, the pre-deploy migration job, the Schedule registration and its idempotency assertion, the eight panels, the six alert rules, the five run-book entries and the SIT smoke profile.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_reporting`; never read another service's tables | none; the release asserts no cross-schema grant |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | none for the deployment; the library object is present and untouched |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none; the release asserts no ACE read path |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | none for the deployment; the lists are read at run time by the app |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | one Schedule registered; no Quartz row |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none; the smoke profile uses the fakes |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1` | none; the smoke profile uses the per-service base |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | the migration job, replayed from the app story |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; the release asserts no lake egress (GAP-2566) |
| DP-19 | Screen, ace-web | gateway-bff composite route | none for the deployment; the route is RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Chart and values | Deployment artefact | api and worker deployments, the login reference, probes, resources and thresholds per environment |
| Migration job | Pre-deploy job | Replays the per-service Flyway sequence, the three tables, their keys and the frozen-row trigger, and fails the release when the trigger is absent |
| Schedule registration | Provisioning step | Registers the 01:30 run once and refuses a second registration |
| Boundary assertion | Pipeline step | Fails a release that declares a topic, a consumer group, an event, a second Schedule or a lake path |
| Dashboard set | Observability artefact | The eight panels of AC4 |
| Alert rules | Observability artefact | The six rules of AC5, each with a values threshold and a catalogue owner |
| Run books | Operations artefact | The five entries below |
| Smoke profile | Test artefact | The SIT journey of AC6 through the composite route |

**Run-book entries.** (1) A publish is held for a stale product: read the gate answer and the product date, raise MSG-P1-001 to the data steward, and take no Workbench action on the ACE batch. (2) A rerun of the baseline date is refused: read the frozen date and MSG-P9-001, confirm the rows, and do not attempt a write around the trigger. (3) A run failed: read its failed step and message ID, fix the cause, rerun from SCR-44 and confirm the run record. (4) A measure was not published: read MSG-P9-003, confirm the definition version in force, and hand the row to the reference data administrator. (5) A read is slow or fails: check the composite route, then the service health, then the database session.

**Build steps**

1. Chart and values with the login reference, the probes and the pinned image digest; tests for AC1.
2. The pre-deploy migration job, the three tables, their keys and the frozen trigger, with the trigger assertion; a failed or missing trigger stops the release.
3. The Schedule registration and its idempotency assertion, including the refusal of a second Schedule and the absence of a Quartz row (AC3).
4. The boundary assertion of AC3, including the lake, the INT-19 extract, the trailer, the event and the consumer group.
5. The eight panels of AC4 and the six alert rules of AC5, each threshold from the values file and each owner from the catalogue.
6. The five run-book entries with their message IDs, first checks and escalation.
7. The SIT smoke profile through the composite route, with the refused rerun and the forced record failure (AC6).
8. The alert rehearsal: one synthetic metric per rule, with its owner and its channel recorded.

**Done when.** The chart renders in the three environments, the migration creates the three tables and the trigger and is idempotent, exactly one Schedule exists and a second is refused, the boundary assertion passes on the release and fails on a deliberate breach, the eight panels carry data for a synthetic business date, each of the six alerts fires in the rehearsal, and the smoke profile proves the refused rerun with the frozen rows unchanged and the absent lake.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P9-001 | A rerun of the baseline date is refused, and the panel and the run book show it | The baseline for {date} is frozen. It cannot be published again. |
| MSG-P9-003 | A measure listed for a run has no definition in force | {measure} has no approved definition. It is not published. |
| MSG-P1-001 | The gate answer for a business date is HOLD and a run waits | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | A publish stays held with its reason | {system} is not available. Try again in a few minutes. |
| MSG-P7-003 | The run record cannot be written and the run changes nothing | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | A definition row is invalid and the load is refused | Enter {field}. |
| MSG-P4-002 | A role lacks Reporting R or Reference data C | You cannot {action} here. Your role does not include it. |

The texts are copied unchanged from the legacy story and FSD P9; no threshold, channel or owner name is written here. The alert thresholds and the channel names are Not specified in the source documents (GAP-2574; ASM-4240) and are values-file entries; the 15-minute target of a failed run comes from NFR-068.

### 15. Screens and states

SCR-44 Interface and job monitor in its four states — running, waiting for the gate, held and complete — is served through the gateway-bff composite route (DP-19). Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-7828). This story proves the four states in the SIT smoke profile and in the panels; it builds no screen and fixes no field, and the run record and the publish state shown there are the app story's. The baseline report itself is read from the snapshot by the Reporting and BI analyst, and SCR-37 Steering dashboard is RWB-P9-E2009-APP's; its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-7827).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P9-E1013-OPS-01 | AC1 | Component | The chart rendered for three environments; the migration and its replay; the frozen-row trigger; the probes and the login reference |
| TC-P9-E1013-OPS-02 | AC2 | Component | One pipeline run; the contract tests of the baseline; the scan; the promotion without a rebuild |
| TC-P9-E1013-OPS-03 | AC3 | Component | The Schedule registered once and a second registration refused; the assertion passes on the release and fails on a declared topic, event, Schedule or lake path |
| TC-P9-E1013-OPS-04 | AC4 | Component | A synthetic business date with a complete run, a held publish and a measure without a definition; eight panels |
| TC-P9-E1013-OPS-05 | AC5 | NFR | One synthetic metric per rule; the owner role from the catalogue; the 15-minute failed-run target |
| TC-P9-E1013-OPS-06 | AC6 | End to end | The SIT smoke through the composite route; the refused rerun with MSG-P9-001 and unchanged frozen rows; a forced record failure; no lake path |
| TC-P9-E1013-OPS-07 | AC1 | Component | Boundary of the section 12.7 tables: the three tables and the Flyway history of rwb_reporting only; no table of rwb-case, rwb-source-data or rwb-decision touched; no v_ace_* grant |

The seven legacy test cases of RWB-E1-013 are owned by RWB-P9-E1013-APP and RWB-P9-E1013-CON, and their `-ITG` copies by RWB-ITG-E1013-ITG; a deployment story owns no business outcome and therefore no legacy test case.

### 17. Guardrails

- No business value in the chart or the code: the measure codes, the formulas, the units, the baseline date, job names, cadences, expected durations, alert minutes, owners and thresholds are rows of the catalogue, of the definitions or of the values files.
- No personal data in a panel, a log line, a trace or a run book: identifiers, codes, dates, counts and durations only.
- One login for the service and no ACE credential; no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-02, DP-05).
- No release adds a lake path, an INT-19 extract, a trailer or an outbound batch (DP-17).
- Exactly one Schedule for the run, no Quartz row and no shared job table; a second registration is refused (DP-10).
- No topic, consumer group or event is declared by this release; the service topic stays as the platform provisioned it (DP-14).
- Every threshold, channel and owner is a values-file or catalogue entry, and the assertion of AC3 and AC5 fails a release that writes one in the chart.
- The frozen-row trigger is part of the release: a migration that creates the tables without it fails the release (BR2).

### 18. Traceability

| Requirement ID | Requirement (short) | Artefact | Test cases |
|---|---|---|---|
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel | The eight panels, the six rules and the five run-book entries | TC-P9-E1013-OPS-04, TC-P9-E1013-OPS-05, TC-P9-E1013-OPS-06 |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target | The failed-run rule with the catalogue owner role and the 15-minute target | TC-P9-E1013-OPS-05 |
| REQ-RDF-012 | Baseline measures published with definitions agreed by the Tribe | The deployed reads, the migrated tables with the frozen-row trigger and the Schedule of the run | TC-P9-E1013-OPS-01, TC-P9-E1013-OPS-03, TC-P9-E1013-OPS-06 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The Schedule registration and the absent Quartz row | TC-P9-E1013-OPS-03 |
| ADR-018 | No data lake; rwb-reporting read model | The boundary assertion and the smoke profile | TC-P9-E1013-OPS-03, TC-P9-E1013-OPS-06 |
| ADR-023 | Observability per service: metrics, traces and logs with one trace | The chart, the dashboard set and the alert rules | TC-P9-E1013-OPS-01, TC-P9-E1013-OPS-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E1-013, disposition Split (rework); features FEAT-RDF-19 and FEAT-RPT-01 |
| Legacy criteria | AC1, AC3, AC4, AC5, AC7 and AC8 with RWB-P9-E1013-APP; AC2 and AC6 with RWB-ITG-E1013-ITG; this story owns none |
| Source text | The legacy story, FSD P9 Reporting v3 A2.1 and A2.8, TSD P9 Reporting v2 T3.1 and T7, and Architecture v5 slides 9 and 44 |
| Test cases | TC-P9-E1013-OPS-01 to -07 |
| Feature and screens | FEAT-RDF-19, FEAT-RPT-01; SCR-44 |
| Decoupling patterns | DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Architecture decisions | ADR-016, ADR-018, ADR-021, ADR-023 |
| Batch trigger | The Airflow report-run call at 01:30 Asia/Bangkok starts JOB-15; one Temporal Schedule is created paused (RD-P1-066; GAP-3573) |
| Events | None declared in this story; any freshness event is a separate story (GAP-2569) |

### 19. Out of scope

- The implementation of the definitions, the six calculators, the snapshot, the freeze and the publish state (RWB-P9-E1013-APP) and the contract baseline that fixes them (RWB-P9-E1013-CON).
- The case facts and their banding (RWB-P3-E1013-APP) and the payments and the gate answer (RWB-P1-E1013-APP).
- The catalogue baseline, the run books' content and the Epic 1 monitoring workbook (RWB-PLT-E1056-OPS).
- The screen composition and the composite route (RWB-PLT-N001-CON) and the Platform administration roles (RWB-P4-AD001 to RWB-P4-AD016).
- The event question of the service topic and whether it ever publishes `rwb.reporting.ReportPublished.v1` (GAP-2569; ASM-4235).
- The Airflow chain itself, which is the bank's: this release only receives its report-run call (RD-P1-066; GAP-3573).
- The data lake, INT-19 and INT-20: removed, with no deployment path and no story that rebuilds them.
- The cross-service journey with the real ACE batch and the real payments (RWB-ITG-E1013-ITG).
