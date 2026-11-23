# RWB-P6-E2021-OPS Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2021-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P6-O |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-010, FR-P6-013, FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-018, FR-P6-019, FR-P6-020, FR-P6-021, FR-P6-022, FR-P6-027, FR-P6-028, FR-P6-029, FR-P6-030, FR-P6-031, FR-P6-036) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-021 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the dispatch loop of rwb-comms deployed from the service template with its Helm values, its own login, its per-service Flyway migration and a worker on task queue `rwb-comms` in namespace `rwb-recovery`, the 16:00 Temporal Schedule and its handoff from the Airflow WIN file window, the outbox relay and the three consumer groups with their retry and `.dlt` paths, the dashboards for a file that is missing and a proof window that has expired, the alerts for a missing file, an unacknowledged file and a proof window expiry, and a runbook for a re-run of JOB-10**, so that **an operator sees within minutes that tonight's letters were not written to WIN, or that the proof never came back, and repairs the run by business date without reading code and without writing a second file for the same date**.

### 2. Business rationale

The legacy capability had one signal and it was a job exception: the 16:00 run either threw or it did not, and a file the bank never received looked exactly like a quiet night (legacy sections 5 and 13). In the target the run is a Temporal Schedule and a workflow, the file is written by rwb-integration, the acknowledgement and the proof results come back through integration, and the notice facts live in `rwb_comms` (Architecture v5 slides 17, 41, 44; DP-10). There is no scheduler row to be late and no job record to inspect, so the operational question moves from "did the job run" to "was the file written, was it acknowledged, did the proof arrive inside the window, and is the decision record chain moving".

The capability is also the one whose failure is silent by design: a held notice, an unserved notice and a notice waiting for proof are all correct outcomes of a correct run, so an operator cannot tell a good night from a bad one by the notice count. That is why the dispatch file, the acknowledgement and the proof window are three dashboard series and three alerts here, each with a message ID of section 14 and one runbook entry, and why the rerun is defined by business date with the skip rule that the legacy story states: a rerun from SCR-44 skips the notices already Unserved or Held and the notices already in a file of that date.

