# RWB-P2-E2034-OPS Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2034-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-16) |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P2-I |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013, REQ-ILG-014, REQ-ILG-007, REQ-ILG-008, REQ-ILG-006) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-034 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (9 resolved, 29 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the rwb-integration ledger intake worker deployed on task queue `rwb-integration` with its consumer groups on the four owner topics, the retry scan and the outbox relay, the EFS read trigger as an event-started workflow, the exception queue alert, the five dashboard series and the runbook entries**, so that **an operator can see a channel event that stopped moving, resend it, and prove that nothing was lost between a channel and the ledger without reading code**.

### 2. Business rationale

The legacy story assumed a consumer named "ledger-channels" inside one module: the outbox, the consumer offset, the exception queue and the ledger were in one process, so a stuck delivery showed up as a failed row and an operator had the database in front of them. In the target the consumer is a deployment of its own. Its progress is a Kafka offset, its failures are delivery rows in `rwb_integration`, its writes go to another service, and its busiest hour is the morning run and the 16:00 letter window (Arch v5 slide 33). Without this story the app story can pass its unit tests while a consumer group is unassigned, a partition lags for a day, the exception queue grows silently and the EFS read step never runs — and the business measure, that a contact is visible on the case, falls with no alert.

Deployment is also where the split is enforced operationally. The release carries the rwb-integration login only, subscribes to the owners' topics only, and applies the `rwb_integration` migration only; it never touches the ledger schema, the case schema or an ACE view (DP-01, DP-02, DP-18). The observability follows ADR-023 per service: five series (consumer lag, deliveries in RETRYING, deliveries in EXCEPTION, append answers by class, EFS read summary counts), three alerts and three runbook entries, each alert carrying a message ID and one runbook entry.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The rwb-integration baseline chart and login are deployed by RWB-P2-E1007-APP, with the REST base `/api/recovery/integration/v1` and the relay of `rwb_integration` (DP-02, DP-13).
- The Kafka event platform provides the four owner topics with their retry and `.dlt` topics and the shared topic `rwb.decision-record.v1`, and the ACLs of this service's principals (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The Temporal workflow kit and the `rwb-recovery` namespace exist, with worker versioning, the build ID provider and the payload codec (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The platform error envelope and the message catalogue are in force, so an alert can carry a message ID.
- The three environments DEV, SIT and UAT exist and the production namespace exists for the release date; the flag `rwb.integration.ledger-channels` exists in the flag library.
- The gateway-bff composite route for SCR-09 is published (RWB-PLT-N001-CON, DP-19).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the API deployment, the ledger intake worker and the outbox relay with the rwb-integration login, the namespace `rwb-recovery`, the task queue `rwb-integration`, the payload codec and the build ID of the release.
3. The consumer group step creates the two groups of the deployment on the four owner topics, with the offset reset policy, the maximum poll and the `.dlt` routing, and records the starting offsets of each partition.
4. The flag step sets `rwb.integration.ledger-channels` from the values of the environment.
5. The migration step applies the `rwb_integration` sequence of this release and refuses to run when the target schema is not `rwb_integration`.
6. The trigger step confirms that the EFS read step is started by `rwb.source-data.AceDataReady.v1` and registers no Schedule for it.
7. The retry scan step starts the delivery retry scan on its interval and confirms the attempt limit of three.
8. The dashboards are published with the five series and the environment, release and build ID as dimensions.
9. The three alerts are wired to their message identifiers and to their runbook entries: MSG-P2-001 for the exception queue, and for the lag alert and the EFS trigger alert the identifier that the Error and Message Standard has yet to name, carried as Not specified in the source documents (GAP-0666; ASM-1175).
10. A smoke step publishes one synthetic `rwb.comms.NoticeDispatched.v1` for a synthetic case in DEV, follows it to DELIVERED against the P1 fake, and then parks one delivery in EXCEPTION and resends it through the admin operation.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render or the migration job fails | The deployment stays unready and the pipeline stops; no traffic and no offset is committed | None | AC1 |
| X2 | A consumer group is assigned no partition, or a partition lags past its threshold | The lag series rises and the lag alert fires; the runbook entry names the check | Not specified in the source documents (GAP-0666; ASM-1175) | AC2, AC5 |
| X3 | The flag is off in an environment | The worker is not deployed, the consumer groups hold no member, the relay is idle and the deliveries stay PENDING | None | AC1 |
| X4 | A delivery reaches its third failure | The delivery is EXCEPTION with the last error code and a task for RW-PLATADM; the exception alert fires | MSG-P2-001 | AC3 |
| X5 | AceDataReady arrives and the EFS read step does not start | The EFS trigger check fails the smoke run and the runbook entry names the event and the group | Not specified in the source documents (GAP-0666; ASM-1175) | AC4 |
| X6 | A dashboard series is missing, or an alert carries no message ID or no runbook link | The observability check fails the release | None | AC5, AC6 |
| X7 | The P1 append is unavailable at release time | The deliveries accumulate in RETRYING, the append-answer series shows the 5xx class and the alert fires; nothing is lost and nothing is parked before the third attempt | MSG-P2-001 | AC3, AC5 |
| X8 | A new build is promoted while deliveries are in RETRYING | The workflow of each delivery replays on the new build from its history; the dashboards show both build IDs | None | AC1, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the topic provisioning and the flag library; no application code is built here |
| Negotiable | Replica counts, resource sizes, lag thresholds, alert thresholds and scan intervals are environment values |
| Valuable | Makes the intake observable, resendable and provable on the morning run and the 16:00 window before the release date |
| Estimable | One chart, two consumer groups, one retry scan, one event trigger, five series, three alerts and three runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the groups hold offsets, an alert fires on a synthetic metric, the trigger starts a workflow, the runbook is reviewed |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the channel ledger intake for rwb-integration

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-integration is rwb-integration
    Given the target environment is SIT

  Scenario: AC1 The worker, the relay and the login are deployed from one chart (new, D-RCV-60)
    Given the rwb-integration chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the ledger intake worker polls only the task queue rwb-integration in namespace rwb-recovery
    Then the outbox relay runs on its one-minute interval and the delivery retry scan on its own interval
    Then the release declares the rwb-integration login and no other service's credential
    Then the migration step applies the rwb_integration sequence and refuses a target schema other than rwb_integration
    Then worker versioning is enabled and a new workflow goes to the new build while the old build drains

  Scenario: AC2 The two consumer groups are created with their offsets and their limits (new, D-RCV-60)
    Given the release of this story and the four owner topics
    When the consumer group step runs
    Then the ledger intake group is a member of rwb.treatment.events.v1, rwb.comms.events.v1, rwb.partner.events.v1 and rwb.payment.events.v1
    Then the EFS read group is a member of rwb.source-data.events.v1 and of no other topic
    Then each assignment has its offset reset policy, its maximum poll and its retry and .dlt topic routing recorded
    Then a topic outside the five is refused by the release, and the committed offset of each partition is reported per environment
    Then no group is created for a topic of this service

  Scenario: AC3 The exception queue alert and the retry scan report a parked delivery (new, D-RCV-60)
    Given the published alert rules and the retry scan of the deployment
    When one synthetic delivery fails its third attempt
    Then the retry scan sets the status EXCEPTION with the last error code and a task for role RW-PLATADM
    Then the exception queue alert fires with MSG-P2-001, the consumer name, the event type and the build ID
    Then the alert payload carries no case identifier beyond the delivery reference, no contact point and no amount
    Then the resend metric rises when the platform administrator resends the delivery through the admin operation

  Scenario: AC4 The EFS read step is triggered by AceDataReady and owns no Schedule (new, D-RCV-60)
    Given the deployed worker and the group on rwb.source-data.events.v1
    When a synthetic AceDataReady message for the EFS source is published
    Then EfsLedgerReadWorkflow starts once with the business date of the event
    Then a duplicate of the same message starts no second run and the hit count rises in the inbox
    Then the deployment registers no Schedule for the EFS read step and none for the intake
    Then the run closes with the read summary rowsRead, written, excluded and notOnCase on the dashboard

  Scenario: AC5 The five dashboard series carry the environment, the release and the build ID (new, D-RCV-60)
    Given the published dashboard of the deployment
    When a synthetic run, a lag and a set of failures are produced
    Then the dashboard shows consumer lag by group and partition, deliveries in RETRYING, deliveries in EXCEPTION, append answers by class and the EFS read summary counts
    Then each series carries the environment, the release and the build ID as dimensions
    Then a lag past its threshold and an EXCEPTION delivery are both visible on the dashboard before any alert is read

  Scenario: AC6 The runbook and the three alerts cover the operational failures (new, D-RCV-60)
    Given the published runbook and the alert rules
    When a lagging group, a parked delivery and a missing EFS run are simulated
    Then the parked-delivery alert carries MSG-P2-001, and the lagging-group and missing-run alerts carry the identifier placeholder of GAP-0666
    Then every alert links exactly one runbook entry that holds its check, its owner role and its recovery step
    Then the runbook names the resend operation, the attempt limit of three and the fact that no delivery may be deleted
    Then no alert threshold and no interval is hard-coded, and no secret appears in a values file, a dashboard or the runbook
