# RWB-P6-E1055-OPS Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1055-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-055 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P6-G |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-013, FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-018, FR-P6-019, FR-P6-020, FR-P6-021, FR-P6-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-055 for rwb-comms (OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the proof-of-delivery loop of rwb-comms deployed from the service template with its chart, its values files and its own login, the Temporal worker deployment that polls `rwb-comms` for `NoticeDispatchWorkflow`, the 16:00 Schedule registered against the workflow kit with the JOB-10 Airflow file-window handoff, the JOB-11 outbox relay, the dashboards and alerts for a missing proof-of-delivery batch and a failed file, a runbook for a re-run of the dispatch and of the pod read, a smoke profile against the four contract fakes, and the feature flags with their rollback**, so that **an operator can see within minutes that a notice will not be dispatched or that a delivery will not land, and repair it inside the business day without reading code or waiting for a business report**.

This story deploys an existing capability. It adds no topic, builds no endpoint, table or workflow and writes no notice: the run is `NoticeDispatchWorkflow` on queue `rwb-comms`, the file moves through rwb-integration, the pod is rwb-source-data's and the timer is rwb-case's.

### 2. Business rationale

The legacy capability leaned on a Quartz job whose only failure signal was a job exception, so a file that was never delivered and a pod batch that was never ingested looked the same as a quiet night. In the target the run is a workflow with a Schedule (DP-10), the cross-system edge is the bank Airflow file window (Architecture v5 slide 44, JOB-10 "Airflow file window + workers"), and the delivery facts arrive as events (DP-09). There is no scheduler row to be late and no job record to inspect, so the operational signal has to move from "did the job run" to "is the file of the day delivered, is the pod of the date COMPLETE, is the outbox moving, and is the workflow stuck".

Two properties of this loop make deployment part of the capability. First, its failure is silent for the officer: a notice stays Generated and looks like a notice that nobody dispatched, so the missing-file and missing-batch alerts have to be built here or nobody will raise them. Second, its clock is legal: a delivered notice starts the notice period (R-LIT-07), so a pod batch that is one business day late delays a legal clock, and the freshness signal with MSG-P1-001 is a control rather than a report.

