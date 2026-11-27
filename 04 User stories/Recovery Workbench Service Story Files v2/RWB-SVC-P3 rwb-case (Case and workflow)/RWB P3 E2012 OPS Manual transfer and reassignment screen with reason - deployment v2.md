# RWB-P3-E2012-OPS Manual transfer and reassignment screen with reason

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2012-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not yet sized; the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-AE |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2012-CON; C RWB-P3-E1043-CON |
| Integration dependencies | H RWB-PLT-E1027-CON; H RWB-PLT-E1072-CON; H RWB-PLT-E1043-CON; H RWB-PLT-TE006-CON; H RWB-PLT-E1071-CON; H RWB-PLT-E1047-CON; H RWB-PLT-E1044-CON; H RWB-PLT-N001-CON |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-013, FR-P3-017, FR-P3-018, FR-P3-019, FR-P3-021, FR-P3-030, FR-P3-031) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-012 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 22 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Not specified in the source documents (DOR-RWB-P3-E2012-OPS-1)**, I want **the manual transfer path of rwb-case deployed from the service template with its Helm values and the rwb-case login, its consumer groups with retry and `.dlt` paths, its Temporal worker and the activity timeouts of the transfer decision, its readiness signal, the four capability metrics, the dashboards, the alerts and a runbook entry for each failure**, so that **an operator can see within minutes that a manual move is failing, being refused or breaching its two-second budget, and repair it without reading code or waiting for a business report**.

This story deploys an existing capability. It adds no topic, no endpoint, no table and no Schedule: the manual move is `POST /api/recovery/case/v1/cases/{caseId}/transfer` over `ManualTransferWorkflow` on task queue `rwb-case`, its rule answer comes from the embedded Drools kit through `EvaluateRules`, and its evidence is the local decision record published on `rwb.decision-record.v1`.

### 2. Business rationale

A manual move is the only write on the case that a person starts and then waits for. In the monolith a refusal was a line in a log and a bulk selection was a loop in a page; in the target the answer is a status and a message ID inside two seconds, and a refusal that nobody counts looks exactly like a quiet day. The operator therefore needs three signals that do not exist in a table: the rate of moves, the rate of refusals split by code, and the share of calls that breach the two-second budget.

The capability also depends on three other services for its correctness — rwb-access for the right, rwb-deviation for the deviation that decides the refusal of a rule, and rwb-decision for the package version — and none of them fails the screen when it is slow: the move is refused and nothing changes. That is the right behaviour for the officer and the wrong behaviour for the operator if nobody counts it, which is why the refusal rate by code and the budget breaches are dashboard series and alerts here rather than a line in a log.