```

```gherkin
Scenario: AC7 Each operation, event and activity of section 12 is verified against its owner's contract (new, D-RCV-60)
    When each operation, event and activity of section 12 is exercised against its owner's contract
    Then a mismatch fails the build

Scenario: AC8 The release touches only the five tables of section 12.7 (new, D-RCV-60)
    When the release is deployed and its smoke run is executed
    Then only the five tables of section 12.7 are touched
    Then no ledger, EFS reference or case table is created, altered or read

Scenario: AC9 A failing smoke run leaves the previous build in force (new, D-RCV-60)
    When the smoke run of a new build fails
    Then the new build is not promoted
    Then the previous build stays in force until the new build passes its tests and its smoke run

Scenario: AC10 Operational outputs carry no contact point, amount or decoded payload (new, D-RCV-60)
    When the dashboard series, alert payloads and runbook entries are scanned
    Then they carry counts, ids, codes, event types and build IDs only
    Then none carries a contact point, an amount or a decoded payload
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One login, one task queue and one schema per service: the release carries the rwb-integration login, polls `rwb-integration` only and migrates `rwb_integration` only | Arch v5 slide 41; DP-02; DP-15 | AC1 / TC-01 |
| BR2 | The deployment subscribes to the owners' topics only, one group for the six business events and one for AceDataReady, and to no topic of this service | Arch v5 slides 42 and 43; DP-09; DP-14 | AC2 / TC-02 |
| BR3 | The attempt limit is three and an exhausted delivery is EXCEPTION with a task for RW-PLATADM; no delivery is ever deleted | Legacy AC7 and AC8; BR6 of the app story | AC3 / TC-03 |
| BR4 | The EFS read step is started by AceDataReady and owns no Schedule; the only periodic element is the relay and the retry scan, which are platform intervals | Legacy section 12; Arch v5 slide 44 JOB-02 and JOB-04 | AC4 / TC-04 |
| BR5 | Every worker carries the build ID of its release and worker versioning is enabled, so a new build takes new workflows while the old build drains | Temporal and Drools design slide 11; RWB-PLT-E1071-CON | AC1 / TC-01 |
| BR6 | Every alert carries a message ID and the agreed text and links one runbook entry | Template and Rules §R7.2 s14 | AC6 / TC-06 |
| BR7 | No environment value is hard-coded: replicas, resources, lag thresholds, alert thresholds, scan intervals and the flag come from values files and parameters | Template and Rules §R7.2 s17 | AC6 / TC-06 |
| BR8 | Dashboard series, alert payloads and the runbook carry counts, ids, codes, event types and build IDs only, never a contact point, an amount or a decoded payload | Temporal and Drools design slide 11 (PDPA); ADR-023 | AC10 / TC-10 |
| BR9 | The release writes no ledger row and reads no ledger table: the append goes to the P1 contract at POST /cases/{caseId}/interactions, and the migration touches `rwb_integration` only. The ledger, its retention class and its ordered read belong to rwb-source-data, and no element of this service declares them | DP-01; DP-18 | AC8 / TC-08 |
| BR10 | A failing release never replaces a working one: the previous build stays in force until the new build passes its tests and its smoke run | DP-10 | AC9 / TC-09 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Worker registered and probes healthy | The worker polls `rwb-integration` only and the two groups hold an assignment | Ready |
| Ready | Release superseded | A new chart version passes its tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open workflows | Ready |
| Ready | Flag off | `rwb.integration.ledger-channels` is turned off in the environment | Not deployed |
| Ready | Smoke run failed | The trigger, the append or the resend step of the smoke run fails | Blocked |
| Blocked | Previous build restored | The smoke run passes on a later build, or the previous chart is redeployed | Ready |

