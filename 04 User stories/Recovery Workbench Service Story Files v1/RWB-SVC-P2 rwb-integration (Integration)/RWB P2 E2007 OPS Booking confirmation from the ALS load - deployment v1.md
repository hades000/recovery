# RWB-P2-E2007-OPS Booking confirmation from the ALS load - deployment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2007-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P2-G |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-CHO-008) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-007 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the booking-confirmation run of rwb-integration deployed on the service's own worker and task queue, registered as an event-started workflow started by `AceDataReady`, with its `job_catalog` row, its Flyway migration, its topic and queue checked, four dashboard series, four alerts and a runbook with its entries**, so that **a missing booking, a differing term, a version not in force and a late ACE batch are visible and actionable by a rota from the first release, without anyone reading a Quartz monitor that no longer exists**.

The legacy story assumed that a Quartz job would start the match after the ACE batch and that the platform team would notice a failed run on a job monitor. In the target JOB-08 is an event-started Temporal workflow (DP-10), and the deployment is where that becomes real: the worker registration, the event trigger, the job catalogue row, the run view, the alerts and the runbook.

This story deploys and proves the deployment only. It builds no workflow, no facts builder and no client: those are RWB-P2-E2007-APP, and the contract they answer to is RWB-P2-E2007-CON. It writes no treatment row and no case row: the treatment is written through its owner's contract and the task through rwb-case. What it owns is the release: the chart and the values files, the migration step, the topic and queue check, the workflow registration, the flag values, the backfill and rerun path, the four series, the four alerts and the four runbook entries.

Architecture v5 slide 44 names rwb-payment the owner of JOB-08. This realignment keeps JOB-08 and its activities with rwb-integration, as RWB-P4-E2007-APP and RWB-ITG-E2007-ITG both state and as RWB-P2-E2007-APP builds it, so the release registers the workflow on the `rwb-integration` queue and records the conflict rather than shipping a job nobody starts (GAP-0659; ASM-1126).

### 2. Business rationale

The booking confirmation is the control that keeps an approved restructure or settlement from waiting unseen: R-RES-22 and R-SET-13 take the case out of an operations-waiting state only when the booked terms appear in the next ALS batch, and the legacy measure REC-03 sets the number of approved treatments that are still unbooked after two days at zero. Three operational facts make the deployment a story of its own.

First, the run is started by another service's event. A worker that is down, an inbox table that is not in the deployed schema, or a consumer group that is not registered means no run at all, and silence looks exactly like a business day with every booking confirmed. Second, the outcome is a comparison against a rule package, so a package version that is not in force is a refusal and not a match: if the alert for that case is missing, the Workbench stops confirming and nobody is told. Third, the two failure modes the officer cares about — a booking that never appears and terms that differ — are raised as tasks inside the run, so the alerts must carry the count of each, not only an exit code.

The deployment therefore carries the state of the run as data. Four series answer the questions a rota asks: how many treatments were read, how many were booked, how many are missing, and how many differ; with the run outcome and duration beside them. Four alerts carry a message ID and one runbook entry each, so an operator acts without reading code: MSG-P2-011 for a missing-booking wave, MSG-P2-012 for a terms wave, MSG-P3-027 for no package in force, and MSG-P1-001 for a late or incomplete ACE batch.