Deployment is otherwise the standard shape: the chart carries the rwb-comms login and no other credential (DP-02), the migration job runs the per-service Flyway sequence in schema `rwb_comms` (DP-15), the consumer groups of the three consumed events are provisioned with retry and `.dlt` paths (DP-09), the outbox relay runs every minute (JOB-11), and the runbook names the four failures an operator will actually see.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON), so the worker polls `rwb-comms` and the Schedule runs in every environment.
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and `rwb.comms.events.v1`, `rwb.case.events.v1` and `rwb.deviation.events.v1` are provisioned by their owners.
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across REST, Kafka, Temporal and the file step.
- The three environments DEV, SIT and UAT exist with their parameter scope and their Kafka, Temporal and object-store endpoints.
- RWB-P6-E1055-CON is published, so the smoke profile runs against the two operations and the four fakes of that baseline.
- RWB-P6-E1055-INF has provisioned the egress path, the identities, the key-store entries, the staging area, the file store and the worker sizing.
- The dispatch Schedule expression and the deployment slot of the service are Not specified in the source documents (GAP-1103; ASM-2051), and the alert values are Not specified in the source documents (GAP-1104; ASM-2052).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-comms with the rwb-comms login, the pre-deploy migration job for schema `rwb_comms`, the readiness and liveness probes, the api deployment and the worker deployment that polls `rwb-comms`.
3. The Schedule registration step registers the 16:00 dispatch Schedule against the workflow kit, with overlap SKIP and the catch-up window of the kit, and asserts that `NoticeDispatchWorkflow` is what it starts.
4. The same step records the JOB-10 handoff: the bank Airflow file window opens the edge for the business date and the in-service Schedule starts the workflow, with no Quartz row, no shared job table entry and no Control-M job anywhere in the release.
5. The provisioning step declares the consumer group `rwb-comms` for `rwb.case.events.v1` and `rwb.deviation.events.v1`, each with its retry topic and its `.dlt` topic, and reuses `rwb.comms.events.v1` and `rwb.decision-record.v1` as their owners provision them.
6. The outbox relay is deployed as the platform standard of JOB-11: every minute, one relay per service, with its lag and its dead-letter count exposed.
7. The dashboards are published: the file of the business date by state, the age of the newest delivered file, the pod batch state of the date, the dispatch and delivery counts, the outbox lag, the workflow open, stuck and failed count, the refusal rate and the SFTP handshake result.
8. The alerts are wired to MSG-P1-001, MSG-GEN-006, MSG-P6-004 and MSG-P4-002 where the condition maps to one, and each alert links exactly one runbook entry.
9. A smoke step runs the loop against the four fakes in SIT: one file for 2026-11-25, one acknowledgment, one Sent notice, one pod batch, one Delivered notice and one unacknowledged run that raises the task.
10. The runbook is published and reviewed with the on-call rota: a missing proof-of-delivery batch, a failed file, a dispatch run that must be re-run, a stuck workflow and an outbox relay that stopped.
11. The feature flags are set per environment and the rollback path is rehearsed once in UAT.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | The worker is deployed with the wrong build ID | The Schedule starts a workflow no worker serves; the stuck-workflow alert fires and the release is rolled back | None | AC1, AC7 |
| X3 | The Schedule is registered twice, or with overlap ALLOW | The registration check fails the release; the duplicate is removed before promotion | None | AC2 |
| X4 | The file of the business date is not delivered by the reviewed time | The missing-file alert fires with MSG-GEN-006 and the failed-file runbook entry opens | MSG-GEN-006 | AC4, AC5 |
| X5 | The pod batch of the date is not COMPLETE | The freshness alert fires with MSG-P1-001 and the missing-batch runbook entry opens | MSG-P1-001 | AC4, AC5 |
| X6 | The outbox relay stops or its lag passes its value | The relay alert fires and the relay runbook entry restarts the relay and replays the topic | None | AC3, AC4 |
| X7 | A workflow stops on a non-retryable failure | The stuck workflow scan of JOB-21 raises the case and the stuck-workflow runbook entry starts from the history | None | AC4, AC5 |
| X8 | A role without the Litigation right is refused | The refusal is counted on the dashboard and no page is sent | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the Schedule registration, the topic provisioning and the observability stack; builds no application code |
| Negotiable | Replica counts, resource sizes, alert thresholds, the Schedule slot and the retention are environment values, not story decisions |
| Valuable | Makes a loop with no job record observable: the file, the batch, the relay and the workflow each have a signal, an owner and a runbook entry |
| Estimable | One chart, one Schedule registration, one provisioning step, one relay, eight panels, six alerts, five runbook entries and one smoke profile |
| Small | Fits one sprint with the runbook and the smoke profile |
| Testable | Every criterion tests an artefact: the chart renders, the Schedule exists once, an alert fires on a synthetic metric, a runbook entry resolves, the smoke profile passes |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the proof-of-delivery loop of rwb-comms

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart deploys rwb-comms with the worker that polls rwb-comms (new, D-RCV-60)
    Given the rwb-comms Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-comms login reference and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_comms before the deployment is marked ready
    Then the worker deployment polls task queue rwb-comms in namespace rwb-recovery with the build ID of the release, and the api deployment serves the notice read
    Then readiness answers healthy only when the migration is at the expected version, the outbox relay is running and the worker has polled
    Then no replica count, resource size, timeout, threshold or cadence is hard-coded in the template

  Scenario: AC2 The 16:00 Schedule runs once and the JOB-10 window handoff is recorded (new, D-RCV-60)
    Given the Schedule registration step of the release
    When it runs against the environment
    Then exactly one Schedule starts NoticeDispatchWorkflow at 16:00 Asia/Bangkok with overlap SKIP and the catch-up window of the workflow kit
    Then the step records the JOB-10 handoff: the bank Airflow file window opens the edge for the business date and the in-service Schedule starts the workflow
    Then no Quartz row, no shared job table entry and no Control-M job is registered for this capability
    Then a release that registers a second Schedule or an overlap of ALLOW fails the registration check
    Then the deployment slot and the namespace assignment are Not specified in the source documents (GAP-1103; ASM-2051)

  Scenario: AC3 The outbox relay of JOB-11 is deployed and measured (new, D-RCV-60)
    Given the deployed outbox relay of the service
    When the relay runs for a metric window
    Then it runs every minute, takes the rows of schema rwb_comms and publishes the two events on rwb.comms.events.v1 and the decision record on rwb.decision-record.v1
    Then its lag, its published count and its dead-letter count are exposed as series
    Then the consumer group rwb-comms subscribes to rwb.case.events.v1 and rwb.deviation.events.v1 with retry and .dlt topics and never acknowledges an event it could not process
    Then no topic is created by this release and no event is published outside the owner's topic

  Scenario: AC4 The dashboards and alerts cover a missing batch and a failed file (new, D-RCV-60)
    Given the published dashboard and the six alert rules
    When a synthetic day is replayed with a delivered file, a missing file, a COMPLETE batch, a FAILED batch, a late batch, a stuck workflow and a refused read
    Then the panels show the file of the business date by state, the age of the newest delivered file, the pod batch state of the date, the dispatch and delivery counts, the outbox lag, the workflow open, stuck and failed count and the refusal rate
    Then a missing file raises its alert with MSG-GEN-006 and a late or failed batch raises its alert with MSG-P1-001, each naming the environment, the business date and the interface
    Then a refused read is counted and never pages the on-call rota
    Then no panel or alert payload carries a name, an address, an identity number or a contact value
    Then the alert thresholds and the reviewed time of the late batch are Not specified in the source documents (GAP-1104; ASM-2052)

  Scenario: AC5 The runbook covers a missing batch, a failed file and a re-run (new, D-RCV-60)
    Given the published runbook and the five alert conditions
    When an operator opens the entry a fired alert links
    Then the runbook holds one entry each for a missing proof-of-delivery batch, a failed file, a dispatch run that must be re-run, a stuck workflow and an outbox relay that stopped
    Then the re-run entry states how the dispatch of a business date is started again without writing a notice into a second file and without re-sending an acknowledged notice
    Then the re-run entry states how the pod read of a business date is repeated with no notice changing state a second time
    Then every entry names its check, the owner role, the recovery step and the escalation path when the step fails
    Then every alert links exactly one entry

  Scenario: AC6 The smoke profile proves the loop against the four fakes (new, D-RCV-60)
    Given the SIT smoke profile of this release
    When it runs in the pipeline and on demand in SIT
    Then it opens the dispatch run of 2026-11-25 against the WIN file fake and asserts one file, one outbound item and one Sent notice on the notice read
    Then it asserts the Sent notice carries sent date 2026-11-26 and barcode "RR123456789TH", and that one NoticeDispatched is seen on the topic
    Then it replays the pod batch of 2026-11-30 against the pod fake and asserts one Delivered notice with callback date 2026-11-28 and one NoticeDelivered
    Then it replays the unacknowledged run and asserts the notice stays Generated and the task with MSG-GEN-006 is raised
    Then it replays the late batch and asserts the stale marker with MSG-P1-001 naming "DP07 Legal" and 2026-11-23
    Then the profile fails the release when any assertion fails, and it touches no production data and no real WIN connection

  Scenario: AC7 The feature flags are set per environment and the rollback is rehearsed (new, D-RCV-60)
    Given the flags rwb.comms.win-dispatch-v1 and the dispatch Schedule state per environment
    When the flag is off in an environment
    Then no notice is written to a file and the pod read changes no notice, while the notice read still answers
    Then the flag and the Schedule state are values-file entries, never code, and are recorded per environment
    Then a rollback to the previous chart version restores the previous flag state and leaves the delivered files and the notices unchanged
    Then the rollback is rehearsed once in UAT and the rehearsal is recorded in the runbook
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-comms login and no other service's credential | DP-02; Architecture v5 slide 29 |
| BR2 | The migration is a per-service Flyway sequence in schema `rwb_comms` and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON |
| BR3 | Every subscription has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Architecture v5 slide 22 notes |
| BR4 | The outbox relay runs every minute and is the platform standard of JOB-11; it is not rebuilt per story | Architecture v5 slide 44; DP-09 |
| BR5 | JOB-10 is the bank Airflow file window plus the dispatch Schedule and workers of this service; no Quartz row and no Control-M job is registered | DP-10; Architecture v5 slide 44 |
| BR6 | No environment value is hard-coded: replica counts, resource sizes, timeouts, thresholds and the Schedule state come from values files | Template and Rules §R7.2 s17 |
| BR7 | An alert carries a message ID and the agreed text, and links exactly one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | A refused read is counted and never pages the on-call rota | MSG-P4-002 |
| BR9 | A re-run of a business date never writes a notice into a second file and never re-sends an acknowledged notice | legacy AC8; DP-10 |
| BR10 | No dashboard series, log line or alert payload carries personal data; notice IDs, case IDs, the barcode, counts and durations only | Template and Rules §R7.2 s17 |
| R-LIT-07 | The delivery date starts the notice period, so a missing pod batch delays a legal clock and is an alert, not a report | Temporal and Drools design slide 20 notes |
| R-UNI-33 | A failed delivery is retried and the notice does not advance until the retry succeeds; the retry interval is a values entry | INT-14 error handling |
| R-UNI-34 | A delivery that passes its retry limit leaves the file in the exception path with its reason, and the operator sees it on the file-age and file-state panels | INT-14 error handling |
| R-UNI-40 | A repeated event or a repeated pod row produces one effect, and the repeat is counted; the re-run entry is written so it cannot break this | legacy BR6 |