The delivery states PENDING, RETRYING, DELIVERED and EXCEPTION are the app story's runtime and are not states of this deployment.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the consumer group step, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic ACLs, the consumer quotas, the flag library and the exception queue resend |
| Platform event owner | Owns the four topics, their retry and `.dlt` topics, the schema registry and the `.dlt` retention |
| Release manager | Approves the promotion of one artefact and may block it on a failing smoke run |
| On-call operator | Runs the three runbook entries and opens an incident when a lag or a parked delivery persists |
| RW-AUDIT | Reads the deliveries, the resend record and the run summaries |

The worker runs as the rwb-integration service identity (DP-02), carried by the chart as a secret reference and never as a literal name. The login name is Not specified in the source documents (GAP-0666; ASM-1175).

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, feature switch | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |
| Task queue | `rwb-integration` in namespace `rwb-recovery`, polled by the rwb-integration worker only | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |
| Consumer groups | The ledger intake group on `rwb.treatment.events.v1`, `rwb.comms.events.v1`, `rwb.partner.events.v1` and `rwb.payment.events.v1`; the EFS read group on `rwb.source-data.events.v1` | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |
| Topics | The five consumed topics with their retry and `.dlt` topics; `rwb.decision-record.v1` published by the local library; `rwb.integration.events.v1` untouched by this slice | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |
| Schema | `rwb_integration`, migrated by its own per-service Flyway sequence; this release applies the intake migration | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |
| Dashboard series | Consumer lag by group and partition, deliveries in RETRYING, deliveries in EXCEPTION, append answers by class, EFS read summary counts; dimensions environment, release, build ID | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |
| Runbook entries | Lagging consumer group, parked delivery, missing EFS run; each with the check, the owner role and the recovery step | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |
| Alerts | Three rules and one runbook entry each: MSG-P2-001 for the exception queue, and the identifier placeholder of GAP-0666 for the lag alert and the EFS trigger alert | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |
| Secrets | The rwb-integration login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |
| Test data | One synthetic `rwb.comms.NoticeDispatched.v1` for case "RW-2026-000301", one synthetic AceDataReady for the EFS source and one synthetic delivery to park and resend; the fixture owner is Not specified in the source documents (GAP-0666; ASM-1175) | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-7) |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value and this story fixes only their names and the rule that they are never hard-coded.