The release also makes the flag real. `rwb.integration.booking-confirmation` is kept as the legacy reference of the switch, and the switch itself is a feature flag of the platform flag library (R-PREC default ruling). Off, the run ends `SKIPPED` with no read and no write. No environment value is hard-coded: the replica counts, the resource sizes, the thresholds and the backfill limit are values files, as DP-06 requires.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit, the `rwb-recovery` namespace, worker versioning and the build ID provider exist (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The platform flag library is available and the flag `rwb.integration.booking-confirmation` is registered for this service (RWB-PLT-E1047-CON; R-PREC default ruling on feature flags).
- The `rwb_integration` schema and its Flyway sequence exist, with `interface_config`, `outbound_item`, `job_catalog` and the library tables `decision_record`, `idempotency_key`, `outbox_event`, `outbox_delivery` and `processed_event` (RWB-PLT-E1044-CON; RWB-P2-E1007-APP).
- The service topic `rwb.integration.events.v1` with its retry and `.dlt` topics, the shared `rwb.decision-record.v1` topic and the consumer access to `rwb.source-data.events.v1` and `rwb.treatment.events.v1` exist (RWB-PLT-EVT, RWB-PLT-TE006-CON).
- The platform error envelope and the message catalogue are in force, so an alert can carry a message ID.
- The operation of RWB-P2-E2007-CON is published, and its fakes answer every consumed path; RWB-P2-E2007-APP delivers the workflow and its six activities on `rwb-integration`.
- The environments DEV, SIT and UAT exist; the wave 2 release deploys to DEV, SIT and UAT, and the production values are a later promotion of the same artefacts.
- The payload codec and the codec server of the namespace are in force (RWB-PLT-WF).
- No source names the per-service login, the secret reference or the worker identity of rwb-integration under DP-02 (GAP-0659; ASM-1129).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image with the embedded Drools kit and the contract client jar, runs the unit, component and contract tests of RWB-P2-E2007-CON, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the rwb-integration worker with its own login, the namespace `rwb-recovery`, the task queue `rwb-integration`, the payload codec and the build ID of the release.
3. The migration step applies the `rwb_integration` Flyway sequence, including `V2007_1__booking_match.sql`, and refuses to promote when the library tables or the indexes are absent.
4. The topic and queue step confirms the topic `rwb.integration.events.v1` with its retry and `.dlt` topics, the shared `rwb.decision-record.v1`, the notification subscription on `rwb.source-data.events.v1` and `rwb.treatment.events.v1` with this service's consumer group, and the task queue `rwb-integration` in the namespace.
5. The registration step confirms that the worker polls `rwb-integration` only, that `BookingMatchWorkflow` and its six activities are registered, and that `AceDataReady` starts the workflow with the `booking-match-` prefix (GAP-0659; ASM-1126).
6. The job catalogue step writes or updates the JOB-08 `job_catalog` row with the event trigger as its schedule text, the owner role, the run book path and the alert threshold, so the catalogue read of the integration base returns it.
7. The flag step sets `rwb.integration.booking-confirmation` from the values of the environment and confirms that the run outcome follows it: off ends the run `SKIPPED` with no write.
8. The backfill and rerun step runs the workflow for a stated business date through the rerun operation with an `Idempotency-Key`, reports the counts, and refuses a date already completed for the same key.
9. The dashboards are published with the four series and the environment, the release and the build ID as dimensions.
10. The four alerts are wired to MSG-P2-011, MSG-P2-012, MSG-P3-027 and MSG-P1-001 and to their runbook entries.
11. A smoke step confirms one synthetic treatment in DEV through the backfill and checks that the treatment contract received exactly one mark-booked call, that the task was raised once, and that a repeat raises no second task and no second `TreatmentBooked`.
12. The release record is written with the chart version, the image digest, the build ID, the package version in force and the run reference of the smoke step.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render, the image pull or the migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1, AC2 |
| X2 | The library tables or the index of `V2007_1__booking_match.sql` are absent after the migration | The migration step fails the release; the run cannot start | None | AC2 |
| X3 | The worker polls a task queue other than `rwb-integration`, the workflow is not registered, or the event subscription is absent | The registration step fails the release; the missing-booking and the late-batch alerts would otherwise fire on a service that cannot run | MSG-P1-001 | AC3 |
| X4 | The flag is off in an environment and the run still reads or writes | The flag step fails the release, because a paused switch must pause the run | None | AC6 |
| X5 | A backfill or rerun is asked for a date already completed under the same key | The stored answer is replayed and nothing is run again | None | AC6 |
| X6 | A run ends with no bookable treatment and a missing-booking wave | The MSG-P2-011 alert fires with the count, the treatment IDs and the accounts, and the runbook entry names the officer role | MSG-P2-011 | AC4 |
| X7 | A terms wave, or a package version not in force | The MSG-P2-012 or the MSG-P3-027 alert fires with the count, the package code and the business date | MSG-P2-012, MSG-P3-027 | AC4 |
| X8 | The ACE batch for ALS is late or ended not COMPLETE | The run ends `SKIPPED` with no missing-booking task, and the MSG-P1-001 alert names the product and the date | MSG-P1-001 | AC4 |
| X9 | The worker stops while a run is in flight | The task stays on the queue, the worker returns and the run resumes from history; the stuck-run entry names the check | None | AC3, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the flag library and the published contract; no application code is built here |
| Negotiable | Replica counts, resource sizes, thresholds, probe timings and the backfill limit are environment values |
| Valuable | Makes the run, its four outcomes and its four failure modes observable and operable before the release, so REC-03 can be read from a dashboard |
| Estimable | One chart, one migration step, one topic and queue check, one registration check, one catalogue row, one flag step, one backfill, four series, four alerts and four runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the migration applies, the worker registers, the run is started by the event, the alerts fire on a synthetic series |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the booking-confirmation run for rwb-integration

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-integration is rwb-integration
    Given the target environment is SIT

  Scenario: AC1 The service and the rerun operation are deployed with the rwb-integration login (new, D-RCV-60)
    Given the rwb-integration chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the deployment declares the rwb-integration login and no other service's credential
    Then POST /api/recovery/integration/v1/admin/jobs/{jobId}/rerun answers through gateway-bff in each environment
    Then the readiness probe reports healthy only after the first successful poll and the first successful authorise call, and the liveness probe writes nothing
    Then the worker image carries the embedded Drools kit of RWB-PLT-E1072-CON and no second rule engine

  Scenario: AC2 The migration, the library tables and the JOB-08 catalogue row are applied (new, D-RCV-60)
    Given the rwb_integration Flyway sequence and V2007_1__booking_match.sql
    When the migration step runs against a fresh environment
    Then the schema holds interface_config, outbound_item, job_catalog and the library tables decision_record, idempotency_key, outbox_event, outbox_delivery and processed_event
    Then the indexes of decision_record and idempotency_key used by the one-record and repeat-run reads exist
    Then one job_catalog row names JOB-08 Booking confirmation, its event trigger as schedule text, its owner role, its runbook path and its alert threshold
    Then the catalogue read of the integration base returns that row
    Then no table of rwb_treatment, rwb_case, rwb_source_data or recovery is created, read or granted by the migration

  Scenario: AC3 The worker registers the workflow and the event subscription starts it (new, D-RCV-60)
    Given a running rwb-integration worker
    When the registration step asks the namespace what the worker polls and what it registers
    Then the worker polls rwb-integration and no other task queue
    Then BookingMatchWorkflow is registered with the workflow ID prefix booking-match-
    Then readBookedTerms, listApprovedTreatments, evaluateBookingMatch, applyBookingOutcome, raiseBookingTasks and writeRunSummary are registered with the retry policy of the kit
    Then AceDataReady on rwb.source-data.events.v1 starts the workflow for the business date, and a duplicate is dropped through processed_event
    Then the payload codec is attached to every client and worker of the deployment
    Then no Schedule is created, because JOB-08 is event-started

  Scenario: AC4 The four alerts carry a message ID and one runbook entry each (new, D-RCV-60)
    Given the published alert rules and the runbook of the deployment
    When a missing-booking wave, a terms wave, a run with no package in force and a late ACE batch are simulated
    Then the first alert fires with MSG-P2-011, the count of missing treatments, the treatment IDs and the accounts not booked
    Then the second alert fires with MSG-P2-012 and the count of differing treatments
    Then the third alert fires with MSG-P3-027, the package code BOOKING_MATCH and the business date
    Then the fourth alert fires with MSG-P1-001, the product ALS and the business date
    Then each alert links one runbook entry with the check, the owner role and the recovery step, and its threshold is a value of the environment

  Scenario: AC5 The four dashboard series and the runbook cover the run (new, D-RCV-60)
    Given the published dashboard and the runbook of the deployment
    When a normal run, a run with a missing booking, a run with differing terms and a run with no package in force are simulated
    Then the dashboard shows the treatments read, the treatments booked, the treatments missing and the treatments differing per business date
    Then the run outcome, the duration and the failed consumed calls are shown beside them
    Then each series carries the environment, the release and the build ID as dimensions
    Then the runbook entries name the check, the message ID, the owner role and the recovery step, and the entries are reviewed by the on-call rota

  Scenario: AC6 The flag governs the run and the backfill is idempotent (new, D-RCV-60)
    Given the flag rwb.integration.booking-confirmation in the platform flag library
    When the flag is off in an environment and the event arrives
    Then the run ends SKIPPED with no treatment read, no mark-booked call and no task
    When the flag is on and the backfill runs BookingMatchWorkflow for business date 2026-12-16 with one Idempotency-Key
    Then each synthetic treatment is handled once and the run reports the counts of read, booked, missing, differing and skipped
    When the same backfill runs again with the same key
    Then the stored answer is replayed, no treatment is handled twice, no second task is raised and no second TreatmentBooked is published
    Then a backfill for a date already completed under the same key writes nothing
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one task queue, one login: the worker polls `rwb-integration` in namespace `rwb-recovery` and carries the rwb-integration login only | Arch v5 slides 24 and 41; DP-02; DP-10 |
| BR2 | Every worker carries the build ID of its release and worker versioning is enabled, so a new build takes new runs while the old build drains | Temporal and Drools design slide 27; RWB-PLT-E1071-CON |
| BR3 | JOB-08 is started by `AceDataReady` and by nothing else: no Schedule is created for it, and the `job_catalog` row records the event trigger | Arch v5 slides 42 and 44; DP-10; GAP-0659; ASM-1126 |
| BR4 | The release writes `rwb_integration` only and holds no grant on `recovery` or on another `rwb_*` schema; the treatment is written through its contract and the task through rwb-case | DP-01; DP-05; BR12 of RWB-P2-E2007-APP |
| BR5 | The flag is the platform flag library's and its legacy name is kept as the reference of the switch; off means a skipped run and no write | R-PREC default ruling; BR14 of RWB-P2-E2007-APP |
| BR6 | The backfill and the rerun are idempotent by job, business date and `Idempotency-Key`: one run, one record and at most one open task per case, task code and treatment | Legacy RWB-E2-007 X5 and X6; AC6 of RWB-P2-E2007-APP; GAP-0659; ASM-1131 |
| BR7 | Every alert carries a message ID and the agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | No environment value is hard-coded: replicas, resources, thresholds, probe timings and the backfill limit come from values files and the flag library | DP-06 principle; Template and Rules §R7.2 s17 |
| BR9 | Dashboard series, alert payloads and the runbook carry counts, treatment IDs, case IDs, account keys, role codes, version labels and build IDs only, never a person's data and never a decoded payload | Arch v5 slide 42 (PDPA) |
| BR10 | A failing release never replaces a working one, and a run left half-applied is picked up by the next business date rather than repaired by hand | Temporal and Drools design slide 27; DP-10 |
| BR11 | The package version in force is a registry value of rwb-decision; the release records the version it tested against and never pins one in a service table | DP-04; RWB-P2-E2007-CON |
| BR12 | No data lake, no lake file and no lake target is deployed by this release | DP-17; Arch v5 slide 37 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Migration applied | The schema, the library tables, the indexes and the JOB-08 row exist | Migrated |
| Migrated | Worker registered and probes healthy | The worker polls `rwb-integration` only and the seven registrations exist | Ready |
| Ready | `AceDataReady` arrives | The flag is on and the batch for the date is COMPLETE | Running |
| Ready | `AceDataReady` arrives | The flag is off, or the batch is not COMPLETE | Skipped (no write) |
| Running | The run completes | Every outcome applied and every task raised or already open | Completed |
| Running | No package in force | The registry answers `NoPackageInForce` | Failed, with the MSG-P3-027 alert |
| Completed | A rerun with the same key | The idempotency record holds the key | Completed, answered from the store |
| Any | Release superseded | A new chart version passes the tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open runs | Ready |
| Any | A failing release or a failed migration step | The previous release stays in force and the pipeline stops | Previous state |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the migration step, the registration check, the catalogue row, the backfill, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the worker versioning policy, the task queue and the flag library registration; reruns JOB-08 for a business date |
| Platform workflow kit owner | Owns the event-started start, the retry policy and the codec server |
| Release manager | Approves the promotion of one artefact and may block it on a failed check |
| On-call operator | Runs the four runbook entries and opens an incident when a run stalls or `NoPackageInForce` persists |
| RW-PLATADM, platform administrator | Reruns JOB-08 and reads the job catalogue and the run view (Platform administration, U and R) |
| RW-DATASTEW, data steward | Reads the REC-03 break list the run feeds |
| RW-COE, center of excellence analyst | Receives the no-package alert, because the package rows are its to load and approve |

The worker runs as the rwb-integration service identity (DP-02), carried by the chart as a secret reference and never as a literal name. The identity name is Not specified in the source documents (GAP-0659; ASM-1129). The four runbook entries and the roles that own them are those of the on-call rota (GAP-0659; ASM-1128).

### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, flag value, alert thresholds, backfill limit |
| Task queue | `rwb-integration` in namespace `rwb-recovery`, polled by the rwb-integration worker only |
| Workflow | `BookingMatchWorkflow`, workflow ID prefix `booking-match-`, started by `AceDataReady`; six activities; no Schedule |
| Job catalogue row | `job_catalog` of `rwb_integration`: job_id, job_name JOB-08 Booking confirmation, owner_role, schedule_text (the event trigger), runbook_path, expected_minutes, alert_after_minutes, first_release |
| Dashboard series | Treatments read; treatments booked; treatments missing; treatments differing; with the run outcome, the duration and the failed consumed calls beside them |
| Alerts | Four rules: MSG-P2-011 missing-booking wave, MSG-P2-012 terms wave, MSG-P3-027 no package in force, MSG-P1-001 late or incomplete ACE batch |
| Runbook entries | Event not received or worker not polling; missing-booking wave; terms wave; no package in force and late ACE batch |
| Secrets | The rwb-integration login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |
| Test data | The synthetic treatments `TRT-SYN-0701` to `TRT-SYN-0704`, cases `RW-2026-000701` and `RW-2026-000702` and accounts `A-0701` to `A-0705`, in DEV and SIT only |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread and ingress class) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value, and this story fixes only their names and the rule that they are never hard-coded.