### 9. State transitions

The release and the Schedule move through these states; no business object moves.

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version, the relay runs and the worker polls `rwb-comms` | Ready |
| Ready | Schedule registered | Exactly one Schedule exists and the window handoff is recorded | Armed |
| Armed | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is the new one | Armed |
| Armed | Alert on a missing file, a missing batch or a stuck workflow | The condition passes its value | Alerted; the runbook entry opens |
| Alerted | Re-run of the business date, or the owner's repair | The file or the batch is delivered and the notice state is what the run wrote | Armed |
| Armed | Rollback | The previous chart version and the previous flag state are restored | Armed on the previous version |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the Schedule registration, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning, the visibility queries behind JOB-21 and the re-run of a job on SCR-44 |
| ACE database administrator | Owns schema `rwb_comms`, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments and the rollback |
| On-call operator | Runs the runbook entries and opens an incident when a missing batch or a failed file persists |
| RW-PLATADM, platform administrator | Reruns the dispatch run from SCR-44 and reads the REC-05 break on SCR-45 in the running service, not in the cluster |
| Service owners of rwb-integration, rwb-source-data and rwb-case | Are paged by the file, batch and workflow alerts and own the repair beyond the rwb-comms breaker |

The per-service login used by the chart is a secret reference resolved at deploy time; the chart references "the rwb-comms login (DP-02)" and never a literal name. The deployment slot and the namespace assignment of the service are Not specified in the source documents (GAP-1103; ASM-2051).

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, the flag `rwb.comms.win-dispatch-v1`, the Schedule state, the two client timeouts, the alert thresholds |
| Schema | `rwb_comms`, migrated by the per-service Flyway sequence; the tables `notice`, `template` and `merge_field` with the library objects |
| Topics | `rwb.comms.events.v1` carries the two events with retry and `.dlt`; `rwb.case.events.v1` and `rwb.deviation.events.v1` are consumed with retry and `.dlt`; `rwb.decision-record.v1` is reused as its owner provisions it |
| Queue | Temporal task queue `rwb-comms` in namespace `rwb-recovery`, and the `rwb-integration` queue of the `deliverFile` activity |
| Schedule | One dispatch Schedule at 16:00 Asia/Bangkok, overlap SKIP, with the catch-up window of the kit |
| Dashboard series | File of the date by state, age of the newest delivered file, pod batch state of the date, dispatch count, delivery count, outbox lag, workflow open, stuck and failed, refusal rate, SFTP handshake result |
| Runbook entries | Missing batch, failed file, dispatch re-run, stuck workflow, outbox relay stopped |
| Secrets | The rwb-comms login secret, the SFTP client certificate reference, the Kafka client credential and the Temporal mTLS material, all from the platform key store |

