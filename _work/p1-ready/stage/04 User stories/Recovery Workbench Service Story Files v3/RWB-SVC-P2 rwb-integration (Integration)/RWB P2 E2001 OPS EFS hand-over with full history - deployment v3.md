# RWB-P2-E2001-OPS EFS hand-over with full history

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-066, RD-P1-067; Test Cases v9 mappings.

- Decision-record event type name corrected to `rwb.decision.DecisionRecorded.v1`; topic `rwb.decision-record.v1` unchanged (RD-P1-008).
- `AceDataReady` consumption aligned: record key per source system and business date, daily work starts only on `sourceSystem` ALS with `status` COMPLETED (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-P2-E2001-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP18, DP19 |
| Parallel lane | L-P2-E |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P2-E2001-OPS-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2001-CON (build status Not started); product group map of rwb-case (DP-07), contract ID Not specified in the source documents (GAP-0593) |
| Contract version | 5.0.0 (Recovery Workbench API Specification v5: rwb-integration.yaml; asyncapi/rwb-source-data.asyncapi.yaml for the consumed `AceDataReady`) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-019) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-008, RD-P1-040, RD-P1-066, RD-P1-067 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-001 for rwb-integration. The legacy story's Quartz job, its run summary and its late-batch alert sat inside one deployable; this story deploys the hand-over step as an event-started worker on the queue `rwb-integration`, subscribes it to `AceDataReady`, publishes the six run series and the held-run and failed-run alerts, and writes the runbook the on-call operator uses. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 34 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **Platform administrator**, I want **the rwb-integration hand-over worker deployed on the task queue `rwb-integration` in the namespace `rwb-recovery` with one subscription on `rwb.source-data.events.v1`, the step and its activities registered, the `rwb_integration` migration applied, six run series on a dashboard, one alert for a held run and one for a failed run, and the runbook entries behind them**, so that **an operator can see a morning that did not create its cases — held, partial or refused — name the business date and the count, and act on it without reading code**.

### 2. Business rationale

The legacy story assumed a Quartz job inside one module: the trigger, the run summary and the database were in one process, so a missed morning showed up as a job row and the operator had the database in front of them. In the target the step is a deployment of its own. It starts from an event on another service's topic, it writes its summary as an activity result and a decision record, its writes go to three other services, and its only busy moment is the morning window when ACE publishes `AceDataReady` (Arch v5 slide 33). Without this story the app story can pass its tests while the consumer group is unassigned, a morning event is consumed and starts nothing, a held run is never alerted, and the business measure — that the cases appear the morning after day 90 — falls with no signal.

