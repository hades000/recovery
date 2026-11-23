# RWB-P9-E2009-OPS Steering dashboard v1 data set — deployment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E2009-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P9-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (FR-P9-007, FR-P9-009, FR-P9-010, FR-P9-011, FR-P9-012, FR-P9-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the deployment slice of RWB-E2-009 for rwb-reporting — the api and worker deployments of the steering build, its login and secrets, the migration and the record table, the Schedule registration on queue `rwb-reporting`, the consumer groups of the eight subscriptions, the extract hand-over, the alerts, the run view, the flag, the backfill and the rollback — is split from the contract baseline (RWB-P9-E2009-CON) and from the application work (RWB-P9-E2009-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **DevOps team of the recovery platform**, I want **the rwb-reporting steering build deployed as one api and one worker behind the recovery edge, on its own login and schema, with its Schedule registered, its eight consumer groups provisioned, an alert for every failure path carrying a message ID and an owned runbook entry, and a rollback that drains a running workflow — so that** the steering data set is published every business morning and an operator can tell a late source from a held day without reading a log.

The release carries, and nothing else:

- two deployments of one image — `api` serving `GET /reports/measures` on `/api/recovery/reporting/v1` through the gateway-bff, and `worker` polling the task queue `rwb-reporting` in namespace `rwb-recovery` (DP-13, DP-19);
- the login `rwb_reporting` on schema `rwb_reporting`, its connection pool and its secret references, and no grant on another schema, on `recovery` or on a `v_ace_*` view (DP-01, DP-02, DP-17);
- the migration increment of the key — the unique key on the business date, the two indexes and the library record table in `rwb_reporting` — gated by lint and drift (DP-15);
- the Schedule `reportingMeasuresDaily` (JOB-15) at 01:30 registered with the build ID of the release, and its workflow with the six activities (DP-10);
- the eight consumer groups of the subscriptions declared by RWB-P9-E2009-CON, and no topic of this service's own (DP-17);
- the extract hand-over to rwb-integration on its queue, with the freshness stamp of the published day;
- the six alerts, the four dashboard series, the run view of JOB-15 and the six runbook entries that go with them;
- the flag `rwb.reporting.steering`, the backfill of a business date and the rollback of a build.

The behaviour of the measures is RWB-P9-E2009-APP and the shapes are RWB-P9-E2009-CON; this story ships neither. Where a deployment value has no source, it is a value of the environment and the default stands as an assumption (GAP-2578; ASM-4249).

### 2. Business rationale

A service that no one operates is not delivered. The legacy story assumed a Quartz job inside one deployed monolith, a shared recovery login, a shared job monitor and a data-lake load area; under D-RCV-60 the run is a Scheduled workflow on its own queue under its own login, its facts arrive on eight subscriptions, its extract leaves through rwb-integration, and its publish can be held by design. Each of those is a deployment object that has to exist before the first business morning, and each has a failure mode an operator must recognise: a source that never arrives, a worker that is not polling, a Schedule that did not fire, a contract that does not answer, a record that cannot be written, and a handed-over extract that never landed.

- **the morning is the deadline.** The 07:30 Power BI refresh follows the 01:30 run, so a stale source or an unstarted worker is a business problem by 07:00, not an infrastructure one.
- **a held day is a successful run.** The most common non-zero outcome is a day held on a count mismatch; the run view and the alert tell that apart from a failed run.
- **a rerun is safe.** The run is idempotent per business date, so the fix for most mornings is a backfill of one date and not a repair script.

### 3. Preconditions

- RWB-P9-E2009-CON is tagged `v1` and the image of RWB-P9-E2009-APP is built and pushed under the release build ID.
- RWB-P9-E1013-APP is deployed: `measure_definition` and `measure_snapshot` exist and the baseline of 2026-11-27 is frozen.
- The platform objects exist: the gateway-bff route for `/api/recovery/reporting/*`, the secret store, the Temporal namespace `rwb-recovery`, the OpenTelemetry collector and the workload identity of the namespace (DP-19).
- The login `rwb_reporting` is allocated with its secret reference; the schema `rwb_reporting` exists; the connection pool size, the replica counts and the resource requests are values of the environment and stand as assumptions (GAP-2578; ASM-4249).
- The producers of the eight subscriptions — rwb-case, rwb-decision, rwb-treatment, rwb-comms and rwb-agent — publish their topics, and rwb-integration accepts the extract hand-over on its queue.
- The six message IDs of section 14 are registered in the platform message catalogue; no business text is written by this story.
- Status is Draft (realignment v1): no approval and no production change are required to prepare the release, and the first environment is non-production (GAP-2578; ASM-4250).

