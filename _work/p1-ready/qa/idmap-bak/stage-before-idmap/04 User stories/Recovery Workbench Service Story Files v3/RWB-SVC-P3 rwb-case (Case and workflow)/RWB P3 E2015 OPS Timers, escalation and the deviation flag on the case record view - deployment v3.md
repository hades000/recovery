# RWB-P3-E2015-OPS Timers, escalation and the deviation flag on the case record view

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004.

| Item | Value |
|---|---|
| Story key | RWB-P3-E2015-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-AH |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2015-CON (build status Not started) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-019, FR-P3-020, FR-P3-021, FR-P3-022) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-015 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 21 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **Platform administrator (RW-PLATADM)**, I want **the clocks-and-deviation capability of rwb-case deployed from the service template with its Helm values and its own login, its two consumer groups for DeviationRaised and DeviationCleared, its timer-projection lag measure, the dashboards for timers, escalation, prescription warnings and degraded reads, the alerts on TimerBreached volume, the MSG-GEN-006 rate and stuck workflows, and a runbook for a stuck timer, a deviation read that is down and an escalation that was not applied**, so that **an operator can see within minutes that a deadline will not fire or that a deviation section is degrading, and repair it without reading code or waiting for a business report**.

This story deploys an existing capability. It adds no topic, registers no timer-check Schedule and builds no endpoint, table or workflow: the clock is a durable Temporal timer inside CaseWorkflow on task queue `rwb-case`, and the deviation flag is fed by the two S8 events on `rwb.deviation.events.v1`.

### 2. Business rationale

The legacy capability leaned on a five-minute Quartz job whose only failure signal was a job exception, so a timer that never fired and a deviation that was never read looked the same as a quiet night. In the target the clock is a durable timer inside the workflow (DP-10): there is no scheduler row to be late and no job record to inspect, so the operational signal has to move from "did the job run" to "is the projection moving, is the workflow stuck and is the deviation section degrading" (Architecture v5 slides 44 and 28; JOB-05 retired, JOB-21 stuck workflow scan kept).

The capability is also the one part of the case record that depends on another service for its correctness at read time: a slow or refused S8 read does not fail the screen, it silently turns the deviation section into MSG-GEN-006 while the banner still shows. That is the right behaviour for the officer and the wrong behaviour for the operator if nobody counts it, which is why the degradation rate is a dashboard series and an alert here rather than a line in a log.