Deployment is also where the split is enforced operationally. The release carries the rwb-integration login only, subscribes to `rwb.source-data.events.v1` only, applies the `rwb_integration` migration only, and never touches `rwb_source_data`, `rwb_case`, `rwb_decision` or an ACE view (DP-01, DP-02, DP-05, DP-18). The observability follows ADR-023 per service: six series, two alerts, four runbook entries, each alert carrying a message id and one runbook entry.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The rwb-integration baseline chart and login are deployed by RWB-P2-E1007-APP, with the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1` and the `rwb_integration` schema (DP-02, DP-13).
- The Temporal workflow kit and the `rwb-recovery` namespace exist, with worker versioning, the build ID provider and the payload codec (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provides `rwb.source-data.events.v1` with its retry and `.dlt` topics and the ACL of this service's principal (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- rwb-source-data publishes `AceDataReady` (EV-26) for the ALS source on that topic (RWB-P1-E1015-APP; Arch v5 slide 43 row 26).
- The platform error envelope and the message catalogue are in force, so an alert can carry a message id.
- The three environments DEV, SIT and UAT exist and the production namespace exists for the release date; the flag `rwb.integration.efs-handover` exists in the flag library.
- The gateway-bff composite routes for SCR-02, SCR-04 and SCR-45 are published (RWB-PLT-N001-CON, DP-19).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the API deployment and the hand-over worker with the rwb-integration login, the namespace `rwb-recovery`, the task queue `rwb-integration`, the payload codec and the build ID of the release.
3. The subscription step creates the hand-over consumer group on `rwb.source-data.events.v1`, with the offset reset policy, the maximum poll, the `.dlt` routing and the starting offsets, and records them.
4. The registration step confirms that `EfsHandoverWorkflow` and its nine activities are registered on the queue and that the workflow ID pattern is `efs-handover-<businessDate>`.
5. The migration step applies the `rwb_integration` sequence of this release and refuses to run when the target schema is not `rwb_integration`.
6. The flag step sets `rwb.integration.efs-handover` from the values of the environment.
7. The Schedule check confirms that this release registers no Schedule and no Quartz trigger, and that JOB-02 and JOB-03 remain rwb-case's.
8. The dashboards are published with the six series and the environment, release and build ID as dimensions.
9. The two alerts are wired to their message ids and one runbook entry each: MSG-P2-007 for a held run and MSG-P7-003 for a failed run; the lag alert and the no-start alert carry the identifier placeholder of GAP-0653 until the Error and Message Standard names them.
10. A smoke step publishes one synthetic `AceDataReady` for ALS, `status` COMPLETED, and a synthetic business date in DEV, follows it to one run against the P1, P3 and P7 fakes, then produces one held run and one refused second start, and checks that both alerts and the six series moved.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready and the pipeline stops; no traffic and no offset is committed | None | AC1 |
| X2 | The consumer group is assigned no partition, or lags past its threshold | The lag series rises and the lag alert fires; the runbook entry names the check | Not specified in the source documents (GAP-0653; ASM-1097) | AC2, AC5 |
| X3 | `AceDataReady` is consumed and no `EfsHandoverWorkflow` starts | The no-start check fails the smoke run and the alert fires; the runbook entry names the event id and the business date | Not specified in the source documents (GAP-0653; ASM-1097) | AC2, AC6 |
| X4 | The run holds because DP01 is incomplete | The held series rises, the held alert fires with the waiting count, and the runbook entry names the data steward route | MSG-P1-001, MSG-P2-007 | AC3 |
| X5 | The run ends `PARTIAL` or fails on its own decision record | The failed-run alert fires with the failing group count and the record class, and the runbook entry names the retry and the incident route | MSG-P7-003 | AC4, AC6 |
| X6 | A second start is requested while the run lock is held | The rerun is refused with 409 and the refusal is counted on the dashboard; nothing changes | MSG-P2-006 | AC6 |
| X7 | The flag is off in an environment | The worker is not deployed, the group holds no member, and no run starts | None | AC1 |
| X8 | A dashboard series is missing, or an alert carries no message id or no runbook link | The observability check fails the release | None | AC5, AC6 |
| X9 | A new build is promoted while a run is open | The open run replays on the new build from its history; the dashboards show both build IDs | None | AC1, AC5 |

The DP05-late smoke check verifies the 409 history read retries every five minutes through the 09:00 interim cut-off, the hand-over completes without history at the cut-off, and the late rows append once when DP05 arrives (RD-P1-067; GAP-3286).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the topic provisioning and the flag library; no application code is built here |
| Negotiable | Replica counts, resource sizes, lag thresholds, alert thresholds and scan intervals are environment values |
| Valuable | Makes the morning run observable and actionable before the release date, and proves that no morning is silently lost |
| Estimable | One chart, one subscription, one registration step, one migration step, six series, two alerts and four runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the group holds offsets, an alert fires on a synthetic metric, a workflow starts, the runbook is reviewed |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the EFS hand-over step for rwb-integration

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-integration is rwb-integration
    Given the target environment is SIT

  Scenario: AC1 The worker and the login are deployed from one chart with the migration (new, D-RCV-60)
    Given the rwb-integration chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the hand-over worker polls only the task queue rwb-integration in the namespace rwb-recovery
    Then the release declares the rwb-integration login and no other service's credential
    Then the migration step applies the rwb_integration sequence of this release and refuses a target schema other than rwb_integration
    Then the release registers no Schedule and no Quartz trigger for the step
    Then worker versioning is enabled and a new workflow goes to the new build while the old build drains

  Scenario: AC2 The AceDataReady subscription and the step registration are fixed (new, D-RCV-60)
    Given the release of this story and the topic rwb.source-data.events.v1
    When the subscription step and the registration step run
    Then the hand-over group is a member of rwb.source-data.events.v1 and of no other topic
    Then the assignment records its offset reset policy, its maximum poll and its retry and .dlt routing
    Then EfsHandoverWorkflow and its nine activities are registered on the queue rwb-integration with the workflow ID pattern efs-handover-<businessDate>
    Then one synthetic AceDataReady for ALS with status COMPLETED starts one run and a duplicate of the same key starts none
    Then a topic outside the one, and a workflow name outside the nine activities, are refused by the release

  Scenario: AC3 The held-run alert names the stale date and the waiting count (new, D-RCV-60)
    Given the published alert rules and a run that finds DP01 stale at business date 2026-12-15
    When the run ends as HELD
    Then the held-run alert fires with MSG-P1-001, MSG-P2-007, the stale data product, the business date and the waiting count
    Then the alert payload carries no account holder, no contact point and no amount
    Then the held series on the dashboard rises for the same business date and names the gap date in the next good run

  Scenario: AC4 The failed-run alert fires for a partial run and for a failed record (new, D-RCV-60)
    Given a run in which one group fails on the case-creation decision record and the run ends PARTIAL
    When the run closes
    Then the failed-run alert fires with MSG-P7-003, the failing group count and the record class
    Then the incident route names the business date and the account keys of the failed groups, and nothing else
    Then a run whose own decision record cannot be written ends as failed with no DecisionRecorded and raises the same alert

  Scenario: AC5 The six run series carry the environment, the release and the build ID (new, D-RCV-60)
    Given the published dashboard of the deployment
    When a good run, a held run and a partial run are produced on synthetic data
    Then the dashboard shows accounts read, cases created, accounts linked, repeats, held and gap dates
    Then each series carries the environment, the release and the build ID as dimensions
    Then a held run and a partial run are both visible on the dashboard before any alert is read

  Scenario: AC6 The runbook and the alerts cover the operational failures (new, D-RCV-60)
    Given the published runbook and the alert rules
    When a lagging group, a held run, a failed run and a refused second start are simulated
    Then each condition raises its alert, carrying MSG-P2-007 or MSG-P7-003 where those messages apply and the identifier placeholder of GAP-0653 for the lag and the no-start alert
    Then every alert links one runbook entry with the check, the owner role and the recovery step
    Then the runbook names the rwb-source-data rerun operation, the 409 refusal of a second concurrent run and the fact that no run is deleted
    Then no alert threshold and no interval is hard-coded, and no secret appears in a values file, a dashboard or the runbook

  Scenario: AC7 The release holds the deployment business rules (new, D-RCV-60)
    Given the release of this story, its dashboards, its alerts and its runbook
    When the release checks and the smoke run are executed
    Then the release carries the rwb-integration login, polls rwb-integration only and migrates rwb_integration only
    Then it subscribes to rwb.source-data.events.v1 only, with one group, the inbox, the retry topic and the .dlt topic, and to no topic of this service
    Then the step is started by AceDataReady and owns no Schedule, and JOB-02 and JOB-03 stay rwb-case's
    Then every worker carries the build ID of its release with worker versioning enabled, and a new build takes new workflows while the old build drains
    Then every alert carries a message id and the agreed text, or the identifier placeholder of GAP-0653 where none is named, and links one runbook entry
    Then replicas, resources, lag thresholds, alert thresholds, intervals and the flag come from values files and parameters
    Then dashboard series, alert payloads and the runbook carry no account holder, no contact point and no amount
    Then the release writes no case, account, interaction or reconciliation row and reads no table of another service
    Then a build that fails its tests or its smoke run is not promoted and the previous build stays in force
    Then a held run is alerted, named by business date and counted
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One login, one task queue and one schema per service: the release carries the rwb-integration login, polls `rwb-integration` only and migrates `rwb_integration` only | Arch v5 slide 41; DP-02; DP-15 |
| BR2 | The deployment subscribes to `rwb.source-data.events.v1` only, with one group, the inbox, the retry topic and the `.dlt` topic, and to no topic of this service | Arch v5 slide 43 row 26; DP-09; DP-14 |
| BR3 | The step is started by `AceDataReady` and owns no Schedule; JOB-02 and JOB-03 stay rwb-case's | Arch v5 slide 44; DP-10 |
| BR4 | Every worker carries the build ID of its release and worker versioning is enabled, so a new build takes new workflows while the old build drains | Temporal and Drools design slide 11; RWB-PLT-E1071-CON |
| BR5 | Every alert carries a message id and the agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR6 | No environment value is hard-coded: replicas, resources, lag thresholds, alert thresholds, intervals and the flag come from values files and parameters | Template and Rules §R7.2 s17 |
| BR7 | Dashboard series, alert payloads and the runbook carry counts, business dates, data product codes, message ids and build IDs only, never an account holder, a contact point or an amount | Temporal and Drools design slide 11 (PDPA); ADR-023 |
| BR8 | The release writes no case, account, interaction or reconciliation row and reads no table of another service; the step's calls go to the owners' contracts | DP-01; DP-05; DP-18 |
| BR9 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run | DP-10 |
| BR10 | The held run is the operational signal of BR4 of the app story: a morning that could not be built is alerted, named by business date and counted, never absorbed | Legacy MSG-P2-007 and CTL-02 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Worker registered and probes healthy | The worker polls `rwb-integration` only and the group holds an assignment | Ready |
| Ready | Release superseded | A new chart version passes its tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open runs | Ready |
| Ready | Flag off | `rwb.integration.efs-handover` is turned off in the environment | Not deployed |
| Ready | Smoke run failed | The start, the summary or the alert step of the smoke run fails | Blocked |
| Blocked | Previous build restored | The smoke run passes on a later build, or the previous chart is redeployed | Ready |

The run states `COMPLETED`, `HELD` and `PARTIAL` and the refusal of a second start are the app story's runtime and are not states of this deployment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the subscription step, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic ACLs, the consumer quotas, the flag library and the administrative rerun of JOB-02 |
| Platform event owner | Owns `rwb.source-data.events.v1`, its retry and `.dlt` topics, the schema registry and the `.dlt` retention |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the four runbook entries and opens an incident when a held or failed run persists |
| RW-DATASTEW, data steward | Receives the held-run alert and reads the run summary (Platform administration, R) |
| RW-AUDIT | Reads the alert history, the run series and the runbook record |

The worker runs as the rwb-integration service identity (DP-02), carried by the chart as a secret reference and never as a literal name. The login name is Not specified in the source documents (GAP-0653; ASM-1087).

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, feature switch | BR6 |
| Task queue | `rwb-integration` in the namespace `rwb-recovery`, polled by the rwb-integration worker only | BR1 |
| Consumer group | One hand-over group on `rwb.source-data.events.v1`, with the offset reset policy, the maximum poll, the retry topic and the `.dlt` topic | BR2 |
| Topic | `rwb.source-data.events.v1` consumed; `rwb.decision-record.v1` published by the local library; `rwb.integration.events.v1` untouched by this slice | BR2 |
| Schema | `rwb_integration`, migrated by its own per-service Flyway sequence; this release applies the hand-over library migration | BR1 |
| Dashboard series | Accounts read, cases created, accounts linked, repeats, held runs, gap dates; dimensions environment, release, build ID, business date | BR7 |
| Runbook entries | Lagging group, missing run after a consumed event, held run, failed or partial run; each with the check, the owner role and the recovery step | BR5 |
| Alerts | Two rules with a message id — MSG-P2-007 for a held run and MSG-P7-003 for a failed run — and two with the identifier placeholder of GAP-0653: lag and no-start | BR5, BR10 |
| Secrets | The rwb-integration login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store | BR6 |
| Test data | One synthetic `AceDataReady` for ALS and one synthetic business date, one held run and one refused second start; the fixture owner is Not specified in the source documents (GAP-0653; ASM-1097) | BR10 |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded.

**Probes.** Readiness answers healthy only after the worker has polled `rwb-integration` once, the consumer group holds an assignment and the workflow and its activities are registered. Liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database or commits an offset, and a failing dependency is reported as not ready, never as live-and-broken. The paths and timings are values of the environment.

### 12. Contract

#### 12.1 REST operations provided

None from this story. The hand-over step provides no REST operation (RWB-P2-E2001-CON §12.1); this deployment exposes the integration base's existing operations through the chart and its ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None from the deployment. The worker calls the P1, P3 and P4 contracts at run time as the app story's clients; the chart carries no REST client of its own, no composite route and no outbound call at start-up beyond the Temporal frontend and the Kafka brokers.

#### 12.3 Events published

None of its own. `rwb.integration.events.v1` carries `FileDelivered` and `FileFailed` from the outbound-file side and this slice publishes neither; `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library through the relay when the run record commits (DP-03, DP-09).