**Probes.** Readiness answers healthy only after the worker has polled `rwb-integration` once, the codec is attached and one authorise call has succeeded; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database or starts a run, and a failing dependency is reported as not ready, never as live-and-broken. The paths and timings are values of the environment.

The four alert thresholds, the aggregation window of the four series and the run-window expectation of the late-batch alert are values of the environment and are reviewed with the business on-call owner (GAP-0659; ASM-1127); the four runbook entries and their owners are those of the on-call rota (GAP-0659; ASM-1128); and the backfill limit per run is a value of the environment too (GAP-0659; ASM-1131).

### 12. Contract

#### 12.1 REST operations provided

None of its own. The rerun operation of this key is provided by RWB-P2-E2007-APP and documented in RWB-P2-E2007-CON; this story deploys it, checks it and declares no path. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None. The deployment needs no REST client of its own: the worker calls the contracts of rwb-treatment, rwb-source-data, rwb-case, rwb-decision and rwb-access inside the activities, and the pipeline calls the platform registry and the secret store only.

#### 12.3 Events published

None. The release publishes no event type. `rwb.integration.events.v1` carries `FileDelivered` and `FileFailed`, which belong to the outbound-file stories of this service; the ledger event `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the decision-record library inside the run (DP-03); and `rwb.payment.TreatmentBooked.v1` is rwb-payment's event and is not produced here.

#### 12.4 Events consumed

None registered by this story of its own beyond the two subscriptions the run needs, which the registration step checks and does not create:

| Event | Topic | Owner | Deployment element |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | The trigger of `BookingMatchWorkflow`; the consumer group and the subscription are confirmed by the registration step and deduplicated through `processed_event` |
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | The approval date the match compares with the booked date; deduplicated through `processed_event` |

No other topic is subscribed, no topic is created by this release and no producer group is registered.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| `BookingMatchWorkflow` | Workflow, workflow ID prefix `booking-match-` | `rwb-integration` | Registered by the worker of this release with the build ID and worker versioning; started by `AceDataReady` and by the backfill step; no Schedule starts it |
| `readBookedTerms` | Activity | `rwb-integration` | Registered with the retry policy of the kit; `AceBatchNotComplete` is non-retryable and countable |
| `listApprovedTreatments` | Activity | `rwb-integration` | Registered with the same policy |
| `evaluateBookingMatch` | Activity | `rwb-integration` | Registered with the same policy; `NoPackageInForce` is non-retryable and countable |
| `applyBookingOutcome` | Activity | `rwb-integration` | Registered with the same policy; the decision record precedes every remote call |
| `raiseBookingTasks` | Activity | `rwb-integration` | Registered with the same policy; one rwb-case call per treatment |
| `writeRunSummary` | Activity | `rwb-integration` | Registered with the same policy; writes the REC-03 result through rwb-source-data |

**Build ID and versioning.** The build ID is the one the workflow kit supplies for the release commit; worker versioning is enabled and a new build takes new runs while the old build drains. The build ID format and the versioning policy are Not specified in the source documents (GAP-0659; ASM-1130).

#### 12.6 Schedules

None. JOB-08 is an event-started workflow and this release creates no Schedule ID, no cadence and no catch-up window (DP-10; Arch v5 slides 42 and 44). Architecture v5 slide 44 names rwb-payment the owner of JOB-08; this realignment keeps it with rwb-integration and the `job_catalog` row carries the trigger so that an operator can see how the run starts (GAP-0659; ASM-1126). The Temporal Schedule inventory of this service is unchanged by this release.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| job_catalog | `rwb_integration` | P2 (Ownership Map; TSD P2 v3 T3.1) | The JOB-08 row is written or updated by the release: job_id, job_name, owner_role, schedule_text, runbook_path, expected_minutes, alert_after_minutes |
| decision_record | `rwb_integration` | PLT library, created in `rwb_integration` (DP-03) | Applied with the baseline; the release adds the index the one-record read uses |
| idempotency_key, outbox_event, outbox_delivery, processed_event | `rwb_integration` | PLT library, created in `rwb_integration` (DP-09) | Applied with the baseline; the release adds the index the repeat-run read uses |

The release applies no other migration and adds no business table. `interface_config` and `outbound_item` are the integration base's and are untouched here. No grant on `recovery` and no grant on another `rwb_*` schema is requested by this release (DP-01, DP-05, BR4; GAP-0659; ASM-1129).

#### 12.8 Contract fakes

None. No fake is deployed: the workflow tests run on `TestWorkflowEnvironment` in the pipeline, and the contract mocks of the consumed services are in-process test doubles of RWB-P2-E2007-CON and RWB-P2-E2007-APP. No WireMock workload is part of this release.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | The rerun of this key is deployed, not declared here; probes are cluster-internal |
| Kafka | 0 published, 2 consumed subscriptions checked | `rwb.source-data.events.v1` and `rwb.treatment.events.v1` are subscribed by the run; no topic, no producer and no other consumer group is created |
| Temporal | 1 workflow, 6 activities, 0 Schedules | Worker on `rwb-integration` with a pinned build ID and worker versioning; `BookingMatchWorkflow` started by `AceDataReady` |
| File | None | The values files and the recorded histories are pipeline inputs, not runtime data |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release writes `rwb_integration` only and reaches the treatment, the task and the account through their owners' contracts | none |
| DP-03 | DecisionLogWriter, decision log | The decision-record library is deployed with the worker and publishes to `rwb.decision-record.v1` through the outbox | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | The embedded kit is part of the worker image, and the model is fetched inside the activity; no second engine is deployed | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read in this release and no view grant; the account facts arrive through rwb-source-data | none |
| DP-06 | Parameters, casewf.config | The grace count and the treatment types are read through the rwb-case contracts; the environment values are values files | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | The reference-data contract of rwb-case is a runtime dependency of the run; no LOV value is deployed | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The outbox, inbox and idempotency tables are applied by the baseline; the subscriptions are checked, not created | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue, the namespace and the event-started start come from the workflow kit; no Schedule is created | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The activities call the consumed contracts with the 2 s budget; the deployment adds no REST path | none |
| DP-13 | `/api/recovery/v1` | The deployed base is `/api/recovery/integration/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff serves the screens; the deployment registers no route of its own | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-integration/` overlay | Worker deployment, config map, secret references, probes, task queue and namespace, flag reference, build ID, alert thresholds |
| `helm/rwb-integration/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, thresholds, backfill limit, build ID, environment |
| Pipeline stage | Build, unit, component and contract tests, image and dependency scan, chart publish, promotion |
| Migration step | Applies the `rwb_integration` sequence including `V2007_1__booking_match.sql`, and refuses to promote when the tables or indexes are absent |
| Topic and queue step | Confirms the service topic with its retry and `.dlt`, the shared ledger topic, the two subscriptions and the task queue |
| Registration check | Worker polls `rwb-integration` only; the workflow and six activities are registered; the codec is attached; `AceDataReady` starts the workflow (GAP-0659; ASM-1126) |
| Job catalogue step | Writes or updates the JOB-08 `job_catalog` row with the event trigger, the owner role, the run book path and the threshold |
| Flag step | Sets `rwb.integration.booking-confirmation` from the environment and confirms that the run outcome follows it |
| Backfill and rerun step | Runs the workflow for one business date under an `Idempotency-Key` and reports the counts |
| Dashboards | The four series of section 11 with the run outcome, the duration and the failed calls |
| Alerts | Four rules, each with a message ID and one runbook entry |
| Runbook | Four entries: event not received or worker not polling; missing-booking wave; terms wave; no package in force and late ACE batch |

