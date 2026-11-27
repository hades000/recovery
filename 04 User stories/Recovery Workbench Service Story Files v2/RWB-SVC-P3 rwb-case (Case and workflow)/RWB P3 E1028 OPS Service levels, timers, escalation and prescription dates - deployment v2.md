# RWB-P3-E1028-OPS Service levels, timers, escalation and prescription dates

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1028-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-K |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E1028-OPS-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P3-E1028-OPS-14) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P3-E1028-OPS-22) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (the `/v1` paths and the `.v1` event names of section 12) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-022, FR-P3-025, FR-P3-030) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-028 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 16 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the timer capability of rwb-case deployed from the service template with its own login, its per-service migration, its consumer groups for the four case events and the two deviation events, its worker on task queue `rwb-case`, the series for timer fires, catch-up after an outage, breached timers and prescription warnings, the alerts and the runbook for a timer that did not fire, a breach that was not escalated and a catch-up that did not happen**, so that **an operator can see within minutes that a deadline will not fire or that a breach was not raised, and repair it without reading code or waiting for a business report**.

This story deploys an existing capability. It adds no topic, registers no timer-check Schedule and builds no endpoint, table or workflow: the clock is a durable Temporal timer inside `CaseWorkflow`, and `JOB-05` with its five-minute Quartz schedule and the `TimerDue` event are retired.

### 2. Business rationale

The legacy capability leaned on a five-minute Quartz job whose only failure signal was a job exception, so a timer that never fired and a quiet night looked identical, and the missed run was discovered only when a debtor's file reached a court date. In the target the clock is a durable timer inside the workflow (DP-10): there is no scheduler row to be late and no job record to inspect, so the operational signal moves from "did the job run" to "is the projection moving, has the worker polled, was a fire satisfied after an outage and is the breach volume the band the business expects" (Architecture v5 slides 44 and 28; `JOB-05` retired, `JOB-21` stuck workflow scan kept).

