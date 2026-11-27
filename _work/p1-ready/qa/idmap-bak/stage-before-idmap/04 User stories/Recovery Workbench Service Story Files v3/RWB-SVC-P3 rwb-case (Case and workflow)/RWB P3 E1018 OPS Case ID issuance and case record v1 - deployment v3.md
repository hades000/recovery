# RWB-P3-E1018-OPS Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1018-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Readiness decisions | RD-P1-003, RD-P1-005, RD-P1-040, RD-P1-041 |
| Parallel lane | L-P3-G |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P3-E1018-OPS-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-001, FR-P3-002, FR-P3-003, FR-P3-004, FR-P3-005, FR-P3-006, FR-P3-007, FR-P3-012, FR-P3-030, FR-P3-031, FR-P3-035) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- D-RCV-60 finishing pass: requests W2-tests-4630; Test Cases v9 mappings.

- AceDataReady starts DailyCaseRun only for `sourceSystem` ALS with `status` COMPLETED; the record key and typed data are stated (RD-P1-003, RD-P1-040).
- The freshness read and its test fake carry status `LOADED` / `STALE` and the never-stamped answer (RD-P1-005, RD-P1-041).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-018 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 30 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **Not specified in the source documents (DOR-RWB-P3-E1018-OPS-1)**, I want **rwb-case deployed as one service from the service template, with its Helm chart and values, its Flyway migration job, its readiness and liveness probes, its topic and queue provisioning with retry and dead-letter topics, the DailyCaseRun schedule registration, the case-creation dashboards and the runbook, and the legacy batch alerts mapped to the new signals**, so that **the case-creation capability of RWB-E1-018 runs predictably in every environment and an operator can see and act on a failed or late run without reading code**.

### 2. Business rationale

The legacy story depends on a Quartz job, a shared schema and an in-line scheduler. In the target, a service is a Helm release built by one pipeline, with its own schema, login, topic, queue and Schedules (DP-02, DP-10, DP-15). Deployment is therefore part of the capability: an unregistered schedule or a topic without a dead-letter path silently loses case creations, and an alert that only fires on a job exception does not catch a run held by a missing rule package. This story makes the case-creation run observable and repeatable, so the app story can be proven in SIT and the on-call rota can operate it.

### 3. Preconditions