#### 12.4 Events consumed

The service shares consumer group rwb-integration.rwb.source-data.events.v1 and one listener across its source-data event workflows, including JOB-08. It has READ on the main topic, READ and WRITE on retry topics and WRITE on the dead-letter topic (RD-P1-066).

| Event type | Topic | Deployment element | Owner | Service |
|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | The hand-over group, with the inbox, the retry topic and the `.dlt` routing; starts `EfsHandoverWorkflow` for the ALS source and the business date, on only the event with `sourceSystem` ALS and `status` COMPLETED (record key `{sourceSystem}:{businessDate}`) | Platform event epic (topic); rwb-source-data (type) | rwb-integration |

The topic, its retry and `.dlt` topics and the type are provisioned and owned by the platform event epic and by rwb-source-data's contract; this deployment configures the one group, the inbox, the offset policy and the relay that turns a message into a workflow start.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| EfsHandoverWorkflow | Workflow, one execution per business date, workflow ID `efs-handover-<businessDate>` | `rwb-integration` | Registered by the worker of this release, with the build ID and worker versioning |
| acceptAceDataReady, readFreshness, listCandidates, buildGroups | Activities | `rwb-integration` | Registered with the kit's retry policy of 1 s, back-off 2, 3 attempts |
| createOrLinkCase, appendEfsHistory, writeRunSummary, recordRunDecision, releaseRunLock | Activities | `rwb-integration` | Registered with the same policy; idempotent on the run and per-account keys |
| AceDataReadyListener and the run lock | Event consumer and lock | not a worker | Deployed in the same release; starts the workflow once per key and holds `handover-run:<businessDate>` |