The alert thresholds and the reviewed time of the late batch are deployment values; their provisional values are carried by the gap and the assumption of section 14 (GAP-1104; ASM-2052). The exact cluster topology, node pools, replica counts and probe timings are deployment values of the platform chart and are not fixed here.

### 12. Contract

#### 12.1 REST operations provided

None. The deployment exposes the operations of RWB-P6-E1055-CON behind gateway-bff: `GET /api/recovery/comms/v1/notices/{noticeId}` and the internal digest write. The probes are cluster-internal and are not part of the API surface, and this story adds no path.

#### 12.2 REST operations consumed

None. The deployment configures the client timeouts and the breakers of the consumed rows declared in RWB-P6-E1055-CON and adds no call of its own.

#### 12.3 Events published

None. The two events are RWB-P6-E1055-APP's; the deployment reuses `rwb.comms.events.v1` with its retry and `.dlt` topics as provisioned by its owner and creates no topic.

#### 12.4 Events consumed

None declared. The consumer groups of the three consumed events are provisioned in the step of section 13 and described in AC3, and their shapes belong to RWB-P6-E1055-CON.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `NoticeDispatchWorkflow` | Workflow, one per business date and dispatch run | `rwb-comms` | Worker deployment with the build ID of the release; holds the dispatch run, the acknowledgment wait and the two events |
| `generateLetter` | Activity, P6 | `rwb-comms` | Registered by the same worker |
| `approveNotice` | Child workflow in rwb-decision | `rwb-decision` | Reached through the platform namespace; no worker of this release serves it |
| `deliverFile` | Activity, P2 | `rwb-integration` | Served by the rwb-integration worker; the deployment asserts the queue exists and is served |