- The service template, chart skeleton and pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The platform error envelope and the message catalogue are in force, so an alert can carry a message ID.
- The three environments DEV, SIT and UAT exist with the parameter scope of LOV-ENVIRONMENT.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image, runs the unit and contract tests, scans the image and the dependencies, and publishes the Helm chart version.
2. The chart deploys the service with its own login, its schema migration job and its probes; the migration job runs before the deployment is marked ready.
3. The provisioning step creates `rwb.case.events.v1` with its retry topic and `.dlt` topic, and the Temporal task queue `rwb-case` in namespace `rwb-recovery`.
4. The Schedule registration step creates or updates DailyCaseRun with the overlap policy and the catch-up window, and checks that AceDataReady with `sourceSystem` ALS and `status` COMPLETED starts the same workflow for the business date.
5. The dashboards are published: run counts, created, excluded, not entered, linked, failed; run duration; event lag; decision-record lag.
6. The alerts are wired to the message IDs of section 14 and to the runbook entries.
7. A smoke step posts a synthetic business date to the DailyCaseRun trigger in a test namespace and checks that the run record and the probe answer are healthy.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod is removed from the service and the pipeline marks the release failed | None | AC3 |
| X3 | The topic is missing its retry or `.dlt` topic | The provisioning step fails the release; the relay refuses to start | None | AC4 |
| X4 | The Schedule registration is rejected by the namespace | The release fails; a case creation would otherwise never start | None | AC5 |
| X5 | A run waits for a complete ALS batch | The alert carries MSG-P1-001 and the runbook entry for the batch gate | MSG-P1-001 | AC6 |
| X6 | The decision-record write fails during a run | The alert carries MSG-P7-003 and the failed-account count | MSG-P7-003 | AC6 |
| X7 | No rule package version is in force | The alert carries MSG-P3-027 and names the package code | MSG-P3-027 | AC6 |
| X8 | The yearly number range is used up | The alert carries MSG-P3-025 and opens an incident | MSG-P3-025 | AC6 |
| X9 | A role without Case record R is refused | The access-denied signal is counted, not alerted as an incident | MSG-P4-002 | AC6 |
| X10 | A case is outside the reader's scope | The out-of-scope count is visible on the dashboard only | MSG-P4-003 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning and the workflow kit; no application code is built here |
| Negotiable | Replica counts, resource sizes and alert thresholds are environment values, not story decisions |
| Valuable | Makes the case-creation run deployable, observable and repeatable in every environment |
| Estimable | One chart, one pipeline stage, one migration job, two probes, one provisioning step, one schedule registration, four dashboards panels and seven alert rules |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the topics exist, the schedule is registered, the alerts fire on a synthetic metric |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-case case-creation capability

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The Helm chart and values deploy rwb-case (new, D-RCV-60)
    Given the rwb-case Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-case login and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_case before the deployment is marked ready
    Then no replica count, resource size or schedule cadence is hard-coded in the template

  Scenario: AC2 The pipeline builds, tests and promotes one artefact (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit, component and contract tests and fails the build on a contract drift
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 Readiness and liveness probes answer (new, D-RCV-60)
    Given a running rwb-case pod
    When the readiness probe is called before the migration job and the start-up window complete
    Then the pod is not marked ready
    When the readiness and liveness endpoints are called after start-up
    Then both answer healthy without a database write
    Then a failing dependency is reported as not ready and never as live-and-broken

  Scenario: AC4 Topics and the task queue are provisioned with retry and dead-letter paths (new, D-RCV-60)
    Given the provisioning step for rwb-case
    When it runs against the environment
    Then the topic rwb.case.events.v1 exists with its retry topic and its .dlt topic
    Then the shared topic rwb.decision-record.v1 is consumed as provided by the platform and is not recreated
    Then the Temporal task queue rwb-case is registered in namespace rwb-recovery
    Then the outbox relay and the consumer are configured with the retry topic and the .dlt topic

  Scenario: AC5 The DailyCaseRun schedule is registered and fires (new, D-RCV-60)
    Given the Schedule registration step
    When it runs
    Then DailyCaseRun is registered with the daily cadence, the overlap policy SKIP and the catch-up window
    Then a synthetic business date starts one run and a second start for the same business date starts nothing
    Then the run record carries the counts accounts read, excluded, not entered, linked, created and failed

  Scenario: AC6 Dashboards and the runbook cover the legacy alerts (new, D-RCV-60)
    Given the published dashboard and the runbook
    When a synthetic run is replayed with a late batch, a failed decision record, a missing package version and an exhausted number range
    Then each condition raises the alert that carries MSG-P1-001, MSG-P7-003, MSG-P3-027 and MSG-P3-025 with the legacy text
    Then the refused-read and out-of-scope counts carry MSG-P4-002 and MSG-P4-003 and do not page the on-call rota
    Then every alert links one runbook entry with the check, the owner role and the recovery step

  Scenario: AC7 The business rules BR1 to BR8 hold (new, D-RCV-60)
    Given the chart, the migration, the topics, the schedule, the alert set and the read paths of rwb-case
    When each rule BR1 to BR8 is checked against them
    Then only the rwb-case login is used and no other service's credential is referenced (BR1)
    Then the migration is the per-service Flyway sequence in schema rwb_case and completes before the deployment is ready (BR2)
    Then every topic has a retry topic and a .dlt topic and no event is acknowledged unprocessed (BR3)
    Then the Schedule uses overlap policy SKIP with a catch-up window and the event-started workflow takes the business date as input (BR4)
    Then no environment value is hard-coded (BR5)
    Then every alert carries a message ID, the agreed text and one runbook entry (BR6)
    Then refused and out-of-scope reads are counted and do not page the on-call rota (BR7)
    Then the service writes only schema rwb_case and reads no other service's tables (BR8)

  Scenario: AC8 A consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-case consumer or the outbox relay calls a consumed dependency
    When the call fails or does not answer
    Then the event is not acknowledged and is retried through the retry topic and then the .dlt topic
    Then the readiness endpoint reports the dependency as not ready and never as live-and-broken

  Scenario: AC9 The case-created event and the P7 decision record reach the platform (new, D-RCV-60)
    Given a smoke run of the release that creates a case
    When the case is created
    Then rwb.case.CaseCreated.v1 is on rwb.case.events.v1 through the outbox relay
    Then rwb.decision.DecisionRecorded.v1 is on rwb.decision-record.v1 and the entry is in the P7 central decision ledger (DP-03)
    Then the run is cleaned up with the P7 administrative rollback
    Then the ALS batch is seeded through the W1J01 harness and the exact synthetic case set is Not specified in the source documents (GAP-0343)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-case login and no other service's credential | DP-02; Arch v5 slide 41 notes |
| BR2 | The migration is a per-service Flyway sequence in schema rwb_case and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every topic has a retry topic and a `.dlt` topic; a consumer never acknowledges an event it could not process | DP-09; Arch v5 slide 42 notes |
| BR4 | A Temporal Schedule uses overlap policy SKIP with a catch-up window, and an event-started workflow takes the business date as its input | DP-10; Arch v5 slide 44 notes |
| BR5 | No environment value is hard-coded: replica counts, resource sizes, thresholds and cadences come from values files and parameters | DP-06; Template and Rules §R7.2 s17 |
| BR6 | An alert carries a message ID and the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | A refused read and an out-of-scope read are counted on the dashboard and never page the on-call rota | MSG-P4-002, MSG-P4-003 |
| BR8 | The service writes only schema rwb_case and reads no other service's tables | DP-01 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version and both probes answer | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning and schedule registration steps, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the Schedule registration rights |
| ACE database administrator | Owns the rwb_case schema, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the runbook entries and opens an incident when MSG-P3-025 or MSG-P7-003 persists |
| RW-PLATADM | Reads and operates the case-creation run in the running service, not in the cluster |

The per-service login name used by the chart is Not specified in the source documents (GAP-0675; ASM-1222); the chart references "the rwb-case login (DP-02)" through a secret reference and never a literal name.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switches | BR5 |
| Schema | rwb_case, migrated by the per-service Flyway sequence; the tables `recovery_case`, `case_account`, `case_party` and `case_entry_exclusion` plus the library objects | BR2, BR8 |
| Topics | `rwb.case.events.v1` with retry and `.dlt`; `rwb.decision-record.v1` consumed as provided | BR3 |
| Queue | Temporal task queue `rwb-case` in namespace `rwb-recovery` | Not specified in the source documents (DOR-RWB-P3-E1018-OPS-7) |
| Schedule | DailyCaseRun with the daily cadence, overlap policy SKIP and catch-up window | BR4 |
| Dashboard series | run started, run finished, accounts read, excluded, not entered, linked, created, failed, run duration, event lag, decision-record lag, refused reads, out-of-scope reads | BR7 |
| Runbook entries | batch gate, decision record failure, package not in force, number range exhausted, migration failure, probe failure | BR6 |
| Secrets | The rwb-case login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store | BR1 |

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) is Not specified in the source documents (GAP-0677; ASM-1224); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded.