**Build ID and versioning.** The build ID is the one supplied by the workflow kit for the release commit; worker versioning is enabled and a new build takes new runs while the old build drains. The build ID format and the versioning policy are Not specified in the source documents (GAP-0653; ASM-1097).

#### 12.6 Schedules

None. The deployment registers no Schedule and no Quartz trigger: the step is event-started from `AceDataReady` (BR3). JOB-02 case creation and JOB-03 allocation are rwb-case's Schedules and steps and are neither created nor read here. The relay and the retry scan of the outbox library run on the platform intervals of DP-09 and are not Schedules of this service.

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| processed_event | PLT library, created in `rwb_integration` | The inbox of `AceDataReady`; read and written by the listener |
| idempotency_key | PLT library, created in `rwb_integration` | The run lock and the per-account keys |
| decision_record | PLT library, created in `rwb_integration` | The run record, published by the library |
| outbox_event, outbox_delivery | PLT library, created in `rwb_integration` | The outbox row and its delivery on `rwb.decision-record.v1` |

The release applies the hand-over library migration of the app story and no other: no table of rwb-source-data, rwb-case or rwb-decision is created, altered or read, and `interface_config`, `outbound_item` and `job_catalog` are untouched (DP-01, DP-05, DP-15, DP-18).

#### 12.8 Contract fakes