**Alert mapping.** The four conditions, the thresholds and the run-window expectation are values of the environment and are reviewed with the business on-call owner (GAP-0659; ASM-1127); each row links one runbook entry whose owner and review cycle are fixed by the rota (ASM-1128); and the four texts, MSG-P1-001 included, are the catalogue's (GAP-0659; ASM-1132).

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P2-011 | The count of treatments with no booking after the grace batches rises above the threshold in one run | Missing-booking alert with the treatment IDs and the accounts not booked | Team manager of RW-RESTRUCT and platform on-call, page |
| MSG-P2-012 | The count of treatments with differing terms rises above the threshold in one run | Terms alert with the treatment IDs and the count | Credit Administration team manager, ticket |
| MSG-P3-027 | The `NoPackageInForce` count is above zero for a business date, or no version is in force at the run start | No-version alert naming the package code BOOKING_MATCH and the business date | Business on-call (RW-COE), page |
| MSG-P1-001 | The ACE batch for ALS is not COMPLETE at the run window, or no `AceDataReady` arrived inside twice the expected window | Late-batch alert naming the product ALS, the business date and the last complete batch | Platform on-call, page |

**Backfill and rerun.** The backfill step runs `BookingMatchWorkflow` for a stated business date under an `Idempotency-Key`. It handles only the treatments not yet handled for that date, raises at most one open task per case, task code and treatment, and reports the counts. A date already completed under the same key replays the stored answer and runs nothing; a treatment that failed on a consumed contract is picked up by the next business date, so no repair script exists. The backfill limit per run is a value of the environment (ASM-1131).