Deployment is part of the capability for the same reason: the chart carries the rwb-comms login and no other credential (DP-02), the migration job runs the per-service Flyway sequence in `rwb_comms` (DP-15, ADR-021), the worker polls `rwb-comms` in namespace `rwb-recovery` and polls nothing else, the Schedule is the only clock of the service, and the three consumer groups exist with retry and `.dlt` so a contact stop that arrives while the run is open is never lost (DP-09).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON), so the worker polls `rwb-comms` and the Schedule runs in every environment.
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and `rwb.comms.events.v1`, `rwb.deviation.events.v1` and `rwb.case.events.v1` are provisioned by their owners.
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across REST, Kafka and Temporal.
- The three environments DEV, SIT and UAT exist with their parameter scope and their Kafka and Temporal endpoints.
- RWB-P6-E2021-CON is published, so the smoke profile and the drift test run against the two operations, the file contract and the six fakes of that baseline.
- The bank Airflow owns the WIN file window for JOB-10 (Architecture v5 slide 44 notes) and its handoff to this Schedule is agreed. The mechanism of the handoff is Not specified in the source documents (GAP-1095; ASM-2043).
- The WIN file drop and the rwb-integration file run are owned by P2 and by the WIN owner; this story deploys nothing of theirs and reads their answers.
- The worker placement, the replica counts and the deployment slots are Not specified in the source documents (GAP-1093; ASM-2041), and the deployment slot decision DL35 is open in the P6 TSD.
- The owner of the daily reconciliation REC-05 that the legacy story names is not stated in the sources (GAP-1090; ASM-2038).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-comms with the rwb-comms login, the pre-deploy migration job for schema `rwb_comms`, the readiness and liveness probes, the api deployment and the worker deployment that polls `rwb-comms`.
3. The provisioning step declares the Schedule of 16:00, the three consumer groups of the capability on `rwb.deviation.events.v1` and `rwb.case.events.v1`, and the outbox relay subscription of the service; it creates no topic and no queue of another service.
4. The provisioning step asserts that no Quartz table, no shared job table and no batch table is read or written, and that the only clock of the service is the one Schedule.
5. The dashboards are published: dispatch files written by business date, notices in a file, acknowledgements received, notices without an acknowledgement, notices held by reason, notices unserved by result, proof window expiries, notices waiting for proof, decision record write failures and workflow health.
6. The alerts are wired to the message IDs of section 14 and to the runbook entries of section 13; the thresholds are values and carry the placeholder of section 11 until they are confirmed.
7. A smoke step runs a synthetic business date in the SIT profile against the six fakes of RWB-P6-E2021-CON: the request, the run, the file, the acknowledgement and one proof result, so the loop is exercised end to end before WIN and the neighbouring services are live.
8. The runbook is published and reviewed with the on-call rota: a missing dispatch file, an unacknowledged file, a proof window that expired without proof, a held notice that should have gone out, a stopped decision record chain and a re-run of JOB-10 by business date.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | The worker is deployed without the `rwb-comms` queue, or on another queue | The readiness probe stays unready and the release fails its own check | None | AC1 |
| X3 | The Schedule is missing, or a second clock is registered | The provisioning check fails the release and the runbook entry for a missing file opens | None | AC2 |
| X4 | The dispatch file is not written for the business date | The missing-file alert fires and the runbook entry for a missing file starts with the file window and the integration run | MSG-P6-004 | AC5, AC6 |
| X5 | The acknowledgement never returns | The unacknowledged-file alert fires; the notices stay Sent-less and the rerun writes no second file for the date | MSG-P6-004 | AC5, AC6 |
| X6 | The proof window expires with no proof for a share of notices | The proof-window alert fires; the notices become Unserved under R-LIT-08 and the runbook entry names the WIN owner | MSG-P6-008 | AC5, AC6 |
| X7 | A consumer group is provisioned without its retry or `.dlt` topic | The provisioning step fails the release and the consumer refuses to start | None | AC4 |
| X8 | The decision record chain stops during a run | The run fails its step, the notices do not proceed and the incident rule of R-UNI-39 applies | MSG-P7-003 | AC4, AC6 |
| X9 | A release declares a new topic, a Quartz row or a second Schedule | The pipeline fails the release on the retired-element check | None | AC2, AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the observability stack; builds no application code |
| Negotiable | Replica counts, resource sizes, alert thresholds, retention and the deployment slots are environment values, not story decisions |
| Valuable | Makes a capability with no scheduler row observable: the file, the acknowledgement and the proof window each have a signal, an alert and an owner |
| Estimable | One chart, one pipeline stage, one migration job, two deployments, one Schedule, three consumer groups, ten dashboard series, six alert rules and six runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the Schedule exists, the groups exist, the panels carry data, the alerts fire on a synthetic metric, the runbook entry resolves |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the letter dispatch loop with proof of delivery

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart deploys the service and a worker on rwb-comms (new, D-RCV-60)
    Given the rwb-comms Helm chart and its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-comms login reference and no other service's credential
    Then the migration job runs the per-service Flyway sequence in schema rwb_comms before the deployment is marked ready
    Then the worker deployment polls task queue rwb-comms in namespace rwb-recovery with the build ID of the release, and polls no other queue
    Then the api deployment serves the two operations of RWB-P6-E2021-CON with the readiness and liveness probes
    Then no replica count, resource size, timeout, threshold or slot is hard-coded in the template, and the deployment slot follows the open decision DL35 with the value Not specified in the source documents (GAP-1093; ASM-2041)

  Scenario: AC2 The 16:00 Schedule is the only clock of the service (new, D-RCV-60)
    Given the provisioning step of rwb-comms
    When it runs against the environment
    Then one Temporal Schedule is registered for the JOB-10 run at 16:00 on business days with overlap policy SKIP and the catch-up window of the workflow kit
    Then the Schedule starts NoticeDispatchWorkflow on task queue rwb-comms with the business date as its only input
    Then no Quartz row, no shared job table and no batch table is read or written by the release, and no second Schedule exists for this service
    Then the outbox relay of the platform runs every minute and is not registered as a Schedule of this service
    Then a release that declares a second clock fails the retired-element check

  Scenario: AC3 The Airflow WIN file window hands off to the run by business date (new, D-RCV-60)
    Given the bank Airflow WIN file window for JOB-10 and the Schedule of this service
    When the window opens for business date 2026-12-14
    Then the handoff triggers the run for that business date and the workflow records the business date in its input
    Then a run for a business date already dispatched writes no second file for that date
    Then the handoff mechanism is exercised through the mechanism recorded in the baseline, and its form is Not specified in the source documents (GAP-1095; ASM-2043)
    Then the reconciliation REC-05 that the legacy story names is not registered here, because no source assigns its owner (GAP-1090; ASM-2038)

  Scenario: AC4 The consumer groups and the outbox relay are provisioned (new, D-RCV-60)
    Given the provisioning step of rwb-comms for the consumed events
    When it compares the groups with the topics
    Then consumer group rwb-comms subscribes to rwb.deviation.events.v1 for DeviationRaised and DeviationCleared with the inbox of schema rwb_comms
    Then consumer group rwb-comms subscribes to rwb.case.events.v1 for CaseStateChanged with the same inbox
    Then each subscription has its retry topic and its .dlt topic and the consumer never acknowledges an event it could not process
    Then NoticeDispatched and NoticeDelivered are produced on the existing rwb.comms.events.v1 with its retry and .dlt topics, and DecisionRecorded is produced on the shared rwb.decision-record.v1 as its owner provisions it
    Then the outbox relay publishes the outbox rows of the service every minute and a stopped chain raises the decision-record alert
    Then the provisioning step fails the release when a retry or .dlt topic is missing

  Scenario: AC5 The dashboards carry the dispatch, acknowledgement and proof series (new, D-RCV-60)
    Given the published dashboard of the capability
    When a synthetic day is replayed with one file written, one file missing, one acknowledgement returned, two notices without an acknowledgement, four notices held by the four reasons, three notices unserved by result and two proof windows expired
    Then the panels show files written by business date, notices in a file, acknowledgements received, notices without an acknowledgement, notices held by reason, notices unserved by result, proof window expiries and notices waiting for proof
    Then the panels show decision record write failures and the workflow open and stuck counts
    Then every panel names its service, its environment and its business date
    Then no panel carries a customer name, an address, an account number or an identity number, only notice IDs, case IDs, barcodes, counts and durations

  Scenario: AC6 The three operator alerts fire with a message ID and one runbook entry (new, D-RCV-60)
    Given the six alert rules and the published runbook
    When the dispatch file is missing for a business date, the acknowledgement does not return inside its value and the proof window expires for a share of notices
    Then each condition raises its alert with its message ID, its environment and its links to the business date, the workflow and the file reference
    Then the missing-file alert carries MSG-P6-004 and pages the on-call rota
    Then the unacknowledged-file alert carries MSG-P6-004 and pages the on-call rota after its second window
    Then the proof-window alert carries MSG-P6-008 and routes to the ticket queue with the WIN owner named
    Then a held notice that should have gone out and a stopped decision record chain raise their alerts, and every alert links exactly one runbook entry

  Scenario: AC7 The runbook reruns JOB-10 by business date without a second file (new, D-RCV-60)
    Given the published runbook entry for a re-run of JOB-10
    When the operator reruns the business date from SCR-44 after a missing file or an unacknowledged file
    Then the rerun starts the workflow for that business date and skips the notices already Unserved or Held and the notices already in a file of that date
    Then the entry names the check, the owner role, the recovery step and the escalation path when the step fails
    Then the rerun is idempotent on the notice ID and the business date, as the legacy story states
    Then the entry never asks the operator to write or edit a file by hand

  Scenario: AC8 The smoke profile exercises the loop against the fakes (new, D-RCV-60)
    Given the SIT profile and the six fakes of RWB-P6-E2021-CON
    When the smoke step runs
    Then it requests a notice, runs the 16:00 run for a synthetic business date, writes the dispatch file to the rwb-integration fake and reads back the acknowledgement with barcode RR223344556TH and sent date 15122026
    Then it returns the DELIVERED and the UNDELIVERABLE proof results and asserts the notice state, the decision record and the ledger answer of the fakes
    Then it asserts the two operations answer inside the 2 s budget
    Then it asserts that no payload of the run, the file or the events carries a name, an address or an account number

  Scenario: AC9 Rollback and the feature switch are safe (new, D-RCV-60)
    Given the release and the feature switch rwb.comms.win-dispatch-loop
    When the switch is turned off in an environment
    Then the run starts no dispatch, writes no dispatch file and holds the notices with the pending reason, and no letter reaches WIN
    Then the two read operations keep answering and the held notices keep their state
    When the release is rolled back
    Then the previous chart version is redeployed and the migration is reversed by its own script
    Then the workflow runs in flight are drained on the previous build ID and no run is started by a Schedule that no longer exists
    Then no secret is written into a values file, a chart template, a dashboard or the runbook