**Probes.** Readiness answers healthy only after the worker has polled `rwb-integration` once, the two consumer groups hold an assignment and the relay has read its first delivery; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database or commits an offset, and a failing dependency is reported as not ready, never as live-and-broken. The paths and timings are values of the environment.

### 12. Contract

#### 12.1 REST operations provided

None from this story. The two admin operations of the slice — `GET /api/recovery/integration/v1/admin/outbox/deliveries` and `POST /api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend` — are declared by RWB-P2-E2034-CON and implemented by RWB-P2-E2034-APP; this deployment exposes them through the chart and its ingress and declares no path of its own. The probes are cluster-internal and are not part of the API surface. Contract version built against: `rwb-integration.yaml` and `asyncapi/rwb-integration.asyncapi.yaml`, each `info.version` 5.0.0 (05 Technical architecture/Recovery Workbench API Specification v5).

#### 12.2 REST operations consumed

None from the deployment. The worker calls the P1 append and the fact contracts at run time as the app story's client; the chart carries no REST client of its own, no composite route and no outbound call at start-up beyond the Temporal frontend and the Kafka brokers.

#### 12.3 Events published

None of its own. `rwb.integration.events.v1` carries FileDelivered and FileFailed from the outbound file side and this slice publishes neither; `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library through the relay when a resend or an exception is recorded (DP-03, DP-09).

#### 12.4 Events consumed

| Event type | Topic | Deployment element | Owner / service |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | Ledger intake group, with the inbox, the retry topic and the `.dlt` routing | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-24) |
| `rwb.comms.NoticeDispatched.v1` | `rwb.comms.events.v1` | Same group | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-24) |
| `rwb.comms.NoticeDelivered.v1` | `rwb.comms.events.v1` | Same group | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-24) |
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | Same group | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-24) |
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | Same group | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-24) |
| `rwb.payment.ProceedsMatched.v1` | `rwb.payment.events.v1` | Same group | Not specified in the source documents (DOR-RWB-P2-E2034-OPS-24) |
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | EFS read group, starting EfsLedgerReadWorkflow; not an outbox delivery | rwb-source-data (producer of AceDataReady) |

The five topics, their retry and `.dlt` topics and the seven types are provisioned and owned by the platform event epic and by the owners' contracts; this deployment configures the two consumer groups, the inbox, the offsets and the relay that turns a delivery into a workflow start.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| LedgerChannelIntakeWorkflow | Workflow, one execution per consumed event, workflow ID = the CloudEvents id | `rwb-integration` | Registered by the worker of this release, with the build ID and worker versioning |
| EfsLedgerReadWorkflow | Workflow, started by AceDataReady for the EFS source | `rwb-integration` | Registered by the same worker; no Schedule |
| mapChannelEvent, resolveChannelFacts, appendLedgerEntry, parkDeliveryInException | Activities | `rwb-integration` | Registered by the same worker with the kit's retry policy of 1 s, back-off 2, 3 attempts |
| readEfsOutcomes, appendEfsEntries, writeEfsReadSummary | Activities | `rwb-integration` | Registered with the same policy; idempotent by the event key and the EFS key |
| LedgerChannelListener and the delivery retry scan | Outbox consumer and scan | not a worker | Deployed in the same release; start the workflow per event and move a delivery on its next attempt |

**Build ID and versioning.** The build ID is the one supplied by the workflow kit for the release commit; worker versioning is enabled and a new build takes new workflows while the old build drains. The build ID format and the versioning policy are Not specified in the source documents (GAP-0666; ASM-1176).

#### 12.6 Schedules

None. The deployment registers no Schedule: the intake is event-started from the seven consumed types and the EFS read step is started by AceDataReady. The relay and the retry scan run on platform intervals of the outbox library, not on a Schedule of this service (BR4).

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| outbound_item | P2 (rwb_integration) | Read by the exception queue screen only; the release adds no column |
| outbox_delivery | PLT library, created in rwb_integration | The delivery trail, its attempt count and its task; read by the retry scan |
| processed_event | PLT library, created in rwb_integration | The inbox; read and written by the listener |
| idempotency_key | PLT library, created in rwb_integration | The stored response of the two admin operations |
| decision_record | PLT library, created in rwb_integration | The record of a resend and of an exception, published by the library |

The release applies the intake migration of the app story and no other: no ledger table, no EFS reference table and no case table is created, altered or read (DP-01, DP-15, DP-18).

#### 12.8 Contract fakes

None. No fake is deployed. The workflow tests run on the platform's test environment in the pipeline and the contract mocks of the P1 append and of the five fact contracts are in-process test doubles of the app story. The smoke run of DEV calls the P1 fake of the service environment, never a fake shipped by this release.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed by the deployment | The two admin operations are the app story's; the probes are cluster-internal |
| Kafka | 0 published, 7 types consumed through 2 groups | Four owner topics with the intake group, `rwb.source-data.events.v1` with the EFS read group; retry and `.dlt` on every one |
| Temporal | 2 workflows, 7 activities, 0 Schedules | Worker on `rwb-integration` with a pinned build ID and worker versioning |
| File | None | No file is read or written by the deployment |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release migrates `rwb_integration` only and reads no other schema | none |
| DP-03 | DecisionLogWriter, decision log | The local record library is deployed with the relay and publishes to `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read in this release; the EFS rows come through the P1 contract at run time | none |
| DP-06 | Parameters, casewf.config | The rwb-case parameters contract is a run-time dependency of the worker, with its client library | H RWB-PLT-E1042-CON |
| DP-07 | Reference data, LOV | The rwb-case reference-data contract is a run-time dependency of the worker | H RWB-PLT-E1043-CON |
| DP-08 | RecoveryAccessGuard | The rwb-access authorise contract is a run-time dependency of the two admin operations | H RWB-PLT-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | The two consumer groups with the inbox, the retry topic and the `.dlt` topic; the relay on its one-minute interval | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue and the namespace come from the workflow kit; no Schedule is registered | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The release declares no REST path and no client of its own; the worker calls the contracts as the app story's client | none |
| DP-13 | `/api/recovery/v1` | The ingress serves `/api/recovery/integration/v1` and no other base | none |
| DP-15 | V0001 baseline, migration | The per-service Flyway sequence of `rwb_integration`; the migration step refuses another schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | No ledger object is deployed, migrated or read; the append goes to rwb-source-data | none |
| DP-19 | Screen, ace-web | gateway-bff serves SCR-09; the deployment registers the route and no screen of its own | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-integration/` overlay | API deployment, ledger intake worker, outbox relay, retry scan, config map, secret references, probes, task queue, namespace, build ID and flag |
| `helm/rwb-integration/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, build ID, consumer group names, intervals (ASM-1175) |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, migration step, smoke run, promotion |
| Consumer group step | The two groups on the five topics, with the offset reset policy, the maximum poll, the retry and `.dlt` routing and the starting offsets |
| Migration step | The `rwb_integration` migration of this release; a target schema other than `rwb_integration` is refused |
| Trigger step | Confirms the EFS read step starts from AceDataReady and registers no Schedule |
| Dashboards | The five series of section 11 with the three dimensions |
| Alerts | Three rules, each with a message identifier or its placeholder and one runbook entry |
| Runbook | Three entries: lagging consumer group, parked delivery, missing EFS run |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P2-001 | A delivery is in EXCEPTION, or the P1 append is failing | Exception queue alert naming the consumer, the event type and the build ID, with the count and the oldest attempt time | Platform on-call, page |
| Not specified in the source documents (GAP-0666; ASM-1175) | Consumer lag of either group is past its threshold | Lag alert naming the group, the topic, the partition and the lag | Platform on-call, page in the morning run and the 16:00 window, else ticket |
| Not specified in the source documents (GAP-0666; ASM-1175) | AceDataReady was consumed and no EfsLedgerReadWorkflow started | EFS trigger alert naming the business date, the source and the group | Platform on-call and the business on-call, ticket |