### 4. Flow

1. The pipeline builds one image and two deployments from it, with the release build ID of the commit and the image digest pinned; no `latest` tag is deployed.
2. The migration job runs the Flyway sequence of `rwb_reporting` before the worker starts, and the drift gate compares the applied state with the baseline of RWB-P9-E2009-CON; a drift fails the release.
3. The api deployment starts behind the gateway-bff route, with its readiness probe on the health endpoint, and declares no route of its own.
4. The worker deployment starts and registers the workflow `reportingMeasuresDaily` and its six activities on the task queue `rwb-reporting`, with worker versioning on the build ID.
5. The Schedule `reportingMeasuresDaily` is created at 01:30 with overlap skipped and catch-up enabled; the Schedule carries the build ID of the release, so a rollback re-registers it against the previous build.
6. The eight consumer groups of section 12.4 are registered on the producers' topics before the first business date; the offsets start at the run window of the first business date and not at the end of the log.
7. The flag `rwb.reporting.steering` is read at the start of the run: off means the execution ends with the run alert, the business date is held and nothing is written.
8. `checkFreshness` reads the data-product freshness of the day on the read RWB-P1-E1013-APP declares; a stale product leaves the run to write its measure from the last complete day with that date as the freshness stamp and to raise MSG-P1-001.
9. `publishDay` commits the record, the snapshot rows and `measure_publish` in one transaction, and `handOverExtract` passes the published day's extract to rwb-integration on its queue.
10. The run writes its summary to the visibility view; the four dashboard series and the run view of JOB-15 read them, and a held day shows both counts and the held reason.
11. A failed run raises its alert with a message ID and a runbook link; the operator fixes the cause — a source, a flag, a contract, the record store — or backfills the business date, which replays the same execution and writes nothing twice.
12. A rollback redeploys the previous chart and build ID; a running execution finishes on the build that started it, the Schedule is re-registered against the previous build, and a new business date starts there until the fix ships again.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A source of the day is late or not ready | The measure of that source carries the last complete day's date, and the screen shows the stale marker | MSG-P1-001 | AC5, AC6, BR6 |
| X2 | The worker is not polling, or the Schedule did not fire | The business date has no execution by the run window; the alert names the Schedule and the date | None (run alert; runbook entry 1) | AC3, AC5 |
| X3 | The case-facts contract does not answer inside 2 s or its breaker is open | The activity retries on the workflow policy; the day stays unpublished rather than published unverified | None | AC5, AC6, BR8 |
| X4 | The record chain is stopped or its store is unavailable | The transaction writes nothing; the incident is raised and the date is backfilled once the store is back | MSG-P7-003 | AC5, AC6 |
| X5 | The dashboard count differs from the case list | The run succeeds as a held day, both counts are named, and the previous day stays the latest published | MSG-P9-002 | AC5, BR7 |
| X6 | The extract hand-over to rwb-integration fails or is not accepted | The published rows stand, the hand-over is retried from the run, and the reporting analyst is alerted | MSG-GEN-006 | AC4, AC5 |
| X7 | The flag is off in an environment that has the run | The date is held, nothing is written, and the run view says the flag is off | None (run alert) | AC6 |
| X8 | The migration leaves the schema not matching the baseline | The drift gate fails the release and the worker is not started | None (pipeline log) | AC2 |
| X9 | A consumer group is missing or its offset policy is wrong at the first business date | The run sees no events of that producer, the counts differ, and the day is held rather than published | MSG-P9-002 | AC4, BR4 |

