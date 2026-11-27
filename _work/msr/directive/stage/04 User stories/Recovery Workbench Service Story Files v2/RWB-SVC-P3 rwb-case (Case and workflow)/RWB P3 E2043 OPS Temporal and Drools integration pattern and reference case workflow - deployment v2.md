# RWB-P3-E2043-OPS Temporal and Drools integration pattern and reference case workflow

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2043-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-043 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement; not sized in this story |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP14, DP15, DP19 |
| Parallel lane | L-P3-AQ |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2043-CON (build status Not started) |
| Contract version | v1 (the /v1 path the story builds against) |
| Screens | Not applicable to this story: SCR-44 is an interface and job monitor in FSD P1 Recovery data engine v4 (03 Requirements and specifications). Empty, loading, error and no-access states are not specified in the source documents (DOR-RWB-P3-E2043-OPS-10) |
| Outbox retry check | Recorded choice (GAP-0422): the retry is asserted through the absence of the effect and the same event key on rwb.case.events.v1. No rwb-case outbox delivery read is added to the rwb-case contract; the ownership map holds none (GAP-0422) |
| Harness repository and SIT environment | Not specified in the source documents (GAP-0422): harness repository, SIT environment, seeding set and script, evidence format and retention, pass or fail gate |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-030) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-043 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (10 resolved, 27 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the rwb-case worker deployed on task queue `rwb-case` with a pinned build ID and worker versioning, the reference workflow deployed in DEV and SIT only behind `rwb.p3.temporal`, the replay gate as a pipeline step before promotion, the stuck-workflow scan, the five dashboard series and the runbook with its alerts**, so that **the reference pattern of RWB-E2-043 is deployed, proved on recorded histories and operable by a rota before any Epic 3 squad copies it**.

### 2. Business rationale

The legacy story assumes a worker and a reference workflow exist and that someone will read the Temporal Web UI when a run fails. In the target the worker is part of the service release, its build ID is what makes an in-flight history replayable after a deploy, and the replay gate is a release step rather than a manual check (Temporal and Drools design slide 27). Without this story the app story can pass its unit tests while a new build silently breaks the histories of running cases, and a failed signal has no owner because nothing raises it.

Deployment is also where the test-only scope is enforced. The skeleton is a reference, not a capability of production: it is deployed to DEV and SIT, never to UAT or production, it starts no production case, and it owns no Schedule. Its task queue is `rwb-case` in namespace `rwb-recovery`, the queue of the owning service, and the legacy queue `rwb-platform` is not part of the release (Arch v5 slides 24 and 41).

The observability follows ADR-023 per service: five series (workflow failures, signal failures, activity retries, NoPackageInForce count, replay results), the stuck-workflow scan of the platform (JOB-21), three alerts and three runbook entries. Every alert carries a message ID and one runbook entry, so an operator acts without reading code.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit and the `rwb-recovery` namespace exist, with worker versioning and the build ID provider (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provides the topic `rwb.case.events.v1` with its retry topic and `.dlt` topic, and the shared topic `rwb.decision-record.v1` (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The platform error envelope and the message catalogue are in force, so an alert can carry a message ID.
- The three environments DEV, SIT and UAT exist; the reference deployment is limited to DEV and SIT, and a production namespace is not a target of this story.
- The replay gate mechanism of RWB-E2-040 is available as a pipeline step or as a runnable job of the workflow kit.
- The codec server and the payload codec are in force, with the keys of the namespace (RWB-PLT-WF).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the rwb-case worker with its own login, the namespace `rwb-recovery`, the task queue `rwb-case`, the payload codec and the build ID of the release.
3. The worker registration step confirms that the worker polls `rwb-case` only, that the two activities and the reference workflow are registered, and that a second task queue is not polled.
4. The flag step sets `rwb.p3.temporal` from the values of the environment: on in DEV and SIT, absent everywhere else; the release refuses a value for an environment outside the two.
5. The replay gate step replays the recorded reference histories against the new build and the new contract jar, and reports the result; a failure stops the promotion.
6. The stuck-workflow scan of the platform (JOB-21) runs every five minutes and reports a workflow that waits on a non-retryable failure or that has made no progress.
7. The dashboards are published with the five series and the release and build ID as dimensions.
8. The three alerts are wired to MSG-P3-036, MSG-P3-027 and MSG-P3-038 and to their runbook entries.
9. A smoke step starts "ref-case-RW-2026-000777" with a synthetic input in DEV and checks that the workflow completes, that the history is encrypted and that the build ID is the released one.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job or the chart render fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1 |
| X2 | The worker polls a task queue other than `rwb-case` | The registration check fails the release, because a second queue would take work away from its owner | None | AC2 |
| X3 | The flag is set for an environment other than DEV or SIT | The release is refused before the chart is applied | None | AC3 |
| X4 | A recorded history does not replay against the new build | The replay gate fails and the artefact is not promoted; the previous build stays in force | MSG-P3-038 | AC4 |
| X5 | No package version is in force for the reference | The workflow fails at once without retry; the scan reports it and the count is on the dashboard | MSG-P3-027 | AC5 |
| X6 | The Temporal frontend is unreachable when the relay signals | The delivery stays PENDING or RETRYING; the signal-failure series rises and the backlog alert fires | MSG-P3-036 | AC5, AC6 |
| X7 | The worker stops while a workflow is running | The task stays on the queue, the worker returns and the workflow resumes from history; the runbook entry names the check | None | AC6 |
| X8 | A build is promoted while an old build still has open workflows | The old build drains; a new workflow goes to the new build; the dashboards show both build IDs | None | AC1, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit and the platform topic provisioning; no application code is built here |
| Negotiable | Replica counts, resource sizes, alert thresholds and scan intervals are environment values, not story decisions |
| Valuable | Makes the reference pattern deployable, replay-safe and operable before Epic 3 copies it |
| Estimable | One chart, one registration check, one flag step, one replay gate step, five series, three alerts and three runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the worker registers, the gate fails a bad build, the alerts fire on a synthetic metric |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the reference case workflow and the replay gate for rwb-case

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-case is rwb-case
    Given the target environment is SIT
    Given the synthetic case RW-2026-000777 is a JSON seed in the test resources, loaded and removed per run in DEV and SIT only and carried by no release

  Scenario: AC1 The worker is deployed with a pinned build ID and worker versioning (new, D-RCV-60)
    Given the rwb-case chart and its values files
    When the chart is rendered for DEV and SIT
    Then each render succeeds with the chart version and the image digest pinned
    Then the worker deployment polls only the task queue rwb-case in namespace rwb-recovery
    Then the worker carries the build ID of the release and worker versioning is enabled
    Then the release declares the rwb-case login and no other service's credential
    Then a new workflow goes to the new build while the old build drains its open workflows

  Scenario: AC2 The worker registers the two activities and the reference workflow (new, D-RCV-60)
    Given a running rwb-case worker
    When the registration step asks the namespace what the worker polls and what it registers
    Then the worker polls rwb-case and no other task queue
    Then EvaluateRulesActivity and RecordAndApplyActivity are registered with their retry policy
    Then ReferenceCaseWorkflow is registered with the workflow ID prefix ref-case-
    Then the payload codec is attached to every client and worker of the deployment
    Then the readiness probe reports healthy only after the first successful poll

  Scenario: AC3 The flag governs the deployment and the scope is test-only (new, D-RCV-60)
    Given the values file of an environment
    When the flag step reads rwb.p3.temporal
    Then the flag is on in DEV and SIT and is not declared for any other environment
    Then the release refuses a chart render that sets the flag outside DEV and SIT
    When the flag is off in an environment
    Then no worker is deployed on rwb-case, the reference workflow is not registered and the relay is idle
    Then no production case is read or written by the deployment

  Scenario: AC4 The replay gate step runs before promotion (new, D-RCV-60)
    Given a new build and the recorded reference histories
    When the replay gate step runs in the pipeline
    Then each recorded history is replayed against the new build and the new contract jar
    Then the step reports the build ID, the number of histories and the result per history
    When a history does not replay
    Then the step fails with MSG-P3-038, the artefact is not promoted and the previous build stays in force
    Then the promotion is blocked until a build passes the gate

  Scenario: AC5 The five dashboard series and the stuck-workflow scan report the pattern (new, D-RCV-60)
    Given the published dashboard of the deployment
    When the reference run and a set of synthetic failures are replayed
    Then the dashboard shows workflow failures, signal failures, activity retries, the NoPackageInForce count and the replay result
    Then each series carries the environment, the release and the build ID as dimensions
    Then the stuck-workflow scan of the platform runs every five minutes and reports a workflow with no progress
    Then a workflow failed on NoPackageInForce appears in the scan and in the count with MSG-P3-027

  Scenario: AC6 The runbook and the alerts cover the three operational failures (new, D-RCV-60)
    Given the published runbook and the alert rules
    When a stuck worker, a signal backlog and a replay failure are simulated
    Then each condition raises its alert, carrying MSG-P3-036 or MSG-P3-038 where the message applies
    Then every alert links one runbook entry with the check, the owner role and the recovery step
    Then the runbook states that the reference deployment is test-only and never a production recovery step
    Then the alert thresholds are values of the environment and are not hard-coded

  Scenario: AC7 The business rules BR1 to BR10 of section 8 hold for the deployment (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8
    When the deployment is rendered and the reference run is replayed
    Then each rule BR1 to BR10 is verified by its test case in section 16
    Then a rule that is an architecture constraint is checked by a guardrail or boundary test

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given the case state model of the reference workflow
    When the workflow requests a status change the model does not allow
    Then the change is refused and no case state is written
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one task queue, one login: the worker polls `rwb-case` in namespace `rwb-recovery` and carries the rwb-case login only | Arch v5 slides 24 and 41; DP-02; DP-10 |
| BR2 | Every worker carries the build ID of its release and worker versioning is enabled, so a new build takes new workflows while the old build drains | Design slide 27; RWB-PLT-E1071-CON |
| BR3 | A build is promoted only after the replay gate replays the recorded histories and passes | Design slide 27; RWB-E2-040 |
| BR4 | The skeleton is deployed to DEV and SIT only; the release refuses the flag in any other environment and starts no production case | Legacy RWB-E2-043 BR7; ASM-1272 |
| BR5 | The deployment owns no Schedule: the reference workflow is started by the harness, and the stuck-workflow scan is a platform capability | Design slide 28; Arch v5 slide 44 (JOB-21) |
| BR6 | Every alert carries a message ID and the agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR7 | No environment value is hard-coded: replicas, resources, thresholds, scan intervals and the flag come from values files and parameters | DP-06 principle; Template and Rules §R7.2 s17 |
| BR8 | Dashboard series, alert payloads and the runbook carry counts, IDs, codes and build IDs only, never personal data or a decoded payload | Design slide 27 (PDPA) |
| BR9 | A failing build never replaces a working one: the previous build stays in force until the new build passes the gate | Design slide 27; DP-10 |
| BR10 | The deployment is test-only in scope: it declares no production route, no production case and no production data set | Legacy RWB-E2-043 BR7 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass and the gate passes | Deploying |
| Deploying | Worker registered and probes healthy | The worker polls `rwb-case` only and the two activities are registered | Ready |
| Ready | Release superseded | A new chart version passes the gate | Rolling |
| Rolling | All workers on the new build | The old build drains its open workflows | Ready |
| Ready | Replay gate failed | A recorded history no longer replays | Blocked |
| Blocked | Previous build restored | The gate passes on a later build, or the previous build is redeployed | Ready |
| Ready | Flag off | `rwb.p3.temporal` is turned off in the environment | Not deployed |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the registration check, the gate step, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the worker versioning policy, the topic provisioning and the stuck-workflow scan |
| Platform workflow kit owner | Owns the replay gate mechanism, the build ID provider and the codec server |
| Release manager | Approves the promotion of one artefact and may block it on a gate failure |
| On-call operator | Runs the three runbook entries and opens an incident when a gate failure or a package failure persists |
| RW-PLATADM | Reads the reference run in the Temporal Web UI, not in the cluster |
| RW-AUDIT | Reads the history with encrypted payloads and references only |

The worker runs as the rwb-case service identity (DP-02), carried by the chart as a secret reference and never as a literal name.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, feature switches | Not specified in the source documents (DOR-RWB-P3-E2043-OPS-7) |
| Task queue | `rwb-case` in namespace `rwb-recovery`, polled by the rwb-case worker only | Not specified in the source documents (DOR-RWB-P3-E2043-OPS-7) |
| Topics | `rwb.case.events.v1` consumed through the outbox relay with its retry and `.dlt` topics; `rwb.decision-record.v1` published by the local library and consumed by rwb-decision | Not specified in the source documents (DOR-RWB-P3-E2043-OPS-7) |
| Schema | `rwb_case`, migrated by its own per-service Flyway sequence; this release adds no migration | Not specified in the source documents (DOR-RWB-P3-E2043-OPS-7) |
| Dashboard series | Workflow failures, signal failures, activity retries, NoPackageInForce count, replay results; dimensions environment, release, build ID | Not specified in the source documents (DOR-RWB-P3-E2043-OPS-7) |
| Runbook entries | Stuck worker, signal backlog, replay failure; each with the check, the owner role and the recovery step | Not specified in the source documents (DOR-RWB-P3-E2043-OPS-7) |
| Scan | The platform stuck-workflow scan (JOB-21) with its interval and its threshold | Not specified in the source documents (DOR-RWB-P3-E2043-OPS-7) |
| Secrets | The rwb-case login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store | Not specified in the source documents (DOR-RWB-P3-E2043-OPS-7) |
| Test data | The synthetic case "RW-2026-000777" in DEV and SIT only; the fixture owner is Not specified in the source documents (GAP-0724; ASM-1272) | Not specified in the source documents (DOR-RWB-P3-E2043-OPS-7) |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class and the exact probe timings) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value, and this story fixes only their names and the rule that they are never hard-coded. No topology value is fixed here.

**Probes.** Readiness answers healthy only after the worker has polled `rwb-case` once, the payload codec is attached and the relay has read its first delivery; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database, and a failing dependency is reported as not ready, never as live-and-broken. The paths and timings are values of the environment.

### 12. Contract

#### 12.1 REST operations provided

None. The reference deployment exposes no REST path, no admin operation and no composite route; the probes are cluster-internal and are not part of the API surface. The REST surface of rwb-case is deployed by its own stories and is untouched by this release.

#### 12.2 REST operations consumed

None. The deployment needs no REST client: the rule package is fetched in-process inside the activity, and the reference data is read through the rwb-case contract inside the same activity.

#### 12.3 Events published

None of its own. The skeleton publishes nothing; DecisionRecorded on `rwb.decision-record.v1` is published by the local decision-record library through the outbox, and the six `rwb.case.*` types belong to the case event contract.

#### 12.4 Events consumed

| Event type | Topic | Deployment element | Owner and service |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | Relay consumer with the inbox; retry topic and `.dlt` configured | RWB-PLT-TE006-CON (topic); rwb-case (consumer) |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | Same consumer | RWB-PLT-TE006-CON (topic); rwb-case (consumer) |
| `rwb.case.CaseAllocationFailed.v1` | `rwb.case.events.v1` | Same consumer | RWB-PLT-TE006-CON (topic); rwb-case (consumer) |
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | Same consumer | RWB-PLT-TE006-CON (topic); rwb-case (consumer) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | Same consumer | RWB-PLT-TE006-CON (topic); rwb-case (consumer) |
| `rwb.case.TimerBreached.v1` | `rwb.case.events.v1` | Same consumer | RWB-PLT-TE006-CON (topic); rwb-case (consumer) |

The topic, its retry and `.dlt` topics and the six event types are provisioned and owned by RWB-PLT-TE006-CON and by the case event contract; this deployment only configures the consumer group, the inbox and the relay that turns a delivery into a CaseEvent signal.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| ReferenceCaseWorkflow | Workflow, test-only scope, workflow ID prefix `ref-case-` | `rwb-case` | Registered by the worker of this release, with the build ID and worker versioning |
| EvaluateRulesActivity | Activity | `rwb-case` | Registered by the same worker with the retry policy of 1 s, back-off 2, 10 attempts |
| RecordAndApplyActivity | Activity | `rwb-case` | Registered by the same worker with the same policy; one transaction, idempotent by the event key |
| CaseEventSignalRelay | Outbox consumer | not a worker | Deployed in the same release; calls `WorkflowGateway.signal` with mTLS to the frontend |

**Build ID and versioning.** The build ID is the one supplied by the workflow kit for the release commit; worker versioning is enabled and a new build takes new workflows while the old build drains. The build ID format and the versioning policy are Not specified in the source documents (GAP-0725; ASM-1273).

#### 12.6 Schedules

None. The deployment registers no Schedule: the reference workflow is started by the harness, and the stuck-workflow scan is the platform's visibility query (JOB-21), not a Schedule of this story. The Schedules of rwb-case belong to their own stories (DP-10).

#### 12.7 Tables owned

None. The release applies no migration and adds no table; the local decision record, the outbox, the inbox and the idempotency objects are created in schema `rwb_case` by the DB story of the service, and the case row is written by the case state service (DP-01, DP-15).

#### 12.8 Contract fakes

None. No fake is deployed: the workflow tests run on TestWorkflowEnvironment in the pipeline, and the contract mocks of the rule evaluator, the record library and the case state service are in-process test doubles. No WireMock workload is part of this release.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | No path and no client; probes are cluster-internal |
| Kafka | 0 published, 6 types consumed through the relay | `rwb.case.events.v1` with retry and `.dlt`; DecisionRecorded is published by the library |
| Temporal | 1 workflow, 2 activities, 0 Schedules | Worker on `rwb-case` with a pinned build ID and worker versioning |
| File | None | The recorded histories used by the gate are pipeline inputs, not runtime data |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the release applies no migration and reads no other schema | none |
| DP-03 | DecisionLogWriter, decision log | The local record library is deployed with the worker and publishes to `rwb.decision-record.v1` through the outbox | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | The embedded kit is part of the worker image; the package model is fetched from rwb-decision in the activity | H RWB-PLT-E1072-CON (registry side is RWB-P7-E1073) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read in this release; the fixture is synthetic and an Epic 3 copy reads ACE data through the rwb-source-data contract | none |
| DP-07 | Reference data, LOV | The reference-data contract of rwb-case is a runtime dependency of RecordAndApply, with the client library | H RWB-PLT-E1043-CON; RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The relay consumer group with the inbox, the retry topic and the `.dlt` topic | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue and the namespace come from the workflow kit; no Schedule is registered | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The release declares no REST client and no REST path; the workflow reaches the rules and the state in-process | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | The consumer uses `rwb.case.events.v1` with the naming library; the deployment adds no topic | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | The per-service Flyway sequence is already applied; this release adds no migration | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff is not used: the deployment registers no route, no screen and no composite target | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-case/` reference overlay | Worker deployment, config map, secret references, probes, the task queue and the namespace, the flag and the build ID |
| `helm/rwb-case/values-dev.yaml`, `values-sit.yaml` | Image digest, replicas, resources, probe timings, log level, flag `rwb.p3.temporal` on, build ID, environment |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, the replay gate step, the promotion |
| Registration check | Worker polls `rwb-case` only; the two activities and the reference workflow are registered; the codec is attached |
| Flag step | Sets `rwb.p3.temporal` from the environment; refuses a value outside DEV and SIT |
| Replay gate step | Replays the recorded reference histories against the build and the contract jar; reports per history and fails the promotion |
| Dashboards | Workflow failures, signal failures, activity retries, NoPackageInForce count, replay results |
| Alerts | Three rules, each with a message ID and one runbook entry |
| Runbook | Three entries: stuck worker, signal backlog, replay failure |

**Replay gate.** The step runs after the contract tests and before the promotion, replays every recorded history of the fixture against the new build and the new contract jar, and reports the build ID with the result per history. A failure leaves the previous build in force and blocks the promotion until a build passes. The corpus size, the retention of the recorded histories and the exact message text of MSG-P3-038 are Not specified in the source documents (GAP-0726; ASM-1274).

**Stuck-workflow scan.** The platform runs the visibility query every five minutes and reports a workflow that has made no progress, a workflow failed on a non-retryable outcome, and a workflow whose build ID is no longer served by any worker. This story consumes the scan and does not implement it; the scan interval and the inactivity threshold are values of the environment.

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P3-036 | The Temporal frontend is unreachable at signal time | Signal-failure alert with the delivery count and the oldest attempt time | Platform on-call, page |
| MSG-P3-027 | No package version is in force for the reference | NoPackageInForce alert naming the package code and the build ID | Business on-call (RW-COE), page |
| MSG-P3-038 | A recorded history does not replay against the build | Replay-gate alert with the history reference and the build ID | Release manager and platform on-call, page; the promotion is blocked |

**Rollback.** A release that fails the gate is not promoted; a release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open workflows until they finish. The reference workflow holds no business state of its own, so a rollback needs no data repair; the synthetic fixture is removed by the harness and no production row is touched.

**Feature switch.** `rwb.p3.temporal`. On: the worker is deployed on `rwb-case`, the reference workflow is registered and the relay runs. Off: no worker, no registered workflow and an idle relay; outbox deliveries stay PENDING. The switch is never set for an environment outside DEV and SIT.

**Done when.** The chart renders for DEV and SIT, the registration check passes, the flag step refuses a third environment, the gate blocks a bad build and passes a good one, the five series and the three alerts are published, the three runbook entries are reviewed by the on-call rota, and the smoke run of "ref-case-RW-2026-000777" completes with the released build ID.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-036 | The Temporal frontend is unreachable at signal time | The workflow service is not available. Try again in a few minutes. |
| MSG-P3-027 | No package version is in force for the reference | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P7-003 | The decision record write fails inside the activity | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-038 | A recorded history does not replay against the build | Not specified in the source documents (GAP-0726; ASM-1274) |

The business texts are copied unchanged from the legacy story; the deployment adds the alert routing and the runbook link, never a new wording. For MSG-P3-027 the {table} names the reference table and the {check} names the failed check.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard, the Temporal Web UI view of "ref-case-RW-2026-000777" and the runbook. The Web UI is behind Entra ID: RW-PLATADM operates and RW-AUDIT reads; payloads are decoded only through the codec server under break-glass (RWB-E2-038). SCR-44 Interface and job monitor is not used, because the deployment registers no job and no queue of its own. The empty, loading, error and no access states: Not specified in the source documents (CG-ALL-4446).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2043-OPS-01 | AC1 | NFR | The chart renders for DEV and SIT with a pinned digest, the build ID, worker versioning and the rwb-case login reference |
| TC-P3-E2043-OPS-02 | AC2 | NFR | A worker polls `rwb-case` only; the two activities and the reference workflow are registered; the codec is attached |
| TC-P3-E2043-OPS-03 | AC3 | NFR | The flag is on in DEV and SIT; a render that sets it elsewhere is refused; flag off deploys no worker |
| TC-P3-E2043-OPS-04 | AC4 | NFR | The gate passes a good build and fails a build whose recorded history no longer replays |
| TC-P3-E2043-OPS-05 | AC5 | NFR | The five series carry the build ID; the scan reports a stalled workflow and a NoPackageInForce failure |
| TC-P3-E2043-OPS-06 | AC6 | NFR | Three synthetic conditions raise the three mapped alerts with one runbook entry each |
| TC-P3-E2043-OPS-07 | §12 operations, §12.4 events | Contract | The operations, events and activities of §12 match the case event contract; the six §12.4 events are consumed through the relay with retry and `.dlt` |
| TC-P3-E2043-OPS-08 | BR1 | NFR | The worker polls `rwb-case` in namespace `rwb-recovery` with the rwb-case login only |
| TC-P3-E2043-OPS-09 | BR2 | NFR | Every worker carries the release build ID and worker versioning is enabled; an old build drains while a new build takes new workflows |
| TC-P3-E2043-OPS-10 | BR3 | NFR | A build is promoted only when the replay gate passes; a failing replay stops promotion |
| TC-P3-E2043-OPS-11 | BR4 | NFR | The flag is refused in any environment other than DEV and SIT; no production case starts |
| TC-P3-E2043-OPS-12 | BR5 | NFR | The deployment renders no Schedule; the reference workflow is started by the harness and the scan is a platform capability |
| TC-P3-E2043-OPS-13 | BR6 | NFR | Each alert carries a message ID, the agreed text and one runbook entry |
| TC-P3-E2043-OPS-14 | BR7 | NFR | No environment value is hard-coded; replicas, thresholds, scan intervals and the flag come from values files |
| TC-P3-E2043-OPS-15 | BR8 | NFR | Dashboard series, alert payloads and the runbook carry counts, IDs, codes and build IDs only |
| TC-P3-E2043-OPS-16 | BR9 | NFR | A failing build leaves the previous build in force until the new build passes the gate |
| TC-P3-E2043-OPS-17 | BR10 | NFR | The deployment declares no production route, production case or production data set |
| TC-P3-E2043-OPS-18 | AC7 | NFR | Not specified in the source documents (NEWAC-RWB-P3-E2043-OPS-AC7) |
| TC-P3-E2043-OPS-19 | AC8 | NFR | Not specified in the source documents (NEWAC-RWB-P3-E2043-OPS-AC8) |

### 17. Guardrails

- No business value in a values file: the package code, the rule ID, the case status and the route values are data in the rule packages and the reference tables, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the runbook or the recorded histories: counts, IDs, codes, reference and build IDs only, and payloads stay encrypted.
- One login per service and one task queue per service: the release carries the rwb-case login and polls `rwb-case` only (DP-02, DP-10).
- The release writes only schema `rwb_case` and applies no migration; no other schema is touched (DP-01, DP-15).
- The consumer dedupes through the inbox and has a retry topic and a `.dlt` topic before it starts (DP-09).
- The skeleton is deployed to DEV and SIT only and starts no production case; the flag is refused in any other environment.
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing gate never replaces a working build.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision is recorded with the rule and version that made it | Worker registration of the two activities; the record path on the dashboard | TC-P3-E2043-OPS-02, TC-P3-E2043-OPS-05 |
| REQ-DRI-005 | No action proceeds if its decision record cannot be written | One-transaction activity in the deployed worker; MSG-P7-003 alert routing | TC-P3-E2043-OPS-02, TC-P3-E2043-OPS-06 |
| REQ-CWC-016 | Rules are evaluated by Drools from a versioned package | The embedded kit in the worker image and the NoPackageInForce series and alert | TC-P3-E2043-OPS-05, TC-P3-E2043-OPS-06 |
| REQ-DRI-007 | An outbound step retries on a defined schedule and leaves a visible exception when it fails | Relay consumer with retry and `.dlt`, the signal-failure series and the backlog runbook entry | TC-P3-E2043-OPS-05, TC-P3-E2043-OPS-06 |
| D-RCV-60 | The pattern is deployed on the owning service's queue and proved on recorded histories | Worker on `rwb-case`, build ID and worker versioning, the replay gate step | TC-P3-E2043-OPS-01, TC-P3-E2043-OPS-04 |
| ADR-023 | Observability per service | Five dashboard series, three alerts and three runbook entries | TC-P3-E2043-OPS-05, TC-P3-E2043-OPS-06 |

### 19. Out of scope

- The workflow, the two activities and the relay as code (RWB-P3-E2043-APP).
- The contract jar, the records and the retry policy as published artefacts (RWB-P3-E2043-CON); this story only deploys and gates them.
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The implementation of the stuck-workflow scan and of the replay gate mechanism (platform epics; RWB-E2-040); this story consumes both.
- The topic provisioning implementation and the schema registry (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The case event types and their schemas, which belong to the case event contract.
- The local decision-record library and the central ledger (RWB-PLT-E1027-CON, RWB-P7-E2043-APP).
- The real cross-service proof of the pattern (RWB-ITG-E2043-ITG).
- The exact cluster topology, node pools, replica counts and probe timings; they are set per environment by the platform team, not by this story.
- gateway-bff, the composite route and every screen; the deployment registers none of them.
- Any production deployment, production data set or production Schedule: the skeleton is test-only in scope.