Deployment is therefore part of the capability: the chart carries the rwb-case login and no other credential (DP-02), the migration job runs the per-service Flyway sequence in schema `rwb_case` (DP-15), the two S8 consumer groups are provisioned with retry and `.dlt` paths so a deviation pause is never lost (DP-09), and the runbook names the three failures an operator will actually see.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON), so CaseWorkflow polls `rwb-case` and the durable timer runs in every environment.
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and `rwb.deviation.events.v1` is provisioned by its owner S8.
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across REST, Kafka and Temporal.
- The three environments DEV, SIT and UAT exist with their parameter scope and their Kafka and Temporal endpoints.
- RWB-P3-E2015-CON is published, so the smoke profile and the drift test run against the two read operations and the three fakes of that baseline.
- The reference data LOV-TIMER, LOV-TIMER-STATUS, LOV-DEVIATION and the SERVICE_LEVEL escalation roles are loaded by the owning stories; this story reads them and holds no copy.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-case with the rwb-case login, the pre-deploy migration job for schema `rwb_case`, the readiness and liveness probes and the worker deployment that polls `rwb-case`.
3. The provisioning step declares the two consumer groups of this capability, `rwb-case` for `rwb.deviation.events.v1` with the topics DeviationRaised and DeviationCleared, each with its retry topic and its `.dlt` topic; it reuses `rwb.case.events.v1` for TimerBreached and creates no new topic.
4. The provisioning step asserts that no timer-check Schedule, task queue or job exists for this capability, and that `rwb.case.events.v1` and `rwb.decision-record.v1` are consumed or produced as their owners provisioned them.
5. The dashboards are published: timers by status, overdue timers, escalated timers, prescription warnings in force, the timer projection lag, the S8 read timeouts and breaches, the MSG-GEN-006 rate, refused and out-of-scope reads, TimerBreached volume and workflow health.
6. The alerts are wired to the message IDs of section 14 and to the runbook entries of section 13; the thresholds are values and carry the placeholder of section 14 until they are confirmed.
7. A smoke step opens the case record of a synthetic case through gateway-bff in the SIT profile, so the composite route, the two rwb-case answers and the three fakes are exercised together.
8. The runbook is published and reviewed with the on-call rota: a stuck timer, a deviation read that is down, an escalation that was not applied, a projection that stopped moving, a refused read that is not an incident.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | A consumer group is provisioned without its retry or `.dlt` topic | The provisioning step fails the release and the consumer refuses to start | None | AC3 |
| X3 | The timer projection lag passes its value | The projection-lag alert fires and the runbook entry for a projection that stopped moving is opened | MSG-GEN-006 | AC4, AC6 |
| X4 | The S8 read times out on a share of reads | The MSG-GEN-006 rate alert fires; the deviation read-down runbook entry names the S8 owner and the breaker state | MSG-GEN-006 | AC6 |
| X5 | A workflow stops on a non-retryable failure | The stuck workflow scan of JOB-21 raises the case and the stuck-timer runbook entry starts from the workflow history | None | AC6 |
| X6 | TimerBreached volume leaves its band | The volume alert fires and the escalation-not-applied runbook entry checks the projection and the record | None | AC6 |
| X7 | A role without Case record R is refused | The refused-read count rises on the dashboard and no page is sent | MSG-P4-002 | AC5 |
| X8 | A case is outside the caller's scope | The out-of-scope count rises on the dashboard and no page is sent | MSG-P4-003 | AC5 |
| X9 | A release declares a timer-check Schedule or a new topic | The pipeline fails the release on the retired-element check of AC4 | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the observability stack; builds no application code |
| Negotiable | Replica counts, resource sizes, alert thresholds and retention are environment values, not story decisions |
| Valuable | Makes a capability with no scheduler row observable: the projection, the workflow and the degraded section each have a signal and an owner |
| Estimable | One chart, one pipeline stage, one migration job, two probes, two consumer groups, eight dashboard panels, five alert rules and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the groups exist, the panels carry data, the alerts fire on a synthetic metric, the runbook entry resolves |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the clocks and the deviation flag on the case record view

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The Helm chart and values deploy rwb-case with its own login (new, D-RCV-60)
    Given the rwb-case Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-case login reference and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_case before the deployment is marked ready
    Then the worker deployment polls task queue rwb-case in namespace rwb-recovery with the build ID of the release
    Then no replica count, resource size, timeout, threshold or cadence is hard-coded in the template

  Scenario: AC2 The pipeline promotes one artefact and runs the contract tests (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit, component and contract tests of RWB-P3-E2015-CON and fails the build on a drift between a fake and the document
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 The two S8 consumer groups are provisioned with retry and dead-letter paths (new, D-RCV-60)
    Given the provisioning step of rwb-case for the deviation flag
    When it runs against the environment
    Then a consumer group rwb-case subscribes to rwb.deviation.events.v1 for DeviationRaised and DeviationCleared with the inbox of schema rwb_case
    Then each subscription has its retry topic and its .dlt topic and the consumer never acknowledges an event it could not process
    Then TimerBreached is produced on the existing rwb.case.events.v1 with its retry and .dlt topics and no new topic is created for this capability
    Then the shared rwb.decision-record.v1 is consumed as its owner provisions it and is not recreated
    Then the provisioning step fails the release when a retry or .dlt topic is missing

  Scenario: AC4 The timer projection is measured and no timer-check Schedule exists (new, D-RCV-60)
    Given the published metrics of the capability
    When the projection lag is computed and the deployed resources are listed
    Then the lag between the durable timer firing and the timer row being readable is exposed as a series with its alert value
    Then the dashboards read the projection by status, by overdue state and by escalation level
    Then no timer-check Schedule, no timer-check task queue and no timer-check job is registered for any environment
    Then a release that declares a new topic for this capability or a timer-check Schedule fails the retired-element check

  Scenario: AC5 The dashboards carry the six capability series (new, D-RCV-60)
    Given the published dashboard
    When a synthetic day is replayed with running, paused, expired and stopped timers, two escalated timers, three prescription dates inside the warning window, a slow S8 answer and a refused read
    Then the panels show timers by status, overdue timers, escalated timers, prescription warnings in force, S8 read timeouts and breaches, and refused and out-of-scope reads
    Then every panel names its service, its environment and its business date
    Then a refused read and an out-of-scope read are counted and never page the on-call rota
    Then no panel carries a customer name, an account number or a personal identifier

  Scenario: AC6 The alerts and the runbook cover the three operator failures (new, D-RCV-60)
    Given the five alert rules and the published runbook
    When TimerBreached volume leaves its band, the MSG-GEN-006 rate passes its value and the stuck workflow scan of JOB-21 raises a case
    Then each condition raises its alert with its message ID, its environment and its links to the case and the workflow
    Then the runbook holds one entry each for a stuck timer, a deviation read that is down and an escalation that was not applied, with the check, the owner role and the recovery step
    Then every alert links exactly one runbook entry and every entry names the escalation path when the step fails
```

These six criteria are new for the deployment and test artefacts only; they restate no business outcome owned by RWB-P3-E2015-APP.

Scenario: AC7 A release that uses any credential other than the rwb-case login is refused (new, D-RCV-60)

Scenario: AC8 The per-service Flyway sequence in schema rwb_case completes before the deployment is ready (new, D-RCV-60)

Scenario: AC9 An event the consumer cannot process is not acknowledged and goes through the retry topic to the .dlt topic (new, D-RCV-60)

Scenario: AC10 No timer-check Schedule or timer-check job is registered in any environment (new, D-RCV-60)

Scenario: AC11 TimerBreached is carried on rwb.case.events.v1 and the two deviation events on rwb.deviation.events.v1, with no new topic (new, D-RCV-60)

Scenario: AC12 Replica counts, resource sizes, timeouts and alert thresholds are read from values files and none is hard-coded (new, D-RCV-60)

Scenario: AC13 An alert carries a message ID, the agreed text and one runbook entry (new, D-RCV-60)

Scenario: AC14 A refused read and an out-of-scope read are counted on the dashboard and never page the on-call rota (new, D-RCV-60)

Scenario: AC15 The stuck workflow scan is the platform's JOB-21 and is reused, not rebuilt (new, D-RCV-60)

Scenario: AC16 No dashboard series, log line or alert payload carries personal data, only case and workflow identifiers (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-case login and no other service's credential | DP-02; Architecture v5 slide 29 |
| BR2 | The migration is a per-service Flyway sequence in schema rwb_case and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every subscription has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Architecture v5 slide 22 notes |
| BR4 | No timer-check Schedule and no timer-check job exists: the clock is a durable timer inside CaseWorkflow (JOB-05 retired) | DP-10; Architecture v5 slide 44 |
| BR5 | No new topic is created for this capability; `rwb.case.events.v1` carries TimerBreached and `rwb.deviation.events.v1` carries the two deviation events | DP-14; Architecture v5 slide 42 |
| BR6 | No environment value is hard-coded: replica counts, resource sizes, timeouts and alert thresholds come from values files; the timer projection lag, MSG-GEN-006 degradation rate and TimerBreached volume alert values are Not specified in the source documents (GAP-0715), are set in the values files and confirmed at UAT | Template and Rules §R7.2 s17 |
| BR7 | An alert carries a message ID and the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | A refused read and an out-of-scope read are counted on the dashboard and never page the on-call rota | MSG-P4-002; MSG-P4-003 |
| BR9 | The stuck workflow scan is the platform's (JOB-21, a visibility query every five minutes) and is reused, not rebuilt | Architecture v5 slide 44 |
| BR10 | No dashboard series, log line or alert payload carries personal data; case and workflow identifiers only | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version, the outbox relay runs and the worker polls | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is the new one | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning step, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the visibility queries behind JOB-21 |
| ACE database administrator | Owns schema rwb_case, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the runbook entries and opens an incident when a stuck workflow or an escalation-not-applied case persists |
| RW-PLATADM | Reads and operates the case record and its clocks in the running service, not in the cluster |
| Service owner of S8 rwb-deviation | Is paged by the deviation read-down alert and owns the repair beyond the rwb-case breaker |

The per-service login name used by the chart is a secret reference resolved at deploy time; the chart references "the rwb-case login (DP-02)" and never a literal name.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switch `rwb.p3.case-clocks`, the two client timeouts, the alert thresholds | Not specified in the source documents (DOR-RWB-P3-E2015-OPS-7) |
| Schema | rwb_case, migrated by the per-service Flyway sequence; the tables `recovery_case`, `timer` and `task` with the library objects | Not specified in the source documents (DOR-RWB-P3-E2015-OPS-7) |
| Topics | `rwb.deviation.events.v1` subscribes DeviationRaised and DeviationCleared; `rwb.case.events.v1` carries TimerBreached with retry and `.dlt`; `rwb.decision-record.v1` is consumed as its owner provisions it | Not specified in the source documents (DOR-RWB-P3-E2015-OPS-7) |
| Queue | Temporal task queue `rwb-case` in namespace `rwb-recovery` | Not specified in the source documents (DOR-RWB-P3-E2015-OPS-7) |
| Schedules | None for this capability; JOB-05 is retired and JOB-21 is the platform's | Not specified in the source documents (DOR-RWB-P3-E2015-OPS-7) |
| Dashboard series | timers by status, overdue timers, escalated timers, prescription warnings in force, timer projection lag, S8 read timeouts, S8 read breaches, MSG-GEN-006 rate, refused reads, out-of-scope reads, TimerBreached volume, workflow open and stuck | Not specified in the source documents (DOR-RWB-P3-E2015-OPS-7) |
| Runbook entries | stuck timer, deviation read down, escalation not applied, projection stopped, refused read is not an incident | Not specified in the source documents (DOR-RWB-P3-E2015-OPS-7) |
| Secrets | The rwb-case login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store | Not specified in the source documents (DOR-RWB-P3-E2015-OPS-7) |

The alert values are deployment values; the provisional values and their confirmation are carried by the gap and the assumption of section 14 (GAP-0715; ASM-1262). The exact cluster topology, node pools, replica counts and probe timings are deployment values of the platform chart and are not fixed here.

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the two read operations of RWB-P3-E2015-CON behind gateway-bff: `GET /api/recovery/case/v1/cases/{caseId}` with `deviations[]` and `deviationsAvailable`, and `GET /api/recovery/case/v1/cases/{caseId}/timers` with the escalation and warning fields. Owner rwb-case (P3). The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The deviation rows of the case answer; 2 s client budget and a breaker (GAP-0714; ASM-1261) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The approver on each deviation decision; 2 s client budget and a breaker |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The authorisation check before either read; cached per request |

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.case.TimerBreached.v1` (event 19) | `rwb.case.events.v1` | The topic, its retry topic and its `.dlt` topic already exist for rwb-case; the deployment reuses them and creates no new topic |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | Shared topic owned by the platform and rwb-decision; reused, not recreated |

#### 12.4 Events consumed

| Event | Topic | Owner | Service | Provisioning |
|---|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 | rwb-case | Consumer group `rwb-case` with the inbox of schema rwb_case; retry and `.dlt` configured in the same step |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 | rwb-case | Same consumer group, same retry and `.dlt` path |
| `rwb.decision.RulePackageInForce.v1` (event 30) | `rwb.decision.events.v1` | Not specified in the source documents (DOR-RWB-P3-E2015-OPS-24) | rwb-case | Consumer group `rwb-case`, already provisioned for the case capability and reused here |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case-{caseId} | `rwb-case` | Worker deployment with the build ID of the release; holds the durable timer and the escalation |
| Timer projection write | Activity inside the workflow | `rwb-case` | Registered by the same worker; the series the projection lag is computed from |
| Timers projection read | Query inside the service | `rwb-case` | Served by the api deployment; not a Temporal element |

#### 12.6 Schedules

None. The deployment registers no timer-check Schedule and no cron entry for this capability, because the five-minute check is replaced by the durable timer inside CaseWorkflow (DP-10; Architecture v5 slide 44, JOB-05 retired). The platform's stuck workflow scan (JOB-21) runs every five minutes as a visibility query and is not registered by this release.

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| recovery_case, timer, task | P3 (rwb_case) | Created and migrated by the per-service Flyway sequence in the migration job |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Created by the same migration job; used by the two consumer groups and the outbox relay |

`deviation` belongs to S8 and `decision_log_entry` to P7; the migration job touches schema `rwb_case` only (DP-01).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-deviation WireMock | Runs in the pipeline and in the SIT smoke profile, including the healthy answer, the empty answer and the delayed answer beyond 2 s |
| rwb-decision WireMock | Same, including entry DLE-9101 and approver U-LG-01 |
| rwb-access WireMock | Same, including a granted read and a refused read |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed in the deployment path | The two reads; deviations, decision log and authorise; one hop, 2 s |
| Kafka | 2 published by their owners, 3 consumed | TimerBreached and DecisionRecorded reused; DeviationRaised, DeviationCleared and RulePackageInForce consumed with retry and `.dlt` |
| Temporal | 1 workflow, 1 activity, no Schedule | CaseWorkflow with the durable timer and the projection write |
| File | None | The release reads no runtime file; values files are build inputs |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | The monolith base path of the legacy API (Template and Rules §R5.5, DP-13) | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

No pattern is claimed for the parameters contract (DP-06): the capability reads no parameter, and the warning days are applied where `warn_at` is computed.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-case/` | Chart with api and worker deployments, service, migration job, config map, secret references, probes and the Schedule hook that registers nothing for this capability |
| `helm/rwb-case/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, `rwb.p3.case-clocks`, the two client timeouts, the alert thresholds |
| Pipeline stage | Build, unit, component and contract tests, retired-element check, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Consumer group `rwb-case` on `rwb.deviation.events.v1` for the two deviation events with retry and `.dlt`; reuse of `rwb.case.events.v1`, `rwb.decision-record.v1` and `rwb.decision.events.v1`; task queue `rwb-case` in namespace `rwb-recovery` |
| Dashboards | Eight panels: timers by status; overdue timers; escalated timers; prescription warnings in force; timer projection lag; S8 read timeouts and breaches; MSG-GEN-006 rate; refused and out-of-scope reads |
| Alerts | Five rules, each with a message ID and one runbook entry |
| Runbook | Five entries: stuck timer, deviation read down, escalation not applied, projection stopped, refused read is not an incident |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running and the Temporal worker on `rwb-case` has polled; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database and neither calls another service.

**Projection lag.** The series is the difference between the durable timer's fire time, which the workflow exposes as its history, and the first read of the timer row with the new status; it is exposed as a histogram and read on the dashboard and by the projection alert. It is not a job-lateness measure, because there is no job.

**Alert mapping.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-GEN-006 | The S8 deviation read times out or breaches on a share of case-record reads | Degradation-rate alert with the S8 owner, the breaker state and the environment | Platform on-call, ticket to the S8 owner |
| MSG-GEN-006 | The timer projection lag passes its value | Projection-lag alert with the lag and the oldest affected case | Platform on-call, page |
| MSG-P4-002 | A read without Case record R is refused | Refused-read count on the dashboard | No page |
| MSG-P4-003 | A case outside the caller's scope is requested | Out-of-scope count on the dashboard | No page |
| None | TimerBreached volume leaves its band in either direction | Volume alert with the count, the band and the change against the trailing hour | Platform on-call, page when the band is exceeded upward, ticket downward |
| None | JOB-21 raises a stuck workflow on `rwb-case` | Stuck-workflow alert with the workflow ID, the stage and the last event | Platform on-call, page |

Every alert carries its message ID where the condition maps to one, and the two conditions without a message ID carry the workflow or the series name instead. The alert thresholds are deployment values with provisional defaults; the missing source for them is carried by the gap and the assumption of section 14 (GAP-0715; ASM-1262).

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact and fails on a fake drift or a retired element, the two consumer groups exist with their retry and `.dlt` paths, the eight panels carry the synthetic day, the six alert conditions fire on synthetic metrics, and the five runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-006 | The deviation read times out or the projection stops moving | {system} is not available. Try again in a few minutes. |
| MSG-P3-003 | A timer or the prescription date is inside its warning period | {timer} ends on {date}. |
| MSG-P3-004 | The case is on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-018 | The case has no running, paused or expired timer | There are no running timers on this case. |
| MSG-P4-002 | A read without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the person's scope | This case is not in your scope. |

The alert values are Not specified in the source documents (GAP-0715; ASM-1262): the message texts are copied unchanged from the legacy story and the deployment adds the routing, the threshold and the runbook link, never a new wording.

### 15. Screens and states

The deployment serves SCR-03 Case record in its Loading, Read only, Editable, On hold and Degraded states (empty, error and no access: Not specified in the source documents (CG-ALL-4233)) behind the gateway-bff composite route (DP-19). The deviation raise screen and deviation queue (SCR-06, SCR-08) are gateway-bff composite routes at the edge over this service's read and command contract; their read operation is confirmed with the platform edge owner before the wave 2 screen test (GAP-1830). The operator-facing surfaces of this story are the pipeline run view, the release view, the eight dashboard panels and the runbook; the smoke step opens the case record of a synthetic case in SIT and asserts that the timers, the prescription date and the deviation section answer inside the 2 s budget. Every message the service shows keeps its message ID and English wording and is served from the message catalogue in Thai and in English; the Thai wording and its approver are left to DL10 (GAP-1831).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2015-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with a pinned digest, the rwb-case login reference, the migration job and the worker on `rwb-case` |
| TC-P3-E2015-OPS-02 | AC2 | NFR | One pipeline run produces one image and one chart version and fails on a fake drift, a critical scan finding or a retired element |
| TC-P3-E2015-OPS-03 | AC3 | NFR | The `rwb-case` consumer group on `rwb.deviation.events.v1` for both deviation events with retry and `.dlt`; a missing `.dlt` fails the release |
| TC-P3-E2015-OPS-04 | AC4 | NFR | The projection-lag series answers; no timer-check Schedule, queue or job is registered in any environment |
| TC-P3-E2015-OPS-05 | AC5 | NFR | A synthetic day with four timer statuses, two escalations, three prescription warnings, a slow S8 answer and a refused read; eight panels populated |
| TC-P3-E2015-OPS-06 | AC6 | NFR | Six synthetic conditions raise their alerts and resolve one runbook entry each, with the message ID and the escalation path |
| TC-P3-E2015-OPS-07 | §12.4, §12.5 | Contract | The `rwb-case` consumer group on both deviation events, CaseWorkflow on `rwb-case` and the timer projection write activity match the operations, events and activities of §12 |
| TC-P3-E2015-OPS-08 | §12.7 | Boundary | The migration job creates recovery_case, timer and task and the PLT library tables in rwb_case only; a write to deviation or decision_log_entry is refused |
| TC-P3-E2015-OPS-09 | AC7 | NFR | A release built with a credential other than the rwb-case login |
| TC-P3-E2015-OPS-10 | AC8 | NFR | A migration run against an empty rwb_case schema, then a deployment readiness check |
| TC-P3-E2015-OPS-11 | AC9 | NFR | A consumer fed an event it cannot process, followed by the retry and .dlt path |
| TC-P3-E2015-OPS-12 | AC10 | NFR | A scan of every environment for a timer-check Schedule or job |
| TC-P3-E2015-OPS-13 | AC11 | NFR | The topic registry and the TimerBreached and deviation event publications |
| TC-P3-E2015-OPS-14 | AC12 | NFR | A values file change to replica counts, timeouts and alert thresholds, with a hard-coded value check |
| TC-P3-E2015-OPS-15 | AC13 | NFR | A synthetic alert, checked for message ID, agreed text and one runbook link |
| TC-P3-E2015-OPS-16 | AC14 | NFR | A synthetic refused read and an out-of-scope read, checked against the on-call rota |
| TC-P3-E2015-OPS-17 | AC15 | NFR | A stuck CaseWorkflow visible to the platform stuck-workflow scan |
| TC-P3-E2015-OPS-18 | AC16 | NFR | A dashboard series, log line and alert payload scan for personal data |

### 17. Guardrails

- No business value in a values file: the warning days, the escalation roles, the deviation codes and the timer and deviation labels are reference data held by their owner, never a deployment value.
- No personal data in logs, dashboard series, alert payloads or the runbook: case IDs, workflow IDs, user IDs of staff, counts and durations only.
- One login per service; the chart carries the rwb-case login reference and no other service's credential (DP-02).
- The service writes only schema rwb_case; the migration job never touches another schema and no dashboard query reads one (DP-01).
- Every subscription has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- No new topic and no timer-check Schedule: the capability reuses `rwb.case.events.v1` and `rwb.deviation.events.v1`, and the clock is the durable timer inside CaseWorkflow (DP-10, DP-14).
- ACE data is read only through the owner's contract or the `v_ace_*` views; no dashboard reads an ACE view or another service's schema.
- The release pins the image digest and the chart version, and no secret is written into a values file, a chart template, a dashboard or the runbook.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-WKM-004 | A breached service level visible to the escalation role without the case moving | Escalated-timers panel, TimerBreached volume alert and the escalation-not-applied runbook entry | TC-P3-E2015-OPS-05, TC-P3-E2015-OPS-06 |
| REQ-WKM-005 | Timers, escalation state and the deviation flag on the case record view | Timers-by-status panel, overdue panel, prescription-warning panel, the two consumer groups and the degradation rate | TC-P3-E2015-OPS-03, TC-P3-E2015-OPS-05 |
| REQ-DVH-002 | A deviation pauses the stage clock and keeps the prescription clock running | The two deviation consumer groups, the projection-lag series and the deviation read-down runbook entry | TC-P3-E2015-OPS-03, TC-P3-E2015-OPS-06 |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the recommendation, the approval and the outcome | The decision log read in the deployment path and its breaker metrics | TC-P3-E2015-OPS-02 |
| ADR-023 | Observability per service | Eight panels, six alert conditions and five runbook entries | TC-P3-E2015-OPS-05, TC-P3-E2015-OPS-06 |

### 19. Out of scope

- The application code of the two read operations, the merge and the panels (RWB-P3-E2015-APP).
- The contract documents and the fakes as published artefacts (RWB-P3-E2015-CON); this story only deploys the test copies.
- The timer mechanism, the escalation write and the TimerBreached publication (RWB-P3-E1028-APP).
- The platform topic provisioning, the Temporal cluster and the observability stack (the platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The stuck workflow scan itself (JOB-21, platform) and the six-monthly access review.
- The rwb_case schema design and the logical model (the database stories of the service epic).
- Data migration from the legacy schema and the reconciliation run (Epic 2 and rwb-source-data).
- The cross-service journey harness and its evidence (RWB-ITG-E2015-ITG).