### 12. Contract

This story builds against contract version v1, the version of the /v1 paths and event types named in sections 12.1 to 12.9.

#### 12.1 REST operations provided

The deployment exposes the four case operations of the contract baseline behind gateway-bff: `GET /api/recovery/case/v1/cases`, `GET /api/recovery/case/v1/cases/{caseId}`, `GET /api/recovery/case/v1/cases/{caseId}/accounts` and `GET /api/recovery/case/v1/cases/{caseId}/parties`. Owner rwb-case (P3). The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/data-products/freshness` | P1 rwb-source-data | Batch completeness for the business date; 2 s client budget (DP-11). `status` `LOADED` / `STALE`; `businessDate` null with `STALE` when never stamped |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Access check before a read |
| GET | `/api/recovery/decision/v1/rule-models/{n}/{v}` | P7 rwb-decision | Package model and checksum |

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | Topic plus retry topic and `.dlt` topic; outbox relay |
| `rwb.case.CaseAllocated.v1`, `rwb.case.CaseAllocationFailed.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1`, `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | Same topic, same retry and `.dlt` path |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | Shared topic owned by the platform and rwb-decision; reused, not recreated |

#### 12.4 Events consumed

| Event | Topic | Consumer service | Owner | Provisioning |
|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | rwb-case | Not specified in the source documents (DOR-RWB-P3-E1018-OPS-24) | Consumer group for rwb-case with the inbox; retry and `.dlt` configured; record key `{sourceSystem}:{businessDate}`; data `sourceSystem`, `businessDate`, `status`, `completedAt`; only the event with `sourceSystem` ALS and `status` COMPLETED starts the run; events for other source systems start nothing |
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | rwb-case | Not specified in the source documents (DOR-RWB-P3-E1018-OPS-24) | Consumer group for rwb-case with the inbox; retry and `.dlt` configured |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case ID | `rwb-case` | Worker deployment with the build ID of the release |
| DailyCaseRun | Workflow started by AceDataReady (`sourceSystem` ALS, `status` COMPLETED) with a daily Schedule fallback; workflow ID form: Not specified in the source documents (CG-ALL-3483); duplicate-start policy: Not specified in the source documents (CG-ALL-3483) | `rwb-case` | Worker deployment plus the Schedule registration |
| allocate, transfer, rebalance | Activities | `rwb-case` | Registered by the same worker |
| EvaluateRules, RecordAndApply | Activities (workflow kit) | `rwb-case` | Registered by the same worker; mTLS to the Temporal frontend |

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| DailyCaseRun | Daily, with AceDataReady as the primary trigger; overlap policy SKIP; catch-up window | The release registers or updates the Schedule and fails if the namespace rejects it | JOB-02 Case creation |
| Allocation step | Daily by 07:00 inside DailyCaseRun | A step of DailyCaseRun, no separate Schedule | JOB-03 Morning allocation |

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| recovery_case, case_account, case_party, case_entry_exclusion | P3 (rwb_case) | Created by the per-service Flyway sequence in the migration job |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Created by the same migration job; used by the outbox relay and the consumer |

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-source-data WireMock | Runs in the pipeline and in the SIT smoke profile so the release can start without the other service. The freshness answers include stamps with `status` `LOADED` and `STALE`, and a never-stamped answer (`businessDate` null, `status` `STALE`) |
| rwb-access WireMock | Same |
| rwb-decision WireMock | Same, including the ENTRY and EXCLUSION models used by the smoke run |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed in the deployment path | Case reads; freshness, authorise and rule models; one hop, 2 s |
| Kafka | 7 published, 2 consumed | `rwb.case.events.v1` with retry and `.dlt`; DecisionRecorded reused; AceDataReady and RulePackageInForce consumed |
| Temporal | 2 workflows, 5 activities, 1 Schedule | CaseWorkflow, DailyCaseRun; allocate, transfer, rebalance, EvaluateRules, RecordAndApply |
| File | None | The release reads no file; values files are build inputs, not runtime data |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
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

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-case/` | Chart with deployment, service, migration job, config map, secret references, probes and the Schedule registration hook |
| `helm/rwb-case/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switches, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Topic `rwb.case.events.v1` with retry and `.dlt`, consumer groups, task queue `rwb-case` in namespace `rwb-recovery` |
| Schedule registration | DailyCaseRun with cadence, overlap policy SKIP and catch-up window; idempotent create or update |
| Dashboards | Run counts, run duration, event lag, decision-record lag, refused and out-of-scope reads |
| Alerts | Seven rules, each with a message ID and one runbook entry |
| Runbook | Six entries: batch gate, decision record failure, package not in force, number range exhausted, migration failure, probe failure |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running and the Temporal worker has polled; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database. Exact paths and timings are values (GAP-0677).