X1 to X5 are the failure paths of the legacy key restated as deployment objects; X6 is the hand-over, X7 the flag's, X8 the migration gate's and X9 the subscription's. None of them changes a business value: the measure codes, formulas, age bands and the zero tolerance of DL25 are rows of their owners, and the thresholds of the alerts are values of the environment.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 from the tagged contract baseline and the image; needs no running neighbour beyond the platform objects and the producers' topics |
| Negotiable | Replica counts, thresholds, series windows, catch-up window, partition counts and retention are values of the environment and are tuned per environment |
| Valuable | The steering data set is delivered every business morning, a held day is visible, and every failure is named by a message ID with an owned runbook entry |
| Estimable | Two deployments, one migration job, one Schedule, eight consumer groups, six alerts, four series and six runbook entries |
| Small | Fits in one sprint with the platform team |
| Testable | Each criterion is a deployment check, a registration check or an alert check at Level NFR or End to end |

### 7. Acceptance criteria

```gherkin
Feature: The deployment of the rwb-reporting steering dashboard build

  Background:
    Given the contract baseline of the service is tagged "v1" and the image of the release is built under its build ID
    Given the namespace "rwb-recovery", the task queue "rwb-reporting", the schema "rwb_reporting" and the login "rwb_reporting"

  Scenario: AC1 The api and the worker are deployed on their own login and route (new, D-RCV-60)
    Given the release chart of the service
    When it is applied to the environment
    Then one api deployment serves "/api/recovery/reporting/v1" through the gateway-bff route and one worker deployment polls the queue "rwb-reporting"
    Then both run under the login "rwb_reporting" with secret references and no secret value in the chart
    Then the api readiness probe passes and neither another schema nor a "v_ace_*" view is reachable from the pod
    Then the build ID and the image digest of the release are recorded

  Scenario: AC2 The migration and the record table are applied and the drift gate is green (new, D-RCV-60)
    Given the migration job of the service
    When it runs before the worker starts
    Then "measure_publish" and the library record table exist in "rwb_reporting" with the key and the indexes of the baseline
    Then the snapshot index of the baseline is present on "measure_snapshot"
    Then the drift gate compares the applied state with the baseline and passes
    Then a second run of the migration changes nothing

  Scenario: AC3 The Schedule is registered and fires at the declared time (new, D-RCV-60)
    Given the worker of the release
    When it starts
    Then "reportingMeasuresDaily" and its six activities are registered on the queue "rwb-reporting" in namespace "rwb-recovery"
    Then the Schedule "reportingMeasuresDaily" exists at 01:30 with overlap skipped and catch-up enabled
    Then the Schedule and the worker versioning policy name the build ID of the release
    Then one execution is opened per business date and a rerun joins the existing execution

  Scenario: AC4 The eight consumer groups are registered and the hand-over is reachable (new, D-RCV-60)
    Given the producers of the eight subscriptions of the baseline
    When the release is applied
    Then the consumer groups of EV-01, EV-02, EV-05, EV-08, EV-10, EV-14, EV-15 and EV-28 exist on their topics with their offset policy
    Then this release creates no topic of the service's own and publishes no domain event
    Then the extract hand-over activity answers rwb-integration on the queue "rwb-integration" and reports an accepted delivery

  Scenario: AC5 Every alert carries its message ID or its runbook entry, and one owned entry per path (new, D-RCV-60)
    Given the six alerts of the release
    When each failure path of section 5 is simulated in a non-production environment
    Then the alert fires with its message ID where a business message exists, and with its service and its business date
    Then the alert links one runbook entry with an owner role
    Then the four dashboard series and the run view of JOB-15 show the run, its summary and a held day

  Scenario: AC6 The flag governs the run and the backfill is idempotent (new, D-RCV-60)
    Given the flag "rwb.reporting.steering" is off
    When the Schedule fires for a business date
    Then the date is held and no snapshot row and no publish row are written
    When the flag is on and the same date is backfilled after a failed run
    Then the execution replays and writes the same values once
    Then the backfill limit per run is a value of the environment

  Scenario: AC7 A rollback drains the build without losing a run (new, D-RCV-60)
    Given a running execution on the current build
    When the previous chart and build ID are redeployed
    Then the running execution finishes on the build that started it
    Then the Schedule is re-registered against the previous build
    Then a new business date starts on the previous build
    Then the alerts and the run view keep reading both builds
```