#### 12.6 Schedules

| Schedule | Cron | Overlap | Handoff |
|---|---|---|---|
| The dispatch Schedule of rwb-comms (RWB-PLT-E1071-CON) | 16:00 Asia/Bangkok, daily | SKIP, with the catch-up window of the kit | The bank Airflow file window opens the WIN edge for the business date (JOB-10); the Schedule starts `NoticeDispatchWorkflow`, which requests the file through rwb-integration |

Exactly one Schedule is registered per environment, and no Quartz row, shared job table entry or Control-M job is created. The deployment slot and the namespace assignment are Not specified in the source documents (GAP-1103; ASM-2051).

#### 12.7 Tables owned

None. The migration job creates and migrates the tables of RWB-P6-E1052-APP and RWB-P6-E1046-APP in schema `rwb_comms` and the dispatch columns of RWB-P6-E1055-APP; this story owns no table and adds no column. `document`, `interaction`, `recovery_case`, `timer` and `outbound_item` belong to their services and the migration job touches schema `rwb_comms` only (DP-01).

#### 12.8 Contract fakes

None. The fakes are test-only workloads of RWB-P6-E1055-CON; the SIT smoke profile of AC6 runs against them and they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | No operation is provided or consumed by the deployment itself |
| Kafka | None | No topic is created; the two events and the three consumed events ride their owners' topics with retry and `.dlt` |
| Temporal | 1 workflow, 1 Schedule | `NoticeDispatchWorkflow` on `rwb-comms`, with the `generateLetter` activity registered by the same worker and the 16:00 Schedule registered once per environment |
| File | 1 dotted grey path | The INT-14 file of the business date through rwb-integration to the WIN edge, and the INT-15 proof file back through ACE and rwb-source-data; the smoke profile asserts the outbound path against the fake |

### 13. Solution plan

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-comms/` | Chart with api and worker deployments, service, migration job, config map, secret references, probes and the Schedule registration hook |
| `helm/rwb-comms/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, `rwb.comms.win-dispatch-v1`, the Schedule state, the two client timeouts, the alert thresholds |
| Pipeline stage | Build, unit, component and contract tests, the retired-element check, image and dependency scan, chart publish, one artefact promoted through the environments |
| Schedule registration step | Exactly one dispatch Schedule, its cron, its overlap and its catch-up, plus the recorded JOB-10 window handoff |
| Provisioning step | Consumer group `rwb-comms` on `rwb.case.events.v1` and `rwb.deviation.events.v1` with retry and `.dlt`; reuse of `rwb.comms.events.v1` and `rwb.decision-record.v1`; task queue `rwb-comms` in namespace `rwb-recovery` |
| Outbox relay | The platform standard of JOB-11, one relay per service, with lag and dead-letter series |
| Dashboards | Eight panels: file by state, file age, batch state, dispatch count, delivery count, outbox lag, workflow health, refusal rate |
| Alerts | Six rules, each with a message ID where one maps, and one runbook entry |
| Runbook | Five entries: missing batch, failed file, dispatch re-run, stuck workflow, outbox relay stopped |
| Smoke profile | The SIT run of AC6 against the four fakes |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H rows are delivered by the platform waves and are not repeated in the metadata H field, which stays empty. DP-10 is the pattern this story serves: the Schedule registration and the worker deployment are the operational form of "no shared Quartz". DP-05 and DP-18 add no work here.

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running and the Temporal worker on `rwb-comms` has polled; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database and neither calls another service.