**Migration job.** Runs the per-service Flyway sequence for schema rwb_case with the rwb-case login, as a pre-deploy job with a backoff limit; a failed job blocks the rollout and the release.

**Alert mapping carried over from the legacy story.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P1-001 | DailyCaseRun waiting for a complete ALS batch | Batch gate alert with product and date fields | Platform on-call, ticket |
| MSG-P7-003 | Decision record write failed for an account | Failed-account alert with the count and the run ID | Platform on-call, page |
| MSG-P3-027 | No ENTRY or EXCLUSION version is in force | Package-in-force alert naming the package code | Business on-call (RW-COE), page |
| MSG-P3-025 | Yearly case number range used up | Number-range alert with the year and an incident | Platform administrator, incident |
| MSG-P4-002 | Read without Case record R | Refused-read count on the dashboard | No page |
| MSG-P4-003 | Case outside the reader's scope | Out-of-scope count on the dashboard | No page |

The WP line lists the number-range message as MVG-P3-025; the message ID in the legacy story and in the message catalogue is MSG-P3-025, which is the ID used above.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer, the topic and queue provisioning is verified by a test, the Schedule is registered and fires once per business date, the six alerts fire on synthetic metrics and the runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | DailyCaseRun waiting for a complete ALS batch | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-027 | No ENTRY or EXCLUSION version is in force on the business date | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P7-003 | Decision record write failed for an account | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-025 | Yearly case number range used up | Case numbers for {year} are used up. New cases are on hold until the range is extended. |
| MSG-P4-002 | Read without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