The seven criteria test the deployment only. No measure value, count or rate of the legacy story is fixed by them; the only dates they name are the business date of the run and the values of the environment (ASM-4249).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One image, two deployments, one login and one queue per service; no deployment reaches another schema | DP-01, DP-02, R4 |
| BR2 | The migration runs before the worker and a drift fails the release | DP-15 |
| BR3 | The Schedule is registered on `rwb-reporting` and a rerun joins the execution of its business date | DP-10 |
| BR4 | The eight consumer groups exist before the first business date; this release creates no topic of its own | DP-17; legacy RWB-E2-009 section 12 |
| BR5 | Every alert names its business message ID where one exists and always one owned runbook entry; no alert without a runbook entry is released | R7.2 s14 |
| BR6 | A source that is not ready is shown with its own date and never counted as today's value | Legacy BR4; MSG-P1-001 |
| BR7 | A day whose counts differ is held and never published; the run itself is a success | Legacy BR2; DL25 |
| BR8 | A consumed contract is called with one hop and a 2 s timeout, and a breaker per downstream protects the run | DP-11; ADR-020 |
| BR9 | A backfill is safe to repeat and writes nothing twice; the key is the business date | Legacy AC9; DP-10 |
| BR10 | A rollback drains in-flight runs and re-registers the Schedule; a new date starts on the rollback build | R8.2; AC7 |

### 9. State transitions

None of business data: this story changes no record, no case state and no publish state. The states it owns are the deployment and the run.

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | The chart is applied and the migration passes | The drift gate is green | Deployed, the worker registered and the Schedule created |
| Deployed | The flag is off | X7 | Deployed, the date held |
| Deployed | The Schedule fires for a new date | The flag is on | Running, then Completed with its summary |
| Running | The counts differ | X5 | Completed as a held day, with its alert |
| Running | A failure path fires | X1 to X4, X6 | Failed with its alert; the date is backfillable |
| Deployed | A rollback is applied | AC7 | The previous build serves new dates; the running execution finishes |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps team | Applies the chart, runs the migration, creates the Schedule, registers the consumer groups, owns the releases and the rollback |
| Platform administrator | Allocates the login and the secret references, the queue and the namespace objects |
| The observability owner (RWB-PLT-OBS) | Owns the collector, the dashboard template and the alert routing; the thresholds are values of the environment |
| The event platform owner (RWB-PLT-EVT) | Owns the topic template of the producers and the consumer-group policy; this release creates no topic |
| The workflow kit owner (RWB-PLT-WF) | Owns the Schedule, the registration contract, the worker versioning policy and the visibility view |
| RW-BIANAL, Reporting and BI analyst | Reads the run view, receives the hold and hand-over alerts, and reruns a business date; changes nothing in the deployment |
| RW-DATASTEW, data steward | Receives the hold alert and reads the reconciliation |
| The service owner of rwb-reporting | Approves the runbook entries and the on-call rota |

No person is named in this story: every duty is a role, and every alert routes to a role.

### 11. Data

| Object | Owner | What this story does |
|---|---|---|
| `measure_publish`, the snapshot index and the library record table in `rwb_reporting` | P9 and the PLT libraries | Creates them by the migration and checks the drift; writes no row |
| The secret references of the login, the reference-data client and the agent client | Platform secret store | References them in the chart; holds no value in a file, a chart value or a pipeline log |
| The Schedule and its build ID | P9 on the workflow kit | Creates and re-registers it; owns the versioning policy of the release |
| The eight consumer groups | P9 | Registers them on the producers' topics before the first business date; creates no topic |
| The extract hand-over | P9 with P2 | Configures the activity, its queue and its retry; the file shape is the contract's |
| The six alerts, the four series and the run view | P9 with the observability owner | Creates them; the thresholds and windows are values of the environment |

No personal data enters a deployment object, an alert, a dashboard series or a log: an alert names the service, the source, the measure family, the business date and the message ID, and never a case, an account or a customer.

### 12. Contract

#### 12.1 REST operations provided

None new. The one operation of the service — `GET /reports/measures` on `/api/recovery/reporting/v1` — is deployed by this story as it is tagged in RWB-P9-E2009-CON, behind the gateway-bff composite route (DP-19). This story changes no path, no parameter, no header and no error, and publishes no health or admin route of its own beyond the platform probe.