**Rollback.** A release that fails a check is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open runs until they finish; no Schedule is paused because none exists. The run is idempotent by job, business date and key, so no data repair is needed; a treatment handled by the new build is skipped by the old one through the same idempotency record. The build ID is the workflow kit's for the release commit and worker versioning carries the rollback (GAP-0659; ASM-1130).

**Feature switch.** `rwb.integration.booking-confirmation`, kept as the legacy reference of the switch and read from the platform flag library. On: the run reads, matches and writes, and the rerun operation answers. Off: every run ends `SKIPPED` with no read and no write, and the rerun answers the feature-off message. The flag is never a value of a service table, and its value is read at the start of every run so that a change needs no redeploy.

**Done when.** The chart renders for DEV, SIT and UAT, the migration step applies and fails closed, the topic and queue and registration checks pass, `AceDataReady` starts the workflow on `rwb-integration`, the JOB-08 catalogue row is read back, the flag governs the run, the backfill is idempotent, the four series and the four alerts are published, the four runbook entries are reviewed by the on-call rota, and the smoke run of one synthetic treatment ends with exactly one mark-booked call, one task and no second task on a repeat.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-011 | The missing-booking wave crosses the threshold, or a run raises missing-booking tasks | No booking for treatment {treatment} was found in the ALS batch for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | The terms wave crosses the threshold | The booked {term} is {booked}. The approved {term} is {approved}. |
| MSG-P1-001 | The ACE batch is late or not complete | {product} is from {date}. Today's data is not yet complete. |
| MSG-P3-027 | No BOOKING_MATCH version is in force for a business date | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-003 | The decision record could not be written during a run | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right calls the rerun | You cannot {action} here. Your role does not include it. |