The texts of MSG-P1-001 and MSG-P3-027 are copied from Error and Message Standard v4 and the other texts are copied unchanged from the legacy story; the deployment adds the alert routing and the runbook link, never a new wording.

While v_ace_batch_status does not exist (RWB-ACE-001 not deployed), the batch gate answers as it does for an incomplete batch: it refuses with MSG-P1-001, returns no candidate and writes no break row. DP01 is never stamped LOADED for that date, so the case creation job creates no case for that date. The gate is read from the view only and is never inferred from data_as_of, a row count or a file. The refusal status is Not specified in the source documents (GAP-0571); the two filled fields of MSG-P1-001 are fixed by the Error and Message Standard v4. The behaviour is settled in ASM-B-P1-07-E1018-4.

### 15. Screens and states

The deployment serves the two screens of the capability: SCR-02 Case list (Loading; empty; list; filtered; error: Not specified in the source documents (CG-ALL-3488); no access: Not specified in the source documents (CG-ALL-3488)) and SCR-03 Case record (Loading; read only; empty: Not specified in the source documents (CG-ALL-3489); error: Not specified in the source documents (CG-ALL-3489); no access: Not specified in the source documents (CG-ALL-3489)), behind the gateway-bff composite route (DP-19). The operator-facing surfaces of this story are the pipeline run view, the release view, the dashboard and the runbook. The composite route specification and the screen field list are Not specified in the source documents (GAP-0674; ASM-1221); the deployment only registers the route target and the health check of the case endpoints.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1018-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with pinned digest, the rwb-case login reference and the migration job |
| TC-P3-E1018-OPS-02 | AC2 | NFR | One pipeline run produces one image and one chart version and fails on a contract drift or a critical scan finding |
| TC-P3-E1018-OPS-03 | AC3 | NFR | Readiness is false before the migration and start-up window, then true; liveness stays true; neither probe writes |
| TC-P3-E1018-OPS-04 | AC4, AC5 | NFR | Topic with retry and `.dlt`, task queue registered, DailyCaseRun registered and fired once for one business date |
| TC-P3-E1018-OPS-05 | AC6 | NFR | Six synthetic conditions raise the six mapped alerts with the legacy text and one runbook entry each |
| TC-P3-E1018-OPS-06 | Section 12 operations, events and activities | Contract | Each operation, event type and activity named in section 12 matches its contract version v1 |
| TC-P3-E1018-OPS-07 | Section 12.7 tables (ASM-3438) | Boundary | Boundary values for each table listed in section 12.7 |
| TC-P3-E1018-OPS-11 | AC7 | Boundary | Each rule BR1 to BR8 checked against the chart, migration, topics, Schedule, alerts and read paths |
| TC-P3-E1018-OPS-09 | AC8 | Component | A consumed call that fails and a call that does not answer: event is not acknowledged, goes to retry then .dlt, and readiness reports not ready |
| TC-P3-E1018-OPS-12 | AC9 | Integration | A smoke run publishes rwb.case.CaseCreated.v1 on rwb.case.events.v1 and DecisionRecorded on rwb.decision-record.v1 into the P7 ledger; the ALS batch is seeded through the W1J01 harness and the run is cleaned up with the P7 administrative rollback |

