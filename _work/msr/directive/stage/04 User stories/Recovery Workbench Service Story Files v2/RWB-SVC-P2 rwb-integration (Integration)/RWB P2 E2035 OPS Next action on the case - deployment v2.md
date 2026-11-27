# RWB-P2-E2035-OPS Next action on the case - deployment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2035-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P2-J |
| Ready to start | Day 1 |
| Size | To be sized by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2035-CON (build status Not started) |
| Contract version | /v1 of RWB-P2-E2035-CON (base `/api/recovery/integration/v1`); numbered contract version not specified in the source documents (DOR-RWB-P2-E2035-OPS-23) |
| Integration dependencies | None |
| External dependencies | None |
| Route, harness and evidence values | Not specified in the source documents (GAP-0418); owner integration lead, agreed with QA at wave 2 entry check |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-035 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (9 resolved, 30 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the next action operations of rwb-integration and the `next-action-check` Schedule deployed on the service's own worker and task queue, behind the platform flag, with a backfill and rerun path, five dashboard series, three alerts and a runbook with its entries**, so that **the measure the legacy story sets — no active case without a next action — is observable and operable by a rota from the first release**.

The legacy story assumed that a Quartz job would find the cases with no next action and that someone would read a job monitor when it failed. In the target the fill is a Temporal Schedule on the queue of this service (DP-10), the legacy JOB-05 is retired (Arch v5 slide 44; the Ownership Map ruling on `timer`), and the deployment is where the Schedule becomes real: its cadence, its overlap policy, its catch-up window, its `job_catalog` row, its run view and its alerts.

This story deploys and proves the deployment only. It builds no resolver, no read and no fill: those are the app story of this key, and the contract they answer to is `RWB-P2-E2035-CON`. It writes no case row: the fill writes through the rwb-case contract, and the case row stays rwb-case's. What it owns is the release: the chart, the worker, the Schedule, the flag values, the backfill operation, the five series and the three runbook entries.

### 2. Business rationale

The next action is the measure of the case: the legacy story sets the count of active cases with no next action at a target of zero, and a case can wait for weeks when nobody owns the sweep. Three operational facts make the deployment a story of its own. The resolve is called inside the case transition, so a resolve that fails holds the move; the fill runs unattended every five minutes, so a stalled worker or a paused Schedule leaves cases with no action and no message; and the rule catalog is read on every resolution, so a version that is not in force is a refusal that must be visible rather than a silent empty action.

The deployment therefore carries the state of the sweep as data. Five series answer the questions a rota asks: how many cases were resolved, how many active cases have no next action, how many fills ended with no due date and raised a task, whether the Schedule ran and how long it took, and how many consumed calls failed or answered `NoPackageInForce`. Three alerts carry a message ID and one runbook entry each, so an operator acts without reading code (ADR-023; MSG-P2-023, MSG-P3-027, MSG-GEN-004).

The release also makes the flag real. `rwb.casewf.next-action` is kept as the legacy reference of the switch, and the switch itself is a feature flag of the platform flag library (R-PREC default ruling). Off, the Schedule is paused, the fill writes nothing and the operations answer the feature-off message; on, the sweep runs and the case record header and the case list columns are served. No environment value is hard-coded: the replica counts, the resource sizes, the thresholds, the catch-up window and the backfill limit are values files, as DP-06 requires.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The Temporal workflow kit, the `rwb-recovery` namespace, worker versioning and the build ID provider exist (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The platform flag library is available and the flag `rwb.casewf.next-action` is registered for this service (RWB-PLT-E1047-CON; R-PREC default ruling on feature flags).
- The `rwb_integration` schema and its Flyway sequence exist, with the `job_catalog` row of section 12.7 and the `decision_record` library table (RWB-PLT-E1044-CON; RWB-P2-E2035-CON).
- The platform error envelope and the message catalogue are in force, so an alert can carry a message ID.
- The three operations of `RWB-P2-E2035-CON` are published, with their paths, rights, answers and errors, and their contract fakes answer every consumed path.
- The environments DEV, SIT and UAT exist; the wave 2 release deploys to DEV, SIT and UAT, and the production values are a later promotion of the same artefacts.
- The topics of this service already exist: `rwb.integration.events.v1` with its retry and `.dlt` topics and the shared `rwb.decision-record.v1` (RWB-PLT-EVT, RWB-PLT-TE006-CON). This release adds no topic and registers no consumer group.
- The payload codec and the codec server of the namespace are in force (RWB-PLT-WF).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests of `RWB-P2-E2035-CON`, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the rwb-integration worker with its own login, the namespace `rwb-recovery`, the task queue `rwb-integration`, the payload codec and the build ID of the release.
3. The worker registration step confirms that the worker polls `rwb-integration` only, that `NextActionCheckWorkflow` and its three activities are registered, and that no second task queue is polled.
4. The API step confirms that the three operations answer on `/api/recovery/integration/v1` behind gateway-bff, with the authorise check of rwb-access reachable and the contract fakes replaced by the real services where they are deployed.
5. The Schedule step creates `next-action-check` with the cadence of 5 minutes, the overlap policy SKIP, the catch-up window of the environment and the workflow input, and writes or updates its `job_catalog` row.
6. The flag step sets `rwb.casewf.next-action` from the values of the environment and confirms that the Schedule state and the API answer follow it.
7. The backfill step runs the same workflow for a stated business date, fills only the cases with no next action, reports the counts, and refuses a window that already completed.
8. The dashboards are published with the five series and the environment, the release and the build ID as dimensions.
9. The three alerts are wired to MSG-P2-023, MSG-P3-027 and MSG-GEN-004 and to their runbook entries.
10. A smoke step fills one synthetic case in DEV through the backfill and checks that the answer of the read operation carries the action, the owner, the due date and the rule with its version, and that no second task is raised on a repeat.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render, the image pull or the migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version and no Schedule is created | None | AC1 |
| X2 | The worker polls a task queue other than `rwb-integration`, or the workflow is not registered | The registration check fails the release | None | AC2 |
| X3 | The Schedule cannot be created, or a second Schedule with the same ID exists | The Schedule step fails the release and names the Schedule ID; no partial Schedule is left behind | None | AC3 |
| X4 | The flag is off in an environment and the Schedule still runs, or the fill still writes | The flag step fails the release, because a paused switch must pause the sweep | None | AC4 |
| X5 | A backfill is asked for a window that already completed | The backfill is refused and nothing is filled again | MSG-GEN-004 | AC5 |
| X6 | A fill ends with no due date | One `NEXT_ACTION_MISSING` task is raised through the rwb-case contract, once per case, and the case shows the missing message | MSG-P2-023 | AC6 |
| X7 | No package version is in force for the business date | The resolve answers `NoPackageInForce`, the fill skips the case, and the count and the alert rise for role RW-COE | MSG-P3-027 | AC6 |
| X8 | A consumed contract or the Temporal frontend does not answer inside the budget | The fill skips the case and the next run picks it up; the failure series and the backlog alert fire | MSG-GEN-004, MSG-P3-027 | AC5, AC6 |
| X9 | The worker stops while a run is in flight | The task stays on the queue, the worker returns and the run resumes from history; the stuck-run entry names the check | None | AC2, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the flag library and the published contract; no application code is built here |
| Negotiable | Replica counts, resource sizes, thresholds, the catch-up window, the backfill limit and the scan intervals are environment values |
| Valuable | Makes the sweep observable and operable before the release, so the target of zero cases with no next action can be read from a dashboard |
| Estimable | One chart, one registration check, one API check, one Schedule step, one flag step, one backfill, five series, three alerts and three runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the worker registers, the Schedule runs and is paused, the backfill is idempotent, the alerts fire on a synthetic metric |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the next action operations and the sweep Schedule for rwb-integration

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-integration is rwb-integration
    Given the target environment is SIT
    Given the legacy criteria AC1 to AC14 of RWB-E2-035 are proved by RWB-ITG-E2035-ITG and the criteria below are new (D-RCV-60)

  Scenario: AC1 The service and the three operations are deployed with the rwb-integration login (new, D-RCV-60)
    Given the rwb-integration chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the deployment declares the rwb-integration login and no other service's credential
    Then POST /api/recovery/integration/v1/next-actions:resolve, GET /api/recovery/integration/v1/cases/{caseId}/next-action and POST /api/recovery/integration/v1/cases/{caseId}/next-action answer through gateway-bff in each environment
    Then the readiness probe reports healthy only after the first successful poll and the first successful authorise call, and the liveness probe writes nothing

  Scenario: AC2 The worker registers the sweep workflow and its three activities (new, D-RCV-60)
    Given a running rwb-integration worker
    When the registration step asks the namespace what the worker polls and what it registers
    Then the worker polls rwb-integration and no other task queue
    Then NextActionCheckWorkflow is registered with the workflow ID prefix next-action-check-
    Then findCasesWithoutNextAction, resolveNextAction and fillNextAction are registered with the retry policy of the kit
    Then the payload codec is attached to every client and worker of the deployment
    Then a workflow that ends on NoPackageInForce appears as a non-retryable failure and is counted

  Scenario: AC3 The next-action-check Schedule is created and reported (new, D-RCV-60)
    Given the values file of an environment and the workflow NextActionCheckWorkflow
    When the Schedule step runs
    Then the Schedule next-action-check exists with the cadence of 5 minutes, the overlap policy SKIP and the catch-up window of the environment
    Then its input carries the business date and the run window
    Then one job_catalog row names next-action-check, its schedule text, its owner role, its runbook path and its alert threshold
    Then the Schedule can be paused, resumed and backfilled through the kit operations, and a fire window runs at most one execution
    Then a rerun of a completed fire window is refused with MSG-GEN-004 and fills nothing

  Scenario: AC4 The flag governs the sweep and the operations (new, D-RCV-60)
    Given the flag rwb.casewf.next-action in the platform flag library
    When the flag step reads its values for each environment
    Then the legacy name of the switch is kept and the value comes from the platform flag library, never from a service table
    When the flag is off in an environment
    Then the Schedule is paused and no execution starts
    Then the three operations answer the feature-off message and no case row is written
    When the flag is on
    Then the Schedule resumes, the fill runs and the case record header and the case list columns are served

  Scenario: AC5 The backfill fills only the missing cases and is idempotent (new, D-RCV-60)
    Given 3 active cases with no next action and a decision-log entry that names R-RES-04 of version "RES-2026.12"
    When the backfill step runs NextActionCheckWorkflow for the business date 2026-12-14
    Then each of the 3 cases is filled once through the rwb-case contract and the run reports 3 filled, 0 unchanged, 0 missing and 0 failed
    When the same backfill runs again for the same business date
    Then no case is filled twice, at most one open NEXT_ACTION_MISSING task exists per case, and the run reports 0 filled and 3 unchanged
    Then a backfill for a fire window that already completed is refused with MSG-GEN-004

  Scenario: AC6 The five dashboard series, the three alerts and the runbook cover the sweep (new, D-RCV-60)
    Given the published dashboard, the alert rules and the runbook of the deployment
    When a normal run, a run with no due date, a run with no package in force and a stalled worker are simulated
    Then the dashboard shows the cases resolved per run, the active cases with no next action, the fills with no due date and their tasks, the Schedule run outcomes and durations, and the consumed-call failures with the NoPackageInForce count
    Then each series carries the environment, the release and the build ID as dimensions
    Then the three alerts fire with MSG-P2-023, MSG-P3-027 and MSG-GEN-004 and each links one runbook entry with the check, the owner role and the recovery step
    Then the alert thresholds and the runbook ownership are values of the environment and are not hard-coded

  Scenario: AC7 The release holds the business rules BR1 to BR10 (new, D-RCV-60)
    Given a release of rwb-integration with its chart, values files, Schedule, dashboard, alert rules and runbook
    When the release checks run, including a repeated backfill, a failing release and a partial deploy
    Then the worker polls rwb-integration only in namespace rwb-recovery with the rwb-integration login only (BR1)
    Then every worker carries the build ID of its release with worker versioning enabled, and a new build takes new runs while the old build drains (BR2)
    Then one Schedule ID next-action-check with the overlap policy SKIP and a catch-up window is the only sweep, and no second job fills the same field (BR3)
    Then the fill writes only through the rwb-case contract, and the release writes no case row and holds no grant on another schema (BR4)
    Then the switch is the platform flag library's under its legacy name, and off means a paused Schedule and no write (BR5)
    Then a repeated backfill or rerun leaves at most one open NEXT_ACTION_MISSING task per case and at most one fill per case and business date (BR6)
    Then every alert carries a message ID and the agreed text and links one runbook entry (BR7)
    Then replicas, resources, thresholds, catch-up window, backfill limit and the flag come from values files and the flag library, with none hard-coded (BR8)
    Then dashboard series, alert payloads and the runbook carry counts, case IDs, role codes, rule IDs, version labels and build IDs only, with no personal data and no decoded payload (BR9)
    Then a failing release does not replace the working one, and a partial deploy leaves no paused Schedule running (BR10)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one task queue, one login: the worker polls `rwb-integration` in namespace `rwb-recovery` and carries the rwb-integration login only | Arch v5 slides 24 and 41; DP-02; DP-10 |
| BR2 | Every worker carries the build ID of its release and worker versioning is enabled, so a new build takes new runs while the old build drains | Temporal and Drools design slide 27; RWB-PLT-E1071-CON |
| BR3 | The `next-action-check` Schedule is the only sweep: one Schedule ID, the cadence of 5 minutes, the overlap policy SKIP and a catch-up window, and no second job fills the same field | Legacy JOB-05; Arch v5 slide 44; DP-10 |
| BR4 | The fill writes only through the rwb-case contract; the release writes no case row and holds no grant on another schema | DP-01; DP-15 |
| BR5 | The flag is the platform flag library's, and its legacy name is kept as the reference of the switch; off means a paused Schedule and no write | R-PREC default ruling; BR11 of RWB-P2-E2035-CON |
| BR6 | The backfill and the rerun are idempotent: at most one open `NEXT_ACTION_MISSING` task per case and at most one fill per case and business date | Legacy BR7; AC9 and AC11 of RWB-E2-035 |
| BR7 | Every alert carries a message ID and the agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | No environment value is hard-coded: replicas, resources, thresholds, catch-up window, backfill limit and the flag come from values files and the flag library | DP-06 principle; Template and Rules §R7.2 s17 |
| BR9 | Dashboard series, alert payloads and the runbook carry counts, case IDs, role codes, rule IDs, version labels and build IDs only, never personal data and never a decoded payload | Arch v5 slide 42 (PDPA) |
| BR10 | A failing release never replaces a working one, and a paused Schedule is never left running by a partial deploy | Temporal and Drools design slide 27; DP-10 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Worker registered and probes healthy | The worker polls `rwb-integration` only and the four registrations exist | Ready |
| Ready | Schedule created | The Schedule step writes `next-action-check` and its `job_catalog` row | Sweeping |
| Sweeping | Flag off | `rwb.casewf.next-action` is off in the environment | Paused |
| Paused | Flag on | The flag is on and the Schedule resumes | Sweeping |
| Sweeping | Release superseded | A new chart version passes the tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open runs | Sweeping |
| Sweeping | Consumed contract or Temporal frontend unavailable | The series and the backlog alert rise; the next run picks the cases up | Sweeping (degraded) |
| Any | A failing release or a failed Schedule step | The previous release stays in force and the pipeline stops | Previous state |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the registration check, the Schedule step, the backfill, the dashboards and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the worker versioning policy, the Schedule operations and the flag library registration |
| Platform workflow kit owner | Owns the Schedule conventions, the catch-up window semantics and the codec server |
| Release manager | Approves the promotion of one artefact and may block it on a failed check |
| On-call operator | Runs the three runbook entries and opens an incident when the sweep stalls or `NoPackageInForce` persists |
| RW-COE, center of excellence analyst | Receives the no-version alert, because the package rows are its to load and to approve |
| RW-TEAMMGR, team manager | Works the `NEXT_ACTION_MISSING` tasks the sweep raises |
| RW-PLATADM | Reads the run, the Schedule and the job catalogue in the operator view, not in the cluster |

The worker runs as the rwb-integration service identity (DP-02), carried by the chart as a secret reference and never as a literal name. The identity name is Not specified in the source documents (GAP-0669; ASM-1187).

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, flag values, Schedule cadence and catch-up window, backfill limit | Not specified in the source documents (DOR-RWB-P2-E2035-OPS-7) |
| Task queue | `rwb-integration` in namespace `rwb-recovery`, polled by the rwb-integration worker only | Not specified in the source documents (DOR-RWB-P2-E2035-OPS-7) |
| Schedule | `next-action-check`, every 5 minutes, overlap policy SKIP, catch-up window of the environment, business date and run window input | Not specified in the source documents (DOR-RWB-P2-E2035-OPS-7) |
| Job catalogue row | `job_catalog` of `rwb_integration`: job_id, job_name, owner_role, schedule_text, runbook_path, expected_minutes, alert_after_minutes | Not specified in the source documents (DOR-RWB-P2-E2035-OPS-7) |
| Dashboard series | Cases resolved per run; active cases with no next action; fills with no due date and tasks raised; Schedule run outcomes and durations; consumed-call failures and the `NoPackageInForce` count | Not specified in the source documents (DOR-RWB-P2-E2035-OPS-7) |
| Alerts | Three rules, each with a message ID and one runbook entry | Not specified in the source documents (DOR-RWB-P2-E2035-OPS-7) |
| Runbook entries | Sweep stalled; missing-action backlog and no-due-date fills; no package version in force and consumed-call failure | Not specified in the source documents (DOR-RWB-P2-E2035-OPS-7) |
| Secrets | The rwb-integration login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store | Not specified in the source documents (DOR-RWB-P2-E2035-OPS-7) |
| Test data | The synthetic cases `RW-2026-000401`, `RW-2026-000402` and `RW-2026-000403` in DEV and SIT only; the fixture owner is Not specified in the source documents (GAP-0669; ASM-1189) | Not specified in the source documents (DOR-RWB-P2-E2035-OPS-7) |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread and ingress class) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value, and this story fixes only their names and the rule that they are never hard-coded.

**Probes.** Readiness answers healthy only after the worker has polled `rwb-integration` once, the codec is attached and one authorise call has succeeded; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database, and a failing dependency is reported as not ready, never as live-and-broken. The paths and timings are values of the environment.

### 12. Contract

The read path `GET /api/recovery/integration/v1/cases/{caseId}/next-action` is served by rwb-integration under the integration base (DP-13). rwb-case keeps the case row and the write; the Ownership Map row still has to be corrected to this split (GAP-0667).

#### 12.1 REST operations provided

None. The three operations of this key — the resolve, the read and the fill — are provided by `RWB-P2-E2035-APP` and documented in `RWB-P2-E2035-CON`; this story deploys them and declares no path of its own. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None. The deployment needs no REST client of its own: the worker calls the contracts of rwb-case, rwb-access and rwb-decision inside the activities, and the pipeline calls the platform registry and the secret store only.

#### 12.3 Events published

None of its own. The release publishes no event type: `rwb.integration.events.v1` carries FileDelivered and FileFailed, which belong to the file stories of this service, and the ledger event `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the decision-record library inside the fill.

#### 12.4 Events consumed

None. The release registers no consumer group and subscribes to no topic; the shared topic `rwb.decision-record.v1` and the service topic exist before the release and are used by other stories of the service.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| NextActionCheckWorkflow | Workflow, workflow ID prefix `next-action-check-` | `rwb-integration` | Registered by the worker of this release, with the build ID and worker versioning; started by the Schedule and by the backfill |
| findCasesWithoutNextAction | Activity | `rwb-integration` | Registered with the retry policy of the kit |
| resolveNextAction | Activity | `rwb-integration` | Registered with the same policy; the `NoPackageInForce` outcome is non-retryable and countable |
| fillNextAction | Activity | `rwb-integration` | Registered with the same policy; one rwb-case call, idempotent by case ID and task code |

**Build ID and versioning.** The build ID is the one the workflow kit supplies for the release commit; worker versioning is enabled and a new build takes new runs while the old build drains. The build ID format and the versioning policy are Not specified in the source documents (GAP-0669; ASM-1187).

#### 12.6 Schedules

| Schedule | Cadence | Deployment element |
|---|---|---|
| `next-action-check` | Every 5 minutes | Created by the Schedule step with the workflow `NextActionCheckWorkflow`, the task queue `rwb-integration`, the overlap policy SKIP, the catch-up window of the environment and the business date input; paused and resumed by the flag; backfilled by the backfill step |

The cadence of 5 minutes is the legacy cadence of JOB-05 and is not an environment value. The catch-up window, the overlap window and the backfill limit are Not specified in the source documents (GAP-0669; ASM-1188) and are fixed as values of the environment.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| job_catalog | rwb_integration | P2 (Ownership Map; TSD P2 v3 T3.1) | The row of `next-action-check` is written or updated by the release: job_id, job_name, owner_role, schedule_text, runbook_path, expected_minutes, alert_after_minutes |

The release applies no other migration and adds no other table. The `decision_record` library table, the outbox, the inbox and the idempotency objects are created in `rwb_integration` by the service baseline and by the DB story of the service (DP-15), and the case row is written only through the rwb-case contract (DP-01).

#### 12.8 Contract fakes

None. No fake is deployed: the workflow tests run on `TestWorkflowEnvironment` in the pipeline, and the contract mocks of the consumed services are in-process test doubles of the app and contract stories. No WireMock workload is part of this release.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | The three operations are deployed, not declared here; probes are cluster-internal |
| Kafka | 0 published, 0 consumed | No topic and no consumer group is created by this release |
| Temporal | 1 workflow, 3 activities, 1 Schedule | Worker on `rwb-integration` with a pinned build ID and worker versioning; `next-action-check` every 5 minutes |
| File | None | The values files and the recorded histories are pipeline inputs, not runtime data |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release writes `rwb_integration` only and reaches the case through the rwb-case contract | none |
| DP-03 | DecisionLogWriter, decision log | The decision-record library is deployed with the worker and publishes to `rwb.decision-record.v1` through the outbox | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | The embedded kit is part of the worker image; the catalog row is fetched inside the activity and no second engine runs | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read in this release and no view grant | none |
| DP-06 | Parameters, casewf.config | The parameters and reference rows are read through the rwb-case contracts; the environment values are values files | H RWB-PLT-E1042-CON; RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | The reference-data contract of rwb-case is a runtime dependency of the resolve activity | H RWB-PLT-E1043-CON; RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | The worker, the task queue, the namespace and the `next-action-check` Schedule come from the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The activities call the consumed contracts with the 2 s budget; the deployment adds no REST path | none |
| DP-13 | `/api/recovery/v1` | The deployed base is `/api/recovery/integration/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | The release uses the existing service topic and adds none | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | The per-service Flyway sequence is applied by the baseline; this release adds the `job_catalog` row only | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff serves the runtime path; the deployment registers no route of its own | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-integration/` overlay | Worker deployment, config map, secret references, probes, task queue and namespace, flag reference, build ID, Schedule values |
| `helm/rwb-integration/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, catch-up window, backfill limit, build ID, environment |
| Pipeline stage | Build, unit, component and contract tests, image and dependency scan, chart publish, promotion |
| Registration check | Worker polls `rwb-integration` only; the workflow and three activities are registered; the codec is attached |
| Worker identity | Login and secret reference of rwb-integration: Not specified in the source documents (GAP-0669); the release carries one login and one task queue |
| API check | The three operations answer through gateway-bff and the authorise call succeeds |
| Schedule step | Creates or updates `next-action-check` and its `job_catalog` row; pause, resume and backfill through the kit |
| Flag step | Sets `rwb.casewf.next-action` from the environment and confirms that the Schedule state follows it |
| Backfill step | Runs the workflow for one business date and reports the counts of filled, unchanged, missing and failed |
| Dashboards | The five series of section 11 |
| Alerts | Three rules, each with a message ID and one runbook entry |
| Runbook | Three entries: sweep stalled, missing-action backlog and no-due-date fills, no package version in force and consumed-call failure |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-P2-023 | The active cases with no next action rise above the threshold, or one run raises missing-action tasks for more than the threshold of cases | Missing-action backlog alert with the count, the team codes and the run reference | Team manager of the team and platform on-call, page |
| MSG-P3-027 | The `NoPackageInForce` count is above zero for a business date | No-version alert naming the package code RESTRUCTURE and the business date | Business on-call (RW-COE), page |
| MSG-GEN-004 | The Schedule has not completed a run inside twice its cadence, or a consumed-call failure rate is above the threshold | Sweep-stalled alert with the last run, its outcome and the oldest unfilled case count | Platform on-call, page |

**Backfill and rerun.** The backfill step runs `NextActionCheckWorkflow` for a stated business date with the same input as the Schedule. It fills only the cases with no next action, is idempotent by case ID and task code, and reports the counts. A window that already completed is refused with MSG-GEN-004 and fills nothing; a case that failed on a consumed contract is picked up by the next run, so no repair script exists. The backfill limit per run is a value of the environment (ASM-1188).

**Rollback.** A release that fails a check is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open runs until they finish; the Schedule is paused during the rollback so that the two builds never fill the same case, and it is resumed once one build serves the queue. The fill is idempotent, so no data repair is needed; a case filled twice is answered 200 unchanged by the rwb-case contract.

**Feature switch.** `rwb.casewf.next-action`, kept as the legacy reference of the switch and read from the platform flag library. On: the Schedule runs, the three operations answer and the case record header and the case list columns are served. Off: the Schedule is paused, the fill writes nothing and the operations answer the feature-off message. The flag is never a value of a service table, and its value is read at the start of every run so that a change needs no redeploy.

**Done when.** The chart renders for DEV, SIT and UAT, the registration check passes, the three operations answer through gateway-bff, the Schedule runs and is paused by the flag, the backfill fills only the missing cases and is refused on a completed window, the five series and the three alerts are published, the three runbook entries are reviewed by the on-call rota, and the smoke run of one synthetic case ends with the action, the owner, the due date and the rule version on the case and no second task on a repeat.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-023 | The active cases with no next action cross the threshold, or a run raises missing-action tasks | This case has no next action. It is on the exception list for {team}. |
| MSG-P3-027 | No RESTRUCTURE version is in force for a business date | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-GEN-004 | A backfill is asked for a completed window, or a consumed contract answers a conflict | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | A role without the right calls a Schedule operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The run reads a case outside its scope | This case is not in your scope. |

The business texts are copied unchanged from the legacy story and the platform catalogue; the deployment adds the alert routing and the runbook link, never a new wording. For MSG-P3-027 the `{check}` is "package in force" and the `{table}` names the reference table of the version load, Not specified in the source documents (CG-ALL-3293); the `{detail}` placeholder is not used. An alert carries the message ID, the counts, the case IDs and the run reference, never a name and never a decoded payload.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard of the five series, the Schedule view of the workflow kit, the scheduled-jobs read of the service baseline and the runbook. The operator view is behind Entra ID: RW-PLATADM operates and RW-AUDIT reads. SCR-44 Interface and job monitor is not used as a new screen: the `job_catalog` row is read through the existing job catalogue operation of this service.

SCR-44 states: empty - Not specified in the source documents (CG-ALL-3296); loading - the placeholder while the gateway-bff composite route answers; error - a failed run is shown with its failed check and message ID; no access - a role without the right is refused with MSG-P4-002 and nothing changes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2035-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with a pinned digest, the rwb-integration login reference and the three operations reachable |
| TC-P2-E2035-OPS-02 | AC2 | NFR | A worker polls `rwb-integration` only; the workflow and three activities are registered; the codec is attached; a non-retryable failure is counted |
| TC-P2-E2035-OPS-03 | AC3 | NFR | `next-action-check` created with 5 minutes, SKIP and the catch-up window; its job_catalog row; pause, resume, backfill; a completed window refused |
| TC-P2-E2035-OPS-04 | AC4 | NFR | The flag on and off per environment; the Schedule state and the operation answer follow it; nothing is written when it is off |
| TC-P2-E2035-OPS-05 | AC5 | NFR | Three cases with no next action filled once; the same backfill reporting three unchanged; a completed window refused with MSG-GEN-004 |
| TC-P2-E2035-OPS-06 | AC6 | NFR | Four synthetic conditions raise the five series and the three alerts with one runbook entry each |
| TC-P2-E2035-OPS-07 | AC1, AC2 | Contract | The operations and the activities of §12 checked against RWB-P2-E2035-CON; each is answered or registered as §12.5 states |
| TC-P2-E2035-OPS-08 | AC3 | Boundary | The job_catalog row of §12.7 written at its boundary values, including the catch-up window of the environment |
| TC-P2-E2035-OPS-09 | AC7 (BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10) | NFR | One release checked rule by rule: worker queue, login and build ID; single Schedule; grants; flag off; repeated backfill; alert content; values files; payload scan; failing release and partial deploy |

### 17. Guardrails

- No business value in a values file: the package code, the rule IDs, the route states and the action text are data of the registry and the reference tables, never a deployment value.
- No personal data in logs, dashboard series, alert payloads, the runbook or the recorded runs: counts, case IDs, role codes, rule IDs, version labels and build IDs only.
- One login per service and one task queue per service: the release carries the rwb-integration login and polls `rwb-integration` only (DP-02, DP-10).
- The release writes `rwb_integration` only and holds no grant on `recovery` or on another `rwb_*` schema; the case row is written through the rwb-case contract (DP-01, DP-15).
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing check never replaces a working release.
- One Schedule ID, one cadence: a second job or a second Schedule that fills the same field fails the review (BR3).
- The flag is the platform library's and its value is read at the start of every run; a paused switch pauses the sweep and the write.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-WKM-012 | Every open case carries one next action with owner and due date | The three operations deployed, the Schedule and the cases-resolved series | TC-P2-E2035-OPS-01, TC-P2-E2035-OPS-05 |
| REQ-WKM-013 | The next action comes from the rule that moved the case | The worker image with the embedded kit and the catalog read inside the activity | TC-P2-E2035-OPS-02, TC-P2-E2035-OPS-03 |
| REQ-WKM-016 | A case with no next action is reported as an exception | The missing-action series, the MSG-P2-023 alert and the runbook entry | TC-P2-E2035-OPS-05, TC-P2-E2035-OPS-06 |
| REQ-WKM-014 | Next action visible on the case record and every queue view | The deployed read operation and the case list columns behind gateway-bff | TC-P2-E2035-OPS-01 |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | The overdue marker served by the deployed read, which the escalation story consumes | TC-P2-E2035-OPS-01 |
| ADR-023 | Observability per service | Five dashboard series, three alerts and three runbook entries | TC-P2-E2035-OPS-06 |
| D-RCV-60 | The legacy timer check becomes a Schedule on the owning service | The worker, `next-action-check`, its job_catalog row and the backfill | TC-P2-E2035-OPS-02, TC-P2-E2035-OPS-03, TC-P2-E2035-OPS-04, TC-P2-E2035-OPS-07, TC-P2-E2035-OPS-08, TC-P2-E2035-OPS-09 |

### 19. Out of scope

- The three operations, the resolver, the read composition and the fill as code (RWB-P2-E2035-APP).
- The contract documents and the fakes (RWB-P2-E2035-CON); this story deploys and checks the baseline, it does not author it.
- The write of the case columns, the task lifecycle and the optimistic lock (RWB-P3-E2035-APP).
- The registry rows of the RESTRUCTURE package, the catalog and the ledger (RWB-P7-E2035-APP), and the role rows and the authorise contract (RWB-P4-E2035-APP).
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The flag library and the naming library (RWB-PLT-E1047-CON).
- The topic provisioning and the schema registry (RWB-PLT-EVT, RWB-PLT-TE006-CON); this release adds no topic and registers no consumer.
- The real cross-service proof of the journey (RWB-ITG-E2035-ITG).
- The exact cluster topology, node pools, replica counts and probe timings; they are set per environment by the platform team.
- The gateway-bff composite route and every screen; the deployment registers no route of its own.