The business texts are copied unchanged from the legacy story, except MSG-P1-001, which takes the FSD P2 Integration v3 wording (GAP-0659; ASM-1132); the deployment adds the alert routing and the runbook link, never a new wording. For MSG-P3-027 the `{check}` is "no package in force" and the `{detail}` names the package code and the business date only. An alert carries the message ID, the counts, the treatment IDs, the case IDs, the account keys and the run reference, never a name and never a decoded payload. The four thresholds and the run-window expectation are values of the environment (GAP-0659; ASM-1127).

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard of the four series, the Temporal run view of the namespace, the job catalogue read of the integration base and the runbook. The operator view is behind Entra ID: RW-PLATADM operates and reruns, RW-AUDIT reads, and RW-DATASTEW reads the REC-03 break list that the run feeds. SCR-14 Treatment record and SCR-01 My work are served by gateway-bff from rwb-case, rwb-treatment and rwb-access and are not part of this deployment. SCR-44 Interface and job monitor is not used as a new screen: the `job_catalog` row is read through the existing job catalogue operation of this service. The four runbook entries an operator reads are the ones this deployment publishes (GAP-0659; ASM-1128).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2007-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with a pinned digest, the rwb-integration login reference and the rerun reachable |
| TC-P2-E2007-OPS-02 | AC2 | NFR | The migration applied to a fresh schema with the three tables, the library tables, the two indexes and the one JOB-08 row; no other schema granted |
| TC-P2-E2007-OPS-03 | AC3 | NFR | A worker polls `rwb-integration` only; the workflow and six activities are registered; `AceDataReady` starts the run; no Schedule exists |
| TC-P2-E2007-OPS-04 | AC4 | NFR | Four synthetic conditions fire the four alerts with one runbook entry each |
| TC-P2-E2007-OPS-05 | AC5 | NFR | Four simulated runs fill the four series with the environment, the release and the build ID as dimensions |
| TC-P2-E2007-OPS-06 | AC6 | NFR | The flag off ends the run SKIPPED with no write; the backfill handles one date once and replays the stored answer on the same key |