```

These nine criteria are new for the deployment and test artefacts only; they restate no business outcome owned by RWB-P6-E2021-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-comms login and no other service's credential | DP-02; Architecture v5 slide 29 |
| BR2 | The migration is a per-service Flyway sequence in schema rwb_comms and runs before the deployment is ready | DP-15; ADR-021; RWB-PLT-E1044-CON |
| BR3 | Every subscription has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Architecture v5 slide 22 notes |
| BR4 | The only clock of the service is the 16:00 Schedule; no Quartz row, no shared job table and no batch table exists | DP-10; Architecture v5 slide 44 |
| BR5 | No new topic is created for this capability: `rwb.comms.events.v1` carries events 14 and 15, `rwb.deviation.events.v1` and `rwb.case.events.v1` are consumed, and `rwb.decision-record.v1` is shared | DP-14; Architecture v5 slide 42 |
| BR6 | The outbox relay is JOB-11 of the platform and runs every minute; the service configures nothing of it but its own outbox | Architecture v5 slide 44; DP-09 |
| BR7 | No environment value is hard-coded: replica counts, resource sizes, timeouts, thresholds and deployment slots come from values files | Template and Rules §R7.2 s17 |
| BR8 | An alert carries a message ID and the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR9 | A refused read and an out-of-scope read are counted on the dashboard and never page the on-call rota | MSG-P4-002; MSG-P4-003 |
| BR10 | A re-run is idempotent on the notice ID and the business date and skips the notices already Unserved or Held and the notices already in a file of that date | Legacy RWB-E2-021 section 12 (Jobs) |
| BR11 | The service writes only schema rwb_comms and reads no other schema and no `v_ace_*` view; the proof rows are the INT-15 results of rwb-integration | DP-01; DP-05; DP-16 |
| BR12 | No dashboard series, log line or alert payload carries personal data; notice IDs, case IDs, barcodes, counts and durations only | Template and Rules §R7.2 s17 |
| BR13 | The stuck workflow scan is the platform's JOB-21 and is reused, not rebuilt | Architecture v5 slide 44 |
| BR14 | The daily reconciliation REC-05 and its owner are not fixed here; no source names them | Legacy RWB-E2-021 section 13; GAP-1090 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version, the outbox relay runs and the worker polls rwb-comms | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is the new one | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |
| Ready | The feature switch is turned off | The parameter changes in the environment | Ready with the dispatch off; the run writes no file |

The notice states are the app story's; this story moves none of them and only turns the dispatch on and off.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning step, the Schedule registration, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the Temporal cluster, the topic provisioning and the visibility queries behind JOB-21 |
| ACE database administrator | Owns schema rwb_comms, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments and the rollback when a run fails |
| On-call operator | Runs the runbook entries and opens an incident when a missing file or an unacknowledged file persists past its second window |
| RW-PLATADM | Reads the notices and operates the run and the rerun from the run view, not in the cluster |
| Owner of rwb-integration (P2) and the WIN owner | Are paged by the missing-file and the unacknowledged-file alerts and own the repair beyond the rwb-comms breaker |
| Owner of rwb-decision (P7) | Is paged by the decision-record alert and owns the shared chain |

The per-service login name used by the chart is a secret reference resolved at deploy time; the chart references "the rwb-comms login (DP-02)" and never a literal name.

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switch `rwb.comms.win-dispatch-loop`, the two client timeouts, the alert thresholds, the deployment slot |
| Schema | rwb_comms, migrated by the per-service Flyway sequence; `notice`, `template`, `merge_field` and the library objects |
| Topics | `rwb.comms.events.v1` produces events 14 and 15 with retry and `.dlt`; `rwb.deviation.events.v1` and `rwb.case.events.v1` are consumed with retry and `.dlt`; `rwb.decision-record.v1` is produced on as its owner provisions it |
| Queue | Temporal task queue `rwb-comms` in namespace `rwb-recovery` |
| Schedules | One: the JOB-10 notice dispatch run at 16:00 on business days; JOB-11 and JOB-21 are the platform's |
| File | The INT-14 dispatch file of one business date and the INT-15 proof result, both written and read through rwb-integration |
| Dashboard series | Files written by business date, notices in a file, acknowledgements received, notices without an acknowledgement, notices held by reason, notices unserved by result, proof window expiries, notices waiting for proof, decision record write failures, workflow open and stuck |
| Runbook entries | Missing dispatch file, unacknowledged file, proof window expired, held notice that should have gone out, stopped decision record chain, re-run of JOB-10 |
| Secrets | The rwb-comms login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |

The alert values, the replica counts, the probe timings and the deployment slot are deployment values; the provisional alert values and their confirmation are carried by the gap and the assumption of this story (GAP-1093; ASM-2041). The exact cluster topology, the node pools and the slot assignment follow the open decision DL35 of the P6 TSD and are not fixed here.

### 12. Contract

#### 12.1 REST operations provided

None. The deployment exposes the two operations of RWB-P6-E2021-CON unchanged; this story adds no path, no parameter and no response field, and the probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None declared by this story. The consumed operations of the capability — the reference data of rwb-case, the approval of rwb-decision, the case read and the case facts, the contact stops of rwb-deviation, the ledger of rwb-source-data and the file of rwb-integration — are deployed as client configuration only: their endpoints, their 2 s budget, their retry and their breaker are values of the environment, and no contract is defined here. The naming of the rwb-integration file operation is Not specified in the source documents (GAP-1089; ASM-2037).

#### 12.3 Events published

None declared by this story. `rwb.comms.NoticeDispatched.v1`, `rwb.comms.NoticeDelivered.v1` and `rwb.decision-record.DecisionRecorded.v1` are produced on the topics their owners provision; the deployment only configures the producer credential, the retry topic and the `.dlt` topic of `rwb.comms.events.v1` and reuses the shared `rwb.decision-record.v1` without recreating it.

#### 12.4 Events consumed

None declared by this story. The three consumer groups of `rwb.deviation.events.v1` and `rwb.case.events.v1` are provisioned with retry and `.dlt` as AC4 states, and their payload shapes belong to RWB-P6-E2021-CON.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| NoticeDispatchWorkflow | Workflow, one run per business date | `rwb-comms` | Worker deployment with the build ID of the release; polls `rwb-comms` in namespace `rwb-recovery` and no other queue |
| conductCheck | Activity, in rwb-comms | `rwb-comms` | Registered by the same worker |
| recordDecision | Activity, in rwb-comms | `rwb-comms` | Registered by the same worker; the series the decision-record alert reads |
| generateLetter | Activity, owner rwb-document | `rwb-document` | Called as a child activity of the other service; nothing deployed here |
| decisionApproval | Child workflow, owner rwb-decision | `rwb-decision` | Called by the workflow; nothing deployed here |
| deliverFile | Activity, owner rwb-integration | `rwb-integration` | Called by the workflow; the file run is rwb-integration's |

The worker is the only workload that polls a Temporal queue in this service. Its autoscaling, its replica count and its resource sizes are values, not template constants.

#### 12.6 Schedules

| Name | Cron | Overlap policy | Deployment element |
|---|---|---|---|
| The JOB-10 notice dispatch run | 16:00 on business days | SKIP with the catch-up window of the workflow kit | One Temporal Schedule, created by the provisioning step of this release, with the business date as the workflow input |

The bank Airflow owns the WIN file window and hands it to this Schedule; the handoff row is part of the release and its mechanism is Not specified in the source documents (GAP-1095; ASM-2043). The outbox relay JOB-11 runs every minute as a platform job and the stuck workflow scan JOB-21 is the platform's visibility query; neither is registered here. The daily reconciliation REC-05 is not registered here, because no source assigns its owner (GAP-1090; ASM-2038).

#### 12.7 Tables owned

None declared by this story as a new element. The migration job creates and migrates `notice`, `template`, `merge_field`, the local decision record and the library objects in schema `rwb_comms`; `recovery_case`, `task`, `timer`, `deviation`, `decision_log_entry`, `document`, `interaction` and `outbound_item` belong to other services and the migration job never touches them (DP-01).

#### 12.8 Contract fakes

None deployed into UAT or production. The six fakes of RWB-P6-E2021-CON run in the pipeline and in the SIT smoke profile of AC8 only, and they are test-only workloads.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None declared | The two operations are deployed unchanged; their clients are configuration |
| Kafka | 3 topic subscriptions and 2 topic productions provisioned | `rwb.deviation.events.v1` and `rwb.case.events.v1` consumed; `rwb.comms.events.v1` produced with retry and `.dlt`; `rwb.decision-record.v1` shared |
| Temporal | 1 worker, 1 workflow, 3 activities, 1 child workflow, 1 Schedule | The worker on `rwb-comms`, its activities, the approval child and the 16:00 Schedule |
| File | 2 | The INT-14 dispatch file of the business date and the INT-15 proof result, both through rwb-integration |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-comms/` | Chart with api and worker deployments, service, migration job, config map, secret references, probes and the Schedule hook of this release |
| `helm/rwb-comms/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, `rwb.comms.win-dispatch-loop`, the two client timeouts, the alert thresholds, the deployment slot |
| Pipeline stage | Build, unit, component and contract tests, retired-element check, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | The 16:00 Schedule; consumer group `rwb-comms` on `rwb.deviation.events.v1` and `rwb.case.events.v1` with retry and `.dlt`; reuse of `rwb.comms.events.v1` and `rwb.decision-record.v1`; task queue `rwb-comms` in namespace `rwb-recovery` |
| Dashboards | Ten series of section 11 |
| Alerts | Six rules, each with a message ID and one runbook entry |
| Runbook | Six entries: missing dispatch file, unacknowledged file, proof window expired, held notice that should have gone out, stopped decision record chain, re-run of JOB-10 |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay dependency is reachable and the Temporal worker on `rwb-comms` has polled; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database, calls another service or opens a file window.

**Dispatch series.** The file series is the count of dispatch files written by business date and read from the run records of the workflow and the file reference of rwb-integration; the acknowledgement series is the count of notices whose barcode and sent date landed after the file; the proof series is the count of notices past the proof window with no proof. They are not job-lateness measures, because there is no job.

**Alert mapping.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P6-004 | The dispatch file of the business date is missing | Missing-file alert with the business date, the workflow and the file reference | Platform on-call, page; ticket to the rwb-integration and WIN owners |
| MSG-P6-004 | The acknowledgement does not return inside its value | Unacknowledged-file alert after the second window with the file reference and the count of notices waiting | Platform on-call, page; ticket to the WIN owner |
| MSG-P6-008 | The proof window expires for a share of notices | Proof-window alert with the count, the oldest sent date and the barcode range | Ticket to the WIN owner, no page |
| MSG-P6-001 | A contact stop holds notices for a share of the case set | Held-by-reason series; a hold that should have gone out raises the held-notice alert | Platform on-call, ticket |
| MSG-P7-003 | The decision record chain stops during a run | Decision-record alert with the run, the notice and the chain position | Platform on-call, page; escalation to rwb-decision |
| None | JOB-21 raises a stuck workflow on `rwb-comms` | Stuck-workflow alert with the workflow ID, the step and the last event | Platform on-call, page |

Every alert carries its message ID where the condition maps to one, and the condition without a message ID carries the workflow name instead. The alert thresholds are deployment values with provisional defaults; the missing source for them is carried by the gap and the assumption of this story (GAP-1093; ASM-2041).

**Rollback.** The previous chart version is redeployed with its image digest, the migration is reversed by its own script in `rwb_comms`, the Schedule is restored to the previous definition, the workflow runs in flight drain on the previous build ID, and the feature switch is turned off first when a run is writing files, so no second file is written for a business date during the rollback. A rolled-back release leaves the notices in their states and writes no compensating notice.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact and fails on a fake drift or a retired element, the Schedule and the three consumer groups exist with their retry and `.dlt` paths, the ten panels carry the synthetic day, the six alerts fire on synthetic metrics, the rerun of a business date writes no second file, the rollback and the switch-off are exercised once in SIT, and the six runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-008 | The proof window expires with no proof, or a notice is unserved | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. |
| MSG-P6-004 | The dispatch file is missing or unacknowledged | {notice} was sent for registered mail on {date}. |
| MSG-P6-001 | A contact stop holds the letters of a case | Contact with this customer is stopped for {reason}. |
| MSG-P6-003 | A template was withdrawn before dispatch | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P3-004 | A legal hold blocks the letter | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P7-003 | The decision record chain stops | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A read without the Litigation right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A notice outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Your request is queued and will be retried. |

The message texts are copied unchanged from the legacy story where the message already existed; the deployment adds the routing, the threshold and the runbook link, never a new wording. The alert values and the deployment slot are Not specified in the source documents (GAP-1093; ASM-2041).

### 15. Screens and states

The deployment serves SCR-18 Notice approval in its Generated, Approved, Sent, Delivered, Unserved and Held states, SCR-04 Case timeline for the ledger entry of each outcome and SCR-44 Batch and job monitor for the 16:00 run, its file, its acknowledgement and its rerun, all behind the gateway-bff composite route (DP-19). The operator-facing surfaces of this story are the pipeline run view, the release view, the ten dashboard panels, the six alerts and the runbook; the smoke step runs the loop of a synthetic business date in SIT and asserts that the two operations answer inside the 2 s budget and that the file and the acknowledgement are exercised against the fakes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-021-01 | AC8 | End to end | N-0101 Approved; acknowledgment RR223344556TH; the smoke step's dispatch path |
| TC-E2-021-02 | AC8 | End to end | INT-15 DELIVERED, call-back 18122026; the smoke step's proof path |
| TC-E2-021-03 | AC5, AC8 | End to end | INT-15 UNDELIVERABLE; the unserved series of the dashboard |
| TC-E2-021-04 | AC5 | End to end | Open X1 with contact stop; the held-by-reason series |
| TC-E2-021-05 | AC5 | End to end | Postal consent WITHDRAWN, DEMAND notice; the statutory notice in the file |
| TC-E2-021-06 | AC5, AC6 | End to end | N-0102 sent 2026-12-15 and N-0103 sent 2026-12-16; JOB-10 on 2026-12-22; the proof-window series and alert |
| TC-E2-021-07 | AC5 | End to end | Legal hold true; the held-by-reason series |
| TC-E2-021-08 | AC5 | End to end | DEMAND-SSME TH v1 withdrawn 2026-12-13; the held-by-reason series |
| TC-E2-021-09 | AC4, AC6 | End to end | Open X2 with stop; decision log stubbed unavailable; the decision-record alert |
| TC-E2-021-10 | AC7 | End to end | POST and run repeated for one business date; the rerun writes no second file |
| TC-E2-021-11 | AC5 | End to end | N-0200 outside scope; the out-of-scope count and no page |
| TC-E2-021-12 | AC5 | End to end | POST with no notice type; the refused count and no page |
| TC-E2-021-13 | AC5 | Component | RW-CASEOWN sends POST; refused with MSG-P4-002; counted, no page |
| TC-E2-021-14 | AC4, AC6 | NFR | Decision log write forced to fail on 10 unserved results; the chain alert and no notice change |
| TC-P6-E2021-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with a pinned digest, the rwb-comms login reference, the migration job and a worker on `rwb-comms` |
| TC-P6-E2021-OPS-02 | AC2 | NFR | The 16:00 Schedule exists with SKIP and the catch-up window; no Quartz row, no second Schedule and no batch table |
| TC-P6-E2021-OPS-03 | AC3 | NFR | The Airflow window hands off business date 2026-12-14; a second run of the date writes no second file |
| TC-P6-E2021-OPS-04 | AC4 | NFR | The three consumer groups exist with retry and `.dlt`; a missing `.dlt` fails the release; the outbox relay series moves |
| TC-P6-E2021-OPS-05 | AC5 | NFR | A synthetic day with one file, one missing file, one acknowledgement, two waits, four hold reasons, three results and two expiries; ten panels populated |
| TC-P6-E2021-OPS-06 | AC6 | NFR | Six synthetic conditions raise their alerts and resolve one runbook entry each, with the message ID and the escalation path |
| TC-P6-E2021-OPS-07 | AC7 | NFR | The rerun of a business date skips the Unserved, the Held and the notices of the file of that date, and is idempotent |
| TC-P6-E2021-OPS-08 | AC8 | NFR | The smoke profile runs the loop on the six fakes in SIT and asserts the two answers, the file, the acknowledgement and no personal data |
| TC-P6-E2021-OPS-09 | AC9 | NFR | The switch off writes no file and holds the notices; the rollback restores the previous chart and drains the runs |

The fourteen legacy cases keep their legacy order, their level mapping (System to End to end, Access to Component, Resilience to NFR) and their legacy data; the nine OPS cases are new and test the deployment and the runbook. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in a values file: the proof window, the statutory notice type list, the eligible states, the hold reasons and the result code map are reference data held by their owner, never a deployment value.
- No personal data in logs, dashboard series, alert payloads or the runbook: notice IDs, case IDs, barcodes, user IDs of staff, counts and durations only.
- One login per service; the chart carries the rwb-comms login reference and no other service's credential (DP-02).
- The service writes only schema rwb_comms; the migration job never touches another schema and no dashboard query reads one (DP-01).
- ACE data is reached only through the owner's contract or the owner's `v_ace_*` views; no dashboard and no smoke step reads an ACE view, and the proof rows come as the INT-15 results of rwb-integration (DP-05, DP-16).
- Every subscription has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- One clock and no new topic: the 16:00 Schedule starts the workflow, `rwb.comms.events.v1` carries the two events, and no Quartz row, shared job table or batch table exists (DP-10, DP-14).
- The release pins the image digest and the chart version, and no secret is written into a values file, a chart template, a dashboard or the runbook.
- A rerun is idempotent on the notice ID and the business date, and no operator writes or edits a dispatch file by hand (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | The 16:00 Schedule, the file series, the acknowledgement series and the proof-window series | TC-P6-E2021-OPS-02, TC-P6-E2021-OPS-03, TC-P6-E2021-OPS-05 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | The held-by-reason series, the held-notice alert and the decision-record alert | TC-P6-E2021-OPS-05, TC-P6-E2021-OPS-06 |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | The smoke step's statutory case and the file series | TC-P6-E2021-OPS-08 |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | The outbox relay check, the unserved series and the decision-record chain alert | TC-P6-E2021-OPS-04, TC-P6-E2021-OPS-06 |
| ADR-023 | Observability per service | Ten panels, six alert rules and six runbook entries | TC-P6-E2021-OPS-05, TC-P6-E2021-OPS-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-021, disposition Split (rework) |
| Legacy criteria | AC1 to AC12 of the legacy story; this story copies none of them and serves them through the run, the file, the dashboards and the runbook |
| Test cases | The fourteen legacy cases as the evidence the deployment serves, and the nine new cases TC-P6-E2021-OPS-01 to -09 |
| Decoupling patterns | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-016 (reusable Temporal layer, Schedules replace Quartz), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership) |

### 19. Out of scope

- The application code of the two operations, the conduct check, the run and the delivery handler (RWB-P6-E2021-APP).
- The contract documents and the fakes as published artefacts (RWB-P6-E2021-CON); this story only deploys the test copies into SIT.
- The generation of a notice and the template catalogue (RWB-P6-E1052-APP, RWB-P6-E1046-APP).
- The proof capture design and its result code map (RWB-P6-E1055-APP, RWB-P6-E1055-CON and RWB-P6-E1055-OPS).
- The SMS and LINE dispatch of the same service (RWB-P6-E2022-OPS).
- The platform topic provisioning, the Temporal cluster and the observability stack (the platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The outbox relay JOB-11 and the stuck workflow scan JOB-21 as platform jobs; this story only measures them.
- The WIN file window and the file runs of rwb-integration (P2, DP-16), and the proof results of the WIN owner.
- The daily reconciliation REC-05 and its mechanism, which no source assigns (GAP-1090).
- The `rwb_comms` schema design and the logical model (the database stories of the service epic).
- The cross-service journey harness and its evidence (`RWB-ITG-E2021-ITG`).