**Retry and offsets.** The retry scan reads `outbox_delivery` where the status is PENDING or RETRYING and the next attempt is due, and moves the delivery on the interval of the environment; the attempt limit is three (BR3). Offsets are committed after the inbox row is marked, so a crash replays the append and the P1 writer returns the same entry — the at-least-once rule of DP-09 with the dedupe of the app story. The interval values and the lag thresholds are environment values (ASM-1175).

**Rollback.** A release that fails the smoke run is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open workflows until they finish; the deliveries in RETRYING are replayed from their history and the inbox makes the replay harmless. No data repair is needed, because the intake writes no ledger row of its own.

**Feature switch.** `rwb.integration.ledger-channels`. On: the worker and the two groups are deployed, the intake and the EFS read step run. Off: no worker and no group member, the relay is idle, and deliveries stay PENDING without being dated or parked.

**Done when.** The chart renders for DEV, SIT and UAT with a pinned digest and the build ID, the two groups hold their assignments and report offsets, the migration step refuses a foreign schema, the smoke run follows one notice to DELIVERED and one delivery to EXCEPTION and back through the resend, the five series and the three alerts are published with their identifiers or placeholders and their runbook links, and the three runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | A delivery is in the exception queue, or the P1 append is failing | Not specified in the source documents (GAP-0666; ASM-1175) |
| Identifier pending | Consumer lag of one group is past its threshold | Not specified in the source documents (GAP-0666; ASM-1175) |
| Identifier pending | AceDataReady was consumed and no EFS read run started | Not specified in the source documents (GAP-0666; ASM-1175) |
| MSG-GEN-005 | A resend is accepted in the smoke run | Not specified in the source documents (GAP-0666; ASM-1175) |