### 17. Guardrails

- No business value in a values file: the package code, the version, the task codes, the treatment types and the message texts are data of the registry, the reference rows and the catalogue, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the runbook or the recorded runs: counts, treatment IDs, case IDs, account keys, role codes, version labels and build IDs only.
- One login per service and one task queue per service: the release carries the rwb-integration login and polls `rwb-integration` only (DP-02, DP-10).
- The release writes `rwb_integration` only and holds no grant on `recovery` or on another `rwb_*` schema; the treatment is written through its contract and the task through rwb-case (DP-01, DP-05, BR4).
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing check never replaces a working release.
- No Schedule is deployed for JOB-08, and a release that creates one fails the review (BR3).
- The flag is the platform library's and its value is read at the start of every run; a paused switch pauses the read and the write.
- No lake target, no lake bucket and no Power BI connection is configured by this release (DP-17).

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next day's ALS load | The deployed run, its trigger, its rerun and the catalogue row | TC-P2-E2007-OPS-01, TC-P2-E2007-OPS-03 |
| REC-03 | Approved treatments against bookings, zero after two days | The four series and the MSG-P2-011 alert | TC-P2-E2007-OPS-04, TC-P2-E2007-OPS-05 |
| R-RES-22, R-SET-13 | A confirmed booking moves the case out of the operations-waiting state | The run that asks for the booking, its counts and its alerts | TC-P2-E2007-OPS-05, TC-P2-E2007-OPS-06 |
| ADR-023 | Observability per service | The four series, the four alerts and the four runbook entries | TC-P2-E2007-OPS-04, TC-P2-E2007-OPS-05 |
| D-RCV-60 | The legacy Quartz job becomes an event-started workflow of the owning service | The worker, the registration, the catalogue row and the backfill | TC-P2-E2007-OPS-03, TC-P2-E2007-OPS-06 |