The capability also produces a legal artefact: a breach whose decision record was not sealed is an escalation that cannot be defended, so the record failure of MSG-P7-003 is a first-class alert here and not a line in a log. Deployment is therefore part of the capability: the chart carries the rwb-case login and no other credential (DP-02), the migration runs the per-service Flyway sequence in `rwb_case` (DP-15), the six subscriptions have retry and `.dlt` paths (DP-09), and the runbook names the three failures an operator will actually see.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the namespace `rwb-recovery` are available (RWB-PLT-WF, RWB-PLT-E1071-CON), so the api and worker deployments of rwb-case poll `rwb-case`.
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON); `rwb.case.events.v1` is provisioned by this service and `rwb.deviation.events.v1` by S8.
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across REST, Kafka and Temporal; the platform's stuck workflow scan `JOB-21` is on.
- The parameters and reference rows of the capability are loaded by their owning stories: the `SERVICE_LEVEL` rows, `legal.prescription.warn.days`, `LEGAL_PERIOD`, `LOV-TIMER` and `LOV-TIMER-STATUS`; this story reads them and holds no copy.
- RWB-P3-E1028-CON is published, so the smoke profile and the drift test run against the two read operations and the four fakes of that baseline.
- The three environments DEV, SIT and UAT exist with their parameter scope and their Kafka and Temporal endpoints, and the alert values are Not specified in the source documents (GAP-2204; ASM-3619).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-case with the rwb-case login, the pre-deploy migration job for `rwb_case`, the readiness and liveness probes, the api deployment and the worker deployment that polls `rwb-case`.
3. The provisioning step declares the consumer groups of the capability: the four case events on `rwb.case.events.v1` and the two deviation events on `rwb.deviation.events.v1`, each with its retry topic and its `.dlt` topic, into the inbox of `rwb_case`.
4. The provisioning step asserts that no timer-check Schedule, timer-check task queue and timer-check job exists, and that `rwb.case.events.v1` and `rwb.decision-record.v1` are used as their owners provisioned them.
5. The dashboards are published: timers by type and status, overdue timers, escalated timers, prescription warnings in force, timer fires and catch-up after an outage, projection lag, breach volume, the MSG-P7-003 rate, the MSG-P3-026 count and worker poll health.
6. The alerts are wired to the message IDs of section 14 and to the runbook entries of section 13; each threshold is a values-file entry with the placeholder of section 14 until it is confirmed.
7. A smoke step reads the timers and the prescription date of a synthetic case through gateway-bff in the SIT profile, so the composite route, the two rwb-case answers and the fakes are exercised together.
8. The runbook is published and reviewed with the on-call rota: a timer that did not fire, a catch-up that did not happen after an outage, a breach that was not escalated, a projection that stopped moving, a missing service level or legal period that is not an incident.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | A subscription is provisioned without its retry or `.dlt` topic | The provisioning step fails the release and the consumer refuses to start | None | AC3 |
| X3 | The worker has not polled `rwb-case` for longer than its value | The worker-poll alert fires and the timer-did-not-fire runbook entry starts from the workflow history | None | AC5, AC6 |
| X4 | A fire fell inside an outage and the catch-up series shows an unmet timer | The catch-up alert fires and the runbook entry for a catch-up that did not happen names the case and the workflow | None | AC5, AC6 |
| X5 | The decision record write fails at a breach | The MSG-P7-003 rate rises, the breach-not-escalated runbook entry checks the projection, the workflow history and the ledger | MSG-P7-003 | AC6 |
| X6 | The breach volume leaves its band | The volume alert fires in the direction it left the band | None | AC6 |
| X7 | The projection lags the fired timer | The projection-lag alert fires and the runbook entry for a projection that stopped moving is opened | None | AC5 |
| X8 | A case has no service level or no legal period | The MSG-P3-026 count rises on the dashboard and no page is sent; SCR-09 lists the case | MSG-P3-026 | AC5 |
| X9 | A release declares a timer-check Schedule or a new topic | The retired-element check fails the release | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the observability stack; builds no application code |
| Negotiable | Replica counts, resource sizes, retention and alert thresholds are environment values, not story decisions |
| Valuable | Makes a capability with no scheduler row observable: the worker, the fire, the catch-up and the record each have a signal and an owner |
| Estimable | One chart, one pipeline stage, one migration job, two probes, six subscriptions, nine panels, six alert rules and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the subscriptions exist, the panels carry data, the alerts fire on a synthetic metric, the runbook entry resolves |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the service levels, timers, escalation and prescription dates

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart and values deploy rwb-case with its own login and its migration (new, D-RCV-60)
    Given the rwb-case Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-case login reference and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_case, including the two escalation columns and the three indexes of RWB-P3-E1028-APP, before the deployment is marked ready
    Then the worker deployment polls task queue rwb-case in namespace rwb-recovery with the build ID of the release
    Then no replica count, resource size, timeout, threshold or cadence is hard-coded in the template

  Scenario: AC2 The pipeline promotes one artefact and runs the contract tests (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit, component and contract tests of RWB-P3-E1028-CON and fails the build on a drift between a fake and the document
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 The six subscriptions are provisioned with retry and dead-letter paths (new, D-RCV-60)
    Given the provisioning step of rwb-case for the timer capability
    When it runs against the environment
    Then a consumer group rwb-case subscribes to rwb.case.events.v1 for CaseCreated, CaseAllocated, CaseTransferred and CaseStateChanged with the inbox of schema rwb_case
    Then the same group subscribes to rwb.deviation.events.v1 for DeviationRaised and DeviationCleared with the inbox of schema rwb_case
    Then each subscription has its retry topic and its .dlt topic and the consumer never acknowledges an event it could not process
    Then rwb.case.TimerBreached.v1 is produced on the existing rwb.case.events.v1 with its retry and .dlt topics and no new topic is created for this capability
    Then the shared rwb.decision-record.v1 is used as its owner provisions it and is not recreated
    Then the provisioning step fails the release when a retry or .dlt topic is missing

  Scenario: AC4 The durable timer is operated and no timer-check Schedule exists (new, D-RCV-60)
    Given the published artefacts of the capability
    When the deployed resources are listed and the worker health is read
    Then the durable timer state is observed through the workflows of CaseWorkflow on task queue rwb-case and through the P3 projection behind GET /api/recovery/case/v1/cases/{caseId}/timers
    Then no timer-check Schedule, no timer-check task queue and no timer-check job is registered for any environment
    Then the retired-element check fails a release that declares a timer-check Schedule, a timer-check job or a TimerDue event
    Then the platform stuck workflow scan of JOB-21 raises a workflow that has not moved for its value

  Scenario: AC5 The dashboards carry the nine capability series (new, D-RCV-60)
    Given the published dashboard
    When a synthetic day is replayed with running, paused, expired and stopped timers, two escalated timers, three prescription dates inside the warning window, a worker stopped for 40 minutes, a decision record failure and two cases with no service level
    Then the panels show timers by type and status, overdue timers, escalated timers, prescription warnings in force, timer fires, catch-up after an outage, projection lag, breach volume and the MSG-P7-003 and MSG-P3-026 counts
    Then every panel names its service, its environment and its business date
    Then the MSG-P3-026 count and the refused reads are counted and never page the on-call rota
    Then no panel carries a customer name, an account number or a personal identifier

  Scenario: AC6 The alerts and the runbook cover the three operator failures (new, D-RCV-60)
    Given the six alert rules and the published runbook
    When a worker stops polling, a fire fell inside the outage and a decision record fails at a breach
    Then each condition raises its alert with its message ID where one exists, its environment, and its links to the case and the workflow
    Then the runbook holds one entry each for a timer that did not fire, a catch-up that did not happen and a breach that was not escalated, with the check, the owner role and the recovery step
    Then every alert links exactly one runbook entry and every entry names the escalation path when the step fails
    Then every threshold that is provisional names the gap and the assumption it carries

  Scenario: AC7 No environment value is hard-coded and every threshold stays a values-file entry (new, D-RCV-60)
    Given the chart templates and the values files of the release
    When the values-file scan and the rendered chart are checked in the pipeline
    Then every replica count, resource size, timeout and threshold resolves from a values file and none is written in a template or a chart default
    Then a template or a chart default that carries a literal replica count, resource size, timeout or threshold fails the pipeline

```

These six criteria are new for the deployment and test artefacts only; they restate no business outcome owned by RWB-P3-E1028-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-case login and no other service's credential | DP-02; Architecture v5 slide 29 |
| BR2 | The migration is a per-service Flyway sequence in `rwb_case` and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every subscription has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Architecture v5 slide 22 |
| BR4 | No timer-check Schedule, timer-check job or `TimerDue` event exists: the clock is a durable timer inside `CaseWorkflow` | DP-10; Architecture v5 slides 42 and 44 |
| BR5 | No new topic is created: `rwb.case.events.v1` carries the case events and `TimerBreached`, `rwb.deviation.events.v1` the deviation events | DP-14; Architecture v5 slide 42 |
| BR6 | No environment value is hard-coded: replica counts, resource sizes, timeouts and thresholds come from values files | Template and Rules §R7.2 s17 |
| BR7 | An alert carries a message ID where the condition maps to one and links one runbook entry; the poll window, catch-up window, breach band and record-failure rate are set in the rwb-case values files, confirmed at UAT and recorded in that runbook entry | Template and Rules §R7.2 s14; GAP-2204 |
| BR8 | A missing service level or legal period is a business exception counted on the dashboard and never an incident | MSG-P3-026; RWB-E1-028 AC4, AC5 |
| BR9 | The stuck workflow scan is the platform's (`JOB-21`) and is reused, not rebuilt | Architecture v5 slide 44 |
| BR10 | No dashboard series, log line or alert payload carries personal data; case and workflow identifiers only | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version, the outbox relay runs and the worker polls `rwb-case` | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is the new one | Ready |
| Ready | Worker stops polling | The worker-poll alert fires | Degraded |
| Degraded | Worker restored | The workflows resume from history and the catch-up series returns to zero | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning step, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the visibility queries behind `JOB-21` |
| ACE database administrator | Owns schema `rwb_case`, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the runbook entries and opens an incident when a breach was not escalated or a catch-up did not happen |
| Service owner of S8 rwb-deviation | Owns the two deviation events this release subscribes to; is named in the runbook when the pause path is silent |
| Service owner of P1 rwb-source-data | Is named in the runbook when the account-date or calendar read is degraded |

The per-service login used by the chart is a secret reference resolved at deploy time; the chart references "the rwb-case login (DP-02)" and never a literal name.

### 11. Data

| Item | Content | BR ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switch `rwb.p3.timers`, the client timeouts, the alert thresholds | BR6 |
| Schema | `rwb_case`, migrated by the per-service Flyway sequence; `recovery_case`, `timer`, `queue` and the library objects, with the two escalation columns and the three indexes of RWB-P3-E1028-APP | BR2 |
| Topics | `rwb.case.events.v1` for the four case events and `TimerBreached`, with retry and `.dlt`; `rwb.deviation.events.v1` for the two deviation events; `rwb.decision-record.v1` used as its owner provisions it | BR3, BR5 |
| Queue | Temporal task queue `rwb-case` in namespace `rwb-recovery` | Not specified in the source documents (DOR-RWB-P3-E1028-OPS-7) |
| Schedules | None for this capability; `JOB-05` is retired and `JOB-21` is the platform's | BR4, BR9 |
| Dashboard series | timers by type and status, overdue timers, escalated timers, prescription warnings in force, timer fires, catch-up after an outage, projection lag, breach volume, MSG-P7-003 rate, MSG-P3-026 count, worker poll health, workflow open and stuck | BR8, BR10 |
| Runbook entries | timer did not fire, catch-up did not happen, breach not escalated, projection stopped, missing level or legal period is not an incident | BR7 |
| Secrets | The rwb-case login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store | BR1 |

The alert values are deployment values and are provisional: the missing source for them is Not specified in the source documents (GAP-2204; ASM-3619). The cluster topology, node pools, replica counts and probe timings are deployment values of the platform chart and are not fixed here.

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the two read operations of RWB-P3-E1028-CON behind gateway-bff: `GET /api/recovery/case/v1/cases/{caseId}/timers` with the `Timer` array and `GET /api/recovery/case/v1/cases/{caseId}` with `prescriptionDate`. Owner rwb-case (P3). The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/accounts/{accountId}` | P1 rwb-source-data | The account dates behind the prescription date; 2 s client budget and a breaker (GAP-2202; ASM-3616) |
| GET | `/api/recovery/source-data/v1/calendar/holidays` | P1 rwb-source-data | The working-day calendar; 2 s client budget, cached per business date |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The authorisation check before either read; cached per request |

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.case.TimerBreached.v1` (event 19) | `rwb.case.events.v1` | The topic, its retry topic and its `.dlt` topic already exist for rwb-case; the deployment reuses them and creates no new topic |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | Shared topic owned by the platform and rwb-decision; reused, not recreated |

#### 12.4 Events consumed

| Event | Topic | Provisioning | Owner |
|---|---|---|---|
| `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | Consumer group `rwb-case` with the inbox of schema `rwb_case`; retry and `.dlt` in the same step | rwb-case (consumer group `rwb-case`) |
| `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1` | `rwb.deviation.events.v1` | Same consumer group, same retry and `.dlt` path; S8 owns the topic | rwb-case (consumer group `rwb-case`); S8 owns the topic |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = `case-{caseId}` | `rwb-case` | Worker deployment with the build ID of the release; holds the durable timers, which are authoritative, and raises `TimerBreached`; the timer row is their audit copy |
| EvaluateRules | Activity | `rwb-case` | Registered by the same worker; reads the parameter and reference rows in force |
| RecordAndApply | Activity | `rwb-case` | Registered by the same worker; the record, the projection and the outbox in one transaction; the timer audit row is written and read back in this activity |

#### 12.6 Schedules

None. The deployment registers no timer-check Schedule and no cron entry, because the five-minute check is replaced by the durable timer inside `CaseWorkflow` (DP-10; Architecture v5 slide 44, `JOB-05` retired). The platform's stuck workflow scan `JOB-21` runs every five minutes as a visibility query and is not registered by this release; `JOB-02`, `JOB-03` and `JOB-06` keep their owners in this service and are deployed by their own stories.

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| recovery_case, timer, queue | P3 (`rwb_case`) | Created and migrated by the per-service Flyway sequence in the migration job |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_case` | Created by the same migration job; used by the six subscriptions and the outbox relay |

`v_ace_account` and `v_ace_holiday` belong to ACE and are read only through P1; the migration job touches `rwb_case` only (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-source-data WireMock | Runs in the pipeline and the SIT smoke profile, including the healthy answer, the account with no last payment date and the delayed answer beyond 2 s |
| rwb-access WireMock | Same, including a granted read, a refused role and a refused scope |
| rwb-decision record double | Same, including the sealed record with `R-UNI-30` and the unavailable answer |
| rwb-deviation event fixture | Same, including `DeviationRaised` on 2026-12-02 and `DeviationCleared` on 2026-12-04 |

The fakes are test-only workloads; they are not deployed into UAT behind real traffic or into production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed in the deployment path | The two reads; account dates, calendar and authorise; one hop, 2 s |
| Kafka | 2 published by their owners, 6 consumed | `TimerBreached` and `DecisionRecorded` reused; four case events and two deviation events consumed with retry and `.dlt` |
| Temporal | 1 workflow, 2 activities, no Schedule | `CaseWorkflow` with the durable timers |
| File | None | The release reads no runtime file; values files are build inputs |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The rows record what the release has to provision; no dependency is a build dependency of this story, which is Day 1 by rule.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-case/` | Chart with api and worker deployments, service, migration job, config map, secret references and probes; no Schedule template for this capability |
| `helm/rwb-case/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, `rwb.p3.timers`, the client timeouts, the alert thresholds |
| Pipeline stage | Build, unit, component and contract tests, retired-element check, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Consumer group `rwb-case` on `rwb.case.events.v1` for four events and on `rwb.deviation.events.v1` for two, with retry and `.dlt`; reuse of `rwb.decision-record.v1`; task queue `rwb-case` in `rwb-recovery` |
| Dashboards | Nine panels: timers by type and status; overdue; escalated; prescription warnings in force; timer fires and catch-up; projection lag; breach volume; MSG-P7-003 rate; MSG-P3-026 count and worker poll health |
| Alerts | Six rules, each with one runbook entry and a message ID where the condition maps to one |
| Runbook | Five entries: timer did not fire, catch-up did not happen, breach not escalated, projection stopped, missing level or legal period is not an incident |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running and the Temporal worker on `rwb-case` has polled after its value; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database and neither calls another service.

**Projection lag and catch-up.** Two series are computed from the workflow history and the projection: the lag between a fire and the first read of the row with its new status, and the count of timers whose `expires_at` has passed while the workflow has not yet satisfied them after a restart. Neither is a job-lateness measure, because there is no job.

**Alert mapping.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P7-003 | The decision record write fails at a warning or a breach | Record-failure alert with the case, the workflow and the ledger state | Platform on-call, page, ticket to the P7 owner |
| MSG-P3-026 | A case has no service level or no legal period | Count on the dashboard and the SCR-09 list; no page | No page |
| None | The worker has not polled `rwb-case` for longer than its value | Worker-poll alert with the build ID and the last poll | Platform on-call, page |
| None | A timer stayed unmet after the worker returned | Catch-up alert with the case, the workflow and the elapsed time | Platform on-call, page |
| None | `TimerBreached` volume leaves its band in either direction | Volume alert with the count, the band and the change against the trailing hour | Page upward, ticket downward |
| None | `JOB-21` raises a stuck workflow on `rwb-case` | Stuck-workflow alert with the workflow ID, the stage and the last event | Platform on-call, page |

Every threshold is a values-file entry; the provisional values and their confirmation are carried by the gap and the assumption of section 14 (GAP-2204; ASM-3619).

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact and fails on a fake drift or a retired element, the six subscriptions exist with their retry and `.dlt` paths, the nine panels carry the synthetic day, the six alert conditions fire on synthetic metrics and resolve one runbook entry each, and the five runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-003 | A timer or the prescription date is inside its warning period | {timer} ends on {date}. |
| MSG-P3-004 | The case is on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-026 | No service level or legal period found | No {item} is set for {scope}. The timer did not start. |
| MSG-P7-003 | The decision record write failed at a warning or a breach | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A read without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the person's scope | This case is not in your scope. |

The message texts are copied unchanged from the legacy story and the deployment adds the routing, the threshold and the runbook link, never a new wording. The alert values are Not specified in the source documents (GAP-2204; ASM-3619): the worker-poll window, the catch-up window, the breach band and the record-failure rate stay values until UAT confirms them.

### 15. Screens and states

The deployment serves SCR-03 Case record in its Read only, On hold and Loading states and SCR-09 Exception queue in its Loading and List states, behind the gateway-bff composite route (DP-19); the Empty, Error and No access states of SCR-03 and SCR-09 are Not specified in the source documents (CG-ALL-3652, CG-ALL-3653). The operator-facing surfaces of this story are the pipeline run view, the release view, the nine dashboard panels and the runbook; the smoke step reads the timers and the prescription date of a synthetic case in SIT and asserts that both answer inside the 2 s budget.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1028-OPS-01 | AC1, BR1, BR2 | NFR | The chart renders for DEV, SIT and UAT with a pinned digest, the rwb-case login, the migration job with the two columns and three indexes, and the worker on `rwb-case` |
| TC-P3-E1028-OPS-02 | AC2 | NFR | One pipeline run produces one image and one chart version and fails on a fake drift, a critical finding or a retired element |
| TC-P3-E1028-OPS-03 | AC3, BR3, BR5 | NFR | Six subscriptions with retry and `.dlt`; a missing `.dlt` fails the release; no new topic |
| TC-P3-E1028-OPS-04 | AC4, BR4, BR9 | NFR | No timer-check Schedule or queue in any environment; the retired-element check fails a release that declares one; the platform stuck workflow scan raises a synthetic stuck `CaseWorkflow`; no `TimerDue` is asserted |
| TC-P3-E1028-OPS-05 | AC5, BR8 | NFR | A synthetic day with four timer statuses, two escalations, three prescription warnings, a 40-minute worker stop, a record failure and two cases with MSG-P3-026; nine panels populated |
| TC-P3-E1028-OPS-06 | AC6, BR7, BR10 | NFR | Six synthetic conditions raise their alerts and resolve one runbook entry each, with the message ID, the links and the escalation path |
| TC-P3-E1028-OPS-07 | §12.4, §12.5 | NFR | Contract test of the operations, events and activities of section 12: the consumed events, CaseWorkflow with its workflow ID form, EvaluateRules and RecordAndApply |
| TC-P3-E1028-OPS-08 | §12.7, ASM-3438 | NFR | Boundary test of the tables of section 12.7: rwb_case objects only, and no write to v_ace_account or v_ace_holiday |
| TC-P3-E1028-OPS-09 | BR6 | NFR | Values file scan finds no hard-coded replica count, resource size, timeout or threshold in the release |
| TC-P3-E1028-OPS-10 | AC7, BR6 | NFR | Not specified in the source documents (NEWAC-RWB-P3-E1028-OPS-AC7) |

The legacy test cases of RWB-E1-028 are owned by RWB-P3-E1028-APP and copied with the `-ITG` suffix by RWB-ITG-E1028-ITG; a deployment story owns no business outcome and therefore no legacy test case.

### 17. Guardrails

- No business value in a values file: the levels, the warning percentage, the escalation roles, the legal periods and the warning days are data held by their owner, never a deployment value.
- No personal data in logs, dashboard series, alert payloads or the runbook: case IDs, workflow IDs, staff user IDs, counts and durations only.
- One login per service; the chart carries the rwb-case login reference and no other service's credential (DP-02).
- The service writes only schema `rwb_case`; the migration job never touches another schema and no dashboard query reads one (DP-01, DP-05).
- Every subscription has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- No new topic and no timer-check Schedule: the release reuses `rwb.case.events.v1` and `rwb.deviation.events.v1`, and the clock is the durable timer inside `CaseWorkflow` (DP-10, DP-14).
- ACE data is read only through the owner's contract: no dashboard reads an ACE view or another service's schema.
- The release pins the image digest and the chart version, and no secret is written into a values file, a chart template, a dashboard or the runbook.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-CWC-011 | Service levels, warnings and escalation as data; a breach does not move the case | Escalated-timers panel, breach volume alert, breach-not-escalated runbook entry and the worker-poll alert | TC-P3-E1028-OPS-05, TC-P3-E1028-OPS-06 |
| REQ-CWC-012 | Prescription date from the legal periods at creation | Prescription-warnings panel, the account-date and calendar client budgets and the MSG-P3-026 count | TC-P3-E1028-OPS-03, TC-P3-E1028-OPS-05 |
| REQ-CWC-016 | Every timer event logged with rule and version | The MSG-P7-003 rate panel, the record-failure alert and the decision-record topic reuse | TC-P3-E1028-OPS-02, TC-P3-E1028-OPS-06 |
| ADR-016 | Durable timers replace Quartz | The worker deployment, the catch-up series and the retirement of `JOB-05` with the `TimerDue` event | TC-P3-E1028-OPS-04, TC-P3-E1028-OPS-05 |
| ADR-023 | Observability per service | Nine panels, six alert rules and five runbook entries | TC-P3-E1028-OPS-05, TC-P3-E1028-OPS-06 |

### 19. Out of scope

- The application code of the timers, the prescription calculation and the two reads (RWB-P3-E1028-APP).
- The contract documents and the fakes as published artefacts (RWB-P3-E1028-CON); this story only deploys the test copies.
- The Case record R right and its refusal (RWB-P4-E1028-APP) and the central ledger (RWB-P7-E1028-APP).
- The platform topic provisioning, the Temporal cluster, the observability stack and the stuck workflow scan (the platform epics RWB-PLT-EVT, RWB-PLT-WF, RWB-PLT-OBS).
- The schedules of this service other than the retired timer check (`JOB-02`, `JOB-03`, `JOB-06`) and their own deployment stories.
- The `rwb_case` schema design and the logical model (the database stories of the service epic).
- Data migration from the legacy schema and the reconciliation run (Epic 2 and rwb-source-data).
- The cross-service journey harness and its evidence (RWB-ITG-E1028-ITG).