None. No fake is deployed. The workflow tests run on the platform's test environment in the pipeline and the contract mocks of the P1, P3 and P4 contracts are in-process test doubles of the app story. The smoke run of DEV calls the fakes of the service environment, never a fake shipped by this release.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The step's calls are the app story's; the probes are cluster-internal |
| Kafka | 0 published, 1 type consumed through 1 group | `rwb.source-data.events.v1` with the hand-over group, retry and `.dlt` |
| Temporal | 1 workflow, 9 activities, 0 Schedules | Worker on `rwb-integration` with a pinned build ID and worker versioning |
| File | None | No file is read or written by the deployment |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_integration` only and reads no other schema | none |
| DP-03 | DecisionLogWriter, decision log | The local record library is deployed with the relay and publishes to `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read in this release; the candidates and the EFS rows come through the P1 contract at run time | none |
| DP-06 | Parameters, casewf.config | The rwb-case parameters contract is a run-time dependency of the worker, with its client library | H RWB-PLT-E1042-CON |
| DP-07 | Reference data, LOV | The rwb-case reference-data contract is a run-time dependency of the worker | H RWB-PLT-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The one consumer group with the inbox, the retry topic and the `.dlt` topic; the relay on its platform interval | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue and the namespace come from the workflow kit; no Schedule is registered | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The release declares no REST path and no client of its own; the worker calls the contracts as the app story's client | none |
| DP-18 | Interaction ledger | No ledger object is deployed, migrated or read; the append goes to rwb-source-data | none |
| DP-19 | Screen, ace-web | gateway-bff serves SCR-02, SCR-04 and SCR-45; the deployment registers no screen of its own | H RWB-PLT-N001-CON |

