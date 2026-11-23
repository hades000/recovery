# RWB-P3-E2004-OPS Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2004-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-Z |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-022, FR-P3-025, FR-P3-033, FR-P3-034) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-004 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the case-side plan-timer path of rwb-case deployed from the service template with its Helm values and its own login, its consumer groups for `rwb.treatment.TreatmentApproved.v1` and `rwb.payment.PaymentMissed.v1` with retry and `.dlt`, its Temporal worker on task queue `rwb-case` with the timer durability settings that keep a 2027 due date on time, no JOB-05 timer-check Schedule anywhere, the readiness and projection-lag measures, the dashboards for plan timers and for the DP04 copy, the alerts and the runbook entries for a timer that did not fire, a consumer that is behind and a projection that stopped moving**, so that **an operator can see within minutes that a plan clock will not fire or that a treatment event is stuck, and repair it without reading code or waiting for a business report**.

This story deploys an existing capability. It adds no topic, builds no endpoint, table, workflow or rule package, and registers no timer-check Schedule: the plan timer is a durable Temporal timer inside CaseWorkflow on task queue `rwb-case`, the projection row is written in schema `rwb_case`, and the treatment record stays in `rwb_treatment` with its owner.

### 2. Business rationale

The legacy capability leaned on a five-minute Quartz check whose only failure signal was a job exception, so a timer that never fired and a night with nothing due looked the same. In the target there is no scheduler row and no job record to inspect: the wait lives in the workflow history (DP-10; ADR-016), and the row the officer sees is a projection. That moves the operational question from "did the job run" to three questions an operator can answer from a dashboard: is the projection moving, is the consumer keeping up, and is the workflow waiting as it should (Architecture v5 slides 28 and 44; JOB-05 retired, JOB-21 stuck workflow scan kept).

The capability is also the one part of the case where a slow owner silently empties a section instead of failing a screen: if the S2 treatment read or the P7 catalogue read does not answer, the plan step retries and then leaves the case in the exception queue with a message, and the officer sees nothing move. That is the right behaviour for the officer and the wrong behaviour for the operator if nobody counts it, which is why the failure rate and the projection lag are dashboard series and alerts here and not a line in a log.

