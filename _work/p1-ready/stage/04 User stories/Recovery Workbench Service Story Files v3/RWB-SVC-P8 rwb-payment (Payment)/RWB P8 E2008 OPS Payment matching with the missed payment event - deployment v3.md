# RWB-P8-E2008-OPS Payment matching with the missed payment event — deployment

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-066: Pin the P1 REST reads and use the service-wide Kafka group for JOB-07.
- The matching run starts only on `AceDataReady` with `sourceSystem` ALS and `status` COMPLETED; events for other source systems start nothing (RD-P1-003, RD-P1-040).
- The record key of `AceDataReady` is `{sourceSystem}:{businessDate}` (RD-P1-003).
- The complete batch status literal reads COMPLETED (RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-P8-E2008-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Contract version | rwb-payment REST base /api/recovery/payment/v1, version 5.0.0 (API Specification v5, rwb-payment.yaml) |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-066 |
| Service epic | RWB-SVC-P8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement; not specified in the source documents (DOR-RWB-P8-E2008-OPS-16) |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P8-D |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1043-CON (reference data for the data product code and source system label) |
| Integration dependencies | None |
| External dependencies | None |
| Deployment values | Thresholds, counts, limits, partitions, retention and login secret reference are environment values; not specified in the source documents (GAP-2505). Outbox-lag, dead-letter and workflow-failure alert thresholds: not specified in the source documents (GAP-1353) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (FR-P8-001, FR-P8-002, FR-P8-004, FR-P8-005, FR-P8-006, FR-P8-007, FR-P8-010, FR-P8-011, FR-P8-012, FR-P8-013, FR-P8-015, FR-P8-016, FR-P8-017, FR-P8-027, FR-P8-028, FR-P8-032) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the deployment slice of RWB-E2-008 for rwb-payment — the api and worker deployments of the matching build, its login and secrets, the migration and the library tables, the workflow registration on queue `rwb-payment`, the topics, the consumer group, the alerts, the run view, the flag, the backfill and the rollback — is split from the contract baseline (RWB-P8-E2008-CON) and from the application work (RWB-P8-E2008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 53 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As the **DevOps team of the recovery platform**, I want **the rwb-payment matching build deployed as one api and one worker behind the recovery edge, on its own login and schema, with its workflow registered, its topics and consumer group provisioned, an alert for every failure path carrying a message ID and an owned runbook entry, and a rollback that drains a running workflow**, so that the build runs unattended every business morning and an operator can tell a late batch from a failed run without reading a log.

The release carries, and nothing else:

- two deployments of one image — `api` serving `GET /proceeds` and `POST /proceeds/{proceedsId}/match` on `/api/recovery/payment/v1` through the gateway-bff, and `worker` polling the task queue `rwb-payment` in namespace `rwb-recovery` (DP-13, DP-19);
- the login `rwb_payment` on schema `rwb_payment`, its connection pool and its secret references, and no grant on another schema or on `recovery` (DP-01, DP-02);
- the migration of `proceeds` and of the library tables in `rwb_payment`, gated by lint and drift (DP-15);
- the workflow `matchPayments` registered on the queue with its build ID and its worker versioning, started by `AceDataReady` (EV-26) with `sourceSystem` ALS and `status` COMPLETED and by no Schedule (DP-10);
- the topics `rwb.payment.events.v1` with `.retry` and `.dlt`, the consumer group `rwb-payment.rwb.source-data.events.v1`, and the relay of the outbox (DP-09);
- the five alerts, the four dashboard series, the run view of JOB-07 and the runbook entries that go with them;
- the flag `rwb.payments.matching`, the backfill of a business date and the rollback of a build.

The behaviour of the match is RWB-P8-E2008-APP and the shapes are RWB-P8-E2008-CON; this story ships neither. Where a deployment value has no source, it is a value of the environment and the default stands as an assumption (GAP-2505; ASM-4145).

### 2. Business rationale

A service that no one operates is not delivered. The legacy story assumed a Quartz job inside one deployed monolith, a shared recovery login and a shared job monitor; under D-RCV-60 the matching run is a workflow on its own queue, in its own namespace, under its own login, with its own topic and its own alerts. Each of those is a deployment object that has to exist before the first business morning, and each has a failure mode an operator must recognise: a batch that never arrives, a run that starts and stops on a missing package, a contract that does not answer, a record that cannot be written, and a topic that falls behind.

- **the morning is the deadline.** The run follows the ALS batch, so a late batch or an unstarted worker is a business problem by 07:00, not an infrastructure one.
- **the failures are distinguishable.** The five alerts separate a stale batch, a missing package, a paused flag, a stopped record chain and a lagging outbox, and each names its message ID.
- **a rerun is safe.** The run is idempotent per business date, so the fix for most mornings is a backfill of one date and not a repair script.

### 3. Preconditions

- RWB-P8-E2008-CON is tagged `v1` and the image of RWB-P8-E2008-APP is built and pushed under the release build ID.
- The platform objects exist: the gateway-bff route for `/api/recovery/payment/*`, the secret store, the Kafka cluster with the event platform's topic template, the Temporal namespace `rwb-recovery`, the OpenTelemetry collector and the workload identity of the namespace (DP-19).
- The login `rwb_payment` is allocated with its secret reference; the schema `rwb_payment` exists; the connection pool size, the replica counts and the resource requests are values of the environment and stand as assumptions (GAP-2505; ASM-4145).
- rwb-source-data publishes `AceDataReady` (EV-26) with `sourceSystem` ALS and `status` COMPLETED (record key `{sourceSystem}:{businessDate}`). Use the rwb-payment workload identity for P1 REST reads (DP-05).
- The five message IDs of section 14 are registered in the platform message catalogue; no text is written by this story.
- Status is Draft (realignment v1): no approval and no production change are required to prepare the release, and the first environment is non-production (GAP-2505; ASM-4146).

### 4. Flow

1. The pipeline builds one image and two deployments from it, with the release build ID of the commit and the image digest pinned; no `latest` tag is deployed.
2. The migration job runs the Flyway sequence of `rwb_payment` before the worker starts, and the drift gate compares the applied state with the baseline of RWB-P8-E2008-CON; a drift fails the release.
3. The api deployment starts behind the gateway-bff route, with its readiness probe on the health endpoint and its authorise dependency checked once, and declares no route of its own.
4. The worker deployment starts and registers the workflow `matchPayments` and its four activities on the task queue `rwb-payment`, with worker versioning on the build ID.
5. The event platform creates the topic `rwb.payment.events.v1` with its `.retry` and `.dlt`, and the service registers the consumer group `rwb-payment.rwb.source-data.events.v1` on `rwb.source-data.events.v1`; the group is created before the first business date.
6. The outbox relay of the library starts inside the worker, with its poll interval and its batch size as values of the environment, and publishes to the service's topic with the CloudEvents envelope of the baseline.
7. The shared listener filters EV-26 for ALS/COMPLETED, then uses signal-with-start on the `matchPayments` workflow ID for the date. Inbox and workflow guards make a redelivery a no-op.
8. The flag `rwb.payments.matching` is read at the start of the run: off means the inbox row is written, the date is held and nothing else happens, and no proceeds row and no event are written.
9. The run writes its summary to the visibility view and to the outcome records; the four dashboard series and the run view of JOB-07 read them.
10. A failed run raises its alert with a message ID and a runbook link; the operator either fixes the cause — a package, a flag, a contract — or backfills the business date, which replays the same execution and writes nothing twice.
11. A rollback redeploys the previous chart and build ID; a running execution finishes on the build that started it, and a new business date starts on the previous build until the fix ships again.
12. The alert on the outbox checks the relay lag and the dead-letter topic; a message in `.dlt` is the operator's to replay after the cause is fixed, and the run is not marked complete until the outbox is empty.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ALS batch for the business date is late or not complete | The run is skipped before matching and the plan view shows the stale product and its date | MSG-P1-001 | AC5, BR6 |
| X2 | The worker is not polling, or the event did not arrive | The business date has no execution by the run window; the alert names the missing event for the source and the date | MSG-P1-001 (runbook entry 1) | AC3, AC5 |
| X3 | No `PAYMENT_MATCH` version is in force | The execution fails before matching, the flag is not the cause and the package owner is paged | MSG-P3-027, MSG-P8-002 | AC5, BR7 |
| X4 | The record chain is stopped or the store is unavailable | The transaction writes nothing; the incident is raised and the date is backfilled once the store is back | MSG-P7-003 | AC5, AC6 |
| X5 | A consumed contract does not answer inside 2 s or its breaker is open | The activity retries on the workflow policy; after the last attempt the run is failed and the downstream owner is paged | None | AC5, BR8 |
| X6 | The outbox relay lags, or a message lands in the dead-letter topic | The lag series and the DLT alert fire, and the replay is the operator's step | None | AC4, AC5 |
| X7 | The flag is off in an environment that has the run | The date is held, no row and no event is written, and the run view says the flag is off | None | AC6 |
| X8 | The migration leaves the schema not matching the baseline | The drift gate fails the release and the worker is not started | None (pipeline log) | AC2 |

X1 to X5 are the failure paths of the legacy key restated as deployment objects; X6 is the event platform's, X7 the flag's and X8 the migration gate's. None of them changes a business value: the window, the tolerance and the grace days are rows of the package, and the thresholds of the alerts are values of the environment.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 from the tagged contract baseline and the image; needs no running neighbour beyond the platform objects of the namespace |
| Negotiable | Replica counts, thresholds, series windows, partition counts and retention are values of the environment and are tuned per environment |
| Valuable | The run happens every business morning and every failure is visible with a message ID and an owned runbook entry |
| Estimable | Two deployments, one migration job, one registration, one topic with two subtopics, one consumer group, five alerts, four series and five runbook entries |
| Small | Fits in one sprint with the platform team |
| Testable | Each criterion is a deployment check, a registration check or an alert check at Level NFR or End to end |

### 7. Acceptance criteria

```gherkin
Feature: The deployment of the rwb-payment matching build

  Background:
    Given the contract baseline of the service is tagged "v1" and the image of the release is built under its build ID
    Given the namespace "rwb-recovery", the task queue "rwb-payment", the schema "rwb_payment" and the login "rwb_payment"

  Scenario: AC1 The api and the worker are deployed on their own login and route (new, D-RCV-60)
    Given the release chart of the service
    When it is applied to the environment
    Then one api deployment serves "/api/recovery/payment/v1" through the gateway-bff route and one worker deployment polls the queue "rwb-payment"
    Then both run under the login "rwb_payment" with secret references and no secret value in the chart
    Then the api readiness probe passes and no other schema is reachable from the pod
    Then the build ID and the image digest of the release are recorded

  Scenario: AC2 The migration and the library tables are applied and the drift gate is green (new, D-RCV-60)
    Given the migration job of the service
    When it runs before the worker starts
    Then "proceeds" and the four library tables exist in "rwb_payment" with the key and the indexes of the baseline
    Then the drift gate compares the applied state with the baseline and passes
    Then a second run of the migration changes nothing

  Scenario: AC3 The workflow is registered and the event starts the run (new, D-RCV-60)
    Given the worker of the release
    When it starts
    Then "matchPayments" and its four activities are registered on the queue "rwb-payment" in namespace "rwb-recovery"
    Then the worker versioning policy names the build ID of the release
    Then "AceDataReady" for sourceSystem ALS with status COMPLETED and a business date starts exactly one execution
    Then no Schedule is created for the job

  Scenario: AC4 The topic, its retry and dead-letter topics and the consumer group exist (new, D-RCV-60)
    Given the event platform of the namespace
    When the release is applied
    Then "rwb.payment.events.v1", "rwb.payment.events.v1.retry" and "rwb.payment.events.v1.dlt" exist with their partition and retention values
    Then the consumer group "rwb-payment.rwb.source-data.events.v1" is registered on "rwb.source-data.events.v1"
    Then the outbox relay of the worker publishes to the service topic and reports its lag

  Scenario: AC5 Every alert carries a message ID and one owned runbook entry (new, D-RCV-60)
    Given the five alerts of the release
    When each of the five failure paths is simulated in a non-production environment
    Then the alert fires with its message ID, its service and its business date
    Then the alert links one runbook entry with an owner role
    Then the four dashboard series and the run view of JOB-07 show the run and its summary

  Scenario: AC6 The flag governs the run and the backfill is idempotent (new, D-RCV-60)
    Given the flag "rwb.payments.matching" is off
    When "AceDataReady" arrives for a business date
    Then the date is held and no proceeds row and no event is written
    When the flag is on and the same date is backfilled after a failed run
    Then the execution replays and writes no second row and no second event
    Then the backfill limit per run is a value of the environment

  Scenario: AC7 A rollback drains the build without losing a run (new, D-RCV-60)
    Given a running execution on the current build
    When the previous chart and build ID are redeployed
    Then the running execution finishes on the build that started it
    Then a new business date starts on the previous build
    Then the alerts and the run view keep reading both builds

  Scenario: AC8 The business rules of section 8 each have a passing test (new, D-RCV-60)
    Given the rules BR1 to BR10 of section 8
    When the test cases of section 16 run against the release
    Then each rule has a passing test and a rule without a criterion is checked by a boundary test

  Scenario: AC9 A consumed event delivered twice starts one execution (new, D-RCV-60)
    Given the event "AceDataReady" for one business date
    When the same event is delivered a second time
    Then the second delivery writes no second proceeds row and no second event
    Then the key of the write is the business date and the payment

  Scenario: AC10 A consumed call that fails or does not answer is bounded (new, D-RCV-60)
    Given a consumed contract that fails or does not answer
    When the run calls it
    Then the call ends at the 2 s timeout and the breaker of that downstream protects the run

  Scenario: AC11 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change that the model does not allow
    When the run applies it
    Then the change is refused and no row changes its state
```

The eleven criteria test the deployment only. No business value, amount, date or plan of the legacy story is fixed by them; the only dates they name are the business date of the run and the values of the environment (ASM-4145).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One image, two deployments, one login and one queue per service; no deployment reaches another schema | DP-01, DP-02, R4 |
| BR2 | The migration runs before the worker and a drift fails the release | DP-15 |
| BR3 | The workflow is registered on `rwb-payment` and started by `AceDataReady`; no Schedule is created | DP-10 |
| BR4 | The topic, its retry and dead-letter topics and the consumer group exist before the first business date | DP-09 |
| BR5 | Every alert names a message ID and one owned runbook entry; no alert without a message ID is released | R7.2 s14 |
| BR6 | A run whose batch is not complete writes nothing and is not retried against stale data | Legacy BR5; CTL-02 |
| BR7 | No package in force is a failed run and never a default match | Legacy BR10; R-UNI-41 |
| BR8 | A consumed contract is called with one hop and a 2 s timeout, and a breaker per downstream protects the run | DP-11; ADR-020 |
| BR9 | A backfill is safe to repeat and writes nothing twice; the key is the business date and the payment | DP-09; legacy AC6 |
| BR10 | A rollback drains in-flight runs and never kills an execution; a new date starts on the rollback build | R8.2; AC7 |

### 9. State transitions

None of business data: this story changes no record and no case state. The states it owns are the deployment and the run.

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | The chart is applied and the migration passes | The drift gate is green | Deployed, the worker registered |
| Deployed | The flag is off | X7 | Deployed, the date held |
| Deployed | `AceDataReady` for a new date | The batch is COMPLETED and a package is in force | Running, then completed with its summary |
| Running | A failure path fires | X1 to X5 | Failed with its alert; the date is backfillable |
| Deployed | A rollback is applied | AC7 | The previous build serves new dates; the running execution finishes |
| Deployed | The outbox has a message in `.dlt` | X6 | The run is not complete until the replay |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps team | Applies the chart, runs the migration, registers the workflow, creates the topics and the consumer group, owns the releases and the rollback |
| Platform administrator | Allocates the login and the secret references, the queue and the namespace objects |
| The observability owner (RWB-PLT-OBS) | Owns the collector, the dashboard template and the alert routing; the thresholds are values of the environment |
| The event platform owner (RWB-PLT-EVT) | Owns the topic template, the partition and retention policy and the dead-letter replay procedure |
| The workflow kit owner (RWB-PLT-WF) | Owns the registration contract, the worker versioning policy and the visibility view |
| RW-CREDITAD, Credit Administration officer | Reads the run view and receives the alert of a failed run; changes nothing in the deployment |
| RW-COE, center of excellence analyst | Owns the package the failed run names; loads the version, not the release |
| The service owner of rwb-payment | Approves the runbook entries and the on-call rota |

No person is named in this story: every duty is a role, and every alert routes to a role.

### 11. Data

| Object | Owner | What this story does | BR Field ID |
|---|---|---|---|
| `proceeds` and the four library tables in `rwb_payment` | P8 and the PLT libraries | Creates them by the migration and checks the drift; writes no row | Not specified in the source documents (DOR-RWB-P8-E2008-OPS-7) |
| The secret references of the login and of the service clients | Platform secret store | References them in the chart; holds no value in a file, a chart value or a pipeline log | Not specified in the source documents (DOR-RWB-P8-E2008-OPS-7) |
| The topic `rwb.payment.events.v1`, its `.retry` and `.dlt` | P8, on the event platform template | Creates them with their partition and retention values | Not specified in the source documents (DOR-RWB-P8-E2008-OPS-7) |
| The consumer group `rwb-payment.rwb.source-data.events.v1` | P8 | Registers it on `rwb.source-data.events.v1` before the first business date | Not specified in the source documents (DOR-RWB-P8-E2008-OPS-7) |
| The workflow registration and its build ID | P8, on the workflow kit | Registers the workflow (Not specified in the source documents (CG-ALL-7552)) and its four activities; owns the versioning policy of the release | Not specified in the source documents (DOR-RWB-P8-E2008-OPS-7) |
| The five alerts, the four series and the run view | P8 with the observability owner | Creates them; the thresholds and windows are values of the environment | Not specified in the source documents (DOR-RWB-P8-E2008-OPS-7) |
| The outcome records of the run summary | P8 | Read from the workflow visibility view; no personal field is written | Not specified in the source documents (DOR-RWB-P8-E2008-OPS-7) |

No personal data enters a deployment object, an alert, a dashboard series or a log: an alert names the service, the source system, the business date and the message ID, and never an account, a payment or a customer.

### 12. Contract

#### 12.1 REST operations provided

None new. The two operations of the service — `GET /proceeds` and `POST /proceeds/{proceedsId}/match` on `/api/recovery/payment/v1` — are deployed by this story as they are tagged in RWB-P8-E2008-CON, behind the gateway-bff composite route (DP-19). This story changes no path, no body and no error, and publishes no health or admin route of its own beyond the platform probe.

#### 12.2 REST operations consumed

| Operation | Base | Owner | Deployment note |
|---|---|---|---|
| Payments, next installment date and batch status of the ALS source | `/api/recovery/source-data/v1` | P1 rwb-source-data | the client is configured with a 2 s timeout, one GET retry with jitter and a breaker |
| Open case and running plans of a case | `/api/recovery/case/v1` and RWB-P3-E2004-CON | P3 rwb-case | same policy; the plan is read before the match of a payment |
| Parameters, lists and the package in force | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E2042-CON | P3 and P7 | read once per run and cached for the run, with the version of each |

The operation names are those of the baseline and carry the placeholder where no published document fixes them (GAP-2505; ASM-4145).

#### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | the topic and its `.retry` and `.dlt` are created with the values of the environment; the outbox relay publishes |
| `rwb.payment.PaymentMissed.v1` (EV-12) | `rwb.payment.events.v1` | as above; the alert on the DLT covers a failed publish |
| `rwb.payment.TreatmentBooked.v1` (EV-11) | `rwb.payment.events.v1` | the topic is shared with the booking story; this release creates it and publishes nothing of it |
| `DecisionRecorded` (EV-08) | `rwb.decision-record.v1` | written by the library; the topic belongs to rwb-decision and is not created here |

#### 12.4 Events consumed

| Event | Topic | Consumer group | Provisioning | Owner |
|---|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1` | `rwb-payment.rwb.source-data.events.v1` | the run starts only on `sourceSystem` ALS and `status` COMPLETED; the group is registered before the first business date and its offset policy is the environment's | rwb-payment |
| `RulePackageInForce` (EV-30) | `rwb.decision.events.v1` | `rwb-payment.rwb.decision.events.v1` | registered with the booking story; this release creates the group only | rwb-payment |

The other five subscriptions of the service belong to the booking and Epic 4 stories and are not registered here.

#### 12.5 Workflows and activities

| Name | Type | Registration |
|---|---|---|
| Not specified in the source documents (CG-ALL-7552; GAP-0144; ASM-0225) | Workflow (event-started) | registered on queue `rwb-payment`; the build ID pins the worker version; the execution id derives from the source and the business date |
| `readFacts`, `evaluateMatch`, `recordAndApply`, `raiseMissedPayment` | Activities | registered with the workflow; the retry policy is the kit's, `NoPackageInForce` is non-retryable |
| Not specified in the source documents (CG-ALL-7553) | Workflow and activity | registered on queue `rwb-payment` by the booking story and the debt-sale journey; this release does not register them |

The registration check asserts the queue, the workflow type, the input schema and the absence of a Schedule. The build ID and the versioning policy are values of the release and are recorded with it (GAP-2505; ASM-4146).

#### 12.6 Schedules

None. No Schedule, cron, overlap policy or catch-up window is created for this service. The run follows `AceDataReady` from the bank's Airflow edge; the outbox relay is a library component inside the worker and not a Schedule.

#### 12.7 Tables owned

| Object | Owner | Applied by |
|---|---|---|
| `proceeds` | P8 (`rwb_payment`) | the migration job of this release, before the worker starts |
| `decision_record`, `inbox_event`, `outbox_event`, `idempotency_key` | PLT libraries in `rwb_payment` | the library migration of the same job |
| The flyway history of `rwb_payment` | P8 | the job's own record; the drift gate reads it |

The job is scoped to `rwb_payment` and uses the P1 workload contract for ACE facts. The deployment requests no ACE-view grants.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Environment stub of rwb-source-data | the payments, the next installment date and a COMPLETED, a FAILED and an absent batch status | the run and alert checks of a non-production environment |
| Environment stub of rwb-decision | a package in force, a second version and no version in force | X3 and AC5 |
| Environment stub of rwb-case and the treatment record | the open case and the running plans of a synthetic account | AC3 and AC6 |
| Fault stub of the record library | a stopped chain answering MSG-P7-003 | X4 and AC5 |

The stubs are the CON fakes of RWB-P8-E2008-CON driven by an environment switch; they are never enabled in production.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided by the service, 9 consumed | the two operations behind the composite route; the clients of 12.2 with one hop and 2 s |
| Kafka | 3 published, 2 groups registered | the service topic with `.retry` and `.dlt`; the consumer group of EV-26 and the group of EV-30 |
| Temporal | 1 workflow, 4 activities, 1 queue | `matchPayments` on `rwb-payment`; no Schedule |
| File | None | no file is transferred or delivered by this release |

### 13. Solution plan

**Chart.** `deploy/rwb-payment/`: one image, two deployments (`api`, `worker`), the migration job, the route fragment, the alert rules, the dashboard, the runbook links and the values files per environment.

| Component | Type | Responsibility |
|---|---|---|
| `api` deployment | Deployment | serves the two operations behind the gateway-bff, with its readiness and liveness probes |
| `worker` deployment | Deployment | polls `rwb-payment`, registers the workflow and its activities, runs the outbox relay |
| `migrate` job | Job | runs the Flyway sequence and the library migration before the worker; the drift gate reads its result |
| `topics` manifest | Manifest | the service topic, its `.retry` and `.dlt`, and the two consumer groups |
| `alerts` rules | Rules | five alerts, each with a message ID, a label set and a runbook link |
| `dashboard` | Chart | four series: runs by outcome, payments read and matched, unmatched receipts, outbox lag |
| `runbook` | Document | five entries: event not received or worker not polling; stale batch; no package; record chain stopped; outbox lag or DLT |

| Runbook entry | Trigger | First step | Owner role |
|---|---|---|---|
| 1 | No execution by the run window | check the relay of rwb-source-data and the worker registration | DevOps team |
| 2 | MSG-P1-001 on the plan view or the run | check the batch status of the source and the business date; do not force the run | DevOps team with the data owner |
| 3 | MSG-P3-027 and MSG-P8-002 | confirm no version is in force and page the package owner; do not load a version here | RW-COE |
| 4 | MSG-P7-003 and a stopped chain | check the record store, then backfill the date | DevOps team with the platform record owner |
| 5 | The lag series or a `.dlt` message | find the cause, replay the message, confirm the run completes | DevOps team with the event platform owner |

**Build steps.** (1) Write the chart, the probes and the migration job; test AC1 and AC2. (2) Register the workflow and the versioning policy; test AC3. (3) Create the topics and the consumer groups; test AC4. (4) Write the five alerts, the four series and the five runbook entries; test AC5. (5) Wire the flag, the backfill and the rollback; test AC6 and AC7.

### 14. Validation and messages

| ID | When | Alert and text |
|---|---|---|
| MSG-P1-001 | The ACE batch is late or not complete | the run is skipped; the text names the product and its date |
| MSG-P8-001 | The run summary carries unmatched payments | the summary text only; no alert of its own |
| MSG-P8-002 | No `PAYMENT_MATCH` version is in force | the failed-run alert carries the text and the business date |
| MSG-P3-027 | The rule version is refused | the failed-run alert carries the refusal detail, the package code and the date only |
| MSG-P7-003 | The record cannot be written | the incident alert carries the text and the business date; the date is backfillable |

The texts are the legacy texts of RWB-E2-008 section 14, unchanged; the English text of MSG-P1-001, MSG-P8-001, MSG-P8-002, MSG-P3-027 and MSG-P7-003 is Not specified in the source documents (DOR-RWB-P8-E2008-OPS-9). MSG-P4-002 is the API's 403 and needs no alert. An alert never carries an account, a payment reference or a customer value. This story delivers no screen; SCR-28 and SCR-44 have no empty, loading, error or no-access state here, and Not specified in the source documents (DOR-RWB-P8-E2008-OPS-10) for those states.

### 15. Screens and states

No screen is built here. The operator reads the run on the workflow visibility view and on the run view of JOB-07 (SCR-44), and the officer reads the receipts on SCR-28; both are served by the base and the composite route the release deploys. The four dashboard series are the operator's view of the same run.

States. SCR-28: loading, empty, error and no access: Not specified in the source documents (CG-ALL-7562). SCR-44: empty, loading, error and no access: Not specified in the source documents (CG-ALL-7563).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P8-E2008-OPS-01 | AC1 | NFR | the chart applied to a non-production environment; the probes and the route |
| TC-P8-E2008-OPS-02 | AC2 | Component | the migration run twice and the drift gate |
| TC-P8-E2008-OPS-03 | AC3 | End to end | `AceDataReady` for one business date, twice, and the registration query |
| TC-P8-E2008-OPS-04 | AC4 | Component | the topic, its two subtopics and the two consumer groups |
| TC-P8-E2008-OPS-05 | AC5 | NFR | each of the five failure paths simulated, with its message ID and its runbook link |
| TC-P8-E2008-OPS-06 | AC6 | End to end | the flag off, then on, then a backfill of the same date |
| TC-P8-E2008-OPS-07 | AC7 | End to end | a running execution and a rollback to the previous build |
| TC-P8-E2008-OPS-08 | §12 operations, events and activities | Contract | the operations of §12, the events of §12.4 and the four workflow activities |
| TC-P8-E2008-OPS-09 | §12.7 tables | Component | the tables of §12.7 at their boundary: the library tables of the same job, and no table of another schema |
| TC-P8-E2008-OPS-10 | AC8 | Component | each rule BR1 to BR10 of §8 checked against its test in this section |
| TC-P8-E2008-OPS-11 | AC9 | End to end | the same "AceDataReady" event delivered twice for one business date |
| TC-P8-E2008-OPS-12 | AC10 | Component | a consumed contract that fails, and one that does not answer within 2 s |
| TC-P8-E2008-OPS-13 | AC11 | Component | a status change the model does not allow |

The thirteen are new with D-RCV-60 and test the deployment only. Integration copies end in `-ITG` and belong to RWB-ITG-E2008-ITG; the legacy test cases stay with the criteria the APP and CON stories own.

### 17. Guardrails

- No secret in a chart value, a pipeline log or a prompt: the login, the client credentials and the payload keys are secret references only.
- No personal data in an alert, a series, a log or a run input: an alert names the service, the source, the business date and the message ID, and never an account, a payment or a customer.
- No business value in a chart, an alert threshold or a runbook: the package values belong to their owner and the thresholds are values of the environment.
- No deployment reaches another schema, another queue or another topic than the ones named here, and no operator edits a row of `rwb_payment` to fix a run.
- No rollout without the drift gate, the registration check and the five runbook entries in place.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-P8-E2008-OPS-03, TC-P8-E2008-OPS-06 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40 | TC-P8-E2008-OPS-01, TC-P8-E2008-OPS-02, TC-P8-E2008-OPS-04, TC-P8-E2008-OPS-05, TC-P8-E2008-OPS-07 |

The release is cited by RWB-P8-E2008-APP as its external dependency and by the Day-1 allocation of the DevOps lane L-P8-D.

### 19. Out of scope

- The behaviour of the match, the record, the events and the read (RWB-P8-E2008-APP) and the published shapes (RWB-P8-E2008-CON).
- The platform objects themselves — the cluster, the Kafka template, the Temporal namespace, the secret store, the collector and the edge — which are owned by their PLT stories.
- The payment booking story (`TreatmentBooked`) and rwb-integration JOB-08 and the Epic 4 posting and matching stories.
- The reference-data and rule-authoring behaviour of RWB-E2-027 and of rwb-decision.
- Any production change, data fix or manual repair of a business row.