#### 12.2 REST operations consumed

| Operation | Base / contract | Owner | Deployment note |
|---|---|---|---|
| The case facts of a business date | `/api/recovery/case/v1` | P3 rwb-case | the client is configured with a 2 s timeout, one GET retry with jitter and a breaker |
| The agent runs of a business date | RWB-P10-E1063-CON | P10 rwb-agent | same policy; read once per run |
| The lists of the measures | RWB-P3-E1043-CON | P3 rwb-case | read once per run and cached for the run, with the version |
| The freshness of the data products of a business date | `/api/recovery/source-data/v1` | P1 rwb-source-data | same policy; read once per run before the facts |
| The extract hand-over | activity on the queue `rwb-integration` | P2 rwb-integration | the activity reports an accepted delivery; a refusal is retried by the run |

The operation and activity names are those of the baseline and carry the placeholder where no published document fixes them (GAP-2578; ASM-4249).

#### 12.3 Events published

None. The ownership row of the service carries no event and this release creates no topic of its own; `rwb.reporting.events.v1`, its `.retry` and its `.dlt` are left unprovisioned for this key and the chart creates nothing on them. The library's `DecisionRecorded` (EV-08) is written to `rwb.decision-record.v1`, whose topic belongs to rwb-decision and is not created here.

#### 12.4 Events consumed

| Event | Topic | Consumer group | Provisioning |
|---|---|---|---|
| `CaseCreated` (EV-01), `CaseAllocated` (EV-02), `CaseStateChanged` (EV-05) | `rwb.case.events.v1` | `rwb-reporting.case.v1` | registered before the first business date; offsets start at the first run window |
| `DecisionRecorded` (EV-08) | `rwb.decision-record.v1` | `rwb-reporting.decision.v1` | as above; the topic belongs to rwb-decision |
| `TreatmentApproved` (EV-10) | `rwb.treatment.events.v1` | `rwb-reporting.treatment.v1` | as above |
| `NoticeDispatched` (EV-14), `NoticeDelivered` (EV-15) | `rwb.comms.events.v1` | `rwb-reporting.notice.v1` | as above |
| `AgentRunCompleted` (EV-28) | `rwb.agent.events.v1` | `rwb-reporting.agent.v1` | as above |

The offset policy, the retention of the consumers' positions and the catch-up window are values of the environment (ASM-4249). A missing group is a held day and an alert (X9), never a silent empty measure.

#### 12.5 Workflows and activities

| Name | Type | Registration |
|---|---|---|
| `reportingMeasuresDaily` (JOB-15) | Workflow | registered on queue `rwb-reporting`; the build ID pins the worker version; the execution id derives from the business date |
| `checkFreshness`, `loadReadModel`, `loadAgentFacts`, `computeMeasures`, `reconcileCounts`, `publishDay` | Activities | registered with the workflow; the hand-over of `publishDay` runs on the rwb-integration queue |
| The Schedule `reportingMeasuresDaily` | Schedule | 01:30 daily, overlap skipped, catch-up enabled; re-registered by a rollback |

The registration check asserts the queue, the workflow type, the input schema, the Schedule and its cadence. The build ID and the versioning policy are values of the release and are recorded with it (GAP-2578; ASM-4250).

#### 12.6 Schedules

| Schedule | Cadence | Overlap | Catch-up |
|---|---|---|---|
| `reportingMeasuresDaily` (JOB-15) | 01:30 on each business day, replacing the Quartz row | skipped: one execution per business date | a missed date catches up one by one, up to the window of the environment |

The time zone, the catch-up window and the backfill limit per run are values of the environment (ASM-4249). No other Schedule, cron, overlap policy or catch-up window is created for this service.

#### 12.7 Tables owned

| Object | Owner | Applied by |
|---|---|---|
| `measure_publish` | P9 (`rwb_reporting`) | created by the parent's migration; this job adds the unique key on `business_date` and the index on `status` |
| The snapshot index on `measure_snapshot` | P9 (`rwb_reporting`) | the same job; the table itself is the baseline of RWB-P9-E1013-CON |
| `decision_record` | PLT library in `rwb_reporting` | the library migration of the same job |
| The flyway history of `rwb_reporting` | P9 | the job's own record; the drift gate reads it |