Deployment is part of the capability: the chart carries the rwb-case login and no other credential (DP-02), the migration job runs the per-service Flyway sequence in schema `rwb_case` (DP-15), the two consumer groups the case service already holds are provisioned with their retry and `.dlt` paths so a deviation pause and a package version are never lost (DP-09), the worker registers the two activities with the retry policy the Temporal and Drools design fixes (DP-10), and the runbook names the four failures an operator will actually see.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace are available (RWB-PLT-WF, RWB-PLT-E1071-CON), so the worker polls `rwb-case` and `ManualTransferWorkflow` runs in every environment.
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and `rwb.case.events.v1`, `rwb.decision-record.v1`, `rwb.deviation.events.v1` and `rwb.decision.events.v1` are provisioned by their owners.
- The observability stack of the platform is available (RWB-PLT-OBS, ADR-023): metrics, traces and logs with one trace across REST, Kafka and Temporal.
- The three environments DEV, SIT and UAT exist with their parameter scope and their Kafka and Temporal endpoints.
- RWB-P3-E2012-CON is published, so the smoke profile and the drift test run against the transfer operation and its five fakes.
- LOV-TRANSFER-REASON and the queue and member rows are loaded by their owning stories; this story reads them and holds no copy.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds one image and one chart version from the same commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys rwb-case with the rwb-case login, the pre-deploy migration job for schema `rwb_case`, the readiness and liveness probes, the api deployment that serves the transfer operation and the worker deployment that polls `rwb-case`.
3. The provisioning step declares the consumer groups the case service already holds — `rwb-case` on `rwb.deviation.events.v1` for DeviationRaised and DeviationCleared, and `rwb-case` on `rwb.decision.events.v1` for RulePackageInForce — each with its retry topic and its `.dlt` topic; it creates no topic and no consumer group for the manual path, because a manual move subscribes to nothing.
4. The provisioning step asserts that `rwb.case.events.v1` carries `rwb.case.CaseTransferred.v1` with its retry and `.dlt` topics, that `rwb.decision-record.v1` is used as its owner provisions it, and that no Schedule, task queue or job is created for a manual move.
5. The worker registers `ManualTransferWorkflow`, `EvaluateRules` and `RecordAndApply` on `rwb-case`, with the retry policy of 1 s, back-off 2 and 10 attempts, `NoPackageInForce` non-retryable, and the activity timeouts of the values files.
6. The readiness probe answers healthy only when the schema is at the expected version, the outbox relay runs, the worker has polled `rwb-case` and the reference-data version of LOV-TRANSFER-REASON is readable; the liveness probe answers healthy when the process and its internal loop are up.
7. The dashboards are published: the move rate, the refusal rate by message ID, the at-cap hits, the 2 s budget breaches, the workspace of the three downstreams, the `.dlt` depth and the outbox lag.
8. The alerts are wired to the message IDs of section 14 and to the runbook entries of section 13; the thresholds are values and carry the placeholder of section 14 until they are confirmed.
9. A smoke step opens SCR-05 through gateway-bff in the SIT profile, moves one synthetic case and one selection of two, and asserts the answer inside two seconds with the record on the topic.
10. The runbook is published and reviewed with the on-call rota: a refusal that is not an incident, a downstream that does not answer, a dead-letter backlog and a worker that stopped polling.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job fails | The deployment stays unready and the pipeline stops; no traffic reaches the new version | None | AC1 |
| X2 | A consumer group is provisioned without its retry or `.dlt` topic | The provisioning step fails the release and the consumer refuses to start | None | AC3 |
| X3 | The worker crash-loops on the task queue | The rollout is held by the readiness gate, the previous worker keeps polling and the restart alert fires | None | AC4, AC6 |
| X4 | A manual move breaches the 2 s budget on a share of calls | The budget-breach alert fires with the downstream that spent the time and the runbook entry for a slow downstream opens | MSG-GEN-006 | AC5, AC6 |
| X5 | A downstream does not answer at all and every move is refused | The refusal-rate alert fires with the code count and the runbook entry for a downstream that is down names its owner | MSG-GEN-006 | AC5, AC6 |
| X6 | The `.dlt` topic of `rwb.case.events.v1` or of an inbound topic grows | The dead-letter alert fires on rate and depth and the runbook gives the drain and replay steps | None | AC6 |
| X7 | No TRANSFER version is in force in SIT | `NoPackageInForce` is non-retryable, the count rises under MSG-P3-027 and no page is sent | MSG-P3-027 | AC5 |
| X8 | A release declares a new topic or a Schedule for a manual move | The pipeline fails the retired-element check of AC3 | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform provisioning, the workflow kit and the observability stack; builds no application code |
| Negotiable | Replica counts, resource sizes, activity timeouts and alert thresholds are environment values, not story decisions |
| Valuable | Makes a write path that a person waits on observable: rate, refusals by code, cap hits, budget breaches and dead letters each have a signal and an owner |
| Estimable | One chart, one pipeline stage, one migration job, two probes, two consumer groups, eight dashboard series, five alert rules and four runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the groups exist, the series answer, the alerts fire on a synthetic metric, the runbook entry resolves |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the manual transfer path of rwb-case

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT
    Given the contract baseline of RWB-P3-E2012-CON version 1 is published

  Scenario: AC1 The Helm chart and values deploy the path with the rwb-case login (new, D-RCV-60)
    Given the rwb-case Helm chart with its values-dev.yaml, values-sit.yaml and values-uat.yaml
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the rwb-case login reference and no other service's credential
    Then the manual-transfer block renders the operation, the workflow ManualTransferWorkflow, the task queue rwb-case and the feature switch rwb.p3.manual-transfer
    Then the migration job runs the per-service Flyway sequence in schema rwb_case before the deployment is marked ready and adds only the read-side index of the app story
    Then no replica count, resource size, timeout, threshold or cadence is hard-coded in the template

  Scenario: AC2 The pipeline promotes one artefact and runs the contract tests (new, D-RCV-60)
    Given a commit on the main line
    When the pipeline runs
    Then it builds one image and one chart version from the same commit
    Then it runs the unit, component and contract tests of RWB-P3-E2012-CON and fails the build on a drift between a fake and the document
    Then it scans the image and the dependencies and fails on a critical finding
    Then it promotes the same artefact through DEV, SIT and UAT without a rebuild

  Scenario: AC3 The consumer groups and the dead-letter paths are provisioned (new, D-RCV-60)
    Given the provisioning step of rwb-case for this capability
    When it runs against the environment
    Then the consumer group rwb-case subscribes to rwb.deviation.events.v1 for DeviationRaised and DeviationCleared with the inbox of schema rwb_case
    Then the consumer group rwb-case subscribes to rwb.decision.events.v1 for RulePackageInForce with the same inbox
    Then each subscription has its retry topic and its .dlt topic and the consumer never acknowledges an event it could not process
    Then rwb.case.CaseTransferred.v1 is produced on the existing rwb.case.events.v1 with its retry and .dlt topics and rwb.decision-record.v1 is used as its owner provisions it
    Then no new topic and no new consumer group is created for a manual move and no Schedule is registered
    Then the provisioning step fails the release when a retry or .dlt topic is missing or when a new topic is declared

  Scenario: AC4 The worker, the activity timeouts and the readiness signal (new, D-RCV-60)
    Given the rendered worker configuration and the probes
    When the activity options of the transfer decision are read
    Then the retry policy states 1 s initial interval, back-off 2 and 10 attempts
    Then NoPackageInForce is listed as non-retryable
    Then each activity carries its start-to-close and schedule-to-close value from the values file, with the provisional default recorded in section 14
    Then the worker is registered on task queue rwb-case in namespace rwb-recovery with the build ID of the release
    Then the readiness probe answers healthy only when the schema version, the outbox relay, the worker poller and the reason-list version are all present, and neither probe calls another service

  Scenario: AC5 The four capability series answer on a synthetic day (new, D-RCV-60)
    Given the published metrics of the capability
    When a synthetic day is replayed with 40 moves, 12 refusals across five message IDs, 6 at-cap hits and 2 budget breaches
    Then the move rate answers as a count and a latency histogram per environment and business date
    Then the refusal rate answers by message ID and by rule ID, and a refusal is counted and never pages the on-call rota on its own
    Then the at-cap hits answer by queue and by owner count, and the budget breaches answer with the downstream that spent the time
    Then the .dlt depth, the outbox lag and the worker poller are on the same dashboard
    Then no series carries a customer name, an account number or a personal identifier

  Scenario: AC6 The alerts and the runbook cover the four operator failures (new, D-RCV-60)
    Given the five alert rules and the published runbook
    When the move rate leaves its band, the refusal rate by code passes its value, the budget breaches pass their share and a .dlt topic grows
    Then each condition raises its alert with its message ID where one applies, its environment and its links to the case and the workflow
    Then the runbook holds one entry each for a refusal that is not an incident, a downstream that does not answer, a dead-letter backlog and a worker that stopped polling, with the check, the owner role and the recovery step
    Then every alert links exactly one runbook entry and every entry names the escalation path when the step fails

  Scenario: AC7 Every business rule BR1 to BR10 is carried by a criterion and a test case (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8 are in force
    When the story is verified against its test cases
    Then each rule BR1 to BR10 is carried by a criterion and a test case, or by a guardrail or boundary test

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given the case status model of rwb-case is in force
    When a manual transfer or reassignment submits a status change that the model does not allow
    Then the change is refused with its reason and no state is written
    Then no CaseTransferred event is produced on rwb.case.events.v1 and nothing is written to the outbox
    Then the refusal is counted in the refusal rate by message ID and never pages the on-call rota on its own
```

These six criteria are new for the deployment and test artefacts only; they restate no business outcome owned by RWB-P3-E2012-APP and no element owned by RWB-P3-E2012-CON.

AC7: Every business rule BR1 to BR10 in section 8 is carried by a criterion and a test case, or by a guardrail or boundary test (NEWAC-RWB-P3-E2012-OPS-AC7).

### 8. Business rules

| ID | Rule | Source | Test cases |
|---|---|---|---|
| BR1 | One service, one schema, one login: the release uses the rwb-case login and no other service's credential | DP-02; Architecture v5 slide 29 | TC-P3-E2012-OPS-01 |
| BR2 | The migration is a per-service Flyway sequence in schema rwb_case and runs before the deployment is ready | DP-15; RWB-PLT-E1044-CON | TC-P3-E2012-OPS-01 |
| BR3 | Every subscription has a retry topic and a `.dlt` topic, and a consumer never acknowledges an event it could not process | DP-09; Architecture v5 slide 22 | TC-P3-E2012-OPS-03 |
| BR4 | A manual move creates no topic, no consumer group and no Schedule: it is a REST call that starts a workflow | DP-10, DP-14; Template and Rules §R5.5 | TC-P3-E2012-OPS-03 |
| BR5 | The retry policy of the transfer decision is 1 s initial interval, back-off 2 and 10 attempts, with `NoPackageInForce` non-retryable | Temporal and Drools design slide 14 | TC-P3-E2012-OPS-04 |
| BR6 | No environment value is hard-coded: replica counts, resource sizes, activity timeouts and alert thresholds come from the values files | Template and Rules §R7.2 s17 | TC-P3-E2012-OPS-04 |
| BR7 | An alert carries a message ID where the condition maps to one, and links exactly one runbook entry | Template and Rules §R7.2 s14 | TC-P3-E2012-OPS-06 |
| BR8 | A refusal is a business answer and never pages the on-call rota on its own; only a rate, a breach or a backlog pages | MSG-P3-001, MSG-P3-002, MSG-P3-005, MSG-P3-033, MSG-P3-035 | TC-P3-E2012-OPS-05 |
| BR9 | The readiness signal reads the schema version, the outbox relay, the worker poller and the reference-data version in force, and calls no other service | Architecture v5 slide 28; DP-07 | TC-P3-E2012-OPS-04 |
| BR10 | No dashboard series, log line or alert payload carries personal data; case IDs, workflow IDs, staff user IDs, message IDs, counts and durations only | Template and Rules §R7.2 s17 | TC-P3-E2012-OPS-05 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration complete and probes healthy | The schema is at the expected version, the outbox relay runs and the worker polls | Ready |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is the new one | Ready |
| Ready | Migration job failed | The schema is not at the expected version | Failed |
| Failed | Rollback | The previous chart version is redeployed and the migration is reversed by its own script | Ready |
| Ready | The feature switch is turned off | A change record names the switch `rwb.p3.manual-transfer` | Ready, capability inert |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning step, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the topic provisioning and the visibility queries behind the stuck workflow scan |
| ACE database administrator | Owns schema rwb_case, the login and its grants, and approves the migration job |
| Release manager | Approves the promotion of one artefact through the environments and the switch-on of the capability |
| On-call operator | Runs the runbook entries and opens an incident when a budget breach, a refusal rate or a dead-letter backlog persists |
| RW-PLATADM | Reads and operates the case and its queues in the running service, not in the cluster |
| Service owner of rwb-access, rwb-deviation and rwb-decision | Is paged by the refusal-rate alert when the code names its contract, and owns the repair beyond the rwb-case breaker |

The per-service login used by the chart is a secret reference resolved at deploy time; the chart references "the rwb-case login (DP-02)" and never a literal name.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switch `rwb.p3.manual-transfer`, the two client timeouts, the activity timeouts, the alert thresholds | Not specified in the source documents (DOR-RWB-P3-E2012-OPS-7) |
| Schema | rwb_case, migrated by the per-service Flyway sequence; the tables `recovery_case`, `assignment`, `queue` and `queue_member` with the library objects | Not specified in the source documents (DOR-RWB-P3-E2012-OPS-7) |
| Topics | `rwb.deviation.events.v1` and `rwb.decision.events.v1` subscribed with retry and `.dlt`; `rwb.case.events.v1` carries `rwb.case.CaseTransferred.v1`; `rwb.decision-record.v1` used as its owner provisions it | Not specified in the source documents (DOR-RWB-P3-E2012-OPS-7) |
| Queue | Temporal task queue `rwb-case` in namespace `rwb-recovery` | Not specified in the source documents (DOR-RWB-P3-E2012-OPS-7) |
| Schedules | None for this capability; a manual move registers nothing | Not specified in the source documents (DOR-RWB-P3-E2012-OPS-7) |
| Dashboard series | move rate, move latency, refusal rate by message ID, refusal rate by rule ID, at-cap hits by queue and owner count, 2 s budget breaches with the downstream, downstream timeouts, `.dlt` depth, outbox lag, worker poller count | Not specified in the source documents (DOR-RWB-P3-E2012-OPS-7) |
| Runbook entries | a refusal that is not an incident, a downstream that does not answer, a dead-letter backlog, a worker that stopped polling | Not specified in the source documents (DOR-RWB-P3-E2012-OPS-7) |
| Secrets | The rwb-case login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store | Not specified in the source documents (DOR-RWB-P3-E2012-OPS-7) |

The activity timeouts and the alert values are deployment values; the provisional values and their confirmation are carried by the gap and the assumption of section 14 (GAP-0713; ASM-1260). The exact cluster topology, node pools, replica counts and probe timings are deployment values of the platform chart and are not fixed here.

The deviation table gets no new column in this story; the data-owner confirmation that the deviation row needs nothing more is Not specified in the source documents (GAP-3096).

### 12. Contract

The contract version the build targets is Not specified in the source documents (DOR-RWB-P3-E2012-OPS-23); the operations use the /v1 path.

#### 12.1 REST operations provided

The deployment exposes one operation of RWB-P3-E2012-CON: `POST /api/recovery/case/v1/cases/{caseId}/transfer`, single and per case in a selection, `Idempotency-Key` required, behind gateway-bff. Owner rwb-case (P3). The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and scope answer before the handler; 2 s client budget and a breaker, cached per request |
| GET | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The open deviations that decide a refusal; 2 s client budget and a breaker |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | P7 rwb-decision | The TRANSFER model the kit fetches and verifies; 2 s client budget and a breaker |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, own contract (RWB-P3-E1043-CON, ASM-0041) | The reason list in force; read at start-up by the readiness signal and per form load |

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.case.CaseTransferred.v1` (event 04) | `rwb.case.events.v1` | The topic, its retry topic and its `.dlt` topic already exist for rwb-case; the deployment reuses them and creates no new topic |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | Shared topic owned by the platform and rwb-decision; reused, not recreated |

#### 12.4 Events consumed

| Event | Topic | Provisioning | Owner |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | Consumer group `rwb-case` with the inbox of schema rwb_case; retry and `.dlt` configured in the same step | `rwb-case` (consumer) |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | Same consumer group, same retry and `.dlt` path | `rwb-case` (consumer) |
| `rwb.decision.RulePackageInForce.v1` (event 30) | `rwb.decision.events.v1` | Consumer group `rwb-case`, already provisioned for the case capability and reused here for the model swap | `rwb-case` (consumer) |

The manual path itself subscribes to nothing; these three subscriptions are the case service's and are listed because the deviation flag and the package version the move depends on arrive through them.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| Transfer activity (no ManualTransferWorkflow in Temporal Catalog v1) | Activity called by CaseWorkflow, one execution per manual request, carries the case ID and the idempotency key | `rwb-case` | Worker deployment with the build ID of the release; the latency the budget-break series is computed from |
| `EvaluateRules` | Activity, from the workflow kit | `rwb-case` | Registered by the same worker; the timeout and the non-retryable `NoPackageInForce` are its values |
| `RecordAndApply` | Activity, from the workflow kit | `rwb-case` | Registered by the same worker; the outbox lag and the record write share its transaction |
| `CaseWorkflow` | Workflow, parent, one per case; workflow ID is the case ID (Temporal design slide 13; ADR-011 writes `case-{caseId}`, see GAP-0148); started by signalWithStart from the case router on the case event; duplicate-start policy Not specified in the source documents (CG-ALL-4152) | `rwb-case` | Not changed by this release; it keeps polling on the same queue |

#### 12.6 Schedules

None. The deployment registers no Schedule and no cron entry for a manual move, because a move is started by a person through the operation. The 06:30 rebalancing Schedule and the morning allocation belong to the case service and are not registered by this release; the platform's stuck workflow scan runs as a visibility query and is not registered here either.

#### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| recovery_case, assignment, queue, queue_member | P3 (rwb_case) | Created and migrated by the per-service Flyway sequence in the migration job; the app story's read-side index is the only change |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Created by the same migration job; used by the outbox relay, the three consumer groups and the stored idempotent response |

`deviation` belongs to S8 and `decision_log_entry` to P7; the migration job touches schema `rwb_case` only (DP-01).

#### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| rwb-access WireMock | Runs in the pipeline and in the SIT smoke profile, including a granted right, a refusal and the no-delegation answer |
| rwb-deviation WireMock | Same, including an open deviation, an empty answer and a delayed answer beyond 2 s |
| rwb-decision WireMock | Same, including the TRANSFER model "TRF-2026.12", a wrong checksum and the catalog answer for R-UNI-18 |
| Drools stub | Same, including the refusing row "TRF-010" and `NoPackageInForce` |
| rwb-case reference-data stub | Same, including LOV-TRANSFER-REASON with R01 to R06 |

The fakes are test-only workloads; they are not deployed into UAT or production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed in the deployment path | The transfer operation; authorise, deviations, the rule model and the own reference data; one hop and 2 s for the three of another owner |
| Kafka | 2 published by their owners, 3 consumed | CaseTransferred and DecisionRecorded reused; DeviationRaised, DeviationCleared and RulePackageInForce consumed with retry and `.dlt` |
| Temporal | 1 workflow, 2 activities, no Schedule | `ManualTransferWorkflow` with `EvaluateRules` and `RecordAndApply` |
| File | None | The release reads no runtime file; values files are build inputs |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-case/` | Chart with api and worker deployments, service, migration job, config map, secret references and probes; no Schedule hook for this capability |
| `helm/rwb-case/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, `rwb.p3.manual-transfer`, the two client timeouts, the two activity timeouts, the alert thresholds |
| Pipeline stage | Build, unit, component and contract tests, retired-element check, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Consumer group `rwb-case` on `rwb.deviation.events.v1` and on `rwb.decision.events.v1` with retry and `.dlt`; reuse of `rwb.case.events.v1` and `rwb.decision-record.v1`; task queue `rwb-case` in namespace `rwb-recovery` |
| Dashboards | Eight series: move rate, move latency, refusal rate by message ID, refusal rate by rule ID, at-cap hits, 2 s budget breaches, `.dlt` depth, outbox lag and worker pollers |
| Alerts | Five rules, each with a message ID where one applies and one runbook entry |
| Runbook | Four entries: a refusal that is not an incident, a downstream that does not answer, a dead-letter backlog, a worker that stopped polling |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the outbox relay is running, the Temporal worker on `rwb-case` has polled and the reference-data version of LOV-TRANSFER-REASON is readable. Liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database and neither calls another service.

**Metric definitions.**

| Series | Definition | Alert value |
|---|---|---|
| Move rate | Count of 200 answers of the operation per environment and business date | Leaves its band in either direction (GAP-0713; ASM-1260) |
| Move latency | Histogram from the request to the answer, with the share above 2 s | Breach share (GAP-0713; ASM-1260) |
| Refusal rate by message ID | Count of 403, 404, 409, 422 and 503 answers grouped by `messageId` | Rate per code (GAP-0713; ASM-1260) |
| Refusal rate by rule ID | Count of MSG-P3-033 answers grouped by `RuleResult.ruleId` | Reported, not paged |
| At-cap hits | Count of MSG-P3-002 answers by target queue, with one and with every owner at the cap | Rate (GAP-0713; ASM-1260) |
| Budget breaches | Count of answers or workflow executions above 2 s, with the downstream that spent the time | Share (GAP-0713; ASM-1260) |
| `.dlt` depth | Depth and rate of each dead-letter topic the capability touches | Depth or rate (GAP-0713; ASM-1260) |
| Outbox lag | Age of the oldest unpublished outbox row | Age (GAP-0713; ASM-1260) |

**Alert mapping.**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written and 503 answers rise | Record-write alert with the store state and the environment | Platform on-call, page |
| MSG-P3-027 | No TRANSFER version is in force and 422 answers rise under that code | Package-in-force alert naming the package and the business date | Platform on-call, ticket to the rwb-decision owner |
| MSG-P3-002 | At-cap hits pass their rate on one queue | Capacity alert with the queue and the owner count; never a page on a single hit | Ticket to the team manager's queue owner |
| MSG-GEN-006 | Budget breaches pass their share, or a downstream times out | Degradation alert naming the downstream and the breaker state | Platform on-call, ticket to the downstream owner |
| None | The `.dlt` depth or the outbox lag passes its value, or the worker poller count falls to zero | Pipeline alert with the topic, the lag and the build ID | Platform on-call, page |

Every alert carries its message ID where the condition maps to one, and the last condition carries the topic or the series name instead. Every threshold is a deployment value with a provisional default; the missing source is carried by the gap and the assumption of section 14 (GAP-0713; ASM-1260).

**Runbook entries.**

| Entry | When it opens | Check | Owner role | Recovery step |
|---|---|---|---|---|
| A refusal is not an incident | A refusal rate rises and the codes are business answers | Read the code counts and the rule IDs; compare with the queue caps and the legal holds | On-call operator | Confirm with the team manager, close without a change |
| A downstream does not answer | The budget breaches pass their share, or the authorise or deviation call times out and every move is refused | Check the breaker state, the downstream's own health and the client budget | Platform on-call, then the downstream owner | Restore the downstream; nothing is replayed, because a refused move changed nothing |
| A dead-letter backlog | A `.dlt` depth or rate passes its value | Read the topic, the failure reason and the affected case IDs | Platform on-call | Fix the cause, replay in order, verify the inbox has no duplicate |
| A worker that stopped polling | The poller count is zero or the workflow executions pile up | Read the build ID, the restart count and the task queue | Platform on-call | Roll back to the previous build ID or restart the worker; no case is left half-moved |

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact and fails on a fake drift or a retired element, the two consumer groups exist with their retry and `.dlt` paths, the eight series carry the synthetic day, the five alert conditions fire on synthetic metrics, the four runbook entries are reviewed by the on-call rota, and one manual move and one selection of two are observed in SIT with the record on the topic.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | No reason code, or a code not in the list in force | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner, or every owner of the target queue, at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Case closed or under a legal hold | This case cannot move to {state} from {current}. |
| MSG-P3-027 | No TRANSFER package version in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-033 | A TRANSFER rule refuses the move | Rule {rule} does not allow this transfer. |
| MSG-P3-035 | A selection with refusals | {done} of {total} cases were moved. The others show the reason on their row. |
| MSG-GEN-004 | Two moves of one case at once | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | A downstream does not answer inside the budget | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A caller without Queue and allocation U | You cannot {action} here. Your role does not include it. |

The message texts are copied unchanged from the legacy story and the contract; the deployment adds the routing, the threshold and the runbook link, never a new wording. For MSG-GEN-006 the {system} value is the name of the downstream that did not answer, and the message is shown on the screen only where a retry remains possible; a refused move is not queued.

SCR-05 states: the empty, loading, error and no access states of SCR-05 are Not specified in the source documents (DOR-RWB-P3-E2012-OPS-10; CG-ALL-4156).

The transfer decision code is Not specified in the source documents (GAP-2500). The text of MSG-P7-009 and the text of REQ-CWC-010 are Not specified in the source documents (GAP-2500). When no TRANSFER package version is in force, the version list answers with the finding and MSG-P3-027. The decision-log page-size guard is Not specified in the source documents (GAP-2500). The login for decision-log reads is Not specified in the source documents (GAP-2500); BR1 permits no other service's credential.

The activity timeouts and the alert thresholds are Not specified in the source documents (GAP-0713; ASM-1260). The provisional defaults are a start-to-close of 10 s and a schedule-to-close of 60 s for each of the two activities, a budget-breach share of 1 per cent of calls, a refusal-rate value per message ID agreed with the service owner, an at-cap rate value per queue and a `.dlt` depth of 1; each is a value in the values file and each is confirmed with the service owner before the capability is switched on in UAT.

### 15. Screens and states

The deployment serves SCR-05 Transfer case in its Form, At cap warning, Refused and Saved states behind the gateway-bff composite route (DP-19). The empty, loading, error and no access states of SCR-05 are Not specified in the source documents (CG-ALL-4156). The operator-facing surfaces of this story are the pipeline run view, the release view, the eight dashboard series and the runbook; the smoke step opens SCR-05 for a synthetic case in SIT and asserts that one move and one selection of two answer inside the two-second budget with the record on the topic.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2012-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with a pinned digest, the rwb-case login reference, the manual-transfer block and the migration job |
| TC-P3-E2012-OPS-02 | AC2 | NFR | One pipeline run produces one image and one chart version and fails on a fake drift or a critical scan finding |
| TC-P3-E2012-OPS-03 | AC3 | NFR | The two `rwb-case` consumer groups with retry and `.dlt`; a missing `.dlt` or a new topic fails the release |
| TC-P3-E2012-OPS-04 | AC4 | NFR | The retry policy, the non-retryable `NoPackageInForce`, the activity timeouts and the readiness gate on a synthetic environment |
| TC-P3-E2012-OPS-05 | AC5 | NFR | A synthetic day with 40 moves, 12 refusals across five message IDs, 6 at-cap hits and 2 budget breaches; eight series populated |
| TC-P3-E2012-OPS-06 | AC6 | NFR | Five synthetic conditions raise their alerts and resolve one runbook entry each, with the message ID and the escalation path |
| TC-P3-E2012-OPS-07 | §12 operations, events and activities | Contract | Contract test of the operations, events and activities of section 12 against the published contract version |
| TC-P3-E2012-OPS-08 | §12.7 table boundaries (ASM-3438) | NFR | Boundary values of each table of section 12.7 |
| TC-P3-E2012-OPS-09 | AC7 | Not specified in the source documents (NEWAC-RWB-P3-E2012-OPS-AC7) | Not specified in the source documents (NEWAC-RWB-P3-E2012-OPS-AC7) |
| TC-P3-E2012-OPS-10 | AC8 | NFR | A status change the model does not allow is submitted and refused; no CaseTransferred event and no outbox write |

### 17. Guardrails

- No business value in a values file: the reason codes, the caps, the rule IDs and the package version are reference data held by their owner, never a deployment value.
- No personal data in logs, dashboard series, alert payloads or the runbook: case IDs, workflow IDs, staff user IDs, message IDs, counts and durations only.
- One login per service; the chart carries the rwb-case login reference and no other service's credential (DP-02).
- The service writes only schema rwb_case; the migration job never touches another schema and no dashboard query reads one (DP-01).
- Every subscription has a retry topic and a `.dlt` topic, and the consumer dedupes through the inbox (DP-09).
- No new topic and no Schedule for a manual move: the capability reuses `rwb.case.events.v1`, `rwb.decision-record.v1`, `rwb.deviation.events.v1` and `rwb.decision.events.v1` (DP-10, DP-14).
- ACE data is read only through the owner's contract or the `v_ace_*` views; no dashboard reads an ACE view or another service's schema.
- The release pins the image digest and the chart version, and no secret is written into a values file, a chart template, a dashboard or the runbook.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-WKM-003 | A manual move only with a reason code from the agreed list | The reference-data readiness check, the MSG-P3-001 refusal series and the runbook entry for a refusal that is not an incident | TC-P3-E2012-OPS-04, TC-P3-E2012-OPS-05 |
| REQ-WKM-007 | An absent or over-cap owner's cases reallocated inside the team, keeping the state and the clocks | The at-cap series by queue and owner count, the MSG-P3-002 alert and the capacity runbook route | TC-P3-E2012-OPS-05, TC-P3-E2012-OPS-06 |
| REQ-WKM-008 | Queue and transfer history visible on the case | The `CaseTransferred.v1` production with retry and `.dlt` and the outbox-lag series | TC-P3-E2012-OPS-03, TC-P3-E2012-OPS-05, TC-P3-E2012-OPS-08 |
| REQ-CWC-010 | Manual request with a reason code, beside the rule-driven triggers | The operation, the worker and the retry policy of the transfer decision | TC-P3-E2012-OPS-01, TC-P3-E2012-OPS-04, TC-P3-E2012-OPS-07 |
| REQ-CWC-016 | Every transfer logged with the rule ID and the rule version | The decision-record publication and the record-write alert | TC-P3-E2012-OPS-02, TC-P3-E2012-OPS-06 |
| ADR-017 | Embedded Drools per service; the registry in rwb-decision | The `RulePackageInForce` consumer group, the model-swap path and the package-in-force alert | TC-P3-E2012-OPS-03, TC-P3-E2012-OPS-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The client budgets, the budget-breach series and the degradation runbook entry | TC-P3-E2012-OPS-04, TC-P3-E2012-OPS-05, TC-P3-E2012-OPS-06 |
| ADR-022 | Local decision record plus central ledger | The record topic reuse and the outbox-lag series | TC-P3-E2012-OPS-03 |

### 19. Out of scope

- The manual path, the pre-checks, the cap check, the bulk runner and the screen (RWB-P3-E2012-APP).
- The contract documents, the schemas and the fakes as published artefacts (RWB-P3-E2012-CON); this story only deploys the test copies.
- The transfer baseline and the rule-driven triggers (RWB-P3-E1021-CON, RWB-P3-E1021-APP).
- The platform topic provisioning, the Temporal cluster and the observability stack (the platform epics RWB-PLT-EVT, RWB-PLT-WF and RWB-PLT-OBS).
- The stuck workflow scan itself and the six-monthly access review.
- The rwb_case schema design and the logical model (the database stories of the service epic).
- Data migration from the legacy schema and the reconciliation run.
- The cross-service journey harness and its evidence (RWB-ITG-E2012-ITG).