Deployment is therefore part of the capability: the chart carries the rwb-case login and no other credential (DP-02), the migration job runs the per-service Flyway sequence in schema `rwb_case` and creates no treatment object (DP-15; DP-01), the two consumer groups are provisioned with retry and `.dlt` so an approved plan is never lost, the worker deployment pins the build ID and the namespace so a plan timer survives a release, and the runbook names the three failures an operator will actually see.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL; RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF; RWB-PLT-E1071-CON), so CaseWorkflow polls `rwb-case` and the durable plan timers run in every environment.
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT; RWB-PLT-TE006-CON), and `rwb.treatment.events.v1` and `rwb.payment.events.v1` are provisioned by their owners S2 and P8.
- The observability stack of the platform is available (RWB-PLT-OBS; ADR-023): metrics, traces and logs with one trace across REST, Kafka and Temporal.
- The three environments DEV, SIT and UAT exist with their parameter scope and their Kafka and Temporal endpoints.
- RWB-P3-E2004-CON is published, so the smoke profile and the drift test run against the two read operations, the two consumed events and the five fakes of that baseline.
- The parameters and reference data the step reads are loaded by their owning stories — CURE_PERIOD_DAYS, `plan.warn-days`, LOV-TIMER with INSTALLMENT_DUE and CURE_PERIOD, LOV-TIMER-STATUS — and this story reads them and holds no copy.
- The DP04 treatment product is loaded by its owners (P1 rwb-source-data; P9 rwb-reporting under the bank Airflow, JOB-15), so the freshness panel has a source.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests of RWB-P3-E2004-CON, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-case with the rwb-case login, the pre-deploy migration job for schema `rwb_case`, the readiness and liveness probes, the api deployment and the worker deployment that polls `rwb-case` in namespace `rwb-recovery`.
3. The provisioning step declares the two subscriptions of this capability on consumer group `rwb-case`: `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1` and `rwb.payment.PaymentMissed.v1` on `rwb.payment.events.v1`, each with its retry topic and its `.dlt` topic and the inbox of schema `rwb_case`.
4. The provisioning step asserts that no timer-check Schedule, timer-check task queue, timer-check job or `TimerDue` topic exists for this capability, that no treatment topic is created by rwb-case, and that `rwb.case.events.v1` carries CaseStateChanged with its retry and `.dlt` topics.
5. The worker deployment pins the release build ID and the namespace, and the release records the workflow retention and the Continue-As-New policy that keep a plan timer of 2027 durable across restarts and upgrades.
6. The dashboards are published: plan timers by type and status, plan timers inside their warning window, overdue plan timers, the projection lag, the ART of the two consumer subscriptions, the `.dlt` count, the retry count, the rate of MSG-P7-003 and MSG-P1-001, the DP04 freshness of the treatment product, and the count of cases in the exception queue for a plan step.
7. The alerts are wired to the message IDs of section 14 and to the runbook entries of section 13; the thresholds are values and carry the placeholder of section 14 until they are confirmed.
8. A smoke step opens the case record of a synthetic case through gateway-bff in the SIT profile and asserts that the plan timers and the route state answer inside the 2 s budget with the fakes of §12.8.
9. The runbook is published and reviewed with the on-call rota: a plan timer that did not fire, a subscription that is behind or in `.dlt`, a projection that stopped moving, a DP04 load that is late, and a refused read that is not an incident.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | A subscription is provisioned without its retry or `.dlt` topic | The provisioning step fails the release and the consumer refuses to start | None | AC3 |
| X3 | A consumer subscription falls behind its lag value | The lag alert fires and the lag runbook entry opens with the subscription, the lag and the oldest event | None | AC4, AC6 |
| X4 | The projection lag passes its value | The projection-lag alert fires and the projection runbook entry starts from the workflow history of the oldest case | None | AC4, AC6 |
| X5 | An event lands in `.dlt` | The `.dlt` count alert fires and the runbook names the event, the key and the refusal | MSG-P3-005 | AC3, AC6 |
| X6 | The plan step leaves cases in the exception queue | The exception-queue panel rises and the plan-step runbook entry checks the S2 and P7 answers | MSG-P7-003 | AC6 |
| X7 | A workflow stops on a non-retryable failure | The stuck workflow scan of JOB-21 raises the case and the stuck-timer runbook entry starts from its history | None | AC6 |
| X8 | The DP04 load of the treatment product is late | The freshness panel shows the previous business date and its age; the DP04 runbook entry names the owning service and the load | MSG-P1-001 | AC5, AC6 |
| X9 | A role without Case record R is refused, or a case is out of scope | The counts rise on the dashboard and no page is sent | MSG-P4-002, MSG-P4-003 | AC5 |
| X10 | A release declares a timer-check Schedule, a `TimerDue` topic or a treatment object in `rwb_case` | The pipeline fails the release on the retired-element check of AC4 | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the observability stack; builds no application code |
| Negotiable | Replica counts, resource sizes, alert thresholds, retention and probe timings are environment values, not story decisions |
| Valuable | Makes a capability with no scheduler row observable: the projection, the subscriptions and the workflow each have a signal, an owner and a runbook entry |
| Estimable | One chart, one pipeline stage, one migration job, two probes, two subscriptions, nine dashboard panels, eight alert rules and five runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the subscriptions exist, the panels carry data, the alerts fire on a synthetic metric, the runbook entry resolves |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the case-side plan-timer path

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT
    Given the Temporal namespace is rwb-recovery and the task queue is rwb-case

  Scenario: AC1 The Helm chart and values deploy rwb-case with its own login and the plan-timer switch (new, D-RCV-60)
    Given the rwb-case Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-case login reference and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_case before the deployment is marked ready and creates no treatment object
    Then the api deployment and the worker deployment start from the same image, and the worker polls task queue rwb-case in namespace rwb-recovery with the build ID of the release
    Then the values files carry the feature switch rwb.p3.plan-timers and no parameter value, no timer length and no warning day
    Then no replica count, resource size, timeout, threshold or cadence is hard-coded in the template

  Scenario: AC2 The pipeline promotes one artefact and runs the contract tests (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit, component and contract tests of RWB-P3-E2004-CON and fails the build on a drift between a fake and the document
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 The two subscriptions are provisioned with retry and dead-letter paths (new, D-RCV-60)
    Given the provisioning step of rwb-case for the plan-timer path
    When it runs against the environment
    Then consumer group rwb-case subscribes to rwb.treatment.events.v1 for TreatmentApproved and to rwb.payment.events.v1 for PaymentMissed, with the inbox of schema rwb_case
    Then each subscription has its retry topic and its .dlt topic and the consumer never acknowledges an event it could not process
    Then CaseStateChanged is produced on the existing rwb.case.events.v1 with its retry and .dlt topics and no new topic is created for this capability
    Then rwb.treatment.events.v1 and rwb.payment.events.v1 are consumed as their owners provisioned them and are not recreated
    Then the provisioning step fails the release when a retry or .dlt topic is missing

  Scenario: AC4 The worker durability settings are set and no timer-check Schedule exists (new, D-RCV-60)
    Given the worker deployment and the published metrics of the capability
    When the deployed resources and the workflow settings are listed
    Then the worker polls rwb-case in namespace rwb-recovery with a pinned build ID and a versioning policy that lets a running plan workflow finish on its own build
    Then the release records the namespace retention and the Continue-As-New policy of CaseWorkflow, so a plan timer of 2027 survives a restart, a release and a history roll-over
    Then the lag between a plan timer being armed and its projection row being readable is exposed as a series with its alert value
    Then no timer-check Schedule, no timer-check task queue, no timer-check job and no TimerDue topic is registered for any environment
    Then a release that declares a timer-check Schedule, a TimerDue topic or a treatment object in rwb_case fails the retired-element check

  Scenario: AC5 The dashboards carry the nine capability series (new, D-RCV-60)
    Given the published dashboard
    When a synthetic day is replayed with running, expired and stopped plan timers, two timers inside their warning window, one overdue timer, a slow S2 answer, one event in .dlt, three cases in the exception queue and a late DP04 load
    Then the panels show plan timers by type and status, timers inside the warning window, overdue timers, the projection lag, the subscription lag of the two subscriptions, the .dlt and retry counts, the MSG-P7-003 and MSG-P1-001 rates, the treatment-product freshness and the exception-queue count
    Then every panel names its service, its environment and its business date
    Then a refused read and an out-of-scope read are counted and never page the on-call rota
    Then no panel carries a customer name, an account number or a personal identifier

  Scenario: AC6 The alerts and the runbook cover the operator failures (new, D-RCV-60)
    Given the eight alert rules and the published runbook
    When the projection lag passes its value, a subscription falls behind its lag value, an event lands in .dlt, the exception-queue count rises and the DP04 load is late
    Then each condition raises its alert with its message ID where it has one, its environment and its links to the case and the workflow
    Then the runbook holds one entry each for a plan timer that did not fire, a subscription that is behind or in .dlt, a projection that stopped moving, a DP04 load that is late and a refused read that is not an incident, with the check, the owner role and the recovery step
    Then every alert links exactly one runbook entry and every entry names the escalation path when the step fails
```

These six criteria are new for the deployment and test artefacts only; they restate no business outcome owned by RWB-P3-E2004-APP. The alert values are provisional and are carried by GAP-0706 and ASM-1253.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-case login and no other service's credential | DP-02; Architecture v5 slide 29 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_case` and runs before the deployment is ready; it creates no treatment object | DP-15; DP-01; RWB-PLT-E1044-CON |
| BR3 | Every subscription has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Architecture v5 slide 22 notes |
| BR4 | No timer-check Schedule, no timer-check job and no TimerDue topic exists: the plan clock is a durable timer inside CaseWorkflow (JOB-05 retired) | DP-10; Architecture v5 slide 44; ASM-0078 |
| BR5 | No new topic is created for this capability; `rwb.case.events.v1` carries CaseStateChanged and the two treatment and payment topics stay their owners' | DP-14; Architecture v5 slide 42 |
| BR6 | No environment value is hard-coded: replica counts, resource sizes, timeouts, retention and alert thresholds come from values files | Template and Rules §R7.2 s17 |
| BR7 | An alert carries a message ID where the condition has one, and links exactly one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | A refused read and an out-of-scope read are counted on the dashboard and never page the on-call rota | MSG-P4-002; MSG-P4-003 |
| BR9 | The stuck workflow scan is the platform's (JOB-21, a visibility query every five minutes) and is reused, not rebuilt | Architecture v5 slide 44 |
| BR10 | No dashboard series, log line or alert payload carries personal data; case, workflow, treatment and timer identifiers only | Template and Rules §R7.2 s17 |
| BR11 | No business value is a deployment value: the cure period, the warning days, the timer types and the escalation roles stay parameters and reference data of their owners | DP-06; DP-07; BR10 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version, the outbox relay runs and the worker polls `rwb-case` | Ready |
| Ready | Release superseded | A new chart version is promoted and the worker build ID moves | Rolling |
| Rolling | Running plan workflows are on their pinned build | The old ReplicaSet drains only after each running workflow finishes or rolls over | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning step, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the visibility queries behind JOB-21 |
| ACE database administrator | Owns schema `rwb_case`, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the runbook entries and opens an incident when a plan timer, a subscription or a projection stays wrong |
| Service owner of S2 rwb-treatment | Is paged by the treatment-read and treatment-event alerts and owns the repair beyond the rwb-case retry |
| Service owner of P7 rwb-decision | Is paged by the catalogue and version alerts and owns the package registry |
| Service owner of P1 rwb-source-data | Is paged by the DP04 freshness alert and owns the load |

The per-service login name used by the chart is a secret reference resolved at deploy time; the chart references "the rwb-case login (DP-02)" and never a literal name.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switch `rwb.p3.plan-timers`, the two client timeouts, the workflow retention, the Continue-As-New policy, the alert thresholds |
| Schema | `rwb_case`, migrated by the per-service Flyway sequence; the tables `recovery_case`, `timer` and `task` with the library objects; no treatment object |
| Topics | `rwb.treatment.events.v1` subscribes TreatmentApproved; `rwb.payment.events.v1` subscribes PaymentMissed; `rwb.case.events.v1` carries CaseStateChanged with retry and `.dlt`; `rwb.decision-record.v1` is produced as its owner provisions it |
| Queue | Temporal task queue `rwb-case` in namespace `rwb-recovery` |
| Schedules | None for this capability; JOB-05 is retired, JOB-21 is the platform's and JOB-15 is rwb-reporting's |
| Dashboard series | plan timers by type and status, plan timers inside the warning window, overdue plan timers, projection lag, subscription lag of the two subscriptions, `.dlt` count, retry count, MSG-P7-003 rate, MSG-P1-001 rate, treatment-product freshness, exception-queue count |
| Runbook entries | plan timer not fired, subscription behind or in `.dlt`, projection stopped, DP04 load late, refused read is not an incident |
| Secrets | The rwb-case login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |

The alert values are deployment values and are Not specified in the source documents (GAP-0706; ASM-1253). The exact cluster topology, node pools, replica counts and probe timings are deployment values of the platform chart and are not fixed here.

### 12. Contract

#### 12.1 REST operations provided

The deployment exposes the two read operations of RWB-P3-E2004-CON behind gateway-bff: `GET /api/recovery/case/v1/cases/{caseId}/timers` with the plan fields and `GET /api/recovery/case/v1/cases/{caseId}` with `routeState` and `ruleVersion`. Owner rwb-case (P3). The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment record the plan step reads; 2 s client budget and a breaker |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The approval entry checked before the first move; 2 s client budget and a breaker |
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` | P7 rwb-decision | The action text, owner role and timer spec of R-RES-25 and R-RES-27; 2 s client budget and a breaker |
| GET | `/api/recovery/source-data/v1/data-products/DP04/records` | P1 rwb-source-data | The DP04 treatment rows whose freshness the dashboard tracks (GAP-0704; ASM-1251) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The authorisation check before either read; cached per request |

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | The topic, its retry topic and its `.dlt` topic already exist for rwb-case; the deployment reuses them and creates no new topic |
| `rwb.decision-record.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | Shared topic owned by the platform and rwb-decision; produced by the local decision-record library, reused and not recreated |

#### 12.4 Events consumed

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` (event 10) | `rwb.treatment.events.v1` | Consumer group `rwb-case` with the inbox of schema `rwb_case`; retry and `.dlt` configured in the same step |
| `rwb.payment.PaymentMissed.v1` (event 12) | `rwb.payment.events.v1` | Same consumer group, same retry and `.dlt` path |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case ID | `rwb-case` | Worker deployment with the build ID of the release; holds the plan-timer step and the durable plan timers |
| PlanTimerStep | Activity | `rwb-case` | Registered by the same worker; the write of the projection row the lag series is computed from |
| EvaluateRules, RecordAndApply | Activities (workflow kit) | `rwb-case` | Registered by the same worker as the kit provides them; no new activity code is deployed by this story |
| Timers projection read | Query inside the service | `rwb-case` | Served by the api deployment; not a Temporal element |

#### 12.6 Schedules

None. The deployment registers no timer-check Schedule and no cron entry for this capability, because the five-minute check is replaced by the durable timer inside CaseWorkflow (DP-10; Architecture v5 slide 44; JOB-05 retired). The platform's stuck workflow scan (JOB-21) runs every five minutes as a visibility query and is not registered by this release; the 01:30 DP04 extract (JOB-15) belongs to rwb-reporting and is loaded by the bank Airflow.

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| recovery_case, timer, task | P3 (rwb_case) | Created and migrated by the per-service Flyway sequence in the migration job, including `timer.treatment_id` |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Created by the same migration job; used by the two subscriptions and the outbox relay |

`treatment` belongs to S2 in `rwb_treatment` and `dp_treatment` to P1 in `rwb_source_data`; the migration job touches schema `rwb_case` only and creates no treatment object (DP-01).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-treatment WireMock | Runs in the pipeline and in the SIT smoke profile, with the healthy treatment answer, the refusal answers and the TreatmentApproved event |
| rwb-decision WireMock | Same, with entry DLE-9001 and approver U-APR-01, the R-RES-25 and R-RES-27 catalogue rows at RES-2026.12 and the no-version answer |
| rwb-payment WireMock | Same, with PaymentMissed for due date 2026-12-31 |
| rwb-source-data WireMock | Same, with the ten DP04 rows and the stale answer of MSG-P1-001 |
| rwb-access WireMock | Same, with a granted read and a refused read |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed in the deployment path | The two reads; treatment, decision log, rule catalogue, DP04 records and authorise; one hop, 2 s |
| Kafka | 2 published, 2 consumed | CaseStateChanged and DecisionRecorded produced; TreatmentApproved and PaymentMissed consumed with retry and `.dlt` |
| Temporal | 1 workflow, 3 activities, no Schedule | CaseWorkflow with the plan-timer step, EvaluateRules and RecordAndApply, and the durable plan timers |
| File | None | The release reads no runtime file; values files are build inputs |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 adds nothing here: no dashboard reads an ACE view and the deployment declares none. DP-19 adds nothing to this story's deliverable either, because the composite route is the platform contract's; the smoke step only passes through it.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-case/` | Chart with api and worker deployments, service, migration job, config map, secret references, probes and the release annotations that record the workflow retention and the Continue-As-New policy |
| `helm/rwb-case/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, `rwb.p3.plan-timers`, the two client timeouts, the workflow retention, the alert thresholds |
| Pipeline stage | Build, unit, component and contract tests, retired-element check, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Consumer group `rwb-case` on `rwb.treatment.events.v1` for TreatmentApproved and on `rwb.payment.events.v1` for PaymentMissed with retry and `.dlt`; reuse of `rwb.case.events.v1` and `rwb.decision-record.v1`; task queue `rwb-case` in namespace `rwb-recovery` |
| Dashboards | Nine panels: plan timers by type and status; timers inside the warning window; overdue timers; projection lag; subscription lag; `.dlt` and retry counts; MSG-P7-003 and MSG-P1-001 rates; treatment-product freshness; exception-queue count |
| Alerts | Eight rules, each with a message ID where it has one and one runbook entry |
| Runbook | Five entries: plan timer not fired, subscription behind or in `.dlt`, projection stopped, DP04 load late, refused read is not an incident |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running and the Temporal worker on `rwb-case` has polled; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database and neither calls another service.

**Projection lag.** The series is the difference between the moment the plan-timer step arms the durable timer, as the workflow exposes it on its history, and the first read of the projection row with its new status; it is exposed as a histogram and read on the dashboard and by the projection alert. It is not a job-lateness measure, because there is no job.

**Alert mapping.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-GEN-006 | The S2 treatment read or the P7 read times out or breaches on a share of plan steps | Degradation-rate alert with the owner, the breaker state and the environment | Platform on-call, ticket to the owning service |
| MSG-P7-003 | A plan step cannot write its decision record and leaves the case in the exception queue | Exception-queue alert with the case, the timer type and the oldest entry | Platform on-call, page when the count passes its value |
| MSG-P1-001 | The DP04 treatment product is older than its business date | Freshness alert with the product and the last loaded business date | Platform on-call, ticket to the P1 owner |
| MSG-P3-005 | A plan-timer event lands in `.dlt` | `.dlt` alert with the event, the case key and the refusal | Platform on-call, page |
| MSG-P4-002 | A read without Case record R is refused | Refused-read count on the dashboard | No page |
| None | The projection lag passes its value | Projection-lag alert with the lag and the oldest affected case | Platform on-call, page |
| None | A subscription passes its lag value | Subscription-lag alert with the subscription, the lag and the oldest event | Platform on-call, page |
| None | JOB-21 raises a stuck workflow on `rwb-case` | Stuck-workflow alert with the workflow ID, the stage and the last event | Platform on-call, page |

Every alert carries its message ID where the condition maps to one, and the conditions without a message ID carry the workflow or the series name instead. The alert thresholds are deployment values and are Not specified in the source documents (GAP-0706; ASM-1253).

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact and fails on a fake drift or a retired element, the two subscriptions exist with their retry and `.dlt` paths, the worker polls `rwb-case` with a pinned build ID and the recorded retention, the nine panels carry the synthetic day, the eight alert conditions fire on synthetic metrics, and the five runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-006 | A consumed owner does not answer in time or the projection stops moving | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The treatment data product is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-005 | An event is refused because the case is closed or not in the state the rule expects | This case cannot move to {state} from {current}. |
| MSG-P4-002 | A read without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the person's scope | This case is not in your scope. |

The message texts are copied unchanged from the legacy story and the deployment adds the routing, the threshold and the runbook link, never a new wording. The alert values are Not specified in the source documents (GAP-0706; ASM-1253).

### 15. Screens and states

The deployment serves SCR-03 Case record in its Loading, Read only and Degraded states behind the gateway-bff composite route (DP-19), and SCR-09 Exception queue for the cases a plan step refused. The operator-facing surfaces of this story are the pipeline run view, the release view, the nine dashboard panels and the runbook; the smoke step opens the case record of a synthetic case in SIT and asserts that the plan timers and the route state answer inside the 2 s budget.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2004-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with a pinned digest, the rwb-case login reference, the migration job without a treatment object, the api and worker deployments on `rwb-case` and the `rwb.p3.plan-timers` switch |
| TC-P3-E2004-OPS-02 | AC2 | NFR | One pipeline run produces one image and one chart version and fails on a fake drift, a critical scan finding or a retired element |
| TC-P3-E2004-OPS-03 | AC3 | NFR | Consumer group `rwb-case` on `rwb.treatment.events.v1` and `rwb.payment.events.v1` with retry and `.dlt`; a missing `.dlt` fails the release |
| TC-P3-E2004-OPS-04 | AC4 | NFR | The worker build ID, the namespace, the retention and the Continue-As-New policy; no timer-check Schedule, queue, job or TimerDue topic in any environment |
| TC-P3-E2004-OPS-05 | AC5 | NFR | A synthetic day with three timer statuses, two warning-window timers, one overdue timer, a slow S2 answer, one `.dlt` event, three exception-queue cases and a late DP04 load; nine panels populated |
| TC-P3-E2004-OPS-06 | AC6 | NFR | Eight synthetic conditions raise their alerts and resolve one runbook entry each, with the message ID and the escalation path |

### 17. Guardrails

- No business value in a values file: the cure period, the warning days, the timer types and the escalation roles are parameters and reference data of their owners, never a deployment value.
- No personal data in logs, dashboard series, alert payloads or the runbook: case, workflow, treatment and timer identifiers, staff user IDs, counts and durations only.
- One login per service; the chart carries the rwb-case login reference and no other service's credential (DP-02).
- The service writes only schema `rwb_case`; the migration job never touches another schema, creates no treatment object and no dashboard query reads one (DP-01).
- Every subscription has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- No new topic and no timer-check Schedule: the capability reuses `rwb.case.events.v1` and the two owner topics, and the clock is the durable timer inside CaseWorkflow (DP-10, DP-14).
- ACE data is read only through the owner's contract or the `v_ace_*` views; this capability reads no ACE view at all.
- The release pins the image digest and the chart version, and no secret is written into a values file, a chart template, a dashboard or the runbook.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome | The S2 treatment read in the deployment path, its breaker metrics and the absence of any treatment object in `rwb_case` | TC-P3-E2004-OPS-01, TC-P3-E2004-OPS-05 |
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | The two subscriptions, the projection-lag series, the plan-timer panels and the timer-not-fired runbook entry | TC-P3-E2004-OPS-03, TC-P3-E2004-OPS-04, TC-P3-E2004-OPS-06 |
| REQ-RDF-014 | Stage 2 data products for plans and treatments exist before the first treatment | The treatment-product freshness panel, the MSG-P1-001 alert and the DP04 runbook entry | TC-P3-E2004-OPS-05, TC-P3-E2004-OPS-06 |
| REQ-CWC-011 | Warning thresholds and escalation targets are data and a breach raises an event without moving the case | The warning-window panel and the timer settings, with no threshold or warning day in a values file | TC-P3-E2004-OPS-01, TC-P3-E2004-OPS-05 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The worker deployment, the retention and Continue-As-New record and the absence of JOB-05 | TC-P3-E2004-OPS-04 |
| ADR-018 | No data lake; rwb-reporting read model from events | The DP04 read in the deployment path and the absence of any extract or data-lake element | TC-P3-E2004-OPS-01, TC-P3-E2004-OPS-05 |
| ADR-023 | Observability per service | Nine panels, eight alert conditions and five runbook entries | TC-P3-E2004-OPS-05, TC-P3-E2004-OPS-06 |

### 19. Out of scope

- The application code of the plan-timer step, the projection, the route moves and the two read answers (RWB-P3-E2004-APP).
- The contract documents and the fakes as published artefacts (RWB-P3-E2004-CON); this story only deploys the test copies.
- The treatment entity, its topics and its own deployment (S2; RWB-S2-E2004-APP and its operations story).
- The package registry and the version in force (P7; RWB-P7-E2042-APP).
- The DP04 treatment product, its 01:30 load and its freshness stamps (P1 rwb-source-data; P9 rwb-reporting).
- The platform topic provisioning, the Temporal cluster and the observability stack (the platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The stuck workflow scan itself (JOB-21, platform) and the six-monthly access review.
- The `rwb_case` schema design and the logical model (RWB-PLT-NF06-DB and the per-service database stories).
- Data migration from the legacy schema and the reconciliation run (Epic 2 and rwb-source-data).
- The cross-service journey harness and its evidence (RWB-ITG-E2004-ITG).