The job creates no table of another schema, requests no grant beyond `rwb_reporting`, and names no `v_ace_*` view and no data-lake object. No migration of the monolith is reused.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Environment stub of rwb-case, rwb-source-data and the reference data | the case facts, the data-product freshness and the five lists of a synthetic day | AC4 and AC6 |
| Environment stub of rwb-agent | an agent with 200 recommendations and an agent with none | AC4 and AC6 |
| Environment stub of rwb-source-data and rwb-integration | a ready and a not-ready source, an accepted and a refused hand-over | X1 and X6 |
| Fault stub of the record library | a stopped chain answering MSG-P7-003 | X4 and AC5 |
| Subscription fixtures | one valid sample per event of 12.4 | AC4 and X9 |

The stubs are the CON fakes of RWB-P9-E2009-CON driven by an environment switch; they are never enabled in production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided by the service, 4 consumed | `/reports/measures` behind the composite route; the case-facts, agent-run, freshness and reference-data clients with one hop and 2 s |
| Kafka | none published, 8 subscribed | eight consumer groups on five producers' topics; no topic of this service and no domain event |
| Temporal | 1 workflow, 6 activities, 1 Schedule, 8 groups of consumers | `reportingMeasuresDaily` on `rwb-reporting`, the P1 and P2 activities on their owners' queues |
| File | 1 out | the published day's extract, handed to rwb-integration for the 07:30 Power BI refresh |

### 13. Solution plan

**Chart.** `deploy/rwb-reporting/`: one image, two deployments (`api`, `worker`), the migration job, the route fragment, the Schedule, the alert rules, the dashboard, the runbook links and the values files per environment.

| Component | Type | Responsibility |
|---|---|---|
| `api` deployment | Deployment | serves the one operation behind the gateway-bff, with its readiness and liveness probes |
| `worker` deployment | Deployment | polls `rwb-reporting`, registers the workflow and its activities, runs the eight consumer groups |
| `migrate` job | Job | runs the Flyway sequence and the library migration before the worker; the drift gate reads its result |
| `schedule` manifest | Manifest | the Schedule `reportingMeasuresDaily` with its cadence, overlap and catch-up values |
| `alerts` rules | Rules | six alerts, each with a message ID, a label set and a runbook link |
| `dashboard` | Chart | four series: runs by outcome, days held, measures written, hand-over failures |
| `runbook` | Document | six entries: Schedule not fired or worker not polling; stale source; count mismatch; record chain stopped; hand-over refused; consumer group missing |

| Runbook entry | Trigger | First step | Owner role |
|---|---|---|---|
| 1 | No execution by the run window | check the Schedule registration and the worker | DevOps team |
| 2 | MSG-P1-001 on the screen or the run | check the data-product freshness and its business date; do not force the run | DevOps team with the data owner |
| 3 | MSG-P9-002 and a held day | confirm both counts on the run view and refer the difference to the data steward; do not edit the row | RW-DATASTEW with the DevOps team |
| 4 | MSG-P7-003 and a stopped chain | check the record store, then backfill the date | DevOps team with the platform record owner |
| 5 | A refused hand-over | check rwb-integration and the freshness stamp, then replay the hand-over from the run | DevOps team with the integration owner |
| 6 | A held day on an empty measure | check the consumer group and its offsets, then backfill the date | DevOps team with the event platform owner |

**Build steps.** (1) Write the chart, the probes and the migration job; test AC1 and AC2. (2) Register the workflow, the Schedule and the versioning policy; test AC3. (3) Register the eight consumer groups and the hand-over; test AC4. (4) Write the six alerts, the four series and the six runbook entries; test AC5. (5) Wire the flag, the backfill and the rollback; test AC6 and AC7.

### 14. Validation and messages