The platform H dependencies those patterns add are the platform contracts the release consumes; they are not repeated in the metadata H column, which stays None because an OPS story builds nothing.

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-integration/` overlay | API deployment, hand-over worker, listener, outbox relay, config map, secret references, probes, task queue, namespace, build ID and flag |
| `helm/rwb-integration/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, build ID, consumer group name, lag and alert thresholds (ASM-1097) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration step, smoke run, promotion |
| Subscription step | The one hand-over group on `rwb.source-data.events.v1`, with the offset reset policy, the maximum poll, the retry and `.dlt` routing and the starting offsets |
| Registration step | `EfsHandoverWorkflow` and its nine activities on `rwb-integration`, with the workflow ID pattern and the build ID |
| Migration step | The `rwb_integration` migration of this release; a target schema other than `rwb_integration` is refused |
| Schedule check | Confirms that no Schedule and no Quartz trigger is registered and that JOB-02 and JOB-03 remain rwb-case's |
| Dashboards | The six series of section 11 with the four dimensions |
| Alerts | Four rules — held, failed, lag, no-start — each with a message id or the placeholder and one runbook entry |
| Runbook | Four entries: lagging group, missing run after a consumed event, held run, failed or partial run |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P2-007 | A run ends `HELD` for a stale DP01 | Held-run alert naming the data product, the business date, the waiting account count and the build ID, with MSG-P1-001 for the data product | Data steward and platform on-call, ticket in the morning window |
| MSG-P7-003 | A run ends `PARTIAL`, or fails on its own decision record | Failed-run alert naming the business date, the failing group count and the record class | Platform on-call, page |
| Not specified in the source documents (GAP-0653; ASM-1097) | Lag of the hand-over group is past its threshold | Lag alert naming the group, the topic, the partition and the lag | Platform on-call, page in the morning window, else ticket |
| Not specified in the source documents (GAP-0653; ASM-1097) | `AceDataReady` was consumed and no `EfsHandoverWorkflow` started | No-start alert naming the event id, the business date and the group | Platform on-call and the business on-call, page |

**Retry and offsets.** Offsets are committed after the inbox row is marked, so a crash replays the intake and the inbox makes the replay harmless. The retry of a failed activity is the workflow kit's, and a final failure ends the run as `PARTIAL` with the failing group named; nothing is deleted and no run is replayed by hand except through the rwb-source-data rerun operation, which is refused while the run lock is held (BR5 of the app story, MSG-P2-006). The interval values and the lag thresholds are environment values (ASM-1097).