The requirement ID is the legacy one; this story adds none of its own. The measure REC-03 is P1's reconciliation answer and this release only feeds and observes it.

### 19. Out of scope

- The workflow, the facts builder, the clients and the rerun as code (RWB-P2-E2007-APP).
- The contract documents and the fakes (RWB-P2-E2007-CON); this story deploys and checks the baseline, it does not author it.
- The treatment record, the mark-booked state and the booking difference (the S2 story of this legacy key, behind RWB-P3-E2004-CON).
- The case route state, the tasks and the case timeline (RWB-P3-E2007-APP).
- The ACE account and batch-status reads and the reconciliation answer (RWB-P1-E2007-APP and RWB-P1-E1069-APP).
- The BOOKING_MATCH rows, the registry and the version-in-force promotion (RWB-P7-E2007-APP, RWB-E2-042, RWB-E1-073).
- The authorise contract and the role rows (RWB-P4-E2007-APP, RWB-P4-E1037-CON).
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The flag library, the naming library and the topic provisioning (RWB-PLT-E1047-CON, RWB-PLT-EVT, RWB-PLT-TE006-CON); this release creates no topic.
- The real cross-service proof of the journey (RWB-ITG-E2007-ITG).
- The exact cluster topology, node pools, replica counts and probe timings; they are set per environment by the platform team.
- The gateway-bff composite routes and every screen; the deployment registers no route of its own.