| ID | When | Alert and text |
|---|---|---|
| MSG-P9-002 | The dashboard count differs from the case list | the held-day alert carries both counts and the date; the screen shows the same text |
| MSG-P1-001 | A source is stale | the stale-source alert carries the product and its date |
| None (run alert) | The flag is off, the Schedule did not fire, or the worker is not polling | the run alert names the Schedule, the business date and, for the flag, that it is off; its message ID is allocated by the catalogue owner and is Not specified in the source documents (GAP-2578; ASM-4249) |
| MSG-GEN-006 | The hand-over or a named system is unavailable | the hand-over alert carries the system name and the business date |
| MSG-P7-003 | The record cannot be written | the incident alert carries the text and the business date; the date is backfillable |
| MSG-P4-002 | The role lacks Reporting R | the API's 403; no alert |

MSG-P9-002, MSG-P1-001 and MSG-P4-002 are the legacy texts of RWB-E2-009 section 14, unchanged; MSG-GEN-006 and MSG-P7-003 are the platform texts the split adds. An alert never carries a case, an account, a payment or a customer value.

### 15. Screens and states

No screen is built here. The operator reads the run on the workflow visibility view and on the run view of JOB-15 (SCR-44), and the officer reads the measures on SCR-37; both are served by the base and the composite route the release deploys. The four dashboard series are the operator's view of the same run, and a held day is visible on both the run view and the screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P9-E2009-OPS-01 | AC1 | NFR | the chart applied to a non-production environment; the probes and the route |
| TC-P9-E2009-OPS-02 | AC2 | Component | the migration run twice and the drift gate |
| TC-P9-E2009-OPS-03 | AC3 | End to end | the Schedule fired for one business date, twice, and the registration query |
| TC-P9-E2009-OPS-04 | AC4 | Component | the eight consumer groups and an accepted hand-over |
| TC-P9-E2009-OPS-05 | AC5 | NFR | each failure path of section 5 simulated, with its message ID and its runbook link |
| TC-P9-E2009-OPS-06 | AC6 | End to end | the flag off, then on, then a backfill of the same date |
| TC-P9-E2009-OPS-07 | AC7 | End to end | a running execution and a rollback to the previous build |

The seven are new with D-RCV-60 and test the deployment only. Integration copies end in `-ITG` and belong to RWB-ITG-E2009-ITG; the ten legacy test cases stay with the criteria the APP story owns.

### 17. Guardrails

- No secret in a chart value, a pipeline log or a prompt: the login, the client credentials and the payload keys are secret references only.
- No personal data in an alert, a series, a log or a run input: an alert names the service, the source, the measure family, the business date and the message ID.
- No business value in a chart, an alert threshold or a runbook: the measure codes, formulas, age bands and the zero tolerance of DL25 belong to their owner; thresholds are values of the environment.
- No deployment reaches another schema, another queue or a topic of this service's own, and no operator edits a row of `rwb_reporting` to force a publish.
- No rollout without the drift gate, the Schedule registration, the eight consumer groups and the six runbook entries in place.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-009 | Steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-OCC-12, FEAT-RPT-03, FEAT-RPT-08 | 15 Manage performance, data and AI | None; NFR-065 and NFR-066 apply | TC-P9-E2009-OPS-03, TC-P9-E2009-OPS-04, TC-P9-E2009-OPS-06 |
| REQ-WKM-006 | Queue counts and ageing reported daily and reconciled to the case list | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-RPT-08 | 15 Manage performance, data and AI | None; DL25 applies | TC-P9-E2009-OPS-01, TC-P9-E2009-OPS-02, TC-P9-E2009-OPS-05, TC-P9-E2009-OPS-07 |

The release is cited by RWB-P9-E2009-APP as its external dependency and by the Day-1 allocation of the DevOps lane L-P9-C.

### 19. Out of scope

- The calculators, the reconciliation, the read and the run (RWB-P9-E2009-APP) and the published shapes (RWB-P9-E2009-CON).
- The platform objects themselves — the cluster, the Temporal namespace, the secret store, the collector and the edge — which are owned by their PLT stories.
- The producers' topics and their schemas, which belong to rwb-case, rwb-decision, rwb-treatment, rwb-comms and rwb-agent.
- The baseline measure set and its deployment (RWB-P9-E1013-APP and RWB-P9-E1013-OPS).
- The queue and service-level measures of RWB-E1-030 and RWB-E2-011, the agent monitoring dashboard of RWB-E2-031, benefit realisation and the regulatory returns.
- Any production change, data fix or manual repair of a business row or a publish row.