**Rollback.** A release that fails the smoke run is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open runs until they finish; the consumed events are replayed from the topic and the inbox makes the replay harmless. No data repair is needed, because the step writes no case, account, interaction or reconciliation row of its own.

**Feature switch.** `rwb.integration.efs-handover`. On: the worker and the group are deployed and the step runs. Off: no worker and no group member, and no run starts (ASM-1098).

**Done when.** The chart renders for DEV, SIT and UAT with a pinned digest and the build ID, the group holds its assignment and reports offsets, the migration step refuses a foreign schema, the smoke run starts one run from one synthetic event and produces one held run and one refused second start, the six series and the four alerts are published with their message ids or placeholders and their runbook links, and the four runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product is stale at the business date of the run | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-007 | A run is held for an incomplete or stale batch | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-P7-003 | A run ends partial, or fails on its own decision record | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | A second start or rerun while the run lock is held | {job} is already running. Wait for it to finish before you run it again. |
| Identifier pending | Lag of the group is past its threshold | Not specified in the source documents (GAP-0653; ASM-1097) |
| Identifier pending | `AceDataReady` was consumed and no run started | Not specified in the source documents (GAP-0653; ASM-1097) |

MSG-P1-001 uses the wording of Error and Message Standard v4. The lag alert and the no-start alert have no message identifier in the source set at all, so their identifier and text are carried as the placeholder until the Error and Message Standard names both. An alert payload names counts, data product codes, business dates, event ids, group names and the build ID only.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard, SCR-45 Data quality through gateway-bff and the runbook. SCR-02, SCR-04 and SCR-45 are served by the app stories of rwb-case, rwb-source-data and this key and by the composite route of RWB-PLT-N001-CON; the deployment registers no screen and only carries the route. The states of SCR-02 are empty and loading, taken from Screen Specifications v1; its error and no access states are Not specified in the source documents (CG-ALL-3060). The states of SCR-04 are loading, taken from Screen Specifications v1; its empty, error and no access states are Not specified in the source documents (CG-ALL-3061). The states of SCR-45 are loading, taken from Screen Specifications v1; its empty, error and no access states are Not specified in the source documents (CG-ALL-3062). The Temporal Web UI stays behind Entra ID: RW-PLATADM operates and RW-AUDIT reads, and payloads are decoded only through the codec server under break-glass.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2001-OPS-01 | AC1, BR1, BR3, BR4 | NFR | The chart renders for three environments with a pinned digest, the build ID, worker versioning and the rwb-integration login reference; a foreign migration target is refused; no Schedule is registered |
| TC-P2-E2001-OPS-02 | AC2, BR2, BR3 | NFR | One group assigned on `rwb.source-data.events.v1`; a second topic refused; the workflow and its nine activities registered; one event starts one run and a duplicate starts none |
| TC-P2-E2001-OPS-03 | AC3, BR7, BR10 | NFR | One synthetic run with DP01 stale at 2026-12-15: HELD, the held alert with MSG-P1-001 and MSG-P2-007, the waiting count, and no personal value in the payload |
| TC-P2-E2001-OPS-04 | AC4, BR5 | NFR | One run PARTIAL on a record failure and one run failing on its own record: MSG-P7-003, the failing group count and the incident route |
| TC-P2-E2001-OPS-05 | AC5 | NFR | The six series carry the four dimensions; a good, a held and a partial run are visible before the alerts |
| TC-P2-E2001-OPS-06 | AC6, BR5, BR6, BR7 | NFR | Four synthetic conditions raise the four mapped alerts, each with one runbook entry; the runbook names the rerun route, the 409 refusal and no deletion; no hard-coded threshold and no secret |
| TC-P2-E2001-OPS-07 | §12 | Contract | The AceDataReady.v1 consumption, the nine activities and the operations of §12 match RWB-P2-E2001-CON; a payload or operation outside the contract fails the build |
| TC-P2-E2001-OPS-08 | §12.7, BR8 | Boundary | A write or read of any table outside processed_event, idempotency_key, decision_record, outbox_event and outbox_delivery is refused; interface_config, outbound_item and job_catalog are untouched |
| TC-P2-E2001-OPS-09 | BR9 | NFR | A build that fails its tests or its smoke run is not promoted; the previous build keeps the workflows in force |
| TC-P2-E2001-OPS-10 | AC7, BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 | NFR | Release checks and the smoke run on one synthetic AceDataReady for ALS: one login, queue, schema and group; no Schedule; build ID and versioning; alerts with runbook links; no hard-coded value or personal value; no foreign write; a failing build not promoted; a held run alerted and counted |