### 17. Guardrails

- No business value in a values file: the entry threshold, the exclusion reasons, the bands and the status list are parameters and reference data, never a deployment value.
- No personal data in logs, dashboard series, alert payloads or the runbook: run counts, IDs and durations only.
- One login per service; the chart carries the rwb-case login reference and no other service's credential (DP-02).
- The service writes only schema rwb_case; the migration job never touches another schema (DP-01).
- Every topic has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due | DailyCaseRun registration, run counts dashboard | TC-P3-E1018-OPS-04, TC-P3-E1018-OPS-05 |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, never reused | MSG-P3-025 alert and the sequence state on the dashboard | TC-P3-E1018-OPS-05 |
| REQ-CWC-003 | One case per customer and product | Run counts created, linked and failed | TC-P3-E1018-OPS-04 |
| REQ-CWC-004 | Exclusion rules as data | MSG-P3-027 alert and the package-in-force runbook entry | TC-P3-E1018-OPS-05 |
| REQ-CWC-005 | State model with one state at a time | Migration job and schema version check in readiness | TC-P3-E1018-OPS-01, TC-P3-E1018-OPS-03 |
| REQ-CWC-016 | Every workflow event logged with rule ID and version | Decision-record lag panel and MSG-P7-003 alert | TC-P3-E1018-OPS-05 |
| REQ-CHO-004 | One agreed hand-over point in days past due for every rule and report | MSG-P1-001 batch-gate alert with the business date | TC-P3-E1018-OPS-05 |
| ADR-023 | Observability per service | Dashboard, six alerts and the runbook | TC-P3-E1018-OPS-05 |

### 19. Out of scope

- The application code of case creation, grouping, numbering and rule evaluation (RWB-P3-E1018-APP).
- The contract documents and the fakes as published artefacts (RWB-P3-E1018-CON); this story only deploys the test copies.
- The platform topic provisioning implementation and the Temporal cluster (platform epics RWB-PLT-EVT and RWB-PLT-WF).
- The exact cluster topology, node pools, replica counts and probe timings (GAP-0677).
- The case screens and the composite route specification (platform edge story and RWB-P3-E1023-APP).
- The rwb_case schema design and the logical model (database stories of the service epic).
- Data migration from the legacy schema and the reconciliation run (Epic 2 and rwb-source-data).