MSG-P2-001 and MSG-GEN-005 are named by the FSD and by the legacy exception flows, and their texts are not in the source set. The lag alert and the EFS trigger alert have no message identifier in the source set at all, so their identifier and their text are carried as the placeholder until the Error and Message Standard names both. An alert payload names counts, event types, group names, business dates and the build ID only, never a case identifier, a contact point or an amount.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard, SCR-09 Exception queue through gateway-bff, and the runbook. SCR-09 is served by the app story and the composite route of RWB-PLT-N001-CON; the deployment only registers the route. The Temporal Web UI stays behind Entra ID: RW-PLATADM operates and RW-AUDIT reads, and payloads are decoded only through the codec server under break-glass. SCR-44 Interface and job monitor is not used for the intake, because the deployment registers no job of its own and the relay is a platform interval. SCR-09 states: loading as in Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-3250). SCR-44 states: empty, loading, error and no access: Not specified in the source documents (CG-ALL-3251).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2034-OPS-01 | AC1 | NFR | The chart renders for three environments with a pinned digest, the build ID, worker versioning and the rwb-integration login reference; a foreign migration target is refused |
| TC-P2-E2034-OPS-02 | AC2 | NFR | Two groups with their assignments on five topics; a sixth topic refused; the offsets of each partition reported |
| TC-P2-E2034-OPS-03 | AC3 | NFR | One synthetic delivery failing three times: EXCEPTION, the task for RW-PLATADM, the alert with MSG-P2-001, and the resend metric |
| TC-P2-E2034-OPS-04 | AC4 | NFR | One synthetic AceDataReady starts one EFS run; a duplicate starts none; no Schedule is registered |
| TC-P2-E2034-OPS-05 | AC5 | NFR | The five series carry the three dimensions; a lag and an EXCEPTION delivery are visible before the alerts |
| TC-P2-E2034-OPS-06 | AC6 | NFR | Three synthetic conditions raise the three mapped alerts, each with one runbook entry and no hard-coded threshold |
| TC-P2-E2034-OPS-07 | AC7 | Contract | Each operation, event and activity of section 12 is exercised against its owner's contract; a mismatch fails the build |
| TC-P2-E2034-OPS-08 | AC8 | Boundary | The five section 12.7 tables are the only tables touched; no ledger, EFS reference or case table is created, altered or read (ASM-3438) |
| TC-P2-E2034-OPS-09 | AC9 | Smoke | A failing smoke run is not promoted; the previous build stays in force until the new build passes its tests and smoke run |
| TC-P2-E2034-OPS-10 | AC10 | NFR | Dashboard, alert and runbook payloads are scanned: counts, ids, codes, event types and build IDs only, with no contact point, amount or decoded payload |