**Alert mapping.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-GEN-006 | The file of the business date is not delivered by the reviewed time, or the SFTP handshake fails | Missing-file alert with the interface, the business date and the attempt count | Platform on-call, page; ticket to the rwb-integration owner |
| MSG-P1-001 | The pod batch of the date is not COMPLETE by the reviewed time, or is FAILED at its record count check | Missing-batch or failed-batch alert with the product, the business date and the last load date | Platform on-call, page; ticket to the rwb-source-data owner |
| MSG-P6-004 | The dispatch count of the date is zero inside the window while notices are eligible | Dispatch-count alert with the eligible count and the workflow state | Platform on-call, page |
| MSG-P4-002 | A read without the Litigation right is refused | Refusal count on the dashboard | No page |
| None | The outbox lag passes its value, or the dead-letter count rises | Relay alert with the lag and the oldest row | Platform on-call, page |
| None | The stuck workflow scan of JOB-21 raises a `rwb-comms` workflow | Stuck-workflow alert with the workflow ID, the business date and the last event | Platform on-call, page |

Every alert carries its message ID where the condition maps to one, and the two conditions without one carry the series or the workflow name instead. The thresholds and the reviewed time are deployment values with provisional defaults; the missing source is carried by the gap and the assumption of section 14 (GAP-1104; ASM-2052).

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact and fails on a fake drift, exactly one Schedule exists in each environment, the consumer groups exist with their retry and `.dlt` paths, the eight panels carry the synthetic day, the six alert conditions fire on synthetic metrics, the five runbook entries are reviewed by the on-call rota and the smoke profile of AC6 passes in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-004 | A notice is acknowledged by WIN | {notice} was sent for registered mail on {date}. |
| MSG-GEN-006 | WIN has not acknowledged after the third attempt, or the file of the date is not delivered | {system} is not available. Your request is queued and will be retried. |
| MSG-P1-001 | The WIN batch is late or not COMPLETE | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A read without the Litigation right | You cannot {action} here. Your role does not include it. |

The message texts are the legacy wording of RWB-E1-055, copied unchanged, and the deployment adds the routing, the threshold and the runbook link, never a new wording. The alert values and the reviewed time of the late batch are Not specified in the source documents (GAP-1104; ASM-2052).

### 15. Screens and states

The deployment serves SCR-44 Interface and job monitor and SCR-45 Data quality for this capability behind the gateway-bff composite route (DP-19): SCR-44 shows the dispatch run and the pod read in the states Running; failed; complete, with the file ID and the attempt count, and SCR-45 shows the held row with check `References` and the REC-05 break in state breaks. The operator-facing surfaces of this story are the pipeline run view, the release view, the Schedule view, the eight panels and the runbook; the smoke step opens the notice of a synthetic case in SIT and asserts that the dispatch and proof fields answer inside the 2 s budget.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-055-01 | AC1, BR1 | End to end | N-0001 Generated; acknowledgment with RR123456789TH |
| TC-E1-055-02 | AC2, BR2 | End to end | v_ace_pod row for 2026-11-30 with RR123456789TH, callback_date 2026-11-28 |
| TC-E1-055-03 | AC3 | End to end | WIN owner sample WIN-POD-SAMPLE-v1, 25 records ingested by ACE |
| TC-E1-055-04 | AC4, BR3 | End to end | No acknowledgment on three runs |
| TC-E1-055-05 | AC5, BR4 | End to end | ACE batch for WIN FAILED at its record count |
| TC-E1-055-06 | AC6, BR4 | End to end | 30 rows, 1 unknown |
| TC-E1-055-07 | AC7 | End to end | v_ace_pod rows of 2026-11-30 read twice |
| TC-E1-055-08 | AC8 | End to end | JOB-10 rerun on 2026-11-25 |
| TC-E1-055-09 | AC9, BR5 | End to end | N-0002 with no barcode on 2026-11-28 |
| TC-E1-055-10 | AC10, BR6 | End to end | Repeat of RR123456789TH on 2026-12-07 |
| TC-E1-055-11 | AC11, BR7 | End to end | No COMPLETE WIN batch for 2026-11-30 |
| TC-E1-055-12 | Access | Component | RW-PHONECOL reads the notice dispatch detail; refused with MSG-P4-002 |