### 17. Guardrails

- No business value in a values file: the threshold, the hold time, the product map and the action codes are rows of their owners, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the runbook or the workflow history: counts, business dates, business keys, codes, event ids and build IDs only, and payloads stay encrypted.
- One login per service, one task queue per service and one schema per service: the release carries the rwb-integration login, polls `rwb-integration` and migrates `rwb_integration` only (DP-02, DP-15).
- The release deploys no case, account, interaction or reconciliation object and reads no table of another service (DP-01, DP-05, DP-18).
- The one consumer group subscribes to `rwb.source-data.events.v1` only and has a retry topic and a `.dlt` topic before it starts (DP-09).
- No run is ever deleted: a held, partial or refused run is a record, and a re-run goes through the rwb-source-data operation and the run lock (BR10).
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing smoke run never replaces a working build.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the daily ALS batch and is read through the ACE data path | The one group on `rwb.source-data.events.v1` and the step registration | TC-P2-E2001-OPS-02 |
| REQ-CHO-001 | Case with full contact and promise history | The six series and the run summary the dashboard reads | TC-P2-E2001-OPS-05 |
| REQ-CHO-005 | Workbench is the system of record for case state after hand-over | The failed-run alert and the runbook entry that names the owner route | TC-P2-E2001-OPS-04, TC-P2-E2001-OPS-06 |
| REQ-RDF-003 | EFS history transfers to the case | The held-run alert and the gap-date series that show a morning that did not build | TC-P2-E2001-OPS-03, TC-P2-E2001-OPS-05 |
| ADR-016 | Event-started workflows replace Quartz; no shared job table | The worker, the queue and the absence of any Schedule or Quartz trigger | TC-P2-E2001-OPS-01, TC-P2-E2001-OPS-02, TC-P2-E2001-OPS-07 |
| ADR-023 | Observability per service | The six series, the four alerts and the four runbook entries | TC-P2-E2001-OPS-05, TC-P2-E2001-OPS-06 |
| DP-01 | No table of another service is created, altered or read | The table set of §12.7 and the refused writes | TC-P2-E2001-OPS-08 |
| DP-10 | A failing release never replaces a working one | The release gate and the previous build kept in force | TC-P2-E2001-OPS-09 |

### 19. Out of scope

- The listener, the workflow, the activities, the group builder, the clients, the summary writer and the migration as code (RWB-P2-E2001-APP).
- The contract documents, the summary shape, the keys, the error classes and the fakes (RWB-P2-E2001-CON); this story only deploys and gates them.
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The topic provisioning, the schema registry and the `.dlt` retention (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The case creation, the account link and `CaseCreated` (RWB-P3-E2001-APP); the EFS append and the REC-01 row (RWB-P1-E2001-APP); the central ledger (RWB-P7-E2001-APP).
- JOB-02 `DailyCaseRun`, JOB-03 allocation and their Schedules (rwb-case).
- The administrative rerun operation and its role data (rwb-source-data and rwb-access).
- The screen fields and states of SCR-02, SCR-04 and SCR-45 (the rwb-case, rwb-source-data and P2 app stories, and the gateway-bff route of RWB-PLT-N001-CON).
- The outbound-file windows, the WIN and debt-buyer files and the outbound-item exception queue (RWB-P2-E1007-APP and RWB-P2-E1007-OPS).
- The real cross-service proof of the held, partial and repeated run against the live owners (RWB-ITG-E2001-ITG).
- The exact cluster topology, node pools, replica counts, lag thresholds and probe timings; they are set per environment by the platform team.