### 17. Guardrails

- No business value in a values file: the event codes, the channels, the attempt limit and the case states are reference data and application behaviour, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the runbook or the workflow history: counts, ids, codes, event types, business dates and build IDs only, and payloads stay encrypted.
- One login per service, one task queue per service and one schema per service: the release carries the rwb-integration login, polls `rwb-integration` and migrates `rwb_integration` only (DP-02, DP-15).
- The release deploys no ledger object and reads no ledger table; the append goes to the rwb-source-data contract (DP-01, DP-18).
- The two consumer groups subscribe to the five owner topics only and have a retry topic and a `.dlt` topic before they start (DP-09).
- No delivery is ever deleted: an exhausted delivery is EXCEPTION with a task, and a resend sets PENDING with attempt count 0 (BR3).
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing smoke run never replaces a working build.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-ILG-009 | Contact outcomes from collections reach the ledger | The EFS read group, the trigger step and the EFS read summary series | TC-P2-E2034-OPS-02, TC-P2-E2034-OPS-04 |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery | The intake group on the two notice types and the append-answer series | TC-P2-E2034-OPS-02, TC-P2-E2034-OPS-03 |
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when | The intake group on the two partner types | TC-P2-E2034-OPS-02 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline | The append to the P1 contract that the timeline reads; no screen is deployed here | TC-P2-E2034-OPS-01 |
| REQ-ILG-013 | Ledger entries carry their own retention class | No deployment element: the class is resolved by rwb-source-data and no environment value sets it | TC-P2-E2034-OPS-01 |
| REQ-ILG-014 | The contact point is a reference and is never copied | The alert and dashboard payload rule and the encrypted workflow history | TC-P2-E2034-OPS-03, TC-P2-E2034-OPS-05 |
| REQ-ILG-007 | One entry per key; a repeat is ignored and counted | The offset-after-inbox rule and the inbox hit count of the intake group | TC-P2-E2034-OPS-02, TC-P2-E2034-OPS-04 |
| REQ-ILG-008 | A failed ledger write loses no entry and the delivery is retried | The retry scan, the attempt limit of three, the exception alert and the runbook entry | TC-P2-E2034-OPS-03, TC-P2-E2034-OPS-06 |
| REQ-ILG-006 | The timeline orders entries by occurred time and case sequence; the page order conflict is recorded under ASM-B2-P3-010-2 | The occurred time carried in the event payload and preserved by the deployment | TC-P2-E2034-OPS-02 |
| ADR-023 | Observability per service | The five series, the three alerts and the three runbook entries | TC-P2-E2034-OPS-05, TC-P2-E2034-OPS-06 |

Placement note. The plan keeps rwb-integration as primary for RWB-E2-033 to RWB-E2-036. The tension with the case and workflow folders named in RWB-E2-036 is recorded here for the assembly step (GAP-3187).

### 19. Out of scope

- The listener, the mapper, the client, the delivery tracker, the two workflows, the activities, the controller and the migration as code (RWB-P2-E2034-APP).
- The contract documents, the entry shape, the dedupe key, the exception rule and the fakes (RWB-P2-E2034-CON); this story only deploys and gates them.
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The topic provisioning, the schema registry and the `.dlt` retention (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The ledger table, its append operation and its read (the rwb-source-data stories of this legacy key).
- The timeline, the case record and the scope check (the rwb-case and rwb-access stories).
- The partner portal, the instruction facts and the partner screens (the rwb-partner stories).
- The outbound file items, the WIN and debt-buyer file windows and the outbound-item exception queue (RWB-P2-E1007-APP and RWB-P2-E1007-OPS).
- The real cross-service proof of the append, the dedup and the exception rule against the live owners (the integration story of this key).
- The exact cluster topology, node pools, replica counts, lag thresholds and probe timings; they are set per environment by the platform team.