The twelve are the legacy test cases of RWB-E1-055 in their legacy order, with the Level column added; System maps to End to end and Access to Component. The deployment checks of AC1 to AC7 and the smoke profile of AC6 carry their own identifiers, because they test an environment and not a business case.

### 17. Guardrails

- No business value in a values file: the eligible state, the attempt limit, the break days, the stale period and the list values stay reference data held by their owner, never a deployment value.
- No personal data in logs, dashboard series, alert payloads or the runbook: notice IDs, case IDs, the barcode, counts, durations and file IDs only.
- One login per service; the chart carries the rwb-comms login reference and no other service's credential (DP-02).
- The service writes only schema `rwb_comms`; the migration job never touches another schema and no dashboard query reads one (DP-01).
- Every subscription has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- No new topic and no Quartz row: the capability reuses its owner's topics and the run is a Temporal Schedule with the Airflow window as the edge (DP-10, DP-14).
- ACE data is read only through the owner's contract; no dashboard reads an ACE view or another service's schema (DP-05).
- The release pins the image digest and the chart version, and no secret is written into a values file, a chart template, a dashboard or the runbook.
- A refused read is not an incident: it is counted and it never pages the on-call rota (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | The worker deployment, the 16:00 Schedule with the JOB-10 handoff, the file and batch panels and the two runbook entries | TC-E1-055-01, TC-E1-055-09 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | The outbox relay and the retry and `.dlt` paths of the consumed groups | TC-E1-055-02 |
| REQ-DRI-006 | No direct call to a system of record; files move only through rwb-integration | The `deliverFile` queue assertion and the file panels | TC-E1-055-03, TC-E1-055-04 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | Exactly one dispatch Schedule, one worker deployment and no Quartz row | TC-E1-055-08, TC-E1-055-10 |
| ADR-023 | Observability per service | Eight panels, six alert conditions and five runbook entries | TC-E1-055-05, TC-E1-055-11 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E1-055 | The runtime of the dispatch and proof-of-delivery loop of the legacy story |
| DP-01 | The migration touches `rwb_comms` only and no panel reads another schema |
| DP-05 | No dashboard reads an ACE view; the pod arrives through rwb-source-data |
| DP-07 | The list values stay reference data, not a deployment value |
| DP-09 | The relay and the three consumer groups with retry, `.dlt` and inbox dedupe |
| DP-10 | The 16:00 Schedule and the worker deployment, with the Airflow window as the edge |
| DP-11 | The client timeouts and breakers of the consumed rows, configured, not built |
| DP-15 | The migration job runs the per-service Flyway sequence in `rwb_comms` |
| DP-18, DP-19 | The ledger is rwb-source-data's and the two screens are the composite route's |
| ADR-013, ADR-014, ADR-015, ADR-021 | 19 services, a schema and login per service, Kafka with outbox and inbox, and per-service migration |
| ADR-020, ADR-023 | One hop and 2 s in the deployed path; observability per service |

### 19. Out of scope

- The workflow, the notice read, the acknowledgment handler and the pod read (RWB-P6-E1055-APP).
- The contract baseline and the fakes as published artefacts (RWB-P6-E1055-CON); this story runs the test copies.
- The egress path, the identities, the key-store entries, the staging area, the file store and the worker sizing (RWB-P6-E1055-INF).
- The legacy criteria AC1 and AC9 and the end-to-end proof on the real services (RWB-ITG-E1055-ITG).
- The file transport, the outbound item and the retry of a failed delivery (rwb-integration, RWB-P2-E1007-CON).
- The pod read, the freshness stamp and the ledger (rwb-source-data, RWB-P1-E1066-CON).
- The notice generation and the template catalog (RWB-P6-E1052-APP, RWB-P6-E1046-APP).
- The WIN acknowledgment loop of Epic 2 and the SMS and LINE dispatch (RWB-P6-E2021-APP, RWB-P6-E2022-APP).
- The platform products behind this release: the Temporal cluster, the Kafka platform, the observability stack and the stuck workflow scan of JOB-21 (RWB-PLT-WF, RWB-PLT-EVT, RWB-PLT-OBS).
- The `rwb_comms` schema design, its tables and its migrations (the database stories of the service epic).
- The deployment slot, the namespace assignment, the alert thresholds and the reviewed time of the late batch, which are reviewed values and Not specified in the source documents (GAP-1103; GAP-1104).
